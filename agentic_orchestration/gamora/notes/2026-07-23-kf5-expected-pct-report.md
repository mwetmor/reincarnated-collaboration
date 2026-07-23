# KF-5 Expected / pct — implementation report (gamora, simulation seam)

**Run:** KIT-FIDELITY (conductor: gandalf) · **Gate:** KF-5 (KFL-12b) · **Date:** 2026-07-23
**Reviewer next:** jack-ryan (Gate-2, BLOCK authority, on the engine diff)
**Commit-NEVER-push:** all commits local; conductor pushes after verification.

## Commit SHAs

**Engine (`~/Games/reincarnated-engine`, branch main):**
- `de0090f` — KF-5 math note (Disc #1, math-before-code) + **Rider 2** (KF-4 note cite refresh, folded)
- `455d76a` — **Rider 1** mirror-sync `spatial_engine._RICH_TO_SPATIAL` (ISOLATED, rides its own Gate-2)
- `2e222e3` — KF-5 core: expected/pct additive frame fields + kf5_expected.py + KF-5 smoke

**Collab (`~/Games/reincarnated-collaboration`):** this report (commit pending; never pushed).

## What I built

1. **`simulation/math/kf5-expected-pct-2026-07-23.md`** — the math note, authored FIRST (Disc #1). Pins
   every formula (§ below). Names two deviations + the non-finite rule.
2. **`simulation/spatial_gauntlet/kf5_expected.py`** (NEW) — pure, stateless gauge math: composes the
   KF-4 `_composition` factors into expected_premit/expected_postmit + the three pct ratios; the
   `attach_composition_blocks` bridge; all finite-or-None guarded. Reads only its args, mutates nothing.
3. **`simulation/spatial_gauntlet/replica_frame_emitter.py`** — `on_hit` gains ADDITIVE
   `expected`/`expected_premit`/`pct`/`pct_premit`/`pct_received`; `dot` carries them null; a
   `_finite_opt` guard (None/non-finite → null, never crash the observability emit). NO schema bump.
4. **`simulation/spatial_gauntlet/spatial_engine.py`** — `_frame_on_hit` closure (a documented pure
   read) computes the gauge via new `_kf5_gauge_for_hit` (live reads of `_composition` + defender
   defense) and forwards it to `sink.on_hit`. **Plus Rider 1** (the mirror-sync, isolated commit).
5. **`simulation/kit_compiler/smoke_kf5_expected_pct.py`** (NEW) — the KF-5 smoke.

## Formulas pinned (per Pins A/B — KFL-3c — and the three-deep stack — KFL-3d)

```
base_mean        = (base_min + base_max) / 2                       # crit-free band midpoint
expected_premit  = base_mean × offensive_mult × crit_ev × hit_chance   # PIN A; variance OMITTED (unit mean)
expected_mag     = expected_premit × buff_dmg_mult                 # live DPS lever, read (not re-derived)
expected_postmit = expected_mag × (1 + scaling_stat×0.005) × (1 − mitigation)   # PIN B, live target
                     mitigation = armor/(armor+3000)  [physical/None]  |  clamp(res,0,0.95) [elemental]
pct_premit  = 100 × amount / expected_premit    # (1) INTERNAL GATE INSTRUMENT — mitigation-free denom (KFL-3d)
pct_postmit = 100 × amount / expected_postmit   # (2) the floater % KF-6 renders (Pin B live)
pct_received= 100 × amount / expected_postmit   # (3) received-side mirror (mob→player); same formula
```

**Two rulings I made (stated for Gate-2, math note §1.1 / §5):**
- **`hit_chance` ENTERS expected** as a multiplicative expectation factor (per-attempt source
  expectation = mean_roll × P(hit)). NO-OP for the current roster (all pilots hit_chance=1.0), carried
  so a future accuracy-anchored kit reads right without a formula change.
- **Non-finite / div-by-zero / absent-anchor → JSON `null`** (field present, value null), NEVER
  NaN/inf and NEVER field-absent. Null is the honest "un-anchorable here" GAP signal (§9 ladder); a
  present-but-null field keeps the schema uniform so KF-6 renders `<amount> (--)`.

**Variance is NOT in expected.** The resolver's per-hit U[0.80,1.20] roll has unit mean → 1.0 in
expectation (Pin A "mean roll"). Realized `amount` carries the draw, so pct scatters ±20% around its
center — the honest per-hit spread, not a fidelity defect. (Confirmed the constant is 0.80/1.20 = ±20%;
some legacy docstrings say "±15%" — the LIVE constant is ±20%; the unit-mean argument holds regardless.)

## Per-constraint evidence

| Charter constraint | Evidence |
|---|---|
| **#1 Math-before-code** | Math note `de0090f` committed BEFORE code `2e222e3` (separate commits, ordered). |
| **#2 Zero combat-logic change** | Byte-diff proof: stamped-vs-unstamped frame streams differ ONLY in `{expected, expected_premit, pct, pct_premit}` (strict subset of gauge keys); strip those keys → combat records BYTE-IDENTICAL. `frame_sink=None` path structurally untouched (gauge lives only in `_frame_on_hit`, which returns None when sink None → `on_hit=None` → per-target guard skips). |
| **Determinism (same seed → same trace)** | Same seed, emitter ON twice → identical frames (verified). ON footer elapsed_s == OFF mean_elapsed_s to 1e-9. |
| **#3 Non-finite guard** | Every new float via `kf5_expected._finite_or_none` (sim) + `_finite_opt` (emitter); div-by-zero → null. Smoke: every gauge field finite-or-null across all 59 damage events. |
| **#4 Additive-only** | `on_hit` gains keys; no existing key changed type/value; NO SCHEMA_VERSION bump (v1-additive). |
| **KF-4 smoke stays 35/1/1** | Re-run after ALL KF-5 code: **35 GREEN · 1 RED (cyclone, docketed) · 1 GAP (gd HELD) · PASS.** |
| **KF-5 own smoke** | `smoke_kf5_expected_pct` **PASS**: bridge stamps `_composition` on all skills; every damage event carries the full gauge key-set; expected_premit==2570.0 (bonestorm base_mean 257 × offensive_mult 10, Pin A); dealt side carries non-null expected; received side schema-checked. |

### Rider 1 (mirror-sync) byte-neutrality — verified independently

- Post-sync the engine mirror and `generation/geometry_derivation._RICH_TO_SPATIAL` are **byte-identical
  (26 == 26, zero key/value diff)** — verified by direct dict comparison.
- **No current producer reaches the Path-2 mirror with `orbit`/`placed_lane`:** every producer sets
  `spatial_geometry_type` explicitly (skill_schema derives it at gen time via
  `derive_spatial_geometry_type`; typed_monster_skills sets it directly; the KF-4 compiler sets it) →
  Path 1 (spatial_engine.py:823-826) returns BEFORE Path 2. Grep-confirmed no `geometry_type='orbit'/
  'placed_lane'` emitter lacks the explicit field. So the sync changes NO current trace; it only removes
  a latent Path-3 heuristic mis-derivation for a future producer that omits the explicit field.
- **KF-4 smoke unchanged (35/1/1)** immediately after the sync — empirical byte-neutrality confirmation.
- Isolated in commit `455d76a` (its own Gate-2; change-class pre-approved by jack-ryan).

## Deviations (logged, never silent)

**DEVIATION 1 — the `_composition` block was NOT plumbed to the sim (resolved, in-seam, no compiler touch).**
The charter/Gate-2 note state "every compiled skill carries a `_composition` block" as KF-5's input.
Empirically (probed live): the KF-4 compiler attaches the block to the `CompiledSkill.composition`
DATACLASS FIELD (kit_compiler.py:549), but `class_dict["skills"]` is built from `cs.skill_dict`
(kit_compiler.py:565) which does NOT contain it — `_composition` as a dict key existed NOWHERE in the
sim. **Resolution:** `attach_composition_blocks(class_dict, compiled_kit)` — a KF-5-owned pure
data-enrichment that stamps the block onto `class_dict["skills"][i]` under an underscore-prefixed
(resolver-ignored) key, so it reaches the on_hit site via `attacker.skills[skill_idx]`. ZERO compiler
edit (KF-4 stays frozen/PASSED), ZERO combat path change. **KF-6 note:** the driver must call
`attach_composition_blocks(class_dict, compiled_kit)` before `run_spatial_fight` (or the gauge renders
all-null). Documented in math note §4.

**DEVIATION 2 — received-side expected is a NAMED GAP (mob skills carry no `_composition`).**
The KF-4 compiler compiles only the 5 player kits, not mobs. Mob skills (from `monster_dict["skills"]`,
KF-3 harvest) carry no `_composition`, so `pct_received` renders with null expected UNTIL the KF-3
monster harvest emits a per-skill monster-attack composition. The received `expected_*`/`pct_*` fields
are PRESENT and guarded-null (KF-6 renders `<amount> (--)` honestly); the field lights up with zero KF-5
change once mob compositions exist. **Named next-lap admission, not a blocker.** (Dealt side — the
load-bearing KF-5 case — is fully wired.)

## BLOCKER — realized damage is ZERO on every compiled kit (conductor must rule)

**This is the one thing I STOPPED on rather than fixing (charter Deviations law: do not make a
combat-logic change to deliver the fields; STOP + report; conductor rules).**

**Finding:** the KF-4 compiler emits the damage effect with **name `"flat_damage"`**
(kit_compiler.py:541), but the resolver processes damage ONLY under **`if name == "damage"`**
(damage_resolver.py:832). `"flat_damage"` is recognized NOWHERE in the resolver or generation. So every
compiled kit's damage effect is silently ignored ⇒ **realized per-hit `amount` == 0.0 for all hits** ⇒
the compiled fighters deal zero realized damage (win_rate 0.00, mobs never die — visible in BOTH the
KF-4 smoke and mine).

**Why KF-4's Gate-2 didn't catch it:** the KF-4 `has_damage_base` assert reads the COMPOSITION (does a
base exist?), and the KF-4 fight assert is "runnable / finite damage" — and 0.0 IS finite. KF-5 is the
FIRST consumer to read the realized per-hit magnitude against an expected, so it is the first thing to
surface it. Note this contradicts the KF-4 math note's OWN stated mechanism (§0: "the RDR numbers flow
into the existing legacy flat-magnitude path damage_resolver.py:879-881" — that path is gated by
`name=='damage'`, which `flat_damage` never enters).

**Proof the KF-5 gauge is correct (the defect is upstream, not mine):** diagnostically renaming
`flat_damage → damage` in a THROWAWAY class_dict (NOT committed) makes bonestorm's realized `amount ≈
2115.6`, `expected 1542`, `pct 137.2`, `pct_premit 82.3`, `expected_premit 2570` — pct band [96.2,
141.8], mean 118.6 = exactly the max-leaf(309)÷mean(257) ratio × ±20% variance. The gauge reads ~100-140%
the instant realized damage is nonzero.

**Consequence for KF-7:** with the live build, the fidelity gauge reads **pct ≈ 0% everywhere** — not
because of source-fidelity drift, but because of this compilation effect-name bug. Matt's watch session
would see a broken gauge (all 0%) that masks the very fidelity the run measures.

**Disposition options (conductor's/Matt's to rule — I do not rule it):**
- **(A)** One-line KF-4 compiler fix: emit effect name `"damage"` not `"flat_damage"`
  (kit_compiler.py:541). This is a combat-logic change (0 → nonzero realized damage) in the frozen
  compiler — needs a separate authorized commit + its own Gate-2 (charter law makes any engine diff
  Gate-2-gated). Smallest, most faithful fix; makes the gauge read true. **My recommendation** —
  but it is NOT mine to make under the charter.
- **(B)** A KF-5-side effect-name normalization (map `flat_damage → damage` at the resolver boundary or
  in `_ResolverSkill`) — but that ALSO changes combat behavior for the compiled path, same Gate-2 gate;
  and it's a semantic shift in the resolver's effect vocabulary (Disc #12). Less clean than (A).
- **(C)** Accept the pct=0 read for this lap as "the gauge honestly showing the compiled kits deal
  nothing" and defer the fix — but this defeats KF-7's purpose (Matt can't read fidelity through an
  all-zero gauge).

I have NOT touched `kit_compiler.py`. My KF-5 diff stands on its own (expected/pct plumbing correct,
determinism proven); it just reads a realized `amount` that is 0 until the upstream effect-name is fixed.

## Gate-2 readiness list (for jack-ryan — checkable claims)

1. **Zero-combat-logic-change:** diff = kf5_expected.py (NEW, pure), replica_frame_emitter.py (additive
   fields + `_finite_opt`), spatial_engine.py (`_kf5_gauge_for_hit` + closure forward + Rider-1
   mirror-sync in a SEPARATE commit), smoke (NEW). No resolver/HP/RNG mutation. `frame_sink=None` path
   byte-identical (gauge only in `_frame_on_hit`, None when sink None).
2. **Determinism / additive-only:** same seed → identical frames; stamped-vs-unstamped differ ONLY in
   gauge-key VALUES (subset proof); strip gauge keys → combat records byte-identical. Reproduce:
   `python3 -m reincarnated.simulation.kit_compiler.smoke_kf5_expected_pct` (the smoke runs the
   determinism check inline).
3. **Non-finite guard (§5):** `_finite_or_none` (sim) + `_finite_opt` (emitter); div-by-zero/absent →
   null. No NaN/inf reachable on the wire.
4. **Pin A (§1):** expected = base_mean × offensive_mult × crit_ev × hit_chance; variance omitted
   (unit mean); hit_chance-in-expected is a deliberate pin (§1.1).
5. **Pin B (§2):** expected_postmit mirrors compute_{physical,elemental}_damage factor-for-factor on the
   mean; buff_dmg_mult/scaling_stat/mitigation read live off resolved state, not re-derived.
6. **Bridge (§4):** attach_composition_blocks = pure class_dict enrichment; `_composition` underscore
   key is resolver-ignored (_ResolverSkill reads only named fields, adapter:97-132); KF-4 untouched.
7. **Rider 1 (isolated `455d76a`):** engine mirror now byte-identical to the authoritative table (26==26);
   byte-neutral to all current traces (Path-1 bypass verified); KF-4 smoke 35/1/1 unchanged.
8. **Rider 2 (folded into `de0090f`):** KF-4 note §0/§6 cites refreshed to `damage_resolver.py:879-881`
   + `spatial_gauntlet/` qualification.
9. **BLOCKER (above):** `flat_damage` effect-name → zero realized damage. NOT a KF-5 defect; NOT fixed by
   me (charter law). Conductor rules the disposition. My gauge is proven correct once realized ≠ 0.

## Reproduce

```
cd ~/Games/reincarnated-engine/src
python3 -m reincarnated.simulation.kit_compiler.smoke_kf4_compiler          # 35 GREEN · 1 RED · 1 GAP
python3 -m reincarnated.simulation.kit_compiler.smoke_kf5_expected_pct       # KF-5 PASS + determinism
```
