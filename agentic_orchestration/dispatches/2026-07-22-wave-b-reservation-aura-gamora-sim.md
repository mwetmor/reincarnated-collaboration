# Dispatch — gamora — Wave-B Reservation/Aura MVP: sim consumers + banner + cert

**Status:** PENDING (starts AFTER rocket LEAD pushes — read the go-token `EMISSION-READY` in `2026-07-22-wave-b-reservation-aura-rocket-emission-LEAD.md`)
**Seam:** gamora (simulation / resolution / calibration)
**Conductor:** knight-rider (Wave-B Reservation/Aura build lane; run-state `agentic_orchestration/knight-rider/wave-b-reservation-aura-run-state.md`)
**Date authored:** 2026-07-22
**Pattern:** B (multi-slice sim work + calibration; dedicated session)
**Gates cleared:** gandalf DRIFT-CRITIC PASS-WITH-FLAGS · jack-ryan Gate-1 DESIGN-MODE PASS-WITH-AMENDMENTS (2026-07-22). Your Fork-8 cost read RULED **8a** (banner ships in Wave-B). Build to the amendments below.

---

## Position in the wave
You are the **consumer**. rocket has emitted `aura_radius_m` + `aura_reattune_ramp_s` and pushed. You read engine HEAD (post-rocket-push), build the sim consumers, cert. **Do NOT run in parallel with the rocket session on the same tree** (Discipline #62 — the Wave-C two-agents-one-tree collision). rocket is done + pushed before you start.

## What this extends — READ FIRST (governance)
Reservation/Aura FIDELITY EXTENSION over the BUILT economy spec. **`canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` is REMOTE TRUTH (Gate-2-passed 2026-07-16, `b850800`) — DO NOT re-open its arithmetic.** Your C3 work is a **carrier-set WIDENING of the built consumer, NOT a new algorithm** (ERRATA 14 already realized the single generalized regen-cap consumer `1a0e5e4`; you widen its input set to include radius-auras/banners). No arithmetic redefined.

## Required reading
1. `agentic_orchestration/gandalf/design-inputs/2026-07-21-wave-b-reservation-aura-spec-draft.md` — §6 (radius, 2b), §8 (swap-ramp, 6b+7a), §9 (banner, 8a), §10 (sim consumers C1–C8), §12 (acceptance criteria), §14 (gamora routing). **Source of record.**
2. `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` — REMOTE-TRUTH boundary. **Read ERRATA 12 (composed floor `eff_cap = max(0.25·M,…)`), ERRATA 13 (per-pool Σ activation-block — the sim site you now build), ERRATA 14 (single generalized consumer), §3.6 (activation-block semantics), the LOCKED Σ<0.90 invariant.**
3. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 (math-before-code) + #1.1 (resource-bounds), #2 (smoke-test), #8 (schema-validation-at-boundaries), #12 (semantic-shifting), #62 (parallel-tree hygiene).
4. Your Wave-A completion records (`dispatches/2026-07-13-gamora-wave-a-summon-simulation.md`) — the C1a ramp device (§8 precedent) + positioned-ally spawn.

## Primitives at HEAD `8d8bd26` (read by symbol/grep — draft §16 line refs are STALE, Disc #62)
- `distance_to(t) <= radius` primitive — `spatial_engine.py:1098` (C1 base).
- `distance_to_point(x, y)` — `spatial_engine.py:1064` (banner point-distance).
- `_PosProbe(x, y, heading)` — `spatial_engine.py:1182` (banner fixed-anchor stand-in, NOT a full entity).
- `_channel_fixed_hits(origin_x, origin_y, targets, skill, geo)` — `spatial_engine.py:1212` (E4 ground-tether: fixed-origin per-tick membership re-test = the banner radius gate).
- Built reservation clamp / composed floor — `spatial_engine.py:283` helper + reservation consumer `:4075-4083` (`_flat_sum`); this is what C3 widens.
- `_build_positioned_allies` — `spatial_engine.py:2486` — **NOT the banner base** (full combat body; would make banner expensive). Use the ground-tether trio above instead.

## Ruled fork set (§15-R — BINDING): 1=(1b) stackable · 2=(2b) radius-hard-edge · 3=(3a) no-cap · 6=(6b) ramp · 7=(7a) instant refund · 8=(8a) banner-in-Wave-B.

---

## SLICE 1 — MVP sim consumers

### AC-1 (inherited, re-assert): composed floor holds for the widened carrier set
`regen_cap_effective ≥ max(0.25·M, M·(1−min(Σ reservation_percent,0.90)) − Σ reservation_flat)` at every tick when radius-auras/banners are added. Sim assertion at the built clamp. C3 = wider input, same arithmetic.

### AC-3 — C1 aura beneficiary radius gate (Fork 2b)
New helper `_aura_beneficiaries_in_radius`, per-tick, reusing `distance_to <= aura_radius_m`. Beneficiary at `distance > aura_radius_m` gets ZERO aura stat-mod that tick; at `distance <= aura_radius_m` gets FULL (hard edge, no falloff — 2b). **Boundary-inclusive: `== radius` is IN** (matches `<=`). Carrier B (self-buff, no radius) applies to caster regardless of position (AC-4).
- **DESIGN C1 TO TAKE AN ORIGIN ARGUMENT FROM THE START** (your own Fork-8 recommendation): the radius gate accepts an origin (caster position OR a fixed plant-point). This makes the Slice-2 banner a *caller change*, not a re-interpretation. Call out this generalization per Discipline #12 ("radius consumer generalized to arbitrary origin: caster OR plant-point").
- Smoke fixture: minion walked across `aura_radius_m`; buff toggles at the boundary tick.

### AC-5 / AC-6 — C4 swap re-attunement ramp (Fork 6b) + reservation timing (Fork 7a)
Ramp-state on `ActiveEffect.params`. On aura toggle-ON: `benefit(t) = full · min(1, elapsed / aura_reattune_ramp_s)` (linear is sufficient — AC-5 only needs "strictly less than full within one ramp-window"; write the shape in the math-note). **Reservation paid at t=0 (toggle-ON tick), NOT after the ramp** (AC-6). On toggle-OFF: ceiling restores INSTANTLY (7a).
- AC-5 smoke: toggle ON@t / OFF@t+1 within one ramp-window ⇒ benefit < full (flicker yields nothing).
- AC-6 smoke: pool ceiling drops at toggle-ON tick, restores at toggle-OFF tick.

### AC-7-SIM — the owed Σ-activation-block sim site (FLAG A — MVP-CRITICAL, Disc #8)
**This is load-bearing.** ERRATA 13 states: once multi-reservation-per-kit (1b stackable) + in-fight toggling (6b ramp) land — which THIS MVP does — an explicit per-pool Σ activation-block check is OWED at emission (Disc #8). The built §3.6 activation-block semantics had no sim site under static reservations; they now go live for the FIRST time.
- **Predicate:** at aura toggle-ON, evaluate `(Σ active reservation_percent on target pool) + this_aura.reservation_percent`; BLOCK activation (aura does NOT turn on, reservation NOT paid, pool ceiling UNMOVED) if the sum would reach/exceed `0.90`. Likewise `Σ reservation_flat + this.flat` vs `0.75·M`. Prior active auras remain live.
- **This is arithmetic-PRESERVING** — a new GUARD SITE honoring the existing LOCKED Σ<0.90 invariant, NOT a redefinition. Do NOT touch `resource_economy.py` or `bc_target_composer`. Cite ERRATA 13 + Disc #8 in the math-note.
- Smoke fixture (AC-7-SIM): stack auras until the next activation would breach Σ<0.90 — the breaching activation is rejected, ceiling does not move, prior auras stay live.

### C3 — widen the built reservation consumer
Add radius-aura/self-buff carriers to the input set summed at the built clamp (`:4075-4083`). No new algorithm; mirror the ERRATA-14 "widen to non-proxy carriers" move. Additive/byte-identity for non-aura kits.

### Discipline requirements (Slice 1)
- **#1 math-before-code:** authored BEFORE code. Cover: C1 boundary-inclusive `<=` semantics; C4 ramp function + reservation@t=0; AC-7-SIM Σ-check (cite ERRATA 13). Zero new RNG (§10 head).
- **#1.1 resource-bounds:** per-tick deterministic at existing fight scale — state the O(active_auras × beneficiaries) per-tick cost is bounded; no full-regen validation owed for the mechanics (smoke certs mechanics).
- **#2 smoke-test:** AC-3, AC-5, AC-6, AC-7-SIM as named smoke deliverables. **Do NOT tag the MVP on smoke alone** — the S6 cert (below) is a separate full-path gate.
- **#12:** the C1 origin-arg generalization + C3 carrier-set widening framed additive; call out in commit + note.
- **MIGRATION:** only if a cross-seam field shape changes on YOUR side (nav/telemetry). The rocket→gamora emission contract is rocket's MIGRATION; you consume it.

---

## SLICE 2 — banner (carrier D, Fork-8 = 8a) — AFTER Slice-1 smoke green
Thin slice on the Slice-1 MVP surface. Reuse the ground-tether trio — NOT `_build_positioned_allies`.
- **Banner record:** plant `(x,y)` snapshot from `player.x/y` at cast; `aura_radius_m`; flat reservation term; `plant_time`; `expiry_time` if durational. A dataclass/dict, NOT a `SpatialEntity`.
- **Radius-from-anchor gate:** call C1's origin-arg radius gate with the plant-point origin (buff set) and mob set (debuff/amp). This is C1 with a relocated origin.
- **Reservation-while-planted:** add banner's flat term into the existing `_flat_sum` (`:4077`); leave-plant/expiry drops the term (ceiling restores). Same consumer, wider input.
- **Expiry tick:** 4-line loop mirroring `_step_proxy_population` expiry (`:2528-2530`).
- **Math-note first (Disc #1):** (a) reservation-while-planted is a FLAT addend (confirm feeds `reservation_flat` path, keeping Σ<0.90 LOCK untouched); (b) banner expiry semantics — pick durational vs toggle-off vs depletion-ends, cite; (c) banner participates in the AC-1 composed-floor assertion (a planted banner is an active carrier).
- **DL-03:** the banner does NOT root the caster (player roams freely; banner stays planted). PASS by construction.
- Smoke: banner planted, beneficiary walked across the plant-point radius; buff toggles at boundary; reservation held while planted, released on expiry.

## SLICE 3 — S6 calibration cert (full-path gate — separate from smoke)
Gauntlet cert of the aura family at the **D2-dominance / evaporate bands** (per built RS calibration §3.10). AC-9 judgment: the aura family plays recognizably (stacking under Σ<0.90 is a live build decision; radius makes positioning matter). Finalize the `aura_reattune_ramp_s` band (rocket shipped scaffold default 1.0s, band [0.5,1.5] — you finalize) and the `aura_radius_m` band [2.0,12.0]. **This full-path cert is the gate before any milestone tag** — do not milestone-tag on smoke alone (Disc #2).

## Out of scope (explicit)
- The §7 capstone consumers (C7) — DEFERRED behind MVP certs AND Q35 (Fork-5 vehicle parked). Not this dispatch.
- Fork-3 target-cap (C2) — ruled (3a) no-cap; do NOT build a cap. (3b is a future S6-escalation only if an offensive-aura outlier surfaces.)
- Any edit to `resource_economy.py` / `bc_target_composer` (REMOTE TRUTH).
- GX-02 shapeshift (out of this wave entirely — waits for the VDM-2-lane SPEC-AUTHOR docket-to-spec pass).

## Commit / push
Auto-commit in-scope. **PUSH authorized "as you go"** (Matt 2026-07-22 — per-cycle push pattern). Tag per slice (`gamora/v<next>-wave-b-reservation-aura-sim-1`, `-banner-2`, `-s6cert-3`). Prove pre-existing failures on HEAD via git-stash. Append a completion record per slice.

---

## Completion record

### Slice 1 (MVP) — DELIVERED + PUSHED (2026-07-22)
**Tag:** `gamora/v1.12-wave-b-reservation-aura-sim-1` (`357bbe3`) · **PUSHED** (Matt as-you-go auth).
**Math note (Disc #1, BEFORE code):** `simulation/math/waveb-reservation-aura-sim-2026-07-22.md`.
**Smoke (Disc #2):** `scripts/gamora_waveb_reservation_aura_slice1_smoke_2026_07_22.py` — **8/8 PASS**.

Consumers landed (all in `simulation/spatial_gauntlet/spatial_engine.py`):
- **C1 `_aura_beneficiaries_in_radius`** (Fork-2b) — boundary-inclusive `<=` hard-edge radius gate, GENERALIZED to an ORIGIN argument from the start (Disc #12 call-out: caster OR plant-point). `aura_effective_benefit()` composes radius-gate × ramp per-tick. Carrier B (radius None) = self-buff, no gate (AC-4).
- **C4 `aura_ramp_fraction`** (Fork-6b) — linear `min(1, elapsed/τ)` ramp; reservation paid at t=0 toggle-ON (AC-6), instant restore at toggle-OFF (Fork-7a).
- **C3 carrier-set WIDENING** (Disc #12; ERRATA-14 2nd application) — `_sum_active_aura_reservation` widens the built regen-cap consumer's Σ; `rs_effective_regen_cap` arithmetic UNCHANGED; byte-identical for non-aura kits.
- **AC-7-SIM `aura_activation_would_breach`** (**FLAG A — the load-bearing MVP-critical site**) — the owed per-pool Σ activation-block (ERRATA 13 + Disc #8). **GUARD OUTCOME: WORKS.** At toggle-ON, a candidate that would push Σ reservation_percent to ≥0.90 (or Σflat > 0.75·M) is BLOCKED: the aura does NOT turn on, reservation is NOT paid, the pool ceiling is UNMOVED, and prior active auras stay live. A fitting candidate (Σ→0.89) succeeds and stacks. Arithmetic-PRESERVING guard honoring the LOCKED Σ<0.90 invariant — NOT a redefinition. Verified by the AC-7-SIM smoke fixture (breach@0.90 rejected + fit@0.89 admitted, both asserted).

**Two empirical finds caught by smoke BEFORE cert (framed as numerical-correctness, NOT design changes):**
1. **Σ<0.90 IEEE-754 float edge** — `0.60 + 0.30 == 0.8999999999999999 < 0.90` silently ADMITTED a stack reaching the LOCKED ceiling. Fixed with `_AURA_SIGMA_EPS = 1e-9` inward bias so a sum rounding to the ceiling blocks (math note §3). This is a genuine guard-correctness bug the smoke surfaced.
2. **Reservation double-count** — the aura's reservation rides the BUILT `resource_economy.reservation_*` fields (rocket MIGRATION [2026-07-22]); it is migrated to the aura carrier + zeroed on the entity at establishment so the pool is taxed ONCE (math note §4). A static-RS kit (no aura geometry/ramp) is NOT treated as an aura — the RS regression smoke confirms static-reservation kits are UNAFFECTED.

Regression: 14/14 sim smokes exit-0 (zero regression). py_compile clean. No touch to `resource_economy.py` / `bc_target_composer` (REMOTE TRUTH).

### Slice 2 (banner, carrier D, Fork-8=8a) — DELIVERED + PUSHED (2026-07-22)
**Tag:** `gamora/v1.12-wave-b-reservation-aura-banner-2` (`eebc52f`) · **PUSHED**.
**Math note:** §5 of the same note (authored up-front in Slice 1).
**Smoke:** `scripts/gamora_waveb_reservation_aura_banner_slice2_smoke_2026_07_22.py` — **4/4 PASS**.

- **`plant_banner()`** — snapshots caster `(x,y)` as a `_PosProbe` plant-point origin (NOT a `SpatialEntity`; reuses the E4 ground-tether device, NOT `_build_positioned_allies`); plants an aura carrier with a FLAT reservation (built `reservation_flat` shape — NO new field) + a durational `expiry_time`. This is C1 with a RELOCATED ORIGIN — a caller change, exactly as the Slice-1 origin generalization intended. 4-line expiry drop in the per-tick loop mirroring `_step_proxy_population`; ceiling restores INSTANTLY at expiry (7a).
- Certs: B1 plant-point radius gate (caster roams away, plant-origin fixed) · B2/B3/B4 reservation held-while-planted + released-at-expiry + composed-floor · B5 DL-03 no-root (PASS by construction — no movement-lock state) · B6 AC-7-SIM flat-ceiling block on plant.

Regression: 14/14 sim smokes exit-0.

### Slice 3 (S6 full-path cert) — NOT started; READY. STOPPING HERE (per dispatch: do NOT rush the full-path cert).
The S6 full-path gauntlet cert at the D2-dominance/evaporate bands is the GATE before any MILESTONE tag (Disc #2 — not smoke alone). It finalizes the `aura_reattune_ramp_s` band [0.5,1.5] (rocket scaffold default 1.0s) + the `aura_radius_m` band [2.0,12.0], and renders the AC-9 archetype-defining judgment. Gauntlet drivers exist (`gauntlet_sim.py`, `unified_calibration_loop.py`, `sc7_calibration_loop.py`). **S6-cert-readiness: READY** — the MVP + banner surfaces are built, smoke-green, and pushed; the cert is a dedicated full-path calibration pass (full-regen wall-clock). Requesting a KR continuation dispatch to run Slice 3.
