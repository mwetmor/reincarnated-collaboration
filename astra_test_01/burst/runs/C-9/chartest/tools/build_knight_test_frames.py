#!/usr/bin/env python3
"""C-9 R-C9-61 (T1): build the knight test skin's SpriteFrames for the ORIGINAL
cliffside route, from a folder tree plus a manifest.

WHAT THIS IS FOR.  The pipeline review (R-C9-60) recommends an AI-3D + auto-rig +
motion-library backbone whose output is a folder of rendered sprite frames.  This is
the consumer end of that pipeline: it takes the folder, and gives the game an
8-direction animation set in exactly the form the Keeper already uses, so the test
skin costs the runtime nothing new.

THE SWAP IS ONE LINE.  Everything specific to the current stand-in lives in
tools/knight_frames_manifest.json -- source_root, which states exist, what each one's
cadence is, and what to do about the ones the stand-in does not have.  When the real
8-direction set lands in runs/C-9/meshy_t1/sprites_t1/, point source_root at it, drop
placeholder to false, and re-run.  No code changes.

THE STAND-IN IS ONE DIRECTION.  paint_a is the Meshy+Astra E walk and nothing else, so
every direction is fed the same E-facing cycle and the knight does not turn.  That is
stated on the HUD and in the manifest rather than left for someone to discover: a
figure that does not turn looks exactly like a broken direction-picker, and the whole
point of the test is to see the PAINT and the MOTION, not to debug a fault that was
put there on purpose.

CADENCE COMES FROM THE KEEPER, read from frames/keeper.tres, not typed here -- the
dispatch says speeds use the Keeper's, and if hers are ever retuned the knight follows.

    python3 tools/build_knight_test_frames.py [--manifest PATH] [--out-name knight_test]
"""
import argparse
import json
import re
import shutil
import sys

import numpy as np
from PIL import Image
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent / "godot"
TOOLS = Path(__file__).resolve().parent
# source_root in the manifest is stated relative to the RUN directory (runs/C-9), not
# to tools/ -- the sets it points at are siblings of this project, not children of it.
RUN = TOOLS.parent.parent
DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]


def keeper_cadence(proj):
    """{animation name: (frame count, fps)} from the Keeper's own SpriteFrames.

    Matches EVERY animation block then filters by name.  Restricting the name inside
    the pattern lets the non-greedy body run across the blocks that do not match and
    absorb their frames -- the same trap that once reported walk_E as 332 frames over
    16 s instead of 12 over 0.58.
    """
    text = (proj / "frames" / "keeper.tres").read_text()
    body = text[text.index("[resource]"):]
    pat = r'\{"frames": \[(.*?)\], "loop": \w+, "name": &"([^"]+)", "speed": ([0-9.]+)\}'
    return {n: (f.count("ExtResource"), float(s))
            for f, n, s in re.findall(pat, body, re.S)}


# Which way a direction leads on screen. E-ward directions must lead with the face to
# the right, W-ward to the left; N and S are dead-on and no profile is right for them.
EASTWARD = {"E", "NE", "SE"}
WESTWARD = {"W", "NW", "SW"}


def needs_mirror(target_dir, source_faces):
    """Should this direction's frames be flipped?

    Matt, on the live route: "E and W are inverted." The stand-in column faces LEFT --
    checked against the Keeper's own cells, where E faces right and W faces left -- so
    it is W-facing art, and feeding it unflipped to all eight directions makes the
    knight moonwalk east. `source_faces` is stated in the manifest rather than decided
    here, because when a real per-direction set lands each direction has its own art and
    NOTHING should be mirrored: that is a property of the source, not of this code.
    """
    if source_faces not in ("E", "W"):
        return False
    if target_dir in EASTWARD:
        return source_faces == "W"
    if target_dir in WESTWARD:
        return source_faces == "E"
    return False


# THE FIGURE-HEIGHT RULE, from cliffside_B/frames/knight_fit.json: every player figure
# stands the same height on screen, 150.2135 canvas px crown-to-sole. The Keeper gets
# there as 238.75 cell px x 0.629167; the C-9 knight as 198.33 x 0.7574. It is a
# property of the SCENE, not of a character, so a new skin does not inherit another
# character's cell scale -- which is exactly the mistake that shipped: the Keeper's
# 0.629167 applied to the knight's shorter cells left him 17% short and Matt asked why
# the Keeper was larger.
FIGURE_H_CANVAS_PX = 150.2135416666667
ROW_MIN_PX = 8          # a prop is a few px wide; a torso is tens -- see body_bounds


def body_bounds(path):
    """Crown-to-sole with a thin prop (staff, haft) split off, plus the sole row.

    Their 238.75 for the Keeper is a staff-split number: her raw silhouette runs to 247
    because the staff clears her head, and a pollaxe haft does the same to the knight.
    Any height meant to be compared with theirs has to split the same way.

    ROW_MIN_PX is an absolute row width, not a fraction of the widest row. The fraction
    form (25%) clipped the crown and the soles, which are legitimately narrow, and came
    in 3.5 px low. VALIDATED against their published figure: sweeping this threshold
    over the Keeper's own idle cells, everything from 4 to 14 px lands within 1.8 px of
    238.75 and 8 px lands within 0.16 -- a broad plateau, so this is a measurement and
    not a constant fitted to one number.
    """
    a = np.asarray(Image.open(path).convert("RGBA"))[..., 3] > 8
    w = a.sum(axis=1)
    keep = np.where(w >= ROW_MIN_PX)[0]
    if not len(keep):
        return None
    return int(keep.min()), int(keep.max())


def state_fps(cfg, n_frames, cad, src_fps=None):
    """Frames per second for one animation.

    `cadence` derives it from the frame count that actually shipped -- fps = frames /
    the Keeper's stride for that gait -- instead of trusting a number typed when the
    stand-in happened to have twelve frames. That matters most for the state fed from
    ANOTHER state's frames: the run plays the WALK cells at running speed, so its fps
    depends on how many walk cells the painter delivered, which is not something this
    file can know in advance. A literal `fps` still wins if no cadence is named.
    """
    key = cfg.get("cadence")
    if key and n_frames:
        stride = cad.get("%s_E" % key)
        if stride and stride[1] > 0:
            return float(n_frames) / (stride[0] / stride[1])
    # Then whatever the SOURCE SET declares. The painter chose the tempo of a state
    # with no ground speed to answer to -- an idle -- and that choice is theirs to make,
    # not something to re-type here where it can drift from the art it describes.
    if src_fps:
        return float(src_fps)
    return float(cfg["fps"])


def find_frames(root, state, direction):
    """Accept either f_NN.png or {state}_{dir}_NN.png, and fall back to the E column
    when a direction is missing -- which is the stand-in's whole situation."""
    for d in (direction, "E"):
        p = root / state / d
        if p.is_dir():
            fs = sorted(p.glob("*.png"))
            if fs:
                return fs, (d != direction)
    return [], False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(TOOLS / "knight_frames_manifest.json"))
    ap.add_argument("--out-name", default="knight_test")
    a = ap.parse_args()

    man = json.loads(Path(a.manifest).read_text())
    root = (RUN / man["source_root"]).resolve()
    # The delivered set may ship its own manifest; read its declared cadence.
    src_man = {}
    src_man_path = root / "manifest.json"
    if src_man_path.exists():
        src_man = json.loads(src_man_path.read_text())
        print("source manifest: %s" % src_man_path)
    if not root.is_dir():
        raise SystemExit("source_root does not exist: %s" % root)
    cad = keeper_cadence(PROJ)
    out_sprites = PROJ / "sprites_knight"
    if out_sprites.exists():
        shutil.rmtree(out_sprites)

    print("source     %s%s" % (root, "   [PLACEHOLDER]" if man.get("placeholder") else ""))
    print("keeper cadence: walk %d f @ %.3f fps (%.4f s)   run %d f @ %.3f fps (%.4f s)"
          % (cad["walk_E"][0], cad["walk_E"][1], cad["walk_E"][0] / cad["walk_E"][1],
             cad["run_E"][0], cad["run_E"][1], cad["run_E"][0] / cad["run_E"][1]))

    anims, substituted, missing, mirrored = [], {}, [], {}
    borrowed_state = {}
    for state, cfg in man["states"].items():
        src_state = cfg.get("from")
        if src_state is None:
            missing.append(state)
            continue
        if src_state != state:
            borrowed_state[state] = src_state
        for d in DIRS:
            frames, borrowed = find_frames(root, src_state, d)
            if not frames:
                missing.append("%s_%s" % (state, d))
                continue
            pick = cfg.get("frames")
            if pick:
                frames = [frames[i] for i in pick if i < len(frames)]
            # Name the copy after its SOURCE, not after the animation that plays it.
            # The stand-in is ONE painted column: all eight directions and the run state
            # read the same twelve files, so naming by target shipped 200 byte-identical
            # PNGs -- 7.3 MB of a pck that is already 31 MB and already slow on a phone.
            # By source they collapse to twelve, and the SpriteFrames just references the
            # same texture from several animations. When a real per-direction set lands,
            # nothing is shared and this collapses to nothing automatically.
            flip = needs_mirror(d, man.get("source_faces", ""))
            names = []
            for i, f in enumerate(frames):
                sub = f.parent.name + ("_mirror" if flip else "")
                rel = "sprites_knight/%s/%s/%s" % (src_state, sub, f.name)
                dest = out_sprites.parent / rel
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if flip:
                        from PIL import Image
                        Image.open(f).transpose(Image.FLIP_LEFT_RIGHT).save(dest)
                    else:
                        shutil.copyfile(f, dest)
                names.append(rel)
            if flip:
                mirrored.setdefault(state, []).append(d)
            if borrowed:
                substituted.setdefault(state, []).append(d)
            anims.append({"name": "%s_%s" % (state, d),
                          "fps": state_fps(
                              cfg, len(names), cad,
                              (src_man.get("states", {}).get(src_state, {}) or {}).get("fps")),
                          "loop": bool(cfg.get("loop", True)), "frames": names})

    # ---- SpriteFrames ----
    ext, ids = [], {}
    for an in anims:
        for p in an["frames"]:
            if p not in ids:
                ids[p] = str(len(ids) + 1)
                ext.append('[ext_resource type="Texture2D" path="res://%s" id="%s"]' % (p, ids[p]))
    blocks = []
    for an in anims:
        fr = ",\n".join('{"duration": 1.0, "texture": ExtResource("%s")}' % ids[p]
                        for p in an["frames"])
        blocks.append('{"frames": [%s], "loop": %s, "name": &"%s", "speed": %.6f}'
                      % (fr, "true" if an["loop"] else "false", an["name"], an["fps"]))
    out = PROJ / "frames" / ("%s.tres" % a.out_name)
    out.write_text('[gd_resource type="SpriteFrames" load_steps=%d format=3]\n\n' % (len(ext) + 1)
                   + "\n".join(ext) + "\n\n[resource]\nanimations = ["
                   + ",\n".join(blocks) + "]\n")

    # --- measure what was built, and size it to the figure-height rule -------------
    # Measured on the IDLE frames, because that is the pose the rule is stated for --
    # their 238.75 is the Keeper's idle -- and because scale and assertion must agree
    # about which pose they mean. A walk frame mid-stride reads shorter than a standing
    # one (legs split, hip dropped, crown down while the planted sole stays), so sizing
    # on a walk frame and then asserting on a standing one builds in a disagreement.
    idle_anims = [an for an in anims if an["name"].startswith("idle")]
    uniq = sorted({p for an in (idle_anims or anims) for p in an["frames"]})
    measured_on = "idle" if idle_anims else "all states (no idle built)"
    heights, soles = [], []
    for rel in uniq:
        b = body_bounds(PROJ / rel)
        if b:
            heights.append(b[1] - b[0])
            soles.append(b[1])
    # PREFER THE SET'S DECLARED FORMAT over my own measurement of it.
    #
    # The delivered cells were RENDERED to camera.json -- px_per_m 110.556, a 1.80 m
    # figure, ground row 398 -- and the set repeats that in its own manifest. Measuring
    # them back is a check, not the source of truth, and on painted cells the check does
    # not work: the knight carries a pollaxe whose haft clears his helm, and no
    # threshold splits it. Row width slides from 229 px down to 198 with no plateau, and
    # a morphological opening hits 200 at one radius while collapsing the Keeper's own
    # figure at the next. Both instruments were tried against BOTH references and
    # neither found a stable answer, so this reports what it measured, says it includes
    # the haft, and sizes the skin from the declared format instead of inventing a
    # crown-to-sole it cannot see.
    #
    # This is also the interface that survives the next delivery: a declared pixel
    # target cannot be corrupted by a px/m convention, and the 3D skin is fitted to the
    # same one, so the two skins coincide by construction rather than by coincidence.
    declared = None
    if src_man.get("px_per_m"):
        declared = float(src_man["px_per_m"]) * float(src_man.get("character_height_m", 1.8))

    fit = {}
    if heights:
        measured = float(np.median(heights))
        body = declared if declared else measured
        fit = {"measured_on": measured_on,
               "sized_from": ("the set's declared format" if declared
                              else "measurement of the delivered cells"),
               "declared_figure_px": declared,
               "measured_figure_px_includes_props": round(measured, 3),
               "figure_h_src_px": round(body, 3),
               "figure_h_spread_px": [int(min(heights)), int(max(heights))],
               "pivot_y_src_px": float(src_man.get("ground_row_y", max(soles))),
               "measured_sole_rows": [int(min(soles)), int(max(soles))],
               "scale": FIGURE_H_CANVAS_PX / body,
               "figure_h_canvas_px": FIGURE_H_CANVAS_PX,
               "row_min_px": ROW_MIN_PX,
               "rule": "cliffside_B/frames/knight_fit.json -- every player figure is "
                       "150.2135 canvas px crown-to-sole, props split off"}

    # HUD notes. NOT gated on `placeholder`: a finished set can still be missing a
    # state's paint, and "the run is really the walk" is exactly the thing a reviewer
    # must not have to discover. The old note only appeared while the whole set was a
    # stand-in, so the moment real art landed the caveat would have gone silent while
    # remaining true.
    hud = []
    if man.get("placeholder"):
        hud.append("PLACEHOLDER: one painted column shown in all 8 directions "
                   "-- the knight does not turn")
    for st, src in sorted(borrowed_state.items()):
        hud.append(man["states"][st].get(
            "hud_note", "%s = %s frames (paint pending)" % (st, src)))
    for st, cfg in sorted(man["states"].items()):
        if cfg.get("from") is None:
            hud.append(cfg.get("hud_note", "no %s (paint pending)" % st))

    report = {
        "note": "C-9 R-C9-61 T1 knight test skin. Written by tools/build_knight_test_frames.py.",
        "source_root": str(root), "placeholder": bool(man.get("placeholder")),
        "placeholder_note": man.get("placeholder_note", ""),
        "animations": len(anims), "textures": len(ids),
        "states_built": sorted({an["name"].rsplit("_", 1)[0] for an in anims}),
        "states_missing_from_source": missing,
        "directions_substituted_from_E": substituted,
        "source_faces": man.get("source_faces", ""),
        "directions_mirrored": mirrored,
        "keeper_cadence_used": {k: {"frames": v[0], "fps": v[1]}
                                for k, v in cad.items() if k in ("walk_E", "run_E", "idle_E")},
        "fps_per_state": {s: c["fps"] for s, c in man["states"].items()},
        "fit": fit,
        "source_manifest": {k: v for k, v in src_man.items() if k != "states"} if src_man else {},
        "source_state_fps": {k: v.get("fps") for k, v in
                             (src_man.get("states", {}) or {}).items()},
        "hud_notes": hud,
        "states_from_another_state": borrowed_state,
    }
    (PROJ / "frames" / ("%s.json" % a.out_name)).write_text(json.dumps(report, indent=1))

    print("built %d animations, %d textures -> %s" % (len(anims), len(ids), out))
    if fit:
        print("   figure %.2f cell px (%s) -> scale %.6f for %.2f canvas px; pivot y %.0f"
              % (fit["figure_h_src_px"], fit["sized_from"], fit["scale"],
                 fit["figure_h_canvas_px"], fit["pivot_y_src_px"]))
        print("   cross-check: measured %.1f px (spread %s) INCLUDING the painted haft; "
              "soles %s vs declared ground row %.0f"
              % (fit["measured_figure_px_includes_props"], fit["figure_h_spread_px"],
                 fit["measured_sole_rows"], fit["pivot_y_src_px"]))
    for s in sorted(substituted):
        print("   %-6s fed from the fallback column: %s" % (s, " ".join(sorted(substituted[s]))))
    for s in sorted(mirrored):
        print("   %-6s MIRRORED (source faces %s): %s"
              % (s, man.get("source_faces", "?"), " ".join(sorted(mirrored[s]))))
    for n in hud:
        print("   HUD: %s" % n)
    if missing:
        print("   NOT BUILT (the skin falls back to idle and says so once): %s" % " ".join(missing))


if __name__ == "__main__":
    sys.exit(main())
