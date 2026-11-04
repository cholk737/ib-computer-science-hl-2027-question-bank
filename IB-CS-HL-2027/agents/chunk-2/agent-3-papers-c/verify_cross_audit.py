from build_records import *
import hashlib
def find(folder,source,question):
 for f in (P/'agents/chunk-2'/folder/'batches').glob(source+'-*.json'):
  b=json.loads(f.read_text())
  for p in b['practice_questions']:
   if p['question_id']==question:
    r=next(r for r in b['source_questions'] if r['source_question_id']==p['source_question_ids'][0])
    return f,p,r
 raise AssertionError(question)
f,p,r=find('agent-1-papers-a','SRC-042','P-SRC042-Q05-f');ns={};exec(p['code'],ns);summary=ns['day_summary'];checks=[]
hours=list(range(24))
assert [h for h in hours if h>=20 or h<6]==[0,1,2,3,4,5,20,21,22,23]
assert not any(h>=19 and h<7 for h in hours)
for value in [-3000,-4,0,4000]:
 result=summary(hours,[value]*24);assert result==(value,value,value,value);checks.append({'case':'constant '+str(value),'result':list(result)})
for hour in [0,5,6,7,18,19,20,23]:
 temperatures=[0]*24;temperatures[hour]=100
 result=summary(hours,temperatures);expected_night=10 if hour in [0,5,20,23] else 0
 assert result==(100,0,100/24,expected_night)
 checks.append({'case':'single nonzero at hour '+str(hour),'night_mean':result[-1]})
for order in [hours,hours[::-1],hours[13:]+hours[:13]]:
 temperatures=[h*h-300 for h in order];got=summary(order,temperatures)
 night=[v for h,v in zip(order,temperatures) if h>=20 or h<6]
 assert got==(max(temperatures),min(temperatures),sum(temperatures)/24,sum(night)/10)
checks.append({'case':'ascending,reversed,rotated parallel lists and mixed negative values','result':'passed'})
receipts=[{'question_id':p['question_id'],'batch':str(f.relative_to(P)),'batch_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'tests':checks,'verdict':'Adapted algorithm passes; original MS defects confirmed. Original and adapted nighttime windows differ explicitly, so the adapted night denominator is10 rather than source12.','mapped_scope':[{c:S[c]} for c in p['syllabus_codes']]}]
f,p,r=find('agent-2-papers-b','SRC-038','P-SRC038-Q05-e');ns={};exec(p['code'],ns);percentage=ns['success_percent'];checks=[]
for trials,winners in [(1,0),(1,1),(2,1),(3,1),(10,0),(1000,1000),(10000,10000),(10000,3721)]:
 calls=[];follow_calls=[]
 def make_links():
  calls.append(1);return list(range(10))
 def follow_all(links,attempts):
  assert links==list(range(10)) and attempts==5
  follow_calls.append(1);return [True]*10 if len(follow_calls)<=winners else [True]*9+[False]
 result=percentage(make_links,follow_all,trials)
 assert result==100*winners/trials and len(calls)==len(follow_calls)==trials
 checks.append({'trials':trials,'wins':winners,'percentage':result,'fresh_calls':len(calls)})
# Every position matters; no stale True state can survive across trials.
seq=iter([[True]*10]+[[True]*i+[False]+[True]*(9-i) for i in range(10)])
assert percentage(lambda:list(range(10)),lambda links,attempts:next(seq),11)==100/11
checks.append({'case':'all ten individual false positions after an all-success trial','percentage':100/11})
receipts.append({'question_id':p['question_id'],'batch':str(f.relative_to(P)),'batch_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'tests':checks,'verdict':'Adapted algorithm passes; fresh per-trial state and correct trial-dependent denominator. Original MS1000/100 scale defect confirmed.','mapped_scope':[{c:S[c]} for c in p['syllabus_codes']]})
atomic(O/'cross_audit.json',{'auditor':'Historical Paper Processor C; read-only review of A/B ownership','date':'2026-11-04','source_evidence':'cross-audit-evidence/ contains independently extracted original PDF pages and inspected renders','receipts':receipts,'non_algorithm_findings':['At audit time SRC042 source original_text and parent_context are synopses, assets empty, and source_issues empty despite known defects. Require owner transcription/evidence/source-issue repair before final integration.','Both adapted algorithms meet the precise mapped list/selection/loop/function scope. Built-in restriction on SRC042 explicitly assesses extrema/accumulation.','P-SRC038-Q05-e should specify positive integer trials, since range requires integer. This is a small wording clarification; algorithm/criteria are correct.']})
print('Cross-audit source defects confirmed; both adapted algorithms pass independent boundary and denominator tests.')
