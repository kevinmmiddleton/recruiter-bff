---
name: job-search-setup
description: >
  Onboards a user's job search and builds a reusable saved search. Use when the user
  says "set up my job search," "help me start a job search," "what should I search for,"
  "set up my search," "build my saved search," or when another Recruiter BFF skill
  reports that no profile exists yet. Also use when the user says "update my job profile,"
  "change my search," "edit my preferences," or "add a company to my skip list." Captures
  target roles, location, comp floor, dealbreakers, and background once, then saves a
  shared profile that every other tool in this plugin reads.
---

# Job Search Setup

Capture what the user is looking for and who they are, save it once, and build a search they can reuse forever. Every other tool in this plugin reads the profile this skill creates, so do this well.

## Step 0: Find (or create) the data home

All of this plugin's data lives in a `job-search/` folder inside the user's Cowork working folder.

1. Identify the user's connected/working folder (the one Cowork can write to).
2. Create `job-search/` there if it doesn't exist.
3. The profile path is `job-search/profile.md`.

If `job-search/profile.md` already exists and the user said something like "set up my job search," they may want to start over or just review. Read it, summarize what's there, and ask whether to update it or build a search. Don't silently overwrite a profile.

## Step 1: Onboarding conversation

Capture enough to (a) filter jobs well and (b) write interview guides that sound like the user. Ask conversationally across a few turns. Do **not** dump all questions at once. Use the AskUserQuestion tool for the multiple-choice parts where it helps; use plain conversation for the open-ended parts.

**Turn 1 — What they're looking for (search essentials):**
- Target job titles (e.g., "Product Manager, Product Lead, Group PM"). Get the words that actually appear in postings.
- Seniority level(s): IC / Senior / Staff·Principal / Lead·Manager / Director+.
- Location: city or metro, and remote / hybrid / onsite. Anywhere they won't go?
- Compensation floor (base). Note that most postings don't list comp; that's fine.

**Turn 2 — Dealbreakers and signals:**
- Role types or functions to exclude (e.g., "no sales-engineering, no pure data-science PM").
- Industries to avoid, and industries that excite them.
- Company types to skip (e.g., staffing/recruiting firms, agencies) and any named companies to block.
- "Strong fit" signals — the kinds of roles to flag as top-tier (e.g., "0-to-1 builds, regulated industries, internal tools, AI tooling").

**Turn 3 — Background (powers fit reads + interview prep):**
- Current/most recent title, years of experience, and a two-sentence career arc.
- Why they're looking.
- 3–6 strongest accomplishments — for each: company, what they did, measurable result. (If they'd rather do this later, that's fine; the interview-guide tool will collect missing pieces on first use.)
- How they sound (formal/casual, dry/warm, concise/expansive) and a go-to question they like to ask interviewers.
- Anything to be upfront about (career gap, title mismatch, domain pivot) so guides address it head-on.

Keep it light. If the user is impatient, capture Turn 1 + Turn 2 (enough to scan) and tell them the rest fills in later.

## Step 2: Build the saved search

A "saved search" is just a job-board URL with the user's filters baked in, so the scan can reuse it. Help them get one.

**Preferred — build a LinkedIn search URL directly.** LinkedIn's public job search accepts URL parameters, so you can construct a link from their answers without them touching the site. See `references/building-a-saved-search.md` for the parameter reference and worked examples. Confirm the constructed URL with the user.

**Alternative — capture an existing search.** If the user prefers another board (Indeed, Built In, Wellfound, a company careers page) or already has a search they like: ask them to set their filters on the site, copy the URL from the address bar, and paste it. Save that.

Either way, you can save more than one saved search (e.g., one broad, one narrow). Label them.

**Also build ATS board search links.** Most roles live on company ATS boards (Ashby, Greenhouse, Lever, etc.), never on LinkedIn, and are far less contested. Build the user a one-click Google search scoped to those boards and restricted to recent postings, using their target titles and location. This is a free browser search (no API, no account) and `find-jobs` can read it just like a saved search. See `references/ats-search-links.md` for how to construct the links and what to generate (typically a "Fresh — NYC (past week)" and a "Fresh — Remote (past week)" link). Save them in the profile's **ATS Board Searches** section and show the user the clickable links.

## Step 3: Save the profile

Write `job-search/profile.md` using the structure in `references/profile-template.md`. Fill every field you captured; leave a clear `(not set yet)` marker for anything skipped so other tools know it's missing rather than empty on purpose.

Then confirm in plain language:

> "Saved. I'll use this for scans, fit reads, and interview prep. You can change anything anytime — just say 'update my job profile.' Want me to run a first scan now?"

If yes, hand off to the `find-jobs` skill.

## Updating later

When the user wants to change preferences, add a skip-list company, raise the comp floor, or revise their search: read the current `profile.md`, make the targeted change, and write it back. Don't re-run full onboarding for a one-field edit.

## Principles

- **Ask once, reuse everywhere.** This profile feeds every other tool. A few extra minutes here saves repetition later.
- **Capture the words postings use.** "Product Lead" and "Group PM" are different searches. Get the user's real target titles, not a category.
- **Dealbreakers are as valuable as wants.** A good skip list removes more noise than a good keyword adds signal.
- **Plain language with the user.** Never expose file paths or schema unless they ask. Talk about "your search" and "your preferences," not "profile.md."
