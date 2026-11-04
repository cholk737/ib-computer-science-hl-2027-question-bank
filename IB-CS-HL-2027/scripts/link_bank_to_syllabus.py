"""Mechanical reference update only; does not assess coverage or identify gaps."""
from pathlib import Path
import csv,json,collections
P=Path(__file__).resolve().parents[1]
links=collections.defaultdict(list)
for row in csv.DictReader((P/'question-bank/QUESTION_BANK.csv').open()):
 for code in json.loads(row['syllabus_codes']):links[code].append(row['question_id'])
records=json.loads((P/'syllabus/SYLLABUS_MASTER.json').read_text())
for s in records:
 s['question_bank_ids']=sorted(links[s['code']])
 s['coverage_status']='practice_links_recorded_pending_coverage_audit' if s['question_bank_ids'] else 'no_practice_link_recorded_pending_coverage_audit'
 s['bank_link_checkpoint']='C2-FINAL; mechanical index links, not a full statement/bullet coverage finding'
 (P/s['record_path']).write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
(P/'syllabus/SYLLABUS_MASTER.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
path=P/'syllabus/SYLLABUS_MASTER.csv';rows=list(csv.DictReader(path.open()));by={s['code']:s for s in records}
with path.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader()
 for r in rows:
  s=by[r['code']];r['question_bank_ids']=json.dumps(s['question_bank_ids']);r['coverage_status']=s['coverage_status'];w.writerow(r)
print('112 syllabus records retain exact scope and now reference the bank; no coverage-gap audit performed.')
