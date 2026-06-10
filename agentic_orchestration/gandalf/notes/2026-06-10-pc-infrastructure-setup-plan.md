# PC Infrastructure Setup Plan — tmux + Permission Allowlist Refinement for Autonomous PC Hive-Mind Cycles

**STATUS:** CURRENT (next-session plan; load-bearing for PC infrastructure setup session)
**Date:** 2026-06-10
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-10 directive — "we dont need to solve for this session, but we do need to solve for the next session" (referring to PC infrastructure brittleness + permission-allowlist friction surfaced during 2026-06-09 evening PC hive-mind cycle)
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-09-next-session-plan-post-branch-A-lock.md` (next-session plan; this PC infrastructure setup is a SEPARATE focused setup session, not the design-trajectory continuation)
- `agentic_orchestration/skill_handoff_2026-06-09.md` (KR orchestration handoff)
- `CLAUDE.md` (meta-repo) — federated PC team architecture + commit/push discipline addendum
- `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` (PC team operational architecture)

---

## 0. TL;DR

PC hive-mind autonomous cycles surfaced two operational ceilings during 2026-06-09 evening:
1. **SSH session persistence is brittle** — connection drops mid-flight kill the David-H session (tmux not installed on PC; no Windows-native equivalent durable through SSH disconnect)
2. **Permission allowlist is too narrow for autonomous operation** — every safe diagnostic operation (git ls-files, where commands, common PowerShell queries) triggers per-operation Matt approval; defeats autonomy purpose

**Matt 2026-06-10 directive — TWO-PHASE APPROACH ratified:**

### Phase 1 + Phase 1.5 CONCURRENT (NEXT SESSION) — Settings refinement + script-wrapping
**Just** refine PC `.claude/settings.local.json` to broad-allow safe operations + author small wrapper `.ps1` files for common compound scripts. **NO tmux install. NO WSL install. NO system-state changes.** Pure settings-file refinement + script authoring, additive only, reversible if needed.

Rationale: Matt 2026-06-10 — "git is the main problem" + amendment "would it make sense to search for common applicable patterns from our mac team's work?" Investigation found:
- Mac `.claude/settings.local.json` has accumulated broad wildcards over months (`Bash(git *)`, `Bash(python3 *)`, broad path globs); PC has not
- Compound PowerShell scripts (RAM check, bridge polling) hit Claude Code's expandable-strings + subexpressions safety checks that allowlist refinement does NOT bypass
- Phase 1 alone delivers ~50-60% friction reduction; Phase 1.5 (script-wrapping) eliminates the residual compound-script friction
- Both fire CONCURRENTLY next session — no reason to defer Phase 1.5 to empirical trigger when authoring is bounded

**Phase 1 scope (~30 min next session) — settings refinement:**
- Read Mac `.claude/settings.local.json` for portable wildcard patterns per § 2.7 analysis
- Append broad wildcards + PowerShell diagnostic patterns + tool-level patterns to PC `.claude/settings.local.json` per § 2.3
- Commit settings change with `david-h` prefix per CLAUDE.md addendum

**Phase 1.5 scope (~1-2 hour same session) — script-wrapping:**
- Author 3-5 common compound PowerShell scripts as `agentic_orchestration/pc-scripts/*.ps1` files per § 2.6 Strategy A
- Allowlist each script's invocation as a single fixed-string pattern
- Commit + push both phases together per PC-seam standing wave-close pattern
- Test next autonomous wave-cycle for friction reduction

### Phase 2 (DEFERRED — subsequent setup session)
**Full PC infrastructure setup** — WSL2 + Ubuntu + tmux install + docs update + comprehensive autonomous-cycle test. **Fires only if Phase 1 proves insufficient** OR session-persistence friction becomes pressing (e.g., autonomous cycles need to run beyond Matt active-monitoring windows).

**Phase 2 scope (~1-2 hour focused session; deferred):**
- Install WSL2 + Ubuntu + tmux on PC (~30-45 min; one-time admin + reboot)
- Update CLAUDE.md + PC team OPs with new tmux-wrapped invocation pattern (~30 min gandalf authoring)
- Test autonomous PC hive-mind cycle end-to-end with full infrastructure (~30 min)

**This document captures BOTH phases.** Phase 1 fires next session per § 2.3 + § 4.2-α below. Phase 2 fires when triggered per § 4.2-β below.

---

## 1. Problem 1 — tmux install for SSH session persistence

### 1.1 The problem

Current PC SSH invocation pattern is direct (no session-multiplexer wrapping). If SSH connection drops mid-cycle (PC sleep, network blip, Mac sleep, idle timeout), David-H session dies with no recovery. The 2026-06-09 evening cycle hit this:
- David-H ran successfully for ~50 min through Mantis sub-agent fire + permission-wall surfacing + 3-path proposal
- SSH connection dropped at the interactive menu (`Connection reset by peer`)
- Matt's "Path A — Approve" landed at Mac local shell instead of reaching David-H
- David-H session was lost; needed full re-engagement with re-engagement prompt

**Tmux solves this** — session persists on PC even when SSH disconnects; attach/detach via `tmux attach -t <session-name>` from any subsequent SSH connection.

### 1.2 Investigation findings (2026-06-09 evening)

| Tool | Status on PC |
|---|---|
| `tmux` | NOT installed |
| `winget` (Windows package manager) | Installed but source data corrupted (`error 0x8a15000f`); non-interactive fix did not succeed |
| WSL (Windows Subsystem for Linux) | NOT installed (requires admin + reboot) |
| MSYS2 (standalone) | NOT installed |
| Git for Windows / Git Bash | Installed at `C:\Program Files\Git\` but NOT in PATH; default install does NOT include tmux |
| `claude.exe` | At `C:\Users\mhwet\.local\bin\claude.exe` |
| `node.exe` | At `C:\Program Files\nodejs\` |

### 1.3 Recommended path — WSL2 + Ubuntu + tmux (Path B)

**Why WSL over alternatives:**
- Most robust long-term Linux tooling on PC
- Native tmux + apt package management
- Integrates with Windows file system via `/mnt/c/` mounts
- Future-proofs PC for other Linux-tooling needs (Python tools, build tools, etc.)
- Anthropic + Microsoft both recommend WSL for Claude Code on Windows

**Concrete steps (Matt at PC; admin PowerShell):**

```powershell
# 1. Install WSL2 (admin PowerShell required; will prompt for reboot)
wsl --install

# 2. After reboot, set up Ubuntu user account when prompted (username + password)

# 3. Inside Ubuntu (via Start menu → Ubuntu, or `wsl -d Ubuntu` from PowerShell):
sudo apt update
sudo apt install -y tmux
tmux -V  # verify install (expect "tmux 3.x")
```

**Time estimate:** ~30-45 min including reboot.

### 1.4 Alternative paths (if WSL is undesirable)

**Path C — Manual MSYS2 standalone install:**
- Download MSYS2 installer from https://www.msys2.org/
- Run installer (default install location `C:\msys64`); takes ~5 min
- Open MSYS2 MSYS shell from Start menu
- Run: `pacman -Syu` (initial sync; may require restart of shell)
- Run: `pacman -S tmux`
- Add `C:\msys64\usr\bin` to Windows PATH for global tmux access

Lighter than WSL but loses broader Linux tooling.

**Path A — Fix winget locally then install MSYS2 via winget:**
- Open winget interactively on PC console (may prompt to accept msstore agreement → accept once)
- `winget install MSYS2.MSYS2`
- Then same MSYS2 steps as Path C for tmux

May or may not succeed depending on winget source state.

### 1.5 Post-install tmux invocation pattern

Once tmux is installed (via any path), the canonical PC-team SSH invocation becomes:

**Direct (WSL path):**
```bash
ssh -t mhwet@192.168.1.133 "wsl -d Ubuntu -- tmux new-session -A -s david-h-wave 'cd /mnt/c/dev/reincarnated-collaboration && claude --agent david-h'"
```

**Direct (MSYS2 path):**
```bash
ssh -t mhwet@192.168.1.133 "C:\msys64\usr\bin\tmux.exe new-session -A -s david-h-wave 'cd C:\dev\reincarnated-collaboration && claude --agent david-h'"
```

**Reattach (any path):**
```bash
ssh -t mhwet@192.168.1.133 "<path-to-tmux> attach -t david-h-wave"
```

---

## 2. Problem 2 — Permission allowlist refinement for autonomous PC operation

### 2.1 The problem

`.claude/settings.local.json` on PC uses **narrow exact-string allowlist** discipline. 50+ specific entries built incrementally across Sessions 1+2 of PC team setup. Each new command outside the allowlist triggers a per-operation Matt approval prompt.

**This pattern was built for one-off Pattern A sub-agent invocations** where each session adds a handful of new entries. **It doesn't scale to autonomous wave-cycles** where David-H legitimately needs to run many varied diagnostic + execution commands.

Sample friction observed 2026-06-09 evening (Matt verbatim sample):

```
PowerShell command
git ls-files .claude/settings.local.json; if ($?) { git check-ignore -v .claude/settings.local.json }
Check if settings.local.json is git-tracked or ignored

Do you want to proceed?
[1] Yes  [2] No
```

That's a safe defensive check (verify git state before modifying) but it hits the permission wall and routes to Matt. Death-by-thousand-cuts pattern; defeats autonomy purpose.

### 2.2 Recommended refinement principles

**Two-tier allowlist architecture:**

| Tier | Pattern shape | Examples |
|---|---|---|
| **Broad-pattern allowed** (autonomous-safe) | Read operations + diagnostic queries + git read commands + common PowerShell queries | `PowerShell(git status*)`, `PowerShell(git log*)`, `PowerShell(git ls-files*)`, `PowerShell(git check-ignore*)`, `PowerShell(git diff*)`, `PowerShell(where *)`, `PowerShell(Get-Command*)`, `PowerShell(Get-Process*)`, `PowerShell(Get-Location*)`, `PowerShell(Test-Path*)`, `Read(...)`, etc. |
| **Narrow exact-string** (preserve audit discipline) | Write operations + scope-amendment operations + arbitrary process spawning + MCP user-level tools | `Write(C:\dev\reincarnated-collaboration\path\to\specific\file)`, `Write(C:\dev\reincarnated-unreal\specific\subtree)`, exact Start-Process for UE Editor, etc. |

**Discipline preserved:** narrow allowlist remains for the **truly load-bearing operations** (writes that mutate the project state; process spawning that could affect system state; tool invocations that exceed PC seam authority). **Broad allowlist for safe read/diagnostic operations** that David-H legitimately needs to run dozens of times per autonomous cycle.

### 2.3 Specific recommended additions

**Add broad patterns (autonomous-safe):**

```json
{
  "permissions": {
    "allow": [
      // ... existing 50+ narrow entries preserved ...

      // === NEW: broad diagnostic + read patterns for autonomous operation ===

      // Git read operations (any path)
      "PowerShell(git status*)",
      "PowerShell(git log*)",
      "PowerShell(git diff*)",
      "PowerShell(git show*)",
      "PowerShell(git ls-files*)",
      "PowerShell(git check-ignore*)",
      "PowerShell(git rev-parse*)",
      "PowerShell(git config --get*)",
      "PowerShell(git remote -v*)",
      "PowerShell(git branch*)",
      "PowerShell(git stash list*)",
      "PowerShell(git ls-tree*)",
      "PowerShell(git blame*)",

      // PowerShell diagnostic queries (safe; read-only)
      "PowerShell(where *)",
      "PowerShell(Get-Command*)",
      "PowerShell(Get-Process*)",
      "PowerShell(Get-Location*)",
      "PowerShell(Get-ChildItem*)",
      "PowerShell(Test-Path*)",
      "PowerShell(Get-Item*)",
      "PowerShell(Get-Content*)",
      "PowerShell(Resolve-Path*)",

      // PowerShell system / hardware introspection (safe; read-only)
      "PowerShell(Get-WmiObject*)",
      "PowerShell(Get-CimInstance*)",
      "PowerShell(Get-ComputerInfo*)",
      "PowerShell(Get-PSDrive*)",
      "PowerShell(Get-Service*)",
      "PowerShell(Get-EventLog*)",

      // Common safe Windows commands
      "PowerShell(dir*)",
      "PowerShell(echo *)",
      "PowerShell(cd *)",

      // Read operations (Claude Code Read tool; any path within scope)
      "Read(C:\\dev\\**)",
      "Read(C:\\Users\\mhwet\\.claude\\**)",
      "Read(C:\\Program Files\\Git\\**)"
    ]
  }
}
```

### 2.4 What stays narrow exact-string

**Preserve narrow allowlist for:**

- **Write operations** — every specific write path that's authorized stays in narrow allowlist (forces explicit per-target-file authorization)
- **Start-Process for executables** — each authorized executable invocation stays narrow (UE Editor windowed mode, specific tool launches)
- **Network operations** — explicit per-URL or per-API allowlist (don't broad-allow)
- **MCP user-level tools** — explicit per-tool authorization
- **Arbitrary script execution** — keep narrow

### 2.5 Estimated friction reduction (with honest caveats)

**For SIMPLE single-cmdlet commands** (git status, where claude, Get-Process node, Get-WmiObject Win32_OperatingSystem):
- Pre-refinement: hits permission prompt
- Post-refinement: passes via broad pattern match → ~10-15 prompts → ~1-3 prompts

**For COMPOUND scripts with PowerShell language features** (e.g., the 2026-06-09 RAM-check command + the bridge-ready-polling script):
- Pre-refinement: hits permission prompt
- Post-refinement: STILL hits permission prompt — **allowlist refinement does NOT bypass Claude Code's built-in safety checks**

Claude Code surfaces three intentional safety mechanisms for PowerShell that operate INDEPENDENTLY of the settings.local.json allowlist:

| Safety check | Triggered by | Example |
|---|---|---|
| **Expandable strings with embedded expressions** | Variable interpolation in strings (`"$var"`); compound `;`-separated statements with variable assignments | `$x = ...; "Result: $x"` |
| **Subexpressions $()** | PowerShell subexpression syntax (`$(expression)`) — evaluates arbitrary expression and embeds result | `"Timeout: $(6*60)s"` |
| **Complex control flow** | `for`, `while`, `if/elseif/else`, compound conditionals with multiple cmdlets | The 2026-06-09 evening bridge-ready-polling script |

**These are intentional Claude Code security design — NOT allowlist gaps.** Settings refinement does not bypass them.

**Net friction reduction Phase 1 will deliver:**
- Simple git read commands: friction near-zero (~80-90% of David-H's diagnostic operations)
- Simple PowerShell single-cmdlet queries: friction near-zero (with the patterns in § 2.3)
- Compound PowerShell scripts: friction PERSISTS (will continue to surface per-operation Matt approval)

**Realistic post-Phase-1 estimate:** autonomous wave-cycles drop from ~10-15 per-cycle prompts to ~3-5 per-cycle prompts. NOT ≤2 as I overpromised earlier. The 3-5 residual prompts come from the compound-script operations that hit safety checks beyond allowlist.

### 2.6 Mitigation strategies for compound-script friction (Phase 1.5 candidate)

For the residual ~3-5 compound-script prompts per cycle, three mitigation strategies are available WITHOUT bypassing Claude Code safety:

**Strategy A — Pre-commit common compound scripts as project `.ps1` files**

Author small `.ps1` files in `agentic_orchestration/pc-scripts/` (or similar):
- `check-ram.ps1` — RAM diagnostic check (replaces the 2026-06-09 inline RAM command)
- `poll-bridge-ready.ps1` — bridge-ready polling (replaces the bridge-polling script)
- `windowed-niagara-verify.ps1` — windowed-mode Niagara verification orchestration

Then allowlist the SCRIPT INVOCATION (which is a single fixed-string pattern):
```json
"PowerShell(* agentic_orchestration/pc-scripts/check-ram.ps1*)",
"PowerShell(* agentic_orchestration/pc-scripts/poll-bridge-ready.ps1*)",
"PowerShell(* agentic_orchestration/pc-scripts/windowed-niagara-verify.ps1*)"
```

Script CONTENT contains the compound logic (safe under Claude Code rules because it's a file, not an inline command); INVOCATION is the allowlisted operation. David-H + Mantis + Sam can iterate inside the script without re-prompting.

**Tradeoff:** requires one-time gandalf authoring of the scripts. Each script becomes a versioned + audited piece of project infrastructure. Higher upfront cost but eliminates per-operation friction.

**Strategy B — Refactor inline compound scripts into simpler sequential cmdlets**

When David-H + Mantis surface compound-PowerShell needs, refactor into sequential simpler commands. E.g., the RAM check could be split:
- Step 1: `Get-WmiObject Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize` (single cmdlet; allowlist passes)
- Step 2: Claude parses output + computes GB conversion in its own context

Tradeoff: more verbose; more tool calls per operation; but each tool call passes the allowlist cleanly.

**Strategy C — Accept residual friction as audit-discipline cost**

The 3-5 prompts/cycle on compound scripts represent Claude Code surfacing the highest-risk operations for explicit Matt approval. Treating these as intentional Matt-approval moments preserves audit discipline. Strategy A reduces friction at cost of script authoring; Strategy B at cost of verbosity; Strategy C accepts friction in favor of audit clarity.

**Phase 1.5 PROMOTED TO CONCURRENT WITH PHASE 1 (per Matt 2026-06-10 amendment).** Author the most-common compound scripts as `.ps1` files in same session as Phase 1 settings refinement. Gandalf-side authoring (~1-2 hours). Concurrent firing rationale: bounded authoring; eliminates compound-script friction in 1 session vs waiting for empirical trigger (which would burn 2+ wave-cycles before fix lands).

### 2.7 Mac team settings.local.json analysis — what ports to PC

Investigation of Mac `.claude/settings.local.json` (102 lines / ~95 entries; accumulated since 2026-05-13) reveals what categories Mac team has allowlisted + what's portable to PC.

#### 2.7.1 Mac patterns that PORT DIRECTLY (tool-level; not shell-specific)

These apply identically on PC because they target Claude Code TOOLS, not specific shell commands. Should be added to PC settings verbatim or near-verbatim:

```json
"WebSearch",
"WebFetch(domain:github.com)",
"WebFetch(domain:pixijs.com)",
"WebFetch(domain:www.poewiki.net)",
"WebFetch(domain:maxroll.gg)",
"WebFetch(domain:mobalytics.gg)",
"WebFetch(domain:www.purediablo.com)",
"WebFetch(domain:diablo.fandom.com)",
"WebFetch(domain:wiki.projectdiablo2.com)",
"WebFetch(domain:www.thegamer.com)",
"WebFetch(domain:diablo2.wiki.fextralife.com)",
"WebFetch(domain:www.poe-vault.com)",
"WebFetch(domain:www.icy-veins.com)",
"WebFetch(domain:pathofexile.fandom.com)",
"Skill(update-config)"
```

**Net add:** 14 tool-level entries; immediate friction reduction on research / config operations.

#### 2.7.2 Mac patterns that PORT BY ANALOGY (shell command equivalents)

These are Bash patterns that PowerShell needs an equivalent for. The Mac team accepted BROAD wildcards here:

| Mac (Bash) | PC equivalent (PowerShell) | Rationale |
|---|---|---|
| `Bash(git *)` | `PowerShell(git *)` | Mac accepted ANY git operation; matches operational pattern |
| `Bash(python3 *)` | `PowerShell(python *)` + `PowerShell(node *)` | Mac broad-allows python3; PC equivalents per PC tooling |
| `Bash(curl *)` (implicit via specific entries) | `PowerShell(Invoke-WebRequest*)` + `PowerShell(Invoke-RestMethod*)` | PowerShell HTTP cmdlets |

**Observation:** Mac team broadened `Bash(git *)` rather than my originally-proposed split-by-read-vs-write. This is the actual operational truth: destructive git operations are rare; audit at workstream-monitoring layer, not per-command-prompt layer. PC team should follow the same broad pattern.

**Recommendation amendment to § 2.3:** replace the granular git read patterns with single `PowerShell(git *)` matching Mac precedent. Audit discipline preserved at workstream-monitoring level (Sam Gate-2 + David-H wave-close memo) where it actually operates.

#### 2.7.3 Mac patterns NOT useful for PC port

- 70+ historical specific commands (sqlite3 queries against Mac-specific paths; specific cp/mv/sed/grep one-shots accumulated over months)
- Mac-specific path Reads (`Read(//Users/admin/...)` — need C:\ translation)
- Mac-specific shell idioms (`xargs`, `sed -i ''`, etc.)

**Net:** ignore these; they're Mac-historical-noise.

#### 2.7.4 Why Mac team has less friction than PC team (3 reasons)

1. **Claude Code safety model is shell-specific.** Bash has fewer "this is dangerous syntax" warnings than PowerShell. PowerShell-specific safety checks (expandable strings, subexpressions `$()`, complex control flow) don't have direct Bash equivalents.

2. **Cumulative settings.local.json maturity.** Mac team has been operating since ~2026-05-13 (1+ month); PC team since 2026-06-07 (3 days). Mac settings has accumulated ~95 entries through cumulative "Yes, and don't ask again" approvals. PC has narrow exact-string allowlist built incrementally over 1-2 sessions.

3. **Operational pattern differences.** Mac team work is mostly Read/Edit/Write tool operations (bypass shell) + simple git + simple file commands. PC team work necessarily uses PowerShell because Windows tooling (UE Editor launch, log polling, hardware diagnostics) is PowerShell-native — and more compound PowerShell → more friction per Claude Code safety model.

**Net implication for PC strategy:** PC team needs more BROADENING (Phase 1) + more SCRIPT-WRAPPING (Phase 1.5) than Mac team needed because the operational pattern is inherently PowerShell-compound-heavy. The plan reflects this reality.

---

## 3. Problem 3 — Update team docs for new infrastructure

### 3.1 CLAUDE.md amendment

Replace current PC SSH launch examples with tmux-wrapped pattern. Add post-install reference for both attach + detach + kill operations.

Specific § "Mobile-accessible sessions via Claude Code Remote Control" section already covers persistence considerations; extend with tmux-wrapped pattern for SSH.

### 3.2 PC team operating procedures

Each of David-H + Sam + Radagast + Mantis OP skills references the SSH invocation pattern. Update to tmux-wrapped pattern post-install.

### 3.3 Federated PC team architecture commit (`canonical/story/2026-06-07-federated-pc-team-architecture-commit.md`)

Append amendment section: "PC infrastructure refinement 2026-06-XX: WSL + tmux installed + permission allowlist refined for autonomous wave-cycle support" with cross-reference to this plan doc.

---

## 4. Recommended setup-session sequencing

### 4.1 Pre-session prep
- (Phase 1) NONE — settings refinement is gandalf-side authoring; no Matt-side prep needed
- (Phase 2, deferred) Backup PC settings.local.json + identify good time window for PC reboot (WSL install requires it)

### 4.2-α PHASE 1 + PHASE 1.5 CONCURRENT — Settings refinement + script-wrapping (NEXT SESSION; ~2-3 hour wall-clock)

| Step | Action | Owner | Time |
|---|---|---|---|
| 1 | Gandalf reads current PC `.claude/settings.local.json` via SSH | gandalf | ~5 min |
| 2 | Gandalf reads Mac `.claude/settings.local.json` for portable wildcards per § 2.7 | gandalf | ~5 min |
| 3 | Gandalf authors PC settings refinement: broad wildcards (`PowerShell(git *)` etc.) + tool-level patterns (WebSearch, WebFetch domains, Skills) + diagnostic patterns per § 2.3 | gandalf | ~15 min |
| 4 | Gandalf authors 3-5 wrapper `.ps1` scripts at `agentic_orchestration/pc-scripts/` per § 2.6 Strategy A (check-ram.ps1 / poll-bridge-ready.ps1 / windowed-niagara-verify.ps1 / log-tail.ps1 / git-state-snapshot.ps1) | gandalf | ~60-90 min |
| 5 | Gandalf appends per-script invocation allowlist entries to PC settings | gandalf | ~5 min |
| 6 | Gandalf commits all changes with `david-h` prefix per CLAUDE.md addendum via SSH | gandalf via SSH | ~5 min |
| 7 | Push per PC-seam standing wave-close pattern | gandalf via SSH | ~5 min |
| 8 | Brief autonomous-cycle test: fire David-H with diagnostic tasks invoking both broad wildcards + wrapper scripts; verify ≤2 Matt-interruption prompts | gandalf + Matt monitors | ~15 min |
| 9 | Gandalf updates ground-state oracle § 5 + this plan doc § 0 to note Phase 1 + 1.5 complete | gandalf | ~10 min |

**Phase 1 + 1.5 acceptance criteria:**
- ✅ PC `.claude/settings.local.json` extended with broad wildcards (matching Mac precedent per § 2.7) + tool-level patterns + diagnostic patterns
- ✅ Narrow exact-string allowlist preserved for write + scope-amendment operations per § 2.4
- ✅ 3-5 wrapper `.ps1` scripts authored at `agentic_orchestration/pc-scripts/` covering common compound-PowerShell operations
- ✅ Wrapper script invocations allowlisted as single fixed-string patterns
- ✅ Settings + scripts committed + pushed via PC-seam standing wave-close pattern
- ✅ Brief autonomous-cycle test shows friction reduction (≤2 Matt-interruption prompts on mixed diagnostic + script-invoking tasks; vs ~10-15 pre-refinement)
- ✅ Ground-state oracle updated; this plan § 0 TL;DR notes Phase 1 + 1.5 complete

**Phase 1 + 1.5 done — return to design-trajectory work** (Pattern B icon design / WS2 commission authoring / etc. per `2026-06-09-next-session-plan-post-branch-A-lock.md`).

### 4.2-β PHASE 2 — Full infrastructure setup (DEFERRED; fires only on empirical trigger)

| Step | Action | Owner | Time |
|---|---|---|---|
| 1 | Install WSL2 via admin PowerShell (`wsl --install`) + reboot | Matt at PC | ~15 min + reboot |
| 2 | Set up Ubuntu user account + install tmux (`sudo apt install tmux`) | Matt in WSL shell | ~10 min |
| 3 | Test tmux from SSH: `ssh -t mhwet@192.168.1.133 "wsl -d Ubuntu -- tmux ls"` | Matt from Mac | ~5 min |
| 4 | Gandalf updates CLAUDE.md + PC team OPs + federated PC team architecture commit doc per § 3 | gandalf | ~30 min |
| 5 | Test autonomous PC hive-mind end-to-end with full infrastructure | David-H autonomous + Matt monitors | ~30 min |
| 6 | Push + commit + skill_handoff for cross-session continuity | KR | ~10 min |

**Phase 2 firing triggers (any one):**
- Phase 1 proves insufficient (friction not adequately reduced; autonomous cycles still hit operational ceiling)
- Session-persistence friction becomes pressing (autonomous cycles need to run beyond Matt active-monitoring windows; e.g., WS2 commission execution at AAA-fidelity scope warrants 1-2 hour autonomous wave-cycles)
- New PC-side tooling needed that justifies WSL install for broader Linux tooling ecosystem

**Phase 2 acceptance criteria** (when fired):
- ✅ tmux installed and operational on PC (via WSL or alternative)
- ✅ SSH-via-tmux invocation pattern documented + tested
- ✅ Test autonomous wave-cycle completes with ≤3 Matt-interruption prompts
- ✅ CLAUDE.md + PC team OP docs updated
- ✅ Cross-session continuity preserved (skill_handoff + ground-state oracle § 5 updates)

---

## 5. Resume protocol for setup session

Setup-session gandalf reads in order (per gandalf OP § 1):

1. `canonical/00-ground-state.md` § 1 + § 5 (refresh state)
2. **This plan doc** (PC infrastructure setup plan)
3. `agentic_orchestration/skill_handoff_2026-06-09.md` (orchestration handoff)
4. `agentic_orchestration/gandalf/notes/2026-06-09-next-session-plan-post-branch-A-lock.md` (parallel next-session plan; design trajectory)
5. `CLAUDE.md` (current PC team launch pattern; will be amended this session)
6. `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` (PC team architecture; will receive amendment)

Then engage Matt direction per § 4.1 pre-session prep + § 4.2 step 1.

---

## 6. Composition with prior canonical commitments

This plan composes natively with:
- **Federated PC team architecture** (2026-06-07) — refines operational ceiling without changing seam-bound authority + cross-host coordination model
- **CLAUDE.md team commit + push discipline addendum** (2026-05-25) — preserves auto-commit + push-pattern for PC team; refines permission-allowlist at the discipline layer
- **PC-seam standing wave-close push pattern** (2026-06-08) — preserved unchanged
- **Hive-mind decision-routing** (Matt 2026-05-23) — preserved; broader allowlist for safe diagnostic operations does NOT erode "seam-owners decide in-scope" because write + scope-amendment operations remain narrow
- **PC team OPs** (each agent skill) — updated to reference new tmux-wrapped invocation post-install

No architectural-commitment changes. Infrastructure refinement only.

---

## 7. Sign-off

**Authored:** gandalf 2026-06-10 per Matt directive — "we dont need to solve for this session, but we do need to solve for the next session" (referring to PC infrastructure brittleness + permission-allowlist friction).

**Authority:** gandalf cross-cutting design-steward authority for cross-session continuity artifact + PC team infrastructure planning + composition with federated PC team architecture commit.

**Routing:** next setup-session gandalf reads at session-start; engages Matt for § 4.1 + § 4.2 step 1 to fire the WSL install at convenient window. Setup session is a focused 1-2 hour engagement separate from design-trajectory work.

**Empirical-evidence triggers for setup session firing:**
- Matt schedules focused infrastructure-setup session window
- Next autonomous PC hive-mind cycle is anticipated (e.g., WS2 commission execution needs PC team autonomy)
- PC team operational ceiling becomes pressing for ongoing work

**Composition with prior canonical commitments:** all preserved (federated PC team architecture 2026-06-07 + CLAUDE.md commit/push addendum 2026-05-25 + hive-mind decision-routing 2026-05-23 + PC-seam standing wave-close push pattern 2026-06-08).

**End of PC infrastructure setup plan.**
