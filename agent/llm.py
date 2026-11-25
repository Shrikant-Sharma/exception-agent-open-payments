"""One small interface to a language model: send messages, get back JSON that fits a schema.

Two ways to run, chosen by environment variables, so nothing else in the project
knows or cares which model is behind it.

  Local file (default)      LLM_MODEL_PATH=/path/to/model.gguf
                            Runs on the CPU with llama-cpp-python. No key, no network.
                            The JSON schema is enforced while the model writes, so the
                            output always parses.

  Any OpenAI-compatible     LLM_BASE_URL=https://api.groq.com/openai/v1   (or Amazon Bedrock, Ollama, vLLM, ...)
  endpoint                  LLM_API_KEY=...   LLM_MODEL=model-name
                            The schema is requested from the service and checked here.
                            A busy service or a rate limit is waited out; a refusal stops the run.

Temperature is 0 in both, so a rerun on the same model gives the same answers.
"""
import json
import os
import re
import time

import requests


def fits(obj, schema):
    """A minimal schema check: required keys, allowed values, types. Returns a problem or None."""
    if not isinstance(obj, dict):
        return "not a JSON object"
    if "anyOf" in schema:                      # the object must fit one of the listed shapes
        problems = [fits(obj, alt) for alt in schema["anyOf"]]
        return None if None in problems else problems[0]
    for key in schema.get("required", []):
        if key not in obj:
            return f"missing '{key}'"
    for key, spec in schema.get("properties", {}).items():
        if key not in obj:
            continue
        v = obj[key]
        if spec.get("type") == "string":
            if not isinstance(v, str):
                return f"'{key}' is not text"
            if "enum" in spec and v not in spec["enum"]:
                return f"'{key}' must be one of {spec['enum']}"
        if spec.get("type") == "array":
            if not isinstance(v, list):
                return f"'{key}' is not a list"
            allowed = spec.get("items", {}).get("enum")
            if allowed and any(x not in allowed for x in v):
                return f"'{key}' may only contain {allowed}"
    return None


def json_object_in(text):
    """The JSON object in a reply. A service can put a stray opening in front of it (Bedrock was seen to send
    '{"{"lookup": ...}'), so each opening brace is tried in turn. The caller still checks the result against the schema."""
    end = text.rindex("}") + 1
    start = text.index("{")
    while True:
        try:
            return json.loads(text[start:end])
        except ValueError:
            start = text.index("{", start + 1)        # raises ValueError when no opening brace is left


class LocalModel:
    def __init__(self, path, threads=None, context=4096):
        from llama_cpp import Llama
        self.name = os.path.basename(path)
        self.kind = "local file, llama-cpp-python"
        self.llm = Llama(model_path=path, n_ctx=context, n_threads=threads or os.cpu_count(),
                         n_batch=256, seed=7, verbose=False)
        # Optional text for the end of the system message. Qwen3 models read "/no_think" there as
        # "answer directly", which is how they are meant to be used when the reply must be JSON.
        self.system_suffix = os.environ.get("LLM_SYSTEM_SUFFIX", "")

    def ask(self, messages, schema, max_tokens):
        t0 = time.time()
        if self.system_suffix and messages and messages[0]["role"] == "system":
            messages = [dict(messages[0], content=messages[0]["content"] + "\n" + self.system_suffix)] + messages[1:]
        tokens_in = tokens_out = 0
        for limit in (max_tokens, 2 * max_tokens):       # if the reply was cut off before the JSON closed, allow more room once
            out = self.llm.create_chat_completion(messages=messages, temperature=0, max_tokens=limit,
                                                  response_format={"type": "json_object", "schema": schema})
            usage = out.get("usage", {})
            tokens_in += usage.get("prompt_tokens", 0)
            tokens_out += usage.get("completion_tokens", 0)
            try:
                obj = json.loads(out["choices"][0]["message"]["content"])
                break
            except ValueError:
                obj = None
        if obj is None:
            raise RuntimeError("The model's reply was cut off before the JSON closed, twice.")
        return obj, {"seconds": round(time.time() - t0, 2), "tokens_in": tokens_in, "tokens_out": tokens_out}


class EndpointModel:
    """Any service that speaks the OpenAI chat format: Groq, Ollama, a llama.cpp server, vLLM and others.

    Services differ in how they take a schema, so three reply formats are tried in order and the first one
    the service accepts is kept:
      0  json_schema, strict      (OpenAI, Groq on some models, Ollama)
      1  json_object plus schema  (llama.cpp servers)
      2  json_object              (everything else; the schema then goes into the prompt)
    Whatever the service does with the schema, the reply is checked against it here.

    Three things a hosted service does that a model file does not:
      - it answers "busy" or "rate limit reached": wait as long as it says, then ask again
      - a model that reasons before it answers can spend the token limit on the reasoning: allow more room
      - it can refuse outright (wrong key, unknown model): stop the run and show what it said.
        Finished exceptions are stored, so the same command picks up where it stopped.
    """
    FORMAT_REJECTED = (400, 404, 422, 500, 501)      # how services answer a reply format they do not take
    BUSY = (429, 502, 503, 504)
    MAX_WAITS = 8                                    # times one request will wait on a busy service
    LONGEST_WAIT = 90                                # seconds; a longer wait means a daily limit, so stop instead
    BAD_REPLY = ("json_validate_failed", "failed_generation", "Failed to generate",
                 "does not match the expected schema")       # the service could not use the model's reply

    def __init__(self, base_url, model, api_key=""):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.name = model
        self.kind = "endpoint " + base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = "Bearer " + api_key
        self.format = 0
        self.answered = False                        # has the service answered at least once in this run
        self.system_suffix = os.environ.get("LLM_SYSTEM_SUFFIX", "")
        self.room = int(os.environ.get("LLM_TOKEN_ROOM", "4"))    # the token limit is this many times the local one
        # Optional, for models that reason before they answer (gpt-oss): low, medium or high. Unset, the request does not mention it.
        self.reasoning_effort = os.environ.get("LLM_REASONING_EFFORT", "")

    @staticmethod
    def _closed(schema):
        """The strict format wants every object to say it takes no other properties. Returns a copy that does."""
        if isinstance(schema, list):
            return [EndpointModel._closed(x) for x in schema]
        if not isinstance(schema, dict):
            return schema
        out = {k: EndpointModel._closed(v) for k, v in schema.items()}
        if out.get("type") == "object":
            out["additionalProperties"] = False
        return out

    def _stop(self, why):
        raise SystemExit(why + "\nFinished exceptions are stored. Run the same command again to continue.")

    def _wait(self, r, waits):
        """Seconds to wait on a busy service: what it says in Retry-After, or a little longer each time."""
        try:
            seconds = float(r.headers.get("retry-after", ""))
        except ValueError:
            seconds = 5 * waits
        if seconds > self.LONGEST_WAIT:
            self._stop(f"The model service says its limit is reached and to come back in about {round(seconds / 60)} minutes.")
        return max(seconds, 1)

    def _post(self, messages, schema, max_tokens):
        """One request. Returns (reply, None), or (None, problem) when the service could not use the model's reply."""
        waits = 0
        while True:
            fmt = [{"type": "json_schema", "json_schema": {"name": "reply", "schema": self._closed(schema), "strict": True}},
                   {"type": "json_object", "schema": schema},
                   {"type": "json_object"}][self.format]
            msgs = messages
            if self.format == 2:          # no schema on the wire: put it in the prompt
                msgs = messages[:-1] + [dict(messages[-1], content=messages[-1]["content"]
                                             + "\nReply with one JSON object that fits this JSON schema: " + json.dumps(schema))]
            body = {"model": self.name, "messages": msgs, "temperature": 0, "max_tokens": max_tokens, "response_format": fmt}
            if self.reasoning_effort:
                body["reasoning_effort"] = self.reasoning_effort
            try:
                r = requests.post(self.url, headers=self.headers, json=body, timeout=300)
            except requests.RequestException as e:
                self._stop(f"Could not reach the model service at {self.url}: {e}")
            if r.ok:
                self.answered = True
                return r.json(), None
            said = r.text[:400]
            if r.status_code in self.BUSY or (r.status_code == 500 and self.format == 2):
                waits += 1
                if waits > self.MAX_WAITS:
                    self._stop(f"The model service is still busy after {self.MAX_WAITS} waits (HTTP {r.status_code}: {said}).")
                time.sleep(self._wait(r, waits))
                continue
            if r.status_code == 400 and any(w in said for w in self.BAD_REPLY):
                return None, "the service could not read the reply as JSON"
            if r.status_code in self.FORMAT_REJECTED and self.format < 2:
                self.format += 1
                continue
            if r.status_code == 400 and self.answered:
                return None, "the service turned the request down"
            self._stop(f"The model service answered HTTP {r.status_code}: {said}\nCheck LLM_BASE_URL, LLM_MODEL and LLM_API_KEY.")

    def ask(self, messages, schema, max_tokens):
        t0 = time.time()
        if self.system_suffix and messages and messages[0]["role"] == "system":
            messages = [dict(messages[0], content=messages[0]["content"] + "\n" + self.system_suffix)] + messages[1:]
        tokens_in = tokens_out = 0
        room = max_tokens * self.room
        problem = None
        for attempt in range(3):
            msgs = messages if problem is None else messages + [
                {"role": "user", "content": f"Your last reply was not usable ({problem}). Reply with one JSON object that fits this schema: {json.dumps(schema)}"}]
            out, problem = self._post(msgs, schema, room)
            if out is None:
                continue
            usage = out.get("usage") or {}
            tokens_in += usage.get("prompt_tokens", 0)
            tokens_out += usage.get("completion_tokens", 0)
            choice = out["choices"][0]
            # Reasoning that some models write before the answer, inside the reply: <think> (Qwen) or <reasoning> (gpt-oss on Bedrock).
            text = re.sub(r"<(think|reasoning)>.*?</\1>", "", choice["message"].get("content") or "", flags=re.S)
            try:
                obj = json_object_in(text)
                problem = fits(obj, schema)
            except ValueError:
                obj = None
                if choice.get("finish_reason") == "length":       # the limit ran out, on reasoning or on the reply: allow twice the room
                    problem, room = "it was cut off before the JSON closed", room * 2
                else:
                    problem = "it was not valid JSON"
            if problem is None:
                return obj, {"seconds": round(time.time() - t0, 2), "tokens_in": tokens_in, "tokens_out": tokens_out}
        raise RuntimeError(f"The model did not return usable JSON after 3 tries: {problem}")


def get_model():
    if os.environ.get("LLM_BASE_URL"):
        return EndpointModel(os.environ["LLM_BASE_URL"], os.environ.get("LLM_MODEL", ""), os.environ.get("LLM_API_KEY", ""))
    path = os.environ.get("LLM_MODEL_PATH", "")
    if not path or not os.path.exists(path):
        raise SystemExit("Set LLM_MODEL_PATH to a .gguf model file, or LLM_BASE_URL / LLM_MODEL / LLM_API_KEY for an endpoint. See README, 'How to run it'.")
    return LocalModel(path, threads=int(os.environ["LLM_THREADS"]) if os.environ.get("LLM_THREADS") else None)
