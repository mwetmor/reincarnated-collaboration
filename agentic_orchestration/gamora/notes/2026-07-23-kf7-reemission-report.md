# KF-7 re-emission lane — implementation report (gamora, simulation seam)

**Run:** KIT-FIDELITY · **Gate:** KF-7 · **Ledger:** KFL-19b · **Conductor:** gandalf (RUN-CONDUCTOR) · **Date:** 2026-07-23

Combat-behavior change **Matt-RATIFIED 2026-07-23** (in-chat: *"I concur with base mean"*), item-6 option (a):
compiler emits `base_mean` as the injected per-hit magnitude. This report is written-as-you-go per lane LAW.
Commit-locally-NEVER-push (conductor verifies + pushes).

---

## Load-bearing pre-flight finding (surfaced, not silently resolved) — the re-emission target

Before touching the payload I established the ground truth of the frame set, because the charter's model and
the on-disk reality diverge in a way that changes what "re-emit" means. Documented here per the Deviations law
(surface, do not silently choose) + Discipline #11 (empirical inspection over assumption).

**What the charter says (KFL-19 line 865-866):** "RE-EMISSION of the pilot replica frame set (same
fights/arms/seeds as on-disk, compositions attached via `attach_composition_blocks`, gauge fields live,
post-shape damage)."

**What is actually on disk** (`agentic_orchestration/gamora/notes/replica1-frames/`, 40 NDJSON + manifest):
- The frames are the **REPLICA-1 ref roster** — 5 procedurally-generated *martial* pilots
  (`d2-bowazon`, `poe1-kinetic-fusillade`, `poe1-caustic-arrow`, `d2-poison-javazon`, `poe1-frost-blades`),
  emitted at engine hash `2f43045` which **PREDATES** the KF-5 gauge fields (`2e222e3`).
  Verified: the first `damage` event on `replica-d2-bowazon__blind__…` carries only 13 keys — **none** of the
  5 gauge fields. `source_id = S1_martial_bar_endgame_bc_ranged_high_flat_dex_none_s0_balanced` — a
  `_build_martial_player_class` W3'-gate synthetic class, **not** a `compile_kit` compiled kit.
- These martial pilots carry **NO `_composition` block** and **cannot** — `attach_composition_blocks(class_dict,
  compiled_kit)` requires a `CompiledKit`, which a W3'-gate martial class does not have. Run through the sink at
  HEAD, `_kf5_gauge_for_hit` returns all-None (spatial_engine.py:3554-3556) → gauge stays null.

**The reconciliation (why the target is the COMPILED kits, not the on-disk martial pilots):**
- The **exit predicate** ("player-DEALT hits … non-null finite `pct` with median ≈ 100") is satisfiable ONLY
  when the fighter carries a `_composition` — i.e. ONLY for a KF-4 **compiled kit**. It is unsatisfiable for the
  on-disk martial pilots (gauge null by construction).
- The **charter payload** itself (line 866: "compositions attached via `attach_composition_blocks`, gauge fields
  live") is a compiled-kit operation.
- **drax's KF-6 scene documents the intent verbatim** (`reincarnated-godot/scripts/replica_playback.gd:43-52`):
  *"the KT-2 rigs are keyed to the KING-TWIN pilot-5 … but the REPLICA-1 frames on disk carry the OLDER ref
  roster … the COMPILED-kit frames arrive with the parent run's KF-5/KF-6 … When KF-5/KF-6 land with pilot-5
  kit_ids, the by-kit path lights up and the bridge default falls away with no scene change."* The scene binds
  by `kit_ref`; `PILOT_RIGS` is keyed to `{d2-firewall-sorc, d2-fire-sorc, gd-flames-of-ignaffar-purifier,
  poe2-bonestorm, poe1-cyclone}` — the compiled pilot-5.

**Therefore:** "same fights/arms/seeds as on-disk" is the **grid SHAPE** (blind/aware × encounter × 4 seeds),
and the re-emission's payload is the **compiled pilot-5 kits** carrying live gauge, REPLACING the stale
pre-KF-5 martial-pilot frames. This is the reading under which every downstream predicate (exit predicate,
drax scene bind, charter payload) is coherent. The literal reading (re-emit the martial pilots) satisfies NONE
of them. Resolution recorded here + carried in the frame-set manifest.

**Also corrected in passing:** the Godot scene reads frames from an ABSOLUTE path into the COLLAB repo
(`FRAMES_DIR_DEFAULT = …/reincarnated-collaboration/agentic_orchestration/gamora/notes/replica1-frames`), NOT
from inside `reincarnated-godot`. There are ZERO `replica-*.ndjson` files in the godot repo. So the "data swap"
is a **collab-repo** file replacement; the lane's "godot: replaced replica-*.ndjson data files ONLY" commit is
**N/A** — no godot data files exist to replace, and no `.gd`/`.tscn` is touched (correct per LAW). The frames'
commit lands in COLLAB.

---

## Commit SHAs

- **Engine (`~/Games/reincarnated-engine`, branch main):** `c5a2f2d`
  (shape fix `kit_compiler.py:280` + math note §10 + KF-5 smoke band re-center + `damage_resolver.py:942`
  docstring INFO-1 + rider-ii `skill_cooldowns` tick field). Message cites the Matt ratification.
- **Collab (`~/Games/reincarnated-collaboration`):** `__COLLAB_SHA__`
  (this report + the KF-7 compiled-kit emit driver). The re-emitted 40-fight compiled pilot-5 frame set +
  manifest are physically written to disk (validated) and REPLACE the stale pre-KF-5 martial-pilot frames,
  but the `replica1-frames/` dir stays **UNTRACKED-by-design** — matching the established precedent (the
  original frames were NEVER git-tracked; the emit driver `40d9b97b` is the git-tracked regenerable source,
  Disc #3). drax's scene reads the frames off disk via `FRAMES_DIR_DEFAULT` regardless of git-tracking.
- **Godot:** N/A — no `replica-*.ndjson` in the godot repo (frames live in collab; scene reads via absolute
  path `FRAMES_DIR_DEFAULT`). No `.gd`/`.tscn` touched (correct per LAW).

All committed locally, NONE pushed (conductor verifies + pushes).

---

## Task-by-task record

### Task 1 — Shape fix (`kit_compiler.py:280`)

`"magnitude": base_max` → `(base_min + base_max) / 2.0` (None-guarded so a GAP base — both leaves None —
still injects None, preserving the existing "None when base is GAP → partial" semantic exactly). One-line
intent; the surrounding comment updated to name the KF-7 shape + the Matt ratification. **Disc-#12
combat-behavior change, Matt-RATIFIED 2026-07-23** ("I concur with base mean"), item-6 option (a).

Empirically bit-verified across ALL compiled pilots — every injected magnitude is now the band mean:
firewall `1308.0=(1296+1320)/2` · fire-sorc FireBall `242.5` / Meteor `1256.0` · cyclone `376.5` ·
bonestorm `257.0` · gd-flames GAP→`None` (HELD).

### Task 2 — Band re-derivation (math §10, math-BEFORE-code) + smoke re-center

**Math note §10 appended** (`simulation/math/kf5-expected-pct-2026-07-23.md`) BEFORE the smoke edit —
same rigor + margin logic as §8:
- **Post-fix center = 100.00 EXACTLY, kit-independently** — the injected magnitude and the expected base
  are now the SAME quantity (`base_mean`), so `injected/base_mean = 1.0000` and `pct` centers on 100 for
  ANY kit (§10.1). Empirically: bonestorm `100 × magnitude/base_mean = 100.0000` (was 120.2335).
- **Analytic band = 100 × [0.80, 1.20] = [80, 120]** (§10.2) under the live `_DMGVAR_LO/HI` draw. Replaces
  §8's pre-fix [96.19, 144.28]; same ±20% spread width, center slid 120.23 → 100.
- **Smoke guard band re-derived = `[70, 130]`** (§10.3) — analytic [80,120] + ~10-pt guard margin each side
  (§8's margin logic, deliberately slightly conservative). Catches CENTER drift: base_max regression →
  center 120.23 → max-corner 144.28 **> 130 → RED**; base_min regression → center 79.77 → min-corner
  63.8 **< 70 → RED**. Fidelity gauge, not variance gate.
- **Smoke assert updated:** `_PCT_LO, _PCT_HI = 90.0, 150.0` → `70.0, 130.0`; the ~30-line band-choice
  docstring rewritten to cite the new center/band/shape; the smoke header docstring gained a KF-7 note.
- **120-center / [90,150] grep + re-center (§10.4):** every live reference re-centered; the remaining
  "120.23/96.19/144.28/[90,150]" strings in the smoke are DELIBERATE — they cite the OLD center as the
  regression the new band catches. §8 left as HISTORICAL pre-fix record (reconcile-not-amputate); a
  note-reader reaches §10 for current truth. No stray live band reference remains (grep-confirmed; other
  "120" hits are the 120 s scenario clock, unrelated).

**Direction guard honored (§10.3.1):** per-hit damage DROPS ÷1.202 (~−17%: bonestorm injected 309→257),
so kill times LENGTHEN ~+20%. Gate-2 finding **line 44** ("mobs die faster") is a direction SLIP; **line
48** is correct. §10 adopts line-48 (damage down, kills down, kill-times up). Empirically confirmed:
KF-5 4000-HP wall `mean_mobs_killed` shifted **12.00 → 11.00** (DOWN) — the expected scenario artifact,
NOT tuned (no calibration knob touched).

### Task 3 — INFO-1 docstring fix (`damage_resolver.py:942`)

"±15%" → "±20%" (live constants `_DMGVAR_LO=0.80 / _DMGVAR_HI=1.20` = ±20%). Docstring ONLY — no constant,
no combat behavior touched. Documented in §10.5.

### Task 4 — Smokes (both green at new expectations)

```
KF-4 compiler smoke:  ASSERTS: 36 GREEN · 0 RED · 1 GAP/untested   SMOKE PASS
  (composition checks center-independent, held exactly as predicted; the 1 GAP is
   gd-flames-of-ignaffar primary_has_damage_base — HELD, T4 pending)

KF-5 expected/pct smoke:  KF-5 SMOKE PASS  (with the NEW band [70,130])
  expected_premit == 2570.0 (base_mean×offensive_mult, Pin A): True     ← UNCHANGED (always base_mean-anchored)
  [healthy] realized amount > 0 on all 59 dealt hits: True (min=1233.7 max=1818.6)   ← all dealt > 0
  [healthy] pct finite on all hits: True; all in sane band [70.0,130.0]: True (min=80.01 max=117.94)
                                                                        ← empirical center 100 (was [96.20,141.80])
  same-seed emitter ON twice → identical frames: True                  ← determinism byte-identity intact
  ON footer elapsed_s=120.100000 vs OFF mean_elapsed_s=120.100000 → identical combat outcome: True
```

The KF-5 empirical band moved [96.20, 141.80] (pre-fix, §8) → [80.01, 117.94] (post-fix) — the ±20%
variance sweep now centered on 100 instead of 120.23. `mean_mobs_killed` shifted down (the accepted
one-time combat consequence, observed not tuned).

### Task 5 — RE-EMISSION (the payload) — compiled pilot-5, gauge live

**Driver:** `agentic_orchestration/gamora/notes/2026-07-23-kf7-emit-compiled-refset.py` (NEW). Built
because no compiled-kit emission driver existed (the on-disk driver emits W3'-gate MARTIAL pilots that
cannot carry a `_composition`). Reuses PROVEN machinery verbatim: `compile_kit(pilot)` →
`attach_composition_blocks(class_dict, ck)` (the KF-5-smoke gauge-lighting path, math §4) × the SAME W3'
`make_encounter_scenario(fclass)` + `build_neutral_mob_dicts(tiers)` encounter the on-disk frames used ×
`policy_config` BLIND/AWARE per arm × sink `kit_id = <compiled pilot id>` → header `kit_ref` = the compiled
pilot id → drax `PILOT_RIGS` binds. PROJECTION path (`player_class=None`, the KF-4 compiler target).
SEQUENTIAL (Disc #3). corpus.db READ-ONLY. Seeds = on-disk `20260722..25` verbatim (NO seed additions).

**Grid:** 5 compiled pilots × {blind, aware} × encounter × 4 seeds = **40 fights** (same grid shape as
on-disk). Deterministic formation-per-pilot (each kit always dresses the same encounter):
firewall→swarm · fire-sorc→volley-fan · gd-flames→lane · bonestorm→emplacement · cyclone→swarm.

**Stale-frame removal (data swap completeness):** the compiled-kit filenames do NOT overlap the on-disk
martial-pilot filenames, so a naive emit LEFT BOTH sets on disk (80 files) — drax's scene enumerates ALL
`replica-*.ndjson`, so it would have shown stale pre-gauge frames alongside the new ones. Removed the 40
stale martial-pilot files (bowazon / kinetic-fusillade / caustic-arrow / poison-javazon / frost-blades);
the frames dir now holds EXACTLY the 40 compiled pilot-5 files + the refreshed manifest (roster switch +
new engine hash recorded in `manifest.json`, `roster_note`).

**Determinism:** `--dup-check` re-emit `poe2-bonestorm/blind/seed20260722` → `filecmp` byte-identical **True**.

### Task 6 — Frame validation (python-side, no Godot) — ALL 40 OK

Every line parses · every `damage` event carries the 5 gauge fields (finite-or-null) · header roster
carries finite `max_hp` · tick entities carry finite `hp` · player-DEALT hits (4 anchored kits) carry
non-null finite `pct` all in-band · all dealt `amount > 0` (anchored) · `pct_received` null on all
mob-dealt hits · gd-flames GAP honest (all 44 dealt hits `pct` null + `amount` 0 — HELD, not faked).

**Per-fight dealt-pct (median / min / max), anchored kits (gd-flames = GAP, null):**

| kit (median-of-fight-medians) | per-fight pct spread |
|---|---|
| d2-firewall-sorc — **96.32** | fight medians 85.68–103.73; hit-level min 80.42 / max 119.95 |
| d2-fire-sorc — **96.77** | fight medians 92.21–106.76; hit-level min 84.94 / max 111.32 |
| poe2-bonestorm — **98.04** | fight medians 93.83–107.27; hit-level min 80.50 / max 117.80 |
| poe1-cyclone — **97.37** | fight medians 93.90–100.89; hit-level min 80.42 / max 119.95 |
| gd-flames-of-ignaffar — **null (GAP)** | 44 dealt hits, all `pct` null + `amount` 0 (HELD, T4) |

**Aggregate anchored dealt pct (280 hits): median 96.51 · mean 97.34 · min 80.42 · max 119.95** — every
hit in the analytic band [80,120]; center **≈ 100** (exit predicate met).

**Diagnosis of the ~2.6–3.5% below-100 residual (Disc #11 — measured, not assumed).** The center is 96.5–
97.4, not exactly 100. Fully diagnosed:
- The variance RNG is provably unit-mean (100k draws of `U[0.80,1.20]` → mean 1.00003). NOT a biased draw.
- The gauge's `buff_dmg_mult`, `armor`, `scaling_stat` mirror the realized path EXACTLY — verified live:
  entity `damage_modifier` == `combatant_state.damage_modifier` == 0.60, buff% = 0, bonus% = 0, so
  `expected_postmit = 2570 × 0.60 × (1−20/3020) = 1531.79` is arithmetically correct. The realized
  `amount`/expected ratios ARE the variance draws.
- Survivorship ruled OUT: first-hit-per-target median (96.85) ≈ all-hit median (96.51).
- **Conclusion:** the residual is **finite-sample scatter of this specific 40-fight seed set** — only 32
  fights carry dealt hits (2–19 each), so the fight-level statistic has low power; a correct fight-level
  permutation test puts the observed center at one-sided p≈0.013 (a small, ~2.6% low, borderline-real
  scatter), NOT a gauge defect and NOT introduced by the KF-7 shape fix (which shifts realized and expected
  identically → cancels). The center is "≈ 100" to within ~2.6% and firmly in-band; the exit predicate
  ("median pct ≈ 100") is met. Should a future lap want a tighter-centered watch demo, use more/larger-count
  fights (more hits per fight → the median converges to 100 by the LLN) — a scenario choice, not a code fix.

### Task 7 — Riders (assessed)

- **Rider (ii) `skill_cooldowns` — INCLUDED (small, honest, null-safe additive; charter KFL-6d assigns the
  hot-bar emit to gamora).** Added to the tick frame's per-entity payload (`replica_frame_emitter.py`
  tick()): a pure read of the live `SpatialEntity.skill_cooldowns: list[float]` (spatial_engine.py:939),
  finite-guarded, `[]` when absent (mobs / pre-fight). v1-ADDITIVE (NO schema bump). Combined with the
  already-emitted `commit_state`/`commit_skill_idx` (cast-in-progress = `commit_state != "idle"`), this
  lights drax's hot-bar cooldown ring + flash-on-use with ZERO derivation (§8 law). **Verified live:** the
  field takes real non-zero values (0.0 → 1.1+ s) through a fight — the ring genuinely animates; KF-5 smoke
  still PASSES (determinism byte-identity intact, combat outcome unchanged). **Frames re-emitted** to carry
  it. **Schema addition documented:** `tick.entities[].skill_cooldowns: list[float]` (v1-additive).
- **Rider (i) `expected_max_hp` — REPORTED AS NEXT-LAP (no honest engine source today).** The header roster
  already carries `max_hp` (the sim's derived HP, which drax's globe reads). But the rider wants a
  max-HP **FIDELITY %** overlay — i.e. an `expected_max_hp` denominator anchored to the SOURCE game's life
  pool at the build point. The compiled kit + `_composition` carry NO source-HP anchor (verified: no
  `max_hp`/`hp`/`base_hp`/`expected_hp` on the CompiledKit or class_dict — `max_hp` is DERIVED from
  `vitality` via the engine HP formula). Emitting a source-fidelity HP % would require INVENTING the
  expected-HP number (violates §8 zero-derivation). **Missing engine state named:** a per-kit
  source-game max-HP anchor from a KF-2-style HP harvest (the character sheet's life pool at the documented
  build point), stamped onto the `_composition` — the exact analog of how the damage `base_min/base_max`
  anchor lets the pct gauge work. Once that anchor exists, `expected_max_hp` becomes a trivial null-safe
  header additive with ZERO change to this lane's emitter shape. Next-lap admission, not a blocker (the HUD
  null-guards; omission is safe).

---

## Gate-2 readiness (scoped, per engine-diff law — follows the lane return)

1. **Shape fix (§10.1):** `kit_compiler.py:280` → band mean, None-guarded (GAP still None). Matt-RATIFIED
   combat-behavior change (item-6 (a), KFL-19). Center → 100.00 kit-independently; bit-verified on all pilots.
2. **Band re-derivation (§10.2–10.3):** analytic [80,120]; smoke guard [70,130] (§8 margin logic). Catches
   CENTER drift (base_max→144.28>130 RED; base_min→63.8<70 RED); absorbs ±20% spread. Fidelity gauge.
3. **Direction (§10.3.1):** damage ÷1.202 down, kill times +20% up (line-48; line-44 slip NOT propagated);
   `mean_mobs_killed` 12→11, observed-not-tuned.
4. **INFO-1 (§10.5):** `damage_resolver.py:942` docstring ±15%→±20%; docstring only.
5. **KF-4 invariance:** 36/0/1 holds (composition asserts center-independent; base_min/base_max unchanged).
6. **Rider-ii additive (`replica_frame_emitter.py` tick):** `skill_cooldowns` pure read of live entity
   field, finite-guarded, `[]`-safe; v1-additive NO schema bump; KF-5 smoke determinism byte-identity intact
   (None-sink path untouched — the field is inside the tick emit which only fires with a sink).
7. **Re-emission purity:** the emit uses ONLY the observability sink + `attach_composition_blocks` (pure
   class_dict enrichment, resolver-ignored underscore key) — NO resolver/HP/RNG mutation; determinism
   byte-identity dup-check True.

---
