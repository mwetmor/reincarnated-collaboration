#!/usr/bin/env python3
"""
pm4v_grade_2026_08_15.py — RUN KC2-PM4 LAP V, INSTRUMENT I-V4.

THE GRADE, and the incumbent-vs-decoded comparator.

Runs AFTER `pm4v_roster_2026_08_15.py` has emitted and hashed `pm4v_prediction.json`.  It re-reads
that file (and re-hashes it, HALTing on any change) so that the grade is provably computed against
a prediction that was fixed first — `PREREGISTRATION.md` § 5, steps 2 then 3.

Second job: run the SIM's OWN recipe (`wave_engine.py` `count_bounds` / `roll_wave`, as coded) over
the identical records, so the per-wave delta the conductor sees is DECODE-vs-INCUMBENT and not
decode-vs-one-seeded-roll.

READ-ONLY.  Author: legolas (UNKNOWN-RESEARCHER), 2026-08-15.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import statistics
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pm4v_roster_2026_08_15 as V                       # noqa: E402

OUT = V.OUT
BAND = V.BAND

# Referent, carried (I-21 § 4.1 / Lap U B-1). A GRADE, never an input (Law-3).
REF_LO, REF_HI, REF_MED = 19, 36, 25
# The sim's as-run rosters for 151..160 (I-21 § 4.2). Comparator only.
AS_RUN = [28, 18, 24, 13, 18, 19, 21, 33, 9, 5]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


# ---- the INCUMBENT recipe, transcribed from wave_engine.py -------------------------------------
def sim_alt_distribution(pool, gp, adj, wave):
    """`count_bounds` + `roll_wave`, as the sim codes them. Champions ADD."""
    def ri(name, d=0):
        v = pool.get(name, d)
        try:
            return int(v)
        except (TypeError, ValueError):
            return d

    exempt = bool(pool.get("ignoreGameBalance", False))
    reg_n, _ = V.roster_capacity(pool, False)
    ch_n, _ = V.roster_capacity(pool, True)
    if exempt:
        n_min, n_max = ri("spawnMin", 1), ri("spawnMax", 1)
        c_min, c_max = ri("championMin"), ri("championMax")
    else:
        n_min = (ri("spawnMin", 1) + 1) * 120 // 100
        n_max = ri("spawnMax", 1) + 1
        if n_min > n_max:
            n_min = n_max
        c_min = ri("championMin") + 1 + adj["spawnChampionMinAdj"][wave]
        c_max = ri("championMax") + 1 + adj["spawnChampionMaxAdj"][wave]
    if reg_n == 0:
        n_min = n_max = 0

    chance = float(pool.get("championChance", 0.0) or 0.0)
    reg_sup = list(range(n_min, n_max + 1)) if n_max >= n_min else [0]
    dist = {}
    if chance > 0.0:
        p = Fraction(min(max(chance, 0.0), 100.0)).limit_denominator(10 ** 6) / 100
        ch_sup = list(range(c_min, c_max + 1)) if c_max >= c_min else [0]
    else:
        p, ch_sup = Fraction(0), [0]
    for r in reg_sup:
        pr = Fraction(1, len(reg_sup))
        if p:
            for c in ch_sup:
                dist[r + c] = dist.get(r + c, Fraction(0)) + pr * p * Fraction(1, len(ch_sup))
        if 1 - p:
            dist[r] = dist.get(r, Fraction(0)) + pr * (1 - p)
    return dist


def main():
    pred_path = OUT / "pm4v_prediction.json"
    pred = json.loads(pred_path.read_text())
    pred_sha = sha256(pred_path)
    dig = json.loads((OUT / "pm4v_digests.json").read_text())
    if dig.get("prediction_before_grade") != pred_sha:
        raise SystemExit("HALT-DIGEST: pm4v_prediction.json changed after it was pinned")

    corpus = V.Corpus()
    _k, gp = corpus.get("records/game/gameproxies.dbr")
    _kk, rec = corpus.get("records/game/balancingadjustment_survivalmode_enemies03.dbr")
    ADJ = {f: {w: int(rec[f][w - 1]) for w in BAND} for f in
           ("spawnMinAdj", "spawnMaxAdj", "spawnChampionMinAdj", "spawnChampionMaxAdj")}

    import re
    from gd_arc_reader_2026_07_26 import ArcArchive
    t16 = ArcArchive(V.GD / "survivalmode1/resources/Scripts.arc") \
        .read_file("game/survival/tier16waves.lua").decode("latin-1")
    proxies = {}
    for m in re.finditer(r"spawnPoint0(\d)wave(\d\d)Proxies\s*=\s*\{([^}]*)\}", t16):
        proxies[(150 + int(m.group(2)), int(m.group(1)))] = re.findall(r'"([^"]+)"', m.group(3))

    sim = {}
    for wave in BAND:
        for limb, use06 in (("p06_off", False), ("p06_on", True)):
            tot = {0: Fraction(1)}
            for sp in range(1, 7):
                if sp == 6 and not use06:
                    continue
                names = proxies.get((wave, sp)) or []
                per_proxy = []
                for px_name in names:
                    _kp, px = corpus.get(px_name)
                    if px is None:
                        continue
                    alts = []
                    for i in range(1, 13):
                        pl = px.get(f"pool{i}")
                        if not pl:
                            continue
                        _kl, pool = corpus.get(pl)
                        if pool is None:
                            continue
                        alts.append((sim_alt_distribution(pool, gp, ADJ, wave),
                                     float(px.get(f"weight{i}", 100) or 0)))
                    if alts:
                        per_proxy.append(V.mix(alts))
                if per_proxy:
                    tot = V.convolve(tot, V.mix([(d, 1.0) for d in per_proxy]))
            sim.setdefault(limb, {})[wave] = V.stats(tot)

    dec_on = [pred["p06_on"][str(w)] for w in BAND]
    dec_off = [pred["p06_off"][str(w)] for w in BAND]
    sim_on = [sim["p06_on"][w] for w in BAND]
    sim_off = [sim["p06_off"][w] for w in BAND]

    def grade(dec, label):
        g1 = [w for w, d in zip(BAND, dec) if d["hi"] >= REF_LO]
        med = statistics.median(d["mean"] for d in dec)
        w160 = dec[-1]
        return dict(
            limb=label,
            G1_waves_whose_envelope_max_reaches_19=len(g1),
            G1_which=g1,
            G2_decoded_median_expected_roster=round(med, 4),
            G2_vs_referent_median_25_ratio=round(med / REF_MED, 4),
            G2_vs_referent_median_25_difference=round(med - REF_MED, 4),
            G3_wave160_expected=w160["mean"],
            G3_wave160_envelope=[w160["lo"], w160["hi"]],
            G3_wave160_shortfall_vs_19=round(REF_LO - w160["mean"], 4),
            total_expected_bodies_over_band=round(sum(d["mean"] for d in dec), 4),
        )

    priors = dict(
        PRIOR_1_median_in_20_26=bool(
            20 <= statistics.median(d["mean"] for d in dec_on) <= 26),
        PRIOR_1_value=round(statistics.median(d["mean"] for d in dec_on), 4),
        PRIOR_2_at_least_3_waves_expected_below_19=sum(
            1 for d in dec_on if d["mean"] < REF_LO),
        PRIOR_2_holds=bool(sum(1 for d in dec_on if d["mean"] < REF_LO) >= 3),
        PRIOR_3_wave160_below_19=bool(dec_on[-1]["mean"] < REF_LO),
        PRIOR_3_point_guess_8_to_12_hit=bool(8 <= dec_on[-1]["mean"] <= 12),
        PRIOR_4_G1_k_le_7=bool(len([w for w, d in zip(BAND, dec_on) if d["hi"] >= REF_LO]) <= 7),
        PRIOR_4_k=len([w for w, d in zip(BAND, dec_on) if d["hi"] >= REF_LO]),
    )

    out = dict(
        prediction_sha256_verified=pred_sha,
        referent_note=("19-36 living inside 11.64 m, median 25, a LOWER bound (Lap U B-1). "
                       "Used ONLY as a grade. Roster is a CEILING on concurrency (prereg B-2), so "
                       "every grade below is a NECESSARY-condition grade and proves no sufficiency."),
        grade_p06_on=grade(dec_on, "p06 ON (bonusSpawnStatus == true)"),
        grade_p06_off=grade(dec_off, "p06 OFF (bonusSpawnStatus == false)"),
        preregistered_priors=priors,
        per_wave=[dict(wave=w,
                       decoded_on=dec_on[i], decoded_off=dec_off[i],
                       incumbent_sim_on=sim_on[i], incumbent_sim_off=sim_off[i],
                       delta_expected_on=round(dec_on[i]["mean"] - sim_on[i]["mean"], 4),
                       delta_expected_off=round(dec_off[i]["mean"] - sim_off[i]["mean"], 4),
                       as_run_single_roll=AS_RUN[i])
                  for i, w in enumerate(BAND)],
        totals=dict(
            decoded_on=round(sum(d["mean"] for d in dec_on), 4),
            decoded_off=round(sum(d["mean"] for d in dec_off), 4),
            incumbent_on=round(sum(d["mean"] for d in sim_on), 4),
            incumbent_off=round(sum(d["mean"] for d in sim_off), 4),
            as_run_single_roll=sum(AS_RUN)),
    )
    (OUT / "pm4v_grade.json").write_text(json.dumps(out, indent=1))

    dg = json.loads((OUT / "pm4v_digests.json").read_text())
    dg["outputs"]["pm4v_grade.json"] = sha256(OUT / "pm4v_grade.json")
    dg["instruments"]["pm4v_grade_2026_08_15.py"] = sha256(__file__)
    (OUT / "pm4v_digests.json").write_text(json.dumps(dg, indent=1, sort_keys=True))

    print(f"{'wave':>5} {'dec ON':>18} {'dec OFF':>18} {'sim ON':>18} {'sim OFF':>18} {'as-run':>7}")
    for i, w in enumerate(BAND):
        f = lambda d: f"{d['mean']:7.3f}[{d['lo']:2d},{d['hi']:2d}]"      # noqa: E731
        print(f"{w:5d} {f(dec_on[i]):>18} {f(dec_off[i]):>18} "
              f"{f(sim_on[i]):>18} {f(sim_off[i]):>18} {AS_RUN[i]:7d}")
    print("\nTOTALS", json.dumps(out["totals"]))
    print("GRADE p06 ON ", json.dumps(out["grade_p06_on"]))
    print("GRADE p06 OFF", json.dumps(out["grade_p06_off"]))
    print("PRIORS", json.dumps(priors))


if __name__ == "__main__":
    main()
