from pathlib import Path
import json,math,copy,ast
P=Path(__file__).resolve().parents[4];out=[]
q=json.loads((P/'question-bank/records/P-SRC005-Q14-a.json').read_text());n=0
for a in range(1,31):
 for b in range(1,31):
  actual=eval(q['solution'],{},dict(a=a,b=b));expected=(a<b and any(a*k==b for k in range(1,b+1)))
  assert actual is expected;n+=1
out.append({'question_id':q['question_id'],'status':'pass','cases':n,'evidence':'Actual answer Boolean expression checked on positive integers1..30 against multiplication-based divisibility oracle.'})
def oracle(n):
 divisors=set()
 for d in range(1,math.isqrt(n)+1):
  if n%d==0:divisors.update([d,n//d])
 divisors.discard(n);return sum(divisors)
q=json.loads((P/'question-bank/records/P-SRC005-Q14-b.json').read_text());ns={};exec(q['code'],ns)
for n in range(1,501):assert ns['proper_sum'](n)==oracle(n)
out.append({'question_id':q['question_id'],'status':'pass','cases':500,'evidence':'Actual function compared against paired-divisor set oracle,including1,perfect squares,prime/perfect/deficient/abundant values.'})
q=json.loads((P/'question-bank/records/P-SRC005-Q14-c.json').read_text());assert ast.dump(ast.parse(q['code']))==ast.dump(ast.parse(q['solution']))
ns={};exec(q['code'],ns);calls=[]
def instrumented(n):calls.append(n);return oracle(n)
ns['proper_sum']=instrumented
for grid in [[],[[]],[[1,6,12],[9,28,12]],[[36],[2,3,4],[]]]:
 calls.clear();before=copy.deepcopy(grid);flat=[n for row in grid for n in row];expected=([],[],[])
 for n in flat:
  total=oracle(n);index=0 if total<n else 1 if total==n else 2;expected[index].append(n)
 assert ns['classify_grid'](grid)==expected and calls==flat and grid==before
out.append({'question_id':q['question_id'],'status':'pass','evidence':'Code and solution AST agree;instrumented helper confirms exactly one call per row-major value;independent oracle classification,duplicates,empty rows/input and no mutation.'})
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':out},indent=2)+'\n');print(json.dumps(out))
