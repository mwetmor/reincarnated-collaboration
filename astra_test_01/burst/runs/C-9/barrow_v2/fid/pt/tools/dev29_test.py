#!/usr/bin/env python3
"""BV2F PT (R-C9-299): DEV-29 constructed test -- the Tier-B block executed in isolation (exec of the BV2F-BEGIN/END text)
on a synthetic canvas: (1) key absent -> the canvas is the SAME object (v1); (2) key present -> exactly the pasted px inside
the mask change, to the patched painting's values; unpasted px and pasted px outside the mask are byte-identical; (3) a
wrong sha -> HALT. -> fid/pt/dev29/dev29_test.json"""
import hashlib, json, os, pathlib, sys
import numpy as np
from PIL import Image
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
OUT = FID + "/pt/dev29"; os.makedirs(OUT, exist_ok=True)
src = open(FID + "/v1tools/tierB/conductor_scripts/guided_paint.py").read()
i = src.index("# BV2F-BEGIN DEV-29"); blk = src[i:src.index("# BV2F-END", i)]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rng = np.random.default_rng(299)
PP = rng.integers(0, 255, (2560, 4096, 3), dtype=np.uint8); Image.fromarray(PP).save(OUT + "/_t_painting.png")
MM = np.zeros((2560, 4096), np.uint8); MM[2400:2560, 900:1300] = 255; MM[1000:1100, 3000:3100] = 255; Image.fromarray(MM).save(OUT + "/_t_mask.png")
c, r, COLS = 1, 3, 5; ox, oy = 1280 * c, 768 * r          # chunk 1_3: context from 0_3 (left), 1_2 (top), 2_2 (top-right), 0_2
can0 = rng.integers(0, 255, (1024, 1536, 3), dtype=np.uint8)
done = lambda k: k in ("0_3", "1_2", "2_2", "0_2")
res = {}
for name, cfg in (("absent", {}), ("present", {"context_patch": {"painting": OUT + "/_t_painting.png", "painting_sha256": sha(OUT + "/_t_painting.png"), "mask": OUT + "/_t_mask.png", "mask_sha256": sha(OUT + "/_t_mask.png")}}),
                  ("wrong_sha", {"context_patch": {"painting": OUT + "/_t_painting.png", "painting_sha256": "0" * 64, "mask": OUT + "/_t_mask.png", "mask_sha256": sha(OUT + "/_t_mask.png")}})):
    canvas = Image.fromarray(can0)
    ns = {"cfg": cfg, "kept": ["x"], "canvas": canvas, "c": c, "r": r, "COLS": COLS, "ox": ox, "oy": oy, "done": done, "k": "1_3",
          "hashlib": hashlib, "pathlib": pathlib, "sys": sys, "Image": Image}
    try:
        exec(blk, ns)
    except SystemExit as e:
        res[name] = {"halt": str(e)[:50]}; continue
    out = np.asarray(ns["canvas"])
    ch = (out != can0).any(-1)
    pz = np.zeros((1024, 1536), bool); pz[:, :256] = True; pz[:256, :] = True   # left + top context of 1_3
    want = np.zeros((1024, 1536), bool); want[:2560 - oy, :] = MM[oy:2560, ox:ox + 1536] > 127; want &= pz
    res[name] = {"same_object": ns["canvas"] is canvas, "changed_px": int(ch.sum()), "changed_equals_pasted_and_mask": bool((ch == want).all()) if name == "present" else None,
                 "values_from_painting": bool((out[want] == np.pad(PP[oy:oy + 1024, ox:ox + 1536], ((0, 1024 - PP[oy:oy + 1024].shape[0]), (0, 0), (0, 0)))[want]).all()) if name == "present" else None}
res["pass"] = res["absent"]["same_object"] and res["present"]["changed_equals_pasted_and_mask"] and res["present"]["values_from_painting"] and "halt" in res["wrong_sha"]
for f in ("_t_painting.png", "_t_mask.png"):
    os.replace(OUT + "/" + f, "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/df21e264-6571-4d04-96ee-b8e2bd6d97fa/scratchpad/" + f)
json.dump(res, open(OUT + "/dev29_test.json", "w"), indent=1); print(json.dumps(res))
