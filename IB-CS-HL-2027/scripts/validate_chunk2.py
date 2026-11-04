"""Final Chunk 2 integrity gate; does not perform a Chunk 3 coverage audit."""
from pathlib import Path
import json,csv,hashlib,collections
P=Path(__file__).resolve().parents[1]
def read_csv(path):return list(csv.DictReader((P/path).open()))
sources=read_csv('extraction/HISTORICAL_QUESTION_INDEX.csv');bank=read_csv('question-bank/QUESTION_BANK.csv');mapping=read_csv('mapping/SYLLABUS_MAPPING.csv');excluded=read_csv('extraction/OBSOLETE_QUESTIONS.csv')
manifest=json.loads((P/'extraction/HISTORICAL_MANIFEST.json').read_text())
scope={s['code']:s for s in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}
review=json.loads((P/'audits/chunk-2/BATCH_REVIEW.json').read_text())
assert review['all_structural_checks_pass'] and not review['review_warnings']
assert len(sources)==review['sources']==1141
assert len(bank)==review['practices']
assert len(set(r['source_question_id'] for r in sources))==len(sources)
assert len(set(r['question_id'] for r in bank))==len(bank)
assert {s['source_id'] for s in sources}=={s['source_id'] for s in manifest}
margin=json.loads((P/'audits/chunk-2/MARK_RECONCILIATION.json').read_text())
assert len(margin)==21 and all(r['pass'] and r['author_complete'] for r in margin)
for sid in ['SRC-001','SRC-002']:assert json.loads((P/f'audits/chunk-2/{sid}_OCR_MARK_RECONCILIATION.json').read_text())['reconciled_all_differences']
assert not json.loads((P/'audits/chunk-2/CODE_REVIEW.json').read_text())['failures']
code_count=sum(bool(json.loads((P/r['record_path']).read_text()).get('code')) for r in bank)
assert json.loads((P/'audits/chunk-2/CODE_REVIEW.json').read_text())['code_records']==code_count
assert json.loads((P/'audits/chunk-2/SQL_REVIEW.json').read_text())['all_pass']
assert not json.loads((P/'audits/chunk-2/ANSWER_CODE_AST_CHECK.json').read_text())['failures']
approved=json.loads((P/'audits/chunk-2/APPROVED_BATCHES.json').read_text())['batches']
for b in approved:assert hashlib.sha256((P/b['path']).read_bytes()).hexdigest()==b['sha256'],'Changed batch '+b['path']
source_by={s['source_question_id']:s for s in sources};bank_by={p['question_id']:p for p in bank}
for s in sources:
 obj=json.loads((P/s['record_path']).read_text());assert obj['source_question_id']==s['source_question_id']
 assert obj['original_marks']==int(s['original_marks'])
 assert all(q in bank_by for q in obj['practice_question_ids'])
 if obj['relevance_status']=='C':assert not obj['practice_question_ids'] and obj['exclusion_reason']
 else:assert obj['practice_question_ids']
for p in bank:
 obj=json.loads((P/p['record_path']).read_text());prompt=json.loads((P/p['question_path']).read_text());ms=json.loads((P/p['markscheme_path']).read_text())
 assert obj['question_id']==prompt['question_id']==ms['question_id']==p['question_id']
 assert obj['question_text']==prompt['question_text'] and obj['solution']==ms['solution']
 assert 'solution' not in prompt and 'marking_points' not in prompt
 assert obj['unofficial'] and ms['unofficial'] and sum(m['marks'] for m in ms['marking_points'])==int(p['marks'])
 assert all(c in scope for c in obj['syllabus_codes'])
 assert all(q in source_by for q in obj['source_question_ids'])
for m in mapping:
 assert m['source_question_id'] in source_by
 assert not m['syllabus_code'] or m['syllabus_code'] in scope
 assert m['review_required']=='False'
assert len(excluded)==sum(s['relevance_status']=='C' for s in sources)
for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text()):
 assert hashlib.sha256((P/r['project_path']).read_bytes()).hexdigest()==r['sha256']==hashlib.sha256(Path(r['original_path']).read_bytes()).hexdigest()
assert not list((P/'exams').rglob('*.pdf')) and not list((P/'final-markschemes').rglob('*.pdf'))
assert not read_csv('coverage/COVERAGE_REPORT.csv'),'Chunk3 coverage audit must not be started'
expected_links=collections.defaultdict(list)
for r in bank:
 for code in json.loads(r['syllabus_codes']):expected_links[code].append(r['question_id'])
assert len(scope)==112
for code,s in scope.items():assert s['question_bank_ids']==sorted(expected_links[code])
count={'checkpoint':'C2-FINAL','papers_processed':23,'papers_remaining':0,'source_subquestions':len(sources),'source_subquestions_mapped':sum(s['relevance_status'] in ['A','B'] for s in sources),'unique_converted_questions':len(bank),'obsolete_source_subquestions':len(excluded),'unresolved_mapped_sources':0,'mapping_rows_including_exclusions':len(mapping),'reused_sources':sum(bool(json.loads((P/s['record_path']).read_text()).get('adaptation_reuse_question_id')) for s in sources),'all_assertions_passed':True,'verification_limits':'All source leaf counts/marks, schema/link/code IDs and marking totals checked; authors checked all source content and answers. Coordinator independently sampled source/solution content and ran code/SQL and boundary tests. Full exam-level independent marking/PDF audit remains Chunk4.'}
(P/'audits/chunk-2/FINAL_VALIDATION.json').write_text(json.dumps(count,indent=2)+'\n')
print(json.dumps(count,indent=2))
