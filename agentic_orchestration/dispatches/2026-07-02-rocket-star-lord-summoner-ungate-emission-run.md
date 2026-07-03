# Dispatch — 2026-07-02 — rocket (+ star-lord) — summoner un-gate + DEMO EMISSION RUN (B4, Lane B)

**From:** knight-rider
**To:** rocket (lift `_DEFERRED_PROXY_BINS` un-gate) · star-lord (the emission run + minimal runs-table write)
**Approved by:** Matt 2026-07-02 (relay §2 ruling 3 — ZERO hand-authored shipped content; demo roster = curated selection from a REAL gauntlet-passed emission run; D2 decls re-purposed to calibration fixtures, never shipped)
**Estimated effort:** 2–3 days
**Acceptance:** the summoner deferral is lifted; ONE real seasonal emission run produces bundle-v2 with proxy bins + the full T4 set (B1) live; the run is **run #1 in the registry** (minimal runs-table write, ledger D.1 #8 rides this). bundle-v2 is the SHIPPING roster source.
**Status:** **GATED on B1** (the proxy-T4 suite must be live before the run — the run's whole point is to emit "decent proxy kits for selection"). Calibration ALREADY CLOSED (D3 certified-HOLD the four scaffold magnitudes; ledger D.1 #6 ✓). Gate-1 critique-pair (jack-ryan DESIGN-MODE — the run-registry schema is a new cross-seam surface; gandalf design-fit — roster shape) required. **DO NOT FIRE until B1 lands + Gate-1 clears.**

## Context

Matt ruled ZERO hand-authored shipped content (relay §2 ruling 3): the demo's ~8–10 becomable kits are a **curated selection from a real, gauntlet-passed emission run** — the D2 hand-authored summoner decls become calibration fixtures only, never shipped. bundle-v1 was a DEVELOPMENT BRIDGE (pre-ruling scope — hand-attached decl summoners, gear_pool=0). **bundle-v2 is the shipping roster source**: one real seasonal run, proxy bins un-gated, the B1 proxy-T4 suite live, six-type flavor (B3) complete. drax content-swaps v2 through the D4-proven loader (no Godot rework) + re-runs `bundle_roundtrip_smoke.gd` — the §20d proof repeats on shipping content.

**The un-gate:** `_DEFERRED_PROXY_BINS` currently defers proxy-bin kits from emission (the summoner deferral). rocket lifts it + retires the stale reason-string. The run then emits proxy kits with real T4s scored by η (B1's axis_match), so proxy-heavy kits emit with proxy-family primary_t4s (spec §4.5 bands — measured, not forced).

## Required reading before starting

- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` D.1 #7 (demo emission run, depends #9) + D.1 #8 (runs-table minimal write) + PART A (the emission-run shape)
- `agentic_orchestration/gandalf/notes/2026-07-02-kr-relay-two-lane-fire-order.md` §2 ruling 3 + §4 B4 row (un-gate + run #1 registry) + §1 (bundle-v1 bridge / v2 shipping)
- `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` §4.5 (the primary_t4 family-share bands the run should MEASURE)
- The B1 completion records (`rocket/v-proxy-t4-suite-strategies-1` + `gamora/v-proxy-t4-suite-eval-1`) — MUST be landed
- `src/reincarnated/generation/` — `_DEFERRED_PROXY_BINS` + its reason-string
- `src/reincarnated/export/` + telemetry — the emission-run driver + the runs-table target for the minimal registry write

## Cross-seam contract change? (Principle 6 gate — YES, TWO)

1. The proxy un-gate changes what the generation emits (proxy bins now present).
2. The **run-registry schema** is a NEW telemetry/export surface (star-lord proposes → jack-ryan Gate-1 → Matt ratifies, per relay §5).
- `Round-trip: MIGRATION.md entry for bundle-v2 shape (proxy bins live, full T4 set, six-type flavor) + the run-registry minimal schema; drax content-swaps v2 + re-runs bundle_roundtrip_smoke.gd. Cross-seam → MIGRATION before tag (ADR-004). Run-registry schema → jack-ryan Gate-1 → Matt ratify BEFORE the write.`

## Scope

- [ ] **rocket:** lift `_DEFERRED_PROXY_BINS`; retire the stale reason-string with a one-line justification; verify proxy-bin kits now enter emission
- [ ] **star-lord:** run ONE real seasonal emission (proxy bins + full B1 T4 set live + B3 six-type flavor) → bundle-v2
- [ ] **star-lord:** minimal runs-table write — this run is **run #1 in the registry** (D.1 #8); the run-registry schema proposed → Gate-1 → Matt-ratified BEFORE the write
- [ ] **Measure (not force) the §4.5 bands:** proxy-heavy kits emit primary_t4 family-share ≥90%, proxy-light ≥60% — report the measured share (A1)
- [ ] `validate_bundle()` passes on v2; MIGRATION.md v2 entry
- [ ] Empirically verify (Discipline #11): the run is gauntlet-passed; proxy kits carry real proxy-family T4s; NO hand-authored content in the shipped roster
- [ ] AGENT_STATE updated (rocket + star-lord)
- [ ] Tags: `rocket/v-proxy-bin-ungate-1` · `star-lord/v-demo-emission-run-v2-1`

## Acceptance criteria

- [ ] `_DEFERRED_PROXY_BINS` lifted; proxy bins emit
- [ ] bundle-v2 emitted from ONE real gauntlet-passed run; proxy kits carry B1 proxy-family T4s
- [ ] Run #1 in the registry (minimal runs-table write; schema Matt-ratified)
- [ ] §4.5 family-share bands MEASURED + reported
- [ ] validate_bundle passes; MIGRATION v2 entry; drax round-trip on v2 confirmed (cross-lane interlock)

## Out of scope (explicit non-goals)

- v2 roster curation (B5 — this run PRODUCES the pool; B5 CHOOSES from it)
- Full runs-table / run-registry feature build (this is the MINIMAL write — run #1 only)
- Gear pass (B2) / flavor completion (B3) — those feed the run; they're not this dispatch's work
- The ranged-proxy nav question — the run EMITS ranged summoners; **curation** (B5) chooses whether to include them (gandalf lean: exclude — melee certifies clean; nav fix post-demo). Does NOT gate this run.

## Quality criterion

**Game-quality goal:** the demo ships content that came out of the real engine pipeline — the §20d honesty instrument at full strength. "400 unique heroes" is credible because the demo's ~10 came from the same generator that would make the 400, gauntlet-passed, not hand-built.

**Refutation conditions (surface if any apply):**
- B1 has NOT landed (this dispatch is HARD-GATED on it — do not run the emission without the proxy-T4 suite live)
- The run emits proxy kits WITHOUT proxy-family T4s (B1 η integration not actually working — surface; don't ship dead-capstone summoners)
- The run-registry schema is written before Matt ratifies (Principle 4 / relay §5 — schema needs Gate-1 → Matt)
- Any hand-authored content leaks into the shipped roster (ruling 3 violation — the D2 decls are fixtures ONLY)
- The §4.5 bands are FORCED rather than measured (the bands are an emission-outcome check, not a filter to jam)

## Open questions for the agent to resolve (document; escalate to KR)

- Season choice for the v2 run (coordinate — must carry gear if the run is to feed a populated gear pool; align with B2's season-001 gear decision)
- Run-registry minimal schema shape (star-lord proposes → jack-ryan Gate-1 → Matt ratifies per relay §5)
- Whether ranged summoners emit cleanly enough to leave IN the pool for B5 to choose from (they can emit; curation decides — don't pre-filter at emission)

## References

- serial-emission ledger D.1 #7/#8 + PART A · relay §2 ruling 3 + §4 B4 + §5 (run-registry) · proxy-t4-suite-spec §4.5
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md` (Lane B)
