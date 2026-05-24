# Cycle 10 Stage 1 — Cheap Proxy Mechanical Fingerprint (elrond + rocket)

**Cycle:** 10 — Substrate Curation Multi-Stage Dispatch
**Stage:** 1 of 4 (cheap-before-expensive sequencing)
**Owners:** elrond (lead — substrate seam) + rocket (collab — name-token / weapon-form lookup table authoring)
**Author:** knight-rider (orchestrator)
**Date:** 2026-05-23
**Status:** **DRAFT — fire-ready on Stage 0 transcription landing.** GATED on Matt + gandalf Stage 0 design call completion.
**Routing source:** `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 1
**State file:** `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`

---

## 0. TL;DR

Derive a coarse `(proxy_range_class, proxy_geometry_class, proxy_tempo_class)` tuple per substrate row (69,137 rows) from already-present `weapon_knowledge_entries` fields. **Zero LLM cost.** Heuristic-only via name-token lookup + structured_properties length/weight extraction where present. Damage-spread / amplitude axis DEFERRED to Stage 4 (accurate mechanical-tagging).

**Empirical criterion for completion:** every active row has a 3-tuple proxy fingerprint + per-row confidence score; gandalf 50-row spot-check pass validates fingerprint sanity.

**Parallelism:** fires in parallel with Stage 1.5 (per-source structured-field extractor — elrond + gandalf). Both gate on Stage 0.

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1 (current truth)
2. `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 1 + § 5.3 + § 5.4 (the spec + Discipline #18 hotspot table + #19.1 refutation discipline)
3. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes; this stage targets the 3 weapon-intrinsic axes range / geometry / tempo at COARSE-spine granularity)
4. **`canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 transcription — LANDED 2026-05-24)** — Sketch A 5-tuple cell space (range × tempo × amplitude × attribute × proxy-density); 22 cells / ~37 forms; bin vocabulary at coarse-spine granularity (range: melee / mid / ranged; tempo: low / medium / high; amplitude DEFERRED to Stage 4); attribute: STR / INT / WIS / DEX. Sketch C geometry distribution per-cell-type (categories: single / multi-hit / cleave / AoE / beam-SKILL-side-only / scatter / cone)
5. **`canonical/story/attribute-system-2026-05-24.md`** — 4-attribute system (STR/INT/WIS/DEX); element-attribute coupling; class-archetype + weapon-family mapping (drives proxy_attribute_class heuristic per § 4)

---

## 2. Inputs

- `weapon_knowledge_entries.canonical_name` — token regex against weapon-form lookup table
- `weapon_knowledge_entries.weapon_kind` — category / unique / named_template / ammo_or_consumable
- `weapon_knowledge_entries.wieldable_humanoid` — one_hand / two_hand / shoulder_supported / either / mount_required
- `weapon_knowledge_entries.structured_properties` JSON — length / weight / materials WHERE PRESENT (Stage 1 does NOT depend on Stage 1.5 for this; uses what's present in raw JSON without per-source extraction)

---

## 3. Outputs

**Schema extension on `weapon_knowledge_entries`:**

```sql
ALTER TABLE weapon_knowledge_entries ADD COLUMN proxy_range_class TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN proxy_geometry_class TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN proxy_tempo_class TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN proxy_attribute_class TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN proxy_fingerprint_confidence REAL;
```

Bin vocabulary **aligned with Stage 0 cell-space (`v1-bc-target-intent-2026-05-24.md` § 1 + § 3):**
- `proxy_range_class`: **melee / mid / ranged** (3 bins per Stage 0 Sketch A)
- `proxy_tempo_class`: **low / medium / high** (3 bins per Stage 0 Sketch A)
- `proxy_geometry_class`: **single / multi-hit / cleave / AoE / scatter / cone** (6 bins per Stage 0 Sketch C; **beam excluded — SKILL-side only**, not substrate-resident)
- `proxy_attribute_class`: **STR / INT / WIS / DEX** (per Stage 0 Sketch A + attribute-system doc § 1; derived from weapon-family token lookup — greatsword/maul → STR; bow/dagger → DEX; staff/wand/orb → INT; mace/holy-symbol/druid-staff → WIS; ambiguous → NULL with low confidence)
- **`amplitude` DEFERRED to Stage 4** (accurate mechanical-tagging on v1_scope rows) — Stage 1 does NOT populate; flat / variable / spiky bin vocabulary applies at Stage 4

Confidence score range: 0.0-1.0. Length/weight-grounded entries get higher confidence than name-token-only entries. Attribute-class ambiguous entries (e.g., war-mace could be STR or WIS) flagged with lower confidence + NULL attribute value for Stage 4 priority refinement.

**Artifact deliverables:**
- Lookup table at `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-XX/weapon_form_token_lookup.json` (~100-200 token types; rocket authors with elrond review)
- Population script at `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-XX/populate_proxy_fingerprint.py` (background execution per Discipline #19)
- Per-source confidence distribution summary at `cycle-10-stage-1-2026-05-XX/confidence-distribution.md` (museum-curated vs community-scraped variance check)
- gandalf 50-row spot-check artifact at `cycle-10-stage-1-2026-05-XX/spot-check-gandalf-2026-05-XX.md`

---

## 4. Method notes

- **Name-token lookup ~100-200 token types** covers most of substrate: sword / longsword / shortsword / dagger / bow / crossbow / arquebus / staff / cannon / hammer / mace / axe / spear / polearm / firearm / rifle / pistol / etc.
- **Length/weight extraction where structured_properties has it.** Default class assignment from token alone when not present.
- **Per-source variance expected:** museum-curated entries (Met Museum, Royal Armouries) likely produce cleaner fingerprints than community-scraped (Wikidata, TRPG). Lower-confidence flag on token-only entries.
- **Bin assignment from length-weight heuristics** (3-bin range per Stage 0 alignment):
  - `melee`: ≤180cm total length (sword, axe, hammer, dagger, mace)
  - `mid`: 180-300cm OR thrown weapons (halberd, pike, javelin, throwing axe, shortbow at mid-range)
  - `ranged`: bow / crossbow / firearm / siege-weapon tokens (regardless of physical length)
- **Tempo heuristic** (3-bin per Stage 0 alignment):
  - `high`: light/fast tokens (dagger, shortsword, twin-blade, rapier, kris, pistol/SMG, light-bow)
  - `medium`: standard tokens (longsword, axe, mace, standard bow, rifle)
  - `low`: heavy/slow tokens (greatsword, maul, polearm, two-handed-hammer, crossbow-with-winder, sniper-rifle, artillery)
- **Geometry heuristic** (6-bin per Stage 0 Sketch C):
  - `single`: point-tip weapons (dagger, rapier, spear, pistol, sniper-rifle)
  - `multi-hit`: twin-blade / multi-projectile / rapid-strike tokens
  - `cleave`: edged-sweep tokens (sword, axe, scimitar)
  - `AoE`: explosive / area tokens (grenade, cannon, bomb, artillery)
  - `scatter`: spread-projectile tokens (shotgun, multi-arrow, fan-shot)
  - `cone`: spread-cone tokens (flamethrower, cone-AoE)
- **Attribute heuristic** (4-bin per Stage 0 attribute-system doc § 1):
  - `STR`: greatsword / maul / two-handed-axe / heavy-polearm / war-hammer (STR-coupling per element_biases physical-coupling)
  - `DEX`: dagger / bow / crossbow / firearm / twin-blade / light-shield / kris / rapier (DEX precision/finesse)
  - `INT`: wand / staff / orb / tome / arcane-focus (INT arcane-coupling per fire/water/lightning/shadow elements)
  - `WIS`: mace / holy-symbol / ritual-implement / censer / horn / druid-staff (WIS channel-coupling per earth/wind/holy elements)
  - `NULL`: ambiguous (e.g., war-mace, ritual-axe) — flagged with low confidence + Stage 4 priority refinement
- **Confidence scoring:**
  - 0.9-1.0: structured_properties has both length + weight + materials, AND name-token cleanly maps to a single form-archetype with unambiguous attribute
  - 0.6-0.9: name-token maps cleanly; one or more structured fields present
  - 0.3-0.6: name-token maps cleanly; no structured fields
  - 0.0-0.3: ambiguous name-token OR ambiguous attribute (default class assigned with NULL attribute; flagged for Stage 4 priority refinement)

---

## 5. Cross-seam impact

- **Substrate DB schema change** (4 new columns on `weapon_knowledge_entries`) — REQUIRES MIGRATION.md per ADR-004 if any other seam consumes this table. **Empirical check:** at firing, elrond verifies which seams consume `weapon_knowledge_entries` schema directly; if any cross-seam consumer exists, MIGRATION.md authored before tag.
- **No row deletion or destructive curation** — additive only.
- **No engine code touched.**

---

## 6. Out of scope (explicit)

- NOT damage-amplitude / damage-spread axis — DEFERRED to Stage 4 (accurate mechanical-tagging post-v1_scope selection)
- NOT Stage 1.5 per-source structured-field extraction — separate parallel dispatch
- NOT methodology consultation per Discipline #18 — Stage 1 is heuristic-only; NOT a methodology hotspot
- NOT v1_scope flag population — Stage 3 territory
- NOT engine-authored gap-fills — Stage 3.5 territory
- NOT changes to existing Phase E-1 cluster_id values — clusters stay as substrate-led identity
- NOT changes to existing canonical_name / source_library / wieldable_humanoid values — additive columns only

---

## 7. Tag intent

`elrond/v0.0-cycle-10-stage-1-proxy-fingerprint` after acceptance criterion met + gandalf 50-row spot-check pass. **NO Matt-approved milestone prefix removal at Stage 1 boundary** — Stage 1 is intermediate; final milestone after Stage 4.

---

## 8. Smoke-test expectation

Per Discipline #2:
- Pre-population smoke: SELECT 100 random rows; manually predict proxy fingerprint for ~10; run population on those 100; verify ≥7/10 match prediction
- Post-population smoke: per-source fingerprint distribution histogram — sanity-check that Met Museum + Royal Armouries weapons trend toward higher confidence than Wikidata-only entries

Per Discipline #2.1 resource-bounds projection:
- 69K rows × ~100 token regex matches per row × <1ms per regex = ~7 seconds total (negligible)
- Population script fits comfortably in single-process Python; no parallelism needed
- DB write cost: 69K × 4-column UPDATE = ~30 sec; acceptable

---

## 9. Gate routing

- **No Gate-1 review required for this dispatch** — Stage 1 is heuristic-only with no methodology hotspot, no architectural commitment, no cross-seam new-scope. knight-rider authors + elrond+rocket execute. If elrond surfaces concern during execution, route to jack-ryan Pattern-A query.
- **No Gate-2 review required at Stage 1 boundary** — Stage 1 output consumed by Stage 2 + 2.5 which fold into Stage 3 design-call review.
- **gandalf 50-row spot-check** serves as the cheapest-refuting-test per Discipline #19.1 (in lieu of formal Gate-2).

---

## 10. Cycle context

- This is one of 9 stages in Cycle 10 (Sidecar A + Stages 0-4 + 3.5 + 3.6). Fires AFTER Stage 0 design call (Matt scheduling). Fires in PARALLEL with Stage 1.5 (per-source structured-field extractor).
- Stages 2 + 2.5 gate on Stage 1 + 1.5 completion.
- Decision routing per Matt 2026-05-23 hive-mind directive: elrond + rocket decide within their seams; knight-rider monitors; Matt is LAST-resort escalation.

---

## 11. Cross-references

- Dispatch source: `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 1
- State file: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`
- BC axes vocabulary: `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- Substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#2, #2.1, #19, #19.1, #21, #22)

---

## 12. Sign-off

**Author:** knight-rider (orchestrator)
**Date:** 2026-05-23
**Authority:** Matt 2026-05-23 — direct authorization of parent dispatch
**Status:** **DRAFT — FIRE-READY** pending Stage 0 transcription
**Owners:** elrond (lead) + rocket (token-lookup table collab)
