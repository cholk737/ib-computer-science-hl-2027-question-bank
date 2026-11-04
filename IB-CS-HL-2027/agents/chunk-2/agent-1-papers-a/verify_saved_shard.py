"""Verify the actual saved records after all editorial changes."""
from pathlib import Path
import collections
import contextlib
import hashlib
import io
import json
import re
import sqlite3

O=Path(__file__).resolve().parent
P=O.parents[2]
INV={r['source_id']:r for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())}
S={r['code']:r for r in json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())}
report={'papers':{},'sql':{},'python':[],'source_hashes':{},'problems':[]}
all_sources=[];all_practice=[];all_batches=[]
for sid in ['SRC-001','SRC-005','SRC-008','SRC-018','SRC-024','SRC-030','SRC-034','SRC-042']:
    paths=sorted((O/'batches').glob(sid+'-b*.json'))
    batches=[json.loads(p.read_text()) for p in paths]
    source=[r for b in batches for r in b['source_questions']]
    practice=[q for b in batches for q in b['practice_questions']]
    audit=json.loads((O/'papers'/sid/'paper_audit.json').read_text())
    assert audit['complete'] and len(source)==audit['leaf_count']
    assert sum(r['original_marks'] for r in source)==audit['extracted_total_marks']
    counts=collections.Counter(r['relevance_status'] for r in source)
    assert dict(counts)==audit['counts'] and len(practice)==audit['converted_count']
    if sid in ['SRC-034','SRC-042']:
        options={c:sum(r['original_marks'] for r in source if r['option']==c) for c in 'ABCD'}
        assert options==dict.fromkeys('ABCD',65),options
    else:options={}
    for r in source:
        assert r['assets'] and r['source_context_page_evidence']
        assert (P/r['complete_original_document_path']).is_file()
        for a in r['assets']:assert (P/a['path']).is_file(),a
        for e in r['source_context_page_evidence']:
            assert (P/e['image_path']).is_file()
            if 'text_path' in e:assert (P/e['text_path']).is_file()
        for m in r['mappings']:
            assert m['syllabus_code'] in S
            assert m['scope_evidence']==S[m['syllabus_code']]['guidance']
            assert m['mapping_target']==('adapted_practice_only' if r['relevance_status']=='B' else 'original_and_adapted')
        if r['relevance_status']=='C':assert not r['mappings'] and r['exclusion_reason']
        if sid!='SRC-001':assert '[Source PDF page ' in r['original_text'] and r['original_text_manual_synopsis']
    for q in practice:
        assert q['unofficial'] and q['markscheme_status'].startswith('preliminary_unofficial')
        assert sum(p['marks'] for p in q['marking_points'])==q['marks'],q['question_id']
        assert re.search(r'\b'+re.escape(q['command_term'])+r'\b',q['question_text'],re.I),(q['question_id'],q['command_term'])
        if q.get('code'):
            ns={}
            with contextlib.redirect_stdout(io.StringIO()):
                exec(q['code'],ns);exec(q['test_code'],ns)
            solution_test=False
            if q.get('solution','').lstrip().startswith(('def ','class ')):
                # The solution is a separately edited field and is executed too.
                ns={}
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(q['solution'],ns);exec(q['test_code'],ns)
                solution_test=True
            report['python'].append(dict(question_id=q['question_id'],code_and_tests_passed=True,separate_solution_tested=solution_test))
    for source_id in [sid]+[x for x in INV[sid]['paired_source_ids'].split(';') if x]:
        if source_id in report['source_hashes']:continue
        h=hashlib.sha256((P/INV[source_id]['project_path']).read_bytes()).hexdigest()
        assert h==INV[source_id]['sha256'],source_id
        report['source_hashes'][source_id]=dict(unchanged=True,sha256=h)
    report['papers'][sid]=dict(source_leaves=len(source),practice_questions=len(practice),counts=dict(counts),marks=sum(r['original_marks'] for r in source),option_marks=options,batches=len(paths),source_transcription='manual_raster_authoritative' if sid=='SRC-001' else 'verbatim_marked_intervals')
    all_sources+=source;all_practice+=practice;all_batches+=paths

assert len({r['source_question_id'] for r in all_sources})==len(all_sources)
assert len({q['question_id'] for q in all_practice})==len(all_practice)
byq={q['question_id']:q for q in all_practice}
conn=sqlite3.connect(':memory:')
conn.executescript('''
CREATE TABLE Buyer(BuyerID INTEGER PRIMARY KEY,FirstName TEXT,Surname TEXT);
CREATE TABLE Invoice(InvoiceID INTEGER PRIMARY KEY,BuyerID INTEGER,InvoiceDate TEXT);
INSERT INTO Buyer VALUES(1,'Mira','Shah'),(2,'Mira','Other');
INSERT INTO Invoice VALUES(10,1,'2026-01-02'),(11,2,'2026-02-01');
CREATE TABLE Role(RoleID INTEGER PRIMARY KEY,Grade INTEGER);
CREATE TABLE Employee(EmployeeID INTEGER PRIMARY KEY,RoleID INTEGER,FirstName TEXT,Surname TEXT);
INSERT INTO Role VALUES(1,8),(2,7);
INSERT INTO Employee VALUES(1,1,'Nila','Patel'),(2,2,'Ari','Patel'),(3,1,'Bo','Jones');
''')
expected={'P-SRC034-Q01-e':[('Mira','Shah','2026-01-02')],'P-SRC042-Q01-d':[('Nila','Patel',8)]}
for qid,wanted in expected.items():
    sql=byq[qid]['solution'];got=conn.execute(sql).fetchall();assert got==wanted,(qid,got)
    report['sql'][qid]=dict(sql=sql,result=got,passed=True)
conn.close()

# Constructor-only answers have no standalone code field; run them with their
# supplied constructor signatures to check values and exact argument order.
class Producer:
    def __init__(self,name,region):self.name=name;self.region=region
ns={'Producer':Producer};exec(byq['P-SRC042-Q14-c']['solution'],ns)
assert (ns['supplier'].name,ns['supplier'].region)==('Aster Works','North')
class ChilledItem:
    def __init__(self,name,stock):self.name=name;self.stock=stock
ns={'ChilledItem':ChilledItem};exec(byq['P-SRC034-Q14-e']['solution'],ns)
assert (ns['item'].name,ns['item'].stock)==('VaccinePack',60)
report['constructor_snippets']=['P-SRC042-Q14-c','P-SRC034-Q14-e']
report['totals']=dict(source_leaves=len(all_sources),local_practice_questions=len(all_practice),counts=dict(collections.Counter(r['relevance_status'] for r in all_sources)),source_marks=sum(r['original_marks'] for r in all_sources),batches=len(all_batches),reused_conversions=sum(bool(r.get('adaptation_reuse_question_id')) for r in all_sources),python_programs=len(report['python']))
report['all_practice_mark_sums_correct']=True
report['all_record_ids_unique']=True
report['all_source_assets_exist']=True
(O/'checks/FINAL_SAVED_SHARD_CHECK.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report['totals']))
print('SQL, Python code and solution fields, constructor snippets, mark totals, mappings, IDs, evidence paths and unchanged source hashes pass.')
