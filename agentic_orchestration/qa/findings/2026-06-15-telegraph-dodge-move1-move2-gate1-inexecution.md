# Finding — 2026-06-15 — telegraph/dodge Move 1 + Move 2 (in-execution Gate-1, math-note review)

**Reviewer:** jack-ryan
**Severity:** INFO (both notes); WARN on one sequencing item (Note 2, build-on-pending-substrate)
**Mode:** DESIGN-MODE Gate-1 (in-execution, pre-code) — the developers HALTED at the math-before-code boundary; neither wrote code.
**Developers:** gamora (Move 1), rocket (Move 2)
**Principles applied:** Principle 1 (math-before-code), Principle 3 (cross-seam impact), Principle 6 (cross-seam round-trip)
**Disciplines applied:** #1, #10, #11, #12; ADR-004

---

## NOTE 1 — gamora (auto-amp delete → flag-and-defer): CLEAR-TO-IMPLEMENT

**Severity: INFO.** No fold. The note is the strongest kind of math-before-code output: it refuted the dispatch's own naive premise (no rogue-keyed amp branch exists — §1.1, empirically grepped) and re-grounded the move on the real live mechanism (the universal binary-search `damage_modifier`, `balance_loop.py:1108-1223` + re-run `:1249-1333`). Discipline #11 satisfied verbatim. The two-door interception (amp door / fail door), the coordinate-keyed (never label-keyed) detector reading `bc_target` bins, the `bc_target is None → False` null-safe default, and the deletion-inert guard (§5, additive `None` fields only on non-glass cells) are all sound and match the §7.2 posture (sim still walls; only the READING changes).

### Door-1 pick (adjudicated): modifier=1.0 + skip-search — CONFIRMED

Take gamora's recommendation. Rationale:
- It is the literal "do not auto-compensate" semantic. A run-search-but-discard variant computes a compensated number whose only consumer would be diagnostics — and the honest native-output WR is ALREADY captured at `comp_wr` (`:1104-1106`, runs at modifier=1.0). The discard variant manufactures a second number that means "what we WOULD have faked," which invites exactly the misreading flag-and-defer exists to kill.
- It is the cheaper path (skips search iterations) and reduces work for glass-close-ST cells — no new hotspot (Discipline #1.1).
- It composes cleanly with the deletion-inert guard: the gated branch is entered or it is not; there is no half-state where a search ran but was thrown away.
One implementation note for Gate-2 (not a Gate-1 block): assert in the smoke that `final_modifier == 1.0` EXACTLY on a gated cell (gamora already lists this, §6.1) — that single assertion is the operational proof the skip-search door fired and the amp door did not.

### Principle-6 call (adjudicated): YES is CORRECT — the star-lord touchpoint is real

gamora's Principle-6 resolution (YES, telemetry-emitted, MIGRATION.md + gamora→star-lord round-trip required) is the right call, and it DOES legitimately add a star-lord touchpoint to a dispatch you scoped as sim-internal. The reasoning is forced by the ruling, not optional: the whole point of the move (ruling §4) is that the season summary must read "viability deferred," not "failure." A verdict-surfacing requirement means the `dodge_gated` status MUST reach star-lord's export, and `ClassBalanceResult` is a star-lord-consumed schema (its entire field history is "star-lord adds nullable column"). Adding a nullable column to a consumed schema is a write to the gamora→star-lord boundary = ADR-004 = Principle 6 YES. Silence here would have been a BLOCK; gamora resolved it correctly and routed the schema-column proposal to star-lord rather than modifying telemetry schema directly (correct seam discipline). MIGRATION.md + round-trip smoke required, as stated.

**Note 1 is CLEAR-TO-IMPLEMENT** on Door-1=modifier-1.0-skip-search, with the star-lord schema-column proposal + MIGRATION.md + gamora→star-lord round-trip as Gate-2 acceptance evidence (alongside the §5 deletion-inert guard). Semantic-shift (Discipline #12) is declared and routes to me for a decisions-log entry — I will author that entry at implementation-land, not now.

---

## NOTE 2 — rocket (dodge-intrinsic on glass-close-ST): CLEAR-TO-IMPLEMENT with one WARN-gated ordering condition

**Severity: INFO on the substance; WARN on the build-on-pending-substrate ordering (condition below).** The SUBSUME (a) verdict is correct and well-proven: the i-frame dodge IS Rule D's already-reserved `def_bin=="glass"` defensive slot (`weapon_envelope_composer.py:396-401`), so it adds ZERO slots — kit_size band + distinctness proof are untouched, no re-proof, and the double-instrument B′ guard is genuinely moot under subsume. The guarantee proof (deterministic `if def_bin=="glass"` predicate, sub-pool draw cannot return 0, no `rng.random()` on the Rule-D path — §1.3) is airtight. Teleport/blink structural bar via the cross-envelope assertion (`:219-221`) is correctly load-bearing. The role-predicate i-frame tag (`role=="defensive" AND geometry in _MOBILITY_GEOMETRIES`) fires on whichever of the three in-range evasions Rule D draws, so guaranteed-intrinsic holds for any draw outcome — I endorse keeping the weighted draw + role-predicate tag (§4.3 lean) over a deterministic `defensive_dash` pin; the i-frame intent is geometry-agnostic across the three in-range physical evasions and pinning adds determinism the ruling does not require.

### (1) Build-on-pending-substrate ruling: WARN — proceed-to-CODE but do NOT tag until role-floor clears Gate-2

The role-floor fix this note builds on is Gate-2-PENDING + unpushed. The MATH is sound to author on top of it (the note IS the math), and Move 2 is cert-INDEPENDENT, so there is no reason to invert the ordering at the design layer. But the CODE ordering must respect dependency: Move 2's i-frame tag has no meaning if Rule D's reservation changes shape in Gate-2 review. Ruling:
- **Proceed to code is permitted** — rocket may implement the i-frame tag on top of the unpushed role-floor substrate.
- **CONDITION (the WARN):** Move 2 may NOT reach its own Gate-2/tag (`rocket/v1.x-dodge-intrinsic`) until the role-floor fix has CLEARED Gate-2. If role-floor Gate-2 forces any change to Rule D's slot shape, geometry pool, or the `_MOBILITY_GEOMETRIES` set (`:117`), Move 2's tag predicate must re-derive against the cleared substrate before it tags. Sequence the two Gate-2s: role-floor first, then dodge-tag. This is the safe ordering without paying the cost of serializing the code work itself.
- This is a Discipline #1 / Principle 1 sequencing call, not a correctness defect in the note. The note is clear; the tag is gated.

### (2) A2-2 export-gap home: CONFIRMED — dispatch 4 (star-lord), NOT a rocket-seam change

I verified rocket's read directly. `ExportSkill` (`schemas.py:244-261`) allow-list ends at `flavor_text`; there is NO `i_frame_window`, NO `cast_time`, NO `damage_resolution_time` field — confirmed by reading the full class. `_build_skill` (`season_exporter.py:409-436`) is a fixed-field projection with no usability filter, so the dodge SKILL survives (good — the §41 whole-skill-drop risk does not materialize) but its i-frame METADATA is silently stripped. Rocket's routing is correct on both counts:
- **The fix belongs in dispatch 4 (star-lord), not rocket.** Extending `ExportSkill` + `_build_skill` to carry the B13 i-frame fields (additive, nullable, ADR-004-clean) is an export-seam change. rocket owns generation; it correctly does NOT touch the export schema and surfaces the gap to KR for dispatch-4 scope. Confirmed.
- **The telegraph-JSON-vs-ExportSkill boundary is correctly left for star-lord.** I read dispatch 4 (`2026-06-15-star-lord-telegraph-export-schema.md`): it serializes gamora's **TelegraphSpec** as a NEW section "alongside the existing fight export" (§11, §53) — a SEPARATE serialization path from the `ExportSkill`/`season_exporter` class-skill projection. So rocket's flagged unknown resolves: the telegraph JSON is a distinct emitter; the `ExportSkill` i-frame strip is a real gap for the class-export path that Godot's dodge-input wiring reads, and it is NOT made moot by the telegraph emitter. star-lord must resolve which path Godot's dodge-input wiring consumes (likely the class-skill export for the role+geometry+timing, with the telegraph JSON for the attack geometry) — correctly left for star-lord.

### (3) Spirit-guide fork

Correctly routed to Matt/gandalf via KR, with composition-baked as the default for Move 2's pipeline-completion gate. I endorse the default-holds recommendation — relocating the dodge's home to `spirit_guide/` now would re-scope the dispatch and couple Move 2 to spirit-swap grant-timing for no pipeline benefit. Future re-home is a worthy design call but does not gate the bridge. No QA action; this is a gandalf/Matt design call, not a process gate.

**Note 2 is CLEAR-TO-IMPLEMENT** on SUBSUME (a) + weighted-draw + role-predicate tag + composition-baked default, with the WARN-gated tag-ordering condition: role-floor Gate-2 clears before Move 2 tags. i-frame default magnitudes (0.05/0.30s) are sim-inert Godot-consumed placeholders — acceptable as a single archetype-default for now; they carry no balance math and rocket correctly does not manufacture a per-form distribution.

---

## CONVERGENCE assessment — TWO independent star-lord touches, NOT one coordinated touch

Both notes land work on star-lord, but they touch DIFFERENT schemas on DIFFERENT boundaries and should NOT be force-merged into one coordinated change:

- **Note 1 → `ClassBalanceResult`** (`balance_loop.py:639`), the gamora→star-lord **balance/telemetry** boundary. Adds `dodge_gated` / `dodge_gated_native_winrate` nullable columns + the new `recompose_outcome="dodge_gated_deferred"` enum value. Consumer: season summary / verdict surface.
- **Note 2 → `ExportSkill`** (`schemas.py:244-261`), the star-lord→drax/Godot **player-surface export** boundary. Adds `i_frame_window` / `cast_time` / `damage_resolution_time` to the skill projection. Consumer: Godot dodge-input wiring (dispatch 5).

These are orthogonal: different files, different schemas, different consumers, different MIGRATION.md entries, and they arrive on different fire-clocks (Note 1's schema lands with gamora's Move-1 implementation; Note 2's `ExportSkill` extension lands inside dispatch 4's already-scheduled work). Coordinating them into one touch would couple two independent fire-clocks for no gain and would bloat a single MIGRATION.md entry across two unrelated boundaries — an anti-pattern against clean per-boundary contract documentation (ADR-004). **Recommendation: two independent star-lord touches, each with its own MIGRATION.md entry and its own round-trip.**

### Does this change dispatch-4 scope you already authored?

**YES — additively, and the addition should be folded into dispatch 4 BEFORE it fires.** Dispatch 4 as written (§32-33) scopes the dodge-export confirmation as "confirm the skill survives; FIX if a filter drops it." That covers the whole-skill-survival half (which rocket confirmed is fine — no filter). It does NOT scope the `ExportSkill` i-frame-FIELD extension, because at authoring time the metadata-strip was not yet surfaced. rocket's A2-2 finding (B) adds a concrete, bounded deliverable to dispatch 4:

> Extend `ExportSkill` (`schemas.py`) + `_build_skill` (`season_exporter.py:409-436`) to carry the B13 i-frame fields (`i_frame_window`, `cast_time`, `damage_resolution_time`) through the class-skill projection — additive, nullable, ADR-004-clean — with its own round-trip on a glass-close-ST fixture asserting the i-frame window survives serialization.

This does NOT change dispatch 4's load-bearing invariant (§7.1 no-drift on the TelegraphSpec) and does NOT touch the telegraph-JSON emitter — it is a second, smaller deliverable on the class-skill export path. Recommend KR fold it into dispatch 4's Scope + Acceptance before dispatch 4 fires (rocket's stated intent — "surface it NOW so dispatch 4's scope includes this BEFORE dispatch 4 fires"). I will re-Gate-1 the dispatch-4 amendment when KR folds it, since it adds a boundary the original Gate-1 clearance did not cover.

---

## Action
- [ ] gamora (Note 1): CLEAR-TO-IMPLEMENT. Door 1 = modifier=1.0 + skip-search. Principle-6 YES confirmed: MIGRATION.md + gamora→star-lord round-trip + schema-column proposal to star-lord required as Gate-2 evidence.
- [ ] rocket (Note 2): CLEAR-TO-IMPLEMENT (code). SUBSUME (a) + weighted-draw + role-predicate tag + composition-baked default confirmed. **WARN condition: do NOT tag `rocket/v1.x-dodge-intrinsic` until role-floor fix clears Gate-2; re-derive the tag predicate if role-floor Gate-2 changes Rule D's shape.**
- [ ] knight-rider: fold rocket's A2-2 `ExportSkill` i-frame-field extension into dispatch 4 (star-lord) scope + acceptance BEFORE dispatch 4 fires. Two INDEPENDENT star-lord touches (ClassBalanceResult + ExportSkill), not one. Re-route to me for a Gate-1 on the dispatch-4 amendment.
- [ ] jack-ryan (me): author the Discipline-#12 semantic-shift decisions-log entry at Move-1 implementation-land (not now). Re-Gate-1 the dispatch-4 amendment when KR folds the ExportSkill extension.

## References
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/auto-amp-delete-flag-defer-2026-06-15.md` (Note 1)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-15-dodge-intrinsic-glass-close-st-math-note.md` (Note 2)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/schemas.py:244-261` (ExportSkill allow-list — i-frame strip confirmed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-15-star-lord-telegraph-export-schema.md` (dispatch 4 — telegraph JSON is a separate path from ExportSkill; dodge-export confirmation scoped, i-frame-field extension NOT yet scoped)
- `agentic_orchestration/dispatches/2026-06-15-gamora-auto-amp-delete-flag-defer.md` (Move 1 dispatch)
- `agentic_orchestration/dispatches/2026-06-15-rocket-dodge-intrinsic-glass-close-st.md` (Move 2 dispatch)
