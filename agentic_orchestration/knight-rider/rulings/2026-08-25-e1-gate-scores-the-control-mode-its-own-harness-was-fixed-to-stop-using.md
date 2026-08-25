# KR finding — **the E-1 gate scores the control mode its own harness comment names as the defect. The cleanup I was queued to perform would have destroyed the evidence for it.**

**By:** knight-rider, 2026-08-25
**Occasioned by:** disposing of drax stage-4 routed finding **#5** — *"`run_s2b_e1.sh` delivered 20 superseded `_fxoff_` frames into the E-1 corpus"* — which sat in the remaining-to-seal table (`dispatches/2026-08-24-drax-s2b-rows-redispatch.md:1337`) as a **knight-rider cleanup item.**
**Status:** measurement dispatched to drax (Pattern A, pre-registration before re-run). **No verdict retired or moved on this finding yet.**
**Everything below is derived from source and receipts. Nothing is taken from an agent summary, including drax's — his assessment of this item is the thing that turned out not to hold.**

---

## 1. What I was about to do, and why it was the wrong move

drax routed item #5 with the assessment: **"No scored artifact consumed them (the gates read `_fxctl_`)."** On that basis the item was housekeeping — delete 20 stale PNGs from `harness_logs/s2b_e1_2026-08-24/` so a later reader does not mistake them for the E-1 record.

**I checked the premise instead of inheriting it. It does not hold, and the direction of the error is the opposite of the one the cleanup assumed.**

## 2. The chain, three files, each read at source

| # | evidence | what it establishes |
|---|---|---|
| 1 | `scripts/wwcr_stage.gd:521` — `var tagname := ("fxon" if _fx_mode == "on" else ("fxoff" if _fx_mode == "off" else "fxctl"))` | `--fx=off` → `_fxoff_`; `--fx=novfx` → `_fxctl_` |
| 2 | `scripts/run_s2b_e1.sh:83` renders the ww control as `--fx=novfx` → `_fxctl_`. Its own comment (76–81) names `--fx=off` as the defective first pass: *"does not build the whirlwind AT ALL… measures the CASTER'S ROTATION, not the effect, and its determinism receipt duly came back **00-pre=88 / 09-off=3939** instead of 0/0."* | the harness **abandoned** `off` and says why |
| 3 | `scripts/s2b_e1_gate.py:186` — `ctp = f"e1_{st}_{row}_ctl" + ("_fxoff" if row == "ww" else "")` | **the gate reads `_fxoff_` by name. `_fxctl_` is never read by name anywhere in that file.** |

**Conclusion: the E-1 gate's `ww` control arm is the "no whirlwind at all" pass the harness was fixed to stop producing.** The correct `_fxctl_` frames were rendered and then never read as the control.

**It only worked because the stale files were still on disk.** `arm_files()` globs the prefix; had the directory been clean, the gate would have emitted `{"ERROR": "missing arms"}` at `:189`.

## 3. Four consumption sites, against a claim that there were none

1. **The ww control arm itself** (`:186`) — exclusively `_fxoff_`. Drives `determinism` and `geometry_lit` for the row.
2. **C-3 uniformity** (`:132`) globs `e1_{st}_*.png`; `per_row.ww` reads **`n: 30`** = 10 `fxon` + 10 `fxctl` + 10 `fxoff`. **One third of the ww uniformity pool is superseded frames.**
3. **Register metrics** (`:157`) glob `e1_{st}_*ctl*.png`, which matches **both** `ww_ctl_fxctl` and `ww_ctl_fxoff` — so `structured_pct`, `HLF_pct_control_mean` and `SHF_pct_control_mean` pool the current and the superseded control together.
4. **`n_arms_sampled`** (`vals.size`) counts every PNG in the stage, superseded included.

**Corroboration that these are leftovers and not a second intended arm:** `render.txt` for that corpus contains **20 `fxctl` and 20 `fxon` references and zero `fxoff`.** The render log of record does not account for the files its own directory contains — precisely the *"stale PNG from a previous build under the correct filename"* failure drax identified and **fixed in `run_wwcr_stage.sh`** in the same return. He found the mechanism and fixed the cause; the sibling corpus is where it had already landed.

## 4. ⚑ The receipt carries the broken mode's own signature — which is why I think this is real and not a naming coincidence

`gate.json` → `rows.ww.arena.determinism`: **`00-pre: 83`, `PASS_exactly_zero: false`**. Cathedral: **265**.

**The harness comment predicts the broken `off` mode returns 88 at `00-pre`. The receipt of record reads 83.**

And the attached note says:

> *"⚑ AND `00-pre` DOES NOT REACH ZERO EITHER (83 px…) — **the wwcr novfx control is not pose-matched before T_BEGIN.** That is a REAL control defect in the clean-room harness, reported not fixed… **SURFACED to knight-rider.**"*

**It is not the novfx control. It is the `off` control.** So a defect standing **open in our record, surfaced to me by name**, may be an artifact of reading the wrong files — in which case this finding *retires* an open defect rather than adding one.

**I am not asserting that it does.** That is a prediction, and I have banked unearned inferences five times this run. It is measured or it is nothing.

**Secondary, no re-run needed:** the `cathedral` note is a **verbatim copy of the arena note carrying arena's own 83 px figure**, while cathedral reads 265. A note quoting another stage's number is **#64 FRAME FORM** in miniature.

## 5. ⚑ The transferable part — the evidence and the defect were the same 20 files

**Had I done the cleanup as queued**, the next gate run would have emitted `missing arms`, someone would have repaired it by re-pointing or re-rendering, and **the fact that a sealed E-1 receipt scored a superseded control would have been unrecoverable.** The frames are untracked under the Synty licence rule, so this Mac's disk is the entire record — and the frame-retention question is an **open Matt decision** (`canonical/matt_decision_needed/2026-08-24-vfx-frame-retention-vs-synty-licence.md`).

**Candidate, offered to jack-ryan and not asserted as a rule:** *a cleanup item that removes an artifact a gate consumed is not hygiene — it is deletion of evidence, and the check is whether any instrument reads the path before it is removed.* The check is one `grep` of the scored directory's basename patterns against the gate sources. **The nearest existing text is #79 cl. 5 (strike, don't delete) in its documentary form; this is the same proposition about pixels.** Whether it needs a number or is already covered is his call — it may simply be **#80 cl. 1** read backwards, since both are about a region whose composition nobody printed.

**And the disposition follows from it: `_fxoff_` frames are to be MOVED or EXCLUDED BY PATTERN, never deleted.** That instruction went out with the dispatch.

## 6. What was dispatched, and what is deliberately not concluded

Pattern A to drax, 2026-08-25, sequenced as: **pre-register the predicted `00-pre` / `09-off` readings, commit and push the prediction, THEN** change `s2b_e1_gate.py:186` `"_fxoff"` → `"_fxctl"` and re-run the gate over the corpus already on disk (**zero render cost — both arms exist**). Report all four consumption sites before/after.

**#80-compliant by construction:** the gate has a demonstrated RED on this population in this configuration (83 / 265 ≠ 0), so a green after the change carries evidence. **The pre-registration explicitly names what refutes me** — a post-change reading near 83/265.

**Not concluded here:** whether the "control not pose-matched" defect dissolves, shrinks, or survives; whether any ww reading in the E-1 record materially moves; whether the tranche-2 seal is affected. **E-1 is a separate gate from tranche-2 row minting and I am not claiming otherwise until measured.**

## 7. Credits, because the conduct around this was good

- **drax found and fixed the mechanism** (`run_wwcr_stage.sh` now wipes `$USERDIR` and asserts frame count) and **flagged the sibling corpus unprompted.** The defect here is one sentence of assessment attached to a finding he did not have to file at all.
- **The gate's own note surfaced the anomaly to me by name** and refused to report a false negative — `det["PASS_exactly_zero"] = "N/A — no effect-off mark exists"` where no mark exists, rather than `false`. **The instrument was honest about a reading taken from the wrong files.** That is #63(c) complied with, and it is the reason the anomaly was visible at all.

*Filed by knight-rider, 2026-08-25. Source reads: `wwcr_stage.gd:521`, `run_s2b_e1.sh:76-83`, `s2b_e1_gate.py:132/157/186/189`, `harness_logs/s2b_e1_2026-08-24/{gate.json,render.txt}` and a file-count of the corpus directory (152 PNG · 20 `_fxoff_` · 20 `_fxctl_` · 20 `_fxon_`).*
