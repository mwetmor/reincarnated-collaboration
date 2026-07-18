# VDM-1 basin-5 mapping batch-p12 summary — Hades (hades1, 7 kits)

**Wave:** p12 · **Cluster:** hades1 · **Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR)

---

## Grade histogram

| Grade | Count | % |
|---|---|---|
| EXACT | 0 | 0% |
| CLOSE | 0 | 0% |
| APPROX | 0 | 0% |
| GAPPED | 7 | 100% |

All 7 kits: `terminal_state: MAPPED_DOCKET`. Per §B5-ROGUELITE and p12 hot-facts: Hades boon/aspect loadout identity has no fixed rotation — the roguelite-park ruling applies universally. This is correct, not a coverage failure.

---

## Per-kit one-liners

| kit_id | Grade | One-liner |
|---|---|---|
| hades1-zeus-chain | GAPPED | Lightning EMITS (attested "Lightning Damage" verbatim); chain geometry confirmed; Jolted status has no 16-ailment equivalent — docketed. |
| hades1-ares-doom | GAPPED | Doom = mechanic name, not element (null); delayed-detonation tag has no engine lane; stack-accumulator docketed. |
| hades1-aspect-chiron | GAPPED | No element; mark-consume homing loop; per-arrow boon-effect stacking is boon-variable (not base-kit attested); docketed. |
| hades1-aspect-guan-yu | GAPPED | Frost Fair Blade = name-only → null; self-cost-contract (permanent max-HP penalty on equip) exceeds hp_cost_scale ceiling; CONTRADICTED mechanics corrected (lifesteal on spin, not Special). |
| hades1-athena-dash | GAPPED | No element; deflect mechanic (projectile reflection) has no 16-ailment or engine lane equivalent; docketed as deflect gap. |
| hades1-beowulf-cast | GAPPED | No base-kit element (cast boon determines element per run); finite-ammo-accumulate-burst shape docketed; CONTRADICTED lodging-in-enemy corrected. |
| hades1-merciful-end | GAPPED | No element; duo-boon pair-capstone (requires Ares + Athena lines) has no engine capstone analogue; builds on both ares-doom and athena-dash component kits. |

---

## T4-door frequency (authored judgment)

| T4 token | Kits |
|---|---|
| RETRIBUTION_ENGINE | zeus-chain, athena-dash, merciful-end |
| TEMPORAL_CHARGE | zeus-chain, ares-doom, beowulf-cast, merciful-end |
| SACRIFICE_ASCENDANCY | aspect-guan-yu |
| DEFENSIVE_TRADEOFF | aspect-guan-yu |
| PHASE_MOMENTUM | athena-dash |
| ZONE_CONTROL | aspect-chiron |
| GEOMETRY_PROPAGATION_overkill | aspect-chiron |
| PERSISTENCE_ENGINE_uptime | ares-doom |
| RESOURCE_CONVERSION | beowulf-cast |

---

## Candidate files

- `docket-candidates-batch-p12.jsonl`: 5 entries
  1. `delayed-detonation-status-tag` (ares-doom, merciful-end) — Doom delay then auto-fire burst; no engine equivalent
  2. `deflect-projectile-reflection` (athena-dash, merciful-end) — projectile reflection mechanic; no 16-ailment or geometry lane
  3. `self-cost-contract-permanent-stat-penalty` (aspect-guan-yu) — equip-level HP penalty exceeds hp_cost_scale lock ceiling
  4. `duo-boon-pair-capstone-identity` (merciful-end, ares-doom, athena-dash) — cross-deity boon pairing as build capstone; no engine analog
  5. `finite-ammo-accumulate-burst` (beowulf-cast) — accumulate Cast bloodstones, release-all on Dragon Rush; pickup-dependent refill
- `mint-candidates-batch-p12.jsonl`: none (no mint candidates this wave — all novel mechanisms either too Hades-specific or require steward adjudication before minting)

---

## §0 near-misses — elements/statuses WANTED but could not attest

| Kit | Wanted | Reason struck |
|---|---|---|
| hades1-aspect-guan-yu | cold/water | "Frost Fair Blade" = aspect/moveset NAME; §0.2 name-only law + §p12 hot-fact explicit |
| hades1-beowulf-cast | lightning (Zeus cast variant) | Zeus cast boon is a run-variable choice, not base-kit attested; element would be per-run |
| hades1-zeus-chain | shock (Jolted) | Jolted = enemy self-damages on attack; PoE shock = sunder per §2, but Jolted is consume-on-hit-back, not a damage-taken buff — no exact 16-ailment map |
| hades1-ares-doom | (no element desired) | Doom is a Hades mechanic name only; correctly null |
| hades1-merciful-end | (cross-boon synergy status) | The "instant Doom on deflect" trigger is a boon-pairing mechanic, not an enemy-directed status in the 16 |

---

## 3 hardest kits — one-line each

1. **hades1-merciful-end** — Duo-boon build IS the capstone itself (not a skill over a capstone), requires cross-kit Ares + Athena lines simultaneously, and the primary mechanic (instant-Doom-on-Deflect) is a two-gap interaction (delayed-detonation + deflect-reflection); hardest to reduce without misrepresenting.
2. **hades1-aspect-guan-yu** — Self-cost-contract economy (permanent max-HP penalty on equip) exceeds engine ceiling, mechanics CONTRADICTED in verify, AND name-only cold trap simultaneously active.
3. **hades1-beowulf-cast** — Finite-ammo-accumulate-burst shape is novel, CONTRADICTED lodging claim required correction, and base-kit element is structurally indeterminate (cast boon is run-variable).

---

## Brief ambiguity / steward flags

- **Jolted crosswalk:** Jolted causes enemies to self-damage when they attack (consuming the status). §2 maps PoE shock → sunder (increased damage taken). Jolted is different: it is a consume-on-attack retaliation, not a damage-taken amp. No §2 row for self-damage-on-enemy-attack. Defaulted to no ailment; flagging for steward to extend §2 if this pattern recurs.
- **Accrual note:** hades1-ares-doom Doom stacking (multiple instances per enemy) has structural similarity to two-tier-accumulator — file accrual to the accumulator family per brief instruction (steward-owned).
- **Deflect_condition ref:** §2 explicitly notes "Deflect is NOT an ailment (def-bin rider deflect_condition)" — the athena-dash and merciful-end kits are the primary basin-5 evidence for that note. Both docketed.
