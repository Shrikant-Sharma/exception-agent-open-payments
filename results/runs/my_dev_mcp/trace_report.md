# Step 11. Traces of run 'my_dev_mcp'

Model: Qwen3-4B-Q4_K_M.gguf. Lookups: mcp. Read back from MLflow experiment `exception-agent`.

A trace is one exception from start to finish. A span is one step inside it: the exception as a whole (the root span), one model call, or one lookup.

- **35 traces for 35 exceptions**, 226 spans in all. A trace holds 5 spans at the median and 12 at most.
- **35 of 35 traces agree with the run's own record** in the number of model calls, the lookups in order, the tokens in and out, and the outcome.
- **Where the time goes.** Model calls took 943 of the 943 seconds, and the 55 lookups 0.2 seconds together. An exception takes 25 seconds at the median and 74 at most.

| Kind of span | Spans | Seconds in all | Tokens in | Tokens out |
|---|---|---|---|---|
| Exception (root) | 35 | 943.1 | | |
| Model call | 136 | 942.8 | 122,604 | 4,598 |
| Lookup | 55 | 0.20 | | |

## One trace, step by step

Checks on its conclusions, in order: FAILED: same_first_name is yes: the line says ELIZABETH, the registry says ELIZABETH; passed.

```
E-002   AGENT   59.1 s   -> {"status": "proposed", "reason": "passed the checks", "root_cause": "SAME_PERSON_OTHER_NAME",...
  model call        CHAT_MODEL     5.5 s   760 tokens in, 22 out   -> {"lookup": "registry_lookup", "input": "1700079118"}
  registry_lookup   TOOL           3.6 ms  1700079118   -> NPI 1700079118: ELIZABETH MARIE SILVESTRI, PA-C | Physician Assistant, Medical | SALEM NH | a...
  model call        CHAT_MODEL     4.2 s   870 tokens in, 20 out   -> {"lookup": "registry_search", "input": "ELIZABETH M GEMBA"}
  registry_search   TOOL           3.4 ms  ELIZABETH M GEMBA   -> SEARCH FOUND NOBODY registered under the name ELIZABETH M GEMBA.
  model call        CHAT_MODEL     2.5 s   948 tokens in, 12 out   -> {"lookup": "conclude", "input": ""}
  model call        CHAT_MODEL    17.7 s   1,121 tokens in, 102 out   -> {"explanation": "Registry lookup found NPI 1700079118 is registered under a different name. R...
  model call        CHAT_MODEL     3.7 s   1,200 tokens in, 16 out   -> {"lookup": "registry_search", "input": "ELIZABETH"}
  registry_search   TOOL           3.0 ms  ELIZABETH   -> Input must be a first and last name.
  model call        CHAT_MODEL     2.3 s   1,269 tokens in, 12 out   -> {"lookup": "conclude", "input": ""}
  model call        CHAT_MODEL    23.3 s   1,454 tokens in, 132 out   -> {"explanation": "Registry lists NPI 1700079118 under ELIZABETH MARIE SILVESTRI, PA-C. Line na...
```

## What the traces are for

- To answer, for any one exception, what the model was sent, what it replied, which lookups ran and what they returned, and how long each step took.
- To see cost and time by step. Tokens are counted on each model call, so a run's bill can be worked out from its traces.
- They are a record, not a check. Whether a conclusion is right is decided by the code checks and the scoring in step 6.
