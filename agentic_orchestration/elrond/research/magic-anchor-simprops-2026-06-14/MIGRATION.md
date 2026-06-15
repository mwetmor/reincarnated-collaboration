# MIGRATION — magic-anchor caster sim_props authoring pass — 2026-06-14

> **Per ADR-004 (cross-repo coordination + MIGRATION.md)**

**Authored:** 2026-06-14
**Author:** elrond (catalogue/substrate seam)
**Authority:** Matt-authorized 2026-06-14 (Pattern-B, via gandalf) — "Author the sim_props pass for these 102 in elrond's seam."
**Spec:** `agentic_orchestration/gandalf/notes/2026-06-14-magic-anchor-simprops-design-spec.md`
**Precedent (same mechanics):** `agentic_orchestration/elrond/research/substrate-enrichment-2026-05-27/MIGRATION.md` (206-row enrichment)
**Ingest script:** `scripts/ingest_magic_anchor_simprops_2026_06_14.py`

---

## 1. What this migration covers

Lifts the **102 `gandalf-authored-magic-anchor-*` caster-weapon rows** in
`reincarnated-loadout/data/telemetry.db` from knowledge-only reserve to
selectable weapon-as-identity roots.

**Pre-state (live-verified 2026-06-14):** all 102 had `v1_scope=0`, **zero** `weapon_sim_props` row,
**zero** `weapon_type_family`, `quality_tier` null, `quality_composite_score=0.0`.

| source_library | rows | period |
|---|---|---|
| `gandalf-authored-magic-anchor-ancient-2026-06-01` | 24 | classical |
| `gandalf-authored-magic-anchor-medieval-2026-06-01` | 29 | medieval |
| `gandalf-authored-magic-anchor-modern-2026-06-01` | 49 | contemporary |

`proxy_attribute_class` distribution (family-resolution INPUT): **INT 7 · INT_or_WIS 81 · WIS 6 · STR_or_WIS 6 · STR 2.**

---

## 2. Tables affected

### 2.1 `weapon_sim_props` (telemetry.db, reincarnated-loadout) — 102 NEW rows

One row authored per weapon_id (FK `weapon_id → weapon_knowledge_entries.id`). Columns populated:

| Column | Value |
|---|---|
| `weapon_type_family` | `caster-arcane` (76) / `caster-faith` (18) / `hybrid` (8) |
| `primary_stat` | INT (arcane) / WIS (faith) / STR (hybrid) — single-stat-per-caster-family preserved |
| `secondary_stat` | `none` for pure casters; `WIS` (faith overlay) for the 8 hybrid/STR rows |
| `range_min_units` / `range_max_units` | per template (see § 4) |
| `base_attack_speed` / `charge_time_s` / `aoe_radius_units` | per template |
| `hits_per_attack` | `1` (all single-hit casters) |
| `damage_amplitude_min` / `damage_amplitude_max` | per template (0.84/2.4 single-target; 0.48/3.0 area) |
| `spell_damage_modifier_pct` | per template band (45–85) |
| `base_physical_damage_l50` | `50.22` (caster modal) / `75.0` (hybrid/STR modal) |
| `element_affinity_modifiers_json` | `{"<element>": 15}` where elemental; `{}` otherwise (pool convention) |
| `sim_viable` | `1` (map onto proven-viable sibling templates — inherit presumption per spec § 6) |
| `sim_viability_notes` | `template=<X>; family=<F>; gandalf_magic_anchor_simprops_v1_2026_06_14[; <flag>]` |
| `sim_verified_date` | `2026-06-14` |

### 2.2 `weapon_knowledge_entries` (102 rows UPDATED)

| Column | Change |
|---|---|
| `quality_composite_score` | `0.52` (A-tier; 59 named-myth-anchor rows) / `0.43` (B-tier; 43 rows) — was `0.0` |
| `quality_tier` | `A` (59) / `B` (43) — was NULL |
| `v1_scope` | `0 → 1` (the Matt-reversible deployment step — see § 6) |
| `v1_scope_composition_trace` | EXISTING trace preserved; appended `magic_anchor_simprops_v1_2026_06_14`, `simprops_template`, `simprops_family` keys |

---

## 3. What DOES NOT change

- No new columns on either table (existing `weapon_type_family` free-TEXT column + SC-6b columns sufficient).
- No schema migration. `weapon_type_family ∈ {caster-arcane, caster-faith, hybrid}` uses pre-existing pool values; no new family value introduced.
- The single-stat-per-caster-family invariant is PRESERVED: post-pass caster-arcane = INT (311/311), caster-faith = WIS (246/246). No off-stat caster rows created.
- No changes to engine telemetry (`reincarnated-engine/data/telemetry.db` — distinct DB, star-lord seam).
- No changes to canonical docs, clustering algorithm, or character JSON output schema.

---

## 4. The six archetype templates (grounded in live pool exemplars)

Values are proven sibling-row conventions pulled live 2026-06-14; NOT invented.

| # | Archetype | family / stat | rng_min–max | spd | chg | aoe | amp | spellmod | exemplar |
|---|---|---|---|---|---|---|---|---|---|
| **A** | Arcane single-target (staff/rod/wand/focus) | caster-arcane / INT | 5.0–18.0 | 1.5 | 0.0 | 0.0 | 0.84–2.4 | 82 | Flutterby Rod |
| **A_short** | Spell-glove / gauntlet (close-mid hand-caster) | caster-arcane / INT | 2.5–10.0 | 1.5 | 0.0 | 0.0 | 0.84–2.4 | 82 | Flutterby Rod (short) |
| **A_ext** | Gun-caster (identity-forced, extended range) | caster-arcane / INT | 8.0–22.0 | 1.5 | 0.0 | 0.0 | 0.84–2.4 | 82 | (§ 5 ruling) |
| **B** | Arcane area (projector/diffuser/emitter) | caster-arcane / INT | 5.0–18.0 | 0.7 | 1.2 | 3.5 | 0.48–3.0 | 68 | Censer-pattern (arcane) |
| **D** | Faith ritual implement (censer/distaff/pestle/sceptre-regalia) | caster-faith / WIS | 2.5–7.0 | 0.7 | 1.2 | 3.5 | 0.48–3.0 | 85 | vajra |
| **E** | Faith long-range area (banner/oriflamme/tug/high censer) | caster-faith / WIS | 5.0–18.0 | 0.7 | 1.2 | 3.5 | 0.48–3.0 | 50 | Censer of Righteousness |
| **F** | Martial-faith hybrid (STR-coded named sword + overlay) | hybrid / STR (sec WIS) | 0.5–2.5 | 1.5 | 0.0 | 0.0 | 0.84–2.4 | 45 | Eldritch Knight's Longsword |

**Template distribution (102 rows):** A 56 · A_ext 5 · A_short 7 · B 8 · D 15 · E 3 · F 8.

### 4.1 DEVIATION from spec (noted, within elrond steward authority)

- **Template F atk_speed.** Spec § 3 lists hybrid/STR atk_speed = 1.2. The **live pool** hybrid/STR convention is **1.5** (Eldritch Knight's Longsword, Runic Greatsword, Gram, Death Knight's Runeblade — all 1.5). For pool coherence the F rows use **1.5** to sit beside the existing hybrid/STR siblings. This is the spec's stated principle ("grounded in real pool exemplars") winning over the spec's table value; flagged here for transparency.
- **Template C unused.** Spec offered template C (faith-melee channel, caster-faith/WIS, mace/reliquary-sword) as a possible route for STR_or_WIS faith-dominant swords. In the actual content, **all 8 STR/STR_or_WIS rows are named-legendary martial blades** (Brand of Surt/Roland — Mjolnir/Gungnir STR parallels; Joyeuse/Durendal/Hauteclère — Charlemagne/Roland/Olivier's actual swords; Skofnung — Norse saga-sword; San Pietro/Curtana — reliquary-swords on martial blades). Every one is martial-dominant, so all routed to **hybrid/F**, not caster-faith/C. This is independently corroborated by the pre-existing `v1_scope_composition_trace.matching_policy` already on these rows (`option_c_cross_attribute` on the 6 STR_or_WIS, `option_alpha_martial_5tuple` on the 2 STR) — the authoring intent already flagged them cross-attribute/martial. Net: template C had zero qualifying rows this pass.

---

## 5. Family-resolution rule applied (spec § 2)

| proxy_attribute_class | n | Resolution applied |
|---|---|---|
| `INT` | 7 | → caster-arcane / INT |
| `WIS` | 6 | → caster-faith / WIS (3 ancient/medieval deity-regalia sceptres + 3 modern sci-fi sceptres) |
| `INT_or_WIS` | 81 | per-row discriminator: deity-anchored **elemental/cosmic** foci → caster-arcane; **ritual-implement form** (censer/distaff/pestle/sigil/broom/athame/seiðstafr/cauldron-ladle/reliquary/banner/oriflamme) → caster-faith |
| `STR_or_WIS` | 6 | all named-legendary martial **swords** → hybrid / STR + WIS-secondary (template F) |
| `STR` | 2 | reliquary-swords (San Pietro, Curtana) → hybrid / STR + WIS-secondary (template F) |

**Final family split (102):** caster-arcane **76** · caster-faith **18** · hybrid **8**.

### 5.1 The 5 gun-casters (spec § 5 — Matt-visible flag)

`Thermal Channeler Carbine-Pistol` (226142) · `Coilgun Caster Pistol` (226168) ·
`Ion Pulse Carbine-Caster` (226171) · `Railgun Caster Rod` (226173) ·
`Antimatter Channeler Rifle-Caster` (226183).

Assigned **caster-arcane / INT, template A_ext (range_max 22)** per the spec ruling; tagged
`gun_caster_identity_forced` in `sim_viability_notes` (greppable). Honors the asserted caster
identity + the modern-caster-axis fill purpose. Matt can veto to ranged-DEX if the gun-form
should win — one-UPDATE per-row revert.

### 5.2 caster-faith share is content-driven (NOT a 50/50 split) — flag for gandalf

The spec's companion mace-domination finding hoped this pass would diversify caster-faith forms.
It does — adding **18** faith-form rows (censers, distaffs, pestles, sceptres, reliquaries,
banners, ritual-daggers, seiðstafr) that are NOT maces, directly diversifying away from the 62%
mace-domination. But the count is **+18, not ~+62** as the spec's rough prediction guessed,
because the actual content of the 102 is **overwhelmingly elemental-arcane** (deity-elemental
foci + sci-fi tech-casters), not devotional-faith. The faith routings are by ritual-implement
FORM (per spec § 4 keyword map), not by literal theology. This is the honest content read.

### 5.3 Closest-to-50/50 calls — gandalf adjudicates (per spec § 2)

These INT_or_WIS rows were routed to **caster-faith / D** on the strength of their **ritual-implement
form**, but their underlying power is **occult-arcane, not devotional-divine** — the genuine
form-vs-theology tension. Listed for gandalf review:

| id | name | routed | tension |
|---|---|---|---|
| 226113 | Witch's Brimstone Censer | caster-faith / D | witch-fire occult, but censer-form = ritual implement |
| 226135 | Grimoire Athame of Solomon | caster-faith / D | Solomonic conjuration (arcane), but athame-form = ritual implement |
| 226138 | Seiðstafr of the Völva | caster-faith / D | Norse seiðr (arcane-occult), but seiðstafr = ritual staff |
| 226140 | Inquisitor's Iron Maiden Reliquary | caster-faith / D | Inquisition-coded; reliquary-form = faith, but darker register |
| 226122 | Geomancer's Sigil-Pestle | caster-faith / D | geomancy (earth-divination, arcane), but sigil-pestle = ritual |
| 226124 | Witch-Storm Broom-Stave | caster-faith / D | witch-storm (occult), but broom-form = folk-ritual implement |

If gandalf prefers any of these in caster-arcane (treating occult-witch/grimoire/seiðr as arcane
rather than faith-ritual), the change is a per-row UPDATE (family `caster-faith→caster-arcane`,
stat `WIS→INT`, template `D→A` or `B`). The single-stat invariant is honored under either routing.

### 5.4 The 3 modern WIS sceptres — register tension flagged

`EMP Channeler Sceptre` (226174) · `Prism Array Sceptre` (226178) · `Blackhole Containment Sceptre`
(226188) were authored `WIS` by gandalf with an explicit **regalia/ceremonial-sceptre** register.
Per the single-stat invariant a WIS row must be caster-faith. Routed to **caster-faith / D**
(sceptre = regalia ritual implement) and tagged `wis_caster_register_tension_scifi` — the element
is sci-fi tech, not devotional, so the "faith" here is register/form, not theology. Greppable for
gandalf review; revertable to caster-arcane/INT if the sci-fi register should override the WIS coding.

---

## 6. The v1_scope-flip — the Matt-reversible deployment step (FLAG, not buried)

**Decision taken: `v1_scope` SET `0 → 1` on all 102** (spec § 6 default — honors "make these selectable").

**Pool-growth consequence (empirically verified post-flip):**

| Metric | Pre-flip | Post-flip | Delta |
|---|---|---|---|
| Total `v1_scope=1` (live cycle-14 BALANCED pool) | 2,499 | **2,601** | +102 |
| caster/hybrid share of pool | 21.3% (533/2499) | **24.4%** (635/2601) | +3.1pp |
| caster-arcane (whole pool, all v1_scope) | 235 | **311** | +76 |
| caster-faith | 228 | **246** | +18 |
| hybrid | 70 | **78** | +8 |
| martial-heavy / martial-light / ranged | unchanged | unchanged | 0 |

This is **directionally aligned** with the deliberate caster-enrichment trajectory (pool was
85.8% martial pre-206-enrichment) — GOOD, not a violation.

**ONE-UPDATE REVERSIBLE.** If Matt prefers cycle-14 frozen, revert with a single statement
(rows then stay ready-but-staged; all sim_props/family/quality authoring REMAINS in place):

```sql
UPDATE weapon_knowledge_entries SET v1_scope = 0
WHERE source_library LIKE 'gandalf-authored-magic-anchor%';
-- restores pool to exactly 2,499; the 102 keep their sim_props rows, families, and quality_tiers.
```

The sim_props authoring is independent of the flip — reverting v1_scope does NOT undo the
weapon_sim_props rows or the quality scoring. Only re-snapshot membership changes.

---

## 7. Quality scoring (spec § 6 acceptance #3)

Pool tier thresholds on `quality_composite_score` (live-verified 2026-06-14):
C 0.10–0.330 · B 0.330–0.479 · A 0.479–0.62 · S special (named-myth-correlated).

**Discipline call (elrond steward judgment):** these are gandalf-authored high-coherence rows,
but the pool's Pattern-6 named-bearer enrichment pipeline has NOT run on them
(`template_quality_score=0`, `extracted_named_bearer` empty on all 102). S-tier in the pool is
strongly correlated with a populated `named_mythological_match` (490/1214 S rows have it vs 0 for
A/B/C) — but S is RARE (1,214 across the whole pool). Mass-promoting the 59 magic-anchor rows
that carry `named_mythological_match` to S would distort the apex tier. Instead:

- **A (composite 0.52):** the **59** rows with populated `named_mythological_match` (genuine deity / named-legendary anchors).
- **B (composite 0.43):** the **43** rows without (sci-fi-vocabulary tech-casters + folk/alchemist forms; includes the 5 gun-casters and the 3 register-tension sceptres).

This sits the cohort as strong-but-not-legendary content, matching gandalf's review
("classical excellent; medieval coherent; contemporary mostly strong, 5 gun-casters flagged")
without inflating S. Reproducible from the ingest script (`tier_for_score`).

---

## 8. Cross-seam round-trip clause (per ADR-004)

| Consumer seam | Owner | Impact | Action required |
|---|---|---|---|
| rocket — substrate_weapon_binding.py | rocket (engine generation/) | READ-only; queries `weapon_sim_props ⋈ weapon_knowledge_entries WHERE v1_scope=1`. +102 caster/hybrid rows visible under existing query shape (`primary_stat` / `weapon_type_family` filters). No new family value. | None code-side; weapon-as-identity root pool grows +102 (anchor counts shift, family-aware logic unchanged). |
| Kit-identity / weapon-as-identity generation | gandalf design (`2026-06-14-weapon-as-identity-generation-spec.md`) | The 102 are now selectable kit-identity roots. | Aware of +102 selectable roots (3 register-tension + 5 gun-caster flags carry into selection telemetry via `sim_viability_notes`). |
| gamora — damage_resolver | gamora (engine simulation/) | NO direct impact. Reads character JSON from rocket. Sees new caster families through JSON shape only. Optional confirmatory sim-viability batch (non-blocking; templates are proven-viable siblings). | None required. |
| drax — loadout React app | drax (loadout/) | READ-only if any view enumerates families. No new family value (caster-arcane/caster-faith/hybrid all pre-exist). | None (no new enum value). |
| star-lord — engine telemetry | star-lord (engine output/telemetry/) | NO impact. These rows live on loadout-side telemetry.db; engine `data/telemetry.db` is a distinct DB. | None. |

---

## 9. Execution record

| Field | Value |
|---|---|
| Ingest agent | elrond |
| Ingest date | 2026-06-14 |
| Ingest script | `agentic_orchestration/elrond/research/magic-anchor-simprops-2026-06-14/scripts/ingest_magic_anchor_simprops_2026_06_14.py` |
| Pre-run backup | `~/Games/reincarnated-loadout/data/telemetry.db.pre-magic-anchor-simprops-2026-06-14.bak` (216 MB; full-DB rollback path) |
| Sim-props tag | `gandalf_magic_anchor_simprops_v1_2026_06_14` (in `sim_viability_notes` + composition_trace) |
| Rows authored | 102 `weapon_sim_props` rows (76 caster-arcane / 18 caster-faith / 8 hybrid) |
| Quality scored | 102/102 (A 59 / B 43) |
| v1_scope flipped | 102/102 (0→1; pool 2,499 → 2,601) — one-UPDATE reversible per § 6 |
| Single-stat invariant | PRESERVED (caster-arcane=INT 311/311; caster-faith=WIS 246/246) |
| Gun-caster flags | 5/5 (`gun_caster_identity_forced`) |
| Register-tension flags | 3 (`wis_caster_register_tension_scifi` — modern WIS sceptres) |
| 50/50 calls surfaced for gandalf | 6 ritual-form-vs-occult-theology rows (§ 5.3) |
| Schema migration | NONE |
| Status | COMPLETE (pending gandalf review of family resolutions + relay of v1_scope choice to Matt) |

### 9.1 Acceptance criteria (spec § 6) — all met

1. ✅ All 102 carry a `weapon_sim_props` row with `weapon_type_family ∈ {caster-arcane, caster-faith, hybrid}` + non-null `primary_stat`.
2. ✅ Family split honors § 2; the 5 gun-casters carry the § 5 flag.
3. ✅ `quality_tier` non-null on all 102.
4. ✅ Pool family counts re-reported: caster-arcane 235→311, caster-faith 228→246, hybrid 70→78. (caster-faith lighter than spec's ~290 guess — content-driven, see § 5.2.)

### 9.2 Validation queries

```sql
-- All 102 carry sim_props + family + stat
SELECT sp.weapon_type_family, sp.primary_stat, COUNT(*)
FROM weapon_sim_props sp JOIN weapon_knowledge_entries wke ON sp.weapon_id=wke.id
WHERE wke.source_library LIKE 'gandalf-authored-magic-anchor%'
GROUP BY sp.weapon_type_family, sp.primary_stat;
-- Expect: caster-arcane/INT 76 | caster-faith/WIS 18 | hybrid/STR 8

-- quality_tier non-null
SELECT quality_tier, COUNT(*) FROM weapon_knowledge_entries
WHERE source_library LIKE 'gandalf-authored-magic-anchor%' GROUP BY quality_tier;
-- Expect: A 59 | B 43 (zero NULL)

-- Single-stat invariant intact
SELECT weapon_type_family, primary_stat, COUNT(*) FROM weapon_sim_props
WHERE weapon_type_family IN ('caster-arcane','caster-faith') GROUP BY 1,2;
-- Expect: caster-arcane|INT|311 ; caster-faith|WIS|246 (no off-stat rows)

-- Pool growth
SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1;  -- Expect 2601
```

---

**Signed:** elrond (curation + ingest 2026-06-14)
**ADR-004 compliance:** MIGRATION.md covers the cross-seam data-contract change (102 new
`weapon_sim_props` rows + 102 `weapon_knowledge_entries` quality/scope UPDATEs; no schema
migration; no new `weapon_type_family` value). Consumers identified § 8. Pre-run backup at
`~/Games/reincarnated-loadout/data/telemetry.db.pre-magic-anchor-simprops-2026-06-14.bak`.
v1_scope flip surfaced as the Matt-reversible deployment decision (§ 6) — reported to gandalf
for relay at hand-back.
