# Development log

How the agent's procedure, lookups and checks were developed, and what each
round changed. Only the 35 development exceptions were used for this. The 95
test exceptions were not run until everything was frozen.

| Round | What was run | What happened | What changed next |
|---|---|---|---|
| 1 | 6 development exceptions, Qwen2.5 1.5B. Each step carried a written reason. | The model repeated lookups it had already run and did not conclude. It took the registry path on a look-alike exception. About 50 seconds per exception. | Moved to a 4B model. Added a section to the procedure on how to reply. A repeated lookup now gets a reminder, and a second repeat forces a conclusion. |
| 2 | 8 development exceptions, Qwen3 4B, same loop. Stopped after 4. | It followed the lookup order. It then made up an NPI to look up, mistook a name difference for a typed-wrong NPI, and slipped into Chinese mid-sentence. 58 to 163 seconds per exception, most of it spent writing reasons at about 3.6 tokens a second. | A step is now only the lookup and its input; the reason is given once, at the conclusion, before the cause is named. Search results got a one-line header that says what was found. The model is handed only the procedure for the kind of exception in front of it. Failed-check messages now say which lookup to run. Added an English-only check. Switched the model to its direct-answer mode. |
| 3 | The same 8 exceptions. | 6 of 8 ended right, 2 went to a person, 0 wrong. A made-up NPI in the free-text "to confirm" note failed a check, and the retry repeated the same text. On a same-name case the model skipped the tie-break lookup. Look-alike cases ran lookups they did not need. About 50 to 60 seconds per exception. | Dropped the model's "to confirm" note; code writes that line from facts. Made the tie-break lookup its own step. Told the model a look-alike needs one lookup. The agent must now name which case of the procedure applies, and code checks that claim against the search result. A retry is told not to repeat the failed answer. Up to two retries. |
| 4 | All 35 development exceptions. Stopped after 21. | 16 of 21 right, 5 to a person, 0 wrong. On 4 look-alike pairs the model called separate documents a double load, the check stopped it, and each retry repeated the same answer. On a name difference it sent a clear same-person case to a person. | Document results got a header that says whether two lines share a document. A failed answer is now taken out of the conversation so it cannot be copied. For a name difference the agent answers three yes or no questions (same first name, same city, type fits); code checks the first two because they are facts. |
| 5 | All 35 development exceptions. Stopped after 24. | 22 of 24 right, 2 to a person, 0 wrong. Every look-alike was now settled with one lookup. On 2 wrong-person cases the model found the right NPI but named the cause as a typing error, and repeated that through both retries. | Before naming a cause that carries a fix, the agent now states one fact: whether the NPI on the line has a registry record. Code checks that fact. Where more than one person carries the name, code also checks that the pick follows the procedure. |
| 6 | All 35 development exceptions. Stopped after 25. | 22 of 25 right, 3 to a person, 0 wrong. The model now stated the facts correctly but still named a cause the procedure does not give for them, on the same 2 wrong-person cases and 1 name difference. | The shape of the conclusion now carries the procedure's decision table: once the facts are stated as yes or no, only the cause the procedure gives for them can be written. Failed-check messages quote the rule that was broken and never give the answer. |
| 7 | All 35 development exceptions, final version. | See results/runs/dev/report.md | Frozen: procedure_v1.md, the lookups, the loop and the checks. The test set was then scored once. |

What stayed fixed throughout: the answer key, the split into development and
test exceptions, the rule that a fix must come from a registry result and
carry the name on the line, and temperature 0.

What the rounds taught: the model was reliable at running lookups and reading
their results, and unreliable at applying the procedure's logic to what it
read. Each round moved one more piece of pure logic out of the model's hands
and into a fact that code checks or a shape the answer must fit.

## After the freeze: steps 10 to 12 (November 22, 2026)

Three things were added around the frozen agent. No development round was run for them, and the test set was not touched.

| Added | What changed in the code | What did not change | How it was checked |
|---|---|---|---|
| The lookups over MCP (step 10) | New files: `mcp_server.py`, `agent/mcp_client.py`, `10_tools_over_mcp.py`. Step 5 takes `--tools mcp` | The lookups themselves (`agent/tools.py`), the loop, the checks, the procedure | All 374 lookups of the stored runs replayed through MCP: same text, same facts. The 35 development exceptions rerun through MCP on the same model: identical to the stored run |
| Traces (step 11) | New files: `agent/tracing.py`, `11_trace_report.py`. Step 5 takes `--trace` | The loop: the model and the lookups are wrapped from the outside | The traces of that rerun read back: 35 traces, 225 spans, all 35 agree with the run's record |
| A hosted model behind the regression check (step 12) | New files: `12_hosted_model.py`, `tests/test_hosted.py`. In `agent/llm.py`, the endpoint class sets aside reasoning written inside `<reasoning>` tags and passes on an optional reasoning-effort setting | The class that runs a model file, so the laptop results | Step 12 end to end against a stand-in that replays the stored answers: the stored results come back exactly. A stand-in that fails the regression check is stopped before the test. No hosted model was run |
