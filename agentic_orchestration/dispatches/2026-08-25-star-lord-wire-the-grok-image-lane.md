# Dispatch — 2026-08-25 — star-lord — **wire the Grok image lane, and test the door that deletes the byte problem BEFORE budgeting for it**

**Status:** COMPLETE (2026-08-25, star-lord — see Completion record)
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

---

## Completion record

**Completed:** 2026-08-25 — star-lord. **Full write-up:** `factory/MIGRATION.md` § 14 (image-lane v1).
**Commit:** see `factory/harness/grok.py`, `factory/tests/test_grok_harness.py`, `factory/tests/test_vocabularies.py`, `factory/MIGRATION.md`.
**Not pushed** (per § 4). **No VFX job fired** (per § 4). **`codex.py` untouched** (per § 4). **Pins, `--no-leader` and banking-window rules untouched** — the window is still at **1 banked job** and none of my 8 live calls wrote a `_run-log.tsv` row.

### ⚑ § 1 first, as instructed — and it neither confirmed nor cleanly refuted

**`resource_link` WORKS.** Both `file://` and a plain absolute path returned correct comprehension of a decoy PNG (planted `KZR-9082` / `ELEVEN LANTERNS`, green triangle lower-left, orange square upper-right — all read back correctly). The bytes really do leave argv.

**And I wired the inline `image` block instead.** The reason is one probe you did not ask for and I would not have run if § 1 hadn't told me to record the argv and response either way:

> ⛔ **A `resource_link` naming a file that DOES NOT EXIST returned `rc=0`.** The CLI never looked at the path. A full model call was launched and **paid for — $0.0061, 28 seconds** — and the *model* discovered at runtime that the file was missing. It replied `NOIMAGE` **only because my probe prompt instructed it to.** Without that instruction it answers fluently and confidently about nothing.

**`resource_link` is not an attachment. It is a pointer the model resolves with its own file-read tool** (`num_turns: 2` vs `1`; the model's own `thought`: *"Let me read the image first"*; and the rc=0 above). Consequences: **1.7×–2.5× the cost** for an identical answer ($0.0075–$0.0112 vs **$0.0045**), **more** context not less (17.5 K / 31.9 K input tokens vs 11.5 K), correctness dependent on the agent's tool fence and `cwd` — surfaces this lane deliberately does not control — and it breaks under `max_turns: 1`. Inline is one turn, cheapest, deterministic, and **refusable at the boundary for free.**

**What in your § 1 framing turned out wrong — you asked, so plainly:** the framing was *"if it accepts a URI, the byte problem disappears."* It accepts a URI **and the byte problem does not disappear.** It relocates into the context window, gets more expensive, and **takes the boundary refusal with it on the way out.** The half that was right is the half that found the door twice now: **the CLI's rejection message is a reliable map of its vocabulary.** Trust that habit; don't trust that a named block type means what its name suggests.

**Literal vendor responses and every argv are recorded in § 14.1 and § 14.8.**

### Acceptance criteria

| # | | |
|---|---|---|
| 1 | probe RUN + RECORDED | ✅ § 14.1 — four `resource_link` variants, argv + literal responses + the rc=0 |
| 2 | `build_argv` emits an image payload, `images` a validated list | ✅ § 14.2 — `--prompt-json` + inline ACP `image` blocks |
| 3 | ceiling against the payload that actually travels, naming file/size/limit | ✅ § 14.3 — **and size DID end up mattering** |
| 4 | no-images argv pinned byte-for-byte | ✅ against a hand-written literal, not a re-derivation |
| 5 | live E2E with the argv the harness actually produces | ✅ § 14.6 — through `GrokHarness.run()` itself, 3 planted crops, read back **in order** |
| 6 | `MIGRATION.md:1324` updated | ✅ superseded in place + § 13.7 row struck; the stale line is left visible with its correction |
| 7 | completion record + header flipped | ✅ |

**On criterion 3 — the size ceiling ended up mattering, and more than one way.** `MAX_PROMPT_ARGV_BYTES` is untouched (correct where it stands, per § 4). A **second** policy ceiling `MAX_PROMPT_JSON_ARGV_BYTES = 512 KiB` now bounds the `--prompt-json` payload, sized for **eight worst-case crops**, so `zoom_ww7_full.png` is a **named refusal** carrying the file, the encoded size, the limit and the crop-don't-downscale remedy.

⚑ **And your refutation condition about the environment has a better answer than a conservative constant.** `ARG_MAX` bounds argv **and environ together**, and the environ **is** knowable at call time. I binary-searched this host's real limit under three environments and checked it against a formula: **exact, 3/3, across a 100 KB environment swing** (§ 14.3 table). A suite row asserts it **against the operating system** at the boundary — exactly `ARG_MAX` must execute, one byte more must raise. So the physics bound is enforced precisely, on **both** paths, and is deliberately inert on the `-p` path with a test pinning the inertness.

### Two things I got wrong, both caught by verification rather than by report

1. ⚑ **One of my own test rows was green for the wrong reason.** `test_a_FAT_ENVIRONMENT…` matched the refusal on `ARG_MAX` — and **passed against pre-fix source**, because the *old* `-p` ceiling's message contains that token too. It was testing nothing. The RED-proof caught it; it now fires through the image path and matches the physics refusal's own words. **This is your "instrument returning cleanly after it stopped answering the question" wearing a test's clothing** — I was one careless `match=` from shipping the very shape you warned me about, inside the fix for it.
2. **I briefly believed I had broken `test_BOTH_lock_fds_are_INHERITED_by_the_child`.** I had not — see below.

### ⚑ Flagged, NOT picked up — a dispatch request

**`test_BOTH_lock_fds_are_INHERITED_by_the_child` is a pre-existing timing flake.** Measured **3/5 failures against unmodified `1a9c5948`** and **1/5 post-change on an idle host** — it fires on both sides, independent of this change. A watcher thread sleeps 0.2 s and spawns a fresh interpreter while the child sleeps 0.5 s; under load the probe lands after the child has exited.

⚑ **Its failure direction is a FALSE ALARM: it reports *"the per-seam lock did not travel to the child"* when the lock travelled correctly** — a correct mechanism accused by a mis-timed instrument. **Same shape as the `git diff HEAD~1` near-miss**, and on a row guarding P-3 exclusivity, a false alarm here would send someone hunting a concurrency bug that does not exist.

**In my seam, small, well-grounded — and I am not touching it without a dispatch.** Requesting one.

### Cost

**8 live vendor calls, ~$0.048**, all at the lane pin, all under the seam+slot semaphore. Per-call ledger in § 14.8. **Well inside normal; no anomaly.**

### Suite

**868 rows** (856 baseline + 12 new), **867 pass**; the single failure is the pre-existing flake above. ⚑ **I am reporting a count rather than "green" on purpose** — I first drafted *"full suite green"* about a run I had not finished reading, which in a dispatch about instruments that stop answering their question is not an irony I get to keep.

RED-proof at `1a9c5948` with the wiring reverted and the helpers retained: **9 of 12 new rows red pre-fix**, headline `ValueError: '--prompt-json' is not in list`. The 3 green-both-sides are green **by design** and named in § 14.6. Two pre-existing vocabulary gates (`JR20`, `JR24`) fired and were **satisfied, not silenced**.
