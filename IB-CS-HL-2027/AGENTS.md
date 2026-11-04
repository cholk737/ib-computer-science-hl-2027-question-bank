# AGENTS.md — IB Computer Science HL 2027 Exam Conversion Project

## 1. Mission

Build a comprehensive, traceable **unofficial** IB Computer Science Higher Level (HL) practice-exam system aligned with the **first-assessment-2027 syllabus**. Start this project **from zero**. Do not import conclusions, progress, or generated work from a previous project unless the user explicitly instructs you to.

Analyse the official 2027 syllabus and specimen, extract historical questions from user-provided past papers, map and adapt those questions to the new syllabus, fill coverage gaps with original questions, then produce realistic HL Paper 1 and Paper 2 practice examinations and separate verified markschemes.

**Order of authority:**
1. Uploaded official 2027 Computer Science guide: defines examinable knowledge, exact learning statements and scope limits.
2. Uploaded official 2027 HL specimen papers: define assessment structure, language options, question types and difficulty benchmark.
3. Uploaded 2027 specimen markschemes: define marking conventions and response expectations.
4. Historical past papers and their markschemes: supply candidate source questions, **not** the new syllabus or examination format.

Keep original source PDFs unchanged. Cite each source question internally by file, session/year, paper, page, question and subquestion. Never invent source references, official questions, syllabus codes, or markscheme status. Label all produced practice papers and new marking schemes **unofficial**.

## 2. Scope: all of HL, not merely HL-only material

Read the guide's **entire Syllabus Content section**, not just the outline or roadmap. Capture every individual learning statement, its exact code, any **HL only** designation, and every accompanying bullet specifying included knowledge, skills, examples, and limits.

- **Theme A — Concepts of computer science:** A1 Computer fundamentals; A2 Networks; A3 Databases; A4 Machine learning.
- **Theme B — Computational thinking and problem-solving:** B1 Computational thinking; B2 Programming; B3 Object-oriented programming; B4 Abstract data types (HL only).

HL includes all applicable SL/HL common content **plus** every HL extension. Do not accidentally omit common requirements. Respect the guide's scope wording: **“must include”** defines included examples used for assessment; **“may include”** supplies non-exhaustive examples and must not be interpreted as an exhaustive list. Preserve the guide's precise scope without broadening an example into an unsupported technical requirement.

For **each** syllabus statement record:
- Exact code and statement text, source page and topic.
- All supporting bullet-point guidance and any scope qualifications.
- SL/HL common versus HL-only classification.
- Assessable knowledge/skills and allowed context.
- Whether and how it appears in question-bank coverage.

If a mapping is uncertain, flag it for review; do not guess. Do not equate a topic heading having questions with each of its learning statements being assessed. An assessment-specific scope sheet supplied later overrides the **topic selection for that assessment only**, while the official guide still defines what the selected topics mean.

## 3. Official examination formats

### HL Paper 1 — Theme A
- **2 hours; 80 marks; all questions compulsory.**
- **Section A: 56 marks.** Theme A SL and HL concepts.
- **Section B: 24 marks.** Questions based on a **pre-seen case study** and its **four HL challenge questions**.
- Use the official HL specimen as the format benchmark. A specimen case study is not automatically the case study for a future real session. For generated exams, use a clearly labelled unofficial practice case study unless the user supplies and explicitly selects an official case study for that purpose.

### HL Paper 2 — Theme B
- **2 hours; 80 marks; all questions compulsory.**
- Use the **Python** version, not Java.
- Assess applicable common and HL-only Theme B content. Include an algorithmic-thinking question that does not require interpreting or writing code, consistent with the guide.
- Follow actual 2027 specimen structure rather than old-syllabus option-paper formats.

Use appropriate IB command terms, difficulty, response depth, mark allocations and representations. If built-in functions are disallowed to assess an algorithm, explicitly say so in the question. Do not arbitrarily ban them elsewhere.

## 4. Four chunks, exactly three steps per chunk

The project is **12 sequential steps**, grouped into **four user-controlled chunks**. The user intends to allocate **one complete Codex five-hour usage window to each chunk**, where their plan permits. **For every chunk, assign three distinct specialist subagents plus the main coordinator** (four agents total) if the active Codex environment supports native subagent delegation. A five-hour window is a reset/usage period, **not** a guarantee of five hours of execution or enough capacity to complete a chunk. Never claim to know remaining credits unless reliable account information is available.

**Chunk 1 — Foundation:**
1. Create the new project structure and inventory all uploaded sources.
2. Extract and verify the complete individual-statement 2027 HL syllabus scope.
3. Analyse both 2027 HL specimen papers and corresponding markschemes.

**Chunk 2 — Historical processing:**
4. Extract individual historical questions, diagrams, marks, command terms and markscheme references.
5. Map each question to exact 2027 syllabus statements and classify its relevance.
6. Adapt relevant questions into unofficial 2027-aligned practice questions and draft verified marking points.

**Chunk 3 — Coverage and draft papers:**
7. Audit every individual syllabus statement and identify coverage gaps and weak difficulty distribution.
8. Write original, technically verified questions and marking points to fill those gaps.
9. Assemble first complete 2027-style HL Paper 1 and HL Paper 2 **student-facing draft** PDFs.

**Chunk 4 — Verification and final outputs:**
10. Produce full separate markscheme PDFs for the draft examinations.
11. Independently audit, repair and recheck all questions, answers, syllabus mappings and PDF layouts.
12. Finalize the PDFs, question bank, audit report and project handover.

**Hard stop:** Only perform the chunk the user explicitly assigns. Do **not** automatically move into the next chunk, even if the current chunk finishes early or allowance remains. If there is extra capacity, perform useful independent checks and improve current-chunk quality; do not manufacture work to exhaust credits. If a chunk cannot finish in one allowance window, resume its remaining work after reset rather than skipping checks.

## 5. Mandatory three-subagent architecture — specific jobs in every chunk

**Requirement:** For **each of the four chunks**, the main coordinator must **launch exactly three specialist subagents**, each with a **different, explicitly named task**. The coordinating agent is **not counted** as one of those three. Therefore, when supported, each chunk uses **four agents total: 1 coordinator + 3 subagents**. Do not replace this with a default of one or two subagents for budget reasons; the user explicitly wants three for every chunk.

**Capability boundary:** This requirement applies when the active Codex environment supports spawning three subagents. If it does not, explicitly report the actual limitation; do **not** claim that three agents were launched. Divide the same three specialist jobs into separate sequential work units, keep their outputs isolated, and request guidance if a native three-subagent setup is required. Do not fabricate concurrency or claim background tasks are still running after the run ends.

### Coordinator responsibilities — apply to all four chunks

- Read `AGENTS.md`, `PROGRESS.md`, project input inventory and existing outputs before assigning work.
- **Spawn 3 distinct subagents** for the current chunk; state each agent's name, goal, inputs, outputs, boundaries and acceptance criteria before delegation.
- Assign **non-overlapping ownership** of input shards, output files and Git worktrees/branches, if supported.
- Schedule work so independent tasks run in parallel; respect necessary dependencies within each chunk instead of forcing premature handoffs.
- Review all three results; independently sample source evidence and mathematical/programming checks; resolve conflicting findings.
- Be the **only writer** to shared master files: `PROGRESS.md`, `SYLLABUS_MASTER.csv`, `QUESTION_BANK.csv`, `SYLLABUS_MAPPING.csv`, `COVERAGE_REPORT.csv`, `QA_ISSUES.md`, and final combined PDFs.
- Merge only validated subagent deliverables into the master project. Record every merge/checkpoint and the exact next task.
- Before declaring a chunk complete, confirm **three distinct subagents actually ran and contributed**, or clearly disclose any unsupported/failed delegation.

### Chunk 1 — Foundation (Steps 1–3): three different specialist jobs

| Subagent | Exclusive assignment | Inputs | Writes only to |
| --- | --- | --- | --- |
| **Agent 1 — Theme A Syllabus Analyst** | Extract and verify **every individual A1–A4 learning statement**, its exact wording, supporting bullet guidance, `must include`/`may include` distinctions, HL-only labels and source page. Identify missing/ambiguous text. | Official 2027 guide, Theme A syllabus pages | `agents/chunk-1/agent-1-theme-a/` (e.g. `theme_a_scope.csv`, `findings.md`) |
| **Agent 2 — Theme B Syllabus Analyst** | Extract and verify **every individual B1–B4 learning statement** and its guidance, exact wording, HL-only labels, programming constraints and source page. Independently check codes and scope. | Official 2027 guide, Theme B syllabus pages | `agents/chunk-1/agent-2-theme-b/` (e.g. `theme_b_scope.csv`, `findings.md`) |
| **Agent 3 — Specimen & Assessment Analyst** | Examine **both official HL specimen papers and their markschemes**. Record the Paper 1/Paper 2 structures, section marks, command terms, question types, Python conventions, case-study rules, mark allocation and assessment depth. Check the syllabus's official examination-format section. | 2027 HL specimen papers, markschemes and guide's assessment pages | `agents/chunk-1/agent-3-specimen/` (e.g. `specimen_analysis.md`, `exam_blueprint.json`, `findings.md`) |

**Coordinator integration:** Set up all folders and inventory the original PDFs (Step 1), launch the above three jobs concurrently where possible, compare their findings against the source pages, merge Agent 1 and Agent 2 into `syllabus/SYLLABUS_MASTER.csv`, and publish Agent 3's verified `specimen/SPECIMEN_ANALYSIS.md`. Count all required syllabus codes; record missing sections; checkpoint and **stop after Step 3**.

### Chunk 2 — Historical extraction, mapping and conversion (Steps 4–6): three separate paper-processing specialists

All three agents do the **same complete pipeline**—extract → map → convert → draft marking criteria—but each owns a **different, non-overlapping subset of historical source papers**. This ensures all three can do meaningful work in parallel rather than leaving one idle while another agent works.

| Subagent | Exclusive assignment | Writes only to |
| --- | --- | --- |
| **Agent 1 — Historical Paper Processor A** | Process assigned **source-paper shard A**: extract every question/subquestion and figure; map to exact 2027 codes; classify A/B/C/D; adapt usable questions into unofficial practice; draft and verify marking points. | `agents/chunk-2/agent-1-papers-a/` |
| **Agent 2 — Historical Paper Processor B** | Process assigned **source-paper shard B** with the same complete pipeline; use distinct paper IDs and stable question IDs; preserve provenance and source markschemes. | `agents/chunk-2/agent-2-papers-b/` |
| **Agent 3 — Historical Paper Processor C** | Process assigned **source-paper shard C** with the same complete pipeline; pay special attention to visual/code questions and source ambiguities; record verification issues. | `agents/chunk-2/agent-3-papers-c/` |

**How to partition work:** The coordinator creates a stable manifest of unprocessed PDFs sorted by unique source ID. Assign papers in round-robin order (1st→A, 2nd→B, 3rd→C, 4th→A, and so on). **Never assign the same paper to multiple agents.** If fewer than three papers remain, divide a paper into **disjoint question-number ranges** with explicit boundaries, while keeping source metadata consistent. Each agent completes extraction, mapping and conversion for **only its assigned papers/ranges**. If some records need later cross-review, the coordinator may request a **separate read-only audit** without changing the original ownership.

**Coordinator integration:** Validate all three batches, independently check a sample from each, reconcile duplicate IDs and inconsistencies, and merge into the master mapping and question bank. Checkpoint every 5–10 questions and every finished source paper. Repeat Chunk 2 in subsequent windows as needed until all intended source papers have been processed. **Never move to Chunk 3 while papers remain unfinished.**

### Chunk 3 — Coverage, new questions and first drafts (Steps 7–9): three distinct specialist jobs

| Subagent | Exclusive assignment | Inputs | Writes only to |
| --- | --- | --- | --- |
| **Agent 1 — Theme A Coverage & Question Designer** | Independently audit each A1–A4 learning statement against the converted bank; identify scope-bullet/difficulty gaps; write and verify **original Theme A practice questions** and provisional marking points to fill the assigned gaps. | Verified syllabus + Theme A question bank | `agents/chunk-3/agent-1-theme-a/` |
| **Agent 2 — Theme B Coverage & Python Question Designer** | Independently audit B1–B4; create original missing **Theme B/Python** questions, verify code outputs, recursion/algorithms/complexity when required, and draft marking points. | Verified syllabus + Theme B question bank | `agents/chunk-3/agent-2-theme-b/` |
| **Agent 3 — Independent Coverage Auditor & Exam Blueprint Designer** | Independently cross-check whole-syllabus coverage, especially HL-only statements; design a mark-accurate **HL Paper 1 and Paper 2 blueprint**, create an **unofficial Paper 1 practice case-study concept**, and report constraints/duplicate or balance issues. **Do not author questions that overlap Agents 1/2.** | Verified syllabus, specimen and existing bank | `agents/chunk-3/agent-3-blueprints-audit/` |

**Coordinator integration:** Compare all three gap assessments, reconcile coverage findings, validate new questions and combine them into the question bank. Then assemble **student-facing draft** HL Paper 1 and HL Paper 2 PDFs using the verified questions and Agent 3's blueprints. Check **Paper 1 56/24** and each paper's **80 total marks**. Save and stop after Step 9; markscheme PDFs are for the next chunk.

### Chunk 4 — Markschemes, independent audit and final publication (Steps 10–12): three distinct specialist jobs

| Subagent | Exclusive assignment | Inputs | Writes only to |
| --- | --- | --- | --- |
| **Agent 1 — HL Paper 1 Markscheme Specialist** | Create the detailed **Paper 1 answer key and markscheme** (including case study and 56/24 division); independently verify technical facts, permitted alternative answers and partial-credit points against the syllabus. | Paper 1 draft, sources and preliminary answers | `agents/chunk-4/agent-1-paper-1/` |
| **Agent 2 — HL Paper 2 Python Markscheme Specialist** | Create the detailed **Paper 2 Python markscheme**; execute/test code where appropriate; verify algorithm traces, data structures, OOP, complexity, alternative solutions, and partial credit. | Paper 2 draft, question bank and Python answer files | `agents/chunk-4/agent-2-paper-2/` |
| **Agent 3 — Independent Exam & PDF Quality Auditor** | Conduct an **independent, read-only audit of both student papers** for exact syllabus coverage, HL level, totals, question ambiguity, PDF layout, missing diagrams/code, and answer leakage. **After** Agent 1/2 deliver drafts, also audit both markschemes for consistency and errors. Report concrete fixes with page/question references; do not silently overwrite authors' artifacts. | Both draft papers, syllabus/specimen, then draft markschemes | `agents/chunk-4/agent-3-independent-audit/` |

**Coordinator integration:** Ensure Agent 3's final markscheme audit is performed **after** the markscheme drafts exist. Resolve audit findings, independently spot-check repaired material, render/inspect final PDFs, publish student papers and separate markschemes, write the handover/coverage report, checkpoint and stop after Step 12.

### Shared multi-agent operating rules

1. **Three subagents per chunk are mandatory when supported**, even if a single-agent run might be cheaper. Each gets a specific non-overlapping job defined above; the coordinator is the fourth agent.
2. Subagents must receive explicit **input file references, excluded responsibilities, owned output path, batch size and validation criteria** in their task briefing.
3. Each subagent saves its own structured result and `findings.md`; a chat-only summary is not a durable deliverable.
4. Never have two agents write the same output file or edit any master CSV simultaneously.
5. The coordinator performs the final authoritative merges and keeps ownership of `PROGRESS.md` and all master records.
6. A check by an independent agent should actually re-examine the relevant source and result, not simply accept the creating agent's conclusions.
7. Use parallel execution for genuinely independent work, but use staged handoffs when downstream tasks require upstream outputs. Maintain **three assigned specialists throughout the chunk**.
8. If one subagent fails, keep its work separate, record the failure and retry its defined shard without losing other agents' results.
9. Record the three subagent assignments and their actual completion status in `PROGRESS.md` for every chunk.
10. Each chunk remains limited to its **three designated steps**, regardless of how many agents are running. The five-hour allowance window is a planning boundary, not a guarantee of sufficient capacity or automatic resumption.

## 6. Historical past-paper extraction and mapping

For every uploaded paper, identify **every question and subquestion**; do not skip diagrams, code snippets, tables, images or small mark allocations. Inspect rendered PDF pages when extracted text misses visual information. Preserve the exact document provenance and which original markscheme is available.

Required metadata:
- Stable internal ID; filename; year; May/November session; time zone if relevant; old paper/option; page; exact question/subquestion.
- Original marks and command term; assessed concepts/skills; relevant source markscheme location.
- Exact 2027 syllabus code(s); Theme A or Theme B; common SL/HL or HL-only; difficulty; relevance status; reviewer/confidence flag.

Classify as:
- **A — Directly relevant:** assessed concept remains within the 2027 scope.
- **B — Adaptable:** partly relevant, but needs updated scope, language or structure.
- **C — Obsolete:** not an examinable 2027 requirement; archive metadata and exclusion reason.
- **D — New coverage required:** no suitable historical question exists for a required learning statement.

Do not infer that old Paper 1 automatically maps to new Paper 1, or that old Paper 2 option content remains in the new syllabus. Check every assessment objective against the **exact learning statement plus guidance**. Mark source records and converted records separately so every generated question is traceable without being mistaken for an original official question.

## 7. Question adaptation and original question creation

- Preserve the assessed reasoning and difficulty of genuinely reusable questions wherever appropriate.
- Remove obsolete content and terminology. Rebuild question structures to suit the **2027 HL specimen**, not the old paper format.
- Use **original wording and scenarios** in practice question deliverables instead of reproducing long copyrighted old-paper passages or entire papers verbatim. Record the original source reference in metadata.
- Use Python for all programming questions. Verify syntax, behavior, output, edge cases and relevant complexity assertions through execution or reproducible tracing when possible.
- Include conceptual understanding, code tracing, debugging, algorithm design, OOP, data structures, and HL requirements **where the individual learning objectives support them**.
- Avoid invented restrictions, obscure tangential material, ambiguous questions and artificial difficulty from unnecessary prose.
- For each generated question, attach stable ID, exact syllabus code(s), level, marks, command term, difficulty, derivation status, source link (if adapted), solution and marking points.
- Write genuinely different questions to fill gaps, not superficial number/name substitutions.

A completed topic has meaningful practice at the individual-learning-statement level, including important scope bullets and a reasonable mixture of difficulty/application. Never claim perfect coverage based solely on question counts.

## 8. Markschemes and verification

Separate student papers from answer keys. For each question supply the correct solution, mark-by-mark criteria, partial credit, acceptable alternatives, and notes about common mistakes when useful. Adapt source marking logic if the question has changed. Do not label AI-created marking criteria as official IB criteria.

Before releasing any question or paper:
1. Verify its complete syllabus statement and scope, including any HL-only tag.
2. Check the command term, expected answer depth and mark allocation.
3. Execute or reliably verify Python code, algorithm traces and outputs; examine edge cases.
4. Check alternate valid approaches and partial-mark consistency.
5. Ensure individual part marks sum to the question and all questions sum to **80** per full HL paper.
6. Check relevant case-study context and the **56/24** Paper 1 division.
7. Render each PDF and inspect every page for clipping, broken figures, code formatting, answer leakage, page breaks and readability.
8. Document and fix failed checks; leave unresolved issues explicitly flagged.

In final materials state that they are **unofficial practice papers**, not IB-issued examination papers. Do not use IB logos or imply endorsement.

## 9. Persistent file structure

Create and maintain this project structure (adapt names only if necessary):

```text
IB-CS-HL-2027/
├── AGENTS.md
├── README.md
├── PROGRESS.md
├── QA_ISSUES.md
├── agents/
│   ├── chunk-1/
│   ├── chunk-2/
│   ├── chunk-3/
│   └── chunk-4/
├── sources/
│   ├── 2027-guide/
│   ├── 2027-specimen/
│   └── historical-papers/
├── syllabus/
│   ├── SYLLABUS_MASTER.csv
│   └── SCOPE_VERIFICATION.md
├── specimen/
│   └── SPECIMEN_ANALYSIS.md
├── extraction/
│   └── by-paper/
├── mapping/
│   └── SYLLABUS_MAPPING.csv
├── question-bank/
│   ├── QUESTION_BANK.csv
│   ├── questions/
│   └── markschemes/
├── coverage/
│   └── COVERAGE_REPORT.csv
├── exams/
│   ├── paper-1/
│   └── paper-2/
├── final-markschemes/
├── audits/
└── scripts/
```

CSV files are **indexes**, not the sole storage for lengthy question text, source evidence, diagrams, and multi-point markschemes. Store substantive question records separately (e.g. JSON/Markdown), identified by stable IDs. Keep full source references, generation status, checks and version history. Add a useful `README.md` describing where to find things and how to resume.

## 10. Checkpoint system and allowance management

Codex allowance can be exhausted mid-task. **Durable files, not chat context, are the source of truth.**

Initialize `PROGRESS.md` immediately. At minimum keep:
- Current chunk and step; exact last completed, verified batch.
- Total number of source papers inventoried, processed and remaining.
- Number of extracted, mapped, adapted, excluded and original questions.
- Completed files with relative paths.
- Unverified results and outstanding `QA_ISSUES.md` entries.
- Next exact file, question ID or action; resume instructions.
- Date/checkpoint identifier and, where applicable, Git commit ID.

**Checkpoint frequency:** At the end of every source paper, every **5–10 questions**, every substantial merge, every phase, and every generated examination or markscheme. Prefer small atomic file writes and safe merges. Commit verified milestones with Git if the workspace permits.

**Before resuming:** Read `AGENTS.md`, `PROGRESS.md`, the relevant indexes, and `QA_ISSUES.md`; check actual files exist; reconcile any incomplete batch; continue at the next unfinished record. Do not silently reprocess or overwrite previously verified batches. If usage ends unexpectedly, resume from the last saved checkpoint; never claim unfinished unsaved reasoning is preserved.

**Full-window policy:** The user may allocate their complete available five-hour usage window to the assigned chunk. Prioritize completeness, independent verification and substantive work **within that chunk**. Do not sacrifice correctness to conserve usage for a later chunk, but do not waste capacity by redundant analysis. Never advance into the next chunk without the user's request. If insufficient allowance, log exact progress and finish the same chunk after the next reset.

## 11. Model and effort guidance (advisory, not self-switching)

The user chooses the Codex model and reasoning level in the app; do not claim to change them unless the environment expressly allows it. Prefer the **strongest efficient coding/reasoning model actually available** for mapping, conversion, analysis and assembly. Use **High reasoning** for first-pass syllabus verification, ambiguous mappings, new HL question design and final auditing; **Medium reasoning** is usually sufficient for systematic extraction and routine adaptation. Low reasoning can suit straightforward metadata extraction if checked afterward. Use a stronger model for difficult isolated QA when available. Do not assume a particular model name or credit cost exists in the user's picker.

Three-subagent delegation may consume allowance faster; this is an explicit user preference for every chunk. Keep assignments bounded and non-overlapping, use checkpoints, and do not waste allowance on redundant work.

## 12. Outputs and phase completion gates

**After Chunk 1:** source inventory; complete verified `SYLLABUS_MASTER.csv` with every learning statement and scope guidance; `SPECIMEN_ANALYSIS.md`; working folders; `PROGRESS.md` updated; explicit list of missing/unreadable source material. **STOP.**

**After Chunk 2:** all *available intended* historical papers processed, or explicit recorded remaining papers if too many for the current window; mapping with uncertainty flags; converted practice questions with preliminary marking points; updated question bank and checkpoint. If papers remain, repeat Chunk 2 after the next reset; do not declare it finished or move to Chunk 3. **STOP.**

**After Chunk 3:** code-by-code coverage report; original gap-filling questions and verified draft answers; first student-facing draft PDFs of complete HL Paper 1 and Paper 2; updated progress. **STOP.**

**After Chunk 4:** detailed separate markscheme PDFs; independently verified and corrected final examination PDFs; technical/visual audit; final coverage report; clear handover and `PROGRESS.md`. **STOP.**

For every completed step, provide a short report with what was done, exact output paths, counts of processed items, verification status, unresolved issues, and the next user-authorized step. Do not report success for files that were not actually created and checked.

## 13. Non-negotiable rules

1. Begin from scratch in this project.
2. Follow the **uploaded 2027 syllabus**, including all individual statements and detailed guidance.
3. Prepare **HL** examinations: all applicable common content plus HL extensions.
4. Use the **2027 HL specimen** as the assessment-style benchmark.
5. Use **Python** for all programming tasks.
6. Preserve and verify historical source references; do not fabricate them.
7. Exclude genuinely obsolete content; record why.
8. Keep official source materials separate from generated unofficial questions.
9. Produce student papers and markschemes separately.
10. Assign exactly **three different specialist subagents in every chunk** (plus the main coordinator) when native delegation supports it; otherwise disclose the limitation and preserve the three separately assigned jobs.
11. Save frequent checkpoints and make every chunk resumable.
12. Respect the user-defined **three-step chunk boundary** even if allowance remains.
13. Never promise automatic background continuation beyond the current Codex run.
14. Never skip source, code or PDF verification to meet an arbitrary window target.
15. Report gaps and limitations honestly.
