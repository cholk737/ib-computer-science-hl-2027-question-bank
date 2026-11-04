from checkpoint_reviews import *
import collections
A=json.loads((O/'coverage_audit.json').read_text());assert len(A['objectives'])==74 and len(A['checked_codes'])==74
for r in A['objectives']:
 assert r['guidance_paragraphs']==S[r['code']]['guidance_paragraphs'];assert len(r['bullet_findings'])==len(r['guidance_paragraphs'])
RS=[r for f in sorted((O/'scope_reviews').glob('*.json')) for r in json.loads(f.read_text())['reviews']];assert len(RS)==len(set(r['question_id'] for r in RS))
stale=[];issues=[]
for r in RS:
 f=P/'question-bank/records'/f"{r['question_id']}.json";d=json.loads(f.read_text());assert d['theme']=='A'
 if sha(f)!=r['record_sha256']:stale.append(r['question_id'])
 for m in r['mappings']:
  code,n=m['scope_bullet_id'].split(':G');assert code==m['code'];assert S[code]['guidance_paragraphs'][int(n)-1]==m['exact_guidance'];assert m['relevance'] in ['direct','partial','supporting','reject']
 for rel,h in r['reviewed_artifact_hashes'].items():
  if sha(P/rel)!=h and r['question_id'] not in stale:stale.append(r['question_id'])
 for h in d['source_question_ids']:
  sf=P/'extraction/by-paper'/('SRC-'+h.split('-')[1][3:])/'questions'/f'{h}.json';s=json.loads(sf.read_text());assert s['source_question_id']==h;assert s['source_filename'] and s['source_pdf_pages'];assert s['markscheme']['status']
 assert set(r['verification'])==set(['mapping','technical','answer','markscheme','assets','provenance']);assert all(v['status'] in ['verified','pending','issue'] and v['evidence'] for v in r['verification'].values())
 if any(v['status']=='issue' for v in r['verification'].values()):issues.append(r['question_id'])
q=json.loads((O/'REVIEW_QUEUE.json').read_text());assert len(q['records'])==459 and q['reviewed_count']==len(RS) and q['pending_count']==459-len(RS)
out={'checkpoint':q['checkpoint'],'contract_checks_passed':True,'all_review_hashes_current':not stale,'stale_review_records':stale,'objective_audits_checked':74,'exact_guidance_and_bullet_counts_match':True,'reviewed_records':len(RS),'pending_records':459-len(RS),'source_metadata_linkages_pass':True,'review_mapping_relations':dict(collections.Counter(m['relevance'] for r in RS for m in r['mappings'])),'issue_records':issues,'question_type_reviewed':sum('question_type' in r for r in RS),'question_type_pending':sum('question_type' not in r for r in RS),'limits':'Mechanical contract/source linkage checks supplement manual record review. No complete bank coverage or Chunk4 independent verification claimed. Old review hashes changed by coordinator repairs require re-review/approval.'};atomic(O/'VALIDATION.json',out)
t=json.loads((O/'STATUS.json').read_text());t['files_created']=sorted(set(t['files_created']+['validate_reviews.py','VALIDATION.json']));t['last_self_validation']=out;atomic(O/'STATUS.json',t);print(json.dumps(out))
