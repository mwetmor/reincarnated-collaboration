# Finding — 2026-10-13 — JOIN-1 KP-417 · J3c close-out delta Gate-2 (whole sealed-runtime change set)

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority; before Matt's windowed self-test)
**Severity:** PASS-WITH-NOTES (0 BLOCK, 0 WARN, 6 INFO)
**Target:** reincarnated-godot
- sealed commits `f414985` (tag `…-j3c`, tree `1700221b`) and `d419666` (tag `…-j3c-s12`, tree `a0e75469`);
- mirror pin `3eefaa2e`;
- emitter `f2432d4` / instrument-of-record `6b31769`;
- `755d30a`, plus the evidence commits named in KP-417.

**Developer:** drax
**Principles applied:** 1, 3, 5

## What I verified independently (read-only; no Godot runs)

| KP-312 leg | Result |
|---|---|
| **Consent covers every sealed site** | Site tags in the two sealed diffs: S-1, S-2, S-3, S-4, S-5, S-7, S-9a/b, S-10, S-11a, M-3 (`f414985`); S-12, M-4 (`d419666`). Ledger: KP-360 (S-1…S-5, S-7, S-9; census rows (a)), KP-363 (M-3), KP-395 → KP-397 (S-10; S-11a; "FULLY CONSENTED"), KP-412 (S-12 including its member M-4), KP-397/402 (the emitter unfreeze, three hooks). **No unconsented site.** S-6 stays held |
| **Hunk audit** | **I re-ran** `kc2p_j3c_hunk_audit.py --config kc2p_j3c_audit_build_config.json` on the tree as it stands. Null projection == `1b244fb` byte for byte in all 4 files; the sites found equal the approved set (13); **PASS**. See INFO-1 |
| **S-12 conditions (`c1dd4b884`)** | The report G-A sits immediately after the pure `want_ambush` line and is guarded on **`board.rulebook`**. The board wiring is a G-A after S-9, guarded on `clock.rulebook`, which closes the gap I raised. The three board sites are G-B; M-4 is declared. **Met** |
| **Census** | `f414985` adds exactly the 8 S-1/S-3 rows + 2 paths (KP-360 (a)). With digits normalised, `d419666` is a pure relocation |
| **Fail-first preceded each site** | S-10 / S-11 / S-7 ran on local variant tags `j3c-ff/v0`, `v1` (19:21), and the provenance records `runtime_tag` (INFO-2). S-12 fail-first `d27e629` (06:36) came before `d419666` (06:40). Emitter hook controls RED as predicted (`0591b86`) |
| **ORACLE identity** | **T-A:** I compared all 25 `cell.json` files with `cmp` against `2026-10-07-ta-preread-kp310-472cffc4-cells`: **25/25 FILE-equal**. **G3:** I compared all 25 summaries field by field against KP-310: **25/25 identical**, including `trace_sha256`. § 4.7 4×5 IDENTICAL and J-S8 ORACLE 7/7 ×5 with inertness 25/25 are taken from the verdicts and diffs |
| **Value fidelity, bit level** | L01-P and L01-W: 7/7 ×10 arms, draws_mm 0, unserved 0. Crit gd-decoded / L06-3 / L06-4 on all-stream traces: 7/7 ×15 arms, per-stream n_mismatch 0 and unserved 0. Row-level replays: 0 unequal (after the precision fix, which had its own fail-first) |
| **Graded as pre-stated** | Graded exactly as pre-stated, and recorded FALSE where false: ctl-summong1 "cross > 0" (FALSE, not re-scored; the supplementary ctl-summong1x is AS PREDICTED); L08-1 per-cell (FALSE, KP-415; fidelity carried by the replay and the immune limb); the first CGD arms INVALID (trace gap, KP-416) and superseded by the all-stream re-run |
| **My earlier conditions** | b.wave == fight.wave: `identity.mismatch_b_wave_vs_fight_wave = 0`, `missing = 0` in the P4b and L01 cells I read. Replay gates graded (INFO-2 of `e676a2058`). `_typeb_for` calls `super(pack)` first. INFO-V3-3 is **moot on the port**: no port code reads `offense_da_population.json`. The windowed `.app` self-test at X, which KP-360 required, ran before the digest moved (`a16b0ab`, 85/85) |

## Notes

**INFO-1 · The hunk audit FAILs under its default invocation.** Without `--config`, `ADJ_J3 = {}` and the audit reports `VIOLATION ADJ-J3 S-1/s1a: anchor not declared`, then FAIL. The docstring says "the build's own config is the default". Make the build config the actual default, or correct the docstring, so a later reviewer doesn't take a correct tree for a broken one. **Cite:** #75.

**INFO-2 · The fail-first evidence was committed 23 s after `f414985` (`274b9c7`).** Validity rests on the variant tags in the provenance, which is sound. For future runs, record wall-clock run times in the provenance. **Cite:** #7.

**INFO-3 · `attributions/S-11.md` understates its own evidence.** Its closing note says `n_typea_fired = 0`. That is true for M0 and M-POL-2-NULL only. In the L01-P provenance, M-POL-2, W1 and W1-NULL fire Type-A **10× per cell (15/25 cells)** under 30/25/11 and are 7/7 bit-equal. So S-11a's tick counts *are* exercised at bit level. Correct the note.

**INFO-4 · The pre-pass offset is recorded, not asserted.** `prepass_offset` appears in each crit-stream record, but `whole − window == prepass_offset` is not checked (my INFO-4, `e676a2058`). It is low-stakes, because `served == recorded` and the grains are 7/7.

**INFO-5 · The port-controls record is still titled "RESULTS-PARTIAL … not a verdict"** although it now carries the complete record. Retitle it, or add a final verdict header. **Cite:** #73. Also: NC-J3-L03-1's death limb is exercised in **1/25** cells. It is as predicted, but thin.

**INFO-6 · drax used `rm -f` once,** on his own zero-byte STOP file outside the repo (`runner-stopfix/RESULTS.md`, AGENT_STATE). It breaks the no-`rm` convention. It was disclosed, and the practice is corrected (`mv` to `.cleared`). No impact on evidence. The conductor should note it on the ledger.

## Verdict

**PASS-WITH-NOTES.** KP-312 condition 4 is met for runtime `a0e75469`. Work may depend on the digest, subject to Matt's windowed self-test. The INFO items are non-blocking.

## Action
- [ ] drax: INFO-1, INFO-3, INFO-4, INFO-5 (doc and instrument hygiene).
- [ ] Conductor: INFO-6 on the ledger.
- [ ] Matt: the windowed `.app` self-test at `a0e75469` (built; `app-d419666/SUMMARY.json`: probe 309, attempt-2 54/0, 16/16 negative controls RED).

## References
- godot `f414985`, `d419666`, `326ea99`, `d27e629`, `274b9c7`, `0591b86`, `6b31769`, `f2432d4`, `755d30a`, `5f71898`, `5d03478`
- `evidence/join1/j3c-hook/`: `failfirst`, `s12-failfirst`, `proofs-d419666`, `l01-d419666`, `port-controls-d419666` (incl. `crit-allstream`), `attributions`, `app-d419666`, `emitter-reproof-f2432d4`, `runner-stopfix`, `DIGEST-BRIDGE.json`
- `evidence/kc2-play/2026-10-13-ta-preread-j3c-s12-a0e75469-cells`, `…/2026-10-07-ta-preread-kp310-472cffc4-cells`, `…/2026-10-07-g3-25cell-kp310-V311FULL-256b3e4`
- Ledger rows KP-333/360/363/395/397/402/406/408/412/415/416
