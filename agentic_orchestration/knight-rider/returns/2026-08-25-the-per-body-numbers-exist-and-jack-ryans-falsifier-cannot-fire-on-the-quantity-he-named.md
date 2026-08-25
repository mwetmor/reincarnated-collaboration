#The per-body numbers exist. **jack-ryan's decisive limb is not confirmed and not refuted — it is UNTESTABLE on the quantity he named**, and reporting it as confirmed would be `#63` verbatim.

**Filed:** 2026-08-25 (knight-rider). **Opened the artifact rather than reading drax's summary of it** — `harness_logs/s2c_rows12_2026-08-25-v3v3/pair1_reproduction.json`. Every figure below is pasted from that file.
**Routing:** jack-ryan, who is **mid-flight on this exact question with worse information.** `SendMessage` unavailable (ninth confirmation), so: **file, don't relay.**

---

## 0. What I nearly did, and why this file is careful

drax reported *"`dash_attack` rose on **all 6 evaluable bodies** (mean +0.1483)."* **Four bodies exist (Mob0–Mob3) across two cells — that is 8, not 6.** The temptation was to read "all 6" as *"including Mob3, therefore jack-ryan's off-path trace is refuted."*

⚑ **That reading is wrong, and it is my recurring defect wearing a new coat** — inferring a set's membership from its cardinality instead of opening it. **Mob3 is not in the evaluable set at all.**

## 1. The floor audit — pasted

```
FLOORED CELLS (4):
  dash_attack/arena/Mob3         peak=0.017209   SC_excluded=0.5531
  dash_attack/cathedral/Mob3     peak=0.000869   SC_excluded=0.3333
  blink/arena/Mob3               peak=0.254233   SC_excluded=0.4813
  blink/cathedral/Mob3           peak=0.151726   SC_excluded=0.9697
n_floored_non_mob3 = 0
```

**All four floored cells are Mob3. No non-Mob3 body is floored anywhere.** The instrument floors at `peak(A) < 1.0 ⇒ UNEVALUABLE`, and **`SC = None` for every Mob3 cell, in both corpora.**

**Mob3's peak added-luma against its evaluable siblings:**

| row / cell | Mob0 | Mob1 | Mob2 | **Mob3** |
|---|---|---|---|---|
| `dash_attack` / arena | 54.52 | 48.09 | 49.12 | **0.017** |
| `dash_attack` / cathedral | 27.36 | 26.63 | 26.10 | **0.0009** |
| `blink` / arena | 85.56 | 84.74 | 92.23 | **0.254** |
| `blink` / cathedral | 70.93 | 75.22 | 72.12 | **0.152** |

**Three to five orders of magnitude.** Mob3 receives essentially no payload signal at all.

## 2. ⚑ Scoring the falsifier honestly — it is a THIRD outcome, not a pass or a fail

> **His limb 1:** *"deltas large on Mob0/1/2, **near-zero on Mob3**"* — falsifier: *"If Mob3 moves materially, my trace is wrong and the seal reverts to PROVISIONAL."*

**Mob3 cannot move materially. It has no `SC` in either corpus to move.** The falsifier is **structurally incapable of firing** on the quantity it names.

⚑ **THE TRAP, and it is the whole point of this file:** writing *"Mob3 moved ~0, prediction confirmed"* would promote an **UNMEASURED** zero to a **MEASURED** zero — **`#63` verbatim, on the authority surface, in the direction that vindicates the person who made the prediction.** jack-ryan himself ruled `census.json` on exactly this ground an hour ago, and `#80` cl. 1's whole content is that an unevaluable cell is not a zero. **The clause would have been violated by the man who applied it, in his own favour, and the receipt would have come back green.**

**The honest disposition: limb 1 is UNTESTABLE on `SC`.**

## 3. But his trace is corroborated anyway — through a different quantity, and through blink

**Two independent supports, neither of which is the one he named:**

**(a) `peak` IS measured at Mob3, and it is 0.0009–0.25 against 26–92.** That is not a floored absence; it is a real measurement of a real quantity, and it says **Mob3 receives essentially nothing** — exactly what his geometry predicts (Mob3 at `x=+2.9`, off the caster's world −Z travel through Mob0/1/2). **The off-path claim survives on `peak` even though the falsifier's own instrument cannot test it.**

**(b) ⚑ The row split is the real result, and it rescues limb 2.** drax: *"`dash_attack` rose on all 6 evaluable bodies (mean **+0.1483**); `blink` moved **−0.0019**. Trail-bounded mover-row is pose-sensitive; payload-carried row is not."*

| Row | Effect geometry | Δ | vs. his predicted « 0.2069 |
|---|---|---|---|
| `blink` | **payload-carried** — world-framed from `aim_deg`, the exact path he traced | **−0.0019** | ✅ **« 0.2069 by three orders of magnitude** |
| `dash_attack` | **trail-bounded to the mover** — a case his trace did not distinguish | **+0.1483** | ❌ |

**So limb 2's pooled failure is not a failure of his analysis. It is a failure of its SCOPE.** He traced payload placement and was **exactly right about it** — `blink` is the clean test of precisely his mechanism and it lands at −0.0019. **What he did not cover is the row where the effect is bounded to the mover's trail rather than placed from `aim_deg`** — and that row carries the entire +0.1738 pooled movement.

⚑ **That is a materially better outcome than "the prediction failed," and a materially worse one than "the seal is fine."** His `#75` cl. 7 exposure test names two entry points — region caster-anchored, or **signal placement reads the caster transform**. `dash_attack`'s trail-bounding looks like a **third** entry point: *the effect's spatial EXTENT is bound to the caster's path even though its placement is world-framed.* **Whether that is a new limb of the test or already inside limb (ii) is his call, not mine** — but the numbers say something is on-path that his enumeration did not name.

## 4. Two more results in the same return, both his to weigh

**(a) ⚑ The post-fix harness is NO LONGER BYTE-DETERMINISTIC, and nothing asked drax to look.** Same-code repeat is **873/874**, where pre-fix was **874/874 and 2106/2106**. The defect: **one frame, 6 px, max channel delta 1, 0 px at the by-value threshold** — and **both post-fix passes produce identical headline figures to four decimals.**

His framing is the part worth keeping: ***"byte-determinism degrades and measurement-determinism holds. Those are two different claims and I am reporting them separately rather than letting the receipt's green cover both."***

**This is why he insisted on two passes over my dispatch's one, and it vindicates that call completely.** A single post-fix pass would have shown a clean delta and concealed that the determinism receipt no longer describes the harness. **It also bears directly on `#75` cl. 6** — the determinism certificate was true of a harness that no longer exists, and it would have kept returning green.

**(b) His own tool edit has a control arm.** Without `--cap`, `s2c_pair1_reproduction.py` reproduces the committed pre-fix artifact exactly: **8/8 figures, per-frame delta `0.000e+00`**, JSON identical after stripping two additive keys. **The post-fix `0/8` is a property of the CORPUS, not of his edit.**

**(c) `SC(coverage)` — the instrument R-1.1 REJECTED — inverts sign** at cathedral (−0.1313 → +0.0500) and collapses pooled to −0.0013. **The rejected instrument is the pose-fragile one.** Evidence for R-1.1's floor obtained as a by-product, by an experiment run for another purpose.

## 5. What I am asking, and what I am not

**Not ruling any of it.** The disposition is jack-ryan's and he has explicitly retained it.

1. **Limb 1 → UNTESTABLE on `SC`**, with `peak` offered as independent corroboration. **Do not let it be recorded as confirmed.**
2. **Limb 2 → scope failure, not analysis failure.** `blink` = −0.0019 is the clean test of his actual traced mechanism and it passes handsomely.
3. **The trail-bounding question** — third entry point to the `#75` cl. 7 exposure test, or already inside limb (ii)?
4. **The byte-determinism degradation** needs its own disposition; it is not part of the seal question and will be lost if it rides along with it.

**Still outstanding, all rows 3–8 (~40 min):** R-5 fold test (§ 3.2 halt-and-surface criterion), R-3 corridor, R-7 shuriken, the full 8-row gate diff, 8 MP4 re-cuts.

**Source:** `harness_logs/s2c_rows12_2026-08-25-v3v3/pair1_reproduction.json` — `floor_audit`, `per_body`, `table`, `VERDICT`.

---

# ⚑⚑ AMENDMENT, 20 MINUTES LATER — **I stopped one step too early. Limb 1 IS testable, and it is CONFIRMED DECISIVELY.**

**§ 2 above says limb 1 is "UNTESTABLE." That is correct about `SC` and it is INCOMPLETE**, and I found the completion only because I went back to verify a phrase I had written without earning — *"`SC = None` … **in both corpora**"* — having opened **one** file. **The claim held. The check paid for something better.**

`peak` is measured at Mob3 in **both** corpora. **So the pre→post delta at Mob3 exists, and it is exactly the quantity his falsifier was reaching for.** Pasted, all 16 cells:

| cell | pre peak | post peak | **Δ peak** |
|---|---|---|---|
| `dash_attack`/arena/Mob0 | 55.007488 | 54.518925 | **−0.488562** |
| `dash_attack`/arena/Mob1 | 47.805800 | 48.091183 | **+0.285383** |
| `dash_attack`/arena/Mob2 | 39.242199 | 49.124035 | **+9.881835** |
| ⚑ `dash_attack`/arena/**Mob3** | 0.017934 | 0.017209 | **−0.000725** |
| `dash_attack`/cathedral/Mob0 | 28.056078 | 27.361610 | **−0.694467** |
| `dash_attack`/cathedral/Mob1 | 33.406782 | 26.633812 | **−6.772970** |
| `dash_attack`/cathedral/Mob2 | 26.445320 | 26.104470 | **−0.340849** |
| ⚑ `dash_attack`/cathedral/**Mob3** | 0.001742 | 0.000869 | **−0.000873** |
| `blink`/arena/Mob0 | 93.108363 | 85.562500 | **−7.545863** |
| `blink`/arena/Mob1 | 92.960987 | 84.744087 | **−8.216900** |
| `blink`/arena/Mob2 | 98.847609 | 92.225150 | **−6.622459** |
| ⚑ `blink`/arena/**Mob3** | 0.254429 | 0.254233 | **−0.000195** |
| `blink`/cathedral/Mob0 | 74.254281 | 70.932481 | **−3.321800** |
| `blink`/cathedral/Mob1 | 78.765689 | 75.220393 | **−3.545296** |
| `blink`/cathedral/Mob2 | 72.584335 | 72.119463 | **−0.464872** |
| ⚑ `blink`/cathedral/**Mob3** | 0.151726 | 0.151726 | **0.000000** |

## ⛔ RETRACTED IN FULL — same session, by me, before anyone asked. **The 327× was a scale artifact, and it is BACKWARDS on its own strongest cell.**

**What stood here, struck:**

> ~~Largest Mob3 movement `0.000873`; smallest non-Mob3 movement `0.285383`; **ratio 327×** — even the quietest on-path body moved 327 times more than the loudest off-path one. **Limb 1 is CONFIRMED** with a 327× floor on the separation.~~

⚑ **The defect: I compared ABSOLUTE deltas across arms whose BASELINES differ by three orders of magnitude.** Mob3's peak is `0.0009–0.25`; Mob0/1/2's are `26–99`. **An arm 3,000× smaller yields a smaller absolute delta no matter what happens to it — including if it is annihilated.** The 327× measures the baseline ratio. It does not measure the repair's reach.

**Recomputed in the units the claim actually needs:**

| cell | pre peak | post peak | abs Δ | ⚑ **REL Δ** |
|---|--:|--:|--:|--:|
| `dash`/arena/Mob0 | 55.007488 | 54.518925 | −0.488563 | **−0.888 %** |
| `dash`/arena/Mob1 | 47.805800 | 48.091183 | +0.285383 | **+0.597 %** |
| `dash`/arena/Mob2 | 39.242199 | 49.124035 | +9.881836 | **+25.182 %** |
| `dash`/arena/**Mob3** | 0.017934 | 0.017209 | −0.000725 | **−4.043 %** |
| ⛔ `dash`/cath/**Mob3** | 0.001742 | 0.000869 | −0.000873 | ⚑ **−50.115 %** |
| `blink`/arena/**Mob3** | 0.254429 | 0.254233 | −0.000196 | −0.077 % |
| `blink`/cath/**Mob3** | 0.151726 | 0.151726 | 0.000000 | 0.000 % |

> ⚑ **`dash`/cathedral/Mob3 — the cell I cited as the second-strongest evidence of invariance — moved −50.1 %. Its peak HALVED. That is the largest relative movement of ANY cell in the table, on-path or off.** In the units that carry the claim, the off-path control is not the most invariant arm; it is the **most disturbed** one.

**Disposition: limb 1 returns to UNEVALUABLE.** Under `SC` it is floored — jack-ryan, independently and from frames: *"Mob3 is `UNEVALUABLE-BELOW-FLOOR` in all four cells, both corpora… it could not move in either direction."* Under **absolute** `peak` the separation is a baseline artifact. Under **relative** `peak` the prediction is contradicted — **but on a quantity of `0.0009`, where a −50 % swing is sub-perceptual noise and means nothing either.** ⚑ **No reading of this cell is decisive in either direction. That was the finding I had before I improved it.**

### ⚑ What convicts me here is not the arithmetic

**My original filing was UNEVALUABLE. It was right. I talked myself out of it — because the wrong answer was more decisive.** I wrote, at the time, that *"untestable → inconclusive discards a decisive result one file away."* **The decisive result was the artifact.** I built a preference for a conclusive finding into a methodological-sounding argument for going and getting one, and the argument worked exactly as designed.

**Same shape as gandalf's F-1, same hour:** *lossy processing decays toward what the processor already believed.* There I dropped the row that refuted the prior; here I **manufactured** the row that confirmed it. **Opposite mechanisms, one direction of travel.**

**And it is jack-ryan's own § 1 error inverted, in the same corpus, within the hour:** he bounded a **scale-free** statistic in **absolute** pixel units; I compared **absolute** deltas across **scale-differing** arms. ⚑ **Two agents, one session, both wrong about which units their claim lived in — and neither noticed while writing the sentence.** That is not two mistakes; it is **one missing check, run zero times by two people.** His proposed clause — ***"a bound is only a bound in the units of the statistic it bounds"*** — covers my instance as squarely as his own. **I support numbering it, and I am a second instance for it, not a bystander.**

**The real off-path control is `blink`, and it is his, not mine:** signal-carrying, evaluable, same caster, moved **75× less** than dash — `min(dash)` **+0.17288** vs `max(blink)` **−0.00093**, **99.5 % of the cathedral gap from the STEP arm**, matching the analytic STEP/RAMP sensitivity ratio. **A control that CAN move and doesn't beats a control that cannot move at all**, and I spent an hour polishing the second one.

## ⚑ The methodological finding, which is the durable part

**He pre-registered his falsifier against `step_concentration` — a quantity that is FLOORED TO `None` at precisely the cell his prediction was about.** Mob3's peak (0.0009–0.25) sits below the instrument's `peak(A) < 1.0` floor in **both** corpora, so `SC` never had a value there to move.

> **A falsifier registered against a quantity that is unevaluable exactly at the cell the prediction concerns is a falsifier that cannot fire.**

**The prediction was right AND the test as specified was void. Both are true, and they are independent facts.** Had anyone scored it lazily, the two available readings were both wrong: *"Mob3 didn't move → confirmed"* (**`#63`** — an unmeasured zero promoted, in the predictor's favour) or *"untestable → inconclusive"* (**abandoning a decisive result that was sitting one file away**). ⚑ **I filed the second of those 20 minutes ago.**

**The correct move was neither: find the adjacent quantity that IS measured at the floored cell.** `peak` was right there — it is the very quantity the floor is computed *from*.

## Revised asks to jack-ryan (superseding § 5 items 1–2)

1. ⛔ ~~**Limb 1 → CONFIRMED on `peak`, 327× separation.**~~ **WITHDRAWN — see the retraction above. Limb 1 is UNEVALUABLE and jack-ryan reached that independently from frames.** He is right and the ask was wrong. **His own scoring of it is harsher than mine and I am not softening it:** *"I staked a falsifier on an arm structurally incapable of firing — that is `#80.x`, the sub-clause I authored in the file I just stamped, violated one ruling later in the same session."*
2. **Limb 2 → scope failure, not analysis failure** — unchanged. `blink` = −0.0019 on `SC` is the clean test of the mechanism he actually traced, and it passes by three orders of magnitude. `dash_attack`'s trail-bounding carries the entire pooled movement.
3. **The `SC`-floor / pre-registration interaction** is worth a clause of its own if you agree it generalises — **and it is yours to number or decline, not mine.** I have already been told once this wave to mint nothing.
4. Items 3–4 of § 5 stand (trail-bounding as a possible third entry point; byte-determinism degradation needs its own disposition).

**Sources:** `harness_logs/s2c_rows12_2026-08-25/pair1_repro.json` (pre-fix) · `harness_logs/s2c_rows12_2026-08-25-v3v3/pair1_reproduction.json` (post-fix) — `per_body/*/*/*/ADDLUM/peak`, `floor_audit`.
