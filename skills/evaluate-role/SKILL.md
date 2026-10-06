---
name: evaluate-role
description: >
  Scores one job posting against the user's background and what they want, and gives a
  straight apply-or-skip answer. Use when the user pastes a job description or a posting link
  and asks "should I apply to this," "score this," "evaluate this role," "how good a fit is
  this," "is this worth my time," "rate this posting," or wants to compare two or three roles.
  Checks the posting is still open, maps every requirement to the user's background, reads it
  against their preferences, scores it, and saves the posting and the evaluation. Not for
  interview prep (that's interview-guide-engine). Needs the profile from job-search-setup.
---

# Evaluate Role: Score One Posting

A scan says a role exists and looks plausible. This skill answers the next question: is this one worth an application? It reads the whole posting, checks it's still live, makes two separate reads (does the user fit what they want, and does the role fit what the user wants), scores it, and says what it would do.

## Never

- Never invent or stretch evidence. If the background is adjacent, call it partial and say why.
- Never upgrade the user's nouns or scope to match the posting (a team of six is not "people management").
- Never present something you couldn't check as checked. Say "couldn't confirm" plainly.
- Never decide for the user. The verdict is advice; they can disagree, and you update.

## Step 1: Load what you know

Read `job-search/profile.md`. No profile: hand off to `job-search-setup` rather than scoring against guesses. Also read `job-search/preferences.md` if it exists.

Pull out: target titles and seniority, signals (strong, weak, parked), exclusions and their exceptions, location and work mode, pay tiers, background and proof points, and from the preferences page the one sentence, must-haves, must-nots, and company preferences.

## Step 2: Get the full posting, and check it's live

- **Pasted text:** use it as is.
- **A link:** if a browser Claude can drive is connected, open it and read the page. Otherwise try a direct fetch for company job sites (Greenhouse, Lever, and Ashby pages usually fetch cleanly). If the page comes back empty or behind a login (LinkedIn often does), ask the user to paste the text. Never get around a login.

Then:

- **Still open?** If the posting came from LinkedIn, a job aggregator, or a recruiter, look for the same role on the company's own careers page or job site. Aggregator copies often outlive the real posting. Report one of: "Live on the company's site" (with that link, and any differences in title, level, location, or pay), "Not on the company's site; it may be closed," or "Unverified: couldn't check." Never imply a role is live when you couldn't check. Don't block the evaluation on it.
- **How old is it?** Note the posting date if you can find it ("posted 3 days ago," "posted 6 weeks ago").
- **Light ghost-job flags.** Flag, never cut: reposted several times, open for more than about 60 days, vague duties with a kitchen-sink list, no pay range in a place that requires one (New York, California, Colorado, Washington, and others), or the same role listed in many cities at once. One line, no lecture: "Heads-up: posted 9 weeks ago and reposted twice. Worth a quick check before you spend an evening on it." A repost isn't always bad news: it often means the last search ended without a hire, which can be a good moment to apply.
- **Timing matters.** Applications in the first day or two get read most. If a strong role is fresh, say so: "Posted yesterday; if you're applying, sooner is better."

If all you have is a title, company, and location, say the evaluation will be shallow and offer to go ahead or wait for the full text.

## Step 3: Pull out the requirements

List 5 to 10 real requirements, split into:

- **Must-haves:** stated as required, or central to the job.
- **Nice-to-haves:** "bonus," "ideally," or clearly on the edge.

Name each plainly ("has grown conversion through experiments," not "demonstrated ownership of the end-to-end growth lifecycle").

## Step 4: Read one: do you fit what they want?

Trace every requirement to the line in the user's background that answers it:

```
| Requirement | Evidence from your background | Read |
|---|---|---|
| 3+ years in growth at a subscription company | Brightloop, Senior PM, Growth, since 2022 | ✅ match |
| Owns the journey through first renewal | Strong up to first payment; renewal isn't on your resume | 🟡 partial |
| Managed a PM (nice to have) | Nothing in your background | ❌ gap |
```

- **Cite the actual line.** A match with no evidence is a guess.
- **For each gap:** one line on the honest answer (a transferable skill, a learning curve), or "real gap, expect the question."

## Step 5: Read two: does it fit what you want?

Check the role against the preferences page and the profile, separately from the requirement match:

- The one sentence: is this the role it describes, a step toward it, or off it?
- Must-haves met, unknown, or missed. Must-nots hit or clear.
- Company size, stage, and ownership against what they said.
- The subject test: is this a subject they said they'd care about every day?
- Any parked signal it touches.

Off-target roles get flagged, never hidden. Sometimes the off-plan role is the right one, and the user decides. If there's no preferences page yet, use the profile alone and mention once that the page would sharpen this read.

## Step 6: Score it

Apply `references/scoring-rubric.md`. Score each dimension from 1 to 5, then take the weighted average:

- **Requirements match** (40%): from read one.
- **Target fit** (25%): title, seniority, and function against the targets; strong signals lift it, weak signals (soft warnings) pull it down a little, parked lanes hold it in the middle; the one sentence counts here.
- **Logistics** (15%): location, work mode, and pay against the profile.
- **Company signals** (10%): industry, size, stage, and ownership against stated preferences; the subject test.
- **Posting quality** (10%): how clear and specific the posting is; ghost-job flags count here.

Unknowns score a neutral 3, never lower. Most postings leave out pay.

## Step 7: Give the verdict

Lead with the score and the action, then the details:

```
**4.6 / 5: apply now.** Live on Fernhill's site, posted 2 days ago.

Fits what they want: [the table]
Fits what you want: the role your one sentence describes; hybrid 2 days, inside your rule;
  range $175k to $205k, above your floor.

What pushes it up: ...
What holds it back: ...
If you apply: lead with [proof point]; expect the question about [gap].
```

Tiers: **4.5 and up** apply now · **4.0 to 4.4** strong, apply · **3.5 to 3.9** decent, apply only with a specific reason (name it) · **3.0 to 3.4** weak fit, probably skip · **below 3.0** skip.

If the user disagrees with a read, update it. If the disagreement shows a preference the profile or page doesn't have, offer to add it so future scores improve.

If you know someone at the company (from `job-search/contacts.csv`, if it exists), add one line: "You know Priya Shah there. A referral beats a cold application; want a short note asking her?"

## Step 8: Save it

The first time a role is evaluated, save two files in the company folder, `job-search/interviews/<company>/` (create it; use a short lowercase name like `fernhill`):

- `posting.md`: the full posting text, the link, the date you saved it, and whether it was live on the company's site. Postings get taken down, and the guide needs the text later.
- `evaluation.md`: the verdict, both reads, the dimension scores, and the date.

If the files already exist for the same role, update `evaluation.md` and keep the original posting. For a second role at the same company, use a suffix: `posting-product-lead.md`.

Then offer to log it in the tracker through `application-tracker`: status `prospect` (or `skipped` if the verdict was skip and the user agrees), the score with one decimal, and the one-line verdict in `notes`.

Comparing several roles? Score each the same way and finish with a one-line ranking.

## Principles

- **Evidence or it didn't happen.** Every match cites a line. Honest partials and gaps make the score worth trusting.
- **Two reads, kept apart.** Being qualified and wanting the job are different questions.
- **The profile and the page are the rules.** Don't import preferences the user never stated; ask and save instead.
- **Skip is a good answer.** The point is to spend application time where it pays.
