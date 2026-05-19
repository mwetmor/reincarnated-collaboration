# Dispatch — 2026-05-19 — drax + elrond — VS2b V5 full Pimen catalogue integration

**From:** knight-rider
**To:** drax (demo VFX integration OWNER) + elrond (Pimen curation completion OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); extends VS2a C2 + C4 in-flight work; can begin at VS2b kickoff in parallel with V1 + V4
**Estimated effort:** ~1–1.5 weeks (drax integration ~1 week + elrond curation completion ~3–5 days)
**Acceptance:** Per § Acceptance. Tag fires: `vs2b/v0.5-pimen-full-integration`.
**Hive context:** VS2b hive — V5 extends VS2a C2 (11/13 GREEN-list element VFX) + C4 (Pimen curation pipeline) to FULL catalogue coverage. Required for VS2b ship trigger ("Pimen full integration").

---

## Context

Per `canonical/16-project-roadmap.md` § VS2a scope:
- C2 (B11 GREEN-list element VFX) ships 11/13 elements during VS2a (in-flight per drax AGENT_STATE)
- C4 (Pimen curation pipeline + subset selection) in-flight per elrond AGENT_STATE

Per `canonical/16-project-roadmap.md` § VS2b ship trigger:
- "Pimen full integration" is one of four ship-trigger components

V5 closes the gap between VS2a's 11/13 partial + VS2b's "full" — covering:
- Remaining 2 GREEN-list elements (12/13 + 13/13)
- Non-GREEN-list Pimen catalogue elements relevant to VS2b season composition
- Final curation pass on Pimen catalogue for cross-element completeness

---

## Required reading

In order:
1. `canonical/16-project-roadmap.md` § VS2a (C2 + C4 framing) + § VS2b (ship trigger)
2. VS2a scope-of-work § 2.6 + § 2.7 (C2 + C4 in-flight context)
3. Drift-14 framework (F3 + F5 + V4 convergence) — culled-pool affects which Pimen elements remain in scope
4. `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (Pimen catalogue inventory)
5. `canonical/story/geometry-vfx-coverage-assessment.md`
6. `canonical/story/style-register.md` (HD-2D register coherence)
7. `reincarnated-demo/AGENT_STATE.md` (drax checkpoint — C2 in-flight status)
8. elrond AGENT_STATE.md (Pimen curation in-flight status)
9. `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.5 (V5)
10. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

### Drax scope (demo VFX integration completion)

- [ ] Complete remaining 2/13 GREEN-list element VFX integrations (from VS2a C2 11/13)
- [ ] Integrate non-GREEN-list Pimen catalogue elements relevant to VS2b season composition (per V6 regen target season_001005's expected element distribution)
- [ ] Verify per-element VFX presence in demo across full Pimen-covered element set
- [ ] HD-2D register coherence pass per `style-register.md`
- [ ] Attribution credits coherent across all integrated Pimen elements (F1 credits overlay; existing convention)
- [ ] AGENT_STATE.md updated

### Elrond scope (Pimen curation completion)

- [ ] Complete curation pipeline for full Pimen catalogue (extends C4 in-flight)
- [ ] Subset selection finalized: which Pimen elements ship in VS2b vs deferred to VS2c+
- [ ] Curation metadata captured per existing convention (vendor metadata + license + intrinsic frame sizes + integration tier)
- [ ] Cross-reference Drift-14 culled-pool (F5 output) to ensure Pimen elements align with vfx-mapping tiers
- [ ] AGENT_STATE.md updated

### Joint scope

- [ ] Cross-seam handoff: elrond curation completion signals drax integration readiness for each element
- [ ] Smoke pass: demo renders full Pimen-covered element set without VFX gaps or register-coherence regressions
- [ ] Visual regression screenshot captured (drax direct per galadriel sub-agent restriction)
- [ ] Hive log STATE entries on completion each seam
- [ ] Tag fire request: `vs2b/v0.5-pimen-full-integration`

---

## Cross-seam contract change? (Principle 6 gate)

**Demo VFX asset integration + curation metadata; no schema or contract change.**

**MIGRATION.md** if Pimen integration pattern shifts (e.g., new element-tier metadata field). L1 drax + elrond decision; document if surfaces.

**Round-trip smoke**: demo loads season → VFX catalogue resolves → all integrated elements render. Field-presence + render-presence check.

---

## Acceptance criteria

- [ ] Full Pimen catalogue coverage operational in demo (12/13 → 13/13 GREEN-list + non-GREEN-list elements relevant to VS2b)
- [ ] Curation completion: elrond AGENT_STATE.md confirms pipeline final pass
- [ ] HD-2D register coherence verified across full integrated set
- [ ] Attribution credits coherent
- [ ] Visual regression smoke + screenshot captured
- [ ] Both seams' AGENT_STATE.md updated
- [ ] Hive log entries: drax STATE on integration progress + elrond STATE on curation completion + HANDOFF at each element handoff + completion STATE
- [ ] Tag: `vs2b/v0.5-pimen-full-integration`

---

## Out of scope

- Non-Pimen vendor expansion (separate VS2c+ legolas sweep territory)
- Demo-side embodiment surface (post-VS2b)
- New chierit character commissioning (post-VS2b)
- Substrate-identity declarations amendment (already locked)
- VS2a C2 + C4 baseline work (in-flight; this dispatch extends, doesn't replace)

---

## Open questions for the agents

- **Subset selection** — L1 elrond + drax. Which non-GREEN-list Pimen elements ship in VS2b vs deferred? Drift-14 culled-pool (F5) informs; surface in hive log if Drift-14 results change scope
- **Per-element integration order** — L1 drax. Element priority (e.g., season_001005's expected primary element first; etc.). Document in AGENT_STATE.
- **Register-coherence regression handling** — L1 drax + gandalf consult if cross-element coherence regresses (e.g., one element's VFX feels register-discordant)
- **License coverage** — L1 elrond. All integrated Pimen elements must have CC-BY or commercial-royalty-free coverage; surface licensing gaps to knight-rider for asset-acquisition decision
- **Tier-2 vendor follow-on** — if Pimen catalogue is insufficient for full VS2b coverage, surface findings-blocker; knight-rider routes to Tier-2 sweep

---

## References

- VS2a scope-of-work § 2.6 + § 2.7 (C2 + C4 in-flight context)
- `canonical/16-project-roadmap.md` § VS2a + § VS2b
- F3 + F5 + V4 (Drift-14 + V4 convergence — chierit + Pimen coordination)
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl`
- `canonical/story/geometry-vfx-coverage-assessment.md`
- `canonical/story/style-register.md`
- `reincarnated-demo/AGENT_STATE.md` + elrond AGENT_STATE.md
- `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.5
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** VS2a L1 ships → VS2b kickoff. Can begin in parallel with V1 + V4. C2 + C4 in-flight progress contributes; V5 closes the remaining gap.

**Post-activation:** drax + elrond L1 within seams; gandalf consult on register-coherence regressions. No Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. V5 closes the Pimen integration gap; 11/13 becomes full coverage; the player gets the visual catalogue VS2b's ship trigger calls for.*
