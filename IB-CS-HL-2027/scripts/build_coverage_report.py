"""Coordinator integration of exact first-pass audits and approved scope evidence.

This reports limits as well as evidence. A direct link never means that an
entire guidance paragraph, topic or learning statement has been satisfied.
"""
from pathlib import Path
import collections
import csv
import hashlib
import io
import json
import os

P = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def atomic(path, data):
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(data, encoding='utf-8')
    os.replace(temp, path)


def main():
    scope = read(P / 'syllabus/SYLLABUS_MASTER.json')
    a_path = P / 'agents/chunk-3/agent-1-theme-a/coverage_audit.json'
    b_path = P / 'agents/chunk-3/agent-2-theme-b/coverage_audit.json'
    a = read(a_path)['objectives']
    b = read(b_path)
    audited = {r['code']: r for r in a + b}
    assert len(audited) == len(scope) == 112
    bank = {p.stem: read(p) for p in (P / 'question-bank/records').glob('*.json')}
    evidence_path = P / 'question-bank/scope_evidence.json'
    evidence = read(evidence_path)['reviews'] if evidence_path.exists() else []
    by_bullet = collections.defaultdict(list)
    for review in evidence:
        qid = review['question_id']
        assert hashlib.sha256((P / f'question-bank/records/{qid}.json').read_bytes()).hexdigest() == review['record_sha256']
        status = review['verification']['mapping']
        status = status.get('status') if isinstance(status, dict) else status
        if status != 'verified':
            continue
        for mapping in review['mappings']:
            by_bullet[mapping['scope_bullet_id']].append({'question_id': qid, **mapping})
    details = []
    csv_rows = []
    for s in scope:
        audit = audited[s['code']]
        assert audit['statement'] == s['statement']
        assert audit['guidance_paragraphs'] == s['guidance_paragraphs']
        assert audit['level'] == s['level']
        assert audit.get('review_status', audit.get('manual_check_status')) not in (None, 'pending_manual_review')
        legacy = [q for q in bank.values() if s['code'] in q['syllabus_codes']]
        reviewed_ids = {r['question_id'] for links in by_bullet.values() for r in links
                        if r['code'] == s['code'] and r['relevance'] in ('direct', 'partial')}
        retrieval_ids = {q['question_id'] for q in legacy} | reviewed_ids
        difficulty = dict(collections.Counter(bank[qid]['difficulty'] for qid in retrieval_ids))
        raw_status = audit.get('coverage_status', audit.get('status'))
        gaps = audit.get('remaining_gaps', audit.get('gaps', []))
        item = {
            'code': s['code'], 'source_code': s['source_code'], 'statement': s['statement'],
            'theme': s['theme'], 'topic': s['topic'], 'level': s['level'],
            'source_pdf_pages': s['source_pdf_pages'], 'guidance_paragraphs': s['guidance_paragraphs'],
            'scope_qualifications': s['scope_qualifications'], 'global_scope_note': s['global_scope_note'],
            'assessable_knowledge_skills': s['assessable_knowledge_skills'],
            'first_pass_status': raw_status, 'missing_or_weak_requirements': gaps,
            'candidate_question_ids': sorted(q['question_id'] for q in legacy),
            'reviewed_question_ids': sorted(reviewed_ids),
            'difficulty_distribution': difficulty,
            'specialist_audit_path': str((a_path if s['theme'] == 'A' else b_path).relative_to(P)),
            'specialist_findings': audit.get('bullet_findings', []), 'bullets': [],
            'verification_status': 'exact_master_text_checked; specialist_first_pass; exhaustive_question_review_in_progress; no_full_coverage_certification',
        }
        for i, guidance in enumerate(s['guidance_paragraphs'], 1):
            bid = f'{s["code"]}:G{i:02d}'
            links = by_bullet.get(bid, [])
            # A specialist must explicitly state what was tested and any limit.
            # A whole paragraph's examples are not silently assigned to a question.
            direct = sorted({m['question_id'] for m in links if m['relevance'] == 'direct'})
            partial = sorted({m['question_id'] for m in links if m['relevance'] == 'partial'})
            supporting = sorted({m['question_id'] for m in links if m['relevance'] == 'supporting'})
            bullet_status = 'reviewed_aspect_evidence_only' if direct or partial else 'no_approved_direct_aspect_evidence_yet'
            source_ids = sorted({sid for qid in direct + partial for sid in bank[qid].get('source_question_ids', [])})
            bullet = {'scope_bullet_id': bid, 'exact_guidance': guidance, 'status': bullet_status,
                      'direct_question_ids': direct, 'partial_question_ids': partial,
                      'supporting_question_ids': supporting, 'reviewed_assessed_skills': links,
                      'coverage_limit': 'Full paragraph coverage is not certified. Unreviewed candidates and residual first-pass gaps require further checking.'}
            item['bullets'].append(bullet)
            csv_rows.append({
                'syllabus_code': s['code'], 'scope_bullet_reference': bid,
                'source_question_ids': json.dumps(source_ids), 'practice_question_ids': json.dumps(direct + partial),
                'coverage_status': bullet_status, 'difficulty_distribution': json.dumps(difficulty),
                'verification_status': item['verification_status'], 'statement': s['statement'],
                'scope_guidance': guidance, 'theme': s['theme'], 'topic': s['topic'], 'level': s['level'],
                'source_pdf_pages': json.dumps(s['source_pdf_pages']), 'candidate_question_ids': json.dumps(item['candidate_question_ids']),
                'supporting_question_ids': json.dumps(supporting), 'first_pass_status': raw_status,
                'missing_requirements': json.dumps(gaps, ensure_ascii=False),
                'assessed_skill_evidence': json.dumps(links, ensure_ascii=False),
            })
        details.append(item)
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(csv_rows[0]))
    writer.writeheader()
    writer.writerows(csv_rows)
    atomic(P / 'coverage/COVERAGE_REPORT.csv', stream.getvalue())
    result = {
        'schema_version': 1, 'unofficial': True, 'statement_count': len(details),
        'guidance_paragraph_count': len(csv_rows), 'fully_covered_statements_certified': 0,
        'limits': 'First-pass audits identify evidence/gaps. Approved per-question direct/partial links identify named assessed aspects, not every element in a paragraph. This is not a claim that all 112 statements are covered.',
        'first_pass_status_counts': dict(collections.Counter(r['first_pass_status'] for r in details)),
        'objectives': details,
    }
    atomic(P / 'coverage/OBJECTIVE_COVERAGE.json', json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    summary = {k: result[k] for k in result if k != 'objectives'}
    summary.update({'approved_scope_review_records': len(evidence), 'bullets_with_direct_or_partial_evidence': sum(bool(r['practice_question_ids'] != '[]') for r in csv_rows)})
    atomic(P / 'audits/chunk-3/COVERAGE_INTEGRATION.json', json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
