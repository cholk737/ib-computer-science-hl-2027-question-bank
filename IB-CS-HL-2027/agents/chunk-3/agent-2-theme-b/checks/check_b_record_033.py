from pathlib import Path
import json,itertools
from types import SimpleNamespace as N
P=Path(__file__).resolve().parents[4];results=[]
q=json.loads((P/'question-bank/records/P-SRC002-Q16-c.json').read_text());ns={};exec(q['code'],ns)
for charges in [[],[[]],[[0]],[[12,8],[],[5.5,10.5]]]:
 stores=[N(bookings=[N(get_cost=lambda c=c:c) for c in row]) for row in charges]
 assert ns['total_income'](stores)==sum(sum(row) for row in charges)
results.append({'question_id':q['question_id'],'status':'pass','evidence':'Actual stored code:empty stores,empty bookings,zero charge,multiple stores/fractional charges checked against nested-sum oracle.'})
q=json.loads((P/'question-bank/records/P-SRC002-Q17-a.json').read_text());ns={};exec(q['code'],ns);count=0
for size in range(6):
 for preferences in itertools.product('AB',repeat=size):
  nodes=[N(customer=N(preferred_shop=p),next=None) for p in preferences]
  for a,b in zip(nodes,nodes[1:]):a.next=b
  head=nodes[0] if nodes else None;before=[x.next for x in nodes]
  assert ns['change_preference'](head,'A','C')==preferences.count('A')
  assert [x.customer.preferred_shop for x in nodes]==['C' if p=='A' else p for p in preferences]
  assert [x.next for x in nodes]==before;count+=1
shared=N(preferred_shop='A');head=N(customer=shared,next=N(customer=shared,next=None))
shared_result=ns['change_preference'](head,'A','C')
same_result=ns['change_preference'](N(customer=N(preferred_shop='A'),next=None),'A','A')
assert shared_result==1 and same_result==1
results.append({'question_id':q['question_id'],'status':'intended_unique_customer_distinct_value_cases_pass_domain_ambiguities','cases':count,'evidence':'Unique customer per node,old!=new:all63 lists length0..5 preserve links and update/count matches.','ambiguities':{'two_nodes_same_customer_initially_matching_return':shared_result,'old_equals_new_single_matching_customer_return':same_result,'note':'Prompt does not define whether count means matching nodes,distinct customer objects,or changed field values; add domain/meaning clarification before full correctness verification.'}})
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(json.dumps(results))
