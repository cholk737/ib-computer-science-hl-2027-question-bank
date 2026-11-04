# Historical source extraction

`HISTORICAL_MANIFEST.csv` / `.json` define the 23 distinct selected source examinations and fixed round-robin shard ownership. SRC045 is a byte duplicate of SRC044; SRC047 is an alternate scan of SRC005 that omits only a blank page. Originals remain unchanged.

`HISTORICAL_QUESTION_INDEX.csv` indexes one record per marked leaf subquestion, including obsolete material. Detailed source text, context, original marks, original command, source/MS locations, code and figure evidence are stored in `by-paper/<source_id>/questions/<source_question_id>.json`. Some linked original code is Java or pseudocode; that is source evidence, not the language of generated practice.

Every old subject option is extracted. Consequently an old HL Paper 2 has 260 total source marks across four 65-mark alternatives, and SL has 180 across four 45-mark alternatives. Those totals verify extraction completeness and are not a proposed 2027 examination format.

`OBSOLETE_QUESTIONS.csv` retains excluded records and specific scope reasons. Classification D is reserved for a later statement-level gap assessment; it is not an invented historical source record. No original gap-filling questions are authored in this chunk.

Full source-page text/renders are linked as evidence. A synopsis is explicitly labelled separately from faithful transcription; diagrams and code require visual review. OCR aids for the two 2026 scans are not official text or a substitute for original-page inspection. There are no uploaded markschemes for those two papers; unofficial solutions remain independently authored and labelled.

Coordinator verification and cumulative merge evidence are in `audits/chunk-2/`. Per-paper author audits and immutable batch handoffs remain in the corresponding isolated specialist folder. Read `PROGRESS.md` for the exact next authorized action.
