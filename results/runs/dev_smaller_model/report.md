# Agent run 'dev_smaller_model': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: qwen2.5-1.5b-instruct-q4_k_m.gguf (local file, llama-cpp-python). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0.

**19 of 35 right (54.3%; 95% interval 38.2 to 69.5). 16 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 6 | 1 | 5 | 0 |
| Wrong person selected (planted) | 6 | 0 | 6 | 0 |
| No safe correction exists (planted) | 2 | 2 | 0 | 0 |
| Name differs from registry (as published) | 3 | 1 | 2 | 0 |
| Document loaded twice (planted) | 6 | 3 | 3 | 0 |
| Look-alike payments (as published) | 12 | 12 | 0 | 0 |
| **All** | **35** | **19** | **16** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 2 of 35 exceptions.
- The checks sent 25 first conclusions back. 22 proposed a fix or a close that did not match the answer key. The other 3 stated a fact or the case of the procedure wrong; 2 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 17 of the 25 ended right, 8 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 29 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 16. By a hand-off on the first conclusion: 8. By a hand-off after an earlier conclusion was sent back: 3. After failing the checks on every try: 5. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 10, 2 lookups in 24, 4 lookups in 1.
- Median 43.2 seconds per exception; 24 minutes of model time in all; 211,761 tokens read, 8,567 written.
- Recipient exceptions, lookup paths used: registry_lookup (10); registry_lookup > registry_search (6); registry_lookup > registry_search > ledger_history > source_documents (1).
- Look-alike exceptions, lookup paths used: registry_lookup > source_documents (18).

## Every exception that did not end right

| Exception | Kind | Answer key | Result | How it ended | First problem the checks found |
|---|---|---|---|---|---|
| E-002 | Name differs from registry (as published) | NO_CHANGE | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | line_npi_in_registry is yes: the registry has a record for the NPI on the line |
| E-021 | NPI typed wrong (planted) | FIX_NPI 1912107285 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-026 | NPI typed wrong (planted) | FIX_NPI 1104370154 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-028 | NPI typed wrong (planted) | FIX_NPI 1962429837 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | the fix is not a different ten-digit NPI |
| E-030 | NPI typed wrong (planted) | FIX_NPI 1952885394 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-035 | NPI typed wrong (planted) | FIX_NPI 1366553398 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-091 | Wrong person selected (planted) | FIX_NPI 1528069424 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-096 | Wrong person selected (planted) | FIX_NPI 1710655006 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 2 conclusions were sent back | the registry was not searched for the name on the line (run registry_search with it) |
| E-101 | Name differs from registry (as published) | NO_CHANGE | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | the registry was not searched for the name on the line (run registry_search with it) |
| E-106 | Wrong person selected (planted) | FIX_NPI 1508850827 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 1 conclusion was sent back | the search result is case A of the procedure, not case B |
| E-107 | Wrong person selected (planted) | FIX_NPI 1669578571 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-114 | Wrong person selected (planted) | FIX_NPI 1396242871 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-116 | Wrong person selected (planted) | FIX_NPI 1922245471 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-131 | Document loaded twice (planted) | REMOVE_LINE L05904 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | source documents were not retrieved for L02936, L05904 (run source_documents with those line IDs) |
| E-133 | Document loaded twice (planted) | REMOVE_LINE L05886 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 2 conclusions were sent back | source documents were not retrieved for L04398, L05886 (run source_documents with those line IDs) |
| E-139 | Document loaded twice (planted) | REMOVE_LINE L05905 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | source documents were not retrieved for L04475, L05905 (run source_documents with those line IDs) |
