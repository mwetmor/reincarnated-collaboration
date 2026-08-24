#!/usr/bin/env python3
"""KC2 MODEL-COMPLETION RUN · Wave 1 · piece D-1 — THE ALERT DECODE.  Instrument I-D1-1.

WHY THIS EXISTS
    The charter (`agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`,
    Wave 1, seat legolas) commissions two undecoded halves of `AlertBeforePursue`:
      (1) ENTRY CONDITION — the predicate named `ShouldPlayRallyOrAlert` (`UNREACHED-U3`)
      (2) DURATION        — how long the state lasts (`U-U-2` / `UNREACHED-AA-3` / `UNREACHED-AB-2`)

    Method is Lap J's, unchanged: the shipped modules are PE32 (`coff-i386`) with FULL
    MSVC-decorated export tables, so a named C++ member is located by RVA and disassembled
    straight out of the shipped bytes.  RE-IMPLEMENTS NOTHING: `pm4s_pe_2026_08_14.PE32`
    is imported unchanged (NOTE-9).

    Every claim in the lap's README is produced by this file.  Nothing is retyped from prose.

READ-ONLY on `/Users/admin/Games/vendor/grim-dawn/`.  Writes ONLY into this lap's evidence dir.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-24.  Run KC2-MC, Wave 1, piece D-1.
"""
from __future__ import annotations

import bisect
import json
import pathlib
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
COLLAB = HERE.parent.parent.parent
LAP = "2026-08-24-kc2-mc-lap-d1-alert-decode"
OUT = COLLAB / "agentic_orchestration/legolas/notes" / LAP / "evidence"
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")

sys.path.insert(0, str(HERE))
from pm4s_pe_2026_08_14 import PE32, sha256  # noqa: E402

# ============================================================ § 1  PINS (HALT on mismatch)
PIN = {
    GD / "Game.dll":   "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    GD / "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
}
for p, want in PIN.items():
    got = sha256(p)
    if got != want:
        raise SystemExit(f"HALT — digest mismatch on {p}: {got} != {want}")

GAME = PE32(GD / "Game.dll")
ENG = PE32(GD / "Engine.dll")


def symtab(pe):
    exp = sorted((r, n) for n, r in pe.exports().items())
    rvas = [r for r, _ in exp]

    def sym(rva):
        i = bisect.bisect_right(rvas, rva) - 1
        return "?" if i < 0 else f"{exp[i][1]}+{rva - exp[i][0]:#x}"
    return sym


SYM_G, SYM_E = symtab(GAME), symtab(ENG)


def cstr(pe, va):
    o = pe.rva_to_off(va - pe.image_base)
    if o is None:
        return None
    e = pe.raw.index(b"\0", o)
    return pe.raw[o:e].decode("latin-1")


def f32(pe, va):
    return struct.unpack_from("<f", pe.raw, pe.rva_to_off(va - pe.image_base))[0]


def calls_to(pe, target_rva, opcodes=(0xE8, 0xE9)):
    """Every direct call/jmp in .text whose target is `target_rva`."""
    text = [s for s in pe.sections if s["name"] == ".text"][0]
    b = pe.raw[text["raddr"]:text["raddr"] + text["rsize"]]
    base = text["vaddr"]
    out = []
    for op in opcodes:
        for i in range(len(b) - 5):
            if b[i] == op:
                rel = struct.unpack_from("<i", b, i + 1)[0]
                if base + i + 5 + rel == target_rva:
                    out.append((hex(op), base + i))
    return out


def refs_to_va(pe, va):
    """Every 4-byte absolute reference to `va` inside .text (literal-address decoy guard)."""
    text = [s for s in pe.sections if s["name"] == ".text"][0]
    b = pe.raw[text["raddr"]:text["raddr"] + text["rsize"]]
    base = text["vaddr"]
    n = struct.pack("<I", va)
    out, st = [], 0
    while True:
        i = b.find(n, st)
        if i < 0:
            break
        st = i + 1
        out.append(base + i)
    return out


def standalone_literals(pe, s: str):
    """D-Z-1 guard: EVERY NUL-delimited standalone copy of `s`, not just the first."""
    needle = b"\0" + s.encode() + b"\0"
    out, st = [], 0
    while True:
        i = pe.raw.find(needle, st)
        if i < 0:
            break
        st = i + 1
        rva = pe.off_to_rva(i + 1)
        if rva is not None:
            out.append(pe.image_base + rva)
    return out


def vtable(pe, rva, n, sym):
    o = pe.rva_to_off(rva)
    rows = []
    for i in range(0, 4 * n, 4):
        f = struct.unpack_from("<I", pe.raw, o + i)[0] - pe.image_base
        rows.append((i, f, sym(f)))
    return rows


OUT.mkdir(parents=True, exist_ok=True)
LOG = []


def log(s=""):
    LOG.append(s)
    print(s)


def dump(name, rva, n, pe=GAME):
    """objdump a range, strip padding, bank verbatim."""
    txt = "\n".join(l for l in pe.disasm(rva, n).splitlines() if "int3" not in l)
    (OUT / name).write_text(txt + "\n")
    return txt


# ============================================================ § 2  HALF 1 — ENTRY CONDITION
log("=" * 78)
log("HALF 1 — ENTRY CONDITION")
log("=" * 78)

E = GAME.exports()
SPRA = E["?ShouldPlayRallyOrAlert@ControllerMonster@GAME@@QAE_NXZ"]
log(f"\nShouldPlayRallyOrAlert @ Game.dll RVA {SPRA:#x} (VA {GAME.image_base + SPRA:#x})")
log(dump("01-ShouldPlayRallyOrAlert.asm", SPRA, 0x20))
log(f"direct call sites: {calls_to(GAME, SPRA)}   <-- fully inlined; zero out-of-line callers")

# every instruction in .text touching ControllerMonster+0x28c (the latch)
import capstone  # noqa: E402
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
text = [s for s in GAME.sections if s["name"] == ".text"][0]
tb = GAME.raw[text["raddr"]:text["raddr"] + text["rsize"]]
tbase = text["vaddr"]
latch_rows, seen, st = [], set(), 0
needle = struct.pack("<i", 0x28C)
while True:
    i = tb.find(needle, st)
    if i < 0:
        break
    st = i + 1
    for back in range(1, 10):
        s0 = i - back
        if s0 < 0:
            continue
        try:
            ins = next(md.disasm(tb[s0:s0 + 16], tbase + s0))
        except StopIteration:
            continue
        if ins.size > back and "0x28c" in ins.op_str:
            r = tbase + s0
            if r not in seen:
                seen.add(r)
                sy = SYM_G(r)
                if "ControllerMonster" in sy or "EnemyFound" in sy:
                    latch_rows.append((hex(r), f"{ins.mnemonic} {ins.op_str}", sy))
            break
log("\nEVERY .text access to ControllerMonster+0x28c (the latch):")
for r in latch_rows:
    log(f"   {r[0]:>10}  {r[1]:<42} {r[2]}")

# the response function itself
DEFR = E["?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z"]
log(f"\nDefaultEnemyFoundResponse @ RVA {DEFR:#x} (VA {GAME.image_base + DEFR:#x})")
dump("02-DefaultEnemyFoundResponse-gate.asm", DEFR + 0x225, 0x1A5)
dump("03-DefaultEnemyFoundResponse-tail.asm", DEFR + 0x3E4, 0xE6)

log("\nGate operands, resolved:")
log(f"   IsInState literal   0x1052d5dc = {cstr(GAME, 0x1052d5dc)!r}")
log(f"   AddTemporaryState   0x1052d5fc = {cstr(GAME, 0x1052d5fc)!r}")
log(f"   SetState literal    0x1052d5d4 = {cstr(GAME, 0x1052d5d4)!r}")
log(f"   anger threshold     0x105f58ac = {f32(GAME, 0x105f58ac)}")
log(f"   'AlertBeforePursue' standalone literals (D-Z-1 guard): "
    f"{[hex(v) for v in standalone_literals(GAME, 'AlertBeforePursue')]}")
for v in standalone_literals(GAME, "AlertBeforePursue"):
    log(f"      {v:#x} referenced from: {[(hex(r), SYM_G(r)) for r in refs_to_va(GAME, v)]}")

log("\nMonster chance/sound field offsets (bound by their own accessors):")
for nm in ("GetAlertSound", "GetAlertSoundChance", "GetAlertAnimChance",
           "GetRallySound", "GetRallySoundChance", "GetRallyAnimChance"):
    hits = [(n, r) for n, r in E.items() if n.startswith(f"?{nm}@Monster@")]
    for n, r in hits:
        body = GAME.disasm(r, 0x10).splitlines()
        off = [l for l in body if "mov" in l][0].split("+")[-1].split("]")[0].strip()
        log(f"   Monster{'+' + off:<10} = {nm}")

log("\nAnimationSet alert-slot emptiness limb:")
log(f"   gate reads AnimationSet+0x90  ->  slot index (0x90-0xc)/4 = {(0x90 - 0xc) // 4:#x}"
    f"  (== AnimationSet_Type 0x21, the Alert slot)")
log(dump("04-AnimationSet-DoesAnimationExist.asm", E["?DoesAnimationExist@AnimationSet@GAME@@QAE_NW4AnimationSet_Type@2@@Z"], 0x30))

log("\nEnemyFound dispatch — which states can reach the gate:")
ef = sorted(((n, r) for n, r in E.items()
             if n.startswith("?EnemyFound@ControllerMonsterState")), key=lambda kv: kv[1])
thin = calls_to(GAME, DEFR)
for r, _n in sorted({r: n for n, r in ef}.items()):
    body = GAME.disasm(r, 0x30)          # 0x30 window: thin wrappers tail-jmp within ~0x14
    tail = "-> DefaultEnemyFoundResponse" if "DefaultEnemyFoundResponse" in body else (
        "NO-OP (ICF-folded empty)" if r == 0x84D0 else "own impl (re-targets, no alert)")
    owners = sorted(x.split("@")[1] for x, y in ef if y == r)
    log(f"   {r:#010x}  {tail:<32} {', '.join(owners)}")
log(f"   tail-jmp/call sites into DefaultEnemyFoundResponse: {[(o, hex(a), SYM_G(a)) for o, a in thin]}")

log("\nalertAnimChance / alertSoundChance — .dbr field literals bound at the loader:")
log(dump("20-Monster-Load-chance-fields.asm", 0x2D3510, 0x70))
for va in (0x10560EA0, 0x10560E70, 0x10560E80):
    log(f"   {va:#x} = {cstr(GAME, va)!r}")

log("\nThe alert-chance operand over the tier-16 roster "
    "(joined from Lap AB `pm4ab_alert_anim.csv`, digest asserted):")
import csv  # noqa: E402
import collections  # noqa: E402
AB_CSV = (COLLAB / "agentic_orchestration/legolas/notes"
          / "2026-08-16-kc2-pm4-lap-ab-march-dispersion/pm4ab_alert_anim.csv")
want = "65706232f07e8366459f20e9c3873527ac4c837f7896b80a3e87eebb56fe3aa5"
if sha256(AB_CSV) != want:
    raise SystemExit(f"HALT — Lap AB CSV digest mismatch: {sha256(AB_CSV)}")
rows = list(csv.DictReader(open(AB_CSV)))
st, ch, na = collections.defaultdict(set), collections.defaultdict(set), {}
for r in rows:
    st[r["record"]].add(r["status"])
    ch[r["record"]].add(int(r["alert_anim_chance"]))
    na[r["record"]] = int(r["n_rostered_actors"])
assert not [k for k, v in st.items() if len(v) > 1], "status non-uniform within a record"
assert not [k for k, v in ch.items() if len(v) > 1], "chance non-uniform within a record"
tot = sum(na.values())
buckets = collections.Counter()
bactors = collections.Counter()
for k in st:
    key = (list(ch[k])[0], list(st[k])[0])
    buckets[key] += 1
    bactors[key] += na[k]
for k in sorted(buckets, key=lambda k: (k[1], k[0])):
    log(f"   alertAnimChance={k[0]:>4}  {k[1]:<17} records={buckets[k]:>3}  rostered_actors={bactors[k]:>3}")
can = [(k, list(ch[k])[0], na[k]) for k in st
       if list(st[k])[0] == "HAS-ALERT" and list(ch[k])[0] > 0]
exp = sum(a * c / 100 for _, c, a in can)
log(f"   records that CAN alert: {len(can)}   actors: {sum(a for _, _, a in can)} / {tot}")
log(f"   EXPECTED alerting actors over the full roster: {exp:.2f} / {tot} ({100 * exp / tot:.1f} %)")

# --- duration operand, restricted to the population that can actually alert -------------
import statistics  # noqa: E402
canrec = {k for k, _, _ in can}
sub = [r for r in rows if r["record"] in canrec and r["frames"] not in ("", "None")]
fr = sorted(int(r["frames"]) for r in sub)
q = statistics.quantiles(fr, n=4)
log("\nDURATION operand over the CAN-ALERT population "
    f"({len(canrec)} records / {len(fr)} resolved slots):")
log(f"   frames  min={min(fr)} p25={q[0]:.1f} med={statistics.median(fr):.1f} p75={q[2]:.1f} max={max(fr)}")
log(f"   seconds = (frames-1)/30  min={(min(fr) - 1) / 30:.3f} "
    f"med={(statistics.median(fr) - 1) / 30:.3f} max={(max(fr) - 1) / 30:.3f}")
spd = collections.Counter(r["anim_speed"] for r in sub)
spd_all = collections.Counter(r["anim_speed"] for r in rows if r["status"] == "HAS-ALERT")
log(f"   AlertAnimSpeed, can-alert subset: {dict(spd)}")
log(f"   AlertAnimSpeed, ALL resolved slots: {dict(spd_all)}   "
    "<-- Lap AB Sect5.3 said 'every resolved slot carries 1.0'; it is 92/94, not 94/94")
for r in sub:
    if r["anim_speed"] != "1.0":
        log(f"      exception: {r['record']} chance={r['alert_anim_chance']} "
            f"frames={r['frames']} speed={r['anim_speed']} actors={r['n_rostered_actors']}")

(OUT / "alert_incidence.json").write_text(json.dumps({
    "source_csv": str(AB_CSV), "source_csv_sha256": want,
    "buckets": [{"alertAnimChance": k[0], "status": k[1],
                 "records": buckets[k], "rostered_actors": bactors[k]}
                for k in sorted(buckets, key=lambda k: (k[1], k[0]))],
    "records_that_can_alert": len(can),
    "actors_that_can_alert": sum(a for _, _, a in can),
    "rostered_actors_total": tot,
    "expected_alerting_actors_full_roster": round(exp, 4),
    "can_alert_duration": {
        "resolved_slots": len(fr),
        "frames": {"min": min(fr), "p25": q[0], "median": statistics.median(fr),
                   "p75": q[2], "max": max(fr)},
        "seconds_frames_minus_1_over_30": {
            "min": round((min(fr) - 1) / 30, 4),
            "median": round((statistics.median(fr) - 1) / 30, 4),
            "max": round((max(fr) - 1) / 30, 4)},
        "alert_anim_speed_can_alert": dict(spd),
        "alert_anim_speed_all_resolved": dict(spd_all),
    },
}, indent=2) + "\n")

log("\nAnger arithmetic:")
log(dump("05-AngerManager-GetAngerDiff.asm", E["?GetAngerDiff@AngerManager@GAME@@QBEMI@Z"], 0x30))
log(dump("06-AngerManager-Update-baseline-snapshot.asm", E["?Update@AngerManager@GAME@@QAEXHM_N0@Z"] + 0xC0, 0x40))
log(f"   AddAnger clamp ceiling 0x105f58e8 = {f32(GAME, 0x105f58e8)}")

# ============================================================ § 3  HALF 2 — DURATION
log("")
log("=" * 78)
log("HALF 2 — DURATION")
log("=" * 78)

AB = {k.split("@")[0].lstrip("?"): v for k, v in E.items()
      if "ControllerMonsterStateAlertBeforePursue" in k and k.startswith("?")}
log(f"\nAlertBeforePursue members: { {k: hex(v) for k, v in sorted(AB.items())} }")
log(dump("07-AlertBeforePursue-OnBegin.asm", AB["OnBegin"], 0x20))
log(dump("08-AlertBeforePursue-HandleEvent.asm", AB["HandleEvent"], 0xA5))
log(f"   HandleEvent event-name literal 0x1052d3f4 = {cstr(GAME, 0x1052d3f4)!r}")

vt = E["??_7ControllerMonsterStateAlertBeforePursue@GAME@@6B@"]
rows = vtable(GAME, vt, 0x48, SYM_G)
log(f"\nAlertBeforePursue vtable @ {vt:#x} — the slots the decode uses:")
for off, f, s in rows:
    if off in (0x34, 0x108, 0x10C, 0x110, 0x114, 0x118):
        log(f"   +{off:#05x}  {f:#010x}  {s}")
log(dump("09-SetDone-IsDone.asm", 0x5E050, 0x20))

log("\nControllerAI event routing + temporary-state pop:")
log(dump("10-ControllerAI-HandleEvent.asm", E["?HandleEvent@ControllerAI@GAME@@UAEXABVName@2@@Z"], 0x35))
log(dump("11-ControllerAI-Update-pop.asm", E["?Update@ControllerAI@GAME@@UAEXH@Z"], 0xD0))

log("\nWho emits the 'End' animation event — EVERY standalone \"End\" literal in Engine.dll:")
for v in standalone_literals(ENG, "End"):
    rs = refs_to_va(ENG, v)
    log(f"   {v:#x}  refs={[(hex(r), SYM_E(r)) for r in rs]}")
log(dump("12-Engine-anim-End-emission.asm", 0x31133, 0x95, pe=ENG))
log(dump("13-Engine-anim-end-crossing-predicate.asm", 0x30577, 0x60, pe=ENG))

log("\nCharacter::AnimationCallback — the 'End' branch, and the animation event vocabulary:")
log(dump("14-Character-AnimationCallback-End-branch.asm", 0x45CB0, 0x40))
o = GAME.rva_to_off(0x104F4EB8 - GAME.image_base)
vocab = GAME.raw[o:o + 160].split(b"\0")
log(f"   animation event names @ 0x104f4eb8: {[x.decode() for x in vocab if x]}")

log("\n.anm header -> GraphicsAnim fields (independent confirmation of Lap AB's field ids):")
log(dump("15-GraphicsAnim-LoadANMData-header.asm", 0x876A0, 0x40, pe=ENG))
log(dump("16-GraphicsAnim-GetLength-GetFrameRate.asm", 0x889A0, 0x20, pe=ENG))
log(f"   ms->s constant 0x102e0400 = {f32(ENG, 0x102e0400)}")
log(f"   1.0f          0x102e0594 = {f32(ENG, 0x102e0594)}")

log("\nControllerAI::PlayAnimation -> PlayAnimationAction -> AnimationSet::PlayAnimation:")
log(dump("17-ControllerAI-PlayAnimation.asm", E["?PlayAnimation@ControllerAI@GAME@@QAEXW4AnimationSet_Type@2@ABVName@2@M_NI@Z"], 0xCA))
log(dump("18-AnimationSet-PlayAnimation.asm", E["?PlayAnimationIfAvailable@AnimationSet@GAME@@QAE?B_NAAVActor@2@W4AnimationSet_Type@2@ABVName@2@M_NI@Z"], 0x55))
log(dump("19-AnimChannel-PlayAnimation.asm", 0x31480, 0xF8, pe=ENG))

(OUT / "decode.log").write_text("\n".join(LOG) + "\n")

manifest = {
    "lap": LAP,
    "instrument": pathlib.Path(__file__).name,
    "pins": {str(p): v for p, v in PIN.items()},
    "evidence": sorted(p.name for p in OUT.iterdir()),
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"\n[ok] evidence -> {OUT}")
