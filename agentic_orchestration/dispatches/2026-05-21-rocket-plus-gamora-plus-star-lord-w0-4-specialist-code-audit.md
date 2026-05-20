# Dispatch — 2026-05-21 — rocket + gamora + star-lord — W0.4: Phase 2 specialist code-side constraint audit

**From:** knight-rider
**To:** rocket (generation seam) + gamora (simulation seam) + star-lord (telemetry/export seam); jack-ryan reviews
**Approved by:** gandalf attestation 2026-05-21 § 5 (six autonomous workstreams cleared); per activation dispatch § 4 Step 4 W0.4
**Status:** PENDING — ACTIVE (specialists may execute when launched; coordinate via this dispatch's shared completion record)
**Estimated effort:** ~1-2 weeks (substantial; broadest-scope P0 workstream; 3 specialists in parallel)
**Acceptance:** Per-seam constraint inventory with file:line citations; 12 HIGH-risk LCs each verified; 18 MEDIUM-risk LCs follow-up; § 2.8 W1.13 current-state verified; Alt A OQ-2 + OQ-3 verified; tag `qd-rebuild/v0.4-code-side-audit-N` per seam.

---

## Context

Jack-ryan's legacy-constraint audit (62 LCs; 12 HIGH-risk) was Phase 1 (DESIGN-MODE; documentation-level inventory). This W0.4 dispatch is **Phase 2 — code-side specialist verification**: each seam's specialist confirms the LC's code-level state, surfaces drift between documented disposition and actual code, and produces a file:line-cited per-seam inventory that knight-rider folds into the QD-rebuild's running constraint-removal record.

This dispatch is broadest-scope in P0 and informs all downstream work. It also folds in two NEW verification items from the activation dispatch:
- **§ 2.8 W1.13 current-state verification**: confirm whether skill-tree-node-population infrastructure exists in any nascent form (Matt: "fairly sure" gap exists; this is bullet-proof confirmation before W1.13 fires in P1)
- **Alt A OQ-2** (lightning chain_lightning boss multi-hop) + **OQ-3** (5-skill kit generation anomaly): verify code-side surfaces

## Per-seam scope

### rocket (generation seam)

**HIGH-risk LCs to verify code-side:** LC-001 (archetype templates dict — file:line per `b6_archetype_templates.py:99-465`), LC-002 (fire selection bias — `element/selector.py`), LC-006 (canonical-four LLM exposure — `llm/naming.py`, `element/selector.py`, `canonical/library_generator.py`), LC-007 (humanoid gear schema — `generation/gear_schema.py:198-310`), LC-008 (STR/DEX/INT math labels — `generation/gear_schema.py` + `can_equip()`), LC-012 (foundation validator — `foundation/foundation.py:39-43`)

**§ 2.8 W1.13 current-state verification:**
- Inspect `b6_kit_builder.py` + `class_generator.py` + `b6_archetype_templates.py` for any existing skill-tree-node structure (likely NOT present per Matt; confirm)
- If any partial structure exists, document its shape (would inform W1.13 design)
- If fully absent (expected), document the architectural starting point for W1.13

**Alt A OQ-2 + OQ-3 verification:**
- OQ-2: trace lightning `chain_lightning` skill — does it support boss multi-hop, or is it bin-limited? File:line cite + behavior summary
- OQ-3: 5-skill kit generation anomaly — Alt A surfaced this as a kit-construction edge case; trace `b6_kit_builder.py` for the 5-skill vs N-skill kit size logic

### gamora (simulation seam)

**HIGH-risk LCs to verify code-side:** LC-003 (modifier floor — `simulation/balance_loop.py` per recompose-hive state; verify Option A `MODIFIER_SEARCH_FLOOR=0.01` active + Option B soft-disabled `LEVER_FLOOR_LOCK_WORKING_MODIFIER=MODIFIER_SEARCH_FLOOR`), LC-004 (energy-type gradient — derived in simulation mechanics; verify ARMOR_MITIGATION_K + rage_startup), LC-005 (PackProxy ×8 — `simulation/combatant.py`; **note: this is the migration target of W0.9 — verify current state as baseline for W0.9 migration**), LC-009 (hunter modifier range — `tests/` for hunter-specific tests; balance_loop interactions), LC-010 (sim is solo-only — `simulation/` no ally-AI; baseline for P4 W4.1), LC-011 (controller/mage iteration overhead — `simulation/balance_loop.py` convergence iteration patterns)

**Alt A OQ-2 + OQ-3 verification (sim side):**
- OQ-2: simulation behavior of chain_lightning during boss fights — does the multi-hop terminate prematurely? File:line cite
- OQ-3: simulation behavior under 5-skill kit — any edge cases?

### star-lord (telemetry/export seam)

**HIGH-risk LCs to verify code-side:** check whether telemetry/export carries any of the HIGH-risk LCs in its consumption pattern (e.g., LC-006 canonical-four label exposure may surface in export packets; LC-007 humanoid gear schema in export). Cross-check schema versions v2.12 + v2.13 against jack-ryan's LC list

**§ 2.8 W1.13 telemetry implications:**
- Does current schema accommodate node-subset + per-node-coefficients (per § 2.8 ArchiveEntry spec)? If not, surface as P1 W1.X schema-extension scoping input

### jack-ryan reviews

Per critique-pair pattern (activation dispatch § 4.2): jack-ryan reviews the per-seam findings for cross-seam coherence and drift between documented audit (Phase 1 DESIGN-MODE) and code-side state (Phase 2 specialist verification). Jack-ryan may surface new LCs not in the original 62 (per protocol § 7.4 emergency protocols: "new HIGH-risk LCs surface in P0 W0.4 that block phase completion" is an explicit halt-and-notify trigger).

## Coordination

This is a multi-seam dispatch. Coordinate via the shared completion record at the bottom. Per-seam findings filed independently in respective AGENT_STATE.md + a shared deliverable at `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/phase-2-code-side-verification.md` (or equivalent location).

**Per-seam tags:**
- `rocket/v1.X-w0-4-code-side-audit` (rocket; next version after current)
- `gamora/v1.X-w0-4-code-side-audit` (gamora)
- `star-lord/v1.X-w0-4-code-side-audit` (star-lord)

**Hive tag (after all 3 seams complete + jack-ryan reviews):** `qd-rebuild/v0.4-code-side-audit-complete`

## Required reading before starting

- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (full inventory; your seam's HIGH + MEDIUM LCs)
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.8 (W1.13 architecture) + § 2.9 (W0.9 gauntlet) — for verification context
- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/spot-check-regen-findings.md` (Alt A; OQ-2 + OQ-3 origins)
- `canonical/story/substrate-design-supplement-2026-05-21.md` (substrate-as-cohesion-only — operative for LC reinterpretation)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 3.1 (LC synthesis)
- Per-seam AGENT_STATE.md (your current state)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11.1 (state-space conditioning — apply to telemetry inspection)

## Math-before-code (if applicable)

Not applicable to verification work; the dispatch is INSPECTION not implementation. If verification surfaces an LC needs an implementation-side fix (not yet in scope of this dispatch), surface to knight-rider for follow-on workstream scoping.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — Phase 2 verification dispatch only; no field add/modify/rename/remove. Any downstream fix dispatch carries its own round-trip clause.**

## Scope (per seam)

- [ ] 12 HIGH-risk LCs verified per your seam's scope (file:line cites + drift status)
- [ ] 18 MEDIUM-risk LCs follow-up (lighter — file:line cite + 1-sentence verdict per LC)
- [ ] § 2.8 W1.13 current-state verified (rocket primary; star-lord schema implications)
- [ ] Alt A OQ-2 + OQ-3 verified (rocket generation-side + gamora sim-side)
- [ ] Per-seam deliverable at `<seam>/research/qd-rebuild-w0-4-<seam>-code-side-audit.md` OR appended to AGENT_STATE.md (your choice)
- [ ] Shared deliverable at `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/phase-2-code-side-verification.md` (consolidated)
- [ ] Seam tag fired
- [ ] AGENT_STATE.md updated

## Acceptance criteria (per seam)

- [ ] Each HIGH-risk LC for your seam: file:line cite + verdict (VERIFIED / RESOLVED / DRIFT-FROM-AUDIT / NEEDS-DOWNSTREAM-FIX)
- [ ] § 2.8 W1.13 current-state findings actionable for W1.13 design
- [ ] OQ-2 + OQ-3 findings file:line-cited
- [ ] Cross-seam impact noted (per ADR-004; surfaces if your verification reveals cross-seam contract gap)
- [ ] Round-trip: not applicable — verification workstream; no contract change

## Out of scope

- Implementing any LC fix (this is verification; fixes are downstream workstreams)
- Re-litigating LC dispositions (jack-ryan Phase 1 audit dispositions are LIVE; this dispatch verifies code-side, not re-judges design)
- Broader code refactoring (focus on LC verification scope only)
- Authoring NEW canonical docs (capture findings in research files)

## Open questions for the agent to resolve

- **If a HIGH-risk LC's code-side state is DRIFT-FROM-AUDIT** (e.g., already resolved by some intermediate work; or worse than audit describes): surface to knight-rider. Don't silently update jack-ryan's audit — preserve audit-trail.
- **If you discover a NEW HIGH-risk LC** during inspection: stop, surface to knight-rider + jack-ryan. Per protocol § 7.4, new HIGH-risk LCs in P0 W0.4 can block phase completion — this is an explicit halt-and-notify trigger.
- **If OQ-2 / OQ-3 surfaces an actual bug** (not just an edge-case behavior to document): math-before-code per Discipline #1, then surface to knight-rider for separate fix dispatch.

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 4 Step 4 W0.4 + § 2.8 + § 2.9
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.4 + § 6.1.3 (critique-pair structure) + § 7.4 (emergency protocols)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (62 LCs full)
- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/` (Alt A deliverables; OQ-2 + OQ-3)
- `canonical/story/substrate-design-supplement-2026-05-21.md` (substrate-as-cohesion-only architecture; informs LC reinterpretation under new architecture)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11.1 (state-space conditioning; apply to telemetry/code inspection)

---

## Completion Record

### Star-lord section — COMPLETE 2026-05-21

**Tag:** `star-lord/v1.15-w0-4-code-side-audit-1`
**Deliverable:** `agentic_orchestration/star-lord/research/qd-rebuild-w0-4-star-lord-code-side-audit.md`

**LC verdicts (star-lord seam):**
- LC-006: RESOLVED (cipher migration live in `llm/naming.py`; test-guarded)
- LC-007: VERIFIED (humanoid slot names confirmed in export schema; migration not yet shipped as expected)
- LC-003: DRIFT-FROM-AUDIT — `floor_lock_recompose`, `working_modifier`, `floor_lock_detected` absent from telemetry schema + recorder; gamora spec is ahead of star-lord implementation
- LC-008: NEEDS-DOWNSTREAM-FIX — `naming.py:323` exposes raw `stats.as_dict()` in name_class LLM prompt

**W1.13:** No ArchiveEntry fields exist in star-lord seam. New `archive_entries` table required for P1.
**W0.8:** `bounce_count` + `spawn_count` additive scope scoped; 4 files, ~20 lines, Matt auth required for SQL.
**Schema v2.12 + v2.13:** Both LIVE. No drift.
**New HIGH-risk LC discovered:** None (no phase-halt triggered).
**Open items for knight-rider:** (1) P1 dispatch for `floor_lock_*` telemetry columns before gamora Option B ships; (2) star-lord as W0.9 stakeholder for fight-context discriminator column when PackProxy is retired.

### Rocket section — COMPLETE 2026-05-21

**Tag:** `rocket/v1.23-w0-4-code-side-audit-1`
**Deliverable:** `agentic_orchestration/rocket/research/qd-rebuild-w0-4-rocket-code-side-audit.md`

**LC verdicts (rocket seam):**
- LC-001: DRIFT-FROM-AUDIT (positive) — D3 Path-a composition live; 23 templates at boot; hardcoded-14 replaced; physical (5 templates) hardcoded by design
- LC-002: VERIFIED — fire allow-list 20 vs wind 7 (2× weight imbalance); ELEMENT_AFFINITY.fire=[wind,earth] secondary-slot contamination as structural presupposition; ablation needed per Discipline #13b
- LC-006: SUBSTANTIALLY-RESOLVED — system prompt clean; `_build_prompt()` `fire_slot`/`wind_slot` example keys present but architecturally acceptable per W0.6; test coverage gap for `_build_prompt()` user prompt outstanding (W0.6 action item)
- LC-007: VERIFIED — humanoid gear schema confirmed as-documented; 4-slot Loadout; medieval BASE_ITEMS in gear_catalog.py; deferred P4 W4.1
- LC-008: NEEDS-DOWNSTREAM-FIX — star-lord `naming.py:323` is actionable site; rocket-side `can_equip()` str/dex/int are math-bearing abbreviations, not LLM-visible
- LC-012: RESOLVED — W0.3 commit `3e428ae`; no drift

**W0.2 prerequisite:** LC-001 structural inventory captured — ArchetypeTemplate field set, role×substrate matrix, BC-target implicit assumptions, physical template constraints. W0.2 math-before-code can consume this directly.

**W1.13:** Skill-tree-node infrastructure FULLY ABSENT. W1.13 builds NEW generation-side infrastructure (node_subset + per_node_coefficients in class output schema).

**OQ-2:** chain_lightning receives full geometric-series multiplier on boss in solo-sim (~2.76×). NOT bin-limited. Solo-sim over-estimates vs multi-target. `damage_resolver.py:325-337`.

**OQ-3:** No 5-skill floor in code. kit_min=10 for all current templates. 5-skill anomaly not reproducible from current code. `b6_kit_builder.py:312-346`.

**Positive MEDIUM-LC drifts:** LC-022 (D3 generates lightning/holy/shadow — 11 new tags live); LC-026 (mana bug RESOLVED in combatant.py:362-375).

**New HIGH-risk LC discovered:** None. No phase-halt triggered.

**Open items for knight-rider:**
1. LC-006 test coverage: Add `_build_prompt()` user prompt assertion to `tests/test_no_canonical_four_in_llm_prompts.py` (non-blocking; W0.6 action item)
2. LC-001 tag expansion awareness: D3 added 11 new archetype tags; telemetry queries enumerating hardcoded tags need updating (gamora/star-lord seam awareness; no MIGRATION.md filed)
3. W0.2 is next substantial rocket workstream

### Gamora section — PENDING

### Jack-ryan review — PENDING (after all 3 seams complete)
