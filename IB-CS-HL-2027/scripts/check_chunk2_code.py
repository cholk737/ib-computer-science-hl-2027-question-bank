"""Independent coordinator compilation/execution and targeted oracle checks."""
from pathlib import Path
import json,subprocess,sys,itertools,io,contextlib
P=Path(__file__).resolve().parents[1]
results=[];practices={}
for f in sorted((P/'agents/chunk-2').glob('*/batches/*.json')):
 for p in json.loads(f.read_text())['practice_questions']:practices[p['question_id']]=p
for p in practices.values():
 code=p.get('code','')
 if not code:continue
 test=p.get('test_code') or p.get('verification',{}).get('test_code','')
 try:
  compile(code,p['question_id'],'exec')
  proc=subprocess.run([sys.executable,'-c',code+'\n'+test],capture_output=True,text=True,timeout=4)
  results.append({'question_id':p['question_id'],'compiled':True,'execution_returncode':proc.returncode,'author_inline_assertions_rerun':bool(test),'stdout':proc.stdout[:2000],'stderr':proc.stderr[:2000],'pass':proc.returncode==0})
 except Exception as e:results.append({'question_id':p['question_id'],'pass':False,'error':str(e)})

def namespace(q):
 ns={}
 with contextlib.redirect_stdout(io.StringIO()):exec(practices[q]['code'],ns)
 return ns
oracles=[]
def oracle(name,fn):fn();oracles.append({'check':name,'pass':True})
def matrix_check():
 ns=namespace('P-SRC008-Q13-b')
 for vals in itertools.product([-1,0,2],repeat=4):
  mat=[list(vals[:2]),list(vals[2:])]
  assert ns['is_band_matrix'](mat)==all(v!=0 for v in vals)
 assert ns['is_band_matrix']([[1,2,0],[3,4,5],[0,6,7]])
 assert not ns['is_band_matrix']([[1,2,8],[3,4,5],[0,6,7]])
def extrema_check():
 for q,fn,maximize in [('P-SRC018-Q14-c','smallest_row_total',False),('P-SRC020-Q14-c','greatest_rows',True)]:
  ns=namespace(q)
  for vals in itertools.product([-2,0,3],repeat=4):
   mat=[list(vals[:2]),list(vals[2:])];totals=list(map(sum,mat));best=(max if maximize else min)(totals)
   assert ns[fn](mat)==(best,[i for i,v in enumerate(totals) if v==best])
def proper_divisor_check():
 ns=namespace('P-SRC005-Q14-c')
 for n in range(1,101):assert ns['proper_sum'](n)==sum(i for i in range(1,n) if n%i==0)
 grid=[[6,12,6],[1,8,28]];got=ns['classify_grid'](grid)
 assert got==([1,8],[6,6,28],[12])
def trimmed_mean_check():
 ns=namespace('P-SRC004-Q14-c')
 for vals in itertools.product([-1,0,2],repeat=4):
  result=ns['final_scores'](['X'],[list(vals)])
  assert result==[('X',sum(sorted(vals)[1:-1])/2)]
def receipts_check():
 ns=namespace('P-SRC001-Q15-c')
 assert ns['total_receipts']([list('SDCX'),list('XXCS')])==53
def lookup_check():
 ns=namespace('P-SRC016-Q12-d');fn=ns['score_for']
 for n in range(9):
  names=[f'{i:02}' for i in range(0,n*2,2)];scores=list(range(n))
  for i in range(-1,n*2+1):
   target=f'{i:02}';expected=scores[names.index(target)] if target in names else 'Not found'
   assert fn(names,scores,target)==expected
for name,fn in [('band matrix exhaustive small entries',matrix_check),('row-extrema negative values and ties',extrema_check),('proper divisor 1..100 and classification duplicates',proper_divisor_check),('trimmed mean including equal extrema',trimmed_mean_check),('receipt accumulation mixed seats',receipts_check),('binary search boundary and absent cases',lookup_check)]:
 try:oracle(name,fn)
 except Exception as e:oracles.append({'check':name,'pass':False,'error':repr(e)})
out={'execution_checks':results,'coordinator_oracles':oracles,'code_records':len(results),'failures':[r for r in results+oracles if not r['pass']],
 'limits':'Compilation/execution and available inline assertions rerun for every saved Python code record. Independent oracles are targeted samples, not proof of every possible input or every prose answer.'}
(P/'audits/chunk-2/CODE_REVIEW.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'code_records':len(results),'independent_oracles':oracles,'failures':out['failures']},indent=2))
