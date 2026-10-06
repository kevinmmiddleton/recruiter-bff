---
name: find-jobs
description: >
  Runs an on-demand job scan against the user's saved searches, company job site searches, and
  watchlist, filters the results against what they want, and shows the matches. Use when the
  user says "scan for jobs," "find me jobs," "any new roles," "what's out there," "run my job
  search," "check for new postings," "find matches," or "just the strong ones today." Reads
  LinkedIn through the user's own logged-in browser (Claude in Chrome) when it's connected, or
  from results the user pastes. Checks every role against the tracker and offers to log
  matches. Needs the profile from job-search-setup.
---

# Find Jobs: On-Demand Scan

Pull fresh roles from the user's sources, cut the noise, and show them what's worth their time. It runs only when asked, on a normal laptop.

## Never

- Never get around a login, and never fetch LinkedIn result pages with code. Use the browser the user controls, or their paste.
- Never apply to anything or contact anyone.
- Never hide a source failure. "Nothing new" and "nothing worked" must look different.
- Never trust a URL the model rewrote. Carry the real posting link from the page.

## Step 1: Load the profile

Read `job-search/profile.md`, and `job-search/preferences.md` if it exists.

- **No profile:** say you need to set up their search first and hand off to `job-search-setup`. Don't guess.
- **No saved search:** run the saved-search step of setup, then continue.

Pull out: target titles, seniority, location and work mode, pay floor, signals (strong, weak, parked), pickiness, exclusions with their exceptions, skip-list companies, saved searches, company job site searches, and companies to watch. From the preferences page: must-nots and company preferences.

If the user asked for something different this time ("just the strong ones today," "include contract roles"), apply it to this scan only, and offer to save it if it sounds lasting.

## Step 2: Get the results

Run every source the profile has. Keep a tally for each one: did it work, and how many results came back.

### Saved search: the user's browser (preferred)

Use the Claude in Chrome extension to read the live search.

1. Check a browser is connected (`list_connected_browsers`). If the Chrome tools aren't loaded, load them with ToolSearch (`query: "chrome", max_results: 20`). Work in a new tab, and close it when you're done.
2. `navigate` to the saved-search URL and wait a few seconds for it to load.
3. **Don't use `get_page_text` on a LinkedIn search.** It returns the description of whichever job is open on the right, not the list. Instead, use `find` ("job search results list") to get the results list, scroll inside the results column a few times (LinkedIn fills in the cards as you scroll, about 25 to a page), then `read_page` on the list's reference. A card that's still empty after scrolling is usually an ad slot; skip it.
4. From each card, take: title, company, location and work mode ("New York, NY (Hybrid)"), pay if shown ("$75/hr - $85/hr" or "$110K/yr - $145K/yr"), posting age ("2 hours ago"), and the link. Links look like `/jobs/view/4476505407/?...`: keep `https://www.linkedin.com/jobs/view/4476505407/` and drop the tracking parameters.
5. Keep LinkedIn's own signals when a card shows them: **"N connections work here"** (a contacts hint: worth offering a check of the user's LinkedIn export, or a look at who it is), "school alum works here," "Easy Apply," "Actively reviewing applicants," "Viewed" (the user already opened it). Ignore "You'd be a top applicant"; it's a paid-feature badge, not a fit read.
6. More than one page: add `&start=25` (then `&start=50`) to the search URL. For a recent search sorted by newest, the first page or two is usually enough.
7. A login wall, an empty page, or a different search page than expected: tell the user what you saw and use the paste flow. LinkedIn has been moving people to a new AI-powered search; if a saved search link stops showing classic results, say so and help the user rebuild the link or paste results instead.

This sees what the user would see, using the session they already have. It never logs in for them.

### Saved search: paste (always works)

No browser, or the browser hit a wall: give the user their saved-search link, ask them to open it and paste the results (or the whole page) back. Never let a missing browser stop the scan.

Pasted results often have no links. Leave the link blank (never make one up), say once that the paste had no links, and ask the user to copy a role's address when they open it, so the tracker can keep it.

### Company job site searches (alongside either)

If the profile has company job site searches (Google searches limited to Ashby, Greenhouse, Lever, and similar, with recency built into the link), run them too: open each in the user's browser and read the results, or hand over the link to click and paste back. Tag these `ats-board`. If the links are missing or stale, `../job-search-setup/references/ats-search-links.md` explains how to build them.

### Watchlist (alongside either)

If the profile has companies to watch, check their public job feeds directly. Greenhouse, Lever, and Ashby publish every company's open roles as public JSON, no browser or login needed. Endpoints and method are in `references/ats-feeds.md`. Narrow each company's feed to the user's function and titles before anything else; a big company's feed can have thousands of roles. Tag these `watchlist`.

## Step 3: Parse into job cards

One record per posting:

- **company**
- **role** (title as posted)
- **location** (and remote, hybrid, or on-site if shown)
- **comp** (only if listed; most postings don't)
- **posted** (the age or date if shown)
- **url** (the direct posting link)

Throw out page junk: pagination, "promoted" labels, ads, anything missing both a company and a title.

## Step 4: Check against the tracker

Read `job-search/applications.csv` if it exists, and follow "Checking against the tracker" in `references/classification-rubric.md`:

- The same role at the same company is already tracked. Drop it and count it.
- A different role at a company already in the tracker stays in, tagged **New role at a company you know**, with one line of history.
- A role whose old row is `closed` or `hold` may be back. Show it with its history.

No tracker yet? Skip this step.

## Step 5: Classify each role

Apply `references/classification-rubric.md`, with the profile and preferences page as the rules:

- **STRONG:** a clear fit that hits a strong signal. Lead with these.
- **INCLUDE:** fits the basics, worth a look. Parked lanes and unknown companies land here, flagged.
- **EXCLUDE:** fails a rule (wrong level, an excluded function with no exception that applies, an excluded industry, a staffing firm or aggregator, a skip-list company, a place they won't work, a listed range entirely below the floor). Hidden, with a count.

When genuinely unsure, INCLUDE. A borderline role the user dismisses in two seconds costs far less than a good one they never see.

Weak signals (soft warnings like contract-to-hire) never cut or upgrade a role: they add a flag and rank it lower within its tier.

Pickiness decides what's shown: "strong plus maybe" (the default) shows STRONG and INCLUDE; "strong only" shows STRONG and a count of the rest.

## Step 6: Present the matches

Open with the summary and the source-health line, then the roles:

```
9 new roles, 3 strong.
Sources: LinkedIn saved search ✓ 18 results · company job sites ✓ 2 searches, 11 results ·
watchlist ✓ 4 of 5 companies (Acme's feed didn't respond).

[STRONG] Fernhill: Senior Product Manager, Growth
  New York (hybrid) · $175k to $205k · posted 2 days ago
  Why it fits: a growth role, your strong signal; the range clears your floor
  <url>

[INCLUDE] Northstar Learning: Senior PM, Retention · New role at a company you know
  Remote (US) · $160k to $180k · posted 5 days ago
  Why it fits: retention work; heads-up, the range starts under your floor
  History: you applied for Product Lead in August; it closed.
  <url>

Hid 6: 2 staffing firms, 2 wrong level, 1 on-site only, 1 already tracked.
```

- **The source-health line is never skipped.** A source that failed, timed out, or hit a login says so, and a source that returned zero results says "0 results," so the user can tell a quiet day from a broken search. Say it louder, in its own line, when fewer than half the sources you tried worked, when a logged-in source keeps returning nothing (the login has probably expired), or when saving to the tracker failed. A source the user chose to skip, or one that can't run in this session (no browser, no web access), isn't a failure: label it "skipped" or "not available here" and leave it out of the count.
- **Carry each role's real source** into the tracker: where it came from, not how it reached you. Pasted LinkedIn results are `linkedin`; pasted company job site results are `ats-board`. It's what later shows which sources lead to interviews.
- **"Why it fits"** is one specific line naming the signal it hit, never a generic compliment. Use only what the card, the posting, or the user said. Don't describe a company you can't verify ("a consumer subscription company") unless the listing says so; if it matters and you can't tell, say that instead ("I can't tell what Tallyho does; check before you spend time"). Add any flag after it: a weak signal ("heads-up: contract-to-hire"), a parked lane, an unknown company, pay that starts below the floor.
- **Posting age** goes on every card when you know it. Very old postings (about 60 days or more) get a short flag: "posted 9 weeks ago, may be stale." Flag, don't hide.
- If the user knows someone at a company (from `job-search/contacts.csv`, if it exists), add: "You know Priya Shah there."

## Step 7: One next step

Make **one** offer per message. Usually it's the tracker:

> "Want me to add the strong ones to your tracker?"

On yes, hand the chosen roles to `application-tracker` to add as prospects. That's also what keeps future scans from showing them again. Don't stack other offers (the preferences page, reminders) into the same message; they come at a quieter moment.

**Who you know there.** If there's no `job-search/contacts.csv` but a LinkedIn connections export (`Connections.csv`) is in the Cowork folder, it's worth one offer, following the order in "Ending a reply": "Your LinkedIn export is in your folder. Want me to check who you know at these companies?" (That's the `contacts` skill.)

For a role the user is seriously considering, offer the fit check: `evaluate-role` reads the whole posting, checks it's still open, and gives a scored apply-or-skip answer.

If a strong match is at a company where they know someone, mention that a referral usually beats a cold application, and offer to draft a short note (through `contacts`, if the user has a contacts file).

## Ending a reply

End with at most one offer. If several apply, pick the first that fits:

1. **Anything time-sensitive:** thank-you notes the same day, a reply someone is waiting on.
2. **Someone to ask before applying:** after a fit check that says apply, if the user knows someone there (from `contacts.csv`), offer the referral note; if there's no `contacts.csv` but a LinkedIn export is in the folder, offer to check it. A referral matters most before the application goes in.
3. **The obvious next step for what the user just did:** after a scan, adding matches to the tracker; after a fit check, adding the role to the tracker (once per role; skip it if the role is already tracked); after a booked round, a practice run.
4. **Checking the user's LinkedIn export** for people they know, in general.
5. **The preferences page.**
6. **Reminders.**

Logging an application or a status change has no next step of its own. That reply is the quiet moment for 4, 5, and 6.

Before offering 4, 5, or 6, check the **Offered** section of `job-search/profile.md` and skip anything already offered; when you offer one, add a dated line there. For reminders, also skip them if the profile's Reminders status is anything other than "(not set yet)." Saying a fact ("this read uses your profile alone") isn't an offer.

## Principles

- **Run only when asked.** No background loop unless the user set one up through `job-search-automation`.
- **High recall, honest filtering.** Show borderline roles and say what you cut.
- **Specific reasons.** Every "why it fits" ties to something in the profile.
- **The tracker is the memory.** Logging matches keeps the next scan clean.
