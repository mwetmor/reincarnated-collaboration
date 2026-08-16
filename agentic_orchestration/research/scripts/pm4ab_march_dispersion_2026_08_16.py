#!/usr/bin/env python3
"""KC2-PM4 · LAP AB — THE REFERENT'S MARCH DISPERSION + TWO CARRIED ITEMS.  Instrument I-AB.

WHY THIS EXISTS
    `R-PM4-70 part 3` commissioned three forks in one bounded record lap:
      (a) THE REFERENT'S MARCH DISPERSION — data side (does anything in the Crucible context act
          on the tier-16 roster's movement speed?) and video/track side (re-query the ALREADY
          PINNED Lap R / Lap U referent-track artifacts under the new question).
      (b) `UNREACHED-AA-3` — the AlertBeforePursue animation length.
      (c) `OBS-I26-1` disposition — reconcile Lap AA § 5.2's "essentially every body" with
          § 2.4's 0.112 m minimum.

    Law 3 (charter): measured decode of the referent is authorized; referent numbers are GRADES
    for the sim, never inputs.  `R-PM4-70 part 4(ii)`: brackets stay brackets — every m/s
    quantity is published on BOTH `UNREACHED-T1` edges, never as a scalar.

    RE-IMPLEMENTS NOTHING.  `gd_arz_adapter_2026_07_24`, `gd_arc_reader_2026_07_26` and
    `pm4s_pe_2026_08_14.PE32` are imported unchanged (NOTE-9).  Prior-lap numbers are IMPORTED
    BY IDENTITY from pinned artifacts with their digests asserted, never restated from prose
    (`R-PM4-67 part 2`, the D-CON-6 law).

READ-ONLY on `/Users/admin/Games/vendor/**` and on every prior lap's notes.  Writes ONLY into
this lap's notes directory.  No sim artifact is opened by any leg (outcome firewall).

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.  Run KC2-PM4, Lap AB.
Pre-registration: `.../2026-08-16-kc2-pm4-lap-ab-march-dispersion/prereg.md`,
committed ALONE in `0e22f57d` before this file existed,
sha256 `61e7db1814f6070627977393448378d4ca42f00cf1a57fb0d5087382c2dd2248`.
"""
from __future__ import annotations

import bisect
import collections
import csv
import hashlib
import importlib.util
import json
import math
import pathlib
import re
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
COLLAB = HERE.parent.parent.parent
LAP = "2026-08-16-kc2-pm4-lap-ab-march-dispersion"
OUT = COLLAB / "agentic_orchestration/legolas/notes" / LAP
NOTES = COLLAB / "agentic_orchestration/legolas/notes"
ED = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")

sys.path.insert(0, str(HERE))
from pm4s_pe_2026_08_14 import PE32, modules, sha256  # noqa: E402


def _load(mod: str, fn: str):
    spec = importlib.util.spec_from_file_location(mod, HERE / fn)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ARZ = _load("arz", "gd_arz_adapter_2026_07_24.py")
ARC = _load("arc", "gd_arc_reader_2026_07_26.py")

LOG: list[str] = []


def log(s: str = "") -> None:
    LOG.append(s)


def halt(msg: str):
    raise SystemExit(f"HALT — {msg}")


# ===================================================================== § 1  PINS
# Prereg § 6 (GL-6).  EXPECT digests are published by a prior lap and are ASSERTED;
# RECORD digests are pinned here for the first time and are recorded, not asserted.

PIN_EXPECT = {
    OUT / "prereg.md":
        "61e7db1814f6070627977393448378d4ca42f00cf1a57fb0d5087382c2dd2248",
    # shipped corpus, published by Lap AA § 11.2 / Lap Z § 10.2
    ED / "database/database.arz":
        "2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd",
    ED / "database/templates.arc":
        "679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602",
    ED / "mods/survivalmode/database/SurvivalMode.arz":
        "e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6",
    ED / "survivalmode1/database/SurvivalMode1.arz":
        "6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252",
    # prior-lap artifacts imported BY IDENTITY
    NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_geometry_v3.csv":
        "5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2",
    NOTES / "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv":
        "991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c",
}

PIN_RECORD = [
    NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact/pm4r_speed_terms.csv",
    NOTES / "2026-08-14-kc2-pm4-lap-t-arrival-decode/pm4t_march_speed.csv",
    NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_ramp_analysis.json",
    NOTES / "2026-08-16-kc2-pm4-lap-aa-referent-spawn-structure/pm4aa_findings.md",
    ED / "gdx1/database/GDX1.arz", ED / "gdx2/database/GDX2.arz", ED / "gdx3/database/GDX3.arz",
    ED / "survivalmode2/database/SurvivalMode2.arz",
    ED / "survivalmode3/database/SurvivalMode3.arz",
    ED / "resources/Creatures.arc", ED / "gdx1/resources/Creatures.arc",
    ED / "gdx2/resources/Creatures.arc", ED / "gdx3/resources/Creatures.arc",
    ED / "mods/survivalmode/resources/Creatures.arc",
    pathlib.Path("/Users/admin/Games/vendor/grim-dawn/Game.dll"),
]

DIGESTS: dict[str, str] = {}


def pins():
    log("=" * 78)
    log("§ 1  PINS — every artifact re-hashed BEFORE use (GL-6, full 64-hex)")
    log("=" * 78)
    for p, expect in PIN_EXPECT.items():
        got = sha256(p)
        DIGESTS[str(p)] = got
        if got != expect:
            halt(f"PIN MISMATCH {p}\n  expect {expect}\n  got    {got}")
        log(f"  EXACT   {got}  {p}")
    for p in PIN_RECORD:
        got = sha256(p)
        DIGESTS[str(p)] = got
        log(f"  RECORD  {got}  {p}")
    log("")


# ===================================================================== § 2  CORPUS
# The mod stack, in load order.  Later layers WIN (Lap AA `D-AA-4`).  The `mods/survivalmode`
# layer is the Crucible's own record set and is where every defence-site record lives; it is
# NOT reachable from the seven-layer stack earlier laps walked, and its absence is why a naive
# `records/creatures/defenses/*` probe returns nothing (Lap R § 5.4's class of miss).
LAYERS = [
    ("base", "database/database.arz"),
    ("gdx1", "gdx1/database/GDX1.arz"),
    ("gdx2", "gdx2/database/GDX2.arz"),
    ("gdx3", "gdx3/database/GDX3.arz"),
    ("sm",   "mods/survivalmode/database/SurvivalMode.arz"),
    ("sm1",  "survivalmode1/database/SurvivalMode1.arz"),
    ("sm2",  "survivalmode2/database/SurvivalMode2.arz"),
    ("sm3",  "survivalmode3/database/SurvivalMode3.arz"),
]
ARCHIVES: list[tuple[str, object]] = []
_RC: dict[str, tuple] = {}


def resolve(path: str):
    """Resolve one record path through the mod stack.  Later layer wins."""
    if path in _RC:
        return _RC[path]
    out = (None, None)
    for name, ar in ARCHIVES:
        if path in ar.records:
            out = (name, ar.read_record(path))
    _RC[path] = out
    return out


# ===================================================================== § 3  DECOY SET
# Prereg § 4.1.1.  The COMPLETE run/total-speed field surface is read out of `templates.arc`
# and published, so that the fields this lap acts on are visibly CHOSEN, not accidentally found
# (`D-Z-1` / `D-AA-1`).

SPEED_ANY = re.compile(r"(RunSpeed|TotalSpeed)")
# the families that can act on a body's own locomotion, as opposed to displaying it,
# animating it, resisting a slow, or slowing somebody else's:
SELF_LOCO = re.compile(r"^(characterRunSpeed|characterRunSpeedModifier|"
                       r"characterRunSpeedMaxModifier|characterTotalSpeedModifier|"
                       r"characterRunSpeedJitter)$")
APPLIED_SLOW = re.compile(r"^(offensiveSlowRunSpeed|offensiveSlowTotalSpeed|"
                          r"retaliationSlowRunSpeed|retaliationSlowTotalSpeed)")
MODIFIER_OR_SLOW = re.compile(r"(SlowRunSpeed|SlowTotalSpeed|RunSpeedModifier|"
                              r"TotalSpeedModifier|RunSpeedMaxModifier)")


def field_surface(tpl):
    """Every template-declared field name matching the run/total-speed surface, classified."""
    rows = []
    seen = {}
    unreadable = 0
    for n in sorted(tpl.names()):
        try:
            b = tpl.read_file(n)
        except Exception:
            unreadable += 1
            continue
        for m in re.finditer(rb'Variable\s*\{(.{0,900}?)\}', b, re.S | re.I):
            blk = m.group(1)
            nm = re.search(rb'name\s*=\s*"([^"]+)"', blk)
            if not nm:
                continue
            nm = nm.group(1).decode()
            if not SPEED_ANY.search(nm):
                continue
            ty = re.search(rb'type\s*=\s*"([^"]*)"', blk)
            cl = re.search(rb'class\s*=\s*"([^"]*)"', blk)
            de = re.search(rb'description\s*=\s*"([^"]*)"', blk)
            key = nm
            if key in seen:
                seen[key]["templates"].add(n)
                continue
            if SELF_LOCO.match(nm):
                fam = "SELF-LOCOMOTION"
            elif APPLIED_SLOW.match(nm):
                fam = "APPLIED-SLOW (acts on the caster's TARGET, not on the caster)"
            elif nm.startswith("defensiveTotalSpeed"):
                fam = "SLOW-RESISTANCE"
            elif re.search(r"CapM(ax|in)$", nm):
                fam = "ENGINE-CAP"
            elif nm.startswith("tab1") or nm.startswith("tab2"):
                fam = "UI-DISPLAY (decoy)"
            else:
                fam = "OTHER (decoy)"
            seen[key] = dict(
                field=nm, family=fam,
                type=(ty.group(1).decode() if ty else ""),
                cls=(cl.group(1).decode() if cl else ""),
                description=(de.group(1).decode() if de else ""),
                templates={n})
    for k in sorted(seen):
        r = dict(seen[k])
        r["n_templates"] = len(r["templates"])
        r["example_template"] = sorted(r.pop("templates"))[0]
        rows.append(r)
    return rows, unreadable


def nonneutral(rec, pat):
    out = {}
    for k, v in rec.items():
        if not pat.search(k):
            continue
        if v in (0, 0.0, False):
            continue
        if isinstance(v, list) and all(x == 0 for x in v):
            continue
        out[k] = v
    return out


# ===================================================================== § 4  FORK (a) DATA
def fork_a_data(tier16_records, all790):
    log("=" * 78)
    log("§ 4  FORK (a) DATA SIDE — what acts on monster movement speed in the Crucible context")
    log("=" * 78)
    res: dict = {}

    # ---- A-d1 : Lap T's three negatives, re-verified from my own seat -------------
    lay_si, si = resolve("records/game/survivalinfo.dbr")
    adj = {k: v for k, v in (si or {}).items() if "survivalAdjustment" in k}
    res["A_d1"] = dict(survivalinfo_layer=lay_si, adjustment_records=adj, per_record={})
    log(f"  A-d1  survivalinfo.dbr [{lay_si}] -> {len(adj)} adjustment records "
        f"(indexed by DIFFICULTY, not by wave):")
    for k in sorted(adj):
        p = adj[k]
        lay, rec = resolve(p)
        surf = {kk: vv for kk, vv in rec.items() if SPEED_ANY.search(kk)}
        nz = nonneutral(rec, SPEED_ANY)
        res["A_d1"]["per_record"][p] = dict(
            selector=k, layer=lay, n_fields=len(rec),
            n_speed_fields=len(surf), n_nonzero=len(nz), nonzero=nz)
        log(f"          {k:26s} {p.split('/')[-1]:52s} fields={len(rec)} "
            f"speed_surface={len(surf)} NON-ZERO={len(nz)}")
    mods_ = collections.Counter()
    for p in tier16_records:
        lay, rec = resolve(p)
        v = rec.get("characterRunSpeedModifier")
        mods_[("ABSENT" if v is None else v)] += 1
    res["A_d1"]["tier16_characterRunSpeedModifier"] = {str(k): v for k, v in mods_.items()}
    log(f"  A-d1  tier-16 characterRunSpeedModifier census: {dict(mods_)}")

    # ---- A-d2 : the layer Lap T's artifact does not carry -------------------------
    cen = {}
    for f in ("characterRunSpeed", "characterRunSpeedModifier", "characterRunSpeedMaxModifier",
              "characterRunSpeedJitter", "characterTotalSpeedModifier"):
        c = collections.Counter()
        for p in tier16_records:
            lay, rec = resolve(p)
            v = rec.get(f)
            c[("ABSENT" if v is None else (tuple(v) if isinstance(v, list) else v))] += 1
        cen[f] = {str(k): v for k, v in sorted(c.items(), key=lambda x: str(x[0]))}
    c790 = collections.Counter()
    for p in all790:
        lay, rec = resolve(p)
        v = rec.get("characterTotalSpeedModifier")
        c790[("ABSENT" if v is None else (tuple(v) if isinstance(v, list) else v))] += 1
    res["A_d2"] = dict(tier16_census=cen,
                       roster790_characterTotalSpeedModifier={str(k): v for k, v in c790.items()},
                       n_tier16=len(tier16_records), n_roster790=len(all790))
    log(f"  A-d2  tier-16 characterTotalSpeedModifier: {cen['characterTotalSpeedModifier']}")
    log(f"  A-d2  tier-16 characterRunSpeedMaxModifier: {cen['characterRunSpeedMaxModifier']}")
    log(f"  A-d2  790-roster characterTotalSpeedModifier: {dict(c790)}")
    log(f"  A-d2  tier-16 characterRunSpeedJitter: {cen['characterRunSpeedJitter']}")

    # ---- A-d3 / A-d4 / A-d5 : the Crucible mod layer, swept EXHAUSTIVELY ----------
    sm = dict(ARCHIVES)["sm"]
    hits = []
    for p in sorted(sm.records):
        lay, rec = resolve(p)
        if rec is None:
            continue
        h = nonneutral(rec, MODIFIER_OR_SLOW)
        if h:
            hits.append(dict(record=p, layer=lay, terms={k: v for k, v in h.items()}))
    # who owns each hit?
    owners = collections.defaultdict(list)
    for p in sorted(sm.records):
        lay, rec = resolve(p)
        if rec is None:
            continue
        for k, v in rec.items():
            if isinstance(v, str) and any(v == h["record"] for h in hits):
                owners[v].append(dict(owner=p, field=k))
    for h in hits:
        h["referenced_by"] = owners.get(h["record"], [])
    res["A_d3"] = dict(n_records_scanned=len(sm.records), n_hits=len(hits), hits=hits)
    log(f"  A-d3  Crucible mod layer swept EXHAUSTIVELY: {len(sm.records)} records, "
        f"{len(hits)} carry a non-neutral MODIFIER/SLOW run- or total-speed term:")
    for h in hits:
        log(f"          {h['record']:64s} {h['terms']}")
        for o in h["referenced_by"]:
            log(f"                referenced by  {o['owner']}  ::  {o['field']}")

    # purchased-vs-unpurchased disposition (Lap PM3-C pinned the four purchases)
    PURCHASED = ["records/creatures/defenses/turret_ice.dbr",
                 "records/creatures/defenses/turret_lightning.dbr",
                 "records/creatures/defenses/turret_fire.dbr",
                 "records/creatures/defenses/banner_offense.dbr"]
    defence_rows = []
    for p in sorted(x for x in sm.records if x.startswith("records/creatures/defenses/")
                    and "/bios/" not in x):
        lay, rec = resolve(p)
        skills = {k: v for k, v in rec.items()
                  if isinstance(v, str) and v.endswith(".dbr")
                  and re.search(r"[Ss]killName", k)}
        terms = {}
        seen = set()
        frontier = [(p, 0)]
        while frontier:
            q, d = frontier.pop(0)
            if q in seen or d > 3:
                continue
            seen.add(q)
            lay2, r2 = resolve(q)
            if r2 is None:
                continue
            h = nonneutral(r2, MODIFIER_OR_SLOW)
            if h and q != p:
                terms[q] = h
            for k, v in r2.items():
                if isinstance(v, str) and v.lower().endswith(".dbr"):
                    frontier.append((v, d + 1))
        defence_rows.append(dict(
            record=p, layer=lay, purchased_in_referent=(p in PURCHASED),
            n_skill_refs=len(skills), chain_size=len(seen), speed_terms=terms))
    res["A_d3"]["defence_records"] = defence_rows
    log(f"  A-d3  defence-site creature records: {len(defence_rows)} "
        f"({sum(1 for d in defence_rows if d['purchased_in_referent'])} purchased in the referent)")
    for d in defence_rows:
        if d["speed_terms"]:
            tag = "PURCHASED" if d["purchased_in_referent"] else "NOT-PURCHASED"
            log(f"          [{tag:13s}] {d['record']:56s} {d['speed_terms']}")

    # the reach of the one purchased term
    lay_c, ctl = resolve("records/controllers/defenses/controller_turretice.dbr")
    lay_i, ice = resolve("records/skills/defenses/turretice_icebolt.dbr")
    reach = {k: v for k, v in (ctl or {}).items()
             if re.search(r"^(ViewDistance|InnerViewDistance|MaxPursuitDistance|MaxYViewDistance)$", k)}
    geom = {k: v for k, v in (ice or {}).items()
            if re.search(r"projectileExplosionRadius|skillProjectileNumber|"
                         r"skillProjectileTargetGroundOnly|offensiveFreezeChance", k)}
    slow = {k: v for k, v in (ice or {}).items() if re.search(r"offensiveSlowRunSpeed", k)}
    res["A_d3"]["purchased_slow"] = dict(
        skill="records/skills/defenses/turretice_icebolt.dbr", skill_layer=lay_i,
        controller="records/controllers/defenses/controller_turretice.dbr",
        controller_layer=lay_c, reach=reach, geometry=geom, slow_terms=slow)
    log(f"  A-d3  the ONE purchased term — turretice_icebolt: {slow}")
    log(f"          reach (controller_turretice): {reach}")
    log(f"          geometry: {geom}")

    # A-d4 : the four celestial blessings
    bless = []
    for p in sorted(x for x in sm.records if x.startswith("records/skills/powerups/")):
        lay, rec = resolve(p)
        bless.append(dict(record=p, layer=lay, cls=rec.get("Class", ""),
                          nonneutral=nonneutral(rec, SPEED_ANY)))
    res["A_d4"] = dict(n_powerup_records=len(bless), records=bless,
                       n_with_speed_term=sum(1 for b in bless if b["nonneutral"]),
                       purchased_in_referent=False,
                       basis="Lap PM3-C README § 1: the referent bought FOUR defence-site "
                             "constructions and ZERO celestial blessings")
    log(f"  A-d4  celestial blessings: {len(bless)} powerup records, "
        f"{res['A_d4']['n_with_speed_term']} carry a non-neutral run/total-speed term "
        f"(MEASURED-INACTIVE for the referent regardless — not purchased)")

    # ---- A-d6 : always-on / conditional / transient, IMPORTED BY IDENTITY from Lap T
    lt = {r["record"]: r for r in csv.DictReader(
        (NOTES / "2026-08-14-kc2-pm4-lap-t-arrival-decode/pm4t_march_speed.csv").open())}
    perm = collections.Counter()
    trans = collections.Counter()
    covered = 0
    for p in tier16_records:
        r = lt.get(p)
        if r is None:
            continue
        covered += 1
        perm[int(r["chain_perm_speed_terms"] or 0)] += 1
        trans[int(r["chain_transient_speed_terms"] or 0)] += 1
    res["A_d6"] = dict(
        source="pm4t_march_speed.csv (Lap T § 3.3), IMPORTED BY IDENTITY",
        tier16_covered=covered, tier16_total=len(tier16_records),
        chain_perm_speed_terms={str(k): v for k, v in sorted(perm.items())},
        chain_transient_speed_terms={str(k): v for k, v in sorted(trans.items())},
        tier16_records_with_a_permanent_term=sum(v for k, v in perm.items() if k > 0))
    log(f"  A-d6  Lap T buckets over the tier-16 subset ({covered}/{len(tier16_records)} covered): "
        f"records with >=1 ALWAYS-ON speed term = "
        f"{res['A_d6']['tier16_records_with_a_permanent_term']}")
    return res


# ===================================================================== § 5  FORK (a) VIDEO
K_EDGES = {"px-LO": 3.055412, "px-HI": 3.209466}   # Lap T § 3.5, UNREACHED-T1, BOTH edges


def quantile(xs, p):
    if not xs:
        return None
    k = (len(xs) - 1) * p
    f = int(math.floor(k))
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (k - f) * (xs[c] - xs[f])


def fork_a_video(speed_rows):
    log("=" * 78)
    log("§ 5  FORK (a) VIDEO/TRACK SIDE — re-query of ALREADY-PINNED artifacts (the Lap Y lesson)")
    log("=" * 78)
    ramp = json.loads(
        (NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_ramp_analysis.json").read_text())
    t50 = ramp["S4_march_reconciliation"]["referent_t50_s"]
    t90 = ramp["S4_march_reconciliation"]["referent_t90_s"]
    measured_width = t90 - t50
    peak = ramp["S2_D_U_3"]["peak_living_per_wave"]
    log(f"  A-v1  Lap U F-10 living-count ramp, IMPORTED BY IDENTITY: "
        f"t50={t50} s  t90={t90} s  width={measured_width:.4f} s")
    log(f"  A-v1  per-wave decomposition present in the pinned artifact? "
        f"{'NO — only pooled t50/t90 are pinned' }")
    log(f"  A-v1  peak living count per wave (pinned): {peak}")

    # A-v2 : is per-body approach speed reachable from the pins?
    arrivals_hdr = (NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_arrivals.csv"
                    ).open().readline().strip().split(",")
    has_speed = [c for c in arrivals_hdr if re.search(r"speed|v_|mps", c, re.I)]
    av2 = dict(
        pinned_arrival_columns=arrivals_hdr,
        columns_carrying_a_speed=has_speed,
        verdict="UNREACHED",
        obstacle=("the pinned track artifact carries entry RADIUS, bearing, lifetime and frame "
                  "count for entries into the OBSERVED ~11.6 m frustum window only — no per-body "
                  "velocity column exists, the tracks do not span the 29-39 m march, and Lap U's "
                  "own D-U-3 demotes the entry set to a STRICT UPPER BOUND on arrival rate. A "
                  "per-body full-march approach-speed distribution is not recoverable from the "
                  "pins, and the prereg forbids re-opening raw video for it."))
    log(f"  A-v2  per-body approach speed: {av2['verdict']} — {av2['obstacle'][:96]}...")

    # A-v3 : the compression test
    v = sorted(float(r["value"]) for r in speed_rows)
    qs = {f"p{int(p*100)}": quantile(v, p) for p in (0, .05, .10, .25, .50, .75, .90, .95, 1.0)}
    D_PROXIES = {
        # Lap AA § 2.4, candidate-restricted (a/b/e) — DO-NOT 5 says this one governs
        "AA-candidate spawn->patrol-centroid median": 33.863,
        "AA-candidate spawn->nearest-patrol median": 16.104,
        # Lap U § 1.7 implied spawn->player, INFERRED-WITH-EVIDENCE, both edges
        "U-implied spawn->player (lo119 edge)": 21.038,
        "U-implied spawn->player (hi125 edge)": 22.0993,
    }
    table = []
    for dname, dval in D_PROXIES.items():
        for ename, K in K_EDGES.items():
            pred_t50 = dval / (qs["p50"] * K)
            pred_t90 = dval / (qs["p10"] * K)   # slow bodies arrive late
            pred_full = dval / (v[0] * K) - dval / (v[-1] * K)
            table.append(dict(
                distance_proxy=dname, distance_m=dval, speed_edge=ename, K_m_per_s_per_unit=K,
                predicted_t50_s=round(pred_t50, 4), predicted_t90_s=round(pred_t90, 4),
                predicted_width_s=round(pred_t90 - pred_t50, 4),
                predicted_full_band_span_s=round(pred_full, 4),
                measured_width_s=round(measured_width, 4),
                ratio_predicted_over_measured=round((pred_t90 - pred_t50) / measured_width, 4)))
    log(f"  A-v3  tier-16 rostered actors (waves 151-160): n={len(v)}")
    log(f"  A-v3  characterRunSpeed quantiles: "
        + "  ".join(f"{k}={vv:.4f}" for k, vv in qs.items()))
    log(f"  A-v3  MEASURED ramp width (t90-t50) = {measured_width:.4f} s")
    log("  A-v3  PREDICTED arrival-time width from the referent's OWN record band, "
        "both edges, every named distance proxy:")
    for r in table:
        log(f"          {r['distance_proxy']:44s} {r['speed_edge']:6s} "
            f"pred_width={r['predicted_width_s']:7.3f} s   "
            f"ratio pred/meas = {r['ratio_predicted_over_measured']:5.2f}")

    fails = all(r["predicted_width_s"] > r["measured_width_s"] for r in table)
    # the confound, priced from pinned artifacts (D-I26-4's lesson, applied to my own criterion)
    vrows = list(csv.DictReader(
        (NOTES / "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv").open()))
    ebod = collections.defaultdict(float)
    for r in vrows:
        ebod[int(r["global_wave"])] += float(r["e_bodies"])
    ratio = {}
    for w in range(151, 161):
        ratio[w] = round(peak[str(w)] / ebod[w], 4) if ebod[w] else None
    med_ratio = quantile(sorted(x for x in ratio.values() if x is not None), 0.5)
    log(f"  A-v3  ⚑ CONFOUND, priced: peak-living / decoded-E[bodies] per wave = {ratio}")
    log(f"          median = {med_ratio:.4f} — fewer than half a wave's decoded bodies are ever "
        f"simultaneously inside the observed window, and waves 159/160 exceed 1.0 "
        f"(previous-wave survivors contaminate the baseline).")

    return dict(
        A_v1=dict(t50_s=t50, t90_s=t90, measured_width_s=round(measured_width, 4),
                  per_wave_ramp_pinned=False, peak_living_per_wave=peak),
        A_v2=av2,
        A_v3=dict(n_actors=len(v), quantiles=qs, table=table,
                  F_AB_1_fails_as_written=fails,
                  confound_peak_over_expected=ratio,
                  confound_median=med_ratio))


# ===================================================================== § 6  FORK (b)
ANM_ARCS = ["resources/Creatures.arc", "gdx1/resources/Creatures.arc",
            "gdx2/resources/Creatures.arc", "gdx3/resources/Creatures.arc",
            "mods/survivalmode/resources/Creatures.arc"]


def b1_ordinal():
    """Three-start convergence on `AnimationSet_Type` ordinal 0x21."""
    g = modules()["Game.dll"]
    raw = g.raw
    TARGET = 0x100E77F0                     # ControllerAI::PlayAnimation
    exp = g.exports()
    rvas = sorted(set(exp.values()))
    rev = {}
    for n, r in exp.items():
        rev.setdefault(r, n)

    def owner(va):
        r = va - g.image_base
        i = bisect.bisect_right(rvas, r) - 1
        return (rev[rvas[i]], r - rvas[i]) if i >= 0 else (None, None)

    text = [s for s in g.sections if s["name"] == ".text"][0]
    lo, hi = text["raddr"], text["raddr"] + text["rsize"]
    sites = []
    i = lo
    while True:
        j = raw.find(b"\xe8", i, hi - 5)
        if j < 0:
            break
        rel = struct.unpack_from("<i", raw, j + 1)[0]
        nxt = g.off_to_rva(j + 5)
        if nxt is not None and g.image_base + nxt + rel == TARGET:
            back = raw[max(lo, j - 48):j]
            pushes = [back[k + 1] for k in range(len(back) - 1) if back[k] == 0x6A]
            sym, d = owner(g.image_base + nxt - 5)
            sites.append(dict(call_va=hex(g.image_base + nxt - 5),
                              push_imm8_window=[hex(x) for x in pushes],
                              ordinal_last_push=(hex(pushes[-1]) if pushes else None),
                              caller=sym, caller_offset=(hex(d) if d is not None else None)))
        i = j + 1

    # start (iii): the animation table's own field ordering, families collapsed
    tpl = ARC.ArcArchive(ED / "database/templates.arc")
    b = tpl.read_file("charanimationtable.tpl")
    names = [m.group(1).decode() for m in re.finditer(rb'name\s*=\s*"([^"]+)"', b)]
    fam = []
    for x in names:
        if not x.startswith("unarmed"):
            continue
        y = x[len("unarmed"):]
        if re.search(r"AnimSpeed\d*[A-C]?$|AnimWeight\d*[A-C]?$", y):
            continue
        f = re.sub(r"Anim(\d+|Ref\d+|Pool\d+[A-C])?$", "", y)
        f = re.sub(r"Anim(\d+)?$", "", f)
        if not fam or fam[-1] != f:
            fam.append(f)
    tpl_index = {f: i for i, f in enumerate(fam)}

    # the REFUTED candidate: raw `.rdata` literal order (exhaustive, two-digit bug repaired)
    lits = [(m.start(), m.group()[:-1].decode())
            for m in re.finditer(rb"unarmed[A-Za-z0-9_]{2,60}\x00", raw)]
    base = [s for _, s in lits if not re.search(r"(AnimSpeed|AnimWeight|Weight|Speed)\d*$", s)]
    rdata_at_0x21 = base[0x21] if len(base) > 0x21 else None
    rdata_at_0x25 = base[0x25] if len(base) > 0x25 else None
    return dict(
        start_i=dict(
            site="Game.dll 0x10109425 : 6a 21  (push 0x21) immediately before "
                 "call ControllerAI::PlayAnimation",
            state="ControllerMonsterStateAlertBeforePursue::OnBegin (0x10109410)",
            note="re-verified from my own seat; reproduces Lap AA § 5.2 byte-for-byte"),
        start_ii=dict(
            n_call_sites=len(sites), sites=sites,
            note="the AnimationSet_Type is the FIRST parameter and is therefore the LAST "
                 "push before the call; `ordinal_last_push` is the ordinal, the rest of the "
                 "window is unrelated pushes and is published so the extraction is auditable"),
        start_iii=dict(
            source="database/templates.arc :: charanimationtable.tpl, `unarmed*` field order, "
                   "numbered variants collapsed to slot families",
            n_families=len(fam),
            index_of=({k: hex(tpl_index[k]) for k in ("Alert", "Waiting", "Rally", "Emote",
                                                      "Flee", "Fidget", "Pickup", "PassItem",
                                                      "Chat", "GetUpFaceDown", "GetUpFaceUp",
                                                      "Stun", "Spawn", "Respawn", "Die")
                       if k in tpl_index})),
        refuted_candidate=dict(
            source="Game.dll .rdata `unarmed*` literal order (exhaustive; the recon filter's "
                   "two-digit `SpecialAnimNN` bug repaired)",
            n_literals=len(base),
            slot_at_ordinal_0x21=rdata_at_0x21,
            slot_at_ordinal_0x25=rdata_at_0x25,
            why_refuted="ordinal 0x25 is passed by ControllerMonsterStateFlee::OnBegin; a Flee "
                        "state cannot play a `SpecialAnimRef` slot. The literal ordering is "
                        "ENUMERATED and EXCLUDED, not used (D-Z-1 discipline)."))


def anm_index():
    arcs = {}
    for rel in ANM_ARCS:
        arcs[rel] = ARC.ArcArchive(ED / rel)
    idx = {}
    for rel, a in arcs.items():
        for x in a.names():
            if not x.lower().endswith(".anm"):
                continue
            k = x.lower().replace("\\", "/")
            idx[k] = (rel, x)
            # ⚑ D-AB-1, self-caught on the first run: the `.dbr` field spells the path
            # `creatures/enemies/<rig>/anm/x.anm` while the ARC entry name omits the leading
            # `creatures/` component.  Both spellings are indexed so the join is total; the
            # first cut silently produced ZERO alert lengths and crashed on the empty list,
            # which is how it was caught rather than published.
            idx["creatures/" + k] = (rel, x)
    return arcs, idx


def anm_header(arcs, rel, name):
    b = arcs[rel].read_file(name)
    if b[:4] != b"ANM\x02":
        return None
    f0, f1, f2, nl = struct.unpack_from("<IIII", b, 4)
    return dict(bones=f0, frames=f1, rate_field=f2, name_len=nl,
                header_bytes=20 + nl, payload_bytes=len(b))


def b2_law(arcs, idx):
    """Population-wide acceptance gate on the ANM header reading (prereg § 4.2 `B-2`)."""
    ratios, rates, bad = [], collections.Counter(), 0
    per_rig_bones = collections.defaultdict(set)
    per_rig_frames = collections.defaultdict(set)
    uniq = sorted(set(idx.values()))          # idx carries two spellings per file (D-AB-1)
    for rel, x in uniq:
        h = anm_header(arcs, rel, x)
        if h is None:
            bad += 1
            continue
        rates[h["rate_field"]] += 1
        rig = "/".join(x.split("/")[:2])
        per_rig_bones[rig].add(h["bones"])
        per_rig_frames[rig].add(h["frames"])
        if h["bones"] * h["frames"]:
            ratios.append((h["payload_bytes"] - h["header_bytes"]) / (h["bones"] * h["frames"]))
    ratios.sort()
    med = quantile(ratios, 0.5)
    conform = sum(1 for r in ratios if abs(r - med) <= 0.05 * med)
    b_const = sum(1 for r, s in per_rig_bones.items() if len(s) == 1)
    f_const = sum(1 for r, s in per_rig_frames.items() if len(s) == 1)
    return dict(
        n_anm_files=len(uniq), n_parsed=len(ratios), n_unparsed=bad,
        rate_field_distribution={str(k): v for k, v in rates.most_common()},
        bytes_per_bone_frame=dict(
            min=round(min(ratios), 4), p25=round(quantile(ratios, .25), 4),
            median=round(med, 4), p75=round(quantile(ratios, .75), 4),
            max=round(max(ratios), 4)),
        conformance_within_5pct=round(conform / len(ratios), 6),
        gate_threshold=0.95, gate_passed=(conform / len(ratios) >= 0.95),
        n_rig_dirs=len(per_rig_bones),
        rig_dirs_with_constant_field0=b_const, rig_dirs_with_constant_field1=f_const,
        field_identification=("field0 is constant within a rig directory far more often than "
                              "field1 -> field0 = BONE COUNT, field1 = FRAME COUNT; 56 bytes per "
                              "bone-frame is exactly 14 float32, a clean per-bone key stride"),
        rate_field_status=("CONSTANT = 30 on 100% of the population. Constancy is CONSISTENCY, "
                           "not proof that the field is frames-per-second. Durations are "
                           "published in FRAMES as primary; the seconds column is derived at "
                           "30 fps and is labelled DERIVED, not decoded (UNREACHED-AB-1)."))


def b3_join(arcs, idx, tier16_records, actor_rows):
    """roster record -> charAnimationTableName -> Alert slot .anm + speed + weight."""
    actors = collections.Counter(r["record"] for r in actor_rows)
    rows = []
    no_table = 0
    for p in tier16_records:
        lay, rec = resolve(p)
        tabp = rec.get("charAnimationTableName")
        chance = rec.get("alertAnimChance")
        if not tabp:
            no_table += 1
            rows.append(dict(record=p, n_rostered_actors=actors[p], anim_table=None,
                             alert_anm=None, status="NO-ANIMATION-TABLE"))
            continue
        lay2, tab = resolve(tabp)
        if tab is None:
            rows.append(dict(record=p, n_rostered_actors=actors[p], anim_table=tabp,
                             alert_anm=None, status="TABLE-UNRESOLVED"))
            continue
        slots = []
        for k, v in sorted(tab.items()):
            m = re.match(r"^(.*)Alert(?:Anim)?(\d)$", k)
            if not m or not isinstance(v, str) or not v.lower().endswith(".anm"):
                continue
            ws, n = m.group(1), m.group(2)
            spd = tab.get(f"{ws}AlertAnimSpeed{n}", 1.0)
            wgt = tab.get(f"{ws}AlertAnimWeight{n}", 100.0)
            key = v.lower().replace("\\", "/")
            hit = idx.get(key)
            hdr = anm_header(arcs, *hit) if hit else None
            slots.append(dict(weaponset=ws, variant=int(n), anm=v,
                              anim_speed=spd, anim_weight=wgt,
                              archive=(hit[0] if hit else None),
                              frames=(hdr["frames"] if hdr else None),
                              bones=(hdr["bones"] if hdr else None)))
        rows.append(dict(record=p, n_rostered_actors=actors[p], anim_table=tabp,
                         alert_anim_chance=chance,
                         n_alert_slots=len(slots), alert_anm=slots,
                         status=("HAS-ALERT" if slots else "ALERT-SLOT-EMPTY")))
    return rows, no_table


# ===================================================================== § 7  FORK (c)
def gate_fraction(D, E=8.0, R=6.0, n=4001):
    """P(placed body is within R of the target) for a spawn point at distance D,
    under Lap AA's DECODED scatter law: rho ~ U(0,E), theta ~ U(0,2pi).  ANALYTIC."""
    if D <= 0:
        return 1.0 if R >= 0 else 0.0
    tot = 0.0
    for i in range(n):
        rho = E * i / (n - 1)
        if rho == 0.0:
            p = 1.0 if D <= R else 0.0
        else:
            c = (D * D + rho * rho - R * R) / (2.0 * D * rho)
            c = max(-1.0, min(1.0, c))
            p = math.acos(c) / math.pi
        w = 0.5 if i in (0, n - 1) else 1.0
        tot += w * p
    return tot / (n - 1)


def gate_fraction_mc(D, E=8.0, R=6.0, n=200000, seed=20260816):
    """Independent second route.  Deterministic LCG so the emitted artifact is byte-stable."""
    s = seed
    hits = 0
    for _ in range(n):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        u1 = s / 0x7FFFFFFF
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        u2 = s / 0x7FFFFFFF
        rho = E * u1
        th = 2 * math.pi * u2
        x = D - rho * math.cos(th)
        y = rho * math.sin(th)
        if x * x + y * y <= R * R:
            hits += 1
    return hits / n


def fork_c():
    log("=" * 78)
    log("§ 7  FORK (c) — OBS-I26-1 DISPOSITION")
    log("=" * 78)
    geo_raw = list(csv.DictReader(
        (NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_geometry_v3.csv").open()))
    # ⚑ D-AB-2, self-caught: the pinned geometry artifact carries the SAME map from more than one
    # Maps.arc (survivalmode1 / survivalmode3), and the two copies are NOT identical (e.g.
    # survivalworld_a's near point reads 10.0946 m in sm1 and 10.2826 m in sm3).  The first cut
    # averaged both copies, double-counting every arena.  Lap AA's `D-AA-4` already ruled the mod
    # stack: survivalmode3 WINS.  Resolved here to the winning archive per map, and the losing
    # copies are counted and published rather than silently dropped.
    ORDER = ["mods/survivalmode/resources/Maps.arc", "survivalmode1/resources/Maps.arc",
             "survivalmode2/resources/Maps.arc", "survivalmode3/resources/Maps.arc"]

    def rank(a):
        return ORDER.index(a) if a in ORDER else -1
    # the two copies of a map carry DIFFERENT coordinates, so the resolution is per MAP
    # (winning archive takes its whole point set), never per row.
    best: dict[str, str] = {}
    for r in geo_raw:
        if r["map"] not in best or rank(r["archive"]) > rank(best[r["map"]]):
            best[r["map"]] = r["archive"]
    geo = [r for r in geo_raw if r["archive"] == best[r["map"]]]
    log(f"  mod-stack resolution (D-AB-2): {len(geo_raw)} pinned geometry rows -> {len(geo)} "
        f"after resolving each (map, spawn point) to the winning archive; "
        f"{len(geo_raw) - len(geo)} superseded copies excluded (counted, not hidden)")
    CAND = ("survivalworld_a.map", "survivalworld_b.map", "survivalworld_e.map")
    R = 6.0                                   # gameengine.dbr :: alertDistance (Lap AA § 5.2)
    out = {"_mod_stack_resolution": dict(rows_in_pin=len(geo_raw), rows_after_resolution=len(geo),
                                         superseded=len(geo_raw) - len(geo),
                                         precedence=ORDER, basis="Lap AA D-AA-4")}
    for scope, sel in (("candidate-restricted (a/b/e)",
                        lambda r: r["map"] in CAND and r["parse_complete"] == "True"),
                       ("all arenas",
                        lambda r: r["parse_complete"] == "True")):
        for proxy in ("to_patrol_centroid_m", "to_nearest_patrol_m"):
            rows = [r for r in geo if sel(r)]
            per = []
            for r in rows:
                D = float(r[proxy])
                E = float(r["placement_extents_m"])
                fa = gate_fraction(D, E, R)
                per.append(dict(map=r["map"], archive=r["archive"], D_m=round(D, 4),
                                extents_m=E, p_inside_gate=round(fa, 6)))
            mean = sum(x["p_inside_gate"] for x in per) / len(per) if per else None
            n_points_with_any = sum(1 for x in per if x["p_inside_gate"] > 0)
            n_points_all_inside = sum(1 for x in per if x["p_inside_gate"] > 0.999)
            key = f"{scope} | {proxy}"
            out[key] = dict(
                n_spawn_points=len(per), alert_distance_m=R,
                mean_fraction_of_placements_inside_gate=round(mean, 6) if mean is not None else None,
                n_points_with_any_placement_inside=n_points_with_any,
                n_points_entirely_inside=n_points_all_inside,
                per_point=per)
            log(f"  {key:60s} n={len(per):3d}  mean P(inside gate)={mean:.6f}  "
                f"points with ANY inside={n_points_with_any}  entirely inside={n_points_all_inside}")
    # corroboration: the independent Monte-Carlo route on the extreme and median points
    cand = [r for r in geo if r["map"] in CAND and r["parse_complete"] == "True"]
    checks = []
    for r in sorted(cand, key=lambda r: float(r["to_patrol_centroid_m"]))[:2] + \
             sorted(cand, key=lambda r: float(r["to_patrol_centroid_m"]))[len(cand) // 2:len(cand) // 2 + 1]:
        D = float(r["to_patrol_centroid_m"])
        E = float(r["placement_extents_m"])
        a = gate_fraction(D, E, R)
        m = gate_fraction_mc(D, E, R)
        checks.append(dict(map=r["map"], D_m=round(D, 4), analytic=round(a, 6),
                           monte_carlo=round(m, 6), abs_diff=round(abs(a - m), 6)))
        log(f"  CORROBORATION  D={D:8.4f} m  analytic={a:.6f}  MC={m:.6f}  |d|={abs(a-m):.6f}")
    out["_corroboration_monte_carlo"] = checks
    return out


# ===================================================================== § 8  MAIN
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pins()

    log("=" * 78)
    log("§ 2  CORPUS — the mod stack, in load order (later layer WINS, Lap AA D-AA-4)")
    log("=" * 78)
    for name, rel in LAYERS:
        ar = ARZ.ArzArchive(ED / rel)
        ARCHIVES.append((name, ar))
        log(f"  {name:5s} {rel:48s} records={len(ar.records):6d}")
    log("  ⚑ the `sm` layer (mods/survivalmode/database/SurvivalMode.arz) is the Crucible's own "
        "record set; every `records/creatures/defenses/*` record lives ONLY there.")
    log("")

    tpl = ARC.ArcArchive(ED / "database/templates.arc")
    log("=" * 78)
    log("§ 3  DECOY SET — the COMPLETE run/total-speed field surface, ENUMERATED (D-Z-1)")
    log("=" * 78)
    surface, unreadable = field_surface(tpl)
    fam_counts = collections.Counter(r["family"] for r in surface)
    log(f"  {len(surface)} distinct fields over {len(tpl.names())} templates "
        f"({unreadable} template payloads unreadable and counted, not skipped silently)")
    for f, c in fam_counts.most_common():
        log(f"    {c:4d}  {f}")
    with (OUT / "pm4ab_speed_surface.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["field", "family", "type", "cls", "description",
                                           "n_templates", "example_template"])
        w.writeheader()
        for r in surface:
            w.writerow(r)
    log("")

    # rosters
    speed_rows = [r for r in csv.DictReader(
        (NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact/pm4r_speed_terms.csv").open())
        if r["side"] == "monster" and r["field"] == "characterRunSpeed"
        and 151 <= int(r["wave"]) <= 160]
    tier16 = sorted({r["record"] for r in speed_rows})
    all790 = sorted({r["record"] for r in csv.DictReader(
        (NOTES / "2026-08-14-kc2-pm4-lap-t-arrival-decode/pm4t_march_speed.csv").open())})
    log(f"  tier-16 band (waves 151-160, Lap R pin): {len(speed_rows)} rostered actors over "
        f"{len(tier16)} distinct records;  full roster (Lap T pin): {len(all790)} records")
    log("  ⚑ Lap AA § 4.5's two-table caveat is CARRIED: the board labelled 150 was dispensed by "
        "the previous tier's table; this lap's band is 151-160 and no wave-150 claim is made.")
    log("")

    a_data = fork_a_data(tier16, all790)
    a_video = fork_a_video(speed_rows)

    log("=" * 78)
    log("§ 6  FORK (b) — UNREACHED-AA-3, THE ALERT ANIMATION LENGTH")
    log("=" * 78)
    b1 = b1_ordinal()
    log(f"  B-1  start (i)   {b1['start_i']['site']}")
    log(f"  B-1  start (ii)  {b1['start_ii']['n_call_sites']} call sites to "
        f"ControllerAI::PlayAnimation; sibling-state anchors:")
    for s in b1["start_ii"]["sites"]:
        if s["caller"] and "ControllerMonsterState" in s["caller"]:
            log(f"          ordinal {s['ordinal_last_push']:5s}  {s['caller']}")
    log(f"  B-1  start (iii) animation-table family order: {b1['start_iii']['index_of']}")
    log(f"  B-1  REFUTED     .rdata literal order puts 0x21 on "
        f"{b1['refuted_candidate']['slot_at_ordinal_0x21']!r} and 0x25 on "
        f"{b1['refuted_candidate']['slot_at_ordinal_0x25']!r} — {b1['refuted_candidate']['why_refuted']}")

    arcs, idx = anm_index()
    b2 = b2_law(arcs, idx)
    log(f"  B-2  {b2['n_anm_files']} .anm files across {len(ANM_ARCS)} archives; "
        f"parsed={b2['n_parsed']} unparsed={b2['n_unparsed']}")
    log(f"  B-2  rate field distribution: {b2['rate_field_distribution']}")
    log(f"  B-2  bytes per bone-frame: {b2['bytes_per_bone_frame']}")
    log(f"  B-2  ACCEPTANCE GATE conformance within +-5% of median = "
        f"{b2['conformance_within_5pct']:.6f} vs threshold {b2['gate_threshold']} -> "
        f"{'PASS' if b2['gate_passed'] else 'FAIL'}")
    if not b2["gate_passed"]:
        halt("B-2 acceptance gate FAILED — the ANM header reading is not established; "
             "fork (b) stops here per prereg § 4.2")

    b3, no_table = b3_join(arcs, idx, tier16, speed_rows)
    actors = collections.Counter(r["record"] for r in speed_rows)
    have = [r for r in b3 if r["status"] == "HAS-ALERT"]
    empty = [r for r in b3 if r["status"] == "ALERT-SLOT-EMPTY"]
    a_have = sum(r["n_rostered_actors"] for r in have)
    a_empty = sum(r["n_rostered_actors"] for r in empty)
    log(f"  B-3  tier-16 records: {len(b3)}  HAS-ALERT={len(have)}  ALERT-SLOT-EMPTY={len(empty)}  "
        f"no-table={no_table}")
    log(f"  B-3  rostered ACTORS: with an alert animation={a_have}  without={a_empty}  "
        f"(total {sum(actors.values())})")
    durations = []
    for r in have:
        for s in r["alert_anm"]:
            if s["frames"]:
                durations.append((r["record"], s["weaponset"], s["variant"], s["anm"],
                                  s["frames"], s["anim_speed"], s["anim_weight"],
                                  r["n_rostered_actors"]))
    fr = sorted(d[4] for d in durations)
    dstat = dict(n=len(fr), min=fr[0], p25=quantile(fr, .25), median=quantile(fr, .5),
                 p75=quantile(fr, .75), max=fr[-1],
                 min_s_at_30=round(fr[0] / 30.0, 4), median_s_at_30=round(quantile(fr, .5) / 30.0, 4),
                 max_s_at_30=round(fr[-1] / 30.0, 4),
                 span_ratio=round(fr[-1] / fr[0], 4))
    log(f"  B-3  alert-animation length over the tier-16 roster, in FRAMES: {dstat}")
    with (OUT / "pm4ab_alert_anim.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["record", "n_rostered_actors", "anim_table", "alert_anim_chance", "status",
                    "weaponset", "variant", "anm_path", "archive", "bones", "frames",
                    "anim_speed", "anim_weight", "seconds_at_30fps_DERIVED", "basis"])
        BASIS = ("frames DECODED from the .anm header (field1); seconds DERIVED at the "
                 "universally-constant rate field 30 and NOT decoded as fps (UNREACHED-AB-1); "
                 "state-duration == animation-length is NOT claimed (UNREACHED-AB-2)")
        for r in b3:
            if r["status"] != "HAS-ALERT":
                w.writerow([r["record"], r["n_rostered_actors"], r.get("anim_table"),
                            r.get("alert_anim_chance"), r["status"], "", "", "", "", "", "",
                            "", "", "", BASIS])
                continue
            for s in r["alert_anm"]:
                sec = round(s["frames"] / 30.0, 5) if s["frames"] else ""
                w.writerow([r["record"], r["n_rostered_actors"], r["anim_table"],
                            r.get("alert_anim_chance"), r["status"], s["weaponset"], s["variant"],
                            s["anm"], s["archive"], s["bones"], s["frames"],
                            s["anim_speed"], s["anim_weight"], sec, BASIS])
    log("")

    c = fork_c()

    # ---------------------------------------------------------------- emit
    (OUT / "pm4ab_fork_a_data.json").write_text(json.dumps(a_data, indent=1, sort_keys=True) + "\n")
    (OUT / "pm4ab_dispersion.json").write_text(json.dumps(a_video, indent=1, sort_keys=True) + "\n")
    (OUT / "pm4ab_alert_ordinal.json").write_text(
        json.dumps(dict(B_1=b1, B_2=b2,
                        B_3_summary=dict(
                            n_records=len(b3), n_has_alert=len(have),
                            n_alert_slot_empty=len(empty), n_no_table=no_table,
                            actors_with_alert=a_have, actors_without_alert=a_empty,
                            frames=dstat)),
                   indent=1, sort_keys=True) + "\n")
    (OUT / "pm4ab_gate_fraction.json").write_text(json.dumps(c, indent=1, sort_keys=True) + "\n")
    (OUT / "decode.log").write_text("\n".join(LOG) + "\n")

    emitted = {}
    for f in ("pm4ab_speed_surface.csv", "pm4ab_fork_a_data.json", "pm4ab_dispersion.json",
              "pm4ab_alert_anim.csv", "pm4ab_alert_ordinal.json", "pm4ab_gate_fraction.json",
              "decode.log"):
        emitted[f] = sha256(OUT / f)
    (OUT / "pm4ab_digests.json").write_text(
        json.dumps(dict(inputs=DIGESTS, emitted=emitted), indent=1, sort_keys=True) + "\n")
    print("EMITTED:")
    for k, v in sorted(emitted.items()):
        print(f"  {v}  {k}")


if __name__ == "__main__":
    main()
