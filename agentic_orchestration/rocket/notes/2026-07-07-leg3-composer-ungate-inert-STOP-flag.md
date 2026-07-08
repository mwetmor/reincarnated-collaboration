# Leg-3 STEP-2 touch-point 4 — composer un-gate is INERT for the pilot path — STOP-and-FLAG

> **STATUS:** FINDING — STOP-and-FLAG (Discipline #11 inspect-source + #19.1 refute-own-claim).
> **Author:** rocket (generation seam), 2026-07-07.
> **Dispatch:** `dispatches/2026-07-07-rocket-starlord-leg3-STEP2-emission-wire-and-run.md` touch-point 4.
> **Gate-1 cleared:** `qa/findings/2026-07-07-rocket-leg3-summoner-emission-wire-projection-gate1.md` (PASS-WITH-CONDITIONS).
> **Corrects:** my own STEP-1 math-note §3.1 causal claim (composer gate → 0 proxy kits in the pilot). That claim was WRONG.

## TL;DR

Touch-point 4 instructs: lift `_DEFERRED_PROXY_BINS` @ `bc_target_composer.py:97` (gate at `:318`) "for the pilot so
proxy-bearing bins compose into the pilot population." **I traced the actual leg-3 pilot generation path against
source (Disc #11) and it does NOT flow through `bc_target_composer.check_infeasibility` or `_DEFERRED_PROXY_BINS`
at all.** Editing that frozenset would add **exactly zero** proxy cells to the pilot population, while silently
changing the behavior of a DIFFERENT (orphan/subspace) composition path. That is a duct-tape edit that fakes a
"un-gate landed" signal. **I did NOT make the composer edit.** C1 (the doc line-ref fix) is folded and lands.

The pilot's proxy population is gated by `ENDGAME_ENCOUNTER_CATALOG` curation, NOT by the composer frozenset.

## The empirical trace (reproducible)

The leg-3 pilot runs through `w3_emission_driver.run_w3_emission` → STEP-2 (`w3_emission_driver.py:435`) calls
`w5r1_generate_kit_candidates(seed_base=generation_seed)`. That generator (`season_generation_pipeline.py:784`,
loop at `:819`) iterates **`ENDGAME_ENCOUNTER_CATALOG`** — the 18-cell curated active catalog. Leg-1's summon path
threads `proxy_density=enc.bc_proxy_density` into `emit_skills_for_kit` (`season_generation_pipeline.py:1067-1068`)
→ a proxy-bearing cell appends a summon skill → `build_proxies_surface(self.skills)` (`:528`) emits a non-empty
`proxies` decl. **This whole path is live and un-gated by the composer.**

- `bc_target_composer` is imported by exactly TWO modules: `bc_target_source.py` and one smoke note. **Neither is
  imported by `season_generation_pipeline.py`, `endgame_encounter_catalog.py`, or `w3_emission_driver.py`.**
  (`grep -rln "from .bc_target_composer|import bc_target_composer"` → 2 hits, both off the pilot path.)
- `bc_target_source.py` is imported by **nobody** in the pilot path (orphan for this run).
- `w5r1_generate_kit_candidates` / the pipeline / the driver contain **zero** references to `check_infeasibility`,
  `_DEFERRED_PROXY_BINS`, `is_deferred`, or `compose_kit`. (`grep` → empty.)
- The driver docstring line 370 ("Step 1 (un-gate): SKIPPED for batch 1") names a step that **does not exist** in
  `run_w3_emission` — there is no un-gate call to skip. The population is 100% catalog-determined.

### The active-catalog proxy distribution (the REAL pilot gate)

`ENDGAME_ENCOUNTER_CATALOG` (18 cells) = **17 `none` + 1 `light` + 0 `heavy`** (empirically counted). The catalog
docstring (`endgame_encounter_catalog.py:8-12, 505-506, 722`) states the curation explicitly: "7 proxy-deferred
cells excluded per BC-axes-lock §5 deferred-evaluation policy. 1 proxy-light non-deferred cell included." The
proxy-heavy and extra proxy-light cells were **never authored into the 18** — they are absent, not commented-out.

### Does the pilot population contain ANY proxy-bearing kit? YES (contra STEP-1 §3.1's "measures nothing")

Probe (in-memory, seed-free structural check): the 1 proxy-light cell
`endgame_bc_ranged_medium_variable_int_light` emits `n_skills=13, n_proxies=1` — a real non-empty proxy decl via
the live leg-1 path. So star-lord's emit-wire will have proxy-bearing kits to measure at N≥10 (one cell × N
samples). The pilot does NOT "measure nothing" — but it measures **only proxy-light, and only from one cell**;
it has **zero proxy-heavy coverage** because those cells are not in the active catalog.

## Why the composer edit is wrong (not just unnecessary)

1. **It adds zero proxy cells to the pilot.** The pilot path is catalog-gated; the frozenset is on a path the
   pilot never touches. `n_proxy_cells` before = 1, after = 1.
2. **It silently changes non-pilot behavior.** `_DEFERRED_PROXY_BINS` still governs the 8-step
   `bc_target_composer` path (via `bc_target_source.py`). Lifting it there changes that path's deferral semantics
   for any future caller — exactly the "do not silently change non-pilot composition behavior" the dispatch's own
   touch-point 4 line forbids. And note my 2026-07-03 refutation still holds for THAT path: composer Phase 4d
   (`:756-757`) is still a no-op stub, so un-gating it there yields hollow `proxies: []` kits — a criterion-B fake.
3. **It fakes an "un-gate landed" signal** to star-lord's TP1-3, which would then run believing the pilot has
   proxy-heavy coverage it does not have.

## What the dispatch's INTENT actually requires (routed to KR — do NOT self-select)

The dispatch intent is unambiguous and Matt-authorized: get proxy-bearing (esp. proxy-heavy) cells into the pilot
population so the emit-wire measures the §8-A1 bands across the proxy role-split. The correct in-seam lever for
that intent is **not** the composer frozenset — it is the **`ENDGAME_ENCOUNTER_CATALOG` curation** (or the driver's
cell source). Options, for KR/Matt:

1. **Run the pilot on the catalog as-is (1 proxy-light cell).** Wire-proof + emit-path proof lands; §8-A1 bands are
   measured on proxy-light only; proxy-heavy A1-coverage is reported as NOT-EXERCISED-THIS-PILOT. Smallest scope,
   zero new content, ships the wire proof. **The emit-wire (star-lord TP1-3) is fully exercisable on this.**
2. **Author the deferred proxy cells into the catalog** (2 proxy-heavy + the other proxy-light cells): net-new
   `EndgameReferenceEncounter` definitions (mob_composition, playability_gate, WR contracts, etc.). This is
   material content generation with its own math-note + Gate-1 — **out of scope for a "wire only, chassis FROZEN,
   kits vote BARE" dispatch.** It is the honest path to proxy-heavy pilot coverage but it is a separate authored
   wave, not a frozenset lift.
3. **Point the pilot driver at the proxy-rich `bc_target_cell_sampler.CELL_DEFINITIONS` roster** (which HAS
   proxy-heavy cells) instead of `ENDGAME_ENCOUNTER_CATALOG`. This is a driver-source swap (star-lord's seam) +
   validation that the two rosters are shape-compatible — a cross-seam re-scope, not a rocket frozenset lift.

**My pragmatic read (not a decision):** Option 1 for THIS pilot — it proves the wire + emit path end-to-end at $0,
measures the proxy-light band, and honestly reports proxy-heavy as not-yet-covered. Option 2 as the named
follow-up to earn proxy-heavy pilot coverage properly (math-first, Gate-1'd). But the coverage-vs-scope call
re-touches the §8-A1 band-coverage acceptance line, so it is Matt's, via KR.

## Integrity ledger

- **Did NOT** edit `_DEFERRED_PROXY_BINS`, `check_infeasibility`, `bc_target_composer.py`, or
  `endgame_encounter_catalog.py`. Zero composition-behavior change landed.
- **Did** fold C1 (doc-only line-ref fix `:451`→`:67-68`) in the STEP-1 math-note.
- Did NOT touch `export/` (star-lord's TP1-3). All probes in-memory; zero files written by probes.

## Evidence commands (reproducible)

- Composer off the pilot path: `grep -rln "from .bc_target_composer|import bc_target_composer" src/` → 2 hits
  (`bc_target_source.py`, one smoke note); `grep -rln "bc_target_source" ...pipeline/driver/catalog` → empty.
- Pipeline has no gate: `grep -n "check_infeasibility|_DEFERRED_PROXY_BINS|compose_kit" season_generation_pipeline.py`
  → empty.
- Catalog distribution: 17 none / 1 light / 0 heavy (counted). Proxy-light cell emits n_proxies=1 (probe above).
- Driver generator: `w3_emission_driver.py:435` → `w5r1_generate_kit_candidates`; docstring `:370` names a
  non-existent un-gate step.
