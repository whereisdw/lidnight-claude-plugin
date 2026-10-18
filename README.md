# Lidnight plugin for Claude Code

Keep your MacBook awake while Claude Code works, even with the lid closed on battery, and let it sleep when the work is done.

This plugin adds three slash commands and one skill that drive the [Lidnight](https://lidnight.app/en/) menu bar app. If Lidnight isn't installed, they fall back to plain `caffeinate` / `pmset` guidance (nothing is installed or changed without asking).

## Install

```text
/plugin marketplace add whereisdw/lidnight-claude-plugin
/plugin install lidnight@lidnight
```

Lidnight itself (Apple Silicon, macOS 13+; free with the lid open, lid closed on battery is Pro with a 7-day trial): `brew install whereisdw/tap/lidnight` or https://lidnight.app/en/

## Commands

| Command | What it does |
|---|---|
| `/lidnight:awake [auto\|timer N\|until\|keep]` | Start keeping the Mac awake. `auto` (default) stays awake while AI agents work and sleeps ~10 minutes after they go quiet |
| `/lidnight:status` | Is the Mac being kept awake? Runs `lidnight doctor` when something looks off |
| `/lidnight:sleep` | Stop keeping it awake now |

The `keep-awake` skill kicks in when you mention leaving a long task running, closing the lid, or "Your computer went to sleep mid-response".

## What it runs

Everything happens locally, only when you use a command or the skill applies:

- `lidnight start | stop | status | doctor`: the Lidnight app's own CLI (installed from the app's settings)
- `open -g "lidnight://..."`: the app's URL scheme, used when the CLI isn't on your PATH
- `pmset -g` / `pmset -g assertions`: read-only checks of the current sleep state when Lidnight isn't installed

The plugin has no hooks, no MCP servers and no network calls of its own, and it never runs `sudo` or changes power settings without asking you first.

## Why

When a Mac sleeps mid-response, Claude Code drops the partial reply and later rewrites the whole turn, often with no prompt cache, which burns usage limits. Closing the lid on battery is worse: macOS ignores `caffeinate`, and `pmset disablesleep` stays on until you remember to undo it. Lidnight watches Claude Code's hooks so the Mac is awake exactly while work runs.

Disclosure: I build Lidnight. The plugin is MIT licensed and free; Lidnight has a free tier (lid open) and a one-time Pro (lid closed, even on battery).
