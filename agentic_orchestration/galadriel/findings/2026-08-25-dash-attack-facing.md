# Dash-attack facing — adjudication

**Date:** 2026-08-25 · **Author:** galadriel (visual perception seam) · **Status:** CURRENT
**Authority:** knight-rider referral of a Matt observation. Research + report only; no Godot
project file and no gate script was modified.
**Evidence:** `s2c12` (234 `da_*` stills + 460 `clip_*` frames), `s2c38` (2106 frames),
`reincarnated-godot/harness_logs/s2c_rows12_2026-08-25/render.txt`.
**Work products:** `agentic_orchestration/galadriel/work/2026-08-25-dash-facing/`

---

## Verdict

**Matt is right, and the defect is larger than dash.** The caster's visible front points
**180° away from his travel direction** — on `dash_attack`, and on every other row of the
S2A/S2C benchmark stage. He also faces the wrong way **at rest, before any skill fires.**

There is no MP4. The encoder step produced none. There ARE 61-frame 60 fps `clip_da_*` novfx
series, which are the evidence the MP4 would have been.

---

## Root cause — two conventions in one repo

The Synty King rig's visible front is **local +Z**. The repo's shipped surfaces say so and
use the matching formula `atan2(d.x, d.z)`:

| File | Line | Formula | Comment |
|---|---|---|---|
| `scripts/render_arena_room.gd` | 524 | `atan2(dir.x, dir.z)` | **"Synty rigs face +Z"** |
| `scripts/playshell.gd` | 206, 306, 474 | `atan2(fwd.x, fwd.z)` | the played surface |
| `scripts/_zoomladder_probe.gd` | 138, 316 | `atan2(fwd.x, fwd.z)` | on `_king_rig` |
| `scripts/render_boss_arena.gd` / `render_descent_scene.gd` | 257 / 765 | `atan2(dir.x, dir.z)` | |

The benchmark stage uses the **opposite** formula — Godot's `-Z`-forward convention:

| File | Line | Formula | Affects |
|---|---|---|---|
| `scripts/s2a_stage.gd` | 303 | `atan2(-ring[i].x, -ring[i].z)` | **every staged mob, every row** |
| `scripts/s2c_dash_attack.gd` | 320 | `atan2(-aim_vector().x, -aim_vector().z)` | dash caster |
| `scripts/s2c_blink.gd` | 285 | *(identical)* | blink caster |
| `scripts/s2c_teleport.gd` | 258 | *(identical)* | teleport caster |
| `scripts/s2c_leap_strike.gd` | 282 | *(identical)* | leap caster |

`atan2(-d.x,-d.z)` aligns local **-Z** with `d`. On a +Z-fronted rig that is a clean 180° error.
Non-mover rows (`cone`, `orbit`, `vortex`, `slam`, `melee`, `circle`, `line`) never set the
caster's yaw at all, so he sits at rest yaw 0 — facing +Z — while their payloads are authored
along -Z (e.g. `s2a_stage.gd:1115` `Vector3(0,0,-1)`; `:1986` `fwd = (-sin aim, 0, -cos aim)`).
Same 180°, reached by omission instead of by formula.

`scripts/king_rig.gd:191` already records the rig's axis — *"toward body-forward (+Z, verified
via probe)"*. The same comment then calls the body's LEFT `-X`, which pairs with -Z-forward,
not +Z. **The comment is internally inconsistent and cannot settle this on its own** — which is
why it was not treated as dispositive here.

---

## Answers to the four questions

**1 · Which way is the model facing?**
`00-pre`, `03b-contact-mid`, `04-arrive` — **all identical, all +Z (screen down-left).** Travel
is -Z (screen up-right). At `00-pre` the caster already faces away from all three on-path bodies,
**before the dash exists.** So the framing is *"the caster is never oriented toward the target,"*
not *"the dash inverts facing."*

*Method — and its limits.* The caster is **43–46 px tall** in a 1920×1080 frame. No facing
judgment by eye at that scale is defensible, mine included. Three instruments were used:

- **World→screen Jacobian** fitted from the harness's own per-frame unprojections (n=305,
  mean residual 1.12 px): `+X → (+30.6,+25.7)`, `+Z → (−30.8,+23.9)` px/m. Under +Z-front the
  caster's front projects to screen `(−0.79,+0.61)` at yaw 0, `(−0.25,+0.97)` at +35,
  `(−0.96,−0.27)` at −50. The -Z hypothesis predicts the exact negation at every yaw.
- **Caster isolation** by differencing each moving novfx arm against its matched `--motion=static`
  arm (identical stage, lighting, camera; caster parked at origin), then NEAREST 10× upsample.
  Confound stated: mobs are knocked back, so mob pixels enter the mask; they are visible in the
  output rather than silently included.
- **Reading the isolated crops.** At yaw +35 the figure is unambiguous: crown, face, frontal
  chest with pendant, both legs, cape spread behind, greatsword in the right hand appearing on
  the **viewer's left** — which only happens when a figure faces you. Its blade hangs straight
  **down**, matching the +Z prediction `(−0.25,+0.97)`. At yaw 0 the cape reads screen-right
  (back = up-right = travel) and the blade down-left. At yaw −50 the blade is horizontal-left,
  matching `(−0.96,−0.27)`. **Three yaws, 85° of rotation, all three consistent with +Z-front.**
  Lighting cannot rotate correctly through three yaws; only the body can.

**Discarded instrument, recorded not deleted.** An automated blade-bearing metric was built
first (segment blue-grey `B−R>12`, take centroid, compare bearing). Unmasked it selected
**19–44 % of the crop** — it was measuring the stage's cool-toned floor, not the sword. Re-run on
the static-diff mask it still scored only **5/8, 66° mean angular error**, because a centroid over
scattered pixels is not a bearing at 45 px. **It is reported as inconclusive and carries none of
the verdict.** Stating it: the instrument answered "where is the average blue pixel," the question
was "where does the sword point," and those are not the same question.

**2 · Does body yaw change across the dash?**
**No — and this is measured from the engine's transform, not from pixels.** The harness emits
`caster.yaw` per frame. Across all **61 clip frames** of `clip_da_{arena,cathedral}_novfx`
(60 fps, aim 0): `yaw = 0.0` on every frame, exactly one distinct value. KR's observed
pixel-identity of the body between `00-pre` and `04-arrive` is therefore **explained and
predicted**, not coincidental — and it is *not* evidence that yaw is unwired (see 3).

**3 · Is yaw driven by aim?**
**Yes, exactly.** Over all 26 dash arms: `aim=0 → yaw {0.0}`, `aim=35 → yaw {0.0, 35.0}`,
`aim=-50 → yaw {0.0, -50.0}` (degrees; 0.0 is the pre-launch rest value). `yaw_deg == aim_deg`
to emitted precision. **Aim drives yaw correctly; the yaw is then applied to the wrong axis.**
At `aim=0` the wrong answer and the rest pose coincide at 0, which is why the aim-0 arms look
like "yaw was never wired" and why the aim arms were needed to tell the two apart.

**4 · Dash-specific or global? — GLOBAL.**
`lp_cathedral_aim35_novfx_05-flight-apex` (leap_strike, `s2c38`) shows the identical frontal
aspect while travelling up-screen: `W_LEAP_cath_aim35_nn.png`. And `cn_cathedral_fire_04-fan-full`
(cone, a non-mover row) shows the fan erupting up-right out of the King's **back** while his blade
points down-left: `Y_CONE_fx_x3.png`. **Dash is not the owner. `s2a_stage.gd` is.** Dash is simply
where the error became legible, because the caster translates.

---

## Second finding — `defensive` byte-identity: CONFIRMED, and EXPECTED BY CONSTRUCTION

MD5 census over all 234 `da_*` frames: **159 unique hashes, 29 duplicate groups.** KR's claim
reproduces exactly.

- `da_{arena,cathedral}_defensive_novfx_{01,02,03a,03b,03c,04}` ≡ the matching `_novfx_` frames.
  **Expected, and predicted in writing before capture.** `run_s2c_rows12.sh` states: *"the effect
  node is hidden wholesale in a control, so the two frames SHOULD be byte-identical, and 'should
  be' is what receipts are for."* This is a **passed receipt between two controls**, not a defect.
- `da_{arena,cathedral}_defensive_04-arrive` ≡ `_neutral_04-arrive` (fx **ON**). Also expected:
  the defensive layer is a `burst` that has expired by arrive. **Evidence it renders at all:**
  fx-on defensive is NOT identical to fx-on neutral at any of the five earlier motion marks.
- Baseline of legitimate duplicates behaves exactly as a correct capture should: all 13 arms
  identical at `00-pre` (×2 stages), 8 arms identical at `05-settle` / `08-post` (×2).

**F-6 disposition:** a separation measured over `defensive_novfx` vs `novfx` is a **structural
zero, not a measured zero** — correctly so, because that pair is two controls. The gate should
**assert it as a predicted identity** rather than measure across it and report the result as data.

**One additional structural zero KR's list did not name:**
`da_cathedral_aimn50_04-arrive ≡ da_cathedral_aimn50_novfx_04-arrive` — fx-ON ≡ fx-OFF, i.e. the
VFX contributes **zero pixels**. Cause is visible in the crop: the cathedral aim−50 landing point
is **fully occluded by a pillar** (`I_yawN50_arrive_cath_lz.png`). The arena counterpart at the
same mark is *not* identical, so this is stage-specific occlusion, not an effect defect. Any
`aimn50` cathedral separation number at `04-arrive` is measuring a pillar.

---

## Recommendation (drax owns the fix; not made here)

The one-line-per-site change is `atan2(-d.x, -d.z)` → `atan2(d.x, d.z)` at the five sites tabled
above. **But do not land it as five line edits.** Two things must happen first, or the fix
re-opens as a different bug:

1. **Settle the rig's forward axis once, in one place**, and reconcile `king_rig.gd:191`'s
   self-contradicting comment (+Z forward / −X left cannot both hold). A named constant or helper
   (`face_toward(node, dir)`) beats five copies of an atan2.
2. **Re-capture is required, not optional.** Every `s2c12` / `s2c38` frame in which the caster or a
   mob appears was rendered with the wrong yaw. Silhouette is a *scored axis* on the trail-bounded
   rows, and `dash_attack`'s § 3.1.11 identity is explicitly *"silhouette + knockback"* — a
   silhouette measured on a backwards body is a measured number about the wrong pose.

---

## The Mirror

The dash was never the thing. The Mirror shows a king who has faced the wrong way the whole time
he has stood on this stage — before the charge, during it, and after — and it took a moving body
to make a still error visible. The stage set every one of them facing outward, away from the
thing they were staged to confront, and every measurement taken there was taken of a back.
