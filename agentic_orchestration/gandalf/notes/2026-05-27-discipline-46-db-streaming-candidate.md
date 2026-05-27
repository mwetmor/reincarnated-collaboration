# Discipline #46 Candidate — DB Anti-Materialization + Stream Discipline

> **STATUS:** CURRENT — gandalf-authored discipline candidate. Matt 2026-05-27 ratified Path (1) Cycle 14 scope expansion + Discipline #46 as load-bearing pre-Phase-4 protection. Routes to jack-ryan for canonical-write at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #46.

**Date:** 2026-05-27 evening
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (Path 1 recognition record; Discipline #46 load-bearing for Phase 4)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` (KR routing)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 4 (math gates spec — needs Discipline #46 to ship correctly)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (canonical-write target)

---

## 0. TL;DR

**Discipline #46 candidate** — DB Anti-Materialization + Stream Discipline. Any production code path touching telemetry DB / substrate catalogue DB / kit archive / Court persistence DB / any DB whose row count can exceed ~1,000 rows MUST follow 7 patterns: stream-not-materialize / push-to-SQL / index-filter-columns / bound-every-exploratory-query / audit-cartesian-joins / WAL-mode / per-cell-bounding-for-math-gates.

**Load-bearing for Path (1) Phase 4 math gates.** Without this discipline, Pareto + Crowding + Mahalanobis algorithms operating against growing kit archive would produce O(n²) computational explosions — the kernel-panic class of failure Matt flagged.

---

## 1. Discipline statement (proposed canonical text)

> **Discipline #46 — DB Anti-Materialization + Stream Discipline.**
>
> Any production code path touching the telemetry DB, substrate catalogue DB, kit archive (MAP-Elites), Court persistence DB, or any DB whose row count can exceed ~1,000 rows MUST follow these 7 patterns:
>
> **1. Stream, don't materialize.** No unbounded `fetchall()`. Use cursor iteration OR `fetchmany(N)` in a loop where N ≤ 1,000. Reserve `fetchall()` only for queries with explicit `LIMIT` clauses where the limit is empirically known small (≤ ~1,000 rows).
>
> **2. Push aggregation into SQL.** If Python is enumerating rows to count, filter, sum, group, or join, the database does it instead. `SELECT COUNT(*) WHERE ...` returns 1 row vs N. `SELECT ... GROUP BY ...` returns K groups vs N rows. SQLite is genuinely fast at this with proper indexes.
>
> **3. Index filter columns.** Every column used in WHERE/JOIN/ORDER BY on tables exceeding ~1,000 rows must be indexed. Use `EXPLAIN QUERY PLAN` to verify queries hit indexes, not full scans. Adding an index is cheap; debugging a slow full-scan in production is expensive.
>
> **4. Bound every exploratory query.** Any query that could return >10k rows must either paginate (`LIMIT N OFFSET M`) or aggregate. No unbounded `SELECT *` in production code paths.
>
> **5. Audit for cartesian joins.** Every JOIN must have an explicit ON clause. Grep audits at Gate-2 for `JOIN ... (?!ON)` patterns AND any implicit comma-joins (`FROM table_a a, table_b b WHERE ...`). Two tables of 10k rows each in a cartesian join becomes 100M rows.
>
> **6. WAL mode for reader/writer separation.** Any DB with concurrent readers + writers must run `PRAGMA journal_mode=WAL`. Reduces lock contention; readers don't block writers and vice versa.
>
> **7. Per-cell bounding for math gates.** Cross-kit comparison algorithms (Pareto dominance, crowding distance, Mahalanobis distance) operate WITHIN BC cells, NOT across the global archive. Cell capacity (~10-100 kits) bounds comparison cost to manageable per-cell scale. Global O(n²) comparisons across the full archive are explicitly forbidden.
>
> **When to cite:**
> - **Gate-1 dispatch review** (jack-ryan): verify DB queries in dispatch follow patterns; reject if forbidden patterns appear
> - **Gate-2 implementation review** (jack-ryan): grep audit for forbidden patterns (unbounded `fetchall`, JOIN without ON, missing index on filter columns)
> - **Math-note authoring** at Phase 4 math gates + Phase 5 multimodal clustering: explicit per-cell bounding requirement in math-note acceptance criteria
> - **Any new DB query introduction** in Phase 8 export work, telemetry analysis, sidecar work — Discipline #46 applies pre-emptively
>
> **Composes with:** #1 (math-before-code; DB query patterns specified before implementation) + #11 (empirical inspection over assumption; `EXPLAIN QUERY PLAN` verifies; not trust) + #18 (math-hotspot routing; query-cost is a methodology consultation hotspot) + #34 (concentration; this discipline is concentration applied at DB-query level)

---

## 2. Why this discipline is needed

### 2.1 Audit findings 2026-05-27 (current code-base risk surfaces)

| Surface | fetchall() usage | Growth potential | Risk class |
|---|---|---|---|
| `src/reincarnated/generation/substrate_weapon_binding.py:332` | YES | Substrate ~2,499 rows; bounded short-term; growing across cycles | LOW → MEDIUM |
| `src/reincarnated/generation/bc_target_substrate_engine.py:342` | YES | Same substrate; bounded | LOW |
| `src/reincarnated/telemetry/db.py:77` | YES | Telemetry **grows UNBOUNDED across seasons** | **HIGH** |
| `src/reincarnated/telemetry/recorder.py:65/80/93/114` (4 sites) | YES | Same telemetry; unbounded growth | **HIGH** |
| `src/reincarnated/export/season_exporter.py:445/455/502` | YES | Per-season; bounded | LOW |
| `src/reincarnated/export/cycle13_loadout_ingest.py` (multiple) | YES | Per-season; bounded | LOW |
| **Phase 4 math gates (NEW; Path 1 Cycle 14)** | DESIGN-DEPENDENT | Archive accumulates across seasons; could grow large | **HIGHEST without discipline** |

**WAL mode status:** ✅ `telemetry.db` confirmed in WAL mode (`PRAGMA journal_mode` returns "wal"); `court_persistence.py:616` explicitly sets WAL on its connection. Reader/writer separation is in place.

**Indexes status:** `weapon_knowledge_entries` has indexes on `canonical_name`, `source_library`, `cluster_id`. **Missing: `v1_scope` index** (filter column used in EVERY substrate query). Quick remediation listed in operational moves below.

**JOIN audit:** ✅ `substrate_weapon_binding.py:154/326` uses explicit ON clauses; no cartesian-join risk found.

### 2.2 Phase 4 math gates specifically — the load-bearing concern

Phase 4 (per doc 39 § Phase 4) implements:
- Pareto dominance check
- Crowding distance / hypervolume contribution
- Mahalanobis distance (duplicate detection)
- Information gain (KL) for novelty score
- Eviction rules if cell at capacity

**Without Discipline #46:** naive implementation would `fetchall()` the entire kit archive, run Python-side O(n²) comparison, and produce kernel-panic when the archive grows past ~5,000 kits (perfectly plausible after ~50 seasons of accumulation).

**With Discipline #46 § 7 (per-cell bounding):** comparisons operate WITHIN BC cells. Cell capacity ~10-100 kits. Per-cell O(k²) with k ≤ 100 is computationally trivial. Global O(n²) eliminated by architecture.

### 2.3 What the discipline catches that existing disciplines don't

- **Discipline #1 (math-before-code):** requires math notes BEFORE code; doesn't specifically address DB query patterns
- **Discipline #11 (empirical inspection):** requires empirical inspection; doesn't specifically require streaming patterns
- **Discipline #18 (math-hotspot routing):** requires methodology consultation at math hotspots; query-cost-methodology is implicit but not called out
- **Discipline #34 (concentration):** addresses capability concentration, not query bounding
- **Discipline #40 (scaffold-with-pending-decision):** addresses scaffold values, not query patterns

**Discipline #46 is novel** — it specifically catches DB query anti-patterns that no current discipline addresses. The class of bug it prevents (kernel-panic from row-enumeration explosion) is empirically dangerous and historically caught Matt's eye 2026-05-27.

---

## 3. Operational hooks (where this discipline fires)

### 3.1 Dispatch authoring (KR)

KR includes Discipline #46 in dispatch out-of-scope-and-acceptance-criteria sections for any dispatch touching DB queries:

```markdown
## Discipline #46 compliance

- [ ] All new DB queries follow stream / push-to-SQL / index / bound / no-cartesian patterns
- [ ] Per-cell bounding applied for math-gate algorithms (§ 7)
- [ ] EXPLAIN QUERY PLAN run on every new query; output captured in math-note or PR description
- [ ] Grep audit at Gate-2: no unbounded `fetchall()` in new code; no JOIN without ON
```

### 3.2 Gate-1 review (jack-ryan)

Gate-1 checklist amendment:
- "Does dispatch include Discipline #46 compliance section?"
- "Do specified DB queries follow streaming + per-cell patterns?"
- "Are indexes mentioned for filter columns?"

### 3.3 Gate-2 implementation review (jack-ryan)

Gate-2 grep audit (mechanical):
```bash
# Forbidden patterns (production code paths only)
grep -rn "\.fetchall()" src/reincarnated/ | grep -v "LIMIT" | grep -v "tests/"
grep -rEn "JOIN [^O]*$" src/reincarnated/  # JOIN lines without ON on same line
grep -rEn "FROM [a-z_]+ [a-z]+, [a-z_]+" src/reincarnated/  # implicit comma-joins
```

Any matches in production code paths require explicit justification (LIMIT clause; bounded-by-design comment; etc.) or are Gate-2 BLOCK.

### 3.4 Math-note authoring (gandalf + elrond + gamora)

Math notes at Phase 4 + Phase 5 + any Phase 8 work explicitly include § "DB query pattern guards (Discipline #46)" with:
- Which DB tables touched
- Which filter columns used (verify indexed)
- Per-cell bounding pattern for math gates
- Expected query result row counts at v1 + steady-state

### 3.5 Code review / pre-commit

Optional (post-Cycle-14): pre-commit hook running the grep audit. Not required for Cycle 14; can fire as Cycle 15+ tooling.

---

## 4. Pre-Phase-4 remediation work (Cycle 14 scope additions)

Per Matt 2026-05-27 confirm, three remediation items fire BEFORE Phase 4 math gates implementation:

### 4.1 Quick-win — add `v1_scope` index

```sql
CREATE INDEX IF NOT EXISTS idx_knowledge_v1_scope ON weapon_knowledge_entries(v1_scope);
```

- **Owner:** elrond
- **Effort:** ~1 hour (DDL + verification via EXPLAIN QUERY PLAN on existing substrate queries)
- **Justification:** every substrate query filters on `WHERE v1_scope = 1`; without this index, queries scan all 90,014 rows in `weapon_knowledge_entries` to filter down to 2,499 v1_scope rows. Index turns this into a targeted lookup.

### 4.2 Telemetry fetchall() refactor sweep

5 sites in telemetry code use `fetchall()` against unbounded-growth telemetry tables:
- `src/reincarnated/telemetry/db.py:77`
- `src/reincarnated/telemetry/recorder.py:65/80/93/114`

**Refactor pattern:** replace `fetchall()` with cursor iteration OR `fetchmany(1000)` in a loop. Add LIMIT clauses where appropriate. Audit whether aggregation can be pushed to SQL (COUNT/GROUP BY).

- **Owner:** star-lord (telemetry seam)
- **Effort:** ~3-5 hours (5 sites × audit + refactor + test)
- **Sequencing:** fires BEFORE Phase 4 math gates implementation (Phase 4 archive queries will compound telemetry-table queries; degraded telemetry queries would magnify)

### 4.3 Substrate query refactor — fetchmany pattern

2 sites in generation code use `fetchall()` against substrate (currently 2,499 rows; growing across cycles):
- `src/reincarnated/generation/substrate_weapon_binding.py:332`
- `src/reincarnated/generation/bc_target_substrate_engine.py:342`

**Refactor pattern:** replace `fetchall()` with `fetchmany(1000)` in a loop OR iterate cursor. Add LIMIT for kit-generation queries that need only N samples.

- **Owner:** rocket (generation seam)
- **Effort:** ~2-3 hours
- **Sequencing:** can fire parallel with Phase 4 work; not blocking

---

## 5. Composition with Path (1) Cycle 14 work

Discipline #46 applies to ALL Path (1) work:

| Phase | Discipline #46 application |
|---|---|
| **Phase 4 math gates** | § 7 per-cell bounding required; § 1-3 streaming + SQL-side + indexes; explicit math-note compliance section |
| **Phase 5 multimodal clustering** | § 1-4 streaming + SQL + indexes + bounded; multimodal clustering operates on per-season survivor set (~28-32 kits), NOT global archive |
| **Phase 7 2-layer joint-gate** | § 2 push aggregation to SQL where joint-gate pass criteria are SQL-expressible |
| **Wave 1.5 Stage 3 re-impl** | § 1-3 patterns apply to substrate query usage |
| **Wave 2 Layers 5+8+9** | § 2 push aggregation to SQL for set keying; § 7 per-cell where applicable |

---

## 6. Cross-references

### 6.1 Engineering disciplines (compose with)

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #1 (math-before-code) + #11 (empirical inspection) + #18 (math-hotspot routing) + #34 (concentration) + #40-#45 (no-class + scaffold-with-pending-decision + framing-audit + design-quality-audit + framing-refusal + vocabulary-lock)

### 6.2 Canonical docs (load-bearing)

- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 4 (math gates require Discipline #46 to ship correctly)
- `canonical/00-ground-state.md` § 1 (this discipline candidate registers as load-bearing pre-Phase-4)

### 6.3 Code surfaces (audit + remediation)

- 5 telemetry fetchall() sites (HIGH risk; remediation queued)
- 2 substrate fetchall() sites (LOW-MEDIUM risk; remediation queued)
- `weapon_knowledge_entries.v1_scope` index addition (quick-win)

### 6.4 Companion docs (Path 1 work)

- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (Path 1 recognition record)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` (KR routing)

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Discipline #46 candidate authored; routes to jack-ryan for engineering-disciplines.md canonical-write at § Discipline #46
**Authority:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Composition:** with Disciplines #1 (math-before-code) + #11 (empirical inspection) + #18 (math-hotspot routing) + #34 (concentration) + #40 (scaffold-with-pending-decision) — Discipline #46 is the DB-query-pattern application of these existing disciplines

**For:** the canonical-write of Discipline #46 (DB Anti-Materialization + Stream Discipline) — production code paths touching DBs whose row counts can exceed ~1,000 rows MUST follow 7 patterns: stream-not-materialize / push-to-SQL / index-filter-columns / bound-every-exploratory-query / audit-cartesian-joins / WAL-mode / per-cell-bounding-for-math-gates. Load-bearing for Path (1) Phase 4 math gates (Pareto + Crowding + Mahalanobis + KL + Eviction) — without this discipline, naive implementation produces kernel-panic-class O(n²) failure as archive grows across seasons. Pre-Phase-4 remediation: `v1_scope` index addition (elrond ~1hr) + telemetry fetchall() refactor (star-lord ~3-5hr) + substrate fetchall() refactor (rocket ~2-3hr).

**Signed:** gandalf (story-and-design steward)
