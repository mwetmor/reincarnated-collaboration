# drax's 3A recapture — **he returned without a result, the capture is STILL RUNNING, and the instruction I gave him would have destroyed the evidence**

**Filed:** 2026-08-25 (knight-rider), on his return.
**Status of the experiment: LIVE AND UNATTENDED at time of writing.** Verified by process, not by report.

---

## ⚑ 0. The capture did not finish with his session. It is running right now.

His closing line was ***"Post-chain is ready and syntax-checked. Waiting for the capture to finish."*** — **an honest return with no number in it.** The harness ended his session; the work did not end with it.

I checked the host rather than inferring, and the experiment is alive:

```
Godot  98.3% CPU  --out=user://s2c12v3/ --prefix=clip_da_arena   ← 4th pass, in flight
bash /tmp/s2c_recapture_all.sh                                    ← orchestrator alive
tail -f /tmp/s2c_recapture_logs/orchestrator.log
```

`s2c38v3` and `s2c38v3b` already exist; `s2c12v3` is being written; `s2c12v3b` does not exist yet. **Four passes, three to go or in progress.**

⚑ **This is the good version of a failure mode that has bitten this session twice.** Earlier, an agent reported `completed` **while having died** — status field lying about an error. Here the status field says `completed` and the agent is being *truthful*: **it finished its turn; the thing it was waiting on did not finish.** Same word, opposite meanings, and **only reading the host distinguishes them.** A dispatch is not complete because its agent returned.

**I have attached a sentinel watch** (`until [ -f …/COMPLETE ] || [ -f …/FAILED ]`) so the completion is not missed. **The post-chain — `s2c_prepost_compare.py`, written and syntax-checked by drax — has no one assigned to run it.** That is the single most important open thread in this workstream: **the experiment will produce frames that nobody analyses unless a drax session is dispatched to consume them.**

## ⚑ 1. The instruction I gave him would have destroyed the sealed verdict's evidence base

My dispatch's § 1 told him to capture under a **fresh suffix** so pre-fix directories were untouched. **That is correct and executable in `run_s2c_rows38.sh`. It is NOT executable in `run_s2c_rows12.sh`, and following it there would have wiped the evidence.**

His measurement of the sibling script:

- `USERDIR` **hardcoded** to `s2c12`
- `--out=user://s2c12/` **baked into all 24 arm invocations**
- `SUFFIX` read, but reaching **only `$OUT`**
- an **unconditional** `rm -f "$USERDIR"/*.png`

> **Every invocation, with any argument, wipes `s2c12`.**

**`s2c12` is the pre-fix capture of `dash_attack` + `blink` — the exact pair the sealed L-29(6) adjudication rests on.** The dispatch line that was supposed to *protect* the evidence was, in that script, **the command that deletes it.** He caught it because he resolved the paths **by running the real scripts and printing what they resolved to**, rather than reading the parameterisation and believing it.

**His own account of the cause, which is the part worth keeping:** *"This is the same defect I removed from the rows-3-8 runner at `a5779c8`. **I fixed the runner that had bitten me and did not sweep its sibling.**"* A defect class fixed at one instance and left standing at every other instance of the same shape — **the fix was applied where the pain was felt, not where the defect lived.**

**Guards he took before anything ran:** all five pre-fix directories `chmod a-w`; all four resolved `USERDIR` values printed **by the real scripts** (`s2c12v3`, `s2c12v3b`, `s2c38v3`, `s2c38v3b`), **each verified unequal to a pre-fix path**; frame counts re-verified intact afterward.

## 2. He corrected my § 4 evidence claim, and it convicts me under a clause I had just been ruled against

I wrote that `s2c38` / `s2c38b` / `s2c12` were the **sole surviving** pre-fix frame sets because *"the `harness_logs` duplicates were deleted in the disk crisis."* **Measured: false for rows 1–2.** `s2c_rows12_2026-08-25` and `…-25b` each hold **874 PNGs, sampled md5 agreeing with the userdir copy.** The rows-1-2 evidence is **triplicated.**

⚑ **`#79` cl. 1 — a number is DERIVED at the moment of writing — convicts me for the second time in one session, and I wrote this one AFTER jack-ryan had already ruled against me under it.** It errs safe (over-caution about evidence) and it was still an unmeasured assertion stated as measurement, sitting in an operative dispatch. **Corrected at the source**, not in a note.

And the reason the triplicate existed at all is the sharpest line in his return: ***"protected by a bug, not by a decision"*** — it survived because of the disk-filling `cp` that the rows-3-8 fix removed **at its cause**. Which is why he fixed the runner rather than recording the redundancy: **evidence that survives by accident is not preserved, it is merely not yet lost.**

## 3. He ruled § 3.1 himself: **TWO passes, not one** — and the reasoning is transferable

Under § 2.2's F-9, a before/after delta is a **FAIL-direction claim** — an assertion that two captures *differ* — **the noise-exposed direction.**

> The sealed determinism receipt proves the **old** harness was deterministic. **Commit A changed render output by design.** So that property **does not transfer.** Without a post-fix same-code repeat, *"the fix moved the number"* cannot be separated from *"the new code has a flake floor."*

**This is a seam-owner decision taken inside his own authority and it is correct.** It is also the same shape as `#75` cl. 6 arriving from the other side: **a receipt does not transfer across a change to the thing it certifies.** The determinism proof was true of a harness that no longer exists.

**§ 8 refutation condition 1 he tested rather than assumed** — arm invocation strings normalised for userdir name; **rows 1–2 shows zero arms in post absent from pre.** Matched-pair premise holds so far.

## ⚑ 4. The reconciliation this return does NOT resolve — and must not be dropped

**jack-ryan pre-registered a falsifier against this exact run, while it was executing, and drax does not know it exists** (blinded, which is ideal; `SendMessage` unavailable, so it could not have been relayed even to request output shape).

> **Prediction:** deltas **large on Mob0/1/2, near-zero on Mob3** · `step_concentration` gaps **« 0.2069** · verdict direction unchanged.
> **Falsifier:** *"If Mob3 moves materially, my trace is wrong and the seal reverts to PROVISIONAL."*

**The post-chain must emit a PER-MOB breakdown or the prediction is untestable against it.** `s2c_prepost_compare.py` was authored before jack-ryan ruled, so there is no reason to expect it does. **If the breakdown is absent, it is a re-analysis over preserved frames — not a re-capture — and it is cheap.** Dropping it silently would be the mooted-escalation failure this project has already ruled on once.

## What landed from his session

`713f487..0800f32` in `reincarnated-godot` (pushed), plus `8866b77a` in the meta-repo. Owed item 1 discharged at `713f487`; item 2 (P-BEAM control-arm-zero) **retired in place with the strike visible** rather than deleted.

**Paths:** `scripts/run_s2c_rows12.sh` (the fix) · `scripts/s2c_prepost_compare.py` (the unrun post-chain) · `scripts/s2c_pair1_reproduction.py` · `agentic_orchestration/drax/notes/2026-08-24-s2b-mint-note.md`

---

# ⚑ SECOND RETURN — the numbers landed, and **one limb of jack-ryan's pre-registered prediction looks refuted**

**Appended 2026-08-25 (knight-rider), same task, on drax's second return.** § 0 above is now partly stale: **rows 1–2 are FINAL.** Rows 3–8 (R-5 fold test, R-3 corridor, R-7 shuriken) are **still rendering, ~45 min.**

## The measurement — rows 1–2, 874/874 frames, 54/54 arms matched

**Byte-identity:** 874 co-named frames, **0 identical, 874 differing.** **Outcome 0 is refuted — the fix reached these rows.**

**Class gap on `SC(added-luma)`, the sealed instrument, computed within each corpus:**

| cell | pre-fix | post-fix | Δ | rel | sign |
|---|---|---|---|---|---|
| arena | +0.2653 | +0.4955 | +0.2302 | +86.7% | preserved |
| cathedral | +0.2069 | +0.3807 | +0.1738 | +84.0% | preserved |
| **pooled** | **+0.2069** | **+0.3807** | **+0.1738** | **+84.0%** | **preserved** |
| worst_stage_swing | +0.1576 | +0.1590 | +0.0013 | +0.9% | — |

**Pre-registered outcome 2: gap survives, same sign, margin moves materially.** drax attached no disposition — *"it is jack-ryan's"* — which is exactly right and is the second time this session he has declined to rule something outside his authority.

⚑ **The gap WIDENED. It did not shrink.** So **the defect was SUPPRESSING the distinction, not manufacturing it.** That direction matters more than the magnitude: the pessimistic reading everyone was braced for — *"the class gap was an artefact of a broken capture path"* — is the one outcome the data rules out.

## ⚑ The tension with jack-ryan's falsifier, and I am NOT ruling it

He predicted three things. **Scored honestly:**

| Limb | Predicted | Observed | Verdict |
|---|---|---|---|
| Verdict direction unchanged | unchanged | sign preserved in **every** cell | ✅ **HOLDS** |
| `step_concentration` gaps move **« 0.2069** | much less than the gap | **+0.1738 — ~84% of it, same order of magnitude** | ⚑ **PRIMA FACIE FAILURE** |
| Deltas **large on Mob0/1/2, near-zero on Mob3** | Mob3 is the control | **NO PER-MOB NUMBER EXISTS** | **UNTESTED — and it is the decisive one** |

His ground was that the yaw defect is a **pure sink** with one bounded on-path residual — caster-silhouette occlusion at **tens of pixels against a ~1,520 px disc**. **A residual of that size does not obviously produce an 84% shift.**

**The confound that may fully explain it, raised because it is his to adjudicate and not mine:** drax's own § 3.1 notes **Commit A changed render output BY DESIGN**, not solely via the yaw fix. If so, this delta conflates repair with intended change and says nothing about the trace. ⚑ **But that argument has to be DERIVED, not asserted** — it is convenient for the person making it, which is precisely when `#75` cl. 2 bites. **Routed to jack-ryan with the confound named and explicitly not granted.**

## Two further measured results, both of which cut in favour of prior rulings

**1. He built a control arm for his own tool change** — the move most agents skip. Run **without `--cap`**, the script reproduces the pre-fix artifact **exactly**: 8/8 figures, per-frame re-derivation delta **`0.000e+00`**, JSON identical after stripping two additive keys. **So the post-fix `False (0/8)` is a property of the CORPUS, not of his edit.** He tested whether his instrument had moved before reporting what it measured — `#75` cl. 6 discharged without being told to.

**2. ⚑ The REJECTED instrument would have given the opposite answer.** `SC(coverage)` — which R-1.1 explicitly rejected as worse — **inverts sign** on cathedral (−0.1313 → +0.0500) and its pooled figure **collapses to −0.0013**, while the ruled instrument `SC(added-luma)` holds sign in every cell.

**The rejected instrument is the pose-fragile one; the ruled instrument is the robust one — measured, not argued.** R-1.1's floor was chosen before anyone knew this, and it is now vindicated by the one experiment capable of vindicating it. It is also a live demonstration that **instrument choice determines whether a repaired defect reaches a verdict** — which is `#75` cl. 7's exposure test in miniature. Flagged to jack-ryan as a possible founding instance; **his call, not mine.**

## Open

- **Per-mob breakdown** — required by `dispatches/2026-08-25-drax-consume-the-3a-recapture-…md` § 2. **Without it the decisive limb of the pre-registration cannot be scored**, and it is a re-analysis over frames already captured, not a re-capture.
- **Rows 3–8**, ~45 min, with the full gate diff.
- **jack-ryan's disposition** on the second limb, and on whether the seal's status changes now or waits.

---

## ⚑ CORRECTION TO § 0 ABOVE, AND THE RESOURCE PROJECTION, BOTH MEASURED

**§ 0 says *"`s2c38v3` and `s2c38v3b` already exist."* That is true and it is MISLEADING, which is worse.** They exist as **EMPTY DIRECTORIES — 0 PNGs each.** They were created ahead of the passes that fill them. My sentence invites the reading *"those two passes are done,"* and **they have not started.**

⚑ **Fourth instance this session of my one recurring defect: inferring an artifact's state from its listing instead of opening it.** The HITL arm, the deletion claim, the receipt, and now this — **and this one I wrote into a committed record while writing up the previous three.** The log settles it in one read:

```
--- rows12_v3  start 22:13:14Z ---
--- rows12_v3  rc=0 elapsed=505s 22:21:39Z ---
--- rows12_v3b start 22:21:39Z ---          ← current
```

**Actual order is rows12 FIRST, then rows38.** Only `orchestrator.log`, `rows12_v3.log`, `rows12_v3b.log` exist. **Rows 3–8 have not begun.**

### Pre-fire resource projection — discharged here so the next session does not re-derive it

**Measured, not assumed:** `s2c12v3` = 874 frames = **1.7 GB → 1.99 MB/frame.**

| Remaining | Frames | Projected |
|---|---|---|
| `rows12_v3b` (496/874 done) | 378 | **0.74 GB** |
| `rows38_v3` | 2,106 | **4.10 GB** |
| `rows38_v3b` | 2,106 | **4.10 GB** |
| **TOTAL** | | **8.93 GB** |

**Free on `/System/Volumes/Data`: 55 GB. Margin: 46 GB — 6.2× headroom. ✅ PROJECTION PASSES.**

⚑ **This matters because the tranche has HALTED TWICE on host resources** — free space was **2.7 GB** at HALT #2, and a `matt_to_do` red-disk warning predicted that failure by name a day before it happened and was not read. **There is no HALT #3 coming from disk.** The check cost one command; the two prior halts cost a tranche each.

**Timing, from the same measurement:** 505 s for 874 frames → **20.3 min per rows38 pass, ~44 min total.** **drax's "~45 min" is accurate to within a minute** — recorded because an estimate that survives independent derivation is worth more than one that is merely repeated.
