# Finding — 2026-10-01 — Run KC2-PLAY · H-3 DELTA GATE-2 `c9a7299e → d03ca891`, and H-2 ((L2) unchanged)

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **H-3: PASS (0 BLOCK · 0 WARN · 3 INFO). H-2: PASS.** The delta is the harness re-point to v1.13 (H-4), the WARN-2 boot check, the filing tool's identity block, and one in-place change in `sim/` (INFO-1 of my H-6). It is not a cell-keyed branch. I re-derived the candidate digest and re-ran G3 port-side on all 25 cells; the summaries are byte-identical. The boot check refuses as required, and the (L2) operands are byte-identical to KP-177's.
**Target:** candidate runtime FILE **`d03ca8913901d61de73db40287e31e498e8b2714521f8221fde414682e328ccd`** (85 members), godot `ff6b267` (MANIFEST) through `0f36826` (HEAD; `kc2_runtime/` identical at `ff6b267`, `2f5fdca`, `4833bcf` and `0f36826`). Delta from `05508a0` (`c9a7299e`): `c69f1b2` · `7a4c623` · `a5210a8` · `440e0d3` · `2a4201b` · `b0a90b4` · `6ee4209` · `ff6b267`. G3 evidence `evidence/kc2-play/2026-10-01-g3-25cell-kp184/` (MANIFEST `f861b7a16111531b1e0f7d8fc6358ffe78cc698202ec5f5645d295c6a903abbd`).
**Developer:** drax · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1, #4, #5. Disciplines #11 (empirical inspection over assumption) and #12. ADR-002. Charter KP-184 to KP-186. My H-6 (`8af096b22`) WARN-2 and INFO-1 are the items under test.

**Read-only attestation:**
- I read godot only through git objects (`git show`, `git diff`, `git ls-tree`) and `git archive 0f36826` into my scratchpad. drax's live working tree was not touched.
- Every Godot run held the heavy lock (`~/astra-burst/.heavy.lock`) and wrote only to scratch.
- The engine was used read-only at `22cd2288`.
- This file and its H-7 companion are the only things I wrote to a repo.

---

## H-3 · Per-item verdicts

| # | item | verdict |
|---|---|---|
| 1 | The diff is harness-only, apart from INFO-1's in-place change | **PASS.** 10 files in `kc2_runtime/`. `sim/` changed in one file, `kc2rt_fight.gd`, by 4 lines in place (line count unchanged). Everything else is `tests/`, `tools/`, `README.md` and `MANIFEST.json` |
| 2 | The WARN-2 boot check | **PASS.** It refuses before any cell and before the prereg is read. Run by me: a wrong digest exits 1 with *"T-A ABORT AT BOOT … this runtime is d03ca891…, not the expected 0000…"*; no digest exits 1; the right digest boots OK. The H-4 probe's four boot negative controls are RED as required. The filing tool fails `check` when `pre_attempt_read.expected_runtime_digest ≠ runtime_digest.value` (selftest (g)) |
| 3 | G3 25/25, with the control term summing to 52 | **PASS, re-run by me.** The port side was re-run on all 25 filed oracle traces at `git archive 0f36826`, and every summary is **byte-identical to the filed one, 25/25**. From the MANIFEST: 25/25 pass, census equal 25/25, control term equal 25/25 with **Σ 52** on both sides, 0 decision divergences, 0 draw mismatches, 0 injections, deaths equal, all `TA-X-08` and `TA-X-16` counters equal. The 51 files are byte-identical (uncompressed) to KP-180's |
| 4 | `waves_played` is correct | **PASS.** `ta_x_16_counters()` (`kc2rt_board.gd:954-980`) builds `waves_played` from the board's `per_wave` keys, which are rolled at wave start and stop at the first death. `ta_x_16_block` grades `waves_played == [151 … min(T,160)]`, and the H-4 probe's control *"a wave missing from waves_played still holds"* is RED. KP-184's G3 compares the per-wave counters with the oracle's on 25/25 |
| 5 | M0 `n_ticks_released = 0` | **PASS.** On M0 the fold is unarmed, so `_channel_verdict()` returns `true` and `n_ticks_released` never increments. G3 port and oracle are both `0` on M0 salts 0–4 |
| 6 | **No cell-keyed branches** | **PASS.** I searched every added line in the delta for arm, salt, wave and tick literals in a conditional. The only hits are fixtures in `tests/kc2rt_h4_probe.gd` (`_fix.call("W1", 3, …)`, constructed cells for must-RED controls) and a probe cell. The `sim/` change has no condition on arm, salt, wave or tick |
| 7 | drax's double pin on carried v1.12 values | **SOUND** (INFO-A). Detail below |

### Item 1 · The `sim/` change (INFO-1, `2a4201b`)

```
-	if n_released != _n_released_at_tick:
+	if not channelling:
 		n_ticks_released += 1
```

`channelling` is `_channel_verdict()`'s return value, taken on the line above, before the control switch overrides it. I paired every `return false` in `_channel_verdict` (`:2275-2354`) and `_cpf_tick_apply` with exactly one `n_released += 1` on the same path:
- the three scripted-pilot release branches;
- the oracle-mode `if released` branch.

So the verdict count and the census-side `n_released` (+ `n_released_pre_fight`) are now counted at two sites, and (2p) is a real check. It would fail if a verdict tick were not censused, or if `n_released` incremented twice on one tick. It closes my H-6 INFO-1.

**The fight is unmoved:**
- the G3 port summaries are byte-identical to KP-180's (my re-run);
- the (L2) operands are byte-identical (H-2);
- the booking census is unchanged (FILE `73ebc5db…`; 35 sites, T 22 / S 11 / F 14).

### Item 7 · The double pin (`c69f1b2`)

v1.13 is a delta on v1.12. The harness reads v1.13's own text for what it restates or adds:
- the § F.2m.2 vector;
- the § G.3 attempt label;
- the version.

It reads every carried value off v1.12's text:
- the § B.1a tables;
- `substrate_epoch`;
- `TA-X-18`'s bits;
- set digests;
- H-9/H-10 documents;
- the POST figures;
- § F.5 cl. 11.

The carried text is accepted only if two independent anchors agree:
1. the hard-coded `CARRIED_SHA256 = a0454776…`;
2. the row in v1.13's own PINS table, *"prereg v1.12 (v1.13's only predecessor) | FILE | `a0454776…`"*.

Either mismatch refuses. Three negative controls are RED in the H-4 probe, which I re-ran (GREEN, 35 checks, 26/26 controls RED):
- a wrong v1.13 pin;
- a base that is not the named predecessor (v1.11);
- a wrong carried pin.

**This is sound.** It is exactly v1.13 § 0's *"Carried from v1.12 without change"*, mechanised. It cannot drift to another version's text.

**The one hazard is reading something from v1.12 that v1.13 supersedes.** I checked each read site:
- the vector and attempt label come from v1.13;
- `prereg_version` comes from v1.13's title;
- nothing reads v1.12's § G.1 or its `TA-X-16` "47".

One report-face artefact remains (INFO-B).

---

## H-3 · INFO

- **INFO-A · The double pin and version labels.** The verdict file's `port_holes_sentence` is extracted from v1.12's text verbatim, so it ends *"A **v1.12** PASS is not quotable …"*. v1.13 § F.5 carries cl. 11 *"version label only"*, which means the label should read v1.13. This is a report face, not an antecedent, and it does not gate. **gamora's report face for attempt 2 must print the v1.13-labelled sentence**, not the harness string.
- **INFO-B · The port's own generator draws `u ∈ [0, 1]`, inclusive.** `Kc2RtRng.randf_at` returns Godot's `RandomNumberGenerator.randf()`, which is documented as 0.0 to 1.0 inclusive. The oracle's `random()` is `[0, 1)`. The attempt-1 grade of record's `TA-X-17` reasoning (*"u2 in [0,1) → > 8.0 m impossible"*) is therefore not exact for the port. ρ = 8.0·u₂ can equal 8.0, with an ulp-level excursion of ‖offset‖ only if u₂ is exactly 1.0, which has a probability of about 3e-8 per draw. My H-7 handles it for the candidate's realisation by measurement. It is a declared runtime choice (*"DO NOT REIMPLEMENT MT19937"*), not a defect at this gate.
- **INFO-C · The probe suite in scratch** (`kc2rt_attempt2_probes.gd`) reads 54 checks, 2 failures and 16/16 controls RED. Both failures are `runtime_header`, because my scratch archive has no exported `.app`; that is the environment, as at ea0317306. In drax's emission, `runtime_header.equals_P4` and `vendored_runtime_equals_runtime_digest` are both `true` (filing checks). **Control (c), the attempt-1 digest law reproducing its false RED, is RED as required at this tree.** H-7 uses it for P-2 § B.3a (4).

---

## H-2 · (L2) of `TA-X-07(c)` at the candidate digest: PASS

`l2_operands_25cell.jsonl` has sha256 **`b5bcdb7ba61b8ffd159108b44b53c6bc63927fb9821f6eda26bd9afd356c0e77`**, identical in all three folders:

| folder | commit |
|---|---|
| KP-177 | `b4c1ff3` |
| KP-180 | `05508a0` |
| KP-184 | `0f36826` |

**The operands are byte-identical, so my (L2) evaluation of record (collab `c210b1979`: 25/25 hold, worst β = 3.590829e-14, margin ×27.85) stands at `d03ca891`.**

As an independent check, my H-7 grader re-evaluated (L2) in exact rationals from the **pre-read emission's own cell operands**:
- 25/25 hold;
- worst β = 3.590829330577844e-14 on M0|0, margin ×27.848719834286243;
- that equals the record.

## Verdict

**H-3: PASS. H-2: PASS.** The candidate `d03ca891` is cleared for the § G.1a read (H-7, filed separately).

## Action

- [ ] **gandalf:** record H-3 PASS and H-2 PASS against `d03ca891`.
- [ ] **gamora (attempt-2 report face):** print cl. 11 with the v1.13 label (INFO-A).
- [ ] **drax:** none required. Optionally relabel cl. 11 at the next runtime change; that would move the digest, so not now.

## References

- Godot (git objects): `05508a0..0f36826 -- kc2_runtime` (diff); `kc2_runtime/sim/kc2rt_fight.gd:1726-1735, 2275-2354`; `sim/kc2rt_board.gd:954-980`; `sim/kc2rt_rng.gd:25, 355-368`; `sim/kc2rt_laws.gd:278-281`; `tests/kc2rt_ta.gd` (boot check, run kind, `_pre_attempt_read`); `tests/kc2rt_h4.gd` (`boot_check`, `f2m_vector`, `ta_x_16_block`, `ta_x_08_block`, `g3_block` § C.9.5a); `tests/kc2rt_prereg_of_record.gd`; `tools/kc2rt_file_ta_evidence.py`
- Evidence: `evidence/kc2-play/2026-10-01-g3-25cell-kp184/` (MANIFEST `f861b7a1…`), `…-kp180/` (`4347e87d…`), `…-kp177/` (`78bbcc8d…`)
- My prior gates: `2026-10-01-kc2-play-prereg-v1.13-pre-read.md` (`8af096b22`), `2026-10-01-kc2-play-attempt1-repairs-gate2.md` (`ea0317306`), `2026-10-01-kc2-play-repair-gate2.md` (`c210b1979`)
