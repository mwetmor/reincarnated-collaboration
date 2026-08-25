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

## Cross-references

`reincarnated-godot` `2afde08` (drax, tag retraction — the source), `612c1e3` / `1c4f90f` / `689116c` (the fix that closes the defect forward), `a1690fe0` (galadriel, the original facing finding); `qa/pending/2026-08-25-r-l93-4-is-a-forward-dangling-pointer-into-a-corpus-write-in-flight.md` (the same compensating control, first firing); dispatches `2026-08-25-drax-forward-axis-and-cathedral-default.md` § MATT'S VERDICT, `2026-08-25-drax-camera-framing-and-wwab-render.md`.
