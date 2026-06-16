# Finding — 2026-06-16 — Gate-2 rocket i-frame dodge glass-close-ST (Move 2, SUBSUME a)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no WARN, no BLOCK)
**Mode:** DEV-MODE Gate-2 (post-output, tag-release gate)
**Target:** engine commit `51867f5` ("rocket: bake guaranteed-intrinsic i-frame DODGE on glass-close-ST (Move 2, SUBSUME a) — CODE only, TAG HELD")
**Developer:** rocket
**Tag released:** `rocket/v1.9-iframe-dodge-glass-close` (applied at `51867f5`)
**Authority:** Tier-1 additive gate per run-plan charter `canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md` §5.2 (KR autonomous run, Matt-ratified 2026-06-16). Gate-2 PASS is terminal-on-clean.
**Principles applied:** Principle 1 (math-before-code), Principle 2 (smoke-gate), Principle 3 (cross-seam impact), Principle 6 (cross-seam round-trip)
**Disciplines applied:** #1, #1.2 (code-cite), #2 (smoke-vs-regen), #11, #12 (semantic-shift); ADR-004

---

## What I found

The SUBSUME (a) implementation is correct and the B′ double-instrument guard is **genuinely MOOT**. I independently verified all four load-bearing claims against the code, not the commit message. The i-frame dodge adds NO new slot: it tags whichever in-range physical evasion Rule D already reserved on `def_bin=="glass"`, so the kit_size band and the geometry-distinct (≥10) proof are untouched and need no re-proof. The SUBSUME predicate is label-free + deterministic. The Gate-1 amendments are folded. The smoke passes. The WARN tag-ordering precondition (role-floor clears Gate-2 first) is satisfied. Verdict: PASS-WITH-INFO; the held tag is released.

## Independent verification (the crux)

**Claim 1 — SUBSUME reuses the existing Rule-D slot, no new slot, no kit_size/distinctness shift (B′ moot):** CONFIRMED.
- The tag is applied at STEP 6 (`weapon_envelope_composer.py:606-607`) to a slot Rule D already reserved (`:436-440`); it appends nothing to the work-list. `skills` length is unchanged; `geometry_only_distinct` (`:611`) is computed identically to pre-Move-2.
- `_DEFENSIVE_FLOOR_GEOMETRIES` (Rule-D pool, `:135` = `defensive_dash, leap_strike, dash_attack`) ⊆ `_MOBILITY_GEOMETRIES` (`:117` = same three). So the predicate fires on EVERY Rule-D draw outcome → guaranteed-intrinsic for any weighted draw, with zero added slots.
- Smoke empirically confirms: across all 6 proxy geometries × 2 sub-60 tiers + synthetic melee (kit_size 10 & 13), `geo_distinct` held at 13 (10/11 on zero-slack melee) and EXACTLY 1 dodge per kit. B′ has nothing to guard — there is one movement instrument, not two. MOOT confirmed on code + empirics, not assertion.

**Claim 2 — predicate is label-free + deterministic, no rng on the guarantee path:** CONFIRMED, and the load-bearing subtlety holds.
- `_is_iframe_dodge_slot(role, geometry)` (`:182-189`) reads ONLY `role=="defensive" AND geometry in _MOBILITY_GEOMETRIES`. No archetype label; no `rng` call.
- The disambiguator from Rule-M is the `role` field: Rule M reserves the SAME three geometries but with `role="mobility"` (`:444-447`), so the predicate excludes them. This is sound ONLY because line 570 (`role = forced_role if forced_role is not None else _role_for_geometry(...)`) preserves the FORCED reserved role. If STEP 6 had recomputed `_role_for_geometry(defensive_dash)` it would return "mobility" (`:361-362`) and silently break the guarantee. It does not — it uses the forced "defensive". Verified.
- The Rule-D reservation itself fires on the deterministic `if def_bin=="glass"` predicate (`:436`), never a probability gate. The weighted draw varies WHICH evasion geometry is drawn (smoke: `{leap_strike:10, dash_attack:4}`), but the tag fires on all of them — so the guarantee is rng-independent.

**Claim 3 — A2-1/A2-2/A2-3/CL-1 Gate-1 amendments folded:** CONFIRMED.
- A2-3 (SUBSUME reconciliation, no double-instrument): folded as SUBSUME (a); the distinct-instrument branch never materializes (math-note §4; code STEP 6 single tag).
- A2-1 (label-free determinism / weighted-draw + role-predicate tag): folded; in-execution Gate-1 (`2026-06-15-telegraph-dodge-move1-move2-gate1-inexecution.md` Note-2) endorsed weighted-draw + role-predicate over a `defensive_dash` pin. Code matches.
- A2-2 (export-survival of i-frame metadata): correctly NOT a rocket change. `ExportSkill` (`export/schemas.py:244-261`) strips i-frame metadata; rocket routed the fix to dispatch 4 (star-lord) per the CONFIRMED home in the in-execution finding. The commit touches no export schema. Correct seam discipline.
- CL-1 / teleport-trap bar: STRUCTURALLY barred. `:257-258` asserts the physical sub-palette never contains a `CASTER_ENVELOPE_GEOMETRIES` member (`teleport`/`blink`, `:74-77`); the dodge pool is in-range physical evasions only. Smoke confirms "NEVER teleport". The ruling's forbidden trap cannot be reached.

**Claim 4 (Principle 6) — no generation→sim contract change:** CONFIRMED. `i_frame_window` is a pre-existing nullable field (`skill_schema.py:64`) added by commit `17772bd` (B6/B13/B14/B15 schema additions), NOT by `51867f5`. The held commit only POPULATES it; no field added/renamed/removed at the boundary. Round-trip not-applicable is the correct call; no MIGRATION.md required.

## Smoke (Discipline #2)

`scripts/rocket_dodge_intrinsic_smoke_2026_06_15.py` (LLM-free, role-composition only, seconds) — **PASS**. Every glass-close-ST kit carries EXACTLY 1 i-frame dodge (defensive role, in-range evasion, never teleport, `i_frame_window` at default 0.05/0.30); Rule-M mobility slots untagged; negative control (mitigator/non-glass) carries ZERO dodge; kit_size + geo_distinct held. Verified by re-running independently (not trusting the committed log line).

## WARN tag-ordering precondition — SATISFIED

The in-execution Gate-1 set a WARN: Move 2 may not tag until the role-floor fix clears Gate-2, and re-derive the predicate if role-floor Gate-2 changed Rule D's shape. Status:
- `rocket/v2.2-envelope-role-floor` tag is applied; the run-plan charter §2.3 treats role-floor as landed substrate. The applied seam tag is the operational gate-clearance signal.
- Rule D's shape is UNCHANGED: nothing touched `weapon_envelope_composer.py` between `51867f5` and HEAD (`51867f5` is engine HEAD); `_MOBILITY_GEOMETRIES` (`:117`) and `_DEFENSIVE_FLOOR_GEOMETRIES` (`:135`) match the predicate's assumptions exactly. No re-derivation needed. Ordering condition met → tag released.

## INFO items (non-blocking)

- **INFO-1 (audit-trail thinness):** No role-floor Gate-2 *finding file* exists in `qa/findings/`; clearance is evidenced only by the applied `rocket/v2.2-envelope-role-floor` tag + the charter's landed-substrate treatment. The tag is sufficient operationally, but a future convention point: a milestone/substrate tag whose Gate-2 has no finding file leaves the gate's reasoning unrecorded. Not a blocker for THIS release; flag for KR's records.
- **INFO-2 (downstream dependency, already routed):** A2-2 export-survival (i-frame metadata stripped by `ExportSkill`) is the one seam where the dodge could silently fail to reach Godot. It is correctly routed to dispatch 4 (star-lord) and is cert-gated downstream. This is a tracked open handoff, not a defect in this commit — re-flagging so it does not fall off KR's dispatch-4 scope.

## Action
- [x] jack-ryan: Gate-2 PASS-WITH-INFO. Tag `rocket/v1.9-iframe-dodge-glass-close` applied at `51867f5`.
- [ ] knight-rider: ensure A2-2 `ExportSkill` i-frame-field extension is in dispatch 4 (star-lord) scope before it fires (INFO-2; per the in-execution Gate-1 fold, re-route to me for a Gate-1 on the dispatch-4 amendment).
- [ ] jack-ryan (deferred, non-blocking): author the Discipline-#12 semantic-shift decisions-log entry for the dodge-intrinsic composition addition at the wave-consolidation point.

## References
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/weapon_envelope_composer.py` (`:117`, `:135`, `:182-189`, `:257-258`, `:436-440`, `:444-447`, `:570`, `:606-607`, `:611`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/skill_schema.py:64` (pre-existing `i_frame_window`; added by `17772bd`)
- `/Users/admin/Games/reincarnated-engine/scripts/rocket_dodge_intrinsic_smoke_2026_06_15.py` (smoke — PASS)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-15-dodge-intrinsic-glass-close-st-math-note.md` (math-note)
- `agentic_orchestration/qa/findings/2026-06-15-telegraph-dodge-move1-move2-gate1-inexecution.md` (in-execution Gate-1, Note-2 — WARN ordering condition + A2-2 home)
- `agentic_orchestration/dispatches/2026-06-15-rocket-dodge-intrinsic-glass-close-st.md` (Move 2 dispatch)
- `canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md` §5.2 (Tier-1 authorization)
