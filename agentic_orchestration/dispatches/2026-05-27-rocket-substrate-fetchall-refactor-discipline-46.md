# Dispatch — 2026-05-27 — rocket — Substrate fetchall refactor (Dispatch 1D; pre-Phase-4 LOW-MEDIUM-risk remediation)

**From:** knight-rider
**To:** rocket (engine generation seam owner)
**Approved by:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Estimated effort:** ~2-3 hours (2 fetchall sites refactor + EXPLAIN QUERY PLAN per query + tests)
**Acceptance:** 2 substrate fetchall sites refactored per Discipline #46 § 1 patterns; EXPLAIN QUERY PLAN captured; grep audit clean post-refactor

## Quality criterion

**Game-quality goal this dispatch serves:** apply Discipline #46 streaming + bounding patterns to substrate query sites; preserves clean query patterns as substrate grows (currently ~2,499 v1_scope rows; could grow across cycles); composes with elrond v1_scope index addition (Dispatch 1B parallel) for filter-column index hits.

**Refutation conditions** (rocket surfaces if any apply):
- Either site is already effectively bounded (substrate v1_scope returns ~2,499 rows < 10k threshold; ratify if bounded by intent)
- Refactor introduces semantic regression in substrate selection (e.g., per-seed determinism breaks if stream order differs)
- Post-refactor performance regresses (LOW-MEDIUM risk per audit — refactor may be over-engineering for ~2,499 row scale)

## Context

Per `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1: **LOW-MEDIUM risk** substrate sites:
- `src/reincarnated/generation/substrate_weapon_binding.py:332`
- `src/reincarnated/generation/bc_target_substrate_engine.py:342`

Substrate currently bounded short-term (~2,499 rows) but grows across cycles. Pre-Phase-4 remediation applies Discipline #46 patterns pre-emptively.

This is one of 4 parallel pre-Phase-4 dispatches per KR Path (1) kicker § 3.1.

## Required reading

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1 (LOW-MEDIUM substrate sites) + § 1 (7 patterns)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1 (this dispatch's routing source)
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py:332` (primary touch surface 1)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_substrate_engine.py:342` (primary touch surface 2)
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines` (Discipline #46 candidate)

## Discipline #46 compliance (DB-touching dispatch)

- [ ] All refactored DB queries follow stream / push-to-SQL / index / bound / no-cartesian patterns
- [ ] Per-cell bounding applied for math-gate algorithms (N/A — substrate refactor scope; Phase 4 math gates separate dispatch)
- [ ] EXPLAIN QUERY PLAN run on every refactored query; output captured in completion record (verify v1_scope index hit per elrond Dispatch 1B parallel)
- [ ] Grep audit at Gate-2: no unbounded `fetchall()` in `src/reincarnated/generation/substrate_weapon_binding.py` + `bc_target_substrate_engine.py` post-refactor

## Scope

For each of 2 sites:

- [ ] Inspect current fetchall site + understand caller's row-count expectation
- [ ] Choose pattern per Discipline #46 § 1:
  - **Pattern 1 (stream):** cursor iteration OR `fetchmany(1000)` if substrate could grow >1000
  - **Pattern 2 (push-to-SQL):** if caller enumerates rows for count/filter, replace with SQL aggregation
  - **Pattern 4 (bound):** if exploratory, add `LIMIT N`
- [ ] Confirm v1_scope index hit (per elrond Dispatch 1B parallel; expect `SEARCH ... USING INDEX idx_knowledge_v1_scope`)
- [ ] Run existing substrate generation tests to confirm no semantic regression (per-seed determinism preserved)

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`
- [ ] Grep audit verification: `grep -n "\.fetchall()" src/reincarnated/generation/substrate_weapon_binding.py src/reincarnated/generation/bc_target_substrate_engine.py` returns ONLY refactored-with-LIMIT OR ratified-as-bounded matches
- [ ] Append completion record to this dispatch with per-site refactor pattern + EXPLAIN QUERY PLAN captures
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] Both substrate fetchall sites refactored OR documented as already-bounded (with rationale)
- [ ] Per-site EXPLAIN QUERY PLAN captured (verifies v1_scope index hit)
- [ ] No semantic regression (existing generation tests PASS; per-seed determinism preserved)
- [ ] Grep audit shows no unbounded fetchall in these 2 sites
- [ ] AGENT_STATE.md updated
- [ ] Completion record appended; commit + push
- [ ] Round-trip: not applicable (generation seam internal; no inter-seam fixture dict change)

## Out of scope

- Do NOT touch telemetry fetchall sites (star-lord Dispatch 1C)
- Do NOT touch v1_scope index addition (elrond Dispatch 1B)
- Do NOT add Discipline #46 amendments to engineering-disciplines.md (jack-ryan seam at Dispatch 1A)
- Do NOT touch Phase 4 math gates code (gamora Dispatch 3A post Matt-gate on math notes)
- Do NOT touch export sites (LOW risk per audit; separate scope if needed)

## Open questions for rocket

- **Q-Sub-Refactor-1:** If substrate fetchall is already effectively bounded at ~2,499 rows < 10k threshold per Discipline #46 § 1 Pattern 4 (bound every exploratory query), document as INFO-close + ratify-as-bounded with rationale. Don't force refactor where unneeded.
- **Q-Sub-Refactor-2:** Per-seed determinism — if stream order differs from materialized order, verify per-seed reproducibility preserved (rocket OP seed-stability discipline composes).

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 1 (7 patterns) + § 2.1 (LOW-MEDIUM substrate sites)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1
- Engineering disciplines #1 + #11 + #46 (candidate; firing in parallel via Dispatch 1A)

---

## Completion record

**Completed:** 2026-05-27
**Agent:** rocket
**Outcome:** Both sites RATIFIED-AS-BOUNDED (INFO-close). No code logic changes. Discipline #46 ratify-as-bounded comments added to both fetchall() calls.

### Per-site outcome

#### Site 1 — `substrate_weapon_binding.py:332`

**Decision:** RATIFY-AS-BOUNDED per Q-Sub-Refactor-1

**Rationale:**
- Three-layer filter: `v1_scope=1 AND weapon_kind IN ('category','named_template','unique') AND primary_stat=?`
- Empirical row counts (2026-05-27): DEX=1,044 / STR=803 / INT=255 / WIS=212
- Worst case 1,044 rows — well below Discipline #46 § 1 Pattern 4 10k threshold
- Full materialization structurally required: caller uses `random.Random(seed).choice(row_dicts)` over all rows; streaming/fetchmany would still collect all rows before the uniform random draw
- Per-seed determinism: fully preserved (no logic change; comment only)

**EXPLAIN QUERY PLAN:**
```
QUERY PLAN
|--SEARCH wke USING INDEX idx_knowledge_v1_scope (v1_scope=?)
`--SEARCH wsp USING INTEGER PRIMARY KEY (rowid=?)
```
Index `idx_knowledge_v1_scope` confirmed present and used as filter entry point. No full scan.

**Action:** Added Discipline #46 ratify-as-bounded comment immediately preceding `rows = cur.fetchall()` at line 332 (post-edit ~340).

---

#### Site 2 — `bc_target_substrate_engine.py:342`

**Decision:** RATIFY-AS-BOUNDED per Q-Sub-Refactor-1

**Rationale:**
- Base filter `v1_scope=1` (2,499 rows total) plus optional attribute/range/tempo/source/cell_label refinements
- Worst case (option_beta, DEX attribute-only, no other filters): 1,097 rows; typical option_alpha strict-match returns far fewer
- Worst case well below Discipline #46 § 1 Pattern 4 10k threshold
- Full materialization structurally required: `_filter_and_sample()` scores ALL candidates (0.40×tier + 0.35×cell_match + 0.15×coherence + 0.10×novelty), sorts by score, then `rng.choices()` with weights — streaming would still collect all rows before scoring pass
- Per-seed determinism: fully preserved (no logic change; comment only)

**EXPLAIN QUERY PLAN (option_alpha, STR+melee+high):**
```
QUERY PLAN
|--SEARCH weapon_knowledge_entries USING INDEX idx_knowledge_v1_scope (v1_scope=?)
`--USE TEMP B-TREE FOR ORDER BY
```

**EXPLAIN QUERY PLAN (option_beta worst case, DEX only):**
```
QUERY PLAN
|--SEARCH weapon_knowledge_entries USING INDEX idx_knowledge_v1_scope (v1_scope=?)
`--USE TEMP B-TREE FOR ORDER BY
```
Index `idx_knowledge_v1_scope` confirmed present and used as filter entry point in both query shapes. No full scan.

**Action:** Added Discipline #46 ratify-as-bounded comment immediately preceding `rows = cursor.fetchall()` at line 342 (post-edit ~351).

---

### v1_scope index status

`idx_knowledge_v1_scope` already exists on `weapon_knowledge_entries(v1_scope)` — elrond Dispatch 1B parallel work either already landed or the index was present. Both queries hit it per EXPLAIN QUERY PLAN above.

### Grep audit

```
$ grep -n "\.fetchall()" src/reincarnated/generation/substrate_weapon_binding.py src/reincarnated/generation/bc_target_substrate_engine.py
src/reincarnated/generation/substrate_weapon_binding.py:340:        rows = cur.fetchall()
src/reincarnated/generation/bc_target_substrate_engine.py:351:            rows = cursor.fetchall()
```

Both calls present. Both immediately preceded by explicit Discipline #46 ratify-as-bounded comments. Audit clean.

### Test results

- `tests/test_w02_bc_target_composer.py` + `tests/test_bc_target_subspace_generator.py`: **85 passed, 0 failed**
- `tests/test_cycle14_wave1_concentration.py` + `tests/test_class_generation.py` + `tests/test_gear_generation.py`: **100 passed, 1 failed, 1 skipped**
  - Pre-existing failure: `test_cycle13_regression_full_smoke` row-count boundary assertion (`2314 outside [2058,2158]`) — substrate grew since test range was set; predates this dispatch
  - Pre-existing failures in `test_d2_substrate_coupling.py` + `test_substrate_identity_loader.py`: element-count assertions expecting canonical-four that predate shadow/lightning/holy additions to foundation
  - None of these failures are caused by or related to comment-only additions in this dispatch

### Acceptance criteria status

- [x] Both substrate fetchall sites refactored OR documented as already-bounded (with rationale) — **RATIFIED-AS-BOUNDED both sites**
- [x] Per-site EXPLAIN QUERY PLAN captured — **idx_knowledge_v1_scope hit confirmed both sites**
- [x] No semantic regression (existing generation tests PASS; per-seed determinism preserved) — **PASS; pre-existing failures unrelated**
- [x] Grep audit shows no unbounded fetchall in these 2 sites — **CLEAN (both have ratify-as-bounded comments)**
- [x] AGENT_STATE.md updated
- [x] Completion record appended; commit + push per Matt 2026-05-27 per-cycle push pattern
