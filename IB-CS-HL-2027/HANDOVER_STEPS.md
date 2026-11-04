# How to hand this project to your other Claude account

Private repository: [ityou3/ib-computer-science-hl-2027-question-bank](https://github.com/ityou3/ib-computer-science-hl-2027-question-bank). It contains the actual project files and preserved Git history. Keep it private. All826 questions are present:823 adapted questions and3 original Python questions, with separate answers and marking criteria. Creating MORE original questions is explicitly required by the included instructions.

## Recommended: download the complete handover

1. Sign in to GitHub as **ityou3**, then open the repository above. Your Claude account can be different; GitHub still needs an account allowed to access this private repository.
2. Open [the latest release](https://github.com/ityou3/ib-computer-science-hl-2027-question-bank/releases/latest). Under **Assets**, download **IB_CS_HL_2027_COMPLETE_CLAUDE_HANDOVER.zip** when listed. The release ZIP includes the actual data, source PDFs, database, all instructions and a full Git-history bundle. If the release is not listed yet, use the already verified local ZIP supplied with this handover, or the repository's Code → Download ZIP for the working files.
3. Unzip it. Open **CLAUDE_HANDOVER/00_READ_FIRST.md**. The actual working project is in **CLAUDE_HANDOVER/PROJECT_FILES/IB-CS-HL-2027/**.
4. Start **Claude Code** using the account you want to continue with. Open **CLAUDE_HANDOVER/PROJECT_FILES/** as its project root, so it can read the root CLAUDE.md and the nested IB-CS-HL-2027 working project. Use an environment that can read/write the project folder and run Python; a repository link in an ordinary chat does not by itself provide that execution access. [Official Claude Code quickstart](https://code.claude.com/docs/en/quickstart).
5. Open **CLAUDE_HANDOVER/RESUME_PROMPT.md**, copy its full text, and paste it into Claude. It tells Claude to read actual data/progress, preserve IDs, work as ONE AGENT, finish Chunk3 and create more verified original questions, including genuine Python code-writing tasks.
6. Claude should first confirm the saved counts and current checkpoint from files, then continue work. The starting bank is826 questions, but later runs must inspect actual counts instead of assuming it never grows. Save after every2–3 questions, update progress, and commit. No examinations/topic tests/PDFs during Chunk3; do not start Chunk4/5 automatically.

## Alternative: clone the repository

If Git is already authenticated for your private repository:

```sh
git clone https://github.com/ityou3/ib-computer-science-hl-2027-question-bank.git
cd ib-computer-science-hl-2027-question-bank
claude
```

Sign in to the desired Claude account when prompted; if switching an existing Claude Code session use its `/login` command. Paste the prompt from `CLAUDE_HANDOVER/RESUME_PROMPT.md`. In a clone, the project root contains `CLAUDE.md`, `CLAUDE_HANDOVER/` instructions and `IB-CS-HL-2027/` data; no `PROJECT_FILES` step is needed. If the ordinary Claude GitHub connector cannot see the repository, authorize this specific private repository for that account or use the local-folder route above.

## Short prompt you can paste

> Read CLAUDE.md, the handover CURRENT_PROGRESS.md, NEXT_ACTIONS.md and QUESTION_GENERATION_INSTRUCTIONS.md, then inspect the actual question database and coverage. Continue incomplete Chunk3 as ONE AGENT, with no subagents. Preserve all existing questions and IDs. Create more genuinely original questions for verified syllabus gaps, including actual Python code-construction questions, with separate tested answers and preliminary marking criteria. Integrate them into the searchable bank and checkpoint every2–3 questions. Continue useful work after the initial checks; do not stop at a plan. Do not restart Chunks1/2 or generate examinations/PDFs in Chunk3. Stop at the chunk boundary and report the actual saved progress.

## Optional: open the searchable bank yourself

In Terminal, change into the actual `IB-CS-HL-2027` folder, then run:

```sh
python3 question-bank/search/bank_db.py --db question-bank/database.sqlite3 import --root "$PWD"
python3 question-bank/search/serve_bank.py --db question-bank/database.sqlite3 --port 8767
```

Open `http://127.0.0.1:8767/`. Stop with Ctrl-C. Re-import refreshes file paths after relocation and preserves existing questions/history. Do not rerun the old Chunk2 generators. There are still outstanding scope, wording, marking and semantic-search tasks; this is not a claim Chunk3 or independent Chunk4 verification is complete.
