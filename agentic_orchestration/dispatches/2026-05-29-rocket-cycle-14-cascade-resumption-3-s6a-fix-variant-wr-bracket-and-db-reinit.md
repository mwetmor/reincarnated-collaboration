# Dispatch — Rocket — Cycle 14 Cascade-Resumption-3 S6a-FIX: Variant wr_bracket_pass Inheritance + kit_archive DB Re-Init

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** rocket (content generation seam — generation/, element/, anchor/, foundation/, engine-internal canonical library)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 authorization + Amendments 1-4 (Disc #48 RAM-awareness retired; KR auto-routes in-scope per Amendment 4 hive-state clarification)
- S6a rocket completion record (collab `2cb4204` + engine `41a6287`) — two § 6 surface findings (HALT) per S6a integration smoke
- S6b jack-ryan Gate-2 Pattern E review PASS-with-WARN (collab `9ee9af6`) — all 8 cascade-r3 streams architecturally sound; Instance 6 7-findings CLOSED; KR cleared to route S6c after S6a runtime gate clears
- Hive-mind decision-routing (Matt 2026-05-23 verbatim) — KR ratifies both fix routes per seam-owner authority

**Pattern:** Pattern A-light follow-up patch (~30min-1h implementation + tests; in-seam scope amendment to S6a)
**R48.4 / R48.5 RETIRED per Amendment 3**
**Standalone dispatch this batch** — gandalf parallel thread continues; no other parallel-firing companions

---

## 0. TL;DR

**Two in-seam fixes per KR routing decisions on S6a findings:**

**Fix 1 — variant wr_bracket_pass inheritance:** Change `_build_variant_kit_rows()` at `wave5_season_orchestrator.py:455` so VariantKitRow inherits base kit's season_emit result (NOT default False from emit_map miss). Semantic: variants represent (base kit) × (T4 strategy) × (investment profile) overlays; WR-bracket gate is at base-kit level; variants inherit base kit's gate result (not re-applied per overlay).

**Fix 2 — kit_archive.db re-init at production-fresh-run:** Clear stale rows (18 pre-cascade class-based IDs + 1 S5b smoke run) + implement INSERT OR REPLACE OR DB re-init at run-start for clean A2-1 RE-FIRE-3 cascade. Rocket elects implementation per simpler-implementation principle (KR ratifies either DB re-init OR INSERT OR REPLACE semantics).

**Effort:** ~30min-1h. Both fixes in-seam (rocket owns generation pipeline + kit_archive initialization integration). No cross-seam coordination required.

---

## 1. Required first reads

1. `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-cascade-resumption-3-s6a-integration-smoke-disc11-audit.md` — S6a completion record (two surface findings detail)
2. `agentic_orchestration/cycle-14-hive-mind-state.md` — KR routing decisions section (post-`32ae979`)
3. `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py`:
   - `_build_variant_kit_rows()` lines 455-540 (emit_map sourcing + smoke=True bypass at line 538)
   - `_persist_kit_to_db()` line 398 (plain INSERT without ON CONFLICT)
   - VariantKitRow dataclass line 420
4. `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md` § 6 — alteration_fields semantics + T4 strategy application at simulation runtime (informs variant wr_bracket_pass inheritance reasoning)
5. Your `AGENT_STATE.md` at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — S6a HALTED checkpoint

---

## 2. Scope

### 2.1 Fix 1 — variant wr_bracket_pass inheritance from base kit

**Current behavior (S6a finding):**
- `_build_variant_kit_rows()` builds `emit_map` from `gauntlet_results_json` (Cycle 13 historical data with class-based legendary_ids)
- S2 variant legendary_ids (substrate-derived `{bc_cell_id}_s2_{strategy}_{invest}`) NEVER match Cycle 13 class-based legendary_ids
- All variants default to `wr_bracket_pass=False`
- smoke=True bypass at line 538 (`if smoke: row.wr_bracket_pass = True`) MASKED this

**Required post-fix behavior:**
- Variants inherit base kit's `season_emit` result (base kit produces season_emit via WR-bracket gauntlet at Phase 3)
- Semantic: VariantKitRow represents (base kit) × (T4 strategy) × (investment profile) overlays; WR-bracket gate measured at base-kit mechanical performance; variants share base kit's performance (only T4 strategy + investment profile overlays differ via alteration_fields per gamora research § 6)
- Lookup base kit's season_emit by base_kit_id (not by S2-derived variant legendary_id)

**Implementation approach:**
- Build emit_map keyed on base kit_id (NOT variant legendary_id) from current-cascade gauntlet results
- VariantKitRow inherits emit_map[base_kit_id] result
- Remove or repurpose smoke=True bypass — variants inherit base kit result whether smoke=True or smoke=False
- Verify base kit gauntlet results are available at Phase 3 → variant construction point

### 2.2 Fix 2 — kit_archive.db re-init + clear stale class-based rows

**Current behavior (S6a finding):**
- kit_archive.db has 19 stale rows (18 pre-cascade class-based IDs + 1 S5b smoke run)
- `_persist_kit_to_db()` uses plain INSERT without ON CONFLICT
- Re-runs on same seed hit UNIQUE constraint

**Required post-fix behavior:**
- Production cascade (A2-1 RE-FIRE-3) produces CLEAN run with substrate-led IDs only
- Pre-cascade class-based stale rows cleared
- Re-runs idempotent (either DB re-init OR INSERT OR REPLACE semantics)

**Implementation approach (rocket elects per simpler-implementation):**

**Option A — DB re-init at run-start (deterministic; throws away historical data):**
- At Phase 0 or Phase 1 initialization, clear kit_archive.db before persistence
- Cascade produces fresh kit_archive per run

**Option B — INSERT OR REPLACE semantics (idempotent; preserves historical rows):**
- Change `_persist_kit_to_db()` from plain INSERT to INSERT OR REPLACE
- Re-runs upsert per kit; historical pre-cascade rows persist OR get cleared by separate one-time cleanup

**Hybrid (recommended for cascade-resumption-3 production):**
- One-time cleanup: clear all pre-cascade class-based rows (legendary_ids matching old class-suffix pattern)
- INSERT OR REPLACE semantics for ongoing idempotency
- Cleanup logic preserves rows compliant with S1 substrate-derived ID scheme

KR ratifies any of A / B / Hybrid per seam-owner authority. Rocket elects per simpler-implementation principle.

### 2.3 Tests

- Update existing S3 tests where smoke=True bypass behavior was assumed (per S6a finding: smoke bypass MASKED variant wr_bracket_pass derivation gap)
- New test: variant wr_bracket_pass inherits base kit season_emit (smoke=False mode); base kit with season_emit=True → variants get wr_bracket_pass=True; base kit with season_emit=False → variants get wr_bracket_pass=False
- New test: kit_archive idempotent re-runs (re-fire cascade with same seed; no UNIQUE constraint violations)
- Verify existing 36 S3 tests still PASS (no regression)

---

## 3. Pre-ratified contingent decisions

| Decision point | Pre-ratified action |
|---|---|
| Fix 1 emit_map keying | Base kit_id (NOT variant legendary_id); per KR routing in state file commit (post-`32ae979`) |
| Fix 1 smoke=True bypass | Repurpose or remove — variants inherit base kit result regardless of smoke flag; rocket elects per simpler-implementation |
| Fix 2 implementation | Rocket elects A / B / Hybrid per simpler-implementation; KR ratifies all three options |
| Stale row cleanup criteria (Fix 2 Hybrid) | Match old class-suffix pattern (S1_endgame_{str|dex|int|wis}_NN_{class_name}); preserve rows compliant with S1 substrate-derived scheme (endgame_bc_*) |
| Disc #42a discipline ratification candidacy | smoke-bypass-context-dependent-behavior pattern (Instance 6 sub-case); document for jack-ryan + gandalf canonical-write at Cycle 14 wave-close; NOT in S6a-FIX scope |

---

## 4. Acceptance criteria

### 4.1 Fix 1 — variant wr_bracket_pass inheritance verified

- VariantKitRow wr_bracket_pass field populated from base kit season_emit (NOT from emit_map miss default False)
- Disc #11 grep verification: `_build_variant_kit_rows()` sources emit_map from current-cascade base kit gauntlet results (NOT historical Cycle 13 JSON)
- New test: variant inherits base kit wr_bracket_pass; smoke=False mode produces wr_bracket_pass=True for variants of passing base kits

### 4.2 Fix 2 — kit_archive idempotent + clean

- Stale pre-cascade class-based rows cleared OR INSERT OR REPLACE handles them
- Re-fire cascade on same seed: no UNIQUE constraint violations
- Disc #11 grep on kit_archive.db: zero rows with class-suffix legendary_ids (post-cleanup)

### 4.3 S6a smoke re-fire PASSES

After both fixes land, rocket re-runs S6a integration smoke (per S6a § 2.1 scope; smoke=False mode):
- Phase 2-7 pipeline fires end-to-end without halt
- PM-1 input cardinality > 22 (NOT degenerate fallback); GMM BIC-selected
- Wave A + F-C + Wave B all fire with cost-tracker accumulating
- Phase 7 cohesion gate operational
- ≥1 kit shipped on small sample

### 4.4 Tests

- All existing tests PASS (no regression beyond pre-existing 7 TestGauntletKitResult failures per gamora S2 surface)
- New tests for Fix 1 + Fix 2 PASS

### 4.5 Tag

- Engine commit + tag (rocket prefix per CLAUDE.md: e.g., `rocket/v1.0-cascade-r3-s6a-fix-variant-wr-bracket-db-reinit-1`)

---

## 5. Out-of-scope for S6a-FIX

- A2-1 RE-FIRE-3 full season production (S6c; sequential after S6a smoke re-fire PASS)
- Modifications to S1-S7-S5-S2-S3-S5b architectural code beyond the two findings
- PM-1 algorithm modifications (S3 + Fix 1 address the input cardinality issue; algorithm separate)
- Phase 7 cohesion threshold modifications (scaffold-flag separate Pattern B)
- LLM cost guard / $50 soft cap modifications
- Discipline canonical-writes (jack-ryan owns; deferred to Cycle 14 wave-close)
- Wave B prompt template modifications (gandalf seam; closed)
- Cross-seam refactor (both fixes in-seam at rocket)

---

## 6. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Base kit gauntlet results not available at variant construction point** | Phase 3 ordering issue prevents inheritance lookup | Halt + surface to KR — coordinate with gamora seam (Phase 3 gauntlet) |
| **Stale row cleanup pattern surfaces unexpected legacy rows** | More legacy ID patterns surface beyond old class-suffix | Document at completion record; rocket elects per simpler-implementation |
| **S6a smoke re-fire HALTS again after fixes** | Pipeline still fails post-S6a-FIX | Halt + surface to KR — different root cause; new investigation cycle |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-fix | Halt + surface to KR |
| **S6a-FIX effort exceeds ~2h** | Implementation complexity surfaces significantly beyond ~30min-1h estimate | Surface to KR — scope reconsideration |

---

## 7. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #11 empirical inspection** | Acceptance gates § 4.1-4.2 grep + smoke re-fire verification |
| **Disc #42a framing-audit Q1-Q6** | LOAD-BEARING — Fix 1 closes smoke-bypass-context-dependent-behavior pattern (Instance 6 sub-case); Disc #42a discipline architecture data point for jack-ryan + gandalf canonical-write at Cycle 14 wave-close |
| **Disc #45 vocabulary lock** | Fix 2 cleanup criteria (clear class-suffix legendary_ids) enforces vocabulary lock at kit_archive layer |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate |
| **Recognition → empirical validation → commit** | Recognition: S6a finding (variant wr_bracket_pass + DB UNIQUE); Validation: § 4 acceptance + S6a smoke re-fire; Commit: rocket auto-commits per CLAUDE.md addendum |

---

## 8. Deliverables

1. **Engine commit(s)** — Fix 1 (wave5_season_orchestrator.py:455 _build_variant_kit_rows + base kit emit_map sourcing) + Fix 2 (kit_archive cleanup + idempotency) + tests + tag (rocket prefix)
2. **AGENT_STATE.md checkpoint** at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — S6a-FIX CLOSED + S6a smoke re-fire PASS + S6c queued
3. **Completion record appended to this dispatch file** — captures: (a) Fix 1 implementation evidence + new test results; (b) Fix 2 implementation evidence + idempotency test; (c) S6a smoke re-fire results (Phase 2-7 end-to-end PASS + PM-1 cardinality > 22 + Wave B fires + cost-tracker accumulates + ≥1 shipped); (d) any surface-to-KR findings
4. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 9. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 hive-state clarification (KR auto-routes in-scope per hive-mind decision-routing) — KR ratifies both fix routes per seam-owner authority based on rocket S6a audit evidence

**Rocket session-start protocol:**
1. Onboard via § 1 required first reads (S6a completion record + state file KR routing decisions)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption — Fix 1 IS the closure of smoke-bypass-context-dependent-behavior pattern (Instance 6 sub-case)
3. Execute § 2.1 (Fix 1) + § 2.2 (Fix 2) + § 2.3 (tests)
4. Apply § 4 acceptance gates INCLUDING § 4.3 S6a smoke re-fire (smoke=False; small sample; end-to-end PASS)
5. Surface per § 6 if triggered — auto-route in-scope per hive-mind decision-routing
6. Author § 8 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on S6a-FIX close:** verify § 4 acceptance + § 8 deliverables INCLUDING smoke re-fire PASS; route S6c dispatch (A2-1 RE-FIRE-3 full season_001 production fire; rocket primary; LLM-cost-bearing).

**Cascade trajectory:** S6a-FIX (closes findings + S6a smoke re-fire) → S6c (A2-1 RE-FIRE-3) → A2-2 → A2-7 + D13 parallel-fire → Cycle 14 v1 MVP D9 close.

**Signed:** knight-rider (orchestrator)
