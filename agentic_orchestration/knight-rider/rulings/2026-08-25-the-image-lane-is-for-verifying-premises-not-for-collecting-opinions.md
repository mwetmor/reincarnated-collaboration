# knight-rider ruling — **the image lane's job is VERIFYING A PREMISE, not COLLECTING AN OPINION** — and galadriel just demonstrated the difference at a cost of one frame

**Filed:** 2026-08-25 (knight-rider). **Class:** usage ruling on a newly-opened capability + measured capacity finding.
**Occasioned by:** Matt — *"Drax and Galadriel both need to zoom in and pause more on each individual frame. In fact, we should probably try calling Codex and Grok for second opinions… all of this can be found in the originals if we slow it down and statistically pick each clip apart."*

---

## The tension this resolves, and it is a real one between two agents who are both right

**gandalf, § 7.2 of his depth ruling** — refusing to point a second model at frames:

> *"A second model shown frames produces an **IMPRESSION**, and impressions are exactly what galadriel's instrument was built to replace. **A fourth prior is not a control.**"*

**He is correct, and I acted on it** — Grok was fired at his ruling rather than at the frames, and it landed five hits it could not have landed from pixels.

**And in the same hours, galadriel consumed exactly ONE image block and it carried the load-bearing ground of a ruling that killed a property.** Both of these are true. **They are not in conflict, because they are different uses of the same door**, and nobody had separated them:

| | **OPINION GENERATION** (gandalf's warning) | ⚑ **PREMISE VERIFICATION** (galadriel's use) |
|---|---|---|
| Question asked | *"What do you think of this VFX?"* | *"Does this clip actually contain a volumetric smoke cloud?"* |
| What comes back | a judgement | **a fact the asker's statistics already depended on** |
| Falsifiable? | not really — it is a prior | ⚑ **yes, and by looking** |
| Fails how? | quietly, by agreeing with whoever framed it | loudly — the premise is there or it is not |
| Cost of being wrong | a fourth prior enters the record wearing evidence's clothes | **the ruling that rests on it collapses, visibly** |

> ### **The rule: an image goes to a model to CHECK something a downstream claim already assumes. It does not go to a model to be ASSESSED.**

## The worked example, because it is not hypothetical

galadriel's P-2 ruling (`03213dd5`) turns entirely on one claim: **ww7 genuinely contains volumetric content.** If it does not, her whole ground A — *the clip with the volume scores finer than the reference* — is vacuous.

**She could not settle that with a statistic. That is the point: the statistic is what is on trial.** So she opened `zoom_ww7_full.png` at **native 1920×1080, no downscale**, and reported what was there:

> *"A grey volumetric cloud occupies roughly a quarter of the frame's central area — soft-edged, internally varying, unmistakably a volume and not a card. It sits directly on top of one thin orange melee arc."*

⚑ **One image. Not an opinion about quality. A yes/no about the contents of a frame, on which a measurement's meaning depended** — and it also caught the **~344 actors** error, because she counted six or seven humanoids while she was in there.

⚑ **And the contrast is in the same document set.** gandalf's own first-listed blind spot is ***"I viewed ZERO frames."*** He ruled correctly anyway — but the number he inherited and propagated (`344`) was one **a single glance refutes**, and it then travelled into Grok's Hit 4 and into a Matt-facing decision doc before anyone looked. **Four readers in a chain; the frame was checked at the fourth.**

## What this licenses, and what it still forbids

**LICENSED — send frames for:**
- **Premise checks.** *"Is there smoke in this frame?" "Are these two frames identical?" "Is the character facing the camera?" "How many actors are on screen?"* ⚑ **Matt's own request is mostly this shape** — *"zoom in and pause more on each individual frame… statistically pick each clip apart for what the originals are doing"* is an inventory question about **contents**, not a request for taste.
- **Reference decomposition.** *"List every distinct visual element you can identify in this frame of the D3 Whirlwind."* An inventory is checkable against the frame by the next reader.
- ⚑ **Adversarial premise-checking of our OWN receipts** — hand a model the frame *and* the number we computed from it and ask whether the number is consistent with what it sees. **That is a control, not a prior.**

**STILL FORBIDDEN — do not send frames for:**
- *"Which of these looks better?"* · *"Rate the VFX quality"* · *"What should we add?"* ⚑ **These produce a fourth prior, gandalf is right about them, and the ruling that says so is not overturned by this one.**
- **Any use where the model's answer cannot be checked against the frame by the next reader.** That is the test, and it is the whole test.

## ⚑ The capacity finding — MEASURED, and the naive wiring CANNOT carry the frame that mattered

I did not estimate this. `zoom_ww7_full.png` — **the exact frame galadriel's ruling rests on:**

| quantity | value |
|---|--:|
| raw PNG | **1,959,839 bytes** |
| base64 (`4/3`) | **2,613,120 bytes** |
| macOS `getconf ARG_MAX` | 1,048,576 |
| `grok.py:251` `MAX_PROMPT_ARGV_BYTES` | 262,144 |

> ⛔ **2.49× over the operating system's argv ceiling. 9.97× over the lane's own declared ceiling.** A full-resolution analysis frame **does not fit on argv at all**, and `--prompt-json` **displaces `-p`**, so the lane's ceiling — the one `build_argv` refuses against — **is not even looking at the payload that would blow it.** *(An instrument returning cleanly after it stopped answering the question. Fifth instance this session; I have stopped being surprised by it.)*

**This composes with the `2000px` wall ruling — and the composition is the good news, not the bad.** That ruling says **crop at native resolution, never downscale.** ⚑ **Cropping is exactly what fixes this**: galadriel's actual working crops measure **2.7 KB – 48 KB**, which clear both ceilings by one to two orders of magnitude. **The frame that fails is the one nobody should have been sending anyway.**

⚑ **And there is an untested door that may sidestep argv entirely.** When star-lord probed the shape, the CLI **enumerated its own vocabulary in the rejection**: `unknown variant 'image_url', expected one of 'text', 'image', 'audio', `**`'resource_link'`**`, 'resource'`. **`resource_link` is the ACP block type that carries a URI rather than inline bytes.** If it accepts a local path, the ceiling stops mattering for every frame size. **Cost of finding out: one call that fails at argv parse for $0.00, and the CLI documents the next step in its own error message — which is how the image door was found in the first place, after I ruled it shut from a `--help` listing.**

## State of the two lanes — verified against the tree, not recalled

| Lane | Vendor capability | **Wired in `factory/harness/`?** |
|---|---|---|
| **Codex** | `-i, --image <FILE>...` | ✅ **YES** — `codex.py:461` `_image_argv`, path-validated at the boundary, **refuses** a missing file rather than dropping it *(«an image the caller asked for and did not get, on a job whose whole purpose is to LOOK AT the image, produces a confident answer about nothing»)* |
| **Grok** | `--prompt-json` ACP `image` block, **probed live against a decoy PNG and it read both planted strings and both shapes in their correct corners** | ⛔ **NO** — `build_argv` still emits `-p` only. star-lord kept the boundary deliberately and said so at `factory/MIGRATION.md:1324`: *"NOTHING IS WIRED FOR GROK. That was the dispatch's boundary and it is kept."* |

**Matt named both models. One lane is open and one is proven-but-shut.** Wiring dispatch follows.

## Route

1. **star-lord** — wire the Grok image lane. ⚑ **Test `resource_link` FIRST** — if a URI block works, the byte problem is deleted rather than budgeted.
2. **galadriel / drax** — the licensed uses above are available on the Codex lane **now**, no dispatch needed. **Crops, not full frames.**
3. **gandalf** — his § 7.2 caution is **narrowed, not overturned.** The distinction is premise-verification vs opinion-generation, and **his own blind spot is the strongest argument for the first half of it.**
4. **Matt** — nothing needed.

## Cross-references

`galadriel/notes/2026-08-25-p2-scale-composition-instrument-ruling.md` § 2 (the worked example) · `gandalf/findings/2026-08-25-vfx-depth-design-ruling.md` § 7.2 + § 9 blind spots · `knight-rider/rulings/2026-08-25-codex-and-grok-are-not-symmetric-…md` (the ruling this supersedes the pessimism of) · `knight-rider/rulings/2026-08-25-the-2000px-wall-killed-drax-…md` (crop, never downscale) · `factory/MIGRATION.md:1324` · `factory/harness/codex.py:461`, `factory/harness/grok.py:251`.
