# Autonomous run 2026-06-16 — Wave 4 CLOSE (knight-rider)

**Charter:** `canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md`
**Wave 4 scope (per charter line 156):** generation completeness + the b6 question — companion-generation pass (season ≥ 2) · D5 reference-kit · D4 proxy-port · Option 1 envelope-vs-b6 boss-efficacy investigation.
**Disposition:** CLOSED. The three real-loadout-INDEPENDENT additive items CLEAR (two via critique-pair, one reconciled as already-done). Option 1 / the b6 deletion correctly PARKS — its binding criterion (re-measured on REAL loadouts) is unreachable this run because the keystone live-integration parks on §6. No Tier-2 deletion fired; no gate FAILED; no Matt surface on gate grounds.

## Items

### Companion-generation pass (rocket) — CLOSED, ADDITIVE
- **Math-note (Discipline #1, before code):** `e5d9c6a` — `generation/math/companion-generation-pass-2026-06-16.md`.
- **Code:** `52c773d` — `generation/companion_generation.py`. `CompanionRecord` = Hall ascended-form reference (lookup-not-generation, D7) + Q8 valid-cell pairing (68 cells verbatim, diagonal rejected, RETRIBUTION/CC anti-synergy cut held, PROXY_INVERSION exception) + §6.2-capped modifier vector (role-class projection of §6.3) + §4 named convergence bond + season ≥ 2 marker (season-1 refused by a real `ValueError` guard). Bounded pass (runnable+measurable, NOT a production fill). LLM-free, sub-second. AGENT_STATE `5578b71`. Tag `rocket/v-companion-gen-1`.
- **Gate (two-witness):** jack-ryan Gate-2 **PASS-WITH-INFO** (`a362953`; 68-cell table source-verified verbatim, 23 strategy strings resolve to real constants, §6.2 caps genuinely bind, season-1 refusal real, determinism seed-real, smoke 12/12). gandalf **ENDORSE-WITH-NOTE** (`eeacbec`; Path Pure + Q8 + §6.2/§6.3 + §4 bond all runtime-verified faithful).
- **gandalf watch-flag (non-blocking):** synthetic Hall must NEVER leak into production as the real source — the season-2 absence→arrival beat collapses if a companion reads as a roster-pick rather than *the* specific self the player lived. Module is explicit it won't (`is_synthetic` + JC-1 park); gandalf holds the line at wire-in.

### D4 proxy-port — Axis-2A discrimination (gamora) — CLOSED, ADDITIVE
- **Math-note (Discipline #1):** `d4-proxy-port-axis2a-2026-06-16.md`. Diagnosis (Disc #11): Axis-2A was inert from a missing SIGNAL, not a missing reduction; the coordinate is a COUNT (mean active proxy count), not a DPS term — COUNT≠CONTRIBUTION cut kept the rework to a per-tick population accumulator.
- **Code:** `fea7e55` — `spatial_engine.py` (flag `track_proxy_population=False`, `_build_player_proxies`, `_step_proxy_population`), `spatial_telemetry.py` (additive `SpatialFightResult.mean_active_proxy_count`, seam-internal — no export column, no MIGRATION), `spatial_bc_measurement.py` (`measure_axis2a_proxy` re-wired). AGENT_STATE `4a28f3b`. Tag `gamora/v-d4-proxy-port-axis2a-1`.
- **Result:** Axis-2A discriminates 3 bins (solo / proxy-light / proxy-heavy) where W-D produced 1 uniform; arity=8 conformance (K5 canary → proxy-heavy, no new reference kit); flag OFF → production unshifted.
- **Gate:** jack-ryan Gate-2 **PASS-WITH-INFO** (`a362953`). The three Discipline-#12 claims code-verified: flag-OFF byte-identical (only 3 production files touched; 1D kernel `proxy_combatant.py`/`fight_engine.py` intact); test supersession legitimate (same K5 fixture, assertion changed because mechanism changed, +2 discrimination tests, frozen export fixture still reads `none`); measurable=False→True a sound flag-gated semantic shift. Smoke 6/6; W-D BC + consume 20/20; spatial 27/27. **Decisions-log entry authored** (engine `93b8fe0`) for the WIRED-DEFERRED→BUILD shift, citing flag-gating that keeps production inert; the production flag-flip added to "Decisions to revisit" as a parked KR/Matt gate.

### D5 reference-kit — STALE-CHARTER RECONCILED (already done)
- Charter line 86 marked D5 "READY, not picked up." It was ALREADY built/committed (`7fd8792`) + tagged (`rocket/v-reference-kit-coverage-1`) 2026-06-13/14, re-verified PASS this run. K7 blood-controller discriminates Axis-5 Resource + Axis-2B Control. The charter line is stale vs disk — D5 marked satisfied. (Third charter-staleness reconciliation of the run, after W-E-closed and M1.3.5-built.)

### Option 1 — envelope-vs-b6 boss-efficacy investigation / b6 deletion — PARKED
- Charter intent (lines 143, 156): run the cheap investigation (b6 is the answer key) to reach the b6-deletion evidence-gate rather than parking immediately; if envelope hits b6-parity → b6 deletion (Tier-2 auto-fire); else PARK the accept-vs-investigate fork.
- **Why it parks:** the deletion's binding criterion is "re-measured on **REAL loadouts**." Real loadouts require the keystone live-integration, which parks on the §6 set-bonus magnitude ruling (Matt's single open design call). The charter (line 181) expected the keystone to be fully *wired* this run; it is materialized + node-staged but the live wire parks on §6, so the real-loadout path is severed. Running the investigation on STOPGAP loadouts would violate the keystone's load-bearing discipline ("do not let a deletion fire on stopgap-loadout evidence") and could not satisfy the criterion anyway. So no deletion-grade b6 investigation was run; the b6 deletion + the accept-vs-investigate fork **PARK for Matt**, gated on the same §6 ruling that gates the 1D deletion.

## Push
Wave-close push pre-authorized by charter. Pushing engine + collab at Wave 4 close (final wave).
