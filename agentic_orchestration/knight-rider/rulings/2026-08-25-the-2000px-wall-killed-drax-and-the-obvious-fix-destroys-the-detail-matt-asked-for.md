# knight-rider ruling — the 2000px image wall killed a 20-minute drax run, and **the obvious remedy would destroy the exact detail Matt asked us to look for**

**Filed:** 2026-08-25 (knight-rider). **Class:** operational constraint + method ruling. **Severity:** ⚑ **binds every frame-analysis dispatch from here on.**
**Occasioned by:** the death of the drax "camera framing and WW-AB render" run (agent `a841d50c9f09d2d39`), and Matt's instruction that occasioned that run in the first place.

---

## What happened

The run executed **126 tool calls over ~20 minutes** and then died. The status reported `completed`. **It had not completed** — the "result" was an API error string:

```
400 invalid_request
messages.1.content.128.image.source.base64.data:
At least one of the image dimensions exceed max allowed size
for many-image requests: 2000 pixels
```

⚑ **Note `content.128`.** The agent had accumulated ~128 image blocks. The request died not on the first oversized image but on the one that broke the camel's back in a **many-image** request — which is why it survived 126 calls and then failed all at once, with no warning and no partial return.

**The run's actual work survived, uncommitted, in a shared working tree** — including a derivation that overturned a cited camera pose by measuring the reference video's ground-ring projections. A separate recovery dispatch exists to get it committed. **The work was good; the container failed.**

## ⚑ The trap: the instruction and the constraint point in opposite directions

Matt's words:

> *"Drax and Galadriel both need to **zoom in and pause more on each individual frame** … we should probably try calling Codex and Grok for second opinions … all of this can be found in the originals if we **slow it down and statistically pick each clip apart**."*

**"Zoom in more" and "pick each clip apart" both push toward MORE images at HIGHER detail. The API constrains exactly those two axes simultaneously.** Following the instruction naively is what killed the run. This is not a case where the constraint is an annoyance to route around — **it is aimed directly at the requested method.**

## The ruling: **CROP. Do not DOWNSCALE.** They are not interchangeable, and the difference decides the whole investigation.

The reflexive fix is `sips -Z 1600` — downscale until it fits. **For this investigation that fix is worse than the crash**, because of what it removes:

| | What it does to a 3840px frame | What happens to the thing we are hunting |
|---|---|---|
| **Downscale to 1600** | keeps the whole frame, **discards ~83% of the pixels** | thin laser filaments, metal-scrape sparks, smoke wisps, cavitation edges are **1–3 px features. They are averaged out of existence.** |
| **Crop to 1600** | keeps a region, **preserves every pixel in it at native resolution** | the fine structure survives exactly as rendered |

⚑ **A downscaled frame does not merely show less — it systematically hides the specific class of detail Matt is asking whether we have.** Matt's thesis is that the originals contain internal VFX depth our versions lack. **Downscaling would erase that depth from the originals and from ours at the same rate — and the comparison would come back "no meaningful difference."** That is a false null produced by the instrument, and it would be indistinguishable from a real one.

**This is flank 3 again** — the SUBJECT flank from the sealed-verdict filing. Full coverage, faithful bytes, procedure repeatable, **and the thing rendered is not the thing under investigation.** Third appearance of that shape this session.

## Standing method for frame-analysis dispatches

1. **Crop to a region of interest at native resolution.** Both dimensions **< 2000px**. Never downscale a frame whose fine detail is the subject.
2. **Budget the image count explicitly in the dispatch.** ~128 blocks was the observed death point; treat **well under 100** as the working ceiling and say so in the brief. A dispatch that says "examine every frame" is a dispatch that dies.
3. **Never modify an original.** Crop to a copy. The originals are evidence — and this wave has already had one near-miss where a re-run command would have silently deleted the sole surviving pre-fix frame set.
4. **Prefer many small crops over few large frames.** This is the direction the constraint and Matt's instruction actually agree on: tight crops at native resolution *are* "zooming in."
5. **Split by pass, not by resolution.** If a clip needs more looking than one context can hold, that is **two dispatches**, not one degraded dispatch.

## ⚑ A correction I am making against my own dispatch, filed before I had thought this through

The recovery dispatch I sent drax minutes ago tells him to `sips -Z 1600` before viewing any image. **For that dispatch specifically it is harmless** — it is a commit-and-report task that needs almost no images, and it needs to not die. **But the instruction is wrong as a general rule and I wrote it as though it were one.** I reached for the fix that prevents the crash without asking what it costs, which is the same move that produced "probably moot" an hour earlier: **treating the first plausible remedy as the answer because it resolves the visible symptom.**

This file is the general rule. **Where the two conflict, this one governs.**

## Applies to galadriel, right now, and I cannot warn her

The galadriel frame-forensics run (`a10a8326e5e69d310`) is **live as I write this** and is doing precisely the high-volume frame inspection that triggers this wall. Checked: **no error signature in her output yet.**

**`SendMessage` is unavailable — seventh confirmation this session — so she cannot be warned mid-flight.** The compensating control is the same as every other time: file by record. If her run dies the same way, this file is the explanation and her work will be recoverable the same way drax's was, **provided nobody discards a dirty tree in the interim.**

## Cross-references

drax agent `a841d50c9f09d2d39` (the death); the recovery dispatch to drax; `qa/pending/2026-08-25-reproducibility-is-not-validity-…md` (flank 3 — the SUBJECT flank); `knight-rider/rulings/2026-08-25-codex-and-grok-are-not-symmetric-…md` (the other half of Matt's second-opinion request).
