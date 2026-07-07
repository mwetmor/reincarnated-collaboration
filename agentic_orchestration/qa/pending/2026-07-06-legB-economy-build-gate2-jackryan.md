# Gate-2 Disposition — 2026-07-06 — batch-2 Leg-B `resource_economy` cross-seam build

**Reviewer:** jack-ryan (DEV-MODE, Gate-2 post-output; BLOCK authority)
**Disposition:** **PASS-WITH-FOLLOWUPS**
**Targets:** `rocket/v-batch2-legB-economy-emit-1` (engine `9eca04c`) + `gamora/v-batch2-legB-economy-consume-1` (engine `7e1a5d1`) — NEITHER pushed
**Developers:** rocket (generation emit) + gamora (simulation consume) — coordinated cross-seam build
**Governing:** dispatch `2026-07-06-rocket-gamora-batch2-legB-build-resource-economy.md`; my Gate-1 conditions C1–C4 (`2026-07-06-legA-economy-axes-gate1-jackryan.md`)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 4 (decisions-log truth), 6 (cross-seam round-trip)
**Disciplines applied:** #1 (math-before-code), #2 (smoke), #8 (schema validation at boundaries), #11 (empirical inspection — I re-ran everything), #12 (semantic-shift framing), #24 (sweep-isolation)
**ADRs applied:** ADR-002 (tiered approval — this is cross-seam schema, ESCALATES to Matt), ADR-004 (MIGRATION.md both halves)

---

## Disposition summary

**PASS-WITH-FOLLOWUPS.** The frozen Route-B contract holds end-to-end with zero drift; I byte-checked
every load-bearing claim against the landed tree and re-ran every smoke + regression suite myself
(Discipline #11 — I did not take any GREEN on trust). All four Gate-1 conditions relevant to this
build (C2 Route-B, C3 round-trip, C4 hard default-corner) are honored. C1 is a Leg-C spec-vocabulary
item, correctly out of scope here. **The C4 default-corner check is a genuine hard-checked assertion
(the run fails, exit≠0, if it breaks), not prose. The production-path instrument fact is sound and
correctly documented.** The two followups are non-blocking (one decisions-log continuity entry I owe;
one stale-line-number cleanup in the MIGRATION docs). No BLOCK.

**This build carries a cross-seam schema change (new `resource_economy` loadout field, generation→sim).
Per ADR-002 that is Matt's approval tier, not mine — I dispose PASS on the engineering, and this
ESCALATES to Matt for the cross-seam-schema sign-off before the star-lord pilot fire.**

---

## What I found

I independently reproduced both smokes and all cited regression suites against the landed tags. The
emit side (`resource_economy.py`) defines the exact 7-key frozen contract, `DEFAULT_RESOURCE_ECONOMY`
byte-matches the contract's default corner, the sampler is salt-disjoint from Leg-1 (`ECONOMY_SALT_BASE
=1_800_000`), and `_validate()` enforces exact key-set + types at the boundary (Discipline #8). Both
emit sites (`season_generation_pipeline.py:533` KitCandidate + `bc_target_player_class.py:428`
PlayerClassV2) carry the field via `default_factory=default_resource_economy`, so the key is always
present — mirroring the `proxies` two-path contract exactly. The sim consumes it at
`entity_from_class_dict` (`spatial_engine.py:2780`, imports the rocket-owned `DEFAULT` anchor so the
sim default IS the emit contract — no drift), folds cost/regen at init and binds cadence at the live
cast write and ramp at the tick, all player-only and identity-at-default. The `on_kill` hook fires at
BOTH kill-flip sites (`:1536` resolver / `:1550` flat), player-only, gated `frac>0.0`, clamped to max,
inert at frac 0.0. The dict keys/types match on both sides of the seam.

## Verification ledger (Discipline #11 — I re-ran all of this, did not trust the completion records)

| # | Claim under review | My independent check | Verdict |
|---|---|---|---|
| 1 | Frozen contract holds end-to-end, no drift | 7-key set identical in `resource_economy.py:38-45`, both emit sites, and sim read; `_validate` rejects extra/missing keys | ✓ NO DRIFT |
| 2 | **C4 = HARD checked assertion, not prose** | `legB_economy_consume_smoke:191-196` — `check("C4a…", open_def==0.0)` + C4b; a non-zero KPM records FAIL and returns exit 1. I ran it: **0.0 KPM on BOTH shells** (open + choke) | ✓ **GENUINE HARD ASSERTION** |
| 3 | C3 round-trip on PRODUCTION (bounded) path; instrument fact documented | Smoke threads `player_class=` → `from_player_class` bounded pool; projection-pins-mana=1e9 fact stated in docstring L18-30 + math note. I ran it: open 0.0→1.0(fav)/2.667(ramp), choke 0.0→1.0 | ✓ SOUND + DOCUMENTED |
| 4 | MIGRATION.md both halves + file:line + Disc #12 note | `generation/MIGRATION.md` [2026-07-06] (declares field, sampler, semantic-shift §) + `simulation/MIGRATION.md` [2026-07-06] (consume sites, WIRE precondition, Disc #12 EXTENDS-Phase-1) | ✓ BOTH PRESENT |
| 5 | WIRE_RESOURCE_ECONOMY is a CHECKED precondition, inert-sweep impossible to fire silently | Hard Python `assert SE.WIRE_RESOURCE_ECONOMY is True` at smoke run-path top (`:163`) + flag-gated at `:1233`/`:2156`/`:2351`; flag default True (`:214`) | ✓ CHECKED (see followup FU-2 nuance) |
| 6 | Per-cohort identity does NOT collapse into shared bucket keys (the Leg-4 miss) | economy carried as first-class named dict on loadout + `cadence_scale`/`on_kill_frac`/`ramp_per_s` first-class on `SpatialEntity` (`:573-575`); identity readable at measurement. No bucketing/fire in this build's scope | ✓ IDENTITY READABLE |
| 7 | on_kill hook at both flip sites, burst=frac·max_energy, no-op at 0.0 | `_on_kill_energy_burst` (`:1440`), called `:1536`+`:1550`, `if attacker.is_player and on_kill_frac>0.0`, clamp to max | ✓ EXACT |
| 8 | Adjacent suites pass, no Leg-1 regression | I re-ran: consume smoke 7/7, emit smoke 4/4 (E1–E4), pathb-1a sim 35/35, subspace 27, generation emitter/proxy/bundle/season suites **266 passed** (superset of the cited 122) | ✓ ALL GREEN |

**Bonus check (byte-identity):** the completion record claims a no-`resource_economy`-key class_dict
produces identical `mean_mobs_killed`+`mean_elapsed_s` to the default corner. This check is NOT in the
committed smoke file (the smoke tests default-vs-favorable, not no-key-vs-default). I therefore ran it
myself directly: **no-key == default corner, byte-identical on both metrics.** The `.get(...) or DEFAULT`
fallback is a true no-op; the additive contract is genuinely backward-compatible. Claim VERIFIED, but
the artifact for it lives only in this finding, not the repo (see FU-3, INFO).

## Gate-1 condition reconciliation

- **C1** (18-cell vs 68,040-cell spec-vocabulary gap) — **correctly OUT OF SCOPE.** C1 was explicitly
  scoped to close before Leg C, not this build; the dispatch's out-of-scope list confirms it (line 64:
  "NO 18-cell / roster-enumeration work — that's the C1 vocab fix, gandalf, spec-side"). Not a Gate-2
  item here. Still open for Leg C.
- **C2** (Route B ratified pending gamora concurrence) — **HONORED.** gamora concurred (consult `be6c7c6`:
  "Route B call, on_kill hook trivial, no route blocker"); both completion records document the
  parallel-against-frozen-contract coordination. No Route-A override. C2 closes.
- **C3** (Leg-B build carries the round-trip) — **HONORED.** Round-trip smoke present, on the production
  path, field-presence check on the joined key GREEN, non-default corner moves KPM. Verified by re-run.
- **C4** (default-corner regression is a hard checked assertion, the built-in refutation) — **HONORED.**
  This was the load-bearing one. It is a real checked assertion that fails the run if the binding breaks,
  and it reproduces 0.0 KPM on both shells. Verified by re-run.

## Rationale

Principle 6 (cross-seam round-trip on production-path fixtures, not test-isolated) is fully satisfied:
the smoke uses a REAL season-001 caster PlayerClass on the bounded production path, and the instrument
choice is deliberate and documented — the projection/harness path pins `mana=1e9` and cannot starve, so
it could not demonstrate a resource-driven move; the production path is the faithful instrument. This
directly determines whether the downstream star-lord pilot fire will actually exercise the economy, and
it will, because the pilot rides the same production path. ADR-004 is satisfied on both seam halves.
Discipline #12 semantic-shift is framed on both sides (KPM now varies with per-kit economy identity —
EXTENDS Phase-1). Discipline #24 sweep-isolation holds: cost folds at one init site inherited by both the
affordability gate and the cast decrement; cadence writes a disjoint field; the categorical strata gate
on_kill/ramp so no two regen mechanisms co-apply. Per ADR-002, the cross-seam schema change itself is
Matt's approval tier — my PASS is on the engineering; the schema sign-off escalates.

## Followups (none blocking)

- **FU-1 (jack-ryan owes, decisions-log continuity):** the sim MIGRATION (line 42) correctly flags
  "jack-ryan: decisions-log continuity entry at Gate-2." The Discipline-#12 semantic shift (KPM now varies
  with per-kit economy identity, extending the Phase-1 resource-budget shift) warrants a decisions-log
  continuity entry. I will author it (jack-ryan owns decisions-log writes; references ADR-004 + Discipline
  #12). This is my action, not the developers'.
- **FU-2 (INFO, precision on item 5):** the WIRE_RESOURCE_ECONOMY hard `assert` lives in the *smoke run
  path*, which validates the build. The actual *pilot* run path is star-lord's downstream dispatch. The
  precondition is genuinely checked where this build can check it (an inert sweep cannot pass this smoke
  silently), and the flag defaults True. Recommendation for the star-lord pilot dispatch: carry the same
  hard `assert SE.WIRE_RESOURCE_ECONOMY is True` at the top of the pilot fire path so the guarantee travels
  to the production sweep, not just the build smoke. Note for the pilot Gate, not a defect in this build.
- **FU-3 (INFO, stale line numbers in the MIGRATION/completion docs):** the docs cite the entity-init read
  at `:2694` and the kill flips at `:1506-1508`/`:1519-1521` and cadence at `:2126`; the landed code has
  these at `:2780`, `:1536`/`:1550`, and `:2147` respectively (line drift from the pre-final state the
  records were drafted against). The *code is correct and the sites exist* — only the doc citations are
  stale. Non-blocking; rocket/gamora may refresh the `file:line`s in the two MIGRATION halves at
  convenience so future archaeology lands on the right lines (Discipline #1.2 code-citation hygiene).
- **FU-4 (INFO):** the no-key-vs-default byte-identity claim is real (I verified) but has no committed
  artifact — it is asserted in the completion record and now in this finding. Optional: gamora could add a
  third default-corner check to the smoke (no-key path == default) so the backward-compat guarantee is
  regression-protected in-repo. Quality-ratchet only.

## Action

- [ ] jack-ryan: author the decisions-log continuity entry for the Leg-B economy semantic shift (FU-1).
- [ ] Matt (ESCALATE — ADR-002 cross-seam schema tier): sign off on the `resource_economy`
      generation→sim cross-seam contract before the star-lord pilot fire. Engineering disposition is PASS;
      this is the architectural cross-seam-schema approval only.
- [ ] star-lord (downstream pilot dispatch, informational): carry the WIRE_RESOURCE_ECONOMY hard assert
      onto the pilot fire path (FU-2); the pilot rides the same production path the smoke validated.
- [ ] rocket/gamora (at convenience, non-blocking): refresh stale `file:line` citations in the two
      MIGRATION halves (FU-3); optionally add the no-key==default byte-identity check to the smoke (FU-4).

## References

- Tags/commits: `rocket/v-batch2-legB-economy-emit-1` (`9eca04c`), `gamora/v-batch2-legB-economy-consume-1` (`7e1a5d1`) — neither pushed
- Emit: `generation/resource_economy.py:38-45,50-58,64,124`; `season_generation_pipeline.py:424,533`; `bc_target_player_class.py:332,428`
- Consume: `spatial_gauntlet/spatial_engine.py:214,573-575,1233,1440-1452,1536,1550,2147,2444,2780-2888`
- Smokes I re-ran: `simulation/notes/legB_economy_consume_smoke_2026_07_06.py` (7/7), `generation/notes/legB_economy_emit_smoke_2026_07_06.py` (4/4)
- Regression I re-ran: `simulation/notes/pathb_1a_sim_consumption_smoke_2026_06_22.py` (35/35); `tests/test_bc_target_subspace_generator.py` (27); `tests/test_cycle14_unified_bundle_emitters.py`, `test_kit_space_emitter.py`, `test_one_realm_bundle_assembler.py`, `test_proxy_pairing_layer.py`, `test_proxy_t4_suite_eval.py`, `test_proxy_t4_suite_strategies.py`, `test_cascade_r4_track_a_season_production.py` (266 combined)
- MIGRATION: `generation/MIGRATION.md` + `simulation/MIGRATION.md`, both [2026-07-06] batch-2 Leg B
- Math notes: `generation/notes/legB-economy-emit-math-2026-07-06.md`; `simulation/math/legB-economy-consume-math-2026-07-06.md`
- Gate-1: `agentic_orchestration/qa/pending/2026-07-06-legA-economy-axes-gate1-jackryan.md` (C1–C4)

**Signed:** jack-ryan, 2026-07-06 — Gate-2 DEV-MODE, PASS-WITH-FOLLOWUPS. The frozen Route-B contract
holds end-to-end with zero drift; C4 is a genuine hard-checked assertion (0.0 KPM on both shells, verified
by re-run); the production-path instrument choice is sound and documented. No BLOCK. The cross-seam schema
change escalates to Matt per ADR-002 before the pilot fire.
