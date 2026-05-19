# Dispatch — 2026-05-19 — rocket + star-lord — VS2a `geometry_type` per-skill schema field

**From:** knight-rider
**To:** rocket (generation seam — schema + catalogue OWNER), star-lord (operational pipeline seam — telemetry + export adaptation OWNER)
**Approved by:** AUTONOMOUS — VS2a hive-mind continuation under Matt directive 2026-05-19 (engine-rebuild closure → VS2a sequencing; no per-dispatch Matt approval; design routing pre-confirmed per R2 H1 disposition § 3.1 + jack-ryan Q1 disposition / `gate1-r2-math-note-2026-05-19.md`)
**Estimated effort:** 2–4 weeks parallel with kit-redesign sprint (S1) — can fire IMMEDIATELY without gating on F2
**Acceptance:** New `geometry_type` enum field operational in skill schema + 5-shipped-season backfill + `_determine_geometry_type()` updated to direct-field-read with fail-loud Pattern-P7 on missing values + MIGRATION.md authored + R2 H1 re-test under original variance ≥ 0.10 threshold staged as gated downstream gamora work. Tag fires: `vs2a/v0.1-geometry-type-schema-shipped`; re-test tag `vs2a/v0.2-r2-h1-revalidated` when gamora completes downstream re-test.
**Hive context:** VS2a hive ACTIVE; engine-rebuild v1.0 batch CLOSED. F1 is a **first-fire batch** dispatch — fires immediately under autonomous mode, no upstream gate. Resolves the R2 H1 instrument-limitation cleanly via the architectural pre-condition gandalf's R2 H1 disposition § 3.1 named.

---

## Context — why this is in front of you

R2 H1 disposition (`canonical/story/r2-h1-disposition-2026-05-19.md`) committed `hive-rebuild/v0.14-r2-hypothesis-test-passed` under a revised 4-sub-claim category-of-completion frame. **Sub-claim 4** explicitly names the architectural pre-condition that re-enables H1 under the original variance ≥ 0.10 threshold:

> **VS2a `geometry_type` per-skill schema field** (per jack-ryan Q1 disposition) re-enables H1 under original variance ≥ 0.10 threshold; re-test gate documented in § 3.2.

This dispatch IS that architectural pre-condition.

The current state:
- `spatial_engine._determine_geometry_type()` uses a **name-heuristic** keyword classifier (point / circle / cone / line / mixed / none)
- Across the 51-class catalogue, the heuristic produces a **43/3/4 distribution** (43 "point" classes; 3 "circle"; 4 "cone")
- The 43/3/4 imbalance collapses the variance metric: variance = 0.017 (threshold 0.10)
- The underlying spatial signal IS operative (point mean WR 0.721 vs cone/circle 1.000 = 28pp delta in the correct direction); the instrument cannot measure it
- WP-R2-A-1 watchpoint (jack-ryan-filed) anticipated this exact pattern; resolution mechanism = this dispatch

When this dispatch ships:
- Skills carry their geometry as data, not as keyword-collision lottery
- The heuristic becomes a *fallback only* with fail-loud Pattern P7 enforcement on `mixed` / `none` when the value should exist
- Gamora's R2 sub-gauntlet re-run under explicit field tests H1 under the ORIGINAL threshold (per R2 disposition § 3.2 forward routing)
- Engineering Discipline #13 drift watchpoint WP-R2-A-1 closes
- The catalogue gains a *first-class* design lever that VS2a kit-redesign work (S1) can use directly (range-diversity criterion § 3.1 of `r1-kit-redesign-queue-2026-05-19.md` benefits from explicit geometry tagging)

This is a cross-seam contract change with broad blast radius. MIGRATION.md required at both producing-seam (rocket) and telemetry/export-seam (star-lord). Field is additive + backward-compatible by default; fail-loud-on-missing is enforced post-backfill.

---

## Required reading before starting

**Both of you, in order:**

1. **`canonical/story/r2-h1-disposition-2026-05-19.md`** — particularly § 3.1 (forward routing for VS2a `geometry_type` schema field), § 3.2 (H1 re-test gate), § 3.3 (WP-R2-A-1 closure)
2. **`agentic_orchestration/hive-mind/gate1-r2-math-note-2026-05-19.md`** — jack-ryan's Q1 disposition + WP-R2-A-1 filing (the watchpoint this dispatch resolves)
3. **`canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`** § 4.0 autonomous-operation + § 4.4 cross-seam coordination + § 4.5 jack-ryan continuous-observation + Discipline #13 drift watch
4. **`agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.1 (F1)** — F1 deliverables
5. **`agentic_orchestration/hive-mind/coordination-matrix-vs2a.md`** § 1 (F1 row) + § 3 concurrent-edit hot-spots (skill JSON schema is multi-seam) + § 4 MIGRATION.md
6. **`reincarnated-engine/src/reincarnated/simulation/spatial_engine.py`** — current `_determine_geometry_type()` heuristic (the function being augmented; not replaced — heuristic stays as fallback)
7. **`reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — particularly Discipline #1 (math-before-code; schema design before implementation), Discipline #11 (attribution), P7 (silent-default / fail-loud), Discipline #13 (drift watch)
8. **`agentic_orchestration/GOVERNANCE.md`** — ADR-004 MIGRATION.md requirement; ADR-006 push authority
9. **The 5 shipped seasons** on disk under `reincarnated-engine/output/` — for backfill scope assessment

**Rocket additionally reads:**
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — your last checkpoint (post-R8 disposition impl; commit `9f6e4e6`)
- `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — existing migrations to append to
- Current skill schema definition (skill JSON fields; existing `range_m` field shipped under R3)
- Output evidence: `reincarnated-engine/output/R2-sprint-2026-05-19/R2-test1.md` (the H1 result that motivated this dispatch)

**Star-lord additionally reads:**
- `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` — your last checkpoint (post-schema 2.12)
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — existing migrations
- Current telemetry schema (`spatial_fight_results` table is the most affected; `class_balance_results` may also extend; `class_fight_loadouts` if per-fight skill-geometry breakdown is wanted)
- Round-trip parity-test harness shipped under R7 (your test surface for this dispatch)

---

## Math-before-code (Discipline #1)

**Not math-load-bearing**, but **design-then-build pattern applies strictly.** Authoring required before implementation:

### Rocket-led schema design draft

**Path:** `reincarnated-engine/design/working-agreement/F1-geometry-type-schema-design-2026-05-19.md`

Captures:

1. **Enum definition.** `geometry_type` ∈ `{circle, cone, line, point, mixed, none}`. Document each value's semantic meaning:
   - `circle` — AOE radial damage around target or self; e.g., explosion, nova
   - `cone` — directional AOE; e.g., breath weapon, wide swipe
   - `line` — linear projectile or beam; e.g., bolt, beam, lance
   - `point` — single-target; e.g., melee strike, single-target bolt
   - `mixed` — multi-shape skill (rare; e.g., shotgun-cone-with-point-impact); document when this is legitimately used vs fallback
   - `none` — no spatial geometry (self-buff, channel, passive); document when this is legitimately used

2. **Backfill derivation rules** for the 5 shipped seasons (rocket + elrond if elrond capacity needed — F1 elrond involvement is OPTIONAL per coordination matrix § 1; rocket can self-author if seasonal regen is the chosen backfill path):
   - **Option A:** Re-derive from existing `_determine_geometry_type()` heuristic outputs on each skill in each shipped season (faster; preserves seed identity; may carry some name-heuristic mis-classifications forward — acceptable, since re-test under explicit field still surfaces signal)
   - **Option B:** Re-roll skill geometry-types at next-regen as generation-time field (more expensive — would require kit-redesign coordination via S1; not the right shape for this dispatch)
   - **Recommendation:** Option A, with rocket reading sample-class outputs + auditing mis-classifications manually for the 10 worst kit-broken classes (per `r1-kit-redesign-queue-2026-05-19.md` evidence) so backfill quality is higher than pure heuristic
   - Idempotency: re-run backfill on already-backfilled season produces no diff
   - Validation: post-backfill content passes existing engine schema validators + every skill has a `geometry_type` value (no nulls)

3. **`_determine_geometry_type()` fallback semantics.** Function continues to exist but operates as:
   - First: read explicit `geometry_type` field from skill JSON
   - Fallback: if field missing (legacy season pre-backfill), apply heuristic + emit telemetry warning (Discipline #13 drift signal — captured as `geometry_type_fallback_applied: true` on the fight log)
   - Fail-loud: if field is `mixed` or `none` AND the call-site expects a measurable geometry (e.g., spatial_engine's geometry-class-WR analyzer), raise + log per Pattern P7 — do NOT silently fall back to "point" default
   - Document call-sites that may need to special-case `mixed` / `none` vs treat them as opaque

4. **Schema migration shape:**
   - Field is **additive** + **nullable initially** + **non-nullable post-backfill** (after backfill executes successfully, schema validator enforces non-null on every skill)
   - No schema_version bump required for additive-nullable; bump REQUIRED at non-null enforcement step. Document the two-stage migration explicitly.
   - Backward-compat: legacy season manifests without the field continue to work via heuristic fallback + telemetry warning

5. **Cross-cutting impact:** which other code paths read geometry-type:
   - `spatial_engine._determine_geometry_type()` (this is the canonical call-site; updates per § 3)
   - Any R2 sub-gauntlet code paths that classify skills by geometry (these become direct field reads)
   - Any future S1 kit-redesign code paths (range-diversity criterion + archetype-alignment criterion may want geometry-type as explicit decision variable; rocket forward-flags but does not implement here)

Star-lord appends section to this design doc capturing telemetry / export surface impact (next subsection).

### Star-lord-led telemetry / export design

**Same doc as above** (rocket + star-lord co-author; rocket writes first; star-lord appends `## Telemetry + Export Surface` section).

Captures:

1. **`spatial_fight_results` field additions.** Currently captures geometry-class via heuristic-derived dominant-skill geometry. Post-F1:
   - Emit `geometry_type_source: explicit | heuristic_fallback` per fight (Discipline #13 drift telemetry)
   - Emit `geometry_type` value per fight as before, now sourced from explicit field where available
   - Decision: extend table additively (preferred) or bump schema_version

2. **`class_balance_results` field additions.** If R2 H1 re-test wants per-class geometry-type captured at class-balance-results level (separate from per-fight): rocket + star-lord decide whether to add field or compute via join. L1 star-lord decision; document in MIGRATION.md.

3. **`class_fight_loadouts` field additions.** Per-fight loadout already captures skill IDs; geometry-type is derivable via skill JSON read. Decision: extend loadout dict to include geometry-type at write-time (faster downstream analysis) or leave as joined-at-analysis-time. L1 star-lord; document.

4. **Round-trip parity-test extension.** Existing R7 parity-test harness should validate that the explicit `geometry_type` field is preserved through generator → telemetry → export → consumer round-trip. Field-presence check at each boundary. This is the **Principle 6 round-trip smoke** for F1; surface in acceptance.

5. **MIGRATION.md content** (star-lord's section at `reincarnated-engine/src/reincarnated/export/MIGRATION.md`):
   - New field per skill; semantic meaning; default if missing (`null` initially; enforced non-null post-backfill)
   - Telemetry additive vs breaking decision + rationale
   - Consumer obligations (gamora R2 re-test consumer; future S1 consumer; loadout if downstream consumes)

**Jack-ryan reviews the design doc before commit** under continuous-observation rhythm (no separate Gate 1 dispatch; jack-ryan watches per protocol § 4.5).

---

## Cross-seam contract change? (Principle 6 gate)

**YES — explicit cross-seam contract change.** This is the textbook MIGRATION.md case.

**Affected boundaries:**
- Skill JSON schema (rocket emitter → all consumers: gamora sim + R2 re-test, drax demo if downstream consumes geometry signal, star-lord telemetry, elrond if backfill curation needed)
- `spatial_fight_results` table (star-lord; new fields)
- `class_balance_results` table (star-lord; field decision per § design above)
- Fight log dict (gamora → star-lord boundary; new geometry-source field optional)
- Season `manifest.json` IF schema_version bumps at non-null enforcement step (engineer the version bump carefully — pre-backfill ships at v_N; post-backfill enforces at v_N+1)

**MIGRATION.md REQUIRED:**
- Rocket appends to `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — schema change + backfill plan + consumer obligations + idempotency
- Star-lord appends to `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — telemetry surface changes + additive-vs-breaking decision + consumer rebuild requirements

**Round-trip smoke REQUIRED.** End-to-end fixture:
- Generator emits skill with explicit `geometry_type` field
- Telemetry recorder captures per-fight geometry-type from explicit field (verifies fallback NOT triggered when field present)
- Export packet contains the field
- Consumer (gamora R2 re-test the canonical consumer; loadout if downstream geometry-relevant)
- Field-presence check at each boundary
- Negative case: legacy season pre-backfill exercises fallback path; warning emitted; Discipline #13 drift telemetry captured

---

## Scope (both seams, coordinated)

### Rocket scope (schema + catalogue + sim consumer)

- [ ] Schema design draft authored at `reincarnated-engine/design/working-agreement/F1-geometry-type-schema-design-2026-05-19.md`
- [ ] MIGRATION.md appended at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` concurrently with schema change
- [ ] `geometry_type` enum field added to skill JSON schema (additive + nullable initially)
- [ ] Generator emits explicit `geometry_type` for newly generated skills (current default value: derived via existing heuristic at generation-time + recorded as explicit; rocket can also adopt a richer generation-time heuristic, your call within seam)
- [ ] Backfill executed across 5 shipped seasons per § 2 design (Option A heuristic re-derive with manual audit on 10 worst-pathology classes; idempotent)
- [ ] Schema validator updated: non-null `geometry_type` enforced post-backfill (two-stage migration)
- [ ] `spatial_engine._determine_geometry_type()` updated to direct-field-read with heuristic fallback + Pattern-P7 fail-loud on `mixed` / `none` where measurable geometry is expected
- [ ] Fight log dict emits `geometry_type_source` for Discipline #13 drift telemetry
- [ ] AGENT_STATE.md updated
- [ ] Tag fire request surfaced in hive log: `vs2a/v0.1-geometry-type-schema-shipped` (knight-rider fires)

### Star-lord scope (telemetry + export adaptation)

- [ ] `## Telemetry + Export Surface` section appended to F1 schema design doc
- [ ] MIGRATION.md authored at `reincarnated-engine/src/reincarnated/export/MIGRATION.md` for telemetry surface change
- [ ] `spatial_fight_results` table extended additively per design § telemetry
- [ ] `class_balance_results` and/or `class_fight_loadouts` extended per L1 decision
- [ ] Round-trip parity-test extension implemented (field-presence check at each boundary)
- [ ] Negative-case test: legacy season exercises fallback path; warning emitted
- [ ] AGENT_STATE.md updated

### Joint scope (round-trip smoke + handoff)

- [ ] Round-trip smoke fixture exercising: generator emits explicit field → telemetry captures with `source: explicit` → export packet contains → consumer reads correctly. Negative case: legacy season uses fallback path → `source: heuristic_fallback` → warning logged.
- [ ] Smoke-test GREEN throughout (each seam's commits leave engine GREEN per protocol § 4.5)
- [ ] Hive log entries: STATE on each seam's start; HANDOFF at producer → consumer boundary; OBSERVATION on any Discipline #13 drift surface
- [ ] Handoff to gamora for R2 H1 re-test: rocket + star-lord surface STATE entry indicating field is ready + backfill complete + re-test fixture is in shape; knight-rider authors gamora re-test dispatch (separate; tags `vs2a/v0.2-r2-h1-revalidated`)

---

## Acceptance criteria

- [ ] Schema design draft authored before any production code change
- [ ] MIGRATION.md (generation + export) authored concurrently with producing-seam work
- [ ] `geometry_type` field operational in skill catalogue (new generation) + 5-shipped-season backfill complete + validator enforces non-null post-backfill
- [ ] `spatial_engine._determine_geometry_type()` direct-field-read with heuristic fallback + Pattern-P7 fail-loud
- [ ] Discipline #13 drift telemetry captured (`geometry_type_source` field per fight)
- [ ] Round-trip smoke per Principle 6: generator → telemetry → export → consumer; field-presence check at each boundary; negative-case legacy-season fallback path tested
- [ ] Smoke-test GREEN throughout
- [ ] Both seams' AGENT_STATE.md updated
- [ ] Hive log entries: STATE / HANDOFF / OBSERVATION as required
- [ ] Tag fire request surfaced (`vs2a/v0.1-geometry-type-schema-shipped`)
- [ ] WP-R2-A-1 closure surface entered in `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (or new VS2a watchpoints file) when re-test passes — that closure happens at the downstream gamora re-test dispatch, NOT in this dispatch; rocket + star-lord surface the *readiness* for that closure here

---

## Out of scope (explicit non-goals)

- **Re-running the R2 sub-gauntlet H1 re-test.** That's gamora's downstream dispatch (separately authored by knight-rider once F1 ships); tags `vs2a/v0.2-r2-h1-revalidated`. Rocket + star-lord ship the architectural pre-condition + readiness signal; gamora executes the re-test.
- **Kit-redesign work (S1).** F1 is independent of F2 / S1 — fires in parallel. Even if F2 chooses path (b) R8-inversion regeneration, the regen still uses the same `geometry_type` field; rocket can have the regen consume the field as a generation-time constraint (gandalf's F2 disposition may clarify).
- **B6 main work (S2).** F1 doesn't gate or block S2.
- **Spatial-boss recalibration.** R2 H1 disposition § 3.4 forward-flagged this as DEFERRED (potentially VS2b territory); not in scope for this dispatch.
- **Telegraph-window / aggro-radius / leash schema fields** — those shipped under R3; F1 is geometry-type ONLY.
- **Demo runtime consumption** of `geometry_type` (drax). Drax decides per AGENT_STATE if/when downstream consumption is wanted; not blocking F1 ship.
- **Loadout consumption** of geometry-type. Out of scope; future surface if loadout analytics wants it.

---

## Open questions for the agents to resolve (in-seam L1 / cross-seam L2 routing)

- **Backfill strategy: Option A heuristic re-derive vs Option B re-roll at next regen** — L1 rocket. My recommendation: Option A with manual audit on 10 worst-pathology classes. Document choice in design doc.
- **Schema validator non-null enforcement timing** — L1 rocket. Two-stage migration (additive-nullable first; non-null after backfill) is the cleanest path. Document choice.
- **Star-lord telemetry additive vs breaking** — L1 star-lord. Additive is the strong default (per ADR-004). Document choice in MIGRATION.md.
- **`mixed` and `none` semantic boundary cases** — L1 rocket judgment + L2 surface to gandalf if cross-cutting design tension surfaces (e.g., "should a multi-stage skill that opens with a cone then becomes a circle be `cone` or `mixed`?"). Document the convention adopted.
- **Sample-class manual audit list** — L1 rocket. Pick the 10 most-extreme kit-broken classes (per `r1-kit-redesign-queue-2026-05-19.md` § 1.1 + sprint v2/v3 evidence) — class_0018, class_0045, class_0016, class_0008, class_0019, class_0033, class_0038, class_0060 + 2 more per your read.
- **Schema_version bump** — L1 star-lord + rocket joint. Likely bumps at non-null enforcement step; document explicit version number in MIGRATION.md.
- **F2 R8-inversion coordination** — if gandalf's F2 disposition lands during F1 and chooses path (b) regeneration, rocket determines whether F1 backfill is still required for the 5 shipped seasons (yes — even if path (b) replaces them with new seasons, the 5 shipped seasons remain canonical telemetry sources for R2 H1 re-test and need the field). Confirm via hive log STATE if it surfaces.

---

## References

- `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.1, § 3.2, § 3.3 (forward routing for F1 + re-test gate + watchpoint closure)
- `agentic_orchestration/hive-mind/gate1-r2-math-note-2026-05-19.md` (jack-ryan Q1 disposition + WP-R2-A-1 filing)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.4 + § 4.5
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.1 (F1)
- `agentic_orchestration/hive-mind/coordination-matrix-vs2a.md` § 1 + § 3 + § 4 (DAG + concurrent-edit hot-spots + MIGRATION.md)
- `agentic_orchestration/GOVERNANCE.md` (ADR-004 MIGRATION.md; ADR-006 push authority)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1, #11, #13, P7)
- `reincarnated-engine/src/reincarnated/simulation/spatial_engine.py` (current `_determine_geometry_type()` heuristic)
- `reincarnated-engine/output/R2-sprint-2026-05-19/R2-test1.md` (H1 result motivating this dispatch)
- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` § 1.1 (worst-pathology class evidence for manual audit list)

---

## Autonomous-operation authority (no Matt-wait)

Per launch dispatch § 3 + protocol § 4.0 (inherited):

- **In-seam decisions** — L1 specialist; no escalation
- **Cross-seam decisions** — L2 via knight-rider in hive log
- **Design-direction question** (e.g., enum semantic boundary) — surface to gandalf via hive log if cross-cutting
- **No Matt-wait at any point during F1.** Matt re-enters only at wind-down.
- **Tag-firing** — surface request in hive log; knight-rider fires + pushes per ADR-006 amendment.

---

*Authored 2026-05-19 by knight-rider under autonomous-operation authority. F1 fires immediately. The instrument R2 H1 needed becomes the catalogue's first-class design lever. The heuristic stays as fallback; the field becomes truth; the re-test under the original threshold becomes possible.*
