"""Step 10. The agent's lookups served over MCP, and the check that nothing else changed.

Steps 5 to 9 call the four lookups directly, as Python functions. This step puts
the same lookups behind an MCP server (mcp_server.py) and checks, without any
model, that the agent would read exactly the same text through it.

    python 10_tools_over_mcp.py                  list the server's tools; replay every lookup of the stored runs through MCP;
                                                 compare the stored run 'dev_mcp' (made through MCP) with the stored run 'dev'
    python 10_tools_over_mcp.py --run my_dev_mcp compare a run of your own made through MCP instead
    python 10_tools_over_mcp.py --run none       the replay only

A run through MCP is made with:   python 05_run_agent.py --split dev --tools mcp --tag my_dev_mcp

Writes results/mcp_check.md and results/mcp_check.json. Exit code 1 if anything differs.
This step never reads the answer key; the comparison with --run does, through step 6, to score the run.
"""
import argparse
import importlib
import json
import statistics
import sys
import time

from agent.loop import build_case
from agent.mcp_client import McpLookups
from agent.tools import Lookups
from common import EXCEPTIONS_CSV, LEDGER_CSV, RESULTS, read_csv, read_json, write_json
from registry import Registry

RUNS = RESULTS / "runs"
# What must be equal, exception by exception, between a run through MCP and the stored run.
SAME = ["status", "reason", "root_cause", "action", "fix_value", "explanation", "lookups", "evidence", "trace",
        "n_conclusions", "model_calls", "tokens_in", "tokens_out"]


def records(tag):
    path = RUNS / tag / "conclusions.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def replay(ledger, reg, exceptions, by_id):
    """Send every lookup of every stored direct run through MCP and compare with what the run stored."""
    rows, times = [], []
    servers = {}                                   # one server per setting: registry up, registry down
    direct = {down: Lookups(ledger, reg, registry_down=down) for down in (False, True)}
    for run_dir in sorted(p for p in RUNS.iterdir() if (p / "conclusions.jsonl").exists()):
        manifest = read_json(run_dir / "run_manifest.json")
        if manifest.get("tools_via", "direct") != "direct" or manifest.get("model_runs_as", "").startswith("endpoint"):
            continue                               # only the stored laptop runs that called the lookups directly
        down = manifest.get("stress") == "outage"
        if down not in servers:
            servers[down] = McpLookups(registry_down=down)
        n = same_text = same_facts = 0
        for rec in records(run_dir.name):
            case = build_case(exceptions[rec["exception_id"]], by_id)
            for ev in rec["evidence"]:
                t0 = time.perf_counter()
                text, facts = servers[down].run(ev["lookup"], ev["input"], case)
                times.append(time.perf_counter() - t0)
                n += 1
                same_text += text == ev["text"]
                same_facts += facts == direct[down].run(ev["lookup"], ev["input"], case)[1]
        rows.append({"run": run_dir.name, "registry": "down" if down else "up", "lookups": n,
                     "same_text": same_text, "same_facts": same_facts})
    tools = next(iter(servers.values())).tools if servers else []
    for server in servers.values():
        server.close()
    return rows, tools, times


def compare(tag):
    """A run made through MCP against the stored direct run of the same split and stress setting."""
    manifest = read_json(RUNS / tag / "run_manifest.json")
    base = manifest["split"] + ("_" + manifest["stress"] if manifest["stress"] != "none" else "")
    base_manifest = read_json(RUNS / base / "run_manifest.json")
    new, old = {r["exception_id"]: r for r in records(tag)}, {r["exception_id"]: r for r in records(base)}
    differing = {}
    for key in sorted(old):
        if key not in new:
            differing[key] = ["missing from the run"]
            continue
        fields = [f for f in SAME if new[key][f] != old[key][f]]
        if fields:
            differing[key] = fields
    evaluate = importlib.import_module("06_evaluate").evaluate
    stress = None if manifest["stress"] == "none" else manifest["stress"]
    score = evaluate(tag, stress, quiet=True)
    return {
        "run": tag, "stored_run": base, "tools_via": manifest.get("tools_via"), "traced": manifest.get("traced", False),
        "model": manifest["model"], "same_model": manifest["model"] == base_manifest["model"],
        "exceptions": len(old), "identical": len(old) - len(differing), "differing": differing,
        "right": score["right"], "to_a_person": score["to_a_person"], "wrong": score["wrong"],
        "mcp_calls": manifest.get("mcp_calls"), "mcp_seconds": manifest.get("mcp_seconds"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="dev_mcp", help="tag of a run made with 05_run_agent.py --tools mcp, or 'none'")
    ap.add_argument("--out", default="mcp_check", help="name of the report files under results/ (the tests use another name)")
    a = ap.parse_args()

    ledger = read_csv(LEDGER_CSV)
    by_id = {r["line_id"]: r for r in ledger}
    exceptions = {e["exception_id"]: e for e in read_csv(EXCEPTIONS_CSV)}
    rows, tools, times = replay(ledger, Registry(), exceptions, by_id)
    total = sum(r["lookups"] for r in rows)
    ok = all(r["lookups"] == r["same_text"] == r["same_facts"] for r in rows)
    median_ms = round(1000 * statistics.median(times), 1) if times else 0.0

    lines = ["# Step 10. The lookups over MCP", "",
             "The agent's four lookups are served by an MCP server (`mcp_server.py`) and called through an MCP client "
             "(`agent/mcp_client.py`). The server is started as a child process and the two exchange JSON-RPC messages "
             "over its standard input and output.", "",
             "## The tools the server offers", "", "| Tool | Arguments | What it does |", "|---|---|---|"]
    for t in tools:
        lines.append(f'| `{t["name"]}` | {", ".join(t["arguments"])} | {" ".join(t["description"].split())} |')
    lines += ["", "## Every stored lookup, replayed through MCP", "",
              "No model is involved. Each lookup the laptop model asked for in the stored runs is sent through MCP again. "
              "The text that comes back is compared with the text the run stored, and the facts with what the direct call returns.", "",
              "| Stored run | Registry | Lookups replayed | Same text | Same facts |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f'| {r["run"]} | {r["registry"]} | {r["lookups"]} | {r["same_text"]} | {r["same_facts"]} |')
    lines += ["", f"**{sum(r['same_text'] for r in rows)} of {total} lookups returned the same text through MCP, and "
                  f"{sum(r['same_facts'] for r in rows)} of {total} the same facts.** "
                  f"One lookup through MCP took {median_ms} milliseconds at the median, on this machine."]

    result = {"tools": tools, "replay": rows, "lookups_replayed": total, "replay_identical": ok, "median_ms_per_lookup": median_ms}
    if a.run != "none" and (RUNS / a.run / "conclusions.jsonl").exists():
        c = compare(a.run)
        result["run_through_mcp"] = c
        ok = ok and c["identical"] == c["exceptions"]
        lines += ["", "## A run through MCP against the stored run", "",
                  f'Run `{c["run"]}` ({c["model"]}, lookups through MCP' + (", traced" if c["traced"] else "") +
                  f') against the stored run `{c["stored_run"]}` of the same exceptions' +
                  ("" if c["same_model"] else ". The two runs used different models, so differences are expected") + ".", "",
                  f'- **{c["identical"]} of {c["exceptions"]} exceptions are identical** in outcome, cause, fix, explanation, '
                  "every lookup and its result, every step, and the token counts.",
                  f'- Scored against the answer key: {c["right"]} right, {c["to_a_person"]} to a person, {c["wrong"]} wrong.']
        if c["mcp_calls"]:
            lines.append(f'- {c["mcp_calls"]} lookups went through MCP in {c["mcp_seconds"]} seconds in all.')
        for key, fields in c["differing"].items():
            lines.append(f"- {key} differs in: {', '.join(fields)}")
    lines += ["", "## What this does and does not show", "",
              "- It shows that moving the lookups behind MCP changed where they run and nothing the model reads.",
              "- It does not make the agent better or worse. The procedure, the model and the checks are the same.",
              "- The server has no login and listens only to the process that started it. A server offered to other teams "
              "would need both."]
    (RESULTS / f"{a.out}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_json(RESULTS / f"{a.out}.json", result)
    print("\n".join(lines[8:]))
    print("\nPASS" if ok else "\nFAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
