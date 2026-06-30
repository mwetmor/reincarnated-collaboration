# Dispatch — 2026-06-15 — rocket — weapon-as-identity generation build (PHASE 2 of 2)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-14 ("fire phase 2")
**Estimated effort:** multi-day (Pattern B)
**Acceptance:** Phase-2 = the recognition record's HEADLINE gate (§ 4.1) — a weapon-rooted physical kit composes to the legacy physical kit_size band (**10-13 skills**) WITHOUT depending on the sparse physical-cost mechanic pools (`rage`/`focus`/`combo`/`stamina-as-resource`) — PLUS the full § 4 gate re-run. **You do NOT commit the architecture** — you produce the gate result. **A gate FAILURE here is a valid, valuable outcome (the deferral's blocker was real); do NOT suppress it or force a pass.**

## Context

Phase 1 LANDED (commit `7fc25a4`, tag `rocket/v1.2-weapon-as-identity-phase-1`): L1 identity is proxy-rooted (element→scaling-attribute), the pseudo-element smuggle is deleted, the § 1.2 ratio guardrail is a first-class step, and the § 4.4 / § 4.2 / § 4.3 gates fired green. **Phase 1 deliberately did NOT touch physical-kit COMPOSITION** — physical kits still ride the HELD legacy b6 machinery (loud-routed). Phase 2 is the other half: move physical-kit skill composition onto the rich weapon-property cross-product, and PROVE the recognition record's load-bearing claim.

**This is the claim the whole recognition record stakes itself on** (spec § 3 + § 4.1): the deferral's stated blocker was that physical kit_size could not reach the legacy band (10-13 skills) because physical skills were keyed to the SPARSE physical-cost mechanic pools (`rage`=4, `focus`=4, `combo`=2, `stamina-as-resource`=2 — `composed_kit_adapter.py:82`; ~12 keyed slots cannot yield 10-13 *distinct* skills without repetition). The recognition's dissolution: root physical skill-composition on the SELECTED WEAPON'S rich properties crossed with the bc_cell behavioral target — the same composition surface caster kits already use — so the physical path stops being starved by the 12-entry mechanic pool. **Move the load from the sparse axis to the rich one.** Phase 2 TESTS this; it does not assume it.

## Required reading before starting

- `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md` §§ 3 (the composition design intent), 4.1 (THE gate), 4 (full gate)
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6 (the deferred-commitment gate, verbatim)
- Your Phase-1 math-note + the Phase-1 build: `src/reincarnated/generation/notes/2026-06-14-weapon-as-identity-phase-1-math-note.md`; `weapon_identity.py`; `class_generator.py:622-737`; the § 1.2 guardrail in `season_generation_pipeline.py:1005`
- `composed_kit_adapter.py:82` — the sparse physical-cost mechanic pools (the starvation source)
- The HELD physical-fork machinery (your Stage-3 audit): G4 `classify_archetype`, G5 `archetype_composer`, G7 `b6 ARCHETYPE_TEMPLATES`, G8 `B6KitBuilder` — Phase 2 builds the REPLACEMENT path but does NOT delete these (see Out of scope)
- The caster composition path (the model § 3 says to mirror): how caster kits compose off element × bc_cell
- Discipline #1 (math-before-code), #1.2 (code-cite), #2 / #2.1 (smoke-test + resource-scaling)

## Math-before-code (Discipline #1) — produce BEFORE any code; HALT for Gate-1

The load-bearing math is the **cross-product cardinality**: does the weapon-property cross-product yield ≥10-13 DISTINCT physical skills without repetition? Work it, code-cited:

1. **Enumerate the rich axes** on a representative physical weapon: `proxy_geometry_class`, `proxy_range_class`, `proxy_tempo_class`, `element_affinity_modifiers_json`, damage profile (cite the substrate fields + their cardinalities on the physical sub-pool). Cross with the bc_cell behavioral target (`geo_bin`, `tempo_bin`, etc.).
2. **Compute the distinct-skill yield** of (weapon properties × bc_cell) and show it reaches the 10-13 band WITHOUT enumerating the 12-entry mechanic pool. Show the cross-product is genuinely RICH (multi-property, high-cardinality) vs the sparse 12-key mechanic axis. If the math shows the cross-product CANNOT reach 10 distinct skills, SAY SO — that falsifies the recognition's prediction and is a valid Gate-1 outcome (route to gandalf for spec revision, do not code around it).
3. **Map the design-intent axes** (spec § 3) to concrete composition rules (rocket designs the algorithm; jack-ryan gates it): skill geometry ← weapon `proxy_geometry_class` × bc_cell `geo_bin`; range/tempo ← weapon `proxy_range_class`/`proxy_tempo_class` × bc_cell `tempo_bin`; flavor/element ← weapon `element_affinity_modifiers_json` (a physical weapon CAN carry elemental affinity — flaming greatsword = physical-identity, fire-flavored); skill count ← the 10-13 band off the cross-product.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**Assessment: CONDITIONAL — rocket resolves at math-note.** Phase 2 changes how physical kits compose (skill CONTENT). If the produced skills land in the SAME loadout/fight_log skill dict structure caster kits already use (spec § 3 asserts the composition surface is shared), there is NO cross-seam contract change. **But** if Phase 2 introduces a new skill field, changes the skill dict shape, or alters the `loadout` packet consumed by simulation / export / loadout, that IS a cross-seam contract change (ADR-004).

**rocket MUST decide + state explicitly in the math-note.** If YES → write `MIGRATION.md` + add a round-trip smoke (production-path fixture → gamora sim boundary / star-lord export boundary → field-presence check) to acceptance. If NO → state `Round-trip: not applicable because physical-kit composition reuses the existing shared skill dict shape; no field added/renamed/removed.` Silence is a Gate-1 BLOCK per Principle 6.

## Scope (Phase 2)

- [ ] **Math-note (Discipline #1) FIRST** — cross-product cardinality + the distinct-skill yield proof-in-principle, code-cited. HALT for Gate-1 before code.
- [ ] § 3 — compose physical-kit skills off the selected weapon's property cross-product × bc_cell behavioral target (mirroring the caster element × bc_cell surface). Route physical coordinates through this NEW path instead of the HELD b6 mechanic-pool fork.
- [ ] Disable/bypass the sparse physical-cost mechanic-pool path for the gate demonstration (§ 4.1 requires proving kit_size off the weapon cross-product WITH the mechanic-pool path disabled).
- [ ] Preserve the L1 identity proxy + the § 1.2 ratio guardrail from Phase 1 (do not regress them).
- [ ] Smoke-test passes (Discipline #2; #2.1 resource-scaling if roster-gen is compute-heavy).
- [ ] MIGRATION.md — IF the Principle-6 assessment resolves YES.
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `rocket/v1.3-weapon-as-identity-phase-2`.

## Acceptance criteria — the full § 4 gate (Phase 2 adds § 4.1, the headline)

- [ ] **§ 4.1 (THE gate, verbatim from the recognition record § 6) — PASS or HONEST FAIL.** A weapon-rooted physical kit composes to the legacy physical kit_size band (**10-13 skills**) WITHOUT depending on the sparse physical-cost mechanic pools — demonstrable by generating physical kits with the mechanic-pool path disabled/bypassed and confirming **≥10 DISTINCT skills**. Report the distinct-skill count + how distinctness is measured. **IF this fails, the deferral's blocker is REAL — report the failure clearly, do NOT force a pass; route to gandalf for spec revision.**
- [ ] **§ 4.4 re-run** — output ratio still in-band (no Phase-2 regression of the Phase-1 ratio guardrail).
- [ ] **§ 4.2 re-run** — caster coherence still ≥90% caster-family + 0% martial-fallback on caster cells (no regression).
- [ ] **§ 4.3 re-run** — no identity smuggle re-imported (grep-clean preserved).
- [ ] **Drift-injection smoke re-run** — the ratio guardrail's corrective branch still fires (no regression).
- [ ] Round-trip smoke per the Principle-6 resolution above (or the not-applicable justification).

## Out of scope (explicit non-goals)

- **NO architecture commit.** Produce the gate result; gandalf + Matt make the commit call.
- **NO Stage-3b deletion of the HELD physical-fork machinery** (G4 `classify_archetype` / G5 `archetype_composer` / G7 `b6 ARCHETYPE_TEMPLATES` / G8 `B6KitBuilder`). Phase 2 BUILDS the replacement path + proves it; the DELETION is a SEPARATE downstream step with its own gate. **G7 carries a cross-seam HOLD-SIM gate** (`balance_loop.py`, R-2) — do NOT delete it on generation-only clearance. (Once Phase 2 proves the new path, Stage 3b becomes re-openable — but that is not this dispatch.)
- **NO literal-weapon-root refactor of L1.** L1 stays proxy-rooted (committed as such 2026-06-14); the literal weapon-root is deferred as-time-allows and is NOT in Phase-2 scope.
- **NO hard-wiring the L2 23% proxy share** — stays DRAFT.
- **NO caster-faith within-family remediation** (§ 5) — open gandalf design call, deferred.

## Open questions for the agent to resolve (document in the math-note)

- The exact composition algorithm: how (weapon properties × bc_cell) maps to distinct skills, and how distinctness is defined/measured (geometry+range+tempo+element tuple uniqueness? skill-identity hash?).
- How elemental affinity on a physical weapon (`element_affinity_modifiers_json`) flavors a physical-identity skill without re-coupling identity to element (do NOT let flavor leak back into the L1 identity proxy).
- The Principle-6 resolution (shared skill dict vs new field) — decide + surface.
- Whether disabling the mechanic-pool path for the gate is a permanent route change or a gate-only toggle (the permanent deletion is Stage 3b, out of scope — but the routing change that makes physical kits USE the new path IS Phase 2).

## References

- gandalf spec `2026-06-14-weapon-as-identity-generation-spec.md` §§ 3, 4.1; recognition record `weapon-as-identity-surface-recognition-2026-06-14.md` § 6
- Phase-1 build: commit `7fc25a4`, tag `rocket/v1.2-weapon-as-identity-phase-1`; math-note `2026-06-14-weapon-as-identity-phase-1-math-note.md`
- `composed_kit_adapter.py:82` (the sparse mechanic pools); the HELD b6 fork (Stage-3 generation audit in `AGENT_STATE.md`)
- decisions-log: the 2026-06-14 L1-commit entry (proxy-rooted; literal-root deferred) + the § 1.2 ratio entry
- Disciplines #1 / #1.2 / #2 / #2.1

## Sequence (per-phase; KR-tracked)

rocket math-note → **jack-ryan Gate-1** → **gandalf design-fit review** → rocket code → **jack-ryan Gate-2 re-Gate**. KR brings the Phase-2 Gate-1 result back for gandalf's design-fit BEFORE code commits. **The § 4.1 gate outcome (pass OR honest fail) is the recognition record's commit/revise signal — KR routes it to gandalf + Matt.**
