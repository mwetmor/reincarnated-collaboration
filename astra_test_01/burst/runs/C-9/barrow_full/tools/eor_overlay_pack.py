#!/usr/bin/env python3
"""C-9 R-C9-146 follow-on (lane EOR2, drax): pack the Eye of Reckoning ARENA OVERLAY atlas for kc2_play.

Reads the raw frames godot/tools/render_eor_overlay.gd wrote (per tint) and writes, under OUT:
  <tint>/under/start/under_start_NN.png  <tint>/under/loop/under_loop_NNN.png
  <tint>/over/<seg>/<DIR>/over_<seg>_<DIR>_NN(N).png          seg = start | loop | end
  manifest.json   previews/*.png

  UNDER  bed + haze. Rendered on a TRANSPARENT viewport: its colour is premultiplied -> divided out to STRAIGHT alpha.
  OVER   cuts + sparks + embers: ADDITIVE emission, rendered on BLACK -> alpha = max(R, G, B), colour / alpha
         (straight). Composited with ordinary alpha-over it reproduces the additive look over a dark-to-mid floor;
         the runtime may instead draw it with additive blend on the raw colour (both declared).
  LOOP   4 revolutions (1.2 s, 64 frames, 16/rev = the body's eor_spin_loop grid). Rendered once from 0.2 s; the
         last FADE frames crossfade (premultiplied) into the frames just BEFORE 0.2 s, i.e. the start segment's tail,
         so start -> loop and loop -> loop are both continuous.
  END    over only (cuts finish in 0.45 rev, sparks 0.42 s, embers 0.2 s), 25 frames @ 30 fps from release. The
         under layer has NO end frames: on release it keeps looping and fades alpha 1 -> 0 over 0.8 s, which is the
         effect's own release (eor_kc2_fx.gd PORT 9) and never jumps to a different haze.

  usage: eor_overlay_pack.py RAW_ROOT OUT PACK_ROOT
"""
import hashlib, json, os, sys
from PIL import Image
import numpy as np

RAW, OUT, PACK = sys.argv[1], sys.argv[2], sys.argv[3]
DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
LOOP_N, TAIL = 64, 5
PPM = 151.33680669505316


def straight_from_premul(im):
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    al = a[..., 3:4]
    rgb = np.where(al > 0, np.minimum(255.0, a[..., :3] * 255.0 / np.maximum(al, 1.0)), 0.0)
    return Image.fromarray(np.concatenate([rgb, al], axis=-1).round().astype(np.uint8), "RGBA")


def straight_from_additive(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    al = a.max(axis=-1, keepdims=True)
    rgb = np.where(al > 0, a * 255.0 / np.maximum(al, 1.0), 0.0)
    return Image.fromarray(np.concatenate([rgb, al], axis=-1).round().astype(np.uint8), "RGBA")


def blend(a, b, w):
    """premultiplied-space blend of two straight RGBA images: (1-w) a + w b"""
    return Image.blend(a.convert("RGBa"), b.convert("RGBa"), w).convert("RGBA")


def edge_touch(im):
    a = im.getchannel("A")
    w, h = im.size
    for box in [(0, 0, w, 1), (0, h - 1, w, h), (0, 0, 1, h), (w - 1, 0, w, h)]:
        if a.crop(box).getextrema()[1] > 0:
            return True
    return False


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def save(im, path, files, lint):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, optimize=True)
    files.append({"file": os.path.relpath(path, OUT), "sha256": sha(path)})
    if edge_touch(im):
        lint.append(os.path.relpath(path, OUT))


def loop_frames(load, conv):
    """the 64 loop frames, the last TAIL crossfaded into the start's tail (m005..m001 = 5..1 frames before 0.2 s)"""
    out = []
    for i in range(LOOP_N):
        im = conv(load("%03d" % i))
        k = i - (LOOP_N - TAIL - 1)              # 1..TAIL over the last TAIL frames
        if k >= 1:
            w = k / (TAIL + 1.0)
            im = blend(im, conv(load("m%03d" % (LOOP_N - i))), w)
        out.append(im)
    return out


man = {"schema": "c9-eor-overlay/1", "skill": "Eye of Reckoning (dark knight / gd-eor-warlord)", "tints": {}, "lint_edge_touch": {}}
for tint in ["red", "original"]:
    root = os.path.join(RAW, tint)
    files, lint = [], []
    # UNDER: start (7) + loop (64), direction-independent
    for i in range(7):
        save(straight_from_premul(Image.open(f"{root}/under/start/{i:02d}.png")), f"{OUT}/{tint}/under/start/under_start_{i:02d}.png", files, lint)
    for i, im in enumerate(loop_frames(lambda n: Image.open(f"{root}/under/loop/{n}.png"), straight_from_premul)):
        save(im, f"{OUT}/{tint}/under/loop/under_loop_{i:03d}.png", files, lint)
    # OVER: per direction, start (7) + loop (64) + end (25)
    for d in DIRS:
        for i in range(7):
            save(straight_from_premul(Image.open(f"{root}/over/start/{d}/{i:02d}.png")), f"{OUT}/{tint}/over/start/{d}/over_start_{d}_{i:02d}.png", files, lint)
        for i, im in enumerate(loop_frames(lambda n, d=d: Image.open(f"{root}/over/loop/{d}/{n}.png"), straight_from_premul)):
            save(im, f"{OUT}/{tint}/over/loop/{d}/over_loop_{d}_{i:03d}.png", files, lint)
        for i in range(25):
            save(straight_from_premul(Image.open(f"{root}/over/end/{d}/{i:02d}.png")), f"{OUT}/{tint}/over/end/{d}/over_end_{d}_{i:02d}.png", files, lint)
    man.setdefault("frames", {})[tint] = {"files": len(files), "list": files}
    man["lint_edge_touch"][tint] = lint
    print(tint, "files", len(files), "edge-touch", len(lint))

idx = json.load(open(os.path.join(PACK, "matrix_index.json")))
man.update({
    "body_pack": {"root": PACK, "index_sha256": sha(os.path.join(PACK, "matrix_index.json")), "kit": idx.get("kit"),
                  "states": {"start": "eor_spin_start", "loop": "eor_spin_loop"}},
    "camera": {"projection": "orthographic", "pitch_deg": 52.9535411256029, "yaw_deg": 0.0,
               "frame": "port model: x screen-right, y toward camera, z up; origin = character ground origin (same as the cells)"},
    "layers": {
        "under": {"contents": "smoke bed + haze (ground plane)", "draw": "BELOW the actor (before his cell; same anchor point)",
                  "canvas_px": [1024, 1024], "anchor_px": [512, 576], "ppm": PPM / 2.0, "scale_vs_cells": 2.0,
                  "per_direction": False, "alpha": "straight", "blend": "alpha-over"},
        "over": {"contents": "sparks (3 source emitters + 1 on the mace head) + ember flecks; NO arc (R-C9-152)", "draw": "ABOVE the actor (after his cell)",
                 "canvas_px": [1536, 1536], "anchor_px": [768, 832], "ppm": PPM, "scale_vs_cells": 1.0,
                 "per_direction": True, "directions": DIRS, "alpha": "straight (a transparent render, un-premultiplied)", "blend": "alpha-over",
                 "holdout": "a 0.28 m x 1.85 m depth-only capsule at his origin hides what is BEHIND his body; the cells' own silhouette is not used"},
    },
    "segments": {
        "start": {"event": "channel_begin", "frames": 7, "fps": 30.0, "t_s": [round(i / 30.0, 6) for i in range(7)],
                  "body_state": "eor_spin_start (same 7 t_s)", "layers": ["under", "over"],
                  "play": "once, from the oracle's channel-begin event; then loop frame 0"},
        "loop": {"event": "sustain", "frames": 64, "frames_per_rev": 16, "revs": 4, "length_s": 1.2, "fps": 16 / 0.3,
                 "t_s": [round(i * 0.01875, 6) for i in range(64)],
                 "phase_lock": "overlay loop frame = 16 * (revolution count mod 4) + the body's eor_spin_loop frame index",
                 "why_4_revs": ("one revolution cannot loop: the haze (5.5 s particles) and the spark schedule (hashed per "
                                "revolution) are not 1-rev periodic. 4 revs (1.2 s); the wrap is a 5-frame crossfade into the "
                                "start's tail, so start -> loop and loop -> loop are continuous."),
                 "layers": ["under", "over"], "play": "repeat while the channel is active (oracle sustain)"},
        "end": {"event": "release", "frames": 25, "fps": 30.0, "length_s": 0.8, "t_s": [round(i / 30.0, 6) for i in range(25)],
                "layers": ["over"],
                "over": "play once from the oracle's release event (sparks and embers die out); its frame 0 is the "
                        "rendered state at release after 4 revs, not the loop frame on screen, so cross 2 frames if the pop shows",
                "under": "NO frames: keep looping the under layer and multiply its alpha by max(0, 1 - t / 0.8) from release "
                         "(the effect's own 0.80 s fade, eor_kc2_fx.gd PORT 9); hide at 0.8 s"},
    },
    "binding_rule": "every segment hangs on an oracle event (channel_begin / sustain / release); no free-running timer",
    "tints": {"red": "eortint=red (the dark knight's default, R-C9-152): the haze slightly dusty-red (strength 0.30 toward (0.84, 0.46, 0.32) linear), translucent",
              "original": "eortint=original: the untinted light haze (PORT 17); sparks and embers identical on both"},
    "ribbon_recommendation": ("DROP kc2_play's 2D ribbon (src/kc2p_whirlwind.gd) when this overlay is on. It is a port of the "
                              "wwcr clean-room mint (WW-AB) -- the source R-C9-143 replaced in the Barrow -- and draws a 150-deg "
                              "TINTED ribbon (an arc, which R-C9-152 removed from this skill) plus its own sparks and scuffs that "
                              "duplicate the overlay's. Keep it behind a flag for comparison."),
    "venue_note": ("the haze colours are PORT 17's, tuned for the Barrow's 0.96 snow (light powder). On a darker arena floor "
                   "they read as a pale mist; the source's original dark-smoke colours exist if the arena wants them."),
    "source": "barrow_full/godot/scripts/eor_kc2_fx.gd (node pool) driven by barrow_full/godot/tools/render_eor_overlay.gd",
})
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)

# previews: under (2x) + body cell + over, on a mid stone grey, at three headings and three loop frames
os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
for tint in ["red", "original"]:
    tiles = []
    for d in ["S", "E", "NW"]:
        for i in [5, 22, 43]:
            bg = Image.new("RGBA", (1536, 1536), (92, 88, 84, 255))
            u = Image.open(f"{OUT}/{tint}/under/loop/under_loop_{i:03d}.png").resize((2048, 2048), Image.BICUBIC)
            bg.alpha_composite(u, (768 - 1024, 832 - 1152))
            body = Image.open(f"{PACK}/cells/eor_spin_loop/{d}/eor_spin_loop_{d}_{i % 16:02d}.png").convert("RGBA")
            bg.alpha_composite(body, (768 - 384, 832 - 448))
            bg.alpha_composite(Image.open(f"{OUT}/{tint}/over/loop/{d}/over_loop_{d}_{i:03d}.png"), (0, 0))
            tiles.append(bg.crop((256, 256, 1280, 1280)).resize((512, 512)))
    sheet = Image.new("RGBA", (1536, 1536))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % 3) * 512, (k // 3) * 512))
    sheet.convert("RGB").save(f"{OUT}/previews/eor_overlay_{tint}_S-E-NW_x_loop5-22-43.png", optimize=True)
print("manifest + previews written")
