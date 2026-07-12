# Dossier — poe1 Totem Archetype (Hierophant / Ancestral Warchief)

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster target:** K18 (deep-iconic harvest hole — totem archetype absent from PoE1 corpus; present only in poe2/gd/le)
**Corpus gap confirmed:** No totem record in `canon-corpus-poe1.jsonl`
**Crawl date:** 2026-07-12

---

## Identity

**Game:** poe1 (Path of Exile 1)
**Patch/era span:** 2.2 (Ascendancy league, March 2016, Hierophant ascendancy introduced) — 3.29 (ongoing); Ancestral Warchief gem introduced ~2.5 (Breach league, December 2016). Continuous meta presence 10+ years in various forms.
**Canon tier:** deep
**Folk names:** "Ancestral Warchief Totem," "AW Totem," "Warchief Hierophant," "Totem Build," "Hierophant Totem," "Spell Totem Hierophant" (two sub-arms of same archetype)
**Shipped / negative-canon status:** SHIPPED — deep canon across multiple eras; repeatedly chosen as league-starter tier by community guides; nerf-survivor (totems were gutted multiple times across 3.x patches yet the Hierophant arm persisted).

## Build identity (2–4 sentences)

The Hierophant/Ancestral Warchief totem archetype is PoE1's defining expression of the "proxy executor" identity: the player places totems that attack enemies while the player repositions, places additional totems, and absorbs any passive buffs granted by the totems' presence. Ancestral Warchief specifically grants a "more melee damage" and "more attack speed" buff to both the player and the totem while the totem is active, creating a joint-benefit loop. Hierophant's ascendancy notables (especially "Pursuit of Faith" for totem placement speed + additional totem, and "Conviction of Power" for Power/Frenzy charge generation via totems) enable stacking 3–4 simultaneous Warchiefs. A second arm — Spell Totem Hierophant — uses the same ascendancy with spell totems (e.g., Lightning Tendrils, Detonate Dead) as the proxy casters instead, producing a distinct tempo profile.

## Lineage

**Ancestors (cross-game):**
- D2: Necromancer Skeleton Army (heavy proxy; different commitment model but proxy-executor root)
- D2: Druid Summon Wolves / Vines (light proxy; stationary support character)
- GD: "Conjurer" builds (pet/totem hybrid roots)

**Descendants / related records (PoE ecosystem):**
- poe2-archmage-totems-oracle (PoE2 version; INT arm; recorded in corpus)
- poe2-warbringer-totem (PoE2 STR arm with damage-absorption mechanic; GX-19 evidence)
- GD totem variants (Demolitionist / Shaman summoner builds)
- LE Primalist Spriggan form (proxy-creation variant)

**Within-PoE lineage:**
- PoE1 "Ancestral Bond" keystone (removes direct damage, allows infinite totems) — a purer expression of the concept that predates Hierophant
- "Spell Totem Support" gem (pre-Hierophant era, 1.x builds) = the founding vessel; Hierophant systematized it

## Engine-prefix claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | MED | Ancestral Warchief is a STR attack skill (weapon-based); Hierophant (Templar) is STR/INT class; the Warchief-melee arm runs STR nodes for weapon/physical damage; the Spell Totem arm is INT. This record covers the canonical Warchief arm. |
| range | MID | MED | Player places totems at mid-field and retreats; totem attacks are melee-range from totem's fixed position; player's own positioning is typically 20–30 units from enemies (not melee-adjacent, not max-range) |
| tempo | LOW | MED | Player's action cadence is LOW: place 3–4 totems, wait, reposition; totems provide continuous output. Action density is low even if kill speed is high. Spell Totem arm may reach MED. |
| amp | FLAT | MED | Warchief grants a stable "more damage" multiplier; totem slam output is consistent once all totems placed; no significant per-hit variance. |
| proxy | HEAVY | HIGH | Totems deal all primary damage; player provides placement, buff absorption, and defense. In pure Ancestral Bond builds, player cannot deal direct damage at all. |
| commitment | INSTANT | HIGH | Placing a totem is an instant action (no cast time in canonical builds; gem quality can add cast time but baseline is instant). |

## Raw descriptors (not engine keys)

**geo:** Large AoE ground slam; Warchief's slam creates a wide cone/circle at melee range from the totem position; effective at clearing clustered enemies near the totem.

**ctrl:** Damage-pure; no meaningful CC from the Warchief slam itself beyond knockback splash on nearby enemies.

**mob:** Player has full mobility while totems persist; totems are stationary. Gameplay loop: place → move → avoid hits → reposition → refresh totems. Very high player maneuverability relative to DPS output.

**def:** Typically life-based tank OR Aegis Aurora block-based; totems draw enemy aggro reducing player threat. Hierophant's own defenses are secondary to the kit's proxy aggro-management.

**econ:** Mana per totem placement (3–4 mana costs per engagement refresh); Spirit of Ruin amulet can provide free totem placements; "Sanctuary" ascendancy node provides free charges. Totem death triggers replacement cost. Low ongoing econ pressure.

**elem:** Physical primary (Warchief hits with weapon); common conversion to fire or cold via Herald of Ash / Hatred. Pure elemental Spell Totem arm uses the element of the socketed spell.

## Sources

- Knowledge base (kb) — attested PoE1 mechanic from training data; lived for 10+ years of documented builds
- Icy Veins / Maxroll totem build guides (referenced via web search, URLs not directly fetched due to 403 errors)
- PoE1 Ascendancy patch notes 2.2 (Hierophant ascendancy addition)
- V4-r2 §F4 mint-list (gandalf, 2026-07-12)
- `agentic_orchestration/gandalf/views/V4r2-roster-adjacency-rebuilt.md` (K18 context)

## Knowledge gaps

- Specific per-league usage %, patch-note arc from 3.x totem nerfs (3.7 Synthesis nerf, 3.9 Conquerors totem-limit changes) not verified via live sources
- "Spell Totem Hierophant" sub-arm should potentially be a separate mint if loop diverges at lattice grain (G1 check owed)
- Post-3.25 (Settlers/Mercenaries era) totem meta status not verified
