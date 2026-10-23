---
description: Stop keeping the Mac awake now (Lidnight), and check nothing else is holding it awake
allowed-tools: Bash(lidnight *), Bash(open -g lidnight://*), Bash(pmset -g*), Bash(pgrep *), Bash(grep *)
---

Run `lidnight stop` (or `open -g "lidnight://stop"` if the command isn't on PATH), then `lidnight status` and report the result in one line.

If Lidnight isn't installed, don't tell the user to install it. Check by hand and report what you find:
- `pmset -g | grep -i sleepdisabled`: if it shows `1`, `disablesleep` is on. Give the user `sudo pmset -a disablesleep 0` to run themselves. Don't run sudo.
- `pgrep -lx caffeinate`: if a `caffeinate` is running, name it and say `kill <pid>` ends it. Don't kill it yourself.
- If neither is found, say nothing is holding the Mac awake from these two sources, and that `pmset -g assertions` lists any other holders.

## What it runs

- `lidnight stop | status`: the Lidnight app's CLI
- `open -g "lidnight://stop"`: the app's URL scheme, if the CLI isn't on PATH
- `pmset -g` and `pgrep -lx caffeinate`: read-only checks, only when Lidnight isn't installed
