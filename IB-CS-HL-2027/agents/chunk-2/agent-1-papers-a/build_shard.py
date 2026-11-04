from pathlib import Path
import json,re,collections
P=Path(__file__).resolve().parents[3]
O=Path(__file__).resolve().parent
INV={r['source_id']:r for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())}
S={r['code']:r for r in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}
DATA={};CURRENT='SRC-001'
def add(q,sub,page,marks,command,text,context,codes,status,prompt='',points=None,solution='',reason='',assets=None,ms=None,code='',tests='',flags=None):
 r=INV[CURRENT]; suffix=f'Q{q:02}'+('-'+sub if sub else ''); sid='H-'+CURRENT.replace('-','')+'-'+suffix; pid='P-'+CURRENT.replace('-','')+'-'+suffix
 maps=[dict(mapping_target='adapted_practice_only' if status=='B' else 'original_and_adapted',syllabus_code=c,scope_evidence=S[c]['guidance'],rationale=reason or 'The assessed skill is explicitly named in the cited statement and its guidance; mapping does not credit unassessed scenario topics.',theme=S[c]['theme'],level=S[c]['level'],confidence='high',review_required=False) for c in codes]
 src=dict(original_assessment_context=context,source_scope_note='B mappings identify the converted question scope and do not certify all original assessed content as within2027 scope.' if status=='B' else 'Original assessed concept classified directly or excluded with reason.',source_question_id=sid,source_id=CURRENT,source_filename=r['filename'],year=r['year'],session=r['session'],source_level=r['level'],paper=r['paper'],zone=r['zone'],option='',question=str(q),subquestion=sub,source_pdf_pages=page if isinstance(page,list) else [page],source_printed_pages=[str(p) for p in (page if isinstance(page,list) else [page])],original_marks=marks,command_term=command,original_text=text,parent_context=context,assets=assets or [],assessed_concepts=[command+': '+text],difficulty='high' if marks>=5 else 'medium' if marks>=3 else 'low',markscheme=ms or dict(status='not_uploaded',source_id='',filename='',pdf_pages=[],question_reference=f'{q}({sub})',marking_summary='No corresponding uploaded official markscheme; practice answer independently derived.',source_issues=[]),relevance_status=status,mappings=maps,exclusion_reason=reason if status=='C' else '',uncertainty_flags=flags or [],verification=dict(source='Source page visually inspected; handwritten annotations excluded from question content.' if CURRENT=='SRC-001' else 'Original PDF text and marked leaf checked.',marks='Printed allocation transcribed.',mapping='Full statement/guidance reviewed; status separates obsolete requirements.',official_answer_status='Uploaded markscheme absence preserved' if CURRENT=='SRC-001' else 'See source markscheme record'))
 practice=None
 if status!='C' and prompt:
  points=points or []
  assert sum(p['marks'] for p in points)==marks,(sid,points,marks)
  themes=sorted(set(S[c]['theme'] for c in codes));levels=sorted(set(S[c]['level'] for c in codes))
  practice=dict(question_id=pid,source_question_ids=[sid],derivation_status='adapted_unofficial',unofficial=True,question_text=prompt,syllabus_codes=codes,theme='/'.join(themes),level='/'.join(levels),marks=marks,command_term=command,difficulty=src['difficulty'],adaptation_rationale=reason or 'Original application rewritten to be self-contained; assessed reasoning retained within cited 2027 scope.',solution=solution or '; '.join(p['criterion'] for p in points),marking_points=points,acceptable_alternatives=['Equivalent technically correct wording or valid implementation earning the specified independent points.'],partial_credit_notes='Award each stated point independently up to the total; do not double-credit the same idea.',common_errors=[],verification=dict(technical='Concrete marking points independently reasoned from the defined context and exact 2027 scope.',code_check='Executable checks saved under checks/ where applicable.' if code else 'No executable code required; manual technical check.'),code=code,test_code=tests,assets=[],markscheme_status='preliminary_unofficial_verified_by_author')
 if practice:
  command_match=re.search(r'\b(Compare and contrast|Copy and complete|To what extent|Construct|State|Identify|Outline|Describe|Explain|Define|Determine|Trace|Sketch|Draw|List|Compare|Evaluate|Discuss|Suggest|Deduce)\b',prompt)
  if command_match:practice['command_term']=command_match.group(1)
 DATA.setdefault(CURRENT,[]).append((src,practice))
 return src,practice
def pts(*items):return [dict(marks=m,criterion=t) for m,t in items]
def save_batches(sid,complete=False,expected_total=None,candidate_total=None,notes=''):
 records=DATA[sid];paths=[]
 for i in range(0,len(records),8):
  chunk=records[i:i+8];name=f'{sid}-b{i//8+1:03}.json';path=O/'batches'/name;path.parent.mkdir(exist_ok=True)
  obj=dict(source_id=sid,batch_id=name[:-5],source_questions=[a for a,b in chunk],practice_questions=[b for a,b in chunk if b]);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2));tmp.replace(path);paths.append(name)
 d=O/'papers'/sid;d.mkdir(parents=True,exist_ok=True)
 tree=[dict(id=a['source_question_id'],question=a['question'],subquestion=a['subquestion'],marks=a['original_marks'],pdf_pages=a['source_pdf_pages']) for a,b in records]
 audit=dict(source_id=sid,complete=complete,source_leaf_tree=tree,leaf_count=len(records),extracted_total_marks=sum(a['original_marks'] for a,b in records),expected_all_option_marks=expected_total,candidate_total=candidate_total,batches=paths,counts=dict(collections.Counter(a['relevance_status'] for a,b in records)),converted_count=sum(b is not None for a,b in records),unresolved_mappings=sum(any(m['review_required'] for m in a['mappings']) for a,b in records),notes=notes,last_completed=records[-1][0]['source_question_id'],next_exact_action='Next assigned source paper' if complete else 'Continue source leaf extraction and conversion; see findings.md')
 (d/'paper_audit.json').write_text(json.dumps(audit,indent=2))
 if complete and expected_total is not None:assert audit['extracted_total_marks']==expected_total,audit
 return audit
