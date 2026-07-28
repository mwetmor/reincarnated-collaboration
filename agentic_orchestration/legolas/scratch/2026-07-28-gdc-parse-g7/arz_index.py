#!/usr/bin/env python3
"""SCRATCH (G-7) — enumerate .arz record names (the adapter exposes read_record only)."""
import pathlib
import struct
import sys

import lz4.block


class Arz:
    def __init__(self, path):
        self.d = pathlib.Path(path).read_bytes()
        d = self.d
        (magic, ver, rt_off, rt_size, rt_count, st_off, st_size) = struct.unpack_from("<HHiiiii", d, 0)
        assert magic == 2, magic
        # string table
        self.strings = []
        o = st_off
        (count,) = struct.unpack_from("<i", d, o)
        o += 4
        for _ in range(count):
            (n,) = struct.unpack_from("<i", d, o)
            o += 4
            self.strings.append(d[o:o + n].decode("latin-1"))
            o += n
        self.recs = {}
        o = rt_off
        for _ in range(rt_count):
            (name_id,) = struct.unpack_from("<i", d, o)
            o += 4
            (tl,) = struct.unpack_from("<i", d, o)
            o += 4
            rtype = d[o:o + tl].decode("latin-1")
            o += tl
            doff, csize, dsize = struct.unpack_from("<3i", d, o)
            o += 12
            o += 8  # timestamp
            self.recs[self.strings[name_id]] = (rtype, doff, csize, dsize)

    def fields(self, name):
        rtype, doff, csize, dsize = self.recs[name]
        blob = lz4.block.decompress(self.d[24 + doff:24 + doff + csize], uncompressed_size=dsize)
        out = {}
        o = 0
        while o < len(blob):
            typ, cnt, key = struct.unpack_from("<HHI", blob, o)
            o += 8
            vals = []
            for i in range(cnt):
                raw = blob[o:o + 4]
                o += 4
                if typ == 1:
                    vals.append(struct.unpack("<f", raw)[0])
                elif typ == 2:
                    vals.append(self.strings[struct.unpack("<I", raw)[0]])
                else:
                    vals.append(struct.unpack("<i", raw)[0])
            out[self.strings[key]] = vals[0] if cnt == 1 else vals
        return rtype, out


if __name__ == "__main__":
    a = Arz(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "--grep":
        pat = sys.argv[3].lower()
        for n in sorted(a.recs):
            if pat in n.lower():
                print(n, a.recs[n][0])
    elif len(sys.argv) > 2:
        rtype, f = a.fields(sys.argv[2])
        print("recordType:", rtype)
        for k in sorted(f):
            print(f"  {k} = {str(f[k])[:300]}")
    else:
        print(len(a.recs), "records")
