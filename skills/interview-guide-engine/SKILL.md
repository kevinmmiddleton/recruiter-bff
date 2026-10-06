---
name: interview-guide-engine
description: >
  Generate comprehensive, role-specific interview guides from a job description.
  This skill should be used when the user shares a JD, mentions an upcoming interview,
  says "help me prep," "interview guide," "what should I expect," "recruiter call for
  [role]," "I have a screen with [company]," or pastes a job posting. Also use when
  the user asks to "add a round" to an existing guide. Reads the shared job-search
  profile for the user's background; if background details are missing, captures them
  once and saves them back to the profile so all future guides are personalized.
---

# Interview Guide Engine

Generate interview guides that help the user walk into any conversation with a clear story, scripted answers, and smart questions ready to go.

## Profile: read the shared profile first

This skill shares one profile with the rest of the Recruiter BFF plugin: `job-search/profile.md` in the user's Cowork folder.

1. Read `job-search/profile.md`.
2. If it doesn't exist, run `job-search-setup` first (it captures the same background fields, so the user never answers twice).
3. If it exists but the **Background** section is thin or marked `(not set yet)` — missing proof points, voice, or the upfront-about field — collect just those pieces now (see the short flow below) and write them back into the profile's Background and Voice sections. Don't create a separate profile file.
4. Also read `job-search/story-bank.md` if it exists — the user's accumulated interview stories. Reuse them before drafting anything new (see The Story Bank below).

### Collecting missing background (only what's absent)

Ask conversationally, only for what's missing:
- Current title, years of experience, two-sentence career arc, why looking.
- 4–6 strongest accomplishments (company, what they did, measurable result).
- Lead-with guidance by role type (e.g., "for AI roles lead with X").
- How they sound in interviews (formal/casual, dry/warm, concise/expansive); a go-to question they like to ask.
- Anything to be transparent about (gap, title mismatch, pivot).

Save into `job-search/profile.md` using the field layout in `references/user-profile-template.md`. Confirm: "Got it — saved to your profile. Building your guide now."

---

## Generating a Guide

### Input

The user provides a job description (pasted, uploaded, or URL). They may also provide interview round details, specific concerns, or research they've already done.

### Step 1: Company Research

Research the company before writing anything. Use web search to find:
- Recent funding, revenue, growth metrics
- Product suite and key features
- Recent news (acquisitions, launches, leadership changes)
- Competitive landscape
- Culture signals (job postings, press, Glassdoor themes)

Compile into a **Company Snapshot**. Only include what's useful for interview prep. No padding.

### Step 2: Role Analysis

Extract what the role is *really* asking for. Job descriptions are wishlists. Identify the 3-5 themes that matter most.

Name each theme plainly, not in JD jargon:
- "Hardware-software integration" not "cross-functional technical collaboration"
- "Post-acquisition integration" not "M&A product strategy alignment"
- "Multi-persona product ownership" not "stakeholder management across diverse user segments"

For each theme, write a short paragraph on why it matters for this specific company and role.

### Step 3: Fit Mapping

For each theme, find the proof points from the user's profile that map to it. Cite the company, what they did, and the result.

Be honest about gaps. If the user lacks direct experience with something the role asks for, say so and frame it constructively: what transferable skills apply, what's the learning curve. The user needs to know where they'll get pushed so they can prepare, not be blindsided.

### Step 4: Fit Story

Write a 3-4 sentence tailored "tell me about yourself" that:
- Opens with the user's career pattern, not their most recent job
- Connects 2-3 proof points to the role's key themes
- Ends with why this role is a natural next step
- Sounds like the user, not a resume read aloud

### Step 5: Likely Questions + Answers

Generate 5-7 questions tailored to the interview round:

**Recruiter screen:** Why this company, why this role, tell me about yourself, why looking, salary, logistics.
**HM screen:** Behavioral "tell me about a time" stories, product thinking, role-specific challenges.
**Panel/final:** Case questions, pushback on gaps, first 90 days, team dynamics.

For each answer:
- Write in the user's voice (read their profile for tone)
- Under 150 words. Interviewers tune out after that.
- Include specific proof points with company names and results
- For gap questions: acknowledge honestly, bridge to transferable experience
- For behavioral questions: pull from the story bank first. A banked story the user has already approved (and maybe told before) beats a fresh draft — adapt its emphasis to this role's themes rather than inventing a new one.

### Step 6: Questions to Ask

Generate 6-8 questions organized by category:
- About the product (2-3)
- About the role (2-3)
- About execution/culture (1-2)

Each question should do double duty: get useful information AND signal something positive about the user. Include a brief note on strategic value.

If the user has a go-to question in their profile, include it as their closer.

### Step 7: Watch-Fors

Flag 3-5 things to probe during the interview:
- Comp below range — what makes up the gap
- Massive scope — what's actually prioritized for Q1
- Title mismatch — growth path
- "Fast-paced" code for understaffed — team size
- Remote but "office culture" — what hybrid means

These are things to investigate, not dealbreakers.

### Step 8: Prep Checklist

- [ ] Review company product (include URL if found)
- [ ] Prepare specific stories for each theme
- [ ] Research interviewer on LinkedIn (if name known)
- [ ] Interview date/time (if known)

---

## Output Format

Save as `guide.md` inside `job-search/interviews/<company>/` in the user's Cowork folder. (This keeps interview prep alongside the rest of their job-search data.)

```
# [Company] Interview Guide
## [Role Title]

---

## Company Snapshot

## Role Analysis: What They're Really Asking For

## Why [User] Fits

## Round [N]: [Round Type]

### Fit Story

### Likely Questions + Answers

### Questions to Ask

### Watch-Fors

## Prep Checklist
```

After saving, share the guide and offer to update the tracker: if this company isn't yet at an interview status, suggest moving it (hand off to `application-tracker`).

---

## Updating Guides

When the user completes a round and returns with new info (who they met, what was discussed, next round), add a new round section. Don't overwrite previous rounds.

Update the prep checklist and watch-fors based on what was learned (e.g., "they confirmed fully remote" resolves a watch-for).

---

## The Story Bank

Interview prep compounds when stories are kept, not regenerated. The bank lives at `job-search/story-bank.md` (format in `references/story-bank-template.md`): 5–10 master stories in STAR+R form — Situation, Task, Action, Result, plus **Reflection**, the what-I-learned line that separates a senior answer from a recitation.

**Reuse:** when generating behavioral answers, check the bank for a story whose themes match before drafting new. Adapt the telling to this role (which details to stress), not the facts.

**Deposit:** after a guide is done, if any behavioral answer introduced a story that isn't banked yet, offer once: "Want me to save the [topic] story to your story bank so future guides reuse it?" On yes, write it in STAR+R form with its theme tags. Same after a round debrief — a story the user actually told (and how it landed) is the most valuable deposit there is.

**Maintain:** if the user corrects a story's facts or framing, update the bank, not just the guide. Cap the bank around ten stories; when an eleventh arrives, suggest which existing one it replaces or merges with.

---

## Principles

**Be honest about fit.** A guide that says "you're perfect for everything" is useless. Show strengths and where they'll get pushed.

**Sound like the user.** Read their profile. Match their tone. No corporate-speak they'd never say out loud.

**Respect their time.** The guide should be skimmable in 15 minutes the morning of. Front-load the important stuff.

**Research matters.** A guide without company research is just a template. Knowing the company raised a Series C or acquired a competitor changes positioning.

**Questions > answers.** The questions the user asks often matter more than their answers. Make them genuinely good — questions that show the user thinks like someone who'd be excellent in the role.
