"""Coordinator's durable full-bank review queue and issue index, without promotion."""
from pathlib import Path
import csv
import io
import json
import os
from integrate_scope_reviews import load_reviews

P = Path(__file__).resolve().parents[1]


def atomic(path, data):
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(data, encoding='utf-8')
    os.replace(temp, path)


def main():
    reviews, errors = load_reviews()
    approved_path = P / 'question-bank/scope_evidence.json'
    approved = {r['question_id']: r for r in json.loads(approved_path.read_text())['reviews']} if approved_path.exists() else {}
    bank = list(csv.DictReader((P / 'question-bank/QUESTION_BANK.csv').open()))
    queue, issues = [], []
    for row in bank:
        qid = row['question_id']
        candidate = reviews.get(qid)
        owner = '/root/theme_a_coverage' if row['theme'] == 'A' else '/root/theme_b_coverage'
        if row['derivation_status'] == 'original_unofficial':
            owner = '/root'
        if candidate:
            r = candidate['review']
            assert r['reviewer'] == owner, f'Wrong/overlapping writer for {qid}'
            for issue in r.get('issues', []):
                issues.append({'question_id': qid, 'reviewer': r['reviewer'], 'source_path': candidate['source_path'],
                               'issue': issue, 'coordinator_approved_review': qid in approved,
                               'status': 'unresolved_reported_finding; read exact review for limits; not an automatic content correction'})
        queue.append({'question_id': qid, 'owner': owner,
                      'specialist_review_status': 'saved_current_hash_valid' if candidate else 'pending',
                      'coordinator_status': 'approved_current' if qid in approved else 'pending',
                      'review_path': candidate['source_path'] if candidate else '',
                      'issue_count': len(candidate['review'].get('issues', [])) if candidate else '',
                      'next_action': 'Resolve explicit outstanding dimensions/issues; independent C4 audit later' if qid in approved else
                                     'Coordinator inspect saved evidence and approve exact version' if candidate else
                                     'Owning specialist read full prompt, exact statements/all guidance, answer/criteria and record actual per-aspect evidence'})
    assert len({r['question_id'] for r in queue}) == len(bank)
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(queue[0]))
    writer.writeheader()
    writer.writerows(queue)
    atomic(P / 'audits/chunk-3/FULL_BANK_REVIEW_QUEUE.csv', stream.getvalue())
    payload = {'question_count': len(bank), 'specialist_reviews_saved': len(reviews),
               'coordinator_reviews_approved': len(approved), 'individual_reviews_remaining': len(bank) - len(reviews),
               'invalid_review_files': errors, 'reported_issues': issues,
               'limits': 'Issue entries are saved reported findings. Approval of mapping evidence does not clear a technical or marking issue; dimensions remain distinct.'}
    atomic(P / 'audits/chunk-3/REVIEW_ISSUES.json', json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    qa = P / 'QA_ISSUES.md'
    text = qa.read_text()
    start, end = '<!-- C3-REVIEW-STATE-START -->', '<!-- C3-REVIEW-STATE-END -->'
    section = '\n'.join([start, '### Current individual-review queue and reported issues', '',
                          f'- {len(reviews)}/{len(bank)} per-question reviews saved with valid current hashes; {len(approved)} coordinator-approved versions; {len(bank)-len(reviews)} individual reviews remaining.',
                          f'- {len(issues)} reported issue entries, all still explicit unresolved findings unless a later repair log says otherwise. Scope approval does not clear marking/technical issues.',
                          '- Full durable queue: `audits/chunk-3/FULL_BANK_REVIEW_QUEUE.csv`.',
                          '- Exact question IDs, issue details, author paths and review limits: `audits/chunk-3/REVIEW_ISSUES.json` and each specialist review.',
                          '- Historical prompts/criteria remain preserved. Do not present a reported ambiguity as an unconditional code defect; read its domain qualification.',
                          end])
    if start in text:
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        text = before + section + after
    else:
        text += '\n\n' + section + '\n'
    atomic(qa, text)
    print(json.dumps({k: v for k, v in payload.items() if k != 'reported_issues'}))


if __name__ == '__main__':
    main()
