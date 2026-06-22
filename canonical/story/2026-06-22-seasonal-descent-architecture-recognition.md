# Seasonal-Descent Architecture — Recognition Record

> **STATUS: RECOGNITION RECORD** (2026-06-22). Architectural commitments are
> DEFERRED per substrate-led / recognition→validate→commit discipline. This
> captures a coherent design vision from a Pattern-B session with Matt so the
> next session opens on the full picture. Nothing here is load-bearing canon
> yet; each open decision names the empirical gate that must resolve before it
> commits.

**Author:** gandalf (story/design steward)
**Session:** Pattern-B terminal dialogue with Matt, 2026-06-22 (following the
Godot play-shell king-rig + MCP-workflow work the same session)
**Cross-refs:** `project_earth_meta_layer.md` (Earth Self / form library /
seasonal journey-as-descent); `canonical/33-progression-skeleton.md` (the
expected-progression curve); `reincarnated-engine/src/reincarnated/anchor/`
(`select_seasonal_anchor` — the per-season theme primitive); `canonical/17-gear-and-spirit-guide-design.md`
(spirit-swap roster); the balance loop (B14.5 primary loop, WR/KPM bands);
`reincarnated-godot/scripts/walltop_level.gd` (`WalltopLevel.build_level →
LevelHandles`, the room-builder seam); the catalogue cluster/faction-coherence
work (elrond Phase-E lineage clustering).

---

## 0. The one-line vision

The game's core loop is an **infinite, reincarnating seasonal descent**: a
persistent Earth Self carries accumulated power across seasons; each season is a
fresh descent (new themed mega-boss + floor lieutenants) into deeper power tiers,
fed serially by the engine's generative content. The loop *is* the title made
mechanical — each re-descent is a reincarnation.

## 1. The reframe — descent, not generic roguelike

The structure is **authored spine + procedural infill** (Diablo's model), NOT a
random node-graph (Hades' model). The narrative shape — descend → trial → return
to Earth — is load-bearing (Earth-meta canon). The procedural variety buys
replayability; the authored beats buy *meaning*. Both, in different layers.

Working name: **the descent / season-descent.** Retire "procedural dungeon" —
name drift becomes design drift (Discipline #13).

## 2. Layered architecture (Matt's correction folded in)

| Layer | Owner | Authored vs procedural |
|---|---|---|
| Entrance arena + mega-boss arena (**bookends**) | drax (authored) | **authored set-pieces** — the box Drax built is a *beat*, not infill |
| **Modular middle** (corridors / junctions / chambers) | drax + seeded assembler | **procedural — PROTOTYPE THIS FIRST** |
| Per-floor sub-anchor → faction-coherent content | engine (rocket) | engine-emitted JSON |
| Floor difficulty = curve-tier, catch-up only | engine (gamora / balance) | engine-authoritative |
| Season anchor = descent spine / mega-boss | engine | the narrative thread |

**Key correction (Matt):** the wall-top battle-arena box is the wrong scale for
procedural connective tissue. Its size/character fit a **hand-authored boss fight
or entrance arena** (a *beat*). The procedural variety lives in the **modular
middle** between bookends. "Test the procedural middle first" is the keystone bet
— and the infinite-re-descent vision (§6) is what *justifies* the procedural
investment (a once-through descent could be fully authored; an infinite one
cannot).

## 3. The procedural-middle prototype (first test target)

Three primitives, in dependency order:

1. **Modular piece kit with explicit connection sockets.** Small starter
   vocabulary: straight corridor, L-junction, T-junction, descent-stair (sells
   "down"), small chamber (the content-slot carrier). Each piece exposes its
   **exit-socket transforms**. Extends the existing seam: today `build_level()`
   returns `LevelHandles`; a piece builder returns the same **plus its socket
   transforms**, and the assembler chains piece N's exit to piece N+1's entry.
2. **The socket/snap contract — the load-bearing primitive.** Pieces meet
   correctly only if socket transforms coincide to the millimetre. This is an
   **alignment problem → MCP is the right tool** (the "snapping staircases" case;
   the +50% king-rig win). Get this right or nothing assembles.
3. **Seeded assembler.** Deterministic-from-seed (matches engine seed
   discipline), strings pieces into a *mostly-linear-with-branches* descent (NOT
   a maze).

**Open decision — "how procedural" is the middle?** (a) pure procedural geometry
(infinite variety; failure mode = soulless asset-flip corridor, cf. D3's weaker
random tilesets); (b) Hades model — authored room *pool*, procedural *order*
(every room hand-quality, only the draw is random); (c) Diablo hybrid —
procedural skeleton + authored prefab stamps. **Steward lean:** build the
socket/snap + seeded assembler first (that IS the capacity to test), with a
deliberately small starter kit, but design the socket contract so individual
pieces can later be upgraded to authored-quality without changing the assembler.
Don't foreclose; don't over-author.

**Smallest first test:** three pieces (corridor, L-junction, descent-stair), a
seeded assembler chaining ~5–8, MCP-snapped sockets, rendered as a walkthrough.
If a seed yields a clean, gap-free, navigable, *seed-varying* descent → capacity
proven.

## 4. The content JSON seam (engine → Godot)

**Boundary discipline:** *the engine emits CONTENT; Godot owns GEOMETRY; the JSON
carries content + binding hints, never room dimensions.* The engine already
produces a balanced ordered sequence (progression skeleton + balance loop). A
content unit per descent-step = encounter composition (which monsters, scaled to
tier) + element/anchor theme + loot table + (for beats) the boss. The JSON binds
**content-unit → room-slot** and the room *type* requested (combat vs boss); it
must NOT specify walls/sizes/props. The moment the engine emits geometry, balance
authority and presentation authority fork (cf. D3 launch client/server difficulty
split).

**Serial emission = the descent, and it's a triple win.** Emit **floor-by-floor
(or room-by-room), not whole-season-at-once:** (1) thematic — you descend *into*
the unknown, not over a revealed map; (2) mobile — page content as you go
(project is mobile-first); (3) adjustable — the next unit is requested *after* the
current resolves, so the engine can supply it at a tier informed by how the player
just did. The seam is **request/response, engine-authoritative:** Godot says "I'm
at floor N; player cleared N-1 in T seconds at X% health" → engine returns floor
N's content JSON. Thin client.

**Validation gate (commitment-gating):** design the content-unit JSON as a
*projection of what the engine already exports* — NOT a new schema invented in a
vacuum. **Before committing the contract, pull one real engine season export
(`export/` + season emission) and diff it against the proposed content-unit
shape** (star-lord + rocket). First move next session.

## 5. The adjustment algorithm — the power spike is sacred

The anti-pattern to design against is **level-scaling backlash** (Oblivion's
glass-armor bandits; D3 + D4 launch "I leveled up and got *weaker*"). The
counter-example that got it right is **Diablo 2's largely fixed-difficulty
zones** — you out-level a zone and the faceroll *is* the reward. Three properties:

1. **Curve-anchored, not actual-power-anchored.** Balance each floor to an
   *expected power budget* = f(depth, expected level at depth, expected gear tier
   at depth). The anchor is the expected-progression curve (doc 33). A lucky drop
   / early level puts you *above* curve → the floor feels easy → that's the spike
   *landing*, not something clawed back.
2. **Asymmetric — catch-up only, never a tax.** Adjustment may pull a floor
   *down* toward a below-curve player (bad luck / skipped rooms); it may **never**
   pull a floor *up* toward an above-curve player. Lucky stays lucky. Up-scaling
   to gear rebuilds D3's mistake.
3. **Spike-runway / lag.** On a spike (level or big drop), the floor you're *on*
   stays at tier and the *next* floor or two are **not** re-tiered upward — a
   window to *spend* the new power. "Let them cook."

Engine stays the balance authority; Godot is a thin client requesting "floor N at
curve-tier(N)" and never touches monster HP.

## 6. Player-directed replay + infinite re-descent = literal reincarnation

Two player-controlled loops, both optional, both expression:

- **Lateral — replay an earlier/same floor** = the **D2 farm/enjoy loop**
  (Pindle/Baal runs). The *direct* answer to spike-pacing: the player rations
  their own spike (go back and bask, or push on). Player-controlled beats
  algorithm-controlled. **Risk to bank:** replay must be **permission, never
  obligation** — if a must-have drop is gated behind a floor, "enjoy your power"
  becomes "grind floor 3 forty times," the opposite of intent. Keep replay as
  expression + optional farm, never a forced loot-gate.
- **Vertical — re-descend deeper, starting from current power** = the **D3
  Greater Rift / PoE endless-Atlas push.** Carry your power; the frontier climbs
  to meet and exceed it; push until you find your wall.

**The reincarnation reveal.** Power *persists* across descents → there is a
**persistent vessel** = the **Earth Self**. Each re-descent is a new season (new
mega-boss, new lieutenants, new generated form). So each descent is a
**reincarnation**: the Earth Self persists and grows; the *form* is new each life;
the **form library is the record of past lives.** This completes the post-Phase-0
"Earth gameplay loop TBD" the canon left open. *Mechanic and theme are the same
object.*

**Coherence to nail:** the Earth Self's *power tier* (the curve) persists; the
*form/kit* worn is a **choice from the claimed roster (spirit-swap)**. Claiming a
new kit **adds to the swap roster; it does NOT reset power.** You descend as the
new form *at your accumulated tier.* (Prevents the incoherence "do I lose my build
when I swap incarnations?" — no; build-power is the Earth Self, the kit is the
mechanics-costume.)

## 7. Per-floor theming — the Anchor, not the element

**Element is a *property*, not a theme** — it tells the player what resist to
bring (tactical flavor, worth keeping) but carries no *story*, and theming by
element scrambles faction coherence. The story-bearing axis is the engine's
existing **Anchor** primitive (`{id, name, category, description}`, one selected
per season, history-aware, category-balanced).

**Make the anchor hierarchical:** the **season anchor** = the descent's
overarching theme / the confrontation at the bottom; each **floor sub-anchor** =
a domain-ruler / lieutenant subordinate to it. The floor's monsters are generated
**AS that sub-anchor's faction**; element falls *out* of the anchor; biome
(eventually) is the anchor's domain. This is the isekai floor-boss / tower-climb
spine (Solo Leveling's gates; the *Slime* floor-master) — *the floor exists
because of who rules it.*

**This dissolves the faction-fit problem by construction:** generate each floor's
roster *under* its floor-anchor → faction + element + identity coherent from
birth. Never shuffle a pre-generated monster into a mismatched floor.

**Pushback to bank:** do NOT go pure floor-anchor with no season anchor. The
season anchor is the **spine** — the *why* you descend, the thread that makes a
run a journey. Lose it → roguelike node-graph again.

**Validation gates:** (a) per-floor anchor selection is a real engine change
(`select_seasonal_anchor` is season-scoped today) — rocket's seam; (b) anchor
**library depth** — N floors × many seasons without repetition-fatigue; may need a
"season anchor generates its own lieutenant sub-anchors" relationship.

## 8. The mega-boss — OPEN DECISION (Matt: leave all options on the table)

The season mega-boss is the bottom-of-descent confrontation; beating it grants a
new incarnation (a claimable kit added to the spirit-swap roster — the gacha
*thrill* preserved but **skill-gated, not RNG-gated**; the trial-room
boss-gallery from early design, now generative + earn-to-wield). The **source** of
the mega-boss kit is UNDECIDED:

**Option A — over-band balance-loop reject.** Kits the loop rejects as out-of-band
(≈60–65% WR, or over-band combined KPM) are promoted to mega-bosses, tuned
*beatable* by under-resourcing (fewer potions, un-maxed gear), NOT by HP/damage
inflation. Strengths: (1) real difficulty, not bullet-sponge (cf. SNK boss
versions / Sekiro's Genichiro — a superior kit, fair); (2) **boss brain is free —
the balance sim already pilots kits; the boss is the same sim piloted vs a human**
→ one subsystem, three uses (measure / select / pilot); (3) **handicap targeted by
the data that rejected it** — over-band on damage → handicap survivability;
over-band on sustain → starve potions. **The blocking concern (Matt):** to keep
the band intact, a claimed kit must be brought *into band* — but a general nerf
risks making the claimed incarnation feel **sub-par / nerfed**, which is a weak
reward. *This is why Option A is not foreclosed.*

**Option B — held-out faction (e.g. a dark/sinister faction).** A curated faction
reserved as the boss/reward pool, generated **in-band but gated** — so claiming it
needs **no nerf** (it was locked, never over-band). Boss difficulty comes from the
*encounter*, not from the kit being out-of-band. Strengths: sidesteps the
claim-tuning feel-bad entirely; **stronger narrative** ("descend toward the dark
faction, confront and claim its forbidden power" — the isekai "absorb the demon
lord / claim the shadow" arc); gives the catalogue/faction work a clear home.
Cost: curation of the held-out faction; bounded variety (only that faction
supplies bosses).

**Option C — hybrid.** The held-out (e.g. dark) faction supplies the *identity*;
beating the faction *champion* (which can be a cranked/over-band member) grants
**induction into the faction** — you claim an *in-band faction member*, not
necessarily the literal over-band boss kit. No nerf, strong theme, boss can still
be over-band. Steward note: this may be the best of both, but it is **not a
commitment** — banked as an option.

**Validation gates:** (Option A) over-band **reject-pool depth** — does the loop
reject *enough* over-band kits to supply one fresh mega-boss per descent across
400+ seasons without repetition? (telemetry read, rocket/gamora). (Option B/C)
**held-out-faction pool depth** + the curation cost. (All) the **generation /
curation quality bar** — the claimable kit must be *interesting* (a distinct
mechanic/fantasy), or it's a treadmill reward regardless of source.

## 9. Treadmill antidotes (where endless loops die)

1. **Number-inflation death** (D3 Paragon/GRift pure number-go-up). Defense:
   **qualitative variety, not bigger tiers** — season 47 must *feel* different
   from season 3, a **generation-quality bar** (rocket).
2. **"Borderline infinite" needs coherent anchor-drawing, not faction salad.**
   400 factions shuffled = noise; the hierarchical anchor drawing a *coherent set
   per season* converts breadth into designed-feeling infinity. **Coherent drawing
   is the multiplier on breadth** — the home of the cluster/faction-coherence
   work (elrond Phase-E).
3. **Replay = permission, not obligation** (§6).
4. **Re-descent needs a narrative motive** (the new mega-boss / anchor), not just
   a bigger number. The season-anchor spine supplies the *why*.

## 10. Consolidated validation gates (the commit ledger)

| # | Gate | Owner | Resolves |
|---|---|---|---|
| G1 | Diff one real engine season export vs proposed content-unit JSON | star-lord + rocket | content contract (§4) — **first move next session** |
| G2 | Per-floor anchor selection + library depth | rocket | hierarchical theming (§7) |
| G3 | Socket/snap contract prototype (3 pieces, seeded, MCP-snapped) | drax | procedural-middle capacity (§3) |
| G4 | Generation-quality + coherent-drawing bars | rocket + elrond | treadmill antidote (§9) |
| G5 | Mega-boss source decision (A / B / C) + (if A) claim-tuning | Matt + gandalf + rocket | §8 |
| G6 | Reject-pool depth (A) / faction-pool depth (B/C) | gamora / rocket | §8 sustainability |

---

**Sign-off:** gandalf, 2026-06-22. Recognition captured; commitments deferred to
the gates above. The vision is coherent end-to-end and recognizably one of the
project's own — the infinite reincarnating descent *is* the title made
mechanical. Next session opens on G1 (content-contract export diff) and G3
(socket/snap prototype) as the two cheapest capacity-proving moves.
