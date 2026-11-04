"""Inventory-level identity/availability checks only; no historical question processing."""
from pathlib import Path
import csv,json,re
from pypdf import PdfReader
P=Path(__file__).resolve().parents[1]
rows=json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())
# Source-paper identities checked from first two PDF pages, scan covers and paired MS.
identities={
 1:('2026','May','HL','1','A/B/C','2226-4428'),
 2:('2026','May','HL','2','A/B/C','2226-4429'),
 4:('2023','November','HL','1','not stated','8823-7011'),
 5:('2022','November','HL','1','TZ0','8822-7011'),
 6:('2021','November','HL','1','TZ0','8821-7011'),
 7:('2021','May','HL','1','TZ0','2221-7011'),
 8:('2019','November','HL','1','TZ0','8819-7011'),
 9:('2024','November','HL','1','not stated','8824-6904'),
 16:('2023','November','SL','1','not stated','8823-7014'),
 18:('2023','May','HL','1','TZ1','2223-9240'),
 20:('2023','May','HL','1','TZ2','2223-7011'),
 22:('2025','November','HL','1','not stated','8825-6404'),
 24:('2025','November','SL','1','not stated','8825-6407'),
 26:('2025','May','HL','1','TZ2 (filename; numerical cover code)','2225-6414'),
 28:('2025','May','SL','1','TZ1/2 (markscheme)','2225-6417'),
 30:('2025','May','HL','1','TZ3 (filename; numerical cover code)','2225-6419'),
 32:('2023','May','HL','2','TZ0 (markscheme)','2223-7012'),
 33:('2020','November','HL','2','TZ0','8820-7012'),
 34:('2023','November','HL','2','not stated','8823-7012'),
 38:('2025','November','HL','2','not stated','8825-6405'),
 40:('2025','November','SL','2','not stated','8825-6408'),
 42:('2025','May','HL','2','TZ3 (filename; numerical cover code)','2225-6420'),
 44:('2025','May','SL','2','TZ3 (filename; numerical cover code)','2225-6423'),
 45:('2025','May','SL','2','TZ3 (filename; numerical cover code)','2225-6423'),
 47:('2022','November','HL','1','not stated on scan cover','8822-7011'),
}
pairs={4:10,5:11,6:12,7:13,8:14,9:15,16:17,18:19,20:21,
       22:23,24:25,26:27,28:29,30:31,32:35,33:36,34:37,38:39,
       40:41,42:43,44:46,45:46,47:11}
for q,m in pairs.items():identities[m]=identities[q]
for r in rows:
 n=int(r['source_id'][4:]); doc=PdfReader(P/r['project_path'])
 r.update(document_type=('guide' if r['category']=='2027-guide' else 'specimen_compilation' if r['category']=='2027-specimen' else 'markscheme' if 'markscheme' in r['filename'].lower() else 'question_paper'),
          year='',session='',level='',paper='',zone='',exam_code='',
          identity_basis='',paired_source_ids='',textless_pdf_pages='',readability_status='',inventory_notes='')
 if n in identities:
  r.update(dict(zip(['year','session','level','paper','zone','exam_code'],identities[n])))
  r['identity_basis']='PDF cover/first two pages; paired markscheme corroboration where available'
  if n in [1,2,47]:r['identity_basis']='Rendered scan cover visually inspected by coordinator'
  r['paired_source_ids']=';'.join(f'SRC-{v:03}' for v in ([pairs[n]] if n in pairs else [q for q,m in pairs.items() if m==n]))
 textless=[]
 for i,page in enumerate(doc.pages,1):
  if len((page.extract_text() or '').strip())<20:textless.append(i)
 r['textless_pdf_pages']=';'.join(map(str,textless))
 r['readability_status']='scanned_requires_visual_or_OCR' if len(textless)==len(doc.pages) else 'text_available; blanks/visuals_need_page_review' if textless else 'text_available'
 if n in [1,2]:r['inventory_notes']='No matching uploaded markscheme identified. Scanned image-only PDF.'
 if n==47:r['inventory_notes']='Scan has 8 PDF pages; cover declares 9 pages. Same exam code as SRC-005; do not process twice. Exact omitted page not established in Chunk 1.'
 if n==45:r['inventory_notes']='Byte-identical duplicate of SRC-044; retain original but process once.'
 if n==5:r['inventory_notes']='Text-readable version of same examination as image-only SRC-047; compare completeness before Chunk 2 processing.'
 if n in [4,9,16,34]:r['inventory_notes']='Session/year corroborated by matching printed numeric code in uploaded markscheme; do not use copyright year alone.'
 if n==48:r['inventory_notes']='Includes HL/SL papers and markschemes, both language alternatives, and specimen case study; see component manifest.'
with (P/'sources/SOURCE_INVENTORY.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'sources/SOURCE_INVENTORY.json').write_text(json.dumps(rows,indent=2))
print(json.dumps({'historical_files':sum(r['category']=='historical-papers' for r in rows),
 'historical_question_files':sum(r['document_type']=='question_paper' for r in rows),
 'historical_markscheme_files':sum(r['document_type']=='markscheme' for r in rows),
 'distinct_historical_exam_codes':len(set(r['exam_code'] for r in rows if r['document_type']=='question_paper')),
 'textless_files':[r['source_id'] for r in rows if r['readability_status']=='scanned_requires_visual_or_OCR']},indent=2))
