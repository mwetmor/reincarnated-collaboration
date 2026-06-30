# Reap. Die. Rise. — Performance, Target Specs & Density Benchmarks (Technical Reference)

**Project:** Reap. Die. Rise. (ARPG)
**Document:** Engine performance characteristics, target hardware tiers, horde architecture, VFX/lighting budgets, profiling discipline, and competitive on-screen monster-density benchmarks
**Status:** Technical reference — companion to the gameplay-loop design doc
**Audience:** Claude implementation/optimization team
**Engine:** Godot 4.x · **Assets:** Synty (low-poly modular) · **VFX:** Binbun Godot Effects Collection (native Godot 4.x GPU particles) · **Platform:** Steam (Windows primary, Mac/Linux secondary)

---

## 0. The one principle that governs everything

**For a horde ARPG in Godot 4, the binding constraint is CPU-side entity simulation (physics + AI), NOT the GPU or the art assets.**

Synty's low-poly geometry and Binbun's GPU particles are the *cheap* parts — any modern GPU draws them trivially. The expensive part is *simulating* hundreds of enemies: collision resolution, steering, and AI update loops, which run on the CPU. This inverts the intuitive worry ("can the hardware render all this?") — the hardware can almost always *render* it; the question is whether the *architecture* can *simulate* it.

Concrete evidence of the trap: built the naive way (each enemy a full `CharacterBody3D` physics node on the default GodotPhysics backend), documented community benchmarks show **sub-15 FPS at roughly 50 enemies** — and worse, performance degrading after as few as 10–40 instances in some cases. That is *nowhere near* ARPG horde density, and it has *nothing to do with the player's GPU*. It is the engine doing per-node collision and steering on the CPU.

The corollary, which is the good news: the *ceiling* in Godot is very high (tens of thousands of units) **if and only if** the entity architecture is built for it. The gap between "50 enemies tanks the game" and "20,000 enemies run fine" is **entirely implementation**, not hardware. Therefore the most important decisions in this document are architectural (§2), not hardware-purchasing.

---

## 1. Renderer decision: Forward+ (locked)

Godot 4 offers three renderers. For this project the choice is effectively forced.

**Use Forward+.** It is the default for desktop, a clustered forward renderer with the full feature set, and critically it **handles many dynamic lights and complex shading efficiently** — which is exactly what the *atmospheric-dark* art direction needs (volumetric fog, low-key directional shadows, many shadow-casting lights are where the game's "grit" is born, per the art-direction decision). Forward+ requires **Vulkan or Direct3D 12**, which sets the hardware floor (see §3) — essentially any GPU from roughly the last eight years.

**Do NOT use Compatibility — there is a project-killing gotcha for this game.** The Compatibility renderer (OpenGL 3.3, broadest hardware reach) causes **`GPUParticles3D` to silently fall back to CPU simulation**. Binbun's effects are GPU particles; running them CPU-side at horde scale would be catastrophic for performance. Compatibility is therefore off the table for a VFX-heavy ARPG. (Compatibility is also required for Web export, which is not a target.)

**Mobile renderer** is not applicable (it targets tile-based mobile GPUs; this is a desktop title).

**Operational note:** ensure the project is on Forward+ in the editor as well, because some performance symptoms (e.g. VFX hitches) can be caused or masked by accidentally running a scene under the wrong renderer. Shaders are not portable between the RenderingDevice renderers (Forward+/Mobile) and Compatibility, so renderer choice should be made once and held.

---

## 2. Horde architecture mandate (decide BEFORE building combat)

This is the single most important technical decision, and it must be made *before* the combat layer is built, because retrofitting it later is a rewrite. It connects directly to the enemy-ontology design (fodder hordes vs. named champions): **the fodder MUST be MultiMesh-class, not individual physics nodes.**

**The hybrid model:**

- **Player + named champions (lieutenants, mega-boss):** full `CharacterBody3D` nodes — they need real collision, navigation, and individuated behavior. There are few of them at once, so the per-node cost is affordable.
- **Monster fodder (the horde):** `MultiMeshInstance3D` — renders thousands in a *single draw call*; you control each transform from a loop and write movement/state logic manually (no free collision/pathfinding). This is mandatory for the fodder, because fodder is exactly "things that exist in large numbers."
- **Extreme counts (thousands+):** drop to the `RenderingServer` / `PhysicsServer3D` APIs directly, bypassing the scene tree. Harder to debug and not editor-visualizable, but the documented path for "dozens of thousands of instances."

**Use Jolt physics, not the default GodotPhysics.** Documented benchmarks show Jolt provides roughly **20× more headroom** for `CharacterBody3D` instances (~800 before degradation vs. ~50 on GodotPhysics). Even with the MultiMesh fodder approach, the named-champion bodies and any physics interactions benefit enormously. (Jolt is available in Godot 4.4+.)

**CPU-side scaling ladder (documented community thresholds, approximate):**

- **Up to ~hundreds of MultiMesh units:** rendering is cheap; the movement/AI loop is the cost. Manageable in GDScript with care.
- **~5,000 units:** GDScript becomes the bottleneck. Move hot loops (movement, targeting) to **C# or GDExtension**.
- **~10,000+ units:** CPU update cost dominates. Use **spatial partitioning**, **stagger updates across frames** (e.g. update 1/4 of units per frame), and **skip off-screen units**. Community accounts of 20,000-unit battles confirm this works with careful optimization.

**Bottom line for this game:** because the design calls for dense fodder hordes plus a handful of named champions, the architecture is non-negotiable — Jolt + MultiMesh hybrid, with staggered/culled updates, escalating to the servers API if pushing into the thousands. Get this right and a *minimum-spec* GPU runs the horde; get it wrong and a top-end GPU chugs at 50 enemies.

---

## 3. Competitive on-screen monster-density benchmarks

**Critical caveat — read first.** None of these studios publish exact on-screen monster caps. Every figure below is a **bounded estimate** derived from community observation, mechanics inference, gameplay footage, and the pattern of performance-complaint threads — **not** an official specification. Numbers describe *roughly how many hostile units are simultaneously visible/active in the densest endgame moments*, which is the quantity that matters for our architecture (§2). Treat them as order-of-magnitude reference points, not precise targets.

These benchmarks exist for one reason: to **calibrate where the density ceiling lives in the genre**, so Reap. Die. Rise. can deliberately choose a target (see §5) rather than guess.

### Per-game estimates (densest endgame moments)

**Diablo II / D2: Resurrected — roughly 30–80 on screen; bursts higher in chokepoints.**
The oldest engine and the most *intrinsically* constrained. Monsters spawn in groups; champion packs spawn in clusters of ~4–5; unique monsters bring several minions. Classic high-density spots (e.g. Baal-run waves, Chaos Sanctuary, cow level) push the upper end, but the engine and design keep simultaneous active counts modest by modern standards. The densest "feel" comes from tight chokepoints concentrating a moderate count, not from huge absolute numbers. Player-count scaling (`/playersX`) increases monster *stats and drops*, not the spawn *count*. Estimate: **tens, peaking under ~100.**

**Diablo III — roughly 50–150; built around larger packs and Rift density.**
D3 deliberately raised pack sizes and introduced Greater Rifts tuned for high-density "pull and detonate" gameplay. Density-pylon Rifts and large pulls are the peak. Estimate: **mid-double-digits to low-hundreds.**

**Diablo IV — roughly 50–150+ in Helltides/Infernal Hordes; engine visibly strains at the top.**
D4 is a modern, well-optimized engine, but on-screen density is *deliberately bounded*, and community reports document **stutter when surrounded by very large exploding-enemy swarms** (e.g. spiders splitting into more spiders) and in large group events. Infernal Hordes (wave-survival) and Helltides are the densest content; high-density builds explicitly scale damage off pack size. The strain reports indicate D4 sits near a practical ceiling for its engine in those moments. Estimate: **low-hundreds at peak, with visible cost.**

**Path of Exile 1 — roughly 100–300+, the genre's high-water mark for juiced density.**
POE1's juiced endgame is the canonical "screen full of monsters" experience. Mechanics like Breach, Legion, Delirium, and Abyss flood the screen, and stacked together they push simultaneous active counts to the **hundreds**, with extreme stacked-mechanic moments going higher. This density is also a **franchise-wide performance pain point** — POE1 stutters and frame-drops in heavily juiced content *even on high-end Windows hardware*, because of its aging, CPU-heavy custom engine. Estimate: **low-to-mid hundreds typical when juiced; higher in stacked extremes — with real performance cost even on strong machines.**

**Path of Exile 2 — high but engine-managed; explicitly tuned/nerfed for density.**
POE2's Breach floods an expanding circle with "hordes" of monsters (swarms of whites plus many magic/rare). Notably, GGG **reduced monster density ~40% in a major patch** while preserving the juiced *feel*, indicating active management of simultaneous counts for performance/balance. Breach circles are the densest case. Estimate: **comparable to POE1's juiced range at peak (low hundreds), but more deliberately bounded.**

**Last Epoch — roughly 50–150; dense but lighter than POE.**
Positioned as a middle ground between D4 and POE. Endgame (Monoliths, high corruption) produces large packs and dense waves, but typically does not reach POE's juiced extremes, and as a smaller-studio engine it does not court the absolute top of the density range. Estimate: **mid-double-digits to low-hundreds.**

### The pattern that matters for us

| Game | Densest-moment estimate | Engine headroom at that density |
|---|---|---|
| Diablo II / D2R | ~30–80 (peaks <100) | Comfortable (low counts by design) |
| Diablo III | ~50–150 | Comfortable |
| Diablo IV | ~50–150+ | Near practical ceiling; documented strain |
| Path of Exile 1 | ~100–300+ (juiced) | **Strains even high-end HW** (legacy engine) |
| Path of Exile 2 | ~100–250 (juiced, ~40% nerfed) | Actively managed/bounded |
| Last Epoch | ~50–150 | Comfortable |

**Read:** the genre's *comfortable* density band is roughly **50–150 simultaneous hostiles**. The genre's *extreme* band (POE-juiced) is **a few hundred** — and that band is exactly where even mainstream engines visibly strain. The extremes are reached by *deliberately stacked endgame mechanics*, not baseline gameplay.

---

## 4. Target hardware tiers (Steam, 2026 data)

The current Steam population is dominated by *aging mid-range Nvidia* — roughly 60% of users own an RTX GPU, and the RTX 30/40 series together are the backbone (the RTX 3060 is the single most common GPU). This is favorable: targets are modest, and the Forward+ floor (Vulkan/DX12) covers the overwhelming majority of users.

**Minimum spec (the floor): GTX 1650 / RTX 3050 — target 1080p / 60 FPS.**
These are the most common *low-end* cards and remain persistent because they handle less-demanding games well. For a low-poly Synty ARPG they handle geometry easily; the only thing that troubles them is *uncapped* horde particle/light counts — a settings problem (§6), not a "this GPU can't run it" problem. No ray tracing (not used here anyway). **This is the tier to certify against.**

**Recommended spec (where the plurality of players are): RTX 3060 — target 1080p high / 1440p 60.**
The most common GPU on Steam, with comfortable headroom for full horde density, full lighting, and full Binbun VFX. Most players sit here or near here.

**High tier: RTX 4070 and up — 1440p high-refresh / 4K.**
The most common high-end card is the RTX 4070; the RTX 50 series is accumulating share slowly. These run anything; the only work here is *offering* high-resolution and high-refresh options, not optimizing for them.

**Steam Deck (stretch target + real market):** Linux/Vulkan, thermally constrained, roughly RTX-3050-class in raw terms. If the GTX-1650/RTX-3050 floor is hit cleanly, Deck playability is within reach — and a run-based ARPG is a natural handheld fit, so the Deck is worth treating as a genuine target.

**Below the floor (likely not supported):** integrated graphics (Intel Iris Xe) and the GTX 1050 ("potato" tier) are small slices. A VFX-heavy horde ARPG is a reasonable place to *not* support the absolute bottom, though efficient horde architecture *might* reach Iris Xe at low settings.

**Net:** with Forward+ and a properly architected horde, the *effective* minimum spec is "almost any Vulkan/DX12 GPU from the last ~8 years," which covers the vast majority of the Steam population. **The hardware is not the risk; the architecture (§2) and the effect budgets (§6) are.**

---

## 5. Density design rule: target the comfortable band, treat juiced-endgame as the anti-target

Combining §3 (where genre density lives) with §0/§2 (the architecture reality):

**Target the genre's *comfortable* density band — roughly 50–150 simultaneous hostiles — as the design baseline, and treat the POE-juiced *extreme* band (a few hundred) as an explicit anti-target.** Rationale:

1. **The extreme band strains even high-end hardware on legacy ARPG engines** (POE1's juiced-content stutter is franchise-wide, not a hardware-tier failure). Reproducing that density is reproducing a known problem.
2. **Unlike those games, this project controls its own density and effect budget.** The enemy-ontology design (fodder hordes + named champions) lets the horde fantasy *feel* dense at a count the architecture (§2) and the minimum-spec floor (§4) comfortably handle. With proper MultiMesh fodder, even the *upper* comfortable band (~150) is very achievable — and *feels* like a screen full of enemies — without courting the extreme band's cost.
3. **The "power fantasy of mowing down a horde" does not require POE-juiced counts.** D2 delivered an iconic horde feel at *under 100* on screen. Density *feel* is driven as much by clustering, effects, and pacing as by raw count.

**The rule:** design the horde power-fantasy to live in the **50–150 comfortable band**, with MultiMesh fodder making it *feel* dense; deliberately do *not* reproduce POE-juiced extremes (a few hundred+). This keeps minimum-spec players smooth, keeps the development machine smooth, and is *more* achievable with Godot + Synty + Binbun than the extreme count is on a legacy engine.

**[OPEN — measure, do not assume]** The *specific* peak target number within the comfortable band is a decision to make against profiling data on the minimum-spec floor (§6), not to guess. §3 gives the genre band; the exact figure falls out of worst-case profiling.

---

## 6. VFX & lighting budget discipline

Binbun's effects are native Godot 4.x GPU particles — a good fit precisely *because* they belong in Godot's `GPUParticles` system and run on the GPU under Forward+ (see the §1 Compatibility warning). The danger is not any single effect; it is **many concurrent effects and dynamic lights at once**, especially in dense moments (a packed fight, a ritual-dense area).

**Required disciplines (most of these are needed for minimum-spec players regardless, so this is not extra work — it is the work):**

- **Pool and cap concurrent VFX.** A dense moment must not be able to instantiate dozens of effects in a single frame. Use an object pool and a hard cap on simultaneous active effects.
- **Particle LOD.** Fewer particles (or simpler effects) at distance; full detail only up close. Cull off-screen emitters.
- **Cap simultaneous shadow-casting dynamic lights.** This is the single most expensive common thing in a Forward+ scene. Lights themselves are cheap-ish; *shadow-casting* lights are not. A dark, ritualistic, candle-and-fire-lit aesthetic will be tempted toward many shadow-casting lights — budget them hard.
- **Stagger VFX activation.** Do not trigger many effects on the same frame an encounter begins or the camera arrives; spread activation across frames.
- **Shader pre-warming.** Godot compiles shaders lazily — the *first* appearance of a material/particle/effect can cause a multi-second stall. Pre-render effects once off-screen during a loading screen so first-encounter compilation does not hitch mid-play. (Far milder in exported builds with caching; still worth doing.)

**Settings architecture — what scales vs. what is fixed.** This is how *one* game serves the whole tier range from §4:

- **Scales with the graphics-settings tier (visual only):** particle density, shadow resolution, shadow-casting light count, anti-aliasing, render resolution, effect complexity. The minimum-spec player turns these down; the high-tier player turns them up.
- **Stays fixed across all tiers (gameplay-critical):** horde count, combat behavior, enemy AI, encounter design. These must NOT scale with hardware, or the game plays differently on different machines (a fairness and design-integrity problem). The *number of enemies* and *how the fight works* are identical everywhere; only the *visual richness* of rendering them changes. (This directly protects the Goldilocks encounter tuning and difficulty balance.)

---

## 7. Profiling discipline

- **Profile an EXPORTED build, not the editor.** The editor adds significant per-frame overhead (gizmos, selection, live inspector sync, undo tracking), so editor performance is misleading. Methods that look expensive in the editor may be fine in the export, and vice versa. Export a debug build and connect the remote profiler for accurate numbers.
- **Define the target before measuring:** e.g. "60 FPS on minimum-spec (GTX 1650 / RTX 3050) at 1080p, with the peak comfortable-band horde count from §5."
- **Profile the worst-case scene:** maximum horde + maximum concurrent VFX + a mega-boss, in one place. The heaviest moment defines the spec floor; know it from month one, not at launch.
- **Read the profiler to localize the bottleneck:** spikes in **Process / Physics** indicate CPU-side cost (entity update loops, or — a red flag — GPU particles falling back to CPU). Spikes on the **render thread** indicate draw calls, lights, or shader compilation. This tells you *which* fix from §2/§6 applies.
- **Certify the floor on real minimum-spec Windows hardware (or a Steam Deck).** Development machines — especially capable ones, and *especially* Apple Silicon with unified memory and the Metal backend — *flatter* performance: they can hide discrete-GPU VRAM limits, PCIe-transfer costs, and Vulkan-path behavior that surface on a real GTX 1650. A dev machine running smoothly does NOT certify minimum-spec. Get a cheap GTX-1650/RTX-3050 Windows box (or lean on a Steam Deck, which is Linux/Vulkan and close to the floor) as the actual minimum-spec gate. Mac/Linux are secondary Steam audiences worth their own build validation, but they are not substitutes for Windows minimum-spec testing because the rendering backend and memory architecture differ.

---

## 8. Editor freezes & frustum-entry spikes (general guidance)

A common and *usually benign* symptom: the editor (or game) hitches/freezes when the camera moves quickly into a spot dense with assets and VFX. Diagnosis matters, because the cause determines whether it can be ignored.

**Key reframe: an Editor-viewport freeze is NOT the same as an exported-game freeze.** The editor's per-frame overhead means a dense-spot hitch is frequently the *editor* choking, not the *scene* being unrenderable. Players never run the editor, so an editor-only hitch is largely ignorable.

**The "freezes only on fast traversal into a dense spot" signature is diagnostic — and it's the *reassuring* version.** If a spot were simply too heavy to render at all, it would hitch when you *sit* in it, not only when you *fly into* it. "Hitches on fast entry" is the classic signature of *too much becoming visible in one frame* — a transient spike, which is the *addressable* kind, not a steady-state scene-weight problem.

**Most likely causes (in order):**
1. **Many GPU particle systems entering the frustum simultaneously** — multiple effects becoming visible in one frame spike hard (worse if any are mis-running on CPU; re-check the renderer is Forward+, §1).
2. **Shader-compilation hitch** — first-time appearance of new effects compiles their shaders in one frame. Tell: hitches the *first* pass, smoother the *second* (shaders now cached). Fix: shader pre-warming (§6); much milder in cached exported builds.
3. **Draw-call / shadow-light explosion at that spot** — many shadow-casting lights entering view at once (likely in a VFX-dense ritual area). This one *can* affect runtime; isolate it.

**Diagnostic ladder:** (1) export a build and fly through the same spot — if it's smooth in-build, it's editor overhead, ignore it; (2) if it hitches in-build, check first-pass-only (→ shader compilation) vs. every-pass (→ genuine density); (3) profiler at that exact spot on the exported build (Process/Physics vs. render-thread, per §7).

**Fixes** are the same density-spike disciplines already required for minimum-spec (§6): pool/cap/stagger VFX, pre-warm shaders, cap shadow-casting lights, particle LOD/culling. An editor freeze on fast traversal is best read as an *early warning* of the VFX-spike discipline the project needs anyway.

---

## 9. Decisions to lock before building the combat & VFX layers

1. **Renderer = Forward+** (§1). Not Compatibility (GPU-particle CPU-fallback), not Mobile.
2. **Enemy architecture = Jolt + MultiMesh hybrid** (§2): full `CharacterBody3D` (Jolt) for player + named champions; `MultiMeshInstance3D` for fodder; servers API for thousands; C#/GDExtension for hot loops past ~5k; staggered/culled updates past ~10k. **Decide this before combat is built.**
3. **Density target = the 50–150 comfortable band** (§3, §5); MultiMesh fodder makes it *feel* dense; deliberately do NOT reproduce POE-juiced extremes (a few hundred+). Exact peak number measured against the floor, not assumed.
4. **Minimum spec = GTX 1650 / RTX 3050 @ 1080p/60** (§4); recommended = RTX 3060; Steam Deck as a stretch target.
5. **Scalable VFX/light settings from day one** (§6): particle density, shadow resolution, shadow-light count, AA, resolution all scale; horde count and combat behavior stay fixed across tiers.
6. **Profile exported builds on real minimum-spec hardware** (§7): worst-case scene (max horde + max VFX + mega-boss); a capable dev machine does not certify the floor.

---

## Appendix: density-benchmark sourcing note

The §3 figures are bounded estimates, not published specs — no studio in this set discloses exact simultaneous on-screen monster caps. They were triangulated from: community gameplay observation and footage; mechanics documentation (pack sizes, spawn behaviors, league/endgame mechanics like Breach/Legion/Delirium/Infernal Hordes); patch-note evidence of deliberate density management (e.g. POE2's ~40% density reduction); and the pattern of performance-complaint threads indicating where each engine strains. They are intended as **order-of-magnitude calibration** for density design (§5), and should be revised if better-instrumented data becomes available. Do not cite these as authoritative counts.
