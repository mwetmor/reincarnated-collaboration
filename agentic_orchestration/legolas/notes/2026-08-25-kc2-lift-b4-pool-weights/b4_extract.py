#!/usr/bin/env python3
"""KC2 LIFT RUN -- Lap B4: within-pool member roll weights, waves 150-160.

READ-ONLY on the vendor corpus and on the engine tree. Emits ONE tidy CSV + a pins file into
this lap directory. Nothing sealed is touched (K-7).

WHY THIS EXISTS
    elrond's B2-B8 curation finding A-B4-1: `pe6_crucible_wave_pools_v2.csv` carries only the
    BETWEEN-pool `pool_weight`; the WITHIN-pool composition is flattened to a pipe-joined name
    list, discarding per-slot weight / limit / player-level gate. A uniform fallback yields the
    right body COUNT and the wrong body MIX. This lap re-extracts the slot arrays from the
    Edition-III `.arz` corpus so the roll is derivable rather than inferred.

READER PROVENANCE (DR-1: derived, not retyped)
    `Ed.winner()` from `gamora_kc2_c1_closure_ed3_2026_08_08` is IMPORTED, not re-implemented --
    the same reader that produced band-A/band-B life. It applies the L-33/C-9 overlay law
    (WHOLE-RECORD REPLACEMENT across the 8 archives; never a field merge). A second reader is a
    second thing that can drift.

    ⚑ The per-slot INDEX-PAIRING law (L-65(e), re-verified by gamora's `pool_slot_proxies`
      docstring): `name<i>` pairs with `weight<i>` / `limit<i>` / `minPlayerLevel<i>` /
      `maxPlayerLevel<i>` / `alwaysSpawn<i>` / `levelVarianceEquation<i>` AT THE SAME INDEX.
      Never union a stem across indices. The champion family is a parallel, independently-indexed
      array (`nameChampion<i>` ...), NOT a continuation of the normal one.

ABSENCE POLICY (R-L2-3 honest-fail, pre-named)
    A slot whose optional field is not declared on the record emits an EXPLICIT EMPTY cell plus a
    `<field>_state` column reading ABSENT. Nothing is defaulted, nothing is inferred. The hole is
    countable by `grep`.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-25. Run KC2-LIFT, lap B4.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import pathlib
import re
import sys

ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
LAP = META / "agentic_orchestration/legolas/notes/2026-08-25-kc2-lift-b4-pool-weights"

sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))
sys.path.insert(0, str(ENGINE / "src"))

from gamora_kc2_c1_closure_ed3_2026_08_08 import E3  # noqa: E402

POOLS_CSV = ENGINE / "data" / "kc2" / "pe6_crucible_wave_pools_v2.csv"
WAVE_FIRST, WAVE_LAST = 150, 160

#: Template-declared slot ceiling (`database/templates/proxypool.tpl`, i = 1..15). We scan to 40
#: anyway so that a record exceeding the template's declared ceiling is DETECTED rather than
#: silently truncated -- and the overshoot band is reported.
TPL_MAX_SLOT = 15
SCAN_MAX_SLOT = 40

#: The 7 per-slot fields the template declares, per family. `name` is the slot's existence key.
SLOT_FIELDS = ["name", "weight", "levelVarianceEquation", "limit",
               "minPlayerLevel", "maxPlayerLevel", "alwaysSpawn"]
FAMILIES = [("normal", ""), ("champion", "Champion")]

#: Pool-grained scalars carried onto every slot row so the row is self-contained for the baton.
POOL_SCALARS = ["spawnMin", "spawnMax", "championMin", "championMax", "championChance",
                "proxyPoolEquation", "ignoreGameBalance"]


def sha256_of(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def scalar(v):
    """`.arz` fields decode to a bare value for count==1 and a list otherwise. Normalize."""
    if v is None:
        return None
    if isinstance(v, list):
        return v[0] if len(v) == 1 else v
    return v


def norm_path(v):
    v = scalar(v)
    if v is None:
        return None
    return str(v).lower().replace("\\", "/").strip()


def main():
    rows = list(csv.DictReader(open(POOLS_CSV)))
    sel = [r for r in rows if WAVE_FIRST <= int(r["global_wave"]) <= WAVE_LAST]

    # (pool_record -> the wave/spawn contexts it is referenced from, for the coverage table)
    refs = collections.defaultdict(list)
    for r in sel:
        refs[r["pool_record"]].append(r)
    pools = sorted(refs)

    out_rows = []
    diag = dict(
        pools_referenced=len(pools), pool_refs=len(sel),
        pools_resolved=0, pools_unresolved=[],
        slots_normal=0, slots_champion=0,
        overshoot=[], holes=[], archive_disagreement=[],
        template_mismatch=[],
    )
    field_state = collections.Counter()
    weightless = []

    for pool in pools:
        rec, arch = E3.winner(pool)
        if rec is None:
            diag["pools_unresolved"].append(pool)
            # HONEST-FAIL: the pool itself is unrecoverable. One countable row, all-NULL.
            out_rows.append(dict(
                pool_record=pool, pool_archive_winner="", pool_archive_csv=refs[pool][0]["pool_archive"],
                pool_template="", family="", slot_index="", member_record="",
                weight="", weight_state="POOL_UNRESOLVED",
                limit="", limit_state="POOL_UNRESOLVED",
                min_player_level="", min_player_level_state="POOL_UNRESOLVED",
                max_player_level="", max_player_level_state="POOL_UNRESOLVED",
                always_spawn="", always_spawn_state="POOL_UNRESOLVED",
                level_variance_equation="", level_variance_equation_state="POOL_UNRESOLVED",
                **{k: "" for k in ("spawn_min", "spawn_max", "champion_min", "champion_max",
                                   "champion_chance", "proxy_pool_equation", "ignore_game_balance")},
                slot_weight_share="", family_weight_total="",
                waves_referencing="|".join(sorted({r["global_wave"] for r in refs[pool]}, key=int)),
                pool_kinds="|".join(sorted({r["pool_kind"] for r in refs[pool]})),
            ))
            continue
        diag["pools_resolved"] += 1

        csv_archs = {r["pool_archive"] for r in refs[pool]}
        if arch not in csv_archs:
            diag["archive_disagreement"].append((pool, arch, sorted(csv_archs)))

        tpl = norm_path(rec.get("templateName"))
        if tpl != "database/templates/proxypool.tpl":
            diag["template_mismatch"].append((pool, tpl))

        sc = {k: scalar(rec.get(k)) for k in POOL_SCALARS}

        for family, suf in FAMILIES:
            present = [i for i in range(1, SCAN_MAX_SLOT + 1)
                       if rec.get(f"name{suf}{i}") is not None]
            if not present:
                continue
            if max(present) > TPL_MAX_SLOT:
                diag["overshoot"].append((pool, family, max(present)))
            if present != list(range(1, len(present) + 1)):
                diag["holes"].append((pool, family, present))

            wsum = 0
            slot_w = {}
            for i in present:
                w = scalar(rec.get(f"weight{suf}{i}"))
                slot_w[i] = w
                if isinstance(w, (int, float)):
                    wsum += w
                else:
                    weightless.append((pool, family, i))

            for i in present:
                vals = {}
                for f in SLOT_FIELDS:
                    key = f"{f}{suf}{i}"
                    raw = rec.get(key)
                    if raw is None:
                        vals[f] = ("", "ABSENT")
                        field_state[(family, f, "ABSENT")] += 1
                    else:
                        v = norm_path(raw) if f in ("name", "levelVarianceEquation") else scalar(raw)
                        vals[f] = (v, "PRESENT")
                        field_state[(family, f, "PRESENT")] += 1

                w = slot_w[i]
                share = (w / wsum) if (isinstance(w, (int, float)) and wsum) else ""
                out_rows.append(dict(
                    pool_record=pool,
                    pool_archive_winner=arch,
                    pool_archive_csv="|".join(sorted(csv_archs)),
                    pool_template=tpl,
                    family=family,
                    slot_index=i,
                    member_record=vals["name"][0],
                    weight=vals["weight"][0], weight_state=vals["weight"][1],
                    limit=vals["limit"][0], limit_state=vals["limit"][1],
                    min_player_level=vals["minPlayerLevel"][0],
                    min_player_level_state=vals["minPlayerLevel"][1],
                    max_player_level=vals["maxPlayerLevel"][0],
                    max_player_level_state=vals["maxPlayerLevel"][1],
                    always_spawn=vals["alwaysSpawn"][0], always_spawn_state=vals["alwaysSpawn"][1],
                    level_variance_equation=vals["levelVarianceEquation"][0],
                    level_variance_equation_state=vals["levelVarianceEquation"][1],
                    spawn_min=sc["spawnMin"], spawn_max=sc["spawnMax"],
                    champion_min=sc["championMin"], champion_max=sc["championMax"],
                    champion_chance=sc["championChance"],
                    proxy_pool_equation=norm_path(sc["proxyPoolEquation"]),
                    ignore_game_balance="" if sc["ignoreGameBalance"] is None else sc["ignoreGameBalance"],
                    slot_weight_share=("%.6f" % share) if share != "" else "",
                    family_weight_total=wsum,
                    waves_referencing="|".join(sorted({r["global_wave"] for r in refs[pool]}, key=int)),
                    pool_kinds="|".join(sorted({r["pool_kind"] for r in refs[pool]})),
                ))
                if family == "normal":
                    diag["slots_normal"] += 1
                else:
                    diag["slots_champion"] += 1

    cols = list(out_rows[0].keys())
    outp = LAP / "b4_pool_members_w150_160.csv"
    with open(outp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)

    diag["rows_emitted"] = len(out_rows)
    diag["slots_weightless"] = weightless
    diag["field_state"] = {f"{fam}.{f}<i>={st}": n for (fam, f, st), n in sorted(field_state.items())}
    (LAP / "b4_diagnostics.json").write_text(json.dumps(diag, indent=2, default=str))

    pins = {}
    for tag, p in [
        ("pools_csv", POOLS_CSV),
        ("arz_base", VENDOR / "database/database.arz"),
        ("arz_gdx1", VENDOR / "gdx1/database/GDX1.arz"),
        ("arz_gdx2", VENDOR / "gdx2/database/GDX2.arz"),
        ("arz_gdx3", VENDOR / "gdx3/database/GDX3.arz"),
        ("arz_sm_mod", VENDOR / "mods/survivalmode/database/SurvivalMode.arz"),
        ("arz_sm1", VENDOR / "survivalmode1/database/SurvivalMode1.arz"),
        ("arz_sm2", VENDOR / "survivalmode2/database/SurvivalMode2.arz"),
        ("arz_sm3", VENDOR / "survivalmode3/database/SurvivalMode3.arz"),
        ("templates_arc", VENDOR / "database/templates.arc"),
        ("reader_c1_closure", ENGINE / "src/reincarnated/simulation/scripts/gamora_kc2_c1_closure_ed3_2026_08_08.py"),
        ("reader_arz_adapter", META / "agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py"),
        ("reader_arc", META / "agentic_orchestration/research/scripts/gd_arc_reader_2026_07_26.py"),
        ("tpl_proxypool", LAP / "tpl_proxypool.txt"),
        ("tpl_proxypoolequation", LAP / "tpl_proxypoolequation.txt"),
        ("out_pool_members", outp),
    ]:
        pins[tag] = dict(path=str(p), sha256=sha256_of(p), bytes=p.stat().st_size)
    (LAP / "pins.json").write_text(json.dumps(pins, indent=2))

    print(json.dumps({k: v for k, v in diag.items() if k != "field_state"}, indent=2, default=str))
    print("\nFIELD STATE")
    for k, v in diag["field_state"].items():
        print(f"  {k:52s} {v}")
    print("\nwrote", outp)


if __name__ == "__main__":
    main()
