from pathlib import Path
import json,sys,io,contextlib
P=Path(__file__).resolve().parents[4];q=json.loads((P/'question-bank/records/P-SRC005-Q09.json').read_text());ns={};exec(q['code'],ns);calls=[]
def trace(frame,event,arg):
 if frame.f_code.co_name=='reveal' and event=='call':calls.append(frame.f_locals['n'])
 return trace
buf=io.StringIO();sys.settrace(trace)
with contextlib.redirect_stdout(buf):result=ns['reveal'](['Oak','Pine','Elm'],2)
sys.settrace(None)
assert calls==[2,1,0] and buf.getvalue()=='Elm\nPine\nOak\n' and result is None
out={'question_id':q['question_id'],'status':'pass','calls':calls,'printed':buf.getvalue().splitlines(),'return':None,'evidence':'Executed actual stored code;one recursive call per activation,post-call printing reverses apparent input order.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
