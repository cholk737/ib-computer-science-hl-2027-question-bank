"""Reproducible Theme A statement extraction; no master files are modified."""
from pathlib import Path
import collections,csv,hashlib,json,re
import pdfplumber

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
PDF=PROJECT/'sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf'
SCOPE_NOTE='The content of each topic below is sometimes clarified by the terms “may include” and “must include”: —“ May include” means that the list includes examples that could be assessed, although other examples may also be used by the IB in assessment. — “ Must include” means that the list includes all the examples that will be used in assessment.'
TOPICS={'A1':'Computer fundamentals','A2':'Networks','A3':'Databases','A4':'Machine learning'}
records=[]
current=None
subtopic=''
subtopic_code=''
subtopic_hl=False
accept=False
with pdfplumber.open(PDF) as doc:
    for n in range(34,44):
        text=doc.pages[n-1].extract_text()
        (OUT/f'evidence-page-{n:03}.txt').write_text(text)
        for raw in text.splitlines():
            line=raw.strip()
            if line in ['Syllabus','Syllabus content'] or re.match(r'^(?:\d+ Computer science guide|Computer science guide \d+)$',line): continue
            m=re.match(r'^(A\d\.\d) (.+)$',line)
            if m:
                subtopic_code,subtopic=m.groups()
                subtopic_hl='(HL only)' in subtopic
                accept=False
                continue
            m=re.match(r'^(A\.?\d\.\d\.\d+) (.+)$',line)
            if m:
                src,statement=m.groups()
                code=src.replace('A.','A')
                current={'code':code,'source_code':src,'theme':'A','topic':f'{code[:2]} {TOPICS[code[:2]]}',
                         'subtopic':f'{subtopic_code} {subtopic}','statement_lines':[statement],
                         'guidance_lines':[],'line_evidence':[{'pdf_page':n,'text':line}],
                         'source_pdf_pages':[n],'hl_from_subtopic':subtopic_hl}
                records.append(current);accept=True
                continue
            if line=='Linking questions' or re.match(r'^A\d [A-Z]',line) or line.startswith('Theme B:'):
                accept=False
            if not accept or current is None: continue
            current['line_evidence'].append({'pdf_page':n,'text':line})
            if n not in current['source_pdf_pages']: current['source_pdf_pages'].append(n)
            if not current['guidance_lines'] and not line.startswith('•'):
                current['statement_lines'].append(line)
            else:
                current['guidance_lines'].append(line)

def paragraphs(lines):
    result=[]
    for l in lines:
        if l.startswith('•') or l.startswith('Note:') or l.startswith('For example,'):
            result.append(l)
        elif result:result[-1]+=('' if result[-1].endswith(('-', '/')) else ' ')+l
        else:result.append(l)
    return result

for r in records:
    full=' '.join(r.pop('statement_lines'))
    r['statement_with_level_tag']=full
    r['statement']=full.replace(' (HL only)','').replace('(HL only)','').strip()
    r['level']='HL-only' if r['hl_from_subtopic'] or '(HL only)' in full else 'SL/HL common'
    r['level_basis']='subtopic heading' if r['hl_from_subtopic'] else ('individual statement label' if '(HL only)' in full else 'no HL-only designation')
    r['guidance_paragraphs']=paragraphs(r.pop('guidance_lines'))
    r['guidance']='\n'.join(r['guidance_paragraphs'])
    r['source_printed_pages']=[x-6 for x in r['source_pdf_pages']]
    r['source_file']=str(PDF.relative_to(PROJECT))
    r['source_sha256']=hashlib.sha256(PDF.read_bytes()).hexdigest()
    r['must_include_guidance']=[p for p in r['guidance_paragraphs'] if 'must include' in p.lower()]
    r['may_include_guidance']=[p for p in r['guidance_paragraphs'] if 'may include' in p.lower()]
    r['explicit_scope_limits']=[p for p in r['guidance_paragraphs'] if any(s in p.lower() for s in ['not required','beyond the scope','note:','for example'])]
    r['scope_qualifications']='\n'.join(r['must_include_guidance']+r['may_include_guidance']+r['explicit_scope_limits'])
    r['global_scope_note']=SCOPE_NOTE
    r['assessable_knowledge_skills']=r['statement']+'\nScope is restricted/qualified by the complete accompanying guidance; no extra technical requirement is inferred.'
    contexts=[p for p in r['guidance_paragraphs'] if any(w in p.lower() for w in ['real-world','scenario','applications','for example'])]
    r['allowed_context']='\n'.join(contexts) if contexts else 'No additional context restriction is stated in this learning statement; use the statement and full guidance.'
    r['coverage_status']='not_yet_assessed_chunk1'
    r['verification_status']='source_text_checked; visual_page_review_completed'
    r['record_path']='agents/chunk-1/agent-1-theme-a/records/'+r['code']+'.json'
    r['uncertainty_flags']=[]
    if r['code']!=r['source_code']:r['uncertainty_flags'].append('Source prints A.1.2.5; canonical A1.2.5 is an explicitly disclosed indexing normalization, not a different learning statement.')
    if r['code']=='A3.3.4':r['uncertainty_flags'].append('Guide lists AVERAGE as an SQL aggregate command. Preserve exact source wording; SQL dialect-specific implementation must be verified later (do not silently treat AVERAGE as standard SQL syntax).')
    if r['code']=='A4.3.1':r['uncertainty_flags'].append('Plain-text extraction flattens the superscript in r² as r2; source PDF visibly shows r squared.')
    (OUT/'records').mkdir(exist_ok=True)
    (PROJECT/r['record_path']).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

expected={f'A1.1.{i}' for i in range(1,10)}|{f'A1.2.{i}' for i in range(1,6)}|{f'A1.3.{i}' for i in range(1,8)}|{'A1.4.1'}
expected|={f'A2.1.{i}' for i in range(1,6)}|{f'A2.{s}.{i}' for s in [2,3,4] for i in range(1,5)}
expected|={'A3.1.1'}|{f'A3.2.{i}' for i in range(1,8)}|{f'A3.3.{i}' for i in range(1,7)}|{f'A3.4.{i}' for i in range(1,5)}
expected|={f'A4.1.{i}' for i in [1,2]}|{f'A4.2.{i}' for i in [1,2,3]}|{f'A4.3.{i}' for i in range(1,11)}|{f'A4.4.{i}' for i in [1,2]}
assert {r['code'] for r in records}==expected
assert len(records)==len(expected)==74
assert all(r['guidance_paragraphs'] for r in records)
assert collections.Counter(r['level'] for r in records)=={'SL/HL common':43,'HL-only':31}
(OUT/'theme_a_scope.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
fields=['code','source_code','theme','topic','subtopic','statement','level','source_pdf_pages','source_printed_pages','guidance','scope_qualifications','assessable_knowledge_skills','allowed_context','coverage_status','verification_status','record_path','level_basis','uncertainty_flags']
with (OUT/'theme_a_scope.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in records:w.writerow({k:json.dumps(r[k],ensure_ascii=False) if isinstance(r[k],list) else r[k] for k in fields})
counts={t:dict(collections.Counter(r['level'] for r in records if r['code'].startswith(t))) for t in TOPICS}
for topic in TOPICS:
    subset=[r for r in records if r['code'].startswith(topic)]
    (OUT/f'checkpoint-{topic}.json').write_text(json.dumps({'checkpoint':f'C1-{topic}-verified','date':'2026-11-04','statement_count':len(subset),'counts':counts[topic],'first_code':subset[0]['code'],'last_code':subset[-1]['code'],'all_guidance_present':all(r['guidance_paragraphs'] for r in subset)},indent=2)+'\n')
(OUT/'checkpoint.json').write_text(json.dumps({'checkpoint':'C1-A-complete','date':'2026-11-04','counts':counts,'total':len(records),'source_pdf_pages':[34,43],'source_printed_pages':[28,37]},indent=2)+'\n')
print(json.dumps(counts,indent=2))
