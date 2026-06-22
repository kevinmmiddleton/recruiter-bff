---
name: job-search-automation
description: >
  Explains how to make the job scan run on its own, and helps set it up. Use when the user
  says "automate my job search," "can this run automatically," "schedule my scan," "run this
  every morning," "do this on a schedule," "set up automation," or asks what it would take to
  build a real always-on pipeline. Covers two tiers: a Cowork scheduled task (no hardware) and
  a full self-hosted pipeline (the serious build). Offers to set up the scheduled task; explains
  the rest honestly, including the tradeoffs.
---

# Job Search Automation

Help the user decide how hands-off they want their search to be, then either set up the lightweight option or explain what the serious build takes. Be honest about the tradeoffs — automation here has a real catch, and the user should hear it before committing.

There are two tiers. Most people want Tier 1. Tier 2 is a genuine engineering project.

## Tier 1 — Cowork scheduled task (no hardware)

Cowork can run a task on a schedule without you asking. This is the lightweight way to "automate" the scan: tell Cowork to run your job search every weekday morning and review what it found.

### How to set it up

If the user wants it, use the scheduled-tasks tool to create a task. A good default:

- **Cadence:** weekdays at 8am (cron `0 8 * * 1-5`), or whatever they prefer.
- **Prompt for the task:** something like *"Run my job scan: load my job-search profile, pull my saved search, filter and dedupe against my tracker, and give me a short digest of new matches (strong first). Don't apply to anything."*

Confirm the cadence with the user before creating it. After it's set, tell them they can change or cancel it anytime ("reschedule my job scan," "stop my job scan").

### The honest catch

The default scan reads results from the user's **logged-in browser**. A scheduled task that fires while the user is away may not have an interactive browser session to drive — so the live-browser scan can fail or come back empty when run unattended. Be upfront about this. Options that work better for unattended runs:

- **Use a public saved-search URL** (no login required) so the scan can read it without the user's session. LinkedIn's public job search works this way.
- **Use the ATS Board Searches** (the Google `site:` dork links from setup). These are public Google searches with recency baked into the URL — no login at all, so they're the most reliable unattended source, and they only ever show fresh roles. A scheduled task can open them, read the results, and digest the new ones; or, lowest-effort, just re-send the one-click links as a "time to check" nudge (the links never go stale, so the same link always shows what's new).
- **Treat the scheduled run as a prompt, not a scrape.** The task can assemble a "time to scan" digest and remind the user to run the live scan themselves when they're at the machine. Lower effort, still useful.
- **Accept partial reliability.** If the browser session happens to be available, great; if not, the user runs it manually. Fine for many people.

Recommend the public approaches — the ATS Board Searches and a public saved-search URL — for anyone who wants the schedule to actually fire on its own. Set expectations: this is convenience scheduling, not a guaranteed unattended scraper. For that, you need Tier 2.

## Tier 2 — Full self-hosted pipeline (the serious build)

For someone who wants scans to run twice a day, every day, untouched — classifying results with a model and texting them the matches — that's a real always-on system. It's the difference between "Cowork reminds me and helps when I'm there" and "a machine does it whether I'm there or not."

Don't try to build this inside Cowork. Instead, when the user asks what it would take, walk them through the blueprint in `references/full-pipeline-blueprint.md`. It covers the components, the rough effort, the ongoing cost, and the maintenance reality — drawn from a working production system. Summarize the shape of it, then offer the full blueprint if they're serious.

The one-line version: a dedicated always-on computer runs a scheduled script that fetches the board with a headless browser, classifies each role with a cheap LLM API call against your saved preferences, dedupes against a running list, and pushes matches to you (text/email/Slack) plus a tracker. Roughly $1–2/month in API cost, a weekend or two to build, and ongoing upkeep when the job board changes its HTML.

## How to talk about this

- **Lead with Tier 1.** It's what most people should do, and it's a two-minute setup.
- **State the catch plainly.** The browser-session limitation is real; don't sell unattended reliability the lightweight tier can't deliver.
- **Don't auto-create anything.** Offer to set up the scheduled task; create it only on a clear yes, with a confirmed cadence.
- **Tier 2 is opt-in and serious.** Present it as a blueprint for the ambitious, not a recommendation. Be honest that it's an engineering project with real maintenance.
