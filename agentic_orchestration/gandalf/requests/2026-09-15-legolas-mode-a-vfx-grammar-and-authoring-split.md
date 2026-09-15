# Legolas Mode A — ARPG skill-VFX grammars + how painted-2D games actually author effects

**From:** gandalf (SPEC-AUTHOR / ARCHITECT — VFX workflow architecture session, 2026-09-15)
**Mode:** A (analytical research; read-only; findings only)
**Findings to:** `agentic_orchestration/legolas/research/2026-09-15-vfx-grammar-and-authoring-split/findings.md`
**Host rule (binding — Mac mini 8 GB, kernel panic 2026-09-14):** NO video decoding, NO frame extraction, NO downloads > 50 MB, one fetch at a time, ≤ 1.5 GB RSS. This is a reading probe, not a sampling probe. The existing atlas at `~/Games/vendor/vfx-atlas/` and your prior findings (`2026-09-14-vfx-oracles/`, `2026-09-15-chronicon-com-slormancer-vfx/`) are in hand — cite, do not redo.

## Why

The six-kit VFX breadth test (Run C-3, ledger R-C3-123) failed on **grammar**, not register: every skill came out as one motion shape (cast → bolt → impact → residual) because the builder knows one grammar. Matt's verdict: *"they are all a variant of the same projectile — not representative of the source-material skill VFX."* Before designing the VFX architecture I need two things the corpus can answer.

## Q1 — The grammar taxonomy (what motion shapes exist, and how many cover the corpus)

Enumerate the **motion grammars** of skill VFX across the five source games we mint from (Diablo II, Grim Dawn, Path of Exile 1, Last Epoch, Hades) — a grammar = the spatial/temporal *shape* of the effect independent of element or art: e.g. projectile (single / multi / fork / pierce), orbit-emitter (D2 Frozen Orb), thrown-arc → ground field (GD Blackwater Cocktail, PoE Poisonous Concoction), chain-with-jump (D2 Chain Lightning, Hades Zeus), instant strike / smite, beam / channel, nova / ring, cone / breath, melee arc / sweep, whirlwind / spin, dash / leap-strike, ground slam / shockwave, aura / self-buff (LE Healing Hands), totem / turret, summon, trap / mine, wall, teleport / blink, DoT cloud, etc.

Deliver:
1. A **taxonomy table**: grammar → definition (phases and what moves) → 2–4 named exemplar skills per source game → the RDR engine geometry it maps to. The engine's palette lives in `~/Games/reincarnated-engine/src/reincarnated/generation/geometry_derivation.py` + `weapon_envelope_composer.py` (`melee_strike, ground_slam, chain, ricochet_bounce, dash_attack, totem, defensive_dash, blink, fork, whirlwind, leap_strike, cone, line, single_target, multi_projectile, ring, projectile, nova, beam_channel, aura, self_buff, summon, trap_mine, totem_turret, orbit, channel, melee_arc`). Report where the engine palette has NO grammar and where a common corpus grammar has NO engine geometry.
2. **Coverage estimate**: if we build N grammar templates, what share of the ~411-kit corpus's key skills is covered at N = 6, 10, 15? Use whatever skill-list evidence is cheapest (wikis, our corpus DB if readable — `agentic_orchestration/`-side, read-only). A rough count with method stated beats a precise count you cannot source.
3. For each grammar: which **phases are shared** across grammars (cast flare, impact burst, residual decal) and which are **grammar-specific** (orbit ring, arc trajectory, chain link, aura loop). This is the "primitive alphabet" question — what minimal painted-primitive set composes into every grammar.

## Q2 — The authoring split: how do painted/pixel 2D action games actually MAKE effects?

For Hades / Hades II, Children of Morta, The Slormancer, Chronicon, Dead Cells, Hyper Light Drifter, CrossCode, Eastward, Moonlighter, Sea of Stars (and any other well-documented painted or pixel action-RPG), from dev talks, postmortems, asset rips, engine data, artist interviews:

- Is an effect a **hand-drawn flipbook per effect**, a **shared primitive sheet composed at runtime** (Hades: 112 of 126 god variants share a tinted sheet — you found this), **particles + shaders**, a **3D sim / render posterised into a sheet** (Dead Cells' 3D→2D; EmberGen-posterised anime explosions), or a mix?
- Where motion comes from a **simulation or engine system** vs **drawn frame by frame** — and where the *painted register* is applied (drawn frames vs paint-over of sim frames vs runtime shader stylisation).
- What makes each game's effects read as **one language** (the coherence mechanism): shared sheets, runtime tint, a fixed layer stack, timing bands, a primitive alphabet, a single artist, a style guide. Name the mechanism per game with the source.

Deliver a table: game → authoring method → motion source → where the register is applied → coherence mechanism → source (VERIFIED / PRACTITIONER-REPORT / INFERRED per your usual classes).

## Q3 — One paragraph each: what the corpus says about our two live hypotheses

- H-A: *"Grammar belongs in the runtime (templates that move painted primitives), not in the sheet."*
- H-B: *"A painted-2D ARPG can keep one register across 15+ grammars with a primitive alphabet of ≤ ~12 painted shapes per element, tinted at runtime."*

Support, refute, or bound each from what you find. Bound the alphabet size if any game's data lets you count it (Hades `Fx.sjson` is in hand).

## Fences

Read-only; no game installs; no purchases; no account creation; classify every claim (VERIFIED / PRACTITIONER-REPORT / INFERRED); list gaps and blocked pages. Budget ~40 min. File findings and stop.

— gandalf, 2026-09-15
