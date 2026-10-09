#!/usr/bin/env python3
"""s52 (e) P3 on the FULL SITE per R-C9-201 (2) / s36: the sea read on ph_p3_sea.gd captures at the site guide plate
(6656 x 4096): rg_base (painted base only), rg_rest (TIME 0), rg_red (lit plane: must FAIL). BINDING = every P3 class on
the rg_base capture <= 15.5. -> results/site/p3_sea.json"""
import os
import sys
os.environ["PH_SITE"] = "1"
os.environ.setdefault("PH_PILOT_OUT", "results/site")
sys.path.insert(0, os.path.dirname(__file__))
import pilot_harness as H  # noqa
from common import *  # noqa
import p3_residual as R3

D = PH / "renders/site/p3_sea"
P = H.painting()
M = H.p3_masks()
out = {}
for nm in ("rg_base", "rg_rest", "rg_red"):
    R = load_rgb(D / (nm + ".png"))
    assert R.shape == P.shape, (nm, R.shape)
    out[nm] = R3.resid(R, P, M["ground: sea"])
    out[nm + "_sha256"] = sha256(D / (nm + ".png"))
Rb = load_rgb(D / "rg_base.png")
rows = {k: R3.resid(Rb, P, m) for k, m in M.items()}
v = R3.verdict(rows)
out["binding_all_classes_on_rg_base"] = v
out["RED_lit_plane_fails"] = out["rg_red"]["mean_abs"] > 15.5
out["pass"] = v["pass"] and out["RED_lit_plane_fails"]
dump(out, str(H.OUT / "p3_sea.json"))
print({k: out[k] for k in ("rg_base", "rg_rest", "rg_red", "RED_lit_plane_fails", "pass")}, v["worst_class"], v["value"])
