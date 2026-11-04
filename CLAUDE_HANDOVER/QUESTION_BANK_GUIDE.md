# Question bank guide

```sh
cd PROJECT_FILES/IB-CS-HL-2027
python3 question-bank/search/bank_db.py --db question-bank/database.sqlite3 import --root "$PWD"
python3 question-bank/search/serve_bank.py --db question-bank/database.sqlite3 --port 8767
```

Open `http://127.0.0.1:8767/`. With a Git clone rather than this ZIP, use `cd IB-CS-HL-2027` instead. Re-import refreshes the relocated source-PDF root without rebuilding existing questions or losing usage/verification history. Python 3.10+ with SQLite FTS5 is needed; the live app has no third-party Python or network-service dependency. It imports no stored question code. Stop the server with Ctrl-C. No live server is promised by this handover.


QUESTION_BANK.csv is an index, not the question content. questions/ID.json contains student content, markschemes/ID.json separate preliminary criteria, records/ID.json the full internal provenance bundle. SQLite questions/answers also preserve full content; answer-bearing internal records are not exposed as public student payloads. Original IDs have no invented historical source links.

syllabus/SYLLABUS_MASTER.csv/.json and records/ contain official statement text/full guidance/level/source pages. Historical mapping/SYLLABUS_MAPPING.csv remains the source-question-to-guide ledger. Current mapping/SCOPE_MAPPING.csv and question-bank/scope_evidence.json add question-to-exact-guidance aspects, including originals and revised/narrowed matches. A supporting or rejected link is not a direct tested requirement. Keep legacy and reviewed mappings distinct.

Canonical local app is question-bank/search/, with question-bank/database.sqlite3. `question_codes` is candidate metadata. `scope_evidence` and `review_records` are current approved exact review snapshots. Import is transactional and incremental; usage, selections and independent manual verification survive unchanged import. Reviews need current record SHA, exact guide bullet, concrete skill/relevance/evidence and structured status. Withdrawn/revised source approvals revoke their supplied checks without erasing independent manual checks. `verification` and `verification_history` separate six dimensions. `review_history`, duplicate_groups, usage_history and selections support later audit/reproducibility. No selection itself generates an examination or marks question use.

Student queries support text/ID, exact code/topic, pasted scope, theme, common/HL/mixed, marks, difficulty, type, original year/session, 2027 target paper and verification. Answers hidden by default. Reviewer rationale/issues can reveal answers and have their own explicit reveal. Source PDFs are unchanged inventory references; the2 historical2026 papers have no supplied official markscheme. All adapted/new marking criteria remain unofficial/preliminary.

Run `python3 question-bank/search/test_db.py` and `python3 question-bank/search/test_semantic_precision.py` from project root. Tests use a temporary isolated DB; fixture questions are never inserted into the real bank. Query aliases are transparent and deliberately narrow; not an unrestricted semantic model. Canonical code has stricter fixes than historical agent-3 source. Read its README plus coordinator installation/QA notes before changing it.

To merge reviewed evidence, scripts/integrate_scope_reviews.py validates exact current hashes and needs an explicit coordinator approval reason. It currently loads A/B historical folders plus original-review-drafts/. Claude may keep those data paths but must record new review authorship honestly and adjust the collector ownership guard if personally authoring revisions as Claude; do not impersonate old agents. scripts/build_coverage_report.py, enrich_bank_index_chunk3.py, collect_chunk3_review_state.py and checkpoint_chunk3.py refresh derived reports. Old specialist first-pass scope audits remain historical inputs, so fix/extend their semantics carefully rather than pretending new questions were in the original audit.
