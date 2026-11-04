"""Append C3 retrieval metadata to the index without changing question records.

Legacy C2 verification is preserved separately from the new review dimensions.
The SQLite verification/usage tables remain the live, updateable authority.
"""
from pathlib import Path
import csv
import io
import json
import os

P = Path(__file__).resolve().parents[1]


def main():
    path = P / 'question-bank/QUESTION_BANK.csv'
    with path.open() as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        rows = list(reader)
    scope = {r['code']: r for r in json.loads((P / 'syllabus/SYLLABUS_MASTER.json').read_text())}
    evidence_path = P / 'question-bank/scope_evidence.json'
    evidence = {r['question_id']: r for r in json.loads(evidence_path.read_text())['reviews']} if evidence_path.exists() else {}
    source_index = {r['source_question_id']: r for f in (P / 'extraction/by-paper').glob('*/questions/*.json') for r in [json.loads(f.read_text())]}
    added = ['legacy_verification_status', 'topics', 'target_papers', 'source_years', 'source_sessions', 'historical_papers',
             'question_type', 'question_type_basis', 'scope_evidence_path', 'reviewed_scope_bullet_ids',
             'syllabus_verification_status', 'technical_verification_status', 'answer_verification_status',
             'markscheme_verification_status', 'asset_verification_status', 'provenance_verification_status',
             'verification_record_reference', 'usage_history_reference', 'outstanding_review_issues', 'reviewed_syllabus_codes']
    fields += [f for f in added if f not in fields]
    for row in rows:
        record = json.loads((P / row['record_path']).read_text())
        codes = record['syllabus_codes']
        sources = [source_index[s] for s in record.get('source_question_ids', [])]
        review = evidence.get(row['question_id'])
        reviewed_codes = {m['code'] for m in review['mappings'] if m['relevance'] in ('direct', 'partial')} if review else set()
        retrieval_codes = set(codes) | reviewed_codes
        # Original C2 verification_status remains untouched; make its meaning
        # explicit in a second column for readers of either index generation.
        row['legacy_verification_status'] = row.get('legacy_verification_status') or row['verification_status']
        row['reviewed_syllabus_codes'] = json.dumps(sorted(reviewed_codes))
        row['topics'] = json.dumps(sorted({scope[c]['topic'] for c in retrieval_codes}))
        row['target_papers'] = json.dumps(sorted({'Paper 1' if scope[c]['theme'] == 'A' else 'Paper 2' for c in retrieval_codes}))
        for key, source_key in [('source_years', 'year'), ('source_sessions', 'session'), ('historical_papers', 'paper')]:
            row[key] = json.dumps(sorted({str(s[source_key]) for s in sources if s.get(source_key) not in (None, '')}))
        row['question_type'] = record.get('question_type') or {
            'Construct': 'construction', 'Trace': 'code tracing', 'Explain': 'explanation',
            'Describe': 'description', 'Evaluate': 'evaluation', 'Discuss': 'discussion',
            'Sketch': 'diagram', 'Outline': 'short response',
        }.get(record.get('command_term'), 'short response')
        row['question_type_basis'] = 'explicit' if record.get('question_type') else 'command-based candidate; review required'
        row['scope_evidence_path'] = 'question-bank/scope_evidence.json' if review else ''
        row['reviewed_scope_bullet_ids'] = json.dumps(sorted({m['scope_bullet_id'] for m in review['mappings']})) if review else '[]'
        for dimension, key in [('mapping', 'syllabus'), ('technical', 'technical'), ('answer', 'answer'),
                               ('markscheme', 'markscheme'), ('assets', 'asset'), ('provenance', 'provenance')]:
            value = review['verification'].get(dimension, 'pending') if review else 'pending'
            row[key + '_verification_status'] = value.get('status', 'pending') if isinstance(value, dict) else value
        row['verification_record_reference'] = 'SQLite verification + verification_history tables; imported C3 snapshot in scope_evidence.json; C4 independent audit pending'
        row['usage_history_reference'] = 'SQLite usage_history table; selection alone is not examination use'
        row['outstanding_review_issues'] = json.dumps(review.get('issues', []), ensure_ascii=False) if review else json.dumps(['Detailed C3 question-to-scope review pending'])
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(stream.getvalue(), encoding='utf-8')
    os.replace(temporary, path)
    print(json.dumps({'preserved_question_rows': len(rows), 'approved_review_rows': len(evidence), 'added_metadata_columns': len(added), 'records_rewritten': 0}))


if __name__ == '__main__':
    main()
