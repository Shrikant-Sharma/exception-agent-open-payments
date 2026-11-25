# Lineage: where every number comes from

Each row is one link in the chain. A fingerprint is the SHA-256 of the file; if a file changes, its fingerprint changes.

| Step | What | Source or version | Rows | Fingerprint (first 12) |
|---|---|---|---|---|
| 1 | Payment extract | CMS Open Payments, 2025 General Payment Data, dataset fb0b1734-1410-429d-92f6-3f4b35218e5e, pulled 2026-11-22T02:38:02Z | 5,885 | af45fee23da6 |
| 2 | Registry snapshot | NPPES NPI Registry API, version 2.1, pulled 2026-11-22T02:39:10Z | 6,068 | b6db0cfa3461 |
| 3 | Ledger with planted errors | 03_build_scenario.py, seed 20261122 | 5,907 | f3e63784efe3 |
| 3 | Draft filing | 03_build_scenario.py, seed 20261122 | 5,805 | bf7713a253e0 |
| 3 | Answer key | 03_build_scenario.py, seed 20261122 | 171 | 714f7159bcc3 |
| 4 | Exception log | 04_reconcile.py, rule file 2025.1 | 167 | 39c2496d814e |
| 5 | Agent run 'dev' | model Qwen3-4B-Q4_K_M.gguf (7485fe6f11af), procedure procedure_v1.md (cceae9482b12), rule file 2025.1, started 2026-11-22T04:48:47Z | 35 | 0f12c47a6bd3 |
| 5 | Agent run 'dev_mcp' | model Qwen3-4B-Q4_K_M.gguf (7485fe6f11af), procedure procedure_v1.md (cceae9482b12), rule file 2025.1, started 2026-11-23T03:28:51Z | 35 | e3bc5ea3c0fa |
| 5 | Agent run 'dev_smaller_model' | model qwen2.5-1.5b-instruct-q4_k_m.gguf (6a1a2eb6d156), procedure procedure_v1.md (cceae9482b12), rule file 2025.1, started 2026-11-22T07:46:23Z | 35 | 2f3638d39e23 |
| 5 | Agent run 'test' | model Qwen3-4B-Q4_K_M.gguf (7485fe6f11af), procedure procedure_v1.md (cceae9482b12), rule file 2025.1, started 2026-11-22T05:22:24Z | 95 | 6f870b4e9773 |
| 5 | Agent run 'test_note' | model Qwen3-4B-Q4_K_M.gguf (7485fe6f11af), procedure procedure_v1.md (cceae9482b12), rule file 2025.1, started 2026-11-22T07:19:40Z | 21 | d70491a2b857 |
| 5 | Agent run 'test_outage' | model Qwen3-4B-Q4_K_M.gguf (7485fe6f11af), procedure procedure_v1.md (cceae9482b12), rule file 2025.1, started 2026-11-22T07:04:42Z | 21 | 9b9b2706d094 |
| 5 | Agent run 'test_recheck_after_hardening' | model Qwen3-4B-Q4_K_M.gguf (7485fe6f11af), procedure procedure_v1.md (cceae9482b12), rule file 2025.1, started 2026-11-22T08:38:21Z | 12 | 69abb2021b1c |

The extract and the snapshot each have a manifest beside them with the exact query. Each agent run folder has a run_manifest.json with the fingerprints of the model file, the procedure and the data it ran on.
