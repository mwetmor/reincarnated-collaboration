# Gate-1 Finding — 2026-07-07 — rocket leg-2 summoner `primary_t4` proxy-family routing

**Reviewer:** jack-ryan (DESIGN-MODE — Gate-1 peer critique; no BLOCK authority at this gate)
**Verdict:** **PASS-WITH-CONDITIONS**
**Critique pair:** jack-ryan (process/technical) + gandalf (design — emission-band pricing)
**Target:** math note `generation/math/leg2-summoner-primary-t4-routing-math-2026-07-07.md` (engine commit `cbac6ed`)
**Developer:** rocket (route side) ∥ star-lord (validator-widen half, co-dispatched)
**Governs:** dispatch `2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md`; spec `proxy-t4-suite-spec-2026-07-02.md` v3 §1/§4/§4.5/§8
**Principles applied:** Review Principles 1 (math-before-code), 3 (cross-seam impact), 4 (decisions-log truth), 6 (cross-seam round-trip); Disciplines #1, #1.1, #11, #23, #19.1; ADR-002, ADR-004

---

## What I found

The note is a clean, source-grounded before-code artifact. I verified every load-bearing claim against engine source rather than accepting the note's citations. The routing predicate P is correct: `select_proxy_t4(..., proxy_decls=[]) is None` is not an assertion the note asks me to trust — it is an EXISTING passing test (`w0_prereqs_smoke_2026_07_03.py:207`, check 6h), so the S2 no-op-off-summoner-bin guarantee is empirically anchored, and the non-summoner population is provably byte-identical post-P. The `is not None` gate (over a bare `proxy_decls != []` test) is the correct single gate — it folds is-summoner and does-any-member-clear-η_floor into one branch, with DDA displaced (never removed) only when a proxy member wins. The FROZEN accepted value-set is correct against source: `PROXY_T4_FAMILY` (`mechanic_alteration.py:1466-1472`) is exactly the five members rocket names; `PROXY_INVERSION` is structurally absent from the family list and `ZONE_CONTROL` lives in a separate `GEOMETRY_ZONE_STRATEGIES` registry — both exclusions are structural, not conventional, so `select_proxy_t4` can never return either. The conditional-widen contract (empty-decl kits still reject a stray non-DDA; DDA stays admissible on both branches for the no-member-clears fallback) is the correct star-lord contract. The three derive sites are real and the seam split is clean: sites 2 (`gauntlet_sim.py:2267`) and 3 (`unified_calibration_loop.py:3577`) both call `select_primary_t4` DIRECTLY today, so rocket's divergence risk (site-1 routes, sim re-derives DDA) is a genuine cross-seam integrity hazard, correctly named as gamora's consume obligation and not patched by rocket. The §2.1 band framing is faithful to spec §4.5 lines 118-120 verbatim ("Emission bands (measured, not forced)... Self-cast T4s stay in `t4_candidates`... outcompeted at scan-time by design, not banned"); the ≥90%/≥60% bands are correctly scoped as a MEASURED leg-3 outcome of a deterministic argmax route, not a leg-2 threshold, and the self-cast-stays-in-`t4_candidates` disposition is a ratified rule (spec §4.5 / R3 line 133), not a new design choice. Disc #1.1 resource-bounds are correctly deferred to the leg-3 note with an explicit forward flag. The 2026-07-06 decisions-log entry (Matt Option 1 / batch 2) is the governing authorization; no conflict with any locked entry.

## Rationale

- **Principle 1 (math-before-code):** SATISFIED. Predicate, η/decl consequence, value-set contract, refutation table, and resource-bounds forward-flag all present before any routing code. No production code landed this session (verified: note is the sole artifact).
- **Principle 3 / ADR-004 (cross-seam impact + MIGRATION):** The note correctly identifies this as a cross-seam certification-path change with a producer (rocket site 1), a validator (star-lord), and TWO consume sites (gamora 2/3). This is a THREE-seam lockstep, not two.
- **Principle 6 (cross-seam round-trip):** The round-trip (S3) is correctly assigned to star-lord's half and includes the negative case (empty-decl stray non-DDA still rejects).
- **Disc #23 / #19.1 (framing audit + cheapest refuting test):** The three framing questions are answered honestly; the one downstream design pre-commit (`primary_t4` slot vs `t4_candidates`) is named-not-silent and traces to a ratified spec rule.
- **The gap:** the note NAMES gamora sites 2/3 as consume obligations but this artifact carries NO gamora-side acknowledgment. The whole leg's cross-seam integrity condition — persisted proxy `primary_t4` not silently overwritten to DDA at sim-time — depends on gamora actually patching 2/3 in the SAME landing as rocket's site 1. A named obligation is not a captured obligation. This is a coordination-capture condition (ADR-004), not a rework of the math.

## Conditions to fold BEFORE routing code lands

- [ ] **C1 (rocket + KR) — three-seam MIGRATION lockstep, not two.** The generation MIGRATION entry must cross-reference BOTH star-lord's validator MIGRATION AND a gamora consume-side acknowledgment for sites 2/3 (`gauntlet_sim.py:2267`, `unified_calibration_loop.py:3577`). Do not land site 1 while sites 2/3 still unconditionally re-derive DDA — that is the exact emitted-vs-simulated capstone divergence the note's §1.1 warns against. If gamora's patch is a separately-sequenced landing, the MIGRATION must state the interim state explicitly (i.e., between rocket-land and gamora-land, sim re-derives DDA for summoners — a known-transient divergence with a named closing event).
- [ ] **C2 (rocket + star-lord) — value-set is FROZEN as a shared MIGRATION constant.** `ACCEPTED_PROXY_PRIMARY_T4 = {PROXY_ASCENSION, PROXY_SOVEREIGNTY, PROXY_FISSION, PROXY_CONVERGENCE, DUAL_PROXY}` must be the single shared entry both seams build against; if either seam reshapes it, the other tracks in lockstep BEFORE either tags (per co-dispatch). Confirmed correct against source — condition is that it is recorded ONCE, not duplicated divergently.
- [ ] **C3 (rocket) — S2 byte-diff is the mandatory pre-tag gate.** The $0 deterministic schema/byte-diff of a non-summoner corpus pre/post-P (note §4 refutation table row 1) is the single most load-bearing invariance check and must be GREEN and cited in the Gate-2 submission, not merely named as available.
- [ ] **C4 (rocket, INFO — carry to Gate-2, not blocking):** the new S1 route-correctness unit case (bone→FISSION, crypt→SOVEREIGNTY under DoF-A `focus`) should be added to the existing 77-test surface and its output cited at Gate-2.

## F-f disposition — CONFIRMED

Leg-2's route does NOT make the GEOMETRY co-draw reachable: `select_proxy_t4` returns a SINGLE argmax member and `ZONE_CONTROL` is structurally outside `PROXY_T4_FAMILY` (verified — separate `GEOMETRY_ZONE_STRATEGIES` registry). `enforce_family_max_one` stays structurally unreachable through the summoner route. Rocket's disposition — **re-surface F-f to KR as still-B4-scoped** — is correct. Confirmed; name it in the leg-2 MIGRATION per the note.

## Action

- [ ] Developer (rocket): fold C1–C3 before routing code; carry C4 to Gate-2.
- [ ] Developer (star-lord): build validator-widen against the C2 shared frozen set; round-trip smoke both cases.
- [ ] KR: ensure C1's gamora consume-side acknowledgment is captured in the lockstep MIGRATION (three-seam, not two).
- [ ] Matt: no decision needed at Gate-1 (peer critique; no locked-entry conflict). Leg-2 routing code + Gate-2 proceed once C1–C3 are folded.

## References

- Math note: `reincarnated-engine/src/reincarnated/generation/math/leg2-summoner-primary-t4-routing-math-2026-07-07.md` (`cbac6ed`)
- `mechanic_alteration.py`: `select_primary_t4:1831` (ALWAYS-DDA), `select_proxy_t4:1895` (returns None on empty/no-clear), `PROXY_T4_FAMILY:1466-1472`, `GEOMETRY_ZONE_STRATEGIES` (ZONE_CONTROL isolated)
- `t4_catalog_v2.py:55-60` (ratified PROXY constants; INVERSION present in catalog but absent from family)
- Derive sites: `season_generation_pipeline.py:404-412` + `:1327-1331` (site 1, rocket); `gauntlet_sim.py:2267` (site 2, gamora); `unified_calibration_loop.py:3577` (site 3, gamora)
- Empty-decl None assertion: `generation/notes/w0_prereqs_smoke_2026_07_03.py:207` (check 6h — existing passing test)
- Spec: `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` §4.5 lines 118-120 (measured-not-forced bands), R3 line 133 (one-primary-per-kit)
- Governing decision: decisions-log `2026-07-06 — W3 summoner emission: Matt rules Option 1 (batch 2)`
- Dispatch: `agentic_orchestration/dispatches/2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md`
