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

## Cross-references

`reincarnated-godot` `2afde08` (drax, tag retraction — the source), `612c1e3` / `1c4f90f` / `689116c` (the fix that closes the defect forward), `a1690fe0` (galadriel, the original facing finding); `qa/pending/2026-08-25-r-l93-4-is-a-forward-dangling-pointer-into-a-corpus-write-in-flight.md` (the same compensating control, first firing); dispatches `2026-08-25-drax-forward-axis-and-cathedral-default.md` § MATT'S VERDICT, `2026-08-25-drax-camera-framing-and-wwab-render.md`.
