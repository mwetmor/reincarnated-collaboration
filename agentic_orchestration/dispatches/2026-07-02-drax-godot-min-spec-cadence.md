# Dispatch — 2026-07-02 — drax — min-spec verification cadence (STANDING GATE) (D10)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-07-02 (one-realm §6.7)
**Estimated effort:** 1–2 days to stand up; then a recurring gate on every Godot dispatch
**Acceptance:** GTX-1650-class min-spec verification exists as a STANDING build gate applied to every Godot dispatch (D4–D9), not a one-shot and not a launch surprise.
**Status:** STANDING — establish EARLY (alongside D4, the first Godot dispatch), then apply to every subsequent Godot beat. Gate-1 required for the initial stand-up.

## Context

§6.7 + §2: "Min-spec verification cadence — GTX-1650-class checks as a **standing build gate**, not a launch surprise." §2 makes it a non-negotiable: "Next Fest judges on GTX-1650-class machines, not Mac/Metal (the perf doc's 'flattering machine' warning goes live at *demo* time). **Burn min-spec verification into the build cadence now.**" This is NOT a dispatch that completes and closes — it **stands up a cadence** and then becomes an **acceptance checkbox on D4–D9**. The Mac/Metal dev environment is the flattering machine; the demo is judged on the floor.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §6.7, §2 (min-spec floor non-negotiable + the flattering-machine warning)
- `canonical/reap-die-rise-story/` / engine perf-stack doc (the "flattering machine" warning source; the min-spec target definition)
- `reincarnated-godot/` AGENT_STATE (current Forward+/Metal render setup — the thing that flatters)

## Cross-seam contract change? (Principle 6 gate)

Presentation-side build/verification infra; no engine schema change.
- `Round-trip: not applicable — build-verification infra; no cross-seam contract modified.`

## Scope

- [ ] Define the min-spec target (GTX-1650-class: framerate floor, resolution, settings baseline)
- [ ] Stand up a min-spec verification method (how to check without necessarily owning the exact card — documented proxy/profiling approach if hardware isn't on hand)
- [ ] Establish the cadence: a min-spec check is a required acceptance item on every Godot dispatch (D4–D9)
- [ ] The load-bearing hotspot: D7 (50+ enemies at min-spec for the escape) — the cadence must catch a density regression before it's a launch surprise
- [ ] **First real application (Matt directive 2026-07-02): the pre-D7 min-spec perf spike** against D7's density-per-area spec — prove the density target holds at the GTX-1650-class floor BEFORE the full AI+horde build. If it fails, D7's density spec re-budgets first.
- [ ] Document the standing gate so each subsequent drax dispatch runs it
- [ ] **Framerate-floor ratification routing (Gate-1 fold):** once Matt ratifies the framerate floor (open question 2), route it to jack-ryan for a decisions-log entry — it's a demo-acceptance invariant, not routine implementation (decision-log-format table)
- [ ] AGENT_STATE updated
- [ ] Tag: `drax/v-godot-min-spec-cadence-1`

## Acceptance criteria

- [ ] Min-spec target defined (GTX-1650-class, explicit framerate/settings floor)
- [ ] A repeatable verification method exists and is documented
- [ ] The cadence is wired as a standing acceptance checkbox on D4–D9 (each Godot dispatch carries a "D10 min-spec check PASS" item)
- [ ] The method demonstrably catches a density regression (test against D7's 50+ escape scene when it lands)

## Out of scope (explicit non-goals)

- Launch-scope perf certification / full hardware matrix (this is the demo min-spec floor)
- Mac/Metal-only profiling (that's the flattering machine — the whole point is to check the floor, not the ceiling)
- Optimizing beyond the min-spec floor (hit the floor; don't gold-plate)

## Quality criterion

**Game-quality goal:** the demo runs on the machines Next Fest judges use — combat feel (§2) and the escape crescendo (D7) survive on GTX-1650-class hardware, so the demo is a net positive at the Fest, not a stuttering net negative.

**Refutation conditions (surface if any apply):**
- Verification only runs on Mac/Metal (the flattering machine — defeats the purpose)
- The gate is a one-shot rather than standing (min-spec discovered late = the launch surprise §6.7 forbids)
- The floor is set too low/high vs. actual GTX-1650-class reality (calibrate the target honestly)

## Open questions for the agent to resolve (document; escalate hardware-access to Matt if needed)

- Whether GTX-1650-class hardware is on hand or the cadence uses a profiling proxy (if hardware is a blocker, flag to Matt's to-do queue — `canonical/matt_to_do/`)
- The exact framerate floor (60fps? 30fps min?) — propose, ratify with Matt

## References

- one-realm-mvp-scope.md §6.7/§2 · engine perf-stack doc (flattering-machine warning)
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
