![Job Search Agent. Turn Claude into your job search assistant.](https://github.com/kevinmmiddleton/job-search-agent/raw/main/banner.svg)

# Job Search Agent

A lightweight, on-demand job search toolkit for Cowork. No servers, no scrapers, no always-on machine. Everything runs when you ask it to, from a normal laptop.

If you've ever seen a "job search automation" setup that needs a dedicated computer running 24/7, a headless browser, a database, and a notification bridge — this is the opposite of that. Same ideas, none of the infrastructure. You point it at a search you trust, it pulls fresh results when you ask, filters them against what you actually want, and keeps a simple file-based record of where everything stands.

## What it does

- **Set up a search** — captures your target roles, location, comp floor, and dealbreakers once, then builds a reusable saved-search link plus one-click, recency-filtered Google searches scoped to company ATS boards (Ashby, Greenhouse, Lever, and more).
- **Scan on demand** — opens your saved search in your own logged-in browser, reads the current results, filters out the noise, and shows you the matches with a quick fit read. It also sweeps your ATS board searches — most roles are posted straight to a company's ATS and never hit LinkedIn — and companies you name on a watchlist get pulled directly through their public ATS job feeds, no browser needed.
- **Score a posting** — paste a JD (or drop a link) and get a 1–5 scored evaluation: every requirement mapped to the specific line in your background that answers it, honest partials and gaps included, ending in a clear apply-or-skip verdict.
- **Track applications** — a plain CSV in your own folder records every role: prospect, applied, interviewing, rejected. Opens in Excel, Numbers, or Google Sheets. Also gives you a pipeline scorecard and flags follow-ups going stale.
- **Prep for interviews** — paste a job description and get a full, role-specific interview guide: company research, role analysis, fit mapping against your background, scripted answers, smart questions to ask, and red flags to probe. Behavioral stories accumulate in a story bank, so every guide reuses material you've already polished instead of starting from zero.
- **Automate it (optionally)** — explains how to run the scan on a schedule with a Cowork scheduled task (no hardware), and what it would take to build a full always-on pipeline if you ever want to.

## Install

Download the plugin: **[job-search-agent.plugin](https://github.com/kevinmmiddleton/job-search-agent/releases/latest/download/job-search-agent.plugin)**

Then open Cowork and drag the file into the window, or go to **Settings → Capabilities → Install plugin** and select it.

That's the whole install. The six skills below will be available the next time you start a conversation.

## First-time setup

Say **"set up my job search"**. It asks a handful of questions about what you're looking for and your background (about five minutes), saves a profile, and helps you build a saved search. Every other tool reads that profile, so you only answer once.

## How to use

- "Set up my job search" → onboarding + saved search
- "Scan for jobs" / "any new roles?" → on-demand scan against your saved search + watchlist
- "Should I apply to this?" + paste a JD → scored evaluation with a verdict
- "I applied to X" / "what's in my pipeline?" → tracker
- "Prep me for my interview with [Company]" + paste the JD → interview guide
- "Can this run automatically?" → automation options

## What you need

- **Cowork** (the desktop app).
- **A browser Claude can drive** for the scan step — the Claude-in-Chrome extension. If you don't have it, the scan falls back to a paste-the-results flow that works for everyone. See `CONNECTORS.md`.
- **A folder Cowork can write to** for your profile and tracker. Setup creates a `job-search/` folder there.

## Where your data lives

Everything stays in your own Cowork folder, in a `job-search/` subfolder:

```
job-search/
├── profile.md              # your search prefs + background (you control this)
├── applications.csv        # your tracker — opens in any spreadsheet app
├── story-bank.md           # your interview stories, reused across guides
└── interviews/
    └── <company>/guide.md  # interview guides
```

Nothing leaves your machine except the web searches and page reads you'd do anyway.

**Your files vs. the plugin's files.** Everything under `job-search/` is yours: the plugin reads these files and only writes to them when you say so in conversation — never silently, and never as part of a plugin update. Updating or reinstalling the plugin replaces only the plugin's own skills, never your data. The files are plain markdown and CSV, so if you stop using the plugin tomorrow, your profile, tracker, stories, and guides remain readable with no export step.

## The six tools

| Tool                     | Trigger                       | What it does                                              |
| ------------------------ | ----------------------------- | --------------------------------------------------------- |
| `job-search-setup`       | "set up my job search"        | Onboards your profile and builds a saved search           |
| `find-jobs`              | "scan for jobs"               | Pulls and filters fresh roles on demand                   |
| `evaluate-role`          | "should I apply to this?"     | Scores one posting against your profile, with a verdict   |
| `application-tracker`    | "I applied", "what's pending" | Maintains your CSV tracker + pipeline status              |
| `interview-guide-engine` | paste a JD, "prep me"         | Generates a role-specific interview guide                 |
| `job-search-automation`  | "automate this"               | Sets up scheduled scans + explains the full-pipeline path |

## Credits

The scored-evaluation approach (dimension scores with action tiers, requirement-by-requirement traceability) and the STAR+R story bank are ideas adapted from [career-ops](https://github.com/santifer/career-ops) by santifer (MIT) — a tool worth knowing about if you want the full always-on version of this workflow. The adaptations here are rewritten for this plugin's local, on-demand design.
