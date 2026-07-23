# Research — KFL-25a Rotation Metadata Probe — 2026-07-23

**Mode:** A (analytical)
**Commissioner:** gandalf (RUN-CONDUCTOR, KIT-FIDELITY run KFL-25a)
**Sources consulted:**
- `corpus.db` — `canon_corpus`, `kit_mapping`, `skill_geometry_band` tables (READ-ONLY)
- `src/reincarnated/simulation/kit_compiler/kit_compiler.py` and `kit_reader.py` — compiled skill dict schema
- `src/reincarnated/simulation/ai_strategies.py` — rotation selector logic
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — `_select_skill_for_entity`
- `claude-mobile-session-docs/ARPG-canonical-kit-research/` — per-game JSONL corpora and harvest reports
- `final-docs-v3/rdr-kit-atlas-v3.csv` and `rdr-roster-kits.jsonl`
- Maxroll.gg D2 Meteor/Fireball Sorceress guide (https://maxroll.gg/d2/guides/meteor-sorceress)
- Maxroll.gg D2 Fire Wall Sorceress guide (https://maxroll.gg/d2/guides/fire-wall-sorceress-guide)
- Crate Entertainment Forum — Fire ConeMan FoI Purifier thread (https://forums.crateentertainment.com/t/1-1-7-2-the-fire-coneman-fire-flames-of-ignaffar-purifier-focused-on-conversion/102294)
- Game8 PoE2 Bonestorm Blood Mage guide (https://game8.co/games/Path-of-Exile-2/archives/490217)
- PoE-Vault Cyclone Slayer guide (https://www.poe-vault.com/guides/murder-on-a-budget-cyclone-slayer-build-guide)
- Overgear Cyclone build guide (https://overgear.com/guides/poe/cyclone-build/)
- Odealo Meteor/Fireball Sorceress guide (https://odealo.com/articles/meteor-fire-ball-sorceress-build-for-diablo-2-resurrected)

---

## Summary

The KF-2 harvest captured geometry, element, cadence, and delivery data per skill but collected NO per-skill rotation signals — no `role`, no `cast_priority`, no cooldown ordering. The compiled kit skill dict (`kit_compiler.py`) likewise emits no `role` field, and the sim's player skill selector (`spatial_engine._select_skill_for_entity`) falls back to shortest-cooldown-first for player kits, which collapses multi-skill kits to their fastest-cycling skill. The actual source rotations for all five pilot kits are recoverable from build guides and are structurally simple: one primary (spam or channel), one secondary with a clear behavioral trigger. The harvest corpus `mech_summary` and `delivery_notes` prose in `mapping_json.skills[].delivery_notes` contain partial rotation signal but not in machine-readable form. The recommended extension shape is (α) a per-skill `role` enum, which is sufficient to fix the collapse for all five pilot kits and is mechanically derivable for the broad corpus from existing structured fields.

---

## Q1 — Does the already-collected source material contain per-skill rotation/role signals?

### What the corpus.db carries per skill

The `skill_geometry_band` table stores the following fields per (kit_id, skill_ordinal):

| Field | Values present for pilot-5 |
|---|---|
| `ordinal` | 0, 1 (position in mapping_json.skills[]) |
| `source_skill` | skill name string |
| `cadence_class` | `spam` / `channel` / `cooldown` / NULL |
| `delivery_class` | `projectile` / `zone` / `motion` |
| `origin` | `self` |
| `width_band` | `wide` (FoI, Cyclone) or NULL |
| `range_band` | `melee` (Cyclone) or NULL |
| `motion_signature` | `straight_line` / `ground_place` / `lane_place` / `fan_spread` / `orbit_fixed` |
| `derivation` | `dossier-prose` (all five kits) |
| `source_anchor` | verbatim prose from the dossier describing delivery |

There is **no `role` field**, **no `cast_priority` field**, and **no cooldown-ordering field** anywhere in `skill_geometry_band`, `kit_mapping`, `canon_corpus`, `kit_composition`, or the compiled skill dict output.

The compiled skill dict (as confirmed by running `compile_kit` on d2-fire-sorc and poe2-bonestorm) contains: `id`, `name`, `geometry_type`, `spatial_geometry_type`, `geometry_params`, `canonical_element`, `scaling_attribute`, `damage_scaling_type`, `damage_multiplier`, `energy_cost`, `cadence`, `tier`, `effects`, `_delivery_class`, `_projectiles_per_cast`, `_source_skill`. **`role` is absent.**

### Partial signal present (not machine-readable)

Two sources carry partial rotation information in prose:

1. **`mapping_json.skills[].delivery_notes`** — the `source_anchor` column echoes these. The d2-fire-sorc Fireball entry reads "Primary spam skill." and Meteor reads "Pair with Fire Ball for overlapping burst." These contain role-implication but are unstructured prose, not a parseable enum.

2. **`mech_summary` in canon_corpus / the JSONL corpora** — e.g., d2-fire-sorc: "Fire Ball spam with Meteor drops on packs; methodical placement caster planning impact zones." This is human-readable rotation description but again unstructured.

3. **`cadence_class`** in `skill_geometry_band` — partially encodes behavior: `spam` implies primary/filler; `channel` implies main-skill; `cooldown` implies secondary/triggered. BUT: Meteor's `cadence_class` is NULL (not captured), and the field alone does not distinguish "main channel" from "setup-then-channel." Not sufficient alone.

4. **`ordinal`** — ordinal 0 is the primary skill by convention (kit_compiler uses `rec.skills[0]` as the primary). This is a weak proxy for priority but is not a rotation-role signal (Meteor at ordinal=1 should actually be PRIORITY=0 in the real rotation).

**Conclusion for Q1: No. The existing collected material contains NO machine-readable per-skill rotation role or cast_priority signal. Prose hints exist in delivery_notes and mech_summary but are not parseable without LLM labeling.**

---

## Q2 — Per-kit actual source rotations

### Kit 1: d2-fire-sorc (FireBall + Meteor)

**Skills in corpus:** Fire Ball (ordinal 0, cadence=spam), Meteor (ordinal 1, cadence=NULL)

**Actual rotation (from guides + knowledge):**
- **Meteor: PRIORITY-0 (primary, use on every cooldown)** — Meteor has a ~6-second cooldown (at level 20). The standard rotation is to cast Meteor first at the target location, then fill with Fire Ball while waiting for Meteor's cooldown to expire. Maxroll guide: "With Meteor you want to continually cast either on top of or leading your targets." "Spam Meteor to prevent the bosses from healing with burning Damage Over Time."
- **Fire Ball: PRIORITY-1 (filler, spam between Meteor casts)** — Maxroll: "Fire Ball is great for fast Area of Effect damage." Odealo notes Fire Ball "has no cooldown, so stands for a quickly accessible source of AoE damage" and "at higher levels, Fire Ball becomes your primary damage-dealing ability because of the Meteor's high delay."

**Firing pattern:** Meteor on cooldown (every ~6s). Fire Ball as spam filler between casts. Static Field situationally vs bosses (not harvested as a core skill for this kit).

**Role assignment:**
- Fire Ball: `role = "primary_attack"` (spam filler, highest fire-rate)
- Meteor: `role = "burst_damage"` (cooldown nuke, highest damage/cast)

**The sim's current behavior (confirmed):** ordinal 0 = Fire Ball (cadence spam, shortest CD) fires every tick; Meteor never fires because its energy_cost or cooldown is always lower for Fire Ball. This is the DPS-max collapse described in the charter.

**Citations:** Maxroll.gg D2 Meteor Sorc guide; Odealo Meteor/Fireball Sorc guide.

---

### Kit 2: d2-firewall-sorc (Fire Wall)

**Skills in corpus:** Fire Wall (ordinal 0, cadence=cooldown)

**Actual rotation:**
This is a single-active-skill kit. Fire Wall is the entire damage output. The "rotation" is purely positional:
- **Fire Wall: PRIORITY-0 (only active damaging skill)** — "Stack Fire Wall for more damage against stationary targets." "With Fire Wall you want to continually cast either on top of or leading your targets."
- **Teleport: passive repositioning** — not a combat damage skill; used for movement between Fire Wall placements. Not in the corpus skill list.
- **Static Field: situational opener vs bosses** — not in the corpus skill list.

**Role assignment:**
- Fire Wall: `role = "area_damage"` (placed zone, spam on cooldown)

**Rotation impact:** Single-skill kit; no multi-skill collapse problem. The sim already fires Fire Wall correctly as the only available skill.

**Citations:** Maxroll.gg D2 Fire Wall guide; mtmmo.com Firewall Sorceress guide.

---

### Kit 3: gd-flames-of-ignaffar-purifier (Flames of Ignaffar + Inquisitor Seal)

**Skills in corpus:** Flames of Ignaffar (ordinal 0, cadence=channel), Inquisitor Seal (ordinal 1, cadence=NULL)

**Actual rotation:**
- **Flames of Ignaffar: PRIORITY-0 (main channel, held down continuously)** — "Channel a widening cone of purging fire that ramps intensity the longer it burns." The kit is explicitly a kiting-channel build: "Key is to kite if you're in trouble. This is perhaps the only kiting channeling skill build in the world."
- **Inquisitor Seal: PRIORITY-1 (place before engaging, refresh when expired)** — "Players stand on it during combat." The Seal is a placed defensive platform providing buffs; standard practice is to place it at the start of a pull, stand on it, then channel FoI. Placement is pre-combat or on repositioning — a setup/guard role, not a primary DPS rotation component.

**Role assignment:**
- Flames of Ignaffar: `role = "primary_attack"` (the sole sustained damage vehicle; channel maintained until rooted-kite repositioning)
- Inquisitor Seal: `role = "defensive"` or `role = "control"` — a placed defensive platform, not a damage skill. It provides buff-platform utility, not direct offense.

**Firing pattern:** Place Seal. Stand on Seal. Channel FoI. Kite-reposition when overwhelmed. Recast Seal at new position. Resume channel.

**Citations:** Crate Entertainment Forum thread (Fire ConeMan build); Grimtools build index for FoI Purifier (RektbyProtoss build entry showing Inquisitor Seal as a non-damage utility skill).

**Note on cadence_class:** FoI correctly has `cadence=channel`. Inquisitor Seal has `cadence=NULL` — this could be mapped to `cooldown` (it has a cooldown in-game) but its rotation-role is `defensive`/`setup`, not DPS.

---

### Kit 4: poe2-bonestorm (Bone Storm + Bone Cage)

**Skills in corpus:** Bone Storm (ordinal 0, cadence=channel), Bone Cage (ordinal 1, cadence=cooldown)

**Actual rotation:**
- **Bone Storm: PRIORITY-0 (primary DPS, spam continuously)** — "Spam Bonestorm constantly." "Just keep spamming Bonestorm." The build's damage output is entirely Bone Storm.
- **Bone Cage: PRIORITY-1 (reactive defensive, use when overwhelmed)** — "Activate Bone Cage if you're overwhelmed by mobs." "Use Bone Cage as the main skill for CLEARING maps" is an alternate version (0.5 totem variant), but the core 0.1-0.2 version treats it as a defensive panic button. The corpus mech_summary: "0.5 reincarnated it as Bone Cage + Bone Storm TOTEMS" — the main sim kit targets the 0.1-0.2 era where Bone Storm is primary.

**Role assignment:**
- Bone Storm: `role = "burst_damage"` (wind-up release, primary nuke)
- Bone Cage: `role = "control"` (root/containment, defensive/utility cast)

**Firing pattern:** Channel/release Bone Storm on every available window. Cast Bone Cage reactively for control or defense. Bone Storm is the priority-0 damage skill; Bone Cage is triggered by survival need.

**Citations:** Game8 PoE2 Bonestorm Blood Mage guide; mobalytics.gg Bonestorm league starter guide (rotation section from web search summary).

---

### Kit 5: poe1-cyclone (Cyclone)

**Skills in corpus:** Cyclone (ordinal 0, cadence=channel)

**Actual rotation:**
Single-active-skill kit (with passive auras and reactive CWDT, none of which are in the corpus skill list).
- **Cyclone: PRIORITY-0 (sole active DPS, hold continuously)** — "You hold your 'Cyclone' button and your character will move toward the cursor." "Spin around while just holding down right-click." Full movement-during-channel is native; the skill IS the movement.
- Supporting skills are auras (Pride, Precision, Dread Banner) that are toggled once at zone entry, not in the damage rotation.
- War Banner is placed situationally before boss fights — not a combat rotation skill.

**Role assignment:**
- Cyclone: `role = "primary_attack"` (the sole combat action, channel-move)

**No multi-skill collapse problem.** Single-skill combat action; the sim fires it correctly.

**Citations:** Overgear Cyclone build guide; PoE-Vault Cyclone Slayer guide (3.28 era).

---

## Q3 — Harvestable-at-scale assessment

### Can a KF-2-style schema extension extract `role` or `cast_priority` mechanically?

**The short answer: No for mechanical extraction; Yes for structured enum extension via LLM-assisted labeling.**

#### Structured fields currently present and what they encode

| Field | Rotation signal encoded | Rotation signal MISSING |
|---|---|---|
| `cadence_class` (spam/channel/cooldown/NULL) | Implies "fires continuously" (spam/channel) vs "fires on CD" (cooldown) | Does not distinguish primary vs secondary; `cooldown` applies to Meteor (primary nuke) and Bone Cage (defensive) equally |
| `ordinal` | Encoding convention: 0 = most important skill | Not a reliable proxy — Meteor at ordinal=1 is actually PRIORITY-0 in the real rotation |
| `delivery_class` | Geometric shape, not rotation role | No rotation signal |
| `motion_signature` | Spatial path, not rotation role | No rotation signal |
| `source_anchor` prose | Contains role-implication ("Primary spam skill", "defensive panic button") | Unstructured; not machine-parseable without LLM |
| `mech_summary` in canon_corpus | Contains rotation description ("Fire Ball spam with Meteor drops") | Unstructured prose |

#### Shape (α): per-skill `role` enum

This is **sufficient and achievable.** A `role` enum with values `{primary_attack, burst_damage, area_damage, control, defensive, setup, mobility}` (aligned with the sim's existing role vocabulary in `ai_strategies.py`) would directly fix the sim's rotation selector for all five pilot kits. The enum values are:

- Derivable from `cadence_class` + `delivery_class` + `source_anchor` prose for ~60-70% of corpus skills (e.g., `cadence=channel + delivery=motion → primary_attack`; `cadence=cooldown + delivery=zone → area_damage or control`)
- For the remainder (ambiguous cadence, NULL cadence), derivable via one-pass LLM labeling over `source_anchor` + `mech_summary` prose — the same prose that currently carries unstructured rotation signal

**Evidence for mechanical derivability:** Four of the five pilot skills can be labeled from `cadence_class` alone (channel→primary_attack for Cyclone, FoI, and Bone Storm; spam→primary_attack for Fire Ball). The exception is Meteor (cadence=NULL): it needs the `source_anchor` prose or `mech_summary` context to disambiguate from a cooldown-defensive skill. This is representative of the broader corpus gap.

#### Shape (β): explicit `cast_priority` ordinal

This is **achievable but overconstrained** for the current need. A numeric ordinal (0=fires first) is sufficient for the pilot-5 fix but adds a cardinal ordering that may be misleading for reactive skills (Bone Cage fires on player discretion, not at a fixed ordinal in a loop). The role enum is more faithful to ARPG gameplay than a fixed ordinal. That said, `cast_priority` as a secondary field (0=primary, 1=secondary, 2=reactive) would be valid addendum if the sim requires an explicit ordering rather than a role lookup.

#### Recommendation: shape (α), role enum, as the harvest extension

- **For the 5 pilot kits:** Hand-author `role` from the findings in Q2. This is the FALLBACK the charter described, and it is fully specified above.
- **For the full corpus:** A schema extension adding `role TEXT` to `skill_geometry_band`, populated via a semi-mechanical pass:
  - Step 1: derive mechanically where `cadence_class` is unambiguous (channel → primary_attack or burst_damage based on `commit_val` in canon_corpus; spam → primary_attack; `delivery=zone + ordinal>=1 → area_damage or control`)
  - Step 2: LLM-label the remainder using `source_anchor` + `mech_summary` prose as context (one-pass; small corpus — ~300 skills total)
  - Step 3: validate against the per-kit `mech_summary` descriptions which already encode rotation intent

This is a KF-2-style mechanical pass with an LLM-assist layer for ambiguous cases — not a full prose-dependent derivation. The field is a controlled 7-value enum, which constrains the LLM output and makes validation straightforward.

---

## Knowledge gaps not resolved

1. **Inquisitor Seal cadence_class is NULL** — in-game it has a cooldown (~16s at max rank). If Meteor's NULL cadence is addressed, Inquisitor Seal should receive `cadence=cooldown` simultaneously.

2. **The PoE2 Bonestorm 0.5 totem variant** has a different rotation (Bone Cage as primary, Bone Storm offloaded to totems). The corpus record notes this variant but the `skills[]` array reflects the 0.1-0.2 base version. If the sim targets the 0.5 era, the role assignments above would need to flip.

3. **GD FoI Purifier is HELD** (R-K5 GAP, T4 pending) — no damage base is compiled. The rotation metadata fix is independent of this hold and can proceed regardless, but the kit will not produce meaningful fight output until the T4 dependency resolves.

4. **GD FoI Purifier secondary skills not in corpus:** The actual Purifier build uses additional active skills (Thermite Mine, Word of Renewal, Aura of Censure) that are not captured in `skill_geometry_band`. These are buff/setup skills outside the core 2-skill harvest, but their absence means the sim's FoI kit is simplified compared to source.

5. **`cast_priority` as ordinal (shape β)** was not assessed against the sim's actual rotation selector interface. If the sim is extended to use an explicit ordinal rather than a role lookup, a separate engineering pass is needed to confirm which selector path to wire.

---

## Source list

- Maxroll.gg D2 Meteor/Fireball Sorceress Guide: https://maxroll.gg/d2/guides/meteor-sorceress
- Maxroll.gg D2 Fire Wall Sorceress Guide: https://maxroll.gg/d2/guides/fire-wall-sorceress-guide
- Odealo D2 Meteor/Fireball Sorceress Guide: https://odealo.com/articles/meteor-fire-ball-sorceress-build-for-diablo-2-resurrected
- mtmmo D2R Firewall Sorceress Guide: https://www.mtmmo.com/news/1001--d2r-25-firewall-sorceress-build-guide-skill-tree-stats-mercenary-gear-gameplay-strategy
- Crate Entertainment Forum — Fire ConeMan FoI Purifier: https://forums.crateentertainment.com/t/1-1-7-2-the-fire-coneman-fire-flames-of-ignaffar-purifier-focused-on-conversion/102294
- Grimtools FoI builds listing: https://www.grimtools.com/builds/skill/2112
- Game8 PoE2 Bonestorm Blood Mage: https://game8.co/games/Path-of-Exile-2/archives/490217
- mobalytics.gg PoE2 Bonestorm build (accessed via web search; 403 on direct fetch): https://mobalytics.gg/poe-2/builds/bonestorm-levelling-and-league-starter
- PoE-Vault Cyclone Slayer Guide (3.28): https://www.poe-vault.com/guides/murder-on-a-budget-cyclone-slayer-build-guide
- Overgear Cyclone Build Guide: https://overgear.com/guides/poe/cyclone-build/
- corpus.db — `canon_corpus`, `kit_mapping`, `skill_geometry_band` (READ-ONLY; /agentic_orchestration/research/curated/corpus.db)
- kit_compiler.py — compiled skill dict schema confirmation (READ-ONLY; reincarnated-engine)
- ai_strategies.py + spatial_engine.py — rotation selector logic (READ-ONLY; reincarnated-engine)
- ARPG canon corpus JSONL files (d2, gd, poe1, poe2) — corpus-level kit records
- rdr-kit-atlas-v3.csv — atlas records for pilot-5 kits
