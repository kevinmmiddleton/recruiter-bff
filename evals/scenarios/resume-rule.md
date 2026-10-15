# Scenarios: one primary resume, never one per posting (1.0)

Kevin's rule (Oct 14, 2026): Recruiter BFF never writes a custom or tailored resume for a job posting. People keep one primary resume, plus at most one alternate for a second kind of role or a different industry. Every fit score runs off those, so scores stay consistent.

Run each scenario in a fresh Cowork-style folder with the plugin's skills, as a simulation (an agent playing Claude with the plugin installed). Today is Wednesday, October 14, 2026. The persona is Sam Okafor (they/them), Brooklyn, from `case.md` in the Oct 6 simulation; the fixtures are below. Pass means every expectation holds.

## Fixtures

**Primary resume** (`sam-okafor-resume.txt`):

```
Sam Okafor
Brooklyn, NY · Senior Product Manager

Brightloop (consumer meditation app, 300 people), Senior PM, Growth, 2022 to present
- Led onboarding and paywall experiments; trial-to-paid conversion rose from 9% to 13% over 18 months across 40+ A/B tests.
- Own the lifecycle email and push program with a team of 6 (design, engineering, data science, lifecycle marketing).
- Responsible for pricing and packaging tests for the annual plan.

Pennant (personal finance app, Series C), Product Manager, 2019 to 2022
- Launched bill pay to 400k users.
- Cut support tickets for failed payments by 35% with a retry flow.

Maplestone Consulting, Consultant, 2016 to 2019
- Digital strategy for retail banks.

Skills: experimentation, SQL, Amplitude, Braze, pricing and packaging.
```

**Alternate resume** (`sam-okafor-program-resume.txt`), for program manager roles:

```
Sam Okafor
Brooklyn, NY · Program Manager

Brightloop, Senior PM, Growth, 2022 to present
- Ran the cross-team launch calendar for 14 experiments a quarter across design, engineering, data science, and marketing.
- Set up the weekly growth review and its decision log, used by three teams.

Pennant, Product Manager, 2019 to 2022
- Coordinated the bill-pay launch across engineering, compliance, and support for 400k users.

Maplestone Consulting, Consultant, 2016 to 2019
- Program plans and status reporting for retail bank digital projects.
```

**Weak resume** (`weak-resume.txt`):

```
Sam Okafor
Product Manager

Brightloop, Senior PM, 2022 to present
- Responsible for growth.
- Worked on onboarding.
- Managed the roadmap.

Pennant, Product Manager, 2019 to 2022
- Helped with bill pay.
- Partnered with engineering and design.
```

**Posting:** the Fernhill Senior PM, Growth posting from `case.md` turn 3.

## Scenarios and expectations

**(a) Setup with one target role.** "Set up my job search." Sam is aiming only at Senior PM roles in growth, retention, or lifecycle; points to `sam-okafor-resume.txt`; says no to a second kind of role.
- Asks for one primary resume, and asks once whether there's a second kind of role or industry.
- Doesn't ask for an alternate after the no.
- Saves `job-search/resume/primary.md` (and the original file, unchanged); no `alternate.md`.
- The profile's Resume line names the primary and says there's no alternate.
- Says in one line that every fit score runs off this resume, so scores stay consistent.
- Gives an honest read of the resume.

**(b) Setup with two kinds of roles.** Same, but Sam is also applying for program manager roles and has `sam-okafor-program-resume.txt`.
- Asks for the alternate after Sam says yes to a second kind of role.
- Saves `primary.md` and `alternate.md` in `job-search/resume/`.
- The profile's Resume line says which roles each covers.
- Never offers or mentions a third resume, or one per posting.

**(c) "Tailor my resume for this posting."** Starting from scenario (a)'s folder, Sam pastes the Fernhill posting and says "Tailor my resume for this posting."
- Declines and says why: by the time a custom resume is done, the early applicants are in, and one strong resume, sent early, to roles where Sam is a strong fit, wins more often.
- Records that it gave the why (the profile's Offered section), so a second ask gets a short decline and the fit check, not the speech again.
- Offers the fit check for Fernhill instead.
- Writes no resume, outputs no rewritten resume, and creates no new resume file.

**(d) "Fix this bullet" on the primary.** From (a)'s folder: "Fix this bullet: Responsible for pricing and packaging tests for the annual plan."
- Rewrites it outcome, then how, then scope, in Sam's words.
- Invents no number; leaves a visible placeholder for the missing result.
- Treats it as a change to the primary resume (a draft Sam applies to their real resume).

**(e) A weak resume at setup.** "Set up my job search," pointing to `weak-resume.txt`.
- Says plainly that the resume needs work.
- Names the weakest spots (for example: no results anywhere, bullets that only describe the job).
- Offers to help strengthen the resume they have (graded on the framing; it doesn't need to mention per-job resumes).

**(f) A different resume pasted during a fit check.** From (a)'s folder: "Should I apply to Fernhill? Use this version of my resume:" with a copy of the primary where the pricing bullet reads "Led pricing and packaging, raising annual plan revenue 40%."
- Doesn't score against the pasted version.
- Asks whether it should replace the primary (so every posting is checked against the same resume).
- If it scores now, it scores against the saved primary and says so.
- Invents nothing from the paste (the 40% isn't in the saved resume), and if it scores, says which pasted lines weren't counted.

## Results

Each run's transcript and a pass/fail table go in `evals/results/` (`resume-rule-YYYY-MM-DD.md`).
