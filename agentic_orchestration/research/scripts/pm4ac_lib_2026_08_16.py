#!/usr/bin/env python3
"""KC2-PM4 Lap AC shared library — THE REFERENT SIDE OF THE RESIDENCE.

READ-ONLY on every external source (referent MP4, pinned Lap H-2 / Lap R artifacts).
OUTCOME-FIREWALLED: no simulation output file, cell, code or telemetry is opened by this
module or by anything that imports it.

Every constant below is pre-registered in
  agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/prereg.md
whose sha256 is asserted at instrument start.  No value here was chosen after seeing a result.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.  Run KC2-PM4, Lap AC.
"""
from __future__ import annotations

import csv
import hashlib
import pathlib
import sys
from typing import Dict, List, Sequence, Tuple

import numpy as np

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
NOTES = META / "agentic_orchestration" / "legolas" / "notes"
LAPH2 = NOTES / "2026-08-13-kc2-pm4-lap-h2-video-match"
LAPR = NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact"
LAPAB = NOTES / "2026-08-16-kc2-pm4-lap-ab-march-dispersion"
OUT = NOTES / "2026-08-16-kc2-pm4-lap-ac-referent-residence"
SCRIPTS = META / "agentic_orchestration" / "research" / "scripts"

VIDEO = pathlib.Path(
    "/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/"
    "eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"
)

PREREG = OUT / "prereg.md"
#: the pre-registration, committed ALONE at 38fb3120 BEFORE this file existed.
PREREG_SHA = "da1fae161096b6299b56c784394d5967910aa4a0862e9825a303bb762e466bc5"

# ══════════════════════════════════════════════════════════════════════════════════════════════
# PINNED INPUTS — prereg § 1.  Re-hashed at run time; ANY mismatch is a HALT, never a warning.
# ══════════════════════════════════════════════════════════════════════════════════════════════
PINNED: Dict[str, str] = {
    str(LAPR / "pm4r_contact_occupancy.csv"):
        "913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6",
    str(LAPR / "method" / "plates60_lapH2.npy"):
        "28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df",
    str(SCRIPTS / "pm4r_contact_2026_08_14.py"):
        "8994b96a8da280e031fd6d795e8db7b5894910c4b8a233b4b064e1010068f2a7",
    str(SCRIPTS / "pm4r_lib_2026_08_14.py"):
        "630bede0bbc10389dca79d04601d319d37a02f266d406c0aad837480b110762b",
    str(LAPH2 / "method" / "bars.py"):
        "2ecfc75543d9498aa81f8d7b733d5f7eca2b7009a2ca7bbd834dffd10258e7e0",
    str(LAPH2 / "method" / "extract.py"):
        "36f7f923501a7ddd4dccfad7e8fd2e688f8ee53e0647989a68e67ba6dea6b36d",
    str(LAPH2 / "method" / "d1b.py"):
        "c26388071e127a0fb8e8420bb4ae151a6a678d444848c67d84cbd445034b876f",
    str(LAPH2 / "method" / "d1run.py"):
        "2cebdc5df62979d0d7d208c1aaf7274c02ff2540ea8e7b44efcff9f61dbdf8c5",
    str(LAPH2 / "method" / "d1final.py"):
        "d9e296eee4e4324b210332b76fe978cf36f5ccc5e657f0ade327e1f940078519",
    str(LAPH2 / "method" / "d2.py"):
        "0366a39faf9586b11278118ba19c50e7d89c2bd49b03643b21ec6ef8a0fc0cd2",
    str(LAPH2 / "method" / "camera_translation_60fps_683-866.npy"):
        "029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33",
    str(LAPH2 / "pm4h2_tracks.csv"):
        "13bb3033cb35012846343dcb077902304eb163a92cb8f7423ba8cf8074563818",
    str(LAPH2 / "pm4h2_ring_density.csv"):
        "a675367c9f46cedcb3413b3c43dfa0ac2aa0591c8ae120dcef05ce9a2f903eb5",
    str(LAPAB / "pm4ab_findings.md"):
        "a0279b1122c4de476e540a0bc34425c68e519a16d667a06abc2964a1675f07ba",
    str(VIDEO):
        "4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8",
}

# ══════════════════════════════════════════════════════════════════════════════════════════════
# CONSTANTS — prereg § 2.  Every one imported by identity from a pinned artifact.
# ══════════════════════════════════════════════════════════════════════════════════════════════
#: pm4r_lib_2026_08_14.py:60 (Lap H-2 OBS-H2-8 ground-plane compression)
K_GROUND = 0.537
#: d1b.py:26
FPS = 60.0
DT = 1.0 / FPS
#: pm4r_lib_2026_08_14.py:55
FIGHT_T0, FIGHT_T1 = 683.0, 864.0
#: pm4r_lib_2026_08_14.py:48-51 (Lap H-2 OBS-H2-6, +-0.25 s)
WAVE_START = {
    151: 683.0, 152: 698.6, 153: 714.9, 154: 729.8, 155: 744.0,
    156: 760.2, 157: 780.4, 158: 799.7, 159: 812.7, 160: 839.0,
}
WAVE_END = {w: (WAVE_START[w + 1] if w < 160 else FIGHT_T1) for w in WAVE_START}

#: pm4r_contact_2026_08_14.py:51 — the player-plate gate, verbatim in form.
PLAYER_GATE_X, PLAYER_GATE_XTOL = 960.0, 50.0
PLAYER_GATE_Y, PLAYER_GATE_YTOL = 429.0, 16.0

#: pm4r_contact_2026_08_14.py:112 / :136 — the dry-run / interval gap-join rule.
GAP_JOIN_S = 0.05

#: prereg § 2.1 — the pinned 2.400 m bracket, THREE RUNGS, never a scalar.
#: Values are the `R_gpx` column of pm4r_contact_occupancy.csv rows `at_sim_D_ENGAGE_M_2.400`.
RING_RUNGS = (285.7, 293.6, 300.0)
RING_PRIMARY = 293.6                 # the MIDDLE rung; declared before measurement
#: prereg § 2.1 — a DIFFERENT ring, reported separately and NEVER pooled with the bracket.
R_CONTACT_VISUAL = 150.0             # d1run.py:R_CONTACT (Lap H-2 visual melee-abutment radius)

#: prereg § 3.3 — the green-plate census sampling grid.
GREEN_SAMPLE_FPS = 2.0
#: extract.py:pbar — the player-plate x gate that this census REMOVES in order to see past it.
PLAYER_XLEFT_LO, PLAYER_XLEFT_HI = 890, 960
#: F-AC-3 non-emptiness clause.
GREEN_MIN_PLAYER_DETECT_FRAC = 0.50

#: prereg § 3.4 — emplacement-signature thresholds (CORROBORATIVE leg, never dispositive).
STATIONARY_NET_GPX = 40.0
STATIONARY_MIN_S = 8.0

#: prereg § 5.1 — death-discriminator bounds.
EDGE_MARGIN_PX = 120.0
REDETECT_WINDOW_S = 1.0
REDETECT_ABORT_FRAC = 0.35

#: prereg § 6 — criteria.
F_AC_1_TOL = 0.05
F_AC_1_MIN_OBS = 10000
F_AC_1_MIN_INTERVALS = 50
F_AC_2_MIN_DECIDABLE = 30
F_AC_2_SHARE_PASS = 0.20

#: prereg § 5.2 — player-speed context window at exits.
EXIT_SPEED_HALFWIN_S = 0.125
#: pm4r_lib_2026_08_14.py:64 — imported by identity.
SMOOTH_FRAMES = 9


# ══════════════════════════════════════════════════════════════════════════════════════════════
def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pinned(skip_video: bool = False) -> List[str]:
    """Re-hash every pinned input.  Raises on ANY mismatch (GL-6 / HALT-on-mismatch)."""
    lines = []
    for path, want in sorted(PINNED.items()):
        if skip_video and path == str(VIDEO):
            lines.append(f"  SKIP   (declared) {pathlib.Path(path).name}")
            continue
        got = sha256(path)
        if got != want:
            raise SystemExit(f"HALT (pinned-input mismatch): {path}\n  want {want}\n  got  {got}")
        lines.append(f"  EXACT  {got}  {pathlib.Path(path).name}")
    return lines


def verify_prereg(expect: str) -> str:
    got = sha256(PREREG)
    if got != expect:
        raise SystemExit(f"HALT (prereg digest): want {expect} got {got}")
    return got


def wave_of(t: float):
    for w in sorted(WAVE_START, reverse=True):
        if t >= WAVE_START[w]:
            return w
    return None


def ground_dist(ax, ay, bx, by) -> float:
    """The ring metric, verbatim in form from pm4r_contact_2026_08_14.py:74-75."""
    return float(np.hypot(ax - bx, (ay - by) / K_GROUND))


def dump_csv(path: pathlib.Path, rows: Sequence[dict], cols: Sequence[str]) -> Tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return sha256(path), len(rows)


def quantiles(xs) -> dict:
    if len(xs) == 0:
        return dict(n=0)
    a = np.asarray(xs, dtype=float)
    return dict(
        n=int(a.size),
        mean=round(float(a.mean()), 5),
        p05=round(float(np.percentile(a, 5)), 5),
        p25=round(float(np.percentile(a, 25)), 5),
        median=round(float(np.median(a)), 5),
        p75=round(float(np.percentile(a, 75)), 5),
        p90=round(float(np.percentile(a, 90)), 5),
        p95=round(float(np.percentile(a, 95)), 5),
        max=round(float(a.max()), 5),
        total=round(float(a.sum()), 5),
        resolution_s=round(DT, 6),
        resolution_note="every duration is +-1 frame = +-0.016667 s at 60 fps",
    )


def load_plates():
    """The pinned Lap H-2 nameplate census.  Columns: t, kind(0=M,1=P), x_anchor, y_bar, w, txt."""
    return np.load(LAPR / "method" / "plates60_lapH2.npy")


def load_camera():
    """The pinned Lap H-2 camera-translation trace.  Columns: t, dx, dy, peak."""
    return np.load(LAPH2 / "method" / "camera_translation_60fps_683-866.npy")


def player_plates(R: np.ndarray) -> Dict[float, Tuple[float, float]]:
    """pm4r_contact_2026_08_14.py:50-52, verbatim in form."""
    P = {}
    for r in R[R[:, 1] == 1]:
        if (abs(r[2] - PLAYER_GATE_X) < PLAYER_GATE_XTOL
                and abs(r[3] - PLAYER_GATE_Y) < PLAYER_GATE_YTOL):
            P[round(r[0], 4)] = (float(r[2]), float(r[3]))
    return P


def import_h2_tracker():
    """Import Lap H-2's tracker BY IDENTITY.  `d1b.load()` (which reads /tmp) is never called."""
    sys.path.insert(0, str(LAPH2 / "method"))
    import d1b                                                            # noqa: E402
    return d1b


def import_h2_bars():
    """Import Lap H-2's plate detector BY IDENTITY."""
    sys.path.insert(0, str(LAPH2 / "method"))
    import bars                                                           # noqa: E402
    return bars
