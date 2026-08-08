#!/usr/bin/env python3
"""F-12a — decode the .map placement section.

Layout SOLVED empirically on survivalworld_a (stride measured from the spacing of plausible
position triples; index field identified by range-validity):

    [u32 count]  then count x 56-byte records:
        +0   9 x f32   orientation basis (identity on most placements)
        +36  3 x f32   world position (x, y, z)   -- METRES (Crate: 'meters per second' unit decl)
        +48  u32       flag (0 on every record observed)
        +52  u32       index into the preceding contiguous DBR string table

Accepted only when EVERY index in the section is a valid table index. READ-ONLY."""
import pathlib, struct, re, csv, math, collections

DBR = re.compile(rb"records/[a-z0-9_/&'\. \-]+?\.dbr")
STRIDE, POS_OFF, IDX_OFF = 56, 36, 52

def u32(b, o): return struct.unpack_from("<I", b, o)[0]
def f32(b, o): return struct.unpack_from("<f", b, o)[0]

def string_table(b):
    starts = []
    for m in DBR.finditer(b):
        s = m.start()
        if s >= 4 and u32(b, s - 4) == m.end() - s: starts.append(s - 4)
    runs, cur = [], [starts[0]]
    for prev, nxt in zip(starts, starts[1:]):
        if prev + 4 + u32(b, prev) == nxt: cur.append(nxt)
        else: runs.append(cur); cur = [nxt]
    runs.append(cur)
    T = max(runs, key=len)
    tbl = [b[o + 4:o + 4 + u32(b, o)].decode("ascii", "replace") for o in T]
    return tbl, T[-1] + 4 + u32(b, T[-1])

def walk(b, start, count, n):
    """[36 rot][12 pos][u32 kind] then kind==0 -> [u32 table_index]; kind==1 -> [16B uid]."""
    out, o = [], start
    for _ in range(count):
        if o + 68 > len(b): return None
        pos = (f32(b, o + 36), f32(b, o + 40), f32(b, o + 44))
        kind = u32(b, o + 48)
        if kind == 0:
            i = u32(b, o + 52)
            if i >= n: return None
            out.append((i, pos)); o += 56
        elif kind == 1:
            out.append((None, pos)); o += 64        # 48 + 4 + 16 uid... resolved below
        else:
            return None
    return out, o

def solve(b, tend, n):
    for cnt_off in range(0, 24, 2):
        count = u32(b, tend + cnt_off)
        if not (0 < count < 20000): continue
        for start in range(tend + cnt_off + 4, tend + cnt_off + 4 + 64):
            for uid_len in (16, 20):
                o, res, ok = start, [], True
                for _ in range(count):
                    if o + 68 > len(b): ok = False; break
                    pos = (f32(b, o + 36), f32(b, o + 40), f32(b, o + 44))
                    kind = u32(b, o + 48)
                    if kind == 0:
                        i = u32(b, o + 52)
                        if i >= n: ok = False; break
                        res.append((i, pos)); o += 56
                    elif kind == 1:
                        res.append((None, pos)); o += 48 + 4 + uid_len
                    else:
                        ok = False; break
                if ok and len(res) == count:
                    return count, start, res, uid_len
    return None, None, None, None

rows = []
for p in sorted(pathlib.Path("maps").rglob("*.map")):
    b = p.read_bytes()
    tbl, tend = string_table(b)
    count, start, res, uidlen = solve(b, tend, len(tbl))
    if count is None:
        print(f"{str(p):34s} table n={len(tbl):4d}  NOT SOLVED"); continue
    nctl = sum(1 for i, _ in res if i is None)
    print(f"{str(p):34s} table n={len(tbl):4d}  placements={count:5d} "
          f"(dbr {count-nctl} / control-object {nctl})  start=0x{start:08x} uid={uidlen}  SOLVED")
    for k, (i, (x, y, z)) in enumerate(res):
        rows.append(dict(arena_map=p.name, arena_archive=p.parent.name, placement=k,
                         table_index=("" if i is None else i),
                         record=("<control-object (patrol point)>" if i is None else tbl[i]),
                         x=round(x, 4), y=round(y, 4), z=round(z, 4)))

KEEP = re.compile(r"spawnpoint|playerspawn|defensepoint|trappoint|spawnbeacon|patrolpoint|"
                  r"rewardchest|bonuschest|survival", re.I)
sel = [r for r in rows if KEEP.search(r["record"])]
with open("kc2_crucible_arena_placements.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(sel)
print(f"\n[wrote] kc2_crucible_arena_placements.csv  {len(sel)} fixture rows "
      f"(of {len(rows)} total placements across {len({r['arena_map'] for r in rows})} maps)")

EM = re.compile(r"spawnpoint0[2-6]\.dbr$|tier\d\dspawnpoint01\.dbr$")
print("\n=== per-arena Crucible emitter geometry (relative to the player spawn) ===")
by = collections.defaultdict(list)
for r in sel: by[(r["arena_archive"], r["arena_map"])].append(r)
geo = []
for k in sorted(by):
    rs = by[k]
    pl = [r for r in rs if r["record"].endswith("playerspawnpoint.dbr")]
    em = [r for r in rs if EM.search(r["record"])]
    if not pl or not em: print(f"  {k}: player={len(pl)} emitters={len(em)} -- skipped"); continue
    px, py, pz = pl[0]["x"], pl[0]["y"], pl[0]["z"]
    print(f"\n--- {k[0]}/{k[1]}   player spawn ({px:.2f}, {py:.2f}, {pz:.2f}) ---")
    uniq = {}
    for r in em:
        nm = r["record"].split("/")[-1].replace(".dbr", "")
        d = math.hypot(r["x"] - px, r["z"] - pz)
        brg = (math.degrees(math.atan2(r["x"] - px, r["z"] - pz)) + 360) % 360
        oc = (brg / 30) % 12
        uniq.setdefault((round(r["x"], 2), round(r["z"], 2)), []).append((nm, d, brg, oc))
    for (x, z), lst in sorted(uniq.items(), key=lambda kv: kv[1][0][1]):
        nm, d, brg, oc = lst[0]
        alias = "" if len(lst) == 1 else f"   [+{len(lst)-1} co-located: {','.join(a[0] for a in lst[1:])[:60]}]"
        print(f"    {nm:24s} ({x:8.2f},{z:8.2f})  r={d:7.2f} m  {brg:6.1f}deg = "
              f"{oc if oc else 12:4.1f} o'clock{alias}")
        geo.append(dict(arena_archive=k[0], arena_map=k[1], emitter=nm, x=x, z=z,
                        player_x=px, player_z=pz, radius_m=round(d, 3),
                        bearing_deg=round(brg, 2), oclock=round(oc if oc else 12, 2),
                        co_located_with=",".join(a[0] for a in lst[1:])))
    ds = [v[0][1] for v in uniq.values()]
    print(f"    -> distinct emitter sites={len(uniq)}  radius min={min(ds):.2f} "
          f"mean={sum(ds)/len(ds):.2f} max={max(ds):.2f} m")
if geo:
    with open("kc2_crucible_emitter_geometry.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(geo[0])); w.writeheader(); w.writerows(geo)
    print(f"\n[wrote] kc2_crucible_emitter_geometry.csv  {len(geo)} rows")
