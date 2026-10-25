# Run 14: the no-install kit in real ChatGPT (Oct 24, 2026)

The first run of the no-install kit in a real AI chat. Every name is fictional (Sam Okafor, the usual persona).

**Setup.** The ChatGPT desktop app for Mac, Chat mode, the default "Instant" model, Kevin's ChatGPT Plus account. A new project ("Recruiter BFF kit test") with project-only memory, so nothing from Kevin's own ChatGPT memory reached the test and nothing from it reached his memory. The kit built from main: `INSTRUCTIONS.md` pasted into the project's instructions, and the eight method files plus Sam's resume added as the project's Sources, the way the kit's README tells a user to. Same fixtures as run 13 (resume, posting, ten-role paste).

## What ChatGPT itself showed

- **Project instructions hold exactly 8,000 characters.** The settings show "N/8,000 left." The kit's build now fails if `INSTRUCTIONS.md` passes that.
- **A project's files are called Sources** in the current app (Add sources: Upload, Paste text, Google Drive, Slack).
- **Chat sometimes offers to "Continue in ChatGPT Work"** to build files. Choosing Stay in Chat finished setup the kit's way.

## Turns, first pass

| Turn | Result |
|---|---|
| "set me up" | Pass. Found the uploaded resume by name, summarized it accurately, asked two questions. |
| Setup answers | Partial. Built the profile table, then offered Work mode instead of the links; after Stay in Chat, it gave LinkedIn and company job site links, two more questions, and the "Say 'wrap up'" line. |
| Fit check (the Fernhill posting) | Fail on the score. 4.6, Apply now. It counted "SQL" in a skills list as a full match for "Strong SQL" (the scoring file's tie-breaker says partial). Company 5 was fair: the profile named healthcare as a plus. |
| Pasted job list | Pass. Kept 6 (Starting at and contract-to-hire with heads-ups, Promoted kept, both near-identical titles), hid 4 with reasons (below floor, staffing firm, confidential, ad tech). |
| Interview guide | Pass, one miss. Real date (Thu Oct 29, 2:00 PM ET), the role, fit with real numbers, honest gaps (SQL depth among them), no invented numbers, a "couldn't verify" company section, a prep checklist. Questions to ask came late, not as the fourth top block. |
| Written answer | Pass. Said it used the resume's pricing story, not a saved answer; 96 words; a skeptical review; one question; offered to save to `answers.md`. |
| wrap up | Pass, one problem. Four files, one per reply, each named, "End of file," well-formed links and CSV. Every file started with a blank line, which makes a CSV's first row empty. |

## Fixes (commit `622719d`)

- The fit check counts requirements (all matched 5, one partial 4, two partials 3.5, a real gap 3) and treats a listed skill as partial when the posting asks for strength.
- The fit check shows the five scores first, then the total and verdict.
- Guides put the four blocks first, in order.
- Wrap up starts each file on its first line.
- README: Sources, and choose Stay in Chat.

## Second pass, after the fixes

- **Fit check, first try with the counting rule:** Requirements 3.5 and a total of 4.3 in the table, but the headline above it said 4.6, Apply now, then corrected itself. **Second try** (told to work out the scores before writing): headline 4.8, table 4.4, corrected again. The default model writes the headline first and guesses it.
- **Third try, scores first:** the five scores as a table, then 4.4, Strong, apply. No correction. (4.4 here and 4.3 in Claude and Codex differ only because this profile names healthcare as a plus, which makes Company a 5 by the rules.)
- **wrap up:** the tracker copied from ChatGPT's Copy button starts on its header line. It also said, unprompted, that no earlier tracker was uploaded, so the user should keep their existing rows when saving.

## Not tested

The kit in Gemini, Copilot, or Claude Projects; the quick-start prompt in a plain chat; ChatGPT's free plan; reminders and "what's due?" across chats.

The test project and its chats are still in Kevin's ChatGPT ("Recruiter BFF kit test"), for him to look at or delete.
