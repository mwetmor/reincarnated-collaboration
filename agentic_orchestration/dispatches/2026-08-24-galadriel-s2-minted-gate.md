# Dispatch — 2026-08-24 — galadriel — Step-2 MINTED GATE (standing procedure + tranche-1 scoring)

**Status:** PENDING — **blocked until drax lands `drax/v<X.Y>-s2a-mint-tranche-1`**
**From:** knight-rider (Step-2 build wave, carve-out #2)
**To:** galadriel (visual perception + UX-similarity steward)
**Approved by:** Matt, 2026-08-24
**Pattern:** B (dedicated session; the procedure half is standing and outlives this tranche)
**Position in wave:** drax mints → **you gate** → gandalf DRIFT-CRITIC.

---

## Context

The VFX archetype-binding run **SEALED 2026-08-24**. Step 2 builds against T-A. You are the gate between "drax minted something" and "it is bound." **This dispatch has two halves, and the first outlives the second:**

- **(A) Author the standing minted-gate procedure** — the rubric applied per row for the whole 24-row wave.
- **(B) Apply it to tranche 1** — `melee_strike`, `ground_targeted_circle`, `aura`.

Your P3 selection gate already produced the **Judge-To corpus**. The minted gate is the From/To comparison: **Judge-From** = drax's Metal capture of the minted effect; **Judge-To** = the source-game reference frame-set for that row. You built the To side; you now score the From side against it.

**One thing worth naming before you start.** In the run just sealed, you **refused to label a frameset rather than guess**, and shipped `judgment/README-EMPTY.md` explaining why. A save-file decode confirmed you 3.5 minutes later, and a mislabeled frame would otherwise have entered the P3 corpus as a skill that isn't even in the build. That HALT was worth more than a fast answer. **The same licence applies here:** a minted effect you cannot score is a HALT with reasons, not a number you invent.

---

## Required reading

1. **`gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md`** — **STATUS: SEALED; the STATUS line governs the filename.** Read **§ 1** (design law), **§ 1.1** (L-19 owner criterion), **§ 1.2** (style register — what "S" is scored against), **§ 2.3** (the seven P0-b constraints), **§ 3.0** (column semantics), and the three tranche-1 rows (**§ 3.1.1, § 3.1.2, § 3.1.8**).
2. Your own `galadriel/notes/2026-08-24-vfx-p3-selection-gate.md` **+ delta** (delta supersedes row-by-row).
3. `galadriel/captures/2026-08-23-vfx-p2-gd-framesets/framesets.json` **v2**.
4. `canonical/reap-die-rise-story/style-register.md`.
5. `dispatches/2026-08-24-drax-s2a-mint-tranche-1.md` — what drax was told to build, including his mint note (`drax/notes/2026-08-24-s2a-mint-note.md`). **Score against T-A, not against his note** — but read the note, because a divergence between the two is itself a finding.

---

## (A) The standing procedure — what the gate must contain

Author it at `agentic_orchestration/galadriel/notes/2026-08-24-s2-minted-gate-procedure.md`. It must operationalize, at minimum:

1. **The § 3.2 judging criterion** — readability at our gameplay camera · parameterizability (recolour / rescale / motif-swap survivable) · style-register fit. Three axis scores per row, with receipts, exactly as P3 carried them.

2. **The L-19 causality check — `action-CAUSED` vs `action-DECORATING`.** Matt's criterion of record, verbatim in the spec § 1.1:
   > *"the diablo franchise does a great job of making it feel more real as a plausible physical manifestation of exceptionally rapidly spinning weapons, clashing into flesh, bone and armor, whereas the Grim Dawn EOR Warlord's artistic rendering of the same move feels more like a generic magical aura that happens to be spinning along with the character."*

   **The check is per-row against that row's declared class, NOT a uniform preference for physical reads.** `aura` and `self_buff` are `magical-cause` **and that is CORRECT** — scoring an aura down for being decorative applies the criterion where it does not live. This distinction is the single most likely way for this gate to go wrong, so state it in the procedure explicitly.

   The failure mode you are hunting is precise and you have already confirmed it twice in pixels (L-25 Eye of Reckoning; L-28 War Cry): **an effect that expands, leaves a mark on the ground, and never touches the bodies it passes through.**

3. **RT-2 — the surface-class check** (spec § 6.1). The Tier-1 surface class (`PAYLOAD-CARRIED` / `TRAIL-BOUNDED` / `FIELD-CARRIED`) is **SPEC-ASSERTED**, not substrate-attested, and it carries a live revisit trigger:
   - **Fires when:** a `TRAIL-BOUNDED` archetype's element variants read as **indistinguishable** at the gameplay camera → that row moves toward `PAYLOAD-CARRIED`, receipt recorded.
   - **Converse outcome:** a variant that has **lost its physical read** → the class *held*, and the tint was over-expanded.
   - Both outcomes are results. Record which one you observed; neither is a failure of the gate.

4. **RT-6 — `vortex_pull` is NOT scored on VFX alone.** Not in this tranche, but bake it into the standing procedure so it cannot be forgotten when the row arrives: its readability is carried by engine-side enemy displacement (routed as X-2). Either the engine dependency has landed, or the row is scored **with the dependency named as the limiting factor.**

5. **C-3 stage albedo — judge recolour survivability against the ACTUAL stage albedo.** Measured: floor albedo 0.20 washes the frame; **0.085 reads correctly.** A parameterizability score taken against the wrong albedo is a score taken against a lie.

6. **C-5 coverage floor AND ceiling.** Measured span 0.03 % → 67 %. One occludes the fight, the other cannot be seen. Readability fails at both ends; the rubric needs both bars.

7. **The evidence-tier and confound vocabulary from § 3.0** — in particular `frame-external` (croppable) vs `effect-internal` (**not** croppable; requires subtracting a layer from inside the thing you are measuring). **Do not collapse them.** The spec is explicit that `aura`'s confound class is *not* the class `whirlwind` carries, and generalizing "confound named ⇒ confound discountable" across the two is an error the ledger specifically warns about.

8. **A stated HALT condition.** When is a row unscorable? Name it in advance, so a HALT is a procedure output rather than a judgment call under pressure.

---

## (B) Tranche-1 scoring

Score the three rows against the procedure. **They were chosen to span the axes the rubric has to discriminate on** — one row per Tier-1 surface class, and three different L-19 causality classes:

| Row | Surface class | L-19 | What this row specifically tests in your rubric |
|---|---|---|---|
| `melee_strike` | TRAIL-BOUNDED | `physical-cause` | Does the rubric catch tint over-expansion — "an energy wave chasing the weapon"? |
| `ground_targeted_circle` | PAYLOAD-CARRIED | `hybrid` | **Perimeter definition under telegraph literacy.** Can a player read *"a thing is going to land THERE"* before it lands? Also: RT-8's `payload_vector` / `zone_valence` params, and whether the effect **blooms out its own interior at large scale** (the named Meteor-Indigo failure mode). |
| `aura` | FIELD-CARRIED | `magical-cause` **(correct)** | Does the rubric correctly **decline** to penalize decoration? And does the field communicate influence **without filling the radius with opaque effects**? |

Also verify, because 112 `self_buff` skills will be **active during other skills**: does `aura` remain something other archetypes' VFX stay readable *through*?

### ⚠ `aura` carries a SCOPE NOTE that must NOT move your score — gandalf ruling L-41, 2026-08-24

X-4 found the `aura` row's owner-attestation covered only 6 of its 73 bound skills. I routed it to gandalf as *membership-or-grain*. **He ruled GRAIN — and the grain answer is a PARAMETER, not a split:**

- **All 73 stay bound. No row changes archetype. T-K untouched at 1,134. No re-derivation, no re-mint.**
- `aura` gains a three-valued emitter-anchor parameter: **`caster_centred` 67 (as sealed) · `world_placed` 4 · `delegate_carried` 2.**
- He **explicitly refused** the membership move: Oak Sage / Voodoo / Holy Banner are *not* `totem`, because that row binds a three-phase delegate **slam** these passive bodies do not have. Re-membering them would render an attacking delegate where the game shows a banner — the same error as field-for-a-crowd, in the other direction.
- The **Demonologist 2** are the **summoner GAP — HELD**, do-not-author-as-`aura`, treated exactly as `knockback`. Step 2 mints nothing for them.

**For your gate, in his words: you score the minted effect against the `caster_centred` binding — the 67. The grain note is scope, not score.** Your L-19 decline-to-penalize instruction stands **verbatim and unchanged.**

**Do not fold membership into the score.** `aura` is in this tranche precisely because it is the row that tests whether your rubric correctly declines to penalize correct decoration. A correct effect passing your gate **is your gate working** — membership is a different instrument's job, and mixing them would corrupt the one row that calibrates the rubric.

---

## Cross-seam contract change? (Principle 6 gate)

**NO.** **Round-trip: not applicable — no cross-seam contract change in this dispatch.** Judging artifacts and a procedure doc only.

## Acceptance criteria

- [ ] Standing procedure authored, covering all eight items in § (A), and reusable for the remaining 21 rows without rewriting
- [ ] Three rows scored on the § 3.2 three-axis rubric with receipts
- [ ] L-19 causality check applied **per row against its declared class** — with the `aura` case demonstrating the rubric declining to penalize correct decoration
- [ ] RT-2 verdict recorded **per `TRAIL-BOUNDED` row** (held / fired / converse-observed). On the others, state **`n/a — class not TRAIL-BOUNDED`** explicitly rather than omitting the line. *(RT-2's trigger is defined only for `TRAIL-BOUNDED`; two of the three tranche rows are `PAYLOAD-CARRIED` and `FIELD-CARRIED`, where it is undefined. **Do not invent a verdict to fill the cell** — an invented verdict and an omitted one fail the same way, silently.)*
- [ ] Judge-From captures verified rendered at stage albedo **0.085**; if they were not, that is a re-render request to drax, not a scored result
- [ ] Per-row verdict: `PASS` / `PASS-WITH-FINDINGS` / `REWORK` / `HALT-unscorable`
- [ ] Round-trip: not applicable
- [ ] Receipts committed; **do not push**

## Quality criterion

**Game-quality goal this dispatch serves:** that the twenty-four canonical effects form a *legible visual language* rather than twenty-four separately-plausible effects. The gate is the only instrument between a minted effect and 1,134 bound skills inheriting it. **A gate that passes everything has failed** — it is a rubber stamp, and the run has already banked one standing exhibit of exactly this (the oversold `whirlwind#1` dossier row walked out of the vendor lane and was caught **only** at your P3 gate).

**Refutation conditions** (surface to knight-rider before executing if any apply):
- The rubric cannot separate two of the three tranche rows — it is under-specified; say so rather than manufacturing a distinction
- A row is unscorable on the available captures — HALT with reasons; **do not guess a label** (your P3 refusal is the precedent, and it was the right call)
- The gate criterion can pass a minted effect that visibly fails the L-19 owner criterion
- Scoring requires reopening a § 1 design-law ruling — HALT to Matt, not a design conversation

## Out of scope

- **Judging `whirlwind`.** It ships under the **WW-AB clean-room protocol** and Matt compares the two builds himself. Your gate scores the clean-room build against T-A § 3.1.12 like any other row — but the **A/B preference is Matt's, not yours**, and you must not be handed the adopted-lineage build as a comparison target for scoring.
- Re-opening any P3 selection. T-A is sealed law.
- Re-hunting reference links. `3BnHvNZ_4YM` is closed as `TBD-UNRESOLVABLE` (L-30/L-32). **403 is never absence** — confirmed bot-blocked: `pathofexile.com`, `gamestar.de`, `bluetracker.gg`.
- The U-8 cross-vendor judge pilot. Gated separately (R-4); not this dispatch.
- Any mint work. You judge; drax builds.

## References

- Sealed spec + charter L-1…L-40 (`gandalf/notes/`)
- Upstream: `dispatches/2026-08-24-drax-s2a-mint-tranche-1.md`
- Carve-out request: `gandalf/requests/2026-08-24-knight-rider-carveout2-step2-build-wave.md`

---

## Gate record

- jack-ryan Gate-1 DESIGN-MODE: **PASS-WITH-FINDINGS → **amendments applied 2026-08-24**** — Gate-1 batch review, 2026-08-24.
  RT-2 acceptance line corrected: RT-2's trigger is defined only for `TRAIL-BOUNDED`, so the other classes get an explicit `n/a` rather than an invented verdict.
  Amendments approved by jack-ryan directly under **ADR-002** (dispatch documents are documentation-only). **Nothing in this batch escalated to Matt.**
