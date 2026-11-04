#!/usr/bin/env python3
"""Persistent local bank. Import never executes stored question or answer code."""
import argparse,csv,datetime,hashlib,json,os,re,sqlite3,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'syllabus/SYLLABUS_MASTER.json').is_file()),HERE.parents[2])
DB=HERE/'question_bank.sqlite3'
DIMENSIONS=('mapping','technical','answer','markscheme','assets','provenance')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(data):return hashlib.sha256(data).hexdigest()
def norm(text):return re.sub(r'[^a-z0-9]+',' ',str(text).lower()).strip()
def dump(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def connect(path=DB):
    db=sqlite3.connect(path);db.row_factory=sqlite3.Row;db.execute('PRAGMA foreign_keys=ON');db.executescript('''
    CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS objectives(code TEXT PRIMARY KEY,theme TEXT,topic TEXT,statement TEXT,level TEXT,full_json TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS bullets(bullet_id TEXT PRIMARY KEY,code TEXT REFERENCES objectives(code),ordinal INTEGER,text TEXT NOT NULL,scope_kind TEXT);
    CREATE TABLE IF NOT EXISTS questions(question_id TEXT PRIMARY KEY,record_sha256 TEXT NOT NULL,question_json TEXT NOT NULL,record_json TEXT NOT NULL,marks INTEGER,difficulty TEXT,question_type TEXT,type_basis TEXT,generation_status TEXT,issues_json TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS answers(question_id TEXT PRIMARY KEY REFERENCES questions(question_id),answer_json TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS question_codes(question_id TEXT REFERENCES questions(question_id),code TEXT REFERENCES objectives(code),PRIMARY KEY(question_id,code));
    CREATE TABLE IF NOT EXISTS source_refs(question_id TEXT REFERENCES questions(question_id),source_question_id TEXT,year TEXT,session TEXT,historical_paper TEXT,source_json TEXT,PRIMARY KEY(question_id,source_question_id));
    CREATE TABLE IF NOT EXISTS verification(question_id TEXT REFERENCES questions(question_id),dimension TEXT,status TEXT,evidence TEXT,reviewer TEXT,reviewed_at TEXT,record_sha256 TEXT,PRIMARY KEY(question_id,dimension));
    CREATE TABLE IF NOT EXISTS verification_origins(question_id TEXT,dimension TEXT,origin TEXT,review_hash TEXT,PRIMARY KEY(question_id,dimension));
    CREATE TABLE IF NOT EXISTS review_source_memberships(source_key TEXT,question_id TEXT,reviewer TEXT,review_hash TEXT,PRIMARY KEY(source_key,question_id,reviewer));
    CREATE TABLE IF NOT EXISTS verification_history(event_id INTEGER PRIMARY KEY,question_id TEXT,dimension TEXT,status TEXT,evidence TEXT,reviewer TEXT,reviewed_at TEXT,record_sha256 TEXT);
    CREATE TABLE IF NOT EXISTS scope_evidence(evidence_id TEXT PRIMARY KEY,question_id TEXT REFERENCES questions(question_id),code TEXT REFERENCES objectives(code),bullet_id TEXT REFERENCES bullets(bullet_id),assessed_skill TEXT,relevance TEXT,evidence TEXT,covers_full_bullet INTEGER DEFAULT 0,reviewer TEXT,reviewed_at TEXT,record_sha256 TEXT,mapping_status TEXT,raw_json TEXT);
    CREATE TABLE IF NOT EXISTS review_metadata_origins(question_id TEXT,field TEXT,reviewer TEXT,review_hash TEXT,PRIMARY KEY(question_id,field));
    CREATE TABLE IF NOT EXISTS review_records(question_id TEXT REFERENCES questions(question_id),reviewer TEXT,review_hash TEXT,review_json TEXT,imported_at TEXT,PRIMARY KEY(question_id,reviewer));
    CREATE TABLE IF NOT EXISTS review_history(event_id INTEGER PRIMARY KEY,question_id TEXT,reviewer TEXT,review_hash TEXT,review_json TEXT,imported_at TEXT);
    CREATE TABLE IF NOT EXISTS usage_history(usage_id TEXT PRIMARY KEY,question_id TEXT REFERENCES questions(question_id),used_at TEXT,context TEXT,selection_id TEXT,notes TEXT);
    CREATE TABLE IF NOT EXISTS duplicate_groups(group_id TEXT,question_id TEXT REFERENCES questions(question_id),kind TEXT,evidence TEXT,review_status TEXT,PRIMARY KEY(group_id,question_id));
    CREATE TABLE IF NOT EXISTS selections(selection_id TEXT PRIMARY KEY,created_at TEXT,query_json TEXT,question_ids_json TEXT,record_hashes_json TEXT,metadata_json TEXT);
    CREATE TABLE IF NOT EXISTS import_runs(run_id TEXT PRIMARY KEY,imported_at TEXT,summary_json TEXT);
    CREATE VIRTUAL TABLE IF NOT EXISTS question_fts USING fts5(question_id UNINDEXED,body,tokenize='unicode61');
    CREATE INDEX IF NOT EXISTS scope_question_idx ON scope_evidence(question_id);
    CREATE INDEX IF NOT EXISTS scope_bullet_idx ON scope_evidence(bullet_id);
    CREATE INDEX IF NOT EXISTS source_year_idx ON source_refs(year,session);
    ''');db.execute("INSERT OR REPLACE INTO meta VALUES('schema_version','1')");db.commit();return db

def update_verification(db,qid,dimension,status,evidence,reviewer,record_hash,reviewed_at=None,origin='manual',review_hash=''):
    if dimension not in DIMENSIONS:raise ValueError('Unknown verification dimension')
    if not evidence or not reviewer:raise ValueError('Verification requires evidence and reviewer')
    actual=db.execute('SELECT record_sha256 FROM questions WHERE question_id=?',(qid,)).fetchone()
    if not actual or actual[0]!=record_hash:raise ValueError('Verification record hash is stale')
    if status not in ('verified','pending','issue','stale'):raise ValueError('Unknown verification status')
    previous=db.execute('SELECT status,evidence,reviewer,record_sha256 FROM verification WHERE question_id=? AND dimension=?',(qid,dimension)).fetchone()
    db.execute('INSERT OR REPLACE INTO verification_origins VALUES(?,?,?,?)',(qid,dimension,origin,review_hash))
    if previous and tuple(previous)==(status,str(evidence),reviewer,record_hash):return
    vals=(qid,dimension,status,str(evidence),reviewer,reviewed_at or now(),record_hash)
    db.execute('INSERT OR REPLACE INTO verification VALUES(?,?,?,?,?,?,?)',vals)
    db.execute('INSERT INTO verification_history(question_id,dimension,status,evidence,reviewer,reviewed_at,record_sha256) VALUES(?,?,?,?,?,?,?)',vals)

def inferred_type(record):
    return record.get('question_type') or {'Construct':'construction','Trace':'code tracing','Explain':'explanation','Describe':'description','Evaluate':'evaluation','Discuss':'discussion','Sketch':'diagram','Outline':'short response'}.get(record.get('command_term'),'short response')
def reset_reviewed_type(db,qid,reviewer,review_hash=None):
    origin=db.execute("SELECT * FROM review_metadata_origins WHERE question_id=? AND field='question_type'",(qid,)).fetchone()
    if origin and origin['reviewer']==reviewer and (review_hash is None or origin['review_hash']==review_hash):
        record=json.loads(db.execute('SELECT record_json FROM questions WHERE question_id=?',(qid,)).fetchone()[0]);db.execute('UPDATE questions SET question_type=?,type_basis=? WHERE question_id=?',(inferred_type(record),'explicit original metadata' if record.get('question_type') else 'command-based candidate; review required',qid));db.execute("DELETE FROM review_metadata_origins WHERE question_id=? AND field='question_type'",(qid,))

def import_project(db,root=ROOT):
    root=Path(root);scope=json.loads((root/'syllabus/SYLLABUS_MASTER.json').read_text());sources={r['source_question_id']:r for f in (root/'extraction/by-paper').glob('*/questions/*.json') for r in [json.loads(f.read_text())]};rows=list(csv.DictReader((root/'question-bank/QUESTION_BANK.csv').open()));stats={'inserted':0,'updated':0,'unchanged':0,'questions_in_master':len(rows),'scope_statements':len(scope),'reviews_imported':0,'reviews_rejected':[]};t=now()
    with db:
        for r in scope:
            db.execute('INSERT OR REPLACE INTO objectives VALUES(?,?,?,?,?,?)',(r['code'],r['theme'],r['topic'],r['statement'],r['level'],dump(r)))
            for i,text in enumerate(r.get('guidance_paragraphs',[]),1):
                kind='must include' if 'must include' in text.lower() else 'may include' if 'may include' in text.lower() else 'guidance'
                db.execute('INSERT OR REPLACE INTO bullets VALUES(?,?,?,?,?)',(f"{r['code']}:G{i:02}",r['code'],i,text,kind))
        for row in rows:
            rp=root/row['record_path'];raw=rp.read_bytes();r=json.loads(raw);qid=r['question_id'];q=json.loads((root/row['question_path']).read_text());a=json.loads((root/row['markscheme_path']).read_text());sha=digest(raw)
            if qid!=row['question_id'] or qid!=a['question_id']:raise ValueError('Mismatched question ID')
            for key in [k for k in q if k in r]:
                if q.get(key)!=r.get(key):raise ValueError(f'Question/master bundle mismatch: {qid} {key}')
            for key in [k for k in a if k in r]:
                if a.get(key)!=r.get(key):raise ValueError(f'Answer/master bundle mismatch: {qid} {key}')
            if any(not db.execute('SELECT 1 FROM objectives WHERE code=?',(c,)).fetchone() for c in q['syllabus_codes']):raise ValueError('Unknown syllabus code')
            prev=db.execute('SELECT record_sha256 FROM questions WHERE question_id=?',(qid,)).fetchone()
            if prev and prev[0]==sha:stats['unchanged']+=1;continue
            if not isinstance(q['marks'],int) or q['marks']<1:raise ValueError('Invalid marks')
            # Explicit metadata is authoritative; fallback command-based type is labelled inferred.
            typ=inferred_type(r)
            vals=(qid,sha,dump(q),dump(r),q['marks'],q.get('difficulty','unknown'),typ,'explicit' if r.get('question_type') else 'command-based candidate; review required',q.get('derivation_status',r.get('derivation_status','unknown')),dump(r.get('outstanding_issues',r.get('uncertainty_flags',[]))),t,t)
            db.execute('INSERT INTO questions VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(question_id) DO UPDATE SET record_sha256=excluded.record_sha256,question_json=excluded.question_json,record_json=excluded.record_json,marks=excluded.marks,difficulty=excluded.difficulty,question_type=excluded.question_type,type_basis=excluded.type_basis,generation_status=excluded.generation_status,issues_json=excluded.issues_json,updated_at=excluded.updated_at',vals)
            db.execute('INSERT OR REPLACE INTO answers VALUES(?,?)',(qid,dump(a)))
            db.execute('DELETE FROM question_codes WHERE question_id=?',(qid,));db.executemany('INSERT INTO question_codes VALUES(?,?)',[(qid,c) for c in q['syllabus_codes']])
            db.execute('DELETE FROM source_refs WHERE question_id=?',(qid,))
            for sid in r.get('source_question_ids',[]):
                s=sources.get(sid)
                if s is None:raise ValueError('Missing source '+sid)
                db.execute('INSERT INTO source_refs VALUES(?,?,?,?,?,?)',(qid,sid,str(s.get('year','')),s.get('session',''),str(s.get('paper','')),dump(s)))
            if prev:
                db.execute("UPDATE verification SET status='stale',evidence=evidence||' [Question record changed; recheck required.]' WHERE question_id=?",(qid,));db.execute("UPDATE scope_evidence SET mapping_status='stale' WHERE question_id=?",(qid,));stats['updated']+=1
            else:
                for dim in DIMENSIONS:update_verification(db,qid,dim,'pending','Imported legacy author/batch metadata retained in record_json; no per-dimension review inferred.','importer',sha,t)
                stats['inserted']+=1
            db.execute('DELETE FROM question_fts WHERE question_id=?',(qid,));db.execute('INSERT INTO question_fts VALUES(?,?)',(qid,' '.join([q.get('question_text',''),qid,q.get('command_term','')]+q['syllabus_codes'])))
        # Exact normalized text duplicate candidates, never treated as confirmed duplicates.
        groups={}
        for row in db.execute('SELECT question_id,question_json FROM questions'):
            text=norm(json.loads(row['question_json']).get('question_text',''));groups.setdefault(digest(text.encode())[:16],[]).append(row['question_id'])
        db.execute("DELETE FROM duplicate_groups WHERE kind='normalized_prompt_candidate'")
        for gid,ids in groups.items():
            if len(ids)>1:db.executemany('INSERT OR REPLACE INTO duplicate_groups VALUES(?,?,?,?,?)',[(gid,qid,'normalized_prompt_candidate','Normalized student prompt text equals; context review still required.','candidate') for qid in ids])
        evidence_path=root/'question-bank/scope_evidence.json'
        if evidence_path.exists():
            result=sync_review_snapshot(db,json.loads(evidence_path.read_text()),'master:question-bank/scope_evidence.json');stats['reviews_imported']=result['imported'];stats['reviews_rejected']=result['rejected'];stats['reviews_revoked']=result['revoked_reviews']
        if not evidence_path.exists():
            result=sync_review_snapshot(db,{'reviews':[]},'master:question-bank/scope_evidence.json');stats['reviews_revoked']=result['revoked_reviews']
        db.execute('INSERT INTO import_runs VALUES(?,?,?)',(str(uuid.uuid4()),now(),dump(stats)))
        db.execute("INSERT OR REPLACE INTO meta VALUES('project_root',?)",(str(root.resolve()),))
    return stats

def import_reviews(db,payload):
    reviews=payload if isinstance(payload,list) else payload.get('reviews',[]);out={'imported':0,'accepted_reviews':0,'unchanged_reviews':0,'rejected':[],'active_reviews':[]}
    for r in reviews:
        qid=r.get('question_id');current=db.execute('SELECT record_sha256 FROM questions WHERE question_id=?',(qid,)).fetchone()
        if not current or r.get('record_sha256')!=current[0]:out['rejected'].append({'question_id':qid,'reason':'missing or stale record hash'});continue
        reviewer=r.get('reviewer');date=r.get('reviewed_at') or now()
        if not reviewer:out['rejected'].append({'question_id':qid,'reason':'reviewer required'});continue
        invalid=[]
        for m in r.get('mappings',[]):
            bid=m.get('scope_bullet_id');bullet=db.execute('SELECT * FROM bullets WHERE bullet_id=?',(bid,)).fetchone()
            if not bullet or bullet['code']!=m.get('code') or bullet['text']!=m.get('exact_guidance'):invalid.append({'question_id':qid,'bullet_id':bid,'reason':'exact literal code/bullet mismatch'})
            elif m.get('relevance') not in ('direct','partial','supporting','reject') or not m.get('assessed_skill') or not m.get('evidence'):invalid.append({'question_id':qid,'bullet_id':bid,'reason':'missing concrete relevance/skill/evidence'})
        for dim,item in r.get('verification',{}).items():
            if dim not in DIMENSIONS:invalid.append({'question_id':qid,'reason':'unknown verification dimension '+dim})
            elif isinstance(item,dict) and item.get('status','pending') not in ('verified','pending','issue','stale'):invalid.append({'question_id':qid,'reason':'unknown verification status'})
        if invalid:out['rejected'].extend(invalid);continue
        review_json=dump(r);review_hash=digest(review_json.encode());previous=db.execute('SELECT review_hash FROM review_records WHERE question_id=? AND reviewer=?',(qid,reviewer)).fetchone()
        question_type=r.get('question_type') or r.get('metadata_updates',{}).get('question_type')
        if question_type:
            db.execute('UPDATE questions SET question_type=?,type_basis=? WHERE question_id=?',(str(question_type),'explicit specialist-reviewed type by '+reviewer,qid));db.execute('INSERT OR REPLACE INTO review_metadata_origins VALUES(?,?,?,?)',(qid,'question_type',reviewer,review_hash))
        else:reset_reviewed_type(db,qid,reviewer)
        out['active_reviews'].append({'question_id':qid,'reviewer':reviewer,'review_hash':review_hash})
        if previous and previous[0]==review_hash:
            # Backfill origin metadata for reviews imported before origin tracking existed.
            for dim,item in r.get('verification',{}).items():
                if not isinstance(item,dict) or not item.get('evidence'):continue
                origin=db.execute('SELECT 1 FROM verification_origins WHERE question_id=? AND dimension=?',(qid,dim)).fetchone();v=db.execute('SELECT status,evidence,reviewer,record_sha256 FROM verification WHERE question_id=? AND dimension=?',(qid,dim)).fetchone()
                if not origin and v and tuple(v)==(item.get('status','pending'),item['evidence'],reviewer,current[0]):db.execute('INSERT INTO verification_origins VALUES(?,?,?,?)',(qid,dim,'review:'+reviewer,review_hash))
            out['unchanged_reviews']+=1;continue
        verification=r.get('verification',{});mapping=verification.get('mapping',{});mstatus=mapping.get('status','pending') if isinstance(mapping,dict) and mapping.get('evidence') else 'pending'
        # Only after complete review validation: replace this reviewer's current links.
        db.execute('DELETE FROM scope_evidence WHERE question_id=? AND reviewer=?',(qid,reviewer))
        for dim,item in verification.items():
            if not isinstance(item,dict) or not item.get('evidence'):continue
            update_verification(db,qid,dim,item.get('status','pending'),item['evidence'],reviewer,current[0],date,origin='review:'+reviewer,review_hash=review_hash)
        for m in r.get('mappings',[]):
            bid=m['scope_bullet_id'];eid=digest(dump([qid,bid,m['assessed_skill'],reviewer]).encode())
            db.execute('INSERT OR REPLACE INTO scope_evidence VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(eid,qid,m['code'],bid,m['assessed_skill'],m['relevance'],m['evidence'],int(m.get('covers_full_bullet') is True),reviewer,date,current[0],mstatus,dump(m)));out['imported']+=1
        db.execute('INSERT OR REPLACE INTO review_records VALUES(?,?,?,?,?)',(qid,reviewer,review_hash,review_json,now()))
        db.execute('INSERT INTO review_history(question_id,reviewer,review_hash,review_json,imported_at) VALUES(?,?,?,?,?)',(qid,reviewer,review_hash,review_json,now()));out['accepted_reviews']+=1
    return out

def sync_review_snapshot(db,payload,source_key):
    previous={(r['question_id'],r['reviewer']):dict(r) for r in db.execute('SELECT * FROM review_source_memberships WHERE source_key=?',(source_key,))}
    result=import_reviews(db,payload);active={(r['question_id'],r['reviewer']):r for r in result['active_reviews']};revoked=0
    for pair,old in previous.items():
        if pair in active:continue
        qid,reviewer=pair;reset_reviewed_type(db,qid,reviewer,old['review_hash']);current=db.execute('SELECT review_hash FROM review_records WHERE question_id=? AND reviewer=?',pair).fetchone()
        if current and current[0]==old['review_hash']:
            db.execute('DELETE FROM scope_evidence WHERE question_id=? AND reviewer=?',pair);db.execute('DELETE FROM review_records WHERE question_id=? AND reviewer=?',pair);revoked+=1
        sha=db.execute('SELECT record_sha256 FROM questions WHERE question_id=?',(qid,)).fetchone()[0]
        for dim in DIMENSIONS:
            origin=db.execute('SELECT origin,review_hash FROM verification_origins WHERE question_id=? AND dimension=?',(qid,dim)).fetchone()
            if origin and origin['origin']=='review:'+reviewer and origin['review_hash']==old['review_hash']:
                update_verification(db,qid,dim,'pending','Previously imported approved review was withdrawn or superseded; renewed checked evidence is required.','approval-snapshot-sync',sha,origin='approval-snapshot-sync')
    db.execute('DELETE FROM review_source_memberships WHERE source_key=?',(source_key,))
    db.executemany('INSERT INTO review_source_memberships VALUES(?,?,?,?)',[(source_key,r['question_id'],r['reviewer'],r['review_hash']) for r in active.values()]);result['revoked_reviews']=revoked
    return result

# Query-expansion only. These aliases never create reviewed question-to-scope evidence.
ALIASES={'counted loop':['counted loop','count controlled'],'conditional loop':['conditional loop','condition controlled'],'pre condition loop':['pre condition loop','precondition loop','pre test','pretest'],'post condition loop':['post condition loop','postcondition loop','post test','posttest','repeat until']}
def concepts(text):
    n=' '.join('loop' if w=='loops' else w for w in norm(text).split());return {k for k,vs in ALIASES.items() if any((' '+v+' ') in (' '+n+' ') for v in vs)}
def skill_match(request,skill):
    a,b=norm(request),norm(skill)
    if a and (' '+a+' ') in (' '+b+' '):return True
    cs=concepts(request)
    return bool(cs and cs.issubset(concepts(skill)))

def requirements(db,query='',code='',scope_text=''):
    text=scope_text or query;codes=list(dict.fromkeys(([code] if code else [])+re.findall(r'\b[AB]\d\.\d\.\d+\b',text,re.I)));codes=[c.upper() for c in codes];requested=[]
    # Full literal guidance receives a bullet match; concepts inside a bullet remain aspect requests.
    for line in re.split(r'[\n;]+',text):
        clean=re.sub(r'\b[AB]\d\.\d\.\d+\b','',line,flags=re.I).strip(' :•-')
        if not clean:continue
        # Split explicitly listed recognized loop concepts, including user's representative query.
        found=[k for k in ALIASES if k in concepts(clean)]
        exact=db.execute('SELECT * FROM bullets').fetchall();matches=[b for b in exact if norm(b['text'])==norm(clean)]
        statements=[o for o in db.execute('SELECT code,statement FROM objectives') if norm(o['statement'])==norm(clean)]
        if statements:requested.extend({'requirement':o['statement'],'kind':'statement','code_candidates':[o['code']]} for o in statements)
        elif matches:requested.extend({'requirement':b['text'],'kind':'bullet','bullet_id':b['bullet_id'],'code_candidates':[b['code']]} for b in matches)
        elif len(found)>1:requested.extend({'requirement':k,'kind':'aspect','code_candidates':codes} for k in found)
        else:requested.append({'requirement':clean,'kind':'aspect','code_candidates':codes})
    if not requested and codes:
        for c in codes:
            requested.extend({'requirement':b['text'],'kind':'bullet','bullet_id':b['bullet_id'],'code_candidates':[c]} for b in db.execute('SELECT * FROM bullets WHERE code=?',(c,)))
    return requested,codes

def detail(db,qid,include_answer=False):
    row=db.execute('SELECT * FROM questions WHERE question_id=?',(qid,)).fetchone()
    if not row:return None
    q=json.loads(row['question_json']);legacy_codes=list(q['syllabus_codes']);mapping_check=db.execute("SELECT status,record_sha256 FROM verification WHERE question_id=? AND dimension='mapping'",(qid,)).fetchone();mapping_current=bool(mapping_check and mapping_check['status']=='verified' and mapping_check['record_sha256']==row['record_sha256']);reviewed_codes=[r[0] for r in db.execute("SELECT DISTINCT code FROM scope_evidence WHERE question_id=? AND record_sha256=? AND mapping_status='verified' AND relevance IN ('direct','partial')",(qid,row['record_sha256']))] if mapping_current else [];codes=sorted(set(legacy_codes+reviewed_codes));objectives=[dict(r) for r in db.execute('SELECT code,theme,topic,statement,level FROM objectives WHERE code IN ('+','.join('?' for _ in codes)+') ORDER BY code',codes)];q['legacy_syllabus_codes']=legacy_codes;q['reviewed_syllabus_codes']=reviewed_codes;q['syllabus_codes']=codes
    for objective in objectives:objective['mapping_basis']='legacy candidate + reviewed aspect' if objective['code'] in legacy_codes and objective['code'] in reviewed_codes else 'reviewed aspect' if objective['code'] in reviewed_codes else 'legacy code candidate only'
    raw_theme=q.get('theme');q['raw_theme']=raw_theme;q['themes']=sorted({o['theme'] for o in objectives});q['theme']=' + '.join(q['themes']);q['topics']=sorted({o['topic'] for o in objectives});q['levels']=sorted({o['level'] for o in objectives});q['raw_level']=q.get('level');q['level']=q['levels'][0] if len(q['levels'])==1 else 'Mixed common/HL';q['target_papers']=['Paper 1' if t=='A' else 'Paper 2' for t in q['themes']];q['question_type']=row['question_type'];q['question_type_basis']=row['type_basis'];q['objectives']=objectives;q['record_sha256']=row['record_sha256'];q['outstanding_issues']=json.loads(row['issues_json']);q['verification']={r['dimension']:{k:r[k] for k in ['status','evidence','reviewer','reviewed_at','record_sha256']} for r in db.execute('SELECT * FROM verification WHERE question_id=?',(qid,))};q['scope_evidence']=[dict(r) for r in db.execute('SELECT * FROM scope_evidence WHERE question_id=? ORDER BY code,bullet_id',(qid,))];q['provenance']=[]
    for r in db.execute('SELECT source_json FROM source_refs WHERE question_id=?',(qid,)):
        s=json.loads(r[0]);q['provenance'].append({k:s.get(k) for k in ['source_question_id','source_id','source_filename','year','session','paper','zone','option','question','subquestion','source_pdf_pages'] }|{'markscheme':{k:s.get('markscheme',{}).get(k) for k in ['status','source_id','filename','pdf_pages']}})
    for e in q['scope_evidence']:
        e['effective_mapping_status']='stale' if e['record_sha256']!=row['record_sha256'] else e['mapping_status'] if mapping_current else (mapping_check['status'] if mapping_check else 'pending')
        bullet=db.execute('SELECT text,scope_kind FROM bullets WHERE bullet_id=?',(e['bullet_id'],)).fetchone();e['exact_guidance']=bullet['text'];e['scope_kind']=bullet['scope_kind']
    for objective in q['objectives']:
        official=json.loads(db.execute('SELECT full_json FROM objectives WHERE code=?',(objective['code'],)).fetchone()[0]);objective['guidance']=official['guidance'];objective['source_pdf_pages']=official['source_pdf_pages'];objective['global_scope_note']=official.get('global_scope_note','')
    q['review_scope_not_assessed']=[]
    for review_row in db.execute('SELECT review_json FROM review_records WHERE question_id=?',(qid,)):
        review=json.loads(review_row[0]);q['outstanding_issues'].extend(review.get('issues',[]));q['review_scope_not_assessed'].extend(review.get('scope_not_assessed',[]))
    q['usage_history']=[dict(r) for r in db.execute('SELECT * FROM usage_history WHERE question_id=? ORDER BY used_at',(qid,))];q['duplicate_groups']=[dict(r) for r in db.execute('SELECT * FROM duplicate_groups WHERE question_id=?',(qid,))]
    if include_answer:q['answer']=json.loads(db.execute('SELECT answer_json FROM answers WHERE question_id=?',(qid,)).fetchone()[0])
    return q

def search(db,filters):
    query=str(filters.get('text',''));requested,codes=requirements(db,query,str(filters.get('code','')),str(filters.get('scope_text','')));exact_id=db.execute('SELECT question_id FROM questions WHERE lower(question_id)=lower(?)',(query.strip(),)).fetchone();
    if exact_id and not filters.get('scope_text') and not filters.get('code'):requested=[];codes=[]
    ids={r[0] for r in db.execute('SELECT question_id FROM questions')};content_ids=set();terms=re.findall(r'[a-zA-Z0-9_]+',query)
    if terms:
        fts=' AND '.join('"'+t+'"' for t in terms);content_ids={r[0] for r in db.execute('SELECT question_id FROM question_fts WHERE question_fts MATCH ?',(fts,))}
        candidate_codes=set(codes)
        qnorm=norm(query)
        for r in db.execute('SELECT * FROM objectives'):
            if qnorm in norm(r['topic']) or qnorm in norm(r['statement']):candidate_codes.add(r['code'])
        for r in db.execute('SELECT * FROM bullets'):
            if qnorm in norm(r['text']):candidate_codes.add(r['code'])
        for c in candidate_codes:content_ids.update(r[0] for r in db.execute('SELECT question_id FROM question_codes WHERE code=?',(c,)))
        for e in db.execute("SELECT question_id,assessed_skill FROM scope_evidence WHERE mapping_status='verified' AND relevance IN ('direct','partial')"):
            if skill_match(query,e['assessed_skill']) or any(skill_match(req['requirement'],e['assessed_skill']) for req in requested):content_ids.add(e['question_id'])
        ids&=({exact_id[0]} if exact_id else content_ids)
    if codes:
        code_ids={r[0] for c in codes for r in db.execute('SELECT question_id FROM question_codes WHERE code=?',(c,))};code_ids|={r[0] for c in codes for r in db.execute('SELECT question_id FROM scope_evidence WHERE code=?',(c,))};ids&=code_ids
    if filters.get('scope_text') and not query:
        # Scope text alone is genuine search input; collect evidence and code-linked candidates.
        scoped=set()
        for e in db.execute('SELECT question_id,assessed_skill FROM scope_evidence'):
            if any(skill_match(req['requirement'],e['assessed_skill']) for req in requested):scoped.add(e['question_id'])
        for req in requested:
            for c in req['code_candidates']:scoped.update(r[0] for r in db.execute('SELECT question_id FROM question_codes WHERE code=?',(c,)))
        if scoped:ids&=scoped
        else:ids=set()
    checked=[];unverified=[];global_matches=set();global_complete=set()
    for qid in sorted(ids):
        q=detail(db,qid)
        if filters.get('theme') and filters['theme'] not in q['themes']:continue
        if filters.get('topic') and norm(filters['topic']) not in norm(' '.join(q['topics'])):continue
        if filters.get('level') and filters['level'] not in q['levels'] and filters['level']!=q['level']:continue
        if filters.get('difficulty') and filters['difficulty']!=q.get('difficulty'):continue
        if filters.get('question_type') and filters['question_type']!=q['question_type']:continue
        if filters.get('target_paper') and filters['target_paper'] not in q['target_papers']:continue
        if filters.get('year') and not any(str(p['year'])==str(filters['year']) for p in q['provenance']):continue
        if filters.get('session') and not any(p['session']==filters['session'] for p in q['provenance']):continue
        if filters.get('minMarks') not in ('',None) and q['marks']<float(filters['minMarks']):continue
        if filters.get('maxMarks') not in ('',None) and q['marks']>float(filters['maxMarks']):continue
        current_evidence=[e for e in q['scope_evidence'] if e['effective_mapping_status']=='verified' and e['record_sha256']==q['record_sha256']]
        reviewed=[e for e in current_evidence if e['relevance'] in ('direct','partial')]
        all_verified=all(q['verification'].get(d,{}).get('status')=='verified' and q['verification'].get(d,{}).get('record_sha256')==q['record_sha256'] for d in DIMENSIONS)
        if filters.get('verified')=='verified' and not all_verified:continue
        if filters.get('verified')=='unverified' and all_verified:continue
        matched=[];unmet=[]
        for i,req in enumerate(requested):
            es=[e for e in (current_evidence if req['kind']=='statement' else reviewed) if (not req['code_candidates'] or e['code'] in req['code_candidates']) and ((req['kind']=='statement' and json.loads(e['raw_json']).get('statement_relevance') in ('direct','partial')) or (req['kind']=='bullet' and e['bullet_id']==req['bullet_id']) or (req['kind']=='aspect' and skill_match(req['requirement'],e['assessed_skill'])))]
            if es:
                complete=any((json.loads(e['raw_json']).get('statement_relevance')=='direct') if req['kind']=='statement' else (e['relevance']=='direct' and (req['kind']!='bullet' or e['covers_full_bullet'])) for e in es)
                matched.append({'requirement':req,'relevance':'direct' if complete else 'partial','evidence':es});global_matches.add(i)
                if complete:global_complete.add(i)
                if not complete:unmet.append({'requirement':req,'reason':'Some assessed aspects established; full requested requirement is not established.'})
            else:unmet.append({'requirement':req,'reason':'No current verified question-to-scope evidence establishes this requirement.'})
        q['matched_requirements']=matched;q['unmet_requirements']=unmet;q['all_dimensions_verified']=all_verified
        if (requested and matched) or (not requested and reviewed):q['relevance']='direct' if requested and not unmet else 'partial';checked.append(q)
        else:q['relevance']='unverified candidate';unverified.append(q)
    checked.sort(key=lambda q:(q['relevance']!='direct',-len(q['matched_requirements']),q['question_id']))
    include=filters.get('include_candidates','true')!='false';result=checked+(unverified if include else []);offset=max(0,int(filters.get('offset',0)));limit=max(1,min(200,int(filters.get('limit',20))))
    return {'total':len(result),'checked_count':len(checked),'unverified_candidate_count':len(unverified),'offset':offset,'limit':limit,'questions':result[offset:offset+limit],'requested_requirements':requested,'requirements_with_no_established_match':[req for i,req in enumerate(requested) if i not in global_matches],'requirements_without_full_match':[req for i,req in enumerate(requested) if i not in global_complete],'notice':'Direct/partial labels apply only to the exact assessed aspect and reviewed evidence. They do not certify an entire syllabus statement/bullet. Candidates remain unverified.'}

def public_question(q):
    if q is None:return None
    out=json.loads(dump(q));out.pop('answer',None)
    for v in out.get('verification',{}).values():v.pop('evidence',None)
    for e in out.get('scope_evidence',[]):
        e.pop('evidence',None);e.pop('raw_json',None)
    for matched in out.get('matched_requirements',[]):
        for e in matched.get('evidence',[]):e.pop('evidence',None);e.pop('raw_json',None)
    out['outstanding_issue_count']=len(out.get('outstanding_issues',[]));out.pop('outstanding_issues',None)
    return out

def public_search(result):
    return dict(result,questions=[public_question(q) for q in result['questions']])

def save_selection(db,ids,query=None,metadata=None):
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate selected IDs')
    records=[detail(db,qid) for qid in ids]
    if any(q is None for q in records):raise ValueError('Unknown selected question ID')
    sid=str(uuid.uuid4());metadata=metadata or {};stamp=now();hashes={q['question_id']:q['record_sha256'] for q in records}
    with db:db.execute('INSERT INTO selections VALUES(?,?,?,?,?,?)',(sid,stamp,dump(query or {}),dump(ids),dump(hashes),dump(metadata)))
    return {'selection_id':sid,'created_at':stamp,'query':query or {},'record_hashes':hashes,'metadata':metadata,'title':'Unofficial question retrieval selection — not an assembled examination','unofficial':True,'total_marks':sum(q['marks'] for q in records),'questions':[{k:q.get(k) for k in ['question_id','question_text','marks','syllabus_codes','command_term','assets']} for q in records]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--db',type=Path,default=DB);sub=p.add_subparsers(dest='command',required=True);i=sub.add_parser('import');i.add_argument('--root',type=Path,default=ROOT);s=sub.add_parser('search');s.add_argument('--text',default='');s.add_argument('--code',default='');r=sub.add_parser('import-reviews');r.add_argument('file',type=Path);bk=sub.add_parser('backup');bk.add_argument('destination',type=Path);a=p.parse_args();db=connect(a.db)
    if a.command=='import':result=import_project(db,a.root)
    elif a.command=='search':result=search(db,{'text':a.text,'code':a.code})
    elif a.command=='backup':
        if a.destination.resolve()==a.db.resolve():raise ValueError('Backup destination must differ from live DB')
        a.destination.parent.mkdir(parents=True,exist_ok=True);tmp=a.destination.with_name(a.destination.name+'.tmp');target=sqlite3.connect(tmp);db.backup(target);target.close();os.replace(tmp,a.destination);result={'backup':str(a.destination),'bytes':a.destination.stat().st_size,'sha256':digest(a.destination.read_bytes())}
    else:
        with db:result=import_reviews(db,json.loads(a.file.read_text()))
    print(json.dumps(result,ensure_ascii=False,indent=2));db.close()
if __name__=='__main__':main()
