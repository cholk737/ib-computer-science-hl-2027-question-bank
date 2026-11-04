# Progress — Chunk 2 active

Current checkpoint C2-003 — 2026-11-04 (Europe/Zurich). Authorized Steps4–6 only. Do not begin Chunk3 or generate full exam PDFs.

## Authoritative merged checkpoint

- 60 approved batch snapshots; 437 extracted source subquestions.
- 331 scoped A/B source subquestions mapped; 541 mapping rows including explicit C exclusions.
- 328 unique converted practice questions; 106 obsolete source exclusions; 3 source records reuse an existing practice.
- 0 unresolved mappings among the approved/merged records. Other saved author batches still require review.
- Each bank record has a separate question file and preliminary unofficial marking file; no official marking status claimed. All original sources unchanged.

## Saved specialist work awaiting remaining review/integration

Latest structural snapshot: 746 source records, 553 practice records, 99 batches across 19 source papers (some partial). Author completeness flags: {"SRC-001": true, "SRC-002": true, "SRC-004": true, "SRC-005": true, "SRC-006": true, "SRC-007": true, "SRC-008": true, "SRC-009": true, "SRC-016": true, "SRC-018": true, "SRC-020": true, "SRC-022": true, "SRC-024": true, "SRC-026": true, "SRC-028": true, "SRC-030": true, "SRC-033": true, "SRC-034": false}. Do not count a paper finished solely because it has saved batches.

Exactly three specialists ran and resumed under the same identities after a reported usage interruption: Processor A /root/historical_processor_a (8 assigned papers), B /root/historical_processor_b (8), C /root/historical_processor_c (7). All have contributed durable results. Source-ID-sorted round-robin assignments are fixed in extraction/HISTORICAL_MANIFEST.json. Ownership is isolated; coordinator alone writes masters.

## Files / evidence

- extraction/HISTORICAL_QUESTION_INDEX.csv and by-paper/<source>/questions/*.json
- mapping/SYLLABUS_MAPPING.csv
- question-bank/QUESTION_BANK.csv; questions/, markschemes/, records/
- extraction/OBSOLETE_QUESTIONS.csv
- audits/chunk-2/APPROVED_BATCHES.json, MERGE_LEDGER.json, MERGE_STATUS.json
- BATCH_REVIEW.json, MARK_RECONCILIATION.json, CODE_REVIEW.json, VISUAL_REVIEW.json, scan OCR mark reconciliations, source issue and coordinator override indexes
- QA_ISSUES.md; all three agents' findings and per-paper audits

Checkpoint history is in audits/chunk-2/PROGRESS_HISTORY.md. Chunk1 ledger is PROGRESS_CHUNK_1_ARCHIVE.md, verified commit46e2823.

## Outstanding / exact next action

Finish remaining assigned old-option Paper2 sources and final wording/transcription repairs. Recheck every new/changed batch snapshot, reconcile paper mark positions against original sources, review full mapped guidance and representative solutions, run saved code checks, resolve duplicate-scope differences, then cumulatively approve/merge. Update history after each batch or finished paper. Existing328 practice records must remain in the cumulative bank unless an explicit logged correction removes/reuses one.

Known source caveats and editorial fixes are in QA and agent findings; no missing2026 markscheme may be invented. Source-only PNG renders and unmodified PDFs are retained locally, excluded from Git. No automatic background continuation is promised. Stop only at completed Chunk2 or an honestly recorded interruption checkpoint.
