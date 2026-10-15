# Finding — 2026-10-15 — JOIN-1 J4b second sealed change set (S24a–e + S25a/b + S26) — delta Gate-2

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: **PASS-WITH-NOTES**; 0 WARN / 6 INFO)
**Target:** runtime `fb49080f3f657dccc63ee65c44a1fcd997185a45e31a52e6f7c823cf13d80142` (godot `4e93fa7`, local tag `kc2/referent-v1-sealed-r2-runtime-j4b2s26`)
**Developer:** drax
**Consent rows:** KP-455 (S24a–e), KP-452 (S25a/b), KP-456 (S26); ledger KP-457 / KP-458 (collab `10dd106b8`)
**Principles applied:** REVIEW_PROCESS 1, 2, 3; Disciplines #8, #10; KP-312 conditions 2–4; CLAUDE.md sealed-artifact protocol

## What I re-derived (my own scripts and commands, not drax's tables)
| Check | Method | Result |
|---|---|---|
| Tree digest | Recomputed the manifest law from git blobs at `4e93fa7` and at HEAD | **fb49080f… at both**, 107 members, 0 mismatches; base `83c5dee` = 8bba8eac…. `kc2_runtime/` is untouched since the seal and the worktree is clean |
| (1) Hunk collapse | `83c5dee→4e93fa7` on `kc2rt_fight.gd` | **added-only**: 16 lines, 0 removed. Every pair is an `if rulebook != null` guard tagged `J4b S2x` plus one body line. Stripping exactly those pairs gives the **base byte-for-byte**. Sites = {S24a–e, S25a, S25b, S26}, equal to the audit JSON's approved set |
| (1) S26 the only new behaviour | `0ae5a01→4e93fa7` | **exactly 2 added lines, the S26 guard + `continue`**; S24/S25 are unchanged |
| (1) Census | Diff of `kc2rt_booking_census.gd` | 55/55 rows match modulo line numbers (3 residues are line refs inside comments); `census_grep` re-run: **MATCH ROW FOR ROW 43/55** |
| Mirror census | Re-ran `kc2p_j4b_mirror_census.py` plus my own grep for indirect calls (`call("_cons_add")`, Callable) | **8 found / 8 pinned MATCH**; no indirect callers |
| Records are mirror-side | Read `kc2rb_port.gd:613`, `kc2rb_d2_flinch.gd:58` | `record_hit` appends to the mirror's `pending`; **no new fight member**. Records are pre-clamp (`applied`, `cb_applied`, post-Cruel `d`, summon `h[1]`), with `H = hp_max`. Soulfire and summons are alive-filtered before the record |
| (2) G3 | Value- and byte-compared 25 summaries vs `2026-10-07-g3-25cell-kp310-V311FULL-256b3e4/summaries` | **25/25 byte-equal**, `trace_sha256` 25/25; `vendor.txt` = fb49080f |
| (2) T-A | `cmp` of 25 `cell.json` vs `2026-10-07-ta-preread-kp310-472cffc4-cells` | **25/25 FILE-equal** (also 25/25 vs the first J4b seal); `runtime_digest_at_boot` = fb49080f |
| § 4.7 | Hashed the `[s4.7]` lines (GREEN dropped) vs KP-310's per-mode files | **4/4 modes EQUAL**, 5/5 seeds GREEN each |
| J-S8 / P4b | Read the 10 committed diff JSONs | `all_equal` true on 5 + 5 arms; 7/7 grains; 0 rows differing |
| .app / attempt-2 | `attempt2.log` | 54/0, negative controls 16/16 RED; the `runtime_header` read by running the .app equals the vendored digest |
| (3) Reach vs acts | Predictions in `3d417e1` (committed 13:39) vs probe wall clock (17:42–17:44Z = 13:42–13:44 local, after the 13:42:16 seal) | off: S26 21,629 / S24 8,437 / S25 0 / ALL EQUAL. d2world: S26 20,382 / S24 8,953 / S25 2,018 / NOT EQUAL / gate (b) 0. **Every predicted limb is as stated, recomputed from `JOIN-PROVENANCE.json`** |
| (4) WARN-2 | Re-ran the current grader `f3009efd` on the probe's own grains (scratch copy); computed `tick − GB.off_tick` for every `dying` G1 row | **PASS: (a) 0, (b) 0, (c) 0, `dying_not_at_death` 0, `n_dying_rows_in_window` 11**. All 18 dying rows sit at `off_tick − 1`, the death tick of a `[on, off)` span. 0 non-dying attacks after `off_tick` |

## Notes (INFO)
- **N-1 · S24b (L-02) and S24c (L-07) are not exercised in this profile.** Reach is counted only as aggregate `J4B-S24`, and both lines share source key `eyeofreckoning1` with S24a, so the evidence cannot separate them. They are proven only null-inert. **Before any profile turns on L-02 or L-07:** add per-sub-site counters (S24a…e), then run a reach + replay probe.
- **N-2 · Records exceed GH rows by one.** S24 shows 8,953 against 8,952 GH rows (d2world probe). This is the same one-row remainder as my CORR-3 INFO-1; name it in the graded run. It is an out-of-tree matter, not a seal defect.
- **N-3 · The word "offered" means two different things.** In the runtime, `_offer` books **pre-mitigation raw**. In CORR-3, GO `offered` is the **pre-clamp applied** value. S24a records `applied`, which is correct for CORR-3's `d`. Never compare GH `d` to the `offered` census key.
- **N-4 · S26 also gates FREEZE-locked pets.** Its guard is `body_locked`, so under her kit, frozen monster pets now stand still where they walked at seal 8bba8eac. KP-456's wording covers this. Any evidence from her arm before `4e93fa7` is superseded for pet motion.
- **N-5 · The probe's GH rows have no `seq`** (they come from the pre-CORR-3 emitter). Graded runs need the seq-bearing instruments (`726ce52`) and the replay plus completeness checks.
- **N-6 · The windowed self-test was skipped (declared).** The tag stays local until Matt's windowed self-test. I verified it is not on `origin`.

## Action
- [ ] drax: N-1, adding sub-site counters before any L-02/L-07 profile. Do not push the tag.
- [ ] gamora: name the N-2 remainder. Grade with the seq-bearing grains (N-5).
- [ ] Matt: the windowed self-test, then the tag push. No other decision is needed. KP-312 condition 4 is discharged by this Gate-2.

## References
- godot: `kc2_runtime/sim/kc2rt_fight.gd`, `kc2_runtime/MANIFEST.json`, `kc2_runtime/tests/kc2rt_booking_census.gd` at `83c5dee` / `0ae5a01` / `4e93fa7`
- godot evidence: `evidence/join1/j4b2-hook/{build-s26,audit-controls-s26,failfirst-s26,reach-post-s26,proofs-fb49080f,app-fb49080f}`; `evidence/kc2-play/2026-10-15-ta-preread-j4b2s26-fb49080f-cells`; `evidence/join1/j4b-hook/mirror-census`
- probe grains (not in the repo; read-only): `/Users/admin/Games/join3c-bulk/j4b2s26-probe/post-d2world{,-join}`
- engine grader `f3009efd`; predictions `kc2_play/tools/kc2p_j4b2s26_probe.sh` at `3d417e1`
