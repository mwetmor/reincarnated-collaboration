# UE Seam Agent Placement Decision — Option B (PC-Resident, SSH-Invoked from Mac)

> **STATUS:** CURRENT (load-bearing as of 2026-05-31) — Architectural decision record. Locks the UE-seam agent's host residence + invocation pattern. Composes with the three-layer architecture (GitHub + Samba + SSH) commitment authored 2026-05-30 + headless-SSH-Unreal capability proven 2026-05-31. The UE-seam agent's full role-definition + operating-procedure remain unwritten; gandalf authors when `reincarnated-unreal` becomes load-bearing (manifestation milestone scope).

**Date:** 2026-05-31
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-31 verbatim recognition: "Can I not invoke the UE agent on the PC while I am SSH'd in from my mac? I thought this would be possible as well." → triggered upgrade of placement decision from Option B (PC-physical-presence required) to Option B + SSH-invoked variant (PC-resident agent controllable from Mac terminal).

**Companion artifacts:**
- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — three-machine architecture commitment (CURRENT)
- `matt_notes_handoff_docs/reincarnated-headless-ssh-handoff.md` § "UPDATE 2026-05-31 — Mac-side execution findings" — proves the SSH→Unreal capability that enables this placement
- `agentic_orchestration/AGENTS.md` — current 8-agent team topology (UE seam not yet enumerated)
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture-placeholder.md` — pattern library architecture that the UE seam agent's playtest work will support

---

## 0. TL;DR

**Decision:** the UE-seam agent's host residence is **the PC** (Windows 11, MSI MAG Codex R2). Native to PC filesystem. Native to UE tool invocation. Default invocation pattern is **SSH-from-Mac**: Matt stays at Mac physically, SSH's into PC, runs `claude` on PC's shell, the agent session is PC-native but controlled via Mac terminal.

**Rationale:**
- Pattern symmetry with existing 8-agent team (each agent lives local to their seam's host machine)
- UE work is filesystem-heavy in ways that wrap-everything-through-SSH would severely friction (binary `.uasset` edits; Blueprint graphs; level editing; cook/build/package operations)
- Mac→PC SSH layer exists for cross-seam observability (Mac-resident agents reach into PC for verification queries); does NOT exist as the UE agent's primary workspace

**The hybrid pattern this enables:**
```
PC: claude session running, PC-filesystem-native, invoked either:
    ├── via Matt physical presence at PC, OR  ← available when at PC
    └── via Matt SSH'd from Mac terminal       ← preferred default
```

**What this does NOT yet provide:**
- A written UE-seam-agent role definition (gandalf authors when manifestation milestone scope activates)
- An operating procedure for the UE seam (composes off existing agent OPs at that time)
- The PC-side environment setup (Claude Code CLI install + reincarnated-collaboration clone + reincarnated-unreal repo location — operational tasks queued for first-invocation session)

---

## 1. Decision in three parts

### 1.1 Host residence: PC

**The UE-seam agent lives on the PC.** Native PC filesystem access; native invocation of `UnrealEditor-Cmd.exe`; native Visual Studio C++ tooling; native cook + build + package pipelines.

**Pattern symmetry with existing team** (per `agentic_orchestration/AGENTS.md`):

| Agent | Seam | Host residence | Primary work surface |
|---|---|---|---|
| gamora | engine simulation | Mac | `~/Games/reincarnated-engine/src/reincarnated/simulation/` (Mac-native) |
| rocket | engine generation | Mac | `~/Games/reincarnated-engine/src/reincarnated/generation/` (Mac-native) |
| star-lord | engine pipeline | Mac | `~/Games/reincarnated-engine/src/reincarnated/{export,output,telemetry,llm}/` (Mac-native) |
| drax | player surfaces | Mac | `~/Games/reincarnated-demo/`, `~/Games/reincarnated-loadout/` (Mac-native) |
| elrond | catalogue / research | Mac | `agentic_orchestration/research/...` + `~/Games/reincarnated-engine/.../substrate/` (Mac-native) |
| legolas | research scout | Mac | Read-only across all sources (Mac-native invocation) |
| jack-ryan | QA / disciplines | Mac | `canonical/` + `decisions-log` + `engineering-disciplines` (Mac-native) |
| gandalf | story / design | Mac | `canonical/story/` + `agentic_orchestration/gandalf/` (Mac-native) |
| knight-rider | orchestrator | Mac | dispatches + hive-mind state (Mac-native) |
| **UE-seam agent (this decision)** | **reincarnated-unreal** | **PC** | **`C:\dev\reincarnated-unreal\` (PC-native)** |

Each agent works locally in its seam's native host environment. The UE seam follows the same pattern because UE work happens on PC.

### 1.2 Invocation pattern: SSH from Mac (default)

**Matt's preferred invocation:** stay physically at Mac, SSH into PC from a Mac terminal tab, run `claude` on PC's shell. The Claude Code session is PC-resident — has full PC filesystem access, runs UE tools natively, lives in PC's `~/Games/reincarnated-collaboration/` clone for canonical docs and PC's `~/Games/reincarnated-unreal/` (or `C:\dev\reincarnated-unreal\`) for seam work. **Only the terminal interaction layer is SSH-transited.**

This is structurally different from Option A (Mac-resident agent that SSH-wraps every command). Option A wraps every operation through SSH; Option B SSH-from-Mac places the agent's *entire process* on PC and the user-facing terminal back-channel through SSH. The agent is PC-native; the keyboard is Mac-mediated.

**Alternative invocation:** Matt physical presence at PC. Run `claude` directly in a PC terminal. Same PC-resident agent; different keyboard mediation. Both produce identical agent capabilities; choice is purely operational (where Matt is sitting).

### 1.3 Cross-seam reach via SSH from Mac

**Mac-resident agents reach into PC via SSH** for cross-seam verification queries:
- gamora verifies "did the JSON I produced cook into the right `.uasset`?"
- star-lord tails Unreal cook logs while debugging telemetry export
- gandalf checks "did the manifestation milestone character actually load + play correctly?"
- knight-rider dispatches an instruction to the UE seam (cross-host dispatch)

These are reach-in queries from Mac-resident agents using the SSH layer **as a tool**. They are NOT the UE agent's primary workspace; they're how other agents observe and coordinate with it.

---

## 2. Why this pattern

### 2.1 Why NOT Option A (Mac-resident agent that SSH-wraps every command)

| Cost | Why it hurts |
|---|---|
| Every file op wrapped in `ssh user@host "cmd"` | Cumulative friction; latency on every Read/Edit/Write/Bash invocation |
| Cannot use Claude Code's native `Read`/`Edit`/`Write` on PC files | `.uasset` binaries, Blueprint graphs, level files all need transit through SSH `type` (cmd.exe) or `scp` |
| UE Editor interactive sessions impossible | Some UE operations genuinely need interactive UI; Mac-driven SSH can't support |
| Heavy ops (cook / build / package) through SSH adds friction | Throughput-sensitive operations want native invocation |
| Cross-seam observability mode is the *wrong* primary mode | SSH is designed for observability + occasional reach-in; making it the *primary work surface* mis-uses the tool |

### 2.2 Why Option B (PC-resident, with SSH-from-Mac as invocation variant)

| Benefit | Why it matters |
|---|---|
| Native filesystem access to `reincarnated-unreal/` | Standard Claude Code workflow with `Read`/`Edit`/`Write`/`Bash` directly on UE files |
| Standard UE tool invocation | `UnrealEditor.exe` / `UnrealEditor-Cmd.exe` / `UnrealBuildTool.exe` all run native; no SSH overhead per command |
| UE Editor interactive sessions possible | Agent can run interactive UE when needed (e.g., visual verification of manifestation milestone scene composition) |
| Cooks / builds / packages run at native speed | The 14700F + RTX 4060 Ti + NVMe runs UE5 at full hardware tier; no SSH bottleneck |
| Pattern symmetry with existing team | Same architectural mental model for Matt + for cross-seam coordination |
| Cross-seam reach still works | Mac-resident agents SSH-into-PC for queries; the SSH layer is preserved as observability tool, used appropriately |

### 2.3 Why specifically the SSH-from-Mac variant matters

Without the SSH-from-Mac variant, Option B requires Matt to **physically be at the PC** to invoke the UE-seam agent. That's a real operational cost:
- Matt's design / engine / coordination work happens at Mac
- Matt's UE work happens at PC
- Switching physical sittings adds friction
- Some UE-seam work could happen during design/engine sessions if invocation were Mac-mediated

The SSH-from-Mac variant **removes the physical-presence requirement** without sacrificing PC-native agent capability. Matt stays at Mac; the agent runs on PC; only the keyboard is remote. **This is the best of both architectural worlds.**

This is enabled by the headless-SSH-Unreal capability proven 2026-05-31 (per companion doc UPDATE section). Without that capability, SSH-from-Mac would be theoretical; with it proven, the variant is operationally real.

---

## 3. What this enables

| Capability | How |
|---|---|
| **UE seam work without physical PC presence** | SSH from Mac terminal → `claude` on PC → agent session runs on PC, native filesystem + native UE tools, controlled from Mac terminal tab |
| **Manifestation milestone scope work** | UE seam agent prototypes the Spirit-form sculpting + manifestation transition + level-50 future-glimpse in `reincarnated-unreal` project; gandalf reviews + iterates via SSH-from-Mac sessions |
| **Pattern library Stage 3 (manifestation in Unreal)** | UE seam agent assembles characters from modular component library per JSON specs from engine; manifestation runs at PC's native UE speed |
| **Pattern library Stage 4 (playtest)** | UE seam agent prepares playtest scenes; Matt + son run actual playtest at PC; agent supports observation + data capture |
| **Cross-seam verification by other agents** | gamora SSH's into PC to verify JSON-to-uasset import correctness; star-lord verifies telemetry export from cooked builds; gandalf reviews scene composition |
| **Automated cook / build / package via Mac-driven SSH** | One-shot SSH commands fire UE cooks remotely (per handoff doc); cooked output flows back via shared filesystem or git |
| **Knight-rider dispatches to UE seam** | Dispatches route via the same hive-mind state model; UE agent picks up on next session invocation (PC physical OR SSH-from-Mac) |

---

## 4. What this does NOT yet enable

| Not yet enabled | Why | When does it land |
|---|---|---|
| **UE seam agent role definition (formal)** | Gandalf authors role-def stubs when seams become load-bearing; `reincarnated-unreal` becomes load-bearing at manifestation milestone scope | Authored when manifestation milestone work begins |
| **UE seam agent operating procedure** | Composes off existing OPs (gamora / rocket pattern adapted for PC seam); authored alongside role-def | Same gate |
| **PC-side Claude Code CLI install verification** | Used during PC setup work, but persistent install for SSH-from-Mac invocation needs confirmation | First UE-seam invocation; quick verify-or-install step |
| **PC clone of reincarnated-collaboration repo** | Canonical docs need to be on PC for UE agent to read; clone is one-time operational setup | First UE-seam invocation; `git clone` step |
| **Reincarnated-unreal as a load-bearing repo** | Currently the blank UE 5.5 project at `C:\dev\reincarnated-unreal\Reincarnated\` is scaffolding; not yet a seam with substantive work | Manifestation milestone scope activates this |
| **UE seam GitHub repo** | When `reincarnated-unreal` becomes load-bearing, it gets its own GitHub repo (separate from reincarnated-collaboration meta-repo) | Same gate; coincides with role-def authoring |
| **CODEOWNERS + branch protection for cross-host commits** | Required for multi-host commit discipline when PC starts committing to repos; queued per 2026-05-31 git discipline conversation | Same gate; jack-ryan canonical write at that point |

These are operational gates, not architectural unknowns. The placement decision (Option B + SSH-from-Mac) is the architectural commitment; the operational setup work compresses into a single session when the manifestation milestone gates the UE seam going load-bearing.

---

## 5. Sequencing — when the UE seam goes live

```
Current state (2026-05-31):
    ├── PC infrastructure scaffolded ✅
    ├── Headless-SSH-Unreal capability proven ✅
    ├── Blank UE project at C:\dev\reincarnated-unreal\Reincarnated\ ✅
    └── UE seam agent placement decision committed ✅ (this doc)
                              ↓
Cycle 14 wave-5 close
                              ↓
WS1A architectural foundations land
                              ↓
Manifestation milestone scope activates UE seam
    │
    ├── Gandalf authors UE-seam-agent role definition stub
    ├── Gandalf authors UE-seam-agent operating procedure (composed off gamora/rocket pattern)
    ├── First UE-seam invocation session (PC physical OR SSH-from-Mac):
    │   ├── Verify Claude Code CLI install on PC; install if needed
    │   ├── Clone reincarnated-collaboration repo on PC for canonical access
    │   ├── Initialize reincarnated-unreal as separate GitHub repo
    │   └── Agent picks up first manifestation milestone tasks
    ├── Knight-rider routes UE-seam dispatches via hive-mind state
    └── Cross-seam reach pattern operational (Mac-resident agents SSH-into-PC for verification queries)
                              ↓
Manifestation milestone landed
                              ↓
Pattern library Phase A-E work (UE seam supports playtest infrastructure per § 6 of pattern library placeholder)
```

---

## 6. Cross-references

### 6.1 Composes with

- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — three-machine architecture (Mac + Pi + PC); this doc places the UE agent within that architecture
- `matt_notes_handoff_docs/reincarnated-headless-ssh-handoff.md` — proves the SSH→Unreal capability that operationalizes the SSH-from-Mac invocation variant
- `agentic_orchestration/AGENTS.md` — current team topology; this doc adds (implicitly) a 9th seam (UE) at PC residence; formal team-topology update is a future amendment
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture-placeholder.md` — pattern library architecture; UE seam supports Stages 3 (manifestation) and 4 (playtest)
- The forthcoming **manifestation milestone Recognition Record** (authored when next prioritized) — manifestation milestone is the gate for activating the UE seam as load-bearing

### 6.2 Refines

- The three-layer architecture work (`canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md`) by specifying that **SSH from Mac → PC is BOTH** (a) the cross-seam observability layer for Mac-resident agents AND (b) the invocation layer for the PC-resident UE seam agent. The SSH layer serves two distinct purposes; they compose cleanly because the Mac-resident agents reach in for queries while the UE agent's session is PC-native throughout.

### 6.3 Anticipates

- **UE-seam-agent role definition** at `.claude/agents/<ue-seam-name>.md` (name TBD; suggestions include `groot` continuing the team naming pattern, or a UE-thematic name)
- **UE-seam-agent operating procedure** at `.claude/skills/reincarnated-<ue-seam-name>-operating-procedure/SKILL.md`
- **Multi-host commit discipline** canonical (jack-ryan; CODEOWNERS + branch protection + rebase-on-pull) — fires when PC starts committing to repos
- **Reincarnated-unreal GitHub repo** creation as separate canonical-versioned repo (separate from meta-repo per gandalf 2026-05-31 git-discipline conversation)
- **AGENTS.md amendment** adding the UE seam to the formal team topology

### 6.4 Does NOT replace or amend

- Existing 8-agent team residence (all Mac-resident; unchanged)
- Existing Pi-middleware role (continues to host Samba share + future Postgres + future LLM proxy)
- Mac as the canonical-docs source-of-truth (PC reads canonical via cloned repo; doesn't author canonical except for UE-seam-specific canonical commitments)
- Existing dispatch routing through knight-rider

---

## 7. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-31 verbatim recognition that SSH-from-Mac invocation of PC-resident Claude IS available and likely preferable to physical-PC-presence requirement

**For:** the durable canonical record of the UE-seam-agent placement decision (Option B, PC-resident, SSH-from-Mac as default invocation variant) that:
1. Locks the architectural placement (PC-resident, not Mac-resident)
2. Locks the invocation pattern (SSH-from-Mac as default; PC physical presence as alternative; both produce identical agent capability)
3. Preserves the SSH layer for cross-seam observability (Mac-resident agents reach into PC for queries)
4. Defers the operational setup (Claude CLI install + repo clones + role-def authoring + OP composition) to the manifestation milestone scope when the UE seam becomes load-bearing
5. Composes cleanly with the three-layer architecture (GitHub + Samba + SSH) and the pattern library architecture (placeholder) authored 2026-05-31

**Empirical foundation:** headless-SSH-Unreal capability proven 2026-05-31 (per `matt_notes_handoff_docs/reincarnated-headless-ssh-handoff.md` UPDATE section). Without that capability, this placement decision would be theoretical; with it proven, the decision is operationally real.

**Composition target:** foundational placement decision for the UE seam agent's eventual role-definition + operating procedure + repo organization; foundation for the manifestation milestone's UE-side work; reference architecture for any future cross-machine seam placements.
