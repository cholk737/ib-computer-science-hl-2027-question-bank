"""Coordinator checks of source mark sequences and selected technical findings."""
from pathlib import Path
import csv,json,re,collections,runpy,sys,io,contextlib
from pypdf import PdfReader
P=Path(__file__).resolve().parents[1]
A=P/'agents/chunk-1/agent-3-specimen'
doc=PdfReader(P/'sources/2027-specimen/Specimen Papers 2027 - English.pdf')
rows=list(csv.DictReader((A/'specimen_question_index.csv').open()))
by_page=collections.defaultdict(list)
for r in rows:by_page[int(r['source_pdf_page'])].append(int(r['marks']))
sequences=[]
for n in list(range(4,19))+list(range(50,62)):
 text=doc.pages[n-1].extract_text(extraction_mode='layout')
 marks=[int(m[1]) for line in text.splitlines() if (m:=re.search(r'\[(\d+)\]\s*$',line))]
 sequences.append({'pdf_page':n,'source_marks':marks,'index_marks':by_page[n],'pass':marks==by_page[n]})
assert all(r['pass'] for r in sequences)
totals=collections.defaultdict(int)
for r in rows:totals[r['paper']]+=int(r['marks'])
assert dict(totals)=={'HL Paper 1':80,'HL Paper 2':80}
assert sum(int(r['marks']) for r in rows if r['paper']=='HL Paper 1' and r['section']=='A')==56
assert sum(int(r['marks']) for r in rows if r['paper']=='HL Paper 1' and r['section']=='B')==24
assert len(rows)==54 and len({r['id'] for r in rows})==54

# Independently execute the visually checked source MS indentation, bounded.
fn=runpy.run_path(str(A/'source_find_player_transcription.py'))['find_player']
class Node:
 def __init__(self,name,score,next=None):self.name=name;self.score=score;self.next=next
class Owner:pass
def run_case(head,name):
 owner=Owner();owner.head=head;events=0
 def bound(frame,event,arg):
  nonlocal events
  if frame.f_code==fn.__code__ and event=='line':
   events+=1
   if events>100:raise RuntimeError('bounded nontermination')
  return bound
 out=io.StringIO();outcome='returned'
 try:
  sys.settrace(bound)
  with contextlib.redirect_stdout(out):fn(owner,name)
 except Exception as e:outcome=type(e).__name__+': '+str(e)
 finally:sys.settrace(None)
 return {'outcome':outcome,'stdout':out.getvalue()}
cases={
 'head_match':run_case(Node('A',10,Node('B',20)),'A'),
 'later_match':run_case(Node('A',10,Node('B',20)),'B'),
 'absent':run_case(Node('A',10),'X'),
 'empty':run_case(None,'X')}
assert cases['head_match']['stdout']=='10\n'
assert cases['later_match']['outcome'].startswith('RuntimeError') and cases['absent']['outcome'].startswith('RuntimeError')
assert cases['empty']['outcome'].startswith('AttributeError')
class Passenger:
 def __init__(self,email):self._email=email
p=Passenger('example');p._email='changed';assert p._email=='changed'
def source_iter(x):
 s=0
 while x>0:s+=x;x-=1
 return s
def source_recur(x):return 0 if x==0 else x+source_recur(x-1)
assert source_iter(6)==source_recur(6)==21 and source_iter(-1)==0
try:source_recur(-1);raise AssertionError('expected failure')
except RecursionError:negative_recursion='RecursionError'

# Flowchart independently traced from rendered PDF50: i=1..N, j=i+1..N.
flow=[]
for i in range(1,4):
 flow.append(i)
 for j in range(i+1,4):flow.append(j)
assert flow==[1,2,3,2,3,3]
report={'date':'2026-11-04','leaf_parts':len(rows),'paper_totals':dict(totals),
        'page_mark_sequences':sequences,'source_code_defect_cases':cases,
        'privacy_external_write':'succeeds','recursive_negative_input':negative_recursion,
        'flowchart_N3_output':flow,'all_assertions_passed':True,
        'visual_samples':[35,50,56,57,84,153],
        'visual_note':'Specimen compilation physical PDF pages independently viewed by coordinator; guide samples recorded separately.'}
(P/'audits/SPECIMEN_INTEGRATION_CHECK.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='page_mark_sequences'},indent=2))
