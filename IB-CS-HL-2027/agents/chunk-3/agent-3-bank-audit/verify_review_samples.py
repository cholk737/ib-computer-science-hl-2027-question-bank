#!/usr/bin/env python3
"""Independent rechecks of concrete A/B review findings, not corpus certification."""
import itertools,json,os,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def record(qid):return json.loads((ROOT/f'question-bank/records/{qid}.json').read_text())
q=record('P-SRC001-Q15-b');ns={};exec(compile(q['code'],'independent_discounted_row','exec'),ns);count=0
for n in range(5):
 for values in itertools.product('SDX',repeat=n):
  row=list(values);matrix=[row,['S']];before=[v[:] for v in matrix];assert ns['discounted_in_row'](matrix,0)==row.count('D');assert matrix==before;count+=1
q2=record('P-SRC002-Q17-a');ns2={};exec(compile(q2['code'],'independent_change_preference','exec'),ns2)
def node(c,n=None):return types.SimpleNamespace(customer=c,next=n)
def customer(v):return types.SimpleNamespace(preferred_shop=v)
f=ns2['change_preference'];assert f(None,'A','B')==0;one=customer('A');assert f(node(one),'A','B')==1 and one.preferred_shop=='B';alias=customer('A');head=node(alias,node(alias));alias_count=f(head,'A','B');assert alias_count==1;unchanged=customer('A');unchanged_count=f(node(unchanged),'A','A');assert unchanged_count==1 and unchanged.preferred_shop=='A'
qp=record('P-SRC001-Q08-a');assert qp['question_text']=='Define a network communication protocol.'
scope=json.loads((ROOT/'syllabus/SYLLABUS_MASTER.json').read_text());codes=['B2.2.2','B2.3.3','B4.1.3','A2.1.4'];source_pages={}
for code in codes:
 r=next(r for r in scope if r['code']==code);source_pages[code]=[{'pdf_page':p,'text_path':f'sources/2027-guide/text/page-{p:03}.txt','code_present':code in (ROOT/f'sources/2027-guide/text/page-{p:03}.txt').read_text()} for p in r['source_pdf_pages']]
result={'reviewer':'/root/searchable_bank_audit','date':'2026-11-04','scope_source_pages':source_pages,'samples':[
{'question_id':'P-SRC001-Q15-b','actual_prompt_answer_and_all_criteria_read':True,'independent_execution':{'status':'pass','cases':count,'domain':'2D list of S/D/X codes, selected row0, including empty row; no mutation'},'finding':'Agree with B: row access/traversal and conditional counting are directly assessed aspects. Finite for-each traversal is not evidence of pre/post-condition or explicitly indexed counted forms. Standalone prompt does not expressly define bookings as a2D list; keep context/criteria issue rather than full verification.','approval_limit':'Original source-PDF provenance not rechecked; no whole-loop guidance certification.'},
{'question_id':'P-SRC002-Q17-a','actual_prompt_answer_and_all_criteria_read':True,'independent_execution':{'empty':0,'distinct_one_match':1,'two_nodes_sharing_one_customer':alias_count,'old_equal_new':unchanged_count,'status':'observations reproduced'},'finding':'Agree with B: traversal/update skill is relevant; returned number changed is ambiguous for repeated object references and identical replacement. Keep technical/markscheme issue and answer pending until domain/count meaning clarified.','approval_limit':'Do not call this question fully verified. Original PDF provenance not rechecked.'},
{'question_id':'P-SRC001-Q08-a','actual_prompt_answer_and_all_criteria_read':True,'finding':'Agree with A: generic protocol definition is sound at1mark but only supporting relevance to named TCP/UDP/HTTP/HTTPS/DHCP roles. The question supplies no named protocol and asks no function/purpose comparison. Do not promote it to direct named-protocol coverage.','approval_limit':'Checked adapted prompt/criteria and exact guide scope; no fresh original scanned-PDF transcription audit.'}
],'limitations':['Independent bounded rechecks only. No master question content was changed. Formal integration remains coordinator-only.']}
t=HERE/'independent_review_samples.json.tmp';t.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');os.replace(t,HERE/'independent_review_samples.json');print(json.dumps({'samples':3,'discounted_row_cases':count,'alias_count':alias_count,'same_value_count':unchanged_count}))
