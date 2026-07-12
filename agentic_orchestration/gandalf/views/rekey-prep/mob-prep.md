# Re-key prep — MOB slot (design session #3, DL-02 adjacency)

**Date:** 2026-07-12 · gandalf (mechanical prep; **elicits, does not rule**) · Spec: `corpus-rekey-spec-v1.md` §2 — mob RETIRES → raw descriptor; engine target = **move-policy / movement-verb vocabulary**.

## 1. Corpus code frequency (v3 CSV canon positives, n=478)

| code | meaning | count | % |
|---|---|---|---|
| H | high mobility | 168 | 35% |
| M | med mobility | 137 | 29% |
| _ | unspec | 58 | 12% |
| L | low mobility | 42 | 9% |
| P | player-verb | 39 | 8% |
| K | skill-is-movement | 24 | 5% |
| R | rooted | 10 | 2% |

**6 live codes** (decoded via `code_mob`) — but two DIFFERENT axes are tangled here (see §4).

## 2. Engine vocabulary of record — move-policy + commitment

Source: `simulation/spatial_gauntlet/commitment_state_machine.py::move_policy = "rooted" | "walk" | "full_move"` (per-skill navigation policy during a cast). Adjacent axis: **commitment** (`instant` / `wind-up` / `channel`, `commitment_state_machine.py` + E4 note). Movement-as-skill lives in geometry (dash/blink = GX-01 verbs) + the `full_move` policy (spin class).

## 3. PROPOSED mapping (corpus → engine) + residue

| corpus | → engine | confidence | note |
|---|---|---|---|
| R rooted | `move_policy=rooted` | HIGH | 1:1 |
| K skill-is-movement | GX-01 movement-verb / `full_move` | MED | dash/blink kits; geometry-side |
| P player-verb | `move_policy=walk`/`full_move` | MED | player-driven repositioning |
| H / M / L (high/med/low) | **no engine slot** | — | **kit-level mobility ≠ per-skill policy — RESIDUE** |
| _ unspec | (unmappable) | — | drop |

**Residue — the big one:** corpus H/M/L (347 kits = 73%) is a **kit-level mobility characterization** with no corresponding engine coordinate. Engine `move_policy` is a per-skill navigation policy (rooted/walk/full_move during a cast), NOT a "how mobile is this build" axis. The two do not compose 1:1.

## 4. Open forks (UNRESOLVED — Matt rules)

- **Fork M1 — the axis-tangle: does the engine NEED a kit-level mobility axis?** Corpus mob conflates (a) per-skill policy (rooted / skill-is-move / player-verb) with (b) build-level mobility feel (high/med/low). The engine expresses (a) via `move_policy` + commitment + GX-01 verbs. It has **no** (b) axis. Options: **(i)** mobility is EMERGENT — it falls out of movement-skill geometry + move_policy + commitment, so no new axis is needed (re-key drops H/M/L as descriptor-only). **(ii)** mobility is a first-class kit-feel axis worth keying (a "kiting/zoom" dimension) — build it. **Genre precedent:** PoE never keyed mobility as a class axis (it emerges from movement-skill choice + Quicksilver); D3/D4 similar (mobility = which movement skill + cooldown). Grim Dawn same. **Lean strongly (i):** mobility is emergent across the whole genre; keying it would invent a coordinate no shipped ARPG treats as primary. Re-key H/M/L → descriptor metadata, not a slot. This is the DL-02 adjacency question — decide it here.
- **Fork M2 — K vs P boundary.** `skill-is-movement` (Whirlwind, Leap, Charge — the skill *is* the traversal) vs `player-verb` (the player repositions between casts). Engine `full_move` (spin) covers K; `walk` covers channel-repositioning. Clean-ish, but the 24 K + 39 P kits deserve a sample-check that the boundary survives re-key. **Lean:** map K→full_move-class, P→walk-class; verify on the B12 spin re-cert.

## 5. RULINGS (Matt 2026-07-12 — session batch, ruling 3 of 6)

- **M1 — (i) RULED: mobility is EMERGENT; no sampled kit-level mobility axis.** Corpus H/M/L → descriptor metadata only. **Matt's composition note (load-bearing):** mobility is *"already planned… at the very end of the content emission pipeline as a hypothesis-test-derived label (among many others which we expect to emerge during battle simulation)."* So mobility WILL be keyed eventually — but as a **measured/derived label** (gauntlet-side, post-emission), never a sampled coordinate. This lands exactly on the measured-vs-projected law: the mobile projection table itself classed Mobility as BC-MEASURED; the ruling makes that the permanent architecture. Expect a family of such emergent labels from battle-sim hypothesis tests.
- **M2 — probe resolves** (movement verbs + policy-while-casting collected per kit; K/P boundary verified on probe facts + B12 spin re-cert).
