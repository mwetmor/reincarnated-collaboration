# VDM-1 Basin-1 Batch-02 Summary
## Kits 13-24 (poe2-grim-feast through poe2-smith-ignite)
## Date: 2026-07-18

---

## Per-kit one-liners

| kit_id | folk_name | verdict_summary | notes |
|---|---|---|---|
| poe2-grim-feast | Grim Feast Overleech | identity CONFIRMED; mechanics CONFIRMED; era 0.2 CONFIRMED; era 0.3+0.4 CONTRADICTED | ES overleech mechanic completely reworked to minion-revival in 0.3.0 |
| poe2-howa-invoker | HoWA Invoker | all families CONFIRMED | HoWA unique gloves introduced 0.1.0; 0.2 nerfed per-INT scaling |
| poe2-ice-strike-invoker | Ice Strike Invoker | all families CONFIRMED | Guide active 0.1.1 → current 0.5.1; author: Milkybk_ |
| poe2-infernal-legion | Infernal Legion Minions | identity CONFIRMED; mechanics CONFIRMED; all era stamps CONFIRMED | Ascendancy shifted Infernalist→Lich from 0.3+; class discrepancy flagged below |
| poe2-lightning-arrow-deadeye | Lightning Arrow Deadeye | all families CONFIRMED; all 5 era stamps CONFIRMED | Persistent build 0.1 through 0.5.4; author: Crouching_Tuna |
| poe2-lightning-spear-amazon | Lightning Spear Amazon | identity CONFIRMED; mechanics CONFIRMED; era 0.2+0.3 CONFIRMED | Class "Amazon" = ascendancy name; base class is Huntress (0.2 introduction) |
| poe2-minion-infernalist | Minion Infernalist | identity CONFIRMED; Skeletal Arsonist+SRS CONFIRMED; "Loyal Hellhound" UNSUPPORTED | Skill is "Summon Infernal Hound" not "Loyal Hellhound"; author: Helm Breaker |
| poe2-perfect-strike-01 (negative=1) | Perfect Strike (launch) | identity CONFIRMED; mechanics CONFIRMED; era 0.1 UNSUPPORTED; negative_canon CONFIRMED | No 0.1 doc in poe2db/fextralife; 0.2.0 nerfs ("no longer always Ignites; 45%→35% speed") confirm pre-nerf degenerate state |
| poe2-poison-pathfinder | Poison Pathfinder | all families CONFIRMED; all 4 era stamps CONFIRMED | 0.1.1 guide attested; 0.4 fubgun recommendation; author: Crouching_Tuna |
| poe2-rake-ritualist | Bleed Ritualist | all families CONFIRMED; era 0.2+0.3 CONFIRMED | Huntress/Ritualist introduced 0.2 — era floor correct |
| poe2-shaman-bear | Shaman Bear | all families CONFIRMED; era 0.4+0.5 CONFIRMED | "Rampage" confirmed as optional alt; "Walking Calamity" is primary clear skill; author: Palsteron |
| poe2-smith-ignite | Smith of Kitava Ignite | all families CONFIRMED; era 0.2-0.5 CONFIRMED | Ascendancy introduced 0.2 (briefly bugged at launch, fixed hotfix 4); Supercharged Slam 0.4 confirmed |

---

## Verdict histogram (advisory — steward recounts from files)

- CONFIRMED: 55
- CONTRADICTED: 3
- UNSUPPORTED: 2
- SOURCE_NOT_FOUND: 0

---

## Contradictions (one line each)

1. **poe2-grim-feast / era 0.3-edict**: ES overleech Grim Feast build stamped as active in 0.3; poe2db confirms "Grim Feast has been completely reworked and re-enabled" in 0.3.0, replacing ES mechanic with minion-revival. Stamped era postdates the mechanic's existence.
2. **poe2-grim-feast / era 0.4**: Same rework — ES overleech Grim Feast did not exist in 0.4. Same source.

---

## SNF kits

None. All 12 kits found in live sources. Zero SOURCE_NOT_FOUND verdicts.

---

## UNSUPPORTED verdicts

- **poe2-minion-infernalist / mechanics "Loyal Hellhound"**: No source uses the alias "Loyal Hellhound." Actual skill name across all guides is "Summon Infernal Hound" or "Infernal Hound." The alias may be folk shorthand not present in guide text; honest UNSUPPORTED.
- **poe2-perfect-strike-01 / era 0.1**: No source directly attests Perfect Strike existed in PoE2 0.1 EA launch. Earliest documented poe2db entry is 0.2.0. Skill likely existed in 0.1 (0.2.0 patch notes say "no longer always Ignites" implying prior state), but direct attestation for 0.1 presence was not found. UNSUPPORTED per no-fabrication law; indirect inference is insufficient for CONFIRMED.

---

## Dossier coverage

12 kits × 6 families = 72 rows.
- Non-abstained: 52 rows
- Abstained: 20 rows
- Coverage: 72% (52/72)

Primary abstentions: `item_alterations` (8 kits — no key unique items referenced in sources beyond HoWA, Fury of the King, and Grim Feast itself), `author_credit` (5 kits without bylined guides found), `capstone_alterations` for poe2-grim-feast (no ascendancy-specific notable found — Grim Feast is a cross-build defensive layer, not ascendancy-gated).

---

## Author credits (bylined guides found)

| kit_id | handle | site |
|---|---|---|
| poe2-ice-strike-invoker | Milkybk_ | maxroll.gg |
| poe2-infernal-legion | Shayd | maxroll.gg |
| poe2-lightning-arrow-deadeye | Crouching_Tuna | maxroll.gg |
| poe2-lightning-spear-amazon | Crouching_Tuna | maxroll.gg |
| poe2-minion-infernalist | Helm Breaker | maxroll.gg |
| poe2-poison-pathfinder | Crouching_Tuna | maxroll.gg |
| poe2-shaman-bear | Palsteron | maxroll.gg |

---

## Red flags and cross-seam notes

1. **Grim Feast ES overleech era boundary** (high confidence contradiction): The corpus records this kit with era `0.2-dawn;0.3-edict;0.4`. The ES overleech version of Grim Feast was the mechanic the kit describes. poe2db is explicit: the skill was "completely reworked and re-enabled" in 0.3.0 to a minion-revival mechanic. The 0.3-edict and 0.4 era stamps are factually incorrect for the ES overleech build identity. Elrond should note this as a record that needs era trim to `0.2-dawn` only, or the kit should be split into two records (ES Grim Feast 0.1-0.2 / Grim Resurrection minion form 0.3+).

2. **Infernal Legion ascendancy lineage shift**: The corpus records class as "Infernalist/Witch." The Infernalist was the dominant form in 0.1/0.2 (attested by Kripp's guide Dec 2024/Jan 2025). From 0.3+ the Lich ascendancy became the dominant host (current maxroll guide = Lich). The `era 0.2-dawn` CONFIRMED for Infernalist; later eras confirm the build archetype persists but under a different ascendancy. The record is not wrong but the class field understates lineage complexity — Elrond may want `lineage` column annotation.

3. **Lightning Spear Amazon — class vs ascendancy naming**: Folk name "Lightning Spear Amazon" is genuine community usage confirmed. However "Amazon" is the ascendancy name, not the base class; the base class is "Huntress." This is consistent terminology in the PoE2 community (ascendancy names are used as shorthand). Record is accurate; no action needed but worth noting for abstraction taxonomy.

4. **Perfect Strike 0.1 documentation gap**: poe2db has no 0.1 version entry for Perfect Strike. This is consistent with the general sparseness of 0.1 patch documentation across poe2db. The 0.2.0 nerf language ("no longer always Ignites"; "previously 45%" attack speed) strongly implies the skill existed in 0.1 in a more powerful form, consistent with the negative_canon_target description. The era `0.1` stamp is UNSUPPORTED rather than CONTRADICTED — the absence of documentation is not proof of absence. The negative canon (degenerate in 0.1, reworked by 0.2) is CONFIRMED by the 0.2.0 change text.

5. **Shaman Bear — "Rampage" as primary skill is imprecise**: Corpus records `core_skills: ["Bear Form", "Rampage"]`. The maxroll guide explicitly states Rampage is optional ("a lot of people use Rampage and like it") and the primary clear skill is Walking Calamity. Bear Form + Walking Calamity + Maul/Furious Slam is the actual skill loop. Rampage is a common variant but not the sole or primary skill. Mechanics verified CONFIRMED because Rampage is confirmed as a used skill in the archetype; the imprecision is worth flagging for Elrond's schema pass.
