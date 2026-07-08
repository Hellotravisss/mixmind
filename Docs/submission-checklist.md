# Submission checklist — Track 3 (Unicorn)

## Deliverables
- [ ] **GitHub repo (public)** — code + README. *Pre-screening reads this.* Ready: `src/`, `web/`, `data/`, `Docs/`, `README.md`.
- [ ] **Slide deck (PDF)** — `web/deck.html` → open in browser → File ▸ Print ▸ Save as PDF. *Pre-screening reads this.*
- [ ] **Demo video (≤3 min)** — record per `Docs/demo-script.md` (screen-record, no camera).
- [ ] **Live demo URL (recommended)** — the published `web/index.html` artifact URL, or deploy to Vercel/GitHub Pages. *Pre-screening reads this.*
- [ ] Confirm AMD compute is evident in repo + deck (`Docs/amd-evidence.md`) — **hard requirement, or disqualified.**

## Before making the repo public — confidentiality (hard rule)
- ✅ `PLAN.md` and `CLAUDE.md` are **git-ignored and untracked** (they hold internal strategy / the employer name). Verify: `git ls-files | grep -iE "plan.md|claude.md"` → should print nothing.
- ✅ `private/` is git-ignored.
- ✅ Scan tracked text files for the sensitive terms (keep the actual term list OUT of this repo — see the private `PLAN.md` red-lines section for what to grep). Result must be empty.
- Never commit: employer name, plant address, real recipe kg amounts, internal product names, the internal tool's URL.
- Public identity is one line only: "a machine operator at a North American precast plant."

## Push steps (when ready)
```bash
git add .
git commit -m "MixMind — plant-private concrete-mix AI on AMD"
# create a NEW public repo on GitHub, then:
git remote add origin <your-repo-url>
git push -u origin main
```
Re-run the confidentiality scan above **after** `git add .` and once more before `git push`.

## Runbook check (repo must run for a reviewer)
- `pip install -r requirements.txt`
- `PYTHONPATH=src python -m mixmind.demo --stub` → strength model trains (R²≈0.91) + copilot/committee structure prints (no GPU needed).
- Full brain: on the AMD box, `python -m mixmind.demo` (or `python -m serve`).
