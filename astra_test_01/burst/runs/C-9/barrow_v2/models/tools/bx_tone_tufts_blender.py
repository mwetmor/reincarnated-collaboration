"""lane BX (R-C9-156 follow-up, Matt): tone the bright red leafy tufts on the rock/mound models toward sketch A's
muted rust heather, and break them into smaller tufts.

    blender --background --python bx_tone_tufts_blender.py -- <in.glb> <out.glb>

In each base-colour image: pixels that are saturated red/red-orange (hue <= 28 deg or >= 335 deg, saturation >= 0.42,
value >= 0.22) are shifted to rust-orange (hue ~24 deg), desaturated (x0.55) and darkened (x0.82); then a
high-frequency noise mask breaks each blob up -- ~40% of those pixels are blended 75% toward the image's own median
non-tuft colour (the rock/snow around them), leaving smaller, sparser tufts. Geometry is untouched.
"""
import sys
import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
src, dst = argv[0], argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)


def rgb_to_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn + 1e-9
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60.0
    s = np.where(mx > 0, (mx - mn) / (mx + 1e-9), 0)
    return h, s, mx


def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - np.abs((h / 60.0) % 2 - 1))
    m = v - c
    z = np.zeros_like(h)
    k = (h // 60).astype(int) % 6
    rgb = np.select([k[..., None] == i for i in range(6)],
                    [np.stack(t, -1) for t in ((c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x))])
    return rgb + m[..., None]


rng = np.random.default_rng(156)
for img in bpy.data.images:
    if img.size[0] == 0:
        continue
    w, h_ = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h_, w, img.channels)
    rgb = px[..., :3]
    H, S, V = rgb_to_hsv(rgb)
    tuft = ((H <= 28) | (H >= 335)) & (S >= 0.42) & (V >= 0.22)
    n = int(tuft.sum())
    if n == 0:
        continue
    base = np.median(rgb[~tuft], axis=0)
    H2 = np.full_like(H, 24.0)
    toned = hsv_to_rgb(H2, S * 0.55, V * 0.82)
    noise = rng.random((h_ // 3 + 1, w // 3 + 1)).repeat(3, 0).repeat(3, 1)[:h_, :w]
    breakup = tuft & (noise < 0.40)
    out = rgb.copy()
    out[tuft] = toned[tuft]
    out[breakup] = 0.25 * out[breakup] + 0.75 * base
    px[..., :3] = out
    img.pixels[:] = px.ravel()
    img.update()
    img.pack()
    print("[tufts] %s: %d px (%.1f%%) toned, %d broken up; base %s" % (img.name, n, 100.0 * n / (w * h_), int(breakup.sum()), np.round(base, 3)))
bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", export_image_format="JPEG", export_jpeg_quality=90, export_yup=True)
