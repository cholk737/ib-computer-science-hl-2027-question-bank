from pathlib import Path
import json,re,collections
import pdfplumber
O=Path(__file__).resolve().parent;P=O.parents[2]
inv={r['source_id']:r for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())}
for sid in ['SRC-005','SRC-008','SRC-018','SRC-024','SRC-030','SRC-034','SRC-042']:
 paths=sorted((O/'batches').glob(sid+'-b*.json'))
 if not paths:continue
 batches=[json.loads(p.read_text()) for p in paths];records=[r for b in batches for r in b['source_questions']]
 records.sort(key=lambda r:(int(r['question']),r['subquestion']))
 segments=[];buffer=[];fullpages={};allmarks=[]
 with pdfplumber.open(P/inv[sid]['project_path']) as doc:
  for n in range(3,len(doc.pages)+1):
   page=doc.pages[n-1];fullpages[n]=page.extract_text(layout=False)
   words=page.extract_words(extra_attrs=['fontname'])
   marks=[w for w in words if re.fullmatch(r'\[\d+\]',w['text']) and w['x0']>=page.width*.89 and not any(s in w['fontname'].lower() for s in ['courier','mono'])]
   marks.sort(key=lambda w:w['top'])
   start=55
   for w in marks:
    end=w['bottom']+1
    text=page.crop((0,start,page.width,end)).extract_text() if end>start else ''
    buffer.append(dict(pdf_page=n,text=text or ''))
    segments.append(dict(marks=int(w['text'][1:-1]),parts=buffer));buffer=[];start=end
   if start<page.height-50:
    text=page.crop((0,start,page.width,page.height-50)).extract_text() or ''
    if text.strip():buffer.append(dict(pdf_page=n,text=text))
 auditpath=O/'papers'/sid/'paper_audit.json'
 complete=json.loads(auditpath.read_text()).get('complete',False)
 if complete:assert len(segments)==len(records),(sid,len(segments),len(records))
 else:segments=segments[:len(records)]
 assert [s['marks'] for s in segments]==[r['original_marks'] for r in records],sid
 for r,s in zip(records,segments):
  r.setdefault('original_text_manual_synopsis',r['original_text'])
  r['original_text']='\n\n'.join(f'[Source PDF page {p["pdf_page"]}]\n'+p['text'] for p in s['parts'])
  r['transcription_status']='Verbatim PDF text for leaf interval, including any shared context since preceding marked leaf; visual figures retained separately. Header/footer text may remain; no source wording replaced by synopsis.'
  r['source_page_evidence']=[dict(pdf_page=n,text_path=f'agents/chunk-2/agent-1-papers-a/source-pages/{sid}/page-{n:03}.txt') for n in r['source_pdf_pages']]
 (O/'source-pages'/sid).mkdir(parents=True,exist_ok=True)
 for n,text in fullpages.items():(O/'source-pages'/sid/f'page-{n:03}.txt').write_text(text)
 for path,b in zip(paths,batches):path.write_text(json.dumps(b,ensure_ascii=False,indent=2))
 print(sid,'exact marked leaf intervals',len(segments),'all marks match')
