# Changelog

## 1.0.1 (2026-10-21)

**Your story bank now helps with applications.** When an application asks "tell us about a time" or "why us," your materials starts from an answer you saved before, matched by meaning (so "a time you pushed back" and "a disagreement with a stakeholder" count as the same question), or builds from the matching story in your story bank. It tells the story the same way the bank does, keeps its "Say carefully" line, and says which answer or story it started from. Saved answers live in `materials/answers.md` with the question, the story, where you've used it, and what to change for the next company. One offer saves the answer and, if it told a story the bank doesn't have yet, adds the story too.

- **Applications and interviews tell the same story.** The interview guide reads what you already wrote to that company, so a story from the application is told the same way in the interview, with more depth. A story's "Used in" line now counts applications, and "I applied to X" records which saved answer and story you sent.
- **A new plugin description** that leads with the fit check and names the story bank.

## 1.0.0 (2026-10-16)

**Clearer file names.** Your `job-search/` folder now reads like what's in it: `search-profile.md`, `looking-for.md`, `job-tracker.csv`, `interview-stories.md`, `contacts.csv`, `resume/`, and `companies/<company>/` with `job-post.md`, `fit-check.md`, and `interview-guide.md`. A 0.4 folder is renamed the first time 1.0 saves something (never on a read-only question like "what's in my pipeline?"), where it can be, and it names each file it renamed. Files you made yourself are renamed only if you say yes, and a profile you wrote yourself keeps its layout; where files can't be renamed from the session, the old names keep working, and it tells you once how to rename them yourself. The tracker gets its two new columns the first time it's updated, and the profile moves to the new section names the first time it's updated; it tells you each time, and what you wrote stays as you wrote it.

**Interview guides that open with the four blocks.** Every guide starts with the role in plain words, your fit, your gaps, and questions to ask, under a one-line verdict and the next round (what it tests, and what it doesn't). Gaps get their own section: what they'll ask, the honest answer, what to point to instead, and whether to raise it first. Below that: a plan for each interviewer, research with sources, scripts for the awkward questions and the pay question, and a method for case rounds.

- **Debriefs and practice.** Debrief right after each round; the guide, the story bank, and the tracker update together, and thank-you notes are drafted. "Practice my interview" plays the interviewer, with critique after every answer.
- **Recruiter BFF scores every posting against your one primary resume (and an alternate for a second kind of role), so the scores stay consistent.** It tells you if your resume needs work, and it won't make a new one for every job.
- **Setup starts from your resume,** and keeps a copy in `job-search/resume/` so every tool works from the same version (new versions sit next to the old ones). It drafts your background and proof points, then asks only what's missing. The first scan never waits on anything else.
- **A preferences page you can share** (`looking-for.md`): what you want next, ending in one sentence that makes it easy for people to help. Adapted from Phyl Terry's *Never Search Alone*.
- **Two reads in every fit check:** do you fit what they want, and does the role fit what you want. It checks the posting is still live on the company's site, notes its age, flags possible ghost jobs, and saves the job post and the fit check in the company folder.
- **Sharper scans:** strong, weak, and parked signals; a pickiness setting; exclusions with exceptions; staffing firms and aggregators filtered out; and a source-health line, so "nothing new" never hides "a source broke." A new role at a company you already know shows up with its history instead of disappearing.
- **The tracker, safer and more useful.** Updates match the exact role (a close title asks first, and a finished row is never reused for a new role), rejections only touch applications sent before them, and a general no with several open roles asks which one. A tracker saved from Excel keeps working, dates included. (If Excel saved it as plain CSV and its accents can't be read safely, as on a Mac, you get a clear message to save it as CSV UTF-8 instead of garbled names.) New `closed` status (not a rejection), plus `furthest_stage` and `next_date` columns, added the next time the tracker is written. Follow-ups for active processes only. "What's in my pipeline?" shows a table sorted by what needs doing, and there's a weekly review.
- **Reminders on your days:** follow-ups due, interviews coming up, roles to apply to, and fresh-role links. They read only your files, so they don't need a browser. To reach your folder, a check-in needs two settings you turn on once (Require this computer and Local folder, in the task's Advanced settings; it walks you through them), and then runs while your computer is awake and the Claude desktop app is open. Quitting the app pauses it until you turn it back on. When it runs and can't reach your files, it says so. A scheduled scan flags weak signals like contract roles and ranks them lower instead of cutting them.
- **New skill: your materials.** Resume bullets, summary, LinkedIn headline and About, and written answers, in your voice, with a skeptical review pass. Never invents a number.
- **New skill: contacts.** Matches your LinkedIn connections export to companies you're pursuing, one next move per person, and short give-first drafts you send yourself.
- **Instructions hidden in postings are never followed.** Text in a posting, a page, a job feed, an email, or a file is information. If it asks for something, Recruiter BFF doesn't do it and tells you it was there.
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
