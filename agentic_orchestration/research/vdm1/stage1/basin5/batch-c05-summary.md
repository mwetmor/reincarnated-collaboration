# VDM-1 basin-5 batch-c05 — Undecember (ud-) — Summary

**Batch:** c05 | **Game:** undecember | **Date:** 2026-07-18 | **Kits:** 12 | **Negative-canon kits:** 0

---

## Per-kit one-liners

| kit_id | verdict summary | element attested | notes |
|--------|----------------|-----------------|-------|
| ud-cwc-spin-caster | identity CONFIRMED / mechanics CONFIRMED / era CONFIRMED | cold (Blizzard proc); physical (Whirlwind base) | Era-U wall: S7 only |
| ud-flamethrower-channel | identity CONFIRMED / mechanics CONFIRMED / era UNSUPPORTED | fire — "Deal Fire DMG to enemies when maintaining Focus" (thein.ru) | Launch-era claim not attested; Arson DoT confirmed |
| ud-ice-crystal-arrow | identity CONFIRMED / mechanics CONFIRMED / era CONFIRMED | cold — "Shoots a Cold Arrow" + Chill/Freeze ailments (thein.ru) | Chain-bounce confirmed; tracking-projectile Verity variant |
| ud-illusion-family | identity CONFIRMED / mechanics CONTRADICTED / era CONFIRMED | physical (Illusion Arrow) — no element word as damage descriptor | CONTRADICTION: corpus claims at-target echo copy spawning; source shows stack-proc auto-fire from caster |
| ud-lightning-vortex | identity CONFIRMED / mechanics CONTRADICTED / era CONFIRMED | lightning — "deal Cleave Lightning area DMG, followed by a vortex that inflicts Vortex Lightning DMG" (pocketgamer) | CONTRADICTION: corpus claims ranged cast at-target; source confirms MELEE weapon swing + vortex |
| ud-multishot-link | identity CONFIRMED / mechanics CONFIRMED / era UNSUPPORTED | none (host skill element) | Link rune confirmed; era span not attested |
| ud-seal-veil-daimonios | identity CONFIRMED / mechanics CONFIRMED / era CONFIRMED | unknown — element unknown per corpus; Seals vary; no attestation | Improved Technique + Seal + Veil economy confirmed; Daimonios credited |
| ud-snowstorm-frost | identity UNSUPPORTED / mechanics UNSUPPORTED / era UNSUPPORTED | NONE ATTESTED | SNF kit — Snowstorm rune not found in thein.ru or gamezebo; guides reference it by name only |
| ud-spread-rapid-dex | identity CONFIRMED / mechanics CONFIRMED / era CONFIRMED | physical — "Fires several arrows over a wide area to inflict physical damage" (thein.ru) | Clean confirmation; launch-floor baseline |
| ud-summon-strand | identity CONFIRMED / mechanics CONFIRMED / era UNSUPPORTED | fire (Rune Knight) + physical (Abyssling) — see RED FLAG below | corpus elem_raw=physical; Rune Knight is FIRE element per thein.ru |
| ud-toxic-flame | identity CONFIRMED / mechanics CONTRADICTED / era CONFIRMED | poison ONLY — "deals Poison DoT" (thein.ru); fire element NOT attested | CONTRADICTION: corpus claims poison/fire dual-element; source attests poison DoT only |
| ud-whirlwind-str | identity CONFIRMED / mechanics CONFIRMED / era CONFIRMED | physical — "Physical DMG 220%-660%" (thein.ru) | Skill-is-movement confirmed; 30% move dampening noted |


---

## Verdict histogram (ADVISORY — steward recounts from files)

| verdict | count |
|---------|-------|
| CONFIRMED | 23 |
| CONTRADICTED | 4 |
| UNSUPPORTED | 9 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions (4 total)

1. **ud-illusion-family / mechanics:** Corpus claims Illusion skills spawn echo copies at target positions. Source (thein.ru IllusionArrow) shows stack-proc auto-fire from caster position: "Chance to automatically fire a Guided Arrow upon reaching stack count with Bow Skills." No copy-spawn mechanic found.
2. **ud-lightning-vortex / mechanics:** Corpus/probe claims ranged cast at-target large-zone AOE. Source confirms MELEE attack: "This Strength-based melee attack swings the weapon forth to deal Cleave Lightning area DMG, followed by a vortex that inflicts Vortex Lightning DMG" (pocketgamer). Skill geometry is self-origin melee cleave, not remote cast.
3. **ud-toxic-flame / identity:** Corpus labels elem_raw as "poison/fire hybrid." Source (thein.ru ToxicFlame) attests POISON DoT only: "Fires a piercing toxic flame that deals Poison DoT." No fire damage descriptor in skill text. Skill name contains "flame" but this is name-only per Element Law — fire NOT attested.
4. **ud-toxic-flame / mechanics:** Corpus claims "small AOE splash" geometry. Source shows PIERCING PROJECTILE (not AOE): "Fires a piercing toxic flame." Explicitly incompatible with splash geometry.

---

## SNF kits (SOURCE_NOT_FOUND = 0; but functionally silent)

- **ud-snowstorm-frost:** All three claim families UNSUPPORTED. "Snowstorm" rune not found in thein.ru rune library (365 items searched), gamezebo rune list (403), or targeted searches. Guides reference Snowstorm as a name-mention only without mechanical description. Cold-zone mechanics not verified. This kit is fully unattested — all dossier families abstained.

---

## Dossier coverage

- Total dossier families across 12 kits: 72 (6 per kit)
- Non-abstained (payload present): 40
- Abstained (source silent): 32
- Coverage: ~55.6%
- snowstorm-frost accounts for all 6 abstentions on its kit; remaining 26 abstentions = capstone_alterations/author_credit/variants gaps
- Highest-confidence kits: ud-whirlwind-str (0.88 avg), ud-spread-rapid-dex (0.85 avg)
- Lowest-confidence kit: ud-snowstorm-frost (all 0.0 / abstained)

---

## Element-attestation summary (per-kit)

| kit_id | element attested | attestation anchor | law-compliant? |
|--------|-----------------|-------------------|----------------|
| ud-cwc-spin-caster | cold (Blizzard proc layer) | "proc Blizzard to rain down projectiles" | YES — damage-type context |
| ud-cwc-spin-caster | physical (Whirlwind layer) | "Physical DMG 220%-660%" (whirlwind page) | YES |
| ud-flamethrower-channel | fire | "Deal Fire DMG to enemies when maintaining Focus" | YES |
| ud-ice-crystal-arrow | cold | "Shoots a Cold Arrow" + Chill/Freeze ailments | YES |
| ud-illusion-family | physical | "Fires several arrows over a wide area to inflict physical damage" (Illusion Arrow proc) | YES (Illusion Arrow fires physical projectiles) |
| ud-lightning-vortex | lightning | "deal Cleave Lightning area DMG, followed by a vortex that inflicts Vortex Lightning DMG" | YES |
| ud-multishot-link | none | link rune; inherits host | N/A (correct) |
| ud-seal-veil-daimonios | none attested | element unknown per corpus; Seals vary; no damage-type descriptor found | N/A (correct) |
| ud-snowstorm-frost | none (source silent) | rune not found | N/A |
| ud-spread-rapid-dex | physical | "Fires several arrows over a wide area to inflict physical damage on the enemy" | YES |
| ud-summon-strand | fire (Rune Knight) + physical (Abyssling) | "Summons a Rune Knight of Fire that periodically breathes Fire" / "deals Physical DMG" | YES — RED FLAG: corpus elem_raw=physical; Rune Knight is fire |
| ud-toxic-flame | poison ONLY | "Fires a piercing toxic flame that deals Poison DoT" | YES — fire element name-only, REJECTED per Element Law |
| ud-whirlwind-str | physical | "Physical DMG 220%-660%" | YES |

---

## Author credits

| kit_id | handle | context |
|--------|--------|---------|
| ud-cwc-spin-caster | Ya55 | Season 7 Whirlwind Blizzard CwC meta build creator |
| ud-ice-crystal-arrow | Zismoo | Season 7 Ice Crystal Arrow build creator |
| ud-lightning-vortex | Daimonios | Season 7 Lightning Vortex build creator; Seal/Veil economy archetype named for this creator |
| ud-seal-veil-daimonios | Daimonios | Same — the build archetype is attributed to this player |

---

## Red flags

1. **ud-toxic-flame element error:** corpus elem_raw lists "poison" (only) but mech_note says "classless poster child: poison + fire both applied from one skill." Source attests POISON DoT only — no fire damage descriptor in Toxic Flame rune text. The skill NAME contains "flame/toxic" but this is name-only. Elrond: elem_raw should remain poison; mech_note dual-element claim should be flagged as corpus error.

2. **ud-summon-strand element mismatch:** corpus elem_raw=physical. Summon Bursting Rune Knight is FIRE element ("Summons a Rune Knight of Fire that periodically breathes Fire"). Summon Abyssling = physical. The strand is dual-element (fire + physical). corpus record is partially inaccurate.

3. **ud-lightning-vortex delivery contradiction:** corpus/probe marks this as "at-target large-zone" ranged cast. It is a melee weapon swing that creates a secondary vortex. Probe conf was already capped at 0.45 (post-cutoff) but the base geometry claim is wrong for all eras — Lightning Vortex has always been a melee cleave skill per thein.ru and pocketgamer.

4. **ud-snowstorm-frost: fully unattested.** Rune not found in the 365-item thein.ru database. Either renamed in EN version, or only available in Korean, or added post-cutoff under a different name. Kit cannot be verified, dossier cannot be populated.

5. **game8 domain miss:** game8.co returned 404 for Undecember. No game8 content exists for this game. Domain order in brief should be updated; thein.ru + pocketgamer + pockettactics are the reliable EN sources.

---

## Domain performance

| source | outcome |
|--------|---------|
| undecember.thein.ru | PRIMARY — rune DB pages functional; individual rune URLs reliable |
| pocketgamer.com/undecember/builds | PRIMARY — Season 7 build guide; author credits, link rune specs |
| pockettactics.com/undecember/builds | SECONDARY — beginner builds, launch-era confirmation |
| showgamer.com (Undecember guide) | SECONDARY — launch-era confirmation |
| game8.co/games/Undecember | 404 — NOT AVAILABLE |
| undecember.fandom.com | NOT TESTED (canary dividend — not needed given thein.ru success) |
| gamezebo.com Undecember runes | 403 |
| vhpg.com Undecember | PARTIAL — Seal/Veil list only |
