#!/usr/bin/env python3
"""
dump_block.py — READ-ONLY structural probe for a single .gdc block.

Why this works: the XOR key advances by folding table[b] for EVERY raw byte
consumed by a key-advancing read, in order. That fold is identical whether the
bytes were consumed as one int or as four bytes. So the key STATE at every
offset inside a block is computable from the block start alone, even when the
block's field layout has drifted past the community reference.

Two plaintext views are therefore available at every offset:
  byte view : raw[i]              ^ (key_i & 0xFF)   -- correct for string chars
  int  view : u32(raw[i:i+4])     ^  key_i           -- correct for int fields

Strings surface as ASCII runs in the byte view; that is enough to recover the
real layout by inspection instead of by guessing.

NO WRITE PATH.
"""

import struct
import sys

import gdc_read


def key_stream(data, start, key, length):
    """Return (keys, bytev) for `length` bytes from `start`, given key at start."""
    r = gdc_read.Reader(data)
    k = key
    keys = []
    bytev = bytearray()
    for i in range(length):
        b = data[start + i]
        keys.append(k)
        bytev.append(b ^ (k & 0xFF))
        k ^= r.table[b]
    return keys, bytes(bytev)


def block_views(path, block_id, block_name):
    import decode_hotbar as D
    data, r, hdr, index = D.header_and_index(path)
    info = index[block_name]
    b = r.seek_block(info["start"], block_id, block_name)
    body_start = r.p
    body_len = b["end"] - body_start
    keys, bytev = key_stream(data, body_start, r.key, body_len)
    ints = []
    for i in range(body_len - 3):
        ints.append(struct.unpack_from("<I", data, body_start + i)[0] ^ keys[i])
    return data, hdr, index, body_start, body_len, bytev, ints


def ascii_runs(bytev, minlen=4):
    runs = []
    cur = []
    for i, c in enumerate(bytev):
        if 32 <= c < 127:
            cur.append(c)
        else:
            if len(cur) >= minlen:
                runs.append((i - len(cur), bytes(cur).decode("ascii")))
            cur = []
    if len(cur) >= minlen:
        runs.append((len(bytev) - len(cur), bytes(cur).decode("ascii")))
    return runs


if __name__ == "__main__":
    path, bid, bname = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    _, hdr, _, bs, bl, bytev, ints = block_views(path, bid, bname)
    print("# %s  body_start=%d  body_len=%d" % (bname, bs, bl))
    for off, s in ascii_runs(bytev):
        # a length-prefixed string has its u32 length at off-4
        pre = ints[off - 4] if off >= 4 else None
        print("%6d  len_prefix=%-6s  %r" % (off, pre, s))
