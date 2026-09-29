# T6 step 5 -- silhouette agreement with the painted plates, and the cheap
# knight rig probe.
#
# IoU: render and plate are alpha-masked, scale-normalised so the figure's
# height matches, aligned on the figure's centre, then intersected. Scale and
# alignment come from the LARGEST BLOB; the full mask including any detached
# fragment is what gets scored. Reported at two percentile trims --
#   0/100  the plain reading of "normalise by height"
#   1/99   trimmed, because the painted manticore BACK plate draws the tail as
#          a spike above the skull and no generator reproduces it, so a full
#          height box measures tail-to-paw on one side and skull-to-paw on the
#          other. The trim narrows that; it does not close it. The manticore
#          back column is a property of the PLATE and is near-constant across
#          all six rows -- read the manticore on front/right/left.
#
# Rig probe (knight row, no Meshy API call, no credits): triangle budget
# against the 300k rigging ceiling, single-island check, and an ARM-CLEARANCE
# test read off the flat front silhouette -- scan the torso band for rows whose
# mask breaks into three runs (arm | body | arm). Three runs means background
# lies between limb and trunk along that ray, so the surfaces are not fused.
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from maskutil import input_mask, render_mask, norm_by_height, iou, colour_sim, main_blob

B = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/'
T6 = B + 'fal_t6/'
PLATES = {'knight': B + 'meshy_t1/knight_%s.jpg', 'manticore': B + 'meshy_t2/manticore_%s.jpg'}
VIEWS = ['front', 'right', 'back', 'left']
GENS = ['meshy', 'hunyuan3d_31_pro', 'rodin_25', 'tripo_h31_mv', 'trellis2', 'hi3d_v3']
H, W = 400, 800
TRIMS = [(0.0, 100.0), (1.0, 99.0)]

ref = {}
for s, pat in PLATES.items():
    for v in VIEWS:
        ref[(s, v)] = input_mask(pat % v)

res = {}
for s in PLATES:
    for g in GENS:
        name = f'{s}_{g}'
        r = {}
        for trim in TRIMS:
            key = f'p{trim[0]:g}_{trim[1]:g}'
            per = {}
            for v in VIEWS:
                rm, rc = render_mask(f'{T6}work/out/silh/{name}_{v}.png')
                pm, pc = ref[(s, v)]
                a, ac = norm_by_height(rm, rc, H, W, *trim)
                b, bc = norm_by_height(pm, pc, H, W, *trim)
                per[v] = dict(iou=round(iou(a, b), 4), colour=round(colour_sim(a, ac, b, bc), 4))
            per['mean_iou'] = round(float(np.mean([per[v]['iou'] for v in VIEWS])), 4)
            per['mean_iou_ex_back'] = round(float(np.mean([per[v]['iou'] for v in VIEWS if v != 'back'])), 4)
            per['mean_colour'] = round(float(np.mean([per[v]['colour'] for v in VIEWS])), 4)
            r[key] = per
        res[name] = r
        h = r['p0_100']
        print(f"{name:30s} IoU f{h['front']['iou']:.3f} r{h['right']['iou']:.3f} "
              f"b{h['back']['iou']:.3f} l{h['left']['iou']:.3f}  mean {h['mean_iou']:.4f} "
              f"(ex-back {h['mean_iou_ex_back']:.4f})  colour {h['mean_colour']:.4f}")

# ---------------- knight rig probe ------------------------------------------
print('\n--- knight rig probe (no Meshy call) ---')
rig = {}
for g in GENS:
    name = f'knight_{g}'
    m = json.load(open(f'{T6}work/metrics/{name}.json'))
    mask, _ = render_mask(f'{T6}work/out/silh/{name}_front.png')
    body = main_blob(mask)
    ys, xs = np.where(body)
    y0, y1 = ys.min(), ys.max() + 1
    Hb = y1 - y0
    best = dict(runs=1, z=None, gaps=[])
    prof = []
    for y in range(y0, y1):
        row = body[y]
        d = np.diff(row.astype(np.int8))
        starts = list(np.where(d == 1)[0] + 1) + ([0] if row[0] else [])
        runs = len(starts)
        zf = 1.0 - (y - y0) / Hb                      # 1 = crown, 0 = sole
        prof.append((round(zf, 3), runs))
        if 0.25 < zf < 0.80 and runs > best['runs']:
            gaps = []
            i = 0
            while i < len(row):
                if not row[i]:
                    j = i
                    while j < len(row) and not row[j]:
                        j += 1
                    if i > 0 and j < len(row):
                        gaps.append(j - i)
                    i = j
                else:
                    i += 1
            best = dict(runs=runs, z=round(zf, 3), gaps=gaps)
    band = [r for zf, r in prof if 0.25 < zf < 0.80]
    rows3 = int(sum(1 for r in band if r >= 3))
    tris = m['tris_welded']
    rig[name] = dict(
        tris=tris, decimate_ratio_to_300k=round(min(1.0, 300000 / tris), 4),
        under_300k_as_delivered=bool(tris <= 300000),
        islands=m['islands'], main_island_area_frac=m['main_island_area_frac'],
        single_humanoid_island=bool(m['main_island_area_frac'] > 0.98),
        floating_fragments=m['floating_fragments_lt1pct'],
        arm_gap_max_runs=best['runs'], arm_gap_at_height_frac=best['z'],
        arm_gap_widths_px=best['gaps'],
        arm_gap_rows_in_torso_band=rows3,
        arms_clear_of_torso=bool(best['runs'] >= 3 and rows3 >= 8))
    r = rig[name]
    print(f"{name:30s} tris {tris:8d} (dec x{r['decimate_ratio_to_300k']:.3f})  "
          f"main-island {r['main_island_area_frac']:.4f} frag {r['floating_fragments']:3d}  "
          f"arm-runs {r['arm_gap_max_runs']} over {rows3:3d} rows  "
          f"gaps {r['arm_gap_widths_px']}  -> arms clear: {r['arms_clear_of_torso']}")

json.dump(dict(iou=res, knight_rig_probe=rig), open(T6 + 'compare/iou_rig.json', 'w'), indent=1)
print('\nwrote compare/iou_rig.json')
