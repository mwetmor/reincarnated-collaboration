# MIGRATION — Catalogue Data Layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema migrations for non-engine data layers under `agentic_orchestration/research/curated/`. Currently: catalogue.db.
**Pattern:** parallels star-lord's engine-side `MIGRATION.md` files per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

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
