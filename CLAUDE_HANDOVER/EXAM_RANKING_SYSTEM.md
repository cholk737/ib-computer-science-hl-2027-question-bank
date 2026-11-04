# Future ranking system — Chunk5 only

Use EXAM_QUALITY_RUBRIC.md weights20+15+25+15+10+10+5=100. Only fully verified papers with no critical defects are eligible. Rank by total, then answer correctness, syllabus accuracy and structure. Keep separate Paper1/Paper2 leaderboards, top10 displays without a total-production cap.



Create:

- EXAM_RANKINGS.csv
- EXAM_RANKINGS.md
- TOP_PAPERS.md
- EXAM_QUALITY_RUBRIC.md
- EXAM_INVENTORY.csv
- PAPER_COVERAGE_REPORT.csv

Maintain:

TOP 10 PAPER 1 EXAMINATIONS

TOP 10 PAPER 2 EXAMINATIONS

Each ranking entry should include:

- Paper ID
- Paper type
- Overall score out of 100
- Individual category scores
- Verification status
- Reason for deductions
- Syllabus requirements covered
- Included question IDs
- Question PDF path
- Markscheme PDF path

Sort by total score.

For ties, prioritize answer correctness, then syllabus accuracy, then examination structure.

Only include fully verified papers in the rankings.

Maintain separate recommendations for:

- Best overall Paper 1
- Best overall Paper 2
- Most specimen-like Paper 1
- Most specimen-like Paper 2
- Most challenging Paper 1
- Most challenging Paper 2

## Chunk 5 checkpoint rules

Save every completed paper and markscheme pair immediately.

Update the exam inventory and ranking after each verified paper.

Continue generating new papers in later sessions without rebuilding completed examinations.

Stop when available resources are exhausted or when further output cannot maintain sufficient accuracy and diversity.

Do not promise automatic background continuation.

---
