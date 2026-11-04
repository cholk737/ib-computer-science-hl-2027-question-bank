# Source inventory — Step 1 verified

4 November 2026. All 48 original PDFs remain unchanged, and all 48 project copies match original SHA-256 hashes.

- 1 official first-assessment-2027 guide, 67 physical pages (SRC-003).
- 1 official 2027 specimen compilation, 154 physical pages (SRC-048). Required HL papers, Python option, markschemes and case study are present; component ranges in `specimen/COMPONENT_MANIFEST.csv`.
- 46 historical files: 25 question-paper files and 21 markschemes. These represent 23 distinct examination codes; none processed as historical question records.
- 47 unique file hashes overall. SRC-045 is byte-identical to SRC-044.
- SRC-047 is an image-only alternate of examination SRC-005, not an extra source examination. Its cover declares nine pages while the PDF has eight. Prefer the more complete source after question-level completeness checking in Chunk 2.
- SRC-001, SRC-002 and SRC-047 are image-only PDFs. Covers visually verified; future extraction needs OCR/visual verification.
- Uploaded matching markschemes were identified for 21 distinct historical examinations. No matching uploaded markschemes for 2026 HL P1 (SRC-001) or P2 (SRC-002).

`SOURCE_INVENTORY.csv` / `.json` contain stable source IDs, exact filenames, original/project paths, hashes, byte/page counts, cover text, source codes, sessions/levels/papers, identity evidence, pairing and uncertainty notes. Do not infer newer numeric exam-code timezone labels where not explicitly supported: qualifier text in `zone` states filename/paired-source evidence.

Historical metadata checks were confined to inventory/cover availability. No historical question extraction, syllabus mapping, adaptation or marking was begun. Sources are authoritative only in the order in AGENTS.md; historical formats do not define 2027 examinations.
