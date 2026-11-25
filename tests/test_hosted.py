"""Checks of steps 10 to 12 together, against a stand-in service that replays the laptop model's stored answers.

No model, no network and no key are needed. The stand-in speaks the OpenAI chat format. For each request it
finds the exception in the conversation and sends back the answer the laptop model gave at that point in the
stored run. So the whole hosted path (step 12, with the lookups through MCP and tracing on) must reproduce the
audited laptop results exactly: 35 of 35 on development, then 88 right, 7 to a person and 0 wrong on the test.

A second stand-in answers every request with the first value the schema allows. It must fail the regression
check, and step 12 must then stop without running the test.

    python tests/test_hosted.py          about a minute; exit code 0 when every check passes
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "results" / "runs"
STORED = ["dev", "test", "test_note", "test_outage"]
passed = []


def check(name, ok, detail=""):
    passed.append(bool(ok))
    print(("PASS  " if ok else "FAIL  ") + name + ("   " + str(detail) if detail else ""), flush=True)


def records(tag):
    path = RUNS / tag / "conclusions.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def answers(rec):
    """The model's answers for one exception, in order, read from the stored steps."""
    out = []
    for step in rec["trace"]:
        if step["lookup"] != "CONCLUSION":
            out.append({"lookup": step["lookup"], "input": step["input"]})
        elif "no usable answer" not in step.get("check", "") and '"No lookup was completed."' not in step["result"]:
            out.append(json.loads(step["result"]))
    return out


REPLAY = {tag: {r["exception_id"]: answers(r) for r in records(tag)} for tag in STORED}
CALLS = {tag: {r["exception_id"]: r["model_calls"] for r in records(tag)} for tag in STORED}


def example(schema):
    if "anyOf" in schema:
        schema = schema["anyOf"][0]
    return {k: [] if s.get("type") == "array" else s["enum"][0] if "enum" in s else "x" for k, s in schema.get("properties", {}).items()}


class StandIn(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        mode = self.path.strip("/").split("/")[0]
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if mode == "first_allowed":
            content = json.dumps(example(body["response_format"]["json_schema"]["schema"]))
        else:
            text = "\n".join(m["content"] for m in body["messages"])
            exception_id = re.search(r"EXCEPTION (E-\d+)", text).group(1)
            said = sum(m["role"] == "assistant" for m in body["messages"])
            if 'Note on the line: "' in text:
                run = "test_note"
            elif "REGISTRY UNAVAILABLE" in text:
                run = "test_outage"
            else:
                run = "dev" if exception_id in REPLAY["dev"] else "test"
            content = json.dumps(REPLAY[run][exception_id][said])
        data = json.dumps({"choices": [{"message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
                           "usage": {"prompt_tokens": 100, "completion_tokens": 10}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


server = ThreadingHTTPServer(("127.0.0.1", 0), StandIn)
PORT = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
scratch = tempfile.mkdtemp()


def clean(name):
    for stored in STORED:
        shutil.rmtree(RUNS / f"hosted_{name}_{stored}", ignore_errors=True)
    for ending in (".md", ".json"):
        (ROOT / "results" / "hosted" / (name + ending)).unlink(missing_ok=True)
    try:
        (ROOT / "results" / "hosted").rmdir()          # only when the tests left it empty
    except OSError:
        pass


def step_12(name, mode, *options):
    clean(name)
    env = dict(os.environ, LLM_BASE_URL=f"http://127.0.0.1:{PORT}/{mode}/v1", LLM_MODEL="stand-in", LLM_API_KEY="not-a-real-key",
               MLFLOW_TRACKING_URI="sqlite:///" + (Path(scratch) / "traces.db").as_posix(), MLFLOW_DISABLE_AGENT_HINT="1")
    env.pop("LLM_MODEL_PATH", None)
    return subprocess.run([sys.executable, "12_hosted_model.py", "--name", name, *options], cwd=ROOT, env=env, capture_output=True, text=True)


# ---- the stored runs can be replayed at all
check("every stored exception's answers can be read back, one per model call",
      all(len(REPLAY[t][k]) == CALLS[t][k] for t in STORED for k in REPLAY[t]))
check("the registry-down run starts each exception the way the normal test run does",
      all(REPLAY["test_outage"][k][0] == REPLAY["test"][k][0] for k in REPLAY["test_outage"]))

# ---- the whole hosted path, replaying the laptop model: lookups through MCP, tracing on, priced
run = step_12("zz_replay", "replay", "--tools", "mcp", "--trace", "--price-in", "1", "--price-out", "2")
report_file = ROOT / "results" / "hosted" / "zz_replay.json"
report = json.load(open(report_file)) if report_file.exists() else {"stages": []}
check("step 12 finishes and the regression check passes", run.returncode == 0 and report.get("regression_passed") is True, run.stderr[-300:])
check("all four stages ran: development, test, and the two stress tests", len(report["stages"]) == 4)
for stage, stored in zip(report["stages"], STORED):
    laptop = json.load(open(RUNS / stored / "evaluation.json"))
    got = (stage["right"], stage["to_a_person"], stage["wrong"])
    check(f"{stored}: scored the same as the laptop run, {got[0]} right, {got[1]} to a person, {got[2]} wrong",
          got == (laptop["right"], laptop["to_a_person"], laptop["wrong"]) and stage["exceptions"] == laptop["exceptions"])
    new = {r["exception_id"]: r for r in records(stage["run"])}
    old = {r["exception_id"]: r for r in records(stored)}
    same = ["status", "root_cause", "action", "fix_value", "explanation", "lookups", "evidence", "trace", "n_conclusions", "model_calls"]
    differing = [k for k in old if k not in new or any(new[k][f] != old[k][f] for f in same)]
    check(f"{stored}: every exception identical to the stored run, step by step", not differing, differing[:5])
    calls = sum(r["model_calls"] for r in new.values())
    check(f"{stored}: tokens and cost add up from the calls",
          stage["tokens_in"] == 100 * calls and stage["tokens_out"] == 10 * calls and abs(stage["cost_dollars"] - (100 * calls + 2 * 10 * calls) / 1e6) < 1e-4)
manifest = json.load(open(RUNS / "hosted_zz_replay_test" / "run_manifest.json")) if (RUNS / "hosted_zz_replay_test").exists() else {}
check("the run manifest says the lookups went through MCP and the run was traced, and does not hold the key",
      manifest.get("tools_via") == "mcp" and manifest.get("traced") is True and manifest.get("mcp_calls", 0) > 0 and "not-a-real-key" not in json.dumps(manifest))
env = dict(os.environ, MLFLOW_TRACKING_URI="sqlite:///" + (Path(scratch) / "traces.db").as_posix(), MLFLOW_DISABLE_AGENT_HINT="1")
traced = subprocess.run([sys.executable, "11_trace_report.py", "--tag", "hosted_zz_replay_test"], cwd=ROOT, env=env, capture_output=True, text=True)
trace_file = RUNS / "hosted_zz_replay_test" / "trace_report.json"
trace_report = json.load(open(trace_file)) if trace_file.exists() else {}
check("step 11 reads back one trace per test exception, and every trace agrees with the run's record",
      traced.returncode == 0 and trace_report.get("traces") == 95 and trace_report.get("agree_with_record") == 95, traced.stderr[-300:])
mcp_check = subprocess.run([sys.executable, "10_tools_over_mcp.py", "--run", "hosted_zz_replay_dev", "--out", "zz_mcp_check"], cwd=ROOT, capture_output=True, text=True)
found = json.load(open(ROOT / "results" / "zz_mcp_check.json")) if (ROOT / "results" / "zz_mcp_check.json").exists() else {}
differing = found.get("run_through_mcp", {}).get("differing", {})
check("step 10: all 374 stored lookups come back the same through MCP", found.get("replay_identical") is True and sum(r["lookups"] for r in found.get("replay", []) if r["run"] in ("dev", "dev_smaller_model", "test", "test_note", "test_outage", "test_recheck_after_hardening")) == 374)
check("step 10: the run through MCP matches the stored development run in everything but the stand-in's own token counts",
      len(differing) == 35 and all(fields == ["tokens_in", "tokens_out"] for fields in differing.values()), mcp_check.stderr[-300:])
for ending in (".md", ".json"):
    (ROOT / "results" / ("zz_mcp_check" + ending)).unlink(missing_ok=True)
clean("zz_replay")

# ---- a model that fails the regression check never sees the test
run = step_12("zz_gate", "first_allowed")
report_file = ROOT / "results" / "hosted" / "zz_gate.json"
report = json.load(open(report_file)) if report_file.exists() else {"stages": []}
text = (ROOT / "results" / "hosted" / "zz_gate.md").read_text(encoding="utf-8") if report_file.exists() else ""
check("a model that fails the regression check: step 12 exits with a failure", run.returncode == 1 and report.get("regression_passed") is False, run.stderr[-300:])
check("and the test is never run for it", len(report["stages"]) == 1 and not (RUNS / "hosted_zz_gate_test").exists() and "was not run on the test" in text)
clean("zz_gate")

# ---- --regression-only stops after the development exceptions even when the check passes
run = step_12("zz_only", "replay", "--regression-only")
report_file = ROOT / "results" / "hosted" / "zz_only.json"
report = json.load(open(report_file)) if report_file.exists() else {"stages": []}
check("--regression-only passes the check and stops before the test", run.returncode == 0 and len(report["stages"]) == 1 and not (RUNS / "hosted_zz_only_test").exists())
check("with no price given, no cost is claimed", report["stages"] and report["stages"][0]["cost_dollars"] is None and report.get("total_cost_dollars") is None)
clean("zz_only")
shutil.rmtree(scratch, ignore_errors=True)

print(f"\n{sum(passed)} of {len(passed)} checks passed")
sys.exit(0 if all(passed) else 1)
