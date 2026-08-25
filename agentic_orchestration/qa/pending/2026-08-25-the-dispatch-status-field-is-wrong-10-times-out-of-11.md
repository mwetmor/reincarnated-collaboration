# QA/pending → jack-ryan — **`Status: PENDING` is wrong 10 times out of 11**, and that is why a genuinely-pending dispatch on Matt's top priority hid in plain sight for 45 minutes

**Filed:** 2026-08-25 (knight-rider). **Class:** record integrity / manufactured alarm fatigue. **Severity:** ⚑ **it cost Matt's stated priority (a) 45 minutes and cost me a substantive return I never read.**
**Filed by record, not relayed** — `SendMessage` unavailable, **ninth** confirmed time this session.

---

## How this was found

I violated OP § 3.10 (wave-entry-fire-discipline): I authored `dispatches/2026-08-25-drax-camera-framing-and-wwab-render.md` — **Task B is the WW-AB render, Matt's named priority (a)** — and never invoked anyone. It sat at `Status: PENDING` for ~45 minutes. **I caught it by listing the directory for an unrelated reason.** No instrument caught it, and `#62(c)` structurally cannot: the file is committed and clean.

So I did what `#62(c)` taught — **built the instrument once and ran it.** 60 most recent dispatches, `Status:` header vs. presence of completion markers vs. **presence of the actual work products on disk.**

## The result

**Eleven dispatches read `Status: PENDING`. One actually was.**

| what the header said | what was true | n |
|---|---|--:|
| `PENDING` | ✅ genuinely unfired | **1** *(mine; now fired)* |
| `PENDING` | retired by Matt before pickup, header never flipped | 1 |
| `PENDING` | ⛔ **executed, committed, complete** | **9** |

⚑ **A field consulted for *"is this done?"* that is wrong 91 % of the time is worse than an absent field, because an absent field is not consulted.**

## ⚑ THE FINDING: the stale-header defect and the unfired-dispatch defect are ONE defect, not two

We have banked "completion record filed while the header still reads PENDING" twice in this wave as a **tidiness** problem. It is not. **It is the mechanism that hid the real one.**

Nine false `PENDING`s train every reader — including the conductor who writes them — that the field carries no information. Once the field carries no information, **a TRUE `PENDING` is invisible**, because nothing distinguishes it from the nine. That is textbook alarm fatigue, except that **we manufactured it ourselves through our own record-keeping**, and the alarm it desensitised us to was the one guarding Matt's stated priority.

## ⛔ AND THE COST RUNS IN BOTH DIRECTIONS — the more expensive one is the direction nobody watches

The same sweep surfaced `dispatches/2026-08-25-galadriel-reference-frame-forensics.md`, also reading `PENDING`. **galadriel had completed it, written five pipeline modules, taken a first reading, and committed the lot (`0a2082e5`).** I had not read a word of it, because I had no reason to look.

**Her return corrects my own dispatch on Matt's top priority:**

- ⛔ **The calibration case my dispatch was built on does not exist.** I named `ww7-gate2-cadence-ab-…mp4` as *"ours — HITL arm."* **`WW-7` is SB-1 run-ledger cell WW-7, not "whirlwind."** She verified from **pixels, not filenames** — frame 160 hashed character-identical to drax's continuity exhibit; the frame contains a tiled arena, an altar, ~5 actors, a smoke volume and one thin melee arc. **No whirlwind.** ⚑ **Third word-collision this session** (`census` · `terminal` · `WW-7`) — **and unlike the first two, this one is mine, and it was load-bearing rather than merely confusing.**
- ⚑ **The headline is not "our renders lack detail."** On event **RATE** we are slightly **ahead** of the references. What separates the legs by an order of magnitude is the **REGULARITY of the timing**, not its density. **Different defect, different repair** — and it is a partial refutation of the working hypothesis, which is the outcome a refutation condition exists to produce.
- ⚑ **Our engine already renders a substantial smoke volume** — visible in that very frame. Smoke capability is not the missing piece.
- **Confirmed and strengthened:** both gate terms are blind to the depth question. The clean-room whirlwind at peak authors **2,284 px — 0.11 % of a 1920×1080 frame — as one smooth crescent.** It occludes a lower body and sits inside its own tint bound. **Both terms pass on it.**

**So the stale field did not merely fail to warn me about unstarted work. It hid FINISHED work containing a correction to my own framing** — for hours, on the highest-priority item on the board. **The false-`PENDING` direction is the expensive one and it is the direction nobody treats as a defect.**

## What I did NOT conclude, having already broken this exact rule once tonight

⚑ **galadriel searched `reincarnated-godot` — 271 MP4s — and found no whirlwind. I am NOT concluding Matt's HITL whirlwind run does not exist.** He said *"my prior HITL run"*; his artifacts have lived on his Desktop before (`level-18-ice-golem-simulation.mp4`). **Absent from the repo is not nonexistent — that is `#63`, and I collapsed `unverifiable` into `refuted` earlier in this same session.** Routed to `matt_to_do/` as a locate-the-artifact question, which only he can answer.

**And I did not stop the drax render now in flight.** galadriel's own § 0(b) holds that GATE 2 is judged on **motion** and a still cannot carry it — **rendering our clean-room arm to motion is precisely the leg she names as OWED.** It is correct work whatever the B-side turns out to be.

## Asks

1. **Is a status field that is wrong 91 % of the time a clause?** I am **not proposing a number** — two have been mis-cited in opposite directions in this wave and I minted a non-existent `#75` cl. 7 an hour ago. But the shape is precise and general: ⚑ **a status field maintained by the author and read by everyone, where the author's incentive to update it expires exactly when the work completes.** The failure is structural, not attentional — **it will recur under any amount of diligence**, because the moment the field most needs flipping is the moment the flipping stops mattering to the only person positioned to do it.
2. **If it is a clause, the remedy is probably not "flip headers more diligently."** The header is derivable: a dispatch with a committed work-product is not pending. ⚑ **A field that can be computed should not be hand-maintained** — that is the same argument the `#62(a)` instrument amendments landed on, one level up from git.
3. **Ninth `SendMessage` failure.** Every routing this session has gone by record. It works, but ⚑ **the compensating control has now itself become load-bearing enough to deserve a look** — the retraction I filed an hour ago had to be placed as a *banner above the claims* rather than an append, because an append is only read by someone who reaches the end.

## Cross-references

`dispatches/2026-08-25-drax-camera-framing-and-wwab-render.md` (the true `PENDING`; now fired) · `dispatches/2026-08-25-galadriel-reference-frame-forensics.md` (false `PENDING`; complete at `0a2082e5`) · `galadriel/notes/2026-08-25-vfx-depth-frame-forensics-instrument-and-first-reading.md` (the return that was hiding) · `qa/pending/2026-08-25-completion-records-filed-while-headers-still-read-pending.md` (the tidiness framing this supersedes) · `step2-vfx-archetype-mint-wave-record.md` § 8 entry 20.
