# Step 10. The lookups over MCP

The agent's four lookups are served by an MCP server (`mcp_server.py`) and called through an MCP client (`agent/mcp_client.py`). The server is started as a child process and the two exchange JSON-RPC messages over its standard input and output.

## The tools the server offers

| Tool | Arguments | What it does |
|---|---|---|
| `registry_lookup` | npi | Look up one ten-digit NPI in the registry snapshot. Returns the registered person, or says there is no record. |
| `registry_search` | line_npi, name | Search the registry snapshot by first and last name. line_npi is the NPI on the ledger line, so each match can say in how many digits it differs from it. |
| `ledger_history` | name | Count the ledger lines under a person's name, by the NPI each line carries. |
| `source_documents` | line_ids | Give the source document number, feed and load date of ledger lines. Input: line IDs such as L00012, separated by commas. |

## Every stored lookup, replayed through MCP

No model is involved. Each lookup the laptop model asked for in the stored runs is sent through MCP again. The text that comes back is compared with the text the run stored, and the facts with what the direct call returns.

| Stored run | Registry | Lookups replayed | Same text | Same facts |
|---|---|---|---|---|
| dev | up | 55 | 55 | 55 |
| dev_smaller_model | up | 62 | 62 | 62 |
| my_dev | up | 55 | 55 | 55 |
| my_dev3 | up | 7 | 7 | 7 |
| my_test | up | 18 | 18 | 18 |
| test | up | 150 | 150 | 150 |
| test_note | up | 42 | 42 | 42 |
| test_outage | down | 38 | 38 | 38 |
| test_recheck_after_hardening | up | 27 | 27 | 27 |

**454 of 454 lookups returned the same text through MCP, and 454 of 454 the same facts.** One lookup through MCP took 3.4 milliseconds at the median, on this machine.

## A run through MCP against the stored run

Run `dev_mcp` (Qwen3-4B-Q4_K_M.gguf, lookups through MCP, traced) against the stored run `dev` of the same exceptions.

- **35 of 35 exceptions are identical** in outcome, cause, fix, explanation, every lookup and its result, every step, and the token counts.
- Scored against the answer key: 35 right, 0 to a person, 0 wrong.
- 55 lookups went through MCP in 0.17 seconds in all.

## What this does and does not show

- It shows that moving the lookups behind MCP changed where they run and nothing the model reads.
- It does not make the agent better or worse. The procedure, the model and the checks are the same.
- The server has no login and listens only to the process that started it. A server offered to other teams would need both.
