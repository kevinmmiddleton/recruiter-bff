# Resume rule scenarios: results, 2026-10-14

Two simulated runs of `evals/scenarios/resume-rule.md` (an agent playing Claude in Cowork with the plugin). Run 1 passed 23 of 23 on the first draft and flagged five wording risks, which were fixed. Run 2, below, passed 23 of 23 on the fixed text and flagged five clarity spots and two ways a user could still drift toward a resume per posting (saying yes to every "replace your primary?", and an alternate shaped to one posting). Those seven were fixed in the same commit, after run 2: the replace question now says "only if it's the version you'd send everywhere," new claims in a replacement are confirmed before use, and an alternate is built for a kind of role from the user's background.

Snapshot check: `python3 tools/check_snippets.py` passed all 94 checks on the final text.

---

# Resume rule simulation: results (Recruiter BFF 1.0, run 2026-10-14)

All six scenarios were run as Claude in Cowork with the plugin's skills, each in its own folder under `runs/<letter>/folder/`. (c), (d), and (f) started from a copy of (a)'s finished folder. Transcripts are in `runs/<letter>/transcript.md`.

Where each run stopped: (a) and (b) ran through setup Step 4 (profile saved, first scan offered). (c) and (d) stopped after one reply. (e) stopped after the honest read (Step 1). (f) went through the full fit check and saved files.

**Result: 23 of 23 expectations PASS. No FAILs and no near-misses on the expectations.** There are five soft spots in the skill text, listed below. None of them caused a failure here, but each one needed a judgment call.

## Expectations

| # | Expectation | Result | Evidence |
|---|---|---|---|
| a1 | Asks for one primary resume, and asks once about a second kind of role or industry | PASS | T1: "Bring your one primary resume: paste it, or tell me which file in your folder it is." T2: "Are you also aiming at a second kind of role or a different industry…" (asked once) |
| a2 | Doesn't ask for an alternate after the no | PASS | Turns 3 to 6 never mention an alternate (`runs/a/transcript.md`) |
| a3 | Saves `primary.md` and the original file unchanged; no `alternate.md` | PASS | `runs/a/folder/job-search/resume/` has `primary.md` and `sam-okafor-resume.txt` (byte-identical to the fixture). No `alternate.md` |
| a4 | The profile's Resume line names the primary and says there's no alternate | PASS | `runs/a/folder/job-search/search-profile.md`: "_Resume: primary, job-search/resume/primary.md, copied from sam-okafor-resume.txt on 2026-10-14, for all roles … Alternate: no alternate._" |
| a5 | Says in one line that every fit score runs off this resume, so scores stay consistent | PASS | T3: "Every fit score runs off it, so the scores stay consistent: a 4.6 means the same thing every time." |
| a6 | Gives an honest read of the resume | PASS | T3: "two of your three Brightloop bullets have no results… this resume undersells your current job a bit" |
| b1 | Asks for the alternate after Sam says yes to a second kind of role | PASS | T3: "Bring that resume the same way: paste it, or tell me which file in your folder it is. And is it just for program manager roles…" |
| b2 | Saves `primary.md` and `alternate.md` in `job-search/resume/` | PASS | `runs/b/folder/job-search/resume/` has `primary.md`, `alternate.md`, and both originals unchanged |
| b3 | The profile's Resume line says which roles each covers | PASS | `runs/b/folder/job-search/search-profile.md`: primary "for Senior PM roles in growth, retention, and lifecycle, and everything the alternate doesn't cover"; alternate "for program manager roles" |
| b4 | Never offers or mentions a third resume, or one per posting | PASS | Searched `runs/b/transcript.md` for "third", "per posting", "each job", and "tailor": none in any reply |
| c1 | Declines in one friendly line: one strong resume sent where it fits beats a custom one per job | PASS | "I don't make a new resume for each job: one strong resume, sent where it already fits, beats a custom one per posting." |
| c2 | Offers the fit check for Fernhill instead | PASS | "Want me to check how your primary resume stacks up against this one?" (the pasted Fernhill posting) |
| c3 | Writes no resume, outputs no rewritten resume, creates no new resume file | PASS | The reply is two sentences. `diff -r runs/a/folder runs/c/folder` is empty |
| d1 | Rewrites it outcome, then how, then scope, in Sam's words | PASS | "[Raised] [annual-plan metric] from [?] to [?] by running [?] pricing and packaging tests for the annual plan, [over ? months, for ? subscribers]." |
| d2 | Invents no number; leaves a visible placeholder for the missing result | PASS | Every number is a bracket. The 40+ tests and the team of 6 weren't borrowed from other bullets |
| d3 | Treats it as a change to the primary resume (a draft Sam applies) | PASS | "This is a draft for your primary resume. Once the brackets are filled in, update your real resume, then share the new file and I'll save it next to the old one" |
| e1 | Says plainly that the resume needs work | PASS | "This resume needs work, and it undersells you" |
| e2 | Names the weakest spots | PASS | "none of your five bullets has a result, and there isn't a number anywhere… 'Responsible for growth,' 'Managed the roadmap,' and 'Partnered with engineering and design' are true of almost any PM" |
| e3 | Offers to help strengthen the resume they have | PASS | "Once setup is done, I can help you strengthen it bullet by bullet." No mention of per-job resumes |
| f1 | Doesn't score against the pasted version | PASS | T1 asks first and gives no score. In T2, every requirement row cites `primary.md` lines, and the pricing row cites "Responsible for pricing and packaging tests for the annual plan" |
| f2 | Asks whether it should replace the primary | PASS | T1: "should this replace your primary resume? I check every posting against the same resume, so the scores stay comparable." |
| f3 | If it scores now, it scores against the saved primary and says so | PASS | T2: "Checked against your primary resume." `fit-check.md` says "checked against your primary resume (2026-10-14)" |
| f4 | Invents nothing from the paste; if it scores, says which pasted lines weren't counted | PASS | T2: "I didn't count this line from the version you pasted…: 'Led pricing and packaging, raising annual plan revenue 40%.'" The 40% appears only in that quote. It isn't in either saved file, and `primary.md` is unchanged |

## FAILs and near-misses

No expectation failed or nearly failed. These spots in the skill text needed a judgment call, and a more literal run could slip on them:

1. **The saved-resume sentence doesn't work with two resumes.** `job-search-setup/SKILL.md` line 51. The quoted sentence is singular ("Every fit score runs off it"). For an alternate, the skill only says to swap in "your resumes" and add "(your alternate for [its roles])". Read literally, that gives broken grammar ("your resumes… runs off it") and leaves open where the parenthetical goes. In (b) I changed "it" to "them" and placed the parenthetical myself. **Fix:** write out the two-resume version: "I saved your resumes in your job-search folder (your alternate for [its roles]). Every fit score runs off the one that matches the role, so the scores stay consistent: a 4.6 means the same thing every time."
2. **"Resume help" gets logged in a profile that doesn't exist yet.** `job-search-setup/SKILL.md` line 53. It says to add "Resume help: YYYY-MM-DD" to the profile's Offered section during Step 1, but the profile isn't written until Step 4 (line 95). If setup stops partway, as (e) did, the offer is never recorded, and a later skill could offer it again. **Fix:** "…and note it; when you write the profile in Step 4, list it under Offered."
3. **Unclear whether to wait for the replace answer.** `evaluate-role/SKILL.md` line 34. "If not, or they don't say, score against the saved one" doesn't say whether to ask and wait, or ask and score in the same reply. (f) asked and waited, which cost a turn. Either reading passes the expectation, but two runs could behave differently. **Fix:** "Ask, and wait for the answer. If the next message doesn't answer it, score against the saved one."
4. **Unclear when to save the primary.** `job-search-setup/SKILL.md` lines 44 to 51 don't say whether to save the primary before or after the alternate question. Line 51's wording changes when there's an alternate, so I saved after the answer. Low risk. **Fix:** "Save once you know whether there's an alternate."
5. **Unclear which review format a bullet gets.** `your-materials/SKILL.md` lines 105 to 107: does a resume bullet get the full FLAGS / VERDICT / REWRITE block, or the short form for "a single line, like a headline"? I used the short form in (d). Low risk. **Fix:** name resume bullets in the short-form sentence, or say they get the full block.

## Anything that still offers or implies a resume per posting

No skill offers a resume per posting. Every mention says the same thing: two resumes at most, and the resume stays as it is. See `job-search-setup/SKILL.md` 44, 62, 127; `profile-template.md` 84, 128; `your-materials/SKILL.md` 9 to 12, 30, 66, 71 to 73; `evaluate-role/SKILL.md` 23, 32, 34, 152; `interview-guide-engine/SKILL.md` 33; `application-tracker/SKILL.md` 52; `tracker-schema.md` 20; `README.md` 57, 72, 103.

Two spots could still lead to one in practice:

1. **A resume per posting, one replacement at a time.** `evaluate-role/SKILL.md` line 34, together with `job-search-setup/SKILL.md` line 127. When the user pastes "this version" for a posting, the skill asks whether it should replace the primary. On a yes, it swaps it in with no further check. A user who says yes every time ends up with a primary rewritten for each posting, and scores stop being comparable, which is the thing the rule protects. In (f), the paste also added an unsourced claim (the 40%), and a yes would have made it citable evidence from then on. **Fix:** add one line to the question: "Only if it's the version you'd send everywhere, not just to [Company]." When a replacement adds a claim the old resume didn't have (a new number), confirm it before it's used as evidence.
2. **An alternate built from one posting.** `your-materials/SKILL.md` line 73: "with only a primary, offer to help build an alternate." This is triggered by a single tailoring request for an off-lane posting. It stays within two resumes, but the alternate could end up shaped to that one posting's wording. **Fix:** "build it for that kind of role, from the user's background, not from this posting's requirements."
