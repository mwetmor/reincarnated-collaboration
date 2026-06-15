# A-vs-B Ruling — "A holds": Synty modular geometry + the lift reaches register-2

**Type:** design ruling (gandalf seam — the A-vs-B resolver the Godot pivot was gated on).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B) — *"Author the A-holds ruling and style-register re-carve."*
**Evidence input (load-bearing, not the ruling):** `agentic_orchestration/galadriel/reports/2026-06-14-godot-lift-register2-scorecard.md` — composite **4.50/5**, both mandatory gates at **5**, 2×-margin CV support.
**Parent briefs:** `agentic_orchestration/gandalf/notes/2026-06-14-drax-godot-vertical-slice-spike-brief.md` (the A-vs-B resolver) + `…-drax-register-lift-capture-increment.md` (the lift+capture increment).
**Consequence:** this ruling fires the `canonical/story/style-register.md` A-vs-B re-carve (recognition → validate → **commit**; validate now DONE).

---

## 0. The ruling, in one line

**A holds.** Register-1 Synty modular geometry — flat per-face color, cheapest-possible mesh — lifted in the lighting + VFX + material-shading layer and framed through the fixed 2.5D camera, reaches galadriel's measured **register-2** (premium-stylized ARPG) bar on our own hardware and our own content. **Path B (selective per-part hand-painting) is NOT needed for the curated-world roster.** It is demoted to a per-asset reserve lever, not deleted.

## 1. The question this rules (verbatim from the spike brief)

> **A** = register-1 modular geometry, lifted in lighting + VFX + material-shading, reaches register-2 → the cheap modular roster holds.
> **B** = it does not → selective per-part hand-painting added on top.

The pivot to Godot 3D + fixed 2.5D camera was Matt-locked 2026-06-14. It left exactly ONE question spike-gated: **does the cheap geometry, treated in the layer we control, read premium?** Everything else about the register was decided. This is the resolver.

## 2. The evidence (galadriel's measured scorecard — I do not re-derive it; I interpret it)

| Axis | Score | CV support | Margin |
|---|---|---|---|
| Lighting drama | **5** | LDR 231.6 (thr 115); SHF 60.7% (thr 30%) | **2× over both** |
| VFX presence | **5** | HLF peak 14.4% (thr 1.5%) | **9.6× over** |
| Material-shading | **4** | LMV 32–38; per-tile variance distributed across lit interiors, not face-boundaries | clears the flat-floor |
| Geometry register | **4** | silhouette legible; clean modular part-swap; low-poly *correct* for register-2 | exceeds the ≥3 target |
| **Composite** | **4.50 / 5** | | ≥ 3.6 PASS |

**Both mandatory gates (lighting ≥ 4 AND VFX ≥ 4) pass at 5.** The composite clears the bar by nearly a full point. This is not a marginal pass I am rounding up — it is a 2×-CV-margin pass on the two axes the rubric made non-negotiable.

**The T-pose caveat is resolved, not waved.** galadriel ruled the static compose-pose does NOT depress the VFX score: the FX_Fire_Large_01 bloom is **body-anchored** — it erupts vertically from the figure's torso, the hot core inside the silhouette — so it reads as *the character's own power*, not as ambient fire a mannequin stands beside. CV instruments are pose-agnostic (the bloom's pixel-presence/brightness/contrast are identical T-pose vs combat-pose). What the T-pose costs is *cast directionality* (narrative legibility — "channeling" vs "casting"), NOT VFX presence. **Re-capture is NOT required for the ruling.**

## 3. Why this is the expected result, not a surprise (genre grounding)

galadriel's premium-perception benchmark predicted this before the spike ran: premium ARPG feel ≈ **~40% lighting + ~30% VFX + ~20% material-shading + ~10% geometry.** Of eleven reference frames she scored, the one with the *cheapest geometry* — **Torchlight Infinite** — read the **most** premium. Geometry is the smallest lever; chasing mesh-detail density is the wrong axis.

This is the oldest truth in the genre, now re-evidenced on our content:

- **Diablo II** shipped premium-feeling on **sprites** — the "feel" lived in hit-flash, screen-shake, gib physics, and lighting, not polygon count.
- **Hades** reads AAA on **stylized 2D** — Supergiant bought the premium with VFX juice and impact framing, not fidelity.
- **Torchlight Infinite / Last Epoch** — the explicit register-2 anchors — run *this exact* silhouette-readable low-poly geometry and carry premium through lighting + skill-VFX.

The design hypothesis the pivot bet on — *lock the cheap-geometry register, spend the saved fidelity budget on S-tier `GPUParticles3D` juice, get ~90% of fuller-fidelity's premium at the cheap register's cost and mobility* — is no longer a hypothesis. The slice clears the bar with one hero-skill bloom and a dark-mood light rig on a $0-extra-cost modular knight.

## 4. What "A holds" claims — and what it does NOT (the honest scope)

**A-holds CLAIMS:**
- Cheap Synty modular geometry + the controllable lift layer (lighting + VFX + material-shading) = register-2 on our hardware (8GB M2 build / capture) and our content (the composed knight in a POLYGON dungeon graybox).
- The roster strategy can rest on **register-1 modular geometry uniformly lifted** — we do not need per-part hand-painting as the *default* path to look premium.
- The fidelity budget belongs in **lighting + VFX**, confirmed by measurement, not asserted.

**A-holds does NOT claim (these are separate milestones, each on its own gate):**
1. **That every form is solved.** This validated a **humanoid** form (the composed knight on the shared rig). Non-humanoid body-plans (doc-37 Tier-2 skeletal + Tier-3 non-skeletal — slime, swarm, dragonling, cloud-being) are NOT proven to lift coherently beside humanoids in-frame. That is the residual long-pole, flagged in the spike brief, untouched by this capture.
2. **That the generative-self (Meshy) forms clear the same bar.** A Meshy-generated whole-form must clear *this same lift* AND sit coherently beside Synty geometry in one frame. Style-coherence-across-sources is its own risk (the A2/A3 architecture question). A-holds validates the *curated-Synty* roster; the *generative-self* roster is a distinct coherence proof still owed.
3. **That this is a live combat loop.** This was a deterministic motion capture (100 frames, Movie Maker) of a composed form with a windowed hero-skill bloom — sufficient for the *register* question (galadriel: the bloom is pose-agnostic). A live, input-driven, multi-form combat scene is a separate **integration** milestone, not a register milestone.

These exclusions do not weaken the ruling. They scope it. The A-vs-B question was always *"does the cheap geometry read premium under the lift?"* — and the answer is **yes, measured.**

## 5. Path B is demoted, not deleted (substrate-honest disposition)

Path B (selective per-part hand-painting, bounded by part-count not form-count) is **not** the roster strategy. But I do not delete the option — I demote it to a **per-asset reserve lever**: if a specific named hero asset (a signature boss, a marquee ascended form, a Court centerpiece) ever wants fidelity the uniform lift can't buy, Path B is available *for that asset*, scoped to its parts. This is the score-don't-filter discipline applied to technique: keep the lever in the catalogue, don't make it the default consumption path. The roster ships on A; B is there if a hero asset earns it.

## 6. Cheap optional polish (non-gating)

galadriel flagged one cheap, high-presentation-value follow-up: a **combat cast-pose re-capture** would convert "character is channeling fire" → "character is *casting* fire," adding agency/directionality to the presentation. It would NOT change any of the four axis scores (the gates already pass). I file it as **optional polish for the A-holds presentation deck**, not a blocker, not a prerequisite for the style-register commit. Worth doing when a combat-pose animation is wired anyway; not worth a special pass now.

## 7. Routing / what this fires

- **gandalf:** this ruling → the `canonical/story/style-register.md` A-vs-B re-carve (locking sub-candidate A; retiring the spike-gated-OPEN status). Authored same session.
- **drax:** the lift scene (`scenes/lift_render.tscn`) + the 100-frame capture are the validated reference build; the lighting/VFX recipe is now the register-2 baseline recipe for the roster, not a one-off.
- **galadriel:** scorecard is the durable evidence; the rubric instruments (`register-metrics.mjs` / `lifecycle-score.mjs`) become the standing register-2 acceptance harness for future captures.
- **KR:** aware the A-vs-B fork is closed → A; the residual long-poles (non-humanoid Tier-2/3 coherence; generative-self/Meshy coherence; live combat loop) are the named next register-adjacent milestones, each separately gated.

---

**Signed:** gandalf, 2026-06-15
**For:** the A-vs-B ruling — galadriel's measured 4.50/5 (both mandatory gates at 5, 2× CV margin) on the cheap-Synty-modular-geometry-plus-lift slice resolves the Godot pivot's one open sub-fork in favor of **A**: register-1 modular geometry, uniformly lifted in lighting + VFX + material-shading and framed through the fixed 2.5D camera, reaches register-2; Path B (per-part hand-painting) is demoted to a per-asset reserve lever, not the roster strategy; the ruling is scoped to the humanoid form under a deterministic capture and explicitly does NOT yet claim non-humanoid coherence, generative-self/Meshy coherence, or a live combat loop — each a separately-gated downstream milestone.
