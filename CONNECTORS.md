# What Recruiter BFF connects to

Very little, on purpose. It works with tools you already have, and every step has a way to work without the optional pieces.

## A browser Claude can drive (optional, for scans)

The scan reads your saved LinkedIn search the way you'd see it, in a browser Claude can drive. Two ways (for Codex, see "In Codex" below):

- **The browser built into the Claude desktop app.** Sign in to LinkedIn there once, and Claude reads your search the same way. (You can import your logins instead: from Chrome, Edge, or Firefox on a Mac, or from Firefox on Windows.)
- **The Claude in Chrome extension.** Claude opens your saved search in your own logged-in Chrome and reads the results, including roles behind your login.

Without either, the scan asks you to open the search yourself and paste the results in. Slower, no setup, works on any computer.

Recruiter BFF never logs in to anything for you and never stores passwords. It only reads pages in a browser session you already control.

## Web search (for interview research and company job sites)

Interview guides research the company and check recent news with Claude's web search. The company job site searches are ordinary Google searches you (or Claude, in your browser) open. Watchlist companies are read from the public job feeds that Greenhouse, Lever, and Ashby publish for every company, with no login.

## Scheduling (optional, for reminders and scheduled scans)

Reminders and scheduled scans use Cowork's built-in scheduled tasks. No extra connector. A scheduled task reaches your `job-search/` folder only while your computer is awake and the Claude desktop app is open on it. With the app closed, a check-in either doesn't run or can't reach your files; when it runs and can't reach them, it tells you so, and it never says "Nothing due today" without reading your tracker. A scheduled scan checks your watchlist's public job feeds whenever it can reach the web (they need no browser or login); your saved LinkedIn search and the company job site searches need a browser Claude can drive, so without one the scan sends you those links instead.

## In Codex

The same pieces work in Codex, with Codex's own tools:

- **A browser.** In the ChatGPT desktop app, Codex can drive its built-in browser: sign in to LinkedIn there once, and scans read your saved search. The Codex CLI has no browser it can drive, so you open your saved search yourself and paste the results in.
- **Web search** is a Codex setting that may be off. Without it, interview guides build the company section from the posting and give you a short research list.
- **Watchlist feeds** are fetched with `curl` when Codex's network access is on. When it's off, the scan says the watchlist wasn't available instead of reporting no new roles.
- **Scheduling.** In the ChatGPT desktop app, reminders and scheduled scans are Codex scheduled tasks. They run while your computer is on and the app is running, and each run shows up under **Scheduled** in the app's sidebar. They use your default sandbox setting: a check-in only reads, so it works in any setting, but a scheduled scan needs network access for the watchlist. The Codex CLI can't schedule anything, so reminders there are a check-in the first time you open Codex in your folder each day (a short section in that folder's `AGENTS.md`), or a calendar event you add with one click.

## The no-install kit

ChatGPT, Microsoft Copilot, Gemini, and Claude without Cowork connect to nothing here. You paste in your resume, job postings, and search results, and it hands you files to keep when you say "wrap up."

## Your LinkedIn connections (optional, for contacts)

The contacts skill reads `Connections.csv`, a file you download yourself from LinkedIn (Settings & Privacy → Data privacy → Get a copy of your data → Connections). No connector and no login: the file stays in your folder.

## Job boards

Examples use **LinkedIn**, because its search links are easy to save and reuse. The same approach works for Indeed, Built In, Wellfound, a company's careers page, or any board with a stable search link. Setup helps you build the link for the board you use.
