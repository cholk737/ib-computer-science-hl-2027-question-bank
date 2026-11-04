from pathlib import Path
import json
x,y,ready=4,7,True
parts={'x_gt_4':x>4,'first_operand':(x>4)!=ready,'second_operand':y-2>4,'final':((x>4)!=ready) and (y-2>4)}
assert parts=={'x_gt_4':False,'first_operand':True,'second_operand':True,'final':True}
out={'question_id':'P-SRC006-Q04','status':'pass','parts':parts,'evidence':'Executed the exact supplied expression and each intermediate component in Python.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
