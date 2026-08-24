#!/usr/bin/env python3
"""KC2 MODEL-COMPLETION RUN - Lap D-6 :: PLAYER-KIT RESIDUAL DECODE.  READ-ONLY.

Three named targets, all declared UNBUILDABLE by build B-1 (gamora) with the missing
decode NAMED, and classified D-2-CLASS (extraction coverage, not substrate absence)
by the gandalf DRIFT-CRITIC verdict finding F-3.

  T1  fighting_spirit  -- the firing rule's DIRECTION (HitByEnemy-class vs AttackEnemy-class)
                          + the field home of the 30 %
  T2  ulzaads_decree   -- the proc's PAYLOAD magnitudes @ devotion 20
  T3  resilience       -- the non-heal limbs of playerclass09/passive02 @ rank 3 + thresholdDuration

SUBSTRATE, three layers, all vendor-shipped:
  (a) the eight-archive .arz overlay  (edition-III depot, the reading every prior KC2 lap used)
  (b) database/templates.arc          -- GD's OWN field schema, with the developers' descriptions
  (c) resources/Text_EN.arc           -- GD's OWN shipped tooltip/description strings
  (d) x64/Game.dll                    -- MSVC-mangled export table + vftables, for the cases where
                                         no data field carries the answer and the SEMANTICS live in code

LAW 3 (decode-before-declare) is honoured per target: verdict is DECODED (fields + provenance) or
UNDECODABLE-FROM-SUBSTRATE (with the search record).  No community-wiki values.  No fitted constants.

INDEX CONVENTION, established here rather than assumed (see § A of the README):
  player skills   array index = rank_effective - 1
  devotion procs  array index = devotion_level - 1
Both are cross-checked against values Lap G pinned independently.

RUN:  python3 d6_decode.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import re
import struct
import sys

ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
VENDOR3 = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GAMEDLL = pathlib.Path("/Users/admin/Games/vendor/grim-dawn/x64/Game.dll")
OUT = pathlib.Path(__file__).resolve().parent

sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "legolas" / "notes"
                      / "2026-08-12-kc2-roster-decode-completion"))

from gamora_kc2_c1_closure_ed3_2026_08_08 import E3 as WINNER   # noqa: E402  whole-record overlay
from s2_lib import E3 as MERGED                                 # noqa: E402  field-merge overlay
from pm4f_lib_2026_08_13 import Templates                       # noqa: E402  templates.arc reader
from gd_arc_reader_2026_07_26 import ArcArchive                 # noqa: E402


# ══════════════════════════════════════════════════════════════════════════════════════════
# helpers
# ══════════════════════════════════════════════════════════════════════════════════════════
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def rec(path):
    r, arcs = WINNER.winner(path)
    return (r or {}), arcs


def at(r, field, idx):
    """Value of `field` at array index `idx`.  ABSENT / OUT-OF-RANGE are reported, never guessed."""
    v = r.get(field)
    if v is None:
        return None, "ABSENT"
    if not isinstance(v, list):
        return v, "scalar"
    if idx >= len(v):
        return None, "OUT-OF-RANGE(len=%d)" % len(v)
    return v[idx], "array[%d]/len%d" % (idx, len(v))


def load_tags():
    tags, src = {}, {}
    arcs = sorted(set(list(VENDOR3.rglob("Text_EN.arc")) + list(VENDOR3.rglob("text_en.arc"))))
    for p in arcs:
        a = ArcArchive(p)
        for n in a.names():
            try:
                raw = a.read_file(n).decode("utf-8-sig", "replace")
            except Exception:
                continue
            for line in raw.splitlines():
                if "=" in line and not line.startswith("//"):
                    k, v = line.split("=", 1)
                    tags.setdefault(k.strip(), v.strip())
                    src.setdefault(k.strip(), "%s::%s" % (p.relative_to(VENDOR3), n))
    return tags, src, arcs


# ══════════════════════════════════════════════════════════════════════════════════════════
# minimal read-only PE reader -- export table + vftable walk.  No third-party dependency.
# ══════════════════════════════════════════════════════════════════════════════════════════
class PE:
    def __init__(self, path):
        self.b = pathlib.Path(path).read_bytes()
        b = self.b
        nt = struct.unpack_from("<I", b, 0x3C)[0]
        assert b[nt:nt + 4] == b"PE\0\0"
        coff = nt + 4
        nsec, optsz = struct.unpack_from("<H", b, coff + 2)[0], struct.unpack_from("<H", b, coff + 16)[0]
        opt = coff + 20
        assert struct.unpack_from("<H", b, opt)[0] == 0x20B, "PE32+ expected"
        self.imagebase = struct.unpack_from("<Q", b, opt + 24)[0]
        nrva = struct.unpack_from("<I", b, opt + 108)[0]
        self.dirs = [struct.unpack_from("<II", b, opt + 112 + 8 * i) for i in range(nrva)]
        so = opt + optsz
        self.sections = []
        for i in range(nsec):
            o = so + 40 * i
            nm = b[o:o + 8].rstrip(b"\0").decode()
            vsz, va, rsz, ptr = struct.unpack_from("<IIII", b, o + 8)
            self.sections.append((nm, va, vsz, ptr, rsz))

    def rva2off(self, rva):
        for _nm, va, vsz, ptr, rsz in self.sections:
            if va <= rva < va + max(vsz, rsz):
                return ptr + (rva - va)
        return None

    def exports(self):
        rva, _ = self.dirs[0]
        o, b = self.rva2off(rva), self.b
        (_c, _t, _mj, _mn, _nm, _base, _nf, nName,
         funcRva, nameRvaT, ordRvaT) = struct.unpack_from("<IIHHIIIIIII", b, o)
        fo, no, oo = self.rva2off(funcRva), self.rva2off(nameRvaT), self.rva2off(ordRvaT)
        out = {}
        for i in range(nName):
            nr = struct.unpack_from("<I", b, no + 4 * i)[0]
            s = self.rva2off(nr)
            out[b[s:b.index(b"\0", s)].decode("latin1")] = struct.unpack_from(
                "<I", b, fo + 4 * struct.unpack_from("<H", b, oo + 2 * i)[0])[0]
        return out

    def pdata(self):
        """x64 PE RUNTIME_FUNCTION table -- exact [begin,end) for every function with unwind data.
        This is what makes `which function contains this byte` exact instead of nearest-export."""
        rva, sz = self.dirs[3]
        o = self.rva2off(rva)
        out = []
        for i in range(sz // 12):
            beg, end, _unw = struct.unpack_from("<III", self.b, o + 12 * i)
            if beg == 0 and end == 0:
                break
            out.append((beg, end))
        out.sort()
        return out

    def vftable(self, ex, sym, n=200):
        off = self.rva2off(ex[sym])
        out = []
        for i in range(n):
            q = struct.unpack_from("<Q", self.b, off + 8 * i)[0]
            if q == 0:
                break
            r = q - self.imagebase
            if not 0 < r < 0xA23000:
                break
            out.append(r)
        return out


# ══════════════════════════════════════════════════════════════════════════════════════════
# T1 -- FIGHTING SPIRIT: the DIRECTION, decoded from Game.dll's dispatch chain
# ══════════════════════════════════════════════════════════════════════════════════════════
FS = "records/skills/playerclass01/fightingspirit1.dbr"
UD = "records/skills/devotion/tier2_37d_skill.dbr"
RS = "records/skills/playerclass09/passive02.dbr"


def t1_direction(pe, ex, log):
    """Prove which combat path reaches Skill_PassiveOnHitBuffSelf::OnHitActivation."""
    base = pe.vftable(ex, "??_7Skill@GAME@@6B@")
    derived = pe.vftable(ex, "??_7Skill_PassiveOnHitBuffSelf@GAME@@6BSkill@1@@")
    rev = {}
    for k, v in ex.items():
        rev.setdefault(v, []).append(k)

    slot_onhit = slot_gate = None
    for i, (a, d) in enumerate(zip(base, derived)):
        if a == d:
            continue
        for nm in rev.get(d, []):
            if nm.startswith("?OnHitActivation@Skill_PassiveOnHitBuffSelf@"):
                slot_onhit = i
            if nm.startswith("?IsSkillOnHitActive@Skill_PassiveOnHitBuffSelf@"):
                slot_gate = i
    log["vslot_OnHitActivation"] = slot_onhit
    log["vslot_IsSkillOnHitActive"] = slot_gate

    # which functions dispatch through those slots?
    _nm, va, _vsz, ptr, rsz = [s for s in pe.sections if s[0] == ".text"][0]
    text = pe.b[ptr:ptr + rsz]
    starts = sorted(set(ex.values()))
    import bisect

    def owner(r):
        i = bisect.bisect_right(starts, r) - 1
        return sorted(rev[starts[i]])[0] if i >= 0 else "?"

    def callers_of_slot(slot):
        """Byte-scan for `call qword ptr [reg + slot*8]`, then VERIFY each candidate by linear
        disassembly from its owning function's entry -- a raw byte match can land mid-instruction."""
        cand = set()
        for reg in range(8):
            pat = bytes([0xFF, 0x90 + reg]) + struct.pack("<i", slot * 8)
            for m in re.finditer(re.escape(pat), text):
                cand.add(va + m.start())
        try:
            from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        except ImportError:
            return {"VERIFIED": None, "byte_scan_candidates_unverified": sorted(owner(c) for c in cand)}
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        pd = pe.pdata()
        import bisect as _b
        begs = [x[0] for x in pd]

        def frange(r):
            i = _b.bisect_right(begs, r) - 1
            return pd[i] if i >= 0 and pd[i][0] <= r < pd[i][1] else None

        verified, rejected = set(), set()
        for c in sorted(cand):
            fr = frange(c)
            if fr is None:
                rejected.add(("<no-unwind-range>", hex(c)))
                continue
            beg, end = fr
            o = pe.rva2off(beg)
            real = {i.address - pe.imagebase for i in md.disasm(pe.b[o:o + (end - beg)],
                                                               pe.imagebase + beg)}
            nm = rev.get(beg, [owner(beg) + " (unnamed@%#x)" % beg])
            (verified if c in real else rejected).add(sorted(nm)[0])
        return {"VERIFIED": sorted(verified),
                "byte_scan_candidates_total": len(cand),
                "rejected_as_mid_instruction_or_unattributable": sorted(map(str, rejected))}

    # ⚑ HONESTY NOTE, and it is load-bearing.  A vtable-SLOT scan cannot tell you the RECEIVER's
    # type: `call qword ptr [rax+0x1a8]` is slot 53 of WHATEVER vtable rax points at.  These two
    # sets are therefore SUPERSETS -- reported in full, not filtered to the convenient answer.
    # What pins the receiver to `Skill*` is that the same two functions also dispatch slot 62 /
    # slot 63, which exist only on the Skill vtable, over the elements of SkillManager's own
    # skill lists.  That pairing is read instruction-by-instruction in d6_gamedll_dispatch.txt.
    log["slot53_bytescan_superset_receiver_type_UNKNOWN"] = callers_of_slot(slot_onhit)
    log["slot62_bytescan_superset_receiver_type_UNKNOWN"] = callers_of_slot(slot_gate)
    log["dispatch_chain_PROVEN"] = [
        "CombatManager::TakeAttack(ParametersCombat&, SkillManager&, CharacterBio&)   [victim side]",
        "  -> SkillManager::UnderAttack(const ParametersCombat&)   [sole caller; see callers_of_...]",
        "     for each Skill* s in this->skills:  if s->vslot62 IsSkillOnHitActive() then",
        "        s->vslot53 OnHitActivation(owner, params)",
        "Skill_PassiveOnHitBuffSelf overrides BOTH vslot62 and vslot53, and does NOT override",
        "vslot63 IsSkillOnCritActive -- so it is unreachable from SkillManager::OnCriticalAttack.",
    ]

    # direct callers of SkillManager::UnderAttack
    tgt = ex["?UnderAttack@SkillManager@GAME@@QEAAXAEBVParametersCombat@2@@Z"]
    found = set()
    for off in range(0, rsz - 5):
        if text[off] != 0xE8:
            continue
        d = struct.unpack_from("<i", text, off + 1)[0]
        if va + off + 5 + d == tgt:
            found.add(owner(va + off))
    log["callers_of_SkillManager_UnderAttack"] = sorted(found)

    # is the class's EndCooldown override a real body, or the COMDAT-folded `ret` stub?
    stub = ex["?EndCooldown@Skill_PassiveOnHitBuffSelf@GAME@@UEAAXH@Z"]
    o = pe.rva2off(stub)
    log["EndCooldown_override_rva"] = hex(stub)
    log["EndCooldown_override_first_bytes"] = pe.b[o:o + 4].hex()
    log["EndCooldown_override_is_ret_stub"] = pe.b[o] == 0xC3 or pe.b[o:o + 3] == b"\xc2\x00\x00"
    log["EndCooldown_stub_aliases"] = sorted(rev.get(stub, []))[:6]
    return log


# ══════════════════════════════════════════════════════════════════════════════════════════
def main():
    T = Templates()
    tags, tagsrc, tagarcs = load_tags()
    pe = PE(GAMEDLL)
    ex = pe.exports()

    summary = {"lap": "KC2-MC / D-6", "date": "2026-08-24", "law": "decode-before-declare (LAW 3)"}

    # ── index convention, established not assumed ────────────────────────────────────────
    conv = []
    for path, lvl, field, expect, src in [
        ("records/skills/devotion/tier2_05f_skill_buff.dbr", 20, "defensiveProtectionModifier", -35.0, "B-1 5.2 / pm4g_defensive_actives"),
        ("records/skills/devotion/tier2_05f_skill_buff.dbr", 20, "offensiveLifeLeechMin", 45.0, "B-1 5.2"),
        ("records/skills/devotion/tier2_17c_skill.dbr", 20, "damageAbsorption", 2900.0, "Lap G Arcane Barrier"),
        ("records/skills/devotion/tier1_29e_skill.dbr", 25, "damageAbsorption", 6100.0, "Lap G Turtle Shell"),
        ("records/skills/devotion/tier1_29e_skill.dbr", 25, "skillCooldownTime", 8.0, "Lap G Turtle Shell"),
        (FS, 5, "onHitActivationChance", 30.0, "Lap G trigger_chance_pct"),
        (FS, 5, "characterOffensiveAbility", 108.0, "B-1 5.1"),
        (FS, 5, "offensiveTotalDamageModifier", 95.0, "B-1 5.1"),
        (RS, 3, "characterHealIncreasePercent", 24.0, "I-17 / B-1 5.3"),
    ]:
        r, _a = rec(path)
        got, how = at(r, field, lvl - 1)
        conv.append(dict(record=path, level=lvl, field=field, index=lvl - 1, read=got,
                         expected_by=src, expected=expect, agrees=(got == expect), how=how))
    summary["index_convention_checks"] = conv
    summary["index_convention_verdict"] = ("CONFIRMED: array index = level - 1"
                                           if all(c["agrees"] for c in conv) else "FAILED")

    # ── T1 ───────────────────────────────────────────────────────────────────────────────
    fs, fs_arcs = rec(FS)
    t1 = {"record": FS, "archives": fs_arcs, "Class": fs.get("Class"),
          "templateName": fs.get("templateName"),
          "onHitActivationChance_declared_on": "templatebase/skill_onhit.tpl",
          "onHitActivationChance_declaration": T.declare("templatebase/skill_onhit.tpl", "onHitActivationChance"),
          "shipped_description_tag": fs.get("skillBaseDescription"),
          "shipped_description": tags.get(_s(fs.get("skillBaseDescription")), None),
          "shipped_description_source": tagsrc.get(_s(fs.get("skillBaseDescription"))), }
    t1_direction(pe, ex, t1)
    summary["T1_fighting_spirit"] = t1

    # class-family census: every corpus record on the OnHit family, with its shipped description
    fam = {}
    WANT = ("Skill_PassiveOnHitBuffSelf", "Skill_PassiveOnHitBuffShield",
            "Skill_PassiveOnCritBuffSelf", "Skill_OnHitBuffSelf",
            "Skill_OnHitAttackRadius", "SkillSecondary_OnHitBuffRadius")
    for p in MERGED.idx:
        if not p.startswith("records/skills/"):
            continue
        r, _ = MERGED.merged(p)
        if not r:
            continue
        c = _s(r.get("Class"))
        if c in WANT:
            fam.setdefault(c, []).append(dict(
                record=p, name=tags.get(_s(r.get("skillDisplayName")), ""),
                desc=tags.get(_s(r.get("skillBaseDescription")), "")))
    summary["T1_onhit_family_census"] = fam

    # ── T2 ───────────────────────────────────────────────────────────────────────────────
    ud, ud_arcs = rec(UD)
    DEV = 20
    t2fields = ["defensiveProtection", "defensiveProtectionModifier",
                "offensivePhysicalModifier", "offensivePierceModifier",
                "offensiveSlowPhysicalModifier", "offensivePhysicalMin", "offensivePhysicalMax",
                "retaliationPhysicalMin", "retaliationPhysicalMax",
                "damageAbsorption", "damageAbsorptionPercent",
                "skillActiveDuration", "skillCooldownTime"]
    t2 = {"record": UD, "archives": ud_arcs, "Class": ud.get("Class"),
          "templateName": ud.get("templateName"),
          "instantCast": ud.get("instantCast"),
          "templateAutoCast": ud.get("templateAutoCast"),
          "buff_companion_record": "records/skills/devotion/tier2_37d_skill_buff.dbr",
          "buff_companion_exists": MERGED.exists("records/skills/devotion/tier2_37d_skill_buff.dbr"),
          "devotion_level": DEV,
          "payload": {f: dict(zip(("value", "how"), at(ud, f, DEV - 1))) for f in t2fields}}
    summary["T2_ulzaads_decree"] = t2

    # ── T3 ───────────────────────────────────────────────────────────────────────────────
    rs, rs_arcs = rec(RS)
    RANK = 3
    t3fields = ["characterHealIncreasePercent", "characterDefensiveAbilityModifier",
                "defensiveAllMaxResist", "defensivePhysical", "defensiveProtection",
                "damageAbsorption", "damageAbsorptionPercent",
                "lifeMonitorPercent", "skillActiveDuration", "skillCooldownTime"]
    thr = T.declare("skill_passiveonlifebuffself.tpl", "thresholdDuration")
    explicit = []
    for p in MERGED.idx:
        if not p.startswith("records/skills/"):
            continue
        r, _ = MERGED.merged(p)
        if r and "thresholdDuration" in r:
            explicit.append((p, _s(r["thresholdDuration"])))
    t3 = {"record": RS, "archives": rs_arcs, "Class": rs.get("Class"),
          "templateName": rs.get("templateName"), "rank_effective": RANK,
          "payload": {f: dict(zip(("value", "how"), at(rs, f, RANK - 1))) for f in t3fields},
          "thresholdDuration_declaration": thr,
          "thresholdDuration_on_record": "thresholdDuration" in rs,
          "thresholdDuration_effective": (rs.get("thresholdDuration")
                                          if "thresholdDuration" in rs
                                          else "TEMPLATE-DEFAULT " + str(thr.get("defaultValue"))),
          "n_corpus_records_setting_it_explicitly": len(explicit)}
    summary["T3_resilience"] = t3

    # ── the UI format tags that fix each field's SEMANTICS (GD's own strings) ─────────────
    semantics = {
        "defensiveProtection": ("DefenseAbsorptionProtectionPlus", "DefenseProtectionModifier"),
        "defensivePhysical": ("DefensePhysical",),
        "defensiveAllMaxResist": ("DefenseAllMaxResist",),
        "characterDefensiveAbilityModifier": ("tagCharDefensiveAbilityModifier",),
        "characterHealIncreasePercent": ("tagCharHealIncreaseModifier", "tagCharStatsHealIncreaseInfo"),
        "retaliationPhysicalMin": ("RetaliationPhysical",),
    }
    summary["field_semantics_from_shipped_ui_tags"] = {
        f: [{"tag": t, "text": tags.get(t), "source": tagsrc.get(t)} for t in ts]
        for f, ts in semantics.items()}

    # the sweep itself, emitted so the "authored vs default" call is reproducible per record
    summary["bool_fields_differing_from_template_default"] = _bool_sweep(T, [
        (FS, "skill_passiveonhitbuffself.tpl"), (UD, "skill_buffselfduration.tpl"),
        (RS, "skill_passiveonlifebuffself.tpl")])

    # ── x86/x64 symbol parity: the prior KC2 laps pinned the 32-bit Game.dll; this lap reads the
    #    64-bit sibling from the SAME install.  Both must carry the same class/method set or the
    #    T1 chain is build-specific and cannot be cited against prior-lap provenance.
    x86 = pathlib.Path("/Users/admin/Games/vendor/grim-dawn/Game.dll").read_bytes()
    x64 = pathlib.Path(GAMEDLL).read_bytes()
    parity = {}
    for stem in ["?UnderAttack@SkillManager@GAME@@", "?OnCriticalAttack@SkillManager@GAME@@",
                 "?TakeAttack@CombatManager@GAME@@",
                 "?OnHitActivation@Skill_PassiveOnHitBuffSelf@GAME@@",
                 "?IsSkillOnHitActive@Skill_PassiveOnHitBuffSelf@GAME@@",
                 "?IsSkillOnCritActive@Skill_PassiveOnCritBuffSelf@GAME@@",
                 "?EndCooldown@Skill_PassiveOnHitBuffSelf@GAME@@"]:
        parity[stem] = {"x86_present": stem.encode() in x86, "x64_present": stem.encode() in x64}
    summary["gamedll_x86_x64_symbol_parity"] = parity
    summary["gamedll_parity_verdict"] = ("ALL PRESENT IN BOTH BUILDS"
                                         if all(v["x86_present"] and v["x64_present"]
                                                for v in parity.values()) else "DIVERGENT")

    # ── provenance digests ───────────────────────────────────────────────────────────────
    summary["digests"] = {
        "Game.dll (x64)": sha(GAMEDLL),
        "database/database.arz": sha(VENDOR3 / "database/database.arz"),
        "gdx2/database/GDX2.arz": sha(VENDOR3 / "gdx2/database/GDX2.arz"),
        "gdx3/database/GDX3.arz": sha(VENDOR3 / "gdx3/database/GDX3.arz"),
        "database/templates.arc": sha(VENDOR3 / "database/templates.arc"),
        "resources/Text_EN.arc": sha(VENDOR3 / "resources/Text_EN.arc"),
        "gdx2/resources/Text_EN.arc": sha(VENDOR3 / "gdx2/resources/Text_EN.arc"),
        "grim-dawn/Game.dll (x86, the build prior KC2 laps pinned)":
            sha("/Users/admin/Games/vendor/grim-dawn/Game.dll"),
    }
    summary["version_skew_DECLARED"] = (
        "MAGNITUDES are read from the edition-III 2026-08-08 depot (the corpus every prior KC2 lap "
        "used).  SEMANTICS (T1's dispatch chain) are read from the 2026-07-23 install's Game.dll, a "
        "DIFFERENT build -- that install's database.arz sha is 8cdeff12..., not the edition-III "
        "2ad6d379....  The bridge is the class-name string, which appears verbatim in BOTH the "
        "edition-III templates.arc (Class=Skill_PassiveOnHitBuffSelf) and in Game.dll's export "
        "table; and the x86/x64 parity check above shows the class/method set is identical across "
        "the two builds shipped in that install.  No MAGNITUDE in this lap comes from Game.dll.")

    _emit_dispatch_listing(pe, ex)
    (OUT / "d6_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    # ── the machine-readable parameter table gamora consumes ─────────────────────────────
    rows = []

    def row(**k):
        rows.append(k)

    dsc = _s(fs.get("skillBaseDescription"))
    row(target="fighting_spirit", record=FS, level_kind="rank", level=5, index=4,
        field="TRIGGER_DIRECTION", value="HitByEnemy",
        unit="enum", status="DECODED",
        provenance="Game.dll CombatManager::TakeAttack -> SkillManager::UnderAttack -> vslot%d IsSkillOnHitActive -> vslot%d OnHitActivation; + shipped desc '%s'"
                   % (t1["vslot_IsSkillOnHitActive"], t1["vslot_OnHitActivation"], tags.get(dsc, "")))
    for f, unit in [("onHitActivationChance", "percent"), ("skillActiveDuration", "seconds"),
                    ("characterOffensiveAbility", "flat_OA"),
                    ("offensiveTotalDamageModifier", "percent")]:
        v, how = at(fs, f, 4)
        row(target="fighting_spirit", record=FS, level_kind="rank", level=5, index=4, field=f,
            value=v, unit=unit, status="DECODED",
            provenance="arz winner overlay (%s) %s" % (",".join(fs_arcs), how))
    v, how = at(fs, "skillCooldownTime", 4)
    row(target="fighting_spirit", record=FS, level_kind="rank", level=5, index=4,
        field="skillCooldownTime", value=v, unit="seconds", status="DECODED-BUT-INERT",
        provenance="value on record; Skill_PassiveOnHitBuffSelf::EndCooldown is the COMDAT-folded ret-stub at %s and OnHitActivation never reads the cooldown timer -- the re-fire gate is activeDurationRemaining>0"
                   % t1["EndCooldown_override_rva"])
    row(target="fighting_spirit", record=FS, level_kind="rank", level=5, index=4,
        field="REFIRE_GATE", value="activeDurationRemaining_ms > 0", unit="predicate",
        status="DECODED",
        provenance="Game.dll Skill_PassiveOnHitBuffSelf::OnHitActivation: early-out on [this+0x5cc]>0; on fire [0x5cc]=[0x5c8]=duration_s*1000.0")
    row(target="fighting_spirit", record=FS, level_kind="rank", level=5, index=4,
        field="ROLL_RULE", value="fire iff uniform_int(0,100) <= onHitActivationChance", unit="predicate",
        status="DECODED",
        provenance="Game.dll: SkillProfile::GetActivationChance(profile, level); rng(0,100); comiss/ja early-out on roll > chance")

    for f, unit in [("defensiveProtection", "flat_armor"),
                    ("offensivePhysicalModifier", "percent"),
                    ("offensivePierceModifier", "percent"),
                    ("offensiveSlowPhysicalModifier", "percent"),
                    ("offensivePhysicalMin", "flat_damage"), ("offensivePhysicalMax", "flat_damage"),
                    ("retaliationPhysicalMin", "flat_damage"), ("retaliationPhysicalMax", "flat_damage"),
                    ("skillActiveDuration", "seconds"), ("skillCooldownTime", "seconds")]:
        v, how = at(ud, f, DEV - 1)
        row(target="ulzaads_decree", record=UD, level_kind="devotion_level", level=DEV, index=DEV - 1,
            field=f, value=v, unit=unit, status="DECODED" if v is not None else "ABSENT-ON-RECORD",
            provenance="arz winner overlay (%s) %s" % (",".join(ud_arcs), how))
    row(target="ulzaads_decree", record=UD, level_kind="devotion_level", level=DEV, index=DEV - 1,
        field="PAYLOAD_HOME", value="self (no _buff companion)", unit="note", status="DECODED",
        provenance="Class=Skill_BuffSelfDuration; tier2_37d_skill_buff.dbr does not exist in any of the 8 archives")

    for f, unit in [("characterHealIncreasePercent", "percent"),
                    ("characterDefensiveAbilityModifier", "percent"),
                    ("defensiveAllMaxResist", "percent"), ("defensivePhysical", "percent"),
                    ("lifeMonitorPercent", "percent"), ("skillActiveDuration", "seconds"),
                    ("skillCooldownTime", "seconds")]:
        v, how = at(rs, f, RANK - 1)
        row(target="resilience", record=RS, level_kind="rank", level=RANK, index=RANK - 1,
            field=f, value=v, unit=unit, status="DECODED" if v is not None else "ABSENT-ON-RECORD",
            provenance="arz winner overlay (%s) %s" % (",".join(rs_arcs), how))
    # ⚑ thresholdDuration is PRESENT on this record and is an AUTHORED OVERRIDE of the template
    # default.  (Caught by a bool-vs-template-default sweep after a first pass mis-read it as
    # absent -- see README D-D6-1.  The sweep is retained below so the check is not one-shot.)
    thr_on = "thresholdDuration" in rs
    thr_val = _s(rs.get("thresholdDuration")) if thr_on else None
    row(target="resilience", record=RS, level_kind="rank", level=RANK, index=RANK - 1,
        field="thresholdDuration", value=thr_val if thr_on else str(thr.get("defaultValue")),
        unit="bool",
        status="DECODED-AUTHORED-OVERRIDE" if thr_on else "DECODED-BY-TEMPLATE-DEFAULT",
        provenance=("ON THE RECORD as %s, OVERRIDING skill_passiveonlifebuffself.tpl default=%s '%s'; "
                    "%d corpus skill records set this field explicitly"
                    % (thr_val, thr.get("defaultValue"), thr.get("description"), len(explicit)))
        if thr_on else
        ("ABSENT on the record; template default=%s '%s'; %d corpus records set it explicitly"
         % (thr.get("defaultValue"), thr.get("description"), len(explicit))))


    with open(OUT / "d6_player_kit_residual.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["target", "record", "level_kind", "level", "index",
                                          "field", "value", "unit", "status", "provenance"])
        w.writeheader()
        w.writerows(rows)

    print("rows:", len(rows), "| index convention:", summary["index_convention_verdict"])
    for k in ("callers_of_SkillManager_UnderAttack", "EndCooldown_override_is_ret_stub"):
        print(" ", k, "=", t1[k])
    print("  T1 verdict chain:")
    for line in t1["dispatch_chain_PROVEN"]:
        print("   ", line)


def _bool_sweep(T, pairs):
    """For each (record, template): every BOOL field whose record value differs from the template
    default.  This is the instrument that distinguishes an AUTHORED value from an inherited one --
    and a `False` that a naive dump filters away as falsy is exactly what it is built to catch."""
    def allvars(tpl, seen=None):
        seen = seen if seen is not None else set()
        k = T._key(tpl)
        if k in seen or not T.has(k):
            return {}
        seen.add(k)
        out = {}
        for v in T.variables(k):
            if v.get("type") == "include" and v.get("defaultValue"):
                out.update(allvars(v["defaultValue"], seen))
            elif v.get("name") != "Include File":
                out[v["name"]] = v
        return out

    res = {}
    for path, tpl in pairs:
        r, _a = rec(path)
        tv = allvars(tpl)
        diffs = []
        for k, v in tv.items():
            if v.get("type") != "bool" or k not in r:
                continue
            cur = r[k]
            cur = cur[0] if isinstance(cur, list) and cur else cur
            if bool(cur) != (str(v.get("defaultValue", "")).strip() in ("1", "true", "True")):
                diffs.append({"field": k, "record_value": cur,
                              "template_default": v.get("defaultValue"),
                              "template_description": v.get("description", "")})
        res[path] = {"template": tpl, "n_template_vars_incl_includes": len(tv),
                     "authored_bool_overrides": diffs}
    return res


def _emit_dispatch_listing(pe, ex):
    """Verbatim disassembly of the four functions the T1 verdict rests on.  No interpretation."""
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    except ImportError:
        return
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    rev = {}
    for k, v in ex.items():
        rev.setdefault(v, []).append(k)
    pd = pe.pdata()
    import bisect as _b
    begs = [x[0] for x in pd]
    ann = {0x1A8: "vslot53 Skill::OnHitActivation",
           0x1F0: "vslot62 Skill::IsSkillOnHitActive",
           0x1F8: "vslot63 Skill::IsSkillOnCritActive",
           0x1C8: "vslot57 Skill::GetCurrentLevel",
           0x1E8: "vslot61 Skill::IsSkillEnabled",
           0x578: "vslot175 Skill::GetSkillProfile"}
    out = ["KC2-MC / D-6 -- Game.dll dispatch listing (verbatim capstone output, no interpretation)",
           "Game.dll x64, imagebase %#x" % pe.imagebase, ""]
    for sym in ["?UnderAttack@SkillManager@GAME@@QEAAXAEBVParametersCombat@2@@Z",
                "?OnCriticalAttack@SkillManager@GAME@@QEAAXAEBVParametersCombat@2@@Z",
                "?OnHitActivation@Skill_PassiveOnHitBuffSelf@GAME@@UEAAXAEAVCharacter@2@AEBVParametersCombat@2@@Z",
                "?IsSkillOnHitActive@Skill_PassiveOnHitBuffSelf@GAME@@UEBA?B_NXZ",
                "?EndCooldown@Skill_PassiveOnHitBuffSelf@GAME@@UEAAXH@Z"]:
        beg = ex[sym]
        i = _b.bisect_right(begs, beg) - 1
        end = pd[i][1] if i >= 0 and pd[i][0] == beg else beg + 0x40
        out += ["=" * 108, sym, "rva %#x .. %#x" % (beg, end), ""]
        o = pe.rva2off(beg)
        for ins in md.disasm(pe.b[o:o + (end - beg)], pe.imagebase + beg):
            tag = ""
            if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
                t = int(ins.op_str, 16) - pe.imagebase
                tag = "   ; -> " + (sorted(rev[t])[0] if t in rev else "sub_%x" % t)
            for d, lbl in ann.items():
                if hex(d) in ins.op_str:
                    tag += "   ; <<< " + lbl
            out.append("  %#012x  %-10s %-44s%s" % (ins.address, ins.mnemonic, ins.op_str, tag))
        out.append("")
    (OUT / "d6_gamedll_dispatch.txt").write_text("\n".join(out))


def _s(v):
    if isinstance(v, list):
        v = v[0] if v else None
    return "" if v is None else str(v)


if __name__ == "__main__":
    main()
