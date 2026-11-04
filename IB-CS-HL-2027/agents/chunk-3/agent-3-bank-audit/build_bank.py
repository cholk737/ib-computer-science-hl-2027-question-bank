#!/usr/bin/env python3
"""Build read-only local UI datasets from authoritative project records."""
import argparse, csv, hashlib, json, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
def atomic(path, text):
    tmp=path.with_name(path.name+'.tmp'); tmp.write_text(text,encoding='utf-8'); os.replace(tmp,path)
def build(root=ROOT, dest=HERE/'web'):
    dest.mkdir(parents=True,exist_ok=True)
    inventory={r['source_id']:r for r in json.loads((root/'sources/SOURCE_INVENTORY.json').read_text())}
    scope={r['code']:r for r in json.loads((root/'syllabus/SYLLABUS_MASTER.json').read_text())}
    sources={r['source_question_id']:(f,r) for f in (root/'extraction/by-paper').glob('*/questions/*.json') for r in [json.loads(f.read_text())]}
    rows=list(csv.DictReader((root/'question-bank/QUESTION_BANK.csv').open()))
    questions=[]; answers={}; hashes={}
    for row in rows:
        qpath=root/row['question_path']; apath=root/row['markscheme_path']; rpath=root/row['record_path']
        q=json.loads(qpath.read_text()); answer=json.loads(apath.read_text()); record=json.loads(rpath.read_text()); qid=q['question_id']
        assert qid==answer['question_id']==record['question_id']==row['question_id']
        assert all(c in scope for c in q['syllabus_codes'])
        public={k:q.get(k) for k in ['question_id','question_text','theme','syllabus_codes','level','marks','command_term','difficulty','derivation_status','assets']}
        public['unofficial']=True; public['verification_status']=row.get('verification_status','not supplied')
        public['topics']=sorted({scope[c]['topic'] for c in q['syllabus_codes']})
        public['objectives']=[{'code':c,'statement':scope[c]['statement'],'level':scope[c]['level'],'guidance':scope[c]['guidance']} for c in q['syllabus_codes']]
        public['provenance']=[]
        for sid in q.get('source_question_ids',record.get('source_question_ids',[])):
            if sid not in sources: raise ValueError(f'Missing source {sid}')
            f,s=sources[sid]; provenance={k:s.get(k) for k in ['source_question_id','source_id','source_filename','year','session','paper','zone','option','question','subquestion','source_pdf_pages','markscheme']}
            provenance['markscheme']={k:s.get('markscheme',{}).get(k) for k in ['status','source_id','filename','pdf_pages','question_reference']}
            source_path=root/inventory[s['source_id']]['project_path']; provenance['source_href']=os.path.relpath(source_path,dest).replace(os.sep,'/')+'#page='+str((s.get('source_pdf_pages') or [1])[0])
            ms=s.get('markscheme',{}); mid=ms.get('source_id')
            if mid in inventory: provenance['markscheme_href']=os.path.relpath(root/inventory[mid]['project_path'],dest).replace(os.sep,'/')+'#page='+str((ms.get('pdf_pages') or [1])[0])
            public['provenance'].append(provenance)
        questions.append(public);answers[qid]=answer
        for f in [qpath,apath,rpath]:hashes[str(f.relative_to(root))]=hashlib.sha256(f.read_bytes()).hexdigest()
    assert len({q['question_id'] for q in questions})==len(questions)
    data={'schema_version':1,'unofficial':True,'questions':questions,'scope':[{'code':r['code'],'statement':r['statement'],'theme':r['theme'],'topic':r['topic'],'level':r['level']} for r in scope.values()]}
    atomic(dest/'questions.js','window.BANK_DATA = '+json.dumps(data,ensure_ascii=False)+';\n')
    atomic(dest/'answers.js','window.BANK_ANSWERS = '+json.dumps(answers,ensure_ascii=False)+';\n')
    manifest={'question_count':len(questions),'scope_count':len(scope),'question_ids':[q['question_id'] for q in questions],'source_hashes':hashes,'question_payload_contains_answers':False,'answer_payload':'answers.js, loaded only on first reveal; local files are not a security boundary'}
    atomic(dest/'build_manifest.json',json.dumps(manifest,indent=2)+'\n')
    return data,answers,manifest
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--dest',type=Path,default=HERE/'web');a=p.parse_args();d,_,m=build(a.root,a.dest);print(json.dumps({'questions':m['question_count'],'scope':m['scope_count'],'dest':str(a.dest)}))
