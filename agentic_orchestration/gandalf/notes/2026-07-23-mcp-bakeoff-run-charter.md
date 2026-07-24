# MCP-BAKEOFF run charter (RATIFIED at birth — Matt 2026-07-23: "charter the bake-off now — $15 approved")

**Date:** 2026-07-23 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executes:** drax (all probes, his seam)
**Pattern:** desirable-run (`operating-procedures/desirable-run-pattern.md`) — fit test §2
**Sequencing:** fires AFTER GLANCE-RESTORE lane-A G4 (drax is one seam; serial). Pro column additionally gated on zip delivery (matt_to_do **T5**).

---

## §0 Intent (one sentence)

Choose the project's Godot MCP stack — the conductor-eye verification + capture + judge-channel + structure-first instrument — by a pre-registered head-to-head on the SAME scene: **incumbent** `satelliteoflove/godot-mcp` (wired, KIT-FIDELITY-proven, $0) vs **Godot MCP Pro** v1.x (youichi-uda; 162 tools; $15 paid zip; standard-build) vs **IvanMurzak/Godot-MCP** (39 tools/11 families; free, Apache-2.0; **requires Mono/C# editor**, .NET 8 SDK). Verdict = capability matrix, not vibes.

**Rubric-law note:** the owner's question is "which instrument serves our proven needs" — decidable as PASS/FAIL cells against pre-registered criteria drawn from ACTUAL project needs (KFL-20 capture fork, KT-5 conductor-eye pattern, galadriel judge channel, structure-first GridMap law). Product PICK is a commitment boundary — Matt ratifies at end.

## §1 Substrate (bounded, frozen at launch)

| Item | Role |
|---|---|
| 3 product stacks (versions PINNED at install: incumbent addon 4.1.0 wired; Pro = zip version on delivery; IvanMurzak = repo tag + Godot.NET editor version) | the compared domain |
| `reincarnated-godot` KT3 arena scene + `CaptureRig.tscn`/`capture_rig.gd` + d2-skeleton asset | the common test scene |
| KIT-FIDELITY-proven command surface (launch, tree, screenshots, run/stop, runtime state, freeze/step) + wire recipe `/tmp/mcp_call.mjs` | the incumbent baseline truth |

## §2 Fit test

- **F1:** YES — 3 products × 6 probes = 18 cells, enumerable at launch.
- **F2:** YES — every cell PASS/FAIL/BLOCKED-ENV vs pre-registered criterion; exit = cells filled + verdict rec authored.
- **F3:** YES — forks pre-drained: purchase **APPROVED** ($15, T5); Mono = **side-by-side editor binary + throwaway branch only** (the csproj/NuGet touch never lands on main in-run); product pick reserved to Matt (declared boundary).
- **F4:** YES — instrument selection for conductor-eye verification is conductor authority; drax owns the executing seam.

→ gandalf conducts; drax executes; KR not engaged (single-seam).

## §3 Probes (pre-registered PASS criteria — same scene for every product)

| # | Probe | PASS criterion |
|---|---|---|
| **P1** | Isolated-node/asset capture (the KFL-20 fork motivator) | Agent-driven capture of d2-skeleton ISOLATED from scene → image exists, subject-only framing. **P1-alt** (scored separately): the CaptureRig path works on this stack. Incumbent expected P1-FAIL/P1-alt-PASS (KFL-20 evidence); Pro expected viewport-only; IvanMurzak is the native-P1 candidate. |
| **P2** | Screenshot comparison (galadriel judge channel) | Produce a diff/similarity artifact between two captures → artifact + score emitted, agent-readable. Artifacts parked for galadriel verdict-stage judge-note. |
| **P3** | GridMap (structure-first law) | Batch `set_cell_item` ≥50 cells on KT3 grid + read-back match. Note editor-time vs runtime-time. |
| **P4** | Freeze/step + runtime-state read (KT-5 conductor-eye pattern) | Freeze at tick, step N, read node transforms → returned values match scene truth. |
| **P5** | Editor-script escape hatch | Execute arbitrary GDScript in editor: create node, set property, verify via independent tree read. |
| **P6** | Wire stability | The proven command surface exercised ×3 cycles, no server restart/hang; latency class noted (sub-second / seconds / worse). |

**Evidence per cell:** command transcript + artifact path. No cell fills without both.

## §4 Column order + gates

1. **Incumbent column** first (baseline; fast — wire already proven).
2. **IvanMurzak column:** download Godot 4.x **.NET** editor binary side-by-side (free; never replaces the project-default editor); throwaway branch carries the csproj + two NuGet refs (`ReflectorNet`, `McpPlugin`); addon from GitHub/AssetLib (asset 5245). Branch is DELETED post-run regardless of verdict.
3. **Pro column:** gated on T5 zip delivery (park OUTSIDE repos — proprietary, never committed). If undelivered when columns 1–2 finish, run pauses **OPEN** (parked, not failed).

**Honorable fallbacks:** Mono editor install failure on this host → column marked **BLOCKED-ENV** with evidence; matrix proceeds 2×6 and says so out loud. Any probe crashing a stack → cell FAIL with transcript, run continues.

**Exit predicate:** all reachable cells filled + conductor verdict recommendation authored (with galadriel P2 judge-note as input) + **Matt ratifies the pick** (commitment boundary). Fallback verdict shape if no clear winner: keep incumbent + name the single capability worth a second stack.

## §5 Matt interface

- **Pre-run (hands):** T5 — buy Pro at itch.io, park zip outside repos, tell drax where.
- **In-run:** red-flag pings only; rulings ledger MBL-1..n, veto-open.
- **At end:** matrix + verdict rec → Matt picks. No purchase beyond the approved $15; no build-posture change to `reincarnated-godot` main without the ratified pick.

---

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
