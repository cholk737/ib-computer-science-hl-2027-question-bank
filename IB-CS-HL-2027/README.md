## Current portable handover (latest user instructions)

826 permanent questions:823 adapted plus3 original Python construction questions. Chunk3 is incomplete and database/search/coverage only. Canonical DB: question-bank/database.sqlite3; canonical application: question-bank/search/. Current scope evidence: question-bank/scope_evidence.json and mapping/SCOPE_MAPPING.csv. Future Claude works ONE AGENT. Later Chunk4 verifies the whole bank without exams; later Chunk5 generates/ranks many distinct exams. Read repository-root CLAUDE.md and CLAUDE_HANDOVER/CURRENT_PROGRESS.md (or the extracted handover wrapper). The older notes below are historical where they conflict.

# IB Computer Science HL 2027 — unofficial practice-exam project

Fresh project initialized 4 November 2026. Chunks 1 and 2 (Steps 1–6) are complete; Chunk 3 is now authorized and active with recovery checkpoints. Read PROGRESS.md for the current checkpoint. All future practice papers and authored marking criteria will be unofficial; no affiliation or endorsement is implied.

## Find the work

- `AGENTS.md`: project rules and user-controlled chunk gates.
- `PROGRESS.md`: authoritative checkpoint and exact resume action.
- `QA_ISSUES.md`: source defects, uncertainties and future processing constraints.
- `sources/SOURCE_INVENTORY.csv` and `.json`: 48 uploaded PDF files with stable IDs, SHA-256 hashes, identities, original paths, verified copies and availability notes.
- `sources/2027-guide/` and `sources/2027-specimen/`: unmodified source copies and page-separated extraction aids.
- `sources/historical-papers/`: unmodified uploaded historical PDFs. Historical processing is recorded in extraction/HISTORICAL_MANIFEST.csv and the Chunk 2 indexes.
- `syllabus/SYLLABUS_MASTER.csv`: consolidated individual-statement scope index after coordinator verification; detailed JSON evidence is referenced per row.
- `syllabus/SCOPE_VERIFICATION.md`: code census, scope rules, checks and caveats.
- `specimen/SPECIMEN_ANALYSIS.md`: verified assessment-format and marking analysis after review.
- `agents/chunk-1/`: three isolated specialist outputs, source evidence and findings.
- `audits/`: independent coordinator checks and checkpoint manifests.
- `mapping/`, `question-bank/`, `coverage/`: mapping and question-bank indexes are cumulatively populated in Chunk 2; the coverage index remains reserved for the later authorized audit. Question counts do not establish coverage.
- `exams/`, `final-markschemes/`: reserved for later authorized chunks.

## Source conventions

Original PDFs in the parent workspace are unchanged. Local source copies are checked against originals by SHA-256. Source IDs identify files, not necessarily unique examinations: SRC-045 duplicates SRC-044 byte-for-byte; SRC-047 is a scanned alternate of SRC-005. Prefer complete verified versions and do not count alternates as extra question coverage.

PDF pages are one-based physical file pages. Printed guide pages are PDF page minus six for the syllabus and assessment sections. Specimen component page numbers restart; use the compilation PDF page together with the printed page. Syllabus wording and source quirks are preserved separately from analyst interpretations.

## Resume

Read `AGENTS.md`, `PROGRESS.md`, `QA_ISSUES.md`, the inventory and relevant master indexes. Confirm files and checksums exist. Continue only the exact unfinished action in the checkpoint. Do not advance to the next chunk without a new user instruction. No automatic continuation is promised.

Python scripts use the bundled runtime documented in `audits/RUNTIME.md`. Raw PDF extraction aids can contain layout spaces and are not the verified scope master. JSON is used for substantive guidance, not just the CSV index.


## Chunk 2 processing

- `extraction/README.md` explains the source manifest, complete leaf records and exclusions.
- `question-bank/README.md` explains the separate question, preliminary marking and full-provenance files.
- `audits/chunk-2/` contains source mark reconciliation, code/SQL tests, source/solution samples, duplicate candidates, coordinator corrections and cumulative batch-approval/merge evidence.
- The checkpoint labelled C1 remains a historical snapshot. `scripts/validate_checkpoint.py` reproduces its original empty-bank assumptions and must not be used as a current Chunk 2 validator. Current Chunk 2 review scripts are named explicitly in the progress/checkpoint reports.
- Source PDFs and PNG evidence stay local, hash-inventoried and excluded from Git; text/JSON/CSV records and scripts are committed at milestones. All practice marking remains unofficial/preliminary until the later exam-specific audit.
