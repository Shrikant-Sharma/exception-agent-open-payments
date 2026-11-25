# Agent run 'test_recheck_after_hardening': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: Qwen3-4B-Q4_K_M.gguf (local file, llama-cpp-python). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0.

**9 of 12 right (75.0%; 95% interval 46.8 to 91.1). 3 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 3 | 2 | 1 | 0 |
| Wrong person selected (planted) | 3 | 2 | 1 | 0 |
| No safe correction exists (planted) | 1 | 1 | 0 | 0 |
| Name differs from registry (as published) | 2 | 1 | 1 | 0 |
| Document loaded twice (planted) | 1 | 1 | 0 | 0 |
| Look-alike payments (as published) | 2 | 2 | 0 | 0 |
| **All** | **12** | **9** | **3** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 4 of 12 exceptions.
- The checks sent 7 first conclusions back. 1 proposed a fix or a close that did not match the answer key. The other 6 stated a fact or the case of the procedure wrong; 4 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 5 of the 7 ended right, 2 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 6 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 3. By a hand-off on the first conclusion: 1. By a hand-off after an earlier conclusion was sent back: 1. After failing the checks on every try: 1. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 3, 2 lookups in 4, 3 lookups in 4, 4 lookups in 1.
- Median 114.8 seconds per exception; 22 minutes of model time in all; 80,970 tokens read, 2,775 written.
- Recipient exceptions, lookup paths used: registry_lookup > registry_search (4); registry_lookup > registry_search > ledger_history (3); registry_lookup > registry_search > registry_search (1); registry_lookup > registry_search > registry_lookup > registry_search (1).
- Look-alike exceptions, lookup paths used: source_documents (3).

## Every exception that did not end right

| Exception | Kind | Answer key | Result | How it ended | First problem the checks found |
|---|---|---|---|---|---|
| E-032 | NPI typed wrong (planted) | FIX_NPI 1821821919 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-090 | Wrong person selected (planted) | FIX_NPI 1235232455 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | the search result is case C of the procedure, not case B |
| E-092 | Name differs from registry (as published) | NO_CHANGE | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 1 conclusion was sent back | same_first_name is yes: the line says KATHRYN, the registry says KATHRYN |
