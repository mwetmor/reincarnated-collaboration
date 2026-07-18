# VDM-1 Stage-1 PoE1 Batch-04 Summary
**Spec lines 37-48 | Kits: poe1-flicker through poe1-ice-shot (12 kits)**
**Date: 2026-07-18**

## Per-kit one-liners

| kit_id | folk_name | verdict summary |
|---|---|---|
| poe1-flicker | Flicker Strike | All 3 positive families CONFIRMED. Terminus Est alias attested. Frenzy charge cooldown bypass confirmed from poedb. Era 1.x-3.20+ confirmed via forum guides. |
| poe1-forbidden-rite | Forbidden Rite | All 3 positive families CONFIRMED. FR totems alias attested. 3.15 launch confirmed. Life-cost-to-totems mechanic confirmed verbatim. |
| poe1-freezing-pulse | Freezing Pulse | Identity + mechanics CONFIRMED. Era UNSUPPORTED — forum/sources do not explicitly attest 1.x and 2.x build presence (3.15 guide says earlier era was "meme-build" but not data-confirmed). |
| poe1-frost-blades | Frost Blades | All 3 positive families CONFIRMED. Introduced 2.0.0 per poedb. Raider 3.11 + Trickster 3.7 attested. Fan-of-projectiles mechanic confirmed verbatim. |
| poe1-generals-cry | General's Cry | Identity + mechanics CONFIRMED. Era CONTRADICTED — era bucket floor 3.7 stamped but skill introduced 3.11; bucket 3.7-3.13 overstates era presence by ~4 patches. |
| poe1-glacial-cascade-mines | Glacial Cascade Mines | All 3 positive families CONFIRMED. Cascade march geometry confirmed (4 bursts, final burst 200% dmg). Mine interaction confirmed. |
| poe1-glacial-hammer | Glacial Hammer (negative=1) | Identity + mechanics + era CONFIRMED. Negative_canon CONFIRMED — "Melee strike skill in modern POE" listed as explicit con in 3.22 guide; author switched to it only as fallback after nerf. |
| poe1-golementalist | Golementalist | All 3 positive families CONFIRMED. Golementalist folk name attested verbatim in forum guide title. Primordial jewel mechanics confirmed. Era 2.x-3.13 confirmed. |
| poe1-heavy-strike-stun | Heavy Strike Stun Berserker | Identity + mechanics + era CONFIRMED. Note: DB spec says Berserker but primary attested class in 3.20+ sources is Champion (mantol456 guide). Berserker class not ruled out but not attested in 3.20+ sources reviewed. |
| poe1-hexblast-mines | Hexblast Mines | Identity + mechanics CONFIRMED. Era CONTRADICTED — DB era floor 3.7-3.13 but Hexblast introduced in 3.12 per official GGG patch notes; era floor 3.7 predates skill by 5 patches. |
| poe1-hoag | Herald of Agony | All 3 positive families CONFIRMED. HoAG alias + crawler folk name attested. Virulence mechanic + Cyclone feeder confirmed. 3.4 introduction confirmed from official patch notes. |
| poe1-ice-shot | Ice Shot | All 3 positive families CONFIRMED. Cone-behind-target geometry confirmed verbatim from poedb. Deadeye class confirmed. Era 3.7+ attested. |

---

## Verdict histogram

| Family | CONFIRMED | CONTRADICTED | UNSUPPORTED | SOURCE_NOT_FOUND |
|---|---|---|---|---|
| identity | 12 | 0 | 0 | 0 |
| mechanics | 12 | 0 | 0 | 0 |
| era | 9 | 2 | 1 | 0 |
| negative_canon | 1 | 0 | 0 | 0 |
| **TOTAL** | **34** | **2** | **1** | **0** |

---

## Contradictions (2)

1. **poe1-generals-cry / era** — DB era bucket `3.7-3.13` has floor at 3.7, but General's Cry was introduced in patch 3.11.0 (confirmed from poedb.tw). The era bucket overstates presence by ~4 patches. Same class of issue caught in batch-02 for era-floor-predates-intro. Earliest valid era stamp within this bucket should be 3.11.
   - Source: https://poedb.tw/us/Generals_Cry — "General's Cry was added in patch 3.11.0"

2. **poe1-hexblast-mines / era** — DB era bucket `3.7-3.13` has floor at 3.7, but Hexblast was introduced in patch 3.12.0 Heist (confirmed from official GGG patch notes). Era bucket floor 3.7 predates skill introduction by 5 patches. Earliest valid era stamp should be 3.12 or era-bucket `3.14-3.19` + `3.20+`.
   - Source: https://www.pathofexile.com/forum/view-thread/2935777 — "Added a new Intelligence Skill Gem - Hex Blast..."

---

## UNSUPPORTED (1)

- **poe1-freezing-pulse / era** — Era stamps `1.x` and `2.x` claimed for Freezing Pulse. Skill introduced 0.8.7 (pre-1.0), so 1.x is plausible by introduction date. However no 1.x or 2.x era build guide was located confirming the skill was meta or actively played in those eras. One 3.15 source notes it "was a meme-build in earlier eras" which weakly supports presence but does not constitute attested meta-presence. Marked UNSUPPORTED (honest). Era `3.0-3.6` is also unattested in sources reviewed — earliest attested forum guides are 3.14+.

---

## SOURCE_NOT_FOUND kits

None. All 12 kits sourced.

---

## Dossier coverage

12 kits × 6 families = 72 dossier rows.
- Abstained (source silent): 12 rows (`capstone_alterations` for all 12 kits — no capstone alteration data found for any kit in this batch).
- Non-abstained: 60 rows.
- Coverage: 60/72 = **83%**

Capstone_alterations family is uniformly unattested across all 12 kits in this batch. This appears to be a systematic gap in accessible sources rather than a kit-specific failure.

---

## Author credits extracted

| handle | site | kits |
|---|---|---|
| Spacefight0r#5392 | pathofexile.com/forum | poe1-flicker |
| ACGIFT#1167 | pathofexile.com/forum | poe1-flicker |
| ShamefulPenguin#7799 | pathofexile.com/forum | poe1-forbidden-rite |
| GhazzyTV | poe-vault.com | poe1-forbidden-rite |
| Fyregrass#7297 | pathofexile.com/forum | poe1-freezing-pulse |
| bashtart#2403 | pathofexile.com/forum | poe1-frost-blades |
| Timmytimmy123#6879 | pathofexile.com/forum | poe1-frost-blades |
| FuzzyDuckzy | maxroll.gg | poe1-frost-blades |
| wishdropper#0634 | pathofexile.com/forum | poe1-generals-cry |
| aer0 | maxroll.gg | poe1-glacial-cascade-mines, poe1-ice-shot |
| mantol456#0648 | pathofexile.com/forum | poe1-glacial-hammer, poe1-heavy-strike-stun |
| Angry_Roleplayer#6657 | pathofexile.com/forum | poe1-golementalist |
| TbXie | poe-vault.com | poe1-hexblast-mines, poe1-hoag |
| Palsteron | maxroll.gg | poe1-hexblast-mines |
| PoEVault | poe-vault.com | poe1-ice-shot |

---

## Red flags

1. **Era-floor contradictions (systematic pattern)**: Batch-04 caught 2 era-floor-predates-intro contradictions (General's Cry, Hexblast), confirming this is a recurring DB quality issue. Recommend Elrond/gandalf review era floors on all kits that use the `3.7-3.13` bucket — this is the bucket most likely to contain skills introduced mid-bucket (3.11 and 3.12 introductions both caught here).

2. **Berserker vs Champion for Heavy Strike Stun**: DB spec lists Berserker as class for poe1-heavy-strike-stun but the primary attested 3.20+ build guide (mantol456 3.23 guide) uses Champion. The Berserker class is plausible (warcry synergy, rage mechanics) but not attested in sources found. Worth noting for Elrond's curation pass.

3. **Capstone_alterations uniformly absent**: No sources in this batch surface capstone-level gem alteration language. This may require deeper wiki/changelog fetches to resolve.

4. **0 contradictions on identity and mechanics families** across all 12 kits. Corpus data quality for these two families is high.
