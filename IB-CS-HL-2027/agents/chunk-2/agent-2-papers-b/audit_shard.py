from build_shard import *
import hashlib,ast
sids=['SRC-002','SRC-006','SRC-009','SRC-020','SRC-026','SRC-032','SRC-038','SRC-044']
fail=[];results=[];allr=[];allp=[];hashes={}
for sid in sids:
 rr=[];pp=[]
 for file in sorted((O/'batches').glob(sid+'-b*.json')):
  b=json.loads(file.read_text());rr+=b['source_questions'];pp+=b['practice_questions'];hashes[file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
 exp=extract(sid)
 assert len(rr)==len(exp)
 assert sum(r['original_marks'] for r in rr)==sum(x['original_marks'] for x in exp)
 for r,x in zip(rr,exp):
  assert r['original_text']==x['original_text'] and r['original_marks']==x['original_marks']
  assert r['source_pdf_pages']==x['source_pdf_pages']
  assert r['relevance_status']!='C' or r['exclusion_reason']
  for m in r['mappings']:assert m['syllabus_code'] in SCOPE and m['scope_evidence']==SCOPE[m['syllabus_code']]['guidance']
  for a in r['assets']:assert (P/a['path']).exists(),a
 for p in pp:
  assert sum(m['marks'] for m in p['marking_points'])==p['marks']
  assert p['command_term']!='See original prompt',p['question_id']
  tc=p['verification'].get('test_code','');result={'question_id':p['question_id'],'test_present':bool(tc)}
  if tc:
   try:exec(tc,{});result['status']='pass'
   except Exception as e:result['status']='FAIL';result['error']=repr(e);fail.append(result)
  else:result['status']='author_reasoned_no_executable_check_required'
  if p.get('code'):
   try:ast.parse(p['code'])
   except Exception as e:fail.append({'question_id':p['question_id'],'code_syntax':repr(e)})
  results.append(result)
 allr+=rr;allp+=pp
print('leaves',len(allr),'practice',len(allp),'status',collections.Counter(r['relevance_status'] for r in allr),'marks',sum(r['original_marks'] for r in allr),'tests',sum(r['test_present'] for r in results),'fail',fail)
(O/'test_results.json').write_text(json.dumps(dict(executable_checks=results,failures=fail,passed=not fail),indent=2))
(O/'batch_sha256.json').write_text(json.dumps(hashes,indent=2))
(O/'final_question_review.txt').write_text('\n\n'.join(p['question_id']+' '+','.join(p['syllabus_codes'])+' '+p['command_term']+' '+str(p['marks'])+'\n'+p['question_text']+'\nANSWER:'+p['solution']+'\nCRITERIA:'+str(p['marking_points']) for p in allp))
assert not fail
