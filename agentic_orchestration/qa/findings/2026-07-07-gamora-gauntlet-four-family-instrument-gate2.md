# Finding — 2026-07-07 — Q11 four-family gauntlet instrument (Lane 1 build)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-FOLLOWUPS (no BLOCK)
**Target:** commit `8d45f95` / tag `gamora/v-batch2-gauntlet-four-family-instrument-1` (math note `657524a`) — NOT pushed
**Developer:** gamora (simulation seam)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam MIGRATION), 4 (decisions-log truth), 6 (cross-seam round-trip); Disciplines #1, #2, #3, #11, #12

## What I found

Verified against SOURCE, not smoke output. Every load-bearing claim in the submission holds. Discipline #1 satisfied — math note `657524a` (09:53) precedes code `8d45f95` (10:15) and is substantive (populations, spawn-cadence math, HP-at-TTK design mapping, compute-cost bounds). Guardrails honored: the three frozen constants (`SPATIAL_DAMAGE_SCALE`, `MOB_HP_DIFFICULTY_MULTIPLIER`, `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6`) show ZERO assignment-line delta in the diff (grep `^[+-].*CONST *=` returns empty). §3 dims read verbatim: `dense_cell` 16×22 (arena.py:946-947), re-based `open_arena` 36×36 (:453-454), `escape_lane` 60×16 mapped to the y-axis as forward-direction (width_m=16/height_m=60, escape_threshold_m=58 on escape_axis="y" — the spec's "60×16 lane" expressed with 60 as the run-length; NOT an invented dim). Nothing deleted: all six original rooms present, wall preserved as `open_arena_wall_diag` (:401), two new canonical rooms registered. Champion-elevation is a post-multiply on the existing `spatial_dm` seam (spatial_engine.py:3307 unchanged; :3314-3316 applies `escape_elevation_multiplier`, default 1.0 = inert) — not a constant change and not a pass/fail threshold. R4 sequencing is correct: `gauntlet_pass()` still returns the legacy 9-of-18 floor (gauntlet_sim.py:854, behavior unchanged); `family_certification_pass()` (:785) encodes the retired-carve-out contract but is exported-only via `to_dict()` (`families_passed`/`four_family_cert`), NOT wired to the ship gate — the one-line flip is explicitly Lane 3's. This avoids silently breaking the paused Step-3 sequence. I re-ran (did not trust GREEN): build smoke PASSES (F4 spawner fires 27 reinforcements, escape resolves to win, all four families instantiate + run end-to-end); 233 tests across the 7 named suites + 70 in `round_trip_spatial_telemetry` all PASS, zero regressions.

**`mobs_killed=0` assessment (review priority 3):** SOUND call, not masking a build defect. The counter reads 0 on F1/F2/F3 AND F4 alike in the smoke — i.e. it reproduces on the KNOWN-GOOD re-based rooms, not just the new F4. That is the signature of a smoke-fixture DPS artifact (the flat synthetic `smoke_functional_kit` DPS path does not register kills in-window), exactly as gamora framed it. Room mechanics ARE proven independently: `aoe_hits > 0` in all four rooms (geometry lands, mobs reach the player), F4 escape resolves, F4 spawner mints reinforcements. Kill-count calibration is a Lane-3 / DPS-fixture concern. Not an F4-specific signal, therefore not a room defect.

## Rationale

- **Principle 1 / Disc #1:** math note precedes code, is non-trivial, and fences instrument-parameters from bars. PASS.
- **Principle 2 / Disc #2:** build-smoke present, GREEN, re-run by reviewer. PASS.
- **Principle 3 + 6 / ADR-004 / Disc #12:** MIGRATION.md v1.84 correctly classifies the change as a PRODUCER change on the star-lord telemetry boundary and enumerates consumer obligations. See cross-seam determination below.
- **Principle 4 / Disc #12:** three semantic shifts (R4 certification contract; `open_arena` re-base; `mobs_killed` range) are framed in the note §7, the commit body, and MIGRATION v1.84 — routed to me for decisions-log. I own these entries (followup 1).
- **Disc #11:** all claims verified against source; no assumption trusted.

## Cross-seam determination (review priority 1) — star-lord action NOT required before this is safe

The two new fields (`escape_reached: bool = False`, `continuous_spawned_total: int = 0`) are genuinely additive/brownfield-safe. Verified via source: they follow the established defaulted-optional pattern (`total_displacement`/`boss_*`), are NOT `validate()`-enforced, and are NOT persisted by the positional SQLite `_INSERT_SQL` (no schema write until a migration lands). The six existing scenarios emit `False`/`0` byte-identically (injection path never fires without `continuous_spawn`). `winner` stays in the existing {player, monster, timeout} set. The `mobs_killed` range shift is correctly documented as scoped to `scenario_id == "escape_lane"` (or any continuous-spawn scenario); for the six existing rooms `mobs_killed ≤ total_mob_count` still holds byte-identically.

**Verdict: a note suffices; no star-lord dispatch is a precondition for this build being safe.** These fields are producer-emitted only and consumed by nothing today (Lane-3 metrology reads them in-process; the export pipeline does not yet touch them). star-lord's obligations (widen SQLite schema + `_INSERT_SQL`; relax the `mobs_killed ≤ total_mob_count` invariant for continuous-spawn scenarios) become live ONLY when Lane-3 metrology or the export pipeline needs these on-disk — a future event, cleanly captured in MIGRATION v1.84's "What star-lord owes" section. KR does not need to dispatch star-lord for this commit to land.

## Action

- [x] jack-ryan: Gate-2 review complete — verified against source, re-ran smoke + regression.
- [ ] jack-ryan: file the three Discipline-#12 decisions-log entries (R4 certification-contract shift; `open_arena` re-base; `mobs_killed` range) — my owed followup, non-blocking on this tag. (Deferred with the Lane-3 metrology pass per the pending gandalf spec-amendment; entries land alongside bar derivation so the log reflects the certifiable end-state.)
- [ ] star-lord (FUTURE, non-blocking): when Lane-3 or export needs F4 telemetry on-disk, action MIGRATION v1.84 "What star-lord owes" (1)+(2). NOT required before this build is safe.
- [ ] Matt (milestone-gate only, NOT this tag): the R4 one-line flip (`gauntlet_pass` → `family_certification_pass`) is Lane 3's and lands with derived bars; it is NOT in this commit.

## References

- `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (R4: :771-785 family_certification_pass, :812-854 gauntlet_pass, :856-882 to_dict export)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (dims :453-454/:946-947/:1013-1060; registries; :401 wall diag)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (elevation seam :3307/:3314-3316; F4 spawner + F3 timed-wave injection)
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.84 (:8363-8394)
- `reincarnated-engine/src/reincarnated/simulation/math/gauntlet-four-family-instrument-build-2026-07-07.md`
- `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §3/§4/§5/§6/§7
- Build smoke: `spatial_gauntlet/_build_smoke_four_family.py` (re-run GREEN by reviewer)
- Regression: 7 named suites (233 pass) + `round_trip_spatial_telemetry` (70 pass), zero regressions
