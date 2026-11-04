"""Create standalone instructions/backlog; packaging and verification are separate.

Does not generate questions, examinations or PDFs. Run from any directory.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import collections
import csv
import io
import json
import os
import sqlite3

P = Path(__file__).resolve().parents[1]
R = P.parent
H = R / 'CLAUDE_HANDOVER'

QUESTION_GENERATION_INSTRUCTIONS = """# Required: create additional original questions

Creating more questions is an explicit part of the assignment. The existing826 questions and the3 original questions already added are a starting bank, not a final limit. Continue expanding it where exact2027 HL requirements lack sufficient genuine practice. Do not treat reviewing, indexing or importing the existing bank as completion of this authoring requirement.

## During the active Chunk3

Work as ONE AGENT, without subagents. Use small cycles: inspect a specific requirement and its existing candidates, identify a genuine gap, write and verify additional questions, integrate them, then checkpoint. Do not postpone all new questions until every unrelated historical record has been reviewed. Where a gap is uncertain, resolve that relevant mapping first; do not invent a gap or duplicate an existing assessed skill.

1. Read the exact learning statement and ALL its guidance in the uploaded2027 guide. Include common SL/HL and HL-only scope; preserve must-include/may-include limits.
2. Consult the appropriate2027 HL specimen and marking conventions. Use ThemeA style for A questions and Python ThemeB style for B questions, with appropriate IB commands, depth and marks.
3. Search the existing bank and inspect complete relevant prompts/answers, checked scope evidence and duplicate candidates. Use CHUNK3_SCOPE_BACKLOG.csv/json and the coverage report to prioritize meaningful missing skills and weak difficulty/application coverage.
4. Write genuinely new questions and contexts. Do not create superficial name/number substitutions or copy substantial source-question wording. Create additional questions for weakly covered requirements as well as requirements with zero links, when the evidence justifies them. Do not impose an arbitrary final question quota.
5. Include real Python CODE-CONSTRUCTION tasks requiring students to write functions, algorithms or classes where applicable. Cover functions/parameters/returns, selection, loops, searches, sorting, simple non-branching recursive code, file processing, debugging/correction, classes/constructors/methods, encapsulation, inheritance/polymorphism and HL ADTs only within exact guide scope. Explanation/tracing alone must not stand in for a required construction skill. SQL remains appropriate for database questions.
6. Make every question self-contained: complete prompt/subquestions, input/domain assumptions, necessary code/tables/diagrams, permanent unique ID, exact code and specific tested scope aspects, level, type, difficulty and realistic marks. Check existing IDs before reserving new ones. O-C3-B-004 and O-C3-A-001 are prospective next IDs, not permission to overwrite an existing file.
7. Store the model answer and mark-by-mark preliminary UNOFFICIAL criteria separately from student content. Include partial credit, acceptable alternatives and scope/verification limits. Keep genuine original questions free of invented historical provenance.
8. Execute Python reference solutions and independently check expected outputs, boundaries and relevant mutation/complexity claims. Verify conceptual answers, calculations and mark totals. Record checks honestly; author verification is not independent Chunk4 verification.
9. Add complete records to the permanent bank, exact scope-evidence indexes, coverage report and canonical SQLite database. Make the new questions searchable and their answers separately retrievable. Preserve all existing questions, stable IDs, provenance and history.
10. Save after every2–3 questions and meaningful milestone, update progress/QA and commit verified changes. Continue the next useful gap within the authorized chunk while resources permit. If interrupted, save completed IDs and the exact next task; do not promise background continuation.

Do not generate examinations, topic tests or PDFs during Chunk3. Stop at the chunk boundary. Chunk4 later independently verifies the full bank. Chunk5, when explicitly assigned after verification, must also create, test and add new questions whenever missing suitable bank content would prevent another genuinely distinct high-quality examination; it must not stop merely because the current bank is too small. Follow the standalone Chunk5 instructions and100-point quality rubric. Do not execute either later chunk now.
"""


def apply_question_generation_instruction():
    """Keep this requirement in every entry point and subsequent rebuild."""
    put('QUESTION_GENERATION_INSTRUCTIONS.md', QUESTION_GENERATION_INSTRUCTIONS)
    (P/'QUESTION_GENERATION_INSTRUCTIONS.md').write_text(QUESTION_GENERATION_INSTRUCTIONS.strip()+'\n')
    start='<!-- REQUIRED-ADDITIONAL-QUESTIONS-START -->'
    end='<!-- REQUIRED-ADDITIONAL-QUESTIONS-END -->'
    block='\n'.join([start, '## Required additional question creation', '',
        '**Create more original questions during Chunk3.** Read QUESTION_GENERATION_INSTRUCTIONS.md in the handover wrapper (also present in the working project). The826-question bank is a starting point, not the final limit. Work in small cycles of relevant scope review, genuine gap-question authoring, answer/code verification, searchable-bank integration and checkpoints. Include substantial actual Python code-writing tasks where the guide requires them. Do not stop at reviewing the existing bank or postpone every new question until unrelated reviews are finished. Preserve existing IDs; keep answers/criteria separate; save every2–3 questions. This authoring work is already part of the active Chunk3 assignment. Later Chunk5 must also generate and verify new questions when needed for more distinct examinations. Keep the single-agent rule and chunk boundaries; no examinations or PDFs in Chunk3.', end])
    targets=[H/n for n in ['00_READ_FIRST.md','CLAUDE.md','RESUME_PROMPT.md','NEXT_ACTIONS.md','CHUNK_3_INSTRUCTIONS.md','CHUNK_3_REMAINING_WORK.md','CHUNK_5_INSTRUCTIONS.md']]+[R/'CLAUDE.md']
    for path in targets:
        text=path.read_text()
        if start in text:
            before,rest=text.split(start,1);_,after=rest.split(end,1);text=before+block+after
        else:
            text=text.rstrip()+'\n\n'+block+'\n'
        temporary=path.with_name(path.name+'.tmp');temporary.write_text(text);os.replace(temporary,path)


def put(name, text):
    path = H / name
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(text.strip() + '\n', encoding='utf-8')
    os.replace(temp, path)


def main():
    H.mkdir(exist_ok=True)
    counts = json.loads((P/'audits/handover/DATA_COUNTS_AND_CHECKS.json').read_text())['counts']
    cover = json.loads((P/'coverage/OBJECTIVE_COVERAGE.json').read_text())
    audit_issues = json.loads((P/'audits/chunk-3/REVIEW_ISSUES.json').read_text())
    source_request = (P/'audits/handover/USER_MASTER_HANDOVER_REQUEST.md').read_text()
    latest = json.loads((P/'audits/chunk-3/LATEST_CHECKPOINT.json').read_text())['checkpoint']
    now = datetime.now(ZoneInfo('Europe/Zurich')).isoformat()
    db = sqlite3.connect(P/'question-bank/database.sqlite3')
    db.row_factory = sqlite3.Row
    typed = db.execute("SELECT count(*) FROM questions WHERE type_basis NOT LIKE '%candidate%'").fetchone()[0]
    candidate_typed = counts['questions'] - typed
    no_links = counts['zero_current_legacy_or_reviewed_question_codes']
    common = """Work as ONE AGENT, sequentially. Never spawn, delegate to, or wait for subagents. Historical specialist notes are evidence, not an active execution requirement. Preserve stable question IDs and completed work. Read progress and actual files before editing. Save after every 2–3 new/reviewed questions and meaningful milestone, update progress, and commit verified work. Complete only the user-authorized active chunk, then stop. No automatic background continuation."""
    commands = """```sh
cd PROJECT_FILES/IB-CS-HL-2027
python3 question-bank/search/bank_db.py --db question-bank/database.sqlite3 import --root "$PWD"
python3 question-bank/search/serve_bank.py --db question-bank/database.sqlite3 --port 8767
```

Open `http://127.0.0.1:8767/`. With a Git clone rather than this ZIP, use `cd IB-CS-HL-2027` instead. Re-import refreshes the relocated source-PDF root without rebuilding existing questions or losing usage/verification history. Python 3.10+ with SQLite FTS5 is needed; the live app has no third-party Python or network-service dependency. It imports no stored question code. Stop the server with Ctrl-C. No live server is promised by this handover.
"""
    put('00_READ_FIRST.md', f"""# Start here — complete private project handover

Saved {now}. Read CLAUDE.md, CURRENT_PROGRESS.md and NEXT_ACTIONS.md before doing work. The active stage is **Chunk 3, incomplete**. Chunks 1 and 2 are complete. Chunk 4 and Chunk 5 have not been executed. No practice examination, topic test or generated PDF is included or claimed.

The actual project is in PROJECT_FILES/IB-CS-HL-2027/. All {counts['questions']} questions, separate answers/criteria, SQLite database, exact syllabus, sources, code, agent-era evidence and checkpoints are there. PROJECT_FILES also preserves repository-root instructions and setup files. The ZIP includes a Git bundle for history; use REPOSITORY_SETUP.md. GitHub creation/push was unavailable through the available authenticated creation paths; no remote URL is claimed. Keep any later remote **private**, named `ib-computer-science-hl-2027-question-bank`.

{common}

{commands}

Do not start from Chunk 1. Historical AGENTS.md multi-agent and old four-chunk examination-output instructions are superseded for Claude by this handover and the latest master user request. Source authority remains guide → HL specimen → specimen markscheme → historical sources. Private uploaded official PDFs are source references, not a redistribution license or official endorsement of generated work.
""")
    claude = f"""# CLAUDE.md — controlling single-agent continuation instructions

{common}

## Authority and current stage

The latest user instruction is preserved verbatim at IB-CS-HL-2027/audits/handover/USER_MASTER_HANDOVER_REQUEST.md (under PROJECT_FILES/ when using ZIP). This file controls Claude execution over conflicting historical subagent/four-chunk notes. Use uploaded official first-assessment-2027 guide for exact scope and common/HL classification, HL Python specimen for question style, specimen criteria for marking conventions, and historical material for provenance. Preserve originals and do not invent codes, references, completed checks or official marking status. All authored questions/criteria are unofficial.

Chunk 1 foundation and Chunk 2 historical conversion are complete; do not repeat them. **Chunk 3 is incomplete**: permanent bank/search, exact per-question scope mapping, genuine gap questions including Python construction. No exam/test/PDF generation in Chunk 3. **Chunk 4** later independently verifies the whole bank, with no full examinations. **Chunk 5** later generates many distinct verified Paper 1/Paper 2 papers, expands the bank when needed, and ranks verified results. Do not execute a later chunk merely because instructions exist.

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
"""
    put('CLAUDE.md', claude)
    (R/'CLAUDE.md').write_text(claude)
    put('PROJECT_OVERVIEW.md', """# Project overview

An unofficial IB Computer Science HL first-assessment-2027 practice system, built from this project's uploaded guide, specimen compilation and historical PDFs. Source files are unchanged and hash-inventoried. Theme A is computer fundamentals, networks, databases and machine learning. Theme B is computational thinking, Python programming, OOP and HL ADTs. All applicable SL/HL common scope plus HL extensions are required.

The project originally planned four chunks; later user instructions superseded stages 3–5. Current stages: 1 source/syllabus/specimen foundation; 2 historical extraction/mapping/adaptation; 3 complete searchable bank and gaps; 4 independently verify entire bank; 5 repeated verified examination batches and quality ranking. Only Chunk 3 is currently active. Existing old stage-4/exam notes are historical, not authorization.

Data layers: immutable source PDFs and extraction evidence; exact syllabus master and per-statement records; historical source subquestions/mappings; adapted and original unofficial student questions; separate preliminary criteria; explicit scope reviews; granular SQLite verification/history; coverage and review queues. 112 statements include68 common and44 HL-only. 271 guidance paragraphs remain exact; paragraph IDs are stable CODE:GNN lookup references, not invented official syllabus codes.
""")
    put('CURRENT_PROGRESS.md', f"""# Current progress — verified saved counts

Saved {now}; active **Chunk 3 incomplete**. Chunk1 complete at46e2823; Chunk2 complete atdd5285c. Repository-first preservation commit26aa6de. Last generated checkpoint at document creation: `{latest}`; the actual newest ID is in PROJECT_FILES/IB-CS-HL-2027/PROGRESS.md and audits/chunk-3/LATEST_CHECKPOINT.json. REPOSITORY_STATUS.json records actual final local/remote/bundle status; no GitHub URL exists at this stage.

| Item | Verified saved count/status |
|---|---:|
| Total questions / searchable DB rows | {counts['questions']} |
| Adapted historical | {counts['adapted']} |
| Original Chunk3 questions | {counts['original']} |
| Full separate answers | {counts['answers']} |
| Preliminary marking criteria | {counts['preliminary_criteria']} |
| Explicit Python-writing directives | {counts['explicit_Python_construction_directives']} |
| Historical individual reviews saved | {counts['specialist_old_record_reviews_saved']} |
| Historical questions not yet individually reviewed | {counts['historical_reviews_not_yet_saved']} |
| Saved reviews awaiting coordinator integration | {counts['saved_reviews_pending_coordinator_merge']} |
| Approved scope review records in DB | {counts['scope_reviews_imported']} |
| Approved scope links | {counts['scope_links']} |
| All six author/current review dimensions marked verified | {counts['author_all_six_dimensions_verified']} |
| Independent Chunk4 verified | 0 |
| Awaiting independent Chunk4 audit | {counts['questions']} |
| Exact syllabus statements / guidance paragraphs |112 /271 |
| Completely covered statements certified |0 (no completeness claim) |
| First-pass substantial-evidence statements |19 (not certified complete) |
| First-pass partial/insufficient statements |78 |
| Baseline zero-linked statements |15; now13 after3 originals in2 codes |
| Explicit/reviewed type metadata |{typed} |
| Inferred type candidates needing review |{candidate_typed} |

The90 Python count is a conservative explicit-directive census with full prompts in audits/handover/PYTHON_CONSTRUCTION_CENSUS.json. Additional implicit-language construction tasks may exist; this is not90 independently technically verified questions. Every question has answer/marking content; presence is not correctness certification.

Originals: O-C3-B-001 file read/write/count/total (5 saved fixture/closure checks); O-C3-B-002 set intersection/difference/union (256 bitmask cases); O-C3-B-003 mutable set membership/add/remove/subset (4096 cases). Author mapping/content/answers/criteria checked; independent Chunk4 review pending. They fill aspects, not all file/set scope.

Current no-link objectives: {', '.join(no_links)}. Wider scope/difficulty gaps remain in code/bullet backlog; do not reduce gaps to these13. First-pass audit covers every exact statement/guidance, not all826 question contents. No full statement coverage is certified from counts.

Search works for persistent import, ID/code/topic/statement/guide/pasted-scope queries with limited concept aliases, all listed filters, paginated retrieval, separate answer/reviewer-rationale reveal, sources, duplicate candidates, six verification dimensions, history and reproducible selections.23 isolated functional and10 precision tests passed before handover; relocated restoration test report gives final evidence. Arbitrary-phrasing semantic recall, comprehensive reviewed question-type metadata, all per-question/bullet mapping and final responsive browser recheck remain incomplete. Known source-code typo lookup A.1.2.5→A1.2.5 needs search normalization work; exact normalized code works.

Known problems: alternative-answer rubric buckets; split words/identifiers; IP versus transport sequencing wording; standalone inherited context; repeated-object/count-domain ambiguity; some mismatched commands; unreviewed legacy scope links. Exact IDs/status/limits are in QA_ISSUES.md, audits/chunk-3/REVIEW_ISSUES.json and saved individual reviews. Mapping approval never clears a technical/criteria issue.

All3 specialist identities actually contributed, then reported usage-limit failures; no live/background work is assumed. Claude continues ONE AGENT. Exact next task: validate and merge the94 saved current-hash reviews awaiting integration, beginning with FULL_BANK_REVIEW_QUEUE.csv; independently sample technical/marking evidence and preserve issue states, then continue669 remaining historical reviews sequentially. Use existing partial independent SRC002 audit rather than repeating completed33 records.
""")
    put('NEXT_ACTIONS.md', """# Exact continuation sequence

1. Verify ZIP manifest or clone bundle. Read controlling CLAUDE.md/current progress. Active Chunk3; ONE AGENT. Never regenerate P-SRC or existing O-C3 IDs.
2. From actual project root, import canonical DB with explicit relocated `--root "$PWD"`; run stdlib search checks. Do not use developer DB as authority or old fixed-C2 validation generators as current validators.
3. Read audits/chunk-3/FULL_BANK_REVIEW_QUEUE.csv.94 saved reviews are not yet coordinator-approved; validate exact current review/record hashes and guide guidance before merging2–3 at a time. Existing33 independently rechecked SRC002 mappings are integrated; remaining independent audit queue is in agent-3-bank-audit/integration_review_SRC002.json and STATUS.json. Resume at its first pending ID rather than rechecking accepted records.
4. Review the669 historical records with no current detailed review, using the saved queue. Former A and B owner folders are historical organization only; Claude personally works sequentially. Author statuses, file assets, technical/answer/criteria/provenance checks remain separate. Read each whole prompt/answer/criteria and complete guide scope; record assessed aspects and explicit limits.
5. Resolve/report exact QA items; don't rewrite a record silently. Retain stable ID, old hash/version and correction reason, update student/answer/full record consistently, invalidate stale scope/verification, rerun necessary checks. Review near duplicates before selecting extra coverage.
6. Use CHUNK3_SCOPE_BACKLOG.csv/json for every objective/bullet and residual skills. Write genuinely original missing questions (especially actual Python construction), separate criteria and reproducible checks. Preserve original three IDs. Next unused reserved original ID is O-C3-B-004, after checking actual files.
7. Finish semantic recall and source-code-typo routing, reviewed type filters and responsive browser QA. Test exact code, broad topic, exact statement, exact bullet, multi-line pasted scope, partial matches, no-match scope, year/session/theme/level/marks/types/status, hidden answers and all-page retrieval. Do not widen conceptual equivalence to manufacture matches.
8. Refresh scope evidence, indexes, coverage, DB and checkpoints. Record remaining gaps honestly. Stop at Chunk3 completion. Chunk4/5 instructions are prepared for later explicit assignments; do not execute now.
""")
    put('QUESTION_BANK_GUIDE.md', f"""# Question bank guide

{commands}

QUESTION_BANK.csv is an index, not the question content. questions/ID.json contains student content, markschemes/ID.json separate preliminary criteria, records/ID.json the full internal provenance bundle. SQLite questions/answers also preserve full content; answer-bearing internal records are not exposed as public student payloads. Original IDs have no invented historical source links.

syllabus/SYLLABUS_MASTER.csv/.json and records/ contain official statement text/full guidance/level/source pages. Historical mapping/SYLLABUS_MAPPING.csv remains the source-question-to-guide ledger. Current mapping/SCOPE_MAPPING.csv and question-bank/scope_evidence.json add question-to-exact-guidance aspects, including originals and revised/narrowed matches. A supporting or rejected link is not a direct tested requirement. Keep legacy and reviewed mappings distinct.

Canonical local app is question-bank/search/, with question-bank/database.sqlite3. `question_codes` is candidate metadata. `scope_evidence` and `review_records` are current approved exact review snapshots. Import is transactional and incremental; usage, selections and independent manual verification survive unchanged import. Reviews need current record SHA, exact guide bullet, concrete skill/relevance/evidence and structured status. Withdrawn/revised source approvals revoke their supplied checks without erasing independent manual checks. `verification` and `verification_history` separate six dimensions. `review_history`, duplicate_groups, usage_history and selections support later audit/reproducibility. No selection itself generates an examination or marks question use.

Student queries support text/ID, exact code/topic, pasted scope, theme, common/HL/mixed, marks, difficulty, type, original year/session, 2027 target paper and verification. Answers hidden by default. Reviewer rationale/issues can reveal answers and have their own explicit reveal. Source PDFs are unchanged inventory references; the2 historical2026 papers have no supplied official markscheme. All adapted/new marking criteria remain unofficial/preliminary.

Run `python3 question-bank/search/test_db.py` and `python3 question-bank/search/test_semantic_precision.py` from project root. Tests use a temporary isolated DB; fixture questions are never inserted into the real bank. Query aliases are transparent and deliberately narrow; not an unrestricted semantic model. Canonical code has stricter fixes than historical agent-3 source. Read its README plus coordinator installation/QA notes before changing it.

To merge reviewed evidence, scripts/integrate_scope_reviews.py validates exact current hashes and needs an explicit coordinator approval reason. It currently loads A/B historical folders plus original-review-drafts/. Claude may keep those data paths but must record new review authorship honestly and adjust the collector ownership guard if personally authoring revisions as Claude; do not impersonate old agents. scripts/build_coverage_report.py, enrich_bank_index_chunk3.py, collect_chunk3_review_state.py and checkpoint_chunk3.py refresh derived reports. Old specialist first-pass scope audits remain historical inputs, so fix/extend their semantics carefully rather than pretending new questions were in the original audit.
""")
    put('CHUNK_1_INSTRUCTIONS.md', """# Chunk1 — historical completed foundation

Original purpose: inventory uploaded sources; extract/verify all individual 2027 HL syllabus statements and guidance; analyse both official HL specimen papers and corresponding criteria. Completed, not an instruction to restart.

Actual:48 PDF files inventoried,47 unique hashes; guide67 pages; specimen compilation154 pages; required HL P1/P2 Python/markschemes and case study present.112 statements:74 ThemeA and38 ThemeB,68 common and44 HL-only; exact wording/all271 guidance paragraphs, source pages, must/may limits and evidence preserved. Canonical normalized lookup A1.2.5 discloses printed A.1.2.5. SQL AVERAGE source spelling retained; executable dialect uses proper verified syntax. Recursion/access-control cautions retained.

Read syllabus/SCOPE_VERIFICATION.md, SYLLABUS_MASTER, specimen/SPECIMEN_ANALYSIS.md and component/question manifests. P1 2h80marks56/24 and pre-seen case/four HL challenges; P2 2h80 Python, compulsory plus non-code algorithmic thinking. Specimen's language options are not old subject options. Marking conventions include independent positive points, valid alternatives and local markbands. Source code defects were documented, not copied as true. Foundation commit46e2823 and original PROGRESS_CHUNK_1_ARCHIVE.md record completion.

Use these verified outputs. Reopen original pages only for relevant uncertainty/QA; do not re-extract whole sources or discard existing scope records. Do not treat historical coverage links as proof of every bullet.
""")
    put('CHUNK_2_INSTRUCTIONS.md', """# Chunk2 — historical completed extraction/conversion

Original purpose: extract every historical question/subquestion/visual/code/mark; map exact2027 scope; classify A direct/B adaptable/C obsolete; adapt usable material into original unofficial practice wording with separate preliminary criteria. Completed atdd5285c; do not repeat generators over repaired records.

Actual:23 distinct exams processed,0 remaining;1141 marked source leaves/3330 original marks;838 mapped (383A/455B);303 C exclusions with reasons;823 adapted practice records;15 explicit reuse links;1418 historical mapping rows including exclusions;152 batch handoffs. All old options were considered by exact guide scope, not assumed to carry forward.93 normalized source-text match groups remain candidates for contextual duplicate review. All823 are preserved.

48 original/project-copy hashes verified; SRC045 duplicates044; SRC047 alternative scan omits a confirmed blank page and is not processed twice. SRC001/002 scanned2026 sources have no uploaded matching official markschemes. Their new criteria are explicitly independently authored unofficial, not official. Source defects and repaired code/SQL checks are in audits/chunk-2. Stable H-SRC... source and P-SRC... practice IDs/provenance survive.

Read extraction/README.md, HISTORICAL_MANIFEST, HISTORICAL_QUESTION_INDEX, by-paper records, question-bank records/questions/markschemes, SYLLABUS_MAPPING.csv, C2 final validation/reports/approved snapshots. Chunk2 code/SQL/schema/source-mark checks passed within their documented limits; later C3 review has found explicit additional wording/criteria/scope issues. Do not reinterpret old author checks as C4 independent verification. Preserve defects/revisions rather than silently regenerating.
""")
    put('CHUNK_3_INSTRUCTIONS.md', f"""# Chunk3 — complete permanent bank/search/coverage

{common}

The bank currently has826 questions. Preserve all823 adapted records and3 original IDs. Complete detailed question-to-statement and bullet evidence; review all remaining saved/unsaved queues; design genuinely original missing questions only after checking existing coverage. Every applicable common and HL-only scope is required. Full text, code/tables/diagrams/subquestions, marks, difficulty/type, original provenance or honest original status, exact scope, separate answers/criteria and granular verification must be retrievable.

Use the guide in full, Paper1 specimen style for ThemeA and Python Paper2 style for ThemeB. For every applicable construct objective, include real Python-writing questions as well as appropriate tracing/explanation/debugging. Cover functions/parameters/returns, selection, loops, searches/sorts, simple non-branching recursive code, files, classes/methods, accurate encapsulation/inheritance/polymorphism and HL ADTs where exact guidance supports them. Do not impose arbitrary function bans; state task-specific algorithm restrictions when needed. Test code/output/edge cases and supported complexity claims; alternatives/partial criteria remain unofficial.

Search must accept code/topic/statement/bullet/pasted scope/keyword with actual reviewed meaning, separate direct/partial/candidate results, assessed aspects and unestablished requirements. Test every filter and full pagination. A narrow matching engine is implemented but arbitrary wording recall is incomplete. Support stable IDs, incremental addition, provenance, independent status updates/history, duplicate candidates and usage/selection metadata. Do not implement full exam assembly here.

Completion gates: all corpus records preserved/current links intact; all112 statements and important scope covered meaningfully with residual gaps resolved or honestly reported; adequate varied original questions where required; exact scoped retrieval tested; separate hidden answers; current statuses/QA; complete documentation/checkpoints. A declaration requires evidence, not counts. No examinations, topic tests or PDFs in Chunk3. Stop when genuinely complete.
""")
    # Full user-written future-stage instructions are kept standalone and exact.
    c4 = source_request.split('# CHUNK 4 — COMPLETE QUESTION BANK VERIFICATION',1)[1].split('# CHUNK 5 — MAXIMUM EXAMINATION GENERATION AND QUALITY RANKING',1)[0]
    c5 = source_request.split('# CHUNK 5 — MAXIMUM EXAMINATION GENERATION AND QUALITY RANKING',1)[1].split('# DATA INTEGRITY CHECK BEFORE HANDOVER',1)[0]
    put('CHUNK_4_INSTRUCTIONS.md', '# Chunk4 — full question-bank independent verification (future only)\n\n'+common+'\n\nStart only after completed Chunk3 and explicit user assignment. Do not execute during current handover. Retain stable IDs, old versions/hashes, correction reason and audit trail; invalidate and recheck dependent mappings/answers on changes. Canonical files and known QA are described in QUESTION_BANK_GUIDE.md.\n\n'+c4)
    put('CHUNK_5_INSTRUCTIONS.md', '# Chunk5 — mass examinations and ranking (future only)\n\n'+common+'\n\nStart only after full bank verification in Chunk4 and explicit user assignment. Do not execute now. Source guide/specimen authority remains binding. Paper1 case study has four HL research challenge questions; specimen SectionB assesses those challenges through multipart questions, not necessarily exactly four separately numbered exam questions. Verify this distinction against SPECIMEN_ANALYSIS.md and originals before assembly. Full response code in Paper2 is Python.\n\n'+c5)
    rubric = source_request.split('## 100-point quality rubric',1)[1].split('## Separate leaderboards',1)[0]
    put('EXAM_QUALITY_RUBRIC.md', '# Future exam quality rubric — not executed\n\n'+rubric+'\n\nScore from saved evidence, not generation order. This is an internal judgment, not an official IB grade, accuracy percentage or prediction of a future paper. Critical unresolved defects prohibit ranking.')
    ranking = source_request.split('## Separate leaderboards',1)[1].split('# DATA INTEGRITY CHECK BEFORE HANDOVER',1)[0]
    put('EXAM_RANKING_SYSTEM.md', '# Future ranking system — Chunk5 only\n\nUse EXAM_QUALITY_RUBRIC.md weights20+15+25+15+10+10+5=100. Only fully verified papers with no critical defects are eligible. Rank by total, then answer correctness, syllabus accuracy and structure. Keep separate Paper1/Paper2 leaderboards, top10 displays without a total-production cap.\n\n'+ranking)
    put('VERIFICATION_REQUIREMENTS.md', """# Verification requirements

For every question: exact statement/all guidance/level; actual demanded knowledge rather than topic mention; command/difficulty/mark depth; full self-contained text/subquestions/data/assets/code; technical correctness; complete answer; mark-by-mark criteria and cap; alternatives/partial credit; valid Python/domain/edge cases and relevant algorithm time/space reasoning; source file/session/page/Q/part or honest original authorship; links/IDs/duplicate relationships; saved checks and current content hashes.

Keep six mutable dimensions distinct: mapping, technical, answer, markscheme, assets, provenance. Mark pending/issue/stale where appropriate and give evidence. Original questions have no invented historical references; provenance can verify original authorship. Author verification is not independent Chunk4 verification. Do not clear a marking ambiguity merely because code executes or scope mapping is accepted.

Python checks should use independent expected results/oracles where feasible, including empty/singleton/boundary/duplicate/invalid-domain handling when actually in the prompt's domain, plus input mutation/aliasing and object identity where relevant. Do not demand out-of-domain inputs without changing the question contract. Preserve source defects separately. All generated criteria are unofficial.

Current semantic regression guards prohibit conflating encapsulation with hiding, generic for with counted, generic while with pre-test, or slope/intercept with the whole regression topic. Exact guide scope may be broader than a tested aspect; show what remains unsupported. All source documents unchanged. Future PDFs only in authorized Chunk5: render and inspect every page for clipping, missing data/figures, code legibility, numbering and answer leakage; student/markscheme PDFs separate.
""")
    put('RESUME_PROMPT.md', """Open this repository or extracted complete Claude handover. Read CLAUDE.md, CURRENT_PROGRESS.md, NEXT_ACTIONS.md, then the actual IB-CS-HL-2027 project progress, question database, coverage and QA. Work as ONE AGENT: do not create subagents or delegate. Confirm active Chunk3 is incomplete and preserve all826 current questions (823 adapted plus3 originals), their stable IDs, answers, mappings and history. Resume the exact saved queue/checkpoint; do not restart Chunk1 or2 or repeat completed reviews. Finish missing Chunk3 scope mappings, genuine original Python construction/gap questions, precise search/retrieval and documentation. Save atomically after2–3 questions, update progress/verification and commit verified milestones. Stop at Chunk3 completion and report evidence. Start Chunk4 only after Chunk3 is complete and I assign it; fully verify/correct every bank record without exams. Start Chunk5 only after Chunk4 is complete and I assign it; repeatedly generate many distinct verified Paper1/Paper2 exams, create/verify new questions when the bank is short, and rank eligible papers with the100-point rubric. Never promise automatic background continuation. Begin by checking actual files and counts, not trusting a past summary.""")
    put('REPOSITORY_SETUP.md', """# Restore history / publish privately later

The existing Git history was retained at workspace root.26aa6de is the repository-first full-state preservation commit. No authenticated creation/push path was available: connector read identity succeeded but exposes no create-repository tool, `gh` absent, browser creation redirected to sign-in. No remote was created and no repository URL is claimed. Final actual commit/bundle status is REPOSITORY_STATUS.json.

To restore full Git history independently of GitHub:

```sh
git clone ib-computer-science-hl-2027-question-bank.bundle ib-computer-science-hl-2027-question-bank
cd ib-computer-science-hl-2027-question-bank
git log -5 --oneline
```

The bundle is at the handover root after packaging. To run from the ZIP alone use PROJECT_FILES/IB-CS-HL-2027 and re-import with explicit relocated root, as in00_READ_FIRST. Do not copy old absolute original-source paths into run commands; all48 available project-copy source PDFs are included with relative paths. Both missing2026 source markschemes were unavailable originally and cannot be restored from this archive.

For later GitHub publishing, sign in, create an EMPTY **PRIVATE** repository named `ib-computer-science-hl-2027-question-bank` with no new README/license/history. Confirm private visibility. In the restored root run `git remote add origin <actual-private-repository-URL>` (or set-url an existing remote only after checking it), then `git push -u origin main`. Do not publish publicly. Do not force-push over unrelated history. Verify the remote default branch points to the final local commit and remains private. User supplies actual authenticated credentials; no secrets are included. No LFS required: current required file contents are included and each file is below90MiB. The ZIP and its nested Git bundle are excluded from the repo to avoid recursive archives; handover instructions and actual project files are committed.
""")
    # Detailed residual code/bullet backlog. Evidence is not converted to whole
    # coverage, and no Java-only requirement is added to the Python bank.
    backlog=[]
    for obj in cover['objectives']:
        code=obj['code'];ids=sorted(set(obj['candidate_question_ids'])|set(obj.get('reviewed_question_ids',[])))
        for bullet in obj['bullets']:
            text=bullet['exact_guidance'];java_only=text.startswith('• Classes for Java users')
            missing='; '.join(obj['missing_or_weak_requirements']) or 'No specific first-pass gap recorded; finish individual review and verify command/scope breadth and varied difficulty before certifying coverage.'
            if code=='B2.5.1':missing='Read/write/count/closing now assessed by O-C3-B-001. Append mode and appending to an existing file remain unassessed; broader application/difficulty still pending. Java-only helper examples do not require Java code.'
            if code=='B4.1.5':missing='O-C3-B-002/003 now assess uniqueness, union/intersection/difference and membership/add/remove/subset. Separate superset form and broader variation are not established; confirm exact required depth, do not infer hash mechanics from this statement.'
            if java_only:missing='Java-only may-include examples: not a Python code-writing gap. Preserve exact official guidance; do not generate Java questions.'
            construct=code.startswith('B') and obj['statement'].startswith('Construct')
            qtype='Python code construction' if construct else 'SQL/ERD/logic representation construction as exact statement requires' if obj['statement'].startswith('Construct') else 'Applied explanation/comparison/evaluation at exact command depth'
            row={'syllabus_code':code,'learning_statement':obj['statement'],'scope_bullet_id':bullet['scope_bullet_id'],'exact_scope_bullet':text,'level':obj['level'],
                 'existing_question_ids':ids,'approved_direct_ids':bullet['direct_question_ids'],'approved_partial_ids':bullet['partial_question_ids'],
                 'knowledge_or_skill_not_sufficiently_tested_or_established':missing,
                 'required_question_type':qtype,'recommended_difficulty':'medium plus application/high-demand variant where supported; not an official difficulty label',
                 'code_construction_required_for_this_statement':construct and not java_only,
                 'additional_questions_recommended_provisionally':0 if java_only else 2 if not ids else 1,
                 'recommendation_limit':'Provisional design target, not a fixed bank quota; review existing candidates first, and combine genuine complementary scope without superficial variants.',
                 'existing_partial_work':obj['specialist_audit_path']+'; coverage/OBJECTIVE_COVERAGE.json; scope_evidence.json; FULL_BANK_REVIEW_QUEUE.csv',
                 'next_action':'No Java authoring; retain source guidance' if java_only else 'Finish saved/candidate per-question scope review, resolve flagged marking/technical issues, then create distinct missing aspects and execute/verify appropriate answers; checkpoint2–3 at a time.'}
            backlog.append(row)
    put('CHUNK3_SCOPE_BACKLOG.json',json.dumps({'rows':backlog,'limits':'Every271 exact guidance paragraph is retained. Rows are residual-review/design tasks, not proof that every paragraph needs a new question or that every cited gap belongs to that individual paragraph.'},indent=2,ensure_ascii=False))
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(backlog[0]));writer.writeheader();writer.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in row.items()} for row in backlog);put('CHUNK3_SCOPE_BACKLOG.csv',stream.getvalue())
    put('CHUNK_3_REMAINING_WORK.md', f"""# Chunk3 remaining work — not complete

Every remaining record review is enumerated in PROJECT_FILES/IB-CS-HL-2027/audits/chunk-3/FULL_BANK_REVIEW_QUEUE.csv:669 unsaved historical reviews;94 saved current-hash reviews pending integration. Complete them sequentially as ONE AGENT. Retain current technical/marking/provenance issues even when mapping is accepted. Partial independent SRC002 results have33 accepted/current reviews already integrated; continue only its listed pending IDs if additional independent checking is needed.

Every112 statement and271 exact guidance paragraph is in **CHUNK3_SCOPE_BACKLOG.csv/.json**. Each row records code, full statement, missing/weak scope or unestablished evidence, exact guidance, full existing IDs, direct/partial approved IDs, level, assessed gaps, required type, suggested difficulty, code-construction requirement, provisional additional-count recommendation, existing partial files and exact next action. Recommendations are not a claim that each row needs a new separate question; review candidate content first. Must/may examples remain exact and Java-only examples do not become Python requirements.

Current no-linked-question codes ({len(no_links)}): {', '.join(no_links)}. Prioritize genuine gaps in pipelining/scheduling/TCP-IP/topologies/addressing/routing/denormalization/feature-selection/dimensionality/CNN/problem-specifications/design-patterns/ADT mechanics, according to exact corresponding statement guidance. Wider code/bullet/difficulty gaps remain in the full backlog. File append and some set variations remain after3 new questions. No whole statement has been finally certified complete.

Other remaining tasks:

1. Adjudicate all reported issue entries in audits/chunk-3/REVIEW_ISSUES.json; apply versioned repairs without changing stable IDs unnecessarily. Some are potential literal-rubric ambiguities, not proven technical failures; do not overstate them.
2. Complete reviewed question-type classification ({candidate_typed} inferred candidates remain); preserve raw and approved metadata separately. Count true Python construction beyond the conservative90 explicit directives where relevant.
3. Complete granular per-record source/mapping/technical/answer/criteria/assets checks needed for author approval; original-PDF rechecks remain explicitly pending in many records. Leave C4 independent verification separate.
4. Add accurate source-spelling query normalization for guide typo A.1.2.5 to normalized A1.2.5. Preserve exact printed source code in stored evidence. Expand conceptual recall only with precise, tested equivalences and genuine scope evidence; no synthetic matches from keywords.
5. Test every requested code/topic/statement/bullet/pasted-section filter and all-page retrieval on the expanded live bank. Ensure reviewed metadata governs direct/partial matches, unmet scopes visible, and supporting/reject evidence not promoted. Final responsive layout and all default-hidden answer/rationale interactions require a fresh browser check; old screenshot showed overflow before repair.
6. Reconcile duplicates and source-reuse families; mark candidates honestly. Preserve usage and reproducible retrieval infrastructure without assembling tests/exams.
7. Update current coverage after each approved batch; initial first-pass statuses are historical baselines. Verify meaningful coverage and varied application difficulty per required statement/bullet before declaring Chunk3 complete.
8. Refresh master indexes, scope evidence, canonical DB, audit results, README and progress; verify portability and commit. Preserve bundle/history. Stop after Chunk3 and await explicit Chunk4 assignment. No examination/topic-test/PDF generation now.
""")
    put('DATA_INTEGRITY_REPORT.md', f"""# Data integrity report

Actual checks before packaging are in PROJECT_FILES/IB-CS-HL-2027/audits/handover/DATA_COUNTS_AND_CHECKS.json. Current counts:826 questions (823 adapted,3 original),826 full linked answers and826 nonempty preliminary criteria. Unique IDs/full prompt/answer identity and individual marking totals checked for all826 DB rows.2469 protected historical question/answer/full-record payload hashes remain unchanged. All48 project source PDF hashes match inventory. No missing external question asset path was found; inline code/Unicode diagrams remain subject to documented per-record rendering QA.

Canonical SQLite integrity_check=ok; incremental import preserved823 old rows and added3, then826 unchanged.63 approved scope reviews/117 links are exact/current; total154 specialist historical reviews plus3 original author reviews saved.94 saved reviews unmerged;669 historical records not yet individually reviewed. All826 await independent Chunk4 audit;39 all-six current author checks are not independent certification.90 explicit Python construction directives are a conservative prompt census with full evidence, not90 correctness approvals.

23 isolated functional tests and10 matching-precision regressions passed in canonical installed code; final relocated/snapshot checks are in PORTABILITY_VERIFICATION.json and ARCHIVE_VERIFICATION.json when generated. Source alias typo normalization and broad arbitrary-phrasing recall incomplete; final narrow-screen/browser audit pending. Actual normalized source-code ID and basic exact/topic/pasted retrieval work. No whole-statement coverage certification or exam/test/PDF generation is claimed.

Initial complete-state commit26aa6de preserved existing history. Initial inventory6694 durable files had2 older Git checkpoint notes still ignored; ignore exceptions were removed for final commit. No file over90MiB; no required LFS pointers. Credential-like-token/private-key pattern scan found0; credentials/caches/temporary artifacts are excluded. This is a pattern scan, not proof against every possible secret format. GitHub connector identity authenticated but create-repo capability absent, gh unavailable and browser creation required sign-in; remote creation/push **not completed**. No URL is invented.

All requested standalone instructions are created: single-agent Claude, completed Chunk1/2 history, active Chunk3/backlog, future full-bank Chunk4 verification, future iterative Chunk5 generation/new-question expansion and100-point ranking with critical-error gates. Examinations remain future work. The package's final manifest and archive tests, not this pre-packaging prose, provide the exact included-file/hash/CRC and bundle restoration evidence. Any later failure is recorded there and must be reported honestly.
""")
    put('FILE_MANIFEST.md', """# File manifest

The complete machine-readable PROJECT_FILE_MANIFEST.json and human PROJECT_FILE_MANIFEST.csv list every actual PROJECT_FILES payload with relative path, byte count and SHA-256. HANDOVER_FILE_MANIFEST.json inventories wrapper instructions/backlogs and the Git bundle. They are generated after final snapshot creation; neither replaces actual files. ARCHIVE_VERIFICATION.json records final ZIP CRC/path/count/hash checks and Git-bundle restoration checks.

PROJECT_FILES/ preserves repository-relative paths, including IB-CS-HL-2027/ actual project, rootAGENTS/CLAUDE/README and setup files. CLAUDE_HANDOVER wrapper documents sit beside PROJECT_FILES rather than recursively copying themselves. Full Git history is in ib-computer-science-hl-2027-question-bank.bundle, with restore commands in REPOSITORY_SETUP.md. The ZIP and generated PROJECT_FILES mirror are intentionally not committed recursively; canonical project and wrapper instructions are committed. Existing sources/evidence/checkpoints are retained, including database backups, rather than replaced by summaries.

Unavailable originals: uploaded matching official markschemes for SRC001/SRC002 were never supplied. No existing durable project data is intentionally omitted; only named caches/temporary files/credentials and redundant parent copies of PDFs already present byte-identically in project sources are excluded. Exact exclusions are in PACKAGE_BUILD_REPORT.json.
""")
    root_readme = f"""# ib-computer-science-hl-2027-question-bank

Private, unofficial IB Computer Science HL2027 question-bank project. Existing Git history preserved. Actual working project: IB-CS-HL-2027/. Start Claude continuation with CLAUDE.md and CLAUDE_HANDOVER/00_READ_FIRST.md. Active Chunk3 incomplete:826 questions, all823 adapted preserved plus3 originals. No examination generation now.

Canonical search and database are in IB-CS-HL-2027/question-bank/search/ and database.sqlite3. Read that README and CLAUDE_HANDOVER/QUESTION_BANK_GUIDE.md; import with relocated root before serving. Answers and answer-bearing review rationale are separate. Search is working but per-question scope review/semantic breadth/coverage remain unfinished. Author checks do not equal independent C4 approval.

This repository contains uploaded source copies and must remain private as requested. No remote URL is claimed; publishing instructions and actual status are in CLAUDE_HANDOVER/REPOSITORY_SETUP.md and REPOSITORY_STATUS.json. The portable ZIP includes the actual project, source files, databases and full Git bundle. Claude works ONE AGENT, sequentially, without subagents. Future Chunk4 verifies all bank records; future Chunk5 repeatedly generates/ranks distinct papers and can author/verify missing bank questions. Neither stage is executed here.
"""
    (R/'README.md').write_text(root_readme)
    put('DEPENDENCIES.md', """# Dependencies and portability

Search server/import/database/functional tests and original3 reference checks use Python standard library only. Use Python3.10+ and a sqlite3 build with FTS5. Browser needs ordinary modern JavaScript. No API keys, embeddings service, Codex tool, cloud connector or running account is needed for local search. Stored question code is never run by import/server.

Older source/PDF extraction verification scripts may additionally need pypdf, pdfplumber, Pillow, Poppler pdftoppm and macOS Swift/Vision OCR. Their exact original runtime is documented in IB-CS-HL-2027/audits/RUNTIME.md; that old absolute bundled-runtime location is not portable. Existing extracted/OCR/rendered evidence is included, so those scripts need not be rerun to resume Chunk3. Reproduce optional tools in a suitable local environment if reinspection is needed. No dependency cache or credentials is included. Chunk5 PDF authoring tools must be selected/verified then; no claim a PDF generator already exists.
""")
    db.close()
    apply_question_generation_instruction()
    print(json.dumps({'handover_markdown_files_created':len(list(H.glob('*.md'))),'structured_backlog_rows':len(backlog),'project_snapshot_status':'not yet copied; packaging follows final commit','counts':{k:counts[k] for k in ['questions','adapted','original','explicit_Python_construction_directives']}}))


if __name__=='__main__':main()
