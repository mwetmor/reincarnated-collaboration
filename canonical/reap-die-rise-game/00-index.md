# Reap. Die. Rise. — GAME Spec (Index)

**STATUS:** LIVE SPEC HOME (born 2026-07-02 — founded by Matt's One-Realm MVP ruling; resolves game-tracker B3's "does the game layer warrant a spec folder" question).
**Author:** gandalf (SCENEWRIGHT / SPEC-AUTHOR). **Build seam:** drax (`reincarnated-godot/`).

---

## What this folder holds

The **playable-product specs** — the third spec home beside `reap-die-rise-story/` (narrative end-state) and `reap-die-rise-engine/` (engine end-state). Story says what the world means; engine says what the systems emit; **this folder says what ships to a player and when.** The delta ledger stays `canonical/current-to-end-state/current-to-end-state-game.md` (spec here, distance there — same grid as the other two homes).

| Doc | Role |
|---|---|
| `one-realm-mvp-scope.md` | **THE DENOMINATOR** — the One Realm demo scope (Matt-ratified 2026-07-02): player path, roster accounting + summoner mandate, demo-critical vs launch-scope split, engine/Godot asks, wishlist gates |
| `arcade-minigame-taxonomy-spec.md` | **POST-LAUNCH SCOPE** (canonized 2026-07-07 from Matt's mobile draft + gandalf review) — the in-game activity layer: 6 design laws (packet-not-code, template lattice, cosmetic+QoL membrane), 11 WC3-lineage templates, rung ladder, two-tier certification. Does NOT gate MVP/demo; build waits on its §9.1 endgame fork (`gates-on: launch-scope-planning`) — game-tracker B6 |
| `ensemble-asset-pipeline-spec.md` | **CURRENT** (canonized 2026-07-10 from Matt's mobile handoff + gandalf ultra-think annex §13) — the character & gear ART layer: mannequin-per-race-frame doctrine, pieces-not-characters, style-bible image layer, MCP-authors-recipes/scripts-run-production, per-slot band ladder (stats→art = one integer), §8 Judge certification, plague-doctor pilot go/no-go. Feeds `../current-to-end-state/pipeline-game.md` Lane B (stages G1–G5) |

## Expected future members (as they're warranted, not before)

- King-rig opening-scene design doc (currently homed at game-tracker A4/B3 + `agentic_orchestration/gandalf/notes/2026-06-22-king-rig-mcp-alignment-brief.md`; migrates here when it grows)
- Descent floor-authoring spec (when the first authored floor graduates the three gates)
- Launch-scope product doc (post-demo; the demo's playtest data is its evidence base)

**Discipline:** this folder holds *product/presentation END-STATE* docs. Presentation grammar rulings live in the game tracker's PART A; open build questions in its PART B. Do not duplicate the tracker here.

**Author:** gandalf, 2026-07-02.
