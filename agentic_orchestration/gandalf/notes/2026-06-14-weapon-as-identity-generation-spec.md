# Weapon-as-identity generation spec — rocket hand-off

**Type:** design-spec-as-math hand-off (gandalf seam → rocket, via KR sequencing).
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 (Pattern-B) — "author both" (this spec + push the recognition record). **Load-bearing Matt constraint (verbatim):** "use the pre-curated pool of weapons that we selected for cycle 14 rather than the entire pool, otherwise we will end up with a skew towards physical and we may select weapons that are less coherent choices for an ARPG kit." + "make sure the elrond folder is the one with the manually created caster weapons in it."
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

**If gate item 1 fails** — i.e., the weapon substrate cross-product does NOT yield 10-13 distinct physical skills — the deferral's blocker is REAL, not dissolved, and the spec revises (the recognition's prediction is falsified; that is a valid, valuable outcome, not a failure to suppress).

---

## 5. Caveats + open design calls (flag, do not silently absorb)

- **caster-arcane ~22% miscategorization tail** (caster-weapon-kind-audit § 2.1): crystal-prefixed melee weapons (`Crystal axe`, `moctezuma_obsidian_blade_knife`), world-objects (`Crystal Spire of Karabor`) sit in caster-arcane. Non-gating for the spike but degrades caster ARPG coherence; a light elrond curation pass is queued-not-blocking.
- **caster-faith within-family heterogeneity** (caster-weapon-kind-audit § 2.2-3.2): caster-faith is monk martial-arts (Bo Staff, Khat Chueak) + mace-dominant (62%) + thin faith-instrument tail (talismans, censers). A "caster-faith" identity rooted on a Battle Mace vs a Talisman reads very differently. The audit's Path A/B/C remediation is an **open gandalf design call** — deferred, not resolved here. It does not block this spec's gate but will shape caster-faith identity quality.
- **102 `gandalf-authored-magic-anchor-*` rows at `v1_scope=0`** (modern/medieval/ancient, authored 2026-06-01; live-verified out of the cycle-14 pool AND lacking `weapon_sim_props`): these are NOT in scope for this spec (not `v1_scope=1`). **Matt design call:** promote any subset into the cycle-14 pool to deepen caster surface, or leave for a later cycle? Flagged, not assumed.

---

## 6. Done / routing

- **rocket:** build the weapon-rooted identity derivation (§ 2) sourcing from the balanced pool (§ 1) with family-aware per-bc_cell selection (§ 1.1); compose physical kit skills off the weapon-property cross-product (§ 3); run the § 4 gate. Math-note per Discipline #1; Gate-1 (jack-ryan). **Do NOT commit the architecture** — produce the gate result.
- **gandalf:** review the gate result → recognition record commit (gate green) OR spec revision (gate red); resolve the caster-faith remediation design call (§ 5) when it gates caster quality.
- **jack-ryan:** Gate-1/Gate-2 on the rocket build; confirm no identity-smuggle path survives (§ 4.3).
- **KR:** sequence the rocket hand-off against the cycle-14 queue; the Godot spike (separate track) does not block this.

---

**Signed:** gandalf, 2026-06-14
**For:** the weapon-as-identity generation spec — root kit identity (physical/caster/hybrid) on the SELECTED WEAPON'S family drawn from the cycle-14 BALANCED pool (`v1_scope=1`=2,499, the one with the manually-created caster rows folded in — NOT the corpus, NOT the 85.8%-martial raw pool), with family-aware per-bc_cell selection so identity does not skew physical; compose physical kit skills off the rich weapon-property cross-product instead of the sparse physical-cost mechanic pools; and PROVE — not assume — that a weapon-rooted physical kit reaches the legacy 10-13 kit_size band, which is the recognition record's deferred-commitment gate.
