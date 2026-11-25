"""Step 6. Score an agent run against the answer key.

This is the only step that reads data/scenario/truth.csv together with the
agent's conclusions.

Every exception ends in one of three places:
  right         the proposal matches the answer key (same action, same value),
                or the case had no safe answer and went to a person
  to a person   the agent could not confirm, or its conclusion failed the checks
  wrong         a proposal passed the checks and does not match the answer key

    python 06_evaluate.py --tag test
    python 06_evaluate.py --tag test_outage --stress outage

Writes results/runs/<tag>/report.md, evaluation.json, cases.csv and outcomes.png
"""
import argparse
import collections
import json
import math
import statistics

from agent.checks import ACTION
from common import RESULTS, TRUTH_CSV, read_csv, read_json, write_csv, write_json

KIND_LABEL = collections.OrderedDict([
    ("NPI_KEYED_WRONG", "NPI typed wrong (planted)"),
    ("WRONG_PERSON_SELECTED", "Wrong person selected (planted)"),
    ("NOT_CONFIRMABLE", "No safe correction exists (planted)"),
    ("NAME_DIFFERENCE_AS_PUBLISHED", "Name differs from registry (as published)"),
    ("NOT_IN_REGISTRY_AS_PUBLISHED", "NPI not in registry (as published)"),
    ("DOCUMENT_LOADED_TWICE", "Document loaded twice (planted)"),
    ("LOOKALIKE_AS_PUBLISHED", "Look-alike payments (as published)"),
])
OUTCOMES = ["right", "to a person", "wrong"]


def wilson(k, n, z=1.96):
    """95% interval for a share k of n."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, mid - half), min(1.0, mid + half))


def matches(action, value, t):
    """Does (action, value) equal the answer key?"""
    if action != t["expected_action"]:
        return False
    return action in ("NO_CHANGE", "SEND_TO_PERSON") or value == t["expected_value"]


def load(tag, stress=None):
    truth = {t["key"]: dict(t) for t in read_csv(TRUTH_CSV) if t["key"]}
    recs = [json.loads(l) for l in (RESULTS / "runs" / tag / "conclusions.jsonl").read_text().splitlines() if l.strip()]
    rows = []
    for r in recs:
        t = dict(truth[r["key"]])
        if stress == "outage" and r["check"] == "IDENTITY":
            # with the registry down there is no evidence, so the only safe answer is a person
            t.update(expected_action="SEND_TO_PERSON", expected_value="", expected_root_cause="CANNOT_CONFIRM")
        first = r["first_conclusion"]
        first_action = ACTION[first["root_cause"]]
        first_value = first["fix_value"].strip().upper() if first_action in ("FIX_NPI", "REMOVE_LINE") else ""
        if r["status"] == "to a person":
            outcome = "right" if t["expected_action"] == "SEND_TO_PERSON" else "to a person"
        else:
            outcome = "right" if matches(r["action"], r["fix_value"], t) else "wrong"
        # Every conclusion the agent reached on any try: did it propose a change the answer key does not have, and was it stopped?
        stopped = got_through = 0
        for step in r["trace"]:
            if step["lookup"] != "CONCLUSION":
                continue
            c = json.loads(step["result"])
            c_action = ACTION[c["root_cause"]]
            c_value = (c.get("fix_value") or "").strip().upper() if c_action in ("FIX_NPI", "REMOVE_LINE") else ""
            if c_action != "SEND_TO_PERSON" and not matches(c_action, c_value, t):
                if step["check"] == "passed":
                    got_through += 1
                else:
                    stopped += 1
        if r["last_problems"]:
            ended = f'failed the checks on all {r["n_conclusions"]} tries'
        elif r["status"] == "to a person" and r["n_conclusions"] == 1:
            ended = "the agent said it could not confirm, on its first conclusion"
        elif r["status"] == "to a person":
            back = r["n_conclusions"] - 1
            ended = f'the agent said it could not confirm, after {back} conclusion{"s were" if back > 1 else " was"} sent back'
        else:
            ended = "proposal passed the checks"
        rows.append({
            "exception_id": r["exception_id"], "kind": t["kind"], "check": r["check"],
            "expected": t["expected_action"] + (" " + t["expected_value"] if t["expected_value"] else ""),
            "got": r["action"] + (" " + r["fix_value"] if r["fix_value"] else ""),
            "status": r["status"], "outcome": outcome,
            "first_conclusion_right": matches(first_action, first_value, t),
            "first_conclusion_failed_checks": bool(r["first_problems"]),
            "first_conclusion_hand_off": first_action == "SEND_TO_PERSON",
            "last_conclusion_failed_checks": bool(r["last_problems"]), "how_it_ended": ended,
            "wrong_proposals_stopped": stopped, "wrong_proposals_passed": got_through,
            "conclusions": r["n_conclusions"], "lookups": " > ".join(r["lookups"]), "n_lookups": len(r["lookups"]),
            "seconds": r["seconds"], "tokens_in": r["tokens_in"], "tokens_out": r["tokens_out"],
            "root_cause_right": r["status"] == "proposed" and r["root_cause"] == t["expected_root_cause"],
            "problems": " | ".join(r["first_problems"]), "explanation": r["explanation"],
        })
    return rows


def summarize(rows):
    n = len(rows)
    count = collections.Counter(r["outcome"] for r in rows)
    lo, hi = wilson(count["right"], n)
    sent_back = [r for r in rows if r["first_conclusion_failed_checks"]]
    # a wrong proposal: the first conclusion proposes a change or a close that does not match the answer key
    wrong_proposal = [r for r in rows if not r["first_conclusion_right"] and not r["first_conclusion_hand_off"]]
    to_person = [r for r in rows if r["outcome"] == "to a person"]      # sent to a person although the answer key has an answer
    by_kind = collections.OrderedDict()
    for kind in KIND_LABEL:
        sub = [r for r in rows if r["kind"] == kind]
        if sub:
            c = collections.Counter(r["outcome"] for r in sub)
            by_kind[kind] = {"n": len(sub), **{o: c[o] for o in OUTCOMES}}
    return {
        "exceptions": n, **{o.replace(" ", "_"): count[o] for o in OUTCOMES},
        "right_pct": round(100 * count["right"] / n, 1), "right_pct_95_low": round(100 * lo, 1), "right_pct_95_high": round(100 * hi, 1),
        "by_kind": by_kind,
        "first_conclusion_right_and_passed": sum(r["first_conclusion_right"] and not r["first_conclusion_failed_checks"] for r in rows),
        "first_conclusion_right_by_action_and_value": sum(r["first_conclusion_right"] for r in rows),
        "sent_back_by_checks": len(sent_back),
        "sent_back_wrong_proposal": sum(r in wrong_proposal for r in sent_back),
        "sent_back_wrong_fact_or_case": sum(r not in wrong_proposal for r in sent_back),
        "sent_back_hand_offs_resting_on_a_wrong_fact": sum(r["first_conclusion_hand_off"] for r in sent_back),
        "sent_back_then_right": sum(r["outcome"] == "right" for r in sent_back),
        "sent_back_then_to_a_person": sum(r["outcome"] == "to a person" for r in sent_back),
        "sent_back_then_wrong": sum(r["outcome"] == "wrong" for r in sent_back),
        "wrong_proposals_that_passed_checks": sum(not r["first_conclusion_failed_checks"] for r in wrong_proposal),
        "wrong_proposals_stopped_on_any_try": sum(r["wrong_proposals_stopped"] for r in rows),
        "wrong_proposals_passed_on_any_try": sum(r["wrong_proposals_passed"] for r in rows),
        "to_a_person_hand_off_on_first_conclusion": sum(not r["last_conclusion_failed_checks"] and r["conclusions"] == 1 for r in to_person),
        "to_a_person_hand_off_after_being_sent_back": sum(not r["last_conclusion_failed_checks"] and r["conclusions"] > 1 for r in to_person),
        "to_a_person_after_failing_every_try": sum(r["last_conclusion_failed_checks"] for r in to_person),
        "explanations_quoting_something_not_in_evidence": sum("the explanation quotes" in r["problems"] for r in rows),
        "lookups_per_exception": dict(sorted(collections.Counter(r["n_lookups"] for r in rows).items())),
        "lookup_paths": {chk: dict(collections.Counter(r["lookups"] for r in rows if r["check"] == chk).most_common())
                         for chk in ("IDENTITY", "LOOKALIKE")},
        "seconds_median": round(statistics.median(r["seconds"] for r in rows), 1),
        "seconds_total": round(sum(r["seconds"] for r in rows)),
        "tokens_in": sum(r["tokens_in"] for r in rows), "tokens_out": sum(r["tokens_out"] for r in rows),
    }


def chart(summary, title, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    surface, ink, ink2 = "#fcfcfb", "#0b0b0b", "#52514e"
    # Blue, yellow, red: checked with a palette validator so any two stay apart for color-blind readers.
    # Every segment also carries its count, so color is never the only signal.
    color = {"right": "#2a78d6", "to a person": "#eda100", "wrong": "#e34948"}
    kinds = list(summary["by_kind"])
    fig, ax = plt.subplots(figsize=(9.2, 0.62 * len(kinds) + 1.7), dpi=200)
    fig.patch.set_facecolor(surface); ax.set_facecolor(surface)
    longest = max(v["n"] for v in summary["by_kind"].values())
    for y, kind in enumerate(kinds):
        v, left = summary["by_kind"][kind], 0
        for o in OUTCOMES:
            if v[o]:
                ax.barh(y, v[o], left=left, height=0.42, color=color[o], edgecolor=surface, linewidth=2)
                if v[o] >= 0.05 * longest:
                    ax.text(left + v[o] / 2, y, str(v[o]), ha="center", va="center", fontsize=9,
                            color="#ffffff" if o != "to a person" else ink)
                left += v[o]
        ax.text(left + longest * 0.012, y, f'{v["right"]} of {v["n"]} right', va="center", fontsize=9, color=ink2)
    ax.set_yticks(range(len(kinds)), [KIND_LABEL[k] for k in kinds], fontsize=9.5, color=ink)
    ax.invert_yaxis()
    ax.set_xlim(0, longest * 1.2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    handles = [plt.Rectangle((0, 0), 1, 1, color=color[o]) for o in OUTCOMES]
    ax.legend(handles, ["Right", "Sent to a person", "Wrong"], loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3,
              frameon=False, fontsize=9.5, handlelength=1.2, columnspacing=1.6, labelcolor=ink)
    fig.suptitle(title, x=0.012, ha="left", fontsize=12, color=ink, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, facecolor=surface)
    plt.close(fig)


def report(tag, rows, s, manifest, stress):
    m = manifest
    lines = [f"# Agent run '{tag}': scored against the answer key", "",
             "A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. "
             "Nobody named in this run made a mistake.", "",
             f"Model: {m['model']} ({m['model_runs_as']}). Procedure: {m['procedure_file']}. Rule file {m['rule_version']}. "
             f"Temperature 0." + (f" Stress test: {stress}." if stress else ""), "",
             f"**{s['right']} of {s['exceptions']} right ({s['right_pct']}%; 95% interval {s['right_pct_95_low']} to {s['right_pct_95_high']}). "
             f"{s['to_a_person']} sent to a person. {s['wrong']} wrong.**", "",
             "| Kind of exception | Exceptions | Right | Sent to a person | Wrong |", "|---|---|---|---|---|"]
    for kind, v in s["by_kind"].items():
        lines.append(f"| {KIND_LABEL[kind]} | {v['n']} | {v['right']} | {v['to a person']} | {v['wrong']} |")
    lines.append(f"| **All** | **{s['exceptions']}** | **{s['right']}** | **{s['to_a_person']}** | **{s['wrong']}** |")
    lines += ["", "## What the checks did", "",
              f"- The agent's first conclusion passed the checks and matched the answer key in {s['first_conclusion_right_and_passed']} of {s['exceptions']} exceptions.",
              f"- The checks sent {s['sent_back_by_checks']} first conclusions back. {s['sent_back_wrong_proposal']} proposed a fix or a close that did not match the answer key. "
              f"The other {s['sent_back_wrong_fact_or_case']} stated a fact or the case of the procedure wrong; "
              f"{s['sent_back_hand_offs_resting_on_a_wrong_fact']} of those were hand-offs resting on a wrong fact.",
              f"- After the reason was given back, {s['sent_back_then_right']} of the {s['sent_back_by_checks']} ended right, "
              f"{s['sent_back_then_to_a_person']} went to a person and {s['sent_back_then_wrong']} ended wrong.",
              f"- Over every try, conclusions that proposed a change the answer key does not have: "
              f"{s['wrong_proposals_stopped_on_any_try']} stopped by the checks, {s['wrong_proposals_passed_on_any_try']} passed.",
              f"- Sent to a person although an answer existed: {s['to_a_person']}. By a hand-off on the first conclusion: {s['to_a_person_hand_off_on_first_conclusion']}. "
              f"By a hand-off after an earlier conclusion was sent back: {s['to_a_person_hand_off_after_being_sent_back']}. "
              f"After failing the checks on every try: {s['to_a_person_after_failing_every_try']}. A hand-off passes the checks when the facts it states are true.",
              f"- Explanations that quoted an NPI, line or document not in the evidence: {s['explanations_quoting_something_not_in_evidence']}.",
              "", "## How the agent worked", "",
              "- Lookups per exception: " + ", ".join(f"{k} lookup{'s' if k != 1 else ''} in {v}" for k, v in s["lookups_per_exception"].items()) + ".",
              f"- Median {s['seconds_median']} seconds per exception; {round(s['seconds_total'] / 60)} minutes of model time in all; "
              f"{s['tokens_in']:,} tokens read, {s['tokens_out']:,} written."]
    for chk, label in (("IDENTITY", "Recipient exceptions"), ("LOOKALIKE", "Look-alike exceptions")):
        if s["lookup_paths"][chk]:
            lines.append(f"- {label}, lookup paths used: " + "; ".join(f"{p or 'none'} ({n})" for p, n in s["lookup_paths"][chk].items()) + ".")
    bad = [r for r in rows if r["outcome"] != "right"]
    if bad:
        lines += ["", "## Every exception that did not end right", "",
                  "| Exception | Kind | Answer key | Result | How it ended | First problem the checks found |", "|---|---|---|---|---|---|"]
        for r in bad:
            lines.append(f"| {r['exception_id']} | {KIND_LABEL[r['kind']]} | {r['expected']} | {r['outcome']}: {r['got']} | {r['how_it_ended']} | {r['problems'] or 'none'} |")
    return "\n".join(lines) + "\n"


def evaluate(tag, stress=None, quiet=False):
    rows = load(tag, stress)
    s = summarize(rows)
    out = RESULTS / "runs" / tag
    manifest = read_json(out / "run_manifest.json")
    write_json(out / "evaluation.json", {"tag": tag, "stress": stress or "none", "model": manifest["model"], **s})
    write_csv(out / "cases.csv", rows)
    text = report(tag, rows, s, manifest, stress)
    (out / "report.md").write_text(text, encoding="utf-8")
    chart(s, f"{s['right']} of {s['exceptions']} right, {s['to_a_person']} sent to a person, {s['wrong']} wrong   (run '{tag}', {manifest['model']})",
          out / "outcomes.png")
    if not quiet:
        print(text)
    return s


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="test")
    ap.add_argument("--stress", choices=["outage", "note"])
    a = ap.parse_args()
    evaluate(a.tag, a.stress)
