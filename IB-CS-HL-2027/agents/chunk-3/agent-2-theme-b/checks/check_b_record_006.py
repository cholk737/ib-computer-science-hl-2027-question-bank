from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[4]
q=json.loads((P/'question-bank/records/P-SRC001-Q14-b.json').read_text())
ns={};exec(q['code'],ns)
events=[]
def trace(frame,event,arg):
 if frame.f_code.co_name=='suffix_product':
  if event=='call':events.append(['call',frame.f_locals['k']])
  if event=='return':events.append(['return',frame.f_locals['k'],arg])
 return trace
sys.settrace(trace)
result=ns['suffix_product'](4,[8,3,2,5,4])
sys.settrace(None)
assert result==40
assert events==[['call',4],['call',3],['call',2],['call',1],['return',1,1],['return',2,2],['return',3,10],['return',4,40]],events
assert ns['suffix_product'](1,[8,3])==1
out={'question_id':q['question_id'],'status':'pass','result':result,'events':events,'additional_checks':['base case k=1 returns 1'],'note':'Independent sys.settrace of actual stored Python code, not copied expected function.'}
(Path(__file__).with_suffix('.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
