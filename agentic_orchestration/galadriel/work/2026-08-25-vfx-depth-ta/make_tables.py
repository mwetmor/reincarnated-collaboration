"""Emit the markdown tables for the note: call matrix, numeric appendix,
matched-pair comparison. One command, so assembly cannot drift from receipts."""
import json, math, subprocess, sys

subprocess.run([sys.executable, "score_matrix.py"], check=True, capture_output=True)
M = json.load(open("out/feature_matrix.json"))
D = json.load(open("out/ta_depth.json"))
try:
    O = json.load(open("out/ours_depth.json"))
except OSError:
    O = {}
ALL = dict(D); ALL.update(O)
for r, d in O.items():
    if "error" not in d:
        pass
# rescore including ours
if O:
    merged = dict(D); merged.update(O)
    json.dump(merged, open("out/ta_depth_merged.json", "w"), indent=2, default=str)

SY = {"PRESENT": "**P**", "ABSENT": "A", "UNCERTAIN": "?", "n/e": "n/e"}
FAM = ["F1 hot head", "F2 gradient", "F3 var width", "F4 sparks",
       "F5 smoke vol", "F6a scar", "F6b impact-distort", "F7 shake"]
ORDER = ["ground_targeted_circle", "melee_strike_CANON", "self_buff", "totem",
         "circle_ring", "circle_ring_alt", "single_target", "melee_arc", "aura",
         "multi_projectile", "line_weak", "dash_attack", "whirlwind",
         "ground_slam", "beam_channel", "blink", "cone", "orbit", "chain",
         "vortex_pull", "placed_lane", "ricochet_bounce", "teleport",
         "leap_strike", "fork"]
ORDER += [k for k in M if k not in ORDER]

def num(row, path, fmt="%.3f"):
    d = ALL.get(row, {})
    if "summary" not in d: return "—"
    cur = d["summary"]
    for p in path:
        if cur is None: return "—"
        cur = cur.get(p) if isinstance(cur, dict) else None
    try:
        v = float(cur)
        return fmt % v if math.isfinite(v) else "—"
    except (TypeError, ValueError):
        return "—" if cur is None else str(cur)

print("### CALL MATRIX\n")
print("| row | " + " | ".join(f.split(" ", 1)[0] for f in FAM) + " | CV | ev/s | peak/med | trip |")
print("|" + "|".join(["---"] * (len(FAM) + 5)) + "|")
for row in ORDER:
    r = M.get(row)
    if not r or "error" in r: continue
    cv = r["CV"]["cv"]; pm = r["CV"]["peak_over_median"]
    print("| `%s` | " % row + " | ".join(SY[r[f]["call"]] for f in FAM) +
          " | %s | %.2f | %s | %s |" % (
              "%.3f" % cv if cv is not None else "—",
              r["CV"]["events_per_s"] or 0.0,
              "%.0f" % pm if pm else "—",
              "⚑TRIP" if r["CV"]["trip_flag"] else "-"))

print("\n### NUMERIC APPENDIX\n")
cols = [("head_white p90", ["F1_head", "head_white_frac_p90"], "%.4f"),
        ("tail_white p90", ["F1_head", "tail_white_frac_p90"], "%.4f"),
        ("lead_known", ["F1_head", "lead_known_frac"], "%.2f"),
        ("val_slope", ["F2_gradient", "val_slope_med"], "%+.3f"),
        ("head_sat", ["F2_gradient", "head_sat_med"], "%.3f"),
        ("tail_sat", ["F2_gradient", "tail_sat_med"], "%.3f"),
        ("h/t width", ["F3_width", "head_tail_width_ratio_med"], "%.3f"),
        ("elong", ["F3_width", "elongation_med"], "%.2f"),
        ("sat_n", ["F4_sparks", "sat_count_med"], "%.0f"),
        ("sat_mass", ["F4_sparks", "sat_massfrac_p90"], "%.3f"),
        ("halo/core", ["F5_smoke", "halo_area_ratio_med"], "%.2f"),
        ("pan px/fr", ["F7_shake", "pan_mean_px"], "%.2f"),
        ("hf p99", ["F7_shake", "hf_p99_px"], "%.2f"),
        ("shake n", ["F7_shake", "n_shake_frames"], "%.0f")]
print("| row | " + " | ".join(c[0] for c in cols) + " |")
print("|" + "|".join(["---"] * (len(cols) + 1)) + "|")
for row in ORDER:
    if row not in M or "error" in M[row]: continue
    print("| `%s` | " % row + " | ".join(num(row, p, f) for _, p, f in cols) + " |")

print("\n### F6b SIGNED, and F7 LOCALISATION\n")
print("| row | F6b why | F7 why | F7 impact-enrichment |")
print("|---|---|---|---|")
for row in ORDER:
    if row not in M or "error" in M[row]: continue
    r = M[row]
    e = r["F7 shake"].get("impact_enrichment")
    print("| `%s` | %s | %s | %s |" % (row, r["F6b impact-distort"]["why"],
          r["F7 shake"]["why"], "%.1fx" % e if isinstance(e, float) and math.isfinite(e) else "—"))

PAIRS = [("dash_attack", "OURS_dash_attack"), ("blink", "OURS_blink"),
         ("teleport", "OURS_teleport"), ("leap_strike", "OURS_leap_strike"),
         ("ground_slam", "OURS_ground_slam"), ("melee_strike_CANON", "OURS_melee_combo")]
have = [(a, b) for a, b in PAIRS if a in M and b in M]
if have:
    print("\n### MATCHED PAIRS — reference vs ours, same operators, same raster\n")
    print("| row | leg | " + " | ".join(f.split(" ", 1)[0] for f in FAM) + " | CV | ev/s |")
    print("|" + "|".join(["---"] * (len(FAM) + 4)) + "|")
    for a, b in have:
        for lab, k in (("REF", a), ("OURS", b)):
            r = M[k]; cv = r["CV"]["cv"]
            print("| `%s` | %s | " % (a, lab) + " | ".join(SY[r[f]["call"]] for f in FAM) +
                  " | %s | %.2f |" % ("%.3f" % cv if cv is not None else "—",
                                      r["CV"]["events_per_s"] or 0.0))
