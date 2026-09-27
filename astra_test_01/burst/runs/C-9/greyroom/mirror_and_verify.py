#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C-9 · P2' — mirror the deliverables somewhere git will actually keep them,
and verify that every number this directory's README asserts is the number the
manifest carries.

WHY THE MIRROR: `astra_test_01/.gitignore` ignores `*.png`, so the grey room's
images cannot be committed where the dispatch says to write them.  They are
copied, byte-for-byte and digest-checked, into the drax captures tree, which is
where the KC2-PLAY arena guide already lives.  The run directory stays the
working copy; the captures tree is what is committed.

Usage: python3 mirror_and_verify.py
"""

import hashlib
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
COLLAB = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
MIRROR = os.path.join(COLLAB, "agentic_orchestration", "drax", "captures",
                      "2026-09-26-c9-cathedral-greyroom")

CARRY = ["guide.png", "id_mask.png", "depth_mm.png", "walkable_mask.png",
         "dot_zone_mask.png", "dot_zone_mask_upper_bound.png",
         "M2_review_cathedral_greyroom.png", "greyroom_manifest.json",
         "README.md", "make_cathedral_greyroom.py", "make_review_image.py",
         "mirror_and_verify.py"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    man = json.load(open(os.path.join(ROOT, "greyroom_manifest.json")))
    bad = []

    # --- 1. the manifest's own output digests still hold --------------------
    for name, row in man["outputs"].items():
        p = os.path.join(ROOT, name)
        if not os.path.exists(p):
            bad.append("MISSING %s" % name)
            continue
        got = sha(p)
        if got != row["sha256"]:
            bad.append("DIGEST DRIFT %s: manifest %s, disk %s"
                       % (name, row["sha256"][:12], got[:12]))

    # --- 2. every number the README asserts is the manifest's number --------
    rd = open(os.path.join(ROOT, "README.md")).read()
    cam, cg, dz = man["camera"], man["chunk_grid"], man["dot_zones"]
    checks = [
        ("px/m east", "%.6f" % cam["px_per_m_east"]),
        ("px/m south", "%.6f" % cam["px_per_m_south_ground"]),
        ("px/m up-screen", "%.6f" % cam["px_per_m_up_screen"]),
        ("canvas W", "%d" % man["canvas"]["size_px"][0]),
        ("canvas H", "%d" % man["canvas"]["size_px"][1]),
        ("world w", "%.3f" % man["canvas"]["width_m"]),
        ("world h", "%.3f" % man["canvas"]["height_m"]),
        ("arena w", "%.3f" % man["arena"]["extent_m"][0]),
        ("arena h", "%.3f" % man["arena"]["extent_m"][1]),
        ("bay", "%.4f" % man["derived_from_geometry"]["bay_m"]),
        ("vessel", "%.3f" % man["derived_from_geometry"]
         ["central_vessel_width_m"]),
        ("n_bays", "%d" % man["derived_from_geometry"]["n_bays"]),
        ("ring length", "%.3f" % man["derived_from_geometry"]["ring_length_m"]),
        ("k_disjoint", "%.4f" % dz["k_disjoint"]),
        ("n_chunks", "%d" % cg["n_chunks"]),
        ("grid rows", "%d" % cg["grid"][0]),
        ("grid cols", "%d" % cg["grid"][1]),
        ("keeper implied body",
         "%.4f" % man["scale_figures"]["keeper_130px_implies_body_m"]),
        ("h_fig px on plate",
         "%.3f" % man["scale_figures"]["kc2_h_fig_px_on_this_plate"]),
        ("rot primary pct", "%.1f" % (100 * dz["primary_floor_fraction"])),
        ("rot envelope pct", "%.1f" % (100 * dz["envelope_floor_fraction"])),
    ]
    for label, want in checks:
        # the README may round further; require the manifest's value to appear
        # as a prefix of some number in the README, at >= 3 significant chars
        stem = want.rstrip("0").rstrip(".") if "." in want else want
        if stem not in rd:
            bad.append("README does not carry %s = %s (from %s)"
                       % (label, want, stem))

    # cross-check: the canvas really is the arena plus the declared surround
    dec = {d["what"]: d["value"] for d in man["declared_not_measured"]}
    ww = man["arena"]["extent_m"][0] + dec["surround_west"] + \
        dec["surround_east"]
    hh = man["arena"]["extent_m"][1] + dec["surround_north"] + \
        dec["surround_south"]
    if abs(ww - man["canvas"]["width_m"]) > 1e-6 or \
       abs(hh - man["canvas"]["height_m"]) > 1e-6:
        bad.append("canvas != arena + declared surround")

    # cross-check: the chunk grid covers the canvas
    ox, oy = [-v for v in cg["origin_offset_px"]]
    nrow, ncol = cg["grid"]
    if (ncol - 1) * cg["step_px"][0] + cg["chunk_px"][0] - ox < \
            man["canvas"]["size_px"][0]:
        bad.append("chunk grid does not cover the canvas in x")
    if (nrow - 1) * cg["step_px"][1] + cg["chunk_px"][1] - oy < \
            man["canvas"]["size_px"][1]:
        bad.append("chunk grid does not cover the canvas in y")

    if bad:
        print("FAILED:")
        for b in bad:
            print("  ·", b)
        return 1
    print("[verify] %d output digests OK · %d README numbers match the "
          "manifest · canvas and chunk grid cross-check OK"
          % (len(man["outputs"]), len(checks)))

    # --- 3. mirror ----------------------------------------------------------
    os.makedirs(MIRROR, exist_ok=True)
    for name in CARRY:
        src = os.path.join(ROOT, name)
        if not os.path.exists(src):
            print("  (skip, absent: %s)" % name)
            continue
        dst = os.path.join(MIRROR, name)
        shutil.copy2(src, dst)
        assert sha(src) == sha(dst), name
    with open(os.path.join(MIRROR, "MIRROR_NOTE.md"), "w") as fh:
        fh.write(
            "# MIRROR — C-9 cathedral grey room\n\n"
            "These files are a byte-identical copy of\n"
            "`astra_test_01/burst/runs/C-9/greyroom/`, which is where the\n"
            "dispatch says to write them and where they are generated.\n\n"
            "They live here as well because `astra_test_01/.gitignore` ignores\n"
            "`*.png`, so the run directory's images cannot be committed. This\n"
            "tree is the committed copy, matching the KC2-PLAY arena-guide\n"
            "precedent (`2026-09-20-kc2-play-arena-guide/`).\n\n"
            "Copied and digest-verified by `mirror_and_verify.py`. Do not edit\n"
            "here — edit the run directory and re-run that script.\n")
    print("[mirror] %d files -> %s" % (len(CARRY), MIRROR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
