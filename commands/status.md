---
description: Show whether Lidnight is keeping this Mac awake, and check its health
allowed-tools: Bash(lidnight *), Bash(pmset -g*)
---

Run `lidnight status`. If the user asked for details or something looks wrong, also run `lidnight doctor` and summarize only the rows that are not OK.
If `lidnight` isn't available, run `pmset -g assertions` and `pmset -g | grep -i sleep` and explain in one or two lines what is currently keeping the Mac awake (or not).
