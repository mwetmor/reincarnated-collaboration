# Combat Temporal Decoupling — telegraph geometry (sim) vs dodging (game), and the glass-close-ST coordinate-survivability ruling

> **STATUS:** CURRENT (load-bearing as of 2026-06-15) — see `canonical/00-ground-state.md`

**Date:** 2026-06-15 (Pattern-B WS1 design dialogue with Matt — the rogue/glass-close-ST coordinate question)
**Author:** gandalf (story-and-design steward)
**Status:** v1 — design ruling. The verdict + the three moves are LOCKED design intent (Matt-authorized). The implementation is a spawned cross-seam workstream (gamora / rocket / star-lord / Godot), NOT yet built. The viability playtest is DEFERRED behind the pipeline-completion gate (§8).
**Authority:** Matt 2026-06-15 — verbatim: *"The sim is a balance-approximation of a player-piloted game. So here is my bridge solution: We load pre-move geometry (telegraph time and space) into the sim and we output it as JSON. Then we delete b6 and let the godot game prove out whether these glass kits can evade and pass their boss skill check or not."* + clarification: *"delete the archetype tag that was finding rogue needs damage amp and providing the damage amp. I want that deleted."* + *"we have special movement skills like dodge, blink, teleport. One of these should be added by design to glass-close-ST."*
**Companion docs:**
- `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` — the SPATIAL twin. This doc is the same decoupling cut on the TIME axis (sim owns the invariant geometry; the game presents it; the player experiences what the sim balanced).
- `agentic_orchestration/gandalf/notes/2026-06-15-rogue-arc-coordinate-confound-reframe.md` (commit b23dce3, jack-ryan-cleared) — the coordinate-confound reframe this ruling resolves.
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-architectural-grammar-gap.md` — sibling WS2 work (referenced only for the shared invariant-discipline pattern).
- `canonical/00-ground-state.md` — oracle (this doc registers as a new CURRENT row).

---

## 0. TL;DR

The sim is a **balance-approximation of a player-piloted game.** Glass-close-ST (a fragile, close-range, single-target coordinate) walls against bosses in the sim because the sim has no dodge layer — and **that walling is correct.** Viability for this coordinate was always supposed to live in the *piloted* layer, not the autobattle.

The architectural move is a **temporal decoupling**, the twin of the spatial battle-room decoupling: **the sim owns the temporal combat geometry** (the telegraph — each boss attack's wind-up *time* and danger-zone *shape*); **the game owns the dodging of it.** The sim computes the telegraph and exports it as JSON; Godot renders it and wires dodge input; the *player*, not the sim, proves whether the glass coordinate passes its boss skill check.

Three moves enact it:

1. **DELETE the archetype auto-amp** — the balance-loop reflex "tag rogue → detect needs-amp → inject amp." It was the *automated* version of the genre-wrong fix (buff the fragile coordinate with raw stats), and it *masked* the coordinate's true shape. Replace "detect→compensate" with "detect→**flag-and-defer**."
2. **ADD a movement skill BY DESIGN** to glass-close-ST — **dodge** (an i-frame roll), guaranteed-intrinsic, not a generation roll. (Not teleport — it dissolves the coordinate. See §5.)
3. **BRIDGE** — telegraph geometry into the sim → JSON → Godot render + dodge input.

**One invariant:** one telegraph source, two consumers (sim costs/flags; Godot renders), **no drift.** **One discipline:** the dodge is *inert in the sim, active in Godot* — the sim must STILL wall glass-close-ST and flag it dodge-gated; do NOT make the sim "model" the dodge. **Pipeline-completion gate:** a faithful round-trip. **Viability playtest: DEFERRED** until the pipeline is complete (Matt directive).

---

## 1. The question this resolves

The WS1 rogue investigation (reframe doc, b23dce3) established — and jack-ryan independently cleared — that the glass-close-ST coordinate walls against bosses **regardless of kit power.** The offense-starved builder (~640 dmg) and the strong builder (b6, ~26,053 mean dmg, 40× more, driving the boss to ~88% / best 71%) **both** reach 0/60 boss kills at that coordinate. The deficiency is therefore a **coordinate-shape property**, not a composition / power-tier / DoT-channel property. The diagnostics decided *what* walls. They explicitly did **not** decide whether walling is *correct*. That is the design call, and this doc makes it.

The call hinged on one fork (framing-audit Q1 — the load-bearing assumption):

> **Is the sim the game, or a balance-approximation of a piloted game?**

Matt resolved it: **the sim is a balance-approximation of a piloted game.** That resolution settles everything downstream. In a piloted game, the *player* is the defensive layer the sim cannot model — they dodge the slam the autobattle has no way to dodge. So the sim walling at glass-close-ST is the sim **honestly reporting** "this coordinate's viability depends on a skill I do not model." It is not a deficiency. It is a *flag*.

## 2. The temporal decoupling (the architectural heart)

We have already committed this exact cut on the *spatial* axis. The battle-room presentation-decoupling separates the **sim-invariant** (spawn positions, the playable tile footprint, where damage lands) from the **presentation** (room extent, walls, dressing, camera, lighting). The sim fixes the small sacrosanct geometry; the game presents it; what the player sees stays faithful to what the sim balanced.

This ruling makes the *same* cut on the **time** axis:

| Axis | **Spatial** decoupling (battle-room) | **Temporal** decoupling (this doc) |
|---|---|---|
| **Sim owns (the invariant)** | spawn positions; playable tile footprint; where damage lands | each boss attack's **wind-up time** + **danger-zone shape** (the telegraph) |
| **Game owns (presentation / skill)** | room extent, walls, dressing, camera, lighting | the **dodging** of the telegraph (movement-skill input) |
| **The faithfulness rule** | the visual footprint must respect the playable footprint | the rendered telegraph must **equal** the costed telegraph |
| **What the player experiences** | a real *place* that respects the sim's combat geometry | a real *fight* whose dodges respect the sim's combat *timing* |

The symmetry is not decorative. It tells us the bridge is **architecturally consonant** with where the project already went — it is the decoupling principle extended from *space* to *time*, not a one-off patch. The sim computes the invariant geometry (spatial: where; temporal: when + what-shape); the game presents it; the player's experience is faithful to the balanced fight.

## 3. The verdict — glass-close-ST should wall on raw stats

A coordinate where the *single most fragile build* also kills bosses **with no compensating mechanic** would collapse the genre's risk/reward spine. The genre has never permitted that, and its solutions are instructive:

- **Diablo II** let glass-ish melee beat boss HP pools through **Crushing Blow** (damage as a % of the boss's *current* life — the one mechanic that scales to boss pools) and **life leech**. Strip those and naked glass-melee *walled* against Diablo / Baal / Ubers — correctly. Hell difficulty even applied a *leech penalty* so the coordinate could not free-ride.
- **Diablo III** baked in the inverse admission: every **melee class gets a flat 30% damage reduction** just for being close-range. The genre *knows* close is a tax and structurally offsets it — without ever letting pure glass free-win.
- **PoE** makes "Glass Cannon" a literal keystone (+damage / +damage-taken). Pure glass *can* clear pinnacle bosses (Sirus, Maven, Uber) — but only by solving survivability *some other way* (flask / dodge / leech / Mind-over-Matter layers, or out-mechanicing the telegraphed slams). Zero-layer glass dies. Always has.
- **Souls / Hades / Monster Hunter** are the purest case: low-vigor/high-damage **clears bosses through perfect dodging** timed to the wind-up (Souls i-frame roll; Hades dash through the red danger-zone; Monster Hunter reading hitbox + wind-up + recovery). In these games the fragile-high-damage build is not the consolation coordinate — it is the **flex** coordinate, *chosen* because mastery shows.

So: glass-close-ST **should** wall on raw stats. The fix is emphatically **not** a flat reach/durability buff to the coordinate (that flattens the spine). The genre-correct cure is to make the coordinate *earn* boss-capability through a **mechanism** — and in a piloted game the cleanest mechanism is the player's own **dodge skill.**

## 4. Move 1 — delete the archetype auto-amp

The balance loop carried a reflex: tag rogue → detect "rogue underperforms" → **inject damage amp to compensate.** That is the *automated* version of the genre-wrong fix. It was the system *lying* — papering over a fragile close-range coordinate by force-feeding it offense, so the coordinate *looked* stat-viable when its real viability was always meant to live in the dodge layer. Delete it. The sim should then **wall glass-close-ST honestly**, and that walling is read as "dodge-gated → defer to Godot," not "deficient → compensate."

Two guardrails on the deletion:

1. **Delete the *auto-compensation*, not *player-chosen* amp.** Damage amp as a build element a player picks (gear affix, skill choice) is legitimate and stays. What dies is the *archetype-tag-triggered, deficiency-detecting, auto-injecting* amp. The trigger is the bug; the mechanic is not.
2. **Replace "detect→compensate" with "detect→flag-and-defer," NOT "detect→fail."** A naive deletion would let the balance loop simply *re-fail* the coordinate, recreating a dead coordinate by another door. The coordinate needs a **new status** — *dodge-gated; viability deferred to the piloted layer; do not auto-compensate, do not fail.* The change is not a deletion; it is the **replacement of a wrong reflex.**

## 5. Move 2 — a movement skill, by design

Removing the fake *offensive* compensation (Move 1) and adding a real *skill-survivability* tool (Move 2) are the two halves of one clean swap: the system was solving a *dodge/skill* problem with a *stat/offense* hack; we replace it with a dodge/skill *instrument*.

The governing rule for which movement skill:

> **The movement skill must solve the survivability puzzle WITHOUT removing the player from the close-range fight.**

Judged against that rule:

| Skill | Verdict |
|---|---|
| **Dodge** (short i-frame roll/dash) | **Design-correct.** Keeps you *in* close range; makes boss-viability a genuine *timing* skill check (read the wind-up, roll through it). This is the Souls/Hades model that makes glass-close-ST the *flex* coordinate. **First choice.** |
| **Blink** (short instant reposition) | Acceptable *only if* tuned as a gap-closer / around-the-target reposition (PoE Whirling Blades; a Souls lunge) so it keeps you on the boss. |
| **Teleport** (long reposition) | **The trap.** It pulls you to *range*, dissolving the very coordinate — a glass-close-ST that keeps teleporting away is just glass-*medium*-ST wearing the wrong tag. Reserve it for a *ranged*-glass kite coordinate, where escape-to-range *is* the identity. |

Two further constraints:

- **Guaranteed, not rolled.** "By design" must mean **archetype-intrinsic** — *every* glass-close-ST kit carries the movement skill. If it is a generation *probability*, the generator will eventually mint a glass-close-ST kit *without* it and the dead coordinate returns. Bake it in.
- **Spirit-guide option (worth weighing).** Grant the movement skill via the **spirit guide** — the future-self teaching you to evade. That places the survivability instrument on the project's load-bearing differentiator (spirit-swap) rather than a generic skill slot, and it is thematically exact.

## 6. Move 3 — the telegraph bridge

The bridge connects the sim's balance math to the game's skill layer:

1. **Telegraph geometry into the sim.** Each boss attack gets a defined **wind-up time** (how long the pre-move telegraphs before it lands) and **danger-zone shape** (the space the attack covers), wired into the sim's action resolution. *Note:* if the sim currently resolves a hit as "deal X at action tick T," this telegraph model does **not yet exist** — it is a **combat-model extension**, the load-bearing *content* (it *is* the dodge game), not JSON plumbing. Scope it as such.
2. **Export as JSON.** The telegraph geometry is serialized alongside the existing fight export.
3. **Godot consumes.** The game renders the danger zones + wind-up timers from the JSON and wires the dodge input. The *player* times the dodge against the rendered telegraph.

## 7. The invariants and disciplines

**7.1 The invariant — one telegraph source, two consumers, no drift.** The telegraph the sim *costs* MUST equal the telegraph Godot *renders*, or the balance and the playtest answer diverge silently. A single telegraph definition is consumed by the sim (to cost / flag) and by Godot (to render). The export schema enforces the contract. This is the *same* invariant-discipline as the battle-room wall ring — name it from line one, not as cleanup.

**7.2 The discipline — the dodge is inert in the sim, active in Godot.** In the autobattle there is no piloting, so the dodge skill does *nothing* there — it cannot time itself to a telegraph. Therefore **the sim must STILL wall glass-close-ST and STILL flag it dodge-gated, even after the dodge is added to the kit.** Do **not** let anyone try to make the sim "model" the dodge — that re-imports the exact faking Move 1 deletes. The dodge's value realizes only in the piloted layer, which is precisely where the viability question is routed. (Operational corollary: the sim must treat a movement skill it cannot use as a clean **no-op** — not crash, not mis-cost the kit for carrying it.)

**7.3 The scale boundary — Godot proves the archetype; the sim still balances per-form.** The engine generates *thousands* of glass-close-ST neighbors; the piloted game can prove the *archetype* ("does the dodge-skill-check coordinate work *in principle*") on an exemplar, but it does **not** replace the sim's per-form balancing. Once the archetype is proven, the sim can **trust** glass-close-ST as a viable coordinate and stop false-failing it. Do not conflate "proved the archetype in Godot" with "balanced every glass form."

## 8. The pipeline-completion gate vs the deferred playtest

**8.1 Pipeline-completion gate (the criterion that closes the build).** The deliverable is a **faithful round-trip**: the telegraph (wind-up time + danger-zone shape) the sim computes **equals** the telegraph Godot renders, **and** dodge input resolves against it. Prove it first on **one boss + the glass-close-ST exemplar** (the first increment of the real pipeline, not a throwaway spike), then extend coverage. This is a *technical round-trip + invariant* criterion — not a viability judgment.

**8.2 The playtest is DEFERRED (Matt directive 2026-06-15).** *No playtest until the pipeline is complete.* The "can a skilled player dodge-clear glass-close-ST" test fires on a **separate Matt go**, AFTER the round-trip is proven. Do not slot a viability playtest into the pipeline build.

**8.3 The honest-test bonus.** Once telegraphs round-trip into Godot, the question "is a coordinate-level reach/durability fix ever owed?" stops being an argument and becomes a **playtest**: put a skilled player on a glass-close-ST boss *with telegraphs rendered and the dodge in hand.* Dodge-clears → the coordinate is legitimate, the sim was false-failing, done. *Cannot* clear even with perfect reads → *now* there is a genuine deficiency (dodge windows too tight / boss reach actually unfair), and *that* is when a reach/durability adjustment is earned — and you **playtest** it rather than argue it. The bridge converts the hardest balance argument into an empirical gate. (Recognition → validate → commit: the empirical gate is a *playtest result*, not time-passage.)

## 9. The work package this spawns

Routed through knight-rider (sequences + authors the per-seam dispatches; seam-routing is KR's call). Recommended shape and dependency order:

| Seam | Work | Order |
|---|---|---|
| **gamora** | Delete the archetype auto-amp; implement the flag-and-defer status. | Independent — can fire immediately (makes the sim honest now). |
| **rocket** (+ gamora) | Bake the dodge intrinsic into glass-close-ST composition. (+ gamora: confirm the sim treats the movement skill as a no-op.) | Parallel. |
| **gamora** | Telegraph combat-model — wind-up time + danger-zone shape per boss attack, wired into action resolution. The load-bearing content. | Critical path. |
| **star-lord** | Telegraph export to JSON; owns the no-drift schema contract (§7.1). | Critical path, after the combat-model. |
| **Godot seam** (drax per WS2 precedent — KR confirm) | Consume telegraph JSON; render danger zones + wind-up timers; wire dodge input. | Critical path, after the export. |

## 10. Player consequence

The player who picks glass-close-ST should feel: **"I'm a scalpel — I delete trash and squishies fast, and bosses are my skill check."** That is a real, beloved archetype (the D2 leech-zerker, the PoE crit-melee, the low-vigor Souls run). What the player must *never* feel is **"my build is structurally a lie — the game generated me a coordinate that can't ever do the content."** The entire distance between those two feelings is whether the *mechanism* to convert fragility into boss-capability **exists and is reachable** from the coordinate. Move 2 (the guaranteed dodge) makes it exist; Move 3 (the telegraph bridge) makes it *expressible*; Move 1 (deleting the auto-amp) stops the system from *faking* it. Together they turn the project's highest-risk coordinate into its highest-skill-expression coordinate — exactly where the genre puts it.

## 11. Cross-references

- **Spatial twin:** `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` (the sim-invariant vs presentation decoupling on the space axis; this doc is the time-axis twin).
- **Source reframe:** `agentic_orchestration/gandalf/notes/2026-06-15-rogue-arc-coordinate-confound-reframe.md` (commit b23dce3, jack-ryan-cleared) — the coordinate-confound finding this ruling resolves.
- **Role-orientation taxonomy:** glass-close-ST is a *damage* archetype (close / single-target / fragile) per the project's damage/support/control/hybrid taxonomy.
- **Discipline:** recognition → validate → commit (the viability gate is a playtest result, not time-passage — §8); the invariant-discipline (§7.1) mirrors the battle-room wall-ring contract.
- **Oracle:** registered as a new CURRENT row in `canonical/00-ground-state.md` § 1.
- **Decisions-log (pending, Matt-gated):** the coordinate-confound + auto-amp-masking methodology lesson is an enrichable jack-ryan decisions-log candidate.

---

**Signed:** gandalf, 2026-06-15 (story-and-design steward)
**For:** the ruling that resolves the glass-close-ST coordinate question by a **temporal decoupling** — the sim owns the telegraph geometry (wind-up time + danger-zone shape) and flags the coordinate dodge-gated; the piloted game owns the dodging and proves the skill check — enacted by deleting the archetype auto-amp (replace with flag-and-defer), giving glass-close-ST a guaranteed-intrinsic dodge by design (not teleport), and bridging telegraph geometry sim→JSON→Godot under one no-drift invariant, with the dodge inert in the sim and active in Godot, and the viability playtest deferred behind the pipeline-completion round-trip gate.
