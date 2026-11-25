# Agent run 'hosted_bedrock_gpt_oss_120b_dev': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: openai.gpt-oss-120b-1:0 (endpoint https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0.

**35 of 35 right (100.0%; 95% interval 90.1 to 100.0). 0 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 6 | 6 | 0 | 0 |
| Wrong person selected (planted) | 6 | 6 | 0 | 0 |
| No safe correction exists (planted) | 2 | 2 | 0 | 0 |
| Name differs from registry (as published) | 3 | 3 | 0 | 0 |
| Document loaded twice (planted) | 6 | 6 | 0 | 0 |
| Look-alike payments (as published) | 12 | 12 | 0 | 0 |
| **All** | **35** | **35** | **0** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 35 of 35 exceptions.
- The checks sent 0 first conclusions back. 0 proposed a fix or a close that did not match the answer key. The other 0 stated a fact or the case of the procedure wrong; 0 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 0 of the 0 ended right, 0 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 0 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 0. By a hand-off on the first conclusion: 0. By a hand-off after an earlier conclusion was sent back: 0. After failing the checks on every try: 0. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 18, 2 lookups in 16, 3 lookups in 1.
- Median 6.1 seconds per exception; 4 minutes of model time in all; 108,719 tokens read, 27,770 written.
- Recipient exceptions, lookup paths used: registry_lookup > registry_search (16); registry_lookup > registry_search > ledger_history (1).
- Look-alike exceptions, lookup paths used: source_documents (18).
