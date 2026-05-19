# Dispatch — 2026-05-19 — gandalf — Stage A2 A7 Playtest Cycle 1 prep + execution + disposition

**From:** knight-rider
**To:** gandalf (design-steward — rubric + observation framework + disposition OWNER) + knight-rider (coordination) + Matt (playtester at execution step; HELD for wind-down)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when A1+A2+A3+A4+A5+A6 land
**Estimated effort:** prep ~2 days gandalf; execution ~1 day Matt (HELD); disposition ~2-3 days gandalf post-execution
**Acceptance:** Per § Acceptance. Tag fires: `stage-a2/v1.0-stage-a2-ship` (Stage A2 CLOSED at disposition).
**Hive context:** Stage A2 closeout hive — A7 is the **closing dispatch**. Three phases: autonomous prep + Matt-gated execution + autonomous disposition.

---

## TL;DR

Playtest Cycle 1 is the first formal playtest checkpoint per `canonical/16-project-roadmap.md` § "Playtest Cycle 1":

> Post-Stage-A2 closeout (~1-2 weeks). Skill tree UI comprehensibility, gauntlet density feel, mobility geometries, telegraphs, mobile-first auto-pickup, loot drop density.

**Three phases:**

1. **Prep (autonomous)** — gandalf authors playtest rubric + observation framework + capture cadence
2. **Execution (Matt-gated; HELD for wind-down)** — Matt plays through VS2a regen (season_001003) + VS2b regen (season_001005) + Stage A2 additions; observations captured per rubric
3. **Disposition (autonomous post-Matt-playtest)** — gandalf authors playtest cycle report + recommendations; routes to roadmap for Stage A3 sequencing decision

---

## Context

Per protocol pattern: playtest cycles are Matt-gated by design — Matt IS the playtester (per session memory + `agentic_orchestration/AGENTS.md` § Matt-role). Knight-rider + gandalf prepare; Matt plays; gandalf dispositions.

Per `canonical/16-project-roadmap.md` § "Track A landing rhythm" + "Single-season-per-playtest rule (LOCKED 2026-05-12)": Stage A2 closeout does NOT regen new season; uses VS2a regen (season_001003) + VS2b regen (season_001005) as playtest substrate.

Per `canonical/16-project-roadmap.md` § "What comes after VS2a + VS2b":
- Stage A3 (B9 series) follows Playtest Cycle 1
- Stage A3 design fully resolved 2026-05-12 in file 32 — gandalf can author Stage A3 scope-of-work post-A7 disposition (pre-approval-batch decision deferred to Matt at wind-down)

---

## Phase 1 — Playtest Cycle 1 prep (autonomous; ~2 days gandalf)

### Deliverable: rubric + observation framework

**Path:** `agentic_orchestration/playtest/playtest-cycle-1-rubric-2026-05-19.md`

(Or wherever gandalf's standing playtest convention places it; create new directory if needed.)

**Coverage axes per roadmap § "Playtest Cycle 1":**
- Skill tree UI comprehensibility (consumes VS2a F4 prototype + B6 main work)
- Gauntlet density feel (consumes B10 already-shipped + S2 + L1 ship)
- Mobility geometries (consumes A3 B13 post-narrow-slice)
- Telegraphs (consumes A3 telegraph-art per A6 § B)
- Mobile-first auto-pickup (consumes A5 B16)
- Loot drop density (consumes A5 B16 + A2 B12 gear-slot inventory)

**Rubric structure (gandalf authors per convention):**
- Per-axis observation prompts + capture format
- Calibration anchors (what's "comprehensible" vs "confused" on skill tree; what's "satisfying" vs "thin" on gauntlet density; etc.)
- Playthrough cadence (suggested play session length; capture cadence)
- Cross-axis synthesis prompts (e.g., "does mobility feel coherent with telegraph?")
- Recommendation framework: each axis lands as PASS / ITERATE / RE-DISPOSITION
- Cross-reference to combined VS2a regen (season_001003) + VS2b regen (season_001005) as playtest substrate per single-season-per-playtest rule extension (here: two seasons; both regenerated under Stage A2 additions)

**Observation framework:**
- Self-capture conventions for Matt (note-taking + video if desired)
- Surface format for sending observations back to gandalf at disposition phase
- Capture cadence (per-session or per-axis)

---

## Phase 2 — Playtest execution (Matt-gated; HELD for wind-down)

### Matt-side scope

- Matt opens wind-down session post-Stage-A2 ship
- Plays through VS2a regen (season_001003) + VS2b regen (season_001005) per rubric guidance
- Observes Stage A2 additions in context (boots/gloves/belt gear slots from A2; mobility geometries from A3; telegraphs from A3 + A6; loot drops from A5)
- Captures observations per rubric format
- Routes observations back to gandalf via standing communication channel

### Knight-rider coordination

- Knight-rider stands ready at wind-down to:
  - Brief Matt on rubric + playtest scope
  - Pre-load VS2a + VS2b regen seasons in demo + loadout
  - Coordinate any technical readiness (assets loaded; environment pack per M1 selection if landed; etc.)
- M1 (Drift-15 environment pack) + M2 (engine-rebuild playtest tags) + A7 execution can co-occur in single Matt wind-down session

---

## Phase 3 — Playtest Cycle 1 disposition (autonomous post-Matt-playtest; ~2-3 days gandalf)

### Deliverable: playtest cycle report + recommendations

**Path:** `canonical/story/playtest-cycle-1-disposition-2026-05-19.md`

(Or per gandalf's standing disposition convention.)

**Content:**

1. **Per-axis observations summary** — Matt's observations digested into per-axis verdict (PASS / ITERATE / RE-DISPOSITION)
2. **Cross-axis synthesis** — gandalf design-judgment on emergent patterns + integration cohesion
3. **Recommendations** — Stage A3 sequencing considerations + any retroactive Stage A2 ITERATE items
4. **Decisions-log entry** (jack-ryan routes) capturing Playtest Cycle 1 arc + outcomes
5. **Forward routing** — Stage A3 (B9 series) ready for pre-approval-batch authoring (deferred to Matt at next wind-down session decision) OR retroactive Stage A2 ITERATE if needed

---

## What you are NOT doing

- **NOT regenerating new seasons** (single-season-per-playtest rule; VS2a + VS2b regens are the substrate)
- **NOT amending Stage A2 specs retroactively** (ITERATE items surface as future dispatches per disposition)
- **NOT escalating execution-phase decisions to Matt during play** (Matt plays; gandalf dispositions; routine cadence)
- **NOT authoring Stage A3 scope-of-work in A7** (separate dispatch; deferred to Matt's pre-approval-batch decision)

---

## Cross-seam contract change? (Principle 6 gate)

**Design + canonical-story authoring + Matt playtest session.** No production code change in A7.

**Round-trip: not applicable — playtest cycle authoring + execution + disposition. Retroactive ITERATE items (if any) surface as future production dispatches with their own round-trip smoke requirements.**

---

## Acceptance criteria

### Phase 1 (autonomous prep)

- [ ] Playtest Cycle 1 rubric authored
- [ ] Observation framework authored
- [ ] Capture cadence + format specified
- [ ] Hive log: gandalf STATE on prep authoring complete + readiness signal to knight-rider for Matt wind-down
- [ ] Tag fire request: `stage-a2/v0.7-playtest-cycle-1-prep-complete`

### Phase 2 (Matt-gated execution)

- [ ] Matt plays VS2a regen + VS2b regen per rubric
- [ ] Observations captured + routed to gandalf
- [ ] Knight-rider coordinates wind-down session technical readiness

### Phase 3 (autonomous disposition)

- [ ] Playtest cycle report authored at `canonical/story/playtest-cycle-1-disposition-2026-05-19.md` (or per convention path)
- [ ] Per-axis verdicts (PASS / ITERATE / RE-DISPOSITION) documented
- [ ] Cross-axis synthesis authored
- [ ] Recommendations for Stage A3 sequencing surfaced
- [ ] Decisions-log entry authored (jack-ryan routes)
- [ ] Forward routing surfaced for Stage A3 pre-approval-batch decision (deferred to Matt)
- [ ] Tag fire request: `stage-a2/v1.0-stage-a2-ship` (Stage A2 CLOSED at disposition)
- [ ] Hive log: gandalf STATE on disposition authored + retrospective entries on playtest signal
- [ ] CHANGELOG entry: Stage A2 CLOSED event

---

## Out of scope

- New regen seasons (single-season-per-playtest rule)
- Stage A3 scope-of-work authoring (deferred)
- Phase 0 ship-readiness assessment (Playtest Cycle 4 territory)
- Audio playtest (post-Phase-0)
- Stage A4+ playtest cycles (each has its own cycle)
- Per-class deep balance retrospective (Stage A2 retrospective only)

---

## Open questions for the agents

- **Rubric depth vs breadth** — L1 gandalf. Rich per-axis or lean cross-axis? Playtest Cycle 1 is first formal cycle; baseline rubric depth + room for refinement in cycles 2-4
- **Combined VS2a + VS2b playtest cohesion** — same player walks through both regen seasons; rubric captures combined arc + per-season specifics
- **M1 Drift-15 environment-pack integration timing** — if F6-D drax integration has not landed at playtest time, geometric environment placeholders persist; rubric notes this caveat
- **ITERATE items routing** — if Stage A2 ITERATE surfaces (e.g., loot drop density needs re-tuning), gandalf authors retroactive dispatch; knight-rider routes
- **Stage A3 scope-of-work timing** — gandalf can author proposal post-A7 disposition; pre-approval-batch decision deferred to Matt at next wind-down
- **Knight-rider's wind-down briefing** — what context does Matt need to playtest effectively? L1 knight-rider per playtest brief convention

---

## References

- `canonical/16-project-roadmap.md` § "Playtest Cycle 1" + § "Track A landing rhythm" + § "What comes after VS2a + VS2b"
- A1 + A2 + A3 + A4 + A5 + A6 dispatches (upstream)
- VS2a F4 dispatch (B6 skill-tree UI per playtest axis)
- VS2a L1 + VS2b V6 ship gates (regen seasons that form playtest substrate)
- `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.7 (A7) + § 5 (continuation)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9 + § 6.5 (forward routing)

---

## Autonomous-operation authority + activation gate

**Activation gates:**
- Phase 1 (prep): A1 + A2 + A3 + A4 + A5 + A6 all land
- Phase 2 (execution): Phase 1 prep + Matt wind-down session (HELD)
- Phase 3 (disposition): Phase 2 observations routed back to gandalf

**Post-Phase-3 forward routing:** Stage A3 scope-of-work decision deferred to Matt at next wind-down session — knight-rider stands ready to extend pre-approval-batch through Stage A3 if Matt requests.

**Matt-gated step:** Phase 2 execution only. Phase 1 prep + Phase 3 disposition are autonomous.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. A7 closes Stage A2. The player walks the two regen seasons; gandalf disposes the playtest; the engine's ARPG-rebalance design queue closes; Stage A3 awaits Matt's next gate.*
