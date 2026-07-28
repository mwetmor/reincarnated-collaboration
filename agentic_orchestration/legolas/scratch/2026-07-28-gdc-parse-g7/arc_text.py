#!/usr/bin/env python3
"""SCRATCH — minimal Grim Dawn .arc reader, for the tag -> display-name bridge.

First time this project has parsed .arc. The 2026-07-24 GD-SLICE adapter left
localization explicitly out of scope ("skillBitmapName workaround, .arc tag-bridge
flagged pending"); this closes that gap for the G-7 gear join.

ARC v3 layout, confirmed against the shipped file's own size arithmetic:
    header 28B: magic 'ARC\\0' | version=3 | nFileEntries | nDataRecords
                | recordTableSize | stringTableSize | recordTableOffset
    [recordTableOffset                                     ) record table, 12B x nDataRecords
                                                             (partOffset, compSize, decompSize)
    [+recordTableSize                                      ) string table, concatenated names
    [+stringTableSize                                      ) file entries, 44B x nFileEntries
Payload parts are LZ4 BLOCK compressed; a part with compSize == decompSize is stored raw.
"""
import pathlib
import struct
import sys

import lz4.block


def read_arc(path):
    d = pathlib.Path(path).read_bytes()
    magic, ver, n_files, n_recs, rt_size, st_size, rt_off = struct.unpack_from("<7I", d, 0)
    if d[:4] != b"ARC\0" or ver != 3:
        raise ValueError(f"not an ARC v3 file: {d[:4]!r} v{ver}")
    recs = [struct.unpack_from("<3I", d, rt_off + 12 * i) for i in range(n_recs)]
    st_off = rt_off + rt_size
    strings = d[st_off:st_off + st_size]
    fe_off = st_off + st_size
    out = {}
    for i in range(n_files):
        (etype, foff, csize, dsize, dhash, ftime, parts, first,
         slen, soff) = struct.unpack_from("<5IQ4I", d, fe_off + 44 * i)
        name = strings[soff:soff + slen].decode("latin-1")
        buf = bytearray()
        if parts == 0:
            buf += d[foff:foff + dsize]
        else:
            for p in range(first, first + parts):
                po, pc, pd = recs[p]
                blob = d[po:po + pc]
                buf += blob if pc == pd else lz4.block.decompress(blob, uncompressed_size=pd)
        if len(buf) != dsize:
            raise ValueError(f"{name}: got {len(buf)} bytes, header says {dsize}")
        out[name] = bytes(buf)
    return out


def load_tags(paths):
    """Merge every tag=value pair from a list of .arc files. Later files win,
    which matches GD's expansion-override precedence."""
    tags = {}
    for p in paths:
        for name, blob in read_arc(p).items():
            text = blob.decode("utf-16-le") if blob[:2] == b"\xff\xfe" else blob.decode("utf-8", "replace")
            for line in text.splitlines():
                if "=" in line and not line.startswith("//"):
                    k, _, v = line.partition("=")
                    tags[k.strip()] = v.strip()
    return tags


if __name__ == "__main__":
    files = read_arc(sys.argv[1])
    for name, blob in files.items():
        print(f"{name:<40} {len(blob):>8} bytes  head={blob[:40]!r}")
