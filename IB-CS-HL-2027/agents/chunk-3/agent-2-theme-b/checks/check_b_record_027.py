from pathlib import Path
import json,itertools
from types import SimpleNamespace as N
P=Path(__file__).resolve().parents[4]
class Example:
 def _add_booking(self):return 'called externally'
assert Example()._add_booking()=='called externally'
q=json.loads((P/'question-bank/records/P-SRC002-Q15-c.json').read_text());ns={};exec(q['code'],ns);n=0
for count in range(6):
 for dates in itertools.product(['2027-01-01','2027-02-01'],repeat=count):
  active=[N(start_day=d) for d in dates];trailing=[None,N(start_day='2027-01-01')];data=N(used=count,bookings=active+trailing);before=data.bookings[:]
  result=ns['bookings_on'](data,'2027-01-01');expected=[b for b in active if b.start_day=='2027-01-01']
  assert len(result)==len(expected) and all(a is b for a,b in zip(result,expected));assert data.bookings==before;n+=1
out={'status':'pass','results':[{'question_id':'P-SRC002-Q15-b','evidence':'External call to single-underscore method succeeds in a minimal stated fixture; underscore alone does not prohibit calling.'},{'question_id':q['question_id'],'cases':n,'evidence':'All active-prefix sizes0..5 over two dates, including absent/all matches; ignored trailing None and matching inactive object; identities/order/input preserved.'}]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
