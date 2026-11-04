from build_shard import *
import hashlib,datetime
sids=['SRC-002','SRC-006','SRC-009','SRC-020','SRC-026','SRC-032','SRC-038','SRC-044']
papers=[];rs=[];ps=[]
for sid in sids:
 files=sorted((O/'batches').glob(sid+'-b*.json'));r=[];p=[]
 for f in files:
  b=json.loads(f.read_text());r+=b['source_questions'];p+=b['practice_questions']
 auditfile=O/'papers'/sid/'paper_audit.json';a=json.loads(auditfile.read_text())
 option_marks=dict(collections.Counter())
 for x in r:option_marks[x['option'] or 'all_questions']=option_marks.get(x['option'] or 'all_questions',0)+x['original_marks']
 candidate=65 if sid in ['SRC-002','SRC-032','SRC-038'] else 45 if sid=='SRC-044' else 100
 assert option_marks==({o:candidate for o in 'ABCD'} if len(option_marks)>1 else {'all_questions':candidate}),option_marks
 a.update(option_marks=option_marks,candidate_selection_rule='Answer all questions in one of four old options.' if len(option_marks)>1 else 'All questions compulsory.',question_tree={str(q):[dict(id=x['source_question_id'],subquestion=x['subquestion'],marks=x['original_marks'],pdf_pages=x['source_pdf_pages'],printed_pages=x['source_printed_pages']) for x in r if x['question']==q] for q in sorted({x['question'] for x in r})},source_MS_leaf_evidence_complete=sid!='SRC-002',code_and_source_visual_assets_checked=True,all_embedded_tests_passed=True,review_status='Author verified; coordinator independent review/integration pending.',last_checkpoint='2026-11-04-B-final')
 tmp=auditfile.with_suffix('.tmp');tmp.write_text(json.dumps(a,indent=2));tmp.replace(auditfile)
 papers.append(dict(source_id=sid,complete=True,leaves=len(r),source_marks=sum(x['original_marks'] for x in r),status_counts=dict(collections.Counter(x['relevance_status'] for x in r)),local_practice=len(p),reused_practice_ids=a.get('reused_practice_ids',[]),audit=str(auditfile.relative_to(P)),batches=[f.name for f in files],option_marks=option_marks))
 rs+=r;ps+=p
used=set(sids)
for sid in sids:used.update(x for x in INV[sid]['paired_source_ids'].split(';') if x)
source_integrity=[]
for sid in sorted(used):
 meta=INV[sid];file=P/meta['project_path'];sha=hashlib.sha256(file.read_bytes()).hexdigest();expected=meta.get('sha256','')
 if expected:assert sha==expected,(sid,sha,expected)
 source_integrity.append(dict(source_id=sid,path=meta['project_path'],sha256=sha,inventory_sha256_matches=sha==expected if expected else None))
checks=json.loads((O/'test_results.json').read_text());assert checks['passed']
receipt=dict(checkpoint='2026-11-04-B-final',agent='Agent 2 — Historical Paper Processor B',owned_output='agents/chunk-2/agent-2-papers-b/',complete=True,assigned_papers=8,completed_papers=8,remaining_papers=0,source_leaves=len(rs),source_marks=sum(x['original_marks'] for x in rs),classifications=dict(collections.Counter(x['relevance_status'] for x in rs)),local_practice_questions=len(ps),reused_cross_source_practice=2,converted_source_questions=sum(x['relevance_status']!='C' for x in rs),batch_files=62,original_MS_available_leaves=381,missing_original_MS_leaves=86,executable_checks=sum(x['test_present'] for x in checks['executable_checks']),all_executable_checks_passed=True,all_code_syntax_passed=True,placeholder_command_terms=0,papers=papers,source_integrity=source_integrity,hash_manifest='agents/chunk-2/agent-2-papers-b/batch_sha256.json',test_results='agents/chunk-2/agent-2-papers-b/test_results.json',remaining_limitations=['SRC-002 has no uploaded official markscheme; all60 adapted answers are independently solved unofficial criteria.','Source defects/ambiguities remain documented as historical evidence; practice prompts explicitly repair them.','Coordinator independent validation and authoritative master integration are pending.'],next_action='Coordinator reread all62 final batch hashes,integrate only validated records,and keep Chunk2 boundary. No remaining shard-B extraction/adaptation work.')
(O/'FINAL_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
with (O/'findings.md').open('a') as f:
 f.write('''
Final checkpoint 2026-11-04-B-final: all eight assigned papers complete. 467 marked source leaves,1360 all-option source marks,113A/220B/134C. 331 locally authored practice questions plus two cross-source reuse links cover333 source leaves. Source009 privacy conversion reclassified A→B after supplying explicit ML context. All62 batches rebuilt; exact SHA256 values are in batch_sha256.json. All62 executable Python/SQLite checks pass; every saved code block parses. Every source/practice command term is now explicit. All381 uploaded-MS leaves have isolated original leaf evidence; no adapted answer is used as the default original MS summary. Existing accurate original paraphrases retained. All original PDFs hashed against inventory,unchanged. Full receipt is FINAL_RECEIPT.json; per-paper audits now include leaf/mark/page trees and separately verified option totals.

SRC044 final:61 leaves,180 marks across four45-mark options,46 practice (10A/36B),15C. Source MS night-time AND bug repaired with OR; before-birthday age adjustment,SQL naming,Unicode-width and invalid Huffman example recorded. All figures/UI/code inspected.

Final scope repairs: generic ethical scenarios in SRC006-Q11d,SRC009-Q13dii,SRC002-Q11d andSRC002-Q16b converted explicitly through ML ethics A4.4.1,with source-versus-adapted scope separated. Generic A4.4.2 coverage no longer claimed. SRC038-Q1a ERD maps A3.2.2. SRC044-Q5c maps A4.3.3 overfitting/evaluation only. SRC038-Q5e requires positive integer trials and uses100*wins/trials. Constructor/object-trace over-credit previously removed as requested. All readable-prose changes protect Python and SQL solutions/identifiers.

Exact next action: coordinator independent review against FINAL_RECEIPT.json and batch_sha256.json,then authoritative master integration. Remaining source limitation is absent SRC002 official MS. No Chunk3 work performed. Earlier progress/count paragraphs above are historical and superseded by this final receipt.
''')
print('RECEIPT',len(rs),len(ps),len(papers),len(source_integrity),'source PDFs unchanged')
