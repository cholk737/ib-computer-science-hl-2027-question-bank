"""Compare saved records against a second PDF text extractor and expected code ranges."""
from pathlib import Path
import json, re
import pdfplumber

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
GUIDE=PROJECT/'sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf'
records=json.loads((OUT/'theme_b_scope.json').read_text())
def norm(t):
    return re.sub(r'\s+','',t).replace('ﬁ','fi').replace('ﬂ','fl')
results=[]
with pdfplumber.open(GUIDE) as doc:
    pages={n:doc.pages[n-1].extract_text() for n in range(44,49)}
    for r in records:
        evidence=norm(''.join(pages[n] for n in r['source_pdf_pages']))
        statement_ok=norm(r['code']+' '+r['statement']) in evidence
        bullets_ok=[norm(b) in evidence for b in r['guidance_bullets']]
        results.append({'code':r['code'],'statement_match':statement_ok,'guidance_bullet_matches':bullets_ok})
assert all(r['statement_match'] and all(r['guidance_bullet_matches']) for r in results),results
(OUT/'second_extractor_verification.json').write_text(json.dumps({'method':'pdfplumber independent text extraction; whitespace/ligature-normalized exact statement and each bullet containment on cited source pages','results':results,'passed':True},indent=2)+'\n')
print(f"Passed: {len(results)} statements and {sum(len(r['guidance_bullet_matches']) for r in results)} bullets.")
