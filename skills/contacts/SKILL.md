---
name: contacts
description: >
  Helps the user find and use the people who can help their search: matches their LinkedIn
  connections export to companies they're pursuing, picks one next move per person, and drafts
  short, give-first messages they send themselves. Use when the user says "who do I know at
  [company]," "import my LinkedIn connections," "who should I reach out to," "help me ask for a
  referral," "draft a note to [name]," "who can refer me," "surface my applications," "who
  helped my career," "help me reconnect," "ask for an intro," or "who should I follow up with
  this week." Keeps job-search/contacts.csv. Never sends anything.
---

# Contacts

Most hires come through people, not job boards. This skill helps the user see who they already know at the companies they want, decide one next move per person, and send short, specific notes that are easy to say yes to.

## Never

- Never send a message, a connection request, or an intro. Every message is a draft; the user sends it.
- Never claim a relationship that isn't there. No logged contact means "never spoke," however familiar the name.
- Never nudge a hiring manager about a role they rejected the user from.
- Never ask someone to do the user's homework. Show the homework, keep the ask small and specific.
- Never upload or share the user's contacts anywhere. The export and `contacts.csv` stay in their folder.

## The file

`job-search/contacts.csv`: the people who matter to this search, not the whole network. Columns, closeness levels, next moves, and the import code are in `references/contacts-schema.md`. Read it before the first write in a conversation.

## Who do I know there? (the LinkedIn export)

1. If there's no export in the folder yet, walk the user through downloading it (steps in the schema file; about 10 minutes, done by them on LinkedIn).
2. Run the import. It reads `Connections.csv`, matches people to companies the user is pursuing (open rows in the tracker and the watchlist), and adds only those people, as `never-spoke`.
3. Go through the matches company by company: "At Fernhill you're connected to Priya Shah, a talent partner, and Marco Diaz, VP of Product. Do you know either of them?" Set closeness from the answers.
4. Re-run it when the tracker grows. It never adds the same person twice.

People's titles in the export are whatever they last put on LinkedIn, so they can be out of date. Say so when it matters.

## Surface my applications

When the user asks "who can help with my applications," or once a week if they've asked for that:

1. List open applications (applied, screening, interview) at companies where they know someone.
2. For each, suggest the best person and the move:
   - **A recruiter or talent partner there:** a short note that they applied, why they're a fit in one line, and a request to make sure the application gets a look.
   - **Someone on or near the team:** a referral ask, if the user knows them at least `friendly`. A referral usually beats a cold application by a wide margin.
   - **A `never-spoke` connection:** usually skip, or a light, specific note if the user wants to try.
3. Draft the messages, one at a time.

Pace it: about one referral ask a day is plenty, and better than ten in an afternoon. Asks spread out get answered.

## One next move per person

Every contact gets at most one next move: `reply`, `follow up`, `ask for an intro`, `ask for a referral`, `nudge`, `keep warm`, `thank`, or `none`. When the user asks "who should I reach out to this week?", list the moves due (by `next_date`) and the `keep warm` check-ins that are due by closeness (about every 30 days for close, 90 for friendly, 180 for loose).

## Writing the message

Give first, keep it short:

- **4 to 7 sentences.**
- **One specific reference** that shows the user knows who they're writing to: a project they shipped, a post they wrote, the last time they talked.
- **Give something** when there's something real to give: a useful link, an intro, a thought on their product.
- **One small, specific ask** that's easy to say yes to. "Would you be open to a 15-minute call next week?" or "Would you be comfortable referring me? Here's the posting and a two-line summary you can forward."
- **One proof link** at most (the user's LinkedIn, a portfolio, a project).
- **The one sentence** from the preferences page, when the ask is "keep an eye out," so they know exactly what to look for.
- Match how well they know each other: a close friend gets a text-length note; a loose connection gets context first ("We met at the product meetup in March").

**Warm intros are double opt-in.** When the user asks a mutual contact for an intro, the draft asks the mutual to check with the other person first, and offers a short forwardable blurb so it's easy.

**After any conversation:** a thank-you the same day that names something specific from it. Log it: update `last_contact`, add a dated note, set the next move.

## Before the asks: the people who've helped

Early in a search, or whenever the user feels stuck, offer this once:

1. **The gratitude list.** "Who's helped your career? Managers, mentors, people who vouched for you." For each: when, where, what they did. Add them with the tag `helped-me` and `source` `gratitude-list`. Flag the well-connected ones. It's also good for morale, and that matters in a long search.
2. **Draft thank-you notes, and hold them** until the user lands, so the thanks never arrives two weeks before a favor.
3. **Three early conversations,** before asking anyone for jobs:
   - **A former colleague:** "What did I do well? What could I have done better?"
   - **Anyone in their network:** "If you were in my shoes, how would you approach this search?" Then listen.
   - **A recruiter:** "Which jobs could I get easily, which are a stretch, and which are out of reach?"

   End each by sharing the preferences page and asking: Is this accurate? Which goal fits me best? Who else should I talk to? Record what they say on the preferences page.
4. **Listening posts.** Once the one sentence exists, the user can ask people to keep an eye out. A short monthly update to the people helping them keeps it going.

These run alongside scanning and applying, never instead of them.

## Principles

- **People first, boards second.** When a strong role turns up at a company where the user knows someone, the person is the next step.
- **Honest warmth.** Call relationships what they are; the message depends on it.
- **Small, specific asks.** Show the homework. Make yes easy.
- **The user sends everything.** Drafts only, always.
