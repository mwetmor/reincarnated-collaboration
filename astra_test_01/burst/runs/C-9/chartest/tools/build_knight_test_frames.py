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

    anims, substituted, missing = [], {}, []
    for state, cfg in man["states"].items():
        src_state = cfg.get("from")
        if src_state is None:
            missing.append(state)
            continue
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
            names = []
            for i, f in enumerate(frames):
                rel = "sprites_knight/%s/%s/%s" % (src_state, f.parent.name, f.name)
                dest = out_sprites.parent / rel
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(f, dest)
                names.append(rel)
            if borrowed:
                substituted.setdefault(state, []).append(d)
            anims.append({"name": "%s_%s" % (state, d), "fps": float(cfg["fps"]),
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

    report = {
        "note": "C-9 R-C9-61 T1 knight test skin. Written by tools/build_knight_test_frames.py.",
        "source_root": str(root), "placeholder": bool(man.get("placeholder")),
        "placeholder_note": man.get("placeholder_note", ""),
        "animations": len(anims), "textures": len(ids),
        "states_built": sorted({an["name"].rsplit("_", 1)[0] for an in anims}),
        "states_missing_from_source": missing,
        "directions_substituted_from_E": substituted,
        "keeper_cadence_used": {k: {"frames": v[0], "fps": v[1]}
                                for k, v in cad.items() if k in ("walk_E", "run_E", "idle_E")},
        "fps_per_state": {s: c["fps"] for s, c in man["states"].items()},
    }
    (PROJ / "frames" / ("%s.json" % a.out_name)).write_text(json.dumps(report, indent=1))

    print("built %d animations, %d textures -> %s" % (len(anims), len(ids), out))
    for s in sorted(substituted):
        print("   %-6s directions fed from the E column: %s" % (s, " ".join(sorted(substituted[s]))))
    if missing:
        print("   NOT BUILT (the skin falls back to idle and says so once): %s" % " ".join(missing))


if __name__ == "__main__":
    sys.exit(main())
