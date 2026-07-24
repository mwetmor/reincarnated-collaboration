# TSF6-TRACK-A run report — parameter-fidelity rung of the sim-fidelity hypothesis

**Date:** 2026-07-24 · **Executes:** gamora (sim seam) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-24-tsf6-track-a-run-charter.md` (its gates govern)
**Ground truth:** `agentic_orchestration/legolas/notes/2026-07-23-gd-arz-extraction-probe.md` §1 + §4
(values consumed FROM the note; no .arz re-parse)
**Unit-pin math note (Discipline #1, preregistered BEFORE results):**
`reincarnated-engine/src/reincarnated/simulation/math/tsf6-track-a-unit-pin-2026-07-24.md`
**Harness (experiment tooling, charter §4):**
`reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/tsf6_track_a_harness.py`

**Rubric-law compliance:** this run answers rung (a) ONLY. It supports NO "sim twins GD" claim. The
verified ceiling is stated in the verdict paragraph (§4). The gap register (§3) is load-bearing coverage,
not decoration — every GD parameter class gets a row (charter §0 predicate-diff).

---

## §0 — STEP 0: the unit pin (G1), preregistered

**K = 1.60** (GD world-units → sim distance-units). FROZEN by the math note BEFORE any scenario ran.

**Derivation anchor (charter-mandated melee pair):** GD `meleeRange` = 1.25 wu ↔ the sim's
melee-engagement distance = **2.0** (`spatial_engine.py:2011` `range_m = float(skill.get("range_m") or
2.0)` — the null-guard distance at which a melee attacker lands its hit; also the player min-attack floor
`:4079` `max(2.0, ...)`). → **K = 2.0 / 1.25 = 1.60.**

**Cross-checks (charter §3):** GD `moderateRange` 9.0 ↔ sim `RANGE_PROFILE_DISTANCE["medium"]` 8.0 →
K_mid = 0.889. GD `longRange` 15.0 ↔ sim `long` 14.0 → K_long = 0.933.

**G1 finding (Discipline #12, framed not buried):** a SINGLE linear K does not reconcile GD's melee ring
with GD's range bands under the sim's constants. The mid/long bands agree (~0.9×) but the melee anchor is
~1.8× larger — the sim's 2.0m melee floor is a coarse bounded-fight null-guard, proportionally wider than
GD's fine 1.25-wu weapon reach. K = 1.60 is carried per charter mandate; where a gate would flip under
K∈[0.889, 1.60] the sensitivity is reported. Matt's Track-B externally-anchored K may supersede this
DBR-internal pin (TSR-6c). **G1: PASS (K derived + logged veto-open, no post-hoc refit).**

K-projected sim-unit boundaries: InnerView 6.4 · **View 24.0** · **MaxPursuit 120.0** · PursuitTime 10.0s
(K-invariant) · Flee 25.6 · Wander 6.4.

---

## §1 — ANVIL scenario (hero stationary, blind policy `[["distance",1.0]]`)

Stationary hero (`movement_speed=0`), single GD zombie (`melee_aggressive`, GD zombie_a01 params × K),
spawn-distance sweep straddling both K·InnerViewDistance (6.4) and K·ViewDistance (24.0). Per-tick mob
trajectory observed via the byte-neutral `frame_sink` hook (zero determinism perturbation). Onset =
mob closes to melee contact (min_dist_to_player ≤ 2.5) from the spawn distance.

| spawn dist (sim u) | closed to melee? | min dist to hero | vs boundary |
|---|---|---|---|
| 4.0 | YES | 0.8 | inside InnerView |
| 6.4 (K·InnerView) | YES | 0.8 | at InnerView |
| 10.0 | YES | 0.8 | mid |
| 21.6 (G2b bound) | YES | 0.8 | K·View −10% |
| 24.0 (K·View) | YES | 0.8 | at View |
| **26.4 (G2a bound)** | **YES** | **0.8** | **K·View +10%** |
| 30.0 | YES | 0.8 | beyond View |
| 40.0 | YES | 0.8 | 1.67× View |
| 60.0 | YES | 0.8 | 2.5× View |
| 100.0 | YES | 1.08 | 4.2× View |

**The mob aggros and closes to melee at EVERY spawn distance**, including far beyond K·ViewDistance+10%.
Trajectory inspection: `dist_from_spawn` grows LINEARLY from tick 0 at every distance (e.g. d=100: dfs
0.6→23.6→46.6→69.6 at t=0/4/8/12s — constant speed, no onset delay, no acceleration ramp).

- **G2a (no aggro beyond K·View·1.10 = 26.4): BLOCKED-MECHANISM.** The sim has NO ViewDistance-gated
  aggro-onset mechanism. Default mob behavior is **pursuit-from-tick-0** regardless of spawn distance
  (confirmed: mob pursues from 100u away). Per charter BLOCKED-MECHANISM law, this ABSENCE is the finding
  — not a fudged pass, not a real failure. The `aggro_radius_m` field exists (`:1124`, default 8.0) but is
  DEAD for onset: it is stored at construction (`:5587,:5659`) and referenced in one comment (`:5710`),
  and is NEVER read in a gating comparison. The only proximity gate is `serial_activation_radius_m`
  (`:1691`) — a different, opt-in mechanism (pack-local latch, permanent once activated), inert here.
- **G2b (aggro onset by K·View·0.90 = 21.6): PASS (vacuously).** The mob aggros at 21.6 and below — but
  it also aggros everywhere else, so the pass reflects the absence of any suppressing gate, not a
  view-distance onset. Reported honestly.
- **G2c (inner-vs-outer anger-rate asymmetry, 12.0 vs 3.0): NO-MECHANISM.** Onset is binary and
  instantaneous at all distances (no ramp, no inner/outer speed difference). The sim has no anger
  accumulation. `InnerSightAngerRate`/`SightAngerRate` have no sim home.

**K-sensitivity:** G2a/G2c outcomes are K-invariant — no aggro gate exists at ANY K in [0.889, 1.60],
so the BLOCKED-MECHANISM verdict does not depend on the melee-vs-band K disagreement.

---

## §2 — KITE-LINE scenario (hero recedes at 0.5× mob speed; mob pursues)

Hero starts inside aggro (4u ahead of mob spawn), recedes along +x at 0.5 × mob movement_speed (pinned
pre-run, math note §4). Mob pursues; net-dragged outward from spawn. Leash distance passed as the
GD-derived value + two sim-native comparators. `is_leashing` flip + dist-from-spawn + elapsed observed.

| leash dist (sim u) | leashed? | dist-from-spawn at leash | elapsed at leash |
|---|---|---|---|
| **120.0 (K·MaxPursuit)** | YES | **120.17** (+0.15%) | 27.5 s |
| 35.0 (swarm override) | YES | 35.11 (+0.3%) | 7.8 s |
| 18.0 (sim default) | YES | 18.40 (+2.2%) | 3.9 s |

- **G3a (pursuit sustained inside K·MaxPursuitDistance = 120): PASS.** The mob pursues continuously out to
  dist_from_spawn ≈ 120 before leashing; sustained pursuit inside the leash radius is confirmed at all
  three leash settings.
- **G3b (disengage at K·MaxPursuit ±10% [108,132] OR PursuitTime 10s ±10% [9,11]s — which?):
  PASS on the DISTANCE mechanism.** At leash=120 the mob disengages at dist_from_spawn = 120.17, squarely
  inside [108, 132]. **The sim keys on DISTANCE, not time:** `leash_at_elapsed_s` VARIES with the leash
  distance (3.9s / 7.8s / 27.5s) — a fixed 10s PursuitTime would fire at a constant time regardless. At
  leash=120 the mob pursued through 10s/15s/20s WITHOUT leashing (leash at 27.5s), positively ruling out a
  10s time-leash. The trigger is `spatial_engine.py:1706` `if dist_from_spawn > entity.leash_distance_m`.
  The +0.15–2.2% overshoot is exactly one movement-step past the threshold (checked after the move-step).
  **`PursuitTime` (10000 ms) has NO sim home — BLOCKED-MECHANISM** (the sim carries only the distance
  leash; GD carries both, and hardcoding one is the TrinityCore #25833 cautionary precedent the charter
  flagged — the sim's choice is distance-only).
- **G3c (`FleeBehavior='NeverFlee'` honored): PASS (trivially).** No flee occurred at any point. The sim's
  only flee mechanism (Wave-D fear-flee, `:1711`) is driven by a `fear` ActiveEffect MARKER, not a low-HP
  `fleeDistance` trigger; no fear was applied in-scenario, so no flee — `NeverFlee` is honored by
  construction, but the sim would ALSO not flee on low HP for ANY mob (see gap register).

**Bonus mechanism characterization (post-leash return):** the sim leash is a full D2/PoE-style
**return-to-spawn with re-aggro**. On crossing MaxPursuitDistance the mob RETURNS toward spawn
(dist_from_spawn decreases to ≈0), then re-aggros and re-pursues; against a receding hero this oscillates
(leash flips True→False repeatedly at ~9.6s/21.6s/33.6s). Distance-keyed throughout; no time component.

---

## §3 — GAP REGISTER (G4, load-bearing) — one row per GD parameter class

| GD parameter class | GD value(s) | Sim mechanism home | Result |
|---|---|---|---|
| **Aggro radii** (`ViewDistance` 15.0, `InnerViewDistance` 4.0) | outer/inner view zones | `aggro_radius_m` field EXISTS (`:1124`) but is DEAD for onset (stored, never gate-read). Onset = pursuit-from-tick-0. | **BLOCKED-MECHANISM.** No view-distance onset gate. Named delta: sim needs a per-tick `dist ≤ aggro_radius_m` onset check (+ inner/outer zoning) to key aggro on view distance. Tested (ANVIL §1): mob aggros at all distances 4→100. |
| **Anger rates** (`SightAngerRate` 3.0, `InnerSightAngerRate` 12.0) | anger accumulation /s, inner 4× outer | none | **BLOCKED-MECHANISM.** No anger-accumulation state; onset is binary/instant. Named delta: sim has no `anger` scalar that accrues at zone-dependent rate to a threshold. Tested (G2c): no ramp, no inner/outer asymmetry. |
| **Pursuit distance** (`MaxPursuitDistance` 75.0) | leash radius | `leash_distance_m` (`:1125`) → trigger `:1706` `dist_from_spawn > leash`. | **EXISTS + PARAMETER-FAITHFUL.** Tested (KITE §2): leash fires at dist_from_spawn = 120.17 vs K·75.0 = 120.0 (+0.15%, inside ±10%). Distance-keyed, return-to-spawn semantics. |
| **Pursuit time** (`PursuitTime` 10000 ms) | time-based leash | none (leash is distance-only) | **BLOCKED-MECHANISM.** Sim has no time-based disengage. Named delta: sim needs a `time_since_aggro > PursuitTime` alternate leash trigger (GD ORs distance ∨ time). Tested (G3b): elapsed-at-leash varies with distance; no fixed-time fire. |
| **Flee** (`fleeDistance` 16.0, `FleeBehavior='NeverFlee'`) | low-HP flee at range, disabled here | Wave-D fear-flee (`:1711`) reads a `fear` EFFECT marker, NOT low-HP `fleeDistance`. | **PARTIAL / BLOCKED for HP-flee.** `NeverFlee` honored trivially (G3c PASS). But the sim has NO low-HP `fleeDistance` mechanism for ANY mob — flee is fear-marker-driven only. Named delta: an HP-threshold flee keyed on `fleeDistance` has no sim home. |
| **Wander** (`WanderDistance` 4.0, `RoamDistance`/`MinRoamDistance`/`MaxTimeBeforeRoam`) | idle roam around spawn | none (grep wander/roam/Roam → 0 hits in spatial_gauntlet) | **BLOCKED-MECHANISM.** No idle-roam behavior; un-aggroed mobs hold at spawn (or pursue from tick 0). Named delta: sim has no pre-aggro idle wander loop. |
| **Distress-call** (`distressCallRange` 16.0, `DistressResponseGroup`, `ChanceToRespondToDistressCall` 75) | faction-aware alert propagation | none | **BLOCKED-MECHANISM.** No aggro-propagation between mobs. Named delta: sim has no distress/alert broadcast (a mob aggroing does not wake neighbors). Consistent with probe §5.3 (no cross-game precedent). |

**Summary:** 1 class PARAMETER-FAITHFUL (pursuit distance / leash), 1 PARTIAL (flee — `NeverFlee` honored
but no HP-flee mechanism), 5 BLOCKED-MECHANISM (aggro radii, anger rates, pursuit time, wander,
distress-call). Every absence is EXPECTED — the sim was built for bounded balance fights, not open-field
aggro (charter §4). No mechanism was built mid-run to force a PASS.

---

## §4 — Verdict

**Parameter-faithful in classes {pursuit-distance / leash}; mechanism-delta in classes {aggro-radii,
anger-rates, pursuit-time, wander, distress-call, and low-HP flee}.**

The one spatial mechanism the sim SHARES with GD — a distance-triggered pursuit leash — reproduces GD's
`MaxPursuitDistance` faithfully under the pinned K (leash at 120.17 vs 120.0 target, +0.15%, well inside
±10%), and does so via the same distance-from-spawn semantics with D2/PoE-style return-to-spawn. Every
other GD monster-AI parameter class (the two-zone view-distance aggro onset, the inner/outer anger
accumulation, the time-based pursuit cutoff, idle wander, and faction distress propagation) has NO home
in the sim: the sim's default is pursuit-from-tick-0 with no perception ramp, no time-leash, no roam, and
no alert broadcast. This is the honest, complete rung-(a) answer: the sim is a bounded-fight engine whose
ONLY open-field-AI overlap with GD is the leash radius, which it renders faithfully; the remaining GD AI
surface is a named mechanism delta, correctly OUT of the sim's built scope and reserved for a next-lap
mechanism charter (no silent scope growth this run). No outcome here supports a "sim twins GD" claim.

**Secondary G1 finding:** the sim's melee-contact distance and its range-band tiers do not share a single
linear conversion to GD's units (K_melee 1.60 vs K_band ~0.9) — a unit-fidelity delta worth carrying into
Matt's Track-B externally-anchored K calibration.

---

## Files

- Run report (this): `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md`
- Math note (K + FROZEN gates): `reincarnated-engine/src/reincarnated/simulation/math/tsf6-track-a-unit-pin-2026-07-24.md`
- Harness: `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/tsf6_track_a_harness.py`
- Primary sim sites cited: `spatial_engine.py` :706 (RANGE_PROFILE_DISTANCE), :1124 (aggro_radius_m dead
  field), :1125/:1706 (leash), :1691 (serial-activation gate), :1711 (Wave-D fear-flee), :2011/:4079
  (melee anchor 2.0), :4952 (frame_sink.tick observation hook).

**jack-ryan Gate-2:** findings-class review pending (charter §5).
