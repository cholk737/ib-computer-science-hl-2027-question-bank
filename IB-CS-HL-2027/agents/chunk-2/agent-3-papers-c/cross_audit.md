# Independent, read-only high-risk algorithm audit

Auditor: Historical Paper Processor C, 4 November 2026. Re-read original PDFs/markschemes directly, inspected rendered defect pages, reviewed complete mapped syllabus guidance and independently executed the current adapted code. Evidence and reproducible tests are in `cross-audit-evidence/`, `verify_cross_audit.py` and `cross_audit.json`. A/B outputs and shared masters were not edited.

## SRC-042 Q5(f): overnight temperatures, 8 marks

Original paper `Computer_science_paper_2_TZ3_HL.pdf`, physical PDF 8 / printed 7, defines night 19:00–06:59 inclusive: 12 hourly readings. MS `Computer_science_paper_2_TZ3_HL_markscheme.pdf`, physical/printed 14, uses an impossible conjunction requiring an ordinary 24-hour time to be both at least 19:00 and below 07:00. It also initializes NIGHT_TOTAL but subsequently uses TOTAL_NIGHT. These are real source-example defects. Correct source logic uses OR and a consistent accumulator; a denominator of 12 is valid for the source’s 24 hourly observations.

P-SRC042-Q05-f in Agent A `batches/SRC-042-b004.json` explicitly changes the window to 20:00–05:59. Its OR predicate correctly selects hours 0–5 and 20–23, ten observations. Counting those observations and dividing by that count is correct; retaining the original denominator 12 would be wrong after this adaptation. Extrema initialized from the first observed value work with temperatures beyond the source sample’s arbitrary ±1000 sentinels. The function preserves parallel-list pairing and computes both means after traversal.

Independent tests passed: constant -3000/-4/0/4000 values; boundary hours 0,5,6,7,18,19,20,23; reversed/rotated hour order; mixed negative temperatures; comparison with a separately calculated oracle. Exact B2.2.2 list traversal, B2.3.2 Boolean selection and B2.3.3 loops support the mapping. The explicit min/max/sum restriction is appropriate for the algorithm being assessed.

Verdict: **adapted algorithm correct**. Source-record repair still required at audit time: original_text/context were compressed synopses, assets empty and source_issues empty despite the known defects. The owner should preserve the exact source wording/context and populate these source-evidence fields before integration. Authored fused-word spacing also needs the owner’s final pass.

## SRC-038 Q5(e): repeated-trial percentages, 4 marks

Original paper `Computer_science_paper_2_HL.pdf`, physical PDF 10 / printed 9, requires 10000 games. MS `Computer_science_paper_2_HL_markscheme.pdf`, physical/printed 17, specifies/loops 1000 repetitions but outputs COUNT/100. That divisor is appropriate for 10000 games, not the 1000 actually executed: 1000 wins would incorrectly display 10% instead of 100%. Reusing N for inner and outer loops is also unsafe if mechanically translated without separate loop semantics.

P-SRC038-Q05-e in Agent B `batches/SRC-038-b004.json` generates fresh input/results each trial, reinitializes the per-trial success flag, checks all ten results, increments once per wholly successful game and returns 100*wins/trials. Its local loop variables avoid the source’s index reuse. Exact B2.3.2 selection, B2.3.3 iteration and B2.3.4 functions/modularization support its mapping.

Independent tests passed: 0/100% at one trial, 50% at two, 100/3% at three, all-success trials at 1000/10000, 37.21% at 10000, exact fresh-generator/callback counts, all ten positions containing one False, and failed games following a successful game. No state leaks or denominator errors found. Four marking points match the rewritten task.

Verdict: **adapted algorithm and criteria correct**. Minor wording clarification: specify that trials is a positive integer, not merely positive, matching range(trials). The source issue is already honestly recorded by the owner.
