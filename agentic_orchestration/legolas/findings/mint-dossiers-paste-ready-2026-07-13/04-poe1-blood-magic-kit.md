# Mint Kit Dossier — poe1-blood-magic-kit

**corpus_kit_id:** `poe1-blood-magic-kit`
**folk_name:** Blood Magic Life-as-Resource (Righteous Fire / Exsanguinate / Corrupting Fever)
**game:** poe1
**status:** positive
**era_year:** 2015
**stabilization_patch:** v2.0.0 (The Awakening expansion, July 9, 2015 — Righteous Fire rework established the canonical RF+Blood Magic self-sustain loop)
**for_roster_kits:** K26
**mint_priority:** MED
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## Provenance + Genre Lineage

The Blood Magic keystone is a passive skill node in PoE1's passive tree that replaces mana with life as the universal spellcasting resource (skills cost life instead of mana; maximum mana is set to zero). It has existed since PoE's open beta (January 2013) and represents one of the earliest instances of the "life-as-resource economy" archetype in ARPGs — a design where the player's HP pool serves double duty as both survival buffer and action economy. The lineage:

- **D2 Paladin Sacrifice** (negative-canon ancestor): paid 8% current HP per melee hit — the genre's first named "self-cost" mechanic, though as a fringe/non-viable primary build
- **PoE1 Blood Magic keystone (2013+):** systematized life-as-resource at the passive tree level; makes ALL skills pay from life, not just one skill
- **PoE1 Righteous Fire (RF) + Blood Magic (dominant chassis):** RF burns HP continuously but builds using Life Leech, Endurance Charges, and Regen can sustain the HP burn; RF+BM = the genre's canonical "burn your own life to power your offense" identity

The RF+BM combination crystallized as the dominant corpus-genus entry for K26 (Blood Mage / self-cost identity) after the Righteous Fire rework in v2.0.0 (2015). Pre-2.0, RF was considered a novelty/suicidal mechanic; post-2.0, RF Elementalist/Chieftain with BM became a stable league-start build documented across multiple meta cycles. Later chassis iterations include Corrupting Fever (physical-damage over time with BM) and Exsanguinate (blood-spreading projectile) in the 3.x era.

PoE2 has a parallel "Blood Mage" Witch ascendancy (post-training-cutoff) that carries this lineage forward into the PoE2 ecosystem — but the corpus entry is for the foundational PoE1 form.

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| January 2013 | PoE Open Beta | Blood Magic keystone added to passive tree; niche usage; no dominant chassis yet |
| 2013–2014 | v1.x | Righteous Fire existed but was suicidal/non-viable as a primary build without extreme gear; BM+RF = fringe |
| **July 2015** | **v2.0.0 (The Awakening)** | **Stabilization** — Righteous Fire reworked: now deals fire damage in an AoE around the player based on HP; Chieftain ascendancy (3.x) and Elementalist both support the RF sustain loop; BM+RF becomes viable league-starter meta |
| 2016–2018 | v2.2.0–3.2.x | RF+BM documented as a popular entry-level league-starter; multiple community guides; Hierophant + RF totem sub-variant also emerges |
| 2019–2020 | v3.7.0–3.12.x | Corrupting Fever and Exsanguinate added as alternative Blood Magic chassis; bleed-spreading and projectile-spreading blood builds emerge |
| 2021–2023 | v3.13.0–3.25.x | RF remains a consistent league-starter meta choice; Chieftain rework (3.16?) further supports; PoE ninja shows RF builds in significant proportions each league |
| 2024–2026 | v3.26–3.29 | RF Inquisitor becomes popular alternate chassis; BM keystone remains core to all RF variants |

## Mechanical Identity

The Blood Magic Life-as-Resource kit has two levels of identity: (1) the KEYSTONE MECHANIC — Blood Magic converts life to the universal casting resource, enabling "mana-irrelevant" caster builds that stack life instead; (2) the CANONICAL CHASSIS — Righteous Fire (or Corrupting Fever / Exsanguinate in later eras) as the primary skill, powered by a massive life pool + life regeneration + leech loop to sustain the life-burn cost. The player walks through enemies, periodically casting skills that drain life, while life regeneration and leech maintain a net-zero or positive life balance.

K26 (Blood Mage / self-cost economy) maps precisely to this genus — the defining cross-game entry for "HP is the casting resource" archetype. PoE1's Blood Magic is the genre's systemic expression of what D2 Sacrifice does as a one-skill trick: the whole economy runs on life.

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | INT | MED | Canonical RF/BM chassis uses Witch/Scion starting area (INT-adjacent); Chieftain and Inquisitor are STR ascendancies but the keystone mechanic is INT-flavored (spellcaster economy). Note: RF+BM is CLASS-agnostic — BM is accessible from any start point. The corpus entry targets the INT (Occultist/Witch) chassis as primary. |
| range | mid | LOW | RF is a self-origin AoE (player burns enemies in radius around themselves — mid-range); Exsanguinate is projectile (mid-range); Corrupting Fever is aura (player walks into enemies = melee-to-mid). Low confidence because chassis varies. |
| tempo | high | MED | RF builds walk continuously through enemies (high movement = high action density at the terrain level); Exsanguinate cast rate is high; the life-leech loop requires sustained hits. Aggregate tempo is high even though individual cast rate may be moderate. |
| amp | flat | MED | RF damage is constant (burning aura); Corrupting Fever DoT is continuous; Exsanguinate blood-spreading is also consistent DoT. All canonical BM chassis produce FLAT amplitude output (no burst; sustained damage). |
| proxy | solo | HIGH | Player-cast skills; no proxy entities; the player IS the damage actor. Blood Magic is explicitly a self-cost economy, not a proxy economy. |
| commit | instant | HIGH | RF toggle is instant (no cast time in canonical builds); Exsanguinate is instant-cast; Corrupting Fever is instant. The economy mechanic (life cost) is a resource price, not a commitment delay. |

## Raw Descriptors

**geo:** Varies by chassis: RF = self-origin AoE (fire aura in radius around player); Exsanguinate = blood projectile (chain-hop spreading pattern); Corrupting Fever = persistent DoT aura. The canonical corpus entry references RF as primary chassis: self-origin continuous-damage aura.

**ctrl:** RF: no CC; damage-only. Exsanguinate/CF: bleeding ailment (minor slow in some configurations). Control is not the build's identity.

**mob:** RF is a "walk through enemies" build — continuous movement, no rooting while dealing damage. Player mobility is HIGH; the build does not stop to cast (RF is always active; player walks). Exsanguinate arm requires brief cast pauses.

**def:** High life stack + life regeneration (to sustain RF burn) + Endurance Charges (physical mitigation). Armor-based typically. The defense IS the build's offensive economy — maintaining a massive life pool that both absorbs damage and sustains the self-burn cost. "Sustain" is the defense model.

**econ:** Self-cost (life). Blood Magic keystone: all mana costs converted to life costs; maximum mana = 0. Builds counteract the ongoing HP drain via Purity of Fire (reduces fire self-burn %), Vitality (flat life regen), Endurance Charges, and life leech from linked supports. Net economy goal: positive life balance each second (regen > burn) — a continuous equilibrium loop rather than a spend-then-recover rhythm.

**elem:** Fire primary (RF; the self-burn IS the damage element). Corrupting Fever arm: physical (chaos conversion). Exsanguinate arm: physical/chaos. The defining element for K26 pedigree purposes is fire (RF as canonical chassis).

## Sources (live URLs)

- [Blood Magic — Path of Exile Wiki (Fandom)](https://pathofexile.fandom.com/wiki/Blood_Magic) — primary keystone documentation (LIVE — confirmed in search 2026-07-13)
- [Blood Magic | PoE Wiki](https://www.poewiki.net/wiki/Blood_Magic) — official wiki URL (403 at fetch time; URL is valid canonical location)
- [Blood Magic Build Guide — vhpg.com](http://www.vhpg.com/blood-magic/) — PoE build guide with keystone context (LIVE — in search results 2026-07-13)
- [PoE2 Blood Mage Ascendancy — Maxroll](https://maxroll.gg/poe2/build-guides/fireball-blood-mage-build-guide) — PoE2 successor documenting lineage; confirms BM keystone ancestry (LIVE)
- [PoE2 Blood Magic Synergy — MMOJUGG](https://www.mmojugg.com/news/poe2-blood-magic-synergy-with-blood-mage.html) — cross-game lineage note (LIVE)

## Knowledge Gaps

- Elrond: reconcile against any existing PoE1 RF records — is this a new standalone record for the "Blood Magic as economy chassis" or should it be a note on an existing RF record? Recommendation: standalone `poe1-blood-magic-kit` corpus row focused on the KEYSTONE MECHANIC as the build identity, with RF as the canonical chassis.
- The Spell Totem + Blood Magic arm (totem pays the life cost = GX-19 / commitment-absorption variant) is a separate corpus entry candidate (`poe1-forbidden-rite` covers this in the proxy cluster)
- Post-3.25 RF meta tier (Inquisitor arm emergence) not measured via live data
