# Dispatch — 2026-06-13 — gamora — W-B sim-side: type-wall + rename (TODAY drift-proofing)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-13 — cert-wave sequence approved; W-B is the Matt-pre-authorized TODAY drift-proofing move (wave doc § 3, "fire immediately on Matt's go").
**Status:** GATE-1 PASS-WITH-INFO (jack-ryan, 2026-06-13). Two INFO folded below (positive admit-canary; test-only mint note). FIRES on Matt go.
**Estimated effort:** ~hours (contained; rename + two types + one boundary test). NOT the spatial engine.
**Acceptance:** A **paired** boundary test: (a) a constructed `SearchGradeEstimate` attempting the identity-authority insert **fails at the boundary** (compile-time or raise); AND (b) a `CommitGradeVerdict` constructed via the legit provenance path **is admitted** (the positive canary — without it, an insert accidentally typed to reject *everything* would pass the negative test while broken). The 1D module + entry are renamed to strip the "fight" affordance. Brownfield: all existing 1D math is behavior-preserved (md5/byte-identical on a regression fixture) — this is a rename + type-wall, NOT a math change.

## Context

The cert wave closes a **recombination-drift trap** (wave doc § 1): in a 14-agent system, a *rule in a doc* ("the 1D duel is never balance-authoritative," contract § 5) is the weakest control — its own author drifted off it in two days (the defensive-bridge acceptance gate was a 1D measurement). The structural fix is a **type at the single archive chokepoint**: behavioral identity may be minted **only** by the commit-grade (spatial) path. This dispatch is the **simulation-side half** of that type-wall (§ 3.1) plus the rename (§ 3.3). star-lord owns the export-side half (parallel dispatch `2026-06-13-star-lord-wb-typewall-export.md`); the two share one type contract you author the MIGRATION for. gandalf fidelity-stamps the 1D artifacts in parallel (`2026-06-13-gandalf-wb-fidelity-stamp.md`).

This is W-B of the 2D-certification wave (`canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` § 5). It does NOT depend on 2D succeeding — it closes the recombination on the current codebase the moment it lands.

## Required reading before starting

- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` §§ 1–3 (the trap + the TODAY moves), § 6 out-of-scope (kernel untouched)
- `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` § 2 (kernel-freeze — `damage_resolver.resolve_skill` is FROZEN, do not touch), § 5 (the fidelity lock this operationalizes as a type)
- Verified code anchors (wave doc § 7): `GauntletArchive.insert` (`spatial_gauntlet/gauntlet_archive.py:208`, the single chokepoint); 1D BC feed (`bc_measurement.py` `run_bc_measurement_over_corpus` → `simulate_fight(measure_bc=True)`)
- `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md` (wave state; arity = 8)

## Math-before-code (Discipline #1)

Minimal — this is structural, not numeric. But author a short MIGRATION-anchored note in `simulation/MIGRATION.md` (or `simulation/math/`) defining the **shared type contract** before code:
- `CommitGradeVerdict` — minted **only** by the spatial path (the function that runs `run_spatial_fight` across the certified scenario set and will compute the 8-axis bin from *spatial* telemetry — that computation is W-D, NOT this dispatch). Carries a non-forgeable provenance marker: `fidelity="commit"`, `engine="spatial"`, scenario-set hash field.
- `SearchGradeEstimate` — minted by the 1D `search_estimator` (renamed `fight_engine`). Carries `fidelity="search"`.
- The provenance fields are the contract star-lord's export-side types must match. Document them in MIGRATION so star-lord reconciles to one shape.
- **(Gate-1 INFO) Note in MIGRATION that in W-B the `CommitGradeVerdict` type EXISTS with NO production mint site yet** — the spatial mint is W-D, out of scope here. So the positive admit-canary (acceptance (b)) uses a **hand-constructed, test-only** `CommitGradeVerdict` instance; do NOT wire a production mint to satisfy it (that would pull W-D forward).

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring)

**YES.** Two boundaries:
- **gamora → star-lord (type contract):** the `CommitGradeVerdict` / `SearchGradeEstimate` provenance shape is the contract star-lord's export-side types and the re-typed `bc_measured_bins.json` consume. Write the emit-side `simulation/MIGRATION.md` section documenting the type fields. star-lord reconciles in `2026-06-13-star-lord-wb-typewall-export.md`.
- **identity-authority insert signature:** the consumer that decides a kit's behavioral cell / culls duplicates (the BC-identity insert; eventually spatial `GauntletArchive.insert` once it computes the real tuple in W-D) accepts **only** `CommitGradeVerdict`. Feeding a `SearchGradeEstimate` must be a **type error**, not a runtime mis-pairing.

**Round-trip smoke (Principle 6):** Round-trip smoke: construct a `SearchGradeEstimate` from the 1D `estimate_search_grade` path and attempt the identity-authority insert across the gamora→consumer boundary — assert it fails at the boundary (the § 3.1 acceptance test IS the round-trip check).

## Scope

- [ ] Introduce `SearchGradeEstimate` (1D path output) + `CommitGradeVerdict` (spatial path output type; **the spatial computation that mints it is W-D — here you define the TYPE and make the insert accept only it**) with the provenance markers above
- [ ] Re-type the identity-authority insert signature to accept only `CommitGradeVerdict` (the type-wall)
- [ ] Paired boundary test: (a) `SearchGradeEstimate` → insert FAILS; (b) hand-constructed test-only `CommitGradeVerdict` → insert ADMITTED (positive canary)
- [ ] Rename `fight_engine` → `search_estimator`; `simulate_fight` → `estimate_search_grade` (and the obvious internal callsites) — vocabulary-as-control (§ 3.3). Keep `measure_bc=` behavior intact; the 1D path keeps working, it just produces a search-grade-typed estimate.
- [ ] The § 3.1 boundary test exists and passes (SearchGradeEstimate → identity insert FAILS at boundary)
- [ ] Brownfield invariant: a 1D regression fixture produces byte-identical numeric output pre/post (rename + type-wall changed no math)
- [ ] `simulation/MIGRATION.md` emit-side type contract section written
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `gamora/v-wb-typewall-rename-1`

## Out of scope (explicit non-goals)

- **The spatial engine internals** — that is W-C (the de-risk spike, separate dispatch). Do NOT bring the spatial engine to a working run here.
- **Computing the commit-grade 8-tuple from spatial telemetry** — that is W-D. Here you only define the `CommitGradeVerdict` TYPE and the insert that requires it.
- **Deleting the 1D engine** — that is W-F (terminal, jack-ryan-gated). The 1D path must keep working through the wave as the search-grade estimator.
- **The frozen kernel** — `damage_resolver.resolve_skill` is FROZEN (contract § 2). Untouched.
- **Fidelity-stamping the 1D artifacts** — that is gandalf's parallel dispatch (§ 3.2). Don't author canonical stamps.

## Open questions for the agent to resolve (document at Gate-2)

- Exact type representation (dataclass vs typed dict vs NewType) — your latitude; the provenance fields are the contract, the representation is HOW.
- Whether the rename warrants a thin back-compat shim for any external caller, or a clean break — your call; document it.

## References

- Wave doc § 3.1 (type-wall), § 3.3 (rename), § 6 (out-of-scope/kernel-freeze)
- Forward-architecture contract § 2 (kernel-freeze), § 5 (fidelity lock)
- W-C.5 close: `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md`
- Gate-2: jack-ryan gates the boundary test exists + passes, and the brownfield invariant, per seam protocol.

---

**Author:** knight-rider, 2026-06-13. The simulation-side half of the chokepoint type-wall + the noun-stripping rename — ends the recombination trap on the current codebase the moment it lands.

---

## Completion record

**Completed by:** gamora, 2026-06-13.
**Status:** COMPLETE. All scope items landed; all acceptance criteria PASS.

### What landed (files)

- **NEW `src/reincarnated/simulation/verdict_types.py`** — the shared provenance type contract.
  - `CommitGradeVerdict` (frozen dataclass): `fidelity="commit"`, `engine="spatial"`, `scenario_set_hash: str`, `bc_cell` (the W-D 8-tuple; `None` in W-B), `payload`. Markers PINNED in `__post_init__` (non-forgeable).
  - `SearchGradeEstimate` (frozen dataclass): `fidelity="search"`, `engine="duel_1d"`, `payload`.
  - `CommitGradeRequired(TypeError)` + `require_commit_grade(verdict)` boundary guard. Provenance literals exported as module constants for single-source reconciliation.
  - **Representation decision (open question resolved):** frozen dataclasses, NOT `NewType` (erases at runtime → no `isinstance` wall) and NOT `TypedDict` (structural → a dict with `fidelity="commit"` would forge through). Rationale in math note § 4.
- **`spatial_gauntlet/gauntlet_archive.py`** — type-wall at the chokepoint.
  - New door `GauntletArchive.insert_identity(verdict, entry)` admits ONLY a `CommitGradeVerdict` (calls `require_commit_grade`); raises `CommitGradeRequired` at the boundary otherwise.
  - Legacy `insert(entry)` (swarm-only, placeholder cell, NOT identity-authoritative) **preserved unchanged** — the running convergence path keeps working through the wave. Placement rationale (math note § 2): the wall belongs on the *identity* door (no production caller until W-D); re-typing `insert` itself would strand the live pipeline before W-D mints any commit-grade verdict.
  - `GauntletArchiveEntry` gains additive default-`None` `commit_grade_provenance: Optional[dict]` (dataclass-brownfield-safe).
- **Rename:** `git mv fight_engine.py → search_estimator.py` (pure move; history preserved; no math re-typed). Canonical entry `estimate_search_grade` = `simulate_fight` (same function object). `fight_engine.py` is now a thin **DEPRECATED re-export shim** (tombstone; removed in W-F).
- **`bc_measurement.py`** — typed front door `estimate_search_grade_bins(...)` wraps the 1D corpus document in a `SearchGradeEstimate` (the round-trip seam the boundary test uses). `run_bc_measurement_over_corpus` unchanged (on-disk JSON contract preserved).
- **`__init__.py`** — exports `estimate_search_grade` + `CommitGradeVerdict` + `SearchGradeEstimate`; imports the entry from the canonical `search_estimator` module.
- **NEW `tests/test_wb_typewall_rename.py`** — 10 acceptance tests (paired boundary, brownfield, rename integrity).
- **Math note `simulation/math/wb-typewall-rename-2026-06-13.md`** (Discipline #1, authored before code).
- **`simulation/MIGRATION.md` § v1.69** — the emit-side provenance-fields contract (cross-seam, star-lord).

### Paired-test result (acceptance § 3.1)

PASS. (a) NEGATIVE — a `SearchGradeEstimate` (including one minted from the REAL 1D `estimate_search_grade_bins` path) attempting `insert_identity` raises `CommitGradeRequired` at the boundary; archive stays empty. (b) POSITIVE admit-canary — a hand-constructed, TEST-ONLY `CommitGradeVerdict` is ADMITTED (`archive.size()==1`, provenance stamped). The canary guards against an insert accidentally typed to reject everything. **No production `CommitGradeVerdict` mint was wired** (the spatial mint is W-D) — the canary is test-only, per the Gate-1 INFO. Additional negatives: arbitrary object rejected; empty `scenario_set_hash` rejected; forged `fidelity` overridden by the pin.

### Brownfield-invariant result (acceptance: byte-identical numeric output)

PASS. Deterministic 5-seed fixture (seeds 1/7/42/1234/99999, full `measure_bc=True` path) — **md5 `8f8fa6915f3c49a99825698f37710c1a` captured pre-change, identical post-change** via BOTH the canonical `estimate_search_grade` AND the `fight_engine` shim. The rename + type-wall changed no math. Empirically corroborated: clean-HEAD worktree baseline shows the only failing tests on the touched suites are pre-existing (5 fast-suite / 12 full-suite failures, reproduced on pristine HEAD; all generation/missing-doc data deps, none from this change). Changed tree adds the 10 new W-B tests as the only delta.

### MIGRATION contract shape (for star-lord)

`SearchGradeEstimate`: `{fidelity:"search" (pinned), engine:"duel_1d" (pinned), payload:dict}`.
`CommitGradeVerdict`: `{fidelity:"commit" (pinned), engine:"spatial" (pinned), scenario_set_hash:str (non-empty required), bc_cell:Any (W-D-computed; None in W-B), payload:dict}`.
star-lord's export-side types reconcile field-for-field. **MIGRATION explicitly notes `CommitGradeVerdict` has NO production mint site in W-B** (W-D mints it from spatial telemetry); export-side should not assume a populated `bc_cell` until W-D. Round-trip (Principle 6): a `SearchGradeEstimate` is structurally un-feedable to the identity authority on both seams.

### Tag

`gamora/v-wb-typewall-rename-1`.

### Gate-2 notes for jack-ryan

- Gate item (a) — the § 3.1 boundary test EXISTS and PASSES: `tests/test_wb_typewall_rename.py::test_search_grade_estimate_rejected_at_identity_insert` (+ `::test_search_grade_from_real_1d_path_rejected`, `::test_commit_grade_verdict_admitted`). SATISFIED.
- Gate item (b) — the brownfield invariant: `::test_brownfield_invariant_canonical_entry` + `::test_brownfield_invariant_via_shim` (both match baseline md5). SATISFIED.
- **Semantic-shift declaration (Discipline #12):** the rename is vocabulary-as-control — it changes how the 1D path's output is *interpreted* (search-grade, not fight-authoritative). Declared in the commit message AND in MIGRATION § v1.69. Routes to a decisions-log entry at your discretion (composes with the cert-wave § 3.3 rename + the type-wall as one structural control).
- **Design-latitude calls recorded** (the dispatch's two open questions): representation = frozen dataclass (math note § 4); rename = canonical-rename + thin back-compat shim, NOT a clean break (math note § 5) — chosen so the brownfield invariant is provable (pure git-mv) and the ~14 importers keep working; the shim is a bounded tombstone removed in W-F.
- No locked-edge change, no telemetry-schema change, no generation-primitive change, frozen kernel untouched.

**Auto-committed (gamora seam). NOT pushed (Matt's wave-close gate).**
