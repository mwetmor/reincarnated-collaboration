# Continuous-Observation Watchpoints — Engine Rebuild (Second Hive Activation)

**Author:** jack-ryan
**Established:** 2026-05-19
**Status:** ACTIVE — continuous-observation mode per hive-mind-protocol-engine-rebuild-2026-05-19.md § 4.5 (inherited from 2026-05-17 protocol § 7)
**Hive log:** `engine-rebuild-log.md` (OBSERVATION entries filed here; findings link to this registry)
**Mission canonical:** `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md`
**Protocol:** `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`

**BLOCK authority retained per protocol § 4.5; use sparingly. First response is OBSERVATION; BLOCK only if seam does not engage.**

---

## Per-discipline load map for this rebuild

| Discipline | Load-bearing workstreams | Risk level |
|---|---|---|
| #1 Math-before-code | R1 (per-tier math), R2 (spatial combat math) | HIGH |
| #11 Live-state verification | R7 (parity test = the live-state verification mechanism) | HIGH |
| #13a Implementation-vs-intent drift | R3 (schema coherence across 4 seams), R7 (catalogue source of truth) | HIGH |
| Pattern P7 Silent-default convergence | R1 (aggregate-mean silent pass), R7 (TS/Python constant fallback) | HIGH |
| MIGRATION.md cadence | R3 (rocket + star-lord), R8 (rocket + star-lord), R1 (gamora if telemetry change) | HIGH |
| Discipline #14 Internal-vs-generative schema | R8 (post-convergence theme-coalescence prompt construction) | MEDIUM |
| Discipline #8 Schema validation at export boundaries | R3 (rocket schema validators), R7 (parity test harness) | MEDIUM |
| R11(b) Cross-seam round-trip discipline | R3 (broadest blast radius), R7, R8, R1 if telemetry | HIGH |
| Hive log commit discipline | All seams | MEDIUM |
| Tag discipline | All workstreams | LOW |

---

## WP-R1-A — Discipline #1 (math-before-code) for R1 per-tier convergence

**Risk level:** HIGH
**Owner watchpoint:** gamora
**Protocol ref:** hive-mind-protocol § 4.5 + § 9; engineering-disciplines.md #1; dispatch `2026-05-19-gamora-R1-per-tier-balance-targets.md`

### WP-R1-A-1: Per-tier math note must precede balance_loop.py modification

The R1 dispatch requires a math note at `reincarnated-engine/design/working-agreement/R1-per-tier-math-2026-05-19.md` BEFORE gamora touches `balance_loop.py:1907-1936`. Jack-ryan reviews the math note before any implementation commit.

**Required contents of the math note (per dispatch):**
1. Per-tier target table (gandalf-confirmed; swarm 0.72 / magic 0.62 / elite 0.52 / mini-boss 0.45 / boss 0.38; floors 0.65/0.55/0.45/0.35/0.30; ceilings 0.80/0.70/0.60/0.55/0.45)
2. Per-tier tolerance band semantics — exact operative convergence criterion (target ± tolerance vs floor/ceiling)
3. Convergence pass criterion — all 5 tiers must pass; early-exit semantics documented
4. Per-tier statistical strategy — boss (1 slot) is noisier than swarm (6 slots); n-shot variance handling documented
5. Pattern P7 callout — explicit fail-loud semantics for per-tier miss; telemetry surface named
6. Per-tier WR telemetry emission spec — what fields added; MIGRATION.md scope determination

**Trigger:** gamora commits any `balance_loop.py` modification without a corresponding committed math note. File OBSERVATION immediately; if implementation merges before math note exists, file WARN.

### WP-R1-A-2: Boss-tier statistical noise handling

The boss slot (1 slot, vs swarm's 6 slots) has inherently higher variance per simulation run. An n-shot strategy is required. If gamora uses a single-run boss result to declare convergence pass/fail, the criterion will be unstable.

**Expected math note answer:** e.g., "Boss tier uses 30 fight simulations per evaluation; swarm uses 30×8 mob simulations per evaluation; per-tier pass criterion uses mean of N simulations per tier-slot."

**Trigger:** math note does not document n-shot strategy per tier, OR implementation uses 1-shot boss evaluation while using multi-shot swarm evaluation without explicit rationale.

---

## WP-R1-B — Pattern P7 (silent-default) for R1 per-tier failure

**Risk level:** HIGH
**Owner watchpoint:** gamora
**Protocol ref:** engineering-disciplines.md Pattern P7; dispatch explicit note on P7 risk

### WP-R1-B-1: No silent aggregate-mean pass on per-tier miss

The current `balance_loop.py:1907-1936` aggregate-mean convergence will silently pass a boss-unwinnable class at mean 0.622. R1 must fail-loud when ANY tier misses its band. The risk: gamora implements per-tier tracking but leaves aggregate-mean as the primary convergence gate with per-tier as "advisory only."

**Required behavior:** convergence loop rejects and triggers re-tune when ANY tier's WR falls outside floor/ceiling band. Per-tier failure cause logged to telemetry (not just printed to console).

**Trigger:** gamora's implementation accepts a class where boss WR = 0.15 and swarm WR = 0.80 as "converged." File BLOCK — this is the exact scenario R1 exists to eliminate.

### WP-R1-B-2: Per-tier failure cause must reach telemetry, not only stdout

Pattern P7's prevention mechanism requires that silent failures surface in observable channels. Per-tier miss reason (e.g., "boss_tier WR=0.18, floor=0.30, FAIL") must appear in the fight log / telemetry record, not only in console output.

**Trigger:** implementation logs per-tier failure to stdout only; no corresponding telemetry field. File WARN.

---

## WP-R3-A — Discipline #13a (drift) for R3 schema migration coherence

**Risk level:** HIGH
**Owner watchpoint:** rocket + star-lord + elrond (joint schema; four consumer seams)
**Protocol ref:** engineering-disciplines.md #13a; hive-mind-protocol § 9; dispatch `2026-05-19-rocket-plus-star-lord-plus-elrond-R3-schema-migration.md`

### WP-R3-A-1: Schema field naming must match across all producer/consumer seams

R3 introduces at minimum: `range_m` (or `range_band`), `preferred_behavior`, `telegraph_window_seconds`, `aggro_radius_m`, `leash_distance_m`, `skill_rotation_priority`, `range_profile_redistribution`. Each field name MUST be identical across:
- Rocket's catalogue emitter (generation seam)
- Star-lord's telemetry recorder and export surface (export seam)
- Elrond's backfill tooling (data-steward seam)
- Gamora's simulation consumer in `fight_engine.py` (engine-sim seam)
- Drax's demo runtime consumer (downstream; R4/R5 seams)

**Drift instance shape:** gamora reads `aggro_radius_m` from monster JSON; rocket emits `aggro_radius` (no `_m` suffix); test is green because test fixture uses rocket's shape directly. Production JSON has the `_m` field; gamora silently gets `None` and uses a default. This is textbook P7 + Discipline #13a.

**Trigger:** any commit where a field name used in a consumer seam differs from the field name in the producing seam's schema design doc (`R3-schema-design-2026-05-19.md`). File OBSERVATION on first discovery; WARN if pattern recurs across two seams.

### WP-R3-A-2: MIGRATION.md authored concurrently — not retroactively

R3 dispatch specifies MIGRATION.md at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` authored concurrently by rocket. Star-lord authors at `reincarnated-engine/src/reincarnated/export/MIGRATION.md`. Both must be present when schema design doc commits.

**The failure pattern:** schema design doc commits without MIGRATION.md; consuming seams begin implementation against the doc; MIGRATION.md is authored after the first consumer seam is already diverging from the actual schema.

**Trigger:** schema design doc (`R3-schema-design-2026-05-19.md`) commits without a corresponding MIGRATION.md commit in the same PR/tag. File WARN; escalate to BLOCK if consuming seams have already begun implementation before MIGRATION.md exists.

### WP-R3-A-3: Schema validators must fail-loud on missing fields (Pattern P7 prevention)

R3 dispatch explicitly requires: "Engine schema validators updated to require new fields (fail-loud on missing, per Pattern P7 avoidance)." If the new fields are optional-nullable in the validator, any content that was backfilled with incorrect or missing values will pass silently.

**Required behavior:** after backfill, schema validation run across all 5 shipped seasons must fail-loud on any monster JSON or skill entry missing required R3 fields.

**Trigger:** gamora's engine-sim consumer or elrond's backfill validation accepts monster JSON with `preferred_behavior: null` without raising. File WARN.

### WP-R3-A-4: R3 is the critical-path workstream — slip here slips R2, R4, R5

R3 gates four downstream workstreams. Jack-ryan watches for scope creep or design-debate delay that stalls R3 without a hive log STATE entry. If R3 goes silent (no hive log entry from any R3 seam for > 1 active day), file OBSERVATION surfacing the gap.

**Trigger:** R3 seams (rocket / star-lord / elrond) have no hive log entry for a full active day after acknowledgment. File OBSERVATION.

---

## WP-R7-A — Discipline #11 (live-state verification) for R7 parity test

**Risk level:** HIGH
**Owner watchpoint:** rocket + star-lord
**Protocol ref:** engineering-disciplines.md #11; hive-mind-protocol § 9; dispatch `2026-05-19-rocket-plus-star-lord-R7-ai-catalogue-source-of-truth.md`

### WP-R7-A-1: Parity test specification must precede harness implementation

The R7 dispatch requires a parity-test spec at `reincarnated-engine/design/working-agreement/R7-parity-test-spec-2026-05-19.md` BEFORE implementing the test harness. Jack-ryan reviews before implementation commit.

**Required contents of the spec:**
- What behavioral facets the parity test asserts (aggro_radius response distance; leash break behavior; preferred_behavior observable; range_profile distribution)
- How parity is measured across 1D engine-sim vs 2D demo runtime (±10% tolerance per Test 1 success criterion; Test 2 requires file:line failure reporting)
- Test harness architecture: instantiate-both-engines vs telemetry-comparison from real fights
- Pattern P7 explicit avoidance: the test MUST fail-loud on silent-default fallback; no consumer accepting hardcoded TS constant or Python default passes silently
- Failure reporting mechanism: file:line of the divergent consumer

**Trigger:** parity-test harness implementation commits without a corresponding parity-test spec doc. File WARN.

### WP-R7-A-2: Consumer audit must enumerate all fallback-to-constant call sites

R7 dispatch requires a consumer audit at `R7-consumer-audit-2026-05-19.md` enumerating all call sites in engine-sim Python and demo TS that currently default to constants instead of reading from JSON. This is Discipline #11 applied to the live-state verification surface — you cannot write a parity test that covers what you haven't audited.

**Specific known sites to verify coverage:**
- `reincarnated-demo/src/world/movement.ts:74-81` — `PREFERRED_RANGE: { close: 90, medium: 420, long: 660 }` and `KITE_TRIGGER: 300`
- Engine-sim AI constant fallback sites in `ai_strategies.py`
- `fight_engine.py` implicit behavior assumptions about aggro/leash (the "no leash" behavior is an implicit constant)

**Trigger:** consumer audit commits without naming `world/movement.ts:74-81` and `KITE_TRIGGER: 300` as enumerated sites. File WARN — these are the known P7 instances; missing them in the audit means the parity test won't catch them.

### WP-R7-A-3: Parity test must fail-loud on intentional break (Test 2 criterion)

R7 Test 2 requires: "Hardcode TS constant override in demo. Parity test should fail loudly, with file:line of the override." This is the self-validation test for the test harness. If the parity test cannot detect a hardcoded override, the harness is not serving its purpose.

**Trigger:** R7 hypothesis tests are executed without Test 2 (intentional-break validation) or Test 2 is skipped because "we trust the harness." File WARN if Test 2 skipped; BLOCK if parity test is being called production-complete without a demonstrated intentional-break failure case.

### WP-R7-A-4: Demo-runtime consumer must iterate registry, not fall back to defaults

Pattern P7 in the R7 context: demo runtime AI currently reads no JSON at runtime; it uses TS constants. When R7 ships the catalogue-as-source-of-truth path, the demo runtime consumer MUST iterate the monster registry to read `preferred_behavior`, `aggro_radius_m`, `leash_distance_m`, etc. — not fall back to `PREFERRED_RANGE.long = 660` if the JSON field is missing.

**Required behavior:** missing JSON field triggers fail-loud in the demo consumer (or in the parity-test mock), not a silent constant fallback.

**Trigger:** star-lord's parity-test spec documents ±10% tolerance WITHOUT documenting what happens when the field is missing (absent vs tolerated). Field-absent behavior is distinct from field-present-but-different behavior. If spec treats `null` and `within-tolerance` as the same, the Pattern P7 gap survives. File OBSERVATION pointing at this distinction; escalate to WARN if not addressed in the spec.

---

## WP-R8-A — Discipline #1 (methodology-before-execution) for R8 cohesion-judging

**Risk level:** MEDIUM
**Owner watchpoint:** gandalf (methodology docs) + rocket + star-lord (pipeline impl)
**Protocol ref:** engineering-disciplines.md #1; dispatch `2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md`

### WP-R8-A-1: Theme-coalescence prompt and cohesion-judging protocol must precede A/B run

The R8 dispatch requires gandalf to author:
- Theme-coalescence prompt at `agentic_orchestration/hive-mind/R8-theme-coalescence-prompt-2026-05-19.md`
- Cohesion-judging protocol at `agentic_orchestration/hive-mind/R8-cohesion-judging-protocol-2026-05-19.md`

Both must exist before the A/B run executes. Running seasons before the judging protocol exists means the cohesion scores cannot be reliably calibrated after the fact (scorer sees the seasons; scale anchoring is contaminated).

**Trigger:** A/B run begins (any inverted-season generation) before both docs are committed. File WARN.

### WP-R8-A-2: Cohesion-judging calibration — scale anchoring must be documented before judging

The cohesion scale (1–5) must be anchored to specific examples from prior seasons BEFORE gandalf judges the A/B seasons. If the scale is anchored post-judging, the baseline and inverted seasons may have been scored against different implicit criteria.

**Trigger:** cohesion-judging protocol does not include anchor examples for each scale point (1, 3, 5 at minimum); or protocol specifies "anchors will be selected from A/B results." Either indicates the calibration will be contaminated. File WARN.

### WP-R8-A-3: Discipline #14 (internal-vs-generative schema) for theme-coalescence prompt

The theme-coalescence prompt (the single LLM call after mechanical convergence) will receive converged content as input. If the prompt leaks canonical-four substrate labels (fire/water/earth/wind) or archetype-tag vocabulary (warrior/mage/rogue/hunter) as explicit input keys, Discipline #14 is violated — internal schema leaked to generative surface.

**Required behavior:** the prompt passes per-instance vocabulary (the actual content that converged — named skills, named monsters, named gear) as its input context, not canonical-four labels as structural framing. The theme emerges FROM the content, not from canonical-four labels attached to the content.

**Trigger:** gandalf's theme-coalescence prompt includes explicit canonical-four element names (fire/water/earth/wind) as structural keys in the prompt body (not as values that happen to appear in skill names). File WARN per Discipline #14.

### WP-R8-A-4: --no-coalesce mode must not silently fill theme fields from defaults

Pattern P7 for R8: the `--no-coalesce` flag is intended to produce raw mechanics output with no theme coalescence. If the generation pipeline has any default-fill code path for `season_theme_element` or cosmological vocabulary fields, those fields may be silently populated even under `--no-coalesce`.

**Required behavior:** under `--no-coalesce`, theme-related fields in `manifest.json` must be absent or explicitly null — not filled from any default or fallback.

**Trigger:** round-trip smoke of `--no-coalesce` mode produces a manifest.json that contains non-null `season_theme_element`, `anchor`, or `cosmological_vocabulary` fields. File WARN.

---

## WP-MIGRATION — MIGRATION.md cadence across R3, R7, R8

**Risk level:** HIGH
**Owner watchpoint:** all producing seams (rocket for R3/R7/R8; star-lord for R3/R8; gamora if R1 telemetry change)
**Protocol ref:** ADR-004; hive-mind-protocol § 4.4 (inherited 2026-05-17 § 6.2); coordination-matrix § 4

### WP-MIGRATION-1: R3 generation MIGRATION.md (rocket) — concurrency check

Path: `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`

R3 is the highest-blast-radius schema change in this rebuild (four downstream workstreams depend on it). MIGRATION.md must commit alongside or before the schema design doc. Jack-ryan checks at every R3 workstream tag.

**At hive-rebuild/v0.4 tag check:** confirm MIGRATION.md at generation path exists and is populated with every new field (range_m/range_band, preferred_behavior, telegraph_window_seconds, aggro_radius_m, leash_distance_m, skill_rotation_priority, range_profile_redistribution). Missing fields are WARN; absent MIGRATION.md entirely is BLOCK.

### WP-MIGRATION-2: R3 export MIGRATION.md (star-lord) — telemetry additive-vs-breaking decision

Path: `reincarnated-engine/src/reincarnated/export/MIGRATION.md`

Star-lord must document whether new telemetry fields are additive (existing tables unchanged; new columns added) or breaking (schema version bump required; consumer rebuild obligations). This decision affects downstream consumers (loadout, demo) who may need coordination.

**At hive-rebuild/v0.4 tag check:** confirm star-lord's MIGRATION.md exists and documents additive vs breaking decision with explicit consumer obligations.

### WP-MIGRATION-3: R7 MIGRATION.md — R7-specific section in R3's MIGRATION.md (or standalone)

R7 shares schema with R3. The R7 dispatch specifies appending R7-specific additions to R3's generation MIGRATION.md. Jack-ryan checks that R7's catalogue-as-source-of-truth contract is documented — specifically: demo runtime AI now reads monster JSON at spawn (new cross-repo contract; not previously present).

**Trigger:** R7 hypothesis tests execute without MIGRATION.md containing an entry for the engine-catalogue → demo-runtime read path (the new cross-repo contract). File WARN.

### WP-MIGRATION-4: R8 generation + LLM MIGRATION.md (rocket + star-lord)

Paths: generation MIGRATION.md (shared); `reincarnated-engine/src/reincarnated/llm/MIGRATION.md` (new)

R8 changes default pipeline behavior (mechanical-first instead of theme-first). Any tooling that invokes `generate-season` without the `--theme-input` flag will experience a behavior change. MIGRATION.md must document: which CLI consumers are affected; what the new default produces; what the `--theme-input` flag restores.

**At hive-rebuild/v0.9 tag check:** confirm both R8 MIGRATION.md entries exist.

### WP-MIGRATION-5: R1 simulation MIGRATION.md (gamora) — telemetry-conditioned

Path: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`

MIGRATION.md required ONLY if gamora introduces a new per-tier WR field to `class_balance_results` or fight_log. If the per-tier breakdown is computed locally in `balance_loop.py` without crossing a seam boundary, not required. Gamora's math note must explicitly declare the cross-seam impact determination.

**Trigger:** gamora's math note does not include the "Round-trip: applicable/not-applicable" determination from the R1 dispatch. File OBSERVATION.

---

## WP-XSEAM — Cross-seam contract change vigilance for R3 blast radius

**Risk level:** HIGH
**Owner watchpoint:** all four first-fire workstreams; cross-seam boundaries
**Protocol ref:** engineering-disciplines.md R11(b); ADR-004; coordination-matrix § 3 concurrent-edit hot-spots

### WP-XSEAM-1: balance_loop.py concurrent edit — R1 (gamora) vs future R3 consumer (rocket)

`balance_loop.py` is edited by gamora for R1 (per-tier convergence) and will later be edited by rocket as an R3 consumer (range checks in sim). Per coordination-matrix § 3: "gamora first; R3 consumer follows after R3 schema ships."

**Risk:** gamora's R1 changes structure the file in a way that creates a merge conflict with rocket's R3 consumer changes. If both are open in parallel sessions without coordination, silent-merge or overwrite is possible.

**Required:** gamora declares intent to modify `balance_loop.py` in hive log before committing. Rocket declares intent before R3 consumer changes touch the same file. Knight-rider mediates if simultaneous intent declarations appear in the log.

**Trigger:** both gamora and rocket have hive log HANDOFF entries declaring concurrent `balance_loop.py` modifications without a knight-rider coordination STATE entry between them. File OBSERVATION.

### WP-XSEAM-2: Monster JSON schema — three-seam concurrent ownership during R3

During R3: rocket (schema emitter), elrond (backfill over existing JSONs), star-lord (telemetry export consumer of new fields). All three may touch monster JSON files or the schema definition concurrently.

**Required:** rocket's schema design doc commits FIRST; elrond and star-lord read from it and do not propose schema changes independently. Any schema field name question routes to rocket as L1 schema owner.

**Trigger:** star-lord or elrond proposes a new field name in hive log that differs from rocket's schema design doc. File OBSERVATION; route to rocket for L1 resolution.

### WP-XSEAM-3: demo runtime read path — R7 source vs R5 consumer sequencing

R7 builds the catalogue-as-source-of-truth on the engine side. R5 (drax) wires the demo runtime to read from that catalogue. The sequencing must not be inverted: R5 cannot wire demo to read fields that R7 has not yet defined and populated.

**Required:** R5 dispatch does not fire until R3 schema + R7 parity-test-source-side ship (per protocol § 5.5 activation gate). Knight-rider enforces this; jack-ryan watches for drax beginning R5 demo-side wiring before R7 parity test source side is tagged.

**Trigger:** drax's hive log acknowledgment of R5 work appears before `hive-rebuild/v0.7-r7-parity-test-operational` is tagged. File OBSERVATION; route to knight-rider.

---

## WP-HIVELOG — Hive log commit discipline (protocol § 4.2 amendment)

**Risk level:** MEDIUM (three silent-loss race condition instances observed during Phase-1 P1)
**Owner watchpoint:** all specialists
**Protocol ref:** hive-mind-protocol § 4.2 amendment; 2026-05-17 protocol § 14.1.1

### WP-HIVELOG-1: Fetch-before-commit required for hive log file

Before any specialist stages `engine-rebuild-log.md`:
1. `git fetch origin`
2. `git log --oneline -5 -- agentic_orchestration/hive-mind/engine-rebuild-log.md`
3. If remote has entries not in local: `git pull --rebase` first
4. Then stage by explicit path + commit

**Silent loss scenario:** two specialists commit hive log entries concurrently without fetching. One push wins; the other push fails silently (or worse, force-overwrites). Entries from the losing push are permanently gone.

**Trigger:** any specialist's hive log commit does not include evidence of a fetch + inspection step (i.e., commit message does not reference or the commit timestamp pattern implies concurrent editing without fetch). Jack-ryan cannot directly observe git fetch/pull operations, but CAN observe when hive log entries from one specialist appear to have displaced entries from another (missing entry gap in chronological log). File WARN on observed entry gap.

---

## WP-TAG — Tag discipline per workstream

**Risk level:** LOW
**Owner watchpoint:** all specialists + knight-rider
**Protocol ref:** hive-mind-protocol § 4.3 (inherited); coordination-matrix § 6 tag milestone plan; engineering-disciplines.md #6

### WP-TAG-1: Intermediate tags use per-seam namespace; milestone tags use hive-rebuild/ namespace

Intermediate tags: `<seam>/<workstream>-<sub-step>-<n>` (e.g., `gamora/r1-per-tier-math-1`, `rocket/r3-schema-draft-1`)
Milestone tags: `hive-rebuild/v0.<N>-<milestone>` (per coordination-matrix § 6 plan)

**Trigger:** a milestone-named tag (e.g., `hive-rebuild/v0.4-r3-schema-draft-committed`) is applied before the hypothesis-test passage criterion is met. Cross-check against coordination-matrix § 6 trigger conditions.

### WP-TAG-2: Never tag against smoke-test results alone (Discipline #6)

Every hive-rebuild/ milestone tag requires full-path validation (or the workstream-specific hypothesis test). Smoke-test-only results are insufficient for milestone tagging.

**Trigger:** a `hive-rebuild/` tag is pushed with only smoke-test passage as evidence. File WARN.

---

## WP-D14 — Discipline #14 (internal-vs-generative schema) for R8 LLM prompt surfaces

**Risk level:** MEDIUM
**Owner watchpoint:** rocket + star-lord (all LLM prompt-construction sites touched by R8)
**Protocol ref:** engineering-disciplines.md #14; dispatch R8 § methodology-first

### WP-D14-1: R8 pipeline modifications must not expose canonical-four labels in new LLM prompt sites

R8's post-convergence theme-coalescence call is a new LLM prompt-construction site. It must not expose:
- Canonical-four element labels (fire/water/earth/wind) as prompt structural keys
- Archetype-tag labels (warrior/mage/rogue/hunter) as explicit category descriptors
- Attribute axis labels (STR/DEX/INT) as explicit strings

The form-bias work (2026-05-16) found this pattern at six existing prompt sites. R8's new coalescence prompt must not add a seventh. Per-instance vocabulary only.

**Trigger:** gandalf's theme-coalescence prompt doc uses fire/water/earth/wind as structural keys in the prompt body. File WARN per Discipline #14 cross-reference.

### WP-D14-2: `--theme-input` legacy path must not re-expose canonical-four at new call sites

When `--theme-input` mode is active (legacy input-driven pipeline), R8's rocket implementation may create new LLM call sites to handle theme-as-input injection. Any new site created by R8 is subject to Discipline #14 (no canonical-four leakage) even in the legacy path.

**Trigger:** rocket's R8 pipeline design doc (`R8-pipeline-design-2026-05-19.md`) adds a new LLM call site for `--theme-input` mode that passes canonical-four element labels as structural keys. File WARN.

---

## WP-D17 — Discipline #17 (empirical-calibration smoke gate) for R1 class-retuning sprint

**Risk level:** MEDIUM
**Owner watchpoint:** gamora
**Protocol ref:** engineering-disciplines.md #17

### WP-D17-1: Class-retuning lever changes need smoke gate before full-cohort application

After R1 convergence loop ships and Test 1 reveals the failure cascade, gamora begins a class-retuning sprint. Each retuning lever (e.g., reducing boss-tier modifier, adjusting elite-tier resistances) must pass a parametric smoke gate (3 sweep points × representative instance threshold) before being applied to the full class cohort.

**Discipline #17 environment-fidelity amendment applies:** the smoke runner must include gear_catalog, monster_pool, and archetype generation parameters matching production. A gear-absent smoke runner will over-estimate lever effectiveness.

**Trigger:** gamora applies a class-retuning lever to the full cohort without documenting a smoke gate. File WARN per Discipline #17.

---

## Open watchpoints status (updated 2026-05-19, third jack-ryan session — implementation-phase observation pass)

| WP | Status | Last updated |
|---|---|---|
| WP-R1-A-1 (math note before balance_loop.py) | CLOSED — Gate 1 PASS `bf47591` preceded `3a73d94`; gamora STATE confirmed | 2026-05-19 impl-pass |
| WP-R1-A-2 (boss-tier n-shot strategy) | CLOSED — `FIGHT_BATCH_SIZE_BOSS=60` named constant at module level in `balance_loop.py` | 2026-05-19 impl-pass |
| WP-R1-B-1 (no silent aggregate-mean pass) | CLOSED — `_evaluate_convergence_gate()` is the authoritative gate; `aggregate_wr_legacy` is diagnostic-only with no code path accepting convergence on it | 2026-05-19 impl-pass |
| WP-R1-B-2 (per-tier failure to telemetry) | CLOSED — WARNING log + `balance_metadata["r1_per_tier_pass"]` write in `_evaluate_convergence_gate()`; not stdout-only | 2026-05-19 impl-pass |
| WP-R3-A-1 (schema field naming drift) | CLOSED — archetype vocabulary unified (`swarmer`/`controller`/`sniper`); both seams call same `_derive_r3_ai_fields()` function | 2026-05-19 impl-pass |
| WP-R3-A-2 (MIGRATION.md concurrent authoring) | CLOSED — both MIGRATION.md files exist with R3 entries; ADR-004 honored | 2026-05-19 |
| WP-R3-A-3 (schema validators fail-loud) | CLOSED — `@model_validator` operational on `monster_schema.py`; 220/220 monsters + 977/977 skills validated; boot-time boot-loud confirmed | 2026-05-19 impl-pass |
| WP-R3-A-4 (R3 critical-path silence watch) | CLOSED — R3 complete at `hive-rebuild/v0.5`; no extended silence observed | 2026-05-19 impl-pass |
| WP-R7-A-1 (parity-test spec before harness) | CLOSED — harness implements spec; WARN-R7-1 fix (direct key access) confirmed in implementation | 2026-05-19 impl-pass |
| WP-R7-A-2 (consumer audit enumeration) | CLOSED — movement.ts:74-78 and :81 both named in audit | 2026-05-19 |
| WP-R7-A-3 (Test 2 intentional-break required) | CLOSED — `test_intentional_break_fails_loud()` in spec § 7; `BrokenDemoAgentMock` confirmed in harness; 9/9 PASS | 2026-05-19 |
| WP-R7-A-4 (registry-iterate, not constant-fallback) | CLOSED — DemoAgentMock reads from JSON dict directly; missing field triggers KeyError (fail-loud); BrokenDemoAgentMock detects constant fallback | 2026-05-19 impl-pass |
| WP-R8-A-1 (methodology docs before A/B run) | CLOSED — both gandalf docs exist and are reviewed | 2026-05-19 |
| WP-R8-A-2 (cohesion scale anchoring) | CLOSED — Gate 1 PASS; anchors durable, blindness confirmed, decision-tree deterministic | 2026-05-19 |
| WP-R8-A-3 (Discipline #14 for coalescence prompt) | CLOSED — sanity skim confirms no canonical-four structural keys in prompt | 2026-05-19 |
| WP-R8-A-4 (--no-coalesce silent fill risk) | CLOSED — schema 2.10 + mode-tagged telemetry; pipeline gates coalesce call behind mode check; NULL for theme fields confirmed under no_coalesce | 2026-05-19 impl-pass |
| WP-MIGRATION-1 (R3 generation MIGRATION.md) | CLOSED — all 7 fields present in generation MIGRATION.md R3+R7 section | 2026-05-19 |
| WP-MIGRATION-2 (R3 export MIGRATION.md) | CLOSED — additive-only documented; consumer obligations stated | 2026-05-19 |
| WP-MIGRATION-3 (R7 cross-repo contract) | CLOSED — MIGRATION.md documents catalogue→demo read path; R7 harness validates it; R5 demo reads from JSON | 2026-05-19 impl-pass |
| WP-MIGRATION-4 (R8 LLM MIGRATION.md) | CLOSED — schema registered as 2.10 (not 2.8); MIGRATION.md status IMPLEMENTED; mode naming consistent | 2026-05-19 impl-pass |
| WP-MIGRATION-5 (R1 simulation MIGRATION.md) | CLOSED — `simulation/MIGRATION.md` v1.15 in same commit as `balance_loop.py` modification (`3a73d94`) | 2026-05-19 impl-pass |
| WP-XSEAM-1 (balance_loop concurrent edit) | CLOSED — gamora and rocket edited different file sets; no concurrent collision observed | 2026-05-19 impl-pass |
| WP-XSEAM-2 (monster JSON three-seam) | CLOSED — rocket schema first; elrond called rocket's helpers directly; star-lord receiver-boundary only | 2026-05-19 impl-pass |
| WP-XSEAM-3 (R7 source before R5 consumer) | CLOSED — `hive-rebuild/v0.7` precedes drax R5 dispatch activation per log sequencing | 2026-05-19 impl-pass |
| WP-HIVELOG-1 (fetch-before-commit) | OPEN — continuing monitoring; no entry gaps detected in this session | 2026-05-19 impl-pass |
| WP-TAG-1 (tag namespace discipline) | OPEN — continuing monitoring; tags observed all use correct namespaces | 2026-05-19 impl-pass |
| WP-TAG-2 (no tag against smoke-only) | OPEN — continuing monitoring; all milestone tags observed have full-path hypothesis test evidence | 2026-05-19 impl-pass |
| WP-D14-1 (coalescence prompt Discipline #14) | CLOSED — prior session | 2026-05-19 |
| WP-D14-2 (--theme-input new sites) | OPEN — rocket R8 pipeline shipped (`bfa3fc3`); no new LLM prompt sites observed that leak canonical-four as structural keys; monitoring | 2026-05-19 impl-pass |
| WP-D17-1 (retuning lever smoke gate) | CLOSED — sprint v3 5-class smoke + targeted reachability test executed before full 51-class sprint; Discipline #17 satisfied | 2026-05-19 gate1-pass |
| WP-R1-C-1 (Discipline #1 math note for R2) | CLOSED — math note `R2-spatial-combat-math-2026-05-19.md` precedes implementation in same commit `18dfc4c`; confirmed by Gate-1 review 2026-05-19 | 2026-05-19 r2-gate1 |
| WP-R2-A-1 (name-heuristic mis-classification) | ACTIVE-DEFERRED → two-stage gate (post-leash+timeout-disposition) — R2-RT v0.2 confirmed instrument MET; recalibration disposition addressed calibration saturation; engagement-geometry layer surfaced as third finding (mob leash + HP>50% timeout-survival). Resolves via two-stage gate per `canonical/story/r2-h1-leash-timeout-disposition-2026-05-19.md`: **Stage 1** (R2-RT v3 existing-catalogue diagnostic; partial close); **Stage 2** (R2-RT v4 on S1 regenerated catalogue gold-standard; full close). H1 original ≥ 0.10 threshold preserved across all three findings. | 2026-05-19 r2-leash-timeout-disp |
| WP-R2-B-1 (star-lord schema 2.12 round-trip) | OPEN — star-lord DB writer not yet implemented; gates production graduation tag | 2026-05-19 r2-gate1 |
| WP-R2-C-1 (damage calibration smoke before 51-class run) | OPEN — armor mitigation fix pending gamora next session | 2026-05-19 r2-gate1 |

**New watchpoints added this session (in-flight work):**

| WP | Owner | Condition | Risk |
|---|---|---|---|
| WP-R1-C-1 (retuning lever smoke gate per Discipline #17) | gamora | CLOSED 2026-05-19 gate1-pass — sprint v3 5-class smoke + targeted test before full sprint. Discipline #17 satisfied. | CLOSED |
| WP-R1-C-2 (rolling median future session) | gamora | When rolling median is added: window MUST reset on modifier change, not iteration count. Math note + docstring both document this. No action now; trigger if future implementation omits the reset. | LOW — future session only |
| WP-PLAYTEST-1 (v0.12 tag trigger) | knight-rider / drax | `hive-rebuild/v0.12-r5-hypothesis-test-passed` fires when Matt playtest confirms kite-default reduction (Test 2). Static-analysis 81% projection is credible but insufficient. | LOW — gate is clear |
| WP-PLAYTEST-2 (v0.16 tag trigger) | knight-rider / drax | `hive-rebuild/v0.16-r4-hypothesis-test-passed` fires when Matt playtest confirms Tests 1, 2, 4. Test 3 (out-of-range visual) is in-session verifiable NOW — knight-rider may fire that sub-criterion independently if useful. | LOW — gate is clear |

**New watchpoints added 2026-05-19 — jack-ryan R2 Gate-1 session:**

| WP | Owner | Condition | Risk |
|---|---|---|---|
| WP-R2-A-1 (name-heuristic mis-classification) | gamora | In 51-class full run: if `geometry_type_dominant = "mixed"` exceeds 20% of classes, investigate name-heuristic keyword collision. Threshold: >20% "mixed" triggers OBSERVATION. Resolution: VS2a `geometry_type` schema field. | LOW — scaffolding approximation; acceptable for hypothesis-test phase |
| WP-R2-B-1 (star-lord schema 2.12 round-trip) | star-lord | Production-graduation tag for R2 may NOT fire before star-lord's concrete `SpatialTelemetryWriter` DB writer is smoke-tested end-to-end: fight → `SpatialFightResult` → `write_fight_result()` → DB row queryable. `validate()` confirmed called before write. Pattern P7 at DB write boundary. | HIGH — R11(b) obligation |
| WP-R2-C-1 (damage calibration smoke before 51-class run) | gamora | Full 51-class R2 sprint must not fire before 5-class smoke (with armor mitigation fix applied) confirms non-degenerate WR (≥0.10 for at least 2 classes in open arena scenario). Discipline #17 environment-fidelity: smoke environment must include armor mitigation factor. | MEDIUM — Discipline #17 |

**New watchpoints added 2026-05-19 — gandalf R2 recalibration disposition session:**

| WP | Owner | Condition | Risk |
|---|---|---|---|
| WP-R2-A-2 (spatial calibration drift under post-disposition partition changes) | gamora | REFINED 2026-05-19 by leash+timeout disposition — was ACTIVE-MONITORING conditional re-test if partition shifts ≥ 10pp; now **ACTIVE-COMMITTED-RE-TEST** under S1 regenerated catalogue per Stage 2 gate (`canonical/story/r2-h1-leash-timeout-disposition-2026-05-19.md` § 6.2). Stage 2 R2-RT v4 on S1 catalogue IS the named re-test surface. Closes at Stage 2 PASS. | MEDIUM — committed to fire post-S1; not conditional |
| WP-R2-D-1 (recalibration math note + MIGRATION.md concurrent authoring per Discipline #1 + ADR-004) | gamora | CLOSED — recalibration impl commit `24cdc7e` included math note `R2-recalibration-math-2026-05-19.md` + MIGRATION.md v1.19 + Discipline #12 citation. 5-class smoke results in output dir. Constants NAMED. WP-R2-D-1 satisfied at impl-pass. | CLOSED 2026-05-19 r2-recalibration-impl |

**New watchpoints added 2026-05-19 — gandalf R2 leash + timeout disposition session (third R2 disposition pass):**

| WP | Owner | Condition | Risk |
|---|---|---|---|
| WP-R2-A-3 (engagement-geometry parity across scenarios under future scenario additions) | gamora + rocket (S1-side) + drax (demo-side) | Whenever a NEW spatial scenario is added (or existing scenario arena dimensions / spawn positions / leash / timeout outcome are modified), the leash override + timeout semantic must be set explicitly for the scenario at definition time, not implicit-defaulted to monster JSON values. PR review by jack-ryan Gate-1 confirms scenario-definition rationale block names leash override value + timeout outcome semantic. | MEDIUM — depends on whether R8 / S1 / R4 add new spatial scenarios |
| WP-R2-E-1 (leash + timeout math note extension + MIGRATION.md concurrent per Discipline #1 + ADR-004) | gamora | Leash + timeout impl commit MUST include `R2-recalibration-math-2026-05-19.md` § 10 extension (engagement-geometry math walkthrough) + `simulation/MIGRATION.md` entry concurrent. Discipline #12 cited in commit message. 5-class smoke results in output dir before Stage 1 R2-RT v3 run. Per-scenario leash override field is NAMED in SpawnSpec or ArenaScenario (no inline literals). | MEDIUM — Discipline #1 + #12 + ADR-004 |
| WP-R2-E-2 (two-stage validation gate sequencing) | gamora + knight-rider | Stage 1 (existing-catalogue R2-RT v3 diagnostic) fires after engagement-geometry impl + 5-class smoke PASS. Stage 2 (S1-catalogue R2-RT v4 gold-standard) fires after S1 first-batch validation gate PASS + S1 4-remaining-seasons regen completes. Tag `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` fires at Stage 1 PASS; tag `vs2a/v0.4-r2-h1-validated-on-S1-catalogue` fires at Stage 2 PASS; original `vs2a/v0.2-r2-h1-revalidated` tag REPLACED by two-tag schema. | LOW — gate is clear; knight-rider sequences |

---

## Closed watchpoints (updated 2026-05-19, third jack-ryan session)

| WP | Closed | Evidence |
|---|---|---|
| WP-R3-A-2 (MIGRATION.md concurrent authoring) | 2026-05-19 | generation/MIGRATION.md + export/MIGRATION.md both have R3 entries authored before implementation |
| WP-R7-A-2 (consumer audit enumeration) | 2026-05-19 | R7-consumer-audit § 5 names movement.ts:74-78 and :81 as primary sites |
| WP-R7-A-3 (Test 2 intentional-break required) | 2026-05-19 | R7-parity-test-spec § 7 includes test_intentional_break_fails_loud() |
| WP-R8-A-1 (methodology docs before A/B run) | 2026-05-19 | Both gandalf docs exist and reviewed; A/B run not yet fired |
| WP-R8-A-2 (cohesion scale anchoring) | 2026-05-19 | Gate 1 PASS; anchors durable; decision-tree deterministic |
| WP-R8-A-3 (Discipline #14 for coalescence prompt) | 2026-05-19 | Sanity skim confirms no canonical-four structural keys in LLM judge prompt or coalescence prompt |
| WP-MIGRATION-1 (R3 generation MIGRATION.md) | 2026-05-19 | All 7 new fields present in [2026-05-19] R3+R7 section |
| WP-MIGRATION-2 (R3 export MIGRATION.md) | 2026-05-19 | Additive-only decision documented; no breaking changes; consumer obligations stated |
| WP-R1-A-1 (math note before balance_loop.py) | 2026-05-19 impl-pass | Gate 1 PASS `bf47591` preceded implementation commit `3a73d94` |
| WP-R1-A-2 (boss-tier n-shot strategy) | 2026-05-19 impl-pass | `FIGHT_BATCH_SIZE_BOSS=60` named constant in balance_loop.py |
| WP-R1-B-1 (no silent aggregate-mean pass) | 2026-05-19 impl-pass | `_evaluate_convergence_gate()` is the sole acceptance gate; aggregate_wr_legacy is diagnostic-only |
| WP-R1-B-2 (per-tier failure to telemetry) | 2026-05-19 impl-pass | WARNING log + balance_metadata write in `_evaluate_convergence_gate()` |
| WP-R3-A-1 (schema field naming drift) | 2026-05-19 impl-pass | Both seams call `_derive_r3_ai_fields()`; archetype vocabulary unified |
| WP-R3-A-3 (schema validators fail-loud) | 2026-05-19 impl-pass | `@model_validator` on monster_schema.py; 220/220 + 977/977 PASS |
| WP-R3-A-4 (R3 critical-path silence) | 2026-05-19 impl-pass | R3 complete; no silence observed |
| WP-R7-A-1 (parity-test spec before harness) | 2026-05-19 impl-pass | WARN-R7-1 fix confirmed in harness; 9/9 PASS |
| WP-R7-A-4 (registry-iterate, not constant-fallback) | 2026-05-19 impl-pass | DemoAgentMock direct key access; KeyError fail-loud; BrokenDemoAgentMock detection confirmed |
| WP-R8-A-4 (--no-coalesce silent fill risk) | 2026-05-19 impl-pass | Pipeline mode check gates coalesce call; NULL theme fields under no_coalesce confirmed |
| WP-MIGRATION-3 (R7 cross-repo contract) | 2026-05-19 impl-pass | MIGRATION.md documents path; harness validates it; R5 reads from JSON |
| WP-MIGRATION-4 (R8 LLM MIGRATION.md) | 2026-05-19 impl-pass | Schema 2.10 registered correctly; mode naming consistent |
| WP-MIGRATION-5 (R1 simulation MIGRATION.md) | 2026-05-19 impl-pass | simulation/MIGRATION.md v1.15 in same commit as balance_loop.py modification |
| WP-XSEAM-1 (balance_loop concurrent edit) | 2026-05-19 impl-pass | Different file sets; no collision |
| WP-XSEAM-2 (monster JSON three-seam) | 2026-05-19 impl-pass | Rocket schema first; elrond called rocket's helpers; star-lord receiver-boundary |
| WP-XSEAM-3 (R7 source before R5 consumer) | 2026-05-19 impl-pass | v0.7 precedes drax R5 activation |

*Watchpoints close when the specific condition is verified via hive log entry, tag, or direct code observation. Jack-ryan updates this table and files a corresponding hive log OBSERVATION on each closure.*

---

*Established 2026-05-19 by jack-ryan. Engine-rebuild scope read. Watchpoints cover the load-bearing disciplines per protocol § 4.5 + § 9. The math note comes before the code; the MIGRATION.md comes before the consumer; the parity test fails loud on intentional break; the hive log is fetched before committed. These are the four pillars this rebuild stands on. Jack-ryan watches.*
