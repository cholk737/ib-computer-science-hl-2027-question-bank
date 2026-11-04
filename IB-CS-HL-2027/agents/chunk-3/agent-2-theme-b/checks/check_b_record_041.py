from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[4];q=json.loads((P/'question-bank/records/P-SRC004-Q09-a.json').read_text());ns={};exec(q['code'],ns);events=[]
def trace(frame,event,arg):
 if frame.f_code.co_name=='digit_total' and event in ['call','return']:events.append([event,frame.f_locals['n']]+([arg] if event=='return' else []))
 return trace
sys.settrace(trace);actual=ns['digit_total'](3407);sys.settrace(None)
assert actual==14
assert events==[['call',3407],['call',340],['call',34],['call',3],['call',0],['return',0,0],['return',3,3],['return',34,7],['return',340,7],['return',3407,14]]
q2=json.loads((P/'question-bank/records/P-SRC004-Q09-b.json').read_text());ns2={};exec(q2['code'],ns2)
for n in list(range(1001))+[101010,999999,100000000]:assert ns2['digit_total'](n)==sum(int(c) for c in str(n))
out={'status':'pass','results':[{'question_id':q['question_id'],'result':actual,'events':events},{'question_id':q2['question_id'],'cases':1004,'evidence':'Actual code compared with independent decimal-string digit-sum oracle for0..1000 and larger repeated/zero-digit cases.'}]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
