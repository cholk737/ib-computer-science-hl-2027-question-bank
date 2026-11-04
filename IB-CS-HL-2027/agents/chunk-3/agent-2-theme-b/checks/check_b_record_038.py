from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[4];q=json.loads((P/'question-bank/records/P-SRC002-Q18-c.json').read_text());ns={};exec(q['code'],ns);calls=[]
def trace(frame,event,arg):
 if event=='call' and frame.f_code.co_name=='sum_down':calls.append(frame.f_locals['n'])
 return trace
sys.settrace(trace);result=ns['sum_down'](-3);sys.settrace(None)
assert result==-3 and calls==[-3]
out={'question_id':q['question_id'],'status':'pass','result':result,'calls':calls,'evidence':'Actual stored code returns immediately from n<=1 base branch; no recursive invocation or recursion error.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
