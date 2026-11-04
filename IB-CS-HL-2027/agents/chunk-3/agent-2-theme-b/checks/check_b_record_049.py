from pathlib import Path
import json,itertools,copy
P=Path(__file__).resolve().parents[4];out=[]
q=json.loads((P/'question-bank/records/P-SRC004-Q14-b.json').read_text());ns={};exec(q['code'],ns)
for data in [[],[[]],[[0,12,6],[12,12]],[[12]],[[0,1],[2,3]]]:
 before=copy.deepcopy(data);expected=sum(v==12 for row in data for v in row)
 assert ns['count_full'](data)==expected and data==before
out.append({'question_id':q['question_id'],'status':'pass','evidence':'Actual function on zero rows,empty rows,ragged rows,all/no/mixed full scores;flattened Boolean-count oracle;input preserved.'})
q=json.loads((P/'question-bank/records/P-SRC004-Q14-c.json').read_text());ns={};exec(q['code'],ns);count=0
for size in range(3,7):
 for values in itertools.product([-2,0,3],repeat=size):
  data=[list(values),[2,2,2]];before=copy.deepcopy(data);actual=ns['final_scores'](['Alpha','Beta'],data);ordered=sorted(values)
  expected=sum(ordered[1:-1])/len(ordered[1:-1])
  assert actual==[('Alpha',expected),('Beta',2.0)] and data==before;count+=1
assert ns['final_scores']([],[])==[]
out.append({'question_id':q['question_id'],'status':'pass','cases':count+1,'evidence':'Independent sorting/drop-first-last oracle for all109? rows length3..6 over three numeric values,plus empty outer lists;includes all-equal,duplicates,negative values,mixed row lengths,names pairing,input preserved.'})
out[-1]['evidence']=out[-1]['evidence'].replace('all109?','all'+str(count))
Path(__file__).with_suffix('.json').write_text(json.dumps({'results':out},indent=2)+'\n');print(json.dumps(out))
