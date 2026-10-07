#!/usr/bin/env python3
"""P2 -- PROVENANCE AS A LINEAGE CHAIN (Gate-1 W-7): every static texture the level wears, walked back link by link
to THE ONE PAINTING's sha. A shader/layer check alone is not this row (it passes R-C9-159); this row asks where
every static texel came from.

A level is described by a LINEAGE SPEC (dict): {"painting": {path, sha?}, "textures": [node...]} where a node is
  {"id", "path", "role", "links": [link...]}   and a link proves "this file was made from that input":
     {"kind": "sha_record",   "record": <json path>, "field": <dotted field>}     the record states this file's sha
     {"kind": "bytes_equal",  "input": <path>}                                   byte-identical copy of the input
     {"kind": "pixels_equal", "input": <path>}                                   same decoded pixels (a re-encode)
     {"kind": "crop_of",      "input": <path>, "rect": [x,y,w,h], "alpha_min": a} pixels under alpha == input crop
     {"kind": "producer",     "tool": <path>, "tool_sha"?, "evidence": <str>, "input": <path>}
                                     a producing tool whose code/record names the input (cited, tool sha recorded)
     {"kind": "foreign",      "input": <path>, "evidence": <str>}               the input is NOT derived from the
                                     painting (e.g. an image generated from a model sheet); ends the chain: FAIL
A node RESOLVES when one link verifies AND that link's input resolves (or is the painting itself). The painting
resolves iff its file's sha == the level's declared painting sha. Every static texture must resolve.
PASS: 100% of nodes resolve to the one painting (plan § 4 P2: "100% from the one stitched painting").

Adapters below build the spec for v1 (positive), R-C9-159 (negative) and two constructed failures, from the records
each lane wrote -- every link cites the file it reads. A later fid level ships its own spec (fid/pt/lineage.json,
same schema) and is scored by `--spec`.
"""
import argparse
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

_SHA = {}


def fsha(p):
    p = str(p)
    if p not in _SHA:
        _SHA[p] = sha256(p)
    return _SHA[p]


def field(d, dotted):
    for k in dotted.split("."):
        d = d[k]
    return d


def check_link(node, ln):
    """-> (ok: bool, input_path or None, note)"""
    k = ln["kind"]
    if k == "sha_record":
        rec = jload(ln["record"])
        want = field(rec, ln["field"])
        ok = fsha(node["path"]) == want
        return ok, ln.get("input"), "record %s:%s %s file sha" % (pathlib.Path(ln["record"]).name, ln["field"],
                                                                   "==" if ok else "!=")
    if k == "bytes_equal":
        ok = fsha(node["path"]) == fsha(ln["input"])
        return ok, ln["input"], "bytes %s" % ("equal" if ok else "DIFFER")
    if k == "pixels_equal":
        a = np.asarray(Image.open(node["path"]).convert("RGB"))
        b = np.asarray(Image.open(ln["input"]).convert("RGB"))
        ok = a.shape == b.shape and int(np.abs(a.astype(int) - b).max()) == 0
        return ok, ln["input"], "decoded pixels %s" % ("equal" if ok else "DIFFER")
    if k == "crop_of":
        x, y, w, h = ln["rect"]
        pl = np.asarray(Image.open(node["path"]).convert("RGBA")).astype(int)
        src = np.asarray(Image.open(ln["input"]).convert("RGB").crop((x, y, x + w, y + h))).astype(int)
        m = pl[..., 3] >= ln.get("alpha_min", 255)
        d = np.abs(pl[..., :3][m] - src[m]).max() if m.any() else 999
        ok = d == 0
        return ok, ln["input"], "plate == painting crop %s (max |d| %s over %d px)" % (ln["rect"], d, int(m.sum()))
    if k == "producer":
        ok = pathlib.Path(ln["tool"]).exists() and ("tool_sha" not in ln or fsha(ln["tool"]) == ln["tool_sha"])
        return ok, ln["input"], "producer %s (%s)" % (pathlib.Path(ln["tool"]).name, ln["evidence"])
    if k == "foreign":
        return False, None, "FOREIGN input %s: %s" % (pathlib.Path(ln["input"]).name, ln["evidence"])
    raise ValueError(k)


def resolve(spec):
    paint = spec["painting"]
    psha = fsha(paint["path"])
    paint_ok = psha == paint["sha"]
    by_path = {str(n["path"]): n for n in spec["textures"]}
    memo = {}

    def res(path, depth=0):
        path = str(path)
        if path == str(paint["path"]):
            return paint_ok, ["painting sha %s %s declared %s" % (psha[:12], "==" if paint_ok else "!=", paint["sha"][:12])]
        if path in memo:
            return memo[path]
        if depth > 12:
            return False, ["chain too deep"]
        node = by_path.get(path)
        if node is None:
            # an input that is not itself a declared node: accept only if it IS the painting by sha
            ok = fsha(path) == paint["sha"]
            return ok, ["input %s sha %s the painting" % (pathlib.Path(path).name, "==" if ok else "!=")]
        trail = []
        pre_ok, chain_ok = True, False
        for ln in node["links"]:
            ok, inp, note = check_link(node, ln)
            trail.append(note)
            if inp is None and ln["kind"] != "foreign":
                pre_ok = pre_ok and ok        # a sha record with no input: a PRECONDITION (a mismatch breaks the node)
                continue
            if ok:
                ok2, t2 = res(inp, depth + 1)
                trail += ["  " + t for t in t2]
                chain_ok = chain_ok or ok2
        memo[path] = (pre_ok and chain_ok, trail)
        return memo[path]

    rows = []
    for n in spec["textures"]:
        if n.get("intermediate"):
            continue
        ok, trail = res(n["path"])
        rows.append({"id": n["id"], "role": n["role"], "resolves": ok, "trail": trail})
    nres = sum(r["resolves"] for r in rows)
    return {"value": round(nres / max(len(rows), 1), 4), "resolved": nres, "n": len(rows),
            "unresolved": [r["id"] for r in rows if not r["resolves"]],
            "pass": nres == len(rows) and paint_ok, "threshold": "100% of static textures resolve to the painting sha",
            "painting_sha": paint["sha"], "rows": rows}


# ------------------------------------------------------------------ adapters (records -> spec)
def spec_v1():
    D = BF / "godot/data/painted"
    man = jload(D / "manifest.json")
    paint = BF / "paint/barrow_full_painted.png"
    T = []
    T.append({"id": "painting.bin", "path": D / "painting.bin", "role": "ground + 29 primitives (projection)",
              "links": [{"kind": "sha_record", "record": D / "manifest.json", "field": "painting.sha256"},
                        {"kind": "bytes_equal", "input": paint}]})
    for key, role in (("ground_inpainted", "ground variant (tufts filled)"), ("lit", "painted direct-sun share")):
        T.append({"id": key, "path": D / man[key]["file"], "role": role,
                  "links": [{"kind": "sha_record", "record": D / "manifest.json", "field": key + ".sha256"},
                            {"kind": "producer", "tool": BF / "tools/paint_world_prep.py",
                             "evidence": "take/build/painted_prep.json painting_sha256 = %s" %
                                         jload(BF / "take/build/painted_prep.json")["painting_sha256"][:12],
                             "input": paint}]})
    br = jload(BF / "take/build/bake_report.json")
    plates = jload(BF / "take/plates/plates.json")["plates"]
    for k, v in br["pieces"].items():
        png = BF / v["texture"]
        pl = plates[k]
        T.append({"id": "bake " + k, "path": D / man["bakes"][k]["file"], "role": "baked hero",
                  "links": [{"kind": "sha_record", "record": D / "manifest.json", "field": "bakes.%s.sha256" % k},
                            {"kind": "bytes_equal", "input": png}]})
        T.append({"id": "work bake " + k, "path": png, "role": "bake output", "intermediate": True,
                  "links": [{"kind": "producer", "tool": BF / "tools/bake_heroes.py",
                             "evidence": "bake_heroes.py runs t5_06b_bake.py --sheet <id>:PAINT, PAINT = "
                                         "paint/barrow_full_painted.png (bake_heroes.py:28,45); record "
                                         "take/build/bake_report.json pieces.%s.texture" % k,
                             "input": BF / "take/plates" / pathlib.Path(pl["file"]).name}]})
        T.append({"id": "plate " + k, "path": BF / "take/plates" / pathlib.Path(pl["file"]).name, "role": "plate",
                  "intermediate": True,
                  "links": [{"kind": "crop_of", "input": paint, "rect": pl["rect_px"], "alpha_min": 255}]})
    return {"name": "v1", "painting": {"path": paint, "sha": jload(BF / "take/take_report.json")["painting"]["sha256"]},
            "textures": T}


def spec_159():
    D = BF / "godot/data/barrow_v2_sw"
    seams = jload(B2 / "paint/v1cam/seams.json")
    ground = D / "painted/ground.png"
    T = [{"id": "ground.png", "path": ground, "role": "ground (projection)",
          "links": [{"kind": "sha_record", "record": B2 / "paint/v1cam/seams.json", "field": "sha256"}]},
         {"id": "lit.png", "path": D / "painted/lit.png", "role": "direct-sun share",
          "links": [{"kind": "producer", "tool": B2 / "tools/v2sw_prep.py",
                     "evidence": "a render of the section (v2_mode lit), not derived from the painting's pixels "
                                 "(barrow_v2_sw.gd v2_mode 'lit'); accepted as light data", "input": ground}]}]
    bk = jload(D / "bakes/bakes.json")
    for key, png in bk.items():
        name = pathlib.Path(png).stem
        cell = BF / ("work/_cells_v2sw_%s/painted_1536.png" % name)
        sheet = ART / ("BV2L-m-%s/BV2L-m-%s.png" % (name, name))
        T.append({"id": "bake " + name, "path": D / "bakes" / png, "role": "model bake (one per GLB, all instances)",
                  "links": [{"kind": "producer", "tool": B2 / "tools/v2sw_model_bake.py",
                             "evidence": "v2sw_model_bake.py bake(): t5_06b_bake.py --sheet v2sw_<name>:"
                                         "_cells_v2sw_<name>/painted_1536.png (v2sw_model_bake.py:183-194)",
                             "input": cell}]})
        T.append({"id": "cell " + name, "path": cell, "role": "painted sheet copy", "intermediate": True,
                  "links": [{"kind": "pixels_equal", "input": sheet}]})
        T.append({"id": "sheet " + name, "path": sheet, "role": "4-view model sheet", "intermediate": True,
                  "links": [{"kind": "foreign", "input": sheet,
                             "evidence": "artifacts/BV2L-m-%s/receipt.json: an Astra paint-over of FOUR VIEWS OF THE "
                                         "MODEL ALONE (v2sw_model_bake.py views), a separate painting -- no pixel of "
                                         "it comes from the ground painting" % name}]})
    # v1's own kit bakes, worn by barrow_v2_sw's kit instances (barrow_v2_sw.gd:528 V1_BAKES)
    v1man = jload(BF / "godot/data/painted/manifest.json")
    for glb, b in (("cairn", "cairn_1"), ("log", "fallen_tree_log_A"), ("stone_tall", "ring_m55"), ("stone_mid", "ring_m135")):
        T.append({"id": "v1 bake %s on %s" % (b, glb), "path": BF / ("godot/data/painted/bakes/%s.bin" % b),
                  "role": "v1 kit bake reused",
                  "links": [{"kind": "foreign", "input": BF / "paint/barrow_full_painted.png",
                             "evidence": "baked from v1's painting (sha eecb4266...) at v1's placement, not from this "
                                         "level's painting (sha %s...): a second painting" % seams["sha256"][:8]}]})
    return {"name": "159", "painting": {"path": ground, "sha": seams["sha256"]}, "textures": T}


def spec_158():
    P = B2 / "paint/section_sw/section_sw_painted.png"
    seams = jload(B2 / "paint/section_sw/seams.json")
    return {"name": "158", "painting": {"path": P, "sha": seams["sha256"]},
            "textures": [{"id": "section_sw_painted.png (projection, every static)", "path": P, "role": "all statics",
                          "links": [{"kind": "sha_record", "record": B2 / "paint/section_sw/seams.json", "field": "sha256"}]}]}


def spec_constructed_swap():
    """v1 with ONE bake file replaced by a different texture (159's crag bake): the manifest sha no longer matches."""
    s = spec_v1()
    for n in s["textures"]:
        if n["id"] == "bake ring_m95":
            n["path"] = BF / "godot/data/barrow_v2_sw/bakes/crag.png"
    s["name"] = "constructed: v1, bake ring_m95 swapped for a foreign texture"
    return s


def spec_constructed_foreign():
    """v1 with ONE bake declared (honestly) as produced from a separately painted model sheet."""
    s = spec_v1()
    for n in s["textures"]:
        if n["id"] == "work bake ring_m95":
            n["links"] = [{"kind": "foreign", "input": ART / "BV2L-m-crag/BV2L-m-crag.png",
                           "evidence": "constructed: a per-model sheet painting"}]
    s["name"] = "constructed: v1, one bake from a per-model sheet"
    return s


SETS = {"v1": spec_v1, "159": spec_159, "158": spec_158, "constructed": spec_constructed_swap,
        "constructed_foreign": spec_constructed_foreign}


def _jsonable(spec_res):
    return json.loads(json.dumps(spec_res, default=str))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="all")
    ap.add_argument("--spec", help="a lineage spec JSON (schema above) for a new level")
    a = ap.parse_args()
    if a.spec:
        sp = jload(a.spec)
        r = resolve(sp)
        print("P2 %s resolved %d/%d -> %s" % (a.spec, r["resolved"], r["n"], "PASS" if r["pass"] else "FAIL"))
        sys.exit(0 if r["pass"] else 1)
    res = {}
    for k, f in SETS.items():
        if a.set not in ("all", k):
            continue
        r = resolve(f())
        res[k] = _jsonable(r)
        print("P2 %-20s resolved %2d/%2d (%.0f%%)  -> %s   unresolved: %s" % (
            k, r["resolved"], r["n"], 100 * r["value"], "PASS" if r["pass"] else "FAIL", ", ".join(r["unresolved"][:6])))
    dump(res, str(PH / "results/p2.json"))
