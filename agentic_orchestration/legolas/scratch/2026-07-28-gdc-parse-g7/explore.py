#!/usr/bin/env python3
"""SCRATCH — typed explorer for reversing drifted .gdc block layouts.

The cipher decrypts a 4-byte word against one key value but a byte against the
key *as of that byte*, so a raw hexdump is meaningless. Layout discovery has to
proceed through correctly-typed reads. This walks a scripted read-plan and
prints each field, so a hypothesis can be tested one token at a time.
"""
import sys

from gdc_parse import Reader
import gdc_parse as G


def prime_to_inventory(path):
    r = Reader(open(path, "rb").read())
    r.read_key(); r.read_int(); r.read_int()
    r.read_wstring(); r.read_byte(); r.read_string(); r.read_int(); r.read_byte()
    r.read_byte(); r.next_int(); r.read_int()
    for _ in range(16):
        r.read_byte()
    bid, bl, end = r.block_start(); r.read_int()
    G.blk_character_info(r, end); r.block_end(end, "ci")
    bid, bl, end = r.block_start(); r.read_int()
    G.blk_character_bio(r, end); r.block_end(end, "bio")
    return r


def show(r, plan):
    for tok in plan:
        off = r.p
        if tok == "i":
            print(f"  0x{off:04x} int    {r.read_int()}")
        elif tok == "b":
            print(f"  0x{off:04x} byte   {r.read_byte()}")
        elif tok == "f":
            print(f"  0x{off:04x} float  {r.read_float()}")
        elif tok == "s":
            print(f"  0x{off:04x} str    {r.read_string()!r}")
        elif tok == "n":
            print(f"  0x{off:04x} nextint(no-adv) {r.next_int()}")
        elif tok == "B":
            bid, bl, e = r.block_start()
            print(f"  0x{off:04x} BLOCKSTART id={bid} len={bl} end=0x{e:x}")
        elif tok == "E":
            ok = r.peek_key_sync()
            v = r.next_int()
            print(f"  0x{off:04x} BLOCKEND sentinel={v} sync={'OK' if ok else 'BAD'}")


if __name__ == "__main__":
    r = prime_to_inventory(sys.argv[1])
    bid, bl, end = r.block_start()
    print(f"inventory id={bid} len={bl} body=0x{r.p:x}..0x{end:x}")
    show(r, sys.argv[2])
    print(f"  cursor now 0x{r.p:04x}  (block end 0x{end:x}, remaining {end - r.p})")
