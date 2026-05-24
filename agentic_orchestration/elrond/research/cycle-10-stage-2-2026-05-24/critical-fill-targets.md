# Cycle 10 Stage 2 — Per-Form-Archetype Critical-Fill Targets

**Date:** 2026-05-24
**Owner:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-cross-tab-thin-cell-surfacing.md`
**Companion:** `cross-tab.html` · `thin-cell-list.md` · `thin-tradition-list.md`

---

## 0. TL;DR

For each of the 25 Stage 0 cell-archetypes (~37 forms total), this artifact reports substrate-coverage status against Sketch B per-cell floors. Composes with `thin-cell-list.md` (cell-level granularity) and adds form-level granularity for Stage 3 design call + Stage 3.5 engine-author scope decisions.

**Total Stage 0 form-count:** ~37 (Sketch A § 1.2 distribution summary)
**Stage 0 cell-archetype count:** 25 (slight discrepancy vs Sketch A TL;DR's "~22 cells" — Section 1.1 lists 25 distinct cell-archetype rows)

| Status | Form count | Cells |
|---|---:|---|
| COVERED | ~24 forms across 13 cells | Heavy Barb (3), Light Fighter (2), Polearm Sold (1), Thrown-Heavy (1), Ancestor-Warrior (1-2), Dagger Assassin (3), Archer (2), Crossbow Sniper (1-2), Falconer (1), Trap Assassin (1-2), Standard Wizard (2), Arcane-Familiar (1), Totem Hierophant (1), Holy Knight (2) |
| MODE-A-THIN | 1 form | Twin-Blade Fencer (1) |
| UNDER-FLOOR-HIGHCONF | 2 forms | Light Fighter is in COVERED above; the UNDER-FLOOR-HIGHCONF designation is for the high-conf subset only |
| THIN | 1 form | Ritual Mage/Oracle (1) |
| CRITICAL | ~12 forms across 9 cells | Artillery Mage (2), Pyromantic Caster (1), Red Mage/Spellsword (1), Necromancer Summoner (2), Channeling Cleric (1), Storm Caller/Druid (1), Monk-archetype (1-2), Druid Beastmaster (1-2), Witch Doctor Petmaster (1) |

**Total critical-fill scope:** ~12 forms (~32% of v1) require external action (substrate-search / engine-author / descope) to populate.

---

## 1. STR-attribute forms (~9 of 37; ~24%)

| Cell | Archetype | Forms | Sketch B floor | Substrate typed | Status | Critical-fill quantity |
|---|---|---:|---|---:|---|---|
| 1 | Heavy Barbarian (D2 Whirlwind, D4 Pulverize) | 3 | 80-120 melee | 960 | COVERED | 0 |
| 2 | Light Fighter (D3 Crusader Sweep, PoE Slayer) | 2 | 80-120 melee | 476 typed (3 high-conf) | UNDER-FLOOR-HIGHCONF | Stage 4 mechanical-tagging priority (re-validate the 473 low-conf rows) |
| 3 | Polearm Soldier (D3 Crusader Phalanx) | 1 | 80-120 melee | 4,068 | COVERED | 0 |
| 4 | Thrown-Heavy / Atlatl | 1 | 60-100 ranged | 956 | COVERED | 0 |
| 5 | Ancestor-Warrior (D3 Ancients call, LE Primalist) | 1-2 | 40-60 light proxy | 960 (shared with cell 1) | COVERED | Stage 4 disambiguation from cell 1 needed |

**STR total: 9 forms; 0 critical-fill; 1 Stage 4 disambiguation; 1 Stage 4 re-validation.**

---

## 2. DEX-attribute forms (~10 of 37; ~27%)

| Cell | Archetype | Forms | Sketch B floor | Substrate typed | Status | Critical-fill quantity |
|---|---|---:|---|---:|---|---|
| 6 | Dagger Assassin (D2 Assassin, PoE Dual-Strike) | 3 | 80-120 melee | 2,730 | COVERED | 0 |
| 7 | Archer (D3 DH, PoE Tornado Shot) | 2 | 60-100 ranged | 1,705 | COVERED | 0 |
| 8 | Crossbow Sniper (D3 DH Cluster Arrow) | 1-2 | 60-100 ranged | 2,706 | COVERED | 0 |
| 9 | Twin-Blade Fencer | 1 | 60-100 mid | 215 | MODE-A-THIN | Sidecar B Filipino-arnis / Indian-katar enrichment OR accept Pan-Fantasy designation |
| 10 | Falconer / Pet-Archer (LE Rogue Falconer) | 1 | 40-60 light proxy | 1,705 (shared with cell 7) | COVERED | Stage 4 disambiguation from cell 7 needed |
| 11 | Trap Assassin / Mine-Mercenary (D2 Trap, PoE2 Merc) | 1-2 | 30-50 heavy proxy | 737 | COVERED | 0 |

**DEX total: 10 forms; 0 critical-fill; 2 Stage 4 disambiguations; 1 MODE-A-THIN (Twin-Blade Fencer).**

---

## 3. INT-attribute forms (~10 of 37; ~27%)

| Cell | Archetype | Forms | Sketch B floor | Substrate typed | Status | Critical-fill quantity |
|---|---|---:|---|---:|---|---|
| 12 | Standard Wizard (D3 Arcane Orb, KonoSuba Megumin) | 2 | 60-100 ranged | 269 | COVERED | 0 (close to floor) |
| 13 | Artillery Mage (D3 Meteor, D2 Frozen Orb) | 2 | 60-100 ranged | 3 | **CRITICAL** | **2 forms need engine-author OR fold into Standard Wizard via T4 algorithmic mechanic-alteration** |
| 14 | Pyromantic Caster (D3 Crusader Phalanx mid-INT) | 1 | 60-100 mid | 0 | **CRITICAL** | **1 form needs engine-author; contested cell per Sketch E** |
| 15 | Red Mage / Spellsword (D2 Sorc+melee, FF Red Mage) | 1 | 80-120 melee | 0 | **CRITICAL** | **1 form needs engine-author OR Phase 5 cohesion-judge over STR-melee base; contested cell per Sketch E** |
| 16 | Arcane-Familiar Mage (PoE Animate Guardian + caster) | 1 | 40-60 light proxy | 269 (shared with cell 12) | COVERED | Stage 4 disambiguation from cell 12 needed |
| 17 | Necromancer Summoner (D2/D3/D4 Necro) | 2 | 30-50 heavy proxy | 0 | **CRITICAL** | **2 forms need substrate-search OR engine-author; very high-priority (D-series Necro is iconic)** |
| 18 | Totem Hierophant (INT) (PoE Hierophant, D3 Familiar-stack) | 1 | 30-50 heavy proxy | 712 | COVERED | 0 |

**INT total: 10 forms; 6 critical-fill; 1 Stage 4 disambiguation. Iconic D-series Necromancer is the highest-pressure critical-fill.**

---

## 4. WIS-attribute forms (~9 of 37; ~24%)

| Cell | Archetype | Forms | Sketch B floor | Substrate typed | Status | Critical-fill quantity |
|---|---|---:|---|---:|---|---|
| 19 | Channeling Cleric (D3 WD, Slime Rimuru) | 1 | 60-100 mid | 3 | **CRITICAL** | **1 form needs substrate-search OR engine-author** |
| 20 | Holy Knight / Paladin / Hammerdin (D2, Mushoku Tensei) | 2 | 80-120 melee | 327 | COVERED | 0 |
| 21 | Ritual Mage / Oracle (D2 Druid summon, isekai oracle) | 1 | 60-100 ranged | 51 | **THIN** | **Sidecar B oracle/ritual vocabulary enrichment OR accept low floor** |
| 22 | Storm Caller / Druid (D4 Druid, Aboriginal/Celtic) | 1 | 60-100 ranged | 2 | **CRITICAL** | **1 form needs Sidecar B Celtic/Druidic enrichment OR engine-author** |
| 23 | Monk-archetype (D1 Hellfire, D3 Sunwuko, PoE2) | 1-2 | 80-120 melee | 0 | **CRITICAL** | **1-2 forms need Sidecar B East-Asian/South-Asian fist-and-staff enrichment OR engine-author** |
| 24 | Druid Beastmaster (D2 Spirit Wolves, LE Primalist-WIS) | 1-2 | 30-50 heavy proxy | 8 | **CRITICAL** (close to threshold) | **Sidecar B Celtic/Pacific enrichment (closest to floor among CRITICAL cells)** |
| 25 | Witch Doctor Petmaster (D3 WD Carnevil, D2 Necro Spirit) | 1 | 30-50 heavy proxy | 3 | **CRITICAL** | **1 form needs Sidecar B Sub-Saharan-African enrichment OR engine-author** |

**WIS total: 9 forms; 6 critical-fill; 1 THIN; 1 form near floor. WIS-attribute starvation is structural.**

---

## 5. Aggregate critical-fill scope

| Source of fill | Critical-fill forms | Substrate-rows needed (per-form floor avg ~60) | Discipline / mode |
|---|---:|---:|---|
| Sidecar B Egyptian crawl | 0 directly (anchors only) | ~3,600 baseline | Mode A enforcement |
| Sidecar B Sumerian / Mesopotamian crawl | 1 (Gilgamesh-anchored Tier-1 mythological form) | ~2,700 baseline | Mode A enforcement |
| Sidecar B Vedic / Hindu crawl | 1 (Karna-anchored Tier-1 mythological form) | ~3,500 baseline | Mode A enforcement |
| Sidecar B Mesoamerican crawl | 1 (Moctezuma-Quetzalcoatl form) | ~3,500 baseline | Mode A enforcement; Pre-Columbian filter |
| Sidecar B Celtic / Druidic enrichment | 2 (Storm Caller + Druid Beastmaster) | ~120 incremental | reclaim from `european` lineage |
| Sidecar B Sub-Saharan-African enrichment | 1 (Witch Doctor Petmaster) | ~50 incremental | `african` canonical exists (563 rows) |
| Sidecar B East-Asian / South-Asian fist-and-staff enrichment | 1-2 (Monk-archetype) | ~120 incremental | reclaim from `east_asian` + `south_asian` |
| Stage 3.5 engine-author (Pan-Fantasy / contested) | 4 (Pyromantic + Red Mage + Necromancer × 2) | engine-generated | bypasses substrate |
| Stage 4 mechanical-tagging re-validation | Light Fighter (473 low-conf rows) | re-classify existing | improves typed pool |
| Stage 4 disambiguation (collision pairs) | 5 pairs → 10 forms | mechanical-tag the proxy-density axis | improves routing precision |

**Total critical-fill scope:**
- **Sidecar B targets:** 5 sub-traditions to enrich; ~13,500 raw substrate rows desired (against ~89,841 baseline = ~15% growth)
- **Stage 3.5 engine-author scope:** 4 forms (Pyromantic Caster + Red Mage/Spellsword + Necromancer Summoner × 2)
- **Stage 4 priorities:** mechanical-tag the 5 collision-pair cells + re-validate the Light Fighter low-conf pool

---

## 6. Per-form sequencing recommendation for Stage 3 + Stage 3.5

### 6.1 Tier-1 (high impact, low cost) — engine-author at Stage 3.5
These 4 forms have ZERO substrate (substrate-search yields nothing); engine-authored gap-fills are the only path:
1. **Pyromantic Caster** (cell 14) — 1 form, ~80 weapons
2. **Red Mage / Spellsword** (cell 15) — 1 form, ~100 weapons
3. **Necromancer Summoner × 2** (cell 17) — 2 forms, ~40 weapons each (heavy proxy floor)

### 6.2 Tier-2 (substrate-recoverable via Sidecar B)
These forms have substrate signal but at THIN/CRITICAL counts; substrate-enrichment is the right path:
4. **Storm Caller / Druid** (cell 22) — Celtic/Druidic Sidecar B crawl
5. **Monk-archetype** (cell 23) — East-Asian + South-Asian fist-and-staff substrate-reclamation
6. **Druid Beastmaster** (cell 24) — Celtic/Pacific substrate-enrichment (closest to floor)
7. **Witch Doctor Petmaster** (cell 25) — Sub-Saharan-African substrate-enrichment
8. **Channeling Cleric** (cell 19) — WIS-attribute fingerprint follow-on + Sidecar B

### 6.3 Tier-3 (architecturally-reroutable)
9. **Artillery Mage** (cell 13) — fold into Standard Wizard via T4 algorithmic mechanic-alteration; descope as separate cell
10. **Ritual Mage / Oracle** (cell 21) — borderline THIN; either accept low floor or Sidecar B oracle/ritual vocabulary

### 6.4 Tier-4 (substrate refinement, not gap-fill)
11. **Light Fighter** (cell 2) low-conf pool — Stage 4 mechanical-tagging re-validation
12. **Twin-Blade Fencer** (cell 9) Mode-A authenticity — Sidecar B Filipino/Indian targeted crawl OR accept Pan-Fantasy
13. **5 collision-pair cells** — Stage 4 mechanical-tagging on proxy-density discriminator

---

## 7. Composition with Sketch B floors

Sketch B § 2.1 floors:
- 80-120 melee pure-attacker / 60-100 ranged-mid pure-attacker / 40-60 light proxy / 30-50 heavy proxy / +10-15 for Tier-S named-bearer / +30-50 off-hand items

Per-form-archetype critical-fill rolls up to:
- **Pure-attacker melee critical-fills:** Red Mage (cell 15; 80-120 floor) + Monk-archetype (cell 23; 80-120) + Light Fighter (cell 2; UNDER-FLOOR-HIGHCONF, 80-120) = ~3 melee floor-deficits
- **Pure-attacker ranged/mid critical-fills:** Artillery Mage (cell 13; 60-100) + Pyromantic Caster (cell 14; 60-100) + Channeling Cleric (cell 19; 60-100) + Storm Caller (cell 22; 60-100) + Ritual Mage (cell 21; 60-100 THIN) = ~5 ranged/mid floor-deficits
- **Light proxy critical-fills:** none (all light-proxy cells COVERED via parent cell)
- **Heavy proxy critical-fills:** Necromancer (cell 17; 30-50) + Druid Beastmaster (cell 24; 30-50) + Witch Doctor (cell 25; 30-50) = ~3 heavy-proxy floor-deficits

**Total floor-deficit aggregate:** ~3 × 100 + ~5 × 80 + ~3 × 40 = ~820 weapon-rows needed for floor satisfaction across critical cells.

This is a useful target magnitude for Stage 3.5 + Sidecar B planning: **~800-1,000 net new weapon-rows** in v1_scope are required to close all critical floors.

---

## 8. Composition with Sketch F named-bearer ratio

Sketch F § 6.1 allocates 12 named-bearer forms across the 37 v1 forms. Crossing this against the critical-fill list:

| Named-bearer anchor | Tier | Target form | Current substrate route | Critical-fill route |
|---|---|---|---|---|
| Arthur (Tier 1 explicit) | Tier 1 | Holy Knight/Paladin (cell 20) | COVERED via European substrate | Stage 1.5 named-bearer extraction; 24 hits |
| Roland (Tier 1 explicit) | Tier 1 | Polearm Soldier or Light Fighter | COVERED via European substrate | 6 hits |
| Hattori Hanzō (Tier 2 soft) | Tier 2 | Dagger Assassin (cell 6) | COVERED via East-Asian substrate; bearer-tagged 0 | Sidecar B Sengoku crawl |
| Lu Bu (Tier 2 soft) | Tier 2 | Polearm Soldier (cell 3) | COVERED cell; bearer-tagged 0 | Sidecar B Three-Kingdoms crawl |
| Thor (Tier 1 explicit) | Tier 1 | Heavy Barbarian (cell 1) hammer-form OR Polearm Soldier | mythological-register NULL-typed (40 bearer hits) | Stage 1.5 named-bearer join |
| Achilles (Tier 1 explicit) | Tier 1 | Light Fighter (cell 2) sword-form | mythological NULL-typed (10 bearer hits) | Stage 1.5 named-bearer join |
| Cú Chulainn (Tier 1 explicit) | Tier 1 | Thrown-Heavy (cell 4) Gáe Bolg | mythological NULL-typed (7 bearer hits) | Stage 1.5 named-bearer join |
| Karna (Tier 1 mythological) | Tier 1 | Archer (cell 7) Vijaya bow | mythological NULL-typed (12 bearer hits, some Mode-C) | Sidecar B Vedic crawl + Stage 1.5 |
| Baba Yaga (Tier 1 mythological) | Tier 1 | Witch Doctor Petmaster (cell 25) | **CRITICAL cell**; 12 bearer hits (6 cultural + 6 Mode-C UAV) | Sidecar B Slavic crawl + Stage 1.5 |
| Cleopatra (Tier 2) | Tier 2 | Polearm Soldier or new Egyptian cell | mythological NULL-typed (2 bearer hits) | Sidecar B Egyptian crawl |
| Moctezuma + Quetzalcoatl | Tier 2 nested Tier 1 | Witch Doctor Petmaster (cell 25) or new Aztec cell | **CRITICAL cell**; 0 bearer hits | Sidecar B Mesoamerican crawl + Stage 1.5 |
| Gilgamesh (Tier 1 mythological) | Tier 1 | Heavy Barbarian (cell 1) or new Sumerian cell | mythological NULL-typed; 0 bearer hits | Sidecar B Sumerian crawl + Stage 1.5 |

**Critical observation for Stage 3 design call:** 4 Sketch F anchors target CRITICAL cells (Baba Yaga / Moctezuma + Quetzalcoatl / both Witch Doctor cell; Gilgamesh / Heavy Barbarian or new cell). The named-bearer protection layer cannot be satisfied via current substrate; both Sidecar B + Stage 1.5 named-bearer join are load-bearing.

---

## 9. Cross-references

- HTML cross-tab: `cross-tab.html` § 2
- Thin-cell list: `thin-cell-list.md`
- Thin-tradition list: `thin-tradition-list.md`
- Sketch A 5-tuple cells: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 1.1
- Sketch B floors: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 2.1
- Sketch F named-bearer: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 6.1
- Stage 1.5 per-source-coverage: `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/per-source-coverage.md` § 4

---

## 10. Sign-off

**Author:** elrond (data steward)
**Authority:** Cycle 10 Wave 3 dispatch — Stage 2 critical-fill targets surfacing
**Status:** EXECUTION COMPLETE — feeds Stage 3 design call + Stage 3.5 engine-author scope + Sidecar B sequencing
**Tag intent:** `elrond/v0.0-cycle-10-stage-2-cross-tab` (combined)
