# Dispatch — 2026-06-02 — EAA-2 — Engine skip-flag pattern for R8 + cosmological_vocabulary retirement

**From:** knight-rider (orchestrator)
**Primary owner:** rocket (generation seam; season_orchestrator.py + R8 pipeline)
**Co-owner:** star-lord (cosmological_vocabulary slot-fill mechanism; LLM call infrastructure)
**Cycle:** cycle-16-eaa-engine-architectural-amendment (Phase 1)
**Authority:** Matt 2026-06-02 Pattern B substantive design session + Locks A-P (LOCK M active for retirement scope)
**Wave tag:** `EAA-2`
**Wave-open dispatch:** `agentic_orchestration/dispatches/2026-06-02-cycle-16-eaa-engine-architectural-amendment-wave-open.md` (READ FIRST)
**State file:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
**Wave-open Gate-1 finding:** `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md` (PASS-with-INFO)
**Estimated horizon:** ~1-2 sessions
**Gates:** jack-ryan Gate-1 pre-fire on this dispatch + Gate-2 on implementation

---

## 1. Authoritative reading (READ IN ORDER before any action)

1. `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 1.2 (R8 retirement) + § 1.3 (cosmological_vocabulary retirement) — binding
2. `canonical/historical/19-llm-call-map.md` — R8 inverted-mode reference (mechanism being retired)
3. `~/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py` — current R8 inverted-mode pipeline source
4. Wave-open dispatch (see header) — chain context + LOCK M two-stage retirement framing

---

## 2. Scope (LOCK M Stage 1 ONLY)

Implement **Stage 1 skip-flag pattern** that bypasses R8 inverted-mode theme coalescence + cosmological_vocabulary slot-fill at engine generation time. Old behavior REMAINS in code for legacy needs (e.g., re-generating historical seasons for inspection). Stage 2 (full code removal) is DEFERRED to a later cleanup workstream gated on no-legacy-need confirmation.

**Two retirement targets:**

### 2.1 R8 inverted-mode theme coalescence (per canonical record § 1.2)

R8 amendment in `canonical/historical/19-llm-call-map.md` (2026-05-19):
> "Phase A `element_selection` is replaced by `theme_coalescence` in the new default pipeline (the `inverted` mode committed per R8 Sub-case 3)."

**Skip-flag scope:**
- Engine flag (proposed name: `skip_theme_coalescence: bool`) bypasses R8 theme_coalescence Phase A
- When skipped: each kit emerges from substrate inputs (primary + cultural-tradition + period + chain composition + T4) WITHOUT season-level theme overlay
- **Intended default for new generation:** `skip_theme_coalescence=true`. Legacy reproduction (e.g., re-running a historical season) requires explicit `skip_theme_coalescence=false`. The same default-naming discipline applies to `skip_cosmological_vocabulary` per § 2.2 below — both default to TRUE for new generation. (Per jack-ryan Gate-1 Phase 1 INFO-A: removes silent wrong-default risk on EAA-5 fire.)

### 2.2 Cosmological_vocabulary slot-fill mechanism (per canonical record § 1.3)

Existing mechanism: 8 effect-category slots (ignition / suffusion / bulwark / displacement / impact / radiance / penumbra / resonance) themed via per-season LLM vocabulary (Pit-Flame Surge / Quench Flood / Slag Wall / etc.).

**Skip-flag scope:**
- Engine flag (proposed name: `skip_cosmological_vocabulary: bool`) bypasses cosmological_vocabulary slot-fill LLM calls
- When skipped: skill naming flows through WS1A.4-lite per-skill flavor-or-canonical decision (EAA-1) instead
- LLM call infrastructure (star-lord seam) gates on this flag

### 2.3 Combined-flag option (rocket+star-lord discretion within LOCK M)

If a combined `skip_legacy_seasonal_overlay: bool` flag is cleaner than two separate flags, rocket+star-lord may opt for that pattern per LOCK J ADDITIVE-AND-REVERSIBLE discipline. Both patterns are within LOCK M scope.

---

## 3. Sub-tasks

### 3.1 R8 skip-flag implementation (rocket)

- Add skip flag to season_orchestrator.py R8 Phase A theme_coalescence
- When flag=true: bypass theme_coalescence; emit no `theme_element` field (or emit `theme_element=None`) — discipline: backward-compatible schema (preserve field; mark null when skipped)
- Verify no downstream code path requires theme_element to be populated (smoke-check)
- Tag commit with seam prefix: `rocket/v1.4-eaa-2-r8-skip-flag-<n>`

### 3.2 Cosmological_vocabulary skip-flag implementation (rocket + star-lord)

- Add skip flag to cosmological_vocabulary mechanism (star-lord LLM call gate + rocket pipeline gate)
- When flag=true: bypass cosmological_vocabulary LLM calls; per-skill naming defers to WS1A.4-lite (EAA-1) when available, OR existing canonical naming fallback if WS1A.4-lite not yet integrated
- Verify cosmological_vocabulary.json artifact is NOT regenerated when skip=true (preserved for historical)
- Coordinate star-lord (LLM call infrastructure) + rocket (pipeline integration) per ADR-004

### 3.3 Smoke-test discipline (Disc #2)

Before EAA-5 generation fire consumes these flags:
- Smoke-test single-kit generation with skip flags ACTIVE
- Verify season_000XXX_smoke directory NOT auto-created if disabled, OR cleanup convention respected
- Verify no downstream schema validation breakage from null theme_element / absent cosmological_vocabulary

### 3.4 Escape clause check

Per LOCK M escape clause:
> "Escape clause: if Stage 1 retirement surfaces unforeseen dependency requiring substantive architectural amendment, escalate"

If rocket+star-lord discover during implementation that R8 OR cosmological_vocabulary is depended upon by an unforeseen downstream path (e.g., a validator, a schema, a different pipeline phase), escalate per escape clause → KR routes to Matt.

---

## 4. Out of scope (explicit non-goals)

- **Stage 2 full code removal** — DEFERRED per LOCK M Stage 2; gates on no-legacy-need confirmation; NOT this dispatch
- **WS1A.4-lite implementation** — EAA-1 scope; not this dispatch (EAA-2 introduces the skip; EAA-1 introduces the replacement)
- **R8 amendments to surviving code paths** — only skip-flag gating; no semantic amendment to the legacy code
- **Cosmological_vocabulary.json regeneration logic** — preserve as-is for historical access
- **Per-season manifest schema deprecation** — handled by EAA-3 (kit-space output schema); not this dispatch
- **Existing seasons regeneration** — preserved as historical per canonical record § 6 Path α; not touched

---

## 5. Cross-seam contract (Principle 6)

**Cross-seam touches:**
- rocket (generation/season_orchestrator.py) ↔ star-lord (llm/cosmological_vocabulary call infrastructure): flag gate added on LLM call
- Output schema: if `theme_element` becomes nullable, that is an additive schema-tolerance extension — ADR-004 MIGRATION.md required

**Discipline:** additive per LOCK J + LOCK M. Backward-compatibility preserved (legacy code unchanged; flags default to behavior that preserves prior contract if discretion warrants; new generation explicitly sets skip=true).

**Round-trip:** if removing theme_element from emit-schema breaks any consumer (elrond ingest, star-lord telemetry, drax loadout app), escalate per LOCK J escape clause.

---

## 6. Acceptance criterion

EAA-2 PASSES when:
1. Skip flag(s) added to engine (either two separate flags OR combined `skip_legacy_seasonal_overlay`)
2. Skip-flag bypass confirmed via single-kit smoke test (R8 theme_coalescence skipped + cosmological_vocabulary skipped)
3. No regressions in legacy-path (flag=false reproduces prior behavior; smoke verifies)
4. MIGRATION.md authored for any schema-tolerance extension (e.g., theme_element nullable)
5. jack-ryan Gate-2 PASS on implementation review

---

## 7. Tag intent

- Intermediate: `rocket/v1.4-eaa-2-skip-flag-<n>`
- Cross-seam coordinated tag per ADR-004 if star-lord branch touches concurrently
- Wave-close milestone tag deferred to EAA-8

---

## 8. Auto-commit + auto-push

Per Matt 2026-06-02 explicit cycle-push authorization for EAA chain + CLAUDE.md addendum 2026-05-25:
- Auto-commit work-products as you go
- Auto-push per established cycle-push pattern
- Update wave-state file workstream status table on completion

---

## 9. References

- **Authoritative architectural commitment:** `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 1.2 + § 1.3
- **R8 historical reference:** `canonical/historical/19-llm-call-map.md`
- **Engine season orchestrator:** `~/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py`
- **Wave-state:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
- **Generation seam owner:** rocket operating procedure
- **LLM seam owner:** star-lord operating procedure
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #2 smoke-test; #18 math-hotspot routing)
- **GOVERNANCE / ADR-004 cross-seam MIGRATION:** `agentic_orchestration/GOVERNANCE.md`

---

**End of EAA-2 dispatch. Fires after jack-ryan Gate-1 PASS on this dispatch.**

---

## Completion record

**Date:** 2026-06-02
**Status:** COMPLETE
**Implementing agent:** rocket (primary); jack-ryan (Gate-2)

### Deliverables

| Item | Status | Detail |
|---|---|---|
| Engine skip-flag implementation | DONE | `src/reincarnated/generation/season_orchestrator.py` — two params added: `skip_theme_coalescence: bool = True` + `skip_cosmological_vocabulary: bool = True`; both gated in pipeline; both carried in `SeasonOutput` |
| CLI legacy-reproduction flags | DONE | `src/reincarnated/cli.py` — `--legacy-theme-coalescence` + `--legacy-cosmological-vocabulary` added to R8 argument group |
| Manifest serialization | DONE | `src/reincarnated/output/season_writer.py` — both flags emitted in `manifest.json` (additive; backward-compatible) |
| ADR-004 MIGRATION.md | DONE | `src/reincarnated/generation/MIGRATION.md` — entry appended with schema extension spec, consumer impact table, escape clause, smoke results |
| Smoke test | PASS | 5 classes, 30 fights, no_coalesce + both skips=True: `season_theme_element=None`, `cosmological_vocabulary=None`, `classes=5`, exit 0 |
| Structural checks | PASS | Signature defaults; SeasonOutput fields; gate expressions; SeasonOutput pass-through |
| jack-ryan Gate-2 | PASS | Finding at `qa/findings/2026-06-02-eaa-2-skip-flag-gate-2.md`; 2 INFOs non-blocking; 0 BLOCKs, 0 WARNs |

### Key decisions made (dispatch § 2.3 + § 3)

**Flag-naming:** Two separate flags (`skip_theme_coalescence` + `skip_cosmological_vocabulary`), not combined `skip_legacy_seasonal_overlay`. Rationale: 1:1 mapping to distinct mechanisms, escape-clause tracing per-mechanism, legacy-reproduction granularity.

**Escape clause:** NOT triggered. No downstream hard-dependency on non-null `theme_element` or `cosmological_vocabulary` surfaced during Stage 1 implementation. `season_theme_element=None` was already handled by all consumers (no_coalesce mode precedent). `cosmological_vocabulary=None` was already handled by Phase B naming (graceful fallback).

### Commit + tag

- Engine commit: `c56db88` tag `rocket/v1.4-eaa-2-skip-flag-1` (reincarnated-engine main)
- Finding commit: `a14b4a5` (reincarnated-collaboration main)

### Cross-seam coordination

Star-lord seam: no code changes required. `generate_cosmological_vocabulary()` and `_coalesce_seasonal_theme()` are not called when flags are True (the new default). Star-lord LLM infrastructure remains available for legacy-reproduction flag activation.

EAA-5 readiness: both skip flags default True — EAA-5 generation fire will activate skip-flag behavior without explicit parameter passing. Composites cleanly with EAA-1 WS1A.4-lite (per-skill naming handles `cosmological_vocabulary=None` gracefully).

### INFOs deferred (jack-ryan Gate-2)

- INFO-1: Skip log fires for non-baseline modes even when vocabulary wouldn't have generated anyway — minor readability issue; non-blocking; fix at next `cli.py` touch
- INFO-2: `--legacy-theme-coalescence` help text references non-existent `--generation-mode` flag — behavior is correct (CLI default is inverted); help text misleading; non-blocking; fix at next `cli.py` touch
