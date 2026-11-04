from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[4]
q=json.loads((P/'question-bank/records/P-SRC002-Q18-b.json').read_text());ns={};exec(q['code'],ns);events=[]
def trace(frame,event,arg):
 if frame.f_code.co_name=='sum_down' and event in ['call','return']:
  events.append([event,frame.f_locals['n']]+([arg] if event=='return' else []))
 return trace
sys.settrace(trace);actual=ns['sum_down'](4);sys.settrace(None)
assert actual==10
assert events==[['call',4],['call',3],['call',2],['call',1],['return',1,1],['return',2,3],['return',3,6],['return',4,10]]
assert ns['sum_down'](1)==1
out={'question_id':q['question_id'],'status':'pass','actual':actual,'events':events,'evidence':'Actual stored recursive code instrumented; one recursive invocation per non-base activation; all requested call/return values verified.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
