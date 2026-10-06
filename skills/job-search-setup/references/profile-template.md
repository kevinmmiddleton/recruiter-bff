# Job Search Profile: Template

The private profile for Recruiter BFF lives at `job-search/profile.md` in the user's Cowork folder. Every skill reads it. Scans use the targets, signals, and exclusions; the fit check uses all of it; interview guides and materials use the background.

Its shareable partner is `job-search/preferences.md` (see `preferences-template.md`). Pay, the skip list, and searches stay here, private.

Fill in what's known. Mark anything not captured yet as `(not set yet)`, so other skills can tell "empty on purpose" from "not asked yet."

---

```markdown
# Job Search Profile

_Last updated: YYYY-MM-DD_
_Preferences page: job-search/preferences.md (or "not built yet")_

## Search Targets

- **Target titles:** Senior Product Manager, Product Lead, Group Product Manager
- **Seniority:** Senior, Staff or Principal, Lead
- **Location:** New York metro
- **Work mode:** remote (US) or hybrid in New York, up to 3 days in the office
- **Won't work in:** fully on-site roles; anywhere outside the New York metro unless remote
- **Pay (base):** floor $170,000 · comfortable $185,000 · ideal $200,000+
- **Unlisted pay:** neutral. Most postings don't list it, so it never counts against a role.

## Signals

- **Strong** (makes a role top-tier on its own): growth, retention, or lifecycle work; consumer subscription products
- **Weak** (a plus, not enough on its own): consumer health; experimentation-heavy teams
- **Parked** (interesting, not pursuing right now): Group PM roles with direct reports
- **Pickiness:** strong plus maybe (show STRONG and INCLUDE) | strong only

## Exclusions (exceptions written in)

- **Functions:** data science PM (but growth analytics is fine); ad-tech PM
- **Industries:** crypto; gambling and sports betting
- **Company types:** staffing and recruiting firms; job aggregators that repost other companies' roles
- **Named companies to skip:** (add over time)

## Saved Searches

- **Primary (broad):** <URL>
- **Secondary (narrow):** <URL or "(not set yet)">
- **Board:** LinkedIn

## Company Job Site Searches

One-click Google searches limited to company job sites (Ashby, Greenhouse, Lever, and others) and to recent posts. Free, in the user's own browser. See `ats-search-links.md`.

- **Fresh, New York (past week):** <Google URL with `tbs=qdr:w`> or "(not set yet)"
- **Fresh, remote (past week):** <Google URL with `tbs=qdr:w`> or "(not set yet)"

## Companies to Watch

Companies the user would jump at, checked through their public job feeds on every scan.

- **[Company]:** board URL if known (`boards.greenhouse.io/acme`), or "(job site unknown)"

## Background (drafted from the resume)

- **Name:**
- **Current or most recent title:**
- **Years of experience:**
- **Career arc (2 sentences):**
- **Currently:** employed / searching full time / between roles since [month]
- **Why looking:**

### Proof Points (3 to 6 strongest)

Outcome first, then how, then scope. Both ends of every number.

1. **[Company]:** [outcome, with the number from and to], by [how], [scope: team, users, budget]
2. ...

### Lead-With Guidance

- For growth roles, lead with: ...
- For platform roles, lead with: ...

## Voice and Logistics

- **How I sound in interviews:** e.g., warm, direct, concise
- **Go-to question for interviewers:**
- **Phrases I like:** framings the user has tested and approved
- **Be upfront about:** a gap, a title mismatch, a pivot, or "nothing"
- **What I say when asked about pay:** the user's own line, in their words, or "(not set yet)"

## Reminders

- **Days and time:** e.g., Mon, Wed, Fri at 8:30am, or "none"
```

---

## Field notes

- **Target titles** are the literal phrases postings use. "Product Lead" and "Group PM" turn up different results than "Product Manager."
- **Pay tiers:** the floor filters (a listed range entirely below it is excluded); comfortable and ideal shape the fit check and the pay scripts in interview guides. If the user gives only a floor, that's enough.
- **Signals:**
  - **Strong** signals make a role STRONG in a scan and lift the target-fit score.
  - **Weak** signals are tie-breakers: they can lift a borderline role into INCLUDE and get named in "why it fits," but never make a role STRONG alone.
  - **Parked** signals are things the user cares about but isn't chasing right now (often a lane where they keep stalling). Don't treat them as strong. Mention a parked match in one line so it isn't lost.
- **Pickiness** sets what a scan shows: "strong plus maybe" shows STRONG and INCLUDE (the default); "strong only" shows STRONG and gives a count of the rest. The user can change it for a single scan ("just the strong ones today").
- **Exclusions with exceptions:** exclude the function, not the whole company or field, and write the exception next to it: "data science PM out, growth analytics in." A precise exclusion removes more noise than any keyword adds. The named-companies list grows over time; append, don't replace.
- **Company types** default to excluding staffing firms and aggregators that repost roles. The user can turn that off.
- **Proof points** come from the resume first. Never invent a number: if the resume says "improved conversion," write that and mark the number as a gap to fill, like `[from ?% to ?%]`.
- **Pay line:** this is what the user has decided to say. Skills can remind them of it; they never say it for the user.
- **Reminders** are set up by `job-search-automation`; this records what the user chose.
