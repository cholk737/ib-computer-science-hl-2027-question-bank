# Unofficial analysis of the uploaded 2027 HL specimens

Specialist analysis by Agent 3, independently checked and integrated by the coordinator. Chunk 1, Step 3 only. Verified checkpoint C1-003, 2026-11-04 (Europe/Zurich). This report analyses official uploaded reference material; it is not an official IB interpretation or a newly authored paper/markscheme.

## Sources and page references

All specimen references below use **one-based PDF pages in the 154-page compilation**, `sources/2027-specimen/Specimen Papers 2027 - English.pdf`. Parentheses give the page printed within that component when useful. The 67-page guide is `sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf`; its PDF page is printed page + 6.

| Component | Compilation PDF pages | Component pages |
|---|---:|---:|
| HL Paper 1 | 3-18 | 1-16 |
| HL Paper 1 markscheme | 19-35 | 1-17 |
| HL Paper 2 | 37-61 | 1-25 |
| Selected Python version, labelled Option B, Q7-12 | 50-61 | 14-25 |
| HL Paper 2 markscheme | 63-84 | 1-22 |
| Selected Python marking, Q7-12 | 76-84 | 14-22 |
| Case study: Preventing network security attacks | 151-154 | 1-4 |

Paper 2 Java is a parallel language version, Q1-6 on PDF38-49, not an additional 80-mark section. The compilation also includes SL papers and markschemes, excluded from the HL target except to confirm repeated questions. `COMPONENT_MANIFEST.csv` identifies every component and separator. No required HL paper, selected Python content, markscheme or specimen case-study page is missing or unreadable.

## Binding guide requirements

The guide, not a specimen's particular scenario or question count, defines the examination requirements:

- Guide PDF53 (printed47): each HL paper lasts 2 hours, carries 80 marks and contributes 40% of course assessment. Both papers together are four hours and 80%.
- Guide PDF55 (printed49): Paper 1 is compulsory throughout. Section A has 56 marks on common SL/HL and HL-only Theme A content. Section B has 24 marks on the pre-seen case study and its four challenges. The sections are completed together without interruption.
- Guide PDF55-56 (printed49-50): HL case-study investigation spans understanding systems and computational thinking, application in context, transfer to other scenarios, impacts and ethics, and evaluation/formulation/justification of strategies using case material, independent research and fresh examination stimulus. Research can include primary/secondary sources, interviews, guest speakers and field trips. The guide says a case study is published 12 months before May and 18 months before November; this is a statement of the uploaded guide's policy, not a claim that a particular future case is available.
- Guide PDF56 (printed50): Paper 2 covers common and HL-only Theme B. All questions in the selected language version are compulsory. Two SL questions recur in HL, including an algorithmic-thinking question that needs neither code interpretation nor code writing. Further questions address HL content.
- Guide PDF15 and 56 (printed9,50): Python and Java versions are comparable in topic, context and assessment objective. Certain built-in functions can be prohibited to expose an algorithmic skill, and such restrictions must be explicitly stated. There is no general prohibition on Python built-ins.

The future practice-exam project selects **Python**. The specimen's Option A/B labels are language choices and must not be confused with old-syllabus subject options. The six Python questions constitute the complete 80-mark Paper 2 version. A future unofficial Python-only paper may use clear consecutive numbering; preserve source Q7-12 in provenance.

## Paper 1: observed specimen structure

Cover PDF3 confirms 2 hours and 80 marks, all Section A questions and the Section B question, a clean case-study copy, and answers within the provided boxes. Section A begins PDF4; Section B begins PDF14. The official markscheme allocation on PDF22 independently confirms 56/24/80.

| Section | Question | Content and assessment forms | Marks |
|---|---|---|---:|
| A | 1 | CPU accumulator, number representation, logic circuit/truth table, OS accounting, PaaS, compiled/interpreted execution | 13 |
| A | 2 | LAN/internet device, TCP/IP, transmission media, switching, NAT | 14 |
| A | 3 | SQL query, 3NF schemas and keys, distributed atomicity, spatial database application | 14 |
| A | 4 | CNN layers, data preparation, GPU training, F1 evaluation, RL justification, contextual ethical discussion | 15 |
| B | 5 | Malware and phishing; BYOD security and benefits; prevention/response evaluation grounded in the case | 24 |
| | | Total | **80** |

There are **26 independently marked leaf parts**: 21 in Section A and 5 in Section B. Section A totals 13+14+14+15=56; Section B totals 2+2+4+4+12=24. Short factual tasks often lead into application and explanation. This is a connected extended-question format containing short subparts, not a requirement that every answer be an essay. Q3 includes both executable SQL-style construction and relational representation; Q1 requires a visual logic representation. Q4(f) is a 5-mark contextual discussion and Q5(d) a 12-mark research-informed evaluation.

The specimen's four Theme A questions and one case question are useful assembly benchmarks, not an express guide rule fixing all future papers to five question numbers or those exact topic weights. A specimen is not proof of complete syllabus coverage.

## Paper 2: observed Python structure

Cover PDF37 explicitly says answer all questions in one option. Option B begins PDF50 with the requirement that all response code be Python. There are **28 independently marked leaf parts**, across six compulsory Python questions:

| Source question | Python PDF pages (printed pages) | Assessment emphasis | Marks |
|---|---|---|---:|
| 7 | 50-53 (14-17) | Flowchart and trace table, Big O, text-file algorithm, stack operations and algorithmic steps | 15 |
| 8 | 54-55 (18-19) | Lists, strings, 2D indexing, Python tracing, 2D data-processing function | 15 |
| 9 | 56-58 (20-22) | OOP instantiation, encapsulation convention, class relationships, conditional methods, object lists, selection-sort explanation | 20 |
| 10 | 59 (23) | Dictionary lookup, sets and duplicate elimination, membership/intersection outputs | 7 |
| 11 | 60 (24) | BST insertion diagram, recursion, iterative trace, recursive construction, runtime limits | 13 |
| 12 | 61 (25) | Linked-list search code and ordered-insertion steps | 10 |
| | | Total | **80** |

Python Q7 and Q8 correspond to SL Python Q4 and Q5 on PDF122-127. They total 30 marks. The remaining 50 marks add HL assessment depth, but individual subparts in those questions should not all be labelled HL-only without exact syllabus mapping.

Q7 supplies the principal no-code algorithmic-thinking benchmark: flowchart/trace, file-processing steps and stack reasoning. Several later parts also request prose algorithms. Q9(e) expressly requires describing selection sort without code; Q12(b) likewise requires non-code ordered-insertion steps. Q7(f) expressly limits solutions to the supplied stack operations. These are task-specific constraints, not an invitation to ban all other functions throughout the paper.

Python conventions observed: zero-based list indices; nested lists for 2D data; `True`, `False`, `None`; `range`, `%`, comparisons and nested `for`/`while`; string splitting as a permitted marking alternative; `__init__`, `self`, instance attributes and object lists; dictionaries and sets, membership `in` and intersection `&`; recursive functions; object references linked through `next`. The sample markscheme uses ordinary helpers such as `len` and `.append`. Partial class stubs marked `# code missing` are scaffolds, not complete executable programs.

These observations do not independently broaden the guide. In particular, no extra library, Python-version-specific feature, recursion limit, import or advanced language mechanism is prescribed by this specimen.

## Commands, depth and difficulty

`SPECIMEN_QUESTION_INDEX.csv` and its JSON counterpart contain all 54 marked leaf parts, mark allocations, command terms, source and markscheme page references, response types and expectations. Command-term objectives come from guide PDF66 (printed60); "Copy and complete" is recorded as source wording with a clearly labelled analyst inference to tracing. The objective attached to a command term is not a complete empirical difficulty rating.

Observed commands include State, List, Identify, Outline, Describe, Explain, Construct, Sketch, Justify, Discuss and To what extent. A one-mark State normally needs a specific brief result. Multi-mark explanation/construction needs sufficient independent reasoning or correct components. The markscheme frequently structures a two-mark Outline as an idea and expansion; always follow the local allocation rather than assuming a universal formula.

The index's low/medium/high labels are **qualitative analyst estimates**, not official IB labels, measured difficulty data or a mandatory distribution. On that basis, Paper 1 has 17/41/22 marks and Paper 2 has 9/47/24 marks respectively. Lower-demand recall and simple output tasks coexist with contextual explanation, relational design, extended evaluation, OOP, recursion and linked-list construction. Difficulty should come from the supported reasoning and representation, not lengthy prose or unfamiliar incidental contexts.

## Marking conventions and response expectations

General instructions and subject guidance are on PDF21-22 and 65-66. The useful assessment conventions are:

- Award whole marks, positively, up to each part's cap. More acceptable points than available marks are deliberate; they are not a totals error.
- Separate semicolon-ended points normally represent credit-bearing ideas. A slash offers accepted alternatives, and parenthesised wording need not appear to earn credit.
- Equivalent meaning and valid alternatives receive credit; effective technical communication matters more than minor language slips.
- When a correctly applied subsequent method uses an earlier wrong result, allow follow-through where applicable. Do not award credit to a contradicted assertion.
- For specified numbers of responses, use the source's particular identify/describe/explain guidance, rather than imposing a blanket penalisation policy.
- Coding criteria decompose solutions into meaningful steps and cap the total: for example Q8(e) and Q12(a) list more possible points than their 5-mark limits. Alternative correct algorithms remain possible.
- Q4(f), PDF31, has holistic levels: 1-2 limited/general; 3-4 contextual and fairly balanced; 5 appropriate conclusion linked to analysis.
- Q5(d), PDF34-35, has bands 1-3, 4-6, 7-9 and 10-12. Top-band work shows detailed understanding, accurate terminology, balanced analysis, conclusions tied to analysis, and clear evidence of extensive independent research. The commentary asks for prevention and response, supported by related real events and/or expertise.

Administrative details such as RED marking, RM Assessor buttons and stamping scanned pages are official examiner workflow, not requirements to reproduce in unofficial student materials. Generic references to multiple options in the P1 general template do not override P1's compulsory format.

## Case-study requirements and the four challenges

The supplied specimen-only case is TaylorMade Healthcare's network security scenario (PDF151-154), involving BYOD, ransomware, rootkits and prevention/recovery interventions. Its challenge list on PDF153 has **two common SL/HL challenges plus two additional HL-only challenges**, giving four challenges for HL:

1. Awareness strategies, especially ransomware and rootkit threats (common).
2. BYOD advantages balanced with preparation for security weaknesses (common).
3. Viability of segmentation and access control (HL additional).
4. Procedures for restoring operations after a breach (HL additional).

These are research challenges, not four compulsory separately numbered examination questions. The specimen assesses them through one multipart Q5, culminating in a 12-mark evaluation. A clean copy is required in the examination. Additional case terminology appears on PDF154. The specimen case must not silently become the case for a future actual session. Unless the user explicitly selects an official case, later project papers must use a clearly labelled **unofficial practice case study**.

## Source defects and cautions

These findings are limitations of the uploaded reference, not missing inputs or permission blockers. Originals remain unchanged. They must not be propagated as validated technical truths into newly authored questions.

| ID | Source | Finding and consequence |
|---|---|---|
| SP-01 | P2 Q12(a) sample code, MS PDF84 (22) | **Confirmed code defect.** The printed `else` is aligned with `while`; `temp` never advances when the head does not match. A later-node match or absent name loops indefinitely, and an empty list dereferences `None`. Visually verified in `renders/source-084.png`; bounded execution reproduced the failures. Use intended traversal criteria as a style reference, never copy this implementation as a correct answer. |
| SP-02 | P2 Q9(a)(ii), PDF56 (20), MS80 (18) | **Confirmed Python-semantics caution.** The source calls a single-underscore attribute private and describes restricted external access. Python does not enforce that restriction; external read/write succeeds. Future questions should distinguish non-public convention from enforced access control. |
| SP-03 | P2 Q9(b), PDF57 (21), MS80 (18) | **Relationship ambiguity.** MS calls the relationship composition and supports it with ticket-price dependence. A reference list and value dependence alone do not establish lifetime ownership. Future questions must specify ownership/lifetime if aggregation versus composition is to have one unambiguous answer. This is a source interpretation concern, not an assertion that every composition reading is impossible. |
| SP-04 | P2 Q11(c)(ii), PDF60 (24), MS83 (21) | **Unstated-domain limitation.** The recursive sample works for nonnegative integers, but for -1 the iterative function returns 0 while the sample recurses to failure. No input range is stated in the question. Future questions should specify the intended range or handle `x <= 0` consistently. |
| SP-05 | P1 Q1(f), PDF5 (3), MS24 (6) | **Scope caution.** The compiled/interpreted speed comparison is an educational model, not a universal performance guarantee for every implementation/workload. Frame future reasoning around the stated execution model and avoid absolute claims about all modern runtimes. |

`verify_specimen_examples.py`, `source_find_player_transcription.py` and `technical_checks.json` preserve reproduction evidence. Ten ordinary example checks passed: hexadecimal and truth table; flowchart output; stack content; nested-loop output; set membership and intersection; iterative summation; nonnegative recursive examples; ticket-price boundary cases. The source-defect tests are deliberately separate from passing examples. They do not claim exhaustive correctness of every official answer.

## Verification and handover

- Checked the selected papers and markschemes in full extracted text; inspected rendered layout for covers, question structures, logic circuit, flowchart, stack, database table, OOP scaffold, BST, markbands and linked-list sample indentation.
- `source_mark_sequence_checks.json` independently compares every printed mark at the end of a question line against the index on all **23 question-bearing PDF pages**. All sequences match. `mark_totals_verification.json` confirms 26+28=54 leaves, 80+80=160 reference marks and P1 56/24.
- Recorded all component boundaries, including excluded SL/Java material. The specimen question index is a reference-analysis artifact, not a historical question bank, syllabus-coverage claim or generated examination.
- No historical questions have been processed, no practice questions authored, and no new examination or markscheme PDF produced in this assignment.

Coordinator verification completed: all marked-page sequences were independently reconstructed from the original PDF and matched to all 54 index parts; totals passed. Rendered compilation pages 35,50,56,57,84,153 were independently inspected. Bounded execution independently reproduced SP-01, an external read/write check confirmed SP-02, and negative-input execution confirmed SP-04. The guide assessment and command-term pages were independently read. Evidence: `audits/SPECIMEN_INTEGRATION_CHECK.json`. All technical evidence/scripts named above remain in `agents/chunk-1/agent-3-specimen/`.

All five cautions are recorded in `QA_ISSUES.md`; source PDFs remain unchanged. The published blueprint describes the official specimen format and is not a Chunk 3 practice-paper blueprint. Chunk 1 stops here. Any historical processing requires new user authorization for Chunk 2.
