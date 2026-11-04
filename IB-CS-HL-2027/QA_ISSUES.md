# QA issues

## Inventory findings

- **C1-SRC-01 — retained duplicate:** SRC-045 is byte-identical to SRC-044 (`Computer_science_paper_2_TZ3_SL.pdf` and its `(1)` alternate). Both originals preserved; process the examination once in Chunk 2.
- **C1-SRC-02 — image-only sources:** SRC-001, SRC-002 and SRC-047 have no usable text layer. Covers rendered and visually read. Chunk 2 requires page-by-page visual/OCR extraction and checking; no questions extracted in this chunk.
- **C1-SRC-03 — incomplete scan warning:** SRC-047 (`Nov 2022 CS HL Paper 1.pdf`) contains 8 PDF pages but its cover declares 9. The same exam code 8822-7011 appears in text-readable SRC-005, which has 10 PDF pages including the copyright page. Exact missing scan page remains to be established before historical extraction; use the more complete source after verification.
- **C1-SRC-04 — missing historical markschemes:** no uploaded matching markschemes identified for SRC-001 (2226-4428, HL Paper 1) or SRC-002 (2226-4429, HL Paper 2). Do not fabricate official criteria or markscheme status later.

## Guide findings

- **C1-SYL-01 — confirmed source code typo:** guide PDF p35 / printed p29 visibly prints `A.1.2.5 Construct logic diagrams.` Store exact `source_code=A.1.2.5` alongside disclosed normalized lookup `A1.2.5`; do not claim the normalized form was printed.
- **C1-SYL-02 — SQL source spelling:** A3.3.4, PDF40 / printed34, lists `AVERAGE`. Visually confirmed and preserved exactly. Future executable SQL must use verified dialect syntax; this source wording is not proof of a callable aggregate with that spelling.
- **C1-SYL-03 — typography normalization:** A4.3.1, PDF42 / printed36, prints r². Master restores the superscript after visual check; raw flattened extraction is retained. No missing mathematical text.
- **C1-SYL-04 — Python implementation calibration:** B3.1.3/B3.1.5/B3.2.1/B3.2.2 use generic OOP wording (access modifiers and static polymorphism). Preserve scope, but implement and mark accurate Python semantics later. B2.4.5 limits code construction/tracing to simple non-branching recursion; B2.4.4 broader conceptual examples do not remove that limit.

## Specimen source findings

All references below are physical pages of `Specimen Papers 2027 - English.pdf`. These are recorded source limitations; required HL inputs are present and readable. Originals are unchanged. No newly authored questions or marking criteria rely on the defective samples.

- **C1-SP-01 — confirmed markscheme code defect:** HL P2 Q12(a), MS PDF84 / component22. Printed `else` aligns with `while`; nonmatching head never advances, and empty input dereferences `None`. Specialist and coordinator independently reproduced bounded nontermination for later/absent targets and the empty-list error. Future answers must be freshly verified; do not copy this code as correct.
- **C1-SP-02 — confirmed Python semantics caution:** HL P2 Q9(a)(ii), PDF56 / component20 and MS80 / component18. A single underscore is non-public convention, not enforced external access control. Specialist/coordinator tests confirm external access. Future wording/marking must make the convention accurate.
- **C1-SP-03 — source ambiguity:** HL P2 Q9(b), PDF57 / component21 and MS80 / component18. Composition is asserted using ticket-price dependence, but ownership/lifetime is under-specified. Future scenarios must state those conditions to distinguish composition from aggregation fairly.
- **C1-SP-04 — unstated-domain limitation:** HL P2 Q11(c)(ii), PDF60 / component24 and MS83 / component21. Recursive sample assumes nonnegative input; original iterative function returns zero for negative integers while the sample does not terminate normally. Independently reproduced. Future prompt must state the intended domain or accept a consistent base case.
- **C1-SP-05 — execution-model caution:** HL P1 Q1(f), PDF5 / component3 and MS24 / component6. Interpret the compiled/interpreted speed comparison within its educational execution model; do not author universal performance claims across all runtimes/workloads.

## Resolution status at Chunk 1 close

No unresolved omission in the 112-statement syllabus or required HL specimen components. All source irregularities are preserved and documented. Historical scan completeness, OCR needs and missing 2026 markschemes remain future processing constraints, not reasons to fabricate evidence. Source interpretation cautions must be revisited when relevant questions are authored in later authorized chunks.

Verification evidence: `audits/SYLLABUS_INTEGRATION_CHECK.json`, `audits/SPECIMEN_INTEGRATION_CHECK.json` and the three specialist findings. No Chunk 2 work performed.


## Chunk 2 — active processing and release checks

- **C2-QA-01 — faithful source extraction:** some initial specialist original_text fields were compressed synopses. Exact source leaf transcriptions and full page/block evidence must be retained separately; summaries are explicitly labelled. Agent C repaired166 earlier leaves with zero extraction fallbacks; A repair pending. Initial batches remain reproducibly snapshotted for revalidation after corrections.
- **C2-QA-02 — authored wording:** fused-word prose and adapted-command metadata inconsistencies are being repaired before full release. Source command terms remain unchanged. Current exact warnings in audits/chunk-2/BATCH_REVIEW.json. No claim all current author batches are final/merged.
- **C2-QA-03 — scope consistency across duplicates:** coordinator harmonized browser/client-server adaptation, generic remote-work social effects, required paging detail and cloud recovery context. B mappings apply to the adapted target and do not certify obsolete parts of original questions. All author corrections require revalidation.
- **C2-QA-04 — duplicate provenance:** byte-identical SRC045 and shorter scanned alternate SRC047 are excluded from processing in favour of canonical sources. Repeated actual questions across different HL/SL/time-zone papers retain separate source IDs and reuse links where verified; text-match candidate groups need contextual confirmation and must not be treated as extra coverage automatically.
- **C2-QA-05 — source answer defects:** specialist-reported source caveats with original question/MS page references are indexed in audits/chunk-2/SOURCE_ISSUES.json. These include unsafe divisor-loop bounds, omitted first inputs, incorrect ROM/power/VPN claims, and faulty extrema examples. They are not imported into authored marking criteria; executed repaired examples have separate tests. The index distinguishes reported source caveats from independently confirmed defects.
- **C2-QA-06 — scanned2026 papers:** both OCR aids are now available and unchanged source pages are rendered/visually checked by the owners. No uploaded official markschemes exist for SRC001/SRC002. All new criteria remain independently authored, unofficial and preliminary. Handwritten annotations are excluded. SRC002 includes contradictory grade boundaries and a negative-recursion premise inconsistent with its printed base case; both are flagged in source records rather than silently treated as correct.

No full examination PDFs or Chunk 3 coverage/gap-filling work has been started.


### Resolved C1-SRC-03 alternate-scan discrepancy

Coordinator rendered SRC047 physical pages2–8 and read printed-page sequence2,3,5,6,7,8,9. The omitted printed page4 is explicitly a blank page in canonical SRC005 physical5. Thus SRC047 omits a blank page, not a historical question; canonical SRC005 still remains the processed version to avoid duplicate extraction. Visual evidence: audits/chunk-2/alternate-scan/contact.png and canonical source-text/SRC005/page005. No question content is missing on account of this shorter alternate.


## Chunk 2 final resolution — C2-FINAL

All 23 selected historical examinations/1,141 source leaves are processed and verified; no missing question content or unresolved mapping remains. C2-QA-01/02/03 source transcription, prose/command and scope consistency repairs are complete in final approved snapshots. Known incidental OOP/dimensionality/ethics over-mappings were repaired. Original MS evidence is separated from adapted-answer fallback. Caught SQL polish regression was corrected and executed successfully before approval. SRC040 exact leaf/mark pages now have separate context provenance; all 21 text-paper mark censuses agree.

C2-QA-04 duplicate detection is retained as 93 normalized text-match candidate groups, with 15 explicit reuse links already consolidated. Other context/skill variants remain separately indexed and do not count as additional syllabus coverage; later paper assembly must avoid redundant selection. This is not an unresolved syllabus mapping.

C2-QA-05 original-source caveats are indexed in audits/chunk-2/SOURCE_ISSUES.json (71 records); originals remain unchanged. Repaired answers are independently tested as appropriate. Two high-risk A/B algorithms received a separate read-only source audit by C. C2-QA-06 has no remaining OCR allocation discrepancy; coordinator inspected every unmatched mark. Missing official markschemes for SRC001/SRC002 remain an availability limitation, explicitly labelled independently authored unofficial criteria.

All current integrity/code/SQL/source-mark checks pass. Preliminary practice marking remains subject to the later Chunk 4 exam-specific audit. No Chunk 3 coverage/gap-filling or full examination PDF work has begun.


## Chunk 3 recovery and first coverage findings

- **C3-RECOVERY-01:** user expected in-progress Chunk 3, but saved files contained only C2-FINAL. No prior Chunk 3 artifacts or live specialists were found. Baseline hash manifest and prior progress are preserved in audits/chunk-3. Three new assigned native specialists are now contributing durable isolated files. No missing unsaved work is claimed recovered.
- **C3-COVERAGE-01:** independent baseline census finds 15 objective codes with no mapped records. Other codes can still have serious scope/command gaps; this count is not the total number of uncovered objectives. See audits/chunk-3/BASELINE_CODE_CENSUS.json.
- **C3-COVERAGE-02:** B1.1.4 has a supporting symbol-purpose explanation but no mapped flowchart trace. Do not count it as full statement coverage. Coordinator independently checked guide PDF44 and full P-SRC009-Q04 prompt/answer. Other bounded audit samples: audits/chunk-3/COORDINATOR_COVERAGE_SAMPLES.json.
- **C3-TEXT-01:** historical author criteria contain occasional spacing defects (e.g. P-SRC005-Q01 solution “express es”; P-SRC044-Q04-e prompt “store24”). These are discovered prose defects, not yet a technical answer failure. Keep historical files unchanged until a concrete correction is logged and reviewed; check any selected paper material before assembly.
- **C3-BANK-01:** no saved searchable-bank feature specification was found. User was asked asynchronously for additions. Proceeding with stated assumptions: search, exact scope/topic/theme/level/difficulty/marks filters, separate answer reveal, provenance references, selected student export without answers. UI/feature verification is pending; Chunk 3 cannot be declared complete yet.

- **C3-SCOPE-OVERRIDE:** later detailed user instruction replaces draft-paper work with permanent database/search infrastructure. No examination, topic-test or PDF generation is authorized this chunk. Detailed scope saved at audits/chunk-3/USER_CHUNK3_SCOPE.md; all three specialists informed. Earlier assumed feature list C3-BANK-01 is superseded by that specification. Full per-question mapping/bullet review (all 823), persistent DB, pasted-scope search and granular verification/usage metadata are now explicit gates.


<!-- C3-REVIEW-STATE-START -->
### Current individual-review queue and reported issues

- 154/823 per-question reviews saved with valid current hashes; 27 coordinator-approved versions; 669 individual reviews remaining.
- 31 reported issue entries, all still explicit unresolved findings unless a later repair log says otherwise. Scope approval does not clear marking/technical issues.
- Full durable queue: `audits/chunk-3/FULL_BANK_REVIEW_QUEUE.csv`.
- Exact question IDs, issue details, author paths and review limits: `audits/chunk-3/REVIEW_ISSUES.json` and each specialist review.
- Historical prompts/criteria remain preserved. Do not present a reported ambiguity as an unconditional code defect; read its domain qualification.
<!-- C3-REVIEW-STATE-END -->


### Search-system review findings and repairs

- Exact-ID keyword search originally returned all823 candidates in the first persistent UI. Coordinator reproduced in browser; developer repaired equality/keyword narrowing; coordinator retest returns exactly P-SRC001-Q03.
- Coordinator required literal guidance validation before any verification mutation, current-review replacement with history, idempotent unchanged imports, authoritative approved-snapshot withdrawal handling, and separation of reviewer rationale that may disclose answers. Saved backend regression tests and browser checks determine final status; do not infer all feature gates passed merely from this list.
- Legacy C2 author/batch verification remains preserved in the original index column. New C3 per-dimension statuses are separate; import defaults pending and no confidence is invented.
- Per-record taxonomy and conceptual-query breadth remain review areas. Command-based question-type fallbacks are labelled inferred, not approved classifications. Curated concept aliases are discovery/routing aids, never evidence by themselves.

- **C3-SEARCH-PRECISION-01 — repaired canonical code:** independent developer audit identified unsafe concept equivalences (encapsulation/hiding, generic for/counted, generic while/pre-test, slope-intercept/whole regression). Coordinator removed them in question-bank/search/bank_db.py and added8 precision regression cases; all8 plus23 functional tests pass. Arbitrary-phrasing semantic recall still incomplete. Developer source is a preserved pre-coordinator revision; canonical installed code is now authoritative.
