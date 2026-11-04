from pathlib import Path
import json,itertools
P=Path(__file__).resolve().parents[4]
try:
 'Isabella'.index(' ')
except ValueError:missing=True
else:missing=False
assert missing
q=json.loads((P/'question-bank/records/P-SRC002-Q05-d.json').read_text());ns={};exec(q['code'],ns);n=0
for length in range(7):
 for values in itertools.product('a ',repeat=length):
  name=''.join(values);positions=[i for i,c in enumerate(name) if c==' '];actual=ns['first_space_or_false'](name)
  if positions:assert type(actual) is int and actual==positions[0]
  else:assert actual is False
  n+=1
out={'status':'pass','results':[{'question_id':'P-SRC002-Q05-c','evidence':'Actual string index call on Isabella raised ValueError.'},{'question_id':q['question_id'],'cases':n,'evidence':'All strings length0..6 over letter/space; first-position index0 stays integer0, absent result is Boolean False using identity/type checks.'}]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
