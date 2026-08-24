# Dispatch — 2026-08-24 — drax — A-1 / A-3 body pipeline (transformation + totem delegate)

**Status:** PENDING — **QUEUED behind `drax/v<X.Y>-s2a-mint-tranche-1`.** Do not start until tranche 1 lands.
**From:** knight-rider (Step-2 build wave, carve-out #2)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Approved by:** Matt, 2026-08-24 — tier-2 rulings **L-36 / L-37**
**Pattern:** B (dedicated session)

---

## Context

Tier-2 law is **SEALED** (sealed spec § 5): **A-1 YES · A-2 ADOPT + WW-AB · A-3 same pipeline as A-1 · Class B REJECTED.** Reopening any of it is a **HALT to Matt, not a sequencing choice.**

A-1 and A-3 were ruled to share **ONE body-acquisition pipeline** — that ruling is what dissolves the § 5.1 double-buy risk. This dispatch establishes that pipeline once and uses it twice.

**A-1 — `self_buff` → `transformation` sub-shape.** The genuine split the run found: **a transformation REPLACES the silhouette; a decal buff must NOT touch it.** Opposite requirements on the same property; one canonical cannot serve both. No recolour of a floor decal produces a werewolf, and the alternative — `Werewolf` shipping as a tinted floor decal — would be the most visible design failure available to us.

**The body is already owned.** Synty `SK_Chr_Werewolf_01.fbx`, live in `vh_race_rig` via `vh_caster.gd:38`, 1.80 m. **A-1's cost is the swap + transition treatment, not model acquisition.** Do not go shopping for a body you already have.

**A-3 — `totem` delegate body.** Tier-1 can recolour what a totem *throws*; it cannot recolour what a totem *is*. Matt's ruling: source **Synty-first; if no fitting Synty body exists, create via the ChatGPT → Meshy pipeline.**

---

## ⚠ SYNTY-CLEAN LINEAGE GATE — BINDING, carried verbatim per conductor guard

> **the 3D-gen input chain must contain no Synty-derived pixels or geometry as generation inputs** (S16 gen-AI block; vision-LLM *judging* permitted under the June-2026 relaxation; 3D-*generation from* Synty assets is not, absent the Custom Licence).

**Operationally, before any Meshy call:**

- **No Synty-derived pixels or meshes anywhere in the input chain.** Not as a reference image, not as a style prompt, not as a screenshot, not as a retopology target, not "just for proportions."
- **Vision-LLM *judging* of Synty assets is permitted.** Vision-LLM or 3D-gen **generation from** them is not. The distinction is the activity, not the file format — the governing clause is activity-scoped.
- Stage-4 of the ensemble asset pipeline carries the same gate; this dispatch does not weaken it.
- **If you cannot construct a Synty-clean input chain for a needed body, that is a HALT to knight-rider, not a judgment call at the keyboard.** The clearance question is cheap to ask and expensive to get wrong.
- Record the input chain for every generated asset — what went in, from where. **A lineage you cannot show is a lineage you cannot defend.**
- **The permitted input chain, stated positively** — because everything above says only what may NOT enter, and the ChatGPT step will want a style reference, and **the nearest style reference to hand is a render of our own game, which is Synty pixels.** That is the most likely real violation, so it is closed here explicitly:
  > A text prompt authored from `canonical/reap-die-rise-story/style-register.md` **PROSE**, plus non-Synty third-party reference art whose source you can name. **In-engine screenshots, `Assets/` renders, and any capture of a scene containing Synty geometry are Synty-derived pixels — including when used "just as a style reference" for the ChatGPT step.** If you need to convey our look to the generator, **convey it in words.**

**Synty-first is not a preference, it is the cheap path AND the clean path.** Exhaust it before opening the Meshy lane at all; a Synty body needs no lineage argument.

---

## Required reading

1. Sealed spec **§ 3.1.3** (`self_buff`, the sub-flag) · **§ 3.1.4** (`totem`)
2. ⚠ **§ 5 and charter L-36 / L-37 are QUARANTINED — do not read them.** They are this dispatch's most natural sources and they are forbidden, because they describe the adopted `whirlwind` lineage in build detail and **you are the agent who mints `whirlwind` clean-room.** Contaminating that experiment costs the run its calibration datum; nothing in this dispatch is worth that price.

   **Everything they give you is extracted here, and the extraction is complete:**
   - **A-1 YES** — `self_buff` gets a `transformation` sub-shape
   - **A-2 ADOPT + WW-AB** — not this dispatch
   - **A-3 same pipeline as A-1** — one body-acquisition pipeline serves both. **This is the ruling that dissolves the § 5.1 double-buy risk**, and it is why this dispatch establishes the pipeline once and uses it twice.
   - **Class B REJECTED** — Matt verbatim: *"We should only adopt one move per skill-type, not one more per kit."*

   If you believe you need something from § 5 that is not in that list, **that is a question for knight-rider, not a judgment call at the keyboard.** The same quarantine covers the carve-out #2 request.
3. `canonical/reap-die-rise-story/style-register.md` — register A; a new body must sit inside it
4. `agentic_orchestration/legolas/notes/2026-08-23-synty-eula-primary-source-read.md` — the primary-source read behind the gate. Channel is **SyntyPass subscription**, single governing licence, current version binds.
5. The ensemble asset-pipeline spec, Stage-4 lineage gate
6. `vh_caster.gd` and `vh_race_rig` in `reincarnated-godot`

---

## Scope

### A-1 — transformation treatment
- [ ] **One scoped transformation treatment** — model swap + transition VFX — reused as the `self_buff` transformation sub-shape. **Scoped means one treatment reused as an archetype sub-shape, exactly as base bindings are reused. NOT "all transformations."**
- [ ] Use the **already-owned** `SK_Chr_Werewolf_01.fbx`; no acquisition
- [ ] Transition VFX: the moment of replacement must read as *a transformation*, not a pop. The silhouette change is the payload.
- [ ] Verify it composes with the `self_buff` **`buff-decal`** sub-shape without either breaking the other — they are opposite requirements on the same property and both ship

### A-3 — totem delegate body
- [ ] **Synty-first survey.** Does a fitting Synty body exist? Record what you searched and what you rejected, with reasons — a negative result needs receipts as much as a positive one.
- [ ] **Only if none fits:** ChatGPT → Meshy, under the lineage gate above, with the input chain recorded
- [ ] Delegate body integrates with the `totem` row's binding: the body is a **MODEL**; the **attack** is the `PAYLOAD-CARRIED` Tier-1 surface. Do not let the body absorb the parameterization that belongs to the attack.
- [ ] Note but do not build: L-39 measured totem delegate mobility at ≤18/97 mobile vs 55 placed-static. **VFX composes identically either way** (summon puff + delegate attacks); mobility is AI/animation, and the body rides A-3. Do not scope-creep into mobility.

### Standing
- [ ] Lineage record per generated asset (if any)
- [ ] `AGENT_STATE.md` updated; tag `drax/v<X.Y>-s2-body-pipeline-1`

## Cross-seam contract change? (Principle 6 gate)

**NO.** **Round-trip: not applicable — no cross-seam contract change in this dispatch.** Presentation-seam model + VFX work.

## Acceptance criteria

- [ ] One transformation treatment shipped, scoped, reusable as the `self_buff` sub-shape
- [ ] Transformation and `buff-decal` sub-shapes coexist without either breaking
- [ ] A-3 body sourced, with the Synty-first survey recorded (including rejections and why)
- [ ] **If Meshy was used: Synty-clean input chain documented and defensible.** If it was not used, say so — that is the better outcome
- [ ] Both bodies sit inside register A at the fixed 2.5D camera
- [ ] Round-trip: not applicable
- [ ] Tag `drax/v<X.Y>-s2-body-pipeline-1`

## Quality criterion

**Game-quality goal:** that a transformation *feels like becoming something else* — the one place in the Tier-1/Tier-2 split where a recolour provably cannot carry the fantasy. This is also the legal-assurance floor: the cheapest possible insurance against the most expensive possible surprise.

**Refutation conditions** (surface to knight-rider before executing if any apply):
- A Synty-clean input chain cannot be constructed for a needed body → **HALT, do not proceed on judgment**
- The transformation treatment cannot be scoped — it keeps generalizing toward "all transformations" → that is scope growth beyond A-1's ruling
- A-3 turns out to need a *different* pipeline than A-1 → that contradicts Matt's ruling; surface it rather than quietly forking
- Acceptance criteria can pass while the transformation still reads as a costume swap rather than a transformation

## Out of scope

- **Class B kit-signature slots — REJECTED BY RULING.** Matt verbatim: *"We should only adopt one move per skill-type, not one more per kit."* Bespoke work attaches at the **archetype level only, never per-kit.** No roster question survives; do not raise one.
- **A-2 `whirlwind`** — separate clean-room dispatch.
- Totem delegate **mobility** (AI/animation, not this dispatch).
- Re-opening any § 5 tier-2 ruling — HALT to Matt.
- Re-grading the Synty licence position. It is CLOSED single-regime; what survives is the renewal-time §1.4 diff watch.

## References

- Sealed spec § 3.1.3 / § 3.1.4 · **(§ 5 and charter L-36 / L-37 quarantined — see Required reading item 2)**
- `legolas/notes/2026-08-23-synty-eula-primary-source-read.md`
- `agentic_orchestration/workflow-upgrades.md` § U-9 (discharged as a build; the lineage gate survives as standing discipline)

---

## Gate record

- jack-ryan Gate-1 DESIGN-MODE: **PASS-WITH-FINDINGS → **amendments applied 2026-08-24**** — Gate-1 batch review, 2026-08-24.
  Quarantine propagated (§ 5, L-36/L-37) with A-3's double-buy-dissolving ruling extracted inline; the Synty gate's hole closed by stating the **permitted** input chain positively — the gate previously said only what may not enter, and the nearest style reference to hand is a render of our own game.
  Amendments approved by jack-ryan directly under **ADR-002** (dispatch documents are documentation-only). **Nothing in this batch escalated to Matt.**
