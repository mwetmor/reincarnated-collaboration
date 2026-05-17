# 2026-05-17 — rocket — Perception asymmetry module + cross-language TS constants

**Authority:** Gandalf L3 § 8 binding decision per Matt L3 standing delegation 2026-05-17.
**Type:** Pattern A (short task) — ~0.5 day.
**Predecessor:** gandalf v1.5 asymmetric perceived AOE radius briefing (`gandalf/v1.5-asymmetric-perceived-aoe-radius-briefing-1` @ `6733866`).

---

## Why this matters

Per gandalf § 8 binding recommendation: substrate-agnostic perception asymmetry at **enemy 1.12× / player 0.90×** (genre centroid; D3 RoS / D4 / LE-documented). Two scalars at engine config root. Damage resolves at true_radius; AI + rendering use apparent_radius. **Discipline #15 enforcement:** demo + engine sim both honor the same asymmetry contract.

This dispatch creates the foundation layer. Gamora, drax-demo, and star-lord all consume from here.

---

## Required reading (in order)

1. `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` — full briefing; § 4 implementation contract (your scope) + § 7 numerical parameters
2. `reincarnated-engine/src/reincarnated/foundation/substrate_identity_loader.py` — pattern for foundation-level config modules
3. `reincarnated-engine/src/reincarnated/foundation/__init__.py` — exports
4. `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — your prior §v3.x entries

---

## Scope

### Item 1 — New module `foundation/perception_asymmetry.py`

Author a new Python module:

```python
# foundation/perception_asymmetry.py
"""
Player-favoring perception asymmetry constants.

Per gandalf L3 binding v1.5: enemy AOE radius appears 1.12× true;
player AOE radius appears 0.90× true. Damage resolves at true_radius;
AI decisions + visual rendering use apparent_radius.

Genre centroid: D3 RoS / D4 / Last Epoch convergence (Wyatt Cheng
"favor the player" design philosophy).
"""

ENEMY_AOE_APPARENT_RATIO: float = 1.12
PLAYER_AOE_APPARENT_RATIO: float = 0.90

def enemy_apparent_radius(true_radius: float) -> float:
    """Convert enemy AOE true radius → apparent (rendered/AI-perceived)."""
    return true_radius * ENEMY_AOE_APPARENT_RATIO

def player_apparent_radius(true_radius: float) -> float:
    """Convert player AOE true radius → apparent (rendered/AI-perceived)."""
    return true_radius * PLAYER_AOE_APPARENT_RATIO
```

Plus fail-loud validation: if either constant falls outside reasonable bounds (e.g., 0.5-2.0 sanity check), raise at module load.

### Item 2 — Export from foundation/__init__.py

Update `foundation/__init__.py` to export:
- `ENEMY_AOE_APPARENT_RATIO`
- `PLAYER_AOE_APPARENT_RATIO`
- `enemy_apparent_radius`
- `player_apparent_radius`

### Item 3 — Cross-language TS constants

Per gandalf § 4 cross-language parity requirement: drax-demo (TypeScript) needs the same constants. Two paths:

**Path A (recommended):** Author `reincarnated-engine/src/reincarnated/foundation/perception_asymmetry.constants.ts` (or wherever the engine-emitted TS-constants pattern lives) that mirrors the Python constants. Drax-demo imports this.

**Path B:** Author the constants directly in `reincarnated-demo/src/data/` and ensure they match Python. Use jack-ryan validation to enforce parity.

**Decision:** Use whichever pattern already exists in the engine for cross-language constant sharing. If neither pattern exists, default to Path B (TS constants in demo + jack-ryan parity check) — simpler for Phase-1 P1; refactor to Path A in Phase-2 if cross-language constants become a recurring pattern.

If you choose Path A, author the TS file alongside the Python module.
If you choose Path B, document the TS-file location requirement in MIGRATION.md so drax-demo knows where to land them.

### Item 4 — Tests

- Unit tests for `enemy_apparent_radius` + `player_apparent_radius` (basic input/output)
- Boundary test for the sanity-check fail-loud (out-of-range constants)
- Integration test: confirm exports work from `foundation/__init__.py`

### Item 5 — MIGRATION.md §v3.4

Author `generation/MIGRATION.md` §v3.4 entry documenting:
- New module + constants
- Discipline #15 satisfaction (engine + demo both use same asymmetry contract)
- Consumer obligations:
  - Gamora: AI escape decisions use apparent_radius; damage resolves at true_radius; emit dual hit-count telemetry
  - Drax-demo: indicator rendering uses apparent_radius
  - Star-lord: telemetry schema carries dual hit-counts
- Discipline #12 semantic shift: perception ≠ damage; intentional player-favoring fudge
- Future Phase-2 expansion: substrate-coupled asymmetry (gandalf § 8 deferred path)

---

## Out of scope (DO NOT)

- ❌ DO NOT implement substrate-coupled asymmetry (Phase-2; gandalf § 8 deferred)
- ❌ DO NOT modify gamora's simulation logic (gamora consumes constants; separate dispatch)
- ❌ DO NOT modify demo or loadout code (different seams)
- ❌ DO NOT change substrate identity declarations (this is a foundation-root config, not substrate-specific)
- ❌ DO NOT add other perception fudges (monster damage scaling, hit-detection forgiveness, etc.) — Phase-2 design surfaces

---

## Acceptance criteria

- [ ] `foundation/perception_asymmetry.py` module authored
- [ ] Constants: ENEMY_AOE_APPARENT_RATIO=1.12, PLAYER_AOE_APPARENT_RATIO=0.90
- [ ] Helper functions: enemy_apparent_radius(), player_apparent_radius()
- [ ] Fail-loud sanity-check validation on constants (out-of-range raises)
- [ ] Exports from `foundation/__init__.py`
- [ ] Cross-language TS constants (Path A or Path B)
- [ ] Unit tests added
- [ ] Full test suite passes
- [ ] `generation/MIGRATION.md` §v3.4 entry authored
- [ ] Hive-log STATE entry + HANDOFFs (gamora / drax-demo / star-lord)
- [ ] Tag `rocket/v1.9-perception-asymmetry-module-1`

---

## Smoke test expectation

- `python -c "from reincarnated.foundation import ENEMY_AOE_APPARENT_RATIO, PLAYER_AOE_APPARENT_RATIO; print(ENEMY_AOE_APPARENT_RATIO, PLAYER_AOE_APPARENT_RATIO)"` outputs `1.12 0.9`
- `python -c "from reincarnated.foundation import enemy_apparent_radius; print(enemy_apparent_radius(100.0))"` outputs `112.0`
- TS file: drax-demo can import + use the same values (parity)
- All existing tests pass

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first. Pull-rebase before engine-repo commits (concurrent agent activity expected).

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 standing delegation + gandalf § 8 binding. Estimated 0.5 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `rocket/v1.9-perception-asymmetry-module-1` @ engine `430236f`; demo `4cc7b89`

### Acceptance criteria status

- [x] `foundation/perception_asymmetry.py` module authored
- [x] Constants: ENEMY_AOE_APPARENT_RATIO=1.12, PLAYER_AOE_APPARENT_RATIO=0.90
- [x] Helper functions: enemy_apparent_radius(), player_apparent_radius(), get_apparent_radius()
- [x] Fail-loud sanity-check validation on constants (out-of-range raises at module load via _validate_constants())
- [x] Exports from `foundation/__init__.py` (5 symbols + __all__)
- [x] Cross-language TS constants — Path B chosen: `reincarnated-demo/src/data/perceptionAsymmetry.ts`
- [x] Unit tests added — 44 tests, all pass; 481 total foundation tests pass
- [x] Full test suite passes (foundation + substrate + role + ailment suites clean)
- [x] `generation/MIGRATION.md` §v3.4 entry authored with full per-seam consumer obligations
- [x] Hive-log STATE + HANDOFFs (gamora / drax-demo / star-lord / jack-ryan) appended
- [x] Tag `rocket/v1.9-perception-asymmetry-module-1`

### Path B rationale

Demo already uses `src/data/substrateIdentity.ts` as the cross-language constants pattern for substrate YAML mirror values. No engine-emitted TS generation infrastructure exists. Path B (TS constants in demo + jack-ryan parity check) is consistent with the existing precedent and simpler for Phase-1 P1.

### Notes

- Smoke tests from dispatch spec: `print(1.12 0.9)` ✓; `enemy_apparent_radius(100.0) == 112.0` ✓
- Fail-loud boundary: `_validate_constants()` tested via module-level patch; 4 out-of-range cases + 3 valid-boundary cases all pass
- Prior demo indicator magnitudes were 1.08×/0.92× (post-B11 lock). Drax consumer obligation: update to 1.12×/0.90× from `perceptionAsymmetry.ts`. That work is in drax's seam (HANDOFF filed).
- Telemetry fields (`aoe_true_radius_hit_count`, `aoe_apparent_radius_hit_count`) are gamora + star-lord obligations (HANDOFFs filed); not authored here per dispatch scope.

— rocket
