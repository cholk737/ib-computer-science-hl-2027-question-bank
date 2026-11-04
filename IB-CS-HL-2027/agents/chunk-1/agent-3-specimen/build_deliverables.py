from pathlib import Path
from collections import Counter, defaultdict
import csv, json, sys, io, contextlib,re
from pypdf import PdfReader

OUT=Path(__file__).resolve().parent
SOURCE='sources/2027-specimen/Specimen Papers 2027 - English.pdf'
rows=[]
def add(paper,q,part,marks,command,page,ms,kind,skill,depth,difficulty='medium',restriction=''):
    ao={'State':1,'List':1,'Identify':2,'Outline':2,'Describe':2,'Explain':3,'Construct':3,'Sketch':3,'Justify':3,'Discuss':3,'To what extent':3}.get(command)
    rows.append(dict(id=f'SPEC-HL-P{paper}-Q{q}-{part}',paper=f'HL Paper {paper}',section=('A' if q<5 else 'B') if paper==1 else 'Option B - Python',question=str(q),subquestion=part,marks=marks,command_term=command,command_objective=ao if ao else '2 (analyst: trace equivalent)',source_file=SOURCE,source_pdf_page=page,source_printed_page=page-(2 if paper==1 else 36),markscheme_pdf_pages=ms,markscheme_printed_pages=';'.join(str(int(v)-(18 if paper==1 else 62)) for v in ms.split(';')),response_type=kind,skill_summary=skill,marking_expectation=depth,difficulty_analyst_estimate=difficulty,explicit_constraint=restriction,status='official_uploaded_specimen_reference_not_generated_question'))

add(1,1,'a',2,'Outline',4,'23','short explanation','Accumulator purpose','Function plus brief expansion','low')
add(1,1,'b',1,'State',4,'23','number representation','Hexadecimal to binary','Correct eight-bit binary result','low')
add(1,1,'c',2,'Construct',4,'23','truth table','Half-subtractor logic circuit','One mark for each correct output column')
add(1,1,'d',2,'Outline',5,'23','short explanation','Operating-system accounting','Resource accounting role and expansion','low')
add(1,1,'e',2,'Outline',5,'23','contextual explanation','PaaS suitability for application development','Two relevant credited points','low')
add(1,1,'f',4,'Explain',5,'24','technical explanation','Execution overhead of compiled versus interpreted code','Four credited causal points')
add(1,2,'a',1,'State',6,'25','recall','LAN-to-internet device','One correct device','low')
add(1,2,'b',2,'Describe',6,'25','technical account','TCP/IP network-interface-layer function','Point and expansion')
add(1,2,'c',3,'List',6,'25','comparative recall','Fibre versus twisted-pair benefits','Three distinct benefits','low')
add(1,2,'d',4,'Explain',7,'26','process explanation','Switch MAC learning and forwarding','Four linked process points')
add(1,2,'e',4,'Explain',7,'26','process explanation','One NAT function in firewall context','Four connected points from same function')
add(1,3,'a',3,'Construct',8,'27','SQL','Unique-name substring query','DISTINCT/GROUP BY; LIKE; wildcard and search term')
add(1,3,'b',5,'Construct',9,'27','schema design','3NF relational decomposition','Entity tables and keys; foreign keys; visit key','high')
add(1,3,'c',3,'Describe',9,'28','technical account','Distributed-transaction atomicity','All-or-nothing unit, cross-node completion/rollback')
add(1,3,'d',3,'Outline',11,'28','contextual account','Spatial database for outbreak addresses','Three relevant application points')
add(1,4,'a',1,'State',12,'29','recall','CNN layer','One valid layer','low')
add(1,4,'b',1,'Identify',12,'29','recall','Data-cleaning reason','One valid reason','low')
add(1,4,'c',2,'Outline',12,'29','contextual explanation','GPU for large-data CNN training','Reason and linked expansion')
add(1,4,'d',3,'Describe',12,'30','model evaluation','CNN evaluation using F1 score','Three correct evaluation/calculation points')
add(1,4,'e',3,'Justify',13,'30','contextual justification','Reinforcement versus supervised learning for robot cleaner','Issue, contextual expansion, supporting reason')
add(1,4,'f',5,'Discuss',13,'31','ethical extended response','Hospital request to retract public comments','Balanced contextual analysis with supported conclusion','high')
add(1,5,'a-i',2,'Identify',14,'32','case-study recall','Other malware types','Two valid types excluding those already given','low')
add(1,5,'a-ii',2,'Outline',14,'32','case-study application','Non-financial phishing consequence for hospital','Consequence and expansion','low','Do not repeat the hospital financial loss already stated; source permits distinct patient financial fraud')
add(1,5,'b',4,'Outline',15,'33','case-study application','BYOD security strategies','Two strategies each with expansion')
add(1,5,'c',4,'Outline',15,'33','case-study application','BYOD advantages over employer-provided devices','Two advantages each with expansion')
add(1,5,'d',12,'To what extent',16,'34;35','evaluative extended response','Prevention and response to cybersecurity attacks','Holistic levels 1–3,4–6,7–9,10–12; balanced analysis, conclusion and independent research','high')

add(2,7,'a',1,'State',50,'76','recall','Reason for flowchart representation','One valid reason','low')
add(2,7,'b',3,'Copy and complete',50,'76','flowchart trace','Nested-loop trace for N=3','Correct i, j and output columns')
add(2,7,'c',1,'State',51,'76','complexity','Big O for nested-loop flowchart','Quadratic time')
add(2,7,'d',5,'Describe',51,'77','algorithm without code','Extract every third file line into surname file','Open both files, loop, counter/equivalent, write relevant lines, close files; cap5','medium','Both files initially closed; describe steps')
add(2,7,'e',2,'Sketch',53,'78','stack trace diagram','Stack after push/peek/pop sequence','Correct contents plus top identified','low','Clearly identify top')
add(2,7,'f',3,'Describe',53,'78','algorithm without code','Locate earliest-pushed stack element','Loop with isEmpty; pop/store; print last popped','medium','Use only push, pop, peek, isEmpty from supplied table')
add(2,8,'a',3,'Explain',54,'79','data-structure reasoning','Lists instead of separate variables','Three appropriate advantages')
add(2,8,'b',4,'Describe',54,'79','string algorithm without code','Swap surname and first name','Loop; locate separator/split; extract parts; recombine','medium','Exactly one space between first name and surname')
add(2,8,'c',1,'State',54,'79','indexing','2D list item access','Correct zero-based indices','low')
add(2,8,'d',2,'State',55,'79','code trace','Nested-loop list computation','Correct a and b outputs')
add(2,8,'e',5,'Construct',55,'79','Python function','Find theatre row with fewest sold seats','Initialisation, nested loops, count False, track row, reset count, output; cap5','high','40 rows by30 columns; unique matching row')
add(2,9,'a-i',3,'List',56,'80','OOP execution account','Passenger constructor and object instantiation','Constructor, new object/reference and initialised attributes')
add(2,9,'a-ii',2,'Outline',56,'80','OOP concepts','Consequences of private attributes','Two conceptual consequences; see source privacy caveat')
add(2,9,'b',2,'Outline',57,'80','OOP relationship','Passenger and Flight relationship','Official MS calls composition and price dependence; ambiguity flagged')
add(2,9,'c',4,'Construct',58,'80','Python method','Ticket price by percentage sold','Percentage, correct ranges, conditional control, returned price')
add(2,9,'d',4,'Construct',58,'81','Python method','Add passenger with current price','Call price method; instantiate Passenger; append; increment count')
add(2,9,'e',5,'Describe',58,'81','algorithm without code','Selection sort on passenger name','Name comparison, sorted/unsorted partition, minimum, swap, repetition','high','Without writing code; selection sort required')
add(2,10,'a',3,'Describe',59,'82','dictionary application','Airport-code to airport-name lookup','String key/value pairs, mapping, lookup result')
add(2,10,'b',2,'Outline',59,'82','set application','Deduplicate promotional-email addresses','Combine into set; uniqueness','low')
add(2,10,'c-i',1,'State',59,'82','Python output','Set membership','Correct Boolean','low')
add(2,10,'c-ii',1,'State',59,'82','Python output','Set intersection','Correct set; order immaterial','low')
add(2,11,'a',2,'Sketch',60,'83','tree diagram','BST insertions','One mark per correct added node')
add(2,11,'b',3,'Explain',60,'83','recursive reasoning','Recursive BST insertion','Root comparison, subtree selection, recursive call, base case; cap3')
add(2,11,'c-i',1,'State',60,'83','code trace','Iterative summation','Correct returned value','low')
add(2,11,'c-ii',4,'Construct',60,'83','Python recursion','Recursive equivalent of iterative summation','Progressing recursive call, base case, return, complete correctness','high')
add(2,11,'c-iii',3,'Explain',60,'83','runtime reasoning','Large-input recursive run-time failure','Call-frame/stack storage, many calls, resource limit')
add(2,12,'a',5,'Construct',61,'84','Python linked-list traversal','Search by name and print score or failure','Traversal, comparison, found handling and correct outputs; alternative points cap5','high')
add(2,12,'b',5,'Describe',61,'84','algorithm without code','Insert into linked list in descending score order','Traverse, previous/current references and correct head/middle/end relinking; cap5','high','Without writing code; assume nonempty list')

assert len(rows)==54
assert sum(r['marks'] for r in rows if r['paper']=='HL Paper 1' and r['section']=='A')==56
assert sum(r['marks'] for r in rows if r['paper']=='HL Paper 1' and r['section']=='B')==24
assert sum(r['marks'] for r in rows if r['paper']=='HL Paper 2')==80
with (OUT/'specimen_question_index.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'specimen_question_index.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False))

manifest=[
 ('COMP-01','Compilation title and contents','all','1-2','n/a','administrative'),
 ('COMP-02','HL Paper 1 question paper','HL','3-18','1-16','selected'),
 ('COMP-03','HL Paper 1 markscheme','HL','19-35','1-17','selected'),
 ('COMP-04','Blank separator','n/a','36','n/a','blank'),
 ('COMP-05','HL Paper 2 question paper','HL','37-61','1-25','selected cover and Python'),
 ('COMP-05A','HL Paper 2 Java option A Q1-6','HL','38-49','2-13','language alternative excluded from target'),
 ('COMP-05B','HL Paper 2 Python option B Q7-12','HL','50-61','14-25','selected'),
 ('COMP-06','Blank separator','n/a','62','n/a','blank'),
 ('COMP-07','HL Paper 2 markscheme','HL','63-84','1-22','selected general and Python'),
 ('COMP-07A','HL Paper 2 Java option A markscheme','HL','67-75','5-13','language alternative excluded from target'),
 ('COMP-07B','HL Paper 2 Python option B markscheme','HL','76-84','14-22','selected'),
 ('COMP-08','SL Paper 1 question paper','SL','85-96','1-12; cover advertises11','outside HL analysis'),
 ('COMP-09','SL Paper 1 markscheme','SL','97-109','1-13','outside HL analysis'),
 ('COMP-10','Blank separator','n/a','110','n/a','blank'),
 ('COMP-11','SL Paper 2 question paper','SL','111-131','1-21','outside HL analysis; repeated questions checked'),
 ('COMP-12','Blank separator','n/a','132','n/a','blank'),
 ('COMP-13','SL Paper 2 markscheme','SL','133-149','1-17','outside HL analysis'),
 ('COMP-14','Blank separator','n/a','150','n/a','blank'),
 ('COMP-15','Preventing network security attacks case study','SL and HL','151-154','1-4','selected specimen-only context')]
with (OUT/'component_manifest.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['component_id','component','level','compilation_pdf_pages','component_printed_pages','selection']);w.writerows(manifest)
totals={}
for paper in ['HL Paper 1','HL Paper 2']:
 qs=defaultdict(int)
 for r in rows:
  if r['paper']==paper:qs[r['question']]+=r['marks']
 totals[paper]=dict(qs)
blueprint={
 'status':'Unofficial analysis of uploaded official 2027 specimens; no practice exam authored',
 'source':SOURCE,'guide':'sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf',
 'guide_assessment_pdf_pages':[53,55,56],'guide_printed_pages':[47,49,50],
 'paper1':{'duration_minutes':120,'marks':80,'weight_percent':40,'all_compulsory':True,'theme':'A common and HL-only','sections':{'A':{'marks':56,'specimen_questions':[1,2,3,4]},'B':{'marks':24,'specimen_questions':[5],'pre_seen_case':True,'research_challenges_for_HL':4}},'specimen_question_marks':totals['HL Paper 1']},
 'paper2':{'duration_minutes':120,'marks':80,'weight_percent':40,'all_compulsory_within_selected_language':True,'theme':'B common and HL-only','selected_language':'Python','compilation_label':'Option B','specimen_questions':[7,8,9,10,11,12],'specimen_question_marks':totals['HL Paper 2'],'language_alternative_Java_questions':[1,2,3,4,5,6],'no_code_algorithmic_thinking_required_by_guide':True,'SL_repeated_specimen_questions':{'HL7':'SL4','HL8':'SL5'},'builtins_policy':'Specific prohibitions only when clearly stated; no blanket ban.'},
 'mark_bearing_leaf_parts':{'paper1':26,'paper2_python':28,'combined':54},
 'difficulty_note':'low/medium/high estimates in index are analyst judgments, not official IB difficulty labels.',
 'future_practice_case_policy':'Use a clearly labelled unofficial case unless user explicitly selects an official one; this specimen case is not an assumed future-session case.'}
(OUT/'exam_blueprint.json').write_text(json.dumps(blueprint,indent=2))
(OUT/'mark_totals_verification.json').write_text(json.dumps({'assertions_passed':True,'questions':totals,'leaf_parts':54,'marks':160,'command_term_counts':dict(Counter(r['command_term'] for r in rows))},indent=2))
print(json.dumps({'rows':len(rows),'totals':totals},indent=2))
reader=PdfReader(OUT.parents[2]/SOURCE)
page_checks=[]
for page in sorted(set(r['source_pdf_page'] for r in rows)):
    # Restrict to end-of-line brackets: seats[2][3] is code, not a mark allocation.
    source_marks=[int(x) for x in re.findall(r'\[(\d+)\][ \t]*$',reader.pages[page-1].extract_text(),re.M)]
    index_marks=[r['marks'] for r in rows if r['source_pdf_page']==page]
    assert source_marks==index_marks,(page,source_marks,index_marks)
    page_checks.append(dict(pdf_page=page,source_marks=source_marks,index_marks=index_marks,passed=True))
(OUT/'source_mark_sequence_checks.json').write_text(json.dumps(page_checks,indent=2))
