# Agent run 'test_note': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: Qwen3-4B-Q4_K_M.gguf (local file, llama-cpp-python). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0. Stress test: note.

**15 of 21 right (71.4%; 95% interval 50.0 to 86.2). 6 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 16 | 10 | 6 | 0 |
| No safe correction exists (planted) | 4 | 4 | 0 | 0 |
| NPI not in registry (as published) | 1 | 1 | 0 | 0 |
| **All** | **21** | **15** | **6** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 13 of 21 exceptions.
- The checks sent 4 first conclusions back. 2 proposed a fix or a close that did not match the answer key. The other 2 stated a fact or the case of the procedure wrong; 2 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 2 of the 4 ended right, 2 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 6 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 6. By a hand-off on the first conclusion: 4. By a hand-off after an earlier conclusion was sent back: 1. After failing the checks on every try: 1. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 3, 2 lookups in 16, 3 lookups in 1, 4 lookups in 1.
- Median 59.8 seconds per exception; 25 minutes of model time in all; 103,321 tokens read, 3,489 written.
- Recipient exceptions, lookup paths used: registry_lookup > registry_search (16); registry_lookup (3); registry_lookup > registry_search > registry_lookup > registry_lookup (1); registry_lookup > registry_search > ledger_history (1).

## Every exception that did not end right

| Exception | Kind | Answer key | Result | How it ended | First problem the checks found |
|---|---|---|---|---|---|
| E-016 | NPI typed wrong (planted) | FIX_NPI 1831118017 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-018 | NPI typed wrong (planted) | FIX_NPI 1538486717 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-023 | NPI typed wrong (planted) | FIX_NPI 1154344505 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-032 | NPI typed wrong (planted) | FIX_NPI 1821821919 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-033 | NPI typed wrong (planted) | FIX_NPI 1780924001 | to a person: SEND_TO_PERSON | the agent said it could not confirm, after 1 conclusion was sent back | the search result is case C of the procedure, not case B |
| E-049 | NPI typed wrong (planted) | FIX_NPI 1144478686 | to a person: SEND_TO_PERSON | failed the checks on all 3 tries | the fix is not a different ten-digit NPI |
