# Finding — 2026-06-19 — str-9pass-floor clear-room measurement run

**Reviewer:** jack-ryan
**Severity:** PASS (overall Gate-2) — with one INFO ruling on the §11.1 seed-stride finding
**Target:** harness `612c1a8` (engine) + results `df6486f` (collab)
**Developer:** gamora (harness build + V1–V6 self-verification), gandalf (full-run execution in persistent parent session)
**Principles applied:** Review Principles #1 (math-before-code), #2 (smoke-gate / measured-not-defaulted), #3 (cross-seam impact / read-only), #4 (decisions-log as truth), #5 (severity matters); Disciplines #1, #2, #3, #11, #12

## What I found

This gate is INDEPENDENT of gamora's self-verification — I confirmed all seven gates first-hand from the production source and from the 4752-cell JSON (not the printed flag). The trap at `gauntlet_sim.py:1019` is real exactly as documented (`if t1_routing == TIER_1_REJECT: … continue` at `:1029`, which skips the tier_2 call at `:1032` and the `enc_result.tier_2_kpm` assignment at `:1041`, leaving it defaulted 0.0). The harness structurally bypasses it: it drives `run_one_cell → w4g2_tier_2_full_sim` directly (harness `:573`), never executing the caller-gate. From data: all 4752 cells ran `n_fights==20` (zero short, zero missing KPM, zero term-sum mismatches). The 20 cells with `observed_kpm==0.0` are NOT the trap — they are all `mini_boss` cells with `termination_counts={timeout:20}`, i.e. a genuinely MEASURED STR survive+kill=0.000 (b_dead=0), not a defaulted masquerade. STR's clear-room verdict is one-sided and wide: open_arena 192/192 in-band (min 11.034 vs floor 9.90, +1.13), chokepoint 144/144 (min 12.757 vs 11.65, +1.11), magic_pack 144/144 (min 6.704 vs 6.06, +0.64), elite_pack 0/192 in-band (max 3.396 vs floor 5.65, −2.25 below). Per-cohort clear-room pass count is 120/120/120/120 (spread 0). The 3 passing clear types sum to 10 of the 14 clear encounters; elite_pack (×4) is the only failing type. V6: engine commit `612c1a8` touches ONLY the two harness files; collab `df6486f` touches ONLY diagnostic JSON/TXT — no gate file (`gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, `t4_sim_cycling.py`) in either commit. The bands read AS-IS match the canonically-locked gandalf-ruled values in decisions-log lines 4205/4229. Boss rail reproduces STR=0.000 with controls corroborating (dex 0.79, int 0.99, wis 0.99) — the harness is not broken.

## Per-gate verdict

- **V1 (the trap — load-bearing): PASS.** Trap confirmed first-hand at `gauntlet_sim.py:1019-1029`. Harness drives tier_2 directly (`:573`), never the caller `continue`. Verified FROM DATA: all 4752 cells `n_fights==20`, n_fights distribution `{20: 4752}`, zero short, zero missing `observed_kpm`, zero defaulted-0.0 masquerades on clear shells (the 20 zero-KPM cells are measured mini_boss timeouts, term `{timeout:20}`). Not the printed flag — independent scan.
- **V2 (faithful / max-profile power): PASS.** `apply_max_profile_investment=True` default flows the full chain (`combatant.py:486`, flip #3) un-overridden through `run_one_cell → w4g2_tier_2_full_sim → run_spatial_fight`. Faithful by construction; reuses blessed `build_population`.
- **V3 (proxy-inclusive KPM): PASS.** `observed_kpm = mobs_killed/min`, `mobs_killed = sum(1 for m in self.mobs if not m.is_alive)` (`spatial_engine.py:1762`) — attribution-agnostic, counts proxy/summon/DoT kills by construction.
- **V4 (clear-shell win-condition integrity — load-bearing): PASS.** 14 clear shells resolve on `all_mobs_killed` (`arena.py`, KILLS_ONLY set `:94-100`). Verified FROM DATA: `Σ termination_counts == n_fights` for every one of the 4752 cells (zero mismatches).
- **V5 (single regime): PASS.** Live `w4g2_tier_2_full_sim` per cell, no persisted phase3 KPM read; mobs/min numerator (`t4_sim_cycling.py:1097`); metadata regime fingerprint `spatial_current_mobs_per_min_faithful`. No old-scale KPM mixed in.
- **V6 (no gate regression — protects production): PASS.** `git show --stat 612c1a8` = 2 harness files only; `df6486f` = 4 diagnostic output files only. Zero edits to any gate file, `ENCOUNTER_COHORT_KPM_BAND`, or routing. The runtime band-table read matches the locked decisions-log values. No MIGRATION needed (read-only diagnostic).
- **Discipline #3 (inter-run seed disjointness): PASS.** Clearroom seed span `[700000, 766703]`, boss harness span `[619000, 684303]`; `684303 < 700000` → disjoint. Confirmed arithmetically and per-fight derivation read first-hand (`spatial_engine.py:2244`: `seed = base_seed ^ (fight_idx * 0x1337BEEF)`).

## Ruling on the §11.1 seed-stride finding: INFO (verdict-immaterial)

The intra-run stride overflow is REAL and correctly self-surfaced per Discipline #12: `enc_idx*100` reaches 1700 for 18 shells, overflowing the 1000 kit-stride, so seeds bleed across kit blocks (production uses a 10,000 kit-stride at `t4_sim_cycling.py:1628`). Empirically: 2080 colliding seed values → 2048 cross-cell shared-noise pairs + 32 same-(shell,cohort) collisions.

I independently tested gamora's two load-bearing claims and found one **imprecision that does not change the disposition**:

- **Claim (a) — "32 true-duplicate redundant samples" is directionally right but imprecise.** Of the 32, only **16 are byte-identical redundant samples** (all STR elite_pack, same `legendary_id`, e.g. kpm 2.492==2.492). The other 16 are INT elite_pack pairs that share (shell, cohort) but have DIFFERENT `encounter_id` → different combat inputs → shared-noise-stream, NOT redundant samples (their KPMs differ, e.g. 9.0 vs 9.281). This is a finer split than gamora stated, but it makes the contamination LESS, not more.
- **Claim (b) — margins dwarf any effective-n reduction: CONFIRMED, structurally.** All 32 collisions land on `elite_pack`. STR elite_pack is ALREADY 0/192 in-band by a 2.25 KPM gap (max 3.396 vs floor 5.65) — no n-reduction flips a type failing by 3× the worst dup jitter. Critically, the **3 PASSING clear types have ZERO true-dups** (verified: true-dup-pairs-by-shell = `{elite_pack: 32}`), so their 192/144/144 in-band counts are untouched by any collision. The verdict (10 of 14, spread 0) is structurally immune to the overflow.

The trap never fired (every cell ran a full executed batch), so the defaulted-0.0 masquerade this run exists to avoid is structurally impossible here. The inter-run disjointness that Discipline #3 actually guards holds. This is a **harness seed-spacing defect to FIX before any re-use** (adopt the production `*10_000` kit / `*1_000` cohort / `+enc_idx` layout), with empirically-zero impact on THIS run's disposition. INFO, not WARN/BLOCK.

## Overall Gate-2 verdict: PASS

All six verify-gates PASS, Discipline #3 inter-run disjointness PASS, and the §11.1 intra-run seed-stride finding rules INFO (verdict-immaterial). **gandalf is cleared to read the numbers as data and rule the STR 9-pass-floor disposition against the pre-registered table.** The measurement is sound: STR passes 10 of the 14 clear-room encounters (open_arena + chokepoint_corridor + magic_pack all fully in-band across all cohorts; elite_pack fully below-floor), spread 0 across cohorts, on a fully-measured tier_2 batch with the production gate untouched.

## Action

- [x] jack-ryan: Gate-2 PASS issued; gandalf cleared to rule disposition.
- [ ] gamora (non-blocking, INFO): before any re-use of this sibling harness, fix the kit-stride to ≥ `n_shells * cohort_stride` (adopt production `base + config_idx*10_000 + cohort_idx*1_000 + enc_idx`). Tracked as a seed-spacing defect, not a result correction.
- [ ] gandalf: rule the disposition against the pre-registered interpretation table (`agentic_orchestration/gandalf/notes/2026-06-19-str-9pass-floor-pre-registered-interpretation.md`).

## References

- `reincarnated-engine/src/reincarnated/simulation/str_9pass_floor_all18_harness_2026_06_19.py`
- `reincarnated-engine/src/reincarnated/simulation/math/str-9pass-floor-all18-clearroom-harness-2026-06-19.md` (V1–V6 + §11.1)
- `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:1019-1041` (the trap), `:591/:1071` (band predicate)
- `reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py:1097` (mobs/min numerator), `:1628` (production kit-stride)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:1762` (mobs_killed), `:2244` (per-fight seed)
- `agentic_orchestration/cycle-14-wave-5-season-001/str-9pass-floor-all18-clearroom-2026-06-19.json` (4752 cells, independently scanned)
- `reincarnated-engine/design/decisions/decisions-log.md:4205,4229` (locked band values, gandalf-ruled)
