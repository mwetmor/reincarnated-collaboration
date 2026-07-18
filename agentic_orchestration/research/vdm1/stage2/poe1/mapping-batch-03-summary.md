# VDM-1 Stage-2 PoE1 mapping — batch-03 summary

**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18 · **Batch:** 03 (12 kits) · **Provenance:** authored-vdm1

Deaths-oath / detonate-dead / discharge / divine-ire / ea-ballista / earthquake / earthshatter / edc / elemental-hit / facebreaker / fire-trap / flameblast.

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 8 | deaths-oath, discharge, divine-ire, ea-ballista, earthquake, earthshatter, facebreaker, flameblast |
| APPROX | 3 | edc, elemental-hit, fire-trap |
| GAPPED | 1 | detonate-dead (victim-max-HP-fraction damage has no engine lane) |

Terminal states: 11 × `MAPPED`, 1 × `MAPPED_DOCKET` (detonate-dead). GAPPED↔MAPPED_DOCKET consistency enforced (grade GAPPED iff terminal MAPPED_DOCKET).

## Docket / mint candidate counts

- **Docket candidates: 2** — (1) detonate-dead target-max-HP-fraction damage scaling; (2) elemental-hit per-attack-RNG-element-pool + pruning. Both qualitative-mint-adjacent, evidence-gated, flagged for cross-corpus accrual before any mint.
- **Mint candidates: 0** — no quantitative range/count extension forced. The engine's native `accumulator` charge-stack model (`accumulator_max` / `accumulator_fill_trigger` / `accumulator_discharge_threshold`) absorbed all five charge/channel kits without a range-widen.

## Per-kit one-liners

- **deaths-oath** — CLOSE. Reserved-aura constant chaos-DoT (zero-button) → `aura` + `drain` + PERSISTENCE_ENGINE_uptime + reservation. Wither amp-debuff has no clean ailment lane (noted). Era errata (floor 1.x) acknowledged.
- **detonate-dead** — GAPPED / MAPPED_DOCKET. Corpse-fuel economy is NATIVE (`on-corpse-consume` accumulator); but explosion damage = % of the corpse's max HP has no engine lane (docketed → GAPPED).
- **discharge** — CLOSE. THE charge-dump: consume-all-charges nova maps NATIVELY to `accumulator` + `accumulator_discharge_threshold` (`ring` nova). Tri-element-per-charge-type compressed to top-2 (fire+lightning).
- **divine-ire** — CLOSE. Gather-then-lance: `beam_channel` + native stage-accumulator (fill on-hit-dealt) + tick-cost channel. shock→sunder.
- **ea-ballista** — CLOSE. Totem-delivered fuse-stack: `totem` (dominant loop) + native 20-fuse accumulator + `ground_targeted_circle` detonation. Multi-totem-shared-fuse generalized to a hit-filled accumulator.
- **earthquake** — CLOSE. Plant-and-payoff: `ground_slam` + native `delayed` timing (`delay_seconds`, whose single-non-stacking-delayed-hit matches EQ's one-aftershock-per-slam exactly). Physical-neutral + stun.
- **earthshatter** — CLOSE. Two-step plant-then-detonate: `ground_slam` + apply-consume-pair trigger (spikes = mark:consumption, warcry consumes → burst-damage), depth-1. Phantom "Foulborn Ghostwrithe" alias correctly ignored (no source fact).
- **edc** — APPROX. Two-button DoT-plague: `drain` + on-defender-death trigger (native) + GEOMETRY_PROPAGATION_cascade; unbounded room-clear cascade truncated to single-hop per MAX_CHAIN_DEPTH=1 (not minted).
- **elemental-hit** — APPROX. Per-attack RNG-element + Combat-Focus pool-pruning has no engine lane; mapped to the meta endpoint (forced mono-fire, ELEMENT_CONVERSION_MONO). Docketed.
- **facebreaker** — CLOSE. Item-is-the-build unarmed: `melee_strike` + physical-neutral + ELEMENT_CONVERSION_PHYSICAL; the 600-1000%-more-unarmed multiplier → dominant unarmed-physical gear-affix.
- **fire-trap** — APPROX. Founding trap: `ground_targeted_circle` burning-ground + ZONE_CONTROL; the throw→arm→proximity-detonate trap primitive approximated (no on-proximity-enter proc; on-hit-threshold is nearest).
- **flameblast** — CLOSE (near-lossless). Purest charge-and-detonate: `circle` expanding nova + native accumulator (10-stage, on-passive-tick, sub-threshold-release = native "early release = weaker") + tick-cost rooted channel.

## T4-door frequency

| T4 token | Count | Kits |
|---|---|---|
| GEOMETRY_PROPAGATION_cascade | 5 | detonate-dead, earthshatter, edc, facebreaker(2nd), (on-death/pack-clear reading) |
| ELEMENTAL_ECHO | 3 | detonate-dead, divine-ire, elemental-hit |
| TEMPORAL_CHARGE | 3 | discharge, divine-ire, flameblast |
| GEOMETRY_COLLAPSE | 3 | earthquake, earthshatter(alt), flameblast(alt) |
| PERSISTENCE_ENGINE_uptime | 2 | deaths-oath, fire-trap(alt) |
| PERSISTENCE_ENGINE_saturation | 2 | ea-ballista, edc(alt) |
| MOMENTUM_CASCADE | 1 | discharge(alt) |
| PROXY_ASCENSION | 1 | ea-ballista |
| ELEMENT_CONVERSION_MONO | 1 | elemental-hit |
| ELEMENT_CONVERSION_PHYSICAL | 1 | facebreaker |
| ZONE_CONTROL | 1 | fire-trap |

All members are verified engine tokens (t4_catalog_v2.py) or defined Layer-2 variants (layer2_dimensions.py) per R-M1. Variant tokens used as HINTs only.

## What felt forced (candour for the steward's 25% audit)

- **detonate-dead** is the sharpest gap: the corpse-fuel economy maps beautifully (native `on-corpse-consume`), which makes it TEMPTING to call the whole kit CLOSE — but the DAMAGE identity (payload = % of the victim's HP; the reason it scales into red maps) is genuinely un-laned. Held to APPROX + MAPPED_DOCKET. Audit this one first.
- **fire-trap → APPROX** is a judgment call. The burning-ground and deploy-a-zone feel land cleanly (could argue CLOSE), but the TRAP primitive itself — throw → arm dormant → detonate on **proximity-enter** — has no matching proc (on-hit-threshold is the honest nearest, not exact). The pre-arm-and-bait positional game is the identity; I graded the missing-primitive honestly rather than optimistically.
- **The five charge/channel kits (discharge, divine-ire, ea-ballista, earthshatter, flameblast)** all lean on the native `accumulator` model. I verified the enum members exist (`accumulator_max` / `accumulator_fill_trigger` / `accumulator_discharge_threshold`, resource_economy.py:70-74, and `on-passive-tick`/`on-corpse-consume` fill triggers at :142-143) rather than asserting native behavior blind — per the arc EXACT→CLOSE audit precedent. Flameblast's "earlier release = weaker" is a genuine native match (sub-threshold discharge), which is why it earned near-lossless CLOSE.
- **earthquake's `delayed` timing** — I verified `delay_seconds` (0.5-2.0s, non-stacking single hit) exists in `ability_grammar.py:551-552` before claiming the aftershock lands natively. The engine's non-stacking-single-delayed-hit matching EQ's "one aftershock per slam, no stacking pre-3.25" is a precise fit, not a hand-wave.
- **capstone abstention (100% batch-wide)** forced every t4_door off core identity + probe facts per the fallback clause — stated in each fidelity_note. No capstone source language existed to route against; the routing is OUR authored judgment on the skill's core loop.
- **element/ailment probe overrides:** deaths-oath and edc probe-facts guessed `poison`/`wither`; I overrode to `drain` (both are chaos hex-DoT / essence-drain namesakes = drain lineage, §2), not the stacking-venom `poison`. deaths-oath and edc chaos→shadow (§1). Flagged in fidelity_notes.

## 3 hardest kits

1. **detonate-dead** — the corpse-fuel economy is native but the victim-max-HP-fraction DAMAGE (its whole reason to scale into endgame) has no lane. Split verdict: native economy vs gapped damage-scaling → graded GAPPED (the un-laned mechanism is identity-bearing) + MAPPED_DOCKET + qualitative-mint docket.
2. **elemental-hit** — the identity IS a mechanic the engine cannot express: per-attack RANDOM element from a pool + Combat-Focus pool-pruning. Mapped to the meta endpoint (forced mono-fire) which captures where the build lands but loses the roll-and-sculpt gameplay. APPROX + docket.
3. **ea-ballista** — a shared fuse-accumulator living on ONE target, fed by MULTIPLE autonomous totems, detonating at cap OR the instant the target dies; totem-vs-detonation dominant-loop call (§7.2 → totem leads, player runs free) + fitting the multi-totem-shared-fuse into a single hit-filled accumulator.

---
**Signed:** gandalf (SPEC-AUTHOR). Read-only DB throughout; grades held to engine-truth (all accumulator/timing/proc/ailment/geometry/T4 claims verified against source before assertion). Candidates ladder-audited to the qualitative-mint step; 0 mints, 2 dockets.

## Steward audit addendum (DRIFT-CRITIC, 2026-07-18)
- **ACCEPTED as-is.** detonate-dead GAPPED⟺MAPPED_DOCKET correctly paired (R-M7-conformant before R-M7 was written).
- Charge/consume enum claims verified against engine `resource_economy.py` (accumulator_discharge_threshold L74; on-corpse-consume / on-hit-dealt L142; on-passive-tick L143) — engine-grounding genuine, no false-nativeness.
- Enum sweep CLEAN.
- Post-audit histogram: EXACT 0 / CLOSE 8 / APPROX 3 / GAPPED 1.
