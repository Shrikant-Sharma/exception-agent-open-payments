# Reconciliation report

A replay on public records. Every error here was planted by 03_build_scenario.py, or is a mismatch already in the public records. Not a real filing.

Rule file version 2025.1 (program year 2025). Plain code, no model.

## 1. Baseline: the records as published, nothing planted

- 5,885 lines: 5,882 to people, 3 to organizations (outside the registry checks).
- Small payments (under $13.46): 1,332 lines. All 1,332 are on recipients whose yearly total is over $134.54, as the rule requires.
- Exceptions already in the published records: 13 identity, 45 look-alike groups.

## 2. The scenario: ledger and draft filing with planted errors

- Ledger 5,907 lines, draft filing 5,805 lines.
- 167 exceptions: 12 completeness, 25 field, 63 identity, 67 lookalike.
- Route: 37 settled by rule, 130 sent to the agent.

| Key risk indicator | Baseline | Line | Draft | Status |
|---|---|---|---|---|
| Lines verified against the registry (%) | 98.79 | below 98.54 | 98.05 | ESCALATE |
| Reportable ledger lines in the filing (%) | 100.00 | below 99.75 | 98.27 | ESCALATE |
| Filing lines that agree with the ledger (%) | 100.00 | below 99.75 | 99.57 | ESCALATE |
| Look-alike lines per 1,000 | 20.74 | above 25.92 | 28.12 | ESCALATE |
| Dollars on lines with an open exception | $423,193.72 | above $528,992.15 | $432,296.53 | within line |

## 3. Why the rule version is recorded on every exception

The same records under last year's rule file (2024.1: $13.07 and $130.66) instead of this year's (2025.1: $13.46 and $134.54):

- Lines that count as small payments: 1,289 under 2024.1, 1,332 under 2025.1. 43 lines change treatment.
- Recipients over the yearly amount: 286 under 2024.1, 282 under 2025.1.
- Completeness exceptions in the scenario: 12 under 2024.1, 12 under 2025.1.
