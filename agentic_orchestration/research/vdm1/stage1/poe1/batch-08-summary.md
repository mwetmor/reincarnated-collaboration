# VDM-1 Stage-1 PoE1 Batch-08 Summary
**Kits:** poe1-venom-gyre through poe1-wormblaster (lines 85–94; FINAL batch)
**Date:** 2026-07-18
**Verdict count:** 45 verify rows · 63 dossier rows · 35 citations

---

## Per-kit one-liners

| kit_id | result |
|---|---|
| poe1-venom-gyre | identity/mechanics CONFIRMED; era 3.7-3.13 CONTRADICTED (introduced 3.8, floor 3.7 bucket contradiction); era 3.20+ CONFIRMED |
| poe1-viper-poison | identity/mechanics CONFIRMED; era 3.0-3.6 CONTRADICTED (Pestilent Strike not introduced until 3.8); era 3.7-3.13 CONFIRMED |
| poe1-wander | identity/mechanics/all 3 eras CONFIRMED; strong evidence from 1.3 onward |
| poe1-warchief | identity/mechanics/all 2 eras CONFIRMED; guggelhupf forum thread June 2016 is anchor |
| poe1-ward-loop | identity/mechanics CONFIRMED; era 3.14-3.19 CONTRADICTED (Ward introduced 3.15, floor 3.14 bucket contradiction); era 3.20+ CONFIRMED |
| poe1-whispering-ice | identity/mechanics/all 4 eras CONFIRMED; poedb confirms 2.0.0 introduction |
| poe1-wild-strike | identity/mechanics CONFIRMED; era 3.0-3.6 and 3.7-3.13 UNSUPPORTED (no guide evidence of meta adoption; niche Trinity build is not mass meta); negative_canon CONFIRMED |
| poe1-winter-orb | identity/mechanics CONFIRMED; era 3.0-3.6 CONTRADICTED (introduced 3.5, floor 3.0 bucket contradiction; 5-patch gap) |
| poe1-woc-ignite | identity/mechanics CONFIRMED; era 3.7-3.13 UNSUPPORTED (WoC introduced 3.6 but ignite Elementalist guide evidence begins 3.14+); era 3.14-3.19 CONFIRMED |
| poe1-wormblaster | identity CONFIRMED; mechanics partially UNSUPPORTED (CoC+Barrage+Pathfinder claim — forum source confirms CoC mechanic but class/skill specifics not attestable from fetched text); both eras CONFIRMED |

---

## Verdict histogram

| Verdict | Count |
|---|---|
| CONFIRMED | 31 |
| CONTRADICTED | 4 |
| UNSUPPORTED | 10 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions (4 — all era floor bucket-floor issues)

1. **poe1-venom-gyre era 3.7-3.13**: Venom Gyre introduced patch 3.8.0; era bucket floor 3.7 predates skill introduction by one patch. Earliest forum guides dated September 2019 (patch 3.8). Correct lower bound = 3.8.
2. **poe1-viper-poison era 3.0-3.6**: Pestilent Strike (core dual-skill kit) introduced patch 3.8.0. The era stamp covers a period where one of the two core skills did not exist. Viper Strike alone existed in 3.0-3.6, but the kit as stamped (Viper/Pestilent) cannot exist before 3.8.
3. **poe1-ward-loop era 3.14-3.19**: Ward as a mechanic was introduced in patch 3.15 (Expedition). Era bucket floor 3.14 predates Ward's existence. Correct lower bound = 3.15.
4. **poe1-winter-orb era 3.0-3.6**: Winter Orb introduced patch 3.5.0 (Betrayal). Era floor 3.0 is a five-patch bucket-floor contradiction. 9% representation confirmed in Betrayal (3.5); 3.0-3.4 is impossible.

---

## SOURCE_NOT_FOUND kits

None. All kits returned usable source material.

---

## Dossier coverage

- 10 kits × 6 families = 60 possible dossier rows
- Abstained rows: 3 (author_credit for poe1-wander, poe1-whispering-ice, poe1-ward-loop — no named individual authors identified in fetched guides)
- Non-abstained rows: 57 / 60 = **95% dossier coverage**
- All abstained rows have null payload (DB CHECK compliant)

---

## Author credits captured

| kit_id | handle | site |
|---|---|---|
| poe1-venom-gyre | ezyanfarihin#5882 | pathofexile.com/forum |
| poe1-viper-poison | tylam6746 | pathofexile.com/forum |
| poe1-warchief | guggelhupf#2310 | pathofexile.com/forum |
| poe1-wild-strike | mamburu#3286 | pathofexile.com/forum |
| poe1-winter-orb | Angry_Roleplayer#6657 | pathofexile.com/forum |
| poe1-woc-ignite | TbXie | poe-vault.com |
| poe1-wormblaster | eirikeiken (c9q9md) | youtube.com |

---

## Red flags / abstention reasons

- **poe1-wormblaster mechanics**: CoC+Barrage+Pathfinder claim is UNSUPPORTED. The fetched sources confirm Writhing Jar + CoC as the mechanic core and eirikeiken as originator, but the specific class (Pathfinder) and core attack skill (Barrage) for the original formulation are not confirmed in fetched text — the 3.3 forum variant uses Slayer + Flameblast, the 3.22 variant uses Herald of Ice. The original Pathfinder CoC Barrage formulation is documented by reputation but the forum thread itself was not recoverable (pobarchives 403; poewiki.net Anubis-blocked).
- **poe1-wild-strike era 3.0-3.6 and 3.7-3.13**: Both UNSUPPORTED. The 2015 forum "Wild Strike is weak" thread confirms community-level awareness and play in 2.x, but no guide evidence of Wild Strike being a mainstream meta build in 3.0-3.13. The [3.13] Trinity Inquisitor is a niche theorycrafted build, not mass meta. Era stamps may be reflecting the skill's continued presence in the game rather than actual community adoption as a build archetype.
- **poe1-woc-ignite era 3.7-3.13**: UNSUPPORTED. Wave of Conviction was introduced in 3.6 (Synthesis), but the Shaper of Flames Elementalist ignite archetype's earliest confirmed guide evidence in fetched text is 3.20+. The WoC ignite build may have existed in 3.7-3.13 but no sources confirmed this specific pairing as documented meta during that window.
- **Reddit blocked** throughout batch-08; all identity/era verification rerouted through official forum + poe-vault + odealo + poedb.
- **poewiki.net Anubis-403 blocked** (confirmed again). All wiki needs routed through poedb.tw successfully.

---

## Batch-08 era contradiction summary for Elrond

Four bucket-floor era contradictions:
- venom-gyre: 3.7 → actual debut 3.8
- viper-poison: 3.0-3.6 → Pestilent Strike debut 3.8; Viper Strike alone era is 3.0-3.6 but dual-skill kit requires 3.8+
- ward-loop: 3.14 → Ward mechanic debut 3.15
- winter-orb: 3.0-3.6 → actual debut 3.5; 5-patch gap

Pattern: all four are wide bucket floor contamination (both buckets 3.7-3.13 and 3.0-3.6 affected). Consistent with addendum warning. Recommend elrond flag these for era field correction in canon_corpus.
