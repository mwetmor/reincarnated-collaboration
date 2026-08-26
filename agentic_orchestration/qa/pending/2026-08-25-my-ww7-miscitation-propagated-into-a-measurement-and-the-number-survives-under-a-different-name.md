# QA/pending → gandalf + jack-ryan + drax — **my `WW-7` mis-citation propagated into drax's measurement.** The HALT survives, the number survives, and **the label on one side of it does not**

**Filed:** 2026-08-25 (knight-rider). **Class:** referent error, propagated downstream. **Severity:** ⚑ **routed to gandalf; correct it before he acts on it.**
**Filed by record, not relayed** — `SendMessage` unavailable, **tenth** confirmed time this session.

---

## ⛔ The error, and it is mine, and it is upstream of everyone else's work

I authored `dispatches/2026-08-25-drax-camera-framing-and-wwab-render.md` naming `ww7-gate2-cadence-ab-….mp4` as **"ours — HITL arm."** It is not. **`WW-7` is SB-1 run-ledger cell WW-7**, and it has nothing to do with whirlwind.

**Verified by me from the script's own header, not from its name:**

```
run_ww7_gate2_clip.sh — SB-1 Cell WW-7 (GATE-2 CLIP). THE A/B CADENCE CLIP,
RE-RENDERED AT THE CAMERA GATE 1 PASSED.
  ⚑ WHY THIS EXISTS. Matt's eyeball gate R-CPB-17b has two gates…
  source: …/2026-08-13-sb1-a2gr-lookdist/a2gr-lookdist-cadence-ab.mp4
```

**`grep -c -i whirlwind run_ww7_gate2_clip.sh` → `0`.**

galadriel reached the same conclusion independently and by a better method — **from pixels, not from headers**: frame 160 hashes character-identical to drax's continuity exhibit, and the frame holds a tiled arena, an altar, ~5 actors, a smoke volume and one thin melee arc. **No whirlwind.**

⚑ **drax then measured against it and labelled it `HITL` throughout his return — because my dispatch told him to.** He did nothing wrong; he consumed the reference his dispatch named, which is the correct behaviour. **The defect entered at authoring and travelled.**

## ⚑ What this is an instance of, and why it is the worst-placed one this session

Fourth word-collision (`census` · `terminal` · `WW-7` · `totem`), **second that is mine, and the only one that reached a second agent's measurement and was on its way to a third's ruling.** The other three cost confusion. **This one was about to be ruled on.**

**`#64` — a name is not a referent.** The chain was: a filename containing `ww` → my inference *"whirlwind"* → a dispatch clause → drax's stand-off and fov figures → a routed HALT to gandalf. **At no point between my inference and this filing did anyone open the file to ask what it was of**, because after the first step it was no longer a guess, it was a citation.

## ✅ WHAT SURVIVES UNTOUCHED — which is most of it

**1. The HALT is correct and its reasoning is independent of the reference.** `wwcr_stage.gd` has no `player_lock` camera and no `--plk`; it has `combat` and `inspect`, full stop. **Matching any external camera needs a hook in a `wwcr_*` file — one of the 12 files quarantined by the clean-room mint § B.3.** That is true whichever clip is on the other side. drax halted rather than working around it, per the dispatch's own refutation condition 1. **Correct call.**

**2. Task A is entirely unaffected** — it was never about whirlwind. And it carries the session's **eighth** instance of the recurring shape, this one also mine:

> ⚑ My § 0 verification was *"`s2a_stage.gd` still reads `CAM_PITCH := -55.0`"* — **literally true, and it does not answer its own question.** `CAM_PITCH` is HELD at −55.0 **deliberately**, as the MEASUREMENT pitch, because moving it would silently re-pose every landed S2A/S2B/S2C differential. The review camera moved via a **new** constant, `CAM_PITCH_REVIEW := -41.0`, read through `_cam_pitch()`. **A grep for a constant is the one instrument guaranteed to miss a change whose entire design was to avoid touching that constant.** The work had landed at godot `1475ed9`, 18:03 — 25 minutes after I authored the dispatch asking for it.

**3. My § A.4 model was not refuted by measurement — it was fed the wrong camera**, which is why it inverted. The reference is `player_lock`, not `arena_full`. drax notes that my own instruction — *put the model on trial rather than Matt's eye* — is what found it. **A model that inverts under a wrong input is not thereby a wrong model, and `#63` applies to my own hypotheses too.**

## ⚑ THE NUMBER SURVIVES, AND UNDER ITS CORRECT NAME IT IS MORE USEFUL, NOT LESS

drax measured **px/m @1080: 81.88 vs 43.64 → 1.971× apparent height → 0.979 OCTAVES.** Both figures are real and derived from declared camera parameters.

| | as drax labelled it | ⚑ **correct name** |
|---|---|---|
| the 81.88 side | *"the HITL arm"* | **SB-1 `ww7-gate2`, `player_lock` k=0.665 — the camera Matt RATIFIED at R-CPB-18 as the pose his gate-2 eye judges from** |
| the 43.64 side | clean-room `combat` | unchanged — clean-room `combat`, 34 m, fov 40 |
| what the gap is between | our whirlwind ↔ Matt's HITL run | **our whirlwind ↔ the camera Matt ratified for judging feel** |

⚑ **Re-named, the finding gets STRONGER and lands directly on Matt's priority (a).** *"Our clean-room VFX is a two-octave-ish mismatch from an artifact we cannot even locate"* would be a weak claim. ⚑ ***"We are rendering our VFX for judgement at HALF the apparent scale of the camera Matt himself ratified as the gate-2 viewing pose"*** **is a strong one, it is measured, and it is actionable now.**

And drax's own § A.7 warning rules why it matters rather than being cosmetic: **band statistics index in PIXELS, not world units.** A one-octave scale variable in a comparison judged on density / palette knee / cadence read / FX draw **does not degrade that comparison, it decides it — and it returns a clean number while doing so.**

## ⚑ AND THE DELIVERED ARTIFACT MAY REFRAME MATT'S HYPOTHESIS ENTIRELY

drax delivered **the first clean-room whirlwind MOTION artifact that has ever existed** — 1920×1080 h264 60 fps, 210 frames, both arms (`combat_fxon` / `combat_fxctl`), rendered through the mint's own unmodified `CAPTURE=seq` path from a frozen copy into a fresh stamp. Plus a 2× magnified pair, with the caveat in the filename because **the filename is the only thing that travels with a gitignored artifact.**

⚑ **At the clean-room camera the entire subject is a 249×254 px island = 3.05 % of frame area, and the effect is barely judgeable.** That independently confirms my § A.4 COMPOSITION hypothesis — 97 % empty plane around a 3 % subject island, on a stage with no rock and no terrain at all — which drax notes I had attached to the wrong task. **Right about a mechanism, wrong about where it applied.**

**Put beside galadriel's finding, a third reading of Matt's priority (a) becomes available and nobody has tested it:**

| finding | source |
|---|---|
| the whirlwind at peak authors **2,284 px = 0.11 % of frame** as one smooth crescent, and **both gate terms pass on it** | galadriel |
| the whole subject is **3.05 % of frame** at the judging camera | drax |
| on event **RATE** we are slightly **AHEAD** of the references; the gap is timing **REGULARITY** | galadriel |
| we render a substantial smoke volume already | galadriel |

⚑ **Matt's stated diagnosis was *"the VFX lack the depth of the originals."* Three independent measurements now suggest a competing explanation that costs far less to fix: we may be looking at adequate VFX from twice too far away, with metronomic timing.** **That is not established** — it is a hypothesis with three supporting measurements and no test yet, and the honest next move is a re-render of the same arms at the ratified `player_lock` camera, which is exactly what the § B.3 quarantine currently blocks.

## Asks

1. **gandalf — the routed item reaches you with a wrong label on one side.** The HALT stands; **re-read the octave figure as *"gap to the ratified gate-2 camera,"* not *"gap to the HITL arm."*** The § B.3 quarantine question you are being asked to rule on is unchanged, but **the prize for lifting it is different and larger than the routing said**: it is not "match a lost reference," it is "judge our own VFX at the pose Matt ratified for judging."
2. **jack-ryan — this is the fourth word-collision and the first to reach a downstream measurement.** Not proposing a number. The shape: ⚑ **an identifier inferred from a filename becomes a CITATION at the moment it is written into a dispatch, and a citation is not re-derived by anyone downstream — it is consumed.** The cheapest refuting test is one command against the artifact's own header, and the expensive part is that **it must be run by the author, because after authoring, nobody's role includes doubting it.**
3. **drax — nothing is owed back.** Your halt, your measurements and your Task-A findings all stand; only the word `HITL` on one column is struck. **Your `CAM_PITCH_REVIEW` finding corrected my verification method, and your domain-vs-channel clause shape is better than mine** — see below.

## ⚑ Conceding drax's clause shape over my own

I proposed the distinguishing property was **"does the control's REFUSAL have a channel to reach anyone."** drax proposes **"was the control's DOMAIN ever derived."** He is right and I am withdrawing mine:

> **Domain covers all five instances; channel covers four** — `git diff HEAD~1` *had* a channel, *used* it, and still answered wrongly. ⚑ **In all five the mechanism was correct and the object it applied to was ASSUMED — which is exactly why a correct mechanism tested against an assumed object AGREES WITH ITSELF.**

That last clause is the precise diagnosis of my own `chmod` error, arrived at independently by the person I had wrongly accused with it. **And it generalises to this filing's subject**: `WW-7` was a mechanism (a citation) applied to an assumed object (a whirlwind), and it agreed with itself all the way to a routed ruling.

## Cross-references

`dispatches/2026-08-25-drax-camera-framing-and-wwab-render.md` (CLOSED, `83a5d531`) · `galadriel/notes/2026-08-25-vfx-depth-frame-forensics-instrument-and-first-reading.md` (`0a2082e5`) · `reincarnated-godot/scripts/run_ww7_gate2_clip.sh` (the header that settles it) · `canonical/matt_to_do/2026-08-25-where-does-your-hitl-whirlwind-run-live.md` · `qa/pending/2026-08-25-chmod-a-w-…md` (the retraction where drax's clause shape is recorded).
