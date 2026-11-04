"""Validate deliverable integrity; save a durable final checksum checkpoint."""
from pathlib import Path
import csv,json,hashlib,re,unicodedata,collections
P=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(s):return re.sub(r'\s+','',unicodedata.normalize('NFKC',s)).replace('(HLonly)','')
inventory=json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())
assert len(inventory)==48 and len(set(r['sha256'] for r in inventory))==47
for r in inventory:
 assert digest(Path(r['original_path']))==r['sha256']==digest(P/r['project_path'])
master=json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())
index=list(csv.DictReader((P/'syllabus/SYLLABUS_MASTER.csv').open()))
originals={}
for path in ['agent-1-theme-a/theme_a_scope.json','agent-2-theme-b/theme_b_scope.json']:
 originals.update({r['code']:r for r in json.loads((P/'agents/chunk-1'/path).read_text())})
assert len(master)==len(index)==len(originals)==112
for r,c in zip(master,index):
 assert r['code']==c['code'] and r==json.loads((P/r['record_path']).read_text())
 assert r['guidance']==c['guidance'] and r['statement']==c['statement']
 o=originals[r['code']]
 assert norm(r['statement']+r['guidance'])==norm(o.get('statement_with_level_tag',o['statement'])+o['guidance'])
 assert r['coverage_status']=='not_yet_assessed_chunk1' and not r['question_bank_ids']
 assert (P/r['specialist_record_path']).exists()
assert collections.Counter(r['level'] for r in master)=={'SL/HL common':68,'HL-only':44}
for name in ['SYLLABUS_INTEGRATION_CHECK','SPECIMEN_INTEGRATION_CHECK']:
 check=json.loads((P/f'audits/{name}.json').read_text())
 assert check.get('all_pass',check.get('all_assertions_passed',False))
for path in ['mapping/SYLLABUS_MAPPING.csv','question-bank/QUESTION_BANK.csv','coverage/COVERAGE_REPORT.csv']:
 assert len(list(csv.DictReader((P/path).open())))==0
for rel in ['agent-1-theme-a','agent-2-theme-b','agent-3-specimen']:
 assert (P/'agents/chunk-1'/rel/'findings.md').is_file()
spec=list(csv.DictReader((P/'specimen/SPECIMEN_QUESTION_INDEX.csv').open()))
assert len(spec)==54
required=['README.md','AGENTS.md','PROGRESS.md','QA_ISSUES.md','syllabus/SCOPE_VERIFICATION.md','specimen/SPECIMEN_ANALYSIS.md','specimen/EXAM_BLUEPRINT.json','specimen/COMPONENT_MANIFEST.csv']
assert all((P/x).is_file() and (P/x).stat().st_size for x in required)
result={'checkpoint':'C1-FINAL','date':'2026-11-04 Europe/Zurich','status':'all_assertions_passed',
 'pdf_files_hash_verified':48,'unique_pdf_hashes':47,'learning_statements':112,'common':68,'HL_only':44,
 'specimen_reference_parts':54,'native_specialists_completed':3,'historical_question_records':0,'practice_questions':0,
 'stop_boundary':'Step 3 complete; Chunk 2 not started'}
(P/'audits/FINAL_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
excluded={'audits/CHECKPOINT_MANIFEST.json','audits/GIT_CHECKPOINT.md'}
files=[{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':digest(f)} for f in sorted(P.rglob('*')) if f.is_file() and str(f.relative_to(P)) not in excluded and '__pycache__' not in str(f)]
(P/'audits/CHECKPOINT_MANIFEST.json').write_text(json.dumps({'checkpoint':'C1-FINAL','files':files},indent=2)+'\n')
print(json.dumps(result,indent=2));print('Checkpoint files hashed:',len(files))
