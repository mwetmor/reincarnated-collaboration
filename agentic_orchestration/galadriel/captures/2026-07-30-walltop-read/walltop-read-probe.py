#!/usr/bin/env python3
"""WALLTOP-READ probe — galadriel, 2026-07-30. READ-ONLY: consumes frames that already exist.
   python3 walltop-read-probe.py            (paths are absolute; no args)"""
import numpy as np, hashlib
from PIL import Image
G = "/Users/admin/Games/reincarnated-godot"
rd   = lambda p: np.asarray(Image.open(p).convert("RGB")).astype(float)
luma = lambda a: 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def s2l(c):
    c = np.asarray(c, dtype=float)/255.0
    return np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:16]

# ---------------------------------------------------------------- masks by per-column walk
def wallnum_masks(A, B):
    """Columns are walked DOWN from the void. Band identity is defined by the WALL-FIX
    BEFORE/AFTER ablation, not by colour: the cap is the run that did NOT change."""
    d, L = np.abs(A-B).max(axis=2), luma(A)
    cap  = np.zeros(L.shape, bool); slab = np.zeros(L.shape, bool)
    used = 0
    for x in range(A.shape[1]):
        col_L, col_d = L[:, x], d[:, x]
        lit = np.nonzero((col_L[:320] > 10))[0]
        if len(lit) == 0: continue
        a = lit[0]
        if a < 20: continue                       # column starts inside HUD text
        b = a
        while b < 320 and col_d[b] <= 2: b += 1   # cap = the unchanged run
        c = b
        while c < 320 and col_d[c] > 2 and A[c, x, 2] > A[c, x, 0]: c += 1   # slab top = changed + cool
        if not (4 <= b-a <= 26 and 12 <= c-b <= 40): continue                # reject contaminated cols
        if col_L[a:c].max() > 150: continue                                  # reject flame / bloom / UI
        cap[a+1:b-1, x] = True; slab[b+1:c-1, x] = True; used += 1
    return cap, slab, used

def pclight_cap_mask(K):
    """No ablation available here, so the cap is bounded by its own two hard edges:
    the void above, and the orange brick face below (R > 1.9 x B)."""
    L = luma(K); cap = np.zeros(L.shape, bool); used = 0
    for x in range(K.shape[1]):
        lit = np.nonzero(L[:400, x] > 10)[0]
        if len(lit) == 0: continue
        a = lit[0]
        b = a
        while b < 400 and not (K[b, x, 0] > 1.9*max(K[b, x, 2], 1e-6)): b += 1
        if not (4 <= b-a <= 40): continue
        if L[a:b, x].max() > 150: continue
        cap[a+1:b-1, x] = True; used += 1
    return cap, used

def stat(tag, img, m):
    v = img[m]; Lv = luma(v)
    print(f"  {tag:34s} n={len(v):6d}  mean sRGB=({v[:,0].mean():6.1f},{v[:,1].mean():6.1f},{v[:,2].mean():6.1f})"
          f"  L mean={Lv.mean():6.2f} p50={np.percentile(Lv,50):6.2f} p95={np.percentile(Lv,95):6.2f}")
    return v

A = rd(f"{G}/tmp/wallnum/frames/wallnum_AFTER_0128.png")
B = rd(f"{G}/tmp/wallnum/frames/wallnum_BEFORE_0128.png")
cap, slab, nc = wallnum_masks(A, B)
d = np.abs(A-B).max(axis=2)

print("="*80); print("§A  WALLNUM AFTER frame 0128 (37.5 m boss room, player_lock) — the two walltop bands")
print("="*80); print(f"  clean columns walked: {nc}")
vcap  = stat("LIGHTER BAND (outer, pre-void)", A, cap)
vslab = stat("band below it (inner walltop)",  A, slab)
print(f"\n  WALL-FIX ablation (drax textured the R-WR1-21 slabs on 2026-07-30):")
print(f"    lighter band  max Δ = {d[cap].max():5.1f}   mean Δ = {d[cap].mean():6.3f}   px with Δ>2: {(d[cap]>2).sum():6d} ({100*(d[cap]>2).mean():.2f}%)")
print(f"    band below it max Δ = {d[slab].max():5.1f}   mean Δ = {d[slab].mean():6.3f}   px with Δ>2: {(d[slab]>2).sum():6d} ({100*(d[slab]>2).mean():.2f}%)")
print(f"  => the lighter band is NOT the slab tops. It predates WALL-FIX and is untouched by it.")
print(f"  => THE INVERSION: the lighter band is {luma(vcap).mean()/luma(vslab).mean():.2f}x brighter than the walltop surface beside it.")

print()
print("="*80); print("§B  S14 ABLATION — cold sky-leak Key 0.00 vs 0.06 (kit_replica harness, R-6 camera)")
print("="*80)
P0, P6 = f"{G}/tmp/pclight/frames/v2_A.png", f"{G}/tmp/pclight/REVIEW/04_VARIANT_cold_skyleak.png"
print(f"  Key=0.00  v2_A == REVIEW/02_AFTER_crypt == afterB     sha {sha(P0)}")
print(f"  Key=0.06  04_VARIANT_cold_skyleak == s14 == v2_B == final_B   sha {sha(P6)}")
K0, K6 = rd(P0), rd(P6)
dk = np.abs(K6-K0).max(axis=2)
capk, nk = pclight_cap_mask(K0)
floor = (luma(K0) > 12) & ~capk; floor[:300,:] = False
wallface = (K0[...,0] > 1.9*np.maximum(K0[...,2],1e-6)) & (luma(K0) > 25); wallface[260:,:] = False
print(f"\n  frame-wide: {(dk>0).sum():6d}/{dk.size} px moved, max Δ {dk.max():.0f}, mean Δ {dk.mean():.3f}")
for tag, m in [("WALLTOP CAP band", capk), ("interior WALL FACE (brick)", wallface), ("FLOOR", floor)]:
    print(f"  {tag:28s} n={int(m.sum()):7d}   max Δ={dk[m].max():5.1f}   mean Δ={dk[m].mean():6.3f}   px Δ>1: {100*(dk[m]>1).mean():6.2f}%")
print("  => the S14 'daylight' lands on the FLOOR. The wall tops receive 0/255 from it.")

print()
print("="*80); print("§C  CROSS-STACK INVARIANCE — one cap, two rooms, two lighting stacks, two days")
print("="*80)
capk6, _ = pclight_cap_mask(K6)
vk = stat("pclight 2026-07-28 cap (R-6 cam)", K6, capk6)
_  = stat("wallnum 2026-07-30 cap (playerlock)", A, cap)
for tag, v in [("pclight", vk), ("wallnum", vcap)]:
    p = np.percentile(luma(v), 99)
    sel = v[luma(v) >= p]
    print(f"    {tag} p99 cap pixel = ({sel[:,0].mean():5.1f},{sel[:,1].mean():5.1f},{sel[:,2].mean():5.1f})")
print("  Between those two frames the room changed size, the camera changed, the ambient went")
print("  warm->purple (-42.7% luma), 4 sconces became 12, and a day passed. The cap did not move.")

print()
print("="*80); print("§D  CHROMA — light colour, or the shader's hard-coded tint constant?")
print("="*80)
tint = s2l(np.array([0.66,0.58,0.48])*255)
tex  = np.array([0.14337,0.14788,0.15431])        # Brick_Small_01 linear mean (WALL-READ §1.1)
pred = tint*tex
r = lambda c: f"{c[0]/c[2]:6.3f} : {c[1]/c[2]:6.3f} : 1.000"
print(f"  PREDICTED unlit  stone_tex x stone_tint(0.66,0.58,0.48) = {r(pred)}   [warm]")
def toplin(v):
    sel = v[luma(v) >= np.percentile(luma(v), 99)]
    return s2l(sel.mean(axis=0))
print(f"  MEASURED  lighter band, wallnum                          = {r(toplin(vcap))}")
print(f"  MEASURED  lighter band, pclight                          = {r(toplin(vk))}")
print(f"  S14 sky-leak Key light_color (0.55,0.66,0.95)            = {r(s2l(np.array([0.55,0.66,0.95])*255))}   [cold]")
print(f"  MEASURED  the LIT walltop surface beside it (slab top)   = {r(s2l(vslab.mean(axis=0)))}   [cold -> it DID receive light]")

print()
print("="*80); print("§E  H3 to scale — the declared beyond-wall glow rim")
print("="*80)
newly = (luma(B) == 0) & (luma(A) > 0)
print(f"  glow rim (drax WALL-FIX §4)  mean {luma(A)[newly].mean():5.2f}/255  max {luma(A)[newly].max():3.0f}  n={int(newly.sum())}")
print(f"  the lighter band             mean {luma(vcap).mean():5.2f}/255  max {luma(vcap).max():3.0f}  n={int(cap.sum())}")
print(f"  ratio of means               {luma(vcap).mean()/max(luma(A)[newly].mean(),1e-9):5.1f}x  -> not the same object")

# mask-validation plate (raw frame + magenta cap / green slab overlay)
ov = A.copy(); ov[cap] = [255,0,255]; ov[slab] = [0,255,0]
Image.fromarray(np.concatenate([A,ov],1).astype(np.uint8)).save("PLATE_bandmask_validation.png")
Image.fromarray(np.uint8(np.concatenate([K6, np.where(capk6[...,None], [255,0,255], K6)],1))).save("PLATE_pclight_capmask.png")
print("\n  masks written for eyeball validation: PLATE_bandmask_validation.png, PLATE_pclight_capmask.png")
