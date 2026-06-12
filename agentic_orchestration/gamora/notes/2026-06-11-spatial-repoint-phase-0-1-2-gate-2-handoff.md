# Gamora → Gate-2 Handoff — Spatial Re-Point Phases 0/1/2 (§ 3 protocol proving run)

**Date:** 2026-06-11
**Author:** gamora
**For:** jack-ryan (Gate-2, BLOCK authority) + KR (sequencing)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-11-gamora-spatial-repoint-recalibration-math-note.md` (completion record appended)
**Engine commits:** `5f2349f` (Phase 0), `5a7b079` (Phase 1), `2e77c28` (Phase 2)

## Disposition

Phases 0/1/2 of the kernel-change protocol's FIRST application are COMPLETE and committed in the
engine repo. **Phase 3 (implementation) is held at the Phase 2/3 boundary** pending Gate-2 approval
of the math-note — per Discipline #1 (math-note approved before code locks values against it) and
the dispatch's "Phase 3 — per APPROVED math-note only" gate. This is the math-before-code gate
doing its job, NOT a blocker-STOP.

## The STOP-clause assessment (key finding)

The dispatch named a hard-STOP condition: "the re-point reveals the resolver cannot serve spatial's
call pattern without kernel modification." **This did NOT fire.** The production spatial caller
(`balance_loop._run_spatial_slot:2625`) already holds the full `PlayerClass`/`Monster` Pydantic
objects and converts them DOWN to dicts (`model_dump()`) purely to feed the spatial engine's
dict-based interface. The resolver-ready objects are present at the call boundary — the resolver
CAN serve spatial without any kernel modification. The re-point is a clean caller-side change.

## What Gate-2 reviews

1. **Math-note** (`engine: simulation/math/spatial-repoint-recalibration-2026-06-11.md`) — six
   contents, measured/derived numbers, predicted-delta contract, recalibration form + target shape,
   re-gate bound, cost re-check trigger, PC-factor disposition.
2. **Phase 0 MIGRATION.md v1.64** — kernel interface declaration (satisfies Gate-1 Dimension-1 WARN).
3. **Phase 1 golden master** — 60-cell oracle, determinism proven, saturation baseline = the symptom.
4. **Semantic-shift declaration (Disc #12)** — spatial WR is no longer the same quantity post-re-point;
   decisions-log entry requested (continues the R-series recalibration lineage).

## Proving-run template (jack-ryan assessment requested per dispatch § Gate-2)

Offered as the reusable § 3 template for subsequent kernel changes (id-substrate rebuild next):
- **Corpus fix:** N + scenarios + archetypes + seed-pin + committed-oracle + self-verify determinism.
- **Predicted-delta convention:** direction = the contract; magnitude = recalibrated to target shape;
  explicit negative non-movement contract; `verify` exit-1 = "predicted-or-STOP" trigger.
- **Re-gate bound model:** `N·C_s·(1 + F·g)` with assumptions flagged ASSUMED until measured;
  production scheduling gated on the bound existing.
- **Corpus-archetype-coverage constraint (Disc #11):** name what the corpus CANNOT exercise (here:
  pre-T4, so chaos_immune/three-path flips are a SEPARATE follow-on corpus, predicted but not verified).

## Queued behind Gate-2 (Phase 3/4)
- Phase 3: adapter (`PlayerClass`/`Monster` → `CombatantState`+`Skill`, threaded through
  `entity_from_class_dict`/`entity_from_monster_dict` — a signature change across the spatial call
  path) + `_apply_skill_damage` re-point + recalibration sweep (locks `SPATIAL_DAMAGE_SCALE`).
- Phase 4: 60-cell golden-master verify (every delta predicted-or-STOP) + telemetry tag (Disc #7).
- PC parallel-factor: SEPARABLE sub-task behind the manifestation spike wave (12× remains ASSUMED).
- T4-bearing golden-master follow-on for the chaos_immune/three-path flip verification.

## Star-lord flag (fired — notification only)
`simulate_fight(...)->FightResult` is now formally named in MIGRATION.md v1.64. No schema field
change in Phases 0–2. Principle-6 watch into Phase 3: `resolve_skill` returns `(damage, events)`;
default is to DROP events (information parity with the simplified model). Carrying events into
telemetry later = a declared cross-seam change.
