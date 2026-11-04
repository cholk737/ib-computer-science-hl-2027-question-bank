"""Refresh handover entry points after real private GitHub publication."""
from pathlib import Path
import json
import os

P=Path(__file__).resolve().parents[1]
R=P.parent
H=R/'CLAUDE_HANDOVER'


def write(path,text):
    temp=path.with_name(path.name+'.tmp');temp.write_text(text.strip()+'\n');os.replace(temp,path)


def main():
    source=P/'audits/handover/GITHUB_PUBLICATION.json'
    if not source.exists():return
    publication=json.loads(source.read_text())
    if publication.get('created') is not True or publication.get('private') is not True:return
    url=publication['repository_url'];releases=url+'/releases/latest'
    steps=f'''# How to hand this project to your other Claude account

Private repository: [{publication['repository_full_name']}]({url}). It contains the actual project files and preserved Git history. Keep it private. All826 questions are present:823 adapted questions and3 original Python questions, with separate answers and marking criteria. Creating MORE original questions is explicitly required by the included instructions.

## Recommended: download the complete handover

1. Sign in to GitHub as **ityou3**, then open the repository above. Your Claude account can be different; GitHub still needs an account allowed to access this private repository.
2. Open [the latest release]({releases}). Under **Assets**, download **IB_CS_HL_2027_COMPLETE_CLAUDE_HANDOVER.zip** when listed. The release ZIP includes the actual data, source PDFs, database, all instructions and a full Git-history bundle. If the release is not listed yet, use the already verified local ZIP supplied with this handover, or the repository's Code → Download ZIP for the working files.
3. Unzip it. Open **CLAUDE_HANDOVER/00_READ_FIRST.md**. The actual working project is in **CLAUDE_HANDOVER/PROJECT_FILES/IB-CS-HL-2027/**.
4. Start **Claude Code** using the account you want to continue with. Open **CLAUDE_HANDOVER/PROJECT_FILES/** as its project root, so it can read the root CLAUDE.md and the nested IB-CS-HL-2027 working project. Use an environment that can read/write the project folder and run Python; a repository link in an ordinary chat does not by itself provide that execution access. [Official Claude Code quickstart](https://code.claude.com/docs/en/quickstart).
5. Open **CLAUDE_HANDOVER/RESUME_PROMPT.md**, copy its full text, and paste it into Claude. It tells Claude to read actual data/progress, preserve IDs, work as ONE AGENT, finish Chunk3 and create more verified original questions, including genuine Python code-writing tasks.
6. Claude should first confirm the saved counts and current checkpoint from files, then continue work. The starting bank is826 questions, but later runs must inspect actual counts instead of assuming it never grows. Save after every2–3 questions, update progress, and commit. No examinations/topic tests/PDFs during Chunk3; do not start Chunk4/5 automatically.

## Alternative: clone the repository

If Git is already authenticated for your private repository:

```sh
git clone {url}.git
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
'''
    write(H/'HANDOVER_STEPS.md',steps)
    write(P/'HANDOVER_STEPS.md',steps)
    status=f'''# GitHub repository and handover status

Private repository created and initial full project/history push completed: [{url}]({url}). The first verified pushed commit was `{publication['first_pushed_commit']}`. Current exact final commit and privacy/push verification are recorded in the generated REPOSITORY_STATUS.json and GitHub branch state; do not substitute this earlier milestone for the latest branch.

Use [HANDOVER_STEPS.md](HANDOVER_STEPS.md) for the simple transfer process. The complete downloadable archive is published under [Releases]({url}/releases) after its bundle, contents and relocated database pass verification. Earlier source notes describing unavailable GitHub creation are historical; the signed-in Chrome and GitHub CLI flow subsequently succeeded. No credentials or authentication configuration is included in the handover.
'''
    write(H/'GITHUB_REPOSITORY.md',status)
    write(H/'REPOSITORY_SETUP.md',f'''# Repository and restoration instructions

The private repository is [{url}]({url}). Existing Git history was preserved and pushed; no force-push or disconnected replacement repository was used. Exact latest pushed commit/private verification is in REPOSITORY_STATUS.json. Simple instructions: [HANDOVER_STEPS.md](HANDOVER_STEPS.md).

For normal use, download the complete ZIP from [Releases]({url}/releases/latest), or clone the private repository with your own GitHub authentication:

```sh
git clone {url}.git
cd ib-computer-science-hl-2027-question-bank
```

To restore offline history from the complete handover ZIP:

```sh
git clone ib-computer-science-hl-2027-question-bank.bundle ib-computer-science-hl-2027-question-bank
cd ib-computer-science-hl-2027-question-bank
git log -5 --oneline
```

The bundle is beside00_READ_FIRST in the extracted handover. From a Git clone work in IB-CS-HL-2027/. From the complete ZIP work in PROJECT_FILES/IB-CS-HL-2027/. Re-import with explicit relocated root before serving the database. All48 available source PDFs are included; the2 never-uploaded2026 official markschemes remain unavailable. No required LFS pointers or credentials are included. New Claude execution is one agent without delegation.

The original repository-first full-state preservation commit is26aa6de. Earlier reports that creation/push were unavailable describe the earlier fallback, before signed-in Chrome created this private repository and terminal authentication completed. Do not publish its uploaded source material publicly.
''')
    replacements={
      'GitHub creation/push was unavailable through the available authenticated creation paths; no remote URL is claimed. Keep any later remote **private**, named `ib-computer-science-hl-2027-question-bank`.':f'The private GitHub repository has now been created and the full project/history pushed: {url}. Read HANDOVER_STEPS.md for clear transfer instructions and REPOSITORY_STATUS.json for exact latest publication verification.',
      'no GitHub URL exists at this stage.':f'the private repository is {url}; read HANDOVER_STEPS.md for transfer instructions.',
      'GitHub connector identity authenticated but create-repo capability absent, gh unavailable and browser creation required sign-in; remote creation/push **not completed**. No URL is invented.':f'An earlier attempt lacked upload access. A later signed-in Chrome flow created {url} privately, and GitHub CLI authentication enabled a full-history push. Current exact privacy/commit verification is in REPOSITORY_STATUS.json.'
    }
    for filename in ['00_READ_FIRST.md','CURRENT_PROGRESS.md','DATA_INTEGRITY_REPORT.md']:
        path=H/filename;text=path.read_text()
        for old,new in replacements.items():text=text.replace(old,new)
        write(path,text)
    write(R/'README.md',f'''# ib-computer-science-hl-2027-question-bank

Private, unofficial IB Computer Science HL2027 question bank and complete Claude handover. **[Start with the handover steps](CLAUDE_HANDOVER/HANDOVER_STEPS.md).**

## Transfer to your other Claude account

1. Sign in to GitHub and open [Releases]({url}/releases/latest).
2. Download `IB_CS_HL_2027_COMPLETE_CLAUDE_HANDOVER.zip` under Assets, then unzip it. The archive includes actual project files, database, source PDFs and full Git bundle. The complete working tree is also in this repository.
3. Open the extracted `CLAUDE_HANDOVER/PROJECT_FILES/` folder in Claude Code with your preferred Claude account. For a Git clone, open the repository root instead.
4. Paste [RESUME_PROMPT.md](CLAUDE_HANDOVER/RESUME_PROMPT.md). Claude must work as ONE AGENT, preserve existing IDs, continue Chunk3, and **create more original questions**, including genuine Python code-writing tasks. See [QUESTION_GENERATION_INSTRUCTIONS.md](CLAUDE_HANDOVER/QUESTION_GENERATION_INSTRUCTIONS.md).

Current bank:826 full questions, including823 protected adapted questions and3 original Python questions, with separate answers/preliminary criteria. Chunk3 remains incomplete. No examination generation now. Later Chunk4 independently verifies the bank; later Chunk5 repeatedly generates/ranks distinct papers and creates verified new questions when needed. These stages are documented, not executed here.

Working data: `IB-CS-HL-2027/`. Canonical search: `question-bank/search/`; database: `question-bank/database.sqlite3`. Keep the repository private as requested. Author verification is separate from independent Chunk4 verification. Existing Git history is preserved; no token or login files are committed. See the handover guide and exact generated publication/integrity receipts for verification.
''')
    print('Updated GitHub status and clear single-agent Claude handover steps.')


if __name__=='__main__':main()
