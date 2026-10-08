#!/usr/bin/env python3
"""BV2F PT: every placement id the pilot ID render (fid/pt/pilot/ids_built) shows -- one per line. pt_export_meshes.gd
keeps only the real models among them (LV's bv2f_fit meta), so its exported set IS the pilot's real-model list."""
import json, os
import numpy as np
from PIL import Image
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(FID, "pt", "pilot", "ids_built")
pl = json.load(open(os.path.join(D, "ids.json")))["placements"]
A = np.asarray(Image.open(os.path.join(D, "ids.png")).convert("RGB")).astype(np.int32)
idx = np.where(A[..., 2] > 100, np.clip(np.round((A[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
               + np.clip(np.round((A[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
n = np.bincount(idx.ravel(), minlength=256)
for k, v in sorted(pl.items(), key=lambda kv: kv[1]["id"]):
    if n[int(k)] > 0:
        print(v["id"])
