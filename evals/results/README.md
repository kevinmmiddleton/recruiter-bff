# Evaluation results

What has been tested in Recruiter BFF 1.0, what it found, what was fixed, and what hasn't been tested yet. Every name in these runs is fictional.

## Snippet checks (rerun any time)

```
python3 tools/check_snippets.py
```

The tracker and contacts snippets are the plugin's only code, so this runs every one of them, straight from `tracker-schema.md` and `contacts-schema.md`, against sample files in a temporary folder. 94 checks: a fresh tracker from create to rejection; header-only, empty, and missing files (a missing tracker stops instead of starting a new one, and a missing contacts file stops the import unless it's the first); a 0.4 folder that couldn't be renamed (`applications.csv`, `profile.md`); the finished-row fallback; a shorter or longer company name ("Northstar" for "Northstar Learning"); files saved by Excel (the "CSV UTF-8" start mark, kept on save and given to new files; Windows' plain CSV; a Mac's plain CSV with é, ñ, ó, ü, ø, or ß, read directly or through a file tool that turned its accents into replacement characters, which stops with a clear message; Windows' plain CSV through a file tool, which stops without blaming a Mac; bare carriage returns, and a copy whose rows ran together (tracker or `contacts.csv`, with ISO dates, Excel for Mac's own like `10/1/26`, day-first dates, a status word, or a link); a new value that already holds the replacement character, in the tracker or from a contacts export; dates rewritten as `9/15/2026`); file permissions kept on save; a 0.4 tracker's booked dates taken from notes; a prospect that goes straight to a screen with no application date, or a recruiter who reached out first; rejection dates typed as `10/5/2026`; the near-miss rejection title; accented and emoji names with Windows' default encoding; columns the user added; a save blocked because Excel has the file open; and the contacts import (LinkedIn's note lines, near misses, recruiter tags, a rerun, a wrong file).

Added in the round-1 review (Oct 6, 2026) and extended after runs 5 and 6 and the round-2, round-4, and round-5 reviews. Against the snippets as they stood before the round-1 review (`2b95a6b`), 64 of the 94 checks fail, including the two worst bugs the reviewers reproduced: a new role overwriting a finished row at the same company, and a tracker saved from Excel breaking every update. Against the copy run 5 used, 42 fail; against the copy run 6 used, 25 fail (the run-6 snippet bugs below, plus the round-4 and round-5 ones). To count these yourself: `python3 tools/check_snippets.py --rev 2b95a6b` for the first, and `--from <folder>` for a copy that isn't committed (the run-5 and run-6 copies aren't kept in the repo). A setting the older snippets don't have yet is added where it does nothing, so the checks that need it fail instead of stopping the run.

## Simulations (Oct 6 and 7, 2026)

In each run, an agent played Claude in Cowork with the plugin installed, followed the skills as written, and wrote every file into a sample folder. The job seeker is Sam Okafor, a senior product manager in Brooklyn who started out at Maplestone Consulting; the companies are Fernhill, Northstar Learning, Brightloop, Tallyho, and Acme. All fictional.

The snippets really ran in a shell (in run 6, on copies, since that shell couldn't see the folder). There was no browser, no web search or fetch, no scheduled-tasks tool, and no multiple-choice question tool, so every run also tested the skills' fallbacks for missing tools.

| Run | Plugin at | Turns | What it covered | What it found | Fixed in |
|---|---|---|---|---|---|
| 1. Full run | `1c67fd8` | 13 | All eight skills: setup from a resume, a pasted scan, a fit check, "I applied," the pipeline table, an interview guide, a debrief, practice, a LinkedIn headline, contacts, a rejection, reminders, the preferences page | About 30 gaps. Contacts weren't wired into scans, fit checks, or guides. Offers stacked and repeated. No rule for a rejection at a company logged only as a prospect. An old `next_date` wasn't cleared. The reminder prompt listed a prospect at a company that had already said no, and ignored contacts. Setup never asked for the pay line. No layouts for the saved posting and fit check. The no-tool paths were unclear (a paste with no links, no question tool, no web, no scheduler). | `a46f77b` |
| 2. Follow-up | `a46f77b` | 8 | Setup, scan, fit check, "I applied," guide and debrief, a rejection, reminders | 7 gaps. Two offers after a fit check, three after a guide. Skills disagreed on when to offer the preferences page. With no scheduler, the reminder request was lost. A rejection left `date_applied` blank. Sources the user skipped counted as failures. The source tag for pasted results was unclear. An unknown company couldn't be STRONG in one place and could in another. | `b4f7556` (one shared "Ending a reply" rule, an Offered section, reminders saved as "requested, not created yet") |
| 3. Offers and reminders | `b4f7556` | 5 | Setup, scan, fit check, "I applied," reminders | One offer per reply every time. But the preferences page lost to a higher offer on every turn, the LinkedIn export check waited too long, and reminders could be offered twice. | `35c0a49` (referrals before applying, logging an application as the quiet moment) |
| 4. Offer order | `35c0a49` | 4 | The user says yes to every offer: setup, scan, contacts import, referral draft, fit check, preferences page, the message to share it | About 8 small gaps. Setup's scan offer and the share message weren't on the offer list. "Product Manager II" had no level. The referral rule needed "has applied." A reply carrying out an accepted offer had no rule. Adding a role that was already tracked did nothing and said nothing. | `61e20ea` |

Two spot checks ran alongside: the tracker snippets at the new `job-tracker.csv` path (a booked screen leaves `furthest_stage` at applied until it happens), and the contacts import ("Fernhill, Inc." matches Fernhill, "Fernhill Partners" doesn't, past employers are skipped).

### Run 5: upgrading from 0.4 (Oct 6, 2026)

**Plugin at:** the working tree with the uncommitted round-1 review fixes on top of `2b95a6b`, so the 1.0 file names, the resume folder, and the round-1 changes all ran. **Setup:** a 0.4 folder (`profile.md`, `applications.csv`, `interviews/fernhill/guide.md`) whose tracker had been saved from Excel (start mark, Windows line endings, dates like `10/6/2026`); the shell's clock wrong on purpose; the same missing tools as runs 1 to 4.

**9 turns:** "what's in my pipeline" on the upgraded folder; keep a copy of a pasted resume; a screen that happened and a hiring manager round booked; a fit check on a posting with hidden text telling AI assistants to rate the candidate 5 and email the company; "I applied"; a rejection that named the company by a shorter name; reminders on Mondays and Thursdays; a daily scheduled scan; and, in a fresh conversation with no connected folder, "set up my job search."

**What worked:** the renames (one line to the user, the guide in `companies/fernhill/`); the Excel-saved tracker loaded first time and the first write converted the dates and added the two columns; booked versus happened; the prospect-only rejection question; the hidden instructions were caught, reported, and not followed, and the score stayed independent; one offer per reply; the no-scheduler fallback; the no-folder stop, with nothing created.

**What it found (25 items), and what changed after it:**
- **Snippets** (now covered by the checks above): a shorter company name found nothing and the next rule would have added a duplicate rejected row (now CHECK FIRST with the near matches, and no new row until the user confirms); every save made the tracker owner-only (permissions now kept); saves dropped Excel's start mark (now kept); 0.4's booked dates stayed in notes (one clear future date on an active row now becomes `next_date`, and the save says which); the rejection message said "stays applied" right after moving a prospect up.
- **0.4 upgrade rules:** an old-to-new table for profile headings and fields, plus the Resume line; a whole-number score with a fit check in its notes counts as a fit check; a 0.4 company folder with no saved posting builds the guide from what's there; an old guide keeps its content and gains the four blocks on its next update; if the folder can't be renamed, keep the old names that conversation rather than writing a copy; README, CHANGELOG, and release notes now say when each change happens.
- **Scoring:** a floor-only pay anchor; round half up everywhere (4.85 becomes 4.9); the fit check's plain labels are now listed in the rubric's "Label the user sees" column.
- **Scans and scheduling:** staffing firms stay excluded unless the profile explicitly includes them; source names compared without regard to case; the scheduled scan is recorded in the profile with the same "requested, not created yet" fallback; it checks what could run unattended first; a daily scan offers the past-day window; the reminder prompt reads M/D/YYYY dates too.
- **Smaller:** hidden text addressed to AI assistants is left out of the saved `job-post.md`, with one line in its place; the LinkedIn-export offer says what to do when there's no export; a first line for a resume pasted into chat.
- **Not changed:** the version in `plugin.json` (release day) and a stray June build in the plugin folder (the release steps already delete it).

### Run 6: the new Cowork, with file-tool-only access (Oct 7, 2026)

**Plugin at:** the working tree after the round-2 review fixes. **Setup:** the way new Pro and Max Cowork sessions work since Oct 6: the agent reached the user's folder only through file tools (read, write, edit, list), and its shell ran in a separate empty folder, so it couldn't rename files. A 0.4 folder whose tracker had been saved by Excel for Mac as plain CSV; the shell's clock wrong on purpose; the same missing tools as before.

**9 turns:** "what's in my pipeline" on the Mac-saved tracker; the same after the user saved it as CSV UTF-8; a restated search on the 0.4 profile; a fit check with a floor-only pay line; prep for the next round with an old guide and no saved posting; a recruiter screen at "Northstar" (a near match, confirmed); a weekday-morning scheduled scan; weekday reminders; and, in the Chat tab with no folder, "what's in my pipeline."

**What worked:** the 0.4 tracker path; scores recorded in notes; a clean first 1.0 write; most of the profile table, including the staffing default; the floor-only pay score and half-up rounding; the old guide upgraded without a saved posting; CHECK FIRST on the near name; the unattended check on the scheduled scan; reminders without a scheduler; the Chat-tab stop, with nothing created.

**What it found (18 items), and what changed after it:**
- **Snippets** (now covered by the checks above): a file tool turned the Mac file's accents into replacement characters before the snippet saw them, so the Mac stop never fired (it now stops on those too, and the message says to close the file in Excel after saving); the snippets now find the 0.4 names on their own; a prospect booked straight into a screen left `date_applied` blank (the snippet now asks).
- **Renames with no shell:** the skills promised a rename that could never happen. Now they keep the 0.4 names for everything, new company folders included, tell the user once which renames they can do themselves, and record that in the profile; every skill uses whichever name exists, and both scheduled prompts read either.
- **Instructions:** more rows in the 0.4 profile table; a restated search keeps what the user didn't mention and says so; no saved resume means working from the profile and mentioning once that a pasted resume can be saved; the guide engine's posting rule split into two cases, and the new top goes above the old guide, which stays below under "Earlier prep"; after a booked round, the next offer is the guide if there isn't one; a booked date that has passed shows "Ask how it went"; a weekday scan uses past-week links on Mondays; a reminder listed as "not created yet" asks first whether the user set it up; the schema says a file-tool round trip may drop Excel's start mark.
- **Not changed:** the scheduled task's own clock (below) and the version in `plugin.json` (release day).

## Kevin's Cowork test of 1.0.0-rc.2 (Oct 14 to 16, 2026)

A live run of the release candidate in the Claude desktop app, on fictional test folders: install (one upload, account-wide), setup with the resume rule, the first scan in the app's built-in browser (signed in to LinkedIn), the watchlist feeds from Cowork, the tracker, a fit check, the tailor test, a new conversation finding the folder, reminders (created, run with the app open, skipped and paused with the app closed, re-enabled), a scheduled scan, a 0.4 folder upgrade, and cleanup. Every section passed; nothing was lost or overwritten. It produced a 17-item fix list (upgrades on hand-made files, "Currently," the narrow search, question batches, install wording, the display name, the rubric, the Require this computer and Local folder steps, the pause when the app is quit, exact times, the scan prompt's weak-signal rule and "you," and the no-folder fit check). All but the scan's "seen before" list were fixed in Phase 3.

## Run 7: the final simulation (Oct 16, 2026)

Five parts on the fixed skills: upgrades and folders, setup and reminders, the resume-rule scenarios again, the full seven-turn case, and a follow-up on the fixes it found. Details in `run-7-2026-10-16.md`.

## Run 8: the story bank for applications (Oct 21, 2026)

The 1.0.1 change: written answers start from saved answers and the story bank. Seven scenarios in order (save, submit, a repeat question at a second company, a failure question with no story, pay, the tailor decline, and an interview guide that reads the application) plus a cold folder. 54 of 55; the miss was the test's own wording. Five wording fixes went in before release. Details in `run-8-2026-10-21.md`.

## Run 9: unlisted pay scored one way (Oct 24, 2026)

The 1.0.2 fix: a posting with no pay listed scores Logistics 4, never 3. Seven cases on five postings and two profiles (with and without a comfortable number): unlisted pay, a range that reaches comfortable, one entirely below the floor, one that starts below it, a vague posting with no pay, and the same posting scored three times by fresh agents that didn't know what was being tested (4.0, 4.0, 4.0). 32 of 33; the miss was a "score it anyway" that called a role below the floor "strong, apply." A blind run on a New York posting with no range found the ghost-job flag and the new rule disagreeing. Three rubric fixes went in before release, and blind reruns of both cases passed. Details in `run-9-2026-10-24.md`.

## Runs 10 and 11: the 1.0.3 batch (Oct 24 and 25, 2026)

Every known open item fixed before launch, then tested in parallel parts with blind agents wherever a reading could go two ways. Run 10: scans and the new scan history (10a, 60 of 60), fit checks, tracker "PM," and contacts (10b, 55 of 56), story bank, guides, and reminders (10c, 47 of 50), and the full end-to-end case on a new persona (10d, 49 of 55). The fixes after it included the tracker's silent row loss when a copy's rows run together under an intact header, confidential postings excluded, the "unknown company" flag dropped, the scan history recording only what was shown, and Requirements counted first. Run 11 rechecked those: data safety and scans (11a, 41 of 46: the agent repaired a damaged tracker without asking, now an offer with a backup), fit checks, guides, and the story bank (11b, 49 of 51), and a blind recheck of the last fixes (11c, 33 of 34). Code checks went from 94 to 130. Details in `run-10a` to `run-10d` and `run-11a` to `run-11c`.

## Live LinkedIn check (Oct 6, 2026)

A real, signed-in LinkedIn saved search, read through Claude in Chrome. Found: reading the page's text returned only the description of the job open on the right, not the results list. Fixed in `8c40f07`: find the results list, scroll so the cards load, read the list, strip tracking from job links, page with `&start=25`, and keep "N connections work here" as a contacts hint.

## Known gaps

- **Run 7 didn't repeat every run-6 case.** It covered the Phase 3 fixes and the full case, with a shell that could reach the folder. File-tool-only access, a contacts import rerun, and a Mac-saved tracker on one line were last simulated in runs 5 and 6 and are covered by the snippet checks.
- **A scheduled task trusts its own clock.** The reminder prompt takes today's date from the system; in run 6 the shell's clock was wrong. Since 1.0.3 the check-in and the scheduled scan start with the date they're using, so a wrong clock is easy to spot, but nothing corrects it.
- **Excel on a Mac can overwrite an update.** A Mac doesn't lock a file that's open in Excel, so if the tracker is open there during an update and the user saves in Excel afterwards, Excel's older copy replaces the update. README and the tracker skill now tell the user to close it first; not tested.
- **File-tool-only access** was simulated in run 6, not tried in a real Cowork session.
- **Plain-CSV accent detection has limits.** From a Mac's plain CSV, an í still slips through (it reads as the same apostrophe Windows uses), and so does an Ñ, Ö, Ç, or Ä starting a word. A Windows plain CSV read directly with š, ž, or œ inside a word, or a dash or ™ between two words with no spaces, gets asked for one re-save as CSV UTF-8.
- **No Windows run.** The snippet checks simulate Windows' default file encoding and console; nothing has run on a Windows machine.
- **The live Cowork run was on rc.2** (Kevin, Oct 14 to 16). The Phase 3 fixes since then were simulated (run 7), not run live. The shell's clock in Cowork wasn't checked.
- **No browser in any simulation.** The LinkedIn steps were checked once live, not inside a full scan.
- **Run 4's two open items are closed in 1.0.3:** remote-anywhere-in-the-US guidance is in `building-a-saved-search.md`, and the headline reads "9 new roles, 3 of them strong."
