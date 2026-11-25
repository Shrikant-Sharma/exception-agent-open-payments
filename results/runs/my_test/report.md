# Agent run 'my_test': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: Qwen3-4B-Q4_K_M.gguf (local file, llama-cpp-python). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0.

**86 of 95 right (90.5%; 95% interval 83.0 to 94.9). 9 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 16 | 13 | 3 | 0 |
| Wrong person selected (planted) | 16 | 11 | 5 | 0 |
| No safe correction exists (planted) | 4 | 4 | 0 | 0 |
| Name differs from registry (as published) | 9 | 8 | 1 | 0 |
| NPI not in registry (as published) | 1 | 1 | 0 | 0 |
| Document loaded twice (planted) | 16 | 16 | 0 | 0 |
| Look-alike payments (as published) | 33 | 33 | 0 | 0 |
| **All** | **95** | **86** | **9** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 72 of 95 exceptions.
- The checks sent 20 first conclusions back. 2 proposed a fix or a close that did not match the answer key. The other 18 stated a fact or the case of the procedure wrong; 16 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 14 of the 20 ended right, 6 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 8 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 9. By a hand-off on the first conclusion: 3. By a hand-off after an earlier conclusion was sent back: 4. After failing the checks on every try: 2. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 49, 2 lookups in 40, 3 lookups in 4, 4 lookups in 2.
- Median 24.6 seconds per exception; 49 minutes of model time in all; 390,634 tokens read, 14,318 written.
- Recipient exceptions, lookup paths used: registry_lookup > registry_search (40); registry_lookup > registry_search > ledger_history (3); registry_lookup > registry_search > registry_lookup > registry_lookup (1); registry_lookup > registry_search > registry_search (1); registry_lookup > registry_search > ledger_history > source_documents (1).
- Look-alike exceptions, lookup paths used: source_documents (49).

## Every exception that did not end right

| Exception | Kind | Answer key | Result | How it ended | First problem the checks found |
|---|---|---|---|---|---|
| E-018 | NPI typed wrong (planted) | FIX_NPI 1538486717 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 1 conclusion was sent back | the search result is case C of the procedure, not case B |
| E-032 | NPI typed wrong (planted) | FIX_NPI 1821821919 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-033 | NPI typed wrong (planted) | FIX_NPI 1780924001 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-082 | Name differs from registry (as published) | NO_CHANGE | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 2 conclusions were sent back | same_first_name is yes: the line says MARIA, the registry says MARIA |
| E-090 | Wrong person selected (planted) | FIX_NPI 1235232455 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | the search result is case C of the procedure, not case B |
| E-095 | Wrong person selected (planted) | FIX_NPI 1760565600 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 2 conclusions were sent back | line_npi_in_registry is yes: the registry has a record for the NPI on the line |
| E-097 | Wrong person selected (planted) | FIX_NPI 1154970093 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 1 conclusion was sent back | line_npi_in_registry is yes: the registry has a record for the NPI on the line |
| E-108 | Wrong person selected (planted) | FIX_NPI 1548007750 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-112 | Wrong person selected (planted) | FIX_NPI 1174017024 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | line_npi_in_registry is yes: the registry has a record for the NPI on the line | the procedure, case A: the cause is NPI_KEYED_WRONG when the NPI on the line has no registry record, and WRONG_PERSON_SELECTED when it has one. Your cause does not agree with the registry |
