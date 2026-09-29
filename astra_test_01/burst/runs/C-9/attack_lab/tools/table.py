import json, sys, glob, os
B = sys.argv[1]
def g(mode, stack, act, frm):
    p = "%s/%s_s%s/%s_%s_R6.json" % (B, mode, stack, act, frm)
    return json.load(open(p)) if os.path.exists(p) else None
cols = [("root_excess_mm_per_24th", "root lurch", "mm/f"), ("fade_in_foot_travel_m", "fade-in foot", "m"),
        ("fade_in_foot_peak_m_s", "fade-in peak", "m/s"), ("fade_out_foot_travel_m", "fade-out foot", "m"),
        ("pose_pop_deg_per_24th", "pose pop", "deg/f"), ("windup_lower_foot_mm_per_24th_median", "wind-up foot", "mm/f")]
print("%-6s %-4s %-6s | " % ("action", "from", "") + " | ".join("%-14s" % (c[1] + " " + c[2]) for c in cols))
for act in ["slash", "chop", "bash", "block"]:
    for frm in ["idle", "run"]:
        for mode in ["before", "after"]:
            d = g(mode, 4, act, frm)
            if d is None: continue
            print("%-6s %-4s %-6s | " % (act, frm, mode) + " | ".join("%-14s" % d.get(c[0], "-") for c in cols))
print()
for frm in ["idle", "run"]:
    d = g("before", 0, "slash", frm)
    if d: print("UNARMED slash from %-4s (stack 0)  | " % frm + " | ".join("%-14s" % d.get(c[0], "-") for c in cols))
