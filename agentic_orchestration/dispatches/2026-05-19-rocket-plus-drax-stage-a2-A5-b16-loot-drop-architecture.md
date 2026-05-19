# Dispatch — 2026-05-19 — rocket + drax — Stage A2 A5 B16 loot drop architecture

**From:** knight-rider
**To:** rocket (drop rules + auto-pickup architecture OWNER) + drax (visual presentation OWNER per A6 § C framework)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when Stage A2 kicks off + A6 framework lands
**Estimated effort:** ~1.5–2 weeks (rocket drop rules + drax visual layer)
**Acceptance:** Per § Acceptance. Tag fires: `stage-a2/v0.5-b16-loot-drop-architecture`.
**Hive context:** Stage A2 closeout hive — A5 closes B16 (Drift-12 candidate filing). Loot architecture + visual layer + auto-pickup feedback.

---

## Context

Per `canonical/28-engine-arpg-rebalance-design.md` B16 + A6 framework § C (loot visual presentation layer):

A5 closes:
- Drop rules engine: per-tier loot drop rates + rarity distribution
- Auto-pickup architecture (mobile-first standard)
- Visual presentation: drop animation + loot beams + rarity colors + tooltips + auto-pickup feedback (per A6 § C)
- Drift-12 filing: loot visual presentation layer was implicit-deferred (P6 pattern); files as Drift-12 in drift-audit at A5 closure

---

## Required reading

In order:
1. `canonical/28-engine-arpg-rebalance-design.md` B16 (full spec)
2. A6 dispatch + framework doc § C (loot visual presentation layer)
3. `canonical/story/drift-audit.md` (Drift-12 forward-flag location; A5 closes)
4. Pet system memory (`agentic_orchestration/memory/project_pet_system.md` — auto-pickup with rarity filter is Stage A3 demo follow-on territory; A5 establishes the base architecture pet system extends)
5. `canonical/story/style-register.md` (HD-2D-pixel-art register for visual layer)
6. `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` + `reincarnated-demo/AGENT_STATE.md`
7. `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.5 (A5)
8. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

### Rocket scope (drop rules + auto-pickup architecture)

- [ ] Drop rules engine: per-monster-tier drop rates (per B16 spec)
- [ ] Rarity distribution per rarity-tier (common / magic / rare / elite / legendary; per A6 § C.3 locked palette)
- [ ] Auto-pickup architecture: mobile-first standard; rarity filter hooks (pet system extension surface in Stage A3)
- [ ] Drop telemetry: per-fight drop counts + rarity breakdown captured (star-lord consumer)
- [ ] MIGRATION.md appended at generation seam
- [ ] AGENT_STATE.md updated

### Drax scope (visual presentation per A6 § C)

- [ ] Drop animation: loot drops with arc + landing-bounce (per A6 § C.1)
- [ ] Loot beams: per-rarity color beams + HD-2D-pixel register (per A6 § C.2)
- [ ] Rarity colors per locked palette (per A6 § C.3)
- [ ] Tooltips: gear name + rarity + key affixes on hover/tap; mobile + desktop UX (per A6 § C.4)
- [ ] Auto-pickup feedback: particle on auto-pickup (audio deferred; visual only)
- [ ] MIGRATION.md at `reincarnated-demo/MIGRATION.md`
- [ ] AGENT_STATE.md updated

### Joint scope

- [ ] Round-trip smoke per Principle 6: monster killed → drop rules fire → drop telemetry captured → demo renders drop animation + beam + auto-pickup feedback
- [ ] **Drift-12 entry filed** in `canonical/story/drift-audit.md` per A6 § D framework
- [ ] Hive log: STATE per seam + HANDOFF rocket → drax + completion STATE
- [ ] Tag fire request: `stage-a2/v0.5-b16-loot-drop-architecture`

---

## Cross-seam contract change? (Principle 6 gate)

**YES** — drop rules engine + drop telemetry surface + demo visual layer.

**MIGRATION.md REQUIRED:**
- Rocket: `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (drop rules contract; telemetry surface)
- Drax: `reincarnated-demo/MIGRATION.md` (visual layer extension)
- Star-lord (if telemetry table extends): `reincarnated-engine/src/reincarnated/export/MIGRATION.md`

**Round-trip smoke REQUIRED**: end-to-end fixture; field-presence + render-presence check.

---

## Acceptance criteria

- [ ] Drop rules engine operational per B16 spec
- [ ] Rarity distribution per A6 § C.3 palette
- [ ] Auto-pickup architecture operational (mobile-first; pet-system extension surface preserved)
- [ ] Visual layer: drop animation + loot beams + tooltips + auto-pickup feedback rendered
- [ ] Drop telemetry captured
- [ ] Drift-12 entry filed
- [ ] Round-trip smoke per Principle 6
- [ ] MIGRATION.md at rocket + drax + star-lord (if extended)
- [ ] Smoke-test GREEN
- [ ] Both seams' AGENT_STATE.md updated
- [ ] Hive log entries appropriate
- [ ] Tag: `stage-a2/v0.5-b16-loot-drop-architecture`

---

## Out of scope

- B7 gear-variance (A1)
- B12 gear slot expansion (A2; A5 consumes A2's slot inventory but doesn't extend)
- B13 mobility geometries (A3)
- B14 multi-band convergence (A4)
- Pet-system rarity filter implementation (Stage A3 territory per memory `project_pet_system.md`)
- Audio cues (Phase 1+)
- Localization (post-Phase-0)
- Per-class loot tuning (beyond B16 base rates)
- Boss-specific loot tables (out of B16 spec; potential VS2c+ extension)

---

## Open questions for the agents

- **Drop rate per monster tier** — L1 rocket per B16 spec
- **Rarity palette hex values** — L1 gandalf in A6 § C.3 framework; drax applies
- **Auto-pickup radius** — L1 rocket + drax joint per mobile-first standard
- **Pet-system extension hooks** — L1 rocket. Preserve seam for Stage A3 pet system (rarity filter integration point)
- **Drop animation duration** — L1 drax per A6 § C.1; mobile-first responsive
- **Cross-with-A2 gear-slot integration** — drop rules emit gear in A2 slot inventory; sequencing ensures A2 lands before A5 round-trip smoke
- **Drift-12 prevention prescription** — gandalf authors in A6 framework; A5 consumes

---

## References

- `canonical/28-engine-arpg-rebalance-design.md` B16
- A6 dispatch + framework doc § C + § D
- `canonical/story/drift-audit.md`
- `canonical/story/style-register.md`
- Memory `project_pet_system.md` (Stage A3 pet rarity filter extension surface)
- `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.5
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** Stage A2 kickoff + A6 framework lands.

**Post-activation:** rocket leads drop rules; drax consumes visual layer per A6 framework. L1 within seams. No Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. A5 closes the loot architecture; the player gets drops; the rarity beams light the catalogue; Drift-12 is filed as the last visual axis P6 instance.*
