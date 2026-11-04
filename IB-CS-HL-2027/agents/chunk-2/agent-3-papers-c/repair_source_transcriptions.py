"""Link complete exact source text; replace hand-entered synopses with faithful leaf extracts where locatable."""
from build_records import *
import pdfplumber
logs=[]
for src in ['SRC-004','SRC-007','SRC-016','SRC-022','SRC-028','SRC-033','SRC-040']:
 trans=O/'papers'/src/'transcription';trans.mkdir(exist_ok=True)
 with pdfplumber.open(P/I[src]['project_path']) as doc:
  texts={i:p.extract_text() for i,p in enumerate(doc.pages,1)}
 for i,t in texts.items():(trans/f'pdf-page-{i:03}.txt').write_text(t+'\n')
 joined='\n'.join(texts.values()); heads=list(re.finditer(r'(?m)^(\d+)\.\s+',joined));regions={}
 for i,m in enumerate(heads):regions.setdefault(int(m[1]),joined[m.start():heads[i+1].start() if i+1<len(heads) else len(joined)])
 for batch in sorted((O/'batches').glob(src+'-*.json')):
  b=json.loads(batch.read_text())
  for r in b['source_questions']:
   if 'original_text_synopsis' not in r:r['original_text_synopsis']=r['original_text'];r['context_synopsis']=r['parent_context']
   q=int(r['question']);sub=r['subquestion'];region=regions[q];target=region
   alpha,_,roman=sub.partition('-')
   try:
    if alpha:
     marker=re.search(r'(?m)^\('+alpha+r'\)\s*',region)
     if not marker:marker=re.search(r'^\d+\.\s*\('+alpha+r'\)\s*',region)
     assert marker
     target=region[marker.start():]
     nxt=re.search(r'(?m)^\('+chr(ord(alpha)+1)+r'\)\s*',target[marker.end()-marker.start():])
     if nxt:target=target[:marker.end()-marker.start()+nxt.start()]
     if roman:
      mm=re.search(r'\('+roman+r'\)\s*',target);assert mm
      target=target[mm.start():]
    end=re.search(r'\[\s*'+str(r['original_marks'])+r'\s*\]',target);assert end
    target=target[:end.end()]
    r['original_text']=target;r['original_text_status']='verbatim_leaf_from_pdf_text_layer; page_render_is_visual_authority'
   except (AssertionError,KeyError):
    r['original_text']='SYNOPSIS (not verbatim): '+r['original_text_synopsis'];r['original_text_status']='explicit_synopsis_with_complete_raw_page_transcription_linked'
   r['parent_context']=region;r['parent_context_status']='complete_original_question_block_from_pdf_text_layer'
   # Add any context dependency physical pages already established by visual review.
   if src=='SRC-007' and q==14:r['source_pdf_pages']=sorted(set(r['source_pdf_pages']+[7]));r['source_printed_pages']=[str(p-1) for p in r['source_pdf_pages']]
   required=[]
   if src=='SRC-033' and q==13:required=[15,16]
   if src=='SRC-040':
    if q==2:required=[5,6]
    if q==4:required=[9,10]
    if q==6:required=[13,14]
    if q==7:required=[15,16]
    if q==10:required=[19,20,21]
    if q in [11,12]:
     r['shared_class_context_transcriptions']=[str((trans/f'pdf-page-{p:03}.txt').relative_to(P)) for p in [19,20,21]]
   if required:
    r['source_pdf_pages']=sorted(set(r['source_pdf_pages']+required));r['source_printed_pages']=[str(p-1) for p in r['source_pdf_pages']]
    for p in required:
     if not any(x['source_pdf_page']==p for x in r['assets']):
      path=O/'papers'/src/'renders'/f'page-{p:02}.png'
      if not path.exists():path=O/'papers'/src/'renders'/f'page-{p}.png'
      r['assets'].append({'kind':'source_page_render','description':'Shared full source question context, table,code or figure inspected.','path':str(path.relative_to(P)),'source_pdf_page':p,'visually_verified':True})
   if src=='SRC-040':
    # Established directly from printed leaf/mark positions, not a last-context-page heuristic.
    leafpage={1:4,2:6 if sub=='e' else 5,3:8,4:9 if sub in ['a-i','a-ii','b'] else 10,5:12,6:13 if sub=='a' else 14,7:16 if sub.startswith('e-') else 15,8:17,9:18,10:21,11:22,12:23}[q]
    previous=r['source_pdf_pages'];r['context_pdf_pages']=sorted(set(previous+r.get('context_pdf_pages',[]))-{leafpage})
    if q in [11,12]:r['context_pdf_pages']=sorted(set(r['context_pdf_pages']+[19,20,21]))
    r['mark_allocation_pdf_page']=leafpage;r['source_pdf_pages']=[leafpage];r['source_printed_pages']=[str(leafpage-1)]
    r['context_printed_pages']=[str(p-1) for p in r['context_pdf_pages']]
    r['raw_context_page_transcriptions']=[str((trans/f'pdf-page-{p:03}.txt').relative_to(P)) for p in r['context_pdf_pages']]
   r['raw_source_page_transcriptions']=[str((trans/f'pdf-page-{p:03}.txt').relative_to(P)) for p in r['source_pdf_pages']]
   logs.append({'source_question_id':r['source_question_id'],'status':r['original_text_status']})
  atomic(batch,b)
atomic(O/'transcription_repair_audit.json',logs)
print('Source records corrected',len(logs),'fallback',sum(x['status'].startswith('explicit') for x in logs))
for x in logs:
 if x['status'].startswith('explicit'):print(x['source_question_id'])
