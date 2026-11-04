"""Independent pypdf extraction check of the pdfplumber-derived records."""
from pathlib import Path
from pypdf import PdfReader
import collections,json,re
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
PDF=PROJECT/'sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf'
records=json.loads((OUT/'theme_a_scope.json').read_text())
reader=PdfReader(PDF)
normalize=lambda text:re.sub(r'\s+','',text)
pages={n:normalize(reader.pages[n-1].extract_text()) for n in range(34,44)}
line_failures=[]
for r in records:
    for evidence in r['line_evidence']:
        if normalize(evidence['text']) not in pages[evidence['pdf_page']]:
            line_failures.append({'code':r['code'],**evidence})
assert not line_failures,line_failures
text='\n'.join(reader.pages[n-1].extract_text() for n in range(34,44))
independent_codes=re.findall(r'(?m)^(A\.?[1-4]\.\d\.\d+)\s',text)
independent_codes=[c.replace('A.','A') for c in independent_codes]
assert len(independent_codes)==74
assert set(independent_codes)=={r['code'] for r in records}
assert len(set(independent_codes))==74
continuations={r['code']:r['source_pdf_pages'] for r in records if len(r['source_pdf_pages'])>1}
assert set(continuations)=={'A2.3.1','A3.2.6','A3.4.3','A4.2.1','A4.3.7'}
result={'date':'2026-11-04','statement_count':len(records),'independent_code_count':len(independent_codes),
        'all_record_evidence_lines_found_in_independent_pypdf_extraction':True,
        'evidence_line_count':sum(len(r['line_evidence']) for r in records),
        'guidance_bullets':sum(p.startswith('•') for r in records for p in r['guidance_paragraphs']),
        'guidance_nonbullet_paragraphs':sum(not p.startswith('•') for r in records for p in r['guidance_paragraphs']),
        'cross_page_continuations':continuations,'unique_codes':len(set(independent_codes)),
        'level_counts':dict(collections.Counter(r['level'] for r in records)),
        'visual_review':'All PDF pages34–43 rendered and inspected individually; source code punctuation, HL labels, continuations, SQL aggregate spelling, r-squared superscript and PCA/LDA exclusion inspected.'}
(OUT/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
