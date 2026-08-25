# S2C — TRANCHE 3A MINT NOTE (the eight beam-pack-INDEPENDENT rows)

**Author:** drax (presentation seam — `reincarnated-godot/`)
**Dispatch:** `agentic_orchestration/dispatches/2026-08-25-drax-s2c-mint-tranche-3a.md` (Gate-1 CLEARED, PASS-WITH-FINDINGS, jack-ryan 2026-08-25)
**Spec of record:** `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` — **STATUS: SEALED. The filename says DRAFT; the STATUS line governs.**
**Gate built toward:** `galadriel/notes/2026-08-24-s2-minted-gate-procedure.md`
**Rows:** § 3.1.11 `dash_attack` · § 3.1.15 `blink` · § 3.1.22 `teleport` · § 3.1.23 `leap_strike` · § 3.1.13 `ground_slam` · § 3.1.16 `cone` · § 3.1.17 `orbit` · § 3.1.19 `vortex_pull`

> **§§ 0–8 ARE COMMITTED BEFORE THE FIRST EFFECT NODE EXISTS.** That ordering is the receipt shape
> (tranche-1/2 precedent) and it is what DRIFT-CRITIC audits against. § 9 RESULTS is appended after.
> **Everything below this line that reads as a number is a PREDICTION until § 9 says otherwise.**

---

## 0 · Pre-execution refutation surface

Stated first so a later finding cannot be presented as foresight.

| # | If this happens, the dispatch's plan is wrong, not my execution |
|---:|---|
| **0.1** | **The mover rows cannot satisfy `00-pre`/`08-post` diff-to-zero on their control arms.** Four rows displace the caster BY CONSTRUCTION. See § 2 — I am amending the check rather than failing it, and the amendment is surfaced, not absorbed. |
| **0.2** | **`cone`'s ordered enemy launch and `vortex_pull`'s prohibited enemy displacement are the same physical act on this stage.** Both move a staged body. The line between them is real but it is a LINE, and § 3 draws it in the open rather than pretending it is a cliff. |
| **0.3** | **The ≥ 1 % `teleport` arrival floor may read as excessive rather than invisible.** The spec pre-registered the revisit trigger in both directions. If it reads excessive, that is the trigger firing, not the row failing. |
| **0.4** | **`vortex_pull`'s `PAYLOAD-CARRIED` axis is flagged PROVISIONAL BY THE SPEC ITSELF.** If authoring shows the axis is wrong, that is a finding for gandalf, surfaced — never a silent re-classification. |
| **0.5** | **The MP4 pipeline may cost materially more per row than the still pipeline.** R-1 is an MP4 row by design so the clip instrument is priced inside the first two rows. HALT-and-surface fires on cost as well as on defects. |

---

## 1 · Two structural decisions taken before any row, and why each is forced

### 1.1 ⚑ NO `class_name` ON ANY OF THE EIGHT NEW SCRIPTS — `preload()` by path instead

Tranche 2 registered seven new global classes (`S2BLine`, `S2BMeleeArc`, …) and the beam pack's
UID cache survived it. **That is evidence, and I am not acting on it.**

C-7's one standing prohibition is *"do not trigger a UID-cache rebuild"*, **3B depends on that cache
being intact**, and registering a global class requires an editor import pass. `s2_stage_env.gd`
already carries the compliant pattern in its own header and has since E-0: consumers `preload()` the
file by path, which needs no registry entry and **cannot invalidate a UID.**

The cost is one property: a `preload`ed script without a `class_name` cannot be the static type of a
variable, so the harness holds these eight untyped and dispatches dynamically. **The safety that
buys back is `selfcheck()`** — every structural claim in every row is a runtime assertion in the
shipping object, which is where tranche 1 and 2 put it anyway.

**"It worked last time" against an explicit standing prohibition, when a zero-cost alternative
exists and a sibling dispatch depends on the property, is not a reason. It is the shape of one.**

### 1.2 ⚑ THE MOVER IS DRIVEN BY THE EFFECT, AND IT RUNS IN THE CONTROL ARM

`dash_attack`, `blink`, `teleport` and `leap_strike` displace the caster. The displacement is the
**archetype**, not the effect's decoration.

Precedent settles who owns it. `s2a_melee_strike.gd:163` `set_vfx_visible()` carries the tranche-1
ruling verbatim: *"The gate CONTROL condition: pose + blade motion run identically, all VFX layers
hidden. Diffing against 'no strike at all' would measure the caster's pose rather than the effect."*

So: **the effect object owns the mover, and the mover moves whether or not `_vfx_visible` is true.**
A control arm in which the caster stands still would make every mover row's fx-on/fx-off diff a
measurement of *the caster having moved*, which is the whirlwind-gate defect re-staged on four rows
at once.

---

## 2 · ⚑ THE CONTROL LAW ON A MOVER ROW — the acceptance criterion I cannot satisfy as written, and what replaces it

**Dispatch acceptance criterion:** *"`00-pre`/`08-post` diff exactly 0 on every row, both stages."*

**On the four mover rows this is unsatisfiable without destroying the archetype.** The check's
purpose (pre-flight 2, *"a control must control everything that moves"*) is to establish that any
fx-on/fx-off difference is attributable to the effect and to nothing else. `00-pre` ≡ `08-post` on
the control arm is a **sufficient** test of that when the row has no authored body motion. Six of my
eight rows have none and get the check exactly as ordered. **Four do, and for them the check does
not fail — it does not apply.** A dash that returns to its start by `08-post` would pass the check
and would not be a dash.

**I am not waiving it. I am replacing it with three checks that are jointly stronger, and every one
of them is a measurement rather than an argument:**

| | Check | Why it is stronger than the thing it replaces |
|---|---|---|
| **M-C1** | **`00-pre` fx-on ≡ `00-pre` fx-off, BYTE-IDENTICAL.** | The ordered check compares two frames *within one arm*. This compares **across the arms**, before the effect exists — which is the claim actually being made. |
| **M-C2** | **The caster's world transform at every mark is BIT-EQUAL between the fx-on and fx-off arms**, emitted per mark by the harness and compared by the gate. | This is *"the control controls everything that moves"* stated directly, on the thing that moves, rather than inferred from a frame diff. |
| **M-C3** | **`00-pre` vs `08-post` on the fx-off arm IS non-zero — and every differing pixel lies inside the caster's SWEPT SCREEN CORRIDOR**, computed from the M-C2 transforms and dilated by the caster's own screen disc. | Converts *"the check does not apply"* into **"the check fails in exactly the predicted place and nowhere else."** A pose drift, a clock drift or a stray emitter lands OUTSIDE the corridor and is caught. |

**M-C3 is the load-bearing one and it is the same discipline as the emptiness sweep: name the
region, then require the difference to live inside it.** A waiver says *"ignore this number."*
M-C3 says *"here is the number, here is the region it is confined to, and here is the arithmetic
that would convict me if it were not."*

⚑ **SURFACED TO knight-rider, NOT ABSORBED** (§ 8). This is a dispatch acceptance criterion being
executed differently from how it is written. It is refutation condition 0.1 and it is reported as
one whether or not the substitute passes.

---

## 3 · ⚑ THE BOUNDARY BETWEEN `cone`'s ORDERED LAUNCH AND `vortex_pull`'s PROHIBITED DISPLACEMENT

Both rows move a staged body. The dispatch orders one (*"Build the launch. It is what the row was
picked for"*, R-6) and prohibits the other (*"Do not implement, stub, or fake it"*, R-8). **I obey
both, and I am recording where the line falls because a future lap will need to know who drew it.**

| | `cone` launch — **BUILT** | `vortex_pull` displacement — **NOT BUILT** |
|---|---|---|
| **Temporal shape** | **Discrete contact response at a contact instant** — the same class already minted twice (`melee_strike` hit response T1; `dash_attack` knockback, this tranche) | **Sustained field continuously supplying a directional vector** |
| **What it carries** | One layer of a burst whose readability is carried by **the fan** | **The archetype's ENTIRE readability** — RT-6: *"in every candidate the inward vector is legible because enemies visibly move"* |
| **If removed** | The row still reads as a forward fan; one L-19 layer is missing | **The row does not read at all** |
| **Engine equivalent** | none — stage-side contact response, presentation | **X-2**, `spatial_engine.py`, gamora's seam, MD-B2-2 precedent |

**The operative distinction: a criterion whose subject is the VFX may use stage-side contact
response; a criterion whose subject is a NON-VFX SYSTEM may not be made to pass by simulating that
system on the capture stage.** Faking the second makes an `UNEVALUABLE` criterion appear to PASS,
which the dispatch correctly calls strictly worse than leaving it unevaluable.

**It is a line and not a cliff, and it is stated here rather than left to be inferred from two
opposite instructions.** Routed as an INFO-class observation, § 8.

---

## 4 · Per-row plan — layers → nodes, tint set, lifecycle, elements, pre-flight

**Common to all eight.** C-1: `cast_shadow = SHADOW_CASTING_SETTING_OFF` on every additive/emissive
mesh and `shadow_enabled = false` on every VFX light, asserted by `s2a_census.gd`'s `!!C-1-SHADOW-ON`
tag, which reaches galadriel's list and not only my selfcheck. C-3: **bare cohort albedo 0.085**
(authored constant); **cathedral and arena cohorts are pack materials** and C-3 is verified as
per-cohort *uniformity*, which is what pixels can attest — **cohorts NEVER pooled** (E-0 law).
C-8: census at every capture mark, both stages, `fx` + `rt` in the declaration key.
**Zero Binbun `beam_vfx` assets in any layer of any row** — payload meshes come from
`Assets/PolygonArsenal/meshes/*.res` (plain `Mesh` resources: no shaders, no particles, no
`uid://` indirection), which is the same source tranche 2 used after the beam pack was measured
self-drifting at ~6.7 % of its authored mask.

**Structured stage of record: `arena`** (E-0's third recipe) **and `cathedral`.** Two stages per row,
never pooled. `bare` is retained as the clean differential surface where the dispatch's checks need
a constant background.

---

### R-1 · `dash_attack` ⊕ `defensive_dash` (§ 3.1.11) — `physical-cause` · `burst` · **TRAIL-BOUNDED** · **MP4 ROW**

**1 · Layers → nodes.**

| Spec layer | Godot realization |
|---|---|
| (a) silhouette + **brief** trail | the `KingRig` itself is the silhouette (mover, § 1.2); trail = one `ImmediateMesh` ribbon rebuilt per frame from the mover's own path history |
| (b) **knockback / contact response DISTRIBUTED ALONG THE PATH** | per-body: a pooled additive `QuadMesh` contact flash + `OmniLight3D`, fired **when the mover passes that body**, plus a lateral displacement applied to that body's transform |
| (c) `[defensive]` deflection flash bound to the mover | a single additive billboard parented to the **mover**, gold-white, **no persistent path ribbon** |

**2 · Tint set — exactly 2 kinds, asserted.** `trail` + `contact`. **MUST NOT:** no aura, no shell,
no radial gradient, no ground decal. ⚑ **This is the smallest Tier-1 surface in T-A and the spec
attaches the warning to it:** *"there is very little here for a tint to occupy, and the temptation
to enlarge the trail into an aura IS the L-19 conversion."* The trail is therefore bounded by an
executable rule, not by taste: **`TRAIL_SPAN_S = 0.09 s`** (against `line`'s 0.34 s, ~3.8× shorter)
and **trail width ≤ the mover's own body girth**, both asserted in `selfcheck()`. 69 % of members
are element-agnostic; `neutral` is a first-class arm.
The `defensive` gold-white is **Discipline #40 Class A — AUTHORED, scaffold-with-pending-decision**,
same status as the `s2a_palette.gd` element table.

**3 · Lifecycle `burst`** — realized as: the trail's vertex count returns to **0** after the dash
clears, sampled at a late mark that exists for exactly that. Coverage windup **Y**.
⚠ **`windup = N` on all five folded `defensive_dash` candidates is the UNBANDED-CLASS SIGNATURE, not
under-research. No windup is invented to fill it.**

**4 · Stage albedo.** bare 0.085 · cathedral/arena pack materials, uniformity-verified per cohort.

**5 · Element set.** `fire · water · earth · wind · neutral` (5) + `defensive=on` layer-toggle arm +
3 aim vectors (C-2). `neutral` is load-bearing at 69 % element-agnostic.

**6 · Pre-flight, with its expected refuting output.**
- *Inspect the artifact that ships* → **assert the DRAWN ribbon instance's AABB is non-degenerate before any measurement.** Refuting output: `aabb_size ≈ (0,0,0)` while `verts_peak > 0` — a ribbon that exists in the tree and draws nothing, which is exactly how tranche 1 measured a trail that was not there.
- *A control must control everything that moves* → **M-C1/M-C2/M-C3** (§ 2). Refuting output: any differing pixel OUTSIDE the swept corridor.
- *Controls on both sides* → every arm has its own matched `novfx` control captured in the same pass, including each aim arm and the `defensive` arm.
- *Both screens* → exact-bound AND by-value. **The arena 0.9993 lesson: one pixel was the entire margin.**
- *Range guards admit ratios > 1* → the along-path illumination ratio is unbounded above; no `0 ≤ v ≤ 1` clamp anywhere in the gate.
- *A name may convict; only arithmetic or pixels may acquit* → `body_lit_frac` is computed as **|lit ∩ body-disc| / |body-disc|** against the fx-off frame at the SAME frame index, never off a field named for the body.

**7 · ⚑ MP4 — capture geometry and the frame window that makes the temporal claim visible.**
**Claim:** contact response is **distributed along the path**, not concentrated at the terminus.
**Window:** `t ∈ [0.24, 1.10] s` at 60 fps = **52 frames**, opening 0.06 s before the dash launches
and closing 0.30 s after the last body is passed. **Geometry:** the locked 2.5D camera, aim = 0,
**three bodies at 2.6 m / 4.4 m / 6.2 m along the path** and **one body 2.9 m off it** — the miss is
part of the receipt.
**Series filed with the clip:** `body_lit_frac` **per body, per frame**. **The discriminator is that
the three on-path bodies peak at THREE DIFFERENT FRAME INDICES, monotone in path distance.** A
single spike at the end is the failure and a still cannot tell you which you built.
⚑ **The clip's frames ARE the series' frames** — one capture pass, one artifact, so the clip and the
series cannot disagree (Gate-1 M4).

⚠ `lYrecr253lY` @ 251 s is a catalogue candidate on this row; **PROMOTION PROHIBITED** (§ 3.1.7). Not opened.

---

### R-2 · `blink` (§ 3.1.15) — `magical-cause` · `burst` · **PAYLOAD-CARRIED** · **frame series (Gate-1 W3)**

**1 · Layers → nodes.** (a) shadow/energy streak along the path = an `ImmediateMesh` corridor ribbon
spanning origin→current, **long and continuous** (the traversal is VISIBLE, § 3.1.15); (b) damage
along the path = a **smooth proximity-driven dissolution** on each body in the corridor — **no
discrete impact spark**; (c) arrival resolution = an additive billboard + light at the destination.

**2 · Tint set — exactly 3 kinds, asserted.** `streak` + `path_damage` + `arrival`.
**MUST NOT:** no weapon trail, no ground decal, no contact spark.

**3 · ⚑ THE FIRST DISTINCTNESS PAIR, AND THE HARDEST IN T-A.** L-29(6): `dash_attack` and `blink`
are identical on all three attested substrate axes (`straight_line`/`motion`/`none`) and held
distinct on **causality class alone**.
**How the separation is BUILT, not asserted:** `dash_attack` fires a **discrete contact flash keyed
to a body at a contact instant** ⇒ `body_lit_frac` shows a **step**. `blink`'s streak lights whatever
is near it as a **continuous function of proximity**, with **no event keyed to a body** ⇒
`body_lit_frac` shows a **smooth ramp**. **The two rows differ in the SHAPE OF ONE CURVE, and the
curve is the same instrument on both.**
**How it is MEASURED:** paired capture, **identical camera and aim vector**, galadriel § 1.2 test (3)
applied in **opposite directions** — `dash_attack` (`physical-cause`) **must** show the step;
`blink` (`magical-cause`) **must not** (§ 1.2's anti-tamper inversion). **Both numbers in ONE
`gate.json` record.** If they look the same, the fold boundary is carried by nothing — **a finding
for gandalf, surfaced, never a silent fork.**

**4 · ⚑ `magical-cause` IS CORRECT AND IS NOT TO BE "FIXED" INTO A PHYSICAL READ.** An arm that
acquires a contact spike here has had physical tells smuggled in to flatter the score.

**5 · `R = 4` dock — "dark palette can lose contrast on dim terrain."** ⚠ **Our register IS
dark-mood, so this is a REAL risk.** Validated against actual stage albedo on **cathedral**, where
structured geometry makes figure/ground falsifiable.

**6 · Elements** `fire · water · earth · wind` (4, PAYLOAD-CARRIED — `neutral` is not the modal
member here) + 3 aim vectors + matched controls.

**7 · ⚑ FRAME SERIES, ORDERED BY GATE-1 W3 AND NOT BY ANYTHING ABOVE IT.** Pair 2's claim is
*authored px in the traversal corridor **in the intervening frames***, and that **cannot be taken off
a single still.** `teleport` gets its series free from its MP4; **`blink` is a stills row and nothing
else ordered a multi-frame capture for it.** Instrument, named: **a frame sequence across
`t ∈ [0.30, 0.80] s` at 60 fps = 30 frames**, same corridor region as R-3, `authored_px_in_corridor`
per frame. **A clip is not required; a series is.** Expected: **non-zero on every intervening frame**
(`teleport`'s must be exactly zero).

---

### R-3 · `teleport` (§ 3.1.22) — `magical-cause` · `burst` · **PAYLOAD-CARRIED** · **MP4 ROW** · ⚠ **THE HEADLINE**

**1 · Layers → nodes.** (a) cast gesture at origin = additive billboard + light, **at the origin,
before the jump**; (b) **SPATIAL DISCONTINUITY** = the mover's `global_position` is reassigned in a
single frame — **nothing travels, and there is no node between the two points to travel**;
(c) arrival flash at destination = additive billboard + light + a brief ground-contact ring.

**2 · Tint set — exactly 2 kinds, asserted.** `departure` + `arrival`. **MUST NOT:** **no streak, no
ribbon, no corridor geometry of any kind.** The absence is the archetype.

**3 · ⚑ THE SECOND DISTINCTNESS PAIR (F-e), AND ITS REGION IS STATED EXPLICITLY SO IT CANNOT RETURN
`UNEVALUABLE` BY ACCIDENT.** The **traversal corridor** is defined as: the screen-space convex hull
of the origin caster-disc and the destination caster-disc, **MINUS both discs each dilated by 1.25×**.
Stating the region is pre-flight 8's requirement — *"where authored pixels and the region are
disjoint, the criterion CANNOT go red and returns UNEVALUABLE, never PASS"* (#80 headline + cl. 1,
the empty-region shape).
⚑ **AND HERE IS THE TRAP IN THAT RULE, WHICH I AM NAMING BEFORE IT BITES:** for `teleport` the
**correct** answer is *zero authored px in the corridor* — which is **exactly what a disjoint region
looks like.** So the sweep alone cannot distinguish *"the archetype is correct"* from *"the
instrument was pointed at nothing."* **The discriminator is the PAIRED leg:** the identical region,
computed the identical way, on `blink`, **must be non-zero.** One region, two rows, opposite
expected outcomes — which is what makes zero a **finding** rather than an artifact.

**4 · ⚑ THE SPEC'D FLOOR.** Arrival burst peak screen coverage **≥ 1 %** at the locked camera.
Derivation carried, not invented: ~30× the measured-invisible datum (0.03 %, `p_trail` at 535 px)
and ~2 orders below the measured occlusion ceiling (67 %). **1 % of 1920×1080 = 20,736 px.**
**Reported per element arm, per stage, cohorts NEVER pooled.**
**Revisit trigger:** scored against the floor **and against the eye — and the eye is Matt's.**
⚑ **A STILL CANNOT EXPRESS A DISCONTINUITY, SO THE MP4 IS THE OBJECT OF THAT JUDGMENT.** Without it
the trigger is unfireable and the WW-AB defect is repeated on the run's most actionable row.

**5 · Lifecycle `burst`.** Elements: 4 + matched controls, both stages.

**6 · Pre-flight.** Coverage-floor risk is the row's whole hazard: *"restrained arrival flash"* sits
near the measured-invisible floor, and **a move the player cannot see is not a telegraph.** Both
screens (exact-bound AND by-value) on the floor comparison.

**7 · ⚑ MP4 — geometry and window.** **Claim:** the archetype **IS** a discontinuity, which is a
two-frame fact. **Window:** `t ∈ [0.20, 1.00] s` at 60 fps = **48 frames**, straddling the jump
instant at `t = 0.50` with 18 frames before and 30 after. **Geometry:** locked camera framing
**both** endpoints — origin and destination must be in one frame or the discontinuity has nothing to
be discontinuous across. **Series filed with the clip:** `authored_px_in_corridor` **per frame**
through the discontinuity, plus `arrival_coverage_pct` per frame. **Expected: corridor px = 0 on
every frame; arrival coverage crossing 1 % within 3 frames of the jump.**

---

### R-4 · `leap_strike` (§ 3.1.23) — `physical-cause` · `burst` · **TRAIL-BOUNDED** · **MP4 ROW** · **the corpus's best windup donor**

**1 · Layers → nodes.** (a) **ANTICIPATION CROUCH** = the mover's root lowered and compressed along
Y over the windup window — **a POSE, deliberately near-untinted**; (b) trajectory = ballistic arc,
caster-bound, restrained `ImmediateMesh` ribbon; (c) **compact** impact radius = ground-anchored
additive disc + light at the landing point.

**2 · Tint set — exactly 2 kinds, asserted.** `trajectory` + `impact`. ⚠ **100 % of this
archetype's referent members are element-agnostic — the PUREST `TRAIL-BOUNDED` row in T-A.** The
tint has almost nowhere to live except the impact. **Accept the small surface; do not manufacture
one.** (Same law as R-1, one notch harder.) **The crouch takes NO tint** — it is a pose, and tinting
a pose is how a windup becomes a charge-up aura.

**3 · ⚑ THE PRESERVED PROPERTY, MADE EXECUTABLE.** *"Restrained palette keeps the character
trajectory and compact impact radius SEPARABLE."* **If a Tier-1 recolour merges trajectory into
impact, the row has lost what it was picked for.** Measured, not asserted: at the impact frame the
**trajectory ribbon's screen mask and the impact disc's screen mask must be DISJOINT** (intersection
= 0 px), on **every** element arm. **A recolour that fuses them convicts itself.**
**Runner-up LE Fury Leap is explicitly "busier" — NOT a C-1 tie; the PoE pick wins on restraint.**
The busier grammar is not imported.

**4 · ⚑ THIS ROW PAYS THE RUN-WIDE WINDUP DEBT.** With `circle`'s D3 Condemn charge it is one of
only **two** strong windup donors the run found against an **80.5 %** windup-scarcity corpus.
**Reported in the GTC shape** (tranche 1 set it: *telegraph full at 0.183 s with payload 5.5 m out*):
**lead time, pre-`t_impact` emitter activity, and the pose's own frame window.**
⚑ **AND THE MARK TABLE SAMPLES THE WINDUP THREE TIMES, NOT ONCE.** Rows 1–2 cost a whole second
capture pass to exactly this: a lead time sampled once, late, reported **0.167 s** — *a property of
where the mark is, not of the beat.* Lead time is a **derived quantity**; windows that carry one are
sampled multiple times, never once.

**5 · Lifecycle `burst`.** Coverage windup/active/impact **Y**. C-2 binds (mover): **3 aim vectors.**
Elements 5 incl. `neutral` (100 % element-agnostic ⇒ `neutral` is the modal member).

**6 · Pre-flight.** As R-1, plus: the crouch's legibility is measured **at the camera** (the earliest
mark at which the pose delta is visible in pixels), never from the authored constant. **The declared
lead time is the comparator; the measured one is the result.**

**7 · ⚑ MP4 — geometry and window.** **Claim:** the leap is *about to land* **before** it lands —
a **lead time**, which is not a still property. **Window:** `t ∈ [0.20, 1.30] s` at 60 fps =
**66 frames**, opening 0.10 s before the crouch begins. **Series filed with the clip:**
`crouch_pose_delta` and `authored_px` **per frame**, with `t_impact` marked — **so lead time is read
off the series rather than trusted from the note.**

---

### R-5 · `ground_slam` (§ 3.1.13) — `physical-cause` · `burst` · **TRAIL-BOUNDED** · **MP4 ROW** · ⚠ **PRE-REGISTERED FOLD TEST**

**1 · Layers → nodes.** (a) weapon-meets-ground impact = the rig's blade driven **into the floor
point** (reusing the tranche-1 pose modifier, which already re-seats the blade without re-positioning
the grip); (b) **a compact circular ground burst well inside the coverage band** = ground-anchored
additive disc + radial spoke ribbon propagating outward on the **floor plane**; (c) contact response
on bodies in range.

**2 · Tint set — exactly 2 kinds, asserted.** `ground_burst` + `impact`. ⚠ **MUST NOT convert the
ground burst into a PERSISTENT FIELD — that is `ground_targeted_circle`, a different archetype with
a different telegraph, and it is ALREADY MINTED (tranche 1), so the confusion is live.** Made
executable: **authored px at the late mark = 0** and **no decal survives the burst.** 81 %
element-agnostic.

**3 · ⚑ THE STEP-2 REVISIT TRIGGER FIRES HERE — PRE-REGISTERED IN THE SPEC, NOT POST-HOC.**
§ 3.1.13: `ground_slam` and `melee_strike` are identical on all three attested substrate axes
(`point_strike`/`melee_arc`/`point`) — **the same shape as the `circle`/`ring` pair that WAS folded**
— and are held distinct on the **STRIKE SURFACE**. The spec's own words: *"the second-strongest
merge candidate in the taxonomy after the one already folded."*

**The object, and it is not a routing statement:** a **PAIRED MP4** — `ground_slam` and the
already-minted `melee_strike`, **same camera, same stage, same aim vector** — plus a `gate.json`
record naming, for each leg: **emitter identity · anchor transform · coverage envelope.**

| | `ground_slam` | `melee_strike` (tranche 1, re-rendered) |
|---|---|---|
| anchor transform | **world ground, y = 0**, at the floor point | **enemy body**, `CONTACT_Y = 1.05` on the mob rig |
| emitter identity | ground disc + floor-plane radial spokes | body-anchored spark billboards |
| ground propagation | **yes — radial, on the floor plane** | **none** |

**If the pair converges, I say so. A fold is a FINDING, not a failure, and it is the outcome the
spec pre-registered.** Verdict stated either way.

⚑ **AND THIS DISCHARGES gandalf's § 4 RIDER FOR FREE.** The `melee_strike` canonical MP4 (spec
§ 3.1.2, *"the cheapest evidence upgrade"*, *"the wave's cheapest Matt-visible artifact"*) **is one
leg of this pair.** Not scheduled separately.

**4 · Lifecycle `burst`.** Coverage windup/active/impact **Y**. Runner-up PoE Ground Slam
**deliberately NOT elevated** (it is `cone`'s shared primary; elevating it double-anchors two
archetypes). Elements 5 incl. `neutral`.

**5 · ⚑ MP4 — geometry and window.** **PAIRED, one window, one camera, one stage.**
`t ∈ [0.24, 1.40] s` at 60 fps = **70 frames** per leg. Both legs framed on the caster with the
struck body in frame, so the **strike surface** is visible in both. **Series filed with the clip:**
`emitter_identity` / `anchor_transform_y` / `coverage_envelope_px` per leg per frame, plus
`ground_propagation_px` — **the discriminator, which must be non-zero on one leg and zero on the
other.**

---

### R-6 · `cone` (§ 3.1.16) — `physical-cause` · `burst` · **TRAIL-BOUNDED**

**1 · Layers → nodes.** (a) the propagating fan = ground-plane `ImmediateMesh` sector expanding
forward from the caster over the burst; (b) **ENEMY LAUNCH + KNOCKBACK** = bodies inside the sector
receive an upward-and-outward ballistic displacement + a contact flash.

**2 · Tint set — exactly 2 kinds, asserted.** `fan` + `contact`. **Tier-1 `TRAIL-BOUNDED`: the fan
is the WEAPON'S CONSEQUENCE, not an independent payload. Do not promote it into a field.** Made
executable: the fan's authored px return to **0** after the burst; it holds no steady state.

**3 · ⚑ `physical-cause` IS THE ENTIRE SELECTION REASON.** *"The only cone candidate with enemy
launch + knockback — contact response on bodies, the exact axis EoR failed."* gandalf's L-41 note:
**the bot-block carry stands, but the selection does not move regardless** — an L-19 judgement no
resolution change can revise. **Build the launch. It is what the row was picked for.** § 3 above
records why this is legitimate here and prohibited on R-8.

**4 · `R = 4` dock — "earthy VFX blends with terrain."** A real coverage-read risk at our camera.
**Tier-1 recolours must preserve figure/ground separation against the ACTUAL stage albedo — measured
on the CATHEDRAL stage, where structured geometry makes it falsifiable.**

**5 · ⚠ The canonical's link is Cloudflare bot-blocked (same signature as `pathofexile.com`).**
**No automated link-check is run against it, by me, anywhere in this tranche.** L-15: a bot-block is
not absence; **403 is never absence** and this run has proved it twice.

**6 · Lifecycle `burst`.** Coverage windup/active/impact **Y**. C-1 applied. Elements 5 incl.
`neutral`; **3 aim vectors** (the fan has a direction, so C-2's reasoning applies even though the
row is not beam-class).

---

### R-7 · `orbit` (§ 3.1.17) — `physical-cause` · **`sustained`** · **TRAIL-BOUNDED** · ⚑ **X-1 DISCHARGED**

**1 · Layers → nodes.** (a) solid revolving payloads with **legible spacing** = N `MeshInstance3D`
payloads parented to an **`OrbitHub` node that rotates**; (b) contact response; (c) **PRESERVED
NEGATIVE SPACE AROUND THE CASTER.**

**2 · ⚑ THE PARENT TRANSFORM IS THE WHOLE L-29(7) ARGUMENT, AND IT IS STRUCTURAL.** *The PAYLOAD
revolves around a stationary-framed character* — **the hub rotates, the caster does not.** Asserted
in `selfcheck()`: the caster's `rotation.y` delta across the entire capture is **0**.
⚠ **This argument is made from § 3.1.17's own text ONLY. No whirlwind artifact is opened, referenced
as a donor, or measured against** — the quarantine binds in both directions.

**3 · Tint set — exactly 2 kinds, asserted.** `payload_trail` + `contact`. **Tier-1 = MOTIF SWAP on
the orbiting payload** (shuriken → blade → hammer → orb) **+ tint its trail.**
⚑ **Payload COUNT and ORBIT RADIUS are ENGINE parameters, NOT element parameters — varying them to
demonstrate Tier-1 demonstrates the wrong axis.** They are exposed and **held fixed** across every
Tier-1 arm; a hash over them is emitted so the gate can prove they did not move.

**4 · ⚑ X-1 IS DISCHARGED, AND THE FINDING THAT CAME WITH IT IS AN AUTHORING INSTRUCTION.**
Tag `gamora/v1.4-x1-orbit-spatial-map` @ `45a0dc15`, on `origin`;
`kit_compiler.py` carries the fix — X-1 comment at `:53`, the `"orbit": "circle"` mapping at `:72`,
the load-bearing annulus NOTE at `:61`. **No X-1 dependency is stated in this row's completion
record; the DISCHARGE is stated, with the tag.**
**The finding:** `circle` is an **APPROXIMATION of orbit's swept ANNULUS, not a representation of
it.** The 6-type vocabulary has **no annulus primitive** and `circle` has **no inner-radius param**,
so the engine gauge **over-covers the interior disc.**
⚑ **THAT OVER-COVERED INTERIOR IS EXACTLY THE REGION THE SPEC TELLS ME TO PROTECT** — *"preserved
negative space around the caster."* **The engine gauge is blind to precisely the property the VFX
must preserve.** So: **author the negative space, MEASURE it, and put the inner radius in
`gate.json`, because nothing downstream of me can infer it.** Reported as **both**
`inner_radius_m` (world) and `negative_space_px` (screen, at the locked camera) — a world number a
future engine lap can consume, and a screen number galadriel can verify against pixels.
⚑ **NOT "fixed" by adding `orbit` to `AOE_GEOMETRIES`, and nobody is asked to** — gamora explicitly
prohibited that inference and it is not my seam.

**5 · The negative space is an ACCEPTANCE CRITERION, not a property.** It is *"the explicit
correction of EoR failure #2"* (caster swallowed by own effect). **Do not lose it to a Tier-1
recolour that raises coverage** — so it is measured on **every element and motif arm**, not once.

**6 · Lifecycle `sustained`** — live against **six `burst` rows in the same tranche** (C-4, spread
> 5×). Realized: the hub rotates indefinitely; authored px are **non-zero at the late mark**, which
is the exact inverse of the six burst rows' late-mark assertion. **STACK-ACCUMULATION reference**
(PoE Blade Vortex, `rCro9h8reZw`) — cited for **how stack count reads as it builds**: payloads phase
in over a build window rather than appearing at full count.

**7 · Confound register: `none named` — and C-1 was applied on a GENUINE TIE**, named rather than
dressed up as discrimination. **Re-audited after inspection** (§ 8).

---

### R-8 · `vortex_pull` (§ 3.1.19) — `hybrid` · **`sustained` field** · **PAYLOAD-CARRIED (PROVISIONAL)** · ⚠ **AUTHOR-not-SELECT + RT-6**

**1 · Layers → nodes.** (a) **PHYSICAL INITIATION** — *a hammer strike triggers the gravitational
eruption*: the rig's blade driven into the floor point, then the field erupts; (b) the sustained
inward field = ground-anchored additive disc + inward-drawn ribbon streamers on the floor plane;
(c) **debris response** = authored `PolyPebble`/`PolyRoundRock` meshes spiralling inward on the
stage clock — **deterministic, no `GPUParticles3D` anywhere.**

**2 · ⚑ AUTHOR-not-SELECT (C-6).** We own **zero** attractor content and **zero** particle-collision
content. **Both work perfectly on this stack and identically on MoltenVK — the gap is CONTENT, not
capability.** This row's canonical is a **SPECIFICATION for an effect to be authored**, not a target
to select a pack asset against. **It is the most expensive row in the tranche and is budgeted as one.**

**3 · ⚑ THE `hybrid` CLASS IS THE ROW'S OWN INSTRUMENT, AND IT IS FALSIFIABLE.** *An inward pull is
inherently magical; this candidate gives it a physical cause* — **the hammer strike is not
decoration; it is how this row satisfies L-19 at all.** So the galadriel § 1.2 test (3) curve on
this row should show **a STEP at initiation** (physical half) **and a FLAT LINE during the field**
(magical half). **That two-phase signature is what `hybrid` predicts, and a row that shows a step in
both phases or neither has not earned the class.**

**4 · Tint set — exactly 3 kinds, asserted.** `field` + `debris` + `initiation`.
⚠ **`PAYLOAD-CARRIED` is PROVISIONAL BY THE SPEC'S OWN WORD** (*"the effect does not exist yet"*).
**If authoring shows the axis is wrong, that is a finding for gandalf, surfaced — not a silent
re-classification** (refutation condition 0.4).

**5 · ⚑⚑ RT-6 — THE DISPLACEMENT CRITERION IS RECORDED `UNEVALUABLE — NEVER PASS`.**
The archetype's readability is carried by a **non-VFX system**: in **every** candidate the inward
vector is legible because **enemies visibly move**, and **no VFX I mint can supply that.**
**Dependency:** **X-2**, engine seam (gamora). gamora's survey returned **wiring, not capability** —
enemy displacement already exists in production (`spatial_engine.py:2378-2443`, the Wave-D fear
flee-AI; *"`vortex_pull` inward displacement is this mechanism with the sign flipped"*). **Cheap.**
**Reason it is nonetheless refused:** a pull would be the **FIRST control effect in the sim to
actually APPLY**, and KC2's B-2 left the effect-application decode a named open (`MD-B2-2`),
deliberately refused. **Building X-2 to unblock one VFX row's SCORING criterion would let a phase
gate set engine law — which inverts engine > game > phase.**
**Owner of the unblock:** **Matt**, at
`canonical/matt_decision_needed/2026-08-25-x2-vortex-pull-displacement-effect-application-precedent.md`.
⚠ **`UNEVALUABLE` IS NOT A SOFT PASS AND MUST NEVER ROUND TO ONE.** It does **not** block this row's
seal nor the wave's 24/24 terminal state — **it blocks the CLAIM**, permanently, until X-2 lands.
**The row is not unfinished. It is fully minted with one criterion that cannot be scored.**
**X-2 is not implemented, not stubbed, and not faked** (§ 3).

**6 · Lifecycle `sustained` field.** Coverage windup/active/impact **Y**. Elements 4.

---

## 5 · Cross-row obligations — the objects, named

| Pair | Claim | **Object** | Expected outcome |
|---|---|---|---|
| **1** `dash_attack` ↔ `blink` | L-29(6): distinct on causality class alone | paired capture, identical camera + aim; **§ 1.2 test in OPPOSITE directions, both numbers in ONE record** | step vs ramp |
| **2** `blink` ↔ `teleport` | F-e: visible traversal vs spatial discontinuity | **corridor region stated explicitly**; `blink` **frame series** (W3) + `teleport` MP4 series | `blink` non-zero every frame · `teleport` **exactly 0** |
| **3** `ground_slam` ↔ `melee_strike` | § 3.1.13 pre-registered fold trigger | **PAIRED MP4** + emitter / anchor / coverage-envelope record | **fold verdict stated either way** |
| **4** `ground_slam` ↔ `ground_targeted_circle` | burst must not read as persistent field | late-mark authored px on both | slam → 0; GTC → residue |
| **5** `orbit` ↔ `vortex_pull` | both caster/ground-anchored `sustained`, `circle`-class | **`orbit` PRESERVES the centre; `vortex_pull` FILLS it** | inner radius > 0 vs centre occupied |

⚑ **FREE FOLD-IN (Gate-1 I2) — retire a known blind spot on SEALED work.** jack-ryan's tranche-2
finding recorded that **rows 3/4/6/7 were never swept for the `melee_arc` C1 defect class.** This
tranche re-opens `melee_strike`, `line` and `multi_projectile` for cross-row comparison anyway, so
the **`authored ∩ region` emptiness sweep runs against those rows' EXISTING gate records at the same
time.** Near-zero marginal cost. ⚠ **If a sealed row's criterion turns out to have been
UNEVALUABLE-not-PASS, that is a finding ABOUT SEALED WORK: surfaced, not repaired here.**

---

## 6 · ⚑ THE CLIP INSTRUMENT — and the cost checkpoint it exists to price

**No MP4 has been produced anywhere in this wave.** WW-AB's entire rendered output is one PNG
directory. This tranche carries a **new deliverable class**, and the dispatch's HALT-and-surface
checkpoint after row 2 **fires on COST as well as on instrument defects.**

**Design — and the design is what makes M4 satisfiable rather than merely satisfied:**

> **The clip's frames ARE the series' frames.** One capture pass writes every frame in the window as
> a PNG **and** emits that frame's numeric row on the same tick. ffmpeg then encodes **those exact
> PNGs**. There is no second render, no resample, no interpolation.
>
> **Consequence: a clip and its series cannot disagree**, because they are two readings of one
> artifact. *"A clip without its series is not a receipt; a series without its clip does not
> discharge the delegated judgment"* — here neither can exist without the other.

Precedent exists in this repo (`scripts/run_ww7_gate2_clip.sh`, SB-1 WW-7: PNG intermediates →
ffmpeg → **ffprobe verification before promotion**), and its FG-9 discipline is carried: **everything
lands on a temporary name; promotion is a separate step that runs only after ffprobe verifies the
stream.** `ffmpeg 8.1.2` present.

**R-1 IS AN MP4 ROW BY DESIGN so the clip pipeline is priced inside the first two rows.**
**Baseline to price against: tranche-2 still arms measured a 6.81 s median over 76 arms** (8.6 min
total, `harness_logs/s2b_rows37_2026-08-24/arm_cost.txt`). **A re-sequence at row 2 is cheap; a
three-row overrun found at row 8 is not.**

---

## 7 · Determinism, and what is NOT claimed

Every effect's own `_process` is disabled; the stage steps it at a fixed `DT = 1/60`. Every
`AnimationPlayer` in the tree is advanced by the **same** fixed `DT` — the tranche-1 defect where
rig and mob skeletons ran on real frame time and two runs reached a mark with bodies in different
poses, which did not merely add noise but **invalidated the instrument**.

**Two independent passes of the full capture, byte-compared.** The bar is byte-identity at the
strictest screen: **`px ≥ 4` AND `maxdiff = 0`**, all three figures reported every pass (M2's
operator, adopted here even though M2 was authored against 3B).

**NOT claimed:** cross-driver byte-identity (structurally N/A — two drivers never emit identical
PNGs). **Zero `GPUParticles3D` in any authored layer of any row**, because they cannot be pinned to
the stage clock; every moving thing in these eight rows is stepped by the stage.

---

## 8 · Routed findings register (pre-registered; § 9 fills in the outcomes)

| # | To | Class | Item |
|---|---|---|---|
| **F-1** | knight-rider | **AMENDMENT** | **§ 2 — the `00-pre`/`08-post` diff-to-zero acceptance criterion does not apply to the four mover rows.** Replaced by M-C1/M-C2/M-C3, which are jointly stronger. **Surfaced whether or not the substitute passes.** |
| **F-2** | knight-rider | INFO | **§ 3 — the boundary between `cone`'s ordered launch and `vortex_pull`'s prohibited displacement.** Both move a staged body; the line is defensible and it is a line. |
| **F-3** | gandalf | pending | **Confound-register re-audit, BOTH directions**, for the four rows carrying `Confound register: none named` (`ground_slam`, `orbit`, `vortex_pull`, `leap_strike`). ⚑ Tranche-1 WARN #1 has teeth: *a `DOSSIER-TEXT` row carries "no confound named" for the trivial reason that NOBODY LOOKED.* **A register that stays empty AFTER inspection is worth strictly more than one that stayed empty because nobody opened the file.** **Which side of galadriel's comparison each confound lands on is named** — a confound she cannot see is a false verdict in either direction. **Spec NOT patched; routed via this note**, as at tranche 1. |
| **F-4** | gandalf | pending | **`vortex_pull`'s `PAYLOAD-CARRIED` axis** — spec-flagged PROVISIONAL. Outcome of authoring reported either way. |
| **F-5** | knight-rider | pending | **Beam-pack reach report, NIL DELTA STATED (#63)** — whether or not any row's authoring reached for the Binbun `beam_vfx` pack. |
| **F-6** | jack-ryan | NOT REACHED | **Emptiness-sweep against tranche-2 SEALED rows 3/4/6/7** (Gate-1 I2 free fold-in). Not run — the tranche halted at the row-2 checkpoint before rows 3-8 opened those records. |
| **F-7** | **jack-ryan** | ⚑ **RAISED** | **A declared constant sitting in a MEASUREMENT'S slot, live in TWO SEALED ROWS.** `line` reports `trail_span_s` 0.34 and realizes 0.3667 (its `single_target` ratio is 4.53 reported / 4.89 real); `melee_strike` declares 0.18, realizes 0.1333, and **references the constant nowhere in the file**. Neither moves a verdict; both numbers are wrong. § 9.6. **Surfaced, not repaired.** |
| **F-8** | **galadriel + knight-rider** | ⚑⚑ **RAISED — THIS IS THE HALT** | **galadriel § 1.2 test (3) SATURATES.** Body-illumination FRACTION is bounded above by 1; when the signal pins at 1.0 the ramp is clipped and its rise is forced into the pre-saturation frames, **inflating any step-vs-ramp statistic toward "step"**. `blink` pins at 1.0 for 5-6 frames; `dash_attack` never reaches 0.99. ⚑ **The artifact pushes the `magical-cause` leg toward looking physical — i.e. toward a FALSE REFUTATION of a sealed L-29 fold boundary.** Pair 1 is **UNEVALUABLE, never FAIL**. § 9.3. The instrument is ordered for **every remaining row in the wave**, which is why this stops the tranche and not just the row. |

⚑ **F-1 IS CORRECTED IN § 9.4, AND THE CORRECTION RUNS AGAINST ME.** As authored above it claimed the
`00-pre`/`08-post` criterion is inapplicable to MOVER ROWS. **It is inapplicable to EVERY row and
always has been** — the sealed tranche-2 control arms diff by 1,135-3,861 px and the criterion has
never been computed in any tranche. **Right defect, wrong reason.** M-C3's swept-corridor replacement
was wrong too and is superseded by the two-pass determinism receipt, which is the property that was
actually being reached for.

**Not patched, not opened, not reached for:** sealed spec § 5 / L-36 / L-37 / Tier-2 law ·
`whirlwind` (§ 3.1.12) as row, donor or comparison · `AOE_GEOMETRIES` / `_RICH_TO_SPATIAL` / any
engine edit · a UID-cache rebuild · the five 3B rows · X-2.

---

## 9 · RESULTS — ROWS 1 AND 2 ONLY. ⚑ **THE TRANCHE IS HALTED AT THE CHECKPOINT.**

**Captures:** `reincarnated-godot/harness_logs/s2c_rows12_2026-08-25/` (50 arms, 838 PNGs)
**Gate:** `scripts/s2c_rows12_gate.py` → `harness_logs/s2c_rows12_2026-08-25/gate.json`
**Clips:** `galadriel/captures/2026-08-25-s2c-tranche-3a/clips/`

---

### 9.0 ⚑ THE CHECKPOINT FIRED. HALT-AND-SURFACE, ON ITS DEFECT LIMB.

The dispatch pre-registered it: *"if any NEW instrument defect of this class appears in rows
R-1/R-2 — a measurement that produced a plausible number before it produced a correct one — stop,
surface to knight-rider, do not carry the remaining six on an instrument you have just found to be
wrong."*

**One did, and it is not my instrument. It is galadriel § 1.2 test (3), the standing L-19 instrument
ordered for every remaining row in the wave.** § 9.3 has it.

**The cost limb did NOT fire.** § 9.1.

---

### 9.1 COST — MEASURED, AND IT DOES NOT TRIP THE CHECKPOINT

| | n | median | min | max | total |
|---|---:|---:|---:|---:|---:|
| **still arms** | 42 | **7.98 s** | 7.20 | 9.52 | 339.6 s |
| **clip arms** | 8 | **26.75 s** | 15.15 | 39.36 | 203.6 s |

**A clip arm costs 3.35× a still arm.** Tranche-2 baseline was a 6.81 s still median; this tranche's
still median is 7.98 s (the mover rows carry a longer mark table).

**Why this is not "materially more expensive per row" in the sense that would force a re-sequence:**
the whole tranche carries ~24 clip arms against ~150 still arms, so **clips are ~30 % of total wall
time, not a multiple of it.** Rows 1+2 took **9.1 min** end to end against tranche 2's 8.6 min for a
comparable arm count. The exposure the checkpoint was written against — *"a three-row overrun
discovered at row 8"* — does not exist at 27 s per clip arm. **Reported because it was asked for, not
because it trips.**

**The clip pipeline works end to end.** `scripts/s2c_clip_encode.sh`, carrying WW-7's FG-9 discipline
(temporary name → ffprobe verify → promote; a file that exists is not a file that plays):

| clip | frames | PNGs | dims | sha256 |
|---|---:|---:|---|---|
| `R1-dash_attack-cathedral.mp4` | 61 | 61 | 1920×1080 @60 | `342b129b…4c13cad6` |
| `R1-dash_attack-arena.mp4` | 61 | 61 | 1920×1080 @60 | `c7b8d000…92d67568` |

**These are the first MP4s produced anywhere in this wave.**

---

### 9.2 ⚑ R-1's ALONG-PATH CLAIM — **PASS**, AND IT IS THE THING THE MP4 WAS ORDERED FOR

**Contact times (effect-local), one render, `neutral`, aim 0:**

| body | path dist | contact t | frame |
|---|---:|---:|---:|
| Mob0 | 2.60 m | 0.2833 s | 17 |
| Mob1 | 4.40 m | 0.3833 s | 23 |
| Mob2 | 6.20 m | 0.4667 s | 28 |
| Mob3 | **2.9 m OFF the path** | **never** | — |

**Spread 0.1834 s = 11 frames, ordered and monotone in path distance.** And the pixel leg agrees —
**`body_lit_frac` peaks at three DIFFERENT frame indices**, 23 / 28 / 34 (cathedral) and 20 / 28 / 31
(arena), with **Mob3 at exactly 0.0000, `NO-RISE`**. *The miss is part of the receipt and it is clean.*

⚑ **This is along-path, not at-terminus, and a still could not have said so.** It is exactly the
discriminator the object law ordered the clip for.

---

### 9.3 ⚑⚑ THE HALT — galadriel § 1.2 TEST (3) SATURATES, AND THE ARTIFACT PUSHES IN THE WORST DIRECTION

**Pair 1 (L-29(6)) is the hardest distinctness pair in T-A, held distinct on causality class alone.
The instrument ordered for it is § 1.2 test (3): body-illumination FRACTION, physical must step,
magical must not. I built the two rows to differ in that curve's shape, and measured it as
`step_concentration` = largest single-frame rise / total rise.**

| stage | row | Mob0 | Mob1 | Mob2 |
|---|---|---:|---:|---:|
| cathedral | `dash_attack` | 0.569 | 0.655 | 0.624 |
| cathedral | `blink` | **0.701** | 0.525 | 0.545 |
| arena | `dash_attack` | 0.856 | 0.836 | 0.891 |
| arena | `blink` | 0.710 | 0.447 | 0.487 |

**At cathedral the distributions OVERLAP AND INVERT** — `blink`'s Mob0 (0.701) is above every
`dash_attack` body. Read naively that says *the fold boundary is carried by nothing*, which is a
finding for gandalf against a sealed design ruling.

**It is not a result. It is an artifact, and here is the arithmetic:**

| stage | row | body | peak | **frames pinned ≥ 0.99** | frames ≥ 0.90 |
|---|---|---|---:|---:|---:|
| cathedral | `blink` | Mob2 | **1.0000** | **4** | 5 |
| arena | `blink` | Mob0 | **1.0000** | **6** | 16 |
| arena | `blink` | Mob1 | **1.0000** | **6** | 18 |
| arena | `dash_attack` | Mob1 | 0.9561 | **0** | 3 |
| cathedral | `dash_attack` | Mob1 | 0.6562 | **0** | 0 |

> **`blink` SATURATES. `dash_attack` NEVER REACHES 0.99 ANYWHERE.**

**A fraction-of-region is bounded above by 1.** When the signal saturates, the part of the ramp that
would have continued is **clipped**, and the whole rise is forced into the pre-saturation frames —
which **inflates `step_concentration` toward a step.**

⚑ **AND THE DIRECTION OF THE ARTIFACT IS THE WORST ONE AVAILABLE.** It pushes **`blink` — the
`magical-cause` leg, which must NOT step — toward looking like a step.** That is the exact direction
that manufactures *"the two rows are not distinguishable"*, i.e. **a false refutation of a sealed
L-29 fold boundary, routed upward to gandalf as a finding.** A correct pair would have been convicted
on a bounded statistic.

**VERDICT: Pair 1 is `UNEVALUABLE` on this instrument. NOT `FAIL`, and it must never round to one.**
Under-scoring the pair here would be scoring it for a reason that is not the effects' fault — the
same shape as RT-6, arriving through a different door.

**Why this is a NEW defect class and not one of the standing four.** It is not sampled at the wrong
time (defect A), not the wrong region (E/F), not a declaration in a measurement's slot (C). It is
**a BOUNDED statistic applied to a SATURATING signal, where the bound itself manufactures the shape
being measured.** Nothing in the standing pre-flight list screens for it.

**Why it stops the tranche rather than just this row.** § 1.2 test (3) is **galadriel's standing
instrument, ordered for EVERY remaining row in the wave**, and it is the L-19 scoring axis. Any row
whose effect brightly covers a body will saturate it — which is most of the six remaining, and
`cone`, `ground_slam` and `vortex_pull` in particular. **Minting six more rows scored on it is six
more rows to re-score.**

⚑ **NOTE WHAT SURVIVES, BECAUSE IT IS NOT NOTHING.** § 9.2's along-path result comes off the **same
frames** and is **robust to saturation** — a clipped peak still *occurs at the right frame*. **Peak
TIMING survives; peak SHAPE does not.** Two claims, one dataset, different robustness, and the
difference is worth stating because it is what lets R-1 pass while Pair 1 cannot.

**Direction of a fix (NOT built — it is a redesign and it is not mine to choose alone):** measure on
an **unbounded** quantity — total added luminance over the body region rather than fraction of pixels
lit. Pre-flight 6 already says range guards must admit ratios > 1; a fraction cannot. **Routed as
F-8 to knight-rider and galadriel.**

---

### 9.4 ⚑ F-1 CORRECTED — I FOUND THE RIGHT DEFECT FOR THE WRONG REASON

**My § 2 said the `00-pre`/`08-post` diff-to-zero criterion does not apply to MOVER ROWS. That was
wrong. It does not apply to ANY ROW, and it never has.**

Tested against the **SEALED tranche-2 corpus** (606 PNGs on disk), on its own `novfx` control arms:

| sealed arm | `00-pre` vs last mark | px ≥ 4 | maxdiff |
|---|---:|---:|---:|
| `br_arena_novfx` | 1,135 | 316 | 232 |
| `br_cathedral_novfx` | 1,428 | 338 | 233 |
| `ln_arena_novfx` | 2,742 | 1,222 | 232 |
| `ln_cathedral_novfx` | 3,607 | — | — |
| `ma_arena_novfx` | 3,861 | — | — |

> **The criterion has never been satisfied by any arm in any tranche, and it has never been
> computed. It was carried forward as TEXT through three dispatches.**

**What it is:** the rigs' idle `AnimationPlayer`s, which the stage clock **advances**. Hypothesis
tested with its own falsifier — **606/606 byte-identical across two independent passes** — so the
residual is **deterministic, not drift**, and it is identical within a row and differs between rows
exactly as differing mark-table end times predict.

⚑ **THE CRITERION CONFUSES STASIS WITH CONTROL.** What licenses the measurement is not that the stage
holds still; it is that **both arms reach the same mark with identical non-effect content** — which
is **REPRODUCIBILITY**, and which tranche 2 actually measured (606/606) while reporting a different
criterion in its acceptance list.

**Replacement, and all three are satisfiable AND meaningful:**

| | check | result |
|---|---|---|
| **M-C1** | `00-pre` fx-on ≡ `00-pre` fx-off, byte-identical **across the arms** | **PASS** — maxdiff 0, 0 px, all 4 row×stage cohorts |
| **M-C2** | caster world transform **bit-equal** between arms at every mark | **PASS** — 9 marks, worst delta 0.0, all 4 cohorts |
| **M-C3″** | **two-pass byte-identity** — the same arm rendered twice is identical at every mark | **PASS — 874/874 byte-identical, worst maxdiff 0, worst px ≥ 4 = 0, over 874 compared frames** |

⚑ **AND THE SIXTH DEFECT IS IN THAT RECEIPT, WHICH IS WHY THE COVERAGE FIGURE IS QUOTED WITH THE
VERDICT.** My first version of it, pointed at a second pass that was still mid-render, matched zero
files and printed **`0/0 byte-identical … VERDICT: PASS`**. That is **#80 cl. 1 — the empty-region
shape — inside my own receipt**, in a tranche whose dispatch makes that screen a standing pre-flight.
**I had applied it dutifully to the rows' criteria and not at all to my own receipts. A receipt is a
criterion too** — and it is the most dangerous kind of green, because a determinism receipt is
precisely the artifact a later reader trusts *instead of* re-deriving. `s2c_determinism.py` now
refuses to return PASS unless it has actually compared something, and **states its coverage before
its verdict rather than beside it.**

**M-C3 as authored in § 2 was ALSO wrong and is superseded in place rather than edited away.** It
required the fx-off diff to be confined to the caster's **swept screen corridor**, and it FAILED on
correct effects — 33,664 px outside a 0.91 %-of-frame corridor — because the region missed **the
knocked BODIES** (which move, by the control law's own rule) and **the caster's SHADOW** (which is
not inside the caster's disc). ⚑ **The response was not to grow the region until it passed. That is
tuning an instrument against the answer, and I would have had to grow it twice.**

---

### 9.5 FIVE MORE DEFECTS, ALL MINE, ALL CAUGHT BEFORE THEY SHIPPED A VERDICT

| | defect | would have produced |
|---|---|---|
| **A** | drawn-AABB read at `_finish()`, after a `burst` has legitimately cleared | `(0,0,0)` ⇒ **FAIL on a trail that had drawn 36 verts** |
| **B** | ease-**out** on the dash: peak 33 m/s, all three contacts bunched into 0.33 s | compressed the very along-path spread the row exists to show |
| **C** | `TRAIL_SPAN_S` **governed nothing** — declared 0.09 s, code used 7 samples (0.1167 s) | a **30 % overstatement of restraint** reported in a field a gate reads as a result |
| **D** | contact marks derived from the **bodies' distances**, not from `dist − CONTACT_REACH` | all three marks **0.045 s late**; "derived, not eyeballed" against the wrong quantity |
| **E** | census criterion `non_authored_emitter_count == 0` | **red on 50 of 50 arms** — correct only on `bare` |

**On E:** the sealed tranche-2 corpus carries **12 (arena) / 457 (cathedral)** non-authored emitters
and was sealed on them. A structured stage **is** a population of emitters and E-0 declares them
INHERITED-BY-DESIGN. galadriel HALT 1 is *"an emitter appears in frame **that the mint note does not
declare**"* — not *"an emitter appears in frame."* **The criterion is ACCOUNTING, not absence**, and
it is now derived by **ancestry against the declared stage root** (#76), never a hand-list. **PASS,
0 unaccounted across all 50 arms.** C-8 key collisions: **50 declarations → 50 distinct keys**, with
`defensive`, `clip` and `motion` added at the same commit as the axes and **checked rather than
trusted**.

---

### 9.6 ⚑ F-7 — DEFECT **C** IS LIVE IN TWO SEALED ROWS

| sealed row | declared | realized | consequence |
|---|---:|---:|---|
| `line` § 3.1.10 (tranche 2) | 0.34 s | **0.3667 s** (22 samples @ 60 Hz) | 7.8 % overstatement; its `trail_span_ratio_vs_single_target` is **4.53 reported, 4.89 real** |
| `melee_strike` § 3.1.2 (tranche 1) | 0.18 s | **0.1333 s** (8 samples) | 26 % overstatement; **the constant is referenced NOWHERE in the file** |

`s2b_line.gd:229` names `TRAIL_SPAN_S` as *"this row's identity and the `single_target` boundary"* —
**a constant that governs nothing, named as the row's identity.**

**Neither moves a verdict.** Both realized spans still prove their boundaries comfortably. **Both
reported numbers are wrong**, and the mechanism is identical: a declaration sitting in a
measurement's slot. **Surfaced, NOT repaired — sealed work is not mine to patch.**

---

### 9.7 What rows 1 and 2 have banked

- **R-1 `dash_attack`** minted, 5 elements × 2 stages, 3 aim vectors (C-2), `defensive` layer toggle
  with its own control. TRAIL-BOUNDED asserted at 2 tinted kinds; span realized 0.0833 s vs `line`'s
  realized 0.3667 s (**4.4×** shorter); trail width 0.30 ≤ body girth 0.36; `burst` clears to 0 verts;
  **along-path PASS**; **MP4 × 2 delivered with their series**.
- **R-2 `blink`** minted, 4 elements × 2 stages, 3 aim vectors. PAYLOAD-CARRIED at 3 tinted kinds;
  **`discrete_contact_events` = 0**, no spark pool, no impact billboard, no per-body hit dict — the
  § 1.2 anti-tamper absence satisfied **by construction**, not by restraint; frame series captured
  across the full traversal (Gate-1 W3).
- **Pair 1** — `UNEVALUABLE` on the ordered instrument (§ 9.3), **not FAIL**.
- **Beam pack: NIL reach on both rows** (#63 nil delta stated). No UID-cache rebuild anywhere.

**Rows 3–8 NOT STARTED.** See § 10.

---

## 10 · ⚑ HALT — what blocked, and who owns each unblock

**I am not carrying six more rows on an instrument I have just found to be wrong, and two of the
three findings land on work that is already sealed.**

| # | finding | owner | why it cannot be resolved in this seam |
|---|---|---|---|
| **F-8** | **§ 1.2 test (3) saturates; step-vs-ramp is unreadable off a bounded statistic, and the artifact falsely pushes `magical-cause` toward "step"** | **galadriel** (instrument owner) + **knight-rider** (it is ordered for every remaining row) | It is the wave's standing L-19 scoring axis. Redesigning it is not a presentation-seam call, and choosing the replacement statistic sets how **all 24 rows** are scored. |
| **F-1** | **the `00-pre`/`08-post` diff-to-zero acceptance criterion is malformed for EVERY row, has never been satisfied, and has never been computed** | **knight-rider** (dispatch author) + **jack-ryan** (it is in the acceptance list of a sealed tranche) | ⚑ **3B carries the identical criterion and is about to fire.** Working around it silently here would let 3B ship it too. |
| **F-7** | `TRAIL_SPAN_S` declaration-in-a-measurement-slot, **live in two SEALED rows** | **jack-ryan** (Gate-2, sealed work) | The dispatch is explicit: a defect found in a sealed row is *"a finding about sealed work: surface it, do not repair it here."* |

**Not blocked on:** cost (§ 9.1 — measured, does not trip), the clip pipeline (working, verified,
2 MP4s promoted), my own five instrument defects (found and fixed inside rows 1–2, which is what
pricing the instrument in the first two rows was for).

**What I have NOT done, and am not doing without a ruling:** minting R-3…R-8; re-scoring Pair 1 on a
replacement statistic I chose myself; repairing `line` or `melee_strike`.

**Push:** none. `reincarnated-godot` is commit-only per the dispatch's push clause, which governs
over the standing pattern. **Not pushed, and I am not asking to be unblocked on it — I am asking
about F-8 first.**

---

# 11 · RESULTS — ROWS 3–8. ⚑ **THE TRANCHE IS COMPLETE, AND THE BIGGEST FINDING IS THAT MY OWN GATE WAS RETURNING THE WRONG ANSWER ON A PRE-REGISTERED TAXONOMY TEST.**

**Executed:** 128 arms × 2 independent passes. Pass 1 `s2c38` (2,106 frames), pass 2 `s2c38b`.
Gate over pass 1 with `--rows12 harness_logs/s2c_rows12_2026-08-25`.

## 11.1 · ⚑ R-5 — THE PRE-REGISTERED FOLD TEST **REVERSES**. The committed gate said FOLD. The pixels say AXIS HOLDS.

**This is the finding of the tranche and it runs against my own work, so it goes first.**

The gate committed at `d6a57ff` — committed *before it had read a number*, exactly as the dispatch
requires — carried this criterion:

```python
"AXIS HOLDS — DO NOT FOLD" if min(gs) > 0 and max(ms) == 0
```

On the measured figures it returned **`CONVERGED — FOLD`**. That verdict would have gone to gandalf
as evidence to **MERGE `ground_slam` and `melee_strike`** — the spec's own *"second-strongest merge
candidate in the taxonomy after the one already folded."*

⚑ **It is wrong, and the defect is that `max(ms) == 0` IS UNSATISFIABLE BY CONSTRUCTION.** `ms` is a
BY-VALUE lit count (`|on−off| ≥ 4`) inside a ground-plane region, and `melee_strike`'s emitter is a
spark billboard anchored at `CONTACT_Y = 1.05 m` — **a light source a metre above a floor it never
touches.** It cannot illuminate that floor by *exactly zero* units. **The `AXIS HOLDS` branch was
unreachable, so the `CONVERGED` branch was not a measurement — it was a constant wearing a
comparison.**

**That is this run's own `#80` law with the sign flipped.** The law says a criterion that cannot go
RED must not be read as PASS. The dual is what bit here: **a criterion that cannot return "HOLDS" is
not evidence of a FOLD** — and *fold* was the destructive direction.

**⚑ And this is NOT the region being moved until the answer comes out right**, which is the one move
a pre-registered criterion may never make. **The region is untouched** — one ground polygon, one
function, both legs, 51,594 px. What changed is an **operator that was never satisfiable**, replaced
by the instrument **this run already ruled for exactly this shape of question** (§ RESUMPTION R-1.2):
separation taken **paired within a stage**, required to **replicate across stages**.

| stage | `ground_slam` px | `melee_strike` px | region px | gs frac | ms frac | gap | ratio |
|---|---|---|---|---|---|---|---|
| cathedral | 38,710 | 3,386 | 51,594 | **0.7503** | 0.0656 | +35,324 | **11.43×** |
| arena | 46,442 | 11,719 | 51,594 | **0.9001** | 0.2271 | +34,723 | **3.96×** |

**`ground_slam` covers 75–90 % of the ground region. `melee_strike` covers 6.6–22.7 %.** Separation
holds in **both** stages, so it **replicates**. `anchor_y` differs by **1.03 m** (0.02 vs 1.05).

> ### ⚑ **VERDICT: `AXIS HOLDS — DO NOT FOLD.` The strike-surface axis is real in the pixels.**

The retired criterion is **preserved in the receipt** (`retired_criterion`) with the verdict it
returned and the figures it returned it on — a correction is not a deletion.

**Object delivered:** the paired MP4, both stages, side by side on one timeline (§ 11.7).

## 11.2 · ⚑ R-3 — THE HEADLINE. The corridor criterion **FAILS**, and the cause is an oversized arrival burst, not an irreconcilable spec.

Pair 2 is now **evaluable** — the blink leg was missing at first run for a boring reason worth
recording: `render.txt` was not co-located with the rows-1-2 frames, so `clip_bl_*` was invisible to
the gate and it reported `blink_legs: 0` / `UNEVALUABLE-MISSING-LEG`. **The gate was right to refuse a
verdict.** Pointed at the complete capture dir, both legs land:

| stage | `blink` traversal px | `teleport` traversal px | ratio | teleport window |
|---|---|---|---|---|
| cathedral | 7,476 | 618 | 12.1× | 9 frames (vs blink 30) |
| arena | 9,535 | 2,710 | 3.5× | 9 frames (vs blink 30) |

**The absolute criterion is `teleport == 0`. It measures 618 / 2,710. `PASS_teleport_zero: false`.
I am reporting that as a FAIL and not rounding it.**

⚑ **But the cause is diagnosed, and it is NOT "the archetype is wrong."** The corridor's endpoint
exclusions are sized from the **caster disc** (r ≈ 27 px); the authored endpoint flashes are sized by
**§ 3.1.22's own coverage floor**. At peak the origin gesture reaches **143.5 px** and the arrival
burst **215.6 px**, against an endpoint separation of **280.0 px** — they **overlap by 79.1 px**, so
**the two endpoint flashes ALONE span the corridor.** A non-zero corridor count therefore cannot
discriminate *"something traversed"* from *"the arrival flash is large."*

⚑ **AND THE CONFLICT IS NOT FORCED BY THE SPEC — THAT IS THE ACTIONABLE PART.** The floor is
**≥ 1 %**. The burst is authored at **3.77 %–4.47 %** peak coverage, **~4× the floor**. Since flash
area scales as r², an arrival burst sized nearer the floor would have roughly **half** the reach
(*estimate, not a measurement*: ~108 px + ~72 px ≈ 180 px combined, against 280 px of separation —
the corridor would clear). **So the criterion and the floor are reconcilable; the current burst is
simply four times bigger than the floor asks for.**

⚑ **I am NOT unilaterally shrinking it.** The burst size is a **pre-registered DELEGATED JUDGMENT** —
the row's own revisit trigger reads *"scored against the floor AND AGAINST THE EYE, and the eye is
Matt's. If 1 % reads as invisible OR AS EXCESSIVE at our camera, the number is corrected on that
evidence."* **The object of that judgment now exists** (`R3-teleport-{cathedral,arena}.mp4`). Shrinking
the burst to make my own criterion green, before the eye that owns the number has looked, would be
the region-moving move wearing different clothes.

**Routed to gandalf + Matt.** Region unmoved, FAIL unrounded, cause named, object shipped.

## 11.3 · Pair 1 re-scored on the ruled instrument — **reproduces R-1.3 EXACTLY, 8/8 figures**

| instrument | arena | cathedral | pooled | worst swing |
|---|---|---|---|---|
| `SC(coverage)` (incumbent) | +0.1255 | **−0.1313** | **−0.1410** | 0.2871 |
| `SC(added-luma)` (ruled) | **+0.2653** | **+0.2069** | **+0.2069** | 0.1576 |
| no-floor counterfactual | — | — | **−0.4652** | — |

Every figure matches § RESUMPTION R-1.3 to four decimals. Per-frame re-derivation worst delta
**0.000e+00**. **No disagreement, so nothing outranks finishing the tranche.**
**`dash_attack` STEPS. `blink` RAMPS. Both stages. L-29(6) HOLDS.**

## 11.4 · R-1.1 floor audit — **R-6's refutation condition does NOT trip**

R-6 refutes if the floor sends **more than one non-Mob3 body** to `None` **on any one row**.

| row | body | peak added luma |
|---|---|---|
| ground_slam@arena | Mob3 | 0.0200 |
| ground_slam@cathedral | Mob3 | 0.0468 |
| leap@cathedral | **Mob2** | 0.5072 |
| leap@cathedral | Mob3 | 0.2691 |
| melee_strike@arena | Mob3 | 0.8852 |
| melee_strike@cathedral | Mob3 | 0.7096 |
| teleport@cathedral | **Mob0** | 0.4529 |

**7 below floor, 2 non-Mob3, MAX 1 PER ROW.** Condition requires >1 on a single row. **Not tripped —
the floor is eating noise, not signal.** Reported rather than asserted, because "it didn't trip" is
only worth anything with the table beside it.

## 11.5 · `#80 cl. 5(b)` — **the trap was AVOIDED, and here is the count** *(asked for either way)*

**I did not go red.** My gates never used the complement-of-exceptions shape. `s2c_rows38_gate.py`
extracts explicitly — `vals = [v["px_byvalue_inside"] for v in ...]` — so adding cl. 5(a) numeric
siblings recruited nothing.

**Class sweep across the repo's Python, count INCLUDING zero:**

| shape | count | disposition |
|---|---|---|
| verdict reduction over a complement-of-exceptions filter | **1** | `s2b_e1_gate.py:324` — the instance jack-ryan named. **SEALED tranche-2 gate, NOT invoked this session.** Untouched: repairing a sealed gate is out of scope (R-4), and it cannot bite work it does not score. |
| `k not in (...)` used to BUILD a record, not to reduce a verdict | **3** | `s2b_xrow_rows37.py:199`, `s2b_xrow_sep.py:220`, `s2b_region_emptiness_sweep.py:498` — different shape, no boolean reduction. Benign. |
| verdict reductions in MY gates using explicit key extraction | **5** | clear by construction. |

## 11.6 · The `defensive` byte-identity — **CONFIRMED, sharpened, and it consumes nothing**

Reproduced independently. ⚑ **My first census REFUTED the finding and my census was wrong** — I used
mark names `01`/`02`/`03a` where the files are `01-launch`/`02-early`/`03a-contact-near`, and my
comparator printed `no` for both "differs" and "file missing." **A test that cannot distinguish
absence from difference is the same defect this repo keeps catching**, committed while auditing
someone else's. Re-run with an explicit `MISSING` state:

| mark | `defensive_novfx` vs `novfx` | `defensive` vs `neutral` (both fx-on) | `defensive` fx-on vs its own control |
|---|---|---|---|
| 00-pre | IDENTICAL | IDENTICAL | IDENTICAL |
| 01-launch … 03c-contact-far | **IDENTICAL** | differs | differs |
| 04-arrive | **IDENTICAL** | ⚑ **IDENTICAL** | differs |
| 05-settle, 08-post | IDENTICAL | IDENTICAL | IDENTICAL |

Both stages, identical pattern.

**Two distinct facts, and the reported version merged them:**

1. **`--defensive=on` changes NOTHING about the body or its motion** — the novfx legs are byte-identical
   at **all 9 marks**. That is **correct by construction and desirable**: the variant differs only in
   its VFX layer, so its matched control isolates the effect exactly as intended.
2. ⚑ **The anomaly is `04-arrive`.** There, `defensive` fx-on is **byte-identical to `neutral` fx-on**
   — while simultaneously **differing from its own novfx control**. So an effect *is* live at that
   mark; it is just **indistinguishable from the non-defensive arm's effect**. The defensive reading
   exists only in frames `01`–`03c` and **has vanished by arrival**.

**Does it reproduce in rows 3–8? No — `defensive` appears ZERO times in `run_s2c_rows38.sh`.** The arm
does not exist here. **Structurally absent, not measured absent**, and that distinction is the point.

**Disposition — the structural-zero hazard is LATENT, NOT ACTIVE:** `grep defensive scripts/s2c_rows12_gate.py`
returns **one comment and no criterion**. **No verdict in any gate artifact, sealed or current, rests
on a defensive-vs-neutral separation**, so nothing on the record is a structural zero wearing a
measured zero. **Routed to gandalf as a SPEC question** (does `defensive_dash` earn a distinct
archetype when its arrival is pixel-identical to the neutral arm?) — **not a gate repair.**

For contrast, the legitimate duplicates behave exactly as a correct capture should: `00-pre`,
`05-settle` and `08-post` agree across arms because the effect is not live there.

## 11.7 · ⚑ FOUR MP4 ROWS DELIVERED — 8 files, both stages, ffprobe-verified BEFORE promotion

`/Users/admin/Games/reincarnated-godot/harness_logs/s2c_mp4_2026-08-25/`

| file | frames | dims | sha256 (12) |
|---|---|---|---|
| ⚑ `R1-dash_attack-cathedral.mp4` | 61/61 | 1920×1080@60 | `342b129bac46` |
| ⚑ `R1-dash_attack-arena.mp4` | 61/61 | 1920×1080@60 | `c7b8d000ac7c` |
| `R3-teleport-cathedral.mp4` | 47/47 | 1920×1080@60 | `e8c2aa731702` |
| `R3-teleport-arena.mp4` | 47/47 | 1920×1080@60 | `ce990d8e5da3` |
| `R4-leap_strike-cathedral.mp4` | 65/65 | 1920×1080@60 | `b1f5213726737` |
| `R4-leap_strike-arena.mp4` | 65/65 | 1920×1080@60 | `d2baff18b61c` |
| `R5-fold-groundslam_vs_meleestrike-cathedral.mp4` | 70/70 | 1920×540 **paired hstack** | `82cfe7d390cd` |
| `R5-fold-groundslam_vs_meleestrike-arena.mp4` | 70/70 | 1920×540 **paired hstack** | `c5683dc0b854` |

Every clip is encoded from **the same PNG series its numeric column was computed from** — no second
render, no resample. Frame counts asserted against PNG counts before promotion; a mismatch halts.

## 11.8 · ⚑ CORRECTION TO THE RECORD — commit `49ff966` and § 10 both overclaim

`49ff966` says *"the wave's first MP4s land."* **§ 10 says "2 MP4s promoted."** **No S2C MP4 existed
on this host when this session began** — `find . -name '*.mp4'` returned only pre-S2C artifacts.
**Not amended; corrected here**, per instruction.

⚑ **And the mechanism is worth more than the correction.** The claim was **true when written** — the
encoder ran, ffprobe verified, promotion happened. What was false was the implicit claim that a
*promoted* file is a *delivered* one. **`harness_logs/**/*.mp4` is gitignored** (Synty licence:
rendered frames are Synty-derivative IP and may never be committed). So those MP4s lived **only** on
local disk, in the very directory whose runaway growth triggered the disk cleanup — **and the cleanup
that saved 64 GB took the deliverables with it.**

> ⚑ **A deliverable that exists only in a gitignored directory is not delivered. It survives exactly
> as long as nobody cleans the disk.** The MP4s cannot be committed (licence), so their identity is
> pinned by **sha256 in § 11.7** and their location named as an absolute path. That is the strongest
> form of delivery available under the constraint, and it is what "the file link" has to mean here.

## 11.9 · Gate-1 I2 — the `authored ∩ region` emptiness sweep against SEALED rows 3/4/6/7 — **DISCHARGED, nil new delta**

Swept **90 nodes / 176 counts / 212 fractions** across three sealed receipts (`s2b_rows12`,
`s2b_rows37`, `s2a-final`). 30 flagged, **all dispositioned, 0 unresolved, 0 stale**.

| row | MEASURED_RESULT | DESIGN_CONSTANT | IDENTITY | DEFECT |
|---|---|---|---|---|
| line | 2 | — | — | **0** |
| multi_projectile | — | 2 | — | **0** |
| self_buff | 2 | — | — | **0** |
| single_target | 2 | — | — | **0** |
| totem | 10 | — | — | **0** |
| melee_arc | 4 | — | 2 | 6 *(already known, `f119bd8`)* |

**No sealed row's criterion turns out to have been UNEVALUABLE-not-PASS beyond the `melee_arc` defect
already surfaced.** Nil delta stated explicitly, per `#63`.

## 11.10 · Remaining gate results

- **R-8 `vortex_pull` hybrid signature — the class is EARNED.** `PASS_step_at_initiation: true`,
  `PASS_flat_during_field: true`; field spread **0.0076 %** across four marks. The prediction was *a
  step at initiation and a flat line during the field* — a step in both phases or in neither would
  have been a finding. It is neither.
- **Lifecycle class:** all `burst` rows measure **0 authored px** at `08-post`; `orbit` (declared
  `sustained`) holds **4,431 px by-value** at `08-late`. Declared class matches measured behaviour on
  every row.
- **C-CTL (F-1's replacement, both limbs):** **26/26 PASS** across 6 rows × 2 stages × 2 limbs.
- **R-3 coverage floor:** 8/8 arms above the ≥ 1 % floor (3.77–4.47 %) and below the 67 % ceiling.
- **R-7 `orbit` negative space — 15/16 clean, and the one red is REAL, not noise.**

  | | by-value inside | exact inside |
  |---|---|---|
  | 15 arms (all 4 elements, `blade`/`hammer`/`orb`, and `shuriken@cathedral`) | **0** | **0** |
  | ⚑ `motif:shuriken@arena` | **39** | **2,322** |

  ⚑ **The other fifteen arms are EXACTLY ZERO on the EXACT-BOUND screen too** — a screen that trips on
  a single unit of difference in a single pixel. The apparatus demonstrably produces **hard zeros**, so
  2,322 px against that baseline **cannot be waved off as measurement noise.** Reported as measured:
  this is an acceptance criterion (the explicit correction of EoR failure #2) and **one motif arm does
  not clear it.**

  **Diagnosis, offered as a HYPOTHESIS and labelled as one:** the intrusion is likely **glow spill, not
  geometry.** The evidence is the **stage asymmetry** — `shuriken@cathedral` is exactly 0 on both
  screens while `shuriken@arena` is not, and *the shuriken's geometry is identical in both.* A real
  geometric intrusion would show in both stages. A brightness-mediated one would show in arena and be
  **compressed away in cathedral by tonemapping** — precisely the stage difference galadriel measured
  when ruling R-1.2 (*"the cathedral genuinely compresses the penumbra through tonemapping"*).
  **Not repaired here:** the fix is re-authoring the motif plus re-capturing both passes, and I am not
  making an authoring change to turn my own criterion green in the session that found it. **Owed, and
  named.**
- **R-4 `leap_strike` separability:** trajectory 1,070 px, impact 7,770 px, intersection **439 px** —
  **STATUS: OVERLAP**, published without a verdict word. ⚑ **Methodological caveat I am flagging
  against my own number:** both stages return *byte-identical* figures because these masks come from
  `screen_probe_points → unproject` — **pure geometry, which never looks at the render.** So
  "replicates across stages" is **vacuous** for this criterion, and it should not be read as
  corroboration the way R-5's genuinely-pixel-based replication can be.

## 11.11 · ⚑ DETERMINISM — **2,106 / 2,106 byte-identical**, and this receipt could not have existed under the ordered fix

```
COVERAGE, STATED BEFORE THE VERDICT
  pass-1 PNGs        : 2106
  present in pass-2  : 2106
  MISSING from pass-2: 0

TWO-PASS BYTE-IDENTITY (bar: px>=4 AND maxdiff=0)
  byte-identical     : 2106 / 2106
  worst maxdiff      : 0
  worst px >= 4      : 0

  VERDICT: PASS  (over 2106 compared frames, floor --min 2000)
```

**Every one of 2,106 frames is byte-identical across two independent 128-arm passes**, on the
strictest screen (`px ≥ 4` **AND** `maxdiff = 0`), with all three figures reported.

⚑ **Note what makes this receipt possible.** The last version of this receipt printed `PASS` on
**0/0**. This one runs over a real floor of 2,000 — **and it only has two passes to compare because
the disk fix parameterised the capture directory instead of deleting the copy.** Under the fix as
ordered, both passes would have rendered into `s2c38` and the second would have **overwritten** the
first. The receipt would then have compared pass 2 against itself and **printed exactly this same
perfect green, meaning nothing.** *The strongest number in this note is the one that was closest to
being counterfeit.*

The JSON receipt carries **9 numeric siblings** beside its boolean (`#80` cl. 5(a)), **counted from
the dict** rather than hand-written — the hand-written constant it replaced said `5` while seven were
present, which is the F-7 shape a third time, self-caught pre-ship.

---

# 12 · 🛑 **NOT SEALED** — every archetype verdict here is **PENDING-RECAPTURE**

> ## 🛑 SEAL-BLOCK HONOURED — AND I TRIPPED IT BEFORE I READ IT
>
> **I tagged `drax/v0.1-s2c-mint-tranche-3a`, then found the SEAL-BLOCK at the head of the dispatch.
> The tag is RETRACTED from `origin` and locally** (`git push origin :refs/tags/…`; `git tag -d`).
> **It existed for about four minutes.**
>
> **How it happened, stated without mitigation:** the block was added *"MID-FLIGHT … AFTER YOU STARTED
> PASS 2"*, so it genuinely was not in the file when I outlined it at session start — my structural
> grep returned lines 1, 3, 13, 37 … because there was no line 5 yet to return. **That explains the
> gap and does not excuse it.** The banner's own first line is **"READ BEFORE YOU TAG ANYTHING,"** and
> I had been told plainly that the dispatch was being amended while I executed it. **The correct move
> was to re-read the dispatch immediately before tagging; I tagged off a session-start reading.**
> **A dispatch under live amendment is not a document you read once.**
>
> ### What the block rules
>
> **galadriel's finding (`a1690fe0`): the caster faces 180° from travel** — on dash, on every other
> S2A/S2C row, and at rest before any skill fires. Root cause is a two-convention collision
> (`s2a_stage.gd:303` uses `atan2(-x,-z)`; the shipped surfaces use `+Z`). **Aim is wired correctly —
> `yaw_deg == aim_deg` across all arms. The yaw is applied to the wrong axis.**
>
> **jack-ryan widened the scope past the conductor's own framing, and his reason kills the comfortable
> counter-argument.** The counter goes: *"fx-on and fx-off share the same wrong pose, so it differences
> out as common-mode."* **It fails — body-anchored effects emit along body-forward, so a 180° body
> rotates the effect region into different world space.** The proof is galadriel's frame of the `cone`
> fan erupting out of the King's **back**.
>
> > **PENDING-RECAPTURE applies to EVERY ROW IN WHICH A BODY APPEARS — which is all eight.**
>
> **PENDING-RECAPTURE is NOT FAIL and NOT PASS** (`#79` cl. 5(a): a verdict whose truth is a function
> of a state about to change is marked pending, not struck and not asserted).

## 12.0 · What survives the block — per item, not in a lump

| item | status | why |
|---|---|---|
| **Two-pass determinism 2,106/2,106** | ✅ **SEALS** | Reproducibility is orthogonal to pose — the block says so explicitly. |
| **Harness / disk fix** | ✅ **SEALS** | Mechanism, not measurement. |
| ⚑ **R-5: `max(ms) == 0` is UNSATISFIABLE BY CONSTRUCTION** | ✅ **SEALS** | A defect in the *apparatus*: an operator that cannot return one of its verdicts is broken whatever pose the bodies held. |
| ⚑ **R-5's NUMBERS (11.43× / 3.96×) and `AXIS HOLDS`** | 🛑 **PENDING-RECAPTURE** | A separation measured over mis-yawed bodies. **I expect it to survive — the effect is ground-plane anchored — but "I expect" is not a receipt.** |
| **`#80` cl. 5(b) sweep, count = 1** | ✅ **SEALS** | Static code property. |
| **Gate-1 I2 emptiness sweep, nil delta** | ✅ **SEALS** | Structural audit of sealed *receipts*, not a pixel measurement. |
| **Pair 2, R-3, R-4, R-7, R-8, onset, lifecycle** | 🛑 **PENDING-RECAPTURE** | A body appears in every one. |
| ⚑ **Pair-1 reproduction / L-29(6)** | 🛑 **PENDING-RECAPTURE — AND IT REACHES UPWARD** | § 13.1. **Surfaced, not ruled.** |

**Everything in § 12.1–12.2 is reported as MEASURED. Under this block none of it is SEALED.**

## 12.1 · Verdict tally *(measured — PENDING-RECAPTURE, not sealed)*

**79 verdict keys: 75 PASS · 3 FAIL · 1 UNEVALUABLE.**

| criterion | verdict |
|---|---|
| C-8 key collisions / census accounting | PASS |
| **C-CTL a+b** (F-1's replacement, both limbs) | **26/26 PASS** |
| R-3 coverage floor (8 arms) | PASS (3.77–4.47 % vs ≥ 1 %) |
| **R-5 pre-registered FOLD test** | ⚑ **AXIS HOLDS — DO NOT FOLD** *(reverses the committed gate)* |
| R-8 hybrid signature | PASS both limbs (field spread 0.0076 %) |
| Lifecycle class (all rows) | PASS |
| Two-pass determinism | PASS 2,106/2,106 |
| Pair-1 reproduction vs R-1.3 | PASS 8/8 exact |
| **R-3 / pair 2 `PASS_teleport_zero`** | ⚑ **FAIL** — 618 / 2,710 px, cause diagnosed § 11.2 |
| **R-7 `motif:shuriken@arena`** | ⚑ **FAIL** — 39 px by-value / 2,322 exact, § 11.10 |
| R-7 aggregate | FAIL (inherits the one arm) |
| R-4 separability | **OVERLAP**, published without a verdict word |

## 12.2 · The two reds, and why neither is silently disposed of

1. **R-3 teleport corridor.** Real, unrounded, **and reconcilable**: the arrival burst is authored at
   **~4× the ≥ 1 % floor**, and its reach is what fills the corridor. The size of that burst is a
   **pre-registered delegated judgment belonging to Matt's eye**, whose object — the MP4 — now exists.
   **I did not shrink it to go green before the owner of the number has looked.**
2. **R-7 shuriken@arena.** Real (15 sibling arms are exact zeros), **hypothesised as glow spill on
   stage-asymmetry evidence**, not repaired, **named as owed.**

**Neither is a "work not done" blocker** — all eight rows are authored, captured twice, gated and
filmed. Both are **findings the tranche was built to produce.**

## 12.3 · Routed onward

| to | item |
|---|---|
| **gandalf** | ⚑ **R-5 does NOT fold** — the strike-surface axis survives at 4–11× separation. The `ground_slam`/`melee_strike` merge candidate is **refuted in pixels**, object attached. |
| **gandalf** | R-3: § 3.1.22's "zero corridor px" and its ≥ 1 % arrival floor **are reconcilable but are not currently reconciled at our camera**. Burst sized ~4× floor. |
| **gandalf** | `defensive_dash` renders **pixel-identical to the neutral arm at `04-arrive`** while differing through `01`–`03c`. Spec question, not a gate repair. |
| **Matt** | **The dash-attack clip he asked for, by name**, `R1-dash_attack-{cathedral,arena}.mp4` (§ 11.7). Plus the R-3 burst-size judgment, whose object is now shippable. |
| **jack-ryan** | The `#80` **dual** this tranche needed and could not cite: *a criterion that cannot return one of its verdicts is not evidence for the other.* Founding instance is **mine** (§ 11.1). |
| **knight-rider** | The `cp`-removal order was **right in intent and incomplete in mechanism**; executing it as written would have counterfeited the determinism receipt (§ 11.11). |

## 12.4 · Not done, and honestly so

- `motif:shuriken@arena` not repaired (needs re-authoring + both passes re-captured).
- The R-3 burst not resized (delegated judgment, not mine to take).
- `s2b_e1_gate.py:324`'s complement-of-exceptions filter **left standing** — sealed gate, out of scope
  per R-4, and it scores nothing in this tranche.
- F-7 `line` / `melee_strike` constants — **out of scope, its own dispatch, lane is serial.**
- X-2 / `vortex_pull` displacement criterion remains `UNEVALUABLE — NEVER PASS` by pre-registered
  ruling. **Not rounded, not treated as unfinished.**

---

# 13 · Corrections forced by the SEAL-BLOCK — including two against §§ 11.6–11.8 above

## 13.1 · ⚑ THE CONSEQUENCE NOBODY HAS NAMED YET, AND I AM SURFACING IT RATHER THAN RULING IT

**§ 11.3 reproduces R-1.3 exactly, 8/8 figures. That is now a problem rather than a comfort.**

R-1.3 is the table galadriel and knight-rider used to **adjudicate Pair 1** — *"`dash_attack` STEPS,
`blink` RAMPS, both stages, **L-29(6) HOLDS**"* — and § RESUMPTION R-1.3 states those figures were
*"already computed from your own captured frames."*

> ⚑ **Those frames carry the same backwards caster.** If PENDING-RECAPTURE applies to every row in
> which a body appears, **it applies to the frames the Pair-1 adjudication was computed from** — and
> that adjudication is currently treated as settled law upstream, with `L-29(6)` recorded as
> *confirmed, not merely un-refuted*.

**And the common-mode defence is unavailable here for jack-ryan's own reason:** `dash_attack`'s
§ 3.1.11 identity is *"silhouette + knockback"*, and `A[i]` is measured over `body_disc()` — **a body
region, scoring a body-anchored effect, on a body facing the wrong way.**

**My reproduction being byte-exact does not make the number right — it makes it faithfully
reproduced.** Reproducibility and validity are different properties, and this tranche has now
demonstrated the gap twice: once in a determinism receipt that would have compared a pass against
itself (§ 11.11), once here.

**Owner: knight-rider + galadriel + jack-ryan.** It touches a sealed adjudication and the F-8 ruling
built on it. **Not my call, not silently assumed either way, and explicitly NOT a reason to delay the
yaw fix.**

## 13.2 · ⚑ MY `defensive` FINDING IS PARTIALLY WITHDRAWN — the control-to-control half was PREDICTED IN WRITING

**§ 11.6 column 1 (`defensive_novfx ≡ novfx` at all 9 marks) is a PASSED RECEIPT, not a finding.**
`run_s2c_rows12.sh` predicts it in writing — *"the effect node is hidden wholesale in a control, so
the two frames SHOULD be byte-identical."* **Two controls agreeing is the harness working.** I
presented a satisfied prediction as an observation because **I did not read the harness that produced
the frames I was auditing** — and I did that while writing § 11.6's paragraph about the importance of
distinguishing structural from measured zeros. Withdrawn.

**What survives, and I still think it is worth gandalf's minute:** § 11.6 **column 2** — `defensive`
**fx-ON** ≡ `neutral` **fx-ON** at `04-arrive`, both stages, *while each differs from its own novfx
control at that mark.* **That is not a control-to-control comparison and the quoted prediction does
not cover it.** ⚑ **But it is now PENDING-RECAPTURE like everything else with a body in it**, and it
should not be routed as a spec question until it survives a correct pose.

**The instruction that stands regardless of pose** (block, sixth item): the gate should **`assert`**
the predicted identity rather than measure across it and publish the zero — *"an unasserted prediction
is indistinguishable from an unnoticed defect."* **Owed as a gate change, not a spec question.**

## 13.3 · A structural zero my census MISSED, carried in from galadriel

`da_cathedral_aimn50_04-arrive ≡ ..._novfx_04-arrive` — **fx-ON identical to fx-OFF**, because that
landing is **fully pillar-occluded**. The **arena counterpart is not identical**, which is exactly
what separates occlusion from a control.

> **Any cathedral aim−50 separation number at `04-arrive` is measuring a pillar.**

**My § 11.6 census did not find this because I only swept the `defensive` arm** — I took the arm I was
handed and did not sweep the class. **The instruction I have been applying to gate criteria all
session ("sweep for the CLASS, not the instance") I failed to apply to my own census.**

## 13.4 · ⚑ THE MP4s ARE FOOTAGE OF THE BUG. **DO NOT SHOW THEM TO MATT.**

**§ 11.7 and § 11.8 are hereby down-graded, and this reverses the most Matt-facing claim in this
note.**

The block is explicit: *"Cutting `clip_da_*` to MP4 is cheap and Matt asked for it by name — **but cut
it only after the yaw fix, or you hand him a video of the bug.**"*

**All 8 MP4s in `harness_logs/s2c_mp4_2026-08-25/` depict a caster facing 180° from travel.** They
are **technically valid** artifacts — right frame counts, ffprobe-verified, encoded from the same
series their numbers came from — and they are **the wrong thing to judge against**, which is worse
than a broken file, because a broken file announces itself.

> ⚑ **`R1-dash_attack-{cathedral,arena}.mp4` MUST NOT be sent to Matt as the dash-attack judging
> object.** He asked *"what are we judging against"*; handing him this would answer a question about
> the archetype with footage of the defect, **and he is the one who spotted the backwards caster in
> the first place.**

**They are retained, not deleted** — they are the object of the *yaw* finding and the before-half of
the fix's evidence. **Re-cut after the yaw fix lands. The re-cut ones are Matt's.**

**§ 11.8's lesson stands unchanged and is now doubly earned:** a promoted file is not a delivered
one — and a *playable* file is not a *correct* one.

## 13.5 · Not folded in, deliberately

- **The yaw fix itself is NOT mine to land in this session.** The ruled shape is **two commits**
  (A: fix `s2a_stage:303` + the four `s2c_*` movers; B: introduce `face_toward()` and adopt it at the
  already-correct sites, **verified by byte-identical re-render**), and it goes to **jack-ryan at
  Gate 1 before it lands**.
- ⚑ **DO NOT BLANKET-FLIP `atan2(-x,-z)`.** `vh_caster.gd:78` sets `MODEL_FORWARD_YAW := 180.0` **at
  the body**, so for that rig family `-Z` is **correct** and flipping it re-opens WR1. jack-ryan's
  ruling, named as the docstring of the helper: **"the right formula is a function of the RIG, not of
  the repo — and nothing at a call site tells you which."** Also not every `atan2(-x,-z)` is a rig yaw
  (`s2c_cone:339` builds fan verts; `s2b_melee_arc:359/450` computes bearings).
- **`king_rig.gd`'s `_sword_yaw_left_deg := 12.0` puts the blade on the king's RIGHT** — separate
  ticket, filed, **explicitly not touched here.** *A remedy that quietly widens is how a verified fix
  becomes an unverified one.*
