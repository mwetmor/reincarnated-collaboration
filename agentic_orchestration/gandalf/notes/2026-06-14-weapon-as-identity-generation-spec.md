# Weapon-as-identity generation spec — rocket hand-off

**Type:** design-spec-as-math hand-off (gandalf seam → rocket, via KR sequencing).
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 (Pattern-B) — "author both" (this spec + push the recognition record). **Load-bearing Matt constraints (verbatim):** (1) "use the pre-curated pool of weapons that we selected for cycle 14 rather than the entire pool, otherwise we will end up with a skew towards physical and we may select weapons that are less coherent choices for an ARPG kit." (2) "make sure the elrond folder is the one with the manually created caster weapons in it." (3) **[2026-06-14 ratio directive — § 1.2]** "21% casters will not suffice, so we will need to cycle through the caster set until we reach the physical vs caster (regular or proxy) ratio we desire. This needs to be in the engine docs and must be part of the process."
**Companion docs:**
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` — the recognition record this spec operationalizes (recognition LOCKED, validate DONE, commit DEFERRED). **This spec is the buildable validate step.**
- `~/Games/reincarnated-engine/src/reincarnated/generation/class_generator.py` § 605-664 — the element/energy-rooted fork this spec replaces.
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py` § `select_n_substrate_weapons_per_bc_cell` (line ~457) — the per-bc_cell weapon selection point.
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py` § 71-92 — the 8-tuple bc_target (no weapon axis; the diagnosis).
- `agentic_orchestration/elrond/research/substrate-enrichment-2026-05-27/MIGRATION.md` — **THE manually-created caster weapons folder** (the elrond folder Matt named).
- `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md` — caster within-family shape audit (the open caster-faith remediation).

---

## 0. TL;DR — what this spec is, and what it is NOT

**IS:** the design-spec-as-math that **rocket builds to RUN the recognition record's empirical gate.** It specifies (a) WHERE kit identity comes from — the SELECTED WEAPON, replacing the element/energy fork; (b) WHICH pool the weapon is selected from — the cycle-14 BALANCED pool, not the corpus, not the raw martial-skewed pool; (c) HOW a weapon-rooted physical kit reaches the legacy kit_size band off the rich weapon substrate instead of the sparse physical-cost mechanic pools.

**IS NOT:** a committed architecture. Per recognition → validate → **commit**, the architecture commit stays DEFERRED until the § 4 gate fires green. This spec is the *validate step*, not the commit. If the gate fails, the spec revises; it does not silently ship.

**The one-line design move:** the selected weapon becomes BOTH the identity root (its `weapon_type_family`) AND the skill-composition surface (its proxy/element/damage properties) — unifying what is currently split between the `dominant_element=="physical"` pseudo-element fork and the `classify_archetype → ARCHETYPE_TEMPLATES` label→template fallback.

---

## 1. The balanced pool (the load-bearing Matt constraint) — LIVE-VERIFIED

Identity is rooted on the **cycle-14 balanced pool = `weapon_knowledge_entries.v1_scope = 1`**, verified live against `~/Games/reincarnated-loadout/data/telemetry.db` 2026-06-14:

| Pool | Total rows | Caster+hybrid share | Use for identity rooting? |
|---|---|---|---|
| Full corpus (`weapon_knowledge_entries`) | ~90,014 | ~caster-sparse, ~22% noise | **NO** — skews physical + pulls ARPG-incoherent rows (Matt's stated failure mode) |
| Raw pre-enrichment `v1_scope` (2026-05-27 morning) | 2,293 | 327 (14.3%); 0 hybrid | **NO** — 85.8% martial; caster identity starves |
| **Cycle-14 BALANCED pool (`v1_scope=1`, post-enrichment)** | **2,499** | **533 (21.3%)** | **YES — root here** |

**Live `v1_scope=1` family composition (2,499 rows):**

| `weapon_type_family` | n | share |
|---|---|---|
| martial-heavy | 801 | 32.1% |
| ranged | 796 | 31.9% |
| martial-light | 369 | 14.8% |
| caster-arcane | 235 | 9.4% |
| caster-faith | 228 | 9.1% |
| hybrid | 70 | 2.8% |
| **physical sub-pool (martial+ranged)** | **1,966** | **78.7%** |
| **caster sub-pool (arcane+faith)** | **463** | **18.5%** |

**The manually-created caster weapons (the elrond folder Matt named):** `agentic_orchestration/elrond/research/substrate-enrichment-2026-05-27/`. Source-tag `legolas_crawl_substrate_enrichment_v1_2026_05_27` — **206 rows, all `v1_scope=1`, verified live:** 75 INT-AoE (→ caster-arcane), 61 Monk (→ caster-faith / WIS-melee), 70 Hybrid (NEW family). These rows are what lifted caster+hybrid representation from 14.3% → 21.3%. **This is the difference between a caster identity that has coherent weapon surface to root on and one that falls back to martial.** (NB: `engine_authored_gap_fill_v1`, 42 v1_scope=1 rows, is a *mixed named-weapon* set — 18 martial-heavy / 9 ranged / only 14 caster — NOT the caster set; do not conflate.)

### 1.1 The skew-control rule (Matt's failure mode, made precise)

A naive uniform sample of `v1_scope=1` assigns physical identity **78.7% of the time** — exactly the "skew towards physical" Matt named. Identity assignment is therefore **family-aware per-bc_cell, NOT uniform-over-pool.** The weapon for a bc_cell is selected by `select_n_substrate_weapons_per_bc_cell` matching the cell's behavioral bins (geo/tempo/attribute) — so caster-flavored cells draw from the 463-row caster sub-pool and physical-flavored cells draw from the 1,966-row physical sub-pool. **rocket confirms the existing binding already honors family-to-cell affinity (it should, via `proxy_attribute_class` / `weapon_type_family` matching); if any code path samples `v1_scope` uniformly to set identity, that path is the skew bug and is in scope to fix.**

### 1.2 Ratio-targeted selection — the caster-cycling requirement (Matt directive 2026-06-14, LOAD-BEARING)

**§ 1.1 prevents *within-cell* skew but does NOT control the *across-roster output ratio*.** Family-aware per-bc_cell selection guarantees a caster cell draws a caster weapon — but if the bc_cells themselves mirror the pool's ~21% caster share, the generated roster's caster output collapses back toward 21%. **Matt has ruled that insufficient (verbatim 2026-06-14):** *"21% casters will not suffice, so we will need to cycle through the caster set until we reach the physical vs caster (regular or proxy) ratio we desire. This needs to be in the engine docs and must be part of the process."*

**The requirement (standing process requirement, NOT a tuning afterthought):** the weapon-selection process MUST hit a **target physical : caster output ratio** across the generated roster, where the **caster side = regular casters (caster-arcane / caster-faith weapons) + proxy casters (proxy-summon composition, L2 of the three-layer model).** The OUTPUT ratio is the controlled variable; the pool's natural family share is NOT.

**The mechanism — cycle the caster set:** the caster sub-pool (463 rows `v1_scope=1`; → ~635 after the magic-anchor sim_props pass) is far smaller than the physical sub-pool (1,966). To fill a caster quota ABOVE the caster set's natural share, the process **cycles through the caster set — re-drawing WITH REUSE** — rather than being capped at the pool's 21%. This is design-legitimate because **the weapon is the identity ROOT, not the whole kit:** the same Staff drawn for ten kits yields ten distinct kits (different element, spirit, skill-composition, bc_cell). **Weapon reuse ≠ kit repetition.** Staves recurring across a caster roster is genre-true — every ARPG has many staff-wielders.

**The parameter (named, Matt-tunable):** `target_physical_caster_ratio` — a first-class generation parameter, NOT pool-proportional. **Default = the canonical-locked genre-aligned distribution, NOT a placeholder guess** (Matt corrected the prior ~50:50 placeholder 2026-06-14 against the verified prior-session finding; the placeholder is retired):

> **`target_physical_caster_ratio` = 40–45% physical : 55–60% caster-side.** Canonical-locked per **Discipline #57 + Matt 2026-06-02 verbatim** (the genre-aligned physical/caster distribution); empirical anchor **QDX-5 = 43.2% / 56.8% — PASS** (`agentic_orchestration/qa/findings/2026-06-02-qdx-phase-3-qdx-5-gate-2.md`). Matt's recall of "42 / 58" lands inside the band on both axes — accurate, not off. Caster-side = regular casters (caster-arcane / caster-faith weapons) + proxy casters. (vs the pool's natural ~79 : 21 — the gap this caster-cycling requirement exists to close.)

**The nested proxy-primary sub-share — a SECOND lever at a DIFFERENT layer (do not conflate):** Matt's full recall was *"58% caster, with 23% being proxy-primary."* That 23% is **not a second weapon-family ratio** — under the three-layer model (§ 2) the physical/caster split is an **L1 weapon-family** property (what `target_physical_caster_ratio` + caster-cycling control), but proxy-primary is an **L2 skill-composition** property: a caster-family weapon hosts EITHER a regular-caster OR a proxy-primary (summoner) skill composition. So the proxy share is a **composition-rate within the caster-side bloc**, governed by a separate parameter (call it `proxy_primary_composition_rate`), NOT by weapon-cycling.

> **`proxy_primary_composition_rate` ≈ 15–25% of the total roster** (Matt recall "23%" sits at the top of this band — accurate). Source: `gandalf/notes/2026-06-12-proxy-primary-architecture-recognition.md` § 3 item 3 + Session-4 spec § 1.1 (genre-typical summoner share; D2 ladder + PoE league data; *NOT* a forced 33/33/33). **DISCIPLINE FLAG — recognition-record DRAFT, empirically gated, NOT a hard lock like the two-way split is.** The proxy-primary architecture type itself is still under recognition → validate → commit: the LABEL + share audit lock only at the gamora reachability + emergent-combat measurement pass (does a realistically-sampled proxy-stacked caster kit cluster at the ~0.80 `proxy_contribution_pct` centroid in emergent combat, AND land in-band at ~15–25%?). rocket MAY build the composition-rate plumbing against this DRAFT; the number does not become a hard generation target until that gate resolves. Treat 23% as the design prior, not a committed constant.

The roster's family-mix becomes a design dial, not an artifact of substrate availability — but the two dials live at two layers: L1 weapon-family (`target_physical_caster_ratio`, hard-locked) and L2 skill-composition (`proxy_primary_composition_rate`, DRAFT-gated).

**The coupled lever — set size ↔ ratio ↔ repetition:** the smaller the caster set, the more weapon reuse a given target ratio forces. **Growing the caster set reduces repetition at any target ratio** — which is exactly what the magic-anchor sim_props pass (firing now in elrond's seam, caster/hybrid ~533 → ~635) serves. Set-size and target-ratio are *coupled* design levers; this spec's caster-set-growth workstream and this ratio requirement reinforce each other.

**Enforcement point (rocket designs the locus; the binding REQUIREMENT is the output ratio):** two candidates — (a) bc_target composition emits caster-flavored cells at the target rate, or (b) the selection layer enforces the caster quota by cycling the caster set. Either or both; rocket chooses, the requirement is the *verified output ratio* (§ 4.4).

**MUST land in the engine docs + the generation process (Matt directive):** not an optional balance knob — a standing requirement of the weapon-selection pipeline. rocket encodes it as an explicit process step AND documents it in the engine generation docs; a decisions-log entry records the ratio-targeting decision (KR drafts, jack-ryan reviews per decisions-log ownership).

---

## 2. The three-layer identity model → the code change

Per the recognition record § 4. Identity is three independent layers; only Layer 1 is the kit-identity root:

| Layer | Source | Produces | Status |
|---|---|---|---|
| **L1 — identity** | selected weapon's `weapon_type_family` | physical / caster / hybrid | **the change** |
| **L2 — runtime label** | skill composition (proxy-summon presence) | normal vs proxy-caster (summon) | genre-true (D2/D4/Last Epoch); unchanged |
| **L3 — behavioral descriptor** | bc_target 8-tuple coordinate | the behavioral fingerprint | unchanged |

**The change (`class_generator.py` ~616-618):**

```python
# REMOVE (the smuggled pseudo-element + sparse-mechanic fork):
is_physical = (dominant_element == "physical" or energy_type in PHYSICAL_COST_TYPES)

# REPLACE WITH (weapon-family-rooted; the selected weapon is the identity root):
fam = selected_weapon.weapon_type_family          # from the bc_cell's bound weapon
is_physical = fam in {"martial-heavy", "martial-light", "ranged"}
is_caster   = fam in {"caster-arcane", "caster-faith"}
is_hybrid   = fam == "hybrid"
```

This deletes the `dominant_element=="physical"` pseudo-element smuggle (the exact label-as-input trap the BC-cutover deleted on the *elemental* path, still alive on the *physical* path) and the `classify_archetype → ARCHETYPE_TEMPLATES.get(archetype)` label→template fallback at ~636-642. Physical identity stops being a pseudo-element and a sparse mechanic-pool key; it becomes a *property of the rich weapon substrate*.

---

## 3. How a weapon-rooted physical kit reaches kit_size 10-13 (the gate's mechanism)

This is the load-bearing claim — the one the build TESTS, not the one the spec assumes.

**The deferral's stated blocker:** physical kit_size could not reach the legacy band (10-13 skills) because physical skills were keyed to the **sparse physical-cost mechanic pools** (`rage`=4, `focus`=4, `combo`=2, `stamina-as-resource`=2 — `composed_kit_adapter.py:82`). ~12 mechanic-keyed slots cannot yield 10-13 *distinct* skills without repetition.

**The weapon-as-identity dissolution:** root the physical kit's skill-composition surface on the **selected weapon's properties** — `proxy_geometry_class`, `proxy_range_class`, `proxy_tempo_class`, `element_affinity_modifiers_json`, damage profile — crossed with the bc_cell behavioral target. This is the SAME composition surface caster kits already use (element × bc_cell); the physical path simply stops being starved by routing through the 12-entry mechanic pool. The weapon substrate is rich (2,499 rows, multi-property each); the mechanic pool is sparse (12 keys). **Move the load from the sparse axis to the rich one.**

**Design intent (axis meanings; rocket designs the exact algorithm, jack-ryan gates it):**
- skill *geometry* variety ← weapon `proxy_geometry_class` × bc_cell `geo_bin`
- skill *range/tempo* variety ← weapon `proxy_range_class` / `proxy_tempo_class` × bc_cell `tempo_bin`
- skill *flavor/element* ← weapon `element_affinity_modifiers_json` (physical weapons can carry elemental affinity — a flaming greatsword is physical-identity, fire-flavored)
- skill *count* target ← the legacy physical kit_size band (10-13), reached off the above cross-product, NOT off mechanic-pool enumeration

---

## 4. Acceptance criteria = the recognition record's empirical gate

The build PASSES (→ gandalf reviews → architecture commit fires) when:

1. **(THE gate, verbatim from the recognition record § 6):** a weapon-rooted physical kit composes to the legacy physical kit_size band (**10-13 skills**) **WITHOUT depending on the sparse physical-cost mechanic pools** (`rage`/`focus`/`combo`/`stamina-as-resource`). I.e., kit_size is achieved off the weapon substrate cross-product, demonstrable by generating physical kits with the mechanic-pool path disabled/bypassed and confirming ≥10 distinct skills.
2. **Caster identity reads coherent:** caster-flavored bc_cells bind caster-family weapons from the 463-row caster sub-pool (the manually-created rows serving caster cells), NOT martial fallback. Spot-check: N generated caster kits, ≥X% carry a caster-family main weapon (rocket + gandalf set X at review; the floor is "materially better than the pre-enrichment martial-fallback rate").
3. **No identity smuggle remains:** `grep` confirms no live path sets identity from `dominant_element=="physical"` or from a label→template lookup. (Same do-not-re-import-the-trap discipline the BC-cutover spent three stages enforcing.)
4. **Output ratio hits target (§ 1.2):** a generated roster of N kits lands the physical : caster-side ratio within tolerance of `target_physical_caster_ratio` — demonstrably by cycling the caster set, NOT capped at the pool's ~21% caster share. Caster-side counts regular casters + proxy casters. The ratio is a verified pipeline property, present in the engine docs as a process step.

**If gate item 1 fails** — i.e., the weapon substrate cross-product does NOT yield 10-13 distinct physical skills — the deferral's blocker is REAL, not dissolved, and the spec revises (the recognition's prediction is falsified; that is a valid, valuable outcome, not a failure to suppress).

---

## 5. Caveats + open design calls (flag, do not silently absorb)

- **caster-arcane ~22% miscategorization tail** (caster-weapon-kind-audit § 2.1): crystal-prefixed melee weapons (`Crystal axe`, `moctezuma_obsidian_blade_knife`), world-objects (`Crystal Spire of Karabor`) sit in caster-arcane. Non-gating for the spike but degrades caster ARPG coherence; a light elrond curation pass is queued-not-blocking.
- **caster-faith within-family heterogeneity** (caster-weapon-kind-audit § 2.2-3.2): caster-faith is monk martial-arts (Bo Staff, Khat Chueak) + mace-dominant (62%) + thin faith-instrument tail (talismans, censers). A "caster-faith" identity rooted on a Battle Mace vs a Talisman reads very differently. The audit's Path A/B/C remediation is an **open gandalf design call** — deferred, not resolved here. It does not block this spec's gate but will shape caster-faith identity quality.
- **102 `gandalf-authored-magic-anchor-*` rows at `v1_scope=0`** (modern/medieval/ancient, authored 2026-06-01; live-verified out of the cycle-14 pool AND lacking `weapon_sim_props`): **Matt RESOLVED this 2026-06-14 — author the sim_props pass** (firing now in elrond's seam per `agentic_orchestration/gandalf/notes/2026-06-14-magic-anchor-simprops-design-spec.md`; six pool-grounded archetype profiles + family resolution + gun-caster ruling). This grows the caster set ~533 → ~635, **directly serving the § 1.2 ratio requirement** (more caster weapons to cycle = less repetition at any target ratio). The `v1_scope=0→1` flip is surfaced as a Matt-reversible deployment step (pool 2,499 → ~2,601); when it fires, this spec's § 1 anchor counts grow (the family-aware logic is count-independent).

---

## 6. Done / routing

- **rocket:** build the weapon-rooted identity derivation (§ 2) sourcing from the balanced pool (§ 1) with family-aware per-bc_cell selection (§ 1.1); compose physical kit skills off the weapon-property cross-product (§ 3); **implement the § 1.2 ratio-targeted caster-cycling as an explicit process step AND document it in the engine generation docs (Matt directive — "must be in the engine docs and must be part of the process")**; run the § 4 gate (including § 4.4 output-ratio verification). Math-note per Discipline #1; Gate-1 (jack-ryan). **Do NOT commit the architecture** — produce the gate result.
- **gandalf:** review the gate result → recognition record commit (gate green) OR spec revision (gate red); resolve the caster-faith remediation design call (§ 5) when it gates caster quality; review the elrond magic-anchor sim_props pass (the caster-set growth § 1.2 depends on).
- **jack-ryan:** Gate-1/Gate-2 on the rocket build; confirm no identity-smuggle path survives (§ 4.3); **draft the decisions-log entry for the § 1.2 ratio-targeting process decision** (KR coordinates; jack-ryan reviews per decisions-log ownership).
- **KR:** sequence the rocket hand-off against the cycle-14 queue; the Godot spike (separate track) does not block this; **coordinate the § 1.2 decisions-log entry capture.**

---

**Signed:** gandalf, 2026-06-14
**For:** the weapon-as-identity generation spec — root kit identity (physical/caster/hybrid) on the SELECTED WEAPON'S family drawn from the cycle-14 BALANCED pool (`v1_scope=1`=2,499, the one with the manually-created caster rows folded in — NOT the corpus, NOT the 85.8%-martial raw pool), with family-aware per-bc_cell selection so identity does not skew physical; compose physical kit skills off the rich weapon-property cross-product instead of the sparse physical-cost mechanic pools; and PROVE — not assume — that a weapon-rooted physical kit reaches the legacy 10-13 kit_size band, which is the recognition record's deferred-commitment gate.
