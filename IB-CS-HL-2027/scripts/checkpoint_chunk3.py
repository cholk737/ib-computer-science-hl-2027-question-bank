"""Save a recoverable, atomic Chunk 3 snapshot; never infer content verification.

Run from any directory: python3 scripts/checkpoint_chunk3.py --note '...'
Only the coordinator runs this script. Specialist STATUS.json files remain owned
by their authors. A checkpoint records saved state, not a claim that agents live
beyond the current run. Git is a separate explicitly staged operation.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import csv
import hashlib
import json
import os
import sqlite3

P = Path(__file__).resolve().parents[1]
A = P / 'audits/chunk-3'
ROLES = [
    ('Theme A coverage and questions', 'agent-1-theme-a'),
    ('Theme B coverage and Python questions', 'agent-2-theme-b'),
    ('Searchable bank and independent audit', 'agent-3-bank-audit'),
]


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(data, encoding='utf-8')
    os.replace(temporary, path)


def read(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--note', required=True)
    args = parser.parse_args()
    now = datetime.now(ZoneInfo('Europe/Zurich'))
    checkpoint = 'C3-' + now.strftime('%Y%m%d-%H%M%S-%f')
    bank = list(csv.DictReader((P / 'question-bank/QUESTION_BANK.csv').open()))
    codes = {s['code'] for s in read(P / 'syllabus/SYLLABUS_MASTER.json')}
    errors = []
    if len({r['question_id'] for r in bank}) != len(bank):
        errors.append('Duplicate master question IDs')
    for row in bank:
        try:
            record = read(P / row['record_path'])
            question = read(P / row['question_path'])
            answer = read(P / row['markscheme_path'])
            assert record['question_id'] == question['question_id'] == answer['question_id'] == row['question_id']
            assert record['question_text'] == question['question_text']
            assert record['solution'] == answer['solution']
            assert not {'solution', 'marking_points', 'test_code'} & question.keys()
            assert record['unofficial'] and answer['unofficial']
            assert set(record['syllabus_codes']) <= codes
            assert sum(p['marks'] for p in answer['marking_points']) == int(row['marks'])
        except (AssertionError, KeyError, TypeError, OSError) as exc:
            errors.append(row['question_id'] + ': ' + str(exc))
    agents = []
    checked = set()
    for role, folder in ROLES:
        directory = P / 'agents/chunk-3' / folder
        status = read(directory / 'STATUS.json', {'status': 'No saved status'})
        objectives = status.get('objectives_checked', status.get('checked_objective_ids', []))
        if folder != 'agent-3-bank-audit':
            checked.update(objectives)
        agents.append({'role': role, 'directory': str(directory.relative_to(P)), 'saved_status': status})
    initial = read(A / 'RECOVERY_INITIAL_MANIFEST.json')
    historical = [r for r in initial['files'] if r['path'].startswith('question-bank/')]
    changed = [r['path'] for r in historical if not (P / r['path']).exists() or digest(P / r['path']) != r['sha256']]
    # The bank index can grow after approved original-question merges; report it
    # separately instead of treating an authorized append as a historical edit.
    changed_records = [x for x in changed if x != 'question-bank/QUESTION_BANK.csv']
    saved_files = []
    for root in [P / 'agents/chunk-3', P / 'coverage', P / 'exams', P / 'question-bank', P / 'scripts']:
        for f in sorted(root.rglob('*')):
            if f.is_file() and not f.name.endswith(('.tmp', '.sqlite3', '.sqlite3-wal', '.sqlite3-shm', '.sqlite3-journal')) and '__pycache__' not in f.parts:
                saved_files.append({'path': str(f.relative_to(P)), 'bytes': f.stat().st_size, 'sha256': digest(f)})
    # A SQLite backup is transactionally consistent even if its owner imports a
    # new batch while checkpointing. Never hash a possibly changing live file.
    live_db = P / 'question-bank/database.sqlite3'
    if not live_db.exists():
        live_db = P / 'agents/chunk-3/agent-3-bank-audit/question_bank.sqlite3'
    database = None
    if live_db.exists():
        directory = A / 'database-snapshots'
        directory.mkdir(exist_ok=True)
        temporary_db = directory / (checkpoint + '.tmp')
        source = sqlite3.connect(f'file:{live_db}?mode=ro', uri=True)
        backup = sqlite3.connect(temporary_db)
        try:
            source.backup(backup)
            integrity = backup.execute('PRAGMA integrity_check').fetchone()[0]
            tables = {r[0] for r in backup.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            counts = {name: backup.execute('SELECT count(*) FROM ' + name).fetchone()[0]
                      for name in ['questions', 'answers', 'scope_evidence', 'verification', 'usage_history', 'selections'] if name in tables}
            verification = [list(r) for r in backup.execute('SELECT dimension,status,count(*) FROM verification GROUP BY dimension,status')] if 'verification' in tables else []
        finally:
            backup.close()
            source.close()
        backup_hash = digest(temporary_db)
        destination = directory / (backup_hash + '.sqlite3')
        if destination.exists():
            temporary_db.unlink()
        else:
            os.replace(temporary_db, destination)
        database = {'live_path': str(live_db.relative_to(P)), 'snapshot_path': str(destination.relative_to(P)),
                    'sha256': backup_hash, 'integrity_check': integrity, 'table_counts': counts,
                    'verification_counts': verification,
                    'limits': 'Database integrity/schema/import counts do not establish completeness of search features or content verification.'}
    state = {
        'checkpoint': checkpoint, 'saved_at': now.isoformat(), 'note': args.note,
        'baseline_commit': 'dd5285c', 'initial_recovery_commit': '523d2b5',
        'master_bank_records': len(bank), 'original_master_records': sum(r['derivation_status'] == 'original_unofficial' for r in bank),
        'specialist_objectives_checked': sorted(checked), 'total_syllabus_objectives': len(codes),
        'master_integrity_errors': errors, 'historical_record_changes_since_recovery': changed_records,
        'specialists': agents, 'saved_files': saved_files,
        'database_snapshot': database,
        'content_verification_limit': 'Integrity pass does not verify technical content. Author status is reported separately from coordinator approval.',
        'chunk3_complete': False,
    }
    atomic(A / 'checkpoints' / (checkpoint + '.json'), json.dumps(state, indent=2) + '\n')
    atomic(A / 'LATEST_CHECKPOINT.json', json.dumps(state, indent=2) + '\n')
    lines = [
        '# Progress — Chunk 3 active, recovery-first', '',
        f'**Checkpoint {checkpoint} — {now.strftime("%d %B %Y %H:%M:%S %Z")} (Europe/Zurich).**', '',
        args.note, '',
        'User authorized Chunk 3 only. Checkpoint after every 2–3 questions, each topic and meaningful milestone. **Do not enter Chunk 4.** Do not enter future chunks; user mentioned a future Chunk 5 but has not authorized it.', '',
        '## Preserved baseline and actual saved state', '',
        '- Initial recovery found Chunk 2 final only, no previous Chunk 3 artifacts or live specialists. Previous report: audits/chunk-3/PROGRESS_BEFORE_C3_RECOVERY.md.',
        '- 48 PDFs inventoried; 23 distinct historical exams processed, 0 remaining; 1,141 source parts; 838 mapped (383 A / 455 B); 303 exclusions; 15 reuse links.',
        f'- Master bank: {len(bank)} records, including {state["original_master_records"]} merged original questions. The 823 historical adapted IDs are preserved.',
        f'- Specialist first-pass objective audits saved: {len(checked)}/{len(codes)}. This is review progress, not complete coverage or coordinator approval.',
        f'- Current structural bank check: {len(errors)} errors. Historical record changes: {len(changed_records)} (must be explained/reviewed if nonzero).',
        '- Initial baseline integrity passed 2,473 file hashes and all 823 record schemas/identities/codes/mark totals. See audits/chunk-3/BASELINE_INTEGRITY.json.',
        '- Existing adapted marking criteria remain unofficial/preliminary; examination-level independent audit belongs to Chunk 4.', '',
        '## Persistent database snapshot', '',
        '```json', json.dumps(database, indent=2), '```', '',
        '## Three actual specialist assignments and saved handoffs', '',
    ]
    for agent in agents:
        status = agent['saved_status']
        lines += [f'### {agent["role"]}', '', f'Owned directory: `{agent["directory"]}/`. Latest saved status (author-reported, not assumed live after interruption):', '', '```json', json.dumps(status, indent=2), '```', '']
    lines += [
        '## Outstanding coordinator integration and completion gates', '',
        '- Read each saved STATUS.json and actual output before reassigning. Resume the next unfinished item without repeating checked objectives or changing stable IDs.',
        '- Independently sample scope/answer evidence in each specialist audit; merge only validated coverage rows. Full objective and important guidance coverage is not inferred from mapped counts.',
        '- Check every new question’s content, exact mapping, answer, marking criteria, alternatives and applicable execution evidence. Preserve author drafts separately. Coordinator alone writes master indexes and approved bank files.',
        '- Merge original questions in batches of 2–3; checkpoint before starting the next batch. Refresh searchable-bank datasets after approved merges and rerun feature tests.',
        '- Searchable bank must work and be tested. Assumed features pending any further user requirements: text search; syllabus/topic/theme/level/marks/difficulty filters; answer reveal; provenance references; student selection/export without answers.',
        '- Later user override: NO examinations, topic tests, PDFs or full assembly during Chunk 3. Read audits/chunk-3/USER_CHUNK3_SCOPE.md. Persistent database, exact scope evidence/search, all filters, verification dimensions and future usage/duplicate metadata are required.',
        '- All 823 adapted questions require individual mapping/bullet review; objective-level sampled evidence is only a first pass. Keep unreviewed records queued. Semantic candidates are not checked relevance. Search must report unsupported scope and verified versus unverified status honestly.',
        '- Known source cautions remain in QA_ISSUES.md. Review audits/chunk-3 for new findings and the coordinator integration ledger if present.', '',
        '## Recovery instructions', '',
        'Read AGENTS.md, PROGRESS.md, audits/chunk-3/USER_CHUNK3_SCOPE.md, QA_ISSUES.md, current bank/coverage and audits/chunk-3/LATEST_CHECKPOINT.json. Verify files against its hashes. Read each agent STATUS.json for more recent atomic saves. Reassign exactly three specialist roles; do not invent previous completions or rely on agents continuing after this run. Existing Chunk 2 generators must not be rerun over approved records.', '',
        'Run `python3 scripts/checkpoint_chunk3.py --note "concrete saved milestone and next action"` after each meaningful milestone. Only coordinator runs it. Git staging/commit follows a verified saved milestone; Git is supplementary to atomic files.', '',
        'Last verified Git milestones: C2 `dd5285c`; initial C3 recovery `523d2b5`. Additional saved Git milestones, if any: audits/chunk-3/GIT_CHECKPOINT.md.', '',
        '**Chunk 3 is incomplete. No automatic continuation or account-credit balance is claimed.**', '',
    ]
    atomic(P / 'PROGRESS.md', '\n'.join(lines))
    print(json.dumps({k: state[k] for k in ['checkpoint', 'master_bank_records', 'original_master_records', 'master_integrity_errors', 'historical_record_changes_since_recovery']}))
    print('Saved specialist objective audits:', len(checked), '/', len(codes))


if __name__ == '__main__':
    main()
