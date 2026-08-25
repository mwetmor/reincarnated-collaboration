# Dispatch — drax: the WW-AB clean-room render, **authorized at HEAD**, unpinned

# ⚑⚑⚑ BLOCKED — DO NOT EXECUTE § 2. THE COMPARISON ARM THIS DISPATCH MATCHES AGAINST DOES NOT EXIST.

**Blocked 2026-08-25 by knight-rider, ~20 minutes after authoring, on galadriel's frame-forensics return (`288e95d2` / `0a2082e5`).**

**§ 2 tells you to render "under the same camera and cadence grammar as the HITL arm." There is no HITL whirlwind arm.** galadriel found it and I verified it independently before writing this block:

```
$ find ~/Games/reincarnated-godot -iname "*.mp4" | wc -l          → 278
$ find ~/Games/reincarnated-godot -iname "*.mp4" | grep -icE "whirl|ww"  → 0
$ find ~/Games -iname "*whirl*" -name "*.mp4"                     → (nothing)
```

**278 MP4s in the repo. Not one is a whirlwind clip. None exists anywhere under `~/Games`.** galadriel reached it from the other direction and by pixels: **`WW-7` is an SB-1 cell id, not a whirlwind capture** — she hashed frame 160 (`ba7e8fb4…`) and reproduced drax's own continuity exhibit. She searched 271 files; I searched 278 by a different predicate. **Two independent methods, same answer.**

⚑ **This is my error, not galadriel's discovery of someone else's.** Matt said *"the WW AB test versus my prior HITL run,"* and **I wrote a dispatch that presumed the arm was in the repo without ever checking that it was.** The same defect as the criterion-4 receipt I mandated against a diff I never ran — **twice in one session, and the second time after I had already written the correction for the first one into two separate files.** Verifying the artifact exists is cheaper than every downstream step that assumes it does.

**What is still LIVE in this dispatch:** § 1 (the lineage ruling — render off HEAD, do not pin), § 3 (resource projection), § 4 (evidence preservation), § 5 (crop, never downscale), § 6 (do not rule which arm is better). **None of those depend on the HITL arm.**

**What is BLOCKED:** the A/B framing itself — §§ 2, and acceptance criteria 3 and 4.

**What unblocks it — and it is a Matt question, not a search problem.** *"My prior HITL Whirlwind run"* is real to Matt; it is simply **not in these repos.** Either it lives outside them, or it is under a name none of our predicates match. **Do not guess, and do not substitute a different clip to make the comparison runnable** — a bake-off against the wrong reference is worse than no bake-off, because it produces a confident answer to a question nobody asked.

⚑ **A one-armed render may still be worth firing** — the clean-room whirlwind rendered off HEAD, as motion, with no comparison claim attached. **That is a decision for the conductor, not for you to take on your own initiative.** If your lane frees and this is still blocked, report and stop.

---

**Status:** ⚑ **BLOCKED (see above)** — was PENDING, **serial behind the 3A recapture.** Do not run these concurrently; both are heavy captures against one host.
**Authored:** 2026-08-25 (knight-rider)
**Seam:** `reincarnated-godot` (drax)
**Supersedes:** **Task B only** of `2026-08-25-drax-camera-framing-and-wwab-render.md`. Task A of that dispatch **landed** at `1475ed9` / `713f487`. Task B was never entered — the session died first. Nothing else of that dispatch is re-opened.

---

## 0. Why this is the priority

Matt, verbatim: *"let's **prioritize the Whirlwind VFX generation with the WW AB test versus my prior HITL run**. I think there is a lot to be learned from that run."*

**It has been blocked on a lineage question, not on capacity. That block is now cleared.**

## 1. The lineage ruling — read it, because it changes what you must NOT do

gandalf ruled at `1511030a` (`gandalf/notes/2026-08-25-s2-wwab-cleanroom-lineage-audit.md`): **disposition (a) — `LINEAGE CLEAN` holds at HEAD. Render off HEAD. Unpinned.**

The question arose because his verdict describes `1692d6e` and the `wwcr_*` glob has since moved **572 insertions / 62 deletions across four commits**. **You surfaced that and correctly declined to rule it.** His four grounds, compressed:

1. **The certified artifact did not move.** `scripts/wwcr_whirlwind.gd` — the authored effect, the thing actually in the bake-off — is **byte-identical at HEAD.** The drift is entirely harness, instrument, a new audit script, and the rig.
2. **He tested the defeat condition rather than assuming it.** Two drifted files were inside his Q2 float forensics, so that part genuinely went stale and **he re-ran it** — 23 new-line floats against 339, 11 shared, 5 non-trivial, **all acquitted** (two aren't quantities at all: `5.6` is a clause number in prose, `7.0` is a printf field width).
3. `king_rig.gd`'s drift **strengthens** the audited condition.
4. ⚑ **Decisive, and it cuts opposite to intuition: pinning would render through a KNOWN-DEFECTIVE capture path.** `f29f12b` records cross-arm maxdiff **185/114/216 at `1692d6e`, 0 at HEAD** — a clock-pin repair. **Pinning would reproduce a repaired defect on purpose, in order to match a certificate.**

⚑ **So: do NOT check out `1692d6e`. Do NOT pin. Render off HEAD.** If your instinct says "the audit named a commit, so use that commit" — that instinct is exactly what ground 4 refutes.

**Matt's frames will differ from the audited ones.** That is expected and correct: **cleaner capture, same authorship.** F-3's confounds are unaffected.

## 2. What the deliverable has to be

**The clean-room arm must exist as MOTION, under the same camera and cadence grammar as the HITL arm, so that the only variable is the build.**

- Same camera pose, same framing, same clip length, same cadence as the HITL reference. **If any of those cannot be matched, say which and why — do not silently substitute.** A comparison with two variables answers nothing, and this wave has already paid twice for comparisons missing an arm.
- The review camera now exists: `CAM_PITCH_REVIEW := -41.0` behind `--audience=review`, distance held at **34.0 m**, from your own `1475ed9`. **Matt has confirmed the `_v3` MP4s show the character facing forward.** Use the review audience.
- **Do not modify `CAM_PITCH`.** It is the measurement pitch and every landed S2A/S2B/S2C differential was captured through it. Your own comment calls a const edit there "the C-3 error class through a sixth door."

## 3. ⚑ Pre-fire resource projection is MANDATORY (#1.1)

**This tranche has already halted twice on host resources.** Free space was **2.7 GB** at HALT #2; a `matt_to_do` red-disk warning predicted that failure by name a day before it happened and was not read.

**Before capturing anything:** declare frames × bytes-per-frame, verify against `df`, and **state the margin.** If the projection fails, **DO NOT FIRE** — report it. Sending a 25-minute capture into a host that fails at minute 24 is worse than not starting.

⚑ **The 3A recapture runs before this one and consumes disk.** Re-measure after it completes; do not reuse its projection.

## 4. ⚑ Evidence that must survive

`s2c38` (2,106) · `s2c38b` (2,106) · `s2c12` (874) are the **sole surviving pre-fix frame sets** — the `harness_logs` duplicates were deleted in the disk crisis. `run_s2c_rows38.sh` runs `rm -f "$USERDIR"/*.png` after `UDIR="s2c38${SUFFIX}"`.

> ⚑ **CORRECTION, 2026-08-25, MEASURED BY DRAX — the sentence above is WRONG for rows 1–2, and it was mine.** `harness_logs/s2c_rows12_2026-08-25` and `…-25b` each hold **874 PNGs, sampled md5 agreeing with the userdir copy.** The rows-1-2 pre-fix evidence is **triplicated, not singular.** I asserted a deletion as measured fact and never measured it — **`#79` cl. 1**, and the second conviction of mine in one session under the clause jack-ryan had *already* ruled against me an hour earlier. It errs in the safe direction (over-caution about evidence) and it is still a false claim in an operative dispatch, which is why it is corrected here rather than in a note.
>
> ⚑ **AND THE FAR MORE DANGEROUS FINDING, also drax's:** `run_s2c_rows12.sh` **wipes `s2c12` on EVERY invocation, with ANY argument.** `USERDIR` was hardcoded, `--out=user://s2c12/` baked into all 24 arm invocations, `SUFFIX` read but reaching only `$OUT`, and an unconditional `rm -f "$USERDIR"/*.png`. **`s2c12` is the pre-fix capture the sealed L-29(6) adjudication rests on.** The fresh-suffix instruction I wrote — safe and executable in `run_s2c_rows38.sh` — **was not executable in its sibling, and following it would have destroyed the evidence it was written to protect.** Fixed by drax at `713f487..0800f32`, with all five pre-fix directories `chmod a-w` before anything ran. His own verdict on it: *"I fixed the runner that had bitten me and did not sweep its sibling"* — and the rows-1-2 triplicate survived **"because of the disk-filling `cp` that the rows-3-8 fix removed at its cause — protected by a bug, not by a decision."**

**Verify any resolved output path matches none of those three before writing.** The loss would be **silent**.

## 5. Image handling — a hard limit killed one of your sessions today

`400 invalid_request` — **image dimensions >2000px on many-image requests**, at ~128 accumulated image blocks. That is what killed the camera/WW-AB session, after 126 tool calls, with `completed` in the status field.

⚑ **CROP at native resolution. Never downscale.** Full ruling: `knight-rider/rulings/2026-08-25-the-2000px-wall-killed-drax-and-the-obvious-fix-destroys-the-detail-matt-asked-for.md`. A recovery brief of mine told you to `sips -Z 1600`; **that was wrong as a general rule and I wrote it as one.** The features under investigation are **1–3 px** — downscaling averages them out of existence in the originals *and* in ours at the same rate, manufacturing a false "no difference."

**Budget images explicitly. Well under 100 blocks.** If the analysis needs more looking than one context holds, that is **two dispatches**, not one degraded one — say so and stop.

## 6. ⚑ What you are FORBIDDEN to do

**Do not rule which arm is better. Matt picks.**

His critique is already on the record and it is a *design* judgement, not a measurement: our VFX are *"basic representations"* lacking the originals' internal depth — *"claw and sword metal scraping timing and intermittent laser effects, alternating through a specific color range as well as smoke and wind effects,"* and possible *"cavitation or gravity appearance effects to show distortion of the environment."*

**That critique routes to gandalf** (he has it queued explicitly) **and to Matt. Not to this dispatch.** Produce the comparison; do not adjudicate it. Surfacing an observation is welcome; **ruling is not.**

## Quality criterion

**Game-quality goal:** Matt's judgement that our VFX lack the originals' depth is currently **unevidenced in motion** — the clean-room arm does not exist as something he can watch beside his HITL run. This dispatch produces the artifact that lets him decide with his eyes instead of from stills.

**Refutation conditions — surface before executing if any apply:**
- The HITL arm's camera/cadence cannot be matched, so the comparison would carry **two** variables.
- Rendering off HEAD produces something that visibly is not the audited effect (**would contradict gandalf's ground 1 — stop and route back to him**).
- Resource projection fails.
- Acceptance criteria can pass without producing a watchable side-by-side.

## Acceptance criteria

1. Pre-fire resource projection **stated with margin**, re-measured after the 3A recapture.
2. Clean-room arm rendered **off HEAD**, unpinned, review audience.
3. Camera / cadence / clip-length parity with the HITL arm **stated explicitly**, including any unmatched dimension and why.
4. Both arms watchable as motion; deliverable path named.
5. The three pre-fix frame sets **verified intact** after the run.
6. No modification to `CAM_PITCH`.
7. `AGENT_STATE.md` updated; dispatch header moved off `PENDING`. *(A completion record filed while the header still reads PENDING is the stale-header defect this wave has four instances of.)*
8. `git commit --only <paths>`; verify **before** with `git diff HEAD --name-status -- <paths>`, **after** with `git show --stat HEAD`. **Never `git diff HEAD~1` alone.** `git -C ~/Games/reincarnated-godot` on every git call.
9. **Do not touch `tmp/br2watch/measure/census.json`** — 23 days dirty, another workstream's, under review at `qa/pending/2026-08-25-a-23-day-old-uncommitted-ocr-regression-nobody-owns.md`. You already made that call once and it was right.
10. No verdict on which arm is better.

## Out of scope

- Any change to the Whirlwind effect itself. **This renders what exists; it does not improve it.** Improving it is downstream of Matt's pick.
- The depth critique (gandalf's).
- 3A recapture work.
- Sealing or tagging.

## Push

Matt authorized push across repos **this session only** — it expires at the session boundary. Do not stage untracked files; the tree carries other sessions' capture directories, and **four other agent sessions are live.**
