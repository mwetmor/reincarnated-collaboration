# Dispatch — 2026-07-02 — gamora — demo summoner sim-certification (W3-lite) (D3)

> ## ✓ STATUS: RATIFIED — QUEUED AFTER D2
> **Matt ratified the demo-certification slice 2026-07-02** ("D3 — after D2 lands. Calibration wants real decls as fixtures; D2's are better than synthetics and arrive fast"). The prior HELD banner (scope-amendment concern) is DISCHARGED — this is now an approved third engine ask. **Sequence: fires AFTER D2 (`rocket/v-demo-summoner-proxy-decls-1`) lands** — the calibration consumes D2's real hand-authored decls as fixtures (better than synthetics). **Gate discipline: this is a SIM wave → jack-ryan DESIGN-MODE Gate-1 BEFORE build** (per the proxy-wave gate protocol, skill_handoff 2026-06-21). The dodge-ceiling stays Godot-gated per the W3 PARK; this dispatch calibrates the build-FLOOR only.

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-07-02 (the D3 ruling — demo-certification slice ratified as engine ask 3; sequenced after D2)
**Estimated effort:** ~1 day (bounded calibration sweep; the fight mechanism is complete — no new production sim code)
**Acceptance:** the four `proxy_vocabulary_bridge.py` scaffold magnitudes are calibrated against the ratified encounter-model shape + locked boss target, and the 2–3 demo summoner kits (D2 decls) grade at the build-floor vs. the demo roster floors.

## Context

The summoner FIGHT mechanism is BUILT (W1+W2, 2026-06-22). The demo-summoner-certification residual is a **bounded calibration + build-floor grade**, not a mechanism build (gamora two-state inspection §Q1/§Q2). If Matt ratifies this slice, this dispatch runs the D2 decls through the W2 proxy-combat machinery, calibrates ONLY the four scaffold magnitudes, and grades the demo summoners against the roster floors. The graded-band *ceiling* (dodge) stays Godot-gated per the W3 PARK — this dispatch calibrates the BUILD-FLOOR only.

**Sequence AFTER D2** — certification consumes the hand-authored decls D2 emits.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §3, §5.2, §5.3 ("Nothing else" — read why this dispatch is a scope-amendment)
- `agentic_orchestration/gamora/notes/2026-07-02-sim-two-state-inspection.md` §Q1 (the built path), **§Q2 (the certification-slice scoping — your own inspection: the four scaffold fields, the harness shape, the resource-bound projection)**, §Q3 (LIVE grading surfaces)
- `agentic_orchestration/gandalf/notes/2026-06-21-encounter-model-firm-up-disposition.md` (**RATIFIED 2026-06-30** — the encounter-model shape: build-floor resist/tank/out-range + dodge-ceiling; the shape you calibrate against)
- decisions-log 2026-06-21 G-C close (the locked boss target: **dm 5.0 @ 4.5s / swarm 0.20**, G-C close) + the anchor ruling `2026-06-21-typed-resistance-boss-anchor-ruling.md`
- D2 (`2026-07-02-rocket-demo-summoner-proxy-decls.md`) — the decls you consume
- `generation/proxy_vocabulary_bridge.py` (the four scaffold constants `:68,77,232,255`); `proxy_commander.py:59-70` (the DIFFERENT, already-calibrated Set-#6 contribution constants — do not confuse the two sets)

## Math-before-code (Discipline #1 — REQUIRED)

Math-note-first: `simulation/math/proxy-fight-calibration-<date>.md`. Derive the four fight magnitudes (`damage_multiplier` / `base_hp` via `PROXY_REFERENCE_HP` × tier / `proxy_max_active` via `PROXY_TIER_MAX_ACTIVE` — the load-bearing count wall = boss-grading lever / `attack_interval_s`) seeking the graded band: neither D3-evaporate (army melts, no contribution) nor D2-dominance (faceroll). `proxy_max_active` is the primary lever (max army boss-DPS = `proxy_max_active × per_proxy_realized_dps`). Pre-fire resource-bound projection (Discipline #1.1): the W2 load-bearing proof was <5s wall; a magnitude sweep is a bounded multiple, well under the 104k-fight budget — declare peak memory + verify vs host RAM.

## Cross-seam contract change? (Principle 6 gate)

The calibration SETS values in `proxy_vocabulary_bridge.py` — **rocket's file.** Per the proxy_commander pattern, gamora derives the constants; **rocket un-scaffolds** (applies gamora's calibrated values), mirroring the calibrated Set-#6 ownership. No schema field change; internal magnitude values only.
- `Round-trip: not applicable — no cross-seam schema change; magnitude values only. Cross-seam APPLY is a rocket follow-on (un-scaffold gamora's calibrated constants), coordinated at completion.`

## Scope

- [ ] Math-note-first (the four-magnitude calibration derivation)
- [ ] 1 dated calibration harness (`gamora_proxy_fight_calibration_<date>.py`) sweeping `proxy_max_active` × `damage_multiplier` × `base_hp` × `attack_interval_s` on injected D2 fixtures vs `boss_with_adds` + `mini_boss`
- [ ] Single-parameter sweep isolation (Discipline #24 — verify the swept parameter is isolated)
- [ ] Engine-level integration assertion of the summation wiring as the FIRST calibration-harness check (star-lord W3 carry: assert `proxy_realized_damage_dealt` summation before reading any band)
- [ ] Grade the 2–3 demo summoners at the build-floor (survive-and-kill + typed-resistance floor) vs. the demo roster floors
- [ ] Smoke-tier first (Discipline #2)
- [ ] AGENT_STATE.md + math-note updated
- [ ] Tag: **`gamora/v-proxy-fight-calibration-1`** (KR-resolved 2026-07-02: fresh tag, NOT the task-mentioned `v-proxy-W2-realized-damage-1` which is the already-landed W2 tag @ `a84a395` — a collision. This is a distinct calibration wave against the built W2 machinery.)
- [ ] Coordinate the rocket un-scaffold apply at completion

## Acceptance criteria

- [ ] Four scaffold magnitudes calibrated against the ratified encounter-model shape (2026-06-30 stamp) + locked boss target (dm 5.0 @ 4.5s / swarm 0.20, G-C close)
- [ ] Demo summoners grade at the build-floor vs. roster floors (neither D3-evaporate nor D2-dominance)
- [ ] Summation-wiring integration assertion passes before any band read
- [ ] Round-trip: not applicable (magnitude values; rocket apply follow-on)

## Out of scope (explicit non-goals — stays launch / Godot-gated)

- `_DEFERRED_PROXY_BINS` lift (launch-track)
- 25% proxy emission share (launch-track)
- Population WR band / matchup-matrix (III.1 launch)
- **Dodge-ceiling** grading — stays Godot-gated per the W3 PARK; this dispatch calibrates the build-FLOOR only
- Per-level sawtooth (III.2), horde certification-at-density (III.3)
- Any new production sim code (the fight mechanism is complete)

## Quality criterion

**Game-quality goal:** the demo summoners are *certified viable* — a hand-authored necromancer kit survives-and-kills at a graded floor, so the summoner fantasy (§3 mandate) is playtest-credible, not a guess.

**Refutation conditions (surface if any apply):**
- The calibration drifts toward the dodge-ceiling (Godot-gated — out of scope; build-floor only)
- A magnitude change pressures the locked boss anchor (dm 5.0 must hold by construction, not by sweep)
- Grading a proxy kit re-introduces the knife-edge W2 flagged under the no-death-risk boss model — if so, name it, don't paper over it
- The scope-amendment premise (this dispatch exists at all) was never actually Matt-ratified → HALT, escalate to KR

## Open questions for the agent to resolve (document; escalate the tag-collision one to KR)

- Tag name collision (see Scope) — resolve with KR before tagging
- Whether `mini_boss` + `boss_with_adds` are the right two fixtures for the demo roster's actual boss shapes, or whether the demo's specific lieutenant/champion kits need bespoke fixtures

## References

- one-realm-mvp-scope.md §3/§5.2/§5.3 · current-to-end-state-engine.md III.1b · IV.2 (the (b′) calibration-slice framing)
- gamora sim two-state inspection §Q2(c) · encounter-model firm-up disposition (RATIFIED)
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md` §3 (why HELD)
