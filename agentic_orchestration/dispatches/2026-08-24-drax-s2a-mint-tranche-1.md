# Dispatch — 2026-08-24 — drax — Step-2 VFX mint, TRANCHE 1 (the loop-proving tranche)

**Status:** PENDING
**From:** knight-rider (Step-2 build wave, carve-out #2)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Approved by:** Matt, 2026-08-24 (launch word covering the whole carve-out #2 agenda)
**Pattern:** B (dedicated session)
**Gates:** jack-ryan Gate-1 DESIGN-MODE — see § Gate record below
**Position in wave:** you mint → **galadriel minted-gate** (`2026-08-24-galadriel-s2-minted-gate.md`) → **gandalf DRIFT-CRITIC**. You are the head. Nothing downstream of you starts until this tranche lands.

---

## Context

The VFX archetype-binding run **SEALED 2026-08-24**. It produced two binding tables: **T-A** (24 archetype → canonical VFX bindings + `knockback` HELD) and **T-K** (**1,134** kit-skills bound to those 24 — 1,135 is the *assigned* count from P1; 1,134 is what T-K IS, post-`knockback`-hold. Corrected by gandalf at L-41). Step 1 was gandalf's; **Step 2 is the build, and this dispatch opens it.**

The design thesis in one sentence: **twenty-four effects stand behind one thousand one hundred and thirty-five skills.** A player who learns what a descending payload inside a crisp perimeter *means* has learned it for 115 skills at once, and the element tint tells him which of them is about to burn him. That is telegraph literacy, and it is the return on the archetype-first factory.

**This tranche is deliberately three rows, not one and not twenty-four.** One row would prove a pipeline but not a *rubric*; twenty-four would commit the whole wave before anyone has seen a single minted effect scored. Three rows chosen to **span the axes the gate has to discriminate on**:

| Row | Spec § | Tier-1 surface class | L-19 causality class | Why it is in the tranche |
|---|---|---|---|---|
| `melee_strike` (115 skills / 98 kits) | 3.1.2 | **TRAIL-BOUNDED** | `physical-cause` | Tied-largest archetype. The row where L-19 matters most — its failure mode is precisely "an energy wave chasing the weapon." |
| `ground_targeted_circle` (115 / 102) | 3.1.1 | **PAYLOAD-CARRIED** | `hybrid` | Largest archetype in the vote. Carries **RT-8**'s two new params. |
| `aura` (73 / 61) | 3.1.8 | **FIELD-CARRIED** | `magical-cause` *(and that is CORRECT)* | Completes surface-class coverage, and is the calibration case for a gate that must NOT score an aura down for being decorative. |

If the loop works across these three, it works. If the rubric cannot separate them, we learn that on three rows instead of twenty-four.

---

## Required reading before starting

1. **`agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md`** — **STATUS: SEALED. The filename says DRAFT; the STATUS line governs. This is law.** Read in this order:
   - **§ 1** — design law digest (the six charter rulings, restated for a builder)
   - **§ 1.1** — the owner criterion of record (L-19), the lens every row is scored through
   - **§ 1.2** — the locked style register, what "S" is scored against
   - **§ 2** — the P0-b constraints inherited from *your own probe*; every one binds every row
   - **§ 3.0** — column semantics; read before reading any row
   - **§ 3.1.1, § 3.1.2, § 3.1.8** — your three rows
   - **§ 6.1** — the pre-registered revisit triggers, especially **RT-2, RT-3, RT-8**
   - **§ 7** — what the spec does NOT decide (so you do not read silence as permission)
2. `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` — ledger **L-19** (the owner criterion), **L-29** (the folds), **L-39** (key-grain audit).

   ⚠ **Do NOT read L-36 or L-37, sealed spec § 5, or the carve-out #2 request.** They are **quarantined under the WW-AB clean-room protocol** — they describe the adopted `whirlwind` lineage in build detail, and **you are the agent who will later mint `whirlwind` clean-room.** Reading them here contaminates that experiment even though this dispatch has nothing to do with it. **You need nothing from them:** the tier-2 rulings are **A-1 YES · A-2 ADOPT + WW-AB · A-3 same pipeline as A-1 · Class B REJECTED**, and not one of the four bears on tranche 1. That is the complete extraction.
3. `galadriel/notes/2026-08-24-vfx-p3-selection-gate.md` **+ its delta** (the delta supersedes row-by-row) — the Judge-To corpus you are building toward.
4. `galadriel/captures/2026-08-23-vfx-p2-gd-framesets/framesets.json` **v2**.
5. `canonical/reap-die-rise-story/style-register.md` — register A, bounded stylized-low-poly-3D (Synty) through a fixed 2.5D ARPG camera.
6. Your own `agentic_orchestration/drax/notes/2026-08-23-metal-vfx-smoke-probe.md` § 7 — you wrote the constraints; re-read them as *inputs* rather than as findings.

---

## The seven P0-b constraints — they are yours, and they bind every row

From your own probe (spec § 2.3). Restated because a constraint you discovered is still a constraint you can forget:

- **C-1 — disable shadow casting on additive/emissive VFX meshes at mount time.** Both vendor packs ship shadow-casting geometry; the effect otherwise paints a hard black blob on the floor beside itself. **Applies to every row in this tranche.**
- **C-3 — additive stacking blows to white over a light floor.** Floor albedo 0.20 washed the frame; **0.085 reads correctly.** Judge Tier-1 recolour survivability against the *actual stage albedo* or "parameterizability" is assessed on a lie.
- **C-4 — lifecycle class is a real authoring axis** (measured spread > 5×). A telegraph that lasts 0.53 s and one that never stops are not interchangeable. Each row below states its lifecycle class; build to it.
- **C-5 — readability has a FLOOR and a CEILING** (measured coverage spans 0.03 % → 67 %). One occludes the fight; the other cannot be seen.
- C-2 (beam −Z orientation) and C-7 (beam-pack `uid://` fragility) do **not** bind this tranche — no beam-class row here. C-6 (zero attractor content) binds `vortex_pull`, not these rows.

### ⚑ C-8 — THE STAGE SHIPS THE FAILURE MODE ON BY DEFAULT (added 2026-08-24, post-WW-AB)

**You found this yourself, hours ago, in the whirlwind clean-room mint** (`drax/v0.1-s2-whirlwind-cleanroom-1`), and you flagged it as bigger than that dispatch. It is:

> **`KingRig`'s stock `HolyAura` read as literally "a generic magical aura spinning with the character"** in your first capture.

That sentence is a near-verbatim statement of the **L-19 failure mode** — an effect that *decorates* the actor rather than being *caused* by the action. **Every T-A row staged on `KingRig` inherits it.** The contamination is silent and it flows the wrong way through the gate: galadriel scores the *frame*, and a frame containing your correct mint plus the rig's stock aura is a frame where the inherited failure is indistinguishable from an authored one. **A row can fail her L-19 check for a reason that is not in your effect at all.**

**Required for every row in this tranche:**

- [ ] **Disable / strip the rig's stock ambient VFX before capture, and state in the mint note that you did.** Name what you disabled, per row.
- [ ] **If a row's staged frame contains ANY emitter you did not author, name it.** An unnamed inherited emitter reaching galadriel is a false verdict in either direction — it can sink a good mint or flatter a bad one.
- [ ] **Say whether stripping it is a capture-time step or a rig fix.** If the rig itself should not ship a spinning aura by default, that is a finding about the staging substrate and it outlives this tranche.

**This is not a scope increase — it is the removal of a confound that was already in every frame.** Judging Tier-1 recolour or L-19 causality against a frame carrying an unattributed emitter is the same class of error as judging albedo against 0.20: **a real measurement taken against the wrong stage.**

---

## Math-before-code (Discipline #1)

Before minting, write a short **mint note** per row into `agentic_orchestration/drax/notes/2026-08-24-s2a-mint-note.md` stating, for each of the three rows:

1. **The layer decomposition you are building to** — T-A names the independently swappable layers per row. Tier-1 parameterization is only possible *because* those layers are separable. State which Godot node/material carries which layer.
2. **What takes the tint and what must NOT** — copied from the row's Tier-1 surface-class clause, then translated into the concrete property you will vary.
3. **The lifecycle class and how you realize it** — burst / decaying / sustained / composite.
4. **Your stage-albedo test value** and why (C-3).
5. **Which element variants you will mint** for the Tier-1 demonstration, and why that set is sufficient to demonstrate parameterizability without being a content lap.

**This note is what DRIFT-CRITIC audits against.** It is cheap now and expensive to reconstruct later.

---

## Scope

### Row 1 — `melee_strike` (§ 3.1.2)

- [ ] **Cut the canonical MP4.** The canonical is Last Epoch **Rive**, a directly downloadable first-party MP4 (`forum.lastepoch.com/uploads/.../0b88fc443d13e2e232e51cbfe567994741b3f8e0.mp4`, HTTP 200, 5.36 MB). The spec names this **the cheapest evidence-tier upgrade available on any T1 row** — it is an extraction master waiting to be cut. Cut it, and the row moves from `DOSSIER-TEXT` to `FRAMES-INSPECTED-BY-EXTRACTION`. Do this **first**; it improves the target you are building toward.
- [ ] Mint the base binding. **Three explicitly separated layers: (a) character motion, (b) weapon trail, (c) hit response on the target.** Body-anchored — it strikes an **enemy body**, not the ground plane. **No ground propagation.**
- [ ] **Tier-1: tint the weapon trail and the hit-response spark only.** Do NOT expand the tint into a body-surrounding field. 70 % of this archetype's referent members carry no element at all; a field-sized tint on a weapon strike is the Eye-of-Reckoning conversion in miniature.
- [ ] Note (do not build) that **Rive escalates on the third stroke** — a cadence-coupled flourish hook that costs no bespoke asset. Record whether your base binding's structure leaves room for it.

### Row 2 — `ground_targeted_circle` (§ 3.1.1) — carries RT-8

- [ ] Mint the base binding: **world-ground anchored**, two independently swappable layers — **(a) a crisp thin perimeter annulus with a TRANSLUCENT interior** (cracked-ground decal, internal detail visible *through* it), **(b) a vertical payload descending on the centre axis.** Caster legible at frame-edge, entirely outside the effect. Target coverage ≈ 20 % (mid-band against C-5).
- [ ] **The deciding property is PERIMETER DEFINITION.** For 115 skills the player must read *"a thing is going to land THERE"* **before it lands.** A competitor reference was rejected for establishing the circular footprint *temporally* rather than through a hard perimeter — that deletes the archetype's telegraph. Do not repeat it.
- [ ] **RT-8 — mint with two params** (measured residuals from the L-39 key-grain audit, pre-registered, not post-hoc):
  - **`payload_vector`** — `descend` / `erupt`. Same perimeter grammar, inverted payload direction. The substrate holds 3 erupt-from-ground skills (Fissure, Fire Trap) inside this key.
  - **`zone_valence`** — `hostile` / `friendly`. A **palette-convention rule**, Tier-1-adjacent, **zero new assets**. ~7 friendly-platform skills (Inquisitor-Seal class) live in this key. **A player must never read a friendly platform as enemy fire.**
  - **If the `erupt` variant cannot share the `descend` emitter cleanly, that is a FINDING for the next lap — surface it. It is not a silent fork.**
- [ ] Lifecycle is **composite: `burst` (payload) → `decaying` (residue)** — a previous cast's residue coexists with a fresh cast.
- [ ] **Avoid the named failure mode:** the Meteor Indigo reference **blooms out its own interior at large scale.** Check your effect at large scale before you call it done.

### Row 3 — `aura` (§ 3.1.8)

- [ ] Mint the base binding: caster-centred field, layers — **(a) a radius-defining ground ring/falloff, (b) sparse influence particles.** The selected property is that it *communicates influence without filling the radius with opaque effects* — that is the coverage-ceiling solve an always-on field needs.
- [ ] **Tier-1: tint the ring and the influence particles. Radius and opacity are NOT Tier-1 knobs on this archetype** — they are the archetype's readability contract, and a recolour must not move them.
- [ ] **`magical-cause` is CORRECT here.** Decoration is what an aura *is*. Do not "fix" it into a physical read.
- [ ] ⚠ **NEW — gandalf ruling L-41, 2026-08-24, landed after this dispatch was authored. It NARROWS what you mint, and that is the only change: you mint the `caster_centred` case and nothing else.**
  X-4 found the row's attestation covered 6 of its 73 skills. gandalf ruled **GRAIN, not membership** — all 73 stay bound, T-K is untouched, **no re-mint** — and the grain resolves as a three-valued emitter-anchor **parameter**, not a split:
  - **`caster_centred` — 67 skills. This is what you mint. It is the row exactly as sealed; nothing about the layer recipe above changes.**
  - `world_placed` — 4 skills (Oak Sage / Voodoo / Holy Banner class). **Do not mint.** gandalf explicitly refused re-membering them as `totem`: that row binds a three-phase delegate **slam** these passive bodies do not have, and minting one would render an attacking delegate where the game shows a banner.
  - `delegate_carried` — 2 skills (Demonologist). **HELD as the summoner GAP — do-not-author-as-`aura`, treated exactly as `knockback`. Step 2 mints nothing for them.**

  **If you find yourself authoring a variant for the 4 or the 2, stop — that is out of scope by ruling, not by omission.**

### Standing

- [ ] Mint note per § Math-before-code, committed before the first mint
- [ ] C-1 shadow-casting disabled on every additive/emissive mesh you mount
- [ ] Capture set for galadriel's gate (Judge-From side), rendered at stage albedo 0.085
- [ ] `AGENT_STATE.md` updated at session end
- [ ] Tag: `drax/v<X.Y>-s2a-mint-tranche-1`

## Cross-seam contract change? (Principle 6 gate)

Does this dispatch add, modify, rename or remove any field on a telemetry schema table, a `fight_log` key, a loadout dict key, an export packet structure, or any inter-seam fixture dict?

**NO.** **Round-trip: not applicable — no cross-seam contract change in this dispatch.** This is Godot-side presentation authoring. `payload_vector` and `zone_valence` are VFX-authoring parameters inside the presentation seam; if a later lap needs them driven from engine emission, that is a contract change *then* and gets its own MIGRATION.md.

---

## Acceptance criteria

- [ ] Three base bindings minted, each demonstrably built to its row's stated layer decomposition
- [ ] Each row's Tier-1 element parameterization demonstrated on the layers T-A permits, and **NOT** on the layers T-A forbids — the "must NOT" clauses are acceptance criteria, not advice
- [ ] `melee_strike` canonical MP4 cut; evidence tier upgraded; frames filed for galadriel
- [ ] RT-8's two params exist on `ground_targeted_circle` and are demonstrated on at least one variant each
- [ ] Mint note committed **before** minting, covering all five required items per row
- [ ] Capture set rendered against stage albedo **0.085** and handed to galadriel's gate
- [ ] Round-trip: not applicable — no cross-seam contract change
- [ ] Tag `drax/v<X.Y>-s2a-mint-tranche-1`

---

## Quality criterion

**Game-quality goal this dispatch serves:** *telegraph literacy.* A player must be able to read, from the effect alone and before the damage lands, **what is about to happen and what kind of damage it is.** These three rows are the first empirical test of whether the archetype-first factory delivers that — and whether one canonical effect per archetype reads as *deliberate visual language* rather than as *reskins*.

**Refutation conditions** (surface to knight-rider before executing if any apply):
- The mint cannot honor a row's "must NOT" clause without the effect becoming unreadable — that is a finding about the surface class (RT-2), not a licence to widen the tint
- Acceptance criteria can pass without the effect actually reading as its archetype at the gameplay camera
- Building to T-A requires reopening a § 1 design-law ruling — **that is a HALT to Matt, not a design conversation**
- Two of the three rows converge in authoring (same emitter, same anchor, same coverage envelope) — a fold finding, record it
- A scaffold value ships without a Discipline #40 declaration

---

## Out of scope (explicit non-goals)

- **The other 21 T-A rows.** Later tranches; sequenced after this loop proves out.
- **`whirlwind`** — separate dispatch, **clean-room protocol**, RT-4-gated. Do not touch it here.
- **`beam_channel` / `line` / `placed_lane`** — RT-5-gated (Binbun `beam_vfx` `uid://` pre-flight in flight).
- **`vortex_pull`** — AUTHOR-not-SELECT, and blocked on an engine-side dependency (X-2). Not this tranche.
- **Tier-2 flourishes.** Tier-2 law is sealed (A-1 YES, A-2 ADOPT+WW-AB, A-3 Synty-first/Meshy, **Class B REJECTED**). None of it is in this tranche.
- **Bespoke-per-kit anything.** Matt verbatim: *"We should only adopt one move per skill-type, not one more per kit."*
- **Asset selection debates.** T-A gives semantics, readability targets, emitter geometry, constraints. **Asset selection is yours** — make it and record it; do not escalate it.
- **Re-grading elements.** `vfx_mapping_tier` is rocket's seam (X-3 routed separately).
- Modifying anything under `Assets/` (read-only).

---

## Open questions for you to resolve and document

- Which pack assets get mounted per layer, and why (§ 7.1 — explicitly yours)
- The element-variant set per row sufficient to demonstrate Tier-1 without becoming a content lap
- Whether `melee_strike`'s base structure leaves room for the third-stroke escalation hook
- Whether `ground_targeted_circle`'s `erupt` variant shares the `descend` emitter cleanly

## References

- Sealed spec: `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` (STATUS governs)
- Charter + ledger L-1…L-40: `gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`
- Carve-out request: `gandalf/requests/2026-08-24-knight-rider-carveout2-step2-build-wave.md`
- Downstream gate: `dispatches/2026-08-24-galadriel-s2-minted-gate.md`

---

## Gate record

- jack-ryan Gate-1 DESIGN-MODE: **PASS-WITH-FINDINGS → **amendments applied 2026-08-24**** — Gate-1 batch review, 2026-08-24.
  Quarantine propagated into Required reading (L-36/L-37, spec § 5, carve-out request) with the four tier-2 rulings extracted inline; tag convention corrected to `v<X.Y>` form.
  Amendments approved by jack-ryan directly under **ADR-002** (dispatch documents are documentation-only). **Nothing in this batch escalated to Matt.**
