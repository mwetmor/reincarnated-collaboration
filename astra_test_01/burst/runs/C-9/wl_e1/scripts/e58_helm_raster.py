# E1b R-C9-141: light (no-Blender) z-buffer raster of the helm piece at REST, textured by its own base colour, from the
# play camera's pitch (52.95 deg) at a heading, ortho. Also writes a per-pixel face-id map and a Lambert shade map, so a mark
# can be traced to triangles and texels.  python3 e58_helm_raster.py <helm.glb> <out_prefix> [--heading S] [--ppm 2000]
#   [--center x,y,z] [--half 0.16] [--tex <png>] [--light]
import sys, os, json, math, numpy as np, io
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
BEAR = {"S": 90.0, "SW": 135.0, "W": 180.0, "NW": 225.0, "N": 270.0, "NE": 315.0, "E": 0.0, "SE": 45.0}
def load(path):
    js, b = L.load_glb(path); G, _ = W.globals_(js); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
    V = W.skin_rest(js, b, mn, G); pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
    uv = L.read_accessor(js, b, pr['attributes']['TEXCOORD_0']); I = L.read_accessor(js, b, pr['indices']).reshape(-1, 3).astype(int)
    mat = js['materials'][pr.get('material', 0)]; ti = mat['pbrMetallicRoughness']['baseColorTexture']['index']
    im = js['images'][js['textures'][ti]['source']]; bv = js['bufferViews'][im['bufferView']]; o = bv.get('byteOffset', 0)
    tex = Image.open(io.BytesIO(bytes(b[o:o + bv['byteLength']]))).convert('RGB')
    return V, uv, I, tex
def view_basis(heading, pitch=52.9535):
    # model frame: x right, y up, +z forward (he faces +z). heading bearing b -> model turned by theta = 90 - b about +y,
    # camera fixed looking along -Z_world from +Z, pitched down. Equivalently rotate the model by theta then view.
    th = math.radians(90.0 - BEAR[heading]); c, s = math.cos(th), math.sin(th)
    Ry = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    p = math.radians(pitch)
    d = np.array([0, math.sin(p), math.cos(p)])           # toward the camera (world)
    right = np.array([1.0, 0, 0]); up = np.cross(d, right); up /= np.linalg.norm(up)
    return Ry, right, up, d
def raster(V, uv, I, tex, heading, ppm, center, half, light=False, pitch=52.9535):
    Ry, right, up, d = view_basis(heading, pitch)
    P = (V - center) @ Ry.T
    sx = P @ right; sy = P @ up; dz = P @ d
    N = int(round(2 * half * ppm)); px = (sx + half) * ppm; py = (half - sy) * ppm
    zb = np.full((N, N), -1e9); fid = np.full((N, N), -1, int); col = np.zeros((N, N, 3)); uvb = np.zeros((N, N, 2))
    T = np.asarray(tex, np.float32) / 255.0; TH, TW = T.shape[:2]
    for f, (a, b_, c_) in enumerate(I):
        xs = px[[a, b_, c_]]; ys = py[[a, b_, c_]]
        x0, x1 = int(max(0, math.floor(xs.min()))), int(min(N - 1, math.ceil(xs.max()))); y0, y1 = int(max(0, math.floor(ys.min()))), int(min(N - 1, math.ceil(ys.max())))
        if x0 > x1 or y0 > y1: continue
        den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if abs(den) < 1e-12: continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l0 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den
        l1 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den; l2 = 1 - l0 - l1
        m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        if not m.any(): continue
        z = l0 * dz[a] + l1 * dz[b_] + l2 * dz[c_]
        sub = zb[y0:y1 + 1, x0:x1 + 1]; w = m & (z > sub)
        if not w.any(): continue
        sub[w] = z[w]; fid[y0:y1 + 1, x0:x1 + 1][w] = f
        u = l0 * uv[a, 0] + l1 * uv[b_, 0] + l2 * uv[c_, 0]; v = l0 * uv[a, 1] + l1 * uv[b_, 1] + l2 * uv[c_, 1]
        uvb[y0:y1 + 1, x0:x1 + 1][w] = np.stack([u[w], v[w]], -1)
    hit = fid >= 0
    tu = np.clip((uvb[..., 0] % 1.0) * TW, 0, TW - 1).astype(int); tv = np.clip((uvb[..., 1] % 1.0) * TH, 0, TH - 1).astype(int)
    col[hit] = T[tv[hit], tu[hit]]
    # face normals (rotated) for shading
    Pn = P; fn = np.cross(Pn[I[:, 1]] - Pn[I[:, 0]], Pn[I[:, 2]] - Pn[I[:, 0]]); fn /= np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12
    Ld = d + np.array([0.3, 0.5, 0.0]); Ld /= np.linalg.norm(Ld)
    sh = np.zeros((N, N)); sh[hit] = np.abs(fn[fid[hit]] @ Ld)
    return dict(col=col, hit=hit, fid=fid, uv=uvb, shade=sh, zb=zb, N=N)
if __name__ == '__main__':
    a = sys.argv[1:]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    V, uv, I, tex = load(a[0])
    if opt('--tex'): tex = Image.open(opt('--tex')).convert('RGB')
    ctr = np.array([float(x) for x in opt('--center', '0,1.86,-0.05').split(',')])
    R = raster(V, uv, I, tex, opt('--heading', 'S'), float(opt('--ppm', '2000')), ctr, float(opt('--half', '0.16')))
    bg = np.array([0.35, 0.35, 0.37]); img = np.where(R['hit'][..., None], R['col'] * (0.45 + 0.75 * R['shade'][..., None]) if '--light' in a else R['col'], bg)
    Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save(a[1] + '.png')
    Image.fromarray((np.where(R['hit'], 0.15 + 0.85 * R['shade'], 0.3) * 255).astype(np.uint8)).save(a[1] + '_shade.png')
    np.savez_compressed(a[1] + '.npz', fid=R['fid'], uv=R['uv'].astype(np.float32))
    print('wrote', a[1], R['N'])
