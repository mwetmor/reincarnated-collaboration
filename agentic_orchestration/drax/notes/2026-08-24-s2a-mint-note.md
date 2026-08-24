# Mint note — S2A tranche 1: `melee_strike` · `ground_targeted_circle` · `aura`

**Author:** drax (presentation seam, `reincarnated-godot/`)
**Date:** 2026-08-24
**Dispatch:** `agentic_orchestration/dispatches/2026-08-24-drax-s2a-mint-tranche-1.md`
**Law of record:** `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` (STATUS: SEALED) §§ 1, 1.1, 1.2, 2, 3.0, 3.1.1, 3.1.2, 3.1.8, 6.1, 7
**Downstream:** `dispatches/2026-08-24-galadriel-s2-minted-gate.md`

> **Written BEFORE minting**, per the dispatch's Math-before-code clause (Discipline #1). § 9 (RESULTS)
> is appended after the build and is the only section written after the fact; every number in §§ 1–8
> was committed before a single effect node existed. The commit that carries §§ 0–8 precedes the
> commit that carries the effect scripts, and that ordering is the receipt.

---

## 0 · Pre-execution refutation surface — surfaced, not worked around

The dispatch names five refutation conditions and instructs me to surface any that apply **before**
executing. I evaluated all five against the sealed spec and against the one piece of evidence I
gathered before authoring (the Rive MP4 cut, which the dispatch ordered done *first*). Result:

| # | Refutation condition | Applies? | Disposition |
|---:|---|---|---|
| 1 | "must NOT" clause unhonorable without unreadability (RT-2) | **NO, pre-execution.** Measurable only after the mint. | RT-2 verdict deferred to § 9.3 and to galadriel's gate. Not pre-judged. |
| 2 | Acceptance criteria pass without the effect reading as its archetype | **NOT YET KNOWN.** | Mitigated structurally: every acceptance claim in § 9 is machine-graded against a stated bar, and the archetype read is galadriel's call, not mine. I do not score my own mint. |
| 3 | Building to T-A requires reopening a § 1 design-law ruling | **NO.** | Nothing in these three rows requires a § 1 ruling to move. No HALT to Matt. |
| 4 | Two of the three rows converge in authoring | **NO, but a related convergence exists and is recorded below (§ 0.2).** | Measured in § 9, not asserted. |
| 5 | A scaffold value ships without a Discipline #40 declaration | **WOULD APPLY if I were silent.** | Pre-empted: § 8 is the complete Discipline #40 register for this tranche. Every authored number is listed there with its class. |

**Net: no HALT-class condition applies. One WARN-class finding (§ 0.1) and one INFO-class observation
(§ 0.2) are surfaced here and the tranche proceeds.**

### 0.1 ⚑ WARN — the sealed spec's `melee_strike` confound register is WRONG, and the extraction the dispatch ordered is what proved it

Spec § 3.1.2, verbatim: **"Confound register: none named on the canonical."**

The dispatch told me to cut the canonical MP4 first because it is "an extraction master waiting to be
cut" and "the cheapest evidence-tier upgrade available on any T1 row." I cut it. The upgrade's **first
product is a correction to the row it upgraded**:

- **Media verified:** `HTTP 200 · 5,363,190 bytes · h264 · 1920×1080 · 60/1 fps · 460 frames ·
  7.666667 s`. First-party Last Epoch forum CDN, exactly as the spec claims. **The link is sound and
  the tier upgrade is real** — the row moves `DOSSIER-TEXT` → `FRAMES-INSPECTED-BY-EXTRACTION`.
- **But the clip is not skill-isolated.** It is a holiday-event town scene. Two confounds are present
  and neither is named in the row:
  1. **A large persistent green swirling column effect co-located with the caster** through roughly
     the back half of the clip (visible from ~t=4.6 s onward; sampled at 30 fps across a 78-frame
     window). It occupies the same screen area as the strike and moves with the caster.
  2. **A gold/white radial burst** at the caster that fires on some strokes. I cannot determine from
     pixels alone whether this is Rive's own hit response (in which case it is layer (c) and is
     *signal*) or a second simultaneous skill (in which case it is confound). **I am not guessing.**
- **Confound class, per § 3.0's two-valued vocabulary: `effect-internal`, NOT `frame-external`.**
  This distinction is the one § 3.0 flags as load-bearing and the one galadriel's dispatch § 7 tells
  her not to collapse. The green column is not a facecam or a HUD element that a crop removes — it is
  entangled with the caster at the same screen position as the effect being referenced. **It is not
  croppable.**

**Why this is WARN and not BLOCK, and why the tranche proceeds:** the red weapon-trail crescent —
which is the layer this row is actually built to — **is legible and separable by eye across ~50
frames**, in windows both with and without the green column present. The earlier part of the clip
(t ≈ 0.2–4.4 s, sampled at 15 fps, 66 frames) carries clean strokes. So the row's *semantics +
readability target* survives intact; what does not survive is the claim that the canonical carries no
confound.

**Routed, not patched.** `melee_strike`'s row lives in a **SEALED** spec and I do not rewrite sealed
spec text (the same discipline that produced the C-7 mechanism correction as a *proposed* refinement
rather than an edit — spec § 2.3 records that as "the discipline working"). This is a finding for
gandalf via knight-rider, with two consequences for people downstream of me:

1. **galadriel's Judge-To side for this row inherits the confound.** Her gate compares my Judge-From
   capture against the source-game reference frame-set. If her To-side frames are drawn from the
   confounded window, an entangled second effect is inside her reference. She should know before she
   scores. *(This is the mirror image of C-8: C-8 puts an unattributed emitter in MY frame; this puts
   one in HERS. Same error class, opposite side of the comparison.)*
2. **The § 3.0 evidence-tier law banked at L-41 predicted this shape.** "Evidence tier attaches to the
   media, not to the page" — and the corollary this cut demonstrates is that **a tier upgrade can
   downgrade a row's confound register.** `DOSSIER-TEXT-ONLY` rows carry "no confound named" for the
   trivial reason that nobody has looked. **Other rows in this corpus rest their empty confound
   registers on the same silence.** Cutting frames is how you find out. I name this because it
   generalizes past my tranche.

**What I did NOT do:** I did not re-select a reference, did not re-hunt links, did not re-grade the
row, and did not treat the confound as licence to build to the runner-up instead. The canonical stays
canonical. I build to it, with its confound named.

### 0.2 INFO — the convergence that exists is `melee_strike` ↔ `whirlwind`, not a within-tranche pair

Refutation condition 4 asks whether two of the three tranche rows converge in authoring. **They do
not** — the three differ on anchor (body / world-ground / caster-centred), on lifecycle
(burst / composite / sustained) and on Tier-1 surface class (TRAIL-BOUNDED / PAYLOAD-CARRIED /
FIELD-CARRIED), which is exactly why these three were chosen. § 9.6 reports the measured convergence
check rather than resting on this prediction.

The convergence I *can* see is across tranches: **`melee_strike` Layer B and `whirlwind` Layer A share
a generator.** Both are a bone-derived `ImmediateMesh` ribbon rebuilt per frame from the blade's real
`(grip, tip)` world segment. That is deliberate and I am reusing it on purpose — it is the cheapest
enforcement of L-19 that exists, because *a tinted surface cannot drift away from its cause when it is
generated from its cause*.

**But they are not the same effect and I am recording why, so a future fold does not get argued from
the shared generator alone:**

| | `melee_strike` | `whirlwind` |
|---|---|---|
| lifecycle | `burst`, per stroke, ribbon **resets between strokes** | `sustained` channel, ribbon is continuous |
| arc | discrete strokes, each < 180° | continuous revolution, 900 °/s |
| hit response anchor | **on the enemy body at the contact point** | on the enemy silhouette edge, phase-locked to blade passes |
| ground layer | **none — "no ground propagation" is spec text and I gate on it** | a neutral, never-tinted scuff layer exists |
| caster motion | strike animation | rotation |

`whirlwind` is not "sustained melee_strike" — it spends its outer radius on *consequences*, and this
row spends it on *one contact*. **L-29 item 7 already ruled `orbit` ↔ `whirlwind` distinct on parent
transform; nothing in T-A puts `melee_strike` ↔ `whirlwind` in question and I am not opening it.**
Recorded as an authoring observation for gandalf's DRIFT-CRITIC, not as a fold proposal.

---

## ⚑ C-8 — the stage's inherited emitters, declared

**This section is what lets galadriel's verdict mean anything.** Her dispatch instructs her to **HALT
back to knight-rider** rather than score around a mint note that fails to declare non-authored
emitters. So this is not paperwork; it is the control on her measurement.

### C-8.1 What I disable, per row

**All three rows stage on `KingRig` and all three strip the same two nodes**, because the strip is a
property of the rig, not of the effect:

| Node | What it is | Why it must go |
|---|---|---|
| `HolyAura` | Binbun `basic_area` magic-circle VFX — a golden caster-surrounding ground disc with upward glow columns and its own `Light`, auto-looping its pulse. Built unconditionally in `KingRig._build_aura()`, called from `_ready()`. | **It is a near-verbatim instance of the L-19 failure mode**: a generic magical field that decorates the actor and spins with him. I found it in the whirlwind clean-room capture, where it read as exactly that. |
| `SwordLootVFX` | An orange/gold loot orb on the weapon. | Additive emissive geometry inside the frame that I did not author and that sits on the very blade the `melee_strike` trail is generated from. On this row in particular it would be **directly inside the layer under test**. |

**On `aura` (row 3) the stakes are highest and the reason is not obvious, so it is stated
explicitly:** row 3 mints a caster-centred field. `HolyAura` **is also a caster-centred field**. Left
in, galadriel would be scoring my aura *plus a second, undeclared aura occupying the same radius*, and
no amount of care on her side could separate them from pixels. `HolyAura` must be off on row 3 or the
row is unscorable — and it would be unscorable **in a way that looks like a score**.

### C-8.2 The declaration is produced by an instrument, not by my memory

Naming two nodes from recall is exactly the enumeration-in-place-of-the-rule failure that the
whitelist ruling was issued over. So the declaration is **derived, not hand-listed**:

`scripts/s2a_census.gd` walks the live SubViewport at every capture mark and enumerates every visible
node that can put light into the frame — `GPUParticles3D`, `CPUParticles3D`, `OmniLight3D`,
`SpotLight3D`, `Decal`, and every `MeshInstance3D` whose material is additive, transparent or
emissive. Each is tagged **AUTHORED** (descends from my effect root) or **INHERITED** (does not). The
inherited list is written into the render log per mark and reproduced verbatim in § 9.2.

**If that list is non-empty beyond what § C-8.1 accounts for, the finding goes in § 9.2 as a finding —
it does not get quietly hidden.** An instrument I only trust when it agrees with me is not an
instrument.

### C-8.3 Capture-time step, or rig fix? — **BOTH, and the rig half is the finding that outlives this tranche**

**For this tranche: capture-time.** The effect is a legitimate feature of that rig for the throne-room
scenes it was built for, and `Assets/` is read-only.

**But the honest answer to the dispatch's question is that this is a rig defect, and here is the
argument:** `KingRig` began as the throne-room king and has become **the project's default humanoid
staging rig** — it is what whirlwind staged on, what all three of these rows stage on, and what the
remaining 21 T-A rows will stage on. A scene-specific piece of set dressing that was correct when the
class had one consumer is now **an unrequested caster-centred magical field switched on by default
underneath every VFX experiment the project will run.** The contamination is silent, it is inherited
rather than authored, and it flows the wrong way through the gate.

**The fix I am making, and its blast radius: zero.** `KingRig` gains an exported
`stock_vfx_enabled: bool = true`. Default `true` preserves the existing behaviour of every scene that
already instantiates the rig, byte-for-byte. VFX stages set it `false` **declaratively**, which
replaces the name-matched `_hide_named("HolyAura")` hack the whirlwind stage used — a hack that fails
*silently* the day someone renames the node. The flag default is registered under Discipline #40 in
§ 8.

**What I am NOT doing:** flipping the default. That is a behaviour change to other seams' scenes and
it is not mine to make unilaterally. **Recommendation to knight-rider: the default should eventually
be `false`, with throne-room scenes opting in.** A staging rig should not ship an effect; a scene
should mount one. Routed, not executed.

---

## 1 · ROW 1 — `melee_strike` (§ 3.1.2) · TRAIL-BOUNDED · `physical-cause` · `burst`

115 skills / 98 kits. Tied-largest archetype. **The row where L-19 matters most** — its named failure
mode is precisely "an energy wave chasing the weapon."

### 1.1 Layer decomposition → which Godot node carries which layer

T-A names three explicitly separated authoring layers. They map one-to-one:

| T-A layer | Godot node | Material / construction | Tinted? |
|---|---|---|---|
| **(a) character motion** | `S2AStrikePose` — pose offsets driven onto the rig's `Skeleton3D` | no material; **carries no VFX at all** | **NO — structurally cannot be** |
| **(b) weapon trail** | `TrailRibbon` — `MeshInstance3D` + `ImmediateMesh`, rebuilt every frame from a rolling history of the blade's real `(grip, tip)` world segment read off the `RightHand` bone attachment | `StandardMaterial3D`, `BLEND_ADD`, `SHADING_UNSHADED`, `vertex_color_use_as_albedo`, `cull=DISABLED`, `emission_enabled`, **`cast_shadow = SHADOW_CASTING_SETTING_OFF` (C-1)** | **YES** |
| **(c) hit response on the target** | `HitPool` — 16 pooled additive billboard quads (`polySpriteGlow` / `polyspriteline`, PolygonArsenal) + one pooled `OmniLight3D` per live hit, `shadow_enabled = false` | additive unshaded billboards, `cast_shadow` OFF | **YES** |

**There is no fourth layer. No field, no ground decal, no body-surrounding shell, no radial gradient.**
The absence is the design, exactly as in whirlwind — and here it is also *spec text*: § 3.1.2 says
**"No ground propagation."**

**Layer (b) is physical by construction, not by art direction.** The ribbon is never authored at a
radius; it is rebuilt from where the blade actually is. A tinted surface cannot drift away from its
cause when it is generated from its cause. This survives future animation changes for free and it is
the cheapest possible enforcement of L-19.

**Layer (c) is anchored to the enemy body, not to the ground plane and not to the caster.** § 3.1.2:
body-anchored, "strikes an **enemy body**, not the ground plane." Hits spawn at the contact point on a
registered target's body volume. This is machine-gated (§ 1.6).

### 1.2 What takes the tint, and what must NOT

Spec clause, § 3.1.2: *"`TRAIL-BOUNDED`. Tint the weapon trail and the hit-response spark. Do NOT
expand the tint into a body-surrounding field."*

Translated into the concrete properties I vary:

**TAKES the tint (exactly two surfaces):**
- `TrailRibbon` — per-vertex colour RGB in the `ImmediateMesh` surface, plus
  `_ribbon_mat.emission` colour. Alpha ramps along the trail's own age and is **not** an element knob.
- `HitPool` quad `albedo_color` RGB + the pooled `OmniLight3D.light_color`.

**MUST NOT take the tint — and cannot, because it does not exist:**
- No caster-surrounding surface of any kind. **`set_element()` asserts the tinted-surface count is
  exactly 2 kinds and hard-fails otherwise**, so a future editor cannot quietly turn this row into the
  EoR conversion.
- No ground geometry. **Gated numerically:** no authored geometry may have world `Y < GROUND_EPS`
  at any capture frame. "No ground propagation" becomes a measurement rather than an intention.
- Trail **radius** is not a Tier-1 knob. Radius comes from the bone. A radius that grew with the tint
  would be an expanding surface — the exact EoR failure, and the place a builder would most naturally
  introduce it. Recorded so the omission reads as a decision rather than an oversight.

### 1.3 Lifecycle class and how I realize it

**`burst`** (§ 3.1.2), realized as a **three-stroke combo of three independent bursts** — not one long
burst. Per stroke: the ribbon history is **cleared at stroke start**, accumulates over the swing, then
ages out. `TRAIL_SPAN_S = 0.18` (ribbon age window) and `HIT_LIFE_S = 0.22` (hit spark). Between
strokes the ribbon is empty, not merely dim. **Clearing rather than fading is what makes three strokes
read as three events instead of one smear**, and it is the difference between `burst` and `decaying`.

Grounding against C-4: measured burst reference on this stack is `p_turb` at **16 frames / 0.53 s**.
A single stroke here occupies ~11 frames of ribbon at 60 fps, inside the measured burst band. C-4
gives the *schema* and the >5× spread; it does not set any archetype's timing (spec § 2.5 (iii)), and
these numbers are authored — see § 8.

### 1.4 Stage-albedo test value

**0.085.** C-3, twice-attested (this probe + the 2026-06-19 spell-VFX finding): floor albedo 0.20
washed the frame; 0.085 reads correctly. Judging Tier-1 recolour survivability against 0.20 assesses
parameterizability on a lie. **This row is the one where it bites hardest** — a `TRAIL-BOUNDED` row's
entire Tier-1 surface is two small additive elements, so a washed floor destroys precisely the
signal galadriel is asked to discriminate on.

### 1.5 Which element variants, and why that set is sufficient

**Five: `neutral` · `fire` · `water` · `earth` · `wind`.**

**`neutral` is first-class here and is the reason the set is five rather than four.** Spec § 4.2.3:
**70 % of this archetype's referent members carry no element at all**, and L-39 evidence (2) records
that `element_primary` is NULL-dominant in the largest cells — "THE PHYSICAL RULE / name-only strikes"
— so **the tint step is intentionally inert for the majority of the 115 skills bound here.** A variant
set that omitted neutral would demonstrate Tier-1 on the *minority* case and never show the modal one.
The neutral variant must look like a *deliberate colourless steel strike*, not like a fire strike with
the saturation slider at zero.

The other four span the axis the tint has to survive: two chromatic opposites (`fire` warm / `water`
cool), one low-chroma earthy (`earth` — the hardest against a 0.085 floor, because it is closest to
the floor's own hue), and one desaturated bright (`wind`).

**Why this is sufficient and not a content lap:** Tier-1 asks whether *the parameterization survives*,
not whether every element ships. Five variants exercise every branch `set_element()` has. Adding
lightning, shadow and holy would add zero branches and four renders.

### 1.6 Machine gates for this row

| Gate | Bar | What it refutes |
|---|---|---|
| tinted-surface count | **exactly 2 kinds** (ribbon, hit quad/light) | the EoR conversion, introduced later by edit |
| ground propagation | **zero authored geometry below `Y = 0.15 m`** at every capture frame | "no ground propagation" as intention rather than fact |
| hit anchor | **every hit spawn within `HIT_EPS` of a registered target's body volume** | a "hit response" that is really a caster-centred flash |
| trail-to-cause coincidence | max distance from any ribbon vertex to the blade segment's swept surface **below a stated bar** | "an energy wave chasing the weapon" — the row's named failure |
| stroke separation | ribbon vertex count **returns to 0** between strokes | one smear masquerading as three events |

### 1.7 Third-stroke escalation hook — NOTED, NOT BUILT

§ 3.1.2: *"Rive escalates on the third stroke — cadence coupling and a Tier-2 flourish hook that costs
no bespoke asset."* The dispatch asks me to **note, not build**, and to record whether the base
structure leaves room.

**It does, and the room is a scalar.** `_stroke_index` already exists as the variable that resets the
ribbon and selects the swing arc. An escalation is a per-stroke multiplier applied to `TRAIL_SPAN_S`,
ribbon emission energy, and hit count — three existing scalars, **no new node, no new asset, no new
layer, and no change to the tinted-surface count** (so the § 1.6 gate still passes with escalation on).
**I am not building it.** Tier-2 is out of scope for this tranche by ruling, and § 9.4 confirms the
hook's viability from the built structure rather than from this prediction.

---

## 2 · ROW 2 — `ground_targeted_circle` (§ 3.1.1) · PAYLOAD-CARRIED · `hybrid` · composite · **carries RT-8**

115 skills / 102 kits. Largest archetype in the vote.

### 2.1 Layer decomposition → which Godot node carries which layer

T-A names two independently swappable layers:

| T-A layer | Godot node | Construction | Tinted? |
|---|---|---|---|
| **(a) crisp thin perimeter annulus with TRANSLUCENT interior** | `Perimeter` (`MeshInstance3D` + `ImmediateMesh` annulus band) **+** `Interior` (`MeshInstance3D` disc) | perimeter: additive unshaded band with **hard inner/outer edges** — no soft radial falloff, because crispness IS the deciding property. interior: **`BLEND_MIX` at low alpha**, `polysplat` cracked-ground texture, so floor detail reads *through* it | **YES (both)** |
| **(b) vertical payload descending on the centre axis** | `PayloadPool` — pooled mesh instances on the centre axis (`PolyDiamond` shard / `PolySphereSmall` meteor / `PolyGlowTube` column) + an impact flash at ground contact | additive unshaded, `cast_shadow` OFF (C-1) | **YES** |

Both layers tinted, per § 3.1.1: *"Tint both layers; motif-swap on the descending payload."*

**Caster is legible at frame-edge and entirely outside the effect** (§ 3.1.1). The caster is staged
off the circle, not in it — this row is world-ground anchored and the caster is not part of the
emitter geometry.

**Target coverage ≈ 20 %** — mid-band against C-5's measured 0.03 %–67 % span.

### 2.2 What takes the tint, and what must NOT

**TAKES the tint:** perimeter band vertex colour + emission; interior decal `albedo_color` RGB;
payload mesh albedo/emission; impact flash.

**MUST NOT move under Tier-1:**
- **Perimeter geometry** — inner radius, outer radius, and band thickness are **fixed across every
  variant**. The perimeter is this archetype's telegraph for 115 skills; a recolour that thickens or
  softens it deletes the thing the row exists to deliver.
- **Interior alpha ceiling** — the interior must stay translucent in every variant. A tint that
  raises interior opacity converts "a marked patch of ground you can still see" into "an opaque
  coloured disc," which is the Meteor-Indigo failure (§ 2.5).
- Asserted in `set_element()` and measured in § 9.

### 2.3 ⚑ The deciding property: PERIMETER DEFINITION — made measurable, not asserted

§ 3.1.1: *"For 115 skills the player must read 'a thing is going to land THERE' **before it lands**."*
GD Devastation was rejected for establishing the footprint **temporally** rather than through a hard
perimeter — "the archetype's telegraph deleted." **I do not get to claim I avoided that by intending
to.** Two gates:

1. **Spatial crispness.** Sample the rendered frame along radial rays from the projected circle
   centre; take the intensity profile across the annulus. **Bar: the 10 %→90 % rise of the perimeter
   edge occupies a small, stated pixel count at the ratified camera.** A soft glow ring fails this;
   a hard band passes.
2. **Temporal precedence — the telegraph gate.** At the frame where the payload is still
   `>= TELEGRAPH_H` metres above the ground, the perimeter must already be at **≥ 90 % of its final
   intensity**. This is the literal operationalization of *"before it lands"*, and **it is the gate
   that would have failed Devastation.**

### 2.4 RT-8 — the two pre-registered params

Pre-registered at spec § 6.1 from the L-39 key-grain audit. **Measured residuals, not post-hoc
inventions.**

#### `payload_vector` ∈ {`descend`, `erupt`}

Same perimeter grammar, inverted payload direction. 3 erupt-from-ground skills (Fissure, Fire Trap)
live inside this key.

**Build intent:** one emitter, one signed axis parameter (`+1` descend / `−1` erupt), swapping start
height, travel direction, easing, and the payload mesh (`PolyDiamond` shard → `PolySpikeSimple` /
`PolyIcicle02` spike). The perimeter layer is **untouched** by the param — that is what "same
perimeter grammar" means and it is checkable: the perimeter's vertex buffer must be **identical**
between the two variants.

**The dispatch's explicit clause:** *"If the `erupt` variant cannot share the `descend` emitter
cleanly, that is a FINDING for the next lap — surface it. It is not a silent fork."* **§ 9.5 reports
the answer honestly either way.** I have a real prediction that it will *not* be perfectly clean —
`descend` gets its telegraph for free (the payload is visible falling, so precedence is automatic),
whereas `erupt` has **nothing above ground to see** during the telegraph window, so the perimeter is
carrying the whole telegraph alone. That asymmetry is a property of the archetype, not of my code, and
if it forces divergence I will say so rather than paper it.

#### `zone_valence` ∈ {`hostile`, `friendly`}

A **palette-convention rule**, Tier-1-adjacent, **zero new assets**. ~7 friendly-platform skills
(Inquisitor-Seal class) live in this key. § 6.1: *"a player must never read a friendly platform as
enemy fire."*

**The convention I am authoring, and the rule behind it:**

> **Valence OUTRANKS element on the zone layers.** In the `friendly` variant, the perimeter and
> interior take a **fixed friendly palette** — not the element tint. The element still reads, on the
> **payload**. In `hostile`, the zone layers take the element tint as normal.

Plus one structural signature costing zero assets: `friendly` draws the perimeter as a **segmented
band** (alternating quads skipped in the *same* annulus mesh — no new geometry, no new texture),
`hostile` draws it solid.

**Why the override rather than a hue shift:** a hue-shift convention fails exactly when it matters —
a friendly *fire* platform and a hostile *fire* meteor would land in adjacent hue, and the player
reading them apart at speed would be relying on the very channel that is already carrying element.
**Misreading valence is a death; misreading element is a suboptimal potion.** The asymmetry in
consequence should be reflected in the asymmetry of the encoding. Element is denied the zone layers in
`friendly` because valence needs an *uncontested* channel.

**This is an authored convention and it is flagged as such** — Discipline #40, § 8, `SCAFFOLD-WITH-
PENDING-DECISION`. It is Tier-1-adjacent per RT-8, and a palette convention that binds ~7 skills is
the kind of default that becomes de facto canonical if nobody re-decides it. **It should be ratified
or overruled, not inherited.**

### 2.5 Named failure mode to avoid: the Meteor-Indigo interior bloom

§ 3.1.1 confound register: Meteor Indigo (`O4_HTOkjOAc`) **"blooms out its own interior at large
scale."** The dispatch: *"Check your effect at large scale before you call it done."*

**Gate (scale-invariance of translucency):** render at nominal radius and at large radius; measure
`interior_mean_luminance / perimeter_peak_luminance` at both. **Bar: the ratio must not increase with
scale.** A bloom shows up as the interior climbing toward the perimeter as radius grows — because
additive payload and residue stack over more screen area. This turns "check it at large scale" into a
number, and it composes with C-3: **the bloom and the albedo error are the same failure** (additive
stacking blowing to white) arriving through scale rather than through floor brightness.

### 2.6 Lifecycle class and how I realize it

**Composite: `burst` (payload) → `decaying` (residue)** (§ 3.1.1). Basis in T-A: the Alabaster frame
shows *a previous cast's residue coexisting with a fresh cast* — a lifecycle state no other reference
in the corpus shows.

Realized as two independent clocks on the same effect: the payload runs a short burst
(`PAYLOAD_FALL_S`), and the interior residue runs a long decay (`RESIDUE_S`) that **outlives the
payload**. **I stage two casts offset in time so the coexistence is visible in an actual frame**, not
merely enabled in code. If the reference's distinguishing lifecycle state is not in my capture, I have
not built the lifecycle — I have built a burst with a longer tail.

### 2.7 Stage-albedo test value

**0.085**, same as row 1, same C-3 reasoning. **This row has the largest additive area of the three**
(≈20 % coverage, payload plus perimeter plus residue), so it is where additive-stacking-to-white is
most likely to appear — which is precisely why the scale gate (§ 2.5) is measured against this
albedo and not a brighter one.

### 2.8 Which element variants, and why that set is sufficient

**Six renders, chosen to cover the params rather than the palette:**

| # | element | `payload_vector` | `zone_valence` | scale | what it demonstrates |
|---:|---|---|---|---|---|
| 1 | `fire` | descend | hostile | nominal | base binding; meteor motif |
| 2 | `water` | descend | hostile | nominal | Tier-1 tint + shard motif-swap |
| 3 | `earth` | descend | hostile | nominal | hardest tint against a 0.085 floor |
| 4 | `fire` | **erupt** | hostile | nominal | RT-8 `payload_vector`, same element as #1 so the *only* delta is the param |
| 5 | `water` | descend | **friendly** | nominal | RT-8 `zone_valence`; valence-overrides-element visible against #2 |
| 6 | `fire` | descend | hostile | **large** | § 2.5 interior-bloom check against #1 |

**Sufficiency argument:** every RT-8 param is demonstrated on at least one variant **with a matched
control** (#4 vs #1, #5 vs #2, #6 vs #1) so each is a controlled comparison rather than a lone
example. That is the acceptance criterion's "demonstrated on at least one variant each," met with the
control that makes the demonstration mean something. Three elements are enough to show the tint
survives; a fourth adds a render and no branch.

---

## 3 · ROW 3 — `aura` (§ 3.1.8) · FIELD-CARRIED · `magical-cause` **(CORRECT)** · `sustained`

73 skills / 61 kits. **Scope, per gandalf ruling L-41: I mint `caster_centred` (67 skills) and nothing
else.** `world_placed` (4) and `delegate_carried` (2, the summoner GAP) are **not authored**. That is
out of scope **by ruling, not by omission** — if I find myself authoring a variant for the 4 or the 2,
I stop.

### 3.1 Layer decomposition → which Godot node carries which layer

| T-A layer | Godot node | Construction | Tinted? |
|---|---|---|---|
| **(a) radius-defining ground ring / falloff** | `Ring` (`MeshInstance3D` + `ImmediateMesh` annulus) **+** `Falloff` (soft inward gradient disc, `polySpriteRingGlowSoft`) | additive unshaded, `cast_shadow` OFF (C-1); **low alpha by contract** | **YES** |
| **(b) sparse influence particles** | `InfluencePool` — a **deliberately small** pool of slow drifting additive billboards inside the radius | additive unshaded, `cast_shadow` OFF | **YES** |

**Two layers, no third.** No opaque fill, no dome, no column.

### 3.2 What takes the tint, and — the load-bearing clause — what must NOT

§ 3.1.8, verbatim: *"Tint the ring and the influence particles. **Radius and opacity are NOT Tier-1
knobs on this archetype** — they are the archetype's readability contract, and a recolour must not
move them."*

**TAKES the tint:** ring vertex colour + emission; falloff `albedo_color` RGB; influence-particle
albedo RGB.

**MUST NOT move across variants — and this is machine-gated, because it is the row's whole contract:**
- **Radius.** `set_element()` never touches it.
- **Opacity.** Alpha is a constant of the archetype, not of the element.
- **Gate:** capture every variant, measure **rendered ring radius in pixels** and **integrated alpha
  over the disc**; assert both are **equal across all elements within tolerance**. A recolour that
  moved either would be a Tier-1 violation *that looks like a nicer aura*, which is exactly the kind
  that survives review.

### 3.3 `magical-cause` is CORRECT — I am not "fixing" it

§ 3.1.8 and § 3.0: *"Scoring an `aura` down for being decorative applies the criterion where it does
not live — decoration is what an aura is."* **This row is the calibration case for the whole rubric.**
The instruction cuts against every instinct the other two rows train, so I state it as a build
constraint: **I must not add physical-causality signals to this row to make it "score better."** No
impact sparks, no contact response, no ground scuff. Adding them would corrupt the one row that tests
whether the gate correctly declines to penalize correct decoration — and it would do it in the
direction that *looks* like diligence.

**Nothing about this contradicts C-8.** The two are easy to conflate and they are opposites:
a **correctly authored** decorative field must pass (that is this row's purpose); an **undeclared
inherited** emitter is not a scoring question at all but a control failure in the capture. Which is
why `HolyAura` — an undeclared caster-centred field — must be stripped from **this row above all**
(§ C-8.1).

### 3.4 The coverage-ceiling solve

The selected property (§ 3.1.8): it *"communicates influence without filling the radius with opaque
effects"* — the coverage-ceiling solve an always-on field needs. C-5: readability has a floor **and** a
ceiling; measured span 0.03 %–67 %.

**A sustained effect is the hardest case for the ceiling** — it is on during everything else. Two
gates:

1. **Opaque-fraction gate.** The fraction of interior disc pixels above an opacity threshold must stay
   **low**. Sparse means sparse.
2. **Read-through gate — and this one answers galadriel's question directly.** Her dispatch asks:
   *"because 112 `self_buff` skills will be active during other skills: does `aura` remain something
   other archetypes' VFX stay readable through?"* I answer it with an experiment instead of an
   opinion: **stage row 1's `melee_strike` inside row 3's aura radius and capture it.** Then measure
   the melee trail's contrast against the same trail captured with the aura off. **Bar: the trail's
   peak-to-local-background contrast must not collapse.** This is nearly free given a shared stage,
   and it converts her question from a judgement call into a measured delta.

### 3.5 Lifecycle class and how I realize it

**`sustained`** (§ 3.1.8) — genuinely never-ending, not a long decay. The ring and falloff hold
constant intensity; the influence particles recycle continuously through the pool. C-4's measured
sustained references (`p_flame`, `p_spike`, `b_poison`, `s_fire` — all 90/90 frames) are the class
exemplars.

**Windup: none.** § 3.1.8 records `windup = N` on all 5 candidates and rules it **coherent** —
`motion_signature_attested = NULL` archetype, **not under-research**. So the absence of a windup here
is spec-faithful, and I record it explicitly so it is not later read as a gap I forgot to fill.

### 3.6 Stage-albedo test value

**0.085.** C-3. **This row has the subtlest interaction with albedo of the three:** its whole design is
low-alpha additive over a large area, which is the precise configuration that "blows to white over a
light floor." At 0.20 the falloff would wash out and the coverage-ceiling solve would be invisible —
**the row would look like it had failed at its one selected property, because of the floor.**

### 3.7 Which element variants, and why that set is sufficient

**Four: `fire` · `water` · `earth` · `wind`.** No neutral variant — unlike `melee_strike`, this row's
members are element-bearing (an aura's whole job is signalling *what kind* of influence), so neutral is
not the modal case here and adding it would test nothing.

Four is sufficient because the Tier-1 assertion on this row is **an invariance claim, not a coverage
claim**: radius and opacity must be *identical* across variants. Four samples establish that with a
spread of hue and chroma; a fifth adds a render and no branch.

---

## 4 · What all three rows share (stated once)

- **Camera:** the ratified combat camera — FOV 40 / pitch −55 / yaw 47 / dist 34
  (`data/camera_floor1_ratification.md`). Every readability claim is made at the camera the player
  actually has, per § 3.2's "readability at our gameplay camera."
- **Stage albedo 0.085** (C-3), floor 60×60 m, dark-mood register (§ 1.2) — background `0.045/0.050/
  0.062`, filmic tonemap, glow on. **Every "loses contrast on dim terrain" dock in T-A is a real risk
  on this stage, not a footage artifact.**
- **C-1 applied to every additive/emissive mesh I mount**, without exception —
  `cast_shadow = SHADOW_CASTING_SETTING_OFF`, `shadow_enabled = false` on every pooled light.
- **Deterministic stepping.** The stage owns the clock and steps each effect at a fixed 1/60 s with
  the effect's own `_process` disabled. Captures are reproducible frame-for-frame, which is what makes
  an ON/OFF or variant-to-variant diff a valid comparison rather than two nearby frames. Inherited
  from the P0-b determinism arm (§ 2.2) and from the whirlwind gate's corrected control.
- **Off-screen renders use `--rendering-driver metal`, never `--headless`** — headless cannot render
  the Metal scene and the SubViewport reads back null.
- **C-2 and C-7 do not bind** — no beam-class row here. **C-6 does not bind** — no attractor row here.

## 5 · Asset selection (§ 7.1 — explicitly mine; recorded, not escalated)

Primitives mounted from **PolygonArsenal** (`assets/PolygonArsenal/`), which passed a 60/60 load gate
(`gate_report.json`):

| Row | Layer | Asset |
|---|---|---|
| 1 | weapon trail | *procedural* `ImmediateMesh` — bone-derived, no vendor prefab (see below) |
| 1 | hit response | `textures/polySpriteGlow.png`, `textures/polyspriteline.png` |
| 2 | perimeter | *procedural* `ImmediateMesh` annulus — crispness is the deciding property |
| 2 | interior decal | `textures/polysplat.png` |
| 2 | payload (descend) | `meshes/PolyDiamond.res`, `meshes/PolySphereSmall.res`, `meshes/PolyGlowTube.res` |
| 2 | payload (erupt) | `meshes/PolySpikeSimple.res`, `meshes/PolyIcicle02.res` |
| 3 | ring / falloff | *procedural* annulus + `textures/polySpriteRingGlowSoft.png` |
| 3 | influence particles | `textures/polySpriteGlow.png` |

**Why primitives and not whole vendor prefabs — the reasoning, since asset selection is mine to make
and record.** The pack ships complete effects (`SwordTrail`, `GroundSlamBlue`, `AuraDamageFrost`,
`ShieldAuraBlue`) that would have been faster to mount. I did not mount them, for three reasons:

1. **Tier-1 requires reaching the tint.** These prefabs carry baked gradient ramps and per-emitter
   colours across dozens of sub-resources. Recolouring them means walking and overriding an authored
   palette that fights back, and "the tint survived" would then be a claim about my override walk
   rather than about the effect's parameterizability.
2. **L-19 requires reaching the geometry.** A prefab trail is authored at a radius; a bone-derived
   ribbon is authored at its *cause*. The whole point of the trail layer is that it cannot drift from
   the weapon, and that property is not available in a prefab.
3. **The layer decomposition is the deliverable.** T-A's independently-swappable-layers claim is what
   makes Tier-1 possible at all. A prefab is one opaque layer.

**Where the vendor content earns its place is at the primitive level** — meshes and textures give the
Synty-adjacent stylized-low-poly read (§ 1.2 register A) for free, without importing a palette. This
is the register-fit lever the spec names: *"a reference whose effect is carried by light and particles
is a good fit by construction"* — and light and particles are exactly what these primitives are.

**`Assets/` is read-only and nothing under it is modified.**

## 6 · Cross-seam contract change

**NONE.** Godot-side presentation authoring only. `payload_vector` and `zone_valence` are VFX-authoring
parameters inside the presentation seam. If a later lap needs them driven from engine emission, that
is a contract change **then**, and it gets its own MIGRATION.md. **Round-trip: not applicable.**

## 7 · What I did NOT read — the quarantine, held as a whitelist

Per the standing rule ratified this session: **a clean-room brief is a WHITELIST, not a blacklist.**
A prohibition list is illustrative of the hazard, never exhaustive of it.

**Quarantined by the dispatch and NOT read:** charter **L-36** and **L-37**; sealed spec **§ 5** (lines
927–1022, incl. § 5.0/5.1/5.2/5.3); the carve-out #2 request
(`gandalf/requests/2026-08-24-knight-rider-carveout2-step2-build-wave.md`).

**The complete extraction the dispatch grants in their place:** tier-2 rulings are **A-1 YES · A-2
ADOPT + WW-AB · A-3 same pipeline as A-1 · Class B REJECTED**. **None of the four bears on tranche 1**,
and I needed nothing further from them.

**Sections of the sealed spec I did NOT open, because the dispatch did not grant them** — applying the
whitelist rather than the prohibition list: § 0, § 3.1a, § 3.1b, § 3.2, § 4 (all), § 6.2–§ 6.6, § 8,
and every row § 3.1.3–§ 3.1.7, § 3.1.9–§ 3.1.24. Two facts from outside my granted range reached me
**through the dispatch's own text** and are used as the dispatch presented them, not sought at source:
§ 4.2.3's *"70 % of this archetype's referent members carry no element"* and the L-29/L-39/L-41
rulings quoted inline. Where I cite § 4.2.3 above, I am citing the dispatch quoting it.

**Whirlwind:** `whirlwind` remains out of scope here. I read **my own** whirlwind mint note and my own
`wwcr_*` source — my work-product, minted and tagged before this dispatch, not adopted-lineage
material — for the harness pattern and the C-8 finding.

## 8 · Discipline #40 register — every scaffold value in this tranche, declared

**Class R = derived from the spec, a ruling, or a measurement of record** (not scaffold — traceable).
**Class A = AUTHORED, no reference basis** → `SCAFFOLD-WITH-PENDING-DECISION`.

The corpus supplies **no windup coverage** (§ 3.1.8 `windup = N` on all 5 `aura` candidates) and
**T-A specifies no durations at all outside `whirlwind`'s two** (§ 2.5: *"The only cadence NUMBERS in
T-A are whirlwind's spin-up 0.70 s / spin-down 0.80 s"*). **Therefore every timing number in this
tranche is Class A by construction.** That is not a defect in my build; it is the state of the
evidence, and the honest move is to mark it rather than to imply a basis I do not have.

| Value | Row | Class | Basis / status |
|---|---|---|---|
| stage albedo `0.085` | all | **R** | C-3, twice-attested |
| camera FOV 40 / pitch −55 / yaw 47 / dist 34 | all | **R** | `data/camera_floor1_ratification.md` |
| `KingRig.stock_vfx_enabled` default `true` | all | **R** | deliberately preserves existing behaviour; flip is a routed recommendation, not an executed change |
| `TRAIL_SPAN_S = 0.18` | 1 | **A** | authored; inside C-4's measured burst band, which is a *schema* not a timing (§ 2.5 iii) |
| `HIT_LIFE_S = 0.22` | 1 | **A** | authored |
| 3-stroke combo count | 1 | **A** | authored; Rive's third-stroke escalation is referenced, the *count* is not |
| `GROUND_EPS = 0.15 m` | 1 | **A** | authored gate threshold for "no ground propagation" |
| perimeter inner/outer radius + band thickness | 2 | **A** | authored to hit the ≈20 % coverage target (**R**: the 20 % is § 3.1.1) |
| `PAYLOAD_FALL_S`, `RESIDUE_S` | 2 | **A** | authored; the *composite* lifecycle is **R** (§ 3.1.1), the durations are not |
| `TELEGRAPH_H` (telegraph-gate height) | 2 | **A** | authored gate threshold |
| **`zone_valence` friendly palette + valence-outranks-element rule** | 2 | **A** | **the most consequential scaffold in this tranche — a palette convention binding ~7 skills. RT-8 calls it "a palette-convention rule"; it does not supply the palette. Ratify or overrule.** |
| `friendly` segmented-perimeter signature | 2 | **A** | authored structural convention, zero new assets |
| aura radius, alpha ceiling, influence-pool size | 3 | **A** | authored; the *invariance requirement* is **R** (§ 3.1.8), the values are not |
| element→RGB palette (5 colours) | all | **A** | authored; carried forward from the whirlwind mint for cross-row consistency. **Element grading is rocket's seam (X-3) and this palette does not pre-empt it.** |

---

## 9 · RESULTS

> *Appended after the build. Everything above this line was committed first.*
