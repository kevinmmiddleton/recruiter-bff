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

## Step 0: Find or create the data home

All of Recruiter BFF's data lives in a `job-search/` folder in the user's Cowork working folder.

1. Find the working folder Cowork can write to.
2. Create `job-search/` there if it doesn't exist.
3. The private profile is `job-search/search-profile.md`; the shareable page is `job-search/looking-for.md`; the resume lives in `job-search/resume/`.

**Folders from 0.4.** If `job-search/` still has 0.4's file names, rename them before anything else, then tell the user in one line ("I gave your job-search files clearer names; nothing inside them changed"): `profile.md` to `search-profile.md`, `preferences.md` to `looking-for.md`, `applications.csv` to `job-tracker.csv`, `story-bank.md` to `interview-stories.md`, `interviews/` to `companies/`, and inside each company folder `guide.md` to `interview-guide.md`. If a new name already exists, don't overwrite it; ask which to keep.

If `search-profile.md` already exists and the user said "set up my job search," read it, summarize it in a few lines, and ask whether to update it or start over. Never overwrite a profile without asking.

## Step 1: Start from the resume

Ask for the resume first: "Paste your resume, or tell me which file in your folder it is." A PDF or document in their folder is fine; read it directly.

**Save it in the job-search folder,** so every skill works from the same version:

- A file: copy it into `job-search/resume/` with its name unchanged. Copy, never move; the original stays where the user keeps it.
- Pasted text, or always alongside a file: write `job-search/resume/resume.md`, a plain-text copy of the resume as given, with a first line like `_Copied from Sam-Okafor-resume.pdf on 2026-10-06_`. Don't edit or improve it; it's the record of what the user's resume actually says.
- Tell the user in one line: "I saved a copy of your resume in your job-search folder, so fit checks and interview guides all work from the same version." 

From the resume, draft:

- **Background:** current or most recent title, years of experience, a two-sentence career arc.
- **Proof points:** the 3 to 6 strongest accomplishments, each written outcome first, then how, then scope, with both ends of any number ("checkout drop-off from 32% to 21%, by redesigning the address step, for a 2-million-user store"). Keep each fact with the accomplishment the resume ties it to; a team size from one bullet doesn't belong on another. Where the resume gives no number, keep the outcome in words and add a placeholder.
- **Likely target titles,** from the arc and the most recent role.
- **Lead-with guidance:** which proof points to put first for which kinds of roles.

Then show a short summary of what you drafted (five to eight lines, not the whole profile) and ask only what the resume couldn't tell you, including one question: "Anything you'd want to be upfront about in interviews, like a gap, a pivot, or something you haven't done yet?" If the user has no resume handy, ask for the same things conversationally instead.

## Step 2: The search essentials

One or two turns, a few questions at a time. Use the AskUserQuestion tool for multiple-choice parts where it helps; if it isn't available, ask in plain text with numbered choices.

**What they want:**
- Confirm the target titles (the words postings actually use) and seniority.
- Location and work mode: city or metro; remote, hybrid (how many days), on-site. Anywhere they won't go?
- Pay: their base floor. Comfortable and ideal numbers are optional; take them if offered. Most postings don't list pay, and that never counts against a role. Then: "When a recruiter asks what you're targeting, what do you say?" Record their words as their pay line, or "(not set yet)" if they'd rather decide later. Never write it for them.
- Company size and stage, if they care: size bands and stage (Series B or later, public, and so on).

**What to cut, and what to flag:**
- Functions to exclude, with exceptions written in. Ask: "Anything that's close to what you do but not it?" Write it as "data science PM out, growth analytics in." Exclude the function, not the whole field.
- Industries to avoid. Company types to skip: staffing firms and job aggregators that repost other companies' roles are excluded by default; say so and let them turn it off.
- **Strong signals:** what makes a role top-tier for them ("growth or retention work at a consumer subscription company").
- **Weak and parked signals** (optional, one question): "Anything that isn't a dealbreaker but makes you hesitate, like contract roles or titles that turn out to be sales? And is there a kind of role you like but keep stalling in?" Weak signals get flagged and ranked lower, never cut. Parked lanes still show up, below the strong ones, with a note.

Keep it light. If the user is impatient, titles, location, floor, and exclusions are enough to scan. Everything else fills in later.

## Step 3: Build the searches

A saved search is a job-board URL with the user's filters built in, so a scan can reuse it.

- **LinkedIn search URL:** build it from their answers. See `references/building-a-saved-search.md` for the parameters and worked examples. Show the user the link and confirm it.
- **Or capture one they already use:** they set filters on any board, copy the address bar, and paste it. Save it. More than one saved search is fine (broad and narrow); label each.
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

Check the profile's Reminders status and **Offered** section first; don't offer reminders to someone who already has them, already asked for them, or already said no. When you offer, add "Reminders: YYYY-MM-DD" to Offered. On yes, hand off to `job-search-automation` to set them up.

## Updating later

For a one-field change (raise the floor, add a skip-list company, add an exception), read `search-profile.md`, make the change, write it back, and say what changed. Don't rerun setup. If the change belongs on the preferences page too, update both.

**A new resume.** When the user shares an updated resume, add the new file to `job-search/resume/` next to the old one (never overwrite or delete the old file), replace `resume.md` with the new text, update the profile's Resume line, and offer to refresh the proof points from what changed. Versions for different kinds of roles ("my growth version") sit side by side in the same folder, each named so the user can tell them apart; the profile lists them.

## Ending a reply

End with at most one offer. If several apply, pick the first that fits:

1. **Anything time-sensitive:** thank-you notes the same day, a reply someone is waiting on.
2. **Someone to ask before applying:** after a fit check that says apply, if the user knows someone there (from `contacts.csv`), offer the referral note; if there's no `contacts.csv` but a LinkedIn export is in the folder, offer to check it. A referral matters most before the application goes in.
3. **The obvious next step for what the user just did:** after setup, a first scan; after a scan, adding matches to the tracker (or a fit check on a strong one); after a fit check, adding the role to the tracker (once per role; skip it if the role is already tracked); after a booked round, a practice run; after building the preferences page, drafting the message to share it.
4. **Checking the user's LinkedIn export** for people they know, in general.
5. **The preferences page.**
6. **Reminders.**

Logging an application or a status change has no next step of its own. That reply is the quiet moment for 4, 5, and 6. A reply that carries out something the user just said yes to (a contacts import, a draft, the preferences page) doesn't add a new optional offer; at most it ends with that task's own next step from 3.

Before offering 4, 5, or 6, check the **Offered** section of `job-search/search-profile.md` and skip anything already offered; when you offer one, add a dated line there. For reminders, also skip them if the profile's Reminders status is anything other than "(not set yet)." Saying a fact ("this read uses your profile alone") isn't an offer.

## Principles

- **Ask once, reuse everywhere.** A few extra minutes here saves the user repeating themselves for months.
- **The resume does the first draft.** The user corrects; they don't fill in forms.
- **The words postings use.** Real target titles, not a category.
- **What to cut matters as much as what to find.** A precise exclusion removes more noise than any keyword adds.
- **Plain language with the user.** Say "your search" and "your preferences," not file names, unless they ask.
