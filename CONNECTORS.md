# What Recruiter BFF connects to

Very little, on purpose. It works with tools you already have, and every step has a way to work without the optional pieces.

## A browser Claude can drive (optional, for scans)

The scan reads your saved LinkedIn search the way you'd see it. The best way is the **Claude in Chrome extension**: Claude opens your saved search in your own logged-in Chrome and reads the results, including roles behind your login.

Without the extension, the scan asks you to open the search yourself and paste the results in. Slower, no setup, works on any computer.

Recruiter BFF never logs in to anything for you and never stores passwords. It only reads pages in a browser session you already control.

## Web search (for interview research and company job sites)

Interview guides research the company and check recent news with Claude's web search. The company job site searches are ordinary Google searches you (or Claude, in your browser) open. Watchlist companies are read from the public job feeds that Greenhouse, Lever, and Ashby publish for every company, with no login.

## Scheduling (optional, for reminders and scheduled scans)

Reminders and scheduled scans use Cowork's built-in scheduled tasks. No extra connector. Scheduled tasks run while the Claude desktop app is open; if it's closed when one is due, it runs the next time the app opens.

## Your LinkedIn connections (optional, for contacts)

The contacts skill reads `Connections.csv`, a file you download yourself from LinkedIn (Settings & Privacy → Data privacy → Get a copy of your data → Connections). No connector and no login: the file stays in your folder.

## Job boards

Examples use **LinkedIn**, because its search links are easy to save and reuse. The same approach works for Indeed, Built In, Wellfound, a company's careers page, or any board with a stable search link. Setup helps you build the link for the board you use.
