import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'syllabus/SYLLABUS_MASTER.json').exists())
SNAPSHOT=HERE/'SRC002_REVIEW_INPUT_SNAPSHOT.json'
def sha(r):return hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def snapshot():
 if SNAPSHOT.exists():return json.loads(SNAPSHOT.read_text())
 scope={r['code']:r for r in json.loads((ROOT/'syllabus/SYLLABUS_MASTER.json').read_text())};pairs=[]
 for f in (ROOT/'agents/chunk-3/agent-1-theme-a/scope_reviews').glob('*.json'):
  pairs.extend((f,r) for r in json.loads(f.read_text()).get('reviews',[]) if r['question_id'].startswith('P-SRC002-'))
 f=ROOT/'agents/chunk-3/agent-2-theme-b/question_reviews.json';pairs.extend((f,r) for r in json.loads(f.read_text())['reviews'] if r['question_id'].startswith('P-SRC002-'))
 result={r['question_id']:{'author_review':r,'author_review_sha256':sha(r),'author_path':str(f.relative_to(ROOT)),'question':json.loads((ROOT/f"question-bank/records/{r['question_id']}.json").read_text()),'scope':{m['code']:scope[m['code']] for m in r['mappings']}} for f,r in sorted(pairs,key=lambda fr:fr[1]['question_id'])};SNAPSHOT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');return result

def dossier(ids):
 snap=snapshot()
 for qid in ids:
  r=snap[qid];q=r['question'];a=r['author_review'];print('\nID',qid,'MARKS',q['marks'],'PROMPT',q['question_text'],'\nANSWER',q['solution'],'\nCRITERIA',q['marking_points']);print('MAPPINGS',[(m['code'],m['scope_bullet_id'],m['relevance'],m['assessed_skill'],m.get('statement_relevance'),m.get('coverage_limit')) for m in a['mappings']]);print('ISSUES',a.get('issues',[]));print('CHECKS',a.get('checks',[]));print('DIMENSIONS',{k:v.get('status') if isinstance(v,dict) else v for k,v in a['verification'].items()})
  for code,s in r['scope'].items():print('SCOPE',code,s['statement'],s['guidance'])

def save(decisions):
 snap=snapshot();p=HERE/'integration_review_SRC002.json';data=json.loads(p.read_text()) if p.exists() else {'reviewer':'/root/searchable_bank_audit','date':'2026-11-04','kind':'bounded independent Chunk3 mapping/review integration audit; not Chunk4 full bank certification','reviews':[],'pending_question_ids':list(snap)};by={r['question_id']:r for r in data['reviews']}
 for qid,outcome,rationale,flags in decisions:
  r=snap[qid];by[qid]={'question_id':qid,'author_review_sha256':r['author_review_sha256'],'record_sha256':r['author_review']['record_sha256'],'author_review_path':r['author_path'],'outcome':outcome,'rationale':rationale,'technical_issue_flags_retained':flags,'checked':['Full actual adapted prompt and all marking criteria/solution read','Every mapped statement and complete exact guide guidance read','Aspect relevance and direct/partial/supporting boundaries independently assessed'],'limits':'Acceptance covers described mapping evidence and retained issue flags only. Original-PDF provenance and full answer correctness are not newly certified unless explicit reproduction is cited.'}
 data['reviews']=sorted(by.values(),key=lambda r:r['question_id']);data['pending_question_ids']=[qid for qid in snap if qid not in by];data['counts']={'reviewed':len(by),'accept_mapping_evidence':sum(r['outcome']=='accept_mapping_evidence' for r in by.values()),'needs_revision':sum(r['outcome']=='needs_revision' for r in by.values()),'remaining':len(data['pending_question_ids'])};t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');os.replace(t,p)
 sp=HERE/'STATUS.json';status=json.loads(sp.read_text());status.update(checkpoint='C3-A3-SRC002-'+str(len(by)).zfill(3),current='Independent SRC002 per-question integration review',src002_review_counts=data['counts'],last_reviewed_question_id=decisions[-1][0],exact_next_action='Read next SRC002 dossier: '+(data['pending_question_ids'][0] if data['pending_question_ids'] else 'None; coordinator validate review hashes and integration recommendations'));st=sp.with_name(sp.name+'.tmp');st.write_text(json.dumps(status,indent=2));os.replace(st,sp);print(data['counts'])
if __name__=='__main__':
 import sys
 dossier(sys.argv[1:] or list(snapshot())[:3])
