#!/usr/bin/env python3
"""kc2_cpb_promote.py — SB-1 Cell A2e item 3/4: the FG-9 promotion leg.

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
finished MP4 in the meta-repo and change nothing — run on spine code.

FG-9's shape, obeyed: the render lands on a TEMPORARY name; ffprobe verifies it;
promotion to the deliverable name happens ONLY on green; the promoted bytes are
then re-hashed against the pre-promotion digest so the promotion itself is
proven not to have changed them.
"""

from __future__ import annotations

import json
import math
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

GODOT = Path("/Users/admin/Games/reincarnated-godot")
CAPTURES = META / "agentic_orchestration/galadriel/captures"
OUT_DIR = CAPTURES / "2026-08-13-sb1-a2f-density"
# ⚑ THE A2e CAPTURE IS READ, NOT RETYPED. The charter asks for a vs-A2e DELTA
#   block so the two clips read as ONE experiment; every figure that CAN come off
#   the previous manifest does, and the handful that cannot (A2e's realized
#   density numbers, which predate the manifest carrying them) are quoted from
#   the A2e landing note and LABELLED as quotations rather than measurements.
PREV_DIR = CAPTURES / "2026-08-13-sb1-a2e-cpbprime"
TMP = Path("/tmp/kc2_cpb")
TEMP_RENDER = TMP / "tmp-cpbprime-cadence-ab.mp4"
DELIVERABLE = OUT_DIR / "a2f-density-cadence-ab.mp4"
SMOKE = GODOT / "tmp/kc2/kc2_motion_smoke.json"
CEILING_KB = 10 * 1024 * 1024
BLACK_S = 0.60          # the held-black seam, must match run_kc2_cpb_clip.sh

# A2e's MEASURED cadence figures, quoted from `drax/notes/2026-08-12-sb1-a2e-
# render-landing.md` § 2.4. These are HISTORY — the article Matt ratified — and
# they are here so the delta can be read without opening a second file. They are
# never compared against, never asserted on, and never used to derive anything.
A2E_MEASURED = {
    "cut_per_rev": 11,
    "stationary_mean_per_rev": 11.003,
    "stationary_thick_thin": 1.20,
    "undulating_mean_per_rev": 8.333,
    "undulating_sd": 1.3357,
    "undulating_thick_thin": 2.40,
    "undulating_range": [5, 12],
    "worst_dark_run_s": 0.0333,
    "analytic_dark_bound_s": 0.0327,
    "epochs_b_ring": 29,
    "epochs_d_close": 15,
    "max_alive": 6,
    "source": ("QUOTED from the A2e landing note § 2.4 and § 4.1, not measured here. "
               "The A2e manifest predates the density block, so these could not be read "
               "off it the way the artifact figures below are."),
}

# ⚑ THE ORDER IS THE COMPARISON. Segment A is the STATIONARY cadence — and after
#   R-CPB-15 that is no longer "the article Matt ratified", because "across the
#   board" raised BOTH cadences. A is here to isolate the undulation at the new
#   rate; the ratified 11/rev density lives in the A2e clip, permanently.
PART_ORDER = [
    ("A-stationary", "b-ring"),
    ("A-stationary", "d-close"),
    ("SEAM", "black"),
    ("B-undulating", "b-ring"),
    ("B-undulating", "d-close"),
]

FRAMING = (
    "ONE clip, TWO cadences, same 16.3 s of trace twice. Segment A is the cut pattern "
    "you called perfect. Segment B is that pattern with your one adjustment folded in: "
    "the sequence of cuts now RUNS, ENDS, and BEGINS AGAIN after a seeded gap, so it "
    "restarts somewhere else on the circle and the ring thickens and thins instead of "
    "holding one constant texture. Same tick window, same camera, same seed, same "
    "binary — ONE boolean differs, and the dip to black is the only thing between them. "
    "The hammer is at WEAPON_SCALE 1.95 in BOTH halves: your 1.65 pick was priced "
    "against a grip defect you yourself caught, and re-pricing it is a one-line revert. "
    "Nothing here strikes, dies or counts — combat is the next act. When a body "
    "vanishes, that is its path ending, not a death being shown."
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


def probe(path: Path) -> dict:
    return json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
         str(path)], capture_output=True, text=True, check=True).stdout)


def part_duration(seg: str, shot: str) -> float:
    if seg == "SEAM":
        return BLACK_S
    return float(probe(TMP / f"tmp-{seg}-{shot}.mp4")["format"]["duration"])


def parallax(cam: dict, ring_y: float, ring_r: float) -> dict:
    """⚑ THE ELEVATION-PARALLAX FACTOR, DECLARED RATHER THAN LEFT TO THE EYE.

    The cut ring is a HORIZONTAL circle at `ring_y`. Seen from an elevated eye it
    projects as an ELLIPSE whose minor/major ratio is sin(depression angle) — so a
    reader of this clip who measures the ring's on-screen height against its width
    is measuring the camera, not the geometry. A2c already caught the consequence
    once (a ring 1.126 m up crossed the boots from a high eye); the number belongs
    in the manifest so nobody has to rediscover it.
    """
    ex, ey, ez = cam["eye"]
    lx, ly, lz = cam["look_at"]
    dy = ey - ring_y
    dh = math.hypot(ex - lx, ez - lz)
    dep = math.degrees(math.atan2(dy, dh)) if dh > 0 else 90.0
    return {
        "eye_height_above_ring_plane_m": round(dy, 6),
        "horizontal_run_m": round(dh, 6),
        "depression_angle_deg": round(dep, 4),
        "ring_ellipse_minor_over_major": round(math.sin(math.radians(dep)), 6),
        "ring_radius_m": ring_r,
        "ring_height_m": ring_y,
        "basis": ("a horizontal circle seen from an elevated eye projects as an ellipse "
                  "with minor/major = sin(depression). The ring is NOT squashed; the "
                  "camera is above it. Measured off this shot's own declared pose."),
    }


def main() -> int:
    before_kb = floor_check("before")
    if not TEMP_RENDER.exists():
        print(f"[promote] HALT — no temp render at {TEMP_RENDER}. Run "
              f"scripts/run_kc2_cpb_clip.sh first.")
        return 8

    sidecars = {}
    for p in sorted(OUT_DIR.glob("shot-*.json")):
        sidecars[p.stem.replace("shot-", "")] = json.loads(p.read_text())
    if len(sidecars) != 4:
        print(f"[promote] HALT — expected 4 shot sidecars (2 segments x 2 shots), "
              f"found {len(sidecars)}: {sorted(sidecars)}")
        return 9

    # ---- the segment map: where each half starts, in ticks AND in seconds ----
    timeline = []
    t = 0.0
    for seg, shot in PART_ORDER:
        d = part_duration(seg, shot)
        row = {
            "segment": seg, "shot": shot,
            "starts_at_s": round(t, 4), "ends_at_s": round(t + d, 4),
            "duration_s": round(d, 4),
        }
        if seg != "SEAM":
            sc = sidecars[f"{seg}-{shot}"]
            row["tick_from"] = sc["tick_from"]
            row["tick_to"] = sc["tick_to"]
            row["cadence"] = "STATIONARY (A2d)" if not sc["undulate"] else "UNDULATING (epochs)"
            row["epochs_in_window"] = sc["epoch_count_in_window"]
        else:
            row["what"] = ("DIP TO BLACK — the segment boundary. Geometry-free and "
                           "WORDLESS (R-A1-1): applied at the encode, never by a node. "
                           "A hard cut separates the two SHOTS inside a segment; this "
                           "dip separates the two CADENCES.")
        timeline.append(row)
        t += d
    expect_s = t

    run = RunContext(run_id="sb1-a2e-cpbprime", root=META, session_dir=TMP)

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

    pr = probe(DELIVERABLE)
    vstream = next(s for s in pr["streams"] if s["codec_type"] == "video")

    # ---- the measured block at 1.95, read off the smoke's own output ---------
    smoke = json.loads(SMOKE.read_text())
    pl = smoke["driver_report"]["player"]
    pose = pl["pose"]
    occ = pose["occlusion"]
    etch = pl["channel_fx"]["etch"]
    measured = {
        "weapon_scale": sidecars["A-stationary-d-close"]["weapon_scale"],
        "grip_frac": sidecars["A-stationary-d-close"]["grip_frac"],
        "grip_seat_m": sidecars["A-stationary-d-close"]["grip_seat_m"],
        "hammer_tip_sweep_m": pl["weapon_sweep"]["mean_m"],
        # ⚑ NAMING TRAP, DECLARED: the player report's `margin_to_kill_ring_m` is
        #   the margin to KILL_RING_M = 2.400, which is the STANDING RANK (where
        #   dwellers stop to attack) and NOT the kill bound. R-CPB-5c re-based the
        #   kill reference to the 3.000 m EoR channel disc. Both computed here from
        #   the sweep so neither can inherit the other's name.
        "margin_to_2400_standing_rank_m": round(2.400 - pl["weapon_sweep"]["mean_m"], 9),
        "margin_to_3000_kill_bound_m": round(3.000 - pl["weapon_sweep"]["mean_m"], 9),
        "cut_ring_radius_m": etch["radius_m"],
        "cut_ring_height_m": etch["height_m"],
        "cut_ring_half_extent_m": etch["contact_band"]["half_extent_m"],
        "sole_pitch_max_deg": pose["stance"]["sole"]["sole_pitch_max_deg"],
        "sole_gap_max_m": pose["stance"]["sole"]["sole_gap_max_m"],
        "retired_bone_line_tilt_deg": pose["stance"]["bone_sole_tilt_max_deg"],
        "elbow_apex_out_min_m": pose["elbows"]["apex_out_min_m"],
        "elbow_flexion_deg": [pose["elbows"]["flexion_min_deg"],
                              pose["elbows"]["flexion_max_deg"]],
        "outward_faces_buried": occ["hand_outward_faces_buried"],
        "deepest_burial_m": occ["deepest_burial_m"],
        "contact_gap_worst_hand_m": occ["contact_gap_m"],
        "contact_gap_best_hand_m": occ["contact_gap_best_hand_m"],
        "retired_envelope_clearance_m": occ["envelope_clearance_min_m"],
        "arm_vs_arm_clearance_m": occ["arm_gap_m"],
        "knee_apex_fwd_min_m": pose["stance"]["knee_apex_fwd_min_m"],
        "hip_drop_m": pose["stance"]["hip_drop_m"],
        "grip_residual_max_m": pose["grip_residual_max_m"],
        "hand_gap_measured_m": pose["hand_gap_measured_m"],
        "basis": ("every number read off `tmp/kc2/kc2_motion_smoke.json` at the shipped "
                  "constants — the same run that returns the 67-check verdict, not a "
                  "second measurement taken for the manifest."),
    }

    dclose = sidecars["B-undulating-d-close"]
    manifest = {
        "cell": "SB-1 Cell A2e — the CP-B' CADENCE COMPARISON clip",
        "ledger_rows": "R-CPB-12 (cut pattern) · R-CPB-13 (palette) · R-CPB-14 (undulation + scale) · A2e-0",
        "date": date.today().isoformat(),
        "artifact_class": ("E — owner-eye. UNTRACKED, never committed. Keep until viewed + veto "
                           "window closed, then demote to class D (PL-5)."),
        "framing_sentence": FRAMING,
        "the_question_this_answers": (
            "Matt ratified the cut pattern with ONE adjustment: 'The sequence should begin "
            "again, linearly (horizontally) at rather random intervals so that the circle of "
            "laser-cuts/claws/sparks seems to undulate/morph naturally.' This clip shows the "
            "before and the after of exactly that, and nothing else changes between them."),
        "deliverable": {
            "file": DELIVERABLE.name,
            "sha256": verified_sha,
            "bytes": size,
            "duration_s": float(pr["format"]["duration"]),
            "expected_s": round(expect_s, 4),
            "codec": vstream["codec_name"],
            "resolution": f'{vstream["width"]}x{vstream["height"]}',
            "fps": vstream.get("r_frame_rate"),
            "frames": vstream.get("nb_frames"),
            "time_base": "1x REAL TIME — the trace clock is inviolate (GL-18)",
        },
        "timeline": timeline,
        "cadence_A": sidecars["A-stationary-d-close"]["cadence"],
        "cadence_B": dclose["cadence"],
        "palette": dclose["palette"],
        "epoch_schedule_realized_segment_B": {
            "b-ring": sidecars["B-undulating-b-ring"]["epoch_schedule_realized"],
            "d-close": dclose["epoch_schedule_realized"],
            "basis": ("computed from CUT_SEED alone for these exact tick windows, so the "
                      "manifest can be CHECKED against the frames rather than believed: "
                      "each row is a sequence's start tick, its length in births, the gap "
                      "that follows it, and the ANGULAR bearing at which it begins again."),
        },
        "measured_at_1_95": measured,
        "camera": {
            seg_shot: {"eye": sc["camera"]["eye"], "look_at": sc["camera"]["look_at"],
                       "fov_deg": sc["camera"]["fov_deg"],
                       "gate": sc["camera_gate"]["ok"]}
            for seg_shot, sc in sorted(sidecars.items())
        },
        "camera_identical_across_segments": (
            sidecars["A-stationary-b-ring"]["camera"] == sidecars["B-undulating-b-ring"]["camera"]
            and sidecars["A-stationary-d-close"]["camera"] == sidecars["B-undulating-d-close"]["camera"]),
        "elevation_parallax": {
            "b-ring": parallax(sidecars["B-undulating-b-ring"]["camera"],
                               etch["height_m"], etch["radius_m"]),
            "d-close": parallax(dclose["camera"], etch["height_m"], etch["radius_m"]),
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
        "fg10_determinism": (TMP / "fg10-probe.txt").read_text().strip()
        if (TMP / "fg10-probe.txt").exists() else
        "see the render log: d-close undulating, 45 frames, rendered TWICE and digest-compared "
        "frame by frame before the real render was trusted.",
        "fg12_prune": (TMP / "fg12-prune-receipts.txt").read_text().strip()
        if (TMP / "fg12-prune-receipts.txt").exists() else "receipts missing",
        "r_a1_1": ("ZERO text nodes anywhere in the scene — the motion smoke walks the whole "
                   "tree with the player, pose, cuts, smoke and bursts in it and counts 0 "
                   "text/canvas nodes. The dip-to-black seam is an ENCODE filter, so it cannot "
                   "introduce one either. Every word about this clip is in this file."),
        "gl15": ("one ongoing-damage read: no damage numbers, no per-cut UI, nothing flashes, "
                 "ticks or counts. The whirlwind's cuts are ONE event."),
        "pl5": {"captures_before_kb": before_kb, "ceiling_kb": CEILING_KB},
        "shots": sidecars,
    }
    (OUT_DIR / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    after_kb = floor_check("after")
    manifest["pl5"]["captures_after_kb"] = after_kb
    (OUT_DIR / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    man_sha = sha256_of(OUT_DIR / "MANIFEST.json")
    print(f"[promote] wrote {OUT_DIR/'MANIFEST.json'}  sha256 {man_sha}")
    print(f"[promote] PROMOTED -> {DELIVERABLE}")
    print(f"[promote] duration {float(pr['format']['duration']):.2f} s "
          f"(expected {expect_s:.2f} s), {vstream.get('nb_frames')} frames")
    for row in timeline:
        print("[promote]   %-14s %-8s %7.2f -> %7.2f s  %s" % (
            row["segment"], row["shot"], row["starts_at_s"], row["ends_at_s"],
            row.get("cadence", "dip to black")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
