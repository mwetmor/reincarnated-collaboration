# VDM-1 Stage-2 PoE1 mapping batch-04 — summary

**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18 · **Kits:** 12 · **Provenance:** authored-vdm1 (OUR judgment against source-verified stage-1 facts)

Batch character: a **cold-heavy melee/ranged cohort** (7 of 12 water/cold) plus three chaos-proxy builds and two physical strikers. The batch is dominated by clean skill-identity maps; friction concentrates in two mechanism-class gaps (cost-redirection, stun-as-damage) and the familiar distance-decay / composite-geometry approximations.

## Grade histogram
| Grade | Count |
|---|---|
| EXACT | 0 |
| CLOSE | 10 |
| APPROX | 2 |
| GAPPED | 0 |

**Terminal state:** MAPPED 10 · MAPPED_DOCKET 2.
**Candidate counts:** docket-candidates **2**, mint-candidates **0** (no quantitative range/count extension was forced this batch; the two docketed gaps are missing-mechanism-class, not param-range).

No EXACT: every kit carried at least a minor behavioral/numeric drift with no enum carrier (distance-decay, every-Nth-hit cadence, composite geometries, random-hop target selection, or cascade-count) — graded CLOSE honestly rather than optimistically per the grade-honesty law and the arc-b01 audit precedent.

## Per-kit one-liners
- **poe1-flicker** (CLOSE): teleport-strike `dash_attack` (engine physical+teleport→dash_attack rule corroborates) + Frenzy-charge cycle economy; TEMPORAL_CHARGE. Random-hop target selection + charge-starvation failure state are behavioral, approximated.
- **poe1-forbidden-rite** (APPROX, DOCKET): totem-delivered chaos nova+homing (`multi_projectile`+`totem`), shadow. The life-cost-OUTSOURCED-to-totems safety identity has no engine lane (cost-payer redirection); mapped hp_cost on chassis + PROXY_ASCENSION/SACRIFICE_ASCENDANCY. Docketed.
- **poe1-freezing-pulse** (CLOSE): piercing cold bolt `line`, water, chill+freeze. Distance-decay ("closer = more damage/freeze") is the lost positional signature — no geometry carries damage-falloff.
- **poe1-frost-blades** (CLOSE): composite `melee_strike`→`multi_projectile` icy-fan-behind-target; water; GEOMETRY_PROPAGATION_cascade for the hit-spawns-fan propagation. One skill = two engine geometries.
- **poe1-generals-cry** (CLOSE): warcry (`self_buff`)→corpse-summoned mirage proxies (`melee_arc`) each firing a linked-cast; PROXY_FISSION + on-cast-linked/linked-cast at DEPTH-1. Era floor **3.11** (errata, verify_ledger authoritative). Skill-cloning + corpse-gate abstracted.
- **poe1-glacial-cascade-mines** (CLOSE): mine-detonated 4-burst marching ice `line` + knockback + freeze; GEOMETRY_PROPAGATION_cascade; mine chassis via trigger-grammar + activation-toggle (DEPTH-1).
- **poe1-glacial-hammer** (CLOSE) [negative=1 kit]: phys→cold `melee_strike`, ELEMENT_CONVERSION_PHYSICAL; freeze/shatter is a DIRECT match to the engine's NATIVE shatter-at-freeze-expiry-under-threshold (ailments.yaml 0.25). Every-3rd-hit cadence is behavioral. Negative flag lives on corpus row, NOT mapping_json (per batch instruction).
- **poe1-golementalist** (CLOSE): 8-golem menagerie, flame golems kill (`totem`, fire+burn) + support-golems buff squad (`totem`); PROXY_ASCENSION + PROXY_CONVERGENCE. Primordial-jewel cooldown-reset/effectiveness loop abstracted to minion traits.
- **poe1-heavy-strike-stun** (APPROX, DOCKET): `melee_strike`, physical→element-neutral, stun+chill. Identity (STUN IS THE DAMAGE + relentless stunlock) has no lane — engine stun is CC with an anti-stunlock floor + boss resist, not a damage source. Nearest door MOMENTUM_CASCADE. Low source confidence (post-cutoff 3.28). Docketed.
- **poe1-hexblast-mines** (CLOSE): curse-consume `circle`, shadow, curse:amplify; on-mark-consume/consume-mark trigger-grammar is the core; NETWORK_AMPLIFIER. Era floor **3.12** (errata). External curse-automation (apply half) noted in economy, DEPTH-1 keeps consume as the modeled step.
- **poe1-hoag** (CLOSE): proxy-feeder — Agony Crawler (`totem`, shadow+poison) does all killing, Cyclone (`whirlwind`) only feeds Virulence (accumulator, crawler dies at 0); PROXY_ASCENSION + PROXY_SOVEREIGNTY.
- **poe1-ice-shot** (CLOSE): cold arrow with `cone`-splash-behind-target (the identity footprint), water, chill+freeze; ELEMENT_CONVERSION_PHYSICAL. Cleanest map of the batch — only the on-target-partial vs cone-total conversion split is folded into the cone note.

## T4-door frequency
| n | door |
|---|---|
| 6 | ELEMENTAL_ECHO |
| 4 | PROXY_ASCENSION |
| 2 | GEOMETRY_PROPAGATION_cascade |
| 2 | ELEMENT_CONVERSION_PHYSICAL |
| 1 | TEMPORAL_CHARGE · PHASE_MOMENTUM · SACRIFICE_ASCENDANCY · ZONE_CONTROL · PROXY_FISSION · PROXY_CONVERGENCE · MOMENTUM_CASCADE · NETWORK_AMPLIFIER · PROXY_SOVEREIGNTY |

All 13 distinct door tokens verified present in `generation/t4_catalog_v2.py` / `layer2_dimensions.py` (R-M1: engine tokens only). ELEMENTAL_ECHO dominance is the expected signature of a mono-cold-heavy batch; the PROXY cluster (4 ASCENSION + FISSION/CONVERGENCE/SOVEREIGNTY) reflects four distinct summoner archetypes (totem-hiero, mirage-warcry, golem-menagerie, crawler-feeder), each routed to a different proxy strategy per its structure.

## Docket candidates (2) — steward ratification required before any elrond ingest
1. **Cost-payer redirection** (forbidden-rite): redirect a skill's self-damage-cost onto a proxy entity's life pool. Engine has hp_cost_scale + totem delivery but no "totem pays the life price" primitive. Ruling needed: mint a cost-payer-redirection primitive, or declare the outsourcing flavor-only.
2. **Control-magnitude-as-damage-source** (heavy-strike-stun): damage computed from stun buildup, plus relentless stunlock the engine deliberately prevents (anti-stunlock immunity floor + boss resist). Engine stun is CC, not a damage source. Ruling needed: mint a control-as-damage capstone class, or accept stun-as-CC-flavor. (Re-check on deeper dossier; current source confidence low.)

Both ran the full ladder (map → approx → quantitative-mint NO → qualitative-mint-candidate → docket). Neither is a range/count extension, so no quantitative mint fired.

## What felt forced / judgment calls worth the steward's eye
- **Flicker `dash_attack` over `teleport`/`blink`:** the crosswalk phrase-book offers both dash and teleport for blink-strikes; I leaned dash_attack because the engine's OWN derivation rule fires physical+teleport→dash_attack, so the choice is engine-corroborated (grade-honest), not arbitrary. The teleport-to-RANDOM-target is the residual behavioral loss.
- **Freezing-pulse & GC-mines both → `line`:** distinct skills, same honest closest type. FP is a single piercing bolt (not a fan → NOT multi_projectile); GC is a forward-MARCHING burst sequence (the marching-along-an-axis IS the identity → line over ground_targeted_circle/ground_slam). Both note the un-enumerated property (FP's distance-decay, GC's discrete-burst-cadence).
- **Frost-blades & ice-shot composites:** both are "one skill, two footprints" (FB: melee→projectile-fan; IS: arrow→cone-splash). FB modeled as two geometries (dominant melee leads §7.2); IS modeled with cone as the single dominant identity footprint (arrow folded into the cone-delivery note) — a defensible asymmetry because FB's melee hit is itself a major damage event whereas IS's on-target arrow hit is subordinate to the cone that clears the pack.
- **Generals-cry linked-cast at DEPTH-1:** the mirages execute the player's linked skill — a genuine trigger→linked-cast, held to one hop (the mirage's hit is terminal, not a further nested trigger) per MAX_CHAIN_DEPTH=1. Did not mint a depth.
- **Glacial-hammer native shatter (negative kit):** despite the negative flag, the freeze/shatter identity is a *direct* match to the engine's native shatter mechanism — a rare case where a negative=1 kit's core mechanic is cleaner than most. Recorded the identity as it existed; flag stays on the corpus row.
