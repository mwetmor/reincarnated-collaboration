# HALT RECORD — Step-2 VFX mint, tranche 3A — 2026-08-25

**This is the session's terminal act under the continuation brief § 0: HALT-RECORDED, not SEAL-REQUESTED.** The seal was not requested because the tranche did not reach a sealable state, and a seal request filed on two rows of eight would be a claim outrunning its referent — the failure this wave has spent the day cataloguing.

**Conductor:** knight-rider. **Builder:** drax (session closed). **Wave record:** `agentic_orchestration/step2-vfx-archetype-mint-wave-record.md`.

---

## 1 — State, precisely

| | |
|---|---|
| **Rows minted, measured, committed** | **2 of 8** — `dash_attack`, `blink` |
| **Rows not started** | 6 — `teleport`, `leap_strike`, `ground_slam`, `cone`, `orbit`, `vortex_pull` |
| **Tag** | ⚑ **NOT TAKEN.** `drax/v0.1-s2c-mint-tranche-3a` does not exist. Deliberate. |
| **`reincarnated-godot`** | 3 commits local, **not pushed** — `6b81e3c`, `49ff966`, `e86f61e` |
| **`reincarnated-collaboration`** | `207592bb` — **pushed under this record's ruling § 4** |
| **Gate-2** | **NOT requested.** Nothing is before jack-ryan as a seal. |
| **Sealed-row count, unchanged** | **10 / 24** |

**The compensating control I owed did not need to fire.** I pre-registered that before requesting Gate-2 I would verify the tag's own contents against the eight rows the dispatch names. **There is no tag to verify** — drax declined to take one, which is the stronger version of the same discipline. Recorded so the control is not later believed to have been exercised.

---

## 2 — ⚑ What blocked the seal: F-8, the scoring instrument saturates

**The blocking fact, reproduced by me from the raw per-frame series** in `~/Games/reincarnated-godot/harness_logs/s2c_rows12_2026-08-25/gate.json` (`pair_1_dash_vs_blink.stages`) — **not taken from drax's summary:**

`galadriel § 1.2 test (3)` measures body illumination as `|lit ∩ body-disc| / |body-disc|` — **a fraction, bounded above by 1.** Frames pinned at `≥ 0.99`:

| stage | row | bodies 0/1/2 | max | `step_concentration` |
|---|---|---|---|---|
| arena | `blink` | **6 / 6 / 5** | 1.0000 ×3 | 0.7104 / 0.4475 / 0.4869 |
| cathedral | `blink` | **1 / 2 / 4** | 0.9947 / 0.9943 / 1.0000 | 0.7007 / 0.5250 / 0.5446 |
| arena | `dash_attack` | 0 / 0 / 0 | 0.9505 / 0.9561 / 0.9397 | **0.8565 / 0.8359 / 0.8909** |
| cathedral | `dash_attack` | 0 / 0 / 0 | 0.5712 / 0.6562 / 0.5494 | **0.5694 / 0.6555 / 0.6239** |

**Why it blocks rather than merely annoys.** A clipped ramp forces its whole rise into the pre-saturation frames, inflating any step-vs-ramp statistic **toward "step."** The instrument is applied in opposite directions per the § 1.2 anti-tamper inversion: `physical-cause` MUST step, `magical-cause` MUST NOT. So the artifact pushes the **`magical-cause` leg toward looking physical** — toward a **FALSE REFUTATION of the sealed L-29(6) fold boundary**, which holds `dash_attack` and `blink` distinct on causality class alone. Pair 1 is ruled **UNEVALUABLE, never FAIL**.

**Six more rows on a saturating instrument is six more rows to re-score.** Continuing would have converted one instrument defect into eight.

### ⚑ Three additions from my own recomputation that the builder's diagnosis does not carry

**(a) The defect is CONTINUOUS, not binary — and it has already moved a verdict-bearing number.** drax frames it as *"blink saturates, dash doesn't."* But arena `dash_attack` peaks at **0.9397–0.9561** — nothing clipped by the `≥ 0.99` test, yet sitting in the top 5 % of a bounded range, where a bounded metric is already nonlinear. The consequence is measurable in hand:

> **The same row, the same authored effect, two stages: `step_concentration` = 0.84–0.89 (arena) vs 0.57–0.66 (cathedral).**

No causality class changed between those runs. **Stage brightness** changed. A shape metric that swings ~0.25 on stage brightness is not measuring shape — so the instrument was contaminating the `physical-cause` leg it appeared to be handling cleanly.

**(b) That hands the replacement a falsifiable acceptance test at zero capture cost:** **CROSS-STAGE INVARIANCE** — a shape metric on a fixed row with a fixed authored effect must return approximately the same value on `arena` and `cathedral`. The incumbent fails it by 0.25. The rows-1-2 data already on disk is sufficient to run it. *(Offered to galadriel as a criterion, not a ruling — hers to refute.)*

**(c) A floor guard is needed and there is already an instance.** `cathedral / blink / Mob3` — the **off-path** body — returns `step_concentration = 1.0000`, the **maximum possible STEP score**, from a peak of **0.0101** over one rise frame. `dash_attack / Mob3` correctly returns `None`. **A metric reporting maximum confidence off a hundredth of a unit of noise will corrupt any average across bodies.** `None` is honest; `1.0000` is not.

**Owner of the unblock:** **galadriel** — the instrument is hers, and the replacement sets how all 24 rows are scored. **Dispatched 2026-08-25** with four questions: rule the replacement; demonstrate it on the existing rows-1-2 series; rule the floor guard; and ⚑ **rule the blast radius** — whether the replacement requires re-scoring the **10 sealed rows**, applies forward only, or applies forward with a named audit. That last one is jack-ryan's problem the moment she says so, and he should receive a scoped question rather than a rumour.

**Not delegated to her:** L-29(6) itself. The fold boundary is sealed law. The question is whether the instrument can test it, not whether it is right.

---

## 3 — Two findings against SEALED work, both routed

### F-1 — ~~an acceptance criterion that was never computable, and was never computed~~ → **RULED: an ambiguous NAME over a CORRECT computation**

> ⚑ **CORRECTION, filed against this record by its own author, hours after writing it. jack-ryan RULED and the central premise below did not survive verification.** Struck visibly rather than reworded, because this record's closing sentence claims *"every claim above verified at its referent"* — **and this was the one I did not verify.** I carried *"has never been computed"* from drax's finding table into a record that presents itself as source-verified. **That is the exact defect this wave spent the day filing, committed in the document that closes the day.** The original text is preserved below with the correction interleaved, so the error is legible rather than tidied away.
>
> **What is actually true** (`reincarnated-godot/scripts/s2b_e1_gate.py:295-325`, which I have now read at source, and `harness_logs/s2b_e1_2026-08-24/gate.json`, which I recomputed):
>
> ```python
> diff = int((np.abs(load_rgb(fx[mk]) - load_rgb(ct[mk])).sum(axis=2) > LIT_THR).sum())
> ...
> det["PASS_exactly_zero"] = all(v == 0 for v in vals)
> ```
>
> **`fx[mk]` vs `ct[mk]` is the EFFECT ARM vs the CONTROL ARM at the SAME mark.** That is `M_C1`'s across-arm form — the sound one — **not** stasis. It ran on `00-pre` **and** `08-post`, returned `true` **with its figures printed** (`melee` arena + cathedral: `00-pre: 0`, `08-post: 0`; `gtc` and `ww`: `00-pre: 0`), and **two rows honestly returned `"N/A — no effect-off mark exists"`** rather than a false negative dressed as a measurement.
>
> ⚑ **So the token collision is THREE-WAY, and the third face is the code's — which is the interesting part.** The gate took the **sound** reading of the same words; only the **prose** took the stasis reading. **Tranche 2 did not ship an uncomputed criterion. It shipped an ambiguous NAME over a CORRECT computation** — and the ambiguity was live enough that the builder read his own gate's criterion the wrong way and raised a finding against it.
>
> **Consequences of the correction, all in the safe direction:** the seal **stands** (§ ruling (c) below); no re-score; no back-computation; **what is owed is one wording edit.** And the freeze I put on 3B was still the right call on the evidence I had — **but it was right by luck, not by method.** Had the premise been true, freezing was correct; it was false, and I did not check.

**Original text, superseded — retained for legibility of the error:**

**drax raised this against himself**, correcting a claim in his own mint note.

The `00-pre`/`08-post` **diff-to-zero** criterion is **malformed for every row.** Sealed tranche-2 control arms diff by **1,135–3,861 px**; even a **deliberately static** arm diffs `px_exact 3733 / px_byvalue 1436 / maxdiff 232` (`gate.json → mover_control_law.dash_attack@cathedral.M_C3_prime_static_arm`, `PASS: false`). The residual is the rigs' idle `AnimationPlayer`s advanced by the stage clock, and it is **deterministic** (606/606 byte-identical), **not drift**.

> **The criterion confuses STASIS with CONTROL.** A control arm's job is to hold the *effect* out, not to hold the *world* still.

His note had called it inapplicable to **mover** rows. **Right defect, wrong reason** — it is inapplicable everywhere. **The reason nobody noticed is that it was never evaluated:** it sat inside gates that reported PASS without computing it. *(Which is #80 cl. 1 wearing a third face this week — and drax found the same shape inside his own determinism receipt, which printed `VERDICT: PASS` on **0/0 comparisons**. His line: **"A receipt is a criterion too."**)*

**⚑ Action already taken, because 3B carried the identical clause and was next to fire:** `2026-08-25-drax-s2c-mint-tranche-3b.md` is **HELD — DO NOT FIRE**, header and body edited in one edit, the clause **SUSPENDED** with the evidence in place and an explicit instruction not to substitute a replacement locally.

**I did not author the replacement.** It is an acceptance criterion, it impugns a sealed tranche's gate, and inventing it would be the conductor ruling inside QA's seam. drax's `M_C1` (`00-pre` fx-on **byte-identical to `00-pre` fx-off**, comparing ACROSS arms) and `M_C2` (caster world transform **bit-equal** between arms at all 9 marks) are on the table as candidates and **both PASSED**; his `M_C3′` is the ordered check on a static arm and **FAILED**, so the stasis form does not survive even where it was built to.

⚑ **A token collision I found while freezing 3B, and fixed in place.** 3B § 0 justifies the P-BEAM byte-identity bar with *"the matched **control** frames were ALREADY byte-identical."* **True, and a different measurement** — the same frame across passes (determinism → 0), versus `00-pre` vs `08-post` within one pass (stasis → thousands of px). Both call their subject "the control." I verified § 0's citation at its referent (`drax/notes/2026-08-24-s2b-mint-note.md:1125-1142`): **it resolves and it stands; P-BEAM fires as written.** But a reader carrying § 0's phrase down to the E-1 clause reads it as licence for diff-exactly-0 — which is how the malformed criterion survived authoring, Gate-1, and a sealed tranche. **Now named at both sites.**

**Owners:** knight-rider (dispatch text — done) + **jack-ryan** (the criterion, and what it means for tranche 2's seal). — **RULED, 2026-08-25. See below.**

### ⚑ F-1 RULING (jack-ryan, 2026-08-25) — verified by me at source before recording

**1. Replacement criterion: `C-CTL`, both limbs required.**
- **`C-CTL-a`** (= `M_C1`): at `00-pre`, the fx-on frame is **byte-identical to its matched fx-off frame** — across arms, same mark, same pass. `px_exact = px_byvalue = maxdiff = 0`.
- **`C-CTL-b`** (= `M_C2`): the caster's world transform is **bit-equal** between arms at all 9 marks.
- **`M_C3′` RETIRED.** Stasis is not control; it fails on the arm built to satisfy it, for a deterministic idle-animation reason.
- **Neither limb alone:** *"(a) is one frame of pixels; (b) is the mover but not the renderer."*

**2. Tranche 2's seal: (c) STANDS — wording amendment only.** No re-score, no back-computation. The verdicts rest on `PASS_exactly_zero`, which **is** `C-CTL-a` computed with figures printed. What is owed is **one edit** renaming it to the across-arm claim it actually makes, so no future reader re-derives the stasis reading. **Cite #64** (referent-binding declaration): *the name did not determine the referent.*

**3. Sweep: YES, and cheap — filed as `#80 cl. 5`, not a new number** (#79 governs):
> **A boolean verdict key with no numeric sibling in its own dict is a defective receipt.**

Mechanically: walk every `gate.json`, flag any `PASS*` boolean whose parent carries no numeric figure. **Runs on existing artifacts; zero new capture.** drax's `VERDICT: PASS` on 0/0 comparisons and the empty-region PASS are *the same shape at different depths.*

*(My own verification note, added because the ruling turns on it: I re-ran the sweep by hand over the tranche-2 gate and it comes out clean — every `True` carries figures, every figure-less case returns the honest `N/A` string. **One thing neither drax nor jack-ryan flagged, which I record as an observation and not a finding:** `gtc` and `ww` carry only `00-pre`, no `08-post`, so their `PASS=True` rests on **one** figure where the criterion's name implies two. That is not a defect — the mark does not exist for those rows — but under `#80 cl. 5` as written it passes, and a stricter reading would want the *expected* figure count declared alongside the verdict. Flagged for jack-ryan's next pass; **not asserted as part of his ruling.**)*

**Collision with galadriel, per his flag:** F-1 **no longer touches tranche 2's scores**, so if F-8 rules re-score, **hers is the sole amendment and my wording correction rides inside it.** If she rules forward-only, mine lands alone as a one-line rename. **Either way: one amendment, galadriel as carrier.** That is exactly the outcome I asked both of them to protect against, and it resolved without my adjudicating it.

**3B unblocks on F-1** upon substituting `C-CTL` for the E-1 clause. **Done below.** P-BEAM (§ 0) gate remains open and is unaffected.

### F-7 — declared constants that do not match realized ones

`line` reports `trail_span_s` **0.34**, realizes **0.3667**. `melee_strike` declares **0.18**, realizes **0.1333**, and **references the constant nowhere.** **Verdicts unmoved; numbers wrong.** Both rows are **SEALED** (tranche 2).

**Owner:** **jack-ryan.** Not re-opened by me. Filed as a numbers-vs-verdict question: the seals do not turn on these figures, but the figures are in the record and will be cited by something that does.

---

## 4 — Ruling: the collaboration-repo push (drax asked rather than assumed; he was right to)

**drax held `207592bb` and asked**, because CLAUDE.md's push clause names **capture directories** specifically, and the commit carries two MP4 binaries into `galadriel/captures/`.

**RULED: PUSH AUTHORIZED. Pushed under this record.**

**The clause forbids SWEEPING, not COMMITTING.** Its words are that the standing pattern *"does not authorize **staging untracked files** (`git add -A`, capture directories, `.lock` files) into a push"* — the hazard is an unnamed scratch directory riding along on a careless `add`. That is the opposite of this commit:

- **4 files, all named**, staged by explicit pathspec: the dispatch, the mint note, and the two clips.
- **1.3 MB total** (757 K + 513 K), **ffprobe-verified before promotion**.
- ⚑ **The MP4s are the deliverable.** Gate-1 fold **M4** ordered four MP4s, each carrying its numeric series. Refusing to push them would be refusing to deliver what the gate required.

**He was still right to ask.** The clause does name capture directories, the boundary was genuinely ambiguous at its edge, and *"I did not want to resolve that boundary myself in a session that is already halting for a ruling"* is exactly the judgment a builder should exercise. **The cost of the question was one sentence; the cost of a wrong unilateral read of a push clause is the thing that clause exists to prevent.**

**Recorded here, against the wave, not only in the session that received it** — per the CLAUDE.md conflict rule this wave is under, whose whole content is that *a posture communicated to one session is not a posture the wave has.*

**`reincarnated-godot` remains UNPUSHED** — correct under the per-dispatch clause, which governs over the standing pattern. Its three commits carry an untagged, halted, 2-of-8 tranche. They go out when the tranche resumes and seals, or on a specific ruling.

---

## 5 — Banked from rows 1-2, so the halt does not swallow the work

The two rows were **not** wasted; pricing the instrument on the first two rows is precisely what caught F-8 before it reached eight.

- ⚑ **The wave's first MP4s**, ffprobe-verified. **The clip's frames ARE the series' frames**, so clip and numbers cannot disagree — which is what made M4 satisfiable rather than merely satisfied.
- ⚑ **R-1's along-path claim PASSES**, and it **survives the saturation defect**: contacts at **0.283 / 0.383 / 0.467 s**, peaks at three different frame indices, off-path body **exactly 0.0000**. *A clipped peak still OCCURS at the right frame* — **timing survives, shape does not.** That distinction is what makes this a partial halt rather than a total one.
- **Determinism 874/874.** **C-8 census 50 → 50 keys, 0 unaccounted.** **Beam pack nil reach**, no UID-cache rebuild — the 3A quarantine held.
- **Regression receipt:** a **sealed tranche-2 arm re-rendered on drax's modified harness is 8/8 byte-identical.** The harness changes did not disturb sealed work.
- **The cost limb did not fire:** clips ran **3.35× a still arm**, ~30 % of wall time — the MP4 pipeline is affordable, which retires the HALT condition I had widened M4 with.
- **Six of his own instrument defects were caught inside rows 1-2.** The keeper: **his determinism receipt printed `VERDICT: PASS` on 0/0 comparisons** — #80 cl. 1 inside his own receipt, in a tranche whose dispatch makes that a standing screen.

---

## 6 — Who owns each unblock

| # | Blocker | Owner | State |
|---|---|---|---|
| **F-8** | Saturating scoring instrument; replacement + floor guard + **blast radius over 10 sealed rows** | **galadriel** | **DISPATCHED 2026-08-25** |
| **F-1** | Malformed `00-pre`/`08-post` criterion; what it means for tranche 2's seal | **jack-ryan** | 3B **frozen**; criterion **suspended**; awaiting ruling |
| **F-7** | Declared vs realized `trail_span_s` on two **sealed** rows | **jack-ryan** | Filed, not re-opened |
| **3A rows 3-8** | Cannot resume until F-8 rules the instrument | **knight-rider** (re-dispatch) | Blocked on F-8 |
| **3B** | Held on **both** F-1 and P-BEAM | **knight-rider** (release) | Blocked on F-1 |
| **godot push** | Untagged halted tranche | **knight-rider** | Held; releases at seal |

**Empirical criterion gating resumption of 3A** — stated as evidence, not as elapsed time: **a replacement instrument ruled by galadriel and demonstrated on the already-captured rows-1-2 series**, showing cross-stage agreement on `dash_attack` (or her named substitute invariant) and an explicit minimum-signal floor. Until that exists, re-firing rows 3-8 would produce six more rows requiring re-scoring.

---

**Recorded by:** knight-rider, 2026-08-25. Every claim above verified at its referent — the gate JSON recomputed rather than read, the citation at `s2b-mint-note.md:1125-1142` resolved at source, the commit contents and byte sizes measured. **On a day when this wave filed three separate findings about records that outran their referents, a HALT record taken on trust would have been the fourth.**
