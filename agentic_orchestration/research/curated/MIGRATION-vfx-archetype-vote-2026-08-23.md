# MIGRATION — VFX archetype vote (P1), 2026-08-23

**Schema version stamp:** `vfx-archetype-vote-2026-08-23/P1`
**Author:** elrond (data steward), named sub-agent of gandalf (`RUN-CONDUCTOR`)
**Run:** VFX ARCHETYPE-BINDING RUN — charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`, phase P1, ledger L-7 / L-8 / L-9
**Script:** `../scripts/vfx_p1_archetype_vote_2026_08_23.py` (transactional, idempotent, additive)
**DB:** `agentic_orchestration/research/curated/corpus.db`
**Class:** ADDITIVE. Four new tables. **No existing table, column, view, trigger or row is altered or deleted.**

---

## 1 · Backups + reversibility

| Artifact | md5 | State |
|---|---|---|
| `corpus.db.pre-vfx-p1-20260824T031600Z-backup` | `fd9d1adb6ab52e0af317243e3095df63` | **TRUE PRE-STATE** — authoritative restore point. Verified `select count(*) from sqlite_master where name like 'vfx%'` = 0. |
| `corpus.db.pre-vfx-p1-20260824T031718Z-backup` | `13dbbeeff59c00231f2e945a59c7f145` | Intermediate (after run 1, before the coverage-accounting amendment that added the `skill_ordinal = -2` exception class). Retained as evidence, not a restore target. |

`pragma integrity_check` = **ok** post-migration.

**Reversibility.** Two independent routes. (a) Restore the true-PRE backup. (b) Additive-only removal:
`drop table vfx_archetype; drop table vfx_archetype_member; drop table vfx_vote_merge_log; drop table vfx_vote_falsifier;`
— nothing else in the DB references them. The script is idempotent: re-running deletes and rebuilds
only rows carrying `vote_run = 'vfx-archetype-vote-2026-08-23'`, so a second vote run can land beside
this one without collision.

**ADR-004.** No engine-side change. Engine telemetry, engine source, `kit_compiler.py` and its two maps
were read ONLY. Star-lord's MIGRATION docs are unaffected. Two cross-seam FINDINGS are filed in § 6 for
routing via knight-rider; neither is acted on here.

---

## 2 · What landed

| Table | Rows | Purpose |
|---|---:|---|
| `vfx_archetype` | **27** | The archetype table. One row per attested axis value. |
| `vfx_archetype_member` | **1,158** | Total membership accounting: 1,138 skill rows + 20 kit-level exception sentinels. |
| `vfx_vote_merge_log` | 5 | Every merge considered, its claimed authority, and the decision. |
| `vfx_vote_falsifier` | 3 | The P0-a pre-registered falsifiers with as-executed outcomes. |

All four are keyed on `vote_run` so future votes are additive rather than destructive — the schema
records votes, not "the answer."

### Schema notes (design rationale)

- **`vfx_archetype.archetype_id` is the axis value verbatim.** Not a mint, not a synthetic id. If the
  substrate's vocabulary changes, the archetype id changes with it and the drift is visible rather than
  hidden behind a stable surrogate key. Discipline #14 spirit: no semantic packing into ids.
- **`vfx_archetype_member` preserves `geometry_value_raw` / `motion_signature_raw` / `delivery_class_raw`**
  alongside the assignment. The curation is fully reproducible from the preserved raw columns; the
  transformation is a projection, never a rewrite.
- **`engine_spatial_primitive` is annotation, and the column comment says so in the DDL.** It records
  what `_RICH_TO_SPATIAL` would do without licensing anyone downstream to do it (see § 4, M-2).
- **`unassignable_reason` is mandatory prose, not a code.** Every non-assignment states its own cause.
- **Negative results are first-class rows**, not prose in a note that gets lost: `vfx_vote_merge_log`
  carries the four merges that were considered and NOT performed, with the reasoning that killed each.

---

## 3 · Method as executed — and one correction to P0-a

**Universe.** `canon_corpus.roster_status = 'active'` ⋈ `canon_engine_key.row_class = 'combat-kit'` = **531 kits**. Unchanged from P0-a § 6.

**Grain.** SKILL. One row per `kit_mapping.mapping_json.skills[]` entry inside the universe = **1,138 rows over 511 kits**.

### 3.1 CORRECTION TO P0-a — the axis changed, for cause

P0-a § 6 recommended `skill_geometry_band.delivery_class × motion_signature` as the primary axis pair.
That recommendation rested on an **incomplete census**: P0-a counted `kit_mapping.mapping_json.skills[]`
at 1,224 entries but never censused the per-skill FIELDS inside those entries. Doing so at P1 found:

```
kit_mapping.mapping_json.skills[]  — 1,224 entries, field coverage:
  source_skill       1,224  100.0%
  geometry_value     1,209   98.8%   <- 28 distinct values
  element_primary    1,224  100.0%
  element_secondary  1,224  100.0%
  ailments           1,224  100.0%
  delivery_notes     1,224  100.0%
```

`geometry_value` here is **the field the engine reads first**. From `kit_compiler.py`:

```python
def _rich_geometry_for_skill(skill: SkillRow) -> str:
    """The rich geometry_type for a compiled skill: mapping geometry_value FIRST (anchored, §3.1),
    delivery_class table as fallback.
    """
    if skill.geometry_value:
        return skill.geometry_value
    if skill.delivery_class and skill.delivery_class in _DELIVERY_TO_RICH:
        return _DELIVERY_TO_RICH[skill.delivery_class]
    return "single_target"
```

and `kit_reader.py` line 37 annotates the field: `geometry_value  # rich geometry_type from mapping (authoritative when present)`.

So P0-a nominated the engine's **fallback** as the primary axis while the engine's **authoritative**
field sat un-censused at 2.5× the coverage. The axis is corrected here:

| | P0-a recommended axis | P1 as-executed axis |
|---|---|---|
| Field | `skill_geometry_band.delivery_class` | `kit_mapping…skills[].geometry_value` |
| Coverage (in universe) | 407 / 1,138 = 35.8% | **1,135 / 1,138 = 99.7%** |
| Arity | 7 | **27** |
| Engine standing | fallback (`_DELIVERY_TO_RICH`) | **authoritative (§3.1)** |

**The correction is strictly better on every P0-a criterion** — coverage, engine-anchoring, and
discriminative power. It also dissolves P0-a bound § 5.1/§ 5.2 (the two-grain split): there is no
kit-grain residual, because the authoritative field is itself per-skill at 99.7%. The P0-a bounds
that survive are § 5.3 (prose derivation) and § 5.5 (the emission-bundle prohibition, untouched).

### 3.2 The refinement axes are functionally determined by the corrected axis

Joining `skill_geometry_band` on `(kit_id, skill_ordinal)`:

- `geometry_value → motion_signature`: **305 joined rows, 22 archetypes, purity 1.000 — zero exceptions.**
  Every archetype carrying banded members has exactly ONE motion_signature.
- `geometry_value → delivery_class`: **407 joined rows, 25 archetypes, purity 1.000 — zero exceptions.**

The corrected axis **strictly refines** both P0-a axes: `zone` fans out to 5 geometry_values;
`burst_around_self` to 2; `straight_line` to 5; `point_strike` to 2. Knowing `geometry_value` determines
delivery and motion; the converse fails. Both are therefore carried as ANNOTATION columns, never as
split axes (merge-log M-4).

**This also explains a weak result P1 found and discarded.** An early bridge attempt used the
KIT-level `canon_engine_key.geometry_value`, and produced modal agreement of only 20–83% (most cells
30–60%) — apparently a broken bridge. It was a grain error on my side, not a substrate defect: the
kit-level column describes a kit's dominant geometry, while bands are per-skill. At the correct grain
the agreement is exact. Recorded so a future lap does not re-derive the false negative.

---

## 4 · Merge log — five merges considered, **zero performed**

L-9 licenses merges only where the engine's own join already collapses the cells. Applied honestly,
it licenses none.

| # | Candidate merge | Claimed authority | Decision | Why |
|---|---|---|---|---|
| **M-1** | Collapse cells across `delivery_class` | `_DELIVERY_TO_RICH` (7 keys) | **NOT-LICENSED** | The map is **injective** over its 7 attested keys (7 → 7 distinct rich values). It collapses nothing. It also takes no motion input, so it can neither merge nor split within a class. |
| **M-2** | Collapse archetypes sharing a spatial primitive | `_RICH_TO_SPATIAL` (25 → 5) | **REJECTED** | Would merge 25 archetypes into 5 (`circle`←6, `none`←6, `line`←6, `point`←5, `cone`←2), erasing every VFX distinction the substrate attests. See § 4.1. |
| **M-3** | Fold `orbit` into `whirlwind` (both attest `orbit_fixed`) | none — no engine join maps `orbit` | **NOT-LICENSED** | `orbit` (n=18, 18 kits) is absent from `_RICH_TO_SPATIAL`. Merging on a shared *refinement* value would be hand-imposition; the substrate attests two distinct geometry_values. Kept separate; the map gap is filed as finding F-1. |
| **M-4** | Split archetypes by `motion_signature` | measurement, not a join | **NOT-LICENSED** | Purity 1.000 (§ 3.2). Splitting on a functionally-determined refinement yields no new classes. |
| **M-5** | Fold the 3 `geometry_value`-NULL skills into `single_target` | `_rich_geometry_for_skill` terminal default | **REJECTED** | The engine's `return "single_target"` is a last-resort default reached when BOTH the mapping value and the delivery fallback are absent. **A default is not an attestation.** Listed unassignable instead. |

### 4.1 Why `_RICH_TO_SPATIAL` is not the merge authority (M-2, the load-bearing call)

P0-a § 6 step 2 named `_RICH_TO_SPATIAL` as the merge authority. Executing it revealed the map runs the
wrong direction for this purpose, and the engine's own code says so:

- Its in-code comment declares its purpose: *"the compiler asserts against the SPATIAL value the engine
  will derive at run time"* — it is the **hit-gauge** primitive, deliberately lossy (25 → 5).
- The engine keeps the rich vocabulary as the **identity** layer: `_rich_geometry_for_skill` returns the
  RICH value as the skill's `geometry_type`; the spatial collapse happens only at `CompiledKit.primary_geometry`,
  for gauge assertion. The engine maintains both **because** spatial is lossy.
- Therefore: the engine's identity vocabulary is the rich keyspace, and the archetype axis already lives
  in it. The merge authority, correctly read, is the **identity map** — it licenses no merge at all.

Using the lossy gauge as identity authority would invert the map's purpose and hand back a 5-class
"taxonomy" that is the hit-gauge wearing an archetype costume — the same failure mode § 5.5 of P0-a
named for the emission bundles, arriving by a different road.

**Consequence for the run:** no merge was hand-waved through, and no class was hand-imposed. The
HALT condition (charter § 4 P1) is **not met**.

---

## 5 · Coverage accounting — total, with every exception named

**Skill grain (denominator 1,138 in-universe mapping skill entries):**

| | Rows | % |
|---|---:|---:|
| Assigned to an archetype | **1,135** | **99.7%** |
| Unassignable — `geometry_value` NULL *and* no `delivery_class` for the engine fallback | 3 | 0.3% |

The three: `gd-blight-fiend-ritualist#0` (Summon Blight Fiend), `gd-pet-conjurer#0` (Summon Briarthorn +
Summon Familiar), `gd-trozan-druid#1` (Wind Devil). All three kits carry a second, assigned skill, so no
kit is lost to them.

**Kit grain (denominator 531 active combat kits):**

| | Kits | % |
|---|---:|---:|
| ≥1 skill assigned | **511** | **96.2%** |
| No `kit_mapping` row at all (sentinel `skill_ordinal = -1`) | 6 | 1.1% |
| `kit_mapping` row present, `skills[]` an EMPTY array (sentinel `skill_ordinal = -2`) | 14 | 2.6% |

511 + 6 + 14 = 531, asserted in-script.

- **The 6:** `chr-crown-proc-engine`, `di-druid-pvp-cc-stack-2026`, `la-destroyer-gravity-compression`,
  `la-destroyer-gravity-force`, `la-destroyer-gravity-impact`, `la-destroyer-vortex-gravity`.
- **The 14** (finding F-2 — these are structurally complete but skill-empty; `motion_frame`, `scaffold`,
  `t4_doors`, `resource_economy`, `trigger_grammar` all present, `skills: []`):
  `gd-berserker-wereforms`, `d2-wl-void-rift`, `d4-spiritborn-vortex`, `di-bombardment-wizard-pvp`,
  `di-minion-necro`, `di-spiritform-druid-pvp`, `la-communication-overflow-summoner`,
  `la-enhanced-weapon-deadeye`, `la-master-summoner`, `chr-arrow-storm-warden`, `chr-bee-warden`,
  `ud-snowstorm-frost`, `hot-blood-catcher`, `hot-spirit-warrior`.

A per-skill mapping lap on those 14 would raise kit coverage to 98.9% with **no change to the archetype
set** — they are a coverage gap, not a taxonomy gap.

---

## 6 · Cross-seam findings (filed, NOT acted on — ADR-004 routing via knight-rider)

**F-1 — `orbit` is outside the engine's geometry map.** `kit_mapping` attests `geometry_value = 'orbit'`
on 18 skills across 18 kits (Frozen Orb, Blessed Hammer, Blade Spirit, Ring Blades, Blade Vortex), and
its banded members are unanimously `motion_signature = 'orbit_fixed'`. But `orbit` is not a key of
`_RICH_TO_SPATIAL`, so `_RICH_TO_SPATIAL.get(rich, "point")` would silently gauge these as **`point`**,
where the neighbouring `whirlwind` gauges as `circle`. Corroborated independently: this repo's own
`MIGRATION.md` V9 census already lists `geometry:orbit` = 6 as a residual blocked bucket. Owner: engine
seam. Not fixed here — I do not write engine code.

**F-2 — 14 active combat kits have an empty `skills[]`.** See § 5. Owner: corpus curation (mine), but it
is a re-mapping lap, out of scope for P1. Docketed here rather than silently absorbed.

**F-3 — `knockback` is a probable vocabulary leak.** `geometry_value = 'knockback'` on exactly one skill
(`Ancient Spear (Rage Flip rune)`). `knockback` is an *effect* noun occupying a *geometry* slot. It is
kept as a singleton class per Discipline #41 (a cluster of one is a finding, not an error) and flagged
in `vfx_archetype.vocab_flag`. It is NOT merged away — merging it would be exactly the hand-imposition
the charter forbids. It is marked T4 support so P2 sequencing can deprioritize it without deleting it.

---

## 7 · Falsifier outcomes

Full evidence + consequence prose is in `vfx_vote_falsifier`. Summary:

| # | Outcome | One line |
|---|---|---|
| **F-a** (over-split) | **PENDING-P3** | First conjunct broadly satisfied (4 spatial primitives carry ≥3 archetypes) — expected, and precisely why M-2 was rejected. Second conjunct needs P3 imagery. A substrate-side watch-list of 5 same-spatial + same-motion groups is banked for P3. |
| **F-b** (under-split) | **FIRED-MISGRAINED** | Fires on 10/27 as pre-registered, but the instrument uses kit-level `delivery_value` against skill-grain archetypes, so it measures kit heterogeneity. Correctly re-grained onto `delivery_class`: **0/27**, purity 1.000. No under-split. |
| **F-c** (representativeness) | **FIRED (mild)** | Banded-vs-unbanded TVD = **0.200**. The banding pass over-sampled zone/summon/spread and under-sampled self-buff/melee. Contained: the taxonomy rests on `geometry_value` at 99.7%, so only the annotation density is skewed. P3/P4 must not read `motion_support` as archetype importance. |

---

## 8 · Iron-law asserts (in-script, all held)

```
universe kits            = 531                     OK
kits_covered + 6 + 14    = 531                     OK
member rows (ordinal>=0) = 1,138 == len(rows)      OK
sum(member_skills)       = 1,135 == assigned       OK
unassignable             = 3 + 6 + 14 = 23         OK
orphan members           = 0                       OK
pragma integrity_check   = ok                      OK
```

---

*Filed by elrond, 2026-08-23, VFX archetype-binding run P1. Auto-committed per project discipline
(Matt-authorized charge). Push held by gandalf (`RUN-CONDUCTOR`) per L-2.*
