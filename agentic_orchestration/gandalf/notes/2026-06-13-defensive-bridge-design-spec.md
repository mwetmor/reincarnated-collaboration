# BC Axis-4 Defensive-Bridge — Design-Spec-as-Math

**Type:** design-spec-as-math (gandalf authors the math; rocket executes the allocator). The fix the sizing ruling sized.
**Date:** 2026-06-13
**Author:** gandalf (story-and-design steward)
**Gated on (now ungated):** `agentic_orchestration/gandalf/notes/2026-06-13-bc-orphan-sizing-ruling.md` (ONE-OFF ratified) — this spec consumes that ruling as its sizing premise.
**Grounded in (read, this session):**
- rocket gen-audit — `reincarnated-engine/src/reincarnated/generation/notes/bc-orphan-lever-inventory-2026-06-13.md` (engine `343c21b`)
- live composer — `bc_target_composer.py` (DefensiveObjective emission, lines 198-201, 414-419, 821-829)
- live allocator — `stat_allocator.py` (`allocate_stats(archetype_tag)`, 270-budget templates)
- live HP/dodge math — `foundation/math_model.py` (`compute_max_hp`, `compute_dodge_chance`)
- live measurement — `simulation/bc_measurement.py` (`_ehp_ratio`, `_avoidance_rate`, `assign_axis4_bin`)
- live combatant fields — `simulation/combatant.py` (`armor`, `dodge_chance`, shield/regen)
- lock baseline — `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.7
**Routes to:** KR → rocket (executes the allocator). jack-ryan guardrails honored as acceptance criteria.
**Empirical "spec done" criterion:** MEASURED Axis-4 bin distribution → 24/24/24/24 across tank/mitigator/dodger/glass on simulated kits, with dodger independently reachable. Substrate evidence, not assertion.

---

## 0. TL;DR

The bridge is **one missing generation-side allocator** that consumes the already-composed `DefensiveObjective`
and lands it on the kit's defensive surface, so Axis-4's already-live measurement reads a real gradient instead
of the element prior. The ruling sized it ONE-OFF; the code confirms the shape and adds precision the ruling
could not have:

- It is **two wires through one allocator**: (W1) an **eHP-gradient wire** — the defensive objective scales/adds
  across HP, mitigation, shield, regen; and (W2) an **avoidance wire** — the defensive objective drives
  `dodge_chance` from the *defensive intent*, not as a dexterity side-effect. Both dead-end at the same missing
  consumer; both have distinct player-consequence (W1 = tank↔glass gradient flat; W2 = dodger bin ABSENT).
- The eHP gradient must be **factored across ≥2 mechanisms per bin** (HP-scale × shield × regen in the
  numerator; mitigation in the denominator) — NOT a single HP slider (guardrail #2).
- The defensive objective is the **AUTHORITY** for the gradient; the element/energy prior supplies the **BASE
  magnitude** it scales — landed as a **multiplier on DERIVED HP** (downstream of the 270-stat budget), so a
  fire-tank and a fire-glass share flavor and diverge on defense without breaking `STAT_BUDGET=270` (guardrail #4).
- The current `_DEF_BIN_OBJECTIVES` targets are **bin EDGES, not centroids** (tank `ehp_ratio_target=5.0` = the
  exact tank threshold) — a latent knife-edge bug the spec corrects: **target centroids with margin.**

This is design-spec-as-math: I fix the gradient shape, the layer factorization, the composition rule, and the
acceptance gates. rocket wires it (which field, which resolver) and runs the calibration sweep against measured
output. The seed numbers below are a **calibration START, not a lock** — Discipline #17 sweeps them to the
measured 24/24/24/24.

---

## 1. What the bridge is (and is not)

**Is:** the single `DefensiveObjective → kit defensive surface` allocator. Reads
`DefensiveObjective(ehp_ratio_target, avoidance_target, preferred_affix, gear_affixes)` — composed today in
`bc_target_composer.py`, consumed by nothing — and lands it on the combatant's defensive fields so the live
`bc_measurement._ehp_ratio` / `_avoidance_rate` read a non-default gradient.

**Is not:** a general allocator-wiring pass (the class path, refuted by the audit — 5 SILENT rows all on Axis-4,
0 elsewhere). Not a sim change (sim side is fully built — `a_shield_absorbed`, `a_premitigation_damage`,
`a_evasion_misses`, `regen_per_sec_est`, `a_incoming_attempts`, `max_hp` all emit). Not the Axis-4 measurement
formula (locked, live). Not the coverage-audit's Bucket-A/B work (separate instrument, separate seam).

**Why one-off is structural, restated against the code:** every other axis reaches the kit through *mechanic
selection* — the composer scores skills, the selected skills carry metadata, the sim measures off executed
skills (closed loop). Axis-4 alone reaches the kit through a *stat objective* that needs an objective→stat
allocator, and that allocator was never built. One mechanism gap, one axis.

---

## 2. The mechanical substrate (what the allocator actually targets)

The ruling named four eHP "layers" abstractly. The code says exactly where each lives. This table is the
allocator's output map:

| Lever | Combatant field today | Sourced from today | eHP role | Bridge action |
|---|---|---|---|---|
| **HP** | `max_hp` = `10000 + vit×75 + str×20` | element/role prior (270-budget vitality) | **numerator** | **SCALE derived HP** by `hp_scale` (defensive authority); base = prior |
| **mitigation** | `armor` = `(str×8 + gear.bonus_armor + t4)×(1+t4%)` | strength + gear affixes | **denominator** (post-mit `damage_taken`) | **ADD** defensive armor (additive, not scale — armor is additive by construction) |
| **shield_pool** | `get_shield_total()` / `absorb_with_shield()` | skill/affix shield effects | **numerator** (`shield_absorbed`) | route shield budget from defensive objective |
| **regen** | HoT / `regen_per_sec_est` | skill/affix regen + lifesteal | **numerator** (`hot_recovered` / `regen×30`) | route regen/lifesteal budget from defensive objective |
| **avoidance** | `dodge_chance` = `min(0.60, 0.05 + dex×0.0015)` | **DEXTERITY only** | **separate scalar** (`avoidance_rate`, gates dodger FIRST) | **ADD** defensive dodge from `avoidance_target`, independent of dex |

**Two facts this table makes load-bearing:**

1. **The implemented eHP folds mitigation into the denominator.** `bc_measurement._ehp_ratio`:
   `eHP = max_hp + shield_absorbed + hot_recovered` (measured) and `damage_taken` is POST-mitigation. The lock's
   `/(1 - mitigation_fraction)` numerator-form **cancels algebraically into the denominator** (proven, sim math
   note `bc-measurement-signal-emission` § 3). **The allocator's internal eHP estimate MUST use the same
   denominator-folded form** so rocket's self-check matches the sim's measurement — else the spec targets a
   formula the acceptance test doesn't measure. The RATIO centroids are identical either way; only the internal
   bookkeeping must agree.

2. **Avoidance is a dexterity side-effect today, not a defensive choice.** `dodge_chance` follows `dex`
   (rogue dex=160 → 0.29; tank dex=20 → 0.08). The dodger bin needs `avoidance_rate ≥ 0.40`. So dodger is
   reachable today only incidentally, by high-offensive-dex kits — never by defensive *intent*. W2 wires
   `avoidance_target` into a defensive dodge contribution so a "dodger"-composed kit reaches the gate regardless
   of its offensive dex.

---

## 3. The eHP gradient math (W1)

### 3.1 Centroids, not edges (the correction)

`assign_axis4_bin` ladder (live, lock-ordered): `if avoidance≥0.40 → dodger; elif eHP_ratio≥5.0 → tank;
elif eHP_ratio<2.0 → glass; else mitigator`. Mitigator is the **residual band** (2.0–5.0, no positive signal).

Targeting bin EDGES (current `_DEF_BIN_OBJECTIVES`: tank=5.0, mitigator=2.0) puts every kit on a knife-edge —
jitter splits the population across the boundary. **Target centroids with margin:**

| Bin | eHP_ratio centroid | Margin to nearest edge | Carried by |
|---|---|---|---|
| **glass** | **~1.3** | 0.7 below the 2.0 glass edge | low everything |
| **mitigator** | **~3.3** | ~1.3–1.7 from both edges | mitigation + lifesteal regen, moderate HP |
| **tank** | **~7.0** | 2.0 above the 5.0 tank edge | HP-scale + mitigation + shield |
| **dodger** | eHP **~2.5** (mitigator band) + **avoidance ≥ 0.45** | avoidance 0.05 above the 0.40 gate | the avoidance wire (W2), NOT eHP |

Dodger's eHP sits *intentionally* in the mitigator band — the avoidance-first ladder routes it to dodger before
the eHP test fires. Dodger is defined by W2, not W1.

### 3.2 The anti-HP-bloat factorization (guardrail #2)

The eHP multiplier `M` for a bin is the product of a numerator gain and a denominator reduction — **each bin
must source `M` from ≥2 distinct mechanisms so no bin is "just more HP":**

```
M  =  hp_scale × (1 + shield_frac + regen_frac)   /   (1 − mitigation)
        └ numerator gain (HP, shield, regen) ┘          └ denom (armor) ┘
```

Calibration SEED (Discipline #17 sweeps to measured 24/24/24/24 — these are a START):

| Bin | hp_scale | mitigation | shield_frac | regen_frac | → M | dominant route |
|---|---|---|---|---|---|---|
| **tank** | 1.8 | 0.45 | 0.40 | 0.25 | 1.8×1.65/0.55 ≈ **5.4** | HP+armor+shield (3-way) |
| **mitigator** | 1.15 | 0.35 | 0.10 | 0.30 | 1.15×1.40/0.65 ≈ **2.5** | armor+lifesteal (denom+regen) |
| **dodger** | 0.9 | 0.10 | 0.0 | 0.10 | 0.9×1.10/0.90 ≈ **1.1** | (eHP modest by design; avoidance carries) |
| **glass** | 0.55 | 0.05 | 0.0 | 0.0 | 0.55×1.0/0.95 ≈ **0.58** | low all (the floor) |

`hp_scale` seeds are the canonical `defensive_vitality_scale` (1.8/1.15/0.9/0.55) rocket found in the
representative-gen script — now given the companion layers that keep them from being HP-bloat. **Acceptance is
not these numbers; acceptance is the measured distribution.** Two bins that hit the same `M` by different routes
(tank via HP+armor, a hypothetical "fortress" via pure armor) are mechanically distinct and BOTH legitimate —
the lock's hybrid-capture table (§ 3.7: Absorber/Regenerator/Thorns) depends on shield/regen/mitigation being
*independently* allocable. The factorization preserves that; a single HP slider would collapse it.

### 3.3 Where M lands

`M` is realized on the combatant as: `max_hp ×= hp_scale`; `armor += defensive_armor_for(mitigation)`;
shield budget and regen/lifesteal budget routed to the shield/HoT effect surface. rocket chooses the field-level
wiring (his seam); the spec fixes that the gradient is **distributed across these channels in the seeded
proportions**, not dumped into HP.

---

## 4. The avoidance gradient math (W2) — the dodger wire

**The independent gate.** `avoidance_rate = (evasion_misses + iframe + stealth + reflection) / incoming_attempts`
(live; iframe/stealth/reflection are lock-deferred → today `avoidance ≈ evasion_misses / attempts`). The dodger
bin requires `avoidance_rate ≥ 0.40` and is tested FIRST in the ladder.

**The wire:** the allocator reads `DefensiveObjective.avoidance_target` (dodger=0.4, mitigator=0.2, tank/glass=0.0)
and lands a **defensive dodge contribution** so the realized `dodge_chance` reaches the target **independent of
offensive dexterity.** Model (seed):

```
dodge_chance_realized  =  min(0.60,  compute_dodge_chance(dex)  +  defensive_dodge(avoidance_target))
```

where `defensive_dodge(0.4)` lifts a non-dex kit from its dex-floor (~0.08) to **≥ 0.45** (margin above the 0.40
gate). The 0.60 engine cap holds. `avoidance_rate` measured in-fight will track realized `dodge_chance` over the
avoidable attack surface; **the acceptance test is the MEASURED `avoidance_rate`, not the set `dodge_chance`** —
because the avoidable-surface fraction (physical vs unavoidable damage) discounts it. Seed `defensive_dodge(0.4)`
high enough that measured `avoidance_rate` clears 0.40 with margin; sweep to confirm.

**Why a SECOND named wire and not folded into W1:** same allocator, same root cause — but distinct
player-consequence. W1 flat = the tank↔glass durability gradient is invisible (every defensive label feels the
same). W2 dead = the **dodger archetype cannot be expressed at all** — the D3 Demon Hunter / D4 Rogue dodge-roll /
PoE Trickster evade-stack fantasy named in the lock's own exemplar table is ABSENT, not flat. Two wires, two
acceptance gates.

---

## 5. The composition rule (guardrail #4) — element prior ↔ defensive objective

**Two sources now write the same stat surface:** the element/role prior
(`stat_allocator.allocate_stats(archetype_tag)` → 270-budget vitality → derived HP) and the new defensive
objective. An unspecified interaction is how the next silent inconsistency is born. The rule:

> **The defensive objective is the AUTHORITY for the eHP gradient; the element/energy prior is the BASE
> MAGNITUDE it scales. The scale is applied to DERIVED HP (downstream of the 270 budget), never to the
> vitality stat (upstream).**

Concretely, **SCALE — not OVERRIDE, not ADD-to-budget:**

- **Not OVERRIDE:** overriding vitality erases the element prior's flavor (a fire-mage's vitality share is part
  of its elemental identity). Rejected.
- **Not ADD-to-budget:** adding vitality points breaks `STAT_BUDGET=270` (the import-time assertion).
  Rejected.
- **SCALE on derived HP:** `max_hp_final = compute_max_hp(vit, str) × hp_scale`. The element prior keeps its
  270-budget vitality (flavor preserved); the defensive scale multiplies the *resulting HP pool* (gradient
  authority). **A fire-tank and a fire-glass share the fire vitality share (flavor) and diverge on the defensive
  axis (intent) — exactly the ruling's cleanest intent, and the only form that preserves the 270 invariant.**

**Mitigation composes ADDITIVELY** (armor is additive by construction: `str×8 + gear + defensive`), so the
defensive objective ADDS its armor contribution on top of the strength-derived base — a high-str archetype keeps
its incidental armor and the defensive objective layers its intent on top. **Shield/regen** are routed budgets
(the kit had ~none defensively before), so they are effectively additive from a zero defensive base. Only HP is
SCALE (because HP has a large prior-driven base that must be preserved as flavor); the other layers ADD (because
their defensive base is ~zero). The spec names this asymmetry explicitly so it is designed, not inherited.

---

## 6. The affix-routing wire (preferred_affix → gear)

`DefensiveObjective.preferred_affix` (`armor_heavy` / `lifesteal_moderate` / `evasion_high` /
`glass_cannon_damage`) and the `gear_affixes` list are composed and **read by nothing** (rocket LC-007; grep
confirms zero consumers outside the composer). `gear_generation.py` has its OWN affix system (`bonus_armor`,
`buff_defense`, lifesteal) that the composer's intent does not drive.

**The wire:** the allocator resolves `preferred_affix` → the matching gear affix budget, so the kit's gear
reinforces its defensive bin: `armor_heavy → bonus_armor`; `lifesteal_moderate → lifesteal/regen`;
`evasion_high → defensive dodge` (the W2 channel); `glass_cannon_damage → offense, minimal defense`. This makes
the eHP/avoidance gradient **coherent across the kit's gear**, not just its base stats — a tank's gear reads as a
tank's gear. rocket maps the affix strings to `gear_generation`'s real affix rolls (his seam); the spec fixes
that the mapping exists and aligns with the bin's eHP/avoidance route from §§ 3–4.

---

## 7. Acceptance criteria (the four guardrails, made measurable)

The spec is NOT done on assertion. Done = MEASURED. The four guardrails as binding gates:

| # | Guardrail | Measurable acceptance |
|---|---|---|
| **G1** (jack-ryan) | Validate against MEASURED Axis-4 | Run BC measurement on simulated kits composed across all four bins → **distribution → 24/24/24/24** (±tolerance from sweep). NOT a "glass takes less damage" intuition-proxy. The orphan survived 3 weeks because nobody read the measured output. |
| **G2** (jack-ryan) | Differentiate via the FOUR layers, NOT HP-bloat | Each non-glass bin sources its `M` from **≥2 distinct mechanisms** (§ 3.2). Audit: no bin reaches its centroid via HP-scale alone; tank uses HP+armor+shield, mitigator uses armor+lifesteal. shield/regen/mitigation independently non-zero where the bin's route requires (preserves the hybrid-capture table). |
| **G3** (gandalf) | Dodger is an INDEPENDENT gate | **MEASURED `avoidance_rate ≥ 0.40` ACHIEVABLE by an evasion-composed kit** (§ 4), checked SEPARATELY — not averaged into "distribution roughly even." A spec that fixes eHP and leaves avoidance near-zero passes a 3-bin check and ships a dead archetype. Dodger has its own gate. |
| **G4** (gandalf) | No regression of the element prior into incoherence | Composition is SCALE-on-derived-HP + ADD-for-armor/shield/regen (§ 5); `STAT_BUDGET=270` assertion still holds; a fire-tank and fire-glass share element flavor (same vitality share) and diverge on defense. Audit a same-element bin pair to confirm flavor-preserved-divergence. |

**Discipline #18 (methodology timing):** if calibrating the `hp_scale`/`mitigation`/`shield`/`regen`/
`defensive_dodge` weights touches a P2/P3/P5 methodology choice, consultation fires **AFTER** a baseline
allocator exists and emits a first measured distribution — not before (OP § 4.2). Consultation-in-the-dark on
the calibration is the failure mode. The empirical "spec done" criterion (G1) gates commit:
recognition → validate → commit.

---

## 8. Scope, lanes, handoff

- **gandalf (this spec):** the gradient math (§ 3), avoidance math (§ 4), composition rule (§ 5), affix-routing
  intent (§ 6), acceptance gates (§ 7). Authored; ungated by the ruling.
- **rocket (executes):** build the single `DefensiveObjective → kit` allocator. Choose the field-level wiring
  (which combatant field, which gear resolver, where in `kit_finalization` the allocator runs). Run the
  Discipline #17 calibration sweep on the § 3.2 / § 4 seeds against MEASURED Axis-4 until 24/24/24/24 + dodger
  reachable. His seam.
- **gamora (parallel, non-blocking):** the 2 GAP-sim rows (Axis-1 mobility reduction, Axis-5 statistical
  resource read) — separable footnote, cannot reclassify Axis-4. Route in parallel; does not gate this spec.
- **jack-ryan (Gate-2):** validates G1–G4 against measured output when rocket returns.
- **Out of scope:** the coverage-audit Bucket-A/B work; iframe/stealth/reflection avoidance sub-mechanisms
  (lock-deferred — today's avoidance is evasion-only); any non-Axis-4 axis.

---

## 9. The player consequence (why this is design work, not a patch)

The BC archive is MAP-Elites: it culls behavioral *duplicates* to preserve diversity. An archive blind to a kit
dimension culls non-duplicates as duplicates — **two kits that differ only on defense look identical to it, and
one dies.** With Axis-4 collapsed: a tank-composed kit and a glass-composed kit with matching
engagement/geometry/tempo collide, one is culled, and the player never sees the variant. With the dodger bin
dead: the evade-stack fantasy is **absent from the entire generated build space.** The genre Diablo and PoE live
on is build diversity along exactly these axes — durability gradient and the dodge-roll archetype. The bridge is
what lets the archive *see* that diversity so it stops flattening it. That is the player consequence, and it is
why the fix is sized as a design-spec-as-math and validated against MEASURED bins, not an intuition proxy.

---

**Signed:** gandalf, 2026-06-13
**For:** the BC Axis-4 defensive-bridge design-spec-as-math — the single `DefensiveObjective → kit` allocator,
as two wires (eHP gradient + avoidance), factored across the four eHP layers to avoid HP-bloat, composed with the
element prior as SCALE-on-derived-HP, with affix-routing, and four MEASURED acceptance gates (24/24/24/24 +
independent dodger reachability). Consumes the ONE-OFF sizing ruling; routes to rocket for execution.
