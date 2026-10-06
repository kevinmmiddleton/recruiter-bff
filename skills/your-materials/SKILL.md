---
name: your-materials
description: >
  Improves the user's job-search materials in their own voice: resume bullets and summary,
  LinkedIn headline and About, and written application answers. Use when the user says "review
  my resume," "fix this bullet," "write my resume summary," "help with my LinkedIn headline,"
  "rewrite my About section," "answer this application question," "why do I want to work
  here," "write a cover note," "does this sound like AI," "is this too much," or "make sure my
  resume and LinkedIn match." Reads the shared profile and preferences page, never invents
  experience or numbers, and hands back drafts the user approves.
---

# Your Materials

Make the resume, LinkedIn, and written answers say what the user has actually done, in words recruiters search for and in the user's own voice. Do this after the one sentence exists if possible: know the target, then make the materials say it.

## Never

- Never invent a number, a tool, a title, or experience. Where a number is missing, leave a visible placeholder like `[from ?% to ?%]` and ask.
- Every claim needs a receipt. If you can't point to where it came from (the resume, the profile, the user), cut it.
- Never upgrade the user's nouns or scope to match a posting. "Ran experiments" doesn't become "led the experimentation strategy."
- Never claim solo what a team did, and credit the right cause for a number.
- Never answer these for the user: pay expectations, current employment, work authorization, background or legal questions, demographic surveys, or anything where the honest answer is "no" or "I don't know." Flag them and let the user answer.
- Draft, never send, never submit. The user clicks submit, every time.
- Never run the user's own work down to sound modest.

## Before you start

Read `job-search/profile.md` (background, proof points, voice) and `job-search/preferences.md` if it exists (the one sentence, must-haves). If the user is working on a specific application, read that company's folder in `job-search/interviews/<company>/` (the saved posting and evaluation).

If there's no preferences page, don't wait for one. Mention once that the summary and headline get easier once the one sentence exists, and offer it later.

## Resume bullets

Rewrite each bullet as **outcome, then how, then scope**:

> Before: "Responsible for onboarding and paywall experiments."
> After: "Raised trial-to-paid conversion from 9% to 13% over 18 months by running 40+ onboarding and paywall tests with a team of 6."

- **No "responsible for," "helped with," or "worked on"** as the main verb. Use the strongest verb the user could defend if an interviewer said "walk me through it." If they helped, say helped; "led" has to be true.
- **Both ends of the number, then the parts behind it:** "from 0.1% to 7.3%, about 50x." "As high as" reads honest; "at peak" reads cherry-picked.
- **Real results, not targets.** "Projected to save $2M" is a plan. Say what actually happened, or say it's a projection.
- **Cut bullets that only describe the job** ("managed the roadmap"). Never cut a bullet that has a number; fix it instead.
- **Translate internal jargon.** Project code names and internal team names mean nothing outside the company. Say what it was in plain words.

## Resume structure

- **The summary argues one point and has a number.** It's not a career history. It says the one sentence in searchable words and backs it with the best proof. Two or three lines.
- **A truthful "current" line** if there's a gap: what the user has actually been doing ("Searching full time and building [project]"). Never call it consulting without clients.
- **The header title is the title recruiters search for,** as long as it's honest.
- **Order by relevance.** The top third of page one gets read; put the proof for the one sentence there.
- **A few versions by job type, not one per job.** Tailor the written answers, not the whole resume. A role-specific version can wait for an interview invite.
- **Plain format:** one column, no skill bars or charts, saved as PDF.
- **Record which version went where** in the tracker's notes when the user applies.

## LinkedIn

- **Headline:** the target role plus the words recruiters search for, never "seeking opportunities." "Senior Product Manager · Growth, retention, and lifecycle · Consumer subscription."
- **About:** a short pitch with numbers, written in first person, that says the one sentence and backs it up. Not a biography.
- **Every surface matches.** Titles, dates, and claims must be identical across the resume, LinkedIn, and any personal site. Mismatches come up at reference checks. When the user asks, compare them side by side and list every difference.
- **Fix it once, then close the tab.** Endless profile tinkering feels like progress and usually isn't. Say so kindly if the user is on their fifth round of headline tweaks.

## Written answers

For "why us," "tell us about a time," cover notes, and short-answer boxes:

1. **Lead with what the user brings,** not a warm-up paragraph. The first sentence should answer the question.
2. **"Why us" formula:** something the user did that looks like the company's product or problem, plus one fact about the company that only research turns up. Then the **swap test**: if another company's name could be swapped in and the answer still works, it isn't done.
3. **Lead with the story the role is buying,** based on the posting's requirements, not on the company's industry.
4. **Honest gaps:** "Not yet. The closest I've done is ..."
5. **AI credit, if it comes up:** additive, never exclusionary. "Built with a small team, including an AI coding assistant," not "not written by AI."
6. **Keep it short.** Match the length and energy of the question.

If a "why us" draft reads hollow even after research, say so. Sometimes the draft is the filter, and the honest answer is that this role isn't a fit.

## The skeptical review pass

Before handing over any draft, read it as a skeptical hiring manager would, and fix what you find. The checklist is in `references/review-pass.md`: flattery, groveling, adjectives used as evidence, buzzwords, sentences that could go to any company, the throat-clearing opener, the slogan closer, and three examples where two would do.

Then show the draft with a short list of what changed and why, so the user learns the pattern.

## Learning the user's voice

When the user edits a draft, notice what they changed: what they cut, what they softened, words they swapped. Offer once to save the lasting ones to the profile's "Phrases I like" or voice notes, so the next draft starts closer. Their edits teach more than "how do you sound?" ever will.

## Where things go

- Approved resume bullets and the summary: offer to update the proof points in `job-search/profile.md`.
- Answers worth reusing: offer to save them in `job-search/materials/answers.md`, with the question, the answer, and a note on what to change for the next company.
- Nothing is overwritten without the user's yes.

## Principles

- **True first, then strong.** Every word has to survive "walk me through it."
- **Searchable words.** Recruiters filter on standard terms; clever labels don't show up in searches.
- **The user's voice.** Warm, specific, theirs. If they wouldn't say it out loud, rewrite it.
