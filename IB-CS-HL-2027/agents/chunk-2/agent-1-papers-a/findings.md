# Processor A — completed Chunk 2 shard

Checkpoint: A-C2-FINAL-20261104, 2026-11-04. Author verification complete; coordinator review and authoritative integration remain separate. All writes are confined to this specialist folder. No master files, gap-filling questions, full examinations or Chunk 3 outputs were written.

All eight assigned papers are processed. The 52 durable JSON batches contain 369 source leaves, 1,090 original inventory marks and 272 distinct local unofficial practice questions. Source classification: A 155, B 118, C 96. One additional B source reuses an existing question outside this shard, giving 273 linked A/B source leaves. No source remains assigned to this processor.

| Source | Leaves | Source marks | Local practices | A | B | C | Batches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SRC-001 | 33 | 100 | 27 | 18 | 9 | 6 | 5 |
| SRC-005 | 35 | 100 | 28 | 22 | 6 | 7 | 5 |
| SRC-008 | 34 | 100 | 28 | 20 | 8 | 6 | 5 |
| SRC-018 | 37 | 100 | 28 | 19 | 9 | 9 | 5 |
| SRC-024 | 26 | 70 | 18 | 11 | 7 | 8 | 4 |
| SRC-030 | 30 | 100 | 22 | 11 | 12 | 7 | 4 |
| SRC-034 | 87 | 260 | 60 | 25 | 35 | 27 | 12 |
| SRC-042 | 87 | 260 | 61 | 29 | 32 | 26 | 12 |

Both old Paper 2 sources include every question from all four options. Each option independently sums to 65 marks; 260 is the all-option inventory total, not the original candidate's mark total or a 2027 paper format.

## Durable deliverables and verification

- `batches/SRC-xxx-bNNN.json`: separate source leaves and rewritten, self-contained unofficial practice records, exact-code mappings, full syllabus guidance, specific solutions and marking criteria.
- `papers/SRC-xxx/paper_audit.json`: leaf trees, counts, original marks, completeness and next action. Complete source-page rasters are under `papers/`; each source record links its entire parent question's page evidence and the unchanged original PDF.
- `source-pages/SRC-xxx/page-NNN.txt`: complete page text for the seven text-readable sources. All 336 marked leaf intervals were reconstructed from the original PDFs with matching leaf counts and original mark sequences. Earlier compressed notes remain explicitly labelled `original_text_manual_synopsis`; they are not presented as exact source wording.
- SRC-001 is image-only. All nine pages were visually read, including the blank fourth page. Its manual leaf transcription and linked full raster remain authoritative; it is not labelled an exact OCR extraction. Code, tables, figures and shared stems are retained by complete page evidence. Handwritten annotations are excluded from official content.
- `checks/FINAL_SAVED_SHARD_CHECK.json`: final tests run against the actual saved JSON after prose edits. All 39 Python programs and saved executable solution fields pass their supplied tests; both SQL answers execute correctly in SQLite; both constructor-only answers execute with the specified signatures. All practice mark sums, IDs, exact guidance strings, source-evidence paths and source/markscheme SHA-256 hashes pass.
- `verify_saved_shard.py` reproduces those checks. `finalize_evidence.py` reproduces the final evidence links, explicit source defects and targeted editorial repairs. Do not regenerate raw authoring scripts over the reviewed JSON without subsequently applying all coordinator corrections, exact-source enrichment and final checks.

Prose was reviewed and corrected for fused words. SQL identifiers, Python identifiers and string literals are preserved. The former SQL spacing regression in P-SRC034-Q01-e is repaired: `FirstName` and `InvoiceDate` execute with the matching prompt schema. Adapted command terms agree with the prompts, including Sketch for P-SRC008-Q12-c-ii, Construct for P-SRC024-Q13-b-ii and State for P-SRC042-Q10-f. Original source commands are retained separately.

## Coordinator consistency resolutions applied

- SRC-008 Q7, SRC-018 Q9 and SRC-030 Q2(b), which require virtual-memory paging, are C. Generic OS memory guidance is not used to manufacture a paging requirement; their former practice copies were removed.
- SRC-030 Q9(c)(i) is B, with `adaptation_reuse_question_id` set to `P-SRC028-Q09-c-i`. It maps A2.1.2 for the adapted cloud-infrastructure benefit only. No separate local copy or original backup-technique coverage is claimed.
- SRC-018 Q11(f) remains C for remote-work social impacts.
- B mappings explicitly identify adapted-practice scope. `assessed_concepts` describes the original source skill; a rewritten prompt does not establish that the original question directly assessed the new objective.
- OOP methods that merely traverse or update existing objects use applicable B2/B4 operations. B3.1.4 is reserved for actual class/object construction, constructor invocation or assessed initial state.
- P-SRC018-Q14-c initializes the extremum from a complete row total or an unset marker. A single element is not a safe bound for row sums. P-SRC030-Q13-c and remaining affected prose use “if and only if”.

## Source defects preserved and corrected in unofficial answers

Specific records contain `source_issues` and corresponding markscheme notes, including:

- SRC-011 p15 Q14(b): a square-root bound is invalid for the shown simple proper-divisor sum without paired factors. The adaptation traverses proper candidates and is tested.
- SRC-014 p14 Q12(b): the static-stack full test is off by one for TOP as occupied index. The adaptation uses the correct boundary. The same markscheme's CPU-cache/disk-cache conflation is not copied.
- SRC-019 p6 Q7: a CPU can read ROM; the contrary source alternative is not copied.
- SRC-025 pp15–16 Q13(c): sentinel extrema with `if/else-if` can miss the minimum, and integer division can destroy the fractional mean. The adaptation uses safe initialization, independent comparisons and true division. Overstated VPN/WEP security alternatives are not imported elsewhere.
- SRC-037 Q1(e): inconsistent date-field naming/reserved table naming is replaced with a new consistent schema and executed SQL. Q17(c) p34 has faulty lexicographic comparison logic; primary-score, secondary-stock, negative-value and tie counterexamples pass the repaired solution. Q18(b) p35 uses a forward algorithm suitable for a singly linked log.
- SRC-042/SRC-043 Q1(b): the source narrative permits multiple departments while its STAFF table holds one DepartmentID. The adaptation explicitly specifies one home department. Q1(d) uses consistent query identifiers and executed SQL.
- SRC-043 p9 Q3(a)(ii): completed age requires a birthday adjustment. The unofficial algorithm compares month and day.
- SRC-043 p14 Q5(f): the original cross-midnight AND condition is impossible, and the night-total identifier changes. The adaptation uses OR and counts included observations; boundary/negative/constant cases pass. Agent C independently cross-checked this question read-only.
- SRC-043 Q8(d): unsupervised learning is distinguished by unlabelled training, not claims of randomness or deeper learning.
- SRC-043 Q14(f): a method absent from the source class is not added to the required UML answer. Q16(d): the fixed 2^16 Unicode claim is not copied.
- SRC-042 Q17: the purported alphabetically ordered linked-list figure is not ordered, and the Java constructor contains an invalid parameter. The adaptation explicitly starts from a sorted list and uses Python.

The original PDFs and original answers are unchanged; all new answers remain preliminary unofficial marking criteria.

## Limitations and next action

SRC-001 has no uploaded corresponding official markscheme. Its 27 practice answers are independently authored and tested where executable; they must not be labelled official. Its source is image-only and therefore retains a manual-transcription status.

The canonical SRC-005 is complete. The coordinator's `audits/chunk-2/ALTERNATE_SOURCE_CHECK.json` and inventory identify SRC-047 as the same examination with an omitted printed blank page 4; no marked question is missing and the examination was not processed twice.

No unresolved mapping flag remains within this shard, but B conversions and C exclusions remain reviewable decisions. Counts do not establish whole-syllabus coverage. The coordinator must recheck the current batch snapshot, resolve any cross-shard findings, link the reused P-SRC028 question, merge validated records into the masters and save the Chunk 2 checkpoint. Stop within Steps 4–6.
