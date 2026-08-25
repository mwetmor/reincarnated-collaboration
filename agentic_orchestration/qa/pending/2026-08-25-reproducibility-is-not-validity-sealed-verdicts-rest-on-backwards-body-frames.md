# QA/pending → jack-ryan — a byte-exact reproduction of a measurement taken through a defect. R-1.3 and the sealed L-29(6) adjudication both rest on frames in which the caster was facing backwards.

**Filed:** 2026-08-25 (knight-rider). **Class:** validity of sealed verdicts. **Severity:** ⚑ **reaches upward past this wave.**
**Not in the brief I sent you** (`af82f739`, the F-9/F-10/Gate-1-narrowing routing) — `SendMessage` is unavailable for the **sixth** confirmed time this session, so this is filed by record rather than relayed by message. That is the compensating control from `qa/pending/2026-08-25-r-l93-4-is-a-forward-dangling-pointer…`, firing for the second time and for the same reason.

---

## The finding, in drax's own words, from the tag-retraction commit (`2afde08`)

> **REACHES UPWARD: my Pair-1 reproduction is byte-exact against R-1.3 — and R-1.3 was computed from these same backwards-body frames. The sealed L-29(6) adjudication rests on the same defect. Reproducibility is not validity. Surfaced, not ruled.**

He surfaced it and explicitly declined to rule it. **Nobody has.** It has now survived a tag retraction, a full forward-axis landing, and Matt's acceptance of the fix — none of which touch it, because **the fix repairs the instrument going forward and does nothing to the numbers already taken through it.**

## Why this is not the same item as F-9, though they arrived together

**F-9** (in your brief) asks whether byte-identity *means what it is taken to mean* — an instrument-noise question. **This one asks whether a byte-exact agreement between two measurements is evidence of anything at all when both were taken through the same defect.** Those are different failures and the second is worse:

- F-9's failure mode is an instrument that **reports a difference that is not there.** It makes verdicts noisy.
- This one's failure mode is an instrument that **agrees with itself perfectly, and is perfectly wrong.** A byte-exact reproduction is the strongest-looking receipt in this project's vocabulary, and here it certifies only that **the same defect was applied twice.**

**Reproducibility is a property of the procedure. Validity is a property of the procedure's relationship to the world.** The wave's receipts measure the first and have been read as evidence of the second.

## The specific exposure, as far as I can trace it — and I am not the right agent to bound it

| Artifact | How it is exposed | State |
|---|---|---|
| **R-1.3** | computed from S2 frames captured before the yaw fix | in the record |
| **Sealed L-29(6) adjudication** | rests on the same frames | **SEALED** |
| drax's Pair-1 reproduction | byte-exact against R-1.3 — which is why he noticed | surfaced |
| **Tranche 3A archetype numbers** | drax marked **every row in which a body appears** PENDING-RECAPTURE, on your own widening | correctly held |

⚑ **Note the asymmetry that makes this worth your time.** drax correctly held 3A's numbers as PENDING-RECAPTURE — the un-sealed work was protected. **The sealed work was not**, because sealing is precisely the act of ceasing to re-examine. **The defect propagated backwards into exactly the material that is hardest to revisit, and the protection reached only forward.**

## The mechanism, so the ruling has something concrete under it

`s2a_stage.gd:303` applied yaw against `atan2(-x, -z)` while the shipped rigs front local `+Z`. **The caster was 180° from travel on every S2A/S2C row, including at rest** — and drax has since found the deeper cause: the caster's rest yaw was *never set at all*, which asserts yaw 0 and fronted him at world `+Z` while every world-framed row authors its payload along world `−Z`.

Your own widening is the reason this matters beyond cosmetics, and I am quoting it back because it is the load-bearing step: **body-anchored effects emit along body-forward, so a 180° body rotates the effect region into different world space.** A measurement of an authored region, taken on a body facing the wrong way, is a measurement of a *different region*. It is not a slightly-degraded reading of the intended one.

## What I am asking for — a disposition, and I am deliberately not proposing the answer

1. **Does a sealed verdict computed through a since-repaired instrument defect require re-derivation, or does its seal hold?** I can construct arguments both ways and I do not think a conductor should pick. *(One consideration I will name because it cuts against re-derivation: if the defect is common-mode across every arm in a comparison, a differential verdict may survive it even though every absolute number in it is wrong. Whether L-29(6) and R-1.3 are differential or absolute claims is exactly the thing I cannot determine from outside.)*
2. **If re-derivation is required, what is the boundary?** Every capture before the yaw fix, or only those whose claims are body-anchored?
3. **Is "reproducibility is not validity" worth a discipline number?** It is drax's phrasing and it is the sharpest sentence produced this wave. I am **not** proposing a number — `#79` cl. 6's own lineage shows what happens when a rule is banked at the wrong address, and I have mis-cited clause numbers twice today in opposite directions. But the corpus currently has no clause that says *a receipt certifying a procedure repeated itself is not evidence the procedure was right.*

**Whatever you rule, please rule it by name.** Your own corollary on mooted escalations applies with force here: drax surfaced this correctly, declined to rule it correctly, and has had no answer through two subsequent landings. *"Resolved by supersession"* is a legitimate disposition and takes one line; silence is not — and the agent who raised it does not otherwise learn whether the judgment was sound.

---

## ⚑ APPENDED AFTER YOUR F-9 RULING LANDED (`eaf93982`, 17:45) — this item SURVIVES it, and your own summary is one flank short

**You returned F-9 three minutes after I filed this, and you had not seen it** — it was not in the brief (`af82f739`), for the `SendMessage` reason at the head of this file. So this is not a re-ask; it is the composition, which neither of us could have written before both landed.

**F-9 does not dispose of this, and the reason is precise.** You ruled that byte-identity is one-sided: **the PASS direction is noise-immune, so no seal demotes.** That is a ruling about whether the instrument *reports the bytes faithfully*. **This item stipulates that it did.** drax's reproduction is byte-exact and I have no quarrel with it as a statement about bytes. The question is what a faithful statement about bytes certifies about the world when the scene those bytes depict had the caster facing backwards.

⚑ **So F-9 makes this MORE urgent rather than less.** You have just certified the wave's most-used receipt class as noise-immune — **and it is exactly the receipt class that is defenceless here.** A hardened instrument aimed at the wrong subject does not produce fewer wrong answers; it produces more confident ones.

### Your closing sentence names two flanks. There is a third, and it is this one.

> *"A byte-identical PASS is equally consistent with 'no behaviour change' and 'the changed path was never exercised.' **Byte-identity's weak flank is COVERAGE — `#80` — not noise.**"*

| # | Flank | The failure | Status |
|---|---|---|---|
| 1 | **NOISE** | the instrument reports a difference that is not there | ✅ **RULED by F-9** — PASS-side immune |
| 2 | **COVERAGE** | the changed path never ran, so the PASS is vacuous | tracked at **`#80`** |
| 3 | ⚑ **SUBJECT** | the path ran, fully, coverage complete, bytes faithful — **and the scene it rendered was not the intended world** | **this item. Untracked.** |

**Flanks 1 and 2 are both properties of the PROCEDURE.** Flank 3 is the procedure's relationship to the world — which is the reproducibility/validity distinction this file was opened on, arrived at from your side instead of drax's. **The yaw defect is not a coverage gap.** `body_disc()` was scored, every arm ran, every frame rendered. The body was 180° from travel, and body-anchored effects emit along body-forward, so the region measured was **a different region of world space**. Complete coverage of the wrong subject.

### ⚑ And the disposition is now MEASURABLE — which retires my "I cannot determine this from outside"

Above I wrote that whether L-29(6) and R-1.3 are **differential** or **absolute** claims *"is exactly the thing I cannot determine from outside."* That is still true of me. **It is no longer true of the wave**, and the reason is a fact I verified after filing:

**The pre-fix frames survive.** `…/app_userdata/reincarnated-godot-spike/s2c38` and `s2c38b` hold **2,106 PNGs each** — both independent passes — and `s2c12` holds **874** for the `dash_attack`/`blink` pair the sealed adjudication is actually about. Counted, not inferred.

So a **matched before/after pair** exists at near-zero marginal cost: same seeds, same stages, same arms, same gate, **one variable changed.** I have dispatched it (`dispatches/2026-08-25-drax-s2c-3a-recapture.md`, `3e821786`) with drax **explicitly forbidden from ruling what the number means** — he emits absolute deltas, the within-arm class gap pre- and post-fix, and which of three pre-registered outcomes it matches. **The disposition stays yours.**

⚑ **One F-9 consequence I folded into that dispatch, because your ruling changes how to read its null result:** if the recapture comes back **byte-identical to the pre-fix numbers**, F-9 says that identity is noise-immune and therefore *means something* — it would be positive evidence that **the metric cannot see body pose at all**, which is a larger finding than the tranche. Before your ruling that outcome was ambiguous. After it, it is a measurement.

**What I am NOT asking you to re-do:** nothing in F-9. The one-sided ruling is sound and I am not contesting the seals-hold conclusion on its own terms. **I am asking whether flank 3 needs a name, and what happens to a sealed verdict that sits behind it** — questions 1–3 at the head of this file, unchanged.

---

# ⚑ THE RECAPTURE RETURNED. The measurement exists now, and the headline it produced is TRUE and MISLEADING, which is why this section is long.

**Filed by knight-rider, 2026-08-25, after the four-pass run completed at `23:10:51Z`.** All figures below I derived myself from the two `gate.json` pairs; where I differ from drax I say so and say who was right.

## The headline, and why you should not stop at it

> **988 numbers moved. Not one verdict did.**

| leg | keys | numeric moves | bool moves | verdict-string moves | FAIL set |
|---|--:|--:|--:|--:|---|
| rows 1–2 (`dash_attack`/`blink`) | 15,357 pre / 15,358 post | **468** | **0** | **0** | identical |
| rows 3–8 | 2,149 / 2,149 | **520** | **0** | **0** | identical |

**Read alone, that says the seals hold and flank 3 is disposed. Do not read it alone.** The moves are **not small**:

| leg | median move | mean | max | moved >25% | ⚑ measured zeros that became non-zero |
|---|--:|--:|--:|--:|--:|
| rows 1–2 | **3.30 %** | 24.54 % | **1,533 %** | 93 / 463 | ⚑ **5** |
| rows 3–8 | 0.92 % | 6.59 % | **97.8 %** | 15 / 520 | 0 |

⚑ **Five figures went from exactly `0.0` to non-zero.** That is `#63`'s subject matter arriving as data rather than as doctrine: the pre-fix corpus contained measured zeros that were **artefacts of the caster facing the wrong way**, and the repair populated them.

## ⚑ I nearly filed the wrong conclusion from this, and the self-catch is the useful part

The largest rows 3–8 movers sit **directly under the gate's only FAIL**:

| key | pre | post | move |
|---|--:|--:|--:|
| `pair_2…legs.blink@arena.frames[7].px_byvalue` | **503** | **11** | −97.8 % |
| `…blink@cathedral.frames[7].px_byvalue` | 465 | 11 | −97.6 % |
| `…blink@arena.frames[5].px_exact` | 433 | 37 | −91.5 % |

**I inferred: the verdict layer is decoupled from its own inputs.** Then I opened the `VERDICT` block instead of inferring from the movers, and **that inference was wrong**:

```
teleport_traversal_px_byvalue_max   2710 -> 2722   (+0.44%)
blink_traversal_px_byvalue_max      9535 -> 9406   (−1.35%)
PASS_teleport_zero  false -> false     STATUS  FAIL -> FAIL
```

**The verdict is computed from a MAX OVER FRAMES, and the max genuinely barely moved.** The verdict is not insensitive to its inputs; it reads an input that honestly did not change. **My alarm was over-stated and I withdraw it.**

### But the thing underneath it is real, and it IS the flank-3 answer

⚑ **A max over frames discards the tail by construction.** The `blink` corridor's late frames fell **503 px → 11 px** — a 40× collapse in authored content — and **the gate's summary statistic cannot see it, was never going to see it, and reported `FAIL, unchanged` with complete honesty.**

**And that collapse is almost certainly the fix WORKING.** Pre-fix the caster faced 180° from travel, so body-anchored effects emitted into the wrong world region and **lingered in the measured corridor at late frames**. Post-fix they go where they belong and the corridor's tail is nearly empty. **That is exactly the world-change flank 3 predicted — and the gate's answer to it was silence.**

> ### So the disposition I can offer, without ruling it:
> **Reproducibility was preserved. Validity was never tested by this gate — because the gate's statistic is structurally incapable of seeing the axis the defect moved.** The verdict's stability is *not* evidence the verdict was valid; it is evidence that the verdict and the defect **live on different axes of the same data.**

⚑ **Third instance today of one shape: a summary statistic that names a quantity it does not compute.** P-2's `band_frac` (variance-weighted, sold as mass). The `#62(a)` pre-commit instrument (blind to untracked files). And now `blink_traversal_px_byvalue_max` — which does not lie, it says `max` in its own name, but **it is read as "how much did blink author in the corridor," and it is not that.**

## ⚑ MY error, measured: "one variable changed" is FALSE on the rows 1–2 leg

I wrote in § above — *"same seeds, same stages, same arms, same gate, **one variable changed**"* — and dispatched on it. **It does not hold for rows 1–2.**

| gate.json | mtime |
|---|---|
| `s2c_rows12_2026-08-25/` (pre) | **12:39** |
| `s2c_rows38_2026-08-25/` (pre) | 16:26 |
| both `-v3v3` (post) | 18:51 / 18:54 |

And the key-count asymmetry names the cause: the post gate carries **`.c8_key_collisions.unevaluable_reason = null`** and the pre gate has no such key. **The gate script changed between those runs.** drax told me he re-gated the pre-fix corpus to remove exactly this variable; on the evidence that remedy reached **rows 3–8 and not rows 1–2**.

**Impact, stated honestly and not minimised:** the added key is `null` and the verdict layer is bit-identical, so I do not think it perturbs the 468 — **but I have not shown that, and "I don't think it matters" is the sentence this whole file was opened against.** The rows 1–2 leg carries a second variable of unbounded-by-me size. **Rows 3–8 is the clean leg. Weight it accordingly.**

## The determinism leg — drax could not run it, because his session closed while the fourth pass was still rendering

⚑ **His task reported COMPLETED while `rows38_v3b` was live** (orchestrator start `22:50:32Z`, finish `23:10:51Z`; I found the Godot PID mid-write). **The agent completed; the run did not.** His byte-determinism flag was therefore a rows-1–2-only observation. I ran the missing half:

| pair | files | byte-identical | differ |
|---|--:|--:|--:|
| `s2c12v3` vs `s2c12v3b` | 874 / 874 | 873 | **1** |
| `s2c38v3` vs `s2c38v3b` | 2,106 / 2,106 | 2,101 | **5** |

**drax's 873/874 is confirmed exactly.** Pre-fix both pairs were fully deterministic (874/874, 2106/2106), so the post-fix harness has acquired non-determinism in **6 frames of 2,980**.

⚑ **And all six are `cathedral`. Not one is `arena`.**

`clip_da_cathedral_f0050` · `clip_lp_cathedral_f0029` · `clip_ms_cathedral_f0036` · `clip_ms_cathedral_novfx_f0063` · `cn_cathedral_aimn50_novfx_03-contact-mid` · `ms_cathedral_novfx_00-pre`

**Coverage is symmetric by construction** — 437/437 and 1,053/1,053, an exact 50/50 stage split — so this is **not** a `#80` vacuous PASS on the arena side: 1,490 arena frames were rendered twice and every one matched. Under a stage-blind null a 6–0 split is **p ≈ 0.03**. That is evidence, not proof, on six events — I am not claiming more.

## ⚑ Where I was wrong about drax a second time, and it is the session's recurring shape

I first computed the FAIL sets with an exact string match and got **0** (rows 1–2) and **1** (rows 3–8), against his reported **4** and **3**. I widened before concluding anything, and he is right on both: his figures are the **`PASS == false` booleans** — `M_C3_prime_static_arm.PASS` ×4, and `PASS_teleport_zero` / `PASS_negative_space_preserved` / `PASS_no_authored_px_inside` ×3. **He counted failing checks, which is the correct referent. My detector was narrower and would have convicted a correct builder** — the third time this session a mismatched instrument nearly did that.

**One figure of mine to correct too:** the "988 numeric moves" counts numbers *typed as numbers*. Two more moved **inside prose strings** (`peak added luma 0.5072 → 0.5053`, `0.2691 → 0.2681`). The true count is **990**. `#64`, on my own arithmetic.

## What I am asking of you, unchanged in kind

Questions 1–3 at the head of this file still stand. The recapture **does not answer them** — it re-poses question 1 more sharply:

> **Does a sealed verdict hold when a re-derivation shows its inputs moved by up to 97.8%, its measured zeros were artefacts, and its verdict statistic is one that could not have registered any of it?**

I can argue that both ways and I still do not think a conductor should pick. **Rule it by name.** drax surfaced this, declined to rule it, has now had the measurement taken out from under his own session mid-flight, and still has no answer.

---

## Cross-references

`reincarnated-godot` `2afde08` (drax, tag retraction — the source), `612c1e3` / `1c4f90f` / `689116c` (the fix that closes the defect forward), `a1690fe0` (galadriel, the original facing finding); `qa/pending/2026-08-25-r-l93-4-is-a-forward-dangling-pointer-into-a-corpus-write-in-flight.md` (the same compensating control, first firing); dispatches `2026-08-25-drax-forward-axis-and-cathedral-default.md` § MATT'S VERDICT, `2026-08-25-drax-camera-framing-and-wwab-render.md`, `2026-08-25-drax-s2c-3a-recapture.md` (`3e821786`, the dispatch this section returns).
**Artefacts:** `reincarnated-godot/harness_logs/s2c_rows{12,38}_2026-08-25{,-v3v3}/gate.json`; `…/app_userdata/reincarnated-godot-spike/s2c{12,38}v3{,b}`; `/tmp/s2c_recapture_logs/orchestrator.log`.
