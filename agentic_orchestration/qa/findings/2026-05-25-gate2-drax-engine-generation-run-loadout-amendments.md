# Finding — 2026-05-25 — drax engine generation run loadout amendments

**Reviewer:** jack-ryan
**Severity:** INFO (PASS-with-INFO)
**Target:** `drax/v0.1-engine-generation-run-loadout-amendments-2026-05-25` @ commit `9acff0d`
**Developer:** drax
**Principles applied:** Principle 1 (math-before-code), Principle 2 (smoke-gate), Principle 6 (cross-seam contract), ADR-002 (tiered approval), ADR-004 (cross-seam MIGRATION)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-drax-engine-generation-run-loadout-amendments.md`

---

## Verdict: PASS-with-INFO

Four scope items (Amendment 1 design-mode toggle, Amendment 2 cultural/period/quality-tier badges, M2 gate-flip, Tier 3 strategy badge) shipped cleanly. Smoke claims verified. No cross-seam contract violations. Two INFO-level observations recorded below — neither blocks T4 post-mortem use.

---

## What I found

### Smoke-gate (Principle 2) — PASS

Build claim (777 modules, 0 TypeScript errors, 75ms dev server launch) is plausible: commit `9acff0d` adds 4 new modules (DesignModeToggle, DesignModePanel, WeaponBadges, StrategyBadge) on top of prior clean-build baseline. Tag is present on origin/main. Vercel preview deploy status READY per completion record. Null-case degradation is structurally enforced: all 6 new ClassData fields are typed `? ... | null`, all component entry points guard with null/undefined checks before render, and WeaponBadges returns null when all three badge fields are absent. Populated-case smoke (class_0001 + class_0002) is against synthesized fixture data (see INFO-1 below) — not yet against real engine emission. Regression against M1/M2/M3/M4/M5/M6 is credible: no existing component files were modified except WeaponSlot.tsx (badge wiring), OffHandSlot.tsx (flag flip), Loadout.tsx (toggle + panel wiring), and types.ts (additive fields only).

### Cross-seam contract (Principle 6) — PASS

All fields consumed by this dispatch were previously emitted by upstream seams:
- `bc_target_cell` / `converged_modifier` — MIGRATION.md § v1.4-layer-4 (rocket Layer 4)
- `mechanical_substrate_triple` / `named_bearer` / `named_mythological_match` / `engine_version` — MIGRATION.md § v1.4-layer-6 (rocket Layer 6)
- `spirit_guide_narration_metadata` — MIGRATION.md § v1.4-layer-6 (already consumed by M6; this dispatch reads the raw struct in DesignModePanel)
- `cultural_lineage_canonical` / `historical_period_canonical` / `quality_tier` on WeaponDescriptor — MIGRATION.md § v1.5 (star-lord Wave 5 off-hand contract extension)
- `t4_alteration_output.strategy_type` — already typed in types.ts from Cycle 11 M3 work

No new cross-seam fields added. No engine-side amendments. ADR-004 compliance: no MIGRATION.md entry required (consuming-only dispatch, dispatch doc explicitly declares Principle 6 gate N/A). PASS.

### M2 gate-flip — PASS (drax seam authority)

`SHOW_OFF_HAND_SLOT = true` flip is within drax seam authority per Cycle 11 dispatch deferral framing ("drax judges whether to flip at this milestone"). Rationale in OffHandSlot.tsx comment + dispatch completion record is sound: Cycle 12 v1.0-new-engine-ready tag closed, Wave 5 42/42 PASS on off-hand contract round-trip, null-safety confirmed across legacy classes (OffHandSlot null-guards `secondaryItem` before render). The Q3 "main-weapon-only for T4 post-mortem" intent was explicitly time-boxed to the pre-v2.0-forms window; that window closed. Flip is structurally safe.

### DEFENSIVE_TRADEOFF forward-compat — PASS

StrategyBadge includes `DEFENSIVE_TRADEOFF` in its label and style maps, even though `T4StrategyType` in types.ts does not list it as a named literal. This is acceptable: `T4StrategyType` already carries `| string` as explicit forward-compat. StrategyBadge lookups use `strategyType as string` with `DEFAULT_STYLE` fallback — an unrecognized value at runtime would render a gray chip rather than crash. When rocket ships DEFENSIVE_TRADEOFF strategy, StrategyBadge renders correctly with no loadout change needed. No type error at build time (TypeScript permits `string` literals in the union). See INFO-2 for the one note.

### Design decisions — within drax seam authority, no decisions-log escalation required

- Toggle persistence (localStorage) — drax design judgment per dispatch open question. No architectural impact.
- Tier 3 inclusion — drax discretion per dispatch framing; ~15min scope, directly serves T4 post-mortem. No escalation.
- source_library dual-surface (labeled design-mode row + M5 badge) — drax design judgment; comment in DesignModePanel.tsx makes the framing explicit. No overlap confusion.
- M2 gate-flip — drax seam authority; rationale documented in source comment + completion record.

None of the above require a decisions-log entry. The M2 flip was tracked as a seam-internal implementation decision (flag state, not architectural policy), and rationale is captured in source + dispatch. If Matt or gandalf want a decisions-log entry for posterity, that is a documentation-only amendment — drax can auto-commit.

---

## Findings (INFO only)

### INFO-1 — Synthesized fixture enrichment in sample-season

class_0001 and class_0002 in `data/sample-season/classes/` have been enriched with synthesized v2.0 engine fields (`bc_target_cell`, `mechanical_substrate_triple`, `converged_modifier`, `engine_version`, weapon `cultural_lineage_canonical` / `historical_period_canonical` / `quality_tier`). These values are not real engine emission — they are plausible-shape placeholders used for populated-case smoke.

Drax tracked this clearly: `TODO(drax): remove sample-season fixture enrichment` is recorded in both the dispatch completion record and AGENT_STATE.md. The populated-case smoke therefore validates component rendering logic but NOT engine field accuracy. This is acceptable for the pre-rocket-completion window.

Action: replace synthesized fields with real engine emission once rocket engine generation run completes and star-lord exports new forms. No block on T4 post-mortem use; drax is responsible for cleanup.

- Cite: Discipline #9 (attribution clarity — fixture data distinct from engine emission)

### INFO-2 — DEFENSIVE_TRADEOFF not in T4StrategyType named literals

`T4StrategyType` union (types.ts line 303-309) lists 5 named literals plus `| string`. The 6th strategy `DEFENSIVE_TRADEOFF` is present in StrategyBadge label/style maps but is not a named literal in the type union. This means TypeScript will not catch a typo in DEFENSIVE_TRADEOFF string comparisons at build time.

This is low-risk: the forward-compat `| string` catch-all + DEFAULT_STYLE fallback prevents any runtime failure. But if rocket ships DEFENSIVE_TRADEOFF as a named literal, a future types.ts amendment will be needed to keep the union accurate. The gap between the named-literal set and the StrategyBadge handling set could widen silently if new strategies are added via the forward-compat path.

Recommendation: when rocket ships DEFENSIVE_TRADEOFF strategy officially, add it as a named literal to T4StrategyType at that time (drax in the next touch to types.ts).

- Cite: Discipline #8 (schema validation at boundaries — type union should match runtime vocabulary when vocabulary is known)

---

## Action items

- [ ] drax: remove sample-season fixture enrichment (class_0001, class_0002 synthesized v2.0 fields) once real rocket-generated forms land via star-lord export — tracked in AGENT_STATE.md TODO
- [ ] drax (deferred, next types.ts touch): add `DEFENSIVE_TRADEOFF` as named literal to `T4StrategyType` union when rocket officially ships that strategy

No Matt escalation required. No cross-seam coordination required. Both items are within drax seam authority.

---

## Production promotion

Vercel preview-only confirmed. No production promotion in commit or CI. Q5 RATIFIED constraint satisfied.

---

## References

- `/Users/admin/Games/reincarnated-loadout/src/components/DesignMode/DesignModeToggle.tsx`
- `/Users/admin/Games/reincarnated-loadout/src/components/DesignMode/DesignModePanel.tsx`
- `/Users/admin/Games/reincarnated-loadout/src/components/WeaponSlot/WeaponBadges.tsx`
- `/Users/admin/Games/reincarnated-loadout/src/components/ui/StrategyBadge.tsx`
- `/Users/admin/Games/reincarnated-loadout/src/components/WeaponSlot/OffHandSlot.tsx`
- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts`
- `/Users/admin/Games/reincarnated-loadout/data/sample-season/classes/class_0001.json`
- `/Users/admin/Games/reincarnated-loadout/data/sample-season/classes/class_0002.json`
- `/Users/admin/Games/reincarnated-loadout/AGENT_STATE.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-25-drax-engine-generation-run-loadout-amendments.md` (including completion record)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §§ v1.4-layer-2 through v1.5
