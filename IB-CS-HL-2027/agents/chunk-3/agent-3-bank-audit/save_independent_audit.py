#!/usr/bin/env python3
"""Independent census and bounded source/answer samples; not full-bank certification."""
import collections,json,os,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def norm(t):return re.sub(r'\s+',' ',t).strip()
scope=json.loads((ROOT/'syllabus/SYLLABUS_MASTER.json').read_text());bank={q['question_id']:q for f in (ROOT/'question-bank/records').glob('*.json') for q in [json.loads(f.read_text())]}
census=[]
for r in scope:
    ids=sorted(qid for qid,q in bank.items() if r['code'] in q['syllabus_codes']);census.append({'code':r['code'],'statement':r['statement'],'level':r['level'],'topic':r['topic'],'linked_question_ids':ids,'linked_count':len(ids),'census_result':'zero linked candidates: definite bank-link gap' if not ids else 'candidates exist: coverage requires per-question/bullet review','coverage_certified':False})
samples=[
('A4.3.1','P-SRC044-Q05-b','Prompt and criteria establish predictor/continuous response, fitted relation and prediction. Slope/intercept are named without individually assessing their interpretation; r² is unassessed.','Partial scope; new fit/parameter-interpretation practice remains needed.'),
('A4.3.3','P-SRC040-Q05-f','Actual prompt/criteria assess simulator-specific overfitting, unseen real-world data and independent evaluation. No explicit hyperparameter decision, precision, recall or F1 calculation.','Valid overfitting aspect; do not certify full hyperparameter/evaluation guidance.'),
('A4.3.10','P-SRC033-Q06-b','The two requested unreliability reasons concern data quality and deployment shift. No candidate algorithm/model is compared or selected.','Narrow performance/data-characteristics relevance; main model-selection skill remains unestablished.'),
('B2.4.5','P-SRC001-Q14-b','Single recursive call per nonbase activation; calls at indices4,3,2,1 return40. Boundary k<2 returns1.','Within simple non-branching scope; target sample executes correctly.'),
('B3.1.5','P-SRC002-Q14-c','DateValue class groups validated state/rules; criteria award coherent grouping and reuse/integrity. No access-control convention or public/non-public interface implementation requested.','Partial encapsulation/information-hiding coverage.'),
('B3.2.2','P-SRC033-Q14-d-ii','Overriding pay uses super().pay(hours)+self.HOURLY_FEE*hours; parent fee plus hourly charge matches prompt.','Dynamic overriding aspect is sound; static forms not assessed by this sample.'),
('B3.2.4','P-SRC002-Q15-d','Prompt states independently reusable Customer objects, so reference/member changes and independent lifetime support aggregation.','Sound aggregation aspect; composition/owned lifetime not assessed here.'),
('B4.1.3','P-SRC001-Q07','Deleting Omar then tail Theo and prepending Nia produces Nia↔Lena↔Priya, exterior links None. Four criteria match. Some stored names have split-word typography.','Correct doubly-linked operation sample; no claim of all singly/doubly/circular operations.')]
reviews=[]
for code,qid,observation,outcome in samples:
    r=next(r for r in scope if r['code']==code);q=bank[qid];source=[]
    for page in r['source_pdf_pages']:
        f=ROOT/f'sources/2027-guide/text/page-{page:03}.txt';text=f.read_text();source.append({'path':str(f.relative_to(ROOT)),'code_present_in_page_text':r.get('source_code',code) in text,'source_page_reexamined':True})
    reviews.append({'code':code,'question_id':qid,'statement':r['statement'],'full_guidance':r['guidance'],'guide_source_check':source,'prompt_read':True,'solution_and_all_mark_points_read':True,'observation':observation,'outcome':outcome,'does_not_certify_whole_code':True,'status':'bounded independent audit sample; formal per-question approval belongs to coordinator evidence pipeline'})
# Independent execution of the exact recursion prompt, no stored test code used.
q=bank['P-SRC001-Q14-b'];code=q['question_text'][q['question_text'].index('def suffix_product'):];namespace={};exec(compile(code,'selected_recursion_prompt','exec'),namespace);assert namespace['suffix_product'](4,[8,3,2,5,4])==40;assert namespace['suffix_product'](1,[8,3,2,5,4])==1
result={'checkpoint':'C3-A3-INDEPENDENT-CENSUS','date':'2026-11-04','specialist':'/root/searchable_bank_audit','scope_statement_count':len(scope),'levels':dict(collections.Counter(r['level'] for r in scope)),'baseline_practice_count':len(bank),'zero_link_codes':[r['code'] for r in census if not r['linked_count']],'objective_link_census':census,'selected_content_reviews':reviews,'executable_checks':[{'question_id':'P-SRC001-Q14-b','check':'Exact prompt recursion at k4 yields40; base k1 yields1','status':'pass'}],'limitations':['112-code census is mechanical candidate accounting, not a112-code substantive coverage audit.','8 source-guidance/prompt/solution samples independently inspected; remaining per-question review belongs to A/B queues and coordinator approval.','No original question or examination authored. No broad whole-statement coverage claim.']}
if (HERE/'independent_review_samples.json').exists():result['independent_review_samples']=json.loads((HERE/'independent_review_samples.json').read_text())
t=HERE/'independent_coverage.json.tmp';t.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');os.replace(t,HERE/'independent_coverage.json');print(json.dumps({k:result[k] for k in ['scope_statement_count','baseline_practice_count','zero_link_codes']}))
