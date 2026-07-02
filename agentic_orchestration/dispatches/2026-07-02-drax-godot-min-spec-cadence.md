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

---

## Completion record — drax, 2026-07-02 (STANDING GATE stood up; cadence wired)

**Status: STOOD UP. The min-spec verification cadence exists as a standing build gate. This dispatch does not close — it becomes an acceptance checkbox on D4–D9.**

### Scope completion
- [x] **Min-spec target defined:** GTX-1650/RTX-3050 @ 1080p, **60 FPS proposed** (16.67 ms frame), 50–150 comfortable density band, POE-juiced ~300 = anti-target, Forward+, Jolt+MultiMesh hybrid — all sourced from `performance-target-specs.md` §4/§5/§1/§2. Doc: `reincarnated-godot/MINSPEC_CADENCE.md`.
- [x] **Verification method stood up (profiling proxy — no card on hand):** `scripts/minspec_probe.gd` + `scripts/run_minspec.sh`. Measures the CPU-side sim-loop cost per frame (the min-spec-BINDING quantity, perf §0 — backend-agnostic; catches horde-loop regressions on Metal that surface on Vulkan). Two gates honestly split: **Gate A (Mac proxy, runs NOW)** = regression tripwire + absolute sim-loop budget; **Gate B (real GTX-1650 cert)** = parked, needs hardware. The Mac is the "flattering machine" (perf §7) — the proxy does NOT claim to certify the floor.
- [x] **Cadence established:** every Godot dispatch D4–D9 carries `[ ] D10 min-spec check PASS` (green iff `run_minspec.sh` exits 0 for the dispatch's worst-case scene). Wired into D4 already; KR carries it into D5–D9 authoring.
- [x] **Load-bearing hotspot D7 handled:** the cadence's job is to catch a D7 density regression before launch. `escape_density` baseline recorded (120 fodder + 4 champions = 124, comfortable band).
- [x] **First application (Matt directive) — pre-D7 min-spec spike:** the `escape_density` proxy baseline IS the pre-D7 spike substrate. When D7's real density-per-area spec lands, re-run; a regression vs baseline flags a re-budget BEFORE the full AI+horde build. NOTE surfaced: the proxy proves the SIM loop scales; the render-cost floor still wants Gate-B real hardware at the D7 spike (the 50+ figures + VFX is where the flattered render cost matters).
- [x] **Standing gate documented:** `reincarnated-godot/MINSPEC_CADENCE.md`.
- [x] **Framerate-floor ratification routed (Gate-1 fold):** 60 FPS → `canonical/matt_decision_needed/` **Q5**; on Matt ratify → jack-ryan decisions-log entry (demo-acceptance invariant, not routine implementation).
- [x] **AGENT_STATE updated.**
- [x] **Tag:** `drax/v-godot-min-spec-cadence-1`.

### Acceptance — all met
- [x] Min-spec target defined (GTX-1650-class, explicit framerate/settings floor proposed + routed to Matt).
- [x] Repeatable verification method exists + documented (`run_minspec.sh`, baselines, MINSPEC_CADENCE.md).
- [x] Cadence wired as a standing checkbox on D4–D9.
- [x] **Method demonstrably catches a density regression:** PROVEN — 3× density → FAIL (exit 1); comfortable-band repeat runs → PASS (exit 0). Empirical calibration (#11): tolerance set 1.5× for noise-robustness at sub-0.13ms magnitudes; absolute budget is the backstop.

### Matt-gated items parked
- **`canonical/matt_to_do/` T2:** provide GTX-1650/RTX-3050 Windows box or Steam Deck → unblocks Gate-B absolute certification (must run before Next Fest).
- **`canonical/matt_decision_needed/` Q5:** ratify the 60-FPS floor → jack-ryan decisions-log entry.

### Refutation conditions — none triggered
- Verification only on Mac/Metal → acknowledged + bounded: Gate A is explicitly a proxy for the sim-loop question; Gate B (real HW) parked as T2, required before Fest. No Mac-only=certified claim.
- One-shot vs standing → it is standing (checkbox D4–D9 + committed baselines that diff every run).
- Floor too low/high → 60 FPS from the perf doc's own §4/§9; Matt ratifies against reality; 30-FPS is a data-driven fallback only.

**Signed:** drax, 2026-07-02. The flattering machine tells you the sim loop scales; only the floor tells you the demo runs. Gate A stands now; Gate B waits on Matt's hands (T2).

