from pathlib import Path
import json,collections,hashlib,re
from save_reviews import atomic
P=Path(__file__).resolve().parent
reviews=json.loads((P/'question_reviews.json').read_text())['reviews'];queue=json.loads((P/'question_review_queue.json').read_text());n=len(reviews);remaining=len(queue)-n
counts=collections.Counter(r['question_id'].split('-')[1] for r in reviews)
s=json.loads((P/'STATUS.json').read_text());s['source_record_review_progress']={code:{'reviewed':num,'remaining':sum(q['question_id'].split('-')[1]==code and q['status']=='queued_no_c3_individual_review' for q in queue),'note':'C3 mapping and stated verification dimensions only;original-PDF source verification pending.'} for code,num in counts.items()};s['files_created']=sorted(str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and '__pycache__' not in str(f) and not f.name.endswith('.tmp'));s['reviewed_question_type_count']=sum('question_type' in r for r in reviews);atomic(P/'STATUS.json',s)
f=P/'findings.md';text=f.read_text();text=re.sub(r'Checkpoint \*\*B-RECORD-\d+\*\*',f'Checkpoint **B-RECORD-{n:03d}**',text);text=re.sub(r'\*\*\d+ individual reviews saved,\d+ queued\*\*',f'**{n} individual reviews saved,{remaining} queued**',text);text+='\n\nCheckpoint '+s['checkpoint']+':'+str(dict(counts))+'. Next:'+s['next_queued_question_id']+'.'+str(s['reviewed_question_type_count'])+'explicit manually reviewed question types;earlier type metadata remains pending.\n';f.write_text(text)
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in str(f) and f.name!='B_CHECKPOINT_MANIFEST.json' and not f.name.endswith('.tmp')]
atomic(P/'B_CHECKPOINT_MANIFEST.json',{'checkpoint':s['checkpoint'],'reviews':n,'remaining':remaining,'files':[{'path':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(files)]})
print('Durable source milestone',s['checkpoint'],dict(counts),'next',s['next_queued_question_id'])
