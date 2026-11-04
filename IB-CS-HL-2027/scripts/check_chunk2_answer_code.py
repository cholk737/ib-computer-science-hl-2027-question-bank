"""Check that prose-polished Python answers preserve executable function bodies."""
from pathlib import Path
import json,ast,re
P=Path(__file__).resolve().parents[1]
checks=[]
for f in (P/'agents/chunk-2').glob('*/batches/*.json'):
 for p in json.loads(f.read_text())['practice_questions']:
  code=p.get('code','');solution=p['solution'];m=re.search(r'(?m)^(?:def|class) ',solution)
  if not code or not m:continue
  snippet=solution[m.start():];parsed=None;prefix=''
  for n in range(len(snippet.splitlines()),0,-1):
   try:
    prefix='\n'.join(snippet.splitlines()[:n]);parsed=ast.parse(prefix);break
   except SyntaxError:pass
  if parsed is None:checks.append({'question_id':p['question_id'],'pass':False,'issue':'No valid answer-code AST prefix'});continue
  actual=ast.parse(code)
  defs={x.name:ast.dump(x,include_attributes=False) for x in ast.walk(actual) if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
  explained={x.name:ast.dump(x,include_attributes=False) for x in ast.walk(parsed) if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
  mismatches=[name for name,dump in explained.items() if name in defs and defs[name]!=dump]
  row={'question_id':p['question_id'],'answer_functions':list(explained),'function_body_differences':mismatches,'pass':not mismatches}
  if p['question_id']=='P-SRC033-Q14-d-i' and mismatches==['pay']:
   ns={};answer={};exec(code,ns);exec(prefix,answer);obj=ns['Rental']()
   assert all(obj.pay(h)==answer['pay'](obj,h)==(obj.ADMIN_FEE if h<=5 else 0) for h in range(21))
   row['pass']=True;row['resolution']='Equivalent if/conditional-expression implementations; executed both for all integer hours0..20, including boundary5/6. Fixture adds Rental class/ADMIN_FEE; standalone answer defines only requested method.'
  checks.append(row)
out={'checks':checks,'failures':[c for c in checks if not c['pass']],'limits':'Checks saved Python function bodies where an answer includes code; prose traces and SQL use separate checks. Equivalent structural differences require an explicit validated exception.'}
(P/'audits/chunk-2/ANSWER_CODE_AST_CHECK.json').write_text(json.dumps(out,indent=2))
print('Answer/code checks',len(checks),'failures',out['failures'])
