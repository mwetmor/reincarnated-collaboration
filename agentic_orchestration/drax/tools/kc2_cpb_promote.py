#!/usr/bin/env python3
"""kc2_cpb_promote.py — SB-1 Cell A2 (CP-B) item 6: the FG-9 promotion leg.

    python3 agentic_orchestration/drax/tools/kc2_cpb_promote.py

THE MECHANICAL LEGS RUN ON THE FACTORY SPINE'S OWN GATES (charter § 4 rider).
Not a re-implementation of ffprobe parsing and not a hand-rolled sha256: this
imports `factory.gates.media.ffprobe_verifies` and `factory.gates.digest.
sha256_matches` and calls them, so SB-1's media promotion is adjudicated by the
same code the spine adjudicates everything else with.

WHAT IS *NOT* ON THE SPINE, AND WHY — declared, not skipped. D-14 (drift-critic
re-verdict, 2026-08-11) says a spine PHASE that imports or renders Godot churns
`.godot/` (3,288 gitignored porcelain lines), which post-D-1 is a visible write,
therefore a breach, therefore an abort; the charter routes all Godot cells to
drax OUTSIDE the spine (§ 7) and D-14's closing sentence is "keep it that way."
So the RENDER runs classic and only the post-hoc artifact gates — which read a
finished MP4 in the meta-repo and change nothing — run on spine code. That is
the rider honoured where it serves and declined where the law says it must be.

FG-9's shape, obeyed: the render lands on a TEMPORARY name; ffprobe verifies it;
promotion to the deliverable name happens ONLY on green; the promoted bytes are
then re-hashed against the pre-promotion digest so the promotion itself is
proven not to have changed them.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

META = Path(__file__).resolve().parents[3]          # reincarnated-collaboration
sys.path.insert(0, str(META / "agentic_orchestration"))

from factory.gates.base import RunContext                      # noqa: E402
from factory.gates.digest import sha256_matches, sha256_of     # noqa: E402
from factory.gates.media import ffprobe_verifies               # noqa: E402

CAPTURES = META / "agentic_orchestration/galadriel/captures"
OUT_DIR = CAPTURES / "2026-08-12-sb1-cpb"
TMP = Path("/tmp/kc2_cpb")
TEMP_RENDER = TMP / "tmp-cpb-motion-watch.mp4"
DELIVERABLE = OUT_DIR / "cpb-motion-watch.mp4"
CEILING_KB = 10 * 1024 * 1024

FRAMING = (
    "This is run E-s09-cp150 MOVING, and every motion in it is a measurement. "
    "344 bodies walk the 1,003 path knots the sim emitted, each entering on its own "
    "tick — the wave-167 ambush drips in over 306 ticks, 24.98 seconds, because that "
    "is what the wire says and a batched spawn would have been tidier and false. "
    "Bodies that stop are standing at knots the sim put two of in one place. The "
    "player never moves: he is pinned at the origin the whole run with the channel "
    "never once off, so his 'sweep' is a spin in place inside a 3.000 m field that is "
    "the wire's own radius. Nothing here strikes, dies or counts — combat is the next "
    "act. When a body vanishes, that is its path ending, not a death being shown."
)


def floor_check(stage: str) -> int:
    kb = int(subprocess.run(["du", "-sk", str(CAPTURES)], capture_output=True,
                            text=True, check=True).stdout.split()[0])
    print(f"[promote] PL-5 {stage}: captures/ = {kb/1048576:.2f} G of 10 G "
          f"({100.0*kb/CEILING_KB:.1f} %)")
    if kb >= CEILING_KB:
        print("[promote] PL-5 HOUSEKEEPING HALT — ceiling breached. Nothing promoted.")
        sys.exit(4)
    return kb


def main() -> int:
    before_kb = floor_check("before")
    if not TEMP_RENDER.exists():
        print(f"[promote] HALT — no temp render at {TEMP_RENDER}. Run "
              f"scripts/run_kc2_cpb_clip.sh first.")
        return 8

    sidecars = {}
    for p in sorted(OUT_DIR.glob("shot-*.json")):
        sidecars[p.stem.replace("shot-", "")] = json.loads(p.read_text())
    if not sidecars:
        print("[promote] HALT — no shot sidecars; the render did not declare its own poses.")
        return 9

    expect_s = sum(float(s["trace_seconds"]) for s in sidecars.values())
    run = RunContext(run_id="sb1-a2-cpb", root=META, session_dir=TMP)

    # ---- FG-9 half 1: VERIFY the temp render, on the spine's own gate --------
    rep = ffprobe_verifies(
        None, run,
        path=str(TEMP_RENDER),
        min_duration_s=expect_s - 1.0,
        max_duration_s=expect_s + 1.0,
        expect_streams=["video"],
        min_width=1920, min_height=1080,
    )
    print("[promote] spine gate ->", rep.one_line())
    if not rep.is_green:
        print("[promote] HALT — a partial or wrong render must never land on the "
              "deliverable path (FG-9). Nothing promoted.")
        return 10

    # ---- the digest of the VERIFIED bytes, taken before the move ------------
    verified_sha = sha256_of(TEMP_RENDER)
    size = TEMP_RENDER.stat().st_size
    print(f"[promote] verified bytes: {size:,} B  sha256 {verified_sha}")

    # ---- promotion -----------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMP_RENDER, DELIVERABLE)

    # ---- FG-9 half 2: the promoted file is the SAME file --------------------
    rep2 = sha256_matches(None, run, path=str(DELIVERABLE), expected=verified_sha,
                          size_bytes=size)
    print("[promote] spine gate ->", rep2.one_line())
    if not rep2.is_green:
        DELIVERABLE.unlink(missing_ok=True)
        print("[promote] HALT — the promoted bytes differ from the verified bytes. "
              "Deliverable removed.")
        return 11

    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
         str(DELIVERABLE)], capture_output=True, text=True, check=True).stdout)
    vstream = next(s for s in probe["streams"] if s["codec_type"] == "video")

    manifest = {
        "cell": "SB-1 Cell A2 (CP-B) item 6 — the motion clip",
        "charter": ("agentic_orchestration/gandalf/notes/2026-08-10-sb1-kc2-scene-run-charter.md "
                    "§ 6 (CP-B: paths, dwells, straight walks, spawn drip, player sweep)"),
        "date": date.today().isoformat(),
        "artifact_class": ("E — owner-eye. UNTRACKED, never committed. Keep until viewed + veto "
                           "window closed, then demote to class D (PL-5)."),
        "framing_sentence": FRAMING,
        "deliverable": {
            "file": DELIVERABLE.name,
            "sha256": verified_sha,
            "bytes": size,
            "duration_s": float(probe["format"]["duration"]),
            "expected_trace_s": expect_s,
            "codec": vstream["codec_name"],
            "resolution": f'{vstream["width"]}x{vstream["height"]}',
            "fps": vstream.get("r_frame_rate"),
            "time_base": "1x REAL TIME — the trace clock is inviolate (GL-18)",
        },
        "fg9": {
            "temp_name": str(TEMP_RENDER),
            "verify_gate": rep.one_line(),
            "promote_gate": rep2.one_line(),
            "adjudicated_by": ("factory.gates.media.ffprobe_verifies + "
                               "factory.gates.digest.sha256_matches — the spine's own code "
                               "(charter § 4 rider)"),
            "render_lane": ("CLASSIC, declared: D-14 keeps Godot phases off the spine "
                            "(.godot/ churn is a post-D-1 breach); only the post-hoc artifact "
                            "gates run on spine code."),
        },
        "fg12_prune": ("PNG intermediates written to /tmp/kc2_cpb/frames-<shot> (OUTSIDE "
                       "captures/) and deleted by scripts/run_kc2_cpb_clip.sh immediately after "
                       "each encode; per-shot MP4s remain in /tmp only. Regenerate with "
                       "`bash scripts/run_kc2_cpb_clip.sh` at the pinned baton + godot HEAD."),
        "pl5": {"captures_before_kb": before_kb, "ceiling_kb": CEILING_KB},
        "shots": sidecars,
    }
    (OUT_DIR / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(f"[promote] wrote {OUT_DIR/'MANIFEST.json'}")
    after_kb = floor_check("after")
    manifest["pl5"]["captures_after_kb"] = after_kb
    (OUT_DIR / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(f"[promote] PROMOTED -> {DELIVERABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
