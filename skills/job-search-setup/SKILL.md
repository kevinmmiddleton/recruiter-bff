---
name: job-search-setup
description: >
  Sets up the user's job search, starting from their resume, and builds the searches every
  other Recruiter BFF skill reuses. Use when the user says "set up my job search," "help me
  start a job search," "here's my resume," "what should I search for," "build my saved
  search," or when another Recruiter BFF skill finds no profile yet. Also use for "update my
  job profile," "change my search," "raise my pay floor," "add a company to my skip list,"
  "build my preferences page," "what do I want next," or "update my preferences." Saves a
  private profile (searches, pay, exclusions, background) and, when the user is ready, a
  shareable one-page preferences file.
---

# Job Search Setup

Learn what the user wants and who they are, save it once, and build searches they can reuse. Every other skill reads what this one writes, so do it well, and do it fast: the user should be able to run a first scan within a few minutes.

## Never

- Never invent a number, a tool, a title, or experience. If the resume doesn't say it, leave a visible placeholder like `[from ?% to ?%]` and ask.
- Never upgrade the user's words to sound bigger ("helped with" stays "helped with" until they tell you more).
- Never decide pay expectations, employment status, or work authorization for the user. Record what they choose to say.
- Never make the first scan wait on the preferences page.
- Never save a file with PowerShell's `>` or `>>`: on Windows that writes a format other apps misread. Use the file tool, or Python with `encoding="utf-8"` (`Set-Content -Encoding utf8` if it has to be PowerShell), and read files with `Get-Content -Encoding UTF8`.

## Step 0: Find or create the data home

All of Recruiter BFF's data lives in a `job-search/` folder inside a folder on the user's computer that they connected for this.

1. Find the folder the user connected: in Cowork, a folder on their computer; in Codex, Claude Code, or another coding agent, the folder you're working in. If that folder is `job-search/` itself (it holds `search-profile.md` or `job-tracker.csv`), the user opened Recruiter BFF's folder directly: it's the data home, so read and write its files without the `job-search/` prefix, and adapt every snippet's paths the same way.
2. If no folder is connected, or you can't tell which one is theirs (Cowork on the web or a phone, a Chat conversation, or the Claude desktop app is closed), stop and say: "I can't reach a folder on your computer from here. In the Claude desktop app on your computer, choose Cowork if you see a Chat/Cowork switch, connect the folder you want to use for your job search, and ask again." In Codex or another coding agent, say instead: "I'm not in a folder on your computer. Open Codex in the folder you want to use for your job search, and ask again." Never create `job-search/` in a temporary workspace or start a second one somewhere else; it won't be there next time. In the ChatGPT desktop app, a Work chat with no project works in a folder the app makes for that one chat (a dated folder under `Documents/Codex/`), and the next chat gets a new one, so treat it as temporary: say "This chat doesn't have a folder of its own. Start a new Work chat with a project on the folder you want for your job search (Choose project, then New project, then add the folder), and ask again there. Every chat in that project will find your search."
3. In Codex, check once that Python works (`python3 --version`, then `python --version`, then `py -3 --version` on Windows): the tracker and contacts need it. If none prints a version, tell the user before the first tracker change: on a Mac, run `xcode-select --install` or install Python from python.org; on Windows, install it from python.org or the Microsoft Store. Until then, list tracker changes in your reply so they can be added once Python works.
4. Create `job-search/` there if it doesn't exist. If it's missing but the user talks about an earlier setup, ask whether they connected a different folder last time before starting over.
5. The private profile is `job-search/search-profile.md`; the shareable page is `job-search/looking-for.md`; the resumes live in `job-search/resume/` (`primary.md`, plus `alternate.md` if there is one).

**Folders from 0.4.** A folder Recruiter BFF 0.4 made has an `applications.csv` whose header starts `company,role,location,comp,url,source,status,score`, or a `profile.md` with 0.4's headings (`## Search Targets`, `## Strong-Fit Signals`, `## ATS Board Searches`). Rename its files only when it passes that check and the user asked for something that writes (setup, a new role, an update, a fit check). On a read-only question like "what's in my pipeline?", read the old names and leave them; the rename can happen at the next write. When you rename, tell the user in one line and name each file you renamed ("I gave your job-search files clearer names, and nothing inside them changed: `profile.md` is now `search-profile.md`, and `applications.csv` is now `job-tracker.csv`."). The renames: `profile.md` to `search-profile.md`, `preferences.md` to `looking-for.md`, `applications.csv` to `job-tracker.csv`, `story-bank.md` to `interview-stories.md`, `interviews/` to `companies/`, and inside each company folder `guide.md` to `interview-guide.md`. If a new name already exists, don't overwrite it; ask which to keep.

**Files the plugin didn't make.** If the names match but the files don't pass that check (a profile, story bank, or notes the user wrote themselves, which their own tools or notes may point to), don't rename anything without asking: list each old and new name, say that anything pointing at the old names would stop finding them, and keep the old names if they'd rather. Ask once: if they keep them, add "File names: kept, YYYY-MM-DD" to Offered, and every skill keeps using the names they have. Never restructure a profile the plugin didn't write. Read it as it is, keep the plugin's own lines (the Resume line, Reminders, and Offered) in a short `## Recruiter BFF` section at the end, change only the lines that change, and say what you changed.

**If you can't rename** (the shell can't reach the folder, as in Cowork's cloud sessions, and the file tools can't rename or delete files), don't promise a rename that can't happen. Keep using the 0.4 names for everything: `profile.md`, `applications.csv`, `story-bank.md`, and new company folders under the existing `interviews/`, with the guide saved as `guide.md` (a new `job-post.md` or `fit-check.md` goes in the same folder). Never write a copy under a new name while the old file stays; two copies drift apart. Tell the user once: "I can't rename files from here, so I'll keep using your current file names. Both work. If you'd like the new names, rename these in Finder or File Explorer: `profile.md` to `search-profile.md`, `preferences.md` to `looking-for.md`, `applications.csv` to `job-tracker.csv`, `story-bank.md` to `interview-stories.md`, `interviews` to `companies`, and `guide.md` to `interview-guide.md` in each company folder." Then add a dated line to the profile's Offered section ("Rename list: YYYY-MM-DD") so later conversations use the old names without telling them again.

A profile 0.4 wrote (by the check above) also uses older headings and field names ("Strong-Fit Signals," "ATS Board Searches," "Compensation floor (base)," "Salary expectation to state when asked," and others). Read them as their 1.0 names, and treat a missing Reminders section as "(not set yet)". The first time you write the profile, move it to the 1.0 names using "Upgrading a 0.4 profile" in `references/profile-template.md`: same content, new headings, plus the Resume line and the Reminders and Offered sections. Say so in one line ("I moved your profile to the new section names; what you wrote is the same"). Before writing "(not set yet)" anywhere, look through the whole profile for something the user already wrote that answers it (their own parked or weak signals, a pay floor under another label), and use that.

If `search-profile.md` already exists and the user said "set up my job search," read it, summarize it in a few lines, and ask whether to update it or start over. Never overwrite a profile without asking.

## Step 1: Start from the resume

Ask for one resume first: "Bring your one primary resume: paste it, or tell me which file in your folder it is." If the user already named or pasted one, that's the primary; don't ask again. A PDF or document in their folder is fine; read it directly. Once you have it, ask once: "Are you also aiming at a second kind of role or a different industry, like PM and program manager, or fintech and health? If so, bring that resume too." If they are, take the alternate the same way, and ask which roles it's for. Two at most: one primary, plus one alternate for a second kind of role. Never a resume per posting.

**Resumes already in the folder.** If the folder already holds more than one resume, list them, ask which is the primary and which, if any, is the alternate, leave the rest exactly as they are, and say so in one line. Never suggest deleting or merging the user's files.

**Save them in the job-search folder** once you know whether there's an alternate, so every skill works from the same resumes:

- A file: copy it into `job-search/resume/` with its name unchanged. Copy, never move; the original stays where the user keeps it. If you can't copy files from here (the shell can't reach the folder, and the file tools can't copy a PDF or Word file), skip the copy and make the plain-text copy's first line say where the original is (`_Text of Sam-Okafor-resume.pdf, which stays in Documents, on 2026-10-06_`). Never write the resume's text into a file named `.pdf` or `.docx`.
- Pasted text, or always alongside a file: write a plain-text copy of the resume as given, `job-search/resume/primary.md` for the primary and `job-search/resume/alternate.md` for the alternate, with a first line like `_Copied from Sam-Okafor-resume.pdf (last changed 2026-10-02 09:14) on 2026-10-06_` (the original file's last-changed date and time, so later skills can tell when it's newer than the copy), or `_Pasted in chat on 2026-10-06_` for pasted text. Don't edit or improve it; it's the record of what the user's resume actually says.
- Record in the profile's Resume line which roles each resume covers (the primary covers everything the alternate doesn't).
- Tell the user in one line: "I saved your resume in your job-search folder. Every fit score runs off it, so the scores stay consistent: a 4.6 means the same thing every time." With an alternate: "I saved your resumes in your job-search folder (your alternate for [its roles]). Every fit score runs off the one that matches the role, so the scores stay consistent: a 4.6 means the same thing every time."

**An honest read.** Then give a short, honest read of each resume: what's working, then the weakest spots by name (bullets with no results, bullets that only describe the job, a summary that reads like a timeline, a missing number). If it needs work, say so plainly ("This resume undersells you: three of your Brightloop bullets have no results.") and offer to help strengthen it with `your-materials` once setup is done, and note it; when you write the profile in Step 4, list "Resume help: YYYY-MM-DD" under Offered. Frame the offer as strengthening the resume they have; don't bring up per-job resumes unless the user asks for one. If it's strong, say so in a line.

**An older folder** may have `job-search/resume/resume.md` (from a 1.0 test build) instead of `primary.md`. Read it as the primary, and rename it to `primary.md` the next time you write a resume file. If you can't rename from here, keep using `resume.md`.

From the primary resume (and the alternate, for the roles it covers), draft:

- **Background:** current or most recent title, years of experience, a two-sentence career arc.
- **Proof points:** the 3 to 6 strongest accomplishments, each written outcome first, then how, then scope, with both ends of any number ("checkout drop-off from 32% to 21%, by redesigning the address step, for a 2-million-user store"). Keep each fact with the accomplishment the resume ties it to; a team size from one bullet doesn't belong on another. Where the resume gives no number, keep the outcome in words and add a placeholder. A result the user tells you that isn't on the resume goes in marked "(you said; not on your resume yet)"; it's worth adding to the resume, since that's what a recruiter sees.
- **Likely target titles,** from the arc and the most recent role.
- **Lead-with guidance:** which proof points to put first for which kinds of roles, in cover notes, written answers, and interviews (the resumes themselves stay as they are).

Then show a short summary of what you drafted (five to eight lines, not the whole profile) and ask only what the resume couldn't tell you (a missing result, a number to confirm), three questions at most, including this one: "Anything you'd want to be upfront about in interviews, like a gap, a pivot, or something you haven't done yet?" If the user has no resume handy, ask for the same things conversationally instead.

## Step 2: The search essentials

A few short turns. **Three questions at most in one message** (each question in a multiple-choice form counts); five at once is too many to answer well. Ask what the first scan needs first (location, pay floor, and what to cut; the titles are confirmed from your summary), then the rest. If the user wants to get going, size, stage, weak and parked signals, and companies to watch can wait until after the first scan. Use the AskUserQuestion tool for multiple-choice parts where it helps; if it isn't available, ask in plain text with numbered choices.

**What they want:**
- Confirm the target titles (the words postings actually use) and seniority.
- Location and work mode: city or metro; remote, hybrid (how many days), on-site. Anywhere they won't go?
- Pay: their base floor. Comfortable and ideal numbers are optional; take them if offered. Most postings don't list pay, and that never counts against a role. Then: "When a recruiter asks what you're targeting, what do you say?" Record their words as their pay line, or "(not set yet)" if they'd rather decide later. Never write it for them.
- Company size and stage, if they care: size bands and stage (Series B or later, public, and so on). Industries they like go here too, under Company, not under strong signals.

**What to cut, and what to flag:**
- Functions to exclude, with exceptions written in. Ask: "Anything that's close to what you do but not it?" Write it as "data science PM out, growth analytics in." Exclude the function, not the whole field.
- Industries to avoid. Company types to skip: staffing firms and job aggregators that repost other companies' roles are excluded by default; say so and let them turn it off. They stay excluded unless the profile explicitly says to include them; a blank line or "(none stated)" keeps the default.
- **Strong signals:** what makes a role top-tier for them ("growth or retention work at a consumer subscription company"). Propose them from the resume and their targets, and let them correct, rather than asking cold.
- **Weak and parked signals** (optional, one question): "Anything that isn't a dealbreaker but makes you hesitate (like contract roles, or titles that turn out to be sales), or a kind of role you like but keep stalling in?" Weak signals get flagged and ranked lower, never cut. Parked lanes still show up, below the strong ones, with a note.

Keep it light. If the user is impatient, titles, location, floor, and exclusions are enough to scan. Everything else fills in later.

## Step 3: Build the searches

A saved search is a job-board URL with the user's filters built in, so a scan can reuse it.

- **LinkedIn search URL:** build it from their answers. See `references/building-a-saved-search.md` for the parameters and worked examples. Show the link in your save message (Step 4), so the user can say if anything's off without a turn of its own.
- **Or capture one they already use:** they set filters on any board, copy the address bar, and paste it. Save it. One good search is usually enough. Add a second only for a title or a place the first misses ("product lead" next to "product manager," or a second city); a keyword added to the same title mostly brings back the same roles. Label each.
- **Company job site searches:** lots of roles get posted straight to company job sites (Ashby, Greenhouse, Lever, and others) and never reach LinkedIn. Build one-click Google searches limited to those sites and to recent posts, using their titles and location. They're free and run in the user's own browser. See `references/ats-search-links.md` for how to build them; typically one for their city and one for remote. Show the links.
- **Companies to watch** (optional): "Any companies you'd jump at?" Scans check their public job feeds directly.

## Step 4: Save, then scan

Write `job-search/search-profile.md` using `references/profile-template.md`. Fill every field you captured and mark the rest `(not set yet)`.

Then, in plain words:

> "Saved. I'll use this for scans, fit checks, and interview prep, and you can change anything by telling me. Want me to run your first scan now?"

On yes, hand off to `find-jobs`.

## Step 5: The preferences page (offer it once, on its own)

Offer the shareable page once, at a quiet moment, following "Ending a reply" (logging an application is the usual one), or when the user asks what to do next. Check the profile's **Offered** section first, and add "Preferences page: YYYY-MM-DD" when you offer it, so no skill offers it twice. If the user asks for it, build it any time.

> "One more thing worth doing this week, when you have half an hour: a one-page 'what I want next' you can share with people who can help. It ends with one sentence that makes it easy for anyone to keep an eye out for you. Scans work fine without it, and they get sharper with it."

On yes, read the profile first, so you confirm what it already knows (size, stage, industries, location) instead of asking again. Then run the conversation in `references/preferences-template.md`: what they'd hate, the bad-boss question, flipping must-nots into must-haves, what they love (and what they're good at but don't enjoy), the company questions with the subject test ("would you care about this every day?"), goals, the one sentence, and the homework of sharing it with three people. Write `job-search/looking-for.md` and link it from the top of `search-profile.md`.

When the page turns up something the scan should use (a must-not, a company size, a subject they'd never work in), add it to the profile's exclusions or signals too, and say so.

## Step 6: Reminders (offer once, on its own)

At a quiet moment, never stacked with another offer (often once the user has something in the tracker):

> "Want me to check in on the days you pick, with follow-ups that are due, interviews coming up, and links to fresh roles?"

In the Codex CLI, or anywhere this session can't create scheduled tasks, offer it as: "Want a short check-in each day you open Codex here, with follow-ups that are due, interviews coming up, and links to fresh roles?"

Check the profile's Reminders status and **Offered** section first; don't offer reminders to someone who already has them, already asked for them, or already said no. When you offer, add "Reminders: YYYY-MM-DD" to Offered. On yes, hand off to `job-search-automation` to set them up.

## Updating later

For a one-field change (raise the floor, add a skip-list company, add an exception), read `search-profile.md`, make the change, write it back, and say what changed. Don't rerun setup. If the change belongs on the preferences page too, update both.

**A restated search.** When the user describes their whole search again, change only what differs. Something they didn't mention isn't removed unless they say so: keep it, and say in one line what you kept ("I kept retention and your four strong signals; say if any should go").

**A new resume.** When the user shares an updated resume, ask whether it replaces the primary or the alternate, unless that's obvious. Add the new file to `job-search/resume/` next to the old one (never overwrite or delete the old file; if they share a name, first add the old copy's date to its name, like `sam-okafor-resume-2026-10-02.txt`) (if you can't copy files from here, skip that, as in Step 1), replace `primary.md` or `alternate.md` with the new text, update the profile's Resume line with the date (add it under the title if the profile has none, as 0.4 profiles don't), and offer to refresh the proof points from what changed. Say in one line that fit scores from now on use the updated resume, and earlier scores used the old one. Two at most: for a third kind of role, ask which one it replaces. Never keep a resume per posting.

## Ending a reply

End with at most one offer. If several apply, pick the first that fits:

1. **Anything time-sensitive:** thank-you notes the same day, a reply someone is waiting on.
2. **Someone to ask before applying:** after a fit check that says apply, if the user knows someone there (from `contacts.csv`), offer the referral note; if there's no `contacts.csv` but a LinkedIn export is in the folder, offer to check it. A referral matters most before the application goes in.
3. **The obvious next step for what the user just did:** after setup, a first scan; after a scan, adding matches to the tracker (or a fit check on a strong one); after a fit check, adding the role to the tracker (once per role; skip it if the role is already tracked); after a booked round, the interview guide if that company doesn't have one yet, otherwise a practice run; after building the preferences page, drafting the message to share it.
4. **Checking the user's LinkedIn export** for people they know, in general. If there's no export in the folder, offer once to walk them through requesting one (LinkedIn usually sends it within about 10 minutes; the steps are in the contacts skill), then move on.
5. **The preferences page.**
6. **Reminders.**

Logging an application or another status change has no next step of its own (a booked round is the exception: see 3). That reply is the quiet moment for 4, 5, and 6. A reply that carries out something the user just said yes to (a contacts import, a draft, the preferences page) doesn't add a new optional offer; at most it ends with that task's own next step from 3.

Before offering 4, 5, or 6, check the **Offered** section of `job-search/search-profile.md` and skip anything already offered; when you offer one, add a dated line there. For reminders, also skip them if the profile's Reminders status is anything other than "(not set yet)" or missing. Saying a fact ("this read uses your profile alone") isn't an offer.

## Principles

- **Ask once, reuse everywhere.** A few extra minutes here saves the user repeating themselves for months.
- **The resume does the first draft.** The user corrects; they don't fill in forms.
- **The words postings use.** Real target titles, not a category.
- **What to cut matters as much as what to find.** A precise exclusion removes more noise than any keyword adds.
- **Plain language with the user.** Say "your search" and "your preferences," not file names, unless they ask.
