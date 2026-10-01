# R-C9-105 paint pass: install a baked texture into a GLB as a BINARY patch -- every embedded image is replaced by the
# given file (JPEG, quality 92); every other bufferView keeps its bytes (mesh, skin, morphs, clips byte-identical).
#   python3 s41_swap_image.py <in.glb> <texture.png> <out.glb> [--size 2048]
import io, json, os, sys
from PIL import Image
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre')
a = sys.argv[1:]; IN, TEX, OUT = a[0], a[1], a[2]
SIZE = int(a[a.index('--size') + 1]) if '--size' in a else None
js, b = L.load_glb(IN)
im = Image.open(TEX).convert("RGB")
if SIZE and im.size != (SIZE, SIZE):
    im = im.resize((SIZE, SIZE), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, "JPEG", quality=92); data = buf.getvalue()
img_views = {}
for i, img in enumerate(js.get("images", [])):
    assert "bufferView" in img, "image %d is not embedded" % i
    img_views[img["bufferView"]] = i
    img["mimeType"] = "image/jpeg"
out = bytearray(); views = []
for v, bv in enumerate(js["bufferViews"]):
    bv = dict(bv)
    chunk = data if v in img_views else bytes(b[bv.get("byteOffset", 0):bv.get("byteOffset", 0) + bv["byteLength"]])
    while len(out) % 4:
        out.append(0)
    bv["byteOffset"] = len(out); bv["byteLength"] = len(chunk); out += chunk; views.append(bv)
js["bufferViews"] = views; js["buffers"] = [{"byteLength": len(out)}]
R_.write_glb(OUT, js, bytes(out))
j2, b2 = L.load_glb(OUT)
same = all(bytes(b[v0.get("byteOffset", 0):v0.get("byteOffset", 0) + v0["byteLength"]]) ==
           bytes(b2[v1["byteOffset"]:v1["byteOffset"] + v1["byteLength"]])
           for k, (v0, v1) in enumerate(zip(L.load_glb(IN)[0]["bufferViews"], j2["bufferViews"])) if k not in img_views)
print(json.dumps(dict(input=os.path.basename(IN), out=OUT, images_replaced=len(img_views), texture=os.path.basename(TEX),
                      tex_px=list(im.size), other_views_identical=same, mb=round(os.path.getsize(OUT) / 1e6, 2))))
