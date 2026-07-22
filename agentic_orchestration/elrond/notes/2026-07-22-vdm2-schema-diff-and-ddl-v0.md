# VDM-2 Schema-Truth Diff + DDL v0 Migration Plan — Wave W0

**Author:** elrond (data steward) · **Date:** 2026-07-22 · **Status:** DELIVERED (analysis + draft only; corpus.db UNTOUCHED)
**Wave:** W0, VDM-2 → Edition-next lap (gandalf `RUN-CONDUCTOR`)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-22-vdm2-edition-next-lap-charter.md`
**Spec under diff:** `matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md`
**DDL draft (companion):** `agentic_orchestration/elrond/notes/2026-07-22-vdm2-ddl-v0.sql` — **NOT APPLIED**
**Store diffed:** `agentic_orchestration/research/curated/corpus.db` @ **v1.1-verified** (terminal stamp confirmed)

---

## 0. STOP-WORK guards — all three PASS

| Guard | Result |
|---|---|
| Spec file present | PASS — `rdr-vdm2-field-delta-spec.md`, 18394 B, read in full |
| corpus.db == v1.1-verified | PASS — `corpus_schema_meta` terminal stamp = `v1.1-verified` / `v1.1-deprecation-source_urls` (same UTC 2026-07-19T20:04:46Z). The `2.0`/`2.1`/`2.3` stamps near the top are the OLD *three-layer ingest schema-model version* (2026-07-12 era), **not** a VDM-2 v2.0 — the log is append-only and the terminal row is v1.1. |
| No prior VDM-2 wave | PASS — zero stamps mention `vdm2`/`door_arg`/`structured deviation`/`v2.0-verified`. The two grep hits (`corpus-db-schema-proposal-2026-07-12.md`, `le-harvest-lich.json`) are (a) a SUPERSEDED v1.0 proposal and (b) a D-7.5 annotation that *references a future* VDM-2 LE re-crawl — neither is a wave that ran. |

**No fork blocked this wave. Proceeding.**

---

## 1. THE HEADLINE CORRECTION (read this first)

The spec self-declares (§0.2) that its schema model was **inferred from a rendered D3 viewer, not the JSON** — and mandates a diff before scoping. The diff's single most important finding:

> **The spec models a kit as a flat JSON record. The actual store is a NORMALIZED RELATIONAL schema.** Every VDM-2 block the spec draws as a nested JSON object (`door args`, `geometry{}`, `numerics{}`, `deviations[]`, `recognition_hooks[]`, `acceptance{}`) must be re-homed as a **side-car table keyed to `kit_id`**, not as a JSON column. The DDL v0 does exactly this.

The current store (confirmed by full `.schema` dump):

- **`canon_corpus`** (585 rows) — identity + provenance + the typed *lattice coordinate* prefix (attr/range/tempo/amp/proxy/commit `_val`+`_conf`) + the raw *descriptor* suffix (`mob_raw`/`geo_raw`/`ctrl_raw`/`def_raw`/`econ_raw`/`elem_raw`). PK = `kit_id`.
- **`kit_mapping`** (574 rows) — `mapping_json` (the rich per-kit blob: `skills[]`, `motion_frame`, `resource_economy`, `trigger_grammar`, **`t4_doors[]`**, `scaffold`, `fidelity_notes`), `grade`, `deviation_notes` (free-text prose), `terminal_state`.
- **`canon_engine_key`** (585 rows) — the BC-axis keyed values + `cell_key` (strict-13 pipe-serialization) + `geometry_value`/`delivery_value`.
- **`kit_dossier`** (3444) / **`kit_citations`** (1287) / **`verify_ledger`** (2068) / **`mint_ledger`** (12) / **`mechanic_gap_docket`** (19) — the VDM-1 four-stream tables.
- **`kit_master`** VIEW (574) — the governing assembled representation. `585 canon_corpus − 11 is_system=1 system-records = 574`.

**Where every VDM-2 target field lives TODAY** (verified by inspecting the `d3-masquerade-spear` exemplar row):

| Spec target | Current home | Current form |
|---|---|---|
| door tags (§2) | `kit_mapping.mapping_json → $.t4_doors[]` | bare array `["DUAL_PROXY","PERSISTENCE_ENGINE_uptime"]`; **no args** |
| deviation prose (§3) | `kit_mapping.deviation_notes` | unstructured free text |
| geometry (§4) | `mapping_json.skills[].geometry_value` (coarse enum) + `.delivery_notes` (adjectives) + `kit_dossier(family='skill_geometry')` (prose @ conf 0.82) + `canon_engine_key.cell_key` slots | split across 4 homes; **no bands** |
| `count_multiplier` (§4) | `mapping_json.skills[].delivery_notes` prose | **stranded in prose** ("tripling projectile delivery") |
| source-scale numerics (§5) | `mapping_json.delivery_notes` + `.fidelity_notes` + dossier payloads | **prose only** (83% DR, 5500% set-mult); no structured numeric |
| recognition_hooks (§6) | — | **none** (implicit in deviation prose) |
| acceptance block (§6) | — | **none** |
| mechanics verdicts (§7) | `verify_ledger(claim_family='mechanics')` | **EXISTS** — 530 CONFIRMED / 25 CONTRADICTED / 42 UNSUPPORTED (coarse, one row/kit) |
| atlas coords (§8) | `canon_engine_key.cell_key` (13-slot) + `canon_corpus.lattice_coord` (6-char) | **present**, needs promotion |
| mutation_surface (§8) | — | **none** |

---

## 2. SECTION-BY-SECTION DIFF

For each section: **spec-assumes vs actual · partial homes · wholly-new · D3-misfit risk.**

### §2 — Door parameterization (P0)

- **Spec assumes:** doors are "bare tags" with no arg schema; adding typed arg schemas registry-wide, bare usage stays legal.
- **Actual:** CONFIRMED exactly. Doors are a bare JSON array (`mapping_json.$.t4_doors`). **~28 distinct doors on record-270** (ZONE_CONTROL 45, PERSISTENCE_ENGINE_uptime 41, PROXY_ASCENSION 35, TEMPORAL_CHARGE 33, … DUAL_PROXY only **2**). "Bare usage stays legal" is trivially satisfied — bare IS the universal current state; the arg schema is a pure additive overlay.
- **Partial home:** none for args (wholly new). The door *vocabulary* is implicit in the array values.
- **Wholly new:** `door_registry`, `door_arg_schema`, `kit_door_arg` (3 tables in DDL).
- **D3-misfit risk:** MODERATE. The exemplar's `DUAL_PROXY` appears **2×** in 270 — it is one of the *rarest* doors, so the spec's arg-schema exemplars are drawn from a near-unique case. The high-frequency doors (`ZONE_CONTROL`, `PERSISTENCE_ENGINE_*`, `PROXY_ASCENSION`) are the ones whose arg schemas actually matter, and their arg surfaces are *unknown* from the D3 exemplar. Also: several doors already carry a `_suffix` mode (`PERSISTENCE_ENGINE_uptime` vs `_saturation`; `GEOMETRY_PROPAGATION_cascade` vs `_overkill`) — the suffix ALREADY encodes what the spec would formalize as an enum arg. **Fork D-1** below: do we normalize `_suffix` doors into `base_door + mode_arg`, or keep them as distinct door tokens? Data-hygiene note: **8 empty-string door slots** on record-270 need cleanup.

### §3 — Structured deviations + docket wiring (P0)

- **Spec assumes:** deviation prose → `deviations[]` with `class ∈ {engine_inexpressible, param_gap, accepted_downgrade}`; EI/PG auto-open a docket; accepted_downgrade requires owner sign-off. A "second intake" alongside the existing mint lane.
- **Actual:** `mechanic_gap_docket` EXISTS (19 rows) but has NO `deviation_class`, NO per-kit FK (uses an `evidence_kits` JSON array), NO `hook_refs`, NO structured `proposed_fix`. Deviation prose lives unstructured in `kit_mapping.deviation_notes`. All 19 dockets are `status='matt-ratified'` (VDM-1) — new auto-opened rows take `status='open'` (table default), cleanly distinguishing them.
- **Partial home:** the docket table itself (extend, don't recreate); deviation prose (raw source, preserved).
- **Wholly new:** `kit_deviation` table + 3 additive docket columns (`source_deviation_id`, `source_kit_id`, `intake_lane`).
- **D3-misfit risk:** LOW. The class enum is ontology-agnostic. The auto-docket CHECK on `accepted_downgrade` (owner sign-off mandatory) is enforced by a table CHECK in the DDL. **This is a strong section** — the pilot G4 gate (≥1 red assert routes to docket end-to-end) exercises it directly.

### §4 — Geometry bands (P1)

- **Spec assumes:** ONE `geometry{}` object per kit, with bands + `count_multiplier` + `motion_signature` + optional `exact{}`.
- **Actual:** geometry is **PER SKILL, not per kit.** The Masquerade exemplar has **3 skills** (Bone Spear / Simulacrum / Grim Scythe), each with its own `geometry_value` + `delivery_notes`. A flat single-`geometry{}` block is a **D3-single-skill-bias artifact** — the exemplar happens to have one *damage* skill so the viewer rendered one geometry. `count_multiplier` (triple volley) is prose-stranded in `delivery_notes` exactly as the spec predicts. The 13-slot `cell_key` already holds delivery/range/tempo/amp coordinates but at kit grain, coarser than the spec's bands.
- **Partial home:** `mapping_json.skills[].geometry_value` (coarse delivery enum); `kit_dossier(skill_geometry)` (the adjectives to band); `cell_key` slots (kit-level coords).
- **Wholly new:** `skill_geometry_band` (**per-skill grain** — critical divergence) + `motion_signature_registry`.
- **D3-misfit risk:** **HIGH — this is the biggest structural misfit.** The spec's single-geometry-per-kit shape breaks on: PoE support-gem kits (one skill, many geometry-altering supports), GD multi-skill loops, D2 synergy stacks (Lightning Sentry + Death Sentry + Fire Blast — 3 delivered geometries). The DDL re-homes geometry at `(kit_id, skill_ordinal)` grain. **The W2 pilot's PoE support-gem kit and GD transmuter are the exact refutation surface for this** — if they band cleanly at per-skill grain, the correction holds; if a support-gem's geometry is better modeled as *modifiers on a base skill's band* rather than its own row, that is a **G5 finding** to surface (see Fork D-2).

### §5 — Dual-column numerics + normalization-rule registry (P1)

- **Spec assumes:** `numerics{}` = `{source_value (immutable/anchored), source_scale, rdr_value (rule-derived), rule}`; a versioned rule registry owned by the battle-sim team; sim reads `rdr_value` only.
- **Actual:** source-scale numerics exist ONLY as prose (83% DR / 5500% in `delivery_notes`/`fidelity_notes`). No structured numeric, no rule registry, no `rdr_value`. **Wholly new** and matches the spec's problem statement cleanly.
- **Wholly new:** `normalization_rule` (versioned registry) + `kit_numeric`.
- **D3-misfit risk:** LOW structurally, but **CROSS-SEAM ownership fork.** The spec says the rule registry is "owned by the battle-sim team." The *table* lives in corpus.db (elrond seam), but rule *semantics* ("D3 set multipliers map into the RDR T4 multiplier band") are engine-balance decisions (gamora/star-lord). Per ADR-004, the rule-registry SEMANTICS need a battle-sim sign-off even though the table is mine. **Fork D-3** below. The DDL carries a `rule_owner` field and `formula_ref` (pointer, not inline math — I do not author balance transforms). The D2 Lightning-Sentry pilot has exact-geometry via the `.txt` datamine lane — good `exact{}`/rule stress test.

### §6 — recognition_hooks + acceptance block (P2)

- **Spec assumes:** ranked `recognition_hooks[]`; machine-checkable coverage QA (no CLOSE while a hook is unexpressed & not downgrade-covered); `acceptance{signature[], delta_t4{shape, asserts[]}}`; `delta_t4.shape=step` = threshold experience, human-validated.
- **Actual:** NONE exists. The concept is implicit in deviation prose ("player would miss…"). Wholly new.
- **Wholly new:** `recognition_hook`, `kit_acceptance_assert`, `kit_delta_t4` (with `shape` + `shape_signoff`).
- **D3-misfit risk:** MODERATE. `delta_t4.shape ∈ {step, ramp}` is where the spec's own §9 flags the risk: the D2 Lightning-Sentry Trapsin is a *stacked-synergy gradient* — "the hardest fit for `shape:step`." The DDL keeps `shape` a 2-value enum but the pilot may reveal a third shape (e.g. `stacked` / `threshold_after_ramp`). I did **not** pre-add a third value (G5: don't let non-D3 force a schema change speculatively) — if the pilot needs it, that is a designed finding. `H4` provenance=`player_attested` is handled by the `provenance` enum. Coverage QA is a VIEW/app-check, not a trigger (kept flexible).

### §7 — VERIFY extension (P3)

- **Spec assumes:** mechanics verdicts DON'T yet exist ("claims the sim will consume carry conf scores but no verdicts"); add mechanics coverage + anchor-entailment lint + `player_attested` source.
- **Actual:** **CORRECTION — mechanics verdicts DO exist.** `verify_ledger.claim_family` already includes `'mechanics'` (**598** rows total: 530 C / 25 X / 42 U / 1 SNF; the components sum to 598 — a prior "597" total here was an off-by-one transcription slip, reconciled per jack-ryan Gate-2 WARN 2026-07-22). They are COARSE (one "core skills + resource" claim per kit). What the spec wants is *finer granularity* (per geometry-band, per numeric.source_value, per skill-loop) — an **extension of coverage WITHIN the existing family**, not a new family/table.
- **Partial home:** `verify_ledger` (extend with additive columns).
- **Wholly new:** 3 additive columns (`claim_subject`, `anchor_lint`, `source_lane`). **Deliberately NOT touching** the `claim_family`/`verdict` CHECK constraints (SQLite can't ALTER a CHECK without a table rebuild — and no new family/verdict *value* is needed, so no rebuild). VDM-2 mechanics rows set the existing `run_tag='vdm2'`.
- **D3-misfit risk:** NONE. The rubber-stamp detector is a query, not a schema object.

### §8 — Housekeeping (P3)

- **`atlas_coords` on-record:** the 13-dim tuple ALREADY exists as `cell_key` (268/270 on-record) + `lattice_coord` (270/270). This is a **promotion/denormalization** so pinnacle-synthesis + season-mutation read coords without an atlas join. 2 record kits lack `cell_key` (`poe1-blood-magic-kit`, `d2-teleport-sorc` — both mechanically atypical) → stay NULL honestly.
- **expected-section checklists:** per-source-game config, NOT per-kit data → modeled as a small reference table (`expected_section_checklist`).
- **`capstone.source_acquisition` enum:** wholly new column (`capstone_source_acquisition`); drives T4 reveal presentation.
- **`mutation_surface`:** folds into `kit_door_arg.mutation_surface` (per-arg `locked|mutable`) per the spec's own §8 note — NOT a separate mechanism, NOT a canon_corpus column.

---

## 3. HOUSEKEEPING IS NOT FREE — the charter's 7-item list, audited

The charter lists housekeeping as if uniformly cheap. The diff says **3 are cheap, 4 are real derivations:**

| Item | Verdict | Evidence |
|---|---|---|
| `corpus_class` (record\|annex) | **CHEAP** (derived from `corpus_bucket`, 100% non-NULL) | but see Fork D-4 (585 vs 574; 11 system-records) |
| `original_element` (promote `elem_raw`) | **CHEAP** — precondition MET | `elem_raw` = **270/270 non-NULL on record**, 0 blanks (verified) |
| `atlas_coords` on-record | **CHEAP** (promote `cell_key`) | present 268/270; 2 honest NULLs |
| `eras_normalized` | **REAL DERIVATION** | `eras` is per-game semicolon shorthand (`3.0-3.6;3.7-3.13`, `lod;d2r`, `aom-2017;patch-1.1-1.2`); needs a per-game era map |
| `court` (k=5, from `elem_raw`) | **REAL DERIVATION + OPEN Q** | `elem_raw` has ~21 distinct values on-record incl. `physical?`, `void`, `aether`, `acid`, `necrotic`(5), `vitality`(6), `magic`(4), `n/a`(5), `mixed(fire/cold/lightning)`; k=5 mapping for the non-canonical tail is undefined (Fork D-5) |
| `mutation_surface` | **CHEAP** (folds into `kit_door_arg`) | spec §8 |
| (implied) `capstone_source_acquisition` | **NEW DERIVATION** | must read capstone provenance per kit from mapping/dossier prose |

**`court` clean cases** (record-270, direct k=5 hits): physical 85, fire 54, lightning 38, cold 27, chaos 22, poison 4. That is 230/270 that map by the obvious rule (+ chaos∪poison → `chaos-poison` court = 26). The remaining **~40 rows** (vitality, necrotic, aether, void, acid, magic, n/a, the `?`-suffixed, the `mixed()`) need an explicit Q38-sanctioned rule. **This is the single housekeeping item I cannot resolve in-seam** — court taxonomy for non-canonical elements is a Q38 design call, not a data-steward call.

---

## 4. MIGRATION PLAN (additive-first)

**Nothing below is applied this wave.** Application = Wave W3.

### 4.1 Sequencing

1. **W2 pilot FIRST (gate the DDL).** The 4-kit cross-ontology pilot (Masquerade D3 · Lightning-Sentry D2 · PoE support-gem · GD transmuter) is the refutation surface for the two HIGH-risk corrections (§4 per-skill geometry; §6 delta_t4.shape). Per G5, if a non-D3 pilot forces a *breaking* change, the DDL returns to draft — that is a finding, not a failure.
2. **W3 apply, in this order:** (a) verified backup `corpus.db.pre-vdm2-schema-<date>-backup` + md5; (b) jack-ryan Gate-2 on the DDL; (c) run the additive DDL (all `CREATE TABLE IF NOT EXISTS` + `ALTER … ADD COLUMN`); (d) housekeeping data riders (corpus_class, eras_normalized map, original_element promotion, court map, atlas_coords promotion); (e) FINAL statement = the `v2.0` stamp into `corpus_schema_meta`; (f) MIGRATION.md entry per ADR-004; (g) re-generate the compendium from `kit_master`.
3. **W4 re-emission** populates the side-car tables (door args, deviations, bands, numerics, hooks, acceptance) in per-game tranches.

### 4.2 What is breaking, and why it is avoidable

**Nothing in DDL v0 is breaking.** Audit:

- Every new structure is `CREATE TABLE IF NOT EXISTS` (side-car) or `ALTER TABLE … ADD COLUMN` (nullable, defaulted). SQLite `ADD COLUMN` is O(1) metadata-only and cannot invalidate existing rows.
- **Zero** `DROP`, zero `ALTER … DROP/RENAME COLUMN`, zero CHECK modification. `kit_master` (574) recomputes identically (it selects named columns; new columns are invisible to it until the view is intentionally extended later). The 469+ frozen `cell_key`s are untouched.
- The one place SQLite *would* force a breaking rebuild — adding a value to an existing CHECK (`verify_ledger.claim_family`/`verdict`) — is **avoided** because §7 needs no new family/verdict value (mechanics already exists; new columns carry the granularity).
- **FK note (non-breaking but flagged):** the new tables declare FKs to `canon_corpus(kit_id)`. SQLite enforces FKs only when `PRAGMA foreign_keys=ON`. The W3 script must set it ON *before* inserting side-car rows so a typo'd `kit_id` fails loud. Existing data is unaffected.

**Gate G5 pin:** the only path to a breaking change is if the W2 pilot proves a spec shape wrong in a way that can't be expressed additively (e.g. per-skill geometry turns out to need a *restructure* of `mapping_json` itself). That path is a designed FINDING that returns the spec to §0 with the bias register updated — it does not get forced through.

### 4.3 Reversibility

Every housekeeping derivation preserves its raw source (`eras`→`eras_normalized`, `elem_raw`→`original_element`+`court`, `cell_key`→`atlas_coords`; raws never dropped). Full rollback = restore the pre-VDM-2 backup (elrond seam convention, VDM-1 lineage). Side-car tables are independently droppable without touching VDM-1 data.

---

## 5. OPEN QUESTIONS / FORKS FOR THE CONDUCTOR

Forks I could **not** resolve in-seam (they cross into design/Q38/cross-seam territory):

- **D-1 — `_suffix` doors (§2 scope).** ~28 door tokens include suffix-mode variants (`PERSISTENCE_ENGINE_uptime`/`_saturation`, `GEOMETRY_PROPAGATION_cascade`/`_overkill`). Normalize into `base_door + mode_arg` (cleaner arg model, but re-keys existing `t4_doors` tokens = a data touch), or keep them as distinct doors (bare-tag legacy preserved, but the arg registry then has redundant near-duplicate doors)? **My lean:** keep distinct tokens for W0/W2 (avoids touching frozen `mapping_json`), record the mode-collapse as a *candidate* normalization for a later pass. Conductor confirms.

- **D-2 — per-skill geometry grain (§4, HIGH-risk).** The DDL re-homes geometry at `(kit_id, skill_ordinal)` against the spec's flat single-`geometry{}`. This is the right shape for multi-skill kits, but the W2 PoE-support-gem pilot may show that support-gem geometry is better modeled as *band-modifiers on a base skill* than as its own skill row. That is a G3/G5-relevant finding. **Needs the pilot to rule.**

- **D-3 — normalization-rule registry ownership (§5, CROSS-SEAM).** Rule *semantics* are battle-sim (gamora/star-lord) per the spec, but the *table* is corpus.db (my seam). ADR-004 says a cross-seam migration needs knight-rider routing + Matt approval. Does the rule-registry TABLE ship in the VDM-2 schema now (I own the container; battle-sim populates rule rows later), or does it wait for a battle-sim co-authored migration? **My lean:** ship the empty container now (it's additive and mine), flag the rule-population as a downstream battle-sim dependency. Conductor + knight-rider route.

- **D-4 — `corpus_class` on 585 vs 574 (housekeeping).** The charter says "corpus_class 574/574" but `canon_corpus` has 585 rows; the 11 extras are `is_system=1` system-records (loot-economy/progression ladders, no `kit_mapping`). My DDL adds a 3rd enum value `system` so all 585 get a class (record 270 · annex 304 · system 11 over the 574+11). Confirm the enum admits `system`, or should system-records be left `corpus_class=NULL` and the rider run only over the 574 kit_master rows?

- **D-5 — `court` k=5 for non-canonical elements (housekeeping, DESIGN CALL).** ~40 record rows carry elements outside {fire,cold,lightning,physical,chaos,poison}: `vitality`(6), `necrotic`(5), `aether`(4), `void`(3), `acid`(3), `magic`(4), `n/a`(5), the `?`-suffixed, `mixed(fire/cold/lightning)`. Q38 fixed k=5 courts but (as far as W0 can see) did not publish the mapping rule for these. This is a Q38 design call I explicitly do NOT make. **Blocks the `court` data-rider (not the schema).** The column + CHECK are safe to land; the *population* waits on the rule.

- **D-6 — `eras_normalized` target vocabulary (housekeeping).** `eras` is per-game shorthand with no cross-game normal form today. Does `eras_normalized` want (a) a numeric era-year band, (b) a game-agnostic ordinal (early/mid/late), or (c) a per-game canonical era-label set? The Leg-B derivation consumes this, so its shape should suit Edition-next. **Needs a target-shape ruling** before the W3 rider.

---

## 6. DELIVERABLE SUMMARY (for the review book)

**Diff highlights (the 5–10 bullets):**

1. **Spec is flat-JSON; store is normalized-relational.** All 6 nested VDM-2 blocks re-home as `kit_id`-keyed side-car tables. Largest correction; drives the whole DDL.
2. **§7 mechanics verdicts already exist** (**598** rows in `verify_ledger`, family=`mechanics`; out of 2068 total ledger rows — prior "597" reconciled per jack-ryan Gate-2 WARN 2026-07-22). Spec assumed they don't. §7 becomes a *granularity* extension (3 additive columns), not a new table — and needs **no CHECK rebuild**.
3. **§4 geometry is per-skill, not per-kit.** The exemplar's 3 skills expose the D3-single-skill bias. Re-homed at `(kit_id, skill_ordinal)`. **Highest misfit risk**; the PoE/GD pilots are its refutation surface.
4. **`count_multiplier` and all source-scale numerics are prose-stranded exactly as predicted** (Masquerade's "tripling projectile delivery", 83% DR, 5500% all live only in `delivery_notes`/`fidelity_notes`). §4/§5 structures land them.
5. **Door args are wholly new but bare-usage is 100% of current state**, so the typed overlay is purely additive. But `DUAL_PROXY` (the exemplar) is 2-of-270 — one of the *rarest* doors; the arg model is validated against a near-unique case. High-frequency doors' arg surfaces are unknown from D3.
6. **`elem_raw` is 100% non-NULL on record-270** → `original_element` promotion is total (charter precondition MET).
7. **`atlas_coords` already exist** as `cell_key` (268/270) — §8 is a promotion, not a derivation.
8. **Housekeeping is 3 cheap / 4 real-derivation.** `eras_normalized` and `court` are genuine derivations; `court`'s non-canonical-element tail (~40 rows) is a Q38 design call that blocks the data-rider (not the schema).
9. **The 11-row gap** (585 canon_corpus − 574 kit_master) is all `is_system=1` system-records → forces the `corpus_class` enum question (Fork D-4).

**DDL summary:** 12 new tables + 9 additive columns across 2 existing tables, all additive.
- New tables: `door_registry`, `door_arg_schema`, `kit_door_arg` (P0 doors); `kit_deviation` (P0 deviations); `skill_geometry_band`, `motion_signature_registry` (P1 geometry); `normalization_rule`, `kit_numeric` (P1 numerics); `recognition_hook`, `kit_acceptance_assert`, `kit_delta_t4` (P2); `expected_section_checklist` (housekeeping).
- Additive columns: `mechanic_gap_docket` +3 (docket wiring); `verify_ledger` +3 (mechanics granularity/lint/lane); `canon_corpus` +6 (corpus_class, eras_normalized, original_element, court, atlas_coords, capstone_source_acquisition). `mutation_surface` lives on `kit_door_arg`, not canon_corpus.

**Migration risks:** none *breaking* (all additive). Operational risks: (1) `PRAGMA foreign_keys=ON` must be set in W3 before side-car inserts; (2) new dockets must take `status='open'` to stay distinct from the 19 `matt-ratified` VDM-1 rows; (3) 8 empty-string door slots + 2 missing cell_keys are honest-NULL/hygiene, not errors; (4) the CHECK-rebuild trap on `verify_ledger` is avoided by design.

**Forks I could NOT resolve in-seam:** D-1 (door-suffix normalization) · D-2 (per-skill geometry grain — needs pilot) · D-3 (normalization-rule registry cross-seam ownership — ADR-004) · D-4 (corpus_class over 585 vs 574) · D-5 (`court` k=5 for non-canonical elements — **Q38 design call**) · D-6 (`eras_normalized` target vocabulary — should suit Leg-B). D-3 and D-5 are the two that genuinely leave my seam; the rest are conductor confirmations.

---

**Signed:** elrond (data steward) · Wave W0 · analysis + draft only · corpus.db UNTOUCHED · local auto-commit, **no push** (E-2 default: local-only until Matt rules).
