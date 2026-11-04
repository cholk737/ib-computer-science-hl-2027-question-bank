"""Validate isolated C3 reviews and merge only coordinator-approved versions.

Inspection never promotes a review. After actually reading its evidence, the
coordinator can use --approve ID [ID ...] --reason 'specific review performed'.
Approval is tied to both the exact review JSON and current question-record hash.
Later review changes require a new coordinator check. No question is rewritten.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

P = Path(__file__).resolve().parents[1]
A = P / 'audits/chunk-3'
DIMENSIONS = {'mapping', 'technical', 'answer', 'markscheme', 'assets', 'provenance'}


def atomic(path, text):
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(text, encoding='utf-8')
    os.replace(temp, path)


def hashed(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def load_reviews():
    scope = {s['code']: s for s in json.loads((P / 'syllabus/SYLLABUS_MASTER.json').read_text())}
    reviews = {}
    errors = []
    paths = [P / 'agents/chunk-3/agent-2-theme-b/question_reviews.json']
    paths += sorted((P / 'agents/chunk-3/agent-1-theme-a/scope_reviews').glob('*.json'))
    # A can use a single wrapped file instead; duplicate IDs are never silently
    # overwritten if both formats are accidentally supplied.
    paths += [P / 'agents/chunk-3/agent-1-theme-a/question_reviews.json']
    for path in paths:
        if not path.exists():
            continue
        payload = json.loads(path.read_text())
        candidates = payload.get('reviews', [payload])
        for r in candidates:
            qid = r.get('question_id', '<missing ID>')
            try:
                assert qid not in reviews, 'duplicate specialist ownership'
                record_path = P / 'question-bank/records' / (qid + '.json')
                record = json.loads(record_path.read_text())
                assert record['question_id'] == qid
                assert hashlib.sha256(record_path.read_bytes()).hexdigest() == r['record_sha256'], 'stale reviewed question hash'
                assert r['reviewer'] and r['reviewed_at']
                assert DIMENSIONS <= r['verification'].keys(), 'missing verification dimension'
                assert isinstance(r['mappings'], list) and r['mappings'], 'no explicit reviewed mapping'
                for m in r['mappings']:
                    code = m['code']
                    assert code in scope, 'unknown syllabus code'
                    prefix, number = m['scope_bullet_id'].rsplit(':G', 1)
                    assert prefix == code and number.isdigit()
                    index = int(number) - 1
                    assert index >= 0 and index < len(scope[code]['guidance_paragraphs'])
                    assert m['exact_guidance'] == scope[code]['guidance_paragraphs'][index], 'changed or incorrect guidance text'
                    assert m['relevance'] in {'direct', 'partial', 'supporting', 'reject'}
                    assert m['assessed_skill'].strip() and m['evidence'].strip(), 'missing substantive evidence'
                reviews[qid] = {'review': r, 'source_path': str(path.relative_to(P)), 'review_sha256': hashed(r)}
            except (AssertionError, KeyError, ValueError, TypeError, OSError) as exc:
                errors.append({'question_id': qid, 'file': str(path.relative_to(P)), 'error': str(exc)})
    return reviews, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--approve', nargs='+', default=[])
    parser.add_argument('--reason')
    args = parser.parse_args()
    if args.approve and not args.reason:
        parser.error('--approve requires a concrete --reason after actual review')
    reviews, errors = load_reviews()
    approvals_path = A / 'SCOPE_REVIEW_APPROVALS.json'
    approvals = json.loads(approvals_path.read_text()) if approvals_path.exists() else {'approvals': {}}
    now = datetime.now(ZoneInfo('Europe/Zurich')).isoformat()
    if args.approve:
        for qid in args.approve:
            assert qid in reviews, 'Review is missing or invalid: ' + qid
            candidate = reviews[qid]
            approvals['approvals'][qid] = {
                'question_id': qid, 'review_sha256': candidate['review_sha256'],
                'record_sha256': candidate['review']['record_sha256'],
                'source_path': candidate['source_path'], 'coordinator': '/root',
                'reviewed_at': now, 'reason': args.reason,
                'limits': 'Coordinator checked the concrete evidence; this is not the later independent Chunk 4 audit.',
            }
        atomic(approvals_path, json.dumps(approvals, indent=2) + '\n')
    merged, stale = [], []
    for qid, approval in sorted(approvals['approvals'].items()):
        candidate = reviews.get(qid)
        if not candidate or candidate['review_sha256'] != approval['review_sha256']:
            stale.append(qid)
            continue
        r = dict(candidate['review'])
        r['coordinator_review'] = approval
        merged.append(r)
    output = {
        'schema_version': 1, 'unofficial': True, 'updated_at': now,
        'scope_bullet_id_rule': 'CODE:GNN is the one-based exact guidance paragraph. Direct relevance certifies the described assessed skill, never every item in the paragraph.',
        'reviews': merged,
        'verification_limits': 'Only coordinator-approved, current-record specialist reviews are merged. Other bank records retain legacy status and are pending detailed C3 scope verification. C4 independent verification remains separate.',
    }
    atomic(P / 'question-bank/scope_evidence.json', json.dumps(output, indent=2, ensure_ascii=False) + '\n')
    columns = ['question_id', 'syllabus_code', 'scope_bullet_id', 'exact_guidance', 'assessed_skill', 'relevance', 'coverage_limit', 'evidence', 'reviewer', 'reviewed_at', 'record_sha256', 'mapping_status', 'coordinator_status']
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=columns)
    writer.writeheader()
    for r in merged:
        status = r['verification']['mapping']
        status = status.get('status') if isinstance(status, dict) else status
        for m in r['mappings']:
            writer.writerow({
                'question_id': r['question_id'], 'syllabus_code': m['code'],
                'scope_bullet_id': m['scope_bullet_id'], 'exact_guidance': m['exact_guidance'],
                'assessed_skill': m['assessed_skill'], 'relevance': m['relevance'],
                'coverage_limit': m.get('coverage_limit', ''), 'evidence': m['evidence'],
                'reviewer': r['reviewer'], 'reviewed_at': r['reviewed_at'],
                'record_sha256': r['record_sha256'], 'mapping_status': status,
                'coordinator_status': 'approved_current_review; C4 independent audit pending',
            })
    atomic(P / 'mapping/SCOPE_MAPPING.csv', stream.getvalue())
    report = {
        'saved_at': now, 'valid_specialist_reviews': len(reviews),
        'approved_current_reviews': len(merged), 'unapproved_ids': sorted(set(reviews) - {r['question_id'] for r in merged}),
        'invalid_reviews': errors, 'stale_approval_ids': stale,
        'merged_mapping_rows': sum(len(r['mappings']) for r in merged),
    }
    atomic(A / 'SCOPE_INTEGRATION_STATUS.json', json.dumps(report, indent=2) + '\n')
    print(json.dumps({**{k: v for k, v in report.items() if k != 'unapproved_ids'},
                      'unapproved_count': len(report['unapproved_ids'])}, indent=2))


if __name__ == '__main__':
    main()
