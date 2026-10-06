---
name: interview-guide-engine
description: >
  Builds a role-specific interview guide from a job posting and the user's own background,
  then keeps it current round by round. Use when the user mentions an upcoming interview or
  screen, shares a posting to prep for, or says "help me prep," "prep me for my interview with
  [company]," "interview guide," "what should I expect," "I have a screen with [company],"
  "add a round," "who am I meeting," "how do I answer the pay question," or "help with this
  case." Also use after an interview ("debrief," "how did that go," "here's what they asked")
  and for practice ("practice my interview," "mock interview," "quiz me"). Reads the shared
  profile, preferences page, and story bank, and saves the guide in the company's folder.
---

# Interview Guide Engine

Help the user walk into every conversation knowing what the role really is, how they fit, where they'll get pushed, and what to ask. Then help them learn from each round.

Every guide opens with the same four blocks, in this order: **the role in plain words, your fit, your gaps, questions to ask.** Above them sit a one-line verdict and the next round. Everything else comes after.

## Never

- Never invent a fact about the company or a person. If you can't verify it, mark it "couldn't verify," and never repeat a claim without a source.
- Never invent or stretch the user's experience, numbers, tools, or scope. Never claim solo what a team did.
- Never decide the user's answer on pay, current employment, work authorization, or legal questions. Offer scripts in their words; they choose.
- Never send anything. Thank-you notes and follow-ups are drafts.
- Never put the user's own work down, in any answer.

## Step 0: Load what's known

1. Read `job-search/profile.md`. No profile: run `job-search-setup` first (it builds the background from the resume, so the user never answers twice).
2. If the background is thin (no proof points, no voice notes), collect only what's missing (see `references/user-profile-template.md`) and write it back into the profile. Never start a second profile.
3. Read, if they exist: `job-search/preferences.md` (must-haves and must-nots become questions), `job-search/story-bank.md` (reuse stories before drafting new ones), the company folder `job-search/interviews/<company>/` (`posting.md`, `evaluation.md`, and any existing `guide.md`), and `job-search/contacts.csv` (anyone the user knows there).
4. Get the round details: when, what kind of round, and who. If the user doesn't say, ask once: "Who are you meeting, and when?" Work out real dates from today and say them back with the weekday.

If there's no saved posting, ask for it (pasted text or a link) and save it as `posting.md` the way `evaluate-role` does.

## Step 1: Research the company and the people

Use web search. Find:

- What they sell, to whom, how they make money, size, stage, funding or revenue if public.
- Recent news, checked today: launches, leadership changes, layoffs, acquisitions. Note the date you checked.
- 4 to 6 numbers worth having in mind (not reciting), each with its source.
- The people: titles and background for each interviewer, if the user named them. Use LinkedIn in the user's own browser if it's connected, or what the user tells you. Anything they've published is worth one reaction, once.

Keep anything you couldn't confirm in a "Couldn't verify" line. Before a product or case round, tell the user to use the product as a customer and bring two or three observations, framed as observations, never gotchas.

## Step 2: The role, in plain words

Postings are wish lists. Name the three to five themes that really matter, plainly ("winning back lapsed members," not "drive retention strategy across the lifecycle"). Two to four sentences on what they're really hiring for and the problem this person solves.

## Step 3: Your fit

For each theme, the proof point that answers it: the company, what the user did, the result with both ends of the number. If the fit check already ran, start from its table.

## Step 4: Your gaps

Every real gap gets its own entry, not a footnote under fit:

- **They'll ask:** the question as an interviewer would put it.
- **Honest answer:** in the user's voice. "Not yet. The closest I've done is ..." then the adjacent proof. Short, and never apologetic.
- **Point to instead:** the proof that covers the most ground.
- **Raise it first?** Per round. Raise it yourself when it's obvious from the resume and the round is about depth (hiring manager, panel), so you frame it before they do. Let it come up naturally in a recruiter screen, and have the answer ready.

## Step 5: Questions to ask

- **Per interviewer, in the order the user meets them.** Different people deserve different questions.
- **"If you only get two":** the two that matter most for this decision.
- **Screen them back:** new seat or backfill (and how the last person did); how long the manager and their boss have been there; a real disagreement and how it was resolved; what happened after a project that didn't work.
- **From the preferences page:** every must-have and must-not that the posting doesn't answer becomes a question. If remote matters, ask how decisions get made across locations; if a bad manager was the lesson, ask how disagreements get settled.
- **The user's go-to question,** if the profile has one, as their closer.

Each question should get real information and show how the user thinks. Skip anything the posting or the company site already answers.

## Step 6: The verdict and the next round (top of the guide)

- **Verdict:** one honest line on fit, plus **the one big risk** most likely to sink it.
- **Next round:** date, time, time zone, type, who. Then **what this round tests and what it doesn't:**
  - **Recruiter screen:** motivation, logistics, pay range, the basic story. Not deep craft.
  - **Hiring manager:** judgment, depth, the stories behind the resume, whether they'd want to work with the user.
  - **Panel:** each person is screening for something different (see the people section).
  - **Case or exercise:** how the user thinks with incomplete information, more than the answer.
  - **Executive or final:** business thinking in their terms, and whether the user can be trusted with the scope.

If this round is a stretch the user is taking for practice (the pay is under their floor, or the role is off their one sentence), say so plainly at the top, so they go in knowing which kind of conversation it is.

## Step 7: Everything else

Build the rest of the guide from `references/guide-template.md`:

- **The people:** for each interviewer, what they're screening for, two or three points to land, likely probes, two questions. For panels, a reminder to confirm who's who in the first minute.
- **The company:** snapshot, numbers with sources, recent news with the date checked, product homework.
- **Tell me about yourself:** three or four sentences: the pattern of the career, two proof points tied to their themes, why this is the natural next step. In the user's voice, not a resume read aloud.
- **Likely questions and answers:** five to seven for this round, each under 150 words, in the user's voice, with real proof points. Pull behavioral answers from the story bank first. For a two-part "and" question, answer the second half first, since that's the part people forget. No "great question," no "happy to walk through examples."
- **Awkward questions, scripted:** only the ones that apply to this user. See `references/answers-and-scripts.md`.
- **Case or exercise:** the method in `references/answers-and-scripts.md`, applied to what the user knows about the prompt.
- **Pay and timeline:** the script for this situation from `references/answers-and-scripts.md`, using the user's own pay line from the profile; and what they'll say about timing and other processes.
- **Watch-fors:** things to probe, not dealbreakers ("fast-paced" might mean understaffed: ask about team size).
- **Prep checklist:** short and specific.

## Step 8: Save and hand off

Save to `job-search/interviews/<company>/guide.md`. Share the top of the guide in the chat (verdict, next round, four blocks), and say the rest is in the file.

Then offer: update the tracker (status and `next_date`) through `application-tracker`, and a practice run.

## After the round: debrief

When the user comes back from an interview, debrief right away, while it's fresh. Ask a few at a time:

1. What did they ask? Anything you didn't expect?
2. What landed? What fell flat?
3. What changed: anything new about the role, the team, the process, the timeline?
4. How did they treat you? Did they listen? Say "we" or "I"? Rush you? Did you feel like a priority or a nuisance? Do they understand their own business? Anything off you can't name yet?
5. What's next, and when?

Write it into the guide's Round notes (never overwrite earlier rounds). Then:

- Update the rest of the guide with what was learned (a watch-for answered, a new gap, the next round's people).
- Update the story bank: mark stories used, note how they landed, and offer to bank any new story the user told.
- Update the tracker's status and `next_date` through `application-tracker`.
- Offer thank-you notes (drafted by `application-tracker`), same day.

How they treat the user is information about the job. An interview is the best behavior anyone will ever show, so take an early bad sign seriously and say so kindly.

## Practice

When the user says "practice my interview" or "mock interview":

1. Play the interviewer for the next round, in that person's voice and with their priorities (a recruiter asks different things than a hiring manager).
2. One question at a time. Wait for the full answer.
3. After each answer: what landed, what was weak, and a tighter version in the user's words.
4. After four to six questions: the pattern across answers (running long, burying the result, skipping the "why").
5. For stories, ask them to say it out loud and time it: about 90 seconds. Cut the setup, never the result.

Keep the critique specific and kind. Practice is for finding the weak spots before the interviewer does.

## The story bank

Prep compounds when stories are kept. The bank lives at `job-search/story-bank.md` (format in `references/story-bank-template.md`): 5 to 10 stories in STAR+R form (situation, task, action, result, reflection).

- **Reuse** a matching story before drafting a new one; adapt the emphasis to this role, never the facts.
- **Check for gaps** before each round: if the round will ask about a failure or a disagreement and the bank has none, say so and help draft one from the user's real experience.
- **Deposit:** after a guide or a debrief, offer once to save any new story.
- **Maintain:** when the user corrects a story, fix the bank, not just the guide. Around ten stories, suggest which one a new story replaces.

## Principles

- **Honest about fit.** A guide that says "you're perfect" is useless. Show strengths and where they'll get pushed.
- **Sound like the user.** Their tone, their words, nothing they'd never say out loud.
- **Respect their time.** The top of the guide works in five minutes; the rest is for the night before.
- **Questions matter as much as answers.** Good questions show how someone thinks, and get the user what they need to decide.
