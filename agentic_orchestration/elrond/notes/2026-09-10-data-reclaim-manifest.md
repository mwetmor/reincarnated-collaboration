# Data-reclaim manifest — elrond seam — 2026-09-10

**Dispatch:** DISK-RECLAIM, conductor gandalf. Matt-ruled GO with binding constraint:
*"I don't want to lose data we will need to reference later."* Conservative default = KEEP.

**Total freed: 3,716,000 KB ≈ 3.54 GiB**

| Scope path | Before | After | Freed |
|---|---:|---:|---:|
| `~/Games/reincarnated-engine/data/` | 34,791,248 KB | 34,791,248 KB | **0** (see §1 — no reclaim available) |
| `agentic_orchestration/elrond/research/` | 2,544,592 KB | 214,256 KB | **2,330,336 KB** |
| `agentic_orchestration/research/curated/` | 1,744,636 KB | 358,972 KB | **1,385,664 KB** |

No commits made (conductor centralizes). No pushes. No tracked file deleted.

---

## 0. Predicate gates (machine-checked, applied to every deletion)

**Gate A — git-tracked?** `git -C <repo> ls-files <path> | wc -l` must be 0.

- curated candidate set: 138 files → **2 were tracked** (`catalogue.db.pre-pixogen-2026-05-16-backup`,
  `catalogue.db.pre-v1.1-backup`) → both reclassified **KEEP** on predicate failure.
- elrond/research candidate set: 20 files → **0 tracked**.
- Post-deletion `git status --porcelain` over both scope dirs: **empty**. No tracked file touched.

**Gate B — cited in engine decisions-log?**
`grep` of `~/Games/reincarnated-engine/design/decisions/decisions-log.md` for
`pre-step`, `pre-stage`, `pre-phase`, `pre-wave`, `pre-sidecar`, `corpus.db.pre`,
`catalogue.db.pre`, `fixtures.db.pre`, `.bak`, `backups/`:

- `pre-stage` → 1 hit, line 520: `` Tag `v1.2-pre-stage-a2` `` — a **git tag name**, not an artifact citation.
- `.bak` → 5 hits under unescaped grep (`.` as wildcard); escaped `\.bak` → **0 hits**.
  The 5 were substring matches inside "baked" / "calibration". **False positives.**
- All other terms → **0 hits**.

**Verdict: no deleted artifact is cited by the decisions-log.**

**Gate C — canonical survivor verified.** For every deleted snapshot class, the surviving copy was
proven present, newer, integrity-ok, and a superset (§2, §3).

---

## 1. `~/Games/reincarnated-engine/data/` — 34.7 GB — **ENTIRELY KEEP, 0 freed**

Not my write-domain (star-lord owns engine telemetry). Diagnosed **read-only**; nothing deleted,
nothing vacuumed. Both parent DBs retained original mtimes after inspection (proof of non-mutation).

### KEEP structure — what the surviving 33 GB actually is

| Item | Size | Class | Note |
|---|---:|---|---|
| `telemetry.db` | 34,735,248 KB | engine telemetry (star-lord) | **99.84% of the pool.** See breakdown below |
| `kc2/` | 50,684 KB | engine run artifacts | 78 entries |
| `kit_space/` | 4,760 KB | engine generation data | |
| `seasonal_elements/` | 256 KB | engine generation data | |
| `identity/` | 96 KB | engine generation data | |
| `seasonal_anchors/` | 68 KB | engine generation data | |
| `emission_registry.db` | 44 KB | engine registry | |
| `synergy_priors/` | 40 KB | engine generation data | |
| `themes/` | 12 KB | engine generation data | |
| `research.db` | **0 KB** | empty | see §4 needs-Matt |
| `knowledge_base.db` | **0 KB** | empty | see §4 needs-Matt |

### Why no reclaim was available (the load-bearing finding)

Read-only diagnostics on `telemetry.db`:

- `page_size` 4096 × `page_count` 8,680,946 = 35.56 GB
- **`freelist_count` = 0** → *there are no free pages.* **A VACUUM would reclaim nothing.**
  All 33 GiB is live data. This rules out the obvious first move.
- mtime **2026-06-21 22:45** — 81 days stale. No WAL, not locked, no concurrent writer.

Per-table breakdown (`dbstat`):

| Table | MB | Share |
|---|---:|---:|
| **`class_fight_loadouts`** | **33,515** | **98.7%** |
| `idx_cfl_outcome` | 186 | |
| `idx_cfl_season_class` | 165 | |
| `llm_calls` | 12 | |
| `gear_instances` | 10 | |
| all others | <10 | |

`class_fight_loadouts` = **4,672,477 rows across 81 seasons**, avg ~7.3 KB/row.
The weight is the `loadout_json TEXT` column — a full `GearInstance.model_dump()` per slot,
stored once **per fight**.

**Negative result (recorded so it is not re-tried).** The intuitive fix — dedupe repeated loadout
blobs — **does not work.** Probe on the largest season (`season_001005`, 1,611,300 rows, 10,299 MB):

```
rows_ = 1611300 | distinct_blobs = 1611300 | avg_bytes = 6702 | total_mb = 10299
```

`distinct_blobs == rows` exactly. Every blob is unique (gear instances carry unique rolls/ids).
**Dedup reclaims zero.** The only real axes are (a) row-pruning by season, (b) column compression,
(c) normalizing gear instances into `gear_instances` and storing slot→id refs.

Season concentration (top 5 of 81): `season_001005` 1,611,300 (34.5% of all rows) ·
`season_000043` 334,569 · `season_099001` 214,800 · `season_001006` 188,600 · `season_099002` 187,200.

**Routing: this is star-lord's call, not mine.** Pruning superseded seasons' fight-level loadout
detail is the single highest-value reclaim on the machine (~10 GB from `season_001005` alone),
but it is engine telemetry and requires a star-lord + Matt ruling. Flagged, not acted on.

---

## 2. `agentic_orchestration/research/curated/` — freed 1,385,664 KB

### Class: superseded pre-migration DB snapshots → DELETE

**133 files deleted** (backup snapshots + their `.md5.txt`, `-shm`, `-wal` sidecars).

**Rationale — the seam's own written doctrine.** `curated/.gitignore` already states this class's
disposition verbatim:

> *"Pre-migration file-copy backups (elrond curation discipline) — **local safety nets, not durable
> records.** The committed migration/curation scripts guarantee byte-identical rebuild, so these
> regenerable backups + their transient WAL/SHM sidecars stay uncommitted. (Durable historical
> snapshots go in `archive/` instead — whitelisted below.)"*

So this class is **DERIVED/regenerable by my seam's standing policy**, and the durable-record home
is `archive/`, which is retained in full.

**Regeneration recipe:** each snapshot is a pre-state of `corpus.db` / `fixtures.db` reachable by
replaying the committed migration scripts under
`agentic_orchestration/research/curated/scripts/` and `.../scripts/catalogue_migrations/`
against the retained predecessor, in the order documented by the retained `MIGRATION-*.md` files
(all 40+ migration docs are git-tracked and were **not** touched).

Largest items deleted (full per-item list preserved in the run's size ledger):
`corpus.db.pre-bridge-m4` 95,380 KB · `pre-bridge-m3` 94,420 · `pre-vfx-x4` 91,444 ·
`pre-vfx-p2-supplement` 91,412 · `pre-vfx-p2` 91,176 · `pre-vfx-p1` ×3 ~91,000 each ·
`fixtures.db.pre-v0.6-…174909Z` 52,048 · `pre-v0.5` ×2 50,980 · `pre-bridge-m2` 28,812 ·
`pre-bridge-m1` ×2 ~18,852/15,392 · the `vdm1-ingest1…18` chain · the `v7…v11` census chain.

### KEEP

| Item | Size | Class | Rationale |
|---|---:|---|---|
| `corpus.db` | 94,432 KB | CURATED canonical | live store, 55 tables, `integrity_check=ok` |
| `fixtures.db` | 52,260 KB | CURATED canonical | live store, `ok` |
| `synty_catalogue.db` | 14,320 KB | CRAWLED canonical | live store, `ok` |
| `catalogue.db` | 384 KB | CURATED canonical | live store, `ok` |
| `corpus.db.pre-geomvocab-20260825T162203Z-backup` | 91,464 KB | rollback net | **newest** corpus snapshot — retained as live reversal window |
| `fixtures.db.pre-v0.6-20260728T175004Z-backup` | 52,048 KB | rollback net | **newest** fixtures snapshot (later label; mtimes tied) |
| `catalogue.db.pre-pixogen-2026-05-16-backup` | 364 KB | **predicate failure** | git-tracked → KEEP |
| `catalogue.db.pre-v1.1-backup` | 356 KB | **predicate failure** | git-tracked → KEEP |
| `atlas/` | 39,600 KB | DERIVED-but-cited | abstraction-analysis output |
| `kits-export/` | 7,132 KB | curated export | |
| `archive/` | 3,204 KB | **durable historical** | the whitelisted durable-snapshot home — never a delete candidate |
| `vdm2-exports/` | 1,316 KB | curated export | |
| `scripts/` | 208 KB | regeneration recipes | **required** for the recipe above |
| all `MIGRATION*.md`, `*.jsonl`, `*.log`, `*-log.md` | — | records | untouched |

**Retention rule applied:** keep the newest snapshot per live lineage as a genuine rollback net,
delete the superseded chain behind it. This is stricter than the `.gitignore` doctrine (which would
permit deleting all of them) and is the conservative reading of Matt's constraint. Cost: 143 MB retained.

**Post-deletion verification:** all four canonical DBs re-checked — `corpus.db ok`, `fixtures.db ok`,
`catalogue.db ok`, `synty_catalogue.db ok`.

---

## 3. `agentic_orchestration/elrond/research/` — freed 2,330,336 KB

### ⚠ The filenames were misleading — this needed a correction mid-dispatch

The 2.4 GB pool is `*/backups/telemetry.db.pre-*` files. **They are not telemetry databases.**
Opening them showed the **crawled weapons substrate** schema:

```
weapons · weapon_sources · weapon_knowledge_entries · weapon_sim_props · weapon_tags
weapon_aesthetic · weapon_readiness · clusters · cluster_membership
knowledge_entry_canonical_merge · knowledge_entry_reference_images
knowledge_model_attachments · libraries · licenses · tag_taxonomy · substrate_density
```

That is **CRAWLED data** (Legolas Mode B: wikidata, wikipedia, Met Museum, Royal Armouries,
osrsbox-db, cataclysm-dda, odin-army-tradoc) — expensive-to-impossible to re-acquire, i.e. the
KEEP-by-default class. The `telemetry.db.pre-*` naming is a copy-paste convention artifact and
actively misleads. Combined with engine `research.db` and `knowledge_base.db` both being **0 bytes**,
this triggered a full stop and a hunt for the surviving canonical copy before any deletion.

### Surviving canonical copy — located and verified

**`~/Games/reincarnated-loadout/data/telemetry.db`** (215,773,184 bytes, mtime **2026-06-14 22:42**).

| Check | Snapshot chain (May 23–25) | Surviving copy (Jun 14) |
|---|---:|---:|
| `integrity_check` | ok | **ok** |
| `weapons` | 5,162 | 5,162 |
| `weapon_knowledge_entries` | 89,839 – 89,971 | **90,345** (superset) |
| `clusters` | 0 – 125 | 125 |
| `cluster_membership` | — | 48,430 |
| `weapon_sim_props` | — | 2,601 |
| table set | subset | superset |

**Coverage proof (`ATTACH` + `EXCEPT`, newest snapshot vs surviving copy):**

```
weapons_missing|0
clusters_missing|0
sources_missing|0
kentry_missing|0
simprops_missing|0
```

**Zero records in the snapshot chain are absent from the surviving copy.** The June copy is newer,
integrity-ok, and a strict superset. The snapshots are therefore genuinely *superseded snapshots of a
surviving canonical copy* — the exact DELETE-eligible condition the dispatch names.

Secondary support: every `backups/.gitignore` in this tree states the policy explicitly —
*"DB backup files — never commit (~150–200 MB each) … Backup naming convention: telemetry.db.pre-\<step\>"*.
The migrations these guarded (Phase D cleaning pipeline, cycle-10 stages 1.5/2.5/3, wave 5.5,
sidecar-b) completed in May 2026 and have been built upon for 3.5 months; the rollback window is
closed in practice.

### DELETE — 19 files, 2,329,976 KB

| File | KB |
|---|---:|
| `phase-D-cleaning-pipeline-2026-05-23/backups/telemetry.db.pre-step7-2026-05-23` | 155,152 |
| `…/pre-step6.5-2026-05-23` | 150,680 |
| `…/pre-step6-2026-05-23` | 150,660 |
| `…/pre-step5-2026-05-23` | 150,536 |
| `…/pre-step4-2026-05-23` | 147,912 |
| `…/pre-step3-2026-05-23` | 147,732 |
| `…/pre-step2-2026-05-23` | 143,420 |
| `…/pre-step1-2026-05-23` | 139,232 |
| `…/pre-schema-migration-2026-05-23` | 139,228 |
| `cycle-10-stage-3-2026-05-25/backups/telemetry.db.pre-phase-2` | 165,584 |
| `cycle-10-stage-3-2026-05-25/backups/telemetry.db.pre-phase-0a` | 165,548 |
| `cycle-10-wave-5-5-2026-05-25/backups/telemetry.db.pre-wave-5-5` (+`-shm`,`-wal`) | 208,104 |
| `cycle-10-stage-2-5-2026-05-24/telemetry.pre-stage-2-5.db.bak` | 163,332 |
| `cycle-10-stage-1-5-2026-05-24/backups/telemetry.db.pre-stage-1-5-2026-05-24` | 154,104 |
| `phase-D-bis-step-6-6-2026-05-23/backups/telemetry.db.pre-step6.6` (+`-shm`,`-wal`) | 148,756 |
| **total** | **2,329,976** |

Plus **360 KB** of orphaned `-shm`/`-wal` sidecars whose parent DB was deleted.

**Re-fetch / regeneration recipe.** Restore from the surviving canonical copy
`~/Games/reincarnated-loadout/data/telemetry.db`, then replay the committed per-step scripts —
all **git-tracked and retained**: `phase-D-cleaning-pipeline-2026-05-23/scripts/`,
`cycle-10-stage-1-5-2026-05-24/scripts/`, `cycle-10-sidecar-b-2026-05-25/scripts/01_schema_extension.py`
and `02_offhand_mining_and_legolas_insert.py`, `cycle-10-stage-3-2026-05-25/populate_v1_scope.py`
and `classify_accessory_armor_subcategory.py`, `cycle-10-wave-5-5-2026-05-25/classify_tier_a_subtype.py`
and `mode_c_eviction.py`. The per-step JSON run-logs under each `logs/` dir are git-tracked and
retained, so each step's inputs/outputs remain auditable without the binaries.

### KEEP

- **`cycle-10-sidecar-b-2026-05-25/backups/telemetry.db.pre-sidecar-b` (207,612 KB) — RETAINED
  deliberately as a second physical copy of the crawled substrate**, not because it holds unique
  rows (it does not — coverage proof above is zero-missing) but because the surviving canonical copy
  is a *single untracked file on one disk* (§4). At 8% of this pool it is cheap insurance and is the
  conservative reading of Matt's binding constraint. Verified post-deletion: `integrity_check=ok`,
  `weapons=5162`.
- All `scripts/`, `logs/`, `*.json` classification/sample outputs, `*.py`, `*.out`, `.gitignore`
  files — untouched (124 git-tracked files in this tree, all intact).
- `cosmograph-substrate-trace-2026-06-06/` (960 KB, parquet + json, git-tracked) — KEEP.

---

## 4. Flagged — needs Matt / cross-seam routing

**(a) The crawled weapons substrate has a single-point-of-failure durability gap. [highest concern]**

The canonical copy of 5,162 weapons / 90,345 knowledge entries / 125 clusters — the accumulated
Legolas Mode B crawl across 7+ external sources — lives at
`~/Games/reincarnated-loadout/data/telemetry.db`. It is:

- **untracked** (`git ls-files data/telemetry.db` → 0) — no remote, no history;
- located in **drax's loadout repo**, not in the data seam that owns it;
- named `telemetry.db`, which actively disguises it as engine telemetry;
- while the engine's nominal homes for it, `data/research.db` and `data/knowledge_base.db`,
  are both **0 bytes**.

This is not a disk-space issue and I did not act on it. But the reclaim surfaced it, and it is the
single most fragile thing I found. Recommendation: promote this store into the data seam under a
truthful name, with a durable `archive/` snapshot per my own retained convention. I have kept one
independent physical copy in the meantime (§3 KEEP).

**(b) `engine data/telemetry.db` — ~10–30 GB reclaim exists but is star-lord's.**
`class_fight_loadouts` is 98.7% of a 33 GiB file; VACUUM yields nothing (freelist=0); dedup yields
nothing (blobs unique). Season-pruning or gear-instance normalization are the live options.
`season_001005` alone is 34.5% of rows / ~10 GB. Needs star-lord + Matt.

**(c) Adjacent reclaim outside my scope, ~1.05 GB, in drax's repo.**
`~/Games/reincarnated-loadout/data/` holds 5 further substrate snapshots of the same superseded
class (`telemetry.db.pre-50-50-adjudication-2026-06-14.bak`, `pre-magic-anchor-simprops-2026-06-14.bak`,
`pre-ia-2-phase-3-2026-06-01.bak`, `pre-substrate-enrichment-2026-05-27.bak`, `pre-sc6b-2026-05-27.bak`),
~215 MB each, all untracked. Same analysis applies — **but** they are currently the only redundancy
protecting the canonical copy they sit beside, so (a) should be resolved *before* they are reclaimed.

**(d) Naming defect worth a convention fix.** Substrate snapshots named `telemetry.db.pre-*` nearly
caused an irreversible misclassification: the dispatch's own framing treated this tree as telemetry
backups (DERIVED), when the contents are CRAWLED. Schema and filenames should make the underlying
truth visible; these did the opposite. Recommend renaming the convention to `substrate.db.pre-*`.

---

## 5. Side effects and hygiene

Read-only `sqlite3` inspection creates `-shm`/`-wal` sidecars as a side effect of opening a DB.

- Sidecars my scan created in **engine `data/`** and **loadout `data/`** were removed; both
  directories were restored to their exact pre-inspection state, verified by listing and by
  `git status` on the loadout working tree.
- Both parent DBs retained original mtimes (engine `2026-06-21 22:45`, loadout `2026-06-14 22:42`),
  **proving the inspection did not write.** All WAL files were 0 bytes before removal (no pending writes).
- Sidecars under `engine/src/`, `engine/baseline/`, `agentic_orchestration/factory/` and
  `cycle-14-wave-5-season-00*/` had **pre-existing** sidecars whose mtime my scan merely touched.
  I did **not** remove these — ~670 KB total, and star-lord has concurrent work in that territory.
  Documented rather than acted on.

**No commits. No pushes. No tracked file deleted. Both scope dirs report clean `git status`.**
