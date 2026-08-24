# P0-a — Kit-substrate clusterability verification (VFX archetype-binding run)

**Date:** 2026-08-23
**Author:** elrond (data steward), invoked as named sub-agent by gandalf (`RUN-CONDUCTOR`)
**Run:** VFX ARCHETYPE-BINDING RUN, charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` § 4 (P0-a), ledger L-3
**Mode:** READ-ONLY verification. No schema change, no curation write, no DB mutation. All numbers below are live reads taken this date.
**Gate semantics briefed:** VOTABLE → P1 · GAP → HALT to Matt. Honorable fallback = pause, never improvise a taxonomy (Discipline #41).

---

## VERDICT — **VOTABLE**

The kit corpus **is** in votable shape for a substrate-led archetype clustering, **provided the vote runs against the canon corpus (`corpus.db`) and NOT against the emission-line bundles.** Every archetype name the vote would produce is an attested substrate value; nothing needs hand-enumeration.

The verdict carries five bounds (§ 5) and one hard prohibition (§ 5.5). The prohibition is the load-bearing part: there is a second, wrong corpus sitting on disk that *looks* like the kit corpus and is arity-2 degenerate. If P1 clusters that one it will produce a two-class "taxonomy" that is the emission scaffold wearing an archetype costume.

---

## 1 · Corpus of record — identification + evidence

Three of our-side kit corpora exist on disk. They are not versions of each other; they are different lineages. Naming which is current-of-record is the first half of this verification.

### 1.1 The corpus of record

**`agentic_orchestration/research/curated/corpus.db`** — schema `v2.x` (latest `corpus_schema_meta` stamp `gd-displayname-bridge-2026-07-26/M4`, 2026-07-26; ratified baseline `v1.1-verified`, md5 `50df15b776ad5b0da93fe90cdee1163d`, 2026-07-19).

| Layer | Table | Rows |
|---|---|---|
| Kit identity | `canon_corpus` | **590** (553 `active` / 37 `parked`) |
| Kit mechanical key | `canon_engine_key` | 590 (**568** `row_class='combat-kit'`) |
| Active combat-kit denominator | `canon_corpus ⋈ canon_engine_key` | **531** |
| Mapped skill entries | `kit_mapping.mapping_json.skills[]` | **1,224** across 574 kits |
| Per-skill delivery geometry | `skill_geometry_band` | **490** rows across **265** kits |
| Skill name lists | `canon_corpus.core_skills` | 573 / 590 = 97.1% |
| Consolidated view | `kit_master` | 574 |

**Why this is current-of-record — the engine says so in code.** `reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_compiler.py` (KF-4, landed 2026-07-23) opens:

> *"No generation PlayerClass is built; the kit's identity is the canon record, not a BC-coordinate draw (**the retired label-synthesis**)."*

The compiler reads corpus geometry directly and owns two authored maps that are the corpus→engine geometry bridge:

- `_DELIVERY_TO_RICH` — `skill_geometry_band.delivery_class` → rich geometry_type (7 keys: projectile/beam/zone/motion/aura/summon_delegate/melee_arc)
- `_RICH_TO_SPATIAL` — rich geometry_type → the engine's 6-type spatial primitive (25 keys incl. `whirlwind`, `vortex_pull`, `dash_attack`, `chain`, `fork`, `totem`, `ring`, `placed_lane`, `blink`)

That is a live, in-code join from the corpus's VFX-shaped vocabulary to the engine's spatial vocabulary. A VFX archetype table keyed on that vocabulary lands on compiled kits **by construction** — the compiler *is* the join. This is the strongest single argument for the VOTABLE verdict.

Caveat of record: `PILOT_KITS` in the compiler is width **4** (`d2-firewall-sorc`, `d2-fire-sorc`, `poe1-cyclone`, `poe2-bonestorm`) + 1 `HELD_KITS` (`gd-flames-of-ignaffar-purifier`). The *architecture* is corpus-as-identity; the *compiled population* is 4. The vote is not blocked by that (the vote is over the corpus, not over compiled output), but no one should read "corpus is kit identity" as "590 kits are compiled today."

### 1.2 The second corpus — the emission line (NOT of record for this run)

`reincarnated-engine/data/emission_registry.db` `emission_runs` (13 rows, latest 2026-07-03) registers the current emission line. Two artifacts:

| Artifact | Kits | Skill rows | Written | Status |
|---|---|---|---|---|
| `src/reincarnated/output/w3_batch1_bundle.json` | 700 | **8,400** | 2026-07-03 | `schema_status: LOCKED`, `stage-2-registered`, run `2d32195d…` |
| `src/reincarnated/output/one_realm_demo_bundle_w3_flavor.json` | 54 | **648** | 2026-07-22 | `schema_status: DRAFT-pending-drax-handshake` |

**The 700 "kits" are not 700 kits.** `archetype_tag` has **7 distinct values** at exactly 100 rows each — 7 BC coordinates × 100 statistical samples. It is a balance **fixture bank**, not a content corpus. Its 8,400 skill rows carry **48 distinct skill names** (template strings: `"Physical Chain A - T1 Primary Attack"`) and **20 distinct `effects` strings**.

The 54-kit demo bundle is the demo-facing assembly (kit source `reincarnated-loadout/data/cycle-14-wave-5-season-001/classes/`, 54 files, verified identical shape). Its 648 skill rows carry 96 distinct template names and — despite the `_w3_flavor` filename — **`skill.flavor_text` = 0 / 648 non-null**. Kit-level flavor landed (54/54); the skill-grain flavor pass did not. Recorded as an incidental finding, not a P0-a input.

### 1.3 The third corpus — `kit_space` (stale; named so it is not rediscovered)

`reincarnated-engine/data/kit_space/kits/*.json` — **411** kit files, **3,612** skill rows, last write 2026-06-13 (commit `22478c20`). The EAA-chain continuous kit space. Materially richer than the emission bundles (`geometry_type` 83.3% populated, **20** distinct values; `spatial_geometry_type` 18.8%; `role` 100%, 10 values; LLM-authored skill names + effects prose on 603 / 3,612 = 16.7%).

It is off **both** live lines — superseded on the identity side by corpus-as-identity (KF-4) and on the emission side by the W3/one-realm line. Named here so a future reader does not find its 20-value geometry vocabulary and mistake richness for currency.

---

## 2 · Field coverage for clustering — the corpus of record

### 2.1 Per-SKILL grain — `skill_geometry_band` (denominator = 490 rows)

```sql
select count(*) rows_total,
       sum(delivery_class is not null), sum(motion_signature is not null),
       sum(origin is not null), sum(width_band is not null),
       sum(range_band is not null), sum(speed_band is not null),
       sum(cadence_class is not null), sum(exact_json is not null)
from skill_geometry_band;
-- 490 | 476 | 352 | 490 | 37 | 181 | 25 | 139 | 0
```

| Axis | Non-null | % of 490 | Distinct | Modal value (share of 490) | Clusterable? |
|---|---:|---:|---:|---|---|
| `delivery_class` | 476 | **97.1%** | **7** | `zone` 115 (23.5%) | **YES — primary axis** |
| `motion_signature` | 352 | **71.8%** | **14** | `straight_line` 71 (14.5%) | **YES — primary axis** |
| `range_band` | 181 | 36.9% | 6 | `melee` 93 (19.0%) | partial — annotation |
| `cadence_class` | 139 | 28.4% | 4 | `cooldown` 77 (15.7%) | partial — annotation |
| `width_band` | 37 | 7.6% | 3 | `wide` 34 (6.9%) | **NO — too thin** |
| `speed_band` | 25 | 5.1% | 4 | `fast` 17 (3.5%) | **NO — too thin** |
| `origin` | 490 | 100% | **1** (`self`) | `self` (100%) | **NO — DEGENERATE** |
| `exact_json` | 0 | **0.0%** | 0 | — | **NO — never populated** |

Full vocabularies (attested, no invention):
- `delivery_class` — zone 115 · projectile 97 · melee_arc 77 · aura 71 · summon_delegate 53 · motion 47 · beam 16 · NULL 14
- `motion_signature` — straight_line 71 · ground_place 63 · point_strike 56 · fan_spread 49 · burst_around_self 37 · orbit_fixed 22 · arc_sweep 21 · chain_hop 10 · blink_translate 8 · lane_place 6 · fork_split 4 · ricochet_return 2 · leap_arc 2 · inward_pull 1 · NULL 138

**Joint occupancy `delivery_class × motion_signature` — 20 non-empty cells:**

```
aura / NULL              71     motion / straight_line   15
zone / ground_place      63     NULL / NULL              14
melee_arc / point_strike 56     beam / chain_hop         10
summon_delegate / NULL   53     zone / fan_spread         8
projectile/straight_line 50     motion / blink_translate  8
projectile / fan_spread  41     zone / lane_place         6
zone/burst_around_self   37     beam / straight_line      6
motion / orbit_fixed     22     projectile / fork_split   4
melee_arc / arc_sweep    21     projectile/ricochet_return 2
                                motion / leap_arc         2
                                zone / inward_pull        1
```

That table read aloud is already an archetype list. Nothing in it was enumerated by hand.

### 2.2 Per-KIT grain — `canon_engine_key` (denominator = 568 combat-kit rows)

| Axis | Non-null | % of 568 | Distinct | Modal value |
|---|---:|---:|---:|---|
| `delivery_value` | 557 | **98.1%** | **9** | `at-target` 303 (53.3%) |
| `geometry_value` | 519 | **91.4%** | **15+** | `ground_targeted_circle` 138 (24.3%) |
| `cell_key` | 563 | 99.1% | — | — |

- `delivery_value` — at-target 303 · projectile 110 · self-origin 90 · beam 19 · aura-pulse 14 · orbit 11 · melee 5 · other 3 · line 2 · NULL 11
- `geometry_value` — ground_targeted_circle 138 · circle 68 · single_target 52 · totem 49 · multi_projectile 41 · melee_strike 37 · chain 28 · vortex_pull 19 · dash_attack 18 · whirlwind 15 · cone 11 · line 9 · ring 8 · aura 8 · (NULL 49) · tail

`geometry_value` is the richest VFX-discriminative categorical in the whole data surface: 91.4% populated at arity 15+, with values that *are* VFX descriptions (`whirlwind`, `vortex_pull`, `dash_attack`, `chain`, `totem`, `ring`, `cone`).

### 2.3 Coverage of the per-skill layer against the corpus

| Measure | Value |
|---|---|
| Kits with ≥1 banded skill | 265 / 590 = 44.9% |
| **Active combat kits with ≥1 banded skill** | **227 / 531 = 42.7%** |
| Banded skills / mapped skill entries | **490 / 1,224 = 40.0%** |
| Per-kit band counts | 1 skill: 97 kits · 2: 125 · 3: 31 · 4: 10 · 5: 2 |
| `derivation` | `dossier-prose` **490 / 490 = 100%** |
| `band_conf` | `0.80` on **490 / 490** — uniform |

The per-skill layer is real but **thin and shallow**: ~1.85 banded skills per covered kit, and it covers 42.7% of the active combat roster. The other 57.3% resolve at kit grain only (`delivery_value` / `geometry_value`, 98.1% / 91.4%).

---

## 3 · Field coverage — the emission line (why it is excluded)

`w3_batch1_bundle.json`, 8,400 skill rows:

| Field | % non-null | Distinct | Modal share |
|---|---:|---:|---:|
| `geometry` | 100% | **2** (`single_target` 4800 / `large_aoe` 3600) | 57.1% |
| `spatial_geometry_type` | **0.0%** | 0 | — |
| `effect_category` | 100% | 4 | 33.3% |
| `role` | 100% | 4 | 33.3% |
| `triggers` | 100% | **1** (`["on_cast"]`) | 100% |
| `effects` | 100% | 20 strings | 15.7% |
| `name` | 100% | 48 template strings | 4.8% |
| `is_dot` | 100% | **1** (`False`) | 100% |
| `terrain_reactive` | 100% | **1** (`False`) | 100% |
| `cc_effect`, `cc_duration_s`, `cc_slow_magnitude` | **0.0%** | 0 | — |
| `proxy_count/_power_per/_duration_s/_spawn_cadence_s/_geometry/_max_active/_acquisition` | **0.0%** | 0 | — |
| `hybrid_pattern`, `magnitude_pattern`, `stackability`, `layer2_trigger`, `scaling_pattern`, `capstone_strategy`, `prerequisite_skill` | **0.0%** | 0 | — |

`one_realm_demo_bundle_w3_flavor.json`, 648 rows: same shape — `geometry` arity 2, `spatial_geometry_type` **0 / 648**, `triggers` arity 1, `color_value` arity 1, `flavor_text` 0 / 648.

**Across both artifacts: `spatial_geometry_type` is 0 / 9,048 skill rows.**

**And the two geometry-ish fields contradict each other.** Joint `(role, geometry, effect_category)` on batch-1:

```
('primary_attack',  'single_target', 'single_target_damage')  1600   consistent
('secondary_attack','single_target', 'aoe_damage')            1600   CONTRADICTS
('primary_attack',  'large_aoe',     'single_target_damage')  1200   CONTRADICTS
('secondary_attack','large_aoe',     'aoe_damage')            1200   consistent
('control',  'single_target','control') 800 · ('support','single_target','support') 800
('control',  'large_aoe',    'control') 600 · ('support','large_aoe',    'support') 600
```

**2,800 / 8,400 = 33.3% of rows** carry a `geometry` that disagrees with its `effect_category`. The two fields are assigned independently by the scaffold; neither is a trustworthy delivery-geometry read. Clustering this substrate returns at most 8 cells, and 1 in 3 of them is internally incoherent. That is the scaffold, not a taxonomy.

---

## 4 · Gap classes (named, so P1 does not re-discover them)

| Class | What | Numbers |
|---|---|---|
| **Degenerate axis** | `skill_geometry_band.origin` | 100% populated, **arity 1** (`self`). Drop from the axis set — it discriminates nothing. |
| **Degenerate axis (emission line)** | `triggers`, `color_value`, `is_dot`, `terrain_reactive`, `composition_mode`, `investment_points` | each arity 1 at 100% |
| **Never-populated** | `skill_geometry_band.exact_json` / `exact_source_type` | 0 / 490. Documented in the DDL as a downstream legolas Mode-B datamine dependency; NULL at apply, still NULL. |
| **Never-populated (emission line)** | `spatial_geometry_type` | **0 / 9,048** — the schema slot exists on every emitted skill row and has never once been written by the emission line |
| **Sub-threshold** | `width_band` 7.6% · `speed_band` 5.1% | usable as annotation on the rows that have them; not as clustering axes |
| **Partial** | `range_band` 36.9% · `cadence_class` 28.4% | secondary / tie-break only |
| **Coverage gap** | per-skill bands cover 42.7% of active combat kits, 40.0% of mapped skills | the residual binds at kit grain, not skill grain |
| **Uniform-confidence** | `band_conf` = 0.80 on 490/490; `derivation` = `dossier-prose` on 490/490 | confidence cannot discriminate; every band is a prose read, none datamined |
| **Freetext** | `origin` is declared free-TEXT with a documented (uncheckd) vocabulary | moot here — it is degenerate anyway |

Incidental (not P0-a inputs, filed because they were found): skill-grain flavor never landed on the demo bundle (`flavor_text` 0/648, 96 template names) despite the `_w3_flavor` filename and the 2026-07-22 wave; `kit_space` carries a 20-value `geometry_type` vocabulary at 83.3% that no live line consumes.

---

## 5 · Bounds on the VOTABLE verdict

**5.1 — The vote runs at two grains, and P1 must say which row it is voting.** Per-skill (490 rows, `delivery_class` × `motion_signature`) is the archetype-shaped grain. Per-kit (568 rows, `delivery_value` × `geometry_value`) is the coverage-complete grain. They are not interchangeable and must not be silently unioned.

**5.2 — 57.3% of active combat kits have no per-skill band.** T-K coverage at skill grain will top out near 40% of mapped skills on today's substrate. The residual is bindable at kit grain. This is a *scope* bound, not a votability failure — but P4 must not claim skill-grain coverage it does not have.

**5.3 — All 490 bands are prose-derived at uniform confidence 0.80.** A P3 canonical-reference selection resting on a band is resting on a dossier prose read, not a datamine. Fine for a VFX archetype (readability is the criterion, not numeric fidelity) — but say so in T-A's provenance column rather than letting `band_conf` imply measurement.

**5.4 — `origin` is degenerate; `width_band` / `speed_band` / `exact_json` are below threshold.** Ruled out here with numbers so P1 does not re-litigate them. Documenting the negative result is the point (methodology step 5).

**5.5 — HARD PROHIBITION: do not vote the emission bundles.** `w3_batch1_bundle.json` and `one_realm_demo_bundle*.json` are arity-2 on geometry, 0.0% on `spatial_geometry_type`, and internally contradictory on 33.3% of rows. A cluster run against them yields exactly two classes and would present the emission scaffold as a substrate verdict. If a future beat needs T-K bound to *emitted* rows rather than corpus rows, that is a **new** P0 question and it fails today.

---

## 6 · P1 method recommendation (recommendation only — P1 is not this invocation)

**Universe.** `canon_corpus` where `roster_status='active'` ⋈ `canon_engine_key` where `row_class='combat-kit'` (531 kits) ⋈ `skill_geometry_band` (490 rows / 227 of those kits).

**Axes.**
- *Primary (skill grain):* `delivery_class` (97.1%, 7v) × `motion_signature` (71.8%, 14v) — 20 attested joint cells.
- *Secondary (kit grain, for the 57.3% unbanded):* `delivery_value` (98.1%, 9v) × `geometry_value` (91.4%, 15+v).
- *Annotation only, never a cluster axis:* `range_band`, `cadence_class`.
- *Excluded with cause:* `origin` (arity 1), `width_band` (7.6%), `speed_band` (5.1%), `exact_json` (0%).

**Grouping approach — contingency lattice, not distance clustering.** These are nominal categoricals with no metric; k-means / hierarchical distance on one-hot vectors would smuggle in an arbitrary similarity function, which is hand-imposition wearing a math hat. The right instrument is a **joint-frequency lattice over the categorical cross-product with a declared minimum-support cut**, then:

1. Enumerate occupied cells (20 at skill grain today).
2. Merge only where the engine's **already-authored** `_RICH_TO_SPATIAL` map collapses two cells to the same spatial primitive — that map is existing engine truth, so merging by it is substrate-led, not invented.
3. Report low-support and singleton cells (`zone/inward_pull` n=1, `motion/leap_arc` n=2, `projectile/ricochet_return` n=2) **as their own classes**, not force-merged into a neighbour. Discipline #41: a cluster of one is a finding, not an error.
4. `NULL`-motion cells (`aura/NULL` 71, `summon_delegate/NULL` 53) are their own class — the NULL is informative (auras and summons have no path signature), not missing data to be imputed.

**External-validity check (methodology step 3).** Cross the emergent labels against two independent authored vocabularies neither of which was written for this run: `kit_compiler._RICH_TO_SPATIAL` (25 keys) and `canonical/sidecars/emit_substrate_registry.py` geometry palette. Agreement is evidence the grouping is about form, not about the reading lens. Disagreement is the finding to report, not to file down.

**Falsifiers to pre-register (methodology step 6).** (a) If ≥3 archetype cells collapse to the same `_RICH_TO_SPATIAL` primitive *and* to the same reference imagery at P3, the taxonomy is over-split. (b) If any archetype's member kits span >4 `delivery_value` classes, the cell is under-split. (c) If the 227 banded kits' archetype distribution differs materially from the 304 kit-grain-only kits' `geometry_value` distribution, the banded subset is not representative and T-K's skill-grain half is biased.

---

## 7 · Evidence index

- `agentic_orchestration/research/curated/corpus.db` — `canon_corpus`, `canon_engine_key`, `skill_geometry_band`, `kit_mapping`, `kit_master`, `corpus_schema_meta` (all read-only)
- `reincarnated-engine/data/emission_registry.db` — `emission_runs` (13 rows)
- `reincarnated-engine/src/reincarnated/output/w3_batch1_bundle.json` (700 kits / 8,400 skills)
- `reincarnated-engine/src/reincarnated/output/one_realm_demo_bundle_w3_flavor.json` (54 kits / 648 skills)
- `reincarnated-engine/src/reincarnated/output/one_realm_demo_bundle.json` (54 kits / 648 skills, 2026-07-03)
- `reincarnated-loadout/data/cycle-14-wave-5-season-001/classes/` (54 files — the demo bundle's kit source)
- `reincarnated-engine/data/kit_space/kits/` (411 files / 3,612 skills) + `kit_space/README.md`
- `reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_compiler.py` — `_RICH_TO_SPATIAL`, `_DELIVERY_TO_RICH`, `PILOT_KITS`, `HELD_KITS`, module docstring
- `reincarnated-engine/src/reincarnated/canonical/sidecars/emit_substrate_registry.py` — geometry palette primitives
- `canonical/reap-die-rise-engine/2026-06-06-atomic-substrate-registry.md` § 1.5 (skill geometry palette)
- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` — PART F roster of record; 2026-07-19 / 07-20 / 07-22 / 07-24 SESSION-DELTAs

Census scripts were scratch (`/tmp`), read-only, and are reproducible from the queries pasted inline above.

---

*Filed by elrond, 2026-08-23, for VFX archetype-binding run P0-a. Verdict: **VOTABLE**, bounded by § 5, with § 5.5 as a hard prohibition. Returned to gandalf (`RUN-CONDUCTOR`) for the P1 gate.*
