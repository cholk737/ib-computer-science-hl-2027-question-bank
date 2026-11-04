from pathlib import Path
import json,itertools
P=Path(__file__).resolve().parents[4];results=[]
q=json.loads((P/'question-bank/records/P-SRC002-Q06-b.json').read_text());ns={};exec(q['code'],ns)
data=list(range(20,81));actual=ns['scale_scores'](data)
# Match the supplied floating-point formula exactly; algebraic rearrangement can differ at a half due to rounding.
expected=[round((s-20)/60*65+30) for s in data]
assert actual==expected and data==list(range(20,81));assert ns['scale_scores']([])==[]
assert ns['scale_scores']([20,50,80])==[30,62,95]
results.append({'question_id':q['question_id'],'status':'pass','evidence':'All integer scores20..80 using supplied operation order; empty list; endpoints; midpoint62.5 rounds62 as Python nearest-even; input unchanged.'})
q=json.loads((P/'question-bank/records/P-SRC002-Q06-d.json').read_text());ns={};exec(q['code'],ns);n=0
for size in range(1,5):
 for data in itertools.product([90,91,95.5,100,101],repeat=size):
  expected=100*sum(1 for x in data if x>=91 and x<=100)/len(data)
  assert abs(ns['high_percentage'](list(data))-expected)<1e-10;n+=1
results.append({'question_id':q['question_id'],'status':'pass','cases':n,'evidence':'All lists length1..4 from90,91,95.5,100,101 cover inclusive endpoints, decimals, none/all matches; denominator total list length.'})
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(json.dumps(results))
