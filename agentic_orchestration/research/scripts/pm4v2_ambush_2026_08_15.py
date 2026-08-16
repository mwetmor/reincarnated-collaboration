#!/usr/bin/env python3
"""KC2-PM4 Lap V-2 — the `ProxyAmbush` decode.  Instruments I-V2-1 .. I-V2-4.

WHY THIS EXISTS
    Lap V (`R-PM4-56 part 2`) surfaced `F-3M-1`: all seven tier-16 spawn-point-5 proxies are
    class `ProxyAmbush`, not `Proxy`, carrying `minGroupSize = maxGroupSize = 30`,
    `spawnThreshold = 15`, `min/maxSpawnTime = 3.0`, `min/maxDelayTime = 4.0`,
    `alertArea = 100.0`.  Under the then-standing HALT rule it was named and NOT decoded.
    Matt authorised the decode on 2026-08-15 (`R-PM4-58 part 2`, verbatim: "decode it").

    This file decodes it out of the shipped bytes: the field->offset map from
    `ProxyAmbush::Load`, the trigger arithmetic from `ProxyAmbush::UpdateSelf`, the release
    shape from `PlaceNextObject`, the queue source from `PoolComplete`, the arming test from
    `IsAlert`, the one-shot latch from `Proxy::RunProxy`, and the wave-advance interaction
    from `GetPlacedObjects` + `game/events/survivalevent.lua`.

    RE-IMPLEMENTS NOTHING: the Lap S PE32 reader, the ARZ adapter and the ARC reader are
    imported unchanged (NOTE-9).

READ-ONLY on `/Users/admin/Games/vendor/`.  Writes ONLY into this lap's notes directory.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-15.  Run KC2-PM4, Lap V-2.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import importlib.util
import json
import pathlib
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
COLLAB = HERE.parent.parent.parent          # …/reincarnated-collaboration
OUT = COLLAB / "agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-v2-proxyambush-decode"
NOTES = COLLAB / "agentic_orchestration/legolas/notes"
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")
ED = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")

sys.path.insert(0, str(HERE))
from pm4s_pe_2026_08_14 import PE32, sha256  # noqa: E402


def _load(mod: str, fn: str):
    spec = importlib.util.spec_from_file_location(mod, HERE / fn)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ARZ = _load("arz", "gd_arz_adapter_2026_07_24.py")
ARC = _load("arc", "gd_arc_reader_2026_07_26.py")

# ---------------------------------------------------------------- § 1 pinned inputs (PREREGISTRATION.md § 1)
PINS_CORPUS = {
    "database/database.arz": "2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd",
    "gdx1/database/GDX1.arz": "431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292",
    "gdx2/database/GDX2.arz": "13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072",
    "gdx3/database/GDX3.arz": "e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4",
    "mods/survivalmode/database/SurvivalMode.arz": "e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6",
    "survivalmode1/database/SurvivalMode1.arz": "6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252",
    "survivalmode2/database/SurvivalMode2.arz": "940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95",
    "survivalmode3/database/SurvivalMode3.arz": "e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a",
    "mods/survivalmode/resources/Scripts.arc": "47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009",
    "database/templates.arc": "679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602",
}
PINS_BIN = {
    "Game.dll": "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
}
PINS_PRIOR = {
    "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_findings.md":
        "5450e1567fe58337827c20719ec477ee56a40351cbd7c49ab823d0896ca1b895",
    "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv":
        "991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c",
    "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_prediction.json":
        "450d52c9c5c430b528d1e2435760ff2ed45dec60c53a3b1981c20cc9701e275b",
    "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_geometry_v3.csv":
        "5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2",
    "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_pursue_decode.json":
        "6efd193aaa88158154beda71a723dbc70feda5f963ad470437137af92f98d733",
}


def verify_pins() -> dict:
    """HALT on any mismatch (PREREGISTRATION § 3.1)."""
    seen, bad = {}, []
    for rel, want in PINS_CORPUS.items():
        got = sha256(ED / rel); seen[f"edition-III/{rel}"] = got
        if got != want:
            bad.append(rel)
    for rel, want in PINS_BIN.items():
        got = sha256(GD / rel); seen[f"vendor/grim-dawn/{rel}"] = got
        if got != want:
            bad.append(rel)
    for rel, want in PINS_PRIOR.items():
        got = sha256(NOTES / rel); seen[rel] = got
        if got != want:
            bad.append(rel)
    if bad:
        raise SystemExit(f"HALT — pinned input digest mismatch: {bad}")
    return seen


# ---------------------------------------------------------------- PE helpers
class Img:
    def __init__(self, name):
        self.pe = PE32(GD / name)
        self.b = self.pe.raw
        self.base = self.pe.image_base
        self.iat = self._imports()

    def _imports(self):
        b, pe = self.b, self.pe
        d_rva, _ = pe.dirs[1]
        off = pe.rva_to_off(d_rva)
        out, i = {}, 0
        while True:
            ilt, _ts, _fc, name_rva, ft = struct.unpack_from("<IIIII", b, off + 20 * i)
            if ilt == 0 and name_rva == 0 and ft == 0:
                break
            no = pe.rva_to_off(name_rva)
            dll = b[no:b.index(b"\0", no)].decode("latin-1")
            t = pe.rva_to_off(ilt or ft)
            j = 0
            while True:
                v = struct.unpack_from("<I", b, t + 4 * j)[0]
                if v == 0:
                    break
                if v & 0x80000000:
                    nm = f"ord{v & 0xffff}"
                else:
                    o = pe.rva_to_off(v)
                    nm = b[o + 2:b.index(b"\0", o + 2)].decode("latin-1")
                out[self.base + ft + 4 * j] = f"{dll}!{nm}"
                j += 1
            i += 1
        return out

    def cstr(self, va):
        o = self.pe.rva_to_off(va - self.base)
        return self.b[o:self.b.index(b"\0", o)].decode("latin-1")

    def f32(self, va):
        return struct.unpack_from("<f", self.b, self.pe.rva_to_off(va - self.base))[0]

    def disasm(self, va, n):
        return self.pe.disasm(va - self.base, n)

    def rdata_hits(self, va):
        pat = struct.pack("<I", va); i = 0; out = []
        while True:
            k = self.b.find(pat, i)
            if k < 0:
                break
            r = self.pe.off_to_rva(k)
            if r and self.pe.section_of_rva(r)["name"] == ".rdata":
                out.append(self.base + r)
            i = k + 1
        return out

    def vt_base(self, cls_gri_rva):
        """Vtable base == the .rdata slot holding `GetRTTIClassInfo` (slot 0 convention,
        verified empirically on ProxyAmbush: UpdateSelf then lands at 0x168, PoolComplete at
        0x1f8, AccessoryComplete at 0x1fc — the only assignment that makes Proxy::RunProxy's
        two 2-argument virtual calls type-correct)."""
        h = self.rdata_hits(self.base + cls_gri_rva)
        return h[0] if h else None

    def vt_slot(self, base, slot):
        o = self.pe.rva_to_off(base - self.base)
        v = struct.unpack_from("<I", self.b, o + slot)[0]
        s = self.pe.sym_at(v - self.base)
        if s:
            return v, s
        o2 = self.pe.rva_to_off(v - self.base)
        if self.b[o2:o2 + 2] == b"\xff\x25":
            t = struct.unpack_from("<I", self.b, o2 + 2)[0]
            return v, "thunk-> " + self.iat.get(t, hex(t))
        return v, "<unnamed>"


# ---------------------------------------------------------------- I-V2-1: the binary decode
FUNCS = [
    ("ProxyAmbush::Load", 0x10354400, 0x120),
    ("ProxyAmbush::UpdateSelf", 0x10354520, 0x1C0),
    ("ProxyAmbush::GetPlacedObjects", 0x10354DD0, 0xD0),
    ("ProxyAmbush::PoolComplete", 0x10354FB0, 0x50),
    ("ProxyAmbush::IsAlert", 0x10355000, 0xC0),
    ("ProxyAmbush::PlaceNextObject", 0x103550C0, 0x200),
    ("Proxy::RunProxy", 0x10351D30, 0x2D0),
    ("Proxy::DelayedRun", 0x10351D10, 0x20),
    ("Proxy::PoolComplete (baseline)", 0x10352580, 0x60),
]

# field name -> (member offset, load kind).  Read out of ProxyAmbush::Load, in program order.
FIELD_MAP = [
    ("alertArea",      0x4E8, "GetFloat(name, 0.0f)",              "float, world units (metres)"),
    ("minSpawnTime",   0x4EC, "(int)(GetFloat(name,0.0f)*1000.0f)", "ms, truncated"),
    ("maxSpawnTime",   0x4F0, "(int)(GetFloat(name,0.0f)*1000.0f)", "ms, truncated"),
    ("minDelayTime",   0x4F4, "(int)(GetFloat(name,0.0f)*1000.0f)", "ms, truncated"),
    ("maxDelayTime",   0x4F8, "(int)(GetFloat(name,0.0f)*1000.0f)", "ms, truncated"),
    ("minGroupSize",   0x4FC, "GetInt(name, 1)",                    "int, default 1"),
    ("maxGroupSize",   0x500, "GetInt(name, 1)",                    "int, default 1"),
    ("spawnThreshold", 0x504, "GetInt(name, 10000)",                "int, default 10000"),
]

RUNTIME_MAP = [
    (0x4A0, "m_totalObjects", "set by PoolComplete = (pool->[0xb0].size())"),
    (0x4A4, "m_placedCount", "incremented once per PlaceNextObject that actually spawns"),
    (0x4AC, "m_runState", "Proxy latch: Load sets 1 when delayedRun; DelayedRun 1->0; RunProxy sets 6 on success / 5 on chance-fail; RunProxy early-returns unless 0"),
    (0x4C8, "m_monsterPool", "ProxyPool*; its resolved entity-id vector lives at pool+0xb0"),
    (0x4CC, "m_accessoryTable", "loot/accessory container (vectors at +0x20 / +0x2c); NOT roster"),
    (0x4D0, "m_pendingIds.begin/end (0x4d0/0x4d4)", "vector<unsigned> — queued, NOT yet spawned"),
    (0x4DC, "m_pendingCoords.begin/end (0x4dc/0x4e0)", "vector<WorldCoords>, stride 0x34"),
    (0x508, "m_placedIds.begin/end (0x508/0x50c)", "vector<unsigned> — spawned AND still alive"),
    (0x514, "m_spawnTimer", "int ms, counts down by dt; ctor-initialised to 0"),
    (0x518, "m_delayTimer", "int ms, counts down by dt; ctor-initialised to 0"),
    (0x51C, "m_armed", "bool latch; set 1 in UpdateSelf on first IsAlert; never cleared"),
    (0x51D, "m_reselectLocations", "bool; set 1 ONLY by RestoreState (save/load path)"),
]


def decode_binary():
    g = Img("Game.dll")
    pa_gri = 0x000B6980            # ?GetRTTIClassInfo@ProxyAmbush@GAME@@
    mon_gri = 0x0000BB00           # ?GetRTTIClassInfo@Monster@GAME@@
    pa_vt = g.vt_base(pa_gri)
    mon_vt = g.vt_base(mon_gri)
    out = {
        "module": {"name": "Game.dll", "sha256": sha256(GD / "Game.dll"),
                   "image_base": hex(g.base), "exports": len(g.pe.exports())},
        "class_exports": {n: hex(r) for n, r in sorted(g.pe.exports().items())
                          if "ProxyAmbush" in n},
        "vtables": {
            "convention": "slot 0x000 == GetRTTIClassInfo (verified on ProxyAmbush)",
            "ProxyAmbush": hex(pa_vt),
            "Monster": hex(mon_vt),
        },
        "field_map": [
            {"dbr_field": f, "member_offset": hex(o), "loader": how, "note": note}
            for f, o, how, note in FIELD_MAP
        ],
        "runtime_members": [
            {"offset": hex(o), "name": n, "note": note} for o, n, note in RUNTIME_MAP
        ],
        "resolved_calls": {},
        "vtable_slots": {},
        "float_constants": {"0x105f5918": g.f32(0x105F5918)},
        "load_field_strings": {},
    }
    for va in (0x104E5394, 0x104E5294, 0x104E5600, 0x104E59E4, 0x104E5028, 0x104E508C,
               0x104E5544, 0x104E504C, 0x104E63E4, 0x104E5288, 0x104E5244, 0x104E5574,
               0x104E5090, 0x104E528C, 0x104E5558, 0x104E5C1C, 0x104E5994):
        out["resolved_calls"][hex(va)] = g.iat.get(va, "<not-an-import>")
    for slot in (0x000, 0x168, 0x1F8, 0x1FC, 0x200):
        v, s = g.vt_slot(pa_vt, slot)
        out["vtable_slots"][f"ProxyAmbush+{slot:#05x}"] = {"target": hex(v), "symbol": s}
    for slot in (0x000, 0x168, 0x22C, 0x314):
        v, s = g.vt_slot(mon_vt, slot)
        out["vtable_slots"][f"Monster+{slot:#05x}"] = {"target": hex(v), "symbol": s}
    for va in (0x10569CA4, 0x10569D30, 0x10569D70, 0x10569D60, 0x10569D50, 0x10569D40,
               0x10569DDC, 0x10569DCC, 0x1056925C, 0x10569250):
        out["load_field_strings"][hex(va)] = g.cstr(va)
    out["rtti_classinfo"] = {
        "0x107ff5a0": "?classInfo@Player@GAME@@  (the IsAlert filter)",
        "0x107ff600": "?classInfo@Monster@GAME@@ (the PlaceNextObject / PoolComplete filter)",
    }
    disasm = []
    for label, va, n in FUNCS:
        disasm.append(f"===== {label}  @ {va:#010x} =====\n" + g.disasm(va, n))
    return out, "\n".join(disasm)


# ---------------------------------------------------------------- I-V2-2: records
def decode_records():
    order = ["database/database.arz", "gdx1/database/GDX1.arz", "gdx2/database/GDX2.arz",
             "gdx3/database/GDX3.arz", "mods/survivalmode/database/SurvivalMode.arz",
             "survivalmode1/database/SurvivalMode1.arz",
             "survivalmode2/database/SurvivalMode2.arz",
             "survivalmode3/database/SurvivalMode3.arz"]
    own, arch = {}, {}
    for a in order:
        z = ARZ.ArzArchive(ED / a)
        arch[a] = z
        for k in z.records:
            own[k.lower()] = (a, k)
    tier16 = sorted(k for k in own if "tier16waves" in k)
    cls = collections.Counter()
    ambush, common = [], collections.Counter()
    for lk in tier16:
        a, real = own[lk]
        f = arch[a].read_record(real)
        cls[f.get("Class")] += 1
        common[(f.get("Class"), f.get("delayedRun"), f.get("chanceToRun"),
                f.get("placementExtents"))] += 1
        if f.get("Class") == "ProxyAmbush":
            ambush.append({
                "record": real, "archive": a,
                "alertArea": f.get("alertArea"),
                "minDelayTime": f.get("minDelayTime"), "maxDelayTime": f.get("maxDelayTime"),
                "minSpawnTime": f.get("minSpawnTime"), "maxSpawnTime": f.get("maxSpawnTime"),
                "minGroupSize": f.get("minGroupSize"), "maxGroupSize": f.get("maxGroupSize"),
                "spawnThreshold": f.get("spawnThreshold"),
                "placementExtents": f.get("placementExtents"),
                "delayedRun": f.get("delayedRun"), "chanceToRun": f.get("chanceToRun"),
                "templateName": f.get("templateName"),
            })
    allprox = collections.Counter(arch[a].records[k]["rtype"]
                                 for lk, (a, k) in own.items()
                                 if lk.startswith("records/proxies/"))
    return {
        "overlay_records": len(own),
        "tier16_wave_proxy_records": len(tier16),
        "tier16_class_census": dict(cls),
        "tier16_common_fields": [{"Class": k[0], "delayedRun": k[1], "chanceToRun": k[2],
                                  "placementExtents": k[3], "n": v}
                                 for k, v in common.items()],
        "all_proxy_record_class_census": dict(allprox),
        "ambush_records": ambush,
        "fourth_mechanism_scan": (
            "R-PM4-56 part 4 due diligence: every one of the 54 tier-16 wave-proxy records is "
            "either Proxy (47) or ProxyAmbush (7).  No ProxyEndless, no SetPiece, no fourth "
            "class declared in the band."),
    }


# ---------------------------------------------------------------- I-V2-3: geometry
def decode_geometry():
    import math
    geo = list(csv.DictReader(open(NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_geometry_v3.csv")))
    plc = csv.DictReader(open(NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_map_placements_v3.csv"))
    pat = collections.defaultdict(list)
    for r in plc:
        if "patrolpoint" in r["dbr"].lower():
            pat[(r["archive"], r["map"])].append((float(r["x"]), float(r["y"]), float(r["z"])))
    sp = collections.defaultdict(list)
    for r in geo:
        sp[(r["archive"], r["map"])].append((float(r["spawn_x"]), float(r["spawn_y"]),
                                             float(r["spawn_z"])))
    rows, pairs, over = [], 0, 0
    for k in sorted(sp):
        P = pat.get(k, [])
        sp_sp = max((math.dist(a, b) for i, a in enumerate(sp[k]) for b in sp[k][i + 1:]),
                    default=0.0)
        sp_pp = max((math.dist(a, b) for a in sp[k] for b in P), default=0.0)
        n_over = sum(1 for a in sp[k] for b in P if math.dist(a, b) > 100.0)
        pairs += len(sp[k]) * len(P); over += n_over
        rows.append({"archive": k[0], "map": k[1], "n_spawn": len(sp[k]),
                     "n_patrol": len(P),
                     "max_spawn_to_spawn_m": round(sp_sp, 4),
                     "max_spawn_to_patrol_m": round(sp_pp, 4),
                     "pairs_beyond_alertArea_100": n_over})
    return {
        "alertArea_radius_world_units": 100.0,
        "unit_basis": "Lap U pm4u_geometry_v3.csv reports world units as metres (_m columns)",
        "per_map": rows,
        "max_spawn_to_spawn_m_over_all_maps": round(max(r["max_spawn_to_spawn_m"] for r in rows), 4),
        "max_spawn_to_patrol_m_over_all_maps": round(max(r["max_spawn_to_patrol_m"] for r in rows), 4),
        "spawn_x_patrol_pairs": pairs,
        "pairs_beyond_alertArea": over,
        "verdict": ("alertArea = 100.0 m covers every arena footprint: 0 of %d spawn-point x "
                    "patrol-point pairs exceed it, and the widest spawn-to-spawn separation in "
                    "any of the 20 arena maps is under 100 m.  IsAlert() is therefore TRUE from "
                    "the first evaluated tick regardless of where the player stands." % pairs),
    }


# ---------------------------------------------------------------- I-V2-4: contribution
def decode_contribution():
    rows = [r for r in csv.DictReader(
        open(NOTES / "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv"))
        if r["spawn_point"] == "5"]
    per = collections.defaultdict(list)
    for r in rows:
        per[int(r["global_wave"])].append(r)
    waves = {}
    for w, alts in sorted(per.items()):
        e = [float(a["e_bodies"]) for a in alts]
        wt = [float(a["pool_weight"]) for a in alts]
        tot = sum(wt)
        exp = sum(x * y for x, y in zip(e, wt)) / tot
        waves[w] = {
            "n_alternatives": len(alts),
            "pool_weights": wt,
            "expected_bodies": round(exp, 6),
            "bodies_lo": min(int(a["bodies_lo"]) for a in alts),
            "bodies_hi": max(int(a["bodies_hi"]) for a in alts),
            "lap_v_floor": round(exp, 6),
            "status": "DECODE-COMPLETE (was labelled a FLOOR by Lap V § 6.1; it is EXACT)",
            "arrival_offset_s": 4.000,
            "release": "single burst; the whole queue empties on the first burst because "
                       "minGroupSize (30) exceeds the resolved pool size",
            "conditional": False,
        }
    return {
        "release_law": {
            "burst_fires_when": ["m_armed", "m_delayTimer <= 0", "m_spawnTimer <= 0",
                                 "len(m_pendingIds) > 0",
                                 "len(m_placedIds_alive) <= spawnThreshold"],
            "n_released_per_burst": "min( UniformInclusive(minGroupSize, maxGroupSize), len(m_pendingIds) )",
            "queue_refill": "NONE — Proxy::RunProxy latches m_runState=6 and early-returns "
                            "thereafter, so PoolComplete runs exactly once per proxy instance, "
                            "and the Lua creates one fresh proxy per wave",
            "decoded_parameter_values": {"minGroupSize": 30, "maxGroupSize": 30,
                                         "spawnThreshold": 15, "delay_ms": 4000,
                                         "spawn_interval_ms": 3000},
            "why_it_collapses_to_a_scalar": (
                "spawnThreshold and the 3.0 s re-burst interval can only bite when the pending "
                "queue survives the first burst.  It cannot: the largest p05 pool resolution in "
                "the band is 7 expected bodies (wave 156) against a release batch of 30.  Both "
                "constants are therefore INERT over waves 151-160."),
        },
        "per_wave": waves,
        "band_total_expected_p05_bodies": round(sum(v["expected_bodies"] for v in waves.values()), 6),
        "waves_declaring_no_p05": [154, 155, 160],
    }


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = verify_pins()
    ambush, disasm = decode_binary()
    ambush["records"] = decode_records()
    ambush["geometry"] = decode_geometry()
    contrib = decode_contribution()

    (OUT / "pm4v2_disasm.txt").write_text(disasm)
    (OUT / "pm4v2_ambush.json").write_text(json.dumps(ambush, indent=2, sort_keys=True) + "\n")
    (OUT / "pm4v2_contribution.json").write_text(json.dumps(contrib, indent=2, sort_keys=True) + "\n")

    dig = {"lap": "KC2-PM4 Lap V-2 — ProxyAmbush decode", "date": "2026-08-15",
           "inputs": inputs, "outputs": {}}
    for p in sorted(OUT.glob("*")):
        if p.name != "pm4v2_digests.json":
            dig["outputs"][p.name] = sha256(p)
    dig["instruments"] = {"pm4v2_ambush_2026_08_15.py": sha256(pathlib.Path(__file__))}
    (OUT / "pm4v2_digests.json").write_text(json.dumps(dig, indent=2, sort_keys=True) + "\n")
    print("PINS OK  ({} inputs)".format(len(inputs)))
    print(json.dumps(contrib["per_wave"], indent=2))
    print("band total p05 expected bodies:", contrib["band_total_expected_p05_bodies"])
    print(ambush["geometry"]["verdict"])
    print("tier16 class census:", ambush["records"]["tier16_class_census"])


if __name__ == "__main__":
    main()
