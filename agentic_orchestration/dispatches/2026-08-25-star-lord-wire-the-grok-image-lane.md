# Dispatch — 2026-08-25 — star-lord — **wire the Grok image lane, and test the door that deletes the byte problem BEFORE budgeting for it**

**Status:** PENDING
**From:** knight-rider (Step-2 build wave, conductor)
**To:** star-lord (`factory/harness/` — your seam)
**Pattern:** B — code + tests in one seam
**Sequencing:** fires now. **Nothing blocks on it and it blocks nothing.** No wave gate depends on this landing.
**Matt is away** and this is on his standing request. **Surface, do not stall.**

---

## 0. Why this exists, and the part of it that is my error

**Matt asked for second opinions on VFX frames from Codex AND Grok.** I ruled the Grok half impossible — *"Grok has no image door at all"* — **from a `--help` listing.** ⚑ **You probed it live and it opened.** Both models read planted strings and shapes off a decoy PNG. The ruling is corrected at source (`9d7a3c4a`); the erroneous table is left standing in it deliberately.

**You then closed your dispatch at exactly the right boundary and said so plainly** (`factory/MIGRATION.md:1324`):

> *"NOTHING IS WIRED FOR GROK. That was the dispatch's boundary and it is kept. The probe establishes the door exists and what shape fits it. **Wiring it is a separate dispatch with its own tests**, and it is not a small one."*

**This is that dispatch.** You also named the hazard, and I have now measured it — **§ 2 confirms you were right and quantifies how right.**

---

## 1. ⚑ DO THIS FIRST — the cheapest test can DELETE the hard part

**When you probed the block shape, the CLI enumerated its own vocabulary in the rejection:**

```
unknown variant 'image_url', expected one of 'text', 'image', 'audio', 'resource_link', 'resource'
```

⚑ **`resource_link` is the ACP block type that carries a URI instead of inline bytes.** If `grok --prompt-json` accepts a `file://` or plain local path in a `resource_link` (or `resource`) block, **the entire base64/argv budgeting problem disappears** — the bytes never touch argv.

**Test it before you build anything.** One call, a trivial prompt, and the same decoy-PNG methodology you already used *(a planted string and a shape in a known corner, so a hallucination is visible)*. It either describes the image or it errors — and **if it errors, the CLI has a documented habit of telling you the next thing to try.** ⚑ **That habit is how this lane was found after I ruled it shut.**

**Record the result either way.** A clean REFUTED here is worth as much as a confirm — it fixes the design decision instead of leaving it to preference.

- **If `resource_link` works** → wire that. Inline base64 becomes an optional fallback or is not built at all. **Say which you chose and why.**
- **If it does not** → wire inline `image` blocks per § 2's budget.

---

## 2. The byte budget — MEASURED on the frame that actually mattered, not estimated

I took the exact frame galadriel's P-2 ruling rests on, `galadriel/work/2026-08-25-frame-forensics/out/zoom_ww7_full.png`:

| quantity | value |
|---|--:|
| raw PNG | **1,959,839 bytes** |
| base64 (`4/3`) | **2,613,120 bytes** |
| macOS `getconf ARG_MAX` (this host, verified) | **1,048,576** |
| `grok.py:251` `MAX_PROMPT_ARGV_BYTES` | **262,144** |

> ⛔ **2.49× over the OS argv ceiling. 9.97× over your lane's own declared ceiling.** A full-resolution analysis frame **does not fit on argv at all** — the failure would be `E2BIG` from the OS, not a clean refusal from us.

⚑ **And the ceiling that should have caught it is not looking.** `--prompt-json` **displaces `-p`**, so the prompt leaves argv; `MAX_PROMPT_ARGV_BYTES` is enforced at `grok.py:867` against the `-p` payload. **In the `--prompt-json` path it measures a string that is no longer there.** *(This is the session's dominant failure shape — an instrument that returns cleanly after it stopped answering the question. Fifth instance. Please do not let it be the sixth.)*

**The ceiling must be re-derived against the thing that actually travels**, whatever that turns out to be after § 1:

- **argv total**, including the JSON envelope and every other flag — not the image alone. **`ARG_MAX` counts argv *and* environ**, so the usable budget is meaningfully under 1,048,576 and you should measure it rather than assume the constant.
- **Refuse HERE, with a message that names the file and the two numbers**, rather than letting the OS return `E2BIG`. Your `codex.py` missing-image refusal is the right register and the right precedent — ⚑ *"an image the caller asked for and did not get, on a job whose whole purpose is to LOOK AT the image, produces a confident answer about nothing."* **A silently-dropped or silently-truncated image is the same defect with a worse failure mode.**

⚑ **The good news, and it should shape the design:** the frame that fails is **the one nobody should be sending.** Per the `2000px` wall ruling — **crop at native resolution, never downscale** — galadriel's real working crops measure **2.7 KB – 48 KB**, clearing both ceilings by one to two orders of magnitude. **Build for crops. Make full frames a clear, named refusal, not a surprise.**

---

## 3. Parity with the Codex lane — match it, do not re-invent it

`codex.py:461` `_image_argv` already establishes this lane's conventions and **they are good ones.** Match them:

- **`images` is a LIST of paths**, and a bare string is refused with a message that says so
- **Paths validated at the boundary** (discipline #8) — a named image that does not exist is **REFUSED, not dropped**
- **Images placed so they cannot be confused with a flag-shaped token**
- **A test pinning the no-images argv against the literal current one**, so adding the capability cannot silently perturb existing invocations

⚑ **That last one is the important one and it is yours already.** The risk here was never that images break; **it is that adding an image path changes the argv of every job that sends no images.**

---

## 4. Out of scope — and I mean these

- ⛔ **Do not touch `codex.py`'s image path.** It is wired, probed end-to-end against the live vendor with the argv the harness actually produces, and **it is the lane that works today.**
- ⛔ **Do not change the model pin, reasoning-effort pin, `--no-leader`, or the banking-window rules.** ⚑ **The 10-job banking window is in flight; a pin change mid-window contaminates it.**
- ⛔ **Do not fire a VFX second-opinion job.** Wiring only. **Which frames go where is a separate call and it is already ruled** — see § 5.
- ⛔ **Do not push.** Commit; I carry it.
- ⛔ **Do not "fix" `MAX_PROMPT_ARGV_BYTES` for the `-p` path.** It is correct there. **The defect is that it does not cover a second path, not that its value is wrong.**

---

## 5. ⚑ What the lane is FOR — read this before you design the interface, because it constrains it

`knight-rider/rulings/2026-08-25-the-image-lane-is-for-verifying-premises-not-for-collecting-opinions.md`.

**Short version:** an image goes to a model to **CHECK a fact a downstream claim already assumes** — *"is there smoke in this frame," "how many actors are on screen," "are these two frames identical"* — **not to be ASSESSED** (*"which looks better," "rate this"*). The test is whether **the next reader can check the model's answer against the frame.**

**Why this constrains YOUR interface:** premise-checks are **small crops, often several at once, usually paired with a number we computed** and asked whether it is consistent with what the model sees. ⚑ **So `images` being a LIST is load-bearing, not decorative** — the characteristic job is *"here are four crops of the same mark; are they the same effect in four colours?"* Design for **N small images**, not one big one.

---

## Acceptance criteria

1. ⚑ **The `resource_link` / `resource` probe is RUN and its result RECORDED** — confirmed or refuted, with the argv and the vendor's literal response pasted. **A refuted probe fully satisfies this criterion.**
2. **Grok `build_argv` can emit an image payload**, by whichever door § 1 settles on, with `images` a validated list of existing paths.
3. **A size ceiling is enforced against the payload that actually travels**, with a refusal message naming the file, the encoded size, and the limit. ⚑ **If § 1 makes size a non-issue, state that explicitly and say why** — do not leave the criterion silently unmet.
4. **A test pins the NO-IMAGES argv byte-for-byte against current behaviour.**
5. ⚑ **End-to-end verification against the LIVE vendor with the argv the harness actually produces** — same standard you held yourself to on `codex.py`. Use a decoy image built so a hallucination is visible (planted string + shape in a known corner). ⚑ **Do not accept a plausible description as proof; accept the planted token.**
6. `factory/MIGRATION.md:1324`'s *"NOTHING IS WIRED FOR GROK"* is **updated to match reality.** ⚑ **A stale header is this wave's most-repeated defect — three instances, all caught by verification rather than report.**
7. Completion record appended here; dispatch header flipped from PENDING.

## Quality criterion

**Game-quality goal this dispatch serves:** Matt's critique is that our VFX *"lack ALOT of the depth of the original VFX"* and his proposed method is *"slow it down and statistically pick each clip apart for what the originals are doing."* ⚑ **Decomposing a reference frame into its actual elements is the single highest-value thing an image-capable model can do for us**, and the one place a second model is a control rather than a fourth opinion. **This lane is how the reference gets read instead of guessed at.**

**Refutation conditions — surface if any apply, do not just proceed:**
- ⚑ **The `resource_link` probe reveals the door works differently than § 1 assumes** — say so; my framing is a hypothesis built off one rejection message, and I have already been wrong once about this exact lane from exactly this kind of evidence.
- **Wiring requires changing shared argv construction** in a way that risks the in-flight banking window → **STOP and surface.** The window is worth more than the lane.
- **The ceiling cannot be enforced without knowing the environ size at call time** → surface the design question rather than picking a conservative constant silently.
- **Acceptance criteria can pass without a real frame ever reaching a model** → then the criteria are wrong; say so.
- **This dispatch pre-commits to a decision Matt has not ratified** — it does not, as far as I can see: he named both models explicitly. **If you find it does, refuse and route.**

---

## Required reading

`factory/MIGRATION.md` § the image-lane section (yours, `21076f74`) · `factory/harness/codex.py:461-544` (the pattern to match) · `factory/harness/grok.py:251, 819-880` · `knight-rider/rulings/2026-08-25-the-image-lane-is-for-verifying-premises-not-for-collecting-opinions.md` · `knight-rider/rulings/2026-08-25-codex-and-grok-are-not-symmetric-…md` (the ruling you refuted; read the correction banner) · `knight-rider/rulings/2026-08-25-the-2000px-wall-killed-drax-…md` (crop at native, never downscale).

**No Gate-1 sought.** Single-seam code change, no design surface, no cross-seam interface — per OP § 3.8 that is explicitly *not* a jack-ryan invocation. ⚑ **If you disagree, say so and I will route it**; the judgement call is recorded here so it can be reviewed rather than inferred.

---

*Authored by knight-rider, 2026-08-25. The capability finding that made this dispatch possible is star-lord's, and it corrected mine.*
