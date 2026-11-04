"""Compare every available source leaf allocation to original right-margin marks."""
from pathlib import Path
import json,collections
P=Path(__file__).resolve().parents[1]
census=json.loads((P/'audits/chunk-2/INDEPENDENT_MARGIN_MARK_CENSUS.json').read_text())
reports=[]
for c in census:
 sid=c['source_id'];records=[]
 for f in (P/'agents/chunk-2').glob(f'*/batches/{sid}-*.json'):records+=json.loads(f.read_text())['source_questions']
 if not records:continue
 expected=collections.Counter((v['pdf_page'],v['marks']) for v in c['source_mark_parts'])
 actual=collections.Counter((s.get('mark_allocation_pdf_page',s['source_pdf_pages'][-1]),s['original_marks']) for s in records)
 missing=list((expected-actual).elements());extra=list((actual-expected).elements())
 audits=list((P/'agents/chunk-2').glob(f'*/papers/{sid}/paper_audit.json'))
 complete=bool(audits and json.loads(audits[0].read_text()).get('complete'))
 reports.append({'source_id':sid,'expected_parts':c['leaf_count'],'extracted_parts':len(records),'expected_marks':c['all_options_marks'],'actual_marks':sum(s['original_marks'] for s in records),'unmatched_source_positions':missing,'extra_record_positions':extra,'author_complete':complete,'pass':not missing and not extra})
(P/'audits/chunk-2/MARK_RECONCILIATION.json').write_text(json.dumps(reports,indent=2))
print(json.dumps({'papers_with_batches':len(reports),'complete_margin_matches':sum(r['pass'] for r in reports),'completed_paper_disagreements':[r for r in reports if r['author_complete'] and not r['pass']],'remaining_partial_or_disagreed':[r['source_id'] for r in reports if not r['pass']]},indent=2))
