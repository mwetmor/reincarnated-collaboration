#!/usr/bin/env python3
"""
galadriel — WW-AB emissive-confound probe (2026-08-24)

QUESTION PUT TO ME: does an undeclared emissive source, CO-LOCATED with the geometry
the authored effect is generated from, confound the measures my minted-gate actually
uses -- or does it wash out of the fx-on minus fx-off difference?

I do not answer that from theory. This measures it on the frames as they sit on disk.

MY GATE HAS TWO CHANNELS AND THEY DO NOT BEHAVE THE SAME:
  (A) DELTA channel   -- lit-px mask, added_rgb, lab_added, hue, bbox, centroid,
                         radius stats, coverage. Computed on (arm - control).
  (B) RENDERED channel -- lab_rendered / L_rendered / chroma_rendered, and therefore
                         dE2000_rendered, which is the instrument RT-2 is adjudicated on
                         (see s2_gate_colour.py header). Computed on ABSOLUTE arm pixels
                         a[m]. It NEVER differences.

Channel B cannot wash out by construction. Channel A washes out only if the pipeline
is LINEAR. It is not: s2_stage_env.gd sets tonemap_mode=FILMIC and glow_enabled=true,
so T(scene+trail) - T(scene) != T(trail), and the error is largest exactly where the
scene is already bright -- i.e. on the emissive blade the trail is authored from.

Hard failure mode tested for: CHANNEL CLIPPING. If emissive pixels sit at or near 255,
added trail light is not merely compressed, it is DISCARDED -- delta is identically zero
where the effect is strongest.
"""
import os, sys, math, json
import numpy as np
from PIL import Image

S2B = "/Users/admin/Games/reincarnated-godot/harness_logs/s2b_receipts_2026-08-24b"
WW  = "/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-24"
S2A = "/Users/admin/Games/reincarnated-godot/harness_logs/s2a_2026-08-24-final"

MARKS = ["00-pre","01-windup-early","02-windup-late","03-rising-mid","04-full",
         "05-sustain","06-sustain-moving","07-release-early","08-release-late","09-off"]

def load(cap, arm, mark):
    return np.asarray(Image.open(os.path.join(cap, f"{arm}_{mark}.png")).convert("RGB")).astype(np.float64)

def lum(im):
    return 0.2126*im[...,0] + 0.7152*im[...,1] + 0.0722*im[...,2]

def srgb_to_lab(rgb):
    c = np.asarray(rgb, dtype=np.float64)/255.0
    c = np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
    M = np.array([[0.4124564,0.3575761,0.1804375],
                  [0.2126729,0.7151522,0.0721750],
                  [0.0193339,0.1191920,0.9503041]])
    xyz = c @ M.T
    wp = np.array([0.95047,1.0,1.08883]); t = xyz/wp; d = 6/29
    f = np.where(t > d**3, np.cbrt(t), t/(3*d*d)+4/29)
    return np.stack([116*f[...,1]-16, 500*(f[...,0]-f[...,1]), 200*(f[...,1]-f[...,2])], axis=-1)

def ciede2000(lab1, lab2):
    L1,a1,b1 = lab1; L2,a2,b2 = lab2
    C1 = math.hypot(a1,b1); C2 = math.hypot(a2,b2); Cb = (C1+C2)/2
    G = 0.5*(1-math.sqrt(Cb**7/(Cb**7+25**7))) if Cb > 0 else 0.5
    a1p,a2p = (1+G)*a1,(1+G)*a2
    C1p,C2p = math.hypot(a1p,b1), math.hypot(a2p,b2)
    h1p = math.degrees(math.atan2(b1,a1p))%360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2,a2p))%360 if (a2p or b2) else 0.0
    dLp = L2-L1; dCp = C2p-C1p
    if C1p*C2p == 0: dhp = 0.0
    else:
        dh = h2p-h1p
        dhp = dh-360 if dh > 180 else (dh+360 if dh < -180 else dh)
    dHp = 2*math.sqrt(C1p*C2p)*math.sin(math.radians(dhp)/2)
    Lbp=(L1+L2)/2; Cbp=(C1p+C2p)/2
    if C1p*C2p == 0: hbp = h1p+h2p
    else:
        s = h1p+h2p
        hbp = (s+360)/2 if abs(h1p-h2p)>180 and s<360 else ((s-360)/2 if abs(h1p-h2p)>180 else s/2)
    T = (1-0.17*math.cos(math.radians(hbp-30))+0.24*math.cos(math.radians(2*hbp))
         +0.32*math.cos(math.radians(3*hbp+6))-0.20*math.cos(math.radians(4*hbp-63)))
    dTh = 30*math.exp(-((hbp-275)/25)**2)
    Rc = 2*math.sqrt(Cbp**7/(Cbp**7+25**7)) if Cbp>0 else 0
    Sl = 1+(0.015*(Lbp-50)**2)/math.sqrt(20+(Lbp-50)**2)
    Sc = 1+0.045*Cbp; Sh = 1+0.015*Cbp*T
    Rt = -math.sin(math.radians(2*dTh))*Rc
    return math.sqrt((dLp/Sl)**2+(dCp/Sc)**2+(dHp/Sh)**2+Rt*(dCp/Sc)*(dHp/Sh))


def find_emissive(ctl):
    """Locate the teal/cyan self-illuminated blade in the CONTROL frame (fx off).
    Anything the trail contributes is absent here, so whatever is bright-and-cyan
    in this frame is the rig's own emission, not the authored effect.
    Criterion is data-driven, not a hand-drawn box: cyan-dominant AND bright."""
    R,G,B = ctl[...,0], ctl[...,1], ctl[...,2]
    L = lum(ctl)
    cyan = (G - R) + (B - R)              # cyan-ness: both G and B above R
    m = (cyan > 40) & (L > np.percentile(L, 99.0))
    return m, cyan, L


def report(cap, arm_on, arm_ctl, label):
    out = {"capture": cap, "arm_on": arm_on, "arm_ctl": arm_ctl, "label": label, "marks": {}}

    # emissive footprint located on the 04-full control frame
    ctl_full = load(cap, arm_ctl, "04-full")
    em, cyan, L = find_emissive(ctl_full)
    out["emissive_footprint_px"] = int(em.sum())
    if em.sum():
        ys, xs = np.nonzero(em)
        out["emissive_bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        out["emissive_mean_rgb"] = [round(float(ctl_full[...,i][em].mean()),1) for i in range(3)]
        out["emissive_max_rgb"]  = [round(float(ctl_full[...,i][em].max()),1) for i in range(3)]
        out["emissive_mean_lum"] = round(float(L[em].mean()),1)
        # CLIPPING: how much of the emissive footprint is already at ceiling?
        anyclip = (ctl_full.max(axis=2) >= 254)
        out["emissive_px_at_ceiling"] = int((em & anyclip).sum())
        out["emissive_pct_at_ceiling"] = round(100.0*float((em&anyclip).sum())/max(1,int(em.sum())),2)
        # near-ceiling: within the top of the filmic curve where compression is severe
        near = (ctl_full.max(axis=2) >= 235)
        out["emissive_pct_near_ceiling"] = round(100.0*float((em&near).sum())/max(1,int(em.sum())),2)

    for mk in MARKS:
        try:
            a = load(cap, arm_on, mk); c = load(cap, arm_ctl, mk)
        except FileNotFoundError:
            continue
        d = a - c
        mag = np.abs(d).sum(axis=2)
        m = mag > 12
        n = int(m.sum())
        r = {"lit": n}
        if n == 0:
            out["marks"][mk] = r; continue

        # per-mark emissive footprint from THIS mark's control (blade moves as it spins)
        emk, _, _ = find_emissive(c)
        r["emissive_px_this_mark"] = int(emk.sum())
        r["trail_x_emissive_overlap_px"] = int((m & emk).sum())
        r["overlap_pct_of_emissive"] = round(100.0*float((m&emk).sum())/max(1,int(emk.sum())),2)

        # ---- CHANNEL A (delta) : does the emissive region SUPPRESS measured delta? ----
        # dilate the emissive footprint to capture the glow halo it throws
        from scipy.ndimage import binary_dilation
        halo = binary_dilation(emk, iterations=12)
        r["halo_px"] = int(halo.sum())
        r["trail_in_halo_px"] = int((m & halo).sum())
        if (m & halo).sum() and (m & ~halo).sum():
            r["delta_mean_in_halo"]  = round(float(mag[m & halo].mean()),2)
            r["delta_mean_out_halo"] = round(float(mag[m & ~halo].mean()),2)
        # DEAD ZONE: control pixels already clipped -> added light provably discarded
        clipped_ctl = (c.max(axis=2) >= 254)
        r["ctl_clipped_px"] = int(clipped_ctl.sum())
        r["ctl_clipped_inside_halo"] = int((clipped_ctl & halo).sum())
        if clipped_ctl.sum():
            # of pixels the control already clips, how many register ZERO delta?
            zero = (mag <= 12) & clipped_ctl
            r["clipped_px_registering_no_delta"] = int(zero.sum())
            r["clipped_deadzone_pct"] = round(100.0*float(zero.sum())/max(1,int(clipped_ctl.sum())),2)

        # ---- CHANNEL B (rendered) : the RT-2 instrument ----
        w = mag[m]
        ren = a[m]
        ren_mean_all = (ren*w[:,None]).sum(0)/w.sum()
        lab_all = srgb_to_lab(np.clip(ren_mean_all,0,255))
        r["lab_rendered_ALL"] = [round(float(x),2) for x in lab_all]
        r["chroma_rendered_ALL"] = round(float(math.hypot(lab_all[1],lab_all[2])),2)

        keep = m & ~halo
        if keep.sum():
            w2 = mag[keep]; ren2 = a[keep]
            ren_mean_clean = (ren2*w2[:,None]).sum(0)/w2.sum()
            lab_clean = srgb_to_lab(np.clip(ren_mean_clean,0,255))
            r["lab_rendered_EXCL_EMISSIVE"] = [round(float(x),2) for x in lab_clean]
            r["chroma_rendered_EXCL"] = round(float(math.hypot(lab_clean[1],lab_clean[2])),2)
            r["dE2000_contamination"] = round(ciede2000(lab_all, lab_clean),2)
            r["dL_contamination"] = round(float(lab_all[0]-lab_clean[0]),2)
        out["marks"][mk] = r
    return out


if __name__ == "__main__":
    res = {}
    res["s2b_ww"]  = report(S2B, "rc_ww_fxon", "rc_ww_ctl_fxctl", "s2b receipts whirlwind")
    res["wwcr"]    = report(WW,  "combat_fxon", "combat_fxctl", "clean-room whirlwind mint (commit 1692d6e)")
    print(json.dumps(res, indent=1))
