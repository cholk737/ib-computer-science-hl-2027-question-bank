from pathlib import Path
import json
from types import SimpleNamespace
P=Path(__file__).resolve().parents[4];results=[]
q=json.loads((P/'question-bank/records/P-SRC002-Q14-e.json').read_text());ns={};exec(q['code'],ns);n=0
for days in [0,1,4,5.5]:
 for rate in [0,1,18.5,100]:
  obj=SimpleNamespace(rate=rate,get_days=lambda d=days:d)
  assert ns['get_cost'](obj)==days*rate;n+=1
results.append({'question_id':q['question_id'],'status':'pass','cases':n,'evidence':'Actual stored method executed against stated instance interface; zero and fractional duration/rate combinations included.'})
q=json.loads((P/'question-bank/records/P-SRC002-Q15-a.json').read_text());ns={};exec('class Depot:\n def __init__(self,location):self.location=location',ns);exec(q['solution'],ns)
assert isinstance(ns['depot'],ns['Depot']) and ns['depot'].location=='North Pier'
results.append({'question_id':q['question_id'],'status':'pass','evidence':'Actual assignment executed with minimal stated constructor fixture; correct class,argument,and variable binding.'})
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(json.dumps(results))
