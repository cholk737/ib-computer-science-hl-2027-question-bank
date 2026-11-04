# Restore history / publish privately later

The existing Git history was retained at workspace root.26aa6de is the repository-first full-state preservation commit. No authenticated creation/push path was available: connector read identity succeeded but exposes no create-repository tool, `gh` absent, browser creation redirected to sign-in. No remote was created and no repository URL is claimed. Final actual commit/bundle status is REPOSITORY_STATUS.json.

To restore full Git history independently of GitHub:

```sh
git clone ib-computer-science-hl-2027-question-bank.bundle ib-computer-science-hl-2027-question-bank
cd ib-computer-science-hl-2027-question-bank
git log -5 --oneline
```

The bundle is at the handover root after packaging. To run from the ZIP alone use PROJECT_FILES/IB-CS-HL-2027 and re-import with explicit relocated root, as in00_READ_FIRST. Do not copy old absolute original-source paths into run commands; all48 available project-copy source PDFs are included with relative paths. Both missing2026 source markschemes were unavailable originally and cannot be restored from this archive.

For later GitHub publishing, sign in, create an EMPTY **PRIVATE** repository named `ib-computer-science-hl-2027-question-bank` with no new README/license/history. Confirm private visibility. In the restored root run `git remote add origin <actual-private-repository-URL>` (or set-url an existing remote only after checking it), then `git push -u origin main`. Do not publish publicly. Do not force-push over unrelated history. Verify the remote default branch points to the final local commit and remains private. User supplies actual authenticated credentials; no secrets are included. No LFS required: current required file contents are included and each file is below90MiB. The ZIP and its nested Git bundle are excluded from the repo to avoid recursive archives; handover instructions and actual project files are committed.
