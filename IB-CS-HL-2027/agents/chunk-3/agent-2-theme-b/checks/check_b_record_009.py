from pathlib import Path
import json,itertools
P=Path(__file__).resolve().parents[4]
results=[]
for qid in ['P-SRC001-Q14-c','P-SRC001-Q15-b']:
 q=json.loads((P/'question-bank/records'/f'{qid}.json').read_text());ns={};exec(q['code'],ns);count=0
 if qid.endswith('Q14-c'):
  for size in range(6):
   for values in itertools.combinations_with_replacement(range(-1,4),size):
    data=list(values)
    for target in range(-2,5):
     assert ns['contains_sorted'](target,data)==any(x==target for x in data)
     assert data==list(values);count+=1
  desc='Exhaustive ascending lists length 0..5 from -1..3, including duplicates, all targets -2..4; oracle any equality; original list unchanged.'
 else:
  for size in range(6):
   for row in itertools.product('SDX',repeat=size):
    data=[['X'],list(row),['D']]
    assert ns['discounted_in_row'](data,1)==sum(x=='D' for x in row)
    assert data[1]==list(row);count+=1
  desc='All rows length 0..5 over S,D,X; checks selected middle row only, zero/all matches and original data unchanged.'
 results.append({'question_id':qid,'status':'pass','assertion_cases':count,'evidence':desc})
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(json.dumps(results))
