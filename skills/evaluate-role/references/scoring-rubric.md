# Scoring Rubric

How to score one posting against the user's profile and preferences. Five dimensions, each 1 to 5; the overall score is the weighted average. The profile and the preferences page are the rules; this file is the method.

> The dimensional approach is adapted from [career-ops](https://github.com/santifer/career-ops) by santifer (MIT), reworked for this plugin's profile and on-demand flow.

## Dimensions and weights

| Dimension | Weight | What it measures |
|---|---|---|
| Requirements match | 40% | How much of the posting the user's background actually answers |
| Target fit | 25% | Whether this is the kind of role they're after |
| Logistics | 15% | Location, work mode, and pay against their rules |
| Company signals | 10% | Industry, size, stage, ownership, and subject against their preferences |
| Posting quality | 10% | Whether the posting itself is a good sign |

## Anchors

Score whole or half points. The anchors are the calibration; land between them when it fits.

### Requirements match (40%)

From read one, every requirement traced to a line in the background.

- **5:** every must-have is a cited match; gaps only in nice-to-haves
- **4:** must-haves nearly all matched; one partial with a believable answer
- **3:** most must-haves matched or partial; one real gap
- **2:** several must-have gaps; applying would lean on stretch framing
- **1:** the posting describes a different person

### Target fit (25%)

- **5:** target title and seniority, hits a strong signal, and matches the one sentence (if there is one)
- **4:** target title and seniority, no strong signal; or a weak signal plus a close match to the one sentence
- **3:** an adjacent title or unclear seniority, plausibly in range
- **2:** outside the targets but arguably transferable; or it mainly hits a parked signal
- **1:** wrong function or clearly the wrong level

### Logistics (15%)

- **5:** location and work mode inside the rules; listed pay at or above comfortable
- **4:** inside the rules; pay unlisted, or listed between floor and comfortable
- **3:** workable with a compromise the user said they'd consider
- **2:** conflicts with a stated rule (hybrid in a city they ruled out)
- **1:** breaks a hard rule (on-site only where they won't work; listed range entirely below the floor)

### Company signals (10%)

- **5:** a subject they'd care about every day, and the size, stage, and ownership they want
- **4:** neutral to positive; nothing they've ruled out
- **3:** no information either way
- **2:** near something they've ruled out, or a size or ownership type they said they dislike
- **1:** an excluded industry or company type (this usually stops at the gate; score it only if the user asked anyway)

### Posting quality (10%)

A clear, specific posting signals a team that knows what it's hiring for.

- **5:** specific duties, a named team and scope, a clear level, pay listed
- **4:** clear and specific, pay unlisted
- **3:** standard boilerplate; nothing alarming
- **2:** vague duties, a kitchen-sink list, "wear many hats" signs of understaffing, or one ghost-job flag
- **1:** barely a posting: generic paragraphs, contradictory level signals, or several ghost-job flags

## Rules

- **Unknowns score 3.** Missing pay, unstated work mode, no stage information: neutral, never a penalty.
- **The gate comes first.** If the role fails a hard rule from the find-jobs classification rubric (skip-list company, a place they won't work, an excluded function with no exception that applies), say so. It needs a skip, not a score. Score it anyway only if the user asks.
- **Exceptions win.** If an exclusion has an exception and the role fits the exception, it passes the gate ("data science PM out, growth analytics in": a growth analytics PM role passes).
- **Round to one decimal,** for the verdict and for the tracker.
- **Show the dimension scores.** The overall number earns trust by being something you can take apart.

## Tiers

| Overall | Verdict |
|---|---|
| 4.5 to 5.0 | Apply now |
| 4.0 to 4.4 | Strong, apply |
| 3.5 to 3.9 | Decent: apply only with a specific reason (name it) |
| 3.0 to 3.4 | Weak fit, probably skip |
| Below 3.0 | Skip |

## Calibration

- Early evaluations are only as good as the profile. If scores keep feeling off, the fix is usually a missing preference. Capture it in the profile or the preferences page rather than nudging scores by hand.
- Resist grade inflation. If everything scores 4 or more, the rubric has stopped doing its job: re-anchor on the 3s.
