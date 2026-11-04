"""Coordinator independent source reconstruction, before authoritative merge.

Uses pypdf layout extraction directly from the original guide. It compares all
statement and guidance characters (ignoring layout whitespace/HL metadata) and
independently computes HL inheritance. No specialist outputs are modified.
"""
from pathlib import Path
import re,json,collections,unicodedata
from pypdf import PdfReader
P=Path(__file__).resolve().parents[1]
guide=P/'sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf'
records=json.loads((P/'agents/chunk-1/agent-1-theme-a/theme_a_scope.json').read_text())+json.loads((P/'agents/chunk-1/agent-2-theme-b/theme_b_scope.json').read_text())
source={};active=None;topic_hl=False;subtopic_hl=False
for n,page in enumerate(PdfReader(guide).pages,1):
 if not 34<=n<=49:continue
 for line in page.extract_text(extraction_mode='layout').splitlines():
  line=line.strip()
  if not line or line in ['Syllabus','Syllabus content'] or re.match(r'^(?:\d+\s+Computer science guide|Computer science guide\s+\d+)$',line):continue
  m=re.match(r'^([AB]\.?\d\.\d\.\d+)\s+(.+)',line)
  if m:
   code=m[1].replace('A.','A');active=code
   source[code]={'source_code':m[1],'text':[m[2]],'pages':[n],
                 'inherited_hl':topic_hl or subtopic_hl}
   continue
  if re.match(r'^[AB]\d\s+[A-Z]',line):
   topic_hl='(HL only)' in line;subtopic_hl=False;active=None;continue
  if re.match(r'^[AB]\d\.\d\s+[A-Z]',line):
   subtopic_hl='(HL only)' in line;active=None;continue
  if line=='Linking questions' or line.startswith('Theme '):active=None;continue
  if active:
   source[active]['text'].append(line)
   if n not in source[active]['pages']:source[active]['pages'].append(n)

def normalized(s):
 s=unicodedata.normalize('NFKC',s)
 return re.sub(r'\s+','',s).replace('(HLonly)','')
results=[]
for r in records:
 s=source[r['code']]
 official=' '.join(s['text'])
 transcribed=r.get('statement_with_level_tag',r['statement'])+' '+r['guidance']
 level='HL-only' if s['inherited_hl'] or '(HL only)' in official else 'SL/HL common'
 check={'code':r['code'],'full_statement_and_guidance_match':normalized(official)==normalized(transcribed),
        'source_code_match':r.get('source_code',r['code'])==s['source_code'],
        'page_set_match':r['source_pdf_pages']==s['pages'],
        'independent_level_match':r['level']==level,
        'source_pdf_pages':s['pages'],'level':level}
 if not check['full_statement_and_guidance_match']:
  check['source_text']=official;check['specialist_text']=transcribed
 results.append(check)
assert set(source)=={r['code'] for r in records},'code-set disagreement'
summary={'date':'2026-11-04','method':'Coordinator pypdf source reconstruction; full character comparison with layout whitespace and Unicode compatibility normalization; independent inherited-HL classification',
 'source_codes':len(source),'master_input_records':len(records),
 'counts':dict(collections.Counter(r['level'] for r in records)),
 'checks':results,'all_pass':all(all(v for k,v in x.items() if k.endswith('_match')) for x in results)}
(P/'audits/SYLLABUS_INTEGRATION_CHECK.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2))
for r in results:
 if not all(v for k,v in r.items() if k.endswith('_match')):print(json.dumps(r,ensure_ascii=False,indent=2))
assert summary['all_pass'],'Inspect evidence discrepancies before merging.'
