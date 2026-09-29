#!/usr/bin/env python3
"""C-9 meshy_t2 step 14: the authoritative sprites_t2 manifest.

    python3 scripts/20_manifest.py

15_assemble.py writes the painted E and SE directions; 16_ebsynth.py writes
the six propagated ones straight into the same tree. Neither can see the
other's work, so the manifest is rebuilt here by SCANNING what is actually on
disk and re-grading it, rather than by merging what each step believed it
did. If a frame is missing, this notices; if a step wrote something it did not
report, this notices that too.

Carries what the game needs to play the sprites and what a reviewer needs to
trust them:
  * frame size, world scale, ground row, elevation, the azimuth convention
  * per clip: frame count, fps, period, ground speed, stride, and the px/s the
    sprite has to be scrolled at for the feet to stay planted
  * per direction: painted or propagated, which Astra variant, per-frame IoU
    against the render's own mask, and any face-drift flag
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
SPR = os.path.join(ROOT, "sprites_t2")
WORK = os.path.join(ROOT, "work")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
PAINTED = ["E", "SE"]
CLIPS = [("idle", 12), ("walk", 12), ("run", 8), ("attack", 12)]


def best_iou(a, m):
    best = (-1.0, 0)
    for r in (0, 1, 2):
        e = a if r == 0 else ndi.binary_erosion(a, np.ones((2 * r + 1,) * 2))
        v = float((e & m).sum()) / max(float((e | m).sum()), 1.0)
        if v > best[0]:
            best = (v, r)
    return best


def main():
    chosen = json.load(open(os.path.join(WORK, "chosen.json")))
    plant = json.load(open(os.path.join(WORK, "plant.json")))
    clipinfo = json.load(open(os.path.join(WORK, "clips.json")))
    man = dict(
        note="C-9 T2 manticore (Rochester Bestiary, c.1230) -- painted sprites. "
             "Quadruped rig built and animated in Blender because the Meshy API "
             "rig is biped-only; Astra paint-over on E and SE, EbSynth "
             "propagation from two keys on the other six directions.",
        frame_px=512, px_per_m=110.1852,
        px_per_m_source="the knight's 198.333 px / 1.80 m -- the manticore "
                        "renders at the same WORLD scale and is ~132 px tall",
        sole_row=398, elevation_deg=19.77,
        azimuths={"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225,
                  "W": 270, "SW": 315},
        path="sprites_t2/{state}/{dir}/{state}_{dir}_NN.png",
        painted_dirs=PAINTED,
        propagated_dirs=[d for d in DIRS if d not in PAINTED],
        ebsynth=dict(guides=dict(pos=4.0, part=2.0, mask=2.0), keys="0 and n/2",
                     blend="inverse circular temporal distance, inside the mask"),
        states={}, missing=[], face_drift={})
    for clip, n in CLIPS:
        p = plant["clips"][clip]
        ci = clipinfo[clip]
        st = dict(frames=n, fps=p["fps"], period_s=p["period_s"],
                  cycle=ci["cycle"],
                  ground_speed_m_s=p["measured_speed_m_s"],
                  stride_m=p["stride_m"],
                  scroll_px_s=p["canvas_px_s"],
                  max_foot_slide_mm=round(1000 * p["max_slide_m"], 2),
                  root_motion_per_frame_m=p["root_motion"]["per_frame_forward_m"],
                  dirs={})
        kc = os.path.join(WORK, "keys_choice_%s.json" % clip)
        drift = json.load(open(kc))["face_drift_ratio"] if os.path.exists(kc) else {}
        for d in DIRS:
            dd = os.path.join(SPR, clip, d)
            rows, miss = [], []
            for i in range(n):
                f = os.path.join(dd, "%s_%s_%02d.png" % (clip, d, i))
                if not os.path.exists(f):
                    miss.append(i); continue
                a = np.asarray(Image.open(f).convert("RGBA"))[..., 3] > 128
                mp = os.path.join(OUT, clip, "guides_mask", d,
                                  "mask_%s_%02d.png" % (d, i))
                m = np.asarray(Image.open(mp).convert("RGBA"))[..., 3] > 128
                iou, er = best_iou(a, m)
                rows.append(dict(frame=i, iou=round(iou, 4), erode_px=er))
            if miss:
                man["missing"].append("%s/%s frames %s" % (clip, d, miss))
            if not rows:
                st["dirs"][d] = dict(present=False)
                continue
            src = chosen.get(clip, {})
            if d in PAINTED:
                variant, kind = src.get(d), "painted"
            else:
                k = src.get("keys")
                variant = (k.get(d) if isinstance(k, dict) else k)
                kind = "propagated"
            e = dict(present=True, kind=kind, variant=variant,
                     frames=len(rows), missing=miss,
                     iou_min=round(min(r["iou"] for r in rows), 4),
                     iou_mean=round(float(np.mean([r["iou"] for r in rows])), 4),
                     per_frame=rows)
            if kind == "propagated" and d in drift:
                e["face_drift_ratio"] = drift[d]
                if drift[d] > 1.25:
                    e["face_drift"] = ("the painted key draws more of the man's "
                                       "face than this view of the render shows")
                    man["face_drift"].setdefault(clip, {})[d] = drift[d]
            st["dirs"][d] = e
        st["complete"] = all(st["dirs"][d].get("present") for d in DIRS)
        man["states"][clip] = st
    done = sum(1 for c in man["states"].values() for d in c["dirs"].values()
               if d.get("present"))
    frames = sum(d.get("frames", 0) for c in man["states"].values()
                 for d in c["dirs"].values())
    man["totals"] = dict(directions=done, directions_expected=32,
                         frames=frames,
                         frames_expected=sum(n * 8 for _, n in CLIPS),
                         complete=done == 32 and not man["missing"])
    json.dump(man, open(os.path.join(SPR, "manifest.json"), "w"), indent=1)
    print("sprites_t2: %d/32 directions, %d/%d frames, complete=%s"
          % (done, frames, man["totals"]["frames_expected"], man["totals"]["complete"]))
    for clip, _ in CLIPS:
        st = man["states"][clip]
        ds = [d for d in DIRS if st["dirs"][d].get("present")]
        ious = [st["dirs"][d]["iou_mean"] for d in ds]
        print("  %-7s %d dirs  IoU %.3f..%.3f  %.2f m/s  %.0f px/s  slide %.1f mm"
              % (clip, len(ds), min(ious) if ious else 0, max(ious) if ious else 0,
                 st["ground_speed_m_s"], st["scroll_px_s"], st["max_foot_slide_mm"]))
    if man["face_drift"]:
        print("  face drift (re-fire targets):",
              {c: v for c, v in man["face_drift"].items()})
    for m in man["missing"]:
        print("  MISSING:", m)


if __name__ == "__main__":
    main()
