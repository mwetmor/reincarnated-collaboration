# research.db — narrative-content archive

**Source DB:** `~/Games/reincarnated-engine/research.db`
**As-of date (last write):** 2026-05-07 05:12 (untouched 9 days at archive time)
**Archive date:** 2026-05-16
**Archivist:** elrond (Phase-1 cleanup per data-architecture audit § 7)
**Audit reference:** `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` § 3.4
**Dispatch reference:** `agentic_orchestration/dispatches/2026-05-16-elrond-A-research-db-retirement.md`
**Supersedes decisions-log entry:** 2026-05-07 (research.db consolidation deferral)

## What this archive contains

Two things:

1. **This markdown** — verbatim preservation of the narrative-only tables (`research_notes`, `bugs_log`) — the content the engine team explicitly wrote as research findings and bug history, not as side-effects of generation. Plus structural-table schema + row-count inventory so the rest of the database is documented even though its content is mirrored (in concept) in `data/telemetry.db`.

2. **Binary snapshot** — `archive/research-db-2026-05-07.db` (2.6 MB, SHA-256 `3846b98b272386dc946104676da7cff6ac1f86f529be195799af7b289f96351e`). Lossless preservation of the full 11-table DB exactly as it stood on retirement. The binary lives committed in this directory as a steward-call belt-and-suspenders against the audit's "all structural content is in telemetry.db" assertion — if any structural row turns out to be unique-to-research.db, it remains recoverable here. The binary is the canonical historical record; this markdown is the human-readable companion.

## Archive scope vs dispatch scope

Dispatch A instructed "preserve all row content verbatim" — for `research_notes` (5) and `bugs_log` (5) this is done inline below. For the structural tables (`fight_results` 13,040 rows; `skills` 166; `monsters` 40; `gauntlet_matchups` 110; `classes` 11; `generation_runs` 1; `trial_bosses` 1) verbatim markdown would be unwieldy and redundant with the binary snapshot — so this markdown captures schema + counts + the small-table content, and points to the binary for the row-level data. Documented deviation; same archival completeness, more practical surface.

---

## Section A — `research_notes` (5 rows, verbatim)

### Schema

```sql
CREATE TABLE research_notes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    date                TEXT NOT NULL,
    category            TEXT,              -- finding / hypothesis / decision / observation
    title               TEXT NOT NULL,
    body                TEXT,
    run_id              TEXT
);
```

### Row 1 — finding (season_000042)

- **id:** 1
- **date:** 2026-05-07
- **category:** finding
- **title:** Phase 0 VALIDATED — seed 42, fire theme
- **run_id:** season_000042
- **body:**

> Full season generation completed successfully. 11/11 classes converged (0 failures). Trial boss at 50.5% defeat rate (target 50%). 40 monsters generated. All 6 Phase 0 success criteria met. Generation time: 370.8 seconds unattended.

### Row 2 — observation (season_000042)

- **id:** 2
- **date:** 2026-05-07
- **category:** observation
- **title:** Balance modifiers cluster low (0.20-0.60) for mage archetypes
- **run_id:** season_000042
- **body:**

> All fire_mage and water_mage classes required modifiers in the 0.20-0.42 range to hit 50% win rate. This suggests elemental skills generate far more raw damage than expected at tier 50. Physical warrior (class_0005/0010) required modifiers of 0.60-0.90, suggesting physical damage is proportionally weaker post-armor-reduction. Worth investigating whether the physical damage formula needs rebalancing for Phase 1.

### Row 3 — observation (season_000042)

- **id:** 3
- **date:** 2026-05-07
- **category:** observation
- **title:** Binary search convergence: most classes settle in 2-8 iterations
- **run_id:** season_000042
- **body:**

> With max_iterations=10 and TOLERANCE=0.03, all 11 classes converged. Average was ~5.5 iterations. The challenge class (target 40%) converged fastest at 4 iterations; the fire mage with utility skills (class_0006) took longest at 10. The binary search bracket [0.20, 4.0] was never saturated — no class needed a modifier outside this range.

### Row 4 — hypothesis (season_000042)

- **id:** 4
- **date:** 2026-05-07
- **category:** hypothesis
- **title:** Weird class (support_healer) may need dedicated balance handling
- **run_id:** season_000042
- **body:**

> class_0011 (Cinder Priestess, support_healer, fire) ended at 47.2% win rate against a 50% target — converged but on the low end. Its skill loadout is sustain-heavy (3× sustain, 2× primary_attack, 1× defensive). The balance loop adjusts damage output but sustain-focused classes may need a different balance metric in Phase 1 (e.g., survival time rather than win rate).

### Row 5 — decision (season_000042)

- **id:** 5
- **date:** 2026-05-07
- **category:** decision
- **title:** Trial HP calibrated to 2-3× class reference for Phase 0 solo
- **run_id:** season_000042
- **body:**

> Phase 1 spec calls for 6-8× HP for group content. Phase 0 reduced to 2-3× for meaningful solo calibration. At 41,473 HP with armor and threshold heals, the trial required a balance modifier of 0.2125 to hit 50% defeat rate — meaning the raw generated stats were too strong even at 2-3×. Phase 1 will need to rethink whether trial boss calibration should be separate from solo-class calibration.

---

## Section B — `bugs_log` (5 rows, verbatim)

### Schema

```sql
CREATE TABLE bugs_log (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    discovered_session  TEXT,
    component           TEXT NOT NULL,
    title               TEXT NOT NULL,
    symptom             TEXT,
    root_cause          TEXT,
    fix_applied         TEXT,
    impact              TEXT,
    date_discovered     TEXT
);
```

### Row 1 — simulation/effect_resolver.py (2026-05-07)

- **id:** 1
- **discovered_session:** 1c803d9d
- **component:** simulation/effect_resolver.py
- **title:** List mutation during DoT tick loop
- **symptom:** `ValueError: list.remove(x): x not in list` — crash during combat when shield effects expired mid-iteration
- **root_cause:** `absorb_with_shield()` removed items from `active_effects` while the tick loop was iterating over the same list
- **fix_applied:** Iterate over `list(combatant.active_effects)` snapshot; use list comprehension for cleanup after the loop
- **impact:** Fight engine crashed on any fight where a shield effect expired during a DoT tick
- **date_discovered:** 2026-05-07

### Row 2 — simulation/combatant.py + foundation/math_model.py (2026-05-07)

- **id:** 2
- **discovered_session:** 1c803d9d
- **component:** simulation/combatant.py + foundation/math_model.py
- **title:** Non-intelligence classes depleted mana in <11 casts
- **symptom:** Win rates for wind/earth classes stuck at 10-20% — classes did almost nothing after opening burst
- **root_cause:** Mana formula was `100 + int×1.0` only. Wind caster (int=9) had mana pool of 109; primary attack cost ~10 mana → empty after ~11 casts. No fallback combat action.
- **fix_applied:** (1) Add wisdom to mana formula: `max_mana = 100 + int + wisdom×0.5`. (2) Use `max(int,wis)` for regen scaling. (3) Add fallback auto-attack (375 base physical) when mana-depleted or all skills on cooldown.
- **impact:** All non-intelligence-primary classes were effectively broken; would have invalidated elemental balance entirely
- **date_discovered:** 2026-05-07

### Row 3 — simulation/balance_loop.py (2026-05-07)

- **id:** 3
- **discovered_session:** 1c803d9d
- **component:** simulation/balance_loop.py
- **title:** Proportional balance loop oscillated and never converged
- **symptom:** Balance modifier stuck bouncing between extremes after 10 iterations; classes landing at 90%+ or <5% win rates
- **root_cause:** Proportional step formula: `modifier *= (1 ± STEP_RATE × |gap| / TOLERANCE)`. A gap of -0.30 with STEP_RATE=0.20 produced adjustment of -2.0, sending modifier negative, hitting the 0.3 floor, then bouncing back. System was unstable.
- **fix_applied:** Replace proportional adjustment with binary search: maintain `[low, high]` bracket, bisect each iteration. Guaranteed monotone convergence. Added separate wider bracket `[0.10, 8.0]` for trial boss.
- **impact:** No classes could converge to target win rate; entire balance loop was non-functional
- **date_discovered:** 2026-05-07

### Row 4 — generation/trial_generator.py (2026-05-07)

- **id:** 4
- **discovered_session:** 1c803d9d
- **component:** generation/trial_generator.py
- **title:** Trial boss HP factor made solo fights impossible
- **symptom:** Trial boss defeat rate stuck at 100% — every class lost every fight regardless of modifier
- **root_cause:** `TRIAL_HP_FACTOR_RANGE` was `(6.0, 8.0)` — from the group-content spec. Solo player DPS ~2K/sec × 50s survival = 100K damage, far short of 120-160K HP + 22.5% threshold heals ≈ 200K effective HP.
- **fix_applied:** Reduce `TRIAL_HP_FACTOR_RANGE` to `(2.0, 3.0)` for Phase 0 solo calibration. Docs note that 6-8× is the group-content target for Phase 1.
- **impact:** Trial balance loop could never converge; defeat rate was always ~100%
- **date_discovered:** 2026-05-07

### Row 5 — generation/trial_schema.py (2026-05-07)

- **id:** 5
- **discovered_session:** 1c803d9d
- **component:** generation/trial_schema.py
- **title:** TrialBoss missing threat_tier field — LLM naming failed
- **symptom:** `WARNING: Trial naming failed: 'TrialBoss' object has no attribute 'threat_tier'` — trial boss kept ID as name
- **root_cause:** `name_monster()` reads `monster.threat_tier` to include in the LLM prompt. `TrialBoss` schema had no such field.
- **fix_applied:** Add `threat_tier: str = 'trial'` to `TrialBoss` model
- **impact:** Cosmetic only — trial boss name stayed as `trial_0001` in season output
- **date_discovered:** 2026-05-07

---

## Section C — single-row metadata tables (verbatim)

### `generation_runs` (1 row)

| Column | Value |
|---|---|
| run_id | season_000042 |
| seed | 42 |
| theme_element | fire |
| n_classes | 11 |
| n_monsters | 40 |
| validation_passed | 0 |
| convergence_failures | 1 |
| canonical_fallbacks | 0 |
| trial_target_defeat_rate | 0.5 |
| trial_actual_defeat_rate | 0.4818 |
| trial_converged | 1 |
| duration_seconds | 18.6 |
| generated_at | 2026-05-07T09:12:45.160008+00:00 |
| notes | (empty) |

### `trial_bosses` (1 row)

| Column | Value |
|---|---|
| id | trial_0001 |
| run_id | season_000042 |
| name | trial_0001 (LLM naming failed per bugs_log #5) |
| dominant_element | fire |
| signature_mechanic | phase_stat_shift |
| max_hp | 41,473.0 |
| armor | 6,365.0 |
| n_phases | 3 |
| n_skills | 6 |
| target_defeat_rate | 0.5 |
| actual_defeat_rate | 0.4818 |
| balance_modifier | 0.2125 |
| convergence_iterations | 4 |
| converged | 1 |

### `balance_overview` (VIEW — not a persisted table)

Derived from `classes` table. Aggregates: `season_000042` — 11 classes, avg_winrate=0.5073, avg_deviation=0.02, max_deviation=0.07, avg_iterations=5.7, max_iterations=10, n_converged=10, avg_modifier=0.4705. (One class did not formally `converged=1` — see notes #4 above for the support_healer outlier.)

### `class_summary` (VIEW — not a persisted table)

Derived join `classes ⋈ generation_runs`. Surfaces the 11 class rows from season_000042 with theme_element decoration. Content recoverable from the binary snapshot or from telemetry.db's `classes` table.

---

## Section D — structural tables (schema + counts; row content preserved in binary snapshot)

These tables hold structural generation output for `season_000042` that is mirrored, in concept, by `data/telemetry.db`. The audit's § 3.4 finding holds: *"Everything in research.db that has structural meaning is now in telemetry.db."* Row content is preserved losslessly in `archive/research-db-2026-05-07.db` for the historical record; markdown verbatim is impractical for the larger tables.

### `classes` (11 rows)

Per-class generation summary for `season_000042`. Schema:

```sql
CREATE TABLE classes (
    id, run_id, name, title_completion, flavor_text, archetype_tag, dominant_element,
    stat_strength, stat_vitality, stat_intelligence, stat_wisdom, stat_agility, stat_dexterity,
    stat_total, n_skills, target_winrate, actual_winrate, winrate_gap, balance_modifier,
    convergence_iterations, converged, role_type,
    PRIMARY KEY (id, run_id),
    FOREIGN KEY (run_id) REFERENCES generation_runs(run_id)
);
```

Telemetry.db equivalent: `classes` table (234 rows across 23 seasons, including season_000042).

### `monsters` (40 rows)

Per-monster generation summary for `season_000042`. Schema:

```sql
CREATE TABLE monsters (
    id, run_id, name, flavor_text, threat_tier, archetype_tag, dominant_element,
    max_hp, armor, in_gauntlet, n_skills,
    PRIMARY KEY (id, run_id),
    FOREIGN KEY (run_id) REFERENCES generation_runs(run_id)
);
```

Telemetry.db equivalent: `monsters` table (1,008 rows across all seasons, including season_000042).

### `skills` (166 rows)

Skill records for classes + monsters + trial in `season_000042`. Schema:

```sql
CREATE TABLE skills (
    run_id, owner_id, owner_type, skill_id, skill_name, role, element, geometry,
    timing_name, cooldown_seconds, mana_cost, composition_mode, canonical_pair_ref, flavor_text,
    PRIMARY KEY (run_id, owner_id, skill_id),
    FOREIGN KEY (run_id) REFERENCES generation_runs(run_id)
);
```

Telemetry.db equivalent: `abilities` table (4,561 rows across all seasons; same row-shape semantics).

### `gauntlet_matchups` (110 rows)

Per-(class, monster) win-rate matrix for `season_000042` (11 classes × 10 monsters or similar combinatoric). Schema:

```sql
CREATE TABLE gauntlet_matchups (
    run_id, class_id, monster_id, win_rate,
    PRIMARY KEY (run_id, class_id, monster_id)
);
```

Telemetry.db equivalent: `class_monster_win_rates` table (990 rows across all seasons).

### `fight_results` (13,040 rows)

Per-fight outcome detail for `season_000042` — the largest table by row count. Schema:

```sql
CREATE TABLE fight_results (
    id, run_id, phase, owner_id, opponent_id, iteration, fight_index, modifier,
    winner, duration_seconds, termination_reason,
    a_final_hp, b_final_hp, a_max_hp, b_max_hp,
    a_final_hp_pct, b_final_hp_pct, a_damage_dealt, b_damage_dealt,
    a_actions_taken, b_actions_taken
);
CREATE INDEX idx_fights_run_phase ON fight_results(run_id, phase);
CREATE INDEX idx_fights_owner ON fight_results(run_id, owner_id);
```

Telemetry.db equivalent: `class_fight_loadouts` table (1,925,180 rows). The schema is broader on the telemetry side (per-fight loadout snapshot included); the research.db version is the older, narrower per-fight record predating the loadout-snapshot pattern.

---

## Section E — engine code that still references `research.db`

The following two scripts are in **star-lord's seam** (`reincarnated-engine/scripts/`); their updates flow through knight-rider → star-lord per ADR-004, not elrond:

1. **`scripts/db.py`** (~34 KB) — `DB_PATH = Path("research.db")` at line 20; "Database initialized at research.db" banner at line 708; module docstring (line 4) refers to "Single SQLite file at research.db in the project root." The script appears to be a pre-bootstrap utility; the audit notes it is no longer referenced by production code.

2. **`scripts/capture-regression-baseline.py`** — copies `research.db` + WAL/SHM as part of the regression baseline snapshot (lines 50, 150); dumps its schema (line 285); script-level docstring (line 21) lists research.db under copied artifacts.

Recommended star-lord MIGRATION.md entry (one-liner candidate):

```
- 2026-05-16 — research.db retired per data-architecture audit § 7 Phase 1.
  Archived to `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md`
  + `archive/research-db-2026-05-07.db` (binary snapshot, SHA-256 3846b98b...).
  Action items (star-lord seam): (1) remove research.db references from scripts/db.py;
  (2) remove research.db handling from scripts/capture-regression-baseline.py (regression
  snapshots no longer need it).
```

---

## Provenance + integrity

- Binary snapshot SHA-256: `3846b98b272386dc946104676da7cff6ac1f86f529be195799af7b289f96351e`
- Snapshot file size: 2,678,784 bytes
- Snapshot mtime preserved at copy: 2026-05-16 (filesystem cp)
- Source mtime at archive: 2026-05-07 05:12 (untouched since)
- WAL sibling at source: `research.db-wal` (0 B, 2026-05-15 — empty WAL, no uncommitted writes)
- SHM sibling at source: `research.db-shm` (32 KB, 2026-05-16 — recent stat-driven open by sqlite3 CLI during this archival pass; no schema changes)

## Status

- **Archive markdown:** committed (this file)
- **Binary snapshot:** committed via `.gitignore` `!archive/*.db` exception
- **Source DB removal:** PENDING — destructive `rm` step (ADR-006) awaiting Matt's per-statement authorization. Elrond will execute on go.
- **scripts/db.py and scripts/capture-regression-baseline.py update:** PENDING — star-lord-seam work, knight-rider sequences via ADR-004 MIGRATION.md.
- **Decisions-log entry:** PENDING — knight-rider drafts per dispatch A item 3.

— elrond, 2026-05-16
