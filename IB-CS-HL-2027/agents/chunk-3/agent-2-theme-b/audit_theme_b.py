from pathlib import Path
import json,os,hashlib,collections
P=Path(__file__).resolve().parents[3]
O=Path(__file__).resolve().parent

def atomic(path,data):
    tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');os.replace(tmp,path)

def checkpoint():
    scope=[s for s in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text()) if s['theme']=='B']
    decisions=json.loads((O/'audit_decisions.json').read_text())
    audit=[]
    for s in scope:
        d=decisions.get(s['code'])
        row={'code':s['code'],'statement':s['statement'],'level':s['level'],'source_pdf_pages':s['source_pdf_pages'],'guidance_paragraphs':s['guidance_paragraphs'],'linked_question_count':len(s['question_bank_ids']),'status':'pending_manual_review','evidence':[],'bullet_findings':[],'gaps':[],'difficulty_note':'Pending manual review; counts alone are insufficient.'}
        if d:
            row.update(d)
            row['manual_check_status']='prompt_solution_and_full_official_scope_read; limited evidence selection, not all bank records reverified'
            for evidence in row['evidence']:
                f=P/'question-bank/records'/f"{evidence['question_id']}.json"
                evidence['record_sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
            assert len(row['bullet_findings'])==len(s['guidance_paragraphs']), s['code']
        audit.append(row)
    atomic(O/'coverage_audit.json',audit)
    questions=sorted((O/'questions').glob('*.json')) if (O/'questions').exists() else []
    verified=[json.loads(f.read_text())['question_id'] for f in questions if json.loads(f.read_text()).get('verification_status')=='author_verified_preliminary']
    pending=[a['code'] for a in audit if a['status']=='pending_manual_review']
    atomic(O/'STATUS.json',{'agent':'/root/theme_b_coverage','checkpoint':f'B-AUDIT-{len(decisions):03d}','status':'active_audit' if pending else 'audit_saved_gap_generation','completed_tasks':['Read project rules, recovery progress, QA and specimen analysis',f'Manual objective/scope evidence audit saved for {len(decisions)} of {len(scope)} Theme B statements'],'unfinished_tasks':['Audit pending objectives: '+', '.join(pending)] if pending else ['Original gap-fill questions for recorded coverage gaps; independent coordinator review and master merge'],'objectives_checked':list(decisions),'generated_ids':[f.stem for f in questions],'verified_ids':verified,'last_saved_question_id':questions[-1].stem if questions else None,'files_created':['STATUS.json','findings.md','audit_theme_b.py','audit_decisions.json','coverage_audit.json']+[str(f.relative_to(O)) for f in questions],'remaining_requirements':{'pending_objectives':pending,'gap_objectives':[r['code'] for r in audit if r['gaps']]},'exact_next_action':('Audit '+pending[0]+' using exact guidance and actual prompt/solution evidence; checkpoint after topic.' if pending else 'Prioritize B1.1.1, B2.5.1, B3.2.5, B4.1.5 and B4.1.6 original questions in batches of 2–3; save reproducible checks.')})
    print('Saved',len(decisions),'/',len(scope),'objective audits;',len(questions),'questions;',len(verified),'author-verified')

if __name__=='__main__':checkpoint()
