# Changelog

## 1.1.0 (unreleased)

**Recruiter BFF now runs in Codex.** Install it with two commands, start a Codex chat in a folder for your job search, and say "set up my job search." That folder is your search's home, and everything works the same way: the fit check, interview guides, the story bank, scans, the tracker, contacts, and your materials. It works in Codex in the ChatGPT desktop app and in the Codex CLI, and best on a paid ChatGPT plan: tested on GPT-6.1 Sol, every workflow held and repeated runs agreed, while the free plan's model got scans and fit checks wrong about half the time.

- **Scans in Codex:** in the ChatGPT desktop app, Codex reads your saved LinkedIn search in its built-in browser after you sign in there once. In the Codex CLI, you paste the results in. Watchlist feeds load when Codex's network access is on, and the scan says so when it's off.
- **Reminders in Codex:** in the ChatGPT desktop app, check-ins and scheduled scans are Codex scheduled tasks, set up from a plain-words request like the Claude ones. In the Codex CLI, which can't schedule anything, you get a check-in the first time you open Codex in your folder each day, or a calendar reminder you add with one click.
- **Windows:** files are saved in a format other apps read correctly, even from PowerShell, and the skills use no characters that garble there.
- **Opening Codex inside `job-search/`** works too: it's treated as the data home, not a place to start a second one.
- **Interview guides** keep a half-given interview time as "not given" and ask once, instead of guessing.
- **The same score every time.** Two tie-breakers in the fit check: a skill that's only listed on your resume is a partial match for a posting that asks for strength in it, and a company in a field your background covers scores 4. The same posting now scores the same in Claude and in Codex.
- **Scans skip less by accident.** Every scan runs its steps in order; a source it can't reach says why (never "checked" from a web search); "show them" leaves out roles that no longer fit your rules. An example in the scan rules named a company, which led a real Codex run to keep a role below the floor; the examples are neutral now.

## 1.0.4 (2026-10-24)

From an outside tester's second round in Codex, on Windows:

- **Scans notice when LinkedIn changes your saved search.** LinkedIn sometimes redirects a saved search into its newer AI-powered search and changes it on the way (a different area, a pay filter, a different date window, or results no longer newest first). Scans now compare the page's filters to your saved link, name each change in the source line, and tell you how to scan with your own filters: set them back on the LinkedIn page, then paste the results.
- **"I applied" remembers your saved answer.** If you saved an answer written for that company, applying notes its story as used in that application, and tells you in one line so you can correct it.
- **"Starting at $X" never counts as below your floor.** It only shows the bottom of the range, so the role stays, with a heads-up.
- **A save that's blocked says why.** It's usually the file open in a spreadsheet app, or marked locked or read-only; if not, the session may not be allowed to write to that folder, and the plugin now says so instead of assuming Excel. A folder the session can't write to now gets that message instead of an error.
- **"I applied to Fernhill" with one Fernhill role tracked** updates that role and names it, so you can correct it, instead of asking which one.
- **Checks:** 132 code checks.

## 1.0.3 (2026-10-24)

**Scans remember what they've shown you.** A role a scan showed you, that you didn't add to your tracker, no longer comes back as "new." Scans keep a small `scan-history.csv` in your folder, hold those roles back with a count ("Also held back: 3 shown in an earlier scan"), and list them if you say "show them." A role still posted a month after you last saw it comes back once, tagged "Shown Oct 24, still open." A near match ("Senior Product Manager, Platform" next to "Senior Product Manager") is never held back. Scheduled scans read the history and add what their digest showed.

**Your tracker can't lose rows to a damaged copy.** If a copy of `job-tracker.csv` or `contacts.csv` comes back with rows run together (or a value with a stray comma), the plugin now stops instead of saving a copy that drops rows. It says which row looks wrong and how to fix it, and offers to fix it for you, saving a backup copy first; it never repairs the file without your yes.

- **Confidential postings are out.** A posting that hides the company ("Confidential," "our client") is excluded by default, in scans and at the fit check's gate. A profile line ("include confidential postings") turns them back on. The "unknown company" flag is gone; when it matters, the reason line says it can't tell what a company does.
- **"PM" means your kind of PM.** The tracker and scans read "PM" as product, project, or program manager, from the roles in your profile. If you look at more than one kind, it asks which role you mean.
- **Contract roles aren't mistaken for staffing firms.** Contract or contract-to-hire is a soft warning, never a reason to hide a role.
- **"I applied" starts your tracker** if you don't have one yet, and "do you track somewhere else?" is asked once per conversation at most.
- **Fit checks score more consistently.** Requirements are counted first (one partial is a 4, one real gap is a 3), and a role stopped at the gate gets its files saved, marked with the rule it failed, with no offer after.
- **Scans read cleaner.** Every skipped source says why, a "Promoted" card is kept, and the headline reads "9 new roles, 3 of them strong."
- **Saved searches** include Group, Principal, and Lead PM roles (LinkedIn often tags them Director), with guidance for remote anywhere in the US.
- **Story bank and guides:** a story needs its lesson before it's banked, and "add this to my story bank" works; two matching saved answers never get mixed; an answer written after a guide adds a line to that guide; guides are checked against your own files before saving, and the chat reply stays short.
- **Older folders:** drafting something in a 0.4 folder no longer renames your files.
- **Contacts in your own field are tagged `same-role`,** whatever your field.
- **Reminders start with the date they're using,** so a wrong clock is easy to spot.
- **Checks:** 130 code checks (up from 94).

## 1.0.2 (2026-10-24)

- **Fixed: missing pay is scored one way.** The fit check's rules disagreed about a posting that doesn't list pay: the Logistics scale gave it a 4, and the general "unknowns score 3" rule gave it a 3, enough to move an overall score across a tier (3.5 to 3.4). Now, when location and work mode fit, unlisted pay always scores Logistics 4, with or without a comfortable number in your profile, and never lower. Posting quality still gives a 4 instead of a 5 when pay isn't listed. Found by an outside tester running Recruiter BFF in Codex.
- **Fixed: a missing range where the law requires one.** In places like New York that require a pay range, a posting without one gets a one-line heads-up to check the company's own posting, and its scores stay the same as any other unlisted pay. Before, the rules could read it either way, enough to change the verdict.
- **Fixed: "score it anyway" keeps the skip.** When a role fails one of your hard rules (say, the whole pay range is below your floor) and you ask for a score anyway, you get the number, and the verdict still says skip and names the rule it failed.

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
