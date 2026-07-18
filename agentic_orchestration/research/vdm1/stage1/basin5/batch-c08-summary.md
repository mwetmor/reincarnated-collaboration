# VDM-1 basin-5 batch-c08 — summary (vs, 12 kits)

**Batch:** c08 | **Game:** Vampire Survivors | **Date:** 2026-07-18
**Primary source:** vampire.survivors.wiki (independent VS wiki — fandom.com returned 402 on all probes)

---

## Per-kit one-liners

| kit_id | identity | mechanics | era | notes |
|---|---|---|---|---|
| vs-big-trouser | CONTRADICTED (not DLC — base game Patch 0.10.0) | CONFIRMED | CONTRADICTED (vs-dlc-era wrong; base game) | greed/Candybox confirmed |
| vs-bloody-tear | CONFIRMED | CONFIRMED | CONFIRMED | heal-on-hit + crit confirmed; patch 0.2.4 (Dec 2021) |
| vs-death-spiral | CONFIRMED | CONFIRMED | CONFIRMED | orbit ring confirmed; patch Oct 2021 |
| vs-fuwalafuwaloo | CONFIRMED | CONFIRMED | CONTRADICTED (vs-dlc-era wrong; both components base game, patch 0.7.2) | union recipe confirmed |
| vs-gatti-amari | CONFIRMED | CONFIRMED | CONFIRMED | negative_canon: UNSUPPORTED — meta discourse does NOT confirm it as off-meta/trap; wiki says "among the most powerful weapons in the game" with Gemini Arcana |
| vs-gorgeous-moon | CONFIRMED | CONFIRMED | CONFIRMED | screen erasure + gem vacuum simultaneous confirmed; patch v0.3.1 |
| vs-heaven-sword | CONFIRMED | CONFIRMED | CONFIRMED | boomerang lane confirmed; patch 0.2.4 |
| vs-hellfire | CONFIRMED | CONFIRMED | CONFIRMED | fire element: UNSUPPORTED (wiki: "flaming meteors" visual only; no explicit fire damage type) |
| vs-holy-wand | CONFIRMED | CONFIRMED | CONFIRMED | holy element: UNSUPPORTED (wiki: "blue magic bolts"; no explicit holy damage type); zero-cooldown framing: CONFIRMED at 0.5s |
| vs-infinite-corridor-crimson-shroud | CONFIRMED | CONFIRMED | CONFIRMED | TRUE BEAM confirmed; HP-halving + damage cap Reaper-kill confirmed; patch 0.6.1 |
| vs-je-ne-viv | CONFIRMED | CONFIRMED | CONFIRMED | DLC (Tides of Foscari, April 2023); Magnet+Greed scaling confirmed |
| vs-la-borra | CONFIRMED | CONFIRMED | CONFIRMED | mobile puddle trail confirmed; "holy water" name — element UNSUPPORTED |

---

## Verdict histogram (advisory — steward recounts from files)

| verdict | count |
|---|---|
| CONFIRMED | 28 |
| CONTRADICTED | 4 |
| UNSUPPORTED | 1 (negative_canon gatti-amari) |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions

1. **vs-big-trouser identity**: corpus claims "DLC character" — CONTRADICTED. Fetched text: "Added in Patch 0.10.0 (4 August 2022). He is part of the base game, not DLC."
2. **vs-big-trouser era**: corpus stamps `vs-dlc-era` — CONTRADICTED. Big Trouser is base game secret character, no DLC gate.
3. **vs-fuwalafuwaloo era**: corpus stamps `vs-dlc-era` as first era — CONTRADICTED. Fuwalafuwaloo added patch 0.7.2 (June 9, 2022); both component weapons (Vento Sacro, Bloody Tear) are base game. No DLC required.
4. **vs-gatti-amari negative_canon**: UNSUPPORTED — no fetched discourse confirms this weapon as off-meta, trap, or avoided. Wiki states it is "among the most powerful weapons in the game, outclassing most evolved weapons as well as its own evolution" (with Gemini Arcana). Anti-harvest-economy framing in corpus is mechanically accurate (cats eat pickups) but the meta-assessment of that as "non-canon / negative" is NOT corroborated by community sources.

---

## SOURCE_NOT_FOUND kits

None. vampire.survivors.wiki returned live pages for all 12 kits.

---

## Dossier coverage

All 12 kits dossier-complete. skill_loop and skill_geometry populated for all. item_alterations populated for all. capstone_alterations populated where wiki attested union/DLC evolution paths (death-spiral, hellfire, la-borra, gatti-amari, infinite-corridor-crimson-shroud). author_credit abstained all (community wiki, no named authors). variants populated where union paths exist.

Dossier coverage: **12/12 kits (100%)**

---

## Element-attestation summary (per-kit)

Element law: record only when fetched text applies element word as damage-type descriptor or enemy-directed behavior verb — NOT name-only.

| kit_id | element claimed | verdict | anchor / reason |
|---|---|---|---|
| vs-hellfire | fire | UNSUPPORTED | Wiki says "large flaming meteors" (visual) + "Evolved Fire Wand" (name lineage). No explicit "fire damage" statement. Category "Fire weapons" = wiki organizational tag, not in-game damage type. |
| vs-holy-wand | holy | UNSUPPORTED | Wiki says "blue magic bolts." No "holy damage" text anywhere. Name lineage only. |
| vs-la-borra | holy | UNSUPPORTED | Wiki says "bottles of holy water" (item name/description). No explicit holy damage type stated. |
| vs-bloody-tear | — | element-silent | Physical slash; no element. |
| vs-death-spiral | — | element-silent | Physical; no element. |
| vs-fuwalafuwaloo | — | element-silent | Physical slash/crit; no element. |
| vs-gatti-amari | — | element-silent | Claw/physical; no element. |
| vs-gorgeous-moon | — | element-silent | Erasure mechanic; no element. |
| vs-heaven-sword | — | element-silent | Physical boomerang; no element. |
| vs-infinite-corridor-crimson-shroud | — | element-silent | Freeze/beam delivery — "freeze" is status effect, not a damage element in VS. No fire/lightning/holy/ice damage type stated. |
| vs-je-ne-viv | — | element-silent | Aura/explosion; no element type stated. |
| vs-big-trouser | — | element-silent | Economy character; no combat element. |

**Summary:** 0 element attestations across all 12 kits. All three name-triggered candidates (Hellfire, Holy Wand, La Borra) are UNSUPPORTED under element law.

---

## Rotation-shaped UNSUPPORTED kits (roguelite marker)

**All 12 kits.** Vampire Survivors has no skill rotation. Every kit is a weapon-evolution (passive auto-trigger) or character-economy archetype. "Build rotation / skill loop" framing does not apply. Dossier skill_loop family was populated with evolution recipe + delivery mechanics rather than rotation steps — this is the correct roguelite encoding. Downstream mapping is expected to GAP all or nearly all of these on the rotation/skill-loop axis.

---

## Red flags

1. **FANDOM-402 SCALE-BLOCKING:** `vampire-survivors.fandom.com` returned HTTP 402 on all probes. This is the VS canonical source per brief. Recovery: `vampire.survivors.wiki` (independent VS wiki at vampire.survivors.wiki/w/) was live and authoritative — all 12 kits resolved. Scale risk for c09 vs-b batch: same domain order applies; fandom.com will 402 again. c09 should route directly to vampire.survivors.wiki without attempting fandom first.
2. **Era stamp errors (2 kits):** vs-big-trouser and vs-fuwalafuwaloo carry `vs-dlc-era` stamps that are CONTRADICTED by fetched text. Both are base game content. Elrond errata queue.
3. **Negative-canon UNSUPPORTED (gatti-amari):** The corpus marks gatti-amari negative=1 presumably on anti-harvest-economy grounds. Meta discourse does not support "off-meta/trap" — wiki explicitly rates it as top-tier with correct setup (Gemini Arcana). Negative flag rationale is not falsifiable from public sources; steward should decide whether the corpus flag survives.

---

## Author credits

None. All sources are community wiki pages (vampire.survivors.wiki) with no named authors.
