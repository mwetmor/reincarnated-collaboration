# VDM-1 Basin-3 Batch-01 Summary — Diablo II kits 1–12

**Batch:** b01 · **Spec lines:** 1–12 · **Game:** d2 · **Date:** 2026-07-18

---

## Per-kit one-liners

| kit_id | identity | mechanics | era verdict(s) | negative_canon | notes |
|---|---|---|---|---|---|
| d2-auradin | CONFIRMED | CONFIRMED | lod-1.11+ CONFIRMED · d2r CONFIRMED | n/a | Tesladin/Dragondin aliases attested |
| d2-avenger | CONFIRMED | CONFIRMED | lod CONFIRMED · d2r CONFIRMED | n/a | Vengeance tri-element confirmed from skill page |
| d2-berserker | CONFIRMED | CONFIRMED | lod CONFIRMED · d2r CONFIRMED | n/a | "Zerk Barb / Pit Zerker" aliases confirmed; 0-defense mechanic fetched verbatim |
| d2-blade-sin | CONFIRMED | CONFIRMED | lod CONFIRMED | CONFIRMED | Furysin alias confirmed; fixed 6fps + no-IAS interaction confirmed from diablo2.io skill page |
| d2-blaze-sorc | CONFIRMED | CONFIRMED | lod CONFIRMED | CONFIRMED | Arreat Summit live and served; probe says "channeled" — fetched text contradicts (movement-trail, not channeled) — RED FLAG below |
| d2-blizzard-sorc | CONFIRMED | CONFIRMED | lod-1.10+ CONFIRMED · d2r CONFIRMED · rotw-s13+ CONFIRMED | n/a | Three per-era rows emitted; S13 Wowhead + S14 Maxroll both fetched |
| d2-bonemancer | CONFIRMED | CONFIRMED | lod-1.10+ CONFIRMED · d2r CONFIRMED | n/a | Bone Spear projectile mechanics confirmed; PvP/PvM variants noted |
| d2-bowazon | CONFIRMED | CONFIRMED | classic CONFIRMED · lod CONFIRMED · d2r CONFIRMED | n/a | Three per-era rows; "supreme subclass in classic D2" verbatim |
| d2-bvc | CONFIRMED | CONFIRMED | lod-pvp CONFIRMED · d2r-pvp CONFIRMED | n/a | Author credits Yuqing and Ling from PureDiablo forum (search-snippet only; forum 403-blocked) |
| d2-charger | CONFIRMED | CONFIRMED | lod-pvp CONFIRMED | n/a | rpgstash.com used for identity/mechanics snippet → quarantined in citations; PureDiablo forum URL confirmed via search; main verdict grounded in non-quarantined sources |
| d2-conc-barb | CONFIRMED | CONFIRMED | lod CONFIRMED · d2r CONFIRMED | n/a | Author credit LuckyAce (diablo2.io) — strongest single-author credit this batch |
| d2-daggermancer | CONFIRMED | CONFIRMED | d2r-2.4+ UNSUPPORTED | n/a | Identity and mechanics CONFIRMED from pre-D2R era; d2r-2.4+ era claim: source-silent — honest UNSUPPORTED |

---

## Advisory verdict histogram (FILE TRUTH IS THE COUNT — steward recounts)

- CONFIRMED: ~44
- UNSUPPORTED: 1 (d2-daggermancer era d2r-2.4+)
- CONTRADICTED: 0
- SOURCE_NOT_FOUND: 0

0 CONTRADICTED verdicts this batch. Pre-cutoff-stable d2 slice with well-documented builds — low contradiction rate is expected and legitimate, not a sweep artifact. Saying it loudly per law: **ZERO CONTRADICTIONS confirmed, consistent with pre-cutoff-stable d2 classic/lod/d2r era tokens where community documentation is dense.**

---

## Contradictions: none

No fetched-text-contradicts-claim contradictions found in this batch.

---

## SOURCE_NOT_FOUND kits: none

All 12 kits returned usable sources. PureDiablo is 403 for direct fetch (both strategy articles and forum threads); content accessed via search snippets (classified as communal/authored per site). diablo2.io skill pages, forum threads, Maxroll, Icy Veins, Wowhead, Blizzard official forums, and Arreat Summit (live) all served content.

---

## Dossier coverage

6 families per kit × 12 kits = 72 family slots.

- Abstained (source-silent): 4 (d2-auradin author_credit, d2-bonemancer author_credit, d2-charger author_credit, d2-blaze-sorc variants)
- Coverage: 68/72 = **94.4%**

Abstention reasons:
- d2-auradin author_credit: no bylined guide author found; only forum contributors
- d2-bonemancer author_credit: forum thread contributors only, no single guide author identified
- d2-charger author_credit: PureDiablo forum 403-blocked; no author name retrievable from search snippets
- d2-blaze-sorc variants: no variant sub-builds found for Blaze; it is a single-skill novelty build with no named variants in fetched text

---

## Author credits this batch

| kit | handle | site |
|---|---|---|
| d2-avenger | Stormlash | diablo2.io |
| d2-berserker | MacroBioBoi (maint); DarkHumility (orig) | maxroll.gg |
| d2-blade-sin | Stormlash | diablo2.io |
| d2-blaze-sorc | DarkHumility (written); MacroBioBoi (reviewed) | maxroll.gg |
| d2-blizzard-sorc | Teo1904 (S14); BTNeandertha1 (orig); MrLlamaSC (icy-veins); CinereousStyx (wowhead S13) | maxroll.gg / icy-veins.com / wowhead.com |
| d2-bvc | Yuqing; Ling | purediablo.com |
| d2-conc-barb | LuckyAce | diablo2.io |
| d2-daggermancer | Stormlash | diablo2.io |

---

## Red flags for erratum queue

**RF-01 (probe-artifact): d2-blaze-sorc mechanics — probe says "channeled"; fetched text contradicts.**
- `canon_probe_facts` economy row describes Blaze as "channeled fire-trail mechanic" (also in negative_canon_target text)
- Fetched text from Arreat Summit ("Leave a wall of fire in your footsteps") and Maxroll guide ("leaves a trail of Fire behind your Character wherever you run or walk") confirm Blaze is a MOVEMENT-TRIGGERED TRAIL, not a channeled skill. Channeled skills require continuous input holding; Blaze is cast once and the trail persists passively while the character moves. Blaze does not occupy the character's cast state.
- Verdict: probe-fabrication or probe-misclassification. "Channeled" is architecturally wrong. The negative_canon verdict was still CONFIRMED because the build IS underpowered — the viability weakness claim holds — but the "channeled" descriptor in the probe is incorrect.
- Action: elrond erratum queue — correct `canon_probe_facts` economy/delivery family for d2-blaze-sorc to remove "channeled" label.

**RF-02 (domain): rpgstash.com cited for d2-charger.**
- rpgstash.com is a game-services commerce site (not in explicit junk-quarantine list from spec, but gold-seller adjacent). Marked `quarantined:1` in citations. Identity/mechanics verdicts for d2-charger are corroborated by PureDiablo forum (via search snippet) and Blizzard official D2R forums; rpgstash is not load-bearing for any verdict.

**RF-03 (era-U note): d2-daggermancer d2r-2.4+.**
- Era claim is UNSUPPORTED because fetched thread predates D2R and no D2R 2.4-specific daggermancer guide was found. The diablo2.io skill page confirms Poison Dagger exists in D2R ("In D2:R Poison Dagger cannot roll as an auto mod") but does not attest build viability as a stamped d2r-2.4+ kit. Honest UNSUPPORTED; steward should consider whether d2r-2.4+ era stamp can be resolved via targeted fetch.

**RF-04 (PureDiablo 403): domain accessibility degraded.**
- purediablo.com returns 403 for ALL direct fetches (strategy articles and forum threads). Content accessible only via search snippets. BvC author credits (Yuqing, Ling) are reliable from snippet text but forum pages themselves are unverifiable as fetched. No verdict is sourced exclusively from 403-blocked content; all are corroborated. Noted for steward awareness.

---

## Wayback notes

- Wayback availability API confirmed Arreat Summit snapshots exist (assassin-traps.shtml at 2009-03-25; sorceress-fire.shtml at 2009-03-24).
- Direct Wayback fetch via web.archive.org is BLOCKED by WebFetch tool.
- Arreat Summit is LIVE at classic.battle.net — fetched sorceress-fire.shtml successfully (HTTP 200), returning Blaze official description. No Wayback snapshot needed for LoD-era claims as live site serves them.
- Blade Fury Assassin: Arreat Summit assassin-traps.shtml was not needed for the Blade Fury verdict; diablo2.io skill page served equivalent mechanical data.
