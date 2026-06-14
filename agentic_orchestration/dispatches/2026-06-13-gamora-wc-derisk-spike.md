# Dispatch — 2026-06-13 — gamora — W-C de-risk SPIKE: spatial engine → first oracle-checked run

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-13 — cert-wave sequence approved; spike-first over dispatch-cold (the spatial engine has never produced a verified run; the spike's per-module triage shapes the real W-C dispatch).
**Status:** GATE-1 PASS-WITH-INFO (jack-ryan, 2026-06-13 — tightest-scoped of the four; one INFO folded: "verified" tied to pre-registration as judge). FIRES when `2026-06-13-gamora-wb-typewall-rename.md` (W-B sim-side) lands and frees gamora.
**Estimated effort:** spike — bounded by outcome, not calendar. Stop at first-successful-verified-run + module triage report. This is NOT full W-C (do NOT drive all 6 scenarios to cert tolerance here).
**Acceptance:** (1) The spatial engine produces its **first successful, ground-truthed run** — at least one oracle cell reproduced and **hand-verified correct** against the golden master. **(Gate-1 INFO) "verified" means: the reproduced cell lands on the PRE-REGISTERED side of the band edge (per the #2 pre-registration below) AND a human-readable trace shows the KPM/outcome derivation — NOT merely "the engine emitted a number near the band."** The pre-registration is the judge. (2) A **per-module keep-vs-rebuild report**: which engine modules reproduce their golden cells (KEEP) vs which fail and need rebuild (REBUILD), with the golden master as the sole judge (no ideological keep-vs-rewrite). (3) A go/restructure recommendation: can the wave proceed validate-then-extend, or does it restructure to module-targeted-greenfield-under-oracle (contract § 8)?

## Context

This is the **de-risk core** of the 2D-certification wave (wave doc § 5, W-C). The spatial engine is ~1900 lines of built scaffolding that has **never produced a single successful, verified run** (oracle § 0.1). Until we can say "for THIS known kit in THIS known room, the engine produces THIS result, hand-verified correct," every kit it characterizes is unprovable — and the entire downstream wave (W-D measurement build, W-E throughput, W-F 1D deletion + bridge re-validation) depends on a working engine.

Authoring the full W-C/W-D/E/F chain cold would presume the modules are salvageable — we have no evidence either way. So this is a **bounded spike**: bring the engine to first verified run, triage modules against the golden master, and report which path the wave takes. KR authors the real W-C-full / W-D / W-E / W-F dispatches **after** your report lands — their shape is spike-determined.

**W-C is the validate-then-extend core** (wave doc § 5): neither greenfield (don't re-render the 6 captured scenarios, arena physics, AOE taxonomy, aggro/leash — re-rendering is the silent-omission mechanism that deleted the battle simulator last cycle) nor naive wrap-and-trust (you cannot freeze-and-build on an oracle never seen correct). **The golden master votes, per module, by evidence.**

## Required reading before starting

- **The golden oracle (the acceptance authority):** `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` — full. Especially § 2 (the KPM bands that anchor the verdicts), § 3 (the six rooms' golden assertions), § 4 (the three baked-in risks A/B/C4), § 5 (the six reference kits + the four CANARY cells), § 6.1 (the RESOLVE cert — the eventual W-C exit), § 7 (methodology-hotspot flag).
- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` § 5 (W-C row + the validate-then-extend framing), § 6 (out-of-scope: kernel frozen, don't re-render scenarios, axis is unvalidated→validated NOT greenfield-vs-brownfield)
- `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` § 2 (kernel-freeze: `damage_resolver.resolve_skill` FROZEN), § 5 (commit-grade = 2D playspace), **§ 8 (refutation clause)** and the **module-targeted-greenfield-under-oracle** fallback the spike's restructure recommendation may invoke
- Verified code anchors (oracle § 8 / wave § 7): scenarios `spatial_gauntlet/arena.py:283-712`; KPM bands `gauntlet_sim.py:206-311`; throughput `gauntlet_sim.py:318-322`; archive insert `gauntlet_archive.py:208`; placeholder cell `balance_loop.py:2827`; spatial engine `spatial_gauntlet/spatial_engine.py`
- `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md` (wave state; arity = 8)

## Reference-kit fixtures — (b) gamora-in-spike, THROWAWAY (Matt directive 2026-06-13)

Hand-build K1–K6 (oracle § 5) as **throwaway in-spike fixtures** — enough to drive the spatial engine and check the golden cells. **Do NOT build durable, oracle-§5-hardened fixtures** — rocket hardens them into the standing MEASURE-cert instrument **only after** the spike passes and the kits graduate. Rationale (Matt): don't build durable fixtures for a wave that might restructure. Construct them by hand (bypassing generation's allocators — that's the point of a known-correct kit per oracle § 6.1); minimal is fine.

## Math-before-code (Discipline #1 + #1.1)

- **Resource-bounds projection (#1.1):** before any full-scenario run, project the spatial sim's peak memory + wall-clock for the spike's run set (N kits × 6 rooms × seeds). The throughput datum (`~5 hrs / 30 kits` full gauntlet; `GAUNTLET_COMPUTE_BUDGET_MAX_FIGHTS = 104,000`) is a warning — the spike must NOT accidentally launch a full-budget run. Bound the spike to the minimal run set that reproduces a verified cell + triages modules.
- **Pre-register expected cells (#2):** before running, write the expected oracle verdict for each (reference-kit, room) cell you intend to check, from oracle § 5. A reproduced cell = the engine lands on the pre-registered side of the band edge.

## Methodology hotspot (Discipline #18 / oracle § 7)

Pack-size calibration (§ 4.A), movement-credit threshold (§ 4.B), and verdict tolerances (§ 6) are design-math calibration choices. Per OP § 4.2: the first golden master is genre-design-authored (the oracle, gandalf seam) and validated empirically by your first runs. **Do NOT route a methodology consult before a baseline exists.** IF, after baseline runs land, the seed-count / tolerance calibration touches a statistical-methodology question (how many seeds to call a KPM "in-band" under spatial collision/aggro stochasticity), THAT is the point to flag KR for a legolas Mode-A consult — not before. The empirical criterion that gates "oracle calibrated" is the reference kits reproducing with stable verdicts across seeds — substrate evidence, not assertion.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring)

**NO** cross-seam contract change in this dispatch — it is a spike (bring-to-run + triage report). The spatial path's commit-grade tuple emission (the cross-seam W-D work) is explicitly OUT of scope here. Round-trip: not applicable — no cross-seam contract change in this dispatch.

## Scope

- [ ] Hand-built throwaway K1–K6 fixtures (minimal; not durable)
- [ ] Resource-bounds projection (#1.1) + pre-registered expected cells (#2) authored before runs
- [ ] Spatial engine brought to **first successful, hand-verified run** against ≥1 golden cell
- [ ] Per-module keep-vs-rebuild report (golden master as sole judge) — which modules reproduce, which fail
- [ ] Go/restructure recommendation: validate-then-extend vs module-targeted-greenfield-under-oracle (contract § 8)
- [ ] Spike findings note in `simulation/math/` or `simulation/notes/`
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `gamora/v-wc-derisk-spike-1`

## Out of scope (explicit non-goals)

- **Full W-C completion** — do NOT drive all 6 scenarios to RESOLVE-cert tolerance. The RESOLVE cert (oracle § 6.1) is the eventual W-C-full exit, authored as a separate dispatch AFTER this spike. Stop at first-verified-run + triage.
- **W-D measurement build** — computing the 8-tuple / behaviorally-realized axis measurement from spatial telemetry is W-D (post-spike, scoped per the W-C.5 close).
- **The type-wall + rename** — that is the W-B sim-side dispatch (must land first).
- **Deleting the 1D engine** — W-F (terminal).
- **Durable / hardened reference-kit fixtures** — rocket, post-spike-pass only.
- **The frozen kernel** — `damage_resolver.resolve_skill` untouched.
- **Re-rendering the 6 scenarios** — they exist (`arena.py`); the oracle certifies them, it does not rebuild them (wave § 6).

## Open questions for the agent to resolve (document in the report)

- Module decomposition: what are the engine's natural modules for the keep-vs-rebuild verdict (movement/positioning, AOE-resolution, aggro/leash AI, KPM accounting, archive insert…)? Define the cut you triage against.
- Minimal run set that yields both a verified cell AND module-discriminating signal — your call, bounded by the #1.1 projection.
- If first-run reveals a blocker that needs another seam (e.g., a generation primitive the spatial path needs that doesn't exist) — surface to KR (Discipline #4: don't fabricate primitives), do not self-author cross-seam work.

## References

- Oracle: `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` (§ 6.1 RESOLVE cert = eventual W-C exit)
- Wave doc § 5 (W-C row), § 6 (out-of-scope)
- Forward-architecture contract § 8 (refutation) + module-targeted-greenfield fallback
- W-C.5 close: `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md`
- Gate-2: jack-ryan gates the spike's verified-run claim + the module triage report at phase exit per seam protocol.

---

**Author:** knight-rider, 2026-06-13. The de-risk spike — bring the never-yet-verified spatial engine to its first ground-truthed run and triage modules against the golden master, so the real W-C/W-D/E/F dispatches are shaped by evidence, not authored cold around an engine that may not hit the oracle.

---

## Completion record — gamora, 2026-06-13

**Status:** COMPLETE. The spatial engine produced its first successful, ground-truthed run. BOUNDED spike — stopped at first-verified-run + module triage + go/restructure rec (did NOT drive to full RESOLVE-cert tolerance).

**Commit:** `275e7a3` (engine). **Tag:** `gamora/v-wc-derisk-spike-1`. **No push** (Matt's wave-close gate).

**Artifacts:**
- Math note (FIRST, Disc #1/#1.1/#2): `reincarnated-engine/src/reincarnated/simulation/math/wc-derisk-spike-oracle-first-run-2026-06-13.md`
- Harness (throwaway K1-K6 fixtures): `reincarnated-engine/scripts/gamora_wc_derisk_spike_2026_06_13.py`
- Raw results: `reincarnated-engine/output/wc-derisk-spike-2026-06-13.json`
- Checkpoint: `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (SESSION 6)

### Did the engine produce a verified run? YES.

**K2 radius-AOE @ open_arena** reproduces its pre-registered genre-correct DIRECTION across all 5 seeds: clears all 8 mobs in ~11 s (KPM 42.9), human-readable trace shown (per-fight kills [8,8,8,8,8] / elapsed [11.0,9.9,11.0,11.0,13.1] s / winners all 'player' / explicit KPM derivation). Canary partner **K1 single-target @ open_arena** clears in ~28 s (KPM 17.3) — single-target NOT over-credited at density (2.5× slower than radius AOE). **The shape-flip MANIFESTS (oracle §3.2), stable per-seed:** K2 radius > K3 line in open_arena (43>19); K3 line > K2 radius in chokepoint (32>26). Geometry × room is genuinely simulated.

### Verified "verified" per Gate-1 INFO

The reproduced cell lands on the PRE-REGISTERED side (math note §2 matrix is the judge) AND a human-readable KPM-derivation trace is emitted — not "a number near the band." First-run blocker found+fixed via Disc #11 mechanism diagnosis (empty `effects:[]` → kernel returned 0 damage; fix = canonical damage-effect shape; fixture-completeness fault, not engine fault).

### Resource-bounds projection (#1.1)

6 kits × 6 rooms × 5 seeds = 180 fights. Projected ~5 s worst case (0.17% of `GAUNTLET_COMPUTE_BUDGET_MAX_FIGHTS=104,000`). Actual 1.3 s. Sequential, single seed-stream (Disc #3). No full-budget run risk.

### DELIVERABLE 1 — per-module KEEP-vs-REBUILD (golden master sole judge)

| Module | Verdict | Evidence |
|---|---|---|
| M1 movement/positioning + nav | **KEEP** | player closes to range; K4≥K2 @ open weakly credits movement-as-setup |
| M2 AOE geometry resolution | **KEEP** | shape-flip manifests + stable per-seed — the strongest positive |
| M3 aggro/leash/target-AI | **KEEP** | single-target underperforms AOE at density 2.5×; no over-clumping |
| M4 damage application (kernel re-point) | **KEEP** | re-pointed resolver produces differentiated DPS per kit |
| M5 KPM/outcome accounting + win-cond | **KEEP-WITH-RECALIBRATE** | logic correct; the BAND it's compared against is the 1D instrument — recalibrate band, not logic (gandalf seam) |
| M6 flanking/survival model | **REBUILD-CANDIDATE** | C4 (K4-kite WR=1.0 vs K6-eHP WR=0.2) distinguished but tank fixture under-DPSes the 240s boss → can't isolate eHP-survival from DPS-failure; needs damage-viable tank fixture + boss-damage tuned so glass risks death |

### DELIVERABLE 2 — go/restructure recommendation: **GO validate-then-extend**

5 of 6 modules KEEP on golden-master evidence; the engine resolves combat correctly and teaches the genre (shape-flip + canary directions hold). The one structural gap is BAND-CALIBRATION (1D 1v1-duel KPM instrument vs spatial N-mob-pack-clear instrument), which is a gandalf-seam recalibration of the COMPARISON TARGET — not an engine rebuild. **Module-targeted-greenfield-under-oracle (contract §8) is NOT invoked.** The refutation clause did not trigger: no module failed its golden cells in a way pointing at rebuild-over-validate.

### LOAD-BEARING FINDING — KPM-instrument mismatch (pre-registered §3, confirmed)

All 36 cells read BELOW the band floor: the spatial engine kills the N-mob pack (max 8) then ENDS (all_mobs_killed) → max KPM ≈ 44; `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:206-311) derives from the 1D 1v1-DUEL kill-rate (t4_sim_cycling.py:202, "0 or 1 kill per fight"; 150-836 floor). Two different instruments — the absolute band is NOT directly applicable to the spatial engine. This is the central triage finding that shapes the real W-C-full dispatch: the eventual RESOLVE cert must compare against a band recalibrated to the spatial instrument (gandalf seam), and verdict reads must be on direction + internal differentiation under the current band.

### Cross-seam blockers (Disc #4 — surfaced to KR, NOT fabricated)

- **gandalf:** recalibrate `ENCOUNTER_COHORT_KPM_BAND` to the spatial-engine N-mob-pack-clear instrument (post-spike #18 item; possible legolas Mode-A consult on seed-count/tolerance under spatial variance — AFTER baseline, which now exists). Band design authority is gandalf's; gamora supplies the empirical spatial KPM regime.
- **rocket (post-spike-pass fixture hardening):** damage-viable K6 tank + boss-damage tuning so C4 (eHP vs kite survival) is isolable; widen open_arena spawn spread (oracle §4.B) so K4≥K2 has real margin. **No new generation PRIMITIVE needed** — the spatial path has no first-class summon primitive, so K5 proxy was approximated as wide-circle AOE; a real proxy fixture is a rocket+gamora follow-on IF the MEASURE-cert proxy-density axis lands (flagged, not built).

**Gate-2 for jack-ryan:** gate (1) the verified-run claim (K2 @ open_arena direction + trace + cross-seed stability) and (2) the per-module KEEP/REBUILD triage + GO recommendation.
