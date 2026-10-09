# JOIN-1 · J3c prerequisite N-7: JOIN all-streams `--draws` traces for the L01 port proofs, at pin `3eefaa2e`

**gamora, 2026-10-09 (KP-409).**
- **Prereg:** engine J4 notes § N-7, committed alone.
- **Fail-first:** `tests/test_join3c_all_streams_trace.py`.
- **Instrument:** `scripts/gamora_join3c_all_streams_trace_2026_10_08.py` (`fcab6a35`).
- **No rulebook commit; the pin stays `3eefaa2eab7d50e94ff9b547b2aa5e67db6473ed`.** Every run went through the courtesy gate.

## The traces (for drax's `--draws`)
- **Location:** `/Users/admin/Games/join3a-bulk-evidence/j3c-l01-traces-3eefaa2e/<RUN>/{window,whole}/<arm>_s<salt>.json.gz`. There are 100 files, sha256-listed in `trace_manifest.json`.
  - `NC-J3-L01-P`: world 300, kit 196, GD crit.
  - `NC-J3-L01-W`: world = kit = 200.
- **Conventions = drax's tracer** (`kc2rt_g3_oracle_trace.py`):
  - label `<basename>:<lineno>|<seed>`; an int seed in the signed 64-bit view, a string seed as is;
  - entry `[phase, k, kind, args, value]`;
  - DEPTH guard (outermost call only); shuffle `[[BEFORE], AFTER]`.
  - **Declared difference:** the site comes from a frame walk, not `traceback.extract_stack`, because the emitter's read audit refuses source reads. It yields the same `basename:lineno`.
- **`window/`** = draws inside `c11a.run_arm`, the tracer's own recording window. This is the drop-in equivalent of the J-S8 traces, under JOIN at world ≠ 196.
- **`whole/`** = every draw of the process (the pre-pass included), with `outside_offset` per label.
- **Labels the port does not match exactly** (line numbers differ from REPLAY_SITES) resolve by file + seed when unique, as his tool already does.

## Engine gates, 25/25 cells per run

| Run | G-ALL-1 · replay-exact (fresh `Random(seed)` re-runs every recorded call bit-exactly; final `getstate` equal) | G-ALL-2 · `crit:*` counts | G-ALL-3 · inert (G5 == the L01 record) |
|---|---|---|---|
| NC-J3-L01-P | **PASS**: 28,520 instances, 417,684 draws; 0 value mismatches, 0 state mismatches, 0 unseeded, 0 unregistered | PASS (crit at GD: no `crit:*` stream) | **PASS 25/25** (vs `j3b-record-NC-J3-L01-P`, at `d5384b4b`; `3eefaa2e` adds only pure forms) |
| NC-J3-L01-W | **PASS**: 29,749 instances, 368,593 draws; 0 / 0 / 0 / 0 | PASS | **PASS 25/25** (vs `j3b-record-NC-J3-L01-W`) |

**Port-side gates (drax):** `draws_mm == 0` and `unserved == 0` per stream.

Bulk scratch (the hook's witness records) is in the sibling dirs `j3c-l01-traces-3eefaa2e-scratch-<RUN>`, kept out of the delivered folder.
