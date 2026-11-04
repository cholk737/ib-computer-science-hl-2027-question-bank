# Persistent local question bank — specialist handoff

This is a saved Chunk 3 implementation, not a claim that all 823 questions or all syllabus scope have been reviewed. No examination, topic test, PDF or blueprint is produced. All practice questions and marking criteria are unofficial.

## Current application

Use `bank_db.py`, `serve_bank.py`, `persistent-web/` and `question_bank.sqlite3`. The earlier `web/`, `build_bank.py` and JavaScript core suite are a preserved static milestone, superseded by the persistent application.

From the project root, run:

```sh
python3 agents/chunk-3/agent-3-bank-audit/bank_db.py import
python3 agents/chunk-3/agent-3-bank-audit/serve_bank.py --port 8766
```

Open `http://127.0.0.1:8766/`. A running local server lasts only for the process lifetime; restart it after resuming. If the runtime sandbox refuses loopback binding, the coordinator must use its scoped server approval. No server or account continuation is promised. To install source elsewhere, copy the Python files and `persistent-web` together, pass `--db /absolute/path/to/permanent.sqlite3` to both commands, and pass `--root /absolute/project` after `import`. Project-root detection also searches ancestor syllabus paths.

The database is permanent on disk. Imports run in a SQLite transaction; original questions are never executed by import. Existing IDs, usage history, selections and independent verification are retained. The importer refuses mismatched question/marking versus full-record fields. All 823 baseline IDs and full prompts are present; no original source PDF is altered or copied into the app.

## Scope and verification contract

- Official objective text/full guidance is stored exactly, with the original complete syllabus JSON. Bullet IDs are `CODE:GNN`, one-based `guidance_paragraphs`. Must/may scope distinctions remain attached.
- `question_codes` records legacy candidate links only. They are not verified question-to-scope coverage.
- The coordinator's `question-bank/scope_evidence.json` is the authoritative approved-review snapshot. Per-question reviews require a current full-record SHA-256, reviewer, exact literal guidance, concrete assessed skill, direct/partial/supporting/reject relevance and rationale. Mapping verification additionally requires a structured verified status with evidence. String-only statuses or absent evidence do not promote anything.
- A review is validated entirely before mutation. Revised reviewer links replace their previous current links; history is retained. Withdrawn/unapproved reviews revoke their supplied links and verification checks. Independently updated manual checks survive snapshot withdrawal. Repeated unchanged review imports do not duplicate verification history.
- A direct mapping describes a directly assessed **aspect**, not automatically the entire bullet. Full-bullet coverage requires an explicit separately reviewed `covers_full_bullet: true`; none is inferred. Optional `statement_relevance` distinguishes statement construction from guidance that asks comparison.
- Six independently mutable dimensions are mapping, technical, answer, markscheme, assets and provenance. Default legacy import leaves them pending. This specialist review is separate from the future independent Chunk 4 audit.
- `question_type` may be explicit in a review or `metadata_updates.question_type`. Reviewed types are labelled as such; other command-based candidate types remain visibly review-required. A withdrawn review restores the original/inferred metadata.
- Current reviewed direct/partial codes join legacy candidate codes for topic/theme/level/paper retrieval, with the two origins labelled separately; original source records are never rewritten.

## Search behavior and limits

The interface supports keyword/ID, exact code, official statement, exact guidance, pasted scope, topic/theme, common/HL, difficulty, marks, type, source year/session, 2027 target Paper 1/Paper 2 and all-six-dimensions verified/unverified filters. Historical source paper is preserved separately. Pagination can retrieve all matching records.

Search retrieves from SQLite FTS and official scope indexes, then uses current checked question-to-scope evidence for reviewed direct/partial results. Candidates are separately labelled and can be excluded. A small transparent loop/concept alias registry helps recognize equivalent phrasing **only against existing reviewed skill evidence**. It is not an unrestricted semantic model, and keyword similarity cannot establish verification. Exact bullet queries preserve qualifiers; the representative pasted loop query keeps unestablished post-condition and other requirements visible. Full natural-language recall across arbitrary wording remains an improvement task rather than a certified feature.

Answers are fetched only after explicit reveal. Reviewer rationale, detailed verification evidence and issue details can also contain answers, so they use a separately labelled explicit reveal endpoint. Public search/detail payloads omit those fields and source markscheme summaries. Assessed-skill descriptions and exact official requirements remain visible. Local SQLite and source files themselves are not a security boundary.

Saved retrieval selections store ordered IDs, full-record hashes, query/filter parameters and metadata in the DB, and download a strict student-content-only JSON file. This is retrieval infrastructure, not exam/test assembly; it does not mark questions as used. Usage records require an explicit API action. Duplicate groups are labelled candidates until reviewed; no record is silently removed.

## Local API

- `GET /api/meta` — counts, objective/topic index and filter values.
- `GET /api/search?...` — paginated reviewed matches and labelled candidates, matched requirements and residual requirements. Query keys match the interface field IDs.
- `GET /api/question/ID` — student prompt/assets and public scope/status/source/history metadata.
- `GET /api/answer/ID` — explicit unofficial answer and marking criteria.
- `GET /api/review/ID` — explicit reviewer rationale/check details, potentially revealing answers.
- `POST /api/selection` — `{question_ids:[...], query:{...}, metadata:{...}}`.
- `POST /api/usage` — `{question_id, context, used_at?, selection_id?, notes?}`.
- `POST /api/verification` — `{question_id, dimension, status, evidence, reviewer, record_sha256}`. Status: verified/pending/issue/stale; update is audit-trailed and independent of other dimensions.
- `/source/SRC-NNN#page=N` — unchanged inventoried source PDF, only from the project sources directory.

Writes require same-origin JSON; server binds loopback only. Arbitrary question code is never run by the server.

## Verification and recovery

`test_db.py` uses a temporary project copy and database. Synthetic review fixtures never enter the real bank. It checks preservation, separate answers, stale/bogus/literal review rejection, whole-review atomicity, direct/partial/unsupported scope, statement versus bullet, all filters, mixed themes, exact IDs, pagination, snapshot withdrawal, revision/idempotence, safe reproducible selections, independent verification, incremental addition and content-change invalidation. `db_test_results.json` records the latest result. Browser checks belong to coordinator audit files; do not infer them from these tests.

```sh
python3 agents/chunk-3/agent-3-bank-audit/test_db.py
python3 agents/chunk-3/agent-3-bank-audit/verify_review_samples.py
python3 agents/chunk-3/agent-3-bank-audit/save_independent_audit.py
```

`independent_coverage.json` preserves a 112-code link census (not coverage certification), eight initial guide/prompt/answer samples, and three subsequent independent A/B review samples with executable reproductions. Fifteen zero-linked objectives remain at baseline; actual scope gaps are wider than link counts.

Create a transactionally consistent DB backup before handoff/install:

```sh
python3 agents/chunk-3/agent-3-bank-audit/bank_db.py backup audits/chunk-3/bank-checkpoint.sqlite3
```

Read `STATUS.json`, coordinator `PROGRESS.md`, the user scope override and approved evidence before resuming. The next exact tasks are recorded there. No new questions were authored by this specialist. All corpus-wide per-question review and original gap filling remain unfinished unless separately completed and checked by the coordinator.
