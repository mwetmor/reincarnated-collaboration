# Merge a PARTIAL render's raw (render_cells.gd with J1_ONLY) into a pack's raw, for a re-render of some cells only.
#
#   python3 scripts/merge_raw.py <base_raw.json> <partial_raw.json> <out_raw.json> <passes.json>
#
# passes.json = {"base": {"pass": "p1", ...meta}, "new": {"pass": "p2", ...meta}} -- meta is whatever each render's
# provenance was (body sha, kit-config sha, tool sha, ts, why). The partial's cells REPLACE the base's; every other
# cell is kept as the base rendered it. durations_s comes from the partial (the renderer writes every state's, read
# from the GLB it loaded, so it is the current one). h_model is the body at REST: if the two renders disagree the
# merge refuses, because a pack whose cells were rendered from two different rest bodies is not one pack.
# Each cell gets `render_pass`; the out raw gets `render_passes` (the indexer copies both into matrix_index.json).
import json, sys
BASE, PART, OUT, PASSES = sys.argv[1:5]
b, p, meta = json.load(open(BASE)), json.load(open(PART)), json.load(open(PASSES))
if b["h_model"] != p["h_model"]:
    raise SystemExit("h_model differs between the renders (%s vs %s): not one body at rest -- re-render the whole pack" % (b["h_model"], p["h_model"]))
out = dict(cells={}, durations_s=p["durations_s"], frames=[], h_model=p["h_model"])
for k, c in b["cells"].items():
    out["cells"][k] = dict(c, render_pass=c.get("render_pass", meta["base"]["pass"]))
for k, c in p["cells"].items():
    out["cells"][k] = dict(c, render_pass=meta["new"]["pass"])
prev = b.get("render_passes") or {meta["base"]["pass"]: meta["base"]}
out["render_passes"] = dict(prev, **{meta["new"]["pass"]: dict(meta["new"], cells=sorted(p["cells"]))})
for k in out["cells"]:
    out["frames"].extend(out["cells"][k]["t_s"])
for pn, pm in out["render_passes"].items():                         # how many cells in the pack each render still provides
    pm["cells_in_pack"] = sum(1 for c in out["cells"].values() if c["render_pass"] == pn)
json.dump(out, open(OUT, "w"), indent=1)
n = {}
for c in out["cells"].values():
    n[c["render_pass"]] = n.get(c["render_pass"], 0) + 1
print("merged %d cells: %s" % (len(out["cells"]), n))
