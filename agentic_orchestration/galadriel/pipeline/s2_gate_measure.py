#!/usr/bin/env python3
"""
galadriel — S2 minted-gate independent measurement instrument (2026-08-24)

Purpose: re-derive the tranche-1 numbers from the PNGs MYSELF. A gate that restates
the builder's numbers is a rubber stamp. Every figure this emits is computed from the
capture set, not read from render.txt / gate.json.

DISCIPLINE: numeric-primary. This script NEVER writes a composite image and never
emits anything wider than 1600 px. Visual loads are separate, downscaled, one at a time.

Isolation method: authored-effect pixels are isolated by differencing an arm against
its MATCHED CONTROL arm at the SAME mark (drax pinned all AnimationPlayers to the
stage clock, so control frames are pose-identical; I verify that claim rather than
assume it -- see check_determinism()).
"""
import sys, os, json, math
import numpy as np
from PIL import Image

CAP = "/Users/admin/Games/reincarnated-godot/harness_logs/s2a_2026-08-24-final"
W, H = 1920, 1080
NPIX = W * H

def load(arm, mark):
    p = os.path.join(CAP, f"{arm}_{mark}.png")
    return np.asarray(Image.open(p).convert("RGB")).astype(np.int16)

def delta(arm, ctl, mark):
    """Per-pixel signed difference vs matched control. Returns (dRGB float, mask)."""
    a = load(arm, mark); c = load(ctl, mark)
    d = a - c
    mag = np.abs(d).sum(axis=2)
    return d, mag

def lit(arm, ctl, mark, thr=12):
    """Lit-px count = pixels whose summed |dRGB| vs control exceeds thr."""
    d, mag = delta(arm, ctl, mark)
    m = mag > thr
    return int(m.sum()), m, d

def hue_of(d, m, weight_by_energy=True):
    """
    Circular-mean hue (degrees) of the ADDED light, over mask m.
    Uses positive part of the delta = the light the effect contributed.
    """
    if m.sum() == 0:
        return None, 0.0
    px = np.clip(d[m], 0, None).astype(np.float64)
    if px.sum() == 0:
        return None, 0.0
    r, g, b = px[:, 0], px[:, 1], px[:, 2]
    mx = px.max(axis=1); mn = px.min(axis=1); c = mx - mn
    hu = np.zeros_like(mx)
    nz = c > 0
    idx = np.argmax(px, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        s0 = nz & (idx == 0); s1 = nz & (idx == 1); s2 = nz & (idx == 2)
        hu[s0] = (60 * (((g - b)[s0] / c[s0]) % 6))
        hu[s1] = (60 * (((b - r)[s1] / c[s1]) + 2))
        hu[s2] = (60 * (((r - g)[s2] / c[s2]) + 4))
    wgt = (c if weight_by_energy else np.ones_like(c))
    wgt = np.where(nz, wgt, 0.0)
    if wgt.sum() == 0:
        return None, 0.0
    ang = np.deg2rad(hu)
    X = (wgt * np.cos(ang)).sum(); Y = (wgt * np.sin(ang)).sum()
    hbar = math.degrees(math.atan2(Y, X)) % 360.0
    R = math.hypot(X, Y) / wgt.sum()          # concentration; 1 = pure single hue
    return hbar, R

def sep(h1, h2):
    if h1 is None or h2 is None: return None
    d = abs(h1 - h2) % 360.0
    return min(d, 360.0 - d)

def bbox(m):
    ys, xs = np.nonzero(m)
    if len(ys) == 0: return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

# ---------------------------------------------------------------- checks

def check_determinism():
    """drax claims 00-pre and 08-post diff to exactly 0 lit px on all five melee arms.
    That claim is the LICENCE for every control-difference in this gate. Verify it."""
    out = {}
    for e in ["neutral", "fire", "water", "earth", "wind"]:
        n_pre, _, _ = lit(f"melee_{e}", "melee_ctl", "00-pre")
        n_post, _, _ = lit(f"melee_{e}", "melee_ctl", "08-post")
        # also: is the CONTROL itself stable between its own pre and post?
        a = load("melee_ctl", "00-pre"); b = load("melee_ctl", "08-post")
        out[e] = dict(pre_lit=n_pre, post_lit=n_post,
                      ctl_self_maxdiff=int(np.abs(a - b).max()))
    return out

def check_albedo():
    """Independent floor-brightness read. Albedo is a material param, not a pixel value,
    but an 0.20 floor vs an 0.085 floor differ by ~2.35x in reflected luminance, which IS
    measurable. I report the floor luminance and its consistency ACROSS ALL 21 ARMS --
    a single arm rendered at the wrong albedo would show up as an outlier."""
    # sample a ground band well away from caster/effect: bottom strip, left+right thirds
    res = {}
    arms = sorted(set(f.rsplit("_", 1)[0] for f in os.listdir(CAP) if f.endswith(".png")))
    for arm in arms:
        marks = sorted(f.rsplit("_", 1)[1][:-4] for f in os.listdir(CAP)
                       if f.startswith(arm + "_") and f.endswith(".png"))
        im = load(arm, marks[0]).astype(np.float64)
        strip = np.concatenate([im[960:1070, 40:300], im[960:1070, 1620:1880]], axis=1)
        lum = (0.2126*strip[:,:,0] + 0.7152*strip[:,:,1] + 0.0722*strip[:,:,2])
        res[arm] = dict(mean_lum=round(float(lum.mean()), 3),
                        p50=round(float(np.median(lum)), 3),
                        p95=round(float(np.percentile(lum, 95)), 3))
    return res

def melee_rows():
    """Row 1. Trail isolation vs melee_ctl (fx=off, same clock)."""
    out = {}
    for e in ["neutral", "fire", "water", "earth", "wind"]:
        arm = f"melee_{e}"; r = {}
        for mark in ["01-s1-windup", "02-s1-swing", "03-s1-contact", "05-s2-swing", "06-s3-swing"]:
            n, m, d = lit(arm, "melee_ctl", mark)
            h, R = hue_of(d, m)
            bb = bbox(m)
            r[mark] = dict(lit=n, cov_pct=round(100.0*n/NPIX, 4),
                           hue=None if h is None else round(h, 2),
                           hue_conc=round(R, 3), bbox=bb,
                           bbox_h=None if bb is None else bb[3]-bb[1],
                           bbox_w=None if bb is None else bb[2]-bb[0])
        out[e] = r
    return out

def melee_rt2():
    """RT-2: pairwise hue separation of the RENDERED trail (not the palette constant).
    RT-2's trigger is 'read as indistinguishable AT THE GAMEPLAY CAMERA' -- so the
    measurement must be taken on rendered pixels, which is what this does."""
    hues = {}
    for e in ["neutral", "fire", "water", "earth", "wind"]:
        # measure on the swing frame (trail at full extent, no hit-flash contamination)
        n, m, d = lit(f"melee_{e}", "melee_ctl", "02-s1-swing")
        h, R = hue_of(d, m)
        # also a brightness/saturation read -- hue is not the only separation channel
        px = np.clip(d[m], 0, None).astype(np.float64)
        mx = px.max(axis=1); mn = px.min(axis=1)
        satm = float(np.mean(np.where(mx > 0, (mx-mn)/np.maximum(mx,1e-9), 0)))
        hues[e] = dict(hue=None if h is None else round(h,2), conc=round(R,3),
                       lit=n, mean_sat=round(satm,4),
                       mean_added_rgb=[round(float(px[:,i].mean()),2) for i in range(3)])
    pairs = {}
    ks = list(hues)
    for i in range(len(ks)):
        for j in range(i+1, len(ks)):
            a, b = ks[i], ks[j]
            s = sep(hues[a]["hue"], hues[b]["hue"])
            pairs[f"{a}|{b}"] = None if s is None else round(s, 2)
    return hues, dict(sorted(pairs.items(), key=lambda kv: (kv[1] is None, kv[1])))

def melee_field_test():
    """The 'must NOT' clause: no body-surrounding field. A field would show as delta
    pixels distributed around the caster silhouette; a trail shows as a compact arc.
    Measure: fraction of lit px within the blade-reach arc vs scattered elsewhere,
    and the vertical floor of authored pixels (ground-propagation test in screen space)."""
    out = {}
    for e in ["neutral", "fire", "water", "earth", "wind"]:
        n, m, d = lit(f"melee_{e}", "melee_ctl", "02-s1-swing")
        ys, xs = np.nonzero(m)
        if len(ys) == 0:
            out[e] = None; continue
        cx, cy = float(xs.mean()), float(ys.mean())
        rad = np.hypot(xs-cx, ys-cy)
        out[e] = dict(lit=n,
                      centroid=[round(cx,1), round(cy,1)],
                      r_p50=round(float(np.percentile(rad,50)),1),
                      r_p99=round(float(np.percentile(rad,99)),1),
                      lowest_y=int(ys.max()), highest_y=int(ys.min()),
                      # compactness: a trail is a thin arc -> high fill-ratio deficit
                      bbox_fill=round(float(n/max(1,(xs.max()-xs.min()+1)*(ys.max()-ys.min()+1))),4))
    return out

def gtc_rows():
    """Row 2. No fx=off control arm exists for circle, so isolate against the arm's own
    00-pre (which drax's determinism fix makes pose-identical -- verified separately)."""
    arms = ["gtc_fire_descend_hostile","gtc_water_descend_hostile","gtc_earth_descend_hostile",
            "gtc_fire_erupt_hostile","gtc_water_descend_friendly","gtc_fire_descend_large"]
    out = {}
    for arm in arms:
        r = {}
        for mark in ["01-telegraph","02-payload-mid","03-impact","04-residue","05-coexist","07-late"]:
            n, m, d = lit(arm, arm, "00-pre") if False else (None,None,None)
            a = load(arm, mark); c = load(arm, "00-pre")
            dd = a - c; mag = np.abs(dd).sum(axis=2); mm = mag > 12
            n = int(mm.sum()); h, R = hue_of(dd, mm)
            r[mark] = dict(lit=n, cov_pct=round(100.0*n/NPIX,4),
                           hue=None if h is None else round(h,2), conc=round(R,3))
        out[arm] = r
    return out

def gtc_perimeter_rise():
    """Perimeter definition = the deciding property for this row (telegraph literacy).
    Measure the 10%->90% intensity rise across the perimeter band by sampling a
    horizontal scanline through the ring at the telegraph mark."""
    out = {}
    for arm in ["gtc_fire_descend_hostile","gtc_water_descend_hostile","gtc_earth_descend_hostile",
                "gtc_water_descend_friendly","gtc_fire_descend_large"]:
        a = load(arm, "01-telegraph").astype(np.float64)
        c = load(arm, "00-pre").astype(np.float64)
        d = np.abs(a - c).sum(axis=2)
        ys, xs = np.nonzero(d > 12)
        if len(ys) == 0: out[arm] = None; continue
        cy = int(np.median(ys))
        row = d[cy]
        # find the left edge of the ring on this scanline
        on = np.nonzero(row > 12)[0]
        if len(on) == 0: out[arm] = None; continue
        x0 = int(on.min())
        seg = row[max(0,x0-12): x0+24]
        lo, hi = seg.min(), seg.max()
        if hi - lo <= 0: out[arm] = None; continue
        t10 = lo + 0.10*(hi-lo); t90 = lo + 0.90*(hi-lo)
        i10 = int(np.argmax(seg >= t10)); i90 = int(np.argmax(seg >= t90))
        out[arm] = dict(scanline_y=cy, x_left=x0, rise_px=abs(i90-i10),
                        seg_lo=round(float(lo),1), seg_hi=round(float(hi),1),
                        ring_width_px=int(len(on)) if len(on)<50 else None,
                        profile=[round(float(v),1) for v in seg[:24]])
    return out

def gtc_interior_bloom():
    """Meteor-Indigo failure mode: does the effect bloom out its own interior at scale?
    Ratio = mean added energy in the disc INTERIOR vs on the PERIMETER band.
    A bloom is that ratio RISING with scale."""
    out = {}
    for arm in ["gtc_fire_descend_hostile", "gtc_fire_descend_large"]:
        a = load(arm, "01-telegraph").astype(np.float64)
        c = load(arm, "00-pre").astype(np.float64)
        d = np.abs(a - c).sum(axis=2)
        m = d > 12
        ys, xs = np.nonzero(m)
        cx, cy = xs.mean(), ys.mean()
        rr = np.hypot(xs-cx, ys-cy)
        rmax = np.percentile(rr, 99)
        # perimeter band = outer 15% of radius; interior = inner 60%
        peri = rr >= 0.85*rmax
        inte = rr <= 0.60*rmax
        vals = d[ys, xs]
        # interior opacity: fraction of interior-disc pixels that are strongly lit
        # build a filled-disc mask to get the true interior denominator
        Y, X = np.ogrid[:H, :W]
        disc = ((X-cx)**2 + (Y-cy)**2) <= (0.60*rmax)**2
        strong = (d > 90) & disc
        out[arm] = dict(rmax_px=round(float(rmax),1),
                        peri_mean=round(float(vals[peri].mean()),2) if peri.sum() else None,
                        int_mean=round(float(vals[inte].mean()),2) if inte.sum() else None,
                        int_over_peri=round(float(vals[inte].mean()/vals[peri].mean()),4) if peri.sum() and inte.sum() else None,
                        disc_px=int(disc.sum()),
                        interior_opaque_pct=round(100.0*float(strong.sum())/max(1,int(disc.sum())),3))
    return out

def gtc_telegraph_precedence():
    """Can the player read 'a thing is going to land THERE' BEFORE it lands?
    Test: at the telegraph mark, is the ground perimeter already present, and how much
    of the frame's added energy is perimeter vs payload? Compare descend vs erupt."""
    out = {}
    for arm in ["gtc_fire_descend_hostile", "gtc_fire_erupt_hostile"]:
        r = {}
        for mark in ["01-telegraph", "02-payload-mid", "03-impact"]:
            a = load(arm, mark).astype(np.float64); c = load(arm, "00-pre").astype(np.float64)
            d = np.abs(a-c).sum(axis=2); m = d > 12
            ys, xs = np.nonzero(m)
            if len(ys)==0: r[mark]=None; continue
            # ground plane vs above-ground split by screen row: the ring sits low in frame,
            # an airborne payload sits high. Use the ring centroid row as the divider.
            gy = int(np.percentile(ys, 60))
            above = int((ys < gy - 60).sum())
            r[mark] = dict(lit=int(m.sum()), y_p10=int(np.percentile(ys,10)),
                           y_p60=gy, y_p99=int(np.percentile(ys,99)),
                           px_well_above_ring=above,
                           frac_above=round(float(above)/max(1,int(m.sum())),4))
        out[arm] = r
    return out

def aura_rows():
    out = {}
    for e in ["fire","water","earth","wind"]:
        arm = f"aura_{e}"
        a = load(arm, "00-steady").astype(np.float64)
        c = load("aura_novfx", "00-steady").astype(np.float64)
        d = a - c; mag = np.abs(d).sum(axis=2); m = mag > 12
        h, R = hue_of(d.astype(np.int16), m)
        ys, xs = np.nonzero(m)
        cx, cy = xs.mean(), ys.mean()
        rr = np.hypot(xs-cx, ys-cy)
        strong = int((mag > 90).sum())
        out[e] = dict(lit=int(m.sum()), cov_pct=round(100.0*int(m.sum())/NPIX,4),
                      hue=None if h is None else round(h,2), conc=round(R,3),
                      r_p50=round(float(np.percentile(rr,50)),2),
                      r_p95=round(float(np.percentile(rr,95)),2),
                      r_p99=round(float(np.percentile(rr,99)),2),
                      opaque_px=strong,
                      opaque_pct_of_screen=round(100.0*strong/NPIX,4))
    pairs = {}
    ks = list(out)
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            pairs[f"{ks[i]}|{ks[j]}"] = sep(out[ks[i]]["hue"], out[ks[j]]["hue"])
    pairs = {k: (None if v is None else round(v,2)) for k,v in pairs.items()}
    return out, dict(sorted(pairs.items(), key=lambda kv:(kv[1] is None, kv[1])))

def aura_readthrough():
    """The 2x2 that answers 'do other archetypes' VFX stay readable THROUGH an aura?'
       rt_on      = aura ON  + trail ON
       rt_trailoff= aura ON  + trail OFF
       rt_ctl     = aura OFF + trail ON
       rt_ctrloff = aura OFF + trail OFF
    Trail-inside  = rt_on      - rt_trailoff
    Trail-outside = rt_ctl     - rt_ctrloff
    retention = inside/outside. This is the correct control on BOTH sides."""
    res = {}
    for mark in ["02-rt-swing", "03-rt-contact"]:
        on = load("aura_rt_on", mark); toff = load("aura_rt_trailoff", mark)
        ctl = load("aura_rt_ctl", mark); coff = load("aura_rt_ctrloff", mark)
        din = on - toff; dou = ctl - coff
        min_ = np.abs(din).sum(axis=2) > 12
        mou = np.abs(dou).sum(axis=2) > 12
        pin = np.abs(din).sum(axis=2); pou = np.abs(dou).sum(axis=2)
        res[mark] = dict(
            trail_inside_lit=int(min_.sum()), trail_outside_lit=int(mou.sum()),
            retention_lit=round(float(min_.sum())/max(1,int(mou.sum())),4),
            peak_inside=int(pin.max()), peak_outside=int(pou.max()),
            energy_inside=int(pin.sum()), energy_outside=int(pou.sum()),
            retention_energy=round(float(pin.sum())/max(1,float(pou.sum())),4),
            iou=round(float((min_&mou).sum())/max(1,int((min_|mou).sum())),4),
        )
    return res

def aura_causality_layers():
    """L-19 is scored PER ROW AGAINST ITS DECLARED CLASS. aura is magical-cause and that
    is CORRECT -- so the check here is NOT 'does it touch bodies'. It is the inverse:
    did the builder smuggle in physical-causality tells to flatter the score?
    Test: does the aura delta intersect the enemy-body regions with impact-like flashes,
    and does it change between steady and contact marks (it must NOT -- it is sustained)."""
    out = {}
    a0 = load("aura_fire", "00-steady"); a4 = load("aura_fire", "04-steady2")
    a5 = load("aura_fire", "05-late")
    c = load("aura_novfx", "00-steady")
    d0 = np.abs(a0 - c).sum(axis=2) > 12
    out["steady_vs_steady2_maxdiff"] = int(np.abs(a0.astype(int)-a4.astype(int)).max())
    out["steady_vs_late_maxdiff"] = int(np.abs(a0.astype(int)-a5.astype(int)).max())
    out["steady_lit"] = int(d0.sum())
    # sustained-ness: lit-px across the arm's own marks vs novfx at same mark
    per = {}
    for mk in ["00-steady","01-rt-windup","02-rt-swing","03-rt-contact","04-steady2","05-late"]:
        aa = load("aura_fire", mk); cc = load("aura_novfx", mk)
        per[mk] = int((np.abs(aa-cc).sum(axis=2) > 12).sum())
    out["lit_per_mark"] = per
    return out

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    R = {}
    if which in ("all","det"):      R["determinism"] = check_determinism()
    if which in ("all","albedo"):   R["albedo_floor"] = check_albedo()
    if which in ("all","melee"):
        R["melee"] = melee_rows()
        h, p = melee_rt2(); R["melee_rt2_hues"] = h; R["melee_rt2_pairs"] = p
        R["melee_field_test"] = melee_field_test()
    if which in ("all","gtc"):
        R["gtc"] = gtc_rows()
        R["gtc_perimeter_rise"] = gtc_perimeter_rise()
        R["gtc_interior_bloom"] = gtc_interior_bloom()
        R["gtc_telegraph_precedence"] = gtc_telegraph_precedence()
    if which in ("all","aura"):
        a, p = aura_rows(); R["aura"] = a; R["aura_pairs"] = p
        R["aura_readthrough"] = aura_readthrough()
        R["aura_causality"] = aura_causality_layers()
    print(json.dumps(R, indent=1))
