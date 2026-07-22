# Wave-B Reservation/Aura MVP — KR build-lane run-state

**Conductor:** knight-rider (spec-frozen build wave; desirable-run-pattern §3 technical-not-design lane)
**Lane opened:** 2026-07-22
**Runs PARALLEL to** the VDM-2 → Edition-next lap (disjoint namespace per brief §6; VDM-2 owns `2026-07-22-vdm2-edition-next-lap-*`).
**Primary source of record:** `agentic_orchestration/gandalf/design-inputs/2026-07-21-wave-b-reservation-aura-spec-draft.md`
**REMOTE-TRUTH boundary (DO NOT reopen):** `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` (built, Gate-2-PASSED 2026-07-16, pushed `b850800`)

---

## Ruled fork set (Matt 2026-07-21, draft §15-R) — BINDING
| Fork | Ruling |
|---|---|
| 1 exclusivity | **(1b) STACKABLE-RESERVED** (PoE; Σ<0.90 is the bound; NO new exclusivity tag) |
| 2 radius | **(2b) RADIUS-GATED HARD-EDGE** (`aura_radius_m`; reuses `distance_to <= radius`) |
| 3 target-cap | **(3a) NO-CAP** (no `aura_target_cap`; S6-cert escalation to 3b only) |
| 4 capstone identity | **(4c) BOTH, efficiency-primary** — CASCADE from Fork 1 (1b→4c); capstone-layer, deferrable behind MVP |
| 5 capstone vehicle | **PARKED → Q35** (soulbound-gear); gates capstone-slice vehicle ONLY, NOT MVP; zero critical-path cost |
| 6 swap-tax | **(6b) RE-ATTUNEMENT RAMP** (`aura_reattune_ramp_s`; reuses Wave-A C1a ramp) |
| 7 refund timing | **(7a) INSTANT at carrier-END**, coupled to 6b |
| 8 banner | **→ gamora Gate-1 cost read** (lean 8a-if-cheap-else-8b) |

**Emission fields fixed:** `aura_radius_m` ships · `aura_reattune_ramp_s` ships · NO `aura_polarity`/`aura_target_cap`/`exclusive_aura_class` · refund instant at carrier-END · AC-7 (stackable predicate) is the live acceptance criterion.

## MVP slice (draft §13/§14)
[MATT-FORK 1] ruled + §6 radius (C1) + §8 swap-ramp (C4, stackable) + carrier-set widen (C3). Makes self-centered auras (A/B) + summoner-slots (C) positionally real. Capstone (§7) + banner (§9) are deferrable layers AFTER MVP certs.

## Scope guard
GX-02 shapeshift Wave-1 build slice (D3-cooldown) is OUT of this wave — waits for SPEC-AUTHOR docket-to-spec pass in the VDM-2 lane. Decline any fold-in.

## Authority envelope (Q33 D2/D3 OPEN as of 2026-07-21)
- Commitment-boundary forks (spec freezes, taste cuts, scope changes, re-opening Matt rulings) → HALT to Matt.
- Design fork mid-build → terminal HALT to Matt (D2 fork-valve UNRULED, so no gandalf-sub-agent routing yet). Re-check Q33 row before any such fork.
- Q35 (Fork 5) / gear-meaning → Matt-present only.
- **Push → Matt-explicit only.** Local auto-commit of in-scope work-products OK.

---

## Progress ledger
| Step | State | Notes |
|---|---|---|
| 1. Wave-A closeout refresh | ✓ DONE 2026-07-22 | Primitives confirmed final: `_build_positioned_allies` :2486, `distance_to<=radius` :1098, built reservation clamp (composed floor), `aoe_radius_mod` NO-OP balance_loop:126. Stable across Wave-C/D. Line-numbers drifted from draft §16 — gamora re-anchors at Gate-1. |
| 2. gandalf DRIFT-CRITIC | ✓ PASS-WITH-FLAGS 2026-07-22 | Boundary intact (C3 = faithful carrier-set widening, blessed by boundary doc lines 303/470; forbidden fields absent; ruling fidelity exact; DL-03 by-construction; no shapeshift/capstone/banner/Q35 creep). Two flags → Gate-1. |
| 3. Gate-1 (jack-ryan DESIGN-MODE) | ✓ PASS-WITH-AMENDMENTS 2026-07-22 | No BLOCK. 5 amendments + 1 INFO (below). FLAG A confirmed MVP-critical. |
| 3b. Fork-8 gamora cost read | ✓ RULED 8a 2026-07-22 | Ship banner in Wave-B as final thin slice after MVP. Reuse E4 ground-tether trio (`_PosProbe`:1182 / `_channel_fixed_hits`:1212 / `distance_to_point`:1064), NOT `_build_positioned_allies`. Design C1 radius consumer to take origin arg from start. |
| 4. Build dispatches authored | 2026-07-22 | rocket LEAD (emission) + gamora consumer (sim/cert). Pattern B. Push authorized "as you go" (Matt 2026-07-22 → per-cycle push pattern). |

## Gate-1 amendment checklist (folded into dispatches)
| # | Dispatch | Amendment |
|---|---|---|
| 1 | gamora | **AC-7-SIM** — owed Σ-activation-block sim site at aura toggle-ON (ERRATA 13 + Disc #8). MVP-critical, arithmetic-preserving. Block activation if `Σ active reservation_percent + this ≥ 0.90` (or flat vs 0.75·M); pool ceiling unmoved, prior auras stay live. |
| 2 | gamora | Math-notes before code: C1 radius gate (boundary-inclusive `<=`) + C4 ramp (`benefit=full·min(1,elapsed/ramp_s)`, reservation paid @t=0). Disc #1. |
| 3 | gamora | Name smoke fixtures AC-3 / AC-5 / AC-6 / AC-7-SIM as deliverables; S6 cert is a SEPARATE full-path gate (do not tag MVP on smoke alone). Disc #2. |
| 4 | rocket | Frame `aura_radius_m` + `aura_reattune_ramp_s` + C3 widen as additive; 1-line MIGRATION.md for new cross-seam consumed fields (ADR-004). Disc #12. |
| 5 | both | Read primitives from HEAD `8d8bd26` by symbol/grep, NOT draft §16 stale line refs. Disc #62. |
| INFO | rocket | `aura_reattune_ramp_s` scaffold default 1.0s, band [0.5,1.5], Disc #40 scaffold-declaration tag; gamora S6 finalizes band. |

## Build progress
- **rocket LEAD ✓ SHIPPED + PUSHED 2026-07-22** — tag `rocket/v2.13-wave-b-reservation-aura-emission-1`, `8d8bd26..e8bccae`. New sibling module `generation/aura_geometry.py` (REMOTE-TRUTH `resource_economy.py` untouched); fields `aura_radius_m` (float|None, band [2.0,12.0]) + `aura_reattune_ramp_s` (float|None, builder-default 1.0, band [0.5,1.5], Disc#40 scaffold) emitted as always-present `aura_geometry` block on `PlayerClassV2.to_dict()` + `KitCandidate.to_character_dict()`. Forbidden fields confirmed absent. MIGRATION [2026-07-22] written. Smoke 35/35 + Wave-B 65/65 + Wave-C all PASS. Banner reuses existing reservation fields (no new field, no escalation). **HEAD now `e8bccae`.**
  - _Benign flags:_ (1) `off_hand_contract.BannerContract.aura_radius_m` (default 8.0) pre-existed on a DIFFERENT serialized path (`off_hand_item` cosmetic) — gamora must consume the economy aura carrier's `aura_geometry` block, NOT the off-hand contract. (2) tag series bumped v2.12→v2.13 (Wave-D consumed v2.12).
- **gamora Slices 1+2 ✓ SHIPPED + PUSHED 2026-07-22** — HEAD `11e06d3`; tags `gamora/v1.12-wave-b-reservation-aura-sim-1` (`357bbe3`) + `-banner-2` (`eebc52f`).
  - **Slice 1 MVP:** C1 radius gate (`_aura_beneficiaries_in_radius`, boundary-inclusive, **origin-arg design** so banner is a caller change) · C4 ramp (`aura_ramp_fraction`, linear, reservation@t=0, instant refund 7a) · C3 carrier-widen (built `rs_effective_regen_cap` UNCHANGED, byte-identical for non-aura kits) · smoke 8/8.
  - **FLAG A / AC-7-SIM guard: WORKS** — Σ-activation-block live for the first time (ERRATA 13 + Disc #8); breaching activation BLOCKED (ceiling unmoved, priors live); Σ→0.89 admitted + stacks. Arithmetic-preserving. Verified by AC-7-SIM smoke.
  - **Two numerical finds (caught by smoke, fixed in-slice, correctness-not-design):** (1) IEEE-754 float edge `0.60+0.30==0.8999…` admitted a ceiling-reaching stack → fixed with `_AURA_SIGMA_EPS=1e-9` inward bias. (2) reservation double-count → migrated to aura carrier + zeroed on entity at establishment → taxed once; static-RS kits unaffected.
  - **Slice 2 banner (8a):** `plant_banner()` reuses E4 ground-tether `_PosProbe` (not `_build_positioned_allies`); flat reservation on built `reservation_flat` shape (no new field); durational expiry; instant ceiling restore (7a); DL-03 no-root PASS. smoke 4/4.
  - **Regression:** 14/14 sim smokes exit-0, zero regression; REMOTE-TRUTH untouched. AGENT_STATE SESSION 67 pushed.
- **gamora Slice 3 (S6 cert) — ⛔ DESIGN-FORK-SURFACED / HALT-TO-MATT 2026-07-22** — tag `gamora/v1.12-wave-b-reservation-aura-s6cert-3` (engine `bcbe001`, HALT record NOT milestone). Engine + collab pushed.
  - **The finding:** the aura family's **benefit-side is UNWIRED.** `aura_effective_benefit()` (`spatial_engine.py:2650`) composes `full·radius_gate·ramp` correctly but has **zero fight-loop call sites** — invoked only by smoke observables. `full_benefit` defaults 1.0, never sourced from the kit; rocket's `AURA_GEOMETRY_KEYS` emits only positional/ramp geometry, no benefit-magnitude field. **Only the reservation TAX side is wired.** So an aura is currently a pure self-imposed reservation-tax with no felt combat benefit.
  - **Contradicts the draft §6 premise** "expressibility ✓ (the aura's stat-mod resolves)" — empirically FALSE: band sweep `aura_radius_m{2,7,12}×aura_reattune_ramp_s{0.5,1,1.5}` → byte-identical fight outcome (<1e-9). The benefit layer the extension assumed-present was never built.
  - **Bands NOT finalizable** (unfalsifiable — they gate an unwired benefit). **AC-9: currently NO** (stacking is pure downside; radius doesn't make positioning matter). Gauntlet NOT run (Disc #1.1 — swept params provably outcome-invariant).
  - **NOT a Slice-1/2 defect** — radius gate / ramp / C3 / AC-7-SIM all built-true + smoke-green; REMOTE TRUTH untouched. The reservation-economy identity works exactly as spec+ERRATA-13 require.
  - **THE FORK (Matt rules — Q33-D2 fork-valve UNRULED ⇒ terminal HALT):** **(A)** aura MVP = reservation-economy-only (benefit-side deferred to a later slice/capstone), or **(B)** benefit-bearing archetype = wire aura-benefit-to-resolution (gamora sink) + a NEW benefit-magnitude emission field (rocket primitive) + a benefit-model/magnitude design ruling (gandalf/Matt) + calibration.
  - **Re-engagement criterion (Disc #3.6):** S6 cert runnable + bands finalizable only after (A)/(B) ruling.
  - Artifacts: `simulation/math/waveb-reservation-aura-sim-2026-07-22.md §8`; AGENT_STATE SESSION 68.

## ⛔ OPEN — Matt ruling required: benefit-side fork (A) vs (B). Build HALTED at S6 cert. MVP+banner surfaces (reservation economy + positional gate + AC-7-SIM guard) are built, smoke-green, pushed. The thing the radius GATES (the aura benefit) is unbuilt.

## Build sequencing
1. **rocket LEAD** — emission fields + MIGRATION land + push first. ✓ DONE.
2. **gamora consumer Slice 1 (MVP)** — C1 radius (origin-arg design) + C4 swap-ramp + C3 carrier-widen + AC-7-SIM guard; math-notes + smoke fixtures; reads HEAD post-rocket-push. **Sequential after rocket (NO parallel same-tree writes — Disc #62).**
3. **gamora Slice 2 (banner 8a)** — final thin slice AFTER MVP smoke green; `_PosProbe`/`_channel_fixed_hits`/`distance_to_point` reuse; math-note (reservation-path + expiry-semantics + AC-1 participation) first.
4. **S6 cert** — full-path gauntlet cert (AC-9 aura-is-felt) at D2-dominance/evaporate bands; separate gate before any milestone tag.
5. **Capstone slice (§7, 4c)** — DEFERRED behind MVP certs AND Q35 (Fork-5 vehicle). NOT authored now.

## DRIFT-CRITIC flags to carry into Gate-1 (build-time OWED-items, neither a BLOCK)
- **FLAG A (load-bearing):** MVP lands the exact two conditions built-spec **ERRATA 13** named as the trigger making the dormant per-pool Σ activation-block semantics go live for the FIRST time — multi-reservation-per-kit (1b) + in-fight toggling (6b swap-ramp). AC-7 specifies the predicate; gamora's build must add the Σ-activation-block sim site ERRATA 13 said didn't yet exist, at emission per Discipline #8. Arithmetic-PRESERVING (a new guard site, not a redefinition). Must not be silently skipped.
- **FLAG B (minor):** draft §16 line-numbers drifted since 2026-07-21. gamora reads from engine HEAD (`8d8bd26`), not the draft's stale refs, when wiring C1 (`_build_positioned_allies` :2486, `distance_to<=radius` :1098, `aoe_radius_mod` NO-OP balance_loop:126).
