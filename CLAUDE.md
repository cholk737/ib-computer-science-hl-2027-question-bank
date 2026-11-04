# CLAUDE.md — controlling single-agent continuation instructions

Work as ONE AGENT, sequentially. Never spawn, delegate to, or wait for subagents. Historical specialist notes are evidence, not an active execution requirement. Preserve stable question IDs and completed work. Read progress and actual files before editing. Save after every 2–3 new/reviewed questions and meaningful milestone, update progress, and commit verified work. Complete only the user-authorized active chunk, then stop. No automatic background continuation.

## Authority and current stage

The latest user instruction is preserved verbatim at IB-CS-HL-2027/audits/handover/USER_MASTER_HANDOVER_REQUEST.md (under PROJECT_FILES/ when using ZIP). This file controls Claude execution over conflicting historical subagent/four-chunk notes. Use uploaded official first-assessment-2027 guide for exact scope and common/HL classification, HL Python specimen for question style, specimen criteria for marking conventions, and historical material for provenance. Preserve originals and do not invent codes, references, completed checks or official marking status. All authored questions/criteria are unofficial.

Chunk 1 foundation and Chunk 2 historical conversion are complete; do not repeat them. **Chunk 3 is incomplete**: permanent bank/search, exact per-question scope mapping, genuine gap questions including Python construction. No exam/test/PDF generation in Chunk 3. **Chunk 4** later independently verifies the whole bank, with no full examinations. **Chunk 5** later generates many distinct verified Paper 1/Paper 2 papers, expands the bank when needed, and ranks verified results. Do not execute a later chunk merely because instructions exist.

When working at repository/PROJECT_FILES root, wrapper documents are under CLAUDE_HANDOVER/ in a clone or beside PROJECT_FILES/ in the extracted ZIP. Resolve CURRENT_PROGRESS.md/NEXT_ACTIONS.md there; the working project is IB-CS-HL-2027/.

## Begin each session

1. Read CURRENT_PROGRESS.md, NEXT_ACTIONS.md, IB-CS-HL-2027/PROGRESS.md, QA_ISSUES.md and the relevant stage instructions.
2. Check the actual database, QUESTION_BANK.csv, scope_evidence.json, coverage and latest checkpoint. Reconcile counts/hashes; do not trust chat summaries.
3. Use FULL_BANK_REVIEW_QUEUE.csv to resume the three saved historical queues sequentially. Their roles do not imply live agents. Latest source002 independent recommendations are partial and hash-bound.
4. Preserve P-SRC... and O-C3-B-001/002/003. Do not rerun old Chunk 2 generators over repaired approved records. Do not rerun create_handover_gap_batch.py: it deliberately refuses existing IDs.
5. Read full exact statement and every guidance paragraph for any question you review/create. A mention, legacy code link, direct aspect or question count does not certify a whole statement/bullet. Respect must/may include. Use Python; SQL is appropriate for database questions. Simple non-branching recursion construction/tracing only where B2.4.5 applies.

## Maintain data without false promotion

Master CSVs are indexes; keep full question/answer records and provenance separately. SQLite `question_codes` are legacy candidate links; current scoped evidence is separately reviewed. Update mapping/technical/answer/markscheme/assets/provenance independently, with reviewer/evidence/current record hashes. All-six author checks do not equal later independent Chunk 4 verification. Retain unresolved issues. Do not promote the remaining corpus on import or keyword match.

Canonical code: question-bank/search/. Canonical DB: question-bank/database.sqlite3. Agent-3 code/database are an older development snapshot. Canonical code includes coordinator semantic precision fixes not present in that developer snapshot. Keep student answers and answer-bearing reviewer rationale hidden until explicitly requested. Search has limited transparent aliases; arbitrary natural-language semantic recall is not certified.

## Save and stop

Save new substantive records, correct index links, exact evidence, reproducible tests and atomic checkpoints after every 2–3 questions. Coordinate sequentially yourself; if retaining historical reviewer names, identify new review authorship honestly. On interruption, write the exact next ID/action and failed checks. Stop after the current chunk and report what is actually saved. Never promise background continuation.

<!-- REQUIRED-ADDITIONAL-QUESTIONS-START -->
## Required additional question creation

**Create more original questions during Chunk3.** Read QUESTION_GENERATION_INSTRUCTIONS.md in the handover wrapper (also present in the working project). The826-question bank is a starting point, not the final limit. Work in small cycles of relevant scope review, genuine gap-question authoring, answer/code verification, searchable-bank integration and checkpoints. Include substantial actual Python code-writing tasks where the guide requires them. Do not stop at reviewing the existing bank or postpone every new question until unrelated reviews are finished. Preserve existing IDs; keep answers/criteria separate; save every2–3 questions. This authoring work is already part of the active Chunk3 assignment. Later Chunk5 must also generate and verify new questions when needed for more distinct examinations. Keep the single-agent rule and chunk boundaries; no examinations or PDFs in Chunk3.
<!-- REQUIRED-ADDITIONAL-QUESTIONS-END -->
