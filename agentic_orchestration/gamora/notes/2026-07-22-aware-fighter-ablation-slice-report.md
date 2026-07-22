# Aware-Fighter Ablation Gate — As-Built Slice Report (named-gamora)

**Executor:** named-gamora (simulation seam). **Conductor:** gandalf `RUN-CONDUCTOR` (ledger L-28/L-29).
**Authority:** the FROZEN prereg sheet `2026-07-22-aware-fighter-ablation-prereg.md` (§1–§8) +
execution charter `2026-07-22-aware-fighter-ablation-execution-charter.md` incl. **RC-1**.
**Nature:** a RUN, not a build — **ZERO engine edits**; engine frozen at `2f43045`. All instrument
code lives in collab notes.

**This report states PREDICATE FACTS ONLY.** The VERDICT (PASS / FAIL / PARTIAL) is the conductor's
DRIFT-CRITIC synthesis against the frozen sheet + Matt's ruling. No verdict word is captioned here.

---

## RC-1 attestations — all three beats CLEAN (run-start / seal / verdict)

| Beat | HEAD | unmoved @ `2f43045` | tracked `*.py` diff under `src/reincarnated/` | non-output tracked deltas | exempted output/ delta (hash) |
|---|---|---|---|---|---|
| run_start | `2f43045` | ✓ | EMPTY | none | `output/leg3_pilot_section8a1_band_measurement.json` — `89380d21fc46…` |
| seal | `2f43045` | ✓ | EMPTY | none | same file — `89380d21fc46…` |
| verdict | `2f43045` | ✓ | EMPTY | none | same file — `89380d21fc46…` |

- The ONLY tracked working-tree delta at every beat is star-lord's `output/` data-sink report
  (RC-1-exempt; not read by any code path either arm executes). Its `git hash-object` was **stable**
  (`89380d21fc46074fd631393975de6fe1d9f54a4c`) at seal-time and verdict-time (star-lord's Lane-1 did
  not rewrite it during my run; RC-1 permits drift either way — both recorded).
- **Zero `*.py` diff** under `src/reincarnated/` at all three beats; **HEAD never moved.** No RC-1
  red-flag condition tripped. Post-run engine re-attestation confirms `2f43045` / empty py-diff /
  exempted-file-only.

## Site-coverage attestation (§7 pin 5 — re-verified at `2f43045`)

`_policy_choose_target` (the policy seam) is the **ONLY** player target-choice source at the frozen
hash. I re-verified every route myself (not by inheritance): primary/movement `:1574` (with
`boss_focus`), attack-target `:1957` (`entity.is_player` branch), E4 whiff-projection `:3137`/`:3239`
(BW-1.1 F2), and the three helper calls that thread `self._policy_config` — `:3590`, `:3922`,
`:4062`. `_policy_config` is set at `:2407` (default BLIND). I hunted every residual raw
`min(…distance…)` in the engine: the six survivors (`:1360` AOE point-hit computation, `:1959` the
MOB branch of the seam-gated `if entity.is_player`, `:3875` mob navigation, `:3889` ally-proxy target,
`:4253` mob retarget, `:4488` ally-proxy proximity-gate) are **all mob / ally-proxy / AOE-hit paths —
none is a player target choice.** The ablation's config-only no-confound guarantee holds in source.

## Config fidelity (§3 — imported VERBATIM, no edits)

- `BLIND_CONFIG = (("distance", 1.0),)` — asserted at import (fail-loud).
- `AWARE_CANDIDATE_CONFIG` = 6 entries, all weights 1.0: `distance_normalized`,
  `exposure_incoming_threat_density`, `cluster_density`, `crossfire_overlap`, `lane_pressure`,
  `escape_gradient` — asserted exact set + all-1.0 + `distance_normalized` (no raw `distance`) at
  import. **No weight edits between seal and verdict.**

## Smoke result (§7 pin 2) — PASS

1 cell (`I|high|d2-bowazon`) × both arms × 4 seeds = 8 + 8 records. Every captured field live and
plausible: `player_damage_taken` ≥ 0 float, `elapsed_s` > 0, `all_mobs_killed` bool (varies),
`trace_len` > 0 int (varies — traces ON), triple complete. BLIND cleared all 8 (winner=player,
40/40; triple `{mobs_killed:40, total_aoe_hits:40, player_damage_total:6000}` — **exactly matches the
W3′ seal precedent's `d2-bowazon` recorded means**, confirming frame reproduction). The config bites:
AWARE differed from BLIND on all 8 intake values, and the clear-guard tripped on this smoke cell (a
DATA finding, correctly captured — not an instrument fault; the smoke's job is field-liveness, which
passed).

## Seal — the C2 invariant HELD

- BLIND arm complete (256, both compositions) → seal-JSON flushed to disk **before any aware fight**:
  256 blind per-fight records + encounter-arm aggregate-per-seed means + `SD_seed` + RC-1 disclosure.
- Seal md5 **`d27991a2bb8d4fac1e5b9378bc747a86`** — identical at seal-time and verdict-time (re-read +
  compared at verdict; **match → no HALT**). Post-seal mutation of the blind record = 0.
- `SD_seed = 80.7016` (`statistics.stdev`, n−1, 3 df — the SAME estimator jack-ryan verified on the
  dealt stand-in). **Non-zero** → the degenerate guard does NOT bind; D3 is a LIVE floor.

## Headline predicate facts (encounter arm; intake PRIMARY, lower is better)

| Quantity | Value |
|---|---|
| `Ī_blind` (encounter mean per-fight intake) | **14730.7520** |
| `Ī_aware` (encounter mean per-fight intake) | **15116.0762** |
| `abs_margin = Ī_blind − Ī_aware` | **−385.3243** (negative → AWARE takes MORE) |
| `M_rel = (Ī_blind − Ī_aware)/Ī_blind` | **−0.026158** |
| `SD_seed` | **80.7016** (non-zero) |
| **D2** (`M_rel ≥ 0.10`) | **met = False** |
| **D3** (`abs_margin ≥ 2 × SD_seed`) | **met = False** (`−385.32` vs `k·SD = 161.40`; live floor, not degenerate) |
| **clear-guard** clean | **False — 14 mismatches** |
| **specificity** `M_rel_baseline` | **−0.028670** (flag = **False**; baseline ≈ encounter, both negative) |
| **time** AWARE slower on encounter aggregate | **+6.64%** → flag = **True** (> 5% §4 threshold) |
| seal md5 match (seal→verdict) | **True** |

Per-seed encounter aggregate intake — blind `{22:14793.5, 23:14724.2, 24:14786.3, 25:14619.1}`;
aware `{22:15170.8, 23:15111.7, 24:15188.6, 25:14993.2}`. AWARE is higher on every seed.

## Clear-guard mismatch detail (§4/§5 — the §6 PARTIAL trigger)

14 per-(cell,seed,composition) `all_mobs_killed` mismatches across **8 unique (cell,composition)**,
spanning 4 kits: `poe1-caustic-arrow`, `poe1-kinetic-fusillade`, `d2-bowazon`, `d2-poison-javazon`.
Direction **bidirectional**: **12 aware-cleared-FEWER, 2 aware-cleared-MORE** (10 encounter,
4 matched_baseline). Examples: `I|high|d2-bowazon|encounter|20260723` aware killed 3/40 vs blind
40/40 (FEWER); `II|high|poe1-caustic-arrow|encounter|20260723` aware 40/40 vs blind 16/40 (MORE).
Per §4, a clear mismatch renders that cell's intake **incommensurable in either direction** (intake
on a non-clear is not comparable), and aware-clearing-MORE "re-opens the frame, not the bar."

## C4 intake-determinism profile (rider — both arms × both compositions)

| Arm | Composition | seed-deterministic cells (intake SD=0) | seed-variable | pooled per-cell seed-SD (diagnostic) |
|---|---|---|---|---|
| blind | encounter | **0 / 32** | 32 | 92.083 |
| blind | matched_baseline | **0 / 32** | 32 | 142.278 |
| aware | encounter | **0 / 32** | 32 | 134.988 |
| aware | matched_baseline | **0 / 32** | 32 | 93.839 |

**Intake is NOT degenerate** (0/32 seed-deterministic everywhere) — exactly the C4 rationale for
intake-primary: unlike dealt-damage (which ceilings at Σ mob HP under full-clear; 21/32 encounter
cells were dealt-degenerate in the sealed W3′ battery), intake has no such ceiling. So `SD_seed` is a
genuine noise floor and the D3 predicate is live (not vacuously auto-satisfied). No near-vacuous-D3
silence to disclose — the guard did not bind.

## Per-cell intake deltas — sign counts (reported, NOT gated; `blind − aware`, + = aware less)

- **encounter:** aware-less (+) = 15 · aware-more (−) = 11 · equal = 6 (of 32)
- **matched_baseline:** aware-less (+) = 13 · aware-more (−) = 19 · equal = 0 (of 32)

Mixed both directions on encounter; matched-baseline skews aware-more. No consistent aware advantage.

## Deviations / as-found corrections (Discipline #11)

1. **RC-1 attestation source — porcelain-prefix fix (caught at smoke, pre-any-fight).** My first
   `_rc1_attest` derived tracked deltas from `git status --porcelain` by stripping a fixed 3-char
   prefix (`l[3:]`). The exempted output/ line's porcelain prefix is width **4** (` \x20M\x20`, i.e.
   `<sp><sp>M<sp>`), so the slice dropped the leading `s` → `rc/reincarnated/output/…` and the
   non-output-tracked guard false-tripped a RED-FLAG HALT. **Zero fights had fired** (the HALT is at
   the run-start beat, before any leg spawns). Fix: derive tracked deltas from
   `git diff --name-only HEAD` (bare paths, no prefix parsing). Re-attested clean; this is an
   instrument-parsing correction, not an engine or predicate change. The frozen-closure invariant
   was never at risk — the underlying git state was always `2f43045` / empty py-diff / output-only.
2. **Duration channel = `elapsed_s` (seconds), the ticks-EQUIVALENT scalar.** The charter/§4 name the
   secondary as "duration ticks"; the `SpatialFightResult` field is `elapsed_s` (fight-end elapsed
   seconds, `:4947`). At the fixed `tick_size` these are affine-equivalent (ticks = elapsed_s /
   tick_size), and the time flag is a **relative** aggregate comparison (AWARE-slower fraction), which
   is invariant to the seconds↔ticks unit. Captured `elapsed_s`; reported the relative slowdown. The
   trace-length channel (also captured per fight) is the other time proxy the sheet's §4 empirical
   basis cites; both agree AWARE is slower.
3. **All-mobs-killed boolean is DERIVED, not a native result field.** The result carries `winner`,
   `player_kill`, `mobs_killed`, `total_mob_count` — no single `all_mobs_killed` bool. The W3′ frame
   is `win_condition == all_mobs_killed` throughout, so all-killed ⟺ `mobs_killed == total_mob_count`
   ⟺ `winner == 'player'`. I derived the boolean as `total_mob_count > 0 and mobs_killed ==
   total_mob_count` and captured `winner`/`player_kill`/counts alongside for auditability. Consistent
   with the seal precedent's all-`all_mobs_killed` frame.
4. **Single-process, no worktree (unlike the BW-1 equivalence battery).** BW-1 split before/after
   across two engine trees (legacy stamp `a3671d4` worktree vs main) to prove BLIND ≡ legacy. This
   ablation runs BOTH arms at the SAME frozen main commit `2f43045` (the config is the only
   difference — §1 ablation property), so no worktree exists or is needed; both legs bind the main
   engine src and assert `bound == intended` (fail-loud). The `/tmp/aware-before-worktree` was
   already removed at BW-1.1 (confirmed absent then; irrelevant here).
5. **Smoke slices by CELL (1 cell × both comps × 4 seeds = 8/arm), per §7 pin 2.** The BW-1 harness's
   `--smoke` sliced 2 pairs × 1 seed; the prereg §7 pin 2 specifies "1 cell × both arms × 4 seeds."
   I implemented the pin's slice (n_done ≥ 1, all 4 seeds, both compositions), not the BW-1 harness's
   older 2-pair × 1-seed slice. Reported as-built.
6. **What is committed vs regenerable (BW-1 precedent).** Committed the four charter-named artifacts:
   runner + seal JSON (embeds all 256 blind per-fight records) + verdict-input JSON (embeds all
   derived facts) + this report. The per-leg raw dumps (`…-blind-full.json`, `…-aware-full.json`,
   smoke dumps) are **regenerable-not-committed** — the frozen runner + frozen engine + fixed seeds
   reproduce them bit-for-bit (BW-1 "full traces regenerable-not-committed" precedent).

## Guardrails honored

**Zero engine edits** (RUN, not build) · engine frozen `2f43045` at all three beats · `corpus.db`
opened READ-ONLY (`?mode=ro`) · no telemetry-schema changes · no seed additions (fixed
{20260722–25}) · did NOT touch star-lord's `output/` file · commit-never-push (the conductor pushes) ·
`git -C <repo>` explicit throughout.

## Artifact paths (all absolute)

- Runner: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-runner.py`
- Seal JSON: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-seal.json` (md5 `d27991a2bb8d4fac1e5b9378bc747a86`)
- Verdict-input JSON: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-verdict-input.json`
- This report: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-slice-report.md`
- Regenerable (not committed): `…-ablation-blind-full.json`, `…-ablation-aware-full.json`, `…-ablation-{blind,aware}-smoke.json`
