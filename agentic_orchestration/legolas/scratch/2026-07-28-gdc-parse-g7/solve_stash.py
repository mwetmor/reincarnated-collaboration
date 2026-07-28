#!/usr/bin/env python3
"""SCRATCH — probe/brute-force the drifted character_stash v11 layout.

Same oracle as solve_inventory: per-tab block end + sentinel, then the outer
stash block end + sentinel.
"""
import itertools
import sys

from gdc_parse import Reader, read_item
import gdc_parse as G
from explore import prime_to_inventory


def prime_to_stash(path):
    r = prime_to_inventory(path)
    bid, bl, end = r.block_start(); r.read_int()
    G.blk_inventory(r, end); r.block_end(end, "inv")
    return r


def probe(path, plan):
    r = prime_to_stash(path)
    bid, bl, end = r.block_start()
    print(f"stash id={bid} len={bl} body=0x{r.p:x}..0x{end:x}")
    from explore import show
    show(r, plan)
    print(f"  cursor 0x{r.p:x}  block end 0x{end:x}  remaining {end - r.p}")


def try_layout(path, hdr_extra, tab_extra, item_extra, xy_float):
    r = prime_to_stash(path)
    bid, bl, end = r.block_start()
    ver = r.read_int()
    for _ in range(hdr_extra):
        r.read_int()
    n_tabs = r.read_int()
    if n_tabs > 64:
        return None
    tabs = []
    for _ in range(n_tabs):
        tid, tlen, tend = r.block_start()
        for _ in range(tab_extra):
            r.read_int()
        w = r.read_int(); h = r.read_int()
        n = r.read_int()
        if n > 500:
            return None
        items = []
        for _ in range(n):
            it = read_item(r)
            it["_extra"] = [r.read_int() for _ in range(item_extra)]
            it["x"] = r.read_float() if xy_float else r.read_int()
            it["y"] = r.read_float() if xy_float else r.read_int()
            items.append(it)
        if r.p != tend or not r.peek_key_sync():
            return None
        r.next_int()
        tabs.append({"width": w, "height": h, "items": items})
    if r.p != end or not r.peek_key_sync():
        return None
    return {"version": ver, "tabs": tabs}


if __name__ == "__main__":
    path = sys.argv[1]
    if len(sys.argv) > 2:
        probe(path, sys.argv[2])
        raise SystemExit
    hits = []
    for hdr, tab, extra in itertools.product(range(4), range(6), range(6)):
        for xyf in (True, False):
            try:
                res = try_layout(path, hdr, tab, extra, xyf)
            except Exception:
                continue
            if res:
                hits.append((hdr, tab, extra, xyf))
                print(f"HIT hdr_extra={hdr} tab_extra={tab} item_extra={extra} "
                      f"xy_float={xyf} tabs={len(res['tabs'])}")
    print(f"{len(hits)} layout(s) pass the oracle")
