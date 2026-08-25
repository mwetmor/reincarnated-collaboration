#!/usr/bin/env python3
"""
galadriel — S2 gate, RT-2 colour separation done with the RIGHT instrument (2026-08-24)

WHY THIS FILE EXISTS. RT-2's trigger is: a TRAIL-BOUNDED row's element variants
"read as INDISTINGUISHABLE at the gameplay camera". Both drax and my own first pass
adjudicated that on HUE-ANGLE SEPARATION. That is the wrong instrument for this
palette, and it is wrong in a way that manufactures false collapses:

  hue angle is undefined at zero chroma and numerically unstable near it.

`neutral` renders at mean saturation 0.053 -- a near-achromatic cream. Its "hue" is
noise amplified by a division by a chroma of ~5/255. Any pair involving `neutral`
therefore produces a hue separation that is an artifact of the metric, not a
statement about whether a player can tell the two trails apart.

Two variants can be trivially distinguishable while sharing a hue angle (cream vs
saturated orange), and can share a hue angle while being obviously different
(different lightness). Perceptual separation needs lightness + chroma + hue
together. This file uses CIE L*a*b* / CIEDE2000.

Measured on TWO surfaces, because they answer different questions:
  (a) the effect's own added light      -> "did the tint take?"
  (b) the RENDERED trail pixels on screen -> "can the player tell them apart?"
(b) is the one RT-2 is actually about.
"""
import os, json, math, itertools
import numpy as np
from PIL import Image

CAP = "/Users/admin/Games/reincarnated-godot/harness_logs/s2a_2026-08-24-final"

def load(arm, mark):
    return np.asarray(Image.open(os.path.join(CAP, f"{arm}_{mark}.png")).convert("RGB")).astype(np.float64)

# ---- sRGB -> Lab (D65) ----
def srgb_to_lab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
    M = np.array([[0.4124564,0.3575761,0.1804375],
                  [0.2126729,0.7151522,0.0721750],
                  [0.0193339,0.1191920,0.9503041]])
    xyz = c @ M.T
    wp = np.array([0.95047, 1.00000, 1.08883])
    t = xyz / wp
    d = 6/29
    f = np.where(t > d**3, np.cbrt(t), t/(3*d*d) + 4/29)
    L = 116*f[...,1] - 16
    a = 500*(f[...,0]-f[...,1])
    b = 200*(f[...,1]-f[...,2])
    return np.stack([L,a,b], axis=-1)

def ciede2000(lab1, lab2):
    L1,a1,b1 = lab1; L2,a2,b2 = lab2
    C1 = math.hypot(a1,b1); C2 = math.hypot(a2,b2)
    Cb = (C1+C2)/2
    G = 0.5*(1 - math.sqrt(Cb**7/(Cb**7 + 25**7))) if Cb > 0 else 0.5
    a1p, a2p = (1+G)*a1, (1+G)*a2
    C1p, C2p = math.hypot(a1p,b1), math.hypot(a2p,b2)
    h1p = math.degrees(math.atan2(b1,a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2,a2p)) % 360 if (a2p or b2) else 0.0
    dLp = L2-L1; dCp = C2p-C1p
    if C1p*C2p == 0: dhp = 0.0
    else:
        dh = h2p-h1p
        dhp = dh - 360 if dh > 180 else (dh + 360 if dh < -180 else dh)
    dHp = 2*math.sqrt(C1p*C2p)*math.sin(math.radians(dhp)/2)
    Lbp = (L1+L2)/2; Cbp = (C1p+C2p)/2
    if C1p*C2p == 0: hbp = h1p+h2p
    else:
        s = h1p+h2p
        hbp = (s+360)/2 if abs(h1p-h2p) > 180 and s < 360 else ((s-360)/2 if abs(h1p-h2p) > 180 else s/2)
    T = (1 - 0.17*math.cos(math.radians(hbp-30)) + 0.24*math.cos(math.radians(2*hbp))
         + 0.32*math.cos(math.radians(3*hbp+6)) - 0.20*math.cos(math.radians(4*hbp-63)))
    dTh = 30*math.exp(-((hbp-275)/25)**2)
    Rc = 2*math.sqrt(Cbp**7/(Cbp**7+25**7)) if Cbp > 0 else 0
    Sl = 1 + (0.015*(Lbp-50)**2)/math.sqrt(20+(Lbp-50)**2)
    Sc = 1 + 0.045*Cbp
    Sh = 1 + 0.015*Cbp*T
    Rt = -math.sin(math.radians(2*dTh))*Rc
    return math.sqrt((dLp/Sl)**2 + (dCp/Sc)**2 + (dHp/Sh)**2 + Rt*(dCp/Sc)*(dHp/Sh))

def trail_stats(elem, mark="02-s1-swing", ctl="melee_ctl", thr=12):
    a = load(f"melee_{elem}", mark); c = load(ctl, mark)
    d = a - c
    mag = np.abs(d).sum(axis=2)
    m = mag > thr
    added = np.clip(d[m], 0, None)
    rendered = a[m]
    # energy-weight by added magnitude so the trail CORE dominates, as it does visually
    w = mag[m]
    add_mean = (added * w[:,None]).sum(0)/w.sum()
    ren_mean = (rendered * w[:,None]).sum(0)/w.sum()
    lab_add = srgb_to_lab(np.clip(add_mean,0,255))
    lab_ren = srgb_to_lab(np.clip(ren_mean,0,255))
    C_add = math.hypot(lab_add[1], lab_add[2])
    C_ren = math.hypot(lab_ren[1], lab_ren[2])
    return dict(n=int(m.sum()),
                added_rgb=[round(float(x),2) for x in add_mean],
                rendered_rgb=[round(float(x),2) for x in ren_mean],
                lab_added=[round(float(x),2) for x in lab_add],
                lab_rendered=[round(float(x),2) for x in lab_ren],
                chroma_added=round(C_add,2), chroma_rendered=round(C_ren,2),
                L_rendered=round(float(lab_ren[0]),2))

def aura_stats(elem, mark="00-steady", ctl="aura_novfx", thr=12):
    a = load(f"aura_{elem}", mark); c = load(ctl, mark)
    d = a - c; mag = np.abs(d).sum(axis=2); m = mag > thr
    w = mag[m]
    added = np.clip(d[m],0,None); rendered = a[m]
    add_mean = (added*w[:,None]).sum(0)/w.sum()
    ren_mean = (rendered*w[:,None]).sum(0)/w.sum()
    lab_ren = srgb_to_lab(np.clip(ren_mean,0,255))
    lab_add = srgb_to_lab(np.clip(add_mean,0,255))
    return dict(n=int(m.sum()),
                added_rgb=[round(float(x),2) for x in add_mean],
                rendered_rgb=[round(float(x),2) for x in ren_mean],
                lab_rendered=[round(float(x),2) for x in lab_ren],
                chroma_rendered=round(math.hypot(lab_ren[1],lab_ren[2]),2),
                lab_added=[round(float(x),2) for x in lab_add],
                chroma_added=round(math.hypot(lab_add[1],lab_add[2]),2))

if __name__ == "__main__":
    out = {}
    els = ["neutral","fire","water","earth","wind"]
    ts = {e: trail_stats(e) for e in els}
    out["melee_trail_stats"] = ts
    pa, pr = {}, {}
    for a,b in itertools.combinations(els,2):
        pa[f"{a}|{b}"] = round(ciede2000(ts[a]["lab_added"], ts[b]["lab_added"]),2)
        pr[f"{a}|{b}"] = round(ciede2000(ts[a]["lab_rendered"], ts[b]["lab_rendered"]),2)
    out["melee_dE2000_added"]    = dict(sorted(pa.items(), key=lambda kv: kv[1]))
    out["melee_dE2000_rendered"] = dict(sorted(pr.items(), key=lambda kv: kv[1]))

    ae = ["fire","water","earth","wind"]
    as_ = {e: aura_stats(e) for e in ae}
    out["aura_stats"] = as_
    qa = {}
    for a,b in itertools.combinations(ae,2):
        qa[f"{a}|{b}"] = round(ciede2000(as_[a]["lab_rendered"], as_[b]["lab_rendered"]),2)
    out["aura_dE2000_rendered"] = dict(sorted(qa.items(), key=lambda kv: kv[1]))
    print(json.dumps(out, indent=1))
