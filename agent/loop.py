"""The agent loop: one exception in, one checked conclusion out.

Each turn the model picks one lookup (or 'conclude') as JSON. Code runs the
lookup and hands back the result with an evidence number. When the model
concludes, code checks the conclusion (agent/checks.py). A conclusion that
fails gets the reason and up to two more tries; after that it goes to a person.
Every step is kept in the trace.

A design choice worth knowing: on a CPU every word the model writes costs
time, so a step is only the lookup and its input. The model gives its reasons
once, at the conclusion, and gives them before it names the cause.
"""
import json

from agent.checks import ACTION, ALLOWED, check
from agent.tools import LOOKUPS
from common import money


class ModelFailed(Exception):
    """The model returned nothing usable for a step, after the interface's own retries."""


MAX_LOOKUPS = 6        # lookups allowed per exception
MAX_REPEATS = 2        # times the model may ask for something it already has before it must conclude
MAX_CONCLUSIONS = 3    # one conclusion, plus two retries after a failed check
STEP_TOKENS, FINAL_TOKENS = 110, 220

STEP_SCHEMA = {
    "type": "object",
    "properties": {"lookup": {"type": "string", "enum": LOOKUPS + ["conclude"]},
                   "input": {"type": "string", "maxLength": 70}},
    "required": ["lookup", "input"],
}
CONCLUDE = {
    "IDENTITY": ("Give your conclusion as JSON, in English. explanation: at most 25 words, the facts from the results that decide it. "
                 "case: A, B or C of the procedure, by what the search found. "
                 "line_npi_in_registry: yes if registry_lookup returned a record for the NPI on the line, no if it said there is none. "
                 "In case B, when there is a record, compare it with the line and answer yes or no: same_first_name, same_city, "
                 "type_fits (is the registry's practitioner type consistent with the type on the line). "
                 "root_cause: the cause the procedure gives. fix_value: the corrected NPI (cases A and C). evidence: the EV numbers you rely on."),
    "LOOKALIKE": ("Give your conclusion as JSON, in English. explanation: at most 25 words, the facts from the results that decide it. "
                  "two_lines_share_a_document: yes or no, as the lookup found. root_cause: the cause the procedure gives. "
                  "fix_value: the line ID to remove (only when two lines share a document). evidence: the EV numbers you rely on."),
}
AGAIN = "Your last conclusion failed the check. Do not repeat it. "


KIND = {"IDENTITY": "RECIPIENT_NOT_VERIFIED", "LOOKALIKE": "POSSIBLE_DUPLICATE"}


def load_procedure(path):
    """Split the procedure file into its sections (the text under each '## NAME' heading)."""
    sections, name = {}, None
    for line in open(path, encoding="utf-8").read().splitlines():
        if line.startswith("## "):
            name = line[3:].strip()
            sections[name] = []
        elif name and not line.startswith("#"):
            sections[name].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def system_prompt(sections, check):
    """What the model is handed: the common part, the procedure for this kind of exception, and the rules."""
    return "\n\n".join([sections["ALWAYS"], sections[KIND[check]], sections["RULES"]])


def tidy(text):
    """The length limit can cut a sentence in half. Keep the full sentences; mark a cut if there are none."""
    text = text.strip()
    if not text or text[-1] in ".!?":
        return text
    cut = max(text.rfind(". "), text.rfind("? "), text.rfind("! "))
    return text[:cut + 1] if cut >= 40 else text + " ..."


def final_schema(case, evidence_ids):
    """The shape of a conclusion. The agent states the deciding facts first, as yes or no, and the shape then
    only admits the cause the procedure gives for those facts (or CANNOT_CONFIRM, which is always open).
    So a conclusion can be wrong about a fact, which code checks, but it cannot contradict the procedure."""
    text = {"type": "string", "maxLength": 200}
    evidence = {"type": "array", "items": {"type": "string", "enum": evidence_ids}, "maxItems": 4}
    fix = {"type": "string", "maxLength": 12}

    def one(*values):
        return {"type": "string", "enum": list(values)}

    def shape(**props):
        props = {"explanation": text, **props, "evidence": evidence}
        return {"type": "object", "properties": props, "required": list(props)}

    if case["check"] == "LOOKALIKE":
        return {"anyOf": [
            shape(two_lines_share_a_document=one("yes"), root_cause=one("DOCUMENT_LOADED_TWICE", "CANNOT_CONFIRM"), fix_value=fix),
            shape(two_lines_share_a_document=one("no"), root_cause=one("SEPARATE_PAYMENTS", "CANNOT_CONFIRM")),
        ]}
    shapes = []
    for letter in ("A", "C"):         # a fix; which of the two causes depends on one fact
        shapes.append(shape(case=one(letter), line_npi_in_registry=one("no"), root_cause=one("NPI_KEYED_WRONG", "CANNOT_CONFIRM"), fix_value=fix))
        shapes.append(shape(case=one(letter), line_npi_in_registry=one("yes"), root_cause=one("WRONG_PERSON_SELECTED", "CANNOT_CONFIRM"), fix_value=fix))
    # case B: no fix. Without a registry record there is nothing to compare. With one, three yes/no comparisons decide.
    b = dict(case=one("B"))
    shapes += [
        shape(**b, line_npi_in_registry=one("no"), root_cause=one("CANNOT_CONFIRM")),
        shape(**b, line_npi_in_registry=one("yes"), same_first_name=one("yes"), same_city=one("yes"), type_fits=one("yes", "no"), root_cause=one("SAME_PERSON_OTHER_NAME")),
        shape(**b, line_npi_in_registry=one("yes"), same_first_name=one("yes"), same_city=one("no"), type_fits=one("yes"), root_cause=one("SAME_PERSON_OTHER_NAME")),
        shape(**b, line_npi_in_registry=one("yes"), same_first_name=one("yes"), same_city=one("no"), type_fits=one("no"), root_cause=one("CANNOT_CONFIRM")),
        shape(**b, line_npi_in_registry=one("yes"), same_first_name=one("no"), same_city=one("yes", "no"), type_fits=one("yes", "no"), root_cause=one("CANNOT_CONFIRM")),
    ]
    return {"anyOf": shapes}


def build_case(exc, by_id, note=""):
    """Turn a row of the exception log into the case the agent sees."""
    lines = [by_id[i] for i in exc["lines"].split("+")]
    first = lines[0]
    kind = KIND[exc["check"]]
    head = f'EXCEPTION {exc["exception_id"]} | {kind} | rule {exc["rule_id"]} version {exc["rule_version"]}\nFound: {exc["what_found"]}'
    detail = (f'{first["name"]} | NPI {first["npi"]} | {first["city"]} {first["state"]} | {first["recipient_type"]} | '
              f'{money(first["amount"])} on {first["pay_date"]} | {first["nature"][:44]}')
    if exc["check"] == "IDENTITY":
        label = f'Line {first["line_id"]}' if len(lines) == 1 else f'First of {len(lines)} lines, {first["line_id"]}'
        body = f"{label}: {detail}"
    else:
        body = f'Lines: {", ".join(l["line_id"] for l in lines)}\nEach line: {detail}'
    text = head + "\n" + body
    if note:
        text += f'\nNote on the line: "{note}"'
    return {"exception_id": exc["exception_id"], "check": exc["check"], "rule_id": exc["rule_id"],
            "rule_version": exc["rule_version"], "key": exc["key"], "lines": lines, "npi": first["npi"],
            "name": first["name"], "first": first["first"], "last": first["last"], "text": text}


def investigate(model, lookups, case, sections, reg):
    messages = [{"role": "system", "content": system_prompt(sections, case["check"])},
                {"role": "user", "content": case["text"] + "\n\nLookups run so far: none. Step 1?"}]
    evidence, trace, conclusions, calls = [], [], [], {}
    usage = {"seconds": 0.0, "tokens_in": 0, "tokens_out": 0, "model_calls": 0}
    repeats = 0

    def ask(schema, max_tokens):
        try:
            obj, u = model.ask(messages, schema, max_tokens)
        except RuntimeError as e:          # the model gave nothing usable: this exception goes to a person
            raise ModelFailed(str(e))
        for k in ("seconds", "tokens_in", "tokens_out"):
            usage[k] += u[k]
        usage["model_calls"] += 1
        messages.append({"role": "assistant", "content": json.dumps(obj)})
        return obj

    def say(text):
        if messages[-1]["role"] == "user":
            messages[-1]["content"] += "\n" + text
        else:
            messages.append({"role": "user", "content": text})

    try:
        while True:
            # ---- one lookup, unless the model is out of lookups
            if len(evidence) < MAX_LOOKUPS and repeats < MAX_REPEATS:
                step = ask(STEP_SCHEMA, STEP_TOKENS)
                if step["lookup"] != "conclude":
                    key = (step["lookup"], " ".join(step["input"].upper().split()))
                    if key in calls:
                        repeats += 1
                        trace.append({**step, "result": f"already ran, see {calls[key]}"})
                        say(f"You already ran that lookup: see {calls[key]}. Run a different lookup, or conclude.")
                        continue
                    text, facts = lookups.run(step["lookup"], step["input"], case)
                    ev = f"EV{len(evidence) + 1}"
                    calls[key] = ev
                    evidence.append({"id": ev, "lookup": step["lookup"], "input": step["input"], "text": text, "facts": facts})
                    trace.append({**step, "result": f"{ev} = {text}"})
                    say(f"{ev} = {text}\nLookups run so far: " + ", ".join(e["lookup"] for e in evidence) + ". Next step of the procedure? If its lookups are done, reply conclude.")
                    continue
                if not evidence:
                    repeats += 1
                    trace.append({**step, "result": "refused: no lookup has been run"})
                    say("You have not run any lookup yet. Run the first lookup of the procedure.")
                    continue
                trace.append({**step, "result": "asked to conclude"})

            # ---- the conclusion, then the checks
            if evidence:
                say((AGAIN if conclusions else "") + CONCLUDE[case["check"]])
                final = ask(final_schema(case, [e["id"] for e in evidence]), FINAL_TOKENS)
            else:
                final = {"explanation": "No lookup was completed.", "root_cause": "CANNOT_CONFIRM", "fix_value": "", "evidence": []}
            final.setdefault("fix_value", "")
            problems = check(case, final, evidence, reg)
            conclusions.append({"conclusion": final, "problems": problems})
            trace.append({"lookup": "CONCLUSION", "input": "", "result": json.dumps(final),
                          "check": "passed" if not problems else "FAILED: " + "; ".join(problems)})
            if not problems or len(conclusions) >= MAX_CONCLUSIONS:
                break
            # Take the failed answer out of the conversation so the model cannot simply copy it, and say what was wrong.
            tried = final["root_cause"] + (f', fix {final["fix_value"]}' if final.get("fix_value") else "")
            messages[-1] = {"role": "assistant", "content": json.dumps({"conclusion": "withdrawn"})}
            say(f"CHECK FAILED on your conclusion ({tried}): " + "; ".join(problems) + ". Correct this: run the missing lookup, "
                "or conclude again with a different answer. If the evidence does not settle it, conclude CANNOT_CONFIRM.")
    except ModelFailed as e:
        final = {"explanation": "The model did not return a usable answer.", "root_cause": "CANNOT_CONFIRM", "fix_value": "", "evidence": []}
        problems = ["the model gave no usable answer: " + str(e)]
        conclusions.append({"conclusion": final, "problems": problems})
        trace.append({"lookup": "CONCLUSION", "input": "", "result": json.dumps(final), "check": "FAILED: " + problems[0]})

    passed = not problems
    cause = final["root_cause"] if passed else "CANNOT_CONFIRM"
    action = ACTION[cause]
    if not passed:
        status, reason = "to a person", "failed the checks"
    elif cause == "CANNOT_CONFIRM":
        status, reason = "to a person", "the agent could not confirm"
    else:
        status, reason = "proposed", "passed the checks"
    return {
        "exception_id": case["exception_id"], "check": case["check"], "key": case["key"],
        "status": status, "reason": reason, "root_cause": cause, "action": action,
        "fix_value": final["fix_value"].strip().upper() if action in ("FIX_NPI", "REMOVE_LINE") else "",
        "evidence_cited": final["evidence"], "explanation": tidy(final["explanation"]),
        "first_conclusion": conclusions[0]["conclusion"], "first_problems": conclusions[0]["problems"],
        "last_conclusion": final, "last_problems": problems, "n_conclusions": len(conclusions),
        "lookups": [e["lookup"] for e in evidence],
        "evidence": [{"id": e["id"], "lookup": e["lookup"], "input": e["input"], "text": e["text"]} for e in evidence],
        "trace": trace, **{k: (round(v, 1) if k == "seconds" else v) for k, v in usage.items()},
    }
