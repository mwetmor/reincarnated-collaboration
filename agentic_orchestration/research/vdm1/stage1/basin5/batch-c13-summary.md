# Batch c13 — mcd (Minecraft Dungeons) — Summary
**Date:** 2026-07-18  
**Mode:** B HARVEST (zero probe facts; all findings built from fetched sources)  
**Kits:** mcd-dynamo-torment · mcd-fireworks · mcd-soul · mcd-speed · mcd-summoner

---

## Per-kit one-liners

| kit_id | verdict summary | notes |
|---|---|---|
| mcd-dynamo-torment | CONFIRMED ×3 | identity, mechanics, era all confirmed; Standstill/Rolling variants community-attested via minecraft.wiki + fextralife |
| mcd-fireworks | CONFIRMED ×3 | identity, mechanics, era all confirmed; Scatter Crossbow × 3 fireworks arrows confirmed; Winter's Touch variant unconfirmed (conf 0.62) |
| mcd-soul | CONFIRMED ×3 | identity, mechanics, era all confirmed; soul-economy loop fully documented; multiple build variant names across community sources |
| mcd-speed | CONFIRMED ×3 | identity, mechanics, era all confirmed; both folk names (Speedy Steve / Speedy Assassin) confirmed from separate sources |
| mcd-summoner | CONFIRMED ×3 | identity, mechanics, era all confirmed; 3-companion loadout + Hunter's Promise targeting confirmed; "Beast Lover" / "Hunter Companion" naming variants documented |

---

## Verdict histogram (ADVISORY — steward recounts from files)

| Verdict | Count |
|---|---|
| CONFIRMED | 15 |
| CONTRADICTED | 0 |
| UNSUPPORTED | 0 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions

**ZERO contradictions across this batch.** All 15 verify rows returned CONFIRMED. No fetched source text contradicted any corpus claim.

---

## SNF kits

None. All 5 kits fully sourced.

**Domain note:** Both minecraftdungeons.fandom.com AND minecraft.fandom.com returned 402 on direct fetch. Fell back to minecraft.wiki (the official Minecraft Wiki successor domain — same editorial team, migrated canonical source) and supplemented with game8.co, gamepur.com, gamingscan.com, thegamer.com, and windowscentral.com. No archive.org retry needed. Clean fallback per HOT-FACT protocol.

---

## Dossier coverage

| kit_id | skill_loop | skill_geometry | item_alterations | capstone_alterations | author_credit | variants | coverage |
|---|---|---|---|---|---|---|---|
| mcd-dynamo-torment | filled | filled | filled | abstained | abstained | filled | 4/6 (67%) |
| mcd-fireworks | filled | filled | filled | abstained | abstained | filled | 4/6 (67%) |
| mcd-soul | filled | filled | filled | abstained | abstained | filled | 4/6 (67%) |
| mcd-speed | filled | filled | filled | abstained | abstained | filled | 4/6 (67%) |
| mcd-summoner | filled | filled | filled | abstained | abstained | filled | 4/6 (67%) |

**Batch dossier coverage: 67% (20/30 rows filled, 10 abstained)**

**Abstention reasons (all 5 kits × 2 families = 10 rows):**
- `capstone_alterations` (all 5): Minecraft Dungeons has NO mastery trees, class skill caps, or keystone passives — the gear+enchant loadout IS the build. There is no structural analog to "capstone alteration" in this game. Family is structurally inapplicable for all MCD kits; not source silence.
- `author_credit` (all 5): Fetched sources are wiki/communal (minecraft.wiki — no named author) or major outlet guides (windowscentral, gamepur, gamingscan, thegamer — no individual byline in fetched page body). Consistent handle extraction not possible from page content; abstained rather than fabricate.

---

## Element-attestation summary

**Element law outcome for all 5 mcd kits: ELEMENT-SILENT**

- `mcd-dynamo-torment`: Dynamo enchantment = damage multiplication on roll; no element-type descriptor in fetched text. Physical/neutral — element-silent.
- `mcd-fireworks`: Fireworks Arrow = "explodes on hit" / "explosive power of TNT" — explosion framing, NOT fire-damage framing. Wiki says "ranged damage" without fire-type qualifier. Game8.co: "area-of-effect explosion" — explosion noun, not fire damage verb applied to enemies. Element law governs: "explosive" ≠ fire attestation. Element-silent.
- `mcd-soul`: Corrupted Beacon = "shadow beam" language in wiki (not "soul damage" or "fire damage"). Soul resource page explicitly: "The documentation contains no references to 'soul damage' or similar damage-type terminology." Soul is a RESOURCE, not an element/damage type in MCD. Engine has no soul family. Element-silent.
- `mcd-speed`: Pure movement build; no elemental damage in any fetched text. Element-silent.
- `mcd-summoner`: Companion damage is physical attack (golem fists, wolf bite, llama ranged projectile) — no elemental descriptor in any fetched text. Element-silent.

**Result: 0 elements attested across batch c13. No engine element-family assignments warranted from this batch.**

---

## Rotation-shaped UNSUPPORTED note

All 5 mcd kits are **loadout/cooldown-shaped, NOT rotation-shaped**. Minecraft Dungeons has no skill rotation (no class, no skill tree, no skill activation sequence in the ARPG sense). The "loop" for each kit is: activate artifact(s) on cooldown + auto-attack. Dossier `skill_loop` fields are filled with the honest loadout/cooldown-management pattern; no fake ARPG rotation was imposed. Downstream mapper should note: mcd kits map to gear-assembly + cooldown-cycle archetypes; skill-rotation columns in the engine mapping layer will be UNSUPPORTED by design.

---

## Red flags

1. **Fandom 402 (both domains):** minecraft.fandom.com and minecraftdungeons.fandom.com both returned 402 on direct fetch. minecraft.wiki is the canonical migrated successor and served all necessary content cleanly. This is not a data-quality issue — it is a domain-access issue fully resolved by fallback. No further grind needed.

2. **Enigma Resonator in corpus mech_note:** Corpus lists Enigma Resonator as a core soul-build enchant alongside Soul Siphon. Both confirmed from minecraft.wiki. No contradiction; both documented in dossier item_alterations.

3. **Refreshment enchantment (mcd-dynamo-torment and mcd-fireworks):** Corpus mech_notes list Refreshment (heals player on artifact use, indirectly extends kill-loop sustainability) as a support enchant. Fetched wiki pages confirm Refreshment exists but none explicitly documented its interaction with Dynamo or Fireworks as the canonical loop enabler — noted in dossier as corpus-listed/wiki-corroborated-existence but conf held at 0.80 rather than 0.90.

4. **Winter's Touch crossbow (mcd-fireworks):** Corpus mech_note lists Winter's Touch as an alternative Fireworks Arrow vehicle. No fetched source explicitly confirmed this pairing (Scatter Crossbow is the dominant confirmed pairing). Documented in variants with conf 0.62; mapper should treat Winter's Touch pairing as plausible-corpus-asserted, not fetched-confirmed.
