---
name: job-search-automation
description: >
  Sets up reminders and scheduled scans, and explains what a fully automatic job search would
  take. Use when the user says "remind me," "check in with me on Mondays," "set up reminders,"
  "change my reminders," "stop my reminders," "automate my job search," "can this run
  automatically," "schedule my scan," "run this every morning," or asks what it would take to
  build an always-on pipeline. Covers reminders on the user's chosen days (reliable, reads only
  their files), a scheduled scan (convenient, with a catch), and the serious self-hosted build.
---

# Job Search Automation

Help the user decide how hands-off they want their search to be, set up what fits, and be honest about the limits before they rely on it.

Three options, from most reliable to most ambitious:

1. **Reminders on your days.** A check-in on the days and time the user picks. It reads only their files, so it works every time it runs. Most people should start here.
2. **A scheduled scan.** Cowork runs the job scan on a schedule. Convenient, with a real catch.
3. **A self-hosted pipeline.** An always-on machine that scans and texts matches. A genuine engineering project.

## Never

- Never create a scheduled task without a clear yes and confirmed days and time.
- Never let a scheduled task apply to anything, send anything, or contact anyone. Reminders and digests only.
- Never promise a schedule fires when it can't. Say how it really runs.

## How schedules run (say this every time you set one up)

Scheduled tasks run while the Claude desktop app is open. If the app is closed when one is due, it runs the next time the app opens. So "Monday at 8:30" really means "Monday at 8:30 if Claude is open, or as soon as you open it after that."

## 1. Reminders on your days

### What a reminder covers

- **Coming up:** interviews and deadlines in the next 7 days (from the tracker's `next_date`), each with its date, weekday, and the path to its interview guide if one exists.
- **Follow-ups due:** active processes (screening, interview, final, offer) that have gone quiet, using the tracker's ladder: nudge at 7 to 13 days, chase or close at 14 to 29, "mark ghosted?" at 30 or more. Cold applications never appear here.
- **Roles you meant to apply to:** prospects scored 4 or higher, added in the last 14 days, not yet applied to or skipped, at companies that haven't already rejected or closed out the user.
- **People to get back to:** from `contacts.csv`, if it exists: next moves due in the next 7 days or overdue.
- **Fresh roles:** the user's one-click company job site search links from the profile, plus a line: "Say 'scan for jobs' when you're at your computer to check your saved search too."

If nothing is due, the reminder is one line plus the fresh-role links. Keep it short enough to read on a phone in 20 seconds.

### Setting it up

1. Ask which days and what time. Offer a sensible default: weekdays at 8:30am, or Monday, Wednesday, and Friday. If a time could be morning or evening ("8:30"), assume morning and say so in your reply. Times are the computer's local time zone.
2. Turn it into a cron expression in that local time: weekdays at 8:30 is `30 8 * * 1-5`; Mon and Thu at 8:30 is `30 8 * * 1,4`.
3. Find the full path to the user's `job-search/` folder: the Cowork working folder's path plus `job-search/` (run `pwd` in that folder if you need it). The task starts fresh each time with no memory of this conversation, so the prompt must name the folder.
4. Create the task with the scheduled-tasks tool, using the prompt below with the path and the user's name filled in. Title it something the user will recognize, like "Job search check-in."
5. Record it in the Reminders status of `job-search/profile.md`: "Mon and Thu at 8:30am (created YYYY-MM-DD)".
6. Tell the user: when it runs, how schedules really run (above), and that they can say "change my reminders" or "stop my reminders" anytime.

**If the scheduled-tasks tool isn't available,** say so plainly: "I can't create scheduled tasks from here." Give the user the title, the schedule in words, and the prompt, so they can set it up from Cowork's scheduled tasks themselves. Record the Reminders status as "requested Mon and Thu at 8:30am, not created yet (YYYY-MM-DD)", so nobody offers reminders again and a later conversation can finish the job.

**Task prompt** (fill in the bracketed parts):

```
Job search check-in for [name]. Their files are in [full path to job-search/].

Read applications.csv, profile.md, and contacts.csv (if it exists) there. Do not change any
file, apply to anything, send anything, or contact anyone. Today's date and weekday come from
the system.

Write a short check-in, plain text, in this order, skipping empty sections:

1. Coming up (next 7 days): rows whose next_date falls within 7 days. For each: weekday and
   date, company, role, what it is (from status and the last entry in notes; entries are
   separated by " | ", newest last), and the path interviews/<company>/guide.md if it exists.
2. Follow-ups due: rows with status screening, interview, final, or offer, whose next_date is
   blank or in the past, and whose last_update is 7 or more days ago. Say "nudge" for 7 to 13
   days, "chase or close" for 14 to 29, "mark ghosted?" for 30 or more. Never include rows
   with status applied.
3. Roles you meant to apply to: status prospect, score 4 or higher, date_added within the
   last 14 days, and no rejected or closed row for the same company.
4. People to get back to: rows in contacts.csv whose next_date is today, past, or within 7
   days, and whose next_move isn't "none". For each: name, company, next move.
5. Fresh roles: copy the links from the "Company Job Site Searches" section of profile.md,
   then add: "Say 'scan for jobs' when you're at your computer to check your saved search too."

If sections 1 to 4 are all empty, write "Nothing due today." and then section 5.
Use real dates with weekdays (Tue Oct 13), never "next week." No more than about 15 lines.
If section 2 or 4 has anything, end with one offer: to draft those messages. Otherwise end
with section 5.
```

### Changing or stopping

"Change my reminders": list the user's scheduled tasks, find the check-in, and update its schedule (or prompt) after confirming the new days and time. "Stop my reminders": find it and disable or delete it after confirming. Update the profile's Reminders status either way. If the status says "not created yet," there's nothing to change: offer to create it now, or update the requested days and time.

## 2. A scheduled scan

Cowork can also run the scan itself on a schedule: load the profile, pull the saved search, filter and check against the tracker, and give a digest of new matches.

**The catch, stated plainly:** the scan reads LinkedIn through the user's own logged-in browser. A task that runs while they're away may not have a browser it can drive, so that part can fail or come back empty. What works better unattended:

- **The company job site searches** from setup are public Google searches with recency built into the URL. No login, so they're the most reliable unattended source.
- **The watchlist** reads public job feeds directly, no browser needed.
- **Or treat the run as a nudge:** the task sends the links and reminds the user to run the full scan when they're at their computer. For most people, reminders (option 1) already do this.

If they still want it, set it up like a reminder: confirm days and time, then create a task with a self-contained prompt such as:

```
Run a job scan for [name]. Their files are in [full path to job-search/]. Read profile.md and
applications.csv. Check the company job site searches and the companies to watch in
profile.md, filter the results against the profile's targets and exclusions, drop roles
already in applications.csv, and write a short digest of new matches, strongest first, each
with company, role, location, one line on why it fits, and the link. If a source fails, say
which one. Do not apply to anything, send anything, or change any file.
```

## 3. A self-hosted pipeline

For someone who wants scans twice a day, every day, untouched, with matches texted to them, that's a real always-on system. It's the difference between "Claude reminds me and helps when I'm there" and "a machine does it whether I'm there or not."

Don't build this inside Cowork. When the user asks what it would take, summarize the blueprint in `references/full-pipeline-blueprint.md`: the parts, the effort, the cost, and the upkeep. Offer the full blueprint if they're serious.

The one-line version: an always-on computer runs a scheduled script that loads the job board in a headless browser, classifies each role with a cheap model call against the user's preferences, checks it against a running list, and sends matches by text or email, plus a tracker. Roughly $1 to $2 a month in model costs, a weekend or two to build, and ongoing upkeep when the job board changes its pages.

## How to talk about this

- **Lead with reminders.** They're reliable and take two minutes.
- **State how schedules run.** The app has to be open, and a missed run happens at the next launch.
- **The scheduled scan is convenience, not a guarantee.** Say why.
- **The self-hosted pipeline is opt-in and serious.** A blueprint for the ambitious, with real upkeep.
