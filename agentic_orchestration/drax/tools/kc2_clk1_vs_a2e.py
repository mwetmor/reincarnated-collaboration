#!/usr/bin/env python3
"""
kc2_clk1_vs_a2e.py — SB-1 Cell CLK-1 item 3(b). THE FIX'S VISUAL DELTA, MEASURED.

    python3 agentic_orchestration/drax/tools/kc2_clk1_vs_a2e.py \
        --render /tmp/kc2_clk1_a2e/<seg>-<shot> --segment B-undulating --shot d-close

WHY THIS EXISTS. Cell A2f's landing said the clock fix "changes every body in
every frame". That is a sentence, and the conductor has to hand Matt a NUMBER.
The reference is the sha-pinned clip Matt actually watched —
`captures/2026-08-13-sb1-a2e-cpbprime/cpbprime-cadence-ab.mp4` @
e2f6a03cc49042e69bd16c35dcc69c03254733f281e2b4e73e87253888580c91 — and the
digest is re-verified from bytes here before a single frame is read (GL-6
discipline applied to a deliverable rather than to the baton).

WHAT IT COMPARES, AND THE FLOOR IT REPORTS SO THE NUMBER MEANS SOMETHING.
The reference is H.264 at CRF 12, so a decoded reference frame is NOT the frame
that was rendered. Comparing a fresh PNG render against it therefore measures

    codec error  +  the A2e clock jitter  +  whatever the fix changed

and quoting the sum as "the fix's delta" would be inflating it. So this reports
the CODEC FLOOR alongside: the same rendered frames encoded with the A2e
settings and decoded back, differenced against themselves. Everything above that
floor is scene change; everything at it is the encoder.

Frames are streamed from ffmpeg as rawvideo — 1,004 frames of 1920x1080 PNG on
disk is 2 GB of intermediate to say one number.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

A2E_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "galadriel/captures/2026-08-13-sb1-a2e-cpbprime"
)
A2E_MP4 = A2E_DIR / "cpbprime-cadence-ab.mp4"
A2E_SHA = "e2f6a03cc49042e69bd16c35dcc69c03254733f281e2b4e73e87253888580c91"
W, H, FPS = 1920, 1080, 30

# The A2e timeline, read from its own MANIFEST rather than retyped.
def a2e_segment_bounds() -> dict[tuple[str, str], tuple[int, int]]:
    man = json.loads((A2E_DIR / "MANIFEST.json").read_text())
    out: dict[tuple[str, str], tuple[int, int]] = {}
    for row in man["timeline"]:
        if row["segment"] == "SEAM":
            continue
        f0 = int(round(row["starts_at_s"] * FPS))
        f1 = int(round(row["ends_at_s"] * FPS))
        out[(row["segment"], row["shot"])] = (f0, f1)
    return out


def verify_reference() -> None:
    h = hashlib.sha256(A2E_MP4.read_bytes()).hexdigest()
    if h != A2E_SHA:
        sys.exit(f"!!! reference digest MISMATCH {h[:12]} != {A2E_SHA[:12]} — HALT")
    print(f"[clk1-vs-a2e] reference verified from bytes: {h[:12]}… ({A2E_MP4.stat().st_size} B)")


def decode_range(path: Path, f0: int, n: int):
    """Yield n frames starting at f0 as uint8 HxWx3, streamed."""
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path),
         "-vf", f"select=between(n\\,{f0}\\,{f0 + n - 1})", "-vsync", "0",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    size = W * H * 3
    try:
        for _ in range(n):
            buf = proc.stdout.read(size)
            if len(buf) < size:
                return
            yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    finally:
        proc.stdout.close()
        proc.wait()


def load_render(dirpath: Path) -> list[Path]:
    return sorted(dirpath.glob("frame*.png"))


def codec_floor(pngs: list[Path], tmp: Path) -> tuple[float, float]:
    """Encode the rendered frames with the A2e settings, decode, diff vs source."""
    from PIL import Image
    mp4 = tmp / "floor.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
         "-pattern_type", "glob", "-i", str(pngs[0].parent / "frame*.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "12", "-preset", "slow",
         str(mp4)], check=True)
    tot, mx, n = 0.0, 0.0, 0
    for i, ref in enumerate(decode_range(mp4, 0, len(pngs))):
        src = np.asarray(Image.open(pngs[i]).convert("RGB"))
        d = np.abs(src.astype(np.int16) - ref.astype(np.int16))
        tot += float(d.mean())
        mx = max(mx, float(d.max()))
        n += 1
    mp4.unlink(missing_ok=True)
    return (tot / max(n, 1), mx)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", required=True, help="dir of frame*.png (preroll already pruned)")
    ap.add_argument("--segment", required=True, choices=["A-stationary", "B-undulating"])
    ap.add_argument("--shot", required=True, choices=["b-ring", "d-close"])
    ap.add_argument("--floor", action="store_true", help="also measure the H.264 floor")
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    from PIL import Image
    verify_reference()
    bounds = a2e_segment_bounds()
    f0, f1 = bounds[(args.segment, args.shot)]
    pngs = load_render(Path(args.render))
    n = min(len(pngs), f1 - f0)
    print(f"[clk1-vs-a2e] {args.label or args.render}")
    print(f"[clk1-vs-a2e] segment {args.segment}/{args.shot}: A2e frames {f0}..{f1 - 1} "
          f"({f1 - f0}), render has {len(pngs)} -> comparing {n}")

    rows = []
    for i, ref in enumerate(decode_range(A2E_MP4, f0, n)):
        src = np.asarray(Image.open(pngs[i]).convert("RGB")).astype(np.int16)
        d = np.abs(src - ref.astype(np.int16))
        rows.append((i, float(d.mean()), float(d.max()),
                     float((d >= 8).mean()), float((d >= 32).mean())))

    arr = np.array([[r[1], r[2], r[3], r[4]] for r in rows])
    print(f"[clk1-vs-a2e] frames compared: {len(rows)}")
    print(f"[clk1-vs-a2e] mean |delta| per channel : {arr[:, 0].mean():.4f}  "
          f"(per-frame min {arr[:, 0].min():.4f} / max {arr[:, 0].max():.4f})")
    print(f"[clk1-vs-a2e] max  |delta| any channel : {arr[:, 1].max():.0f}")
    print(f"[clk1-vs-a2e] channel-samples >= 8     : {100 * arr[:, 2].mean():.3f} %")
    print(f"[clk1-vs-a2e] channel-samples >= 32    : {100 * arr[:, 3].mean():.3f} %")
    worst = sorted(rows, key=lambda r: -r[1])[:8]
    print("[clk1-vs-a2e] worst frames (index within segment, mean |delta|): "
          + ", ".join(f"{w[0]}:{w[1]:.2f}" for w in worst))
    # the A2e jitter band, in this segment's own frame numbering
    band = [r for r in rows if 16 <= r[0] <= 25]
    rest = [r for r in rows if not (16 <= r[0] <= 25)]
    if band and rest:
        bm = sum(r[1] for r in band) / len(band)
        rm = sum(r[1] for r in rest) / len(rest)
        print(f"[clk1-vs-a2e] A2e jitter band (frames 16..25): mean {bm:.4f}  "
              f"vs rest of segment {rm:.4f}  ratio {bm / max(rm, 1e-9):.3f}")

    if args.floor:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fm, fx = codec_floor(pngs[:n], Path(td))
        print(f"[clk1-vs-a2e] H.264 CRF-12 FLOOR (same frames, encode+decode): "
              f"mean {fm:.4f}  max {fx:.0f}")
        print(f"[clk1-vs-a2e] SCENE DELTA ABOVE THE CODEC FLOOR: "
              f"{arr[:, 0].mean() - fm:+.4f} per channel")


if __name__ == "__main__":
    main()
