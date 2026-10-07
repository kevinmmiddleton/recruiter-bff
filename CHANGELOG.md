# Changelog

## 1.0.0 (unreleased)

**Clearer file names.** Your `job-search/` folder now reads like what's in it: `search-profile.md`, `looking-for.md`, `job-tracker.csv`, `interview-stories.md`, `contacts.csv`, `resume/`, and `companies/<company>/` with `job-post.md`, `fit-check.md`, and `interview-guide.md`. A 0.4 folder is renamed automatically the first time you use 1.0; nothing inside the files changes.

**Interview guides that open with the four blocks.** Every guide starts with the role in plain words, your fit, your gaps, and questions to ask, under a one-line verdict and the next round (what it tests, and what it doesn't). Gaps get their own section: what they'll ask, the honest answer, what to point to instead, and whether to raise it first. Below that: a plan for each interviewer, research with sources, scripts for the awkward questions and the pay question, and a method for case rounds.

- **Debriefs and practice.** Debrief right after each round; the guide, the story bank, and the tracker update together, and thank-you notes are drafted. "Practice my interview" plays the interviewer, with critique after every answer.
- **Setup starts from your resume,** and keeps a copy in `job-search/resume/` so every tool works from the same version (new versions sit next to the old ones). It drafts your background and proof points, then asks only what's missing. The first scan never waits on anything else.
- **A preferences page you can share** (`looking-for.md`): what you want next, ending in one sentence that makes it easy for people to help. Adapted from Phyl Terry's *Never Search Alone*.
- **Two reads in every fit check:** do you fit what they want, and does the role fit what you want. It checks the posting is still live on the company's site, notes its age, flags possible ghost jobs, and saves the job post and the fit check in the company folder.
- **Sharper scans:** strong, weak, and parked signals; a pickiness setting; exclusions with exceptions; staffing firms and aggregators filtered out; and a source-health line, so "nothing new" never hides "a source broke." A new role at a company you already know shows up with its history instead of disappearing.
- **The tracker, safer and more useful.** Updates match the exact role, rejections only touch applications sent before them, and a general no with several open roles asks which one. New `closed` status (not a rejection), plus `furthest_stage` and `next_date` columns, added the next time the tracker is written. Follow-ups for active processes only. "What's in my pipeline?" shows a table sorted by what needs doing, and there's a weekly review.
- **Reminders on your days:** follow-ups due, interviews coming up, roles to apply to, and fresh-role links. They read only your files, so they run reliably while the Claude app is open.
- **New skill: your materials.** Resume bullets, summary, LinkedIn headline and About, and written answers, in your voice, with a skeptical review pass. Never invents a number.
- **New skill: contacts.** Matches your LinkedIn connections export to companies you're pursuing, one next move per person, and short give-first drafts you send yourself.
- **Fixed:** marking one role rejected could mark every role at that company with the same first word; follow-up flags no longer nag about cold applications.

## 0.4.1 (2026-10-06)

- **Fix: the first status update no longer wipes an empty tracker.** If you logged "I applied" before the tracker had any rows, the update step could rewrite `applications.csv` with no header at all. It now keeps the header row whether or not the file has rows yet.

## 0.4.0 (2026-10-06): Recruiter BFF

- **New name.** Job Search Agent is now Recruiter BFF: a recruiter that works for you. The GitHub repo moved to `kevinmmiddleton/recruiter-bff`, and old links redirect.
- **New look.** The brand kit lives in `assets/brand/`: logo, app icon, favicon, and colors. The README uses the new logo, with a white version for dark mode. Five share banners (link preview, GitHub, wide, square, portrait) live in `assets/brand/banners/`.
- **Your files stay put.** Everything still lives in your `job-search/` folder. Nothing moves when you switch.
- **Switching from Job Search Agent:** uninstall Job Search Agent first, then install Recruiter BFF. With both installed, both answer "scan for jobs."

## 0.3.0 (2026-06-22)

- One-click Google searches limited to company job sites (Ashby, Greenhouse, Lever, and more), filtered to recent posts. Free, in your own browser, no API.

## 0.2.0 (2026-06-11)

- Scored evaluations: every posting rated 1 to 5, each requirement mapped to your background, with an apply-or-skip verdict.
- A story bank that interview guides reuse.
- Watchlist companies pulled straight from their public job feeds.
- A clear promise about your data: your files are yours, and updates never touch them.

## 0.1.1 (2026-06-11)

- Added the license field and a `.gitignore`.

## 0.1.0 (2026-06-04)

- First release: setup, on-demand scans, a CSV tracker, interview guides, and optional scheduled scans.
