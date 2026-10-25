# Recruiter BFF 1.1.1: your search stays put in the ChatGPT app

In the ChatGPT desktop app, a Work chat with no project works in a folder the app makes for that one chat, and the next chat gets a new one. A search started there was out of reach a chat later. Recruiter BFF now asks you to start a Work chat with a project on your job search folder first, and saves nothing until you do.

**Claude desktop app (paid Claude plan):** download `recruiter-bff.plugin`, then in the Claude app open Customize, then Plugins, click + Add, choose Upload plugin, and pick the file. Updates keep everything you've saved.

**Codex in the ChatGPT desktop app:** open Plugins, click Add, then Add a marketplace, enter `kevinmmiddleton/recruiter-bff`, and install Recruiter BFF. Start a Work chat (not Chat, where the plugin doesn't load), choose a project with your job search folder, and say "set up my job search." To update, open Settings, then Plugins, then the Marketplace tab, and click Upgrade.

**Codex CLI:** run `codex plugin marketplace add kevinmmiddleton/recruiter-bff`, then `codex plugin add recruiter-bff@recruiter-bff`. To update, run `codex plugin marketplace upgrade`.

**ChatGPT or any AI chat (no install):** download `recruiter-bff-no-install-kit.zip` and follow the README inside.

It works best on a paid ChatGPT plan. It never applies for you or contacts anyone.
