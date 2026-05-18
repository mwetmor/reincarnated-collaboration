# MIGRATION — Catalogue Data Layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema migrations for non-engine data layers under `agentic_orchestration/research/curated/`. Currently: catalogue.db.
**Pattern:** parallels star-lord's engine-side `MIGRATION.md` files per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

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
