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
- **R-LR-4 (Matt-directed 2026-07-28, mid-run eye on V-H ambient): CONTAINMENT is a binding AMBIENT contract clause** — *"we need to make sure the ambient particles don't pass through/out of the walls into the void."* Room-owned means room-CONTAINED: no particle visibly crosses the wall plane into the void at the locked camera. States TRUE not how (L-K — collision, emission-volume sizing, lifetime, or masking all legal). Applies symmetrically to all three arms; a leak at verdict time is a contract MISS, not a style note.
- **Matt mid-run eye (2026-07-28): corner torches "100% perfect"** — Task-0 stage dressing PASSED at the owner's eye; frozen as-is into the shared stage.
- **R-LR-5 (conductor, on V-H's measurement):** the AURA silhouette clause is **restated at 9.31%** — the werewolf's actual frame height at the locked R-6 camera (the 12.5% of record omitted the −50° pitch, cos 50° = 0.643; the clause as written was unreachable by the frozen substrate). Same number for all arms; no arm advantaged. Companion method note: "eaten fraction" alone can't tell lit-from-covered — the no-particles light-only control decomposes it (V-H: 98% of apparent silhouette loss was illumination; sprites *raised* edge retention).
- **R-LR-6 (conductor):** `void_leak.py` (V-H's instrument, fires both directions: 3,752 px pre-fix / 0 px shipped) is **THE R-LR-4 verdict instrument for all arms** — stage frame + pass frame, 0 leak px is the bar. Portable, identical, symmetric.
- **Next-lap finding (post-freeze law, not applied mid-race):** TCP-51's *ordering* holds but its *exclusivity* doesn't — at 4K, ×16 area = +0.241 ms vs ×16 count = +0.142 ms (~1.7×, count term ~1.4σ). "Area is the entire cost" should read "area is the larger driver." At 720p the whole pass hides under the 6.05 ms vsync floor.
- **Ceilings banked (L-G — PASSes):** 9.31% scale gap · macOS/Metal windowed vsync survives `VSYNC_DISABLED` · `viewport_get_measured_render_time_gpu` returns 0.0 on Metal 4.6.3.

## §7 — Matt interface

- Pre-declared: **three blind MP4 strips at verdict** (M-EYE), then attribution reveal — attribution is part of the verdict (fixes L8's "which tool built this?" gap permanently).
- Mid-run: red-flag pings only. All rulings veto-open.
- Honorable fallback: an arm that cannot satisfy a brief delivers its best state + a named ceiling (L-G: ceilings are PASSes) — no cell is a mystery, no strip slot goes empty silently (a ceiling card takes the slot).

## §8 — Cell log (live)

| Cell | State |
|---|---|
| V-H (drax) | **RELAUNCHED 2026-07-28** — first instance died on stream timeout (same class as PC's W1-B) AFTER landing Task-0 work uncommitted (torch dressing +242 in `kit_replica_level.gd`, values-unchanged refactor; 5 stage draw-pass .tres in `vfx/stage/`; vh_* scripts) and BEFORE any capture. Resume brief: verify + commit inherited state, then the three briefs, with per-brief commits + incremental note (the relaunch cost = exactly the un-committed span; incremental-write discipline named in-brief) |
| V-PRO | **LAUNCHED 2026-07-28** — W-PRO arm on the frozen post-torch stage; R-LR-4 containment binding with `void_leak.py` as verdict instrument; AURA clause at 9.31% (R-LR-5) |
| V-MUR | queued |
| Verdict assembly | queued |

**Parallel non-race cells in flight (separate substrate, no contention):** galadriel holy-glyph candidates (L8) · drax L6-EMIT-PROBE (confined to `mcp-lab/l6probe/`).

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.

## §9 — V-PRO close + drift rulings (2026-07-28)

- **V-PRO ✓ COMPLETE** (note: `drax/notes/2026-07-28-l7-race-vpro.md`; 3 MP4s in `tmp/l7race/VPRO/`). Arm discipline held falsifiably: 357 MCP calls all ledgered (`wire/*.jsonl`), forbidden-tool census clean, `update_property` self-restricted to `position`. Contract reads: CAST 4 beat levels / impact 0.600 s · AURA eaten 12.04% (interior 6.38%, rim-dominant, edge retention 1.5752) · AMBIENT **0 leak px** (R-LR-6 instrument), analytic reach 7.790 m vs 8.30 m wall. Enabling discovery: `#RRGGBBAA` alpha ramps as the wire's only clock ("no timeline — lifetime is the clock, alpha ramp is the keyframe track").
- **T-3 suspicion REFUTED for this arm:** wire time 16.25 s of ~42 min (~0.6%); never round-tripped a screenshot. The Pro arm's real cost is the **create-time-only re-author tax** (`amount`/`lifetime`/`one_shot`/`explosiveness` settable only at create — every count change rebuilds the effect). Six ceilings as PASSes; load-bearing: **no light tool** (caster backlit into silhouette rather than lit — H's strongest technique structurally unreachable to Pro).
- **Hazard confirmed + contained:** the Pro addon REWROTE `project.godot` (3 autoloads added, `mesh_lod` threshold dropped) — caught, zero-pixel-tested, reverted. `.claude/skills` hazard: zero delta this cell.
- **R-LR-7 (conductor — stage-drift protocol):** V-H's datum no longer reproduces on today's stage (LSTAT-2 6.83→6.63, tails only, median unchanged; both arms' rigs byte-identical today `bf818b61`; four suspects excluded, cause honestly UNFOUND). Ruling: **strips must compare same-stage renders.** V-MUR renders on the current state recording LSTAT-2 pre/post as drift telemetry; then a V-H RE-CAPTURE cell (capture-only — authored effects untouched, ~32 s/clip) re-renders vh_*.mp4 on the then-current state immediately before strip assembly; if LSTAT moves again between V-MUR and re-capture, halt strips and diagnose. V-H's original MP4s retained as lineage.
- **R-LR-8 (conductor):** `project.godot` snapshot+diff is now a per-cell mandatory instrument (V-MUR inherits; any wire-side rewrite is caught-tested-reverted-logged, not silently shipped).

## §10 — V-MUR close (2026-07-29)

- **V-MUR ✓ COMPLETE** (note: `drax/notes/2026-07-28-l7-race-vmur.md`, 870 lines, written incrementally + committed per brief; 3 MP4s in `tmp/l7race/VMUR/` — LOCAL-ONLY, Synty-derivative IP). All three verified 1280×720 · 180 f · 6.000 s · 30 fps · no in-frame text.
- **R-LR-7 drift telemetry: ZERO.** PRE and POST stage datums byte-identical to each other AND to V-PRO's recorded frame (`bf818b61…c139d1c`, LSTAT-2 6.63 both ends). The 6.83→6.63 move is bracketed between V-H and V-PRO and has been stationary since. **V-H re-capture is CLEARED to fire.**
- **R-LR-4 / R-LR-6 discharged at 0 leak px** — instrument made to fire FIRST on this arm's own build (1,323 px) before clearing. Method note banked with the clause: at −50° pitch, crossing the wall plane and leaking visibly are different events; only an outward leak past the NEAR wall makes void pixels — two of three leak controls correctly returned 0.
- **Arm discipline held falsifiably:** 1,515 calls ledgered (tool + intent + timestamp + latency); TCP-50 census clean — `script-*` and `reflection-method-*` ZERO in every ledger; `project.godot` byte-identical to pre-cell snapshot (R-LR-8); `.claude/skills` zero delta.
- **Correction banked against PC-EXIT §4.3:** `draw_pass_1` is NOT a symmetric ceiling — true of the particle wires (`particles-create`, `create_particles`), FALSE of Murzak's `node-modify` (general property wire; sets no draw pass, no visibility AABB). The §1 remedy stands undisturbed (stage-supplied mesh, byte-identical, all arms — only the typist differs), but the race's true shape is **hand vs PARTICLE wire vs GENERAL-PROPERTY wire**; five of W-PRO's six ceilings are NOT inherited by W-MUR.
- **T-3 (registered suspicion) SPLITS:** REFUTED on latency — 29.24 s wire time across 1,515 calls vs ~2 h 15 m cell time (0.36%). **CONFIRMED on readback** — no tool returns the VALUE of a property the wire set (`node-find`/`scene-get-data` topology only, `resource-get-data` identity only, `screenshot-*` headless-fails); every verification was an independent disk read. The discriminator is not loop speed; it is the wire's inability to see what it wrote.
- **Next-lap findings (post-freeze law):** (a) `animation-add-track` accepts a `targetPath` resolving to NOTHING and reports `isError: false` — killed the CAST travel beat through two iterations while every call passed; caught by added-luma census (0.019 M = empty-stage torch floor), not by eye; confirmed by deliberate probe. (b) `Godot.StringName` unwritable across four encodings → `AnimationPlayer.autoplay` unreachable; answered by a disclosed press-play in the rig. Both are findings for the wire's next lap, not this race's problem.
- **Declared deviation (judgment call, named §0.3 of the cell note):** the wire ran on the PROVISION-CAL lab project (addon is C#; the frozen stage project is not), with md5-verified transfer in BOTH directions. Stage bytes governed; the lab was a typist's desk.
- **Next:** V-H RE-CAPTURE cell fires now (capture-only, authored effects untouched, originals kept as lineage); strips assemble AFTER re-capture, by the conductor's hands (R-LR-1), A/B/C seal held by the conductor.

## §11 — Re-capture close + blind strips assembled — RACE AT MATT'S EYE (2026-07-29)

- **V-H-RECAP ✓ COMPLETE, no anomalies** (note § appended to `drax/notes/2026-07-28-l7-race-vh.md`, `15152bec`). Drift pair PRE=POST=`bf818b61…c139d1c` (LSTAT-2 6.63, p05/p50/p95 identical) — **stage provably stationary across three consecutive cells; all nine strip inputs same-stage by construction.** R-LR-7 satisfied without the halt clause firing. Containment re-read on the new ambient render: **0 leak px** (VOID-1 unmodified). R-LR-8: `project.godot` NO DELTA; `git status` zero tracked deltas repo-wide — zero authoring confirmed rather than asserted. Originals in `tmp/l7race/VH/` untouched (hashes held). Supporting datum: ambient photometric lift invariant across the stage shift (+5.7% now vs +5.6% of record; p05 unmoved) — only the substrate moved, the briefs behave identically.
- **T-2 ✓ DELIVERED — three blind strips assembled by the conductor** (R-LR-1): `reincarnated-godot/tmp/l7race/STRIPS/strip_{cast,aura,ambient}.mp4`, each 3840×720 · 180 f · 30 fps, three panels labelled A/B/C via overlay. **Per-strip independent shuffle** (a label does NOT mean the same arm across strips — each brief is judged on its own). **Seal integrity: the key was generated and written without ever being displayed — the conductor is also blind.** Key at `STRIPS/SEALED_KEY.json`, read only AFTER Matt's per-strip calls are recorded. LOCAL-ONLY (Synty-derivative IP).
- **T-1 ✓** (nine deliverables + clocks + ledgers, per cell notes) · **T-3 ✓ answered with a split verdict** (§10) · **T-4 OPEN — the only remaining item**, and it is Matt's: watch three strips (M-EYE: motion), call each brief, then the reveal + verdict record closes the run.

### Matt — the verdict surface (when you're back)

Watch, in any order — each is 6 s, three panels side by side:
1. `tmp/l7race/STRIPS/strip_cast.mp4` — flash → travel → impact readable?
2. `tmp/l7race/STRIPS/strip_aura.mp4` — survives the walk, doesn't eat the silhouette?
3. `tmp/l7race/STRIPS/strip_ambient.mp4` — room-owned, contained (your R-LR-4)?

Per strip: which panel wins, which is unacceptable (if any), one line why. Then I unseal, reveal attribution, and file the verdict record → T7-FORGE.

## §12 — MATT'S VERDICT (recorded verbatim BEFORE unseal, per §11 seal discipline) (2026-07-29)

1. **CAST:** "C wins for charge-up and detonation burst, but I like the traveling of A. All readable, but the werewolf is facing backwards."
2. **AURA:** "A wins, but the floor portion of the aura doesn't follow the werewolf. I don't quite understand the question on the silhouette, but the werewolf is facing backwards and walking backwards."
3. **AMBIENT:** "A wins. Leak is gone, but I would still get rid of the remaining part of the particle aura around the four torches. What is remaining is something like a 30 degree cone of particles facing towards the center of the room in each picture. We dont need the cone I don't think."

**Cross-strip stage finding (Matt, twice):** the werewolf is FACING BACKWARDS (and in AURA, walking backwards) — a capture/retarget orientation defect, symmetric across arms (same clip, all arms, R-LR-3), so no arm advantaged; verdicts stand. Routed below post-reveal.

Key unsealed AFTER this block was written.
