# Research — Motion sources and tooling for stylised painted-2D VFX (runnable on this host) — 2026-09-15

> **STATUS:** CURRENT — legolas Mode A (UNKNOWN-RESEARCHER). Commissioned by gandalf (SPEC-AUTHOR / ARCHITECT, VFX workflow architecture session). Brief: `agentic_orchestration/gandalf/requests/2026-09-15-legolas-mode-a-vfx-motion-sources-and-tooling.md`. Filed by gandalf verbatim from the agent's returned text (the harness blocks sub-agent repo writes — same precedent as `2026-09-14-vfx-oracles/findings.md`).

**Mode:** A (analytical; read-only)
**Commissioner:** gandalf
**Host rule observed:** no video decoding, no frame extraction, no downloads at all (largest artefact this session: nothing written outside the scratchpad), one fetch at a time, peak RSS trivial. No installs, no purchases, no accounts created.

**Evidence classes:** VERIFIED (primary source fetched and read this session) · MEASURED (first-hand computation on this host, method stated) · V-SNIP (vendor/primary text seen only through a search index, not fetched — one step below VERIFIED) · PRACTITIONER-REPORT · INFERRED (my reasoning, marked) · GAP.

**Prior work cited, not redone:** `…/2026-09-15-vfx-grammar-and-authoring-split/findings.md` (grammar families F1–F11; 11 painted primitives + 5 shared constants; Hades `Fx.sjson` measurements) · `…/2026-09-14-vfx-oracles/findings.md` (Hades timing bands) · `…/2026-09-15-video-generation-alternatives/findings.md` (video-model prices and end-frame support) · `…/2026-09-15-chronicon-com-slormancer-vfx/findings.md`.

---

## Headline summary

**The motion source that is not the image model is already installed, free, and runs on this host: Godot itself.** Every external simulation tool in the brief fails at least one binding fence — EmberGen is Windows-only (a macOS edition is announced for 2.0, undated); Houdini Apprentice is macOS-arm64-native but wants 50 GB and Sonoma; Blender's Mantaflow sits at Blender's *stated minimum* RAM on an 8 GB machine; Juice FX has no Mac build; Particle Illusion's free standalone requires an account. Pixel FX Designer ($19.95, Windows **and** macOS, exports PNG sheets) is the one purchasable tool that clears every fence — but it authors *primitives*, not grammars.

**Two VERIFIED mechanisms settle the architecture.** First, `CanvasItemMaterial` gives `particles_animation` + `particles_anim_h_frames/v_frames/loop` and a `blend_mode` enum including `ADD`, `MIX` and `PREMULT_ALPHA`, plus `light_mode` — meaning the Hades layer stack measured in the prior probe (additive painted body + black Mix duplicate of *the same sheet* + flash + nova + decal + light disc) is expressible natively as sibling `GPUParticles2D` nodes sharing one texture. Second, Movie Maker mode (`--write-movie out.png --fixed-fps 30`, plus `Rendering > Transparent Background`) writes a **deterministic, alpha-preserving, 8-digit-numbered PNG sequence** — so any procedural effect can be baked to a flipbook and paint-over-stylised.

**Therefore flipbook-vs-runtime is not a fork; it is a per-grammar dial, reversible in both directions.** The rule that falls out: bake where duration and extent are fixed; compose at runtime where they are data-driven.

---

## 0. Host, established first-hand

**MEASURED** (`system_profiler SPHardwareDataType`, this session): Mac mini `Mac14,3`, **Apple M2, 8 cores (4 performance + 4 efficiency), 8 GB unified memory.** No discrete GPU; the M2 integrated GPU is the only accelerator. This is the machine every feasibility call below is made against, and it is below the *recommended* floor of every 3D simulation package surveyed.

---

# Q1 — Motion-source candidates

## 1.1 The comparison table

| Candidate | Produces | Runs on M2 / 8 GB? | Cost / licence | Stylisation applied how | Timing controlled how | → Godot | Register fit (64–128 px, 2–4 bands, no white core) | Class |
|---|---|---|---|---|---|---|---|---|
| **Godot 4.x native, procedural** (`GPUParticles2D`/`CPUParticles2D`, CanvasItem shaders, `AnimationPlayer`, `Line2D`) | A live scene — and, via Movie Maker, frames on alpha | **Yes — it is the target runtime** | Free, MIT | Runtime: `blend_mode` ADD/MIX/PREMULT_ALPHA, `modulate` tint, `light_mode`, posterise/erosion shaders on a painted mask | `fixed_fps` (per-node), `lifetime`, `explosiveness`, `preprocess`, `speed_scale`, `Curve` ramps, `AnimationPlayer` keys, engine `--fixed-fps` | native | **Best available** — it moves *painted sprites*, not procedural noise, via `particles_animation` | **VERIFIED** (class docs) |
| **Godot native → baked sheet** (Movie Maker PNG sequence) | PNG frames **with alpha**, deterministic | Yes | Free | Same as above, **plus** paint-over on the baked frames | `--fixed-fps N`; "perfect frame pacing… never… dropped frames" | re-import as flipbook | Same, plus a hand pass | **VERIFIED** |
| **Blender** (Mantaflow smoke/fire, particles, Grease Pencil, Freestyle/toon) | Rendered frames → sheet | **Qualified.** Apple-silicon native; 8 GB is Blender's *stated minimum*, and physics sim is named the most hardware-demanding workload | Free, GPL | Render settings: toon/flat shading, posterise in compositor; Grease Pencil is drawn, not simulated | Scene fps, frame range, F-curves | PNG sequence → sheet | Mantaflow output is *volumetric noise*; posterising it is a paint-over step, not a register | **V-SNIP** + **INFERRED** risk |
| **Houdini Apprentice** | Rendered frames → sheet (`mosaic` node builds the sheet natively) | Native macOS **arm64** build ("Gold"); needs macOS Sonoma 14.0+ and **50 GB free SSD** | Free non-commercial; **watermarked renders**; `.hipnc` only | Render/shader settings | Full curve control | image sequence → sheet | Same objection as Blender; also the heaviest tool to learn | **V-SNIP** |
| **EmberGen** | Rendered fire/smoke frames → sheet | **NO.** "available for Windows 10 only." A **macOS edition is announced for EmberGen 2.0**, due "2025/2026", no date | Paid (tiers not read this session) | Posterise at render (the 80.lv anime-explosion case) | Sim timeline, export fps | sheet | Would be strong for *burst* grammars if it existed on Mac | **V-SNIP** (CG Channel × 2; vendor page carries no requirements) |
| **Pixel FX Designer** (CodeManu) | **`.png` sprite sheets or `.gif`** | **Yes — Windows and macOS** | **$19.95** (currently $14.96) | Built-in: "custom pixel render pixelation", glow, outline, sepia; canvas size | "Timeline for particles" | PNG sheet → `AnimatedSprite2D` / flipbook shader | **Purpose-built for exactly our register.** Authors *primitives*, not grammars | **VERIFIED** (itch.io product page) |
| **Pixel Composer** (Ttanasart) | Node-graph pixel VFX → frames/sheets | **Yes, with a caveat** — Windows plus a **macOS build that shipped as alpha/beta** | Free on GitHub; paid on Steam | Node graph (image ops, feedback, loop, physics, fluid) | Node-graph timeline | sheet | Node-based and procedural; strong for *primitives* and for deriving variants of one painted shape | **V-SNIP** |
| **Effekseer** + `EffekseerForGodot4` | Live effects inside Godot via GDExtension | macOS build path exists (`.framework`, notarisation); arm64 not explicitly confirmed for macOS | Free (MIT-family) | Effekseer's own material/blend settings | Effekseer's timeline | native node | Introduces a **second** effect system alongside Godot's — a coherence cost, not a coherence mechanism | **V-SNIP**, with an inconsistency flagged in § 1.2 |
| **Particle Illusion** (Boris FX) standalone | Rendered particle frames | Mac + Windows | **Free** — but **requires a Boris FX account** | Emitter library presets | Timeline | image sequence | Motion-graphics register, not pixel register | **V-SNIP** — *fence violation: account required, not attempted* |
| **Juice FX** (CodeManu) | Animated variants of a still | **No macOS build** (an open "please port to macos" request exists) | Paid | — | — | — | — | **V-SNIP** |
| **TimelineFX** (RigzSoft) | "sprite sheets, animation strips, or image sequences in PNG" | Windows (BlitzMax/Monkey lineage) | Paid | — | Timeline | sheet | — | **V-SNIP** |
| **Aseprite + Lua** | Drawn frames | Yes | ~$20, already common | Drawn | Per-frame durations (holds) | sheet | **Perfect register — it *is* the register.** No motion source; the hand is the motion source | PRACTITIONER-REPORT |
| **Video model on a plate** | RGB frames, **no alpha** | Hosted; host-safe to *call*, not to decode here | $0.16–$0.84 per 6 s clip (prior findings) | — | prompt only; `end_image`/`camera_fixed` on some | would need keying | See § 1.3 | prior findings + § 1.3 |

## 1.2 Per-candidate notes that change the ranking

**Godot native — the two mechanisms that decide the architecture (both VERIFIED).**

`CanvasItemMaterial` exposes `particles_animation` — *"If true, enable spritesheet-based animation features when assigned to GPUParticles2D and CPUParticles2D nodes"* — with `particles_anim_h_frames`, `particles_anim_v_frames`, `particles_anim_loop`; and `blend_mode` with `BLEND_MODE_MIX / ADD / SUB / MUL / PREMULT_ALPHA`; and `light_mode`. **This means each emitted particle can itself be a painted flipbook, and the same sheet can be drawn twice with different blend modes.** The Hades stack measured in the prior probe — additive painted body, **black-tinted Mix duplicate of the same sheet** (56 of 78 dark sheets are the same sheet also drawn additive), 0.1 s flash, ground nova, 1–3 s decal, light disc — is therefore expressible as **sibling `GPUParticles2D` nodes pointing at one texture**, with `light_mode` excluding the additive body from the 2D light pass and a `PointLight2D` carrying Children of Morta's floor light. **This is the single most important finding in the probe:** the coherence mechanism the corpus identified as strongest is native, not something we must build.

`GPUParticles2D` timing surface (all VERIFIED, class reference): `fixed_fps` (default 30; *"changing the value to 2 will make the particles render at 2 frames per second"* — this is Guilty Gear Xrd's stepped timing as a property), `interpolate`, `explosiveness`, `lifetime`, `preprocess` (*"starts as if it had already run for this many seconds"* — instant-peak without a ramp), `speed_scale` (0 pauses), `amount_ratio` (changes density **without restarting**), `sub_emitter`, `trail_enabled` / `trail_lifetime` / `trail_sections`, `capture_rect()`, and — critically for baking — **`use_fixed_seed` + `seed`**: *"particles will use the same seed for every simulation… useful for situations where the visual outcome should be consistent across replays."* One caveat: `emit_particle()` is *"only supported on the Forward+ and Mobile rendering methods, not Compatibility."*

**EmberGen is out, and its absence is the reason the sim lane is not a lane.** Windows-only today; the macOS edition is an announced 2.0 feature with no ship date. The 80.lv posterised-anime-explosion precedent cited in the brief therefore remains a *technique* we can imitate, not a tool we can run.

**Effekseer — one inconsistency, flagged rather than resolved.** The releases page reports the latest release as **1.80.7, 9 August 2024**, and simultaneously reports that *"1.80.2 and later requires Godot 4.6"* with the note *"godot-cpp updated to 4.6 (it no longer works earlier than Godot 4.6)"*. **A 2024 release cannot have required Godot 4.6**; either the version mapping or the dates in that summary are wrong. **Do not commit to Effekseer on this reading** — someone should open the releases page by hand. Independent of that, adding Effekseer means running a second particle system with its own material model beside Godot's, which works directly against the *one stack, shared primitives* invariant.

**Pixel FX Designer is the only paid tool that clears every fence** (Mac build, $19.95, PNG-sheet export, no account, no install of a 50 GB package). Its correct role is **primitive authoring** — making the 11 painted shapes the prior probe enumerated (head, trail/streak, field body, decal, link/arc, ring, wedge, beam-mid, beam-cap, swirl, lane-segment) and the 5 shared constants — **not** grammar authoring. It cannot express "chain to N targets" or "beam of runtime length"; nothing outside the engine can.

## 1.3 Video models on a plate — evidence, and a clear negative

**No hosted RGBA/alpha video-generation endpoint was found.** Transparent video generation is an active *research* area with at least four papers: **TransPixeler** (arXiv 2501.03006; IEEE/CVPR) — a DiT with alpha-specific tokens and LoRA fine-tuning, explicitly motivated by VFX (*"alpha channels are crucial for visual effects… allowing transparent elements like smoke and reflections to blend seamlessly"*); **TransVDM** (2502.19454), a motion-constrained diffusion model for transparent video; **"Video Generation with Stable Transparency via Shiftable RGB-A Distribution Learner"** (2509.24979); **TransText** (2603.17944), alpha-as-RGB for transparent text animation. **None surfaced with a hosted API.** Every commercial endpoint priced in the prior video-generation probe (Grok, Veo 3.1, Kling, Seedance, Hailuo, Runway, Luma, Sora 2) returns **opaque RGB only**.

**Consequence for the effects lane, INFERRED but tightly constrained:** an effect returned as an opaque plate must be *keyed*, and keying requires either a flat backing colour the model holds perfectly across 144 frames or a learned matte. Neither is available here, and the failure modes the brief names — boil, hue pulsing, internal cuts — are exactly the ones that break a key, because they move the backing colour. **The character lane survives a plate because a character is a silhouette against a plate; an effect *is* the transparency.** I found no practitioner report of a shipped 2D game effect produced by keying a generated video.

**One narrow use that does survive:** a generated clip as a **timing and shape oracle** — watched, not shipped — the same role the C-3 character-lane oracle cut played. That is a design call, not a research finding.

## 1.4 Sim-then-paint precedents — what was and was not confirmable

| Precedent | Status |
|---|---|
| **EmberGen posterised anime explosion** (80.lv) | PRACTITIONER-REPORT, carried from prior findings. Technique confirmed; **tool not runnable on this host.** |
| **Houdini `mosaic` node builds sprite sheets from sim renders** | V-SNIP (SideFX forum) — *"Houdini has a mosaic node that can organize rendered images and combine them all into a flipbook texture."* The sheet-assembly step is solved in that ecosystem. |
| **"3D particle base with painted 2D sprites on top"** | PRACTITIONER-REPORT (VFX Apprentice) — *"many games mix both: a 3D particle base with painted 2D sprites on top."* This is the hybrid the brief is circling, stated as industry-normal. |
| **Fortnite "20 of ~50" frames cut from a sim** | **GAP (G-3).** Searched; not found in any primary or secondary source this session. **Do not cite it until sourced.** |
| **Guilty Gear Xrd stepped timing · Hades `Fx.sjson` per-frame holds** | Carried from prior findings, already VERIFIED/MEASURED there. |
| **An *image model* painting over sim frames** | **GAP (G-4).** No research paper and no practitioner account found. The nearest hit is the generic 3D-base + painted-2D-overlay hybrid above, which is a *human* paint-over. |

---

# Q2 — Which candidate produces the invariants an ARPG VFX system needs?

Scored 1–5. (i) timing control · (ii) grammar expressiveness · (iii) register fidelity · (iv) coherence · (v) marginal cost per new skill · (vi) host feasibility.

| Candidate | i | ii | iii | iv | v | vi | **Σ** |
|---|---|---|---|---|---|---|---|
| **Godot native, procedural (runtime composition)** | **5** | **5** | **4** | **5** | **5** | **5** | **29** |
| **Godot native → Movie Maker bake → paint-over → flipbook** | **5** | 2 | **5** | 4 | 2 | **5** | **23** |
| **Pixel FX Designer → primitives → Godot runtime** | 3 | 1 | **5** | 4 | 4 | **5** | **22** |
| Aseprite/Krita hand-drawn primitives → Godot runtime | 4 | 1 | **5** | 3 | 3 | **5** | 21 |
| Pixel Composer → primitives → Godot runtime | 3 | 1 | 4 | 3 | 4 | 4 | 19 |
| Effekseer + Godot 4 runtime | 4 | 4 | 2 | **1** | 4 | 2 | 17 |
| Blender → posterised sheet | 4 | 2 | 2 | 3 | 1 | 2 | 14 |
| Houdini Apprentice → sheet | **5** | 3 | 2 | 3 | 1 | 1 | 15 |
| EmberGen → posterised sheet | 4 | 2 | 3 | 3 | 1 | **0** | 13 |
| Video model on a plate | **1** | 1 | 2 | 1 | 1 | 3 | 9 |

**Why (ii) is where everything except the engine dies.** The prior probe established eleven grammar families whose parameters — range, radius, count, duration, chain depth, beam length — are *generated per skill* by our own pipeline. **A sheet cannot carry a runtime parameter.** No external tool can express "chain to the N nearest targets", "a beam whose mid-section tiles to the distance to the cursor", or "a field that ticks for the skill's rolled duration". Those are engine facts. Every sim/authoring tool in the table scores 1–3 on (ii) not because it is weak but because it is **upstream of the parameter**.

**Why (iii) is where the engine is weakest and the reason the hybrid exists.** Godot moves painted sprites faithfully — but the shape *inside* a burst must change between frames, and no transform produces that. A nova is not a ring scaling up; the prior probe found Hades ships `Fx\RadialNova` as a **Book** (flipbook) type referenced by 16 entries. That is exactly the gap the bake path fills, and the reason row 2 exists.

**(iv) coherence is the decisive criterion and it favours one stack unambiguously.** The prior probe's strongest finding was that the coherence mechanism which survives density is *a fixed layer stack applied identically to every effect*, not an alphabet size. Row 1 is that stack, natively. Effekseer scores **1** on coherence precisely because it is a second stack: two blend models, two timing models, two tint paths.

**(vi) is not a tiebreak; it is an elimination.** EmberGen scores 0 — it cannot be run. Houdini scores 1 — arm64-native but a 50 GB install on a machine that panicked five days ago, and its free tier watermarks output. Blender scores 2 — Apple-silicon-native, but **8 GB is Blender's stated *minimum*, and Mantaflow is identified as the most hardware-demanding workload in the package**; running a fluid sim on this host is the exact class of action the host rule exists to prevent.

**Ranking, stated plainly:** **build in Godot; author primitives in Pixel FX Designer or by hand; keep Movie Maker baking as the escape hatch for the four or five grammars that need internal shape change; treat every sim package and every video model as precedent, not tooling.**

---

# Q3a — Baking a Godot effect to a sprite sheet

**VERIFIED, and there are two independent mechanisms. Named, with their caveats.**

**Mechanism 1 — Movie Maker mode. This is the one to use.**

`godot --path /path/to/your_project --write-movie output.avi --fixed-fps 30`

- **PNG image sequence is a supported output format**, described as *"lossless video compression, at the cost of large file sizes and slow encoding"* alongside a WAV. Give the output a `.png` path.
- **Filenames are deterministic:** *"always contains 8 digits, starting at 0 with zero-padded numbers… `folder/example00000000.png`, `folder/example00000001.png`."*
- **Alpha is preserved, conditionally:** *"the root viewport must have its `transparent_bg` property set to true for transparency to be visible on the output image,"* set via the **`Rendering > Transparent Background`** advanced project setting. `Display > Window > Size > Transparent` and `Per Pixel Transparency > Enabled` optionally let you preview it while recording.
- **It is non-real-time and frame-exact:** *"The output video will always have perfect frame pacing; it will never exhibit dropped frames or stuttering,"* and it permits *"extremely demanding settings"* and *"a higher resolution than the screen resolution"* — so a 128 px effect can be baked at 4× and downsampled with control over the aliasing, which is the Dead Cells "register comes from the render settings" move.
- **Determinism of the particles themselves** comes from `GPUParticles2D.use_fixed_seed` + `seed` plus `fixed_fps`; without the fixed seed a re-bake will not reproduce.

**Mechanism 2 — `SubViewport.get_texture().get_image().save_png()` per frame.** Works, and is the right choice when you need to bake *many* variants headlessly from a script. **But it carries live known defects** (PRACTITIONER-REPORT / issue tracker): `ViewportTexture.has_alpha()` returns false when the source `SubViewport` has `transparent_bg` on (godot#94332); partial transparency can be blended against black in saved screenshots (godot#113103); `get_image()` can return blank without an `await RenderingServer.frame_post_draw` first (godot#106957); and `transparent_bg` with physical lighting units can make the *whole* subviewport transparent (godot#95805). **Use Mechanism 1 unless you need the scripting.**

**Assembling the numbered PNGs into a sheet** is solved off the shelf: the Godot Asset Library carries **Spritesheet Generator** (asset 1486) — *"generate a spritesheet from a series of images… automatically trimmed based on provided alpha threshold value,"* with padding and column control — and **Sprite Baker** (asset 370) for the 3D→2D case. TexturePacker also documents a Godot path.

**The architectural consequence, which is larger than the mechanism:** because the bake is one command and the re-import is a flipbook, **flipbook-vs-runtime is not a commitment.** Any effect can start procedural, be baked when it needs a paint pass, and be re-authored procedurally later. There is no fork in the road here — only a dial.

---

# Q3b — Flipbook vs runtime composition, per grammar class

**The rule that falls out of the evidence, stated once:**

> **Bake a flipbook where the shape changes *internally* and the duration is *fixed*. Compose at runtime where extent, direction, count or duration are *data-driven*.**

Every parameter our generator rolls — range, radius, chain depth, beam length, field duration, projectile count — is on the runtime side of that line by construction.

| Grammar class | Default | Why | Evidence |
|---|---|---|---|
| **Burst / nova / impact** (F7 radial, F10 vortex, the shared flash + glow-disc constants) | **Flipbook**, one sheet, tinted per element | Duration is short and fixed (Hades: flash 0.1 s, light disc 0.2 s); the interior must *change*, not scale. A scaled ring reads as a rubber stamp. | Hades ships `Fx\RadialNova` as a **Book** type, **16 entries off one sheet**; `particle_glow` 57 entries, `particle_quickflash` 30 (MEASURED, prior) |
| **Projectile** (F1: single, multi, fork, ricochet) | **Runtime composition** — a painted head sprite (optionally a 3–4 frame boil loop via `particles_animation`) translated by the engine, plus a trail via `trail_enabled` or a `Line2D` | Direction and count are runtime. Baking direction is the measured trap. | Hades takes direction from `AngleFromOwner=Take` / `UseOwnAngle` / `RandomFlipHorizontal`. **Diablo II bakes 8/16/32 directions per missile and 366 of 684 missiles ship single-direction** because per-direction baking stops being affordable (VERIFIED, prior) |
| **Ground field** (F3) | **Runtime** — painted decal + a looping body, scrolled/eroded by shader | Duration is rolled per skill; a fixed-length flipbook cannot cover an arbitrary duration. Needs a *loop*, not a clip. | Hades scorch decals 3.0 s @ α .85, ground crack 1 s (MEASURED, prior) |
| **Chain hop** (F6) | **Runtime, necessarily** — one painted link sprite drawn N times between N point pairs | N and the point pairs do not exist until the cast resolves | Hades `ZeusStaticArcA/B/C`, **11 entries each**, off shared arc sheets (MEASURED, prior) |
| **Beam / channel** (F9) | **Runtime, necessarily** — tileable mid + two caps | Length is the distance to the target. Only the mid's *texture* can be a scrolled flipbook. | § 1.4 of prior findings |
| **Aura / self-buff** (F2, G7) | **Runtime loop** — short painted flipbook pulse + `PointLight2D` floor light, anchored to the owner | Indefinite duration, follows the owner | Children of Morta: halo **+.16 to +.41** above ground, near-white share **0.1 %**, ground *brightens* during casts (MEASURED, prior) |
| **Displacement / dash / blink** (F4) | **Runtime** — owner silhouette streak + arrival flare | The path is the engine's own movement | Hades `AphroditeStreakA/B`, `SpearDashSwipe` ×10 |
| **Delegate** (F5) | **Neither** — the delegate carries its own grammar | Established in prior § 1.4 | — |
| **Cone** (F8), **whirlwind** (G12), **orbit** (G11), **lane** (F11) | **Runtime** — an aperture that opens, an owner that rotates, an anchor that revolves, a segment tiled to length | All four are one animated transform over a painted primitive | prior § 1.4 |

**Three constraints this imposes on the painted primitives, which are authoring-spec items, not research findings:**

1. **Primitives must be painted to be rotated.** The prior probe's H-A bound said this and it is the live risk: a head or wedge painted with a baked highlight or an implied light direction will break under runtime rotation. Hades' sheets are radially symmetric, axis-aligned, or squashable (`PostRotateScaleY ≈ 0.5–0.62`). **Spec the primitives as direction-neutral.**
2. **Primitives must be painted greyscale-tintable if one sheet is to serve every element.** That is the Hades mechanism (112 of 126 god-variant families share one texture, recoloured at runtime) and it is what makes the ≤ ~12-shapes-per-element figure achievable. It also composes with the "no white core" rule: a tint multiplied into a near-white sheet *is* white.
3. **Memory is not the constraint at this register.** A 12-frame 128 px flipbook is a 512×384 sheet. **The cost of a flipbook here is the authoring hour, not the VRAM** — which is why the bake path is affordable for the four or five burst-class grammars and unaffordable as a default for all eleven.

**Where the corpus disagrees with itself, reported rather than averaged:** Hades composes almost everything at runtime (66 % of 5,141 FX entries declare no texture at all); Cuphead draws every effect and paid years for it; Dead Cells bakes everything from 3D and gets its register from render settings; Slormancer **splits by layer** — pixel-drawn shapes for signature forms and summons, engine particles for glow — and the prior probe measured Slormancer and Hades as the two that read most strongly as one language. **The split-by-layer answer is the one with two independent supporters, and it is the one this rule reproduces.**

---

# Cheapest first experiments

Ordered by cost. **Nothing below requires a purchase, an account, or an install.**

1. **£0, ~1 hour — the layer-stack proof.** In Godot, one 128 px greyscale painted disc. Two `GPUParticles2D` siblings on that one texture: A with `CanvasItemMaterial.blend_mode = ADD` and a hue `modulate`; B with `blend_mode = MIX`, `modulate = black`, drawn beneath, at ~1.05 scale. Add a 0.1 s `quickflash` sprite, a `PointLight2D` floor light, and a 3 s decal. **Question it answers:** does the Hades stack, reproduced natively, make *one painted shape* read as a finished effect at our register? This is the cheapest test of the probe's strongest finding and it needs one drawing.
2. **£0, ~1 hour — the bake round-trip.** Same scene. Enable `Rendering > Transparent Background`, set `use_fixed_seed`, run `godot --path . --write-movie bake/fx.png --fixed-fps 30`, confirm the 8-digit PNGs carry alpha, assemble with Spritesheet Generator, re-import as a flipbook, and **A/B the baked flipbook against the live scene.** If they match, the dial in Q3b is real and every later flipbook/runtime decision is reversible.
3. **£0, ~30 min — the rotation-survival test.** Take one painted head primitive and spin it through 360° at runtime. **Question:** at what point does the paint read as a rotating *drawing* rather than a moving *thing*? This is the one thing the whole corpus does not test, and it directly bounds H-A.
4. **£0, ~2 hours — the stepped-time probe.** Set `fixed_fps` to 30, then 15, then 12, then 8 on the same effect, `interpolate` off. **Question:** where is our Guilty Gear Xrd point — the frame rate at which the effect reads as *drawn* rather than *simulated*? Hades runs `PlaySpeed` median 60; the Xrd precedent runs far lower. Our register is nearer Xrd's.
5. **$14.96, if 1–4 land — Pixel FX Designer**, to author the 11 primitives rather than draw them. **Not before**, because its output only has value once the stack that consumes it is proved.

**Explicitly not recommended as a first experiment:** any Blender/Houdini install (host rule, and the 50 GB figure), any EmberGen work (does not run), any Effekseer integration (second stack; version claim unresolved), any video-model spend on effects (no alpha, no keyable plate, no shipped precedent).

---

# Knowledge gaps not resolved

- **G-1 — EmberGen 2.0's macOS ship date and requirements.** Both CG Channel references are secondary; the vendor product page carries no requirements section and the docs landing page returned navigation only. **Next source:** `docs.jangafx.com/embergen/` full sidebar, or the JangaFX roadmap page. Not pursued — the tool is out on this host either way.
- **G-2 — `EffekseerForGodot4`'s Godot-version mapping is self-inconsistent** (a August-2024 release cannot require Godot 4.6). Also unconfirmed: whether the macOS `.framework` assets are arm64, universal, or x86_64-only. **Next source:** open the releases page by hand and read one release's asset list.
- **G-3 — The Fortnite "20 of ~50 frames cut from a sim" datum was not found.** Searched this session against VFX-pipeline sources; no primary or secondary hit. **Do not cite it until sourced.**
- **G-4 — No case found of an *image model* painting over simulation frames**, in research or practice. The nearest attested pattern is the human 3D-base-plus-painted-2D-overlay hybrid.
- **G-5 — No hosted RGBA video-generation API found.** Four research systems exist (TransPixeler, TransVDM, Shiftable RGB-A, TransText); none surfaced as a callable endpoint. Running any of them locally is out under the host rule.
- **G-6 — Blender Mantaflow at 8 GB is UNTESTED, and I did not test it.** Every statement in the table is from secondary system-requirement writeups, and the one directly relevant fact — 8 GB is Blender's *stated minimum* while smoke sim is its *most demanding workload* — is an argument against attempting it on a machine that kernel-panicked on 2026-09-14, not a measurement.
- **G-7 — Godot 4.6's release status was not confirmed this session.** The brief names 4.6; every class-reference citation above is from the `stable` docs channel, and every property cited is long-standing 4.x API. `use_fixed_seed`/`seed` and `restart(keep_seed)` are the newest and should be version-checked against the installed build before the bake experiment.
- **G-8 — Pixel Composer's macOS build maturity.** Sources indicate a macOS build that shipped as alpha; current stability unknown. Not load-bearing given its ranking.
- **Blocked / not attempted (host rule and fences):** no video decoded, no frames extracted, nothing downloaded, no account created (which is why Particle Illusion's free standalone was not evaluated first-hand), no software purchased or installed.

---

# Source list (accessed 2026-09-15)

**Host (MEASURED, first-hand)**
- `system_profiler SPHardwareDataType` on the Mac mini `Mac14,3` — Apple M2, 8 cores, 8 GB

**Godot (VERIFIED — fetched and read this session)**
- Creating movies / Movie Maker mode — https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html
- `GPUParticles2D` class reference — https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html
- `CanvasItemMaterial` class reference — https://docs.godotengine.org/en/stable/classes/class_canvasitemmaterial.html

**Godot (V-SNIP / PRACTITIONER-REPORT, via search index)**
- Movie Maker PR — https://github.com/godotengine/godot/pull/62122
- `SubViewport` capture defects — godot issues #94332, #113103, #106957, #95805
- Sprite Baker (asset 370) — https://godotengine.org/asset-library/asset/370 · Spritesheet Generator (asset 1486) — https://godotengine.org/asset-library/asset/1486
- Godot Shaders library (posterisation / stylised / 2D VFX tags) — https://godotshaders.com/ · https://godotshaders.com/shader/2d-sprite-based-vfx-gradient-shader/ · https://github.com/arkology/ShaderV

**Tools (VERIFIED)**
- Pixel FX Designer — https://codemanu.itch.io/particle-fx-designer

**Tools (V-SNIP)**
- EmberGen — https://jangafx.com/software/embergen (fetched; carries no requirements) · https://www.cgchannel.com/2025/01/check-out-the-new-features-due-in-embergen-2-0/ · https://jangafx.com/roadmap
- Houdini — https://www.sidefx.com/Support/system-requirements/20.5/ · https://www.sidefx.com/community/houdini-for-apple-silicon-now-gold/ · https://www.cgchannel.com/2023/02/sidefx-releases-houdini-for-apple-silicon/
- EffekseerForGodot4 — https://github.com/effekseer/EffekseerForGodot4/releases · https://github.com/effekseer/EffekseerForGodot4
- Pixel Composer — https://github.com/Ttanasart-pt/Pixel-Composer · https://github.com/Ttanasart-pt/Pixel-Composer/issues/47 · https://pixel-composer.com/
- Juice FX — https://codemanu.itch.io/juicefx · https://itch.io/t/3319904/please-port-to-macos
- TimelineFX — https://www.rigzsoft.co.uk/timelinefx-help/
- Particle Illusion — https://borisfx.com/products/particle-illusion/ · https://www.cined.com/boris-fx-particle-illusion-free-standalone-app-for-motion-graphics-and-vfx-released-2/
- Blender — https://www.myarchitectai.com/blog/blender-system-requirements · https://docs.blender.org/manual/en/2.80/physics/smoke/index.html

**RGBA video generation (research; no hosted API found)**
- TransPixeler — https://arxiv.org/pdf/2501.03006 · https://wileewang.github.io/TransPixar/ · https://ieeexplore.ieee.org/document/11092913/
- TransVDM — https://arxiv.org/pdf/2502.19454
- Shiftable RGB-A Distribution Learner — https://arxiv.org/pdf/2509.24979
- TransText — https://arxiv.org/html/2603.17944v1

**Pipeline precedent (PRACTITIONER-REPORT)**
- https://www.vfxapprentice.com/blog/what-are-flipbooks-in-games · https://www.sidefx.com/forum/topic/43276/ · https://80.lv/articles/006sdf-vfx-production-in-houdini-ue4

**Prior findings cited, not redone (INTERNAL)**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-09-15-vfx-grammar-and-authoring-split/findings.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-09-15-video-generation-alternatives/findings.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-09-15-chronicon-com-slormancer-vfx/findings.md`

— legolas (UNKNOWN-RESEARCHER), 2026-09-15
