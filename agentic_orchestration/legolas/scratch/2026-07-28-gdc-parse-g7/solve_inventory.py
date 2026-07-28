#!/usr/bin/env python3
"""SCRATCH — brute-force the drifted inventory-v11 item layout.

Oracle: a candidate layout is accepted only if the whole inventory block is
consumed to exactly its declared end AND the end-of-block sentinel decrypts to
0. The sentinel is a stored literal 0, so the raw word equals the running key
at that point -- a 32-bit check. A wrong layout passing by chance is ~2^-32.
"""
import itertools
import sys

from gdc_parse import Reader
import gdc_parse as G
from explore import prime_to_inventory


def make_item_reader(pre, mid, post):
    """pre/mid/post = counts of extra 4-byte words at three candidate slots."""
    def read_item(r):
        it = {}
        for _ in range(pre):
            r.read_int()
        it["baseName"] = r.read_string()
        it["prefixName"] = r.read_string()
        it["suffixName"] = r.read_string()
        it["modifierName"] = r.read_string()
        it["transmuteName"] = r.read_string()
        for _ in range(mid):
            r.read_int()
        it["seed"] = r.read_int()
        it["componentName"] = r.read_string()
        it["relicBonus"] = r.read_string()
        it["componentSeed"] = r.read_int()
        it["augmentName"] = r.read_string()
        it["unknown"] = r.read_int()
        it["augmentSeed"] = r.read_int()
        it["var1"] = r.read_int()
        it["stackCount"] = r.read_int()
        it["_extra_post"] = [r.read_int() for _ in range(post)]
        return it
    return read_item


def try_layout(path, pre, mid, post, eq_extra, inv_xy):
    r = prime_to_inventory(path)
    bid, bl, end = r.block_start()
    ri = make_item_reader(pre, mid, post)
    out = {"sacks": [], "equipment": [], "weapon1": [], "weapon2": []}
    ver = r.read_int()
    flag = r.read_byte()
    if not flag:
        return None
    numBags = r.read_int()
    out["focused"] = r.read_int()
    out["selected"] = r.read_int()
    for _ in range(numBags):
        sid, slen, send = r.block_start()
        tempBool = r.read_byte()
        n = r.read_int()
        if n > 500:
            return None
        items = []
        for _ in range(n):
            it = ri(r)
            it["_xy"] = [r.read_int() for _ in range(inv_xy)]
            items.append(it)
        if r.p != send:
            return None
        if not r.peek_key_sync():
            return None
        r.next_int()
        out["sacks"].append({"tempBool": tempBool, "items": items})
    out["useAlternate"] = r.read_byte()
    for i in range(12):
        off = r.p
        it = ri(r)
        it["_attached"] = [r.read_byte() for _ in range(eq_extra)]
        it["_slot"] = i
        it["_offset"] = f"0x{off:x}"
        out["equipment"].append(it)
    out["alternate1"] = r.read_byte()
    for i in range(2):
        off = r.p
        it = ri(r)
        it["_attached"] = [r.read_byte() for _ in range(eq_extra)]
        it["_slot"] = i
        it["_offset"] = f"0x{off:x}"
        out["weapon1"].append(it)
    out["alternate2"] = r.read_byte()
    for i in range(2):
        off = r.p
        it = ri(r)
        it["_attached"] = [r.read_byte() for _ in range(eq_extra)]
        it["_slot"] = i
        it["_offset"] = f"0x{off:x}"
        out["weapon2"].append(it)
    if r.p != end:
        return None
    if not r.peek_key_sync():
        return None
    return out


if __name__ == "__main__":
    path = sys.argv[1]
    hits = []
    for pre, mid, post in itertools.product(range(5), repeat=3):
        if pre + mid + post > 6:
            continue
        for eq_extra in (0, 1, 2):
            for inv_xy in (2, 3):
                try:
                    res = try_layout(path, pre, mid, post, eq_extra, inv_xy)
                except Exception:
                    continue
                if res:
                    hits.append((pre, mid, post, eq_extra, inv_xy))
                    print(f"HIT pre={pre} mid={mid} post={post} "
                          f"eq_extra={eq_extra} inv_xy={inv_xy}")
    print(f"{len(hits)} layout(s) satisfy the block-end + sentinel oracle")
