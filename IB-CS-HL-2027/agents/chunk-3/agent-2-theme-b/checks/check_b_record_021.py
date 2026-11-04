from pathlib import Path
import json
P=Path(__file__).resolve().parents[4]
q=json.loads((P/'question-bank/records/P-SRC002-Q14-b-i.json').read_text())
ns={};exec('class Reservation:\n def __init__(self,rate,priority=False):\n  self.rate=rate\n  self.priority=priority\n',ns)
exec(q['solution'].split('. The optional')[0],ns)
assert ns['a'].rate==ns['b'].rate==40
assert ns['a'].priority is False and ns['b'].priority is True
ns={};exec('class Example:\n def __init__(self,value): self.first=value\n def __init__(self): self.second=2\n',ns)
x=ns['Example']();assert x.second==2 and not hasattr(x,'first')
try:ns['Example'](3)
except TypeError:replacement=True
else:replacement=False
assert replacement
out={'status':'pass','results':[{'question_id':'P-SRC002-Q14-b-i','evidence':'Executed actual answer constructor calls against minimal stated initializer fixture; states40/False and40/True.'},{'question_id':'P-SRC002-Q14-b-ii','evidence':'Minimal duplicate-definition class executes later initializer; earlier one-argument signature is not retained and raises TypeError when called.'}]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
