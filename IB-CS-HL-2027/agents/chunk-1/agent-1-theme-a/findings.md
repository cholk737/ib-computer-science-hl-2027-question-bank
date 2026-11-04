# Agent 1 — Theme A Syllabus Analyst

Checkpoint C1-A-complete, 2026-11-04 (Europe/Zurich). Chunk 1 / Step 2 only.

## Source and ownership

Source: `sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf`, PDF pages 34–43 / printed pages 28–37. The full ten pages were read, rendered and visually inspected. The original source PDF was not modified. All this specialist's outputs are confined to `agents/chunk-1/agent-1-theme-a/`; no master files were edited.

## Complete individual-statement counts

| Topic | Total | SL/HL common | HL-only |
| --- | ---: | ---: | ---: |
| A1 Computer fundamentals | 22 | 16 | 6 |
| A2 Networks | 17 | 12 | 5 |
| A3 Databases | 18 | 11 | 7 |
| A4 Machine learning | 17 | 4 | 13 |
| **Theme A** | **74** | **43** | **31** |

All 74 source statements and their complete accompanying guidance are represented. Guidance comprises 179 bullet paragraphs and two additional non-bullet paragraphs: the explicit PCA/LDA exclusion and the crime-analysis association-rule example. No missing or unreadable Theme A statement was found. Every statement has a nonempty guidance record, level classification, assessable statement, allowed-context note, source pages and `not_yet_assessed_chunk1` coverage status. These counts establish scope completeness, not question-bank coverage.

HL-only status is inherited from the headings A1.4, A3.4, A4.2 and A4.3, as well as individual statement labels. Common content immediately following an HL-only subsection returns to common status where the source heading/statement does not designate HL-only. In particular A4.4.1–A4.4.2 remain common.

## Scope handling and important limits

- The scope note on PDF p34 / printed p28 explicitly defines **may include** as examples that could be assessed, with other examples also possible; **must include** lists all the examples used in assessment. Every record carries that global note; clause-level `must_include_guidance`, `may_include_guidance` and `explicit_scope_limits` are in JSON.
- All guidance is retained without treating illustrative examples as exhaustive technical requirements. `allowed_context` and `assessable_knowledge_skills` are index aids; the exact statement and full guidance remain authoritative.
- A2.3.4 explicitly excludes requiring an explanation of a specific routing protocol.
- A4.2.3 explicitly places statistical techniques such as principal component analysis (PCA) and linear discriminant analysis (LDA) beyond course scope.
- A4.3.1 mentions fit measures like r-squared; this wording is retained without inferring a further unsupported statistical calculation requirement.
- Source guiding/linking questions and teaching-hour headers are retained in page-evidence text. They are not silently appended to the previous individual learning statement as compulsory scope.

## Source irregularities requiring transparent treatment

1. **Code punctuation:** PDF p35 / printed p29 visibly prints `A.1.2.5 Construct logic diagrams.` The `source_code` field preserves `A.1.2.5`. `code=A1.2.5` is a disclosed indexing normalization consistent with adjacent source codes. This is one statement, not two. Coordinator should retain the source-code field and flag.
2. **SQL aggregate spelling:** A3.3.4 (PDF p40 / printed p34) visibly lists `AVERAGE, COUNT, MAX, MIN, SUM`. `AVERAGE` is preserved exactly. Future question/code authoring must verify dialect syntax and distinguish this guide wording from executable SQL syntax; this report does not silently substitute `AVG`.
3. **Mathematical typography:** A4.3.1 (PDF p42 / printed p36) visibly uses r with a superscript 2. Plain-text libraries flatten it to `r2`; the record flags that typography and the source PNG preserves it. No mathematical meaning is uncertain.
4. Source grammar such as “Explain how classifications techniques …” in A4.3.2 is preserved without editorial correction.

## Verification performed

`extract_theme_a.py` extracts directly from the PDF using pdfplumber. `verify_theme_a.py` independently reads the original PDF with pypdf and confirms all 74 unique codes and all **351 evidence lines** in the independently extracted page text. Assertions check unique expected code sets, nonempty guidance, 43/31 level counts and the five page continuations:

| Statement | PDF pages | Printed pages |
| --- | --- | --- |
| A2.3.1 | 37–38 | 31–32 |
| A3.2.6 | 39–40 | 33–34 |
| A3.4.3 | 40–41 | 34–35 |
| A4.2.1 | 41–42 | 35–36 |
| A4.3.7 | 42–43 | 36–37 |

All ten rendered pages `visual-34.png` through `visual-43.png` were inspected individually, including HL labels, the standalone `(HL only)` continuation, inherited HL headings, statement transitions, the code punctuation, source SQL spelling, mathematical superscript and exclusion note. `verification_results.json` records the checks. Per-topic checkpoints are `checkpoint-A1.json` through `checkpoint-A4.json`; the combined checkpoint is `checkpoint.json`.

## Deliverables and coordinator handoff

- `theme_a_scope.csv`: one row per individual statement, including full guidance and record link.
- `theme_a_scope.json`: substantive structured records, all bullets, source-line/page evidence, exact source code and flags.
- `records/A1.1.1.json` through the individual 74 code records: durable statement records referenced by the CSV.
- `evidence-page-034.txt` through `evidence-page-043.txt`: full page text, including non-assessment contextual material.
- `visual-34.png` through `visual-43.png` and two contact sheets: source visual evidence.
- Reproducible extraction/verification scripts, verification results and checkpoints.

Ready for coordinator review and authoritative merge. No historical question extraction, mapping, adaptation, original questions, examination drafts or markscheme generation was performed.
