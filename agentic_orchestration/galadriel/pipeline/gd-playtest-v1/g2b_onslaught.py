#!/usr/bin/env python3
"""G-2b deliverable 6 -- the onslaught-attribution check.

Matt testifies he used Onslaught IN werewolf form. The ledger shows the
`onslaught` counter bursting to ~54 by play_time ~1145 and then apparently
frozen. This script answers ONE question empirically:

    Does the `onslaught` counter increment ANYWHERE at play_time > 1145?

with exact sample citations, and then -- separately, and only as far as the
series licenses -- reports whether the werewolf `claws` counter's behaviour is
CONSISTENT with absorbing those presses (the transform-remap hypothesis).
Consistency is not confirmation and is labelled as such.

Every counter here is treated as MEASURED: refusals (blank cells) are
reported as refusals, never as zeros and never interpolated.

Usage: g2b_onslaught.py <ta-gated.csv> <out.json>
"""
import csv
import json
import sys

COUNTERS = ("onslaught", "defaultweaponattack", "defaultkickattack",
            "werewolf1", "werewolf1_skill01_claws", "werewolf1_skill02_charge")
HUMAN_TOTALS = {"onslaught": 54, "defaultweaponattack": 74,
                "werewolf1_skill01_claws": 358,
                "werewolf1_skill02_charge": 175}


def load(path):
    rows = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            d = dict(i=int(r["i"]), pts_s=float(r["pts_s"]), gate=r["gate"],
                     play_time=int(r["play_time"]) if r["play_time"] else None)
            for c in COUNTERS:
                d[c] = int(r[c]) if r[c] else None
            rows.append(d)
    return rows


def trace(rows, col):
    """Every increment of a counter, with the citing sample on both sides."""
    incs, prev = [], None
    first_read = last_read = None
    n_read = n_refused = n_regress = 0
    for r in rows:
        v = r[col]
        if v is None:
            n_refused += 1
            continue
        n_read += 1
        if first_read is None:
            first_read = dict(i=r["i"], pts_s=r["pts_s"],
                              play_time=r["play_time"], value=v)
        last_read = dict(i=r["i"], pts_s=r["pts_s"],
                         play_time=r["play_time"], value=v)
        if prev is None:
            prev = dict(r)
            continue
        if v < prev[col]:
            n_regress += 1
            continue
        if v > prev[col]:
            incs.append(dict(
                delta=v - prev[col],
                from_sample=dict(i=prev["i"], pts_s=prev["pts_s"],
                                 play_time=prev["play_time"],
                                 value=prev[col], gate=prev["gate"]),
                to_sample=dict(i=r["i"], pts_s=r["pts_s"],
                               play_time=r["play_time"], value=v,
                               gate=r["gate"]),
                read_gap_s=round(r["pts_s"] - prev["pts_s"], 2)))
        prev = dict(r)
    return dict(column=col, n_read=n_read, n_refused=n_refused,
                coverage=round(n_read / len(rows), 4),
                n_nonmonotone_reads=n_regress,
                first_read=first_read, last_read=last_read,
                n_increments=len(incs),
                total_climb=(last_read["value"] - first_read["value"]
                             if first_read else None),
                human_read_total=HUMAN_TOTALS.get(col),
                increments=incs)


def main():
    src, out_path = sys.argv[1], sys.argv[2]
    rows = load(src)
    out = {"source": src, "n_samples": len(rows)}

    tr = {c: trace(rows, c) for c in COUNTERS}

    # ---- the question, answered exactly ------------------------------------
    ons = tr["onslaught"]
    after = [x for x in ons["increments"] if
             (x["to_sample"]["play_time"] or 0) > 1145]
    out["ANSWER_onslaught_increments_after_pt_1145"] = dict(
        n=len(after), increments=after)
    out["onslaught_full_trace"] = ons

    # frozen-plateau census: the run of samples reading the terminal value
    term = ons["last_read"]["value"]
    plateau = [r for r in rows if r["onslaught"] == term]
    first_at_term = plateau[0]
    out["onslaught_plateau"] = dict(
        terminal_value=term,
        first_sample_at_terminal=dict(
            i=first_at_term["i"], pts_s=first_at_term["pts_s"],
            play_time=first_at_term["play_time"]),
        n_samples_reading_terminal=len(plateau),
        n_refusals_after_first_terminal=sum(
            1 for r in rows if r["i"] > first_at_term["i"]
            and r["onslaught"] is None),
        n_samples_after_first_terminal=sum(
            1 for r in rows if r["i"] > first_at_term["i"]),
        play_time_span_at_terminal=[first_at_term["play_time"],
                                    ons["last_read"]["play_time"]])

    # ---- transform-remap consistency: what the OTHER counters do -----------
    out["counter_lifecycles"] = {
        c: {k: tr[c][k] for k in ("coverage", "n_read", "n_refused",
                                  "n_nonmonotone_reads", "first_read",
                                  "last_read", "n_increments", "total_climb",
                                  "human_read_total")}
        for c in COUNTERS}

    claws = tr["werewolf1_skill01_claws"]
    charge = tr["werewolf1_skill02_charge"]
    ons_rate_pre = None
    if ons["increments"]:
        pre = [x for x in ons["increments"]]
        span = (pre[-1]["to_sample"]["play_time"] -
                ons["first_read"]["play_time"])
        ons_rate_pre = round(ons["total_climb"] / span, 5) if span else None
    claws_span = None
    if claws["first_read"] and claws["last_read"]:
        claws_span = (claws["last_read"]["play_time"] -
                      claws["first_read"]["play_time"])
    out["transform_remap_consistency"] = dict(
        question=("If Onslaught presses were remapped onto a werewolf ability, "
                  "SOME werewolf counter must be absorbing them."),
        onslaught_presses_per_second_pre_freeze=ons_rate_pre,
        onslaught_active_span_play_time=[
            ons["first_read"]["play_time"],
            (ons["increments"][-1]["to_sample"]["play_time"]
             if ons["increments"] else None)],
        claws_total=claws["total_climb"],
        claws_active_span_play_time=[
            claws["first_read"]["play_time"] if claws["first_read"] else None,
            claws["last_read"]["play_time"] if claws["last_read"] else None],
        claws_presses_per_second=(round(claws["total_climb"] / claws_span, 5)
                                  if claws_span else None),
        charge_total=charge["total_climb"],
        reading=("Consistency only. The ledger can show that a werewolf "
                 "counter was live and climbing while `onslaught` was frozen; "
                 "it CANNOT show which physical key produced a claws "
                 "increment. Confirmation requires a keybind-visible v2 "
                 "capture or an input log."))

    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k != "onslaught_full_trace"}, indent=1)[:6000])
    print("\n--- onslaught increments (all) ---")
    for x in ons["increments"]:
        print(f"  i={x['to_sample']['i']:>6} pts={x['to_sample']['pts_s']:>8.1f} "
              f"pt={x['to_sample']['play_time']} "
              f"{x['from_sample']['value']}->{x['to_sample']['value']} "
              f"(+{x['delta']}) read_gap={x['read_gap_s']}s")


if __name__ == "__main__":
    main()
