#!/usr/bin/env python3
"""TQIT .arz reader (READ-ONLY). Format per legolas 2026-07-23 probe §0,
same constants as research/scripts/gd_arz_adapter_2026_07_24.py."""
import struct, pathlib, lz4.block

DEPOT = pathlib.Path("/Users/admin/depots")
ARZS = {
    "database.arz":     DEPOT/"219991/24346246/database/database.arz",
    "GDX1.arz":         DEPOT/"642280/24346246/gdx1/database/GDX1.arz",
    "GDX2.arz":         DEPOT/"897670/24346246/gdx2/database/GDX2.arz",
    "GDX3.arz":         DEPOT/"2699230/24346246/gdx3/database/GDX3.arz",
    "SurvivalMode.arz": DEPOT/"483840/24346246/mods/survivalmode/database/SurvivalMode.arz",
    "SurvivalMode1.arz":DEPOT/"642281/24346246/survivalmode1/database/SurvivalMode1.arz",
    "SurvivalMode2.arz":DEPOT/"897671/24346246/survivalmode2/database/SurvivalMode2.arz",
    "SurvivalMode3.arz":DEPOT/"2699231/24346246/survivalmode3/database/SurvivalMode3.arz",
}

class Arz:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.d = self.path.read_bytes()
        magic, ver, rt_off, rt_size, rt_cnt, st_off, st_size = struct.unpack_from("<HHiiiii", self.d, 0)
        assert magic == 2, f"magic {magic}"
        self.ver = ver
        # string table
        self.strings = []
        p = st_off
        cnt = struct.unpack_from("<i", self.d, p)[0]; p += 4
        for _ in range(cnt):
            n = struct.unpack_from("<i", self.d, p)[0]; p += 4
            self.strings.append(self.d[p:p+n].decode("latin-1")); p += n
        # record table
        self.records = {}
        p = rt_off
        for _ in range(rt_cnt):
            nid = struct.unpack_from("<i", self.d, p)[0]; p += 4
            n = struct.unpack_from("<i", self.d, p)[0]; p += 4
            rtype = self.d[p:p+n].decode("latin-1"); p += n
            off, csz, dsz = struct.unpack_from("<iii", self.d, p); p += 12
            p += 8  # timestamp
            self.records[self.strings[nid]] = (rtype, off, csz, dsz)

    def get(self, name):
        if name not in self.records: return None
        rtype, off, csz, dsz = self.records[name]
        blob = self.d[24+off:24+off+csz]
        raw = lz4.block.decompress(blob, uncompressed_size=dsz)
        out = {}
        q = 0
        while q + 8 <= len(raw):
            typ, cnt, kid = struct.unpack_from("<HHI", raw, q); q += 8
            vals = []
            for i in range(cnt):
                b = raw[q:q+4]; q += 4
                if typ == 1: vals.append(struct.unpack("<f", b)[0])
                elif typ == 2: vals.append(self.strings[struct.unpack("<I", b)[0]])
                else: vals.append(struct.unpack("<i", b)[0])
            out[self.strings[kid]] = vals[0] if cnt == 1 else vals
        out["__type__"] = rtype
        return out

_cache = {}
def arz(name):
    if name not in _cache: _cache[name] = Arz(ARZS[name])
    return _cache[name]

# Expansion override precedence: LATER archives override EARLIER ones.
PRECEDENCE = ["database.arz","GDX1.arz","GDX2.arz","GDX3.arz"]

def find(rec, include_mods=False):
    """Return (archive_name, record dict) for the HIGHEST-PRECEDENCE archive
    holding rec. Expansions override base -- first-hit ordering is WRONG here
    (verified: _classtraining_class09 is a 32-rank stub in database.arz and the
    live 100-rank record in GDX2.arz)."""
    order = PRECEDENCE + (["SurvivalMode.arz","SurvivalMode1.arz","SurvivalMode2.arz","SurvivalMode3.arz"] if include_mods else [])
    hit = (None, None)
    for n in order:
        a = arz(n)
        if rec in a.records:
            hit = (n, a.get(rec))
    return hit

def find_all(rec):
    out = []
    for n in ARZS:
        a = arz(n)
        if rec in a.records:
            out.append((n, a.get(rec)))
    return out
