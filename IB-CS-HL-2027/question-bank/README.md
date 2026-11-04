# Unofficial converted practice question bank

`QUESTION_BANK.csv` is the cumulative index, not the full question text. Each row links:

- `questions/<question_id>.json`: prompt and metadata, without the answer key.
- `markschemes/<question_id>.json`: separate preliminary unofficial solution, mark-by-mark criteria, alternative/partial-credit notes and technical verification.
- `records/<question_id>.json`: complete provenance bundle combining the two for internal review.

All practice records are adapted unofficial material in original wording. Source IDs refer to the uploaded historical papers; no new marking criteria are official IB criteria. Python is the selected programming language; SQL remains appropriate for database questions.

The original source records are separate in `extraction/by-paper/<source_id>/questions/`. Source level/paper/marks are historical metadata, not automatic 2027 classifications. Full mapped guide statements and scope are in the syllabus master. B mappings refer to the adapted scoped target and do not certify every part of the original question as examinable.

When a genuinely reused practice has several source references, its source IDs are combined; it is counted once in this index. Other source-text matches are review candidates, not automatic proof of identical context or extra syllabus coverage.

Marking files are preliminary author-verified criteria with coordinator batch integrity, source/solution sampling and executable checks. The later Chunk 4 independent examination/markscheme audit is separate. No full practice examinations have been assembled in Chunk 2.

Resume and current counts: `PROGRESS.md`, `audits/chunk-2/MERGE_STATUS.json`. Only the coordinator runs the approval/merge process. Changed batch hashes require revalidation; `merge_chunk2.py` refuses to merge stale approvals.
