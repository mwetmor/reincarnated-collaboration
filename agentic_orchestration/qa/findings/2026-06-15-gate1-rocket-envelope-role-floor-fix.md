# Finding — 2026-06-15 — Gate-1 (DESIGN-MODE) — rocket envelope coordinate-derived role-floor fix

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1, pre-fire on the dispatch)
**Severity:** CLEAR-WITH-AMENDMENTS
**Target:** `agentic_orchestration/dispatches/2026-06-15-rocket-envelope-role-floor-fix.md` (DRAFT, Matt-GREENLIT)
**Developer:** rocket (recipient)
**Author:** knight-rider (dispatch)
**Principles applied:** Review Principle #1 (math-before-code), #3 (cross-seam impact), #4 (decisions-log as truth); Disciplines #1, #6, #12; ADR-004

## Verdict

**CLEAR-WITH-AMENDMENTS.** The dispatch is well-built, tightly code-cited, and the anti-creep spine is sound in intent. The amendments below are not blockers to firing — they are math-note Gate-1 constraints to fold into the dispatch BEFORE it fires, so the mandatory floor-math-note Gate-1 has a concrete checklist to verify against and rocket doesn't walk into a known collision unwarned. All amendments are documentation additions to the dispatch; none change the fix's scope.

---

## Answers to the six questions

### Q1 — Is the anti-creep spine enforceable, or just exhortation? → ENFORCEABLE, with one verification rule the dispatch must add.

It is enforceable, AND I found the concrete verification mechanism for the math-note Gate-1. The spine is NOT just an exhortation, because the floor mechanism is forced through `grammar.generate(role=..., element="physical", forced_geometry=...)` — the exact lever b6 uses (`weapon_envelope_composer.py:329-339`). A label cannot drive that call; only a role string + a geometry do. So the smuggling surface is narrow and inspectable.

The subtle failure mode you named — a coordinate-tuple that is a 1:1 proxy for the old rogue label — is real but **detectable by a single test the math-note Gate-1 can run**: the floor rule must fire on the COORDINATE PREDICATE, not on the cell's full 8-tuple equality. Concretely:

- LEGITIMATE: `if def_bin == "glass": reserve ≥1 defensive slot`. This fires for EVERY glass cell (rogue, skirmisher, glass casters, future glass cells) — it is a coordinate predicate, archetype-blind.
- SMUGGLED LABEL: `if (def_bin, geo_bin, eng_bin, tempo_bin) == ("glass","single-target","close-fast","high"): ...`. That conjunction IS the rogue cell's signature (`bc_target_source.py:36/:54/:147-149`) — a label in coordinate clothing.

**Verification rule for the math-note Gate-1 (the smuggle-test):** each floor rule must key on the SINGLE coordinate that genre-justifies it (glass→survival; *-fast→mobility; single-target→AoE-share), and must demonstrably fire on a DIFFERENT cell that shares that one coordinate but is not rogue. If any floor rule requires ≥3 coordinates in conjunction to fire correctly, that is the smuggle tell — halt and surface. The dispatch already names the per-coordinate mapping in its math-note section; this amendment makes the "one-coordinate-per-rule, cross-cell-firing" property an EXPLICIT Gate-1 pass criterion rather than leaving it implicit.

### Q2 — Is the Principle-6 (cross-seam contract) lean-NO correct? → CORRECT. Verified against the Skill dict + grammar boundary.

Confirmed empirically. `role` is an existing field on the shared `Skill` dict, and the grammar ALREADY maps `role="defensive"` to geometries (`ability_grammar.py:138`). The b6 path emits defensive-role skills through the identical `grammar.generate` + `composer.compose` mechanism with a `require_defensive_skill` post-check (`b6_kit_builder.py:844-848`). Emitting `role="defensive"` from the envelope reuses the existing field, the existing grammar role-table, and the existing Skill shape. No field added/renamed/removed. Lean-NO is correct; the dispatch's required not-applicable justification language is accurate. The gamora G7 re-pass exercises the sim boundary regardless. No MIGRATION.md needed on the most-likely path.

### Q3 — Is the kit_size non-regression adequately specified? → YES, with one tightening.

The dispatch correctly requires the 10-13-band cross-product re-proof WITH reserved role slots and correctly asks for geometry-only-distinct reporting (matching Phase-2's metric, `weapon_envelope_composer.py:357`). Tightening: the re-proof must show the band holds AFTER the reserved slots are subtracted from the free draw — i.e. `(reserved_floor_count) + (free_geometry_distinct_draw) ≥ 10` AND total distinct ≤ 13. The risk is not the floor over-filling; it is the floor RESERVING slots that then collapse geometry-distinctness (e.g. if defensive + mobility both resolve to the same `self_buff`-adjacent geometry, the distinct count drops). The math-note should report distinct-geometry count WITH floor slots in place, not just total kit_size. Folded into amendment A3.

### Q4 — Are the out-of-scope fences correct and complete? → YES. The live-wiring fence is correctly out-of-scope.

Confirmed: `compose_physical_kit_envelope` is not referenced in the live `class_generator` path (the audit found physical coords still route to legacy b6). Keeping live-wiring out-of-scope is CORRECT and the fix remains meaningful without it, because the validation path is the G7 HOLD-SIM harness, which invokes the composer directly — the fix is provable through the harness without re-routing the live path. Live-wiring is genuinely a separate downstream routing step (its own dispatch, its own Gate-2) and bundling it here would (a) expand a multi-day fix into a cross-seam routing change and (b) entangle the b6-deletion tally with a routing cutover. The NO-b6-deletion, NO-caster, NO-architecture fences are all correct and consistent with gandalf §6 and the held architectural question. Fences complete.

### Q5 — Is the sequencing right? → YES. No mis-ordering.

math-note → MANDATORY Gate-1 → implement → Gate-2 → gamora G7 re-pass (its own Gate-2) → KR carries toward b6-deletion both-pass tally → Decision 2 (separate, gandalf+Matt confirm). This matches gandalf §7 routing exactly and respects recognition→validate→commit (the G7 re-pass is the validate gate; b6 deletion is the commit, correctly downstream and Matt-gated). The architectural question staying HELD throughout and NOT gating the fix is correct per gandalf §6. Nothing missing.

### Q6 — Anything that lets the fix regress something or smuggle the label back? → ONE material catch (amendment A1, below).

---

## What I found — the one material catch (NEVER-cross collision)

The dispatch says "the composer has NO defensive-emission path today — design the coordinate-derived defensive emission" and cites the grammar. What it does NOT flag: the grammar's `defensive` role maps ONLY to `self_buff` (4.0) and `teleport` (1.5) geometries (`ability_grammar.py:138`), and **BOTH `self_buff` and `teleport` are in `CASTER_ENVELOPE_GEOMETRIES`** (`weapon_envelope_composer.py:74-77`) — the explicit NEVER-cross set a physical weapon must never reach (gandalf Q2 step-3 rule, the cross-envelope assertion at `:184`).

So the obvious defensive-emission path — call `grammar.generate("defensive", "physical", ...)` — collides head-on with the weapon-as-envelope NEVER-cross invariant. A greatsword would emit a `self_buff`/`teleport` skill, which is exactly the caster-geometry crossing the architecture forbids. This is the single point where rocket is most likely to either (a) silently let a caster geometry into the physical envelope (regressing the NEVER-cross invariant the whole envelope rests on), or (b) hit the wall and reach for a label to special-case it (regressing the anti-creep spine). The dispatch's HONEST clause covers case (b) as a valid finding, but the collision should be NAMED so rocket meets it with eyes open rather than discovering it mid-implementation.

This is descriptive: the collision EXISTS in the current code. The resolution is rocket's to design at the math-note (a physical-coherent defensive geometry vocabulary, or a `forced_geometry` defensive slot drawn from physical-palette geometries that carry a defensive role-stamp, or a justified narrow grammar extension) — but the dispatch must surface the collision as an explicit math-note open question so the floor-math-note Gate-1 can verify the chosen resolution does NOT cross the envelope.

## Rationale

- The NEVER-cross set (`weapon_envelope_composer.py:74-77`, assertion `:184`) is a load-bearing architectural invariant of the weapon-as-envelope design (gandalf Q2 step-3). A defensive-emission path that reaches a caster geometry regresses it. Review Principle #3 (cross-seam / cross-invariant impact) — a fix must not silently break an invariant a sibling design layer proved.
- Discipline #12 (semantic-shifting fixes need explicit framing): adding a defensive-emission path where none exists IS a composer semantic addition. The dispatch correctly tags it #12 and mandates Gate-1; the NEVER-cross collision is precisely the semantic edge that #12 demands be framed explicitly rather than carried silently.
- Discipline #1 (math-before-code) + Review Principle #1: the coordinate→floor mapping and its NEVER-cross resolution belong in the math-note BEFORE code — the smuggle-test (Q1) and the collision resolution (A1) are math-note Gate-1 pass criteria.

## Amendments (fold into the dispatch before it fires)

- **A1 (the material one):** Add to "Open questions for the agent to resolve" and to the math-note section: *"The grammar's `defensive` role maps only to `self_buff`/`teleport` (`ability_grammar.py:138`), BOTH of which are in `CASTER_ENVELOPE_GEOMETRIES` (the NEVER-cross set, `weapon_envelope_composer.py:74-77`). The coordinate-derived defensive emission MUST resolve this collision WITHOUT crossing the envelope — design a physical-coherent defensive vocabulary or a defensive role-stamp on a physical-palette geometry. The math-note Gate-1 will verify no emitted floor skill lands on a CASTER_ENVELOPE_GEOMETRIES geometry. If a physical-coherent defensive geometry cannot be built without a grammar change or a label, that is a valid HONEST-clause finding → route to gandalf."*
- **A2 (the smuggle-test, Q1):** Add to the math-note section as an explicit Gate-1 pass criterion: *"Each floor rule keys on the SINGLE coordinate that genre-justifies it (one-coordinate-per-rule), and must be shown to fire on a non-rogue cell sharing that one coordinate. Any rule requiring a ≥3-coordinate conjunction to fire is a smuggled-label tell — halt and surface."*
- **A3 (Q3 tightening):** Amend the cardinality re-proof bullet to require reporting distinct-geometry count WITH floor slots reserved (not just total kit_size), proving `reserved_floor_distinct + free_draw_distinct` stays in the 10-13 band — the floor must not collapse distinctness, not merely fit within the count.

None of these expand scope; all are math-note Gate-1 constraints + one named open question. The fix as designed remains correct and fireable.

## Action

- [ ] knight-rider: fold A1/A2/A3 into the dispatch (documentation-only; my ADR-002 tiered authority covers approving the dispatch to fire once folded — no Matt escalation needed, nothing here conflicts with a locked decisions-log entry).
- [ ] rocket: at the math-note, resolve the A1 NEVER-cross collision explicitly and satisfy the A2 smuggle-test + A3 distinctness-with-floor proof. HALT for the mandatory floor-math-note Gate-1 (I review it).
- [ ] rocket: if the defensive vocabulary cannot be built physical-coherent without a label or grammar change, invoke the HONEST clause → gandalf.

## References

- `agentic_orchestration/dispatches/2026-06-15-rocket-envelope-role-floor-fix.md` (reviewed)
- `agentic_orchestration/gandalf/notes/2026-06-15-rogue-degeneracy-role-floor-diagnosis-for-kr.md` (parent spec, §5/§6/§7)
- `reincarnated-engine/src/reincarnated/generation/weapon_envelope_composer.py` — `CASTER_ENVELOPE_GEOMETRIES` `:74-77`, NEVER-cross assertion `:184`, `_role_for_geometry` `:243-252`, `compose_physical_kit_envelope` `:277-372`, geometry-only-distinct `:357`
- `reincarnated-engine/src/reincarnated/generation/ability_grammar.py` — `defensive` role→geometry map `:138`
- `reincarnated-engine/src/reincarnated/generation/b6_kit_builder.py` — `require_defensive_skill` post-check `:844-848`
- `reincarnated-engine/src/reincarnated/generation/bc_target_source.py` — rogue cell coords `:36/:54/:147-149`
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` — rogue `required_roles` `:247-251`, AoE-share `:242`
