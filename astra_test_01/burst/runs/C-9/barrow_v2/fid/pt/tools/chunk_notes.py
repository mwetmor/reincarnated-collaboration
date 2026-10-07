#!/usr/bin/env python3
"""BV2F DEV-10 (charter § 7): per-chunk painter notes GENERATED FROM THE ID RENDER (lane PT). No hand-written content:
every sentence is a template filled from the ID render's own pixels and the guide manifest's id_table.

    python3 fid/pt/tools/chunk_notes.py [--chunks 0_0,1_0,...] [--out fid/pt/pilot/chunk_notes.json]

Inputs (sha-checked against fid/pt/pilot/pins.json): fid/lv/guide_art/ids_art.png (R<<16|G<<8|B = id) and
fid/lv/guide_art/guide_manifest.json `id_table`. Chunk key = guided_paint.py's own '<col>_<row>'; the chunk's
pixels = guide crop (col*1280, row*768, +1536, +1024), the canvas guided_paint stages.

Per chunk the note names: what is in the panel (an object counts only if it covers >= MIN_PX of the canvas),
where (thirds of the canvas, from the object's pixel centroid), how many separate pieces of a grouped object
(connected components >= MIN_PX), and the panel's dark openings (`passage_dark` ids) -- or that it has none.
That last sentence is the invention guard (P6a): a panel with no declared opening is told so.
"""
import hashlib, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CW, CH, SX, SY = 1536, 1024, 1280, 768
MIN_PX = 1500          # ~0.1% of a canvas: below this a sliver is not named
# id -> (painter noun, countable?) -- nouns are the geo text's own words (fid/pt/geo_bv2art_draft.txt)
NOUN = {
    "barrow_front": ("the barrow's carved stone facade with its lintel and posts", False),
    "fallen_gable": ("the charred, collapsed gable", False),
    "ground_ash": ("the yard of trampled ash and soot", False),
    "ground_ice": ("the frozen mere", False),
    "ground_mound": ("the snowy flank of the barrow mound", False),
    "ground_path": ("the trodden path", False),
    "ground_rock": ("bare grey rock", False),
    "ground_sea": ("the open dark sea", False),
    "ground_shingle": ("the shingle beach", False),
    "ground_shore_ice": ("thick shore ice", False),
    "blobs_shore_ice": (("ice floe", "ice floes"), True),
    "ground_shrub": ("juniper and heather patches", False),
    "ground_snow": ("open snow", False),
    "ground_stream": ("the frozen stream", False),
    "logs": (("fallen log", "fallen logs"), True),
    "longhall": ("the half-burned longhall", False),
    "palisade": (("palisade post", "palisade posts"), True),
    "ring_stones": (("carved standing stone of the broken ring", "carved standing stones of the broken ring, upright or fallen"), True),
    "slope_stones": (("lone standing stone", "lone standing stones"), True),
    "stair_steps": ("the rock-cut stair", False),
    "wreck": ("the longship wreck", False),
    "cliff_faces": ("the layered granite sea cliff", False),
    "crags": (("granite crag", "granite crags"), True),
    "curtain_barrow_door": ("the barrow's great door (DARK doorway)", False),
    "curtain_hall_great_door": ("the longhall's great door (DARK doorway)", False),
    "curtain_sea_cave_mouth": ("the sea cave mouth (DARK opening)", False),
}
SKIP = {"door_post_R", "door_post_L", "door_lintel"}      # v1 instrument stubs (class none), drawn by barrow_front


def where(ys, xs):
    cy, cx = ys.mean() / CH, xs.mean() / CW
    v = "top" if cy < 1 / 3 else ("bottom" if cy > 2 / 3 else "middle")
    h = "left" if cx < 1 / 3 else ("right" if cx > 2 / 3 else "centre")
    return "centre" if (v, h) == ("middle", "centre") else "%s %s" % (v, h)


def main():
    a = sys.argv[1:]
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(FID, "pt", "pilot", "chunk_notes.json")
    chunks = a[a.index("--chunks") + 1].split(",") if "--chunks" in a else ["%d_%d" % (c, r) for r in range(3) for c in range(3)]
    pins = json.load(open(os.path.join(FID, "pt", "pilot", "pins.json")))
    ids_p = os.path.join(FID, "lv", "guide_art", "ids_art.png")
    s = hashlib.sha256(open(ids_p, "rb").read()).hexdigest()
    if s != pins["ids"]["sha256"]:
        sys.exit("[notes] HALT: ids_art.png %s != pinned %s" % (s[:12], pins["ids"]["sha256"][:12]))
    table = json.load(open(os.path.join(FID, "lv", "guide_art", "guide_manifest.json")))["id_table"]
    A = np.asarray(Image.open(ids_p).convert("RGB")).astype(np.int64)
    G = (A[..., 0] << 16) | (A[..., 1] << 8) | A[..., 2]
    res = {"_what": "BV2F DEV-10 per-chunk painter notes, generated from the ID render by fid/pt/tools/chunk_notes.py (no hand-written content)",
           "ids_sha256": s, "min_px": MIN_PX, "notes": {}, "inventory": {}}
    for k in chunks:
        c, r = map(int, k.split("_"))
        T = G[r * SY:r * SY + CH, c * SX:c * SX + CW]
        items, darks, inv = [], [], {}
        u, n = np.unique(T, return_counts=True)
        for gid, cnt in sorted(zip(u.tolist(), n.tolist()), key=lambda x: -x[1]):
            e = table.get(str(gid))
            if gid == 0 or e is None or e["id"] in SKIP or cnt < MIN_PX:
                continue
            noun, countable = NOUN[e["id"]]
            ys, xs = np.nonzero(T == gid)
            pos = where(ys, xs)
            if countable:
                lab, nl = ndimage.label(T == gid)
                sizes = ndimage.sum(np.ones_like(lab), lab, range(1, nl + 1))
                m = int((np.asarray(sizes) >= MIN_PX).sum())
                if m == 0:
                    continue
                phrase = "%d %s (%s)" % (m, noun[0] if m == 1 else noun[1], pos)
            else:
                phrase = "%s (%s)" % (noun, pos)
            inv[e["id"]] = {"px": int(cnt), "share": round(cnt / (CW * CH), 4), "where": pos}
            (darks if e["class"] == "passage_dark" else items).append(phrase)
        if darks:
            dark_s = "Its ONLY dark opening is %s; paint no other door, cave, hole or passage." % "; ".join(darks)
        else:
            dark_s = "It has NO dark opening: paint no door, cave, hole or passage anywhere in it."
        res["notes"][k] = ("THIS PANEL (%s), from the render's own object map: %s. %s Nothing else stands here: no other building, ship, standing stone, crag or cliff."
                           % (k, "; ".join(items), dark_s))
        res["inventory"][k] = inv
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"), indent=1)
    for k in chunks:
        print(res["notes"][k]); print()


main()
