# Dossier — poe1 Blood Magic Keystone Kit

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster target:** K26 (blood-family build; the PoE1 keystone as the foundational genre-attestation for life-as-resource identity)
**Priority:** MED
**Corpus gap confirmed:** No blood-magic keystone record in `canon-corpus-poe1.jsonl` (poe1-autobomber, poe1-archmage, poe1-soulrend, etc. exist — none capture Blood Magic as primary defining mechanic)
**Crawl date:** 2026-07-12

---

## Identity

**Game:** poe1 (Path of Exile 1)
**Patch/era span:** 0.9 beta (pre-release, 2011) — 3.29 (ongoing); Blood Magic is one of the foundational keystone passives, present since the game's inception. Peak meta presence: 1.x–2.x era (pre-Vaal Pact nerf, when life regeneration could offset skill costs); continued presence in 3.x as a deliberate design choice for specific builds.
**Canon tier:** moderate (the keystone has deep history but the "Blood Magic as kit identity" builds peaked in early-era PoE; by 3.x it became a niche choice for specific synergies rather than a dominant meta staple)
**Folk names:** "Blood Magic build," "BM Caster," "Life-cost build," "RF Blood Magic" (most canonical specific form), "Dark Pact BM," "Blood Sacrifice build"
**Shipped / negative-canon status:** SHIPPED — present since PoE's inception; deeply attested; survived every major patch as a valid build approach.

## Build identity (2–4 sentences)

The Blood Magic keystone converts all skill costs from mana to life and sets maximum mana to zero, creating a build identity where life is the sole resource — attacked by both incoming damage and skill costs. The canonical form is the Righteous Fire (RF) + Blood Magic build: RF constantly burns the player's own life as a damage aura, while the keystone means all other skill activations also cost life, creating a unified life-economy that demands extreme life pool + regeneration investment. The cross-game family this record attests: GX-06 (self-damage economies), in which PoE1 Blood Magic is the foundational example of life-as-both-resource-and-weapon. The key design tension: Blood Magic creates maximum all-in resource concentration — you can never be mana-starved, but you CAN be life-drained by your own skills.

## Lineage

**Ancestors (cross-game):**
- D2 Sacrifice paladin (self-damage per hit — a distant precursor, the cost-as-damage flavor)
- D2 Blood Golem (life drain between necromancer and minion — bidirectional life economy)

**Descendants / within-PoE lineage:**
- PoE1 "The Covenant" unique body armor (Blood Magic support gem socketed — non-keystone shortcut to the mechanic for specific skills)
- PoE1 "Eldritch Battery" keystone (converts ES to mana) + "Mind over Matter" — conceptual cousin in the resource-unification space
- PoE2 Blood Mage ascendancy (direct lineage — skills cost life; GX-06 confirmed)
- D4 Blood Nova / Necromancer blood cost skills
- D4 Spiritborn resource variants
- Chronicon Warlock resource (partial evidence)
- RDR K26 ("Blood Sacrifice" — blood-family member; this mint provides the primary PoE1 genus-ancestor)

**GX reference:** GX-06 (self-damage economies) — this is a PRIMARY example, not peripheral evidence.

## Engine-prefix claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | MED | Canonical Blood Magic builds use Marauder/Juggernaut for maximum life pool (STR class). However, Witch (INT) RF builds also use Blood Magic; the keystone itself is class-agnostic. STR for the RF-Juggernaut canonical form; LOW confidence if recording the abstract keystone. |
| range | MID | LOW | Highly variable by build arm: RF (melee/self-radius), Dark Pact (self-targeted chaos spell = short range), Life-cost casters (ranged). RF = effectively melee range (self-burn AoE). Overall MID with LOW confidence. |
| tempo | LOW | MED | RF builds are "set and forget" — activation once, then movement through packs; low per-combat action density. Life-cost caster variants are higher, but the canonical RF arm is LOW tempo. |
| amp | FLAT | MED | RF produces consistent burning ground output; the damage is sustained flat-burn, not burst or variable per-hit. |
| proxy | SOLO | HIGH | Blood Magic builds are strictly solo-damage; life economy leaves no room for proxy management. |
| commitment | INSTANT | HIGH | RF toggle is instant; Dark Pact cast is instant; skill costs deducted from life are immediate. No wind-up or channel in the core Blood Magic commitment model. |

## Raw descriptors (not engine keys)

**geo:** RF = self-radius burning AoE (small, ~2–3 units); Dark Pact = self-targeted chaos nova (small AoE). Geography: tight, close-range. Player must be within visual range of enemies for RF to deal damage.

**ctrl:** Damage-pure for RF. Blood Magic by itself adds no CC. Dark Pact variant has some splash. The build's "control" is indirect — enemies near the player take continuous burn damage.

**mob:** Moderate-to-low mobility required; RF works while moving but enemies must catch up to you. Some Blood Magic builds are genuinely stationary (stand in RF and let enemies burn); others use it as a walking burn-clear.

**def:** Extreme life-investment; Kaom's Heart (massive life bonus) is the canonical life-stacking item. Juggernaut or Inquisitor ascendancy for consecrated-ground-based regeneration (offsets blood cost + RF self-burn simultaneously). The defense IS the life-regeneration economy — it covers both damage-in and cost-out.

**econ:** Life replaces mana entirely; life regeneration IS the "mana regen" equivalent. The economic model: incoming regeneration must exceed (skill costs per second + RF self-burn per second + enemy damage per second). Vaal Pact (leech-based) was a major economic enabler in early eras; post-3.5 nerf (Betrayal league), regeneration-based models became canonical.

**elem:** Fire primary (RF canonical form — self-applied burning damage); Chaos alternative (Dark Pact — chaos nova AoE; self-damage variant).

## Sources

- Knowledge base (kb) — Blood Magic keystone is foundational PoE1 mechanic from training data; present since 0.9 beta
- Blood Magic PoE Wiki (https://pathofexile.fandom.com/wiki/Blood_Magic) — confirms life-replaces-mana mechanic
- PoE Forum thread "Blood Magic Keystone Incinerate Marauder" (early-era build example)
- vhpg.com Blood Magic build reference
- V4-r2 §F4 mint-list (gandalf, 2026-07-12)
- GX-06 ledger entry (self-damage economies family)

## Knowledge gaps

- Blood Magic was implicitly present in all RF records already in the PoE1 corpus if they run RF — the question is whether those records' `proj` attribute already assigns Blood Magic as a defining mechanic note. Elrond should check if any existing PoE1 record carries Blood Magic in its build notes.
- "Dark Pact + Blood Magic" as a distinct build grain should be evaluated per G1 (does the loop change at lattice grain vs RF + Blood Magic? Answer: yes — different range, amp, geo → likely separate record)
- Era note: early PoE1 Blood Magic builds are deeply different from 3.x versions; era stratification rider applies
