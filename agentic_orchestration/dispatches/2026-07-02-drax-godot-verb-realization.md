# Dispatch — 2026-07-02 — drax — verb realization incl. summon (D5)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-07-02 (one-realm §6.2)
**Estimated effort:** 4–7 days (this is the heart of the §20d test)
**Acceptance:** the §4 primitive subset (~6–10 ability primitives) realized as distinct playable Godot verbs, INCLUDING the summon-verb class (spawn / proxy AI / fight / despawn).
**Status:** FIRES against bundle-v1 (`star-lord/v-one-realm-bundle-LOCKED-2` @ `08e6f24`) — D4 CLOSED; the two summoner kits carry non-empty scaffold-flagged proxies. **bundle-v1 is the development bridge** (relay `gandalf/notes/2026-07-02-kr-relay-two-lane-fire-order.md` §1): build verb *capability* against it; the v2 demo-emission run swaps *content* through the D4-proven loader — no Godot rework. Gate-1 critique-pair (jack-ryan DESIGN-MODE + gandalf design-fit) required before execution.

## Context

§6.2 + §4: "~6–10 ability primitives realized as distinct Godot verbs, including the summon-verb class." This is the empirical core of **§20d, THE test**: if ~10 kits cannot become 10 *distinct playable verbs* cheaply, we must know before promising 400. Summon is the **net-new verb class** the summoner mandate (§3) adds: spawn → proxy AI → fight → despawn — the Godot-side realization of the sim's built proxy-combat path. The proxy decls (D2) ride into Godot via D1's bundle; this dispatch makes them *play*.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §4 (the primitive subset + summon-verb class), §6.2, §8 (§20d the test), §2 (combat feel non-negotiable — "convicts in the first ninety seconds")
- `canonical/reap-die-rise-story/gameplay-loop-design.md` §6–§10 (the verbs the loop enacts)
- `canonical/reap-die-rise-story/style-register.md` (verbs must read in-register — feeds D6's G2)
- D4 loader + D2 summoner decls (the proxy payloads you realize as the summon verb)
- `agentic_orchestration/gamora/notes/2026-07-02-sim-two-state-inspection.md` §Q1 (the sim proxy-combat model your summon verb mirrors: spawn ring, allegiance, realized damage, death)

## Cross-seam contract change? (Principle 6 gate)

Presentation-side realization of bundle content; no engine schema change.
- `Round-trip: not applicable — presentation-layer verb realization; consumes D1 bundle records via D4 loader, no cross-seam contract modified.`

## Scope

- [ ] Realize the §4 primitive subset (~6–10) as **distinct** playable verbs (distinctness is the deliverable — not 10 reskins of one verb)
- [ ] The summon-verb class: spawn (owner-ring per the sim model) / proxy AI (navigate + attack allegiance-filtered) / fight (realized damage) / despawn (death/timeout)
- [ ] **SCAFFOLD boundary (carry the D4 fold-3 discipline, #40):** the four proxy magnitudes (`base_hp`/`damage_multiplier`/`attack_interval_s`/`proxy_max_active`) render AS-LOADED and stay flagged non-tuned — they are gamora-D3 calibration TARGETS, not Godot-side tunables. Do NOT re-tune them to make the summon feel right; if it doesn't work at the loaded magnitudes, feed back to gamora
- [ ] **On-screen legibility rider (D3 disposition + `gandalf/findings/2026-07-02-one-realm-summoner-kit-designation.md`):** the two summoners must READ DISTINCTLY — Shadow Warden = horde (many-light-fast skeletons streaming, count-2/1-live) vs Crypt-Lieutenant = bruiser (one-heavy-slow bone-guard slam). Demonstrate the read; it's the only legibility lever for two same-proxy-type summons
- [ ] Combat feel pass (§2 non-negotiable — stagger/responsiveness in the first ninety seconds)
- [ ] Verbs read in-register (coordinate with D6's G2 galadriel gate)
- [ ] Min-spec check per D10 (verbs + summon at density is a perf hotspot — see D7)
- [ ] AGENT_STATE updated
- [ ] Tag: `drax/v-godot-verb-realization-1`

## Acceptance criteria

- [ ] ~6–10 primitives realized as verbs that are *distinguishable in play* (§20d: distinct verbs, cheaply)
- [ ] Summon verb complete: spawn → proxy AI → fight → despawn, playable
- [ ] Combat feel passes the §2 bar (first-ninety-seconds conviction)
- [ ] §20d evidence captured: how cheap was 10-distinct-verbs? (this is the demo's headline validation — report the cost honestly)

## Out of scope (explicit non-goals)

- The full §4 primitive superset beyond the demo subset
- Enemy AI behavior depth (D7 — this dispatch is *player* verbs incl. summon; enemy AI baseline is separate)
- Horde density rendering (D7)
- Experimental kits (§18, launch)

## Quality criterion

**Game-quality goal:** §20d answered empirically — 10 kits become 10 distinct playable verbs, cheaply, so "400 unique heroes" is a credible promise. Combat feel convicts in the first ninety seconds (§2).

**Refutation conditions (surface if any apply):**
- 10 kits collapse into <10 distinguishable verbs (§20d FAILING — this is the single most important thing to surface to Matt, per §8)
- Realizing distinct verbs is expensive per-verb (the 400-promise economics break — surface the cost)
- The summon verb drifts toward enemies-that-remember-you (patent hygiene, §2 / loop-doc §1a — becoming is beat-it-become-it, not nemesis)
- Combat feel is sacrificed for verb count (§2: feel outranks content count everywhere)

## Open questions for the agent to resolve (document)

- Which ~6–10 primitives map from the demo roster's kits (coordinate with the bundle content + gandalf)
- Summon verb's on-screen proxy cap Godot-side vs. the sim's `proxy_max_active` (render budget vs. balance — coordinate with D7 horde density)

## References

- one-realm-mvp-scope.md §4/§6.2/§8/§2 · gameplay-loop-design §6–§10 · style-register
- gamora sim two-state inspection §Q1 (the proxy-combat model to mirror)
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
