# Cycle 10 Wave 5.5 — Closeout Report (elrond)

**Date:** 2026-05-25
**Wave:** 5.5 (add-on per gandalf SO-4 amendment + sign-off Conditions 1 + 3)
**Owner:** elrond (substrate seam; classifier extension + SQL eviction)
**Co-owner pending:** gandalf (small-batch post-eviction audit ~10 rows)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-wave-5-5-phase-0c-and-mode-c-eviction.md`
**Authority basis:**
- gandalf 50-row Phase 2 spot-check FAIL (29/50 = 58%) per `2026-05-25-phase-2-50-row-spot-check.md`
- gandalf SO-4 RATIFY-WITH-AMENDMENT per `2026-05-25-so-1-2-4-sign-off-verdicts.md`
- gandalf Phase 3 distribution report sign-off § 3 Conditions 1 + 3 per `2026-05-25-stage-3-distribution-report-sign-off.md`

---

## 0. TL;DR

**Phase 0c (Tier-A NULL-subtype classifier extension):** classified 7,943 Tier-A NULL-subtype rows via per-source heuristic rules. Of these, 1,431 were in v1_scope=1; 761 of those (53%) classified to D1c-excluded subtypes and got v1_scope→0 with `wave_5_5_downgrade.rule = 'd1c_excluded_scope_deferred_tier_a_post_phase_0c'`.

**Part B (Mode-C-by-semantics SQL eviction):** ran gandalf sign-off § 3 Condition 3 SQL signature VERBATIM. Identified 30 eviction candidates (well below the dispatch ~50-100 estimate — see § 3 explanation; Phase 0c front-ran most of the Mode-C-by-period overlap). All 30 evicted with `wave_5_5_mode_c_eviction.rule = 'mode_c_by_semantics_evicted_wave_5_5'`.

**v1_scope total:** 3,042 → 2,251 (net reduction 791 = 761 Phase 0c downgrade + 30 Mode-C eviction). Just below the ~2,900-2,990 floor named in dispatch § 5.5 acceptance-criterion 5, but the dispatch range estimated only ~50-150 reduction; empirical is materially higher because Tier-A NULL-subtype scope-creep was substantially worse than estimated (the gandalf spot-check sampled 10 hist-european Tier-A rows and 8/10 were D1c-equivalent — 80% scope-creep rate; the classifier confirmed 53% across the full 1,431-row Tier-A v1_scope pool).

**Per-axis distribution post-Wave-5.5:** historical 52.5% (was 57.5%, now centered in 50-55% band — IMPROVED); fantasy 45.2% (was 33.8%, now over 30-35% upper bound — composition consequence of historical eviction); military_modern 1.4% (was 8.0%, now well below 5-8% band — consequence of odin-army-tradoc UAVs/missiles/naval-craft routing to siege_vehicle); mythological 0.9% (was 0.7%, ~unchanged; Stage 4 rescue still needed per Phase 3 report).

**Compositional implication:** Wave 5.5 successfully evicted contamination but the v1_scope size + register-share profile both shifted materially. The shift may trigger Phase 2 micro-sample re-fire (knight-rider's call per dispatch § 4.4 + § 6) and/or composition policy v1.1+ revisit. See § 5 + § 6 below.

**Pre-eviction list + 10-row gandalf audit sample saved** for knight-rider routing post-this-session.

---

## 1. Part A — Phase 0c Tier-A NULL-subtype classifier extension

### 1.1 Method

Extended the Phase 0a Tier-S classifier pattern (`cycle-10-stage-3-2026-05-25/accessory-armor-subcategory-classification.md`) to the Tier-A NULL-subtype pool. Per-source heuristic rules — same load-bearing principle as Phase 0a (keyed on source-side structured signal at higher fidelity than canonical_name token-matching):

| Source | Primary signal | Token override |
|---|---|---|
| **met-museum** | `structured_properties.classification` (e.g., "Helmets", "Shafted Weapons", "Krisses", "Firearms-Pistols-Wheellock") — same field Phase 0a used | name-token fallback for unclassified rows |
| **royal_armouries** | `structured_properties.object_type[0]` (e.g., "Armour", "Swords", "Firearms & Equipment", "Animal armour and Equestrian Equipment") + `category_type` ("Firearms & Artillery", "Edged Weapons", "Armour") | name-token override list for shield/helmet/cuisse/scabbard/magazine/bayonet/saddle/etc. (38 tokens) |
| **odin-army-tradoc** | `structured_properties.properties."System.Type"` (UAV, Anti-Tank Guided Missile, etc.) — virtually all rows are heavy military hardware | handheld weapon tokens (sniper rifle, assault rifle, etc.); heavy tokens (machine gun, ATGM, mortar); ammo tokens (missile, mine, rocket) |
| **wikipedia** | `structured_properties.type` (HTML-comment debris normalized) — military-modern weapon types | name-token fallback |
| wow-classic-items / dnd / pf2ools / wikidata | name-token fallback only | — |

Heuristic only; no LLM cost; classifier code at `classify_tier_a_subtype.py`; execution log at `phase-0c-classify-log.out`.

### 1.2 Classifier output — per-subtype counts (full 7,943 Tier-A NULL-subtype pool)

| Subtype | Count | D1 status |
|---|---:|:---:|
| `handheld_weapon` | 3,085 | D1a allowed |
| `siege_vehicle` | 2,086 | D1c excluded |
| `ammo_consumable` | 743 | D1c excluded |
| `armor_body_or_head` | 702 | D1c excluded |
| `other` | 517 | D1c excluded |
| `accessory_weapon_integrated` | 328 | D1b allowed |
| `accessory_horse_or_equipment` | 180 | D1c excluded |
| `art_object` | 155 | D1c excluded |
| `armor_shield` | 126 | D1b allowed |
| `accessory_handheld` | 21 | D1b allowed |
| **Total** | **7,943** | |

**D1a-allowed pool (Tier-A handheld_weapon):** 3,085 rows — substantial pool, including 2,513 from royal_armouries (mostly historical European edged weapons, firearms, polearms) + 365 from met-museum (similar historical breadth).
**D1b-allowed pool:** 21 + 328 + 126 = 475 rows.
**D1c-excluded pool:** 743 + 702 + 517 + 180 + 155 + 2,086 = 4,383 rows.

### 1.3 Per-source × subtype cross

| Source | Total | handheld | siege | ammo | arm_body | other | acc_wep_int | acc_horse | art | arm_shld | acc_hh |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| met-museum | 642 | 365 | 0 | 4 | 66 | 62 | 14 | 52 | 38 | 20 | 21 |
| royal_armouries | 4,531 | 2,513 | 119 | 290 | 629 | 318 | 312 | 128 | 117 | 105 | 0 |
| odin-army-tradoc | 2,258 | 36 | 1,814 | 408 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wikipedia | 495 | 166 | 153 | 40 | 7 | 126 | 2 | 0 | 0 | 1 | 0 |
| wow-classic-items | 9 | 1 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| nick-aschenbach-dnd-data | 5 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| wikidata | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf2ools | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

**Observation:** odin-army-tradoc dominates the siege_vehicle bucket (1,814 of 2,086) and the ammo_consumable bucket (408 of 743). This source is overwhelmingly modern-military hardware and its Tier-A admission via the Sub-phase A preferred-include rule was the dominant driver of military_modern over-representation in pre-Wave-5.5 v1_scope.

### 1.4 v1_scope downgrade applied — per-subtype

For Tier-A v1_scope=1 rows that classified to D1c-excluded subtypes:

| Subtype | Downgrade count |
|---|---:|
| `armor_body_or_head` | 242 |
| `siege_vehicle` | 197 |
| `other` | 120 |
| `accessory_horse_or_equipment` | 78 |
| `ammo_consumable` | 70 |
| `art_object` | 54 |
| **Total** | **761** |

Each row updated with: `v1_scope = 0` + `v1_scope_composition_trace.wave_5_5_downgrade.rule = 'd1c_excluded_scope_deferred_tier_a_post_phase_0c'` (original trace.rule preserved; new field added for full provenance).

### 1.5 Verification — spot-check FAIL exemplars confirmed downgraded

Per gandalf 50-row spot-check § 1 + § Diagnosis 1 exemplars:

| Spot-check FAIL exemplar | Classified subtype | v1_scope post-Wave-5.5 |
|---|---|:---:|
| helmet rows (n=4 sampled) | armor_body_or_head | 0 (downgraded) |
| sallet | armor_body_or_head | 0 (downgraded) |
| cuisses | armor_body_or_head | 0 (downgraded) |
| riding boot | accessory_horse_or_equipment | 0 (downgraded) |
| Bevor (chin defense) | armor_body_or_head | 0 (downgraded) |
| Shaffron | accessory_horse_or_equipment | 0 (downgraded) |
| Composite armour | armor_body_or_head | 0 (downgraded) |
| Gun Carriage Wheels | siege_vehicle | 0 (downgraded) |
| Buff coat | armor_body_or_head | 0 (downgraded) |
| KOLIBRI 13-O UAV | siege_vehicle | 0 (downgraded) |
| Magazine (the standalone item, id=197771) | accessory_weapon_integrated | 1 (retained as D1b) |

### 1.6 Heuristic-edge observations (gandalf review candidates)

The classifier is heuristic-only and surfaces three edge-case patterns:

1. **Met-museum "Miscellaneous" classification** (62 met-museum rows routed to `other`): the museum's catch-all bucket contains a mix of weapons + non-weapons. The classifier defaults to OTHER (D1c-excluded) as the safe choice. False-negatives are possible — e.g., "Pair of Tiger's Claws (Bagh Nakh)" (id 203930) is a hand-claw weapon classified `Miscellaneous` by met-museum; the classifier routed to OTHER (D1c-excluded). Loss to v1_scope: small (estimate ~3-5 rows of bona-fide handheld weapons mis-routed via met:Miscellaneous). Gandalf review can re-promote specific rows in a follow-on.

2. **Royal-armouries "magazine" name-token override** (62 royal_armouries rows with "magazine" in name routed to `accessory_weapon_integrated`): the override correctly catches standalone magazines (e.g., "Magazine", id=197771) but also fires on rifle/shotgun model names that contain the word "magazine" as a descriptor (e.g., "Centrefire bolt-action magazine rifle"). These rifle rows are mis-labeled as accessory_weapon_integrated rather than handheld_weapon. The mis-label is **semantically wrong but operationally inert** — `accessory_weapon_integrated` is D1b-allowed so the row stays in v1_scope (correct v1_scope outcome); only the subtype label is wrong. Loss to v1_scope: zero.

3. **Wikipedia type-field HTML debris**: many wikipedia rows have HTML-comment fragments in the type field ("Revolver\n<!-- Type selection -->"). Normalizer strips these; classification proceeds correctly. No known false-negatives.

These edges are documented in the per-row JSON trace (`phase-0c-tier-a-subtype-classification.json` — see `rationale` field per row) for gandalf review.

---

## 2. Part B — Mode-C-by-semantics SQL eviction

### 2.1 SQL signature (verbatim per gandalf sign-off § 3 Condition 3)

```sql
SELECT id, canonical_name, register_canonical, historical_period_canonical,
       cultural_lineage_canonical, named_mythological_match
FROM weapon_knowledge_entries
WHERE v1_scope = 1
  AND named_mythological_match IS NOT NULL
  AND (
    historical_period_canonical IN ('contemporary', 'modern', 'industrial')
    OR canonical_name LIKE '%UAV%' OR canonical_name LIKE '%missile%'
    OR canonical_name LIKE '%helicopter%' OR canonical_name LIKE '%submarine%'
    OR canonical_name LIKE '%aircraft%' OR canonical_name LIKE 'F-%'
    OR canonical_name LIKE '%MK-%' OR canonical_name LIKE 'AIM-%'
    OR canonical_name LIKE 'AGM-%' OR canonical_name LIKE 'SUB-%'
    OR canonical_name LIKE '%Type %'
    OR canonical_name LIKE '%Particle %' OR canonical_name LIKE '%Plasma %'
    OR canonical_name LIKE '%Quantum %' OR canonical_name LIKE '%Laser %'
  );
```

### 2.2 Eviction count and breakdown

**30 rows evicted.** Dispatch § 2 estimate was ~50-100; empirical 30 is below the lower bound. Explanation in § 3.

| Per-period | n | Per-tier | n | Per-cultural-lineage | n |
|---|---:|---|---:|---|---:|
| contemporary | 14 | S | 30 | european | 16 |
| industrial | 7 | A | 0 | east_asian | 7 |
| modern | 7 | B | 0 | unknown | 5 |
| unknown | 2 | C | 0 | southeast_asian | 1 |
| | | | | south_asian | 1 |

**All 30 evicted are Tier-S** — consistent with the Mode-C SQL signature's targeting of `named_mythological_match IS NOT NULL`, which is concentrated at Tier-S (the Phase 1 mythological-NULL pipeline + Tier-S quality bar produce this concentration).

### 2.3 Gandalf 10-row audit sample (pre-staged at `gandalf-eviction-audit-sample.json`)

Random sample (seed=20260525) of 10 evicted rows for gandalf small-batch audit:

| id | canonical_name | period | named_mythological_match |
|---:|---|---|---|
| 107 | Mace-AO 2152 | contemporary | Ninurta (mesopotamian, tier_1) |
| 46 | Shield Depicting Saint George Slaying the Dragon | industrial | Saint George (european_medieval, tier_2) |
| 175669 | Claíomh Solais | modern | Lugh (celtic, tier_1) |
| 181777 | ČZ 2000 | contemporary | Lada (slavic, tier_1) |
| 208183 | Sword blade (katana) | industrial | Sadamune (east_asian, tier_2) |
| 189505 | Type 73 light machine gun | unknown | Isis (egyptian, tier_1) |
| 215455 | Flintlock muzzle-loading musket | industrial | Suvorov (slavic, tier_2) |
| 190567 | H-S Precision Pro Series 2000 HTR | contemporary | Horus (egyptian, tier_1) |
| 187044 | .475 Nitro Express | modern | Wayland the Smith (european_medieval, tier_1) |
| 202673 | Belt | contemporary | Robin Hood (european_medieval, tier_1) |

**Self-audit assessment** (substrate-led, advisory; gandalf has final call):
- 9 of 10 are clear Mode-C-by-semantics contamination (modern-period weapons or contemporary military hardware wearing mythological name-tags — the precise pattern the marginal-lineage Mode-C framework names)
- Saint George shield (id=46) is industrial-period and wears a medieval saint's name; correctly evicted (note: a separate early_modern Saint George shield id=180526 retained — that one is period-appropriate)
- 1 borderline (Claíomh Solais id=175669, period=modern): this is the Sword of Light of Lugh — the canonical Lugh weapon. The substrate tags it `modern` period which triggered Mode-C eviction. If the legitimate mythological weapon should be retained but mis-tagged at the period level, the right fix is period-tag remediation (not Mode-C eviction). Routed for gandalf judgment — Mode-C eviction caught real contamination but may have over-evicted in this borderline case.

### 2.4 Verification (Discipline #11)

- Post-eviction smoke assertion: `SELECT COUNT(*) WHERE v1_scope=1 AND v1_scope_composition_trace LIKE '%mode_c_by_semantics_evicted_wave_5_5%'` returns 0 — PASS (evicted rows do NOT remain in v1_scope)
- All 30 evicted rows carry the trace marker — PASS
- Mode-C SQL signature applied VERBATIM — no modifications

### 2.5 Why only 30 evictions vs ~50-100 estimate?

Three reasons:

1. **Phase 0c front-ran significant Mode-C-by-period contamination.** Many Tier-A rows that would have matched the Mode-C SQL signature (modern-period + named_mythological_match) got their v1_scope set to 0 in Phase 0c first because they ALSO classified to D1c-excluded subtypes. Examples: contemporary UAVs / missiles classified as siege_vehicle/ammo via odin-army-tradoc System.Type ran through Phase 0c before Mode-C SQL saw them. The two passes overlap in coverage but Mode-C SQL fired second so it saw a smaller residual pool.

2. **The Mode-C SQL signature requires `named_mythological_match IS NOT NULL`.** The substrate's named-mythological-match column was populated only via Stage 1.5 + Stage 2.5 mythological-NULL pipeline, which is concentrated at Tier-S quality. Most modern-period contamination at Tier-A is `named_mythological_match=NULL` (e.g., AIM-68 Big Q has `named_mythological_match=''` not a Quetzalcoatl bearer tag). These rows are caught by Phase 0c but NOT by Mode-C SQL.

3. **The dispatch's ~50-100 estimate was informed by a substrate audit performed before Phase 0c was scoped.** With Phase 0c handling the bulk of the modern-military contamination, Mode-C SQL is left to clean only the residual: modern-period rows that survived Phase 0c (because they classified to a D1a/D1b subtype like handheld_weapon) but still carry a mythological-bearer tag (the Saint George shield, the Claíomh Solais, etc.). 30 is the empirical count.

---

## 3. Combined Wave 5.5 effect on v1_scope

### 3.1 Reduction summary

| Step | Reduction | v1_scope after |
|---|---:|---:|
| Pre-Wave-5.5 (Phase 3 baseline) | — | 3,042 |
| Phase 0c Tier-A D1c-downgrade | -761 | 2,281 |
| Part B Mode-C-by-semantics eviction | -30 | **2,251** |

**Net reduction: 791 rows (-26%).**

### 3.2 Per-tier distribution

| Tier | Pre-Wave-5.5 | Post-Wave-5.5 | Δ |
|---|---:|---:|---:|
| S | 532 | 502 | -30 |
| A | 1,431 | 670 | -761 |
| B | 1,056 | 1,056 | 0 |
| C | 23 | 23 | 0 |
| **Total** | **3,042** | **2,251** | **-791** |

Tier-A is the dominant change locus, exactly per the spot-check FAIL diagnosis. Tier-S contribution to the reduction is the 30 Mode-C-evicted rows.

### 3.3 Per-register distribution (vs composition policy § 2.1 ±5pp targets)

| Register | Pre share | Post share | Pre count | Post count | Target band | Post verdict |
|---|---:|---:|---:|---:|---|:---:|
| historical | 57.5% | 52.5% | 1,749 | 1,181 | 50-55% | **WITHIN ±5pp** (was at +5.0pp edge; now centered) |
| fantasy | 33.8% | 45.2% | 1,028 | 1,017 | 30-35% | **OUT** — +10.2pp over upper bound 35% (composition-shift consequence of historical eviction) |
| military_modern | 8.0% | 1.4% | 243 | 32 | 5-8% | **OUT** — -3.6pp below lower bound 5% (odin-army-tradoc UAVs routed siege; D1c excluded) |
| mythological | 0.7% | 0.9% | 22 | 21 | 1.5% (with Stage 4 rescue) | UNCHANGED — Stage 4 rescue still needed |

**Headline:** historical improved (now within target band); military_modern dropped well below band; fantasy share rose above band as a composition consequence (the same absolute count is now a larger fraction of the smaller total).

### 3.4 Per-cultural-tradition distribution (vs composition policy § 2.2 form-share targets)

| Cultural lineage | Pre share | Post share | Pre count | Post count | Target band | Post verdict |
|---|---:|---:|---:|---:|---|:---:|
| european | 49.5% | 40.4% | 1,505 | 910 | 30-35% | OUT — +5.4pp over upper bound 35% (improved from +14.5pp pre) |
| fantasy_generic | 33.6% | 44.9% | 1,021 | 1,010 | 15-18% | OUT — +26.9pp over upper bound 18% (worsened by composition shift) |
| east_asian | 10.6% | 9.0% | 323 | 203 | 15-20% | OUT — -6.0pp under lower bound 15% (was -4.4pp pre; worsened) |
| south_asian | 2.6% | 2.4% | 78 | 55 | 3-4% | OUT — -0.6pp under lower bound (borderline) |
| middle_eastern | 1.4% | 1.2% | 44 | 26 | not in policy | — |
| southeast_asian | 0.9% | 1.0% | 28 | 23 | not in policy | — |
| mesoamerican | 0.3% | 0.04% | 8 | 1 | 3-5% via Sidecar B | OUT — Sidecar B priority signal |
| african | 0.2% | 0.1% | 7 | 2 | Sidecar B target | OUT — Sidecar B priority signal |
| unknown | 0.8% | 0.9% | 25 | 20 | — | sentinel |

**Headline:** european improved (49.5% → 40.4%; closer to band but still +5.4pp over) but fantasy_generic worsened proportionally (33.6% → 44.9%; +26.9pp over). East_asian dropped 10.6% → 9.0% — the eviction took out some east_asian rows but also reduced the historical-european denominator more, paradoxically pushing east_asian's percentage down further. Mesoamerican + african thin-tradition counts dropped further — Sidecar B + Stage 3.5 enrichment are now MORE urgent post-Wave-5.5.

### 3.5 Per-period distribution

| Period | Post count | Share |
|---|---:|---:|
| fictional | 922 | 41.0% |
| early_modern | 499 | 22.2% |
| industrial | 371 | 16.5% |
| modern | 140 | 6.2% |
| classical | 114 | 5.1% |
| unknown | 77 | 3.4% |
| contemporary | 75 | 3.3% |
| medieval | 53 | 2.4% |

Contemporary/modern/industrial total: 586 (26.0%) — these are non-mythological non-named-bearer instances that survive both Phase 0c and Mode-C SQL because they classify to D1a/D1b subtypes (handheld firearms, swords) and lack mythological name-match.

### 3.6 Per-axis distribution (proxy fingerprint)

| Geometry | Count | | Range | Count | | Tempo | Count | | Attribute | Count |
|---|---:|---|---|---:|---|---|---:|---|---|---:|
| single | 1,003 | | melee | 809 | | medium | 902 | | DEX | 849 |
| cleave | 544 | | ranged | 586 | | low | 454 | | STR | 649 |
| NULL | 442 | | NULL | 442 | | NULL | 442 | | NULL | 442 |
| AoE | 152 | | mid | 390 | | high | 429 | | WIS | 146 |
| multi-hit | 50 | | melee_close_or_grapple | 17 | | reactive_block_tempo | 17 | | INT | 141 |
| scatter | 33 | | off_hand_aura | 7 | | aura_pulse_tempo | 7 | | STR_or_DEX | 17 |
| shield_blocker | 17 | | | | | | | | STR_or_WIS | 7 |
| banner_rally_aura | 7 | | | | | | | | | |
| cone | 3 | | | | | | | | | |

NULL-axis count is 442 (19.6% of v1_scope post-Wave-5.5). Pre-Wave-5.5 was 1,152 NULL-typed of 3,042 (37.9%). Wave 5.5 evicted 710 NULL-typed rows (most via Phase 0c D1c downgrade — body armor / horse equipment / siege vehicles are NULL-typed because the proxy fingerprint is weapon-shaped). The typed-rate of v1_scope rose from 62.1% → 80.4% — a substantial improvement for downstream Stage 4 + Phase 2 form-generation.

### 3.7 Per-subtype distribution (post-Phase-0c population in v1_scope)

| Subtype | Count | Share |
|---|---:|---:|
| NULL (Tier-B/C unpopulated) | 1,079 | 47.9% |
| handheld_weapon | 961 | 42.7% |
| accessory_weapon_integrated | 164 | 7.3% |
| armor_shield | 34 | 1.5% |
| accessory_handheld | 13 | 0.6% |

The remaining NULL subtype rows are all Tier-B (1,056) + Tier-C (23) — Phase 0c only ran on Tier-A. Tier-B / Tier-C subtype population is a future-stage decision (Stage 4 mechanical-tagging surfaces NULL-typed Tier-B as enrichment candidates per gandalf SO-4 amendment context).

---

## 4. Acceptance criteria coverage (per dispatch § 5.5)

- [x] **1. Phase 0c classifier executed on Tier-A NULL-subtype rows; subtype counts documented.** Note: scope was 7,943 (broader than dispatch's "940" — see § 1.1; 940 was the gandalf-spot-check count of Tier-A v1_scope=1 NULL-typed-proxy rows, not NULL-subtype rows; this script operated on the dispatch SQL signature `quality_tier='A' AND weapon_kind_classified_subtype IS NULL`)
- [x] **2. Per-subtype v1_scope eligibility recheck applied (D1c-excluded subtypes downgraded).** 761 rows downgraded.
- [x] **3. Mode-C SQL eviction executed per gandalf sign-off § 3 Condition 3 signature.** VERBATIM SQL; 30 rows evicted.
- [x] **4. Actual eviction count documented vs ~50-100 estimate.** 30 rows (below estimate); explained in § 2.5.
- [x] **5. Updated v1_scope count + per-tier + per-axis distribution documented (verify still within ±5pp composition policy § 2 targets).** Documented in § 3; historical now within ±5pp (improved); military_modern + fantasy_generic now out of tolerance (worsened — composition consequence of eviction; see § 5).
- [x] **6. Wave 5.5 closeout report + per-phase outputs at named paths.** This document + companion JSONs.
- [x] **7. Pre-Wave-5.5 DB backup at named path (gitignored).** `backups/telemetry.db.pre-wave-5-5` (213 MB; `.gitignore` in dir).
- [x] **8. MIGRATION.md drafted (updates-only pattern).** `MIGRATION.md` at deliverable path.
- [x] **9. Round-trip: not applicable — substrate-only updates; no cross-seam contract change per Principle 6.**
- [ ] **10. AGENT_STATE.md updated at session end** — elrond seam AGENT_STATE not currently maintained.
- [ ] **11. Tag: `elrond/cycle-10-wave-5-5-phase-0c-and-mode-c-eviction-2026-05-25`** — to be cut after closeout commit lands.
- [ ] **12. Auto-commit + auto-push** — pending session-end commit.
- [x] **13. Pre-eviction list + 10-row gandalf audit sample saved.** `eviction-candidates-pre.json` + `gandalf-eviction-audit-sample.json`.

---

## 5. Composition shifts triggered by Wave 5.5 — observations for routing

Wave 5.5 successfully removed contamination but the post-Wave-5.5 v1_scope has materially shifted register-share + cultural-tradition profile. These shifts are observations, not recommendations — knight-rider + gandalf + Matt decide routing per dispatch § 6 + gandalf sign-off § 4.

### 5.1 Military_modern under-represented (1.4% vs 5-8% target)

The 211-row reduction in military_modern is driven by odin-army-tradoc UAVs / missiles / naval craft routing to `siege_vehicle` (D1c-excluded). The retained 32 military_modern rows include `handheld_weapon`-classified items (sniper rifles, machine pistols, etc.) that are genre-bridgeable to fantasy-isekai modern-military fantasy archetypes.

**Routing surface for knight-rider:**
- Option A: accept the substrate-led reduction — military_modern in the v1_scope is now smaller and "cleaner" (genuine handheld military hardware; no vehicles)
- Option B: fire Phase 2 micro-sample to re-fill military_modern budget from the Tier-A pool with `weapon_kind_classified_subtype IN ('handheld_weapon', 'armor_shield', 'accessory_weapon_integrated')` filter applied
- Option C: composition policy v1.1+ revision to lower the military_modern target band (acknowledge that "military_modern in form-library" is genuinely smaller than substrate suggests when D1c-excluded items are removed)

### 5.2 Fantasy share over upper bound (45.2% vs 30-35% target)

Composition consequence: same fantasy count (1,028 → 1,017, -11 rows) over smaller total (3,042 → 2,251) increases percent share. Fantasy didn't grow; historical and military_modern shrunk.

**Routing surface for knight-rider:**
- Option A: accept — the form-library will be more fantasy-skewed at v1 (matches the "HEFTY per Matt" composition policy § 2.2 explicit fantasy_generic over-weighting)
- Option B: re-balance — fire Phase 2 micro-sample to add Tier-A historical rows (now that the D1c-contamination is gated out, the Tier-A handheld_weapon pool is 3,085 - ~670 currently-in-scope = ~2,400 candidate rows available for additional sampling)

### 5.3 Thin-tradition coverage decreased (mesoamerican 0.04%, african 0.1%)

The few Tier-A mesoamerican/african rows in v1_scope pre-Wave-5.5 may have included D1c-equivalent items that got evicted (e.g., Aztec horse-trappings, African ceremonial banners) — meaningfully reducing already-thin cultural-tradition coverage.

**Routing surface for knight-rider:** Sidecar B + Stage 3.5 enrichment is now more urgent — pre-Wave-5.5 the gap was -2.7pp / -Sidecar-B-target; post-Wave-5.5 the gap is wider. Stage 3.5 (Moctezuma + Mesoamerican anchors) + Sidecar B (thin-tradition substrate enrichment) become higher-priority Cycle 10 wave work.

### 5.4 Tier-A under-coverage now possible

Tier-A in v1_scope dropped 1,431 → 670 (-53%). The pre-Wave-5.5 composition policy assumed Tier-A would contribute ~25-30% of v1_scope (1,431 / 3,042 = 47% actual pre; 670 / 2,251 = 29.8% post). The post-Wave-5.5 Tier-A share is closer to the composition policy intent.

**Routing surface for knight-rider:** if the policy intent was tighter Tier-A share, no further action needed. If the intent was richer Tier-A coverage to surface marginal weapon-types (less-canonical regional weapons), Phase 2 micro-sample with `weapon_kind_classified_subtype IN ('handheld_weapon', ...)` filter from the now-cleaner Tier-A pool would lift Tier-A back toward 1,000+.

---

## 6. Open routing surfaces (forwarded to knight-rider)

Per dispatch § 4.4 + gandalf sign-off § 4 recommendation:

| Question | Routing target | Substantive content |
|---|---|---|
| Whether to fire Phase 2 micro-sample to re-fill freed budget | knight-rider authoring per dispatch § 4.4 + gandalf Path-2 (cleanest unblock; conditional on Matt + gandalf priority for v1_scope volume) | If yes: D1c-filtered Tier-A pool is ~2,400 rows available; target lift of ~500-700 rows would bring v1_scope back to ~2,800-2,950 range (~within the original ~1,700-3,100 envelope and aligned with composition policy § 2 historical 50-55% / fantasy 30-35% targets) |
| Gandalf 10-row eviction sample audit | knight-rider routes to gandalf | Path: `gandalf-eviction-audit-sample.json`; smoke threshold ≥ 8/10 per dispatch § 8 |
| Gandalf re-run 50-row spot-check on cleaned v1_scope | knight-rider routes to gandalf | Path: `post-wave-5-5-spot-sample-50.json`; stratification mirrors pre-Wave-5.5 50-row spot-check for direct comparability with 29/50 = 58% FAIL baseline; expected ≥40/50 = 80% PASS |
| Stage 3 milestone tag sequencing | knight-rider per gandalf sign-off § 4 | Wave 5.5 intermediate seam-prefixed tag fires now; final `elrond/v0.0-cycle-10-stage-3-v1-scope-materialization` fires AFTER Wave 5.5 + Wave 6 land |
| Borderline Mode-C eviction case (Claíomh Solais id=175669) | knight-rider routes to gandalf for judgment | Modern-period tag on a legitimate mythological weapon — eviction was rule-correct but the underlying period-tag may be the actual error; gandalf decides remediation path (re-promote with corrected period; v1.1+ queue; or accept loss) |
| Heuristic-edge gandalf review candidates | knight-rider routes to gandalf | Per § 1.6: met:Miscellaneous routes to OTHER (Bagh Nakh + ~3-5 similar); royal-armouries "magazine" name-token override mis-labels rifle rows; documented in per-row rationale JSON |

---

## 7. Cross-references

**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-wave-5-5-phase-0c-and-mode-c-eviction.md`

**Authority chain:**
- gandalf 50-row spot-check (FAIL): `agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md`
- gandalf sign-off § 3 Conditions 1 + 3: `agentic_orchestration/gandalf/notes/2026-05-25-stage-3-distribution-report-sign-off.md`
- gandalf SO-4 RATIFY-WITH-AMENDMENT: `agentic_orchestration/gandalf/notes/2026-05-25-so-1-2-4-sign-off-verdicts.md`
- gandalf SO-3 Pattern A-deep (Discipline #25 first canonical application): `agentic_orchestration/gandalf/notes/2026-05-25-so-3-pattern-a-deep-verdict-roland-karna-stage-3-5-amendment.md`

**Substrate chain:**
- Parent dispatch (Stage 3 v1_scope materialization): `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md`
- Phase 0a precedent: `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/accessory-armor-subcategory-classification.md`
- Phase 3 distribution report (pre-Wave-5.5 baseline): `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/v1-scope-distribution-report.md`

**Policy + framework:**
- Composition policy v1: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- Marginal-lineage Mode A/B/C/D framework: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Engineering disciplines (#11 empirical inspection, #18 methodology-before-execution, #25 semantic-layer rep-audit): `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

**Wave 5.5 artifacts (this dir):**
- `classify_tier_a_subtype.py` — Phase 0c classifier code
- `phase-0c-tier-a-subtype-classification.json` — per-row classification trace + per-subtype counts
- `phase-0c-classify-log.out` — execution log with empirical pre/post counts
- `mode_c_eviction.py` — Part B Mode-C eviction code
- `eviction-candidates-pre.json` — full pre-eviction candidate list (30 rows + breakdown)
- `gandalf-eviction-audit-sample.json` — 10-row random sample for gandalf small-batch audit
- `mode-c-eviction-log.out` — execution log
- `post_wave_5_5_distribution.py` — distribution recomputation + spot-check sample assembly
- `post-wave-5-5-distribution.json` — full closeout distribution payload
- `post-wave-5-5-distribution-log.out` — execution log
- `post-wave-5-5-spot-sample-50.json` — 50-row spot-check sample pack for gandalf re-run
- `backups/telemetry.db.pre-wave-5-5` — pre-Wave-5.5 DB backup (gitignored)
- `MIGRATION.md` — Wave 5.5 migration record (updates-only pattern per ADR-004)

---

## 8. Sign-off

**Author:** elrond (substrate seam; Wave 5.5 classifier + eviction execution)
**Date:** 2026-05-25
**Authority:** dispatch FIRE-READY (Sidecar B mining COMPLETE; commit `6efd730`) + gandalf sign-off Conditions 1 + 3 (SQL signature pre-specified) + Cycle 10 scope-doc § 1 autonomous decisions on heuristic-rule design
**Status:** Wave 5.5 execution complete; v1_scope reduced 3,042 → 2,251; 791 rows evicted across Phase 0c (761) + Part B (30); composition shifts surfaced in § 5 for knight-rider routing decision

**Awaiting:**
- (a) knight-rider routing of 10-row eviction sample → gandalf small-batch audit
- (b) knight-rider routing of 50-row post-Wave-5.5 spot-check sample → gandalf re-run audit
- (c) knight-rider routing decision on Phase 2 micro-sample re-fire per § 5 + § 6
- (d) Stage 3 milestone tag sequencing (after Wave 5.5 + Wave 6 land)
