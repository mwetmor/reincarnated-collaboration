# Dispatch — 2026-05-19 — rocket + gamora — Stage A2 A3 B13 post-narrow-slice

**From:** knight-rider
**To:** rocket (catalogue + generator role-tagging + trait-pool OWNER) + gamora (sim AI + observability OWNER) + drax (telegraph UI consumer per A6 § B)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when Stage A2 kicks off + A6 framework lands
**Estimated effort:** ~2.5–3 weeks (down from original 3–4 weeks per narrow-slice reduction)
**Acceptance:** Per § Acceptance. Tag fires: `stage-a2/v0.3-b13-post-narrow-slice-complete`.
**Hive context:** Stage A2 closeout hive — A3 closes the ~75% of B13 deferred post-narrow-slice (Phase-1 P1 Deliverable 28 shipped ~25%).

---

## Context

Per `canonical/16-project-roadmap.md` § "B13 scope reduction (2026-05-17 L3 narrow-slice decision)" + `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 7 + `canonical/32-progression-design.md` § 12.5 Amendment 2026-05-17:

**Narrow-slice already-shipped (Phase-1 P1 Deliverable 28):**
- Universal dodge mechanic ✓
- Enemy-AOE telegraph indicators ✓
- Elite-tier reactive escape AI ✓
- Cross-doc updates ✓

**A3 closes the remaining ~75% B13-proper scope:**
- 5 defensive mobility geometries as kit-pool additions: `roll` / `defensive_dash` / `strafe_mode` / `blink` / `dodge_stance`
- Mini-boss + boss strategic / anticipatory / substrate-coherent escape AI (extends elite-tier reactive AI)
- Archetype-emergence observability (telemetry surface)
- Mobility role-tagging in generator
- Full B13 trait-pool extension surface
- Telegraph-art UI per A6 § B framework

---

## Required reading

In order:
1. `canonical/16-project-roadmap.md` § "B13 scope reduction" + § Stage A2 forward-audit watch-items
2. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 7 (narrow-slice scope + remaining B13-proper)
3. `canonical/32-progression-design.md` § 12.5 Amendment 2026-05-17 (narrow-slice locks + B13-proper open items)
4. `canonical/28-engine-arpg-rebalance-design.md` B13 (full spec)
5. A6 dispatch + framework doc § B (telegraph-art convention)
6. Phase-1 P1 Deliverable 28 completion record (universal dodge + AOE telegraph indicators + elite-tier reactive AI)
7. F1 dispatch + completion record (`geometry_type` per-skill schema — mobility geometries become explicit `geometry_type` consumers)
8. S2 dispatch (B6 tree-aware convergence — mobility geometries integrate into tree-structured kit composition)
9. `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` + `simulation/AGENT_STATE.md`
10. `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.3 (A3)
11. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

### Rocket scope (catalogue role-tagging + mobility geometries + trait-pool)

- [ ] 5 defensive mobility geometries added to skill pool: `roll` / `defensive_dash` / `strafe_mode` / `blink` / `dodge_stance`
  - Each has explicit `geometry_type` (per F1 schema)
  - Each has `mobility_role_tag` (new field; per narrow-slice spec convention)
  - Each integrates into tree-structured kit composition (per B6 / S2)
- [ ] Generator role-tagging: archetype generation considers mobility-coverage as criterion (per § 3 R1 kit-redesign queue criterion expansion)
- [ ] B13 trait-pool extension surface (per `canonical/32-progression-design.md` § 12.5)
- [ ] MIGRATION.md appended at generation seam
- [ ] AGENT_STATE.md updated

### Gamora scope (sim AI + observability)

- [ ] Mini-boss + boss strategic / anticipatory / substrate-coherent escape AI
  - Strategic: AI considers player position + class kit before AOE / telegraph fire
  - Anticipatory: AI projects player movement trajectory + adjusts AOE placement
  - Substrate-coherent: AI behaviors are coherent with monster substrate (water-substrate boss kites; earth-substrate boss roots)
- [ ] Archetype-emergence observability: telemetry capture for AI behavior patterns + emergent archetypes
- [ ] Sim consumer for 5 new mobility geometries (per rocket emission)
- [ ] MIGRATION.md appended at sim seam
- [ ] AGENT_STATE.md updated

### Drax scope (telegraph UI per A6 § B)

- [ ] Telegraph-art convention applied per A6 § B: primitive-rendered with locked color/opacity in HD-2D-pixel register
- [ ] Per-shape (circle/cone/line/point) telegraph rendering
- [ ] Per-tier intensity (trash/elite/boss) windup-duration calibration
- [ ] Mobile-first responsive
- [ ] AGENT_STATE.md updated

### Joint scope

- [ ] Round-trip smoke per Principle 6: generator emits mobility geometry + role-tagging → sim AI consumes + emergent observability → telemetry captures → demo renders telegraphs
- [ ] B13 hypothesis test per spec: mobility geometries surface in catalogue + sim emergent archetype observability operational + telegraph UI player-readable
- [ ] Hive log: STATE entries per seam + HANDOFF at boundaries + completion STATE
- [ ] Tag: `stage-a2/v0.3-b13-post-narrow-slice-complete`

---

## Cross-seam contract change? (Principle 6 gate)

**YES** — skill schema additive (mobility geometries + `mobility_role_tag` field); sim AI extension; demo telegraph UI extension.

**MIGRATION.md REQUIRED at all three seams.**

**Round-trip smoke REQUIRED** end-to-end.

---

## Acceptance criteria

- [ ] 5 mobility geometries in catalogue with role-tagging
- [ ] Trait-pool extension operational
- [ ] Mini-boss + boss escape AI operational; substrate-coherent
- [ ] Archetype-emergence observability captured
- [ ] Telegraph UI per A6 § B framework
- [ ] Round-trip smoke per Principle 6
- [ ] MIGRATION.md at gen + sim + demo seams
- [ ] Smoke-test GREEN
- [ ] All three seams' AGENT_STATE.md updated
- [ ] Tag: `stage-a2/v0.3-b13-post-narrow-slice-complete`

---

## Out of scope

- Universal dodge mechanic (already-shipped narrow-slice)
- Enemy-AOE telegraph indicators baseline (already-shipped narrow-slice)
- Elite-tier reactive escape AI (already-shipped narrow-slice)
- B14 multi-band convergence (A4)
- B7 gear-variance (A1)
- Audio cues for telegraphs (Phase 1+)
- New monster archetypes beyond mobility-aware extensions (out)

---

## Open questions for the agents

- **Per-geometry sim integration cost** — L1 gamora. Some mobility geometries (e.g., `blink`) may need new sim primitives; others (e.g., `roll`) extend existing
- **Mobility-role-tag values** — L1 rocket. Recommendation: `escape` / `repositioning` / `defensive` / `aggressive` per common ARPG taxonomy; document choice
- **Boss substrate-coherence convention** — L1 gamora + gandalf consult if cross-cutting (e.g., is fire-substrate boss "kite" or "rush"?)
- **Observability telemetry shape** — L1 gamora + star-lord consult; new fields likely needed on class_fight_loadouts or spatial_fight_results
- **Trait-pool integration** — L1 rocket per § 12.5 Amendment 2026-05-17; document trait-pool entries that gate mobility-geometry unlock

---

## References

- `canonical/16-project-roadmap.md` § "B13 scope reduction"
- `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 7
- `canonical/32-progression-design.md` § 12.5 Amendment
- `canonical/28-engine-arpg-rebalance-design.md` B13
- A6 dispatch + framework doc § B
- Phase-1 P1 Deliverable 28 completion
- F1 + S2 dispatches (geometry_type + tree-structured kit consumers)
- `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.3
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** Stage A2 kickoff + A6 framework lands.

**Post-activation:** rocket + gamora L1 within seams; gandalf L2 consult on substrate-coherence convention. No Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. A3 closes B13-proper; the player gets defensive mobility tools; the bosses learn to anticipate; the telegraphs become the readable language of combat.*
