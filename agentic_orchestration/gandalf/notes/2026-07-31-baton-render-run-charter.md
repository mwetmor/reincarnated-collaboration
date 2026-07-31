# BR-1 — BATON-RENDER run charter (the fully-rendered battle sim)

**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Chartered:** 2026-07-31 · **Pattern:** desirable-run
(`operating-procedures/desirable-run-pattern.md`; F1–F4 all YES, audit in the fold-in ledger)
**Ledger of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` (Scopes 1–22 bind; this
charter composes them — it does not restate them)
**Matt authorization:** 2026-07-31 — *"take the phase2c baton and complete the run ending at the
fully godot rendered battle sim (including lighting, shadows, VFX, characters (player and enemy)?
Full combat sim render in a beautiful corner"* + two-lap law + Scope-22 casting rulings.

## §1 — Bounded substrate (frozen at launch)

- **S-1 Lap-1 traces:** 30 per-fight replay traces `boss__A__seed74000800-829.jsonl`
  (`reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/g5/traces/`, engine ≥
  `bef1f55`, real received-side). Schema = BATON-CENSUS (banked `32fa408f`): per-frame
  `alive/x_m/y_m/heading_rad/hp`, decision aim-lines, 19-field telegraphs (real nova:
  circle/12.0 m/2.32 s), damage/dot with element, ailments as `action_lock`.
- **S-2 Lap-2 traces:** Stage-2c rider-bearing replay traces (icearmor channel, telegraph
  `family`, `attack_id`). NOT yet located on disk — Lap-2 opens only when they exist (gate G-5).
- **S-3 Stage:** crypt corner — `kit_replica_level` at the CAM-LOCK-verified GD camera
  (GAL-CAM pinhole family, `godot-spec.json`), PC-LIGHT lighting fix in.
- **S-4 Bodies:** werewolf (player, Matt-locked) + Fantasy Rivals pack
  (`matt_notes_handoff_docs/recent-synty-packs/fantasy-rivals`, 20 SK rigs + emissive maps).
- **S-5 Feedback surfaces:** Bangers numerals + crit RED (verdicted); judgeable VFX presets
  (PASS ×3); element family 6/6.
- **S-6 Lighting cosmology:** the Scope 12–21 chain (Arm A, one sun, cone beams, cold pools,
  D1-esque carried light, ρ≈0.50 multiplicative shadow) — inherited, not re-opened.

## §2 — Decidable target-state

**T-1 (Lap 1):** one integrated watch MP4 — a full phase-1 fight rendered start→death in the
crypt corner at the GD camera, containing ALL of: cone-beam skylights + cold pools (BEAM-CONE
landed), unified shadow grammar (SHADOW-UNIFY acceptance: bright/dim tile ρ within ~10%, one
directional author), werewolf with warm carried light, cast boss with cold emissive, telegraph
decals rendering the real nova (shape+radius+wind-up from trace), damage numerals with crit RED,
element-mapped VFX on damage events, death resolution on `alive→false`. Checkable: each element
verified present per-cell before the watch is cut; the watch itself is Matt's M-EYE surface.
**T-2 (Lap 2):** same scene re-rendered on an S-2 trace with the three rider channels visibly
consumed (icearmor readable on the boss for the first time; `family`-qualified telegraph
handling; `attack_id`-keyed attack anims). Diff vs Lap 1 named in the landing note.

## §3 — Cell sequence (single-writer godot tree; one drax cell at a time)

| # | Cell | Owner | Scope |
|---|---|---|---|
| 1 | **BEAM-FIX** | drax | IN FLIGHT — five Scope-20 rulings |
| 2 | **BEAM-CONE** | drax | Scope-21 cone law; pool-BASE identity check |
| 3 | **RIVAL-CAST** | drax | pack import (R-PC-2 asset home), rig-compat + retarget on ElementalGolem lean (fallbacks: FortGolem, SpiritDemon), cold-emissive tint, casting verdict banked |
| 4 | **SHADOW-UNIFY** | drax | full cosmology; grammar validated on BOTH cast bodies; pools-vanish reconciliation; fog-unlit A/B |
| 5 | **TELL-DRESS** | drax | telegraph decals vs Lap-1 schema, `family`-hardening pre-built for Lap 2 |
| 6 | **ROOM-DRESS** | drax | per-room disrepair + doorway dirt-bleed (the "beautiful corner" dressing) |
| 7 | **LAP-1 WATCH** | drax | trace-driven playback, fight select from the 30 seeds, integrated MP4 → Matt |
| 8 | **LAP-2 RE-RENDER** | drax | gated on G-5; rider channels consumed; diff note |

Read-only measurement cells (galadriel) may run in parallel at any step; every cell reads the
fold-in ledger FIRST; every landing banks + pushes to the meta-repo; godot commits LOCAL only.

## §4 — In-run rulings (veto-open) + pre-registered gates

**Ruled in-run by the conductor (reasoning-boundaries):**
- **R-BR-1 boss-ID:** `is_boss` lies false in Lap-1 traces → boss = max-HP actor. Lap 2: prefer
  the rider if present, diff against the heuristic.
- **R-BR-2 animation mapping:** locomotion from kinematics (position/heading drive; blend by
  speed), attack anims keyed to telegraph wind-up + damage emission, death on `alive→false`,
  via the RETARGET-READY pipeline. Foot-slide is acceptable Lap-1 debt; named, not hidden.
- **R-BR-3 VFX mapping:** `damage.element` → preset family; nova = TELL-DRESS ring + burst at
  `fire_tick`. No invented projectiles — travel is ABSENT from schema; instant-resolve renders
  as such (declared limitation, wave territory).
- **R-BR-4 fight selection (Lap-1 watch):** conductor picks the seed whose fight best exercises
  the feature set (nova fired, both a crit and a death present); selection logged with counts.
- **R-BR-5 casting:** ElementalGolem lean per Scope 22; drax holds final say at rig-quality.

**Gates:**
- **G-1** BEAM-CONE: measured base-radius == pool-radius per window (tolerance named in-cell).
- **G-2** RIVAL-CAST: boss rig imports, retargets, animates without inversion (the L6
  `remove_tracks/unmapped_bones` law available); FAIL → fallback chain, then dark-fantasy
  DarkLord as honorable floor (scene-proven).
- **G-3** SHADOW-UNIFY: ρ within ~10% bright-vs-dim; zero non-directional shadow authors;
  pools survive (pools-vanish landmine reconciled).
- **G-4** LAP-1 WATCH completeness: every T-1 element present in-frame at least once; checklist
  in the landing note.
- **G-5** LAP-2 open-gate: rider-bearing traces exist on disk + schema spot-check passes.
  If Stage-2c traces never materialize → honorable fallback: Lap 1 IS the deliverable; Lap 2
  parks as a standing queue row against the battle-sim run's ledger.

**Gate FAIL = processable finding**, never a terminal event.

## §5 — Matt interface

- **M-EYE standing:** verdicts in motion; the Lap-1 watch is the review surface.
- **Commitment-boundaries that HALT:** godot push (local-only until his word), any purchase,
  any charter amendment, taste vetoes on cast/dressing (veto-open by construction).
- **Red-flag pings only** mid-run; landings bank+push to the meta-repo as they occur.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-31.
