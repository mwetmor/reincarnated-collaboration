# Dispatch — 2026-05-25 — Post-Cycle 10 #3 — Loadout App Readiness Scoping (drax + star-lord)

**Cycle:** Post-Cycle-10 continuation (fires immediately after Cycle 10 wind-down filing)
**Lead owner:** drax (loadout app surface)
**Co-owner:** star-lord (engine→loadout data plumbing; substrate consumption)
**From:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 fresh-session kicker § "Post-cycle continuation" #3 + Matt 2026-05-25 skip-confirmation fire-forward authorization + `agentic_orchestration/gandalf/requests/2026-05-24-knight-rider-t4-reframing-and-loadout-readiness.md`
**Status:** FIRE — scoping work only; gated on Matt scope-lock before any implementation work fires

---

## 0. TL;DR

Scoping output for loadout app readiness per gandalf request 2026-05-24 (T4-reframing + loadout-readiness). drax + star-lord coordinate to produce a scoping memo that informs Matt scope-lock for any subsequent implementation work. NOT implementation work — scoping only.

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1
2. **`agentic_orchestration/gandalf/requests/2026-05-24-knight-rider-t4-reframing-and-loadout-readiness.md`** (loadout app readiness scope context)
3. `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` (loadout analytics suite info-architecture; star-lord first-read)
4. `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (v1_scope is consumed by loadout app at substrate-display time; loadout app must read v1_scope flag)
5. `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary architecture; loadout app must surface both slots)
6. `canonical/story/attribute-system-2026-05-24.md` (STR/INT/WIS/DEX; loadout app surfaces character attributes)
7. `canonical/story/skill-system-2026-05-24.md` (10-15 node skill tree; loadout app surfaces skill tree once authored)
8. Latest reincarnated-loadout repo state (drax owns; check repo README + recent commits)
9. `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4 (D-series delivery commitments including D9 player-facing analytics)
10. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #2 + #2.1 smoke; #11 empirical inspection)

---

## 2. Scope (drax + star-lord coordination)

Produce a scoping memo covering:

### Data plumbing surface (star-lord lead)
- Engine substrate (`weapon_knowledge_entries` + `weapon_sim_props` + `weapons` + `clusters`) → loadout app consumption pattern
- v1_scope flag handling (filter at consumption boundary)
- Off-hand item schema integration (post-Sidecar B schema extension)
- Engine-authored gap-fill rows transparency (per Stage 3.5 provenance flag)
- Stage 4 mechanical-tagging consumption (range/geometry/tempo/amplitude in display layer)
- Cross-DB / cross-host plumbing if Pi-Postgres lands (recognition record at `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` § 7 D4)
- Existing telemetry seam analysis (per loadout-analytics-suite info-architecture)

### Player-facing surface (drax lead)
- Loadout slot surface: main weapon + off-hand item + (other equipment slots TBD)
- Weapon-display surface: name + description + tier + mechanical profile (range/geometry/tempo/amplitude)
- Attribute display (STR/INT/WIS/DEX per attribute system canonical)
- Skill tree surface (gated on algorithm § 8 implementation; not in v1.0 scope)
- Cohesion-judge naming display (player-facing archetypal names per skill-system § 12.3)
- Off-hand item slot display (per off-hand-items canonical)
- Variant C engine-as-general-product implications (loadout app could become multi-profile; not v1.0)

### Cross-cutting (drax + star-lord)
- v1.0 ship surface: what's MUST-HAVE for v1.0 vs deferred to v1.1+
- Engine→loadout deployment cadence (when engine outputs land in loadout; manual export vs CI/CD pipeline)
- Vercel deployment implications (loadout app deploys to Vercel)
- Production observability (per Pi recognition record § 5 monitoring)

---

## 3. Out of scope

- ANY implementation work (scoping output only; Matt scope-locks before any implementation fires)
- Infrastructure execution (Pi-Postgres setup / migration / etc. — gated on D1 ratification per Pi recognition record § 7)
- Engine code changes
- Canonical doc amendments (gandalf authors post-Cycle-10 per canonical authoring queue)
- New architectural decisions
- Algorithm § 8 implementation (separate workstream)

---

## 4. Acceptance criteria

- [ ] Scoping memo authored at `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` (drax lead) + star-lord cross-references
- [ ] Memo covers data plumbing surface (star-lord) + player-facing surface (drax) + cross-cutting
- [ ] v1.0 MUST-HAVE list explicit
- [ ] v1.1+ deferred list explicit
- [ ] Resource-bounds projection per surface area (drax effort + star-lord effort + engine effort)
- [ ] Cross-references to Pi recognition record (G4 Vercel reachability for Pi-Postgres) + Variant C implications
- [ ] Memo returns for Matt scope-lock before any implementation work fires
- [ ] Auto-commit + auto-push per drax + star-lord seam authorization
- [ ] Tag intent: `drax/loadout-readiness-scoping-2026-05-25` after memo lands

---

## 5. Open questions for the agent to resolve

- v1.0 surface boundary (what's IN vs OUT for player-facing v1.0) — drax proposes; gandalf consults if design-experiential ambiguity surfaces (Pattern A-light)
- Engine→loadout cadence model (manual vs CI/CD vs container-pipeline per Pi recognition record § 4) — star-lord + drax propose; informs Pi infrastructure decision indirectly
- Cohesion-judge naming integration timing (when do engine-authored archetypal names land in loadout app surface) — gated on algorithm § 8 implementation; v1.0 may surface raw substrate canonical_name with TBD
- Variant C multi-profile implications for loadout app (v1.1+ scope; recognize implications but defer commitment)

---

## 6. Cross-seam impact

Round-trip: not applicable — scoping work; no production code changes; no schema changes; no cross-seam contract change. Memo informs future implementation work which WILL have round-trip per Principle 6 if implementation fires.

---

## 7. References

- `agentic_orchestration/gandalf/requests/2026-05-24-knight-rider-t4-reframing-and-loadout-readiness.md` (parent context)
- `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` (info-architecture)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (v1_scope; substrate consumption)
- `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary architecture)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system)
- `canonical/story/skill-system-2026-05-24.md` (skill tree; algorithm § 8)
- `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` (G4 Vercel reachability; D4 loadout DB location)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4 (D9 player-facing analytics)
- Pre-existing reincarnated-loadout repo (drax owns)

---

## 8. Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Cycle 10 fresh-session kicker post-cycle continuation #3 + Matt 2026-05-25 skip-confirmation fire-forward authorization
**Status:** FIRE — scoping work only; Matt scope-locks before any implementation fires

**Matt-touch sequence:** scoping memo lands → Matt reads → Matt scope-locks for implementation OR triages → knight-rider routes implementation dispatch if scope-locked
