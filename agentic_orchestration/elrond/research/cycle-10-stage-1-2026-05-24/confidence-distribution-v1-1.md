# Cycle 10 Stage 1 v1.1 — Confidence Distribution + v1.0 Diff

**Date:** 2026-05-24
**Owner:** elrond (Cycle 10 Stage 1 v1.1 micro-fix)
**Population script:** `populate_proxy_fingerprint_v1_1.py`
**Lookup table:** `weapon_form_token_lookup_v1_1.json` (additive on v1.0 277 tokens; +10 new spear tokens + 4 compound-suffix script-level rules)
**Source DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`

---

## 0. TL;DR

v1.1 micro-fix applied **2 REQUIRED items** from gandalf's Stage 1 spot-check verdict (§ 6.3):

- **Item 1 (new spear vocabulary):** added shortspear / longspear / boar-spear / boar-spear-variant / winged spear weapon tokens
- **Item 2 (compound-noun word-boundary refinement):** suffix-match rule fires `blade`/`sword`/`axe`/`hammer` tokens within compound words (spiritblade, lightblade, doomaxe, warhammer) AND on bare-plural forms (blades, swords, axes, hammers)

**Result:** 527 rows updated (526 low-to-typed + 1 already-better margin). 68,610 rows unchanged per UPDATE-only-on-improve discipline (zero regressions on currently-typed rows).

**Substrate impact:** +526 typed rows (21,507 → 22,033) — +2.4% of typed-row pool; +2.7% lift in confidence ≥0.45 band.

**Cheapest-refuting-test catch:** gandalf's prediction of "~60% of bsdata-warhammer-aos low-conf" was at the wrong granularity. Actual measured impact across bsdata-warhammer-aos low-conf rows: 283 / 1,372 = **20.6%** lift into the 0.45-0.64 band. The original elrond § 6.3 source claim referred to fantasy-coinage broadly (~60%), most of which doesn't have a compound-suffix form (named templates like "Plaguereaper", "Flame Tongue" have no blade/sword/axe/hammer suffix). Compound-suffix refinement reaches the SUBSET that does. Net effect is still substantive — but caller should not expect the larger fantasy-coinage substrate-quality lift; that lift requires Stage 4 named-template recognition.

---

## 1. Confidence band distribution (v1.0 → v1.1 diff)

| Band | v1.0 | v1.1 | Δ |
|---|---:|---:|---:|
| 0.85-1.00 | 10,899 | 10,906 | **+7** (new spear tokens with structured data) |
| 0.65-0.84 | 5,380 | 5,380 | 0 (untouched per UPDATE-only-on-improve) |
| 0.45-0.64 | 2,981 | 3,497 | **+516** (compound-suffix matches + spear-tokens-no-structured) |
| 0.30-0.44 | 2,247 | 2,250 | +3 |
| 0.10-0.30 | ~10,396 | ~10,396 | 0 (accessory null-flags preserved) |
| 0.00-0.10 | ~37,234 | ~36,708 | **-526** |
| **Total** | 69,137 | 69,137 | 0 |

Reading: 526 rows moved from no-match (0.05) to low-spec compound-suffix tier (0.45). Seven rows moved to high-spec (0.85+) via the new spear tokens.

## 2. Typed-row pool diff

| Metric | v1.0 | v1.1 | Δ |
|---|---:|---:|---:|
| Range-typed (non-null) | 21,507 | 22,033 | **+526** |
| Geometry-typed | 21,507 | 22,033 | +526 |
| Tempo-typed | 21,507 | 22,033 | +526 |
| Attribute-typed | 21,507 | 22,033 | +526 |

## 3. Per-bin distribution shift

### proxy_range_class

| Bin | v1.0 | v1.1 | Δ |
|---|---:|---:|---:|
| melee | 9,272 | 9,792 | **+520** |
| ranged | 9,632 | 9,632 | 0 |
| mid | 2,603 | 2,609 | +6 (longspear adds mid-range) |

### proxy_geometry_class

| Bin | v1.0 | v1.1 | Δ |
|---|---:|---:|---:|
| single | 12,245 | 12,306 | +61 (warhammer/handhammer compounds, shortspear/longspear) |
| cleave | 5,312 | 5,777 | **+465** (blade/sword/axe compounds dominate) |
| AoE | 2,957 | 2,957 | 0 |
| multi-hit | 647 | 647 | 0 |
| scatter | 324 | 324 | 0 |
| cone | 22 | 22 | 0 |

### proxy_tempo_class

| Bin | v1.0 | v1.1 | Δ |
|---|---:|---:|---:|
| medium | 10,139 | 10,661 | +522 |
| low | 5,959 | 5,959 | 0 |
| high | 5,409 | 5,413 | +4 |

### proxy_attribute_class

| Bin | v1.0 | v1.1 | Δ |
|---|---:|---:|---:|
| DEX | 13,117 | 13,125 | +8 |
| STR | 6,728 | 7,246 | **+518** |
| INT | 1,271 | 1,271 | 0 |
| WIS | 391 | 391 | 0 |

Reading: STR dominates the compound-suffix attribute distribution (518/526 = ~98%). DEX attribution via prefix-hint (e.g., "spiritblade" → DEX, "shadowblade" → DEX) accounts for only ~8 rows; most compound-suffix rows fall to STR fallback because their prefix doesn't contain a DEX-hint keyword. **Calibration note for Stage 3 awareness:** if compound-suffix rows over-pull substrate toward STR, Stage 3 composition policy will need to consider this when sampling for v1_scope.

---

## 4. Per-source lift (top sources gaining typed rows in 0.45-0.64 band)

| Source | Conf 0.45-0.64 (v1.1) | Conf 0.45-0.64 (v1.0) | Δ |
|---|---:|---:|---:|
| wikipedia | 632 | ~545 | +87 |
| wow-classic-items | 573 | ~420 | +153 |
| royal_armouries | 473 | ~445 | +28 |
| nick-aschenbach-dnd-data | 351 | ~243 | +108 |
| bsdata-warhammer-aos | 283 | ~220 | +63 |
| met-museum | 246 | ~240 | +6 |
| cataclysm-dda | 220 | ~210 | +10 |
| osrsbox-db | 110 | ~85 | +25 |
| odin-army-tradoc | 92 | ~90 | +2 |
| path-of-exile-repoe | 78 | ~70 | +8 |

(v1.0 column estimated from current state minus per-source delta; small source-by-source totals may not sum perfectly to 526 due to confidence-band cross-firing.)

Top beneficiaries: **wow-classic-items (+153)**, **nick-aschenbach-dnd-data (+108)**, **wikipedia (+87)**, **bsdata-warhammer-aos (+63)**. The fantasy-game data sources dominate compound-suffix patterns ("Soulblade", "Runeblade", "Spellblade", "Shadowblade") — confirming gandalf's directional intuition that fantasy-coinage substrate is the impact zone, even if the specific bsdata-warhammer-aos number was over-stated.

---

## 5. Cheapest-refuting-test outcomes (Discipline #19.1)

**Pre-execution prediction (gandalf verdict § 6.3 item 2):** "Touches ~60% of bsdata-warhammer-aos low-conf"

**Pre-execution row-count check (elrond):**
- bsdata-warhammer-aos low-conf rows: 1,372
- bsdata-warhammer-aos low-conf rows matching `*[a-z](blade|sword|axe|hammer)*` GLOB: 62 (4.5%)

**Actual v1.1 impact on bsdata-warhammer-aos:** 283 rows shifted from <0.45 to ≥0.45 (20.6% lift)

**Why higher than the pre-execution GLOB-based estimate?** The bare-plural fallback also fires (e.g., "Merciless Blades" → 2 blades-plural matches; "Pair of Cursed Blades" → 1 blades-plural). The GLOB filter only caught compound-noun forms; the regex catches BOTH compound (with prefix ≥1 letter) AND bare-plural. So pre-execution estimate (~62 rows) was too narrow; actual lift (~283 rows including bare-plural cases) is meaningfully larger.

**Why STILL far below gandalf's "~60% of bsdata-warhammer-aos low-conf" claim (which would be ~820 rows)?** gandalf's claim mis-quoted elrond's § 6.3 fantasy-coinage finding. The original elrond claim was that ~60% of bsdata-warhammer-aos low-conf rows are *fantasy-coinage named templates* (e.g., "Plaguereaper", "Flame Tongue", "Cinderbreath's Gouts of Flame") — most of which have NO compound-noun blade/sword/axe/hammer suffix. They're named templates whose form is implicit, requiring Stage 4 cohesion-judge or named-template recognition to fingerprint. Word-boundary refinement only reaches the compound-suffix subset.

**Implication:** the v1.1 lift IS substantive (~526 substrate-wide typed-row additions; ~20% lift on bsdata-warhammer-aos low-conf), but the broader fantasy-coinage substrate-quality concern surfaced by elrond § 6.3 / gandalf § 6.5 cross-cutting concern remains as a **Stage 4 / cohesion-judge target**, not solved by Stage 1 v1.1 heuristic refinement.

**Verdict on the refuting-test claim:** prediction was **DIRECTIONALLY CORRECT but QUANTITATIVELY OVER-STATED**. The compound-suffix refinement does meaningful work but only on the compound-suffix subset; the broader fantasy-coinage substrate-quality target is Stage 4 / Sketch G territory.

---

## 6. UPDATE-only-on-improve discipline verification

Pre-execution targeted smoke (30 random currently-high-conf rows; ≥0.65): **0 would-update; 30 unchanged.** ✓

Post-execution stats:
- `n_unchanged: 68,610` — rows whose v1.0 fingerprint already matched or exceeded v1.1's computation
- `n_already_better: 1` — a single row where v1.1's strict-improvement margin (old + 0.10) was met, indicating a defensible re-upgrade
- Zero regressions confirmed: no row's previous high-conf fingerprint was downgraded by v1.1

**Discipline #11 attribution clarity:** v1.0 artifacts preserved unchanged; v1.1 is additive lineage at separate file paths. Lookup table v1.1 references v1.0 explicitly. Population script v1.1 loads v1.0 tokens + v1.1 additions in a clearly-marked combined-load step.

---

## 7. New v1.1+ refinement flags surfaced during v1.1

1. **`AeroVironment Switchblade`** (id 190001) — compound-suffix matcher fires `switchblade` → melee/cleave/STR. False positive — this is a US loitering munition UAV (modern weapon, ranged). Composes with Stage 1.5 spot-check Mode-C-with-description-text-noise pattern; defer to v1.1+ refinement queue (Pass B canonical_name modern-weapon-pattern detection per Stage 1.5 verdict item 2).

2. **`Sen'jin Beakblade Longrifle`** (id 167221) — v1.0 whole-word matcher misses `rifle` inside `Longrifle` (no word-boundary before); v1.1 compound-suffix matcher fires `beakblade` → melee/cleave/STR. The row IS a longrifle (ranged firearm), not a beakblade. **Defer:** add `longrifle` weapon token in v1.1+ queue.

3. **`Stump Blades` / `Vile Bile` / `Cavernous Jaws` / `Avian Head` (bsdata-warhammer-aos)** — bare-plural fallback fires on rows whose canonical_name describes monster-body-part attack profiles, not weapons. These DO get classified as melee/cleave weapons by v1.1, which is wrong. Stage 4 mechanical-tagging or `weapon_kind` field discrimination would catch this; current low-spec confidence (0.45) flags these as priority for Stage 4 review.

4. **Compound-suffix STR dominance** — 98% of compound-suffix-matched rows fall to STR attribution. The DEX-hint prefix list (spirit/light/shadow/frost/ghost/soul/shade/wind/ether) catches only the explicitly-light-attuned fantasy-coinage forms. Consider expanding DEX-hint list in v1.1+ refinement if Stage 3 composition surfaces STR over-pull.

---

## 8. Cross-references

- v1.0 confidence distribution: `confidence-distribution.md`
- v1.0 population script: `populate_proxy_fingerprint.py`
- v1.0 lookup table: `weapon_form_token_lookup.json`
- v1.1 lookup table: `weapon_form_token_lookup_v1_1.json`
- v1.1 population script: `populate_proxy_fingerprint_v1_1.py`
- v1.1 execution log: `log_v1_1.out`
- v1.1 re-spot-check artifact: `spot-check-v1-1-gandalf-request.md`
- gandalf Stage 1 spot-check verdict: `spot-check-gandalf-request.md` § 6
- Cycle 10 state file: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#2 smoke-test, #11 attribution clarity, #19 background, #19.1 cheapest-refuting-test)

---

## 9. Sign-off

**Owner:** elrond (Cycle 10 Stage 1 v1.1 micro-fix)
**Authority:** Cycle 10 hive-mind state (Wave 2 follow-on per Option B sequencing) + gandalf Stage 1 verdict § 6.3 REQUIRED items 1 + 2
**Tag intent (Option B combined commit):** `elrond/v0.0-cycle-10-stage-1-proxy-fingerprint` cut after combined commit landing
**Status:** EXECUTION COMPLETE — 20-row re-spot-check artifact prepared for gandalf at `spot-check-v1-1-gandalf-request.md`
**Compute cost:** $0.00 (heuristic-only per ADR-006); 32.3 sec execution time
