#!/usr/bin/env python3
"""MD-B4app-2 — the referent's MOVE / CHANNEL duty cycle, measured off camera.

The question (KC2-MC B-4app § 7, gandalf DRIFT-CRITIC `F-11`): the sim's pilot
channels Eye of Reckoning through 87.7 % of its channel ticks *while walking*.
The referent physically cannot -- D-9 decoded `MoveToAction -> StopCurrentSkill`.
So: what fraction of the referent's combat time is he actually channelling, and
what is the episode structure of the stops?

TWO INDEPENDENT INSTRUMENTS, neither of which asks the player what he intended.

  (1) MOTION -- camera-pan registration of the play-area band. The Grim Dawn
      camera is player-locked, so scene translation IS player translation. Sampled
      at 10 Hz; sub-pixel phase correlation on the achromatic component with
      saturated combat VFX down-weighted 1/(1+6*sat), Hann-windowed.
      A sample is MOVING when |d| exceeds the measured static-floor.

  (2) ENERGY -- the HUD energy readout `cur/max`, glyph-atlas OCR at the same
      10 Hz. EoR's own tooltip (read on this footage at t=215, note 2026-08-08 § 3)
      publishes `176.4 Energy Cost per Second`. A sustained negative ramp in E is
      a channel; a step is an instant cast; a positive ramp is regen with the
      channel down. The drain rate is the game's own published number, so the
      classifier threshold is not fitted -- it is quoted.

The two instruments are INDEPENDENT (one reads the world, one reads the HUD) and
D-9 predicts they must agree: drain must not survive movement. § agreement in the
note is therefore a test of the decode, not a calibration of the tool.

  energy <video> <t0> <t1> <atlas.npz> <out.json> [hz]
  atlas  <video> <spec.json> <out.npz>
  motion <video> <t0> <t1> <out.json> [hz]
"""
import sys, os, json, subprocess
import numpy as np
from PIL import Image

W, H = 1920, 1080
FPS = 60.0

# --- HUD energy readout box (1920x1080, 100% UI scale) ---------------------
# located, not assumed: achromatic-bright column runs inside x 1180..1400,
# y 1000..1035 give exactly 9 glyph runs spanning x 1252..1328 for "1456/2576".
EBOX = (1240, 1004, 104, 26)     # x, y, w, h -- w and h EVEN: ffmpeg's crop on a
                                 # yuv420p source silently rounds an odd width DOWN,
                                 # which desynchronises a rawvideo byte stream. Caught
                                 # at 105 -> 104 on the pilot; recorded so it is not
                                 # re-introduced.
THRESH = 140                     # min-channel; same calibration as eor_playerhp
CH_H, CH_W = 18, 12

# --- play-area band for camera registration --------------------------------
# HUD, minimap, floating combat text column and the top status strip excluded.
BAND = (150, 930, 40, 1620)      # y0, y1, x0, x1
DS = 2


# ===========================================================================
#  HUD numeral OCR  (same instrument family as eor_playerhp.py)
# ===========================================================================
def mask_of(rgb):
    """Achromatic-bright field. HUD numerals are cream/white; the orb is green."""
    a = rgb.astype(np.int16)
    mn = a.min(axis=2); mx = a.max(axis=2)
    return (mn > THRESH) & ((mx - mn) < 45)


def segment(m):
    col = m.any(axis=0)
    runs, i, n = [], 0, len(col)
    while i < n:
        if col[i]:
            j = i
            while j + 1 < n and col[j + 1]:
                j += 1
            if j - i + 1 >= 2:
                runs.append((i, j))
            i = j + 1
        else:
            i += 1
    return runs


def norm(m, c0, c1):
    g = m[:, c0:c1 + 1]
    rs = np.where(g.any(axis=1))[0]
    if len(rs) == 0:
        return None
    g = g[rs.min():rs.max() + 1, :]
    canvas = np.zeros((CH_H, CH_W), bool)
    h, w = g.shape
    if h > CH_H or w > CH_W:
        g = np.array(Image.fromarray(g).resize((min(w, CH_W), min(h, CH_H))))
        h, w = g.shape
    canvas[(CH_H - h) // 2:(CH_H - h) // 2 + h, (CH_W - w) // 2:(CH_W - w) // 2 + w] = g
    return canvas


def grab_box(video, t, box):
    tmp = f"/tmp/_eorch_{os.getpid()}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", video,
                    "-frames:v", "1", "-vf",
                    f"crop={box[2]}:{box[3]}:{box[0]}:{box[1]}", "-y", tmp], check=True)
    a = np.array(Image.open(tmp).convert("RGB"))
    os.remove(tmp)
    return a


def build_atlas(video, spec, out):
    protos = {}
    for job in spec:
        m = mask_of(grab_box(video, job["t"], EBOX))
        runs = segment(m)
        s = job["s"]
        if len(runs) != len(s):
            print(f"  SKIP t={job['t']}: {len(runs)} runs vs {len(s)} chars '{s}'",
                  file=sys.stderr)
            continue
        for (c0, c1), ch in zip(runs, s):
            g = norm(m, c0, c1)
            if g is not None:
                protos.setdefault(ch, []).append(g)
    keys = sorted(protos)
    arr = np.stack([np.mean(np.stack(protos[k]).astype(np.float32), axis=0) for k in keys])
    np.savez(out, keys=np.array(keys), protos=arr,
             counts=np.array([len(protos[k]) for k in keys]))
    print("atlas:", {k: len(protos[k]) for k in keys})


def classify(g, keys, protos):
    d = ((protos - g.astype(np.float32)[None]) ** 2).sum(axis=(1, 2))
    i = int(np.argmin(d))
    srt = np.sort(d)
    return keys[i], float(srt[0]), float(srt[1] - srt[0]) if len(srt) > 1 else 1e9


def read_mask(m, keys, protos):
    runs = segment(m)
    if not runs:
        return None, 0.0
    out, worst = [], 1e9
    for c0, c1 in runs:
        g = norm(m, c0, c1)
        if g is None:
            return None, 0.0
        ch, d, marg = classify(g, keys, protos)
        out.append(ch)
        worst = min(worst, marg)
    return "".join(out), worst


def trace_energy(video, t0, t1, atlas, out, hz):
    z = np.load(atlas, allow_pickle=True)
    keys = list(z["keys"]); protos = z["protos"]
    x, y, w, h = EBOX
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}",
           "-i", video, "-vf", f"fps={hz},crop={w}:{h}:{x}:{y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    rows, fsz, k = [], w * h * 3, 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        s, marg = read_mask(mask_of(fr), keys, protos)
        cur = mx = None
        if s and "/" in s:
            a, _, b = s.partition("/")
            if a.isdigit() and b.isdigit():
                cur, mx = int(a), int(b)
        rows.append({"t": round(t0 + k / hz, 4), "s": s, "cur": cur, "max": mx,
                     "marg": round(marg, 1)})
        k += 1
    p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "hz": hz, "box": EBOX,
               "rows": rows}, open(out, "w"))
    ok = sum(1 for r in rows if r["cur"] is not None)
    print(f"energy: {len(rows)} samples, {ok} parsed ({100.0*ok/max(1,len(rows)):.1f} %)")


# ===========================================================================
#  Camera-pan registration -> player motion
# ===========================================================================
def prep(fr):
    a = fr[BAND[0]:BAND[1], BAND[2]:BAND[3]].astype(np.float32)
    mx = a.max(axis=2); mn = a.min(axis=2)
    sat = (mx - mn) / (mx + 1.0)
    v = mn * (1.0 / (1.0 + 6.0 * sat))       # achromatic, VFX-suppressed
    v = v[::DS, ::DS]
    v = v - v.mean()
    hy = np.hanning(v.shape[0])[:, None]
    hx = np.hanning(v.shape[1])[None, :]
    return v * hy * hx


def phase_corr(a, b):
    """peak of the normalised cross-power spectrum; returns (dy, dx, peak, ratio).

    dx,dy are the shift (in DS-resolution px) that takes b onto a.
    `ratio` = peak / 2nd-highest-outside-a-3px-neighbourhood: the lock quality.
    """
    A = np.fft.rfft2(a); B = np.fft.rfft2(b)
    R = A * np.conj(B)
    R /= (np.abs(R) + 1e-9)
    c = np.fft.irfft2(R, s=a.shape)
    idx = int(np.argmax(c))
    py, px = divmod(idx, c.shape[1])
    peak = float(c[py, px])
    # suppress a 7x7 neighbourhood, take the runner-up -> lock ratio
    cc = c.copy()
    for ddy in range(-3, 4):
        for ddx in range(-3, 4):
            cc[(py + ddy) % c.shape[0], (px + ddx) % c.shape[1]] = -1e9
    second = float(cc.max())
    # sub-pixel parabolic refinement
    def par(vm, v0, vp):
        d = (vm - vp)
        n = 2.0 * (vm - 2.0 * v0 + vp)
        return d / n if abs(n) > 1e-12 else 0.0
    sy = par(c[(py - 1) % c.shape[0], px], peak, c[(py + 1) % c.shape[0], px])
    sx = par(c[py, (px - 1) % c.shape[1]], peak, c[py, (px + 1) % c.shape[1]])
    dy = py + np.clip(sy, -1, 1); dx = px + np.clip(sx, -1, 1)
    if dy > c.shape[0] / 2: dy -= c.shape[0]
    if dx > c.shape[1] / 2: dx -= c.shape[1]
    return float(dy), float(dx), peak, float(peak / (second + 1e-9))


def trace_motion(video, t0, t1, out, hz):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}",
           "-i", video, "-vf", f"fps={hz}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    fsz = W * H * 3
    prev, rows, k = None, [], 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        cur = prep(fr)
        if prev is not None:
            dy, dx, pk, ratio = phase_corr(prev, cur)
            rows.append({"t": round(t0 + k / hz, 4),
                         "dx": round(dx * DS, 3), "dy": round(dy * DS, 3),
                         "mag": round(float(np.hypot(dx, dy)) * DS, 3),
                         "peak": round(pk, 5), "lock": round(ratio, 3)})
        prev = cur
        k += 1
    p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "hz": hz, "band": BAND,
               "ds": DS, "rows": rows}, open(out, "w"))
    print(f"motion: {len(rows)} intervals")


# ===========================================================================
#  INDEPENDENT CROSS-CHECK: minimap registration
# ===========================================================================
#  The minimap is a player-centred, north-up render of the arena on a separate
#  draw path that carries NO combat VFX (established: note 2026-08-08 § 0). If
#  the player translates, the arena plan translates on the disc; if he does not,
#  it does not. Monster icons move independently and are clipped out by an
#  upper-luminance cut before registration. This shares NO pixels and NO failure
#  mode with the play-area instrument.
MINI = (1668, 46, 216, 198)      # x, y, w, h -- full-frame minimap box
MC, MR = (108, 101), 88          # disc centre in crop coords, analysis radius
ICON_CUT = 150                   # luminance above which a pixel is icon, not map


def mini_prep(fr):
    a = fr.astype(np.float32)
    lum = a.mean(axis=2)
    yy, xx = np.mgrid[0:fr.shape[0], 0:fr.shape[1]]
    disc = ((xx - MC[0]) ** 2 + (yy - MC[1]) ** 2) <= MR * MR
    v = np.where(lum > ICON_CUT, 0.0, lum)      # icons -> 0, they are not the map
    v = np.where(disc, v, 0.0)
    v = v - v[disc].mean()
    v = np.where(disc, v, 0.0)
    return v


def trace_mini(video, t0, t1, out, hz):
    x, y, w, h = MINI
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}",
           "-i", video, "-vf", f"fps={hz},crop={w}:{h}:{x}:{y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    fsz = w * h * 3
    prev, rows, k = None, [], 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        cur = mini_prep(np.frombuffer(buf, np.uint8).reshape(h, w, 3))
        if prev is not None:
            dy, dx, pk, ratio = phase_corr(prev, cur)
            rows.append({"t": round(t0 + k / hz, 4), "dx": round(dx, 3),
                         "dy": round(dy, 3),
                         "mag": round(float(np.hypot(dx, dy)), 3),
                         "lock": round(ratio, 3)})
        prev = cur
        k += 1
    p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "hz": hz, "box": MINI,
               "rows": rows}, open(out, "w"))
    print(f"minimap: {len(rows)} intervals")


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "atlas":
        build_atlas(sys.argv[2], json.load(open(sys.argv[3])), sys.argv[4])
    elif c == "energy":
        hz = float(sys.argv[7]) if len(sys.argv) > 7 else 10.0
        trace_energy(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
                     sys.argv[5], sys.argv[6], hz)
    elif c == "minimap":
        hz = float(sys.argv[6]) if len(sys.argv) > 6 else 20.0
        trace_mini(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
                   sys.argv[5], hz)
    elif c == "motion":
        hz = float(sys.argv[6]) if len(sys.argv) > 6 else 10.0
        trace_motion(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
                     sys.argv[5], hz)
    else:
        print(__doc__)
