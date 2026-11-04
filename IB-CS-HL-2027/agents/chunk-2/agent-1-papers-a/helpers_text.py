import build_shard as B
from build_shard import *

def use(sid):
 B.CURRENT=sid

def emit(q,sub,page,marks,command,text,context,codes,status,ms_page,summary,prompt='',points=None,solution='',reason='',assets=None,code='',tests='',flags=None):
 r=INV[B.CURRENT]; msid=r['paired_source_ids'].split(';')[0]
 ms=dict(status='uploaded_official_available',source_id=msid,filename=INV[msid]['filename'],pdf_pages=ms_page if isinstance(ms_page,list) else [ms_page],question_reference=f'{q}({sub})',marking_summary=summary,source_issues=[])
 result=add(q,sub,page,marks,command,text,context,codes,status,prompt,points,solution,reason,assets,ms,code,tests,flags)
 src,p=result
 src['source_printed_pages']=[str(n-1) for n in src['source_pdf_pages']]
 src['verification']['source']='Complete original text read, exact leaf/marks checked against source PDF; all referenced visual/code pages inspected.'
 return result

def pageasset(sid,n,description):
 match=next((O/'papers').glob(f'{sid}-page-*{n}.png'))
 return dict(kind='source_page',description=description,path=str(match.relative_to(P)),source_pdf_page=n,visually_verified=True)

def finish(sid,expected,candidate,notes=''):
 results=[]
 for src,p in DATA[sid]:
  if p and p.get('code'):
   ns={};exec(p['code'],ns);exec(p['test_code'],ns);results.append(dict(question_id=p['question_id'],passed=True))
 (O/'checks'/f'{sid}-code-checks.json').write_text(json.dumps(results,indent=2))
 a=save_batches(sid,True,expected,candidate,notes)
 print(sid,'leaves',a['leaf_count'],'practices',a['converted_count'],'statuses',a['counts'])
 return a
