"""Read-only inventory of original PDFs; copies are byte-verified, originals unchanged."""
from pathlib import Path
import csv, hashlib, json, shutil
from pypdf import PdfReader

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
rows = []
for i, src in enumerate(sorted(ROOT.glob('*.pdf'), key=lambda p:p.name.casefold()), 1):
    kind = ('2027-guide' if 'First-Assessment-2027-guide' in src.name else
            '2027-specimen' if 'Specimen Papers 2027' in src.name else 'historical-papers')
    dst = PROJECT / 'sources' / kind / src.name
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    if not dst.exists(): shutil.copy2(src, dst)
    assert hashlib.sha256(dst.read_bytes()).hexdigest() == digest
    doc = PdfReader(src).pages
    cover = doc[0].extract_text()
    row = dict(source_id=f'SRC-{i:03}', filename=src.name, category=kind,
               original_path=str(src), project_path=str(dst.relative_to(PROJECT)),
               bytes=src.stat().st_size, sha256=digest, pages=len(doc),
               cover_text=' '.join(cover.split()), duplicate_of='',
               processing_status='inventoried_not_question_processed')
    for previous in rows:
        if previous['sha256']==digest:
            row['duplicate_of']=previous['source_id']; break
    rows.append(row)
    evidence = PROJECT/'sources'/'inventory-evidence'
    evidence.mkdir(exist_ok=True)
    (evidence/f'{row["source_id"]}-cover.txt').write_text(cover)
    if kind != 'historical-papers':
        textdir = PROJECT/'sources'/kind/'text'
        textdir.mkdir(exist_ok=True)
        for n,page in enumerate(doc,1):
            (textdir/f'page-{n:03}.txt').write_text((page.extract_text(extraction_mode="layout") if "/Contents" in page else ""))
        (textdir/'all-pages.txt').write_text('\n'.join(f'\n=== PDF PAGE {n} ===\n'+(p.extract_text(extraction_mode="layout") if "/Contents" in p else "") for n,p in enumerate(doc,1)))
with (PROJECT/'sources'/'SOURCE_INVENTORY.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)
(PROJECT/'sources'/'SOURCE_INVENTORY.json').write_text(json.dumps(rows,indent=2))
print(json.dumps({'pdf_files':len(rows),'unique_hashes':len(set(r['sha256'] for r in rows)),
                  'categories':{k:sum(r['category']==k for r in rows) for k in set(r['category'] for r in rows)},
                  'duplicates':[(r['source_id'],r['duplicate_of']) for r in rows if r['duplicate_of']]},indent=2))
for row in rows:
    if row['category']!='historical-papers':print(row['source_id'],row['filename'],row['pages'])
