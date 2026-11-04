from pathlib import Path
import json,collections
O=Path(__file__).resolve().parent;P=O.parents[2];S={r['code']:r for r in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}
exclude={'H-SRC030-Q02-b','H-SRC008-Q07','H-SRC018-Q09'}
removed={'P-'+q[2:] for q in exclude}|{'P-SRC030-Q09-c-i'}
for path in sorted((O/'batches').glob('*.json')):
 b=json.loads(path.read_text())
 for r in b['source_questions']:
  if r['source_question_id'] in exclude:
   r['relevance_status']='C';r['mappings']=[];r['exclusion_reason']='Virtual-memory paging is not explicitly required by2027 statement guidance; generic OS memory-management wording is not treated as a requirement to explain paging. Coordinator cross-paper consistency resolution.'
  if r['source_question_id']=='H-SRC030-Q09-c-i':
   r['relevance_status']='B';r['mappings']=[dict(syllabus_code='A2.1.2',theme='A',level=S['A2.1.2']['level'],scope_evidence=S['A2.1.2']['guidance'],rationale='Coordinator duplicate resolution reuses cloud-infrastructure availability practice; original backup/recovery technique is not claimed as direct2027 scope.',confidence='high',review_required=False,mapping_target='adapted_practice_only')]
   r['reused_practice_question_ids']=['P-SRC028-Q09-c-i']
   r['adaptation_reuse_question_id']='P-SRC028-Q09-c-i'
   r['conversion_note']='No separate copy authored;coordinator links this source to existing cloud-benefit practiceP-SRC028-Q09-c-i.'
  if r['source_id']=='SRC-001':
   r['transcription_status']='Manual source leaf transcription from raster;shared source context summarized separately;full source page image authoritative. No uploaded official markscheme.'
   r['source_page_evidence']=[dict(pdf_page=n,path=f'agents/chunk-2/agent-1-papers-a/papers/SRC-001/page-{n}.png',kind='visually_checked_original_raster') for n in r['source_pdf_pages']]
 b['practice_questions']=[q for q in b['practice_questions'] if q['question_id'] not in removed]
 for q in b['practice_questions']:
  if q['question_id']=='P-SRC030-Q13-c':q['question_text']=q['question_text'].replace('i ff','if and only if').replace(' iff ',' if and only if ')
  if q['question_id']=='P-SRC018-Q14-c':q['marking_points'][0]['criterion']='Initializes best with the first complete row total or with an unset marker; a single element is not a safe row-total bound.'
  if q['question_id']=='P-SRC008-Q12-c-ii':q['command_term']='Sketch'
  if q['question_id']=='P-SRC024-Q13-b-ii':
   q['command_term']='Construct';q['question_text']=q['question_text'].replace('Correct show_readings','Construct a corrected show_readings function')
  # A few uncommon/proper technical strings are kept as intact words after prose normalization.
  for key in ['question_text','solution','adaptation_rationale','partial_credit_notes']:
   if isinstance(q.get(key),str):
    q[key]=q[key].replace('ex trema','extrema').replace('ear lier','earlier').replace('un set','unset').replace('large st','largest').replace('inrowr','in row r').replace('inFIFOorder','in FIFO order').replace('Falseifanyflag','False if any flag').replace('Trueonlyifall','True only if all').replace('andis Empty','and isEmpty')
  for point in q['marking_points']:
   point['criterion']=point['criterion'].replace('ex trema','extrema').replace('ear lier','earlier').replace('un set','unset').replace('large st','largest').replace('inrowr','in row r').replace('inFIFOorder','in FIFO order').replace('Falseifanyflag','False if any flag').replace('Trueonlyifall','True only if all').replace('andis Empty','and isEmpty')
 path.write_text(json.dumps(b,ensure_ascii=False,indent=2))
for sid in ['SRC-001','SRC-005','SRC-008','SRC-018','SRC-024','SRC-030']:
 batches=[json.loads(p.read_text()) for p in sorted((O/'batches').glob(sid+'-b*.json'))]
 source=[r for b in batches for r in b['source_questions']];practice=[r for b in batches for r in b['practice_questions']]
 path=O/'papers'/sid/'paper_audit.json';audit=json.loads(path.read_text());audit['counts']=dict(collections.Counter(r['relevance_status'] for r in source));audit['converted_count']=len(practice);audit['reused_conversion_count']=sum(bool(r.get('reused_practice_question_ids')) for r in source)
 audit['source_transcription_check']='Exact marked-leaf intervals reconstructed from original PDF with matching count and source-mark sequence' if sid!='SRC-001' else 'Manual leaf transcription and visually checked source raster;no text layer'
 audit['prose_check']='Authored prose spacing corrected;code fields unchanged;command mismatches fixed.'
 path.write_text(json.dumps(audit,indent=2));print(sid,len(source),len(practice),audit['counts'])
