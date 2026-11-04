# Start here — complete private project handover

Saved 2026-11-04T19:29:54.384789+01:00. Read CLAUDE.md, CURRENT_PROGRESS.md and NEXT_ACTIONS.md before doing work. The active stage is **Chunk 3, incomplete**. Chunks 1 and 2 are complete. Chunk 4 and Chunk 5 have not been executed. No practice examination, topic test or generated PDF is included or claimed.

The actual project is in PROJECT_FILES/IB-CS-HL-2027/. All 826 questions, separate answers/criteria, SQLite database, exact syllabus, sources, code, agent-era evidence and checkpoints are there. PROJECT_FILES also preserves repository-root instructions and setup files. The ZIP includes a Git bundle for history; use REPOSITORY_SETUP.md. GitHub creation/push was unavailable through the available authenticated creation paths; no remote URL is claimed. Keep any later remote **private**, named `ib-computer-science-hl-2027-question-bank`.

Work as ONE AGENT, sequentially. Never spawn, delegate to, or wait for subagents. Historical specialist notes are evidence, not an active execution requirement. Preserve stable question IDs and completed work. Read progress and actual files before editing. Save after every 2–3 new/reviewed questions and meaningful milestone, update progress, and commit verified work. Complete only the user-authorized active chunk, then stop. No automatic background continuation.

```sh
cd PROJECT_FILES/IB-CS-HL-2027
python3 question-bank/search/bank_db.py --db question-bank/database.sqlite3 import --root "$PWD"
python3 question-bank/search/serve_bank.py --db question-bank/database.sqlite3 --port 8767
```

Open `http://127.0.0.1:8767/`. With a Git clone rather than this ZIP, use `cd IB-CS-HL-2027` instead. Re-import refreshes the relocated source-PDF root without rebuilding existing questions or losing usage/verification history. Python 3.10+ with SQLite FTS5 is needed; the live app has no third-party Python or network-service dependency. It imports no stored question code. Stop the server with Ctrl-C. No live server is promised by this handover.


Do not start from Chunk 1. Historical AGENTS.md multi-agent and old four-chunk examination-output instructions are superseded for Claude by this handover and the latest master user request. Source authority remains guide → HL specimen → specimen markscheme → historical sources. Private uploaded official PDFs are source references, not a redistribution license or official endorsement of generated work.

<!-- REQUIRED-ADDITIONAL-QUESTIONS-START -->
## Required additional question creation

**Create more original questions during Chunk3.** Read QUESTION_GENERATION_INSTRUCTIONS.md in the handover wrapper (also present in the working project). The826-question bank is a starting point, not the final limit. Work in small cycles of relevant scope review, genuine gap-question authoring, answer/code verification, searchable-bank integration and checkpoints. Include substantial actual Python code-writing tasks where the guide requires them. Do not stop at reviewing the existing bank or postpone every new question until unrelated reviews are finished. Preserve existing IDs; keep answers/criteria separate; save every2–3 questions. This authoring work is already part of the active Chunk3 assignment. Later Chunk5 must also generate and verify new questions when needed for more distinct examinations. Keep the single-agent rule and chunk boundaries; no examinations or PDFs in Chunk3.
<!-- REQUIRED-ADDITIONAL-QUESTIONS-END -->
