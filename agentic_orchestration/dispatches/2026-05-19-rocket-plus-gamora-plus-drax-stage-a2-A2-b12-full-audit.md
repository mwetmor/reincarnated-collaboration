# Dispatch — 2026-05-19 — rocket + gamora + drax — Stage A2 A2 B12 full audit

**From:** knight-rider
**To:** rocket (catalogue schema + slots + affixes OWNER) + gamora (sim consumer) + drax (UI per A6 framework)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when Stage A2 kicks off + A6 framework lands
**Estimated effort:** ~1.5–2 weeks (rocket schema + gamora sim consumer + drax UI)
**Acceptance:** Per § Acceptance. Tag fires: `stage-a2/v0.2-b12-full-audit-complete`.
**Hive context:** Stage A2 closeout hive — A2 closes B12 audit deferred from VS2a (only +% MS values shipped in VS2a per movement-speed cascade; B12 full audit adds boots/gloves/belt + affixes + hard-cap).

---

## Context

Per `canonical/28-engine-arpg-rebalance-design.md` B12 + `canonical/16-project-roadmap.md` § VS2a "Out of scope for VS2a" + § "Stage A2 forward-audit watch-items":

VS2a shipped +% MS values per Matt verdict reversal (Option-B 8.0/5.75/7.5/0.719 lock). B12 FULL audit adds:
- Boots / gloves / belt gear slots to catalogue
- +% MS affixes per slot per rarity
- Hard-cap on aggregate MS modifier (~50% per ARPG canon)
- UI surfaces (per A6 design framework § A)

A2 is the cross-seam closure dispatch.

---

## Required reading

In order:
1. `canonical/28-engine-arpg-rebalance-design.md` B12 (full spec)
2. A6 dispatch + framework doc `canonical/story/stage-a2-design-watch-items-framework-2026-05-19.md` § A (B12 visual/UX)
3. VS2a movement-speed baseline: `canonical/story/movement-speed-baseline.md` § "Verdict Reversal"
4. S3 dispatch + completion record (Gate-3b sim MS extension) — MS source-of-truth pattern
5. `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` + `simulation/AGENT_STATE.md`
6. `reincarnated-demo/AGENT_STATE.md` + `reincarnated-loadout/AGENT_STATE.md`
7. `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` + `export/MIGRATION.md`
8. `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.2 (A2)
9. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

### Rocket scope (catalogue schema + slots + affixes)

- [ ] Boots / gloves / belt gear-slot schema additions
- [ ] +% MS affixes per slot per rarity (per B12 spec)
- [ ] Hard-cap on aggregate MS modifier (engine-side cap; sim consumes)
- [ ] Generator emits new slots on regen
- [ ] Schema validator enforces additive non-null post-backfill
- [ ] MIGRATION.md appended at generation seam
- [ ] AGENT_STATE.md updated

### Gamora scope (sim consumer)

- [ ] Sim consumes boots/gloves/belt slot effects in fight engine
- [ ] Aggregate MS modifier with hard-cap honored in sim
- [ ] Telemetry: per-fight MS modifier breakdown captured
- [ ] MIGRATION.md appended at sim seam if telemetry extends
- [ ] AGENT_STATE.md updated

### Drax scope (UI per A6 framework § A)

- [ ] Loadout app: boots/gloves/belt slot grid layout
- [ ] +% MS modifier VFX in demo (per A6 § A.2)
- [ ] Hard-cap UX cue (per A6 § A.3)
- [ ] Tooltips per existing pattern
- [ ] MIGRATION.md at `reincarnated-demo/MIGRATION.md` + `reincarnated-loadout/MIGRATION.md` if cross-loadout-internal contract surfaces
- [ ] AGENT_STATE.md updated

### Joint scope

- [ ] Round-trip smoke per Principle 6: generator emits boots/gloves/belt + affixes → sim consumes + applies cap → telemetry captures → export → loadout UI renders + demo VFX renders
- [ ] Hive log: STATE on rocket start + HANDOFF rocket → gamora + HANDOFF gamora → drax + completion STATE
- [ ] Tag fire request: `stage-a2/v0.2-b12-full-audit-complete`

---

## Cross-seam contract change? (Principle 6 gate)

**YES** — gear schema additive (boots/gloves/belt + affixes); sim consumer extension; UI consumer extension. Three seams.

**MIGRATION.md REQUIRED at all three:**
- Rocket: `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (slot + affix additions + hard-cap value)
- Gamora (if telemetry extends): `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- Drax: `reincarnated-demo/MIGRATION.md` + `reincarnated-loadout/MIGRATION.md` per consumer-side contract

**Round-trip smoke REQUIRED**: end-to-end fixture exercising generator → sim → telemetry → export → loadout + demo render.

---

## Acceptance criteria

- [ ] Boots/gloves/belt slots operational in catalogue + generator emits
- [ ] +% MS affixes per slot per rarity operational
- [ ] Hard-cap enforced in sim
- [ ] UI: loadout slot grid + demo VFX + cap UX cue rendered
- [ ] Round-trip smoke per Principle 6
- [ ] MIGRATION.md at all three seams (gen + sim + demo/loadout)
- [ ] Smoke-test GREEN
- [ ] All three seams' AGENT_STATE.md updated
- [ ] Hive log entries appropriate
- [ ] Tag: `stage-a2/v0.2-b12-full-audit-complete`

---

## Out of scope

- B7 gear-variance gate (A1; upstream sim work)
- B13 mobility geometries (A3)
- B14 multi-band convergence (A4)
- B16 loot drop architecture (A5)
- Per-season MS variation (Phase 1+ territory)
- Audio cues for +% MS active (Phase 1+)
- Localization

---

## Open questions for the agents

- **Hard-cap value** — L1 rocket per B12 spec + A6 framework. ~50% per ARPG canon; confirm
- **Affix tier distribution** — L1 rocket; tier-based rarity + magnitude
- **Sim telemetry surface** — L1 gamora + star-lord consult if class_fight_loadouts or class_balance_results extends
- **Loadout slot grid layout** — L1 drax per A6 § A.1 framework
- **VFX intensity per modifier tier** — L1 drax per A6 § A.2 (light particle / strong particle / etc.)
- **Cap UX cue** — L1 drax per A6 § A.3 ("MAX" indicator vs greyed slot vs tooltip warning)

---

## References

- `canonical/28-engine-arpg-rebalance-design.md` B12
- A6 framework doc (upstream)
- VS2a movement-speed baseline + S3 dispatch
- `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.2
- All three seams' AGENT_STATE.md
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** Stage A2 kickoff + A6 framework lands.

**Post-activation:** rocket leads schema; gamora consumes; drax consumes per A6 framework. L1 within seams. No Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. A2 completes the gear-slot inventory + finalizes MS as an earned axis of investment per `canonical/16-project-roadmap.md` § VS2a "Explicit non-coverage" (deferred from VS2a).*
