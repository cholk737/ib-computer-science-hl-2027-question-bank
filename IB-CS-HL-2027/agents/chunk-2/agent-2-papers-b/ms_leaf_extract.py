from pathlib import Path
import re
HDR=re.compile(r'(?m)^\s*(\d{1,2})\.\s*(?=\([a-z]+\)|Award)')
# Part letters stop before i,which is a roman subpart in these papers.
PART=re.compile(r'(?m)^\s*\(([abcdefghjklmnopqrstuvwxyz])\)')
ROMAN=re.compile(r'(?m)^\s*\((i|ii|iii|iv|v|vi)\)')
def leaf_evidence(text,question,subquestion):
 headers=list(HDR.finditer(text));matches=[(i,m) for i,m in enumerate(headers) if int(m[1])==question]
 if len(matches)!=1:raise ValueError(('question',question,len(matches)))
 i,m=matches[0];end=headers[i+1].start() if i+1<len(headers) else len(text)
 body=text[m.end():end]
 parts=subquestion.split('-') if subquestion else []
 if parts:
  labels=list(PART.finditer(body));want=parts[0];hits=[(i,m) for i,m in enumerate(labels) if m[1]==want]
  if len(hits)!=1:raise ValueError(('part',question,subquestion,[m[1] for m in labels]))
  i,m=hits[0];body=body[m.end():labels[i+1].start() if i+1<len(labels) else len(body)]
 if len(parts)>1:
  labels=list(ROMAN.finditer(body));hits=[(i,m) for i,m in enumerate(labels) if m[1]==parts[1]]
  if len(hits)!=1:raise ValueError(('roman',question,subquestion,[m[1] for m in labels]))
  i,m=hits[0];body=body[m.end():labels[i+1].start() if i+1<len(labels) else len(body)]
 body=re.sub(r'(?m)^=== PDF PAGE \d+ ===\n','',body)
 body=re.sub(r'(?m)^– \d+ –.*$','',body)
 return body.strip()
if __name__=='__main__':
 from build_shard import *
 fails=[];out=[]
 for sid in ['SRC-006','SRC-009','SRC-020','SRC-026','SRC-032','SRC-038','SRC-044']:
  msid=INV[sid]['paired_source_ids'].split(';')[0];txt=(O/'evidence'/msid/'all.txt').read_text()
  for x in extract(sid):
   try:
    evidence=leaf_evidence(txt,x['question'],x['subquestion']);out.append({'id':sid+'-'+x['key'],'excerpt':evidence})
   except Exception as e:fails.append([sid,x['key'],repr(e)])
 print('extracted',len(out),'failed',fails)
 (O/'ms_leaf_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
