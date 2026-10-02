# EN-E2 round 5: the frost-gaunt vs the revenant, BODY L* at the play camera (the conductor's separation measure). Pixels by exact region:
#   gaunt   = beauty pixels whose class-pass pixel is RED in en39's region-ID texture (the graded SINEW, rime excluded) and GREEN (the head)
#   revenant= beauty pixels whose class-pass pixel is GREEN in en17's region-ID texture (the BONE, en16 rule "ivory")
# Both from the same harness, idle + walk, 8 headings, scale 1.
#   python3 scripts/en40_value_sep.py <gaunt_stills_dir> <revenant_stills_dir> [--json f]
import sys, glob, os, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); C = __import__('en16_colourlib')
def collect(D, sel):
    out = []
    for bf in sorted(glob.glob(os.path.join(D, '*_beauty.png'))):
        b = np.asarray(Image.open(bf).convert('RGB')).astype(float) / 255; c = np.asarray(Image.open(bf.replace('_beauty', '_class')).convert('RGB')).astype(int)
        out.append(C.rgb2lab(b[sel(c)]))
    return np.concatenate(out)
red = lambda c: (c[..., 0] > 200) & (c[..., 1] < 50) & (c[..., 2] < 50)
green = lambda c: (c[..., 1] > 200) & (c[..., 0] < 50) & (c[..., 2] < 50)
g_body = collect(sys.argv[1], red); g_head = collect(sys.argv[1], green); r_bone = collect(sys.argv[2], green)
rep = dict(gaunt_sinew_L=round(float(g_body[:, 0].mean()), 2), gaunt_sinew_lab=g_body.mean(0).round(2).tolist(), gaunt_head_L=round(float(g_head[:, 0].mean()), 2),
           revenant_bone_L=round(float(r_bone[:, 0].mean()), 2), revenant_bone_lab=r_bone.mean(0).round(2).tolist(),
           separation_dL=round(float(r_bone[:, 0].mean() - g_body[:, 0].mean()), 2), head_vs_body_dL=round(float(g_head[:, 0].mean() - g_body[:, 0].mean()), 2),
           px=dict(gaunt_sinew=len(g_body), gaunt_head=len(g_head), revenant_bone=len(r_bone)))
print('VALUE', json.dumps(rep))
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
