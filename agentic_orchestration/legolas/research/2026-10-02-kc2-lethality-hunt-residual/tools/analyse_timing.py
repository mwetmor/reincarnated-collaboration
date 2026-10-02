"""Lead 1 + 2: engagement onset and the per-wave / per-attacker residual, oracle vs referent."""
import csv
import json
import sys
from collections import defaultdict
from statistics import mean, median

TRACE = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
         "2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv")
REF = 1605.6
BINS = (0, 3, 5, 7.5, 10, 15, 20, 30, 1e9)


def referent():
    W = defaultdict(list)
    for r in csv.DictReader(open(TRACE)):
        try:
            W[int(r["wave"])].append((float(r["t_sec"]), float(r["hp"]), float(r["health_max"])))
        except ValueError:
            pass
    out = {}
    for w, f in sorted(W.items()):
        t0 = f[0][0]
        decs = [(f[i][0] - t0, f[i - 1][1] - f[i][1]) for i in range(1, len(f))
                if f[i][1] < f[i - 1][1] and f[i][2] == f[i - 1][2]]   # E1: max-HP steps excluded
        T = f[-1][0] - t0 + 1 / 60
        bins = [0.0] * (len(BINS) - 1)
        for tt, a in decs:
            for i in range(len(BINS) - 1):
                if BINS[i] <= tt < BINS[i + 1]:
                    bins[i] += a
                    break
        first100 = next((tt for tt, a in decs if a >= 100), None)
        out[w] = {"t0": t0, "T": round(T, 3), "first_dec": decs[0][0] if decs else None,
                  "first_dec_ge100": first100, "intake": sum(a for _, a in decs), "bins": bins}
    return out


def oracle(path):
    d = json.load(open(path))
    rows = d["rows"]
    per = defaultdict(list)
    for s, rr in rows.items():
        for r in rr:
            per[r["wave"]].append(r)
    return d, per


def main(path, label):
    ref = referent()
    d, per = oracle(path)
    res = {"label": label, "per_wave": {}}
    print(f"== {label}  x{d['summary']['ratio_vs_referent']}")
    print("wave | ref first(>=100) | orc first med [min,max] | ref T | orc T | ref rate | orc rate | ratio | ref<10 hp/s | orc<10 hp/s | <10 ratio | >=10 ratio")
    for w in range(151, 161):
        rr = per.get(w, [])
        if not rr:
            continue
        fh = [r["ext"]["first_hit"]["t"] for r in rr if r["ext"]["first_hit"]]
        T = sum(r["t_s"] for r in rr) / len(rr)
        L = sum(r["landed"] for r in rr) / len(rr)
        ob = [sum(r["ext"]["landed_bins"][i] for r in rr) / len(rr) for i in range(len(BINS) - 1)]
        R = ref[w]
        # matched windows: first 10 s (or the wave, if shorter) and the remainder
        o10 = sum(ob[:4]); ot10 = min(10.0, T)
        r10 = sum(R["bins"][:4]); rt10 = min(10.0, R["T"])
        orest = L - o10; otr = max(T - 10.0, 0)
        rrest = R["intake"] - r10; rtr = max(R["T"] - 10.0, 0)
        row = {"ref_first_dec": R["first_dec"], "ref_first_dec_ge100": R["first_dec_ge100"],
               "orc_first_hit_median": median(fh), "orc_first_hit_min": min(fh), "orc_first_hit_max": max(fh),
               "orc_first_hit_mean": round(mean(fh), 3),
               "ref_T": R["T"], "orc_T_mean": round(T, 2),
               "ref_rate": round(R["intake"] / R["T"], 1), "orc_rate": round(L / T, 1),
               "ratio_vs_own_wave": round((L / T) / (R["intake"] / R["T"]), 3),
               "ratio_vs_pooled_ref": round((L / T) / REF, 3),
               "ref_first10_rate": round(r10 / rt10, 1), "orc_first10_rate": round(o10 / ot10, 1),
               "first10_ratio": round((o10 / ot10) / (r10 / rt10), 3) if r10 else None,
               "rest_ratio": (round((orest / otr) / (rrest / rtr), 3) if otr and rtr and rrest else None),
               "orc_bins_mean": [round(x) for x in ob], "ref_bins": [round(x) for x in R["bins"]]}
        res["per_wave"][w] = row
        print(f"{w} | {R['first_dec_ge100']} | {row['orc_first_hit_median']} [{row['orc_first_hit_min']},{row['orc_first_hit_max']}] | "
              f"{R['T']} | {row['orc_T_mean']} | {row['ref_rate']} | {row['orc_rate']} | {row['ratio_vs_own_wave']} | "
              f"{row['ref_first10_rate']} | {row['orc_first10_rate']} | {row['first10_ratio']} | {row['rest_ratio']}")
    return res


if __name__ == "__main__":
    out = main(sys.argv[1], sys.argv[2])
    if len(sys.argv) > 3:
        json.dump(out, open(sys.argv[3], "w"), indent=1)
