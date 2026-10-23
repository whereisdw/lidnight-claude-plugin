---
description: Show whether this Mac is being kept awake, and check its health (Lidnight, or plain pmset)
allowed-tools: Bash(lidnight *), Bash(pmset -g*), Bash(pgrep *)
---

Run `lidnight status`. If the user asked for details or something looks wrong, also run `lidnight doctor` and summarize only the rows that are not OK.

If `lidnight` isn't available, don't suggest installing it. Run `pmset -g assertions`, `pmset -g | grep -i sleep` and `pgrep -lx caffeinate`, and explain in one or two lines what is currently keeping the Mac awake (or that nothing is, so it will sleep on idle or when the lid closes).

## What it runs

- `lidnight status | doctor`: the Lidnight app's CLI
- `pmset -g assertions`, `pmset -g`, `pgrep -lx caffeinate`: read-only, used when Lidnight isn't installed
