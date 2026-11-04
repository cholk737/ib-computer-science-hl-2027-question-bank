from build_records import *
from pypdf import PdfReader
expected={'SRC-004':(39,100),'SRC-007':(37,100),'SRC-016':(28,70),'SRC-022':(38,100),'SRC-028':(24,70),'SRC-033':(75,260),'SRC-040':(64,180)}
all_sources=[];all_practice=[];receipts=[]
for src,(leaves,marks) in expected.items():
 files=sorted((O/'batches').glob(src+'-*.json'));sources=[];practices=[]
 for f in files:
  b=json.loads(f.read_text());sources+=b['source_questions'];practices+=b['practice_questions']
 assert len(sources)==leaves and sum(s['original_marks'] for s in sources)==marks
 max_page=len(PdfReader(P/I[src]['project_path']).pages)
 for r in sources:
  assert r['original_text_status'].startswith('verbatim_leaf')
  assert r['parent_context_status']=='complete_original_question_block_from_pdf_text_layer'
  assert r['original_text'] and r['parent_context']
  assert all(1<=p<=max_page for p in r['source_pdf_pages'])
  assert all((P/f).exists() for f in r['raw_source_page_transcriptions'])
  if src=='SRC-040':
   assert r['source_pdf_pages']==[r['mark_allocation_pdf_page']]
   assert all((P/f).exists() for f in r.get('raw_context_page_transcriptions',[]))
  assert all((P/a['path']).exists() and a['visually_verified'] for a in r['assets'])
  assert r['markscheme']['status']=='uploaded_official_available'
  assert all(m['syllabus_code'] in S and m['scope_evidence']==S[m['syllabus_code']]['guidance'] for m in r['mappings'])
  if r['relevance_status']=='C':assert r['exclusion_reason'] and not r['mappings']
  else:assert r['mappings'] and (any(r['source_question_id'] in p['source_question_ids'] for p in practices) or r.get('adaptation_reuse_question_id'))
 for p in practices:
  assert sum(x['marks'] for x in p['marking_points'])==p['marks']
  assert p['unofficial'] and p['source_question_ids'] and p['solution']
  assert all(c in S for c in p['syllabus_codes'])
  term=re.search(r'\b(State|Identify|Outline|Explain|Construct|Sketch|Describe|Compare|Calculate|Trace|Distinguish|Discuss|Evaluate)\b',p['question_text'])
  assert not term or p['command_term']==term[1],p['question_id']
  if p.get('code'):compile(p['code'],'<practice>','exec')
 audit=json.loads((O/'papers'/src/'paper_audit.json').read_text())
 audit.update(complete=True,source_leaf_count=leaves,practice_count=len(practices),extracted_marks_total=marks,batches=[str(f.relative_to(P)) for f in files],leaf_tree=[{'id':r['source_question_id'],'marks':r['original_marks'],'pages':r['source_pdf_pages'],'option':r['option']} for r in sources],verification_status='Specialist source,scope,visual and technical checks complete; coordinator review/integration pending',missing_unreadable_content=[],source_transcription_status='All leaves verbatim PDF text-layer extracts with complete raw question context and page evidence; renders remain visual authority',next_exact_action='Coordinator independent verification and integration; no remaining source paper in shard C')
 if src in ['SRC-033','SRC-040']:
  assert audit['option_marks']==dict.fromkeys('ABCD',65 if src=='SRC-033' else 45)
 atomic(O/'papers'/src/'paper_audit.json',audit)
 receipts.append({'source_id':src,'leaves':leaves,'all_option_marks':marks,'practices':len(practices),'reuse_links':sum(bool(r.get('adaptation_reuse_question_id')) for r in sources),'relevance_counts':dict(collections.Counter(r['relevance_status'] for r in sources))})
 all_sources+=sources;all_practice+=practices
assert len({s['source_question_id'] for s in all_sources})==305
assert len({p['question_id'] for p in all_practice})==220
tech=json.loads((O/'technical_checks.json').read_text())
receipt={'checkpoint':'CHUNK2-C-FINAL-2026-11-04','status':'specialist_complete_coordinator_verification_pending','papers':receipts,'source_leaf_count':len(all_sources),'all_source_marks':sum(s['original_marks'] for s in all_sources),'practice_count':len(all_practice),'reuse_links':sum(bool(s.get('adaptation_reuse_question_id')) for s in all_sources),'relevance_counts':dict(collections.Counter(s['relevance_status'] for s in all_sources)),'python_code_tests':sum(bool(p.get('code')) for p in all_practice),'technical_test_receipts':len(tech),'source_transcription_fallbacks':0,'cross_audit_status':'Complete; see cross_audit.md/json and verify_cross_audit.py','next_exact_action':'Coordinator revalidates SRC040 exact leaf-page/context separation, then integrates all seven completed papers.'}
atomic(O/'final_receipt.json',receipt);atomic(O/'checkpoint.json',receipt)
print(json.dumps(receipt,indent=2))
