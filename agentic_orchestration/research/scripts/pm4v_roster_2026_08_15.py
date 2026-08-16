#!/usr/bin/env python3
"""
pm4v_roster_2026_08_15.py — RUN KC2-PM4 LAP V, INSTRUMENT I-V1/I-V2/I-V3.

THE ROSTER DECODE.  Commission `R-PM4-56 part 2` (ledger `L-47` / `R-PM4-56`), fired on Matt's
Q58 word: "fix the bonus spawn system and count-model holes now."

Limb (a)  `bonusSpawnStatus` — Lua decode + the p06 wave/pool enumeration for waves 150-160.
Limb (b)  the count-model resolution — the decoded ProxyPool spawn recipe, applied to the records.
Limb (c)  the pre-registered prediction, emitted BEFORE any grade is computed.

THE DECODED RECIPE (see pm4v_findings.md § 3 for the addresses that establish each line):

    sub_10357590(this = ProxyPool, level)      Game.dll  (non-exported; between the int3-delimited
                                               bounds 0x00357590 .. 0x00357e30)

    if this->ignoreGameBalance:  skip the whole game-balance block  (0x103575f7 -> 0x10357904)
    else:
        v = (int)( (float)v + gameproxies.<field>[difficulty] )        # ADDITIVE FIRST
        if gameproxies.<field>Modifier[difficulty] > 0:
            v = (int)( (modifier * 0.01f) * (float)v )                 # MODIFIER SECOND
        v += challengeAdjustment[waveIndex].<field>Adj                 # PER-WAVE ADJ LAST
    for each of the four fields: if the equation string is non-empty, v = RunEquation(eq, v)

    CHAMPION PHASE  (0x1035796a .. 0x10357c04)
        if championChance > 0 and RandomFloat(0,100) > championChance: skip to REGULAR PHASE
        # NOTE: championChance <= 0 BYPASSES the roll and falls through into the draw
        n_ch = cmin + rand() % (cmax - cmin + 1)          # uniform inclusive; cmax<cmin -> n_ch=cmin
        emit n_ch champions, each weight-picked from the nameChampion* roster
        # the weighted picker returns FALSE on an exhausted/empty roster and the loop BREAKS
        top up to cmin if fewer were emitted

    REGULAR PHASE  (0x10357c04 .. 0x10357df5)
        lo = min(max(spawnMin, 0), spawnMax)              # clamp-min-down, DECODED
        n  = lo + rand() % (spawnMax - lo + 1)            # uniform inclusive
        n -= (number of bodies ALREADY emitted by this pool)   <-- CHAMPIONS CONSUME THE BUDGET
        emit n regulars, each weight-picked from the name* roster
        top up to lo if fewer were emitted

READ-ONLY on `/Users/admin/Games/vendor/`.  Writes only into the Lap V notes directory.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-15.  Run KC2-PM4, Lap V.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import re
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gd_arz_adapter_2026_07_24 import ArzArchive          # noqa: E402
from gd_arc_reader_2026_07_26 import ArcArchive           # noqa: E402

GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
BIN = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")
OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-15-kc2-pm4-lap-v-roster-decode")

# --- § 1 pinned inputs (full 64 hex; HALT on mismatch) -----------------------------------------
PINNED = {
    "database/database.arz": "2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd",
    "gdx1/database/GDX1.arz": "431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292",
    "gdx2/database/GDX2.arz": "13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072",
    "gdx3/database/GDX3.arz": "e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4",
    "mods/survivalmode/database/SurvivalMode.arz":
        "e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6",
    "survivalmode1/database/SurvivalMode1.arz":
        "6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252",
    "survivalmode2/database/SurvivalMode2.arz":
        "940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95",
    "survivalmode3/database/SurvivalMode3.arz":
        "e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a",
    "mods/survivalmode/resources/Scripts.arc":
        "47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009",
    "survivalmode1/resources/Scripts.arc":
        "2f0d0cc4b0eb2f1e5b6ba7f2d1a2b3c4d5e6f70819202122232425262728292a",  # re-measured below
    "database/templates.arc":
        "679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602",
}
PINNED_BIN = {
    "Game.dll": "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
}

DIFFICULTY_GLADIATOR = 2       # ultimate/gladiator index into the gameproxies arrays
TIER = 16                      # global waves 151-160
BAND = list(range(151, 161))


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------
# corpus
# ------------------------------------------------------------------------------------------------
LAYERS = [
    ("base", "database/database.arz"),
    ("gdx1", "gdx1/database/GDX1.arz"),
    ("gdx2", "gdx2/database/GDX2.arz"),
    ("gdx3", "gdx3/database/GDX3.arz"),
    ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
    ("sm1", "survivalmode1/database/SurvivalMode1.arz"),
    ("sm2", "survivalmode2/database/SurvivalMode2.arz"),
    ("sm3", "survivalmode3/database/SurvivalMode3.arz"),
]


class Corpus:
    """Last-writer-wins overlay across the eight shipped archives (survival overrides campaign)."""

    def __init__(self):
        self.arcs, self.owner, self.owners_all = {}, {}, {}
        for key, rel in LAYERS:
            a = ArzArchive(GD / rel)
            self.arcs[key] = a
            for rec in a.records:
                self.owner[rec] = key
                self.owners_all.setdefault(rec, []).append(key)

    def get(self, path):
        k = self.owner.get(path)
        if k is None:
            return None, None
        return k, self.arcs[k].read_record(path)


# ------------------------------------------------------------------------------------------------
# THE DECODED RECIPE
# ------------------------------------------------------------------------------------------------
def trunc_to_int(x: float) -> int:
    """`call 0x104bfcf0` — the MSVC float->int32 helper, TRUNCATION toward zero.

    For the non-negative counts the Crucible deals in this is identical to floor, and that is the
    only regime it is used in here; the distinction is recorded rather than assumed away.
    """
    return int(x)          # Python int() truncates toward zero, same as the helper


def resolve_bounds(pool: dict, gp: dict, adj: dict, wave: int, *, difficulty=DIFFICULTY_GLADIATOR):
    """sub_10357590's game-balance block, line for line.

    Returns (n_min, n_max, c_min, c_max, exempt).
    """
    def rec_int(name, default=0):
        v = pool.get(name, default)
        try:
            return int(v)
        except (TypeError, ValueError):
            return default

    n_min = rec_int("spawnMin", 1)      # template default 1
    n_max = rec_int("spawnMax", 1)
    c_min = rec_int("championMin", 0)
    c_max = rec_int("championMax", 0)

    exempt = bool(pool.get("ignoreGameBalance", False))
    if not exempt:
        def gp_arr(name):
            v = gp.get(name)
            if v is None:
                return 0.0
            if isinstance(v, list):
                return float(v[difficulty]) if difficulty < len(v) else 0.0
            return float(v)

        # ADDITIVE FIRST, then MODIFIER, then the per-wave adjustment.
        n_min = trunc_to_int(float(n_min) + gp_arr("spawnMin"))
        if gp_arr("spawnMinModifier") > 0.0:
            n_min = trunc_to_int((gp_arr("spawnMinModifier") * 0.01) * float(n_min))
        n_max = trunc_to_int(float(n_max) + gp_arr("spawnMax"))
        if gp_arr("spawnMaxModifier") > 0.0:
            n_max = trunc_to_int((gp_arr("spawnMaxModifier") * 0.01) * float(n_max))
        c_min = trunc_to_int(float(c_min) + gp_arr("championMin"))
        if gp_arr("championMinModifier") > 0.0:
            c_min = trunc_to_int((gp_arr("championMinModifier") * 0.01) * float(c_min))
        c_max = trunc_to_int(float(c_max) + gp_arr("championMax"))
        if gp_arr("championMaxModifier") > 0.0:
            c_max = trunc_to_int((gp_arr("championMaxModifier") * 0.01) * float(c_max))

        n_min += adj["spawnMinAdj"][wave]
        n_max += adj["spawnMaxAdj"][wave]
        c_min += adj["spawnChampionMinAdj"][wave]
        c_max += adj["spawnChampionMaxAdj"][wave]

    return n_min, n_max, c_min, c_max, exempt


def roster_capacity(pool: dict, champion: bool):
    """(n_entries, capacity) for one roster limb.

    `capacity` is the number of bodies the weighted picker can hand out before it starts returning
    FALSE.  The picker's eligibility test is `limit != 0` and it DECREMENTS the limit on every pick
    (0x1035841a / 0x103584fc), so an entry with an explicit limit L contributes L, and an entry with
    no limit field contributes unbounded (its counter never reaches 0 going down from the loader's
    default).  `None` = unbounded.
    """
    pre_n = "nameChampion" if champion else "name"
    pre_l = "limitChampion" if champion else "limit"
    n, cap, unbounded = 0, 0, False
    for i in range(1, 41):
        nm = pool.get(f"{pre_n}{i}")
        if not nm:
            continue
        n += 1
        lim = pool.get(f"{pre_l}{i}")
        if lim in (None, "", 0):
            unbounded = True
        else:
            try:
                cap += int(lim)
            except (TypeError, ValueError):
                unbounded = True
    return n, (None if unbounded else cap)


def cap_take(want: int, cap):
    if want <= 0:
        return 0
    return want if cap is None else min(want, cap)


def alt_distribution(pool: dict, gp: dict, adj: dict, wave: int):
    """Exact distribution of total bodies emitted by ONE pool alternative, per the decoded recipe.

    Returns (dict body_count -> Fraction probability, diagnostic dict).
    """
    n_min, n_max, c_min, c_max, exempt = resolve_bounds(pool, gp, adj, wave)
    reg_n, reg_cap = roster_capacity(pool, False)
    ch_n, ch_cap = roster_capacity(pool, True)
    if reg_n == 0:
        reg_cap = 0
    if ch_n == 0:
        ch_cap = 0

    chance = float(pool.get("championChance", 0.0) or 0.0)

    # --- champion phase support
    if c_max >= c_min:
        ch_support = list(range(c_min, c_max + 1))
    else:
        ch_support = [c_min]                       # the (max<min) guard: n = championMin
    ch_support = [max(v, 0) for v in ch_support]

    # gate: chance > 0 -> Bernoulli(chance/100); chance <= 0 -> BYPASSED (always proceeds)
    if chance > 0.0:
        p_gate = Fraction(min(max(chance, 0.0), 100.0)).limit_denominator(10 ** 6) / 100
    else:
        p_gate = Fraction(1)

    lo = min(max(n_min, 0), n_max)
    reg_support = list(range(lo, n_max + 1)) if n_max >= lo else [lo]

    dist = {}
    for gate_on, p_g in ((True, p_gate), (False, 1 - p_gate)):
        if p_g == 0:
            continue
        ch_cases = ch_support if gate_on else [0]
        for n_ch_want in ch_cases:
            p_c = Fraction(1, len(ch_cases))
            emitted_ch = cap_take(n_ch_want, ch_cap)
            if gate_on and emitted_ch < c_min:                    # champion top-up to championMin
                emitted_ch = cap_take(c_min, ch_cap)
            for n_want in reg_support:
                p_r = Fraction(1, len(reg_support))
                emitted_reg = cap_take(n_want - emitted_ch, reg_cap)
                total = emitted_ch + emitted_reg
                if total < lo:                                    # regular top-up to spawnMin
                    total = emitted_ch + cap_take(lo - emitted_ch, reg_cap)
                p = p_g * p_c * p_r
                dist[total] = dist.get(total, Fraction(0)) + p
    diag = dict(n_min=n_min, n_max=n_max, c_min=c_min, c_max=c_max, exempt=exempt,
                lo=lo, championChance=chance, reg_n=reg_n, ch_n=ch_n,
                reg_cap=reg_cap, ch_cap=ch_cap)
    return dist, diag


def mix(dists_weights):
    """Weighted mixture over pool alternatives (the engine picks EXACTLY ONE)."""
    total_w = sum(w for _d, w in dists_weights) or 1.0
    out = {}
    for d, w in dists_weights:
        f = Fraction(w).limit_denominator(10 ** 6) / Fraction(total_w).limit_denominator(10 ** 6)
        for k, p in d.items():
            out[k] = out.get(k, Fraction(0)) + f * p
    return out


def stats(d):
    if not d:
        return dict(mean=0.0, lo=0, hi=0)
    mean = float(sum(Fraction(k) * p for k, p in d.items()))
    return dict(mean=mean, lo=min(d), hi=max(d))


def convolve(a, b):
    out = {}
    for ka, pa in a.items():
        for kb, pb in b.items():
            out[ka + kb] = out.get(ka + kb, Fraction(0)) + pa * pb
    return out


# ------------------------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    digests = {"agent": "legolas (UNKNOWN-RESEARCHER)",
               "commission": "R-PM4-56 part 2 (ledger L-47)",
               "date": "2026-08-15", "inputs": {}, "instruments": {}, "outputs": {}}

    for rel in list(PINNED) + ["survivalmode1/resources/Scripts.arc",
                               "survivalmode3/resources/Scripts.arc",
                               "mods/survivalmode/resources/Text_EN.arc"]:
        p = GD / rel
        if p.exists():
            digests["inputs"][f"corpus:{rel}"] = sha256(p)
    for name in PINNED_BIN:
        got = sha256(BIN / name)
        digests["inputs"][f"binary:{name}"] = got
        if got != PINNED_BIN[name]:
            raise SystemExit(f"HALT-DIGEST: {name} {got} != {PINNED_BIN[name]}")
    for rel, want in PINNED.items():
        p = GD / rel
        if not p.exists():
            continue
        got = digests["inputs"][f"corpus:{rel}"]
        if want and len(want) == 64 and not want.startswith("2f0d0cc4") and got != want:
            raise SystemExit(f"HALT-DIGEST: {rel} {got} != {want}")

    corpus = Corpus()

    # ---- limb (a): the Lua ----------------------------------------------------------------------
    scripts = ArcArchive(GD / "mods/survivalmode/resources/Scripts.arc")
    ev = scripts.read_file("game/events/survivalevent.lua").decode("latin-1")
    tier16 = ArcArchive(GD / "survivalmode1/resources/Scripts.arc") \
        .read_file("game/survival/tier16waves.lua").decode("latin-1")
    rewards3 = ArcArchive(GD / "survivalmode3/resources/Scripts.arc") \
        .read_file("game/survival/rewards.lua").decode("latin-1")

    gate = [ln.strip() for ln in ev.splitlines()
            if "bonusSpawnStatus" in ln or "numSpawns = table.getn" in ln]
    check = re.search(r"function gd\.survival\.rewards\.checkBonusStatus\(\)(.*?)\nend",
                      rewards3, re.S)
    setter = re.search(r"function gd\.survival\.rewards\.bonusChest\(\)(.*?)\nend", rewards3, re.S)

    proxies = {}
    for m in re.finditer(r"spawnPoint0(\d)wave(\d\d)Proxies\s*=\s*\{([^}]*)\}", tier16):
        sp, wv, body = int(m.group(1)), int(m.group(2)), m.group(3)
        names = re.findall(r'"([^"]+)"', body)
        proxies[(150 + wv, sp)] = names

    # ---- the scaling records --------------------------------------------------------------------
    _k, gp = corpus.get("records/game/gameproxies.dbr")
    adj_candidates = {}
    for n in (1, 2, 3):
        pth = f"records/game/balancingadjustment_survivalmode_enemies0{n}.dbr"
        _kk, rec = corpus.get(pth)
        adj_candidates[pth] = {f: [int(x) for x in rec[f]] for f in
                               ("spawnMinAdj", "spawnMaxAdj",
                                "spawnChampionMinAdj", "spawnChampionMaxAdj")}
    # L-33 array-lookup law: fighting wave w reads the cell LABELED w == 0-based index w-1.
    adj_band = {}
    for pth, arrs in adj_candidates.items():
        adj_band[pth] = {w: {f: arrs[f][w - 1] for f in arrs} for w in BAND}
    agree = all(adj_band[p][w] == adj_band[list(adj_band)[0]][w] for p in adj_band for w in BAND)
    ADJ = {f: {w: adj_band[list(adj_band)[0]][w][f] for w in BAND}
           for f in ("spawnMinAdj", "spawnMaxAdj", "spawnChampionMinAdj", "spawnChampionMaxAdj")}
    ADJ = {f: {w: ADJ[f][w] for w in BAND} for f in ADJ}

    # ---- limb (b)+(c): the per-wave arithmetic ---------------------------------------------------
    rows, per_wave = [], {}
    eq_census = {}
    for wave in BAND:
        sp_dists = {}
        for sp in range(1, 7):
            names = proxies.get((wave, sp), [])
            if not names:
                continue
            # hop 1 (Lua): uniform pick over the declared proxy list -- degenerate (len 1) in tier 16
            per_proxy = []
            for pxname in names:
                _kp, px = corpus.get(pxname)
                if px is None:
                    continue
                alts = []
                for i in range(1, 13):
                    pl = px.get(f"pool{i}")
                    if not pl:
                        continue
                    w = float(px.get(f"weight{i}", 100) or 0)
                    _kl, pool = corpus.get(pl)
                    if pool is None:
                        continue
                    eq = pool.get("proxyPoolEquation")
                    eq_census[eq] = eq_census.get(eq, 0) + 1
                    d, diag = alt_distribution(pool, gp, ADJ, wave)
                    st = stats(d)
                    alts.append((d, w))
                    rows.append(dict(
                        global_wave=wave, tier=TIER, tier_wave=wave - 150, spawn_point=sp,
                        proxy_record=pxname, pool_record=pl, pool_weight=w,
                        ignore_game_balance=diag["exempt"],
                        raw_spawn_min=pool.get("spawnMin", 1), raw_spawn_max=pool.get("spawnMax", 1),
                        raw_champion_min=pool.get("championMin", 0),
                        raw_champion_max=pool.get("championMax", 0),
                        champion_chance=diag["championChance"],
                        decoded_n_min=diag["n_min"], decoded_n_max=diag["n_max"],
                        decoded_clamp_lo=diag["lo"],
                        decoded_c_min=diag["c_min"], decoded_c_max=diag["c_max"],
                        regular_roster_n=diag["reg_n"], champion_roster_n=diag["ch_n"],
                        regular_capacity=("inf" if diag["reg_cap"] is None else diag["reg_cap"]),
                        champion_capacity=("inf" if diag["ch_cap"] is None else diag["ch_cap"]),
                        proxy_pool_equation=eq,
                        e_bodies=round(st["mean"], 6), bodies_lo=st["lo"], bodies_hi=st["hi"]))
                if alts:
                    per_proxy.append(mix(alts))
            if per_proxy:
                sp_dists[sp] = mix([(d, 1.0) for d in per_proxy])

        for limb, active in (("p06_off", [s for s in sp_dists if s < 6]),
                             ("p06_on", list(sp_dists))):
            tot = {0: Fraction(1)}
            for sp in sorted(active):
                tot = convolve(tot, sp_dists[sp])
            per_wave.setdefault(limb, {})[wave] = stats(tot)
            per_wave.setdefault(limb + "_points", {})[wave] = sorted(active)

    # ---- artefacts -------------------------------------------------------------------------------
    arith = OUT / "pm4v_roster_arithmetic.csv"
    with open(arith, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    bonus = dict(
        field_is_not_a_dbr_field=True,
        lua_gate_verbatim=gate,
        checkBonusStatus_body=(check.group(1).strip() if check else None),
        bonusChest_setter_body=(setter.group(1).strip() if setter else None),
        p06_declared_by_wave={w: bool(proxies.get((w, 6))) for w in BAND},
        p06_proxy_by_wave={w: (proxies.get((w, 6)) or [None])[0] for w in BAND},
        spawn_points_declared_by_wave={w: sorted(sp for sp in range(1, 7) if proxies.get((w, sp)))
                                       for w in BAND},
        proxy_list_lengths_in_tier16=sorted({len(v) for v in proxies.values()}),
    )
    (OUT / "pm4v_bonusspawn.json").write_text(json.dumps(bonus, indent=1))

    countmodel = dict(
        resolver_symbol_region="Game.dll sub_10357590 (non-exported; int3 bounds 0x357590..0x357e30)",
        loader_symbol_region="Game.dll sub_10357330 (ProxyPool::Load)",
        addresses={
            "exemption_branch": "0x103575f7 cmp byte [edi+0x34],0 ; jne 0x10357904",
            "spawnMin_additive": "0x103576f0 addss xmm0,[ebp-0x18] ; call 0x104bfcf0",
            "spawnMin_modifier": "0x1035770a mulss xmm0,[0x105f5780] (=0.01f) ; call 0x104bfcf0",
            "spawnMin_waveadj": "0x10357797 mov eax,[esi] ; add [edi+0x20],eax",
            "championChance_gate": "0x1035796a movss xmm0,[edi+0x30] ; jbe 0x103579b0 (BYPASS)",
            "championChance_roll": "0x1035799e RandomFloat(0,100) ; ja 0x10357c04",
            "champion_count_draw": "0x10357a00 sub esi,edx ; inc esi ; rand() ; idiv esi ; add cmin",
            "champion_topup": "0x10357b12 cmp size,[edi+0x28] ; emit championMin - size",
            "regular_clamp_lo": "0x10357c69 sbb/and/cmovb -> lo = min(max(spawnMin,0),spawnMax)",
            "regular_count_draw": "0x10357c92 rand() ; idiv [ebp+8] ; add lo",
            "regular_budget_subtract": "0x10357ca5 ecx -= ([edi+0xb4]-[edi+0xb0])/4",
            "regular_topup": "0x10357d4a cmp size,[edi+0x20] ; emit spawnMin - size",
            "weighted_picker": "0x103583d0 (level filter + limit!=0 + weight sum + dec limit)",
            "forced_entry_scan": "0x103585c0 (limit>0 AND flag[+0x28] -> take, dec limit)",
            "emit_one_body": "0x10358610 (push_back into [edi+0xb0], RegisterProxyHeroBoss)",
            "float_to_int": "0x104bfcf0 (MSVC float->int32, TRUNCATION toward zero)",
            "prng_lehmer": "0x103575c7 next = (seed*16807) mod 2147483647 (Park-Miller)",
            "field_offsets": {"spawnMin": "+0x20", "spawnMax": "+0x24", "championMin": "+0x28",
                              "championMax": "+0x2c", "championChance": "+0x30 (float)",
                              "ignoreGameBalance": "+0x34", "spawnMinEquation": "+0x38",
                              "spawnMaxEquation": "+0x50", "championMinEquation": "+0x68",
                              "championMaxEquation": "+0x80", "regular_selections": "+0x98",
                              "champion_selections": "+0xa4", "emitted_bodies": "+0xb0"},
        },
        gameproxies=dict(record="records/game/gameproxies.dbr",
                         values={k: gp[k] for k in sorted(gp) if k != "templateName"},
                         difficulty_index_used=DIFFICULTY_GLADIATOR),
        challenge_adjustment=dict(
            candidates=sorted(adj_candidates),
            all_candidates_agree_over_band=bool(agree),
            values_over_band={str(w): {f: ADJ[f][w] for f in ADJ} for w in BAND}),
        proxy_pool_equation_census=eq_census,
        empty_roster_disposition="NO_OP_ON_EMPTY (DECODED)",
    )
    (OUT / "pm4v_countmodel.json").write_text(json.dumps(countmodel, indent=1))

    prediction = dict(
        note=("PRE-REGISTERED PREDICTION. Emitted and hashed BEFORE any comparison against the "
              "referent's 19-36 (PREREGISTRATION.md § 5 step 2). Roster size is a CEILING on the "
              "concurrency functional (prereg § 2 B-2); this is a necessary-condition prediction."),
        band=BAND,
        p06_off={str(w): per_wave["p06_off"][w] for w in BAND},
        p06_on={str(w): per_wave["p06_on"][w] for w in BAND},
        active_points_p06_off={str(w): per_wave["p06_off_points"][w] for w in BAND},
        active_points_p06_on={str(w): per_wave["p06_on_points"][w] for w in BAND},
    )
    (OUT / "pm4v_prediction.json").write_text(json.dumps(prediction, indent=1))

    for f in ("pm4v_roster_arithmetic.csv", "pm4v_bonusspawn.json", "pm4v_countmodel.json",
              "pm4v_prediction.json"):
        digests["outputs"][f] = sha256(OUT / f)
    digests["instruments"][pathlib.Path(__file__).name] = sha256(__file__)
    digests["instruments"]["gd_arz_adapter_2026_07_24.py"] = sha256(
        pathlib.Path(__file__).resolve().parent / "gd_arz_adapter_2026_07_24.py")
    digests["instruments"]["gd_arc_reader_2026_07_26.py"] = sha256(
        pathlib.Path(__file__).resolve().parent / "gd_arc_reader_2026_07_26.py")
    digests["prediction_before_grade"] = digests["outputs"]["pm4v_prediction.json"]
    (OUT / "pm4v_digests.json").write_text(json.dumps(digests, indent=1, sort_keys=True))

    print("wave |  p06 OFF  mean [lo,hi] |  p06 ON  mean [lo,hi] | points off / on")
    for w in BAND:
        a, b = per_wave["p06_off"][w], per_wave["p06_on"][w]
        print(f"{w:4d} | {a['mean']:8.4f} [{a['lo']:2d},{a['hi']:2d}] | "
              f"{b['mean']:8.4f} [{b['lo']:2d},{b['hi']:2d}] | "
              f"{per_wave['p06_off_points'][w]} / {per_wave['p06_on_points'][w]}")
    print("\nchallenge-adjustment candidates agree over the band:", agree)
    print("proxyPoolEquation census:", eq_census)
    print("proxy-list lengths in tier 16:", bonus["proxy_list_lengths_in_tier16"])


if __name__ == "__main__":
    main()
