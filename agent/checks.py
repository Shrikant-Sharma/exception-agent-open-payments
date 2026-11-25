"""Code checks on every conclusion the agent reaches. No model in here.

The agent proposes; these checks decide whether the proposal may go forward.
They test facts that code can verify from the lookups the agent actually ran:
that a proposed NPI really came back from the registry and carries the name on
the line, that a line marked as a double load really shares its document, that
the procedure's lookups were run before the conclusion, and that every number
quoted in the explanation appears in the evidence.

What they cannot test is judgment: whether a registry record under another
last name is the same person. That part is measured against the answer key
in 06_evaluate.py.
"""
import os
import re

from common import digits_different, first_names_agree, name_agrees_with_registry

ALLOWED = {
    "IDENTITY": ["NPI_KEYED_WRONG", "WRONG_PERSON_SELECTED", "SAME_PERSON_OTHER_NAME", "CANNOT_CONFIRM"],
    "LOOKALIKE": ["DOCUMENT_LOADED_TWICE", "SEPARATE_PAYMENTS", "CANNOT_CONFIRM"],
}
ACTION = {
    "NPI_KEYED_WRONG": "FIX_NPI", "WRONG_PERSON_SELECTED": "FIX_NPI", "SAME_PERSON_OTHER_NAME": "NO_CHANGE",
    "DOCUMENT_LOADED_TWICE": "REMOVE_LINE", "SEPARATE_PAYMENTS": "NO_CHANGE", "CANNOT_CONFIRM": "SEND_TO_PERSON",
}
# When a conclusion breaks the procedure, the agent is given the rule it broke, in the procedure's words. Never the answer.
CASE_B_RULE = ("the procedure, case B: the same first name, and the same city or a type that fits, means SAME_PERSON_OTHER_NAME; "
               "anything else means CANNOT_CONFIRM. Your yes and no answers and your cause do not agree")
CAUSE_RULE = ("the procedure, case A: the cause is NPI_KEYED_WRONG when the NPI on the line has no registry record, "
              "and WRONG_PERSON_SELECTED when it has one. Your cause does not agree with the registry")
# An optional, stricter rule for hand-offs, added on November 25, 2026. Off unless AGENT_STRICT_HANDOFF=1.
# Every stored result was made with it off.
STRICT_HANDOFF = os.environ.get("AGENT_STRICT_HANDOFF") == "1"
QUOTED = re.compile(r"\b\d{10}\b|\bL\d{5}\b|\b(?:EXP|AP)-25-\d{6}\b")


def check(case, conclusion, evidence, reg):
    """Returns a list of problems. Empty list: the proposal may go forward."""
    problems = []
    cause = conclusion.get("root_cause", "")
    value = (conclusion.get("fix_value") or "").strip()
    if cause not in ALLOWED[case["check"]]:
        return [f"{cause} is not a possible cause for this kind of exception"]

    ids = {e["id"] for e in evidence}
    cited = conclusion.get("evidence", [])
    if any(c not in ids for c in cited):
        problems.append("cites evidence that does not exist")
    if cause != "CANNOT_CONFIRM" and not cited:
        problems.append("cites no evidence")

    said = conclusion.get("explanation", "")
    seen_text = case["text"] + " " + " ".join(e["text"] for e in evidence)
    for token in dict.fromkeys(QUOTED.findall(said)):
        if token not in seen_text:
            problems.append(f"the explanation quotes {token}, which is not in the exception or any lookup result")
    if any(ord(ch) > 0x2FF for ch in said):
        problems.append("the explanation is not written in English")

    ok = [e for e in evidence if not e["facts"].get("failed")]
    npis_returned = {n for e in ok for n in e["facts"].get("npis", [])}
    line_npi_looked_up = [e for e in ok if e["lookup"] == "registry_lookup" and e["facts"].get("looked_up") == case["npi"]]
    searched = [e for e in ok if e["lookup"] == "registry_search"]
    documents, loaded = {}, {}
    for e in ok:
        documents.update(e["facts"].get("documents", {}))
        loaded.update(e["facts"].get("loaded", {}))
    line_ids = [l["line_id"] for l in case["lines"]]

    # Which case of the procedure the search result is. A fact, so code can check the agent's claim.
    if case["check"] == "IDENTITY" and searched:
        found = searched[-1]["facts"]
        others = [n for n in found.get("npis", []) if n != case["npi"]]
        actual = "B" if not others else ("A" if found.get("total", 0) == 1 else "C")
        on_file = reg.lookup(case["npi"])
        if conclusion.get("case") and conclusion["case"] != actual:
            problems.append(f'the search result is case {actual} of the procedure, not case {conclusion["case"]}')
        elif conclusion.get("line_npi_in_registry") not in (None, "yes" if on_file is not None else "no"):
            problems.append("line_npi_in_registry is " + ("yes: the registry has a record for the NPI on the line" if on_file is not None
                                                          else "no: the registry has no record of the NPI on the line"))
        elif actual == "B" and conclusion.get("case") == "B" and on_file is not None and "same_first_name" in conclusion:
            # In case B the agent answers three yes/no questions. Two are facts and code checks them.
            # The third, whether the practitioner type fits, is the agent's judgment.
            line = case["lines"][0]
            first = "yes" if first_names_agree(case["first"], on_file["first"]) else "no"
            city = "yes" if line["city"] == on_file["city"] else "no"
            if conclusion.get("same_first_name") != first:
                problems.append(f'same_first_name is {first}: the line says {case["first"]}, the registry says {on_file["first"]}')
            if conclusion.get("same_city") != city:
                problems.append(f'same_city is {city}: the line says {line["city"]}, the registry says {on_file["city"]}')
            same_person = first == "yes" and (city == "yes" or conclusion.get("type_fits") == "yes")
            if not problems and cause == "SAME_PERSON_OTHER_NAME" and not same_person:
                problems.append(CASE_B_RULE)
            if not problems and cause == "CANNOT_CONFIRM" and same_person:
                problems.append(CASE_B_RULE)
        elif actual in ("A", "C") and conclusion.get("case") == actual:
            # Case C: more than one person carries the name. The procedure says how to pick, and code checks the pick.
            if actual == "C":
                close = [n for n in others if digits_different(n, case["npi"]) <= 2]
                history = {}
                for e in ok:
                    history.update(e["facts"].get("history", {}))
                picked = re.sub(r"\D", "", value)
                if len(close) == 1:
                    if cause != "CANNOT_CONFIRM" and picked != close[0]:
                        problems.append("the procedure, case C: the fix is the person whose NPI differs from the NPI on the line in 1 or 2 digits")
                elif not any(e["lookup"] == "ledger_history" for e in ok):
                    problems.append("case C and nobody's NPI is within 2 digits: run ledger_history with the name on the line before you conclude")
                elif cause != "CANNOT_CONFIRM":
                    top = max(history, key=history.get) if history else ""
                    if top not in others:
                        problems.append("the ledger history does not point to one of the people found, so this is CANNOT_CONFIRM")
                    elif picked != top:
                        problems.append("the procedure, case C: when nobody is that close, the fix is the NPI that most ledger lines under that name carry")

    if cause in ("NPI_KEYED_WRONG", "WRONG_PERSON_SELECTED"):
        npi = re.sub(r"\D", "", value)
        on_file = reg.lookup(case["npi"])
        if not line_npi_looked_up:
            problems.append("the NPI on the line was not looked up in the registry (run registry_lookup with it)")
        if len(npi) != 10 or npi == case["npi"]:
            problems.append("the fix is not a different ten-digit NPI")
        elif npi not in npis_returned:
            problems.append(f"NPI {npi} did not come back from any registry lookup in this case")
        else:
            p = reg.lookup(npi)
            if p["status"] != "active":
                problems.append(f"the registry record for NPI {npi} is not active")
            if not name_agrees_with_registry(case["first"], case["last"], p):
                problems.append(f"the registry name for NPI {npi} does not agree with the name on the line")
        if cause == "NPI_KEYED_WRONG" and on_file is not None:
            problems.append(CAUSE_RULE)
        if cause == "WRONG_PERSON_SELECTED" and on_file is None:
            problems.append(CAUSE_RULE)

    elif cause == "SAME_PERSON_OTHER_NAME":
        if not line_npi_looked_up:
            problems.append("the NPI on the line was not looked up in the registry (run registry_lookup with it)")
        elif not line_npi_looked_up[0]["facts"].get("found"):
            problems.append("the registry has no record of the NPI on the line, so there is no registry record to call the same person")
        if not searched:
            problems.append("the registry was not searched for the name on the line (run registry_search with it)")
        for n in npis_returned - {case["npi"]}:
            if name_agrees_with_registry(case["first"], case["last"], reg.lookup(n)):
                problems.append(f"the registry lists another person (NPI {n}) under the name on the line")

    elif cause in ("DOCUMENT_LOADED_TWICE", "SEPARATE_PAYMENTS"):
        missing = [i for i in line_ids if i not in documents]
        if missing:
            problems.append("source documents were not retrieved for " + ", ".join(missing) + " (run source_documents with those line IDs)")
        else:
            docs = [documents[i] for i in line_ids]
            shared = "yes" if len(set(docs)) < len(docs) else "no"
            if conclusion.get("two_lines_share_a_document") not in (None, shared):
                problems.append(f"two_lines_share_a_document is {shared}: " + ("two lines carry the same document number" if shared == "yes"
                                                                               else "all document numbers in this exception are different"))
            if cause == "SEPARATE_PAYMENTS" and len(set(docs)) < len(docs):
                problems.append("two lines share a document number, so these are not all separate payments")
            if cause == "DOCUMENT_LOADED_TWICE":
                line = value.upper()
                if line not in line_ids:
                    problems.append("the line to remove is not one of the lines in the exception")
                else:
                    twins = [i for i in line_ids if i != line and documents[i] == documents[line]]
                    if not twins:
                        problems.append(f"{line} does not share its document number with another line"
                                        + (": all document numbers in this exception are different" if len(set(docs)) == len(docs) else ""))
                    elif any(loaded[i] > loaded[line] for i in twins):
                        problems.append(f"{line} is not the line with the later load date")

    # The stricter rule. A hand-off that itself names a corrected NPI is sent back, when that NPI came back from the
    # registry in this case, is active and carries the name on the line. The reason given is what the agent wrote, never the answer.
    if STRICT_HANDOFF and case["check"] == "IDENTITY" and cause == "CANNOT_CONFIRM":
        named = re.sub(r"\D", "", value)
        p = reg.lookup(named) if len(named) == 10 and named != case["npi"] and named in npis_returned else None
        if p is not None and p["status"] == "active" and name_agrees_with_registry(case["first"], case["last"], p):
            problems.append(f"you wrote NPI {named} as the fix and still concluded CANNOT_CONFIRM. If the procedure makes that NPI the fix, "
                            "conclude with the cause the procedure gives. If it does not, leave fix_value empty")
    return problems
