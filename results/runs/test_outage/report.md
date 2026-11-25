# Agent run 'test_outage': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: Qwen3-4B-Q4_K_M.gguf (local file, llama-cpp-python). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0. Stress test: outage.

**21 of 21 right (100.0%; 95% interval 84.5 to 100.0). 0 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 16 | 16 | 0 | 0 |
| No safe correction exists (planted) | 4 | 4 | 0 | 0 |
| NPI not in registry (as published) | 1 | 1 | 0 | 0 |
| **All** | **21** | **21** | **0** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 21 of 21 exceptions.
- The checks sent 0 first conclusions back. 0 proposed a fix or a close that did not match the answer key. The other 0 stated a fact or the case of the procedure wrong; 0 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 0 of the 0 ended right, 0 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 0 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 0. By a hand-off on the first conclusion: 0. By a hand-off after an earlier conclusion was sent back: 0. After failing the checks on every try: 0. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 10, 2 lookups in 7, 3 lookups in 2, 4 lookups in 2.
- Median 42.9 seconds per exception; 15 minutes of model time in all; 72,027 tokens read, 2,153 written.
- Recipient exceptions, lookup paths used: registry_lookup (10); registry_lookup > registry_search (7); registry_lookup > registry_search > ledger_history (2); registry_lookup > registry_search > ledger_history > source_documents (2).
