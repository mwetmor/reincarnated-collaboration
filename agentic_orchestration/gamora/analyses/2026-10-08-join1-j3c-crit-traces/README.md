# JOIN-1 · J3c prerequisite N-4-B: the JOIN crit:* `--draws` traces at rulebook `d5384b4b`

**gamora, 2026-10-08.**
- **Prereg:** engine J4 notes § N-4-B (`math/join1-j4-design-notes-2026-10-08.md`), committed alone before the instrument.
- **Fail-first:** `tests/test_join3c_crit_trace.py`.
- **Instrument:** `scripts/gamora_join3c_crit_trace_2026_10_08.py` (`cc5faec0`).
- **No rulebook commit; the pin stays `d5384b4b951092911cf75a05103987ab772f6343`.** Every run went through the courtesy gate.

## The traces (for drax's `--draws`)
- **Location:** `/Users/admin/Games/join3a-bulk-evidence/j3c-crit-traces-d5384b4b/<PROFILE>/{whole,window}/<arm>_s<salt>.json.gz`. There are 150 files, sha256-listed in `trace_manifest.json`. The port's `_load_trace` reads `.json.gz`.
- **Format:** `{"arm", "salt", "streams": {label: [[phase, k, "random", [], u], …]}, "stream_ids": {label: "crit:…"}, "profile", "rulebook_commit", "label_status"}`.
  - `whole` = every draw of the process: the `c11a._period()` pre-pass, then the window.
  - `window` = window draws only, plus `prepass_offset` = {label: number of pre-pass draws}.
- **Label (PROVISIONAL; drax to agree; a rename, not a rebuild):** `join2_rulebook/crit.py:stream|<signed seed>`, with seed = `crit.seed_of(arm, salt, stream_id)` (sha256 `"{arm}|{salt}|{stream_id}"`, first 8 bytes, big-endian), shown in the signed 64-bit view.

## Gates (engine side), per profile, all 25 cells

| Profile | G-REC-1: recorded == `crit.counters()["draws"]`, per stream | Totals (recorded = counters) | G-REC-3 (inert vs the G-D3 record) |
|---|---|---|---|
| `gd-decoded` | **PASS 25/25** | `crit:player` 158,047 · `crit:soulfire` 65,462 (equal to the G-D3 re-emission's) | **PASS 25/25** (G5: terminal, wave, n_ticks, final_hp) |
| `NC-J3-L06-3` (intake + summon independent-proc 0.10 / 1.5) | **PASS 25/25** | `crit:intake` 29,467 · `crit:summon` 22,348 (equal to the J3a control's) | n/a |
| `NC-J3-L06-4` (player-stream independent-proc 0.10 / 1.57) | **PASS 25/25** | `crit:player` 181,438 · `crit:soulfire` 75,022 | n/a |

- **G-REC-2** (whole == pre-pass ++ window; offset == len(pre-pass)) is enforced per cell by the instrument: a violation HALTs the cell. None occurred.
- **G-REC-4** (no stream at GD) is a form test, green.
- **Port-side graded gates (drax):** per `crit:*` stream, `n_mismatch == 0` **and** `unserved == 0`.
- **drax decides** whether the port replays from `whole` (the pre-pass included) or from `window` + `prepass_offset`.
