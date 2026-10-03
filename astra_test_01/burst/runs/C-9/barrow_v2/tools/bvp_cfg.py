#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): writes paint/cfg_barrow_v2.json, the guided-paint config
(modelled on barrow_full/paint/cfg_barrow_full.json), with per-chunk notes naming what each panel
holds, computed from the layout's own footprints projected onto the plate grid.

    python3 tools/bvp_cfg.py
"""
import hashlib, json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
A9 = os.path.join(os.path.dirname(BV2), "artifacts")
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
FR = json.load(open(os.path.join(BV2, "paint", "frame_bvp.json")))
P = FR["px_per_m"]; X0, Y0 = FR["origin_px"]
A = math.radians(FR["pitch_deg"]); S, C = math.sin(A), math.cos(A)
GUIDE = os.path.join(BV2, "paint", "barrow_v2_zonemap.png")


def px(x, y, z=0.0):
    return X0 + P * x, Y0 + P * S * y - P * C * z


# plain words for the painter, per feature kind (no names of anything outside this game)
WORDS = {
    "mound": "part of the great BARROW MOUND (olive-tan): a huge burial mound of earth and dead grass under deep wind-drifted snow, ringed by old kerb stones",
    "door": None,  # per id below
    "stone": "a tall weathered standing stone on the barrow slope, rimed",
    "standing_stone": "a tall weathered standing stone on the barrow slope, rimed, leaning a little",
    "wreck": "the WRECK: an old wooden longship beached and frozen into the shore ice, heeled over TOWARD the open ground so its rail (the gunwale nearest the open ground) is low and broken; snow in the hull, ice around it",
    "mast": "the wreck's broken mast, raked, with a torn frozen sail rag",
    "rock": "weathered grey rock outcrops and boulders, fractured, snow on their tops",
    "tree": "a few bare, wind-bent birches",
    "juniper": "low dark juniper scrub",
    "hall": "part of the BURNT LONGHALL (dark brown slab): a long ruined timber hall, roof half fallen in, charred rafters showing, snow on what roof is left; its long west wall faces the open ground",
    "porch": "the hall's GRAND PORCH (orange): a tall gabled timber porch built out from the hall's west wall toward the open ground, its steep snowy ridge rising ABOVE the hall roof, carved finials crossed at its gable peak; its great double doors (4.5 m high and wide) stand OPEN, dark smoke rolls out of the doorway and up over the porch roof, an ember glow inside; two iron braziers burn on a flagged stone apron in front",
    "gable": "the hall's own COLLAPSED SOUTH-WEST END: the gable wall fallen outward onto its rubble, charred beams and planks in a heap, ash drifting out of it",
    "palisade": "a broken, half-burned timber palisade: leaning sharpened stakes with gaps, some fallen, snow against the bases",
    "cliff": "the sea cliff's face: layered dark wet rock with snow on the ledges, dropping to the sea",
    "cave": "the SEA CAVE: a HUGE dark cave mouth (about 9 m wide, 7 m high) in the cliff face at the water, waves and ice at its foot",
    "fallen_stone": "an old circle stone fallen flat and half buried in snow, rimed, with old carving",
    "grave_marker": "a low old grave marker, half sunk",
    "driftwood": "a grey driftwood log on the shingle",
    "beam": "a charred roof beam lying flat in the ash",
}
DOOR = {"barrow_door": "the BARROW DOOR, monumental (over 6.5 m high, 5 m wide): a stone-lined forecourt cutting into the mound's front, two colossal carved door posts and a massive carved lintel, the deep dark passage behind; it faces the open ground and is the grandest thing in the whole site",
        "hall_great_door": "the hall's great double door (inside the porch)"}


SK_TIES = {"p01": [160, 399], "p02": [814, 134], "p03": [636, 612], "p04": [1289, 420], "p05": [649, 366],
           "p06": [1421, 561], "start": [783, 452]}


def hull(pts):
    pts = sorted(set((round(p[0], 2), round(p[1], 2)) for p in pts))
    if len(pts) < 3:
        return pts
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def notes():
    out = {}
    feats = list(L["features"])
    st = L["stair"]
    items = []
    for f in feats:
        fp = f["footprint"]
        z1 = float(f.get("z_top_m", 0)); z0 = float(f.get("z_bottom_m", 0))
        pts = [px(p[0], p[1], z) for p in fp for z in (z0, z1)]
        w = DOOR.get(f["id"]) if f["kind"] == "door" else WORDS.get(f["kind"])
        if w:
            items.append((f["id"], f["kind"], w, pts))
    fl = st["flight"]["polygon"]
    items.append(("sea_cave_stair", "stair", "the STAIR: a straight, wide, rough stone stair cut into the cliff face, climbing FROM the rock ledge at the sea-cave mouth UP the face to the cliff top; open on its sea side, the cliff face its wall",
                  [px(p[0], p[1], z) for p in fl for z in (0.0, float(st["flight"]["z_bottom_m"]))]))
    m = L["mere"]["polygon"]
    items.append(("mere", "mere", "the FROZEN MERE: a large irregular frozen shallow lake, flat lapis ice with dark cracks, frozen reeds along its edges", [px(p[0], p[1]) for p in m]))
    items.append(("stream", "stream", "the frozen STREAM winding down from the barrow slope into the mere", [px(p[0], p[1]) for p in L["stream"]["polyline"]]))
    masks = {}
    cen = {fid: (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)) for fid, kind, w, pts in items}
    for ch in FR["chunks"]:
        x0, y0, x1, y1 = ch["px"]
        names, seen = [], set()
        for fid, kind, w, pts in items:
            m = masks.get(fid)
            if m is None:
                from PIL import Image, ImageDraw
                im = Image.new("1", (FR["size_px"][0] // 16 + 1, FR["size_px"][1] // 16 + 1), 0)
                hp = hull([(p[0] / 16, p[1] / 16) for p in pts]) if kind not in ("stream",) else [(p[0] / 16, p[1] / 16) for p in pts]
                d = ImageDraw.Draw(im)
                (d.line(hp, fill=1, width=3) if kind == "stream" else d.polygon(hp, fill=1, outline=1))
                import numpy as np
                m = masks[fid] = np.asarray(im)
            if not m[y0 // 16:y1 // 16 + 1, x0 // 16:x1 // 16 + 1].any():
                continue
            own = (min(int(cen[fid][0] // 1280), FR["chunk"]["cols"] - 1), min(int(cen[fid][1] // 768), FR["chunk"]["rows"] - 1))
            if kind in ("door", "porch", "cave") and own != (x0 // 1280, y0 // 768):
                continue          # a one-of-a-kind opening is named ONLY in the panel holding its centre (chunk test: 8_6 grew a 2nd door)
            if w in seen:
                continue
            seen.add(w); names.append(w)
        out[ch["key"]] = (("it shows " + "; ".join(names) + ".") if names else "open land and its ground cover only.") + (
            " The whole site has exactly ONE barrow door, ONE hall porch with its open double doors, ONE sea cave and ONE stair: "
            "if a painted strip already shows one of them, continue it and never paint a second.")
    return out


GEO = ("a FLAT COLOUR-CODED ZONE MAP of a real game level, seen from the game's fixed high camera (orthographic, 53 degrees "
       "down, NORTH AT THE TOP) at true scale: 1 metre = 100 px across, a person would stand about 115 px tall. It is NOT a "
       "picture; it only says WHERE things are. ZONE COLOURS: pale warm white = open snow; pale rust-pink = a grave-ground of "
       "rust heather and dead grass poking through snow, with a few old half-sunk grave markers; pale grey-beige = shingle "
       "shore ground (grey pebbles, driftwood and kelp under thin snow); pale warm grey = wind-scoured cliff-top rock with thin "
       "snow; mid grey-brown = the trampled ash, soot and frozen mud of a burnt hall's yard; pale blue = frozen fresh water "
       "(flat lapis ice with dark cracks, frozen reeds at its edges); a light cream stripe = a worn footpath; pale blue-grey = "
       "snow-covered land beyond, a touch darker where it rises; olive-tan = the great BARROW MOUND (earth and dead grass under "
       "deep wind-drifted snow); grey-brown bands = steep rock faces and broken rocky slopes; grey-tan = a shingle beach; very "
       "pale blue = shore ice and broken sea ice; dark slate blue = open sea far below the cliffs. FLAT MARKS: the DARK BROWN "
       "slab = the footprint of the BURNT LONGHALL (a ruined timber hall stands on it and rises to the thin brown outline above "
       "it: charred posts and rafters, half its roof fallen in, snow on what roof is left); ORANGE = the hall's grand gabled ENTRANCE "
       "PORCH on its west side, the tallest thing on the hall: its steep snowy ridge rises ABOVE the hall roof, carved finials cross at its "
       "gable peak, its great double doors (4.5 m high and wide) stand OPEN with dark smoke rolling out and up over the porch roof and an "
       "ember glow inside, two iron braziers burn on a flagged stone apron in front of it; the LIGHTER BROWN block at the "
       "hall's south-west end = its COLLAPSED END, the gable wall fallen outward onto a heap of charred beams and rubble; thin "
       "brown lines = a broken, half-burned PALISADE of leaning sharpened stakes with gaps; the MID BROWN long block at the west "
       "shore = an old wooden longship WRECK beached and frozen into the shore ice, heeled over toward the open ground, its low "
       "broken rail on that side; the NEARLY BLACK bar in the mound's front = the BARROW DOOR, MONUMENTAL (over 6.5 m high and 5 m wide, a giant could walk out of it): "
       "a stone-lined forecourt cutting, two colossal carved door posts and a massive carved lintel, a deep dark passage behind; small grey marks out on the slopes = tall weathered "
       "standing stones; small grey marks inside the open ground = old circle stones FALLEN FLAT and half buried; the tan stair "
       "shape in the south cliff = a broad rough stone STAIR (5 m wide) climbing the cliff face from a rock ledge at the sea up to the cliff top, "
       "and the black shape beside its foot = a HUGE dark SEA-CAVE mouth in the cliff (about 9 m wide and 7 m high). SMALL DARKER SPECKLES = "
       "GROUND COVER, one clump per speckle: rust heather and dry-grass clumps on the pink, pebbles, kelp and driftwood bits on the shingle, "
       "ash, charred debris and embers in the yard, tufts, low drifts and footprints on the snow; dark green blobs = juniper bushes; grey "
       "blobs = rocks and boulders; a thin brown stroke with a ring = a bare birch. A thin outline above a mark shows how high that "
       "thing rises. The faint DOTTED grey line and the faint DOTTED gold ellipses are measuring marks only: do NOT paint them.")
RULES = ("Paint the scene this map describes, in the hand, palette, mood and composition of IMAGE 2 (the chosen sketch of this "
         "same site; it shows the whole site, so this panel is a small part of it seen much closer: paint at THIS scale). INVENT "
         "every shape: organic rocks with fractured strata, wind-scalloped drifts and snow banks; a barrow mound with a real "
         "silhouette and kerb stones; a ruined, charred hall; a broken old ship; real sea cliffs with ledges. No flat colour of "
         "the map may remain, and nothing may look like a block or a box. DENSITY: match IMAGE 2 and the detail in the last image -- the "
         "ground is RICH and BUSY everywhere, never bare: on the open ground a dense carpet of LOW heather and dry-grass clumps, scattered "
         "pebbles and small flat stones, drift ripples, footprints, ash and charred debris in the yard, heather thick on the grave-ground; "
         "outside the open ground denser still: boulders, rock clusters, juniper bushes, bare birches, kerb stones, heather banks. Keep every structure at its place and size on the map, "
         "and every opening (the barrow door, the porch doorway, the cave mouth, the stair, the ship's low rail) where the map "
         "puts it. THE OPEN GROUND (inside the dotted line: snow, heather ground, shingle, cliff-top rock, ash yard, the frozen "
         "mere, the path) STAYS OPEN, WALKABLE GROUND: low texture only (snow, small tufts, pebbles, cracks, embers, footprints) "
         "with NOTHING standing on it: no rocks, posts, trees, walls or stones above ankle height. The mini-biomes MELD into "
         "each other over a few metres (ash into snow, shingle into ice, heather into drift). Draw no line, fence, rim or ring "
         "along the edge of the open ground: its edge is the land itself. One low warm winter sun from the upper LEFT; short "
         "soft blue-violet shadows touching their objects. Hand: one thin warm dark-brown ink line on contours, transparent "
         "watercolour washes, cream paper highlights; a cold winter palette of blue-white snow, warm grey stone, rust heather, "
         "sooty ash and lapis ice. No sky, no horizon, no text, no labels, no UI, no border, no people, no creatures.")


def main():
    cfg = {
        "prefix": os.environ.get("BVP_PREFIX", "BVR"),   # BVP = chunk test 1 (layout v4); BVR = layout v5 + density (R-C9-154)
        "name": "barrow_v2 Fjord Headland, whole site: guided paint-over at the arena camera (plate density)",
        "guide": GUIDE, "cols": FR["chunk"]["cols"], "rows": FR["chunk"]["rows"], "skip": FR["skipped_chunks"],
        "experiment": "R-C9-147-barrow-v2-paintover", "run_tag": "Run C-9 Phase 2 lane BVP", "ruling": "R-C9-145/147/148/151",
        "_frame": "paint/frame_bvp.json: plate_X = P*x + X0, plate_Y = P*sin(a)*y - P*cos(a)*z + Y0, P = %.6f, origin %s, size %s" % (P, FR["origin_px"], FR["size_px"]),
        "_guide_sha256": hashlib.sha256(open(GUIDE, "rb").read()).hexdigest() if os.path.exists(GUIDE) else None,
        "geo": GEO, "rules": RULES,
        "refs": [[os.path.join(A9, "BV3r2-A", "BV3r2-A.png"),
                  "the CHOSEN SITE SKETCH of this same site (Matt's pick): the painted hand, palette, mood and composition to follow -- it is the whole site at a far smaller scale, not to scale"]],
        "fill_phrase": "paint the scene the zone map describes, replacing every flat map colour and mark with painting",
        "unpainted_phrase": "any flat map colour or mark (a dotted line, a flat block) remains unpainted",
        "retry_extra": "something tall stands on the open ground, ",
        "sketch_detail": {
            "image": os.path.join(A9, "BV3r2-A", "BV3r2-A.png"), "frame": os.path.join(BV2, "paint", "frame_bvp.json"),
            "_ties": "sim (x, y) -> sketch A px (1536 x 1024), read off sites/BV3r2-A_spawns.png (the same picture, annotated) at the six anchors and the start",
            "ties": [[a["x"], a["y"]] + SK_TIES[a["id"]] for a in L["anchors"]["points"]] + [[0.0, 0.0] + SK_TIES["start"]],
            "crop_px": [384, 256],
            "role": ("a DETAIL of the chosen sketch (IMAGE 2) around this panel's place in the site, enlarged: match its DENSITY "
                     "of ground cover and small detail -- heather and dry-grass clumps, scattered stones, drifts, footprints, debris -- "
                     "and its finish; NOT its exact shapes, layout or scale")},
        "chunk_notes": notes(),
    }
    out = os.path.join(BV2, "paint", "cfg_barrow_v2.json")
    json.dump(cfg, open(out, "w"), indent=1, ensure_ascii=False)
    print(out, "chunks", len(cfg["chunk_notes"]))


if __name__ == "__main__":
    main()
