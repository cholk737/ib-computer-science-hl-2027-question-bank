"""Coordinator-only cumulative merge of explicitly approved batch snapshots.

Run review_chunk2.py first, then approve/review batches in APPROVED_BATCHES.json.
This script never approves its own inputs or modifies specialist artifacts.
"""
from pathlib import Path
import csv,json,hashlib,collections,os
P=Path(__file__).resolve().parents[1]
APP=P/'audits/chunk-2/APPROVED_BATCHES.json'
approval=json.loads(APP.read_text());sources={};practices={};ledger=[]
def atomic_json(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)
for a in approval['batches']:
 f=P/a['path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256'],'Changed approved batch: '+a['path']
 b=json.loads(f.read_text());ledger.append(a)
 for s in b['source_questions']:
  q=s['source_question_id'];assert q not in sources;sources[q]=s
 for q in b['practice_questions']:
  assert q['question_id'] not in practices;practices[q['question_id']]=q
overrides=P/'audits/chunk-2/COORDINATOR_OVERRIDES.json'
if overrides.exists():
 for fix in json.loads(overrides.read_text()).get('practice_fixes',[]):
  if fix['question_id'] in practices:
   p=practices[fix['question_id']];p.update(fix['fields']);p['coordinator_revision_note']=fix['reason']
links=collections.defaultdict(list)
for p in practices.values():
 for q in p['source_question_ids']:assert q in sources;links[q].append(p['question_id'])
for s in sources.values():
 if s.get('adaptation_reuse_question_id'):
  q=s['adaptation_reuse_question_id'];assert q in practices,'Approve reused target batch first';links[s['source_question_id']].append(q)
  if s['source_question_id'] not in practices[q]['source_question_ids']:practices[q]['source_question_ids'].append(s['source_question_id'])
source_index=[];mapping=[];bank=[];exclusions=[]
for q,s in sorted(sources.items()):
 path=f'extraction/by-paper/{s["source_id"]}/questions/{q}.json'
 s=dict(s);s['coordinator_status']='batch_structure_source_marks_and_sample_review_passed';s['practice_question_ids']=links[q]
 atomic_json(P/path,s)
 source_index.append(dict(source_question_id=q,source_id=s['source_id'],source_filename=s['source_filename'],year=s['year'],session=s['session'],source_level=s['source_level'],paper=s['paper'],zone=s['zone'],option=s['option'],question=s['question'],subquestion=s['subquestion'],source_pdf_pages=s['source_pdf_pages'],source_printed_pages=s['source_printed_pages'],original_marks=s['original_marks'],command_term=s['command_term'],relevance_status=s['relevance_status'],practice_question_ids=links[q],record_path=path,markscheme_status=s['markscheme']['status'],review_required=any(m.get('review_required') for m in s['mappings'])))
 if s['relevance_status']=='C':exclusions.append(dict(source_question_id=q,source_id=s['source_id'],question=s['question'],subquestion=s['subquestion'],source_pdf_pages=s['source_pdf_pages'],original_marks=s['original_marks'],reason=s['exclusion_reason'],record_path=path))
 for i,m in enumerate(s['mappings'] or [{}],1):
  mapping.append(dict(mapping_id=f'MAP-{q}-{i:02}',source_question_id=q,practice_question_id=';'.join(links[q]),syllabus_code=m.get('syllabus_code',''),scope_bullet_reference=m.get('scope_evidence',''),relevance_status=s['relevance_status'],mapping_target=m.get('mapping_target','adapted_practice_only' if s['relevance_status']=='B' else 'original_and_adapted' if s['relevance_status']=='A' else 'excluded'),theme=m.get('theme',''),level=m.get('level',''),confidence=m.get('confidence',''),review_required=m.get('review_required',False),reviewer='specialist_author; coordinator_batch_checks_and_sample_review',notes=m.get('rationale',s['exclusion_reason'])))
for q,p in sorted(practices.items()):
 assert sum(x['marks'] for x in p['marking_points'])==p['marks']
 record_path=f'question-bank/records/{q}.json';question_path=f'question-bank/questions/{q}.json';ms_path=f'question-bank/markschemes/{q}.json'
 p=dict(p);p['record_path']=record_path;p['question_path']=question_path;p['markscheme_path']=ms_path;p['coordinator_status']='batch_checks_and_source_solution_sample_review_passed; preliminary_unofficial'
 atomic_json(P/record_path,p)
 public={k:p[k] for k in ['question_id','source_question_ids','derivation_status','unofficial','question_text','syllabus_codes','theme','level','marks','command_term','difficulty','adaptation_rationale','assets'] if k in p}
 atomic_json(P/question_path,public)
 atomic_json(P/ms_path,{k:p[k] for k in ['question_id','unofficial','marks','solution','marking_points','acceptable_alternatives','partial_credit_notes','common_errors','verification','code','test_code','markscheme_status'] if k in p})
 bank.append(dict(question_id=q,record_path=record_path,question_path=question_path,derivation_status=p['derivation_status'],source_question_ids=p['source_question_ids'],theme=p['theme'],syllabus_codes=p['syllabus_codes'],level=p['level'],marks=p['marks'],command_term=p['command_term'],difficulty=p['difficulty'],verification_status=p['coordinator_status'],markscheme_path=ms_path))
def write_csv(path,rows,fields=None):
 assert rows or fields
 fields=fields or list(rows[0]);tmp=(P/path).with_suffix('.csv.tmp');tmp.parent.mkdir(parents=True,exist_ok=True)
 with tmp.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in rows:w.writerow({k:json.dumps(r[k],ensure_ascii=False) if isinstance(r.get(k),(list,dict)) else r.get(k,'') for k in fields})
 tmp.replace(P/path)
write_csv('extraction/HISTORICAL_QUESTION_INDEX.csv',source_index)
write_csv('mapping/SYLLABUS_MAPPING.csv',mapping)
write_csv('question-bank/QUESTION_BANK.csv',bank)
write_csv('extraction/OBSOLETE_QUESTIONS.csv',exclusions,['source_question_id','source_id','question','subquestion','source_pdf_pages','original_marks','reason','record_path'])
result={'approved_batches':len(ledger),'source_records_merged':len(sources),'source_records_mapped':sum(s['relevance_status'] in ['A','B'] for s in sources.values()),'mapping_rows':len(mapping),'unique_practice_questions':len(practices),'obsolete_sources':len(exclusions),'reused_sources':sum(bool(s.get('adaptation_reuse_question_id')) for s in sources.values()),'unresolved_mapped_sources':sum(any(m.get('review_required') for m in s['mappings']) for s in sources.values())}
atomic_json(P/'audits/chunk-2/MERGE_STATUS.json',result)
atomic_json(P/'audits/chunk-2/MERGE_LEDGER.json',{'batches':ledger,'counts':result})
print(json.dumps(result,indent=2))
