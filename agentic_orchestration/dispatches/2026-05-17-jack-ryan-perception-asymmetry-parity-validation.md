# 2026-05-17 — jack-ryan — Perception asymmetry cross-language parity + tuning-drift discipline

**Authority:** Gandalf L3 § 8 binding + rocket v1.9 module ship.
**Type:** Pattern A — ~0.25 day.
**Predecessor:** rocket v1.9 perception_asymmetry module shipped (`rocket/v1.9-perception-asymmetry-module-1`).

---

## Why this matters

Rocket v1.9 chose Path B for cross-language constants (TS constants in demo + parity-check discipline). Your job:
1. Validate the Python (engine) and TypeScript (demo) constants are byte-identical
2. Author the tuning-drift discipline entry per gandalf § 5.4 (factor changes require gandalf sign-off)
3. Add the parity check to the continuous-observation rhythm

---

## Required reading

1. `reincarnated-engine/src/reincarnated/foundation/perception_asymmetry.py` — Python truth
2. `reincarnated-demo/src/data/perceptionAsymmetry.ts` — TS mirror
3. `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` § 5.4 — tuning-drift discipline framing
4. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — your destination for new discipline entry

---

## Scope

### Item 1 — Parity validation

- Diff the Python and TS files
- Confirm constants are numerically identical (1.12 and 0.90 both sides; bounds [1.08-1.18] / [0.85-0.93] both sides)
- Confirm helper function semantics match (enemy_apparent_radius vs enemyApparentRadius; player_apparent_radius vs playerApparentRadius; get_apparent_radius vs getApparentRadius with same owner strings)
- Document validation result in hive log

### Item 2 — Tuning-drift discipline entry

Author an entry in `engineering-disciplines.md` capturing:

> **Tuning-drift discipline (perception asymmetry):** The `ENEMY_AOE_APPARENT_RATIO` and `PLAYER_AOE_APPARENT_RATIO` constants in `foundation/perception_asymmetry.py` AND the mirror TS constants in `reincarnated-demo/src/data/perceptionAsymmetry.ts` are gandalf-authoritative. Both must remain within genre-centroid bounds (enemy [1.08, 1.18] / player [0.85, 0.93]) per gandalf v1.5 briefing § 5.4. Cross-language parity is structural. Changes require: (a) gandalf sign-off via L3 briefing amendment; (b) both Python + TS updated in same commit; (c) jack-ryan continuous-observation re-validation. Drift outside bounds raises at engine module load via `_validate_constants()`; demo doesn't enforce hardcoded bounds but should reference the discipline.

(Format-match existing disciplines #11/#12/#13/#15 in the doc.)

### Item 3 — Continuous-observation rhythm extension

- Add a watchpoint: WP-N "perception_asymmetry constants drift check"
- On every checkpoint review, verify Python + TS constants still parity + still within bounds
- Append to `agentic_orchestration/hive-mind/watchpoints-2026-05-17.md`

### Item 4 — Hive log + tag

- STATE entry capturing parity result + discipline entry + watchpoint
- Tag `jack-ryan/v1.1-perception-asymmetry-parity-validation-1`

---

## Acceptance criteria

- [ ] Parity diff complete; both files numerically aligned
- [ ] Tuning-drift discipline entry authored in engineering-disciplines.md
- [ ] Watchpoint added
- [ ] Hive-log STATE entry
- [ ] Tag `jack-ryan/v1.1-perception-asymmetry-parity-validation-1`

---

*Dispatched 2026-05-17 by knight-rider per cascade auto-execution. ~0.25 day. Append completion record when done.*

---

## Completion record — 2026-05-17 — jack-ryan

**Status:** COMPLETE
**Tag:** `jack-ryan/v1.1-perception-asymmetry-parity-validation-1`
**Engine commit:** `d99cbc0` (Discipline #16 authored)
**Collaboration commit:** `4877f58` (hive log STATE + WP-12)
**Elapsed:** ~0.25 day (within estimate)

### Item 1 — Parity validation: PASS

Python `ENEMY_AOE_APPARENT_RATIO = 1.12` matches TypeScript `ENEMY_AOE_APPARENT_RATIO = 1.12`. Python `PLAYER_AOE_APPARENT_RATIO = 0.90` matches TypeScript `PLAYER_AOE_APPARENT_RATIO = 0.90`. Helper function semantics (`enemy_apparent_radius` / `enemyApparentRadius`, `player_apparent_radius` / `playerApparentRadius`, `get_apparent_radius` / `getApparentRadius`) are byte-semantically identical: same dispatch pattern, same fail-loud unknown-owner behavior. One acceptable structural difference: TypeScript does not replicate `_validate_constants()` or bound constants — Python is the authoritative fail-loud layer by Path B design.

### Item 2 — Discipline #16: AUTHORED

`engineering-disciplines.md` Discipline #16 "Tuning-drift discipline (perception asymmetry)" appended after #15. Format-matches existing numbered disciplines. Gates factor changes behind: (a) gandalf sign-off, (b) same-commit cross-language update, (c) jack-ryan re-validation. Runtime guard (`_validate_constants()`) noted as structural enforcement. Gate-1 question added.

### Item 3 — WP-12: ADDED

`watchpoints-2026-05-17.md` WP-12 "Perception-asymmetry constants drift check (Discipline #16)" appended. Baseline table confirmed at current values. Active observation queue updated.

### Deferred (post-gamora)

KPM gauntlet spillover-ratio validation (briefing § 5.3 items 14-15) is blocked on gamora reactive-escape AI landing. Will surface as WP-12 sub-item at that checkpoint.
