# Public ATS Feeds (Watchlist Sweep)

Greenhouse, Lever, and Ashby publish each company's open roles as public, documented JSON endpoints: the same data the company's careers page renders. No login, no key, no browser. This is the fastest, cleanest scan source there is, and it isn't scraping: these APIs exist precisely so the postings can be read programmatically.

Use this for the companies in the profile's **Companies to Watch** list.

## Endpoint patterns

| ATS | Endpoint | You have the slug when the careers page looks like |
|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` | `boards.greenhouse.io/<slug>` or `job-boards.greenhouse.io/<slug>` |
| Lever | `https://api.lever.co/v0/postings/<slug>?mode=json` | `jobs.lever.co/<slug>` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/<slug>` | `jobs.ashbyhq.com/<slug>` |

## Finding a company's slug

1. If the watchlist entry already has a board URL, the slug is the path segment after the domain.
2. Otherwise, search the web for `<company> careers` and look at where the "open roles" page lives. If it's hosted on one of the three domains above, you have the slug.
3. If the careers page is custom-hosted (Workday, custom site, etc.), this method doesn't apply. Note it on the watchlist entry ("custom board") so future scans don't re-derive that, and cover the company via the saved search or paste flow instead.

## Fetching and parsing

Fetch the endpoint (WebFetch or `curl -s` both work; these are plain public JSON). Per ATS, the fields you need:

- **Greenhouse:** `jobs[]` → `title`, `location.name`, `absolute_url`, `updated_at`
- **Lever:** array → `text` (title), `categories.location`, `categories.commitment`, `hostedUrl`, `createdAt`
- **Ashby:** `jobs[]` → `title`, `location`, `isRemote`, `jobUrl` (fall back to `applyUrl`)

Then treat the results exactly like any other scan source:

1. Filter titles against the profile's target titles **loosely** (a watchlist company is already one the user wants, so show anything plausibly in their function, not just exact title matches).
2. Build the standard job cards (company, role, location, comp if present, url).
3. Dedupe against the tracker like every other source.
4. Classify with the standard rubric and fold into the same STRONG/INCLUDE presentation.

## Practical notes

- **Batch it.** A dozen watchlist companies is a dozen quick fetches. Run them together, don't narrate each one.
- **A 404 usually means the slug is wrong or the company changed ATS.** Re-derive from the careers page once; if it moved to a custom board, update the watchlist note.
- **An empty list isn't an error.** "Acme: no open roles matching your targets" is a useful result; say it in one line, and count it as working in the source-health line. A fetch that fails or times out is the error, and the source-health line says so.
- **`updated_at`/`createdAt` are worth surfacing** for fresh postings ("posted this week"). Recency is a real signal for watchlist companies the user checks repeatedly.
