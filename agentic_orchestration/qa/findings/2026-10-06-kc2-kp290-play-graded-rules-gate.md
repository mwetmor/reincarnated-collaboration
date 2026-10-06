# Finding — 2026-10-06 — Run KC2-PLAY · KP-290 / KP-294 · "PLAY runs the graded rules": delta Gate-2 `3e2359a6 → 892bb1c2`, plus the proof legs

**Reviewer:** jack-ryan (DEV-MODE, Gate-2 with BLOCK authority; conductor gandalf)

**Severity: BLOCK (narrow) for the H-8 re-replay. One item, BLOCK-1:** the oracle's automatic counterplay and the human's War Cry and potion keys now both apply, and that stacking is unregistered.

Everything the gate asked me to prove holds:
- **ORACLE byte-identity: PASS.** It holds by code reading and by independent re-runs. My own T-A pre_read emits **25/25 `cell.json` byte-equal** to drax's.
- **§4.7 harness: PASS-WITH-FINDINGS.** It is honest on the leg it runs: P-MOVE in the seat, the oracle's own channel verdict. But it posts **no intents**, so it cannot see BLOCK-1.
- **Config-audit probe and control: PASS** (INFO).
- **Self-test:** it does not block the replay; it blocks the re-seal.

Counts: 1 BLOCK · 2 WARN · 6 INFO.

**Target:** runtime FILE **`892bb1c279d0540a745e1c4daff1b6971aef2a9f6f4870e7380c2c66bdff27a0`** (107 members).
- I re-derived it over `git archive 0eacae1`; `MANIFEST.json` is byte-equal.
- `kc2_runtime/` is unchanged from `0eacae1` through `d4c068a`.
- Native library `74360ffa…`, unchanged.
- Delta `git diff 66605a1 0eacae1 -- kc2_runtime`: **a6d7dc2** (runtime) and **0eacae1** (MANIFEST). 7 files, +239 / −90. `play/kc2play_driver.gd`, `play/kc2play_session.gd`, `sim/kc2rt_config.gd`, `sim/kc2rt_fight.gd`, booking census, loader smoke.
- Outside the digest: **08b3f43** (`kc2_play/tools`: §4.7 harness, config audit, probe, selftest), **dbe6934** (intro card), **d4c068a** (evidence).

**Principles applied:**
- REVIEW_PROCESS #1, #4, #5.
- Disciplines #10, #11, #12.
- ADR-002.
- Charter KP-289 … KP-294: Matt's "PLAY runs the graded rules"; the seal re-opened until his re-replay.
- Prereg v1.14 § H (H-8).

**Read-only attestation.**
- godot was read only through git objects and `git archive` into my scratchpad. I did not run any Godot project inside drax's tree, `kc2_play/`, or the `.app`.
- The `.app` and the vendor copy were inspected by file hash only.
- All runs held the heavy lock. Free disk was at least 24 GiB throughout.
- Instruments: `2026-10-06-kc2-kp290-play-graded-rules-gate/` (`SHA256SUMS`).

---

## § 1 · ORACLE byte-identity: PASS

**By reading.** Every new behaviour branch in `sim/` is gated on `play_driver`, which is `null` on every graded path. `kc2rt_ta.gd`, `kc2rt_ta_emit.gd` and the G3 tools never set it.

| site (`kc2rt_fight.gd` at `0eacae1`) | graded path (`play_driver == null`) |
|---|---|
| `:1732` `play_step` dry-out `(not is_oracle or play_driver != null)` | `play_step` is not on the graded path; for a driverless caller the predicate is unchanged |
| `:1789` the oracle energy step `is_oracle and play_driver == null` | unchanged (true) |
| `:1955` the held-channel energy step `not is_oracle or play_driver != null` | unchanged (false) |
| `:2250-2257` `_drive`: `play_driver != null` → `_human_pilot()` (if `is_oracle`) | not entered |
| `:1687-1697` `_play_enter_wave` reorder | PLAY wave head only (`play_open` / `play_step`). Now in `run()`'s order (`:1562-1570`): ids + append, then emergence, pin, v3.11 open |

**The `_pmove_pilot` split is statement for statement.** I extracted mechanically the non-blank, non-comment statements of `66605a1`'s `_pmove_pilot` and compared them with `0eacae1`'s `_pmove_propose` + `_pilot_wraps`: **35 = 35, EQUAL, in order** (`review/split_compare.py`). The new `_pmove_pilot` is exactly `_pmove_propose(p0x, p0y)` then `_pilot_wraps(p0x, p0y, k)`. No local crosses the seam: `mb` and `r` stay in propose; the wraps use only their parameters and members.

**By the evidence, re-checked.**
- `equal_to_kp274.json`: `all_equal_except_trace_sha256: true`, 25/25.
- **T-A pre_read:** the 25 `ta_manifest.cells[].digest` values (the run-determined `Kc2RtTaEmit.cell_digest`) equal attempt 4's, 25/25.
- **Stronger, mine:** every one of the 25 `cell.json` files differs from attempt 4's by **exactly one line**, `telemetry_header."⚑ lineage_rows_not_hashed": 9 → 15`. That is the divergence register growing from DR-0…8 to DR-0…14. Its `register_sha256` `453231e0…` is unchanged, because lineage rows are not hashed (`preread/attempt4_vs_kp290_cells_normalised.txt`).

**By independent re-run** (`git archive 0eacae1`, heavy lock):
- **G3, contact=shadow, port side** on my own oracle traces (oracle frozen at `969fbd8d`, generated from my own archive):

  | cell | decision div. | draw mism. | death oracle / port | census · ctrl · x08 · x16 | shadow mism. |
  |---|---|---|---|---|---|
  | **M0 s3** | 0 | 0 | [160,225] / [160,225] | ✓ ✓ ✓ ✓ | 0 (44,707 scans) |
  | **W1 s2** | 0 | 0 | [160,161] / [160,161] | ✓ ✓ ✓ ✓ | 0 (41,332) |
  | M-POL-2 s2 | 0 | 0 | [160,221] / [160,221] | ✓ ✓ ✓ ✓ | 0 (43,657) |

  The summaries equal drax's KP-290 filed ones except `trace_sha256`. They are **byte-identical in every key to my own `66605a1` summaries** for the same traces.
- **T-A pre_read** (`kc2rt_ta.gd -- expect_runtime=892bb1c2… g3=<drax's 25 KP-290 summaries> run_kind=pre_read`, contact=shadow by the harness default):
  - **25/25 cell digests equal drax's filed pre_read, and all 25 `cell.json` files are BYTE-EQUAL to his.** For example, M0/3 is `bfdaf515…` and W1/2 is `3c9739cb…`.
  - The one emission failure is `runtime_header` (no `.app` in my scratch archive), the environment.

## § 2 · §4.7 harness (`kc2_play/tools/kc2p_s47_harness.gd`, evidence `…-kp290-s47-config-audit-build/`): PASS-WITH-FINDINGS

**Honesty of the substitution: confirmed.**
- The PLAY leg is `Kc2PlaySession.open` exactly as the app builds it, with `driver.pilot_substitute = "P-MOVE"`.
- `_human_pilot` calls `_pmove_propose` from the driver's **float64** tick-start (`tick_start_xy`, fed by `note_after_wraps`), then the driver's floor test, then the **same** `_pilot_wraps`.
- The channel verdict in the seat is the oracle's own `_cpf_tick_apply()` (`kc2play_driver.gd:434-438`). For M0 it returns `true` with no draw, because `channel_policy_armed` is false (`fight.gd:2449-2452`).
- The ORACLE leg is built as `run_cell` builds it (ORACLE pack, oracle board, `configure_arm_from_pack("M0")`, contact=shadow).
- The comparison runs at the tick's last line on both sides, bit-exact float64 over x, y, HP and energy, plus the channel, a body digest and the draw total.

**Results, re-read:**
- **Ablated leg (floor and pools removed): seeds 0, 1, 3 EQUAL on every channel, every tick, terminal equal.** Seeds 2 and 4 differ **only** in energy (first at ticks 991 and 543, PLAY +6.2367). Every other channel stays bit-equal to the end.
- **Plain leg:** every first divergence attributes to DR-10 (floor), DR-2 (pools) or DR-9 (energy), with the rest inherited.

**Rewritten DR-1, and `walls_armed`.** DR-1 is right: M0 arms no ArenaFold, and the audit prints `walls_armed` PLAY false = ORACLE false. DR-4 (P-MOVE; M0 always channels) and DR-14 (native vs shadow, the same library) are accurate.

### WARN-1 · The harness proves only the no-input path

It posts no intents: no skills, no potion, no War Cry, no charges. So DR-6, DR-12 and DR-13 are listed in its `EVIDENCE` map but are **never exercised**, and BLOCK-1 is invisible to it.

Three further limits:
- Attribution names only the **first** divergence per channel. In the plain leg everything after the first floor stop is "inherited". The ablated leg is what makes the proof strong.
- **The energy channel cannot go UNREGISTERED.** Any energy difference is attributed to DR-9 "structurally".
- The measured energy residue occurs **with the channel held every tick** (seeds 2, 4). DR-9's text explains the difference as "charged only on ticks the human channels", which does not describe this residue; the step order and ceiling clamp differ as well.

**Fix (drax):**
- an **intent leg**: scripted presses of each bar key at fixed ticks, with the expected deltas named per DR row;
- an energy check against PLAY's own DR-9 law rather than an unconditional attribution;
- DR-9's text to name the order/clamp difference.

## § 3 · Config-audit probe (`kc2_play/tools/kc2p_config_audit.gd`): PASS (INFO)

- The verdict compares 17 fold rows PLAY against ORACLE M0, both after the same w151 wave head. **0 differ.** The w151 roll is equal, and the rig counts over 4 seeds are equal.
- The **negative control** rebuilds the pre-KP-290 PLAY-HUMAN arm (CONFIG_PLAY pack, non-oracle board, `configure_arm("PLAY-HUMAN", …)`) and reads **15 rows RED**, so the run would exit 1 if the comparator were blind. The control is real.
- **INFO-1:**
  - The control is wholesale: every fold off at once. A single-fold control (null `mut_fold` alone, for example) would show per-row sensitivity. The comparator is per-row, so that holds by construction, but it is not demonstrated.
  - The audit does not list **`loop_layer_on` / `cp_on`** (the counterplay layer), which is where BLOCK-1 lives. Add them.

## § 4 · ⛔ BLOCK-1 · Under the graded arm, PLAY runs the oracle's AUTOMATIC counterplay **and** the human's War Cry and potion. They stack, and nothing registers it

**What is.**
- `play_open` → `_loop_layer_open` (`fight.gd:1663`, `:4348-4350`) sets `loop_layer_on = is_oracle` and `cp_on = is_oracle and not cp_kit.is_empty()`.
- Under KP-290 PLAY is configured with `is_oracle = true` (`kc2play_session.gd`, `configure_arm_from_pack(GRADED_ARM, true, …)`).
- So the counterplay layer runs every tick in PLAY (`_cp_begin_tick`, `:2009`): **War Cry on its cooldown (V13-WARCRY-1, −29 % incoming), the health potion at its threshold (V13-POTION-1/2), Menhir's Will, Turtle / Barrier / Ascension, HoTs.**
- On a graded M0 cell this layer absorbs **736,370 HP** (attempt-4 cell M0/3, `counterplay_absorbed`).
- The human's bar is unchanged and ungated by `is_oracle`:
  - `war_cry` → `_fire_warcry` sets `fight.play_incoming_mult = 0.71`, applied separately on the raw row (`fight.gd:5892-5895`);
  - `potion` → `_fire_potion` (flat + instant % + HoT) (`kc2play_driver.gd:465-581`).
- **A pressed War Cry therefore multiplies on top of the automatic one, and a manual potion adds to the automatic potion.**
- Before KP-290 the arm was PLAY-HUMAN with `is_oracle = false`, so the layer was off and the human's keys were the only source. **KP-290 created the overlap.**

**Why the register does not cover it.**
- **DR-12-potion's ORACLE column reads "absent (the scripted pilot carries none)". That is false.** The oracle's counterplay layer drinks potions (V13-POTION-1; `cp_counts.health_potion`).
- **DR-6** ("Blitz not simulated; … War Cry radius 16.0 … OFF under ORACLE") speaks of the bound-skill riders in the old two-configuration world. PLAY is now itself under the oracle configuration, and the row says nothing about the automatic War Cry running beside the human's.
- No DR row says the two **stack**.
- §4.7 (§ 2, no intents) and the config audit (no `cp_on` row) both pass with it present.

**Why it blocks the re-replay.**
- Matt's ruling is that PLAY runs **the graded rules**, with every remaining difference a DR row (KP-291 – 293).
- The defect is material: a −29 % incoming multiplier, and an extra potion, on top of a layer that already absorbs ~0.7 M HP per cell.
- It is silent: the driver's `buffs()` (`kc2play_driver.gd:774-783`), the HUD's buff source, lists only the human's War Cry and potion HoT, never the counterplay layer's.
- It is invisible to every proof leg filed.
- A replay taken on this build would not be a replay of the graded configuration plus registered differences, which is the exact defect KP-289 re-opened the seal for. Same failure family as Discipline #12: a semantic shift with no name on it.

**Path forward. The choice is a design call, so it is ruled by Matt; the conductor elicits it.**
- **(a) Recommended, smallest.** Under `GRADED_RULES`, the human's `war_cry` and `potion` keys do not cast, because the counterplay layer casts them as the graded configuration does. Register this as DR-15, and show the automatic casts on the HUD so Matt sees them.
- **(b)** Turn the automatic counterplay off in PLAY and let the human's keys drive War Cry and potion. This is a larger registered divergence (manual timing in place of cooldown and threshold).
- **(c)** Keep both, registered as a stacking divergence with its magnitude.

**Whichever is chosen:**
- correct DR-12's ORACLE column and DR-6's wording;
- add `cp_on` to the config audit;
- add an intent leg to §4.7 that presses `war_cry` and `potion` and names the row;
- the digest moves (`play/` and `sim/kc2rt_config.gd` are members), so re-run § 1's identity legs: G3 25/25 and the pre_read. I will re-gate the delta.

## § 5 · The windowed self-test is owed: it blocks the re-seal, not the replay

- The headless build-gate legs are GREEN on all three filed runs: the probe, the geometry and the bar keys (War Cry 29 %, every key fired).
- The **windowed** self-test on the calibrated 1920×1080 canvas did not run, because the host display became 3440×1440 and the export used `KC2_SKIP_SELFTEST=1` (declared).
- The sim proofs (§ 1 to § 3) do not depend on it, and Matt's replay is itself the human check of that surface.
- **It does not block the replay** (once BLOCK-1 is closed). **It blocks the re-seal:** the sealed `.app` must have passed its full build gate.
- If the self-test later fails on a presentation defect that could have affected what Matt saw, the replay is repeated on the fixed build.
- **Owner:** drax, on a 1920×1080 window, or by setting the canvas, before the seal.

## § 6 · WARN / INFO (non-blocking)

- **WARN-2 · DR-10's "Where" points at a function this change renamed.** It cites `kc2play_driver.gd _clamped`, which a6d7dc2 renamed to `_walkable`. Its `tested_by` and the semantics are otherwise right: the stop is now applied and returns to the float64 tick-start. Fix with BLOCK-1. (drax)
- **INFO-2 · The floor stop now applies.** The old `_clamped` returned the refused position itself, so the correction was counted and emitted but **never applied** (a6d7dc2). That fix is correct and overdue. It also means pre-KP-290 PLAY sessions (P1(e)) could leave the floor; nothing graded depends on them.
- **INFO-3 · A float32 counter on the PLAY side.** `drive()` still updates `max_player_radius_m` from `player_pos.length()` (float32), before the wraps' float64 `hypot`. It is a counter only, and PLAY is not graded.
- **INFO-4 · The DR rows sit outside the register hash.** DR-0…14 are lineage, not hashed by `register_sha256` (unchanged at `453231e0`). They are still pinned by the runtime tree digest. Record it so that nobody reads an unchanged register hash as "no register change".
- **INFO-5 · 5b525ec-style self-consistency.** The `kc2p_probe` statue guard now accepts a far park when GD engagement holds it. That is a PLAY build-gate relaxation tied to the v3.11 laws, and it is declared.
- **INFO-6 · `_play_enter_wave` was out of order.** Before KP-290 it registered emergence, the stationary pin and the v3.11 wave-open **before** appending the bodies (a6d7dc2 message). That was inert while PLAY armed no fold. The fix aligns it with `run()` (`:1562-1570`), and §4.7's bit-equality on 5 seeds confirms the wave head empirically.

## Verdict

- **ORACLE identity (proof leg 1): PASS.** Every new branch is gated on `play_driver`. The split is statement for statement. G3 is 3/3 mine plus 25/25 drax's. **My own pre_read is byte-equal on 25/25 cells.**
- **§4.7 (proof leg 2): PASS-WITH-FINDINGS** on the no-input path (WARN-1). DR-1, DR-4 and DR-14 are accurate. **DR-6, DR-9, DR-10 and DR-12 need correction, and the register is not complete** (BLOCK-1).
- **Config audit (3): PASS**; the control is real (INFO-1).
- **Self-test (4):** blocks the re-seal, not the replay.

**Overall: BLOCK (narrow).** Matt's H-8 re-replay should not run on `892bb1c2` until BLOCK-1 is ruled and fixed or registered. The fix does not touch the ORACLE path. Its re-gate is the § 1 identity legs plus an intent leg in §4.7.

## Action

- [ ] **gandalf (ELICITOR → Matt):** put BLOCK-1's choice (a), (b) or (c) to Matt. I recommend (a). Hold the re-replay until it lands.
- [ ] **drax:**
  - implement the ruling;
  - correct DR-6, DR-9, DR-10 and DR-12, and add DR-15;
  - add `cp_on` / `loop_layer_on` to the config audit, with a single-fold control;
  - add the §4.7 intent leg;
  - regenerate the MANIFEST and re-run G3 25/25 and the T-A pre_read;
  - run the windowed self-test on 1920×1080 before the re-seal.
- [ ] **jack-ryan:** delta Gate-2 on the fix.

## References

- **Godot (git objects / `git archive 0eacae1`, `d4c068a`):**
  - `kc2_runtime/sim/kc2rt_fight.gd:457, 1540-1570, 1663, 1671-1712, 1732, 1786-1800, 1955-1970, 2000-2012, 2250-2257, 2370-2378, 2449-2452, 4340-4352, 4385-4480, 5885-5897, 7912-7980`;
  - `play/kc2play_session.gd:34-45, 98-170`;
  - `play/kc2play_driver.gd:430-440, 465-600, 609-690, 690-770`;
  - `sim/kc2rt_config.gd:55-190`;
  - `tests/kc2rt_ta_emit.gd:170-200`; `tests/kc2rt_ta.gd:441-445, 540-550`;
  - `kc2_play/tools/kc2p_s47_harness.gd`, `kc2p_config_audit.gd` (08b3f43);
  - evidence `2026-10-06-g3-25cell-kp290-V311FULL-0eacae1/`, `2026-10-06-ta-preread-kp290-892bb1c2-cells/`, `2026-10-06-kp290-s47-config-audit-build/`, `2026-10-03-ta-attempt1of2-overall4-v1.15-cells/` (attempt 4).
- **Engine (`969fbd8d`, read-only, my scratch archive):** the oracle composition for G3.
- **Collab:**
  - charter KP-289 … KP-294;
  - my prior gate `2026-10-02-kc2-attempt4-candidate-h3-h5.md` (incl. the 2026-10-03 delta).
