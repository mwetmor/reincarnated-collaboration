# VDM-1 basin-5 batch-c02 — summary (tq c02, 10 kits)

**Date:** 2026-07-18
**Batch:** c02 · game=tq · negative=0 on all kits (no negative_canon family emitted)

---

## Per-kit one-liners

| kit_id | verdict summary | element attested |
|---|---|---|
| tq-onslaught-assassin | CONFIRMED across identity/mechanics/era. Warfare+Rogue Assassin; Onslaught as default-attack; dual-wield with pierce + poison overlay. | physical (dominant); poison rider via Envenom — **not attested as damage-type descriptor in fetched text**, only "Dex does [boost poison damage]". No explicit "deals physical damage" either. Element-silent. |
| tq-petmaster-summoner | CONFIRMED across identity/mechanics/era. Soothsayer (Nature+Spirit); wolves+Liche King proxy; reserve economy. | pets deal "physical damage" (wolves), "vitality damage" (Liche King), "elemental damage" (Nymph) — all three attested explicitly in fetched guide text. |
| tq-phantom-strike-dreamkiller | CONFIRMED across identity/mechanics/era. Dream+Rogue Dreamkiller; Phantom Strike vanish-teleport confirmed; Dream Stealer 360-arc. | pierce/physical: guide says "physical damage" for Phantom Strike in one source; pierce label from probe. Neither confirmed as explicit damage-type descriptor for the Phantom Strike skill in fetched text. Element-silent. |
| tq-ranger-hunting-nature | CONFIRMED across identity/mechanics/era. Hunting+Nature Ranger; Marksmanship primary; pierce damage explicitly named; wolves light proxy. | **pierce** attested: "Since your primary damage will be Pierce, you'll want to dump a ton of points into Dexterity" — explicit damage-type descriptor. |
| tq-rune-weapon-thunderer | CONFIRMED across identity/mechanics/era. Storm+Rune Thunderer (Ragnarok); Rune Weapon toggle-reserve; Thunder Strike lightning active. | **lightning** attested: "Thunderer (Rune & Storm) is the best build if you want to go for full elemental melee conversion" + Thunder Strike "fires a lightning attack." Explicit. |
| tq-shield-charge-conqueror | CONFIRMED across identity/mechanics/era. Warfare+Defense Conqueror; Shield Charge dash-lane confirmed; stun+disruption on charge; Onslaught sustained. | physical: no explicit "deals physical damage" descriptor in fetched text. Element-silent. |
| tq-ternion-bone-charmer | CONFIRMED identity (Spirit+Hunting Bone Charmer) and mechanics (Ternion triple projectile). Era CONFIRMED. **RED FLAG (internal inconsistency, not verdict ground):** canonical Bone Charmer = bow/spear pierce, never Ternion. Ternion variant is niche/non-canonical; kit is spec'd as Ternion variant. | **vitality** attested: "+% Vitality Damage will boost your DPS" from Soothsayer/Spirit mastery guides; Ternion fires vitality damage projectiles. Explicit. |
| tq-thane-storm-warfare | CONFIRMED identity and era. Mechanics: "Thunderous Strike" skill name NOT found in any fetched source — UNSUPPORTED (see mechanics note). Lightning melee + DW procs confirmed directionally. | **lightning** attested: "dual wielding elemental warrior class combining Storm and Warfare" + Lightning Bolt/Thunderball/Squall all explicitly lightning. |
| tq-trap-magician | CONFIRMED across identity/mechanics/era. Rogue+Storm Magician; traps as heavy proxy; traps count as pets; pierce damage primary from traps; Storm adds elemental overlay. | **pierce** attested (traps): DB elem_raw=pierce, consistent with "elemental knife thrower" and trap piercing-projectile behavior. Weak explicit descriptor in fetched text — community says "elemental damage" for Storm layer more clearly than "pierce damage" for trap shots. Note as **weakly attested**. |
| tq-warlock-poison-vitality | CONFIRMED across identity/mechanics/era. Rogue+Spirit Warlock; vitality+poison dual damage; Ternion+Envenom core; Deathchill Aura. | **poison** attested: "add Poison Damage as well as add other effects to your attacks" — explicit. **vitality** attested: "a vitality damage staff is strongly recommended ... leverages Deathchill Aura, which significantly reduces Vitality Resistance" — explicit. Both attested. |

---

## Verdict histogram (advisory — steward recounts from files)

| verdict | count |
|---|---|
| CONFIRMED | 28 |
| UNSUPPORTED | 1 |
| CONTRADICTED | 0 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions

**0 contradictions.** All CONTRADICTED verdicts = zero.

---

## UNSUPPORTED kits / families

- **tq-thane-storm-warfare / mechanics:** "Thunderous Strike" skill name not found in any fetched source. Searched Storm mastery skill lists and Thane community discussions. Sources name Lightning Bolt, Thunderball, Squall, Storm Surge — no "Thunderous Strike." Likely a probe-fact skill naming that doesn't match in-game skill name. Community confirms lightning proc on DW procs, and Squall for zone damage. The kit's broader mechanics (lightning melee Warfare+Storm) are confirmed; the specific skill name is UNSUPPORTED.

---

## SOURCE_NOT_FOUND kits

None. All kits found via Steam/community fallback after fandom 402.

---

## Dossier coverage

All 6 families emitted for all 10 kits = 60/60 rows. No abstentions. Coverage = 100%.

---

## Element-attestation summary (per kit)

| kit_id | elem_raw (DB) | attested? | evidence strength | anchor summary |
|---|---|---|---|---|
| tq-onslaught-assassin | physical | silent (no explicit descriptor in fetched text) | — | Dex boosts pierce; physical not named as damage type |
| tq-petmaster-summoner | physical | YES (wolf physical), YES (Liche King vitality), YES (Nymph elemental) | strong | "dealing 43-71 physical damage"; "vitality and elemental damage type buffs on gear" |
| tq-phantom-strike-dreamkiller | pierce | silent (physical mentioned but as stat not damage descriptor) | — | guide says "physical damage" incidentally; no clean descriptor for Phantom Strike |
| tq-ranger-hunting-nature | pierce | YES | strong | "Since your primary damage will be Pierce" |
| tq-rune-weapon-thunderer | lightning | YES | strong | "fires a lightning attack"; "full elemental melee conversion" |
| tq-shield-charge-conqueror | physical | silent | — | no explicit "deals physical damage" descriptor |
| tq-ternion-bone-charmer | vitality | YES | moderate | "+% Vitality Damage will boost your DPS"; Spirit mastery vitality theme |
| tq-thane-storm-warfare | lightning | YES | strong | "dual wielding elemental warrior"; Lightning Bolt/Thunderball/Squall all lightning |
| tq-trap-magician | pierce | WEAK | weak | Pierce implied by trap projectile behavior; Storm "elemental damage" clearer in text |
| tq-warlock-poison-vitality | poison + vitality | YES (both) | strong | "add Poison Damage"; "vitality damage staff"; "reduces Vitality Resistance" |

---

## Red flags

1. **tq-ternion-bone-charmer: Ternion variant is niche.** The canonical Bone Charmer = bow/spear pierce, no staff. One source explicitly: "never using a staff or Ternion." Ternion variant documented but noted as "probably won't be better than Oracle." The kit as spec'd is the Ternion variant — identity CONFIRMED as a real variant, but downstream mapper should note this is a non-canonical usage of the Bone Charmer class combination. elem_raw=vitality holds for the Ternion variant; pierce would be correct for the bow variant.

2. **tq-thane-storm-warfare: "Thunderous Strike" skill name unconfirmed.** No fetched source contains this exact skill name. May be a probe-fact artifact or informal community nickname. Actual Storm mastery active skills are Squall, Lightning Bolt, Thunderball, Storm Surge, Thunder Strike (Rune mastery). The kit mechanics are real; the named skill is the gap.

3. **fandom.com 402 blanket block.** titanquest.fandom.com returned 402 on all attempts. All verification conducted via Steam guides, almarsguides.com, alteredgamer.com, and community discussions. Canary dividend prediction validated.

4. **tq-trap-magician pierce attestation weak.** DB elem_raw=pierce but fetched text is clearer on Storm "elemental damage" layer than trap pierce-damage. Trap piercing behavior is implied by game mechanics but not quoted explicitly. Downstream mapper should note.

---

## Author credits (named)

- Almar (almarsguides.com): Ranger, Conqueror, Soothsayer, Warlock guides
- Bown (steamcommunity.com): Bone Charmer guide
- All others: anonymous community guides / discussion threads
