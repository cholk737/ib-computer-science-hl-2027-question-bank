# Verified syllabus scope — Chunk 1

Checkpoint C1-002, 4 November 2026 (Europe/Zurich). This is an unofficial scope extraction from the uploaded official guide, not a replacement guide or an authored examination.

## Source and completeness

Source: `sources/2027-guide/Computer-Science-First-Assessment-2027-guide-sbs (1).pdf`, SHA-256 `7e7c9408946e66e9b3d58ccb43110cf0b4bf55d368ca5cd6ebcf11437fbe9745`.

The entire Syllabus Content section was examined: physical PDF pp34–49, printed pp28–43, including the last page's linking-question continuation. Scope statements are on PDF pp34–48. Guiding/linking questions and teaching hours were read and retained as source context; they are not additional coded requirements.

| Topic | Individual statements | Common SL/HL | HL-only |
| --- | ---: | ---: | ---: |
| A1 Computer fundamentals | 22 | 16 | 6 |
| A2 Networks | 17 | 12 | 5 |
| A3 Databases | 18 | 11 | 7 |
| A4 Machine learning | 17 | 4 | 13 |
| Theme A subtotal | 74 | 43 | 31 |
| B1 Computational thinking | 4 | 4 | 0 |
| B2 Programming | 18 | 16 | 2 |
| B3 Object-oriented programming | 10 | 5 | 5 |
| B4 Abstract data types | 6 | 0 | 6 |
| Theme B subtotal | 38 | 25 | 13 |
| **Complete HL scope** | **112** | **68** | **44** |

The master includes all 112 unique applicable statements. There are no missing or unreadable syllabus statements and no unresolved level classifications. The extracted guidance contains 269 bullet paragraphs plus two additional Theme A explanatory/exclusion paragraphs. Sixteen guidance paragraphs contain “must include” and 21 contain “may include”; these are paragraph counts, not extra statements or question coverage.

## Exact scope and interpretation

Guide PDF p34 / printed p28 defines “may include” as assessable examples with other examples possible; “must include” identifies all examples that will be used in assessment. Full clauses and bullets remain in the master records. Unqualified lists and “such as” wording have not been relabelled as formal must-include clauses. Derived skill/context fields are reading aids; the exact statement and guidance control.

HL-only status is inherited where explicitly designated at topic/subtopic level: A1.4, A3.4, A4.2, A4.3, B3.2 and all B4. Individual HL labels are also recorded. Common content is retained, including B2 complexity/search/sort and A4.4 ethics. General common OOP concepts are retained even where detailed multiple-class applications are HL-only.

Important scope limits remain explicit: A2.3.4 does not require explanation of a specific routing protocol; A4.2.3 excludes PCA/LDA statistical techniques; B2.4.5 construction/tracing of recursive code is limited to simple non-branching recursion, while B2.4.4 conceptual recursion has wider examples. No unsupported r-squared calculation requirement has been added.

Python is the project language. Java-specific alternatives remain in exact source transcriptions but are not imposed on Python questions. The generic OOP language needs accurate Python treatment in later authoring. See `agents/chunk-1/agent-2-theme-b/programming_policy_notes.md` for per-statement cautions. The guide permits built-ins unless a question explicitly prohibits particular functions.

## Verification evidence

1. Three native specialists ran in isolated folders. Agents 1 and 2 read all their assigned scope pages and visually inspected every relevant page; their own verification scripts independently compared text using pypdf and pdfplumber.
2. Coordinator independently counted codes directly from the source: `audits/independent_code_census.json`, 112 unique records, no gaps against the source set.
3. Coordinator reconstructed source statement/guidance blocks directly from the original PDF using pypdf and compared **all characters** to all 112 specialist records, ignoring layout whitespace and Unicode compatibility differences. Source-code identity, page sets and independently derived HL inheritance all pass: `audits/SYLLABUS_INTEGRATION_CHECK.json`.
4. Coordinator independently viewed rendered PDF pp35,40,42,46,47,48 to check source irregularities, cross-page guidance, recursion scope and inherited HL labels. This sampling supplements the specialists' full-page visual reviews.
5. All six cross-page statement continuations were checked: A2.3.1 (37–38), A3.2.6 (39–40), A3.4.3 (40–41), A4.2.1 (41–42), A4.3.7 (42–43), B2.4.2 (45–46). Numbers here are physical PDF pages.
6. Only the coordinator merged records, using `scripts/merge_syllabus.py`, gated by the passing source integration report. No specialist wrote shared master files.

## Source quirks and faithful transcription

- Guide PDF p35 / printed p29 prints `A.1.2.5`; exact source code is retained in `source_code`. The master lookup `A1.2.5` is an explicitly disclosed normalization, not a claim that this form was printed.
- A3.3.4 visibly lists `AVERAGE` among SQL aggregates. The source spelling is preserved; executable SQL syntax must be checked for the selected dialect in later chunks.
- A4.3.1 visibly prints r². The master restores superscript typography, retains the specialist's flattened raw transcription, and records the normalization. No scope inference follows from the formatting.
- Source line wraps and layout whitespace are normalized; printed wording and grammar remain intact. Source HL suffixes are retained in the master statement field when printed, and inherited labels have separate evidence metadata.

## Master records and coverage status

`SYLLABUS_MASTER.csv` is the index; `SYLLABUS_MASTER.json` and `records/<code>.json` preserve full guidance, scope qualifiers, source evidence, uncertainty flags and specialist provenance. CSV page arrays use JSON syntax; physical PDF pages are one-based.

Every statement currently has `coverage_status=not_yet_assessed_chunk1` and no question-bank IDs. No historical questions have been extracted, mapped or adapted, and no original practice questions have been authored. Scope completeness does not establish question coverage. Future assessment-specific scope sheets may select topics for one assessment while the guide remains authoritative for their meaning.
