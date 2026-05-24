# Cycle 10 Stage 2 — Thin-Cell List

**Date:** 2026-05-24
**Owner:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-cross-tab-thin-cell-surfacing.md`
**Companion:** `cross-tab.html` (interactive visualization) · `critical-fill-targets.md` (per-form-archetype gap-fill scope) · `thin-tradition-list.md` (Sidecar B substrate-enrichment scope)

---

## 0. TL;DR

Per dispatch threshold definition:
- **CRITICAL** = substrate row-count < 10
- **THIN** = 10 ≤ row-count < 50

Result on the 25 Stage 0 cell-archetypes (Sketch A § 1.1):

| Status | Count | Cells |
|---|---:|---|
| CRITICAL | 9 | 13, 14, 15, 17, 19, 22, 23, 24, 25 |
| THIN | 1 | 21 |
| UNDER-FLOOR | 2 | 2, 9 |
| MODE-A-THIN | 1 | 9 (also counted above; mode-a < 10) |
| COVERED | 13 | 1, 3, 4, 5, 6, 7, 8, 10, 11, 12, 16, 18, 20 |

The CRITICAL set is concentrated in **INT/WIS-attribute deep-mechanic cells** (caster + summoner + channeler + monk + petmaster).

---

## 1. CRITICAL cells (row-count < 10)

### Cell 13 — Artillery Mage `(ranged, low, spiky, INT, none)`
- **Typed rows:** 3
- **High-conf rows:** 3
- **Mode-A clean rows:** 0
- **Sketch B floor:** 60-100 (ranged pure-attacker)
- **Stage 0 forms depending on this cell:** Artillery Mage (D3 Wizard Meteor; D2 Frozen Orb) — 2 forms
- **Why thin:** fingerprint v1.1 doesn't recognize spell-projectile language; the 3 typed rows are likely accidental matches.
- **Recommended action:** **Stage 3 design call decision.** Three routes: (a) accept that artillery-mage forms generate from `fantasy_generic` pool (substrate-led skew per Sketch D); (b) Sidecar B substrate-enrichment via targeted fantasy-coinage curation (PoE/Diablo spell items); (c) descope (fold into Standard Wizard cell 12). **Suggested: route (a)** — Standard Wizard cell (cell 12) carries 269 typed and is COVERED; Artillery Mage is a variant of caster identity that algorithmic mechanic-alteration (T4) can express.

### Cell 14 — Pyromantic Caster `(mid, low, spiky, INT, none)`
- **Typed rows:** 0
- **High-conf rows:** 0
- **Mode-A clean rows:** 0
- **Sketch B floor:** 60-100 (mid pure-attacker)
- **Stage 0 forms depending on this cell:** Pyromantic mid-range — 1 form (Sketch A note: D3 Crusader Phalanx mid-INT variant)
- **Why thin:** there are no historical/community-game weapons that satisfy `(mid, low, spiky, INT)` mechanical profile. The cell-archetype description ("pyromantic-mid-range") is a Pan-Fantasy generative slot, not a substrate-resident form.
- **Routing-ambiguous collapse:** shares substrate 3-tuple `mid|low|INT` with Cell 17 Necromancer Summoner (proxy=heavy). Both BOTH zero substrate.
- **Recommended action:** **Stage 3 design call decision.** This is a contested-cell per Sketch E § 5.1 ("contested cells IN at strawman counts; Pan-Fantasy bucket absorbs"). Suggested: confirm cell stays in v1 but flag as **engine-authored gap-fill territory** (Stage 3.5); substrate not expected to populate.

### Cell 15 — Red Mage / Spellsword `(melee, high, flat, INT, none)`
- **Typed rows:** 0
- **High-conf rows:** 0
- **Mode-A clean rows:** 0
- **Sketch B floor:** 80-120 (melee pure-attacker)
- **Stage 0 forms depending on this cell:** Red Mage/Spellsword (D2 Sorc+melee; FF Red Mage) — 1 form
- **Why thin:** mechanically defines as INT-melee, which is a cross-attribute hybrid; fingerprint v1.1 falls to STR-fallback on compound-suffix tokens. Per Stage 1 v1.1 § 3 finding (98% of compound-suffix rows fall to STR), the substrate's INT-melee population is mechanically invisible to fingerprint.
- **Recommended action:** **Stage 3 design call decision.** This is a contested-cell per Sketch E § 5.1. Suggested: (a) engine-author Stage 3.5 gap-fill OR (b) Phase 5 cohesion-judge composes Red Mage identity over a STR-melee substrate base (substrate weapon + INT-flavored kit composition).

### Cell 17 — Necromancer Summoner `(mid, low, spiky, INT, heavy)`
- **Typed rows:** 0
- **High-conf rows:** 0
- **Mode-A clean rows:** 0
- **Sketch B floor:** 30-50 (heavy proxy)
- **Stage 0 forms depending on this cell:** Necromancer Summoner (D2/D3/D4 Necro) — 2 forms
- **Why thin:** same as cell 14 (zero substrate at 3-tuple). Substrate has no canonical "necromancer wand" mechanical profile.
- **Routing-ambiguous collapse:** shares substrate 3-tuple `mid|low|INT` with Cell 14 Pyromantic Caster.
- **Recommended action:** **Stage 3 design call decision.** Necromancer is heavy-proxy (proxy-density discriminator), so floor is 30-50; can be satisfied via Stage 3.5 engine-author OR substrate-search for fantasy-coinage Necro-flavor staves/wands in WoW/PoE/D&D pools.

### Cell 19 — Channeling Cleric `(mid, medium, variable, WIS, none)`
- **Typed rows:** 3
- **High-conf rows:** 3
- **Mode-A clean rows:** 0
- **Sketch B floor:** 60-100 (mid pure-attacker)
- **Stage 0 forms depending on this cell:** Channeling Cleric (D3 Witch Doctor; Slime Rimuru) — 1 form
- **Why thin:** WIS-attribute is severely under-fingerprinted (only 391 WIS-typed rows substrate-wide). Most WIS-coded weapons are fingerprinted as INT or STR by v1.1.
- **Routing-ambiguous collapse:** shares substrate 3-tuple `mid|medium|WIS` with Cell 25 Witch Doctor Petmaster (proxy=heavy).
- **Recommended action:** **Stage 3 design call decision.** WIS-cell starvation is structural to the current fingerprint heuristic; a Stage 1.2 follow-on broadening WIS-attribute attribution would help. Suggested near-term: (a) Sidecar B substrate-enrichment OR (b) Stage 3.5 engine-author.

### Cell 22 — Storm Caller / Druid (active) `(ranged, medium, variable, WIS, none)`
- **Typed rows:** 2
- **High-conf rows:** 2
- **Mode-A clean rows:** 0
- **Sketch B floor:** 60-100 (ranged pure-attacker)
- **Stage 0 forms depending on this cell:** Storm Caller / Druid (D4 Druid; Aboriginal/Celtic wind-channeler) — 1 form
- **Why thin:** same WIS-starvation pattern.
- **Recommended action:** **Stage 3 design call decision.** Suggested: Sidecar B substrate-enrichment targeting Celtic/Druidic sources OR Stage 3.5 engine-author.

### Cell 23 — Monk-archetype `(melee, high, variable, WIS, none)`
- **Typed rows:** 0
- **High-conf rows:** 0
- **Mode-A clean rows:** 0
- **Sketch B floor:** 80-120 (melee pure-attacker)
- **Stage 0 forms depending on this cell:** Monk-archetype (D1 Hellfire Monk; D3 Monk Sunwuko; PoE2 Monk) — 2 forms
- **Why thin:** monks are typically unarmed-or-fistweapon — fingerprint v1.1 doesn't have monk-specific tokens. Fist-weapons / knuckle / quarterstaff would be substrate candidates.
- **Recommended action:** **Stage 3 design call decision.** Suggested: substrate-search via Sidecar B for fist/staff weapons in East Asian + South Asian + Celtic substrate; potential candidate is quarterstaff (might be already typed under STR melee).

### Cell 24 — Druid Beastmaster `(mid, low, variable, WIS, heavy)`
- **Typed rows:** 8
- **High-conf rows:** 8
- **Mode-A clean rows:** 5
- **Sketch B floor:** 30-50 (heavy proxy)
- **Stage 0 forms depending on this cell:** Druid Beastmaster (D2 Druid Spirit Wolves; LE Primalist Beastmaster-WIS) — 2 forms
- **Why thin:** WIS-starvation. The 8 typed rows + 5 Mode-A clean is barely under the 10 threshold; closest to "merely THIN."
- **Recommended action:** **Stage 3 design call decision.** Suggested: Sidecar B substrate-enrichment with Celtic/Druidic/Pacific cultural targets; very close to floor with mild effort.

### Cell 25 — Witch Doctor Petmaster `(mid, medium, variable, WIS, heavy)`
- **Typed rows:** 3
- **High-conf rows:** 3
- **Mode-A clean rows:** 0
- **Sketch B floor:** 30-50 (heavy proxy)
- **Stage 0 forms depending on this cell:** Witch Doctor Petmaster (D3 WD Carnevil; D2 Necro Spirit-summon) — 1 form
- **Routing-ambiguous collapse:** shares substrate 3-tuple `mid|medium|WIS` with Cell 19 Channeling Cleric.
- **Recommended action:** **Stage 3 design call decision.** Suggested: Stage 3.5 engine-author for fetish-style throwing weapons + ritual staves; substrate Sub-Saharan-African enrichment via Sidecar B.

---

## 2. THIN cells (10 ≤ row-count < 50)

### Cell 21 — Ritual Mage / Oracle `(ranged, low, spiky, WIS, none)`
- **Typed rows:** 51
- **High-conf rows:** 49
- **Mode-A clean rows:** 6
- **Sketch B floor:** 60-100 (ranged pure-attacker)
- **Stage 0 forms depending on this cell:** Ritual Mage / Oracle — 1 form
- **Why thin:** narrowly above the THIN-vs-CRITICAL boundary; below Sketch B floor (60-100).
- **Recommended action:** **Stage 3 design call decision.** Suggested: Sidecar B substrate-enrichment targeting ritual/oracle vocabulary across cultures; or accept low floor (single form, low cell-pressure).

---

## 3. UNDER-FLOOR cells (≥ 50 rows, below Sketch B floor)

### Cell 2 — Light Fighter `(melee, high, flat, STR, none)` — UNDER-FLOOR-HIGHCONF
- **Typed rows:** 476
- **High-conf rows:** 3 (severe drop)
- **Mode-A clean rows:** 341
- **Sketch B floor:** 80-120 (melee pure-attacker)
- **Anomaly:** typed >> floor, but high-conf only 3 — this means 473 of the 476 rows are at v1.1 low-spec (0.45 confidence). Per Stage 1 v1.1 § 5 finding: most are bare-plural compound-suffix matches ("Blades", "Swords") which read as melee/cleave/STR; v1.1 keeps these at 0.45.
- **Stage 0 forms depending on this cell:** Light Fighter (D3 Crusader Sweep; PoE Slayer) — 2 forms
- **Recommended action:** **Stage 3 design call decision.** Suggested: composition policy can include the 0.45-confidence pool (v1_scope sampling treats 0.45 as good-enough for COVERED cells), but flag this cell as Stage 4 mechanical-tagging priority. Mode-A clean is healthy (341).

### Cell 9 — Twin-Blade Fencer `(mid, high, flat, DEX, none)` — MODE-A-THIN
- **Typed rows:** 215
- **High-conf rows:** 213
- **Mode-A clean rows:** 5
- **Sketch B floor:** 60-100 (mid pure-attacker)
- **Anomaly:** typed and high-conf both healthy; Mode-A clean is only 5. Substrate is community-game-data dominated (fantasy-coinage twin-blade items in WoW/PoE). Authentic historical/cultural-tradition twin-blade weapons (e.g., paired-sword Filipino arnis, Indian katar, Arabian shamshir-pair) are not strongly attested.
- **Stage 0 forms depending on this cell:** Twin-Blade Fencer (D2 Bowazon-Strafe variant; KonoSuba) — 1 form
- **Recommended action:** **Stage 3 design call decision.** If Twin-Blade Fencer is intended as Pan-Fantasy form per Sketch D § 5.3, current substrate is fine. If authentic-cultural-tradition representation is desired, Sidecar B Filipino-arnis / Indian-katar substrate-enrichment.

---

## 4. Per-cell action summary (Stage 3 design call input)

| Cell | Archetype | Status | Recommended action |
|---|---|---|---|
| 13 | Artillery Mage | CRITICAL | Fold into Standard Wizard (cell 12) via T4 algorithmic mechanic-alteration; substrate stays at 12 |
| 14 | Pyromantic Caster | CRITICAL | Stage 3.5 engine-author OR Sidecar B fantasy-coinage curation; contested cell per Sketch E |
| 15 | Red Mage/Spellsword | CRITICAL | Stage 3.5 engine-author OR Phase 5 cohesion-judge composes over STR-melee substrate base |
| 17 | Necromancer Summoner | CRITICAL | Sidecar B fantasy-coinage Necro-flavor staves/wands OR Stage 3.5 |
| 19 | Channeling Cleric | CRITICAL | Sidecar B WIS-enrichment OR Stage 3.5; consider Stage 1.2 follow-on broadening WIS fingerprint |
| 21 | Ritual Mage/Oracle | THIN | Sidecar B oracle/ritual vocabulary OR accept low floor |
| 22 | Storm Caller/Druid | CRITICAL | Sidecar B Celtic/Druidic substrate-enrichment OR Stage 3.5 |
| 23 | Monk-archetype | CRITICAL | Sidecar B East-Asian/South-Asian fist-and-staff weapons OR Stage 3.5 |
| 24 | Druid Beastmaster | CRITICAL | Sidecar B Celtic/Pacific substrate-enrichment (closest to floor) |
| 25 | Witch Doctor Petmaster | CRITICAL | Sidecar B Sub-Saharan-African substrate-enrichment OR Stage 3.5 |
| 2 | Light Fighter | UNDER-FLOOR-HIGHCONF | Include 0.45-conf pool; flag for Stage 4 mechanical-tagging priority |
| 9 | Twin-Blade Fencer | MODE-A-THIN | Pan-Fantasy acceptable OR Sidecar B Filipino-arnis/Indian-katar enrichment |

---

## 5. Cross-references

- HTML cross-tab: `cross-tab.html`
- Per-form-archetype gap-fill scope: `critical-fill-targets.md`
- Sidecar B substrate-enrichment scope: `thin-tradition-list.md`
- Stage 0 cell definitions: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 1.1
- Sketch B floors: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 2.1
- Stage 1 v1.1 fingerprint context: `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/confidence-distribution-v1-1.md`
- Stage 1.5 named-bearer context: `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/per-source-coverage.md`

---

## 6. Sign-off

**Author:** elrond (data steward)
**Authority:** Cycle 10 Wave 3 dispatch — Stage 2 cross-tab + thin-cell surfacing
**Status:** EXECUTION COMPLETE — feeds Stage 3 design call
**Tag intent:** `elrond/v0.0-cycle-10-stage-2-cross-tab` (combined with HTML + sibling MDs)
