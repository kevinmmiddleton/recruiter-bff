---
name: application-tracker
description: >
  Keeps the user's job applications in a plain CSV in their own folder and reports on the
  pipeline. Use when the user says "I applied to X," "add this to my tracker," "what's in my
  pipeline," "show my applications," "show me the table," "what's pending," "update the status
  of," "I got a rejection from," "they paused the role," "what's stale," "follow-ups," "who
  should I follow up with," "weekly review," "how's my search going," or "help me write a
  thank-you note." Also logs scan matches as prospects. The CSV opens in Excel, Numbers, or
  Google Sheets.
---

# Application Tracker

A tracker that's just a file the user owns: `job-search/applications.csv` in their Cowork folder. No database, no server. You keep it accurate, and you read it back like a coach who knows what needs doing next.

## Never

- Never send anything. Follow-ups and thank-you notes are drafts; the user sends them.
- Never guess which application an update or a rejection belongs to. Ask.
- Never delete rows. Rows that are done stay, so scans don't show them again and the history stays honest.
- Never record a pause or a cancelled role as a rejection.
- Never lecture about how many applications the user is sending.

## The file

Columns, in order:

```
company,role,location,comp,url,source,status,score,date_added,date_applied,last_update,notes,furthest_stage,next_date
```

Statuses: `prospect`, `applied`, `screening`, `interview`, `final`, `offer`, `rejected`, `closed`, `hold`, `ghosted`, `withdrawn`, `skipped`. Full meanings, the matching rules, and the Python snippets are in `references/tracker-schema.md`. Read it before your first write in a conversation.

Older trackers have no `furthest_stage` or `next_date` columns. The snippets add them on the next write and change nothing else. Tell the user once, in a sentence.

**Edit with Python, never by hand.** Hand-typed CSV rows break on commas and quotes. Use the snippets (they load, change, and save the whole file in one step, and keep any columns the user added). Read the file back after every write and say exactly what changed.

## Recording things

**Prospects from a scan or an evaluation.** Append with `status=prospect`, the score, and the source. Exact duplicates (same company, same role after normalizing) are skipped. A different role at a company already in the tracker is a new row.

**"I applied to X."** If X is a prospect, move it to `applied` and set `date_applied`. If it isn't tracked, add it, then mark it applied. Put the resume version or anything else they mention in `notes`.

**Moving forward.** Screens, interviews, finals, offers: update `status` and `last_update`, raise `furthest_stage`, and set `next_date` when there's a date ("screen Thursday" means next Thursday's date; work it out from today and say the date back). Add a dated note with any context.

**Honest endings.**
- The company said no: `rejected`.
- The posting came down, or someone was hired before the user was considered, or the role was cancelled: `closed`.
- "We've paused the search": `hold`. A pause isn't a no.
- An active process went silent for a month or more: suggest `ghosted`, and only change it on a yes. If they reply later, move it back.
- The user pulled out: `withdrawn`. Decided not to apply: `skipped`.

**Rejections.** Follow the safe rules in the schema file: only applications sent on or before the rejection, the exact role when the email names one, and a "which one?" question when a general no could mean more than one open application at that company. Leave `furthest_stage` where it was. Acknowledge a rejection in one line and move on; don't dwell, and don't spin it.

## The pipeline table (on demand)

When the user asks "what's in my pipeline?", "show my applications," or "show me the table," show the roles as a table. The CSV is the record; the table is just a view of it.

```
| Company | Role | Status | Score | Last update | Next step |
|---|---|---|---|---|---|
| Fernhill | Senior PM, Growth | interview | 4.6 | 3 days ago | Prep: hiring manager round Tue Oct 13 |
| Northstar | Senior PM, Retention | screening | 4 | 9 days ago | Nudge the recruiter |
| Acme | Product Lead | prospect | 4 | today | Decide: apply or skip |
```

- **Order by what needs action:** offers, then anything with a `next_date` in the next 7 days, then follow-ups due (per the ladder), then the rest of the active processes, then `applied`, then prospects.
- **Next step** comes from the row: an upcoming date ("Prep: panel Fri Oct 16"), the follow-up ladder ("Nudge," "Chase or close," "Mark ghosted?"), "Decide: apply or skip" for prospects, "Waiting" for a recent application.
- **Leave finished rows out by default** (rejected, closed, withdrawn, skipped, ghosted) and give one line of counts under the table instead: "Plus 12 finished: 7 rejected, 3 closed, 2 skipped." Show them if the user asks for everything.
- **Long pipelines:** if there are more than about 25 open rows, show the top 25 and say how many more.
- Use real dates with the weekday ("Tue Oct 13"), never just "next week."

Under the table, at most three lines of what matters most this week. That's it.

## Follow-ups

Follow-ups apply to **active processes only** (screening, interview, final, offer). A cold application that hasn't heard back gets no flag: silence there is normal.

Use the ladder in the schema file: nudge at 7 to 13 days quiet, chase or close at 14 to 29, ask about ghosted at 30 or more. A future `next_date` means it isn't quiet yet.

When a nudge is due, offer to draft it. Keep it short and friendly, and give them something: one line on why the user is still excited, or one small, concrete thought tied to their product. Never more than one follow-up suggestion per role per conversation.

## Thank-you notes

After the user logs an interview (or finishes a debrief), offer once: "Want thank-you notes for the people you met?"

- One note per interviewer, plus the recruiter.
- Each one names something specific from that conversation, ties it back to the role in one line, and stays under about 120 words.
- If the role might pause or close, add a light "keep me in mind for what comes next."
- Pull names and details from the guide's round notes when they exist. If you don't know who was there, ask.
- Drafts only. The user sends them, ideally the same day.

## Weekly review

When the user asks for a weekly review, or "how's my search going," read the whole file and report like a coach:

1. **This week:** applications sent, processes that moved forward, rejections, what's coming up (with dates), and, if `job-search/contacts.csv` exists, conversations held and messages sent (from `last_contact` dates). Keep scheduling conversations even in busy interview weeks, so the next week isn't empty.
2. **Open loops:** every active process with its next step, and anything the user promised to send (look in `notes` for promised follow-ups and in the company folders for unsent drafts).
3. **Where things stall:** count `furthest_stage` across finished rows. "Most of your finished processes ended after the recruiter screen" is useful. Only say it when there are enough rows to mean something (about 8 or more).
4. **By source:** which sources produced screens and interviews (from `source` and `furthest_stage`), so the user can spend time where it pays off. If a source never produces anything after a few weeks, say so once.
5. **One process carrying everything:** if one company is the only active process past the screen, say so warmly and suggest keeping a few more moving, so one no doesn't empty the pipeline.
6. **Your preferences:** if `job-search/preferences.md` exists, ask one question: "Is anything in your preferences changing?" Searches teach people what they want.

Notice the effort, not just the outcomes. A week with no interviews but steady applications is still a real week. Keep the whole review skimmable, and never repeat a suggestion the user already declined.

## Exporting

The tracker is already a CSV, so it opens in Excel, Numbers, or Google Sheets as is. If the user wants a formatted spreadsheet (tabs, filters, colors), offer to build one with the xlsx skill from the same data. The CSV stays the source.

## Principles

- **The user owns the file.** They can edit it by hand, sort it, or open it anywhere. Read before you write, and respect their edits.
- **One source of truth.** Prospects, applications, and outcomes all live in one file with a status column.
- **Coach, don't clerk.** Lead with what needs action. The tracker exists to move the search forward.
