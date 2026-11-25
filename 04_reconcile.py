"""Step 4. Reconcile: ledger against filing against registry, under one version of the rules.

Plain code, no model. This step never sees the answer key.

Four checks, each tied to a rule ID and the rule file's version:
  COMPLETENESS  every ledger line that must be reported is in the filing   (R-COMP-01, R-SMALL-01)
  FIELD         amount and date on the filing equal the ledger             (R-FIELD-01)
  IDENTITY      the NPI is in the registry and the name agrees with it     (R-ID-01, R-ID-02)
  LOOKALIKE     lines that share NPI, date, amount and nature              (R-DUP-01)

Every exception gets a priority and one of two routes:
  rule   the ledger settles it, so code proposes the fix (completeness, field)
  agent  it needs lookups and a judgment (identity, look-alike)

    python 04_reconcile.py
        1. baseline: the same checks on the records as published (nothing planted)
        2. the scenario: writes results/exception_log.csv and the key risk indicators
        3. the same completeness check under last year's rule file, to show the version matters
"""
from common import (EXCEPTIONS_CSV, FILING_CSV, LEDGER_CSV, RESULTS, SCENARIO_DIR, load_rules, money,
                    read_csv, write_csv, write_json)
from reconciliation import EXC_FIELDS, KRI_LABELS, kri_lines, kri_status, kri_text, reconcile
from registry import Registry


def main():
    reg = Registry()
    rules = load_rules()
    RESULTS.mkdir(exist_ok=True)

    # 1. baseline on the records as published: the filing is the ledger, line for line
    clean = read_csv(SCENARIO_DIR / "ledger_clean.csv")
    base_exc, base = reconcile(clean, [dict(r) for r in clean], reg, rules)
    lines = kri_lines(base["kris"], rules)
    write_json(RESULTS / "baseline_kris.json", {"rule_version": rules["version"], "kris": base["kris"], "lines": lines,
                                                "exceptions_in_published_records": base["counts"]})

    # 2. the scenario
    ledger, filing = read_csv(LEDGER_CSV), read_csv(FILING_CSV)
    exc, facts = reconcile(ledger, filing, reg, rules)
    write_csv(EXCEPTIONS_CSV, exc, EXC_FIELDS)
    write_json(RESULTS / "kris_draft.json", {"rule_version": rules["version"], "kris": facts["kris"], "facts": facts})

    # 3. the completeness check under last year's rule file
    old = load_rules("2024.1")
    _, old_base = reconcile(clean, [dict(r) for r in clean], reg, old)
    old_exc, _ = reconcile(ledger, filing, reg, old)

    rep = ["# Reconciliation report", "",
           "A replay on public records. Every error here was planted by 03_build_scenario.py, or is a mismatch already in the public records. Not a real filing.", "",
           f"Rule file version {rules['version']} (program year {rules['program_year']}). Plain code, no model.", "",
           "## 1. Baseline: the records as published, nothing planted", "",
           f"- {base['ledger_lines']:,} lines: {base['person_lines']:,} to people, {base['organization_lines']} to organizations (outside the registry checks).",
           f"- Small payments (under {money(rules['rules']['R-SMALL-01']['parameters']['small_payment'])}): {base['small_payment_lines']:,} lines. "
           f"All {base['small_lines_on_recipients_over_yearly']:,} are on recipients whose yearly total is over "
           f"{money(rules['rules']['R-SMALL-01']['parameters']['yearly_total'])}, as the rule requires.",
           f"- Exceptions already in the published records: {base['counts'].get('IDENTITY', 0)} identity, {base['counts'].get('LOOKALIKE', 0)} look-alike groups.", "",
           "## 2. The scenario: ledger and draft filing with planted errors", "",
           f"- Ledger {facts['ledger_lines']:,} lines, draft filing {facts['filing_lines']:,} lines.",
           f"- {len(exc)} exceptions: " + ", ".join(f"{v} {k.lower()}" for k, v in sorted(facts["counts"].items())) + ".",
           f"- Route: {facts['by_route'].get('rule', 0)} settled by rule, {facts['by_route'].get('agent', 0)} sent to the agent.", "",
           "| Key risk indicator | Baseline | Line | Draft | Status |", "|---|---|---|---|---|"]
    for k, label in KRI_LABELS.items():
        rep.append(f"| {label} | {kri_text(k, base['kris'][k])} | {lines[k]['escalate_when']} {kri_text(k, lines[k]['line'])} | "
                   f"{kri_text(k, facts['kris'][k])} | {kri_status(facts['kris'][k], lines[k])} |")
    p24, p25 = old["rules"]["R-SMALL-01"]["parameters"], rules["rules"]["R-SMALL-01"]["parameters"]
    rep += ["", "## 3. Why the rule version is recorded on every exception", "",
            f"The same records under last year's rule file ({old['version']}: {money(p24['small_payment'])} and {money(p24['yearly_total'])}) "
            f"instead of this year's ({rules['version']}: {money(p25['small_payment'])} and {money(p25['yearly_total'])}):", "",
            f"- Lines that count as small payments: {old_base['small_payment_lines']:,} under {old['version']}, {base['small_payment_lines']:,} under {rules['version']}. "
            f"{base['small_payment_lines'] - old_base['small_payment_lines']} lines change treatment.",
            f"- Recipients over the yearly amount: {old_base['recipients_over_yearly']} under {old['version']}, {base['recipients_over_yearly']} under {rules['version']}.",
            f"- Completeness exceptions in the scenario: {sum(e['check']=='COMPLETENESS' for e in old_exc)} under {old['version']}, "
            f"{sum(e['check']=='COMPLETENESS' for e in exc)} under {rules['version']}.", ""]
    (RESULTS / "reconciliation_report.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
