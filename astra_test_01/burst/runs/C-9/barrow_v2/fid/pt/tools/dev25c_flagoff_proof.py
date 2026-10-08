#!/usr/bin/env python3
"""BV2F PT (R-C9-278 B-1): DEV-25c FLAG-OFF PROOF, before either arm -- code-level (the disk gate forbids stitching and
painting now; the byte-level stitch cmp runs the moment disk >= 21 GiB: flag unset -> fid/pt/ps4_dry painting a25fb3).
  T1 TEXTUAL IDENTITY: in every BV2F function DEV-25c touched (_bv2f_tone, _bv2f_grain, _dev27_ctx, _bv2f_poisson), the
     new body with its marked `cb = _cb(c, r)` line removed and `cb` read back as `OV` equals the pre-DEV-25c body
     (fid/pt/dev25c/guided_stitch_before.py, the Tier-B file as shipped at 7ef0ee442) character for character.
     (one normalisation, stated: up[cb-BAND:cb] reads back as up[OV-BAND:], identical since len(up) == OV)
  T2 FUNCTIONAL IDENTITY: _bv2f_tone and _bv2f_grain (pure) executed old vs new on random canvases with DEV-25c unset:
     bit-equal outputs.
  T3 GUARDS: every other DEV-25c line (stitch DEV-26 confinement; the paint stage block) runs only under
     BV2F_DEV25C == '1' AND a chunk listed in cfg['dev25c_chunks']; _cb(c, r) == OV when unset.
  T4 verify.sh green; patch diffs re-derive the shipped Tier-B files.
    python3 fid/pt/tools/dev25c_flagoff_proof.py -> fid/pt/dev25c/flagoff_proof.json"""
import ast, json, re, subprocess, sys
import numpy as np
from scipy import ndimage
V = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid/v1tools"
OUT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid/pt/dev25c"
old = open(OUT + "/guided_stitch_before.py").read()
new = open(V + "/tierB/conductor_scripts/guided_stitch.py").read()
gp_new = open(V + "/tierB/conductor_scripts/guided_paint.py").read()
gp_old = open(OUT + "/guided_paint_before.py").read()


def fn(src, name):
    t = ast.parse(src)
    for n in t.body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return "\n".join(src.splitlines()[n.lineno - 1:n.end_lineno])
    raise KeyError(name)


res = {"T1": {}, "T2": {}, "T3": {}}
for f in ("_bv2f_tone", "_bv2f_grain", "_dev27_ctx", "_bv2f_poisson"):
    b = "\n".join(l for l in fn(new, f).splitlines() if "cb = _cb(c, r)" not in l)
    b = re.sub(r"\bcb\b", "OV", b)
    # the one non-substitution edit: up[cb - BAND:cb] (needed when cb < OV); with cb = OV it IS up[OV - BAND:] (len(up) == OV)
    b = b.replace("up[OV - DEV27_BAND:OV]", "up[OV - DEV27_BAND:]")
    res["T1"][f] = b == fn(old, f)
# T2: exec the pure pieces of both files' DEV-23/25 blocks with the same globals
def ns(src):
    g = {"np": np, "ndimage": ndimage, "os": __import__("os"), "cfg": {}, "W": 1536, "H": 1024, "SX": 1280, "SY": 768, "OV": 256}
    i = src.index("DEV23 = os.environ.get"); j = src.index("# BV2F-BEGIN DEV-27")
    code = "\n".join(l for l in src[i:j].splitlines() if not l.startswith("# BV2F-"))
    exec(code, g)
    return g
go, gn = ns(old), ns(new)
rng = np.random.default_rng(278)
ok = True
for t in range(3):
    im = rng.uniform(120, 255, (1024, 1536, 3)); im[300:500, 400:900] *= 0.4
    for (c, r) in ((1, 0), (0, 1), (1, 1)):
        a = go["_bv2f_grain"](go["_bv2f_tone"](im, c, r), c, r)
        b = gn["_bv2f_grain"](gn["_bv2f_tone"](im, c, r), c, r)
        ok &= bool(np.array_equal(a, b))
res["T2"]["tone_then_grain_bit_equal_9_cases"] = ok
res["T2"]["_cb_unset"] = gn["_cb"](3, 2) == 256 and not gn["DEV25C"]
# T3: the guards, read from the code
res["T3"]["stitch_dev26_confinement_guarded"] = "if DEV25C_CHUNKS:   # BV2F DEV-25c" in new
res["T3"]["stitch_chunks_empty_unless_flag"] = "DEV25C_CHUNKS = set(cfg.get('dev25c_chunks', [])) if DEV25C else set()" in new
res["T3"]["paint_block_guarded"] = "if os.environ.get('BV2F_DEV25C') == '1' and k in cfg.get('dev25c_chunks', []):" in gp_new
res["T3"]["paint_unchanged_outside_block"] = re.sub(r"# BV2F-BEGIN DEV-25c.*?# BV2F-END\n", "", gp_new, flags=re.S) == gp_old
v = subprocess.run(["bash", V + "/verify.sh"], capture_output=True, text=True)
res["T4_verify"] = v.stdout.strip().splitlines()[-1]
res["pass"] = all(res["T1"].values()) and all(res["T2"].values()) and all(res["T3"].values()) and v.returncode == 0
res["owed_when_disk_allows"] = "byte-level: BV2F_DEV25C unset, cfg_bv2a_pilot_ps4 stitch == fid/pt/ps4_dry/painting.png (a25fb3); all flags 0 == Tier-A v1 (cmp)"
json.dump(res, open(OUT + "/flagoff_proof.json", "w"), indent=1)
print(json.dumps(res, indent=1))
