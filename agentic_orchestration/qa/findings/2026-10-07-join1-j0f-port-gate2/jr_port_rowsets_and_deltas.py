"""jack-ryan, J0-F PORT-HALF Gate-2: independent ROWSET re-derivation + row-level cross-side diffs.

Written from the manifests' printed `rowset_law` text; imports nothing from drax's emitter or diff tool.

For each fixture directory given (port re-frozen, port r2, oracle, my own re-emission ...):
  * the 7 ROWSETs re-derived (f64 -> 'f64:'+big-endian hex, KEY-sorted, ',' ':' separators, no trailing newline),
    compared with that directory's manifest; FILE digests; row counts; key uniqueness.
Then, row-level, keyed by the grain KEY:
  * A vs B for each named pair: rows only-in-A / only-in-B / differing, by grain; for G2/G3 the differing rows
    are bucketed by WAVE (G2 tick -> wave via G7's [wave_start_tick, wave_end_tick] for that (arm, salt)),
    by family, by differing field, and pre_mitigation's ulp distance.

usage: python3 jr_port_rowsets_and_deltas.py <out.json> NAME=<dir>[:<manifest file>] ... -- PAIR=A,B ...
"""
import collections, gzip, hashlib, json, pathlib, struct, sys

args = sys.argv[2:]
out_path = sys.argv[1]
dirs, pairs = {}, []
for a in args:
    k, v = a.split("=", 1)
    if k == "PAIR":
        pairs.append(tuple(v.split(",")))
    else:
        p, _, mf = v.partition(":")
        dirs[k] = (pathlib.Path(p), mf or None)


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


def ulps(a, b):
    ia = struct.unpack(">q", struct.pack(">d", a))[0]
    ib = struct.unpack(">q", struct.pack(">d", b))[0]
    return ib - ia


def manifest_of(d, mf):
    for name in ([mf] if mf else ["manifest-port.json", "manifest.json"]):
        if name and (d / name).exists():
            return name, json.loads((d / name).read_text())
    raise FileNotFoundError(d)


DATA, OUT = {}, {"fixtures": {}, "pairs": {}}
for name, (d, mf) in dirs.items():
    mname, m = manifest_of(d, mf)
    SC = m["schema"]
    res, data = {}, {}
    for g, sc in SC.items():
        gm = m["grains"][g]
        raw = (d / gm["file"]).read_bytes()
        body = gzip.decompress(raw) if gm["file"].endswith(".gz") else raw
        names = sc["key"] + sc["fields"]
        rows = [json.loads(x) for x in body.decode("utf-8").splitlines() if x]
        for r in rows:
            assert set(r) == set(names), (name, g, sorted(r))
        keyed = sorted(rows, key=lambda r: tuple(r[k] for k in sc["key"]))
        keys = [tuple(r[k] for k in sc["key"]) for r in keyed]
        assert len(set(keys)) == len(keys), (name, g, "duplicate keys")
        txt = "\n".join(json.dumps(canon([r[n] for n in names]), ensure_ascii=False, separators=(",", ":"))
                        for r in keyed)
        rs = hashlib.sha256(txt.encode("utf-8")).hexdigest()
        res[g] = {"rows": len(rows), "rowset_rederived": rs, "rowset_manifest": gm["rowset_sha256"],
                  "rowset_equal": rs == gm["rowset_sha256"],
                  "file_equal": hashlib.sha256(raw).hexdigest() == gm["file_sha256"],
                  "n_cells": len({(r["arm"], r["salt"]) for r in rows})}
        data[g] = {k: r for k, r in zip(keys, keyed)}
    DATA[name] = (SC, data)
    OUT["fixtures"][name] = {"dir": str(d), "manifest": mname,
                             "manifest_sha256": hashlib.sha256((d / mname).read_bytes()).hexdigest(),
                             "grains": res, "all_rowsets_equal_manifest": all(v["rowset_equal"] for v in res.values())}


def wave_of(g7, arm, salt, tick):
    for (a, s, w), r in g7.items():
        if a == arm and s == salt and r["wave_start_tick"] <= tick <= r["wave_end_tick"]:
            return w
    return None


for A, B in pairs:
    SC, da = DATA[A]
    _, db = DATA[B]
    g7 = da["G7"]
    pr = {}
    for g in SC:
        ka, kb = set(da[g]), set(db[g])
        diff = [k for k in sorted(ka & kb) if da[g][k] != db[g][k]]
        ent = {"only_in_A": len(ka - kb), "only_in_B": len(kb - ka), "differing": len(diff)}
        if diff and g in ("G2", "G3"):
            by_wave, by_fam, by_field, ul = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
            cells = collections.Counter()
            for k in diff:
                ra, rb = da[g][k], db[g][k]
                cells[(ra["arm"], ra["salt"])] += 1
                w = ra["wave"] if g == "G3" else wave_of(g7, ra["arm"], ra["salt"], ra["tick"])
                by_wave[w] += 1
                if g == "G2":
                    by_fam[ra["family"]] += 1
                    if ra["pre_mitigation"] != rb["pre_mitigation"]:
                        ul[ulps(ra["pre_mitigation"], rb["pre_mitigation"])] += 1
                for f in SC[g]["fields"]:
                    if ra[f] != rb[f]:
                        by_field[f] += 1
            first = min(diff)
            ent.update({"by_wave": dict(sorted((str(k), v) for k, v in by_wave.items())),
                        "by_family": dict(by_fam), "by_field": dict(by_field),
                        "pre_mitigation_ulps_B_minus_A": {str(k): v for k, v in sorted(ul.items())},
                        "n_cells": len(cells), "first_key": list(first),
                        "first_A": da[g][first], "first_B": db[g][first]})
        pr[g] = ent
    OUT["pairs"]["%s_vs_%s" % (A, B)] = {"grains": pr, "all_equal": all(
        v["only_in_A"] == 0 and v["only_in_B"] == 0 and v["differing"] == 0 for v in pr.values())}

json.dump(OUT, open(out_path, "w"), indent=1, sort_keys=True, default=str)
for n, f in OUT["fixtures"].items():
    print(n, "rowsets==manifest:", f["all_rowsets_equal_manifest"],
          {g: (v["rows"], v["rowset_rederived"][:8], v["file_equal"]) for g, v in f["grains"].items()})
for n, p in OUT["pairs"].items():
    print(n, "ALL EQUAL" if p["all_equal"] else {g: {k: v[k] for k in ("only_in_A", "only_in_B", "differing", "by_wave") if k in v}
                                              for g, v in p["grains"].items() if v["differing"] or v["only_in_A"] or v["only_in_B"]})
