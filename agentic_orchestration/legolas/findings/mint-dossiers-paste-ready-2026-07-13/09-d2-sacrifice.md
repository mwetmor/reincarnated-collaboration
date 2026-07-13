# Mint Kit Dossier — d2-sacrifice

**corpus_kit_id:** `d2-sacrifice`
**folk_name:** Sacrifice (Paladin)
**game:** d2
**status:** positive (with negative-canon annotation — never meta-viable as primary loop; self-damage spiral prevents sustained use)
**era_year:** 2001
**stabilization_patch:** NULL (no stabilization era — Sacrifice never achieved a meta-dominant build identity; existed from D2 Lord of Destruction launch as a fringe/utility skill)
**for_roster_kits:** K26
**mint_priority:** LOW
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## Provenance + Genre Lineage

Sacrifice is a Diablo 2 Lord of Destruction Paladin skill in the Combat Skills tree, available from character level 1. Its defining mechanic: each melee strike with Sacrifice deals bonus physical damage (+80% at rank 1, scaling to +250% at rank 20) in exchange for 8% of the current hit's physical damage being dealt back to the Paladin as unavoidable self-damage. At higher ranks (post-D2R patch 2.4): self-damage is reduced by 1% per skill level (so rank 20 = 8% - 20% = actually 0% self-damage at max rank, per new scaling).

Genre significance: Sacrifice is the ARPG genre's earliest named "self-cost melee strike" archetype — a single-skill attack that trades player HP for enhanced damage output. It predates PoE1's Blood Magic keystone (2013) and the "life-as-resource" economy concept by over a decade. Its negative-canon status comes from practical unviability: the 8% self-damage is before life leech application, creating a damage spiral that kills the Paladin at low HP levels even with strong life-leech gear.

**Self-damage mechanic details (verified via live sources 2026-07-13):**
- "Each hit inflicts 8% of its damage on the Paladin" (Diablo Fandom wiki)
- "Life is reduced before life steal and Life Tap are applied, so using Sacrifice while at low HP can be fatal, even with sufficient life steal" (Diablo2 wiki)
- D2R patch 2.4 (April 2022): "Damage to Self is reduced by leveling up, from 8% (Before Patch) to 8% - [1% per level]" — at max rank, self-damage approaches 0% effectively

**Genre lineage:**
- **No meaningful ARPG ancestor** — Sacrifice is the genre's founding entry for named melee self-cost mechanics
- **Descendants:** PoE1 Blood Magic keystone (life-as-universal-resource, 2013); PoE1 Forbidden Rite (totem pays life cost, GX-19); PoE1 Corrupting Fever (DoT sourced from hit self-damage); D4 Blood Surge Necromancer (life sacrifice for skill power); LE Forge Guard Hemorrhage (limited self-cost trade)
- **K26 lineage anchor:** Sacrifice is the most direct corpus ancestor for K26's self-cost economy genus — the earliest named expression of "trade HP for damage output"

**GX-06 evidential value:** Even as negative-canon, Sacrifice documents the genre's FIRST melee self-cost expression. It is important for the corpus as a negative discriminator — showing WHERE the self-cost mechanic was too punishing to be a primary build loop without a sustain mechanism. This is why the previous session recommends: NEGATIVE CANON + mint (for evidential value, not positive-canon status). This dossier concurs.

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| June 2001 | D2 Lord of Destruction launch | Sacrifice added to Paladin Combat Skills tree; 8% self-damage; immediately identified as a high-risk/fringe skill; virtually no primary-loop builds documented |
| 2001–2012 | v1.07–v1.13 | Sacrifice remains fringe; the Zealot Paladin (Zeal skill) dominates D2 Paladin melee builds; Sacrifice used only in hybrid "Auraradin" builds for its attack speed synergies |
| April 2022 | D2R v2.4 | D2R patch 2.4 reduces self-damage scaling per level; at rank 20 this effectively removes self-damage. This patch makes Sacrifice theoretically more viable as a primary attack, but the build has never entered meta documentation even post-2.4 |
| 2022–2026 | D2R v2.5+ | Project Diablo 2 (fan mod, S13) documents a Sacrifice Paladin build — this is the ONLY documented "primary loop" Sacrifice build found; it is in a heavily-modified fan mod context, not vanilla D2 |

**Note on Project Diablo 2 documentation:** The Odealo guide "[S13] Sacrifice Paladin Build – PD2 Guide" (https://odealo.com/articles/sacrifice-paladin-build-guide-for-pd2) documents a Season 13 PD2 build. PD2 is a modded version of D2 with different balance parameters. This does NOT establish Sacrifice as a meta-viable kit in vanilla D2/D2R — it confirms the skill is interesting enough to build around in a modded context, but the negative-canon status for the vanilla corpus entry is unchanged.

## Mechanical Identity

Sacrifice is a single-target melee strike that deals massively amplified physical damage at the cost of a percentage of that damage reflected back to the Paladin as self-damage (unavoidable, applied before life leech). The identity: "maximum single-hit physical damage with continuous self-harm as the economy cost." Unlike PoE1's Blood Magic (where the player sustains via regen/leech to maintain net-positive HP), Sacrifice creates a damage spiral that is only mitigated by life leech (which requires the hit to be large enough to leech more than the 8% self-damage) or by reaching rank 20 in D2R (eliminating the self-damage).

This is negative-canon because: (1) the Paladin's own Attack Speed is not high enough to sustain the leech loop; (2) Zeal is strictly superior for melee Paladins (multi-hit with no self-damage); (3) the skill has no AoE or crowd control; (4) it provides only damage scaling where the downside (self-damage before leech) creates a death spiral at medium health levels.

**Practical viability threshold:** To negate self-damage, life leech must return MORE than 8% of hit damage per hit. Vanilla D2 nightmare requires 16% leech to break even; Hell difficulty requires 24%+ leech. These are achievable thresholds but require specific gear; the Paladin's offense does not benefit from that gear as much as the leech mitigation costs.

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | HIGH | Paladin = STR primary class in D2 (Strength governs Paladin gear requirements and melee damage); Sacrifice is a melee-physical skill scaling with weapon damage (STR-dependent) |
| range | melee | HIGH | Single-target melee strike; no range; Paladin must be adjacent to enemy |
| tempo | med | MED | Standard melee attack cadence; Sacrifice itself has no cooldown or animation modification; tempo = whatever the Paladin's base Attack Speed allows. Not particularly high or low. |
| amp | spiky | MED | Per-hit bonus damage is very high (250% at max rank); but the "spike" is consistent per-hit rather than burst-then-cooldown. "Spiky" reflects the high-variance self-damage feedback loop (each hit's self-damage spikes the player's HP down). |
| proxy | solo | HIGH | Solo melee attacker; no proxies; Paladin is always the damage dealer |
| commit | instant | HIGH | No cast time; immediate melee strike on activation |

## Raw Descriptors

**geo:** At-target single-hit melee strike: Sacrifice strikes one adjacent enemy for amplified physical damage. No AoE; no bounce; no splash. Single-target point delivery.

**ctrl:** No CC from Sacrifice directly. Holy Shield aura (common alongside) provides block. Zeal (alternative) has knockback. Sacrifice: pure single-target physical hit.

**mob:** Paladin has standard movement; Sacrifice does not restrict or enhance mobility. The build's mobility is "walk to enemy + hit" — no mobility tools native to the skill.

**def:** Armor + Block primary (Paladin defensive archetype). The self-damage mechanic creates a defense tension: you need life leech to sustain the loop, which constrains gear choices. A "damage-your-own-defense-by-attacking" economy.

**econ:** HP self-cost (8% of hit physical damage, before leech). The economy tension: large hits = large self-damage; require large leech return. At D2R patch 2.4 rank 20: self-damage effectively 0% (the self-cost is gone at max rank). Pre-2.4 or lower ranks: self-cost loop is the defining economic feature. Also: Sacrifice makes attacks independent from the Mana pool (no mana cost) — a minor advantage for aura-heavy Paladin builds that drain mana.

**elem:** Physical (Sacrifice is a physical melee hit; no elemental component). Note: The "holy" aura damage from Conviction or Blessed Hammer (common build companions) is a SEPARATE damage source. Sacrifice's own hit = physical only.

## Sources (live URLs)

- [Sacrifice (Diablo II) — Diablo Wiki (Fandom)](https://diablo.fandom.com/wiki/Sacrifice_(Diablo_II)) — primary skill documentation; confirms "8% of damage inflicted on Paladin" mechanic (LIVE — confirmed in search 2026-07-13)
- [Sacrifice — Diablo2 DiabloWiki](https://diablo2.diablowiki.net/Sacrifice) — D2 fansite wiki; details leech requirements (16%/24% for break-even at Nightmare/Hell) and skill scaling (LIVE)
- [Sacrifice | Diablo 2 Fextralife Wiki](https://diablo2.wiki.fextralife.com/Sacrifice) — additional documentation (LIVE)
- [Sacrifice — Diablo 2 PureDiablo Wiki](https://www.purediablo.com/d2wiki/Sacrifice) — PureDiablo reference (LIVE)
- [Sacrifice Paladin PD2 Build Guide — Odealo](https://odealo.com/articles/sacrifice-paladin-build-guide-for-pd2) — Project Diablo 2 Season 13 documentation (LIVE; note: modded context, not vanilla D2)
- [Combat Skills (Paladin) — Project Diablo 2](https://wiki.projectdiablo2.com/wiki/Combat_Skills_(Paladin)) — PD2 wiki with D2R 2.4 damage-to-self scaling per level (LIVE)
- [Paladin Combat Skills — PureDiablo](https://www.purediablo.com/diablo-2/paladin-combat-skills) — comprehensive combat skills documentation (LIVE)

## Knowledge Gaps

- **Matt ruling requested (carried forward from 2026-07-12):** The original commission flagged "arguably negative-canon; Matt rules." Legolas recommendation (unchanged): NEGATIVE CANON annotation on a MINTED RECORD — the skill is real, historically documented, and provides GX-06 evidential value as the genre's founding self-cost melee archetype. Elrond should mint the row with `negative: true` unless Matt rules otherwise.
- D2R patch 2.4 scaling confirmed (source: PD2 wiki): "8% - [1% per level]" — at rank 20 this is 8% - 20% = effectively 0% self-damage (the math produces a negative result, suggesting damage floor = 0%). The exact floor calculation not confirmed (may cap at 0%, not go negative).
- No vanilla D2/D2R meta documentation found for Sacrifice as a primary-loop build; the only primary-build documentation is in the heavily-modified PD2 (Project Diablo 2) context.
