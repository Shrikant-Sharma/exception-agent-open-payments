"""Step 12. The same agent on a hosted model, behind the regression check.

Steps 5 to 9 ran a 4-billion-parameter open model on a laptop CPU. This step
runs the same agent, lookups, procedure and code checks on a model hosted by a
service: Amazon Bedrock, Groq, or any other that speaks the OpenAI chat format.
Only three settings change (the service's address, the model's name, your key).

The order is fixed, and the first stage is a gate:

  1  The regression check. The model runs the 35 development exceptions and must
     meet the stored bar: at least 33 right and no wrong proposal passed by the
     checks. A model that fails here never sees the test.
  2  The frozen test: the 95 unseen exceptions.
  3  The two stress tests on 21 test exceptions: the registry does not answer,
     and a planted instruction sits in the record.

    $env:LLM_BASE_URL = "https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1"     (PowerShell)
    $env:LLM_MODEL    = "openai.gpt-oss-120b-1:0"
    $env:LLM_API_KEY  = "<your key; never put it in a file>"
    python 12_hosted_model.py --name bedrock_gpt_oss_120b --price-in 0.15 --price-out 0.60

Options: --regression-only    stop after stage 1 (to compare models before one of them sees the test)
         --skip-stress        stop after stage 2
         --tools mcp          call the lookups through the MCP server (step 10)
         --trace              write every exception as an MLflow trace (step 11)
         --price-in, --price-out    the service's price in dollars per million tokens, to work out the cost
Output:  results/hosted/<name>.md and <name>.json, and one folder per stage under results/runs/hosted_<name>_*

A run that stops (a daily limit, a lost connection) keeps what it finished. Run the same command
again and it continues. The laptop model has already been scored on these 95 exceptions, so a
hosted model's score is a second use of the same test, and the report says so.
"""
import argparse
import importlib
import json
import os
import statistics
import subprocess
import sys

from common import RESULTS, ROOT, read_json, write_json

RUNS = RESULTS / "runs"
STAGES = [                       # label, stored laptop run to set beside it, arguments of step 5, stress setting for step 6
    ("Development (the regression check)", "dev", ["--split", "dev"], None),
    ("Test (95 unseen exceptions)", "test", ["--split", "test"], None),
    ("Stress: planted instruction", "test_note", ["--split", "test", "--rule", "R-ID-01", "--stress", "note"], "note"),
    ("Stress: registry down", "test_outage", ["--split", "test", "--rule", "R-ID-01", "--stress", "outage"], "outage"),
]


def run_stage(tag, arguments, extra):
    done = subprocess.run([sys.executable, str(ROOT / "05_run_agent.py"), *arguments, "--tag", tag, *extra], cwd=ROOT)
    if done.returncode != 0:
        sys.exit(f"\nThe run '{tag}' stopped before it finished. What it finished is stored. Run the same command again to continue.")


def usage_of(tag):
    recs = [json.loads(line) for line in (RUNS / tag / "conclusions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    return {"tokens_in": sum(r["tokens_in"] for r in recs), "tokens_out": sum(r["tokens_out"] for r in recs),
            "model_calls": sum(r["model_calls"] for r in recs),
            "median_seconds": round(statistics.median(r["seconds"] for r in recs), 1) if recs else 0.0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="a short label for this service and model, for example bedrock_gpt_oss_120b")
    ap.add_argument("--price-in", type=float, default=None)
    ap.add_argument("--price-out", type=float, default=None)
    ap.add_argument("--regression-only", action="store_true")
    ap.add_argument("--skip-stress", action="store_true")
    ap.add_argument("--tools", choices=["direct", "mcp"], default="direct")
    ap.add_argument("--trace", action="store_true")
    a = ap.parse_args()
    if not os.environ.get("LLM_BASE_URL") or not os.environ.get("LLM_MODEL"):
        sys.exit("Set LLM_BASE_URL, LLM_MODEL and LLM_API_KEY first. See the top of this file, or README, 'Step 12'.")
    extra = ["--tools", a.tools] + (["--trace"] if a.trace else [])
    evaluate = importlib.import_module("06_evaluate").evaluate
    priced = a.price_in is not None and a.price_out is not None

    rows, passed = [], None
    for n, (label, laptop_tag, arguments, stress) in enumerate(STAGES):
        tag = f"hosted_{a.name}_{laptop_tag}"
        print(f"\n===== Stage: {label}  ->  results/runs/{tag}", flush=True)
        run_stage(tag, arguments, extra)
        score = evaluate(tag, stress, quiet=True)
        laptop = read_json(RUNS / laptop_tag / "evaluation.json")
        use = usage_of(tag)
        cost = (use["tokens_in"] * a.price_in + use["tokens_out"] * a.price_out) / 1e6 if priced else None
        rows.append({"stage": label, "run": tag, "exceptions": score["exceptions"], "right": score["right"],
                     "to_a_person": score["to_a_person"], "wrong": score["wrong"],
                     "laptop": {k: laptop[k] for k in ("right", "to_a_person", "wrong")}, **use,
                     "cost_dollars": None if cost is None else round(cost, 4)})
        if n == 0:               # the gate
            gate = subprocess.run([sys.executable, str(ROOT / "09_regression.py"), "--tag", tag], cwd=ROOT)
            passed = gate.returncode == 0
            if not passed or a.regression_only:
                break
        if n == 1 and a.skip_stress:
            break

    manifest = read_json(RUNS / rows[0]["run"] / "run_manifest.json")
    bar = read_json(RESULTS / "regression_bar.json")
    total = {k: sum(r[k] for r in rows) for k in ("tokens_in", "tokens_out", "model_calls")}
    total_cost = round(sum(r["cost_dollars"] for r in rows), 4) if priced else None
    lines = [f"# Step 12. The agent on a hosted model: {a.name}", "",
             f'Model `{manifest["model"]}`, run as {manifest["model_runs_as"]}. Lookups: {a.tools}' + (", traced" if a.trace else "") + ". "
             "Same procedure, lookups and code checks as the laptop runs. Temperature 0.", "",
             f'**The regression check: {"PASSED" if passed else "FAILED"}.** The bar is {bar["passes_when"]} on the '
             f'{bar["exceptions"]} development exceptions. This model: {rows[0]["right"]} right, {rows[0]["to_a_person"]} to a person, {rows[0]["wrong"]} wrong.']
    if not passed:
        lines += ["", "The model did not meet the bar, so it was not run on the test. The 95 unseen exceptions were not shown to it."]
    elif a.regression_only:
        lines += ["", "Stopped after the regression check, as asked. The test has not been run for this model."]
    lines += ["", "| Stage | Exceptions | Right | To a person | Wrong | Laptop model: right, to a person, wrong | Tokens in | Tokens out | Median seconds per exception | Cost |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        cost = "not priced" if r["cost_dollars"] is None else f'${r["cost_dollars"]:.2f}'
        lines.append(f'| {r["stage"]} | {r["exceptions"]} | {r["right"]} | {r["to_a_person"]} | {r["wrong"]} | '
                     f'{r["laptop"]["right"]}, {r["laptop"]["to_a_person"]}, {r["laptop"]["wrong"]} | {r["tokens_in"]:,} | {r["tokens_out"]:,} | '
                     f'{r["median_seconds"]} | {cost} |')
    lines += ["", f'In all: {total["model_calls"]:,} model calls, {total["tokens_in"]:,} tokens in and {total["tokens_out"]:,} out'
                  + (f", ${total_cost:.2f} at ${a.price_in} per million tokens in and ${a.price_out} out." if priced else ". No price was given, so no cost is shown."),
              "", "## How to read this", "",
              "- The laptop model was scored on the same 95 exceptions first. A hosted model's score is a second use of that test: "
              "it is a fair comparison of the two models, and it is no longer an unseen test for the project as a whole.",
              "- A proposal is counted wrong only when it passed the checks and does not match the answer key. \"To a person\" means "
              "the agent or the checks handed the exception over, which is the safe outcome.",
              "- In the registry-down test the right outcome for an identity exception is to hand it to a person.",
              "- Seconds are the time the service took to answer, summed over an exception's model calls. They include the service's "
              "queue and any waiting on a rate limit inside one request."]
    out = RESULTS / "hosted"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{a.name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_json(out / f"{a.name}.json", {"name": a.name, "model": manifest["model"], "model_runs_as": manifest["model_runs_as"],
                                        "tools_via": a.tools, "traced": a.trace, "regression_passed": passed,
                                        "price_in": a.price_in, "price_out": a.price_out, "stages": rows, "total": total,
                                        "total_cost_dollars": total_cost})
    print("\n" + "\n".join(lines))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
