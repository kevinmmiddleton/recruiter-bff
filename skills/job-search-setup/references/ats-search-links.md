# Company Job Site Searches (Google `site:` links)

Lots of roles are posted directly on a company's job site (Ashby, Greenhouse, Lever, and others, often called ATS boards) and never make it to LinkedIn, and those postings get far fewer applicants. Google has indexed all of them. This builds the user a **one-click Google search, scoped to those boards and restricted to recent postings**, that surfaces fresh roles across every company at once.

## Why the browser, not an API

Google's normal **web search** (in the user's browser) supports the `site:` operator, `OR`, and a recency filter (`tbs=qdr:`), all for free: no key, no account, no billing. (Paid SERP APIs gate exactly these operators behind their paid tiers; don't send the user down that road. The browser does it for free and better.) This keeps the feature true to the plugin: no infrastructure, no credentials.

## The ATS domains

A solid default set, highest-yield for tech/product roles first:

```
jobs.ashbyhq.com
boards.greenhouse.io
job-boards.greenhouse.io
jobs.lever.co
jobs.smartrecruiters.com
careers.workable.com
```

Add or trim per the user's field (e.g., add `myworkdayjobs.com` and `careers.icims.com` for enterprise/finance, `jobs.jobvite.com`, `*.bamboohr.com` for SMB). Keep the combined link to ~6–8 domains; past that Google's results get diluted and the URL unwieldy.

## Building the link

A Google search URL is `https://www.google.com/search?q=<QUERY>&tbs=qdr:<R>`, URL-encoded.

**Query =** `(site: OR group) (title OR group) (location)`, for example, before encoding:

```
(site:jobs.ashbyhq.com OR site:boards.greenhouse.io OR site:job-boards.greenhouse.io OR site:jobs.lever.co OR site:jobs.smartrecruiters.com OR site:careers.workable.com) ("senior product manager" OR "product manager" OR "product lead") "New York"
```

- **Titles:** OR together the user's real target titles from the profile (quote multi-word phrases).
- **Location:** append the metro in quotes (e.g., `"New York"`), or drop it and add `remote` for the remote variant.
- **Recency (`tbs=qdr:`):** this is the whole point. `qdr:d` = past day, `qdr:w` = past week, `qdr:m` = past month. Match it to how often the user checks: **`qdr:d` for daily, `qdr:w` for a few times a week.** Without it, Google returns static top-relevance results and the same roles every time.

### Encoding

Spaces -> `+` (or `%20`), `"` -> `%22`, `(` -> `%28`, `)` -> `%29`, `:` -> `%3A`, and leave `OR` as is (an unencoded `site:` works too). Worked example (week recency):

```
https://www.google.com/search?q=%28site%3Ajobs.ashbyhq.com+OR+site%3Aboards.greenhouse.io+OR+site%3Ajob-boards.greenhouse.io+OR+site%3Ajobs.lever.co+OR+site%3Ajobs.smartrecruiters.com+OR+site%3Acareers.workable.com%29+%28%22senior+product+manager%22+OR+%22product+manager%22%29+%22New+York%22&tbs=qdr:w
```

## What to generate

Build a small, labeled set from the profile and save them (see the profile template's **Company Job Site Searches** section):

- **Fresh, NYC (past week):** combined-boards link, titles + metro, `qdr:w`.
- **Fresh, remote (past week):** same, swap the metro for `remote`.
- *(optional)* a **daily** variant with `qdr:d` for someone checking every morning.

Keep it to two or three links. They're personalized but evergreen: because recency is in the URL, the *same link* always shows only what's new. The user clicks; no regeneration needed.

## Reading the results (for `find-jobs`)

These links are read like any other source: open in a browser this session can drive (the Claude or ChatGPT desktop app's built-in browser, or the user's Chrome through an extension), read the page text, parse the result cards into job records, then run the normal dedupe -> classify -> present pipeline. If Google throws a CAPTCHA on an automated read, hand the user the link to click and use the paste flow. The URL needs no login, but Google shows results only to a real browser (a plain fetch gets a page asking for JavaScript), so a scheduled run with no browser hands the user the links instead. For an unattended run, the watchlist's public job feeds are the reliable source.
