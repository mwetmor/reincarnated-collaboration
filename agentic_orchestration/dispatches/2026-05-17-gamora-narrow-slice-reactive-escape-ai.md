# 2026-05-17 — gamora — Narrow-slice reactive escape AI (elite-tier monster repositioning)

**Status:** QUEUED — auto-spawn after gamora's current standard-demo regen ships.
**Authority:** Gandalf L3 § 7 binding decision (narrow-slice Phase-1 P1 extension per § 5.1).
**Type:** Pattern B (long task) — ~3-5 days.
**Predecessor:** gamora standard-demo regen (in flight) + rocket v1.7 schema fields (shipped).
**Seam:** simulation (gamora; AI movement logic during combat windows).

---

## Why this matters

Gandalf briefing § 4 + § 5.1: elite-tier monsters need to reactively escape player AOE telegraphs. Without this, the player perceives combat as "I drop an AOE and the monster just stands there and takes it" — substrate cosmologies that emphasize *positioning* (vortex_pull, cone push-out, persistent_zone vs burst) lose meaning when monsters don't move.

Narrow slice scope: **elite tier only.** Basic adds stay reactive-instant (no escape behavior). Mini-bosses + bosses + strategic + anticipatory escape are deferred to B13-proper post-VS2a.

---

## Required reading (in order)

1. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 4 (Monster AI escape behavior); § 5.1 (this work in scope)
2. Rocket v1.7 schema fields (`windup_duration_seconds` per substrate) — your timing reference
3. `reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` — current monster AI; you authored most of this; add escape behavior
4. `reincarnated-engine/src/reincarnated/simulation/fight_engine.py` (or equivalent) — fight resolver; AOE cast windows
5. `reincarnated-engine/src/reincarnated/generation/archetype_composer.py` — your D3 work; monster archetypes have role + substrate

---

## AMENDMENT 2 — 2026-05-17 (perception asymmetry per gandalf v1.5 § 4)

**Discipline #15 enforcement, perception-layer:** Per gandalf v1.5 binding § 8 — substrate-agnostic perception asymmetry at enemy 1.12× / player 0.90× apparent-vs-true ratio. Rocket v1.9 (in flight) ships `foundation/perception_asymmetry.py` with the constants.

**Added Item 6 (must integrate WITH Items 1-5):** Perception asymmetry consumption in fight resolver + AI.

### Item 6 (REQUIRED; added per amendment) — Perception asymmetry integration

**Goal:** Engine simulation gauntlet uses apparent_radius for AI escape decisions; damage resolves at true_radius. Telemetry emits both hit-counts per AOE cast.

**Fix:**
- Import from rocket v1.9: `foundation.perception_asymmetry.ENEMY_AOE_APPARENT_RATIO`, `PLAYER_AOE_APPARENT_RATIO`, `enemy_apparent_radius()`, `player_apparent_radius()`
- In fight_engine.py:
  - AOE damage resolution: continue using `true_radius` (no change from Item 0 logic)
  - Emit dual hit-count telemetry per gandalf § 4 (star-lord v1.4 defines the schema; gamora emits)
  - Per cast: compute `apparent_hit_count = combatants inside apparent_radius` AND `true_hit_count = combatants inside true_radius`
  - Per gandalf § 5: dual hit-counts feed D14 calibration
- In ai_strategies.py reactive-escape (Item 1-5):
  - Monster escape decision evaluates whether monster is inside apparent_radius (NOT true_radius)
  - Effect: monsters appear to escape just-barely (visual-aligned); some get caught by spillover at true_radius (which is larger for player AOEs)
- Player AOEs: `apparent_radius = true × 0.90` (smaller visual; more spillover hits — player feels effective)
- Enemy AOEs: `apparent_radius = true × 1.12` (larger visual; more "buffer" — player feels skilled at escape)

**Cosmological framing:** This is the perception-engineering pattern gandalf canonicalized in v1.5. Damage truth ≠ visual truth; intentional player-favoring fudge per Discipline #15 (engine + demo converge on same asymmetry contract).

**Acceptance for Item 6:**
- [ ] Imports from rocket v1.9 foundation/perception_asymmetry
- [ ] AOE damage resolution uses true_radius (unchanged)
- [ ] AI reactive escape uses apparent_radius (Item 1-5 logic operates on apparent_radius footprint)
- [ ] Dual hit-count telemetry emitted per AOE cast (using star-lord v1.4 schema)
- [ ] Unit tests for perception-asymmetric AI behavior (5+ tests)
- [ ] Existing tests continue to pass
- [ ] MIGRATION.md updated noting cross-seam consumption

---

## AMENDMENT 2026-05-17 (post-spawn; Matt-confirmed pillar)

**Discipline #15 enforcement:** Per Matt's 2026-05-17 sign-off pillar, any demo-added mechanic must have engine-simulation-gauntlet parity (except dodge dash, deferred per narrow-slice scope). Drax v1.0 introduced demo-side AOE ground indicators with substrate-coupled windup timing. **This dispatch must therefore also include explicit engine fight resolver windup-delay logic** — the gauntlet sim must model the same AOE cast-windup-then-resolve timeline as the demo, so monster reactive escape (this dispatch's primary work) has a window to operate in AND so engine-simulated KPM matches demo-playtest KPM.

**Added Item 0 (must complete BEFORE Items 1-5):** Engine fight resolver AOE windup support.

### Item 0 (REQUIRED; new per amendment) — Engine fight resolver AOE windup support

**Goal:** When an AOE skill is cast in the engine simulation gauntlet, damage resolves at the END of `windup_duration_seconds` (consumed from substrate identity declaration), NOT instantaneously at cast-start. Target combatants have a window to move out of the AOE footprint during the windup.

**Fix:**
- Audit `simulation/fight_engine.py` for AOE skill cast resolution logic
- For AOE geometries (circle / ground_targeted_circle / ground_slam / cone / ring / vortex_pull / whirlwind — match drax-demo's `noIndicatorGeoms` complement):
  - Cast-start: record AOE target position + footprint + windup_end_time = cast_time + substrate.windup_duration_seconds
  - Tick during windup: combatants can move; their position updates
  - Windup-end: re-evaluate footprint vs each combatant's CURRENT position; apply damage only to combatants STILL inside the footprint
- For non-AOE geometries (projectile / chain_lightning / etc.): existing instantaneous resolution unchanged
- Add fight_engine telemetry: `aoe_windup_started`, `aoe_windup_resolved` events with footprint + hit count
- Damage resolution uses the TRUE radius (post-asymmetry-design land; for now uses single radius)

**Why this matters for Items 1-5:** Without Item 0, the reactive escape AI has no escape window to operate in — AOE damage would resolve instantaneously, monster escape would be useless. Item 0 establishes the windup window; Items 1-5 leverage it.

**Acceptance for Item 0:**
- [ ] Fight engine AOE skills resolve damage at windup_end, not cast_start
- [ ] Combatants who move out of footprint during windup do NOT take damage at windup_end
- [ ] Unit tests for windup-delay behavior (5+ tests)
- [ ] Existing single-target / projectile skill resolution unchanged
- [ ] Existing 348+ sim tests continue to pass
- [ ] Telemetry events emit correctly

---

## Scope

### Item 1 — Elite-tier identification

**Define "elite tier":**
- Monsters with `monster_tier` ∈ {`elite`, `champion`} — or whatever conventions your monster schema uses
- NOT `basic` / `add` (lowest tier)
- NOT `mini_boss` / `boss` (highest tiers; deferred to B13-proper)

If monster_tier field doesn't exist explicitly, use a proxy:
- HP > 1.5x average → likely elite
- Damage > 1.5x average → likely elite
- Or: a fixed fraction of monsters per encounter (~25-30%) flagged as elite

Document the proxy logic in MIGRATION.md if applicable.

### Item 2 — Reactive escape behavior

**Trigger:** when player casts AOE skill with visible ground indicator (i.e., on cast-start, before windup completes)

**Decision logic:**
- Elite monster within AOE indicator footprint: perform escape behavior
- Probability: 50-70% per cast (not deterministic; gives variance + tactical reads)
- Escape direction: perpendicular to player-monster axis (creates flank read; cosmologically substrate-agnostic at narrow-slice tier)
- Escape distance: enough to clear the indicator footprint + ~1 tile buffer
- Escape duration: complete within `windup_duration_seconds` (consumed from substrate identity per the AOE's substrate)
- Escape interrupts: if monster is mid-attack-cast, escape preempts (intentional; tactical legibility — monster commits to escape over its attack)

**Decline-to-escape probability (30-50%):** monster stays; takes the hit. Gives player rewarding "got 'em" moments + variance.

### Item 3 — Integration with archetype_composer.py + ai_strategies.py

- Extend `ARCHETYPE_ROLE_PRIORITY` with escape-behavior entries OR add a separate `MONSTER_ESCAPE_BEHAVIOR` map
- The escape decision fires during the fight resolver's per-tick update; consumes the AOE's substrate (via `windup_duration_seconds` lookup) + indicator footprint
- Telemetry: emit `monster_escape_decision` event (monster_id, archetype_tag, decision: escape/stay, position before/after, frame); supports D14 calibration

### Item 4 — Tests

- Unit test: elite monster within AOE indicator → escape probability 50-70%
- Unit test: basic monster within AOE → no escape (no behavior change)
- Unit test: elite outside AOE → no escape
- Unit test: escape direction perpendicular to player-monster axis
- Unit test: escape clears indicator footprint + buffer
- Unit test: telemetry event emitted

### Item 5 — MIGRATION.md + AGENT_STATE.md

- `simulation/MIGRATION.md` §v3.X entry documenting:
  - New escape behavior + elite-tier identification proxy (if used)
  - Consumer obligations (drax narrow-slice consumes telemetry for VFX feedback; D14 consumes for calibration)
  - Discipline #1 (math-before-code): N/A (probability-based behavior; not new mechanic math)
  - Discipline #12 semantic shift: elite monsters now have positional intent
- Update `simulation/AGENT_STATE.md`

---

## Out of scope (DO NOT)

- ❌ DO NOT implement mini-boss / boss strategic + anticipatory escape (B13-proper)
- ❌ DO NOT implement substrate-coherent escape directions (B13-proper; narrow slice is substrate-agnostic perpendicular escape)
- ❌ DO NOT add escape behavior to basic adds (cognitive load on player; gandalf judgment)
- ❌ DO NOT add player-side mobility skills (B13-proper)
- ❌ DO NOT modify rocket schema files (consume only)
- ❌ DO NOT touch drax demo, loadout, or rocket-side foundation code
- ❌ DO NOT begin D10 code phase yet (still in your queue after this dispatch)

---

## Acceptance criteria

- [ ] Elite-tier identification logic (explicit field OR documented proxy)
- [ ] Reactive escape behavior implemented in ai_strategies.py
- [ ] 50-70% escape probability per cast
- [ ] Perpendicular escape direction
- [ ] Escape clears indicator + buffer within `windup_duration_seconds`
- [ ] Telemetry hook fires per decision
- [ ] Unit tests added (5-8 tests)
- [ ] Full test suite passes
- [ ] `simulation/MIGRATION.md` entry authored
- [ ] AGENT_STATE.md updated
- [ ] Hive-log STATE entry
- [ ] Tag `gamora/v1.5-narrow-slice-reactive-escape-ai-1`

---

## Smoke test expectation

- Run a fight where player drops an AOE on an elite monster → monster escapes 50-70% of the time
- Basic adds stay; do not escape
- Escape direction is perpendicular to player-monster line
- Telemetry events log correctly

---

## Cross-seam impact

- **Drax narrow-slice render** consumes the AOE indicator + dodge timing (Item 2 of drax narrow-slice); player perceives monsters moving as VFX feedback. Schema fields landed at rocket v1.7.
- **D14 mirror-match diversity gate** calibration uses escape telemetry as signal for "did substrates feel different in spatial combat" (per gandalf § 6.2).
- **D10 substrate-coherent generation** is your next dispatch after this; D10 acceptance can now include spatial-perception validation per gandalf § 6.4.

---

## Math-before-code requirements

N/A — probability-based behavior; no new mechanic math. Discipline #1 not triggered.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first. Apply broader pull-rebase discipline if engine-side concurrent commits possible (per gandalf 2026-05-17 OBSERVATION).

---

## Tag intent

`gamora/v1.5-narrow-slice-reactive-escape-ai-1` — seam-prefixed.

---

*Queued 2026-05-17 by knight-rider. Spawn after gamora's standard-demo regen ships. Estimated 3-5 days. Append completion record when done.*
