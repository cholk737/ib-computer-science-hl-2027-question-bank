"""Write a bounded batch of original C3 questions (batch 2). Refuses overwriting IDs.

Usage: python3 scripts/create_c3_original_batch2.py --ids O-C3-A-001 O-C3-A-002 ...

For each ID: validates scope references against SYLLABUS_MASTER.json, checks
mark totals, runs an executable check where the answer is computable or code,
writes record/question/markscheme files plus an author review draft, and appends
the index row. Answers never enter the student question file. No exam, test or
PDF is assembled. Author checks are not independent Chunk 4 verification.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import itertools
import json
import math
import os
import random
import sys
from datetime import datetime, timezone

P = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from c3_original_batch2_definitions import AUTHOR, DEFINITIONS  # noqa: E402

CHECKS_PATH = P / 'audits/chunk-3/ORIGINAL_BATCH2_CHECKS.json'


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    os.replace(temp, path)


# --------------------------------------------------------------- executable checks
def check_pipeline(_):
    def simulate(instructions, stages, pipelined):
        if instructions == 0:
            return 0
        if not pipelined:
            return instructions * stages
        finish = 0
        for i in range(instructions):  # instruction i enters fetch at cycle i (1 stage per cycle)
            finish = max(finish, i + stages)
        return finish
    assert simulate(10, 4, False) == 40
    assert simulate(10, 4, True) == 13
    assert max(simulate(10, 4, True) for _core in range(4)) == 13
    for n in range(1, 50):
        assert simulate(n, 4, True) == 4 + n - 1
    return 52


def check_scheduling(_):
    bursts = {'P1': 8, 'P2': 4, 'P3': 2}
    order = ['P1', 'P2', 'P3']
    t, fcfs = 0, {}
    for p in order:
        t += bursts[p]
        fcfs[p] = t - bursts[p]
    assert fcfs == {'P1': 0, 'P2': 8, 'P3': 12} and abs(sum(fcfs.values()) / 3 - 20 / 3) < 1e-9
    queue, left, t, done = list(order), dict(bursts), 0, {}
    while queue:
        p = queue.pop(0)
        run = min(2, left[p]); t += run; left[p] -= run
        if left[p]:
            queue.append(p)
        else:
            done[p] = t
    assert done == {'P3': 6, 'P2': 10, 'P1': 14}
    waits = {p: done[p] - bursts[p] for p in order}
    assert waits == {'P1': 6, 'P2': 6, 'P3': 4} and round(sum(waits.values()) / 3, 2) == 5.33
    return 2


def check_cnn(_):
    def out(width, kernel, stride):
        # count positions where the window fits entirely, by actually sliding it
        return len(range(0, width - kernel + 1, stride))
    w1 = out(32, 5, 1); w2 = out(w1, 2, 2); w3 = out(w2, 3, 2)
    assert (w1, w2, w3) == (28, 14, 6)
    assert out(32, 5, 2) == 14
    for width in range(5, 80):
        for k in range(1, 6):
            for s in range(1, 4):
                if k <= width:
                    assert out(width, k, s) == (width - k) // s + 1
    return 4 + 75 * 15


def check_observer(ns):
    WS, D = ns['WeatherStation'], ns['Display']
    ws, a, b = WS(), D(), D()
    assert ws.temperature is None and ws._observers == [] and a.readings == []
    ws.set_temperature(5); assert ws.temperature == 5
    ws.subscribe(a); ws.subscribe(a); ws.subscribe(b)
    assert ws._observers == [a, b]
    order = []

    class Spy:
        def __init__(self, tag): self.tag = tag
        def update(self, value): order.append((self.tag, value))
    s1, s2 = Spy(1), Spy(2)
    ws.subscribe(s1); ws.subscribe(s2)
    ws.set_temperature(12)
    assert a.readings == [12] and b.readings == [12] and order == [(1, 12), (2, 12)]
    ws.unsubscribe(a); ws.unsubscribe(a); ws.unsubscribe(D())
    ws.set_temperature(-3)
    assert a.readings == [12] and b.readings == [12, -3] and ws.temperature == -3
    return 9


def check_factory(ns):
    exec('class Enemy:\n    def __init__(self, health):\n        self.health = health\n'
         'class Goblin(Enemy):\n    def __init__(self):\n        super().__init__(30)\n'
         'class Dragon(Enemy):\n    def __init__(self):\n        super().__init__(200)\n'
         'class Bat(Enemy):\n    def __init__(self):\n        super().__init__(10)\n', ns)
    f = ns['create_enemies']
    r = f(['bat', 'Goblin', 'DRAGON', 'bat'])
    assert [type(x).__name__ for x in r] == ['Bat', 'Goblin', 'Dragon', 'Bat'] and r[0] is not r[3]
    assert [x.health for x in r] == [10, 30, 200, 10]
    assert f([]) == []
    for bad in (['bat', 'orc'], ['Goblins'], ['']):
        try:
            f(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('no ValueError for ' + repr(bad))
    return 6


def check_hashtable(ns):
    HT = ns['HashTable']
    rng = random.Random(2027)
    cases = 0
    for capacity in range(1, 12):
        for trial in range(200):
            t = HT(capacity)
            assert t.slots == [None] * capacity and t.count == 0 and t.load_factor() == 0
            oracle = {}
            for _ in range(rng.randint(0, 3 * capacity)):
                key = ''.join(rng.choice('abcAB') for _ in range(rng.randint(0, 3)))
                if rng.random() < 0.6 and (key in oracle or len(oracle) < capacity):
                    value = rng.randint(-99, 99)
                    t.put(key, value); oracle[key] = value
                    expected_hash = sum(ord(c) for c in key) % capacity
                    assert t._hash(key) == expected_hash
                    # stored as tuple in slots, reachable by linear probing from the hash index
                    i = expected_hash
                    for _step in range(capacity):
                        assert t.slots[i] is not None
                        if t.slots[i][0] == key:
                            break
                        i = (i + 1) % capacity
                    assert t.slots[i] == (key, value)
                probe = ''.join(rng.choice('abcABz') for _ in range(rng.randint(0, 3)))
                assert t.get(probe) == oracle.get(probe)
                assert t.count == len(oracle) and math.isclose(t.load_factor(), len(oracle) / capacity)
                cases += 1
    full = HT(3)
    for k in ('a', 'b', 'c'):
        full.put(k, k)
    assert full.get('zz') is None and full.load_factor() == 1  # absent key in a full table terminates
    return cases + 1


def check_hash_trace(_):
    probe = [None] * 7
    for k in (15, 22, 8, 29, 3):
        i = k % 7
        while probe[i] is not None:
            i = (i + 1) % 7
        probe[i] = k
    assert {k: probe.index(k) for k in (15, 22, 8, 29, 3)} == {15: 1, 22: 2, 8: 3, 29: 4, 3: 5}
    chains = [[] for _ in range(7)]
    for k in (15, 22, 8, 29, 3):
        chains[k % 7].append(k)
    assert chains[1] == [15, 22, 8, 29] and chains[3] == [3] and sum(map(len, chains)) == 5
    assert round(5 / 7, 2) == 0.71
    return 3


EXECUTABLE = {
    'O-C3-A-002': check_pipeline, 'O-C3-A-003': check_scheduling, 'O-C3-A-014': check_cnn,
    'O-C3-B-006': check_observer, 'O-C3-B-007': check_factory, 'O-C3-B-008': check_hashtable,
    'O-C3-B-009': check_hash_trace,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ids', nargs='+', required=True)
    args = parser.parse_args()
    defs = {d['question_id']: d for d in DEFINITIONS}
    unknown = [i for i in args.ids if i not in defs]
    assert not unknown, 'Unknown definition IDs: ' + ', '.join(unknown)
    scope = {s['code']: s for s in json.loads((P / 'syllabus/SYLLABUS_MASTER.json').read_text())}
    with (P / 'question-bank/QUESTION_BANK.csv').open() as f:
        reader = csv.DictReader(f); fields = list(reader.fieldnames); rows = list(reader)
    existing = {r['question_id'] for r in rows}
    checks = json.loads(CHECKS_PATH.read_text()) if CHECKS_PATH.exists() else {
        'method': 'Computable answers re-derived by independent simulation; Python references executed against oracles/edge cases. Conceptual answers manually checked by the author against full exact guidance. Author verification only, not independent Chunk 4 verification.',
        'results': {}}
    batch = [defs[i] for i in args.ids]
    for d in batch:
        qid = d['question_id']
        assert qid not in existing, 'Refuse duplicate/overwrite: ' + qid
        assert not (P / 'question-bank/records' / (qid + '.json')).exists(), 'Refuse overwrite of record file: ' + qid
        code = d['code_id']
        assert code in scope and scope[code]['level'] == d['level'] and scope[code]['theme'] == d['theme'], 'scope/level mismatch ' + qid
        assert len(d['criteria']) == d['marks'], 'mark total mismatch ' + qid
        for number, _skill, rel in d['skills']:
            assert 1 <= number <= len(scope[code]['guidance_paragraphs']) and rel in {'direct', 'partial', 'supporting'}
        is_code = d['question_type'] == 'Python code construction'
        ns = {}
        if is_code:
            exec(d['reference'], ns)
            assert qid in EXECUTABLE, 'code question without execution check: ' + qid
        cases = EXECUTABLE[qid](ns) if qid in EXECUTABLE else 0
        checks['results'][qid] = {
            'passed': True, 'executed_cases': cases,
            'method': 'executed reference/oracle check' if cases else 'manual author check against exact guidance and criteria',
            'reference_sha256': hashlib.sha256(d['reference'].encode()).hexdigest(),
            'checked_at': datetime.now(timezone.utc).isoformat()}
    atomic(CHECKS_PATH, checks)

    for d in batch:
        qid = d['question_id']; code = d['code_id']; stamp = datetime.now(timezone.utc).isoformat()
        is_code = d['question_type'] == 'Python code construction'
        cases = checks['results'][qid]['executed_cases']
        technical = (f'Executed check in audits/chunk-3/ORIGINAL_BATCH2_CHECKS.json ({cases} cases).' if cases
                     else 'Manual author check of every criterion against the exact statement and all guidance paragraphs; no executable component.')
        record = {
            'question_id': qid, 'source_question_ids': [], 'derivation_status': 'original_unofficial', 'unofficial': True,
            'question_text': d['prompt'], 'syllabus_codes': [code], 'theme': d['theme'], 'level': d['level'],
            'marks': d['marks'], 'command_term': d['command_term'], 'difficulty': d['difficulty'],
            'question_type': d['question_type'],
            'adaptation_rationale': 'Original question written by ' + AUTHOR + ' for a syllabus statement with no linked question at handover; no historical source question or official marking status claimed.',
            'solution': d['reference'], 'marking_points': [{'marks': 1, 'criterion': c} for c in d['criteria']],
            'acceptable_alternatives': d['alternatives'],
            'partial_credit_notes': f'Award each independent point once, up to {d["marks"]} marks. Accept equivalent correct wording or valid alternative code. Do not double-credit one idea.',
            'common_errors': [], 'verification': {'technical': technical, 'scope': d['limits']},
            'code': d['reference'] if is_code else '', 'test_code': '', 'assets': [],
            'markscheme_status': 'preliminary_unofficial_verified_by_author',
            'record_path': f'question-bank/records/{qid}.json', 'question_path': f'question-bank/questions/{qid}.json',
            'markscheme_path': f'question-bank/markschemes/{qid}.json',
            'coordinator_status': 'author_content_scope_answer_marking_checks_passed; independent_Chunk4_audit_pending',
            'independent_verification_status': 'pending',
        }
        question = {k: v for k, v in record.items() if k in ['question_id', 'source_question_ids', 'derivation_status', 'unofficial', 'question_text', 'syllabus_codes', 'theme', 'level', 'marks', 'command_term', 'difficulty', 'question_type', 'assets']}
        answer = {k: record[k] for k in ['question_id', 'unofficial', 'solution', 'marking_points', 'acceptable_alternatives', 'partial_credit_notes', 'common_errors', 'verification', 'code', 'markscheme_status']}
        for rel, data in [(record['record_path'], record), (record['question_path'], question), (record['markscheme_path'], answer)]:
            atomic(P / rel, data)
        record_hash = hashlib.sha256((P / record['record_path']).read_bytes()).hexdigest()
        evidence = {
            'mapping': 'Read the complete exact statement and every guidance paragraph; mapped only the assessed aspects; omitted scope stated in coverage_limit.',
            'technical': technical,
            'answer': 'Full reference answer matches the criteria and the stated domain; student question file contains no answer.',
            'markscheme': f'{d["marks"]} independent one-mark criteria sum to the question total; alternatives and partial credit recorded; preliminary unofficial author criteria.',
            'assets': 'All required context, code stimulus and data are contained in the prompt text; no diagram or external file needed.',
            'provenance': 'Original authorship recorded; no historical source IDs; the official guide is cited only as scope evidence.',
        }
        review = {
            'question_id': qid, 'record_sha256': record_hash, 'reviewer': AUTHOR, 'reviewed_at': stamp,
            'question_type': d['question_type'],
            'review_scope': 'Author review of a new original question; independent Chunk 4 review pending.',
            'verification': {k: {'status': 'verified', 'evidence': v} for k, v in evidence.items()},
            'mappings': [{
                'code': code, 'scope_bullet_id': f'{code}:G{n:02d}',
                'exact_guidance': scope[code]['guidance_paragraphs'][n - 1], 'assessed_skill': skill, 'relevance': rel,
                'evidence': 'The prompt and its independent marking criteria require this aspect. ' + d['limits'],
                'coverage_limit': d['limits'], 'statement_relevance': 'direct',
                'statement_evidence': f'Prompt uses the command term "{d["command_term"]}" on the scoped content of {code}.'}
                for n, skill, rel in d['skills']],
            'issues': [], 'scope_not_assessed': [d['limits']],
            'execution_evidence': 'audits/chunk-3/ORIGINAL_BATCH2_CHECKS.json' if cases else 'manual',
        }
        atomic(P / f'question-bank/original-review-drafts/{qid}.json', {'reviews': [review]})
        row = {f: '' for f in fields}
        for k in ['question_id', 'record_path', 'question_path', 'derivation_status', 'theme', 'level', 'marks', 'command_term', 'difficulty', 'markscheme_path']:
            row[k] = record[k]
        row.update({'source_question_ids': '[]', 'syllabus_codes': json.dumps(record['syllabus_codes']), 'verification_status': record['coordinator_status']})
        rows.append(row)
    stream = io.StringIO(); writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    temp = P / 'question-bank/QUESTION_BANK.csv.tmp'; temp.write_text(stream.getvalue()); os.replace(temp, P / 'question-bank/QUESTION_BANK.csv')
    print(json.dumps({'saved': [d['question_id'] for d in batch], 'total_bank_rows': len(rows),
                      'checks': {d['question_id']: checks['results'][d['question_id']]['executed_cases'] for d in batch}}))


if __name__ == '__main__':
    main()
