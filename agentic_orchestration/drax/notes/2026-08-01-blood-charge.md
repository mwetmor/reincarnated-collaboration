# BLOOD-CHARGE — the charge-up Matt objected to is not the charge-up

**Date:** 2026-08-01
**Agent:** drax (presentation seam)
**Cell:** 6 BLOOD-CHARGE of run BR-2 (TRUE-SHAPE) · conductor gandalf (`RUN-CONDUCTOR`) · **final cell**
**Charter:** `gandalf/notes/2026-08-01-br2-true-shape-run-charter.md` (Addendum 17)
**Scope:** S-1 blood-red + translucent charge-up · S-2 SFX back on · S-3 `--dress` default · S-4 R-BR-52 shell red
**Battery of record:** `~/Games/reincarnated-godot/tmp/wr3acc/traces/`, engine stamp `16fa7e8d`. Read-only.
**Watch seed** 74000909 · camera `player_lock` · 1600×900 · **opened at godot** `51876a8`.

---

## THE CLIP

```
/Users/admin/Games/reincarnated-godot/tmp/br2watch/BR2W.mp4          ← re-cut, WITH AUDIO
/Users/admin/Games/reincarnated-godot/tmp/br2watch/BR2W-predress.mp4 ← the cell-5 cut, kept for A/B
```

Same seed, same camera, same 1600×900, same cut points, same fixed tail hold (frames 1091–1171,
2.70 s on the corpse; end card 1172–1210).

---

## §1 — S-1. THE MATERIAL AUDIT SAID ONE THING AND THE FRAME SAID A BIGGER ONE

### 1a. Where the white came from. Measured before anything was changed.

The conductor flagged that `ChargeSphereRed` is *named* Red and *renders* white, and asked which
property carries it. `Assets/PolygonArsenal/effects/ChargeSphereRed.tscn` has **two** emitters and
only one of them is red:

| node | mesh / amount | particle colour | material_override |
|---|---|---|---|
| `ChargeSphereRed` | `PolySphereMega` ×1, scale 1.3 — **the body** | `color (1,1,1,1)` · `color_initial_ramp` white→white · **`color_ramp` ABSENT** | `albedo_color (1.88809, 1.88809, 1.88809, 1)` · **no albedo_texture** · **emission NOT enabled** · `shading_mode 0` unshaded · `vertex_color_use_as_albedo true` · `transparency 1` |
| `Particles` | `PolyDiamond` ×35, scale 0.2 — the inrushing shards | `color_ramp` **IS** red→orange→pale `(1,0.141,0.133) … (1,0.952,0.656)` | the same achromatic `1.88809` albedo |

**The answer: ALBEDO.** An over-1 **achromatic** `albedo_color` multiplied by an **all-white particle
vertex colour**, on an unshaded material. Not an emission, not a texture, not white-by-design-and-
meant-to-be-tinted. The 35 shards carry the pack's "Red"; the one big sphere that dominates the
silhouette was never red at all. Third name-vs-material disagreement of the run.

### 1b. The change, as shipped

`scripts/wr2_playback.gd` — `_cj_bloodify_windup()` (new, **L12811**) called from `_cj_build()` (**L13030**),
constants at **L12396–12405**, `--windupmat` control arm at **L12414**.

- **Hue in one place:** `pm.color` ← `CJ_BLOOD (0.46, 0.055, 0.06)` — the same triple cell 3 recoloured
  the death pools to. Chosen unchanged because blood in this room is one colour or it is decoration.
  It goes on `pm.color` specifically so `_cj_modulate` keeps working: the wind-up still **brightens
  0.45 → 1.35 across its 0.500 s window** and the telegraph keeps its shape.
- **Translucency in one other place:** `material_override.albedo_color.a` — `CJ_WINDUP_BODY_A 0.18`
  on the body sphere, `CJ_WINDUP_SHARD_A 0.30` on the 35 shards (higher deliberately: they are
  ~0.2-scale specks and they carry the inward *rush*, the half of the tell that reads "still
  charging" rather than "on"). Told apart by `amount`, a structural property, not by node name.
- **The over-1 achromatic albedo is KEPT as a gain** — the hue now lives upstream of it.
- **`CJ_WINDUP_SCALE` is UNTOUCHED at 0.95.** Matt asked for translucency; a charge-up that gets
  small stops telegraphing the swipe.

Printed on every render: `[cj] claw wind-up: … MATERIAL ARM 'blood' [S-1: CJ_BLOOD (0.460, 0.055,
0.060) · body alpha 0.18 · shard alpha 0.30 · pack albedo GAIN kept · scale UNCHANGED]`.

### 1c. ⚑⚑ AND THEN I MEASURED IT, AND IT IS NOT WHAT MATT IS LOOKING AT

I built a one-word control arm to take the before/after: **`--windupmat white|off`**. `off` does not
mount the effect — but it still calls `_cj_load`, because `_cj_load` increments `_cj_seed_ctr` and
seeds every emitter off it, so skipping the load **re-seeds every combat-juice effect downstream**.
(The first build of the control did skip it, and returned a 22,000 px "footprint" with a *negative*
added signal, which is not a thing a bright additive effect can do. This file's own SLASH-ARC-1
comment — *"the Nth `_cj_load` call is the same effect in both"* — is the invariant I broke and then
restored. Load-and-discard costs one instantiate.)

With the control honest, at the wind-up's own lit frames:

```
frame 88  (wind-up lit, G-5a coverage 2/2 in-window events, 24 captured frames lit)
  CW_W (pack white) minus CW_O (not mounted)  →  the ONLY added signal in the whole
  1600x900 frame is two floating damage numerals drifting by one tween step.
```

**The claw wind-up draws ≈0 added lit pixels at watch scale.** It is mounted (2/2 hand sockets, 0
misses), it is emitting, G-5a is satisfied — and it is invisible. Plate:
`tmp/br2watch/m6/plates/S1_windup_added_signal_f88.png`.

*Descriptive, not a gate.* G-14b/c/d are NOT CALLABLE this cell (clip floor 2,305 lit px against a
40 px bar). Frames chosen under 100, where cell 4 found the two renders byte-clean.

### 1d. What the bright white opaque thing on the werewolf actually is

Found by peel, not by argument. Each arm is one flag off the treatment:

| arm | flag | the white capsule on the werewolf |
|---|---|---|
| `CW_O` | `--windupmat off` | **still there** |
| `CW_A` | `--aura 0` | **still there** |
| `CW_S` | `--slasharc 0` | **still there** |
| `CW_L` | `--leechpulse 0` | **still there** |
| `SH6N` | `--nomark 1` | **GONE** |

Only two things sit behind `--nomark`: the **ward** shell and the **rime** shell. This body is not
warded — `wr3_icearmor` is the boss's (120 ticks, G-5e 100 % on the boss). Therefore it is the
**`action_lock` RIME CRUST on the player**. The shell differential images it as a blue capsule with a
**clipped white core** — saturated in both arms, which is exactly why it reads "opaque".

Plates: `S1_object_as_rendered_f72.png` · `S1_object_nomark_f72.png` · `S1_shell_differential_f72.png`.

⚑ **This is the third time this run that Matt's eye has found a real defect and named the wrong
object.** R-BR-44 was the first (*"is the consistently appearing circle around the boss just its wind
up for its swings? IF SO, we can remove that entirely"* — the condition was false; the register error
was real). The defect here is written in `tg_body_shell.gdshader`'s **own header**:

> *"the read must be ATTACHED TO THE BODY'S OUTLINE and must not fill it — a solid shell would hide
> the swing animation and the commit-lock pose, which are the two channels the fight's melee tell is
> carried on."*

At 36.32 px/m it fills, and it hides the swing. The shader forbids what the shader is doing.

### 1e. S-1b — I took the translucency half and I did not take the hue half

`scripts/wr2_playback.gd` — `TG_RIME_GAIN := 0.30` (**L6620**), applied at the rime call sites (**L8243 / L8248**).

- **"Barely there" is unambiguous under every reading of Matt's instruction**, and the shader's own
  design intent asks for it independently of Matt. **Taken.**
  The number is grounded, not eyeballed: Matt **ratified** the boss's ward shell, which runs
  `rim_gain 0.95` with no crackle. The rime ran **1.10 with `crackle 0.55`**, so its peaks reach
  1.10 × 1.55 = **1.71** — about 1.8× the gain of the shell he approved. **0.30** puts its peak at
  0.465, roughly **half** the ratified ward. "Subordinate to the shell the owner already approved" is
  a definition of *barely there* someone else can check.
- **The three properties that keep the rime separable from the ward in a still frame are UNTOUCHED**:
  1.02× scale, 1.20 s breath, `crackle 0.55`. Only brightness moves.
- **"Blood-red" is NOT unambiguous. NOT TAKEN.** This is an **ice control tell** — the frost crust of
  an `action_lock` — and Matt believed he was looking at the werewolf's own charge-up. Repainting the
  fight's control grammar red on the strength of a mis-identification is not mine to do.
  **→ MATT DECISION, §5.**

---

## §2 — S-2. THERE WAS NO MUTE. THE MIXER WAS NEVER RUN.

Matt: *"hoping the SFX will turn back on along with the `--dress 1`"*.

I looked for the flag and **there is no flag.** `wr2_playback.gd` contains no `--nosfx`, no `_sfx_on`,
and no `AudioStream` of any kind — **by design**: this is a captured-frame render, Godot's audio clock
is the wall clock, and a windowed Metal capture does not run at 30 fps wall. The audio is **mixed
offline** by `scripts/rs_sfx/mix_sfx.py` from the render's own `beats.json` + `framemap.json`, then
muxed at encode time, so a sound cannot land on a different frame from the picture it belongs to.

Cell 5 **emitted both ledgers correctly** (`tmp/br2watch/measure/beats.json` 13.6 KB,
`framemap.json` 66.5 KB — both present, both valid; re-running the mixer over them produces a
41.87 s track with the full beat census). It then took its MP4 straight off the tail of
`scripts/run_wr2_playback.sh`, **whose ffmpeg call has exactly one input and it is the PNG sequence.**
`ffprobe` on the cell-5 file: one stream, `h264`, **no audio stream at all**.

**The audio was lost by pipeline path, not by a guard.** That is why grepping for the guard found
nothing.

**Fixed structurally, not by remembering:**
- `tmp/br2watch/run_watch.sh` now owns its own finish stage: render → `mix_sfx.py` → mux.
- `tmp/br2watch/mkclip.sh` (new, HUD-FIX-1's assembler character for character) carries the **F-AH-6
  decode gate** — full decode before the path is printed as a deliverable — and **shouts** if handed
  an empty WAV: `⚑⚑ NO WAV — this clip will ship SILENT. If that is not deliberate, S-2 has regressed.`
  A silent deliverable now has to survive a warning to ship.
- **Music stays off** (R-BR-16, `--music 0`, one flag away). Matt asked for SFX.

`assets/sfx` gate re-run before the cut: `GATE: PASS — every named file present` (50/50).

---

## §3 — S-3. THE GATE WAS CLOSED BY AN OWNER RULING

`scripts/wr2_playback.gd:5890` — `var _dress := false` → **`var _dress := true`**.

The comment read *"opt-in until the dressing is verdicted"*. **Matt watched the `--dress 1` cut and
verdicted it in.** The comment now says which, so the next reader cannot mistake a closed gate for
drift:

> *"⚑⚑ THE GATE IS CLOSED, AND AN OWNER RULING CLOSED IT — NOT DRIFT. … `--dress 0` stays, and it is
> now the CONTROL arm rather than the default: it is how a clip banked earlier in this run — every one
> of which predates the verdict — is still re-renderable byte-for-byte from its own command line. The
> flag did not disappear; which side of it is the deliverable changed."*

`--dress 1` was also **removed from `run_watch.sh`'s command line**, deliberately, so the re-cut
exercises the new default rather than masking it. Verified on the smoke run — with no `--dress` on
the line at all: `[wr1_dress] room 0 R0 the collapsed guardroom kit=dark-fortress props=131`.

---

## §4 — S-4 / R-BR-52. THE DRIFT WAS A COLOUR-SPACE BUG, AND IT COST NOTHING IN SHEEN

### 4a. Cell 4 guessed the mechanism and guessed wrong

Cell 4 attributed the red running colder with camera distance to *"the fresnel rim and the body
underneath winning more of the pixel"*. It is not that.

`tg_body_shell.gdshader` declares **`uniform vec4 tint : source_color`**. The `source_color` hint
means Godot treats the Color it is handed as **sRGB** and **linearises it** before the shader sees it.
The palette handed to it — `TG_ICE_BODY` — is an area-weighted mean of **8-bit sRGB pixels** off the
ARSENAL-2 peak plates. **It was linearised a second time.**

```
authored / sampled     0.7145, 0.9118, 1.0000     (sRGB — what the ice IS)
what the shader got    0.4689, 0.8122, 1.0000     (srgb_to_linear of it)
what cell 4 measured   0.4172, 0.8836, 1.0000     (added signal, 8-bit)
```

**0.4689 against a measured 0.4172.** The channel this run has been calling drift is the sRGB→linear
transfer sitting where nobody looked. The shell has never once emitted the ice the telegraphs are made
of. This is the **fourth** declared-vs-actual disagreement of the run and the **first one that is ours**.

### 4b. The fix, in two named terms, both solved

`scripts/wr2_playback.gd` — `_l2s()` (**L6614**) + `_shell_tint()` (**L6624**) + `TG_SHELL_R_GAIN` (**L6566**),
applied at the ward call site (**L8280**) and both rime call sites (**L8243 / L8247**).

1. **`_shell_tint()`** — pre-compensates red by calling `linear_to_srgb`, so what the shader *receives*
   after Godot's conversion is the sampled value. Written as the mechanism, not as a pasted constant,
   so it travels with any tint the callers pass.
2. **`TG_SHELL_R_GAIN = 1.1252`** — the residual tonemap term. The shell is `blend_add` onto a body
   whose red base is already high, and an sRGB transfer compresses an addition the brighter the base
   under it is. Solved from two measured points on the same instrument, not dialled:
   `measured = 0.72476 × red_in + 0.07736`; solving for **0.65** (the middle of the ruled band,
   because per-frame scatter runs 0.32–0.80 and aiming at an edge would be aiming at a number the
   instrument cannot resolve) gives red_in = 0.7901 = 1.1252 × 0.7145.

**Red only, deliberately.** The same bug is on green and blue. Cell 4 measured green landing on the
sample and the conductor ruled red. Correcting all three lifts the shell's whole luma and is a look
change nobody asked for. **Green/blue routed to BR-3, §5.**

### 4c. The measurement. Three points, one instrument (`scripts/sheen_gate.py`, unchanged).

| | red | green | blue | **p99 / median (sheen)** |
|---|---|---|---|---|
| ARSENAL-2 sampled ice (the target) | 0.7145 | 0.9118 | 1.0000 | — |
| cell 4, watch scale, **as verdicted** | **0.4172** | 0.8836 | 1.0000 | **4.93** |
| colour-space fix alone | 0.5952 | 0.8959 | 1.0000 | 4.95 |
| **+ tonemap term — AS SHIPPED** | **0.6508** | 0.8968 | 1.0000 | **4.90** |

**Landed at 0.6508. Ruled band 0.60–0.71. Target was 0.65.** 86,505 pooled shell pixels.

**And it cost nothing in sheen.** 4.93 → 4.95 → **4.90** across the three configurations — the
prediction was that a per-channel constant multiply of one spatial distribution leaves a ratio of its
own percentiles where it is, and it did. **No HALT on S-4.**

⚑ **Instrument honesty, two items.**
1. The ~2,000 px non-determinism speckle is ~2.4 % of an 85 k sample and enters as scatter, not
   concentrated on the shell. I would not quote either figure past two decimals.
2. **The instrument was never boss-only, and cell 4 called it "the boss shell".** At frames 60–100
   the *player's* rime shell is **70–85 %** of the shell pixels in the pool (14,876 / 17,286 at
   frame 60). §1e dims that shell, so the as-shipped 0.6508 is measured on a pool the ward now
   dominates — **more** faithful to the ruling than the number it replaces, but not the same pool
   cell 4 measured. Both changes are in the shipped arm and the number describes the shipped picture.

---

## §5 — ROUTED TO BR-3 / MATT. NAMED, NOT TAKEN.

| item | for | why not here |
|---|---|---|
| **Should the player's `action_lock` rime crust be BLOOD-RED?** | **MATT** | He asked for it believing it was the werewolf's charge-up. It is an ice control tell. He should rule knowing what it is. §1e. |
| **`ChargeSphereRed` draws ≈0 px at watch scale** | BR-3 | It is mounted, emitting, and G-5a-clean, and the player cannot see it. Either it earns a size/placement that reads at 36 px/m or the claw wind-up needs a different carrier. The gate that passed it measured presence, not visibility. |
| **`tg_body_shell.gdshader` fills instead of rims at watch scale** | BR-3 | `TG_RIME_GAIN` treats the symptom on one caller. The `rim_power 2.6` fresnel on a capsule at 36 px/m is the cause, and the ward has it too. |
| **Green + blue of the shell tint are still double-linearised** | BR-3 | Same bug as §4a, two channels, deliberately left. Fixing them is a luma change. |
| **`sheen_gate.py` pools player + boss shells** | BR-3 | Cell 4's "boss shell" statistic. Needs a body-scoped mask before anyone quotes it as the boss's again. |
| **The third renderer non-determinism term** | BR-3 | Untouched per dispatch. 2,305 lit px from frame 100 onward, surviving `--nodust`/`--noambient`/`--nohud` and the `_cj_load` seeding fix. |

---

## §6 — FILES

**Changed (godot, local-only):**
- `scripts/wr2_playback.gd` — S-1 (`_cj_bloodify_windup`, `CJ_WINDUP_BODY_A/SHARD_A`, `--windupmat`),
  S-1b (`TG_RIME_GAIN`), S-3 (`_dress` default), S-4 (`_l2s`, `_shell_tint`, `TG_SHELL_R_GAIN`).
- `tmp/br2watch/run_watch.sh` — S-2 finish stage; `--dress 1` removed from the line.

**New (godot, local-only):**
- `tmp/br2watch/mkclip.sh` — audio-carrying assembler + F-AH-6 decode gate + silent-clip warning.
- `scripts/windup_measure.py` — S-1's instrument. Descriptive by construction and says so.
- `tmp/br2watch/run_measure6.sh` — the measurement batch.
- `tmp/br2watch/m6/plates/` — the four evidence plates.

**Unchanged and never written:** `tmp/wr3acc/traces/`.
