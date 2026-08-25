# KR finding — **the E-1 gate scores the control mode its own harness comment names as the defect. The cleanup I was queued to perform would have destroyed the evidence for it.**

**By:** knight-rider, 2026-08-25
**Occasioned by:** disposing of drax stage-4 routed finding **#5** — *"`run_s2b_e1.sh` delivered 20 superseded `_fxoff_` frames into the E-1 corpus"* — which sat in the remaining-to-seal table (`dispatches/2026-08-24-drax-s2b-rows-redispatch.md:1337`) as a **knight-rider cleanup item.**
**Status:** ~~measurement dispatched to drax (Pattern A, pre-registration before re-run). **No verdict retired or moved on this finding yet.**~~ → **MEASURED AND CONFIRMED, 2026-08-25** (drax `0c38b79` prereg → `0d26021` result). **Branch A fired: arena `00-pre` 83 → 0, cathedral 265 → 0, `PASS_exactly_zero` false → true on both.** The open "control not pose-matched" defect is **RETIRED**. **See § 8, which also records the two consequences NOBODY pre-registered — one of them larger than the finding.** Original text below is preserved unedited per #79 cl. 5.
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

---

# § 8 — MEASURED. Confirmed on the pre-registered branch, and the two largest consequences were not on anyone's list.

**Appended 2026-08-25 after drax's return. Every figure below I re-read out of `gate.json` and `s2b_e1_gate.py` myself; none is taken from his summary — which is the discipline that produced §§ 1–7 and would be hollow to abandon at the payoff.**

## 8.1 The primary reading

| | before | after | pre-registered branch |
|---|---:|---:|---|
| arena `00-pre` | 83 | **0** | **A — CONFIRMED** |
| cathedral `00-pre` | 265 | **0** | **A — CONFIRMED** |
| `PASS_exactly_zero` | false | **true** | both stages |

**The "wwcr novfx control is not pose-matched before T_BEGIN" defect is RETIRED.** It was an `--fx=off` property attributed to `novfx` by a gate that named one arm and read the other. § 4's prediction — that the anomaly carried the broken mode's own signature — held: drax's localiser puts the 83 px on a **201×208 mixed-sign residual on the caster**, which is a real pose mismatch, on an arm that renders no whirlwind at all.

**This finding retired an open defect rather than adding one.** § 4 said explicitly that I was not asserting that, and that it was measured or it was nothing. It measured.

## 8.2 ⚑ The consequence I missed, and it is bigger than the one I found

§ 3 listed four consumption sites and I put determinism first. **I described site 1 as "drives `determinism` and `geometry_lit`" and did not notice what that second word costs** — `geometry_lit` takes the control as its **second operand**, so a wrong control does not merely mis-score a comparison, it **inflates the numerator of every ratio built on it.**

| | before | after | move |
|---|---:|---:|---|
| arena `authored_px` | 6,452 | **1,869** | **3.5×** |
| cathedral `authored_px` | 5,773 | **1,842** | **3.1×** |
| arena `GLF` | 0.8345 | 0.8229 | small |
| cathedral `GLF` | 0.7116 | **0.5733** | **large** |
| cathedral `mean_added_luma_on_structure` | −0.10 | **+57.04** | sign and magnitude |

**The caster's own body was being counted as authored effect pixels**, and cathedral's near-zero added-luma was a silhouette averaging against itself. **A reading of −0.10 that looks like a clean null was the most corrupted number in the receipt.**

**This is mine to carry, in two ways.** First, the miss: I had the site in my own table and stopped one step short of asking what the operand *was*. Second, the repair: **the published E-0 GLF table in `dispatches/2026-08-24-drax-s2b-mint-tranche-2.md` § E-0 is MY file**, its whirlwind row was computed against the superseded control, and I have struck-and-corrected it in place rather than overwriting it (#79 cl. 5). GLF carries no threshold, so **no verdict flips**; the other three rows are byte-identical.

## 8.3 The `post` mark — a second reason-on-record that does not reproduce

The `ROWS` header's stated reason for leaving ww's `post` unscored is a **neutral never-tinted scuff layer persisting through `09-off`, cited at 3,973 px.** Against the rendered control, `09-off` **diffs to exactly 0 on both stages.** The reason does not reproduce; it was a property of the superseded arm too.

**drax did not switch `post` on.** His words: turning an N/A into a PASS **moves favourably and was not pre-registered.** He reported it, flagged it in the receipt's own note, and left it for its own registration. **That is the correct call and I am ratifying it rather than collecting the free green** — a verdict improvement discovered mid-run is exactly the thing #80 exists to make you pay for in advance.

## 8.4 ⚑ The conduct finding — his own falsifier convicted him, and it is the most instructive line in the return

drax pre-registered **(a) "I predict C-3 spread DECREASES"**, with the falsifier *"if spread is UNCHANGED, they contributed nothing."*

**Measured: ww `n` 30 → 20; spread `0.8716 → 0.8716` and `2.4192 → 2.4192`. Unmoved to the digit.** The falsifier fired against its author. `std` fell only from dropping ten in-range samples.

**His own sentence is the finding:** *"Had I measured first, 'spread fell, because std fell' is a sentence I could have written without noticing."* **A true sentence, about a real number, that would have been a false explanation** — and nothing downstream would have caught it, because nothing downstream reads `std`'s provenance. **Pre-registration did not merely discipline the claim; it was the only instrument in the run capable of detecting that particular error.** I offer this to jack-ryan as the cleanest live instance of #80 cl. 2 available, found by a developer against himself.

## 8.5 The frames — disposition executed, and better than I specified

I instructed **MOVE or EXCLUDE BY PATTERN, never delete.** He excluded by pattern **and emitted the exclusion into `gate.json` as `superseded_excluded`, carrying the pattern, both pool counts, and all twenty filenames.** Verified present; **40 `_fxoff_` and 40 `_fxctl_` PNGs still on disk across the corpus, nothing moved, nothing deleted.**

**That is strictly better than moving them.** A moved file is silent about why it moved; **an exclusion that publishes its own membership list is a receipt that cannot drift from the directory it describes.** The next reader does not have to reconstruct this ruling to know what was dropped.

**And § 5 is now demonstrated rather than predicted.** The re-run cost **zero renders** — both arms were on disk. The evidence and the defect being the same 20 files is not a hazard I argued for; it is the reason this finding was recoverable at all, and the reason confirming it was free. **That is a concrete input to Matt's open frame-retention fork** (`canonical/matt_decision_needed/2026-08-24-vfx-frame-retention-vs-synty-licence.md`): a retention policy that had discarded this corpus would have made the defect permanent AND the confirmation expensive.

## 8.6 § 4's secondary item, closed — and I checked it the hard way

The cathedral note is no longer a copy of arena's. **Both stages now emit identical note text, which by itself proves nothing — an identical output is exactly what a re-introduced copy would look like when both residuals are zero.** So I read the code: `s2b_e1_gate.py:312-318` builds `note` from the stage-independent `why`, then appends `PRE_RESIDUAL_NOTE` **only when that stage's own `pre` mark measures a non-zero residual**, formatted with that stage's number. **Derived, not copied. The receipt could not have told me; the source could.**

*Appended by knight-rider, 2026-08-25, from `gate.json` (`rows.ww.{arena,cathedral}.{determinism,geometry_lit}`, `stages.*.superseded_excluded`), `s2b_e1_gate.py:127-151/244-257/307-324`, `git log` on `reincarnated-godot` (`0c38b79` prereg strictly precedes `0d26021` result), and a live file-count of the corpus. **`reincarnated-godot` is unpushed and outside the standing push pattern — that ask is owed to Matt and is not taken here.***
