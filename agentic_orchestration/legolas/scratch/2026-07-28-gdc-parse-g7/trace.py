#!/usr/bin/env python3
"""SCRATCH — byte-wise decrypt trace to reverse the drifted inventory v11 layout.

Valid only until the first nested block (whose length/sentinel words are read
via the non-advancing next_int primitive and would desync a byte-wise walk).
"""
import struct
import sys

from gdc_parse import Reader, MAGIC


def prime(path):
    r = Reader(open(path, "rb").read())
    r.read_key()
    r.read_int()  # magic
    r.read_int()
    r.read_wstring(); r.read_byte(); r.read_string(); r.read_int(); r.read_byte()
    r.read_byte(); r.next_int(); r.read_int()
    for _ in range(16):
        r.read_byte()
    # character_info
    bid, blen, end = r.block_start()
    while r.p < end:
        r.read_byte()
    r.next_int()
    # character_bio
    bid, blen, end = r.block_start()
    while r.p < end:
        r.read_byte()
    r.next_int()
    return r


if __name__ == "__main__":
    r = prime(sys.argv[1])
    bid, blen, end = r.block_start()
    print(f"inventory block id={bid} len={blen} start=0x{r.p:x} end=0x{end:x}")
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 260
    plain = bytearray()
    base = r.p
    for _ in range(n):
        plain.append(r.read_byte())
    for off in range(0, len(plain), 16):
        chunk = plain[off:off + 16]
        hexs = " ".join(f"{b:02x}" for b in chunk)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        ints = ""
        if off % 4 == 0:
            ints = " | " + " ".join(
                str(struct.unpack_from("<I", plain, off + i)[0])
                for i in range(0, min(16, len(plain) - off) - 3, 4))
        print(f"0x{base + off:04x} +{off:<4d} {hexs:<48} {asc:<16}{ints}")
