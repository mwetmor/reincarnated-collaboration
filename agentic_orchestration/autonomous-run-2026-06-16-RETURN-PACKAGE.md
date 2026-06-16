# Autonomous run 2026-06-16 — RETURN PACKAGE (knight-rider)

**Charter:** `canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md` (Path Pure ruled; three-tier envelope + Option 1 + wave-close push authorized).
**Run disposition:** COMPLETE. All four waves processed park-and-advance. Every additive item that had a path to its acceptance criterion CLEARED through full gates. Every Tier-2 deletion correctly PARKED (no clean criterion reachable on real loadouts this run). **No gate FAILED; no BLOCK issued; nothing forced a Matt surface on gate grounds.** The remaining open items are design calls + parked preconditions, enumerated below.

---

## 1. Run-log (what shipped)

| Wave | Item | Disposition | Key commits / tags |
|---|---|---|---|
| 1 | D6 grouping-vocab loader fix | CLOSED on deliverable | `d583f64` · `rocket/v-grouping-vocab-loader-fix-1` |
| 1 | W-D export-side consume | CLOSED | `2a91d50` · `star-lord/v-wd-export-1` · Gate-2 `09f0dbd` |
| 1 | rocket i-frame dodge (glass-close) | TAG RELEASED | `51867f5` · `rocket/v1.9-iframe-dodge-glass-close` · Gate-2 `41487da` |
| 1 | telegraph combat-model dispatch 3 | CLOSED | `da80750`/`ffafd4e` · `gamora/v1.4-telegraph-combat-model` · Gate-1 `ba95624` Gate-2 `5911d32` |
| 1.5 | M1.3.5 reduced-spatial search substrate | BUILT + Gate-2 PASS | `b7014a2`/`457026e` · `gamora/v1.0-m1-3-5-reduced-substrate` · legolas consult → gandalf §5 ratify `8944f6e` → Gate-2 `0fb5597` → gandalf close `1051d69` |
| 2 | representative-loadout contract (gandalf) | CLOSED | `c7b0de5` |
| 2 | keystone gear materialization (rocket) | CLOSED, ADDITIVE | `54e6304`/`c4f20f6`/`6aee023` · `rocket/v-keystone-gear-materialization-1` |
| 2 | keystone node-wire (gamora) | CLOSED, ADDITIVE | `76a74a0`/`85f5c97`/`4c9592c` · `gamora/v-keystone-node-wire-1` |
| 2 | keystone two-witness gate | PASS-WITH-INFO + ENDORSE | jack-ryan `174f7cb` · gandalf `0fa3c66` |
| 4 | companion-generation pass (rocket) | CLOSED, ADDITIVE | `e5d9c6a`/`52c773d`/`5578b71` · `rocket/v-companion-gen-1` · Gate-2 `a362953` · gandalf `eeacbec` |
| 4 | D4 proxy-port Axis-2A (gamora) | CLOSED, ADDITIVE | `fea7e55`/`4a28f3b` · `gamora/v-d4-proxy-port-axis2a-1` · Gate-2 + decisions-log `93b8fe0` |
| 4 | D5 reference-kit | RECONCILED (already done) | `7fd8792` · `rocket/v-reference-kit-coverage-1` |

Wave-close summaries: `autonomous-run-2026-06-16-wave-1-close.md`, `-wave-2-close.md`, `-wave-4-close.md`. (Wave 3 had no additive work remaining — see §3.)

---

## 2. PARKING LOT (for Matt — nothing here was promoted to a decision)

**Design calls (Matt-only):**
1. **§6 set-bonus magnitude (6a generated-kit-aligned vs 6b fixed-reference)** — the run's single highest-leverage open call. KEYSTONE-GATING: blocks set-piece materialization (rocket §7.1 step 3), the keystone live-integration, and therefore BOTH Tier-2 deletions (1D-delete cond.5 + b6-delete parity, since both require real-loadout re-measurement). gandalf leans 6b-for-keystone / 6a-as-shipped; magnitude is Matt's. Ref: `canonical/story/representative-loadout-measurement-contract-2026-06-16.md` §6.
2. **b6 accept-vs-investigate fork** — Option 1's deletion verdict. Parked because the b6-parity criterion needs real loadouts (gated on #1). When real loadouts exist, run Option 1; if envelope hits b6-parity → b6 deletion auto-fires; else this fork is Matt's.

**Production semantic shifts (Matt-gated; flag-gated OFF on disk so production is inert):**
3. **F1 geometry-blindness adapter fix** — production spatial swarm path reads geometry via a degraded keyword heuristic (field-name mismatch: emitters write `geometry`/`damage_geometry`; engine reads `spatial_geometry_type`/`geometry_type`; `_lever_geometry_mix` never re-derives). A W-F-adoption precondition. The FIX is a production semantic shift → Matt. (Did NOT block the M1.3.5 build or D4 — both fed real geometry in-harness.)
4. **D4 Axis-2A production flag-flip (`track_proxy_population` ON) + archive re-measurement** — flipping the new discriminating measurement live is a production semantic shift. In the engine decisions-log "Decisions to revisit" (`93b8fe0`). Pairs naturally with #6 below on the same downstream wire-in.
5. **gamora keystone node-wire production adoption (flip `apply_max_profile_investment` default ON)** — the live measurement-loadout shift; needs a decisions-log semantic-shift declaration + rides the keystone integration (#1).

**Downstream wire-ins (engineering, gated on the above):**
6. **Real-Hall companion population source** — companion-gen used a bounded SYNTHETIC Hall; the real source needs cross-season-persistence to emit ascended-form packets + gandalf's Hall-as-ally player-journey authoring (gandalf's seam, per commitment §8). gandalf watch-flag: synthetic Hall must never leak to production.
7. **Keystone live-integration** — consume real gear + flip the node flag + swap 4 slots to set pieces + re-measure the archive. Carry-forward order (gandalf): (a) Matt's §6 ruling FIRST; (b) T4-variant coherence (gear-attuned T4 == alteration-firing T4 at live measurement); (c) JC-3 ruling (count all 11 slots even for 2H — gandalf resolved in-lane); (d) empirical re-measure as the gate validating JC-2 + contract §8 predictions.

**Test-health / housekeeping (no decision needed; surfaced):**
8. **D6's 13 pre-existing unmasked test failures** — Family A b6-generator structural/constraint/balance ×5; Family B element-naming/no-canonical-four ×8. Each needs a product-bug-vs-stale-test judgment (spec call). Unmasked by the D6 collection fix; out of D6 scope.
9. **D6 canon-placement question** — the live-authority grouping-layer-vocabulary doc is filed under `historical/` with `STATUS:HISTORICAL-INFORMATIVE`. May be mis-filed; gandalf's canon seam (not relocated by the run).
10. **telegraph dispatches 4 & 5** — fire-ready but OUT of the charter wave plan; parked per do-not-invent-scope.
11. **Non-gating doc WARNs** (jack-ryan `0fb5597`): M1.3.5 stale fixture comment (hp=2500 vs executed 7500) + preserve the band-probe output. Clearable anytime; not gating.

---

## 3. Ground-state oracle update (charter-vs-disk reconciliations)

The charter's blocker lists were partly stale relative to disk. Three reconciliations the run established:
- **W-E throughput: already CLOSED** (Matt RATIFIED 2026-06-14 "Do all three"), not "NOT STARTED" as the charter implied. The genuine 1D-delete precondition was **M1.3.5** (omitted from the charter's W-F trigger) — the run built it (substrate + Gate-2 PASS).
- **M1.3.5 reduced-spatial search substrate: now BUILT** (was the unstated critical-path blocker). Directionally honest on Axis-2 (Geometry/AOE) + Axis-1 (Mobility/kite) at the locked Pareto config (tick=0.2, full packs). HARD precondition for the 1D `search_estimator` deletion.
- **D5 reference-kit: already DONE** (`7fd8792`, 2026-06-14), not "not picked up" (charter line 86).

**Frontier state after this run:** the two completion-blocker lists are worked down to a single convergent gate. Both Tier-2 deletions (1D `search_estimator`; b6 retirement) and the W-F §6.4 close now sit behind ONE design call (§6 set-bonus magnitude) plus its dependent keystone live-integration, plus the F1 fix as a W-F-adoption precondition. Everything additive that could be built without real loadouts has been built and gated. The trunk never halted.

**Most likely first move at re-entry:** rule §6 set-bonus magnitude → unblocks keystone integration → real loadouts exist → run cond.5 (1D) + Option 1 (b6) on real loadouts → fire/park the two deletions on honest evidence. F1 fix is the parallel W-F-adoption precondition.

---

## 4. Push confirmation

Pushed at each wave-close per charter pre-authorization:
- Wave 1: collab `06e8042..4655882`; engine (through `ffafd4e`).
- Wave 2: collab `4655882..68af6b9`; engine `ffafd4e..4c9592c`.
- Wave 4 (final): collab + engine pushed at this close (hashes recorded in the close commit).

**Discipline note:** all commits used `git add <specific files>` (never `-A`) — the cycle-14 working tree was left dirty and untouched throughout (those files are not run work-products).
