# Dispatch — 2026-06-21 — star-lord — typed-threat telemetry (death-cause-with-element)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-06-21 — publish-go on the typed-resistance recal wave.
**Estimated effort:** ~0.5 wave. **Concurrent** with rocket/gamora — author the additive field + MIGRATION; the round-trip smoke needs gamora's live typed death channel, so coordinate the field shape with gamora before her calibration validation needs it.
**Acceptance:** an additive telemetry field makes the now-live TYPED death channel observable (death-cause-with-element / damage-by-type); existing consumers byte-identical; MIGRATION + round-trip smoke pass.

> **Parent MASTER (Gate-1 ENDORSE):** `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`. This pickup is the star-lord section extracted verbatim. Gate-1 finding: `qa/findings/2026-06-21-recal-wave-typed-resistance-MASTER-gate1.md`.

## Context

The recal wave restores a real player-death channel routed through the kernel resolver with TYPED damage (each signature boss does its element; the kit's per-element resist mediates). Today survival = 1.000 instrument-wide — invisible because nothing dies. To tune the typed band AND verify "matching matters," the death channel must be OBSERVABLE: which element killed the kit, and how much damage by type. Without it, gamora's "a matched kit eases" is unmeasurable.

## Required reading before starting
1. `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md` — **§8** (star-lord handoff), **§3** (why typed telemetry is needed to verify reward-for-matching).
2. `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md` — the 0a spike (the typed damage path the telemetry observes).

## NON-NEGOTIABLE GUARDS (carry verbatim)
- **Additive only** — no field renamed/removed; existing consumers byte-identical (keeps the offensive instrument's banked artifacts intact).
- **Content emission HELD until the two-axis joint close** — this telemetry supports the wave's validation; it does not unlock emission.

## Scope
- [ ] Additive telemetry capturing the now-live TYPED death channel: **death-cause WITH element** and/or **damage-by-type** — richer than the typeless version, NEEDED to tune the typed band and verify matching matters. Your call on exact shape at build (converge with gamora on what her band-validation reads).
- [ ] **Additive only** — see guard.
- [ ] MIGRATION.md (star-lord ↔ gamora boundary, ADR-004).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `star-lord/v-typed-threat-telemetry-N`

## Cross-seam contract change? (Principle 6 — YES, round-trip REQUIRED)
ADDS fight_log/telemetry fields. Round-trip smoke: a production-path fight that kills the player with a TYPED skill → assert death-cause-with-element + damage-by-type present and populated through the gamora→star-lord boundary into the season JSON.

## Out of scope (explicit non-goals)
- The `_DEFERRED_PROXY_BINS` lift / 25% proxy emission (Matt-reserved, separate).
- Any non-additive schema change.

## Open questions for you to resolve (and document)
- Exact additive field shape (death-cause-with-element vs damage-by-type vs both) — converge with gamora on what her typed-band validation needs to read.

## References
- Typed-resistance design-half: `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md`
- 0a resolver spike: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md`
- Coordinating MASTER: `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`
- Disciplines: #11 empirical inspection, #12 semantic-shift
