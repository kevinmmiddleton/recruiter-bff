<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/kevinmmiddleton/recruiter-bff/raw/main/assets/brand/svg/recruiter-bff-horizontal-white.svg">
    <img src="https://github.com/kevinmmiddleton/recruiter-bff/raw/main/assets/brand/svg/recruiter-bff-horizontal.svg" alt="Recruiter BFF. A recruiter that works for you." width="300">
  </picture>
</p>

# Recruiter BFF

A recruiter that works for you. *Formerly Job Search Agent.*

Find out if you're a match before you apply, then walk in prepared. Recruiter BFF is a free plugin for Claude. Paste a job posting and it tells you how you really stack up, gaps included, and whether to apply. It never applies to jobs or contacts anyone for you. When the interview comes, it hands you a guide built from your own background. Everything lives in plain files on your computer.

It runs when you ask, in Claude Cowork with the Claude desktop app (Mac or Windows), on a normal laptop. Nothing to host: no servers of your own, no scrapers, no always-on machine.

## Walk in prepared

Tell it you have an interview and paste the posting. Every guide opens with four things, in this order:

- **The role, in plain words:** what they're really hiring for, before the jargon.
- **Your fit:** each requirement matched to something you've actually done.
- **Your gaps:** what they'll ask, the honest answer, what to point to instead, and whether to bring it up first.
- **Questions to ask:** for each person you're meeting, plus the two to ask if you only get two.

Above them: a one-line verdict, the one big risk, and what the next round tests. Below them: a plan for each interviewer, company research with sources, likely questions with answers in your words, scripts for the awkward questions and the pay question, and a method for case rounds.

After each round it debriefs you while it's fresh, updates the guide, and drafts thank-you notes. Say "practice my interview" and it plays the interviewer, with honest critique after every answer. Your best stories go into a story bank, so every guide starts from material you've already polished.

## Check your fit before you apply

Paste a posting, or a link, and ask "should I apply?"

- It checks the posting is still live on the company's own site, and flags postings that look stale.
- It matches every requirement to the line in your background that answers it, and calls partial matches partial.
- It reads the role against what you want, separately: your one-sentence target, your must-haves, your dealbreakers.
- It scores the role from 1 to 5, tells you to apply or skip, and says what to lead with if you apply.
- It saves the posting and the evaluation, so the interview guide can start from them later.

## Apply early, to the right roles

Being one of the first 50 applicants beats being a perfectly tailored 200th. Say "scan for jobs":

- It reads your saved LinkedIn search in a browser you're logged in to (the Claude desktop app's built-in browser, or the Claude in Chrome extension), or you paste the results in.
- It builds one-click Google searches of recent posts on company job sites like Greenhouse, Lever, and Ashby, where lots of roles get posted and never reach LinkedIn.
- It checks the public job feeds of companies on your watchlist.
- It hides your dealbreakers, staffing firms, and job aggregators, says why each match made the cut, and tells you if any source failed.

## Keep track, without a spreadsheet habit

- **Your tracker** is a plain CSV that opens in Excel, Numbers, or Google Sheets. Say "what's in my pipeline?" and you get a table sorted by what needs doing. Close it in your spreadsheet app before you ask Claude to change it, so the app doesn't save its older copy over the update.
- **Follow-ups** are flagged when an active process goes quiet (cold applications never nag you), and it offers a short draft.
- **Reminders on your days:** pick the days and time, and it checks in with follow-ups due, interviews coming up, and links to fresh roles.
- **A weekly review** shows what moved, where things tend to stall, and which sources pay off.

## Your materials, and your people

- **Your materials:** resume bullets rewritten as outcome, then how, then scope; a LinkedIn headline people actually search for; "why us" answers that couldn't go to any other company. It never invents a number.
- **Contacts:** download your LinkedIn connections and it shows who you know at the companies you're pursuing, suggests one next move per person, and drafts short notes you send yourself.

## Install

You need a paid Claude plan (Pro, Max, Team, or Enterprise) and the Claude desktop app for Mac or Windows.

1. Download the plugin: **[recruiter-bff.plugin](https://github.com/kevinmmiddleton/recruiter-bff/releases/latest/download/recruiter-bff.plugin)**
2. In the Claude app, open **Customize**, then **Plugins**, then **Add**, then **Upload plugin**, and pick the file. <!-- verify the exact button names in the app on release day -->
3. Choose Cowork if your message box shows a Chat/Cowork switch, then connect a folder on your computer for your job search. Setup creates `job-search/` inside it.

The skills are ready in your next conversation. **To update,** download the new file and upload it the same way. Updates keep everything you've saved.

## Get started

Say **"set up my job search"** and paste your resume. It drafts your background from the resume, asks only what's missing (the roles you want, where, your pay floor, your dealbreakers), and builds your searches. Then it offers a first scan.

Later, when you have half an hour, it can help you write a one-page "what I want next" to share with people who can help. It ends in one sentence that makes it easy for anyone to keep an eye out for you.

## Say it in plain words

| Say | What happens |
| --- | --- |
| "Set up my job search" | Setup, starting from your resume |
| "Scan for jobs" | Fresh roles from your searches and watchlist, filtered to you |
| "Should I apply to this?" | A scored fit check with an apply-or-skip answer |
| "Prep me for my interview with [company]" | An interview guide for every round |
| "Here's how the interview went" | A debrief, an updated guide, and thank-you drafts |
| "Practice my interview" | A mock interview with critique |
| "What's in my pipeline?" | Your tracker as a table, sorted by what needs doing |
| "Who do I know at [company]?" | Matches from your LinkedIn connections, and a next move |
| "Fix this resume bullet" | A truthful rewrite in your voice |
| "Remind me on Mondays and Thursdays" | Check-ins on your days |

## What you need

- **A paid Claude plan** (Pro, Max, Team, or Enterprise) and the **Claude desktop app** for Mac or Windows. Cowork reaches your folder through the desktop app, so keep the app open while you work and when reminders run.
- **A folder on your computer, connected in Claude.** Setup creates `job-search/` there.
- **Optional:** a browser Claude can drive (the Claude desktop app's built-in browser, or the Claude in Chrome extension), so scans can read your saved LinkedIn search. Without one, you paste results in. See `CONNECTORS.md`.

## Where your files live

Everything is in a `job-search/` folder inside the folder you connected:

```
job-search/
├── resume/               # your resume files, plus a plain-text copy every tool reads
├── search-profile.md     # your search, pay, dealbreakers, and background (private)
├── looking-for.md        # what you want next, in one page you can share
├── job-tracker.csv       # your tracker; opens in any spreadsheet app
├── interview-stories.md  # your interview stories, reused across guides
├── contacts.csv          # people at companies you're pursuing, and next moves
├── materials/            # written answers worth reusing
└── companies/
    └── <company>/        # job-post.md, fit-check.md, interview-guide.md
```

**Your files are yours.** There's no Recruiter BFF server. Claude reads these files when you ask, the way it reads anything else you share with it, and writes to them only while doing something you asked for. Installing a new version replaces the plugin's skills and keeps everything you've saved. Everything is plain markdown and CSV, so if you stop using the plugin tomorrow, it's all still readable.

**Coming from 0.4?** The first time you use 1.0, it gives your files the names above if it can. Where it can't rename files (Cowork can't from every session), it keeps your current names, which work just as well, and tells you once how to rename them yourself if you'd like. The first time it updates your tracker, it adds two columns: the furthest stage each role reached, and the date of the next thing, filled in from your notes only when a note names one clear upcoming date. The first time it updates your profile, it moves it to the new section names. It tells you each time. Your notes, answers, and entries stay as you wrote them.

**Had Job Search Agent?** Uninstall it first, so only one of them answers.

**It never acts for you.** It never applies to a job, sends a message, or contacts anyone. You decide, and you hit send.

## The eight skills

| Skill | Say | What it does |
| --- | --- | --- |
| `job-search-setup` | "set up my job search" | Builds your profile from your resume, your searches, and your preferences page |
| `find-jobs` | "scan for jobs" | Pulls and filters fresh roles on demand |
| `evaluate-role` | "should I apply to this?" | Checks a posting is live, scores it, and saves it |
| `interview-guide-engine` | "prep me for my interview" | Guides, debriefs, practice, and the story bank |
| `application-tracker` | "what's in my pipeline?" | Your tracker, follow-ups, weekly review, thank-you drafts |
| `your-materials` | "fix this bullet" | Resume, LinkedIn, and written answers, in your voice |
| `contacts` | "who do I know at [company]?" | Your LinkedIn connections matched to your search, and drafts |
| `job-search-automation` | "remind me on Mondays" | Reminders, scheduled scans, and the self-hosted option |

## Credits

The scored evaluation (dimension scores with action tiers, every requirement traced to your background) and the STAR+R story bank are adapted from [career-ops](https://github.com/career-ops-hq/career-ops) by santifer (MIT), worth knowing about if you want an always-on version of this workflow.

The preferences page, the one-sentence target, and the early-conversation questions are adapted from Phyl Terry's book *Never Search Alone: The Job Seeker's Playbook*. The wording here is the plugin's own.

Made by [Kevin Middleton](https://middleton.io). Free and open source under the MIT license.
