#!/usr/bin/env python3
"""C-9 image bake-off (R-C9-79): contact sheets, the one-page table, and the results file.

    python3 09_deliver.py

Scores come from the score_j*.json files; nothing is re-typed. The VERDICTS are the part the
instruments cannot give on their own -- which way a profile faces, whether a helmet has a face
mask, whether a painting invented a tarn -- so each one is written here as a sentence with its
evidence, next to the numbers it qualifies, and it is the verdict and not the number that
decides PASS / FAIL. Where a number and the eye disagreed, the instrument was fixed first
(J3 detail gain, J4 chance baseline and invented-content share) and both are reported.
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
C9 = HERE.parent
DEST = pathlib.Path.home() / "Desktop" / "Astra Burst Review - 2026-09-26" / "C-9 image bake-off"
CANDS = [("astra", "Astra (ChatGPT lane)"), ("nb", "Nano Banana"), ("nbp", "Nano Banana Pro")]
PRICE = {"astra": 0.0, "nb": 0.0398, "nbp": 0.15}

S1, S2, S3, S4 = (json.loads((HERE / f).read_text()) for f in
                  ("score_j1.json", "score_j2.json", "score_j3.json", "score_j4.json"))
B1 = json.loads((HERE / "score_j1_build.json").read_text())
GEN = json.loads((HERE / "generate_log.json").read_text())

# Astra seconds per image: the lane's wall clock / image calls (ledger), and per delivered image
ASTRA_S = {"J1": (177, 355), "J2": (118, 178), "J3": (129, 129), "J4": (219, 328)}


def secs(job, c):
    if c == "astra":
        return ASTRA_S[job][0]
    xs = [x["seconds"] for x in GEN[job] if x["file"].startswith("%s_%s_" % (job, c))]
    return round(sum(xs) / len(xs), 1)


FILES = {
    "J1": {"astra_a": C9 / "artifacts/NB-1/NB-1_a.png", "astra_b": C9 / "artifacts/NB-1/NB-1_b.png"},
    "J2": {"astra_a": C9 / "artifacts/NB-G1/NB-G1_a.png", "astra_b": C9 / "artifacts/NB-G1/NB-G1_b.png"},
    "J3": {"astra_a": C9 / "artifacts/T8P-B/T8P-B_a.png", "astra_b": C9 / "artifacts/T8P-B/T8P-B_b.png"},
    "J4": {"astra_a": C9 / "artifacts/IBO-J4/IBO-J4_a.png", "astra_b": C9 / "artifacts/IBO-J4/IBO-J4_b.png"},
}
for j in FILES:
    for c in ("nb", "nbp"):
        for v in ("a", "b"):
            FILES[j]["%s_%s" % (c, v)] = HERE / "out" / ("%s_%s_%s.png" % (j, c, v))
INPUTS = {"J1": (C9 / "artifacts/inputs/nb_style_ref_matt.png", "input: style ref only"),
          "J2": (C9 / "artifacts/NB-1/NB-1_b.png", "input: NB-1_b base sheet"),
          "J3": (C9 / "artifacts/CS9-guides/t8_sheet_b_canvas.png", "input: sheet A projected (canvas)"),
          "J4": (C9 / "artifacts/CS9-guides/IBO-J4-2_1_canvas.png", "input: guide chunk 2_1")}

# (pass, one-line evidence) per sheet
V = {
 "J1": {"astra_a": (True, "profiles face correctly; tattoo on his right arm in every view"),
        "astra_b": (True, "profiles face correctly; tattoo right arm; the approved sheet (R-C9-70)"),
        "nb_a": (False, "LEFT view faces the wrong way; front view tattoo on the wrong arm"),
        "nb_b": (False, "LEFT view faces the wrong way"),
        "nbp_a": (None, "profiles correct, best build; BUT text labels + cell borders, front tattoo on wrong arm"),
        "nbp_b": (False, "RIGHT view faces the wrong way; front tattoo on the wrong arm")},
 "J2": {"astra_a": (False, "body moved: legs shifted up to 11 px"),
        "astra_b": (True, "spangenhelm + nasal, no mask; body held within 1 px"),
        "nb_a": (False, "helmet right, but body moved (legs up to 8.5 px, IoU 0.72)"),
        "nb_b": (False, "FACE MASK (spectacle guards) -- brief says NO face mask"),
        "nbp_a": (False, "FACE MASK (spectacle guards); pose held 0.974"),
        "nbp_b": (False, "FACE MASK; whole body restyled (paler, different hand)")},
 "J3": {"astra_a": (True, "real repaint (detail x1.42) at low disagreement; the variant used (D1 15.38)"),
        "astra_b": (True, "real repaint (detail x1.40) at low disagreement"),
        "nb_a": (False, "no repaint (detail x0.96); head close-ups redrawn from a new camera"),
        "nb_b": (False, "canvas handed back almost unchanged (detail x1.00)"),
        "nbp_a": (False, "heavy restyle: disagreement 31.9, the blind-painting level (T5: 34.2)"),
        "nbp_b": (False, "views re-laid out as an eye-level turnaround")},
 "J4": {"astra_a": (True, "6/6 stones at 1.0 px; figure painted out; nothing invented"),
        "astra_b": (True, "6/6 stones at 1.0 px; figure painted out; nothing invented"),
        "nb_a": (False, "invented a barrow scene (mound, tarn, path, trees); figure left in"),
        "nb_b": (False, "invented a scene (mound, tarn, mountains, fire); 2/6 stones"),
        "nbp_a": (False, "stones kept, but tarn, path, mound, cairns invented on open snow"),
        "nbp_b": (False, "stones kept (5/6), but mound, tarn, path, cairns invented")},
}


def score_line(job, k):
    if job == "J1":
        s = S1[k]
        t = "mirror %.3f  pair %.3f  h-cv %.3f" % (s["mirror_iou"], s["pair_iou"], s["height_cv"])
        if k == "nbp_a":
            t += "  | build IoU %.3f" % B1["nbp_a"]["sheet_iou_mean"]
        if k == "astra_b":
            t += "  | build IoU %.3f" % B1["astra_b (NB-1_b)"]["sheet_iou_mean"]
        return t
    if job == "J2":
        s = S2[k]
        return "IoU outside gear %.3f  paint delta %.1f  legs %.1f px" % (
            s["iou_outside_gear"], s["paint_delta_outside_gear"], s["leg_shift_max_px"])
    if job == "J3":
        s = S3[k]
        return "disagreement %.1f  >24: %.0f%%  detail x%.2f" % (
            s["screen_disagreement"]["mean"], s["screen_disagreement"]["pct_over_24"], s["detail_gain"])
    s = S4[k]
    return "kept %d/%d  %.1f px  invented %.0f%%%s" % (
        s["shapes_kept"], s["shapes_total"], s["mean_chamfer_px"], 100 * s["open_ground_not_snow"],
        "" if s["figure_out"] else "  figure LEFT IN")


TITLES = {"J1": "JOB 1 - design sheet (NB-1 brief): mirror IoU, view consistency, facing; one Tripo build",
          "J2": "JOB 2 - gear-layer EDIT on NB-1_b (NB-G1 brief): body held outside the gear, gear as briefed",
          "J3": "JOB 3 - texture repaint EDIT over sheet A's projection (T8P-B brief): D1-proxy disagreement + detail gain",
          "J4": "JOB 4 - blockout paint-over, ring-centre chunk (TEST canvas): shapes kept, registration, nothing invented"}
FN = {"J1": "job 1 - design sheet.png", "J2": "job 2 - gear edit.png",
      "J3": "job 3 - texture repaint.png", "J4": "job 4 - paint-over.png"}


def font(sz, bold=False):
    for p in (("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else
               "/System/Library/Fonts/Supplemental/Arial.ttf"), "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def contact(job):
    portrait = job in ("J1", "J2")
    tw, th = (300, 450) if portrait else (450, 300)
    cap = 74
    W = 20 + (tw + 20) * 4
    H = 60 + 36 + 2 * (th + cap + 16) + 10
    im = Image.new("RGB", (W, H), (242, 242, 245))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 52], fill=(30, 33, 40))
    d.text((16, 14), TITLES[job], font=font(20, True), fill=(240, 242, 246))
    x0 = 20
    ip, il = INPUTS[job]
    t = Image.open(ip).convert("RGB")
    t.thumbnail((tw, th))
    im.paste(t, (x0, 96))
    d.text((x0, 96 + t.size[1] + 6), il, font=font(14, True), fill=(40, 44, 52))
    for ci, (c, label) in enumerate(CANDS):
        cx = 20 + (tw + 20) * (ci + 1)
        d.text((cx, 56), label, font=font(15, True), fill=(30, 33, 40))
        d.text((cx, 76), "%s s/img  ·  %s/img" % (secs(job, c), "$0 sub." if c == "astra" else "$%.4f" % PRICE[c]),
               font=font(13), fill=(90, 94, 104))
        for vi, v in enumerate(("a", "b")):
            k = "%s_%s" % (c, v)
            cy = 96 + vi * (th + cap + 16)
            t = Image.open(FILES[job][k]).convert("RGB").resize((tw, th), Image.LANCZOS)
            im.paste(t, (cx, cy))
            ok, why = V[job][k]
            col = (40, 140, 70) if ok else ((190, 120, 20) if ok is None else (190, 50, 40))
            tag = "PASS" if ok else ("PARTIAL" if ok is None else "FAIL")
            d.rectangle([cx, cy, cx + 74, cy + 22], fill=col)
            d.text((cx + 6, cy + 3), "%s %s" % (v, tag), font=font(14, True), fill=(255, 255, 255))
            d.text((cx, cy + th + 4), score_line(job, k), font=font(13), fill=(40, 44, 52))
            words, line, yy = why.split(), "", cy + th + 24
            for w_ in words:
                if d.textlength(line + " " + w_, font=font(13)) > tw:
                    d.text((cx, yy), line.strip(), font=font(13), fill=col)
                    yy += 17
                    line = ""
                line += " " + w_
            d.text((cx, yy), line.strip(), font=font(13), fill=col)
    im.save(DEST / FN[job])
    return im.size


ROWS = [  # job, recommendation
 ("J1", "KEEP ASTRA. Nano Banana fails (profiles face the wrong way in both). Pro is the one worth a second look -- its best "
        "sheet built MORE consistently than NB-1_b (0.918 vs 0.845) -- but 1 of 2 had a wrong-facing view and both put the "
        "tattoo on the wrong arm; usable only behind an automated facing/sidedness/label gate we do not have."),
 ("J2", "KEEP ASTRA. Pro held pose and outline as well as Astra's approved variant (0.974 vs 0.976) but put a FACE MASK on "
        "the helmet in both variants against an explicit 'NO face mask'. Nano Banana: one masked, one drifted."),
 ("J3", "KEEP ASTRA. Both candidates fail: Nano Banana did not repaint (detail x0.96-1.00) or redrew the close-ups; Pro "
        "restyled at the blind-painting disagreement level (31.9 vs T5's 34.2) or re-laid the sheet out."),
 ("J4", "KEEP ASTRA. Both candidates fail: they painted the prompt's colour legend as a scene (tarn, path, mound, cairns) "
        "onto open snow -- 20-38% of it. Astra: 6/6 stones at 1.0 px, figure out, nothing invented."),
]


def table():
    W, pad = 1900, 18
    rows = []
    for job, rec in ROWS:
        for c, label in CANDS:
            ks = ["%s_%s" % (c, v) for v in ("a", "b")]
            res = [V[job][k][0] for k in ks]
            rows.append((job, label, "  |  ".join(score_line(job, k) for k in ks),
                         " / ".join("PASS" if r else ("PARTIAL" if r is None else "FAIL") for r in res),
                         "%s" % secs(job, c), "$0 (sub.)" if c == "astra" else "$%.4f" % PRICE[c]))
    H = 110 + len(rows) * 30 + 4 * 16 + len(ROWS) * 64 + 140
    im = Image.new("RGB", (W, H), (248, 248, 250))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 64], fill=(30, 33, 40))
    d.text((pad, 10), "C-9 image-model bake-off (R-C9-79): Astra vs Nano Banana vs Nano Banana Pro", font=font(24, True), fill=(240, 242, 246))
    # SPEND IS READ FROM THE LEDGER, not typed: a figure written into a label goes stale the
    # moment anything else is spent, and this page is the one Matt reads.
    led = json.loads((HERE / "fal_spend_R-C9-79.json").read_text())
    by = {}
    for e in led["entries"]:
        k = "images" if "nano-banana" in e["endpoint"] else ("Tripo" if "tripo" in e["endpoint"] else "mattes")
        by.setdefault(k, [0, 0.0])
        by[k][0] += 1
        by[k][1] += e["usd"]
    d.text((pad, 40), "2 variants per candidate per job, same brief text and inputs; scored with the run's own "
                      "instruments. fal spend $%.4f of $%.2f (%s)." % (
                          led["running_usd"], led["budget_usd"],
                          ", ".join("%d %s $%.4f" % (n, k, v) for k, (n, v) in by.items())),
           font=font(15), fill=(170, 176, 190))
    cols = [(pad, "job"), (70, "candidate"), (260, "score (variant a | variant b)"), (1370, "verdict a / b"),
            (1570, "s / image"), (1690, "$ / image")]
    y = 78
    for x, t in cols:
        d.text((x, y), t, font=font(15, True), fill=(30, 33, 40))
    y += 26
    last = None
    for job, label, sc, ver, s, usd in rows:
        if job != last and last is not None:
            y += 16
        last = job
        col = (40, 140, 70) if ver == "PASS / PASS" else ((190, 50, 40) if "PASS" not in ver else (190, 120, 20))
        for (x, _), t in zip(cols, (job, label, sc, ver, s, usd)):
            d.text((x, y), t, font=font(14, x in (pad, 1370)), fill=col if x == 1370 else (40, 44, 52))
        y += 30
    y += 12
    d.text((pad, y), "RECOMMENDATION PER JOB", font=font(17, True), fill=(30, 33, 40))
    y += 28
    for job, rec in ROWS:
        words, line = rec.split(), ""
        d.text((pad, y), job, font=font(15, True), fill=(30, 33, 40))
        for w_ in words:
            if d.textlength(line + " " + w_, font=font(15)) > W - 120:
                d.text((70, y), line.strip(), font=font(15), fill=(40, 44, 52))
                y += 21
                line = ""
            line += " " + w_
        d.text((70, y), line.strip(), font=font(15), fill=(40, 44, 52))
        y += 30
    d.text((pad, y + 4), "Astra s/image = lane wall clock / image calls; per DELIVERED image it is 355 / 178 / 129 / 328 s "
                         "(its agent retries: NB-1 4 calls, NB-G1 3, T8P-B 2, IBO-J4 3). Candidates: one call per variant, "
                         "no retries -- the actual trade on offer.", font=font(14), fill=(110, 114, 124))
    im = im.crop((0, 0, W, y + 40))
    im.save(DEST / "bake-off table.png")
    return im.size


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for job in ("J1", "J2", "J3", "J4"):
        print(job, contact(job), "->", DEST / FN[job])
    print("table", table(), "->", DEST / "bake-off table.png")
    out = {"_what": "C-9 image-model bake-off (R-C9-79): verdicts, scores, seconds and cost per image.",
           "verdicts": {j: {k: {"pass": v[0], "evidence": v[1]} for k, v in d.items()} for j, d in V.items()},
           "seconds_per_image": {j: {c: secs(j, c) for c, _ in CANDS} for j in V},
           "astra_seconds_per_delivered_image": {j: ASTRA_S[j][1] for j in V},
           "usd_per_image": PRICE, "recommendations": dict(ROWS)}
    (HERE / "bakeoff_results.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
