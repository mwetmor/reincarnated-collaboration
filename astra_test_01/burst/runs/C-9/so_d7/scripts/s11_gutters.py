# Where do her white speckles come from? The texture's GUTTERS -- texels no triangle maps to.
#
#   python3 scripts/s11_gutters.py <x.glb> [...]   (read-only survey)
#   python3 scripts/s11_gutters.py --fix <in.glb> <out.glb> [--tag <tagged.glb>]
#
# Everything is read from the GLB itself -- UVs and indices from the accessors, the image from
# its bufferView -- so no Blender round trip is involved. That matters: a Blender re-export
# re-orders the joints by hierarchy and undoes 52_weapon_bones' appended weapon_r / weapon_l.
# The fix rewrites ONLY the image bytes and the bufferView offsets after them.
#
# COVERAGE = the union of every triangle that samples this image, rasterised in texel space
# (glTF v runs top-down, like image rows). A texel outside it is gutter. At play scale the GPU
# samples a low MIP level, and a mip averages blocks of texels -- so a WHITE gutter next to an
# island is averaged into the island's edge. That is a speckle along every seam.
#
# FIX = fill EVERY gutter texel with its nearest covered texel's colour (an exact Euclidean
# distance transform), not a few-texel dilation: at ~100 px/m a 4096 texture is read around
# mip 4-5, 16-32 texels a sample, and a shallow dilation would only move the speckle outward.
#
# --tag writes a copy with every gutter texel pure MAGENTA -- the render instrument's control:
# a pixel that turns magenta in the tagged render is a pixel the gutters reach.
import io, json, struct, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
sys.path.insert(0, __file__.rsplit('/', 1)[0])
L = __import__('21_lint_export')


def primitives_by_image(g):
    """image index -> list of (uv accessor, index accessor or None)"""
    tex_img = {i: t.get('source') for i, t in enumerate(g.get('textures', []))}
    mat_img = {}
    for mi, m in enumerate(g.get('materials', [])):
        bct = (m.get('pbrMetallicRoughness') or {}).get('baseColorTexture')
        if bct is not None:
            mat_img[mi] = (tex_img.get(bct['index']), bct.get('texCoord', 0))
    out = {}
    for me in g.get('meshes', []):
        for p in me.get('primitives', []):
            if p.get('mode', 4) != 4 or p.get('material') not in mat_img:
                continue
            img, tc = mat_img[p['material']]
            uva = p['attributes'].get('TEXCOORD_%d' % tc)
            if img is None or uva is None:
                continue
            out.setdefault(img, []).append((uva, p.get('indices')))
    return out


def coverage(g, b, prims, W, H):
    m = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(m)
    for uva, ia in prims:
        uv = L.read_accessor(g, b, uva)
        idx = (L.read_accessor(g, b, ia)[:, 0].astype(np.int64) if ia is not None
               else np.arange(len(uv)))
        tri = uv[idx.reshape(-1, 3)] * np.array([W, H])
        for t in tri:
            d.polygon([tuple(t[0]), tuple(t[1]), tuple(t[2])], fill=255)
    cov = np.asarray(m) > 0
    # a rasterised triangle under-covers by up to half a texel at its edge: grow by one
    return ndimage.binary_dilation(cov, iterations=1)


def near_white(a):
    return (a[..., :3].min(-1) > 225)


def survey(path):
    g, b = L.load_glb(path)
    by = primitives_by_image(g)
    rep = {}
    for ii, prims in by.items():
        im = g['images'][ii]
        bv = g['bufferViews'][im['bufferView']]
        o = bv.get('byteOffset', 0)
        arr = np.asarray(Image.open(io.BytesIO(b[o:o + bv['byteLength']])).convert('RGB'))
        H, W = arr.shape[:2]
        cov = coverage(g, b, prims, W, H)
        gut = ~cov
        wg = gut & near_white(arr)
        # gutters that TOUCH an island are the ones a mip can pull in
        ring = gut & ndimage.binary_dilation(cov, iterations=24)
        rep[ii] = dict(size=[W, H], coverage_pct=round(100 * cov.mean(), 2),
                       gutter_near_white_pct=round(100 * wg.sum() / max(gut.sum(), 1), 2),
                       white_texels_within_24_of_an_island=int((ring & near_white(arr)).sum()),
                       own_whites_inside_islands=int((cov & near_white(arr)).sum()))
    return rep


def fix(src, dst, tag=None):
    g, b = L.load_glb(src)
    by = primitives_by_image(g)
    new_bytes, tag_bytes, rep = {}, {}, {}
    for ii, prims in by.items():
        im = g['images'][ii]
        bv = g['bufferViews'][im['bufferView']]
        o = bv.get('byteOffset', 0)
        pil = Image.open(io.BytesIO(b[o:o + bv['byteLength']]))
        fmt = (pil.format or 'PNG').upper()
        arr = np.asarray(pil.convert('RGB')).copy()
        H, W = arr.shape[:2]
        cov = coverage(g, b, prims, W, H)
        _, (iy, ix) = ndimage.distance_transform_edt(~cov, return_indices=True)
        filled = arr[iy, ix]
        tagged = filled.copy()
        tagged[~cov] = (255, 0, 255)
        def enc(a):
            bio = io.BytesIO()
            if fmt == 'JPEG':
                Image.fromarray(a).save(bio, 'JPEG', quality=95)
            else:
                Image.fromarray(a).save(bio, 'PNG', optimize=True)
            return bio.getvalue()
        new_bytes[im['bufferView']] = enc(filled)
        tag_bytes[im['bufferView']] = enc(tagged)
        rep[ii] = dict(format=fmt, size=[W, H], gutter_filled_pct=round(100 * (~cov).mean(), 2),
                       white_gutter_before=int((~cov & near_white(arr)).sum()),
                       white_gutter_after=int((~cov & near_white(filled)).sum()))
    write(g, b, new_bytes, dst)
    if tag:
        write(g, b, tag_bytes, tag)
    return rep


def write(g, b, repl, dst):
    """Rebuild BIN: every bufferView in its original order, replacements swapped in, 4-aligned.
    Accessors address bufferViews, not raw offsets, so only byteOffset/byteLength change."""
    g = json.loads(json.dumps(g))
    order = sorted(range(len(g['bufferViews'])), key=lambda i: g['bufferViews'][i].get('byteOffset', 0))
    out = bytearray()
    for i in order:
        bv = g['bufferViews'][i]
        o = bv.get('byteOffset', 0)
        data = repl.get(i, b[o:o + bv['byteLength']])
        while len(out) % 4:
            out.append(0)
        bv['byteOffset'] = len(out)
        bv['byteLength'] = len(data)
        out += data
    while len(out) % 4:
        out.append(0)
    g['buffers'][0]['byteLength'] = len(out)
    js = json.dumps(g, separators=(',', ':')).encode()
    js += b' ' * (-len(js) % 4)
    total = 12 + 8 + len(js) + 8 + len(out)
    with open(dst, 'wb') as f:
        f.write(struct.pack('<4sII', b'glTF', 2, total))
        f.write(struct.pack('<I4s', len(js), b'JSON')); f.write(js)
        f.write(struct.pack('<I4s', len(out), b'BIN\x00')); f.write(bytes(out))


if __name__ == '__main__':
    if sys.argv[1] == '--fix':
        tag = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else None
        print(json.dumps(fix(sys.argv[2], sys.argv[3], tag)))
    else:
        for p in sys.argv[1:]:
            for ii, r in survey(p).items():
                print("%-14s img %d %s cov %5.1f%% | gutter near-white %5.1f%% | white texels within 24 of an island %8d | island whites %8d"
                      % (p.split('/')[-1], ii, r['size'], r['coverage_pct'], r['gutter_near_white_pct'],
                         r['white_texels_within_24_of_an_island'], r['own_whites_inside_islands']))
