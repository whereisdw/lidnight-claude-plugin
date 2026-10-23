---
description: Show your Claude Code 5-hour and weekly usage limits in two lines
allowed-tools: Bash(claude -p /usage*), Bash(ls /Applications/*), Bash(test *)
---

Summarize the user's Claude Code usage limits in exactly two lines.

1. Run `claude -p /usage --no-session-persistence --setting-sources ""` (add `timeout 60` in front if available).
2. From its output, write:
   - `5-hour: <percent used> used, resets <time>`
   - `Weekly: <percent used> used, resets <time>`
   Use only numbers that appear in the output. If a value isn't there (for example API-key sessions only print cost totals, with no subscription limits), write `5-hour: not reported` / `Weekly: not reported` and add one short line saying what the output did contain. Never estimate.
3. If the command fails or times out, say so in one line and suggest typing `/usage` inside a session. Don't retry in a loop.
4. If `/Applications/Lidnight Limits.app` exists, add one line: the menu bar item shows the same numbers (5-hour and weekly, Claude Code and Codex) without running a command. Don't suggest installing anything.

## What it runs

- `claude -p /usage --no-session-persistence --setting-sources ""`: the official `/usage` view in a one-shot, non-persisted run that loads no settings or hooks
- `test -d "/Applications/Lidnight Limits.app"`: only to decide whether to point at the menu bar item

Nothing is written, no network calls of its own, no `sudo`. The free, open-source menu bar app is [Lidnight Limits](https://github.com/whereisdw/lidnight-limits) (`brew install --cask whereisdw/tap/lidnight-limits`).
