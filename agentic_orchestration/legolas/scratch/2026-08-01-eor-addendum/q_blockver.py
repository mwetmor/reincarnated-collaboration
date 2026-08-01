"""Block-version comparison, 1.1.9.x-era .gdc vs 1.3.0.0-written .gdc. READ-ONLY.

Method: run the existing gdc_parse.py (whose want_ver constants are the pre-1.2
public reference) over both files and read the emitted 'VERSION DRIFT' notes.
Absence of a drift note == that block's version equals the pre-1.2 reference.
"""
import re, sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
import gdc_parse as G

REF = {"expansion_byte":3,"character_info":5,"character_bio":8,"inventory":4,
       "character_stash":6,"respawn_list":1,"teleport_list":1,"marker_list":1,
       "shrine_list":2,"character_skills":5,"lore_notes":1,"faction_pack":5,
       "ui_settings":5,"tutorial_pages":1,"play_stats":11,"trigger_tokens":2}

def vers(path):
    r = G.parse(path)
    v = dict(REF); v["file_version"] = r["file_version"]
    for n in r["notes"]:
        m = re.match(r"VERSION DRIFT: (\S+) version=(\d+)", n)
        if m: v[m.group(1)] = int(m.group(2))
        m = re.match(r"post-header byte = (\d+)", n)
        if m: v["expansion_byte"] = int(m.group(1))
    return v

OLD = vers('player.gdc.eor')                                   # 2022-08-13, 1.1.9.x
NEW = vers('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/'
           'legolas/scratch/2026-07-28-gdc-parse-g7/player.gdc.scratch')  # 1.3.0.0
print(f"{'block':20s}{'1.1.9.x (2022)':>16s}{'1.3.0.0 (2026)':>16s}   verdict")
for k in ["file_version","expansion_byte"] + list(REF):
    if k == "expansion_byte" and k in REF: pass
    print(f"{k:20s}{OLD.get(k)!s:>16s}{NEW.get(k)!s:>16s}   "
          f"{'same' if OLD.get(k)==NEW.get(k) else 'BUMPED'}")
