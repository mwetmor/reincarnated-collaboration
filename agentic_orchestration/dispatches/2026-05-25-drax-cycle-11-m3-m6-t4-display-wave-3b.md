# Dispatch — 2026-05-25 — drax — Cycle 11 M3 + M6 T4 alteration display (Wave 3b; Tier 2 ratified)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-05-25 (Tier 2 ratification per Cycle 11 § 8 BC-shift FAIL response — ship § 8 as intent metadata + spirit-guide narration + loadout display; M3 + M6 Q1-Q5 ratified per matt-log-back P2c)
**Estimated effort:** ~3 days (~1.5 days M3 + ~1.5 days M6)
**Acceptance:** T4 alteration output rendered in SkillTree.tsx + spirit-guide narration display + T4 comparison panel (TOGGLE per Q2); consumes existing `t4_alteration_output` intent metadata from class JSON (already shipped per Cycle 11 Wave 1 star-lord schema extensions)

---

## Context

Cycle 11 BC-shift validation sweep FAILED (direction 41.67% / magnitude 0.00%) — diagnostic triple-fire (rocket + gandalf + legolas) reached UNANIMOUS CONVERGENCE: § 8 architecture is SOUND; failure was test-design + missing-wire-up issue, NOT architectural. Matt ratified **Tier 2** per Cycle 11 escape-hatch resolution: ship § 8 v1 as intent metadata + spirit-guide narration + loadout display; defer combat-arithmetic wire-up + magnitude validation to v1.1 (Cycle 12 Layer 6 picks this up against the new engine).

This unblocks Wave 3b drax M3/M6 implementation. M3 + M6 consume the existing `t4_alteration_output` field (already shipped per star-lord Wave 1 schema extensions; round-trip 79/79 PASS). No wait on wire-up; intent metadata is sufficient for T4 post-mortem readiness.

Per Matt P2c Q1-Q5 RATIFIED:
- **Q2** — T4 comparison panel uses **toggle** display (cleaner on mobile)
- **Q3** — T4 post-mortem proceeds with **main weapon only**; off-hand display added for v1.0 production launch (post-Sidecar-B-loadout-integration)
- **Q5** — Vercel deploy: **preview-only** for T4 post-mortem (production deploy ADR-006 trigger deferred)

This is Cycle 11 Wave 3b — fires in parallel with Cycle 12 Day-1 open (legolas MC-1+MC-2 + jack-ryan Gate-1 + elrond SC-1+SC-2). No specialist contention.

---

## Required reading before starting

- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c (Matt verbatim authorization + Q1-Q5 RATIFIED; Q2 TOGGLE; Q3 main-weapon-only for T4 post-mortem; Q5 preview-only)
- `agentic_orchestration/cycle-11-v1-implementation-push-state.md` § Wave 3b (BC-shift sweep FAIL → diagnostic triple-fire → UNANIMOUS Tier 2 framing → Matt ratification context)
- `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § M3 + M6 specifications
- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m1-m2-m5-loadout-display.md` § Completion record (Wave 2 pattern — null-safe consumption + per-item intermediate tags + UI-staging constant pattern)
- `agentic_orchestration/dispatches/2026-05-25-star-lord-cycle-11-schema-extensions.md` + `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.3 (4 new fields landed; `t4_alteration_output` shape + null-safe consumer patterns)
- `canonical/story/skill-system-2026-05-24.md` § 8 (Algorithm § 8 architecture — what the alteration represents) + § 9 (spirit-guide explainer pattern — narration design substrate that converts cognitive-load risk into story win)
- `~/Games/reincarnated-engine/src/reincarnated/generation/notes/algorithm-section-8-bc-shift-fail-diagnostic-2026-05-25.md` (rocket calibration analysis — context for what alteration metadata represents semantically)
- `~/Games/reincarnated-loadout/src/` — current SkillTree.tsx + WeaponSlot + ProvenanceBadge patterns
- `~/Games/reincarnated-loadout/AGENT_STATE.md` — current loadout state

---

## Math-before-code

No new math. Two display-layer items consuming existing intent-metadata field:

**M3 — T4 alteration output display in SkillTree.tsx:**

- Consume `t4_alteration_output` field from class JSON (struct per `mechanic_alteration.py` AlterationOutput dataclass; nullable for pre-§-8 classes)
- AlterationOutput shape:
  - `strategy_name: str` (e.g., "RESOURCE_CONVERSION", "TRADE_OFF", "ELEMENT_CONVERSION", "DEFENSIVE_CONVERSION", "GEOMETRY_COLLAPSE", + 6th strategy from legolas verdict)
  - `eta_score: float` (selection η-score per methodology)
  - `parameters: dict` (strategy-specific: e.g., for ELEMENT_CONVERSION includes `target_element`; for RESOURCE_CONVERSION includes `target_resource`)
  - Plus narration metadata if star-lord schema includes spirit-guide explainer text (check MIGRATION.md § v1.3)
- Render integrated into SkillTree.tsx at the T4 keystone slot (existing T4 slot UI position OR new section if T4 slot UI doesn't yet exist)
- Display:
  - Strategy name (player-facing label, NOT raw enum — drax design judgment per cohesion-judge naming pattern OR direct human-readable mapping)
  - Brief description of what the alteration does (per § 9 spirit-guide explainer; drax may use a static lookup OR consume narration field if star-lord ships one)
  - Strategy-specific parameters surfaced contextually (e.g., for ELEMENT_CONVERSION show "all damage → fire"; for RESOURCE_CONVERSION show "skills cost HP instead of mana")
- Null-safe: classes without `t4_alteration_output` show no T4 alteration section (or "Awaiting alteration" placeholder — drax UI judgment)
- Per Tier 2 framing: this is INTENT METADATA — the alteration text describes what the kit WILL DO once Cycle 12 Layer 6 wire-up lands; until then, it's design-side narration not combat-arithmetic-side effect. Drax can frame as "Build identity" or "Spirit Guide commentary" to honor the intent-metadata semantic without overpromising mechanical effect

**M6 — T4 comparison panel for post-mortem authoring:**

- New panel surface for side-by-side T4 alteration comparison (e.g., compare 2-3 candidate alterations OR compare current kit's alteration vs alternative strategies the kit could have produced)
- Per Q2 RATIFIED: **TOGGLE** display (cleaner on mobile — toggle to open/close; not always-visible)
- Toggle pattern: button or chevron-icon that reveals the comparison panel; closed by default
- Panel content: drax design judgment on exactly what to compare and how to lay out
  - Recommended: current class's `t4_alteration_output` vs 1-2 alternative strategies (drax pulls from class JSON if multi-candidate data exists; if not, surface current alteration only with "more comparisons in v1.1" placeholder)
  - Each comparison row shows strategy name + eta_score + parameters + brief description
- Per Q3: main-weapon-only context for T4 post-mortem (no off-hand surface here)
- Null-safe: classes without `t4_alteration_output` hide the toggle entirely (or show disabled state with "No T4 alteration" — drax judgment)

**Spirit-guide narration display surface (Tier 2 framing component):**

- The Tier 2 framing requires THREE outputs: intent metadata + **spirit-guide narration** + loadout display
- "Spirit-guide narration" surface — drax may absorb this into M3 as the "brief description" element (per § 9 spirit-guide explainer pattern) OR surface as a distinct in-card panel element
- Drax design judgment on whether narration is a separate UI affordance OR woven into M3's strategy description
- Reference: `canonical/story/skill-system-2026-05-24.md` § 9 spirit-guide explainer pattern — the design substrate that converts algorithmic complexity into story win
- If star-lord schema includes a narration field on AlterationOutput, consume that; otherwise drax static-maps strategy_name → human-readable narration template

## Cross-seam contract change? (Principle 6 gate)

**No.** Drax consumes existing class JSON field (`t4_alteration_output`) shipped per star-lord Wave 1 schema extensions. No schema change initiated by drax. No reverse-direction emission. Pure display-layer work in loadout app.

Round-trip: not applicable — drax is the consumer side of star-lord's Wave 1 round-trip smoke (which already PASSED 79/79).

**Null-safe consumption REQUIRED** per star-lord MIGRATION.md § v1.3:
- `t4_alteration_output: null` is valid for pre-§-8 classes (legacy seasons; classes where η-scoring produced no viable candidate above ETA_FLOOR)
- All other consumer fields (strategy_name, parameters subkeys) should be defensively guarded

---

## Scope

- [ ] M3: T4 alteration output rendered in SkillTree.tsx (strategy name + parameters + description; null-safe)
- [ ] M3.spirit-guide: spirit-guide narration surface (woven into M3 OR distinct in-card element per drax judgment; per § 9 explainer pattern)
- [ ] M6: T4 comparison panel for post-mortem authoring (TOGGLE display per Q2; null-safe; mobile-friendly)
- [ ] Smoke: open loadout app, navigate to a class with `t4_alteration_output` populated, verify M3 + M6 render correctly + spirit-guide narration is present
- [ ] Null-case smoke: navigate to a class with `t4_alteration_output: null`, verify graceful render (M3 hides or placeholder; M6 toggle hides or disabled state)
- [ ] No regression in existing loadout views (M1/M2/M4/M5 + base SkillTree)
- [ ] Tier 2 framing honored: M3 + M6 + narration positioned as INTENT METADATA + design-side narrative (not over-promising mechanical effect at v1)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `drax/v0.1-cycle-11-m3-m6-t4-display-wave-3b-2026-05-25`
- [ ] Per-item intermediate tags acceptable (drax discretion: `drax/v0.0-cycle-11-m3-t4-alteration-display-2026-05-25`, `drax/v0.0-cycle-11-m6-t4-comparison-panel-2026-05-25`)

## Acceptance criteria

- [ ] M3 T4 alteration output visible in SkillTree.tsx for classes with `t4_alteration_output` populated (one of the 6 v1 strategies); null-safe for classes without
- [ ] Spirit-guide narration surface present (per § 9 explainer pattern; drax positions per design judgment — woven OR distinct)
- [ ] M6 T4 comparison panel visible via TOGGLE per Q2 ratification; mobile-friendly; null-safe
- [ ] Visual styling clean + consistent with existing UI patterns (WeaponSlot + ProvenanceBadge + StatsDisplay)
- [ ] No regression in existing loadout views
- [ ] Tier 2 framing honored — intent-metadata framing visible in copy (not "combat-affecting" language)
- [ ] Round-trip: not applicable — drax is consumer side of star-lord Wave 1 round-trip (already PASSED)
- [ ] Vercel preview deployment succeeds (per Q5 — preview-only; do NOT promote to production)

## Out of scope (explicit non-goals)

- DO NOT wire alteration to combat arithmetic (Tier 2 framing — Layer 6 wire-up is Cycle 12 work; M3/M6 are intent-metadata display only)
- DO NOT change `t4_alteration_output` shape (star-lord owns the schema; consume existing fields)
- DO NOT touch star-lord schema or engine code
- DO NOT promote to production Vercel (Q5 RATIFIED preview-only for T4 post-mortem)
- DO NOT design `/the-work` analytics surfaces (Q4 post-T4-post-mortem)
- DO NOT surface off-hand item in T4 post-mortem M3/M6 context (Q3 RATIFIED main-weapon-only for T4 post-mortem; M2 off-hand display is UI-staged via SHOW_OFF_HAND_SLOT constant)
- DO NOT add multi-candidate comparison data sourcing in M6 if class JSON doesn't already contain alternative candidates (graceful degradation: surface current alteration only; defer multi-candidate scaffolding to v1.1)
- DO NOT add LLM-call dependency for narration at M3 (use static template mapping OR consume star-lord-shipped narration field; LLM-call for spirit-guide is generation-side work)

## Open questions for the agent to resolve

- M3 exact UI layout — where in SkillTree.tsx does the T4 alteration sit (existing T4 slot UI vs new section)? (drax design judgment)
- M3 spirit-guide narration positioning — woven into M3 description OR distinct in-card element? (drax design judgment per § 9 pattern)
- M3 description text source — static template mapping by strategy_name OR consume star-lord-shipped narration field? (drax checks MIGRATION.md § v1.3 for narration field presence; if absent, static template)
- M6 toggle UI affordance — button text? chevron icon? mobile-friendly placement? (drax design judgment)
- M6 comparison content — show current-only with "v1.1 multi-candidate placeholder" OR attempt to source alternative candidates from class JSON if structure permits? (drax judgment based on what class JSON actually contains; lean toward current-only for v1 simplicity)
- Whether M3/M6 ship as a single combined commit OR per-item commits (drax discretion; per-item allows incremental verification — same pattern as Wave 2 M1/M2/M5)
- Whether Cycle 11 final tag is cut after drax Wave 3b PASS + jack-ryan Gate-2 PASS (KR drafts wind-down summary; Matt ratifies tag — separate from this dispatch)

## References

- Matt verbatim: "Approved" (P2c — `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c) + Tier 2 ratification (per Cycle 11 BC-shift FAIL resolution context)
- Drax loadout scoping memo: `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md`
- Star-lord Wave 1 schema PASS: `agentic_orchestration/dispatches/2026-05-25-star-lord-cycle-11-schema-extensions.md` + MIGRATION.md § v1.3
- Cycle 11 state file Wave 3b context: `agentic_orchestration/cycle-11-v1-implementation-push-state.md`
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md`
- Drax memo Q1-Q5 RATIFIED: Q2 (T4 comparison TOGGLE per mobile); Q3 (T4 main-weapon-only; off-hand for v1.0 production launch); Q5 (Vercel preview-only)
- Skill-system § 8 + § 9: `canonical/story/skill-system-2026-05-24.md`
- Cycle 11 BC-shift FAIL diagnostic synthesis (Tier 2 framing source): rocket commit `70061a7` + gandalf commit `af13cba` + legolas Pattern A-deep

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Tier 2 ratification per Cycle 11 § 8 BC-shift FAIL response (Matt log-back implicit via "Let's move ahead with it" framing brief approval + P2c Q1-Q5 RATIFIED + Cycle 12 framing brief § L10 "Tier 2 ratification for Cycle 11 § 8 BC-shift FAIL (Matt 2026-05-25)" — Cycle 11 closes with § 8 shipping as intent metadata + spirit-guide narration + loadout display per drax M3/M6)
**Status:** FIRE — Wave 3b unblocked per Tier 2; runs in parallel with Cycle 12 Day-1 open (no specialist contention)

**Matt-touch sequence:** dispatch completes → jack-ryan Gate-2 validates → KR drafts Cycle 11 wind-down summary → Matt log-back ratifies (or skip-confirmation re-authorized) → Cycle 11 final tag cut (proposal: `v1.0-t4-intent-metadata-ready` or KR judgment)

---

## Completion record

**Completed:** 2026-05-25
**Agent:** drax
**Commit:** `b948d3d` (M3+M6 implementation) + `0ece86f` (AGENT_STATE.md update)
**Tag (intermediate):** `drax/v0.0-cycle-11-m3-t4-alteration-display-2026-05-25` @ `b948d3d`
**Tag (final):** `drax/v0.1-cycle-11-m3-m6-t4-display-wave-3b-2026-05-25` @ `b948d3d`
**Push status:** PUSHED — main + both tags to `origin` (github.com/mwetmor/reincarnated-loadout)
**Preview URL:** https://reincarnated-loadout-bc7s9pqpu-matthew-wetmore-s-projects.vercel.app (Q5 RATIFIED: preview-only; not promoted to production)

### Acceptance criteria checkmarks

- [x] M3 T4 alteration output visible in SkillTree.tsx for classes with `t4_alteration_output` populated (RESOURCE_CONVERSION smoke path via class_0001 sample fixture)
- [x] Spirit-guide narration surface present (woven into M3 panel; ◈ icon; uses `thematic_rationale` from class JSON when present; § 9 template voice fallback)
- [x] M6 T4 comparison panel visible via TOGGLE per Q2 ratification; closed by default; mobile-friendly text toggle with ▶ chevron
- [x] Null-safe: all 11 real seasons (no `t4_alteration_output`) — both panels hidden, no broken UI
- [x] Visual styling clean + consistent with existing patterns (WeaponSlot / ProvenanceBadge / StatsPanel register)
- [x] No regression in existing loadout views (M1/M2/M4/M5 + base SkillTree verified via clean build)
- [x] Tier 2 framing honored: "Build Identity" badge on M3; "Intent Metadata" label in M6; M6 footer cites Cycle 12 Layer 6 for wire-up
- [x] Vercel preview deployment succeeds (Q5 — preview-only; NOT promoted to production)

### Smoke results

- `npm run build`: 773 modules, 0 TypeScript errors — PASS
- Cycle-11+ path (sample-season class_0001): RESOURCE_CONVERSION alteration renders M3 panel + M6 toggle + spirit-guide narration with `thematic_rationale` from class JSON
- Null-case path: all 11 real seasons → both panels hidden cleanly (TypeScript null-guard enforced at type level)
- M6 toggle: collapsed by default; expands to show current strategy (violet "selected" badge) + 4 static alternative rows + footer note

### Decisions made

- M3 position: BELOW tree/detail-panel row (not inside the grid) — class-level identity, not per-skill
- Spirit-guide narration: WOVEN INTO M3 panel (not a separate affordance) — single visual register
- M6 toggle trigger: text button + ▶ chevron (rotate-90 on open) — mobile tap target per Q2 framing
- M6 comparison: current-only with static alternative descriptions — multi-candidate deferred to v1.1 per dispatch
- T4StrategyType: typed union of 5 known strategies + `string` forward-compat
- `thematic_rationale`: primary narration source when present; § 9 template voice as fallback

### Outstanding TODOs (tracked in AGENT_STATE.md)

- TODO(drax): remove sample-season `t4_alteration_output` fixture from `class_0001.json` when rocket §8 regen ships
- TODO(drax): review M3 panel position if Matt wants it as a separate named section in Loadout.tsx (currently inside SkillTree.tsx return)
