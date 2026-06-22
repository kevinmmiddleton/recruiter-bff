# Job Search Profile — Template

This is the shared profile for the Job Search Agent plugin. It lives at `job-search/profile.md` in the user's Cowork folder. Every skill in the plugin reads it: `find-jobs` uses the search section, `application-tracker` uses the strong-fit signals for scoring, and `interview-guide-engine` uses the background section.

Fill in what's known. Mark anything not yet captured as `(not set yet)` so other tools can tell the difference between "empty on purpose" and "not asked yet."

---

```markdown
# Job Search Profile

_Last updated: YYYY-MM-DD_

## Search Targets

- **Target titles:** Product Manager, Senior Product Manager, Product Lead, Group PM
- **Seniority:** Senior, Staff/Principal, Lead/Director
- **Location:** New York metro
- **Work mode:** Remote (US) or hybrid NYC
- **Will not relocate to / work in:** (e.g., New Jersey onsite)
- **Compensation floor (base):** $150,000
- **Note on comp:** Most postings don't list it. Include unlisted-comp roles by default.

## Strong-Fit Signals (flag these as top-tier)

- Enterprise / internal tools / platform
- 0-to-1 product builds
- Regulated industries (finance, healthcare, gov/civic)
- AI tooling / LLM products

## Exclusions

- **Role types / functions:** ML/Data-Science PM (AI tooling is OK), ad-tech PM, payments PM
- **Industries:** (e.g., gambling, adult)
- **Company types:** staffing/recruiting firms, advertising agencies
- **Named companies to skip:** (your block list — add over time)

## Saved Searches

- **Primary (broad):** <paste URL>
- **Secondary (narrow):** <paste URL or "(not set yet)">
- **Board:** LinkedIn

## ATS Board Searches (Google `site:` dorks)

One-click Google searches scoped to company ATS boards (Ashby/Greenhouse/Lever/etc.) and restricted to recent postings — free browser search, no API. `find-jobs` reads these like saved searches. See `ats-search-links.md` for construction.

- **Fresh — NYC (past week):** <Google URL with `tbs=qdr:w`> or "(not set yet)"
- **Fresh — Remote (past week):** <Google URL with `tbs=qdr:w`> or "(not set yet)"

## Companies to Watch (optional)

Companies the user would join in a heartbeat — scanned directly via their public ATS feeds on every `find-jobs` run, no saved search needed.

- **[Company]** — board URL if known (e.g., `boards.greenhouse.io/acme`), or "(ATS unknown)"
- **[Company]** — `jobs.lever.co/acme`

## Background (for fit reads + interview prep)

- **Current/most recent title:** Senior Product Manager
- **Years of experience:** 12
- **Career arc (2 sentences):** ...
- **Why looking:** ...

### Proof Points (3–6 strongest)

1. **[Company]** — what you did — measurable result
2. **[Company]** — what you did — measurable result
3. **[Company]** — what you did — measurable result

### Lead-With Guidance

- For AI/tooling roles, lead with: ...
- For platform roles, lead with: ...

## Voice & Logistics

- **How I sound in interviews:** dry, concise, warm
- **Go-to question for interviewers:** ...
- **Be upfront about:** (career gap, title mismatch, domain pivot — or "nothing")
- **Salary expectation to state when asked:** ...
```

---

## Field notes for whoever fills this in

- **Target titles** should be the literal phrases that appear in postings. "Product Lead" and "Group PM" surface different results than "Product Manager." Capture all the user actually wants.
- **Strong-fit signals** drive the STRONG tier in scans and the score in the tracker. Keep them concrete.
- **Exclusions** do the heavy lifting in filtering. A precise skip list removes more noise than any keyword adds signal. The named-companies block list grows over time — append, don't replace.
- **Saved searches** are job-board URLs with filters applied. See `building-a-saved-search.md`.
- **ATS board searches** are free Google `site:` dorks scoped to company ATS boards with recency baked into the URL. See `ats-search-links.md`. They complement the watchlist: the watchlist checks companies the user *names*; these sweep *every* company on those boards for fresh roles.
- **Companies to watch** get swept directly via public ATS feeds (Greenhouse/Lever/Ashby) on every scan — fast and browser-free. Capture the board URL when known; `find-jobs` can derive it once and save it back.
- **Proof points** can be deferred to first interview-guide use if the user is in a hurry, but they make every fit read sharper, so capture them when you can.
