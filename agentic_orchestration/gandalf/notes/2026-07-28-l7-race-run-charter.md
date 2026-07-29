# L7 VFX RACE — RUN CHARTER (LR)

> **STATUS:** LIVE — chartered 2026-07-28 on Matt's explicit go (*"Go on the NOW race"*).
> **Conductor:** gandalf (`RUN-CONDUCTOR`). **Pattern:** desirable-run (`operating-procedures/desirable-run-pattern.md`); fit test §0.1 below.
> **Lineage:** design source = TCP wind-down handoff §2 (`2026-07-26-tcp-wind-down-and-suite-architecture-handoff.md`, L7 bake-off table); calibration = PROVISION-CAL (`2026-07-28-provision-cal-run-charter.md` + PC-EXIT review). V-PREP is SUPERSEDED — PROVISION-CAL discharged every V-PREP item (menu verdicted, stage fixed + lit + ruled B-cold, camera locked, caster body ready, probes ①②③ answered).
> **L7-V rulings R-1..R-14 stand. TCP laws inherited by number** (L-B, L-G, L-H, L-J, L-K, L-N, TCP-32, TCP-50, TCP-51). **M-EYE standing (program-wide): VFX eye-checkpoints deliver MOTION, never stills.**

---

## §0 — Rubric law

The race answers **WHICH ARM PRODUCES THE BETTER JUDGED VFX UNDER IDENTICAL CONTRACTS** — and, as first-class telemetry, **what each arm's iteration loop actually costs** (TCP-32 clocks). Contracts state what must be TRUE, never how (L-K). No arm gets mid-race uplift (L-J post-freeze law: new tool versions are findings for the next lap). Where the instrument is missing, record the gap — never invent a negative (L-N).

### §0.1 — Fit test

- **F1 Enumerable:** 3 arms × 3 briefs = 9 cells + 1 verdict assembly. Countable, listable, frozen. ✓
- **F2 Decidable:** each cell's done-predicate = MP4 delivered at the locked camera + contract-TRUE self-check + clocks logged. The RACE verdict is Matt's eye (blind strips) — a **declared Matt commitment-boundary**, pre-named, not a decidability leak. ✓
- **F3 Pre-drained:** forks drained across TCP (R-1..R-14), PROVISION-CAL (R-PC-1..11), and this charter's §6 rulings. Residuals are reasoning-boundaries. ✓
- **F4 Authority-resident:** conductor rules stage/sequencing/measurement questions; taste and winner belong to Matt's eye. ✓

## §1 — Frozen substrate (the L-J re-freeze record — PC-EXIT §7, executed here)

| Arm | Frozen as |
|---|---|
| **H** (harness) | drax hand-authoring directly in `reincarnated-godot` at current sha; full instrument corpus (F8/F9, LSTAT-2, framediff, TCP meters) — available to ALL arms per L-H |
| **W-PRO** | as-installed; `apply_particle_preset` REACHES; presets **Matt-verdicted judgeable ×3** (PC check 4: *"fire is fire without the label"*) — races on a live surface. TCP-50: `create_particles`-family calls only |
| **W-MUR** | core **v0.20.1** + server **9.2.4** + all ten extensions; LOCAL-ONLY env (four vars, R-PC-6); consumer pins ReflectorNet 5.4.0 / McpPlugin 7.5.2. Fielded on PC check 3's ★YES (`node-modify` ResourceRef reaches `ParticleProcessMaterial`, disk-confirmed) |

**Shared stage (identical for all arms, frozen before cell 1):**
- **Crypt:** `kit_replica_level.gd` at B-cold (godot `8caa733`, verified 6.833×; R-PC-3 + B-cold lock *"I agree, continue"*).
- **Camera = the judge:** R-6 locked — dist 34, fov 24, yaw 47, pitch −50. No arm touches it.
- **Determinism regime:** SDFGI OFF / glow ON (standing correction: settle-count variance is the discriminating instrument, not byte-identity).
- **Caster body:** werewolf (R-PC-4) — SK rig THE body (R-PC-8), albedo repaired LOADS-CLEAN (R-PC-7), RETARGET-READY at 0.0000° mean/max rest-Δ.
- **Corner-torch dressing (Matt: the two lit corners "need a fire VFX or a torch"):** authored ONCE by the stage before the race, shared by all arms, **never judged** — it motivates the B-cold light, it does not compete.
- **`draw_pass_1` mesh is STAGE-SUPPLIED** to all arms (PC-EXIT §4.3: neither MCP wire sets it — symmetric ceiling honored symmetrically).
- **Off the board:** 2D-only rows (R-PC-9); GATED-Q46 none; editor tooling open to every arm (L-H, all-arms-or-none).

## §2 — Target-state

- **T-1:** 9 cell deliverables — per arm × per brief, one MP4 at the locked camera (M-EYE: motion) + TCP-32 clock log + iteration count + declared-surfaces list.
- **T-2:** 3 blind verdict strips (one per brief, arms labelled A/B/C, identity sealed) assembled by the conductor and put to Matt's eye.
- **T-3:** Iteration-loop telemetry answering the registered suspicion: *the discriminator is the iteration loop* — H reads its own file; W-MUR can't read back what it made; Pro round-trips screenshots. Refutable; the clocks decide.
- **T-4:** Race verdict record (Matt's eye + revealed attribution) filed → feeds **T7-FORGE** (Wave ζ, soft — not chartered here).

## §3 — The three briefs (verbatim contract, L-K: TRUE never how)

1. **CAST** — flash at `prop_r` → travel → impact; full event lifecycle readable at the locked camera.
2. **AURA** — persistent loop on the character; **survives motion**; must not eat the silhouette at 12.5% frame height.
3. **AMBIENT** — room-owned; ground-plane rule R-10 binding; area×layers budget (TCP-51: **area is the entire cost**).

**Per-cell discipline:** TCP-32 clocks · declared surfaces · W-PRO vs W×H strictly split (TCP-50: `create_particles`-family = W-PRO; `execute_editor_script` = W×H — an arm crossing the split forfeits the cell, it does not blend).

## §4 — Order and cadence

**V-H → V-PRO → V-MUR → verdict** (Matt-ordered; sequential under L-J — one wire live at a time). Each V-cell runs all three briefs before the next arm mounts. Blind strips assemble only after all three arms return (R-LR-1 below).

## §5 — Hazards inherited (pre-registered, not discoveries)

- `resource-modify` is **all-or-nothing on disk + silent-flush dirty state** (PC check 3 rider) — W-MUR cells snapshot before write.
- Skinned-mesh-not-root transform-class warning on emitted `.glb`s — L6's problem, NOT this run's; any bleed-in is a finding routed to L6-EMIT-PROBE, not chased here.
- White-on-transparent instrument lesson (L-N): every eye-artifact dark-composited/rendered before judgment is requested.
- `.claude/skills` self-write telemetry (105 files, unasked) — watch for recurrence under Pro cells; log, don't block.

## §6 — Rulings ledger (veto-open unless Matt-signed)

- **R-LR-1 (conductor):** blind strips assemble at END of all three V-cells, one strip per brief — per-arm interim eye-returns would unblind attribution. Matt's declared interface: three strips + reveal, red-flag pings only mid-run.
- **R-LR-2 (conductor):** corner-torch dressing is authored by the H cell as its first act (stage work, pre-race, not judged, then FROZEN into the shared stage) — someone must hold the brush, and the stage's keeper (drax) holds it before any arm races.
- **R-LR-3 (conductor):** AURA's "survives motion" is tested on the werewolf's retargeted walk (the 0.0000° map) — same clip, all arms.

## §7 — Matt interface

- Pre-declared: **three blind MP4 strips at verdict** (M-EYE), then attribution reveal — attribution is part of the verdict (fixes L8's "which tool built this?" gap permanently).
- Mid-run: red-flag pings only. All rulings veto-open.
- Honorable fallback: an arm that cannot satisfy a brief delivers its best state + a named ceiling (L-G: ceilings are PASSes) — no cell is a mystery, no strip slot goes empty silently (a ceiling card takes the slot).

## §8 — Cell log (live)

| Cell | State |
|---|---|
| V-H (drax) | **RELAUNCHED 2026-07-28** — first instance died on stream timeout (same class as PC's W1-B) AFTER landing Task-0 work uncommitted (torch dressing +242 in `kit_replica_level.gd`, values-unchanged refactor; 5 stage draw-pass .tres in `vfx/stage/`; vh_* scripts) and BEFORE any capture. Resume brief: verify + commit inherited state, then the three briefs, with per-brief commits + incremental note (the relaunch cost = exactly the un-committed span; incremental-write discipline named in-brief) |
| V-PRO | queued |
| V-MUR | queued |
| Verdict assembly | queued |

**Parallel non-race cells in flight (separate substrate, no contention):** galadriel holy-glyph candidates (L8) · drax L6-EMIT-PROBE (confined to `mcp-lab/l6probe/`).

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.
