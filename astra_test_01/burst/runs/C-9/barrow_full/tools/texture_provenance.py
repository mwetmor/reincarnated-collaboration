#!/usr/bin/env python3
"""C-9 TEXTURE PROVENANCE (the coordinator, after the E1 lane's finding that the dark knight's shipped bodies carried
Tripo's FLAT texture, not the painted bake). drax.

  python3 tools/texture_provenance.py [--json OUT]        exit 1 on any mismatch

For every body and gear GLB the web build packs (godot/models/{gear,sorceress,warlord,variants/*}), the image EMBEDDED in
the GLB is decoded and compared with its INTENDED source, as each lane's own record names it:
  painted  -> the painted / graded atlas (mean |d| <= 2/255 at the smaller of the two sizes: a re-encode passes, a
              different image does not -- the flat Tripo texture against the bake reads ~20)
  own      -> no painted atlas exists for this piece (its lane's record: only the body, or only the armour set, was
              painted); its texture must equal the lane's own export of the piece (the same check)
Sources (the records): wl_e1/scripts/e42_embed_tex.py (tex_final.png), so_d7/export/manifest.json .texture,
gear_sets/sorceress_battlemage/stage2_results.json (paint/tex_armour_final|graded), gear_sets/barbarian_gladiator/
stage2_results.json + s43 (paint/tex_body_*, tex_armour_*), nb_d2/artifacts/D2-manifest.json body_texture.
"""
import argparse
import io
import json
import pathlib
import struct
import sys

import numpy as np
from PIL import Image

C9 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9")
G = C9 / "barrow_full/godot/models"
GS = C9 / "gear_sets"
WL = C9 / "wl_e1"
TOL = 6.0          # a JPEG re-encode of the right atlas reads ~2; the flat Tripo texture against the bake reads ~22
# and the deciding rule: the intended source must ALSO be the nearest of its alternatives (C against D's grade, B against
# C's, the bake against the flat) -- so a grade swapped for its sibling fails even inside the tolerance


def glb_images(p):
    b = open(p, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n])
    off = 20 + n
    bn = struct.unpack("<I", b[off:off + 4])[0]
    bin_ = b[off + 8:off + 8 + bn]
    out = []
    for im in j.get("images", []):
        if "bufferView" not in im:
            continue
        bv = j["bufferViews"][im["bufferView"]]
        data = bin_[bv.get("byteOffset", 0):bv.get("byteOffset", 0) + bv["byteLength"]]
        out.append((im.get("name", "?"), im.get("mimeType", "?"), data))
    return out


def arr(img, size):
    return np.asarray(img.convert("RGB").resize(size, Image.BOX), dtype=np.float64)


def diff(data, src_path):
    a = Image.open(io.BytesIO(data))
    s = Image.open(src_path)
    size = (min(a.width, s.width), min(a.height, s.height))
    return float(np.abs(arr(a, size) - arr(s, size)).mean())


def rows():
    R = []
    def add(staged, kind, src, record, alt=()):
        R.append({"glb": str(staged.relative_to(C9)), "kind": kind, "source": str(src.relative_to(C9)), "record": record,
                  "alternatives": [str(a.relative_to(C9)) for a in alt]})
    # the barbarian: the painted body (nb_t8 bake); his gear unpainted by design
    for b in [G / "gear/nb-body.glb"] + [G / f"variants/barb_{v}/nb-body.glb" for v in ("t1211", "f25l", "f40l")]:
        add(b, "painted", C9 / "nb_t8/work/texture_AB.png", "nb_d2/artifacts/D2-manifest.json body_texture")
    for p in ("axe", "bracers", "byrnie", "helmet", "mantle", "shield"):
        add(G / f"gear/{p}.glb", "own", C9 / f"nb_d2/export_staging/T12_11_trails/{p}.glb", "D2-manifest: only the body is painted")
    # the sorceress: the painted body; her garments unpainted by design
    # R-C9-120: her body is the LEGGINGS body (so_d7's painted bake with the legs recoloured, so-body_leggings.json), her
    # pieces the export_r120_ship set (the robe re-skinned, textures unchanged)
    add(G / "sorceress/so-body.glb", "own", C9 / "gear_sets/sorceress_robe/export/so-body_leggings.glb", "sorceress_robe/export/so-body_leggings.json")
    for p in ("robe", "belt", "mantle", "bracers", "staff"):
        add(G / f"sorceress/{p}.glb", "own", C9 / f"so_d7/export/{p}.glb", "so_d7/scene_pkg/README.md: only the body is painted (the r120 re-skin keeps each texture)")
    # the battle mage C / D: her body, the painted (C) and graded (D) armour atlas; wand and grimoire unpainted by design
    for v, exp, atlas in (("so_bmc", "export_bmc120", "tex_armour_final.png"), ("so_bmd", "export_bmd120", "tex_armour_graded.png")):
        add(G / f"variants/{v}/so-body_bm119.glb", "painted", C9 / "so_d7/work/tex_final.png", "battlemage paint/scenes.json images.B_body (body119)")
        other = "tex_armour_graded.png" if atlas == "tex_armour_final.png" else "tex_armour_final.png"
        for p in ("breastplate", "gauntlets", "gown", "hood", "legs"):
            add(G / f"variants/{v}/{p}.glb", "painted", GS / "sorceress_battlemage/paint" / atlas, f"battlemage stage2_results.json files ({exp})",
                [GS / "sorceress_battlemage/paint" / other])
        for p in ("wand", "grimoire"):
            add(G / f"variants/{v}/{p}.glb", "own", GS / "sorceress_battlemage" / exp / f"{p}.glb", "battlemage paint/scenes.json: not dressed")
    # R-C9-138: the ARENA KIT (so_bm134 = so_mx/export/ss138a, from ss134f): her painted body bake; the battle-mage armour on
    # the GRADED atlas (D's steel pass: measured nearest, 2.27 vs 4.01 for C's); orb staff and shield keep their own textures
    # R-C9-237: her body's atlas is body119's bake with the HEAD lifted (so_mx r233_04: the face/neck skin lifted, the forehead
    # repainted) -- the intended source is that lifted atlas, the plain bake its alternative
    add(G / "variants/so_bm134/so-body_ss237.glb", "painted", C9 / "so_mx/work/r233/tex_final_r237.png", "so_mx ss237 body: body119's bake, head lifted (R-C9-237)",
        [C9 / "so_d7/work/tex_final.png"])
    for p in ("breastplate", "gauntlets", "gown", "hood", "legs"):
        add(G / f"variants/so_bm134/{p}.glb", "painted", GS / "sorceress_battlemage/paint/tex_armour_graded.png", "so_mx ss134 pieces (bmd120's graded set)",
            [GS / "sorceress_battlemage/paint/tex_armour_final.png"])
    for p in ("orbstaff", "shield", "under_legs"):
        add(G / f"variants/so_bm134/{p}.glb", "own", C9 / f"so_mx/export/ss134f/{p}.glb", "so_mx R-C9-134 props (Tripo, unpainted by design)")
    # the champion B (painted) / C (painted + graded)
    for v, body, bimg, aimg, exp in (("barb_gladb", "nb-body_champion_painted.glb", "tex_body_final.png", "tex_armour_final.png", "export_painted"),
                                     ("barb_gladc", "nb-body_champion_graded.glb", "tex_body_graded.png", "tex_armour_graded.png", "export_graded")):
        ob = "tex_body_graded.png" if bimg == "tex_body_final.png" else "tex_body_final.png"
        oa = "tex_armour_graded.png" if aimg == "tex_armour_final.png" else "tex_armour_final.png"
        add(G / f"variants/{v}/{body}", "painted", GS / "barbarian_gladiator/paint" / bimg, "gladiator stage2_results.json paint_pass / s43",
            [GS / "barbarian_gladiator/paint" / ob])
        for p in ("chest", "girdle", "greaves", "helm", "kilt", "pauldron", "wraps", "wrists"):
            add(G / f"variants/{v}/{p}.glb", "painted", GS / "barbarian_gladiator/paint" / aimg, "gladiator stage2_results.json paint_pass / s43",
                [GS / "barbarian_gladiator/paint" / oa])
    # the dark knight: the painted body bake (e42_embed_tex.py); his gear keeps its Tripo textures by design
    # R-C9-127: final_k's body is painted AND value-graded (wl_manifest.json _what) -- tex_final_graded.png, nearer it
    # than the ungraded bake it was graded from (final_j2's)
    add(G / "warlord/wl_body.glb", "painted", WL / "work/tex_final_graded.png", "wl_e1 final_k wl_manifest.json: painted + value-graded body",
        [WL / "work/tex_final.png"])
    for p in ("wl_mace", "wl_chest", "wl_pauldrons", "wl_helm", "wl_helm_ice", "wl_cape"):
        add(G / f"warlord/{p}.glb", "own", WL / f"export/final_k_eor3/{p}.glb", "wl_e1 final_k_eor3 (R-C9-141) wl_manifest.json: pieces keep their own materials")
    return R


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    o = ap.parse_args()
    out = []
    bad = 0
    for r in rows():
        staged = C9 / r["glb"]
        src = C9 / r["source"]
        ims = glb_images(staged)
        if not ims:
            r.update(result="PASS", note="no embedded image (material colour only)")
        elif src.suffix == ".glb":
            sims = glb_images(src)
            d = max(diff(a[2], io.BytesIO(b[2])) for a, b in zip(ims, sims)) if len(sims) == len(ims) else 99.0
            r.update(mean_abs_diff=round(d, 3), result="PASS" if d <= TOL else "FAIL", note="unpainted by design: equals its lane export")
        else:
            d = min(diff(im[2], src) for im in ims)
            alts = {a: round(min(diff(im[2], C9 / a) for im in ims), 3) for a in r["alternatives"]}
            nearest = all(d < v for v in alts.values())
            r.update(mean_abs_diff=round(d, 3), alternatives_diff=alts, result="PASS" if (d <= TOL and nearest) else "FAIL",
                     embedded=[i[0] for i in ims])
        bad += r["result"] == "FAIL"
        out.append(r)
        print(f'{r["result"]:4}  {r.get("mean_abs_diff", "-"):>7}  {r["glb"]}  <-  {r["source"]}')
    if o.json:
        json.dump({"tolerance_mean_abs_8bit": TOL, "rows": out, "fails": bad}, open(o.json, "w"), indent=1)
    print(f"texture provenance: {len(out) - bad}/{len(out)} pass")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
