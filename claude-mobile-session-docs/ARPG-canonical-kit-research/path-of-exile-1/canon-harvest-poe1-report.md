# Canon Harvest — PoE1 Corpus Report

**Delivered:** `canon-corpus-poe1.jsonl` — **91 records, 100% valid JSON** (85 positive · 6 negative · 4 flagged `degenerate-famous`), emitted in six validated chunks per Amendment A2.
**Coverage (per the A5 contract):** deep canon COMPLETE, strong-moderate comprehensive. Family counts: melee/attack 18 · bow/wand 10 · cold 4 · fire 8 · lightning 8 · chaos/DoT 9 · minions 7 · totems/traps/mines 5 · trigger/mechanic archetypes 10 · defense-and-oddity archetypes 3 · negatives 6 · **post-cutoff search-derived 3**. A coverage claim without the boundary statement below is malformed — read §5.

## §1 — Era-rider findings (fired again, twice)
PoE1 is at **3.28 "Mirage"** (May 2026), past a **3.27 wand rework** — both postdate the harvester's training. Live-source catches recorded at c≤0.5 per A1: **Kinetic Fusillade** (3.27 rework attack), **Minion Pact Blade Vortex** (3.28 spectre-sacrifice snapshot, flagged degenerate-famous, community expects a nerf), **Heavy Strike Stun Berserker** (3.28). Transfigured-gem variants folded per A3.5 (PConc of Bouncing → PConc aliases). PoE2 is at 0.5 "Return of the Ancients" — logged for the later PoE2 run, not harvested here.

## §2 — Gap register (13 gaps; two NEW)
| Gap | Finding → routes to |
|---|---|
| P1-01 | **Self-damage economies** (RF, Boneshatter, Forbidden Rite, Dark Pact, CWDT/Ward loops; Reaper as failure; Minion Pact at exploit tier) → Axis-5 candidate bins; K26/K27 adjacency |
| P1-02 | **Mark-and-consume / apply-then-detonate** (Earthshatter, Hexblast, Lightning Conduit, BF/BB, Discharge) → phase-axis evidence; now CROSS-GAME with GAP-D2-03 |
| P1-03 | **Skill-is-movement + deploy-emitters** (Flicker, EA ballista, mines, traps, totems, Autobomber; **Charged Dash = the contrastive FAILURE** — movement-verb damage needs low friction) → B5/B6 + K11/H4 family |
| P1-04 | **Channel-stack-release** (Blade Flurry, Scourge, Flameblast, Incinerate, Divine Ire; Pizza Sticks = the commitment OUTSOURCED to proxies) → commitment-axis texture |
| P1-05 | **Conversion chains** (LS, Frost Blades, TS, wander) → Codex surface/mask — pre-registered prediction CONFIRMED |
| P1-06 | **Autonomous orbiters / body-orbit** (Helix, Winter Orb, Ball Lightning, **Poison BV = the body-orbit rotational anchor**) → rotational addendum evidence |
| P1-07 | **Boomerang return paths** (Spectral Throw, Venom Gyre catch-and-release) → dr/dt sign-flip family |
| P1-08 | **Gear-stat-as-weapon** (SST, Facebreaker, Death's Oath, Archmage, Baron, Iron Commander, Whispering Ice) → stat-is-the-build archetype family |
| P1-09 | **Mirages execute the player's own skill** (General's Cry) → novel proxy mode, no roster surface |
| P1-10 | **Stochastic element roll** (Ele Hit; Wild Strike as the negative twin) → exceeds element schema — ruling owed |
| P1-11 | Pod-slow DoT zones (Toxic Rain) → DoT-geometry note |
| **P1-12 NEW** | **Consumable-charge & loot-as-ammo economies** — PConc's flask charges, Animate Weapon's drop stream, Wormblaster's manufactured trigger-fodder → named Axis-5 reserved-bin candidate occupant |
| **P1-13 NEW** | **Enemy-roster-as-arsenal** (Spectres: which corpse you bind defines the kit) → the reap verb's closest genre cousin; mechanics AND fiction note for Matt |

**Cross-game confirmations this run:** corpse economy (DD, General's Cry ← GAP-D2-04) · multi-element cap collisions (Discharge, Golementalist, Wild Strike ← GAP-D2-10) · movement verbs (← GAP-D2-01) · **reservation economies now have NAMED Axis-5 occupants** (Solo Aurastacker, Low-Life Shavs, Aurabot).

## §3 — Projection rules applied
**Attributes:** STR/DEX/INT read literally from PoE; **WIS assigned by Templar fantasy** (Inquisitor/Hierophant/Guardian, c 0.55-0.6); Saboteur → INT c 0.6-0.7; delivery-agnostic mechanic archetypes (Aegis, LL Shavs) carry host-dependent low-c values. **Elements** stay in PoE vocab (fire/cold/lightning/chaos/physical) with `abstain_map:true` throughout — poison recorded as chaos-DoT per source truth. **Abstains** cluster on `econ` enum mapping, `mob`, spectre/host-dependent axes, and everything post-cutoff — the reconciliation queue is the abstain set, as designed. The Aurabot's `ctrl:"support"` abstain demonstrates the enum-exceeded case cleanly.

## §4 — Provenance legend
`mb` mobalytics PoE tier lists (Jungroan/Ben/Ruetoo-curated, live) · `od2` odealo 3.28 build index · `el` exitlag 2026 overview · `sky` skycoach lists · `kb` settled community canon (wiki/forum-guide/reddit lineage — live-URL backfill owed) · `pw` poewiki · `pf` forum archive · `rd` r/PathOfExileBuilds · **`pn` poe.ninja + `pb` PoB codes = TEAM BACKFILL (Rank-1 sources requiring API access).**

## §5 — Documented shallow tail (named, NOT recorded — completeness boundary)
Rain of Arrows · Smite · Static Strike · Infernal Blow · Dominating Blow · Absolution · Cremation (DD sibling) · Eye of Winter mines · Pyroclast Mine · Exsanguinate self-cast/mines (current-tier Trickster pairing — dossier candidate) · Lightning Trap · Storm Rain · Manaforged Arrows · Blight · Wintertide Brand · Frostblink ignite · Consecrated Path · Reave · Shockwave Totem · Ngamahu Cyclone (variant-folded) · Vaal Spark (era-folded into Spark) · Fire Nova Mine (removed skill; era-canon note only).

## §6 — Team completion pass (spec)
1. **poe.ninja API sweep per league** → attach usage-share column; auto-flag any name ≥0.5% share missing from corpus. 2. **PoB code attachment** per record (Rank-1 mechanical truth). 3. Live-URL backfill for every `kb` row. 4. Dossiers for the three post-cutoff records + Exsanguinate mines. 5. **Audit per spec §3.5:** ≥10% sample (~9 records), inter-rater on all proj axes — this dataset gates the FUN instrument.

## §7 — Calibration notes → D3 run
Fold rules A3 held under PoE's volume — 91 records covered what naive skill×ascendancy enumeration would have made 400+. The mechanic-archetype record class (A3.4) earned its keep: Archmage, Ward Loop, Aurastacker, Aegis are the corpus's highest-information rows. D3's shape differs — set-defined archetypes per class per era — so the D3 run keys records on **set+skill archetype** (e.g. "Whirlwind Wastes Barb"), one record per set-archetype lineage, era bands = seasonal meta snapshots. Negative canon in D3 = never-used sets (documented per class).
