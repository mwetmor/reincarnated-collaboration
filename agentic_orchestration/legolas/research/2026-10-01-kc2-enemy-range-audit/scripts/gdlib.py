"""READ-ONLY GD .arz reader over the Edition IV / II vendor trees (TQIT magic=2, LZ4 block)."""
import struct, pathlib, lz4.block, hashlib
ROOTS = {"IV": pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929"),
         "II": pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")}
REL = [("base","database/database.arz"),("gdx1","gdx1/database/GDX1.arz"),("gdx2","gdx2/database/GDX2.arz"),
       ("gdx3","gdx3/database/GDX3.arz"),("sm_mod","mods/survivalmode/database/SurvivalMode.arz"),
       ("sm1","survivalmode1/database/SurvivalMode1.arz"),("sm2","survivalmode2/database/SurvivalMode2.arz"),
       ("sm3","survivalmode3/database/SurvivalMode3.arz")]
class Arz:
    def __init__(self, path):
        self.path = pathlib.Path(path); d = self.d = self.path.read_bytes()
        magic, ver, rt_off, rt_size, rt_cnt, st_off, st_size = struct.unpack_from("<HHiiiii", d, 0)
        assert magic == 2
        self.strings = []; p = st_off
        cnt = struct.unpack_from("<i", d, p)[0]; p += 4
        for _ in range(cnt):
            n = struct.unpack_from("<i", d, p)[0]; p += 4
            self.strings.append(d[p:p+n].decode("latin-1")); p += n
        self.records = {}; p = rt_off
        for _ in range(rt_cnt):
            nid = struct.unpack_from("<i", d, p)[0]; p += 4
            n = struct.unpack_from("<i", d, p)[0]; p += 4
            rtype = d[p:p+n].decode("latin-1"); p += n
            off, csz, dsz = struct.unpack_from("<iii", d, p); p += 20
            self.records[self.strings[nid].lower().replace("\\","/")] = (rtype, off, csz, dsz)
    def get(self, name):
        name = name.lower().replace("\\","/")
        if name not in self.records: return None
        rtype, off, csz, dsz = self.records[name]
        raw = lz4.block.decompress(self.d[24+off:24+off+csz], uncompressed_size=dsz)
        out = {}; q = 0
        while q + 8 <= len(raw):
            typ, cnt, kid = struct.unpack_from("<HHI", raw, q); q += 8
            vals = []
            for i in range(cnt):
                b = raw[q:q+4]; q += 4
                if typ == 1: vals.append(struct.unpack("<f", b)[0])
                elif typ == 2: vals.append(self.strings[struct.unpack("<I", b)[0]])
                else: vals.append(struct.unpack("<i", b)[0])
            out[self.strings[kid]] = vals[0] if cnt == 1 else vals
        return out
class Edition:
    def __init__(self, ed):
        self.ed = ed; self.arcs = []
        for k, r in REL:
            p = ROOTS[ed] / r
            if p.exists(): self.arcs.append((k, Arz(p)))
    def holders(self, rec):
        rec = rec.lower().replace("\\","/")
        return [k for k, a in self.arcs if rec in a.records]
    def winner(self, rec):
        """CRUCIBLE precedence: whole record from the LAST archive in REL order that carries it."""
        rec = rec.lower().replace("\\","/"); hit = (None, None)
        for k, a in self.arcs:
            if rec in a.records: hit = (k, a.get(rec))
        return hit
    def merged(self, rec):
        out = {}; hs = []
        for k, a in self.arcs:
            r = a.get(rec)
            if r is not None: out.update(r); hs.append(k)
        return (out if hs else None), hs
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
