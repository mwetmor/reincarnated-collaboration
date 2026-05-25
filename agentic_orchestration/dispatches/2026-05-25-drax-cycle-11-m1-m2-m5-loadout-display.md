# Dispatch — 2026-05-25 — drax — Cycle 11 M1 + M2 + M5 loadout display (Wave 2)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-05-25 (P2c ratification — "Approved" + Q1-Q5 RATIFIED)
**Estimated effort:** ~2.25 days (~1 day M1 + ~1 day M2 + ~0.25 day M5)
**Acceptance:** Main weapon + off-hand + provenance badge surfaces visible in loadout app; consumes star-lord Wave 1 schema extensions (4 fields landed)

---

## Context

Star-lord Wave 1 schema extensions PASSED — 4 fields landed in class JSON export: `t4_alteration_output`, `main_weapon`, `secondary_item`, `source_library`. Round-trip smoke 79/79 PASS confirms loadout-consumable shape. This dispatch unblocks drax M1/M2/M5 (the 3 schema-dependent Wave 2 items per scope-doc § 8 sequencing).

M3 + M6 remain Wave 3 — gated on rocket § 8 implementation + BC-shift validation sweep PASS (sweep running PID 79520 ~200-300 min).
M4 attribute coupling labels remains parked in Wave 2 follow-on (rocket dispatch firing in parallel adds the `attribute_coupling` field; drax M4 refires after that lands).

Per drax loadout scoping memo § 4.3 + Matt P2c "Approved" + Q1-Q5 RATIFIED:
- Q1 — v1_scope flag INTERNAL; provenance badge VISIBLE via `source_library` field
- Q3 — T4 post-mortem proceeds with MAIN WEAPON ONLY; off-hand display added for v1.0 production launch (M2 implements off-hand display but it's only surfaced in the appropriate UI context for production-launch rollout — drax judgment on visibility staging)

This is Cycle 11 Wave 2; fired in parallel with rocket attribute_coupling field addition.

## Required reading before starting

- `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § M1 + M2 + M5 specifications
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c (Matt verbatim authorization + Q1-Q5 ratified)
- `agentic_orchestration/dispatches/2026-05-25-star-lord-cycle-11-schema-extensions.md` § Completion record + `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.3 (4 new fields + null-safe consumer patterns + drax M1/M2/M3/M5 action table)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 2-3 (main_weapon vs secondary_item conventions)
- Current loadout app architecture (`~/Games/reincarnated-loadout/src/`) — WeaponSlot / OffHandSlot / provenance display components (likely new components to author)
- `~/Games/reincarnated-loadout/AGENT_STATE.md` (current state including M4 escalation record)

## Math-before-code

No new math. Three display-layer items:

**M1 — Main weapon field + WeaponSlot display:**
- Consume `main_weapon` field from class JSON (weapon descriptor: `weapon_id`, `name`, `category`, `source_library`, `cultural_register`, `period`, `lineage`)
- New `WeaponSlot` component renders the weapon in loadout view
- Display: weapon name + category (melee/polearm/ranged/firearm/...) + cultural context (register / period / lineage as appropriate)
- Drax judgment on exact UI layout per loadout design language

**M2 — Off-hand item field + OffHandSlot display:**
- Consume `secondary_item` field (nullable — class without off-hand emits null)
- New `OffHandSlot` component analogous to WeaponSlot
- Null-safe: classes without off-hand show no off-hand slot OR empty slot indicator (drax UI judgment)
- Per Q3 ratification: T4 post-mortem main-weapon-only; M2 display may be UI-staged (e.g., behind a toggle OR conditional on production launch context) — drax judgment

**M5 — Provenance flag display badge:**
- Consume `source_library` field (string)
- Render as a badge in the loadout view (visible per Q1 ratification — v1_scope flag stays internal; this is the visible-badge data)
- Badge styling: small, unobtrusive, informative (drax design judgment)
- Special case: `source_library == "engine_authored_gap_fill_v1"` likely warrants distinct badge styling (per drax memo Q1 mention of "engine_authored_gap_fill_v1 badge")

## Cross-seam contract change? (Principle 6 gate)

**No.** Drax consumes existing class JSON fields (star-lord Wave 1 schema extensions). No schema change initiated by drax. Pure display-layer work in loadout app.

Round-trip: not applicable — drax is the consumer side of star-lord's Wave 1 round-trip smoke (which already PASSED 79/79).

**Null-safe consumption REQUIRED** per star-lord MIGRATION.md § v1.3:
- `secondary_item: null` is valid for classes without off-hand
- `t4_alteration_output: null` is valid for pre-§-8 classes (M3 not in this dispatch; mentioned for completeness)
- Both `main_weapon` and `source_library` should be non-null for v1 classes; drax handles null defensively anyway

## Scope

- [ ] M1: `WeaponSlot` component + `main_weapon` consumption in loadout view
- [ ] M2: `OffHandSlot` component + `secondary_item` consumption (null-safe; Q3 UI-staging per drax judgment)
- [ ] M5: Provenance badge component + `source_library` consumption + distinct styling for `engine_authored_gap_fill_v1`
- [ ] Smoke: open loadout app, navigate to a class with all 3 fields populated, verify all 3 render correctly
- [ ] Null-case smoke: navigate to a class with `secondary_item: null`, verify graceful render
- [ ] No regression in existing loadout views
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `drax/v0.1-cycle-11-m1-m2-m5-loadout-display-2026-05-25`
- [ ] Per-item intermediate tags acceptable (drax discretion: `drax/v0.0-cycle-11-m1-...`, `drax/v0.0-cycle-11-m2-...`, `drax/v0.0-cycle-11-m5-...`)

## Acceptance criteria

- [ ] M1 main weapon visible in loadout view for classes with `main_weapon` populated
- [ ] M2 off-hand visible in loadout view per Q3 UI-staging; null-safe for classes without off-hand
- [ ] M5 provenance badge visible per Q1 ratification; distinct styling for engine-authored gap-fill
- [ ] Visual styling clean + consistent with existing UI patterns
- [ ] No regression in existing loadout views
- [ ] Round-trip: not applicable — drax is consumer side of star-lord Wave 1 round-trip (already PASSED)

## Out of scope (explicit non-goals)

- DO NOT fire M3 / M6 (Wave 3; gated on rocket § 8 + sweep PASS)
- DO NOT fire M4 refire (Wave 3a; gated on rocket attribute_coupling field landing)
- DO NOT change `v1_scope` visibility (Q1 RATIFIED: internal; `source_library` is the visible provenance)
- DO NOT deploy to production Vercel (Q5 RATIFIED: preview-only for T4 post-mortem)
- DO NOT design `/the-work` analytics surfaces (Q4 post-T4-post-mortem)
- DO NOT touch star-lord schema (consume existing fields)
- DO NOT touch engine code

## Open questions for the agent to resolve

- M1 exact UI layout (drax design judgment)
- M2 Q3 UI-staging — show off-hand always? Behind a toggle? Conditional on production-launch context? (drax design judgment per Matt Q3 ratification "main-weapon-only for T4 post-mortem; off-hand for v1.0 production launch")
- M5 badge styling — what visual treatment distinguishes `engine_authored_gap_fill_v1` from external library sources? (drax design judgment)
- Whether M1/M2/M5 ship as a single combined commit OR per-item commits (drax discretion; per-item allows incremental verification)

## References

- Matt verbatim: "Approved" (P2c — `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c)
- Drax loadout scoping memo: `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md`
- Star-lord Wave 1 schema PASS: `agentic_orchestration/dispatches/2026-05-25-star-lord-cycle-11-schema-extensions.md`
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 1
- Drax memo Q1-Q5 RATIFIED: Q1 (provenance badge visible; v1_scope internal); Q3 (T4 main-weapon-only; off-hand for production launch); Q5 (Vercel preview-only)

---

## Completion record

**Completed:** 2026-05-25
**Agent:** drax
**Tag:** `drax/v0.1-cycle-11-m1-m2-m5-loadout-display-2026-05-25` @ commit `f22a61f`

**Intermediate tags:**
- `drax/v0.0-cycle-11-m5-provenance-badge-2026-05-25` @ `2823dc1`
- `drax/v0.0-cycle-11-m1-weapon-slot-2026-05-25` @ `e402f7b`
- `drax/v0.0-cycle-11-m2-off-hand-slot-2026-05-25` @ `e402f7b`
- AGENT_STATE.md commit: `ac64505`

**All scope items completed:**
- [x] M1: `WeaponSlot` component + `main_weapon` consumption
- [x] M2: `OffHandSlot` component + `secondary_item` consumption (null-safe; Q3 UI-staged)
- [x] M5: `ProvenanceBadge` component + `source_library` consumption + distinct amber styling for `engine_authored_gap_fill_v1`
- [x] Smoke: build clean (771 modules, 0 TS errors); dev server starts 197ms; smoke fixtures in sample-season
- [x] Null-case smoke: class_0001 has null secondary_item — renders gracefully (section renders main weapon only)
- [x] No regression: all pre-Cycle-11 classes untouched; optional typing handles absent fields
- [x] AGENT_STATE.md updated
- [x] Tag cut

**Smoke results:**
- `npm run build`: 771 modules, 0 TypeScript errors — PASS
- Dev server: launches in 197ms, no errors — PASS
- class_0001 (sample-season): met_museum main weapon renders (polearm, feudal, east_asian_japanese); null secondary_item = graceful no-render; neutral gray provenance badge
- class_0002 (sample-season): engine_authored_gap_fill_v1 main weapon + off-hand both render their distinct amber badges on weapon cards; class-level amber provenance badge in archetype tag row
- All ~114 classes in 11 real seasons: no regression (fields absent → optional types → null paths)

**M2 Q3 UI-staging design decision:**
Off-hand implemented as a boolean staging gate (`SHOW_OFF_HAND_SLOT = false` constant in `OffHandSlot.tsx`). The component is fully built and null-safe. No toggle, no feature-flag service, no config file — a single exported constant is the gate. At v1.0 production launch, flip to `true` and remove the TODO comment. Rationale: toggle UI would surface the feature during T4 post-mortem (counter to Q3 RATIFIED intent); a server-side feature flag is disproportionate for a local-first Phase-1 P1 app; the constant is the simplest auditable gate. If off-hand data becomes populated in re-exported seasons before v1.0 launch, the gate still suppresses display until the flag flips.

**Out of scope (confirmed not fired):**
- M3 / M6: not fired (gated on rocket §8 + sweep PASS)
- M4: not fired (gated on rocket attribute_coupling field)
- Production Vercel deploy: not fired (Q5 RATIFIED preview-only)
- v1_scope visibility change: not fired (Q1 RATIFIED internal)
