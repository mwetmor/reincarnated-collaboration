# MIGRATION — Catalogue Data Layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema migrations for non-engine data layers under `agentic_orchestration/research/curated/`. Currently: catalogue.db + (NEW v1.8 / v1.9) engine `data/kit_space/` chronicle (cross-seam co-ownership with star-lord per LOCK K).
**Pattern:** parallels star-lord's engine-side `MIGRATION.md` files per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

---

## v1.12 — synty_catalogue.db schema 1.1→1.2: gandalf axis-3/4 rep-audit curation (Option A consumption rule + frontier-western value-split) — 2026-06-17

### What changed (one line)

gandalf curated elrond's axis-3/4 PROPOSALS at the semantic-layer rep-audit (ruling `agentic_orchestration/gandalf/notes/2026-06-17-synty-gear-spec-upstream-wiring-ruling.md` §1.3/§1.4/§1.6, closing Q2 gate 1 of the Synty gear-spec upstream-wiring call). Axis 3 (`time_period`): **ACCEPTED as-proposed — no change.** Axis 4 (`cultural_identity`): **TWO additive corrections** materialized here — (1) the **Option A consumption rule** (read-time binding gate, NOT a data migration) and (2) the **`modern-western` → `frontier-western` value-split** (touches data, additively). synty_catalogue internal schema_meta `1.1 → 1.2`. **No schema-column churn, no destructive change.**

### Correction 1 — Option A consumption rule (READ-TIME gate; ruling §1.3 / §1.6) — NOT a data migration

gandalf ruled **Option A** over Option B (physical column split): the `cultural_mode_flag` column (written at 1.1) **already partitions** the rows, so the fix is a consumption rule, not a migration. **Nothing in the data changes.** The durable rule:

> `cultural_identity_proposed` is binding as a **cultural-tradition substrate ONLY for rows where `cultural_mode_flag ∈ {A, B}`.**
> - **Mode A/B** → the value IS a cultural-tradition read (egyptian, east-asian, norse, greco-roman, w-euro-medieval, **frontier-western**). Bind it.
> - **Mode C** → the value is a `register_default_skin` (genre-default: generic-fantasy / sci-fi / modern-western-urban — **NOT a culture**).
> - **Mode D** → null cultural read (nature biomes).
> - **unresolved** (`?`) → no cultural home; do NOT force one.

Downstream cultural-rotation / faction surfaces (the `canonical/48` seasonal-rotation operator; any Fate-genre faction-architecture surface) read cultural-tradition **ONLY from Mode-A/B rows**, and never inherit `generic-fantasy` / `sci-fi` / `modern-western` as a culture. This is the exact **Mode-C artifact** the §4.4 rep-audit discipline exists to catch — a label that passes the name-token vote but fails semantic cultural-coherence (the S.-American-Indigenous-Shotgun-Cluster failure mode).

**Recorded durably in three places** (the .db is gitignored — script + this entry are the committed source-of-truth): (a) the `CULTURE_BINDING_MODES` constant + `is_cultural_tradition_binding()` helper + `CONSUMPTION RULE` docblock in `scripts/tag_synty_multiaxis_2026_06_17.py`; (b) a quoted CONSUMPTION-RULE block atop the **Axis 4** section of the regenerated `multiaxis-tags-2026-06-17.md`, which now renders Mode-A/B (binding) strata separately from Mode-C/D (non-binding); (c) this MIGRATION entry. **No column added, no row re-typed for this rule** — it is read-time semantics over existing data.

### Correction 2 — `modern-western` homonym split → `frontier-western` (ruling §1.4) — additive, touches data

`modern-western` was a homonym doing double duty: **Mode-B** (Western Frontier / Western Pack = the American-frontier cultural tradition, cowboys — a REAL cultural read) vs **Mode-C** (Apocalypse / City / Battle Royale = modern-western-urban register-default). The Mode-B rows are split to the new value **`frontier-western`** (cultural-tradition); the Mode-C rows retain **`modern-western`** in the register-default sense (already de-fanged by Option A's mode gate).

**Verified row count (ruling estimated ~2): exactly 2 Mode-B rows split** —

| collection_id | pack | 1.1 value | 1.2 value | mode |
|---|---|---|---|---|
| 154809 | `POLYGON - Western Frontier Pack` | `modern-western` | **`frontier-western`** | B |
| 154810 | `POLYGON - Western Pack` | `modern-western` | **`frontier-western`** | B |

The 30 Mode-C `modern-western` rows (Apocalypse / City / Battle Royale / Apocalypse-HUD / Military-Combat-HUD …) are **unchanged**. Post-split authoritative field-value counts (verified against the regenerated JSONL, by field value not substring): `frontier-western` = **2** (both mode B); `modern-western` = **30** (all mode C); 157 total rows preserved. `cultural_basis` on the 2 split rows updated to name the new value + cite the ruling (descriptive text, not identity).

### Reversibility / regeneration (source-anchored discipline)

`synty_catalogue.db` stays **gitignored** (`curated/.gitignore` ignores `*.db`). The value-split is encoded in the `western` entry of `CULTURE_RULES` in `scripts/tag_synty_multiaxis_2026_06_17.py` (`("western", "frontier-western", "B", …)`), so a **from-scratch deterministic rebuild lands directly at the curated 1.2 state** — the curation is reproducible from committed source, not a one-off DB mutation:
```
python3 build_synty_catalogue_2026_06_17.py full      # WAVE 1 (136 zip packs)
python3 build_synty_catalogue_2026_06_17.py nonfbx    # WAVE 2 (21 extracted packs)
python3 tag_synty_multiaxis_2026_06_17.py all          # 5-axis tag + gandalf-curated axis-4 (1.2) + regen JSONL/MD
```
The live DB for this entry was updated surgically (a 2-row additive `UPDATE` + schema_meta 1.2 row) rather than a full re-tag, to keep the touch minimal; the script reproduces the identical curated state on any clean rebuild. The `tag … all` schema_meta insert records BOTH the 1.1 (multi-axis) and 1.2 (curation) version rows for lineage.

### Deliverables touched

- `agentic_orchestration/research/scripts/tag_synty_multiaxis_2026_06_17.py` — `CULTURE_RULES` western entry → `frontier-western`; `CULTURE_BINDING_MODES` + `is_cultural_tradition_binding()` + CONSUMPTION-RULE docblock added; `NEW_SCHEMA_VERSION` 1.1→1.2; schema_meta now records both version rows; report renders Mode-A/B binding vs Mode-C/D non-binding strata + the Option A block.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.jsonl` — regenerated; the 2 Mode-B rows carry `axis4_cultural_identity_proposed='frontier-western'`.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.md` — regenerated; Axis 4 section carries the Option A consumption rule + value-split notes + binding/non-binding stratum split.
- `synty_catalogue.db` (gitignored) — 2-row value-split applied; schema_meta `1.2` row inserted.

### Downstream hooks

- **gandalf** — axis-3/4 curation now materialized; this closes the consumption-rule handoff from ruling §1.4/§5. The wiring-call half (fantasy-first + silhouette degrade) is gandalf/rocket-side, not in this data-layer entry. **gandalf holds the push** (ADR-006) — this entry is committed but NOT pushed by elrond.
- **Any cultural-rotation / faction-architecture consumer** — read cultural-tradition via `is_cultural_tradition_binding(cultural_mode_flag)` (i.e. `cultural_mode_flag IN ('A','B')`) before inheriting `cultural_identity_proposed`. Mode-C is `register_default_skin`, not a culture.
- **Incorporation ledger** — unchanged; no incorporation event in this entry.

---

## v1.11.1 — synty_catalogue.db WAVE 2: 21 extracted-unitypackage packs indexed (no schema change) — 2026-06-17

### What changed (one line)

The 21 no-FBX Synty packs (variant=Unity, native `has_fbx=0`) were downloaded as `.unitypackage` files and **knight-rider extracted their meshes into a LOOSE FBX TREE** (not zips) at `~/Games/synty-corpus/nonfbx_extracted/<PACK_FOLDER>/Assets/Synty/.../Models/*.fbx` (8,655 FBX + 11,930 textures, 2.8 GB). The populate script gained a **second scan path** (`nonfbx` mode — walks the directory tree instead of `unzip -l`-ing zips) and a WAVE-2 classifier (`classify_asset_loose`). All 21 packs + 8,655 mesh assets are now indexed. **No schema change** — `packs`/`assets`/`textures`/`schema_meta` are unchanged at v1.0; this is a pure data-population pass keyed on the existing `(collection_id, download_id)` identity, so it is idempotent and additive to the WAVE-1 136 packs (which stay untouched).

### Catalogue totals after WAVE 2

- **Packs: 157** (136 WAVE-1 zip-backed `source='synty-store'` + 21 WAVE-2 loose-tree `source='synty-store-unitypackage'`).
- **Assets: 62,281** (53,626 WAVE-1 + 8,655 WAVE-2).
- **structural_class: 156 monolithic / 1 modular** (the lone modular pack remains the WAVE-1 Modular Fantasy Hero pack; all 21 WAVE-2 packs are monolithic — none ship per-slot body parts or `_Texture_Mask`).

### Integrity (path-index + count check) — PASS

Every WAVE-2 `assets` row resolves to a real file under `nonfbx_extracted/`: **8,655 paths checked, 0 misses.** Per-pack FBX counts **match `~/Games/synty-corpus/extract.log` exactly for all 21 packs** (the integrity target). `verify` mode now runs both waves: WAVE-1 zip-backed (157→packs reported as 157 incl. WAVE-2 by the zip-existence pass, 0 zip-misses for WAVE-1 source) + WAVE-2 loose-tree (21 packs / 8,655 assets / 0 path-misses).

### WAVE-2 naming convention differs from WAVE-1 SourceFiles (why a second classifier)

Unity-export FBX lack the `SK_` skeletal prefix that the WAVE-1 SourceFiles packs use. The WAVE-2 conventions, all handled by `classify_asset_loose` (the WAVE-1 `classify_asset` is left untouched):

| WAVE-2 pattern | asset_type | note |
|---|---|---|
| `Characters.fbx` / `Generic_Characters.fbx` / `Characters_<Variant>.fbx` | character (slot=whole_character) | baked monolithic appearance-unit (Unity export bakes the whole char into one FBX) |
| `SM_(Gen_)Chr_Attach_*` | armor_part + **is_accent=1** | the silhouette-breaker accent layer — hats / hair / beards / masks / glasses |
| `SM_(Gen_)Wep_*` | weapon | |
| `SM_(Gen_)<Bld\|Env\|Veh\|Fol\|Tree\|Tile>_*` | environment | |
| `SM_(Gen_)<Prop\|Item>_*` | prop | |
| `SM_(Gen_)<UI\|FX\|...>_*`, `FX_*`, `Sphere*`, `Animations*` | other | |
| OLDER SIMPLE-line bare prefixes (`Building_`/`Vehicle_`/`Env_`/`road`/`Prop_`/`Item_`/`Sign*`…) | environment / prop | the SIMPLE packs predate the `SM_` prefix |
| `SI_Letter`/`SI_Symbol`/`SI_Number`/`*Icon` | other | Props-pack 2D-icon-as-mesh family |
| Shop-Interiors `SI_*` / Simple-Temples `ST_*` | prop | product-line prefixes (icon check fires first to resolve the `SI_` collision) |

### Provenance (source-anchored discipline)

Every WAVE-2 pack is stamped `source='synty-store-unitypackage'` (distinct from WAVE-1 `'synty-store'`) and `corpus_rel_path='nonfbx_extracted/<folder>'`; each pack `notes` records `extracted-from-unitypackage (variant=Unity, native has_fbx=0); meshes extracted by knight-rider 2026-06-17`. Each WAVE-2 asset `notes='extracted-from-unitypackage'`. The `has_fbx` flag stays **0** on these packs (it reflects NATIVE Synty variant availability per the manifest — these never shipped a native FBX SourceFiles download; the indexed meshes are extracted, not native). `has_unity=1`. This keeps the variant-availability columns truthful while the path index points at the extracted tree.

### Survey-accurate findings (reporting what EXISTS, not what "should" be there)

- **POLYGON MINI - Fantasy Pack ships ZERO character meshes** in this extraction. The dispatch hint listed it character-relevant (`Generic_Characters.fbx` expected), but the extracted tree is entirely `SM_Bld_*` / `SM_Tile_*` / `SM_Env_*` / `SM_Prop_*` + FX (892 FBX, 0 character, 0 accent). It populates as an environment/prop pack — which is what is actually on disk. (The MINI product-line character minis were evidently not in this no-FBX Unity download.)
- **The shared `PolygonGeneric` module rides along in nearly every POLYGON pack.** Even environment-leaning packs (Nature Pack) carry `Generic_Characters.fbx` (1 character mesh) + ~22 `SM_Gen_Chr_Attach_*` generic accents because the Generic module is bundled. This produces a baseline of ~1 generic character + ~22 generic accents per POLYGON pack on top of each pack's themed content. Kids Pack (184 accents) and Battle Royale (89) carry large pack-specific accent sets on top of the generic baseline.
- **No `_Texture_Mask` in any WAVE-2 pack** (verified) → all `recolor_scheme='whole_atlas_swap'`, consistent with the page-1 named monolithic packs. The per-region 5-zone mask lever stays unique to the WAVE-1 Modular Fantasy Hero pack.

### Regeneration

`synty_catalogue.db` stays **gitignored** (`curated/.gitignore` ignores `*.db`). Committed source-of-truth is the populate script + this MIGRATION entry. Full deterministic rebuild from on-disk corpus + committed manifest:
```
python3 build_synty_catalogue_2026_06_17.py full     # WAVE 1 (136 zip packs)
python3 build_synty_catalogue_2026_06_17.py nonfbx   # WAVE 2 (21 extracted packs)
```
Both modes are idempotent (upsert-keyed on `(collection_id, download_id)`); order-independent.

### Downstream hooks (unchanged from v1.11)

All WAVE-2 packs default `incorporation_status='NOT_INCORPORATED'`; `distinctiveness_score` NULL (galadriel's seam — hook only). No incorporation event has occurred.

---

## v1.11 — synty_catalogue.db landed (Synty 3D gear-substrate catalogue; NEW standalone DB) — 2026-06-17

### What changed (one line)

Created a **new standalone SQLite DB** `agentic_orchestration/research/curated/synty_catalogue.db` (schema v1.0) indexing the downloaded Synty FBX corpus — **136 FBX packs, 53,626 mesh assets** — as metadata + filesystem path index ONLY (bytes stay on disk in the corpus zips at `~/Games/synty-corpus/fbx/`; the DB never holds mesh bytes). Tables: `packs` (collection/variant/structural_class/recolor_scheme/license-incorporation ledger), `assets` (one row per FBX mesh; slot taxonomy + asset_type + distinctiveness hook), `textures` (recolor mask + palette-atlas index), `schema_meta`. Populate script: `agentic_orchestration/research/scripts/build_synty_catalogue_2026_06_17.py` (re-runnable: `schema|slice|full|verify|queries`).

### Why (one line)

Materializes the **gandalf §7.1 elrond acceptance hook** in `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` — the substrate catalogue + license ledger that resumes the deferred gear-spec generation design session. Dispatch: `agentic_orchestration/dispatches/2026-06-17-elrond-synty-catalogue.md` (Gate-1-cleared, 837dd7f).

### SEPARATE DB vs extend catalogue.db — decision + justification

**Decision: separate `synty_catalogue.db`, NOT an extension of `catalogue.db`.**

Rationale — the two catalogues have near-zero schema overlap and orthogonal shapes:
- `catalogue.db` is a **2D-sprite STYLE-RUBRIC** catalogue: six-axis pixel-art register scoring (resolution_band / palette_size / shading_technique / linework_style / animation_frame_density / derived_register), embodiment tags, abstraction groupings, multi-vendor `catalogue_sources` + `crawl_sessions` provenance. It answers *"what visual register is this 2D sprite asset?"*
- `synty_catalogue.db` is a **3D-FBX MESH** catalogue: per-mesh slot taxonomy, structural_class (monolithic vs modular), license incorporation ledger, recolor-lever class, filesystem path index into corpus zips. It answers *"which mesh fills which gear slot, and is it license-incorporated?"*

Forcing 3D-mesh fields onto the sprite-rubric tables (the six-axis CHECKs do not apply to FBX meshes; `crawl_sessions` is a Legolas-crawl construct that does not model a knight-rider corpus download) — or vice versa — would muddy both schemas and break the existing 2D consumers' assumptions. The **vendor-catalogue precedent already separates concerns by folder** (`research/catalogue/<vendor>/`); we separate by DB *file* here because the overlap is near-zero rather than partial. Cross-DB linkage, if ever needed, is by the stable string key `collection_id` (Synty's). This is the lower-coupling, lower-risk choice and preserves `catalogue.db`'s consumers untouched.

### Schema shape (v1.0)

- `packs` — `collection_id` + `download_id` (identity is the PAIR; a collection MAY ship >1 FBX download — Water Guns ships two), `collection_name`, `zip_name`, `corpus_rel_path`, `size_mb`; variant flags `has_fbx/has_unity/has_unreal/has_godot` (joined from `full-fbx-variant-manifest.jsonl`); `structural_class` ∈ {monolithic, modular}; `recolor_scheme` ∈ {per_region_mask, whole_atlas_swap, unknown}; license ledger `incorporation_status` (default `NOT_INCORPORATED`; `INCORPORATED` carries `incorporated_season` + ISO `incorporated_at`); `source`, `source_date`, `added_at`, `notes`.
- `assets` — one row per FBX mesh: `pack_id` FK, `zip_rel_path` + `member_path` + `file_name` (the path index — bytes resolve at `<corpus_root>/<zip_rel_path> :: <member_path>`, never in DB); `asset_type` ∈ {character, weapon, armor_part, prop, environment, other}; `slot` (nullable; monolithic→`whole_character`, modular→canonical slot, weapon→`weapon`, prop/env→NULL); `is_accent`, `is_modular_part`, `gender`; `distinctiveness_score` (**nullable hook — DO NOT populate; galadriel scores later per gandalf §7.4**); `added_at`, `notes`.
- `textures` — recolor mask + palette-atlas index per pack: `texture_role` ∈ {region_mask, palette_atlas, base_atlas, other}; `channel_region_map` JSON (modular pack's 5-zone RGB-corner scheme from galadriel slice-verification 2026-06-17 §3.1; semantic per-zone labels marked expected-but-unrendered per galadriel §5).

### Slot vocabulary — modular `Chr_<Slot>` → canonical slot mapping (gandalf open-question §2)

Reconciled the modular pack's raw token names to a clean canonical slot set gandalf designs against:

| Synty modular token | canonical slot | layer |
|---|---|---|
| Torso | chest | body |
| Hips | hips | body |
| LegLeft / LegRight | leg_l / leg_r | body |
| ArmUpperLeft/Right | arm_upper_l / arm_upper_r | body |
| ArmLowerLeft/Right | arm_lower_l / arm_lower_r | body |
| HandLeft / HandRight | hand_l / hand_r | body |
| Head | head | body |
| Hair / FacialHair / Eyebrow / Ear | hair / facial_hair / eyebrow / ear | cosmetic |
| HeadCoverings | head_covering | **accent** |
| HelmetAttachment | helmet_accent | **accent** |
| ShoulderAttachLeft/Right | shoulder_accent_l / shoulder_accent_r | **accent** |
| ElbowAttachLeft/Right | elbow_accent_l / elbow_accent_r | **accent** |
| KneeAttachLeft/Right | knee_accent_l / knee_accent_r | **accent** |
| HipsAttachment | hips_accent | **accent** |
| BackAttachment | back_accent | **accent** |

Accent slots are flagged `is_accent=1` — they mount to the rig's named `All_NN_` sockets (galadriel §2) and are the silhouette-breaker layer (gandalf §3.6 "accents SECOND"). Monolithic packs' named-character capes (`SK_Chr_<Name>_Cape_NN`) are also classed `back_accent` (a hint of accent-modularity even in the silhouette lane).

### Galadriel slice-verification (2026-06-17) findings folded in

- **`recolor_scheme` per-pack field** captures galadriel's load-bearing §3.3 bifurcation: the per-region `_Texture_Mask` lever is **modular-pack-specific** (Modular Fantasy Heroes = `per_region_mask`); page-1 named-character packs (Adventure, Fantasy Kingdom, Samurai) ship coarser whole-atlas palette-swaps = `whole_atlas_swap`.
- **CAVEAT for consumers:** 15 packs carry `recolor_scheme=per_region_mask` because they *ship a mask texture*, but most are **environment** packs (Dungeon, Horror Asylum, Palm City, Sci-Fi Worlds, etc.) whose masks recolor props, NOT character armor. For the **armor restyle lane** specifically, only the **Modular Fantasy Hero Characters** pack's mask is character-relevant (it is also the sole `structural_class=modular` pack). Filter on `structural_class='modular'` (not `recolor_scheme`) to isolate the per-region armor-recolor lane. This is survey-mode accurate: the field reports what EXISTS (a mask ships), not what it is FOR.
- **`textures.channel_region_map`** carries the modular pack's verified 5-zone RGB-corner scheme (WHITE/CYAN/BLUE/YELLOW/MAGENTA); per-zone semantic labels (primary/secondary/metal/leather/accent) marked expected-but-unrendered per galadriel §5 — galadriel locks them on a later render pass.
- **distinctiveness_score** left NULL across all 53,626 assets — galadriel's seam (§7.4), hook only.

### Who's affected

- **Gandalf** — design-resumption consumer. The slice checkpoint (5 packs: Adventure, Fantasy Kingdom, Samurai, Modular Fantasy Heroes, Bow and Crossbow) + galadriel's geometry verdict clear the §4 resumption gate. The full 136-pack catalogue is the substrate for the §7.6 StyleProfile output-shape ruling. Slot vocabulary + structural_class + recolor_scheme are the design-facing fields.
- **Galadriel** — distinctiveness scoring (§7.4): `assets.distinctiveness_score` is the nullable target column; runs on a working subset, not the full corpus. The per-zone semantic-label render pass (§5 follow-up) updates `textures.channel_region_map`.
- **Knight-rider** — second-wave hook: the 21 no-FBX `.unitypackage` extractions (in progress, `~/Games/synty-corpus/nonfbx/`) populate as a clean second `full` pass once extracted to FBX (the populate script is re-runnable + upsert-keyed on (collection_id, download_id), so a second pass is idempotent for existing packs + additive for new ones).
- **Rocket** — L2 restyle leaf (§7.2): the modular pack's slot set + mask scheme are the build target; reads `synty_catalogue.db`, no write dependency.
- **Star-lord** — engine telemetry NOT affected. This is a standalone research catalogue; no telemetry table / fixture / export key touched (Principle 6 round-trip: not applicable, confirmed by KR at dispatch authoring).

### License incorporation ledger semantics (Matt stipulation)

Every pack defaults `incorporation_status='NOT_INCORPORATED'`. Assets not INCORPORATED before the Synty-Pass subscription lapses cannot be used afterward. The stamp path (smoke-tested): `UPDATE packs SET incorporation_status='INCORPORATED', incorporated_season='<season/build>', incorporated_at='<ISO>' WHERE …`. All 136 packs are NOT_INCORPORATED at landing (no incorporation event has occurred).

### Path-index integrity

`verify` pass: **136 packs, 53,626 assets, 0 zip-misses** — every `packs.zip_name` resolves to a real file on disk. (Asset-level paths are zip MEMBERS verified via `unzip -l` at index time; the zip-existence check is the on-disk integrity gate since members are not extracted.)

### DB is a build artifact (gitignored; regenerable — matches catalogue.db precedent)

`synty_catalogue.db` is **gitignored** (`curated/.gitignore` ignores `*.db`), exactly as `catalogue.db` is. The committed source-of-truth is the **populate script** `agentic_orchestration/research/scripts/build_synty_catalogue_2026_06_17.py` + this MIGRATION entry. The DB regenerates deterministically from the on-disk corpus + the committed `full-fbx-variant-manifest.jsonl` via `python3 build_synty_catalogue_2026_06_17.py full`. This honors the reversibility principle (curation reproducible from raw input) and the existing vendor-catalogue precedent (schema/script committed, `.db` regenerable). A consumer that needs the DB and does not have the local corpus should request the regenerated `.db` or the corpus location from elrond.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. New standalone DB; relationship to `catalogue.db` documented above (separate, low-coupling, cross-link by `collection_id`).
- **Cross-seam contract change?** No — standalone research catalogue; no engine-telemetry / fixture / export-key change (KR-confirmed not-applicable at dispatch authoring).
- Push to remote deferred to Matt's gate (auto-commit fired per team commit discipline).

---

## v1.10 — kit_star_sign_assignments.json sidecar landed (kit-to-star-sign MVP Phase 2) — 2026-06-09

### What changed (one line)

Landed `reincarnated-loadout/public/kit-space/kit_star_sign_assignments.json` (schema v1.0; artifact_kind `kit_star_sign_assignments`) — a parallel sidecar to `faction_assignments.json` carrying per-kit `star_sign_id` + `star_sign_name` + `star_sign_tradition` + `star_sign_assignment_method` (HAND_CURATED | RANDOM) + optional `hand_curated_anchor` for the active 37-kit corpus. Source corpus: Legolas 423-entry zodiac substrate at `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml`. 3 hand-curated overrides (Duskweaver→Mula; Cannonade Cleric→Krittika; Stonefist→Hercules per gandalf Phase 1 doc) + 34 deterministic-random assignments from a 394-entry filtered pool (29 high-flag-level entries deferred to gandalf review; 0 restricted).

### Why (one line)

Operationalizes the kit-binds-1:1-to-star-sign architectural commitment (Branch A half per Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09) at MVP scope per Matt 2026-06-09 directive ("3 kits map cleanly; rest random"); unblocks drax /forge cosmograph kits-as-constellations rendering + downstream mantis UE port WS1 DataTable ingestion of `star_sign_id` without pre-committing to full-corpus canonical semantic mapping methodology (deferred to Cycle 15+ Pattern B once empirical vertical-slice playtest informs).

### Who's affected

- **Drax** — `/forge` cosmograph consumer: read `public/kit-space/kit_star_sign_assignments.json` alongside existing `faction_assignments.json` + per-kit JSONs; `star_sign_id` is the FK into the Legolas zodiac corpus (sign_id key); `star_sign_name` + `star_sign_tradition` are denormalized for direct display without corpus-load dependency. Rendering kits-as-constellations is a separate Phase 5 or amendment dispatch — this MIGRATION lands the data surface, not the rendering.
- **Mantis (PC seam; downstream)** — UE port WS1 absorbs `star_sign_id` via DataTable ingestion when WS1 scope is authored. No immediate action; surface for awareness.
- **Gandalf** — design-review surface: 29 high-sensitivity-flag corpus entries deferred to gandalf review per dispatch § 3.4 (substrate-cleanliness-over-volume default applied). If gandalf reviews + decides any subset should be includable in the random pool, bump filter policy in script and re-run (deterministic; only affected RANDOM assignments shift).
- **Star-lord** — engine emit is NOT affected. The kit JSON files at `public/kit-space/kits/` were NOT modified (no kit regeneration triggered). Engine-side telemetry has no new write path.
- **Rocket** — engine-side generation has no new dependency. Kit corpus generation continues to emit the existing schema; the sidecar is purely an elrond-seam additive curation pass on top of generated kit IDs.
- **Knight-rider** — wave-close routing surface: this commission is the Phase 2 closure of dispatch `2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md`. Phase 1 (gandalf hand-curation) committed prior at `7d334d7`.
- **Legolas** — substrate-source-of-truth: 423-entry zodiac corpus is the canonical source-of-truth for sign_id resolution; future corpus updates (per-tradition additions; sensitivity-flag refinements) will require Phase 2 re-run to propagate.
- **Matt** — no action required; commission MVP scope satisfied per dispatch acceptance criteria.

### What downstream consumers need to do

**Drax (when /forge cosmograph rendering phase fires):**
1. Load `kit_star_sign_assignments.json` alongside `faction_assignments.json` (parallel sidecar pattern; same loading discipline)
2. Use `star_sign_id` as FK into Legolas corpus for full sign data (mythic_narrative, star_coordinates, asterism_schematic, etc.); use `star_sign_name` + `star_sign_tradition` denormalized fields for tooltip/label rendering without corpus dependency
3. Distinguish HAND_CURATED vs RANDOM assignments in UI presentation if narrative-richness emphasis is desired (e.g., HAND_CURATED kits get prominent star-sign narrative overlay; RANDOM kits get minimal sign-name binding)
4. The 3 HAND_CURATED mappings have `hand_curated_anchor` field referencing gandalf doc § anchors for traceability

**Mantis (when UE port WS1 commission fires):**
1. Add `star_sign_id` (string FK) + `star_sign_assignment_method` (enum string) columns to kit DataTable schema
2. Ingest from `kit_star_sign_assignments.json` at import time; reverse-lookup against zodiac corpus for full sign data
3. No engine-side runtime LLM dependency (D7 AI-tell line preserved)

**Gandalf (downstream review of deferred high-flag-level entries):**
1. Review the 29 high-sensitivity-flag corpus entries (any of the 423 zodiac entries with `cultural_sensitivity.flag_level == "high"`)
2. Per-entry include/exclude decision; for any entries promoted from deferred to eligible, document rationale per Discipline #25 (semantic-layer rep-audit) and bump script `ELIGIBLE_FLAG_LEVELS` or `DEFERRED_FLAG_LEVELS` constants accordingly
3. Re-run script; deterministic — only RANDOM-method assignments shift (HAND_CURATED unaffected)

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema):** sidecar pattern parallels the established `faction_assignments.json` precedent (event_id `kse_20260602_008`); no NEW cross-seam contract — same sidecar discipline as cycle-18 Issue 5A. No Matt re-approval required; covered by parent dispatch `2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md` authorization (Matt 2026-06-09 directive).
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the requirement. Drax-side does not need a parallel MIGRATION; consumption is loadout-app data-ingestion (parallel to existing faction_assignments.json consumption pattern). Mantis-side adds a MIGRATION when WS1 ingestion lands.
- **ADR-006 (external-systems writes require authorization):** the write is to a meta-repo-adjacent loadout-public asset under elrond-domain authority for catalogue/abstraction-analysis data. Push to remote remains Matt-explicit-authorization per CLAUDE.md addendum; this entry covers auto-commit only.
- **Discipline #59 (substrate-coverage honesty):** flagged in close report — random assignment WILL produce kit-pairs sharing the same star_sign_id (birthday-paradox math: 34 picks from 394 pool → ~1.5 expected collisions). Two collision-pairs observed empirically (`andean-001 Yacana` hit by fire_000006 + wind_000004; `aztec-tonalpohualli-004 Cuetzpallin` hit by physical_000019 + water_000006; `iau-constellations-033-dorado` hit by physical_000014 + wind_000005; `western-zodiac-005 Leo` hit by earth_000006 + wind_000006). Uniqueness was NOT a dispatch requirement — many-to-one mapping is architecturally acceptable at MVP scope (cosmograph visualization layer; multiple kits can orbit one star-sign). Surfaced as observation for Phase 3 design review.

### Open follow-ons (not blocking the lock)

1. **Gandalf review of 29 high-flag-level deferred entries** — non-blocking; default exclusion preserved substrate-cleanliness; review can promote subset to eligible if appropriate per culture-specific assessment; re-run script propagates.
2. **Cycle 15+ Pattern B canonical semantic mapping** — replaces RANDOM assignments with semantic methodology (similarity / curated rule-table / hybrid) per dispatch § 1; gated on vertical-slice spike playtest empirical signal informing methodology choice.
3. **Star-sign-to-kit reverse-mapping** — out of scope per dispatch § 6; can be derived at query time from forward mapping if needed by drax /forge.
4. **Seasonal-substrate-rotation operator integration** — per atomic-substrate-registry Layer 0.5; the 3 hand-curated mappings have per-season cultural-variant alternatives documented in gandalf Phase 1 doc § 4.3 (Krittika → Pleiades/Matariki/Mǎo; Hercules → Gilgamesh/Thor/Bhima; Mula → Ketu/Scorpius/Andean dark-cloud). Operator design is downstream of this MVP.
5. **Cross-tradition collision-handling** — the 4 observed RANDOM-collision pairs are MVP-acceptable but worth surfacing if cosmograph visualization makes the same-star-sign coupling visually awkward; uniqueness constraint can be added in a future re-run if desired (constrained random sampling without replacement up to pool size).

---

## v1.9 — EAA-4 chronicle implementation slice — `kit_space_chronicle.json` source-of-truth landed + smoke 9/9 PASS — 2026-06-02

### What changed (one line)

Implemented the EAA-4 chronicle source-of-truth layer per the v1.8 joint design verdict: authored `CHRONICLE_SCHEMA.md` v1.0 (per-event entry shape + 4-field lineage_tags substructure + emit-order discipline) at `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`, landed empty `kit_space_chronicle.json` source-of-truth file ready for EAA-5 first-fire, landed kit_space/ directory layout (`README.md` + `kits/` empty dir), authored smoke-test script verifying 9/9 round-trip checks PASS (TempDir + live), verified cleanup discipline (live dir returns to clean ready state).

### Why (one line)

Operationalizes the v1.8 joint design verdict for the EAA-4 chronicle-implementation slice specifically (the v1.8 entry authored the joint EAA-3 + EAA-4 design + format locks + shadow-table DDL; this entry lands the chronicle source-of-truth surface + smoke-test that downstream — EAA-5 first-fire — consumes); composes natively with EAA-3 per-kit JSON (rocket) on the locked FK format (`kse_<YYYYMMDD>_<seq3>`).

### Who's affected

- **Star-lord** — engine emit integration (per CHRONICLE_SCHEMA.md § 5 emit-order discipline): mint `event_id` per joint spec § 1.3 → append chronicle event entry FIRST to `kit_space_chronicle.json` (atomic write) → emit per-kit JSONs SECOND. Engine-side companion MIGRATION.md entry SHOULD be authored at `reincarnated-engine/src/reincarnated/output/MIGRATION.md` or `export/MIGRATION.md` when emit-integration commit lands.
- **Rocket** — EAA-3 per-kit JSON schema MUST adopt the locked FK format for `kit_space_expansion_event_id` per joint spec § 1; per-kit JSON lands under `data/kit_space/kits/kit_<primary>_<seq6>.json` per joint spec § 5.
- **Drax** — EAA-7 engine page reframe (LOCK O scope): consumes `data/kit_space/kit_space_chronicle.json` via single `fetch()`; flat JSON shape per CHRONICLE_SCHEMA.md § 4. Not blocking EAA-5.
- **Elrond (self; future post-EAA-5)** — shadow-table CREATE + ingest scripts deferred to post-EAA-5 (the joint spec § 3.5 authored the DDL; ingest implementation fires when first real chronicle data exists). Rebuildable from filesystem per joint spec § 3.2.
- **Gandalf** — design steward; chronicle's `substrate_inputs_changed` + `event_scope` + `lineage_tags` fields surface design narrative for engine-page rendering (EAA-7). Not load-bearing at this phase.
- **Jack-ryan** — Gate-2 review on this implementation + v1.8 joint design + smoke results.
- **Knight-rider** — receives EAA-4 completion report; routes Gate-2.
- **Matt** — no action; LOCK K + cycle-push pre-authorized.

### What downstream consumers need to do

**Star-lord (REQUIRED before or coincident with EAA-5 fire):**
1. Implement emit-order discipline per CHRONICLE_SCHEMA.md § 5: chronicle entry FIRST → per-kit JSONs SECOND
2. Use joint spec § 1.3 reference impl for `event_id` minting: query chronicle for `prior_today_count`; `+1`; format `kse_YYYYMMDD_seq3`
3. Use atomic-write convention: write to `.tmp` → `os.replace`
4. Author engine-side companion MIGRATION.md entry per ADR-004 round-trip
5. Surface `engine_version_sha` as 7-char short (`git rev-parse --short=7 HEAD`)

**Rocket (REQUIRED for EAA-3 schema spec):** include `kit_space_expansion_event_id` field per joint spec § 4.1; format MUST match `^kse_\d{8}_\d{3}$`. Per-kit JSON lands at `data/kit_space/kits/<kit_id>.json`. Per-skill `flavor_decision` + `flavor_word_used` cross-coupling per EAA-1 § 3 + joint spec § 4.3.

**Drax (EAA-7 scope; not blocking EAA-5):** consume `kit_space_chronicle.json` via `fetch('/data/kit_space/kit_space_chronicle.json')`; render `events[]` via existing `EngineStatePipelineFlow` component pattern per LOCK O.

**Jack-ryan (Gate-2):** review chronicle schema (`reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`) + smoke results (9/9 PASS TempDir + 9/9 PASS live; cleanup verified clean state) + this v1.9 entry composing on v1.8 design verdict.

### Schema diff or example before/after

**Before this implementation slice:** v1.8 design verdict authored format locks + storage medium choice + shadow-table DDL; NO chronicle source-of-truth file existed; NO directory layout existed; NO smoke-test existed.

**After this implementation slice:**

```
reincarnated-engine/data/kit_space/
├── README.md                                # NEW; directory layout + consumer guide
├── chronicle/
│   └── CHRONICLE_SCHEMA.md                  # NEW; per-event entry schema v1.0 + emit-order discipline
├── kit_space_chronicle.json                 # NEW; empty source-of-truth (events: []) ready for first emit
└── kits/                                    # NEW; empty dir (EAA-3 populates per-kit JSONs; star-lord emit fills)
```

**Chronicle file shape (per joint spec § 3.4 + CHRONICLE_SCHEMA.md § 4):** `{schema_version, schema_notes, events: [event-entry...]}` where each event-entry has required fields `event_id`, `event_type`, `event_timestamp`, `event_date_utc`, `event_scope`, `substrate_inputs_changed`, `engine_version_sha`, `kit_ids_generated`, `kit_count`; optional fields `engine_version_full`, `skip_flags_active`, `lineage_tags`, `generation_parameters`, `substrate_trace_summary`, `notes`.

**Format locks (re-stating from joint spec § 1 + § 2; preserved verbatim):**

| Field | Format | Regex |
|---|---|---|
| `event_id` | `kse_<YYYYMMDD>_<seq3>` | `^kse_\d{8}_\d{3}$` |
| `kit_id` | `kit_<primary>_<seq6>` | `^kit_(fire\|water\|earth\|wind\|lightning\|holy\|shadow\|physical)_\d{6}$` |
| `primary_element` | lowercase canonical-7+1 | — |
| `period` | uppercase enum nullable | — |
| `engine_version_sha` | 7-char short SHA | `^[0-9a-f]{7}$` |

### Smoke-test results (Discipline #2)

Script: `agentic_orchestration/research/scripts/eaa_4_chronicle_smoke_2026_06_02.py`

Modes verified:
- `python3 eaa_4_chronicle_smoke_2026_06_02.py` — TempDir dry-run: **9/9 PASS**
- `python3 eaa_4_chronicle_smoke_2026_06_02.py --live` — write to live engine `data/kit_space/`: **9/9 PASS**
- `python3 eaa_4_chronicle_smoke_2026_06_02.py --cleanup-live` — remove smoke artifacts: **verified clean state** (chronicle returned to `events: []`; smoke kit JSON removed; ready for EAA-5)

Round-trip checks (all 9 PASS both TempDir + live):
1. event_id regex match (`^kse_\d{8}_\d{3}$`)
2. kit_id regex match (`^kit_(canonical-7+1)_\d{6}$`)
3. chronicle JSON round-trips through `json.load`
4. chronicle contains target event (event_id appended correctly)
5. chronicle event's `kit_ids_generated` contains kit_id
6. per-kit JSON exists + round-trips
7. per-kit FK matches chronicle event_id
8. per-kit `primary_element` matches kit_id encoding (FK integrity in two-direction)
9. chronicle `event_date_utc` matches event_id date segment (denormalization consistency)

Smoke uses reserved seq6 range (kit_shadow_999xxx) to avoid colliding with real generation; smoke kits + events tagged with sentinel `_smoke_test_stub: true` for safe cleanup identification.

### Storage medium decision (re-stating v1.8 joint spec § 3.1)

Per joint spec § 3.1: **Option α (source-of-truth) + Option β-light (analytical shadow)**.

- Option α: flat `data/kit_space/kit_space_chronicle.json` (this v1.9 implements)
- Option β-light: `engine_kit_space_events` + `engine_kit_index` in elrond's catalogue.db (DDL authored in joint spec § 3.5; ingest implementation deferred to post-EAA-5)

This v1.9 lands the source-of-truth surface only. Shadow-table CREATE + ingest scripts are queued for post-EAA-5 (when first real chronicle data exists to ingest).

### Backward compatibility

- This implementation is **NEW + ADDITIVE** per LOCK J + LOCK K
- Existing `seasons/season_*` (season_000001-200) preserved as historical per Path α — not migrated
- Engine emit branches on EAA-2 skip flags: skip-flags-active → emit to `data/kit_space/`; skip-flags-inactive → emit to legacy `seasons/season_*` per pre-EAA convention
- Drax consumes BOTH layouts; data-shape distinguishable by directory location
- Verified via smoke-test cleanup: live `data/kit_space/` returns to clean ready state (chronicle `events: []`); no irreversible state introduced

### Coordination with EAA-3 (rocket primary) — FK format compose

The locked FK format (`kse_<YYYYMMDD>_<seq3>`) is **shared verbatim** between EAA-3 per-kit JSON `kit_space_expansion_event_id` field and EAA-4 chronicle `event_id` field. Authoritative source: joint spec § 1. Rocket's EAA-3 schema spec MUST adopt this format. This v1.9 implementation respects the format; smoke-test verifies it.

A prior `eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md` doc was authored in parallel proposing an alternative `kse_<YYYYMMDD>_<HHMMSS>_<6hex>` format; that doc has been **SUPERSEDED** and now redirects to the joint spec as authoritative.

### Files committed (this v1.9 entry)

- `reincarnated-engine/data/kit_space/README.md` — NEW; directory layout + consumer guide + format-lock summary
- `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md` — NEW; chronicle schema v1.0 spec
- `reincarnated-engine/data/kit_space/kit_space_chronicle.json` — NEW; empty source-of-truth (`events: []`) ready for EAA-5
- `reincarnated-engine/data/kit_space/kits/` — NEW empty dir (rocket EAA-3 populates)
- `agentic_orchestration/research/scripts/eaa_4_chronicle_smoke_2026_06_02.py` — NEW; smoke-test (9/9 PASS verified)
- `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md` — SUPERSEDED (redirects to joint spec)
- `agentic_orchestration/research/curated/MIGRATION.md` — THIS entry (v1.9; composing on v1.8)

### Related canonical docs + disciplines

- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.4 (chronicle commitment)
- `agentic_orchestration/dispatches/2026-06-02-eaa-4-kit-space-chronicle-infrastructure.md` (this dispatch)
- `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md` (authoritative joint design verdict; v1.8 MIGRATION entry covers)
- `agentic_orchestration/qa/findings/2026-06-02-eaa-phase-1-batch-gate-1.md` (Phase-1 batch Gate-1; recommended amendment 2 — FK format coordination — fulfilled by joint spec + this implementation)
- `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md` (wave-open INFO-3 — per-kit engagement telemetry out-of-scope — respected in CHRONICLE_SCHEMA.md § 9)
- Discipline #2 (smoke-gate; 9/9 PASS satisfies), #6 (cross-seam contract; satisfied via joint spec + this v1.9 round-trip), #8 (schema validation at boundaries; chronicle schema versioned + atomic-write), #10 (attribution clarity; engine_version_sha + lineage_tags), #11 (empirical inspection; smoke verifies live dir state)
- ADR-004 (cross-seam MIGRATION) + ADR-006 (read-only-by-default external systems; engine owns kit_space/ writes; elrond owns catalogue.db shadow-table writes per joint spec § 3.5; no remote pushes from this step)

### Routing back to KR

- Joint design verdict v1.8 authored + LOCKED (FK format + kit_id format + storage medium + shadow-table DDL + 5 iteration points named for rocket EAA-3)
- Chronicle source-of-truth layer LANDED (CHRONICLE_SCHEMA.md + empty chronicle JSON + layout README)
- Smoke-test 9/9 PASS TempDir + 9/9 PASS live + cleanup verified clean state
- Live `data/kit_space/` ready for EAA-5 first-fire consumption (empty chronicle; star-lord emit-integration may co-fire with EAA-5)
- Cross-dispatch FK format LOCKED + SUPERSEDED-coord-doc redirects to joint spec
- Star-lord engine-emit integration (per CHRONICLE_SCHEMA.md § 5) is the named NEXT cross-seam touch; companion MIGRATION.md entry recommended on engine-emit commit
- Routing back: **proceed to jack-ryan Gate-2** on v1.8 joint design + v1.9 implementation slice + smoke results; EAA-4 acceptance criteria 1, 2, 4, 5, 6 satisfied; AC #3 (engine emit path) lands at star-lord integration

---

## v1.8 — EAA-3 + EAA-4 — engine kit_space shadow tables (engine_kit_index + engine_kit_space_events) — 2026-06-02

### What changed (one line)

Authored ELROND-SIDE schema for cycle-16 EAA-3 (per-kit JSON output) + EAA-4 (kit-space chronicle infrastructure) as joint cross-dispatch spec: locked `kit_id` format (`kit_<primary>_<seq6>`) + `kit_space_expansion_event_id` format (`kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>` per pre-existing coordination note at `cycle-16-eaa-engine-architectural-amendment/eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md`); chose Option α (filesystem source-of-truth at `reincarnated-engine/data/kit_space/`) + Option β-light (additive shadow tables `engine_kit_index` + `engine_kit_space_events` in curated catalogue.db) as analytical-index for cross-cutting joins; confirmed elrond ingest-compat against rocket DRAFT per-kit JSON schema with 5 iteration points named for joint resolution.

### Why (one line)

Operationalizes canonical record `2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 + § 3.4 (continuous kit space + parameter-expansion-event chronicle); replaces per-season manifest as engine output unit (additive; historical seasons preserved per Path α); composes EAA-3 + EAA-4 elrond-side decisions before either rocket spec (EAA-3) or elrond chronicle implementation (EAA-4) finalizes, per Phase 1 batch Gate-1 INFO-B amendment (jack-ryan).

### Who's affected

- **Rocket** — owns engine emit (per-kit JSON shape, EAA-3 primary); MUST consume FK format lock (§ 1 of joint spec note) + kit_id format lock (§ 2); MUST align engine-side enum casing on 5 iteration points named in joint spec note § 4.4 (primary_element lowercase / period uppercase enum / engine_version short-sha format / emit ordering chronicle-first / flavor_decision+flavor_word_used integrity at per-skill level).
- **Star-lord** — owns engine output pipeline (EAA-3 + EAA-4 co-owner on emit); MUST implement chronicle event emit FIRST then per-kit JSONs SECOND (atomicity discipline § 5 of joint spec note); MUST emit `engine_version` short-sha consistently; MAY trigger elrond shadow ingest as post-emit hook.
- **Drax** — LOCK O scope (EAA-6 + EAA-7); consumes kit space output + chronicle for loadout app + engine page reframe; NOT impacted by this MIGRATION (consumption deferred to those workstreams).
- **Gandalf** — design steward; new chronicle event log provides design-narrative substrate for engine page + Realm-Expansion-targeting-underplayed-kits future workstream; new shadow tables enable cross-cutting analytical queries.
- **Jack-ryan** — Gate-2 review (BLOCK authority) on EAA-3 + EAA-4 schema spec including this MIGRATION; verifies FK format consistency across dispatches + LOCK K ADDITIVE-AND-REVERSIBLE discipline + cross-seam contract reversibility.
- **Knight-rider** — receives report-back; routes Gate-2; sequences EAA-5 first-fire to consume EAA-3 + EAA-4 infrastructure.
- **Legolas** — no action.
- **Matt** — LAST-resort escalation if (a) rocket DRAFT diverges substantially from joint spec § 4 on any of 5 iteration points AND iteration cycle fails to converge OR (b) cross-seam contract reversibility surfaces unexpected coupling.

### What downstream consumers need to do

**Rocket (EAA-3 implementation):**
- Author per-kit JSON schema as DRAFT (per joint spec note § 4); iterate against five iteration points if engine-side surfaces divergence
- Engine-side `primary_element` enum: lowercase canonical-7+1 only (`fire`, `water`, `earth`, `wind`, `lightning`, `holy`, `shadow`, `physical`)
- Engine-side `period` enum: uppercase WS2.P2 substrate values (`ANCIENT`, `MEDIEVAL`, `MODERN`) when populated; nullable when substrate doesn't supply
- Engine emit `kit_id` using `mint_kit_id(primary, prior_primary_count)` rule (joint spec § 2.4)
- Engine emit `kit_space_expansion_event_id` using `mint_kit_space_expansion_event_id(event_date_utc, prior_today_count)` rule (joint spec § 1.3)
- Engine emit `lineage_tags` 4-field substructure: `kit_space_lineage` / `engine_provenance` / `substrate_provenance` / `generation_cohort_date`

**Star-lord (EAA-3 + EAA-4 emit pipeline):**
- Implement emit-order discipline: chronicle event entry FIRST, then per-kit JSON entries (so FK target exists in chronicle when shadow ingest runs)
- Implement chronicle JSON shape per joint spec § 3.4 (events array; schema_version present)
- Source `engine_version_sha` from `git rev-parse --short=7 HEAD` at fire-time; commit at emit-time
- Path discipline: `data/kit_space/kit_space_chronicle.json` + `data/kit_space/kits/<kit_id>.json` per kit; optional `data/kit_space/kits_index.json`

**Elrond (this MIGRATION + EAA-3/4 implementation):**
- Author shadow-table CREATE script (DDL at joint spec § 3.5)
- Author ingest script: walks `data/kit_space/`; upserts to `engine_kit_index` + `engine_kit_space_events`; tolerates partial emissions (skips kit if FK target missing; surfaces warning)
- Rebuildable: truncate + reload = deterministic
- Smoke-test against EAA-5 first-fire output (joint spec § 7)

**Drax / Gandalf (no immediate action; future workstreams):**
- Drax EAA-6 (loadout MVP) + EAA-7 (engine page MVP) consume kit space + chronicle via LOCK O existing-components-only discipline; deferred
- Gandalf has new analytical surface for substrate-led discipline at content-engagement layer (Disc #41 composition; future Realm Expansion targeting underplayed-kit telemetry)

### Schema diff or example before/after

**Old (per-season manifest path; legacy; PRESERVED for historical seasons per Path α):**
- `seasons/season_NNNNNN/manifest.json` — per-season summary + theme element + cosmological_vocabulary + class JSON refs
- `seasons/season_NNNNNN/classes/class_NNNN.json` — per-class skill + stat data; season-anchored numbering
- No cross-file foreign key; class id is season-scoped

**New (per-kit + chronicle path; ADDITIVE; emitted when EAA-2 skip flags active):**
- `data/kit_space/kit_space_chronicle.json` — append-only event list; `events: [{event_id, event_type, event_timestamp, event_scope, substrate_inputs_changed, engine_version_sha, kit_ids_generated, kit_count, skip_flags_active, lineage_tags}]`
- `data/kit_space/kits/kit_<primary>_<seq6>.json` — per-kit; `{kit_id, primary_element, cultural_tradition, period, chain_composition, t4_selection, supporting_chain, skills, emergent_kit_concept, substrate_trace, kit_space_expansion_event_id, engine_version, generation_timestamp, lineage_tags}`
- Foreign key: per-kit `kit_space_expansion_event_id` → chronicle `event_id` (format: `kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>`; regex `^kse_\d{8}_\d{6}_[0-9a-f]{6}$`; per pre-existing coordination note)
- Per-skill EAA-1 metadata: each `skills[]` entry carries `flavor_decision: bool` + `flavor_word_used: str | null` (cross-coupled per EAA-1 § 3 plus joint spec § 4.3)

**New shadow tables (elrond catalogue.db; ADDITIVE; rebuildable from filesystem):**

```sql
-- engine_kit_space_events: per-chronicle-event row indexed by event_id
CREATE TABLE engine_kit_space_events (
    event_id                TEXT PRIMARY KEY,                      -- kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>
                                                                   -- regex: ^kse_\d{8}_\d{6}_[0-9a-f]{6}$ (27 chars)
    event_uuid_full         TEXT,                                  -- full UUID4 source for the 6-char-hex suffix (nullable; provenance trace)
    event_type              TEXT NOT NULL DEFAULT 'kit-space-expansion'
                            CHECK (event_type IN ('kit-space-expansion', 'realm-expansion', 'reserved-future')),
    event_timestamp         TEXT NOT NULL,                         -- ISO-8601 UTC
    event_date_utc          TEXT NOT NULL,                         -- ISO date
    event_scope             TEXT NOT NULL,
    substrate_inputs_changed_json TEXT NOT NULL,
    engine_version_sha      TEXT NOT NULL,
    engine_version_full     TEXT,
    kit_count               INTEGER NOT NULL CHECK (kit_count >= 0),
    skip_flags_active_json  TEXT,
    lineage_tags_json       TEXT,
    source_chronicle_path   TEXT NOT NULL,
    ingest_timestamp        TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_kse_event_date ON engine_kit_space_events(event_date_utc);
CREATE INDEX idx_kse_event_type ON engine_kit_space_events(event_type);

-- engine_kit_index: per-kit row indexed by kit_id
CREATE TABLE engine_kit_index (
    kit_id                          TEXT PRIMARY KEY,                  -- kit_<primary>_<seq6>
    primary_element                 TEXT NOT NULL
                                    CHECK (primary_element IN ('fire', 'water', 'earth', 'wind', 'lightning', 'holy', 'shadow', 'physical')),
    cultural_tradition              TEXT,
    period                          TEXT
                                    CHECK (period IS NULL OR period IN ('ANCIENT', 'MEDIEVAL', 'MODERN')),
    emergent_kit_concept            TEXT,
    chain_composition_json          TEXT,
    t4_selection_json               TEXT,
    supporting_chain_json           TEXT,
    skill_count                     INTEGER NOT NULL CHECK (skill_count >= 0),
    skills_summary_json             TEXT NOT NULL,
    substrate_trace_json            TEXT NOT NULL,
    kit_space_expansion_event_id    TEXT NOT NULL REFERENCES engine_kit_space_events(event_id),
    engine_version_sha              TEXT NOT NULL,
    generation_timestamp            TEXT NOT NULL,
    lineage_tags_json               TEXT,
    source_kit_json_path            TEXT NOT NULL,
    ingest_timestamp                TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_kit_primary ON engine_kit_index(primary_element);
CREATE INDEX idx_kit_event ON engine_kit_index(kit_space_expansion_event_id);
CREATE INDEX idx_kit_period ON engine_kit_index(period);
CREATE INDEX idx_kit_cultural_tradition ON engine_kit_index(cultural_tradition);
```

**schema_meta entry:**
```sql
INSERT INTO schema_meta (version, applied_at, description) VALUES (
    'v1.8-eaa-3-plus-4-engine-kit-shadow-tables',
    CURRENT_TIMESTAMP,
    'EAA-3 + EAA-4: engine_kit_index + engine_kit_space_events shadow tables; additive; rebuildable from kit_space/ filesystem; source-of-truth lives at reincarnated-engine/data/kit_space/*.json.'
);
```

### Format locks (cross-dispatch coordination per Phase 1 batch Gate-1 INFO-B amendment)

**LOCKED jointly between EAA-3 (rocket) + EAA-4 (elrond) per LOCK K:**

| Field | Format | Owner |
|---|---|---|
| `kit_id` | `kit_<primary>_<seq6>` (e.g., `kit_shadow_000001`) | elrond decision per LOCK K; rocket implements emit |
| `kit_space_expansion_event_id` | `kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>` (e.g., `kse_20260602_143052_a1b2c3`); per pre-existing coordination note | elrond decision per LOCK K (pre-existing coordination artifact); rocket + star-lord implement emit |
| `primary_element` | lowercase canonical-7+1 (`fire`, `water`, `earth`, `wind`, `lightning`, `holy`, `shadow`, `physical`) | upstream canonical-7+1 lock; rocket emit must match |
| `period` | uppercase `ANCIENT` / `MEDIEVAL` / `MODERN` (nullable when substrate doesn't supply) | WS2.P2 substrate convention; rocket emit must match |
| `engine_version_sha` | 7-char short sha (`git rev-parse --short=7 HEAD`) | star-lord seam; consistent across emit |
| `lineage_tags` substructure | 4-field object (`kit_space_lineage` / `engine_provenance` / `substrate_provenance` / `generation_cohort_date`) per pool.json v1.1 pattern | elrond decision per LOCK K; rocket + star-lord populate |

### Migration verification (deferred to EAA-3 + EAA-4 implementation; this MIGRATION authors design)

Acceptance criteria (verified at jack-ryan Gate-2 + EAA-5 smoke-test):
- [ ] Rocket per-kit JSON schema spec PASSES Gate-2 with format locks applied
- [ ] Star-lord chronicle emit + per-kit emit lands in `data/kit_space/` per § 5 layout
- [ ] elrond shadow-table CREATE script runs against catalogue.db; idempotent
- [ ] elrond ingest script populates shadow tables from filesystem; deterministic rebuild
- [ ] Single-event-single-kit smoke (§ 7 joint spec) passes end-to-end
- [ ] FK integrity: every `engine_kit_index.kit_space_expansion_event_id` resolves to `engine_kit_space_events.event_id`
- [ ] Backward-compat: existing season manifests + class JSONs at `seasons/` unchanged
- [ ] Reversibility (LOCK J): dropping shadow tables and deleting `kit_space/` directory both restore prior-state cleanly

### Files committed (this MIGRATION authoring step)

- `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md` — joint elrond-side spec (10 sections; LOCKED kit_id + event_id formats; shadow-table DDL; ingest-compat verdict)
- `agentic_orchestration/research/curated/MIGRATION.md` — THIS entry (v1.8)

**Deferred to EAA-3 + EAA-4 implementation phase (post-Gate-2):**
- `agentic_orchestration/research/scripts/eaa_3_4_create_kit_shadow_tables_2026_06_02.py` — shadow-table CREATE script
- `agentic_orchestration/research/scripts/eaa_3_4_ingest_kit_space_2026_06_02.py` — ingest from filesystem
- Smoke-test scripts (single-event-single-kit; rebuild determinism; FK integrity)
- Engine-side EAA-3 schema implementation (rocket); engine-side EAA-4 chronicle emit (star-lord)

### Related canonical docs + disciplines

- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 + § 3.4 (binding architectural commitment)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 vocabulary lock; consumed by per-skill flavor naming + lineage tag substrate provenance)
- `agentic_orchestration/dispatches/2026-06-02-eaa-3-kit-space-output-schema.md` (rocket primary + elrond co-owner)
- `agentic_orchestration/dispatches/2026-06-02-eaa-4-kit-space-chronicle-infrastructure.md` (elrond primary + star-lord co-owner)
- `agentic_orchestration/qa/findings/2026-06-02-eaa-phase-1-batch-gate-1.md` (Phase 1 batch Gate-1 PASS-with-INFO; INFO-B amendment composed into this entry)
- `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md` (workstream status)
- Locks A-P (per gandalf transmission 2026-06-02; LOCK K active for engine schema design authority; LOCK J ADDITIVE-AND-REVERSIBLE heuristic governs both shadow tables and filesystem layout)
- Discipline #41 substrate-led (kit space is the substrate; engine emits per-kit entries; analytical layer reads substrate truth not pre-imposed taxonomy)
- ADR-004 (cross-seam MIGRATION discipline; this entry is the elrond-side artifact composing with future rocket-side engine emit MIGRATION)
- ADR-006 (read-only-by-default external systems; elrond owns curated catalogue.db writes; engine remains source-of-truth)

### Routing back to KR

- Joint spec authored ✅
- `kit_space_expansion_event_id` format LOCKED (§ 1) ✅
- `kit_id` format LOCKED (§ 2) ✅
- Chronicle storage medium LOCKED (§ 3) ✅
- elrond ingest-compat CONFIRMED (§ 4.4) ✅
- Five iteration points named for rocket DRAFT alignment (§ 4.4) — needs rocket acknowledgment
- Cross-seam MIGRATION.md COMMITTED at elrond seam boundary (this entry)
- Backward-compat statement complete (§ 6 of joint spec); historical seasons preserved
- Routing back: **proceed to rocket DRAFT review + jack-ryan Gate-2** (schema + MIGRATION) with format locks attached for joint verification

---

## v1.7 — WS1A.Q18 sub-phase 5f — pool.json v1.1 migration + physical_taxonomy.json — 2026-06-01

### What changed (one line)

Executed POST-WAVE pool.json v1.0→v1.1 schema-extension-and-data-migration per WS1A.Q18 PG-3 ratification: extended `PoolElement` with 4 additive fields, migrated `data/seasonal_elements/pool.json` from 156 → 214 entries (100 Architecture-A locked allow-list + 114 legacy preserved-as-quarantined), created `data/seasonal_elements/physical_taxonomy.json` as separate Architecture-A taxonomy-sibling registry (9 physical entries), authored engine-side ADR-004 MIGRATION.md companion entry.

### Why (one line)

Operationalizes WS1A.Q18 wave-close architectural commitment (Architecture A LOCKED 2026-06-01: 7 rotating primaries with substrate-honest flavor pools + physical-as-Architecture-A-taxonomy-sibling); deferred from wave-scope to sub-phase 5f POST-WAVE per ADR-004 cross-seam contract change discipline.

### Who's affected

- **Rocket** — owns engine generation; no immediate action required (backward-compat preserved); MAY consume new fields in future WS1A.3 theme-coherence gating per deferred-commitments item 5.1.1.
- **Star-lord** — owns telemetry/export; no immediate action required (telemetry packets do not currently read pool.json beyond named fields); MAY surface lineage tags in future telemetry-audit work.
- **Drax** — owns loadout/demo; zero impact (consumes engine-generated artifacts, not pool.json directly).
- **Gandalf** — design steward; new lineage tags enable per-tag distribution audit queries; useful surface for deferred-commitments items 5.1.1 (theme-coherence) + 5.1.2 (modern-caster substrate-gap).
- **Jack-ryan** — Gate-2 review (BLOCK authority) on this migration per dispatch § 4 acceptance criteria.
- **Knight-rider** — receives report-back; routes Gate-2; sequences cardinality-discrepancy ambiguity-surface for resolution.
- **Legolas** — no action.
- **Matt** — LAST-resort escalation for cardinality ambiguity surfaced below (internal inconsistency in canonical lock cardinality assertions vs verbatim per-primary lists).

### What downstream consumers need to do

**Rocket (no immediate action):** v1.1 schema is fully backward-compatible; existing selector.py + naming.py readers absorb new fields silently. Future lineage-tag-aware sub-element selection is a separate dispatch.

**Star-lord (no immediate action):** export packet schema unchanged. Future telemetry extension to surface lineage tags would be a separate dispatch.

**Drax (no action):** zero impact.

**Gandalf (no action; future query surface enabled):** new lineage tag enum supports per-tag-distribution queries.

### Schema diff or example before/after

**Engine-side MIGRATION.md companion entry** (authoritative engine-side schema spec): `reincarnated-engine/src/reincarnated/element/MIGRATION.md` § "[2026-06-01] WS1A.Q18 sub-phase 5f". Contains before/after schema diff, enum value spec, backward-compat verification, and migration order. This data-layer-side entry COMPOSES with the engine-side entry per ADR-004 round-trip discipline.

**Pool.json v1.1 file-level diff:**
- `version`: "1.0" → "1.1"
- New top-level fields: `schema_version: "1.1"`, `schema_notes`
- `elements` array: 156 → 214 entries (100 Architecture-A locked + 114 legacy preserved)

**New file: `data/seasonal_elements/physical_taxonomy.json`** — 9-entry Architecture-A taxonomy-sibling registry (4 damage_sub_type + 4 mechanical_action_vocabulary + 1 ailment). Physical kits opt out of WS1A.4 LLM judgment per canonical lock § 4.

### Cardinality discrepancies surfaced (NOT silently resolved — per dispatch ambiguity-surface protocol)

**Ambiguity 1 — Canonical lock cardinality (109 claimed vs 100 enumerated):** canonical lock + PG-3 ratification both assert "109 rotating-primary + 9 physical = 118 total", but per-primary verbatim entry lists (Gate-2-PASS-verified entry-by-entry) sum to 16+14+18+13+13+14+12 = **100**, not 109. Elrond seam decision: migrate against the verified verbatim per-primary lists; surface to KR for resolution by canonical-doc steward (gandalf) and/or PG-3 ratification author (Matt). Final lineage tag application targets adjusted to reconcile with 100-entry actual total.

**Ambiguity 2 — Lineage tag aggregate reconciliation:** PG-3 § 5 binding aggregate (65/24/19/1/9 = 118) does NOT reconcile with 100 actual rotating-primary entries. Canonical § 7.1 illustrative col-sum (57/19/23/1/9 = 109) DOES reconcile with 100 actual rotating-primary entries. Canonical § 7 explicit modern-scientific enumeration is 19 entries (matches PG-3 § 5; not § 7.1 col 23). Elrond seam decision: apply lineage tags per § 7.1 col-sum reconciliation BUT honor canonical § 7 explicit overlay enumeration → final per-entry distribution: 57/23/19/1 = 100 rotating + 9 physical = 109 actual total. Documented + traceable in migration script.

**Ambiguity 3 — INFO-1 `stormtide`:** stormtide appears in slot-routing decisions but NOT in the 109-entry rotating-primary lock NOR in v1.0 pool.json. Elrond seam decision: no-op (no entry to route; slot-routing decision preserved in script for future reference).

### Migration verification

- ✅ Schema-extended PoolElement reads v1.1 pool.json cleanly (all 214 entries parse)
- ✅ Pre-extension PoolElement reads v1.1 pool.json cleanly (backward-compat)
- ✅ Round-trip JSON parse OK for pool.json + physical_taxonomy.json
- ✅ Lineage-tag aggregate matches § 7.1 col-sums: 57+23+19+1 = 100 rotating + 9 physical = 109
- ✅ Slot routing applied: mist → water primary (was wind)
- ✅ Cull-tag dispositions applied: thorn promoted (drift-14-plant-anatomical dissolved-for-thorn); cyclone/whirlwind/squall/hurricane cull-tag dissolved (entries now in lock); typhoon legacy with cull-tag preserved
- ✅ Drift-14 invariant validator still fires for new entries that lack VFX manifest coverage (expected; future surface)

### Files committed (this MIGRATION)

- `reincarnated-engine/src/reincarnated/element/schema.py` — PoolElement extended with 4 additive fields
- `reincarnated-engine/src/reincarnated/element/pool.py` — add_element_to_pool() preserves new fields
- `reincarnated-engine/src/reincarnated/element/MIGRATION.md` — engine-side cross-seam MIGRATION entry
- `reincarnated-engine/data/seasonal_elements/pool.json` — v1.0 → v1.1 (156 → 214 entries)
- `reincarnated-engine/data/seasonal_elements/pool.json.pre-q18-2026-06-01-backup` — pre-migration snapshot
- `reincarnated-engine/data/seasonal_elements/physical_taxonomy.json` — NEW Architecture-A taxonomy registry
- `agentic_orchestration/research/scripts/q18_pool_migration_2026_06_01.py` — migration script
- `agentic_orchestration/research/curated/MIGRATION.md` — THIS entry (v1.7)

### Related canonical docs + disciplines

- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Architecture A LOCK)
- `canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md` (wave-close record)
- `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md` (PG-3 ratification)
- `agentic_orchestration/dispatches/2026-06-01-elrond-cycle-15-ws1a-q18-sub-phase-5f-pool-migration.md` (this dispatch)
- Discipline #41 (substrate-led) + #49 (substrate-silence ≠ substrate-validation; the 23 substrate-silent lineage tags here are this discipline's first operational application) + #50 (3-test inclusion gate) + #51 (synthesis-draft adversarial Pattern B critique)
- ADR-004 (cross-seam MIGRATION discipline) + ADR-006 (read-only-by-default external systems)

### Routing back to KR

- Migration COMMITTED per acceptance criteria § 4
- Cross-seam MIGRATION.md COMMITTED at engine-side seam boundary
- Backward-compat VERIFIED (pre-extension + extended schemas both parse pool.json v1.1 cleanly)
- Per-entry lineage tag application: clean per § 7.1 col-sum reconciliation; 3 ambiguities surfaced — see above; do NOT silently resolved
- Cross-seam touches surfaced for follow-on: NONE require secondary dispatch (rocket + star-lord + drax all confirmed no-action-required)
- Routing back: **proceed to jack-ryan Gate-2 (schema + migration review)** with cardinality-discrepancy ambiguity-surface attached for joint resolution

---

## v1.6 — Pattern A: Tier 5.1/5.2 final curation — additive schema spec + manifest extension — 2026-05-18

### What changed (one line)

Authored additive catalogue-DB schema spec (`catalogue-db-schema-v2-2026-05-18.md`) introducing `usage_recommendation` + `license_class` enum columns on `catalogue_assets` per Matt L3 Tier 5.2 approval; extended `ambient-props-subset-vs2a-2026-05-17.jsonl` with 8 new prop rows (Tier 5.1 prop pool extension); authored consolidated drax v1.21+ handoff brief covering icons + props + credits.txt + schema cross-reference.

### Why (one line)

Closes Tier 5.1 (Game-icons.net SIL-1.1 / consistent prop scale 0.75× / medium decoration density / single credits.txt) + Tier 5.2 (additive schema rubber-stamp); operationalizes the dungeon-objects audit § 6 curation lesson at schema level (per-file `usage_recommendation` prevents shred-defect class); enables programmatic credits.txt generation via `license_class` per-asset specific-license tracking.

### Who's affected

- **Drax** — receives `tier-5-1-5-2-drax-v1.21-handoff-brief-2026-05-18.md` as consumption-ready brief for v1.21+ wire-in (queued post-mobile-chain + post-chierit-monster-wiring; lowest VS2a polish priority). Brief covers 28-icon game-icons.net role mapping, `PROP_RENDER_SCALE_OVERRIDE = 0.75` application, 8 new prop descriptors with source coords, complete credits.txt verbatim text, schema cross-reference. No drax-side schema consumption required in v1.21+ pass (schema is upstream-curator-facing; future passes populate the new columns).
- **Legolas** — no action; future Mode B crawls can populate `usage_recommendation` per persona-rule extension if knight-rider sequences. Optional addition to legolas.md per-row output format.
- **Gandalf** — schema additions enable license-risk + per-class-substrate queries; surfaces for any future cipher-width / cluster-clarity sensitivity that wants to factor license-class exposure.
- **Star-lord** — no engine-side impact; ADR-004 satisfied via elrond-side MIGRATION.md v1.6 only.
- **Rocket** — unaffected.
- **Knight-rider** — receives this MIGRATION + handoff-brief + schema spec + manifest extension + AGENT_STATE update. Sequences drax v1.21+ at lowest VS2a polish priority; sequences future elrond v1.12 schema-execution dispatch when convenient.
- **Matt** — Tier 5.1 + Tier 5.2 lock satisfied at the curation seam; no further upstream action needed for this loop.

### What downstream consumers need to do

**Drax (v1.21+ when fired):**

1. Download 28 game-icons.net icons (SIL-1.1; zero spend) per handoff brief § 1.3 role mapping.
2. Apply `PROP_RENDER_SCALE_OVERRIDE = 0.75` multiplier per handoff brief § 2.1.
3. Append 8 new prop descriptors to `STATIC_PROP_DESCS` per handoff brief § 2.3.
4. Extend `dungeonPropsForRoom()` to per-room-size variable density per handoff brief § 2.2.
5. Deploy verbatim `credits.txt` text per handoff brief § 3.1.
6. Acceptance criteria per handoff brief § 5; out-of-scope guards per § 6.

**Star-lord:** no action.

**Gandalf:** schema additions enable license-class + usage-recommendation queries when next abstraction-analysis pass benefits.

**Legolas:** future Mode B crawls may populate `usage_recommendation` per-row optionally; persona.md addition not in scope for this dispatch.

### Schema diff or example before/after

**catalogue.db schema:** NO CHANGE EXECUTED IN THIS DISPATCH. v1.1 schema columns hold. v1.6 spec is authored and approved but execution is deferred to a future elrond v1.12 dispatch (per `catalogue-db-schema-v2-2026-05-18.md` § 7).

**catalogue.db data:** NO CHANGE. v1.5 data state (3 sources / 3 packs / 48 assets / 461 tags / 1 session) holds.

**Curated-layer artifacts:**

| Artifact | Before | After |
|---|---|---|
| `ambient-props-subset-vs2a-2026-05-17.jsonl` row count | 26 (1 meta + 25 rows) | **35** (1 meta + 25 rows + **1 addendum-meta + 8 new rows**) |
| `catalogue-db-schema-v2-2026-05-18.md` | did not exist | **NEW** — spec for `usage_recommendation` + `license_class` columns + indexes + v1.6 schema_meta row |
| `tier-5-1-5-2-drax-v1.21-handoff-brief-2026-05-18.md` | did not exist | **NEW** — consolidated 4-deliverable brief (icons + props + credits + schema cross-ref) |
| `MIGRATION.md` | v1.5 latest | **v1.6 entry appended** |

**Schema-spec-only mutations (NOT yet applied to catalogue.db):**

| Aspect | Spec'd v1.6 | Execution |
|---|---|---|
| New column `usage_recommendation TEXT NULL CHECK (...)` on `catalogue_assets` | spec'd | deferred to elrond v1.12 |
| New column `license_class TEXT NULL CHECK (...)` on `catalogue_assets` | spec'd | deferred to elrond v1.12 |
| Partial indexes on new columns | spec'd | deferred |
| `schema_meta` v1.6 row | spec'd | deferred |
| Migration script `v1_6_usage_recommendation_license_class.sql` | NOT yet authored (spec-only) | future dispatch |

### Tier 5.1 / 5.2 Matt-lock satisfaction record

| Tier 5.1 lock | Satisfied by |
|---|---|
| Game-icons.net (SIL-1.1) | Handoff brief § 1 (role mapping for 28 icons + license posture + on-disk placement spec) |
| Consistent prop scale | Handoff brief § 2.1 (`PROP_RENDER_SCALE_OVERRIDE = 0.75` per gandalf v1.7 canon) |
| Medium decoration density | Handoff brief § 2.2 (4-6-8 per-room-size density rules + within-room uniqueness) |
| Single credits.txt | Handoff brief § 3.1 (complete verbatim file content for drax deployment) |

| Tier 5.2 lock | Satisfied by |
|---|---|
| Defer mega-pack-02 | No mega-pack-02 work in this dispatch; pass-through |
| Rubber-stamp HD-cinematic | Pass-through (no elrond surface) |
| Approve catalogue-DB additive schema | Schema spec authored at `catalogue-db-schema-v2-2026-05-18.md`; v1.6 design-locked, execution deferred |

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** Matt L3 2026-05-18 explicit approval of additive schema. v1.6 spec is within scope.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. Engine telemetry untouched.
- **ADR-006 (external system writes require authorization):** writes confined to elrond-owned paths (`research/curated/*`). No drax/demo/loadout code touched. No tag push.
- **ADR-007 (survey-mode):** handoff brief separates "what to wire" from "what NOT to wire" (§ 6 out-of-scope guards explicit).

### Files changed

- `agentic_orchestration/research/curated/catalogue-db-schema-v2-2026-05-18.md` (NEW)
- `agentic_orchestration/research/curated/tier-5-1-5-2-drax-v1.21-handoff-brief-2026-05-18.md` (NEW)
- `agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl` (EXTENDED — 26 → 35 lines)
- `agentic_orchestration/research/curated/MIGRATION.md` (THIS FILE — v1.6 entry)
- `agentic_orchestration/research/curated/AGENT_STATE.md` (UPDATED — Pattern A Tier 5.1/5.2 completion record)

### Files intentionally NOT changed

- `agentic_orchestration/research/curated/catalogue.db` — schema execution deferred per § Schema diff
- `agentic_orchestration/research/scripts/catalogue_migrations/v1_6_*.sql` — migration script NOT yet authored (future dispatch)
- `reincarnated-demo/public/credits.txt` — drax v1.21+ seam (this dispatch authors text only)
- `reincarnated-demo/src/visuals/ambientPropsExtension.ts` — drax v1.21+ seam
- `reincarnated-demo/src/visuals/gameIcons.ts` — drax v1.21+ seam (new module)
- Other curated artifacts (`dungeon-objects-quality-audit-2026-05-18.md` etc.) — unchanged

### Reversibility

Spec-only mutation:
- Three new docs (`catalogue-db-schema-v2-*`, `tier-5-1-5-2-drax-v1.21-handoff-brief-*`, MIGRATION.md v1.6 entry) — revertible by `rm` + git-reset
- Manifest extension (`ambient-props-subset-vs2a-2026-05-17.jsonl`) — revertible by `head -n 26` (the addendum-meta + 8 rows are contiguous at the file tail)
- No catalogue.db mutation in this dispatch; no DB backup needed.

### Out-of-scope follow-ons (for knight-rider sequencing)

1. **elrond v1.12 — execute v1.6 schema migration** — author `v1_6_usage_recommendation_license_class.sql`; apply to catalogue.db; create pre-v1.6 backup. Estimated 30-45 min.
2. **elrond v1.13 — back-fill existing 48 rows with `usage_recommendation` + `license_class`** — single curator pass over the corpus. Estimated 1-2 hours.
3. **drax v1.21+ — wire-in per handoff brief** — Tier 5.1 surfaces (icons + props + credits.txt). Estimated 2-3 hours when sequenced.
4. **legolas persona.md extension** — optional addition of `usage_recommendation` field to Mode B crawl output schema. Knight-rider sequences.
5. **future curation passes consume `license_class`** — credits.txt generator script (research/scripts/) when corpus crosses ~100 attribution surfaces and hand-curation becomes brittle.

### Tag

`elrond/v1.11-tier-5-1-5-2-final-curation-1` (local; no push per ADR-006)

---

## v1.5 — Pattern A: Pixogen catalogue loop closure (HOLD → APPROVED-WITH-ATTRIBUTION) — 2026-05-16

### What changed (one line)

Pixogen vendor row inserted into `catalogue_sources` (data migration v1.2 against schema v1.1; no schema change); curated JSONL `pixogen-catalogue-curated-2026-05-16.jsonl` filed with HOLD-to-APPROVED-WITH-ATTRIBUTION flag transitions for both Full and Lite SKUs; pricing/access metadata corrected (Full €19.99 paid not-yet-acquired; Lite €0 acquired); attribution-required flag carried per AFGameAssets license § 3.A.1.

### Why (one line)

Closes Pixogen Path-A loop per Matt license-file verification 2026-05-16 (downloaded Lite pack; read 18kB AFGameAssets license) + drax v0.19 Void Shield demo wiring with attribution credit. Prior state: legolas Mode B raw extraction carried `license_unverified: true` + `consumption_hold: HOLD`; cipher-width-inclusion analysis excluded Pixogen; pivot-insurance-ledger flagged Pixogen as SPOF for technology-vfx substrate. Verification cleared HOLD; substrate-evidence may now re-include Pixogen (separate downstream re-analysis dispatch).

### Who's affected

- **Drax** — Pixogen Void Shield wired v0.19 (already done; this dispatch attests upstream catalogue state). Future Pixogen-asset consumption: query `catalogue_sources WHERE source='itch-pixogen'` returns vendor row with `default_license='commercial-royalty-free'` + notes carrying `attribution_required` clause. Per-pack/per-asset rows NOT yet curated in catalogue.db (out of scope for this dispatch); the curated JSONL serves as interim reference for the two SKUs.
- **Legolas** — PARALLEL dispatch updates `pixogen/findings-summary-2026-05-16.md` with verified `license_terms_verbatim` (license file full text). Coordinate via this MIGRATION.md timestamp (2026-05-17T02:11:09Z, the catalogue.db schema_meta v1.2 applied_at). Legolas's raw extraction file at `catalogue/pixogen/full-2026-05-16.jsonl` is INTENTIONALLY UNTOUCHED by this dispatch per ownership-boundary discipline — raw extraction is a snapshot artifact; curated state lives in `curated/pixogen-catalogue-curated-2026-05-16.jsonl`.
- **Gandalf** — Pixogen substrate evidence (void-spatial + technology-vfx) is now re-includable in any future cipher-width / cluster-clarity sensitivity analysis. Pivot-insurance-ledger line 136 + cross-vendor substrate inventory still carry HOLD-era exclusion language; UPDATE NOT MADE in this dispatch (downstream document update is a separate gandalf-or-elrond sequencing call). Reversal-path documented in pivot-insurance-ledger line 145 is now ACTIVATED — when next emergent-grouping analysis is run, Pixogen rows can be re-included.
- **Star-lord** — no engine-side impact; ADR-004 satisfied via elrond-side MIGRATION.md v1.5 only. No cross-DB ATTACH pattern changes.
- **Rocket** — unaffected.
- **Knight-rider** — Pixogen Path-A loop CLOSED; consumption is APPROVED-WITH-ATTRIBUTION per AFGameAssets license § 3.A.1. Sequences any follow-on Pixogen pack-curation dispatches (Lite per-animation curation; Full acquisition decision; void/technology re-inclusion in cipher-width analysis).
- **Matt** — license verification action complete; no further upstream action needed for this loop. Full pack (€19.99) acquisition is a future commission decision; flagged in vendor notes.

### What downstream consumers need to do

**Drax:**
1. Continue Void Shield consumption per v0.19. When sourcing additional Pixogen assets, ensure attribution credit is maintained in demo + loadout per AFGameAssets license § 3.A.1.
2. If consuming additional Lite animations (Water/Fire/Wind/Holy/Electric/Fireworks/Explosions), reference `curated/pixogen-catalogue-curated-2026-05-16.jsonl` for asset metadata until per-pack catalogue_assets curation lands.

**Star-lord:** no action.

**Gandalf:**
1. When commissioning next cipher-width or cluster-clarity sensitivity pass, request Pixogen re-inclusion. Substrate-evidence weights change: void-spatial gains a confirming row (n=2 with CraftPix Black Hole already present); technology-vfx becomes attested (n=1; Pixogen-exclusive).
2. Consider sequencing a `pivot-insurance-ledger.md` + `cross-vendor-substrate-inventory-2026-05-16.jsonl` HOLD-language refresh dispatch (elrond can author once gandalf signals timing).

**Legolas:** author parallel `pixogen/findings-summary-2026-05-16.md` update populating `license_terms_verbatim` from license file inspection. Timestamp coordination via this v1.5 entry. Raw extraction file (`catalogue/pixogen/full-2026-05-16.jsonl`) remains untouched per legolas ownership.

### Schema diff or example before/after

**catalogue.db schema:** NO CHANGE (v1.1 holds). This is a DATA migration only.

**catalogue.db data:**

| Aspect | Before (v1.4 / data migration v1.1 applied) | After (v1.5 / data migration v1.2 applied) |
|---|---|---|
| `catalogue_sources` rows | 2 (itch-pimen, craftpix) | 3 (**+itch-pixogen** — individual-creator, hand-drawn-pixel, commercial-royalty-free, register_mixed=0) |
| `catalogue_packs` rows | 3 (pimen) | 3 (**no change** — Pixogen pack curation out of scope per dispatch) |
| `catalogue_assets` rows | 48 (pimen) | 48 (**no change** — Pixogen asset curation out of scope per dispatch) |
| `schema_meta` rows | 2 (v1.0, v1.1) | 3 (**+v1.2** data-migration entry) |
| `pixogen-catalogue-curated-2026-05-16.jsonl` | did not exist | **NEW** — 2 rows (Full + Lite) with HOLD-cleared flag state |

**Curated JSONL flag transitions (per row):**

| Field | Before (legolas raw extraction) | After (elrond curated) |
|---|---|---|
| `license_unverified` | `true` | `false` |
| `consumption_hold` | (implicit HOLD; HOLD literal in legolas findings-summary) | `APPROVED-WITH-ATTRIBUTION` |
| `license_verified_date` | (absent) | `2026-05-16` |
| `license_verified_by` | (absent) | `matt` |
| `license_verification_method` | (absent) | `lite-pack-download-license-file-inspection` (Full) / `lite-pack-download-license-file-direct-inspection` (Lite) |
| `attribution_required` | (absent) | `true` |
| `attribution_recipient` | (absent) | `Pixogen / AFGameAssets / Antoine Fauville` |
| `cost_currency` | (absent for Full; absent for Lite) | `EUR` (Full) / `EUR` (Lite, €0) |
| `cost_usd_approx` | (absent) | `21.59` (Full) / `0.0` (Lite) |
| `cost_acquired_by_project` | (absent) | `false` (Full) / `true` (Lite) |
| `cost_acquired_note` | (absent) | corrected pricing/access metadata (Full not-yet-acquired; Lite acquired) |
| `c2_license_flag` | `true` | `false` |
| `c2_license_outcome` | "LICENSE UNVERIFIED..." | "CLEARED 2026-05-16 — License verified clean..." |
| `license` | `proprietary-pending-verification` | `commercial-royalty-free` |
| `license_terms_verbatim` | "License of AFGameAssets — terms in downloadable 18 kB file; NOT publicly readable..." | "AFGameAssets license (Antoine Fauville) — distributed as 18kB file with each pack. Verified terms: commercial use permitted; modification permitted; Pixi.js runtime tinting permitted per § 2.A.4; attribution REQUIRED per § 3.A.1. (Full verbatim license text held by legolas in pixogen findings-summary update; this row carries verified-status flags only.)" |

**Sequencing note on `license_terms_verbatim`:** elrond carries the abbreviated verified-state summary in the curated jsonl; legolas (parallel dispatch) authors the full verbatim license text in `pixogen/findings-summary-2026-05-16.md`. This split mirrors the ownership boundary: legolas's findings-summary is the canonical full-text reference; elrond's curated jsonl carries operational state. If both touch this field on the same row at the same time, MIGRATION.md timestamps (2026-05-17T02:11:09Z for elrond) are the conflict-resolution reference.

### Pricing/access correction (dispatch item 3)

Prior catalogue metadata referenced "Pixogen Lite free version" framing — Matt clarified the actual structure:

| SKU | Cost | Acquisition path | Project acquisition state |
|---|---|---|---|
| Pixel Art RPG VFX (Full Pack) | **€19.99** | itch.io direct purchase OR Mega Pack (€59.99) | **NOT YET ACQUIRED** (future commission decision) |
| Pixel Art RPG VFX Lite | **€0** | itch.io separate download | **ACQUIRED 2026-05-16** (Matt download; license verification vector) |

The Lite is **not a free version of the Full** — it is a separate standalone free download with a reduced category set (8 categories vs Full's 11). Categories missing from Lite: Technology, Attack Slash, Ice. This distinction is now captured in vendor `notes` + per-SKU `cost_acquired_note` fields.

### Files changed

- `agentic_orchestration/research/curated/catalogue.db` (mutated — schema_meta v1.2 row + catalogue_sources itch-pixogen row inserted)
- `agentic_orchestration/research/curated/catalogue.db.pre-pixogen-2026-05-16-backup` (NEW — pre-migration safety snapshot; ~1 week soft-retention)
- `agentic_orchestration/research/curated/pixogen-catalogue-curated-2026-05-16.jsonl` (NEW — 2 rows; verified-state flag transitions)
- `agentic_orchestration/research/scripts/catalogue_migrations/v1_2_pixogen_vendor_insert.sql` (NEW — idempotent? NO — INSERT with no ON CONFLICT clause; re-run will fail on UNIQUE constraint, which is the intended replay safety)
- `agentic_orchestration/research/curated/MIGRATION.md` (THIS FILE — v1.5 entry)
- `agentic_orchestration/research/curated/AGENT_STATE.md` (UPDATED — Pattern A Pixogen dispatch completion)

### Files intentionally NOT changed

- `agentic_orchestration/research/catalogue/pixogen/full-2026-05-16.jsonl` (legolas's raw extraction; ownership boundary — untouched)
- `agentic_orchestration/research/catalogue/pixogen/findings-summary-2026-05-16.md` (legolas parallel dispatch updates `license_terms_verbatim`)
- `agentic_orchestration/research/catalogue/pixogen/geometry-signatures-2026-05-16.jsonl` (geometry signatures unchanged by license verification)
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (carries HOLD-era exclusion language; refresh deferred per dispatch scope — separate gandalf-sequencing call)
- `agentic_orchestration/research/curated/pivot-insurance-ledger.md` (carries HOLD-era exclusion language at line 136 + reversal-path at line 145; refresh deferred per dispatch scope)
- `agentic_orchestration/research/curated/cipher-width-inclusion-flags-2026-05-16.jsonl` (Pixogen-exclusion flags from HOLD era; refresh deferred per dispatch scope)
- `agentic_orchestration/research/curated/post-step-b-cleanup-2026-05-16.md` (HOLD-era operational state record; historical artifact, not updated)

### Out-of-scope follow-ons (for knight-rider sequencing)

1. **Pixogen Lite per-pack curation** — 8 Lite animations × catalogue_packs row + 8 catalogue_assets rows; requires curator visual inspection of frames. Estimated: 1-2 hours.
2. **Pixogen Full acquisition decision** — Matt + knight-rider; €19.99 purchase OR Mega Pack at €59.99. Substrate-coverage argument (technology-vfx is Pixogen-exclusive) may motivate.
3. **Cipher-width / cluster-clarity sensitivity re-run with Pixogen re-included** — elrond dispatch; substrate-evidence weights will shift (void-spatial gains confirming row; technology-vfx becomes attested).
4. **HOLD-era language refresh in downstream documents** — pivot-insurance-ledger line 136 + line 145, cross-vendor substrate inventory Pixogen-exclusion blocks, cipher-width inclusion flags. Combined elrond dispatch; estimated 1 hour.
5. **Decisions-log entry** — knight-rider sequences; codifies Pixogen license-verification + first-vendor-consumption pattern (vendor onboarding playbook precedent).

### Reversibility

Pure data INSERT into `catalogue_sources`. Reverse via:
```sql
DELETE FROM catalogue_sources WHERE source='itch-pixogen';
DELETE FROM schema_meta WHERE version='1.2';
```
Safe while no downstream `catalogue_packs` / `catalogue_assets` rows reference `itch-pixogen` (FK constraints block deletion once downstream rows land). Curated jsonl is a flat file; `rm` reverses. Backup at `catalogue.db.pre-pixogen-2026-05-16-backup` is canonical pre-migration snapshot.

---

## v1.4 — Pattern A combined: bundle-pipeline follow-up + register-mixed schema amendment — 2026-05-16

### What changed (one line)

Schema bumped to v1.1 (per-vendor `register_mixed` convenience flag + per-product `deliverable_register` field per Drift-13 / Pattern P8 prescription (d)); CraftPix vendor record added as canonical first cross-register instance; three curation amendments landed on Pimen rows in response to drax bundle-pipeline follow-on items (slug-collision disambiguation hints, new bundle-internal-only Icons sub-pack curated, explosion-effect matcher-correction tags).

### Why (one line)

Closes the Pattern A dispatch ("yes to all 7" Matt-authorization 2026-05-16, decisions #2 + #5): Track A unblocks drax's bundle-pipeline matcher on the slug-collision case + brings the Icons sub-pack into the catalogue + corrects an explosion-VFX misread; Track B operationalizes the Drift-13 / Pattern P8 (d) prevention prescription at the catalogue-db schema layer, with CraftPix as the canonical first cross-register vendor.

### Who's affected

- **Drax** — bundle-pipeline matcher can now consult `bundle-folder-hint:*` tags + `subpack-organization-style:*` tags + `_amendment_2026_05_16_bundle_folder_hint` JSON overlay to resolve the slug-collision case + the per-animation-subfolders style-B case. Existing matcher logic continues to work for the simple slug↔folder cases; the new hints are advisory upgrades. Schema additions (`deliverable_register`, `register_mixed`) consumed at downstream filtering time — drax cross-register safety query in §5.5 of catalogue-schema.md applies once schema doc is amended.
- **Legolas** — Track B's per-product `deliverable_register` field aligns with persona-rule extension landed today (`legolas.md` line 34). Future Mode B catalogue dispatches populate the field per product line. Pimen rows are NOT retroactively backfilled (Pimen is single-register; `register_mixed=0` holds; field remains NULL for pimen rows, which is valid per CHECK).
- **Gandalf** — Track B closes the Drift-13 / Pattern P8 prevention prescription (d) (downstream-consumption safety net). Track A's Icons curation extends UI/icon coverage for VS2a/VS2b scene composition. CraftPix vendor record is now schema-attestable as cross-register (queryable via `SELECT register_mixed FROM catalogue_sources WHERE source='craftpix';`).
- **Star-lord** — no immediate action; cross-store ATTACH pattern unchanged. The new columns are queryable via standard SQLite ATTACH.
- **Rocket** — unaffected.
- **Knight-rider** — receives this MIGRATION + dispatch-completion notification; sequences `catalogue-schema.md` v1.1 doc-update follow-on (schema diff captured here is canonical; the design doc should reflect by next session).

### What downstream consumers need to do

**Drax:**

1. Bundle-pipeline matcher upgrades (recommendations in `pimen-bundle-follow-up-2026-05-16.md` §§ 1, 2, 3):
   - Read `_amendment_2026_05_16_bundle_folder_hint` from `source_metadata_raw` OR scan `asset_style_tags WHERE tag LIKE 'bundle-folder-hint:%'` to disambiguate slug-collision cases.
   - Consult `animations_count` + new `subpack-organization-style:*` tags before classifying folder structure as "sub-packs" vs "per-animation-subfolders."
   - Treat `bundle-internal-only:<bundle_id>` tagged rows as bundle-sourced-only (no standalone-product URL applies).
2. Cross-register-safety query (Track B): when sourcing assets from a vendor with `register_mixed=1`, check `deliverable_register` at the per-row level. CraftPix is the only current `register_mixed=1` vendor; future ones inherit the pattern automatically.
3. The Icons sub-pack row (`source_asset_id='mega-pack-elemental-icons'`) is `quality_flag='deferred'` until visual inspection completes. Default consumption filter (which requires `quality_flag='pass'`) excludes it for now. Use a `quality_flag IN ('pass','deferred')` widened filter if early-prototype UI work needs the icons before inspection lands.

**Star-lord:** no action. The ATTACH pattern in `catalogue-schema.md` §5.1 continues to work; the new columns are additive.

**Gandalf:**

1. Track A Icons curation widens UI/icon coverage. When VS2a/VS2b design surfaces element-identity-rendering needs, the catalogue row provides the canonical reference.
2. Track B's `register_mixed=1` CraftPix row attests the Drift-13 instance in schema. Cross-register-safety queries are now expressible — useful for any future register-validation pass against the catalogue.

**Legolas:** no action. Future Mode B crawls populate `deliverable_register` per persona-rule extension; the field is OPTIONAL/NULL-allowed so persona compliance is checked at curation, not at extraction.

### Schema diff or example before/after

**catalogue.db schema:**

| Aspect | Before (v1.0) | After (v1.1) |
|---|---|---|
| `catalogue_sources` columns | 7 (source, display_name, url, vendor_type, primary_register_hint, default_license, notes, added_at) | **+1**: `register_mixed INTEGER NOT NULL DEFAULT 0 CHECK (register_mixed IN (0,1))` |
| `catalogue_assets` columns | 37 (see v1_0_initial.sql) | **+1**: `deliverable_register TEXT NULL CHECK (deliverable_register IN ('pixel-art-raster', 'vector-ai', 'vector-eps', 'vector-svg', 'hand-drawn-pixel', 'painterly-raster', 'photographic', 'audio', 'font', 'mixed', 'not-applicable', 'unknown'))` |
| Indexes | 9 on catalogue_assets | **+1**: `idx_catalogue_assets_deliverable_register` (partial, WHERE NOT NULL) |
| `catalogue_sources` rows | 1 (itch-pimen) | 2 (itch-pimen `register_mixed=0`, craftpix `register_mixed=1`) |
| `catalogue_assets` rows | 47 | 48 (Track A item 2 added `mega-pack-elemental-icons`) |
| `asset_style_tags` rows | 444 | 461 (+4 bundle-folder-hint amendments + 11 icon tags + 2 explosion matcher-correction) |
| Schema version | 1.0 | 1.1 |

**Track A non-schema mutations:**

- 2 `catalogue_assets` rows had `source_metadata_raw` JSON amended in-place via additive overlay key `_amendment_2026_05_16_bundle_folder_hint` (the existing `_curation_overlay_2026_05_16` key preserved untouched). Append-only intent: this is an additive metadata layer, not a curation supersession.
- 1 row had matcher-correction tags appended without metadata mutation (`explosion-effect`).
- 1 new row inserted (`mega-pack-elemental-icons` — bundle-internal-only sub-pack).

**JSONL snapshot:**

- `pimen-catalogue-curated-2026-05-16.jsonl`: 47 → 48 rows (icon row appended; 2 rows updated in-place with amendment overlay; 1 row updated in-place with 2 new tags).

### Track A — bundle-pipeline follow-up summary

| Item | Drax surface | Elrond resolution |
|---|---|---|
| Slug collision (`Earth Spell 03` vs `Earth Effect 03`) | Both fuzzy-match `earth-spell-effect-03`; ambiguous | Same pack in 2 formats inside bundle. Canonical = `Earth Spell 03`; fallback = `Earth Effect 03`. Amendment overlay + 4 bundle-folder-hint tags added. |
| Icons sub-pack out-of-band | Not curated; inspect + decide | INCLUDED — 10 PNGs (5 elements × 2 variants); curated as `mega-pack-elemental-icons` with `bundle-internal-only` flag; quality_flag=deferred + manual_review_queued=1 |
| 30 explosion VFX out-of-band | Inspect + recommend subset OR all-out-of-band | MISIDENTIFIED — they ARE the 30 animations of curated `explosion-effect`. 2 matcher-correction tags added; no new curation. |

Full detail: `agentic_orchestration/research/curated/pimen-bundle-follow-up-2026-05-16.md`.

### Track B — schema amendment summary

Per Drift-13 / Pattern P8 prescription (d) (`canonical/story/drift-audit.md`), the catalogue.db schema now exposes register-mixedness at two layers:

1. **Per-product (source-of-truth)** — `catalogue_assets.deliverable_register TEXT NULL` with closed CHECK enum capturing observed vendor-shipping-register vocabulary (`pixel-art-raster`, `vector-ai`, `vector-eps`, `vector-svg`, `hand-drawn-pixel`, `painterly-raster`, `photographic`, `audio`, `font`, `mixed`, `not-applicable`, `unknown`). Populated per-row by curators at curation time. NULL allowed because single-register vendors (where the vendor row's `register_mixed=0` holds) don't require per-row inspection.
2. **Per-vendor (convenience aggregate)** — `catalogue_sources.register_mixed INTEGER NOT NULL DEFAULT 0 CHECK (register_mixed IN (0,1))`. Set to 1 when any product carries a register different from `primary_register_hint`. Downstream consumers can quickly filter cross-register vendors without scanning per-product rows.

CraftPix added as canonical first instance:
```
source='craftpix', vendor_type='aggregator-marketplace',
primary_register_hint='mixed', default_license='mixed', register_mixed=1,
notes='Cross-register vendor (Drift-13 / Pattern P8 canonical first instance). ...'
```

Distinction from existing `derived_register`:
- `derived_register` (v1.0): curator's inferred VISUAL register from six-axis rubric (hand-drawn-pixel / retro-16bit / clean-vector / painterly-raster / anime-cel / manual-review). Output of rule cascade.
- `deliverable_register` (v1.1): vendor's SHIPPING register as delivered per product (PNG/PSD pixel-art / AI vector / EPS vector / etc.). Source-of-truth for cross-register routing.
- Both overlap on happy path; diverge when vendor mislabels OR ships rare formats OR delivers mixed in one product. The two columns together let consumers reason about both visual-register-fit AND shipping-format-fit.

### Pre-migration backup

`agentic_orchestration/research/curated/catalogue.db.pre-v1.1-backup` — byte-identical snapshot of catalogue.db before v1.1 migration applied. Retain until v1.1 has been consumed by drax + gandalf in downstream work, then prune at next housekeeping pass (suggest: 1-week soft-retention).

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** Matt authorized 2026-05-16 ("yes to all 7" — decisions #2 + #5). Schema migration v1.1 applied within authorization scope.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement for both Track A (data mutations) + Track B (schema mutation). No engine-telemetry or other-seam schema changed. Drax-side response (matcher updates) is drax-internal; no companion MIGRATION required unless drax declares it.
- **ADR-006 (external system writes require authorization):** writes confined to elrond-owned paths (`research/curated/*`, `research/scripts/*`, `catalogue.db`). No engine-side mutation. The pre-v1.1 backup is an additional safety layer (not required by ADR but elected here given schema migration is the rarer operation).
- **ADR-007 (survey-mode):** the bundle-follow-up findings doc reports what exists (inspection findings, decisions, action taken) without interleaving prescriptive content beyond the explicit "Recommendation to drax" subsections.

### Verification

```
$ python3 agentic_orchestration/research/scripts/amend_pimen_bundle_folder_hints_2026_05_16.py
[jsonl] {'total_rows': 47, 'amended': 2}
[db]    {'db_updates': 2, 'tags_inserted': 4, 'tags_already_present': 0}

$ python3 agentic_orchestration/research/scripts/curate_pimen_elemental_icons_2026_05_16.py
[db] {'inserted': 1, 'asset_uid': 48, 'tags_inserted': 11}
[jsonl] appended row for mega-pack-elemental-icons

$ sqlite3 catalogue.db < agentic_orchestration/research/scripts/catalogue_migrations/v1_1_register_mixed_flag.sql
(no output — transaction committed cleanly)

$ sqlite3 catalogue.db "SELECT version, applied_at FROM schema_meta ORDER BY applied_at;"
1.0|2026-05-16T04:14:38Z
1.1|2026-05-17T00:29:04Z

$ sqlite3 catalogue.db "SELECT source, vendor_type, primary_register_hint, register_mixed FROM catalogue_sources;"
itch-pimen|individual-creator|hand-drawn-pixel|0
craftpix|aggregator-marketplace|mixed|1

$ sqlite3 catalogue.db "SELECT COUNT(*) FROM catalogue_assets;"
48

$ sqlite3 catalogue.db "SELECT COUNT(*) FROM asset_style_tags;"
461

$ sqlite3 catalogue.db "INSERT INTO catalogue_sources (source, display_name, url, vendor_type, primary_register_hint, default_license, notes, added_at, register_mixed) VALUES ('test', 'test', 'http://x', 'individual-creator', 'unknown', 'unknown', 't', 't', 2);"
Error: stepping, CHECK constraint failed: register_mixed IN (0, 1)   ← CHECK enforced

$ sqlite3 catalogue.db "UPDATE catalogue_assets SET deliverable_register='BOGUS-VALUE' WHERE asset_uid=1;"
Error: stepping, CHECK constraint failed: deliverable_register IN (...)   ← CHECK enforced
```

Schema v1.1 holds under empirical 48-row pressure with all CHECK constraints enforced. The 47 existing v1.0 rows are preserved (no back-fill required; `deliverable_register=NULL` is valid).

### Open follow-ons (NOT elrond-blocking)

1. **catalogue-schema.md v1.1 doc update** — design doc should be amended to reflect: § 3.2 (`register_mixed` column on catalogue_sources), § 3.4 (`deliverable_register` column on catalogue_assets), § 4 (deliverable_register enum value-set table parallel to license taxonomy), § 5 (new worked-example query for cross-register-safety). Knight-rider sequences — small doc update; ~30 min effort.
2. **CraftPix vendor curation crawl** — Legolas Mode B dispatch to populate the 7 known CraftPix products (5 pixel-art-raster VFX + 2 vector-ai character; per `craftpix/full-2026-05-16.jsonl`) into catalogue.db, with per-product `deliverable_register` populated per persona-rule extension. Not in this dispatch's scope; queued for future activation.
3. **Drax bundle-pipeline matcher updates** — per recommendations in `pimen-bundle-follow-up-2026-05-16.md` §§ 1.recommendation, 2.recommendation, 3.recommendation. Drax-side implementation; knight-rider sequences if drax wants a focused matcher-improvement dispatch.
4. **Backfill `subpack_organization_style` + `bundle_folder_hint` at next curation pipeline pass** — both surfaced as amendment-time additions in this dispatch. Next pipeline pass (per v1.3 open follow-on #2) should promote to first-class curation-time fields.
5. **Visual-inspection queue grew to 23 rows** (was 22 in catalogue.db post-v1.3 — minor discrepancy with v1.3 curation-log's "21" claim worth noting; the 22-vs-21 delta predates this dispatch and is not investigated here). Icons sub-pack added at MEDIUM priority (bundle-internal; no incremental acquisition decision).
6. **Pre-v1.1 backup pruning** — `catalogue.db.pre-v1.1-backup` retained until next housekeeping pass (~1 week soft-retention).
7. **Generalization of `bundle-internal-only` operational pattern** — this is the first instance. Future bundle-inspections should reuse the `bundle_internal_only: true` + `bundle-internal-only:<bundle_id>` tag pair. Eventually candidate for first-class schema field if the pattern recurs.

---

## v1.3 — First live curation pass (Pimen full-catalogue, 47 rows) — 2026-05-16

### What changed (one line)

First end-to-end live application of the v1.0 catalogue schema: Pimen full-crawl raw extraction (46 rows) → curated rows (47 after category split) → ingest into `catalogue.db`; the four dispatch pre-processor rules + CC-BY tagging + bundle relationships + category split all landed without schema rework.

### Why (one line)

Closes the `2026-05-16-elrond-pimen-full-catalogue-curation` dispatch; first empirical validation that the v1.0 schema + rubric R5 cascade + curator-tagging conventions hold under live-data pressure; produces the first queryable catalogue dataset available to drax/star-lord/gandalf via the cross-store ATTACH pattern.

### Who's affected

- **Drax** — can now query `catalogue.db` for Pimen consumption (see `catalogue-schema.md` § 5.3 worked example). **Caveat:** outline-profile secondary tags (`outline-profile:hard-1px` vs `outline-profile:soft-or-variable`) are NOT yet populated for any Pimen row because `linework_style` is universally `unknown` until post-acquisition visual inspection — scene-coherence filter on outline-profile cannot constrain Pimen rows at this curation pass.
- **Gandalf** — viability-gate design-track queries are now executable against real Pimen data. Sample-time threshold (>20% `license = 'unknown'`) cleared trivially (0% unknown in Pimen).
- **Star-lord** — no immediate action; cross-store ATTACH pattern unchanged.
- **Legolas** — Pimen Mode B extraction format passed curation with 0 extraction errors. The format is operationally correct for downstream consumption; future Pimen crawls or other vendor crawls can use this as the reference shape.
- **Rocket** — unaffected.
- **Knight-rider** — receives this MIGRATION + dispatch-completion notification; sequences post-acquisition visual-inspection follow-on when Matt makes acquisition decisions on the 21 visual-inspection-queued rows.

### What downstream consumers need to do

**Drax:** query patterns per `catalogue-schema.md` § 5.3 work today. Constraining queries by outline-profile is currently a no-op for Pimen — flag for awareness. The locked-register query (`derived_register = 'hand-drawn-pixel'` + `license IN (commercial-OK set)` + `embodiment_tag != 'pending-amendment'` + `superseded_at IS NULL`) returns 27 rows; `quality_flag = 'pass'` filter is currently 0 (post-acquisition inspection promotes to `pass`).

**Star-lord:** no action.

**Gandalf:** when Pimen-acquisition decisions surface, design-track read of the queue's 21 visual-inspection rows is a candidate input. No active dispatch.

**Legolas:** Mode B format works. Future crawls can use this Pimen pass as the reference for "what shape elrond's curation accepts cleanly."

### Schema diff or example before/after

**Before:** `catalogue.db` empty (v1.0 schema applied but no data). `archive/` populated with retired stores (research.db + Yomi snapshot).

**After:**

```
catalogue.db
├── schema_meta            : 1 row (v1.0)
├── catalogue_sources      : 1 row  (itch-pimen)
├── crawl_sessions         : 1 row  (legolas-pimen-mode-b-full-2026-05-16)
├── catalogue_packs        : 3 rows (mega-pack-01, mega-pack-02, earth-spell-effect-03)
├── catalogue_assets       : 47 rows
├── asset_style_tags       : 444 rows (328 legolas-inferred + 116 elrond-curated)
├── catalogue_rejections   : 0 rows
└── abstraction_groupings  : 0 rows (stub)
```

**New files under `research/curated/`:**

- `pimen-catalogue-curated-2026-05-16.jsonl` (47 lines, JSON Lines format; one curated row per line)
- `pimen-bundle-relationships-2026-05-16.json` (2 bundles registered)
- `pimen-curation-log-2026-05-16.md` (full per-row decisions, queue disposition, schema verification)
- `pimen-full-catalogue-snapshot-2026-05-16-rows-only.txt` (auxiliary diagnostic — not committed)

**New file under `research/scripts/`:**

- `curate_pimen_full_2026_05_16.py` (one-shot curation tool; ~470 lines; stdlib only)

### Pre-processor rules applied (per dispatch)

1. **R5 derivation cascade** — `style_register: "pixel-art"` parent value resolves to one of `hand-drawn-pixel` (28), `retro-16bit` (2), or `manual-review` (17). Cascade prioritizes positive style_tags (`hand-drawn-pixel`, `retro` + band-coherence) over Legolas-flagged uncertainty (`sub-register-uncertain`). One vendor-hint-inferred case (`fantasy-skeleton-enemies`).
2. **`pimen_element` → source_metadata_raw + queryable tag** — 23 of 46 raw rows had non-null pimen_element; emitted as `asset_style_tags.tag = 'pimen-element:<value>'`. Vendor-namespaced prefix generalizes to future crawls.
3. **`file_format` prose parser** — closed-enum cascade with vendor-heuristic fallback for pimen's RAR-only strings; aseprite-negation guard ("No Aseprite files" correctly classified as `has_aseprite_source = false`). 25 `png-spritesheet` + 22 `png`.
4. **`requires_visual_inspection` flag** — 21 of 47 curated rows (20 `resolution_band = unknown` raw rows + 1 inherited by the split sister); queryable via `asset_style_tags.tag = 'requires-visual-inspection'` + `manual_review_queued = 1`.

### Operational decisions captured (curation log § 6)

- **Visual-inspection queue Option (b)** — 21 rows filed as sub-list with priority guidance (4 paid rows = HIGH, 16 free rows = MEDIUM, 1 split sister = HIGH, 2 mega-packs = LOW per constituent-coverage); deferred to a later inspection step paired with Matt's acquisition decision.
- **CC-BY 4.0 attribution** — 2 rows (`pixel-battle-effects`, `cutting-and-healing`) tagged via curation_attribution overlay + 3 queryable tags (`attribution-required`, `attribution-acquired-yet:false`, `license-specifics:cc-by-4.0`).
- **Bundle relationships** — both external JSON file + inline `in-bundle:<bundle_id>` tags (redundancy + queryability). Bundle-01 = 9 constituents ($34.21 sum, $12.75 sale = 63% discount); bundle-02 = 5 constituents (3 overlap with bundle-01 + 2 new) ($24.95 sum, $20.40 sale = 18% discount). Version-drift caveat surfaced (mega-02 may ship different versions of overlap rows).
- **Category split** (`earth-spell-effect-03`) — 1 row → 2 rows (vfx + enemy sister), shared `pack_id`. Sister tagged `embodiment_tag = 'pending-amendment'` with hint `'elemental humanoid form'` (per the narrative-layer amendment protocol).

### Pipeline rules NOT applied (deferred — curation log § 7)

- R6 outline-profile secondary tag (linework_style universally unknown until post-acquisition inspection)
- R7 boundary-cluster borderline default (no rows trigger R7 in this corpus)
- Pivot-insurance ledger format finalization (single-vendor data not yet pivot-meaningful)
- Standing `manual-review-queue.md` and `pipeline-runs.md` (deferred until first multi-pass cycle)

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** no schema change in this pass; v1.0 lock holds.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement. No engine-telemetry or other-seam schema changed.
- **ADR-006 (external system writes require authorization):** writes confined to elrond-owned paths (`research/curated/*`, `research/scripts/*`, `catalogue.db`). No engine-side mutation.
- **ADR-007 (survey-mode):** the curation log reports what exists (47 curated rows, decisions per row); separates "what is" (§§ 1-5) from "what's queued" (§ 2 visual-inspection) from "what's deferred" (§ 7).

### Verification

```
$ python3 agentic_orchestration/research/scripts/curate_pimen_full_2026_05_16.py
[load] 46 raw rows from full-2026-05-16.jsonl
[curate] 47 rows after category split
[write] .../pimen-catalogue-curated-2026-05-16.jsonl
[write] .../pimen-bundle-relationships-2026-05-16.json
[ingest] {'assets_inserted': 47, 'tags_inserted': 444, 'packs_registered': 3}
[summary] derived_register: {'manual-review': 17, 'hand-drawn-pixel': 28, 'retro-16bit': 2}
[summary] quality_flag:     {'deferred': 17, 'unreviewed': 29, 'borderline': 1}
[summary] license:          {'commercial-royalty-free': 45, 'CC-BY': 2}

$ sqlite3 catalogue.db "SELECT COUNT(*) FROM catalogue_assets;"
47

$ sqlite3 catalogue.db "SELECT version FROM schema_meta;"
1.0
```

Schema v1.0 holds under empirical 47-row pressure with 0 CHECK-constraint failures.

### Open follow-ons (NOT elrond-blocking)

1. **Visual-inspection queue drain** — 21 rows queued in catalogue.db (`manual_review_queued = 1`). Paired with Matt's acquisition decision moment, OR knight-rider sequences as separate dispatch. ~2 min per asset.
2. **Curation-pipeline generalization** — this pass is one-shot for Pimen. Future vendor crawls (CraftPix, CreativeKind) want a generalized `curate_catalogue.py` per `curation-pipeline.md` § 10. Estimated 1-2 days when the second-vendor crawl lands.
3. **Pivot-insurance ledger format finalization** — deferred until a second-register vendor (e.g., a retro-16bit source) lands. Pimen-only is pivot-meaningless.
4. **`embodiment-narrative-layer.md` cross-reference for `elemental` form** — gandalf-owned. Pressure low (one row); will accumulate.
5. **Post-acquisition visual-inspection workflow** — single-batch session per acquired pack, backfills axes 2-4 + finalizes resolution_band + clears manual_review_queued + promotes quality_flag from `unreviewed` to `pass`/`borderline`/`fail`.

---

## v1.2 — Yomi (season_002328) archive (Dispatch B Option 3) — 2026-05-16

### What changed (one line)

Archived `reincarnated-loadout/data/season_002328/` (Yomi season — 10 classes + manifest + gear_pool, 556 KB total) into elrond's `archive/yomi-season_002328-2026-05-13/` for four-deep redundancy on design-vocabulary-bearing data, complementing the loadout remote push (Option 2) earlier same session.

### Why (one line)

Closes the residual Yomi-specific redundancy gap surfaced by the provenance audit (`yomi-provenance-audit-2026-05-16.md`); applies the same four-deep redundancy standard the research.db retirement established to a second category of historical/design data; gives gandalf / drax / engine pipeline a stable file-system referent for Yomi independent of loadout app evolution.

### Who's affected

- **Gandalf** — Yomi remains a stable referent for design vocabulary (Lantern-Keeper, Pomegranate, miasma/lantern/brine/bone elements) even if the loadout app data evolves.
- **Drax** — no immediate action; the loadout app continues consuming `reincarnated-loadout/data/season_002328/` as before. The archive is a parallel copy, not a redirected source.
- **Star-lord** — the c1f02ca deterministic-replay fragility is documented in the provenance audit § 7 + this archive's companion markdown. Knight-rider sequences the engine-side note on `export/MIGRATION.md`.
- **Knight-rider** — receives this MIGRATION entry + archive completion notification; may draft a decisions-log entry codifying the side-seed-archive-on-import discipline if Matt wants it as a standing rule.

### What downstream consumers need to do

**No required action.** The archive is a redundancy layer, not a redirected source. Existing consumers continue reading from their existing paths:

- Loadout app: continues consuming `reincarnated-loadout/data/season_002328/` (working tree of loadout repo)
- Design docs in `canonical/story/`: continue prose-level references to Yomi (no path change)
- Engine pipeline: if/when Yomi is ever needed engine-side, either re-generate from seed=2328 (lossy — produces A Yomi, not THIS Yomi) or read THIS Yomi from the elrond archive

### Schema diff or example before/after

**Before:** `archive/` directory contained the research.db retirement archive only.

**After:**

```
agentic_orchestration/research/curated/archive/
├── research-db-2026-05-07.db                          (existing — research.db binary)
├── research-db-narrative-archive-2026-05-16.md        (existing — narrative archive)
├── yomi-season_002328-2026-05-13/                     (NEW — Yomi season data tree)
│   ├── manifest.json
│   ├── gear_pool.json
│   └── classes/class_0001.json ... class_0010.json
└── yomi-season_002328-2026-05-13.md                   (NEW — companion archive doc)
```

### Convention extension (v1.2)

The v1.1 archive convention established `archive/<store>-<as-of-date>.db` for SQLite binary preservation. v1.2 extends to directory-tree archives:

- **Filename pattern (directory tree):** `archive/<store>-<as-of-date>/` (no extension) + companion markdown `archive/<store>-<as-of-date>.md`
- **Filename pattern (SQLite binary):** `archive/<store>-<as-of-date>.db` (as v1.1) + companion markdown `archive/<store>-narrative-archive-<archive-date>.md`
- **`.gitignore` exception:** `!archive/*.db` (v1.1) covers binary case; directory-tree archives are not affected by `*.db` rule so no additional exception needed
- **Companion markdown required** in both cases — captures provenance, integrity hashes, status footer

### Cross-seam ADR compliance

- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement. No engine-telemetry or other-seam schema changed.
- **ADR-006 (external system writes require authorization):** the source `cp -r` is a read from loadout (permitted) + write to elrond seam (permitted, within own domain). No destructive ops on the source — loadout `data/season_002328/` is unmodified.
- **ADR-007 (survey-mode):** the companion markdown reports what exists (manifest values, class roster, integrity hashes) without interleaving prescriptive content.

### Verification

```
$ find archive/yomi-season_002328-2026-05-13 -type f | wc -l
12

$ diff <(find loadout/data/season_002328 -type f -exec shasum -a 256 {} \; | sort)
       <(find archive/yomi-season_002328-2026-05-13 -type f -exec shasum -a 256 {} \; | sort)
# (no output — byte-identical)

$ du -sh archive/yomi-season_002328-2026-05-13/
556K
```

### Housekeeping in same pass

- Removed WAL/SHM siblings (`research-db-2026-05-07.db-shm`, `-wal`) that had been auto-created on the research-db archive during my earlier SQL verification queries. They were operational noise, not canonical archive content. Post-removal, the research-db archive .db SHA-256 unchanged (`3846b98b…f96351e`).

### Open follow-ons (NOT elrond-blocking)

1. **Knight-rider decisions-log entry (optional)** — codifies side-seed-archive-on-import as standing discipline, if Matt wants it as a rule.
2. **Star-lord note** on `reincarnated-engine/src/reincarnated/export/MIGRATION.md` re: the c1f02ca deterministic-replay's silent assumption on `seasons/<id>/gear/catalog.json` persistence (the fragility that bit Yomi). Knight-rider sequences.
3. **Audit § 3.6 update** — points at the provenance audit + this archive. Folded into this pass.

---

## v1.1 — Archive directory + research.db retirement (Phase-1 cleanup, COMPLETE on elrond side) — 2026-05-16

### What changed (one line)

Added `archive/` subdirectory for durable historical SQLite snapshots; archived dormant `reincarnated-engine/research.db` (binary + narrative markdown); audit § 3.4 updated; Matt-authorized destructive removal of research.db + WAL/SHM siblings + empty engine-root telemetry.db executed 2026-05-16.

### Why (one line)

Closes the 2026-05-07 decisions-log deferral on research.db consolidation (Phase-1 cleanup per data-architecture audit § 7); establishes the `archive/` pattern for future historical preservation of retired data stores.

### Who's affected

- **Star-lord** — `scripts/db.py` and `scripts/capture-regression-baseline.py` still reference research.db; updates flow through knight-rider per ADR-004. Recommended one-liner for star-lord's MIGRATION.md captured in archive markdown § E.
- **Knight-rider** — drafts decisions-log entry per dispatch A item 3 ("research.db deprecation: archived to research/curated/archive/, removed from repo. Supersedes 2026-05-07 deferral").
- **All agents** — future references to research.db content should point at the archive markdown or binary snapshot, not the engine-repo path.
- **Elrond (self)** — `.gitignore` now contains `!archive/*.db` exception permitting intentional historical snapshots; future archived DBs follow the `archive/<store>-<as-of-date>.db` filename pattern.

### What downstream consumers need to do

**Star-lord:** at next session, remove research.db references from `scripts/db.py` (DB_PATH, init banner, docstring) and `scripts/capture-regression-baseline.py` (copy step, schema dump step, docstring listing). The script-level refactor is small (~10-line cleanup); a star-lord-side MIGRATION.md entry should accompany.

**Knight-rider:** draft decisions-log entry; sequence star-lord script cleanup.

**Other agents:** when referencing research.db content historically, link to `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md` (or the binary snapshot for structural recovery).

### Schema diff or example before/after

**Before:** No `archive/` directory under `research/curated/`. `reincarnated-engine/research.db` was the sole copy of the early-May Phase-0 research data.

**After:**

```
agentic_orchestration/research/curated/
├── archive/                                          (NEW directory)
│   ├── research-db-2026-05-07.db                     (NEW — binary snapshot, 2.6 MB)
│   └── research-db-narrative-archive-2026-05-16.md   (NEW — verbatim narrative + structural inventory)
├── .gitignore                                        (UPDATED — !archive/*.db exception added)
└── (existing files unchanged)
```

`reincarnated-engine/research.db` — UNCHANGED at archive time. PENDING Matt's `rm` authorization per ADR-006.

### Archive convention (new pattern established v1.1)

- **Path:** `agentic_orchestration/research/curated/archive/<store>-<as-of-date>.<ext>`
- **Companion markdown:** `archive/<store>-narrative-archive-<archive-date>.md` (provenance header, narrative content verbatim, structural-table schemas + counts, integrity hash, status section)
- **`.gitignore` rule:** `!archive/*.db` (intentional preservation; archives are durable historical records, not runtime DBs)
- **Integrity:** SHA-256 captured in companion markdown at archive time

### Cross-seam ADR compliance

- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement. Star-lord-side MIGRATION.md update is the cross-seam companion (knight-rider sequences with star-lord).
- **ADR-006 (external system writes require authorization):** the binary copy `cp research.db → archive/research-db-2026-05-07.db` is a read-from-engine + write-to-elrond-domain operation. The read is permitted; the write lands in elrond's owned path. The destructive `rm` on engine-side is held at the authorization gate.
- **ADR-007 (survey-mode):** the audit-update subsection § 3.4.1 reports what exists and what is pending; does not interleave "should" statements with descriptive findings.

### Verification

```
$ ls /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/archive/
research-db-2026-05-07.db
research-db-narrative-archive-2026-05-16.md

$ shasum -a 256 .../archive/research-db-2026-05-07.db
3846b98b272386dc946104676da7cff6ac1f86f529be195799af7b289f96351e

$ sqlite3 .../archive/research-db-2026-05-07.db ".tables"
   (returns the same 11-table inventory as the source)
```

### Destructive-op completion log (Matt-authorized 2026-05-16, ADR-006)

Authorization scope: explicit per-statement go-ahead on the four-file removal window. Executed by elrond, 2026-05-16:

```
rm /Users/admin/Games/reincarnated-engine/research.db        ✓ removed
rm /Users/admin/Games/reincarnated-engine/research.db-wal    ✓ removed
rm /Users/admin/Games/reincarnated-engine/research.db-shm    ✓ removed
rm /Users/admin/Games/reincarnated-engine/telemetry.db       ✓ removed (the empty 0 B root-of-repo orphan from audit § 3.1; bundled into the same authorization window)
```

Post-rm verification:
- All four file paths return "No such file or directory"
- `data/telemetry.db` (15.7 GB canonical telemetry) UNTOUCHED
- `git -C reincarnated-engine status --short` reports no new untracked artifacts (all four were `.gitignore`d; removal does not perturb git state)
- Archive at `agentic_orchestration/research/curated/archive/research-db-2026-05-07.db` remains the canonical historical record

### Open follow-ons (still pending — not elrond-blocking)

1. **Star-lord script cleanup** (scripts/db.py, scripts/capture-regression-baseline.py) — knight-rider sequences. Engine-side MIGRATION.md update accompanies. ~10-line cleanup.
2. **Knight-rider decisions-log entry** — closes the 2026-05-07 deferral.

---

## v1.0 — Initial catalogue schema lock — 2026-05-16

### What changed (one line)

Initial catalogue database schema and six-axis style register rubric locked v1.0 post-gandalf dialogue.

### Why (one line)

Operationalizes the locked HD-2D-pixel style register (`canonical/story/style-register.md`) into curator-checkable axes + DB schema, unblocking Legolas Pimen Mode B sample dispatch and downstream catalogue work.

### Who's affected

- **Legolas** — Mode B catalogue output now has a defined target schema. Pimen sample dispatch can proceed (was held pending this work).
- **Gandalf** — viability-gate design-track now has a queryable catalogue (once curated) for sample review.
- **Drax** — eventual consumption-time filter consumer; no immediate action.
- **Star-lord** — no immediate action; cross-store ATTACH-read-only pattern documented in `catalogue-schema.md` § 5.
- **Knight-rider** — receives this MIGRATION + dispatch-completion notification; draft decisions-log entry for the rubric lock per gandalf's commission item 5 + ADR-002 (cross-seam schema = Matt approval).

### What downstream consumers need to do

**Legolas:** continue Mode B output in JSON Lines per `~/.claude/agents/legolas.md` spec. Output is consumed by elrond curation script (forthcoming) which maps to catalogue.db. No schema changes Legolas-side.

**Gandalf:** at viability-gate sample-time, use queries in `catalogue-schema.md` § 5 (the default consumption filter and the form-bias case study) for design-track review. Strengthened sample threshold: >20% `license = 'unknown'` fails design track on data-hygiene grounds.

**Drax:** when first sample is curated and a downstream consumption need arises, query catalogue.db via the patterns in `catalogue-schema.md` § 5.3. The default filter includes `outline-profile:hard-1px` vs `outline-profile:soft-or-variable` constraint per scene — see `catalogue-rubric-schema.md` § 3.1.

**Star-lord:** no action. ATTACH-read-only pattern documented for future cross-store work.

### Schema diff or example before/after

**Before:** No catalogue.db. The curated/ directory contained only the data-architecture audit doc.

**After:** Five new design docs + one new DB file:

```
agentic_orchestration/research/curated/
├── data-architecture-audit-2026-05-16.md   (existing)
├── AGENT_STATE.md                          (existing — updated)
├── catalogue-rubric-schema.md              (NEW — six-axis rubric, locked v1.0)
├── catalogue-schema.md                     (NEW — DB schema, locked v1.0 design)
├── curator-tagging-guide.md                (NEW — per-axis curator instructions)
├── catalogue-rubric-validation-2026-05-16.md (NEW — validation pass on empirical vendors)
├── curation-pipeline.md                    (NEW — operational flow)
├── pivot-insurance-ledger.md               (NEW — pivot-insurance monitoring stub)
├── MIGRATION.md                            (NEW — this file)
└── catalogue.db                            (NEW — empty SQLite; gitignored)

agentic_orchestration/research/scripts/
└── catalogue_migrations/
    └── v1_0_initial.sql                    (NEW — migration script for the schema)

agentic_orchestration/research/curated/.gitignore
└── catalogue.db, *.db-wal, *.db-shm        (NEW — gitignore for SQLite files)
```

### Key design decisions baked in this v1.0 lock

Per post-dialogue lock with gandalf (full record in `catalogue-rubric-schema.md` § 9):

1. **Six-axis rubric** — five mechanically-checkable axes + one rule-derived. Closed enum value sets for two-curator convergence. Reasonable boundary cases captured in rules R6 (CreativeKind hard-outlined hand-drawn-pixel) and R7 (Foozle higher-tier boundary cluster with `quality_flag = 'borderline'` default).
2. **Per-asset granularity, not per-pack or per-vendor.** Schema tags each asset on all six axes. Pack-level `pack_register_consistency` is advisory only.
3. **Outline-profile secondary tag** auto-applied by curation pipeline on R6 outputs. Scene-level consumption filters constrain to one outline-profile (`hard-1px` vs `soft-or-variable`).
4. **Embodiment taxonomy v1.0** — eight starter forms (humanoid / slime / beast / dragonling / swarm / construct / spirit / plant) + `not-applicable` + `unknown` + `pending-amendment` (with `pending_amendment_hint` for curator-recorded form-read). New embodiments enter via narrative-layer amendment, NOT by pre-loading the catalogue.
5. **License taxonomy v1.0** — `commercial-license` split into four narrower values; `itch-standard` dropped (curators must read actual license); `unknown` license at >20% of sample fails viability-gate design track.
6. **Pivot-insurance ledger** — curation pipeline emits monitoring summary at each run, tracking per-register / per-embodiment coverage to surface silent pivot-insurance erosion.
7. **Curator-override threshold** — overrides exceeding 10% of corpus or clustering >5 on a single rule clause surface as rule-bug to elrond.
8. **`gandalf-call` reserved for register-genuinely-ambiguous cases**, not curator-vs-rule disagreements (those use `override`).

### Migration script

Schema applied to empty catalogue.db via `agentic_orchestration/research/scripts/catalogue_migrations/v1_0_initial.sql`. Reproducible — re-running on an empty DB produces the same schema.

### Verification

`sqlite3 agentic_orchestration/research/curated/catalogue.db .schema` produces the v1.0 schema as documented in `catalogue-schema.md` § 3.

`SELECT * FROM schema_meta;` returns the v1.0 row:
```
1.0|2026-05-16T<applied_at>Z|Initial catalogue schema; six-axis style rubric v1.0; embodiment tag aligned to embodiment-narrative-layer.md v1.0|catalogue_migrations/v1_0_initial.sql
```

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** the schema is **design-locked v1.0 but pending Matt approval** before live application to the project's curation workflow. The empty DB has been created in this dispatch to validate the schema applies cleanly; production use awaits Matt's go-ahead.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this file fulfills the requirement. star-lord-side telemetry MIGRATION.md is unaffected (no engine-telemetry change in this work).
- **ADR-006 (external system writes require authorization):** the empty catalogue.db file creation is a one-time elrond-domain operation in elrond's owned path; no engine telemetry or other seam DB was touched.

### Drax wiring-track flag responses (resolved in v1.0)

Per drax's wiring-track review at `agentic_orchestration/qa/findings/2026-05-16-drax-elrond-schema-wiring-review.md` (verdict: PASS WITH FLAGS):

- **Flag 1 — `file_format` underspecified for sprite-sheet consumption.** RESOLVED IN v1.0. Added CHECK constraint with closed enum to `catalogue_assets.file_format`: `'png'`, `'png-spritesheet'`, `'aseprite'`, `'svg'`, `'gif'`, `'jpg'`, `'mp4'`, `'webm'`, `'json-atlas'`, `'tmx'`, `'wav'`, `'mp3'`, `'ogg'`, `'ttf'`, `'otf'`, `'other'`, `'unknown'`. Curators cannot diverge on format strings; demo wiring can rely on enum-stable values. Smoke-tested: `INSERT ... file_format = 'BOGUS-FORMAT'` rejected by CHECK; `'png-spritesheet'` succeeds.

- **Flag 2 — Confidence threshold convention for loadout tag display.** DEFERRED. Per drax's own recommendation ("low priority; defer to drax S1 dispatch"). When catalogue tags surface in the loadout app UI, drax authors the rendering convention. No schema change.

- **Flag 3 — `'itch-standard'` still in `catalogue_sources.default_license` CHECK + `catalogue_packs.pack_license` CHECK.** RESOLVED IN v1.0. The migration SQL (v1_0_initial.sql) had already dropped `'itch-standard'` from both — gandalf dialogue Topic 5 outcome was applied consistently. The catalogue-schema.md design doc had a stale earlier-draft reference in two places; both updated. Smoke-tested: `INSERT INTO catalogue_sources VALUES (..., default_license='itch-standard', ...)` rejected by CHECK.

### Open follow-ons (not blocking the lock)

1. **`embodiment-narrative-layer.md` cross-reference update** — gandalf to author a cross-reference acknowledging the catalogue's `pending-amendment` pattern as the schema-side companion to the narrative-layer amendment protocol. Elrond surfaces this to knight-rider; not done unilaterally (gandalf owns that doc).
2. **Knight-rider decisions-log entry** — per gandalf's commission item 5 + ADR-002, the rubric lock + cross-seam schema needs decisions-log capture. Knight-rider drafts when this dispatch is acknowledged.
3. **Legolas Pimen sample dispatch release** — was held pending this rubric lock. Now unblocked. Knight-rider sequences release at convenient time.
4. **Curation script implementation** — `research/scripts/curate_catalogue.py` (per `curation-pipeline.md` § Tool). Implementation deferred until first Legolas sample lands (no point implementing curator pipeline before there's data to curate).
5. **Form-bias gap-fill consideration** — validation pass surfaces thin coverage in `hand-drawn-pixel` for slime / swarm / plant / dragonling / construct / spirit embodiments. Form-bias work (doc 37 § 4) should sequence either targeted Legolas commissions, LLM image generation, or deferred non-humanoid coverage. Surfaced as input, not blocked.

---

## 2026-06-13 — FACTION_LOOKUP_TABLE Q10 redraw populated (schema_version 1.0 -> 1.1)

**Dispatch:** `agentic_orchestration/dispatches/2026-06-13-elrond-q10-faction-lookup-table-redraw.md` (Gate-1 PASS).
**Owned data layer:** `reincarnated-engine/data/identity/faction_lookup_table.json` (elrond owns `records[]` content; rocket owns the loader `src/reincarnated/generation/identity_sampling.py`).
**Builder script (reproducible):** `agentic_orchestration/research/scripts/build_faction_lookup_table_q10_2026_06_13.py` — re-run to regenerate the table verbatim.

### What changed
- `records[]` populated from empty stub to **637 records** (one exact `(lineage, period, register)` entry per non-void cell the sampler can produce).
- `schema_version` bumped `1.0 -> 1.1` (content population; NO schema-shape change — the record key contract `{lineage, period, register, faction}` is rocket's existing loader contract, confirmed unchanged before authoring).
- Added a `factions[]` roster field (9 factions) for legibility; void_override_* fields preserved verbatim from the stub.

### Q10 redraw (Matt-ratified 2026-06-12; executed 2026-06-13)
8 redrawn faction homes + 1 composite ninth. Faction is **lineage-anchored** per Session 2 § 7.2 (cultural lineage is the primary key; period/register are secondary descriptors):

| Faction | Lineage(s) homed |
|---|---|
| Iron Covenant | western_european_germanic |
| Shadow Courts | western_european_gothic |
| Rune-Clans | norse_germanic_celtic |
| Bronze Sanctum | greek_roman |
| Sunfire Dominion | middle_eastern_persian, north_african_egyptian |
| Eternal Dynasties | east_asian_chinese, east_asian_japanese, east_asian_korean |
| Forge Republics | pan_industrial |
| **Solar Pantheon (composite ninth)** | mesoamerican, sub_saharan_african, south_southeast_asian |
| Void Covenant (override, not in records) | void_liminal lineage + cosmic_horror/void_arcane registers |

**Why a composite ninth (Solar Pantheon) was needed, not absorption:** the three formerly-homeless lineages are cosmologically distinct from each other AND from the existing eight; the Q10 ruling itself rejects absorbing them (e.g. obsidian-priest -> Sunfire Dominion by tie-break). They share one real, non-token thread — divine-kingship + ancestral pantheons + sun/serpent cosmology rendered in stone and bronze, outside the Euro-Sinitic-MENA axes. Solar Pantheon is a real home with mythological / high_fantasy / primal_shamanic register coherence.

### Loader contract confirmation (cross-seam discipline — done BEFORE authoring)
Read rocket's `derive_faction` / `FactionTable` in `identity_sampling.py`. Contract: exact index on `(lineage, period, register)`; Void override fires FIRST (before records); nearest-match score `register*4 + lineage*2 + period*1`. **Satisfiable with content alone — no loader shape change needed.** Did NOT touch rocket's loader.

- `void_liminal` lineage + `cosmic_horror`/`void_arcane` registers are **intentionally absent** from records (consumed by the Void Covenant override before record lookup). Emitting them would be dead cells.

### Empirical check (Q10 acceptance — nearest-match never reached by construction)
Exercised rocket's real loader (`load_faction_table` + `derive_faction`) over the full 14×7×9 = **882-cell** sampler space:
- exact: **637** | override (Void): **245** | nearest: **0** | unassigned: **0**
- distinct factions produced: **9** (all 8 record-factions + Void Covenant)
- **0 nearest-match cells, 0 UNASSIGNED** — no lineage routes through fallback by construction. rocket's nearest-match logging is the standing empirical proof.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. Loader-contract confirmation logged; no engine-telemetry change; star-lord-side MIGRATION.md unaffected.
- **Cross-seam contract change?** No — content population of an existing schema shape; rocket's loader untouched.
- Push to remote deferred to keystone-close (Matt's gate).

---

## 2026-06-17 — Synty catalogue multi-axis tagging (synty_catalogue.db 1.0 -> 1.1, ADDITIVE)

**Commission:** `agentic_orchestration/gandalf/requests/2026-06-17-elrond-catalogue-multiaxis-tagging.md` (Q2 gate 1 — gear-spec upstream-wiring decision).
**Owned data layer:** `agentic_orchestration/research/curated/synty_catalogue.db` (separate DB; gitignored/regenerable).
**Tagging script (reproducible):** `agentic_orchestration/research/scripts/tag_synty_multiaxis_2026_06_17.py` — re-run `all` to reproduce verbatim. Idempotent; ADDITIVE only.
**Deliverables:** `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.{jsonl,md}`.

### What changed (ADDITIVE — no destructive change)
- Added 10 nullable columns to `packs` via `ALTER TABLE ADD COLUMN` (zero existing-row rewrites; 62,281 asset rows untouched):
  `register`, `contribution_role`, `contribution_basis`, `time_period_proposed`, `time_period_basis`,
  `cultural_identity_proposed`, `cultural_mode_flag`, `cultural_basis`, `seam`, `tagged_at`.
- Tagged **all 157 pack rows** (156 content collections; Water Guns ships 2 FBX packs) on 5 axes. Zero nulls — every pack routes.
- `synty_catalogue` schema_meta bumped `1.0 -> 1.1`. (Distinct from the sprite-rubric `catalogue.db` schema lineage above — separate DB, separate schema_meta.)

### Axis discipline (substrate-led split — brief §2)
- **Axes 1 (register) + 5 (seam): substrate-GIVEN** — parsed from Synty pack naming + light curation. AUTHORITATIVE.
- **Axis 2 (contribution_role): doc-DERIVED** — gear-spec asset-class × skinned/static split. Every pack routes:
  environment 89 / armor-base-skinned 38 / ui 8 / bestiary 7 / anim 6 / accent-attach-static 6 / weapon-base-static 3.
  The 34 POLYGON armor-base-skinned packs = the consumption-line restyle base (register filter keeps POLYGON; MINI+SIMPLE corpus-retained, set-aside).
- **Axes 3 (time_period) + 4 (cultural_identity): substrate-VOTED — PROPOSALS ONLY.** The DB holds elrond's proposed
  stratum + a `*_basis` evidence column (the name-token the proposal rests on); the MD deliverable carries rep examples
  per stratum. **gandalf curates the final semantic label at a rep-audit** (semantic-layer rep-audit discipline #25 — substrate
  vote binds at the geometry layer, NOT the semantic layer). Period/culture-agnostic packs (animation, ui, weapon-only, FX,
  seasonal, animal, generic-interior) carry `unresolved` — intentionally NOT hand-labeled; flagged for gandalf.
- `cultural_mode_flag` guards the Mode A/B/C/D collapse: A=geographic-origin, B=cultural-tradition, C=naming-allusion
  (NOT a real culture — e.g. dwarven/elven/sci-fi), D=metadata/no-cultural-read.

### Density-map findings (the gap-fill routing surface — brief §3)
- **Finding 1 (headline):** POLYGON sci-fi humanoid skinned-character coverage EXISTS (~110 chars: Sci-Fi City 40, Space 52,
  Cyber City 18). Brief premise ("only SIMPLE-Space-Characters") REFUTED by substrate. sci-fi-body does NOT require full
  gap-fill. UPDATES prior-canon "sci-fi = zero coverage, deferred v1.1+" entry.
- **Finding 2:** cultural coverage is ASYMMETRIC by layer — Egypt (0 chars / 28 weapons), Vikings (0-1 chars / 215 weapons),
  Samurai-Empire, Goblin, Knights ship rich environment+weapon but HOLLOW skinned-character base → character gap-fill forced.
- **Finding 3:** ZERO-coverage cultural registers (full image-to-3D/Sidekick route): Mesoamerican/Aztec, Indo-Asian,
  Persian/MENA, Sub-Saharan African — all 0 packs. Matches `canonical/48` non-Euro-Sinitic roster homes.
- **Finding 4:** Victorian-steampunk = 0 packs; industrial thin (WWI map + Trains only).
- **Finding 5:** Sidekick Character Creator (157753) is the gap-fill MECHANISM, not a content pack (correctly absent from 157 DB rows).
  WAVE-2 extracted packs contribute the accent silhouette-breaker layer; WAVE-1 FBX packs the skinned-armor bases.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected.
- **Cross-seam contract change?** No — additive tagging on elrond-owned synty_catalogue.db; no consumer-contract reshape.
  Axes 3+4 are PROPOSALS pending gandalf rep-audit curation (Tier-2 escalation, NOT elrond-decided).
- **Reversibility (schema principle):** raw asset classification preserved; contribution_role routing corrects above the
  upstream SK_Veh_/SK_Bld_ false-positive without rewriting asset rows. Re-runnable from script.
- Push to remote deferred to KR's gate (Matt authorization).

---
