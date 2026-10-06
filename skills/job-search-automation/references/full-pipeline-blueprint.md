# Self-Hosted Pipeline Blueprint

What it actually takes to build a job-scan system that runs unattended, twice a day, forever: classifying roles with a model and pushing matches to your phone. This is a real engineering project, not a Cowork feature. The blueprint below is distilled from a working production system so you can judge the effort honestly before committing.

Share this with anyone who asks "could I just automate the whole thing?" The answer is yes, and here's the shape of it.

## The shape

```
Scheduler (fires 2x/day)
   │
   ▼
Orchestrator script
   │
   ├── Fetch: headless browser loads your saved search → raw HTML
   ├── Extract: parse HTML into structured job cards (cuts ~200KB → ~35KB)
   ├── Pre-filter (no model): drop URLs/companies/roles already seen
   ├── Classify: one cheap LLM API call tags each role INCLUDE/EXCLUDE/STRONG
   ├── Assemble: rebuild matches with real URLs, write to a tracker
   ├── Notify: push the matches to you (text / email / chat)
   └── Log: append metrics for debugging
```

## Components, and what each one costs you

**1. An always-on computer.** A cheap mini desktop, a Raspberry Pi, or a small cloud VM. It has to be awake and online when the scheduler fires. This is the piece the lightweight plugin exists to avoid. Cost: hardware you own, or a few dollars a month for a VM.

**2. A scheduler.** Whatever your OS offers: cron (Linux), launchd or the Shortcuts app (macOS), Task Scheduler (Windows). Fires the orchestrator on a cadence. Watch out for: the machine being asleep, network not ready on wake (add DNS retries), and overlapping runs.

**3. A fetcher (headless browser).** The hard part. Job boards render results with JavaScript and actively discourage scraping, so a plain HTTP fetch returns an empty shell. You need a real browser driven headlessly (e.g., Playwright with headless Chromium). Expect to handle: login walls, stale sessions, layout changes that break extraction, and the occasional block. Public search URLs (no login) are far more durable than authenticated ones. Budget for this breaking a few times a year.

**4. An extractor.** Parse the fetched HTML into clean records (company, title, location, URL). Multiple strategies (data attributes, href patterns, embedded JSON) give resilience when one breaks. This step is also the main cost control: it shrinks a ~200KB page to ~35KB of structured text before the model ever sees it.

**5. Deterministic pre-filters.** Before spending a model call, drop anything you've already seen (a running list of URLs and company|role pairs) and anything on your hard skip list. On a scan that closely follows another, this can remove almost everything, which means zero model calls and near-zero cost. Cheap, deterministic, do it first.

**6. A classifier (cheap LLM API).** Send the surviving roles to a small, fast model (e.g., a Haiku-class or Flash-class model) with your preferences as the rule set. Ask only for INCLUDE/EXCLUDE/STRONG plus a reason. That's classification, not generation, so the output is tiny. A clear system instruction ("classify every role, never refuse, when in doubt INCLUDE") matters. Cost: roughly **$1 to $2 a month** at twice-daily cadence with good pre-filtering. Don't trust the model's echoed URLs; carry the real ones from the extractor.

**7. A tracker (the running memory).** A database (or even a synced file) holding every role ever processed and every application's status. Feeds the dedup pre-filter and gives you a pipeline view. A lightweight SQL database is plenty; a single computer doesn't need anything fancy.

**8. A notifier.** How matches reach you: a text message, an email, a chat message. On macOS this can be the Shortcuts app sending iMessage via a tiny localhost bridge; elsewhere, an email API or a chat webhook. Keep messages short and linkable.

**9. Logging + maintenance.** Append one line per run (sizes, counts, timing) so you can tell at a glance whether it's healthy. Plan to trim the dedup list periodically (it grows forever otherwise) and to fix extraction when the board changes its markup.

## Effort and reality

- **Build:** a weekend or two for someone comfortable with a scripting language and a headless browser. Longer if the fetch/auth fights back.
- **Cost:** ~$1–2/month in API calls; plus hardware or a small VM.
- **Maintenance:** the fetcher is the fragile part. Expect to fix extraction a few times a year when the board changes its HTML, and to refresh any login session it depends on.
- **The payoff:** scans happen whether you're there or not, and matches land on your phone without you opening anything.

## Cost-control lessons (learned the expensive way)

- **Extract before you classify.** Feeding raw HTML to a model is the single biggest waste; structured extraction cut input ~5x.
- **Pre-filter deterministically.** Most duplicates can be removed with string matching, no model call. This is what keeps the bill near zero.
- **Use a small model.** Classification doesn't need a frontier model. A Haiku/Flash-class model at low temperature is plenty and ~5x cheaper than a mid-tier one.
- **Cap the cadence.** Twice a day catches essentially everything; a midday scan mostly returns duplicates. More frequency ≠ more signal.
- **Trim the memory.** The dedup list grows unbounded and inflates every prompt. Archive entries older than ~45 days.

## When this is worth it

Build this if you're searching for months, scanning daily, and the manual "open the board, skim, dedupe in your head" loop is genuinely costing you. If you're searching for a few weeks, reminders and on-demand scans in Cowork will serve you better for a fraction of the effort. Most people never need this, but if you do, this is the whole map.
