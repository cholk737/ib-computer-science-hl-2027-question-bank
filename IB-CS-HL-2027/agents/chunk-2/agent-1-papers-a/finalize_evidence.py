"""Final, repeatable shard-local evidence and editorial corrections.

Run after extraction/enrichment/polish. Never segments executable text.
"""
from pathlib import Path
import collections
import json
import re

O = Path(__file__).resolve().parent
P = O.parents[2]
INV = {r['source_id']: r for r in json.loads((P/'sources/SOURCE_INVENTORY.json').read_text())}

issues = {
 'H-SRC005-Q14-b': ['SRC-011 PDF p15: the suggested square-root bound is invalid for the shown simple proper-divisor accumulator without adding paired factors. The unofficial solution traverses all candidates below n and is tested.'],
 'H-SRC008-Q12-b': ['SRC-014 PDF p14: the static-stack full condition TOP > N-1 is inconsistent with TOP as the occupied last index. The adapted stack uses the correct capacity boundary.'],
 'H-SRC018-Q07': ['SRC-019 contains a misleading claim that a CPU cannot read ROM; this claim is not copied into unofficial criteria.'],
 'H-SRC024-Q13-c': ['SRC-025 PDF p15: Example 1 uses if/else-if extrema updates with sentinels and can miss the minimum in an increasing sequence; independent comparisons are required for that initialization. Integer DIV also gives the wrong fractional mean. The unofficial answer uses safe initialization, independent updates and true division.'],
 'H-SRC034-Q01-e': ['SRC-037 SQL example has inconsistent OrdDate/OrderDate naming and uses ORDER as a table name. The unofficial SQL uses a new consistent Buyer/Invoice schema and is executed in SQLite.'],
 'H-SRC034-Q17-c': ['SRC-037 PDF p34: the recommendation sample incorrectly requires both effectiveness and health to increase. It can reject a higher primary score with lower health and mishandle equal primary scores. The unofficial answer implements lexicographic priority and is tested with these counterexamples.'],
 'H-SRC034-Q18-b': ['SRC-037 PDF p35: backward traversal is not directly supported by the stated singly linked list. The unofficial algorithm counts the nodes, skips length-n nodes and traverses forward without modifying the log.'],
 'H-SRC042-Q01-b': ['SRC-042 PDF p3 narrative allows staff in several departments while STAFF stores only one DepartmentID. SRC-043 PDF p4 accepts contradictory cardinalities. The practice explicitly specifies one home department; the original contradiction is preserved as source evidence.'],
 'H-SRC042-Q01-d': ['SRC-043 query example inconsistently refers to ROLE/Roles. The unofficial query has consistent schema identifiers and is executed in SQLite.'],
 'H-SRC042-Q03-a-ii': ['SRC-043 PDF p9 year-only age subtraction ignores whether the birthday has occurred this year. The unofficial algorithm compares month/day and adjusts the completed-year count.'],
 'H-SRC042-Q05-f': ['SRC-043 PDF p14 uses a cross-midnight condition TIME >= 19:00 AND TIME < 07:00, which is impossible, and inconsistent NIGHT_TOTAL/TOTAL_NIGHT names. The adapted hour-based answer uses OR and counts the included observations before division; boundary, negative and constant-value cases are tested.'],
 'H-SRC042-Q08-d': ['The source markscheme characterization of unsupervised learning as more random/deeper is not a sound distinction. The unofficial criteria distinguish target-labelled training from unlabelled pattern discovery.'],
 'H-SRC042-Q14-f': ['SRC-043 UML example adds a toString method absent from the given source class. The unofficial task specifies every attribute/method required and does not import the added method.'],
 'H-SRC042-Q16-d': ['SRC-043 PDF p34 fixed 2^16 characterization does not correctly describe the full Unicode code-point repertoire. The practice states the general cross-script representation benefit without this claim.'],
 'H-SRC042-Q17-b': ['SRC-042 PDF pp23-24 describes an alphabetically ordered list but Figure 10 shows Matthew, Jon, Angelica, Maria, which is not alphabetical. The Customer constructor also contains an invalid int maximumBudget() parameter. The adapted list is explicitly assumed sorted and all programming uses valid Python.'],
}

fixes = {
 'cardinal i ties': 'cardinalities', 'unitprice': 'unit price',
 '1 NF': '1NF', '2 NF': '2NF', '3 NF': '3NF',
 'as anew ': 'as a new ', 'co ordinated': 'coordinated',
 'multi layer': 'multilayer', 'mislabel led': 'mislabelled',
 'toother': 'to other', 'en co dings': 'encodings',
 'long linkedlist': 'long linked list', 'non branching': 'nonbranching',
 'and"North"': 'and "North"', 'and_products': 'and _products',
 'andtotal_fee': 'and total_fee', 'market place': 'marketplace',
 ' i ff ': ' if and only if ',
}
prose_keys = {'question_text','solution','adaptation_rationale','criterion',
              'acceptable_alternatives','partial_credit_notes','common_errors'}

def edit(value, key=''):
    if isinstance(value, dict):
        return {k: edit(v,k) for k,v in value.items()}
    if isinstance(value, list):
        return [edit(v,key) for v in value]
    if isinstance(value, str) and key in prose_keys:
        # No identifier/token segmentation. These exact editorial replacements
        # target known natural-language defects only.
        for old,new in fixes.items():
            value = value.replace(old,new)
    return value

for sid in ['SRC-001','SRC-005','SRC-008','SRC-018','SRC-024','SRC-030','SRC-034','SRC-042']:
    paths = sorted((O/'batches').glob(sid+'-b*.json'))
    batches = [json.loads(p.read_text()) for p in paths]
    sources = [r for b in batches for r in b['source_questions']]
    pages_by_question = collections.defaultdict(set)
    for r in sources:
        pages_by_question[r['question']].update(r['source_pdf_pages'])
        pages_by_question[r['question']].update(int(n) for n in re.findall(r'\[Source PDF page (\d+)\]',r['original_text']))
    # These are the actual scenario/class-definition pages preceding the first
    # marked leaf; no guessed text is inserted into source transcription.
    if sid in ['SRC-034','SRC-042']:
        pages_by_question['14'].add(19)
    for r in sources:
        qpages = sorted(pages_by_question[r['question']])
        context_evidence = []
        for n in qpages:
            if sid == 'SRC-001':
                image = O/'papers'/sid/f'page-{n}.png'
            else:
                candidates = sorted((O/'papers').glob(f'{sid}-page-*.png'))
                image = next(p for p in candidates if int(p.stem.rsplit('-',1)[1]) == n)
            evidence = dict(pdf_page=n,image_path=str(image.relative_to(P)),kind='complete_original_page_raster')
            text = O/'source-pages'/sid/f'page-{n:03}.txt'
            if text.exists(): evidence['text_path'] = str(text.relative_to(P))
            context_evidence.append(evidence)
        r['source_context_page_evidence'] = context_evidence
        r['parent_context_status'] = 'Manual synopsis; complete exact original shared context, tables and code are linked in source_context_page_evidence and the unchanged source PDF.'
        r['complete_original_document_path'] = INV[sid]['project_path']
        existing = {a.get('path') for a in r['assets']}
        for e in context_evidence:
            if e['image_path'] not in existing:
                r['assets'].append(dict(kind='source_page',path=e['image_path'],source_pdf_page=e['pdf_page'],description='Complete original question/context page; preserves diagrams, code, tables and exact typography.'))
        specific = issues.get(r['source_question_id'],[])
        generated = {s for v in issues.values() for s in v}
        r['source_issues'] = list(dict.fromkeys([s for s in r.get('source_issues',[]) if s not in generated]+specific))
        r['markscheme']['source_issues'] = list(dict.fromkeys([s for s in r['markscheme'].get('source_issues',[]) if s not in generated]+specific))
    for b in batches:
        b['practice_questions'] = edit(b['practice_questions'])
        for q in b['practice_questions']:
            if q['question_id'] == 'P-SRC042-Q10-f':
                q['command_term'] = 'State'
                q['question_text'] = q['question_text'].replace('For check_upload below, state its returned value for each call:', 'State the returned value of check_upload below for each call: ')
            if q['question_id'] == 'P-SRC042-Q04-a':
                q['question_text'] = 'Identify two alternative database approaches explicitly included in the 2027 guide.'
                q['marking_points'] = [dict(marks=1,criterion='Any one of NoSQL, spatial, cloud or in-memory databases.'),dict(marks=1,criterion='A second distinct approach from NoSQL, spatial, cloud or in-memory databases.')]
                q['solution'] = 'Any two distinct approaches: NoSQL, spatial, cloud, in-memory databases.'
    for path,b in zip(paths,batches):
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(b,ensure_ascii=False,indent=2));temp.replace(path)
    audit_path = O/'papers'/sid/'paper_audit.json'
    audit = json.loads(audit_path.read_text())
    audit['source_transcription_check'] = 'Manual leaf transcription; full original raster authoritative; no OCR exactness claim.' if sid=='SRC-001' else 'Exact marked-leaf intervals reconstructed from the original PDF; count and original mark sequence match every leaf.'
    audit['context_evidence_check'] = 'Every leaf links complete original page rasters and all pages for its parent question; original PDF unchanged.'
    audit['next_exact_action'] = 'Coordinator independent validation and authoritative merge; no source remains in this shard.'
    audit['notes'] = ('All four original options extracted; each option is 65 marks, 260 inventory marks total. These are old-syllabus source options, not a 2027 examination format.' if sid in ['SRC-034','SRC-042'] else audit.get('notes',''))
    audit_path.write_text(json.dumps(audit,indent=2))
    print(sid,len(sources),'source leaves have complete linked page evidence')
