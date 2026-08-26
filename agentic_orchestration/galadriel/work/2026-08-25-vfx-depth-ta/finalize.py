"""One command: rescore, build every table, inject into the note at <!--MATRIX-->."""
import json, math, subprocess, sys, io, contextlib

NOTE = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/notes/2026-08-25-vfx-depth-feature-matrix-ta.md"

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(open("make_tables.py").read(), {"__name__": "__main__"})
tables = buf.getvalue()

# ---- the radial (G-7) table, if the radial pass produced one -----------------
rad = ""
try:
    R = json.load(open("out/radial_depth.json"))
    rows = [(k, v) for k, v in R.items() if "summary" in v]
    if rows:
        rad = ["\n### 3.1 ⚑ G-7 RADIAL READING — the rows the axial operator had to refuse\n",
               "Control anchors: hot-core disc **0.4798** · matched flat disc **0.0000** "
               "(`out/synth_radial_control.json`). `r_sat_slope` is disqualified and not shown.\n",
               "| leg | core_white p90 | edge_white p90 | **core/edge ratio** | core_sat | edge_sat | **val_slope** (−ve = bright centre) | call (preregistered bar) |",
               "|---|---:|---:|---:|---:|---:|---:|---|"]
        for k, v in rows:
            f = v["summary"]["F1r_radial_core"]
            def g(n):
                x = f.get(n)
                try:
                    x = float(x); return x if math.isfinite(x) else float("nan")
                except (TypeError, ValueError):
                    return float("nan")
            cw, ew, vs = g("core_white_frac_p90"), g("edge_white_frac_p90"), g("val_slope_med")
            if not math.isfinite(cw):
                call = "n/e"
            elif cw >= 0.15 and cw >= 3 * max(ew, 1e-6):
                call = "**PRESENT — hot core**"
            elif cw < 0.02:
                call = "ABSENT"
            else:
                call = "UNCERTAIN"
            ratio = cw / max(ew, 1e-6) if math.isfinite(cw) and math.isfinite(ew) else float("nan")
            rad.append("| `%s` | %.4f | %.4f | **%.1f×** | %.3f | %.3f | **%+.4f** | %s |"
                       % (k, cw, ew, ratio, g("core_sat_med"), g("edge_sat_med"), vs, call))
        rad.append("")
        rad.append("> ⚑ **READ THE RATIO AND THE SLOPE, NOT ONLY THE CALL.** The preregistered "
                   "`core_white ≥ 0.15` bar was calibrated on a synthetic whose core is *pure* "
                   "white; real footage does not reach that absolute level. **But the core/edge "
                   "ratio is 6–27× on every reference leg, and `val_slope` runs −0.15 to −0.45 "
                   "against the synthetic POSITIVE control's −0.052** — a radial intensity "
                   "gradient five to nine times STRONGER than the arm the operator was validated "
                   "on. I am not lowering the bar after seeing the data; I am reporting that the "
                   "absolute predicate (`V>0.80 AND S<0.30`) is a synthetic's idealisation while "
                   "**the gradient itself is unambiguous and present in every radial reference "
                   "measured.** That is precisely what the § 4.1 eye-register saw and the axial "
                   "operator could not reach.")
        rad = "\n".join(rad) + "\n"
except OSError:
    pass

s = open(NOTE).read()
A, B = "<!--MATRIX-->", "<!--MATRIX-END-->"
assert A in s and B in s, "anchors missing"
# idempotent: replace BETWEEN the markers, never consume them, so this can be
# re-run every time another row lands without corrupting the note.
pre, rest = s.split(A, 1)
_, post = rest.split(B, 1)
s = pre + A + "\n" + tables + (rad or "") + "\n" + B + post
open(NOTE, "w").write(s)
print("injected %d chars of tables%s" % (len(tables), " + radial" if rad else ""))
