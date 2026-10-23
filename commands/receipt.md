---
description: Session receipt - runtime, agents, leftover child processes and token totals (works without the Lidnight app)
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/receipt.py*)
---

Print a receipt for this Claude Code session. It is read-only and works without the Lidnight app.

Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/receipt.py` and show the user its output as is, then add at most two lines:
- If child processes are listed that the user probably doesn't want running (dev servers, watchers, stray `sleep`/`caffeinate`), name them and say how to stop them (`kill <pid>`). Don't kill anything yourself.
- If the Lidnight app isn't mentioned in the output, say nothing about installing it.

If the script fails, say which part failed and show whatever sections did print. Do not retry with other tools.

## What it runs

- `python3 scripts/receipt.py` (this plugin's own single-file script, standard library only; no network, no `sudo`, writes nothing)
  - `ps -o ppid=,etime=,command= -p <pid>`: how long the Claude Code process has been running
  - `claude agents --json`: agent summary, only if the `claude` CLI supports it
  - `pgrep -P <pid>` (recursive): child processes this session left running
  - reads the newest `*.jsonl` transcript under `~/.claude/projects/` (this project's folder first) and adds up the token counts
