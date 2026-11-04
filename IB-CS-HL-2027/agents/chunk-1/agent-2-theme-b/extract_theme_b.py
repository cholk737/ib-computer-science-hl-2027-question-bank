"""Theme B specialist extraction. All writes stay in this specialist's directory."""
from pathlib import Path
import re, json, csv, hashlib
from collections import Counter
from pypdf import PdfReader

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
GUIDE=PROJECT/'sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf'
reader=PdfReader(GUIDE)

def join(lines):
    text=''
    for line in lines:
        line=line.strip()
        if not line: continue
        text += ('' if not text or text.endswith(('-', '/')) else ' ')+line
    return text

records=[]
current=None
part=None
def flush():
    global current
    if current is not None:
        current['statement']=join(current.pop('_statement'))
        current['guidance_bullets']=[join(b) for b in current.pop('_bullets')]
        current['guidance']='\n'.join('• '+b for b in current['guidance_bullets'])
        records.append(current)
        current=None

for pdf_page in range(44,50):
    text=reader.pages[pdf_page-1].extract_text(extraction_mode='layout')
    (OUT/f'evidence-pdf-page-{pdf_page}.txt').write_text(text)
    for raw in text.splitlines():
        line=raw.strip()
        if not line or line=='Syllabus content' or 'Computer science guide' in line: continue
        if re.match(r'^(Linking questions|Guiding question|B[1-4]\.\d+\s|B[1-4] )',line):
            flush(); part=None; continue
        m=re.match(r'^(B[1-4]\.\d+\.\d+) (.*)',line)
        if m:
            flush()
            current={'code':m[1], '_statement':[m[2]], '_bullets':[], 'source_pdf_pages':[pdf_page]}
            part='statement'
        elif current is not None:
            if pdf_page not in current['source_pdf_pages']:current['source_pdf_pages'].append(pdf_page)
            if line.startswith('•'):
                current['_bullets'].append([line[1:].strip()]);part='bullet'
            elif part=='statement':current['_statement'].append(line)
            elif part=='bullet':current['_bullets'][-1].append(line)
flush()

expected={**{'B1.1':4},**{f'B2.{s}':n for s,n in [(1,4),(2,4),(3,4),(4,5),(5,1)]},'B3.1':5,'B3.2':5,'B4.1':6}
assert {r['code'] for r in records}=={f'{sub}.{i}' for sub,n in expected.items() for i in range(1,n+1)}
assert len(records)==38

topics={'B1':'Computational thinking','B2':'Programming','B3':'Object-oriented programming','B4':'Abstract data types'}
subtopics={'B1.1':'Approaches to computational thinking','B2.1':'Programming fundamentals','B2.2':'Data structures','B2.3':'Programming constructs','B2.4':'Programming algorithms','B2.5':'File processing','B3.1':'Fundamentals of OOP for a single class','B3.2':'Fundamentals of OOP for multiple classes (HL only)','B4.1':'Fundamentals of ADTs'}
skills={
'B1.1.1':'Construct a problem specification with relevant problem definition, constraints, inputs, outputs and evaluation criteria.',
'B1.1.2':'Describe abstraction, algorithmic design, decomposition and pattern recognition.',
'B1.1.3':'Explain application of computational thinking to approach and solve problems; programming is not required.',
'B1.1.4':'Trace standard-symbol flowcharts, track variables and determine outputs.',
'B2.1.1':'Construct and trace programs using global/local variables and the listed data types.',
'B2.1.2':'Construct programs that extract and manipulate substrings.',
'B2.1.3':'Describe failure points, exception handling and try/except/finally in Python.',
'B2.1.4':'Construct and use debugging techniques; named techniques are non-exhaustive examples.',
'B2.2.1':'Compare static/dynamic structures in allocation, resizing, speed, memory usage and flexibility.',
'B2.2.2':'Construct programs using 1D/2D Python Lists, adding, removing and traversing dynamic-list elements.',
'B2.2.3':'Explain LIFO stacks, named operations, performance/memory impact and appropriate selection.',
'B2.2.4':'Explain FIFO queues, named operations, performance/memory impact and appropriate selection.',
'B2.3.1':'Construct correctly sequenced programs and avoid instruction-order errors.',
'B2.3.2':'Construct selection with Python if/else/elif, Boolean and relational operators.',
'B2.3.3':'Construct counted/conditional loops and conditions governing execution.',
'B2.3.4':'Construct reusable functions and modular programs; apply local/global scope.',
'B2.4.1':'Calculate time/space Big O and describe scalability and efficiency in algorithm choice.',
'B2.4.2':'Construct and trace linear/binary searches; compare efficiency and select an appropriate technique.',
'B2.4.3':'Construct and trace bubble/selection sort and evaluate time/space complexity and relative efficiency.',
'B2.4.4':'Explain recursion, advantages/limitations, applications and memory/complexity; conceptual recursive examples include quicksort.',
'B2.4.5':'Construct and trace simple, non-branching recursive algorithms only.',
'B2.5.1':'Construct sequential text-file code to open read/write/append, read, write, append and close.',
'B3.1.1':'Evaluate OOP concepts and advantages/disadvantages for modelling real-world entities.',
'B3.1.2':'Design classes, methods and behaviour; use UML class diagrams for relationships, attributes and methods.',
'B3.1.3':'Distinguish static/non-static variables/methods, usage/scope, instance/class variables and code application.',
'B3.1.4':'Define classes, instantiate objects and initialize state through constructors.',
'B3.1.5':'Explain/apply encapsulation, information hiding, access control and protection of object state.',
'B3.2.1':'Explain/apply inheritance, reuse/extensions and the effect of parent-member access restrictions.',
'B3.2.2':'Construct polymorphic code, method overriding and dynamic/static polymorphic behaviour within language-appropriate semantics.',
'B3.2.3':'Explain abstraction, modular code and abstract classes providing common subclass interfaces.',
'B3.2.4':'Explain composition/aggregation, design with components and distinguish dependent versus independent component lifetimes.',
'B3.2.5':'Explain common OOP design patterns and recurring-problem applications; named patterns include singleton, factory and observer.',
'B4.1.1':'Explain ADT properties/purpose as high-level structures and associated operations.',
'B4.1.2':'Evaluate singly/doubly/circular linked lists, sketch operations and compare memory/performance with arrays.',
'B4.1.3':'Construct/apply singly/doubly/circular linked lists and basic operations.',
'B4.1.4':'Explain BST structures/properties and organization; insert/delete/traverse/search nodes and sketch BSTs.',
'B4.1.5':'Construct/apply unordered unique-element sets, union/intersection/difference, membership/add/remove and subset/superset code.',
'B4.1.6':'Explain ADT principles, hash mechanics/functions/collisions/load factors, set mechanics and Python dict/set.',
}
contexts={
'B1.1.1':'Problem specifications; named specification elements are may-include examples.',
'B1.1.2':'Computational problem-solving using the four listed concepts.',
'B1.1.3':'Real-world problems; software development, data analysis, ML, database design and network security are may-include examples.',
'B1.1.4':'A range of programming-algorithm flowcharts using listed standard symbols.',
'B2.1':'Python programs and relevant inputs/failures/debugging scenarios within the stated scope.',
'B2.2':'Data-structure choices and Python List programs, stack/queue problems with performance and memory considerations.',
'B2.3':'Python programs selected to meet specified objectives, using the relevant constructs and functions.',
'B2.4.1':'Specific algorithms with assessable time/space scalability and efficiency requirements.',
'B2.4.2':'Linear/binary search and efficiency-driven technique selection; the sorted/indexed names/phone-number example illustrates context.',
'B2.4.3':'Bubble/selection sort across various data sets.',
'B2.4.4':'Problems decomposable into smaller similar subproblems; quicksort, fractal image creation, binary-tree traversal and sorting are included conceptual contexts.',
'B2.4.5':'Simple, non-branching recursive programs only; do not turn conceptual quicksort coverage into a requirement to construct branching recursion.',
'B2.5':'Sequential text files and read/write/append modes. Listed Python functions are may-include examples.',
'B3.1':'OOP scenarios modelling entities, single-class design/code, UML and class/object state, as specified.',
'B3.2':'Multiple-class OOP scenarios using the specified inheritance/polymorphism/abstraction/relationships/design-pattern scope.',
'B4.1':'Specified ADTs and operations, diagrammatic linked lists/BSTs, Python implementations where requested, memory/performance comparisons.',
}

for r in records:
    c=r['code']; topic=c[:2]; sub=c.rsplit('.',1)[0]
    hl = c in ['B2.4.4','B2.4.5'] or sub=='B3.2' or topic=='B4'
    r.update(theme='B',topic=f'{topic} {topics[topic]}',subtopic=f'{sub} {subtopics[sub]}',
        level='HL-only' if hl else 'SL/HL common',
        level_evidence=('Explicit statement marker (HL only)' if c in ['B2.4.4','B2.4.5'] else 'Inherited from B3.2 heading (HL only)' if sub=='B3.2' else 'Inherited from B4 heading (HL only)' if topic=='B4' else 'No HL-only marker; common content'),
        source_printed_pages=[p-6 for p in r['source_pdf_pages']],
        source_file=str(GUIDE.relative_to(PROJECT)),source_sha256=hashlib.sha256(GUIDE.read_bytes()).hexdigest(),
        scope_qualifications=' | '.join(b for b in r['guidance_bullets'] if any(w in b.lower() for w in ['must include','may include','only','not limited','such as'])),
        scope_bullet_labels=[{'text':b,'label':'must include' if 'must include' in b.lower() else 'may include (non-exhaustive examples)' if 'may include' in b.lower() else 'explicit limit' if 'only' in b.lower() else 'unqualified guidance'} for b in r['guidance_bullets']],
        assessable_knowledge_skills=skills[c],allowed_context=contexts.get(c,contexts.get(sub,contexts.get(topic,''))),
        coverage_status='not_yet_assessed_chunk1',question_bank_ids=[],
        verification_status='specialist_source_and_visual_verified; coordinator_review_pending',
        record_path=f'agents/chunk-1/agent-2-theme-b/records/{c}.json')
    assert r['allowed_context'],c
    (OUT/'records').mkdir(exist_ok=True)
    (OUT/'records'/f'{c}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

(OUT/'theme_b_scope.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
fields=['code','theme','topic','subtopic','statement','level','source_pdf_pages','source_printed_pages','guidance','scope_qualifications','assessable_knowledge_skills','allowed_context','coverage_status','verification_status','record_path','level_evidence','source_file','source_sha256']
with (OUT/'theme_b_scope.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in records:
        row={k:r[k] for k in fields}
        for k in ['source_pdf_pages','source_printed_pages']:row[k]=';'.join(map(str,row[k]))
        w.writerow(row)
counts={t:{'total':sum(r['code'].startswith(t+'.') for r in records),'common':sum(r['code'].startswith(t+'.') and r['level']=='SL/HL common' for r in records),'hl_only':sum(r['code'].startswith(t+'.') and r['level']=='HL-only' for r in records)} for t in topics}
summary={'total':len(records),'common':sum(r['level']=='SL/HL common' for r in records),'hl_only':sum(r['level']=='HL-only' for r in records),'counts_by_topic':counts,'guidance_bullets':sum(len(r['guidance_bullets']) for r in records),'must_include_bullets':sum('must include' in b.lower() for r in records for b in r['guidance_bullets']),'may_include_bullets':sum('may include' in b.lower() for r in records for b in r['guidance_bullets'])}
(OUT/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
