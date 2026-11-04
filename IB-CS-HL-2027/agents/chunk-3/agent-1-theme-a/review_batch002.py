from review_batches import *
import itertools
rows=[{'inputs':[a,b,c],'value':4*a+2*b+c,'one_count':a+b+c,'output':int(a+b+c==2 or 4*a+2*b+c>=6)} for a,b,c in itertools.product([0,1],repeat=3)]
assert [r['output'] for r in rows]==[0,0,0,1,0,1,1,1]
atomic(O/'checks/P-SRC001-Q06-truth-check.json',{'question_id':'P-SRC001-Q06','method':'Independent exhaustive evaluation of both stated conditions for all 8 input combinations.','rows':rows,'expected_output':[0,0,0,1,0,1,1,1],'passed':True})
R2=[]
R2.append(review('P-SRC001-Q06',[
 m('A1.2.4',2,'Construct every output of a three-input truth table from an alarm problem description.','direct','Prompt requires complete table from exactly-two-one inputs OR numeric value>=6. Exhaustively recomputed all eight rows; this directly assesses the problem-description truth-table guidance, not Karnaugh maps or circuit simplification.'),
], 'Evaluated all 8 triples independently. Exactly-two criterion selects 011,101,110; value>=6 selects110,111; union gives outputs0,0,0,1,0,1,1,1.', 'Stored exhaustive check checks/P-SRC001-Q06-truth-check.json passes against all answer rows.', 'Four 1-mark row-pair criteria total4, cover all8 outputs, give positive partial credit by independent pairs. Prompt row order explicit.'))
R2.append(review('P-SRC001-Q08-a',[
 m('A2.1.4',1,'Define the general concept of an agreed communication protocol.','supporting','No named TCP/UDP/HTTP/HTTPS/DHCP role or behaviour is tested. This foundation supports the statement but does not establish direct coverage of any listed protocol.'),
], 'A network protocol is an agreed communication-rule set; wording does not confuse protocol with physical medium.', 'One concise definition contains rules plus communication context, appropriate Define1.', 'Single1-mark criterion and equivalent wording allowance match demand.'))
R2.append(review('P-SRC001-Q08-b',[
 m('A2.1.4',1,'List general communication properties standardized by protocols.','supporting','Message format, timing/order and addressing/error conventions are general protocol aspects. No specific function of the five listed transport/application protocols is tested.'),
], 'Data formats/encoding, interaction timing/order, addressing and error/acknowledgement behaviour are legitimate protocol-standardized properties.', 'The model lists three valid aspects. Alternative legitimate triples also exist; no single protocol must implement every listed function.', 'Three1-mark categories total3, but third merges addressing/routing with error/acknowledgement. A valid answer message format,addressing,error handling could receive only2 under literal buckets. Clarify award any3 distinct valid aspects, without double-crediting synonyms.', ['A-C3-MS-002: List3 valid protocol aspects must permit e.g. format + addressing + error handling as3 distinct answers; current fixed bucket grouping could cap at2.']))
atomic(O/'scope_reviews/batch-002.json',{'checkpoint':'A-RECORDS-002','reviews':R2})
allr={r['question_id']:r for f in (O/'scope_reviews').glob('*.json') for r in json.loads(f.read_text())['reviews']}
q=json.loads((O/'REVIEW_QUEUE.json').read_text())
for r in q['records']:
 if r['question_id'] in allr:
  d=allr[r['question_id']];r['status']='reviewed_with_issue' if d['issues'] else 'reviewed_specialist';r['review_path']=next(str(f.relative_to(P)) for f in (O/'scope_reviews').glob('*.json') if any(v['question_id']==r['question_id'] for v in json.loads(f.read_text())['reviews']))
q.update(checkpoint='A-RECORDS-002',reviewed_count=len(allr),pending_count=len(q['records'])-len(allr));atomic(O/'REVIEW_QUEUE.json',q)
t=json.loads((O/'STATUS.json').read_text());t.update(checkpoint='A-RECORDS-002',last_saved_question_id='P-SRC001-Q08-b',last_saved_reviewed_question_id='P-SRC001-Q08-b',record_review_counts={'total_owned':459,'reviewed':len(allr),'pending':459-len(allr)},reviewed_question_ids=sorted(allr),next_action='Review P-SRC001-Q09, P-SRC001-Q11-c-i and P-SRC001-Q11-c-ii; save batch-003 after full scoped checks.');t['files_created']+=['scope_reviews/batch-002.json','review_batch002.py','checks/P-SRC001-Q06-truth-check.json'];t['unfinished_tasks'][1]='Resolve marking alternative issues A-C3-MS-001 and A-C3-MS-002 via coordinator.';atomic(O/'STATUS.json',t)
with (O/'findings.md').open('a') as f:f.write('\nA-RECORDS-002: 6/459 reviewed,453 pending; last P-SRC001-Q08-b. Q06 truth table exhaustively executed and saved. Q08-a/Q08-b only supporting protocol-concept evidence, not direct named-protocol coverage. Marking issue A-C3-MS-002: fixed grouped categories could under-credit valid3 distinct protocol aspects. No original questions or master edits.\n')
print('Saved A-RECORDS-002:',len(allr),'reviewed; pending',459-len(allr))
