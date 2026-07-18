# VDM-1 basin-4 batch-04 summary — 2026-07-18

**Batch:** b04 (10 kits) | **Mode:** B (systematic crawl) | **Primary source:** maxroll.gg

---

## Per-kit one-liners

- **la-nights-edge-souleater** — CONFIRMED identity/mechanics/era. Edge Meter + Soul Snatch loop verified; no Deathlord Mode entered. Co-viable with Full Moon per meta discourse.
- **la-order-emperor-arcanist** — CONFIRMED identity/mechanics/era. Class engravings replaced by Ark Passive Enlightenment tree (notable schema flag). Emperor card = Deck Meter booster confirmed. Oct 2025 patch added new core combination.
- **la-peacemaker-gunslinger** — CONFIRMED identity/mechanics/era. Unified stance buffs confirmed via "Pacifist" mechanic. Mech_note said "more complex than Time to Hunt but all-stance capable" — confirmed.
- **la-perfect-suppression-shadowhunter** — CONFIRMED identity/era. Demon Form disabled confirmed. Specific bonus percentages (+30% damage/+50% Shadowburst Meter generation) UNSUPPORTED — guide describes mechanic but does not give those exact figures.
- **la-phantom-beast-awakening-wildsoul** — CONFIRMED identity/mechanics/era. Ship date verified (2026-02-26). Stack CDR confirmed at 5%/stack, mana 2%/stack. Era stamp la-wildsoul-2025-02-26 CONFIRMED.
- **la-pinnacle-glaivier** — CONFIRMED identity/era. CONTRADICTED on buff values: corpus claims +20%/+50% per Focus switch and +15%/+25%/+15% per Flurry switch; fetched text gives unified switch values (+15% ATK SPD, +25% DMG, +15% MVT SPD, +60% Crit DMG) with no per-stance split.
- **la-predator-slayer** — CONFIRMED identity/mechanics/era. Fatigue/Exhaustion loop confirmed verbatim. "sustained female Berserker analog" claim not contradicted.
- **la-punisher-slayer** — CONFIRMED identity/mechanics/era. Shorter cyclical burst vs Predator sustained confirmed. Specialization-scaling claim UNSUPPORTED (guide gives stat split but doesn't assert Punisher scales more aggressively than Predator).
- **la-rage-hammer-destroyer** — CONFIRMED identity/mechanics/era. Builder-spender loop confirmed. "Mobile throughout compared to GT's locked Hypergravity phase" confirmed by implication (GT comparison notes burst-only Hypergravity; RH is consistent).
- **la-rage-hammer-destroyer-bt** — Negative kit. CONTRADICTED: the negative_canon claim that BT is the "losing side of a Destroyer identity comparison" is wrong on two grounds: (1) BT is a Berserker identity, not a Destroyer identity; (2) fetched meta does not classify BT as dominated — both BT and Mayhem are co-viable per maxroll + community sources. The corpus mech_note itself flags this as an internal inconsistency ("NOT a record — redundancy note").

---

## Verdict histogram (advisory — file truth is the count)

| Verdict | Count |
|---|---|
| CONFIRMED | 28 |
| CONTRADICTED | 3 |
| UNSUPPORTED | 2 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions (one line each)

1. **la-pinnacle-glaivier / mechanics**: Corpus claims per-stance split buffs (+20%/+50% crit damage for Focus switch, +15%/+25%/+15% for Flurry switch); fetched text shows unified switch values (+15% ATK SPD, +25% DMG, +15% MVT SPD, +60% Crit DMG) with no per-stance differentiation. Values also diverge numerically (corpus: +50% crit damage; source: +60% crit damage).
2. **la-rage-hammer-destroyer-bt / negative_canon (claim: losing Destroyer identity)**: BT is a Berserker identity, not Destroyer. This is a kit_id naming/slot error in the corpus. The negative_canon claim is wrong by identity class.
3. **la-rage-hammer-destroyer-bt / negative_canon (claim: strictly dominated)**: Fetched meta (maxroll + community) confirms BT and Mayhem are co-viable; BT has higher burst ceiling, Mayhem has better uptime. Neither is "strictly dominated." Mayhem is more popular but BT is not off-meta/niche/dead.

---

## SNF kits

None. 0 SOURCE_NOT_FOUND. All 10 kits resolved via maxroll.gg (primary) + official playlostark.com (Wildsoul ship date) + WebSearch (BT meta discourse).

---

## Dossier coverage

All 6 families attested for all 10 kits. 0 abstentions. Coverage: 100% (60/60 family rows filled, 0 null payload_json rows).

---

## Author credits (unique handles, this batch)

- **Sekwah** — la-nights-edge-souleater, la-order-emperor-arcanist, la-perfect-suppression-shadowhunter, la-phantom-beast-awakening-wildsoul, la-punisher-slayer (5 kits)
- **Raeinor** — la-peacemaker-gunslinger, la-pinnacle-glaivier, la-predator-slayer (3 kits)
- **Civo** — la-rage-hammer-destroyer, la-rage-hammer-destroyer-bt (2 kits)
- **Perciculum** — reviewer credit on 8 of 10 kits (all except la-rage-hammer-destroyer-bt and la-order-emperor-arcanist where reviewer credit was absent or unclear)

---

## Element-attestation summary

**Element-silent kits (D4 name-only law applied — no element attested):**
- la-peacemaker-gunslinger — ranged bullet damage; no elemental type
- la-perfect-suppression-shadowhunter — "Shadow Shards" and "Shadow Injection" appear in text as buff mechanic names, NOT as damage-type descriptors; element-silent per D4
- la-nights-edge-souleater — no elemental damage type in fetched text; dark/demonic theme not sufficient; element-silent
- la-pinnacle-glaivier — no elemental descriptor in fetched text; positioning-typed (back attack); element-silent
- la-predator-slayer — skill names include "Volcanic Eruption" and "Flame Deathblade" but fetched text does NOT describe fire damage AoE or fire damage type; these are skill names only; element-silent per D4
- la-punisher-slayer — same as Predator; melee burst with no elemental damage typing in text; element-silent
- la-phantom-beast-awakening-wildsoul — Fox Flame skill name present; text does NOT describe fire damage type; element-silent per D4
- la-rage-hammer-destroyer — "Gravity" appears as damage-type descriptor (Gravity Release, Gravity Cores, Hypergravity); however "gravity" is not in the engine element family and is an LA identity-mechanic term, not an element in the D4 sense; recorded as identity-typed, element-silent for engine mapping
- la-rage-hammer-destroyer-bt — physical/melee only; element-silent
- la-order-emperor-arcanist — "Destruction damage" noted for Mysterious Stampede; this is a CC/stagger damage category in LA (not an element); element-silent

**No element attestations across the full b04 batch.** This batch is uniformly physical/identity-typed. No stretch assignments made.

---

## Red flags

1. **la-rage-hammer-destroyer-bt slot error**: The kit_id and folk_name reference "Berserker's Technique vs Mayhem (Destroyer comparison)" but the actual class is Berserker, not Destroyer. The corpus mech_note itself acknowledges this is "NOT a record — redundancy note." The negative=1 flag is mismatch — fetched meta shows both BT and Mayhem are co-viable. Recommend elrond review whether this slot should be retired (negative=0 BT guide exists and is canonical) or reframed.
2. **la-pinnacle-glaivier buff value divergence**: Canon corpus records per-stance split buffs. Fetched maxroll (June 2026) gives a single unified set of stance-switch buffs with no per-stance differentiation, and the crit damage figure differs (corpus +50%, source +60%). The corpus values appear to reference an older Ark Passive configuration. Recommend elrond flag for schema correction.
3. **la-order-emperor-arcanist Ark Passive schema note**: Class engravings for Arcanist (Empress's Grace / Order of the Emperor) were removed and replaced by the Enlightenment Ark Passive tree. The engraving field in canon_corpus may be stale for this class — the spec identity is now Ark Passive path, not class engraving. Downstream mapping should not map "engraving" as the differentiation mechanism.
4. **la-perfect-suppression-shadowhunter specific percentages**: The +30%/+50% bonus figures in mech_note are UNSUPPORTED by fetched text. The mechanic is confirmed but the exact values were not quoted in the maxroll guide. Low risk — these figures may be from official skill descriptions not captured in the build guide layer.
