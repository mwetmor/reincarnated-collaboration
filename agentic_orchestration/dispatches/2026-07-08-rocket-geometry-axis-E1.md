# Dispatch — rocket: Geometry-widening axis (E1, first axis of the full-spec main line)

**From:** knight-rider → **To:** rocket (generation seam)
**Date:** 2026-07-08
**Pattern:** B (multi-hour build; math-before-code) — **Gate-1 (jack-ryan) REQUIRED before fire**
**Authority:** Matt-ratified full-run pivot 2026-07-08. E1 ruled **FLIP → IN-FLIGHT** (surface-ledger, first axis). Transmission: `agentic_orchestration/gandalf/notes/2026-07-08-kr-retransmission-full-run-pivot.md` § 4 action 2.
**Status:** DRAFT — awaiting jack-ryan Gate-1. Do NOT execute until Gate-1 PASS is recorded.

---

## 0. Why this axis exists (the trivialization it closes)

Source-verified this session (surface-ledger **E1**): the live kit-gen path emits a **certification
lattice, not a build-diversity population.** The headline bottleneck is ONE rocket-side table —
`_BC_AMPLITUDE_TO_GEOMETRY` (`generation/per_skill_emitter.py:215-219`) collapses ALL of a kit's
skill geometry to **3 shapes** (spiky→single_target / sustained→small_aoe / flat→large_aoe), and it
is applied **once per kit** (`:585` — `geometry_type = _BC_AMPLITUDE_TO_GEOMETRY.get(config.bc_amplitude, ...)`),
so all 12 skill slots share one shape. Meanwhile the SIM SIDE already resolves a **24-type rich
geometry vocabulary** (`_RICH_TO_SPATIAL`, `simulation/spatial_gauntlet/spatial_engine.py:404`) with
**B11 per-geometry mechanics** already implemented (`simulation/damage_resolver.py:85-139` — chain
decay 0.7, fork 0.6, multiproj 0.65, ring 1.2×, leap 1.3×, i-frame window). **The sim is NOT the
bottleneck — it already consumes the rich palette.** The build was narrowed on the emitter side only.

This axis widens the emitter to emit **per-skill geometry drawn from the rich vocabulary the sim
already resolves.** Matt's words: *"I Don't want only 3 skills and I cringe to think of what else was
trivialized in the name of 'sprint to Demo.'"*

## 1. Target seam + the change

- **File:** `generation/per_skill_emitter.py` (yours). No sim-side change — the sim already resolves
  the rich vocabulary (that is the point).
- **The change:** per-skill geometry assignment over the rich `_RICH_TO_SPATIAL` vocabulary, replacing
  the single-shape-per-kit collapse. A kit's 12 skill slots should express a **distribution** of
  geometries appropriate to each skill's kernel/role/element, not one shape cloned twelve times.

## 2. MATH-BEFORE-CODE (Discipline #1) — REQUIRED, precedes any code

Author a math note (`generation/math/geometry-axis-e1-<date>.md`) BEFORE code. It must answer the
design question this axis opens:
- **Which rich geometries** from `_RICH_TO_SPATIAL`'s 24 keys are in-scope for player-skill emission,
  and **what assigns each skill its geometry** (by kernel? role-split? element? amplitude-as-one-input-
  among-several?). The current single input (`bc_amplitude`) is insufficient for per-skill variety —
  name the new assignment basis and justify it.
- **Balance-spine preservation:** the tier curve stays the balance spine (E2 note — economy scalars are
  a SEPARATE axis; do NOT touch `BASE_SPELL_DAMAGE_L50` here). Show the geometry widening does not
  smuggle in a damage-magnitude change — B11 mechanics are multipliers the sim applies, so widening
  geometry SHIFTS effective throughput; name that shift and confirm it is the intended axis effect, not
  an accidental balance move. (This is exactly why C3 band re-fit `gates-on: E1` — see § 6.)
- **Vocabulary-subset proof:** every geometry value you emit MUST be a key the sim's `_RICH_TO_SPATIAL`
  recognizes (else it falls to the degraded Path-3 fallback — see `f1-geometry-fieldname-reconciliation-
  2026-06-17.md`). Enumerate your emitted set ⊆ the 24 sim keys.

## 3. HARD EXCLUSION — movement verbs (Matt-ruled OUT of this axis)

**dash / blink / teleport / leap-as-mobility and any movement-verb geometry are EXCLUDED.** They ride
the **parked F4-martial fork** (post-Leg-ii, evidence-shaped — kit-side mobility is the PoE-true F4
answer, ruled separately). `leap_strike` as a *damage-geometry* landing-burst multiplier (B11
`_LEAP_DEFAULT_LANDING_MULT`) is a damage shape, NOT a mobility verb — if you include it, include it as
damage geometry only, with no movement/exit-window semantics. When in doubt, exclude and flag.

## 4. Cross-seam discipline (ADR-004 + Review Principle 6)

- No sim contract CHANGE is expected (you emit within the already-accepted `_RICH_TO_SPATIAL`
  vocabulary). **If** your math note concludes you need a geometry key the sim does not map, that is a
  cross-seam contract change → **MIGRATION.md + Matt before tagging**, and it likely belongs in a
  separate dispatch (gamora owns `_RICH_TO_SPATIAL`).
- **Round-trip smoke is MANDATORY** (Principle 6): a generated kit's emitted geometry values → the sim's
  `_RICH_TO_SPATIAL` → a real spatial class → the B11 mechanic fires. Prove the round-trip end-to-end,
  not just that the emitter wrote richer strings.

## 5. #2-FF fields (MANDATORY — eat our own cooking, per transmission § 4.2)

- **Verdict-rendering instrument named:** the round-trip smoke (§4) + a **distribution check** — a
  generated kit's 12 slots now express **>3 distinct geometries** (the pre-change state was ≤3, one per
  kit), every emitted value ∈ `_RICH_TO_SPATIAL` keys, zero movement verbs.
- **One-command pre-fire verification:** a single command proving the pre-change baseline, e.g.
  `python -c "from reincarnated.generation.per_skill_emitter import _BC_AMPLITUDE_TO_GEOMETRY; print(len(set(_BC_AMPLITUDE_TO_GEOMETRY.values())))"` → `3` (the collapse you are widening). State the
  expected post-change first-log line (e.g. "kit <id>: N distinct geometries across 12 slots, all ∈ RICH").
- **Precondition state cited:** surface-ledger E1 (`canonical/current-to-end-state/surface-ledger.md`);
  four-rulings authority (`gandalf/notes/2026-07-08-full-run-pivot-four-rulings.md`); this transmission
  (`gandalf/notes/2026-07-08-kr-retransmission-full-run-pivot.md`).

## 6. Acceptance criteria

1. Math note lands FIRST (Discipline #1), answering § 2.
2. `per_skill_emitter.py` emits per-skill geometry over the rich vocabulary; a kit's 12 slots express a
   distribution (>3 distinct geometries), each value ∈ `_RICH_TO_SPATIAL`, movement verbs excluded.
3. Round-trip smoke passes (emitted geometry → sim resolves → B11 mechanic fires) with output captured.
4. #2-FF fields present in the commit/run banner.
5. Tag `rocket/v<X.Y>-geometry-axis-1` (seam prefix — intermediate; Matt approves any prefix drop).

## 7. Explicitly OUT OF SCOPE (prevents scope creep)

- **E2 economy scalars** (`BASE_SPELL_DAMAGE_L50`, energy/cooldown/cast tables) — separate queued axis.
- **E3 hybrid dual-scaling** — separate queued axis, needs a gandalf design pass first.
- **E4 timing variety** (cast-time/wind-up/charge) — separate queued axis.
- **Movement verbs** — F4-martial fork (§ 3).
- **KPM band re-fit** — that is C3 (`gates-on: E1`); it fires AFTER this axis lands, on the
  geometry-widened population, at bands re-fit to the new declared baseline (gamora/jack-ryan seam).
  Do NOT touch band tables.
- **Sim-side `_RICH_TO_SPATIAL` / B11** — already resolves the vocabulary; not your file, no change.

## 8. Downstream consequence (for awareness, not action)

When this lands, the population regenerates at a new declared baseline → **C3 band re-fit fires**
(`gates-on: E1`) → the content-bearing per-axis pilot re-runs on the geometry-widened population at the
re-fit bands. That sequencing is KR-orchestrated; your deliverable is the emitter widening + the
round-trip proof.

---

**Required reading (rocket, at session start):**
1. This dispatch.
2. `canonical/current-to-end-state/surface-ledger.md` — E1 row (your axis) + the survey-mode discipline.
3. `agentic_orchestration/gandalf/notes/2026-07-08-full-run-pivot-four-rulings.md` — why the main line is per-axis.
4. `simulation/math/f1-geometry-fieldname-reconciliation-2026-06-17.md` — the `_RICH_TO_SPATIAL` two-key contract (so your emitted values round-trip, not fall to Path 3).
5. `simulation/damage_resolver.py:85-139` — the B11 mechanics your geometries will trigger.

**Sign-off:** knight-rider, 2026-07-08 (DRAFT — Gate-1 pending). Fires on jack-ryan Gate-1 PASS.
