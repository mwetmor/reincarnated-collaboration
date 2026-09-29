#!/usr/bin/env python3
"""KC2-PLAY SEAL LAP · THE FULL ENERGY RE-READ — the work T30 was blocking.

On 2026-09-21 the energy globe was re-read with the HP globe's reader on the
SIXTEEN committed frames, and the note said, in one line, what it could not do:

    "The per-frame crops were never committed and the full re-read needs the
     MP4: T30."   (notes/2026-09-21-kc2-play-energy-globe-reread.md § 0)

T30 is now DONE.  `/Volumes/reincarnated` is mounted and the referent MP4's
identity is verified against legolas Lap Q's pinned sha256.  So this module is
the deferred half: the STRONG reader (Apple Vision, `ocr_vision.swift`, the
pinned byte-identical reader that produced the 100.00 %-accepted HP trace)
pointed at EVERY frame of the combat window, not at the sixteen that survived.

WHAT IT SETTLES THAT THE SIXTEEN COULD NOT
------------------------------------------
The 2026-09-21 lap ended holding one thing open, and said so:

    "with one confirmed above-ceiling frame I cannot apportion the other 1,186."

The atlas trace carries a large above-ceiling population.  ONE of those frames
(t = 735.0, displaying 1610) is confirmed by three independent readings.  The
rest were unapportionable because the only reader that had seen them was the
weak one.  A full strong-reader pass apportions them by measurement.

STAGES (each runs alone; each writes its own JSON; none silently transforms)
---------------------------------------------------------------------------
  identity    sha256 the MP4 on the mount; compare to the pin READ OUT OF
              legolas's `pm4q_digests.json` -- the digest is never retyped.
  control     the SIXTEEN hand-read timestamps, freshly extracted from the
              mounted file, under an UPSCALE SWEEP.  Picks the smallest scale
              that reproduces every hand read.  A positive control chosen
              BEFORE the population run, on labels fixed in August.
  population  every frame of D-COMBAT-182 at 60 Hz, same crop box, same window,
              same row grid as the committed atlas trace -> Vision -> trace.
  analyse     atlas vs Vision, frame by frame; the above-ceiling apportionment;
              the spend/spill decomposition re-derived on the strong reader.

DECLARED TRANSFORMATIONS (no silent manipulation)
-------------------------------------------------
  1. CROP.  `EBOX` is IMPORTED from `eor_channel.py`, not restated, so the
     re-read cannot drift from the box the atlas trace used.
  2. UPSCALE.  Vision needs more pixels than a 104x26 crop carries.  The factor
     is not chosen by taste: `control` sweeps it and the smallest factor that
     reproduces 16/16 hand reads is the one the population runs at.  The sweep
     table ships in the output whichever way it falls.
  3. NOTHING ELSE.  No denoise, no threshold, no contrast stretch.  Nearest-
     neighbour upscale only -- it invents no intensity.

Usage:
    python3 kc2_energy_fullreread.py identity   [out.json]
    python3 kc2_energy_fullreread.py control    [out.json]
    python3 kc2_energy_fullreread.py population [out.json]
    python3 kc2_energy_fullreread.py analyse    [out.json]

Read-only on the mount and on every committed input.  Writes only under
`agentic_orchestration/galadriel/` and the session scratchpad.
galadriel, 2026-09-28, Run KC2-PLAY seal lap, seat W1.
"""
import json, os, re, sys, hashlib, shutil, subprocess, tempfile, time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from eor_channel import EBOX                      # (1240, 1004, 104, 26)
from eor_release import clean, CEIL               # CEIL = 1594.0
from kc2_energy_shape import (AO, CHAN, ENER, F_E60, WINDOW, HZ, TICK_DE,
                              TICK_DT, D_COMBAT, sha256)

REPO = os.path.abspath(os.path.join(AO, "..", ".."))
MOUNT_MP4 = ("/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/"
             "video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4")
PIN_JSON = os.path.join(REPO, "agentic_orchestration/legolas/notes/"
                              "2026-08-14-kc2-pm4-lap-q-heal-discriminator/"
                              "pm4q_digests.json")
SWIFT_SRC = os.path.join(HERE, "ocr_vision.swift")
SCRATCH = os.environ.get("KC2_SCRATCH", "/private/tmp/kc2-energy-fullreread")
NOTES = os.path.join(AO, "notes")

DENOM = "2576"                     # the energy max, constant across the fight
SCALE_SWEEP = (1, 4, 6, 8, 12)     # nearest-neighbour upscale factors
BATCH = 400                        # image paths per Vision process invocation

# --- the SIXTEEN hand reads, carried verbatim from committed artifacts -------
# 10 from atlas-spec.json (the atlas's own TRAINING DATA, hand-typed 2026-08-25)
# 2 from MD-B4app-2b § 1.1 (exc_*.png filenames + the note's table)
# 4 from MD-B4app-2b § 1.3 (x7 blind-gap strip, hand-read across the largest gap)
HAND_BLIND = [(702.05, 1399), (702.60, 1430), (703.15, 1434), (703.70, 1417)]
HAND_EXC = [(688.18, 1497), (702.90, 1437)]


# ===========================================================================
#  small shared machinery
# ===========================================================================
def digest(path, bs=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bs)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def pinned_digest():
    """The Lap Q pin, READ from legolas's JSON. Never retyped."""
    d = json.load(open(PIN_JSON))["inputs"]["referent_video"]
    return d["sha256"], int(d["bytes"]), d["path"]


def hand_reads():
    spec = json.load(open(os.path.join(CHAN, "atlas-spec.json")))
    out = [(float(s["t"]), int(s["s"].split("/")[0]), "atlas-spec.json") for s in spec]
    out += [(t, v, "MD-B4app-2b 1.1 exc") for t, v in HAND_EXC]
    out += [(t, v, "MD-B4app-2b 1.3 blind strip") for t, v in HAND_BLIND]
    return sorted(out)


def build_ocr():
    if not shutil.which("swiftc") or not os.path.exists(SWIFT_SRC):
        return None, None
    d = tempfile.mkdtemp(prefix="kc2ocr_")
    exe = os.path.join(d, "ocr")
    r = subprocess.run(["swiftc", "-O", SWIFT_SRC, "-o", exe],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:])
        return None, None
    return exe, sha256(SWIFT_SRC)


def vision(exe, paths):
    """path -> [(text, conf)] from the pinned Apple Vision reader."""
    out = {}
    for i in range(0, len(paths), BATCH):
        chunk = list(paths[i:i + BATCH])
        r = subprocess.run([exe] + chunk, capture_output=True, text=True)
        for line in r.stdout.splitlines():
            f = line.split("\t")
            if len(f) < 7:
                continue
            out.setdefault(f[0], []).append((f[1], float(f[2])))
    return out


PAT = re.compile(r"(\d{3,4})\s*/\s*(\d{4})")


def parse_lines(cands):
    """PARSE POLICY, declared: a frame reads as `cur` iff some Vision line, or
    the frame's lines joined in emission order, matches NNN(N)/NNNN with the
    denominator EXACTLY 2576.  A wrong denominator is a PARSE FAILURE, not a
    silent acceptance -- the denominator is the reader's own error check and it
    is the only check available per frame.  Returns (cur, conf, raw) or Nones."""
    for s, c in cands:
        m = PAT.search(s.replace(" ", ""))
        if m and m.group(2) == DENOM:
            return int(m.group(1)), c, s
    joined = "".join(s.replace(" ", "") for s, _ in cands)
    m = PAT.search(joined)
    if m and m.group(2) == DENOM:
        return int(m.group(1)), min([c for _, c in cands] or [0.0]), joined
    return None, None, ("|".join(s for s, _ in cands) if cands else "")


def write_pngs(frames, outdir, scale, prefix="f"):
    """frames: iterable of (key, HxWx3 uint8). Nearest-neighbour upscale only."""
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for key, arr in frames:
        im = Image.fromarray(arr)
        if scale != 1:
            im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        p = os.path.join(outdir, f"{prefix}{key}.png")
        im.save(p)
        paths.append(p)
    return paths


def grab_single(video, t, box):
    """One frame at `t` by input-seek, cropped to `box`. Same form as
    eor_channel.grab_box, which produced the committed crops."""
    tmp = os.path.join(SCRATCH, "_one.png")
    os.makedirs(SCRATCH, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", video,
                    "-frames:v", "1", "-vf",
                    f"crop={box[2]}:{box[3]}:{box[0]}:{box[1]}", "-y", tmp],
                   check=True)
    a = np.array(Image.open(tmp).convert("RGB"))
    os.remove(tmp)
    return a


# ===========================================================================
#  STAGE identity
# ===========================================================================
def stage_identity(out):
    pin_sha, pin_bytes, pin_path = pinned_digest()
    st = os.stat(MOUNT_MP4)
    t0 = time.time()
    got = digest(MOUNT_MP4)
    res = {
        "stage": "identity",
        "path_on_mount": MOUNT_MP4,
        "path_in_pin": pin_path,
        "path_match": os.path.normpath(MOUNT_MP4) == os.path.normpath(pin_path),
        "bytes_derived": st.st_size,
        "bytes_pinned": pin_bytes,
        "bytes_match": st.st_size == pin_bytes,
        "sha256_derived": got,
        "sha256_pinned": pin_sha,
        "sha256_match": got == pin_sha,
        "pin_source": os.path.relpath(PIN_JSON, REPO),
        "pin_read_programmatically": True,
        "hash_seconds": round(time.time() - t0, 1),
        "verdict": "IDENTITY CONFIRMED" if (got == pin_sha and st.st_size == pin_bytes)
                   else "IDENTITY MISMATCH -- HALT",
    }
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))
    return res


# ===========================================================================
#  STAGE control -- the sixteen, fresh off the mount, under a scale sweep
# ===========================================================================
def stage_control(out):
    exe, swift_sha = build_ocr()
    if exe is None:
        sys.exit("APPLE-VISION-UNAVAILABLE")
    hands = hand_reads()
    d = os.path.join(SCRATCH, "control")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)

    raws = []
    for t, v, src in hands:
        raws.append((f"{t:.2f}", grab_single(MOUNT_MP4, t, EBOX)))

    sweep = {}
    for sc in SCALE_SWEEP:
        sd = os.path.join(d, f"x{sc}")
        paths = write_pngs(raws, sd, sc)
        got = vision(exe, paths)
        rows = []
        for (t, v, src), p in zip(hands, paths):
            cur, conf, raw = parse_lines(got.get(p, []))
            rows.append({"t": t, "hand": v, "src": src, "vision": cur,
                         "conf": conf, "raw": raw, "match": cur == v})
        n_ok = sum(1 for r in rows if r["match"])
        n_parse = sum(1 for r in rows if r["vision"] is not None)
        sweep[f"x{sc}"] = {"scale": sc, "n": len(rows), "parsed": n_parse,
                           "exact": n_ok, "rows": rows}
        print(f"  x{sc}: parsed {n_parse}/{len(rows)}  exact {n_ok}/{len(rows)}")

    best = None
    for sc in SCALE_SWEEP:
        s = sweep[f"x{sc}"]
        if s["exact"] == s["n"]:
            best = sc
            break
    if best is None:
        best = max(SCALE_SWEEP, key=lambda sc: (sweep[f"x{sc}"]["exact"],
                                                sweep[f"x{sc}"]["parsed"]))

    res = {"stage": "control", "swift_sha256": swift_sha, "ebox": list(EBOX),
           "n_hand_reads": len(hands), "scale_sweep": sweep,
           "chosen_scale": best,
           "chosen_rule": "smallest factor reproducing every hand read; "
                          "else the best-scoring factor, declared as imperfect",
           "clean_sweep": sweep[f"x{best}"]["exact"] == len(hands)}
    json.dump(res, open(out, "w"), indent=1)
    print(f"CHOSEN SCALE x{best}  clean={res['clean_sweep']}")
    return res


# ===========================================================================
#  STAGE population -- every frame of the combat window
# ===========================================================================
def stage_population(out, scale=None, limit=None):
    if scale is None:
        cj = os.path.join(NOTES, "2026-09-28-kc2-play-energy-fullreread-control.json")
        scale = json.load(open(cj))["chosen_scale"]
    exe, swift_sha = build_ocr()
    if exe is None:
        sys.exit("APPLE-VISION-UNAVAILABLE")

    t0, t1 = WINDOW
    x, y, w, h = EBOX
    d = os.path.join(SCRATCH, "pop")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)

    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}",
           "-i", MOUNT_MP4, "-vf", f"fps={HZ},crop={w}:{h}:{x}:{y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    fsz, k, paths, ts = w * h * 3, 0, [], []
    tstart = time.time()
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        im = Image.fromarray(fr)
        if scale != 1:
            im = im.resize((w * scale, h * scale), Image.NEAREST)
        pth = os.path.join(d, f"{k:06d}.png")
        im.save(pth)
        paths.append(pth)
        ts.append(round(t0 + k / HZ, 4))
        k += 1
        if limit and k >= limit:
            p.kill()
            break
    p.wait()
    print(f"extracted {k} frames in {time.time()-tstart:.1f}s -> {d}")

    tv = time.time()
    got = vision(exe, paths)
    print(f"vision on {len(paths)} frames in {time.time()-tv:.1f}s")

    rows = []
    for t, pth in zip(ts, paths):
        cur, conf, raw = parse_lines(got.get(pth, []))
        rows.append({"t": t, "cur": cur,
                     "conf": (round(conf, 4) if conf is not None else None),
                     "raw": raw if cur is None else None})
    res = {"stage": "population", "video": MOUNT_MP4, "t0": t0, "t1": t1,
           "hz": HZ, "box": list(EBOX), "scale": scale, "swift_sha256": swift_sha,
           "reader": "Apple Vision VNRecognizeTextRequest .accurate, "
                     "usesLanguageCorrection=false, minimumTextHeight=0.004",
           "n": len(rows),
           "parsed": sum(1 for r in rows if r["cur"] is not None),
           "rows": rows}
    json.dump(res, open(out, "w"))
    print(f"parsed {res['parsed']}/{res['n']} "
          f"({100.0*res['parsed']/max(1,res['n']):.2f} %)")
    shutil.rmtree(d, ignore_errors=True)   # crops are regenerable; disk is scarce
    return res


# ===========================================================================
#  STAGE analyse
# ===========================================================================
DENOM_I = 2576


def vision_erows(pop):
    """Put the Vision trace into the shape `clean()` consumes.

    DECLARED, because it is a transformation: `max` is set to 2576 because the
    PARSE POLICY only accepts a reading whose denominator VISION ITSELF read as
    2576 -- the field restates the accepted read, it does not assume it.  And
    `marg` is set to 0.0, a value the default gate (`marg_min = 0.0`) never
    consults.  ⚑ Vision's per-line CONFIDENCE is deliberately NOT written into
    `marg`: a recognition confidence and a template-matching margin are
    different quantities, and putting one in the other's field would smuggle a
    reader change into a cleaning parameter.
    """
    return [{"t": r["t"], "cur": r["cur"],
             "max": (DENOM_I if r["cur"] is not None else None), "marg": 0.0}
            for r in pop["rows"]]


def stage_analyse(out):
    from kc2_energy_reread import clamp_decomposition, above_ceiling_anatomy

    popf = os.path.join(NOTES, "2026-09-28-kc2-play-energy-fullreread-population.json")
    pop = json.load(open(popf))
    atlas = json.load(open(F_E60))

    a_by_t = {round(r["t"], 4): r for r in atlas["rows"]}
    v_by_t = {round(r["t"], 4): r for r in pop["rows"]}
    common = sorted(set(a_by_t) & set(v_by_t))

    # ---- 1 · the reader gap, at POPULATION scale (raw, before cleaning) ----
    both = [(t, a_by_t[t]["cur"], v_by_t[t]["cur"]) for t in common
            if a_by_t[t]["cur"] is not None and v_by_t[t]["cur"] is not None]
    agree = sum(1 for _, a, v in both if a == v)
    dis = [(t, a, v) for t, a, v in both if a != v]
    a_only = [t for t in common if a_by_t[t]["cur"] is not None
              and v_by_t[t]["cur"] is None]
    v_only = [t for t in common if a_by_t[t]["cur"] is None
              and v_by_t[t]["cur"] is not None]
    neither = [t for t in common if a_by_t[t]["cur"] is None
               and v_by_t[t]["cur"] is None]

    # ---- 2 · THE APPORTIONMENT the 2026-09-21 lap could not do -------------
    def ed1(a, b):
        a, b = str(a), str(b)
        return len(a) == len(b) and sum(1 for x, y in zip(a, b) if x != y) == 1

    a_above = [t for t in common if (a_by_t[t]["cur"] or 0) > CEIL]
    conf_ab = [t for t in a_above if (v_by_t[t]["cur"] or 0) > CEIL]
    refu_ab = [t for t in a_above if v_by_t[t]["cur"] is not None
               and v_by_t[t]["cur"] <= CEIL]
    unre_ab = [t for t in a_above if v_by_t[t]["cur"] is None]
    conf_exact = [t for t in conf_ab if v_by_t[t]["cur"] == a_by_t[t]["cur"]]
    conf_hard = [t for t in conf_ab if not ed1(a_by_t[t]["cur"], 1594)]
    v_above_new = [t for t in common if (v_by_t[t]["cur"] or 0) > CEIL
                   and a_by_t[t]["cur"] is not None
                   and a_by_t[t]["cur"] <= CEIL]

    # ---- 3 · the COMMITTED pipeline, run unchanged on each reader ----------
    #      `clean()` and `clamp_decomposition()` are IMPORTED, not reimplemented.
    def arm(erows, label):
        t, e, census = clean(erows)
        cd = clamp_decomposition(t, e)
        return {"reader": label, "census": census, "n_clean": int(len(e)),
                # ⚑ "ceiling duty" in the committed figures means EXACTLY at
                # 1594, not at-or-above. Both are reported so neither is read
                # as the other; the committed 0.2801 is the `at` one.
                "ceiling_duty_AT_1594": round(float((e == CEIL).mean()), 4),
                "at_or_above_ceiling_frac": round(float((e >= CEIL).mean()), 4),
                "above_ceiling_n": int((e > CEIL).sum()),
                "above_ceiling_frac": round(float((e > CEIL).mean()), 4),
                "clamp_decomposition": cd}

    atlas_arm = arm(atlas["rows"], "glyph atlas (committed 2026-08-25)")
    vis_arm = arm(vision_erows(pop), "Apple Vision (this lap, full re-read)")

    # ⚑ REPRODUCTION CONTROL.  Before any NEW number here is worth reading, the
    # instrument must reproduce the committed ones EXACTLY on the committed
    # input.  Expected values carried from the 2026-09-21 reread JSON, CL block.
    acd = atlas_arm["clamp_decomposition"]
    census_a = atlas_arm["census"]
    atlas_arm["reproduction_control"] = {
        "source": "notes/2026-09-21-kc2-play-energy-globe-reread.json CL block",
        "n_ticks": {"expected": 1626, "got": acd["n_ticks"],
                    "EXACT": acd["n_ticks"] == 1626},
        "SPEND_sum": {"expected": 18025.0, "got": acd["SPEND"]["sum"],
                      "EXACT": acd["SPEND"]["sum"] == 18025.0},
        "SPILL_sum": {"expected": 11723.0, "got": acd["SPILL"]["sum"],
                      "EXACT": acd["SPILL"]["sum"] == 11723.0},
        "census": {"expected": {"max_gate_pass": 10360,
                                "neighbour_median_rejected": 315,
                                "roundtrip_excursion_rejected": 86,
                                "used": 9959},
                   "got": {k: census_a[k] for k in
                           ("max_gate_pass", "neighbour_median_rejected",
                            "roundtrip_excursion_rejected", "used")},
                   "EXACT": (census_a["max_gate_pass"] == 10360
                             and census_a["neighbour_median_rejected"] == 315
                             and census_a["roundtrip_excursion_rejected"] == 86
                             and census_a["used"] == 9959)},
        "ceiling_duty_AT_1594": {"expected": 0.2801,
                                 "got": atlas_arm["ceiling_duty_AT_1594"],
                                 "EXACT": atlas_arm["ceiling_duty_AT_1594"] == 0.2801},
        "spill_share": {"expected": 0.3941,
                        "got": acd["SPILL"]["frac_of_published_gross"],
                        "EXACT": acd["SPILL"]["frac_of_published_gross"] == 0.3941},
    }
    atlas_arm["reproduction_control"]["ALL_EXACT"] = all(
        v["EXACT"] for k, v in atlas_arm["reproduction_control"].items()
        if isinstance(v, dict))

    # ---- 4 · the substitution anatomy, now on the STRONG reader ------------
    vrows = vision_erows(pop)
    # ⚑ `above_ceiling_anatomy` reports margin statistics. On the Vision arm
    # `marg` is the 0.0 PLACEHOLDER written by `vision_erows`, NOT a measured
    # quantity -- every `*_marg` field below reads 0.00 for that reason and
    # means nothing. Flagged rather than stripped, so the shape of the imported
    # instrument stays visible.
    v_anat = (above_ceiling_anatomy(vrows)
              if any(r["cur"] is not None and r["cur"] > CEIL for r in vrows)
              else {"n_above_ceiling_raw": 0,
                    "note": "the strong reader produced NO above-ceiling read"})

    res = {"stage": "analyse",
           "n_common_rows": len(common),
           "atlas_trace": os.path.relpath(F_E60, REPO),
           "vision_trace": os.path.relpath(popf, REPO),
           "cross_reader_population": {
               "n": len(common),
               "both_parsed": len(both),
               "exact_agreement": agree,
               "agreement_rate": round(agree / max(1, len(both)), 6),
               "n_disagreements": len(dis),
               "atlas_parsed_vision_not": len(a_only),
               "vision_parsed_atlas_not": len(v_only),
               "neither_parsed": len(neither),
               "atlas_parse_rate": round(
                   sum(1 for t in common if a_by_t[t]["cur"] is not None)
                   / max(1, len(common)), 6),
               "vision_parse_rate": round(
                   sum(1 for t in common if v_by_t[t]["cur"] is not None)
                   / max(1, len(common)), 6),
               "disagreement_sample": [{"t": t, "atlas": a, "vision": v}
                                       for t, a, v in dis[:200]]},
           "above_ceiling_apportionment": {
               "question": ("2026-09-21 closed holding this open: 'with one "
                            "confirmed above-ceiling frame I cannot apportion "
                            "the other 1,186.'  This is that apportionment."),
               "atlas_above_ceiling": len(a_above),
               "vision_CONFIRMS_above_ceiling": len(conf_ab),
               "vision_confirms_EXACT_same_value": len(conf_exact),
               "vision_REFUTES_at_or_below": len(refu_ab),
               "vision_unreadable": len(unre_ab),
               "confirmed_share_of_readable":
                   round(len(conf_ab) / max(1, len(conf_ab) + len(refu_ab)), 4),
               "confirmed_and_NOT_one_substitution_from_1594": len(conf_hard),
               "vision_above_that_atlas_did_not_see": len(v_above_new)},
           "arm_atlas": atlas_arm,
           "arm_vision": vis_arm,
           "vision_above_ceiling_anatomy": v_anat,
           "vision_anatomy_marg_fields_are_MEANINGLESS": (
               "every *_marg value in vision_above_ceiling_anatomy is the 0.0 "
               "placeholder from vision_erows(); Apple Vision has no template "
               "margin. Do not quote them."),
           "decode_confound": "see the decodecheck stage: re-running the "
                              "committed atlas tonight reproduces 10,816 of "
                              "10,959 August rows, so 1.3 % of any "
                              "atlas-vs-Vision difference is not the reader."}
    json.dump(res, open(out, "w"), indent=1)
    cr = dict(res["cross_reader_population"]); cr.pop("disagreement_sample")
    print(json.dumps(cr, indent=1))
    print(json.dumps(res["above_ceiling_apportionment"], indent=1))
    print("REPRODUCTION CONTROL:",
          json.dumps(atlas_arm["reproduction_control"], indent=1))
    for a in (atlas_arm, vis_arm):
        print(a["reader"], "| clean", a["n_clean"], "| duty@1594", a["ceiling_duty_AT_1594"],
              "| above", a["above_ceiling_n"],
              "| ticks", a["clamp_decomposition"]["n_ticks"],
              "| SPEND", a["clamp_decomposition"]["SPEND"],
              "| SPILL", a["clamp_decomposition"]["SPILL"])
    return res


# ===========================================================================
#  STAGE sheet -- resolve the row<->label alignment the 2026-09-21 note
#                 could only INFER (that note, Sect 8 item 5)
# ===========================================================================
SHEET_PNG = os.path.join(CHAN, "energy-sheet.png")
SHEET_X = 6          # the sheet is a x6 nearest upscale: 630 = 6*105, 2184 = 6*156
SHEET_W = 105        # the ODD pre-fix crop width (EBOX carries the fixed 104)
SHEET_H = 26
SHEET_ROWS = 14


def grab_exact(t, x, y, w, h):
    """A crop at an EXACT box, including odd x / odd w.

    ⚑ ffmpeg's `crop` on a yuv420p source silently rounds an odd width DOWN and
    an odd offset to the chroma grid -- the defect `eor_channel.EBOX` carries a
    comment about.  So grab an even-aligned SUPERSET and slice it in numpy,
    where no rounding happens.  Verified by the shape assertion below.
    """
    x0 = x - (x % 2)
    w0 = w + (x - x0)
    w0 += w0 % 2
    a = grab_single(MOUNT_MP4, t, (x0, y, w0, h + h % 2))
    out = a[0:h, (x - x0):(x - x0) + w]
    assert out.shape == (h, w, 3), out.shape
    return out


def locate_sheet_box(row, t, win=(1230, 994, 126, 46)):
    """LOCATE the sheet's crop box; do not assume it.

    ⚑ It is NOT `EBOX`.  Assuming it was cost a reading: matched at EBOX's
    x = 1240 every row scores MAD ~ 26 and the assignment rests on a
    separation of ~3.  One pixel to the left the SAME comparison scores 0.32.
    A crop box is an empirical fact about an artifact, and this one is read off
    the artifact by an exhaustive offset search, with the runner-up reported so
    the lock is visible.
    """
    big = grab_single(MOUNT_MP4, t, win)
    hits = []
    for dy in range(win[3] - SHEET_H + 1):
        for dx in range(win[2] - SHEET_W + 1):
            sub = big[dy:dy + SHEET_H, dx:dx + SHEET_W].astype(np.int16)
            hits.append((float(np.abs(sub - row).mean()), dx, dy))
    hits.sort()
    b, second = hits[0], hits[1]
    return ((win[0] + b[1], win[1] + b[2], SHEET_W, SHEET_H),
            {"mad": round(b[0], 4), "runner_up_mad": round(second[0], 4),
             "searched": f"{win[2]-SHEET_W+1} x {win[3]-SHEET_H+1} offsets",
             "probe_t": t})


def stage_sheet(out):
    """Pin each sheet row to a TIMESTAMP by pixels, not by value-order.

    The 2026-09-21 note declared a limitation against itself:

        "energy-sheet.png carries 14 crops and atlas-spec.json labels 10 ...
         the sheet records no row index, so the row<->label alignment is
         INFERRED from order and value."

    With the footage reachable the inference is unnecessary: re-extract the
    crop at each labelled timestamp and match it to a sheet row by pixels.
    Every match ships its DISTANCE and its RUNNER-UP, so a weak match reads
    as weak.
    """
    sheet = np.array(Image.open(SHEET_PNG).convert("RGB"))
    assert sheet.shape[:2] == (SHEET_H * SHEET_X * SHEET_ROWS,
                               SHEET_W * SHEET_X), sheet.shape
    rows = [sheet[i * SHEET_H * SHEET_X:(i + 1) * SHEET_H * SHEET_X:SHEET_X,
                  ::SHEET_X].astype(np.int16) for i in range(SHEET_ROWS)]
    blk = sheet[0:SHEET_X, 0:SHEET_X]
    nearest_ok = bool((blk == blk[0, 0]).all())   # verified, not trusted

    spec = json.load(open(os.path.join(CHAN, "atlas-spec.json")))
    box, loc = locate_sheet_box(rows[6], float(spec[6]["t"]))

    fresh = [grab_exact(float(s["t"]), *box).astype(np.int16) for s in spec]
    M = np.zeros((len(spec), SHEET_ROWS))
    for i, f in enumerate(fresh):
        for j, r in enumerate(rows):
            M[i, j] = float(np.abs(f - r).mean())

    assign, used = [], set()
    for i, s in enumerate(spec):
        order = np.argsort(M[i])
        j = int(order[0])
        assign.append({"t": float(s["t"]), "hand": s["s"], "best_row": j,
                       "mad": round(float(M[i, j]), 4),
                       "runner_up_row": int(order[1]),
                       "runner_up_mad": round(float(M[i, order[1]]), 4),
                       "separation": round(float(M[i, order[1]] - M[i, j]), 4),
                       "row_already_taken": j in used})
        used.add(j)

    mads = [a["mad"] for a in assign]
    seps = [a["separation"] for a in assign]
    res = {"stage": "sheet",
           "purpose": "replace the INFERRED row<->label alignment with a "
                      "pixel-matched one, now that the footage is reachable",
           "sheet": os.path.relpath(SHEET_PNG, REPO),
           "sheet_sha256": sha256(SHEET_PNG),
           "upscale_was_nearest_neighbour_VERIFIED": nearest_ok,
           "sheet_box_LOCATED": list(box),
           "sheet_box_vs_EBOX": {"EBOX": list(EBOX), "delta_x": box[0] - EBOX[0],
                                 "delta_y": box[1] - EBOX[1],
                                 "delta_w": box[2] - EBOX[2]},
           "sheet_box_location_quality": loc,
           "n_rows": SHEET_ROWS, "n_labels": len(spec),
           "assignment": assign,
           "worst_mad": round(max(mads), 4),
           "smallest_separation": round(min(seps), 4),
           "all_distinct_rows": len({a["best_row"] for a in assign}) == len(assign),
           "monotone_in_time": all(assign[i]["best_row"] < assign[i + 1]["best_row"]
                                   for i in range(len(assign) - 1)),
           "unmatched_rows": sorted(set(range(SHEET_ROWS))
                                    - {a["best_row"] for a in assign}),
           "verdict": ("ALIGNMENT RESOLVED BY PIXELS"
                       if max(mads) < 2.0 and min(seps) > 5.0
                       else "ALIGNMENT NOT DECISIVE -- remains inferred")}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "assignment"}, indent=1))
    for a in assign:
        print(f"  t={a['t']:7.2f} {a['hand']:>10}  -> row {a['best_row']:2d}  "
              f"mad {a['mad']:9.4f}  runner-up row {a['runner_up_row']:2d} "
              f"mad {a['runner_up_mad']:9.4f}")
    return res


# ===========================================================================
#  STAGE boxprobe -- is the ONE-PIXEL box offset the atlas's defect?
# ===========================================================================
ATLAS_NPZ = os.path.join(CHAN, "energy-atlas.npz")
PROBE_X0 = 1236          # left edge of the offset sweep
PROBE_N = 9              # x offsets probed: 1236 .. 1244


def stage_boxprobe(out):
    """Run the COMMITTED glyph atlas over the whole window at a sweep of crop
    offsets, and see which one it was built for.

    ⚑ WHY.  The `sheet` stage found the atlas build sheet sits at x = 1239 while
    the trace box `EBOX` reads at x = 1240 -- ONE PIXEL apart, MAD 0.32 against
    24.73.  If the atlas's templates were cut at one offset and the trace read
    at another, that is a candidate MECHANISM for the atlas's error rate, and
    it is testable without settling anything else.  If the sweep is flat, the
    offset is not the mechanism and this stage says so.

    The atlas reader is IMPORTED from `eor_channel`, not reimplemented.
    """
    from eor_channel import mask_of, read_mask
    z = np.load(ATLAS_NPZ, allow_pickle=True)
    keys, protos = list(z["keys"]), z["protos"]

    committed = {round(r["t"], 4): r for r in json.load(open(F_E60))["rows"]}
    hands = {round(t, 2): v for t, v, _ in hand_reads()}

    t0, t1 = WINDOW
    _, y, w, h = EBOX
    span = PROBE_N + w + 1
    span += span % 2
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}",
           "-i", MOUNT_MP4, "-vf", f"fps={HZ},crop={span}:{h}:{PROBE_X0}:{y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    fsz = span * h * 3
    reads = {PROBE_X0 + d: {} for d in range(PROBE_N)}
    k = 0
    tstart = time.time()
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(h, span, 3)
        t = round(t0 + k / HZ, 4)
        for d in range(PROBE_N):
            sub = fr[:, d:d + w]
            sstr, marg = read_mask(mask_of(sub), keys, protos)
            cur = None
            if sstr and "/" in sstr:
                a, _, b = sstr.partition("/")
                if a.isdigit() and b.isdigit() and b == DENOM:
                    cur = int(a)
            reads[PROBE_X0 + d][t] = (cur, sstr, marg)
        k += 1
    p.wait()
    print(f"atlas swept {PROBE_N} offsets over {k} frames in "
          f"{time.time()-tstart:.1f}s")

    per_x = {}
    for x, d in reads.items():
        cur = [v[0] for v in d.values()]
        parsed = [c for c in cur if c is not None]
        same = sum(1 for t, v in d.items()
                   if committed.get(t, {}).get("cur") == v[0])
        hits = miss = 0
        for ht, hv in hands.items():
            key = min(d, key=lambda tt: abs(tt - ht))
            if abs(key - ht) <= 0.02:
                if d[key][0] == hv:
                    hits += 1
                else:
                    miss += 1
        per_x[x] = {"x": x, "n": len(cur), "parsed": len(parsed),
                    "parse_rate": round(len(parsed) / max(1, len(cur)), 6),
                    "above_ceiling": sum(1 for c in parsed if c > CEIL),
                    "above_ceiling_frac": round(
                        sum(1 for c in parsed if c > CEIL) / max(1, len(parsed)), 4),
                    "agrees_with_committed_trace": same,
                    "hand_control_hits": hits, "hand_control_misses": miss}
        print(f"  x={x}: parse {per_x[x]['parse_rate']:.4f}  "
              f"above-ceiling {per_x[x]['above_ceiling']:5d}  "
              f"== committed {same:5d}  hand {hits}/{hits+miss}")

    best_parse = max(per_x.values(), key=lambda r: r["parse_rate"])
    matchx = max(per_x.values(), key=lambda r: r["agrees_with_committed_trace"])
    rates = [r["parse_rate"] for r in per_x.values()]
    res = {"stage": "boxprobe",
           "atlas": os.path.relpath(ATLAS_NPZ, REPO),
           "atlas_sha256": sha256(ATLAS_NPZ),
           "sweep_x": [PROBE_X0 + d for d in range(PROBE_N)],
           "EBOX_x": EBOX[0], "sheet_box_x": 1239,
           "per_offset": per_x,
           "best_parse_rate_at_x": best_parse["x"],
           "reproduces_committed_trace_at_x": matchx["x"],
           "parse_rate_spread": round(max(rates) - min(rates), 6),
           "verdict": ("THE OFFSET MATTERS" if max(rates) - min(rates) > 0.01
                       else "THE OFFSET IS NOT THE MECHANISM -- sweep is flat")}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k2: v for k2, v in res.items() if k2 != "per_offset"},
                     indent=1))
    return res


# ===========================================================================
#  STAGE decodecheck -- separate the READER GAP from the DECODE CONFOUND
# ===========================================================================
def stage_decodecheck(out):
    """The committed atlas trace was decoded in August; this lap's Vision trace
    was decoded tonight.  Any difference between them mixes TWO causes.

    ⚑ `boxprobe` surfaced the confound without being aimed at it: re-running the
    COMMITTED atlas over the SAME window today reproduces the committed trace on
    10,816 of 10,959 rows, not all of them.  So some of the atlas-vs-Vision gap
    is not a reader difference at all.  This stage sizes it, by running the
    atlas and reading the Vision trace off the SAME decode.
    """
    from eor_channel import mask_of, read_mask
    z = np.load(ATLAS_NPZ, allow_pickle=True)
    keys, protos = list(z["keys"]), z["protos"]
    committed = {round(r["t"], 4): r["cur"] for r in json.load(open(F_E60))["rows"]}
    popf = os.path.join(NOTES, "2026-09-28-kc2-play-energy-fullreread-population.json")
    visn = {round(r["t"], 4): r["cur"] for r in json.load(open(popf))["rows"]}

    t0, t1 = WINDOW
    x, y, w, h = EBOX
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}",
           "-i", MOUNT_MP4, "-vf", f"fps={HZ},crop={w}:{h}:{x}:{y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    fsz, k, today = w * h * 3, 0, {}
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        sstr, _ = read_mask(mask_of(fr), keys, protos)
        cur = None
        if sstr and "/" in sstr:
            a, _, b = sstr.partition("/")
            if a.isdigit() and b.isdigit() and b == DENOM:
                cur = int(a)
        today[round(t0 + k / HZ, 4)] = cur
        k += 1
    p.wait()

    ks = sorted(set(today) & set(committed) & set(visn))
    aug_today = sum(1 for t in ks if committed[t] == today[t])
    ab = [t for t in ks if today[t] is not None and visn[t] is not None]
    same_decode = sum(1 for t in ab if today[t] == visn[t])
    ab_aug = [t for t in ks if committed[t] is not None and visn[t] is not None]
    cross_decode = sum(1 for t in ab_aug if committed[t] == visn[t])

    res = {"stage": "decodecheck",
           "n": len(ks),
           "atlas_AUGUST_vs_atlas_TONIGHT": {
               "identical_rows": aug_today,
               "rate": round(aug_today / max(1, len(ks)), 6),
               "differing_rows": len(ks) - aug_today,
               "meaning": "the DECODE + environment term: same reader, same "
                          "box, same file, different day"},
           "reader_gap_SAME_decode": {
               "both_parsed": len(ab), "agree": same_decode,
               "rate": round(same_decode / max(1, len(ab)), 6),
               "meaning": "atlas vs Vision with the decode held FIXED -- this "
                          "is the reader gap with the confound removed"},
           "reader_gap_CROSS_decode": {
               "both_parsed": len(ab_aug), "agree": cross_decode,
               "rate": round(cross_decode / max(1, len(ab_aug)), 6),
               "meaning": "atlas(August) vs Vision(tonight) -- the headline "
                          "number, which CONTAINS the decode term"},
           "atlas_parse_rate_tonight": round(
               sum(1 for t in ks if today[t] is not None) / max(1, len(ks)), 6),
           "atlas_parse_rate_august": round(
               sum(1 for t in ks if committed[t] is not None) / max(1, len(ks)), 6)}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))
    return res


STAGES = {"identity": stage_identity, "control": stage_control,
          "population": stage_population, "analyse": stage_analyse,
          "sheet": stage_sheet,
          "boxprobe": stage_boxprobe,
          "decodecheck": stage_decodecheck}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in STAGES:
        sys.exit(__doc__)
    st = sys.argv[1]
    dflt = os.path.join(NOTES, f"2026-09-28-kc2-play-energy-fullreread-{st}.json")
    STAGES[st](sys.argv[2] if len(sys.argv) > 2 else dflt)
