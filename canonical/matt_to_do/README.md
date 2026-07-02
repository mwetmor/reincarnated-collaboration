# Matt — To-Do (the human-action queue)

**STATUS:** LIVING QUEUE — born 2026-07-02 (Matt: *"Maybe we should make another folder called matt-to-do, where we can park the claude remote control work for now?"*).
**Maintained by:** gandalf + knight-rider (any agent may park a row). **Executed by:** Matt.

---

## What this is (and is NOT)

The **action queue** — things only **Matt can physically DO**: host-level runs, account/credential actions, purchases, anything requiring a live human terminal or externally-authenticated context. Glance here at session start/end, same cadence as the decision queue.

The three-surface contract:

- **`matt_decision_needed/`** = what Matt must **RULE** (judgment; work blocked on a decision).
- **THIS queue** = what Matt must **DO** (hands; work blocked on a human-performed action).
- **`current-to-end-state/` trackers** = what the **WORK owes the spec** (agent-executable deltas).

A row belongs here ONLY if no agent can perform it (environment / credential / hardware constraint). If an agent could do it with authorization, it goes to a tracker or a dispatch instead — never here.

**How it flows:** any agent parks a row (the action + why only Matt + what it unblocks). Matt performs it → the row is **struck with date** and swept to DONE (never silently deleted). Same sync discipline as the decision queue: when the unblock-target resolves some other way, the row is re-synced or struck in the same unit of work.

---

## THE QUEUE (open — waiting on Matt's hands)

| # | Action | What it unblocks | Source / context | Parked |
|---|---|---|---|---|
| **T1** | **Run Claude Code Remote Control on the Mac** — in a spare terminal (kept alive; the Mac Mini's no-sleep config supports it): `cd ~/Games/reincarnated-collaboration && claude remote-control --name "Mac RC"` | Registers a CCR **environment** → unblocks `canonical-hygiene-audit-routine.md` instantiation (the standing weekly canon-hygiene audit — SPEC-READY since 2026-06-30, blocked *only* on environment availability). Once the environment exists, one `create_trigger` call from any session with CCR context stands the routine up; the reorg's tripwires (dead-home regression, OP↔skill twin drift) ride the same routine. | `CLAUDE.md` § Remote Control; `agentic_orchestration/operating-procedures/canonical-hygiene-audit-routine.md` | 2026-07-02 |
| **T2** | **Provide GTX-1650/RTX-3050-class min-spec hardware** — a cheap GTX-1650 or RTX-3050 Windows box, OR a Steam Deck (Linux/Vulkan, close to the floor). Needed to run the exported demo build's worst-case scene (max horde + max VFX + a boss) and certify 60 FPS @ 1080p on the actual floor. | Unblocks the **ABSOLUTE min-spec certification gate** (D10 Gate B). The dev machine is Apple-M2/Metal — a *flattering* machine (perf-target-specs.md §7: "a dev machine running smoothly does NOT certify minimum-spec"). drax stood up the **proxy regression gate** (D10 Gate A, `reincarnated-godot/MINSPEC_CADENCE.md` + `scripts/run_minspec.sh`) which catches sim-loop regressions on the Mac NOW, but the absolute frame-floor (render/shadow/VFX cost, the Metal-flattered part) can only be certified on real Vulkan hardware. This gate must run before the demo goes to Next Fest. | `reincarnated-godot/MINSPEC_CADENCE.md` §2 Gate B; `canonical/reap-die-rise-engine/performance-target-specs.md` §4/§7; D10 dispatch | 2026-07-02 |

---

## DONE (struck, with date)

*(none yet — born 2026-07-02)*

---

**Signed:** gandalf, 2026-07-02. The decision queue holds what waits on your judgment; this one holds what waits on your hands.
