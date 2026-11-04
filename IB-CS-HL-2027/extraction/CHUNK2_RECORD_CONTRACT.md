# Chunk 2 record and handoff contract

All files refer to paths relative to IB-CS-HL-2027 unless absolute paths are explicitly given. Read AGENTS.md, syllabus/SYLLABUS_MASTER.json (full guidance), specimen/SPECIMEN_ANALYSIS.md and QA_ISSUES.md. Exactly three processors, no further delegation. Agents write only their assigned agent folder; coordinator writes masters. Immutable source PDFs unchanged.

## Batch format

Save immutable `batches/SRC-001-b001.json` etc in the agent folder, in batches of approximately 5–10 marked leaf subquestions. Use atomic writes. Each batch contains `source_id`, `batch_id`, `source_questions` array and `practice_questions` array. Tell coordinator when ready. After any correction, report the exact batch and correction; coordinator will revalidate. Save `findings.md` and per-paper `paper_audit.json`. Continue all assigned papers; do not stop at one batch/paper unless input is genuinely unavailable. Preserve checkpoints even when not finished.

## Source question record (one per marked leaf subquestion)

- `source_question_id`: H-SRC001-Q01-a-i (example); stable, unique and based on original numbering. No two records for the same leaf. Include all old options, not only the option a candidate would select.
- `source_id`, `source_filename`, `year`, `session`, `source_level`, `paper`, `zone`, `option` (or empty), `question`, `subquestion`.
- `source_pdf_pages`: array of one-based physical source PDF pages; `source_printed_pages`: array of printed page labels. Preserve exact source reference, not a guess.
- `original_marks`: integer; `command_term`; `original_text`: full source leaf transcription; `parent_context`: stem/context required to interpret it. Store lengthy shared context separately and reference it if needed. Do not publish long source text as a practice question.
- `assets`: array of asset records with `kind`, `description`, `path`, `source_pdf_page`, `visually_verified`. Preserve code/tables in source text or separate exact files, and save full source-page renders/crops for diagrams. A page reference without actually inspecting a visual is not sufficient.
- `assessed_concepts`: array of specific skills; `difficulty`: low/medium/high (analyst estimate).
- `markscheme`: object with `status` (uploaded_official_available / not_uploaded), `source_id`, `filename`, `pdf_pages`, `question_reference`, `marking_summary` (accurate paraphrase of relevant points), and any `source_issues`. Inspect the actual source MS; do not invent page refs. Missing MS does not prevent independently solved unofficial criteria but must remain explicit.
- `relevance_status`: A (direct within-scope concept), B (usable with changed scope/structure/language), C (no supported requirement). D represents a later coverage-gap need; do not attach D arbitrarily to historical questions or perform Chunk3 gap-filling.
- `mappings`: array of objects `syllabus_code`, `scope_evidence` (exact relevant guidance excerpt or bullet locator), `rationale`, `theme`, `level`, `confidence` (high/medium/low), `review_required` boolean. Use valid master codes only. C normally has no mappings and has an explicit exclusion reason. Partial relevance needs clear scope separation. Content mentioned in a scenario is not necessarily assessed.
- `exclusion_reason` (C); `uncertainty_flags` array; `verification`: explicit source/marks/code/visual checks, not generic assertions. Uncertain scope stays review-required; never guessed as verified.

## Adapted practice record (separate from source)

- `question_id`: P-SRC001-Q01-a-i; `source_question_ids`: array; `derivation_status`: adapted_unofficial; `unofficial`: true.
- `question_text`: genuinely rewritten prompt/scenario, self-contained with all needed data/diagrams/code. Preserve supported reasoning depth; avoid superficial name/number substitutions. Do not copy whole official papers or retain old option instructions.
- `syllabus_codes`, `theme`, `level`, `marks`, `command_term`, `difficulty`; `adaptation_rationale`: what was retained/changed/excluded and why.
- `solution`: concrete correct full answer; `marking_points`: array of {`marks`:integer, `criterion`:specific credit}; `acceptable_alternatives`, `partial_credit_notes`, `common_errors` as useful.
- `verification`: object with technical reasoning/source comparison; executable Python/SQL checks and result file when relevant; manual reproducible traces acceptable for non-code. Marking-point marks must sum to allocation, or explicit alternative points/caps must be machine-accountable. Do not replace actual answers with generic 'award for correct response' templates.
- `code` / `test_code` / `assets` as required. Only Python executable programming code; faithful pseudo-code/source Java may remain in source-only records. Do not add unsupported advanced requirements. B2.4.5 recursion code simple/non-branching only. No blanket built-in bans; explicit restrictions only when needed to assess an algorithm.
- `markscheme_status`: preliminary_unofficial_verified_by_author. Detailed criteria stored separately on coordinator integration. No claim of official status.

All resolvable A/B questions should get a practice record. Hold uncertain/defective records for review with exact reason rather than producing unsupported answers. Obsolete C records must retain complete source metadata and exclusion rationale. Future bank may contain repeated underlying skills, but report actual duplicated source content and do not count copies as extra coverage.

## Per-paper audit

Save `papers/SRC-001/paper_audit.json`: expected question/subquestion tree established from the PDF; every leaf ID/marks; sum of ALL options separately (not candidate selected max), printed candidate total/rules; source physical/printed page sequence; missing/unreadable content; visuals/code checked; associated MS checks; batch filenames; last completed and next exact leaf. `complete=true` only if all source leaves extracted/classified, all mappings resolved or explicitly held, and usable conversions/criteria saved and checked. Save checkpoint and findings after every batch and finished paper.

The coordinator reviews batches, independently samples evidence and technical checks, resolves flags and merges all validated batches cumulatively. No full exam PDFs, coverage audit/original gap-filling, or Chunk3 work.
