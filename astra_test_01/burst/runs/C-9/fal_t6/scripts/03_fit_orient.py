# T6 step 2b -- MEASURE each model's facing instead of assuming it.
#
# Two separate questions, deliberately not answered by one score:
#
#   YAW    is decidable from silhouette. Try yaw in {0,90,180,270}. `yaw` is the
#          rotation 04_render.py ACTUALLY APPLIES (Matrix.Rotation(+yaw,'Z')),
#          and for such a model the view from azimuth A is the delivered
#          model's view at (A + yaw): rotating the subject by +yaw is the same
#          as walking the camera round by +yaw. Score against the painted
#          plates. The earlier version of this file wrote (A - yaw) and so
#          reported the INVERSE rotation; it agreed with the applied one for
#          every 180 deg model -- five of six rows -- and was silently 180 deg
#          out on the two Tripo models, whose left and right plates then scored
#          0.60/0.62 where the correct rotation scores 0.88. Verified by hand
#          on knight_tripo_h31_mv at both 90 and 270 before this was changed.
#          Mirror composes as hflip of the delivered view at (-A - yaw).
#   MIRROR is NOT decidable from silhouette -- these subjects are near
#          bilaterally symmetric, so flipping one costs ~0.004 of IoU, which is
#          noise. It is decidable from PAINT: the knight's gold cross sits on
#          one side of the surcoat and the stripes on the other. So it gets its
#          own test, on the front and back plates only, colour-weighted, and
#          the margin is reported so a weak call can be read as weak.
#
# usage: python3 03_fit_orient.py [plo phi]     (percentile trim, default 0 100)
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from maskutil import input_mask, render_mask, norm_by_height, iou, colour_sim

B = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/'
T6 = B + 'fal_t6/'
PLATES = {'knight': B + 'meshy_t1/knight_%s.jpg', 'manticore': B + 'meshy_t2/manticore_%s.jpg'}
VIEWS = {'front': 0, 'right': 90, 'back': 180, 'left': 270}
GENS = ['meshy', 'hunyuan3d_31_pro', 'rodin_25', 'tripo_h31_mv', 'trellis2', 'hi3d_v3']
H, W = 320, 640
PLO, PHI = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else (0.0, 100.0)
MIRROR_MIN = 0.05   # evidence bar for APPLYING a mirror; see below

ref = {}
for s, pat in PLATES.items():
    for v in VIEWS:
        m, rgb = input_mask(pat % v)
        ref[(s, v)] = norm_by_height(m, rgb, H, W, PLO, PHI)

out = {}
print(f'--- orientation fit, percentile trim {PLO}/{PHI} ---')
for s in PLATES:
    for g in GENS:
        name = f'{s}_{g}'
        R = {}
        for az in (0, 90, 180, 270):
            R[az] = render_mask(f'{T6}work/orient/{name}_az{az:03d}.png')
        areas = [int(R[a][0].sum()) for a in (0, 90, 180, 270)]
        assert len(set(areas)) > 1, f'{name}: four azimuths, identical areas {areas}'

        def score(yaw, mir):
            per, ti, tc = {}, 0.0, 0.0
            for v, A in VIEWS.items():
                az = ((-A - yaw) if mir else (A + yaw)) % 360
                m, rgb = R[az]
                if mir:
                    m, rgb = m[:, ::-1], rgb[:, ::-1]
                nm, nc = norm_by_height(m, rgb, H, W, PLO, PHI)
                rm, rc = ref[(s, v)]
                I, C = iou(nm, rm), colour_sim(nm, nc, rm, rc)
                per[v] = dict(iou=round(I, 4), colour=round(C, 4)); ti += I; tc += C
            return ti / 4, tc / 4, per

        ys = sorted(((score(y, False)[0], y) for y in (0, 90, 180, 270)), reverse=True)
        yaw = ys[0][1]
        yaw_margin = ys[0][0] - ys[1][0]
        # --- mirror: its own question, and its own evidence ------------------
        # Left+right IoU catches a handedness error through the POSE (the
        # painted manticore's legs are staggered, so its two flanks are not the
        # same picture); front+back colour catches it through the PAINT (the
        # knight's gold cross is on one side of the surcoat, the stripes the
        # other). Judging mirror on the same all-view score as yaw cannot work:
        # on a near-symmetric subject a flip costs ~0.004, which is noise.
        mir_sc, mir_parts = {}, {}
        for mir in (False, True):
            _, _, per = score(yaw, mir)
            lr = float(np.mean([per[v]['iou'] for v in ('left', 'right')]))
            fb = float(np.mean([per[v]['colour'] for v in ('front', 'back')]))
            mir_parts[mir] = dict(lr_iou=round(lr, 4), fb_colour=round(fb, 4))
            mir_sc[mir] = lr + fb
        flip = bool(mir_sc[True] > mir_sc[False])
        mir_margin = float(abs(mir_sc[True] - mir_sc[False]))
        # A flip is only APPLIED on real evidence. MIRROR_MIN is set above the
        # noise floor these subjects produce: on a near-symmetric figure the
        # two hypotheses land within ~0.006 of each other and the winner is not
        # stable across a change of percentile trim, so a bare argmax would
        # "detect" a handedness error that is not there -- and mirroring a
        # correct model is an unforced corruption of it. Where the evidence IS
        # real the margin is not marginal: both Tripo models reject the flip by
        # ~0.38. Nothing here clears the bar in favour of flipping.
        applied_flip = bool(flip and mir_margin >= MIRROR_MIN)
        I, C, per = score(yaw, applied_flip)
        out[name] = dict(yaw_deg=yaw, flip_x=applied_flip, mirror_argmax=flip,
                         mean_iou=round(I, 4), mean_colour=round(C, 4),
                         yaw_margin_iou=round(yaw_margin, 4),
                         yaw_runner_up=ys[1][1],
                         yaw_iou_by_hypothesis={str(y): round(v, 4) for v, y in ys},
                         mirror_test_no=mir_parts[False], mirror_test_yes=mir_parts[True],
                         mirror_margin=round(mir_margin, 4),
                         per_view=per)
        print(f'{name:30s} yaw={yaw:3d} (margin {yaw_margin:.3f}, next {ys[1][1]})  '
              f'flip={str(applied_flip):5s} (argmax {str(flip):5s}, margin {mir_margin:.4f})  iou={I:.4f} col={C:.4f}  '
              f'per-view iou ' + ' '.join(f'{v[0]}{per[v]["iou"]:.2f}' for v in VIEWS))

json.dump(dict(percentile_trim=[PLO, PHI], models=out),
          open(T6 + f'compare/orientation{"" if PLO == 0 else "_p%g_%g" % (PLO, PHI)}.json', 'w'), indent=1)
print('wrote compare/orientation.json')
