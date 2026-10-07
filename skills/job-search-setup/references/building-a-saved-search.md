# Building a Saved Search

A saved search is just a job-board URL with the user's filters baked in. Save it once and the `find-jobs` scan can reuse it forever. This file covers building one for LinkedIn (most common) and capturing one from any other board.

## LinkedIn: build the URL from the user's answers

LinkedIn's public job search reads filters from URL parameters, so you can assemble a working search link from the setup answers, and the user never has to touch the site.

Base:

```
https://www.linkedin.com/jobs/search/?
```

Append these parameters, joined with `&`:

| Parameter | Meaning | Example |
|-----------|---------|---------|
| `keywords` | Search terms (URL-encode spaces as `%20`) | `keywords=product%20manager` |
| `location` | Location text | `location=New%20York%2C%20New%20York%2C%20United%20States` |
| `f_E` | Experience level (comma-joined) | `f_E=4` |
| `f_TPR` | Date posted (seconds) | `f_TPR=r604800` (last week) |
| `f_WT` | Work type (comma-joined) | `f_WT=2` (remote) |
| `sortBy` | Sort order | `sortBy=DD` (most recent) |

**`f_E` experience codes:** `2`=Entry, `3`=Associate, `4`=Mid-Senior, `5`=Director, `6`=Executive. Pick the levels the user is actually after: a senior individual-contributor search is usually `4` alone; add `5` for director-level searches. `6` (executive) lets VP and C-level roles in, so leave it out unless they want those.

**`f_TPR` time windows:** `r86400`=last 24 hours, `r43200`=last 12 hours, `r604800`=last week. Match it to how often the user scans. Scans here run when the user asks, often a few times a week, so `r604800` (last week) is the default; use `r86400` for someone who scans every morning.

**`f_WT` work types:** `1`=Onsite, `2`=Remote, `3`=Hybrid. Comma-join for multiple (`f_WT=2,3`). Omit the parameter entirely to include all.

**`sortBy`:** `DD`=date (newest first), best for scanning. `R`=relevance.

### Worked example

A senior PM, NYC metro, remote or hybrid, looking at the last week, newest first:

```
https://www.linkedin.com/jobs/search/?keywords=product%20manager&location=New%20York%2C%20New%20York%2C%20United%20States&f_E=4&f_WT=2,3&f_TPR=r604800&sortBy=DD
```

Confirm the assembled URL with the user before saving. If you want to be sure it's valid, you can open it in the browser during setup and check that real results load.

### Multiple keywords

LinkedIn treats the keyword field as an OR-ish phrase match. To cover several titles, either:
- keep `keywords` broad (`product%20manager`) and let the plugin's filtering catch level/title, or
- save two searches, one broad and one narrow (e.g., `product%20lead`), and scan both.

## Any other board: capture an existing search

For Indeed, Built In, Wellfound, Otta, a company careers page, or anything else:

1. Ask the user to go to the board and set their filters (title, location, date, remote, etc.).
2. Have them copy the URL from the address bar once the results look right.
3. Paste it in. Save it as the saved search.

The scan doesn't care which board the URL points at. It reads whatever results that page shows. The only requirement is that the URL reliably reproduces the same filtered search.

## Saving

Write the chosen URL(s) into the **Saved Searches** section of `job-search/search-profile.md`. Label each (e.g., "Primary (broad)" / "Secondary (narrow)") and record which board it's on. The `find-jobs` skill picks these up automatically.
