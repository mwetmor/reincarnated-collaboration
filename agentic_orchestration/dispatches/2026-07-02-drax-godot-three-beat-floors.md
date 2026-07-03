# Dispatch — 2026-07-02 — drax — three-beat floors + camera ratification (D6)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-07-02 (one-realm §6.3)
**Estimated effort:** 5–8 days (the three-beat descent is the demo's spatial body)
**Acceptance:** the §23.1 three-beat descent (Structure 1 → biome crossing → Structure 2) authored through the three-gate method, consuming the banked ravine/crypt ruleset; **camera ratifies on the FIRST floor** (game-tracker B1/A′1).
**Status:** FIRES against bundle-v1 (`star-lord/v-one-realm-bundle-LOCKED-2` @ `08e6f24`) — D4 CLOSED. **bundle-v1 is the development bridge** (relay §1): author floor *capability* against it; the v2 demo-emission run swaps *content* through the D4-proven loader — no Godot rework. **Camera-ratification beat sequences EARLY** — lead with it, before the full three-beat authoring completes. Gate-1 critique-pair (jack-ryan + gandalf register + galadriel G2) required.

## Context

§6.3: three-beat floors "authored through the three-gate method (G1 engine-truth / G2 register-CV / G3 Matt), consuming the banked ravine/crypt ruleset; **camera ratifies on the first floor**." The player path (§1): Structure 1 (tight architectural rooms, ~7–8 min, ends at lieutenant boss floor) → biome crossing (open WFC field, ~6–7 min, the register-shift beat) → Structure 2 (tight rooms escalating to the realm champion, ~7–9 min). The **camera is ratified on the first floor and sequenced EARLY** because every subsequent beat inherits it — a bad camera discovered at floor three is expensive.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §1 (player path), §6.3, §4 (per-floor element rotation), §2 (locked register non-negotiable)
- `canonical/reap-die-rise-story/gameplay-loop-design.md` §23.1 (the three-beat structure + timings)
- `canonical/reap-die-rise-story/style-register.md` (the register every floor must pass at G2)
- `canonical/current-to-end-state/current-to-end-state-game.md` B1/A′1 (camera ratification)
- D4 loader (floors instantiate bundle content) + the banked ravine/crypt ruleset in `reincarnated-godot/`

## Three-gate method (the authoring gate for each floor)

- **G1 engine-truth** — the floor's content/encounters come from the engine bundle (not hand-invented Godot-side)
- **G2 register-CV** — galadriel's visual-similarity CV gate against the style-register (each authored floor passes). **jack-ryan Gate-1 fold D6-1: G2 is a STANDING gate drax CANNOT self-clear** — floors author to G1+G3 now, but G2 sign-off is a galadriel dependency that may lag the authoring and must NOT be self-stamped. Do not close a floor "passed G1/G3, called it done" while G2 is unrun (Principle 4 — the gate is the truth; Disc #11 — don't self-certify another seam's gate). Note: the biome-crossing exterior open-WFC field is the style-register's least-proven surface (register validated on enclosed graybox + cathedral) — if G2 struggles there, that's a real register datapoint, not a drax failure
- **G3 Matt** — final sign-off

## Cross-seam contract change? (Principle 6 gate)

Presentation-side level authoring; consumes bundle + galadriel CV. No engine schema change.
- `Round-trip: not applicable — level authoring consuming D4 bundle + galadriel G2; no cross-seam contract modified.`

## Scope

- [ ] **FIRST: camera ratification on floor 1** (early beat — G3 Matt on the camera before the rest of the descent is authored)
- [ ] Structure 1 — tight architectural rooms, ends at lieutenant boss floor (the Goldilocks spread holder, §3)
- [ ] Biome crossing — open WFC field, ranged/environmental threats, the register-shift beat
- [ ] Structure 2 — tight rooms escalating to the realm champion
- [ ] Per-floor element rotation from the bundle (§4, engine-supported)
- [ ] Each floor passes G1 (engine-truth) → G2 (galadriel register-CV) → G3 (Matt)
- [ ] Min-spec check per D10
- [ ] AGENT_STATE updated
- [ ] Tag: `drax/v-godot-three-beat-floors-1`

## Acceptance criteria

- [ ] Camera ratified on floor 1 (G3 Matt) — sequenced EARLY, before full descent authoring
- [ ] Three beats authored; each passes the three-gate method (G1/G2/G3)
- [ ] The biome-crossing register-shift reads as a distinct beat (§1)
- [ ] Per-floor element rotation live from the bundle

## Out of scope (explicit non-goals)

- The escape sequence (§23.3) + horde density (D7) — floors here are descent beats; the escape is a later beat
- King-rig → descent stitch (D9)
- Enemy AI behavior (D7 — floors here are spatial/authoring)
- Structure-2 champion becoming/escape mechanics (the +3 becoming is realized in the run-stitch/escape work)

## Quality criterion

**Game-quality goal:** the demo's spatial body is feel-complete and in-register — a Hades-EA-one-biome slice that convinces. The camera (ratified first) makes the whole descent read right.

**Refutation conditions (surface if any apply):**
- A floor passes G1/G2 but doesn't feel like the §1 beat it's supposed to be
- The camera is ratified late (inverting the §6.3 sequence — camera must lead)
- The register-shift at the biome crossing is invisible in play (§1 beat lost)
- Floors hand-author content that should come from the bundle (G1 engine-truth violation)

## Open questions for the agent to resolve (document; escalate camera to Matt at G3)

- Camera model (fixed ARPG top-down vs. dynamic) — ratify with Matt on floor 1
- How much of the banked ravine/crypt ruleset maps directly vs. needs demo-specific authoring

## References

- one-realm-mvp-scope.md §1/§6.3/§4/§2 · gameplay-loop-design §23.1 · style-register
- current-to-end-state-game.md B1/A′1
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
