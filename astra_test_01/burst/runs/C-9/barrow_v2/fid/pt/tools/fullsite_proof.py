#!/usr/bin/env python3
"""BV2F PT (R-C9-272 (c)): FULL-SITE STITCH proofs P-1..P-3 on a STAND-IN (0 images, no Godot).
Stand-in prefix BV2F-PS4SI: the 9 pilot chunks = byte copies of the PS4 canvases; the 16 new chunks (cols 3-4, rows 3-4)
= crops of the pinned PS4 guide at their grid positions (any pixels serve: only the stitch's mechanics are under test).
  S0  3x3 stand-in stitch (DEV-23/25/26/27 on) == fid/pt/ps4_dry/painting.png (the pilot stitch, a25fb3), and its
      DEV-26 band paths recorded (BV2F_DEV26_DUMP) -> fid/pt/r272/fullsite/dev26_paths_pilot.json
  P-1/P-2  5x5 stitch WITH the pin (x_len 2304, y_len 3840): the pilot region x < 3840, y < 2304 byte-identical to S0
  P-3  5x5 stitch WITHOUT the pin: the control -- the pilot region must MOVE (else the proof cannot fail)
  P-2b 5x5, pin + DEV-24 (per-patch read-region check): the pilot region == the pilot-4 build painting (7105731298ef)
Every stitch runs the shipped Tier-B guided_stitch.py; outputs go to the scratch dir given; records to fid/pt/r272/fullsite/.
    python3 fid/pt/tools/fullsite_proof.py <scratch dir>"""
import hashlib, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
A9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts"
GS = FID + "/v1tools/tierB/conductor_scripts/guided_stitch.py"
OUT = FID + "/pt/r272/fullsite"
SCR = sys.argv[1]
os.makedirs(OUT, exist_ok=True); os.makedirs(SCR, exist_ok=True)
PX = "BV2F-PS4SI"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
psha = lambda a: hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
XL, YL = 3840, 2304          # the pilot region kept identical: x < 3840, y < 2304 (outside the new joins' zones)


def stand_in():
    G = Image.open(FID + "/pt/pilot/guide_art_pinned_ps4.png").convert("RGB")
    rec = {}
    for r in range(5):
        for c in range(5):
            k = "%d_%d" % (c, r)
            d = "%s/%s-%s" % (A9, PX, k)
            os.makedirs(d, exist_ok=True)
            p = "%s/%s-%s.png" % (d, PX, k)
            if c <= 2 and r <= 2:
                shutil.copyfile("%s/BV2F-PS4-%s/BV2F-PS4-%s.png" % (A9, k, k), p)
                rec[k] = {"from": "BV2F-PS4-%s (byte copy)" % k}
            else:
                G.crop((1280 * c, 768 * r, 1280 * c + 1536, 768 * r + 1024)).save(p)
                rec[k] = {"from": "pinned PS4 guide crop (stand-in)"}
            rec[k]["sha256"] = sha(p)
            json.dump({"_what": "R-C9-272 (c) STAND-IN chunk for the full-site stitch proof -- NOT a painting", **rec[k]},
                      open(d + "/STAND_IN.json", "w"), indent=1)
    return rec


def cfg(n, pin=None, dev24=None):
    c = json.load(open(FID + "/pt/pilot/cfg_bv2a_pilot_ps4.json"))
    c["prefix"], c["cols"], c["rows"] = PX, n, n
    c.pop("dev24", None)
    if pin:
        c["dev26_pin"] = pin
    if dev24:
        c["dev24"] = dev24
    p = "%s/cfg_%d_%s%s.json" % (SCR, n, "pin" if pin else "nopin", "_dev24" if dev24 else "")
    json.dump(c, open(p, "w"), indent=1)
    return p


def stitch(cfgp, outp, env=None):
    e = dict(os.environ, **(env or {}))
    r = subprocess.run(["python3", GS, cfgp, outp], env=e, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("stitch failed: %s\n%s" % (cfgp, r.stdout[-2000:] + r.stderr[-2000:]))
    return np.asarray(Image.open(outp).convert("RGB")), r.stdout


def main():
    res = {"_what": __doc__.split("\n")[0], "stand_in": stand_in()}
    dump = OUT + "/dev26_paths_pilot.json"
    s0, log0 = stitch(cfg(3), SCR + "/s0_3x3.png", {"BV2F_DEV26_DUMP": dump})
    ref = np.asarray(Image.open(FID + "/pt/ps4_dry/painting.png").convert("RGB"))
    res["S0"] = {"equals_ps4_dry_stitch": bool((s0 == ref).all()), "pixels_sha256": psha(s0), "paths": sha(dump)}
    pin = {"file": dump, "sha256": sha(dump), "x_len": YL, "y_len": XL}
    full_pin, logp = stitch(cfg(5, pin), SCR + "/p2_5x5_pin.png")
    reg = (slice(0, YL), slice(0, XL))
    d = (full_pin[reg] != s0[reg]).any(-1)
    res["P2_pin"] = {"pilot_region_identical": bool(not d.any()), "px_changed": int(d.sum()),
                     "pinned": [l for l in logp.splitlines() if l.startswith("DEV-26")][:1]}
    full_nopin, _ = stitch(cfg(5), SCR + "/p3_5x5_nopin.png")
    d3 = (full_nopin[reg] != s0[reg]).any(-1)
    ys, xs = np.nonzero(d3) if d3.any() else ([], [])
    res["P3_nopin_control"] = {"pilot_region_moves": bool(d3.any()), "px_changed": int(d3.sum()),
                               "bbox": [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))] if d3.any() else None}
    # P-2b: DEV-24 with per-patch read-region pins (computed on each layer's staged base)
    sys.path.insert(0, FID + "/v1tools")
    import dev24
    blk = json.load(open(FID + "/pt/dev24/dev24_block.json"))
    bases = [ref, np.asarray(Image.open(FID + "/pt/dev24/layer1.png")), np.asarray(Image.open(FID + "/pt/dev24/layer2.png"))]
    for li, layer in enumerate(blk["layers"]):
        assert dev24.pixels_sha(bases[li]) == layer["base_pixels_sha256"]
        for p in layer["patches"]:
            p["read_sha256"] = dev24.read_sha(bases[li], p)
    json.dump(blk, open(OUT + "/dev24_block_readpins.json", "w"), indent=1)
    full24, log24 = stitch(cfg(5, pin, blk), SCR + "/p2b_5x5_pin_dev24.png", {"BV2F_DEV24": "1"})
    built = np.asarray(Image.open(FID + "/pt/pilot/painting.png").convert("RGB"))
    d24 = (full24[reg] != built[reg]).any(-1)
    res["P2b_pin_dev24"] = {"pilot_region_equals_pilot4_build": bool(not d24.any()), "px_changed": int(d24.sum()),
                            "read_regions_inside_pilot_region": None}
    # every patch's read region inside x < 3840, y < 2304?
    inside = True
    for layer in blk["layers"]:
        for p in layer["patches"]:
            x0, y0 = p["rect_xy"]
            R = np.asarray(Image.open(p["region_png"])) > 127
            pc = np.asarray(Image.open(p["paste_png"])) > 127
            rr = dev24.read_region(R, pc)
            yy, xx = np.nonzero(rr)
            if (xx + x0).max() >= XL or (yy + y0).max() >= YL:
                inside = False
    res["P2b_pin_dev24"]["read_regions_inside_pilot_region"] = inside
    json.dump(res, open(OUT + "/fullsite_proof.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "stand_in"}, indent=1))


if __name__ == "__main__":
    main()
