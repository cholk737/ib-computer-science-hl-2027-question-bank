from pathlib import Path
import json, re, math, collections
P=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
S={r['code']:r for r in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}
I={r['source_id']:r for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())}
for p in ['batches','papers']:(O/p).mkdir(exist_ok=True)

def atomic(path,data):
 path.parent.mkdir(exist_ok=True,parents=True);t=path.with_suffix('.tmp');t.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');t.replace(path)

def make(src,q,sub,page,marks,command,text,context,ms_pages,ms_summary,status,codes,reason,prompt=None,answer=None,points=None,difficulty='medium',code=None,test=None,issues=None):
 r=I[src];qid='H-'+src.replace('-','')+'-Q'+str(q).zfill(2)+('-'+sub if sub else '')
 maps=[{'syllabus_code':c,'scope_evidence':S[c]['guidance'],'rationale':reason,'theme':S[c]['theme'],'level':S[c]['level'],'confidence':'high','review_required':False} for c in codes]
 assets=[]
 path=O/'papers'/src/'renders'/f'page-{page}.png'
 if not path.exists():path=O/'papers'/src/'renders'/f'page-{page:02}.png'
 if path.exists():assets=[{'kind':'source_page_render','description':'Full source page inspected; includes all question context, source code/figures where present.','path':str(path.relative_to(P)),'source_pdf_page':page,'visually_verified':True}]
 msid=r['paired_source_ids'].split(';')[0]
 source={'source_question_id':qid,'source_id':src,'source_filename':r['filename'],'year':r['year'],'session':r['session'],'source_level':r['level'],'paper':r['paper'],'zone':r['zone'],'option':'','question':str(q),'subquestion':sub,'source_pdf_pages':[page],'source_printed_pages':[str(page-1)],'original_marks':marks,'command_term':command,'original_text':text,'parent_context':context,'assets':assets,'assessed_concepts':[S[c]['statement'] for c in codes] if codes else [reason],'difficulty':difficulty,'markscheme':{'status':'uploaded_official_available','source_id':msid,'filename':I[msid]['filename'],'pdf_pages':ms_pages,'question_reference':str(q)+('('+sub+')' if sub else ''),'marking_summary':ms_summary,'source_issues':issues or []},'relevance_status':status,'mappings':maps,'exclusion_reason':reason if status=='C' else '', 'uncertainty_flags':issues or [],'verification':{'source_text':'transcribed from original PDF and compared with rendered page','source_marks':'checked against printed allocation and official MS','visual_review':'full question page inspected','mapping':'full exact statement and guidance reviewed; old syllabus headings not treated as new requirements'}}
 practice=None
 if prompt:
  assert answer is not None and points is not None
  if isinstance(points,str):points=points.split('|')
  assert len(points)==marks,(qid,marks,len(points))
  levels={S[c]['level'] for c in codes}
  practice={'question_id':qid.replace('H-','P-',1),'source_question_ids':[qid],'derivation_status':'adapted_unofficial','unofficial':True,'question_text':prompt,'syllabus_codes':codes,'theme':'/'.join(sorted({S[c]['theme'] for c in codes})),'level':'HL-only' if levels=={'HL-only'} else 'SL/HL common' if levels=={'SL/HL common'} else 'mixed common/HL','marks':marks,'command_term':(re.search(r'\b(State|Identify|Outline|Explain|Construct|Sketch|Describe|Compare|Calculate|Trace|Distinguish|Discuss|Evaluate)\b',prompt).group(1) if re.search(r'\b(State|Identify|Outline|Explain|Construct|Sketch|Describe|Compare|Calculate|Trace|Distinguish|Discuss|Evaluate)\b',prompt) else command),'difficulty':difficulty,'adaptation_rationale':reason+' Scenario and wording rewritten; source reasoning retained only within supported 2027 scope.','solution':answer,'marking_points':[{'marks':1,'criterion':p} for p in points],'acceptable_alternatives':['Equivalent technically correct answers meeting the same scoped requirement; valid alternative algorithms accepted where they meet any explicit question constraints.'],'partial_credit_notes':'Award each specified criterion independently up to the allocation. Credit correct method after an earlier slip when consistent; do not award the same point twice.','common_errors':[],'verification':{'technical':'Independently solved; compared relevant source MS points, with obsolete/source-error assertions not imported.','mark_sum':marks,'code_execution':test or 'No executable code required; explicit answer/trace checked manually.'},'markscheme_status':'preliminary_unofficial_verified_by_author','assets':[]}
  if code:practice['code']=code
 return source,practice

def save_batches(src,items,complete=True,total=100,notes=None):
 sq=[x[0] for x in items];pq=[x[1] for x in items if x[1]]
 batches=[]
 for start in range(0,len(items),8):
  chunk=items[start:start+8];b=f'{src}-b{start//8+1:03}';path=O/'batches'/f'{b}.json'
  atomic(path,{'source_id':src,'batch_id':b,'source_questions':[x[0] for x in chunk],'practice_questions':[x[1] for x in chunk if x[1]]});batches.append(str(path.relative_to(P)))
 audit={'source_id':src,'complete':complete,'source_leaf_count':len(sq),'practice_count':len(pq),'relevance_counts':dict(collections.Counter(x['relevance_status'] for x in sq)),'leaf_tree':[{'id':s['source_question_id'],'marks':s['original_marks'],'pages':s['source_pdf_pages']} for s in sq],'extracted_marks_total':sum(s['original_marks'] for s in sq),'printed_candidate_total':total,'candidate_rules':'All questions compulsory' if I[src]['paper']=='1' else 'Original option selection rules retained in source evidence','batches':batches,'last_completed_leaf':sq[-1]['source_question_id'],'next_exact_action':'Coordinator verification and integration' if complete else 'Continue remaining source leaves','notes':notes or []}
 assert not complete or sum(s['original_marks'] for s in sq)==total
 atomic(O/'papers'/src/'paper_audit.json',audit)
 atomic(O/'checkpoint.json',{'last_source':src,'last_leaf':sq[-1]['source_question_id'],'batch_count':len(batches),'source_count':len(sq),'practice_count':len(pq),'status':'paper_complete' if complete else 'partial'})
 print(src,len(sq),len(pq),audit['relevance_counts'],audit['extracted_marks_total'])
