# KR BRIEF — ruled engine changes: `chain` rename · commitment `instant` spelling · `water`→`ice` + cold/frost register

> **PASTE INTO A KNIGHT-RIDER SESSION** (`cd ~/Games/reincarnated-collaboration && claude --agent knight-rider`), or prompt an adopted KR session with: *"Read `agentic_orchestration/gandalf/briefs/2026-07-12-kr-engine-renames-and-ice-element.md` and execute per its sequencing."* Authored by gandalf 2026-07-12. **Authority:** Matt rulings 2026-07-12 (geo-prep §5 G0 · elem-prep §6 EL2 · corpus-rekey-spec-v1.md §2 + §5 rows 1c/1d). gandalf recommends; KR sequences seams; specialists implement.

## Mission

Three Matt-RULED engine changes fell out of the corpus re-key design sessions. Two are hygiene renames; one is a genuine design change. KR dispatches them to seam owners with the sequencing below. **Source of record:** `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` §5 rows 1c/1d; per-slot rulings in `agentic_orchestration/gandalf/views/rekey-prep/geo-prep.md` §5 and `elem-prep.md` §6.

## Binding laws (all units)

1. **Census-first.** Each dispatch opens with a full-repo grep census of the identifier being renamed (src + config + tests + data artifacts) before any edit. Known surfaces below are anchors, not exhaustive lists.
2. **Historical artifacts immutable.** Emitted kits (`data/kit_space/`), telemetry rows, `output/` bundles, and past-season data keep their old strings as provenance. Renames land at **load boundaries** (read-compat normalizer: old string accepted on read → normalized) + **emit paths** (new string written going forward). Regen-able artifacts regen at next emission; never retro-edit.
3. **MIGRATION.md entry per unit** (ADR-004 / Discipline #12 semantic-shift documentation).
4. **Gate-2 (jack-ryan) on each unit** before tag.
5. **Auto-commit, no push** (Matt-gated per CLAUDE.md).
6. **No scope creep:** no freeze-mechanic design, no ailment-parameter changes, no new geometry types, no element-pool re-balancing. Renames + register pass only. Design questions that surface route back to gandalf.

## Unit 1 — `chain_lightning` → `chain` (rocket; hygiene, RULED geo G0)

Matt verbatim: *"For chain, we can map to chain_lightning, but we will need to change the engine's type name to chain as we go."* The geometry type predates the 8-element layer; the name wrongly welds a geometry to one element (a corpus `chain` kit can be any element — free-axis law).

- **Known surfaces:** `generation/geometry_constants.py` (16-type palette tuple, line ~26) · `generation/geometry_derivation.py` · `canonical/sidecars/emit_substrate_registry.py` → regen `atomic_substrate_registry_v1.json` · `simulation/damage_resolver.py` · `simulation/spatial_gauntlet/spatial_engine.py` + `spatial_resolver_adapter.py` · `generation/` consumers (bc_target_source, gear_instance_generator, proxy_vocabulary_bridge, bc_target_composer, weapon_envelope_composer, per_skill_emitter, ability_grammar) · **config:** `substrate_identities/lightning.yaml` (PREFER list) + `holy.yaml` (AVOID list) · 3 test files.
- **Persisted:** `data/kit_space/kits/*.json` carry `chain_lightning` — read-compat normalizer per Law 2; do not rewrite kit files.
- **Acceptance:** grep for `chain_lightning` in live code paths returns only the read-compat alias + historical-artifact references; tests green; registry sidecar regenerated.

## Unit 2 — commitment `"snap"` → `"instant"` (rocket + gamora touch; hygiene, RULED — ⚠ SEQUENCING HAZARD)

Enum of record (re-key spec §2): **instant / wind-up / channel**. Code currently spells the first bin `"snap"`.

- **Known surfaces:** `generation/per_skill_emitter.py` (`_COMMITMENT_SNAP`, `_TAU_SNAP`, bins frozenset, fallback return) · `generation/bc_target_player_class.py` (default `"snap"`) · `generation/bc_target_cell_sampler.py` (`COMMITMENT_BINS`) · `simulation/spatial_gauntlet/commitment_state_machine.py` (`BIN_SNAP`, fallback cast time) · `spatial_engine.py` comments/paths.
- **⚠ HAZARD 1 — persisted population:** the ENTIRE currently-certified kit population persists `bc_commitment: "snap"` (E4 byte-identity work asserts on it). Read-compat normalizer mandatory (`"snap"` → `"instant"` on read); emit `"instant"` forward; byte-identity guards updated to normalize before compare.
- **⚠ HAZARD 2 — E4 Gate-2 held:** commitment surfaces carry HELD E4 work (Steps 4–6 held, re-escalated — see KR's own E4 state). **KR decides:** fold this rename into the E4 closure wave, or fire strictly after Gate-2 resolves. Do NOT land it mid-hold.
- **Acceptance:** live code emits/compares `"instant"`; old artifacts load clean; E4 smokes green post-normalization.

## Unit 3 — element `water` → `ice` + cold/frost register (DESIGN change, RULED EL2; rocket leads · gamora + star-lord touches)

Matt verbatim: *"let's change our water element to Ice and adopt the cold/frost ailment. The genre's corpus has spoken."* The locked-8 amends substrate-led: **fire · ice · earth · wind · lightning · holy · shadow · physical**. Corpus evidence: 38 cold/frost kits, zero "water" kits — RDR's "water" was the genre outlier name.

**Design content of the rename (rocket drafts, gandalf reviews the register surfaces):**

- `config/elements.yaml` water entry → `name: ice`, `display: Ice`, **`ailment: chill` UNCHANGED** — chill (soft_control slow, 20–50%) already IS the genre's cold/frost ailment mechanically; EL2's "adoption" lands as the register confirmation, not a new mechanic. Description/`theme_tags` re-register: propose `[cold, preservation, stillness]` (preservation carries over from water — ice preserves; `flow`/`depth` retire). `color_range [560000, 700000]` (blue band) KEEPS — ice-coherent.
- `config/substrate_identities/water.yaml` → `ice.yaml` (file rename + identity-declaration content pass; PREFER/AVOID lists re-read under ice register).
- `config/ailments.yaml` chill entry: description pass only — re-register as the cold/frost ailment ("chill/freeze register"); **parameters untouched**.
- `generation/season_generation_pipeline.py::STAT_ELEMENT_POOLS`: INT pool → `["fire", "ice", "lightning", "shadow"]` (the classic mage quartet — Matt-noted); DEX 8-pool + `_ALL_8_ELEMENTS` likewise.
- **Census scale:** ~114 `"water"` literals across src (generation 23 · simulation 8 · telemetry 5 · export 5 · llm 4 · foundation 3 · element 2 · canonical 1) + **58 test files** + config + `element/schema.py`/`selector.py`. Seam split: rocket = generation/element/anchor/foundation/canonical/config · gamora = simulation (resistance_matrix, combatant, damage_resolver, spatial) · star-lord = llm (naming, cosmological_vocabulary, spirit_guide_voice, phase5), telemetry, export.
- **Element-name vocab pools (data-side, small, non-blocking):** D1 pools carry `element=water` rows → ice register. Flag for the pool pass: **`rime` re-promotion** (demoted vocab-obscure 2026-05-12 under the water register; under an ice register rime is register-coherent) = **Matt one-word call** — queue it in the dispatch report, don't block on it.
- **Explicitly OUT of scope:** freeze-as-hard-control escalation (routes to ailment-layer design with the thematic-ailment-signatures proposal — gandalf's queue) · retro-pinning corpus cold kits to Ice (Matt's free-axis aside: *"if we run enough iterations across time, we will see these kits in their Ice Elemental version"*) · any resistance-value or pool-probability change.
- **Downstream flag (not in critical path):** drax consumes element labels/colors in loadout/demo/godot — KR queues a drax follow-on pass after engine lands. elrond schema note already filed separately (`elem_raw` provenance-only).
- **Acceptance:** live code + config speak `ice`; read-compat normalizer at load boundaries (`"water"` → `"ice"`); historical artifacts untouched; tests green (58 files updated); MIGRATION.md documents the semantic shift + INT-pool reading.

## Recommended sequencing (KR decides)

1. **Wave 1 — Unit 1** (chain): small, independent, fires now.
2. **Wave 2 — Unit 3** (ice): the substantive one; rocket-led with gamora/star-lord sub-dispatches; own tag.
3. **Unit 2** (instant): HELD behind the E4 Gate-2 decision (Hazard 2). KR folds or sequences after.

**Report-back:** ≤200-word status per wave to Matt; gandalf review requested on the Unit-3 register surfaces (elements.yaml prose, theme_tags, substrate-identity content) before Gate-2.
