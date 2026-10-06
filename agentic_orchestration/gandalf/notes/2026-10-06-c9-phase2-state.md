# Run C-9 Phase 2: state at 2026-10-06 (addendum to the 2026-10-02 handoff)

**STATUS:** CURRENT (working-memory note). **Author:** gandalf (RUN-CONDUCTOR, session aab928). **Truth of record:** `astra_test_01/burst/runs/C-9/ledger.json`, rulings R-C9-135..157. Where this note and the ledger disagree, the ledger wins.

## Matt's playtest order (R-C9-135, R-C9-156)

1. **Warlord vs real enemies in the 2D arena.** This is KC2-PLAY, run by the Sim Session. REFERENT-v1 is SEALED (KP-286), and P1(e), the dressed build, is being wired by KC2's drax on the crucible floor.
2. **Sorceress, then barbarian** in the arena. These wait on their JOIN-1 kit oracles (KC2 J2..J4).
3. **barrow_v2 in TRUE 3D**, like the v1 Barrow, in the barrow_full project. It starts **after Matt's warlord playtest** (R-C9-156/157). It is not a 2D skin.

## Handed to KC2 for P1(e)

**Warlord:**
- `join1_pack/gd-eor-warlord-eor3`: helm notch fixed (R-C9-141). Its cells have no baked red.
- EoR overlay atlas `join1_vfx/eor_overlay/` (R-C9-152): red-tinted translucent haze plus sparks, no arc. Drop the kc2p ribbon.

**Enemy packs, all with true_size** (table `join1_render/true_size_table_2026-10-02.*`):
- every tier-1 and tier-2 pack;
- painted bosses `_p` (warden, magister, witch, mindtaker);
- fleshshaper, ascended, vigillord;
- fleshhulk and colossus (Mixamo mutant set, R-C9-150);
- abomination, woollyrhino, crawlerlarva_p, burrowworm_p;
- coilseer and gloamwing (the REFERENT alternates, R-C9-137);
- hellhound.

**Every w151–160 family has a pack.**

## Paused (each awaits Matt's go)

**SO, the sorceress hood fix.** Option B, R-C9-152, built at `so_mx/export/ss152b`. Stills are in `so_mx/look/R-C9-152_*`. Matt answered "Not now".
- It still needs the next Barrow web deploy. Build with `PIN_SHA=b4de84e65` for EOR2's final effect.
- It still needs the JOIN v5 sorceress pack. **First delete the empty `join1_pack_v5/d2-fire-sorc-bm/`**, because the script refuses to run while it exists.
- Resume notes: `so_mx/RESUME.md`.

**MX adoption remainder (R-C9-150):** the wretch and revenant zombie clips and the "stand up" emerge.

**Hellhound left-foreleg band** barely reads. A repaint is optional and costs Astra images.

## barrow_v2: what was learned (the 2D route is SHELVED, R-C9-151..156)

- **Root cause:** coupling barrow_v2 to the 2D arena and to KC2's P1(e) deadline forced geometry-by-rule before art.
- **What failed:**
  - a 3D greybox as the paint guide (boxy shapes carry through);
  - flat zone maps (the painter invents and duplicates structures per chunk);
  - density on the fight floor;
  - no exit lanes.
- **Keep:**
  - sketch A, `barrow_v2/sites/BV3r2-A.png`, the look of record;
  - layout v6 (`barrow_v2/layout_v2.json`; validator R1–R13 at 66/66), which has the anchors, the organic floor, the exit lanes, the clean floor and `models[]` slots;
  - doors sized to their monsters (R-C9-154);
  - 9 Tripo models in `barrow_v2/models/builds/` (hall, porch, gable, barrow, wreck, cavecliff, staircliff, cliffplain, crag);
  - DV's spawn-VFX event contract (`join1_vfx/barrow_v2_spawn/`).
- **True-3D plan:** the v1 method in the barrow_full project:
  - real models for every structure;
  - real coast, ice and streams, cairns and stones;
  - a whole-site guided paint-over baked onto the 3D world;
  - then the KC2 sim running inside it with 3D enemies (joint with KC2's drax; scope later).
- **First step when Matt says go:** a 3D blockout with the real models, for his review before any painting.

## Live

- **Barrow web deploy** `d069c4b` (loadout). It has:
  - the sorceress arena kit (`armor=bm134`), carrying the transparent-hood defect that option B fixes;
  - the character-light toggle;
  - the Meteor scorch;
  - eor3;
  - EoR at 1b56f15ba (the R-C9-143 look; R-C9-152's red-tinted smoke is NOT deployed yet).
- **Disk** about 32 GiB free (gate 20). Superseded-scratch lists are in each lane's RESUME.md for Matt.
- **Known gap:** the manifest lint checks cast releases only. index_cells covers attack contact frames.
