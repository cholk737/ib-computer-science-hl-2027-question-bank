# Chunk 2 completion report — unofficial practice system

Checkpoint C2-FINAL, 4 November 2026 (Europe/Zurich). Steps 4–6 complete; stop before Chunk 3.

## Verified totals

- 23 distinct historical examinations fully processed; 0 remain. All old subject options included.
- 1,141 marked source subquestions extracted/classified (3,330 original source marks across all options).
- 838 source subquestions mapped to exact 2027 statements/guidance:383 A directly relevant and455 B requiring adaptation.
- 823 converted practice records, with separate preliminary unofficial marking records;15 source records explicitly reuse existing practice questions.
- 303 C exclusions retained with specific reasons;0 unresolved mappings;no invented D historical records or original gap-filling questions.
- 1,418 mapping-index rows, including303 explicit exclusion rows;152 approved batch handoffs from exactly three native specialist processors.

Counts are records, not a claim of complete syllabus coverage. 93 normalized source-text match groups are flagged for contextual/assembly review; meaningful statement/bullet coverage is the later Chunk 3 task.

| Source | Historical identity | Shard | Source leaves | Scoped A/B | Locally created practice | C excluded |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| SRC-001 | May 2026 HL P1 | A | 33 | 27 | 27 | 6 |
| SRC-002 | May 2026 HL P2 | B | 86 | 60 | 60 | 26 |
| SRC-004 | November 2023 HL P1 | C | 39 | 31 | 31 | 8 |
| SRC-005 | November 2022 HL P1 | A | 35 | 28 | 28 | 7 |
| SRC-006 | November 2021 HL P1 | B | 36 | 24 | 24 | 12 |
| SRC-007 | May 2021 HL P1 | C | 37 | 35 | 35 | 2 |
| SRC-008 | November 2019 HL P1 | A | 34 | 28 | 28 | 6 |
| SRC-009 | November 2024 HL P1 | B | 37 | 32 | 32 | 5 |
| SRC-016 | November 2023 SL P1 | C | 28 | 20 | 8 | 8 |
| SRC-018 | May 2023 HL P1 | A | 37 | 28 | 28 | 9 |
| SRC-020 | May 2023 HL P1 | B | 37 | 28 | 27 | 9 |
| SRC-022 | November 2025 HL P1 | C | 38 | 31 | 31 | 7 |
| SRC-024 | November 2025 SL P1 | A | 26 | 18 | 18 | 8 |
| SRC-026 | May 2025 HL P1 | B | 30 | 23 | 22 | 7 |
| SRC-028 | May 2025 SL P1 | C | 24 | 19 | 19 | 5 |
| SRC-030 | May 2025 HL P1 | A | 30 | 23 | 22 | 7 |
| SRC-032 | May 2023 HL P2 | B | 89 | 61 | 61 | 28 |
| SRC-033 | November 2020 HL P2 | C | 75 | 53 | 53 | 22 |
| SRC-034 | November 2023 HL P2 | A | 87 | 60 | 60 | 27 |
| SRC-038 | November 2025 HL P2 | B | 91 | 59 | 59 | 32 |
| SRC-040 | November 2025 SL P2 | C | 64 | 43 | 43 | 21 |
| SRC-042 | May 2025 HL P2 | A | 87 | 61 | 61 | 26 |
| SRC-044 | May 2025 SL P2 | B | 61 | 46 | 46 | 15 |

“Locally created” uses the practice ID's originating source; reused links retain all source provenance. Differences in numbers/contexts can remain as practice variants. Do not treat variant counts as additional knowledge coverage.

## Files

- extraction/HISTORICAL_MANIFEST.csv/json; HISTORICAL_QUESTION_INDEX.csv; by-paper/<source>/questions/*.json
- mapping/SYLLABUS_MAPPING.csv
- question-bank/QUESTION_BANK.csv; questions/, markschemes/, records/; marking policy/readme
- extraction/OBSOLETE_QUESTIONS.csv
- syllabus master: mechanical bank-ID links updated, exact official scope unchanged; no gap audit performed
- three isolated specialist folders: batches, exact source/context evidence, figures, code checks, per-paper audits and final receipts
- audits/chunk-2/APPROVED_BATCHES.json, MERGE_LEDGER.json, FINAL_VALIDATION.json, source/candidate/technical/visual review evidence

## Verification

All 1,141 source leaves reconcile to original allocations:21 text-readable papers checked by independent right-margin census;two scans checked by owners page-by-page, with coordinator visual resolution of every OCR allocation discrepancy. All original/copy PDF hashes agree. Authors read their source papers and available markschemes, preserved source code/tables/figures, and verified each adapted answer. Coordinator reviewed all three handoffs, mapped scope, representative questions/solutions and source defects.

Coordinator reran 134 saved Python code records and available inline assertions, six independent boundary/oracle families, 93 answer-versus-code AST comparisons (one equivalent implementation tested separately), and nine SQLite checks (eight SELECT answers and one stored-versus-fresh average scenario). All passed. Agent C additionally re-examined original source/MS pages and independently tested A/B overnight-time and repeated-trial algorithms; both pass. All bank marking allocations and source/bank/MS links pass final integrity checks.

Source/prose/mapping corrections are logged: exact transcriptions separated from earlier synopses; adapted command terms reconciled; generic paging/social and incidental OOP mappings repaired; SQL identifiers protected after a caught polish regression; SRC040 allocation pages separated from later context; B's original marking evidence separated from adapted-answer fallback. Scope/wording corrections are represented in final approved hashes. Original source defects remain unchanged and explicitly identified.

This is author-wide verification plus independent coordinator sampling and executable checks, not an assertion that every prose answer has received the later independent exam-specific audit. That audit and final markscheme/PDF production remain Chunk 4.

## Limitations and stop boundary

No uploaded official markschemes exist for 2026 SRC001/SRC002; their solutions/criteria are independently authored and unofficial. Scanned source quality/annotations remain in original evidence; annotations were excluded as official answer evidence. SRC047 omits only a blank page, confirmed against canonical SRC005; no question content is missing.

Original-source errors and 93 duplicate text candidates remain documented, not unresolved invented references. Full syllabus/bullet coverage and difficulty distribution have not been audited. No student examination or markscheme PDFs have been generated. Await explicit user authorization for Chunk 3 (Steps 7–9).
