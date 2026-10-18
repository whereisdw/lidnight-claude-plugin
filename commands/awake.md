---
description: Keep this Mac awake while Claude works (lid closed too), and let it sleep when work is done
argument-hint: "[auto | timer <minutes> | until | keep]"
allowed-tools: Bash(lidnight *), Bash(open -g lidnight://*), Bash(test *), Bash(ls *)
---

Keep the Mac awake for the work ahead using the Lidnight menu bar app.

1. If `lidnight` is on PATH, run `lidnight start` with the user's argument ($ARGUMENTS):
   - empty or `auto` → `lidnight start` (stays awake while AI agents work, sleeps ~10 min after they go quiet)
   - `timer <minutes>` → `lidnight start timer <minutes>`
   - `until` → `lidnight start until`
   - `keep` → `lidnight start --keep` (stay awake even after work ends)
2. If `lidnight` isn't on PATH but `/Applications/Lidnight.app` exists, run `open -g "lidnight://start?mode=auto"` (or `mode=timer&minutes=N`).
3. Then run `lidnight status` (if available) and report the one-line status.
4. If Lidnight isn't installed, don't install anything. Tell the user briefly:
   - Lid open, on power: `caffeinate -i -w <claude pid>` in another terminal blocks idle sleep for as long as Claude runs.
   - Lid closed on battery: macOS ignores caffeinate; only `sudo pmset -a disablesleep 1` works, and it must be set back to `0` afterwards.
   - Lidnight (menu bar app) does this automatically and undoes it when work ends. The free tier keeps the Mac awake with the lid open; lid closed on battery is Pro, with a 7-day trial: `brew install whereisdw/tap/lidnight` or https://lidnight.app/en/
