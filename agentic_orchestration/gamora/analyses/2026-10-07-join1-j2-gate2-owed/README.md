# JOIN-1 · J2 Gate-2: engine-side owed items (KP-340)

gamora, 2026-10-07. This answers jack-ryan's S1/E5 Gate-2 finding (`qa/findings/2026-10-07-join1-j2-s1-e5-gate2.md`, collab `ca731da6e`), § 5 items 1–3 and 10.

## Engine commits (each committed alone)

| Commit | What |
|---|---|
| `f50b7e25` | **The ONE instrument commit.** Adds `gamora_join2_structural_2026_10_07.py` with its predictions in the docstring, committed before any run of record. INFO-S1-1: forbidden dirs + control nc8j. INFO-E5-1: `operand_pack` recorded in the JOIN hook record and in JOIN-PROVENANCE. The hook now **fails closed** (defect below). Tests: fail-first shown. |
| **`0dda17bd`** (rulebook, tree `cb38bbdf…`) | **The ONE rulebook move.** INFO-E4-1 / INFO-E4-2 on their own rows: `operands.NOT_READ_IN_V0` for `pcl_defence_pct`; A-2 rows 23 and 28 get `bound_by_j2_binder: false` plus a note. No value, no `_FIELDS` provenance string and no form changed. |
| `ef327a15` | **Instrument fix, a second commit, declared.** The structural script's aggregation glob also matched the emitter's `*.cell.json` dumps and crashed *after* all 50 child runs had finished. Adds `dynamic-report` (rebuilds the report from the child outputs on disk; nothing is re-emitted). Also adds a declared post-hoc scope beside the comparison as predicted. |

**Rulebook worktree:** `4da5044b` → **`0dda17bd`**, clean. **drax re-pins once, to `0dda17bde1ee5ac727f41ccb8b85f475a922c096` (tree `cb38bbdfc6fd7fc4105d856417b5f0c4e96503e4`), at D2's Gate.**

## Defects found, and how they are fixed

1. **The JOIN hook could run UNBOUND.** Python's `site` swallows any non-SystemExit exception raised in `sitecustomize` ("Error in sitecustomize") and runs the interpreter with exit 0.
   - **How it surfaced.** E5c (`7f80d3cd`) made the control-spec path call `from_pack()`. In the scratch-worktree hook tests that raised `FileNotFoundError`, so 3 control-spec tests ran unbound and failed.
   - **My miss.** After E5c I ran only `py_compile`, not the tests, and reported E5 without seeing this.
   - **No run of record was affected.** The E5 golden master bound (26/26 records, bind-log row 0 = PACK). The runner's fingerprint check would also have flagged an unbound run, because a substituted key with no installed fingerprint is a hit.
   - **Fix (`f50b7e25`).** Every hook step is guarded, and any exception is now a JOIN2-HALT. The hook also builds the pack OperandSet explicitly (`JOIN2_RB_ENGINE_ROOT`, else the rulebook's declared resolution).
   - **Tests.** New test `test_hook_fails_closed_when_the_pack_is_not_found`. Against the committed E5c hook, 4 hook tests FAIL (fail-first).
2. **The aggregation glob** (`ef327a15`): described in the table above.

## Results

### P-J2-5: offense certainty (`pj25.json`; path captured by `dynamic/`)

| Claim | Prediction | Result |
|---|---|---|
| `p2m_attacker_OA` | 3259.0 on every row | **3259.0, uniform** |
| min over the 95-row OA/DA table of `probability_to_hit(3259, DA)` (sealed equation) | 103.53684386948976 | **103.53684386948976** (`4059e25ba663a110`); max deviation from the CSV's 4-dp `p2m_pth_raw` is 4.9e-5 |
| every path (record, wave) **on the table** has p ≥ 100 | yes | **yes: 74 / 74; path min 105.98** (`hero/springscrab_h01` @ w152) |
| path pairs **absent** from the table | counted, not predicted | **122 of 196** (112 records never in the table, e.g. bosses, bounties and summons; 2 on the table at other waves only) |
| draw sites added | 0 | **0** (dynamic, below) |

**What this does and does not show.**
- **Shown:** certainty holds for the 74 path pairs the OA/DA table measures. The DA at which p = 100 is **DA\* = 2897.2555**, against a table maximum of 2770.09.
- **Not shown:** the 122 absent pairs. No measured DA exists for them in the pinned corpus, and the design's guard (`OffenseHitUndecided` when p < 100) **is not implemented in v0**. So the theorem is a **37.8 % coverage result, not a proof over the path**. That is a finding for the J2 Gate-2 and J3: either source DA for those records or implement the guard.
- **WITHDRAWN supplementary reading** (`pj25_board_da_supplement.{py,json}`, kept for the record).
  - It read DA from the mitigation board's `DA` column for all 196 pairs (min p 157.03).
  - **That column is not the equation's DA input.** It omits the level and attribute terms: for the same pairs the table's DA is about 1,600 higher (e.g. 558.5 vs 2174.875). The reading is invalid and is not evidence.

### P-J2-8: the alias scan, committed output (`aliases.json`)

**Scan method:** `ast` over every sealed `kc2` module, covering single-line and parenthesised `from … import` alike, plus call-time imports. The scan set is the A-2 rows' symbols and operand constants. After that, a JOIN-shaped child installs GD and reads back every module-level holder.

| Prediction | Result |
|---|---|
| function holders = exactly the `player_sustain` pair, both IDENTICAL to the installed form | **as predicted** |
| D_ENGAGE_M ×6, EOR_RADIUS_M ×5, FIXTURE_ATTACK_SPEED_PCT ×3: IDENTICAL shared object | **as predicted** |
| SOULFIRE_PERIOD_S ×2: "equal-bits at GD, a by-name copy" | **count as predicted, characterisation WRONG.** Both holders (`channel`, `energy`) import **`fixture.SOULFIRE_PERIOD_S`**, the shared `Cited`, and read back IDENTICAL. No module holds `secondary_streams.SOULFIRE_PERIOD_S` by name |
| other operand constants: counted | BASE_TICK_PERIOD_S ×1 (`channel`), `locomotion.Mover` ×1 (`run`): both IDENTICAL |
| 0 STALE | **0 STALE**; 20 holders in all, 15 of them multi-line imports |

### TA-X-21 / 26(d) / 27(c) / 28 over the JOIN tree

**Static** (`static.json`, rulebook at `0dda17bd`):

| Class | Rulebook sites |
|---|---|
| `round(` | 0 |
| draw | 0 |
| leech cap | 0 |
| `max(0, 1 − x/100)` | 3, each a **TRANSCRIPTION** of the site in the sealed body it replaces under GD: `secondary_streams` :277 and :293, `summon_offense` :475 |
| uncapped `1 − x/100` | 4 (see the MISS below) |

- **0 NEW sites.**
- **TA-X-26(d) proper:** 0 resist helpers on the leech/sustain path in either tree. The sealed sustain fold reads `adcth_mult_*` from the CSV column.
- **The sealed tree's "leech cap" hits** are the counter `n_caps_applied` (its field and its export), not a cap.
- **MISS (instrument category, recorded):** predicted 1 uncapped site, got **4**. The uncapped regex also matches the 3 `max(0, 1 − x/100)` lines; the 4th is `forms.mitigate` :76, which transcribes `threat.py:314`. All 4 are TRANSCRIPTIONs, so the substantive claim holds. The script's `pass` reads false on this count and **was not tuned**.

**Dynamic** (`dynamic/dynamic_report.json`): 25 cells × ORACLE / JOIN, emitter `--cell` under one profiler, engine `f50b7e25`, rulebook `0dda17bd`.

| Prediction | Result |
|---|---|
| draw multiset ORACLE == JOIN, all sites | **MISS as predicted, 25/25 cells:** each cell differs on exactly two **stdlib import-time** entries, `secrets.py:20` SystemRandom construction and `<frozen importlib._bootstrap>` getrandbits. Both are present under ORACLE and absent under JOIN, because the JOIN hook imports those modules in `sitecustomize` before the profiler starts |
| same, over the simulation's own sites (`reincarnated/`, `join2_rulebook/`); **declared post-hoc** in `ef327a15` | **equal in 25/25** |
| round-site multiset ORACLE == JOIN | **equal in 25/25** (all sites) |
| offense path set ORACLE == JOIN | **equal in 25/25** |
| draw / round sites under `join2_rulebook/` | **0 / 0 in 25/25** |
| distinct draw call sites (reported, not predicted) | **30** simulation call sites, all in sealed `kc2`, excluding Random construction |

**TA-X-28:** no leech cap anywhere in the rulebook (static). G3, the leech grain, is FILE-equal under JOIN (golden master below).

### INFO-S1-1: the pack is forbidden to ORACLE interpreters, with a control

- The pack directory and the S1 loader are in **both** `forbidden_dirs()` (§ 4.7 v4) and the witness's `FORBIDDEN_DIRS`, asserted equal by test.
- **nc8j** (`s47-nc8j/`), as predicted: B′ RED.
  - Path hit "opened a file in a rulebook/hook directory" on the HEAD child, naming `…/kc2-rulebook-pack-v0-20261007_182352/manifest.json`.
  - Witness hit on the HEAD pid (`opened_forbidden` = that file).
  - Census equal; sealed child GREEN.
  - Limb B also flags the manifest as a file changed since the seal.

### INFO-E5-1: JOIN-PROVENANCE records the pack copy read at bind

`golden-master/JOIN-PROVENANCE.json` → `operand_pack_at_bind`:
- pack realpath `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-rulebook-pack-v0-20261007_182352`;
- loader realpath;
- engine root HEAD `ef327a15…`;
- `git status --porcelain` = "" (clean);
- 8 tracked files;
- the digest pin.

The runner now treats a dirty or untracked pack as a hit, and requires one identical record across all 26 pids.

### Golden master and § 4.7 at the results

- **JOIN[warlord, GD] at rulebook `0dda17bd`:** J-S8 7/7 ROWSET-equal and **all 7 grain FILEs byte-equal to the fixture**. TA-X equal; 26 records, tree ok, 0 hits. Bind-log row 0 = operand-source PACK `974ff092…`. A-2 digest `9b89d534…` (labels).
- **§ 4.7 v4 at engine HEAD `ef327a15`:** **ORACLE BYTE-IDENTICAL**. HEAD fixed; A, B and B′ pass; B′ path hits none. This is the first § 4.7 run with the pack in the forbidden list.

### INFO-E4-1 / 2 / 4: closed

- **E4-1 and E4-2:** now on their own rows (`0dda17bd`), as the Gate's § 1.5 asks ("on its own row", "say so on the row"), as well as in the E4 README § 7 (`dc09064ed`).
- **E4-4** asked for the README "where it lists them". The E4 README is append-only, so the status of record ("pass under recheck at `47c976f7` / `99043eed`") is in its § 7 corrigendum, which names § 1's two runs.

## Bulk evidence

Moved with `os.rename` (nothing deleted) to `/Users/admin/Games/join2-gate2-owed-bulk-evidence/`:
- `golden-master/{emission,records}`;
- `dynamic/{*.cell.json,*.records}`.

`bulk_manifest.json` (sha256 verified after the move) and `emission_manifest.json` stay in each run directory. The dynamic child outputs (`ORACLE_*/JOIN_*.json`) and logs stay in the repo.
