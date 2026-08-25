#!/usr/bin/env python3
"""Evidence exhibit: what each leg's EFFECT FIELD actually contains.

Left column: the frame as rendered. Right column: the field every series in this
run is computed on -- |frame - motion-compensated local plate| for the video
legs, |fx_on - fx_ctl| for the clean-room stills.

The right column is the honest object. Matt's instruction was to zoom in and
pause on individual frames; this is that, with the background removed so the
effect's own internal structure is the only thing left to look at.
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame_forensics as ff   # noqa: E402
import frame_forensics_run as fr   # noqa: E402


def field_at(path, fps, target_idx, w=1280, h=720):
    models, resids, oks, centres, shifts = ff._flow_pass(path, w, h, fps)
    ring, ringsh, idxs = [], [], []
    for i, frame in enumerate(ff.stream_frames(path, w, h, fps)):
        ring.append((frame.copy(), ff.luma(frame)))
        ringsh.append(shifts[i]); idxs.append(i)
        if len(ring) > 2 * ff.PLATE_HALFWIN + 1:
            ring.pop(0); ringsh.pop(0); idxs.pop(0)
        if len(ring) < 2 * ff.PLATE_HALFWIN + 1:
            continue
        c = ff.PLATE_HALFWIN
        if idxs[c] == target_idx:
            cf, L = ring[c]
            pl = ff.local_plate([lu for (_, lu) in ring], ringsh, c)
            return cf, np.abs(L - pl)
    return None, None


def tone(d, cap):
    x = np.clip(d / cap, 0, 1) ** 0.6
    return (x * 255).astype(np.uint8)


def main():
    out = fr.OUT
    panels = []

    cf, d = field_at(fr.REF, 30000 / 1001, 150)
    panels.append(("REFERENCE  D3 Whirlwind (Blizzard 2012 master)", cf, d))

    cf2, d2 = field_at(fr.OURS, 30.0, 150)
    panels.append(("OURS  06_melee_combo CATHEDRAL (2026-08-25 render)", cf2, d2))

    W = "/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25"
    on = np.array(Image.open(f"{W}/combat_fxon_05-sustain.png").convert("RGB"))
    ct = np.array(Image.open(f"{W}/combat_fxctl_05-sustain.png").convert("RGB"))
    dd = np.abs(on.astype(np.int16) - ct.astype(np.int16)).max(axis=2).astype(np.float32)
    on_s = np.array(Image.fromarray(on).resize((1280, 720), Image.BILINEAR))
    dd_s = np.array(Image.fromarray(dd).resize((1280, 720), Image.BILINEAR))
    panels.append(("CLEAN-ROOM whirlwind, 05-sustain (matched fx-off control)",
                   on_s, dd_s))

    tile_w, tile_h = 640, 360
    canvas = Image.new("RGB", (tile_w * 2, tile_h * len(panels)), (12, 12, 14))
    for r, (name, frame, d) in enumerate(panels):
        if frame is None:
            continue
        im = Image.fromarray(frame).resize((tile_w, tile_h), Image.LANCZOS)
        canvas.paste(im, (0, r * tile_h))
        cap = float(np.percentile(d[d > 0], 99)) if (d > 0).any() else 1.0
        fld = Image.fromarray(tone(d, max(cap, 1.0))).convert("RGB")
        fld = fld.resize((tile_w, tile_h), Image.LANCZOS)
        canvas.paste(fld, (tile_w, r * tile_h))
        print(f"row {r}: {name}   field p99={cap:.1f}  "
              f"nonzero={float((d>0).mean()):.4f}")
    canvas.save(os.path.join(out, "evidence_effect_fields.png"))
    print("wrote evidence_effect_fields.png")


if __name__ == "__main__":
    main()
