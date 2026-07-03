# Dispatch — 2026-07-03 — gamora — W0 DDA-propagation sweep (DEMO-READINESS UNATTENDED RUN)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-07-03 (G5 propagate-now ruling; run fire authorized)
**Single authority:** `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` **v1.1** — §2 G5, §3 W0, §6, §7. Cite it; do not re-derive.
**Estimated effort:** one focused session
**gates-on:** — *(W0 root; parallel with rocket + star-lord W0)*
**Failure policy:** §7 — degeneracy OR demo-summoner floor-regression → halt-loud with math-note finding; run proceeds (b)-configured (still-certified 1.0 baseline) with the finding attached for Matt.

## Context

Matt ruled G5 propagate-now (gear-as-power lean; the D3-vanilla lesson). **The load-bearing Gate-1 catch (#1):** the D3 cert baseline was derived with proxy `damage_modifier` **hard-coded to 1.0** (`proxy-fight-calibration-2026-07-02.md:72,77`) — proxy DPS received ZERO player-power scaling in the certified fixtures. The propagation flip therefore establishes a **NEW build-floor, not a re-earn of the old one** — the killing-blow arithmetic changes.

## Required reading before starting

- Spec v1.1 §6 (verbatim scope) + §7 failure rows
- `proxy-fight-calibration-2026-07-02.md` (the D3 method + the 1.0 hard-code at :72,:77)
- B1-REBASE Phase-2 completion record (your own A2/A3/A5/A6 method + magnitudes at `67fc0a9`)
- Engine decisions-log `a10a695` (G5 registration)

## Math-before-code

Mandatory math note FIRST (Disc #1, #1.2 code-citations, #24 single-parameter isolation): the propagation-ON killing-blow arithmetic; what the new floor must satisfy; boss anchor dm 5.0 @ 4.5s / swarm 0.20 must hold **by construction**. Pre-fire resource-bounds projection per #1.1 if the sweep is compute-heavy.

## Cross-seam contract change? (Principle 6 gate)

The bundle's `proxy_scaling` contract (spec §6) is star-lord's W1/W3 surface — your sweep DERIVES the config; star-lord EMITS the flag. No emit-shape change from this dispatch itself.
**Round-trip: not applicable — sim-side sweep + cert; the `proxy_scaling` emission contract lands in star-lord's W1/W3 seam.**

## Scope

- [ ] **Single-parameter flip** (Disc #24): propagation ON, everything else held; verify swept-parameter isolation explicitly
- [ ] **(i) Derive the propagation-live build-floor** — fixtures + D3 method carry; boss anchor dm 5.0 @ 4.5s / swarm 0.20 hold by construction
- [ ] **(ii) RE-CERTIFY `demo_bone_acolyte` + `demo_crypt_lieutenant` against the NEW floor** — explicit acceptance gate; a floor-regression on either is a **halt-condition, same standing as degeneracy**
- [ ] Double-dip degeneracy check — if found: halt-loud with finding, ship (b)-config (§6/§7)
- [ ] Math note committed with code citations (#1.2)
- [ ] AGENT_STATE.md updated
- [ ] Tag: `gamora/v-demo-run-w0-dda-sweep-1`

## Quality criterion (OP §3.11)

**Game-quality goal this dispatch serves:** summoner power growth is REAL in the demo — proxies scale with player power (G5, the RoS lesson) so summoner kits don't fall out of band as gear improves; and the certification floor under that scaling is honest, not inherited from a 1.0-hard-coded world.

**Refutation conditions** (surface before executing if any apply):
- The flip cannot be isolated to a single parameter (something else moves with it) — that's a #24 violation to report, not work around
- Evidence that the D3 method does NOT carry under propagation (method break, not just floor shift)
- Acceptance could pass with a floor that no emitted kit could actually meet (vacuous cert)
- Any framing here pre-commits the launch inheritance model (percent vs minion-channels — explicitly launch-scope, §6)

## Acceptance criteria

- [ ] Math note precedes code/sweep, with citations
- [ ] Propagation-live floor derived; anchors hold by construction (shown, not asserted)
- [ ] Both demo melee summoners RE-CERTIFIED against the new floor (or halt-loud + (b)-config + finding)
- [ ] Sweep isolation verified (#24)
- [ ] Round-trip: not applicable (reason above)

## Out of scope

- The exact launch inheritance model (percent inheritance vs minion-specific channels — launch study, §6)
- Emitting the `proxy_scaling` flag (star-lord)
- G4 hypothesis test + tagging (that's your W4 item — separate dispatch)
- Any pairing-layer work (W2)

## References

- Spec §6 + §11 finding #1 · D3 cert `abb010d` · B1-REBASE `67fc0a9` · decisions-log `a10a695`
