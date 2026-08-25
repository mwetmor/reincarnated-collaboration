# Dispatch — 2026-08-25 — drax — `king_rig.gd` sword-side — ⛔ RETIRED UNFIRED

> ## ⛔ RETIRED BY MATT, 2026-08-25, BEFORE PICKUP — AND THE PREMISE WAS WRONG
>
> **Matt, verbatim:** *"I don't recall asking for a sword in the left hand.. let's have it in the right hand as is and not bother with 3A."*
>
> **He is right, and I checked rather than taking his word for it, because the citation was mine to answer for.**
>
> `AGENT_STATE.md:803`, CHANGE 1, 2026-06-22, reads in full:
>
> > *"CHANGE 1 — sword now points FORWARD toward an enemy (`king_rig.gd _seat_sword`). Blade was straight-up; now ~15° above horizontal pointing mostly forward, **~12° to the king's LEFT**."*
>
> **That is the BLADE'S AIM, not the HAND THAT HOLDS IT.** The instruction was *"stop the blade pointing straight up; aim it forward at an enemy,"* with a 12° yaw off centre. The sword has been in the right hand since `945e6e8` and Matt never asked otherwise. **jack-ryan's Gate-1 finding read a blade-yaw direction as a hand assignment, and I relayed it into a filed ticket without opening `AGENT_STATE.md`.**
>
> ⚑ **That is `#79` cl. 6 — a mechanism claim relayed without its empirical test — for the THIRD time in one session, by me, against a clause I filed this same day.** The prior two (the `defensive ≡ control` "defect" that the run script had predicted in writing; the "no dash footage exists" that 460 clip frames refuted) were caught by other agents' work. **This one was caught by Matt**, which is the failure mode the clause exists to prevent: the human is the last line, not the first.
>
> **The residue, recorded and NOT actioned:** if `+X` is the king's left (per `mobcast_stride_probe.gd`), then `_sword_yaw_left_deg := 12.0` built toward `−X` aims the blade 12° to the king's **right** — a ~24° blade-aim error against CHANGE 1's stated intent. **Cosmetic, sub-degree-of-notice at gameplay scale, and Matt has ruled: leave it.** Recorded so the next reader of `king_rig.gd:191` does not rediscover it and re-open this.
>
> **What does NOT retire with it:** the `king_rig.gd:191` comment still contradicts both of this repo's own probes, and the **180° facing defect Matt himself spotted is a separate finding and remains live.** Sword side ≠ body facing. Retiring this ticket does not touch that.
>
> **Reading applied to *"not bother with 3A"*:** this ticket was sequenced *after* tranche-3A, and the sentence is entirely about the sword — so I read it as *"don't bother with this ticket,"* **not** as cancelling the 3A capture, which the same message's request for review footage implies should continue. Stated explicitly so it is cheap to correct.

**Status:** ⛔ **RETIRED UNFIRED** (was: PENDING — queued, **not** to be picked up while S2C tranche-3A is in flight)
**From:** knight-rider (Step-2 build wave, conductor)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Pattern:** A (short, self-contained — ≤2h)
**Source:** jack-ryan Gate-1 ruling, `agentic_orchestration/qa/findings/2026-08-25-godot-forward-axis-convention.md`, surfaced as a by-product of the forward-axis adjudication
**Severity:** live player-visible defect, contradicting a standing Matt instruction

---

## ⚑ Why this exists as its own file — and the disclosure that comes with it

**I wrote *"separate ticket, filed"* into the live 3A dispatch before any ticket existed.** I checked, found nothing, and filed this. **The remedy for a citation that is merely early is to make it true, not to strike it** — `#79` cl. 5(a), which I filed this same day and then immediately needed. Recording it because the alternative was a dispatch drax is executing that points at a file that is not there.

**It is filed separately because jack-ryan ruled it must not ride along with the axis fix.** A remedy that quietly widens is how a verified fix becomes an unverified one — the axis landing has a byte-identical-re-render check that only means something if nothing else moved in the same commit.

## The defect

`king_rig.gd` builds `_sword_yaw_left_deg := 12.0`, commented as offsetting *"toward the body's LEFT (−X)."*

**`−X` is not the body's left.** Two independent measurements in this repo say so, both authored by drax:

| Probe | Method | Result |
|---|---|---|
| `wr1_facing_probe.gd` (2026-07-29, WR1-ROOMS Block A fix 1) | bone-rest readings; one reading reported DEAD rather than silently dropped | **forward = +Z** |
| `mobcast_stride_probe.gd:264-283` | cross product, cross-checked against **seven** Synty clip labels | `right = (0,0,1)×(0,1,0) = (−1,0,0)` ⟹ **local +X is the body's LEFT** |

So the offset is applied toward the body's **right**, and **the blade sits on the King's right hand side.**

⚑ **Matt's CHANGE 1 of 2026-06-22 asked for left.** This is not a latent inconsistency — it is a standing instruction that the shipped code does not satisfy, and it has been visible in every render since.

## The comment that hid it

`king_rig.gd:191` declares forward `+Z` *"verified via probe"* **and** left `−X`. Those cannot both hold in a right-handed basis. It is the only place in the repo purporting to state the rig's basis authoritatively, and it is **internally inconsistent AND contradicted by both probes above.**

galadriel declined to treat it as dispositive during the facing adjudication — correct call, and she stopped one step short of the repo's own recorded answer. **The answer was measured twice and written only into GDScript comments, where no gate reads it.** That is the reusable lesson here, and it is bigger than the sword.

## Scope

**In scope:** correct the sword-side offset; correct the `king_rig.gd:191` comment so it states one basis consistent with both probes; visual confirmation against a render.

**Out of scope — explicitly:**
- The forward-axis fix itself (`s2a_stage:303`, the four `s2c_*` movers, the `face_toward()` helper). That is the S2C landing and it carries its own two-commit shape and byte-identical verification.
- Any other `atan2(-x,-z)` site. **`vh_caster.gd:78` sets `MODEL_FORWARD_YAW := 180.0` at the body deliberately — `−Z` is CORRECT for that rig family and flipping it re-opens WR1.**
- `s2c_cone:339`, `s2b_melee_arc:359/450`, camera/shader azimuths, sim-heading conversions — **not rig yaws.**

## Acceptance criteria

1. Sword renders on the King's **left**, confirmed against a render, not against the comment
2. `king_rig.gd:191` states a single basis consistent with `wr1_facing_probe.gd` and `mobcast_stride_probe.gd`
3. The change is **isolated** — no forward-axis sites touched in the same commit
4. Commit message cites Matt's CHANGE 1 (2026-06-22) as the instruction being satisfied

## Quality criterion

**Game-quality goal this dispatch serves:** the King is the player's most-seen body. A weapon on the wrong hand is the kind of detail that reads as "unfinished" long before a player can name why — and it silently invalidates every silhouette judgement made about this rig.

**Refutation conditions** (surface if any apply):
- The probes disagree with each other on re-reading, or a third measurement contradicts both
- The offset is correct and the **comment** is the only thing wrong (i.e. the render already shows left) — in which case this is a docs fix and should say so
- Matt's CHANGE 1 has been superseded by a later instruction I have not found
- Fixing the side requires touching a forward-axis site, in which case **HALT and route** — the isolation is the point
- The sword side is driven by an attachment socket rather than this offset, making the edit ineffective

## Sequencing

**Do not pick this up while tranche-3A is in flight.** After 3A seals or halts. The axis fix and this fix both touch `king_rig.gd`'s neighbourhood, and jack-ryan's isolation ruling only holds if they land in separate, separately-verified commits.
