#!/usr/bin/env python3
"""
galadriel — WW-AB probe 2 (2026-08-24). Two questions probe 1 raised and did not settle.

Q1 GLOW BLEED. Probe 1 found trail-mask pixels within 12 px of the emissive register
   ~1.7x the delta of trail pixels further out. That is CONSISTENT with glow bleed, but
   it is equally consistent with "a trail is simply brightest at its root, near the
   blade." Those two explanations are not distinguishable from the delta alone, so the
   ratio proves nothing on its own. This settles it WITHOUT needing the trail at all:
   measure the CONTROL frame (fx off, no trail anywhere) for an elevated luminance halo
   around the emissive footprint. Light in the control frame beyond the blade silhouette
   cannot be trail. It can only be the emitter spreading.

Q2 QUIESCENCE / POSE DETERMINISM. My gate's check_determinism() states the licence for
   every control-difference it takes: arms must diff to ZERO lit px at the pre and off
   marks. s2b whirlwind satisfies that (0 / 0). The clean-room mint at commit 1692d6e
   does NOT (30 px at 00-pre, 184 px at 09-off). Characterise that: is it pose drift,
   or is it residual effect?
"""
import os, json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, distance_transform_edt

S2B = "/Users/admin/Games/reincarnated-godot/harness_logs/s2b_receipts_2026-08-24b"
WW  = "/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-24"

def load(cap, arm, mark):
    return np.asarray(Image.open(os.path.join(cap, f"{arm}_{mark}.png")).convert("RGB")).astype(np.float64)

def lum(im): return 0.2126*im[...,0]+0.7152*im[...,1]+0.0722*im[...,2]

def find_emissive(ctl):
    R,G,B = ctl[...,0],ctl[...,1],ctl[...,2]
    L = lum(ctl)
    cyan = (G-R)+(B-R)
    return (cyan > 40) & (L > np.percentile(L,99.0))

# ------------------------------------------------------------------ Q1
def bleed_profile(cap, arm_ctl, mark):
    """Luminance vs distance from the emissive footprint, IN THE CONTROL FRAME.
    No trail exists in this frame. Any elevation that decays with distance from the
    blade is the emitter spreading light -- glow, and the blade's own direct lighting."""
    c = load(cap, arm_ctl, mark)
    em = find_emissive(c)
    if em.sum() == 0: return None
    L = lum(c)
    dist = distance_transform_edt(~em)
    # cyan-ness in the control frame: glow carries the emitter's COLOUR outward,
    # which separates it from ordinary stage light far better than luminance alone.
    cyan = (c[...,1]-c[...,0]) + (c[...,2]-c[...,0])
    rings = [(0,4),(4,8),(8,12),(12,20),(20,32),(32,48),(48,80),(80,140),(300,600)]
    out = []
    for lo,hi in rings:
        m = (dist>lo)&(dist<=hi)
        if m.sum()==0: continue
        out.append(dict(ring_px=f"{lo}-{hi}", n=int(m.sum()),
                        mean_lum=round(float(L[m].mean()),2),
                        p95_lum=round(float(np.percentile(L[m],95)),2),
                        mean_cyan=round(float(cyan[m].mean()),2),
                        p95_cyan=round(float(np.percentile(cyan[m],95)),2)))
    return out

# ------------------------------------------------------------------ Q2
def quiescence(cap, arm_on, arm_ctl, marks):
    out = {}
    for mk in marks:
        a = load(cap,arm_on,mk); c = load(cap,arm_ctl,mk)
        d = np.abs(a-c); mag = d.sum(axis=2); m = mag>12
        r = dict(lit=int(m.sum()), maxdiff=int(d.max()))
        if m.sum():
            ys,xs = np.nonzero(m)
            em = find_emissive(c)
            eys,exs = np.nonzero(em)
            r.update(bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
                     centroid=[round(float(xs.mean()),1),round(float(ys.mean()),1)],
                     emissive_centroid=[round(float(exs.mean()),1),round(float(eys.mean()),1)] if em.sum() else None,
                     mean_mag=round(float(mag[m].mean()),1),
                     p99_mag=round(float(np.percentile(mag[m],99)),1))
            # signed: pose drift produces BOTH signs (geometry moved: brighter here,
            # darker there). A residual EFFECT is additive -> overwhelmingly positive.
            sd = (a-c)[m]
            r["frac_pixels_net_positive"] = round(float((sd.sum(axis=1)>0).mean()),3)
            # does the difference sit on the blade? -> pose drift of the weapon
            if em.sum():
                halo = binary_dilation(em, iterations=10)
                r["frac_diff_in_blade_halo"] = round(float((m&halo).sum())/max(1,int(m.sum())),3)
        out[mk] = r
    return out

if __name__ == "__main__":
    R = {}
    R["Q1_bleed_wwcr_04full"] = bleed_profile(WW,  "combat_fxctl", "04-full")
    R["Q1_bleed_s2b_04full"]  = bleed_profile(S2B, "rc_ww_ctl_fxctl", "04-full")
    R["Q2_quiescence_wwcr"] = quiescence(WW,  "combat_fxon", "combat_fxctl",
                                         ["00-pre","01-windup-early","09-off"])
    R["Q2_quiescence_s2b"]  = quiescence(S2B, "rc_ww_fxon", "rc_ww_ctl_fxctl",
                                         ["00-pre","01-windup-early","09-off"])
    print(json.dumps(R, indent=1))
