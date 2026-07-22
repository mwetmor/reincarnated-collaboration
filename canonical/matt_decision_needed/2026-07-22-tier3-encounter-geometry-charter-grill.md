# Tier-3 Encounter-Geometry — Charter Elicitation Grill (R5 = BEGIN)

> **STATUS:** ⚡ RULINGS RECEIVED 2026-07-22 same-day — **F2 ✓ RULED (gamora + drax-sequencing rider) · F3 ✓ RULED (all three, Q38 frame) · F1 lean ADOPTED + two Matt-riders, folded in § THE F1 FOLD — ONE confirm pending on the folded shape.** T3-F4 gate v0 drafted below. **Queue row Q41.**
> **Authority:** Q40 ruling sheet R5 = *"BEGIN = ELICITOR charter session with me present."* This sheet is the durable grill surface for that session — rule async here or live in-session; either lands the same.
> **Author:** gandalf (ELICITOR) · 2026-07-22
> **Discipline:** desirable-run-pattern § 3 — a Tier-3 run cannot charter without a **decidable target-state**. These three forks ARE the target-state definition. ELICIT, don't impose: leans stated, Matt rules.

**▶ ROLE: ELICITOR — draining the unmade decisions out of "Tier-3 encounter-geometry" before any charter is drafted.**

---

## What Tier-3 is (one paragraph of shared ground)

The kit corpus (574 real kits; 267 record-class with full v2.0 six-block geometry data) describes what builds DO. Nothing yet describes what they do it TO — the encounter side: arena shapes, mob formations, pressure patterns, the geometry a kit's bands collide with. Tier-3 is the run that gives the project an encounter-geometry layer. D2's pit runs vs Baal waves, PoE's breach-circles vs ritual-rings, Last Epoch's monolith arenas — every ARPG that respects its kits builds encounter geometry that STRESSES them differently. We have the kit half; Tier-3 builds the collision half.

---

## T3-F1 — What is the run's PRODUCT? (the decidable target-state)

| Option | What ships | Decidability | Tradeoff |
|---|---|---|---|
| **(a) Encounter-grammar spec** | A design vocabulary: arena archetypes, formation grammars, pressure patterns (named, typed, parameterized) | Weak alone — a vocabulary can't FAIL | Fast; pure design doc; but an undecidable product violates the run pattern |
| **(b) Kit→encounter fit layer** | A computable mapping: given a kit's geometry bands, which encounter geometries stress vs showcase it — emitted as data | Strong — the mapping either discriminates or it doesn't | Needs (a)'s vocabulary as substrate; larger |
| **(c) Walls prereg** | A pre-registered sim experiment: encounter variants vs kit sample, effect sizes asserted | Strongest per-experiment | Narrowest; proves discrimination without shipping the layer |

**Lean: (a) as intermediate → (b) as the decidable product.** The grammar spec is Leg-1 scaffolding, not the deliverable; the run CLOSES on the fit layer discriminating. (c)'s experiment shape becomes the gate (see T3-F4), not the product.

**— Matt's word (2026-07-22): lean ADOPTED, with two riders —** (1) *"Would it make sense to marry this to the roguelite run structure (act of a run = era/age; fit the encounter-grammar to the kits of that era/age)?"* (2) *"Do any grammars lean toward potential areas of a map — e.g., the centralized multi-faction melee area or the de-centralized faction outpost area?"* → Both folded into **§ THE F1 FOLD** below; one confirm pends on the folded shape.

## T3-F2 — Who is the FIRST CONSUMER? (routes the output format)

| Option | Consumes as | Consequence |
|---|---|---|
| **gamora (sim)** | Encounter specs become sim scenarios; fit-layer claims become effect-size asserts | Falsifiable immediately; output = machine-readable scenario data |
| **drax (Godot floors)** | Grammar feeds level-authoring (crypt/ravine grammar) | Player-visible soonest; but claims stay unfalsified until playtest |
| **Q11 gauntlet** | Encounter variants slot into the gauntlet harness | Reuses built harness; narrower coverage |

**Lean: gamora.** Sim-falsifiable first; drax inherits a VALIDATED grammar rather than a speculative one. (Matches engine-first orientation: prove the layer against the sim before it shapes floors.)

**— Matt's word (2026-07-22): RULED — gamora.** Sequencing rider registered: *"Drax cannot engage until something emits from the serial content pipeline via JSON. Then we build out the demo with the emitted modular roster (kits → mapped gear, monsters → mapped factions, biome/tileset → faction morph)."* Consumer chain therefore: **gamora falsifies → serial-content JSON emission → drax modular roster.** Tier-3's fit-layer output format must be emission-compatible with `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` from day one — the fit layer is a future JSON block, not a design-doc-only artifact.

## T3-F3 — What SUBSTRATE feeds it? (bounded substrate, per the run pattern)

| Option | In | Cost |
|---|---|---|
| **record-267 six-block** | gb_* geometry bands as the kit half | Free — landed in VDM-2 Leg A |
| **+ mob-harvest** | New capture: genre mob-formation/arena data (D2/PoE/GD/LE encounter shapes) | New legolas/elrond harvest lane — the only NEW collection |
| **+ Q38 biome-morph frame** | k=5 element-courts + eras-as-shelves + biome-morph rider as the encounter-side organizing frame | Free — already ruled (Q38); using it keeps encounter vocabulary congruent with kit vocabulary |

**Lean: all three, Q38 as the frame.** The kit half exists; the mob-harvest is the run's genuine collection cost; Q38 keeps the two halves speaking one language. (Sizing note: mob-harvest scope gets its own bound in the charter — it is the substrate risk.)

**— Matt's word (2026-07-22): RULED — all three, Q38 as frame.** F1's era rider stratifies the mob-harvest by era/age shelf (per-era collection bounds go in the charter).

## THE F1 FOLD — Matt's two riders, folded (2026-07-22; confirm pending)

**Folded product shape: the fit layer is ERA-INDEXED and the grammar is TIERED.**

1. **Era-act marriage (rider 1 — ADOPTED into the fold).** The roguelite run structure (act = era/age) becomes the fit layer's indexing spine: `fit(kit, encounter | era)`. Q38 already ruled eras-as-shelves on the kit side — this makes the encounter side speak the same coordinate. Three concrete wins: (i) the mob-harvest gets per-era strata (bounded substrate, tractable collection); (ii) the decidability gate sharpens — showcase/stress claims are tested per-era, not corpus-global; (iii) an act's encounter deck IS its era's grammar subset — the fit layer feeds run-generation directly. Genre precedent: Hades' act-biomes each carry their own encounter grammar and the same build plays differently per act; D2's acts carry distinct pressure signatures (Act-2 swarm+ranged-burst beetles/mummies vs Act-4 curse-pressure oblivion knights). **One named caution:** era-conditioning states what encounters SUIT an era's kits — it must NOT silently become kit-availability gating. Availability is progression design (the §1.6 scaling-curve lane, jack-ryan Gate-1 per R6), not Tier-3's to decide.
2. **Map-area archetypes (rider 2 — ADOPTED as the grammar's MACRO tier).** The grammar is three-tiered: **MACRO-topology** (map-area archetype: hub-brawl / outpost-lattice / corridor-gauntlet / siege-line, …) → **MESO-formation** (mob formations within an area: swarm ring, ranged crescent, elite+retinue) → **MICRO-pressure** (per-pack timing/spacing). Matt's two examples are genuinely distinct macro archetypes with opposite pressure grammars: *centralized multi-faction melee* (converging pressure, faction crossfire, player-as-third-party — D2 Travincal council brawl, GD three-way faction fights) vs *decentralized faction outposts* (sweep-and-clear, approach-vector choice, pull discipline — D2 Pit/seal-pop patterns, GD nemesis outposts, PoE expedition placement). **Faction-composition is a macro-tier PARAMETER** (mono-faction outpost vs multi-faction contested) — which plugs straight into the F2 modular roster (monsters → mapped factions; biome/tileset → faction morph). Falsifiability split: MESO/MICRO claims are gamora-sim-testable now; MACRO claims become fully testable when drax floors consume — so the T3-F4 gate binds on meso/micro, and macro ships as parameterized grammar with sim-proxy checks (spawn-topology effects on pressure metrics).

**Confirm wanted (one word):** F1 = era-indexed fit layer + three-tier grammar (macro/meso/micro) with faction-composition as a macro parameter — the run CLOSES on the fit layer discriminating at meso/micro per-era. On confirm, the charter drafts.

## T3-F4 — Decidability gate v0 (DRAFTED, per the folded F1; finalized at prereg)

For **each era shelf**: a stratified record-class kit sample (floor n≥8 per era, courts represented) runs in sim against (i) its fit-layer-matched **SHOWCASE** encounter, (ii) its matched **STRESS** encounter, (iii) a **neutral arena** baseline. Pre-registered claims: showcase beats neutral on the kit's declared showcase metrics (declared per register — e.g., sustain-uptime for channel kits, burst-window kill-time for strikers) by effect size ≥ X; stress trails neutral by ≥ X in the opposite direction; direction-consistency ≥ Y% of the sample. **X and Y are set at prereg from gamora baseline variance data (Discipline #18 — methodology AFTER baseline), not guessed here.** Fallback envelope §8-C-style, pre-committed: if the fit layer discriminates corpus-global but fails per-era (or vice versa), the fit layer is NOT served; the grammar spec still lands as scaffolding and the failure mode is named in the review book. Gate text goes to jack-ryan Gate-1 with the charter.

---

**Next beat:** Matt's one-word confirm on THE F1 FOLD → charter drafts (conductor: gandalf RUN-CONDUCTOR per desirable-run-pattern § 3 fit test, confirmed at charter time) → prereg (X/Y set on gamora baselines) → jack-ryan Gate-1 → run. Island re-cut + naming stays gated behind Tier-3 completion AND R1 resolution per the Q40 §5 re-anchor proposal.
