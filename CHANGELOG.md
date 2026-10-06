# Changelog

## 0.4.1 (2026-10-06)

- **Fix: the first status update no longer wipes an empty tracker.** If you logged "I applied" before the tracker had any rows, the update step could rewrite `applications.csv` with no header at all. It now keeps the header row whether or not the file has rows yet.

## 0.4.0 (2026-10-06): Recruiter BFF

- **New name.** Job Search Agent is now Recruiter BFF: a recruiter that works for you. The GitHub repo moved to `kevinmmiddleton/recruiter-bff`, and old links redirect.
- **New look.** The brand kit lives in `assets/brand/`: logo, app icon, favicon, and colors. The README uses the new logo, with a white version for dark mode. Five share banners (link preview, GitHub, wide, square, portrait) live in `assets/brand/banners/`.
- **Your files stay put.** Everything still lives in your `job-search/` folder. Nothing moves when you switch.
- **Switching from Job Search Agent:** uninstall Job Search Agent first, then install Recruiter BFF. With both installed, both answer "scan for jobs."

## 0.3.0 (2026-06-22)

- One-click Google searches limited to company job sites (Ashby, Greenhouse, Lever, and more), filtered to recent posts. Free, in your own browser, no API.

## 0.2.0 (2026-06-11)

- Scored evaluations: every posting rated 1 to 5, each requirement mapped to your background, with an apply-or-skip verdict.
- A story bank that interview guides reuse.
- Watchlist companies pulled straight from their public job feeds.
- A clear promise about your data: your files are yours, and updates never touch them.

## 0.1.1 (2026-06-11)

- Added the license field and a `.gitignore`.

## 0.1.0 (2026-06-04)

- First release: setup, on-demand scans, a CSV tracker, interview guides, and optional scheduled scans.
