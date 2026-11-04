# Processor C findings — final source-processing checkpoint

Checkpoint `CHUNK2-C-FINAL-2026-11-04`. All seven assigned papers are processed through Steps 4–6. No shared masters, other agents’ outputs, or Chunk 3 work were edited. Coordinator verification/integration remains authoritative.

| Source | Leaves | Original marks, all options | Unique practices | Reuse links | C exclusions |
|---|---:|---:|---:|---:|---:|
| SRC-004 | 39 | 100 | 31 | 0 | 8 |
| SRC-007 | 37 | 100 | 35 | 0 | 2 |
| SRC-016 | 28 | 70 | 8 | 12 | 8 |
| SRC-022 | 38 | 100 | 31 | 0 | 7 |
| SRC-028 | 24 | 70 | 19 | 0 | 5 |
| SRC-033 | 75 | 260 | 53 | 0 | 22 |
| SRC-040 | 64 | 180 | 43 | 0 | 21 |
| Total | 305 | 880 | 220 | 12 | 73 |

Classification totals: A 115, B 117, C 73. SRC-033 includes all four old HL options, 65 marks each; SRC-040 includes all four old SL options, 45 marks each. Original candidate maxima remain 65/45. SRC-016 reused questions were independently compared with SRC-004 and retain explicit duplicate/reuse IDs.

`batches/` contains separate source and unofficial practice records. Per-paper `papers/SRC-xxx/paper_audit.json` lists every leaf, mark, physical page and current batch filename. SRC-040 uses eight batches of 7–9 leaves. `final_receipt.json` and `checkpoint.json` provide the aggregate checkpoint.

All 305 `original_text` fields are verbatim PDF text-layer leaf extracts, with complete original question blocks and linked raw page transcriptions. There are zero synopsis fallbacks. Previous hand-entered synopses survive only in separate synopsis fields. Source renders remain the visual authority for diagram geometry, typography and text extraction artifacts. Shared table/code pages are linked, including SRC-007 Q14, SRC-033 Q13 and SRC-040 multi-page questions/classes. All source question pages were inspected; SRC-040 MS ERD/UML pages were also rendered and inspected.

Technical checks passed for all 45 Python-bearing records and three SQL queries, with executable edge checks in `verify_practice.py` and 48 results in `technical_checks.json`. Checks include empty/singleton inputs, threshold equality, first/middle/last/absent searches, object identity/list holes, stack restoration, inherited dispatch, fractional means, SQL boundaries, independent permutation-cycle oracles and repeated-trial denominators. All marking allocations sum correctly, valid syllabus codes carry exact guidance, and adapted command metadata follows adapted wording. `final_audit.py` verifies these invariants and durable source/asset links.

Explicit final prose cleanup fixes fused words across old batches, including every P-SRC016-Q12-d criterion. It preserves code and source transcriptions. See `final_polish_audit.json`. Do not reconstruct batches from first-pass author scripts without rerunning subsequent source repairs and final corrections; checked batch JSON files are the handoff authority.

Material source defects and scope decisions:

- SRC-004: source MS uses MARKS where paper uses SCORES; a sorting sample has questionable bounds. Correct independently checked Python used.
- SRC-007 / MS-013 PDF 16 Q14(c): one example resets TOTAL after reading the first valid input, omitting it. Adaptation fixes this. Broad claims about every dynamic structure were not imported.
- SRC-022 / MS-023 PDF 10: VPN anonymity/multiple-exit-node claims are not generally valid; omitted. WEP/SSID and generic dynamic-structure claims were not promoted to new requirements.
- SRC-028 / MS-029 PDF 15: integer division is accepted for an average, producing wrong fractional-threshold outcomes. Adaptation uses true division and tested boundaries. P-SRC028-Q10-b-i credits a fibre property and linked campus explanation, not repeating the supplied medium. P-SRC028-Q10-a requires authentication/authorization reasoning; MFA is optional.
- SRC-033: source claims about dates, supervised genetic algorithms, browser authentication by site certificates, aggregation preventing reuse, arbitrary BSTs guaranteeing logarithmic search, and singly linked tail pop being constant-time were corrected or excluded. MS-036 PDF 23 addVehicle example 1 has defective index/return logic. Existing-object operations in Q13(d)(ii), Q14(a), Q14(d)(i), Q15(c) do not claim B3.1.4 constructor coverage.
- SRC-040 / MS-041: PDF 7 SQL example omits a comparison operand and mixes date formats; adaptation uses a tested ISO full-day interval. PDF 11 gives a decimal inconsistent with (1/2)^10 and false spreadsheet shuffling limitations. PDF 13 loops 1000 rather than 10000 with inconsistent percentage scaling; adaptation uses its actual positive trial count. Original Case constructor identifiers are inconsistent. PDF 31 example 2 omits the count return. PDF 32 mixes aggregation/composition and incorrectly excludes polymorphic delegation; adapted lifetimes are explicit. Q12(a)(ii) prose permits any passed judgment but its bullet specifies A; adaptation explicitly requires A only.

Narrow B conversions retain only supported reasoning and explain discarded historical requirements. Old web-science/SEO/CGI, generic simulation and industry-policy material is C unless a concrete scoped subskill survives. These records do not establish complete syllabus coverage; that audit belongs to Chunk 3.

SRC-040 provenance correction: all 64 records now have an explicit `mark_allocation_pdf_page` and primary `source_pdf_pages` containing the actual leaf page only. Supporting pages are separate `context_pdf_pages`/raw context links. The 13 formerly shifted references are Q2(a–d) → physical 5, Q4(a)(i–ii)/(b) → 9, Q6(a) → 13, Q7(a)(i–ii)/(b–d) → 15. `page_provenance_repair.json` lists all 64 assignments; no mark totals changed.

The bounded read-only cross-audit is complete in `cross_audit.md`/`.json` and `verify_cross_audit.py`: both adapted algorithms pass independent boundary/denominator checks. SRC-042’s source night-predicate/accumulator defects and SRC-038’s trial-count/scaling defect are confirmed. At the audit snapshot, Agent A still needed source-record evidence repair; Agent B needed only the wording “positive integer” for trials. Other ownership was unchanged.

Exact next action: coordinator revalidates the SRC-040 page repair, then integrates all seven papers. No remaining specialist extraction/conversion work in shard C.
