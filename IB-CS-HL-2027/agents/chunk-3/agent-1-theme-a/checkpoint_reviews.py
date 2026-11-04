from review_batches import *
def save_batch(records,number,next_action,extra_files=[]):
 checkpoint=f'A-RECORDS-{number:03d}';filename=f'scope_reviews/batch-{number:03d}.json';target=O/filename
 if target.exists(): raise RuntimeError('Refusing to overwrite saved review batch; resume from next pending record.')
 atomic(target,{'checkpoint':checkpoint,'reviews':records})
 allr={r['question_id']:r for f in (O/'scope_reviews').glob('*.json') for r in json.loads(f.read_text())['reviews']}
 q=json.loads((O/'REVIEW_QUEUE.json').read_text())
 for r in q['records']:
  if r['question_id'] in allr:
   d=allr[r['question_id']];r['status']='reviewed_with_issue' if d['issues'] else 'reviewed_specialist';r['review_path']=next(str(f.relative_to(P)) for f in (O/'scope_reviews').glob('*.json') if any(v['question_id']==r['question_id'] for v in json.loads(f.read_text())['reviews']))
 q.update(checkpoint=checkpoint,reviewed_count=len(allr),pending_count=len(q['records'])-len(allr));atomic(O/'REVIEW_QUEUE.json',q)
 t=json.loads((O/'STATUS.json').read_text());t.update(checkpoint=checkpoint,last_saved_question_id=records[-1]['question_id'],last_saved_reviewed_question_id=records[-1]['question_id'],record_review_counts={'total_owned':459,'reviewed':len(allr),'pending':459-len(allr)},reviewed_question_ids=sorted(allr),next_action=next_action,unfinished_tasks=['Review remaining Theme A records individually against exact statement/bullets in batches of2–3.','Coordinator resolve explicit review issues; changed record hashes need fresh validation.','Original gap generation after database mapping priority; no original generated.']);t['files_created']=sorted(set(t['files_created']+[filename,'checkpoint_reviews.py']+extra_files));atomic(O/'STATUS.json',t)
 with (O/'findings.md').open('a') as f:f.write(f'\n{checkpoint}: {len(allr)}/459 reviewed,{459-len(allr)} pending; last {records[-1]["question_id"]}. Saved {filename}. Next: {next_action}\n')
 print('Saved',checkpoint,len(allr),'reviewed;',459-len(allr),'pending')
