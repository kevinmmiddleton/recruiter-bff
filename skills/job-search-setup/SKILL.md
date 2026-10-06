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
3. The private profile is `job-search/profile.md`; the shareable page is `job-search/preferences.md`.

If `profile.md` already exists and the user said "set up my job search," read it, summarize it in a few lines, and ask whether to update it or start over. Never overwrite a profile without asking.

## Step 1: Start from the resume

Ask for the resume first: "Paste your resume, or tell me which file in your folder it is." A PDF or document in their folder is fine; read it directly.

From the resume, draft:

- **Background:** current or most recent title, years of experience, a two-sentence career arc.
- **Proof points:** the 3 to 6 strongest accomplishments, each written outcome first, then how, then scope, with both ends of any number ("trial-to-paid conversion from 9% to 13% across 40+ tests, with a team of 6"). Where the resume gives no number, keep the outcome in words and add a placeholder.
- **Likely target titles,** from the arc and the most recent role.
- **Lead-with guidance:** which proof points to put first for which kinds of roles.

Then show a short summary of what you drafted (five to eight lines, not the whole profile) and ask only what the resume couldn't tell you. If the user has no resume handy, ask for the same things conversationally instead.

## Step 2: The search essentials

One or two turns, a few questions at a time. Use the AskUserQuestion tool for multiple-choice parts where it helps.

**What they want:**
- Confirm the target titles (the words postings actually use) and seniority.
- Location and work mode: city or metro; remote, hybrid (how many days), on-site. Anywhere they won't go?
- Pay: their base floor. Comfortable and ideal numbers are optional; take them if offered. Most postings don't list pay, and that never counts against a role.

**What to cut, and what to flag:**
- Functions to exclude, with exceptions written in. Ask: "Anything that's close to what you do but not it?" Write it as "data science PM out, growth analytics in." Exclude the function, not the whole field.
- Industries to avoid. Company types to skip: staffing firms and job aggregators that repost other companies' roles are excluded by default; say so and let them turn it off.
- **Strong signals:** what makes a role top-tier for them ("growth or retention work at a consumer subscription company").
- **Weak and parked signals** (optional, one question): "Anything that's a nice plus but wouldn't make a role great on its own? Anything you're interested in but not chasing right now?"

Keep it light. If the user is impatient, titles, location, floor, and exclusions are enough to scan. Everything else fills in later.

## Step 3: Build the searches

A saved search is a job-board URL with the user's filters built in, so a scan can reuse it.

- **LinkedIn search URL:** build it from their answers. See `references/building-a-saved-search.md` for the parameters and worked examples. Show the user the link and confirm it.
- **Or capture one they already use:** they set filters on any board, copy the address bar, and paste it. Save it. More than one saved search is fine (broad and narrow); label each.
- **Company job site searches:** lots of roles get posted straight to company job sites (Ashby, Greenhouse, Lever, and others) and never reach LinkedIn. Build one-click Google searches limited to those sites and to recent posts, using their titles and location. They're free and run in the user's own browser. See `references/ats-search-links.md` for how to build them; typically one for their city and one for remote. Show the links.
- **Companies to watch** (optional): "Any companies you'd jump at?" Scans check their public job feeds directly.

## Step 4: Save, then scan

Write `job-search/profile.md` using `references/profile-template.md`. Fill every field you captured and mark the rest `(not set yet)`.

Then, in plain words:

> "Saved. I'll use this for scans, fit checks, and interview prep, and you can change anything by telling me. Want me to run your first scan now?"

On yes, hand off to `find-jobs`.

## Step 5: The preferences page (offer it after the first scan)

Once the user has seen a first scan, or whenever they ask, offer the shareable page:

> "One more thing worth doing this week, when you have half an hour: a one-page 'what I want next' you can share with people who can help. It ends with one sentence that makes it easy for anyone to keep an eye out for you. Scans work fine without it, and they get sharper with it."

On yes, run the conversation in `references/preferences-template.md`: what they'd hate, the bad-boss question, flipping must-nots into must-haves, what they love (and what they're good at but don't enjoy), the company questions with the subject test ("would you care about this every day?"), goals, the one sentence, and the homework of sharing it with three people. Write `job-search/preferences.md` and link it from the top of `profile.md`.

When the page turns up something the scan should use (a must-not, a company size, a subject they'd never work in), add it to the profile's exclusions or signals too, and say so.

## Step 6: Reminders (offer once, at the end)

> "Want me to check in on the days you pick, with follow-ups that are due, interviews coming up, and links to fresh roles?"

On yes, hand off to `job-search-automation` to set up reminders. Record the days and time in the profile's Reminders section.

## Updating later

For a one-field change (raise the floor, add a skip-list company, add an exception), read `profile.md`, make the change, write it back, and say what changed. Don't rerun setup. If the change belongs on the preferences page too, update both.

## Principles

- **Ask once, reuse everywhere.** A few extra minutes here saves the user repeating themselves for months.
- **The resume does the first draft.** The user corrects; they don't fill in forms.
- **The words postings use.** Real target titles, not a category.
- **What to cut matters as much as what to find.** A precise exclusion removes more noise than any keyword adds.
- **Plain language with the user.** Say "your search" and "your preferences," not file names, unless they ask.
