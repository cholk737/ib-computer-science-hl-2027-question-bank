from pathlib import Path
import json,math,io,contextlib,itertools,sqlite3
from types import SimpleNamespace
O=Path(__file__).resolve().parent
results=[]
for path in sorted((O/'batches').glob('*.json')):
 b=json.loads(path.read_text())
 for p in b['practice_questions']:
  assert sum(x['marks'] for x in p['marking_points'])==p['marks']
  if not p.get('code'):continue
  ns={}; capture=io.StringIO()
  with contextlib.redirect_stdout(capture):exec(p['code'],ns)
  if 'digit_total' in ns:
   assert [ns['digit_total'](n) for n in [0,7,3407,1216]]==[0,7,14,10]
  if 'count_full' in ns:
   assert [ns['count_full'](v) for v in [[],[[]],[[12,12],[0,12]],[[1,2],[3,4]]]]==[0,0,3,0]
  if 'final_scores' in ns:
   rows=[[1,1,5,5],[7,7,7],[-3,5,1,4],[3,2,1]]
   expected=[sum(sorted(r)[1:-1])/(len(r)-2) for r in rows]
   got=ns['final_scores'](['A','B','C','D'],rows)
   assert [v for _,v in got]==expected
  if 'split_names' in ns:
   assert ns['split_names']([])==([],[])
   assert ns['split_names']([' Okafor, Ada ','Diaz, Ana Maria'])==(['Okafor','Diaz'],['Ada','Ana Maria'])
  if 'sort_names' in ns:
   for surnames,first in [([],[]),(['Z','A','A'],['z','a1','a2']),(['B'],['b'])]:
    before=list(zip(surnames,first));ns['sort_names'](surnames,first)
    assert list(zip(surnames,first))==sorted(before,key=lambda pair:pair[0])
  if 'summarize' in ns:
   it=iter([False,0,-1,1000,5,9,6]);assert ns['summarize'](lambda:next(it))==(0,1000,204)
   it=iter([7]*5);assert ns['summarize'](lambda:next(it))==(7,7,7)
  if 'product' in ns:assert capture.getvalue()=='120\n'
  if 'values' in ns:assert capture.getvalue()=='6\n12\n24\n'
  if 'n' in ns and 'x' in ns:assert (ns['n'],ns['x'],capture.getvalue())==(0,15,'15\n')
  if 'average' in ns and callable(ns['average']):
   for values in [[3],[1,2,9],[-4,2]]:assert ns['average'](values)==sum(values)/len(values)
  if 'count_above' in ns:
   assert ns['count_above']([],0)==0 and ns['count_above']([2,2,2],2)==0 and ns['count_above']([1,3,4],2)==2
  if 'score_for' in ns:
   assert ns['score_for']([],[],'A')=='Not found'
   for target,expected in [('A',1),('C',2),('F',3),('B','Not found'),('Z','Not found')]:assert ns['score_for'](['A','C','F'],[1,2,3],target)==expected
  if 'echo' in ns:
   for n in [-3,0,1,4]:
    out=io.StringIO()
    with contextlib.redirect_stdout(out):ns['echo'](n)
    assert len(out.getvalue().splitlines())==(1 if n<=0 else 2*n+1)
  if 'route' in ns:
   class Stack:
    def __init__(self,data):self.data=data[:]
    def isEmpty(self):return not self.data
    def pop(self):return self.data.pop()
   class Queue:
    def __init__(self):self.data=[]
    def enqueue(self,value):self.data.append(value)
   st=Stack(['Zed','Nora','Mika','Ada']);early,late=Queue(),Queue();ns['route'](st,early,late)
   assert not st.data and early.data==['Ada','Mika'] and late.data==['Nora','Zed']
  if 'is_upper' in ns:
   assert ns['is_upper']([]) and ns['is_upper']([[3]])
   for v in itertools.product([0,1],repeat=4):
    mat=[list(v[:2]),list(v[2:])];assert ns['is_upper'](mat)==(mat[1][0]==0)
   assert not ns['is_upper']([[1,2],[-1,4]])
  if 'identify' in ns:
   for u,l,label in [(True,True,'BOTH'),(True,False,'UPPER'),(False,True,'LOWER'),(False,False,'NONE')]:
    ns['is_upper']=lambda m:u;ns['is_lower']=lambda m:l;assert ns['identify']([])==label
  if 'r' in ns and 's' in ns and 'a' in ns:assert (ns['n'],ns['s'],ns['r'],capture.getvalue())==(0,3,10,'10\n')
  if 'grade' in ns:
   assert [ns['grade'](n) for n in range(101)]==[min(7,1+n//10) for n in range(101)]
  if 'resit_names' in ns:
   assert ns['resit_names']([],[])==[] and ns['resit_names'](['A','B','C'],[1,2,1])==['A','C']
  if 'letter_grades' in ns:
   for marks in [[0,15,30],[1,16,32],[7],[2,2,2],[0,90,100]]:
    mean=sum(marks)/len(marks);expected=['A' if x>mean+15 else 'C' if x<mean-15 else 'B' for x in marks]
    assert ns['letter_grades'](marks)==expected
  if 'estimate' in ns:
   for kind,count,sale,days,material in [('small',1,220000,17,100000),('small',10,220000,17,100000),('large',1,400000,23,190000),('large',5,400000,23,190000)]:
    assert ns['estimate'](kind,count)==count*sale-500000-count*days*2500-count*material
  if 'net_profit' in ns:
   for months in [1,7,12]:assert ns['net_profit'](100000,months)==100000-4500*months
  if 'item' in ns:
   assert ns['item'].identifier=='LAB-27'
   if p['question_id'].endswith('d-ii'):assert ns['item'].colour==ns['Asset'].BLACK
  if 'add_asset' in ns:
   asset=object()
   for slots,expected in [([],-1),([object()],-1),([None],0),([object(),None],1)]:
    owner=SimpleNamespace(slots=slots);got=ns['add_asset'](owner,asset);assert got==expected
    if expected>=0:assert slots[expected] is asset
  if 'Rental' in ns:
   assert [ns['Rental']().pay(h) for h in [0,5,6]]==[4,4,0]
  if 'PoweredRental' in ns:
   assert [ns['PoweredRental']().pay(h) for h in [0,5,6]]==[4,19,18]
  if 'remove_asset' in ns:
   asset=SimpleNamespace(identifier='A');other=SimpleNamespace(identifier='B');slots=[None,asset,other]
   owner=SimpleNamespace(slots=slots);assert ns['remove_asset'](owner,'A') is asset and slots==[None,None,other]
   assert ns['remove_asset'](owner,'Z') is None
  if 'remove_target' in ns:
   class Stack:
    def __init__(self):self.data=[]
    def isEmpty(self):return not self.data
    def push(self,x):self.data.append(x)
    def pop(self):return self.data.pop()
   for target in ['A','B','C']:
    stack=Stack();items=[SimpleNamespace(identifier=x) for x in ['A','B','C']];stack.data=items[:]
    removed=ns['remove_target'](stack,target,Stack)
    assert removed is next(x for x in items if x.identifier==target)
    assert [x.identifier for x in stack.data]==[x.identifier for x in items if x.identifier!=target]
  results.append({'question_id':p['question_id'],'code_compiles':True,'specific_edge_tests':'passed'})
(O/'technical_checks.json').write_text(json.dumps(results,indent=2))
print('Code and marking checks passed:',len(results))

# SQL is stored as a query answer rather than as Python code.
for f in (O/'batches').glob('SRC-033-*.json'):
 for p in json.loads(f.read_text())['practice_questions']:
  if p['question_id']=='P-SRC033-Q03-b':
   db=sqlite3.connect(':memory:');db.executescript("CREATE TABLE Product(ProductID,SupplierID,ProductName,Description);CREATE TABLE Stock(ProductID,Quantity);INSERT INTO Product VALUES(1,'S','A','fruity'),(2,'T','B','fruity'),(3,'U','C','fruity'),(4,'V','D','fruity'),(5,'W','E','dry');INSERT INTO Stock VALUES(1,25),(2,35),(3,24),(4,36),(5,30);")
   assert db.execute(p['solution']).fetchall()==[('S','A'),('T','B')]
   db.close()
print('SQL boundary/join query check passed')
