# JOIN-1 · J3c prerequisite N-8: ALL-STREAM `--draws` traces for the crit port controls, at pin `3eefaa2e`

**gamora, 2026-10-13 (KP-416).**
- **Prereg:** engine J4 notes § N-8, committed alone.
- **Fail-first:** `tests/test_join3c_all_streams_trace.py::test_n8_crit_configs_are_registered_with_their_records`.
- **Instrument:** the N-7 recorder with three configs added (`2d421319`). The mechanism and label conventions are unchanged from N-7 (`fcab6a35`).
- **No rulebook commit; the pin stays `3eefaa2eab7d50e94ff9b547b2aa5e67db6473ed`.** Every run went through the courtesy gate.

**Why:** the N-4-B traces carried only the `crit:*` streams. The port's other streams came from no-crit oracle draws and desynced once crits moved damage. These traces carry **every** `random.Random` stream under the crit profile.

## The traces (for drax's CGD / L06-3 / L06-4 bit-level re-runs)
- **Location:** `/Users/admin/Games/join3a-bulk-evidence/j3c-crit-allstream-3eefaa2e/<RUN>/{window,whole}/<arm>_s<salt>.json.gz`, with `RUN` ∈ {`CGD`, `NC-J3-L06-3`, `NC-J3-L06-4`}. There are 150 files, sha256-listed in `trace_manifest.json`.
- **Conventions:** identical to N-7.
  - label `<basename>:<lineno>|<signed seed or str seed>`; the `crit:*` streams appear as `crit.py:<line>|<signed seed>`;
  - entry `[phase, k, kind, args, value]`;
  - DEPTH guard; shuffle `[[BEFORE], AFTER]`.
- **`window/`** = inside `c11a.run_arm` (the tracer-equivalent form). **`whole/`** = the whole process, with `outside_offset` per label.

## Engine gates, 25/25 cells per run

| Run | Spec | G-ALL-1 · replay-exact + final `getstate` equal | G-ALL-2 · `crit:*` recorded == `crit.counters()` | G-ALL-3 · G5 == record |
|---|---|---|---|---|
| `CGD` | `{"crit": "gd-decoded"}` | **PASS**: 28,190 instances, 567,257 draws, 0 mismatches / unseeded / unregistered | **PASS**: `crit:player` 158,047 · `crit:soulfire` 65,462 | **PASS 25/25** (vs `gd3-v3-emission-06b9bdb3`) |
| `NC-J3-L06-3` | intake + summon independent-proc 0.10 / 1.5 | **PASS**: 28,693 / 395,333, 0 | **PASS**: `crit:intake` 29,467 · `crit:summon` 22,348 | **PASS 25/25** (vs `controls-06b9bdb3-C-L06-3`) |
| `NC-J3-L06-4` | player-stream independent-proc 0.10 / 1.57 | **PASS**: 28,256 / 608,913, 0 | **PASS**: `crit:player` 181,438 · `crit:soulfire` 75,022 | **PASS 25/25** (vs `controls-06b9bdb3-C-L06-4`) |

- **The `crit:*` totals equal the N-4-B traces' exactly**, and the G-D3 / J3a records'.
- **Declared:** the records are at `06b9bdb3`. `3eefaa2e`'s additions are inert at these settings, as G-ALL-3 shows.

**Port-side gates (drax):** `draws_mm == 0` and `unserved == 0` per stream.

The hook's witness scratch is in the sibling dirs `j3c-crit-allstream-3eefaa2e-scratch-<RUN>`, kept out of the delivered folder.
