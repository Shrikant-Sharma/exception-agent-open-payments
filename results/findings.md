# Findings: one write-up per exception the agent investigated

A replay on public records. Every error below was planted by 03_build_scenario.py, or is a name difference already in the public records. Nobody named on this page made a mistake.

Each fact below is filled in by code from the exception log, the rule file and the lookup results. The model's own words appear only inside quotation marks.

### E-001: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1891713905 is on 11 ledger line(s) under the name JACQUELINE ANN FOURNIER. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry found NPI on line under different name, search found same NPI."
- **Impact.** 11 line(s), $357.08. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1891713905): NPI 1891713905: JACQUELINE FOURNIER COOK, PA | Physician Assistant, Medical | CONCORD NH | active | other names listed: none
    - EV2, registry_search(JACQUELINE ANN FOURNIER): SEARCH FOUND ONLY THE NPI ALREADY ON THE LINE under the name JACQUELINE ANN FOURNIER: / NPI 1891713905: JACQUELINE FOURNIER COOK, PA | Physician Assistant, Medical | CONCORD NH | active | other names listed: none | SAME NPI AS THE LINE
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-002: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1700079118 is on 18 ledger line(s) under the name ELIZABETH M GEMBA. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry lists NPI 1700079118 under ELIZABETH MARIE SILVESTRI, PA-C. Line name is ELIZABETH M GEMBA. Same first name, same city (Salem NH), type fits (Physician Assistant)."
- **Impact.** 18 line(s), $266.26. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1700079118): NPI 1700079118: ELIZABETH MARIE SILVESTRI, PA-C | Physician Assistant, Medical | SALEM NH | active | other names listed: ELIZABETH CURRAN
    - EV2, registry_search(ELIZABETH M GEMBA): SEARCH FOUND NOBODY registered under the name ELIZABETH M GEMBA.
    - EV3, registry_search(ELIZABETH): Input must be a first and last name.
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-003: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1831940444 is on 13 ledger line(s) under the name BRENDA E LAPIERRE. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry NPI matches line NPI with same first name and city."
- **Impact.** 13 line(s), $261.89. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1831940444): NPI 1831940444: BRENDA MACDONALD, APRN | Nurse Practitioner, Family | AMHERST NH | active | other names listed: none
    - EV3, registry_search(BRENDA MACDONALD): SEARCH FOUND ONLY THE NPI ALREADY ON THE LINE under the name BRENDA MACDONALD: / NPI 1831940444: BRENDA MACDONALD, APRN | Nurse Practitioner, Family | AMHERST NH | active | other names listed: none | SAME NPI AS THE LINE
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-004: Separate payments. Proposed, waiting for approval.

- **Condition.** 8 ledger lines share NPI 1023139250, date 2025-09-25, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are unique; separate payments."
- **Impact.** 8 line(s), $36,400.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L04516,L04517,L04519,L04520,L04521,L04522,L04523,L04524): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L04516: document AP-25-000212 | accounts payable | loaded 2025-10-03 / L04517: document AP-25-000213 | accounts payable | loaded 2025-10-03 / L04519: document AP-25-000215 | accounts payable | loaded 2025-10-03 / L04520: document AP-25-000216 | accounts payable | loaded 2025-10-03 / L04521: document AP-25-000217 | accounts payable | loaded 2025-10-03 / L04522: document AP-25-000218 | accounts payable | loaded 2025-10-03 / L04523: document AP-25-000219 | accounts payable | loaded 2025-10-03 / L04524: document AP-25-000220 | accounts payable | loaded 2025-10-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-009: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1582656774 is on 1 ledger line(s) under the name ANNE L SPERANZA. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry has no record for NPI on line. Search found nobody. Case B: CANNOT_CONFIRM."
- **Impact.** 1 line(s), $43.80. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1582656774): NPI 1582656774: no registry record. Check digit not valid.
    - EV2, registry_search(ANNE L SPERANZA): SEARCH FOUND NOBODY registered under the name ANNE L SPERANZA.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-010: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1972912616 is on 7 ledger line(s) under the name KARA C DOBERSTEIN. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry has NPI 1972912616 under KARA CLARK SPECTOR, same first name and city, type fits."
- **Impact.** 7 line(s), $261.46. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1972912616): NPI 1972912616: KARA CLARK SPECTOR, MS, FNP-C | Family Medicine | MEREDITH NH | active | other names listed: none
    - EV2, registry_search(KARA C DOBERSTEIN): SEARCH FOUND NOBODY registered under the name KARA C DOBERSTEIN.
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-013: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1586622801 is on 1 ledger line(s) under the name YOKO FUKUDA. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $33.37. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1586622801): NPI 1586622801: no registry record. Check digit not valid.
    - EV2, registry_search(YOKO FUKUDA): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name YOKO FUKUDA: / NPI 1568622801: YOKO FUKUDA, M.D. | Internal Medicine, Hematology & Oncology | PORTSMOUTH NH | active | other names listed: YOKO KORENAGA | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L02201 to 1568622801.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-014: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1295979799 is on 1 ledger line(s) under the name JOSEPH T HYATT. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $32.94. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1295979799): NPI 1295979799: no registry record. Check digit not valid.
    - EV2, registry_search(JOSEPH T HYATT): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JOSEPH T HYATT: / NPI 1295799799: JOSEPH T HYATT, MD | Anesthesiology | NASHUA NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L01047 to 1295799799.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-015: Could not be confirmed. Sent to a person: failed the checks.

- **Condition.** NPI 1821713905 is on 1 ledger line(s) under the name JACQUELINE ANN FOURNIER. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry lookup for line NPI shows no record, search found a matching NPI with name discrepancy."
- **Impact.** 1 line(s), $32.95. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1821713905): NPI 1821713905: no registry record. Check digit not valid.
    - EV4, registry_search(JACQUELINE FOURNIER COOK): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JACQUELINE FOURNIER COOK: / NPI 1891713905: JACQUELINE FOURNIER COOK, PA | Physician Assistant, Medical | CONCORD NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-016: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1832118017 is on 1 ledger line(s) under the name GEOFFREY STARR. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $30.48. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1832118017): NPI 1832118017: no registry record. Check digit not valid.
    - EV2, registry_search(GEOFFREY STARR): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name GEOFFREY STARR: / NPI 1831118017: GEOFFREY E STARR, M.D. | Psychiatry & Neurology, Neurology | EXETER NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Change the NPI on L04950 to 1831118017.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-017: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1417394311 is on 1 ledger line(s) under the name EDWARD PAUL DOHERTY. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Search found 3 people (case C). Fix is NPI differing in 1-2 digits (1417394131)."
- **Impact.** 1 line(s), $30.18. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1417394311): NPI 1417394311: no registry record. Check digit not valid.
    - EV2, registry_search(EDWARD PAUL DOHERTY): SEARCH FOUND 3 PEOPLE under the name EDWARD PAUL DOHERTY: / NPI 1417394131: EDWARD P DOHERTY, M.D. | Anesthesiology, Pain Medicine | NASHUA NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits / NPI 1407849870: EDWARD M. DOHERTY, A.T.,C | Specialist/Technologist, Athletic Trainer | BELMONT MA | active | other names listed: none | differs from the NPI on the line in 7 of 10 digits / NPI 1598127367: EDWARD DOHERTY, RPH | Pharmacist | STRATHAM NH | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits
    - EV3, ledger_history(EDWARD PAUL DOHERTY): Ledger lines under the name EDWARD PAUL DOHERTY: 17 lines carry NPI 1417394131; 1 line carries NPI 1417394311.
- **Recommendation.** Change the NPI on L01039 to 1417394131.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-018: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1358486717 is on 1 ledger line(s) under the name TIMOTHY SULLIVAN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Search found 2 people, NPI 1538486717 differs in 2 digits, fix is that NPI ..."
- **Impact.** 1 line(s), $29.90. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1358486717): NPI 1358486717: no registry record. Check digit not valid.
    - EV2, registry_search(TIMOTHY SULLIVAN): SEARCH FOUND 2 PEOPLE under the name TIMOTHY SULLIVAN: / NPI 1538486717: TIMOTHY W SULLIVAN, MD | Ophthalmology | PORTSMOUTH NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits / NPI 1972179893: TIMOTHY JAMES SULLIVAN | Pharmacy Technician | CONCORD NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L01847 to 1538486717.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-019: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1558945876 is on 1 ledger line(s) under the name CAITLYN HUTTER. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $29.89. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1558945876): NPI 1558945876: no registry record. Check digit not valid.
    - EV2, registry_search(CAITLYN HUTTER): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name CAITLYN HUTTER: / NPI 1558915876: CAITLYN HUTTER | Nurse Practitioner, Family | AMHERST NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Change the NPI on L02092 to 1558915876.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-020: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1631371263 is on 1 ledger line(s) under the name MICHAEL R KACZANOWSKI. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry has no record for line's NPI. Search found one person with different NPI."
- **Impact.** 1 line(s), $28.60. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1631371263): NPI 1631371263: no registry record. Check digit not valid.
    - EV2, registry_search(MICHAEL R KACZANOWSKI): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name MICHAEL R KACZANOWSKI: / NPI 1639371263: MICHAEL ROBERT KACZANOWSKI, M.D. | Internal Medicine, Gastroenterology | NASHUA NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Change the NPI on L02386 to 1639371263.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-021: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1912017285 is on 1 ledger line(s) under the name JOEL R TUITE. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for NPI on line. Registry search found one person with different NPI."
- **Impact.** 1 line(s), $26.70. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1912017285): NPI 1912017285: no registry record. Check digit not valid.
    - EV2, registry_search(JOEL R TUITE): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JOEL R TUITE: / NPI 1912107285: JOEL ROBERT TUITE, O.D. | Optometrist | LITTLETON NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L04529 to 1912107285.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-022: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1255692378 is on 1 ledger line(s) under the name MARIA T BOYLAN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "No registry record for NPI on line. Search found nobody. Case B: CANNOT_CONFIRM."
- **Impact.** 1 line(s), $26.05. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1255692378): NPI 1255692378: no registry record. Check digit not valid.
    - EV2, registry_search(MARIA T BOYLAN): SEARCH FOUND NOBODY registered under the name MARIA T BOYLAN.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-023: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1154344502 is on 1 ledger line(s) under the name NANCY KATHY GILBERT. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $25.38. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1154344502): NPI 1154344502: no registry record. Check digit not valid.
    - EV2, registry_search(NANCY KATHY GILBERT): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name NANCY KATHY GILBERT: / NPI 1154344505: NANCY K GILBERT, APRN | Nurse Practitioner, Psych/Mental Health | NASHUA NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Change the NPI on L05076 to 1154344505.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-024: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1083805410 is on 1 ledger line(s) under the name MICHELLE T LINCOLN. The registry has no record of that NPI (check digit valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "No registry record for NPI on line. Search found nobody. Case B: CANNOT_CONFIRM."
- **Impact.** 1 line(s), $24.24. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1083805410): NPI 1083805410: no registry record. Check digit valid.
    - EV2, registry_search(MICHELLE T LINCOLN): SEARCH FOUND NOBODY registered under the name MICHELLE T LINCOLN.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-025: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 9172912616 is on 1 ledger line(s) under the name KARA C DOBERSTEIN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "No registry record for NPI on line. Search found nobody."
- **Impact.** 1 line(s), $24.20. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(9172912616): NPI 9172912616: no registry record. Check digit not valid.
    - EV2, registry_search(KARA C DOBERSTEIN): SEARCH FOUND NOBODY registered under the name KARA C DOBERSTEIN.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-026: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1104370124 is on 1 ledger line(s) under the name ERIC A SENNEVILLE. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the NPI on the line. Search found one person with a different NPI."
- **Impact.** 1 line(s), $23.56. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1104370124): NPI 1104370124: no registry record. Check digit not valid.
    - EV2, registry_search(ERIC A SENNEVILLE): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name ERIC A SENNEVILLE: / NPI 1104370154: ERIC ALLEN SENNEVILLE, PA-C | Physician Assistant, Medical | HOOKSETT NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Change the NPI on L02438 to 1104370154.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-027: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1729558960 is on 1 ledger line(s) under the name AMANDA GRIFFIN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $21.27. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1729558960): NPI 1729558960: no registry record. Check digit not valid.
    - EV2, registry_search(AMANDA GRIFFIN): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name AMANDA GRIFFIN: / NPI 1629558960: AMANDA N GRIFFIN, NP | Nurse Practitioner, Family | CONCORD NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Change the NPI on L01792 to 1629558960.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-028: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1962429387 is on 1 ledger line(s) under the name ROSE S EHRET. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup failed; search found one person with different NPI."
- **Impact.** 1 line(s), $20.96. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1962429387): NPI 1962429387: no registry record. Check digit not valid.
    - EV2, registry_search(ROSE S EHRET): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name ROSE S EHRET: / NPI 1962429837: ROSE S EHRET, MD | Psychiatry & Neurology, Psychiatry | MANCHESTER NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L00519 to 1962429837.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-029: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 9172283778 is on 1 ledger line(s) under the name EMMA KENNEY. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "No registry record for NPI on line. Search found nobody. Case B: CANNOT_CONFIRM."
- **Impact.** 1 line(s), $20.75. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(9172283778): NPI 9172283778: no registry record. Check digit not valid.
    - EV2, registry_search(EMMA KENNEY): SEARCH FOUND NOBODY registered under the name EMMA KENNEY.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-030: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1952858394 is on 1 ledger line(s) under the name CONSOLATA OMINGO. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $20.06. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1952858394): NPI 1952858394: no registry record. Check digit not valid.
    - EV2, registry_search(CONSOLATA OMINGO): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name CONSOLATA OMINGO: / NPI 1952885394: CONSOLATA OMINGO, APRN | Nurse Practitioner, Psych/Mental Health | NASHUA NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L05764 to 1952885394.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-031: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1528656774 is on 7 ledger line(s) under the name ANNE L SPERANZA. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry shows same first name, city, and type fits. Case B, line_npi_in_registry: yes."
- **Impact.** 7 line(s), $125.64. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1528656774): NPI 1528656774: ANNE KEZER, PA | Physician Assistant | NASHUA NH | active | other names listed: none
    - EV3, registry_search(ANNE KEZER): SEARCH FOUND ONLY THE NPI ALREADY ON THE LINE under the name ANNE KEZER: / NPI 1528656774: ANNE KEZER, PA | Physician Assistant | NASHUA NH | active | other names listed: none | SAME NPI AS THE LINE
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-032: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1821829119 is on 1 ledger line(s) under the name NATHANIEL N BROWN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry lookup failed. Search found 2 people; no NPI matches line's NPI in 1-2 digits. Conclude C."
- **Impact.** 1 line(s), $18.69. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1821829119): NPI 1821829119: no registry record. Check digit not valid.
    - EV2, registry_search(NATHANIEL N BROWN): SEARCH FOUND 2 PEOPLE under the name NATHANIEL N BROWN: / NPI 1821821919: NATHANIEL BROWN | Nurse Practitioner, Psych/Mental Health | CONCORD NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits / NPI 1750657755: NATHANIEL JOSEPH BROWN, MD, PHD | Anesthesiology | SANTA FE NM | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-033: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1780914001 is on 1 ledger line(s) under the name JENNIFER SUSANN MAYNARD. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Search found 2 people, none with NPI differing by 1-2 digits."
- **Impact.** 1 line(s), $18.27. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1780914001): NPI 1780914001: no registry record. Check digit not valid.
    - EV2, registry_search(JENNIFER SUSANN MAYNARD): SEARCH FOUND 2 PEOPLE under the name JENNIFER SUSANN MAYNARD: / NPI 1780924001: JENNIFER SUSANN MAYNARD, APRN | Nurse Practitioner, Psych/Mental Health | HOPKINTON NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits / NPI 1093321036: JENNIFER MAYNARD, CCC-SLP | Speech-Language Pathologist,   | CLAREMONT NH | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-034: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1184907080 is on 1 ledger line(s) under the name CARA JEAN DONAGHEY. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry has no record for NPI on line. Search found one person with different NPI."
- **Impact.** 1 line(s), $17.06. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1184907080): NPI 1184907080: no registry record. Check digit not valid.
    - EV2, registry_search(CARA JEAN DONAGHEY): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name CARA JEAN DONAGHEY: / NPI 1184907800: CARA-JEAN DONAGHEY, ANP | Nurse Practitioner, Adult Health | NASHUA NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L01651 to 1184907800.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-035: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1366535398 is on 1 ledger line(s) under the name JEROME RAMOS-ESTEBAN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for NPI on line. Registry search found one person with different NPI."
- **Impact.** 1 line(s), $15.70. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1366535398): NPI 1366535398: no registry record. Check digit not valid.
    - EV2, registry_search(JEROME RAMOS-ESTEBAN): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JEROME RAMOS-ESTEBAN: / NPI 1366553398: JEROME C RAMOS ESTEBAN, MD | Ophthalmology | CONCORD NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L02901 to 1366553398.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-036: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1548435620 is on 1 ledger line(s) under the name FREDERICK LANSIGAN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for NPI on line. Registry search found one person with different NPI."
- **Impact.** 1 line(s), $15.00. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1548435620): NPI 1548435620: no registry record. Check digit not valid.
    - EV2, registry_search(FREDERICK LANSIGAN): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name FREDERICK LANSIGAN: / NPI 1548436520: FREDERICK LANSIGAN, M.D. | Internal Medicine, Hematology & Oncology | LEBANON NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L05629 to 1548436520.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-037: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1249545484 is on 1 ledger line(s) under the name SHELLEY R REED. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $14.75. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1249545484): NPI 1249545484: no registry record. Check digit not valid.
    - EV2, registry_search(SHELLEY R REED): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name SHELLEY R REED: / NPI 1245945484: SHELLEY R REED, APRN | Nurse Practitioner, Family | LONDONDERRY NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L00816 to 1245945484.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-038: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1455859757 is on 1 ledger line(s) under the name CAROLYN JAMIE KUSSMAUL. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "No registry record for NPI on line. Search found nobody."
- **Impact.** 1 line(s), $14.65. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1455859757): NPI 1455859757: no registry record. Check digit not valid.
    - EV2, registry_search(CAROLYN JAMIE KUSSMAUL): SEARCH FOUND NOBODY registered under the name CAROLYN JAMIE KUSSMAUL.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-039: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1306617424 is on 1 ledger line(s) under the name CHAD HARTMAN MESHBERGER. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry has no record for line's NPI. Search found one person with different NPI."
- **Impact.** 1 line(s), $13.53. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1306617424): NPI 1306617424: no registry record. Check digit not valid.
    - EV2, registry_search(CHAD HARTMAN MESHBERGER): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name CHAD HARTMAN MESHBERGER: / NPI 1306167424: CHAD H MESHBERGER, DO | Psychiatry & Neurology, Neurology | CONCORD NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L05465 to 1306167424.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-040: Separate payments. Proposed, waiting for approval.

- **Condition.** 5 ledger lines share NPI 1023139250, date 2025-01-15, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different; no duplicates."
- **Impact.** 5 line(s), $22,750.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L00281,L00282,L00283,L00284,L00285): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L00281: document AP-25-000010 | accounts payable | loaded 2025-02-03 / L00282: document AP-25-000011 | accounts payable | loaded 2025-02-03 / L00283: document AP-25-000012 | accounts payable | loaded 2025-02-03 / L00284: document AP-25-000013 | accounts payable | loaded 2025-02-03 / L00285: document AP-25-000014 | accounts payable | loaded 2025-02-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-041: Separate payments. Proposed, waiting for approval.

- **Condition.** 5 ledger lines share NPI 1023139250, date 2025-11-13, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different; no duplicate lines."
- **Impact.** 5 line(s), $22,750.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05334,L05335,L05336,L05337,L05338): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05334: document AP-25-000260 | accounts payable | loaded 2025-12-03 / L05335: document AP-25-000261 | accounts payable | loaded 2025-12-03 / L05336: document AP-25-000262 | accounts payable | loaded 2025-12-03 / L05337: document AP-25-000263 | accounts payable | loaded 2025-12-03 / L05338: document AP-25-000264 | accounts payable | loaded 2025-12-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-042: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1346724941 is on 1 ledger line(s) under the name WENDY L WRIGHT. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the line's NPI. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $10.00. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1346724941): NPI 1346724941: no registry record. Check digit not valid.
    - EV2, registry_search(WENDY L WRIGHT): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name WENDY L WRIGHT: / NPI 1346274941: WENDY L WRIGHT, ARNP | Nurse Practitioner, Family | AMHERST NH | active | other names listed: none | differs from the NPI on the line in 2 of 10 digits
- **Recommendation.** Change the NPI on L05624 to 1346274941.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-043: Separate payments. Proposed, waiting for approval.

- **Condition.** 4 ledger lines share NPI 1023139250, date 2025-02-04, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different; separate payments."
- **Impact.** 4 line(s), $18,200.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L00640,L00642,L00643,L00644): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L00640: document AP-25-000020 | accounts payable | loaded 2025-03-03 / L00642: document AP-25-000022 | accounts payable | loaded 2025-03-03 / L00643: document AP-25-000023 | accounts payable | loaded 2025-03-03 / L00644: document AP-25-000024 | accounts payable | loaded 2025-03-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-044: Separate payments. Proposed, waiting for approval.

- **Condition.** 4 ledger lines share NPI 1023139250, date 2025-03-04, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different, so separate payments."
- **Impact.** 4 line(s), $18,200.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01098,L01099,L01100,L01101): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01098: document AP-25-000034 | accounts payable | loaded 2025-04-03 / L01099: document AP-25-000035 | accounts payable | loaded 2025-04-03 / L01100: document AP-25-000036 | accounts payable | loaded 2025-04-03 / L01101: document AP-25-000037 | accounts payable | loaded 2025-04-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-045: Separate payments. Proposed, waiting for approval.

- **Condition.** 4 ledger lines share NPI 1023139250, date 2025-05-28, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different; separate payments."
- **Impact.** 4 line(s), $18,200.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02868,L02870,L02871,L02872): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02868: document AP-25-000128 | accounts payable | loaded 2025-06-03 / L02870: document AP-25-000130 | accounts payable | loaded 2025-06-03 / L02871: document AP-25-000131 | accounts payable | loaded 2025-06-03 / L02872: document AP-25-000132 | accounts payable | loaded 2025-06-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-046: Separate payments. Proposed, waiting for approval.

- **Condition.** 4 ledger lines share NPI 1023139250, date 2025-07-17, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different, so separate payments."
- **Impact.** 4 line(s), $18,200.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L03580,L03581,L03582,L03585): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L03580: document AP-25-000165 | accounts payable | loaded 2025-08-03 / L03581: document AP-25-000166 | accounts payable | loaded 2025-08-03 / L03582: document AP-25-000167 | accounts payable | loaded 2025-08-03 / L03585: document AP-25-000169 | accounts payable | loaded 2025-08-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-047: Separate payments. Proposed, waiting for approval.

- **Condition.** 4 ledger lines share NPI 1023139250, date 2025-10-29, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different; separate payments."
- **Impact.** 4 line(s), $18,200.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05042,L05043,L05044,L05046): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05042: document AP-25-000243 | accounts payable | loaded 2025-11-03 / L05043: document AP-25-000244 | accounts payable | loaded 2025-11-03 / L05044: document AP-25-000245 | accounts payable | loaded 2025-11-03 / L05046: document AP-25-000247 | accounts payable | loaded 2025-11-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-049: NPI typed wrong. Proposed, waiting for approval.

- **Condition.** NPI 1144478386 is on 1 ledger line(s) under the name MARIA A MARTIN. The registry has no record of that NPI (check digit not valid).
- **Criteria.** R-ID-01, rule file 2025.1: The NPI on a line has an active record in the NPI registry. (42 CFR 403.904(c)(3)(ii): National Provider Identifier as listed in the NPPES)
- **Cause.** NPI typed wrong. Agent's explanation: "Registry lookup found no record for the NPI on the line. Registry search found one person with a different NPI."
- **Impact.** 1 line(s), $4.14. Filed as is, the payment would be reported against an NPI that does not exist.
- **Evidence.**
    - EV1, registry_lookup(1144478386): NPI 1144478386: no registry record. Check digit not valid.
    - EV2, registry_search(MARIA A MARTIN): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name MARIA A MARTIN: / NPI 1144478686: MARIA ALEJANDRA MARTIN, PA-C | Physician Assistant, Medical | SOMERSWORTH NH | active | other names listed: none | differs from the NPI on the line in 1 of 10 digits
- **Recommendation.** Change the NPI on L03195 to 1144478686.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-050: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1023139250, date 2025-02-04, amount $5,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different, so no duplicate."
- **Impact.** 3 line(s), $17,550.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L00638,L00639,L00641): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L00638: document AP-25-000018 | accounts payable | loaded 2025-03-03 / L00639: document AP-25-000019 | accounts payable | loaded 2025-03-03 / L00641: document AP-25-000021 | accounts payable | loaded 2025-03-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-051: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1184981466, date 2025-12-04, amount $3,685.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different."
- **Impact.** 3 line(s), $11,055.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05599,L05600,L05602): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05599: document AP-25-000274 | accounts payable | loaded 2026-01-03 / L05600: document AP-25-000275 | accounts payable | loaded 2026-01-03 / L05602: document AP-25-000277 | accounts payable | loaded 2026-01-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-052: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1184981466, date 2025-12-18, amount $3,685.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different."
- **Impact.** 3 line(s), $11,055.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05845,L05847,L05849): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05845: document AP-25-000291 | accounts payable | loaded 2026-01-03 / L05847: document AP-25-000293 | accounts payable | loaded 2026-01-03 / L05849: document AP-25-000295 | accounts payable | loaded 2026-01-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-053: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1700825791, date 2025-05-28, amount $2,750.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents are different, so no duplicate."
- **Impact.** 3 line(s), $8,250.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02853,L02855,L02857): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02853: document AP-25-000121 | accounts payable | loaded 2025-06-03 / L02855: document AP-25-000123 | accounts payable | loaded 2025-06-03 / L02857: document AP-25-000125 | accounts payable | loaded 2025-06-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-054: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1700825791, date 2025-06-03, amount $2,750.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different."
- **Impact.** 3 line(s), $8,250.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02955,L02956,L02958): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02955: document AP-25-000134 | accounts payable | loaded 2025-07-03 / L02956: document AP-25-000135 | accounts payable | loaded 2025-07-03 / L02958: document AP-25-000137 | accounts payable | loaded 2025-07-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-055: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-01-14, amount $5,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $11,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L00253,L00254): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L00253: document AP-25-000007 | accounts payable | loaded 2025-02-03 / L00254: document AP-25-000008 | accounts payable | loaded 2025-02-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-056: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-03-04, amount $5,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $11,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01104,L01105): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01104: document AP-25-000038 | accounts payable | loaded 2025-04-03 / L01105: document AP-25-000039 | accounts payable | loaded 2025-04-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-057: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-03-18, amount $5,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different. No fix needed."
- **Impact.** 2 line(s), $11,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01383,L01384): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01383: document AP-25-000051 | accounts payable | loaded 2025-04-03 / L01384: document AP-25-000052 | accounts payable | loaded 2025-04-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-059: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1184981466, date 2025-04-29, amount $2,345.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different."
- **Impact.** 3 line(s), $7,035.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02286,L02287,L02289): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02286: document AP-25-000096 | accounts payable | loaded 2025-05-03 / L02287: document AP-25-000097 | accounts payable | loaded 2025-05-03 / L02289: document AP-25-000099 | accounts payable | loaded 2025-05-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-060: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1184981466, date 2025-08-12, amount $2,345.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different."
- **Impact.** 3 line(s), $7,035.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L03934,L03936,L03937): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L03934: document AP-25-000178 | accounts payable | loaded 2025-09-03 / L03936: document AP-25-000179 | accounts payable | loaded 2025-09-03 / L03937: document AP-25-000180 | accounts payable | loaded 2025-09-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-062: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-04-29, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $9,100.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02294,L02295): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02294: document AP-25-000101 | accounts payable | loaded 2025-05-03 / L02295: document AP-25-000102 | accounts payable | loaded 2025-05-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-063: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-08-27, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $9,100.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L04141,L04142): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L04141: document AP-25-000196 | accounts payable | loaded 2025-09-03 / L04142: document AP-25-000197 | accounts payable | loaded 2025-09-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-064: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-08-28, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $9,100.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L04163,L04164): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L04163: document AP-25-000198 | accounts payable | loaded 2025-09-03 / L04164: document AP-25-000199 | accounts payable | loaded 2025-09-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-065: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-11-06, amount $4,550.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different. No fix needed."
- **Impact.** 2 line(s), $9,100.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05194,L05195): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05194: document AP-25-000253 | accounts payable | loaded 2025-12-03 / L05195: document AP-25-000254 | accounts payable | loaded 2025-12-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-068: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1851513832 is on 1 ledger line(s) under the name CHAUNTELLE C CARTY. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found different name for NPI on line."
- **Impact.** 1 line(s), $123.10. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1851513832): NPI 1851513832: SUSAN CATHERINE CARTY, BS | Pharmacist | LONDONDERRY NH | active | other names listed: none
    - EV2, registry_search(CHAUNTELLE C CARTY): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name CHAUNTELLE C CARTY: / NPI 1437821899: CHAUNTELLE CLAUDINE CARTY | Nurse Practitioner, Psych/Mental Health | ANTRIM NH | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits
- **Recommendation.** Change the NPI on L02204 to 1437821899.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-069: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-03-11, amount $3,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01230,L01231): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01230: document AP-25-000041 | accounts payable | loaded 2025-04-03 / L01231: document AP-25-000042 | accounts payable | loaded 2025-04-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-070: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-04-07, amount $3,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01806,L01807): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01806: document AP-25-000076 | accounts payable | loaded 2025-05-03 / L01807: document AP-25-000077 | accounts payable | loaded 2025-05-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-071: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-04-11, amount $3,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01907,L01908): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01907: document AP-25-000082 | accounts payable | loaded 2025-05-03 / L01908: document AP-25-000083 | accounts payable | loaded 2025-05-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-072: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-05-12, amount $3,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02583,L02585): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02583: document AP-25-000109 | accounts payable | loaded 2025-06-03 / L02585: document AP-25-000111 | accounts payable | loaded 2025-06-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-073: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-05-28, amount $3,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02854,L02856): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02854: document AP-25-000122 | accounts payable | loaded 2025-06-03 / L02856: document AP-25-000124 | accounts payable | loaded 2025-06-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-074: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-12-18, amount $3,850.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,700.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05825,L05826): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05825: document AP-25-000285 | accounts payable | loaded 2026-01-03 / L05826: document AP-25-000286 | accounts payable | loaded 2026-01-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-075: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1184981466, date 2025-03-11, amount $3,685.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,370.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01241,L01243): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01241: document AP-25-000044 | accounts payable | loaded 2025-04-03 / L01243: document AP-25-000046 | accounts payable | loaded 2025-04-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-076: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1184981466, date 2025-07-17, amount $3,685.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,370.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L03576,L03577): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L03576: document AP-25-000162 | accounts payable | loaded 2025-08-03 / L03577: document AP-25-000163 | accounts payable | loaded 2025-08-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-077: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1184981466, date 2025-10-23, amount $3,685.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $7,370.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L04941,L04943): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L04941: document AP-25-000236 | accounts payable | loaded 2025-11-03 / L04943: document AP-25-000238 | accounts payable | loaded 2025-11-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-078: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1184981466, date 2025-12-18, amount $3,015.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $6,030.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05844,L05848): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05844: document AP-25-000290 | accounts payable | loaded 2026-01-03 / L05848: document AP-25-000294 | accounts payable | loaded 2026-01-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-079: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-04-11, amount $2,750.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different. No fix needed."
- **Impact.** 2 line(s), $5,500.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01909,L01910): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01909: document AP-25-000084 | accounts payable | loaded 2025-05-03 / L01910: document AP-25-000085 | accounts payable | loaded 2025-05-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-080: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-04-18, amount $2,750.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $5,500.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02080,L02081): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02080: document AP-25-000088 | accounts payable | loaded 2025-05-03 / L02081: document AP-25-000089 | accounts payable | loaded 2025-05-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-081: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-05-12, amount $2,750.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $5,500.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02584,L02586): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02584: document AP-25-000110 | accounts payable | loaded 2025-06-03 / L02586: document AP-25-000112 | accounts payable | loaded 2025-06-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-082: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1255694378 is on 2 ledger line(s) under the name MARIA T BOYLAN. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry NPI 1255694378 is under a different name and city."
- **Impact.** 2 line(s), $50.52. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1255694378): NPI 1255694378: MARIA THERESA BRALEY, D.O. | Family Medicine | BEDFORD NH | active | other names listed: none
    - EV2, registry_search(MARIA T BOYLAN): SEARCH FOUND NOBODY registered under the name MARIA T BOYLAN.
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-083: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1184981466, date 2025-02-27, amount $2,345.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines have different documents, so no duplicate."
- **Impact.** 2 line(s), $4,690.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L00998,L00999): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L00998: document AP-25-000028 | accounts payable | loaded 2025-03-03 / L00999: document AP-25-000029 | accounts payable | loaded 2025-03-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-084: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1184981466, date 2025-10-23, amount $2,345.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $4,690.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L04940,L04942): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L04940: document AP-25-000235 | accounts payable | loaded 2025-11-03 / L04942: document AP-25-000237 | accounts payable | loaded 2025-11-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-086: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1063058931, date 2025-12-04, amount $1,750.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines have different documents, so no duplicate."
- **Impact.** 2 line(s), $3,500.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05597,L05598): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05597: document AP-25-000272 | accounts payable | loaded 2026-01-03 / L05598: document AP-25-000273 | accounts payable | loaded 2026-01-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-088: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1063058931, date 2025-04-29, amount $1,250.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $2,500.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L02282,L02283): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L02282: document AP-25-000093 | accounts payable | loaded 2025-05-03 / L02283: document AP-25-000094 | accounts payable | loaded 2025-05-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-089: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1437111796 is on 1 ledger line(s) under the name JENNA E CLARK. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry NPI matches line NPI, but registry name differs. Ledger shows NPI 1457027583 is most used."
- **Impact.** 1 line(s), $34.97. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1437111796): NPI 1437111796: ELIZABETH C CLARK, M.D. | Internal Medicine, Infectious Disease | MERRIMACK NH | active | other names listed: none
    - EV3, ledger_history(JENNA E CLARK): Ledger lines under the name JENNA E CLARK: 3 lines carry NPI 1457027583; 1 line carries NPI 1437111796.
- **Recommendation.** Change the NPI on L03518 to 1457027583.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-090: Could not be confirmed. Sent to a person: failed the checks.

- **Condition.** NPI 1881714889 is on 1 ledger line(s) under the name PAUL F BELLIVEAU. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry NPI matches line NPI, but search found 2 people, none with 1-2 digit diff. Ledger shows line NPI is used."
- **Impact.** 1 line(s), $30.11. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1881714889): NPI 1881714889: NANCY A. BELLIVEAU, MA, CCC-SLP | Speech-Language Pathologist,   | BEDFORD NH | active | other names listed: none
    - EV2, registry_search(PAUL F BELLIVEAU): SEARCH FOUND 2 PEOPLE under the name PAUL F BELLIVEAU: / NPI 1164419974: PAUL PHILIP BELLIVEAU, PHARM.D., R.PH | Pharmacist, Pharmacotherapy | FITCHBURG MA | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits / NPI 1235232455: PAUL FREDERICK BELLIVEAU, M.D. | Psychiatry & Neurology, Psychiatry | EXETER NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
    - EV3, ledger_history(PAUL F BELLIVEAU): Ledger lines under the name PAUL F BELLIVEAU: 7 lines carry NPI 1235232455; 1 line carries NPI 1881714889.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-091: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1881298875 is on 1 ledger line(s) under the name ELIOT D FOLEY. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI but different name. Search found one person with different NPI."
- **Impact.** 1 line(s), $26.51. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1881298875): NPI 1881298875: MEGAN FOLEY | Occupational Therapy Assistant | CONCORD NH | active | other names listed: none
    - EV2, registry_search(ELIOT D FOLEY): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name ELIOT D FOLEY: / NPI 1528069424: ELIOT D FOLEY, MD | Ophthalmology, Retina Specialist | MANCHESTER NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L02123 to 1528069424.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-092: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1194758359 is on 1 ledger line(s) under the name KATHRYN L SCOVILLE. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry NPI found but no match in search; line NPI in registry ..."
- **Impact.** 1 line(s), $26.03. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1194758359): NPI 1194758359: KATHRYN LEAH CHILDERS, APRN | Nurse Practitioner, Family | CLARKSVILLE TN | active | other names listed: none
    - EV2, registry_search(KATHRYN L SCOVILLE): SEARCH FOUND NOBODY registered under the name KATHRYN L SCOVILLE.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-093: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1689613242 is on 1 ledger line(s) under the name JOAN E ROMBOLI. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI but different name. Search found one person with different NPI."
- **Impact.** 1 line(s), $25.63. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1689613242): NPI 1689613242: JOAN D SMITH, MD | Family Medicine | BARRINGTON NH | active | other names listed: none
    - EV2, registry_search(JOAN E ROMBOLI): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JOAN E ROMBOLI: / NPI 1134260607: JOAN ELLEN ROMBOLI, ARNP | Nurse Practitioner, Family | LONDONDERRY NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L02897 to 1134260607.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-094: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1265484000 is on 1 ledger line(s) under the name JODI F MARSHALL. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI but different name. Search found one person with different NPI."
- **Impact.** 1 line(s), $25.51. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1265484000): NPI 1265484000: SHARON A MARSHALL, M.D. | Radiology, Diagnostic Radiology | ROCHESTER NH | active | other names listed: none
    - EV2, registry_search(JODI F MARSHALL): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JODI F MARSHALL: / NPI 1710093174: JODI F MARSHALL, MD | type not listed | PORTSMOUTH NH | active | other names listed: JODI LEVERONE | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L03321 to 1710093174.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-095: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1265485056 is on 1 ledger line(s) under the name JAMES R KATES. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry has NPI 1265485056 under JAMES D POTTER, MD. Search found one person with different NPI. Case A: NPI_KEYED_WRONG."
- **Impact.** 1 line(s), $25.51. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1265485056): NPI 1265485056: JAMES D POTTER, MD | Family Medicine | JAFFREY NH | active | other names listed: none
    - EV2, registry_search(JAMES R KATES): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JAMES R KATES: / NPI 1760565600: JAMES R KATES, MD | Psychiatry & Neurology, Psychiatry | DOVER NH | active | other names listed: none | differs from the NPI on the line in 7 of 10 digits
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-096: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1750032801 is on 1 ledger line(s) under the name CLIVE E ROBERTSON. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI but different name. Search found one person with different NPI."
- **Impact.** 1 line(s), $24.96. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1750032801): NPI 1750032801: JANET ROBERTSON | Marriage & Family Therapist | KEENE NH | active | other names listed: none
    - EV2, registry_search(CLIVE E ROBERTSON): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name CLIVE E ROBERTSON: / NPI 1710655006: CLIVE E ROBERTSON, FNP-BC | Nurse Practitioner, Family | BEDFORD NH | active | other names listed: CLIVE TUCCERI | differs from the NPI on the line in 6 of 10 digits
- **Recommendation.** Change the NPI on L01272 to 1710655006.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-097: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1841931284 is on 1 ledger line(s) under the name SARA M DION. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI but different name. Search found one person with different NPI."
- **Impact.** 1 line(s), $24.88. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1841931284): NPI 1841931284: JESSICA LYNN DION | Behavior Technician | SWANZEY NH | active | other names listed: none
    - EV2, registry_search(SARA M DION): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name SARA M DION: / NPI 1154970093: SARA M DION, FNP | Nurse Practitioner, Family | ROCHESTER NH | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits
- **Recommendation.** Change the NPI on L01583 to 1154970093.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-098: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1184933657 is on 1 ledger line(s) under the name ALLISON M DILL. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry NPI found but no match in search; line NPI in registry."
- **Impact.** 1 line(s), $24.35. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1184933657): NPI 1184933657: ALLISON CASTONGUAY, APRN | Nurse Practitioner, Family | DURHAM NH | active | other names listed: none
    - EV2, registry_search(ALLISON M DILL): SEARCH FOUND NOBODY registered under the name ALLISON M DILL.
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-099: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1811081987 is on 1 ledger line(s) under the name TERESA W TRANCHEMONTAG. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry shows same first name and city as line, but no match found."
- **Impact.** 1 line(s), $22.56. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1811081987): NPI 1811081987: TERESA WHITE TRANCHEMONTAGNE, DO | Internal Medicine | AMHERST NH | active | other names listed: none
    - EV2, registry_search(TERESA W TRANCHEMONTAG): SEARCH FOUND NOBODY registered under the name TERESA W TRANCHEMONTAG.
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-100: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1255859757 is on 1 ledger line(s) under the name CAROLYN JAMIE KUSSMAUL. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry lookup found NPI 1255859757 under a different name. Registry search found no matches for the line's name."
- **Impact.** 1 line(s), $21.58. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1255859757): NPI 1255859757: CAROLYN JAMIE BIBA, PA | Physician Assistant | PORTSMOUTH NH | active | other names listed: none
    - EV2, registry_search(CAROLYN JAMIE KUSSMAUL): SEARCH FOUND NOBODY registered under the name CAROLYN JAMIE KUSSMAUL.
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-101: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1972283778 is on 1 ledger line(s) under the name EMMA KENNEY. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry NPI matches line NPI, same name and city."
- **Impact.** 1 line(s), $21.49. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1972283778): NPI 1972283778: EMMA MARIE BAR, FNP-BC | Nurse Practitioner, Family | SALEM NH | active | other names listed: none
    - EV3, registry_search(EMMA MARIE BAR): SEARCH FOUND ONLY THE NPI ALREADY ON THE LINE under the name EMMA MARIE BAR: / NPI 1972283778: EMMA MARIE BAR, FNP-BC | Nurse Practitioner, Family | SALEM NH | active | other names listed: none | SAME NPI AS THE LINE
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-102: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1093894875 is on 1 ledger line(s) under the name KATELYN AUSTIN HANSON. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry lookup found NPI 1093894875 is valid; search found a different NPI. Case A: WRONG_PERSON_SELECTED."
- **Impact.** 1 line(s), $20.96. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1093894875): NPI 1093894875: JEFFREY HANSON | Physical Therapist | CONWAY NH | active | other names listed: none
    - EV2, registry_search(KATELYN AUSTIN HANSON): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name KATELYN AUSTIN HANSON: / NPI 1861920209: KATELYN AUSTIN HANSON, DO | Internal Medicine | PORTSMOUTH NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L00666 to 1861920209.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-103: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1063292233 is on 1 ledger line(s) under the name LYDIA ANNE MCKENZIE. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry has NPI 1063292233 under different name, search found one person with different NPI."
- **Impact.** 1 line(s), $19.92. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1063292233): NPI 1063292233: RENATTO DIEAGO MCKENZIE, RN | Registered Nurse, General Practice | MANCHESTER NH | active | other names listed: none
    - EV2, registry_search(LYDIA ANNE MCKENZIE): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name LYDIA ANNE MCKENZIE: / NPI 1386129856: LYDIA ANNE MCKENZIE, DNP, PMHNP-BC | Nurse Practitioner, Psych/Mental Health | PLYMOUTH NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L02049 to 1386129856.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-104: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1811856685 is on 1 ledger line(s) under the name REBECCA E KRASNOF. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found different name for NPI on line. Search found one person with different NPI."
- **Impact.** 1 line(s), $18.75. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1811856685): NPI 1811856685: REBECCA M. WATTS | Marriage & Family Therapist | EXETER NH | active | other names listed: none
    - EV2, registry_search(REBECCA E KRASNOF): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name REBECCA E KRASNOF: / NPI 1831395011: REBECCA ERICKSON KRASNOF, M.D. | Family Medicine | WINDHAM NH | active | other names listed: none | differs from the NPI on the line in 7 of 10 digits
- **Recommendation.** Change the NPI on L03151 to 1831395011.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-105: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1518951250 is on 1 ledger line(s) under the name MELISSA KANTER. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI on line under different name. Search found one person with different NPI."
- **Impact.** 1 line(s), $18.45. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1518951250): NPI 1518951250: ALYSE K KANTER, MD | Obstetrics & Gynecology | NASHUA NH | active | other names listed: none
    - EV2, registry_search(MELISSA KANTER): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name MELISSA KANTER: / NPI 1265968515: MELISSA KANTER, APRN | Nurse Practitioner, Psych/Mental Health | CONWAY NH | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits
- **Recommendation.** Change the NPI on L03117 to 1265968515.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-106: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1467933598 is on 1 ledger line(s) under the name PAUL G DEGREGORIO. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found different name for NPI on line. Search found one person with different NPI."
- **Impact.** 1 line(s), $17.69. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1467933598): NPI 1467933598: JULIE DEGREGORIO | Counselor, Mental Health | LACONIA NH | active | other names listed: none
    - EV2, registry_search(PAUL G DEGREGORIO): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name PAUL G DEGREGORIO: / NPI 1508850827: PAUL G DEGREGORIO, M.D. | Ophthalmology, Retina Specialist | MANCHESTER NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L05483 to 1508850827.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-107: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1093305385 is on 1 ledger line(s) under the name AIMEE MURRAY. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI for line's name but different name. Search found one person with different NPI."
- **Impact.** 1 line(s), $16.44. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1093305385): NPI 1093305385: AIMEE Y TUCKER, MLADC | Counselor, Addiction (Substance Use Disorder) | NEW LONDON NH | active | other names listed: none
    - EV2, registry_search(AIMEE MURRAY): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name AIMEE MURRAY: / NPI 1669578571: AIMEE MURRAY, PA | Physician Assistant | WINDHAM NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L02809 to 1669578571.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-108: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1720013972 is on 1 ledger line(s) under the name PETER SIRAGUSA. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry lookup found NPI 1720013972 linked to Peter Kelley, PSY.D., but search found Peter Siragusa with different NPI. Case A: NPI keyed wrong."
- **Impact.** 1 line(s), $16.32. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1720013972): NPI 1720013972: PETER KELLEY, PSY.D. | Psychologist, Clinical | NASHUA NH | active | other names listed: none
    - EV2, registry_search(PETER SIRAGUSA): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name PETER SIRAGUSA: / NPI 1548007750: PETER SIRAGUSA | Registered Nurse, Psych/Mental Health | EXETER NH | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-109: Could not be confirmed. Sent to a person: the agent could not confirm.

- **Condition.** NPI 1659913028 is on 1 ledger line(s) under the name JENNIFER A PENN. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Could not be confirmed. Agent's explanation: "Registry has NPI 1659913028 under Stephen Sam Penn, PHARMD, but line's NPI is under Jennifer A Penn. Search found one person with different NPI. Case A: fix is that person's NPI."
- **Impact.** 1 line(s), $14.77. Unknown until a person reviews it. The lines stay open.
- **Evidence.**
    - EV1, registry_lookup(1659913028): NPI 1659913028: STEPHEN SAM PENN, PHARMD | Pharmacist | CONCORD NH | active | other names listed: none
    - EV2, registry_search(JENNIFER A PENN): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name JENNIFER A PENN: / NPI 1093153959: JENNIFER A. PENN, APRN | Nurse Practitioner, Psych/Mental Health | NASHUA NH | active | other names listed: JENNIFER PATEY | differs from the NPI on the line in 8 of 10 digits
    - EV3, ledger_history(JENNIFER A PENN): Ledger lines under the name JENNIFER A PENN: 18 lines carry NPI 1093153959; 1 line carries NPI 1659913028.
- **Recommendation.** Send to a person.
- **To confirm.** Who was paid, from the source document.

### E-110: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1528001377 is on 1 ledger line(s) under the name PHILIP J FINOCCHIARO. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found different name for NPI on line. Search found one person with different NPI."
- **Impact.** 1 line(s), $14.18. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1528001377): NPI 1528001377: CAROLYN FINOCCHIARO, NP | Nurse Practitioner | BEDFORD NH | active | other names listed: none
    - EV2, registry_search(PHILIP J FINOCCHIARO): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name PHILIP J FINOCCHIARO: / NPI 1538143730: PHILIP J FINOCCHIARO, M.D. | Internal Medicine | NASHUA NH | active | other names listed: none | differs from the NPI on the line in 7 of 10 digits
- **Recommendation.** Change the NPI on L04736 to 1538143730.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-111: Same person under another name. Proposed, waiting for approval.

- **Condition.** NPI 1750462669 is on 1 ledger line(s) under the name SARAH E SPOONER RIGGLES. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Same person under another name. Agent's explanation: "Registry shows same first name and city, type fits. Case B, no fix."
- **Impact.** 1 line(s), $14.16. The NPI is right. The name on file differs from the registry and may be questioned at submission.
- **Evidence.**
    - EV1, registry_lookup(1750462669): NPI 1750462669: SARAH ELIZABETH PROULX, RPA-C | Physician Assistant | STRATHAM NH | active | other names listed: SARAH RIGGLES
    - EV2, registry_search(SARAH E SPOONER RIGGLES): SEARCH FOUND ONLY THE NPI ALREADY ON THE LINE under the name SARAH E SPOONER RIGGLES: / NPI 1750462669: SARAH ELIZABETH PROULX, RPA-C | Physician Assistant | STRATHAM NH | active | other names listed: SARAH RIGGLES | SAME NPI AS THE LINE
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Whether the name on file should be updated to the registry name before submission.

### E-112: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1346763927 is on 1 ledger line(s) under the name LAURA ANDERSON. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry has NPI 1346763927 under different name, search found 2 people, ledger shows NPI 1174017024 is used more."
- **Impact.** 1 line(s), $13.00. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1346763927): NPI 1346763927: KERRY ANGELINE ANDERSON, APRN, FNP | Nurse Practitioner, Family | HAMPSTEAD NH | active | other names listed: none
    - EV2, registry_search(LAURA ANDERSON): SEARCH FOUND 2 PEOPLE under the name LAURA ANDERSON: / NPI 1942464458: LAURA ANDERSON, APRN | Nurse Practitioner, Family | CONCORD NH | active | other names listed: none | differs from the NPI on the line in 7 of 10 digits / NPI 1174017024: LAURA ANDERSON, PA | Physician Assistant | STRATHAM NH | active | other names listed: LAURA MENKE | differs from the NPI on the line in 8 of 10 digits
    - EV3, ledger_history(LAURA ANDERSON): Ledger lines under the name LAURA ANDERSON: 22 lines carry NPI 1174017024; 1 line carries NPI 1346763927.
- **Recommendation.** Change the NPI on L04557 to 1174017024.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-113: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1861920209 is on 1 ledger line(s) under the name KATELYN ISHERWOOD. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry found NPI on line, but name mismatch. Search found one person with different NPI."
- **Impact.** 1 line(s), $12.46. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1861920209): NPI 1861920209: KATELYN AUSTIN HANSON, DO | Internal Medicine | PORTSMOUTH NH | active | other names listed: none
    - EV2, registry_search(KATELYN ISHERWOOD): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name KATELYN ISHERWOOD: / NPI 1639890502: KATELYN ISHERWOOD | Family Medicine | DERRY NH | active | other names listed: none | differs from the NPI on the line in 7 of 10 digits
- **Recommendation.** Change the NPI on L01577 to 1639890502.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-114: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1962870899 is on 1 ledger line(s) under the name DIANA LI. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry NPI matches line NPI, but search found 2 people with NPIs differing by 7/10 and 8/10 digits. Ledger shows NPI 1396242871 is most used. Case C, fix_value 1396242871."
- **Impact.** 1 line(s), $11.83. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1962870899): NPI 1962870899: KRISTEN E LI, MED | Counselor, Mental Health | NASHUA NH | active | other names listed: none
    - EV2, registry_search(DIANA LI): SEARCH FOUND 2 PEOPLE under the name DIANA LI: / NPI 1265235089: DIANA HOPE LI, DO | Student in an Organized Health Care Education/Training Program | LEBANON NH | active | other names listed: none | differs from the NPI on the line in 7 of 10 digits / NPI 1396242871: DIANA LI, MD | Psychiatry & Neurology, Neurology | LEBANON NH | active | other names listed: none | differs from the NPI on the line in 8 of 10 digits
    - EV3, ledger_history(DIANA LI): Ledger lines under the name DIANA LI: 50 lines carry NPI 1396242871; 1 line carries NPI 1962870899.
- **Recommendation.** Change the NPI on L05423 to 1396242871.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-115: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-09-08, amount $305.32 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $610.64. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04233,L05900): TWO LINES SHARE A DOCUMENT NUMBER: L04233 and L05900 (document EXP-25-004033). / L04233: document EXP-25-004033 | expense reports | loaded 2025-10-03 / L05900: document EXP-25-004033 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05900.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-116: Wrong person selected. Proposed, waiting for approval.

- **Condition.** NPI 1568909125 is on 1 ledger line(s) under the name MOLLY B CHARTIER. The registry lists that NPI under a different name.
- **Criteria.** R-ID-02, rule file 2025.1: The recipient name on a line agrees with the name the NPI registry lists for the NPI on that line: same last name, and the same first name or initial. Another name the registry lists for the person also counts. (42 CFR 403.904(c)(1): the name must be as listed in the NPPES)
- **Cause.** Wrong person selected. Agent's explanation: "Registry has NPI 1568909125 under different name, search found one person with different NPI."
- **Impact.** 1 line(s), $7.92. Filed as is, the payment would be reported against another person.
- **Evidence.**
    - EV1, registry_lookup(1568909125): NPI 1568909125: BRITTONY CHARTIER, MSW | Social Worker, Clinical | CONCORD NH | active | other names listed: none
    - EV2, registry_search(MOLLY B CHARTIER): SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name MOLLY B CHARTIER: / NPI 1922245471: MOLLY BETH CHARTIER, M.D. | Dermatology | PORTSMOUTH NH | active | other names listed: none | differs from the NPI on the line in 9 of 10 digits
- **Recommendation.** Change the NPI on L02579 to 1922245471.
- **To confirm.** That the person the registry lists under the corrected NPI is the person who was paid.

### E-117: Separate payments. Proposed, waiting for approval.

- **Condition.** 4 ledger lines share NPI 1154327591, date 2025-03-26, amount $55.20 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All documents differ; separate payments."
- **Impact.** 4 line(s), $220.80. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01562,L01565,L01567,L01570): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01562: document AP-25-000062 | accounts payable | loaded 2025-04-03 / L01565: document AP-25-000065 | accounts payable | loaded 2025-04-03 / L01567: document AP-25-000067 | accounts payable | loaded 2025-04-03 / L01570: document AP-25-000070 | accounts payable | loaded 2025-04-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-118: Separate payments. Proposed, waiting for approval.

- **Condition.** 3 ledger lines share NPI 1154327591, date 2025-03-26, amount $88.50 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different."
- **Impact.** 3 line(s), $265.50. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L01564,L01568,L01569): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L01564: document AP-25-000064 | accounts payable | loaded 2025-04-03 / L01568: document AP-25-000068 | accounts payable | loaded 2025-04-03 / L01569: document AP-25-000069 | accounts payable | loaded 2025-04-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-119: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1578824959, date 2025-09-15, amount $145.30 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $290.60. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04333,L05895): TWO LINES SHARE A DOCUMENT NUMBER: L04333 and L05895 (document EXP-25-004129). / L04333: document EXP-25-004129 | expense reports | loaded 2025-10-03 / L05895: document EXP-25-004129 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05895.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-120: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1184981466, date 2025-06-08, amount $138.52 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $277.04. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03073,L05894): TWO LINES SHARE A DOCUMENT NUMBER: L03073 and L05894 (document EXP-25-002935). / L03073: document EXP-25-002935 | expense reports | loaded 2025-07-03 / L05894: document EXP-25-002935 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05894.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-121: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1891711156, date 2025-09-23, amount $103.43 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $206.86. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04476,L05893): TWO LINES SHARE A DOCUMENT NUMBER: L04476 and L05893 (document EXP-25-004268). / L04476: document EXP-25-004268 | expense reports | loaded 2025-10-03 / L05893: document EXP-25-004268 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05893.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-122: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1629333182, date 2025-06-24, amount $89.01 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $178.02. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03276,L05896): TWO LINES SHARE A DOCUMENT NUMBER: L03276 and L05896 (document EXP-25-003128). / L03276: document EXP-25-003128 | expense reports | loaded 2025-07-03 / L05896: document EXP-25-003128 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05896.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-123: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1346274941, date 2025-11-15, amount $59.46 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines have different documents, so no duplicate."
- **Impact.** 2 line(s), $118.92. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05378,L05379): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05378: document EXP-25-005114 | expense reports | loaded 2025-12-03 / L05379: document EXP-25-005115 | expense reports | loaded 2025-12-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-124: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1730599473, date 2025-06-02, amount $33.05 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $66.10. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L02937,L05902): TWO LINES SHARE A DOCUMENT NUMBER: L02937 and L05902 (document EXP-25-002805). / L02937: document EXP-25-002805 | expense reports | loaded 2025-07-03 / L05902: document EXP-25-002805 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05902.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-125: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1477707164, date 2025-06-25, amount $31.10 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document number, causing duplicate payment."
- **Impact.** 2 line(s), $62.20. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03291,L05897): TWO LINES SHARE A DOCUMENT NUMBER: L03291 and L05897 (document EXP-25-003141). / L03291: document EXP-25-003141 | expense reports | loaded 2025-07-03 / L05897: document EXP-25-003141 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05897.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-126: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1710971957, date 2025-06-13, amount $29.30 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $58.60. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03145,L05899): TWO LINES SHARE A DOCUMENT NUMBER: L03145 and L05899 (document EXP-25-003003). / L03145: document EXP-25-003003 | expense reports | loaded 2025-07-03 / L05899: document EXP-25-003003 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05899.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-127: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1598259947, date 2025-06-23, amount $28.11 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $56.22. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03251,L05889): TWO LINES SHARE A DOCUMENT NUMBER: L03251 and L05889 (document EXP-25-003107). / L03251: document EXP-25-003107 | expense reports | loaded 2025-07-03 / L05889: document EXP-25-003107 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05889.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-128: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1053762682, date 2025-09-25, amount $26.81 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document number, causing duplicate payment."
- **Impact.** 2 line(s), $53.62. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04527,L05907): TWO LINES SHARE A DOCUMENT NUMBER: L04527 and L05907 (document EXP-25-004307). / L04527: document EXP-25-004307 | expense reports | loaded 2025-10-03 / L05907: document EXP-25-004307 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05907.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-129: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1750510533, date 2025-09-26, amount $25.47 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $50.94. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04541,L05891): TWO LINES SHARE A DOCUMENT NUMBER: L04541 and L05891 (document EXP-25-004321). / L04541: document EXP-25-004321 | expense reports | loaded 2025-10-03 / L05891: document EXP-25-004321 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05891.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-130: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1346274941, date 2025-11-15, amount $24.77 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "All document numbers are different."
- **Impact.** 2 line(s), $49.54. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L05376,L05380): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L05376: document EXP-25-005112 | expense reports | loaded 2025-12-03 / L05380: document EXP-25-005116 | expense reports | loaded 2025-12-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-131: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1679093843, date 2025-06-02, amount $24.12 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $48.24. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L02936,L05904): TWO LINES SHARE A DOCUMENT NUMBER: L02936 and L05904 (document EXP-25-002804). / L02936: document EXP-25-002804 | expense reports | loaded 2025-07-03 / L05904: document EXP-25-002804 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05904.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-132: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1043673379, date 2025-06-03, amount $23.24 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $46.48. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L02962,L05892): TWO LINES SHARE A DOCUMENT NUMBER: L02962 and L05892 (document EXP-25-002825). / L02962: document EXP-25-002825 | expense reports | loaded 2025-07-03 / L05892: document EXP-25-002825 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05892.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-133: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1023139250, date 2025-09-17, amount $22.64 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $45.28. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04398,L05886): TWO LINES SHARE A DOCUMENT NUMBER: L04398 and L05886 (document EXP-25-004192). / L04398: document EXP-25-004192 | expense reports | loaded 2025-10-03 / L05886: document EXP-25-004192 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05886.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-134: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1780892836, date 2025-06-13, amount $21.46 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $42.92. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03149,L05898): TWO LINES SHARE A DOCUMENT NUMBER: L03149 and L05898 (document EXP-25-003007). / L03149: document EXP-25-003007 | expense reports | loaded 2025-07-03 / L05898: document EXP-25-003007 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05898.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-136: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1346683240, date 2025-09-03, amount $20.47 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $40.94. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04191,L05906): TWO LINES SHARE A DOCUMENT NUMBER: L04191 and L05906 (document EXP-25-003991). / L04191: document EXP-25-003991 | expense reports | loaded 2025-10-03 / L05906: document EXP-25-003991 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05906.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-137: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1235566324, date 2025-06-16, amount $15.59 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $31.18. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03175,L05888): TWO LINES SHARE A DOCUMENT NUMBER: L03175 and L05888 (document EXP-25-003033). / L03175: document EXP-25-003033 | expense reports | loaded 2025-07-03 / L05888: document EXP-25-003033 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05888.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-138: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1346683240, date 2025-06-05, amount $15.00 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two lines share same NPI and date but different documents."
- **Impact.** 2 line(s), $30.00. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L03007,L03013): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L03007: document EXP-25-002869 | expense reports | loaded 2025-07-03 / L03013: document EXP-25-002875 | expense reports | loaded 2025-07-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-139: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1790446045, date 2025-09-23, amount $14.17 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $28.34. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04475,L05905): TWO LINES SHARE A DOCUMENT NUMBER: L04475 and L05905 (document EXP-25-004267). / L04475: document EXP-25-004267 | expense reports | loaded 2025-10-03 / L05905: document EXP-25-004267 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05905.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-140: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1700825791, date 2025-09-09, amount $12.94 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $25.88. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04260,L05887): TWO LINES SHARE A DOCUMENT NUMBER: L04260 and L05887 (document EXP-25-004058). / L04260: document EXP-25-004058 | expense reports | loaded 2025-10-03 / L05887: document EXP-25-004058 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05887.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-143: Separate payments. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1013432251, date 2025-08-01, amount $9.65 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Separate payments. Agent's explanation: "Two separate payments with different documents."
- **Impact.** 2 line(s), $19.30. None. The lines are separate payments.
- **Evidence.**
    - EV1, source_documents(L03803,L03804): ALL DOCUMENT NUMBERS ARE DIFFERENT. / L03803: document EXP-25-003630 | expense reports | loaded 2025-09-03 / L03804: document EXP-25-003631 | expense reports | loaded 2025-09-03
- **Recommendation.** No change. Record the reason in the accepted register so the exception does not come back.
- **To confirm.** Nothing further.

### E-144: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1124656335, date 2025-06-03, amount $9.41 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $18.82. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L02970,L05890): TWO LINES SHARE A DOCUMENT NUMBER: L02970 and L05890 (document EXP-25-002833). / L02970: document EXP-25-002833 | expense reports | loaded 2025-07-03 / L05890: document EXP-25-002833 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05890.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-160: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1346683240, date 2025-09-24, amount $5.10 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document, causing duplicate payment."
- **Impact.** 2 line(s), $10.20. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L04491,L05901): TWO LINES SHARE A DOCUMENT NUMBER: L04491 and L05901 (document EXP-25-004283). / L04491: document EXP-25-004283 | expense reports | loaded 2025-10-03 / L05901: document EXP-25-004283 | expense reports | loaded 2025-10-17
- **Recommendation.** Remove line L05901.
- **To confirm.** That the document was paid once, before the second line is removed.

### E-164: Document loaded twice. Proposed, waiting for approval.

- **Condition.** 2 ledger lines share NPI 1558725861, date 2025-06-24, amount $2.25 and nature of payment.
- **Criteria.** R-DUP-01, rule file 2025.1: Two or more lines with the same NPI, payment date, amount and nature of payment are confirmed as separate payments before filing. (Internal control. Each payment is reported once (42 CFR 403.904(a)).)
- **Cause.** Document loaded twice. Agent's explanation: "Two lines share the same document number, causing duplicate payment."
- **Impact.** 2 line(s), $4.50. Filed as is, the same payment would be reported twice.
- **Evidence.**
    - EV1, source_documents(L03273,L05903): TWO LINES SHARE A DOCUMENT NUMBER: L03273 and L05903 (document EXP-25-003125). / L03273: document EXP-25-003125 | expense reports | loaded 2025-07-03 / L05903: document EXP-25-003125 | expense reports | loaded 2025-07-17
- **Recommendation.** Remove line L05903.
- **To confirm.** That the document was paid once, before the second line is removed.
