# Original question batch 2 — author report

Written 2026-11-04 (evening) by Claude working as ONE AGENT on the active Chunk 3. 21 new original, unofficial questions were added for the 13 syllabus statements that had no linked question at handover. No examination, topic test or PDF was produced. Author checks are **not** the independent Chunk 4 verification.

| ID | Code | Level | Command | Marks | Type | Check |
|---|---|---|---|---:|---|---|
| O-C3-A-001 | A1.1.6 | HL-only | Describe | 4 | description | manual vs exact guidance |
| O-C3-A-002 | A1.1.6 | HL-only | Calculate | 3 | calculation | 52 executed cases |
| O-C3-A-003 | A1.3.3 | SL/HL common | Calculate | 4 | calculation | 2 executed cases |
| O-C3-A-004 | A1.3.3 | SL/HL common | Compare | 6 | comparison | manual vs exact guidance |
| O-C3-A-005 | A2.1.5 | HL-only | Describe | 6 | description | manual vs exact guidance |
| O-C3-A-006 | A2.2.1 | SL/HL common | Describe | 5 | description | manual vs exact guidance |
| O-C3-A-007 | A2.2.1 | SL/HL common | Compare | 4 | comparison | manual vs exact guidance |
| O-C3-A-008 | A2.3.1 | SL/HL common | Describe | 6 | description | manual vs exact guidance |
| O-C3-A-009 | A2.3.4 | HL-only | Explain | 6 | explanation | manual vs exact guidance |
| O-C3-A-010 | A3.2.7 | SL/HL common | Evaluate | 6 | evaluation | manual vs exact guidance |
| O-C3-A-011 | A4.2.2 | HL-only | Describe | 6 | description | manual vs exact guidance |
| O-C3-A-012 | A4.2.3 | HL-only | Describe | 5 | description | manual vs exact guidance |
| O-C3-A-013 | A4.3.9 | HL-only | Describe | 6 | description | manual vs exact guidance |
| O-C3-A-014 | A4.3.9 | HL-only | Calculate | 4 | calculation | 1129 executed cases |
| O-C3-B-004 | B1.1.1 | SL/HL common | Construct | 6 | problem specification construction | manual vs exact guidance |
| O-C3-B-005 | B3.2.5 | HL-only | Explain | 6 | explanation | manual vs exact guidance |
| O-C3-B-006 | B3.2.5 | HL-only | Construct | 7 | Python code construction | 9 executed cases |
| O-C3-B-007 | B3.2.5 | HL-only | Construct | 5 | Python code construction | 6 executed cases |
| O-C3-B-008 | B4.1.6 | HL-only | Construct | 8 | Python code construction | 20245 executed cases |
| O-C3-B-009 | B4.1.6 | HL-only | Trace | 6 | trace | 3 executed cases |
| O-C3-B-010 | B4.1.6 | HL-only | Explain | 4 | explanation | manual vs exact guidance |

## How they were made and checked

- Read each exact statement and all guidance paragraphs from syllabus/SYLLABUS_MASTER.json; level and theme asserted against it by the generator.
- Searched every bank prompt for overlapping concepts (round robin, NAT, pipelining, observer, hash/probing, IPv6, mesh, routing, feature selection, dimensionality, CNN, problem specification, TCP/IP): no existing near-duplicate.
- Theme A follows Paper 1 command/mark style; Theme B uses Python. Answers and one-mark criteria are stored separately from the student file; criteria sum to marks.
- Executable checks (audits/chunk-3/ORIGINAL_BATCH2_CHECKS.json): pipeline cycle simulation, FCFS/RR simulation, CNN sliding-window size simulation, observer and factory behaviour/edge cases, hash table vs dict oracle with 20k+ randomized operations including wrap-around, replacement and full-table lookups, and hash trace re-derivation.
- Integrated through scripts/integrate_scope_reviews.py approvals, enrich_bank_index_chunk3.py, build_coverage_report.py, bank_db import and checkpoint_chunk3.py in batches of three, one commit per batch.

## Search changes

- bank_db.normalize_codes routes printed variants such as the guide typo A.1.2.5 (and B.4.1.6) to normalized codes for code/text/scope_text queries. Stored evidence is unchanged.
- New isolated test suite question-bank/search/test_c3_originals.py (5 checks) plus 7 new code-route cases in test_semantic_precision.py (17 total). Existing 23 functional tests still pass.
- Browser check (Playwright, 390 px and 1280 px): objective B4.1.6 search lists the new originals, answers stay hidden by default, no horizontal overflow, no page errors. Saved in audits/chunk-3/UI_CHECK_BATCH2.json.

## Limits and what remains

- Each link covers named aspects only; no statement is certified fully covered. Coverage limits are stored per question (verification.scope).
- The 94 saved reviews awaiting integration and 669 unreviewed historical records were not processed in this session.
- 821 inferred question types, REVIEW_ISSUES.json adjudication, duplicate families and arbitrary-wording semantic recall remain open.
- Next original IDs: O-C3-A-015, O-C3-B-011.
