#!/usr/bin/env python3
"""Isolated functional tests. Synthetic review fixtures never touch live bank."""
import csv,json,shutil,tempfile,time
from pathlib import Path
import bank_db as b
HERE=Path(__file__).resolve().parent
checks=[]
def check(name,fn):
    start=time.perf_counter()
    try:fn()
    except Exception as e:
        (HERE/'db_test_results.json').write_text(json.dumps({'suite':'persistent-bank-functional','passed':len(checks),'failed':1,'failed_check':name,'error':repr(e),'checks':checks},indent=2)+'\n');raise
    checks.append({'name':name,'status':'pass','seconds':round(time.perf_counter()-start,3)})
with tempfile.TemporaryDirectory() as td:
    root=Path(td)/'project';root.mkdir();(root/'syllabus').mkdir();shutil.copy(b.ROOT/'syllabus/SYLLABUS_MASTER.json',root/'syllabus/SYLLABUS_MASTER.json');shutil.copytree(b.ROOT/'question-bank',root/'question-bank');(root/'question-bank/scope_evidence.json').unlink(missing_ok=True);(root/'extraction').symlink_to(b.ROOT/'extraction',target_is_directory=True)
    db=b.connect(Path(td)/'test.sqlite3');stats=b.import_project(db,root);baseline=stats['questions_in_master']
    def preservation():
        assert stats['inserted']==baseline and baseline>=823
        for row in csv.DictReader((root/'question-bank/QUESTION_BANK.csv').open()):
            q=b.detail(db,row['question_id']);record=json.loads((root/row['record_path']).read_text());assert q['question_text']==record['question_text'];assert not any(k in q for k in ['solution','marking_points','answer','test_code']);assert db.execute('SELECT answer_json FROM answers WHERE question_id=?',(q['question_id'],)).fetchone()
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    check('All 823 full prompts/IDs preserved, separate answers, DB integrity',preservation)
    def pending():
        assert db.execute("SELECT count(*) FROM verification WHERE status='pending'").fetchone()[0]==baseline*6
        assert b.search(db,{'verified':'verified'})['total']==0
        r=b.search(db,{'code':'B2.3.3'});assert r['total']>0 and r['checked_count']==0 and r['unverified_candidate_count']==r['total']
    check('Import never promotes code links or legacy metadata into verified matches',pending)
    code='B2.3.3';qid=db.execute('SELECT question_id FROM question_codes WHERE code=? ORDER BY question_id',(code,)).fetchone()[0];hash_=db.execute('SELECT record_sha256 FROM questions WHERE question_id=?',(qid,)).fetchone()[0];bullet=dict(db.execute('SELECT * FROM bullets WHERE bullet_id=?',(code+':G01',)).fetchone())
    def fixture(relevance='direct'):
        return {'question_id':qid,'record_sha256':hash_,'reviewer':'SYNTHETIC TEST FIXTURE — isolated DB','reviewed_at':'2026-11-04','mappings':[{'code':code,'scope_bullet_id':bullet['bullet_id'],'exact_guidance':bullet['text'],'assessed_skill':'construct a counted loop (for loop)','relevance':relevance,'evidence':'Synthetic unit-test evidence; no live verification.'}],'verification':{d:{'status':'verified','evidence':'Synthetic isolated verification test.'} for d in b.DIMENSIONS}}
    def stale():
        bad=fixture();bad['record_sha256']='0'*64;result=b.import_reviews(db,[bad]);assert result['imported']==0 and result['rejected'];assert db.execute('SELECT count(*) FROM scope_evidence').fetchone()[0]==0
    check('Stale or missing record hash rejected without scope promotion',stale)
    def bad_bullet():
        bad=fixture();bad['mappings'][0]['exact_guidance']='Invented nonofficial bullet';result=b.import_reviews(db,[bad]);assert result['imported']==0 and result['rejected'];assert db.execute('SELECT count(*) FROM scope_evidence').fetchone()[0]==0;assert b.detail(db,qid)['verification']['mapping']['status']=='pending'
    check('Invented or wrong exact guidance rejected',bad_bullet)
    with db:result=b.import_reviews(db,[fixture()]);assert result['imported']==1
    def direct():
        r=b.search(db,{'code':code,'scope_text':'counted loops; post-condition loops'});q=next(q for q in r['questions'] if q['question_id']==qid);assert q['relevance']=='partial';assert any(m['relevance']=='direct' for m in q['matched_requirements']);assert any('post condition loop' in b.norm(x['requirement']) for x in r['requirements_with_no_established_match']);assert any('post condition loop' in b.norm(x['requirement']) for x in r['requirements_without_full_match']);assert q['all_dimensions_verified']
        full=b.search(db,{'scope_text':bullet['text'],'code':code});q=next(q for q in full['questions'] if q['question_id']==qid);assert q['relevance']=='partial' and q['unmet_requirements']
    check('Reviewed aspect direct; full bullet and unmatched post-condition remain incomplete',direct)
    def partial():
        with db:b.import_reviews(db,[fixture('partial')])
        r=b.search(db,{'code':code,'scope_text':'counted loop'});q=next(q for q in r['questions'] if q['question_id']==qid);assert q['relevance']=='partial';assert q['unmet_requirements']
        with db:b.import_reviews(db,[fixture()])
    check('Partial evidence never becomes direct',partial)
    def supporting():
        with db:b.import_reviews(db,[fixture('supporting')])
        r=b.search(db,{'code':code,'scope_text':'counted loop','include_candidates':'false'});assert r['total']==0
        with db:b.import_reviews(db,[fixture()])
    check('Supporting evidence excluded from reviewed-direct/partial search',supporting)
    def filters():
        r=b.search(db,{'text':'Databases','theme':'A','target_paper':'Paper 1'});assert r['total'] and all('A' in q['themes'] for q in r['questions'])
        r=b.search(db,{'verified':'verified'});assert r['total']==1 and r['questions'][0]['question_id']==qid
        mixed=next((b.detail(db,r[0]) for r in db.execute('SELECT question_id FROM questions') if len(b.detail(db,r[0])['themes'])>1),None);assert mixed
        for t in mixed['themes']:assert any(q['question_id']==mixed['question_id'] for q in b.search(db,{'text':mixed['question_id'],'theme':t})['questions'])
        ref=next(q for q in b.search(db,{'limit':200})['questions'] if q['provenance']);p=ref['provenance'][0];r=b.search(db,{'year':p['year'],'session':p['session'],'question_type':ref['question_type'],'minMarks':ref['marks'],'maxMarks':ref['marks']});assert r['total'] and all(q['marks']==ref['marks'] for q in r['questions'])
    check('Broad topic and all requested filters; mixed-theme inclusion normalized',filters)
    def pagination():
        results=[]
        for offset in range(0,baseline,73):results.extend(q['question_id'] for q in b.search(db,{'offset':offset,'limit':73})['questions'])
        assert len(results)==baseline and len(set(results))==baseline
    check('Pagination retrieves every genuine baseline record exactly once',pagination)
    def id_and_unknown():
        r=b.search(db,{'text':qid.lower()});assert r['total']==1 and r['questions'][0]['question_id']==qid and not r['requested_requirements']
        assert b.search(db,{'text':'zzzzUnknownQueryForever'})['total']==0
    check('Exact stable-ID retrieval narrows to one; unknown keyword does not return all',id_and_unknown)
    def literal_and_atomic():
        bad=fixture();bad['mappings'][0]['exact_guidance']=bullet['text'].replace('Types','types');bad['verification']['mapping']['status']='issue';before=b.detail(db,qid)['verification']['mapping'];result=b.import_reviews(db,[bad]);assert result['rejected'];assert b.detail(db,qid)['verification']['mapping']==before
        bad=fixture();bad['mappings'].append(dict(bad['mappings'][0],scope_bullet_id='INVENTED'));result=b.import_reviews(db,[bad]);assert result['imported']==0 and result['rejected'];assert len(b.detail(db,qid)['scope_evidence'])==1
    check('Literal changed guidance and one bad mapping reject whole review with zero promotion',literal_and_atomic)
    def revised_and_idempotent():
        before=db.execute('SELECT count(*) FROM verification_history').fetchone()[0]
        with db:r=b.import_reviews(db,[fixture()])
        assert r['unchanged_reviews']==1 and db.execute('SELECT count(*) FROM verification_history').fetchone()[0]==before
        changed=fixture();changed['mappings'][0]['assessed_skill']='construct conditional while loop';
        with db:b.import_reviews(db,[changed])
        e=b.detail(db,qid)['scope_evidence'];assert len(e)==1 and 'conditional' in e[0]['assessed_skill'];assert b.search(db,{'code':code,'scope_text':'counted loop','include_candidates':'false'})['total']==0
        with db:b.import_reviews(db,[fixture()])
    check('Unchanged review import idempotent; revised review replaces stale broad matches',revised_and_idempotent)
    def snapshot_revocation():
        with db:b.sync_review_snapshot(db,{'reviews':[fixture()]},'synthetic-master')
        with db:b.update_verification(db,qid,'technical','issue','Manual override survives snapshot withdrawal','independent reviewer',hash_)
        with db:r=b.sync_review_snapshot(db,{'reviews':[]},'synthetic-master')
        assert r['revoked_reviews']==1;assert not b.detail(db,qid)['scope_evidence'];q=b.detail(db,qid);assert q['verification']['mapping']['status']=='pending';assert q['verification']['technical']['status']=='issue' and q['verification']['technical']['reviewer']=='independent reviewer'
        with db:b.sync_review_snapshot(db,{'reviews':[fixture()]},'synthetic-master')
    check('Authoritative snapshot withdrawal revokes links/source checks and preserves independent manual check',snapshot_revocation)
    def public_payload():
        q=b.public_question(b.detail(db,qid));assert all('evidence' not in v for v in q['verification'].values());assert all('raw_json' not in e and 'evidence' not in e for e in q['scope_evidence']);assert 'outstanding_issues' not in q;assert 'answer' not in q
        q=b.public_search(b.search(db,{'code':code,'scope_text':'counted loop'}))['questions'][0];assert all('evidence' not in e and 'raw_json' not in e for m in q['matched_requirements'] for e in m['evidence'])
    check('Public question/search omit answer-bearing reviewer rationale until explicit reveal',public_payload)
    def exact_scope_and_statement():
        req,_=b.requirements(db,scope_text=bullet['text']);assert len(req)==1 and req[0]['kind']=='bullet'
        f=fixture('supporting');f['mappings'][0].update(statement_relevance='direct',statement_evidence='Synthetic explicit construct-program assessment, distinct from guidance comparison.')
        with db:b.import_reviews(db,[f])
        statement=db.execute('SELECT statement FROM objectives WHERE code=?',(code,)).fetchone()[0];r=b.search(db,{'text':statement});q=next(q for q in r['questions'] if q['question_id']==qid);assert q['relevance']=='direct';assert q['matched_requirements'][0]['requirement']['kind']=='statement';assert b.search(db,{'code':code,'include_candidates':'false'})['total']==0
        with db:b.import_reviews(db,[fixture()])
    check('Exact guidance keeps qualifiers; explicit statement assessment distinct from supporting bullet',exact_scope_and_statement)
    def reviewed_type():
        f=fixture();f['metadata_updates']={'question_type':'algorithm construction — reviewed'}
        with db:b.sync_review_snapshot(db,{'reviews':[f]},'synthetic-type-source')
        assert b.detail(db,qid)['question_type']=='algorithm construction — reviewed' and 'specialist-reviewed' in b.detail(db,qid)['question_type_basis'];assert b.search(db,{'question_type':'algorithm construction — reviewed'})['total']==1
        with db:b.sync_review_snapshot(db,{'reviews':[]},'synthetic-type-source')
        assert b.detail(db,qid)['question_type']!='algorithm construction — reviewed'
        with db:b.import_reviews(db,[fixture()])
    check('Reviewed explicit question type filters persist and revoke with withdrawn approval',reviewed_type)
    def reviewed_code_union():
        f=fixture();other=dict(db.execute("SELECT * FROM bullets WHERE code='A1.3.7' ORDER BY ordinal LIMIT 1").fetchone());m=dict(f['mappings'][0],code=other['code'],scope_bullet_id=other['bullet_id'],exact_guidance=other['text'],assessed_skill='Synthetic checked new code aspect');f['mappings'].append(m)
        with db:b.import_reviews(db,[f])
        q=b.detail(db,qid);assert 'A1.3.7' in q['reviewed_syllabus_codes'] and 'A1.3.7' not in q['legacy_syllabus_codes'];assert 'A' in q['themes'];r=b.search(db,{'code':'A1.3.7','theme':'A','topic':'Computer fundamentals'});assert any(q['question_id']==qid for q in r['questions'])
        with db:b.import_reviews(db,[fixture()])
        assert 'A1.3.7' not in b.detail(db,qid)['syllabus_codes']
    check('Approved new code/theme/topic joins detail/filters without rewriting legacy code metadata',reviewed_code_union)
    def mapping_dimension_controls_relevance():
        with db:b.update_verification(db,qid,'mapping','issue','Synthetic later mapping objection','independent mapper',hash_)
        assert b.search(db,{'code':code,'scope_text':'counted loop','include_candidates':'false'})['total']==0
        q=b.detail(db,qid);assert not q['reviewed_syllabus_codes'];assert all(e['effective_mapping_status']!='verified' for e in q['scope_evidence'])
        revised=fixture();revised['reviewed_at']='2026-11-05'
        with db:b.import_reviews(db,[revised])
        assert b.search(db,{'code':code,'scope_text':'counted loop','include_candidates':'false'})['total']==1
    check('Independent mapping objection immediately removes checked relevance without rewriting question',mapping_dimension_controls_relevance)
    selection=b.save_selection(db,[qid],{'code':code},{'purpose':'isolated test'})
    with db:db.execute('INSERT INTO usage_history VALUES(?,?,?,?,?,?)',('test-usage',qid,b.now(),'isolated test',selection['selection_id'],'Synthetic test only'))
    def selection_safe():
        out=json.dumps(selection);assert 'marking_points' not in out and 'solution' not in out;assert selection['record_hashes'][qid]==hash_;assert db.execute('SELECT query_json FROM selections WHERE selection_id=?',(selection['selection_id'],)).fetchone()
    check('Persistent reproducible retrieval selection has IDs/query/hashes, student export omits answers',selection_safe)
    def incremental():
        r=b.import_project(db,root);assert r['unchanged']==baseline and r['inserted']==r['updated']==0;assert db.execute('SELECT count(*) FROM usage_history').fetchone()[0]==1;assert db.execute('SELECT count(*) FROM selections').fetchone()[0]==1;assert b.detail(db,qid)['verification']['mapping']['status']=='verified'
    check('No-change import preserves per-dimension verification, usage and selection history',incremental)
    def dimension():
        with db:b.update_verification(db,qid,'technical','issue','Isolated test issue','test reviewer',hash_)
        q=b.detail(db,qid);assert q['verification']['technical']['status']=='issue';assert q['verification']['mapping']['status']=='verified';assert q['question_text']==json.loads(db.execute('SELECT record_json FROM questions WHERE question_id=?',(qid,)).fetchone()[0])['question_text'];assert db.execute('SELECT count(*) FROM verification_history WHERE question_id=?',(qid,)).fetchone()[0]>6
    check('Individual verification dimension update is independent and audit-trailed',dimension)
    def additions():
        rows=list(csv.DictReader((root/'question-bank/QUESTION_BANK.csv').open()));base=rows[0];record=json.loads((root/base['record_path']).read_text());q=json.loads((root/base['question_path']).read_text());a=json.loads((root/base['markscheme_path']).read_text());newid='O-ISOLATED-TEST-001';q.update(question_id=newid,source_question_ids=[],derivation_status='original_unofficial');a['question_id']=newid;record.update(q);record['source_question_ids']=[]
        row=dict(base);row.update(question_id=newid,record_path=f'question-bank/records/{newid}.json',question_path=f'question-bank/questions/{newid}.json',markscheme_path=f'question-bank/markschemes/{newid}.json');record.update(record_path=row['record_path'],question_path=row['question_path'],markscheme_path=row['markscheme_path'])
        for f,d in [(row['record_path'],record),(row['question_path'],q),(row['markscheme_path'],a)]: (root/f).write_text(json.dumps(d))
        with (root/'question-bank/QUESTION_BANK.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(base));w.writeheader();w.writerows(rows+[row])
        r=b.import_project(db,root);assert r['inserted']==1 and r['unchanged']==baseline;assert b.detail(db,newid)['provenance']==[];assert b.detail(db,qid)['usage_history'];assert db.execute('SELECT count(*) FROM questions').fetchone()[0]==baseline+1
    check('Incremental original addition preserves all IDs/history and unknown provenance stays empty',additions)
    def changed():
        row=next(r for r in csv.DictReader((root/'question-bank/QUESTION_BANK.csv').open()) if r['question_id']==qid);record=json.loads((root/row['record_path']).read_text());q=json.loads((root/row['question_path']).read_text());q['question_text']+='\nSYNTHETIC CONTENT CHANGE';record['question_text']=q['question_text'];(root/row['question_path']).write_text(json.dumps(q));(root/row['record_path']).write_text(json.dumps(record));r=b.import_project(db,root);assert r['updated']==1;assert b.detail(db,qid)['verification']['mapping']['status']=='stale';assert b.detail(db,qid)['scope_evidence'][0]['mapping_status']=='stale';assert b.detail(db,qid)['usage_history']
    check('Changed content invalidates old reviews but preserves usage and selection snapshots',changed)
    db.close()
result={'suite':'persistent-bank-functional','passed':len(checks),'failed':0,'checks':checks,'isolation':'Temporary project copy/database; synthetic review fixtures were never imported into live bank.','limitations':['Real browser layout/interaction audit delegated to coordinator.','Search uses verified evidence and transparent lexical/concept alias candidate discovery, not an opaque semantic model.','Question type inferred from command when no explicit type exists; labelled as requiring review.']};(HERE/'db_test_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
