"""Checks of the endpoint path (agent/llm.py, EndpointModel) against a scripted stand-in service.

No model and no network are needed. The stand-in speaks the OpenAI chat format and misbehaves on purpose:
it answers "rate limit reached", refuses a reply format, cuts a reply off, sends back text that is not JSON.
Each check says what the endpoint code must do about it.

    python tests/test_endpoint.py          about 20 seconds; exit code 0 when every check passes

The last three checks run the whole agent loop on two development exceptions with a model that never
returns usable JSON: both must go to a person, and the run must finish.
"""
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from agent import llm  # noqa: E402

SEEN = {}          # what the stand-in was sent, by mode


def example(schema):
    """The simplest object that fits a schema: the first allowed value of every property."""
    if "anyOf" in schema:
        schema = schema["anyOf"][0]
    out = {}
    for key, spec in schema.get("properties", {}).items():
        out[key] = [] if spec.get("type") == "array" else spec["enum"][0] if "enum" in spec else "x"
    return out


def schema_in(body):
    """Find the schema in a request, wherever the reply format put it."""
    fmt = body.get("response_format", {})
    if fmt.get("type") == "json_schema":
        return fmt["json_schema"]["schema"]
    if "schema" in fmt:
        return fmt["schema"]
    for message in reversed(body["messages"]):
        for marker in ("JSON schema: ", "fits this schema: "):
            if marker in message["content"]:
                return json.loads(message["content"].split(marker)[-1])
    raise ValueError("no schema in the request")


class StandIn(BaseHTTPRequestHandler):
    """The first part of the path picks how the service behaves: /ok/v1/..., /busy/v1/..., and so on."""

    def log_message(self, *args):
        pass

    def send(self, code, obj, headers=None):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def reply(self, body, content=None, finish="stop"):
        if content is None:
            content = json.dumps(example(schema_in(body)))
        self.send(200, {"choices": [{"message": {"role": "assistant", "content": content}, "finish_reason": finish}],
                        "usage": {"prompt_tokens": 100, "completion_tokens": 10}})

    def do_POST(self):
        mode = self.path.strip("/").split("/")[0]
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        SEEN.setdefault(mode, []).append(body)
        first = len(SEEN[mode]) == 1
        fmt = body.get("response_format", {})
        if mode == "busy" and first:
            return self.send(429, {"error": {"message": "Rate limit reached"}}, {"Retry-After": "1"})
        if mode == "busy_no_header" and first:
            return self.send(503, {"error": {"message": "overloaded"}})
        if mode == "daily_limit":
            return self.send(429, {"error": {"message": "Rate limit reached for tokens per day"}}, {"Retry-After": "3600"})
        if mode == "plain_json_only" and (fmt.get("type") == "json_schema" or "schema" in fmt):
            return self.send(400, {"error": {"message": "this response_format is not supported"}})
        if mode == "no_json_schema" and fmt.get("type") == "json_schema":
            return self.send(500, {"error": {"message": "Internal Server Error"}})
        if mode == "cut_off" and first:
            return self.reply(body, content="", finish="length")
        if mode == "wrong_key":
            return self.send(401, {"error": {"message": "Invalid API Key"}})
        if mode == "unknown_model":
            return self.send(404, {"error": {"message": "The model does not exist"}})
        if mode == "bad_reply" and not first:
            return self.send(400, {"error": {"message": "Failed to generate JSON.", "code": "json_validate_failed"}})
        if mode == "thinks_first":
            return self.reply(body, content="<think>The record {looks odd}.</think>\n" + json.dumps(example(schema_in(body))))
        if mode == "reasons_first":      # gpt-oss on Amazon Bedrock writes its reasoning into the reply like this
            return self.reply(body, content="<reasoning>The user wants {\"lookup\": ...}. I pick the first lookup.</reasoning>" + json.dumps(example(schema_in(body))))
        if mode == "breaks_schema" and first:
            return self.reply(body, content=json.dumps({"lookup": "not_a_lookup", "input": "x"}))
        if mode == "never_json":
            return self.reply(body, content="I cannot help with that.")
        self.reply(body)


server = ThreadingHTTPServer(("127.0.0.1", 0), StandIn)
PORT = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()

STEP = {"type": "object", "required": ["lookup", "input"],
        "properties": {"lookup": {"type": "string", "enum": ["registry_lookup", "conclude"]}, "input": {"type": "string"}}}
FINAL = {"anyOf": [{"type": "object", "required": ["explanation", "root_cause"],
                    "properties": {"explanation": {"type": "string"}, "root_cause": {"type": "string", "enum": ["CANNOT_CONFIRM"]}}}]}
ASK = [{"role": "system", "content": "You follow the procedure."}, {"role": "user", "content": "EXCEPTION E-000. Step 1?"}]
GOOD = {"lookup": "registry_lookup", "input": "x"}
passed = []


def model(mode):
    return llm.EndpointModel(f"http://127.0.0.1:{PORT}/{mode}/v1", "stand-in", "not-a-real-key")


def check(name, ok, detail=""):
    passed.append(bool(ok))
    print(("PASS  " if ok else "FAIL  ") + name + ("   " + detail if detail else ""))


def stops(mode):
    """Run one request that should stop the run; return the message, or '' if it did not stop."""
    try:
        model(mode).ask(ASK, STEP, 110)
    except SystemExit as e:
        return str(e)
    return ""


# ---- a service that behaves
obj, used = model("ok").ask(ASK, STEP, 110)
sent = SEEN["ok"][0]
check("a good reply comes back, with its token counts", obj == GOOD and used["tokens_in"] == 100 and used["tokens_out"] == 10)
check("the strict json_schema format is asked for first", sent["response_format"]["type"] == "json_schema" and sent["response_format"]["json_schema"]["strict"] is True)
check("temperature is 0 and the token limit is 4 times the local one", sent["temperature"] == 0 and sent["max_tokens"] == 440)
model("ok").ask(ASK, FINAL, 220)
wire = SEEN["ok"][-1]["response_format"]["json_schema"]["schema"]
check("every object in the strict schema is closed, and the caller's schema is left alone",
      wire["anyOf"][0]["additionalProperties"] is False and "additionalProperties" not in FINAL["anyOf"][0])

check("with LLM_REASONING_EFFORT unset, the request does not mention reasoning effort", "reasoning_effort" not in sent)
os.environ["LLM_REASONING_EFFORT"] = "low"
model("effort").ask(ASK, STEP, 110)
del os.environ["LLM_REASONING_EFFORT"]
check("with LLM_REASONING_EFFORT=low, the request carries it", SEEN["effort"][0].get("reasoning_effort") == "low")

# ---- a busy service
start = time.time()
obj, used = model("busy").ask(ASK, STEP, 110)
check("rate limit: waits as long as the service says, then asks again", obj == GOOD and 1 <= time.time() - start < 4 and len(SEEN["busy"]) == 2)
start = time.time()
obj, used = model("busy_no_header").ask(ASK, STEP, 110)
check("busy with no wait time given: waits 5 seconds, then asks again", obj == GOOD and 5 <= time.time() - start < 8)
said = stops("daily_limit")
check("daily limit: stops at once and says the run can be continued", "about 60 minutes" in said and "Run the same command again" in said and len(SEEN["daily_limit"]) == 1)

# ---- a service that does not take the reply format
m = model("plain_json_only")
obj, used = m.ask(ASK, STEP, 110)
last = SEEN["plain_json_only"][-1]
check("falls back to plain json_object and puts the schema in the prompt",
      obj == GOOD and m.format == 2 and last["response_format"] == {"type": "json_object"} and "JSON schema: " in last["messages"][-1]["content"])
m.ask(ASK, STEP, 110)
check("and keeps that format for the next request", len(SEEN["plain_json_only"]) == 4)
m = model("no_json_schema")
obj, used = m.ask(ASK, STEP, 110)
check("an HTTP 500 on json_schema steps down to json_object plus schema (llama.cpp servers)", obj == GOOD and m.format == 1)

# ---- replies that cannot be used
obj, used = model("cut_off").ask(ASK, STEP, 110)
one, two = SEEN["cut_off"]
check("a reply cut off by the token limit is asked for again with twice the room", obj == GOOD and (one["max_tokens"], two["max_tokens"]) == (440, 880))
obj, used = model("thinks_first").ask(ASK, STEP, 110)
check("reasoning inside <think> tags is set aside", obj == GOOD and len(SEEN["thinks_first"]) == 1)
obj, used = model("reasons_first").ask(ASK, STEP, 110)
check("reasoning inside <reasoning> tags is set aside, braces and all", obj == GOOD and len(SEEN["reasons_first"]) == 1)
obj, used = model("breaks_schema").ask(ASK, STEP, 110)
check("a reply that breaks the schema is sent back with the reason", obj == GOOD and "not usable" in SEEN["breaks_schema"][1]["messages"][-1]["content"])
m = model("bad_reply")
m.ask(ASK, STEP, 110)
try:
    m.ask(ASK, STEP, 110)
    failed = ""
except RuntimeError as e:
    failed = str(e)
check("a reply the service cannot read, three times over, raises an error and keeps the format", "after 3 tries" in failed and m.format == 0)

# ---- refusals stop the run and show what the service said
said = stops("wrong_key")
check("a wrong key stops the run", "HTTP 401" in said and "Invalid API Key" in said)
said = stops("unknown_model")
check("an unknown model stops the run", "HTTP 404" in said and "does not exist" in said)
try:
    llm.EndpointModel("http://127.0.0.1:9/v1", "stand-in").ask(ASK, STEP, 110)
    said = ""
except SystemExit as e:
    said = str(e)
check("a service that cannot be reached stops the run", "Could not reach" in said)

# ---- the whole loop with a model that never returns usable JSON
tag = "zz_endpoint_test"
run_dir = ROOT / "results" / "runs" / tag
shutil.rmtree(run_dir, ignore_errors=True)
env = dict(os.environ, LLM_BASE_URL=f"http://127.0.0.1:{PORT}/never_json/v1", LLM_MODEL="stand-in", LLM_API_KEY="not-a-real-key")
env.pop("LLM_MODEL_PATH", None)
run = subprocess.run([sys.executable, "05_run_agent.py", "--split", "dev", "--limit", "2", "--tag", tag], cwd=ROOT, env=env, capture_output=True, text=True)
rows = [json.loads(line) for line in open(run_dir / "conclusions.jsonl")] if (run_dir / "conclusions.jsonl").exists() else []
check("loop: the run finishes", run.returncode == 0 and len(rows) == 2, run.stderr[-200:])
check("loop: both exceptions go to a person, with the reason",
      len(rows) == 2 and all(r["status"] == "to a person" and r["root_cause"] == "CANNOT_CONFIRM" and "no usable answer" in r["last_problems"][0] for r in rows))
manifest = json.load(open(run_dir / "run_manifest.json")) if (run_dir / "run_manifest.json").exists() else {}
check("loop: the run manifest names the endpoint and does not hold the key",
      manifest.get("model_runs_as", "").startswith("endpoint http://127.0.0.1") and "not-a-real-key" not in json.dumps(manifest))
shutil.rmtree(run_dir, ignore_errors=True)

print(f"\n{sum(passed)} of {len(passed)} checks passed")
sys.exit(0 if all(passed) else 1)
