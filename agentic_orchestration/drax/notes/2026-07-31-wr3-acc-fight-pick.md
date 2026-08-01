# WR3 FULL-MIX ACCEPTANCE — ONE FIGHT, PICKED BY MEASUREMENT, AND ITS CLIP

**Date:** 2026-07-31 · **Author:** drax (presentation seam) · **Status:** CURRENT
**Cell:** R-WR3-2 full-mix acceptance cohort, boss tier / `FULL` arm
**Conductor task:** gandalf — one fight, two characteristics, one clip. Micro-task, no new pipeline.

**Artifacts**
- Pick table (200 rows + the rule + the distribution): `agentic_orchestration/drax/notes/2026-07-31-wr3-acc-fight-pick.json`
- Clip: `~/Games/reincarnated-godot/tmp/wr3acc/clips/WR3ACC_full_74000909.mp4` (1280×720, 1082 frames @ 30 fps = **36.07 s, 1× real time**, 4.8 MB)
- Driver: `~/Games/reincarnated-godot/scripts/wr3_acc_pick_scan.py`
- Traces: `~/Games/reincarnated-godot/tmp/wr3acc/traces/` (200, untracked, regenerable in **11 s**)

---

## THE PICK

**Seed 74000909** — `cornering_fraction` **0.0000** · `min_hp_fraction` **0.6545** · `intake_pool_fraction` **0.5740**.

Rule applied: **PRIMARY** — `argmin(min_hp_fraction)` among fights with `cornering_fraction == 0`.
Neither degenerate branch fired. Winner `player`, 36.10 s, 435.68 HP taken of a 759.0 pool, closest
approach to a wall 0.806 m (centre), 3.3 % of its ticks inside the 2.0 m wall band — **none of them
with a melee body in reach.**

Its five nearest rivals under the same rule, for context:

| seed | min-HP | intake/pool | s | min wall dist m |
|---|---|---|---|---|
| **74000909** | **0.6545** | **0.5740** | 36.1 | 0.806 |
| 74000861 | 0.7119 | 0.3495 | 37.3 | 2.684 |
| 74000958 | 0.7352 | 0.7589 | 36.3 | 3.751 |
| 74000930 | 0.7444 | 0.5392 | 36.8 | 3.991 |
| 74000863 | 0.7533 | 0.3445 | 37.8 | 1.834 |

The gap between the pick and its runner-up is **0.057 pools of HP** — the pick is not a coin-flip
between near-ties, it is the clear floor of the uncornered set.

## THE DISTRIBUTION, IN TWO SENTENCES

**140 of 200 fights corner at all** — but the cornering is thin almost everywhere: the mean
`cornering_fraction` is 0.0393, only 85 fights exceed 0.05, and exactly **one** fight (74000848)
exceeds 0.20, at 0.661. **Min-HP never goes deep**: the floor across all 200 is 0.4764, the median
is 0.7945, 22 fights dip below 0.75, **one** dips below 0.50, and **none** below 0.25 — on this arm
the player is pressured but never close to dying, which is exactly the shape the artifact's own
`SATURATION_DECLARED` sentence predicts (H1 sits at the ceiling; intake is the discriminating
statistic, not win-rate).

⚑ **The two characteristics are anti-correlated at the extreme, and that is the finding.** The
deepest min-HP in the whole cohort (74000848, 0.4764) is also the **most-cornered** fight in the
cohort (0.661) and the **worst intake** in the cohort (1.1122 pools — the artifact's own
`worst_intake_pool_fraction`, reproduced here exactly). The one fight that gets genuinely dangerous
is the one where the player spends two thirds of it pinned to a wall. Matt's rule excludes it by
construction, and the excluded fight is the interesting one for a *different* question.

## THE ARM, AND HOW IT WAS OBTAINED

Same custody shape as the anchor at owner-eye #4, one cell on. `wr3_cell_acc_2026_07_31.py::_run`
attaches a `_VocabSink` which in its own words *"serialises nothing and writes no file"* — so **the
acceptance cohort has no trace on disk anywhere**, and this seam does not edit the engine to get
one. `scripts/wr3_acc_pick_scan.py` transcribes the cell's `_run("boss", ARMS["FULL"])` call
character for character and swaps the sink for a `G5TraceSink`. Nothing in `reincarnated-engine/`
was opened for write.

**REPRODUCTION IS EXACT, at the cohort's own n = 200:**

| | measured here | banked (`wr3_acc.json` → `tiers.boss.FULL`) |
|---|---|---|
| H1 | 1.0000 | 1.0 |
| `dmg_taken_mean` | 313.60457108215974 | 313.60457108215974 |
| `duration_mean_s` | 36.14750000000024 | 36.14750000000024 |
| `intake_pool_fraction` | 0.4131812530726742 | 0.4131812530726742 |
| `worst_intake_pool_fraction` | 1.112183215707797 | 1.112183215707797 |

Digit for digit. **Sink neutrality re-proven independently** (`--verify`): the same 200 seeds re-run
with no sink returned identical per-seed `(win, duration, intake)` vectors. The cohort's own banked
proof is at `vocabulary_probe.sink_neutrality_detail` (boss n=10, `identical: true`).

**NOT PASSED, deliberately:** `emit_telegraphs` / `nova_telegraph_v2` (mechanism-bearing; the cohort
was measured without them — conductor ruling: the clip must be the accepted fight, not a cousin) and
`trace_decisions` (the cell does not pass it either). Consequence, measured not assumed: these
traces carry **zero** `decision` records and the player's aim-line has no data at all.

## THE THREE SCALARS — HOW EACH IS DERIVED

1. **`cornering_fraction`** — fraction of live-player ticks with `min(x, y, 36-x, 36-y) ≤ 2.0 m`
   **and** ≥1 alive **melee** body within its own reach. Arena is 36 × 36 m, origin bottom-left, read
   off `header.frame`. Reach is the **engine's own**, read from
   `g5_header.g5.commit_reach.by_attacker_m` (law: `min(range_m over damaging skills) + target
   radius`) — boss 2.5, Vanguard 2.5, **Evocator 18.5**. "Melee" = reach ≤ 3.0 m, which keeps the
   first two and drops the Evocator: an 18.5 m reach is not a wall-pin, it is a caster with line of
   sight. Both figures are emitted (`cornering_fraction` and `cornering_fraction_any_reach`) so the
   choice is visible; **on this cohort they are identical on every one of the 200 seeds** — the
   Evocator never adds a cornering tick the melee bodies did not already own.
2. **`min_hp_fraction`** — `min` over ticks of `tick.entities[player].hp / max_hp`. Present on every
   tick block; no event-level reconstruction needed.
3. **`intake_pool_fraction`** — `SpatialFightResult.player_damage_taken / 759.0`, the cell's own
   statistic.

## SELF-CAUGHT ISSUES, ON RECORD

1. **⚑ The brief's arm description was wrong, and it would have been a `TypeError`, not a silent
   no-op.** The task said `wr3_encounter_ai_v1=True` goes on **both** `build_scenarios` and
   `run_spatial_fight`. `kitcal_g5_scenarios.build_scenarios` is keyword-only with **no `**kwargs`**
   and has no such parameter (signature at `kitcal_g5_scenarios.py:1200-1221`). The cell's `ARMS`
   dict reaches the **engine half only** (`**arm_kw` on `run_spatial_fight`). Transcribed from the
   source per the brief's own "character-for-character" instruction. The exactness of the n=200
   reproduction is the proof the transcription is right.
2. **⚑ `sink_neutrality` is not an artifact root key.** The brief pointed at
   `wr3_acc.json` → `sink_neutrality`; the root keys are `[ablation, acceptance, anchor_parity_leg,
   arm_of_record, arms_run, cell, commission, gates, math_note, matt_signed_intent, mix,
   predictions, secondary_NON_DECISIONAL, seeds, sub_flag_inertness, tiers, vocabulary_probe]`. The
   proof lives at `vocabulary_probe.sink_neutrality_detail`. Re-proven here independently anyway.
3. **⚑ ENGINE-SIDE, ROUTED: the trace's `damage` event stream carries no over-time channel.**
   Summing `delivered` over player-targeted `damage` events under-reads
   `SpatialFightResult.player_damage_taken` by up to **47.5 %** (max residual 288.96 HP), and the
   residual is **one-signed non-negative on all 200 seeds** — exact on only 17 of 200. So the event
   sum is a **lower bound** on intake, not a second measurement of it. This scan uses the
   fight-result figure and never the event sum; the `--scan-only` path, which has no fight result in
   hand, labels its substitution `event_stream_delivered_sum_LOWER_BOUND_no_dot_channel`. **No
   `TODO(drax)` override was added** — nothing is being compensated for, the gap is reported.
4. **⚑ MY OWN READER WAS THREE LABELS SHORT.** `AI_STATES_W1` in `wr2_playback.gd` listed six
   members; W-2 grew the vocabulary to **nine** (`dormant` / `alert` / `return`). Left as it was,
   this reader fires `push_warning "OUTSIDE the R-WR3-14 vocabulary"` on **every dormant and alert
   tick of the acceptance cohort** — a correct, in-vocabulary label reported as an out-of-vocabulary
   defect, which is the noise that trains a reader to ignore the warning that matters. Extended
   against the engine's own list (`vocabulary_probe.AI_STATES`). `return` is registered even though
   the artifact measures it never emitted (the pursuit-timeout limb is unsampled, G-W2-7).
5. **⚑ MY OWN CENSUS PRINTED A HARD-CODED "92,525".** `_ai_print_census()` announced
   *"`decision` records carry NO subject — 92,525 of them"* on every trace this scene has ever
   opened — a literal from the WR2 battery. On the acceptance cohort it was not merely stale, it was
   **backwards**: these traces carry **zero** decision records. Now counted per trace, and a zero
   prints as a measurement ("the producing cell left the emission gate shut").
6. **⚑ `_ai_src_census` was accumulated and never printed.** Its own declaration says it exists so
   that *"the render used `ai_state`" is a measurement rather than an intention* — and it was the
   intention. Now printed. **Measured on this clip: `{"ai_state": 1840}`** — every one of the 1,840
   enemy tags was painted from `ai_state`, **zero** fell through to the `commit_state` fallback.

## `ai_state` IS PAINTED, AND VERIFIED WITH MY EYES

The frame painter already reached `ai_state` (landed at owner-eye #4). Two things were owed and are
now done: the three W-2 members are **in the vocabulary** (item 4) and have **their own colours** —
deliberately cooler than `approach`/`engage`, because a dormant boss wearing the engage blue reads
as a threat that is not there:

- `dormant` dead slate · `alert` dull gold · `return` cold green

Verified on captured frames, not asserted: frame 0020 carries **ALERT** in gold over the boss and
**DORMANT** in slate over the Vanguard. Census for this fight: boss `{dormant 6, alert 3, engage 216,
windup 45, strike 9, recover 81, null 1}`; Vanguard `{dormant 175, alert 2, approach 24, engage 22,
null 1}`; Evocator `{null 1}` (it dies on tick 0); the **player block carries no `ai_state` key at
all**, which is the three-valued presence AI-D3 named, handled in three arms.

## GUARDS

Engine tree **never opened for write** · the banked artifact
`output/kitcal_g5/wr3_acc/wr3_acc.json` opened **READ-ONLY**, nothing regenerated there ·
`project.godot` NOT touched · beam / walltop / ambient shaders NOT touched · prior cells' clips
(`tmp/wr3anchor/`, `tmp/wr2/`, …) intact · authorised surfaces: `scripts/wr3_acc_pick_scan.py`
(new) + `scripts/wr2_traceset.gd`, `scripts/wr2_playback.gd`, `scripts/run_wr2_playback.sh`
(modified).

## OWED / OPEN

1. **Trace custody, same shape as the anchor.** `tmp/wr3acc/traces/` (87 MB, 200 files) is
   **untracked**; a `git clean` here takes it. Regenerable deterministically in **11 s** by
   `python3 scripts/wr3_acc_pick_scan.py --seeds 200`, which cross-checks itself against the frozen
   artifact on every run. Not banked, by choice.
2. **⚑ `tmp/wr3acc/clips/frames/` is 799 MB of PNGs and I could not prune it** — the `rm` was
   denied by the sandbox. The mp4 is encoded and complete; the frames are pure intermediate.
   **Someone with delete rights should `rm -rf ~/Games/reincarnated-godot/tmp/wr3acc/clips/frames`**,
   or leave it — nothing depends on it.
3. Carried unchanged from owner-eye #4: `TelegraphSpec.family` dropped at the emission boundary
   (rung (a) still dead — the `attack_id` substring sniff is still carrying the discriminator; this
   clip's three novas and three blizzards were separated by it); MIGRATION ANCHOR-REFIT §2(1) still
   false at this boundary; the split-declaring roster row still has no entity id; the beam/pool
   brightness package still at Matt's eye; `GPUParticles3D` per-launch non-determinism.
4. **`project.godot` is still dirty from a prior cell** (`[rendering] mesh_lod/lod_change/
   threshold_pixels=1.0` removed) and is **still not mine to bank**. Unchanged statement from
   owner-eye #4.
