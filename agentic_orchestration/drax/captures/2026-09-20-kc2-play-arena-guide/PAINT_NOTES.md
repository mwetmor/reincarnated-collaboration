# PAINT_NOTES — arena grey-room guide (KP-B1a, ONE image, then HALT)

1. FLOOR = #2ECC40 in `id_mask.png` (flat grey in the guide): the walkable arena plate. WALL = #FF4136: paint surface only, 2.00 m band, DECLARED thickness — the runtime owns collision at its inner edge. ISLAND = #0074D9 (raised 1.00 m, DECLARED). POOL = #FFDC00: enterable damage fields, NEVER walls. BEYOND = #000000: leave black, the parallax layers own it.

2. MAY BE EMBELLISHED, freely and within the class: surface (stone, grit, cracks, stain, wear), rubble and debris that does not read as an obstacle, light and its falloff, the fire register of the reference. Paint the picture, not the diagram.

3. MAY NOT MOVE: every edge in `id_mask.png` — the ring's inner edge, the wall band, the four island footprints, the six pool discs. The painting must register 1:1 with the mask at 1920 x 1080. A moved edge is a moved distance and the geometry is measured.

4. CYAN (#00FFFF) IS ANNOTATION, NOT SURFACE: the frame-origin cross, the ring edge line, the island contact lines, the Vanguard Banner aura footprint (r 8.0 m, placement DECLARED not decoded) and all text. Paint floor straight over them — but do NOT bake the Banner ring into the floor: it is a runtime overlay.

5. REGISTER: `ref_cathedral_far_ruins.png` — a native cut from the cliffside's own far_ruins layer, bbox [300, 960, 900, 1400], the burning gothic cathedral (R-C3-72 / CS-cathedral). Match its H1 line register and its identity. It is a PARALLAX asset: copy the register, not the scale.

6. DO NOT DRESS G5: interior nave vs exterior arena is Matt's open call. Plate scale 100.617554 px/m; this crop is ZOOM-GD 75.668403 px/m; world rect x [-12.6869, 12.6869] m EAST, y [-8.9412, 8.9412] m SOUTH, centred on the frame origin (north gate).
