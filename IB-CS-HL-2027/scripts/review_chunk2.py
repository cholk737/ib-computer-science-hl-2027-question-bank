"""Coordinator structural checks of isolated batches. No agent output is modified."""
from pathlib import Path
import json,re,collections,hashlib
P=Path(__file__).resolve().parents[1]
scope={r['code']:r for r in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}
inv={r['source_id']:r for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())}
manifest={r['source_id']:r for r in json.loads((P/'extraction/HISTORICAL_MANIFEST.json').read_text())}
sources={};practices={};batches=[];errors=[];warnings=[]
def error(where,msg):errors.append({'where':where,'issue':msg})
for a in sorted((P/'agents/chunk-2').glob('agent-*')):
 for f in sorted((a/'batches').glob('*.json')):
  b=json.loads(f.read_text());sid=b['source_id'];owner=manifest[sid]['agent_output']
  if str(a.relative_to(P))!=owner:error(str(f),'source shard ownership mismatch')
  batches.append({'path':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source_id':sid,'batch_id':b['batch_id']})
  for s in b['source_questions']:
   q=s['source_question_id']
   if q in sources:error(q,'duplicate source question ID')
   sources[q]=s
   if s['source_id']!=sid:error(q,'source ID does not match batch')
   if not isinstance(s['original_marks'],int) or s['original_marks']<=0:error(q,'invalid marks')
   if not s.get('original_text'):error(q,'missing source transcription')
   if not s.get('source_pdf_pages') or any(not 1<=n<=int(inv[sid]['pages']) for n in s['source_pdf_pages']):error(q,'invalid source page')
   ms=s.get('markscheme',{})
   if ms.get('status')=='uploaded_official_available':
    mid=ms.get('source_id')
    if mid not in inv or mid not in inv[sid]['paired_source_ids']:error(q,'unpaired/invalid markscheme')
    elif not ms.get('pdf_pages') or any(not 1<=n<=int(inv[mid]['pages']) for n in ms['pdf_pages']):error(q,'invalid MS pages')
   elif sid not in ['SRC-001','SRC-002']:error(q,'unexpected missing markscheme')
   status=s['relevance_status']
   if status not in ['A','B','C']:error(q,'invalid historical relevance classification')
   if status=='C' and (not s.get('exclusion_reason') or s['mappings']):error(q,'C requires exclusion and no confirmed map')
   if status in ['A','B'] and not s['mappings']:error(q,'usable source lacks mapping')
   for m in s['mappings']:
    code=m['syllabus_code']
    if code not in scope:error(q,'invalid syllabus code '+code);continue
    if m['level']!=scope[code]['level'] or m['theme']!=scope[code]['theme']:error(q,'incorrect mapping level/theme')
    if not m.get('scope_evidence') or not m.get('rationale'):error(q,'missing scope evidence/rationale')
    if m.get('review_required'):warnings.append({'where':q,'issue':'mapping review required','code':code})
   for asset in s.get('assets',[]):
    if asset.get('path') and not (P/asset['path']).is_file():error(q,'missing asset '+asset['path'])
  for p in b['practice_questions']:
   q=p['question_id']
   if q in practices:error(q,'duplicate practice ID')
   practices[q]=p
   if not p.get('unofficial') or p.get('derivation_status')!='adapted_unofficial':error(q,'unofficial status missing')
   if not p.get('question_text') or not p.get('solution') or not p.get('marking_points'):error(q,'missing substantive prompt/answer/criteria')
   if sum(x['marks'] for x in p['marking_points'])!=p['marks']:error(q,'marking points do not sum')
   if any(c not in scope for c in p['syllabus_codes']):error(q,'invalid practice codes')
   for asset in p.get('assets',[]):
    if asset.get('path') and not (P/asset['path']).is_file():error(q,'missing practice asset')
   if p.get('command_term') and not re.search(r'\b'+re.escape(p['command_term'])+r'\b',p['question_text'],re.I):warnings.append({'where':q,'issue':'prompt/command metadata mismatch','command':p['command_term']})

links=collections.defaultdict(list)
for p in practices.values():
 for q in p['source_question_ids']:
  links[q].append(p['question_id'])
  if q not in sources:error(p['question_id'],'missing source link '+q)
for q,s in sources.items():
 reuse=s.get('adaptation_reuse_question_id')
 if reuse:
  if reuse not in practices:error(q,'missing reused practice '+reuse)
  links[q].append(reuse)
 if s['relevance_status'] in ['A','B'] and not links[q]:error(q,'eligible source not converted/reused')
 if s['relevance_status']=='C' and links[q]:error(q,'excluded source has practice')

def compact(s):
 s=re.sub(r'\[\s*\d+\s*\]\s*$','',s.strip())
 s=re.sub(r'^\s*\d+\.\s*','',s)
 s=re.sub(r'^(?:\s*\([a-zivx]+\)\s*)+','',s,flags=re.I)
 return re.sub(r'\W+','',s.lower())
dupes=collections.defaultdict(list)
for q,s in sources.items():dupes[(compact(s['original_text']),s['original_marks'])].append(q)
duplicate_groups=[v for k,v in dupes.items() if len(v)>1]
summary={'sources':len(sources),'practices':len(practices),'batches':len(batches),
 'paper_counts':dict(collections.Counter(s['source_id'] for s in sources.values())),
 'classifications':dict(collections.Counter(s['relevance_status'] for s in sources.values())),
 'structural_errors':errors,'review_warnings':warnings,'duplicate_source_text_candidates':duplicate_groups,
 'batch_snapshots':batches,'all_structural_checks_pass':not errors}
(P/'audits/chunk-2/BATCH_REVIEW.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k not in ['batch_snapshots','duplicate_source_text_candidates']},indent=2))
print('Duplicate text candidate groups',len(duplicate_groups))
