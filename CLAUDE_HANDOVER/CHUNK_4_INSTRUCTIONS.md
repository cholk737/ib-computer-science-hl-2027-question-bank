# Chunk4 — full question-bank independent verification (future only)

Work as ONE AGENT, sequentially. Never spawn, delegate to, or wait for subagents. Historical specialist notes are evidence, not an active execution requirement. Preserve stable question IDs and completed work. Read progress and actual files before editing. Save after every 2–3 new/reviewed questions and meaningful milestone, update progress, and commit verified work. Complete only the user-authorized active chunk, then stop. No automatic background continuation.

Start only after completed Chunk3 and explicit user assignment. Do not execute during current handover. Retain stable IDs, old versions/hashes, correction reason and audit trail; invalidate and recheck dependent mappings/answers on changes. Canonical files and known QA are described in QUESTION_BANK_GUIDE.md.



Create a detailed, standalone CHUNK_4_INSTRUCTIONS.md.

This file must provide enough information for Claude to execute Chunk 4 without having to ask Codex anything.

## Objective

Independently verify and correct the entire question bank.

For EVERY question, Claude must check:

1. Correct 2027 syllabus learning statement.
2. Correct detailed scope mappings.
3. Technical accuracy.
4. Appropriate specimen-paper style.
5. Appropriate difficulty.
6. Realistic marks.
7. Complete question wording.
8. Complete model answer.
9. Correct marking criteria.
10. Partial-credit guidance.
11. Alternative acceptable solutions.
12. Python syntax where relevant.
13. Python execution and expected outputs.
14. Algorithm correctness.
15. Code-construction task validity.
16. Required tables, code and diagrams.
17. Duplicate or near-duplicate questions.
18. Source traceability.
19. Database and answer-link integrity.

For programming questions, test reference solutions and relevant edge cases where feasible.

Correct identified errors without unnecessarily changing permanent question IDs.

Maintain a verification and correction history.

Use manageable batches and save frequently.

Do not mark a question fully verified unless all required checks have passed.

At the end of Chunk 4, produce:

- Verified question database
- Verified answers and markschemes
- Per-question verification records
- Updated syllabus coverage report
- Duplicate-question report
- Final QA summary
- Verified and unverified question counts

Do not generate full examinations during Chunk 4.

Stop at the completion of Chunk 4.

---
