#!/usr/bin/env python3
"""kc2_cpb_promote.py — SB-1 the FG-9 promotion leg. Cell A2g-r (the look distance).

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

⚑ THE CLAIM LEDGER IS THE DESIGN PRINCIPLE, NOT A PROMISE IN A COMMENT. A2f's
  landing filed surface 8 ("THE PROMOTE TOOL IS WIRED FOR A2f AND HAS NEVER BEEN
  RUN"); A2g ran it for the first time. The rider it was rewritten around stands:
  A MANIFEST THAT ASSERTS WHAT WAS NOT MEASURED IS A DEFECT. Every figure below
  is (a) read out of a file something else wrote — the sidecar, the smoke,
  ffprobe, ffmpeg's signalstats — or (b) recomputed here from those and CHECKED
  against them. `verify()` collects a verdict per claim, prints them, folds them
  into the manifest, and HALTS BEFORE PROMOTION if any one of them is false.

⚑ AND AT A2g-r THE LEDGER'S OWN DISTANCE ROW HAD TO BE REWRITTEN, WHICH IS THE
  POINT OF HAVING ONE. A2g's row read "the canon distance is the wr1 law
  recomputed, not a number that was typed" and it PASSED — it recomputed
  34.0 * (86.915 / 17.5) and matched the sidecar to 1e-6. R-CPB-17 struck the law
  that row was checking. A ledger row is a claim about what SHOULD be true, so
  when the ruling moves, the row moves with it or it certifies the old world
  perfectly. The distance row is now three rows: the boom is the rig's read
  (checked against 510/7), the pose contains NO room dimension (checked by
  recomputing the eye from station + angles + boom alone), and the arena's
  rectangle reaches the manifest as a REPORT rather than as an input.

⚑ THE ANCESTRY IS NOW FOUR DELTAS, AND EACH CARRIES WHOSE WORD MOVED IT: the rate
  is Matt's lever (R-CPB-15), the clock is the run's own fix (CLK-1), the lens
  ANGLES are Matt's canon (R-CPB-16), and the BOOM is Matt's ruling (R-CPB-17).
  A fifth block compares against A2g — the immediate predecessor — where the
  declared delta count is exactly ONE.
"""

from __future__ import annotations

import json
import math
import re
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
OUT_DIR = CAPTURES / "2026-08-13-sb1-a2gr-lookdist"
# ⚑ THE A2e CAPTURE IS READ, NOT RETYPED. The charter asks for an ANCESTRY block
#   against the artifact Matt actually watched, so every figure that CAN come off
#   that manifest does, and the handful that cannot are quoted and LABELLED as
#   quotations rather than dressed up as measurements.
PREV_DIR = CAPTURES / "2026-08-13-sb1-a2e-cpbprime"
PREV_MP4 = PREV_DIR / "cpbprime-cadence-ab.mp4"
# ⚑ AND THE IMMEDIATE PREDECESSOR IS READ TOO. A2g is the clip this one differs
#   from by exactly ONE authored change, so its sidecars are the instrument that
#   proves the boom was the only thing that moved: every tick and layout field
#   must match, field for field, while every camera field must differ.
A2G_DIR = CAPTURES / "2026-08-13-sb1-a2g-canon"
TMP = Path("/tmp/kc2_cpb")
DELIV_STEM = "a2gr-lookdist-cadence-ab"
# ⚑ CELL-SPECIFIC, AND THAT IS A DEFECT FIX. Until A2g every cell concatenated
#   into `tmp-cpbprime-cadence-ab.mp4` and this tool read that path. A2e's file
#   was still sitting there when A2g opened: a quietly-failed render would have
#   had this tool verify, hash and promote A2e's bytes under A2g's name with
#   every gate green. FG-9 protects the deliverable path, not a shared temp path.
# ⚑ AND AT A2g-r THE SAME HOLE WAS FOUND ONE LEVEL DOWN: the PARTS this tool reads
#   in `part_facts()` were `$TMP/tmp-$SEG-$SHOT.mp4`, shared across cells, with
#   A2g's two parts sitting in exactly those names and ffmpeg's exit status
#   unchecked in the harness. A quietly-failed encode would have had this tool
#   build its timeline — durations, frame counts, the concat-equals-its-parts
#   claim — out of ANOTHER CLIP'S parts. Parts are now cell-scoped. (NOTE-80.)
TEMP_RENDER = TMP / f"tmp-{DELIV_STEM}.mp4"
PARTS_DIR = TMP / f"parts-{DELIV_STEM}"
DELIVERABLE = OUT_DIR / f"{DELIV_STEM}.mp4"
SMOKE = GODOT / "tmp/kc2/kc2_motion_smoke.json"
CEILING_KB = 10 * 1024 * 1024
BLACK_S = 0.60          # the held-black seam, must match run_kc2_cpb_clip.sh
FADE_S = 0.50           # the dip at each side of it, likewise

# A2e's MEASURED cadence figures, quoted from `drax/notes/2026-08-12-sb1-a2e-
# render-landing.md` § 2.4. These are HISTORY — the article Matt watched — and
# they are the "before" column of the ancestry block. They are never compared
# against as if they were measurements taken here.
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
               "off it the way the artifact figures are."),
}

# ⚑ ONE SHOT, TWO SEGMENTS. R-CPB-16(d) demoted b-ring and d-close to diagnostic
#   instruments, so the deliverable is A / dip / B over ONE frame and ONE window.
PART_ORDER = [
    ("A-stationary", "canon"),
    ("SEAM", "black"),
    ("B-undulating", "canon"),
]

# ⚑ THE FIELDS THAT MUST NOT HAVE MOVED, NAMED IN ADVANCE. "One authored change"
#   is only a checkable claim if the things it does not change are enumerated
#   before the comparison rather than after it. Every one of these is a tick,
#   layout, article or clock property; not one of them is a camera property. The
#   comparison is `==` on the raw sidecar values, including the whole realized
#   epoch schedule — 36 rows of start tick, length, gap and re-anchor bearing,
#   which is the strongest single invariant in the file because it is a function
#   of CUT_SEED and the tick window and of nothing a camera can touch.
A2G_INVARIANT_FIELDS = [
    "tick_from", "tick_to", "trace_seconds", "tick_period_s", "time_base",
    "cut_per_rev", "density_target_cuts_per_rev", "undulate", "cadence",
    "epoch_count_in_window", "epoch_schedule_realized",
    "weapon_scale", "grip_frac", "grip_seat_m", "palette",
    "preroll_frames_tick_frozen", "tick0_is_shot_default",
    "fps", "width", "height", "frames_expected",
    "baton_sha256", "driver", "shot", "segment", "clk1_diagnostics", "fg10_layer",
]

FRAMING = (
    "ONE clip, TWO cadences, the same 10.6 s of trace twice — through YOUR camera, at "
    "YOUR distance. You said the camera should have nothing to do with room size, so it "
    "no longer does: the boom is FIXED at 72.857 m, which is the werewolf shot's own "
    "realized distance — the frame you ratified — and it will be that distance in every "
    "room, forever, until you say otherwise. The man is back at ~13 % of frame height, "
    "the Grim Dawn register. FOUR things have moved since the clip you watched and only "
    "one of them was ever mine: the CUT RATE went 11 -> 17 because you pulled that lever; "
    "the CLOCK was fixed so the same tick renders the same pixels twice (it costs a "
    "different draw of the smoke and sparks, and nothing else); the LENS ANGLES are your "
    "canon; and the BOOM is your ruling. Against the last clip I sent you — the one where "
    "the man was sixty pixels tall — there is exactly ONE change, and this is it. Segment "
    "A is the stationary cadence at 17, segment B is the undulating one: one boolean "
    "between them, same window, same seed, same binary, one dip to black. The hammer is "
    "still at WEAPON_SCALE 1.95. Nothing here strikes, dies or counts — combat is the next "
    "act. When a body vanishes, that is its path ending, not a death being shown. ⚑ THE "
    "ARENA NOW RUNS OFF ALL FOUR EDGES OF THE FRAME AND THAT IS THE POINT, NOT THE PRICE: "
    "the frame holds ~55 m of a 86.9 m room, exactly the way an ARPG crops a room around "
    "its hero. This is not an arena overview and should not be read as one."
)


# ---------------------------------------------------------------------------
# ⚑ THE CLAIM LEDGER. Every assertion this manifest makes gets a row: what is
#   claimed, whether it was checked, and against what. A row that comes back
#   false HALTS before promotion — the charter's rider, implemented rather than
#   promised.
# ---------------------------------------------------------------------------
CLAIMS: list[dict] = []


def verify(claim: str, ok: bool, detail: str) -> bool:
    CLAIMS.append({"claim": claim, "verdict": "PASS" if ok else "FAIL", "checked_against": detail})
    print(f"[promote] {'OK  ' if ok else 'FAIL'} {claim} — {detail}")
    return ok


def close(a: float, b: float, tol: float) -> bool:
    return abs(float(a) - float(b)) <= tol


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


def part_facts(seg: str, shot: str) -> tuple[float, int]:
    """Duration AND frame count of a part, both off ffprobe. The frame count is
    read rather than derived because Godot's movie writer emits one frame more
    than the scene reports driving (the iteration on which it quits is still
    written), and a manifest that computed the total from the scene's number
    would be off by one per shot and would not know it."""
    if seg == "SEAM":
        return BLACK_S, int(round(BLACK_S * 30))
    pr = probe(PARTS_DIR / f"tmp-{seg}-{shot}.mp4")
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    return float(pr["format"]["duration"]), int(v.get("nb_frames", 0))


def luma_series(path: Path, start_s: float, dur_s: float) -> list[float]:
    """⚑ THE SEAM'S LUMA, MEASURED OFF THE PROMOTED FILE.

    The dip is applied at the ENCODE, so the only place its depth exists is in
    the encoded bytes. `signalstats` reports YAVG per frame; the seam claim
    ("dips to black") is then a number rather than a description of an intent.
    """
    # ⚑ NO SEEKING. `-ss` on an H.264 file lands relative to a keyframe, and a
    #   seam measurement that quietly sampled the wrong 0.5 s would report a
    #   perfect dip from the middle of a fade or a fade from the middle of the
    #   dip. `select` between two timestamps is exact; the file is ~30 s, so
    #   decoding all of it costs nothing worth trading accuracy for.
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path),
         "-vf", f"select='between(t,{start_s:.4f},{start_s + dur_s:.4f})',"
                f"signalstats,metadata=print:file=-",
         "-vsync", "0", "-f", "null", "-"],
        capture_output=True, text=True, check=True).stdout
    return [float(m) for m in re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)", out)]


def parallax_analytic(cam: dict, ring_y: float, ring_r: float) -> dict:
    """The elevation-parallax PREDICTION, kept beside the measurement, never in
    place of it. A horizontal circle seen from an elevated eye projects as an
    ellipse with minor/major = sin(depression) — under an ORTHOGRAPHIC camera.
    The sidecar carries the perspective camera's actual projection; this is the
    number that would have been reported if nobody had measured."""
    ex, ey, ez = cam["eye"]
    lx, ly, lz = cam["look_at"]
    dy = ey - ring_y
    dh = math.hypot(ex - lx, ez - lz)
    dep = math.degrees(math.atan2(dy, dh)) if dh > 0 else 90.0
    return {
        "eye_height_above_ring_plane_m": round(dy, 6),
        "horizontal_run_m": round(dh, 6),
        "depression_angle_deg": round(dep, 4),
        "predicted_minor_over_major": round(math.sin(math.radians(dep)), 6),
        "ring_radius_m": ring_r, "ring_height_m": ring_y,
        "basis": ("PREDICTION from the pose, orthographic. The MEASURED value is in "
                  "optics_measured.cut_ring_ellipse, taken by projecting 720 points of the "
                  "circle through the camera that rendered."),
    }


def smoke_density(smoke_text: str) -> dict:
    """⚑ THE REALIZED MEANS ARE PARSED OUT OF THE SMOKE'S OWN EVIDENCE STRING AND
    THE STRING IS CARRIED WITH THEM. The smoke reports density in prose; a
    regex over prose is exactly the sort of thing that silently returns the
    wrong number, so the sentence it was read from ships beside the numbers and
    a failed parse HALTS rather than defaults."""
    ev = ""
    canon_ev = ""
    for c in json.loads(smoke_text)["checks"]:
        if "RESTORED mean" in c["check"]:
            ev = c["evidence"]
        if "RESTARTS INSIDE THE CLIP" in c["check"]:
            canon_ev = c["evidence"]
    # ⚑ `[\d.]+` IS THE WRONG CHARACTER CLASS FOR A NUMBER AT THE END OF A
    #   SENTENCE, and this is not a hypothetical: the first run of this parser
    #   read "THICK/THIN = 1.12." and returned the string `1.12.`. A decimal is
    #   `\d+(\.\d+)?`, not "digits and dots"; the full stop belongs to the prose.
    NUM = r"(\d+(?:\.\d+)?)"
    pat = (r"{0}: (\d+) births, " + NUM + r" per window, sd " + NUM
           + r", range (\d+)\.\.(\d+) — THICK/THIN = " + NUM)
    st = re.search(pat.format("STATIONARY"), ev)
    un = re.search(pat.format("UNDULATING"), ev)
    rate = re.search(r"at the shipped rate of (\d+) births/rev", ev)
    canon = re.search(r"canon \[(\d+)\.\.(\d+)\] = " + NUM + r" rev: (\d+) sequence restarts, "
                      r"thinnest frame (\d+) cuts, longest dark run " + NUM + r" s", canon_ev)
    if not (st and un and rate and canon):
        print("[promote] HALT — could not parse the smoke's density evidence. A manifest "
              "does not get to guess the number it is about to assert.")
        sys.exit(14)
    return {
        "shipped_rate_per_rev": int(rate.group(1)),
        "stationary": {"births": int(st.group(1)), "mean_per_rev": float(st.group(2)),
                       "sd": float(st.group(3)),
                       "range": [int(st.group(4)), int(st.group(5))],
                       "thick_over_thin": float(st.group(6))},
        "undulating": {"births": int(un.group(1)), "mean_per_rev": float(un.group(2)),
                       "sd": float(un.group(3)),
                       "range": [int(un.group(4)), int(un.group(5))],
                       "thick_over_thin": float(un.group(6))},
        "canon_window": {"tick_from": int(canon.group(1)), "tick_to": int(canon.group(2)),
                         "revolutions": float(canon.group(3)),
                         "sequence_restarts": int(canon.group(4)),
                         "thinnest_frame_cuts": int(canon.group(5)),
                         "longest_dark_run_s": float(canon.group(6))},
        "source_sentence_density": ev,
        "source_sentence_canon_window": canon_ev,
        "basis": ("READ from `tmp/kc2/kc2_motion_smoke.json` — the 71-check run at the shipped "
                  "constants — by regex, with the sentence parsed carried above so the "
                  "extraction can be checked by eye rather than trusted."),
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
    if sorted(sidecars) != ["A-stationary-canon", "B-undulating-canon"]:
        print(f"[promote] HALT — expected exactly the two canon sidecars, found "
              f"{sorted(sidecars)}. A demoted shot's record must not reach this manifest.")
        return 9
    seg_a = sidecars["A-stationary-canon"]
    seg_b = sidecars["B-undulating-canon"]

    # ---- the segment map: where each half starts, in ticks AND in seconds ----
    timeline = []
    t = 0.0
    seam_at = 0.0
    frames_in_parts = 0
    for seg, shot in PART_ORDER:
        d, nf = part_facts(seg, shot)
        frames_in_parts += nf
        row = {"segment": seg, "shot": shot, "starts_at_s": round(t, 4),
               "ends_at_s": round(t + d, 4), "duration_s": round(d, 4), "frames": nf}
        if seg != "SEAM":
            sc = sidecars[f"{seg}-{shot}"]
            row["tick_from"] = sc["tick_from"]
            row["tick_to"] = sc["tick_to"]
            row["cadence"] = "STATIONARY (A2d's law at 17/rev)" if not sc["undulate"] \
                else "UNDULATING (epochs)"
            row["epochs_in_window"] = sc["epoch_count_in_window"]
        else:
            seam_at = t
            row["what"] = ("DIP TO BLACK — the segment boundary. Geometry-free and "
                           "WORDLESS (R-A1-1): applied at the encode, never by a node. "
                           "With one shot per segment there is no hard cut left inside a "
                           "segment; this dip is the only boundary in the clip.")
        timeline.append(row)
        t += d
    expect_s = t

    run = RunContext(run_id="sb1-a2gr-lookdist", root=META, session_dir=TMP)

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

    # ---- the measured blocks, assembled BEFORE promotion so the claim ledger
    #      can halt on a false one -------------------------------------------
    smoke = json.loads(SMOKE.read_text())
    pl = smoke["driver_report"]["player"]
    pose_m = pl["pose"]
    occ = pose_m["occlusion"]
    etch = pl["channel_fx"]["etch"]
    density = smoke_density(SMOKE.read_text())

    measured_1_95 = {
        "weapon_scale": seg_a["weapon_scale"],
        "grip_frac": seg_a["grip_frac"],
        "grip_seat_m": seg_a["grip_seat_m"],
        "hammer_tip_sweep_m": pl["weapon_sweep"]["mean_m"],
        # ⚑ NAMING TRAP, DECLARED: the player report's `margin_to_kill_ring_m` is
        #   the margin to KILL_RING_M = 2.400, which is the STANDING RANK and NOT
        #   the kill bound. R-CPB-5c re-based the kill reference to the 3.000 m
        #   EoR channel disc. Both computed here so neither inherits the other.
        "margin_to_2400_standing_rank_m": round(2.400 - pl["weapon_sweep"]["mean_m"], 9),
        "margin_to_3000_kill_bound_m": round(3.000 - pl["weapon_sweep"]["mean_m"], 9),
        "cut_ring_radius_m": etch["radius_m"],
        "cut_ring_height_m": etch["height_m"],
        "cut_ring_half_extent_m": etch["contact_band"]["half_extent_m"],
        "sole_pitch_max_deg": pose_m["stance"]["sole"]["sole_pitch_max_deg"],
        "contact_gap_worst_hand_m": occ["contact_gap_m"],
        "grip_residual_max_m": pose_m["grip_residual_max_m"],
        "basis": ("every number read off `tmp/kc2/kc2_motion_smoke.json` at the shipped "
                  "constants — the same run that returns the 71-check verdict, not a "
                  "second measurement taken for the manifest."),
    }

    # ---- the seam, measured off the promoted bytes ---------------------------
    #      the dip runs FADE out, BLACK held, FADE in; the held black is the
    #      middle, and that is where "dips to black" is either true or not.
    seam_luma = luma_series(TEMP_RENDER, seam_at + 0.05, BLACK_S - 0.15)
    pre_luma = luma_series(TEMP_RENDER, max(seam_at - FADE_S - 1.5, 0.0), 0.50)
    seam = {
        "held_black_starts_at_s": round(seam_at, 4),
        "held_black_duration_s": BLACK_S,
        "fade_each_side_s": FADE_S,
        "frames_sampled": len(seam_luma),
        "seam_luma_mean_Y": round(sum(seam_luma) / len(seam_luma), 4) if seam_luma else None,
        "seam_luma_max_Y": round(max(seam_luma), 4) if seam_luma else None,
        "picture_luma_mean_Y_before_the_dip": round(sum(pre_luma) / len(pre_luma), 4)
        if pre_luma else None,
        "basis": ("MEASURED with ffmpeg signalstats YAVG over the PROMOTED file. The dip is "
                  "an ENCODE filter, so the encoded bytes are the only place its depth "
                  "exists — 'dips to black' is a number here, not a description of intent."),
    }

    # ---- promotion -----------------------------------------------------------
    # (claims are checked first; the copy happens only after the ledger is clean)
    pr_tmp = probe(TEMP_RENDER)
    v_tmp = next(s for s in pr_tmp["streams"] if s["codec_type"] == "video")

    cam_a = seg_a["camera"]
    cam_b = seg_b["camera"]
    der = seg_b["canon_derivation"]
    opt = seg_b["optics_measured"]
    ell = opt["cut_ring_ellipse"]
    subj = opt["subject"]
    gl13 = opt["gl13_rectangle_projected"]

    # ⚑ A2g's OWN SIDECAR, READ FROM DISK — the one-delta claim is checked against
    #   the predecessor's recorded facts, never against this note's memory of them.
    #   GL-12: absent means ABSENT and the row fails, it does not quietly skip.
    a2g_sidecar_path = A2G_DIR / "shot-B-undulating-canon.json"
    a2g_b = json.loads(a2g_sidecar_path.read_text()) if a2g_sidecar_path.exists() else None

    # ---- THE CLAIM LEDGER ----------------------------------------------------
    ok = True
    ok &= verify("the deliverable is the two canon segments and a dip, nothing else",
                 sorted(sidecars) == ["A-stationary-canon", "B-undulating-canon"],
                 f"sidecars on the deliverable path: {sorted(sidecars)}")
    ok &= verify("both segments render the SAME camera (the A/B is one boolean)",
                 cam_a == cam_b,
                 f"eye {cam_a['eye']} look {cam_a['look_at']} fov {cam_a['fov_deg']}, identical")
    ok &= verify("both segments render the SAME tick window",
                 (seg_a["tick_from"], seg_a["tick_to"]) == (seg_b["tick_from"], seg_b["tick_to"]),
                 f"ticks {seg_a['tick_from']}..{seg_a['tick_to']} on both")
    ok &= verify("the segments differ in the cadence boolean and in nothing else named",
                 seg_a["undulate"] is False and seg_b["undulate"] is True
                 and seg_a["cut_per_rev"] == seg_b["cut_per_rev"]
                 and seg_a["weapon_scale"] == seg_b["weapon_scale"],
                 f"undulate {seg_a['undulate']}/{seg_b['undulate']}, rate "
                 f"{seg_a['cut_per_rev']} both, scale {seg_a['weapon_scale']} both")
    ok &= verify("the rate in the frames is R-CPB-15's 17, in the sidecars AND in the smoke",
                 seg_b["cut_per_rev"] == 17 == density["shipped_rate_per_rev"],
                 f"sidecar {seg_b['cut_per_rev']} · smoke {density['shipped_rate_per_rev']}")
    # ------------------------------------------------------------------
    # ⚑ THE BOOM. Three rows where A2g had one, because R-CPB-17 struck the
    #   law A2g's single row was checking. A ledger row that survives a ruling
    #   unchanged is certifying the world the ruling replaced.
    # ------------------------------------------------------------------
    # the rig read, RECOMPUTED here from wr1's own two constants — 34.0 m for a
    # 17.5 m room, applied to the WEREWOLF room's 37.5 m. Exactly 510/7.
    rig_read = 34.0 * (37.5 / 17.5)
    ok &= verify("the boom is the wr1 rig's REALIZED werewolf-shot distance, read and not chosen",
                 close(der["boom_m"], rig_read, 1e-9)
                 and close(der["boom_m"], 510.0 / 7.0, 1e-9)
                 and der["boom_pin_matches_rig_read"] is True,
                 f"wr1_level_rig.gd:28-29 applied to wr1_level.gd:87 -> "
                 f"34.0 x (37.5 / 17.5) = {rig_read:.9f} m = 510/7; sidecar boom "
                 f"{der['boom_m']:.9f} m; the scene's own pin check "
                 f"{der['boom_pin_matches_rig_read']} at delta {der['boom_pin_delta_m']:.3g}")
    # ⚑ ROOM-INVARIANCE, CHECKED RATHER THAN DECLARED. The eye is recomputed from
    #   (aim, angles, boom) with NO ROOM DIMENSION ANYWHERE IN THIS ARITHMETIC. If
    #   it reproduces the rendered eye, the rendered camera is a function of those
    #   three things and of nothing else — which is R-CPB-17, as a measurement.
    p = math.radians(der["pitch_deg"])
    y = math.radians(der["yaw_deg"])
    aim = der["aim_world"]
    eye_recomputed = [aim[0] + der["boom_m"] * math.cos(p) * math.sin(y),
                      aim[1] - der["boom_m"] * math.sin(p),
                      aim[2] + der["boom_m"] * math.cos(p) * math.cos(y)]
    ok &= verify("the camera is (station, angles, boom) and NO room dimension — recomputed",
                 all(close(a, b, 1e-3) for a, b in zip(eye_recomputed, cam_b["eye"]))
                 and der["room_size_influences_camera"] is False
                 and der["rectangle_is_an_input_to_the_camera"] is False,
                 f"wr1 orbit of yaw {der['yaw_deg']} / pitch {der['pitch_deg']} at boom "
                 f"{der['boom_m']:.6f} m about aim {aim} = "
                 f"[{eye_recomputed[0]:.3f}, {eye_recomputed[1]:.3f}, {eye_recomputed[2]:.3f}] "
                 f"vs rendered {[round(v,3) for v in cam_b['eye']]} — the 86.915 x 85.303 m "
                 f"rectangle appears in no term")
    # and the boom as the RENDERED camera actually realizes it: |eye - aim|
    realized_boom = math.dist(cam_b["eye"], cam_b["look_at"])
    ok &= verify("the boom the frames were shot at is the boom that was pinned",
                 close(realized_boom, der["boom_m"], 1e-3),
                 f"|eye - aim| off the rendered camera = {realized_boom:.6f} m vs pinned "
                 f"{der['boom_m']:.6f} m (A2g shot the same frame at 168.863429 m)")
    ok &= verify("the arena rectangle reaches the manifest as a REPORT, not as an input",
                 close(der["rectangle_longer_side_m"],
                       max(der["rectangle_size_x_m"], der["rectangle_size_z_m"]), 1e-9),
                 f"GL-13 {der['rectangle_size_x_m']:.3f} x {der['rectangle_size_z_m']:.3f} m read "
                 f"and never moved; longer side {der['rectangle_longer_side_m']:.3f} m is carried "
                 f"as the scale reference the measured block reports against")
    ok &= verify("the lens is the canon lens, verbatim",
                 (der["yaw_deg"], der["pitch_deg"], cam_b["fov_deg"]) == (47.0, -50.0, 24.0),
                 f"yaw {der['yaw_deg']} / pitch {der['pitch_deg']} / fov {cam_b['fov_deg']} "
                 f"from {der['source_file']}")
    ok &= verify("the aim height is wr1's convention, not this file's",
                 close(der["aim_up_m"], 1.0, 1e-9) and close(aim[1], 1.0, 1e-6),
                 f"aim {aim} = station + {der['aim_up_m']} m ({der['aim_convention_source'][:52]}…)")
    ok &= verify("the ellipse is MEASURED and its prediction is carried, not substituted",
                 "measured_minor_over_major" in ell and ell["points_projected"] > 0,
                 f"measured {ell['measured_minor_over_major']:.6f} from "
                 f"{ell['points_projected']} projected points; predicted "
                 f"{ell['analytic_sin_depression']:.6f}")
    ok &= verify("the subject fraction is measured through the rendering camera",
                 subj["screen_height_fraction"] > 0.0,
                 f"{subj['screen_h_px']:.2f} px of 1080 = "
                 f"{100.0*subj['screen_height_fraction']:.3f} % on a "
                 f"{subj['world_height_m']:.3f} m subject")
    ok &= verify("the camera gate passed on the pose that rendered",
                 seg_a["camera_gate"]["ok"] and seg_b["camera_gate"]["ok"]
                 and seg_b["camera_gate"]["fov_deg"] == cam_b["fov_deg"],
                 f"9 rays, gate fov {seg_b['camera_gate']['fov_deg']} == render fov "
                 f"{cam_b['fov_deg']}")
    ok &= verify("the clock is CLK-1's, untouched: preroll 60, tick-frozen, both segments",
                 seg_a["preroll_frames_tick_frozen"] == seg_b["preroll_frames_tick_frozen"] == 60,
                 f"{seg_b['preroll_frames_tick_frozen']} tick-frozen warm-up frames, pruned")
    ok &= verify("the concatenated file is exactly its parts — no frame lost, none invented",
                 int(v_tmp.get("nb_frames", 0)) == frames_in_parts,
                 f"ffprobe {v_tmp.get('nb_frames')} on the concat vs "
                 f"{'+'.join(str(r['frames']) for r in timeline)} = {frames_in_parts} in the parts")
    # ⚑ 1x TRACE TIME, TO WITHIN THE FRAME QUANTIZATION, AND THE SLACK IS NAMED.
    #   A 130-tick window is 318.37 frames at 30 fps: the scene renders ceil() of
    #   that and the movie writer emits one more (the iteration it quits on). So
    #   playback runs up to TWO frames long against the trace span, structurally,
    #   and the bar is two frames rather than a number chosen to pass.
    ok &= verify("each segment plays 1x trace time, to within the frame quantization",
                 all(close(r["duration_s"], sidecars[f"{r['segment']}-{r['shot']}"]["trace_seconds"],
                           2.0 / 30.0 + 1e-4)
                     for r in timeline if r["segment"] != "SEAM"),
                 " · ".join(f"{r['segment']} {r['duration_s']:.4f} s playback vs "
                            f"{sidecars[f'''{r['segment']}-{r['shot']}''']['trace_seconds']:.4f} s "
                            f"of trace (delta "
                            f"{r['duration_s'] - sidecars[f'''{r['segment']}-{r['shot']}''']['trace_seconds']:+.4f} s = "
                            f"{30.0*(r['duration_s'] - sidecars[f'''{r['segment']}-{r['shot']}''']['trace_seconds']):+.2f} frames)"
                            for r in timeline if r["segment"] != "SEAM"))
    ok &= verify("the seam actually dips to black",
                 seam["seam_luma_max_Y"] is not None and seam["seam_luma_max_Y"] <= 20.0,
                 f"held black max Y {seam['seam_luma_max_Y']} over {seam['frames_sampled']} "
                 f"frames, against picture Y {seam['picture_luma_mean_Y_before_the_dip']}")
    ok &= verify("no diagnostic switch was on: these are shipped frames",
                 seg_a["clk1_diagnostics"]["shipped_configuration"]
                 and seg_b["clk1_diagnostics"]["shipped_configuration"],
                 "anim on · fx on · phaselog off, on both segments")
    ok &= verify("the baton behind the frames is the run's baton (GL-6)",
                 seg_a["baton_sha256"].startswith("d7ecd866ac45")
                 and seg_a["baton_sha256"] == seg_b["baton_sha256"],
                 f"{seg_b['baton_sha256'][:12]}… on both segments")
    ok &= verify("the A2e reference this manifest compares against is the file Matt watched",
                 PREV_MP4.exists()
                 and sha256_of(PREV_MP4).startswith("e2f6a03cc490"),
                 f"{PREV_MP4.name} recomputed from bytes = "
                 f"{sha256_of(PREV_MP4)[:12] if PREV_MP4.exists() else 'ABSENT'}…")

    # ------------------------------------------------------------------
    # ⚑ THE PRE-REGISTERED CORNER FACT. A2gr-0 predicted all four corners
    #   outside the frame and required it be reported as a FACT rather than
    #   discovered as a failure. A prediction recorded before the render and
    #   checked after it is worth more than either half alone.
    # ------------------------------------------------------------------
    ok &= verify("all four GL-13 corners fall OUTSIDE the frame — pre-registered, and a fact",
                 gl13["corners_outside_frame"] == 4,
                 f"{gl13['corners_outside_frame']} of 4 corners outside; the frame spans "
                 f"{gl13['frame_spans_m_across_at_aim_plane']:.2f} m across at the aim plane "
                 f"against a {gl13['rectangle_longer_side_m']:.3f} m arena. R-CPB-17(b): rooms "
                 f"crop. At A2g's 168.863 m two of four were already outside")

    # ------------------------------------------------------------------
    # ⚑ THE vs-A2g PROOF, AND IT IS THE WHOLE ARGUMENT OF THIS CELL. A2g and
    #   A2g-r differ by ONE authored change. That is a claim about which fields
    #   moved and which did not, so it is checked as one: every tick and layout
    #   field must be IDENTICAL, and every camera field must DIFFER. Either half
    #   failing alone would falsify the cell — identical camera fields would mean
    #   the boom never landed; a moved layout field would mean something else did.
    # ------------------------------------------------------------------
    if a2g_b is not None:
        same = [f for f in A2G_INVARIANT_FIELDS if seg_b.get(f) == a2g_b.get(f)]
        differ = [f for f in A2G_INVARIANT_FIELDS if seg_b.get(f) != a2g_b.get(f)]
        ok &= verify("every tick and layout invariant matches A2g's sidecar, field for field",
                     not differ,
                     f"{len(same)}/{len(A2G_INVARIANT_FIELDS)} identical: "
                     + ", ".join(f"{f}={seg_b.get(f)!r}" for f in A2G_INVARIANT_FIELDS[:6])
                     + f", …(+{len(A2G_INVARIANT_FIELDS)-6} more)"
                     + (f" — MOVED: {differ}" if differ else ""))
        a2g_cam = a2g_b["camera"]
        a2g_der = a2g_b["canon_derivation"]
        ok &= verify("and the camera DID move — the boom is the only authored change",
                     a2g_cam["eye"] != cam_b["eye"]
                     and a2g_cam["look_at"] == cam_b["look_at"]
                     and a2g_cam["fov_deg"] == cam_b["fov_deg"]
                     and a2g_der["yaw_deg"] == der["yaw_deg"]
                     and a2g_der["pitch_deg"] == der["pitch_deg"],
                     f"eye {[round(v,2) for v in a2g_cam['eye']]} -> "
                     f"{[round(v,2) for v in cam_b['eye']]}; aim, fov, yaw and pitch ALL "
                     f"unchanged ({cam_b['look_at']} / {cam_b['fov_deg']} / {der['yaw_deg']} / "
                     f"{der['pitch_deg']}); distance {a2g_der['distance_m']:.6f} -> "
                     f"{der['distance_m']:.6f} m")
    else:
        ok &= verify("A2g's sidecar is on disk so the one-delta claim can be checked",
                     False, f"ABSENT at {A2G_DIR} — the vs-A2g proof cannot be taken")

    # ------------------------------------------------------------------
    # ⚑ NOTE-80: THE PARTS THIS TOOL READ ARE THIS CELL'S PARTS. The freshness
    #   check is not decoration — until this cell the parts lived in a shared
    #   directory under names A2g had already written, and `part_facts()` would
    #   have read them without noticing. Cell-scoping is the fix; this row is the
    #   proof that the fix is in force for the bytes actually promoted.
    # ------------------------------------------------------------------
    a2g_newest = max((f.stat().st_mtime for f in A2G_DIR.glob("*")), default=0.0)
    part_paths = [PARTS_DIR / f"tmp-{seg}-{shot}.mp4" for seg, shot in PART_ORDER
                  if seg != "SEAM"]
    ok &= verify("the parts this timeline was read from are THIS cell's, not the last cell's",
                 all(p.exists() and p.stat().st_mtime > a2g_newest for p in part_paths)
                 and DELIV_STEM in str(PARTS_DIR),
                 f"{len(part_paths)} parts under {PARTS_DIR.name}/ (cell-scoped), every one "
                 f"written after the newest byte in the A2g capture "
                 f"({', '.join(f'{p.name} +{p.stat().st_mtime - a2g_newest:.0f}s' for p in part_paths if p.exists())})")

    if not ok:
        print("[promote] HALT — the claim ledger is not clean. A manifest that asserts what "
              "was not measured is a defect, so nothing is promoted and nothing is written.")
        return 15

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
    prev = json.loads((PREV_DIR / "MANIFEST.json").read_text())

    # ⚑ THE DEMOTED FRAMES, MEASURED RATHER THAN QUOTED. The A2e manifest's
    #   ellipse figures are ANALYTIC — sin(depression), which is the ORTHOGRAPHIC
    #   answer — and comparing a measurement against a prediction and calling the
    #   difference "the lens change" would be sloppy. The FG-10 matrix rendered
    #   both demoted shots in this same run and their sidecars carry the same
    #   projection instrument, so the comparison costs nothing and is like for
    #   like. If the probe sidecars are absent the block says so (GL-12) rather
    #   than falling back to the prediction.
    demoted_measured = {}
    for shot in ("b-ring", "d-close"):
        p = TMP / "probe-sidecars" / f"shot-B-undulating-{shot}.json"
        if not p.exists():
            demoted_measured[shot] = "ABSENT — no probe sidecar on disk for this leg"
            continue
        d = json.loads(p.read_text())
        o = d["optics_measured"]
        demoted_measured[shot] = {
            "fov_deg": d["camera"]["fov_deg"],
            "tick": d["tick_from"],
            "ring_ellipse_minor_over_major_MEASURED":
                o["cut_ring_ellipse"]["measured_minor_over_major"],
            "ring_ellipse_minor_over_major_PREDICTED_by_sin_depression":
                o["cut_ring_ellipse"]["analytic_sin_depression"],
            "prediction_error_pct": round(100.0 * (
                o["cut_ring_ellipse"]["measured_minor_over_major"]
                / o["cut_ring_ellipse"]["analytic_sin_depression"] - 1.0), 3),
            "ring_major_axis_px": o["cut_ring_ellipse"]["major_axis_px"],
            "subject_screen_height_fraction": o["subject"]["screen_height_fraction"],
            "px_per_metre_at_station": o["subject"]["px_per_metre_at_station"],
        }
    demoted_measured["⚑ what this comparison shows"] = (
        "sin(depression) is the ORTHOGRAPHIC ellipse and the manifests before A2g "
        "reported it as though it were the ring. The prediction's error grows as the boom "
        f"comes in, and this cell is the third point on that curve: A2g +0.0035 % at "
        f"168.9 m, THIS clip "
        f"{100.0*(ell['measured_minor_over_major']/ell['analytic_sin_depression']-1.0):+.4f} % at "
        f"{der['boom_m']:.1f} m, d-close +13.4 % at 4.3 m (measured 0.5305 against a predicted "
        "0.4679 — the prediction is 12 % low, because a circle 2.2 m across seen from 4.3 m "
        "away is not a parallel projection). ⚑ THE POINT IS NOT THE ERROR, IT IS THAT THE "
        "ERROR IS KNOWN: every figure this manifest reports for the ring is the MEASURED one, "
        "and the prediction rides beside it. The A2e figures Matt was given for the close shot "
        "were the formula, not the frame.")
    demoted_measured["provenance"] = (
        "read off the FG-10 probe legs' own sidecars from THIS run (legs 4 and 5, "
        "d-close/undulating and b-ring/undulating, 4 passes each, one distinct state each), "
        "through the same unproject_position instrument as the canon numbers.")

    manifest = {
        "cell": "SB-1 Cell A2g-r — THE LOOK DISTANCE (rate 17 + fixed clock + the "
                "Grim-Dawn-matched lens, at the ratified boom). THE BINDING FRAME.",
        "ledger_rows": ("R-CPB-17 (the boom / the distance fork ruled, Matt) · R-CPB-16 (camera "
                        "canon, Matt) · R-CPB-15 (the rate lever, Matt) · CLK-1-1 / CLK-1-2 (the "
                        "clock) · A2gr-0 (this charter) · A2g-1 / A2g-2 (the predecessor and its "
                        "routed fork)"),
        "date": date.today().isoformat(),
        "artifact_class": ("E — owner-eye. UNTRACKED, never committed. Keep until viewed + veto "
                           "window closed, then demote to class D (PL-5)."),
        "framing_sentence": FRAMING,
        "the_question_this_answers": (
            "A2g put the canon LENS on the arena and, by the canon's own distance LAW, put the "
            "eye 168.863 m out and the man at 5.59 % of frame height — sixty pixels. Matt ruled "
            "the fork: 'oh wow, the camera angle and zoom should have nothing to do with room "
            "size. nothing at all.. that is ludicrous.' (R-CPB-17.) So the law is STRUCK and the "
            "boom is FIXED at the werewolf shot's realized 72.857 m — the frame his eye ratified. "
            "This clip is the same 10.6 s of trace, the same seed, the same everything, at that "
            "boom. R-CPB-17(d) routes the BINDING eye-calls here: density feel, palette knee, "
            "cadence read, and the CLK-1 FX-draw question that A2g's geometry deferred."),
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
        "camera_canon": {
            "ruling": der["ruling"],
            "derivation": der,
            "camera_as_rendered": {"eye": cam_b["eye"], "look_at": cam_b["look_at"],
                                   "fov_deg": cam_b["fov_deg"], "far_m": cam_b["far_m"]},
            "camera_identical_across_segments": cam_a == cam_b,
            "gate": {"ok": seg_b["camera_gate"]["ok"],
                     "rays": len(seg_b["camera_gate"]["rays"]),
                     "skirt_half_m": seg_b["camera_gate"]["skirt_half_m"],
                     "fog_depth_end_m": seg_b["camera_gate"]["fog_depth_end_m"]},
        },
        "optics_measured": opt,
        "elevation_parallax_predicted": parallax_analytic(cam_b, etch["height_m"],
                                                          etch["radius_m"]),
        "density_realized": density,
        "seam": seam,
        "epoch_schedule_realized_segment_B": {
            "canon": seg_b["epoch_schedule_realized"],
            "count_in_window": seg_b["epoch_count_in_window"],
            "basis": ("computed from CUT_SEED alone for this exact tick window, so the manifest "
                      "can be CHECKED against the frames rather than believed: each row is a "
                      "sequence's start tick, its length in births, the gap that follows it, and "
                      "the ANGULAR bearing at which it begins again."),
        },
        "cadence_A": seg_a["cadence"],
        "cadence_B": seg_b["cadence"],
        "palette": seg_b["palette"],
        "measured_at_1_95": measured_1_95,

        # ------------------------------------------------------------------
        # ⚑ THE ANCESTRY BLOCK. Matt watched ONE clip. Three things have moved
        #   since, and the point of this block is that he can tell which is
        #   which and on whose word each one moved.
        # ------------------------------------------------------------------
        "ancestry_vs_the_clip_you_watched": {
            "reference": {
                "file": prev["deliverable"]["file"],
                "sha256": prev["deliverable"]["sha256"],
                "bytes": prev["deliverable"]["bytes"],
                "duration_s": prev["deliverable"]["duration_s"],
                "cell": prev["cell"],
                "verified_here": "sha256 recomputed from the bytes on disk before this block "
                                 "was written; see the claim ledger.",
            },
            "delta_1_RATE": {
                "what_moved": "CUT_PER_REV 11 -> 17",
                "on_whose_word": "MATT (R-CPB-15): 'we could increase the sequence rate across "
                                 "the board and see what it looks like.'",
                "landed_by": "Cell A2f item 1, commit 34dcd41",
                "before": {"cut_per_rev": A2E_MEASURED["cut_per_rev"],
                           "stationary_mean_per_rev": A2E_MEASURED["stationary_mean_per_rev"],
                           "undulating_mean_per_rev": A2E_MEASURED["undulating_mean_per_rev"],
                           "undulating_thick_thin": A2E_MEASURED["undulating_thick_thin"],
                           "source": A2E_MEASURED["source"]},
                "after": {"cut_per_rev": density["shipped_rate_per_rev"],
                          "stationary_mean_per_rev": density["stationary"]["mean_per_rev"],
                          "undulating_mean_per_rev": density["undulating"]["mean_per_rev"],
                          "undulating_thick_thin": density["undulating"]["thick_over_thin"],
                          "source": "measured by the smoke at HEAD, this run"},
                "the_number_that_matters": (
                    f"the undulating mean is back inside the ratified band: "
                    f"{density['undulating']['mean_per_rev']} against 11.0 ± 0.5, and the BREATH "
                    f"widened rather than flattening — thick/thin "
                    f"{A2E_MEASURED['undulating_thick_thin']} -> "
                    f"{density['undulating']['thick_over_thin']}."),
                "costs_nothing_visually_elsewhere": (
                    "CLK-1 measured the raise against the A2e bytes at rate 11 and found the "
                    "residual at +0.40/channel above the codec floor — A2e's own clock jitter. "
                    "The raise changed the cut layout and no other pixel."),
            },
            "delta_2_CLOCK": {
                "what_moved": ("locomotion phase is now a pure function of the tick "
                               "(per-tick seek_phase) + a 60-frame TICK-FROZEN warm-up preroll "
                               "that is rendered and thrown away"),
                "on_whose_word": ("the run's: A2f's FG-10 halt proved the scene had never "
                                  "rendered the same span twice; CLK-1 convicted a one-time "
                                  "RENDERER transient at engine frames 18..25 and excluded it."),
                "landed_by": "Cell CLK-1 items 1-2, commits e81a827 + 6eff089",
                "visual_cost_decomposed_and_MEASURED_at_CLK_1_not_re_measured_here": {
                    "codec_floor_mean_abs_delta_per_channel": 0.95,
                    "a2e_own_jitter_plus_head_residual": 0.40,
                    "the_locomotion_seek": 0.14,
                    "the_warm_up_preroll": 5.01,
                    "reading": ("the fix everyone feared moves the picture by 0.14 of 255 — "
                                "0.06 % of full scale. 97 % of the change is the PREROLL, and it "
                                "is a different DRAW of the smoke bed and spark ring (lower "
                                "centre of frame; top quarter 0.03-1.38), a layer A2e § 0 had "
                                "already declared was one draw from a distribution. No body, no "
                                "geometry, no palette, no cut layout."),
                    "source": ("MEASURED at CLK-1 with `drax/tools/kc2_clk1_vs_a2e.py` against "
                               "the sha-pinned A2e bytes, codec floor subtracted. CITED here, "
                               "not re-measured — re-measuring it against a clip with a "
                               "different LENS would confound the two deltas."),
                    "⚑ the_caveat_on_citing_it": (
                        "those four numbers were measured THROUGH THE OLD LENS, at b-ring and "
                        "d-close, where the smoke bed and spark ring filled the lower centre of "
                        "the frame. Under the canon frame the same 3.0 m bed is a few dozen "
                        "pixels across, so the preroll's +5.01 does NOT transfer to this clip as "
                        "a magnitude — what transfers is the DECOMPOSITION (the clock fix is "
                        "3 % of it, the FX re-draw 97 %) and the conclusion (no body, no "
                        "geometry, no palette, no cut layout moved). Quoting +5.01 as this "
                        "clip's delta would be quoting a measurement of a different picture."),
                },
                "what_it_buys": ("FG-10 now returns ONE distinct state on every leg of a "
                                 "five-leg matrix, and the two promoted legs are probed at FULL "
                                 "SPAN. The frames in this file are reproducible from the pinned "
                                 "baton and the pinned code."),
            },
            "delta_3_LENS_ANGLES": {
                "what_moved": ("fov 48 with scene-derived offsets (b-ring eye +6.5/5.6/7.0, "
                               "d-close +2.4/3.0/2.7) -> the canon lens: yaw 47 / pitch -50 / "
                               "fov 24, copied verbatim out of wr1_level_rig.gd:25-27"),
                "on_whose_word": ("MATT (R-CPB-16): 'The werewolf scene is our canonical camera "
                                  "angle/zoom as it is set to match grim dawn... we should use "
                                  "it as canon for the time being, especially while testing GD "
                                  "scenes.'"),
                "landed_by": "Cell A2g item 1, commit c011182 — UNCHANGED by this cell",
                "⚑ scope_of_this_delta": (
                    "ANGLES AND ZOOM ONLY. A2g also took the DISTANCE from that rig, by its "
                    "same-angular-size law, and that half is now its own delta below — R-CPB-17 "
                    "separated them, and this manifest keeps them separated so Matt can see that "
                    "the thing he ratified in A2g (the lens) never moved and the thing he struck "
                    "(the law) is the only thing that did."),
                "before": {
                    "b-ring": {"fov_deg": prev["camera"]["B-undulating-b-ring"]["fov_deg"],
                               "eye": prev["camera"]["B-undulating-b-ring"]["eye"],
                               "ring_ellipse_minor_over_major":
                                   prev["elevation_parallax"]["b-ring"]
                                   ["ring_ellipse_minor_over_major"],
                               "depression_deg": prev["elevation_parallax"]["b-ring"]
                                   ["depression_angle_deg"]},
                    "d-close": {"fov_deg": prev["camera"]["B-undulating-d-close"]["fov_deg"],
                                "eye": prev["camera"]["B-undulating-d-close"]["eye"],
                                "ring_ellipse_minor_over_major":
                                    prev["elevation_parallax"]["d-close"]
                                    ["ring_ellipse_minor_over_major"],
                                "depression_deg": prev["elevation_parallax"]["d-close"]
                                    ["depression_angle_deg"]},
                    "note": ("read off the A2e MANIFEST, not retyped. Both of those poses are "
                             "now DIAGNOSTIC INSTRUMENTS (R-CPB-16(d)), not segments."),
                    # ⚑ AND THOSE TWO ELLIPSE FIGURES ARE PREDICTIONS, WHICH MAKES
                    #   COMPARING THEM AGAINST A MEASUREMENT AN UNFAIR COMPARISON —
                    #   so the demoted frames were MEASURED too, for free, off the
                    #   FG-10 probe legs that rendered them in this same run.
                    "MEASURED_at_HEAD_off_the_FG10_probe_legs": demoted_measured,
                },
                "after": {
                    "fov_deg": cam_b["fov_deg"], "yaw_deg": der["yaw_deg"],
                    "pitch_deg": der["pitch_deg"],
                    "ring_ellipse_minor_over_major_MEASURED":
                        ell["measured_minor_over_major"],
                    "ring_ellipse_minor_over_major_predicted":
                        ell["analytic_sin_depression"],
                },
                "the_parallax_re_declared": (
                    f"the cut ring's minor/major goes "
                    f"{prev['elevation_parallax']['b-ring']['ring_ellipse_minor_over_major']:.4f} "
                    f"/ "
                    f"{prev['elevation_parallax']['d-close']['ring_ellipse_minor_over_major']:.4f}"
                    f" -> {ell['measured_minor_over_major']:.4f} MEASURED. The ring OPENS toward "
                    f"circular: at the old depressions it read as a squashed band, at pitch -50 "
                    f"it reads as very nearly the circle it is. ⚑ AND THIS IS THE ROW THAT PROVES "
                    f"THE BOOM WAS THE ONLY CHANGE SINCE A2g: the ellipse is a function of the "
                    f"ANGLE, so moving the eye in along its own axis must leave it alone — A2g "
                    f"measured 0.765857 at 168.863 m, this clip measures "
                    f"{ell['measured_minor_over_major']:.6f} at {der['boom_m']:.3f} m."),
            },

            # ------------------------------------------------------------------
            # ⚑ DELTA 4 — THE BOOM. THE ONE THING THAT MOVED SINCE THE LAST CLIP.
            # ------------------------------------------------------------------
            "delta_4_BOOM": {
                "what_moved": (f"the camera distance: 168.863429 m, derived by the wr1 "
                               f"same-angular-size law from this arena's 86.915 m edge, -> a "
                               f"FIXED {der['boom_m']:.9f} m that no room can move"),
                "on_whose_word": ("MATT (R-CPB-17), verbatim: 'oh wow, the camera angle and zoom "
                                  "should have nothing to do with room size. nothing at all.. "
                                  "that is ludicrous.'"),
                "landed_by": "Cell A2g-r item 1 (this cell), commits 4646dd2 + 9e6068d",
                "what_was_struck": {
                    "the_law": "DIST = 34.0 * (EDGE / 17.5)  —  wr1_level_rig.gd:28-29",
                    "its_status_now": ("STRUCK from the presentation canon (R-CPB-17(a)) and "
                                       "demoted to what it always was: R-6's ROOM-VERIFICATION "
                                       "convention — a judge instrument for 'does this room fit "
                                       "the frame'. Legitimate there. It remains in "
                                       "wr1_level_rig.gd UNTOUCHED; that file is wr1's. This shot "
                                       "simply stops calling it."),
                    "the_question_it_answers": ("NOTE-78 asked which invariant a transplanted "
                                                "canon means. R-CPB-17 answers: THE SUBJECT, not "
                                                "the room."),
                },
                "where_the_number_came_from": {
                    "rule": ("GL-17 reference-governs: READ the rig's realized werewolf-shot "
                             "distance, print the read, pin the constant with the citation. Do "
                             "not choose a number."),
                    "read": ("wr1_level_rig.gd:28-29 (ROOM_DIST = 34.0 * (ROOM_EDGE / 17.5)) "
                             "applied to wr1_level.gd:87 (ROOM_EDGE = 37.5 m)"),
                    "arithmetic": f"34.0 x (37.5 / 17.5) = 510/7 = {der['boom_m']:.15f} m",
                    "charter_expectation": "~72.857 m",
                    "delta_from_expectation_m": round(der["boom_m"] - 72.857, 9),
                    "verdict": ("MATCH to 0.14 mm — nothing to route up. The charter required a "
                                "HALT if the rig's realized number differed materially; it does "
                                "not."),
                    "pinned_as": ("a LITERAL in kc2_cpb_clip.gd, not a live reference. A literal "
                                  "is the only form of this number no room dimension can reach — "
                                  "if wr1's room ever changes size, this camera must NOT move, and "
                                  "a live link would quietly re-introduce exactly what was struck. "
                                  "The scene recomputes the read and compares "
                                  f"(pin delta {der['boom_pin_delta_m']:.3g}, "
                                  f"{der['boom_pin_matches_rig_read']}), so the pin is checked "
                                  "rather than trusted."),
                },
                "the_subject_re_declared": (
                    f"{subj['world_height_m']:.3f} m of man-and-hammer subtends "
                    f"{subj['screen_h_px']:.1f} px of 1080 = "
                    f"{100.0*subj['screen_height_fraction']:.2f} % of frame height. ⚑ THAT IS THE "
                    f"GRIM DAWN REGISTER, AND IT IS THE POINT OF THE RULING: the werewolf frame "
                    f"Matt ratified put a subject of this size at 12.96 %, and this clip lands at "
                    f"{100.0*subj['screen_height_fraction']:.2f} % because it is shot from the "
                    f"same boom. A2g put it at 5.59 %."),
                "what_the_canon_s_OWN_shots_now_agree_ON": {
                    "wr1 room shot, 37.5 m room at 72.857 m (RATIFIED BY EYE)": "~12.96 %",
                    "THIS clip, 86.915 m arena at the same boom":
                        f"{100.0*subj['screen_height_fraction']:.2f} %",
                    "reading": ("the two agree because the boom is the same, which is the whole "
                                "content of a room-size-invariant camera: a body reads the same "
                                "in a 37.5 m room and an 86.9 m one. Under the struck law they "
                                "differed by 2.3x."),
                },
                "what_it_costs_and_the_cost_is_not_hidden": {
                    "the_room_crops": (
                        f"the frame spans {gl13['frame_spans_m_across_at_aim_plane']:.2f} m across "
                        f"and {gl13['frame_spans_m_down_at_aim_plane']:.2f} m down at the aim "
                        f"plane, against a {gl13['rectangle_longer_side_m']:.3f} m arena, so ALL "
                        f"FOUR GL-13 corners fall outside it "
                        f"({gl13['corners_outside_frame']} of 4, pre-registered in A2gr-0 and "
                        f"checked in the claim ledger). This is R-CPB-17(b): rooms crop. GL-13 "
                        f"pins the rectangle in the WORLD and never promised it fits a frame "
                        f"(NOTE-77). ⚑ THIS CLIP IS NOT AN ARENA OVERVIEW."),
                    "at_A2g_two_of_four_were_already_outside": (
                        "so this is a difference of degree, not of kind — and R-6's own 17.5 m "
                        "room did not fit either."),
                },
                "the_edge_judgement_is_DISSOLVED_not_resolved": (
                    "A2g's one declared judgement was maxf-vs-minf on a non-square rectangle, "
                    "worth 1.9 % of distance and parked veto-open at A2g-2(3). With the boom "
                    "fixed there is no edge to choose: the judgement does not need deciding, it "
                    "stops existing. A2gr therefore carries ZERO camera judgements — every term "
                    "is a ruling or a read."),
            },

            # ------------------------------------------------------------------
            # ⚑ AND THE SAME ANCESTRY AGAINST THE IMMEDIATE PREDECESSOR, WHERE THE
            #   DECLARED DELTA COUNT IS EXACTLY ONE. Matt has not watched A2g — the
            #   conductor audited five of its frames — but it is the clip this one
            #   is a revision OF, so "one authored change" has to be checkable
            #   against it rather than asserted about it.
            # ------------------------------------------------------------------
            "ancestry_vs_A2g_the_clip_this_one_revises": {
                "reference": {
                    "file": "a2g-canon-cadence-ab.mp4",
                    "cell": "SB-1 Cell A2g — THE CANON FRAME",
                    "status": ("DEMOTED to a diagnostic by R-CPB-17(c). Its proofs CARRY: "
                               "transplant exactness, full-span FG-10, cross-cell digest "
                               "identity, the corrected ellipse measurements on the demoted "
                               "shots."),
                },
                "declared_deltas": 1,
                "the_one_delta": (f"the boom: 168.863429 m -> {der['boom_m']:.9f} m. "
                                  f"R-CPB-17, Matt's ruling."),
                "checked_how": ("the claim ledger compares this cell's segment-B sidecar against "
                                f"A2g's, field for field, over {len(A2G_INVARIANT_FIELDS)} named "
                                "tick / layout / article / clock fields — including the whole "
                                "36-row realized epoch schedule, which is a function of CUT_SEED "
                                "and the tick window and of nothing a camera can touch. Every one "
                                "must be IDENTICAL and the camera must DIFFER; either half "
                                "failing falsifies the cell."),
                "invariant_fields_compared": A2G_INVARIANT_FIELDS,
                "⚑ what_the_FG10_digests_do_and_do_not_prove": (
                    "the frame digests differ from A2g's EVERYWHERE, and they must: the camera "
                    "moved, so every pixel moved. Determinism is per-leg internal (4 passes, one "
                    "distinct state). The cross-cell identity A2g could assert on legs 4 and 5 "
                    "still holds here for the DEMOTED shots, whose poses this cell did not touch "
                    "— see fg10_determinism. Those two digests are the arithmetic proof that "
                    "nothing outside `_canon_pose` moved."),
            },
            "what_did_NOT_move": (
                "WEAPON_SCALE 1.95, the grip constants, the palette ramp and its knee, the epoch "
                "bands, the spin period 0.36 s, the cut pool, the seed, the tick window, the "
                "baton, the clock (PREROLL 60 + per-tick seek), and — since A2g — the lens "
                "ANGLES (yaw 47 / pitch -50 / fov 24) and the player-anchored aim. Verified in "
                "the sidecars above, at the commit, and field-for-field against A2g's own "
                "sidecar in the block below."),
        },

        "claims_verified": CLAIMS,
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
            "second_live_run": ("A2f surface 8 was 'this tool is wired and has never been run'; "
                                "A2g was its first end-to-end execution. A2g-r is the second, and "
                                "it is the first time the ledger has been re-pointed at a RULING "
                                "rather than at a render: four rows about the struck distance law "
                                "were replaced by four rows about the boom, because a ledger row "
                                "that survives a ruling unchanged is certifying the world the "
                                "ruling replaced."),
            "parts_are_cell_scoped": (
                f"{PARTS_DIR} — NOTE-80. `part_facts()` used to read `$TMP/tmp-$SEG-$SHOT.mp4`, a "
                "path shared across cells, with A2g's two parts sitting in exactly those names "
                "and the harness not checking ffmpeg's exit status. The claim ledger now proves "
                "the parts it read were written after the newest byte in the A2g capture."),
        },
        "fg10_determinism": (TMP / "fg10-probe.txt").read_text().strip()
        if (TMP / "fg10-probe.txt").exists() else "MISSING — the gate log is not on disk",
        "fg12_prune": (TMP / "fg12-prune-receipts.txt").read_text().strip()
        if (TMP / "fg12-prune-receipts.txt").exists() else "receipts missing",
        "r_a1_1": ("ZERO text nodes anywhere in the scene — the motion smoke walks the whole "
                   "tree with the player, pose, cuts, smoke and bursts in it and counts 0 "
                   "text/canvas nodes (5,123 nodes walked at HEAD). The dip-to-black seam is an "
                   "ENCODE filter, so it cannot introduce one either. Every word about this clip "
                   "is in this file."),
        "gl15": ("one ongoing-damage read: no damage numbers, no per-cut UI, nothing flashes, "
                 "ticks or counts. The whirlwind's cuts are ONE event."),
        "gl13": ("the pinned rectangle was READ and never moved: "
                 f"{der['rectangle_size_x_m']:.3f} x {der['rectangle_size_z_m']:.3f} m. ⚑ AND AT "
                 "A2g-r IT IS NO LONGER AN INPUT TO ANYTHING. A2g derived the canon distance FROM "
                 "it; R-CPB-17 struck that derivation, so the rectangle is now read purely to be "
                 "REPORTED — the scale reference the measured block quotes against and the number "
                 "that makes 'the room crops' checkable. Nothing about the clip writes to it, and "
                 "now nothing about the camera reads it either."),
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
