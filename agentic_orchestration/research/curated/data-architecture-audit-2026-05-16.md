# Data Architecture Audit — 2026-05-16

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-elrond-data-architecture-audit.md`
**Scope:** Read-only inventory + ownership map + architectural recommendations across all four repos and the new orchestration research surface.
**Verdict (one line):** The data layer is structurally sound at the seam level but has three concrete fragilities — a 15 GB telemetry hotspot driven by JSON-blob columns, a silent `engine/seasons/` → `loadout/data/` shape mismatch, and a dormant `research.db` whose deprecation has been deferred long enough to risk silent drift. The forthcoming catalogue layer fits cleanly as a fourth, independent data store. No emergency restructures recommended; three sequenced cleanups proposed.

---

## 1. Inventory

Every persistent data store across the four repos and the orchestration tree. Sizes and timestamps captured 2026-05-16.

### 1A. Engine repo (`~/Games/reincarnated-engine/`)

| Store | Path | Owner | Shape | Size | Rows / files | Last modified | Schema version |
|---|---|---|---|---|---|---|---|
| **telemetry.db** | `data/telemetry.db` | star-lord | SQLite (15 tables) | **15 GB** (+ WAL/SHM siblings) | 1,925,180 `class_fight_loadouts` rows; 23 seasons; see § 1A.1 | 2026-05-14 23:56 | 1.9 (10 migrations applied) |
| **telemetry.db (root)** | `telemetry.db` | (orphan) | empty file | 0 B | — | 2026-05-14 22:39 | n/a — see § 3.1 |
| **research.db** | `research.db` | (legacy; no current owner) | SQLite (11 tables) | 2.6 MB | season_000042 only (1 run); 13,040 fight_results; 5 research_notes; 5 bugs_log | 2026-05-07 05:12 (untouched 9 days) | undocumented |
| **seasons/** | `seasons/<season_id>/` | rocket (writer) → star-lord (exporter reader) | per-season directory: `manifest.json` (v1.3), `classes/*.json`, `monsters/*.json`, `trial.json`, `gear/catalog.json`, `validation_report.json`, `reference_gauntlet.json`, `fights.jsonl`, `generation_log.txt` | **2.8 GB total** (e.g., season_001005 = 870 MB, fights.jsonl = 119K lines) | 23 seasons | rolling | manifest.json `1.3` (see `src/.../output/season_writer.py:125`) |
| **exports/** | `exports/<season_id>/` | star-lord | demo-shaped: `metadata.json` (v1.0), `classes.json` (single file), `monsters.json`, `gear_pool.json`, `damage_formula.md`, `design_context.md` | 2.5 MB total | 5 seasons (001001–001005); season_001005 = 516 KB | rolling | `format_version` 1.0 (gear_pool.json sub-schema bumped to 1.1 per export/MIGRATION.md) |
| **seasonal_elements pool** | `data/seasonal_elements/pool.json` + `.md` | rocket | JSON list of element records with D1 scoring | 60 KB | 156 element entries | 2026-05-13 02:03 | implicit `1.0` |
| **seasonal_anchors library** | `data/seasonal_anchors/library.json` + `.md` | rocket | JSON list of anchor records | 68 KB | n entries | 2026-05-08 | implicit `1.0` |
| **canonical_library** | `foundation/canonical_library.json` | rocket | engine internal canonical library (ability templates, geometry refs) | (see file) | n entries | 2026-05-07 | `1.0.0` |
| **config/** | `config/*.yaml` (attributes, color_spectrum, elements, resources, vocabularies) | rocket / shared | YAML reference data | small | 5 files | rolling | unversioned |
| **cache/llm** | `cache/llm/<sha>.json` | star-lord | LLM response cache (SHA-keyed) | 16 MB | many | rolling | cache convention |
| **logs/llm** | `logs/llm/` | star-lord | LLM call logs | 6.9 MB | rolling | rolling | text/jsonl |
| **baseline/** | `baseline/v1.2-pre-stage-a2/` | (process artifact) | regression-capture snapshot: DB copies + exports copies + checksums | 5.1 MB | one snapshot | 2026-05-12 04:51 | snapshot-time |
| **notes/, reports/, test-plans/** | (various) | mixed | working artifacts (markdown, ppt, xlsx) | 232 KB / 268 KB / 124 KB | scattered | rolling | n/a |

#### 1A.1 — `telemetry.db` table inventory (15 tables, ordered by row count)

```
class_fight_loadouts     1,925,180   (this single table dominates DB size; see § 3.2)
gear_instances               7,178
abilities                    4,561
gear_traits                  2,812
llm_calls                    1,991
monsters                     1,008
class_monster_win_rates        990
generation_steps               662
gear                           305
classes                        234
seasonal_elements               88
generation_runs                 68
trials                          25
seasons                         23
element_proposals                1
schema_meta                     11   (one row per applied migration)
```

Schema-meta version history (per `schema_meta` table):
- `1.0` (2026-05-08) — initial schema
- `1.1` (2026-05-08) — `llm_calls` table
- `1.2` (2026-05-08) — `seasonal_elements` + `element_proposals`
- `1.3` (2026-05-08) — Phase-1 dimensional refactor (`energy_type`, rename `mana_cost_pct` → `energy_cost_pct`)
- `1.4` (2026-05-08) — Phase-2 dimensional refactor (`role_orientation`)
- `1.5`, `1.6` (2026-05-09) — applied without description; intent unclear
- `1.7` (2026-05-09) — gear_instances flavor/visual/stat_requirements
- `1.8` (2026-05-09) — `class_fight_loadouts` table; `carried_gear` on classes
- `1.9` (2026-05-13) — `convergence_wall_time_seconds`, `seasonal_element_name` on classes; `termination_reason` on fight loadouts

Migration source: `src/reincarnated/telemetry/migrations.py` (489 lines).

### 1B. Loadout repo (`~/Games/reincarnated-loadout/`)

| Store | Path | Owner | Shape | Size | Files |
|---|---|---|---|---|---|
| **season_NNNN/** (sample-season + 5 numbered) | `data/<season_dir>/` | drax (consumer); star-lord (exporter for season_002328 gear_pool) | `manifest.json` (engine `seasons/` shape, `manifest_version: 1.2/1.3`) + `classes/class_NNNN.json` per-class files | 84 KB – 556 KB per season | 6 season folders (`sample-season`, `season_001001`–`001004`, `season_002328`) |
| `season_002328/gear_pool.json` | (within above) | star-lord (re-export sourced from `engine/exports/` shape) | `format_version 1.1` (export-style schema, post-MIGRATION.md additive stats fields) | 350 KB | 1 |
| **App source** | `src/data/`, `src/hooks/useSeasonData.ts` | drax | TS modules with `import.meta.glob` over `data/*/` | n/a | code |
| **deploy** | Vercel build artifacts | drax | derived | n/a | n/a |

**Loadout consumption pattern:** `useSeasonData.ts` uses Vite's `import.meta.glob` to eagerly load every `manifest.json` and every `classes/*.json` under `data/`. Sample-season is the canonical "current season" for Page 1; other folders feed analytics views. Page 1 (`Sample.tsx`) and Encounters page (`Encounters.tsx`) import `season_002328/gear_pool.json` and select per-class JSONs directly via static `import` statements.

### 1C. Demo repo (`~/Games/reincarnated-demo/`)

| Store | Path | Owner | Shape | Size | Files |
|---|---|---|---|---|---|
| **public/seasons/season_NNNN/** | `public/seasons/<season_id>/` | drax (consumer); star-lord (exporter) | demo-shaped — byte-identical hash to `engine/exports/season_NNNN/` (see § 4) | ~500 KB per season | 5 seasons (001001–001005) |
| **public/sprites/** | `public/sprites/` | drax | sprite assets | (not measured) | art |
| **public/audio/** | `public/audio/` | drax | audio | (not measured) | art |
| **App source** | `src/data/loader.ts` | drax | runtime `fetch('/seasons/<id>/metadata.json')` etc. | n/a | code |

**Demo consumption pattern:** runtime `fetch()` against `/seasons/<id>/` paths, parsing the export-shape `metadata.json`, `classes.json`, `monsters.json`, `gear_pool.json`. See `src/data/loader.ts:30-49`.

### 1D. Collaboration / orchestration repo (`~/Games/reincarnated-collaboration/`)

| Store | Path | Owner | Shape | Size | Files |
|---|---|---|---|---|---|
| **research/knowledge/** | `agentic_orchestration/research/knowledge/<topic>/` | legolas (Mode A) | per-topic markdown findings; one file per commission | 6.6 KB so far | 1 file (`asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`); 5 empty topic subdirs awaiting Mode A passes |
| **research/catalogue/** | `agentic_orchestration/research/catalogue/` | legolas (Mode B raw) | will be JSON Lines / CSV per source | empty | 0 |
| **research/curated/** | `agentic_orchestration/research/curated/` | **elrond** | curated state (to be populated); will host catalogue.db | empty (this audit is the first file) | 0 |
| **research/commissions/** | `agentic_orchestration/research/commissions/` | knight-rider + gandalf | commission briefs | 6.2 KB | 1 (`2026-05-16-gandalf-onboarding-arpg-isekai-knowledge.md`) |
| **research/scripts/** | `agentic_orchestration/research/scripts/` | **elrond** | curation/migration scripts | empty | 0 |
| **qa/findings/** | `agentic_orchestration/qa/findings/` | jack-ryan | Gate-2 finding files | small | 1 (`2026-05-15-b10-4-option-2-and-aoe-philosophy.md`) |
| **qa/pending/** | `agentic_orchestration/qa/pending/` | developers ship in; jack-ryan drains | review queue | empty | 0 |
| **dispatches/** | `agentic_orchestration/dispatches/` | knight-rider | one md per active task | small | 12 active/historical |
| **canonical/** | `canonical/*.md` (design discussion) | jack-ryan + gandalf | numbered design docs | small | many |
| **CHANGELOG.md, GOVERNANCE.md, AGENTS.md, REVIEW_PROCESS.md, skill_handoff_*.md** | root of `agentic_orchestration/` | knight-rider + jack-ryan | team-level state | small | several |

---

## 2. Ownership map

Per `AGENTS.md` § 3, observed code references, and `MIGRATION.md` provenance.

| Store | Authoritative owner | Read-only consumers | Notes |
|---|---|---|---|
| `data/telemetry.db` | star-lord | gamora (simulation), rocket (generation reads), elrond (planned cross-DB reads) | Singular owner; clear |
| `data/telemetry.db` schema | star-lord | — | Migrations in `src/reincarnated/telemetry/migrations.py` |
| `telemetry.db` (engine root, 0 B) | **ambiguous / orphan** | nobody | See § 3.1 |
| `research.db` | **none current** (originally an unnamed pre-bootstrap surface) | nobody at runtime | Last touched 2026-05-07. `scripts/db.py` still imports it. Decisions-log entry 2026-05-07 says "deferred until contents audited" — this audit completes that audit |
| `seasons/` directory | rocket (writer via `output/season_writer.py`) | star-lord (exporter), drax (loadout indirectly via copies) | Boundary leak — see § 3.3 |
| `exports/` directory | star-lord (`export/season_exporter.py`) | drax (demo via direct hash-equal copy; loadout NOT — see § 3.3) | Clean |
| `demo/public/seasons/` | drax (the repo) but **filled by manual copy from `engine/exports/`** | demo runtime | Copy mechanism is undocumented |
| `loadout/data/` | drax (the repo) but **content authored by mixed sources** — see § 3.3 | loadout runtime | The mixed-shape state is the central data-pipeline issue |
| `data/seasonal_elements/pool.json` | rocket | engine generation pipeline | Stable |
| `data/seasonal_anchors/library.json` | rocket | engine generation pipeline | Stable |
| `foundation/canonical_library.json` | rocket | engine generation pipeline | Stable |
| `cache/llm/`, `logs/llm/` | star-lord | LLM client | Operational |
| `baseline/v1.2-pre-stage-a2/` | knight-rider / process | regression scripts (`scripts/capture-regression-baseline.py`) | One-shot snapshot |
| `research/knowledge/` | legolas (Mode A writes) | gandalf + elrond | New surface |
| `research/catalogue/` | legolas (Mode B writes) | elrond (curator) | Empty, awaits crawl |
| `research/curated/` | **elrond** | gandalf, rocket (eventual) | Empty, will host catalogue.db + curated tables |
| `research/scripts/` | **elrond** | n/a (tool scripts) | Empty |
| `research/commissions/` | knight-rider + gandalf (write) | legolas + elrond (read as work queue) | 1 active commission |
| `qa/findings/`, `qa/pending/` | jack-ryan | all dev seams (visibility) | Stable |
| `dispatches/` | knight-rider | all agents (work queue) | Stable |
| `canonical/` | jack-ryan + gandalf | all agents (read at startup) | Stable |

**Ambiguous / orphan stores:** `telemetry.db` at engine root (§ 3.1); `research.db` (§ 3.4). Both flagged for cleanup.

---

## 3. Gaps, overlaps, brittleness

### 3.1 — Empty `telemetry.db` at engine repo root (orphan)

`~/Games/reincarnated-engine/telemetry.db` is a 0-byte file dated 2026-05-14 22:39. The canonical telemetry path is `data/telemetry.db` (15 GB, same day, 1 h 17 min later). The root file is not referenced in production code (`cli.py` defaults to `data/telemetry.db`; `season_exporter.py` defaults to `data/telemetry.db`). The root file is almost certainly the residue of a one-off `sqlite3 telemetry.db ".tables"` invocation that auto-created an empty file when run from the wrong cwd. Risk: low; cosmetic. A wrong-cwd `sqlite3` against it returns "no tables" and could mislead an agent into thinking telemetry is empty.

**Recommendation:** delete (with Matt approval per ADR-006). Add `telemetry.db` (no path) to `.gitignore` only if not already covered — current `.gitignore` covers `research.db` and `research.db-wal`/`-shm` but I did not verify the bare `telemetry.db` rule from the repo root.

### 3.2 — `class_fight_loadouts.loadout_json` drives 15 GB telemetry DB

Average JSON blob: **6,690 bytes per row** × 1,925,180 rows ≈ **12.7 GB** of JSON text inside a single TEXT column. The blob is `{slot: GearInstance.model_dump() | null}` — i.e., a full re-serialization of the equipped gear for every fight, including duplicated `flavor_text`, `visual_prompt`, all `rolled_effects`, etc. Most fields are reachable via `gear_instances` (table already keyed by `gear_id`), so the blob is largely a denormalized snapshot redundant with the canonical gear store.

Per-season blow-up: season_001005 alone has **1,488,900** loadout rows (≈ 10 GB). The next-largest is season_001006 at 176K rows.

**Risk profile:**
- Disk space: 15 GB is currently fine on a laptop but will compound as Yomi-scale seasons accumulate (~10 GB per intense balance pass).
- Query performance: full-table scans on `loadout_json` (via `LIKE` or JSON extraction) will be slow.
- Backup/regression-capture: `capture-regression-baseline.py` does a full `shutil.copytree` on telemetry.db. Future runs become expensive.

**Recommendation (deferred — see § 7):** normalize `loadout_json` into a `class_fight_gear` join table (`fight_loadout_id`, `slot`, `gear_id` → join `gear_instances`). Schema change owned by star-lord; cross-seam impact on gamora (read-side) and any analytics consumers. This is a meaningful refactor — math-before-code (Discipline #1) demanded.

### 3.3 — `engine/seasons/` shape leaks into `loadout/data/` (the central pipeline issue)

The data flow today:

```
rocket
  └─ output/season_writer.py
       └─ writes engine/seasons/<id>/   (manifest.json v1.3, per-class JSON, fights.jsonl, ...)

star-lord
  └─ export/season_exporter.py
       └─ writes engine/exports/<id>/   (metadata.json v1.0, classes.json [aggregated], gear_pool.json [v1.1])

drax/demo
  └─ engine/exports/<id>/  ──manual copy──>  demo/public/seasons/<id>/
       (byte-identical; verified by md5: fd8906a50c1505c48e1f527ac7b5abaa for metadata.json season_001005)

drax/loadout
  └─ engine/seasons/<id>/  ──manual copy──>  loadout/data/<id>/
       (manifest.json + classes/ tree; different shape from demo)
  └─ engine/exports/season_002328/gear_pool.json  ──manual copy──>  loadout/data/season_002328/gear_pool.json
       (Yomi-only; hybrid shape — engine's internal manifest + export-shape gear_pool)
```

Evidence:
- `engine/exports/season_001001/metadata.json` vs `loadout/data/season_001001/manifest.json` — different hashes, different field names (`format_version` vs `manifest_version`, `seed` vs `generation_seed`, `class_count` vs `summary.classes_generated`).
- `engine/exports/season_001005/metadata.json` vs `demo/public/seasons/season_001005/metadata.json` — identical hash.
- `loadout/data/season_002328/gear_pool.json` is from the v1.1 export-side schema (per `engine/src/reincarnated/export/MIGRATION.md`); other loadout seasons have no `gear_pool.json` at all.

**Why this is fragile:**

1. **No script publishes from engine to loadout.** Grep across `engine/scripts/`, `engine/src/`, and the export module: zero references to `reincarnated-loadout`. The publish step is a manual `cp -r` (or equivalent) done by whoever shipped that season. There is no provenance, no checksum, no schema-validation gate.
2. **Loadout consumes two shapes simultaneously.** `useSeasonData.ts` reads engine's *internal* `manifest.json` shape for season_001001–001004 + sample-season; `Sample.tsx` and `Encounters.tsx` directly import `season_002328/gear_pool.json` in the *export* shape. Drax's TypeScript types span both. A future schema change to either pipeline can silently break the loadout if the wrong shape gets copied.
3. **Demo and loadout disagree on what they consume.** Demo consumes the clean export shape; loadout consumes the engine's internal shape. They cannot share a loader.
4. **Internal `seasons/` directory was not designed as a public consumer interface.** Per `output/season_writer.py`, it's the raw orchestrator output — `fights.jsonl` (119K lines per season), `generation_log.txt`, `validation_report.json` are operational artifacts, not consumer-facing data. Treating it as a publishable surface forces star-lord and rocket to think twice every time they touch the internal shape.

**This is the single largest architectural issue surfaced by the audit.** It is not currently breaking anything (everything works), but it is a discipline-#13/#14 setup — implicit pillars carrying load they were not designed for, internal schemas leaking into generative consumers.

### 3.4 — `research.db` is dormant but undeleted; deferral has gone stale

Per decisions-log 2026-05-07 (line 147): *"research.db (pre-existing research database) and telemetry.db (new, purpose-built generation telemetry database added May 7) coexist. Consolidation into a single database is explicitly deferred ... Active. Consolidation deferred until research.db contents and schema are audited."*

This audit now satisfies the precondition. `research.db` contains:
- `generation_runs` — 1 row (season_000042)
- `classes` — 11
- `monsters` — 40
- `gauntlet_matchups` — 110
- `skills` — 166
- `trial_bosses` — 1
- `fight_results` — 13,040
- `research_notes` — 5 (findings/decisions from 2026-05-07 about Phase 0 validation, mana formula bug, binary search convergence, sustain-weird-class observation, trial HP calibration)
- `bugs_log` — 5 (the early-May bug discoveries that became fixes)

**Everything in research.db that has structural meaning is now in telemetry.db.** The `research_notes` and `bugs_log` rows are the only narrative content. None of these are referenced from production code; the live engine writes nothing to research.db. `scripts/db.py` still has it as the default DB path, but that script appears to be a pre-bootstrap utility.

**Recommendation:** archive (not delete) — export `research_notes` and `bugs_log` to a markdown file under `agentic_orchestration/research/curated/historical-research-db-extract-2026-05-16.md` for the historical record, then remove `research.db` + the WAL/SHM siblings + the `scripts/db.py` reference. Decisions-log gets a "superseded by data-architecture audit 2026-05-16" entry.

#### 3.4.1 — Phase-1 cleanup status (added 2026-05-16, COMPLETE on elrond side)

Per dispatch `2026-05-16-elrond-A-research-db-retirement.md`, cleanup executed 2026-05-16 in two passes:

**Pass 1 — non-destructive prep:**
- **Narrative archive committed:** `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md` — `research_notes` (5) + `bugs_log` (5) verbatim, all single-row metadata tables verbatim, structural-table schemas + counts.
- **Binary snapshot committed:** `agentic_orchestration/research/curated/archive/research-db-2026-05-07.db` (2.6 MB, SHA-256 `3846b98b272386dc946104676da7cff6ac1f86f529be195799af7b289f96351e`). Steward-call addition — `.gitignore` exception `!archive/*.db` permits this intentional preservation. Lossless recovery path for structural rows in case the audit's "all structural is in telemetry.db" claim has edge cases.

**Pass 2 — destructive removal (Matt-authorized per ADR-006, 2026-05-16):**
- `rm /Users/admin/Games/reincarnated-engine/research.db` ✓
- `rm /Users/admin/Games/reincarnated-engine/research.db-wal` ✓
- `rm /Users/admin/Games/reincarnated-engine/research.db-shm` ✓
- `rm /Users/admin/Games/reincarnated-engine/telemetry.db` (the empty 0 B root-of-repo orphan from § 3.1 — bundled into the same authorization window) ✓
- Engine `data/telemetry.db` (15.7 GB canonical) — UNTOUCHED, verified post-rm. Engine `git status` reports no new untracked artifacts; all four removed files were already `.gitignore`d so removal does not perturb git state.

**Engine-side script cleanup still pending (star-lord seam, ADR-004):**
- `scripts/db.py` (line 20 `DB_PATH = Path("research.db")` etc.) and `scripts/capture-regression-baseline.py` (lines 50/150/285) still reference research.db. Both files are star-lord's. Recommended one-liner for star-lord's MIGRATION.md captured in archive markdown § E. Knight-rider sequences with star-lord.

Future references to research.db content should point at the archive instead. The audit's § 3.1 finding (empty `telemetry.db` at engine root) is now superseded — the file no longer exists.

### 3.5 — Telemetry field-population gaps despite migration 1.9

Quantitative gaps in fields the schema declares but generation doesn't populate consistently:

| Column | Table | NULLs | Total | NULL % |
|---|---|---|---|---|
| `seasonal_element_name` | `classes` | 204 | 234 | 87% |
| `convergence_wall_time_seconds` | `classes` | 197 | 234 | 84% |
| `termination_reason` | `class_fight_loadouts` | 1,522,800 | 1,925,180 | 79% |
| `engine_version` | `seasons` | 0 | 23 | 0% (fine) |
| `damage_dealt`, `damage_taken` | `class_fight_loadouts` | 0 | 1,925,180 | 0% (fine) |
| `flavor_text` (legendary) | `gear_instances` | 1,199 | 1,439 | 83% |

The three high-NULL fields were added in migration 1.9 (2026-05-13) but most rows pre-date that migration. New rows since 2026-05-13 likely populate them; older rows are NULL by historical accident. Star-lord's AGENT_STATE notes these as known open items requiring Matt approval before backfill (ADR-006).

**Recommendation:** no action from elrond. This is squarely star-lord's seam. Surface during the next telemetry-tier-1 dispatch as a backfill candidate.

### 3.6 — Inconsistent season coverage across stores

| Store | Season count | Set |
|---|---|---|
| `telemetry.db.seasons` | 23 | 000001, 000007, 000013, 000042, 000043, 000046, 000093, 000099, 000100, 000200, 000300, 000400, 000500, 000600, 000700, 000999, 001001–001007 |
| `engine/seasons/` (disk) | 23 | identical to telemetry |
| `engine/exports/` (disk) | 5 | 001001–001005 |
| `demo/public/seasons/` | 5 | 001001–001005 |
| `loadout/data/` | 6 | 001001–001004, 002328, sample-season |

Notable mismatches:
- **`season_002328` (Yomi) is in loadout but NOT in `engine/seasons/`, NOT in `engine/exports/`, NOT in telemetry.** Star-lord's gear_pool re-export ran against telemetry, so the data must be there — let me check… actually it's not in the seasons list above. Yomi must be in a separate telemetry pass or has been generated against a different telemetry instance. **This is a real provenance gap** — the canonical Yomi data lives only in the loadout repo. If the loadout repo is lost, Yomi is lost.

#### 3.6.1 — Yomi provenance audit + remediation (added 2026-05-16, RESOLVED)

The hypothesis above was refined by the provenance audit at `agentic_orchestration/research/curated/yomi-provenance-audit-2026-05-16.md`. Reality: Yomi was generated against the canonical engine on 2026-05-13 (seed=2328, anchor=myth-014-yomi), `seasons/season_002328/` + telemetry rows existed at generation time, and **both were subsequently deleted from the engine repo** after the v1.1 gear_pool re-export of 2026-05-14 23:58. The loadout commit message phrase "from engine side-seed" framed it as a deliberate side-experiment outside the canonical 001xxx series; the engine-side artifacts were treated as disposable scaffolding. Re-running from seed=2328 today produces **A Yomi** but not **THIS Yomi** (engine code changes — notably B10.4 swarm calibration — shift convergence outcomes).

**Remediation taken 2026-05-16, in two passes:**

1. **Option 2 — loadout origin remote (Matt-authorized, elrond-executed as cross-seam exception):** loadout pushed to `https://github.com/mwetmor/reincarnated-loadout`; `main` tracks `origin/main`. Loadout SPOF closed at the repo level (3-deep redundancy restored: working tree + local git + remote).
2. **Option 3 — Yomi archived into elrond's seam (Dispatch B Option 3):** `archive/yomi-season_002328-2026-05-13/` (556 KB, byte-identical to source; companion markdown at `archive/yomi-season_002328-2026-05-13.md`; MIGRATION.md v1.2 entry). Yomi-specific 4-deep redundancy now matches the standard established by research.db retirement.

**Open follow-on (NOT elrond):** star-lord-side note on `reincarnated-engine/src/reincarnated/export/MIGRATION.md` documenting the c1f02ca deterministic-replay's silent assumption on `seasons/<id>/gear/catalog.json` persistence — the fragility that allowed Yomi to lose its engine-side artifacts without warning. Knight-rider sequences.
- `engine/seasons/season_001006` and `_001007` exist on disk and in telemetry but are not exported. The export step is gated separately from generation.

**Recommendation:** establish a "canonical season set" convention — every season referenced by demo or loadout must have a complete trail through `telemetry.db → seasons/ → exports/ → published artifacts`. Yomi specifically needs an audit: where was it generated, where is its source data? Defer to a follow-on dispatch (star-lord).

### 3.7 — No SQL ATTACH or formal cross-store join pattern exists today

Grep across all four repos: zero occurrences of `ATTACH DATABASE` and zero formal cross-store joins. Today's cross-store queries happen via:
- Python scripts reading both telemetry.db and JSON files on disk (e.g., the gear_pool stats re-derivation in `export/season_exporter.py:_regen_gear_stats` re-runs a generator with deterministic seed instead of cross-joining)
- Ad-hoc `sqlite3` CLI invocations during investigation
- Manual file-shape comparison (Matt eyeballing, agents grepping)

**This is fine today** because there's only one DB. Once `catalogue.db` exists, formal SQL ATTACH patterns become useful for cross-cutting analysis (e.g., "what telemetry'd classes have an embodiment tag that the catalogue can visually deliver?"). See § 8.

### 3.8 — Schema-versioning is inconsistent across stores

Telemetry.db has rigorous `schema_meta` + numbered migrations. Other stores have implicit versioning at best:

| Store | Versioning |
|---|---|
| `data/telemetry.db` | Explicit `schema_meta` + `migrations.py` (10 migrations, append-only) ✓ |
| `engine/exports/<id>/metadata.json` | `format_version: 1.0` field — but the field hasn't moved despite gear_pool's v1.1 |
| `engine/seasons/<id>/manifest.json` | `manifest_version: 1.3` — moves with major changes; no migration log |
| `data/seasonal_elements/pool.json` | `"version": "1.0"` in root — unchanged despite many entry additions |
| `data/seasonal_anchors/library.json` | `"version": "1.0"` in root — same |
| `foundation/canonical_library.json` | `"version": "1.0.0"` — same |
| YAML configs | unversioned |

The `gear_pool.json` v1.1 schema bump is documented in `export/MIGRATION.md` but the parent `metadata.json` still says `format_version: 1.0`. Versioning at the file level is inconsistent.

**Recommendation:** see § 6 schema conventions.

---

## 4. Cross-store joins currently performed

| Pattern | Where | Pages of code | Fragility |
|---|---|---|---|
| Read `seasons/<id>/gear/catalog.json` from disk + re-run gear generator + match against `telemetry.db gear_instances` by reverse-row-order | `export/season_exporter.py:_regen_gear_stats` | ~50 LOC | High — implicit dependency on insertion order (`ORDER BY rowid DESC` matched by position). Documented in MIGRATION.md so star-lord owns the brittleness consciously. |
| Read `telemetry.db seasonal_elements` + fallback to disk `seasons/<id>/manifest.json` if missing | `export/season_exporter.py` (paraphrased) | ~10 LOC | Low — fallback is explicit |
| Read `telemetry.db classes/abilities/monsters/gear_instances` + read `seasons/<id>/` JSON files + assemble single export JSON | `export/season_exporter.py:_export_season_inner` | bulk of exporter | Medium — multi-source assembly works but depends on both stores being in sync |
| Loadout React app reads `data/*/manifest.json` and `data/*/classes/*.json` via Vite glob, then runs analytics in `useAnalytics.ts` joining across all loaded seasons | `loadout/src/hooks/useSeasonData.ts`, `useAnalytics.ts` | several hundred LOC | Medium — Vite's glob is build-time; new seasons require a rebuild |
| Demo runtime fetches `metadata/classes/monsters/gear_pool` JSONs in parallel via `fetch()` | `demo/src/data/loader.ts:loadSeason` | ~20 LOC | Low |
| Regression baseline script copies both DBs + exports + computes checksums | `engine/scripts/capture-regression-baseline.py` | ~200 LOC | Low (one-shot artifact tooling) |

**Cross-DB joins (SQL ATTACH-style):** none.
**Cross-repo file reads:** the engine writes; demo and loadout copy. There is no engine-side script that pushes to either downstream repo; the push is manual.

---

## 5. Recommended architecture

The dispatch proposed a four-layer separation. After audit I endorse it with one refinement and one addition.

### 5.1 — Four authoritative layers

| Layer | Owner | Purpose | Stores |
|---|---|---|---|
| **L1 — Engine internal data** | rocket (writer) + star-lord (telemetry) | The engine's working memory: simulation telemetry, raw season working files, LLM cache | `data/telemetry.db`, `seasons/<id>/`, `cache/`, `logs/`, `foundation/canonical_library.json`, `data/seasonal_*` |
| **L2 — Generated artifacts** (published) | star-lord (exporter) | Consumer-facing season payloads. Schema-stable. The boundary between engine internals and downstream apps | `exports/<id>/` (and any future "published-export" surface) |
| **L3 — External research + catalogue** (NEW) | **elrond** | Knowledge-gathering surface: raw research, curated catalogue, abstraction analyses | `agentic_orchestration/research/curated/catalogue.db`, `research/knowledge/`, `research/catalogue/`, `research/scripts/` |
| **L4 — App-derived data** (consumer-side) | drax | Copies / transformations of L2 used by loadout and demo. NEVER authoritative | `demo/public/seasons/`, `loadout/data/` |

**Refinement vs the dispatch's proposal:** the dispatch listed "Generated season artifacts" as a single layer co-owned by star-lord and consumed by drax. I split L2 (the engine's authoritative export) from L4 (the apps' copies). The apps' copies are *projections* of L2 — they may have additional shape (e.g., loadout's per-class file tree) but they are derivable from L2 and never authoritative. This makes the publish step explicit and the source-of-truth unambiguous.

**Addition vs the dispatch's proposal:** the dispatch didn't call out the engine-internal `seasons/` directory as a distinct surface. It is. It belongs in L1 because it's working memory, not a publishable contract — and L4's current consumption of it (loadout) is the leak that motivates the cleanup in § 7.

### 5.2 — The publish step needs to be a thing

Today, "publish" is a manual `cp`. Tomorrow, "publish" should be an explicit engine command that:

1. Reads L1 + writes L2 (already exists as `star-lord season_exporter`).
2. **Transforms L2 → L4 shapes per consumer.** For demo: direct copy (already byte-identical). For loadout: aggregate the export-shape into the per-class JSON tree loadout expects (or, better, retire the per-class tree and have loadout consume the same shape as demo). Step 2 is the new piece.
3. Records provenance (source export-id, sha of each file, target consumer-repo) — could go in a new `publish_log` table in telemetry.db or in a sidecar JSON in `exports/<id>/publish_manifest.json`.

Drax does not own this step; it crosses repos. Star-lord owns it (his seam is "output / telemetry / LLM"). The publish step belongs in `engine/src/reincarnated/export/` as a sibling to `season_exporter.py`.

### 5.3 — L3 catalogue layer fits cleanly as an independent SQLite DB

Per doc 37 § 8 (Catalogue-based form-bias resolution path), the catalogue is fed by Legolas Mode B crawls and curated by elrond into structured form. The natural store is `agentic_orchestration/research/curated/catalogue.db` (per AGENTS.md elrond entry and doc 37 § 8 explicit reference). Specifically:

- One SQLite file at `agentic_orchestration/research/curated/catalogue.db`
- Schema versioning via `schema_meta` table (same pattern as telemetry.db)
- Migrations in `agentic_orchestration/research/scripts/catalogue_migrations.py` (parallel to engine's `migrations.py`)
- Cross-DB analysis via `ATTACH DATABASE '/path/to/data/telemetry.db' AS engine` from elrond scripts in read-only mode

**Tables I anticipate (preview, not designed yet):**
- `assets` (asset_id, source, url, name, category, dimensionality, decomposition, file_format, license, cost, crawl_date)
- `asset_style_tags` (asset_id, style_register, tag, confidence) — score-don't-filter
- `asset_metadata_raw` (asset_id, source_metadata_json) — preserves raw extraction for reproducibility (Discipline #11 attribution clarity)
- `crawl_sessions` (session_id, source, started_at, completed_at, asset_count, legolas_version)
- `abstraction_groupings` (grouping_id, name, dimension, member_count, created_by_analysis, created_at) — emergent groupings from analysis
- `asset_grouping_membership` (asset_id, grouping_id, confidence)

Detailed schema design is **out of scope for this audit**; it follows once Gandalf locks the style register and Legolas returns the first sample.

### 5.4 — `research.db` retires

Becomes an archive markdown file at `agentic_orchestration/research/curated/historical-research-db-extract-2026-05-16.md`. The DB file and SCRIPT references go away. See § 7 sequencing.

---

## 6. Schema conventions (recommended; apply to L3 and any new stores; back-fill L1/L2 incrementally)

### 6.1 — Source-anchored

Every row that originates outside the engine carries:
- `source` (TEXT) — provenance string (`'opengameart.org/...'`, `'unity-asset-store/...'`, `'legolas-crawl-2026-05-16'`)
- `source_date` (TIMESTAMP) — when the source claim was true (crawl date for catalogue; generation date for engine-derived)
- `source_metadata` (JSON, optional) — raw source response preserved for reproducibility

Engine-derived rows (telemetry-side) implicitly have `engine_version` + `schema_version`; pattern is already established.

### 6.2 — Reversible

Curation transformations must be reproducible from raw input. For the catalogue: keep `asset_metadata_raw` for every curated `assets` row. For abstraction analyses: keep the script (in `research/scripts/`) and the run parameters; the output table can always be regenerated. This is Discipline #11 (attribution clarity) at the data-layer.

### 6.3 — Tagged, not encoded

Per doc 37 § 9.2b / Discipline #14 candidate. Use explicit tag columns / association tables rather than packing semantic meaning into compound IDs. Example: don't make a `humanoid_fire_legendary` asset_id; use separate columns / tags for embodiment, element, tier. This is also the score-don't-filter principle expressed at the schema layer — style register lives in a tag table, not in the asset_id or even in a single column.

### 6.4 — Versioned, with an explicit migration log

Every store carries a schema version that increments append-only on change. For SQLite stores: `schema_meta` table + numbered migrations (telemetry.db pattern is the reference).

For JSON-file stores (anchor library, element pool, canonical library): add a `MIGRATION.md` in the directory documenting every schema bump. Bump the embedded `"version"` field accordingly. Today these are pinned at `1.0` despite having grown content.

### 6.5 — License + cost legibility for external data (catalogue-specific)

Every external asset gets `license` (TEXT — `'CC0'`, `'CC-BY 4.0'`, `'commercial-only'`, `'unknown'`) and `cost` (TEXT — `'free'`, `'$5-pack'`, `'paid-required'`). NULL for license is forbidden — use `'unknown'` explicitly. This is the audit trail the team needs when a future asset goes into a published season.

### 6.6 — Audit-trail columns on every curated table

Standard quartet on every elrond-curated table:
- `curated_at` (TIMESTAMP)
- `curated_by` (TEXT — `'elrond'` or `'elrond+script-name'`)
- `curation_run_id` (FK to a `curation_runs` table, optional)
- `superseded_at` (TIMESTAMP, nullable — if NULL, this is the current curation; if set, this row is historical)

Curation is append-only with `superseded_at` rather than UPDATE-in-place. Preserves history.

### 6.7 — Naming: schemas should make truth visible

A schema name should pass the *"what is actually being said by this data when I look at it"* test. Examples:
- `class_fight_loadouts.loadout_json` — the name says exactly what it is. Good.
- `class_monster_win_rates` (with `fight_count` column) — also good; the name plus structure makes the aggregation level visible.
- `asset_grouping_membership` — better than `asset_groups` (the latter could mean groupings, members, or both).

For the catalogue: prefer clarity over brevity. `asset_style_tags` not `tags`.

---

## 7. Migration recommendations and sequencing

Three sequenced cleanups, ordered by *enables-next-work*.

### Phase 0 (this dispatch) — Audit lands

This document. No code changes. **DONE on completion.**

### Phase 1 (next, low cost) — `research.db` retirement + `telemetry.db` root cleanup

- **Cost:** 30 min elrond work + Matt approval per ADR-006 for deletion
- **Benefit:** removes ambiguity about which DB is canonical; closes the 2026-05-07 decisions-log deferral
- **Steps:**
  1. Elrond writes `research/curated/historical-research-db-extract-2026-05-16.md` capturing `research_notes` (5) and `bugs_log` (5) rows as durable narrative
  2. Matt authorizes deletion of `research.db`, `research.db-wal`, `research.db-shm`, the empty `telemetry.db` at engine root, and the `scripts/db.py` legacy script
  3. Knight-rider drafts decisions-log entry: "research.db deprecation: archived to research/curated/, removed from repo. Supersedes 2026-05-07 deferral"
  4. Jack-ryan Gate-1 quick review (docs-only)
- **No cross-seam impact.** Pure cleanup.

### Phase 2 (medium cost; high value) — Codify the L2→L4 publish step

- **Cost:** 1-2 days star-lord + drax coordination + jack-ryan Gate-1 review
- **Benefit:** eliminates the silent `engine/seasons/ → loadout/data/` shape leak (the largest fragility surfaced by this audit); makes the publish step explicit, scripted, and provenance-tracked; unblocks future schema changes from worrying about consumer breakage
- **Steps:**
  1. Knight-rider authors a dispatch (`2026-05-XX-star-lord-publish-step.md`) commissioning:
     - A new `engine/src/reincarnated/export/publisher.py` that takes a season-id and writes both demo-shape and loadout-shape outputs
     - A `publish_manifest.json` recording source-export-id + sha-per-file + target-consumer-repo
     - A one-time backfill pass that re-publishes all 5 current seasons cleanly
     - MIGRATION.md documenting the new publish contract
  2. Drax dispatch to retire the engine-internal `manifest.json` consumption in loadout, replacing it with the published shape
  3. Yomi (season_002328) provenance audit: where is its source data? Either bring it under `engine/seasons/` properly or document it as an outlier
- **Cross-seam impact:** L2 contract change affects drax (loadout); MIGRATION.md required (ADR-004); Matt approval (ADR-002 cross-seam schema)
- **Risk:** the per-class JSON tree the loadout uses may have advantages I haven't seen (e.g., HTTP/2 multiplexing in dev). Drax should weigh in before retirement.

### Phase 3 (deferred; medium-high cost) — `class_fight_loadouts.loadout_json` normalization

- **Cost:** several days star-lord + gamora coordination; math-before-code on join performance; full-regen confirms parity
- **Benefit:** reduces telemetry.db from ~15 GB to ~2-3 GB; opens efficient gear-loadout analytics queries; reduces baseline-snapshot cost
- **Steps:**
  1. Math note on JSON-blob vs join performance for the existing analytical queries (gamora B10.4 used these)
  2. New `class_fight_gear` table (`fight_loadout_id`, `slot`, `gear_id`)
  3. Migration 1.10 backfills from existing blobs, then drops `loadout_json` column
  4. Smoke + full regen on Yomi-scale season
- **Cross-seam impact:** any analytics that reads `loadout_json` directly. Star-lord MIGRATION.md.
- **Trigger:** wait until disk pressure forces it OR until a B14.5 V2 / B10 V2 analytics need exposes the query cost. Not today.

### Phase 4 (pending Gandalf style-register lock + first Legolas catalogue sample) — Catalogue DB schema design

- **Cost:** 1-2 days elrond, dependent on first viability-gate-passing sample
- **Benefit:** unblocks form-bias resolution per doc 37 § 8
- **Out of scope for this audit;** flagged as the next major elrond deliverable

### Recommendations NOT acted on

- **Backfilling NULL columns in telemetry (§ 3.5).** Star-lord's seam. Not elrond's call.
- **Renaming `seasonal_elements` / `element_proposals`.** Schemas are clear today; no reason to rename.
- **Consolidating cache/llm into telemetry.db.** Separate concern (operational vs analytical); current split is fine.
- **Touching the YAML configs in `engine/config/`.** Rocket's seam; no current pain.

---

## 8. Cross-store query patterns (recommended for legitimate cross-store work)

Once L3 (catalogue.db) exists, cross-store analytical queries become routine. Recommended patterns:

### 8.1 — Read-only SQL ATTACH from elrond scripts

```python
import sqlite3
conn = sqlite3.connect("agentic_orchestration/research/curated/catalogue.db")
conn.execute("ATTACH DATABASE 'file:///Users/admin/Games/reincarnated-engine/data/telemetry.db?mode=ro' AS engine")
# Now: SELECT ... FROM catalogue.assets JOIN engine.abilities ON ...
```

Pattern rules:
- Catalogue.db is the primary connection (write-allowed in elrond's scripts)
- Engine telemetry is ATTACHed in `mode=ro` (read-only file URI) — enforces the ownership boundary at the SQL layer
- The script's filename + purpose comment makes the cross-store intent legible

### 8.2 — Materialized cross-store views land in catalogue.db, not telemetry.db

Cross-cutting analytical results (e.g., "which engine-generated abilities have catalogue-deliverable visual representation") are written to catalogue.db as new tables, with provenance pointing to the engine snapshot they were computed against. Telemetry.db stays single-purpose.

### 8.3 — For shell-level investigation, the convention is

```bash
sqlite3 agentic_orchestration/research/curated/catalogue.db \
  "ATTACH '/Users/admin/Games/reincarnated-engine/data/telemetry.db' AS engine; SELECT ..."
```

Same pattern; works for interactive elrond work without writing a script.

### 8.4 — Cross-repo file reads stay in their lane

L2 → L4 transformations happen in star-lord's publisher (per § 7 Phase 2). No agent reads another repo's runtime data directly — they go through the published artifacts or through documented APIs.

---

## 9. Pending work this audit enables

| Item | How this audit unblocks it | Owner | Status |
|---|---|---|---|
| **Catalogue DB schema design** (`research/curated/catalogue.db`) | Audit confirms L3 as a clean new layer with no overlapping responsibility. Schema-convention recommendations (§ 6) ready to apply | elrond | Pending Gandalf style-register lock + first Legolas sample |
| **`research.db` retirement** | Audit closes the 2026-05-07 deferral; recommended Phase-1 cleanup | elrond + Matt approval | Ready when Matt authorizes |
| **L2→L4 publish step codification** | Audit identifies the leak in § 3.3; sequences as Phase 2 | star-lord (lead) + drax | Pending dispatch authorship by knight-rider |
| **Catalogue-based form-bias work** (doc 37 § 8) | Audit clears the data-architecture preconditions for the catalogue layer | elrond → rocket (eventual integration) | Awaits viability-gate pass on first Legolas catalogue sample |
| **Star-lord telemetry tier-1 extension** (dispatch 2026-05-14, pending) | Audit's § 3.5 quantifies the NULL gaps the tier-1 work targets — useful context, not blocking | star-lord | Already dispatched; awaiting pickup |
| **Yomi (season_002328) provenance audit** | Audit identifies the gap in § 3.6 | star-lord | New dispatch needed |
| **`class_fight_loadouts.loadout_json` normalization** (Phase 3) | Audit quantifies the cost; defers until trigger | star-lord | Not active |
| **Schema-convention back-fill** (JSON-file stores get MIGRATION.md and version-field bumps) | Audit recommends in § 6; light-touch per-store | rocket (for L1 JSON files) | Opportunistic, not active |

---

## 10. Appendix — methodological notes

- This audit reads everything; modifies nothing. ADR-006 honored.
- Survey-mode constraint (ADR-007) honored: § 1–4 are descriptive; § 5–9 are explicitly prescriptive (the dispatch requested both).
- Every quantitative claim cites the query that produced it (DB queries shown inline where useful; full transcripts in elrond session log).
- Three cross-store hash checks performed:
  - `engine/exports/season_001005/metadata.json` ≡ `demo/public/seasons/season_001005/metadata.json` → byte-identical (`fd8906a50c1505c48e1f527ac7b5abaa`)
  - `engine/exports/season_001001/metadata.json` ≢ `loadout/data/season_001001/manifest.json` → different hashes, different shapes (the § 3.3 finding)
  - `engine/exports/season_001005/classes.json` ≡ `demo/public/seasons/season_001005/classes.json` → byte-identical (confirms direct copy)
- Eight stores I considered and dismissed as out-of-scope: `node_modules/` trees (build artifacts), `dist/` directories (build outputs), `.claude/settings.local.json` (per-session config), `.DS_Store` (filesystem cruft), `tests/` fixtures (test-local), `prototypes/` in loadout (drax sketches), `notes/` in engine (personal working), `pyproject.toml`/`package.json` (build manifests, not data).

---

## 11. Sign-off

Audit complete. No new schemas written; no production code touched. Recommendations land in three sequenced phases (§ 7) plus the deferred Phase-3 normalization and the pending Phase-4 catalogue work. Knight-rider notified at completion with this path and the 2-3 sentence verdict (§ top of doc).

**Filed:** 2026-05-16
**Reviewer (suggested):** jack-ryan Gate-1 docs-only review; Matt approval for Phase-1 cleanup when ready

