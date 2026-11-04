from pathlib import Path
import json,itertools,copy
P=Path(__file__).resolve().parents[4];results=[]
qid='P-SRC001-Q15-c';q=json.loads((P/'question-bank/records'/f'{qid}.json').read_text());ns={};exec(q['code'],ns);n=0
for row in itertools.product('SDCX',repeat=4):
 data=[list(row),list(reversed(row))];before=copy.deepcopy(data)
 assert ns['total_receipts'](data)==2*sum({'S':18,'D':9,'C':4,'X':0}[v] for v in row)
 assert data==before;n+=1
assert ns['total_receipts']([])==0
results.append({'question_id':qid,'status':'pass','cases':n+1,'evidence':'All256 rows length4 over four seat codes, duplicated/reversed second row, independent tariff dictionary oracle; input unchanged; empty list zero.'})
qid='P-SRC002-Q05-a-ii';q=json.loads((P/'question-bank/records'/f'{qid}.json').read_text());n=0
for test in range(51):
 for project in range(81):
  ns={'test_score':test,'project_score':project};exec(q['solution'],ns)
  assert abs(ns['percentage']-(0.6*test+0.875*project))<1e-10;n+=1
results.append({'question_id':qid,'status':'pass','cases':n,'evidence':'All valid integer component scores; independent simplified coefficients oracle, full scores100 and zero scores0.'})
qid='P-SRC002-Q05-b';q=json.loads((P/'question-bank/records'/f'{qid}.json').read_text());ns={};exec(q['code'],ns)
bands=[(35,46,'E'),(47,59,'D'),(60,69,'C'),(70,84,'B'),(85,100,'A')]
for score in range(35,101):
 expected=next(g for low,high,g in bands if low<=score<=high)
 assert ns['grade'](score)==expected
results.append({'question_id':qid,'status':'pass','cases':66,'evidence':'All allowed integers35..100 checked against disjoint interval oracle, including every boundary.'})
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(json.dumps(results))
