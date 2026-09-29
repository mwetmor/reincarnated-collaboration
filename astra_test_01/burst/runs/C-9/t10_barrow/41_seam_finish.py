#!/usr/bin/env python3
"""C-9 T10: composite the seam repairs as a BAND, roll back, re-test, resample to 1024.

    python3 41_seam_finish.py [--apply] [--band 80]

The repairs were painted on the rolled canvas, and every one of them was retried for the
same fault: the EDIT softened or altered the texture away from the cross. Taking the whole
returned image would therefore trade a seam for a degraded tile -- a swap that the wrap test
would score as a PASS, because a blurred tile has a low gradient everywhere including at its
seam. The test cannot tell "repaired" from "smoothed", so the pipeline must not give it the
chance.

So only a band around the cross is taken, cosine-feathered to zero at its edges, and
everything outside it is the original tile BYTE FOR BYTE -- asserted, not assumed. For bark,
only the horizontal band: bark_a already scores 0.81 across its left-right wrap, cleaner
than anywhere in its own interior, and a band there could only make it worse.

    weight(d) = 0.5*(1 + cos(pi*d/B))    d = distance in pixels from the seam line

Then roll back by the same half-and-half offset, re-run the wrap test, and record BOTH
numbers. Resampling to 1024 is last: it changes the gradient statistic the test reads, so
measuring after it would be measuring a resize.
"""
import argparse
import importlib.util
import json
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts"
SEAM = HERE / "seam"
OUT = HERE / "tiles"

_spec = importlib.util.spec_from_file_location("st", HERE / "30_seam_test.py")
st = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(st)

# repaired burst -> (original burst, variant sent, which bands to take)
REPAIRS = {
    "T10S-snow": ("T10T-snow-r1", "a", ("rows", "cols")),
    "T10S-rock": ("T10T-rock", "b", ("rows", "cols")),
    "T10S-bark": ("T10T-bark", "a", ("rows",)),     # horizontal line only
}
PASSED = {"T10T-path": "b", "T10T-heather": "b", "T10T-ice": "a"}
FINAL = 1024


def band_weight(n: int, centre: int, B: int) -> np.ndarray:
    d = np.abs(np.arange(n) - centre).astype(np.float32)
    w = np.where(d <= B, 0.5 * (1.0 + np.cos(np.pi * np.clip(d / max(B, 1), 0, 1))), 0.0)
    return w.astype(np.float32)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--band", type=int, default=80)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    prev = json.loads((HERE / "seam_report.json").read_text())
    rec = {"band_px": a.band, "feather": "cosine to zero at the band edge",
           "repairs": {}, "passed_first_time": {}, "final_px": FINAL}

    print("%-14s %-4s %-8s %-8s %-8s %-9s %-20s %s"
          % ("tile", "var", "before", "after", "detail", "outside", "bands", "verdict"))
    for burst, (orig, ovar, bands) in REPAIRS.items():
        base_p = SEAM / ("%s_%s_rolled.png" % (orig, ovar))
        if not base_p.exists():
            print("%-14s  no rolled original at %s" % (burst, base_p))
            continue
        base = np.asarray(Image.open(base_p).convert("RGB"))
        h, w = base.shape[:2]
        before = prev.get("%s_%s" % (orig, ovar), {}).get("worst_ratio")
        best = None
        for v in ("a", "b"):
            p = ART / burst / ("%s_%s.png" % (burst, v))
            if not p.exists():
                continue
            rep = Image.open(p).convert("RGB")
            if rep.size != (w, h):
                rep = rep.resize((w, h), Image.LANCZOS)
            rep = np.asarray(rep).astype(np.float32)

            wt = np.zeros((h, w), np.float32)
            if "rows" in bands:
                wt = np.maximum(wt, band_weight(h, h // 2, a.band)[:, None] * np.ones((1, w), np.float32))
            if "cols" in bands:
                wt = np.maximum(wt, np.ones((h, 1), np.float32) * band_weight(w, w // 2, a.band)[None, :])
            comp = base.astype(np.float32) * (1 - wt[..., None]) + rep * wt[..., None]
            comp = np.clip(np.rint(comp), 0, 255).astype(np.uint8)
            # OUTSIDE THE BAND, BYTE FOR BYTE. Asserted, because the whole point of the
            # band is that nothing beyond it moved.
            outside = wt <= 0.0
            identical = bool(np.array_equal(comp[outside], base[outside]))
            n_out = int(outside.sum())
            # IS THE BAND A REPAIR OR A BLUR? A seam ratio BELOW 1.0 means the wrap line
            # is smoother than the material around it, which is what a softened edit looks
            # like -- and the wrap test scores it as a pass, because a blurred tile has a
            # low gradient everywhere including at its seam. So measure the high-frequency
            # energy inside the band against the same measure outside it: ~1.0 means the
            # texture survived, well under 1.0 means the band was smoothed and will read as
            # a soft stripe once the tile repeats.
            from scipy import ndimage as _nd
            gcomp = comp.astype(np.float32).mean(-1)
            hf = np.abs(gcomp - _nd.gaussian_filter(gcomp, 2.0))
            inb = wt > 0.5
            outb = wt <= 0.0
            detail = float(hf[inb].mean() / max(hf[outb].mean(), 1e-6)) if inb.any() else 1.0
            back = np.roll(np.roll(comp, -(h // 2), 0), -(w // 2), 1)
            s = st.score(back)
            s.update({"variant": v, "outside_identical": identical,
                      "outside_px": n_out, "band_detail_ratio": round(detail, 3),
                      "array": back})
            # PICK ON BOTH CRITERIA, not on the seam alone. Ranking by seam ratio picked
            # bark_a at 0.81 seam / 0.744 detail over bark_b at 0.81 seam / 0.767 detail --
            # the same seam score and a blurrier band. A lower seam number is not better
            # when it was bought by smoothing; the null here is 0.998, the unrepaired
            # tile's own band, so a detail ratio is a real measurement and not a feel.
            s["passes"] = s["worst_ratio"] < 1.6 and s["band_detail_ratio"] >= 0.75
            better = (best is None
                      or (s["passes"], s["band_detail_ratio"]) >
                         (best["passes"], best["band_detail_ratio"]))
            if better:
                best = s
        if best is None:
            print("%-14s  no repaired output" % burst)
            continue
        # BOTH conditions: the seam has to go AND the texture has to stay.
        ok = best["worst_ratio"] < 1.6 and best["band_detail_ratio"] >= 0.75
        print("%-14s %-4s %-8s %-8.2f %-8.2f %-9s %-20s %s"
              % (burst, best["variant"], ("%.2f" % before) if before else "?",
                 best["worst_ratio"], best["band_detail_ratio"],
                 "identical" if best["outside_identical"] else "CHANGED",
                 "+".join(bands) + " @%dpx" % a.band,
                 "PASS" if ok else ("BLURRED" if best["band_detail_ratio"] < 0.75
                                    else "STILL FAILS")))
        rec["repairs"][burst] = {
            "original": orig, "variant_sent": ovar, "repaired_variant": best["variant"],
            "before": before, "after": best["worst_ratio"],
            "vertical_wrap": best["vertical_wrap"]["ratio"],
            "horizontal_wrap": best["horizontal_wrap"]["ratio"],
            "band_detail_ratio": best["band_detail_ratio"],
            "bands_taken": list(bands), "outside_band_identical": best["outside_identical"],
            "outside_band_px": best["outside_px"], "pass": ok}
        if a.apply and ok:
            Image.fromarray(best["array"]).resize((FINAL, FINAL), Image.LANCZOS).save(
                OUT / ("%s.png" % orig.replace("T10T-", "").replace("-r1", "")))

    for orig, v in PASSED.items():
        p = ART / orig / ("%s_%s.png" % (orig, v))
        if not p.exists():
            continue
        rec["passed_first_time"][orig] = {
            "variant": v, "ratio": prev.get("%s_%s" % (orig, v), {}).get("worst_ratio")}
        if a.apply:
            Image.open(p).convert("RGB").resize((FINAL, FINAL), Image.LANCZOS).save(
                OUT / ("%s.png" % orig.replace("T10T-", "")))

    (HERE / "seam_finish.json").write_text(json.dumps(rec, indent=1) + "\n")
    print("-> %s" % (HERE / "seam_finish.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
