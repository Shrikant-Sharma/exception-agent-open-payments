# Remediation report

A replay on public records with planted errors. Not a real filing.

Agent runs used: dev,test. Every agent proposal that passed the checks is treated as approved, to show what an unattended run would do. In real use a person approves each one.

## Where the exceptions ended

| Status | Exceptions |
|---|---|
| approved in the replay, applied | 116 |
| applied by rule | 37 |
| waiting for a person | 14 |

Re-run of the reconciliation on the corrected books: 153 applied fixes closed, 0 still open, 0 new exceptions created by a fix.

## The filing against the records as published

A line agrees when its NPI, amount and date match the published record. 5,885 published records.

| Stage | Lines that agree | Missing | Differ | Extra lines |
|---|---|---|---|---|
| Draft | 5,704 | 102 | 79 | 22 |
| After rule fixes | 5,831 | 0 | 54 | 22 |
| After agent proposals | 5,869 | 0 | 16 | 0 |
