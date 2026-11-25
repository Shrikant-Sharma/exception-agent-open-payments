"""Step 11. Read the traces of a run back from MLflow and say what they hold.

A run made with --trace writes one trace per exception (agent/tracing.py):
a root span for the exception, one span for every model call and one for every
lookup. This step reads those traces back and checks them against the run's own
record, so the traces can be trusted when something has to be looked up later.

    python 05_run_agent.py --split dev --trace --tag dev_traced      make a traced run
    python 11_trace_report.py --tag dev_traced                        read it back

Writes results/runs/<tag>/trace_report.md and trace_report.json.
To look at the same traces in a browser:  mlflow ui --backend-store-uri sqlite:///mlflow.db
"""
import argparse
import json
import os
import statistics
import sys

from common import RESULTS, ROOT, read_json, write_json

EXPERIMENT = "exception-agent"


def ms(span):
    return (span.end_time_ns - span.start_time_ns) / 1e6


def short(value, limit=96):
    text = value if isinstance(value, str) else json.dumps(value)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


def tree(trace, usage_key):
    """One trace as indented text: the root span, then its steps in the order they ran."""
    spans = sorted(trace.data.spans, key=lambda s: s.start_time_ns)
    root = next(s for s in spans if s.parent_id is None)
    out = [f"{root.name}   {root.span_type}   {ms(root) / 1000:.1f} s   -> {short(root.outputs)}"]
    for s in spans:
        if s.parent_id is None:
            continue
        if s.span_type == "CHAT_MODEL":
            u = s.get_attribute(usage_key) or {}
            out.append(f'  model call        CHAT_MODEL   {ms(s) / 1000:5.1f} s   {u.get("input_tokens", 0):,} tokens in, '
                       f'{u.get("output_tokens", 0)} out   -> {short(s.outputs)}')
        else:
            out.append(f'  {s.name:17s} TOOL         {ms(s):5.1f} ms  {short((s.inputs or {}).get("input", ""), 30)}   -> {short((s.outputs or {}).get("text", ""))}')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    run_dir = RESULTS / "runs" / a.tag
    manifest = read_json(run_dir / "run_manifest.json")
    if not manifest.get("traced"):
        sys.exit(f"Run '{a.tag}' was not made with --trace.")

    import mlflow
    from mlflow.tracing.constant import SpanAttributeKey
    if not os.environ.get("MLFLOW_TRACKING_URI"):
        mlflow.set_tracking_uri("sqlite:///" + (ROOT / "mlflow.db").as_posix())
    experiment = mlflow.get_experiment_by_name(EXPERIMENT)
    if experiment is None:
        sys.exit("No MLflow experiment named 'exception-agent' was found. Make a run with --trace first.")
    traces = mlflow.search_traces(locations=[experiment.experiment_id], filter_string=f"tags.run = '{a.tag}'",
                                  return_type="list", include_spans=True, max_results=5000)
    latest = {}                                    # one trace per exception; a rerun of an exception keeps its newest trace
    for t in sorted(traces, key=lambda t: t.info.request_time):
        latest[t.info.tags["exception_id"]] = t
    records = {r["exception_id"]: r for r in (json.loads(line) for line in (run_dir / "conclusions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())}

    by_type = {"AGENT": {"spans": 0, "seconds": 0.0}, "CHAT_MODEL": {"spans": 0, "seconds": 0.0, "tokens_in": 0, "tokens_out": 0},
               "TOOL": {"spans": 0, "seconds": 0.0}}
    per_trace, agree, disagree = [], 0, []
    for key, rec in records.items():
        t = latest.get(key)
        if t is None:
            disagree.append(f"{key}: no trace")
            continue
        calls = [s for s in t.data.spans if s.span_type == "CHAT_MODEL"]
        tools = [s for s in t.data.spans if s.span_type == "TOOL"]
        root = next(s for s in t.data.spans if s.parent_id is None)
        tokens_in = sum((s.get_attribute(SpanAttributeKey.CHAT_USAGE) or {}).get("input_tokens", 0) for s in calls)
        tokens_out = sum((s.get_attribute(SpanAttributeKey.CHAT_USAGE) or {}).get("output_tokens", 0) for s in calls)
        for kind, spans in (("AGENT", [root]), ("CHAT_MODEL", calls), ("TOOL", tools)):
            by_type[kind]["spans"] += len(spans)
            by_type[kind]["seconds"] += sum(ms(s) for s in spans) / 1000
        by_type["CHAT_MODEL"]["tokens_in"] += tokens_in
        by_type["CHAT_MODEL"]["tokens_out"] += tokens_out
        per_trace.append({"exception_id": key, "spans": len(t.data.spans), "seconds": ms(root) / 1000})
        same = (len(calls) == rec["model_calls"] and [s.name for s in sorted(tools, key=lambda s: s.start_time_ns)] == rec["lookups"]
                and tokens_in == rec["tokens_in"] and tokens_out == rec["tokens_out"]
                and (root.outputs or {}).get("status") == rec["status"] and (root.outputs or {}).get("root_cause") == rec["root_cause"])
        if same:
            agree += 1
        else:
            disagree.append(f"{key}: the trace and the run's record differ")
    for kind in by_type:
        by_type[kind]["seconds"] = round(by_type[kind]["seconds"], 1)

    n = len(records)
    spans = [p["spans"] for p in per_trace]
    seconds = [p["seconds"] for p in per_trace]
    model_s, tool_s, all_s = by_type["CHAT_MODEL"]["seconds"], by_type["TOOL"]["seconds"], by_type["AGENT"]["seconds"]
    # the trace to print: one where a check sent a conclusion back, if there is one; otherwise the one with the most spans
    def checks_of(t):
        root = next(s for s in t.data.spans if s.parent_id is None)
        return root.get_attribute("checks") or []
    shown = next((t for k, t in latest.items() if k in records and any(c != "passed" for c in checks_of(t))), None)
    if shown is None and per_trace:
        shown = latest[max(per_trace, key=lambda p: p["spans"])["exception_id"]]

    lines = [f"# Step 11. Traces of run '{a.tag}'", "",
             f'Model: {manifest["model"]}. Lookups: {manifest.get("tools_via", "direct")}. Read back from MLflow experiment `{EXPERIMENT}`.', "",
             "A trace is one exception from start to finish. A span is one step inside it: the exception as a whole (the root span), "
             "one model call, or one lookup.", "",
             f"- **{len(per_trace)} traces for {n} exceptions**, {sum(spans)} spans in all. A trace holds {statistics.median(spans):.0f} spans at the median and {max(spans)} at most.",
             f"- **{agree} of {n} traces agree with the run's own record** in the number of model calls, the lookups in order, the tokens in and out, and the outcome.",
             f"- **Where the time goes.** Model calls took {model_s:,.0f} of the {all_s:,.0f} seconds, and the {by_type['TOOL']['spans']} lookups {tool_s:.1f} seconds together. "
             f"An exception takes {statistics.median(seconds):.0f} seconds at the median and {max(seconds):.0f} at most.", "",
             "| Kind of span | Spans | Seconds in all | Tokens in | Tokens out |", "|---|---|---|---|---|",
             f'| Exception (root) | {by_type["AGENT"]["spans"]} | {all_s:,.1f} | | |',
             f'| Model call | {by_type["CHAT_MODEL"]["spans"]} | {model_s:,.1f} | {by_type["CHAT_MODEL"]["tokens_in"]:,} | {by_type["CHAT_MODEL"]["tokens_out"]:,} |',
             f'| Lookup | {by_type["TOOL"]["spans"]} | {tool_s:,.2f} | | |']
    for d in disagree:
        lines.append(f"- {d}")
    if shown is not None:
        checks = checks_of(shown)
        lines += ["", "## One trace, step by step", "",
                  "Checks on its conclusions, in order: " + "; ".join(short(c, 140) for c in checks) + "." if checks else "", "",
                  "```"] + tree(shown, SpanAttributeKey.CHAT_USAGE) + ["```"]
    lines += ["", "## What the traces are for", "",
              "- To answer, for any one exception, what the model was sent, what it replied, which lookups ran and what they returned, "
              "and how long each step took.",
              "- To see cost and time by step. Tokens are counted on each model call, so a run's bill can be worked out from its traces.",
              "- They are a record, not a check. Whether a conclusion is right is decided by the code checks and the scoring in step 6."]
    (run_dir / "trace_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_json(run_dir / "trace_report.json", {"tag": a.tag, "exceptions": n, "traces": len(per_trace), "spans": sum(spans),
                                               "agree_with_record": agree, "by_kind": by_type,
                                               "median_spans": statistics.median(spans), "max_spans": max(spans),
                                               "median_seconds": round(statistics.median(seconds), 1), "max_seconds": round(max(seconds), 1),
                                               "disagree": disagree})
    print("\n".join(lines))
    sys.exit(0 if agree == n and len(per_trace) == n else 1)


if __name__ == "__main__":
    main()
