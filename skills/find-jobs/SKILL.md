---
name: find-jobs
description: >
  Runs an on-demand job scan against the user's saved search, filters the results against
  their preferences, and surfaces the matches. Use when the user says "scan for jobs,"
  "find me jobs," "any new roles," "what's out there," "run my job search," "check for
  new postings," or "find matches." Pulls live results using the user's logged-in browser
  (Claude-in-Chrome) when available, or a paste flow when it isn't. Classifies each role,
  removes duplicates already in the tracker, and offers to log matches. Requires a profile
  from job-search-setup; if none exists, route there first.
---

# Find Jobs — On-Demand Scan

Pull fresh roles from the user's saved search, cut the noise, and show them what's worth their attention. This is the on-demand replacement for an always-on scraper: it runs only when asked, on a normal machine.

## Step 1: Load the profile

Read `job-search/profile.md` from the user's Cowork folder.

- **No profile?** Tell the user you need to set up their search first, and hand off to `job-search-setup`. Don't guess preferences.
- **No saved search in the profile?** Run the saved-search step of `job-search-setup`, then continue.

Pull out: target titles, seniority, location/work-mode, comp floor, strong-fit signals, exclusions, skip-list companies, and the saved-search URL(s).

## Step 2: Get the results

Try these in order. Use the first one that works.

### Method A — Logged-in browser (preferred)

Use the Claude-in-Chrome extension to read the live search.

1. Confirm a browser is connected (`list_connected_browsers`). If the Chrome tools aren't loaded, load them via ToolSearch (`query: "chrome", max_results: 20`).
2. `navigate` to the saved-search URL.
3. `get_page_text` (and scroll / read more if the board lazy-loads) to capture the visible result cards.
4. If the page shows a login wall or "no results," tell the user what you saw and fall back to Method B.

This sees what the user would see, including results behind their login. It does **not** log in for them — it uses the session they already have.

### Method B — Paste flow (universal fallback)

If no drivable browser is available, or Method A hit a wall:

- Give the user their saved-search URL and ask them to open it, then paste the results (or the whole page text) back. Or ask them to paste a list of roles they're looking at.

Either way, you end up with raw result text to parse. Never block the scan just because the browser isn't connected — the paste flow always works.

> Do not try to fetch LinkedIn (or similar) result pages with web_fetch/curl/python — they render client-side and return an empty shell, and scraping them programmatically is off-limits. Use the browser the user controls, or the paste flow.

### Watchlist sweep (runs alongside A or B)

If the profile has a **Companies to Watch** list, also sweep those companies' public ATS feeds — Greenhouse, Lever, and Ashby publish every company's open roles as documented public JSON, no browser or login needed. Method and endpoint patterns are in `references/ats-feeds.md`. Fold the results into the same pipeline as the saved-search results; tag the source so the user can see which matches came from the watchlist.

### ATS board sweep (runs alongside A or B)

If the profile has **ATS Board Searches** (Google `site:` dork links), sweep those too. They surface fresh roles posted directly on company ATS boards (Ashby, Greenhouse, Lever, etc.) across *every* company at once — the postings that never reach LinkedIn and are far less contested. The recency filter is baked into each URL, so you only see recent postings. Open each link in the user's browser (Method A) and read the results, or hand the user the link to click and paste back (Method B). Fold into the same pipeline and tag the source as `ats-board`. Construction details, if the links are missing or need a refresh, are in `../job-search-setup/references/ats-search-links.md`.

This complements the watchlist: the watchlist checks companies the user *named*; this sweeps the whole boards for anyone new.

## Step 3: Parse into job cards

From the captured text, extract one record per posting:

- **company**
- **role** (title as posted)
- **location** (and remote/hybrid/onsite if shown)
- **comp** (only if the posting lists it — most don't)
- **url** (the direct posting link)

Discard obvious junk: pagination text, "promoted" labels, ads, anything under ~20 characters or missing both a company and a title.

## Step 4: Check against the tracker

Read the tracker (`job-search/applications.csv`) if it exists, and follow "Checking against the tracker" in `references/classification-rubric.md`:

- The same role at the same company is already tracked. Drop it and count it.
- A different role at a company already in the tracker stays in, tagged **New role at a company you know**, with one line of history.
- A role whose old row is `closed` or `hold` may be back. Show it with its history.

No tracker yet? Skip this step.

## Step 5: Classify each role

Apply the rubric in `references/classification-rubric.md`, using the user's profile as the rule set. Tag every surviving role:

- **STRONG** — clear fit and hits a strong-fit signal. Lead with these.
- **INCLUDE** — fits the basic criteria, worth a look.
- **EXCLUDE** — fails a rule (wrong level, excluded function/industry, skip-list company, wrong location). Don't show these by default; keep a count.

When genuinely unsure, lean INCLUDE. Better to show a borderline role and let the user dismiss it than to silently bury a good one. This mirrors how a well-tuned classifier behaves: high recall, let the human make the final cut.

## Step 6: Present the matches

Lead with a one-line summary: "12 new roles, 3 strong." Then list STRONG first, then INCLUDE, grouped and skimmable. For each role:

```
[STRONG] Company — Role
  Location · Comp (if listed)
  Why it fits: <one line tied to a profile signal>
  <url>
```

Keep the "why" to a single, specific line — name the signal it hit ("regulated industry + 0-to-1," not "good match"). If you dropped roles, say so briefly: "Hid 8 (4 wrong level, 2 staffing firms, 2 already tracked)." Don't dump the excludes unless asked.

## Step 7: Offer to log them

Ask if they want the matches saved to the tracker as prospects:

> "Want me to add the strong ones to your tracker so they're easy to find later?"

If yes, hand the selected roles to `application-tracker` to append with status `prospect`. This is also what makes future scans dedupe correctly — anything logged won't resurface.

For roles the user is seriously considering, offer the deeper read: `evaluate-role` takes the full posting and produces a dimension-scored evaluation with a requirement-by-requirement match against their profile. A scan read is a glance; that's the decision tool.

## Principles

- **Run only when asked.** No background loop, no schedule unless the user set one up via `job-search-automation`.
- **High recall, honest filtering.** Surface borderline roles; explain what you cut. The user's time is better spent dismissing than digging.
- **Specific fit reads.** "Why it fits" should reference a real signal from their profile, never a generic compliment.
- **Never scrape around a login.** Use the browser the user controls or the paste flow. No headless workarounds.
- **The tracker is the memory.** Dedup depends on logging. Encourage saving matches so the next scan stays clean.
