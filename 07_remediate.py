"""Step 7. Remediation: track every exception to a close, apply the fixes, and prove what changed.

Three routes end here:
  settled by rule       code applies the fix the ledger supports
  proposed by the agent a person would approve these; in this replay every proposal that
                        passed the checks is treated as approved, to see what an
                        unattended run would have done
  sent to a person      left open and listed

Then the control is tested end to end: the reconciliation is run again on the
corrected ledger and filing, and the corrected filing is compared, line by
line, with the records as CMS published them. That last comparison is the
only use of the published records here.

    python 07_remediate.py                 uses the agent runs 'dev' and 'test'
    python 07_remediate.py --tags test     only the test run

Writes results/remediation_tracker.csv, accepted_register.csv, findings.md,
filing_corrected.csv, kris_after.json and remediation_report.md
"""
import argparse
import collections
import json

from common import (EXCEPTIONS_CSV, FILING_CSV, LEDGER_CSV, RESULTS, SCENARIO_DIR, load_rules, money, read_csv,
                    write_csv, write_json)
from reconciliation import reconcile
from registry import Registry

CAUSE_TEXT = {
    "NPI_KEYED_WRONG": "NPI typed wrong", "WRONG_PERSON_SELECTED": "Wrong person selected",
    "SAME_PERSON_OTHER_NAME": "Same person under another name", "DOCUMENT_LOADED_TWICE": "Document loaded twice",
    "SEPARATE_PAYMENTS": "Separate payments", "CANNOT_CONFIRM": "Could not be confirmed",
}
IMPACT = {
    "NPI_KEYED_WRONG": "Filed as is, the payment would be reported against an NPI that does not exist.",
    "WRONG_PERSON_SELECTED": "Filed as is, the payment would be reported against another person.",
    "SAME_PERSON_OTHER_NAME": "The NPI is right. The name on file differs from the registry and may be questioned at submission.",
    "DOCUMENT_LOADED_TWICE": "Filed as is, the same payment would be reported twice.",
    "SEPARATE_PAYMENTS": "None. The lines are separate payments.",
    "CANNOT_CONFIRM": "Unknown until a person reviews it. The lines stay open.",
}


TO_CONFIRM = {
    "NPI_KEYED_WRONG": "That the person the registry lists under the corrected NPI is the person who was paid.",
    "WRONG_PERSON_SELECTED": "That the person the registry lists under the corrected NPI is the person who was paid.",
    "SAME_PERSON_OTHER_NAME": "Whether the name on file should be updated to the registry name before submission.",
    "DOCUMENT_LOADED_TWICE": "That the document was paid once, before the second line is removed.",
    "SEPARATE_PAYMENTS": "Nothing further.",
    "CANNOT_CONFIRM": "Who was paid, from the source document.",
}


def compare_with_published(filing, ledger_by_id, published):
    """Line by line against the records as published. A line agrees when NPI, amount and date all match."""
    lines_for = collections.defaultdict(list)
    for f in filing:
        lines_for[ledger_by_id[f["line_id"]]["record_id"]].append(f)
    agree = missing = differ = extra = 0
    for p in published:
        got = lines_for.get(p["record_id"], [])
        if not got:
            missing += 1
            continue
        extra += len(got) - 1
        f = got[0]
        if (f["npi"], f["amount"], f["pay_date"]) == (p["npi"], p["amount"], p["pay_date"]):
            agree += 1
        else:
            differ += 1
    return {"agree": agree, "missing": missing, "differ": differ, "extra_lines": extra, "published_records": len(published)}


def finding(exc, c, rules):
    """A facts-first write-up. Code fills in every fact; the model's own words appear only as a quoted explanation."""
    rule = rules["rules"][exc["rule_id"]]
    cause = c["root_cause"]
    if c["action"] == "FIX_NPI":
        rec = f'Change the NPI on {exc["lines"].replace("+", ", ")} to {c["fix_value"]}.'
    elif c["action"] == "REMOVE_LINE":
        rec = f'Remove line {c["fix_value"]}.'
    elif c["action"] == "NO_CHANGE":
        rec = "No change. Record the reason in the accepted register so the exception does not come back."
    else:
        rec = "Send to a person."
    status = "Proposed, waiting for approval." if c["status"] == "proposed" else f'Sent to a person: {c["reason"]}.'
    out = [f'### {exc["exception_id"]}: {CAUSE_TEXT[cause]}. {status}', "",
           f'- **Condition.** {exc["what_found"]}',
           f'- **Criteria.** {exc["rule_id"]}, rule file {exc["rule_version"]}: {rule["text"]} ({rule["citation"]})',
           f'- **Cause.** {CAUSE_TEXT[cause]}. Agent\'s explanation: "{c["explanation"].strip()}"',
           f'- **Impact.** {exc["n_lines"]} line(s), {money(exc["dollars"])}. {IMPACT[cause]}',
           "- **Evidence.**"]
    out += [f'    - {e["id"]}, {e["lookup"]}({e["input"]}): ' + e["text"].replace("\n", " / ")
            for e in c["evidence"] if e["id"] in c["evidence_cited"] or not c["evidence_cited"]]
    out.append(f"- **Recommendation.** {rec}")
    out.append(f"- **To confirm.** {TO_CONFIRM[cause]}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", default="dev,test")
    a = ap.parse_args()

    reg, rules = Registry(), load_rules()
    exceptions = read_csv(EXCEPTIONS_CSV)
    ledger, filing = read_csv(LEDGER_CSV), read_csv(FILING_CSV)
    published = read_csv(SCENARIO_DIR / "ledger_clean.csv")
    conclusions = {}
    for tag in a.tags.split(","):
        path = RESULTS / "runs" / tag / "conclusions.jsonl"
        if path.exists():
            for l in path.read_text().splitlines():
                if l.strip():
                    c = json.loads(l)
                    conclusions[c["exception_id"]] = dict(c, run=tag)

    by_id = {r["line_id"]: r for r in ledger}
    stage = {"draft": compare_with_published(filing, by_id, published)}

    # ---- 1. fixes the ledger settles (route: rule)
    filed = {f["line_id"]: f for f in filing}
    tracker = []
    for e in exceptions:
        if e["route"] != "rule":
            continue
        if e["rule_fix"] == "ADD_LINES":
            for i in e["lines"].split("+"):
                filed[i] = {k: by_id[i][k] for k in filing[0] if k != "filing_id"}
                filed[i]["filing_id"] = "added"
        else:                                           # SET_FROM_LEDGER:amount=...,pay_date=...
            for pair in e["rule_fix"].split(":", 1)[1].split(","):
                k, v = pair.split("=")
                filed[e["key"]][k] = v
        tracker.append({"exception_id": e["exception_id"], "check": e["check"], "rule": e["rule_id"], "route": "rule",
                        "root_cause": "", "action": e["rule_fix"].split(":")[0], "value": "", "status": "applied by rule",
                        "lines": e["n_lines"], "dollars": e["dollars"]})
    filing = sorted(filed.values(), key=lambda f: f["line_id"])
    stage["after rule fixes"] = compare_with_published(filing, by_id, published)

    # ---- 2. proposals from the agent that passed the checks (treated as approved in this replay)
    accepted, findings = [], []
    removed = set()
    for e in exceptions:
        if e["route"] != "agent":
            continue
        c = conclusions.get(e["exception_id"])
        row = {"exception_id": e["exception_id"], "check": e["check"], "rule": e["rule_id"], "route": "agent",
               "lines": e["n_lines"], "dollars": e["dollars"]}
        if c is None:
            tracker.append(dict(row, root_cause="", action="", value="", status="not investigated"))
            continue
        findings.append(finding(e, c, rules))
        row.update(root_cause=c["root_cause"], action=c["action"], value=c["fix_value"])
        if c["status"] != "proposed":
            tracker.append(dict(row, status="waiting for a person"))
            continue
        if c["action"] == "FIX_NPI":
            for i in e["lines"].split("+"):
                by_id[i]["npi"] = c["fix_value"]
                if i in filed:
                    filed[i]["npi"] = c["fix_value"]
        elif c["action"] == "REMOVE_LINE":
            removed.add(c["fix_value"])
        elif c["action"] == "NO_CHANGE":
            accepted.append({"key": e["key"], "rule": e["rule_id"], "reason": c["root_cause"], "exception_id": e["exception_id"],
                             "evidence": " / ".join(x["text"].replace("\n", " ") for x in c["evidence"] if x["id"] in c["evidence_cited"])[:400]})
        tracker.append(dict(row, status="approved in the replay, applied"))
    ledger = [r for r in ledger if r["line_id"] not in removed]
    filing = [f for f in filing if f["line_id"] not in removed]
    stage["after agent proposals"] = compare_with_published(filing, {r["line_id"]: r for r in read_csv(LEDGER_CSV)}, published)

    # ---- 3. run the reconciliation again on the corrected books
    again, facts = reconcile(ledger, filing, reg, rules)
    accepted_keys = {x["key"] for x in accepted}
    still_open = [x for x in again if x["key"] not in accepted_keys]
    open_keys = {x["key"] for x in still_open}
    key_of = {e["exception_id"]: e["key"] for e in exceptions}
    for t in tracker:
        if t["status"].endswith("applied") or t["status"] == "applied by rule":
            t["verified"] = "closed on re-run" if key_of[t["exception_id"]] not in open_keys else "STILL OPEN on re-run"
        else:
            t["verified"] = ""
    waiting = {key_of[t["exception_id"]] for t in tracker if t["status"] in ("waiting for a person", "not investigated")}
    new_open = [x for x in still_open if x["key"] not in waiting]

    for n, f in enumerate(filing, 1):
        f["filing_id"] = f"F{n:05d}"
    write_csv(RESULTS / "filing_corrected.csv", filing, list(read_csv(FILING_CSV)[0].keys()))
    write_csv(RESULTS / "remediation_tracker.csv", tracker,
              ["exception_id", "check", "rule", "route", "root_cause", "action", "value", "status", "verified", "lines", "dollars"])
    write_csv(RESULTS / "accepted_register.csv", accepted or [{"key": "", "rule": "", "reason": "", "exception_id": "", "evidence": ""}],
              ["key", "rule", "reason", "exception_id", "evidence"])
    (RESULTS / "findings.md").write_text(
        "# Findings: one write-up per exception the agent investigated\n\n"
        "A replay on public records. Every error below was planted by 03_build_scenario.py, or is a name difference already in the public records. "
        "Nobody named on this page made a mistake.\n\n"
        "Each fact below is filled in by code from the exception log, the rule file and the lookup results. "
        "The model's own words appear only inside quotation marks.\n\n" + "\n".join(findings), encoding="utf-8")
    # After the fixes, an exception closed with a recorded reason is no longer open.
    after = dict(facts["kris"])
    line_of = {r["line_id"]: r for r in ledger}
    after["open_exception_dollars"] = round(sum(float(line_of[i]["amount"]) for i in {i for x in still_open for i in x["lines"].split("+")}), 2)
    write_json(RESULTS / "kris_after.json", {"rule_version": rules["version"], "kris": after,
                                             "exceptions_on_rerun": len(again), "accepted": len(accepted_keys & {x["key"] for x in again}),
                                             "still_open": len(still_open), "stages": stage})

    status = collections.Counter(t["status"] for t in tracker)
    verified = collections.Counter(t["verified"] for t in tracker if t["verified"])
    rep = ["# Remediation report", "",
           "A replay on public records with planted errors. Not a real filing.", "",
           f"Agent runs used: {a.tags}. Every agent proposal that passed the checks is treated as approved, to show what an unattended run would do. "
           "In real use a person approves each one.", "",
           "## Where the exceptions ended", "",
           "| Status | Exceptions |", "|---|---|"]
    rep += [f"| {k} | {v} |" for k, v in status.most_common()]
    rep += ["", f"Re-run of the reconciliation on the corrected books: {verified.get('closed on re-run', 0)} applied fixes closed, "
            f"{verified.get('STILL OPEN on re-run', 0)} still open, {len(new_open)} new exceptions created by a fix.", "",
            "## The filing against the records as published", "",
            f"A line agrees when its NPI, amount and date match the published record. {len(published):,} published records.", "",
            "| Stage | Lines that agree | Missing | Differ | Extra lines |", "|---|---|---|---|---|"]
    for name, s in stage.items():
        rep.append(f"| {name.capitalize()} | {s['agree']:,} | {s['missing']} | {s['differ']} | {s['extra_lines']} |")
    rep += [""]
    (RESULTS / "remediation_report.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
