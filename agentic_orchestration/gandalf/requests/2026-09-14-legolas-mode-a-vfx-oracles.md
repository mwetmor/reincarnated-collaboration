# Legolas Mode A — oracles for VFX: generation process and outcome, in the H1 painted-2D register

> **STATUS:** CURRENT — research commission, gandalf (RUN-CONDUCTOR, Run C-3 → VFX lane). Matt 2026-09-14: *"move back to VFX … send out a Legolas research probe and ultra think through where we can find an oracle(s) for VFX generation process and outcome in our register and style."* Context ruling R-C3-88: every library VFX set (Gigapack, CreativeKind) was judged "none of them any good"; our own VFX system is the path.

## 0. What an "oracle" means here (so the probe returns the right shape)
An oracle is a **source of truth we can check our VFX against**, in two kinds:
- **OUTCOME oracle** — what a finished effect in our register *is*, stated as numbers we can measure on our own frames (closed-form where possible), plus the few judgement axes that cannot be closed-form. Precedent: the Hades run-speed finding (3.9 body-heights/s measured from footage, cross-checked against shipped data) and the R10 walk/idle cycle oracle.
- **PROCESS oracle** — how shipped games in (or next to) our register actually *make* effects: authoring medium, layers, frame counts and rates, blend modes, what is hand-drawn vs particle vs shader, how directionality and readability are achieved. It tells us which generation route can hit the outcome oracle at all.

Our register and camera: **H1** (hand-drawn painted 2D, tapered dark contour, painted planes, restrained texture; `canonical/reap-die-rise-story/style-register.md` § H1) with the **Hades dialect** allowed in levels (jewel tones, graphic shapes); ARPG camera (~45–53° elevated ¾), Keeper 130 px tall at 1080p (12.5 %); Godot 4.6 2D (Sprite2D / AnimatedSprite2D / CPUParticles2D / CanvasItem shaders). Existing canon is 3D-oriented: `canonical/reap-die-rise-engine/vfx-pipeline.md` (Diablo 3 layered-noise, alpha composite) — carry over only what survives 2D painted.

## 1. Threads
**T1 — PROCESS precedents (shipped painted / hand-drawn 2D action games).** For each: Hades + Hades II (Supergiant; Jen Zee interviews; GDC/Noclip; shipped data files — look for FX / Animation / Particle definition files in the public mod-tutorial repos already used: frame counts, PlaySpeed, blend, scale, "Fx" entries per god boon), Transistor/Pyre, Hollow Knight/Silksong, Cuphead, Children of Morta, Dead Cells (3D→2D pipeline), Sea of Stars, Eastward, Hyper Light Drifter, Skul, Diablo II (pre-rendered sprite FX). Extract: authoring medium, layer breakdown (core / body / edge / sparks / ground decal / light), frames and fps (on 1s/2s/3s?), blend mode (additive / alpha / premultiplied), whether FX carry contour lines, shape language, element palettes, directional handling (8/16/32 directions? rotation?), and what is procedural.

**T2 — PRINCIPLES canon for hand-drawn FX.** Joseph Gilland, *Elemental Magic* I & II (Disney FX animator — fire, water, smoke, magic, energy design rules, timing, dissipation); anime FX lineage (Yoshinori Kanada "Kanada effects", Norio Matsumoto, sakuga FX timing on 2s/3s, smear frames); Riot VFX readability / style-guide talks; Overwatch and Hi-Fi Rush stylised FX talks; Guilty Gear Xrd stepped animation; Simon Trümpler / Gabriel Aguiar stylised VFX; realtimevfx.com community rules of thumb (anticipation → peak → dissipation ratios, value grouping, silhouette first). Return the rules as **testable statements** where possible.

**T3 — OUTCOME measurement from footage (the core of the oracle).** Pick 4–6 exemplar effects: Hades (e.g. a Zeus lightning boon hit, a Poseidon splash, the Cast/Bloodstone projectile + impact, an Artemis crit) and Hades II (a Melinoë Omega cast), plus one ARPG-language effect in the D2R/Grim Dawn neighbourhood for contrast. From 1080p footage (YouTube was bot-blocked last session — Twitch VODs / Dailymotion worked) measure per effect, in scale-free units against the character's body height where relevant:
- phase timing: anticipation / peak / dissipation frame counts @ source fps (and whether animated on 1s/2s);
- peak extent (body-heights), projectile travel speed (body-heights/s), impact radius;
- value structure: number of discrete value bands at peak, core luminance, edge luminance; presence of a dark contour or not;
- hue spread per element (HSV bands), saturation of core vs edge;
- area-over-time and luminance-over-time curves (normalised), flash frames;
- secondary layers: ground decal, light spill on floor, screen shake, hit-stop frames.
Same evidence discipline as the speed probes: VERIFIED / MEASURED (method) / DERIVED / PRACTITIONER-REPORT; every run of numbers with its source and timestamp. **Footage is for measurement only — never used as an image-model reference; delete downloads afterwards.**

**T4 — GENERATION-route oracle for OUR tools.** What evidence exists for each candidate route hitting a hand-drawn FX look: (a) GPT-image-class painted flipbook sheets (frame consistency with no seed; grain-scale mismatch across canvases — see `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md` § 1.5); (b) painted keyframes + image-to-video tweening (Grok i2v) for FX; (c) procedural Godot 2D: CanvasItem shaders with posterised/stepped noise, animate-on-2s, toon ramps, painted shape masks + scrolling textures, CPUParticles2D with painted sprites (precedents: stylised/toon real-time FX that read as hand-drawn); (d) hybrids (painted silhouettes per phase + shader motion). For each: what it is good/bad at against the T3 measures, and precedent.

**T5 — Internal corpus (read, summarise what carries to 2D H1).** `canonical/reap-die-rise-engine/vfx-pipeline.md`; `agentic_orchestration/research/vfx-p2-dossiers/`; the Godot MCP particle bake-off learnings (search `agentic_orchestration/` for "bake-off"); Run C-3 frost-bolt history (ledger `astra_test_01/burst/runs/C-3/ledger.json` R-C3-19/28–31/38/81/88; K4v-gen frost sheets judged non-directional; library sets rejected); `canonical/matt_decision_needed/` VFX items.

## 2. Deliverable (return as text; gandalf files it at `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md`)
1. **TL;DR** — the recommended oracle stack: which OUTCOME measures (closed-form) + which JUDGE axes + which PROCESS precedent, and the recommended exemplar set.
2. **Oracle table** — measure · definition · closed-form? · reference value(s) from T3 with evidence class · source.
3. **Process table** — game · medium · layers · frames/fps · blend · contour? · directionality · source.
4. **Principles** as testable rules (T2).
5. **Route assessment** (T4) — per route: fit to the oracle, risks, precedent, cheapest first experiment.
6. **Gaps** — what could not be sourced or measured, stated plainly.
Budget: be efficient; prefer primary sources and first-hand measurement over recall; never substitute recalled numbers for blocked routes.

— gandalf, 2026-09-14
