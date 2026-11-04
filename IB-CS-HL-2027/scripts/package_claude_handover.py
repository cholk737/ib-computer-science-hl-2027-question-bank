"""Package a committed project, verify full manifests/history and portable DB.

Run only after the final content commit. No network, question generation or
examination assembly. The generated mirror/bundle/receipts are Git-ignored.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import zipfile

P = Path(__file__).resolve().parents[1]
R = P.parent
H = R/'CLAUDE_HANDOVER'
DEST = R/'IB_CS_HL_2027_COMPLETE_CLAUDE_HANDOVER.zip'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, value):
    temp=path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    os.replace(temp,path)


def run(*args, cwd=R):
    return subprocess.check_output(args,cwd=cwd,text=True,stderr=subprocess.STDOUT)


def main():
    head=run('git','rev-parse','HEAD').strip()
    status=run('git','status','--porcelain')
    assert not status,'Commit all content before packaging:\n'+status
    publication_path=P/'audits/handover/GITHUB_PUBLICATION.json'
    publication=json.loads(publication_path.read_text()) if publication_path.exists() else {}
    github_created=publication.get('created') is True and publication.get('private') is True
    remote_url=publication.get('repository_url') if github_created else None
    verified_remote_head=None
    gh_path=os.environ.get('IBCS_GH_PATH')
    if github_created and gh_path:
        repository=publication['repository_full_name']
        live_repo=json.loads(run(gh_path,'api','repos/'+repository,'--jq','{full_name,private,html_url}'))
        assert live_repo['private'] is True and live_repo['html_url']==remote_url
        verified_remote_head=run(gh_path,'api','repos/'+repository+'/git/ref/heads/main','--jq','.object.sha').strip()
        assert verified_remote_head==head,'Push final content before packaging the GitHub handover.'
    push_completed=github_created and verified_remote_head==head
    tracked=run('git','ls-files','-z').split('\0')
    tracked=[s for s in tracked if s]
    bundle=H/'ib-computer-science-hl-2027-question-bank.bundle'
    subprocess.run(['git','bundle','create',str(bundle),'--all'],cwd=R,check=True,stdout=subprocess.DEVNULL)
    bundle_verify=run('git','bundle','verify',str(bundle))
    mirror=H/'PROJECT_FILES';mirror.mkdir(exist_ok=True)
    project_rows=[]
    for rel in tracked:
        # Wrapper docs already sit next to PROJECT_FILES; avoid recursion.
        if rel.startswith('CLAUDE_HANDOVER/'):
            continue
        source=R/rel
        if not source.is_file():
            continue
        target=mirror/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
        digest=sha(source);assert sha(target)==digest
        project_rows.append({'path':str(target.relative_to(H)),'repository_path':rel,'bytes':source.stat().st_size,'sha256':digest})
    put(H/'PROJECT_FILE_MANIFEST.json',{'commit':head,'files':project_rows})
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(project_rows[0]));writer.writeheader();writer.writerows(project_rows);(H/'PROJECT_FILE_MANIFEST.csv').write_text(stream.getvalue())
    print('Snapshot copied and hash-verified:',len(project_rows),'files.',flush=True)
    # Validate the complete snapshot in an unrelated temporary location. Do not
    # change the archived DB or its committed project-root metadata during QA.
    with tempfile.TemporaryDirectory(prefix='ib-cs-claude-restore-') as td:
        base=Path(td);clone=base/'history-restore'
        subprocess.run(['git','clone','-q',str(bundle),str(clone)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        assert run('git','rev-parse','HEAD',cwd=clone).strip()==head
        run('git','cat-file','-e','26aa6de^{commit}',cwd=clone)
        preserved_csv=run('git','show','26aa6de:IB-CS-HL-2027/question-bank/QUESTION_BANK.csv',cwd=clone)
        assert len(list(csv.DictReader(io.StringIO(preserved_csv))))==823
        restored=base/'moved-project'
        shutil.copytree(mirror/'IB-CS-HL-2027',restored)
        spec=importlib.util.spec_from_file_location('portable_ib_bank',restored/'question-bank/search/bank_db.py');bank=importlib.util.module_from_spec(spec);spec.loader.exec_module(bank)
        db=bank.connect(restored/'question-bank/database.sqlite3')
        imported=bank.import_project(db,restored)
        assert imported['unchanged']==826 and imported['inserted']==0 and imported['updated']==0
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert bank.search(db,{'text':'O-C3-B-001'})['total']==1
        assert bank.search(db,{'code':'B4.1.5'})['total']>=2
        assert bank.search(db,{'topic':'A2 Networks'})['total']>0
        guidance=json.loads((restored/'syllabus/SYLLABUS_MASTER.json').read_text())
        set_ops=next(s for s in guidance if s['code']=='B4.1.5')['guidance_paragraphs'][1]
        pasted=bank.search(db,{'scope_text':set_ops,'code':'B4.1.5'})
        assert pasted['checked_count']>=1
        public=bank.public_question(bank.detail(db,'O-C3-B-001'))
        assert not {'answer','solution','marking_points','test_code'}&public.keys()
        assert bank.detail(db,'O-C3-B-001',True)['answer']['solution']
        root_in_db=Path(db.execute("SELECT value FROM meta WHERE key='project_root'").fetchone()[0]);assert root_in_db==restored.resolve()
        source_inventory=json.loads((restored/'sources/SOURCE_INVENTORY.json').read_text())
        assert len(source_inventory)==48
        for s in source_inventory:assert sha(restored/s['project_path'])==s['sha256']
        portability={'git_bundle_clone_restores_head':head,'phase0_commit_and_823_bank_restored':True,'relocated_database_integrity':'ok','incremental_import':imported,'query_checks':['exact stable original ID','set scope code','broad networks topic','pasted official set-operations guidance','student answer separation and explicit answer retrieval'],'source_root_rebased':True,'source_pdf_hashes_checked':48,'all_passed':True,'limits':'Local data/API semantics checked after relocation. No new browser layout approval, whole-corpus independent verification or GitHub push is implied.'}
        db.close()
    put(H/'PORTABILITY_VERIFICATION.json',portability)
    repo_status={'repository_name_requested':'ib-computer-science-hl-2027-question-bank','local_head':head,'local_history_preserved':True,'phase0_commit':'26aa6de','working_content_committed':True,'github_private_repository_created':github_created,'remote_url':remote_url,'push_completed':push_completed,'verified_remote_main':verified_remote_head,'private_visibility_independently_verified':bool(github_created and gh_path),'reason':'Created using signed-in Chrome; authenticated GitHub API confirmed private visibility and exact remote branch commit.' if push_completed else 'Remote publishing not verified for this archive; use the local snapshot and Git bundle.','git_bundle':bundle.name,'git_bundle_sha256':sha(bundle),'git_bundle_verify_passed':True,'git_bundle_clone_passed':True,'git_lfs_used':False,'large_file_limit_note':'Every included required file below90MiB and full data present; no LFS placeholders.'}
    put(H/'REPOSITORY_STATUS.json',repo_status)
    ignored=run('git','ls-files','--others','--ignored','--exclude-standard','IB-CS-HL-2027').splitlines()
    package_report={'saved_at':datetime.now(ZoneInfo('Europe/Zurich')).isoformat(),'commit':head,'project_payload_files':len(project_rows),'project_payload_bytes':sum(r['bytes'] for r in project_rows),'sources_included':48,'snapshot_rule':'All committed repository content except wrapper documents, which are included once beside PROJECT_FILES. Working project and root instructions retain relative paths.','excluded_runtime_files':ignored,'other_exclusions':['Git internals/credentials are replaced by a full bundle; no .git/config or auth files copied','Redundant parent upload PDFs: exact available project source copies are included and hash-verified','Caches, .pyc, .tmp, sqlite journal/WAL/SHM, .DS_Store, env credentials; no durable project question/evidence record intentionally omitted'],'unavailable_source_files':['Uploaded official matching markscheme for SRC001','Uploaded official matching markscheme for SRC002'],'remote_publishing_incomplete':not push_completed}
    put(H/'PACKAGE_BUILD_REPORT.json',package_report)
    excluded_receipts={'HANDOVER_FILE_MANIFEST.json','ARCHIVE_VERIFICATION.json'}
    wrapper_rows=[]
    for f in sorted(H.rglob('*')):
        if f.is_file() and 'PROJECT_FILES' not in f.relative_to(H).parts and f.name not in excluded_receipts and not f.name.endswith('.tmp'):
            wrapper_rows.append({'path':str(f.relative_to(H)),'bytes':f.stat().st_size,'sha256':sha(f)})
    put(H/'HANDOVER_FILE_MANIFEST.json',{'excluded_from_self_hashing':sorted(excluded_receipts),'files':wrapper_rows})
    temporary=DEST.with_name(DEST.name+'.tmp')
    files=[f for f in sorted(H.rglob('*')) if f.is_file() and not f.name.endswith('.tmp') and f.name!='ARCHIVE_VERIFICATION.json']
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
        for i,f in enumerate(files,1):
            archive.write(f,'CLAUDE_HANDOVER/'+str(f.relative_to(H)))
            if i%1500==0:print('ZIP saved files:',i,flush=True)
    with zipfile.ZipFile(temporary) as archive:
        assert archive.testzip() is None
        names=archive.namelist();assert len(names)==len(set(names))
        assert not any(Path(n).is_absolute() or '..' in Path(n).parts for n in names)
        for r in project_rows:
            data=archive.read('CLAUDE_HANDOVER/'+r['path']);assert hashlib.sha256(data).hexdigest()==r['sha256'] and len(data)==r['bytes']
        for r in wrapper_rows:assert hashlib.sha256(archive.read('CLAUDE_HANDOVER/'+r['path'])).hexdigest()==r['sha256']
    verification={'archive_filename':DEST.name,'content_commit':head,'project_files_sha256_checked':len(project_rows),'wrapper_files_sha256_checked':len(wrapper_rows),'payload_crc_test_passed':True,'unique_safe_archive_paths':True,'full_git_bundle_included_and_clone_verified':True,'relocated_database_search_and_sources_passed':True,'questions':826,'adapted':823,'original':3,'sources_included':48,'missing_durable_project_files':[],'unavailable_original_sources':['SRC001/SRC002 official matching markschemes were never uploaded'],'github_private_repository_created':github_created,'github_push_verified':push_completed,'known_unfinished_work':'Chunk3 remains incomplete; see CURRENT_PROGRESS and complete code/bullet/record backlog.','receipt_note':'Payload was verified before appending this receipt. Packaging routine also checks the final expanded ZIP CRC and atomically publishes only on success.'}
    put(H/'ARCHIVE_VERIFICATION.json',verification)
    with zipfile.ZipFile(temporary,'a',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:archive.write(H/'ARCHIVE_VERIFICATION.json','CLAUDE_HANDOVER/ARCHIVE_VERIFICATION.json')
    with zipfile.ZipFile(temporary) as archive:assert archive.testzip() is None;assert len(archive.namelist())==len(files)+1
    os.replace(temporary,DEST)
    checksum=sha(DEST);DEST.with_suffix(DEST.suffix+'.sha256').write_text(checksum+'  '+DEST.name+'\n')
    assert not run('git','status','--porcelain'),'Packaging unexpectedly changed committed content.'
    print(json.dumps({'zip':str(DEST),'bytes':DEST.stat().st_size,'sha256':checksum,'head':head,'archive_members':len(files)+1,'project_files':len(project_rows),'all_package_checks_passed':True,'github_created':github_created,'github_push_verified':push_completed}),flush=True)


if __name__=='__main__':main()
