# Dispatch — 2026-05-16 — star-lord — Stage B export-DTO fix (movement_speed field) — VS2a-gating

**From:** knight-rider (authored per Matt directive Day-4 close: "authorize all four" — MS verdict reversal cascade item #3; promoted from medium-time-critical to severity-HIGH-VS2a-gating)
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** QUEUED — fires after your in-flight Stage 3 cipher migration returns. Per Matt's authorization of my (a) recommendation: let Stage 3 complete; queue Stage B; do not violate per-seam one-dispatch-per-session by parallel-firing.
**Estimated effort:** 1 session (~3-4h); ExportClass + ExportMonster DTO fix; smoke + MIGRATION.md + intermediate tag

**Gate-1 bypass rationale:** Matt-directed (verdict-reversal cascade explicitly authorized), single-seam (star-lord export only), VS2a-gating (delaying = blocking the entire engine-to-demo MS pipeline).

**Acceptance summary:** ExportClass + ExportMonster DTOs ship `movement_speed` field through consolidated JSON (and any other VS2a-relevant fields the prior gandalf finding identified). Smoke verifies engine-emitted movement_speed lands in consolidated JSON for fresh class/monster instances. MIGRATION.md entry. Intermediate tag.

---

## Why this dispatch exists

Per gandalf's MS verdict-reversal cascade (item #3):

> star-lord: Stage B export-DTO fix (the finding I just filed) — PRECONDITION for #5; demo can't consume engine-emitted MS until ExportClass + ExportMonster ship the field through consolidated JSON

**Severity:** medium-time-critical → **HIGH-VS2a-gating** per Matt's verdict reversal. Under old plan, drax hardcoded mid-game MS values and engine schema was decorative. Under new plan, drax consumes engine-emitted MS from JSON — if Stage B drops the field at the boundary, drax has no MS to render with. Hardcoded fallback would re-introduce the workaround we're closing.

This dispatch IS the load-bearing path enabling end-game-anchored VS2a playtest.

## Cross-seam contract change?

**Round-trip: YES — additive `movement_speed` field on export DTOs.**

- **Acceptance criteria includes:** round-trip smoke verifying field flows from rocket schema → engine instance → ExportClass/ExportMonster DTO → consolidated JSON → drax-consumable shape
- Boundary check: field-presence assertion on consolidated JSON output for fresh class + fresh monster
- Downstream consumer: drax MS-consume dispatch (queued; fires after this + rocket schema-defaults both return)
- Per R11(b) Principle 6 operationalized 2026-05-16

## What this dispatch produces

### Step 1 — Locate gandalf's filed finding

Gandalf filed the Stage B export-DTO finding ~20 min before Matt's verdict reversal Day-4 close. Check `agentic_orchestration/gandalf/findings/` or `agentic_orchestration/research/` (or wherever gandalf's recent findings land). Pick up scope from there — it may identify additional VS2a-relevant fields beyond movement_speed alone.

If finding not located: contact knight-rider for routing rather than expanding scope unilaterally.

### Step 2 — ExportClass DTO update

Add `movement_speed: float` field to ExportClass DTO. Wire from `class.movement_speed` (rocket cascade item #2 sets default to 8.0 end-game player baseline).

### Step 3 — ExportMonster DTO update

Add `movement_speed: float` field to ExportMonster DTO. Wire from `monster.movement_speed` (rocket per-archetype: trash 5.75 / fast 7.5 / named-boss gamora-design-call).

### Step 4 — Consolidated JSON emission

Verify the field flows through to the final consolidated JSON shape drax consumes. If serializer is auto-derived from DTO, this is automatic. If serializer is hand-rolled, update.

### Step 5 — Smoke test (Discipline #2 + R11(b) round-trip)

- Generate a fresh class via rocket; export to consolidated JSON; verify `movement_speed=8.0` present
- Generate a fresh trash monster; verify `movement_speed=5.75` in JSON
- Generate a fresh fast-archetype monster; verify `movement_speed=7.5` in JSON
- Boundary field-presence assertion (not null; correct type)
- Existing export tests pass

### Step 6 — MIGRATION.md entry (ADR-004)

- v2.x bump (next in your sequence after V2.4 modifier_flag_tier; pick v2.5 unless Stage 3 cipher migration introduced its own)
- Downstream consumer notes: drax MS-consume dispatch (queued); gamora sim consumption (Gate 3b firing parallel)
- Upstream anchor: rocket schema-defaults (parallel); gandalf canonical update (parallel)

### Step 7 — Tag + AGENT_STATE + completion record

- Intermediate tag: `star-lord/v1.3-stage-b-export-dto-movement-speed`
- AGENT_STATE updated
- Fill completion record

## Out of scope (explicit)

- **NO Stage 3 cipher migration touchpoints** (just-completed work; do not regress)
- **NO schema-default edits** (rocket's seam)
- **NO sim consumption code** (gamora Gate 3b)
- **NO demo / drax code** (drax MS-consume queued)
- **NO new V2 telemetry fields** (Stage B is the export-DTO seam, not the telemetry-schema seam — different lane)
- **NO live DB migration to data/telemetry.db** (separate ADR-006 authorization)
- **NO scope expansion beyond gandalf finding + movement_speed** (if finding identifies additional VS2a-relevant fields, those are in-scope; do not add others)

## Required reading

- Gandalf's Stage B export-DTO finding (locate per Step 1)
- Gandalf's MS verdict-reversal cascade (Matt-relayed Day-4 close)
- `canonical/story/movement-speed-baseline.md` (gandalf updating in parallel)
- Rocket MS schema-defaults dispatch (parallel; upstream source)
- Your prior export work + existing MIGRATION.md (DTO patterns)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #2 smoke, #11 attribution, R11(b) cross-seam round-trip

## Acceptance criteria

- [ ] Gandalf finding located + scope confirmed
- [ ] ExportClass DTO has movement_speed field
- [ ] ExportMonster DTO has movement_speed field
- [ ] Consolidated JSON emission verified (round-trip smoke)
- [ ] Boundary field-presence assertion
- [ ] Existing export tests pass; new smoke tests pass
- [ ] MIGRATION.md entry filed with downstream consumer notes
- [ ] Intermediate tag `star-lord/v1.3-stage-b-export-dto-movement-speed` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, gandalf-finding additional-field scope (if any), unblocks-drax-MS-consume confirmation

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-stage-b-export-dto-movement-speed`
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Gandalf finding path:** `agentic_orchestration/gandalf/findings/2026-05-16-export-dto-stage-b-silent-drop.md`
**Additional VS2a-relevant fields in scope:** movement_speed only. Gandalf's finding identifies 10+ additional silently-dropped fields (embodiment_tag, grouping_pair_structure, convergence_report, etc.) — all are VS2b or later scope, not VS2a-relevant per the dispatch scope clause. No scope expansion taken.
**Intermediate tag:** `star-lord/v1.3-stage-b-export-dto-movement-speed @ a08bd6e`
**Tests status:** 39/39 export tests pass (31 pre-existing + 8 new round-trip smoke tests). Round-trip confirmed: class default → 8.0 in classes.json; monster default → 5.75 in monsters.json; explicit values survive Stage B boundary; Stage B validator raises on movement_speed=0.0. Full seam smoke (export + movement_speed + telemetry + cipher migration guard): 254/254 pass.
**Notes for knight-rider:**
- Drax MS-consume dispatch (`2026-05-16-drax-engine-emitted-ms-consumption.md`) is NOW UNBLOCKED on the star-lord side. Dispatch fires when this + rocket-schema-defaults both return. Rocket-schema-defaults was in-flight parallel (a103f7513d7eedcf4 per dispatch notes); confirm rocket seam is back before firing drax.
- Full Stage B DTO fix (all 10+ silently-dropped fields per gandalf finding) is still open. This dispatch closes VS2a-gating field only. The broader Track A commission from `agentic_orchestration/gandalf/requests/2026-05-16-star-lord-export-dto-stage-b-fix-and-r11b.md` needs a separate dispatch authored when ready.
- Stage B boundary validator is in place in `season_exporter.py`. Current coverage: `_STAGE_B_REQUIRED_CLASS_FIELDS` + `_STAGE_B_REQUIRED_MONSTER_FIELDS` — scoped to VS2a surface. Recommend expanding frozensets as future fields are wired through ExportClass/ExportMonster.
