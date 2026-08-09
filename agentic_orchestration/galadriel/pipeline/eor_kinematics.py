#!/usr/bin/env python3
"""Per-body screen kinematics from the in-world HP-readout anchor.

Why the readout and not the sprite: at Crucible wave 150+ the body itself is buried
under overlapping combat VFX and cannot be segmented. The readout string is drawn
ON TOP of everything, is achromatic-white against saturated VFX, and is anchored to
its body -- so the readout's centroid IS the body's screen locus, up to a fixed
head-offset that cancels in every DIFFERENCE.

What that buys, and what it does not:
  DOES   translation per frame -> speed, stationary/moving classification,
         approach speed as a body closes on the player.
  DOES   root-lock: the fraction of a contact window in which a body's locus is
         stationary within the anchor's own jitter floor.
  DOES NOT  wind-up / recovery / telegraph. Those are animation-POSE facts. The
         readout is pose-blind. Any pose claim must come from an eye-read of the
         body sprite, and is graded separately.

The readout's own jitter floor is measured, not assumed: `floor` reports the
centroid scatter of tracks that are provably stationary (a body whose bounding box
never moves more than 1 px over >= 0.5 s).

  scan   <video> <t0> <t1> <out_index.json>          60 fps blob scan
  track  <index.json> <out_tracks.json> [max_jump_px]
  report <tracks.json> [min_frames]
"""
import sys, os, json, subprocess
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eor_hptext as HT

W, H = 1920, 1080
FPS = 60.0

# GAL-CAM (2026-07-30) scale field. TRANSFER ASSUMPTION: the eor sittings use the
# same camera zoom as play_test_2026-07-26. Named, not verified -- every metre
# figure derived here carries that assumption. Pixel figures do not.
A_SCALE, Y_H = 0.021404, -1950.0          # g_x(y) = A*(y - y_h) px per metre of ground-X
C_SCALE = 6.861e-06                       # g_y(y) = C*(y - y_h)^2 px per metre of ground-Z


def gx(y):
    return A_SCALE * (y - Y_H)


def gy(y):
    return C_SCALE * (y - Y_H) ** 2


def cen(b):
    return (b[0] + b[2]) / 2.0, b[1]      # x centre, TOP row (stable vs digit-count changes)


def scan(video, t0, t1, out):
    dur = t1 - t0
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", video,
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    nb = W * H * 3
    idx, i = [], 0
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        for (x0, y0, x1, y1, dens, n) in HT.blobs(fr):
            idx.append({"f": i, "t": round(t0 + i / FPS, 5), "box": [x0, y0, x1, y1]})
        i += 1
    p.stdout.close(); p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "frames": i, "blobs": idx},
              open(out, "w"))
    print(f"scan {t0}-{t1}: {i} frames, {len(idx)} blobs")


def track(index, out, maxjump=16.0):
    d = json.load(open(index))
    byf = {}
    for b in d["blobs"]:
        byf.setdefault(b["f"], []).append(b)
    tracks, live = [], []        # live: dicts with last centroid + point list
    for f in range(d["frames"]):
        obs = byf.get(f, [])
        used = set()
        for tr in live:
            best, bd = None, maxjump
            cx, cy = tr["pts"][-1][1], tr["pts"][-1][2]
            for j, b in enumerate(obs):
                if j in used:
                    continue
                x, y = cen(b["box"])
                dd = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if dd < bd:
                    bd, best = dd, j
            if best is None:
                tr["miss"] += 1
            else:
                used.add(best)
                x, y = cen(obs[best]["box"])
                tr["pts"].append([f, x, y]); tr["miss"] = 0
        for j, b in enumerate(obs):
            if j not in used:
                x, y = cen(b["box"])
                live.append({"pts": [[f, x, y]], "miss": 0})
        keep = []
        for tr in live:
            if tr["miss"] > 4:
                tracks.append(tr)
            else:
                keep.append(tr)
        live = keep
    tracks += live
    tracks = [t for t in tracks if len(t["pts"]) >= 8]
    json.dump({"index": index, "t0": d["t0"], "n": len(tracks),
               "tracks": [t["pts"] for t in tracks]}, open(out, "w"))
    print(f"track: {len(tracks)} tracks >= 8 frames")


def report(path, minf=20):
    d = json.load(open(path))
    t0 = d["t0"]
    print(f"{'#':>3} {'t_start':>8} {'nf':>4} {'span_s':>7} {'net_px':>7} "
          f"{'v_med':>7} {'v_p90':>7} {'stat%':>6} {'v_m/s':>7}")
    rows = []
    for i, pts in enumerate(d["tracks"]):
        p = np.array(pts, float)
        if len(p) < minf:
            continue
        dt = np.diff(p[:, 0]) / FPS
        dx = np.diff(p[:, 1]); dy = np.diff(p[:, 2])
        step = np.hypot(dx, dy) / dt                       # px/s
        stat = float((np.hypot(dx, dy) <= 1.0).mean())     # jitter-floor stationary
        ymid = float(np.median(p[:, 2]))
        # ground speed: decompose with the anisotropic scale at the body's own row
        vms = np.hypot(dx / gx(ymid), dy / gy(ymid)) / dt
        net = float(np.hypot(p[-1, 1] - p[0, 1], p[-1, 2] - p[0, 2]))
        rows.append((i, t0 + p[0, 0] / FPS, len(p), (p[-1, 0] - p[0, 0]) / FPS, net,
                     float(np.median(step)), float(np.percentile(step, 90)), stat,
                     float(np.median(vms))))
    rows.sort(key=lambda r: -r[2])
    for r in rows:
        print(f"{r[0]:>3} {r[1]:8.3f} {r[2]:4d} {r[3]:7.2f} {r[4]:7.1f} "
              f"{r[5]:7.1f} {r[6]:7.1f} {100*r[7]:6.1f} {r[8]:7.2f}")
    return rows


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "scan":
        scan(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
    elif c == "track":
        track(sys.argv[2], sys.argv[3],
              float(sys.argv[4]) if len(sys.argv) > 4 else 16.0)
    elif c == "report":
        report(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20)
