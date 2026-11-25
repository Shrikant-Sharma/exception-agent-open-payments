# Agent run 'my_small_dev': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: qwen2.5-1.5b-instruct-q4_k_m.gguf (local file, llama-cpp-python). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0.

**18 of 35 right (51.4%; 95% interval 35.6 to 67.0). 17 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 6 | 0 | 6 | 0 |
| Wrong person selected (planted) | 6 | 0 | 6 | 0 |
| No safe correction exists (planted) | 2 | 2 | 0 | 0 |
| Name differs from registry (as published) | 3 | 1 | 2 | 0 |
| Document loaded twice (planted) | 6 | 3 | 3 | 0 |
| Look-alike payments (as published) | 12 | 12 | 0 | 0 |
| **All** | **35** | **18** | **17** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 2 of 35 exceptions.
- The checks sent 23 first conclusions back. 21 proposed a fix or a close that did not match the answer key. The other 2 stated a fact or the case of the procedure wrong; 2 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 16 of the 23 ended right, 7 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 29 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 17. By a hand-off on the first conclusion: 10. By a hand-off after an earlier conclusion was sent back: 1. After failing the checks on every try: 6. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 11, 2 lookups in 21, 3 lookups in 2, 4 lookups in 1.
- Median 25.0 seconds per exception; 15 minutes of model time in all; 210,438 tokens read, 8,204 written.
- Recipient exceptions, lookup paths used: registry_lookup (11); registry_lookup > registry_search (3); registry_lookup > registry_search > registry_lookup (2); registry_lookup > registry_search > ledger_history > source_documents (1).
- Look-alike exceptions, lookup paths used: registry_lookup > source_documents (18).

## Every exception that did not end right

| Exception | Kind | Answer key | Result | How it ended | First problem the checks found |
|---|---|---|---|---|---|
| E-002 | Name differs from registry (as published) | NO_CHANGE | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | line_npi_in_registry is yes: the registry has a record for the NPI on the line |
| E-013 | NPI typed wrong (planted) | FIX_NPI 1568622801 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-021 | NPI typed wrong (planted) | FIX_NPI 1912107285 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-026 | NPI typed wrong (planted) | FIX_NPI 1104370154 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-028 | NPI typed wrong (planted) | FIX_NPI 1962429837 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | the fix is not a different ten-digit NPI |
| E-030 | NPI typed wrong (planted) | FIX_NPI 1952885394 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-035 | NPI typed wrong (planted) | FIX_NPI 1366553398 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-091 | Wrong person selected (planted) | FIX_NPI 1528069424 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-096 | Wrong person selected (planted) | FIX_NPI 1710655006 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | the registry was not searched for the name on the line (run registry_search with it) |
| E-101 | Name differs from registry (as published) | NO_CHANGE | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-106 | Wrong person selected (planted) | FIX_NPI 1508850827 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 1 conclusion was sent back | the search result is case A of the procedure, not case B |
| E-107 | Wrong person selected (planted) | FIX_NPI 1669578571 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-114 | Wrong person selected (planted) | FIX_NPI 1396242871 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-116 | Wrong person selected (planted) | FIX_NPI 1922245471 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-125 | Document loaded twice (planted) | REMOVE_LINE L05897 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | source documents were not retrieved for L03291, L05897 (run source_documents with those line IDs) |
| E-128 | Document loaded twice (planted) | REMOVE_LINE L05907 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | source documents were not retrieved for L04527, L05907 (run source_documents with those line IDs) |
| E-133 | Document loaded twice (planted) | REMOVE_LINE L05886 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | source documents were not retrieved for L04398, L05886 (run source_documents with those line IDs) |
