"""Coordinator-only merge, gated by independently passing source checks."""
from pathlib import Path
import csv,json,re,collections
P=Path(__file__).resolve().parents[1]
check=json.loads((P/'audits/SYLLABUS_INTEGRATION_CHECK.json').read_text())
assert check['all_pass'] and check['source_codes']==112
records=[]
for rel in ['agents/chunk-1/agent-1-theme-a/theme_a_scope.json','agents/chunk-1/agent-2-theme-b/theme_b_scope.json']:
 for original in json.loads((P/rel).read_text()):
  r=dict(original)
  r['specialist_record_path']=r['record_path']
  r['source_code']=r.get('source_code',r['code'])
  r['source_statement']=r.get('statement_with_level_tag',r['statement'])
  r['statement']=r['source_statement']
  r['level_basis']=r.get('level_basis',r.get('level_evidence',''))
  r['transcription_normalizations']=['Source line wraps joined; layout whitespace normalized; full original PDF remains authoritative.']
  r['specialist_guidance_transcription']=r['guidance']
  r['guidance']=re.sub(r'(?<=\w)([-/]) (?=\w)',r'\1',r['guidance'])
  if r['code']=='A4.3.1':
   r['guidance']=r['guidance'].replace('like r2.','like r².')
   r['transcription_normalizations'].append('Superscript 2 restored from visually verified source; specialist raw extraction retained separately.')
  r['guidance_paragraphs']=r['guidance'].splitlines()
  r['must_include_guidance']=[s for s in r['guidance_paragraphs'] if 'must include' in s.lower()]
  r['may_include_guidance']=[s for s in r['guidance_paragraphs'] if 'may include' in s.lower()]
  r['global_scope_note_source']='Guide PDF p34 / printed p28'
  r['global_scope_note']='“May include” means that the list includes examples that could be assessed, although other examples may also be used by the IB in assessment. “Must include” means that the list includes all the examples that will be used in assessment.'
  r['question_bank_ids']=[]
  r['coverage_status']='not_yet_assessed_chunk1'
  r['verification_status']='verified_source_text_all_characters; independent_code_pages_HL_check_pass; specialist_all_page_visual_review; coordinator_visual_sampling'
  r['coordinator_check_path']='audits/SYLLABUS_INTEGRATION_CHECK.json'
  r['uncertainty_flags']=r.get('uncertainty_flags',[])
  if r['code'] in ['B3.1.3','B3.1.5','B3.2.1','B3.2.2']:
   r['uncertainty_flags'].append('Generic source OOP language must be implemented accurately in Python; see programming_policy_notes.md. No Java access enforcement or overload semantics may be assumed in Python.')
  r['record_path']='syllabus/records/'+r['code']+'.json'
  (P/'syllabus/records').mkdir(exist_ok=True)
  (P/r['record_path']).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
  records.append(r)
fields=['code','source_code','theme','topic','subtopic','statement','level','level_basis','source_file','source_sha256','source_pdf_pages','source_printed_pages','guidance','scope_qualifications','must_include_guidance','may_include_guidance','assessable_knowledge_skills','allowed_context','coverage_status','question_bank_ids','verification_status','uncertainty_flags','record_path','specialist_record_path']
with (P/'syllabus/SYLLABUS_MASTER.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in records:w.writerow({k:json.dumps(r[k],ensure_ascii=False) if isinstance(r.get(k),list) else r.get(k,'') for k in fields})
(P/'syllabus/SYLLABUS_MASTER.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'merged':len(records),'levels':dict(collections.Counter(r['level'] for r in records)),
 'must_include_paragraphs':sum(len(r['must_include_guidance']) for r in records),
 'may_include_paragraphs':sum(len(r['may_include_guidance']) for r in records)},indent=2))
