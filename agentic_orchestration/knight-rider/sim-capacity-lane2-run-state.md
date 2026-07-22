# Lane-2 — SIM CAPACITY (multi-actor / horde) — KR conductor run-state

**Lane:** Lane-2 of the three-lane braid (gandalf brief `2026-07-22-parallel-kr-lanes-emission-sim.md`): Tier-3 (gandalf-conducted) × Lane-1 EMISSION (star-lord) × **Lane-2 SIM CAPACITY (gamora, this run-state)** → converge at THE BUNDLE.
**Conductor:** knight-rider.
**Seam:** gamora (simulation / spatial gauntlet / calibration).
**Authorization:** Matt fire-word on gandalf brief §3 (2026-07-22).
**Pattern:** B, spec-frozen (F4 technical-not-design → KR-conducted build wave).
**Dispatch:** `dispatches/2026-07-22-gamora-sim-capacity-multi-actor-horde.md`.

## Lifecycle (the internal gate is load-bearing)
1. `[✓ DISPATCH AUTHORED + Gate-1 cleared]` — 2026-07-22. jack-ryan Gate-1 (dispatch review) PASS-WITH-AMENDMENTS; 5 amendments folded. Dispatch FIREABLE.
2. `[✓ STEP (a)]` — DONE. gamora spec `simulation/spec/sim-capacity-extension-spec-2026-07-22.md` + math note `simulation/math/sim-capacity-resource-bounds-2026-07-22.md`, engine `4ee8ccb` PUSHED (push-as-you-go). Partition + #1.1 + Principle-6 + A3 W2-pre-hedge all delivered.
3. `[✓ INTERNAL GATE]` — jack-ryan Gate-1 (DESIGN-MODE) on the SPEC: **PASS-WITH-AMENDMENTS** (2026-07-22). All 5 headline axes independently source-verified. AM-1 (Disc #18: M1-C math-note pins neutral-baseline composition explicitly, provenance-verifiable measured-at-≥50-not-scaled) · AM-2 (Disc #62: re-ground `balance_loop.py:1935` anchor ONLY if A5 scaffold enters — N/A, A5 deferred). Cleared to build the A1-enemy + A2/A6 + A3 envelope behind AM-1/AM-2.
4. `[→ STEP (b) FIRING]` — build A1-enemy + A2/A6 + A3 ONLY; math-note-first; smoke + #2.1 resource-scaling; empirical band re-fit at the ≥50 floor (NOT 150 — resource math confirms; Disc #18 baseline pin per AM-1); push-as-you-go, tag per slice. A5 NOT in scope (Matt flag-#2 deferred).
5. `[ ] Gate-2` on the build (KR routes; gamora does not self-invoke).

## Step-(a) headline — SUBSTRATE-TRUTH DRIFT (verified by gamora + jack-ryan)
The horde-density gap is **materially smaller than the canonical tracker framed.** Live arena composition at HEAD already caps ~50 (`open_arena`=40 "saturation repair"; `escape_lane` `engaged_cap=50`, 2026-07-07 four-family rebase), NOT ≤8; the M1 gather primitive already exists as an off-by-default ablation (`player_gather_primitive=False`, `M1_GATHER_RADIUS_M=20.0`). The old 8-mob wall survives as `SCENARIO_OPEN_ARENA_DIAG`. Buildable work narrows to: named cert scenario (`SCENARIO_OVERRUN`) + gather-promotion + empirical band re-fit. **#1.1 verdict:** ≥50 CLEARS host bounds (mem ~50MB flat non-binding; wall-clock binding via O(N²) `_apply_soft_collision`; N=50 ~7× headroom; break at N≈150 ~91min vs ~90min ceiling → fire the 50 floor, do NOT certify constants at 150). **A3:** all four formations expressible at HEAD, no new engine mechanism → Tier-3 W2 Q1 "NOT VERIFIED" retired to VERIFIED-EXPRESSIBLE (W2 pre-hedge SATISFIED). **Principle-6:** all sim-internal (`scenario_id` free-form str both sides), round-trip N/A; emitting a telemetry `formation` label would RE-FIRE Principle-6 → fenced OUT of the envelope (fresh Gate-1 if step (b) elects it).

## ROUTED OUT (KR surfacing to Matt)
- **Canonical doc-fix (non-blocking):** `current-to-end-state-engine.md` §I.1 lines 717/767-768/837 assert "≤8 concurrent / mean_mobs_killed 8.0" with stale `[gandalf-verified]` provenance (pre-dates the 2026-07-07 rebase). Owes a provenance-preserving re-ground to the 40/24/50 regime (DIAG preserves the 8-mob instrument). Recommend routing to jack-ryan (collaboration-side canonical). Does NOT block the build.
- **W2 pre-hedge SATISFIED** — worth relaying to gandalf (Tier-3 conductor): the formation-topology harness-expressiveness risk is retired from the sim side. Read-only courtesy note; no Tier-3 write.

## Design-gated items that ROUTE OUT of this lane (not built here)
- **A1-player second-kit fight slot** → gandalf (III.1 temperature-definition decides if it's even needed). Audit characterizes cost only.
- **A4 matchup-temperature DEFINITION** → gandalf Pattern-A (III.1 design-fit).
- **A5 +3-becoming acceptance band** → Matt flag-#2 persistence ruling (III.2). KR decides build-scaffold-now vs defer.

## Coordination law (T3-V7 — one-way, Tier-3 → lane)
- W2 (Tier-3) harness-expressiveness red-flag routes INTO this lane's spec as requirements, never a new lane.
  - Before step-(a) Gate-1 clears → fold into spec under review.
  - After Gate-1 clears, before step (b) done → re-enters step (a) as amendment; fresh Gate-1 on the delta.
- Lane-2 reads Tier-3 run-state (`gandalf/notes/2026-07-22-tier3-encounter-geometry-run-state.md`) READ-ONLY. No writes into Tier-3 artifacts.
- Namespace: own dispatch namespace only.

## Push posture
**PUSH-AS-YOU-GO authorized** (Matt 2026-07-22 — ADR-006 per-workstream push pattern for this lane). Auto-push after each unit completes (spec at step-(a) close; each build slice). No per-slice push-request needed.

## Open KR actions
- Relay to gamora any W2 red-flag arrival from the Tier-3 run.
- Route gamora's Pattern-A design requests (temperature definition; kit-vs-kit fight-vs-signal) to gandalf when the spec surfaces them.
- Surface the A5 flag-#2 persistence ruling to Matt if the audit shows the checkpoint harness is otherwise buildable.
