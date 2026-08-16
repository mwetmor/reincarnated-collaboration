#!/usr/bin/env python3
"""KC2-PM4 · LAP AA — THE REFERENT'S SPAWN STRUCTURE.  Instrument I-AA-1.

WHY THIS EXISTS
    `R-PM4-67 part 7` commissioned a measured decode of how a Crucible wave's monster
    population ENTERS the board for waves 150-160: (a) WHERE bodies spawn, (b) WHEN they
    spawn, (c) what happens between spawn and engage.  Fight-recipe INPUT class.

    The residual it serves is THE ARRIVAL SCHEDULE (`R-PM4-67 part 1`): everything the sim
    has folded is DOWNSTREAM of whatever spaces arrivals out.  This file decodes the
    referent side out of the shipped bytes.

    RE-IMPLEMENTS NOTHING.  The project's `gd_arz_adapter_2026_07_24`, `gd_arc_reader_2026_07_26`
    and `pm4s_pe_2026_08_14.PE32` are imported unchanged (NOTE-9).  Prior-lap numbers are
    IMPORTED BY IDENTITY from pinned artifacts, never restated from prose (`R-PM4-67 part 2`,
    the D-CON-6 law).

READ-ONLY on `/Users/admin/Games/vendor/` and on every prior lap's notes.  Writes ONLY into
this lap's notes directory.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.  Run KC2-PM4, Lap AA.
Pre-registration: `.../2026-08-16-kc2-pm4-lap-aa-referent-spawn-structure/prereg.md`,
committed ALONE in `ba368773` before this file existed.
"""
from __future__ import annotations

import bisect
import csv
import hashlib
import importlib.util
import json
import pathlib
import re
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
COLLAB = HERE.parent.parent.parent
LAP = "2026-08-16-kc2-pm4-lap-aa-referent-spawn-structure"
OUT = COLLAB / "agentic_orchestration/legolas/notes" / LAP
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

LOG: list[str] = []


def log(s: str = "") -> None:
    LOG.append(s)


def halt(msg: str):
    raise SystemExit(f"HALT — {msg}")


# ===================================================================== § 1  PINS
# Prereg § 5 leg 1.  HALT on any mismatch.  Digests marked EXPECT are published
# by a prior lap and are asserted; digests marked RECORD are pinned here for the
# first time and are recorded, not asserted.

PIN_EXPECT = {
    # --- shipped corpus, published by Lap Z § 10.2 -------------------------------
    ED / "database/database.arz":
        "2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd",
    ED / "database/templates.arc":
        "679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602",
    ED / "mods/survivalmode/database/SurvivalMode.arz":
        "e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6",
    ED / "survivalmode1/database/SurvivalMode1.arz":
        "6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252",
    ED / "survivalmode2/database/SurvivalMode2.arz":
        "940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95",
    ED / "survivalmode3/database/SurvivalMode3.arz":
        "e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a",
    GD / "Game.dll":
        "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    GD / "Engine.dll":
        "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
    GD / "Grim Dawn.exe":
        "1a71e188ea3d7f83bec296e22acecf7cac71686c9c0c117d0eb03c9d7ada1ff4",
    # --- world assets, published by Lap S § 1 ------------------------------------
    ED / "survivalmode1/resources/Maps.arc":
        "2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237",
    ED / "survivalmode2/resources/Maps.arc":
        "cef96030be9bdc9be64bf187389aeccec6552ba1cfde30d1c63d716d2f6dbaec",
    ED / "survivalmode3/resources/Maps.arc":
        "94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911",
    # --- shipped Lua, banked verbatim by Lap S -----------------------------------
    NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance/evidence/survivalevent.lua":
        "8f1a434fd10b92fb0e3a9fc6293a2bfedca307f697243ec9f102e81f01a588fb",
    NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance/evidence/tier16waves.lua":
        "208abadefcb213d8227b61127a97a9e5fb4d5b4011150f713a81d4ecba8fd5d3",
    NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance/evidence/eventcontrol.lua":
        "cd2bf304d89555d3471e6b449e7e2d170350fc6dfe97726f43ab9b395224a2be",
    # --- prior-lap artifacts imported BY IDENTITY --------------------------------
    NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_geometry_v3.csv":
        "5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2",
}

PIN_RECORD = [
    ED / "mods/survivalmode/resources/Maps.arc",
    ED / "mods/survivalmode/resources/Scripts.arc",
    ED / "resources/Text_EN.arc",
    NOTES / "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv",
    NOTES / "2026-08-15-kc2-pm4-lap-v2-proxyambush-decode/pm4v2_ambush.json",
    NOTES / "2026-08-14-kc2-pm4-lap-n-crit-and-collision/pm4n_fct_events.csv",
    NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_pursue_decode.json",
    NOTES / "2026-08-16-kc2-pm4-lap-z-ring-operand/pm4z_findings.md",
    OUT / "prereg.md",
]


def verify_pins() -> dict:
    seen, bad = {}, []
    for p, want in PIN_EXPECT.items():
        got = sha256(p)
        seen[str(p)] = got
        if got != want:
            bad.append(f"{p}: got {got} want {want}")
    for p in PIN_RECORD:
        seen[str(p)] = sha256(p)
    if bad:
        halt("pinned input digest mismatch:\n  " + "\n  ".join(bad))
    log(f"[PINS] {len(PIN_EXPECT)} asserted EXACT, {len(PIN_RECORD)} recorded. No HALT.")
    return seen


# ===================================================================== § 2  PE helpers
class Img:
    def __init__(self, name: str):
        self.name = name
        self.pe = PE32(GD / name)
        self.b = self.pe.raw
        self.base = self.pe.image_base
        t = self.pe.sections[0]
        assert t["name"].startswith(".text"), t["name"]
        self.text = self.b[t["raddr"]: t["raddr"] + t["rsize"]]
        self.text_rva = t["vaddr"]
        self.ex = self.pe.exports()
        self._rvs = sorted(set(self.ex.values()))
        self._rev = {}
        for n, r in self.ex.items():
            self._rev.setdefault(r, n)
        self._iat = None

    def enclosing(self, rva: int):
        i = bisect.bisect_right(self._rvs, rva) - 1
        if i < 0:
            return (None, 0)
        return (self._rev[self._rvs[i]], rva - self._rvs[i])

    def cstr(self, va: int) -> str:
        o = self.pe.rva_to_off(va - self.base)
        return self.b[o: self.b.index(b"\0", o)].decode("latin-1")

    def f32(self, va: int):
        o = self.pe.rva_to_off(va - self.base)
        return struct.unpack_from("<f", self.b, o)[0], self.b[o:o + 4].hex()

    def iat(self) -> dict:
        if self._iat is not None:
            return self._iat
        b, pe = self.b, self.pe
        d_rva, _ = pe.dirs[1]
        off = pe.rva_to_off(d_rva)
        out, i = {}, 0
        while True:
            ilt, _ts, _fc, name_rva, ft = struct.unpack_from("<IIIII", b, off + 20 * i)
            if ilt == 0 and name_rva == 0 and ft == 0:
                break
            dll = b[pe.rva_to_off(name_rva):].split(b"\0")[0].decode()
            tbl, j = (ilt or ft), 0
            while True:
                (e,) = struct.unpack_from("<I", b, pe.rva_to_off(tbl) + 4 * j)
                if e == 0:
                    break
                va = self.base + ft + 4 * j
                nm = (f"ord{e & 0xFFFF}" if e & 0x80000000
                      else b[pe.rva_to_off(e) + 2:].split(b"\0")[0].decode("latin-1"))
                out[va] = f"{dll}!{nm}"
                j += 1
            i += 1
        self._iat = out
        return out

    def dis(self, rva: int, n: int = 0x200) -> str:
        return self.pe.disasm(rva, n)

    def dis3(self, rva: int, n: int, needle: str) -> str:
        """`D-Z-3` guard: decode from three independent starts and require the line
        containing `needle` to be byte-identical in all three.  HALT on disagreement."""
        got = []
        for back in (0x00, 0x10, 0x24):
            txt = self.dis(rva - back, n + back)
            hit = [l for l in txt.splitlines() if needle in l]
            got.append(tuple(hit))
        if not got[0]:
            halt(f"dis3: needle {needle!r} not found at {hex(rva)} in {self.name}")
        if not (got[0] == got[1] == got[2]):
            halt(f"dis3 DISAGREEMENT at {hex(rva)} on {needle!r}: {got}")
        return "\n".join(got[0])

    def imm_refs(self, imm: int):
        """Every .text site whose 4 little-endian bytes equal `imm`.  Used to ENUMERATE
        the reference set of a literal (`D-Z-1` guard) rather than take the first hit."""
        pat = re.escape(struct.pack("<I", imm))
        out = []
        for m in re.finditer(pat, self.text):
            rva = self.text_rva + m.start()
            sym, off = self.enclosing(rva)
            out.append(dict(va=hex(self.base + rva), prev_op="%02x" % self.text[m.start() - 1],
                            enclosing=sym, delta=hex(off)))
        return out

    def callers(self, target_rva: int):
        out = []
        for i in range(len(self.text) - 5):
            if self.text[i] == 0xE8:
                rel = struct.unpack_from("<i", self.text, i + 1)[0]
                if self.text_rva + i + 5 + rel == target_rva:
                    rva = self.text_rva + i
                    sym, off = self.enclosing(rva)
                    out.append(dict(va=hex(self.base + rva), enclosing=sym, delta=hex(off)))
        return out


# ===================================================================== § 3  FORK (d)  ARENA IDENTITY
ARENA_TAG_RE = re.compile(rb"tagSurvivalArena_\d\d")
MAP_ARCS = [
    "mods/survivalmode/resources/Maps.arc",
    "survivalmode1/resources/Maps.arc",
    "survivalmode2/resources/Maps.arc",
    "survivalmode3/resources/Maps.arc",
]


def fork_d(exe: Img) -> dict:
    log("\n===== FORK (d) — ARENA IDENTITY =========================================")

    # d.1 the referent's own on-screen area name, from a PINNED referent artifact.
    fct = NOTES / "2026-08-14-kc2-pm4-lap-n-crit-and-collision/pm4n_fct_events.csv"
    names, tiers = {}, {}
    with fct.open(newline="") as fh:
        for row in csv.DictReader(fh):
            t = row["text"].strip()
            if t.startswith("Crucible of the"):
                names[t] = names.get(t, 0) + 1
            if t in ("Aspirant", "Challenger", "Gladiator"):
                tiers[t] = tiers.get(t, 0) + 1
    log(f"[d.1] referent OCR area names   : {names}")
    log(f"[d.1] referent OCR difficulty   : {tiers}")

    # d.2 the shipped tag table (base game text arc)  — the FULL table, enumerated.
    tags = {}
    a = ARC.ArcArchive(str(ED / "resources/Text_EN.arc"))
    for n in a.names():
        if not n.endswith(".txt"):
            continue
        for line in a.read_file(n).decode("utf-8", errors="replace").splitlines():
            if line.startswith("tagSurvivalArena"):
                k, _, v = line.partition("=")
                tags[k.strip()] = (v.strip(), n)
    log(f"[d.2] tagSurvivalArena_* declared: {len(tags)}")
    for k in sorted(tags):
        log(f"        {k} = {tags[k][0]!r}   ({tags[k][1]})")

    # d.3 the decoy set — every shipped arena map, and which arena tags it carries.
    per_map = {}
    for arc in MAP_ARCS:
        ar = ARC.ArcArchive(str(ED / arc))
        for n in sorted(ar.names()):
            d = ar.read_file(n)
            found = sorted(set(m.group().decode() for m in ARENA_TAG_RE.finditer(d)))
            per_map.setdefault(n, {})[arc] = found
    log(f"[d.3] shipped arena maps (decoy set ENUMERATED): {len(per_map)}")
    for n in sorted(per_map):
        log(f"        {n:24s} {per_map[n]}")

    # d.4 the exe's two ordered arrays: the map list, and the selection dropdown.
    eb = exe.b
    m = re.search(rb"maps/survivalworld_[a-z]\.map", eb)
    seg = eb[m.start(): m.start() + 400]
    map_array = [x.decode() for x in re.findall(rb"maps/survivalworld_[a-z]\.map", seg)]
    m2 = re.search(rb"survivalMapDrop\x00tagSurvivalArenaRandom", eb)
    seg2 = eb[m2.start(): m2.start() + 400]
    drop_array = ["tagSurvivalArenaRandom"] + [
        x.decode() for x in re.findall(rb"tagSurvivalArena_\d\d", seg2)]
    log(f"[d.4] exe map array   ({len(map_array)}): {map_array}")
    log(f"[d.4] exe dropdown    ({len(drop_array)}): {drop_array}")

    # d.5 what the referent's name resolves to, and the surviving candidate set.
    ref_name = max(names, key=names.get) if names else None
    ref_tag = next((k for k, v in tags.items() if v[0] == ref_name), None)
    cands = sorted(n for n, per in per_map.items()
                   if any(ref_tag in v for v in per.values()))
    log(f"[d.5] referent name {ref_name!r} -> {ref_tag}")
    log(f"[d.5] maps carrying {ref_tag}: {cands}  (of {len(per_map)})")

    # d.6 is the tag->map binding reachable?  The selector lives in the exe's .text.
    sec = {s["name"]: s for s in exe.pe.sections}
    drm = ".bind" in sec
    log(f"[d.6] exe sections: {sorted(sec)}   .bind(DRM) present = {drm}")

    return dict(
        referent_area_name=ref_name, referent_area_name_frames=names,
        referent_difficulty_tier=max(tiers, key=tiers.get) if tiers else None,
        referent_difficulty_frames=tiers,
        referent_name_source=str(fct),
        tag_table={k: v[0] for k, v in tags.items()},
        tag_table_source="edition-III/resources/Text_EN.arc :: tags_uimain.txt",
        maps_and_tags=per_map,
        exe_map_array=map_array, exe_dropdown_array=drop_array,
        exe_dropdown_omits=sorted(set(tags) - set(drop_array) - {"tagSurvivalArenaRandom"}),
        referent_tag=ref_tag, candidate_maps=cands,
        n_shipped_maps=len(per_map),
        exe_sections=sorted(sec), exe_has_bind_section=drm,
    )


# ===================================================================== § 4  FORK (a)  WHERE
def fork_a(game: Img, eng: Img) -> dict:
    log("\n===== FORK (a) — WHERE ==================================================")

    # a.1 the three release-shaping fields, from `Proxy::Load`, with their literals.
    lo = game.ex["?Load@Proxy@GAME@@UAEXABVLoadTable@2@@Z"]
    txt = game.dis(lo, 0x300)
    fields = {}
    for line, memb, name_va, dflt in [
        ("placementExtents", 0x410, 0x10569268, 0x40200000),
        ("chanceToRun", 0x3E0, 0x1056925C, 0x00000000),
    ]:
        nm = game.cstr(name_va)
        if nm != line:
            halt(f"Proxy::Load literal mismatch: {nm!r} != {line!r}")
        fields[line] = dict(member=hex(memb), name_literal_va=hex(name_va),
                            loader_default=struct.unpack("<f", struct.pack("<I", dflt))[0])
    nm = game.cstr(0x10569250)
    if nm != "delayedRun":
        halt("delayedRun literal mismatch")
    fields["delayedRun"] = dict(member="+0x4ac (state latch <- 1)",
                                name_literal_va=hex(0x10569250), loader_default=False)
    game.dis3(0x35110E, 0x40, "[ebx + 0x410]")     # `D-Z-3` guard, three starts
    log("[a.1] Proxy::Load field->member map:")
    for k, v in fields.items():
        log(f"        {k:18s} {v}")

    # a.2 RunProxy -> SelectPoolLocations -> PoolComplete -> PlaceObjects.
    sel = game.ex["?SelectPoolLocations@Proxy@GAME@@IAEXABV?$vector@I@mem@@AAV?$vector@VWorldCoords@GAME@@@4@_N@Z"]
    stxt = game.dis(sel, 0x300)
    iat = game.iat()
    fill_va = next(va for va, nm in iat.items() if "FillPointSet" in nm)
    if "FillPointSet" not in iat[fill_va]:
        halt("FillPointSet import not resolved")
    # the per-body clearance radius pushed into the radii vector
    clear_hex = "0x3e800000"
    if clear_hex not in stxt:
        halt("SelectPoolLocations: per-body clearance constant not found")
    clearance = struct.unpack("<f", struct.pack("<I", 0x3E800000))[0]
    # the facing randomiser
    two_pi_hex = "0x40c90fdb"
    facing_random = two_pi_hex in stxt
    two_pi = struct.unpack("<f", struct.pack("<I", 0x40C90FDB))[0]
    log(f"[a.2] SelectPoolLocations @ {hex(game.base + sel)}")
    log(f"        per-body clearance pushed into radii vector = {clearance} (0x3e800000)")
    log(f"        calls Engine.dll!{iat[fill_va].split('!')[1][:70]}")
    log(f"        random facing constant {two_pi_hex} = {two_pi!r} present = {facing_random}")

    # a.3 the sampler itself — the scatter law.
    SAMPLER = 0xEDF30           # Engine.dll, reached from FillPointSet's `bool2` branch
    stx = eng.dis(SAMPLER, 0x200)
    k_theta_va, k_rho_va = 0x102E03DC, 0x102E03C8
    k_theta, k_theta_hex = eng.f32(k_theta_va)
    k_rho, k_rho_hex = eng.f32(k_rho_va)
    eng_iat = eng.iat()
    rng = eng_iat.get(0x102A263C)
    cosf = eng_iat.get(0x102A250C)
    sinf = eng_iat.get(0x102A2510)
    # retry cap
    cap = re.search(r"cmp\s+esi, 0x([0-9a-f]+)", stx)
    retry_cap = int(cap.group(1), 16) if cap else None
    eng.dis3(SAMPLER, 0x180, "mulss\txmm0, dword ptr [0x102e03c8]")
    import math
    exact_theta = 2 * math.pi / 32767
    exact_rho = 1.0 / 32767
    log(f"[a.3] sampler @ Engine.dll {hex(eng.base + SAMPLER)}")
    log(f"        RNG            = {rng}")
    log(f"        angle constant = {k_theta!r} ({k_theta_hex})   2*pi/32767 = {exact_theta!r}")
    log(f"        radius constant= {k_rho!r} ({k_rho_hex})   1/32767    = {exact_rho!r}")
    log(f"        cos -> {cosf}")
    log(f"        sin -> {sinf}")
    log(f"        rejection retry cap = {retry_cap}")

    # a.4 the geometry, IMPORTED BY IDENTITY from Lap U's corrected artifact,
    #      then RESTRICTED to fork (d)'s surviving candidate arenas so that the
    #      unreached arena identity becomes a BOUND rather than a shrug.
    geom_rows = []
    with (NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_geometry_v3.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            geom_rows.append(row)
    log(f"[a.4] Lap U pm4u_geometry_v3.csv imported: {len(geom_rows)} rows, "
        f"columns = {sorted(geom_rows[0]) if geom_rows else None}")

    def stats(rows, col):
        v = sorted(float(r[col]) for r in rows if r.get(col) not in (None, "", "nan"))
        if not v:
            return None
        n = len(v)
        med = v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])
        return dict(n=n, min=round(v[0], 4), median=round(med, 4),
                    mean=round(sum(v) / n, 4), max=round(v[-1], 4))

    # `D-AA-4` guard: Lap U's artifact carries TWO archive copies of every map (a lower
    # mod layer and survivalmode3).  Pooling them double-counts, and on `survivalworld_a`
    # — one of fork (d)'s three candidates — the two copies DISAGREE.  Resolve the mod
    # stack: survivalmode3 is the highest layer and ships all ten maps, so it wins.
    RESOLVER = "survivalmode3/resources/Maps.arc"
    layers = {}
    for r in geom_rows:
        layers.setdefault(r["map"], {}).setdefault(r["archive"], []).append(
            (r["spawn_x"], r["spawn_y"], r["spawn_z"], r["to_patrol_centroid_m"]))
    disagree = sorted(m for m, d in layers.items()
                      if len(d) == 2 and sorted(list(d.values())[0]) != sorted(list(d.values())[1]))
    log(f"[a.4] archive copies per map: {sorted({len(d) for d in layers.values()})}; "
        f"resolver = {RESOLVER}")
    log(f"[a.4] maps whose lower-layer copy DISAGREES with the resolver: {disagree}")
    if not all(RESOLVER in d for d in layers.values()):
        halt("resolver archive absent for some map — mod-stack resolution unsafe")
    resolved = [r for r in geom_rows if r["archive"] == RESOLVER]
    if len(resolved) != 60:
        halt(f"resolved geometry row count {len(resolved)} != 60 (10 maps x 6 spawn points)")

    per_arena, cand_rows = {}, []
    CAND = ("survivalworld_a.map", "survivalworld_b.map", "survivalworld_e.map")
    for r in resolved:
        per_arena.setdefault(r["map"], []).append(r)
    for m in sorted(per_arena):
        rs = per_arena[m]
        log(f"        {m:22s} n={len(rs):3d}  to_patrol_centroid={stats(rs, 'to_patrol_centroid_m')}")
        if m in CAND:
            cand_rows.extend(rs)
    bound = {c: stats(cand_rows, c) for c in
             ("to_patrol_centroid_m", "to_nearest_patrol_m", "ring_max_extent_m",
              "placement_extents_m")}
    allb = {c: stats(resolved, c) for c in
            ("to_patrol_centroid_m", "to_nearest_patrol_m", "ring_max_extent_m",
             "placement_extents_m")}
    log(f"[a.4] CANDIDATE-ARENA BOUND (maps a/b/e only, n={len(cand_rows)} spawn points):")
    for k, v in bound.items():
        log(f"        {k:26s} {v}")
    log(f"[a.4] all-arena comparison (n={len(resolved)}):")
    for k, v in allb.items():
        log(f"        {k:26s} {v}")

    return dict(
        candidate_arena_bound=bound, all_arena_stats=allb,
        candidate_arena_spawn_points=len(cand_rows),
        per_arena_centroid={m: stats(per_arena[m], "to_patrol_centroid_m")
                            for m in sorted(per_arena)},
        proxy_load_fields=fields,
        select_pool_locations_va=hex(game.base + sel),
        per_body_clearance_m=clearance, per_body_clearance_hex="0x3e800000",
        fill_point_set=iat[fill_va],
        random_facing=dict(present=facing_random, constant_hex=two_pi_hex, value=two_pi),
        sampler_va=hex(eng.base + SAMPLER),
        sampler_rng=rng, sampler_cos=cosf, sampler_sin=sinf,
        k_theta=dict(va=hex(k_theta_va), value=k_theta, hex=k_theta_hex,
                     exact_2pi_over_32767=exact_theta),
        k_rho=dict(va=hex(k_rho_va), value=k_rho, hex=k_rho_hex,
                   exact_1_over_32767=exact_rho),
        rejection_retry_cap=retry_cap,
        geometry_source="lap-u/pm4u_geometry_v3.csv (import by identity)",
        geometry_rows=len(geom_rows), geometry_columns=sorted(geom_rows[0]) if geom_rows else [],
    )


# ===================================================================== § 5  FORK (b)  WHEN
TIER16_DIR = "records/proxies/tier16waves/"


def resolve_record(path: str, stack: list):
    """Whole-record replacement across the mod stack: last archive wins."""
    for name, arch in reversed(stack):
        if path in arch.records:
            return name, arch.record_type(path), arch.read_record(path)
    return None, None, None


def fork_b(game: Img) -> dict:
    log("\n===== FORK (b) — WHEN ===================================================")

    # b.1 the release chain, decoded instruction by instruction.
    ex = game.ex
    chain = []

    dr = ex["?DelayedRun@Proxy@GAME@@QAEXXZ"]
    dtxt = game.dis(dr, 0x20)
    n_ins = len([l for l in dtxt.splitlines() if re.match(r"^[0-9a-f]{8}:", l)])
    tail = "jmp" in dtxt and "RunProxy" in dtxt
    game.dis3(dr, 0x20, "cmp\tdword ptr [ecx + 0x4ac], 0x1")
    chain.append(dict(step="Proxy::DelayedRun", va=hex(game.base + dr),
                      body=f"{n_ins} instructions; state 1 -> 0 then TAIL-JMP RunProxy",
                      timer="NONE", tail_jump=tail))
    log(f"[b.1] Proxy::DelayedRun @ {hex(game.base + dr)} — {n_ins} instructions, "
        f"tail-jmp into RunProxy = {tail}, NO timer")

    rp = ex["?RunProxy@Proxy@GAME@@IAEXXZ"]
    rtxt = game.dis(rp, 0x2E0)
    latch_in = "cmp\tdword ptr [edi + 0x4ac], 0x0" in rtxt
    latch_out = "mov\tdword ptr [edi + 0x4ac], 0x6" in rtxt
    n_selcalls = rtxt.count("SelectPoolLocations")
    vcall_pool = "call\tdword ptr [eax + 0x1fc]" in rtxt
    game.dis3(rp, 0x2E0, "mov\tdword ptr [edi + 0x4ac], 0x6")
    chain.append(dict(step="Proxy::RunProxy", va=hex(game.base + rp),
                      body="one-shot latch +0x4ac; chanceToRun roll; SelectPoolLocations x2; "
                           "virtual PoolComplete (vtbl+0x1fc); latch -> 6",
                      timer="NONE", latch_in=latch_in, latch_out=latch_out,
                      selectpoollocations_calls=n_selcalls, pool_complete_vcall=vcall_pool))
    log(f"[b.1] Proxy::RunProxy @ {hex(game.base + rp)} — latch-in {latch_in}, latch-out {latch_out}, "
        f"{n_selcalls} SelectPoolLocations calls, PoolComplete vcall {vcall_pool}, NO timer")

    pc = ex["?PoolComplete@Proxy@GAME@@MAEXPAVProxyPool@2@ABV?$vector@VWorldCoords@GAME@@@mem@@@Z"]
    ptxt = game.dis(pc, 0x160)
    po_rva = ex["?PlaceObjects@Proxy@GAME@@IAEXAAV?$vector@I@mem@@ABV?$vector@VWorldCoords@GAME@@@4@@Z"]
    direct = f"call\t{hex(game.base + po_rva)}" in ptxt or "PlaceObjects" in ptxt
    queued = "+0x4d0" in ptxt
    game.dis3(pc, 0x160, "PlaceObjects@Proxy")
    chain.append(dict(step="Proxy::PoolComplete", va=hex(game.base + pc),
                      body="per-body proxy-parent stamping loop, then a DIRECT call to PlaceObjects",
                      timer="NONE", direct_call_to_placeobjects=direct, queues_pending=queued))
    log(f"[b.1] Proxy::PoolComplete @ {hex(game.base + pc)} — direct PlaceObjects call = {direct}, "
        f"queues into a pending vector = {queued}")

    ptxt2 = game.dis(po_rva, 0x2A0)
    loops = "jne\t" in ptxt2 or "je\t" in ptxt2
    addent = next((nm for va, nm in game.iat().items() if "AddEntity@World" in nm), None)
    game.dis3(po_rva, 0x2A0, "AddUniqueIdToEntity@Proxy")
    chain.append(dict(step="Proxy::PlaceObjects", va=hex(game.base + po_rva),
                      body="single loop over (ids x coords): AddUniqueIdToEntity, then World::AddEntity",
                      timer="NONE", world_add=addent, loop=loops))
    log(f"[b.1] Proxy::PlaceObjects @ {hex(game.base + po_rva)} — one loop, per body -> {addent}")

    # b.1b THE LATCH's COMPLETE WRITER SET.  This is what makes "the Lua's :Run() reaches
    #      DelayedRun" a decoded inference rather than an assumption: the binding body is
    #      behind the exe's DRM, but state 1 has exactly ONE exit in the whole module.
    LW = re.compile(rb"\xc7[\x80-\x87]\xac\x04\x00\x00(....)")     # mov [reg+0x4ac], imm32
    latch_writers = []
    for m in LW.finditer(game.text):
        rva = game.text_rva + m.start()
        sym, off = game.enclosing(rva)
        latch_writers.append(dict(va=hex(game.base + rva), value=struct.unpack("<I", m.group(1))[0],
                                  enclosing=sym, delta=hex(off)))
    exits_from_1 = [w for w in latch_writers
                    if w["value"] == 0 and "DelayedRun" in str(w["enclosing"])]
    log(f"[b.1b] Proxy state latch +0x4ac — imm32 writers ENUMERATED: {len(latch_writers)}")
    for w in latch_writers:
        log(f"        {w['va']} = {w['value']}   {w['enclosing']} {w['delta']}")
    log(f"[b.1b] writers that clear the delayedRun park (1 -> 0) inside DelayedRun: "
        f"{[w['va'] for w in exits_from_1]}")

    # b.2 the 54-record field census.  P-AA-1 is a CENSUS, not an impression.
    stack = []
    for nm, rel in [("SurvivalMode", "mods/survivalmode/database/SurvivalMode.arz"),
                    ("SurvivalMode1", "survivalmode1/database/SurvivalMode1.arz"),
                    ("SurvivalMode2", "survivalmode2/database/SurvivalMode2.arz"),
                    ("SurvivalMode3", "survivalmode3/database/SurvivalMode3.arz")]:
        stack.append((nm, ARZ.ArzArchive(ED / rel)))
    paths = sorted({p for _, a in stack for p in a.records if p.startswith(TIER16_DIR)})
    rows, all_fields = [], {}
    classes = {}
    for p in paths:
        src, cls, rec = resolve_record(p, stack)
        classes[cls] = classes.get(cls, 0) + 1
        for k, v in rec.items():
            all_fields.setdefault(k, set()).add(str(v))
        rows.append(dict(record=p, source_archive=src, cls=cls,
                         placementExtents=rec.get("placementExtents"),
                         chanceToRun=rec.get("chanceToRun"),
                         delayedRun=rec.get("delayedRun"),
                         n_fields=len(rec),
                         pools=";".join(sorted(k for k in rec if k.startswith("pool"))),
                         ambush_fields=";".join(sorted(
                             k for k in rec if k in ("alertArea", "minSpawnTime", "maxSpawnTime",
                                                     "minDelayTime", "maxDelayTime", "minGroupSize",
                                                     "maxGroupSize", "spawnThreshold")))))
    # the timing-word census: any field whose NAME suggests a schedule
    TIMEWORDS = ("delay", "time", "interval", "rate", "period", "stagger", "cooldown",
                 "duration", "wait", "tick", "batch", "burst", "frequency")
    timing_fields = sorted(f for f in all_fields
                           if any(w in f.lower() for w in TIMEWORDS))
    log(f"[b.2] tier-16 wave proxies: {len(paths)}  classes = {classes}")
    log(f"[b.2] distinct field names across all {len(paths)} records: {len(all_fields)}")
    log(f"[b.2] fields whose NAME contains a timing word: {timing_fields}")

    # b.3 per-wave batch composition, IMPORTED BY IDENTITY from Lap V.
    comp = {}
    with (NOTES / "2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            w = int(row["global_wave"])
            sp = int(row["spawn_point"])
            e = float(row["e_bodies"])
            lo_, hi_ = float(row["bodies_lo"]), float(row["bodies_hi"])
            d = comp.setdefault(w, {}).setdefault(sp, dict(e=0.0, lo=0.0, hi=0.0, pools=0))
            d["e"] += e
            d["lo"] += lo_
            d["hi"] += hi_
            d["pools"] += 1
    log("[b.3] per-wave batch composition (import by identity, Lap V pm4v_roster_arithmetic.csv):")
    for w in sorted(comp):
        pts = comp[w]
        log(f"        w{w}: points={sorted(pts)} "
            f"E_bodies={{{', '.join(f'p{p}:{pts[p]['e']:.3f}' for p in sorted(pts))}}} "
            f"total={sum(pts[p]['e'] for p in pts):.3f}")

    # b.4 the ambush limb, IMPORTED BY IDENTITY from Lap V-2.
    amb = json.loads((NOTES / "2026-08-15-kc2-pm4-lap-v2-proxyambush-decode/pm4v2_ambush.json").read_text())

    # b.5 the Lua orchestration — verbatim line citations.
    lua = (NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance/evidence/survivalevent.lua").read_text()
    llines = lua.splitlines()

    def find_line(sub, after=0):
        """`D-Z-1` guard applied to TEXT: publish the full hit set, then take the one
        after the named anchor.  The first textual match is not the right match."""
        hits = [(i, l.strip()) for i, l in enumerate(llines, 1) if sub in l and i > after]
        return (hits[0] if hits else (None, None)), [h[0] for h in hits]

    spawnnext_def = next(i for i, l in enumerate(llines, 1)
                         if l.startswith("function SurvivalEvent_SpawnNext"))
    l_for, for_hits = find_line("for id = 1, waveEvent.numSpawns do", after=spawnnext_def)
    log(f"[b.5] 'for id = 1, waveEvent.numSpawns do' occurs at lines {for_hits} "
        f"(SurvivalEvent_SpawnNext begins L{spawnnext_def}; the dispensing loop is the first after it)")
    l_create, _ = find_line("Proxy.Create(waveEvent.waves[id]")
    l_run, _ = find_line("waveEvent.proxy[id]:Run()")
    l_start_spawn, _ = find_line("SurvivalEvent_SpawnNext(objectId)")
    l_incr, _ = find_line("Game.IncrementSurvivalWaveTier()")
    l_link, _ = find_line("LinkPatrolPointGroup")
    log(f"[b.5] survivalevent.lua L{l_link[0]} : {l_link[1]}")
    log(f"[b.5] survivalevent.lua L{l_for[0]} : {l_for[1]}")
    log(f"[b.5] survivalevent.lua L{l_create[0]} : {l_create[1][:90]}")
    log(f"[b.5] survivalevent.lua L{l_run[0]} : {l_run[1]}")
    log(f"[b.5] survivalevent.lua L{l_incr[0]} : {l_incr[1]}")
    log(f"[b.5] SurvivalEvent_Start dispenses immediately at L{l_start_spawn[0]}")

    return dict(
        release_chain=chain, latch_writers=latch_writers,
        n_tier16_proxies=len(paths), proxy_classes=classes,
        distinct_field_names=len(all_fields),
        timing_named_fields=timing_fields,
        field_rows=rows,
        batch_composition={str(w): {str(p): comp[w][p] for p in sorted(comp[w])}
                           for w in sorted(comp)},
        ambush_import={k: amb[k] for k in list(amb)[:40]} if isinstance(amb, dict) else amb,
        lua_sites=dict(spawn_loop=l_for[0], spawn_loop_all_hits=for_hits,
                       spawnnext_def=spawnnext_def,
                       proxy_create=l_create[0], proxy_run=l_run[0],
                       link_patrol_group=l_link[0],
                       wave_counter_increment=l_incr[0], start_dispenses_at=l_start_spawn[0]),
    )


# ===================================================================== § 6  FORK (c)  BETWEEN
def fork_c(game: Img) -> dict:
    log("\n===== FORK (c) — BETWEEN SPAWN AND ENGAGE ===============================")

    # c.1 the rally/alert latch — writers and readers ENUMERATED, not sampled.
    W = re.compile(rb"\xc6[\x80-\x87]\x8c\x02\x00\x00[\x00\x01]")
    R = re.compile(rb"\x80[\xb8-\xbf]\x8c\x02\x00\x00\x00")
    writers, readers = [], []
    for m in W.finditer(game.text):
        rva = game.text_rva + m.start()
        sym, off = game.enclosing(rva)
        writers.append(dict(va=hex(game.base + rva), bytes=m.group().hex(),
                            value=m.group()[-1], enclosing=sym, delta=hex(off)))
    for m in R.finditer(game.text):
        rva = game.text_rva + m.start()
        sym, off = game.enclosing(rva)
        readers.append(dict(va=hex(game.base + rva), enclosing=sym, delta=hex(off)))
    log(f"[c.1] ControllerMonster +0x28c  writers={len(writers)}  readers={len(readers)}")
    for w in writers:
        log(f"        W {w['va']} = {w['value']}   {w['enclosing']}{'' if w['enclosing'] is None else ' ' + w['delta']}")
    for r in readers:
        log(f"        R {r['va']}   {r['enclosing']} {r['delta']}")

    # c.2 the AlertBeforePursue state — is it ever ENTERED?
    #     `D-Z-1` guard, and it FIRED on my own first pass: the literal has MORE THAN ONE
    #     copy in .rdata.  Every copy is enumerated and every copy's reference set is
    #     scanned; taking one address would have been the exact D-Z-1 error.
    raw_hits = len(re.findall(rb"AlertBeforePursue", game.b))
    occ, standalone = [], []
    for m in re.finditer(rb"AlertBeforePursue", game.b):
        rva = game.pe.off_to_rva(m.start())
        sec = game.pe.section_of_rva(rva) if rva is not None else None
        # a STANDALONE literal is NUL-terminated AND NUL-preceded; the rest are substrings
        # of exported C++ mangled names (`...StateAlertBeforePursue@GAME@@...`).
        is_standalone = (game.b[m.start() - 1] == 0
                         and game.b[m.end()] == 0)
        rec = dict(file_off=hex(m.start()), va=hex(game.base + rva) if rva else None,
                   section=sec["name"] if sec else None, standalone=is_standalone,
                   context=game.b[max(0, m.start() - 24): m.start() + 30].decode("latin-1",
                                                                                 "replace"))
        occ.append(rec)
        if is_standalone and rva is not None:
            standalone.append(game.base + rva)
    log(f"[c.2] literal 'AlertBeforePursue' raw occurrences in Game.dll = {raw_hits}")
    for o in occ:
        log(f"        {o['file_off']:>10s} {str(o['section']):>8s} standalone={o['standalone']}  {o['context']!r}")
    log(f"[c.2] STANDALONE literal copies (the decoy set, ENUMERATED): "
        f"{[hex(v) for v in standalone]}")
    refs = []
    for va in standalone:
        if game.cstr(va) != "AlertBeforePursue":
            halt(f"standalone literal at {hex(va)} does not read back as expected")
        rs = game.imm_refs(va)
        log(f"[c.2]   .text sites referencing {hex(va)}: {len(rs)}")
        for r in rs:
            log(f"          {r['va']} prev_op={r['prev_op']}  {r['enclosing']} {r['delta']}")
            r["literal_va"] = hex(va)
        refs.extend(rs)
    lit_va = standalone[-1] if standalone else None

    # cross-module: is the literal present anywhere else at all?
    other = {}
    for mod in ("Engine.dll", "Grim Dawn.exe"):
        other[mod] = len(re.findall(rb"AlertBeforePursue", (GD / mod).read_bytes()))
    log(f"[c.2] literal in other shipped modules: {other}")

    # ... and is it a RECORD value anywhere in the shipped corpus?
    corpus_hits = {}
    for nm, rel in [("database", "database/database.arz"),
                    ("GDX1", "gdx1/database/GDX1.arz"),
                    ("GDX2", "gdx2/database/GDX2.arz"),
                    ("GDX3", "gdx3/database/GDX3.arz"),
                    ("SurvivalMode", "mods/survivalmode/database/SurvivalMode.arz"),
                    ("SurvivalMode1", "survivalmode1/database/SurvivalMode1.arz"),
                    ("SurvivalMode2", "survivalmode2/database/SurvivalMode2.arz"),
                    ("SurvivalMode3", "survivalmode3/database/SurvivalMode3.arz")]:
        p = ED / rel
        if not p.exists():
            continue
        a = ARZ.ArzArchive(p)
        corpus_hits[nm] = sum(1 for s in a.strings if "AlertBeforePursue" in s)
    log(f"[c.2] 'AlertBeforePursue' as a shipped record STRING: {corpus_hits}")

    # positive controls — a name the engine demonstrably DOES dispatch on
    pos = {}
    for label, va in [("Pursue(registration)", 0x1052C19C), ("Pursue(SetState)", 0x1052D5D4)]:
        pos[label] = dict(text=game.cstr(va), refs=game.imm_refs(va))
    log("[c.2] positive controls:")
    for k, v in pos.items():
        log(f"        {k:22s} {v['text']!r}  refs={[r['enclosing'] for r in v['refs']]}")

    # c.2b THE ALERT GATE.  The second standalone literal IS referenced — from inside
    #      `DefaultEnemyFoundResponse`.  Decode the branch that reaches it.
    der = game.ex[next(k for k in game.ex
                       if k.startswith("?DefaultEnemyFoundResponse@?$ControllerMonsterState@"
                                       "VControllerMonster"))]
    gate = game.dis(der + 0x330, 0xC0)
    need = ["sqrtss", "[eax + 0xc80]", "GetAngerDiff", "0x1052d5fc", "AddTemporaryState"]
    missing = [n for n in need if n not in gate]
    if missing:
        halt(f"alert-gate decode incomplete, missing {missing}")
    game.dis3(der + 0x330, 0xC0, "[eax + 0xc80]")

    # the two operands of the gate
    anger_const, anger_hex = game.f32(0x105F58AC)
    # +0xc80 is a GameEngine member: find its sole writer and its field literal
    W2 = re.compile(rb"\xd9[\x98-\x9f]\x80\x0c\x00\x00")            # fstp [reg+0xc80]
    R2 = re.compile(rb"\x0f\x2f[\x80-\xbf]\x80\x0c\x00\x00")        # comiss xmm,[reg+0xc80]
    C2 = re.compile(rb"\xc7[\x80-\x87]\x80\x0c\x00\x00(....)")      # mov [reg+0xc80], imm32
    w2 = [(hex(game.base + game.text_rva + m.start()),
           game.enclosing(game.text_rva + m.start())) for m in W2.finditer(game.text)]
    r2 = [(hex(game.base + game.text_rva + m.start()),
           game.enclosing(game.text_rva + m.start())) for m in R2.finditer(game.text)]
    c2 = [(hex(game.base + game.text_rva + m.start()),
           game.enclosing(game.text_rva + m.start()),
           struct.unpack("<f", m.group(1))[0]) for m in C2.finditer(game.text)]
    field_name = game.cstr(0x1054D7C0)
    neighbour = game.cstr(0x1054D7AC)
    log(f"[c.2b] alert gate inside DefaultEnemyFoundResponse @ {hex(game.base + der)}")
    log(f"        distance operand : GameEngine+0xc80  field literal {field_name!r} "
        f"(loader neighbour at +0xc7c is {neighbour!r})")
    log(f"        +0xc80 writers   : {w2}")
    log(f"        +0xc80 readers   : {r2}")
    log(f"        +0xc80 ctor imms : {[(a, s, v) for a, s, v in c2 if 'GameEngine' in str(s)]}")
    log(f"        anger operand    : {anger_const!r} ({anger_hex}) @ 0x105f58ac")

    # the shipped value, whole-record replacement across the mod stack, EXACT PATH ONLY.
    ge_stack = []
    for nm, rel in [("database", "database/database.arz"),
                    ("SurvivalMode", "mods/survivalmode/database/SurvivalMode.arz"),
                    ("SurvivalMode1", "survivalmode1/database/SurvivalMode1.arz"),
                    ("SurvivalMode2", "survivalmode2/database/SurvivalMode2.arz"),
                    ("SurvivalMode3", "survivalmode3/database/SurvivalMode3.arz")]:
        ge_stack.append((nm, ARZ.ArzArchive(ED / rel)))
    decoys = sorted({p for _, a in ge_stack for p in a.records if "gameengine" in p.lower()})
    log(f"[c.2b] 'gameengine' SUBSTRING decoy set ({len(decoys)}) — enumerated, `D-Z-1`:")
    for p in decoys:
        vals = {}
        for nm, a in ge_stack:
            if p in a.records:
                vals[nm] = a.read_record(p).get(field_name)
        log(f"        {p:56s} {field_name} = {vals}")
    src, _, ge = resolve_record("records/game/gameengine.dbr", ge_stack)
    alert_distance = ge.get(field_name)
    melee_target = ge.get(neighbour)
    log(f"[c.2b] SHIPPED (exact path records/game/gameengine.dbr, resolver {src}): "
        f"{field_name} = {alert_distance}   {neighbour} = {melee_target}")

    # the state's own body
    ob = game.ex["?OnBegin@ControllerMonsterStateAlertBeforePursue@GAME@@UAEXXZ"]
    oe = game.ex["?OnEnd@ControllerMonsterStateAlertBeforePursue@GAME@@UAEXXZ"]
    ou = game.ex["?OnUpdate@ControllerMonsterStateAlertBeforePursue@GAME@@UAEXH@Z"]
    obt = game.dis(ob, 0x30)
    oet = game.dis(oe, 0x08)
    out_ = game.dis(ou, 0x120)
    anim_type = "push\t0x21" in obt
    anim_speed = "0x3f800000" in obt
    onend_noop = bool(re.search(r"^[0-9a-f]{8}: c3\s", oet, re.M))
    MOVEWORDS = ("MoveTo", "SetDestination", "Move@", "Path", "Steer", "Velocity")
    move_calls = sorted({w for w in MOVEWORDS if w in out_})
    log(f"[c.2b] AlertBeforePursue::OnBegin @ {hex(game.base + ob)} — "
        f"PlayAnimation(AnimationSet_Type 0x21={anim_type}, speed 1.0f={anim_speed})")
    log(f"[c.2b] AlertBeforePursue::OnEnd   @ {hex(game.base + oe)} — bare ret (no-op) = {onend_noop}")
    log(f"[c.2b] AlertBeforePursue::OnUpdate@ {hex(game.base + ou)} — "
        f"locomotion-named calls in first 0x120 bytes: {move_calls or 'NONE'}")

    alert = dict(
        gate_site=hex(game.base + der + 0x330),
        distance_member="GameEngine+0xc80", distance_field=field_name,
        distance_field_literal_va=hex(0x1054D7C0),
        loader_neighbour_field=neighbour,
        shipped_alertDistance=alert_distance, shipped_meleeTargetDistance=melee_target,
        gameengine_record="records/game/gameengine.dbr", resolver_archive=src,
        gameengine_substring_decoys=decoys,
        ctor_default=[v for a, s, v in c2 if "GameEngine" in str(s)],
        writers=[(a, s[0], hex(s[1])) for a, s in w2],
        readers=[(a, s[0], hex(s[1])) for a, s in r2],
        anger_constant=anger_const, anger_constant_hex=anger_hex,
        anger_constant_va="0x105f58ac",
        anger_call="AngerManager::GetAngerDiff",
        entry_call="ControllerAI::AddTemporaryState(name, ControllerAIStateData&)",
        state_onbegin=dict(va=hex(game.base + ob), animation_set_type="0x21",
                           speed_1_0=anim_speed, plays_animation=anim_type),
        state_onend_is_noop=onend_noop,
        state_onupdate_locomotion_calls=move_calls,
    )

    # c.3 the acquisition radius, IMPORTED BY IDENTITY from Lap U.
    pursue = json.loads((NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_pursue_decode.json").read_text())

    # c.4 the proxy-parent stamping that PlaceObjects performs on every body
    po = game.ex["?PlaceObjects@Proxy@GAME@@IAEXAAV?$vector@I@mem@@ABV?$vector@VWorldCoords@GAME@@@4@@Z"]
    pc = game.ex["?PoolComplete@Proxy@GAME@@MAEXPAVProxyPool@2@ABV?$vector@VWorldCoords@GAME@@@mem@@@Z"]
    ptxt = game.dis(pc, 0x160)
    stamps = dict(
        proxy_parent_id="[ebx + 0x37bc]" in ptxt,
        proxy_parent_name="[ebx + 0x37c0]" in ptxt,
        proxy_sibling_count="[ebx + 0x37d8]" in ptxt,
    )
    if not all(stamps.values()):
        halt(f"PoolComplete stamping predicate failed: {stamps}")
    game.dis3(pc, 0x160, "[ebx + 0x37bc]")
    log(f"[c.4] PoolComplete per-body stamping: {stamps}")

    return dict(
        rally_latch=dict(member="ControllerMonster+0x28c", writers=writers, readers=readers),
        alert_before_pursue=dict(
            standalone_literal_vas=[hex(v) for v in standalone],
            literal_va=hex(lit_va) if lit_va else None, raw_occurrences_game_dll=raw_hits,
            occurrences=occ, text_references=refs,
            other_modules=other, corpus_record_strings=corpus_hits,
            positive_controls={k: dict(text=v["text"],
                                       enclosing=[r["enclosing"] for r in v["refs"]])
                               for k, v in pos.items()}),
        alert_gate=alert,
        pursue_import_source="lap-u/pm4u_pursue_decode.json",
        pursue_import_keys=sorted(pursue) if isinstance(pursue, dict) else None,
        pursue_import=pursue,
        placeobjects_va=hex(game.base + po),
        poolcomplete_stamping=stamps,
    )


# ===================================================================== § 7  MAIN
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    log("KC2-PM4 · LAP AA — THE REFERENT'S SPAWN STRUCTURE — instrument I-AA-1")
    log("prereg committed ALONE in ba368773 before this file existed")
    pins = verify_pins()

    game = Img("Game.dll")
    eng = Img("Engine.dll")
    exe = Img("Grim Dawn.exe")

    d = fork_d(exe)
    a = fork_a(game, eng)
    b = fork_b(game)
    c = fork_c(game)

    # ---- emissions
    (OUT / "pm4aa_arena_identity.json").write_text(json.dumps(d, indent=1, sort_keys=True) + "\n")
    (OUT / "pm4aa_placement_law.json").write_text(json.dumps(a, indent=1, sort_keys=True) + "\n")

    with (OUT / "pm4aa_release_chain.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["step", "va", "body", "timer", "detail"])
        w.writeheader()
        for step in b["release_chain"]:
            det = {k: v for k, v in step.items() if k not in ("step", "va", "body", "timer")}
            w.writerow(dict(step=step["step"], va=step["va"], body=step["body"],
                            timer=step["timer"], detail=json.dumps(det, sort_keys=True)))

    with (OUT / "pm4aa_proxy_fields.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=sorted(b["field_rows"][0]))
        w.writeheader()
        for r in b["field_rows"]:
            w.writerow(r)

    struct_out = dict(
        lap="KC2-PM4 Lap AA", commissioned_by="R-PM4-67 part 7",
        prereg_commit="ba368773",
        fork_a_where={k: v for k, v in a.items() if k != "geometry_columns"},
        fork_b_when={k: v for k, v in b.items() if k != "field_rows"},
        fork_c_between=c,
        fork_d_arena=d,
    )
    (OUT / "pm4aa_spawn_structure.json").write_text(
        json.dumps(struct_out, indent=1, sort_keys=True, default=str) + "\n")

    (OUT / "decode.log").write_text("\n".join(LOG) + "\n")

    emitted = ["pm4aa_arena_identity.json", "pm4aa_placement_law.json",
               "pm4aa_release_chain.csv", "pm4aa_proxy_fields.csv",
               "pm4aa_spawn_structure.json", "decode.log"]
    digests = dict(
        inputs=pins,
        instrument={str(pathlib.Path(__file__).resolve()): sha256(pathlib.Path(__file__))},
        emitted={f: sha256(OUT / f) for f in emitted},
    )
    (OUT / "pm4aa_digests.json").write_text(json.dumps(digests, indent=1, sort_keys=True) + "\n")
    print("OK — emitted:", ", ".join(emitted + ["pm4aa_digests.json"]))


if __name__ == "__main__":
    main()
