# Lidnight plugin for Claude Code

Keep your MacBook awake while Claude Code works, even with the lid closed on battery, and let it sleep when the work is done.

This plugin adds three slash commands and one skill that drive the [Lidnight](https://lidnight.app/en/) menu bar app. If Lidnight isn't installed, they fall back to plain `caffeinate` / `pmset` guidance (nothing is installed or changed without asking).

## Install

```text
/plugin marketplace add whereisdw/lidnight-claude-plugin
/plugin install lidnight@lidnight
```

Lidnight itself (free, Apple Silicon, macOS 13+): `brew install whereisdw/tap/lidnight` or https://lidnight.app/en/

## Commands

| Command | What it does |
|---|---|
| `/lidnight:awake [auto\|timer N\|until\|keep]` | Start keeping the Mac awake. `auto` (default) stays awake while AI agents work and sleeps ~10 minutes after they go quiet |
| `/lidnight:status` | Is the Mac being kept awake? Runs `lidnight doctor` when something looks off |
| `/lidnight:sleep` | Stop keeping it awake now |

The `keep-awake` skill kicks in when you mention leaving a long task running, closing the lid, or "Your computer went to sleep mid-response".

## Why

When a Mac sleeps mid-response, Claude Code drops the partial reply and later rewrites the whole turn, often with no prompt cache, which burns usage limits. Closing the lid on battery is worse: macOS ignores `caffeinate`, and `pmset disablesleep` stays on until you remember to undo it. Lidnight watches Claude Code's hooks so the Mac is awake exactly while work runs.

Disclosure: I build Lidnight. The plugin is MIT licensed; Lidnight has a free tier and a one-time Pro.
