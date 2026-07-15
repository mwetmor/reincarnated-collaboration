# Canon Harvest — D2 Corpus Report (calibration run)

**Delivered:** `canon-corpus-d2.jsonl` — **58 records, 100% valid JSON** (53 positive · 5 of 8 planned negatives inline as `negative:true` — blade-sin & golemancer sit in their class blocks; net 51 positive / 7 negative).
**Coverage:** Amazon 5 · Assassin 6 · Barbarian 8 (incl. BvC PvP) · Druid 7 · Necromancer 5 · Paladin 7 · Sorceress 9 · **Warlock 6 (post-cutoff era)** · negatives across classes.
**Method:** knowledge-derived for the settled eras (D2 canon is 25-year consolidated history) + **search-derived for the RotW era**, per-record confidence reflecting the split. Provenance keys → §4.

## §1 — Era strata (the rider fired immediately)
`classic` (2000) · `lod-1.09` (Firewall/Fishyzon era) · `lod-1.10+` (synergy revolution — most deep canon born here) · `lod-1.11+` (runeword auras) · `d2r-2.x` (2.4 buff-rebirths: FoH, Hydra, Fire Druid, Throw, Daggermancer; 2.6 Mosaic) · **`rotw-s13+`** — a *Reign of the Warlock* expansion (8th class, Seasons 13–14, patch 3.2) that **postdates the harvester's training**. The era rider caught a content stratum the harvester didn't know existed — exactly what it's for. Warlock records carry low confidence + heavy abstains; **full dossier pass owed** from live sources.

## §2 — Gap register (fires into projection-atlas §3)
| Gap | Finding | Routes to |
|---|---|---|
| GAP-D2-01 | **Movement verbs are load-bearing genre-wide** — Teleport (every sorc, Enigma-era every class), Charge (verb IS the damage), Leap, plus Blaze as movement-paints-damage inversion | B5/B6 · F4 priority CONFIRMED (pre-registered) |
| GAP-D2-02 | **Form-shift family** (Fury/Rabies/Maul/Fireclaws) — a form is a stat-and-skill BODY swap; kit-within-kit state | pre-registered NOVELTY CONFIRMED — no roster surface; candidate CODEX-SURFACE (form-state machine) or T4 family; hearing owed |
| GAP-D2-03 | **Mark-and-consume charges** (MA charge-up; Mosaic's persist-exception) | §5 surface #6 phase axis (ladder #4) evidence — strong |
| GAP-D2-04 | **Corpse-as-resource economy** (CE, Raise-from-corpse, Find Item, Grim Ward) | Axis-5 **reserved-bin candidate occupant** — named |
| GAP-D2-05 | Party-external scaling (Enchant-on-others, BO) | out-of-scope solo filter; note for mob/party layer |
| GAP-D2-08 | Overlapping-cloud DoT stacking (Plague Jav) | blacklist-adjacent note for DoT geometry rules |
| GAP-D2-09 | **Terrain-occlusion walls** (Bone Prison/Wall as build-relevant control) | B4 re-spike evidence (pre-registered) |
| GAP-D2-10 | **Tri-element single-swing** (Avenger/Vengeance) exceeds the one-secondary cap | element addendum edge: rider-stack vs cap exception — ruling owed |
| GAP-D2-11 | **Bind Demon = enemy-conversion economy in official D2** (Warlock) | converts-archetype evidence + striking reap-verb adjacency (fiction note for Matt) |

## §3 — The abstain law, demonstrated
Abstains cluster exactly where they should: `econ` (the 7-bin enum not visible to the harvester — every record carries source-vocab labels like corpse-resource/mana-hungry/charge-builder awaiting bin mapping), `mob` (engagement's mobility half — R-2 catalog-blind anyway), `elem_*` (**all element values in D2 source vocab with `abstain_map:true`** — the canonical 8-element enum stays unguessed), and Warlock-era axes (thin sources → c≤0.4 + abstains rather than confabulation). Reconciliation work queue = every `abstain:true`.

## §4 — Provenance legend
`mx` maxroll.gg/d2 tierlists · `iv` icy-veins.com/d2 PvM rankings · `dw` diablo-wiki.com/tier-list · `od` odealo S14 build list · `aoe` aoeah S13/RotW list · `ph` playhub 2026 tier list · `dx` dexerto S10 · `sk` sportskeeda S13 · `kb` = settled community canon (Amazon Basin wiki / Arreat Summit archive / r/diablo2 lineage) — **live-URL backfill owed by the team for kb rows** (Wayback for era-authentic 1.09/1.10 lists).

## §5 — Roster cross-references (reconciliation preview)
Direct anchor confirmations: Hammerdin→K20 (orbiter_spiral cast_point noted in-record) · WW Barb→K1/B12 (channel bin) · Meteorb→chain_partition co_equal anchor · Summonmancer→K17 · Summon Druid→K24 · Trapsin→K11 (stationary emitters) · Hydra→H4/K18 turret shape · Frenzy/Maul→K28 on-hit-builder shapes · Blood Boil Warlock→K26/K29 adjacency check owed. Verdict column (`duplicate-of/variant-of/new-cell`) deferred to the reconciliation stage per spec §3.4.

## §6 — Calibration lessons → PoE1 run
1. Schema held; per-axis `{v,c,abstain}` is the right grain. 2. **Negative canon is harvestable in-line** at near-zero marginal cost. 3. Era stratification is not optional — it caught a whole expansion. 4. `kb` provenance is acceptable for settled history but each record should gain ≥1 live URL at audit; PoE1 won't need the crutch (PoB/poe.ninja are Rank-1). 5. PvP builds (Ghost, BvC, Charger) project fine but need a `context:pvp` tag next run. 6. Estimated PoE1 scale: several hundred records — chunked emission (~20/write) with per-chunk JSON validation, exactly as run here.
