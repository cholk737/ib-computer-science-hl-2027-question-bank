# Agent 2 — Theme B Syllabus Analyst

Status: complete specialist extraction and verification; coordinator integration/review pending.

## Counts

| Topic | All statements | SL/HL common | HL-only |
|---|---:|---:|---:|
| B1 Computational thinking | 4 | 4 | 0 |
| B2 Programming | 18 | 16 | 2 |
| B3 Object-oriented programming | 10 | 5 | 5 |
| B4 Abstract data types | 6 | 0 | 6 |
| **Total** | **38** | **25** | **13** |

All 90 statement-guidance bullets are retained. Six bullets contain “must include”; five contain “may include” (including the language-specific Java file-class examples). All count as extracted guidance, while only Python is selected for later generated programming work.

## Durable outputs

- `theme_b_scope.csv`: 38-row index with full statement/guidance, classification, page references, derived assessable skills, allowed context, coverage status and substantive record paths.
- `theme_b_scope.json` and `records/B*.json`: full structured statement and bullet records; exact source text is distinguished from derived skills/context. JSON preserves bullet boundaries and level evidence.
- `scope_context.json`: official scope note, Theme B topic-level guiding/linking context and programming/assessment policy excerpts. Linking questions are context, not additional coded learning statements.
- `programming_policy_notes.md`: Python selection, built-in policy, recursion limit, language-specific caution flags and assessment rules with source locators.
- `verification_summary.json`: counts; `second_extractor_verification.json`: independent-extractor text comparisons.
- `extract_theme_b.py`, `verify_theme_b.py`: reproducible extraction/checks; `evidence-pdf-page-44.txt` through `49.txt`: source text evidence; `guide-43.png` through `guide-49.png`: rendered source pages inspected.

## Verification performed

1. Read guide Syllabus Content PDF 43–49 / printed 37–43, including the final continuation page and all topic/section level labels.
2. Rendered and visually inspected every page PDF 43–49. Every statement and bullet was read; no diagrams are embedded in these scope pages.
3. Asserted the exact expected code ranges: B1.1.1–4; B2.1.1–4, B2.2.1–4, B2.3.1–4, B2.4.1–5, B2.5.1; B3.1.1–5, B3.2.1–5; B4.1.1–6. No missing/duplicate codes.
4. Checked B2.4.2 continuation across PDF 45–46; both bullets retained.
5. Checked the individual HL markers on B2.4.4–5, inherited B3.2 heading marker and inherited B4 topic marker. B3.1 and common Big O/search/sort requirements remain included.
6. Compared every exact statement and each of the 90 bullets against a second extractor (`pdfplumber`, independently of `pypdf`) on the cited source pages; whitespace/ligature normalization only for comparisons.

Source transcription normalization: line wraps joined, layout-only spaces collapsed, line breaks after a hyphen or slash removed without removing the printed hyphen/slash. Source wording, punctuation and capitalization are otherwise preserved. The source `(HL only)` suffix remains in the two individually tagged statement texts. Inherited HL labels are separate metadata.

## Checkpoints and limits

- B1 verified: 4 common statements, PDF 44.
- B2 verified: 18 statements, PDF 44–46, including the two explicit HL recursion statements.
- B3 verified: 10 statements, PDF 47, with five inherited HL-only labels.
- B4 verified: 6 statements, PDF 48; final linking-question continuation on PDF 49 saved as context.
- No historical questions extracted/mapped/adapted and no new practice questions created. Coverage is `not_yet_assessed_chunk1`, not a claim of question-bank coverage.

## Issues for coordinator

No missing/unreadable Theme B text. Preserve two interpretation cautions for later question design: generic OOP wording requires faithful Python treatment (particularly access modifiers/static polymorphism); conceptual recursion is broader than the explicitly simple non-branching recursion programming limit. Full details are in `programming_policy_notes.md`. Also, preserve the linking questions exactly as contextual source text rather than silently correcting topic references (for example network communication is referenced as A3 in a B3 linking question).
