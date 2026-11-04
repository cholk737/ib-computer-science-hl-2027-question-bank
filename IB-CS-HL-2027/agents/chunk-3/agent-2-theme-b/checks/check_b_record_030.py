from pathlib import Path
import json
P=Path(__file__).resolve().parents[4];out=[]
for suffix,expression,expected in [('i','stores[1].location','Hilltop'),('ii','stores[0].bookings[0].customer_id',310),('iii','stores[2].bookings[1].end_day','2027-04-10')]:
 qid='P-SRC002-Q16-a-'+suffix;q=json.loads((P/'question-bank/records'/f'{qid}.json').read_text())
 assert q['question_text'].split('\n',1)[1].strip()==q['code'].strip()
 ns={};exec(q['code'],ns);actual=eval(expression,ns);assert actual==expected and str(actual)==q['solution']
 out.append({'question_id':qid,'status':'pass','expression':expression,'actual':actual,'actual_type':type(actual).__name__,'evidence':'Full code embedded in prompt equals separate code field; executed actual setup and evaluated requested expression.'})
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':out},indent=2)+'\n');print(json.dumps(out))
