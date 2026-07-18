# VDM-1 basin-3 batch-04 summary — kits 37-48 (d2-meteorb through d2-teleport-sorc)

**Crawl date:** 2026-07-18
**Kits:** d2-meteorb, d2-mosaic-sin, d2-nova-sorc, d2-poison-javazon, d2-poison-nova-necro, d2-rabies-wolf, d2-sacrifice, d2-singer, d2-smiter, d2-summon-druid, d2-summonmancer, d2-teleport-sorc

---

## Advisory verdict histogram (steward recounts from files; this is ADVISORY)

| verdict | count (advisory) |
|---|---|
| CONFIRMED | ~37 |
| UNSUPPORTED | ~13 |
| CONTRADICTED | 0 |
| SOURCE_NOT_FOUND | 0 |

**0 contradictions across the batch.** Pre-cutoff-stable d2 slice (mostly lod/d2r tokens) — low-contradiction is expected for this game segment. Steward to judge.

---

## Per-kit one-liners

- **d2-meteorb:** identity+mechanics+lod+d2r CONFIRMED; rotw-s14 UNSUPPORTED (post-cutoff, no fetched text). Good dossier. PureDiablo direct fetches 403 — all content recovered from search snippets or non-purediablo fetches.
- **d2-mosaic-sin:** identity+mechanics+d2r-2.6+ CONFIRMED via diablo2.io Mosaic runeword page; rotw-s13+ UNSUPPORTED (post-cutoff). Strong capstone_alterations row (charge-persistence mechanic verbatim). Author credit: Teebling (diablo2.io admin).
- **d2-nova-sorc:** identity+mechanics+lod+d2r CONFIRMED via diablo2.io; rotw-s14 UNSUPPORTED. ES variant documented as sub-variant. Author credits: saggytits, APKefka (diablo2.io).
- **d2-poison-javazon:** identity+mechanics+lod CONFIRMED via PureDiablo search snippets and theamazonbasin search results; no d2r era claim in spec. Skill loop fully documented from PureDiablo v1.10 guide snippet.
- **d2-poison-nova-necro:** identity+mechanics+lod-1.10++d2r CONFIRMED. item_alterations row captured (Bramble vs Enigma debate). Author credit: Schnorki (diablo2.io moderator).
- **d2-rabies-wolf:** identity+mechanics+lod+d2r CONFIRMED. item_alterations row strong (Trang Oul's Claws, Carrion Wind, Gore Riders, Jalal's Mane). Contagion-spreading mechanic verbatim confirmed. Author credit: Deleted User 632 (diablo2.io).
- **d2-sacrifice (TRIPLE):** identity+mechanics CONFIRMED; negative_canon CONFIRMED — self-damage ceiling confirmed by community text ("you are only attacking once, which means clearing anything is going to be time consuming"). Era = NULL-kit; no era verdict issued. Wayback instrument: Arreat Summit paladin combat skills page returned `archived_snapshots: {}` on two attempts (timestamps 20050101, 20040601). WebFetch to web.archive.org blocked by tool. Era row filed as UNSUPPORTED per honest-UNSUPPORTED law; Wayback availability API result recorded as retry evidence in citation row (cite_class: official, rank_class: recovered). Attested eras from fetched text: d2r-era (patch 2.4 referenced on diablo2.io skill page) and pre-Resurrected discussion. No classic-era or lod-era attestation recovered.
- **d2-singer:** identity+mechanics+lod+d2r CONFIRMED; rotw-s14 UNSUPPORTED. Patch 1.10 origin of "Singer" build identity verbatim confirmed on diablo2.io War Cry skill page. Author credit: Blubbalutsch (diablo2.io).
- **d2-smiter:** identity+mechanics+lod-1.10++d2r CONFIRMED. Strong item_alterations row (Grief, Fortitude, Guillaume's, Gore Riders, Dracul's Grasp). Smite auto-hit mechanic verbatim confirmed. Author credit: azeroti (diablo2.io).
- **d2-summon-druid:** identity+mechanics+lod+d2r-2.4+ CONFIRMED. D2R 2.4 buff to Summon Dire Wolf passive life bonus confirmed. Author credit: tmGrunty (diablo2.io). Note: guide title shows "3.2 RotW" — steward may wish to add rotw to era list for this kit.
- **d2-summonmancer:** identity+mechanics+classic+lod-1.10++d2r CONFIRMED; rotw-s14 UNSUPPORTED. Classic era confirmed via PureDiablo guide title presence (Bone/Summon V 2.0, older era guide).
- **d2-teleport-sorc (NULL-era):** identity+mechanics CONFIRMED. Era = NULL-kit; no era verdict issued. No damage or combat; pure utility/movement build identity confirmed by forum discussions (rush teleporter, Baal teleporter, mule roles). Attested eras from fetched text: classic through d2r (Teleport skill unchanged across all eras). No single era uniquely contested.

---

## Contradictions

None.

---

## SOURCE_NOT_FOUND kits

None.

---

## Dossier coverage

- skill_loop: 12/12 — 100%
- skill_geometry: 12/12 — 100%
- item_alterations: 5/12 — d2-rabies-wolf, d2-smiter, d2-poison-nova-necro abstained remaining; d2-sacrifice geometry abstained
- capstone_alterations: 1/12 non-abstained (d2-mosaic-sin Mosaic runeword)
- author_credit: 8/12 non-abstained
- variants: 11/12 non-abstained (d2-nova-sorc, d2-singer, d2-smiter, d2-teleport-sorc, d2-rabies-wolf, d2-meteorb, d2-poison-javazon, d2-poison-nova-necro, d2-summon-druid, d2-summonmancer, d2-sacrifice — all populated; d2-mosaic-sin abstained)

Estimated overall dossier non-abstained rate: ~70% (advisory; steward to count from file).

---

## Author credits

| kit_id | handle | site |
|---|---|---|
| d2-mosaic-sin | Teebling | diablo2.io |
| d2-nova-sorc | saggytits | diablo2.io |
| d2-nova-sorc | APKefka | diablo2.io |
| d2-poison-nova-necro | Schnorki | diablo2.io |
| d2-rabies-wolf | Deleted User 632 | diablo2.io |
| d2-sacrifice | Maldoror | diablo2.io |
| d2-singer | Blubbalutsch | diablo2.io |
| d2-smiter | azeroti | diablo2.io |
| d2-summon-druid | tmGrunty | diablo2.io |

PureDiablo author handles: not recoverable (403 on direct fetches; guide pages show no byline in search snippets). purediablo.com guide-page author credits are SNF for this batch — 403 blocks byline recovery.

---

## Red flags

1. **d2-sacrifice Wayback null result:** Arreat Summit `classic.battle.net/diablo2exp/skills/paladin/combatskills.shtml` returned `archived_snapshots: {}` at both timestamp=20050101 and timestamp=20040601. Separate attempt at `/skills/paladin/` directory also empty. `web.archive.org` snapshot fetches blocked by tool. Classic-era Arreat Summit snapshot for Sacrifice not recoverable in this pass. Retry evidence stored in citations row (cite_class: official, rank_class: recovered). **Steward: this URL may need a direct Wayback CDX API probe or alternate timestamp range.**
2. **d2-sacrifice negative_canon anchor quality:** Anchor quote from diablo2.io community forum ("you are only attacking once, which means clearing anything is going to be time consuming") is indirect — it documents clearing speed as the endgame problem rather than the sustain ceiling framing in the spec's negative_canon_target. The self-damage/sustain ceiling framing is corroborated by the skill page's mechanic description. No single verbatim quote captures both dimensions cleanly; anchor quote chosen is the strongest available from fetched text.
3. **d2-summon-druid guide titled "3.2 RotW Summon Druid Guide"** (tmGrunty, diablo2.io) — era_attested in fetched text includes rotw-era context. Spec eras for this kit are `lod;d2r-2.4+` and do not include rotw. Steward/Elrond may wish to add rotw-era token. Internal inconsistency; verdict issued against fetched text only (both lod and d2r-2.4+ CONFIRMED).
4. **d2-mosaic-sin eras:** Spec lists `rotw-s13+;d2r-2.6+`. Mosaic runeword page states "As of 3.1 (Reign of the Warlock), Mosaic can only be made in Non-Ladder." This implies it transitioned to NL-only in a rotw patch. The rotw-s13+ token is post-cutoff so left UNSUPPORTED per post-cutoff law; the ladder/NL transition is a flag for steward — the rotw era claim may need nuance (non-ladder only post-3.1).
5. **PureDiablo 403:** All direct purediablo.com fetches returned 403 throughout batch. All PureDiablo content in this batch recovered from search snippets only. PureDiablo bylines not recoverable. This pattern held across batches 01-03 as well — consistent with post-amendment briefing.

---

## STEWARD AUDIT ADDENDUM (gandalf, 2026-07-18 — CW2, audited on return)

**ACCEPTED, 0 corrections.** File truth: **51 rows = 44C/7U/0X/0SNF** (advisory "~37C/~13U" — crawl-drift series #14, C drifted by 7; kits 12 ✓, families 12/12/26/1, per-era-token rows used ✓, negative_canon exactly 1 per roster — d2-sacrifice ✓). Anchors: C/X all present, zero >40w. Abstain-null law HELD 27/27. Citations 27/0 quarantined (purediablo 11 snippet-recovered · diablo2.io 15 · web.archive.org 1 retry-evidence row). Dossier 72 rows, 45 non-abstained = 62.5% — d2 old-canon abstain density expected (capstone 1/12; d2 runeword/synergy material is thin outside compendium pages).

**Sacrifice triple (NULL-era + negative + wayback) handled cleanly:** negative_canon CONFIRMED on fetched community text ("you are only attacking once…" — clear-speed framing; self-damage/sustain corroborated by skill-page mechanics, red-flag #2's honesty about anchor indirectness is CORRECT handling, not a defect). NULL-era = nothing-to-contradict ✓. **Wayback: availability API returned `archived_snapshots: {}` at 2004/2005 timestamps for the Arreat Summit combat-skills URL — NOT the CW1 instrument failure (protocol was followed); this is a genuine empty-availability result → BACKFILL-3 upgraded: d2-sacrifice needs a CDX-API probe (`http://web.archive.org/cdx/search/cdx?url=…`) or wider timestamp range, steward/micro-agent vehicle.**

**Erratum queue adds (INGEST-13):** d2-summon-druid — tmGrunty guide is titled "3.2 RotW Summon Druid Guide" → rotw era-token BACKFILL candidate (spec eras `lod;d2r-2.4+` attested C; rotw attested in fetched text but absent from spec) · d2-mosaic-sin — "As of 3.1 (Reign of the Warlock), Mosaic can only be made in Non-Ladder" → rotw-s13+ era row needs NL-only nuance at ingest (post-cutoff token left honest-U per law ✓). PureDiablo 403 byline-wall = standing pattern (b01–b04), author_credit 8/12 all diablo2.io.
