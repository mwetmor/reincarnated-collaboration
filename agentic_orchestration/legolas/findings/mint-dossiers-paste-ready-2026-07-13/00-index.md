# Mint Kit Dossiers — Paste-Ready Index (S1 Parallel Track)

**Commissioned by:** gandalf (S1 data completion wave, §3 of wind-down note 2026-07-13)
**Filed:** legolas, 2026-07-13
**Purpose:** 9 paste-ready mint-kit evidence dossiers + URL backfill manifest, formatted for elrond ingest (clears `dossier_owed = 1` in corpus.db rebuild)
**Collision rule observed:** corpus.db NOT read or written during this session (elrond rebuild window per commission)
**Prior dossiers:** `legolas/research/mint-list-dossiers-2026-07-12/` (preliminary Markdown) + `legolas/research/megaprobe-2026-07-12/mint-dossiers-reexpressed.jsonl` (structured JSON) — this is the upgraded paste-ready series

---

## ⚠ CRITICAL FLAG — GAME ATTRIBUTION ERROR: kit `poe1-ring-of-shields`

**"Ring of Shields" is a Last Epoch Sentinel → Forge Guard skill, NOT a PoE1 skill.**

Evidence confirmed 2026-07-13 via live sources:
- [Ring of Shields — Last Epoch Wiki](https://lastepoch.fandom.com/wiki/Ring_of_Shields): "Ring of Shields is a Forge Guard Summon Skill which is unlocked at level 5."
- Multiple searches for "Ring of Shields Path of Exile 1" and "Ring of Shields PoE2" returned NO matching skill gem.

**Elrond action:** When ingesting the dossier for `poe1-ring-of-shields`, correct `game` field to `le`. Update kit_id convention accordingly (`le-ring-of-shields` or `le-forge-guard-ring-of-shields`). Previous sessions (2026-07-12) flagged this as a knowledge gap — it is now resolved.

---

## 9 Dossiers

| # | corpus_kit_id | folk_name | game | era_year | stabilization_patch | status | mint_priority |
|---|---|---|---|---|---|---|---|
| 01 | `poe1-totem-hierophant` | Totem Hierophant / Ancestral Warchief | poe1 | 2016 | v2.3.0 | positive | HIGH |
| 02 | `d3-call-of-the-ancients` | Call of the Ancients Barbarian / IK Ancients | d3 | 2017 | v2.6.1 | positive | HIGH |
| 03 | `poe1-ring-of-shields` ⚠ | Ring of Shields — Forge Guard (**game=le, not poe1**) | **le** ⚠ | 2024 | v1.0 | positive | MED |
| 04 | `poe1-blood-magic-kit` | Blood Magic Life-as-Resource | poe1 | 2015 | v2.0.0 | positive | MED |
| 05 | `d2-teleport-sorc` | Teleport Sorceress / Enigma Teleporter | d2 | 2003 | v1.10 | positive | MED |
| 06 | `d3-dashing-strike-monk` | Dashing Strike Monk | d3 | 2016 | v2.4.2 | positive (brief_era) | MED |
| 07 | `le-shift-bladedancer` | Shift Bladedancer | le | 2024 | v1.0 | positive | MED |
| 08 | `poe1-vaal-blade-vortex` | Vaal Blade Vortex | poe1 | 2016 | NULL | positive | LOW-MED |
| 09 | `d2-sacrifice` | Sacrifice (Paladin) | d2 | 2001 | NULL | positive + negative_annotation | LOW |

---

## Slot-confidence matrix

Key: H = HIGH · M = MED · L = LOW

| # | kit_id | attr | range | tempo | amp | proxy | commit |
|---|---|---|---|---|---|---|---|
| 01 | poe1-totem-hierophant | STR/M | mid/M | low/M | flat/M | heavy/H | instant/H |
| 02 | d3-call-of-the-ancients | STR/H | melee/H | low/M | spiky/M | light/M | instant/H |
| 03 | poe1-ring-of-shields (game=le) | STR/M | mid/M | low/M | flat/M | light/M | instant/M |
| 04 | poe1-blood-magic-kit | INT/M | mid/L | high/M | flat/M | solo/H | instant/H |
| 05 | d2-teleport-sorc | INT/H | ranged/H | high/H | flat/M | solo/H | instant/H |
| 06 | d3-dashing-strike-monk | WIS/H | melee/H | high/H | flat/M | solo/H | instant/H |
| 07 | le-shift-bladedancer | DEX/H | melee/H | high/H | flat/M | solo/H | instant/H |
| 08 | poe1-vaal-blade-vortex | INT/M | melee/M | high/H | flat/M | solo/H | instant/M |
| 09 | d2-sacrifice | STR/H | melee/H | med/M | spiky/M | solo/H | instant/H |

---

## Actions for downstream agents

**→ Elrond (priority order):**
1. **⚠ CRITICAL:** Correct `game = poe1 → le` for `poe1-ring-of-shields`; update kit_id and all cross-references
2. Kit 02 (d3-call-of-the-ancients): reconcile vs any existing `d3-ik-hota` record — recommend DISTINCT row for proxy-light CotA identity
3. Kit 03 (ring-of-shields): note "Replica" variant mentioned in original V4-r2 brief is NOT documented in Last Epoch; may be a cross-game confusion — flag for review
4. Kit 04 (blood-magic-kit): reconcile vs any existing PoE1 RF records; recommend standalone row for keystone-economy identity
5. Kit 05 (teleport-sorc): reconcile vs any existing `d2-blizzard-sorc` etc.; recommend standalone row for movement-verb identity
6. Kit 07 (le-shift-bladedancer): note proxy dual-layer — `proxy_primary = solo; proxy_extended = light` (Shadow generation extension)
7. Kit 08 (vaal-blade-vortex): reconcile vs any existing `poe1-blade-vortex` and `poe1-poison-bv` records; confirm grain separation
8. Kit 09 (d2-sacrifice): flag `negative: true` annotation; mint for GX-06 evidential value (Matt ruling pending — see below)

**→ Matt (ruling queue, carried forward):**
1. Kit 09 (d2-sacrifice): NEGATIVE CANON recommendation pending Matt's ruling. Legolas recommends: mint as negative-canon for GX-06 evidential value.
2. Kit 06 (d3-dashing-strike-monk): brief_era flag vs positive-canon — is the shallow canon value sufficient for a positive mint, or should this also be negative-annotated? Legolas recommendation: positive with `brief_era: ["v2.4.2"]`.

**→ Gandalf:**
1. Kit 03 (ring-of-shields) game correction confirmed — the "(Sentinel Guard)" parenthetical correctly identifies the Last Epoch Sentinel Forge Guard class.
2. Kit 08 (poe1-vaal-blade-vortex): `stabilization_patch = NULL` — exact VBV introduction patch not confirmed; naming-law label for this kit omits the patch segment: `PoE1-2016 · Vaal Charge Spinning Blades`.

---

## URL-backfill manifest

→ See `url-backfill-manifest-2026-07-13.md` in this directory.

---

## Research methodology note

Prior session (2026-07-12) dossiers were preliminary research documents. This S1 upgrade:
- Adds explicit `era_year` and `stabilization_patch` fields (naming law §7.1 feed)
- Supplies live source URLs (not just `kb` references)
- Resolves the `poe1-ring-of-shields` game attribution error via live source confirmation
- Formats each dossier for elrond paste-in with no reshaping required
- Preserves honest NULL where patch data could not be verified (VBV, Sacrifice stabilization)
