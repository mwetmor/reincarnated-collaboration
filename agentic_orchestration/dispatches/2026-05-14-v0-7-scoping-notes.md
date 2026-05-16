# v0.7-encounter-analytics — pre-dispatch scoping notes

**Status:** v0.7 is **BLOCKED** on the star-lord fight-log-granularity research pass (also 2026-05-14). Once that research completes and Matt reviews the findings, this scoping notes file becomes the basis for the v0.7 dispatch.

**Captured:** 2026-05-14 from Matt's clarifications on encounter-viz scope expansion.

**Origin:** Matt's first-pass QA on drax v0.6-encounter-viz: "limited to one fight for 3 classes. I would like to be able to see the mean of means across fights and for all classes." Followed by clarifications that bake in below.

## Re-scoping (v0.6 → v0.7)

v0.6 was **illustration** (static SVG showing the AOE-vs-single-target mechanic for 3 selected classes). v0.7 is **analytics** — a different kind of work. Static SVG hits its ceiling well below this; v0.7 likely needs D3 or similar.

The v0.6 milestone tag `v0.6-encounter-viz` is **held** pending scope expansion. The seam-prefixed intermediate `drax/v0.6-encounter-viz` is on `main`.

## Matt's sharpenings (must be baked into the dispatch)

### 1. Feature space defined deliberately

Pick **3-5 dimensions** from:

- Damage dealt
- Time-to-kill
- Skill-geometry mix (% damage by geometry type)
- Sustain expenditure
- Damage concentration
- Pack-member kill rate

Final choice depends on:
- What the fight log captures (per star-lord research pass)
- What produces visually distinguishable centroids
- Drax's judgment on visual legibility

### 2. Show centroid AND dispersion, not just mean

Render centroid points with **standard-deviation ellipses** around them. A class with wide variance across encounter slots is itself a finding — echoes the **hunter modifier-range observation** from the B14.5 sidecar analysis (hunter's 1.82 modifier range = least consistent shape across seeds; recorded in Matt's memory log `project_b14_5_sidecar_analyses.md`).

Mean-only visualizations would obscure exactly the kind of finding the sidecar analyses surfaced.

### 3. Vocabulary: "encounter slot," not "room"

The engine is **abstract, not spatial**. The A3 gauntlet has **12 encounter slots**, not 12 rooms. Vocabulary precision matters so drax doesn't accidentally model spatial concepts the engine doesn't have. Use "encounter slot" or "encounter position" consistently in code, comments, UI labels, and the dispatch text.

## View structure

| View | Cards | Default? |
|---|---|---|
| **Per-class small-multiples** | 14 (one per Yomi class) | **Primary default** — class is the unit of analysis Matt mostly cares about |
| **Per-encounter-slot small-multiples** | 12 (one per gauntlet slot) | Secondary toggle |

Both views must be available; class-primary because class is the unit we mostly care about.

## Likely tech implications

- Static SVG (v0.6 approach) won't suffice — centroid + stdev-ellipse rendering needs computed geometry
- **D3 or similar visualization library probably required.** The v0.6 "no D3" scope was for v0.6 only.
- Aggregation logic location TBD: computed in app vs. pre-computed in star-lord export. Depends on data shape from research pass. Pre-computed export is cleaner if telemetry data is large; in-app is fine if data is small.

## Open questions to resolve at dispatch authoring time

- **Which 3-5 feature dimensions** to pick (decided after fight-log research completes)
- **Whether telemetry needs extension** for the chosen features
- **Whether aggregation runs in-app or pre-computed export**
- **Tag intent** — proposed: `drax/v0.7-encounter-analytics` intermediate; `v0.7-encounter-analytics` milestone (requires Matt sign-off per ADR-003)
- **Whether v0.7 supersedes or extends `drax/v0.6-encounter-viz`** — likely extends/replaces the `/encounters` route content

## Process flag (recorded so it isn't lost)

The v0.6-encounter-viz dispatch was marked **HELD** in this morning's handoff pending B10.4 metrics. Drax executed it anyway, reading "HELD" as "wait for the metric data that may inform the mechanism viz" rather than "do not execute until knight-rider confirms unblock." The dispatch language was ambiguous. **Future held-dispatch language must explicitly state:** *"Do not execute. Knight-rider will confirm when this dispatch is active."* Worth tightening across all held dispatch templates.

Not flagged for jack-ryan Gate 2 — the work itself is sound, only the process hygiene needs adjustment.

## Star-lord research findings — 2026-05-14

Star-lord completed the read-only fight-log granularity research pass. Summary below.

### Current state of fight-log capture

- `class_fight_loadouts` table (1.8M rows, schema v1.9) captures per-fight aggregates
- Persisted columns: `class_id`, `monster_id`, `iteration`, `fight_index`, `outcome`, `termination_reason`, `damage_dealt`, `damage_taken`, `loadout_json`, `legendary_count`
- In the in-memory `fight_log` dict but NOT persisted: `modifier`, `duration_seconds`, `a_final_hp`, `b_final_hp`, `a_max_hp`, `b_max_hp`, `a_actions_taken`, `b_actions_taken`
- `heals_received` tracked on `CombatantState` but never read into `FightResult`
- `action_trace` list exists as a diagnostic path in `fight_engine.py` (captures per-skill use with `actor_id`, `energy_type`, `skill_role`, `mana_before`, `mana_after`) but never wired to telemetry
- No `fight_events` table exists; the stub methods `start_fight` / `complete_fight` / `record_event` on `TelemetryRecorder` are no-ops

### Per-dimension feasibility (against Matt's 6 candidates)

| Dimension | Status | Notes |
|---|---|---|
| Damage dealt | **(a) already in fight log** | Query `class_fight_loadouts.damage_dealt` directly |
| Time-to-kill | **Tier 1 fix (1 line + migration)** | `duration_seconds` already in dict, just dropped at persist step |
| Skill-geometry mix (kit composition) | **(b) computable by join today** | `abilities` table has `geometry_type`; join via `owner_id ↔ class_id`. Static per class, not per-fight usage |
| Sustain expenditure | **Tier 1 fix (~8 lines + migration)** | Read `state_a.heals_received` and `(POTION_COUNT - state_a.health_potions)` in `_build_result()`; persist as `a_heals_received` + `a_potions_used` |
| Skill-geometry mix (per-fight usage) | **Tier 2 fix (~40 lines + new table)** | Wire existing `action_trace` to a new `fight_skill_uses` table; gate behind flag pattern. Storage cost meaningful (~10-20 rows × 1.8M fights) — flag-gated capture recommended |
| Damage concentration across pack members | **Out of scope for v0.7** | PackProxy collapses N=8 swarm mobs to a single aggregate HP pool; per-mob distribution is structurally lost at the abstraction layer. True per-mob data would require PackProxy disaggregation = significant simulation change |
| Pack-member kill rate | **Out of scope for v0.7** | Same root cause as above. Approximable via geometry-mix-by-usage (Tier 2) as a proxy |

### Star-lord's recommended v0.7 dimensions (ranked)

1. Damage dealt — today
2. Time-to-kill — after Tier 1 fix
3. Skill-geometry mix (kit composition) — today, via join
4. Sustain expenditure — after Tier 1 fix
5. Pack concentration via geometry-mix-by-usage proxy — Tier 2 if approved, otherwise defer

This produces a clean 4-or-5 dimension feature space for centroid + stdev-ellipse clustering, exactly the shape Matt's sharpening § 1 requires.

## Decisions — Matt resolved 2026-05-14

- **(A) Tier 1 extension — APPROVED.** Dispatch: `2026-05-14-star-lord-telemetry-tier1.md`.
- **(B) Tier 2 extension — DEFERRED.** Revisit "as time allows" (Matt). v0.7 ships with 4 dimensions (damage / time-to-kill / kit-composition-geometry / sustain), not 5. The 5th dimension (per-fight skill-geometry usage) waits for Tier 2.
- **(C) PackProxy disaggregation — DEFERRED INDEFINITELY.** Out of v0.7 scope.

## Locked v0.7 dimensions (post-Tier-1)

1. **Damage dealt** — queryable today
2. **Time-to-kill** — available after Tier 1 lands and a fresh regen pass populates `duration_seconds`
3. **Skill-geometry mix (kit composition)** — queryable today via `abilities ⋈ class_fight_loadouts`. Static per class, not per-fight dynamic. Acceptable for centroid signature given Tier 2 is deferred.
4. **Sustain expenditure** — available after Tier 1 lands and a fresh regen pass populates `a_heals_received` + `a_potions_used`

These four dimensions form the v0.7 feature space for centroid + stdev-ellipse clustering.

## v0.7 data prerequisites

- Tier 1 star-lord dispatch must ship before v0.7 drax dispatch can be authored
- A **fresh regen of Yomi (season_002328) with Tier-1-extended telemetry** is required to populate the new columns. Existing 1.8M rows cannot be backfilled — `duration_seconds` and `heals_received` are runtime computed and not preserved on aggregate. The regen happens at v0.7 time, not Tier 1 time.

## v0.7 viz interpretation hook — AOE balance philosophy dependency

Matt observation 2026-05-15: the AOE balance philosophy lock (View A / B / C — pending jack-ryan Gate 1 Q3 finding on the B10.4 dispatch) **affects how v0.7 centroid viz should be interpreted**, not just whether the viz is viable.

If View A is locked (AOE classes earn pack-clear identity as "free upside" with no 1v1 damage penalty), then clusters along a **completion-time axis** in the v0.7 viz become a **diagnostic surface for the AOE-favored metagame implication** — they're not showing a balance failure, they're showing the genre-flavored upside operating as designed.

If View B or C is locked (damage-per-target or cost-mediated trade-off), then completion-time clusters reflect **genuine balance trade-offs operating as intended** — AOE classes complete pack content faster but pay through 1v1 damage / energy cost / cooldown elsewhere.

**Implication for v0.7 dispatch authoring:** the dispatch must include the AOE-philosophy framing in its viz-interpretation guidance to drax. Same chart, different reading depending on which view is locked. The dispatch should reference whichever view the decisions-log entry codifies post-jack-ryan.

## Next step

1. Jack-ryan returns Gate 1 findings on B10.4 Option 2 + AOE philosophy (running in background as of 2026-05-15)
2. Matt decides AOE philosophy lock (View A / B / C) based on jack-ryan's empirical findings
3. Star-lord executes Tier 1 telemetry dispatch (when picked up — currently queued)
4. Knight-rider drafts v0.7 drax dispatch *including the locked AOE-philosophy framing for viz interpretation*, with a Yomi regen step (drax + gamora coordination)
5. Tier 2 stays in the queue under "as time allows"
