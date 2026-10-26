# Recruiter BFF 1.1.2: Windows fixes

Fixes from a Windows test in the ChatGPT app's Codex. The tracker now stops instead of saving a file a spreadsheet app scrambled (LibreOffice with Semicolon ticked as a separator splits your notes into extra columns), and the guide says how to open it there. Setup recognizes another Windows Python error. Scheduled reminders say where to find them, and the calendar reminder reaches your phone.

**Claude desktop app (paid Claude plan):** download `recruiter-bff.plugin`, then in the Claude app open Customize, then Plugins, click + Add, choose Upload plugin, and pick the file. Updates keep everything you've saved.

**Codex in the ChatGPT desktop app:** open Plugins, click Add, then Add a marketplace, enter `kevinmmiddleton/recruiter-bff`, and install Recruiter BFF. Start a Work chat (not Chat, where the plugin doesn't load), choose a project with your job search folder, and say "set up my job search." To update, open Settings, then Plugins, then the Marketplace tab, and click Upgrade.

**Codex CLI:** run `codex plugin marketplace add kevinmmiddleton/recruiter-bff`, then `codex plugin add recruiter-bff@recruiter-bff`. To update, run `codex plugin marketplace upgrade`.

**ChatGPT or any AI chat (no install):** download `recruiter-bff-no-install-kit.zip` and follow the README inside.

It works best on a paid ChatGPT plan. It never applies for you or contacts anyone.
