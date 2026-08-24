# Atlas-of-Kits ↔ T-A archetype alignment check (pre-seal verification)

**Date:** 2026-08-24
**Author:** elrond (data steward), invoked by gandalf (`RUN-CONDUCTOR`)
**Run:** VFX ARCHETYPE-BINDING RUN — charter ledger **L-36** commissioned this check
**Motivation:** Matt's Class B ruling — bespoke VFX attaches at the SKILL-TYPE level ("one move per
skill-type, not one more per kit"), grounded in the **Atlas of Kits** on the Glance/loadout app, on the
belief that the Atlas's existing decomposition (keys such as *geometry*, *tempo*) already supplies the
partition the VFX table needs.
**Mode:** READ-ONLY. No schema change, no rows written, no view created.

---

## VERDICT — **MAPPED**, not SAME PARTITION.

**Matt is right about the substrate and looking at the wrong grain of it.**

The Atlas's `geometry` key and the T-A archetype axis are **the same field, the same vocabulary, the
same export lineage** — Matt's intuition about provenance is exactly correct, and it is the load-bearing
half of the answer. But the key he can *see* on the Atlas coords strip is the **kit-level rollup** of
that field, while T-A is the **per-skill** value. They are not the same partition:

- The kit rollup carries a geometry value that is **not any of its own skills' archetypes in 96 of 203
  cases (47 %)**.
- **9 of the 24 T-A archetypes never appear as an Atlas geometry value at all** — 166 skills, 14.6 % of
  the assigned corpus, including `melee_arc` (T1, 76 skills / 63 kits).
- The Atlas exports **43 %** of the T-A kit universe (229 of 531) and **36 %** of its skill rows.

The skill-grain decomposition Matt wants **already exists one panel down on the same page**
(`CanonKit.tsx:240` — "mapping skills (mapping_json.skills)"). No bridge is needed to reach it from a kit
page. A bridge is needed only if the *index* / *atlas-coords* surface is to carry it, and separately to
resolve the 27→24 fold, which lives in prose and not in the DB.

---

## 1 · Axis provenance — **SAME substrate field, same lineage.** Not independent decompositions.

The Atlas renders from `public/canon-data/` in `~/Games/reincarnated-loadout/`, written by
`scripts/export_canon_corpus.py`, whose source of truth is declared in the export's own provenance block:

```
source_db: /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db
```

— the same `corpus.db` the P1 vote ran on. Not a separate dataset, not an engine-side export. One DB.

**The 14-slot key-space.** `canon_corpus.atlas_coords` is a pipe-delimited 14-slot string
(`export_canon_corpus.py:69–90`, `ATLAS_SLOT_LABELS`; slot labels were derived empirically by the
exporter and are labelled positionally + honestly in the UI). Attested census over all 268 rows carrying
coords:

| # | label | arity | modal values |
|---:|---|---:|---|
| 0 | motion / mobility | 5 | full-move 111 · walk 72 · rooted 55 · blank 24 |
| 1 | delivery | 8 | at-target 153 · projectile 56 · self-origin 33 |
| 2 | amplitude (damage var.) | 4 | flat 175 · spiky 62 · var 29 |
| **3** | **geometry** | **19** | **ground_targeted_circle 55 · totem 34 · circle 30 · multi_projectile 29 · blank 28** |
| 4 | control function | 3 | damage 233 · control 7 |
| 5 | control ailment | 9 | none 164 · hard-stop 25 · hex 24 |
| 6 | defensive profile | 7 | tank 92 · mitigate 79 · evade 31 |
| 7 | resource economy | 12 | spend 113 · free 30 · cooldown 28 |
| 8 | proxy density | 3 | solo 184 · light 43 · heavy 41 |
| 9 | engagement range | 3 | melee 118 · ranged 88 · dual 62 |
| 10 | damage tempo | 3 | high 115 · med 103 · low 50 |
| 11 | commitment | 4 | instant 232 · channel 21 · wind-up 13 |
| 12 | activation | 3 | active 214 · triggered 50 |
| 13 | cadence / dependency | 4 | one-shot 202 · apply→detonate 38 · build→spend 24 |

Slots 9/10/2 are additionally surfaced as first-class index columns `range_val` / `tempo_val` /
`amp_val` (`canonTypes.ts:39–41`; rendered `CanonIndex.tsx:247` as `range / tempo / amp`).

**Slot 3 IS the engine geometry field.** Compared against `canon_engine_key.geometry_value` per kit:

```
atlas slot3 vs canon_engine_key.geometry_value: same=239  diff=3  ek_null=26
   DIFF  poe1-charged-dash    slot3='blank'  ek='dash_attack'
   DIFF  d2-leap-attack-barb  slot3='blank'  ek='dash_attack'
   DIFF  le-frost-wall-rm     slot3='totem'  ek='placed_lane'
```

So the Atlas "geometry" key is a materialised copy of `canon_engine_key.geometry_value`, 98.8 % identical,
with three drift rows (two under-populated, one genuinely stale — `le-frost-wall-rm` still reads `totem`
where the engine key reads `placed_lane`).

**T-A's axis** is `kit_mapping.mapping_json.skills[].geometry_value` — the field
`kit_compiler._rich_geometry_for_skill` reads FIRST as authoritative (P1 § 2.1). Same rich-geometry
vocabulary; one grain finer.

**Vocabulary overlap is a strict subset, one direction:**

```
T-A archetype_ids (27, pre-fold)   : aura beam_channel blink chain circle cone dash_attack defensive_dash
                                     fork ground_slam ground_targeted_circle knockback leap_strike line
                                     melee_arc melee_strike multi_projectile orbit placed_lane
                                     ricochet_bounce ring self_buff single_target teleport totem
                                     vortex_pull whirlwind
Atlas slot-3 attested (19)         : the above MINUS the nine below, PLUS the sentinel 'blank'
Atlas-not-in-T-A                   : ['blank']   (a sentinel, not a class)
T-A-not-in-Atlas                   : blink · defensive_dash · fork · ground_slam · knockback ·
                                     leap_strike · melee_arc · orbit · placed_lane
```

**Answer to Q1: same underlying substrate field, same export lineage, one DB. Not independent
decompositions.** The Atlas's other 13 slots are kit-descriptor axes (largely the BC axis family) that do
not participate in the geometry partition at all — see § 2.3.

---

## 2 · Partition comparison — **crosscutting at kit grain; neither a coarsening nor a refinement.**

### 2.1 Universe first: the Atlas is a 43 % window on the T-A corpus

The exporter's pool is `SELECT * FROM canon_corpus WHERE corpus_class='record'` → 267 rows
(`export_canon_corpus.py:14`); `annex` (304) and `system` (19) are explicitly out of scope.

| | kits | skill rows |
|---|---:|---:|
| T-A universe (`roster_status='active'` ⋈ `row_class='combat-kit'`) | 531 | 1,138 |
| Atlas export pool (`corpus_class='record'`) | 267 | — |
| **Atlas ∩ T-A** | **227** | **~412** |
| T-A kits invisible to the Atlas — `corpus_class='annex'` | **282** | **726 (64 %)** |
| Atlas kits outside T-A — 36 `roster_status='parked'` + 2 `system-record` | 40 | — |

**Two-thirds of the skill corpus the VFX table binds is not on the Atlas at all.** This is a scope gap,
not temporal staleness (§ 4).

### 2.2 Within the intersection, the kit rollup crosscuts the skill partition

Per kit, comparing the Atlas geometry value against the set of T-A archetypes its own skills carry
(203 kits with a non-blank Atlas geometry):

| Relation | kits | % |
|---|---:|---:|
| Atlas geo **==** the kit's one and only archetype | 35 | 17 % |
| Atlas geo **is one of** several archetypes on the kit | 72 | 35 % |
| Atlas geo is **NOT among** the kit's archetypes at all | **96** | **47 %** |

Distinct archetypes per kit: 1 → 98 kits · 2 → 103 · 3 → 24 · 4 → 2. A majority of kits carry more than
one archetype, so a single kit-level slot cannot represent them even in principle.

**Counterexample rows** (`kit_id` · Atlas geometry · T-A skill archetypes · the skills):

| kit | Atlas `geometry` | T-A archetypes | skills |
|---|---|---|---|
| `d2-hammerdin` | `multi_projectile` | `orbit`, `teleport` | Blessed Hammer · Teleport (Enigma runeword) |
| `d2-frozen-orb-sorc` | `multi_projectile` | `orbit`, `teleport` | Frozen Orb · Teleport |
| `d2-javazon` | `chain` | `fork`, `melee_strike` | Lightning Fury · Charged Strike |
| `d2-fire-sorc` | `totem` | `ground_targeted_circle`, `single_target` | Fire Ball · Meteor |
| `d2-fohdin` | `ground_targeted_circle` | `aura`, `single_target` | Fist of the Heavens · Conviction (aura) |
| `d2-frost-bowazon` | `circle` | `single_target` | Freezing Arrow · Cold Arrow |
| `d2-fury-wolf` | `single_target` | `melee_strike`, `self_buff` | Fury · Feral Rage |
| `d2-ghost-assassin-pvp` | `ground_targeted_circle` | `single_target`, `totem`, `whirlwind` | Lightning Sentry · Mind Blast · Whirlwind |
| `d2-kicksin` | `single_target` | `melee_strike`, `self_buff` | Dragon Talon · Fade · Cobra Strike |
| `d2-rabies-wolf` | `chain` | `melee_strike`, `self_buff` | Werewolf · Rabies |

`d2-hammerdin` is the cleanest one to hand Matt: the Atlas geometry slot reads `multi_projectile`, and
neither of the kit's two skills is a multi-projectile — Blessed Hammer is `orbit` and Teleport is
`teleport`. Binding a bespoke VFX off the Atlas slot would give Blessed Hammer the wrong effect.

### 2.3 The nine archetypes the Atlas key-space cannot express

| archetype | skills | kits |
|---|---:|---:|
| `melee_arc` | 76 | 63 |
| `ground_slam` | 27 | 25 |
| `blink` | 18 | 18 |
| `orbit` | 18 | 18 |
| `placed_lane` | 9 | 9 |
| `leap_strike` | 8 | 8 |
| `fork` | 5 | 5 |
| `defensive_dash` | 4 | 4 |
| `knockback` | 1 | 1 |
| **TOTAL** | **166 / 1,135 = 14.6 %** | |

`melee_arc` is a **T1** archetype — Grim Scythe, Crippling Wave, Sweep Attack, Spectral Blade, Flurry —
entirely invisible in the Atlas geometry vocabulary. `orbit` is the F-1 archetype the engine's
`_RICH_TO_SPATIAL` also does not carry, so its absence here is a second corroboration of that finding
rather than a new one.

### 2.4 "geometry, tempo, etc." — only *geometry* partitions VFX

The remaining 13 slots are **kit-grain descriptors orthogonal to visual form**. Crossing the two Matt
named, at kit grain over the 265 coord-bearing records:

```
geometry × tempo  ->  44 cells   (geometry arity 18 × tempo arity 3)
```

44 ≠ 24, and the extra cells are not new visual classes: they split one geometry into up to three cells
on an axis (`high`/`med`/`low` damage tempo) that has no bearing on what the effect looks like. Crossing
in more slots (delivery 8, amplitude 4, defensive 7, resource 12 …) multiplies the cell count further
while the visual form stays constant. **Tempo is a parameter of the archetype, not a partition of it** —
the same standing element/sub-element/colour have in Matt's own formulation.

**Answer to Q2: CROSSCUTTING, not exact / coarsening / refinement.** As a partition of *skills*, the
Atlas index key-space does not partition skills at all — it is kit-grain. As a partition of *kits*, its
geometry key disagrees with the kits' own skill archetypes in 47 % of cases and cannot name 9 of the 24
active archetypes. The T-A partition is the finer, complete one; the Atlas key is a lossy modal
projection of it onto kits.

---

## 3 · Consequence — **a builder CAN navigate deterministically from an Atlas kit page today.** No bridge
needed at kit-page grain. Two bridges wanted elsewhere.

### 3.1 The join key is already present in the exported per-kit payload

`export_canon_corpus.py:249` exports the whole `kit_mapping` row, and `mapping_json` is JSON-parsed
(`JSON_COLS['kit_mapping']`), so `mapping.mapping_json.skills[]` reaches the browser intact.
`CanonKit.tsx:213–241` renders it — § 4 "Skills & geometry" → `MappingSkills` subsection. Verified in the
shipped artifact:

```
public/canon-data/kits/d2-hammerdin.json
  mapping.mapping_json.skills[0] = {source_skill: 'Blessed Hammer',                geometry_value: 'orbit'}
  mapping.mapping_json.skills[1] = {source_skill: 'Teleport (Enigma runeword)',    geometry_value: 'teleport'}
  engine_key.geometry_value      = 'multi_projectile'          <- the Atlas coords-strip value
```

and the T-A rows for the same kit:

```
d2-hammerdin | 0 | orbit    | Blessed Hammer
d2-hammerdin | 1 | teleport | Teleport (Enigma runeword)
```

**Ordinal alignment is exact** — `vfx_archetype_member.skill_ordinal` is the positional index of
`mapping_json.skills[]`, so the join key `(kit_id, skills[] array index)` is present on **both** sides
with no transformation. Equivalently, `geometry_value` on the skill row **is** the `archetype_id`
verbatim (P1 § 1: labels are the axis value unrenamed), so a builder can read the archetype straight off
the Atlas kit page without a lookup at all.

### 3.2 Where a bridge IS wanted (naming only — NOT created)

**(a) The 27 → 24 fold has no home in the DB.** `vfx_archetype` carries 27 rows and no fold column
(`PRAGMA table_info(vfx_archetype)` — no `folded_into` / `alias_of`). The L-29 folds
(`ring` → `circle`, `defensive_dash` → `dash_attack`) exist only as prose in the binding spec § 3.1b. A
reader joining raw member rows to the spec's 24-row index gets two unmatched names. One-statement shape:

```sql
ALTER TABLE vfx_archetype ADD COLUMN folded_into TEXT;   -- NULL = active; L-29 authority in `source`
```

This is the one I would recommend to the conductor, because it is the only case where the DB and the
sealing spec currently disagree on the archetype set.

**(b) Surfacing the archetype on the Atlas index / coords strip.** If the index or the coords strip is to
carry the skill-grain archetype rather than the kit rollup, the shape is a read-only view exported
alongside the existing payload — no new table:

```sql
CREATE VIEW v_atlas_kit_vfx_archetype AS
SELECT kit_id, skill_ordinal, source_skill, archetype_id
FROM vfx_archetype_member
WHERE vote_run = 'vfx-archetype-vote-2026-08-23' AND skill_ordinal >= 0;
```

plus a one-line exporter change to attach it per kit. **Not created.** Note this only helps the 43 % of
the T-A universe the Atlas exports at all; widening `corpus_class='record'` to include `annex` is a
separate, larger call and is drax's + the conductor's, not mine.

---

## 4 · Staleness — the Atlas is 33 days old, but the gap is **SCOPE, not TIME**

| | |
|---|---|
| `index.json` `exported_utc` | **2026-07-22T23:26:38Z** |
| exporter's recorded `schema_version` | `v2.0`, applied `2026-07-22T06:35:21Z` |
| last commit touching `public/canon-data/` | `f869d45`, 2026-07-22 |
| `corpus.db` mtime | 2026-08-24 10:13 |
| migrations applied since the export | `gd-edition-pin` · `gd-devotion-payloads` · `gd-deviation-reverify` · `gd-displayname-bridge` M1–M4 (2026-07-24 → 07-26) · `vfx-archetype-vote-2026-08-23/P1` (2026-08-24) |

**The record set itself has NOT drifted.** The export's `corpus_class_counts`
(`annex 304 / record 267 / system 19`) match today's `canon_corpus` **exactly**, and its
`record_count: 267` matches today's row count. The intervening migrations were GD-side and additive.

So: **do not report this as a stale dataset.** Report it as a **scoped** one — the Atlas was always a
window on `corpus_class='record'`, and the VFX corpus is 2.3× larger than that window. The three
`atlas_coords` drift rows in § 1 are the only genuine staleness found, and one of them
(`le-frost-wall-rm`: coords say `totem`, engine key says `placed_lane`) is on a `parked` kit outside the
T-A universe anyway.

**What this changes about what Matt's ruling binds to:** the ruling's *principle* — attach at skill-type,
parameterise element/colour on top — binds cleanly, because the skill-type field it names is the exact
field T-A voted on and it is already rendered on the Atlas kit page. The ruling's *pointer* — the
geometry key visible on the Atlas coords strip and index — is a kit-grain rollup that would mis-bind 47 %
of kits and could not name 9 of the 24 archetypes. **The T-A table is not a second decomposition
competing with the Atlas; it is the Atlas's own geometry key read at the grain the ruling asks for.**

---

## 5 · Evidence index

- `~/Games/reincarnated-loadout/scripts/export_canon_corpus.py` — `:14` pool query · `:69–90` `ATLAS_SLOT_LABELS` · `:125` `split_atlas_coords` · `:228` record select · `:249` kit_mapping export · `:401` slot labels into provenance (READ ONLY)
- `~/Games/reincarnated-loadout/src/data/canonTypes.ts` — `:1–12` source-of-truth header · `:29–52` `CanonIndexRow` (`range_val`/`tempo_val`/`amp_val`) · `:78–89` `AtlasSlot` / `AtlasCoordsParsed` · `:104–122` `CanonKitDetail` (READ ONLY)
- `~/Games/reincarnated-loadout/src/pages/CanonKit.tsx` — `:203` `AtlasCoords` (the kit rollup) · `:213–241` § 4 "Skills & geometry" → `MappingSkills` (the skill grain) (READ ONLY)
- `~/Games/reincarnated-loadout/src/pages/CanonIndex.tsx:247` — `range / tempo / amp` index rendering (READ ONLY)
- `~/Games/reincarnated-loadout/public/canon-data/index.json` — export provenance block; `kits/d2-hammerdin.json` — the counterexample payload (READ ONLY)
- `agentic_orchestration/research/curated/corpus.db` — `canon_corpus.atlas_coords`, `canon_engine_key.geometry_value`, `kit_mapping.mapping_json`, `vfx_archetype`, `vfx_archetype_member`, `corpus_schema_meta` (READ ONLY, no writes)
- `agentic_orchestration/elrond/notes/2026-08-23-vfx-p1-archetype-vote.md` — P1 § 1 axis + labels, § 2.1 the authoritative-field correction, § 2.3 the kit-grain/skill-grain negative result this check independently re-confirms
- `agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` § 3.1a (24 active rows) · § 3.1b (L-29 fold record)

---

*Filed by elrond, 2026-08-24, VFX archetype-binding run — L-36 pre-seal verification. Verdict **MAPPED**.
Read-only throughout; no schema change, no rows, no view. Returned to gandalf (`RUN-CONDUCTOR`).*
