from pathlib import Path
import json,os,hashlib,datetime
P=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent

def atomic(f,v):
 t=f.with_name(f.name+'.tmp');t.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n');os.replace(t,f)

def save(batch):
 scope={s['code']:s for s in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}
 target=O/'question_reviews.json';old=json.loads(target.read_text())['reviews'] if target.exists() else []
 ids={r['question_id'] for r in old}
 for b in batch:
  assert b['question_id'] not in ids,'Refuse duplicate review overwrite'
  q=json.loads((P/'question-bank/records'/f"{b['question_id']}.json").read_text())
  b.update({'reviewer':'/root/theme_b_coverage','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_sha256':hashlib.sha256((P/'question-bank/records'/f"{q['question_id']}.json").read_bytes()).hexdigest(),'record_path':q['record_path'],'original_syllabus_codes':q['syllabus_codes'],'review_scope':'Actual prompt and full mapped guidance, answer and all marking points read. Verification dimensions apply only where stated; no original-PDF source recheck implied.'})
  for m in b['mappings']:
   i=m['guidance_index'];m['scope_bullet_id']=f"{m['code']}:G{i:02d}";m['exact_guidance']=scope[m['code']]['guidance_paragraphs'][i-1];m['statement']=scope[m['code']]['statement'];m['mapping_verification_status']='verified'
  assert sum(x['marks'] for x in q['marking_points'])==q['marks']
  b['mark_total_check']={'question_marks':q['marks'],'marking_point_sum':sum(x['marks'] for x in q['marking_points']),'status':'pass'}
  old.append(b);ids.add(b['question_id'])
 atomic(target,{'schema_version':1,'scope_bullet_id_rule':'CODE:GNN means 1-based guidance_paragraphs index in verified syllabus master. Direct relevance certifies the named assessed skill only, not complete coverage of the paragraph or objective.','reviews':old})
 queue=json.loads((O/'question_review_queue.json').read_text())
 for item in queue:
  if item['question_id'] in ids:item['status']='c3_individual_review_saved';item['review_path']='agents/chunk-3/agent-2-theme-b/question_reviews.json';item['next_action']='Coordinator review/integration; consult independent verification dimensions for outstanding checks.'
 atomic(O/'question_review_queue.json',queue)
 s=json.loads((O/'STATUS.json').read_text());pending=[q['question_id'] for q in queue if q['question_id'] not in ids];s.update({'checkpoint':f'B-RECORD-{len(old):03d}','individual_record_reviews_completed':len(old),'individual_record_reviews_total':len(queue),'individual_record_reviews_remaining':len(pending),'last_saved_review_question_id':old[-1]['question_id'],'exact_next_action':('Review next queued record '+pending[0]+' plus next two; save actual scope evidence and each verification dimension separately.' if pending else 'All B individual reviews saved; await coordinator integration and resolve flagged repairs.'),'next_queued_question_id':pending[0] if pending else None});s['files_created']=sorted(set(s.get('files_created',[])+['question_reviews.json','question_review_queue.json','save_reviews.py']));atomic(O/'STATUS.json',s)
 print('Saved batch',len(batch),'total',len(old),'remaining',len(pending))

def m(code,i,skill,relevance,evidence,limits):return {'code':code,'guidance_index':i,'assessed_skill':skill,'relevance':relevance,'evidence':evidence,'coverage_limit':limits}
def v(technical,answer,markscheme,assets='not_required',provenance='pending_original_source_recheck'):
 def state(value,dimension):
  if value in ['verified','verified_manual']:
   return {'status':'verified','evidence':'Current specialist manually checked actual '+dimension+' against prompt and guide scope; concrete checks recorded in this review. This is not Chunk 4 independent audit.'}
  if value=='not_required':
   return {'status':'verified','evidence':'No external asset or visual-only information required; self-contained text prompt inspected.'}
  if value.startswith('needs_'):
   return {'status':'issue','evidence':value+'; concrete issue recorded in review.'}
  return {'status':'pending','evidence':value}
 return {'mapping':{'status':'verified','evidence':'Actual prompt and full exact scope compared; see individual mappings and coverage limits.'},'technical':state(technical,'technical content'),'answer':state(answer,'answer'),'markscheme':state(markscheme,'marking criteria'),'assets':state(assets,'assets'),'provenance':state(provenance,'provenance')}
