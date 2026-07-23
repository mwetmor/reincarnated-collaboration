# KIT-FIDELITY run — session wind-down (RUN FAILED)

**Date:** 2026-07-23 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Verdict:** **FAILED — Matt ruling, logged at KFL-27, run CLOSED**
**Charter + full ledger:** `agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-charter.md` (KFL-1..KFL-27)
**Rule of record:** the owner's eye is the instrument of record. The run's gates said green twice; Matt's eyes said otherwise both times. His verdict governs.

---

## 1. The verdict and why (failure taxonomy — KFL-27, compressed)

1. **Verification-claim inflation, twice.** KFL-22 "verified" on a data-honesty rubric when the question was twin-fidelity; KFL-26 "all five facts green" and the run still failed at the owner's eye. The gates measured narrower rubrics than the owner's question.
2. **Decidability bought by predicate-narrowing = intent leak.** Every exit predicate was formally met; the purpose ("a watchable, source-faithful twin of the king scene") was not. Charter-time failure by the conductor-author: the load-bearing intent only became gates (KF-8) when Matt forced it via field report v2.
3. **Fidelity gates gauged the joined fraction, never audited COVERAGE.** The camera shows a majority-synthetic surface: 40/41 entities unjoined (mob-harvest gap), player HP unjoined, Meteor cost a compiler default, flagship kit never casts its signature skill (dm-tie → no rotation). The byte-chain lock is real — and it certifies a sliver of what the player/owner actually watches.
4. **Owner-eye checkpoints came too late.** The declared Matt interface put his eyes at the END (watch brief). Both catches were his, mid-stream, unprompted by the run.

## 2. What stands (mechanical truth — next session can trust this state)

**All pushed; both trees clean of run debt.** Pre-existing tree noise (godot `project.godot` mesh_lod drift, `harness_logs/`, probe scenes, `*.uid`) untouched, as documented.

| Repo | State |
|---|---|
| `reincarnated-godot` | `3315953` pushed — KF-8 corrections (grid quantization in `render_kt3_arena.gd`; king-register camera home + debug-grid gating in `replica_playback.gd`) + NEW instrument `scripts/kf8_verify_twin.gd` (SceneTree walk, `[kf8]` VERDICT lines for the five facts). Prior: `a3556fc` (drax KF-6b), `9f130cd` (drax KF-6 HUD). |
| `reincarnated-collaboration` | `ac0d1aa7` pushed (KFL-26 + capture `gandalf/captures/2026-07-23-kf8/kf8_after_tick40.png`); `631ae85a` (legolas rotation probe); this wind-down + KFL-27 in the closing commit. |
| corpus.db | READ-ONLY throughout; untouched. |
| MCP instruments | Game instance stopped, editor quit. Wire recipe: addon `addons/godot_mcp/` (4.1.0), `ws://127.0.0.1:6550`, client `/tmp/mcp_call.mjs` (`node mcp_call.mjs '<command>' '<params-json>'`; NOTE `open_scene` takes `scene_path`, `run_project`'s scene param name unresolved). Command surface enumerated in-session from `addons/godot_mcp/commands/*.gd`. |

**Smoke:** GREEN post-corrections (aura suppressed under `--smoke` per KTL-6; the one Binbun DummyShader shutdown line on the visible path is documented, not a leak).

## 3. Evidence that SURVIVES the failed run (do not re-derive next lap)

- **Byte-chain source→compiled→frames→scene (KFL-26d):** corpus Fire Ball (227+258)/2 = 242.5 = compiled EXACT; Meteor 987+269 = 1256 EXACT; fireball manacost 14.5 EXACT; Fire Mastery ×2.63 EXACT — and the frame's `expected_premit = 637.775 = 242.5 × 2.63` to the third decimal; join key `source_id = "d2-fire-sorc"` byte-equal; `skill_idx 0 = "Fire Ball"` per header roster; scene renders the same fields zero-derivation. **The player side of the pilot is genuinely source-joined.**
- **Provenance truth table (KFL-25d):** player skills/damage/element/energy = source-joined; player HP = engine-realized (source life rows EXIST in corpus — join lane, not harvest lane); mobs = 100% synthetic; rotation = absent in corpus (probe-confirmed).
- **dm-tie root cause:** SOURCE-FAITHFUL (D2 Fire Mastery multiplies both fire skills); sim-side first-wins resolver is why Meteor never fires. Fix is behavioral (rotation), not data.
- **New compiler finding (KFL-26e):** Meteor `energy_cost` 10.0 = `_skill_energy_cost` fall-through default (`kit_compiler.py:656–670` branches Fire Wall/Cyclone/Fire Ball only); source manacost **26 exists in corpus** under R-T3. Must land WITH the dm-tie fix or Meteor over-fires when the tie breaks.
- **Rotation probe (legolas, verified):** corpus carries NO machine-readable role/cast_priority; pilot-5 source rotations documented WITH citations; 7-value role enum (α) recommended; hand-author fallback content already delivered in the report.
- **Mono/.NET fork RESOLVED:** standard build suffices — full MCP wire proven (launch, tree, screenshots, run/stop, runtime state, freeze/step). KT-5 conductor-eye verification unblocked without a build switch.
- **Five-fact scene state:** grid on-lattice (dressing quantizes UP; sim dims stay data authority), king camera register carried as home per fight-load, lighting register verbatim, rig heights in band. Whatever the next lap does, it starts from a geometrically honest scene.

## 4. Next-lap docket (decision-shaped; nothing fires without Matt)

| # | Lap | Seam | Shape |
|---|---|---|---|
| 1 | **Mob-harvest** — the dominant made-up gap: 40/41 entities synthetic | legolas (harvest) + gamora (compile) | THE coverage lap; without it any "fidelity" surface stays majority-synthetic |
| 2 | **Rotation** — R1 Path 1 (role/cast_priority harvest) with hand-authored-5 fallback content in hand | gamora wiring + legolas | Fixes "flagship kit never casts Meteor" |
| 3 | **Compiled-kit fidelity patch** — `flat_damage` rename (KF-5 §BLOCKER) + Meteor cost 26 | gamora | Two-line class; pairs with #2 |
| 4 | **Player-HP join** — life_base/per_level/per_vit rows already in corpus | gamora | Join lane, not harvest lane |
| 5 | **KT-5 King-twin verdict** | Matt + conductor eyes via MCP | Unblocked on standard build |
| 6 | **Taste forks** — action reads small at 44 m under true king pose; edge bone-deco reads large | Matt's eye | Options ledgered at KFL-26h |
| 7 | **Desirable-run-pattern amendment observation** (from this failure: coverage-gates, owner-eye checkpoints, owner's-question rubric) | gandalf, future session | QUEUED — observation, not yet drafted |

## 5. Conductor lessons (binding on my next charter, whoever conducts)

1. **Rubric law:** a VERIFIED claim must name the rubric AND show it is the OWNER'S question, not a narrower proxy. "Data-honest" ≠ "twin-faithful." If the owner's question is aesthetic/experiential, the gate is his eyes — schedule them.
2. **Coverage before accuracy for fidelity runs:** first gate = what fraction of the watched surface is source-joined (entities, skills, stats, behavior). Accuracy gates on the joined part come second. This run ran them in the wrong order.
3. **Owner-eye checkpoints are pre-registered gates,** not end-of-run briefings, for any presentation-surface run.
4. **Predicate-narrowing is the failure mode of F2.** When making a target-state decidable, diff the predicate set against the charter's §0 intent sentence and name what fell out — out loud, at launch.
5. **Post-compaction charter-freshness held** (disk re-reads done each compaction this session) — keep it; it was not the failure surface this time.

## 6. For the next session (mechanics)

- Read this wind-down + charter KFL-25..KFL-27 before touching anything KIT-FIDELITY-adjacent. The run is CLOSED; do not "resume" it — laps in §4 charter fresh.
- Open at Matt: docket ratification (§4), taste forks, KT-5. Nothing in this seam is mid-flight; legolas probe closed, all pushes clean.
- Charter-freshness gate: re-read role file + OP §2 + desirable-run-pattern from disk on any post-compaction turn (disk governs).

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23 — logging my own run as failed, which is the ledger doing exactly what it is for.
