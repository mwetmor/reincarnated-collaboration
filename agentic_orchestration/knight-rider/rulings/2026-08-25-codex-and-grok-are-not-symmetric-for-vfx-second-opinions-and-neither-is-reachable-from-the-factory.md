# knight-rider ruling — Matt's "call Codex and Grok for second opinions" on the VFX frames is **not executable as framed**, and the two lanes are **not the same shape**

**Filed:** 2026-08-25 (knight-rider). **Class:** capability finding + disposition on a standing Matt request.
**Occasioned by:** Matt, this session — *"we should probably try calling Codex and Grok for second opinions… all of this can be found in the originals if we slow it down and statistically pick each clip apart."*

> ## ⛔ CORRECTED AT SOURCE — same session, by star-lord's live measurement (`18c64165` / `21076f74`). **THE CENTRAL FINDING OF THIS RULING IS WRONG. Matt's request IS executable, on BOTH lanes.**
>
> **I ruled that Grok "has no image door at all." That is true of the FLAG SURFACE and false of the CAPABILITY.**
>
> `grok --prompt-json` accepts **ACP content blocks**, and `image` is one of them — `{"type": "image", "data": "<base64>", "mimeType": "image/png"}`. **Both lanes were probed live against a decoy PNG built so a hallucination would show:** 640×300, blue square upper-left, red circle lower-right, strings `VXQ-7413` and `SEVEN SPOONS`. ⚑ **Both models returned both strings verbatim and both shapes in their correct corners.** Codex `-i/--image` is now emitted and verified end-to-end against the live vendor with the argv the harness actually produces.
>
> ⚑ **Eighth instance of my own trigger this session, and the most on-the-nose of them: `--help` OUTPUT — a LISTING — stood in for the CAPABILITY, and I did not register that a substitution had occurred.** I ran a real command and quoted its real output. **The output was accurate and the inference from it was not.** My own check table says *the name is not the referent*; the same holds one level up — **a flag surface is not a capability surface, and absence from a `--help` listing is not absence from an API.** The refuting probe costs **$0.00** because it fails at argv parse, and **the CLI documents its own vocabulary in the rejection**: `unknown variant 'image_url', expected one of 'text', 'image', 'audio', 'resource_link', 'resource'`. **One command would have told me. I wrote a ruling instead.**
>
> ⚑ **What this changes downstream, and it is not small.** gandalf's VFX-depth ruling (`b8d8cae9`) lists **"I viewed ZERO frames"** as his first blind spot, and Grok's return names it real-but-smaller. **That blind spot is now closeable on both lanes.** Matt's request was *"Drax and Galadriel both need to zoom in and pause more on each individual frame… we should probably try calling Codex and Grok for second opinions"* — **frame-level, and now reachable.** *(gandalf's § 7.2 caution — that a second model shown frames produces an IMPRESSION, and a fourth prior is not a control — stands on its own merits and is not overturned by this. **But that was his design judgement about where to point it, not a capability limit, and I had been treating my error as corroborating his judgement.** Two independent reasons collapsed into one, and one of them was false.)*
>
> ⚑ **Live hazard flagged by star-lord for whoever gets the wiring dispatch:** `--prompt-json` **DISPLACES `-p`**, so the prompt leaves argv entirely — and `MAX_PROMPT_ARGV_BYTES`, the ceiling `build_argv` refuses against, **stops measuring the right thing the moment base64 joins the payload.** A 640×300 PNG is 11.8 KB of JSON. **A VFX frame is not.** Composes with the `2000px` wall ruling (`knight-rider/rulings/2026-08-25-the-2000px-wall-killed-drax-…md`): **crop at native resolution, never downscale** — and now **also budget the base64 against a ceiling that is no longer watching.**
>
> **The table below is left standing with its error intact. It is the artifact of the mistake, and rewriting it would hide what a `--help` listing did to a ruling.**

**Disposition: ~~DEFERRED-WITH-ROUTE~~ → ⚑ EXECUTABLE ON BOTH LANES.** The request is sound and the finding does not touch its merit — **and the finding itself was half wrong.**

---

## The request presumes a symmetry that does not exist

Matt named Codex and Grok in one breath, as two interchangeable second opinions. **They are not interchangeable for this task**, and the difference is not a matter of quality — it is that **one of them has no door for an image at all.**

| Lane | Vendor CLI accepts an image? | Reachable through `factory/harness/`? |
|---|---|---|
| **Codex** | ✅ **`-i, --image <FILE>...`** — *"Optional image(s) to attach to the initial prompt"* | ❌ **no** — `build_argv` never emits it |
| **Grok** | ❌ **no `--image` flag exists** | ❌ **no** |

Both measured this session, first-hand, not recalled:

```
$ codex exec --help | grep -i image
  -i, --image <FILE>...
          Optional image(s) to attach to the initial prompt

$ grok --help | grep -i "image\|prompt-json"
      --prompt-json <JSON>          # ← the ONLY candidate; no --image anywhere in the flag surface
```

## The factory floor is text-on-argv, both lanes, no exceptions

```
$ grep -n "image\|vision\|attach\|png\|base64\|prompt-json" factory/harness/*.py
(no output)
```

**Zero hits across every harness file.** The two `build_argv` bodies confirm it:

- `factory/harness/grok.py` → **`build_argv`** → `argv = [binary, "-p", prompt, "--output-format", "json"]` (+ `--no-leader`, `-m`, `--reasoning-effort`, `--permission-mode`, `--disable-web-search`, `--allow`/`--deny`, `--max-turns`)
- `factory/harness/codex.py` → **`build_argv`** → `argv = [self.executable, "exec", "--json"]`

⚑ **Cited by SYMBOL, not by line — and that correction was forced within twelve minutes of filing.** This file first said `grok.py:733`. star-lord's `7837ade3` (the transient-auth debounce) landed in the same file minutes later and moved it to **732**. The finding was untouched; the pointer to it rotted immediately.

**A line number is a claim about a file's current state, and it decays silently every time anyone commits to that file.** Nothing errors, nothing warns — the citation just quietly starts pointing one line off, and the next reader either shrugs or chases a phantom. `build_argv` will still be `build_argv` after the next fifty commits. **Same family as `#75` cl. 6 and as the `git diff HEAD~1` defect: an instrument that keeps returning cleanly after it has stopped answering the question.**

⚑ **The Codex row is the one worth pausing on.** Codex is **capable at the vendor and unreachable through the factory** — the flag exists, the model accepts it, and the only reason a frame cannot get to it is that our own `build_argv` does not emit it. That is a **one-line-ish harness change in a seam I do not own**, not a capability gap. It would have been easy to report "Codex can't see images" and be wrong in the direction that closes the door.

## Grok's only candidate door is UNTESTED, and I am not going to assume it

`--prompt-json <JSON>` — *"Single-turn prompt as JSON content blocks."* **Content blocks** is the vocabulary that image inputs normally travel in, so this is a **plausible** door. It is not a demonstrated one.

**I have not tested whether `--prompt-json` accepts an image block, and I am not claiming it does.** Per `#79` cl. 6, a mechanism claim carries an empirical-test obligation *before relay* — and this is exactly the shape of claim that gets relayed as fact because it sounds like one. The cheapest refuting test is a single `grok --prompt-json` call with one image block and a trivial prompt: it either returns a description of the image or it errors. **One call settles it.**

**That test is star-lord's to run, not mine** — `factory/harness/` is his seam, and the finding is only useful to him if it arrives as a question rather than as an answer I invented.

## What this changes in the record

**Handoff SESSION 3, decision item 4** currently reads *"Probably moot; do not answer yet"* — on the premise that the in-flight Grok auth fix dissolves the question. **That premise is now known to be incomplete.** Auth and vision are independent failures: **a fully-repaired auth lane still cannot show either model a frame.** Fixing the credential cascade gets Grok answering text prompts; it does nothing about the image path. The item is not moot; it is two items, and only one of them is in flight.

## Route

1. **star-lord** — (a) run the one-call `--prompt-json` image-block probe and record the result either way; (b) if Codex-only is acceptable, emit `-i/--image` from `codex.py` `build_argv`, which is the smaller of the two changes and unblocks half the request immediately.
2. **knight-rider** — do not author the VFX second-opinion dispatch until (1a) returns. Authoring it now would pre-commit to a two-lane comparison that may only have one lane, and a comparison missing an arm is the failure shape this wave has already paid for twice.
3. **Matt** — nothing needed. The request stands; it is queued behind a capability, not behind a decision.

## What is NOT affected

The **depth critique itself** — that the current VFX are basic representations lacking the internal detail of the originals (metal-scrape timing, intermittent lasers cycling a colour range, smoke, wind, cavitation / gravity-distortion) — is a **design finding that needs no external model to act on.** It routes to gandalf and drax on its own merits. The second-opinion lane was proposed as *corroboration*, and corroboration being unavailable is not a reason to hold the underlying observation. **Do not let this finding become a reason the depth critique waits.**

## Cross-references

`factory/harness/grok.py:733`, `factory/harness/codex.py:342`; handoff `skill_handoff_2026-08-25.md` § SESSION 3 decision item 4; in-flight star-lord Grok transient-auth cascade dispatch; `#79` cl. 6 (mechanism claims carry an empirical-test obligation before relay).
