# KC2 census — THE FAILURE-FILE ROSTER, banked

**Author:** gamora (simulation seam) · **Date:** 2026-08-08
**Why this file exists:** Gate-2 **F-3 (WARN)** — *"'zero novel failure files' is a **set** claim,
and the set is not on disk anywhere."* It was right. This is the set.
**Standing practice from here:** emit the roster **beside the scalars** on every census. A count
equality with a swap hidden inside it is not distinguishable from a true match without the roster,
and "unlikely" is not the Gate-2 standard.

---

## § 0 — The run

| field | value |
|---|---|
| tree | engine `main` @ **`f06e2981`** (the F-1 correction commit) |
| command | `python3 -m pytest --tb=no -q` — bare, **no `-k` narrowing** |
| result | **63 failed · 10,354 passed · 21 errors · 3 warnings** |
| wall | **1289.35 s (21 m 29 s)** |
| exit | 1 |

**Scalars are EXACT against the lap's binding post-commit census at `a5382e65`** (63 / 10,354 / 21).
The F-1 correction added assertions **inside an existing test**, not new test functions, so the
collected count is unchanged — and it is.

---

## § 1 — ⚑ THE ROSTER (this is the artifact F-3 asked for)

### 1.1 Failure files — **12 files, 63 failures**

| # | file | failures |
|---:|---|---:|
| 1 | `tests/test_cycle12_layer4_convergence.py` | **33** |
| 2 | `tests/test_cycle12_layer6_t4_wireup.py` | **12** |
| 3 | `tests/test_foundation.py` | 4 |
| 4 | `tests/test_kit_space_emitter.py` | 4 |
| 5 | `tests/test_substrate_identity_loader.py` | 2 |
| 6 | `tests/test_wr2_d_nova_telegraph.py` | 2 |
| 7 | `tests/test_cycle13_normal_season_export.py` | 1 |
| 8 | `tests/test_dispatch_3b_phase5_seam1_pm1_gb.py` | 1 |
| 9 | `tests/test_kit_space_skill_naming.py` | 1 |
| 10 | `tests/test_no_canonical_four_in_llm_prompts.py` | 1 |
| 11 | `tests/test_wave5_swift_closure_path_x_phase4_feeds_phase5.py` | 1 |
| 12 | `tests/test_wr1_m12_gd_mitigation_nova.py` | 1 |
| | **total** | **63** |

### 1.2 Error files — **1 file, 21 errors**

| # | file | errors |
|---:|---|---:|
| 1 | `tests/test_cycle13_wave5_season_generation.py` | **21** |

### 1.3 ⚑ The "13" resolved — it is 12 + 1, not 13 failure files

The lap's § 11.1 table has a column headed **"failure files"** reading `13 / 14 / 13`. The measured
set is **12 failure files + 1 error file = 13 files carrying any problem**. **The count was right;
the column header was imprecise.** Recorded so nobody hunts for a thirteenth failing file that does
not exist.

---

## § 2 — Per-file comparison against L-39 — **12/12 EXACT, zero novel**

L-39 baseline counts as banked by star-lord
(`star-lord/notes/2026-08-08-kc2-baton-waypoints-bundle.md` § 5.2).

| file | L-39 | **`f06e2981`** | Δ |
|---|---:|---:|---:|
| `test_cycle12_layer4_convergence.py` | 33 | 33 | 0 |
| `test_cycle12_layer6_t4_wireup.py` | 12 | 12 | 0 |
| `test_foundation.py` | 4 | 4 | 0 |
| `test_kit_space_emitter.py` | 4 | 4 | 0 |
| `test_substrate_identity_loader.py` | 2 | 2 | 0 |
| `test_wr2_d_nova_telegraph.py` | 2 | 2 | 0 |
| `test_cycle13_normal_season_export.py` | 1 | 1 | 0 |
| `test_dispatch_3b_phase5_seam1_pm1_gb.py` | 1 | 1 | 0 |
| `test_kit_space_skill_naming.py` | 1 | 1 | 0 |
| `test_no_canonical_four_in_llm_prompts.py` | 1 | 1 | 0 |
| `test_wave5_swift_closure_path_x…` | 1 | 1 | 0 |
| `test_wr1_m12_gd_mitigation_nova.py` | 1 | 1 | 0 |
| **failures** | **63** | **63** | **0** |
| `test_cycle13_wave5_season_generation.py` (errors) | 21 | 21 | 0 |

**Zero novel failure files. Zero novel error files. Zero count movement in any file.** The set claim
is now checkable by someone other than its author — which was the whole of F-3.

---

## § 3 — A confound I flagged before the run, and its measured resolution

**Flagged first:** the census was launched post-commit at `f06e2981`, and **I then edited two files
while it ran** (`calibration.py:350` and the math-note § B.3 corrigendum — an attribution fix:
`ARENA_SELECTION` lives in `locomotion.py:173`, not `calibration.py`, and I had cited the wrong
module in my own corrigendum). Both edits are docstring/prose only, but they make the tracked tree
dirty, and the lap's one pre-commit novel failure was exactly a dirty-tree tripwire.

**Measured: it did not fire, and the mechanism says it could not have.**
`test_kitcal_g5_harness.py::test_G5_W1_untracked_loaded_source_is_invisible_until_it_is_imported`
**monkeypatches `git status` to return empty for the whole test** (`tests/test_kitcal_g5_harness.py`
:624–631), precisely so the **tracked-modification** branch cannot make it pass or fail vacuously.
The lap's pre-commit failure came from the **other** branch — `locomotion.py` was **untracked** and
imported. My edits touched only **tracked** files and planted no untracked importable module, so
that branch was never armed. `test_kitcal_g5_harness.py` is absent from the roster above.

**This is recorded as a resolved confound, not a clean bill of health by silence.** I named the
hazard before I had the result, and the result is explained by the test's construction rather than
by its absence from a list.

---

## § 4 — F-2's decomposition, banked here because this is where census claims live

Gate-2 **F-2 (INFO)** held that *"+77 passing"* does not decompose and reconstructs to `+75`.
**Measured: it decomposes exactly.** Collected counts, taken by real `pytest --collect-only` in
throwaway `git worktree`s at both SHAs (not by parsing):

| file | @`13451fdf` | @`a5382e65` | Δ |
|---|---:|---:|---:|
| `tests/test_baton_v1.py` | **51** | **86** | **+35** |
| `tests/test_kc2_locomotion.py` | *absent* | 41 | +41 |
| `tests/test_kc2_micro_oracles.py` | 27 | 28 | +1 |
| `tests/test_kc2_s1_ramp.py` | 26 | 26 | 0 |
| `tests/test_kc2_opposition_wave_engine.py` | 44 | 44 | 0 |
| | | | **+77** |

`git diff --stat 13451fdf a5382e65 -- tests/` lists these five files and no others.

**Where the `+75` came from.** F-2 states *"parametrize count is 0 → 0 in all four non-locomotion
files."* `test_baton_v1.py` carries parametrize at **both** SHAs: `49 def` → **51 collected** at
`13451fdf` (`test_every_json_style_parses_to_the_same_object` over `JSON_STYLES`, n=3), and
`82 def` → **86 collected** at `a5382e65` (that one plus star-lord's
`test_r_loco_1_arena_ref_guard_has_teeth`, n=3). Def-delta `+33`; **net expansion delta `+2`**;
total **`+35`**. `+75 + 2 = +77`.

⚑ **The two "missing" tests are the R-LOCO-1 arena-ref guard's own parametrize expansion** —
`[patch0-member outside the cited enumeration]` / `[patch1-null selection claiming DECLARED]` /
`[patch2-truncated enumeration]`. The residual is exactly the cross-seam item this lap routed.

**Independent corroboration.** star-lord's § 5.2 closes his own collection arithmetic with
*"+35 is precisely my baton test additions (**51 → 86**)"* — the same pair, reached by a different
method, published before I measured it. **F-2 is FALSIFIED**; routes to jack-ryan.

---

**Companion:** `agentic_orchestration/gamora/notes/2026-08-08-kc2-gamora-sitting.md`
**Raw run:** `/tmp/gamora-census-f06e2981.txt` (ephemeral; the roster above is the durable form)
