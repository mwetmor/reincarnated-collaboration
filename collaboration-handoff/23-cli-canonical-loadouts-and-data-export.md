# CLI Session Prompt — Canonical Loadouts + Priority 04 Verification + Data Export

**Captured:** 2026-05-10
**Working repo:** `/Users/admin/Games/reincarnated-engine/`
**Estimated total:** ~2 weeks (1.5 CPs for canonical loadouts + ~1 week for data export + small Priority 04 task)

This is a multi-phase CLI session. Three sequential phases with clear stop-and-report gates between each. The phases are ordered so each builds on the previous one's output.

## How to use

Paste the entire prompt below into a fresh Claude Code session opened at the engine repo. The CLI will work through the three phases sequentially, stopping for review at each gate.

---

## The prompt

```
This is a combined three-phase CLI session for the post-Priority-02 successor work. Read the entire prompt before starting any phase. Each phase has a clear stop-and-report gate.

═════════════════════════════════════
Required reading before any work begins
═════════════════════════════════════

1. `CLAUDE.md` (engine repo root) — operational orientation
2. `design/decisions/decisions-log.md` — read the 2026-05-10 entries from Priority 02 CP10 wrap-up
3. `design/planning/current-phase.md` — confirm Priority 02 is closed and what's queued
4. `notes/sessions/2026-05-09-priority-02-gear.md` — the Priority 02 session note for context on what was just built
5. `/Users/admin/Games/reincarnated-collaboration/canonical/16-project-roadmap.md` — current critical path
6. `/Users/admin/Games/reincarnated-collaboration/canonical/17-gear-and-spirit-guide-design.md` — gear architecture (substantially updated through Priority 02)
7. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/22-three-js-demo-and-data-export.md` — the data export + demo plan; demo1 depends on the carried_gear feature being in place
8. Code surfaces this session will touch:
   - `src/reincarnated/balance/balance_loop.py` — convergence loop; needs per-fight loadout persistence
   - `src/reincarnated/generation/gear_generation.py` — gear pool, sample_scenario_loadout
   - `src/reincarnated/generation/season_orchestrator.py` — where canonical loadout selection will run
   - `src/reincarnated/telemetry/recorder.py` + `migrations.py` — schema for new persistence
   - `src/reincarnated/llm/naming.py` — naming pipeline (for Priority 04 verification context)

Branch: `work/canonical-loadouts-data-export` (or whichever name fits the repo's branch convention).

═════════════════════════════════════
Phase 1 — Canonical loadouts engine feature (~1.5 CPs)
═════════════════════════════════════

Goal: convergence loop persists per-fight loadout details; post-convergence, a canonical loadout selection step identifies the best-performing loadout per class; each class's `carried_gear` is populated from its canonical loadout.

This is the load-bearing feature that gives demo1 its boss-drops-gear mechanic with real narrative provenance. Both regular playable classes AND act-boss classes get carried_gear.

**Three workstreams:**

1. **Per-fight loadout persistence (schema + recording).**

   - New telemetry table — name suggestion: `class_fight_loadouts`, with columns:
     * `id` (PK), `season_id`, `class_id`, `monster_id`, `iteration` (which binary-search iteration of convergence), `fight_index` (which fight within the iteration's batch), `loadout` (JSON or normalized — your call: list of gear_instance_ids per slot, plus handedness flag), `outcome` (won / lost), `legendary_count` (denormalized for selection efficiency), `damage_dealt`, `damage_taken` (or whatever fight-outcome metadata is cheaply available)
   - Migration version bump to 1.8 (or whatever's next).
   - Storage cost estimate: ~3000 fights/class × ~100 bytes/row × ~10 classes/season ≈ ~3 MB/season. Well within budget.
   - Wire `BalanceLoop` to record each fight's loadout + outcome during `run_batch_geared()`. The loadout is already constructed for the fight; just persist it instead of discarding.
   - Backward compat: existing seasons without per-fight loadout data have empty `class_fight_loadouts` rows; canonical loadout selection skips them gracefully (returns None).

2. **Canonical loadout selection (post-convergence step).**

   - New module: `src/reincarnated/generation/canonical_loadout.py` (or similar). Pure deterministic function.
   - `select_canonical_loadout(class_id, season_id) -> Loadout | None`:
     * Read all `class_fight_loadouts` rows for the (class, season) tuple
     * Filter to wins only (outcome=won)
     * If no winning loadouts: return None (graceful — class has empty carried_gear)
     * Group by loadout signature (4-slot gear_instance_id tuple + handedness)
     * For each unique loadout: compute aggregate stats (win count, win rate among fights with that loadout, has_legendary boolean)
     * Selection rule: prefer loadouts with at least one legendary; among those, pick highest win count; tiebreak by win rate, then by legendary tier (legendary > epic > rare)
     * If no winning loadouts have a legendary: pick highest win count overall
   - Tests: deterministic given input; handles edge cases (no wins, single winning loadout, multiple ties)

3. **carried_gear field on class data + integration.**

   - Add `carried_gear: list[str]` field to the playable class data schema (gear instance IDs). Same field for act-boss classes (they're playable classes too).
   - At end of `season_orchestrator.generate_season()`, after convergence completes, run `select_canonical_loadout()` for each class and populate `carried_gear`. Persist to telemetry as part of the existing class persistence path.
   - The carried_gear does NOT affect combat — it's purely associated state. Convergence used the per-fight sampled loadouts to find the canonical; the canonical is captured for downstream consumers.

**Phase 1 acceptance tests:**

- Schema migration applies cleanly to a fresh DB
- A test season runs convergence; per-fight loadout rows persist (verify count: ~30 fights × ~10 matchups × ~10 iterations × ~10 classes per season for the row count)
- After convergence, each class has populated carried_gear (or None if no winning loadouts; flag if pattern is widespread)
- Canonical loadout selection is deterministic — same season state → same canonical loadout per class
- Round-trip: write canonical loadout, read it back, equality check
- Spot-check: a fire_mage class's canonical loadout contains gear whose class_fit_profile leans toward fire/mana — sanity check that successful fights produced sensible loadouts

**STOP after Phase 1, report in standard format (built / learned / surprised / next), wait for go-ahead before Phase 2.**

═════════════════════════════════════
Phase 2 — Generate fresh seasons + Priority 04 verification (~half day)
═════════════════════════════════════

Goal: generate ~5–10 fresh full-LLM-mode seasons using the canonical loadout pipeline from Phase 1; assess Priority 04 (class quality measurement) against one of them.

**Two workstreams:**

1. **Generate ~5–10 fresh seasons.**

   Run season generation in FULL mode against fresh seeds. Each season produces:
   - Class generation + monster generation + trial boss generation + gear pool
   - Convergence with per-fight loadout persistence (Phase 1 feature)
   - Canonical loadout selection populates carried_gear for all classes
   - LLM naming for class skills, classes, monsters, trial, and gear (rare+ tiers)
   - Total LLM calls per season: ~199 per file 19's projection
   
   Verify: each generated season has populated carried_gear on its classes (both playable + act-bosses). Surface any class that ended up with empty carried_gear (i.e., no winning loadouts found in convergence) — that's an outlier worth investigating.

2. **Priority 04 verification on one fresh season (~2 hours).**

   Goal: assess whether the original Priority 04 / "Cluster 2" class-quality concerns are substantively addressed by the dimensional refactor + Priority 02 gear work.

   Pick one of the fresh seasons (any seed). Inspect qualitatively:
   - Each playable class has distinct mechanical identity (energy_type, range_profile, damage_type, role_orientation produce visibly different feel)
   - Ability sets feel coherent with class identity (no glaring "this ability shouldn't be on this class" cases)
   - Gear pool's epic/legendary names feel evocative and seasonally coherent (anchor + element flavor land in names)
   - Affix coherence holds (no staff with melee_strike, no plate with INT bonuses, etc.)
   - Monster + trial-boss content fits the season's theme
   - Canonical loadouts feel sensible — the carried gear roughly matches each class's archetype identity

   Surface findings as a structured report:
   - What's working (specific evidence — class names, ability synergies, gear names, canonical loadout examples)
   - What's not (any quality gaps, naming collisions, mechanical incoherence, weird canonical loadouts)
   - Recommendation: close Priority 04 or keep tracked

**Phase 2 acceptance:**
- 5–10 seasons generated cleanly; each has populated carried_gear; LLM call counts match projection
- Priority 04 verification report produced; recommendation surfaced

**STOP after Phase 2, report findings, wait for go-ahead before Phase 3.**

═════════════════════════════════════
Phase 3 — Engine data export layer (~1 week)
═════════════════════════════════════

Goal: produce a stable JSON export of generated season content, suitable for consumption by the Three.js demo and future game implementations.

Per `collaboration-handoff/22-three-js-demo-and-data-export.md` § "Part 1 — Engine data export layer". Both Phase A (pre-gear) AND Phase B (gear_pool.json + carried_gear) land in this single pass since Priority 02 is closed and Phase 1 added the canonical loadout feature.

**Three workstreams:**

1. **Schema definitions in `src/reincarnated/export/schemas.py`** — frozen Pydantic for each output file. Include version field at top of each schema for forward compatibility. Schemas per § "JSON contracts (sketch)" in file 22, plus the `carried_gear` field on class data (added in Phase 1).

2. **Exporter logic in `src/reincarnated/export/season_exporter.py`** — reads season state, transforms to schema, writes JSON. Deterministic: same input → byte-identical output.
   - Exports: metadata.json, classes.json (with carried_gear), monsters.json, abilities.json, gear_pool.json, damage_formula.md (hand-authored), design_context.md (hand-authored or template-generated).
   - The class data export must include carried_gear with full GearInstance details (not just IDs), so the demo can render drops without doing extra lookups.

3. **CLI command in `src/reincarnated/tools/export_season.py`** — `python3 -m reincarnated.tools.export_season --season N --out path/`, plus a batch wrapper for multiple seasons (`export_seasons --range 90-99 --out exports/`).

**Phase 3 acceptance:**
- Schema migration n/a (export is read-only on existing schemas)
- Round-trip: export → re-load → assert structural equality
- Determinism: export same season twice → byte-identical files
- Schema completeness: every dimensional axis, every ability geometry, every gear field, carried_gear all captured
- Cross-reference integrity: ability ids in classes.json all exist in abilities.json; carried_gear gear_instance_ids all exist in gear_pool.json
- damage_formula.md is human-authored and covers the full damage pipeline (crit, block, armor, DoT post-CP7b fix)
- design_context.md exists as a hand-authored or template-generated reference
- 5–10 seasons can be exported via the batch command; output files validate against schemas

**Specific readiness fields surfaced 2026-05-10 by season 1001 inspection (must be present in Phase 3 export):**

These were identified as gaps in `_class_to_dict()` and the existing `season_writer.py` outputs. Phase 3's data export layer must include them:

1. **`geometry_type` per skill in classes.json.** Currently the geometry exists in the abilities DB table but is not serialized to per-class skill output. Demo1 needs geometry to know how to render each ability (projectile vs AOE vs melee swing, etc.). Demo-blocking.

2. **`carried_gear` field on each class in classes.json.** The carried_gear data lives on the class in DB (per CP9) but is not currently serialized. Demo1's boss-drops-gear mechanic depends on it. Demo-blocking.

3. **`gear_pool.json` populated with the full 200-item pool.** The pool exists in DB but is not currently exported beyond `catalog.json` (which has base type definitions only, not pre-rolled instances). Demo1's drops sample from this pool. Demo-blocking.

4. **`is_act_boss` boolean flag on each class.** Currently identifiable by `target_winrate ≠ 0.5` in balance_metadata, but explicit flag is cleaner. Low-priority but trivial to add.

5. **`visual_prompt` field on rare+ gear instances in gear_pool.json.** Exists in DB; not currently in export. Required for downstream art generation (per file 25 Tier 3 + Meshy/Stable-Diffusion pipelines).

6. **`threat_tier` field on monsters in monsters.json.** Already confirmed queryable in DB (per inspection report); ensure it's included in export. Demo1's 5-tier wave structure depends on it.

The tier values present in season 1001: trash (15), standard (12), elite (7), mini-boss (4), boss (2). Demo1 will need to map these to wave structure.

**Phase 3 does NOT include:**
- Boss-side gear loadouts that affect combat stats (still Priority 13 territory)
- Loot drop event persistence (Priority 15 / Demo Phase 3)
- Player inventory persistence (runtime concern)

**STOP after Phase 3, report in standard format, produce a session note covering the full session, wait for go-ahead.**

═════════════════════════════════════
Cross-phase considerations
═════════════════════════════════════

- All three phases land on the same branch.
- Each phase's commit should be cleanly separable (in case we want to merge them as separate PRs).
- LLM cost: Phase 2's fresh-season generation is the bulk (~5–10 seasons × ~$1.00/season = ~$5–10 in API spend). Engine work in Phase 1 + Phase 3 is zero-LLM.
- Test count: each phase adds tests; at end of session, total test count should be ~1300+ (current: 1172 + Phase 1 ~50 + Phase 2 ~10 + Phase 3 ~50).

If anything in this prompt seems ambiguous, surface questions BEFORE starting work. If architectural surprises emerge during implementation, route through `collaboration-handoff/` rather than deciding in-flight.
```

---

## Notes for the project owner

- **Total session estimated 2 weeks of CLI bandwidth.** Phase 1 is the most architecturally interesting (the per-fight persistence + canonical selection); Phase 2 is small but yields the Priority 04 closure decision; Phase 3 is the data export layer that unblocks the demo work.
- **The session produces three deliverables:** (1) canonical-loadout engine feature, (2) Priority 04 verdict, (3) data export layer with 5–10 seasons of JSON. After this session, the Three.js demo agent has everything they need to start demo1.
- **No design decisions deferred to in-flight.** All architectural calls are settled in the prompt: per-fight persistence schema, canonical selection algorithm (legendary preference + win count), carried_gear field structure.
- **Watch for:** the canonical loadout selection might surface unexpected patterns. E.g., a class whose "best" loadout doesn't have a legendary because the class doesn't synergize with any of the season's legendaries. That's a finding worth surfacing, not a bug.
