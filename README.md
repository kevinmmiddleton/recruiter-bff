<p align="center">
  <img src="https://github.com/kevinmmiddleton/recruiter-bff/raw/main/assets/brand/banners/github-social-1280x640.png" alt="Recruiter BFF. A recruiter that works for you." width="640">
</p>

<p align="center">
  <a href="https://github.com/kevinmmiddleton/recruiter-bff/releases/latest"><img alt="Download the latest release" src="https://img.shields.io/badge/download-latest-5FD6A4?style=for-the-badge&labelColor=16131F"></a>
  <a href="#install"><img alt="Runs in Claude Cowork and Codex" src="https://img.shields.io/badge/runs%20in-Cowork%20%C2%B7%20Codex-FFE14D?style=for-the-badge&labelColor=16131F"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-FFF8EF?style=for-the-badge&labelColor=16131F"></a>
</p>

# Recruiter BFF

Find out if you're a match before you apply, then walk in prepared.

Paste a job posting and Recruiter BFF checks the key requirements against your resume, scores the match from 1 to 5, names the gaps, and tells you to apply or skip. When you land the interview, it hands you a guide built from your own background.

It's a free plugin for Claude Cowork (with a paid Claude plan and the Claude desktop app) and for Codex (best on a paid ChatGPT plan). It never applies to jobs or contacts anyone for you, and everything lives in plain files on your computer. *Formerly Job Search Agent.*

It runs when you ask, on a normal laptop. Nothing to host: no servers of your own, no scrapers, no always-on machine.

## Walk in prepared

<p align="center"><img src="https://github.com/kevinmmiddleton/recruiter-bff/raw/main/assets/brand/marketing/recruiter-bff-guide-wd-ice.gif" alt="Someone asks Recruiter BFF to prep them for an interview with Fernhill, and it builds a guide for the Senior PM, Growth role: the role in plain words, their fit, and their gap, with the question to expect and how to answer it." width="720"></p>

Tell it you have an interview and paste the posting. Every guide opens with four things, in this order:

- **The role, in plain words:** what they're really hiring for, before the jargon.
- **Your fit:** each requirement matched to something you've actually done.
- **Your gaps:** what they'll ask, the honest answer, what to point to instead, and whether to bring it up first.
- **Questions to ask:** for each person you're meeting, plus the two to ask if you only get two.

Above them: a one-line verdict, the one big risk, and what the next round tests. Below them: a plan for each interviewer, company research with sources, likely questions with answers in your words, scripts for the awkward questions and the pay question, and a method for case rounds.

After each round it debriefs you while it's fresh, updates the guide, and drafts thank-you notes. Say "practice my interview" and it plays the interviewer, with honest critique after every answer. Your best stories go into your story bank, so every guide starts from material you've already polished.

## Your story bank

Every search asks the same questions in different words, first in the application and then in the interview. Your best stories live in a story bank (`interview-stories.md`), in your own words, with the numbers you can stand behind, so you only have to tell each one once.

- **Applications start there.** When an application asks "tell us about a time" or "why us," it starts from the answer you saved last time, or from your best matching story, and adjusts it for this company. It tells you which one it used.
- **So do your interview guides.** It picks the stories each round will ask for and adjusts the emphasis for the role. The facts stay the same, and a story the company already read in your application gets told the same way, with more depth.
- **It spots what's missing.** If a round will ask about a failure and you don't have one ready, it helps you draft one from your real experience.
- **It remembers how they landed.** Each story notes where you've used it, applications included, and your debriefs note how it went.

## Check your fit before you apply

<p align="center"><img src="https://github.com/kevinmmiddleton/recruiter-bff/raw/main/assets/brand/marketing/recruiter-bff-fit-wd-ice.gif" alt="A job posting for Senior PM, Growth at Fernhill gets a fit check: 4.6 out of 5, apply now, with each requirement marked a match, a partial match, or a gap, and what to lead with if you apply." width="720"></p>

Paste a posting, or a link, and ask "should I apply?"

- It checks the posting is still live on the company's own site, and flags postings that look stale.
- It matches every requirement to the line in your background that answers it, and calls partial matches partial.
- It reads the role against what you want, separately: your one-sentence target, your must-haves, your dealbreakers.
- It scores the role from 1 to 5, tells you to apply or skip, and says what to lead with in your note and first conversations if you apply.
- It saves the posting and the evaluation, so the interview guide can start from them later.

## Apply early, to the right roles

Being one of the first 50 applicants beats being a polished 200th. Say "scan for jobs":

- It reads your saved LinkedIn search in a browser you're logged in to (the built-in browser in the Claude or ChatGPT desktop app, or the Claude in Chrome extension), or you paste the results in.
- It builds one-click Google searches of recent posts on company job sites like Greenhouse, Lever, and Ashby, where some roles get posted and never reach LinkedIn.
- It checks the public job feeds of companies on your watchlist.
- It hides your dealbreakers, staffing firms, job aggregators, and postings that don't name the company, says why each match made the cut, and tells you if any source failed.
- It remembers what it showed you, so a role you passed on in a recent scan doesn't come back as new. Say "show them" to see those again.

## Keep track, without a spreadsheet habit

- **Your tracker** is a plain CSV that opens in Excel, Numbers, or Google Sheets. Say "what's in my pipeline?" and you get a table sorted by what needs doing. Close it in your spreadsheet app before you ask Recruiter BFF to change it, so the app doesn't save its older copy over the update.
- **Follow-ups** are flagged when an active process goes quiet (cold applications never nag you), and it offers a short draft.
- **Reminders on your days:** pick the days and time, and it checks in with follow-ups due, interviews coming up, and links to fresh roles. In the Claude app, turn on two settings once so the check-in can read your files (it walks you through them), and keep the app open; quitting it pauses your check-in until you turn it back on. In Codex, check-ins run as scheduled tasks in the ChatGPT desktop app while it's open. In the Codex CLI, you get a check-in the first time you open Codex each day, or a calendar reminder.
- **A weekly review** shows what moved, where things tend to stall, and which sources pay off.

## Your materials, and your people

- **Your materials:** sharpen your primary resume bullet by bullet, written as outcome, then how, then scope (it won't make a new resume for every job); a LinkedIn headline people actually search for; "why us" and "tell us about a time" answers that start from your story bank and couldn't go to any other company. It never invents a number.
- **Contacts:** download your LinkedIn connections and it shows who you know at the companies you're pursuing, suggests one next move per person, and drafts short notes you send yourself.

## Install

### In the Claude desktop app

You need a paid Claude plan (Pro, Max, Team, or Enterprise) and the Claude desktop app for Mac or Windows.

1. Download the plugin: **[recruiter-bff.plugin](https://github.com/kevinmmiddleton/recruiter-bff/releases/latest/download/recruiter-bff.plugin)**
2. In the Claude desktop app, with Chat or Cowork selected (the switch at the top left), open **Customize** in the left sidebar, then the **Plugins** tab. Click **+ Add**, then **Upload plugin**, pick the file, and click **Upload**. You'll see the standard warning for installing a plugin. The plugin's page then has a **Try in Cowork** button.
3. Choose Cowork if your message box shows a Chat/Cowork switch, then connect a folder on your computer for your job search. Setup creates `job-search/` inside it.

The skills are ready in your next conversation. Installing from Chat or Cowork adds them to your whole account, Claude Code sessions in the app included; installing from the Code side adds them to one project only. **To update,** download the new file and upload it the same way. Updates keep everything you've saved.

**If you see "Skill files must have a .skill, .zip, or .md file extension,"** you're on the Skills tab. Use the Plugins tab instead.

### In Codex

<!-- verify on Codex (Mac and Windows) before release, and add the version checked -->
You need Codex, in the ChatGPT desktop app or the Codex CLI, and Python 3 on your computer for the tracker and contacts (on Windows, from python.org or the Microsoft Store). It works best on a paid ChatGPT plan, with GPT-6.1 Sol (the default there). The free plan's model can get scans and fit checks wrong, so if you're on it, check what it hides and how it scores. In a terminal, run:

```
codex plugin marketplace add kevinmmiddleton/recruiter-bff
codex plugin add recruiter-bff@recruiter-bff
```

Then start a new Codex chat in the folder you want to use for your job search and say "set up my job search." **To update,** run `codex plugin marketplace upgrade`. Updates keep everything you've saved.

In the ChatGPT desktop app, Codex can read your saved LinkedIn search in its built-in browser (sign in to LinkedIn there once), and reminders run as scheduled tasks while the app is open. In the Codex CLI, you paste search results in, and reminders are a check-in the first time you open Codex each day, or a calendar file you double-click to add.

## Get started

Say **"set up my job search"** and paste your primary resume (plus an alternate, if you're aiming at a second kind of role). It gives you an honest read on it, drafts your background from it, asks only what's missing (the roles you want, where, your pay floor, your dealbreakers), and builds your searches. Then it offers a first scan.

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

- **In Claude:** a paid Claude plan (Pro, Max, Team, or Enterprise) and the **Claude desktop app** for Mac or Windows. Cowork reaches your folder through the desktop app, so keep the app open while you work and when reminders run. Quitting the app pauses your reminders until you turn them back on in **Scheduled**. Connect a folder on your computer; setup creates `job-search/` there.
- **In Codex:** Codex in the ChatGPT desktop app or the Codex CLI, opened in a folder for your job search, and Python 3 for the tracker and contacts. A paid ChatGPT plan works best.
- **Optional:** a browser your assistant can drive (the built-in browser in the Claude or ChatGPT desktop app, or the Claude in Chrome extension), so scans can read your saved LinkedIn search. Without one, you paste results in. See `CONNECTORS.md`.

## Where your files live

Everything is in a `job-search/` folder inside the folder you connected (in Codex, the folder you opened):

```
job-search/
├── resume/               # your primary resume (and an alternate), plus plain-text copies every tool reads
├── search-profile.md     # your search, pay, dealbreakers, and background (private)
├── looking-for.md        # what you want next, in one page you can share
├── job-tracker.csv       # your tracker; opens in any spreadsheet app
├── scan-history.csv      # roles earlier scans showed, so they don't come back as new
├── interview-stories.md  # your story bank, reused in applications and interviews
├── contacts.csv          # people at companies you're pursuing, and next moves
├── materials/            # answers.md: application answers worth reusing
└── companies/
    └── <company>/        # job-post.md, fit-check.md, interview-guide.md
```

**Your files are yours.** There's no Recruiter BFF server. Your assistant (Claude or Codex) reads these files when you ask, the way it reads anything else you share with it, and writes to them only while doing something you asked for. Installing a new version replaces the plugin's skills and keeps everything you've saved. Everything is plain markdown and CSV, so if you stop using the plugin tomorrow, it's all still readable.

**Coming from 0.4?** The first time you ask it to save something in 1.0, it gives your files the names above if it can, and tells you which ones it renamed. Just asking what's in your pipeline never renames anything, and files you wrote yourself are renamed only if you say yes. Where it can't rename files (Cowork can't from every session), it keeps your current names, which work just as well, and tells you once how to rename them yourself if you'd like. The first time it updates your tracker, it adds two columns: the furthest stage each role reached, and the date of the next thing, filled in from your notes only when a note names one clear upcoming date. The first time it updates your profile, it moves it to the new section names. It tells you each time. Your notes, answers, and entries stay as you wrote them.

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
| `your-materials` | "fix this bullet" | Resume, LinkedIn, and written answers from your story bank, in your voice |
| `contacts` | "who do I know at [company]?" | Your LinkedIn connections matched to your search, and drafts |
| `job-search-automation` | "remind me on Mondays" | Reminders and scheduled scans (in Claude or Codex), and the self-hosted option |

## Credits

The scored evaluation (dimension scores with action tiers, every requirement traced to your background) and the STAR+R story bank are adapted from [career-ops](https://github.com/career-ops-hq/career-ops) by santifer (MIT), worth knowing about if you want an always-on version of this workflow.

The preferences page, the one-sentence target, and the early-conversation questions are adapted from Phyl Terry's book *Never Search Alone: The Job Seeker's Playbook*. The wording here is the plugin's own.

Made by [Kevin Middleton](https://middleton.io). Free and open source under the MIT license. More at [middleton.io/recruiter-bff](https://middleton.io/recruiter-bff/).
