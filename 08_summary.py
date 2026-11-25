"""Step 8. The summary for leadership: key risk indicators, what needs a decision, and a short note.

Code computes every number. The model only writes the short note under the
title, from a handful of facts it is handed. Code then checks three things:
every number in the note is one of those facts, the note is in English, and
no sentence is cut off. If the note fails twice, a note written by code is
used instead, and the summary says so.

    python 08_summary.py              writes results/leadership_summary.md and results/lineage.md
    python 08_summary.py --no-model   call no model: keep the stored note if it still passes its checks,
                                      otherwise use the code-written note
"""
import argparse
import collections
import json
import re

from common import EXCEPTIONS_CSV, LEDGER_CSV, RESULTS, load_rules, money, read_csv, read_json, write_json
from reconciliation import KRI_LABELS, kri_status, kri_text

NOTE_SCHEMA = {
    "type": "object",
    "properties": {"headline": {"type": "string", "maxLength": 100},
                   "where_we_stand": {"type": "string", "maxLength": 220},
                   "decisions_needed": {"type": "string", "maxLength": 220}},
    "required": ["headline", "where_we_stand", "decisions_needed"],
}
SYSTEM = ("You write a short status note for compliance leadership about a payments filing. "
          "Use only the facts you are given. Every number you write must appear in the facts exactly as written. "
          "Write in English, in plain complete sentences. Do not list the facts back. No abbreviations.")
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def numbers_in(text):
    return {n.replace(",", "").rstrip(".") for n in NUMBER.findall(text)}


def collect_facts():
    rules = load_rules()
    base = read_json(RESULTS / "baseline_kris.json")
    draft = read_json(RESULTS / "kris_draft.json")
    after = read_json(RESULTS / "kris_after.json")
    tracker = read_csv(RESULTS / "remediation_tracker.csv")
    exc = {e["exception_id"]: e for e in read_csv(EXCEPTIONS_CSV)}
    ledger = {r["line_id"]: r for r in read_csv(LEDGER_CSV)}

    kri = []
    for k, label in KRI_LABELS.items():
        line = base["lines"][k]
        kri.append({"key": k, "label": label, "baseline": base["kris"][k], "line": line,
                    "draft": draft["kris"][k], "after": after["kris"][k],
                    "draft_status": kri_status(draft["kris"][k], line), "after_status": kri_status(after["kris"][k], line)})
    status = collections.Counter(t["status"] for t in tracker)
    waiting = [t for t in tracker if t["status"] in ("waiting for a person", "not investigated")]
    waiting.sort(key=lambda t: -float(exc[t["exception_id"]]["priority"]))
    # pattern: which loads did the confirmed double loads come from
    loads = collections.Counter(ledger[t["value"]]["loaded_on"] for t in tracker
                                if t["action"] == "REMOVE_LINE" and t["status"].endswith("applied"))
    return {
        "rule_version": rules["version"], "program_year": rules["program_year"],
        "ledger_lines": draft["facts"]["ledger_lines"], "filing_lines_draft": draft["facts"]["filing_lines"],
        "exceptions": len(tracker),
        "settled_by_rule": status.get("applied by rule", 0),
        "agent_proposals_applied": status.get("approved in the replay, applied", 0),
        "waiting_for_a_person": len(waiting),
        "waiting_dollars": round(sum(float(t["dollars"]) for t in waiting), 2),
        "kri": kri,
        "kris_over_line_in_draft": sum(r["draft_status"] == "ESCALATE" for r in kri),
        "kris_over_line_after_fixes": sum(r["after_status"] == "ESCALATE" for r in kri),
        "waiting": [{"exception_id": t["exception_id"], "rule": t["rule"], "lines": t["lines"], "dollars": t["dollars"],
                     "what_found": exc[t["exception_id"]]["what_found"]} for t in waiting],
        "double_loads_confirmed": sum(loads.values()),
        "double_loads_by_load_date": dict(sorted(loads.items())),
    }


def facts_text(f):
    """The few facts the model may use, each already a plain sentence."""
    n = len(f["kri"])
    lines = [f"{f['exceptions']} exceptions were raised.",
             f"{f['settled_by_rule']} were settled by rule.",
             f"{f['agent_proposals_applied']} agent proposals passed the checks and were applied.",
             f"{f['waiting_for_a_person']} exceptions wait for a person, with {money(f['waiting_dollars'])} on their lines.",
             f"{f['kris_over_line_in_draft']} of {n} key risk indicators were over their escalation line in the draft filing.",
             f"{f['kris_over_line_after_fixes']} of {n} key risk indicators are over their escalation line after the fixes."]
    if f["double_loads_confirmed"]:
        lines.append(f"All {f['double_loads_confirmed']} confirmed double loads came from the loads dated "
                     + " and ".join(f["double_loads_by_load_date"]) + ".")
    return "\n".join(lines)


def note_problems(note, allowed):
    """Three checks code can make on the model's note: its numbers, its language, and that no sentence was cut off."""
    text = " ".join(note.values())
    problems = []
    bad = sorted(numbers_in(text) - allowed)
    if bad:
        problems.append("these numbers are not in the facts: " + ", ".join(bad))
    if any(ord(ch) > 0x2FF for ch in text):
        problems.append("the note is not all in English")
    cut = [k for k in ("where_we_stand", "decisions_needed") if not note[k].strip().endswith((".", "!", "?"))]
    if cut:
        problems.append("these parts end mid-sentence: " + ", ".join(cut) + ". Write shorter, complete sentences")
    return problems


def code_note(f):
    return {
        "headline": f"{f['exceptions']} exceptions raised; {f['waiting_for_a_person']} still need a person.",
        "where_we_stand": (f"{f['settled_by_rule']} exceptions were settled by rule and {f['agent_proposals_applied']} agent proposals "
                           f"passed the checks and were applied. {f['kris_over_line_after_fixes']} of {len(f['kri'])} indicators are over their line after the fixes."),
        "decisions_needed": f"{f['waiting_for_a_person']} exceptions wait for a person, with {money(f['waiting_dollars'])} on their lines.",
    }


def write_note(f):
    """Ask the model for the note, check it, give it one more try, then fall back to the code-written note."""
    from agent.llm import get_model
    model = get_model()
    text = facts_text(f)
    allowed = numbers_in(text)
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": "FACTS\n" + text + "\n\nWrite the note as JSON. headline: under 12 words. "
                                            "where_we_stand: one or two sentences on what was raised and what is settled. "
                                            "decisions_needed: one sentence on what waits for a person."}]
    log = []
    for attempt in (1, 2):
        note, usage = model.ask(messages, NOTE_SCHEMA, 300)
        problems = note_problems(note, allowed)
        log.append({"attempt": attempt, "note": note, "problems": problems, "seconds": usage["seconds"]})
        if not problems:
            return note, f"written by {model.name} and passed the checks on try {attempt}", log
        messages += [{"role": "assistant", "content": json.dumps(note)},
                     {"role": "user", "content": "That note failed a check: " + "; ".join(problems) + ". Write it again."}]
    return code_note(f), f"written by code, because the note from {model.name} failed the checks twice (both attempts are in results/summary_facts.json)", log


def write_lineage():
    """One page that ties every output back to its inputs: sources, fingerprints, versions."""
    from common import (EXTRACT_MANIFEST, FILING_CSV, REGISTRY_MANIFEST, SEED, TRUTH_CSV, sha256_of)
    ex, rg = read_json(EXTRACT_MANIFEST), read_json(REGISTRY_MANIFEST)
    rules = load_rules()
    out = ["# Lineage: where every number comes from", "",
           "Each row is one link in the chain. A fingerprint is the SHA-256 of the file; if a file changes, its fingerprint changes.", "",
           "| Step | What | Source or version | Rows | Fingerprint (first 12) |", "|---|---|---|---|---|",
           f"| 1 | Payment extract | {ex['source']}, dataset {ex['dataset_id']}, pulled {ex['retrieved_at_utc']} | {ex['rows']:,} | {ex['sha256'][:12]} |",
           f"| 2 | Registry snapshot | {rg['source']}, pulled {rg['retrieved_at_utc']} | {rg['people']:,} | {rg['sha256'][:12]} |",
           f"| 3 | Ledger with planted errors | 03_build_scenario.py, seed {SEED} | {len(read_csv(LEDGER_CSV)):,} | {sha256_of(LEDGER_CSV)[:12]} |",
           f"| 3 | Draft filing | 03_build_scenario.py, seed {SEED} | {len(read_csv(FILING_CSV)):,} | {sha256_of(FILING_CSV)[:12]} |",
           f"| 3 | Answer key | 03_build_scenario.py, seed {SEED} | {len(read_csv(TRUTH_CSV)):,} | {sha256_of(TRUTH_CSV)[:12]} |",
           f"| 4 | Exception log | 04_reconcile.py, rule file {rules['version']} | {len(read_csv(EXCEPTIONS_CSV)):,} | {sha256_of(EXCEPTIONS_CSV)[:12]} |"]
    for run in sorted((RESULTS / "runs").glob("*/run_manifest.json")):
        m = read_json(run)
        n = sum(1 for l in (run.parent / "conclusions.jsonl").read_text().splitlines() if l.strip())
        out.append(f"| 5 | Agent run '{m['tag']}' | model {m['model']} ({m['model_file_sha256'][:12] or 'endpoint'}), "
                   f"procedure {m['procedure_file']} ({m['procedure_sha256'][:12]}), rule file {m['rule_version']}, started {m['started_utc']} | "
                   f"{n} | {sha256_of(run.parent / 'conclusions.jsonl')[:12]} |")
    out += ["", "The extract and the snapshot each have a manifest beside them with the exact query. "
            "Each agent run folder has a run_manifest.json with the fingerprints of the model file, the procedure and the data it ran on.", ""]
    (RESULTS / "lineage.md").write_text("\n".join(out), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-model", action="store_true")
    a = ap.parse_args()
    write_lineage()
    f = collect_facts()
    if a.no_model:
        # Keep the note a model wrote in the stored run, if it still passes its checks against the facts just computed.
        facts_file = RESULTS / "summary_facts.json"
        stored = read_json(facts_file) if facts_file.exists() else {}
        by_model = stored.get("note") and not stored.get("note_source", "").startswith("written by code")
        if by_model and not note_problems(stored["note"], numbers_in(facts_text(f))):
            note, how, log = stored["note"], stored["note_source"], stored.get("note_log", [])
            print("Kept the stored note: it still passes its checks against the facts just computed.\n")
        else:
            note, how, log = code_note(f), "written by code (no model used)", []
    else:
        note, how, log = write_note(f)
    write_json(RESULTS / "summary_facts.json", {"facts": f, "note": note, "note_source": how, "note_log": log})

    out = [f"# Filing readiness summary, program year {f['program_year']}", "",
           "A replay on public records with planted errors. Not a real filing.", "",
           f"**{note['headline']}**", "", note["where_we_stand"], "", note["decisions_needed"], "",
           "## Key risk indicators", "",
           "| Indicator | Baseline | Escalation line | Draft | After fixes |", "|---|---|---|---|---|"]
    for r in f["kri"]:
        out.append(f"| {r['label']} | {kri_text(r['key'], r['baseline'])} | {r['line']['escalate_when']} {kri_text(r['key'], r['line']['line'])} | "
                   f"{kri_text(r['key'], r['draft'])} ({r['draft_status']}) | {kri_text(r['key'], r['after'])} ({r['after_status']}) |")
    out += ["", "Baseline is the same check on the records as published. Each line is the baseline moved by a margin written in the rule file.", "",
            f"## Decisions needed: {f['waiting_for_a_person']} exceptions wait for a person", "",
            "| Exception | Rule | Lines | Dollars | What was found |", "|---|---|---|---|---|"]
    for w in f["waiting"][:12]:
        out.append(f"| {w['exception_id']} | {w['rule']} | {w['lines']} | {money(w['dollars'])} | {w['what_found']} |")
    if len(f["waiting"]) > 12:
        out.append(f"| | | | | and {len(f['waiting']) - 12} more in results/remediation_tracker.csv |")
    if f["double_loads_confirmed"]:
        out += ["", "## Pattern worth knowing", "",
                f"All {f['double_loads_confirmed']} confirmed double loads came from "
                + " and ".join(f"the load dated {d} ({n})" for d, n in f["double_loads_by_load_date"].items()) + "."]
    out += ["", "---", f"How this page was made: every number in the tables is computed by code. The note under the title was {how}. "
            "Code checks the note's numbers, its language and that no sentence is cut off. It cannot check that a sentence reads the facts correctly, "
            "so the tables are the record.", ""]
    (RESULTS / "leadership_summary.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
