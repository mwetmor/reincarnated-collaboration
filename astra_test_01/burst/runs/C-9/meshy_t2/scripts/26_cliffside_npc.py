#!/usr/bin/env python3
"""C-9 meshy_t2 step 20: install the manticore as an NPC in the 2D cliffside.

    python3 scripts/26_cliffside_npc.py [--app ../cliffside_B_app]

Copies the 352 painted frames into the Godot project, writes a SpriteFrames
resource, an NPC script and a scene, and patches scenes/cliffside.tscn to
instance it. Idempotent: re-running replaces its own files and leaves the rest
of the scene alone.

SCALE. The keeper's AnimatedSprite2D is offset (-256, -400) at scale
0.629167, and the manticore takes THE SAME SCALE -- that is the whole point of
having rendered it at the knight's px/m rather than at his pixel height. The
creature is 132 px tall in the 512 frame against the knight's 198, so at one
shared scale it arrives on screen at its true relative size: about 83 px to
the top of the man's head against the player's 125. Nothing is fitted by eye.

The OFFSET is -398, not the keeper's -400. My ground row is 398 by
construction (08_render.py solves the aim height for it), so -398 puts the
pivot exactly on the row the feet were rendered to stand on. Two pixels, but
they are two pixels of the creature floating.

SPEED. The scene moves a CharacterBody2D in node pixels per second, and the
sprite is drawn at 0.629167, so the world is 110.185 * 0.629167 = 69.33 px per
metre on screen. The walk was measured at 0.933 m/s with 1.9 mm of foot slide,
so the node speed that keeps those feet planted is 0.933 * 69.33 = 64.7 px/s.
It is NOT the player's 247 px/s: the manticore's stride is 0.75 m over a 0.8 s
cycle and the knight's game cadence is nothing like it. Driving the NPC at the
player's speed would put 4x of slide under a creature whose feet were
carefully planted; the number stays measured and the pace is a design call.

FPS per state is each clip's own: idle 5.0, walk 15.0, run 19.05, attack
17.14. Those are the cadences the plants were solved at.
"""
import argparse, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}
LOOP = {"idle": True, "walk": True, "run": True, "attack": False}
SPRITE_SCALE = 0.629166666667          # the keeper's, deliberately shared
SOLE_ROW = 398                         # this render's ground row
PX_PER_M = 110.1852


def build_tres(app, rel):
    ext, anims, i = [], [], 0
    for clip in sorted(CLIPS):
        for d in DIRS:
            ids = []
            for f in range(CLIPS[clip]):
                i += 1
                ext.append('[ext_resource type="Texture2D" '
                           'path="res://%s/%s/%s/%s_%s_%02d.png" id="%d"]'
                           % (rel, clip, d, clip, d, f, i))
                ids.append(i)
            frames = ",\n".join('{"duration": 1.0, "texture": ExtResource("%d")}' % k
                                for k in ids)
            anims.append('{"frames": [%s], "loop": %s, "name": &"%s_%s", '
                         '"speed": %s}'
                         % (frames, "true" if LOOP[clip] else "false", clip, d,
                            FPS[clip]))
    return ('[gd_resource type="SpriteFrames" load_steps=%d format=3]\n\n%s\n\n'
            '[resource]\nanimations = [%s]\n'
            % (i + 1, "\n".join(ext), ",\n".join(anims)))


NPC_GD = '''extends CharacterBody2D
## C-9 T2 manticore NPC -- Rochester Bestiary, c.1230.
##
## Walks a CLOSED LOOP of eight legs and idles at two opposite corners. Eight
## authored directions, never mirrored: the sprites were rendered per
## direction, so a mirrored W would put the man\'s parting and the tail\'s curve
## on the wrong side.
##
## THE LOOP IS EIGHT EQUAL LEGS, ONE PER DIRECTION, so it closes exactly:
## the eight unit compass vectors sum to zero. A horizontal there-and-back
## showed only E and W, which is half the painted work invisible.
##
## SPEED is measured, not chosen. The walk cycle plants its feet at 0.933 m/s
## (1.9 mm of residual slide), and the scene draws this sprite at 69.33 px per
## metre, so 64.7 px/s is the only speed at which the feet do not skate. The
## player walks at 247 px/s; this creature is not the player.
const DIRECTIONS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
@export var walk_speed: float = 64.7
@export var waypoints: PackedVector2Array = PackedVector2Array()
@export var pause_at: PackedInt32Array = PackedInt32Array([0, 4])
@export var pause_seconds: float = 1.5
## Advance when the body stops moving. The cliffside\'s floor collision is
## authored for the PLAYER, and a leg laid across it pins the NPC: measured,
## it walked east from x=2680, jammed at x=3023 and pushed into that wall for
## the rest of the run at full speed with the animation playing. A path that
## can only advance when it REACHES a waypoint cannot recover from never
## reaching one.
@export var stuck_speed_frac: float = 0.25
@export var stuck_seconds: float = 0.6

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
var _i: int = 0
var _pausing: float = 0.0
var _facing: String = "S"
var _state: String = "idle"
var _stuck: float = 0.0
var _last_pos: Vector2 = Vector2.ZERO
var _skipped: int = 0

func _ready() -> void:
	if waypoints.size() < 2:
		# a small octagon around the spawn, so the node is still usable if no
		# path was authored on the instance
		var p := global_position
		var L := 90.0
		var d := 0.70710678
		var steps := [Vector2(0, 1), Vector2(d, d), Vector2(1, 0), Vector2(d, -d),
			Vector2(0, -1), Vector2(-d, -d), Vector2(-1, 0), Vector2(-d, d)]
		var wp := PackedVector2Array()
		for st in steps:
			wp.append(p)
			p += st * L
		waypoints = wp
	_i = 0
	_pausing = pause_seconds
	_last_pos = global_position
	_play()

func _physics_process(delta: float) -> void:
	if _pausing > 0.0:
		_pausing -= delta
		velocity = Vector2.ZERO
		_set_state("idle")
		move_and_slide()
		return
	var target: Vector2 = waypoints[(_i + 1) % waypoints.size()]
	var to_target := target - global_position
	if to_target.length() < 8.0:
		_arrive()
		return
	var dir := to_target.normalized()
	velocity = dir * walk_speed
	_facing = DIRECTIONS[posmod(roundi(dir.angle() / (PI / 4.0)) + 6, 8)]
	_set_state("walk")
	move_and_slide()
	var advanced := global_position.distance_to(_last_pos)
	_last_pos = global_position
	if advanced < walk_speed * delta * stuck_speed_frac:
		_stuck += delta
		if _stuck >= stuck_seconds:
			_skipped += 1
			_arrive()
	else:
		_stuck = 0.0

func _arrive() -> void:
	_i = (_i + 1) % waypoints.size()
	_stuck = 0.0
	_last_pos = global_position
	if _i in pause_at:
		_pausing = pause_seconds
	velocity = Vector2.ZERO
	_set_state("idle")
	move_and_slide()

func _set_state(s: String) -> void:
	if s == _state and sprite.animation == "%s_%s" % [_state, _facing]:
		return
	_state = s
	_play()

func _play() -> void:
	var want := "%s_%s" % [_state, _facing]
	if sprite.sprite_frames != null and sprite.sprite_frames.has_animation(want):
		sprite.play(want)
'''



# The capture harness lives here too, because cliffside_B_app is an
# UNTRACKED tree -- 134 MB of sprites and parallax that is not committed --
# so a file written straight into it has no home in the repo and would be
# lost to the next machine. One tracked installer regenerates the NPC and
# its harness together.
CAPTURE_GD = 'extends Node\n## C-9 T2 capture harness: films the manticore NPC in the cliffside.\n##\n## Two modes, chosen by the T2_MODE environment variable:\n##   film    follow the NPC for N frames and write a PNG per frame\n##   stills  hold the NPC still and step it through all eight directions,\n##           one PNG each, so the sheet can be read direction by direction\n##\n## The viewport is grabbed AFTER frame_post_draw; grabbing in _process gives\n## the previous frame, which on a moving camera is a frame of lag and on the\n## stills pass is the WRONG DIRECTION entirely.\nconst DIRECTIONS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]\nvar _out: String = ""\nvar _mode: String = "film"\nvar _n: int = 0\nvar _max: int = 240\nvar _npc: Node2D = null\nvar _cam: Camera2D = null\nvar _dir_i: int = 0\nvar _hold: int = 0\n\nfunc _ready() -> void:\n\t_out = OS.get_environment("T2_OUT")\n\tif _out == "":\n\t\t_out = "res://_t2_capture"\n\t_mode = OS.get_environment("T2_MODE")\n\tif _mode == "":\n\t\t_mode = "film"\n\tvar mx := OS.get_environment("T2_FRAMES")\n\tif mx != "":\n\t\t_max = int(mx)\n\tDirAccess.make_dir_recursive_absolute(_out)\n\tawait get_tree().process_frame\n\t_npc = get_tree().get_root().find_child("ManticoreNPC", true, false)\n\tif _npc == null:\n\t\tpush_error("ManticoreNPC not found")\n\t\tget_tree().quit(1)\n\t\treturn\n\t_cam = Camera2D.new()\n\t_npc.add_child(_cam)\n\t_cam.zoom = Vector2(2.4, 2.4) if _mode == "stills" else Vector2(1.6, 1.6)\n\t_cam.offset = Vector2(0, -60)\n\t_cam.make_current()\n\tif _mode == "stills":\n\t\t# freeze the patrol so the creature holds its ground while the\n\t\t# direction is stepped: otherwise each still is taken at a different\n\t\t# place on the path and they cannot be compared\n\t\t_npc.set("walk_speed", 0.0)\n\t\t_npc.set("pause_seconds", 1e9)\n\tRenderingServer.frame_post_draw.connect(_grab)\n\nfunc _grab() -> void:\n\tif _mode == "stills":\n\t\t_hold += 1\n\t\tif _hold < 6:\n\t\t\treturn\n\t\t_hold = 0\n\t\tif _dir_i >= DIRECTIONS.size():\n\t\t\tget_tree().quit()\n\t\t\treturn\n\t\tvar d: String = DIRECTIONS[_dir_i]\n\t\tvar img := get_viewport().get_texture().get_image()\n\t\timg.save_png("%s/idle_%s.png" % [_out, d])\n\t\t_dir_i += 1\n\t\tif _dir_i < DIRECTIONS.size():\n\t\t\t# Set the NPC\'s OWN facing, do not call play() on the sprite.\n\t\t\t# The NPC re-plays "idle_" + _facing every physics frame, so an\n\t\t\t# external play() is overwritten before the next draw and all\n\t\t\t# eight stills came out facing S.\n\t\t\t_npc.set("_facing", DIRECTIONS[_dir_i])\n\t\treturn\n\tvar im := get_viewport().get_texture().get_image()\n\tim.save_png("%s/f_%04d.png" % [_out, _n])\n\t_n += 1\n\tif _n >= _max:\n\t\tget_tree().quit()\n'

CAPTURE_TSCN = '[gd_scene load_steps=3 format=3]\n\n[ext_resource type="PackedScene" path="res://scenes/cliffside.tscn" id="Cliff"]\n[ext_resource type="Script" path="res://scripts/t2_capture.gd" id="Cap"]\n\n[node name="T2Capture" type="Node"]\n\n[node name="Cliffside" parent="." instance=ExtResource("Cliff")]\n\n[node name="Capture" type="Node" parent="."]\nscript = ExtResource("Cap")\n'


def npc_tscn(frames_path, script_path):
    return ('[gd_scene load_steps=4 format=3]\n\n'
            '[ext_resource type="Script" path="%s" id="NpcScript"]\n'
            '[ext_resource type="SpriteFrames" path="%s" id="NpcFrames"]\n\n'
            '[sub_resource type="CapsuleShape2D" id="NpcFeet"]\n'
            'radius = 26.0\nheight = 34.0\n\n'
            '[node name="ManticoreNPC" type="CharacterBody2D"]\n'
            'script = ExtResource("NpcScript")\n'
            'motion_mode = 1\ncollision_layer = 1\ncollision_mask = 1\n\n'
            '[node name="AnimatedSprite2D" type="AnimatedSprite2D" '
            'parent="."]\n'
            'sprite_frames = ExtResource("NpcFrames")\n'
            'animation = &"idle_S"\nautoplay = "idle_S"\n'
            'centered = false\noffset = Vector2(-256, -%d)\n'
            'scale = Vector2(%s, %s)\n\n'
            '[node name="CollisionShape2D" type="CollisionShape2D" parent="."]\n'
            'shape = SubResource("NpcFeet")\n'
            % (script_path, frames_path, SOLE_ROW, SPRITE_SCALE, SPRITE_SCALE))


def octagon(origin, leg):
    """Eight equal legs, one per compass direction, in the order S SE E NE N
    NW W SW. The eight unit compass vectors sum to zero, so a loop of equal
    legs closes EXACTLY -- no fudge waypoint and no drift back to the start."""
    d = 0.70710678
    steps = [(0, 1), (d, d), (1, 0), (d, -d), (0, -1), (-d, -d), (-1, 0), (-d, d)]
    pts, p = [], list(origin)
    for sx, sy in steps:
        pts.append((round(p[0], 2), round(p[1], 2)))
        p[0] += sx * leg
        p[1] += sy * leg
    return pts


def patch_scene(tscn, npc_scene_path, pos, wps, pause_at):
    src = open(tscn).read()
    marker = "; C-9 T2 manticore NPC"
    # Strip EVERY existing ManticoreNPC block, by node header rather than by
    # marker. A first version put the marker on the node line itself; cutting
    # at the marker then sliced mid-line and left a headless node behind, and
    # the next run appended a second one. Re-running a patcher has to be able
    # to clean up after a patcher that was wrong.
    out, skip = [], False
    for line in src.split("\n"):
        if line.startswith('[node name="ManticoreNPC"'):
            skip = True
            continue
        if skip:
            if line.startswith("[") or line.startswith(";"):
                skip = False
            else:
                continue
        if line.strip() == marker:
            continue
        out.append(line)
    src = "\n".join(out).rstrip("\n") + "\n"
    ext = ('[ext_resource type="PackedScene" path="%s" id="ManticoreNPC"]'
           % npc_scene_path)
    if ext not in src:
        lines = src.split("\n")
        last = max(i for i, l in enumerate(lines) if l.startswith("[ext_resource"))
        lines.insert(last + 1, ext)
        src = "\n".join(lines)
    # the marker is its OWN line: a .tscn comment is ";" at the START of a
    # line, so appending it to the node declaration would make the node header
    # unparseable rather than commented.
    flat = ", ".join("%s, %s" % (x, y) for x, y in wps)
    node = ('\n%s\n[node name="ManticoreNPC" parent="Actors" '
            'instance=ExtResource("ManticoreNPC")]\n'
            'position = Vector2(%s, %s)\n'
            'waypoints = PackedVector2Array(%s)\n'
            'pause_at = PackedInt32Array(%s)\n'
            % (marker, pos[0], pos[1], flat,
               ", ".join(str(i) for i in pause_at)))
    if not src.endswith("\n"):
        src += "\n"
    open(tscn, "w").write(src + node)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=os.path.join(os.path.dirname(ROOT),
                                                  "cliffside_B_app"))
    ap.add_argument("--x", type=float, default=2680.0)
    ap.add_argument("--y", type=float, default=2407.32)
    # leg length of the octagon; the loop spans about 2.4 legs each way
    ap.add_argument("--leg", type=float, default=90.0)
    args = ap.parse_args()
    app = os.path.abspath(args.app)
    rel = "sprites_manticore"
    dst = os.path.join(app, rel)
    plant = json.load(open(os.path.join(ROOT, "work", "plant.json")))
    global FPS
    FPS = {c: round(plant["clips"][c]["fps"], 4) for c in CLIPS}

    n = 0
    for clip in CLIPS:
        for d in DIRS:
            sd = os.path.join(ROOT, "sprites_t2", clip, d)
            dd = os.path.join(dst, clip, d)
            os.makedirs(dd, exist_ok=True)
            for f in range(CLIPS[clip]):
                name = "%s_%s_%02d.png" % (clip, d, f)
                shutil.copy(os.path.join(sd, name), os.path.join(dd, name))
                n += 1
    print("copied %d frames -> %s" % (n, os.path.relpath(dst, app)))

    tres = os.path.join(app, "frames", "manticore.tres")
    open(tres, "w").write(build_tres(app, rel))
    print("wrote", os.path.relpath(tres, app), "fps", FPS)

    gd = os.path.join(app, "scripts", "manticore_npc.gd")
    open(gd, "w").write(NPC_GD)
    sc = os.path.join(app, "scenes", "manticore_npc.tscn")
    open(sc, "w").write(npc_tscn("res://frames/manticore.tres",
                                 "res://scripts/manticore_npc.gd"))
    print("wrote", os.path.relpath(gd, app), "and", os.path.relpath(sc, app))

    cg = os.path.join(app, "scripts", "t2_capture.gd")
    open(cg, "w").write(CAPTURE_GD)
    cs = os.path.join(app, "scenes", "t2_capture.tscn")
    open(cs, "w").write(CAPTURE_TSCN)
    print("wrote", os.path.relpath(cg, app), "and", os.path.relpath(cs, app))

    wps = octagon((args.x, args.y), args.leg)
    patch_scene(os.path.join(app, "scenes", "cliffside.tscn"),
                "res://scenes/manticore_npc.tscn",
                (args.x, args.y), wps, (0, 4))
    xs = [w[0] for w in wps]; ys = [w[1] for w in wps]
    print("patched scenes/cliffside.tscn: octagon at (%.0f, %.0f), leg %.0f px, "
          "extent x %.0f-%.0f y %.0f-%.0f, idle at waypoints 0 and 4"
          % (args.x, args.y, args.leg, min(xs), max(xs), min(ys), max(ys)))
    px_per_m_screen = PX_PER_M * SPRITE_SCALE
    print("scale %.6f shared with the keeper; screen world %.2f px/m; "
          "walk %.2f m/s -> %.1f px/s"
          % (SPRITE_SCALE, px_per_m_screen, plant["clips"]["walk"]["measured_speed_m_s"],
             plant["clips"]["walk"]["measured_speed_m_s"] * px_per_m_screen))


if __name__ == "__main__":
    main()
