# ARSENAL-HARVEST — Polygon Arsenal into the Godot crypt

**Date:** 2026-08-01
**Agent:** drax (presentation seam)
**Cell:** ARSENAL-HARVEST of run BR-1 (BATON-RENDER) · conductor gandalf (RUN-CONDUCTOR)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-30-ambient-refit-fold-in.md` — Scope 28
(Matt's two named misses), D-VFX-1 (purchase + delivery), VFX-SCOUT (license verdict + Option A
asset-strip method), F-BR-4/F-BR-5 (VFXController collision; usability gate)
**Single-writer:** opened at godot `42e9caf` (BEAM-V3) as the brief specified. No foreign commits.
**Substrate (read-only, unmodified):** `/Users/admin/Setup Guide In-Editor Tutorial/Assets/Polygon Arsenal/`

---

## 1. What landed

**33 effects, 119 emitters, 13 meshes, 8 textures — both of Matt's named misses covered by name.**

| Matt's miss (Scope 28) | Harvested payload |
|---|---|
| (b) "the boss AoR Ultimate has no VFX" | `Ground Slam` ×4 tints + the **nine Nova types** + `LightningWave` = **14 effects** |
| (a) "I don't feel the player character's swings … very sad for a werewolf fantasy" | **17 Melee & Sword effects** — 7 slashes, 4 sword impacts, Club Slam, 2 sword trails, Stun, 2 Cleave |
| bonus (pipeline proved cheap) | `SurfaceExplosion`, `GroundSpikes` = 2 |

Method was Option A asset-strip exactly as the scout specified: copy the meshes and textures,
parse the Shuriken YAML deterministically, hand-derive Godot equivalents from the transcribed
parameters. **EULA §2.2.1.1(g) honoured by construction** — the transcriber is a parser, never a
generator; every number in the emitted scenes traces to a line in a source prefab. No pack content
was fed to a model.

The scout's central claim held up: **Archanor puts the look in the art.** 76 of the 96 material
references are Unity's stock particle shader; only 10 touch one of the pack's four custom Amplify
shaders. 13 meshes and 8 textures carry 33 effects.

---

## 2. Gates — honest

| Gate | Result |
|---|---|
| **Config + live** (`scripts/pa_gate.gd`, headless) — loads, owns a draw-capable node (`draw_pass_1` non-null, `amount > 0`, `lifetime > 0`, process material present, non-degenerate AABB), reports emitting after 3 frames in a running tree | **33 / 33 PASS** |
| **Pixel** (`scripts/pa_pixel_gate.gd`, windowed Metal) — renders each effect alone on a black stage with glow on, counts lit pixels at peak against an **in-run empty-stage control** | **33 / 33 PASS**, control lit = 0 |
| **Register test** — same fight, same camera, same beats, one flag differs | rendered; **Matt judges, no self-verdict** |

⚑ **The pixel gate passes three effects that are effectively invisible standing still**, and the
number says so rather than the label hiding it: `SwordTrailShadow` peaks at **7 lit pixels**,
`SwordChargeUp` at 139, `SwordTrail` at 232, against 12,000–47,000 for the hero effects. These are
the **trail-class** effects — Unity draws them as ribbons behind a *moving* host (a swung weapon),
and a static isolation stage gives them nothing to streak along. They are not broken and they are
not proven either; they need a moving-host test this cell did not run. Named as a debt.

⚑ **What the gates cannot settle:** whether the register is *right*. That is Matt's, in motion.

---

## 3. Four defects caught in my own output

Each of these passed a reading of the source and produced a plausible picture. Each was wrong.

**1 — `minScalar` is stale editor state.** Shuriken keeps every mode's last-used value in one
record, so a *constant*-mode field carries a minimum from whenever the artist last had it on
random-between-two-constants. `SlashWideBlue`'s start speed is constant 0 and carries `minScalar: 5`;
its emission rate is constant 0 and carries `minScalar: 10`. Reading `minScalar` as the minimum
invented values the effect does not contain — a 5 m/s drift on a stationary slash and a 10/s
emission on an emitter that only bursts. It is authoritative **only** in modes 2 and 3. Fixed in
`pa_parse.mmcurve`; the same fix also ordered mode-3 pairs, because Unity does not guarantee
min ≤ max (a ±120°/s rotation serialises as min +2.094, max −2.094).

**2 — flattening the hierarchy discarded the prefab root's rotation.** Every Polygon Arsenal combat
prefab roots at −90° X. That single rotation is what stands `VerticalGlow` up and lays GroundSlam's
emission ring flat on the floor; all five children are identity. Emitting each child with only its
own local transform tipped every effect on its side. Fixed by composing the whole ancestor chain in
Unity space and conjugating by `diag(1,1,−1)` **exactly once** at the end — a handedness flip is a
similarity transform, not a component swap, so it cannot be applied per-node.

⚑ **The orientation was then settled against the pack's own demo scene, not my eye.**
`Demo/Scenes/Combat/PolyCombat02.unity` instantiates `GroundSlamRed` at `m_LocalRotation (0,0,0,1)`
on the ground plane — identity. The prefab's own root rotation *is* the authored orientation, and
our port reproduces it. My first read of the render had it backwards; the deterministic read of the
demo scene corrected me. (This is the BEAM-V3 lesson repeating: one sign, and the eye is not the
instrument that settles it.)

**3 — the mesh extractor baked a translation Unity never applies.** Godot's ufbx importer parks two
different things on the same `MeshInstance3D` node: the Z-up→Y-up axis conversion (which we need,
because Unity bakes its equivalent into the Mesh asset) and the FBX node's own placement offset
(which we must refuse, because Unity's `ParticleSystemRenderer` references the object-local Mesh
asset with no node transform). Basis yes, origin no. `PolyStar03`'s importer node sits at
(0.579, 0, −0.561) — baked in, every star would have drawn half a metre off its own particle.

**4 — `m_RenderMode: 5` read wrong twice before it read right.** Eleven emitters carry it.
- *First read* — fall through to the default QuadMesh. Result: eleven white billboard blobs Unity
  does not draw. A fidelity error in the **worse** direction, because it adds.
- *Second read* — mode "None" means Unity draws nothing, so drop them. Result: NovaLightning's ring,
  NovaLightningWave's three arc banks, SwordImpactEpic's ring, both sword trails and Stun's two
  lines all deleted. `SwordChargeUp` dropped to zero emitters and failed the gate.
- *Third and correct read* — **all eleven carry an enabled `TrailModule`.** "Renderer None + Trail"
  is Unity's ribbon idiom: the particle is not drawn, the trail behind it is the entire visual.
  Mapped to `RibbonTrailMesh` + `trail_enabled`. A mode-None emitter *without* a trail genuinely
  draws nothing and is dropped-and-counted; across this harvest there are none.

**And one refusal that is not a defect but would have flattered the result:** the bake-off arm
applies a `big` 1.7× multiplier when spawning an area effect. That constant is a *catalogue
correction* — Binbun scenes are authored small and need it to read at the CAM-LOCK stand-off.
Polygon Arsenal is authored at ARPG combat scale already (GroundSlam's expanding ring is 4.65 m in
the source prefab). 1.7× makes it 7.9 m, which is **42 % of frame height** at the 34.8 m stand-off
and reads as a dome swallowing the stage. Polygon Arsenal now spawns at 1.0, so the register Matt
judges is the pack's own and not ours amplified.

---

## 4. Census — per effect

`unmapped` = refused rather than faked. `partial` = approximated, and named.

| Effect | Emitters | Unmapped | Partial (approximated) |
|---|---|---|---|
| GroundSlamRed / Purple / Blue / Green | 6 each | — | TrailModule; limitVelocity(fraction→absolute); renderer:stretch; sizeOverLifetime:separateAxes |
| NovaFrost | 3 | **SubModule (1)** | inheritVelocity; limitVelocity; renderer:stretch |
| NovaHoly | 3 | **SubModule (1)** | inheritVelocity; limitVelocity; renderer:stretch |
| NovaLife | 3 | **SubModule (1)** | inheritVelocity; limitVelocity; renderer:stretch |
| NovaShadow | 5 | — | TrailModule; inheritVelocity; limitVelocity; velocityOverLifetime |
| NovaEnergy | 7 | — | TrailModule; inheritVelocity; limitVelocity; sizeOverLifetime:separateAxes |
| NovaFire | 3 | — | TrailModule; limitVelocity; sizeOverLifetime:separateAxes |
| NovaLightning | 7 | — | TrailModule; inheritVelocity; limitVelocity; renderer:None+Trail→ribbon; sizeOverLifetime |
| NovaSpike | 3 | **SubModule (1)** | inheritVelocity; limitVelocity |
| NovaStorm | 5 | — | TrailModule; inheritVelocity; limitVelocity; renderer:None+Trail→ribbon; velocityOverLifetime |
| NovaLightningWave | 6 | **SubModule (2)** | TrailModule; inheritVelocity; limitVelocity; renderer:None+Trail→ribbon; sizeOverLifetime |
| SlashWide / Gold / Green | 2 each | — | limitVelocity; velocityOverLifetime |
| SlashSmall | 2 | — | limitVelocity; velocityOverLifetime |
| SlashSpinThick | 2 | — | limitVelocity; velocityOverLifetime |
| SlashSpinThin | 2 | — | velocityOverLifetime |
| SlashFrenzy | 3 | — | limitVelocity; renderer:stretch; velocityOverLifetime |
| SwordImpact | 3 | — | limitVelocity; renderer:stretch |
| SwordImpactEpic | 4 | — | TrailModule; limitVelocity; renderer:None+Trail→ribbon; renderer:stretch |
| SwordBlock | 3 | — | limitVelocity; renderer:stretch |
| SwordChargeUp | 1 | — | TrailModule; renderer:None+Trail→ribbon; velocityOverLifetime |
| ClubSlam | 3 | — | limitVelocity; renderer:stretch; sizeOverLifetime:separateAxes |
| SwordTrail / SwordTrailShadow | 2 each | — | TrailModule; inheritVelocity; limitVelocity; renderer:None+Trail→ribbon; shape:single_sided_edge |
| Stun | 3 | — | TrailModule; renderer:None+Trail→ribbon; velocityOverLifetime |
| CleaveGeneric / CleaveShadow | 3 each | **SubModule (1) + SubModule (4)** | limitVelocity; renderer:stretch; sizeOverLifetime; velocityOverLifetime |
| SurfaceExplosion | 2 | — | limitVelocity |
| GroundSpikes | 6 | **SubModule (0)** | limitVelocity; renderer:stretch; sizeOverLifetime:separateAxes |

**Totals across 119 emitters:** unmapped = SubModule ×12 (8 effects). Partial =
limitVelocityOverLifetime ×84 · renderer (stretch + ribbon) ×27 · TrailModule ×21 ·
velocityOverLifetime ×18 · inheritVelocity ×16 · sizeOverLifetime:separateAxes ×13 · shape ×4.

**The one that matters:** `SubModule` — sub-emitters are not instanced. The affected effects
(NovaFrost/Holy/Life/Spike, NovaLightningWave, both Cleaves, GroundSpikes) lose a secondary
particle burst that Unity spawns off the primary. Godot has `sub_emitter_mode`, so this is
buildable; it needs a second pass that emits the sub-system as a node and wires the reference.
Queued, not refused-forever.

**Render-mode census (119 emitters):** mesh 74 · billboard 18 · stretch 16 · none+trail 11.
**Flattened (not skipped):** 2 depth-2 emitters (`CleaveGeneric`/`CleaveShadow` → `Ember`) are
emitted with their full composed transform; the intermediate node is not reproduced.
**Dangling texture refs (2):** `PolyIce` and `PolyCrystalDark` point at texture GUIDs that exist
nowhere in the imported project (Unity built-in editor resources). Those two materials rebuild
untextured. Named, not silently substituted.

---

## 5. Skipped, and why

| Skipped | Why |
|---|---|
| Colour siblings of every harvested effect (~60 prefabs: GroundSlam Pink/Yellow, all EnergyNova/FireNova/LightningNova/SpikeNova/StormNova tints, Slash Purple set, SwordImpact Gold/Green, ClubSlam ×3, Sword Enchantment ×10, Sword Trail ×7) | Identical emitter topology; they differ **only** in the startColor gradient, which §6 shows our element grammar overrides. Harvesting one buys all of them. |
| `Barrage/Nova` (14) | Nova-shaped barrages of *flying* projectiles. **R-BR-3 forbids invented travel** — our schema has no projectile flight, so these would render a mechanic that does not exist. |
| `Missiles` (25), `Beams`, `Chains`, `Flamethrower`, `Orbital Beam` | Travel- or channel-bearing. Same R-BR-3 bar. |
| `SpikeCleave` / `SpikeCleaveFast` / `BoneCleave` (20) | Ground-spike variants; the family is represented by `GroundSpikes`. Redundant against budget. |
| `Aura` (6), `Curses` (9), `Debuffs` (9), `Enchant` (8), `Necromancy` (6), `Death` (8), `Gore` (11), `Explosions` (32), `Muzzleflash` (30) | Outside the two named misses. **Queued, not refused** — the pipeline now runs in one command, so a second tier costs a manifest edit. |
| Whole `Environment/` and `Interactive/` trees | Ambient + loot layers; the crypt's ambient seam is settled (BEAM-V3) and re-dressing it is not this cell's scope. |
| Pack `Scripts/` (5 C# files) | Unity C#. Assets and parameters only, per the brief's hazard note. `PolygonLightFade`'s *behaviour* is worth re-authoring later for the 15 harvested OmniLight3Ds; its code is not portable. |

---

## 6. Element grammar — measured, not assumed

**All 8 harvested textures measure chroma 0.0000. Every one is a pure greyscale mask.**

| Texture | Mean chroma | Verdict |
|---|---|---|
| polyslash02 / 03 / 04 .png | 0.0000 | material/vertex-driven → **tintable** |
| polySpriteGlow · polySpriteRingGlowSoft · polyspriteline | 0.0000 | **tintable** |
| polyGradientVertical · polyGradientMirrored | 0.0000 | **tintable** |

(Measured by decoding each PNG in pure stdlib and taking mean `(max−min)/max` over opaque samples.)

**Where the colour actually lives** — confirmed by diffing three harvested tints of the same effect:

```
GroundSlamRed    color_ramp = (1, 0.884, 0.542) → (1, 0.575, 0) → (1, 0.361, 0) → (1, 0.264, 0)
GroundSlamBlue   color_ramp = (1, 1, 1) → (0.971, 1, 1) → (0, 1, 1) → (0.165, 0.133, 1)
GroundSlamGreen  color_ramp = (1, 1, 1) → (1, 1, 1) → (0.490, 1, 0) → (0, 1, 0)
```

Identical emitter topology, identical meshes, identical textures — **only the transcribed
`colorOverLifetime` gradient differs.** So the whole harvest is retintable to our
fire/ice/wind/dark/nature families by swapping one `GradientTexture1D` per emitter, with no
re-harvest. That is a property of the pack (art-carried, per the scout) and it is now measured
rather than inferred.

**Zero texture-baked (fixed-colour) effects in this harvest.**

---

## 7. The register test — what Matt watches

Rendered in the crypt (`kit_replica_level`) at the **CAM-LOCK camera**, on the same fight the
VFX-BAKEOFF C2 arm was judged on (`after / pre / boss / A / 74000806`, `--playerlight A`,
520 frames, NOHUD). **The only variable between the two clips is `--vfxarm`.**

A new `--vfxbeats 1` flag overlays a **fixed, labelled beat script** so the watch contains the two
things Matt named as missing whether or not this seed produces them. Both arms fired the identical
six beats at identical times and identical world positions (verified from both logs):

| t | Beat | Position source |
|---|---|---|
| 2.23 s | BEAT 1 — BOSS ULTIMATE (Ground Slam) | boss's own trace position |
| 5.00 s | BEAT 2 — NOVA (frost) | boss |
| 7.63 s | BEAT 3 — MELEE SWIPE 1 at werewolf strike range | midpoint player↔boss, hand height |
| 8.37 s | BEAT 4 — MELEE SWIPE 2 | same |
| 10.63 s | BEAT 5 — BOSS ULTIMATE (Ground Slam, fire) | boss |
| 13.03 s | BEAT 6 — NOVA (lightning) | boss |

⚑ **Times and beat kinds are scripted; positions are read from the live frame.** Nothing is
invented about where anything is, and R-BR-3 holds — no projectile travels. **Zero fight semantics
move**: the beat layer only draws.

⚑ **C2 has no ground-slam primitive.** It answers BEAT 1 and BEAT 5 with its largest available
effect. That shortfall is the finding, not a defect in the comparison — it is precisely miss (b).

### The clip is measured, not assumed

The two clips are byte-identical except the arm, so **any pixel difference between them IS the
VFX.** Decoded both in full and differenced frame by frame at 320×180:

| Beat | peak mean \|diff\| in the following second |
|---|---|
| 1 — Ground Slam | **2.00** |
| 2 — Nova (frost) | 8.68 |
| 3 — Melee swipe 1 | 9.44 |
| 4 — Melee swipe 2 | **10.52** |
| 5 — Ground Slam (fire) | 6.14 |
| 6 — Nova (lightning) | 8.83 |
| *whole-clip median* | *4.55* |

Every beat moves the frame. Five of six clear the whole-clip median comfortably.

⚑ **A hypothesis of mine was built into an instrument and then refuted by it.** Beat 1 is the
weakest at 2.00, and I read that as "the ultimate fired off-screen" — CAM-LOCK is locked to the
*player*, so a boss-anchored beat is a real framing hazard. I built a per-beat camera projection to
confirm it. **It measures (0.448, 0.563) — near dead centre — and so do all six; the boss is in
frame for the entire fight** (`tmp/arsenalharvest/logs/PROBE.log`, half-second framing census).
So Ground Slam reading fainter than the Novas at a 34.8 m stand-off is a **register fact about the
effect**, not a framing fault. Those are very different things to hand to Matt, and I nearly handed
him the wrong one. The census stays in the harness because the hazard is real; the hypothesis it
was built for was wrong.

⚑ **My first difference check was the broken thing, not the render.** An
`ffmpeg blend=difference,eq=…` chain returned a uniformly green image that I briefly read as "the
arms are identical". It was a colour-space artifact of my own filter graph. The raw-video decode
above is the instrument that actually answers the question.

**What differs, descriptively (NOT a verdict):** at the same beat, C2 reads larger, brighter and
bloomier; the harvested Polygon Arsenal effects read smaller, sharper and more structured — the
mesh silhouettes (rings, diamonds, icicle spikes, slash arcs) are legible where C2's are billboard
glow. Whether that is the right register is Matt's call, in motion.

**NO SELF-VERDICT.** I did not grade which arm wins.

### Clips

- **WATCH FIRST → `~/Games/reincarnated-godot/tmp/arsenalharvest/clips/ARSENAL_BEATS_halfspeed.mp4`**
  — the six beats back to back, both arms side by side, at half speed. Every claim in §7 is visible
  in 40 seconds.
- `~/Games/reincarnated-godot/tmp/arsenalharvest/clips/ARSENAL_REGISTER_SIDEBYSIDE_NOHUD_CAMLOCK.mp4`
  — the full fight, C2 baseline left, Polygon Arsenal right, labels burned.
- `~/Games/reincarnated-godot/tmp/arsenalharvest/clips/ARSENAL_D_SOLO_NOHUD_CAMLOCK.mp4`
  — the harvested arm alone at full frame width.
- Isolation peaks (one PNG per effect, the frame at peak lit-pixel count):
  `~/Games/reincarnated-godot/tmp/arsenalharvest/gate/*_peak.png`

**On the labels.** The charter wants each beat labelled on-screen; the clip must render `--nohud 1`,
because the ten-line provenance banner buries the very effects Matt is judging (the first render of
this cell was unreadable for exactly that reason). Those two requirements collide on one
CanvasLayer. Resolved with a second layer (`BeatLabels`) that `--nohud` deliberately does not peel:
the clip is clean **and** self-describing, and the arm name is on every frame for the same reason
camera identity is (Scope 20 ruling 1). ⚑ This also forced *how* — **this machine's ffmpeg is built
without libfreetype, so `drawtext` does not exist.** The compose script adds no text at all. That is
the better outcome regardless: an in-engine label is stamped at the frame the beat actually fired,
where a burned-in label is stamped at a time transcribed from a log, and a transcription can drift.

⚑ **An ffmpeg encode hazard, banked:** `-preset medium -crf 18 -movflags +faststart` produced
**corrupt H.264** for the 2560×720 hstack (thousands of "Invalid NAL unit size" on decode) while
reporting success and exit 0. Caught only because I decoded the output before shipping it.
`-preset veryfast -crf 20 -r 30` is clean and verified. **Every clip in this cell was decode-verified
(`ffmpeg -v error -i … -f null -`) before being listed here.** Also: `select`+`setpts` for the
beats reel produced the same corruption; `trim`+`concat` does not.

---

## 8. Findings to route

- **F-AH-1 (queue, low) — SubModule is buildable and is the largest remaining fidelity gap.**
  12 sub-emitters across 8 effects are not instanced. Godot has `sub_emitter_mode` +
  `sub_emitter_amount_at_*`; a second transcriber pass can emit the sub-system as a node and wire
  the reference. This is the difference between FrostNova's icicles shattering and not.
- **F-AH-2 (debt, mine) — the trail-class effects are unproven, not proven.** `SwordTrail`,
  `SwordTrailShadow` and `SwordChargeUp` pass the letter of the pixel gate on 7–232 lit pixels.
  Unity draws them as ribbons behind a moving host. They need a moving-host test (attach to a
  swinging bone, measure) before anyone relies on them. The arm's `trail_attach` path now points at
  `SwordTrail`, so the restage will exercise it — but exercising is not measuring.
- **F-AH-3 (process, recurrence) — `Godot --headless --import` strips the `[rendering]` block from
  `project.godot` again.** Same defect VFX-BAKEOFF caught and restored. It recurred here and was
  restored again (`mesh_lod/lod_change/threshold_pixels=1.0`). It will recur on every cell that
  imports assets. `run_harvest.sh` now backs the file up and restores it automatically, but the
  *harness* (`run_wr2_playback.sh` and friends) has no such guard. **Route to knight-rider/jack-ryan
  as a standing guard row**, not to me — it is not the presentation seam's file.
- **F-AH-4 (INFO) — `--check-only --script` is a cheap gate this seam should have been running.**
  Both edits to the 6,700-line `wr2_playback.gd` compiled clean in under a second before any render.
  One typed-variable inference error was caught that would otherwise have cost a full render cycle.
- **F-AH-5 (INFO, for the conductor) — the scout's ranking is vindicated on measurement.**
  "Translatability is a property of the pack" was the decisive call, and the numbers back it: 13
  meshes + 8 textures carry 33 effects; 76 of 96 material references are Unity stock shader. A
  shader-graph pack would have cost a rebuild for each of the 33.
- **F-AH-6 (process, tooling hazard) — ffmpeg `-preset medium -crf 18 -movflags +faststart` emits
  corrupt H.264 on this machine at 2560×720 and exits 0.** So does `select`+`setpts`. Both were
  caught only by decode-verifying the output. Any cell that ships an MP4 should decode-verify it;
  a silent-corruption path that returns success is exactly the kind of defect a "the render
  finished" check cannot see. Route as a standing clip-gate row.

---

## 9. What this cell did NOT touch

Per the brief: **`UNIFIED_KEY_ENERGY` stays 1.00** (the 3.50 flip per R-BR-8 remains the restage
cell's job — I did not go near it). No beams, no light pools, no body scales. `project.godot`
restored to its committed state after the `--import` strip, verified by `git diff` returning empty.

## 10. Debts

- `tmp/arsenalharvest/frames/` pruned to empty after encoding (file-level `rm -f`; directory-level
  `rm -rf` remains sandbox-denied, so the empty dirs stay).
- `tmp/vfxbakeoff/` ~8 GB still awaits Matt's hand — carried forward from VFX-BAKEOFF, unchanged.
- `reincarnated-godot/AGENT_STATE.md` is now five cells behind (CAM-LOCK, MOB-CAST, BEAM-PIN2,
  VFX-BAKEOFF, BEAM-V3, ARSENAL-HARVEST). Named again; still not paid.
- F-AH-2 (trail-class moving-host test) is mine and unpaid.

---

## 11. Commits

Godot repo, all **pushed** (standing Matt authorisation, 2026-07-31). Opened at `42e9caf`.

| Hash | What |
|---|---|
| `d508f23` | the harvest pipeline — parser, material reader, manifest, transcriber, mesh extractor, both gates, arm D; the four defects in §3 |
| `5c76d84` | beat labels onto their own CanvasLayer so a `--nohud` clip can still carry them |
| `88a29a9` | per-beat camera projection + half-second framing census; the hypothesis it refuted |

Meta-repo: this note.

**Assets NOT committed** (`/Assets/PolygonArsenal/` gitignored) — commercial third-party IP under
the Asset Store EULA, same rule as the Synty trees. The tracked authority is
`scripts/pa_harvest/run_harvest.sh`, which rebuilds the whole tree from Matt's imported copy in one
command: copy → import → extract meshes → transcribe → gate.

---

*ARSENAL-HARVEST · drax · presentation seam · 2026-08-01*
*Single-writer held throughout; opened and closed with no foreign commits on the godot head.*
