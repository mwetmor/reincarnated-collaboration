# P1 — The archetype vote (VFX archetype-binding run)

**Date:** 2026-08-23
**Author:** elrond (data steward), invoked as named sub-agent by gandalf (`RUN-CONDUCTOR`)
**Run:** VFX ARCHETYPE-BINDING RUN — charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` § 4 (P1); ledger **L-7** (gate PASS + bounds), **L-8** (emission bundles PROHIBITED), **L-9** (method authorized)
**Predecessor:** `agentic_orchestration/elrond/notes/2026-08-23-vfx-p0a-kit-substrate-clusterability.md`
**Migration:** `agentic_orchestration/research/curated/MIGRATION-vfx-archetype-vote-2026-08-23.md`
**Script:** `agentic_orchestration/research/scripts/vfx_p1_archetype_vote_2026_08_23.py`
**Stamp:** `vfx-archetype-vote-2026-08-23/P1`

---

## VERDICT — **PROCEED**. 27 archetypes. 99.7% of skills assigned, 96.2% of kits covered. Zero merges performed, zero classes hand-imposed. HALT condition not met.

The substrate voted, and it voted more cleanly than P0-a predicted — because P0-a had nominated the
wrong axis. The correction (§ 2) is the most consequential thing in this report and it makes the
taxonomy better on every criterion P0-a itself declared.

---

## 1 · Method as executed

**Universe.** `canon_corpus.roster_status='active'` ⋈ `canon_engine_key.row_class='combat-kit'` = **531 kits**.

**Grain.** SKILL — one row per `kit_mapping.mapping_json.skills[]` entry in the universe = **1,138 rows over 511 kits**. Single grain; the P0-a two-grain split dissolved (§ 2.2).

**Axis.** `kit_mapping.mapping_json.skills[].geometry_value` — the per-skill field `kit_compiler.py`
reads FIRST as authoritative. 99.7% populated in universe, arity 27.

**Instrument.** Contingency lattice over the attested axis values. No distance clustering: these are
nominal categoricals with no metric, and any one-hot distance would smuggle in an arbitrary similarity
function — hand-imposition wearing a math hat (L-9).

**Merge rule.** Merge only where the engine's own join already collapses cells. Five candidate merges
were examined; **none was licensed** (§ 4).

**Labels.** `archetype_id` is the axis value **verbatim**. Nothing was renamed, glossed into genre
vocabulary, or minted. The `researcher_gloss` column is a mechanical concatenation of attested facts
(modal motion + modal delivery + verbatim exemplar `source_skill` strings) — legible to a zero-context
researcher without introducing a single word the substrate did not supply.

---

## 2 · The correction to P0-a (report this to Matt; it changes the shape of the answer)

### 2.1 P0-a nominated the engine's fallback while its authoritative field sat un-censused

P0-a § 6 recommended `skill_geometry_band.delivery_class × motion_signature`. That rested on an
incomplete census: P0-a counted `kit_mapping.mapping_json.skills[]` at 1,224 entries but never censused
the fields **inside** those entries. P1 did:

```
kit_mapping.mapping_json.skills[] — 1,224 entries
  source_skill      1,224  100.0%
  geometry_value    1,209   98.8%   <- 28 distinct values
  element_primary   1,224  100.0%
  element_secondary 1,224  100.0%
  ailments          1,224  100.0%
  delivery_notes    1,224  100.0%
```

`kit_compiler.py`:

```python
def _rich_geometry_for_skill(skill: SkillRow) -> str:
    """The rich geometry_type for a compiled skill: mapping geometry_value FIRST (anchored, §3.1),
    delivery_class table as fallback."""
    if skill.geometry_value:
        return skill.geometry_value
    if skill.delivery_class and skill.delivery_class in _DELIVERY_TO_RICH:
        return _DELIVERY_TO_RICH[skill.delivery_class]
    return "single_target"
```

and `kit_reader.py:37` — `geometry_value  # rich geometry_type from mapping (authoritative when present)`.

| | P0-a recommended | P1 as-executed |
|---|---|---|
| Field | `skill_geometry_band.delivery_class` | `kit_mapping…skills[].geometry_value` |
| Coverage (universe) | 407 / 1,138 = 35.8% | **1,135 / 1,138 = 99.7%** |
| Arity | 7 | **27** |
| Engine standing | fallback | **authoritative (§3.1)** |

The corrected axis wins on coverage, on engine-anchoring, and on discriminative power simultaneously.
P0-a's central argument — *"a VFX table keyed on this vocabulary lands on compiled kits by construction,
because the compiler IS the join"* — is not weakened by the correction; it is **strengthened**, because
the corrected axis is the exact field the compiler consults first.

### 2.2 Two consequences

**(a) The two-grain problem dissolved.** P0-a bounds § 5.1 and § 5.2 (skill-grain covers only 42.7% of
kits; the residual must bind at kit grain) were artifacts of the wrong axis. The authoritative field is
per-skill at 99.7%. There is **one grain and no kit-grain residual**. P4 may claim skill-grain coverage
across the roster. (Bounds § 5.3 — prose derivation — and § 5.5 — the emission-bundle prohibition —
stand untouched.)

**(b) The refinement axes are functionally determined by the corrected axis.** Joining
`skill_geometry_band` on `(kit_id, skill_ordinal)`:

- `geometry_value → motion_signature`: **305 joined rows, 22 archetypes, purity 1.000, zero exceptions.**
- `geometry_value → delivery_class`: **407 joined rows, 25 archetypes, purity 1.000, zero exceptions.**

The corrected axis **strictly refines** both P0-a axes — `zone` fans out to 5 geometry_values,
`burst_around_self` to 2, `straight_line` to 5, `point_strike` to 2 — while the converse fails. Both
P0-a axes are therefore carried as annotation columns, never as split axes.

### 2.3 A negative result worth banking

An early P1 attempt bridged the grains using the **kit-level** `canon_engine_key.geometry_value` and got
modal agreement of only 20–83% (most cells 30–60%) — which read as a broken bridge and nearly became a
finding about substrate incoherence. It was a **grain error on my side**: the kit-level column describes
a kit's dominant geometry, while bands are per-skill. At the correct grain the agreement is exact.
Recorded so a future lap does not re-derive the false negative (methodology step 5).

---

## 3 · The archetype table

27 archetypes. Grain = skill for all. Purity is 1.000 on every archetype carrying banded members.
`motion` / `delivery` are ANNOTATION (§ 2.2b), not defining axes.

| # | archetype_id (label READ from axis) | tier | skills | kits | motion_signature | delivery_class | spatial¹ | exemplar skills |
|---:|---|---|---:|---:|---|---|---|---|
| 1 | `ground_targeted_circle` | T1 | 115 | 102 | ground_place | zone | circle | Plague · Blaze · Blizzard · Fissure · Meteor |
| 2 | `melee_strike` | T1 | 115 | 98 | point_strike | melee_arc | point | Fulmination · Holy Reckoning · Zeal · Vengeance · Berserk |
| 3 | `self_buff` | T1 | 112 | 102 | *none — no path signature* | aura | none | Death Speaker · Bone Armor · Enchant · Fade · Werewolf |
| 4 | `totem` | T1 | 97 | 80 | *none — no path signature* | summon_delegate | none | Rocket Drone · Lightning Sentry · Iron Golem · Grim Ward |
| 5 | `single_target` | T1 | 90 | 77 | straight_line | projectile | point | Glacial Spike · Bone Spirit · Guided Arrow · Screaming Skull |
| 6 | `melee_arc` | T1 | 76 | 63 | arc_sweep | melee_arc | cone | Grim Scythe · Crippling Wave · Sweep Attack · Spectral Blade · Flurry |
| 7 | `aura` | T1 | 73 | 61 | *none — no path signature* | aura | circle | Conviction aura · Battle Orders · Fanaticism aura · Shout · Lower Resist |
| 8 | `multi_projectile` | T1 | 68 | 63 | fan_spread | projectile | point | Multiple Shot · Strafe · Frozen Orb · Phoenix Strike · Double Throw |
| 9 | `line` | T1 | 51 | 48 | straight_line | projectile | line | Blade Fury · Ice Blast · Bone Spear · Molten Boulder |
| 10 | `ring` | T1 | 50 | 47 | burst_around_self | zone | circle | Nova · Static Field · Poison Nova · Ring of Fire · Condemn |
| 11 | `circle` | T2 | 43 | 43 | burst_around_self | zone | circle | Bone Prison · Armageddon · War Cry · Tornado |
| 12 | `whirlwind` | T2 | 33 | 33 | orbit_fixed | motion | circle | Whirlwind · Tempest Rush · Eye of Reckoning · Reaper's Scythe |
| 13 | `dash_attack` | T2 | 32 | 31 | straight_line | motion | none | Charge · Dashing Strike · Steed Charge · Furious Charge · Seven-Sided Strike |
| 14 | `ground_slam` | T2 | 27 | 25 | point_strike | melee_arc | point | Hammer of the Ancients · Earthquake · Pulverize · Bolting Crash |
| 15 | `beam_channel` | T2 | 23 | 21 | straight_line | beam | line | Inferno · Heaven's Fury · Disintegrate · Siphon Blood · Incinerate |
| 16 | `blink` | T3 | 18 | 18 | straight_line | motion | none | Spirit Walk · Falling Sword · Blood Rush · Shadow Step · Wraith Form |
| 17 | `cone` | T3 | 18 | 18 | fan_spread | zone | cone | Howl · Shockwave · Flame Wave · Seismic Slam · Way of the Hundred Fists |
| 18 | `orbit` ² | T3 | 18 | 18 | orbit_fixed | motion | — | Frozen Orb · Blessed Hammer · Blade Spirit · Ring Blades · Blade Vortex |
| 19 | `chain` | T3 | 17 | 16 | chain_hop | beam | line | Chain Lightning · Claws of Thunder · Rabies · Touch of Death |
| 20 | `vortex_pull` | T3 | 15 | 15 | inward_pull | zone | circle | Abyss · Cyclone Strike · Black Hole · Corpse Tendrils · Whirlpool |
| 21 | `placed_lane` | T3 | 9 | 9 | lane_place | zone | line | Blade Sentinel · Fire Wall · Slow Time · Wall of Death · Bone Wall |
| 22 | `ricochet_bounce` | T3 | 9 | 8 | ricochet_return | projectile | line | Saw blade · Rapid Fire · Spinning Shield · Aegis of Menhir |
| 23 | `teleport` | T3 | 8 | 8 | blink_translate | motion | none | Teleport · Teleport (Enigma runeword) · Shadow Strike |
| 24 | `leap_strike` | T3 | 8 | 8 | leap_arc | motion | point | Leap · Leap Attack · Leaping Dragon · Fox Leap · Starfall Pounce |
| 25 | `fork` | T3 | 5 | 5 | fork_split | projectile | line | Lightning Fury · Panetti's Replicating Missile · Galvanic Shards · Scatter Shot |
| 26 | `defensive_dash` | T4 | 4 | 4 | *none attested* | *unbanded* | none | Evade (Rushing Claw) · Divine Dash (Athena boon) · Light Feather artifact |
| 27 | `knockback` ³ | T4 | 1 | 1 | *none attested* | *unbanded* | — | Ancient Spear (Rage Flip rune) |

¹ `spatial` is the `_RICH_TO_SPATIAL` value — **annotation only, never a merge authority** (§ 4, M-2).
² `orbit` is NOT a key of `_RICH_TO_SPATIAL` — cross-seam finding F-1 (§ 6).
³ `knockback` is a probable vocabulary leak, kept as a singleton class — finding F-3 (§ 6).

Support tiers: T1 ≥50 skills · T2 20–49 · T3 5–19 · T4 <5. Tiering is a **sequencing annotation for P2**,
not a merge and not a judgment about which archetypes are real. All 27 are equally attested.

**25 of the 27 are keys of the engine's own `_RICH_TO_SPATIAL` map, and all 25 keys are attested** —
the taxonomy is bijective onto the engine's authored rich-geometry vocabulary, plus `orbit` and
`knockback` which the engine's map does not carry. That is the strongest external-validity result in
this report: the substrate's emergent classes and the engine's independently-authored geometry
vocabulary are the *same set*, arrived at from opposite directions.

---

## 4 · Merge log — five candidates, **zero merges**

| # | Candidate | Claimed authority | Decision | Why |
|---|---|---|---|---|
| **M-1** | Merge across `delivery_class` | `_DELIVERY_TO_RICH` (7 keys) | **NOT-LICENSED** | The map is **injective** over its 7 attested keys. It collapses nothing, and it takes no motion input, so it can neither merge nor split within a class. |
| **M-2** | Collapse archetypes sharing a spatial primitive | `_RICH_TO_SPATIAL` (25→5) | **REJECTED** | See § 4.1. |
| **M-3** | Fold `orbit` into `whirlwind` | none — no engine join maps `orbit` | **NOT-LICENSED** | Merging on a shared *refinement* value would be hand-imposition; the substrate attests two distinct geometry_values. |
| **M-4** | Split archetypes by `motion_signature` | measurement, not a join | **NOT-LICENSED** | Purity 1.000. Splitting on a functionally-determined refinement yields no new classes. |
| **M-5** | Fold the 3 NULL-`geometry_value` skills into `single_target` | `_rich_geometry_for_skill` terminal default | **REJECTED** | **A default is not an attestation.** Listed unassignable instead. |

### 4.1 Why `_RICH_TO_SPATIAL` is not the merge authority — the load-bearing call of this phase

P0-a § 6 step 2 (adopted verbatim into L-9) named `_RICH_TO_SPATIAL` as the merge authority. Executing
it revealed that the map runs the wrong direction for this purpose, and **the engine's own code says so**:

- Its in-code comment declares its purpose: *"the compiler asserts against the SPATIAL value the engine
  will derive at run time."* It is the run-time **hit-gauge** primitive, deliberately lossy: 25 rich keys
  → 5 spatial values.
- The engine keeps the rich vocabulary as the **identity** layer. `_rich_geometry_for_skill` returns the
  RICH value as the skill's `geometry_type`; the spatial collapse happens only at
  `CompiledKit.primary_geometry`, for gauge assertion. The engine maintains both **because** spatial is lossy.

So the engine's identity vocabulary is the rich keyspace — which is where the archetype axis already
lives. The merge authority, correctly read, is the **identity map**, and it licenses no merge.

Had it been applied as written, it would have merged the 25 rich-key archetypes into 5
(`circle`←6, `none`←6, `line`←6, `point`←5, `cone`←2), putting Nova, Whirlwind, Fire Wall, Blizzard,
Cyclone Strike and Conviction-aura into one class. That is the hit-gauge wearing an archetype costume —
the same failure mode P0-a § 5.5 named for the emission bundles, arriving by a different road.

**This is a proposed amendment to L-9**, not a defiance of it: L-9's *principle* (the engine's join is
the only legitimate merge authority) is upheld exactly. Only the *identification* of which hop of the
join carries identity is corrected. Matt's veto remains open.

---

## 5 · Coverage accounting — total, every exception named

**Skill grain** (denominator 1,138):

| | Rows | % |
|---|---:|---:|
| **Assigned** | **1,135** | **99.7%** |
| Unassignable — `geometry_value` NULL *and* no `delivery_class` for the engine's fallback | 3 | 0.3% |

The three: `gd-blight-fiend-ritualist#0` (Summon Blight Fiend) · `gd-pet-conjurer#0` (Summon Briarthorn +
Summon Familiar) · `gd-trozan-druid#1` (Wind Devil). Each of those kits carries a second, assigned skill,
so no kit is lost to them. Their names read as summon-class — but assigning them by reading the skill
*name* is precisely the hand-imposition the charter forbids, so they stay unassigned.

**Kit grain** (denominator 531):

| | Kits | % |
|---|---:|---:|
| **≥1 skill assigned** | **511** | **96.2%** |
| No `kit_mapping` row (sentinel ordinal −1) | 6 | 1.1% |
| `kit_mapping` row present, `skills[]` EMPTY (sentinel ordinal −2) | 14 | 2.6% |

511 + 6 + 14 = 531, asserted in-script. The 6: `chr-crown-proc-engine`, `di-druid-pvp-cc-stack-2026`,
`la-destroyer-gravity-{compression,force,impact}`, `la-destroyer-vortex-gravity`. The 14 are listed in
the migration doc § 5 (finding F-2). A re-mapping lap on the 14 would raise kit coverage to 98.9% with
**no change to the archetype set** — a coverage gap, not a taxonomy gap.

---

## 6 · Cross-seam findings (filed, not acted on — ADR-004 routing via knight-rider)

**F-1 — `orbit` is outside the engine's geometry map.** 18 skills / 18 kits (Frozen Orb, Blessed Hammer,
Blade Spirit, Ring Blades, Blade Vortex), banded members unanimously `orbit_fixed`. Not a key of
`_RICH_TO_SPATIAL`, so `.get(rich, "point")` would silently gauge these as **`point`** where the
neighbouring `whirlwind` gauges as `circle`. Independently corroborated: this repo's `MIGRATION.md` V9
census already lists `geometry:orbit` = 6 as a residual blocked bucket. Engine seam owns the fix; I do
not write engine code.

**F-2 — 14 active combat kits have an empty `skills[]`** despite structurally complete mapping rows
(`motion_frame` / `scaffold` / `t4_doors` / `resource_economy` / `trigger_grammar` all present). Mine to
fix, but a separate lap.

**F-3 — `knockback` is a probable vocabulary leak.** One skill; an *effect* noun in a *geometry* slot.
Kept as a singleton class (Discipline #41 — a cluster of one is a finding, not an error), flagged in
`vfx_archetype.vocab_flag`, tiered T4 so P2 can deprioritize without deleting.

---

## 7 · Falsifier outcomes (pre-registered in P0-a § 6; full prose in `vfx_vote_falsifier`)

**F-a — over-split. → PENDING-P3.** The falsifier is a conjunction: ≥3 archetypes collapsing to the same
spatial primitive **AND** to the same reference imagery at P3. First conjunct satisfied broadly (circle←6,
line←6, none←6, point←5) — expected, and exactly why M-2 was rejected. Second conjunct is untestable
until P3. **Banked for P3: the substrate-side watch-list** — archetype groups sharing BOTH spatial
primitive and attested motion_signature, i.e. the genuine over-split candidates:

- `circle` + `ring` (both burst_around_self)
- `beam_channel` + `line` (both straight_line)
- `ground_slam` + `melee_strike` (both point_strike)
- `blink` + `dash_attack` (both straight_line; `blink`'s motion evidence is n=1 — weak)
- `defensive_dash` + `self_buff` + `totem` (all NULL-motion; semantically far apart despite the shared cell)

If any such group also selects the same canonical reference at P3, **that group** — not the taxonomy —
is over-split, and P4 merges it with the receipt recorded.

**F-b — under-split. → FIRED-MISGRAINED.** As pre-registered (kit-level `delivery_value` spread > 4) it
fires on 10 / 27. But `delivery_value` is a KIT-level column while archetypes are SKILL-grain, so a
3-skill kit donates its single `delivery_value` to 3 different archetypes: the statistic measures kit
heterogeneity, not archetype heterogeneity. The instrument was designed when the vote was expected to run
on kit-grain cells. Correctly re-grained onto the skill-grain `delivery_class`: **0 / 27 archetypes span
>1 class** (407 joined rows, purity 1.000). **No archetype is under-split.** Both forms are recorded
rather than the inconvenient one filed down.

**F-c — representativeness. → FIRED (mild), consequence contained.** Total variation distance between the
banded (n=407) and unbanded (n=728) archetype distributions = **0.200**. Largest deltas:
`ground_targeted_circle` +6.0% · `melee_arc` −5.1% · `totem` +4.3% · `multi_projectile` +4.1% ·
`self_buff` −3.5%. The banding pass over-sampled skills with legible delivery geometry and under-sampled
self-buffs and generic melee. **Contained** because the taxonomy rests on `geometry_value` at 99.7% while
`motion_signature` is annotation — the bias skews annotation *density*, not class membership.
**Consequence for P3/P4: do not read `motion_support` as evidence of archetype importance.**

---

## 8 · What landed (catalogue rows — my seam)

In `agentic_orchestration/research/curated/corpus.db`, additive, stamped `vfx-archetype-vote-2026-08-23/P1`:

| Table | Rows | Purpose |
|---|---:|---|
| `vfx_archetype` | 27 | The archetype table. |
| `vfx_archetype_member` | 1,158 | Total accounting: 1,138 skill rows + 20 kit-level exception sentinels. |
| `vfx_vote_merge_log` | 5 | Every merge considered, its claimed authority, the decision, the reasoning. |
| `vfx_vote_falsifier` | 3 | Falsifiers with as-executed outcomes. |

Schema choices, backups + md5s, reversibility, and the iron-law asserts are in
`MIGRATION-vfx-archetype-vote-2026-08-23.md`. Notable: `archetype_id` is the axis value **verbatim**
(no surrogate key — vocabulary drift stays visible); member rows preserve `geometry_value_raw` /
`motion_signature_raw` / `delivery_class_raw` so the curation is a projection, never a rewrite; every
non-assignment carries mandatory prose stating its cause; and the four rejected merges are **rows**, not
prose in a note that gets lost.

---

## 9 · Hand-off to P2

The 27 `archetype_id` + `researcher_gloss` pairs are the dossier job list. The glosses are built from
attested facts only and name real skills from real games (Nova, Whirlwind, Chain Lightning, Fire Wall,
Blessed Hammer, Hammer of the Ancients, Teleport) — a researcher with zero repo context can hunt
references from the gloss alone, which is what L-9 / R-2 require of the serialized Codex lane.

Sequencing suggestion (annotation, not authority — knight-rider and gandalf sequence): T1 (10) first,
they cover 847 / 1,135 = 74.6% of assigned skills. T4 (`defensive_dash` n=4, `knockback` n=1) last or
deferred. `knockback` in particular should not consume a Codex job until F-3 is dispositioned.

One P2 note the run should carry: **`circle` and `ring` are the pair most likely to come back with the
same imagery** (same spatial, same motion, both nova-shaped). That is not a reason to merge them now —
it is the F-a test, and P3 is where it resolves.

---

## 10 · Evidence index

- `agentic_orchestration/research/curated/corpus.db` — `canon_corpus`, `canon_engine_key`, `kit_mapping`, `skill_geometry_band`, `motion_signature_registry`, `corpus_schema_meta`, and the four new `vfx_*` tables
- `agentic_orchestration/research/scripts/vfx_p1_archetype_vote_2026_08_23.py` — the vote, transactional + idempotent
- `agentic_orchestration/research/curated/MIGRATION-vfx-archetype-vote-2026-08-23.md` — migration record
- `reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_compiler.py` — `_rich_geometry_for_skill`, `_DELIVERY_TO_RICH`, `_RICH_TO_SPATIAL`, `CompiledKit.primary_geometry` (READ ONLY)
- `reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_reader.py:37` — the "authoritative when present" annotation (READ ONLY)
- `agentic_orchestration/research/curated/MIGRATION.md` — V9 census, `geometry:orbit` residual bucket (F-1 corroboration)
- `agentic_orchestration/elrond/notes/2026-08-23-vfx-p0a-kit-substrate-clusterability.md` — P0-a, corrected at § 2 above

---

*Filed by elrond, 2026-08-23, VFX archetype-binding run P1. Verdict **PROCEED** — 27 archetypes, no
merges, no hand-imposed classes, HALT condition not met. Two items carry Matt's veto open: the § 2 axis
correction to P0-a, and the § 4.1 amendment to L-9's identification of the merge-authority hop.
Returned to gandalf (`RUN-CONDUCTOR`) for the P1 gate and P2 sequencing.*
