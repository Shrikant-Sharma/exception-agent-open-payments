"""The reconciliation itself: four checks under one version of the rule file, and the key risk indicators.

Plain code, no model, and no access to the answer key. Used by 04_reconcile.py
(the draft filing), 07_remediate.py (the filing after fixes) and 08_summary.py.
"""
import collections
import math

from common import money, name_agrees_with_registry, npi_check_digit_ok

KRI_LABELS = collections.OrderedDict([
    ("registry_verified_pct", "Lines verified against the registry (%)"),
    ("completeness_pct", "Reportable ledger lines in the filing (%)"),
    ("field_agreement_pct", "Filing lines that agree with the ledger (%)"),
    ("lookalike_lines_per_1000", "Look-alike lines per 1,000"),
    ("open_exception_dollars", "Dollars on lines with an open exception"),
])


def kri_text(key, value):
    return f"${value:,.2f}" if key.endswith("dollars") else f"{value:,.2f}"


EXC_FIELDS = ["exception_id", "check", "rule_id", "rule_version", "route", "key", "n_lines", "dollars",
              "priority", "what_found", "rule_fix", "lines"]


def must_report(line, yearly_total, p):
    """R-SMALL-01. A small payment may be left out only if the recipient's yearly total is not over the yearly amount."""
    return float(line["amount"]) >= p["small_payment"] or yearly_total > p["yearly_total"]


def reconcile(ledger, filing, reg, rules):
    """Run the four checks. Returns (exceptions, facts) where facts feed the key risk indicators."""
    version = rules["version"]
    p_small = rules["rules"]["R-SMALL-01"]["parameters"]
    weights = rules["priority_weights"]
    people = [r for r in ledger if r["recipient_kind"] == "person"]
    filed = {f["line_id"]: f for f in filing}
    yearly = collections.Counter()
    for r in people:
        yearly[r["npi"]] += float(r["amount"])

    out = []

    def raise_exception(check, rule_id, key, lines, what, rule_fix=""):
        dollars = round(sum(float(l["amount"]) for l in lines), 2)
        sev = rules["rules"][rule_id]["severity"]
        priority = (weights["severity"] * sev + weights["log10_dollars"] * math.log10(1 + dollars)
                    + weights["lines_up_to_10"] * min(len(lines), 10))
        out.append({"check": check, "rule_id": rule_id, "rule_version": version,
                    "route": rules["rules"][rule_id]["handled_by"], "key": key, "n_lines": len(lines),
                    "dollars": f"{dollars:.2f}", "priority": f"{priority:.2f}", "what_found": what,
                    "rule_fix": rule_fix, "lines": "+".join(l["line_id"] for l in lines)})

    # ---- COMPLETENESS: ledger lines that are not in the filing
    missing = collections.defaultdict(list)
    reportable, reportable_filed, left_out_ok = 0, 0, 0
    for r in people:
        need = must_report(r, yearly[r["npi"]], p_small)
        reportable += need
        if r["line_id"] in filed:
            reportable_filed += need
        elif need:
            missing[r["npi"]].append(r)
        else:
            left_out_ok += 1
    for npi, lines in sorted(missing.items()):
        n_small = sum(float(l["amount"]) < p_small["small_payment"] for l in lines)
        what = (f'{len(lines)} ledger lines for NPI {npi} are not in the filing. {n_small} are under {money(p_small["small_payment"])}, '
                f'but the recipient\'s yearly total is {money(yearly[npi])}, over {money(p_small["yearly_total"])}, so all must be reported.')
        raise_exception("COMPLETENESS", "R-SMALL-01" if n_small == len(lines) else "R-COMP-01", npi, lines, what, "ADD_LINES")

    # ---- FIELD: amount and date
    agree = 0
    for r in ledger:
        f = filed.get(r["line_id"])
        if f is None:
            continue
        diffs = [(k, f[k], r[k]) for k in ("amount", "pay_date") if f[k] != r[k]]
        if not diffs:
            agree += 1
            continue
        what = "; ".join(f"filing {k} {fv}, ledger {k} {lv}" for k, fv, lv in diffs)
        fix = "SET_FROM_LEDGER:" + ",".join(f"{k}={lv}" for k, fv, lv in diffs)
        raise_exception("FIELD", "R-FIELD-01", r["line_id"], [r], what, fix)

    # ---- IDENTITY: one exception per (NPI, name) pair the registry does not support
    pairs = collections.defaultdict(list)
    for r in people:
        pairs[(r["npi"], r["name"])].append(r)
    verified_lines = 0
    for (npi, name), lines in sorted(pairs.items()):
        p = reg.lookup(npi)
        if p is None:
            digit = "valid" if npi_check_digit_ok(npi) else "not valid"
            raise_exception("IDENTITY", "R-ID-01", f"{npi}|{name}", lines,
                            f"NPI {npi} is on {len(lines)} ledger line(s) under the name {name}. The registry has no record of that NPI (check digit {digit}).")
        elif p["status"] != "active":
            raise_exception("IDENTITY", "R-ID-01", f"{npi}|{name}", lines,
                            f"NPI {npi} is on {len(lines)} ledger line(s) under the name {name}. The registry record is not active.")
        elif not name_agrees_with_registry(lines[0]["first"], lines[0]["last"], p):
            raise_exception("IDENTITY", "R-ID-02", f"{npi}|{name}", lines,
                            f"NPI {npi} is on {len(lines)} ledger line(s) under the name {name}. The registry lists that NPI under a different name.")
        else:
            verified_lines += len(lines)

    # ---- LOOKALIKE
    groups = collections.defaultdict(list)
    for r in people:
        groups[(r["npi"], r["pay_date"], r["amount"], r["nature"])].append(r)
    lookalike_lines = 0
    for key, lines in sorted(groups.items()):
        if len(lines) > 1:
            lookalike_lines += len(lines)
            raise_exception("LOOKALIKE", "R-DUP-01", "+".join(sorted(l["line_id"] for l in lines)), lines,
                            f"{len(lines)} ledger lines share NPI {key[0]}, date {key[1]}, amount {money(key[2])} and nature of payment.")

    out.sort(key=lambda e: (-float(e["priority"]), e["check"], e["key"]))
    for n, e in enumerate(out, 1):
        e["exception_id"] = f"E-{n:03d}"

    by_id = {r["line_id"]: r for r in ledger}
    open_lines = {i for e in out for i in e["lines"].split("+")}
    facts = {
        "ledger_lines": len(ledger), "person_lines": len(people), "organization_lines": len(ledger) - len(people),
        "filing_lines": len(filing), "left_out_and_allowed": left_out_ok,
        "kris": {
            "registry_verified_pct": round(100 * verified_lines / len(people), 3),
            "completeness_pct": round(100 * reportable_filed / reportable, 3),
            "field_agreement_pct": round(100 * agree / len(filing), 3),
            "lookalike_lines_per_1000": round(1000 * lookalike_lines / len(people), 2),
            "open_exception_dollars": round(sum(float(by_id[i]["amount"]) for i in open_lines), 2),
        },
        "counts": dict(collections.Counter(e["check"] for e in out)),
        "by_route": dict(collections.Counter(e["route"] for e in out)),
        "small_payment_lines": sum(float(r["amount"]) < p_small["small_payment"] for r in people),
        "small_lines_on_recipients_over_yearly": sum(float(r["amount"]) < p_small["small_payment"] and yearly[r["npi"]] > p_small["yearly_total"] for r in people),
        "recipients_over_yearly": sum(v > p_small["yearly_total"] for v in yearly.values()),
    }
    return out, facts


def kri_lines(baseline, rules):
    """Escalation lines: the baseline moved by the margin written in the rule file."""
    lines = {}
    for k, spec in rules["kri_lines"].items():
        if k == "note":
            continue
        b = baseline[k]
        lines[k] = {"escalate_when": spec["escalate_when"],
                    "line": round(b - spec["margin_points"], 3) if "margin_points" in spec else round(b * spec["margin_factor"], 2)}
    return lines


def kri_status(value, line):
    bad = value < line["line"] if line["escalate_when"] == "below" else value > line["line"]
    return "ESCALATE" if bad else "within line"
