# Cycle 10 Stage 3 — v1_scope Materialization via Constrained Sampling (elrond + legolas Mode A consult prerequisite + gandalf curation review)

**Cycle:** 10 — Substrate Curation Multi-Stage Dispatch
**Stage:** 3 of 4 (composition-policy-driven constrained sampling)
**Owners:** elrond (lead — substrate seam; constrained-sampling implementation) + legolas Mode A (methodology consult prerequisite per Discipline #18) + gandalf (curation review on output; closure-call gate)
**Author:** knight-rider (orchestrator)
**Date:** 2026-05-24
**Status:** **DRAFT — pending Gate-1 critique-pair clearance (gandalf + jack-ryan parallel).** FIRE-READY post-Gate-1.
**Routing source:** `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 7 (Stage 3 execution parameters for elrond)
**State file:** `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`

---

## 0. TL;DR

Produce the `v1_scope` subset of the 89,841-row weapon substrate per the composition policy v1 locked at Stage 3 design call 2026-05-24 (D1-D7). Materialize as 3 new columns on `weapon_knowledge_entries`: `v1_scope BOOLEAN`, `v1_scope_composition_trace TEXT` (JSON), `v1_scope_genre_filter TEXT`. Estimated subset size **~1,700-3,100 items** (main weapons + secondaries + future Sidecar B + Stage 3.5 + Stage 4 rescue additions).

**Pipeline:**
1. **Phase 0a (elrond, ~30 min):** second-pass weapon-kind subcategory classifier on 255 Tier-S accessory+armor rows (per composition policy § 1.1 D1 prerequisite)
2. **Phase 0b (gandalf, ~30 min):** substrate-fit lookup for `accessory_weapon_integrated` → parent-weapon-kind compatibility (per composition policy § 1.1 D1b prerequisite)
3. **Phase 1 (legolas Mode A, ~30-60 min):** methodology consult on constrained-knapsack-with-must-include literature (per Discipline #18 hotspot)
4. **Phase 2 (elrond, ~1-3 hr):** constrained-sampling execution per composition policy § 2 (per-axis target weights) + § 3 (Option α/β/C cell-type matching) + § 7.1-7.3 (algorithm + outputs)
5. **Phase 3 (elrond, ~30 min):** per-axis distribution + per-tier counts + per-cell coverage report → handoff for Matt + gandalf sign-off

**Empirical criterion for completion:** all 89,841 active rows have `v1_scope` populated; v1_scope subset size lands in or near 1,700-3,100 range OR design-call re-engages for amendment; per-axis/per-tier/per-cell report ready for Matt + gandalf sign-off; gap-cell list ready for handoff to Stage 3.5 gap-fill scoping.

**Architecture B substrate-genre-flagging:** `v1_scope_genre_filter = 'fantasy|mythological|historical'` for Reincarnated v1; column extensible for future commercial profiles per Architecture B.

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1 (current truth oracle)
2. **`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (THE SPEC; load-bearing)** — D1-D7 locks, § 1 v1_scope membership rules, § 2 per-axis target weights, § 3 Option α/β/C cell-type matching, § 4 thin-cell resolution (10 cells routed; 5-tuple cell-pair sharing per D3), § 5 bi-modal form-library + named-bearer discipline, § 6 Architecture B integration, § 7 execution parameters, § 11 empirical grounding
3. **`canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`** (Architecture B production canonical — substrate-bound at Phase 2 + substrate-genre-flagging)
4. **`canonical/story/v1-bc-target-intent-2026-05-24.md`** (Stage 0 cell-targeting intent — Sketch A 22 cells / ~37 forms; Sketch B per-cell coverage floors; Sketch D substrate-led skew + tradition distribution; Sketch F 12 named-bearer anchors)
5. `canonical/story/attribute-system-2026-05-24.md` (4-attribute system; STR/INT/WIS/DEX cell-type categories)
6. `canonical/story/skill-system-2026-05-24.md` § 13 (substrate-AGNOSTIC Phase 2 + substrate-coalesces Phase 5 — context for Option α/β/C policy at Phase 2 substrate-binding)
7. `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary architecture per D1b auto-promote categories)
8. `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (Discipline #25 semantic-layer rep-audit — applies to Mode-C contamination at v1_scope inclusion boundary)
9. `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md` § Wave 3 (Stage 2 + 2.5 + pre-Stage-3 weapon-kind classifier outputs already landed)
10. `agentic_orchestration/elrond/research/cycle-10-stage-2-5-2026-05-24/tier-s-weapon-kind-classification.md` (449 Tier-S handheld_weapon rows per threshold R1)
11. `agentic_orchestration/gandalf/notes/2026-05-24-source-library-reputation-tier.md` + `2026-05-24-cultural-tradition-weight-lookup.md` (gandalf prep lookups — already feed Stage 2.5 composite; ALSO usable for Stage 3 distribution weighting if Phase 2 sampling needs additional source/tradition signals)
12. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #2 + #2.1 smoke + resource bounds; #11 empirical inspection; #18 + #18.2 methodology-before-execution; #19 + #19.1 background processes + cheapest-refuting-test; #25 semantic-layer rep-audit)

---

## 2. Inputs (substrate DB state — verified pre-fire)

- `weapon_knowledge_entries` — 89,841 active rows
- Stage 1 columns populated: `proxy_range_class`, `proxy_geometry_class`, `proxy_tempo_class`, `proxy_attribute_class`, `proxy_fingerprint_confidence` (22,033 typed; 67,808 NULL — Stage 4 territory)
- Stage 1.5 columns populated: 8 `extracted_*` columns including 1,051 `extracted_named_bearer` matches against Sketch F seed-list + tradition signals
- Stage 2.5 columns populated: `composite_score`, `quality_tier` (Tier S 1,126 / A 7,943 / B 58,315 / C 22,457), `named_mythological_match` (452 named-mythological-match path → Tier S)
- Pre-Stage-3 classifier column populated on 1,126 Tier-S rows: `weapon_kind_classified_subtype` (handheld_weapon 449 / siege_vehicle 316 / accessory 130 / armor 125 / art_object 52 / other 31 / ammo_consumable 23)
- **Tier-S denominator reconciliation (per Gate-1 amendment 1):** Tier-S count moved 1,065 → 1,126 between composition policy authoring (§ 11.1 snapshot value) and post-Stage-2.5 actual classifier output. **The classifier-output 1,126 (and its 449-handheld breakdown) is binding for Phase 2 sampling auto-include + smoke-test denominator.** Composition policy § 1.1 D1a "~449 rows" estimate now empirically confirmed; § 1.7 v1_scope total estimate envelope unaffected.
- Source-library reputation tier (4-tier A/B/C/D; 25 sources) and cultural-tradition weight (14 lineages; 6 Tier-3 excluded) already feeding composite

**Substrate DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`

---

## 3. Outputs

### 3.1 Schema extension on `weapon_knowledge_entries`

```sql
ALTER TABLE weapon_knowledge_entries ADD COLUMN v1_scope BOOLEAN DEFAULT 0;
ALTER TABLE weapon_knowledge_entries ADD COLUMN v1_scope_composition_trace TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN v1_scope_genre_filter TEXT;
```

- `v1_scope`: 1 if row included in v1 scope; 0 otherwise (default 0; substrate optionality preserved per Variant C)
- `v1_scope_composition_trace`: JSON capturing **why** row entered v1_scope OR why excluded (D1c case); format per § 3.4 below — all rows get a `composition_trace`, including `v1_scope = 0` rows with `rule: 'd1c_excluded_scope_deferred'` or omitted-from-pool rationale. NULL only on rows the sampler did not visit (e.g., out-of-genre-filter rows; recorded via NULL `v1_scope_genre_filter`).
- `v1_scope_genre_filter`: which genre filter the row passed (`'fantasy'`, `'mythological'`, `'historical'` for Reincarnated v1; column extensible for future commercial profiles per Architecture B; NULL for rows whose `register_canonical` is outside the Reincarnated-v1 genre filter)

### 3.2 Phase 0a output — accessory + armor subcategory classifier

- New values populated on existing `weapon_kind_classified_subtype` for 255 Tier-S accessory(130) + armor(125) rows
- Accessory subcategories: `accessory_handheld` / `accessory_weapon_integrated` / `accessory_horse_or_equipment`
- Armor subcategories: `armor_shield` / `armor_body_or_head`
- Artifact: `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-24/accessory-armor-subcategory-classification.md` + JSON
- Heuristic-only; no LLM cost; gandalf 25-row spot-check validates ≥80% sensible

### 3.3 Phase 0b output — substrate-fit lookup table

- gandalf-authored lookup mapping `accessory_weapon_integrated` subset → compatible parent weapon families (e.g., tsuba/menuki → katana/wakizashi/tanto; quiver → bow/crossbow; bayonet-lug → rifle/musket)
- Artifact: `agentic_orchestration/gandalf/notes/2026-05-24-accessory-weapon-integrated-parent-compatibility.md` (YAML/JSON structured-data block parseable by Phase 2 sampler)
- Used at Phase 2 by elrond sampler to keep `accessory_weapon_integrated` rows aligned with retained parent weapon families

### 3.4 v1_scope_composition_trace JSON schema (per row included)

```json
{
  "rule": "tier_s_auto_promote_handheld | tier_s_auto_promote_secondary | tier_a_preferred | tier_b_constrained_sample | tier_c_floor_fill | sketch_f_anchor_substrate_resident | sketch_f_anchor_substrate_missing_stage_3_5_target | stage_4_mythological_rescue_pending | sidecar_b_pending | stage_3_5_gap_fill_pending | d1c_excluded_scope_deferred",
  "tier": "S | A | B | C",
  "axis_contributions": {
    "register": "fantasy | historical | mythological | military_modern",
    "cultural_tradition": "european_medieval | east_asian | norse | greek | ...",
    "period": "fictional | classical | medieval | early_modern | ...",
    "mechanical_cell": "cell_NN_archetype_name",
    "proxy_density": "none | light | heavy"
  },
  "matching_policy": "option_alpha_martial_5tuple | option_beta_caster_attribute_level | option_c_cross_attribute_omega_penalty | not_applicable",
  "weapon_kind_classified_subtype": "handheld_weapon | accessory_handheld | accessory_weapon_integrated | armor_shield | ...",
  "filter_passes": ["genre_fantasy_mythological_historical", "weapon_kind_gate", "tier_protection"],
  "notes": "free-text optional"
}
```

### 3.5 Per-axis + per-tier + per-cell coverage report

- Artifact: `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-24/v1-scope-distribution-report.md` (markdown summary)
- Companion JSON: `v1-scope-distribution.json` (machine-readable; feeds Matt + gandalf sign-off)
- Sections:
  - **Per-tier counts:** Tier S / A / B / C in v1_scope vs total
  - **Per-axis distribution:** register / cultural-tradition / period / mechanical-cell / proxy-density actuals vs composition policy § 2 targets
  - **Per-cell coverage:** floor satisfaction per Sketch B (30-120 per cell-type) — pass/under-floor flagged
  - **Gap-cell list:** cells where coverage floor unsatisfied; routes to Stage 3.5 gap-fill scoping
  - **Sketch F anchor coverage:** which of the 12 named-bearer anchors have substrate-resident representation post-sampling (per Stage 1.5 finding: 9 of 12 substrate-present; 4 substrate-thin gaps queued for Stage 3.5 gap-fill per D5)
  - **Named-bearer gap-list subsection (required; per Gate-1 amendment 3):** explicitly enumerates the substrate-missing Sketch F anchors **Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh** as Stage 3.5 author-and-insert targets, paired with their per-cultural-tradition cell-coverage status. This gap-list flows directly into the Stage 3.5 gap-fill dispatch authoring (knight-rider → rocket + gandalf + star-lord) without re-derivation. Substrate-resident Sketch F anchors are flagged in `composition_trace.rule = 'sketch_f_anchor_substrate_resident'`; substrate-missing anchors get `rule = 'sketch_f_anchor_substrate_missing_stage_3_5_target'` recorded on a sentinel row (one per missing anchor; `v1_scope = 0` with composition trace naming the cultural tradition + Sketch F § 5.2 anchor identity)

### 3.6 Other artifacts

- Population script: `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-24/populate_v1_scope.py` (background execution per Discipline #19)
- Sampling-algorithm choice + rationale doc: `cycle-10-stage-3-2026-05-24/sampling-algorithm-rationale.md` (records methodology consult outcome + chosen algorithm + parameter choices)
- legolas Mode A consult artifact: `agentic_orchestration/legolas/research/cycle-10-stage-3-methodology-consult-2026-05-24/` (per Discipline #18 — fires before Phase 2)
- gandalf 50-row spot-check (post-Phase-2): `cycle-10-stage-3-2026-05-24/spot-check-gandalf-request.md` — validates v1_scope inclusion sanity across tiers + cell-types
- Pre-Phase-2 DB backup: `cycle-10-stage-3-2026-05-24/backups/telemetry.db.pre-stage-3-2026-05-24` (gitignored per Stage 1.5 precedent)

---

## 4. Method notes (composition-policy-driven; binding per D1-D7)

### 4.1 Auto-include rules (Tier S; per composition policy § 1.1)

- **D1a:** `quality_tier = 'S' AND weapon_kind_classified_subtype = 'handheld_weapon'` → ~449 rows auto-include with `rule: tier_s_auto_promote_handheld`
- **D1b:** `quality_tier = 'S' AND weapon_kind_classified_subtype IN ('armor_shield', 'accessory_handheld', 'accessory_weapon_integrated')` → ~100-160 rows auto-include with `rule: tier_s_auto_promote_secondary` (subcategory split per Phase 0a + parent-family-fit gate per Phase 0b)
- **D1c excluded:** `weapon_kind_classified_subtype IN ('siege_vehicle', 'art_object', 'other', 'ammo_consumable', 'accessory_horse_or_equipment', 'armor_body_or_head')` → flagged `v1_scope = 0` with `composition_trace.notes = "D1c excluded — scope deferred to v1.1+"`

### 4.2 Tier-A preferred-include + military_modern trim (per composition policy § 1.2)

- Tier A rows are **preferred-include**; eviction last in sampling
- `register_canonical = 'military_modern' AND tier = 'A'` rows are TRIMMED — sampling weight reduced ~80% (specific weight choice gets recorded in `sampling-algorithm-rationale.md`); D10 Path C confirmation NOT in scope for v1
- **Per-row sampling weight vs per-axis target weight composition (per Gate-1 amendment 5):** the 80% sampling-weight reduction is the INITIAL trim signal to the sampler; the FINAL military_modern v1_scope share is further constrained by per-axis target weight § 4.7 (composition policy § 2.1 — military_modern ~5-8% of v1_scope) at the constraint-satisfaction layer of the sampling algorithm. Phase 2 smoke § 8 measures against the per-axis target (5-8%), NOT the per-row sampling weight (80% trim). Naive composition of the two yields ~15-26% share which would trip smoke — that path is NOT correct; the constraint-satisfaction layer must enforce the per-axis target over the per-row weight

### 4.3 Tier-B + Tier-C constrained sampling (per composition policy § 1.3 + § 7.1)

- Constrained against per-axis target weights (§ 2) + per-cell coverage floors (§ 4.4)
- Methodology choice locked via Phase 1 legolas Mode A consult; recommended baseline is **greedy-with-swap-repair** (simple; design-call-friendly) with LP-solver as fallback if greedy gap-floor satisfaction lands >15% short
- Tier C eligibility: included ONLY to meet per-cell coverage floors when higher-tier alternatives unavailable

### 4.4 Per-cell coverage floors (per Stage 0 Sketch B)

- ~30-120 rows per cell-type depending on cell category (floor magnitudes in v1-bc-target-intent doc § 1)
- Floor accounting respects 5-tuple cell-pair sharing per D3 Option A: 5 routing-ambiguous pairs share 4-tuple substrate (proxy_density discriminated at form-generation, not sampling boundary)
  - Pair 1: Cell 1 Heavy Barbarian / Cell 5 Ancestor-Warrior — shared `(melee, low, spiky, STR)`
  - Pair 2: Cell 7 Archer / Cell 10 Falconer — shared `(ranged, high, flat, DEX)`
  - Pair 3: Cell 12 Standard Wizard / Cell 16 Arcane-Familiar Mage — shared `(ranged, medium, variable, INT)`
  - Pair 4: Cell 14 Pyromantic Caster / Cell 17 Necromancer Summoner — shared `(mid, low, spiky, INT)`
  - Pair 5: Cell 19 Channeling Cleric / Cell 25 Witch Doctor Petmaster — shared `(mid, medium, variable, WIS)`
- Floor failure on a cell does NOT block sampling completion; gap-cell list routes to Stage 3.5 gap-fill OR Sidecar B substrate-enrichment

### 4.5 Cell-type matching policies (per composition policy § 3 + Architecture B Phase 2 substrate-binding)

- **Option α (martial cells; STR or DEX primary; physical-element coupling):** 5-tuple mechanical-fingerprint match required at sampling boundary
- **Option β (caster cells; INT or WIS primary; non-physical-element coupling):** attribute-level match only at sampling boundary (skills deliver kit BC-target; weapon scales)
- **Option C (cross-attribute hybrid cells — Cell 15 Red Mage / Cell 23 Monk-archetype / Holy Knight):** substrate pulled from the primary-attribute-of-physical-vector pool (e.g., STR-melee for Red Mage cohesion-composing INT-flavored kit per composition policy § 4.1; WIS-substrate-base for Monk-archetype Option C). **The ω-penalty flag is set on ALL rows entering these cells by construction (not per-row evaluation) — these are per-cell architectural facts, not per-row decisions.** `composition_trace.matching_policy = 'option_c_cross_attribute_omega_penalty'` always-on for these cells; sampler implementer does not write a per-row Option-C branch

### 4.6 Thin-cell resolution (per composition policy § 4.1 — locked at design call)

- 10 cells with critical/under-floor substrate routed per D2 (table in composition policy § 4.1)
- Stage 3 sampling executes per-cell action; cells routed to Sidecar B / Stage 3.5 / algorithm proxy-spawn are FLAGGED in `composition_trace` but no substrate sampled at Stage 3
- Cell 14 Pyromantic Caster (0 typed) → flagged `composition_trace.rule = 'stage_3_5_gap_fill_pending'` for the cell

### 4.7 Per-axis target weights (per composition policy § 2)

- Register: historical ~50-55% / fantasy ~30-35% / military_modern ~5-8% / mythological NULL-handled (Stage 4 rescue adds ~30 rows; flag pending)
- Cultural-tradition per § 2.2 (Pan-Fantasy/Hybrid ~20% hefty; European medieval ~18%; East Asian ~15%; etc.)
- Period: substrate-led skew preserved with composition weighting nudge toward medieval/classical (~10-15%) — sync with register trim
- Mechanical-cell + proxy-density per § 2.4 (STR ~24% / DEX ~27% / INT ~27% / WIS ~24%; proxy-density none ~75%)
- Tier S/A protected per § 2.5

### 4.8 Genre filter (per Architecture B substrate-genre-flagging)

- Apply BEFORE sampling: row eligible ONLY if `register_canonical IN ('fantasy', 'mythological', 'historical')` (military_modern routed by D1 / register weights, not by genre exclusion; sci_fi / cyberpunk / future-profile registers excluded for Reincarnated v1)
- `v1_scope_genre_filter` column populated with the passing register value (or NULL on D1c exclusions / out-of-filter rows)

### 4.9 Stage 4 mythological-NULL rescue + Sidecar B + Stage 3.5 gap-fills (per composition policy § 1.4-1.6)

- These are downstream additions; Stage 3 v1 sampling fires against CURRENT 89,841 substrate
- Stage 4 mythological-NULL rescue (~30 rows): flagged `composition_trace.rule = 'stage_4_mythological_rescue_pending'` on the NULL-typed mythological rows for downstream re-sample
- Sidecar B (~600-1,400 v1_scope-eligible additions from ~1,400-5,500 sourced): re-sample pass post-Sidecar-B; Stage 3 v1 dispatch does NOT block on Sidecar B completion
- Stage 3.5 gap-fills (~25-50 engine-authored entries): same — re-sample post-Stage-3.5

---

## 5. Cross-seam impact

- **Substrate DB schema change** (3 new columns on `weapon_knowledge_entries`; 1 column UPDATE-in-place on `weapon_kind_classified_subtype` for 255 accessory+armor subdivision) — REQUIRES MIGRATION.md per ADR-004 if any other seam consumes this table directly
- **Empirical check (per Phase D precedent):** elrond grep-verifies at Phase 2 launch which seams consume `weapon_knowledge_entries` schema; if any cross-seam consumer exists, MIGRATION.md authored before tag. Stage 1 + 1.5 + 2.5 found ZERO cross-seam consumers (purely loadout-app substrate read); same pattern expected here. MIGRATION.md drafted at deliverable path as additive-column-pattern per established precedent
- **Round-trip Principle 6 (per REVIEW_PROCESS.md):** **Round-trip: not applicable** — additive columns on substrate DB only; no fight_log dict / loadout dict / export packet structure / inter-seam fixture touched; no engine code touched; loadout app reads substrate but does NOT yet consume v1_scope (drax integration is post-Cycle-10 work per T4-reframing request)
- **No row deletion or destructive curation** — additive only; substrate optionality preserved per Variant C
- **No engine code touched**

---

## 5.5 Acceptance criteria (formal per dispatches/README.md § Acceptance criteria + Principle 6)

- [ ] Phase 0a subcategory classifier executed on 255 Tier-S accessory+armor rows; gandalf 25-row spot-check ≥ 20/25 sensible (~80% threshold)
- [ ] Phase 0b substrate-fit lookup landed at named gandalf-note path with YAML/JSON parseable structured-data block
- [ ] Phase 1 legolas Mode A consult artifact landed at named legolas-research path with chosen algorithm + parameter recommendations + cheapest-refuting-test design
- [ ] Phase 2 population script executes successfully against 89,841-row substrate; all 3 new columns + 1 UPDATE-in-place column populated; ZERO regressions on prior-stage columns
- [ ] Phase 2 pre-population smoke ≥ 7/10 prediction-match on hand-graded 10-row sample
- [ ] Phase 2 post-population smoke all SQL assertions return 0 (Tier-S non-handheld; Tier-3-lineage via named-match; Mode-C-flagged in v1_scope)
- [ ] Per-axis distribution histogram within ±5pp of composition policy § 2 targets across register / cultural-tradition / period / mechanical-cell / proxy-density / military_modern share
- [ ] Phase 3 distribution report + companion JSON landed at named elrond-research paths; named-bearer gap-list subsection lists the 4 substrate-missing Sketch F anchors
- [ ] gandalf 50-row Phase 2 spot-check PASS ≥ 40/50 (~80% threshold)
- [ ] MIGRATION.md drafted at deliverable path per Phase D precedent (additive-column-pattern verified vs prior stages; zero production-code consumers grep-confirmed)
- [ ] Pre-Phase-2 DB backup created and gitignored per Stage 1.5 precedent
- [ ] **Round-trip: not applicable — additive substrate-only; no cross-seam contract change per Principle 6 trigger-type table; no engine code touched; no fight_log dict / loadout dict / export packet structure / inter-seam fixture touched; loadout app reads substrate but does NOT yet consume v1_scope columns (drax integration is post-Cycle-10 work per T4-reframing request).**
- [ ] AGENT_STATE.md updated at session end (elrond seam if maintained; otherwise Cycle 10 state file)
- [ ] Tag: `elrond/v0.0-cycle-10-stage-3-v1-scope-materialization` after Matt + gandalf sign-off on distribution report (per composition policy § 7.4 empirical criterion)

---

## 6. Out of scope (explicit)

- NOT Stage 3.5 engine-authored gap-fills — separate dispatch (rocket + gandalf + star-lord + jack-ryan Gate-2; ~25-50 entries)
- NOT Stage 4 accurate mechanical-tagging — separate dispatch (rocket + gamora + jack-ryan + legolas Mode A consult prerequisite per Discipline #18)
- NOT Sidecar B substrate-enrichment crawl + schema extension — separate dispatch (elrond + legolas Mode B + gandalf curation review)
- NOT Stage 3.7 / "re-sample post-enrichment" pass — fires AFTER Sidecar B + Stage 3.5 + Stage 4 rescue land; separate dispatch at that point
- NOT v1.1+ enhancements per accumulated v1.1+ queue (15 items + Mode-E taxonomic extension + Stage-1 weapon_kind enum refinement)
- NOT Phase 5 cohesion-judge calibration spec — post-Cycle-10 canonical authoring queue (gandalf authors)
- NOT loot architecture canonical doc — post-Cycle-10 canonical authoring queue
- NOT element canonical-pair flavor architecture canonical doc — post-Cycle-10 canonical authoring queue
- NOT engine code changes — substrate-only stage
- NOT changes to existing Stage 1+1.5+2+2.5 column values — Phase 0a only EXTENDS `weapon_kind_classified_subtype` enum on already-classified Tier-S rows; no rescore of prior stages
- NOT loadout-app integration — separate post-Cycle-10 drax + star-lord scoping (T4-reframing request) — fires in parallel with Cycle 10 wind-down

---

## 7. Tag intent

`elrond/v0.0-cycle-10-stage-3-v1-scope-materialization` after:
1. Phase 0a + 0b complete
2. Phase 1 legolas Mode A consult artifact landed
3. Phase 2 sampling execution complete
4. Phase 3 distribution report ready
5. gandalf 50-row spot-check PASS
6. Matt + gandalf sign-off on per-axis distribution + per-tier counts + per-cell coverage (per composition policy § 7.4 empirical criterion)

**Intermediate tag (seam-prefixed) per project convention. NO Matt-approved milestone prefix removal at Stage 3 boundary** — final Cycle 10 milestone fires after Stage 4 + wind-down.

---

## 8. Smoke-test expectation

Per Discipline #2:

### Phase 0a smoke
- 25 random rows from 255 accessory+armor classified subset; gandalf spot-check ≥20/25 sensible subcategorization (~80% threshold per Stage 1 + 1.5 + 2.5 precedent)

### Phase 2 pre-population smoke
- SELECT 100 sample rows from substrate spanning all 4 tiers + 5 register classes + 6 cultural-tradition Tier 1/2 + 6 cell-types
- Manually predict v1_scope inclusion for ~10 rows using composition policy § 1 + § 2 + § 3 rules
- Run population on those 100; verify ≥7/10 match prediction
- Per-tier inclusion smoke: confirm 100% of Tier-S handheld inclusion + ~80%+ Tier-A preferred-include hit + ~5-15% Tier-B sample + Tier-C only-on-floor-fill

### Phase 2 post-population smoke
- Per-axis distribution histogram against composition policy § 2 targets; flag any axis where actual >±5pp from target
- Tier-S non-handheld_weapon: 0 rows in v1_scope (D1c gate verified) — assertion: `SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope = 1 AND weapon_kind_classified_subtype IN ('siege_vehicle', 'art_object', 'other', 'ammo_consumable', 'accessory_horse_or_equipment', 'armor_body_or_head')` MUST RETURN 0
- Tier-3-lineage (per gandalf cultural-tradition-weight): 0 rows in v1_scope via named-mythological-match path (Stage 2.5 Gate-3 already enforces; v1_scope inclusion verifies no Phase 2 leak) — assertion: `SELECT COUNT(*) WHERE v1_scope = 1 AND cultural_lineage_canonical IN (<Tier-3 list per gandalf weight doc>) AND named_mythological_match IS NOT NULL` MUST RETURN 0
- **Mode-C-contamination-flagged rows pass-through verification (per Gate-1 WARN-2):** Discipline #25 rep-audit working at consumption — explicit assertion: `SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope = 1 AND rep_audit_mode_c_naming_allusion_suspected = 1` MUST RETURN 0 (Mode-C-flagged rows from Stage 1.5 are blocked from named-mythological-match path at Stage 2.5 Gate-2; Phase 2 v1_scope inclusion must NOT leak them in via composite-top-1% pathway either). If non-zero, surface to Matt + gandalf for design-call review at Phase 3 sign-off — do NOT auto-strip retroactively

Per Discipline #2.1 resource-bounds projection:
- Phase 0a: 255 rows × ~50 token regex × <1ms per regex = <2 sec compute + <1 sec DB write
- Phase 2: 89,841 rows × per-axis weight evaluation (~10 hashed-lookup operations per row) = ~10 sec compute; sampler iteration (greedy-with-swap; bounded ~5K-row sample size) ~30-60 sec; DB write of 3 columns on 89,841 rows = ~60 sec; **total ~3 min compute + write**
- Memory: bounded by 89,841-row in-memory table at ~1-2 KB per row = ~150 MB peak; well within host RAM
- Background execution per Discipline #19 (no foreground polling)

---

## 9. Methodology consult per Discipline #18

**This dispatch IS a Discipline #18 methodology hotspot** — constrained-sampling against multi-axis weighted constraints with must-include + cell-coverage-floor + cross-attribute penalty is non-trivial. Per Discipline #18.2 (consultation-after-baseline at extension hotspots): Stage 1 + 1.5 + 2 + 2.5 baseline outputs already landed (empirical evidence available); Stage 3 methodology consult fires AFTER baseline + BEFORE Phase 2 execution.

**Phase 1 legolas Mode A consult scope:**
- Constrained-knapsack-with-must-include literature scan (~30-60 min)
- Algorithmic options surveyed: greedy-with-swap-repair / LP solver (CPLEX / Gurobi / open-source alternatives) / mixed-integer programming / simulated annealing
- Recommendation memo with: (a) chosen baseline algorithm + rationale; (b) failure-mode signals (when to fall back to LP solver from greedy); (c) parameter recommendations for our specific constraint structure (multi-axis weighted + must-include Tier S/A + per-cell floor + cross-attribute penalty); (d) cheapest-refuting-test design per Discipline #19.1 (e.g., per-cell-floor satisfaction percentage post-Phase-2)
- Output artifact: `agentic_orchestration/legolas/research/cycle-10-stage-3-methodology-consult-2026-05-24/methodology-recommendation.md`

**Sequencing discipline:**
- legolas Mode A fires BEFORE elrond Phase 2 (load-bearing gate)
- Phase 0a + 0b can fire in parallel with legolas Mode A (they don't gate methodology choice; they prepare substrate-side inputs)

---

## 10. Gate routing

- **Gate-1 critique-pair review on THIS dispatch:** fires now (parallel gandalf + jack-ryan); per critique-pair-gate-protocol § 3 Common Gate-1 catches — Principle 1 (math-before-code; composition policy doc + Phase 1 consult constitute the math), Principle 3 (cross-seam impact called out — additive substrate-only), Principle 4 (decisions-log truth — composition policy IS the locked decision via Stage 3 design call), Principle 6 (round-trip not-applicable justification per § 5)
- **Gate-2 critique-pair review on Phase 2 output:** fires AFTER elrond completion; jack-ryan DEV-MODE on per-tier composition trace fidelity + cross-seam round-trip review (substrate-only confirmation); gandalf design-side review on per-axis distribution alignment with composition policy § 2 targets + cell-type-matching policy fidelity (Option α/β/C) + Sketch F anchor coverage report sanity
- **gandalf 50-row spot-check** serves cheapest-refuting-test per Discipline #19.1 + feeds Gate-2 design-side review
- **Matt + gandalf sign-off on distribution report:** per composition policy § 7.4 empirical criterion (also Phase 3 deliverable); if v1_scope subset size or per-axis distribution materially deviates from composition policy estimate (~1,700-3,100 items; per-axis targets), design call re-engages for amendment

---

## 11. Cycle context

- This is Stage 3 of 4 in Cycle 10 (Stage 4 + Stage 3.5 + Stage 3.6 follow); Wave 5 fires Stage 3.5 + Stage 4 in parallel post-Stage-3
- Composition policy v1 (THE spec) consolidates D1-D7 design-call locks; this dispatch is the execution layer
- Architecture B production canonical engine architecture (substrate-bound at Phase 2 + substrate-genre-flagging) governs the v1_scope semantics
- Decision routing per Matt 2026-05-23 hive-mind directive: elrond + legolas + gandalf decide within their seams; knight-rider orchestrates; Matt is LAST-resort escalation. Matt + gandalf sign-off on distribution report is empirical-criterion gate (per composition policy § 7.4), NOT routine decision routing

---

## 12. Discipline checklist (per engineering-disciplines.md)

- [x] **#1 math-before-code:** composition policy v1 doc (~520 lines) is the math; Phase 1 legolas Mode A consult adds methodology rigor
- [x] **#1.1 pre-fire resource-bounds projection:** § 8 — ~3 min compute + ~150 MB peak; well within host RAM
- [x] **#1.2 math-note code-citation discipline:** Phase 2 script cites composition policy § sections in code comments
- [x] **#2 + #2.1 smoke-test:** § 8 phased smoke (Phase 0a + Phase 2 pre/post)
- [x] **#11 empirical inspection:** Phase 3 distribution report is empirical-inspection artifact
- [x] **#18 methodology-before-execution:** Phase 1 legolas Mode A consult precedes Phase 2
- [x] **#18.2 methodology-consultation timing at extension hotspots:** consult fires AFTER Stage 1+1.5+2+2.5 baseline
- [x] **#19 + #19.1 background processes + cheapest-refuting-test:** Phase 2 runs background; Phase 1 consult names cheapest-refuting-test design
- [x] **#20 density-based row-duplication prohibition:** N/A (no density-based clustering)
- [x] **#23 framing-audit checklist:** composition policy doc is framing-audit substrate; Stage 3 EXECUTES-AS-FRAMED per locked D1-D7
- [x] **#24 single-parameter sweep isolation:** N/A (no sensitivity sweep)
- [x] **#25 semantic-layer rep-audit:** composition_trace passes through Mode-C contamination flags from Stage 1.5; rep-audit working at consumption (Stage 2.5 named-mythological-match path already filtered Tier 3 + 72 Mode-C-flagged rows; no Phase 2 leak path)

---

## 13. Cross-references

- Composition policy spec (load-bearing): `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- Architecture B production canonical: `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`
- Stage 0 cell-targeting intent: `canonical/story/v1-bc-target-intent-2026-05-24.md`
- Attribute system: `canonical/story/attribute-system-2026-05-24.md`
- Skill system § 13: `canonical/story/skill-system-2026-05-24.md`
- Off-hand items: `canonical/story/off-hand-items-2026-05-24.md`
- Marginal-lineage meta-record: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Cycle 10 state file: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`
- BC axes vocabulary: `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- Substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Dispatches template: `agentic_orchestration/dispatches/README.md`
- Critique-pair-gate-protocol: `agentic_orchestration/operating-procedures/critique-pair-gate-protocol.md`

---

## 14. Sign-off

**Author:** knight-rider (orchestrator)
**Date:** 2026-05-24 (authored) + Gate-1 amendments integrated post-critique-pair
**Authority:** composition policy v1 § 7 (locked at Stage 3 design call 2026-05-24 with D1-D7) + dispatch routing per gandalf request `2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 3 + Matt 2026-05-23 hive-mind decision-routing directive (knight-rider authors in-scope; Matt is last-resort escalation)
**Status:** **FIRE-READY** — Gate-1 critique-pair cleared (gandalf PASS-WITH-AMENDMENTS × 5 + jack-ryan PASS-WITH-AMENDMENTS × 2 WARN; all 7 integrated; 0 BLOCK). elrond picks up at next-session start per dispatch protocol.
**Gate-1 verdicts:** `agentic_orchestration/gandalf/notes/2026-05-24-gate-1-design-verdict-cycle-10-stage-3-dispatch.md` + `agentic_orchestration/qa/findings/2026-05-24-gate1-stage-3-dispatch.md`
**Amendment record:** § 2 Tier-S reconciliation (G-1) / § 3 JSON schema enum extensions (G-2, G-3) + composition-trace non-NULL clause (G-2) / § 3.5 named-bearer gap-list subsection (G-3) / § 4.2 per-row-vs-per-axis composition note (G-5) / § 4.5 Option C per-cell architectural-fact clarification (G-4) / § 5.5 formal Acceptance criteria section added (J-WARN-1) / § 8 Mode-C SQL assertion added (J-WARN-2)
**Owners:** elrond (lead — Phases 0a + 2 + 3) + legolas Mode A (Phase 1 methodology consult prerequisite) + gandalf (Phase 0b substrate-fit lookup + 25-row Phase 0a spot-check + 50-row Phase 2 spot-check + Gate-2 design-side + sign-off on distribution report)

---

## 15. Open questions for the agent to resolve (within scope)

- Phase 1 legolas Mode A consult: which algorithmic baseline lands (greedy-with-swap-repair vs LP solver vs MIP vs SA) — elrond + legolas decide post-consult per Discipline #18
- Phase 2 sampling iteration cap + swap-budget hyperparameters — elrond decides per consult recommendations
- military_modern Tier-A trim weight (~80% suggested in § 4.2) — elrond + gandalf finalize at Phase 2 launch per actual Tier-A military_modern row count and post-trim downstream effect
- Whether to fire Phase 0a + Phase 0b serially vs in parallel with Phase 1 — elrond decides (parallel recommended; they don't gate each other)
- Tag boundary: single tag at Stage 3 completion vs separate intermediate tags for Phase 0 + Phase 1 + Phase 2 + Phase 3 — elrond proposes; knight-rider ratifies per Wave 2 Option B precedent (single combined commit + tag)
