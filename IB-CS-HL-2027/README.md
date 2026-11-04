# IB Computer Science HL 2027 — unofficial practice-exam project

Fresh project initialized 4 November 2026. Only Chunk 1 (Steps 1–3) is currently authorized. All future practice papers and authored marking criteria will be unofficial; no affiliation or endorsement is implied.

## Find the work

- `AGENTS.md`: project rules and user-controlled chunk gates.
- `PROGRESS.md`: authoritative checkpoint and exact resume action.
- `QA_ISSUES.md`: source defects, uncertainties and future processing constraints.
- `sources/SOURCE_INVENTORY.csv` and `.json`: 48 uploaded PDF files with stable IDs, SHA-256 hashes, identities, original paths, verified copies and availability notes.
- `sources/2027-guide/` and `sources/2027-specimen/`: unmodified source copies and page-separated extraction aids.
- `sources/historical-papers/`: unmodified uploaded historical PDFs. Inventory only in Chunk 1; no question processing.
- `syllabus/SYLLABUS_MASTER.csv`: consolidated individual-statement scope index after coordinator verification; detailed JSON evidence is referenced per row.
- `syllabus/SCOPE_VERIFICATION.md`: code census, scope rules, checks and caveats.
- `specimen/SPECIMEN_ANALYSIS.md`: verified assessment-format and marking analysis after review.
- `agents/chunk-1/`: three isolated specialist outputs, source evidence and findings.
- `audits/`: independent coordinator checks and checkpoint manifests.
- `mapping/`, `question-bank/`, `coverage/`: initialized CSV schemas; empty until their authorized work. An empty index does not mean coverage has been established.
- `exams/`, `final-markschemes/`: reserved for later authorized chunks.

## Source conventions

Original PDFs in the parent workspace are unchanged. Local source copies are checked against originals by SHA-256. Source IDs identify files, not necessarily unique examinations: SRC-045 duplicates SRC-044 byte-for-byte; SRC-047 is a scanned alternate of SRC-005. Prefer complete verified versions and do not count alternates as extra question coverage.

PDF pages are one-based physical file pages. Printed guide pages are PDF page minus six for the syllabus and assessment sections. Specimen component page numbers restart; use the compilation PDF page together with the printed page. Syllabus wording and source quirks are preserved separately from analyst interpretations.

## Resume

Read `AGENTS.md`, `PROGRESS.md`, `QA_ISSUES.md`, the inventory and relevant master indexes. Confirm files and checksums exist. Continue only the exact unfinished action in the checkpoint. Do not advance to the next chunk without a new user instruction. No automatic continuation is promised.

Python scripts use the bundled runtime documented in `audits/RUNTIME.md`. Raw PDF extraction aids can contain layout spaces and are not the verified scope master. JSON is used for substantive guidance, not just the CSV index.
