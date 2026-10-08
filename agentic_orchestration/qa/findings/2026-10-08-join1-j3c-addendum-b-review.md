# Finding — 2026-10-08 — JOIN-1 KP-396 · DESIGN-MODE review of J3c inventory ADDENDUM B (X-path probe, S-11b in-form)

**Reviewer:** jack-ryan (DESIGN-MODE, before Matt rules on S-11)
**Severity:** PASS-WITH-NOTES (INFO only)
**Target:** godot `e97cde3` (Addendum B + `evidence/join1/j3c-hook/xprobe/`, 15 files)
**Developer:** drax
**Follows:** `b392a24b1`; WARN-1 and INFO-1…4 there
**Principles applied:** 1, 3, 5

## Checks

**The probe method is valid.**
- **What it does.** `probewrap.py` uses `sys.monitoring` LINE, first hit per line, then DISABLE; the result per configuration is a union over cells. It runs gamora's emitter child with the environment `run_join` builds: profile `gd`, sealed `969fbd8d` source, and the rulebook worktree. I checked that worktree: HEAD `d5384b4b`, clean.
- **Population:** 25 cells per configuration, all rc 0.
- **The cell-matched diff (`agg2.py`)** is right for the question "which branches does X reach that 196 does not".
- **Limits, stated by drax:** a line probe sees branches, not values. The static sweep covers values.
- **One provenance gap (INFO-1).** The Addendum-A V311-FULL probe (`probe_v311full.py`) rooted the **live** engine `kc2/`, not the sealed worktree. This is valid only because engine HEAD's `kc2` tree = `7496a28a` = the sealed tree, which I verified today. Record that equality beside the list.

**The diffs and the sweep support "no further site".**
- The P300-only lines (29) and the W200-only lines (14) are event or telemetry branches, the H-18 / S-10 paths, or values whose port counterparts derive from `ticks_per_s` / `_period_s()`.
- **My own, broader token scan** over the same 3,906 JOIN-only lines adds `frame`, `fps`, `_s`, `_ms`, `round`/`ceil`/`floor`, `1000`, `/16` and `*16`. It flags 242 lines, 181 of them outside drax's 61. On inspection those are:
  - import-time `def` / field lines (`gate_model`, `deferred_arrival`, `kinematics`, `calibration`);
  - telemetry or calibration constants;
  - accumulators already dispositioned: `movement.py:429–516` follows the clock; `control_states.py:450` falls under P0-6; `player_drive.py:249–268` falls under P0-9.
- **No new clock-bound value on the port.** INFO-2: commit the scanner and its token list. Only its output is in the evidence dir.

**The retarget parity verdict is correct.** `player_drive` 12/24 ticks and port `kc2rt_fight.gd:212/214` are fixed on both sides, so the mirrors stay equal at any X. It is a modelling question, and a conditional **S-12** if gamora's answer rebinds it in Python. Same class as P0-6 and P0-7.

**The emitter hook is a pure refactor at the defaults.**
- `kc2p_join1_gm_emit.gd:1086–1090` defines `typeb`, `v19` and `d19`. Only `typeb` is read afterwards (`:1092`, `:1109`).
- `superseded_value` has no side effect beyond `last_error` on absence (`kc2rt_v3p2.gd:144–148`). Moving the five lines verbatim into `_typeb_for(pack)` therefore preserves behaviour.
- INFO-3: the JOIN override should call `super(pack)` **first** and keep it, then substitute under a moved clock. That way a missing `V19-TYPEB-1` row still trips the zero-rate refusal rather than being masked by the derived `p`.

**Re-pinning the J-S8 port-half instrument.**
- No KP-312 consent is needed: the file is outside `kc2_runtime/`. But its bytes (`5a9466c2…` @ `34e77e3`, re-hashed today) are **frozen** by D2 site list C-1 / #75 cl. 6 and pinned in the J-S8 port manifests.
- **Recommendation:** name it in the same Matt S-11 ask as one explicit line ("S-11b moves in-form by un-freezing the J-S8 port-half emitter: a verbatim refactor, re-proved at the new digest"), rather than treating it as consent-free.
- The re-proof drax lists is the right set: J-S8 port ORACLE 7/7 vs `f82807fb`, inertness (bare == hooked), the 196 unit bits, and the forced-pack-value negative control at P300. **The old J-S8 evidence stays valid at the old digest.**

**INFO-3 / INFO-4 from `b392a24b1` are closed.**
- B.4 makes each RED attributable: the first differing field must be a release field, or the run HALTs. W200 isolates S-11b.
- B.5: I re-grepped. Only the two report lines carry `typeb_duration_ticks` (const 7). No grader reads it.

**Replaying `crit:*` from the window is sound.**
- The port has no `c11a._period()` pre-pass, so its first `crit:*` draw corresponds to the window's first (gamora recorder `cc5faec0`, traces `d7c496bbc`: G-REC-1 25/25).
- `n_mismatch == 0` plus `unserved == 0` per stream proves the kinds and the exact consumption. The `site|<signed seed>` label ties the stream identity.
- INFO-4: also assert `len(whole) − len(window) == prepass_offset` per label, so the window cut itself is checked rather than taken from the recorder.

## Action
- [ ] drax:
  - INFO-1: record the kc2-tree equality beside `lines_V311FULL196.json`;
  - INFO-2: commit the clock scanner and its token list;
  - INFO-3: the override calls `super(pack)` first;
  - INFO-4: the window-offset assertion.
- [ ] Conductor: fold the J-S8 port-half un-freeze into the S-11 ask as one line.
- [ ] Matt: S-11 = S-11a (5 sealed lines) + S-11b in-form (emitter refactor, re-proved). **Ready to ask.**

## References
- godot `e97cde3`: Addendum B; `evidence/join1/j3c-hook/xprobe/` (`probewrap.py`, `drive.py`, `agg2.py`, `probe_v311full.py`, `lines_*.json`, `diff_*.txt`, `sweep_join_minus_v311_clock_scan.txt`)
- `kc2_play/tools/kc2p_join1_gm_emit.gd:1080–1112`; `kc2_runtime/loader/kc2rt_v3p2.gd:144–148`; `kc2_runtime/sim/kc2rt_fight.gd:212/214`, `:6703`; `kc2_runtime/play/kc2play_driver.gd:769`
- Engine `cc5faec0`; collab `d7c496bbc`; engine HEAD `kc2` tree `7496a28a`; rulebook worktree `d5384b4b`
