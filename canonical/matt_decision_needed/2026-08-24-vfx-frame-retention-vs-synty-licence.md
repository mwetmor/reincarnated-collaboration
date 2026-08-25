# Matt decision — the VFX run's evidence insurance cannot live in the repo, because Synty's licence forbids it

**Raised by:** knight-rider, 2026-08-24
**Occasioned by:** drax's stage-1 return on the Step-2 build wave. He flagged it correctly as *"a decision that is not mine."* It is not mine either — it is a licence question with a cost attached.
**Blocking:** nothing right now. **The exposure grows with every row minted**, which is why it is filed rather than carried.

---

## 1. The collision, in three lines

1. **jack-ryan's Gate-1 made frame retention the wave's insurance** — and specifically corrected me for aiming the insurance at the wrong hazard. The risk is not an unscored S-axis; it is **S becoming uncomputable without a re-mint.** The remedy is retaining raw + control frames with camera, tonemap and seed pinned per arm.
2. **The frames cannot go on the remote.** `reincarnated-godot/.gitignore` lines 20–22, licence-grounded, not a size convenience: raw Synty IP *"must NOT go on a shared remote (Synty license)."* Harness PNGs render Synty geometry and fall under it. **I verified the rule rather than taking it on report.**
3. **So the insurance currently exists on exactly one machine — this Mac — and nowhere else.**

## 2. What IS protected, so the decision is scoped correctly

**Partial insurance already exists and drax built the right half of it unprompted:**

- **`transfer_function` now travels in `stage_meta` on every arm**, read off the live `Environment`. His reasoning is the correct lesson from this run: *"the tonemap is what retired HLF and no record said so."*
- **Render logs, receipts and derived JSON are committed and pushed** — `sensitivity.json`, `gate.json`, `render.txt`, per-arm metadata.
- **Camera, tonemap and seed are pinned and recorded per arm.**

**The gap is the pixels only.** Everything needed to *interpret* a frame travels. The frame itself does not.

## 3. Why the gap is not cosmetic

The whole reason retention became the insurance is that **this run has repeatedly discovered that a measurement's frame was wrong after the number was already load-bearing** — seven instances of `#64 FRAME FORM`, four of them mine. Each time, the recovery was *go back to the pixels and re-measure*. The 9.35 % cathedral anchor is under an open galadriel verdict right now for exactly this reason.

**If this machine is lost, that recovery path closes** and every affected row needs a re-mint — not a re-measure. Re-mint is the expensive operation; capture is cheap (measured: **4.39 s/arm**, 14 arms ≈ 60 s of render). **The asset at risk is the authoring, not the rendering.**

## 4. The fork

**(A) Accept the exposure.** Frames are local-only; if the machine is lost, affected rows re-mint. Costs nothing now. Bets the run's evidence base on one disk.

**(B) External storage outside the repo** — an encrypted external drive or a private non-shared backup. **Turns on a licence reading I am not qualified to make:** does *"shared remote"* mean *"any remote"*, or *"a remote other people can read"*? A private single-user backup may or may not be inside the prohibition. **This is the crux and it is a judgment about Synty's terms, not about our tooling.**

**(C) Retain a licence-safe derivative instead of the frames** — e.g. the difference masks or the derived descriptors, which encode the authored effect but arguably not the Synty geometry. **Cheaper legally, weaker as insurance:** a derivative answers the questions we already knew to ask. The whole lesson of the seven `#64` instances is that **the question we needed to ask later was not the one we asked at capture time.**

**(D) Re-scope the insurance** — decide the S-axis is not worth insuring, and accept re-mint as the recovery path by design. Makes the Gate-1 finding moot rather than unmet, which is at least honest.

## 5. What I am NOT doing, and why it is parked rather than decided

**I am not picking (B) and quietly making a backup.** ADR-006 is read-only-by-default for external systems, and a licence question is above my seam in the plainest possible way. **Nor am I letting the Gate-1 requirement lapse silently** — an unmet gate finding that nobody records is the failure this wave already produced once, when an escalation died by supersession rather than by ruling.

**Related open item:** `matt_to_do/` T18 already carries a **Synty licence / AI-terms exposure** item surfaced by the Codex audit. **This is a second face of the same underlying question** and the two may be worth ruling together — if T18 produces a reading of the licence, that reading probably decides this.

## 6. What unblocks on a ruling

- **(A) or (D):** nothing changes operationally; I record the accepted exposure against the wave and the Gate-1 finding is dispositioned rather than left open.
- **(B):** drax gets a retention target and the insurance becomes real. One-time setup.
- **(C):** needs galadriel to say which derivative preserves her measurement options — **do not route (C) to drax directly**, he would have to guess at her instrument, which is the error class this run keeps producing.

*Filed by knight-rider, 2026-08-24.*
