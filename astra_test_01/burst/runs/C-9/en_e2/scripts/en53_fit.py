# EN-E2: a pack's canvas fit -- every cell's alpha union bbox vs the 768 canvas (anchor 384,448): the tightest cells, the margin
# (gate 5 % = 38.4 px), and the largest height factor that would still clear the gate (fit x).
#   python3 scripts/en53_fit.py <pack dir>
import json, sys
K = sys.argv[1]; d = json.load(open('%s/matrix_index.json' % K))
bb = [c['alpha_union_bbox'] for c in d['cells'].values()]; u = (min(b[0] for b in bb), min(b[1] for b in bb), max(b[2] for b in bb), max(b[3] for b in bb))
w = sorted((min(c['alpha_union_bbox'][0], c['alpha_union_bbox'][1], 768 - c['alpha_union_bbox'][2], 768 - c['alpha_union_bbox'][3]), k) for k, c in d['cells'].items())
L, T, R, B = 384 - u[0], 448 - u[1], u[2] - 384, u[3] - 448; allow = (384 - 38.4, 448 - 38.4, 384 - 38.4, 320 - 38.4)
f = min(a / max(x, 1e-6) for a, x in zip(allow, (L, T, R, B))); st = [c['status'] for c in d['cells'].values()]
print('FIT', K.split('/')[-1], d['complete'], '/', d['expected'], {s: st.count(s) for s in set(st)}, 'h', d['source']['h_model_m'], 'union', u, 'tightest', w[:2], 'margin %.1f%%' % (100 * w[0][0] / 768), 'fit x%.3f' % f)
