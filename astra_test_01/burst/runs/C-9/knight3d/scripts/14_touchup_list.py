#!/usr/bin/env python3
"""C-9 knight3d: the ASTRA TOUCH-UP LIST.

Which parts of the body no still could see, where they are, and how much of
what the camera actually renders they account for. These are the patches
gandalf fires Astra bursts for; nothing here is invented paint.

Two numbers per piece, and they answer different questions:
  atlas_unseen_pct   -- share of that piece's TEXELS with no painted source.
                        Large for every piece, because a closed solid's inside
                        and back can never be seen and never need to be.
  render_unseen_pct  -- share of the pixels the piece actually CONTRIBUTES TO
                        A RENDERED FRAME that fall on unpainted texels. This
                        is the one that matters; the first one on its own
                        would send Astra after surfaces nobody will ever see.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import knight_proxy as kp
from raster import raster, tri_normals

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d"); OUT = os.path.join(K3, "out")
WORK = os.path.join(K3, "work"); SHEETS = os.path.join(K3, "overlays")
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta = fit["theta_elevation_deg"]
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    tex = np.asarray(Image.open(os.path.join(OUT, "knight_paint.png")).convert("RGB"))
    unseen = np.asarray(Image.open(os.path.join(OUT, "paint_unseen.png"))) > 127
    pr = json.load(open(os.path.join(OUT, "paint_report.json")))
    tri_v = A["tri_v"].astype(np.float64); tri_uv = A["tri_uv"].astype(np.float64)
    tri_id = A["tri_id"]; names = [str(n) for n in A["names"]]

    W = H = 900
    scale = 430.0
    tiles, per_piece_px = [], {n: [0, 0] for n in names}
    for d in ("S", "E", "N", "W", "SE", "NW"):
        r, u = kp.basis(AZI[d], theta); c = kp.cam_dir(AZI[d], theta)
        flat = tri_v.reshape(-1, 3)
        xy = np.stack([flat @ r * scale + W / 2, -(flat @ u) * scale + H - 60], -1)
        xy = xy.reshape(len(tri_v), 3, 2)
        z = (-(flat @ c)).reshape(len(tri_v), 3)
        at = np.zeros((len(tri_v), 3, 3)); at[:, :, 0:2] = tri_uv
        at[:, :, 2] = tri_id[:, None]
        zb, ib, ab, _ = raster(xy, z, at, W, H)
        solid = ib >= 0
        tu = np.clip((ab[..., 0] * tex.shape[1]).astype(int), 0, tex.shape[1] - 1)
        tv = np.clip((ab[..., 1] * tex.shape[0]).astype(int), 0, tex.shape[0] - 1)
        col = np.full((H, W, 3), 245, np.uint8)
        col[solid] = tex[tv[solid], tu[solid]]
        bad = solid & unseen[tv, tu]
        col[bad] = (230, 40, 190)
        pid = np.where(solid, tri_id[np.clip(ib, 0, len(tri_v) - 1)], -1)
        for i, n in enumerate(names):
            m = pid == i
            per_piece_px[n][0] += int(m.sum())
            per_piece_px[n][1] += int((m & bad).sum())
        im = Image.fromarray(col)
        dr = ImageDraw.Draw(im)
        dr.text((12, 12), "%s  -- magenta = NO painted source" % d, fill=(20, 20, 20))
        tiles.append(im)
    sheet = Image.new("RGB", (450 * 6, 450), (250, 250, 250))
    for i, t in enumerate(tiles):
        sheet.paste(t.resize((450, 450), Image.LANCZOS), (i * 450, 0))
    p = os.path.join(SHEETS, "M-b_touchups.png")
    sheet.save(p)

    rows = []
    for n in names:
        tot, bad = per_piece_px[n]
        rows.append(dict(piece=n, bone=idx["parts"][n]["bone"],
                         atlas_unseen_pct=pr["per_piece_unseen"].get(n, {}).get("unseen_pct"),
                         rendered_px=tot, rendered_unseen_px=bad,
                         render_unseen_pct=round(100.0 * bad / tot, 2) if tot else None))
    rows.sort(key=lambda r: -(r["render_unseen_pct"] or 0))
    out = dict(note=__doc__.strip().splitlines()[0],
               views_sampled=["S", "E", "N", "W", "SE", "NW"],
               screenshot=p, pieces=rows,
               total_rendered_px=sum(r["rendered_px"] for r in rows),
               total_rendered_unseen_px=sum(r["rendered_unseen_px"] for r in rows))
    out["overall_render_unseen_pct"] = round(
        100.0 * out["total_rendered_unseen_px"] / max(out["total_rendered_px"], 1), 2)
    with open(os.path.join(OUT, "touchup_list.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("overall %.2f %% of rendered pixels have no painted source" %
          out["overall_render_unseen_pct"])
    print("%-20s %8s %10s  %s" % ("piece", "rend px", "unseen %", "bone"))
    for r in rows[:14]:
        if not r["rendered_px"]:
            continue
        print("%-20s %8d %9.1f %%  %s" % (r["piece"], r["rendered_px"],
                                          r["render_unseen_pct"], r["bone"]))
    print("wrote", p)


main()
