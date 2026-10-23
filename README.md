# Lidnight plugin for Claude Code

Five slash commands for Claude Code on macOS. Two of them work on their own, without any app: a **session receipt** and a **usage-limits summary**. The other three keep your MacBook awake while Claude works and let it sleep afterwards; they drive the [Lidnight](https://lidnight.app/en/) menu bar app and fall back to plain `caffeinate` / `pmset` guidance when it isn't installed (nothing is installed or changed without asking).

[English](#install) · [한국어](#한국어)

## Install

```text
/plugin marketplace add whereisdw/lidnight-claude-plugin
/plugin install lidnight@lidnight
```

Lidnight itself is optional (Apple Silicon, macOS 13+): `brew install whereisdw/tap/lidnight` or https://lidnight.app/en/. Free tier: keeps the Mac awake with the lid open (auto mode, and timer mode up to 1 hour). Lid closed is Pro, whether the Mac is on battery or plugged in; there is a 7-day trial. Pricing: https://lidnight.app/en/#pricing

## Commands

| Command | What it does | Needs the Lidnight app? |
|---|---|---|
| `/lidnight:receipt` | Session receipt: how long Claude Code has been running, `claude agents` summary, child processes this session left running, token totals from the latest transcript | No |
| `/lidnight:limits` | Your Claude Code 5-hour and weekly usage in two lines | No |
| `/lidnight:awake [auto\|timer N\|until\|keep]` | Start keeping the Mac awake. `auto` (default) stays awake while AI agents work and sleeps ~10 minutes after they go quiet | Optional: shows `caffeinate` / `pmset` options without it |
| `/lidnight:status` | Is the Mac being kept awake? Runs `lidnight doctor` when something looks off | Optional: reads `pmset` without it |
| `/lidnight:sleep` | Stop keeping it awake now | Optional: checks `pmset` and `caffeinate` without it |

The `keep-awake` skill kicks in when you mention leaving a long task running, closing the lid, or "Your computer went to sleep mid-response".

## What it runs

Everything happens locally, only when you use a command or the skill applies. Each command file also lists its own commands under "What it runs".

- `/lidnight:receipt`: `python3 scripts/receipt.py` (one file in this repo, standard library only, read-only), which calls `ps`, `pgrep -P`, `claude agents --json` (if your `claude` has it) and reads the newest `*.jsonl` under `~/.claude/projects/`
- `/lidnight:limits`: `claude -p /usage --no-session-persistence --setting-sources ""`, and checks whether `/Applications/Lidnight Limits.app` exists
- `lidnight start | stop | status | doctor`: the Lidnight app's own CLI (installed from the app's settings)
- `open -g "lidnight://..."`: the app's URL scheme, used when the CLI isn't on your PATH
- `pmset -g` / `pmset -g assertions` / `pgrep -lx caffeinate`: read-only checks of the current sleep state when Lidnight isn't installed

The plugin has no hooks, no MCP servers and no network calls of its own, and it never runs `sudo` or changes power settings without asking you first.

## Why

When a Mac sleeps mid-response, Claude Code drops the partial reply and later rewrites the whole turn, often with no prompt cache, which burns usage limits. Closing the lid is worse: macOS ignores `caffeinate`, and `pmset disablesleep` stays on until you remember to undo it. Lidnight watches Claude Code's hooks so the Mac is awake exactly while work runs.

## See your limits in the menu bar

`/lidnight:limits` gives you a one-off answer. If you want your Claude Code and Codex 5-hour and weekly limits always visible in the menu bar, there's a free, open-source companion: [Lidnight Limits](https://github.com/whereisdw/lidnight-limits) (`brew install --cask whereisdw/tap/lidnight-limits`). It reads the official `/usage` and Codex's own session logs; nothing leaves your Mac.

For plain hook scripts without any app (answer `AskUserQuestion` from a hook, Stop notifications, ntfy phone push, caffeinate, leftover processes), see [claude-code-hooks-recipes](https://github.com/whereisdw/claude-code-hooks-recipes).

Disclosure: I build Lidnight. The plugin is MIT licensed and free; Lidnight has a free tier (lid open) and a one-time Pro (lid closed, on battery or plugged in).

---

## 한국어

macOS용 Claude Code 슬래시 명령 5개입니다. 둘은 앱 없이 단독으로 동작합니다: **세션 영수증**과 **사용량 한도 요약**. 나머지 셋은 Claude가 일하는 동안 MacBook을 깨워 두고 끝나면 재웁니다. [Lidnight](https://lidnight.app/en/) 메뉴 막대 앱을 제어하며, 앱이 없으면 `caffeinate` / `pmset` 안내로 대신합니다(묻지 않고 설치하거나 설정을 바꾸지 않습니다).

### 설치

```text
/plugin marketplace add whereisdw/lidnight-claude-plugin
/plugin install lidnight@lidnight
```

Lidnight 앱은 선택입니다(Apple Silicon, macOS 13+): `brew install whereisdw/tap/lidnight` 또는 https://lidnight.app/en/. 무료는 뚜껑을 연 상태에서 깨워 두기(자동 모드, 시간 모드 최대 1시간)입니다. 뚜껑 닫힘은 Pro이며, 배터리든 전원 연결이든 같습니다. 7일 체험이 있습니다. 가격: https://lidnight.app/en/#pricing

### 명령

| 명령 | 하는 일 | Lidnight 앱 필요? |
|---|---|---|
| `/lidnight:receipt` | 세션 영수증: Claude Code 실행 시간, `claude agents` 요약, 이 세션이 남긴 자식 프로세스, 최신 대화 기록의 토큰 합계 | 아니오 |
| `/lidnight:limits` | Claude Code 5시간·주간 사용량을 두 줄로 | 아니오 |
| `/lidnight:awake [auto\|timer N\|until\|keep]` | Mac 깨워 두기 시작. `auto`(기본)는 AI 에이전트가 일하는 동안 깨어 있다가 조용해지고 약 10분 뒤 재움 | 선택: 없으면 `caffeinate` / `pmset` 방법을 안내 |
| `/lidnight:status` | Mac이 깨워져 있는지 확인. 이상하면 `lidnight doctor` 실행 | 선택: 없으면 `pmset`으로 확인 |
| `/lidnight:sleep` | 지금 깨워 두기 해제 | 선택: 없으면 `pmset`·`caffeinate` 확인 |

`keep-awake` 스킬은 긴 작업을 걸어 두고 자리를 뜰 때, 뚜껑을 닫을 때, "Your computer went to sleep mid-response"를 언급할 때 동작합니다.

### 실행하는 것

모두 로컬에서, 명령을 쓰거나 스킬이 적용될 때만 실행됩니다. 각 명령 파일의 "What it runs"에도 같은 목록이 있습니다.

- `/lidnight:receipt`: `python3 scripts/receipt.py`(이 저장소의 파일 하나, 표준 라이브러리만, 읽기 전용). 내부에서 `ps`, `pgrep -P`, `claude agents --json`(있을 때)을 호출하고 `~/.claude/projects/` 아래 최신 `*.jsonl`을 읽습니다
- `/lidnight:limits`: `claude -p /usage --no-session-persistence --setting-sources ""`, 그리고 `/Applications/Lidnight Limits.app` 존재 여부 확인
- `lidnight start | stop | status | doctor`: Lidnight 앱 자체의 CLI(앱 설정에서 설치)
- `open -g "lidnight://..."`: 앱의 URL 스킴. CLI가 PATH에 없을 때 사용
- `pmset -g` / `pmset -g assertions` / `pgrep -lx caffeinate`: Lidnight가 없을 때 현재 잠자기 상태를 읽기만 합니다

플러그인에는 훅, MCP 서버, 자체 네트워크 호출이 없고, 묻지 않고 `sudo`를 실행하거나 전원 설정을 바꾸지 않습니다.

### 왜 필요한가

Mac이 응답 도중 잠들면 Claude Code는 받던 응답을 버리고 나중에 그 턴 전체를 다시 쓰는데, 프롬프트 캐시가 없는 경우가 많아 사용량 한도를 태웁니다. 뚜껑을 닫으면 더 나쁩니다. macOS는 `caffeinate`를 무시하고, `pmset disablesleep`은 되돌리는 걸 잊을 때까지 켜져 있습니다. Lidnight는 Claude Code의 훅을 지켜보다가 작업이 도는 동안에만 Mac을 깨워 둡니다.

### 메뉴 막대에서 한도 보기

`/lidnight:limits`는 한 번 확인하는 용도입니다. Claude Code와 Codex의 5시간·주간 한도를 메뉴 막대에 항상 띄워 두려면 무료 오픈소스 동반 앱 [Lidnight Limits](https://github.com/whereisdw/lidnight-limits)(`brew install --cask whereisdw/tap/lidnight-limits`)가 있습니다. 공식 `/usage`와 Codex 자체 세션 로그를 읽으며, 데이터는 Mac 밖으로 나가지 않습니다.

앱 없이 쓰는 훅 스크립트(훅으로 `AskUserQuestion` 답하기, Stop 알림, ntfy 휴대폰 푸시, caffeinate, 남은 프로세스)는 [claude-code-hooks-recipes](https://github.com/whereisdw/claude-code-hooks-recipes)를 보세요.

공개: 저는 Lidnight를 만듭니다. 플러그인은 MIT 라이선스로 무료이고, Lidnight는 무료(뚜껑 연 상태)와 1회 결제 Pro(뚜껑 닫힘, 배터리든 전원 연결이든)가 있습니다.
