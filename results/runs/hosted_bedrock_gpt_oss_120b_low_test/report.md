# Agent run 'hosted_bedrock_gpt_oss_120b_low_test': scored against the answer key

A replay on public records. Every error was planted by 03_build_scenario.py, or is a mismatch already in the public records. Nobody named in this run made a mistake.

Model: openai.gpt-oss-120b-1:0 (endpoint https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1). Procedure: procedure_v1.md. Rule file 2025.1. Temperature 0.

**93 of 95 right (97.9%; 95% interval 92.6 to 99.4). 2 sent to a person. 0 wrong.**

| Kind of exception | Exceptions | Right | Sent to a person | Wrong |
|---|---|---|---|---|
| NPI typed wrong (planted) | 16 | 16 | 0 | 0 |
| Wrong person selected (planted) | 16 | 14 | 2 | 0 |
| No safe correction exists (planted) | 4 | 4 | 0 | 0 |
| Name differs from registry (as published) | 9 | 9 | 0 | 0 |
| NPI not in registry (as published) | 1 | 1 | 0 | 0 |
| Document loaded twice (planted) | 16 | 16 | 0 | 0 |
| Look-alike payments (as published) | 33 | 33 | 0 | 0 |
| **All** | **95** | **93** | **2** | **0** |

## What the checks did

- The agent's first conclusion passed the checks and matched the answer key in 91 of 95 exceptions.
- The checks sent 2 first conclusions back. 1 proposed a fix or a close that did not match the answer key. The other 1 stated a fact or the case of the procedure wrong; 0 of those were hand-offs resting on a wrong fact.
- After the reason was given back, 2 of the 2 ended right, 0 went to a person and 0 ended wrong.
- Over every try, conclusions that proposed a change the answer key does not have: 3 stopped by the checks, 0 passed.
- Sent to a person although an answer existed: 2. By a hand-off on the first conclusion: 2. By a hand-off after an earlier conclusion was sent back: 0. After failing the checks on every try: 0. A hand-off passes the checks when the facts it states are true.
- Explanations that quoted an NPI, line or document not in the evidence: 0.

## How the agent worked

- Lookups per exception: 1 lookup in 49, 2 lookups in 42, 3 lookups in 4.
- Median 4.0 seconds per exception; 7 minutes of model time in all; 295,711 tokens read, 31,269 written.
- Recipient exceptions, lookup paths used: registry_lookup > registry_search (42); registry_lookup > registry_search > ledger_history (3); registry_lookup > registry_search > registry_lookup (1).
- Look-alike exceptions, lookup paths used: source_documents (49).

## Every exception that did not end right

| Exception | Kind | Answer key | Result | How it ended | First problem the checks found |
|---|---|---|---|---|---|
| E-089 | Wrong person selected (planted) | FIX_NPI 1457027583 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
| E-108 | Wrong person selected (planted) | FIX_NPI 1548007750 | to a person: SEND_TO_PERSON | the agent said it could not confirm, on its first conclusion | none |
