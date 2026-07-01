# Dispatch — 2026-06-30 — gamora — perception-asymmetry AoeCastEvent producer (symmetric-sim)

**From:** knight-rider
**To:** gamora (primary — sim producer)
**Coordination:** star-lord (sink confirmation — no build; see § star-lord coordination)
**Approved by:** Matt 2026-06-30 (F2 hinge ruling — direct authorization to fire)
**Estimated effort:** ≤2 hours (small, self-contained wiring)
**Acceptance:** an `AoeCastEvent` row emits per AOE cast at both sim cast sites; `apparent_radius == true_radius` (spillover 0) on every row; player WR unchanged vs the current symmetric baseline; round-trip smoke lands a row through the existing recorder sink.

## Context

The perception-asymmetry near-miss mechanic is designed + foundation-built + demo-wired + telemetry-schema'd, but **never carried into the spatial sim** — `spatial_engine.py` resolves all AOE symmetrically and `AoeCastEvent` has **no producer** (the `aoe_cast_events` table is a schema with zero writers). This is the registered build-vs-spec GAP (`current-to-end-state-engine.md`, 2026-06-30 delta).

**Matt's F2 hinge ruling (2026-06-30) simplifies this decisively.** The battle sim is **SYMMETRIC** — player and enemy resolve AOE on the same radius; **neither has an edge in the balance math**. The player-favoring perceptual edge is granted at the **control layer** (human-piloted = full edge; AI-piloted = reduced edge) as a **piloted-Godot layer-handoff** (drax future-scope, sibling to `dodge_gated_deferred`), **controller-keyed, not role-keyed**. This supersedes the original brief's §2/§5 (edge-in-sim, role-keyed 1.12/0.90 constants) and re-homes the §6 WR-falsifier to the piloted layer.

**What survives for THIS dispatch:** wire the `AoeCastEvent` producer (§1 gap) — but emit `apparent_radius = true_radius` (spillover 0 = the honest "sim granted no edge" assertion). Damage resolution is **untouched**. This fills the waiting telemetry table with a producer and closes the staged loop, while the perceptual edge waits for the piloted Godot layer that will consume the still-locked constants.

## Required reading before starting
- `agentic_orchestration/gandalf/notes/2026-06-15-gamora-brief-perception-asymmetry-sim-wiring.md` — the lineage brief (**read the SUPERSEDED-IN-PART banner at top first** — §2/§5 are superseded by F2; §1 gap + §4.3 emission survive)
- `canonical/matt_decision_needed/README.md` — RESOLVED appendix Q1 (the full F2 ruling, verbatim)
- `src/reincarnated/telemetry/aoe_cast_event.py` — the `AoeCastEvent` dataclass + field semantics + Discipline-#8 validation invariant
- `src/reincarnated/foundation/perception_asymmetry.py` — the locked constants module (DO NOT consume/redefine in sim under this ruling; it stays as the spec the piloted layer will consume)

## Math-before-code
Minimal — the symmetric ruling removes the modeling choice the original brief §3 flagged. Document in a short math-note:
- **The symmetric assertion:** `apparent_radius := true_radius` at both cast sites → `apparent_radius_hit_count == true_radius_hit_count` by construction → spillover delta = 0. This is the *encoded evidence* that the sim grants no perceptual edge (per F2).
- **The WR-invariance prediction (register it):** because damage resolution is untouched AND apparent==true (no avoidance change), player WR must be **byte-identical / statistically unchanged** vs the current symmetric baseline. This is a producer-only add, not a balance change. **Falsifier:** any WR movement means the wiring accidentally touched a decision/damage path — surface it, do not ship.

## Cross-seam contract change? (Principle 6 gate — completed by knight-rider at authoring)

Does this dispatch add/modify/rename/remove a field on a telemetry schema table, fight_log key, loadout key, export packet, or inter-seam fixture dict?

**NO field change** — the `aoe_cast_events` table + `AoeCastEvent` dataclass already exist (schema built 2026-05-17). **BUT** this dispatch introduces gamora as a **NEW producer** of rows that star-lord's `recorder.record_aoe_cast_event` sink consumes (a producer-contract change, not a schema change). Round-trip smoke is therefore **REQUIRED**:

- **Round-trip smoke:** construct an `AoeCastEvent` at a real cast site via the production sim path → emit through `recorder.record_aoe_cast_event` → confirm a row lands in `aoe_cast_events` with `apparent_radius_hit_count == true_radius_hit_count` and all identity fields populated (cast_owner ∈ {player, enemy}, skill_id, substrate, geometry, true_radius, apparent_radius).

## Scope
- [ ] **Player cast site** (`spatial_engine.py:2090`, `_compute_aoe_hits(self.player, ...)`): construct + emit `AoeCastEvent` with `cast_owner="player"`, `true_radius = skill.radius`, `apparent_radius = true_radius`, `true_radius_hit_count = len(targets_hit)`, `apparent_radius_hit_count = true_radius_hit_count`.
- [ ] **Enemy cast site** (`spatial_engine.py:2193`, `_compute_aoe_hits(mob, ...)`): same, `cast_owner="enemy"`.
- [ ] Damage resolution UNCHANGED — the event is a post-hit observer emission; assert `_apply_skill_damage` path is byte-identical.
- [ ] Leave a code comment at each emit site citing the F2 ruling (`apparent==true` in sim by design; edge deferred to piloted Godot layer, controller-keyed) so a future reader doesn't "fix" it back to asymmetric.
- [ ] Smoke-test: WR-invariance check vs current symmetric baseline (seed base disjoint from used range — 41M–51M taken; use **52,000,017+**).
- [ ] Round-trip smoke (per Principle 6 above).
- [ ] MIGRATION.md — producer-contract entry (gamora → star-lord; new `AoeCastEvent` producer, no schema change; next version after v1.82).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tracker-delta to gandalf/KR: the perception-asymmetry PART-I sim GAP is CLOSED (producer wired, symmetric-emit); the perceptual EDGE re-homes to the piloted-Godot layer-handoff (drax future-scope).
- [ ] Tag: `gamora/v-perception-asymmetry-producer-1`

## Acceptance criteria
- [ ] An `AoeCastEvent` row emits per AOE cast at both player (`:2090`) and enemy (`:2193`) cast sites.
- [ ] `apparent_radius == true_radius` and `apparent_radius_hit_count == true_radius_hit_count` on every emitted row (spillover = 0 — the symmetric assertion).
- [ ] Player WR **unchanged** vs the current symmetric baseline (the pass — producer-only, no balance movement). Any WR delta ≠ 0 is a falsifier → surface, don't ship.
- [ ] Damage resolution byte-identical (observer emission only; `_apply_skill_damage` untouched).
- [ ] Round-trip smoke: real-cast-site `AoeCastEvent` → `recorder.record_aoe_cast_event` → row lands in `aoe_cast_events` with symmetric hit-counts and populated identity fields.

## Out of scope (explicit non-goals)
- **The ally-proxy cast site** (`spatial_engine.py:2356`, `_compute_aoe_hits(_ally, ...)`) — proxy telemetry is a proxy-wave concern (proxies only appear via injected fixtures; no production emission). Do NOT wire proxy emission here. If you judge it trivial to include symmetrically, surface it as an open question — do not silently add.
- **Consuming `perception_asymmetry.py` constants in the sim** — the F2 ruling explicitly keeps the sim symmetric. The 1.12/0.90 constants stay in `foundation/` as the spec the piloted Godot layer consumes. Do NOT import or apply them in `spatial_engine.py`.
- **Any change to AI avoidance / positioning / targeting radius** — the original brief §3 "proxy avoids enemy AOE at apparent" is SUPERSEDED. No decision-layer change.
- **Any schema/migration change to `aoe_cast_events`** — table already exists; producer-only.
- **The piloted-layer edge itself** — that's drax future-scope (Godot combat doesn't exist yet). This dispatch only registers the handoff, it does not build the edge.

## Open questions for the agent to resolve (document your call)
- Exact `skill_geometry` / `skill_substrate` field population at each cast site — pull from the resolved skill object; document the source field. If a cast site lacks a clean substrate/geometry handle, note it (don't fabricate).
- `season_id` / `run_id` / `fight_id` provenance at the cast site — use the existing fight-context handles the recorder already expects; note if any are `None` for out-of-regen gauntlet fights (the dataclass allows `run_id=None`).

## Gate plan
- **No Gate-1.** Matt's F2 ruling states no semantic shift (the sim was already symmetric; this is a producer-only observer add that changes nothing in the balance math). Gate-1 is waived by that ruling.
- **Normal Gate-2** (jack-ryan DEV-MODE) on the tagged commit → submit to `qa/pending/`. jack-ryan verifies: damage-path byte-identity, WR-invariance, symmetric-emit (apparent==true), round-trip, MIGRATION producer entry.

## star-lord coordination (no build — confirmation only)
star-lord's `recorder.record_aoe_cast_event` sink (`telemetry/recorder.py:1029`) and the `aoe_cast_events` table already exist. star-lord's role here is **confirmation, not build**: verify the sink handles the emit volume (one row per AOE cast across a full gauntlet run is a meaningful row-count increase — confirm no write-path bottleneck / no unbounded buffer) and that **no schema change** is needed. This is exercised by gamora's round-trip smoke; star-lord confirms at Gate-2 (or KR routes a quick star-lord confirmation if volume raises a flag). No MIGRATION obligation on star-lord's side (gamora authors the producer-contract entry).

## References
- F2 ruling: `canonical/matt_decision_needed/README.md` RESOLVED / Q1 (Matt 2026-06-30)
- Lineage brief (superseded-in-part): `agentic_orchestration/gandalf/notes/2026-06-15-gamora-brief-perception-asymmetry-sim-wiring.md`
- Original design (two-layer model): `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md`
- Dataclass + field semantics: `src/reincarnated/telemetry/aoe_cast_event.py`
- Constants (locked; sim does NOT consume under F2): `src/reincarnated/foundation/perception_asymmetry.py`
- Sim conservatism precedent (this stacks with it): decisions-log:1240 (movement-speed-blind sim under-credits player margin)
- Discipline #16 (tuning-drift — constants untouched), #12 (semantic-shift — N/A per F2 ruling), #8 (schema validation at boundaries — the round-trip)
