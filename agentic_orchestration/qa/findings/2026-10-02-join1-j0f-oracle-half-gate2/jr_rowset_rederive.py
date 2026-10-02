"""jack-ryan, J0-F Gate-2: INDEPENDENT re-derivation of the 7 grain ROWSETs from the stored grain files.

Written from the manifest's printed `rowset_law` text alone; imports nothing from the emitter.
Also: FILE digests, row counts, key uniqueness, per-cell row counts, WARN-1 population figures,
G4 halted / beyond totals, the trajectory-collapse census, and an inertness cross-check of the
fixture against a second fixture directory (if given).

usage: python3 jr_rowset_rederive.py <fixture_dir> [<second_fixture_dir>]
"""
import gzip, hashlib, json, struct, sys, pathlib, collections

d = pathlib.Path(sys.argv[1])
m = json.loads((d / "manifest.json").read_text())
SCHEMA = m["schema"]


def canon(v):
    if v is None or isinstance(v, (bool, str)):
        return v
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return "f64:" + struct.pack(">d", v).hex()
    if isinstance(v, list):
        return [canon(x) for x in v]
    raise TypeError(type(v))


def load(g):
    p = d / m["grains"][g]["file"]
    raw = p.read_bytes()
    fsha = hashlib.sha256(raw).hexdigest()
    body = gzip.decompress(raw) if p.suffix == ".gz" else raw
    rows = [json.loads(x) for x in body.decode("utf-8").splitlines() if x]
    return rows, fsha


out = {}
cache = {}
for g, sc in SCHEMA.items():
    rows, fsha = load(g)
    names = sc["key"] + sc["fields"]
    for r in rows:
        assert list(r.keys()) == names, (g, list(r.keys()))
    keyed = sorted(rows, key=lambda r: tuple(r[k] for k in sc["key"]))
    keys = [tuple(r[k] for k in sc["key"]) for r in keyed]
    assert len(set(keys)) == len(keys), f"{g}: duplicate keys"
    canon_txt = "\n".join(json.dumps(canon([r[n] for n in names]), ensure_ascii=False,
                                     separators=(",", ":")) for r in keyed)
    rs = hashlib.sha256(canon_txt.encode("utf-8")).hexdigest()
    per_cell = collections.Counter((r["arm"], r["salt"]) for r in rows)
    out[g] = {"rows": len(rows), "rowset_rederived": rs, "rowset_manifest": m["grains"][g]["rowset_sha256"],
              "rowset_equal": rs == m["grains"][g]["rowset_sha256"],
              "file_rederived": fsha, "file_equal": fsha == m["grains"][g]["file_sha256"],
              "n_cells_with_rows": len(per_cell)}
    cache[g] = rows

# WARN-1 population
G1 = cache["G1"]
pu = [r["pth_used"] for r in G1]
out["warn1"] = {"n": len(G1), "min_pth_used": min(pu), "min_pth_raw": min(r["pth_raw"] for r in G1 if r["pth_raw"] is not None),
                "n_used_lt70": sum(x < 70 for x in pu), "n_used_lt55": sum(x < 55 for x in pu),
                "n_eff_ne_used": sum(r["pth_effective"] != r["pth_used"] for r in G1),
                "pth_used_quantiles": sorted(pu)[:5]}
# G4 totals
G4 = cache["G4"]
out["g4"] = {"sum_halted": sum(r["n_bodies_halted"] for r in G4),
             "sum_beyond": sum(r["n_bodies_halted_beyond_d_engage"] for r in G4),
             "n_max_halt_nonnull": sum(r["max_halt_distance_m"] is not None for r in G4)}
# trajectory collapse: per-cell digest over all grains' rows with the arm column blanked
cell_rows = collections.defaultdict(list)
for g in SCHEMA:
    for r in cache[g]:
        rr = dict(r); a = rr.pop("arm")
        cell_rows[(a, r["salt"])].append(g + json.dumps(canon(list(rr.values())), separators=(",", ":")))
dig = {k: hashlib.sha256("\n".join(sorted(v)).encode()).hexdigest()[:16] for k, v in cell_rows.items()}
classes = collections.defaultdict(list)
for k, v in sorted(dig.items()):
    classes[v].append(f"{k[0]}|{k[1]}")
out["trajectory_classes"] = {"n_distinct": len(classes), "classes": sorted(classes.values())}

if len(sys.argv) > 2:
    d2 = pathlib.Path(sys.argv[2]); m2 = json.loads((d2 / "manifest.json").read_text())
    out["second"] = {g: {"rowset_equal": m2["grains"][g]["rowset_sha256"] == m["grains"][g]["rowset_sha256"],
                         "file_equal": m2["grains"][g]["file_sha256"] == m["grains"][g]["file_sha256"]}
                     for g in SCHEMA}
    inert = m2.get("inertness_bare_vs_hooked") or {}
    out["second_inertness"] = f"{sum(v['equal'] for v in inert.values())}/{len(inert)}"
    out["second_obs1"] = f"{m2['obs1_completeness']['n_complete']}/{m2['obs1_completeness']['n_cells']}"
print(json.dumps(out, indent=1))
