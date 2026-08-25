# Dispatch — 2026-08-25 — drax — TRANCHE 3A RECAPTURE: the yaw fix landed, and the re-run command as written would destroy the only evidence that can answer what the defect cost

**Status:** ✅ **COMPLETE** — 10/10 acceptance criteria discharged. **§ 2 outcome 2.** Fold test does **NOT** move toward FOLD. ⚑ **Two findings the dispatch did not ask for, one of which is a § 8 refutation condition firing** — see § Completion record (C) and (D).
**From:** knight-rider (Step-2 build wave, conductor)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Pattern:** B — dedicated session
**Position in wave:** discharges `Owed` item 1 of `2026-08-25-drax-s2c-mint-tranche-3a.md` § Completion record (2).
**Lane:** ⚑ **SERIAL behind the camera-framing / WW-AB dispatch** (`2026-08-25-drax-camera-framing-and-wwab-render.md`) per wave-record § 3 ruling 5. Do not run these concurrently in one working tree.

---

## 0. What unblocked this

The forward-axis fix landed in three commits — `612c1e3` (Commit A, the genuinely-wrong sites), `1c4f90f` (Commit B, `face_toward()` as a byte-verified no-op), `689116c` (Commit C, cathedral review default). **Matt then verified it by eye, verbatim:**

> *"I confirmed that the _v3 mp4s from drax now have the character facing the correct way (forwards)."*

So `Owed` item 1's precondition — *"the fix is explicitly not mine to land"* — is discharged. **Re-capture is now yours.**

---

## 1. 🛑 READ THIS BEFORE YOU TYPE THE RUN COMMAND. THE DEFAULT INVOCATION DESTROYS THE BEFORE-HALF.

**I read the runner rather than trusting my memory of it, and it is worse than I expected:**

```
run_s2c_rows38.sh:126   UDIR="s2c38${SUFFIX}"
run_s2c_rows38.sh:145   rm -f "$USERDIR"/*.png
```

**So `bash scripts/run_s2c_rows38.sh <stamp>` wipes `s2c38/`, and the pass-2 form with `SUFFIX=b` wipes `s2c38b/`.** Those two directories are, right now, **2,106 PNGs each — the complete pre-fix capture, both independent passes.** I counted them; they are not inferred from your prose:

| Directory | Frames | Size | What it is |
|---|---|---|---|
| `…/reincarnated-godot-spike/s2c38` | **2,106** | 4.2 G | rows 3–8, pass 1, **pre-fix** |
| `…/reincarnated-godot-spike/s2c38b` | **2,106** | 4.2 G | rows 3–8, pass 2, **pre-fix** |
| `…/reincarnated-godot-spike/s2c12` | **874** | 1.7 G | rows 1–2 (`dash_attack` + `blink`), **pre-fix** |
| `harness_logs/s2c_rows38_2026-08-25{,b}` | **0** | 29 M each | ⚑ **PNGs already gone** — I deleted them during the disk crisis. `render.txt` only. |

⚑ **The `harness_logs` copies are already gone and I am the one who deleted them.** The userdir is therefore **the sole surviving copy** of the pre-fix frames. There is no second chance at this.

**THE ORDER: run with a fresh suffix. `v3` for pass 1, `v3b` for pass 2.** That yields `s2c38v3` / `s2c38v3b` and leaves `s2c38` / `s2c38b` untouched by construction, because the `rm` is scoped to `$USERDIR` and `$USERDIR` now names a different directory.

**Verify before you fire, not after:** `echo` the resolved `USERDIR` for both passes and confirm neither string equals `s2c38` or `s2c38b`. **This is the exact failure that already fired once in this tranche** — `USERDIR` a constant while `OUT` carried `$SUFFIX`, pass 2 silently overwriting pass 1, and the receipt printing green afterwards. You found it and fixed it at the cause. **The same shape is now pointed at the pre-fix frames instead of at pass 1**, and this time the loss would be silent in a different way: nothing would error, the recapture would succeed, and the comparison in § 2 would simply become impossible with no message saying so.

---

## 2. ⚑ Why this is not merely owed work — the recapture is the cheapest refuting test for a question now blocking a SEALED verdict

**You surfaced this and declined to rule it, correctly:**

> *"My Pair-1 reproduction is byte-exact against R-1.3 — and R-1.3 was computed from these same backwards-body frames. The sealed L-29(6) adjudication rests on the same defect. **Reproducibility is not validity.** Surfaced, not ruled."*

I routed it to jack-ryan by record (`qa/pending/2026-08-25-reproducibility-is-not-validity-sealed-verdicts-rest-on-backwards-body-frames.md`, commit `82aedca6`) because `SendMessage` is unavailable — sixth time this session. **In filing it I had to admit I could not answer its central question from outside:**

> *"If the defect is common-mode across every arm in a comparison, a differential verdict may survive it even though every absolute number in it is wrong. **Whether L-29(6) and R-1.3 are differential or absolute claims is exactly the thing I cannot determine from outside.**"*

**Neither can jack-ryan. But your recapture MEASURES it, at near-zero marginal cost, because the before-half is already on disk and the after-half is the thing you were going to capture anyway.**

Same seeds, same stages, same arms, same gate — **one variable changed.** That is a matched pair, and it is the strongest experimental object this wave has produced by accident.

### 2.1 What to emit

For the `dash_attack` / `blink` pair specifically (rows 1–2, `s2c12` — **the pair the sealed L-29(6) adjudication is about**), and then across rows 3–8:

| | Emit |
|---|---|
| **Absolute** | `A[i]` per body, pre-fix vs post-fix, **per arm.** How wrong was each number? |
| **Differential** | the class gap (`dash` vs `blink`) computed **within** pre-fix and **within** post-fix. Does the gap survive? Does it survive with the same sign? |
| **Verdict** | does `dash_attack` STEPS / `blink` RAMPS still hold on correct bodies — and by how much margin, against the sealed `+0.2069` |

**Three outcomes, all publishable, none of them a failure:**

1. **The gap survives with the same sign and comparable margin** → the defect was common-mode for this claim, L-29(6) is differential, **the seal holds and now has a receipt instead of an argument.**
2. **The gap survives but the margin moves materially** → the seal holds on its verdict and its *figures* are wrong; jack-ryan rules on whether a verdict may carry corrected figures.
3. **The gap inverts or collapses** → ⚑ **a sealed verdict is refuted by measurement.** Halt, do not re-seal, route immediately.

⚑ **You produce the number. You do NOT rule what it means.** The disposition of a sealed verdict is jack-ryan's at Tier A, and it is already filed and waiting for him. **This dispatch converts a jurisprudential argument into a measurement** — which is the whole of your job here and the end of it. Do not write "the seal holds" or "the seal falls" anywhere in your return. Write the numbers and name which of the three outcomes they match.

**Cost check, because this could be scope creep and I want it refuted if it is:** rows 1–2's pre-fix frames exist (`s2c12`, 874) and rows 1–2 are two of 3A's eight rows, so they are inside the recapture you already owe. **If re-running rows 1–2 turns out to cost materially more than folding them into the same pass, say so and I will re-scope it** rather than have you absorb it silently.

---

### 2.2 ⚑ F-9 LANDED WHILE I WAS WRITING THIS, AND IT CHANGES HOW TO READ ONE OUTCOME

jack-ryan ruled F-9 at `eaf93982` (engine, pushed): **byte-identity is a ONE-SIDED instrument.**

| direction | exposure to the flake floor | requirement |
|---|---|---|
| reporting **IDENTITY** (a PASS) | noise can only *break* identity, never *manufacture* it | **none** |
| reporting a **DIFFERENCE** (a FAIL) | fully exposed | **same-code repeat first** |

**Consequence for you, and it is good news twice over:**

1. **Your 2,106/2,106 receipt is a PASS. It does not demote and is not re-scored.** Neither does S2B, S2C, or Commit B's 471/472. The ruling is explicit: *"Every seal in this wave rests on a PASS. Therefore no seal demotes."*
2. ⚑ **It converts § 8's scariest refutation condition from ambiguous into diagnostic.** If the recapture returns numbers **byte-identical to the pre-fix ones**, that identity is now certified noise-immune — so it is *positive evidence that the metric cannot see body pose at all.* Before the ruling that outcome could have been shrugged off as flake. After it, **it is a measurement, and it is a bigger finding than this tranche.** Report it loudly if it happens.

⚑ **The FAIL branch now carries a precondition, and § 2's comparison lives on the FAIL branch.** Your before/after delta is, structurally, a claim that two captures *differ*. Under F-9 that direction is the exposed one. **So: a same-code repeat is required before any "the numbers moved" claim** — which the two-pass structure in § 3.1 already gives you for free if you take two passes. **This is now an argument for two passes that did not exist when I wrote § 3.1**; weigh it there and rule accordingly.

**And state the denominator.** jack-ryan flagged that the original flake report gave *"f0030 differs across runs of identical code"* with **no frame count** — *"an existence proof of a non-zero floor, not a measurement of one."* Owed item 3 below makes that standing. **Any FAIL-direction byte claim in your return states the repeat's frame count.**

## 2.3 Three items jack-ryan left OWED, all yours, none blocking — folded here because I cannot message you

From his F-9/F-10/Gate-1 return. **All three are one-liners; none is a reason to delay the capture.**

1. ⚑ **Commit the `project.godot` deletion.** F-10 is **settled as a semantic no-op, by measurement on the shipped binary** — Godot 4.6.3, scratch project, no `[rendering]` section: `HAS=true VALUE=1.0`, i.e. the default equals the deleted value. Git history confirms it entered as editor churn in `cfb70c9` (a ravine-carve commit enumerating five changes, none about LOD). **Your call to freeze the tree rather than restore mid-dispatch was CONFIRMED CORRECT under your uncertainty** — restoring would have introduced a tree delta between the sealed corpus and the new arm, the exact confound. Now that it is settled, the line is no longer comparability-relevant and **the editor will keep re-deleting it and generating recurring false alarms until you commit it.**
2. **One line on `drax/notes/2026-08-24-s2b-mint-note.md:1125-1142`** retiring the P-BEAM control-arm-zero sentence and re-anchoring the verdict to the **6,084 px** figure. The sentence is falsified as stated (it was a sample, not a property); **the verdict is untouched** — three populations at 1× / 338× / 656× with no overlap, so striking the sentence changes nothing. Same shape as F-1: premise refuted, verdict stands, one line of prose owed.
3. **Standing, from here on:** a byte claim on the **FAIL direction** states the repeat's frame count.

⚑ **And one thing to NOT carry.** jack-ryan checked the record and the `melee` item in my forward-axis dispatch **was not your error and not mine** — `melee` was never in his finding's site list; it was swept in by his own Q4 scope amendment (*"widen it to every row in which a body appears"*). His words: *"You relayed my clause faithfully. Don't carry that one."* He also banked a third error against himself: **`s2a_stage:303` was already correct and he asserted it safe to flip "checked, not assumed"** — he checked the rig and never checked the argument. **Your refusal to make that edit, measured at six bearings, is ratified.** Your `face_toward(n, -ring[i])` rewrite — passing the *direction* explicitly — is named as the disambiguation.

## 3. Scope — exactly the PENDING-RECAPTURE set, and explicitly not one row more

**Re-derive (all eight 3A rows — every row in which a body appears, per jack-ryan's widening):**
`dash_attack` · `blink` · `teleport` · `leap_strike` · `ground_slam` · `cone` · `orbit` · `vortex_pull`

1. **Both passes**, fresh suffixes per § 1
2. **Re-gate** — all 79 verdict keys
3. **Re-cut all 8 MP4s** (the existing ones are footage of the bug, by your own words; retain them as the before-half, do not delete)
4. **Then** the tag — `drax/v0.1-s2c-mint-tranche-3a`, which you retracted and may now re-take

**DO NOT re-derive — these sealed and your own halt says why:**
- the determinism receipt as a *property claim about the harness* (pose-orthogonal)
- the harness/disk `SUFFIX` fix
- `max(ms)==0` unsatisfiable-by-construction (an apparatus defect, true whatever pose the bodies held)
- the `#80` cl. 5(b) repo-wide count
- the Gate-1 I2 emptiness sweep

### 3.1 ⚑ One item in that split is YOURS to rule, and I am not deciding it for you

**Does the *recapture* need two passes, or one?**

The sealed determinism receipt proves *the harness was deterministic*. **But the harness is not the same harness** — Commit A changed render output by design, and Commit B's no-op claim is byte-verified against the *old* corpus. My reading is that a fresh two-pass receipt is therefore **not** redundant, and the marginal cost is 4.2 GB and ~25 minutes.

**That is my reasoning offered, not imposed.** Determinism methodology is your seam and you have already corrected me once on this exact runner. If one pass is defensible, take one and say why.

### 3.2 ⚑ The self-referential trap in R-5 — the highest-stakes single number here

**R-5's own `AXIS HOLDS` verdict is itself PENDING-RECAPTURE.** You wrote it: *"PENDING-RECAPTURE: every archetype number including R-5's own AXIS HOLDS."*

That fold test already reversed once — the criterion `max(melee_strike_ground_px) == 0` was unsatisfiable by construction, so `CONVERGED — FOLD` was *"a constant wearing a comparison."* You repaired it to the ruled instrument (cathedral 11.43×, arena 3.96×, replicating). **Those replication figures were taken on backwards bodies.**

⚑ **`FOLD` is the destructive direction** — it routes to gandalf as evidence to **merge two archetypes**. A wrong FOLD permanently collapses a distinction the design depends on. **If the recaptured fold test moves toward FOLD, do not route it to gandalf. Halt and surface it.** A criterion that has already reversed once, re-run on corrected data, is the last place in this tranche to trust a single reading.

---

## 4. Discipline #1.1 — pre-fire resource-bounds projection, RUN AND RECORDED

I ran this before authoring, which is the part that was missing when this tranche halted on disk at 0.6% free.

| | |
|---|---|
| Measured per-frame | **~2.88 MB** (`s2c38/clip_*.png`, sampled) |
| Two passes × 2,106 frames | **~8.4 GB** |
| Pre-fix frames RETAINED (§ 1) | +8.4 GB already resident, **not reclaimable** |
| Free on `/System/Volumes/Data` | **59 GiB (87% used)** |
| Projected free after | **~50 GiB** |
| Margin | **~6×** |

**Fits with margin. Fire it.**

⚑ **Two caveats that are yours to re-check at fire time, not mine to assert from here:**
- **A concurrent drax session (camera-framing / WW-AB) is consuming this same pool right now.** § 0's serial-lane rule exists partly for this. **Re-run `df -h` yourself immediately before firing** — my number has a shelf life and the last time this tranche trusted a stale disk reading it died at minute 24 of a 25-minute capture.
- Do **not** reclaim `s2c38` / `s2c38b` to make room. If the projection stops fitting, **halt and route to me** — the before-half is worth more than the convenience, per § 2.

---

## 5. Push clause — READ IT, IT OVERRIDES THE STANDING PATTERN

**Commit as you go. Push is authorized for this session** under Matt's verbatim *"push as you go through this session"*, which he extended to **all repos including `reincarnated-godot`** — this session only.

**This is a narrower instruction than it looks and it is deliberately explicit**, because this wave has already run the two-sessions-opposite-push-instructions failure once (conflict rule, `CLAUDE.md`). **The per-dispatch clause governs. This one says: push.**

⚑ **`#62(a)` still binds.** Stage by explicit pathspec; `git commit --only <paths>`; verify with **`git show --stat HEAD`**, never `git diff HEAD~1` — concurrent agent sessions are writing in these trees and `git diff HEAD~1` compares your commit to the *working tree*, so it will name other agents' uncommitted files as though they rode along. That instrument produced a false alarm in this session already.

**Do not stage capture directories.** `harness_logs/**/*.png` and `**/*.mp4` are gitignored under the Synty licence and must stay that way.

---

## 6. Acceptance criteria

1. Both passes captured under **fresh suffixes**, with `s2c38` / `s2c38b` **verified intact afterwards** (frame count re-counted, not assumed)
2. All 8 rows re-gated; the 79 verdict keys re-emitted; **nothing rounded**
3. All 8 MP4s re-cut and ffprobe-verified; pre-fix MP4s retained as the before-half
4. **The § 2 before/after comparison emitted** — absolute, differential, and which of the three outcomes it matches, **with no ruling attached**
5. § 3.1 (one pass or two) **ruled by you, with the reason stated**
6. § 3.2 fold test re-run; **halt-and-surface if it moves toward FOLD**
7. `Owed` items 2 (R-3 teleport corridor re-cut) and 3 (R-7 `motif:shuriken@arena`) re-checked against corrected frames — they may dissolve, and if they do, **say that they dissolved rather than deleting them silently**
8. § 2.3's three owed items discharged — `project.godot` deletion committed; the P-BEAM control-arm-zero line retired; FAIL-direction byte claims carry a frame count
9. Tag `drax/v0.1-s2c-mint-tranche-3a` taken **only** if 4 and 6 are clean
10. Completion record appended **to this file**, and this file's header `Status:` updated in the same edit

## 7. Out of scope (explicit non-goals)

- **Ruling the sealed-verdict question.** Measure it; jack-ryan disposes. (§ 2)
- **`king_rig.gd` `_sword_yaw_left_deg` / the sword-side defect** — separate dispatch exists (`2026-08-25-drax-king-rig-sword-side.md`). *"A remedy that quietly widens is how a verified fix becomes an unverified one."*
- **F-7** (`TRAIL_SPAN_S` / `TRAIL_SAMPLES` declared-vs-realized) — filed, unrepaired, still out of scope
- **Tranche 3B** — behind P-BEAM, not yours in this session
- **Any further forward-axis edits.** The fix landed and Matt verified it. If you find another site, **file it; do not fold it in.**
- **Re-opening tranche-2 sealed rows** beyond what the emptiness sweep already discharged

## 8. Quality criterion

**Game-quality goal this dispatch serves:** the archetype numbers minted here become **inherited design substrate** (Discipline #25) — they decide which skills read as distinct to a player and which get merged. Every one of them was measured on a body facing 180° from travel, scoring **body-anchored effects that emit along body-forward**, which means they are precise numbers about the wrong pose. **A wrong FOLD here permanently collapses a distinction the player would have felt.** This dispatch is what makes the eight rows describe the game that exists.

**Refutation conditions** (surface if any apply):
- The § 2 comparison cannot be computed because the pre-fix and post-fix captures are not arm-matched — **say so immediately**; it is the load-bearing assumption of this dispatch and I have not verified it beyond frame counts
- The recapture reproduces the pre-fix numbers **byte-exactly** — which would mean either the fix did not reach these rows or the metric cannot see body pose. **Either is a finding that outranks the tranche.**
- Acceptance criteria can pass while the § 2 comparison produces something nobody can rule on
- This dispatch pre-commits to "the sealed verdict is wrong." **It must not.** Outcome 1 in § 2.1 — the seal holding, with a receipt — is the single most likely result and should be reported as plainly as a refutation
- § 3's do-not-re-derive list retires something that the *fix itself* invalidated, which I would not have caught from outside

## 9. References

- `2026-08-25-drax-s2c-mint-tranche-3a.md` — § SEAL-BLOCK, § RESUMPTION, § Completion record (2), § Owed
- `qa/pending/2026-08-25-reproducibility-is-not-validity-…md` (`82aedca6`) — the sealed-verdict question this measures
- `reincarnated-godot` `2afde08` (tag retraction) · `612c1e3` / `1c4f90f` / `689116c` (the fix) · `a1690fe0` (galadriel, the original facing finding)
- `step2-vfx-archetype-mint-wave-record.md` § 3 ruling 5 (serial lane)
- `canonical/matt_to_do/2026-08-24-mac-disk-space-red.md` — the disk lineage and the `cp` correction

---

## Completion record — drax, 2026-08-25

**Status: COMPLETE. 10/10 acceptance criteria discharged.** Full numbers:
`agentic_orchestration/drax/notes/2026-08-25-s2c-mint-note.md` **§ 14**.

### The answer to the question this dispatch existed to ask

**OUTCOME 2 — the gap survives, same sign, and the margin moves materially.**

| `SC(added-luma)` (the sealed instrument) | pre-fix | post-fix | Δ | sign |
|---|---:|---:|---:|---|
| **pooled** | **+0.2069** | **+0.3807** | **+0.1738 (+84.0 %)** | **preserved** |
| arena | +0.2653 | +0.4955 | +0.2302 (+86.7 %) | preserved |
| cathedral | +0.2069 | +0.3807 | +0.1738 (+84.0 %) | preserved |

⚑ **THE GAP WIDENED. The defect was SUPPRESSING the distinction, not manufacturing it.** Mechanism
is per-body and unambiguous: `dash_attack` rose on all 6 evaluable bodies (mean **+0.1483**, +13.2 %
to +42.7 %); `blink` moved **−0.0019**, every body within ±3.6 %. Trail-bounded mover-row is
pose-sensitive; payload-carried row is not — the spec's own taxonomy falling out of a measurement.

⚑ **I AM NOT RULING WHAT THIS MEANS.** Whether a sealed verdict may carry corrected figures is
jack-ryan's at Tier A, filed at `qa/pending/2026-08-25-reproducibility-is-not-validity-…md`. The
instrument (`scripts/s2c_prepost_compare.py`, committed at **`0800f32` — before the after-half
existed**, so its thresholds cannot have been chosen to fit) contains no branch that can write "the
seal holds" or "the seal falls."

### (A) § 1's catastrophe was REAL, and worse in a place the dispatch did not look

`run_s2c_rows38.sh` is suffix-parameterised, so the fresh-suffix order was executable there.
**`run_s2c_rows12.sh` was not** — `USERDIR` a constant (`s2c12`), `--out=user://s2c12/` hardcoded in
**all 24 arm invocations**, and an unconditional `rm -f "$USERDIR"/*.png`. `SUFFIX` was read and
reached `$OUT` only. **Every invocation, with any argument, wipes `s2c12`** — the pre-fix capture of
`dash_attack` + `blink`, the exact pair the sealed L-29(6) adjudication is about. Same defect I
removed from the rows-3-8 runner at `a5779c8`; I fixed the runner that bit me and did not sweep its
sibling. Fixed at `ce71ff8`.

⚑ **CORRECTION TO § 1'S TABLE, MEASURED:** the rows-1-2 `harness_logs` PNGs were **not** deleted —
874 in each of `s2c_rows12_2026-08-25{,b}`, sampled md5 agreeing with the userdir. So the rows-1-2
pre-fix evidence was **triplicated, not singular**. But it survived *because of the disk-filling `cp`
that the rows-3-8 fix removed at its cause* — **protected by a bug, not by a decision.** That is why
it was fixed rather than noted.

**Guards taken BEFORE anything ran:** all five pre-fix directories `chmod a-w`; all four resolved
`USERDIR` values printed **by the real scripts** (`ONLY=none`, stamp `PATHPROBE`) and checked against
the protected names; frame counts re-verified after. **Acceptance 1: `s2c38` 2106, `s2c38b` 2106,
`s2c12` 874 — intact, re-counted, not assumed.**

### (B) § 3.1 RULED BY ME: TWO PASSES — and the ruling paid for itself

Reason, stated before firing: under **F-9** a before/after delta is structurally a claim that two
captures **DIFFER**, the noise-**exposed** direction, so a same-code repeat is its *precondition*.
The sealed receipt proves the **old** harness was deterministic; Commit A changed render output by
design, so the property does not transfer. **A one-pass recapture would have shipped (C) invisibly.**

### (C) ⚑ A § 8 REFUTATION CONDITION FIRED — the do-not-re-derive list retired something the FIX ITSELF INVALIDATED

The dispatch predicted this exact shape and said it could not be caught from outside. § 3 retired the
determinism receipt as *"a property claim about the harness (pose-orthogonal)."* **The corrected
harness is no longer byte-deterministic:**

| corpus | pre-fix (sealed) | post-fix | worst maxdiff | worst px ≥ 4 |
|---|---:|---:|---:|---:|
| rows 3–8 | **2106 / 2106** | **2101 / 2106** | 29 | 15 |
| rows 1–2 | **874 / 874** | **873 / 874** | 1 | 0 |

The seal remains true of the **old** harness; what is refuted is that it **carries forward**.
"Pose-orthogonal" was the wrong axis to retire it on — Commit A did not only change pose, it changed
render output.

⚑ **BYTE-DETERMINISM AND MEASUREMENT-DETERMINISM ARE TWO CLAIMS AND ONLY ONE MOVED.** Gate run
independently on both post-fix passes: **17,507 leaves, 0 verdicts flipped, 0 figures moved** —
bit-identical. On the one rows-1-2 flake frame, noise is maxdiff 1 / 6 px / **0 px ≥ 4**, while the
pre-vs-post signal on that same frame is maxdiff 236 / 10,337 px / **4,873 px ≥ 4**. The by-value
screen sees the signal and does not see the noise at all. **Reported as two claims rather than
letting the measurement's green cover the byte receipt's red.**

**This is surfaced, not disposed of.** It is a new defect in the shipped harness, discovered by a
receipt the dispatch had retired.

### (D) ⚑ A CONFOUND IN THE BEFORE-HALF, caught by a key-set check

The rows-1-2 pre-fix `gate.json` was written by an **older gate script**
(`c8_key_collisions.unevaluable_reason` present post, absent pre). The comparison as filed would have
moved **two** variables. The pre-fix rows-1-2 corpus was **re-gated with the current instrument**
before any figure was taken. Conclusion unchanged; now genuinely one-variable.

### (E) § 3.2 — the fold test does NOT move toward FOLD. Nothing routed to gandalf.

| | pre-fix | post-fix |
|---|---|---|
| **FOLD** | AXIS HOLDS — DO NOT FOLD | ⚑ **AXIS HOLDS — DO NOT FOLD** |
| cathedral ratio | 11.43× | **11.43×** |
| arena ratio | 3.96× | **3.92×** |
| `melee_strike_px` both stages | 3,386 / 11,719 | **3,386 / 11,719 — IDENTICAL** |

The mint note recorded *"I expect it to survive — but 'I expect' is not a receipt."* **It is a receipt
now.** `ground_slam` is floor-anchored (0.02), `melee_strike` body-anchored (1.05) — neither leg
emits along body-forward, so the discriminator was pose-invariant all along.

### (F) Acceptance 7 — NEITHER OWED ITEM DISSOLVED. Said plainly, as instructed.

- **R-3 teleport corridor: 2,710 → 2,722 px (+0.44 %). STILL FAIL, real, not pose-caused.** The
  delegated judgment remains Matt's and its object (the re-cut MP4) exists.
- **R-7 `motif:shuriken@arena`: 39 / 2,322 px → 39 / 2,322 px — EXACTLY IDENTICAL. STILL FAIL.**
  ⚑ On a row that is **144/144 byte-identical** across the fix. Under F-9 that identity is
  noise-immune, so **body pose is eliminated as a cause by measurement** — the item does not
  dissolve, it gets **smaller and sharper**.

### (G) ⚑ A byte receipt for the edit I REFUSED to make

Per-row byte-identity across the fix shows **`melee_strike` at 35/36 and `clip_ms` at 315/316**
(the single differing frame in each is (C)'s flake, not the fix) — and **R-7 `orbit` at 144/144**.
Everything that emits along body-forward changed 100 %; everything anchored elsewhere changed 0 %.

jack-ryan ratified my refusal to flip `s2a_stage:303` on the *argument* (*"he checked the rig and
never checked the argument"*; `melee` was swept into the site list by a scope amendment and was never
in the finding). **Had I made that edit, these 35 frames would have moved — and the fold test's
control leg would have moved with them.** The refusal was measured at six bearings then; it is
measured at 35 frames now.

### Acceptance criteria — all ten

| # | criterion | status |
|---|---|---|
| 1 | Both passes, fresh suffixes; pre-fix **re-counted** intact | ✅ `s2c38` 2106 · `s2c38b` 2106 · `s2c12` 874 |
| 2 | All 8 rows re-gated; verdict keys re-emitted; nothing rounded | ✅ 2,149 + 15,358 keys · **0 flips** · 988 figures moved |
| 3 | 8 MP4s re-cut, ffprobe-verified; pre-fix retained | ✅ frame-count parity on all 8; before-half retained |
| 4 | § 2 comparison emitted — absolute, differential, outcome, **no ruling** | ✅ **outcome 2**, no disposition attached |
| 5 | § 3.1 ruled by me with reason | ✅ **two passes** (B) |
| 6 | Fold test re-run; halt if toward FOLD | ✅ **does not move toward FOLD** (E) |
| 7 | Owed 2 + 3 re-checked; say so if they dissolve | ✅ **neither dissolved** (F) |
| 8 | § 2.3's three owed items | ✅ 1 already at `713f487` · 2 at `8866b77a` · 3 standing, honoured throughout |
| 9 | Tag only if 4 and 6 clean | ✅ both clean — **tag taken, with (C) named in its annotation** |
| 10 | Completion record + `Status:` in one edit | ✅ this |

### ⚑ What I did NOT do

- **Did not rule the sealed-verdict question.** Measured it. jack-ryan disposes.
- **Did not route the fold test anywhere** — it did not move toward FOLD.
- **Did not touch `king_rig.gd` / `_sword_yaw_left_deg`, F-7, tranche 3B, or any further
  forward-axis site.** No remedy quietly widened.
- **Did not touch `tmp/br2watch/measure/census.json`** — not mine, still dirty, untouched.
- **Did not delete a single pre-fix frame or MP4.**

### Owed forward

1. ⚑ **(C) the byte-determinism regression in the corrected harness** — surfaced, unrepaired,
   **not mine to dispose of**. Measurement-determinism is intact (0/17,507), so nothing downstream is
   blocked, but the tranche's byte-reproducibility claim is weaker than it was and the tag says so.
2. **R-3 corridor** — still FAIL, still Matt's delegated judgment, object now exists as a corrected MP4.
3. **R-7 `motif:shuriken@arena`** — still FAIL, now proven pose-independent; glow-spill hypothesis
   unrepaired.
