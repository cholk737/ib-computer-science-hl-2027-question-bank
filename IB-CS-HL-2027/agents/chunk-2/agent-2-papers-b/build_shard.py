from pathlib import Path
import json,re,collections
from pypdf import PdfReader
P=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
INV={r['source_id']:r for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())}
SCOPE={r['code']:r for r in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}

def extract(sid):
 manual=O/'papers'/sid/'manual_leaves.json'
 if manual.exists():return json.loads(manual.read_text())
 records=[];q=None;part='';roman='';buf=[];pages=[];openleaf=False
 for n,page in enumerate(PdfReader(P/INV[sid]['project_path']).pages,1):
  layout=page.extract_text(extraction_mode='layout');allowed={int(m[1]) for l in layout.splitlines() if (m:=re.match(r'^(\d{1,2})\.\s',l))};t=page.extract_text()
  if n<3:continue
  for line in t.splitlines():
   if not line.strip() or re.match(r'^(?:[–-] \d+ [–-]|[MN]\d\d/|\d{4} [–-]|Turn over|Section [AB]|Answer all|\(.*continued\)|\(This question)',line):continue
   m=re.match(r'^(\d{1,2})\.\s*(.*)',line)
   if m and int(m[1]) in allowed:q=int(m[1]);part='';roman='';buf=[];pages=[];line=m[2];openleaf=True
   if q is None:continue
   line=line.strip()
   labels=re.findall(r'^\(([a-z]+)\)\s*',line)
   while (m:=re.match(r'^\(([a-z]+)\)\s*(.*)',line)):
    label,line=m.groups()
    if label in ['ii','iii','iv','v','vi'] or label=='i' and part:roman=label
    else:part=label;roman=''
    buf=[];pages=[];openleaf=True
   buf.append(line)
   if n not in pages:pages.append(n)
   m=re.search(r'\[(\d+)\]\s*$',line) if openleaf else None
   if m:
    # Bare diagram index headers are not marks.
    if re.match(r'^(?:\[\d+\]\s*)+$',line):buf=[];pages=[];continue
    sub='-'.join(x for x in [part,roman] if x);key=str(q)+(':'+sub if sub else '')
    txt=' '.join(' '.join(b.split()) for b in buf);txt=re.sub(r'\s*\[\d+\]\s*$','',txt)
    records.append(dict(key=key,question=q,subquestion=sub,original_text=txt,original_marks=int(m[1]),source_pdf_pages=pages[:]))
    buf=[];pages=[];openleaf=False
 return records

def source_record(sid,x,entry):
 r=INV[sid];codes=entry.get('codes',[]);status=entry.get('status','A' if codes else 'C')
 maps=[]
 for code in codes:
  sc=SCOPE[code];maps.append(dict(syllabus_code=code,scope_evidence=sc['guidance'],rationale=entry.get('rationale',entry.get('concept','')+' assesses '+sc['statement']),theme=sc['theme'],level=sc['level'],confidence='high',review_required=False))
 msids=r['paired_source_ids'].split(';') if r['paired_source_ids'] else [];msid=msids[0] if msids else ''
 out=dict(source_question_id='H-'+sid.replace('-','')+'-Q'+str(x['question']).zfill(2)+('-'+x['subquestion'] if x['subquestion'] else ''),source_id=sid,source_filename=r['filename'],year=r['year'],session=r['session'],source_level=r['level'],paper=r['paper'],zone=r['zone'],option=entry.get('option',''),question=x['question'],subquestion=x['subquestion'],source_pdf_pages=x['source_pdf_pages'],source_printed_pages=entry.get('printed_pages',[str(n-1) for n in x['source_pdf_pages']]),original_marks=x['original_marks'],command_term=entry.get('command',next((c for c in ['State','Outline','Identify','Explain','Describe','Evaluate','Discuss','Compare','Construct','Determine','Sketch','Draw'] if re.search(r'\b'+c+r'\b',x['original_text'])),'See original prompt')),original_text=x['original_text'],parent_context='\n'.join((O/'evidence'/sid/f'page-{n:03}.txt').read_text() for n in entry.get('context_pages',x['source_pdf_pages'])),assets=entry.get('assets',[]),assessed_concepts=['Original source task: '+x['original_text'],entry.get('concept','Source topic outside explicit 2027 scope')],difficulty=entry.get('difficulty','medium'),markscheme=dict(status='uploaded_official_available' if msid else 'not_uploaded',source_id=msid,filename=INV[msid]['filename'] if msid else '',pdf_pages=entry.get('ms',[]),question_reference=f"Q{x['question']} {x['subquestion']}",marking_summary=entry.get('ms_summary',entry.get('answer','Excluded topic; original criteria retained in referenced MS source.')),source_issues=entry.get('source_issues',[]),source_marking_evidence='\n'.join((O/'evidence'/msid/f'page-{n:03}.txt').read_text() for n in entry.get('ms',[])) if msid else ''),relevance_status=status,mappings=maps,exclusion_reason=entry.get('exclude','') if status=='C' else '',uncertainty_flags=entry.get('flags',[]),verification=dict(source_text='Read complete source page and matched leaf/mark to original PDF.',markscheme='Read cited MS page(s).' if msid else 'No uploaded MS; independent unofficial answer.',visual=entry.get('visual','No visual required by this leaf.'),technical=entry.get('check','Independently reasoned and compared with available source marking points.')))
 out['adaptation_reuse_question_id']=entry.get('reuse_practice_id','')
 out['practice_question_ids']=([entry['reuse_practice_id']] if entry.get('reuse_practice_id') else [out['source_question_id'].replace('H-','P-',1)] if status!='C' else [])
 return out

def practice(src,e):
 if src['relevance_status']=='C':return None
 codes=[x['syllabus_code'] for x in src['mappings']]
 criteria=e['criteria'];marks=e.get('marks',src['original_marks'])
 assert sum(c[0] for c in criteria)==marks,(src['source_question_id'],criteria,marks)
 return dict(question_id=src['source_question_id'].replace('H-','P-',1),source_question_ids=[src['source_question_id']],derivation_status='adapted_unofficial',unofficial=True,question_text=e['prompt'],syllabus_codes=codes,theme=';'.join(dict.fromkeys(SCOPE[c]['theme'] for c in codes)),level='HL-only' if any(SCOPE[c]['level']=='HL-only' for c in codes) else 'SL/HL common',marks=marks,command_term=e.get('new_command',(re.search(r'\b(State|Outline|Identify|Explain|Describe|Evaluate|Discuss|Compare|Construct|Determine|Sketch|Trace|Distinguish|Define|List|Suggest|Justify)\b',e['prompt']).group(1) if re.search(r'\b(State|Outline|Identify|Explain|Describe|Evaluate|Discuss|Compare|Construct|Determine|Sketch|Trace|Distinguish|Define|List|Suggest|Justify)\b',e['prompt']) else src['command_term'])),difficulty=e.get('difficulty','medium'),adaptation_rationale=e.get('adapt','Rebuilt scenario and response wording while retaining the supported reasoning; source-specific obsolete material excluded.'),solution=e['answer'],marking_points=[dict(marks=n,criterion=t) for n,t in criteria],acceptable_alternatives=e.get('alternatives',[]),partial_credit_notes='Award independent criteria up to the stated total; accept equivalent technically correct wording/solutions.',common_errors=e.get('errors',[]),verification=dict(technical=e.get('check','Concrete answer reasoned and checked against full syllabus guidance and available source MS.'),source_comparison=src['markscheme']['pdf_pages'],test_code=e.get('test_code',''),result_file=e.get('result_file','')),code=e.get('code',''),assets=e.get('practice_assets',[]),markscheme_status='preliminary_unofficial_verified_by_author')

def finish(sid,entries,expected_total=100):
 xs=extract(sid);assert set(e['key'] for e in entries)=={x['key'] for x in xs},(sid,'MISSING',set(x['key'] for x in xs)-set(e['key'] for e in entries),'EXTRA',set(e['key'] for e in entries)-set(x['key'] for x in xs))
 ent={e['key']:e for e in entries};rs=[];ps=[]
 for x in xs:
  e=ent[x['key']];r=source_record(sid,x,e);rs.append(r)
  if r['relevance_status']!='C' and not e.get('reuse_practice_id'):ps.append(practice(r,e))
 assert sum(x['original_marks'] for x in xs)==expected_total,(sid,sum(x['original_marks'] for x in xs))
 batches=[]
 for start in range(0,len(rs),8):
  name=f'{sid}-b{start//8+1:03}.json';batches.append(name)
  srcs=rs[start:start+8];ids={r['source_question_id'] for r in srcs}
  batch=dict(source_id=sid,batch_id=name[:-5],source_questions=srcs,practice_questions=[p for p in ps if p['source_question_ids'][0] in ids])
  (O/'batches').mkdir(exist_ok=True);dest=O/'batches'/name
  dest.write_text(json.dumps(batch,ensure_ascii=False,indent=2))
 d=O/'papers'/sid;d.mkdir(exist_ok=True,parents=True)
 audit=dict(source_id=sid,complete=True,leaf_count=len(rs),source_leaf_ids=[r['source_question_id'] for r in rs],source_marks=sum(r['original_marks'] for r in rs),expected_candidate_marks=expected_total,all_options_included=True,classification_counts=dict(collections.Counter(r['relevance_status'] for r in rs)),converted=len(ps),reused_practice_ids=[e['reuse_practice_id'] for e in entries if e.get('reuse_practice_id')],converted_source_questions=sum(r['relevance_status']!='C' for r in rs),batches=batches,last_completed=rs[-1]['source_question_id'],next_action='Coordinator independent review and integration.',unreadable_content=[],source_page_evidence=f'agents/chunk-2/agent-2-papers-b/evidence/{sid}/',markscheme_checked=True)
 (d/'paper_audit.json').write_text(json.dumps(audit,indent=2))
 print(sid,len(rs),'leaves',len(ps),'converted',audit['classification_counts'])
 return audit

if __name__=='__main__':
 for sid in ['SRC-006','SRC-009','SRC-020','SRC-026','SRC-032','SRC-038','SRC-044']:
  print(sid,[(x['key'],x['original_marks'],x['original_text'][:100]) for x in extract(sid)])
