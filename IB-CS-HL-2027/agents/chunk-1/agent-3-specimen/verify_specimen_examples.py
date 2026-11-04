"""Reproducible checks of selected uploaded specimen examples; does not alter originals."""
from pathlib import Path
import json,sys,io,contextlib
OUT=Path(__file__).resolve().parent
checks=[]
def check(name,actual,expected,reference):
 assert actual==expected,(name,actual,expected)
 checks.append(dict(check=name,actual=actual,expected=expected,passed=True,source_reference=reference))
check('hexadecimal AC',f'{int("AC",16):08b}','10101100','P1 Q1b; PDF4/MS23')
check('truth table difference/borrow',[[x,y,x^y,int(not x and y)] for x,y in [(0,0),(0,1),(1,0),(1,1)]],[[0,0,0,0],[0,1,1,1],[1,0,1,0],[1,1,0,0]],'P1 Q1c; PDF4/MS23')
output=[]
for i in range(1,4):
 output.append(i)
 for j in range(i+1,4):output.append(j)
check('flowchart output N3',output,[1,2,3,2,3,3],'P2 Q7b; PDF50/MS76; flowchart visually checked')
stack=[]
for op,v in [('push',1),('push',2),('push',9),('peek',None),('pop',None),('push',8),('push',10),('pop',None),('push',6)]:
 if op=='push':stack.append(v)
 elif op=='pop':stack.pop()
 else:peek=stack[-1]
check('stack bottom to top',stack,[1,2,8,6],'P2 Q7e; PDF53/MS78')
MAT=[[2,7,1],[8,9,0]]
a=b=0
for row in range(0,2):
 for col in range(0,3):
  a=a+1
  item=MAT[row][col]
  if item%2!=0:b=b+item
check('nested-loop outputs',[a,b],[6,17],'P2 Q8d; PDF55/MS79')
set1={3,6,2,9,10};set2={2,6,1,11}
check('set membership',12 in set1,False,'P2 Q10ci; PDF59/MS82')
check('set intersection',sorted(set1&set2),[2,6],'P2 Q10cii; PDF59/MS82')
def iter_source(x):
 s=0
 while x>0:
  s=s+x;x=x-1
 return s
def recur_source(x):
 if x!=0:return x+recur_source(x-1)
 else:return x
check('iter6',iter_source(6),21,'P2 Q11ci; PDF60/MS83')
check('recursive nonnegative sample',[recur_source(x) for x in [0,1,6]],[iter_source(x) for x in [0,1,6]],'P2 Q11cii; PDF60/MS83')
def ticket_price(sold,capacity,initial):
 percent_sold=sold*100/capacity
 if percent_sold>=10 and percent_sold<=50.0:price=initial*1.5
 elif percent_sold>50.0:price=initial*3
 else:price=initial
 return price
check('ticket price boundaries',[ticket_price(x,100,100) for x in [0,9,10,50,51]],[100,100,150,150,300],'P2 Q9c; PDF58/MS80')

# Literal transcription from visually inspected printed MS PDF84, component p22.
source='''def find_player(self, name):
    temp = self.head
    found = False
    while temp != None:
        if temp.name == name:
            found = True
            print(temp.score)
            break
    else:
            temp = temp.next
    if found == False:
        print("Not found")
'''
(OUT/'source_find_player_transcription.py').write_text('# Uploaded official specimen MS PDF84, printed22; indentation preserved. Known bug.\n'+source)
scope={};exec(compile(source,'source_find_player_transcription.py','exec'),scope)
class Node:
 def __init__(self,name,score,next=None):self.name=name;self.score=score;self.next=next
class Linked:
 def __init__(self,head):self.head=head
class StepLimit(Exception):pass
def bounded_run(obj,name):
 events=0;stream=io.StringIO()
 def trace(frame,event,arg):
  nonlocal events
  if event=='line' and frame.f_code.co_filename=='source_find_player_transcription.py':
   events+=1
   if events>100:raise StepLimit('100 source-line events without termination')
  return trace
 try:
  with contextlib.redirect_stdout(stream):
   sys.settrace(trace)
   scope['find_player'](obj,name)
  result={'outcome':'returned','stdout':stream.getvalue()}
 except Exception as e:result={'outcome':type(e).__name__,'message':str(e),'stdout':stream.getvalue()}
 finally:sys.settrace(None)
 return result
bug_tests={
 'matching_head':bounded_run(Linked(Node('A',10)),'A'),
 'matching_second_node':bounded_run(Linked(Node('A',10,Node('B',20))),'B'),
 'absent_name_nonempty':bounded_run(Linked(Node('A',10)),'Z'),
 'empty_list':bounded_run(Linked(None),'Z')}
assert bug_tests['matching_head']['outcome']=='returned'
assert bug_tests['matching_second_node']['outcome']=='StepLimit'
assert bug_tests['absent_name_nonempty']['outcome']=='StepLimit'
assert bug_tests['empty_list']['outcome']=='AttributeError'

# Single underscore does not enforce private access in Python.
class Passenger:
 def __init__(self,name,email,price):
  self._passenger_name=name;self._email=email;self._ticket_price=price
p=Passenger('A','old@example.net',240)
read_from_outside=p._email
p._email='changed@example.net'
privacy={'external_read_succeeded':read_from_outside=='old@example.net','external_write_succeeded':p._email=='changed@example.net'}
assert all(privacy.values())

old_limit=sys.getrecursionlimit()
try:
 sys.setrecursionlimit(300)
 try:recur_source(-1);negative='returned'
 except RecursionError:negative='RecursionError'
finally:sys.setrecursionlimit(old_limit)
assert negative=='RecursionError' and iter_source(-1)==0
report={'ordinary_example_checks':checks,'source_defects_or_limitations':{
 'SP-01':{'reference':'HL P2 Q12a MS PDF84/component22','source_code_transcription':'source_find_player_transcription.py','result':bug_tests,'finding':'else is aligned with while; temp never advances for a nonmatching head; empty list dereferences None'},
 'SP-02':{'reference':'HL P2 Q9aii PDF56/component20 and MS80/component18','result':privacy,'finding':'single underscore expresses non-public convention but does not enforce privacy'},
 'SP-04':{'reference':'HL P2 Q11cii PDF60/component24 and MS83/component21','iter_minus_one':iter_source(-1),'recur_minus_one':negative,'finding':'official recursive sample assumes nonnegative x; no input domain is stated in question'}}}
(OUT/'technical_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'ordinary_checks_passed':len(checks),'source_bug_cases':bug_tests,'privacy':privacy,'negative_recursion':negative},indent=2))
