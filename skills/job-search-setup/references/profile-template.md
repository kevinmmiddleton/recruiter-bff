# Job Search Profile: Template

The private profile for Recruiter BFF lives at `job-search/search-profile.md` in the user's Cowork folder. Every skill reads it. Scans use the targets, signals, and exclusions; the fit check uses all of it; interview guides and materials use the background.

Its shareable partner is `job-search/looking-for.md` (see `preferences-template.md`). Pay, the skip list, and searches stay here, private.

Fill in what's known. Mark anything not captured yet as `(not set yet)`, so other skills can tell "empty on purpose" from "not asked yet."

---

```markdown
# Job Search Profile

_Last updated: YYYY-MM-DD_
_Preferences page: job-search/looking-for.md (or "not built yet")_
_Resume: job-search/resume/resume.md, copied from Sam-Okafor-resume.pdf on YYYY-MM-DD. Other versions: Sam-Okafor-growth.pdf (growth roles)._

## Search Targets

- **Target titles:** Senior Product Manager, Product Lead, Group Product Manager
- **Seniority:** Senior, Staff or Principal, Lead
- **Location:** New York metro
- **Work mode:** remote (US) or hybrid in New York, up to 3 days in the office
- **Won't work in:** fully on-site roles; anywhere outside the New York metro unless remote
- **Pay (base):** floor $170,000 · comfortable $185,000 · ideal $200,000+
- **Unlisted pay:** neutral. Most postings don't list it, so it never counts against a role.

## Company

- **Size:** 50 to 2,000 people
- **Stage and ownership:** Series B or later, or public

## Signals

- **Strong** (what I want most; makes a role top-tier): growth, retention, or lifecycle work; consumer subscription products
- **Parked** (a lane I like but keep stalling in, or am not chasing right now): Group PM roles with direct reports
- **Weak** (soft warnings: flag it, rank it lower, never cut it): contract or contract-to-hire roles; titles that often mean sales-facing work
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
- **Current LinkedIn headline:** as it reads today, or "(not set yet)"

## Reminders

- **Status:** e.g., "Mon, Wed, Fri at 8:30am (created YYYY-MM-DD)"; "requested Mon and Thu at 8:30am, not created yet (YYYY-MM-DD)"; "none"; or "(not set yet)"
- **Scheduled scan:** same forms, e.g., "every day at 7:30am (created YYYY-MM-DD)"; "requested every day at 7:30am, not created yet (YYYY-MM-DD)"; "none"; or "(not set yet)"

## Offered

Optional things already offered, with the date, so no skill offers them twice. Add a line whenever you offer one.

- (e.g., "Preferences page: 2026-10-07", "LinkedIn export check: 2026-10-06", "Reminders: 2026-10-08")
```

---

## Field notes

- **Target titles** are the literal phrases postings use. "Product Lead" and "Group PM" turn up different results than "Product Manager."
- **Pay tiers:** the floor filters (a listed range entirely below it is excluded); comfortable and ideal shape the fit check and the pay scripts in interview guides. If the user gives only a floor, that's enough.
- **Signals:**
  - Signals rank roles; they never cut them. Cutting is what exclusions are for.
  - **Strong** signals make a role STRONG in a scan (the "why it fits" line names the one it hit) and lift the target-fit score.
  - **Parked** lanes are ones the user likes but keeps stalling in, or isn't chasing right now. Show a parked match below the strong ones, as INCLUDE, with the reason and a note to revisit.
  - **Weak** signals are soft warnings: contract roles, titles that often turn out to be sales-facing, anything the user hesitates on without ruling out. Flag the role and rank it lower; never hide it.
- **Pickiness** sets what a scan shows: "strong plus maybe" shows STRONG and INCLUDE (the default); "strong only" shows STRONG and gives a count of the rest. The user can change it for a single scan ("just the strong ones today").
- **Exclusions with exceptions:** exclude the function, not the employer, and write the exception on the same line: "data science PM out, growth analytics in." A precise exclusion removes more noise than any keyword adds.
- **Industries** are judged by the company's core business, not one product line. A software company that sells *to* an excluded industry gets shown with a flag, not cut.
- **Temporary blocks** carry a reason and a revisit date: "Acme: hiring freeze, revisit January," or a cooling-off period after a rejection when the same role keeps getting reposted. The named-companies list grows over time; append, don't replace.
- **Direct reports** the user doesn't want: flag the role and let them decide; don't skip it automatically.
- **Company types** default to excluding staffing firms and aggregators that repost roles. The user can turn that off, but only an explicit line does it ("include staffing firms"); a missing line or "(none stated)" keeps the default.
- **Company size and stage** shape the fit check's company score and the scan's ranking. A size or stage the user dislikes is a soft warning unless they call it a dealbreaker.
- **The resume** lives in `job-search/resume/`: the user's own files, unchanged, plus `resume.md`, a plain-text copy of the current version. It's the record of what the resume really says, so every claim a skill makes can be checked against it. The profile summarizes it; it never replaces it.
- **Proof points** come from the resume first. Never invent a number: if the resume says "improved conversion," write that and mark the number as a gap to fill, like `[from ?% to ?%]`.
- **Pay line:** this is what the user has decided to say. Skills can remind them of it; they never say it for the user.
- **Reminders and the scheduled scan** are set up by `job-search-automation`; these lines record what the user chose and whether each task actually exists.
- **Offered** keeps the one-offer-per-message rule from turning into the same offer every day. Check it before offering anything optional.
- **Fields setup doesn't ask for** (voice, go-to question, phrases, the current LinkedIn headline) get filled in later by the skills that need them: interview guides and materials. Leave them `(not set yet)` until then.

## Upgrading a 0.4 profile

A profile from Job Search Agent or Recruiter BFF 0.4 has the same kinds of facts under older names. Skills read the old names as the new ones. The first time a skill writes the profile, it moves the old names to the new ones and keeps every value exactly as written:

| 0.4 | 1.0 |
|---|---|
| `## Search Targets` field "Compensation floor (base): $170,000" | "Pay (base): floor $170,000" (add comfortable and ideal only if the user gives them) |
| `## Search Targets` field "Note on comp" | "Unlisted pay" |
| `## Search Targets` field "Will not relocate to / work in" (or "Will not work") | "Won't work in" |
| `## Search Targets` fields "Will not work" and "Will not relocate to," when they're separate | one "Won't work in" line with both ("fully on-site roles; not relocating to Boston"); leave out a part that says "(not set yet)" |
| `## Search Targets` field "Ideal focus" | added to **Strong** in `## Signals`, unless Strong already says the same thing |
| `## Exclusions` field "Work arrangement" | added to "Won't work in" in Search Targets, unless it's already there |
| `## Search Targets` field "Company size / stage," if there is one | a `## Company` section with "Size" and "Stage and ownership" |
| `## Strong-Fit Signals (flag these as top-tier)` | `## Signals`: the old list becomes **Strong**; add **Parked** and **Weak** as "(not set yet)" and **Pickiness** as "strong plus maybe" |
| `## Exclusions` | `## Exclusions (exceptions written in)` |
| `## Exclusions` field "Role types / functions" | "Functions" |
| `## Exclusions` field "Company types: (none stated)" or missing | "Company types: staffing and recruiting firms; job aggregators that repost other companies' roles" (the default; tell the user once) |
| `## ATS Board Searches (Google site: dorks)` | `## Company Job Site Searches` |
| `## Companies to Watch (optional)` | `## Companies to Watch` |
| `## Background (for fit reads + interview prep)` | `## Background (drafted from the resume)` |
| "Current/most recent title" | "Current or most recent title" |
| `### Proof Points (3–6 strongest)` | `### Proof Points (3 to 6 strongest)` |
| `## Voice & Logistics` | `## Voice and Logistics` |
| "Salary expectation to state when asked" | "What I say when asked about pay" |
| no "Phrases I like" or "Current LinkedIn headline" | add both to Voice and Logistics as "(not set yet)" |
| `## Field notes for whoever fills this in` | drop it (the field notes live here) |
| no Resume line | `_Resume: job-search/resume/resume.md, ..._` under the title if a copy exists, or `_Resume: not saved yet_` |
| no Preferences page line | `_Preferences page: job-search/looking-for.md_` if it exists, or "not built yet" |
| no `## Reminders` or `## Offered` | add both, with Status and Scheduled scan as "(not set yet)" and an empty Offered list |

Anything else the user added stays where it is. Tell the user in one line that the section names changed and what they wrote didn't.
