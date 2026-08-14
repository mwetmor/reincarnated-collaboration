#!/usr/bin/env python3
"""KC2-PM4 Lap R shared library — THE LOCOMOTION-AND-CONTACT DECODE.

READ-ONLY on every external source (referent MP4, vendor `.arz` corpus).
OUTCOME-FIREWALLED: no simulation output file is opened by this module.

Every threshold used here is pre-registered in
`agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-r-locomotion-contact/PREREGISTRATION.md`
sha256 dc49d0ba8f176ab1d4814d522e5183867fe2ad56334ed7251e81b3db124cec10
(written and hashed 2026-08-14T13:43:46Z, BEFORE any instrument ran on the full video).

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap R.
"""
from __future__ import annotations

import csv
import hashlib
import pathlib
import re
import subprocess
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
NOTES = META / "agentic_orchestration" / "legolas" / "notes"
LAPN = NOTES / "2026-08-14-kc2-pm4-lap-n-crit-and-collision"
LAPH2 = NOTES / "2026-08-13-kc2-pm4-lap-h2-video-match"
OUT = NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact"

VIDEO = pathlib.Path(
    "/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/"
    "eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"
)

# ══════════════════════════════════════════════════════════════════════════════════════════════
# PRE-REGISTERED CONSTANTS  (PREREGISTRATION.md — no value below was chosen after seeing a result)
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: PREREG § A.1 clause 3 — a screen element present in >= this fraction of frames is not FCT.
STATIC_ELEMENT_FRAC = 0.50

#: PREREG § A.3 — measured FCT on-screen lifetime (Lap N, tracked across a 10 fps burst t=749..753).
FCT_LIFETIME_S = 1.35
FCT_LIFETIME_BAND = (1.2, 1.5)

#: PREREG § A.4 — the six sweep rungs.  FIXED.  None added, removed or re-cut after the numbers.
SWEEP_RUNGS_S = (0.5, 1.0, 2.0, 3.0, 5.0, 10.0)

#: PREREG § A.5 — wave-increment times, Lap H-2 OBS-H2-6, measured +-0.25 s from the wave-counter
#: digit crop 52x26 at (1582,138) by 4 fps frame-difference.  151 starts at the run start.
WAVE_START = {
    151: 683.0, 152: 698.6, 153: 714.9, 154: 729.8, 155: 744.0,
    156: 760.2, 157: 780.4, 158: 799.7, 159: 812.7, 160: 839.0,
}
#: Lap H-2 pm4h2_movement_cadence.csv closes wave 160 (and the fight) at 864.0.
FIGHT_T0, FIGHT_T1 = 683.0, 864.0
WAVE_END = {w: (WAVE_START[w + 1] if w < 160 else FIGHT_T1) for w in WAVE_START}

#: PREREG § B.1 — Lap H-2 OBS-H2-8 isometric ground-plane compression (player ground decal 80x43 px).
K_GROUND = 0.537
#: PREREG § B.1 — Lap H-2 OBS-H2-7: the player's ground point is pinned at screen (958, 544).
PLAYER_SCREEN = (958.0, 544.0)

#: PREREG § B.1 — Schmitt trigger on smoothed ground speed.
V_ON_PRIMARY = 200.0        # ground px/s  (Lap H-2's middle published rung, adopted unchanged)
V_ON_SENSITIVITY = (100.0, 200.0, 400.0)
V_OFF_RATIO = 0.5           # V_OFF = V_ON / 2  (standard hysteresis convention)
SMOOTH_FRAMES = 9           # 0.15 s centred rolling median
MIN_EPISODE_S = 0.25
MIN_GAP_MERGE_S = 0.15

#: PREREG § B.2 — validation draw.
VALIDATION_SEED = 154
VALIDATION_N_PER_CLASS = 10
VALIDATION_DT_S = 0.25
VALIDATION_CLASS_CUT_GPX = 50.0     # over 0.25 s == 200 gpx/s == V_ON_PRIMARY
VALIDATION_PASS_AGREE = 16          # of 20
VALIDATION_PASS_MEDIAN_RELERR = 0.25

#: PREREG § B.3 — channel-persistence probe.
CHANNEL_N_EPISODES = 12
CHANNEL_SAMPLE_FPS = 10.0
RING_ANNULUS_PX = (60, 110)
RING_CONTROL_ANNULUS_PX = (300, 350)
CHANNEL_CONTINUES_FRAC = 0.50
CHANNEL_INTERRUPTED_RATIO = 0.20

#: PREREG § B.4 — Lap H-2 D2 contact radius, calibrated there by visual inspection on frames
#: 783.000 / 824.400.  150 primary; 120 / 180 reported as sensitivity.
R_CONTACT_GPX = 150.0
R_CONTACT_SENSITIVITY = (120.0, 150.0, 180.0)

# ══════════════════════════════════════════════════════════════════════════════════════════════
# Pinned inputs — every one re-hashed at run time; a mismatch is a HALT, never a warning
# ══════════════════════════════════════════════════════════════════════════════════════════════
PINNED_INPUTS = {
    str(LAPN / "pm4n_fct_events.csv"):
        "cf8ed21815339bd62813237c73363e06db86b1758a725ff32567212ed0424ce2",
    str(LAPN / "method" / "build.py"):
        "1d8032185626bd74ca7458b60f837b7beb106527a19cea3194387a71691bab9a",
    str(LAPN / "method" / "ocr.swift"):
        "1a96036ddbdfe4d55e2be31f534e9a9661db152dc71d4c36e18c684ab8b94ec1",
    str(LAPH2 / "method" / "camera_translation_60fps_683-866.npy"):
        "029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33",
    str(LAPH2 / "method" / "player_hp_frac_60fps.npy"):
        "692cd4115f93e7761e2ffe10089426ce096cc4abb263ce201b8ffec578c370aa",
}


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pinned() -> List[str]:
    """Re-hash every pinned input.  Returns report lines; raises on ANY mismatch (GL-6)."""
    lines = []
    for path, want in PINNED_INPUTS.items():
        got = sha256(path)
        ok = got == want
        lines.append(f"  {'EXACT' if ok else 'MISMATCH'}  {got}  {pathlib.Path(path).name}")
        if not ok:
            raise SystemExit(f"HALT (GL-6): {path}\n  want {want}\n  got  {got}")
    return lines


def wave_of(t: float) -> Optional[int]:
    for w in sorted(WAVE_START, reverse=True):
        if t >= WAVE_START[w]:
            return w if t <= FIGHT_T1 else None
    return None


# ══════════════════════════════════════════════════════════════════════════════════════════════
# LIMB A — the FCT observation classifier + gap machinery
# ══════════════════════════════════════════════════════════════════════════════════════════════
CRIT = re.compile(r'^(\d[\d,]{0,9})\s*\(x(\d\.\d{2})\)$')
BARE = re.compile(r'^(\d[\d,]{0,9})$')
MULT_ANY = re.compile(r'\(?x(\d)[.,](\d{2})\)?')
HEALTH = re.compile(r'^\(?[\d,]+\s*/\s*[\d,]+\)?$')

#: Lap N method/build.py HUD_BOXES — imported UNCHANGED (fixed-position screen furniture).
HUD_BOXES = [(0.715, 0.885), (0.822, 0.846), (0.486, 0.053),
             (0.297, 0.050), (0.645, 0.046), (0.700, 0.960)]


def is_hud(bx: float, by: float) -> bool:
    return any(abs(bx - hx) < 0.02 and abs(by - hy) < 0.02 for hx, hy in HUD_BOXES)


def classify(text: str, bx: float, by: float) -> str:
    """Lap N's classifier, character-for-character the same decision tree."""
    if HEALTH.match(text):
        return "health_readout"
    if is_hud(bx, by):
        return "hud"
    if CRIT.match(text):
        return "crit"
    if BARE.match(text):
        return "bare"
    if MULT_ANY.search(text):
        return "crit_garbled"
    return "other"


def colour_class(r: float, g: float) -> str:
    rg = r / max(g, 1.0)
    return "red_taken" if rg >= 1.6 else "cream_dealt" if 1.02 <= rg < 1.6 else "neutral"


def parse_damage(text: str) -> Optional[int]:
    m = CRIT.match(text)
    if m:
        return int(m.group(1).replace(",", ""))
    m = BARE.match(text)
    if m:
        return int(m.group(1).replace(",", ""))
    m = re.match(r'^(\d[\d,]{0,9})', text)
    return int(m.group(1).replace(",", "")) if m else None


def static_positions(obs: Sequence[dict], n_frames: int) -> set:
    """PREREG § A.1 clause 3 — positions recurring in >= STATIC_ELEMENT_FRAC of frames."""
    from collections import defaultdict
    seen = defaultdict(set)
    for o in obs:
        seen[(round(o["bbox_x"], 2), round(o["bbox_y"], 2))].add(o["frame"])
    return {k for k, v in seen.items() if len(v) >= STATIC_ELEMENT_FRAC * n_frames}


def p_out(obs: Sequence[dict], n_frames: int) -> Tuple[List[dict], set]:
    """PREREG § A.1 — the player-outgoing predicate, applied unchanged."""
    static = static_positions(obs, n_frames)
    keep = []
    for o in obs:
        if (round(o["bbox_x"], 2), round(o["bbox_y"], 2)) in static:
            continue
        cls, col = o["cls"], o["colour_class"]
        if not (cls in ("crit", "crit_garbled") or (cls == "bare" and col == "cream_dealt")):
            continue
        d = o.get("damage")
        if d is None or d == "" or int(d) < 1:
            continue
        keep.append(o)
    return keep, static


def gap_runs(sample_times: Sequence[float], dry_flag: Sequence[bool],
             cadence: float) -> List[Tuple[float, float, int]]:
    """Contiguous runs of DRY samples -> (t_first_dry, t_last_dry, n_samples)."""
    runs, i, n = [], 0, len(sample_times)
    while i < n:
        if not dry_flag[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and dry_flag[j + 1] and \
                abs(sample_times[j + 1] - sample_times[j] - cadence) < cadence * 0.51:
            j += 1
        runs.append((sample_times[i], sample_times[j], j - i + 1))
        i = j + 1
    return runs


def sweep(gaps_s: Sequence[float], total_s: float) -> Dict[float, dict]:
    """PREREG § A.4 — fraction of fight time inside gaps longer than each fixed rung."""
    out = {}
    a = np.asarray(gaps_s, dtype=float)
    for r in SWEEP_RUNGS_S:
        sel = a[a > r]
        out[r] = dict(n_gaps=int(sel.size),
                      time_in_gaps_s=round(float(sel.sum()), 4),
                      frac_of_fight=round(float(sel.sum() / total_s), 6) if total_s else None)
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# LIMB B — locomotion
# ══════════════════════════════════════════════════════════════════════════════════════════════
def ground_speed(cam: np.ndarray, fps: float = 60.0) -> Tuple[np.ndarray, np.ndarray]:
    """(t, speed in ground px/s) from the Lap H-2 camera-translation trace."""
    t = cam[:, 0]
    v = np.hypot(cam[:, 1], cam[:, 2] / K_GROUND) * fps
    return t, v


def rolling_median(x: np.ndarray, w: int) -> np.ndarray:
    if w <= 1:
        return x.copy()
    half = w // 2
    pad = np.pad(x, (half, half), mode="edge")
    return np.median(np.lib.stride_tricks.sliding_window_view(pad, w), axis=-1)


def episodes(t: np.ndarray, v: np.ndarray, v_on: float) -> List[Tuple[float, float]]:
    """PREREG § B.1 — Schmitt trigger + min-gap merge + min-duration reject."""
    v_off = v_on * V_OFF_RATIO
    on, spans, start = False, [], None
    for i in range(len(t)):
        if not on and v[i] >= v_on:
            on, start = True, t[i]
        elif on and v[i] < v_off:
            on = False
            spans.append((start, t[i]))
    if on:
        spans.append((start, t[-1]))
    merged = []
    for s in spans:
        if merged and s[0] - merged[-1][1] < MIN_GAP_MERGE_S:
            merged[-1] = (merged[-1][0], s[1])
        else:
            merged.append(list(s) if False else (s[0], s[1]))
            merged[-1] = (s[0], s[1])
    fixed = []
    for s in merged:
        if fixed and s[0] - fixed[-1][1] < MIN_GAP_MERGE_S:
            fixed[-1] = (fixed[-1][0], s[1])
        else:
            fixed.append((s[0], s[1]))
    return [s for s in fixed if s[1] - s[0] >= MIN_EPISODE_S]


def frames_at(times: Sequence[float], outdir: pathlib.Path, tag: str) -> List[pathlib.Path]:
    """Extract single frames at arbitrary timestamps (read-only on the MP4)."""
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, t in enumerate(times):
        p = outdir / f"{tag}_{i:04d}_{t:.3f}.png"
        if not p.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", str(VIDEO),
                            "-frames:v", "1", "-y", str(p)], check=True)
        paths.append(p)
    return paths


def ncc_shift(a: np.ndarray, b: np.ndarray, patch: Tuple[int, int, int, int],
              search: int = 200) -> Tuple[float, float, float]:
    """Normalised cross-correlation template match — the INDEPENDENT second instrument
    (raw-luminance template match; a different principle from the trace's FFT phase
    correlation on gradient magnitude).  Returns (dx, dy, peak_ncc)."""
    x, y, w, h = patch
    tpl = a[y:y + h, x:x + w].astype(np.float64)
    tpl = tpl - tpl.mean()
    tn = np.sqrt((tpl ** 2).sum())
    if tn < 1e-9:
        return (0.0, 0.0, 0.0)
    best = (0.0, 0.0, -2.0)
    H, W = b.shape
    for dy in range(-search, search + 1, 2):
        yy = y + dy
        if yy < 0 or yy + h > H:
            continue
        for dx in range(-search, search + 1, 2):
            xx = x + dx
            if xx < 0 or xx + w > W:
                continue
            win = b[yy:yy + h, xx:xx + w].astype(np.float64)
            win = win - win.mean()
            wn = np.sqrt((win ** 2).sum())
            if wn < 1e-9:
                continue
            c = float((tpl * win).sum() / (tn * wn))
            if c > best[2]:
                best = (float(dx), float(dy), c)
    return best


def dump_csv(path: pathlib.Path, rows: Sequence[dict], cols: Sequence[str]) -> Tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return sha256(path), len(rows)
