# KC2 arena inside barrow_v2: scoping reply to C-9 (2026-10-09)

**Status:** PROPOSAL. No build. It needs (a) Matt's ratification of C-9's full-site review and (b) Matt's decision D-1 below. Owner of the integration: drax (kc2_play / kc2_runtime / pack). Owner of the art, coordinates and entrance VFX: C-9.
**Request:** the C-9 conductor, citing Matt R-C9-318 ("play a version of the arena here": the KC2 wave fight inside barrow_v2, with p01–p06 mapped to three doorway and three feature spawns, and bosses rising from the grave-ground or climbing from the sea cave).

## D-1 · Matt decides: presentation skin, or terrain-true? (recommendation: skin first)
- **(A) PRESENTATION SKIN, recommended for v1.** The sealed fight runs unchanged. ORACLE/PLAY decisions stay byte-identical (§ 4.7), and barrow_v2 is the visual setting. The sim's p01–p06 anchors, approach paths and timings stay the referent's. The barrow shows them through a declared, presentation-only transform (sim board → barrow world). Nothing re-seals. It is the same category as the original PLAY .app's art layer.
- **(B) TERRAIN-TRUE.** The sim adopts barrow_v2's walkability, distances and approach geometry. That changes fight outcomes (approach times, ranges, crowding), so it is the REFERENT-v2 item V2-TERRAIN: a new referent with a new seal, oracle work and a playtest. Large.
- A natural sequence: ship (A), and let Matt's play of it decide whether (B) is worth a REFERENT-v2.

## Proposed route under (A)
1. **Where it lives:** the barrow_v2 level imported into `kc2_play` as an art scene. The sealed runtime stays vendored and digest-checked by `kc2_play`'s existing vendor seam, MANIFEST, export and attempt-2 checks, and the pck stays clean of `res://join/`. Vendoring the runtime into `barrow_full` would mean rebuilding all of those checks there. drax confirms after the restart, including disk cost (the barrow assets are large; the disk HALT is 20 GiB).
2. **Anchors:** C-9 provides world coordinates for the 6 spawn points (doors p02 / p04 / p03, features p01 / p05 / p06) plus a walkable approach polyline from each spawn to the fight area, and the grave-ground and sea-cave boss points. drax fits a declared presentation transform per anchor. The sim's positions remain the truth for hits and ranges.
3. **Entrances (DV VFX set):** visual events are DRIVEN BY the sim's own events (spawn / enter tick / emergence). They never drive them. p05's "4 s of cracks then burst" already matches the sim's 4.0 s ambush release (the same law S-12 just made exact under moved clocks). Each entrance VFX's timing must fit inside the sim's emergence window.
4. **Bosses from grave-ground / sea cave:** the sim decides which anchor a boss spawns at. If the art shows it rising elsewhere, that is a visual-only offset during emergence, converging to the sim position before the boss can act. Otherwise the player sees hits land from the wrong place. C-9 and drax agree the convergence rule.
5. **Enemy art:** C-9 supplies enemy GLBs and clips (or names their source). drax binds sim actor types to art. Animation timing follows sim events (attack, hit, death). Any missing visual clip falls back to the current no-art marker, with no sim change.
6. **Camera and controls:** the barrow's v1 fixed ortho camera (pitch 52.95354°, yaw 47) is presentation. drax checks whether PLAY's key-to-direction mapping (KP-298: keys drive War Cry / potion, procs automatic; movement input) assumes the current camera yaw. If so, the input mapping rotates with the camera (presentation-side, no sim change).
7. **Performance:** the sim runs at its own tick rate (the runtime measured ~1.2–1.3 ms/tick), decoupled from render. Target 60 fps on this Mac with the full barrow site plus wave-160 crowds. C-9 supplies the site's render cost; drax measures the combined frame cost. LOD and culling are C-9's levers.

## What could block it on the JOIN-1 / KC2 side
- **J3c is mid-flight** (paused for Matt's restart, ledger KP-414). The sealed runtime moves X → `a0e75469` once J3c closes (jack-ryan Gate-2 + Matt's windowed self-test). ORACLE/PLAY are proven byte-identical across that move, so presentation work can start against the current PLAY runtime and re-pin later at no fidelity risk.
- **KP-312:** if the integration needs ANY new hook inside the sealed runtime (e.g. an event the art layer can't currently observe), that is a sealed-runtime change and needs its own Matt ruling, fail-first, byte-identity proof and jack-ryan gate. The aim is zero sealed edits: observe existing state from the presentation layer.
- **Disk:** importing the barrow site into the godot repo must fit under the 20 GiB HALT with margin.

## Ask of C-9 now (no build)
1. World coordinates for the 6 spawn points, 2 boss points, approach polylines, and the fight-area bounds.
2. The enemy art manifest (GLB + clip list per enemy family on the w151–160 line-up; the line-up is in `reincarnated-engine/src/reincarnated/simulation/kc2/referent_lineup.py`).
3. The DV entrance VFX list with durations.
4. The site's render-cost numbers.
5. The size of barrow_full on disk.
