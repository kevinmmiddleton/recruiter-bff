# Recruiter BFF: the no-install kit

For ChatGPT, Microsoft Copilot, Gemini, or the Claude app without a paid plan. Nothing to install: you paste in some instructions, and your AI chat becomes a recruiter in your corner. It tells you honestly whether a role fits and preps you for every interview. It never applies for you or contacts anyone.

The trade-off: a chat can't save files, search job sites, or remind you. So it hands you files to keep, you paste in job lists, and you add reminders to your own calendar.

## Pick the one that matches your AI app

**1. You can make a project** (ChatGPT Projects, Claude Projects, a Gemini Gem, or anything that saves instructions and files)

1. Unzip this kit. Move the `job-search` folder somewhere you keep your files, like Documents. That's your search's home.
2. Make a new project (in ChatGPT, choose Project-only memory, so your search stays in the project). Paste everything in `INSTRUCTIONS.md` into the project's instructions.
3. Upload to the project: the eight files in `Project files`, and your resume. (In ChatGPT, a project's files are called Sources: open the project, choose Sources, then Add sources.)
4. Start a chat in the project and say "set me up." If ChatGPT offers to continue in Work, choose Stay in Chat.
5. Paste a job posting anytime and ask "should I apply?" Before an interview, say "prep me for [company]."
6. Before you close the chat, say **"wrap up."** It hands you each file that changed. Save each one in your `job-search` folder (see below), replacing the old copy. Then in the project, delete the old copy and upload the new one, so there's only ever one version. **If you don't say "wrap up," nothing from that chat is saved.**

**2. You can only chat**

1. Start a chat and paste everything in `QUICK-START-PROMPT.md` as your first message.
2. Paste your resume, then a job posting, and ask "should I apply?"
3. Before you close the chat, say "wrap up" and save the files it hands you in your `job-search` folder. Next time, paste your `search-profile.md` in after the quick-start prompt, so it remembers your search.

**3. You'd rather keep it simple**

Use the `job-search` folder on its own. `job-tracker.csv` opens in Excel, Numbers, or Google Sheets: one row per role, so you always know what you applied to, what's due, and who to follow up with.

## How to save what it hands you

Each file comes in a gray box with its name above it, like `job-search/search-profile.md`.

1. Click the box's **Copy** button.
2. Open a plain text editor: **Notepad** on Windows, or **TextEdit** on a Mac (then choose Format, then Make Plain Text).
3. Paste, and save it in your `job-search` folder with exactly the name shown, like `search-profile.md` or `job-tracker.csv`. If the editor adds `.txt` to the end, remove it.

Files ending in `.md` are plain text; any text editor opens them. `job-tracker.csv` opens in your spreadsheet app. Interview guides are named for the company, like `fernhill-interview-guide.md`, so they all live side by side.

## What's in the kit

| File | What it's for |
|---|---|
| `INSTRUCTIONS.md` | Paste into a project's instructions (option 1) |
| `QUICK-START-PROMPT.md` | Paste as your first message (option 2) |
| `Project files/` | Eight files for a project to follow: how roles are scored, how job lists are sorted, the interview guide template, answer scripts, the story bank template, the review checklist, and how search links are built |
| `job-search/` | Your search's home, with a blank tracker to start from |

## Finding roles

"Set me up" gives you search links: a LinkedIn search and a few Google searches of company job sites, filtered to the past week. Open them, copy the results, paste them in, and ask "which of these fit?"

## Reminders

Ask "remind me on Mondays and Thursdays," and you'll get a calendar event to add yourself. When it pops up, open your project and ask "what's due?" It reads the latest tracker you uploaded.

## Ground rules

- Your resume and search stay with you and the AI app you chose. Use an account you trust with them.
- It drafts. You send and you submit, every time.
- Want it to search for you and keep your files itself? The full Recruiter BFF runs in the Claude desktop app (paid plan) and in Codex: github.com/kevinmmiddleton/recruiter-bff
