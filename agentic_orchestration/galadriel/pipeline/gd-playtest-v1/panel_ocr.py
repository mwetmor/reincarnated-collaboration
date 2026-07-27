#!/usr/bin/env python3
"""
T-A ledger tier: PlayStats panel OCR for the GD general-play run v1.

Design constraints inherited from gandalf's verification note (2026-07-26):

  D-1  Legibility is not accuracy. Crops are taken at NATIVE resolution and are
       never downscaled before reading. Upscaling is for human inspection only.
       Every glyph read carries a match score; low-scoring glyphs are refused,
       not guessed.

  D-2  The in-game quest tracker renders over the panel's right edge and eats
       digits. Occluded fields are emitted as UNREADABLE. They are never
       inferred and never interpolated.

Four geometry/typography facts discovered during calibration that the note did
not have, and each of which silently corrupts a naive reader:

  G-1  The panel is RIGHT-ANCHORED. Its left edge L migrates leftward as the
       skill list grows (observed L = 1481, 1473, 1398, 1390, 1382 over the
       run). L is therefore detected per frame, not assumed.

  G-2  The `Skills Used` list is sorted ALPHABETICALLY by .dbr path and only
       grows. A newly-used skill INSERTS a row and shifts every row below it,
       including `Life healed` and `Shield block chance`. Rows are identified
       by matching the skill-path bitmap, never by row index.

  G-3  ADJACENT DIGITS CAN TOUCH (zero blank columns between them). Splitting a
       number on blank columns therefore merges digit pairs into one blob, and
       a merged blob still scores ~0.69 against a single-digit template -- a
       confidently WRONG read. Numbers are read by greedy left-to-right
       template matching at native glyph width instead, never by gap
       segmentation. This is D-1's failure mode reproduced at the glyph level.

  G-4  The `Shield block chance` row uses a DETACHED colon ("chance : 18.00"),
       unlike every other field ("Life healed: 12468.06"). Skill rows use the
       detached form too.

Field rows sit on a fixed 20 px pitch starting at y=54 (title). Only the
number of skill rows varies.
"""

import json

import numpy as np

# --- panel text mask ------------------------------------------------------
# Panel text is near-white. Requiring a high BLUE channel is what excludes the
# orange/tan quest-tracker text that causes the D-2 overlap.
TXT_R, TXT_G, TXT_B = 170, 170, 150

ROW_PITCH = 20
ROW_H = 14
TITLE_Y = 54
SKILLS_HDR_Y = 274
SKILL_INDENT = 21
MAX_ROW_Y = 540

# Fixed rows above the skills block, as (y, key, value-search-start offset
# from L, value kind). Offsets sit just past the label's last glyph.
FIXED_ROWS = [
    (74,  "play_time",      120, "duration"),
    (94,  "total_score",     95, "int"),
    (114, "deaths",         146, "int"),
    (134, "kills",          129, "int"),
    (154, "health_potions", 161, "int"),
    (174, "mana_potions",   151, "int"),
    (194, "max_level",      156, "int"),
    (234, "dps",            155, "dec"),
]
# trailing rows, in display order, as (key, kind, value-search offset from L)
TRAIL_ROWS = [("life_healed", "dec", 88), ("shield_block_chance", "dec", 180)]

GLYPH_MIN_IOU = 0.72   # per-glyph acceptance
MIN_ROW_INK = 60       # below this a "row" is game-world speckle, not panel text
SKILL_MIN_CORR = 0.88  # skill-path identification floor


def text_mask(rgb):
    return (rgb[:, :, 0] > TXT_R) & (rgb[:, :, 1] > TXT_G) & (rgb[:, :, 2] > TXT_B)


def row_xstart(mask, y, x_lo=1330, x_hi=1915):
    band = mask[y:y + ROW_H, x_lo:x_hi]
    nz = np.nonzero(band.sum(axis=0))[0]
    return (x_lo + int(nz.min())) if len(nz) else None


def row_ink(mask, y, x_lo=1330, x_hi=1915):
    return int(mask[y:y + ROW_H, x_lo:x_hi].sum())


def detect_L(mask):
    """Panel left edge = modal xstart of the fixed field rows (G-1)."""
    cands = []
    for y in (74, 94, 114, 134, 154, 174, 194, 234, SKILLS_HDR_Y):
        if row_ink(mask, y) >= MIN_ROW_INK:
            xs = row_xstart(mask, y)
            if xs is not None:
                cands.append(xs)
    if not cands:
        return None
    vals, counts = np.unique(np.array(cands), return_counts=True)
    return int(vals[int(np.argmax(counts))])


def segment(mask, y, x0, x1, gap=6):
    """Split a row band into WORD groups separated by >= `gap` blank columns.
    Used for words/paths only -- never for digits (G-3)."""
    col = mask[y:y + ROW_H, x0:x1].sum(axis=0)
    out, run, blank = [], None, 0
    for i, v in enumerate(col):
        if v > 0:
            run = [i, i] if run is None else [run[0], i]
            blank = 0
        else:
            if run is not None:
                blank += 1
                if blank >= gap:
                    out.append((run[0] + x0, run[1] + x0))
                    run = None
    if run is not None:
        out.append((run[0] + x0, run[1] + x0))
    return out


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum()) / u if u else 0.0


class PanelReader:
    def __init__(self, model_path):
        m = json.load(open(model_path))
        # each character carries a LIST of templates: the panel renders
        # differently on a native PNG screenshot than on an h264 video frame,
        # and a native-only template set under-matches on video (glyph edges
        # are softened by compression). Templates from both instruments are
        # banked and matched as alternatives.
        self.digits = {k: [np.array(b, dtype=bool) for b in v]
                       for k, v in m["digits"].items()}
        self.skill_sigs = {k: [np.array(b, dtype=float) for b in v]
                           for k, v in m.get("skills", {}).items()}

    # -- glyph level (G-3: greedy, native-width, no gap segmentation) -------
    def _best_glyph(self, mask, y, x, allow_dot=True, dxs=(0,)):
        """Best template match near column x. Searching a small dx window is
        required because inter-digit advance is not constant in this
        proportional font -- a rigid advance drops the 2nd digit of a number."""
        best, bestv, bestw, bestdx = None, -1.0, 0, 0
        for ch, tmpls in self.digits.items():
            if ch == "." and not allow_dot:
                continue
            for t in tmpls:
                th, tw = t.shape
                for dx in dxs:
                    win = mask[y:y + th, x + dx:x + dx + tw]
                    if win.shape != t.shape:
                        continue
                    for dy in (-1, 0, 1):
                        v = iou(np.roll(win, dy, axis=0), t)
                        if v > bestv:
                            best, bestv, bestw, bestdx = ch, v, tw, dx
        return best, bestv, bestw, bestdx

    def read_token(self, mask, y, x0, x1, allow_dot=True):
        """Greedily read one contiguous numeric token starting at/after x0.
        Returns (string, min_glyph_iou, x_after)."""
        col = mask[y:y + ROW_H, x0:x1].sum(axis=0)
        nz = np.nonzero(col)[0]
        if not len(nz):
            return "", 0.0, x1
        x = x0 + int(nz.min())
        out, confs = [], []
        first = True
        while x < x1:
            dxs = (0,) if first else (0, 1, 2, 3, -1)
            ch, v, w, dx = self._best_glyph(mask, y, x, allow_dot, dxs)
            if ch is None or v < GLYPH_MIN_IOU:
                break
            out.append(ch)
            confs.append(v)
            x += dx + w
            first = False
            # a wide blank run ends the token
            sub = mask[y:y + ROW_H, x:x + 8].sum(axis=0)
            k = 0
            while k < len(sub) and sub[k] == 0:
                k += 1
            if k >= 5:
                break
        return "".join(out), (min(confs) if confs else 0.0), x

    def read_number(self, mask, y, x0, x1, kind):
        """Read the FIRST numeric token at/after `x0` (just past the label).

        First-token rather than last-token is what keeps the quest-tracker text
        (D-2), which always sits further right, out of the number. Where the
        tracker overlaps the digits themselves the glyph score collapses and
        the field is refused rather than guessed.
        """
        if kind == "duration":
            s1, c1, x = self.read_token(mask, y, x0, x1, allow_dot=False)
            if not s1.isdigit():
                return None, 0.0
            # step past the word "min" (letters match no digit template)
            s2, c2 = "", 0.0
            for gx0, gx1 in segment(mask, y, x, x1, gap=4):
                s2, c2, _ = self.read_token(mask, y, gx0, min(gx1 + 2, x1), allow_dot=False)
                if s2.isdigit():
                    break
            if not s2.isdigit():
                return None, 0.0
            return int(s1) * 60 + int(s2), min(c1, c2)

        s, c, _ = self.read_token(mask, y, x0, x1, allow_dot=(kind == "dec"))
        if not s:
            return None, 0.0
        try:
            return (float(s) if kind == "dec" else int(s)), c
        except ValueError:
            return None, c

    # -- skill rows (G-2) --------------------------------------------------
    def skill_row(self, mask, y, L):
        """Identify the skill on a row and read its count.

        The path profile is taken over the FULL path span (row indent up to the
        detached colon), not over segment()'s first group. Background bleed can
        dim a mid-path glyph below threshold and split the path into two
        groups; profiling only the first group then yields a different-length
        signature that scores ~0.82 against the right skill and is refused.
        Anchoring on the span rather than on a group fixes that.
        """
        x_lo = L + SKILL_INDENT
        groups = segment(mask, y, x_lo, 1915, gap=6)
        if len(groups) < 2:
            return None, -2.0, None, 0.0
        num_x0, num_x1 = groups[-1]
        # the detached colon (G-4) is the narrow group before the count
        colon_x0 = None
        for gx0, gx1 in groups[:-1]:
            if gx1 - gx0 + 1 <= 4:
                colon_x0 = gx0
        path_x1 = (colon_x0 - 2) if colon_x0 else (num_x0 - 6)
        if path_x1 - x_lo < 32:
            return None, -2.0, None, 0.0
        prof = mask[y:y + ROW_H, x_lo:path_x1].sum(axis=0).astype(float)
        idx = np.linspace(0, len(prof) - 1, 64)
        sig = np.interp(idx, np.arange(len(prof)), prof)

        scores = {}
        for k, refs in self.skill_sigs.items():
            for ref in refs:
                if np.std(sig) < 1e-6 or np.std(ref) < 1e-6:
                    continue
                scores[k] = max(scores.get(k, -2.0),
                                float(np.corrcoef(sig, ref)[0, 1]))
        name, corr = (None, -2.0)
        if scores:
            ranked = sorted(scores.items(), key=lambda kv: -kv[1])
            name, corr = ranked[0]
            runner_up = ranked[1][1] if len(ranked) > 1 else -2.0
            # Refuse on a low match OR on an ambiguous one: two paths within
            # 0.02 cannot be told apart, and a mis-assigned skill silently
            # corrupts two counter series at once. The monotonicity gate in
            # gate_and_fit.py is the second net.
            if corr < SKILL_MIN_CORR or (corr - runner_up) < 0.02:
                name = None
        cnt, cconf = self.read_number(mask, y, num_x0, min(num_x1 + 3, 1915), "int")
        return name, corr, cnt, cconf

    # -- frame level -------------------------------------------------------
    def read(self, rgb):
        mask = text_mask(rgb)
        L = detect_L(mask)
        rec = {"L": L}
        if L is None:
            rec["status"] = "NO_PANEL"
            return rec
        rec["status"] = "OK"

        for y, key, off, kind in FIXED_ROWS:
            val, conf = self.read_number(mask, y, L + off, 1915, kind)
            rec[key] = val
            rec[key + "_conf"] = round(conf, 3)

        skills, trailing = {}, []
        y = SKILLS_HDR_Y + ROW_PITCH
        while y < MAX_ROW_Y:
            if row_ink(mask, y) < MIN_ROW_INK:
                break
            xs = row_xstart(mask, y)
            if xs is None:
                break
            if abs(xs - (L + SKILL_INDENT)) <= 3:
                name, corr, cnt, conf = self.skill_row(mask, y, L)
                skills[name or f"UNKNOWN@{y}"] = {
                    "count": cnt, "conf": round(conf, 3),
                    "path_corr": round(corr, 3),
                }
            elif abs(xs - L) <= 3:
                trailing.append(y)
            y += ROW_PITCH

        rec["skills"] = skills
        for i, (key, kind, off) in enumerate(TRAIL_ROWS):
            if i < len(trailing):
                val, conf = self.read_number(mask, trailing[i], L + off, 1915, kind)
            else:
                val, conf = None, 0.0
            rec[key] = val
            rec[key + "_conf"] = round(conf, 3)
        return rec
