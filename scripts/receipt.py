#!/usr/bin/env python3
"""Session receipt for Claude Code: runtime, agents, leftover child processes, token totals.

Read-only. Standard library only. No network, no sudo. Works on macOS and Linux.
Usage: receipt.py [--pid CLAUDE_PID] [--projects-dir DIR]
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys


def run(cmd, timeout=10):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    return p.stdout if p.returncode == 0 else None


def parse_etime(s):
    """ps etime ([[dd-]hh:]mm:ss) -> seconds."""
    m = re.fullmatch(r"(?:(\d+)-)?(?:(\d+):)?(\d+):(\d+)", s.strip())
    if not m:
        return None
    d, h, mi, se = (int(x or 0) for x in m.groups())
    return ((d * 24 + h) * 60 + mi) * 60 + se


def fmt_duration(sec):
    if sec is None:
        return "unknown"
    h, rem = divmod(int(sec), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m"
    return f"{m}m {s:02d}s" if m else f"{s}s"


def ps_info(pid):
    """-> (ppid, etime_seconds, command) or None."""
    out = run(["ps", "-o", "ppid=,etime=,command=", "-p", str(pid)])
    if not out or not out.strip():
        return None
    parts = out.strip().split(None, 2)
    if len(parts) < 3:
        return None
    return int(parts[0]), parse_etime(parts[1]), parts[2]


def is_claude(command):
    exe = os.path.basename(command.split()[0]) if command.split() else ""
    return exe == "claude" or exe.startswith("claude-code")


def find_claude_pid(start):
    pid = start
    for _ in range(32):
        info = ps_info(pid)
        if not info:
            return None
        ppid, _, command = info
        if is_claude(command):
            return pid
        if ppid <= 1:
            return None
        pid = ppid
    return None


def children(pid):
    out = run(["pgrep", "-P", str(pid)])
    return [int(x) for x in out.split()] if out else []


def process_tree(root, skip):
    """Descendants of root as (depth, pid, etime_sec, command), skipping the pids in `skip`."""
    rows = []

    def walk(pid, depth):
        for c in children(pid):
            if c in skip:
                continue
            info = ps_info(c)
            if info:
                rows.append((depth, c, info[1], info[2]))
                walk(c, depth + 1)

    walk(root, 1)
    return rows


def ancestors(pid):
    seen = set()
    while pid and pid > 1 and pid not in seen:
        seen.add(pid)
        info = ps_info(pid)
        if not info:
            break
        pid = info[0]
    return seen


def project_dir_for(cwd, projects):
    return os.path.join(projects, re.sub(r"[^A-Za-z0-9]", "-", cwd))


def newest_jsonl(projects):
    cands = glob.glob(os.path.join(project_dir_for(os.getcwd(), projects), "*.jsonl"))
    if not cands:
        cands = glob.glob(os.path.join(projects, "*", "*.jsonl"))
    return max(cands, key=os.path.getmtime) if cands else None


def token_totals(path):
    keys = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
    totals = dict.fromkeys(keys, 0)
    seen = set()
    turns = 0
    first_ts = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if not isinstance(ev, dict):
                continue
            first_ts = first_ts or ev.get("timestamp")
            msg = ev.get("message")
            if ev.get("type") != "assistant" or not isinstance(msg, dict):
                continue
            usage = msg.get("usage")
            if not isinstance(usage, dict):
                continue
            # streaming writes the same message several times; count each id once
            ident = (msg.get("id"), ev.get("requestId"))
            if ident != (None, None):
                if ident in seen:
                    continue
                seen.add(ident)
            turns += 1
            for k in keys:
                v = usage.get(k)
                if isinstance(v, int):
                    totals[k] += v
    return totals, turns, first_ts


def agents_summary():
    if not shutil.which("claude"):
        return "claude CLI not on PATH"
    out = run(["claude", "agents", "--json"], timeout=15)
    if out is None:
        return "not available (claude agents --json failed or is unsupported)"
    try:
        data = json.loads(out)
    except ValueError:
        return "unreadable output from claude agents --json"
    if isinstance(data, dict):
        for k in ("agents", "items", "sessions"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    if not isinstance(data, list):
        return "unrecognized output shape"
    if not data:
        return "none"
    lines = [f"{len(data)} listed"]
    for a in data[:8]:
        if isinstance(a, dict):
            label = a.get("name") or a.get("id") or a.get("sessionId") or "?"
            status = a.get("status") or a.get("state")
            lines.append(f"  - {label}" + (f" [{status}]" if status else ""))
        else:
            lines.append(f"  - {a}")
    if len(data) > 8:
        lines.append(f"  ... and {len(data) - 8} more")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pid", type=int, help="Claude Code process id (default: found by walking up parents)")
    ap.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"))
    args = ap.parse_args()

    me = os.getpid()
    claude_pid = args.pid or find_claude_pid(os.getppid())
    info = ps_info(claude_pid) if claude_pid else None

    print("Session receipt")
    print("---------------")
    jsonl = newest_jsonl(args.projects_dir) if os.path.isdir(args.projects_dir) else None
    totals, turns, first_ts = token_totals(jsonl) if jsonl else (None, 0, None)

    if info:
        print(f"Process:  pid {claude_pid}, running {fmt_duration(info[1])}")
    else:
        print("Process:  Claude Code process not found; showing transcript data only")
    if first_ts:
        print(f"Started:  {first_ts} (first transcript entry)")
    print()

    print("Agents:")
    summary = agents_summary()
    print("  " + summary.replace("\n", "\n  "))
    print()

    print("Child processes of this session:")
    if claude_pid:
        # skip this script and the shells that launched it
        rows = process_tree(claude_pid, ancestors(me) | {me})
        if rows:
            for depth, pid, et, cmd in rows[:30]:
                print(f"  {'  ' * (depth - 1)}{pid}  {fmt_duration(et):>8}  {cmd[:100]}")
            if len(rows) > 30:
                print(f"  ... and {len(rows) - 30} more")
        else:
            print("  none")
    else:
        print("  unknown (no Claude Code process found)")
    print()

    print("Tokens (latest transcript):")
    if totals:
        total = sum(totals.values())
        print(f"  file:           {jsonl}")
        print(f"  assistant msgs: {turns}")
        print(f"  input:          {totals['input_tokens']:,}")
        print(f"  output:         {totals['output_tokens']:,}")
        print(f"  cache write:    {totals['cache_creation_input_tokens']:,}")
        print(f"  cache read:     {totals['cache_read_input_tokens']:,}")
        print(f"  total:          {total:,}")
    else:
        print(f"  no transcript found under {args.projects_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
