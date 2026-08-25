# Dispatch — star-lord: the image lane Matt's second-opinion request needs, plus the two items you flagged back to me

**Status:** PENDING
**Authored:** 2026-08-25 (knight-rider)
**Seam:** `factory/harness/` + `factory/` (star-lord)
**Predecessor:** `7837ade3` — the Grok transient-auth debounce. **This dispatch exists partly because you flagged two items and correctly declined to pick them up without one.**

---

## 0. Before anything — what you did on `7837ade3` and why I am not re-opening it

I verified your return against the tree rather than relaying it: `AUTH_CONFIRM_READINGS = 3`, `probe_auth_once` / `check_auth` split, `LaneAvailability.terminal` defaulting `False`, `codex.py` `terminal: bool = True` preserved, both named tests present. **All of it is there.**

Three things in that return I want to name, because they are the reason this dispatch trusts your judgement on the calls below:

- **You said the number 3 is chosen on cost asymmetry, not fitted to a measured refresh window, and you wrote that into the code so nobody later reads it as empirical.** You measured the probe (n=6, 0.74–0.96 s) and were explicit that you could *not* measure the thing that actually matters because inducing it needs `grok logout`, which is Matt-only on a live lane. **A number honestly labelled as unfitted is worth more than one silently presented as derived.**
- **You put the fix in `check_auth`, not at the drain boundary, and said the drain "was the easier write, which is the tell."** It was also the placement that keeps `factory lane-status` — the surface a *human* read the false verdict off — from continuing to report a blip as a closure.
- **You declined to fix Codex.** Held to below.

## 1. ⚑ THE IMAGE LANE — this one unblocks a standing Matt request, so it leads

Matt asked for **Codex and Grok second opinions on the VFX frames**. I ruled that request **not executable as framed** and routed the empirical part to you. Full finding: `knight-rider/rulings/2026-08-25-codex-and-grok-are-not-symmetric-for-vfx-second-opinions-and-neither-is-reachable-from-the-factory.md`.

The short version, measured first-hand:

| Lane | Image door at the vendor | Reachable from our factory |
|---|---|---|
| **Codex** | ✅ `-i, --image <FILE>...` | ❌ `build_argv` never emits it |
| **Grok** | ❌ **no `--image` flag exists at all** | ❌ |

`grep image|vision|attach|png|base64` across `factory/harness/*.py` → **zero hits.** Both `build_argv` bodies emit text on argv only.

### 1a. The Grok probe — one call, and I want the answer either way

`grok --prompt-json <JSON>` is documented as *"Single-turn prompt as JSON content blocks."* **Content blocks** is the vocabulary image inputs normally travel in. **That makes it plausible. It does not make it true, and I am not claiming it is.**

**Run the cheapest refuting test:** one `--prompt-json` call with a single image content block and a trivial prompt ("describe this image in one sentence"). It either describes the image or it errors.

- **Record the result either way, including the exact error text if it fails.** A negative is a real finding here — it closes Matt's request down to one lane permanently, and that is something he needs to know rather than something to keep re-probing.
- **Do not build anything on top of a passing probe in this dispatch.** Probe, record, stop. If it passes, wiring it is the next dispatch with its own tests.

### 1b. Codex — emit the flag

Codex is **capable at the vendor and blocked only by our own `build_argv`.** Emit `-i/--image` from `codex.py`'s `build_argv` behind an explicit optional parameter (images default empty; today's callers must produce byte-identical argv).

- **Pin it with a test that asserts the no-images call is argv-identical to current behaviour.** The risk here is not that images break; it is that adding the parameter perturbs every existing Codex call silently.
- **Cite by symbol, not line number, in anything you write.** My own ruling cited `grok.py:733` and your `7837ade3` moved it to `732` **within twelve minutes.** `build_argv` will still be `build_argv` in fifty commits.

### 1c. ⚑ A constraint you must know before you test with real frames

An API limit killed a 20-minute drax run: **`400 invalid_request` — image dimensions exceed 2000px for many-image requests**, at ~128 accumulated image blocks. Ruling: `knight-rider/rulings/2026-08-25-the-2000px-wall-killed-drax-…md`.

**For your probes, use one small synthetic image.** Do not pull production VFX frames into your context to test a plumbing question. The plumbing question is answered by any image at all.

## 2. `preflight_failed` — the item you flagged first, and you were right to flag it

Your words: *"`assert_no_leader_parses` folds 'the flag was REJECTED' into 'the assertion could not be MADE' (a 30 s timeout) as one `False` — and the `AUTH-BLOCKED.md` it files tells Matt to run `grok login`, the wrong remedy for a flag a CLI update removed."*

⚑ **This is the same defect you just fixed, wearing different clothes: a reading that cannot distinguish two states is collapsed into a verdict that treats them identically, and the wrong one is terminal.** The auth case merged "expired" with "transient"; this one merges "rejected" with "unanswerable."

**And this one has a second harm the auth case did not:** it escalates to Matt with a **remedy that cannot work.** `grok login` does nothing about a flag a CLI update removed. Matt runs it, it succeeds, the lane stays broken, and the escalation has now consumed his time *and* burned the credibility of the next one.

**Do it.** You declined last time on sound grounds — *"I left it rather than turn one fix with a proven gate into two changes with one gate."* **That reasoning was correct then and is discharged now**, because this dispatch gives it its own gate.

- Third return value from `assert_no_leader_parses` (or a small result type — your call which reads better).
- **`preflight_failed` by timeout must NOT be terminal.** Unanswerable is not refuted. Same principle as `auth_unknown`.
- **`preflight_failed` by genuine rejection may be terminal — but its escalation must name the right remedy.** If the flag was removed by a CLI update, the `AUTH-BLOCKED.md` vocabulary is wrong end to end; it is not an auth problem and should not be filed as one.
- Tests for both branches, and a test that the escalation artifact for the rejection branch does **not** tell Matt to re-auth.

## 3. The word collision — small, and worth ten minutes now

Your flag: `factory lane-status` already prints `terminal : True` (leg-3, *"last run-log row is terminal"*, display-only) and now `LaneAvailability.terminal` exists with an unrelated meaning. **You didn't touch it; you said the two will read as one field to anyone skimming.**

They will, and the person skimming will be reading it during an incident, which is the worst possible moment. **Rename one of them.** Whichever you rename, you own the call — I'd lean toward renaming the *display* string, since it has no consumers beyond human eyes and `LaneAvailability.terminal` is now a real contract with a `MIGRATION.md` entry behind it.

## 4. Codex's one-reading hazard — ⚑ DECIDE, do not default, and I am not deciding for you

You left `codex.py` `terminal: bool = True`, byte-preserving today's behaviour, pinned by a green-on-purpose test that goes RED when the hazard closes. Your reason: *"The premise is what's missing: nobody has observed a ChatGPT-auth refresh presenting as a failed `codex login status`. xAI evidence doesn't travel to OpenAI any more than OpenAI's serial precondition travelled to xAI."*

**That is disciplined and I am not overruling it.** But I want it decided rather than inherited, because there is a real argument on the other side and it deserves an answer in the record:

- **For holding:** evidence-free generalization across vendors is exactly the move this project keeps getting burned by. The pinning test is honest engineering — the hazard is *declared*, not hidden.
- **For closing:** the debounce costs ~0.9 s and $0.00, and the failure it prevents is *the entire queue handed to Claude plus a false Matt escalation*. **You do not need evidence that a specific vendor's token refreshes to know that a single reading is a bad instrument for a verdict.** The argument for debouncing is about *reading discipline*, which is vendor-independent, not about xAI's refresh behaviour, which is not.

**Write the disposition down either way**, in the code and in `MIGRATION.md`. *"Held, because X"* is a complete answer. **What must not happen is that it stays `True` because nobody revisited it** — a declared hazard that is never dispositioned decays into an undeclared one, and the pinning test's green will eventually read as approval rather than as a bookmark.

⚑ **If you close it, note that this dispatch is NOT evidence Codex has the defect.** It is only a ruling that the dispatch's author thinks reading-discipline generalizes. Do not let a future reader mistake my argument for a measurement — that inversion is the exact thing your `AUTH_CONFIRM_READINGS` comment was written to prevent.

## Quality criterion

**Game-quality goal this dispatch serves:** Matt's judgement that the VFX lack the internal depth of the originals is currently **unverifiable by any external model**, because no lane can be shown a frame. § 1 restores the ability to get a second opinion at all. §§ 2–4 protect the job queue that every subsequent VFX render run depends on — an auth or preflight blip that empties the queue costs a render wave, and it costs it *silently*.

**Refutation conditions — surface before executing if any apply:**
- The `--prompt-json` probe passes but returns something that only *looks* like image comprehension (e.g. it describes a filename or hallucinates from the prompt text). **Design the probe so a hallucinated answer is distinguishable from a real one** — use an image whose content cannot be guessed from its name.
- Emitting `-i/--image` perturbs existing Codex argv in any case. **Stop and report; do not "fix forward."**
- § 2's third return value turns out to need a wider signature change than described. Report the true scope rather than expanding silently.
- Anything here contradicts `MIGRATION.md` § 12 as you left it.

## Acceptance criteria

1. `--prompt-json` image-block probe **run**, result recorded either way, exact error text if it fails.
2. `codex.py` `build_argv` emits `-i/--image` when images are supplied; **test asserts no-images argv is byte-identical to current**.
3. `preflight_failed` distinguishes rejection from timeout; timeout is **non-terminal**; rejection's escalation artifact does **not** prescribe re-auth.
4. Tests for both `preflight_failed` branches, both RED before the fix.
5. Word collision resolved; the rename named in `MIGRATION.md`.
6. Codex `terminal` **dispositioned in writing** — held or closed, with the reason, in code *and* `MIGRATION.md`.
7. Full suite green; report the count against your 845 baseline.
8. `MIGRATION.md` § 12 extended (cross-seam: `gamora` / `drax` / `jack-ryan` read `DrainReport` and the telemetry stream).
9. Cite by **symbol**, never by line number.
10. Commit with `git commit --only <paths>`; verify **before** with `git diff HEAD --name-status -- <paths>` and **after** with `git show --stat HEAD`. **Never `git diff HEAD~1` alone** — with one commit named it compares against the working tree and reports other sessions' files as if they rode along. Use `git -C <path>` on every git call.

## Out of scope

- **Wiring a working `--prompt-json` image path into the harness.** Probe only. If it passes, that is the next dispatch.
- Any VFX analysis, any production frames, any judgement about the VFX themselves.
- `reincarnated-godot`, `reincarnated-demo`, `reincarnated-loadout` — a live drax recovery session is in the godot tree.
- Sealing or tagging.

## Push

Matt authorized push across repos **for this session only**; it expires at the session boundary. `reincarnated-collaboration` also sits under the standing Step-2 wave pattern. Push your own committed work; **do not stage untracked files** — the tree carries other sessions' capture directories.
