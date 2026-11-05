#!/usr/bin/env python3
"""Retrieval checks for original Chunk 3 questions on an isolated copy of the live DB.

Checks every O-C3 record is searchable by its code, ID and reviewed scope; answers
stay hidden until requested; typo-routed codes equal normalized codes; filters
and full pagination return every original exactly once. The live DB is not modified.
"""
import json, shutil, tempfile
from pathlib import Path
import bank_db as b

HERE = Path(__file__).resolve().parent
LIVE = HERE.parent / 'database.sqlite3'
checks = []
with tempfile.TemporaryDirectory() as td:
    copy = Path(td) / 'copy.sqlite3'; shutil.copy(LIVE, copy); db = b.connect(copy)
    originals = [r[0] for r in db.execute("SELECT question_id FROM questions WHERE question_id LIKE 'O-C3-%' ORDER BY question_id")]
    assert len(originals) >= 24, len(originals)
    for qid in originals:
        q = b.detail(db, qid)
        assert not {'answer', 'solution', 'marking_points'} & q.keys(), qid
        answer = b.detail(db, qid, include_answer=True)['answer']
        assert sum(p['marks'] for p in answer['marking_points']) == q['marks'], qid
        assert q['verification']['mapping']['status'] == 'verified' and q['reviewed_syllabus_codes'], qid
        for code in q['reviewed_syllabus_codes']:
            res = b.search(db, {'code': code, 'limit': 1000})
            assert qid in {x['question_id'] for x in res['questions']}, (qid, code)
        assert [x['question_id'] for x in b.search(db, {'text': qid})['questions']] == [qid], qid
    checks.append({'name': 'every original searchable by reviewed code and ID; answers hidden by default and complete on request', 'count': len(originals)})
    gap = 'A1.1.6 A1.3.3 A2.1.5 A2.2.1 A2.3.1 A2.3.4 A3.2.7 A4.2.2 A4.2.3 A4.3.9 B1.1.1 B3.2.5 B4.1.6'.split()
    for code in gap:
        res = b.search(db, {'code': code}); assert res['total'] >= 1 and res['checked_count'] >= 1, code
    checks.append({'name': 'all 13 handover no-link codes now return a reviewed (checked) match', 'codes': gap})
    for raw, norm in [('A.1.2.5', 'A1.2.5'), ('B.4.1.6', 'B4.1.6')]:
        for key in ('code', 'text', 'scope_text'):
            ids = lambda f: sorted(x['question_id'] for x in b.search(db, {key: f, 'limit': 1000})['questions'])
            assert ids(raw) == ids(norm) and ids(norm), (raw, key)
    checks.append({'name': 'printed source-code typo routes (A.1.2.5, B.4.1.6) equal normalized code results for code/text/scope_text'})
    for theme in 'AB':
        res = b.search(db, {'code': '', 'text': '', 'theme': theme, 'limit': 1000, 'offset': 0})
        seen, offset = [], 0
        while True:
            page = b.search(db, {'theme': theme, 'limit': 50, 'offset': offset})
            seen += [x['question_id'] for x in page['questions']]
            offset += 50
            if offset >= page['total']: break
        assert len(seen) == len(set(seen)) == page['total'], theme
        want = {q for q in originals if q.startswith(f'O-C3-{theme}-')}
        assert want <= set(seen), theme
    checks.append({'name': 'theme filters with full pagination return each record once, including all originals'})
    res = b.search(db, {'question_type': 'Python code construction', 'limit': 1000})
    assert {'O-C3-B-006', 'O-C3-B-007', 'O-C3-B-008'} <= {x['question_id'] for x in res['questions']}
    checks.append({'name': 'question_type filter returns the new Python construction originals'})
(HERE / 'c3_originals_test_results.json').write_text(json.dumps({'suite': 'c3-originals-retrieval', 'passed': len(checks), 'failed': 0, 'checks': checks}, indent=2) + '\n')
print(json.dumps({'passed': len(checks), 'failed': 0}))
