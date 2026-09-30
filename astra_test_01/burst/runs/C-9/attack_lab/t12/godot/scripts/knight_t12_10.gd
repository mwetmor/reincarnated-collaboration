extends CharacterBody3D
## C-9 R-C9-66 — a character in the true-3D cliffside, at the WORLD CAMERA'S REAL ANGLE.
##
## Matt, R-C9-68, verbatim: "Use the real 53 degree angle." So the character is a real
## object seen by the player_lock camera at its own 52.95 deg pitch -- it occludes and
## is occluded per pixel, the lights reach it, and it turns as it walks, with no
## eight-direction set to pick from and no flat card to sort.
##
## The alternative that was going to be built alongside -- rendering the character by
## its own camera at the 19.77 deg the approved art is PAINTED at, then compositing it
## as a card -- is dropped on that ruling. Worth recording what it would have cost, in
## case the question returns: a composited card is flat, so it carries ONE depth for the
## whole figure, and a rock that should hide a walker's legs while leaving his head in
## view has to hide all of him or none. Real 3D has no such problem. What real 3D costs
## instead is that the world camera sees a figure from 33 degrees higher than any
## painted frame contains -- helm crowns and shoulder tops nobody has drawn.
##
## THE OCCUPANT IS A STAND-IN. R-C9-69 replaces it with a Norse barbarian whose sheet is
## being painted now. The Meshy knight is here to check scale, ground contact, occlusion
## and light, and is deliberately not polished.

const PPM := 100.617553710938
const CHAR_LAYER := 4
const WALK_PX_S := 247.0          # parallax.json movement, the Keeper's own
const RUN_PX_S := 494.0
# LAB ONLY (drax T12_11 before/after): the T12_10 knight fb35d9d0, the character file from KNIGHT_CHARACTER
var CHARACTER: String = OS.get_environment("KNIGHT_CHARACTER") if OS.has_environment("KNIGHT_CHARACTER") else "res://data/character.json"
# preloaded rather than referenced by class_name: a global class is only visible once the
# editor's class cache has been rebuilt, and an exported app that loads before that has a
# character with no gear and no error anybody sees.
const CharGear := preload("res://scripts/gear.gd")
const FootLock := preload("res://scripts/foot_lock.gd")
const LINE_PX := 1.1

## THE SLOT IS SWAPPABLE, and nothing below names the knight.
##
## Who stands here is data/character.json: a GLB path, the four clip ROLES the scene
## drives, and an optional hand prop. The T8 barbarian arrives as a textured, rigged GLB
## with idle/walk/run/attack, so he replaces one string in that file. The scale he stands
## at is data/figure.json's measured 1.25178 -- a property of this painted world's metric,
## not of the model -- so it carries across the swap unchanged.
var cfg := {}
var _roles := {}

var right := Vector3.RIGHT
var up := Vector3.UP
var fwd := Vector3.FORWARD
var facing := "S"
var state := "idle"

var _rig: Node3D
var _skel: Skeleton3D
var _anim: AnimationPlayer
var _mesh: MeshInstance3D
var _outline: MeshInstance3D
var _pollaxe: Node3D
var _attach: BoneAttachment3D
var _socket_basis := Basis()
var _socket_offset := Vector3.ZERO
var _clip := ""
var _clip_len := {}
var _figure_scale := 1.0
var _forward_axis := Vector3(0, 0, -1)
var gear := {}
var gear_stack := 0
var _tree: AnimationTree
var _walk_len := 1.0
var _run_len := 1.0
var _phase_aligned := false
## A/B SWITCH, for measurement only. Off = the pre-sync behaviour: run weight read
## LINEARLY off speed (what a BlendSpace1D's own point mapping does), both clips at their
## authored rate, no phase alignment. It exists because the "10.2 mm median, one frame at
## 219 mm" recorded for the pre-sync build was measured with an instrument that counted
## airborne frames and tested only one end of each pair -- so those numbers cannot be
## compared with today's. One instrument has to measure both builds. Default ON.
var sync_group := true
## How fast the locked cycle length may change. Nothing else in the rig is rate-limited.
## SWEPT, not chosen -- the probe takes --tau= and the two named cases disagree, so the
## value is the one that minimises the WORST frame across both (the sweep is deterministic,
## so these are reproducible; what shifts with tau is which pairs qualify as planted):
##     tau     run-stop worst    crossover worst    joint    crossover planted of 84
##     off       218.5 mm          142.3 mm        218.5          1
##     0.08      172.3              75.5           172.3         19
##     0.15      138.1              55.4           138.1         16
##     0.18      126.9             113.2           126.9          9
##     0.20      119.6             104.7           119.6         13   <-- lowest joint
##     0.25      101.1             180.9           180.9         15
##     0.40       64.7             190.3           190.3         16
## Longer helps the stop monotonically and hurts the crossover past 0.15.
var CYCLE_TAU_S := 0.20
var _cycle_len := 0.0
var _prev_w := 0.0
## THE ARMED UPPER LAYER (armed-speed split) -- see _upper_spec
var _upper_on := false
var _walk_len_u := 1.0
var _run_len_u := 1.0
var _walk_contact_u := 0.0
var _run_contact_u := 0.0
var _prev_a := 0.0
var _w_cur := 0.0
var _w_init := false
var _walk_contact := 0.0
var _run_contact := 0.0
var _speed := 0.0
var _move_dir := Vector2(0, 1)
var _yaw_cur := 0.0
var _yaw_init := false
var _layer_on := false
var _attack_t := 0.0
var _strikes: Array[String] = []
var _blocking := false
## BLOCK: raise -> hold -> lower. "off" | "raise" | "hold" | "lower"
var _block_phase := "off"
var _block_t0 := 0.0          # where the raise starts in the clip -- measured at load
var _block_peak := 0.0        # where it peaks -- measured at load
var _block_rate := 1.0        # clip seconds per real second while raising / lowering
var _block_lower_rate := 1.0
## FOOT LOCK -- see scripts/foot_lock.gd
var _foot_lock: Node = null
var _strike_anim := ""        # the playing strike's AnimationNodeAnimation, e.g. "a_slash"
var _strike_len := 0.0
var _strike_out_sent := false
var _rel_fire := {}             # strike key -> fired this frame (the clip position is stale until the tree runs)
var _was_moving := false
var _block_w := 0.0
var _strafe_w := 0.0
var _block_req_frame := -1
var _armed := false
var _root_speeds := {}
var _recentred := {}
var _manifest_px_s := {}
var _root_dirs := {}
var _strafing := false
var _strafe_side := "l"


func setup(r: Vector3, u: Vector3, f: Vector3, figure_scale: float) -> void:
	right = r
	up = u
	fwd = f
	_figure_scale = figure_scale


func _ready() -> void:
	# He stands ON the terrain layer and is not ON it: CliffWorld.ground_at masks to the
	# terrain, so his own body can never answer the question "where is the ground".
	collision_layer = 1
	collision_mask = CliffWorld.TERRAIN_BIT
	var shape := CollisionShape3D.new()
	var cap := CapsuleShape3D.new()
	cap.height = float(cfg.get("model_height_m", 1.8)) * _figure_scale
	cap.radius = 0.35 * _figure_scale
	shape.shape = cap
	shape.position = Vector3(0, cap.height * 0.5, 0)
	add_child(shape)

	cfg = _read_cfg()
	var model := String(cfg.get("model", "res://models/knight_t3.glb"))
	if not ResourceLoader.exists(model):
		push_error("character: no model at %s" % model)
		return
	_rig = (load(model) as PackedScene).instantiate()
	_rig.scale = Vector3.ONE * _figure_scale
	add_child(_rig)
	_skel = _find(_rig, "Skeleton3D") as Skeleton3D
	_mesh = _find(_rig, "MeshInstance3D") as MeshInstance3D
	_anim = _find(_rig, "AnimationPlayer") as AnimationPlayer
	if _anim != null:
		_anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
		for n in _anim.get_animation_list():
			_clip_len[n] = _anim.get_animation(n).length
	_manifest_px_s = _read_manifest_speeds()
	_recentred = _recentre_all()     # BEFORE the de-root: it tests the clips as shipped
	_root_speeds = _deroot_all()
	var fa = cfg.get("forward_axis", null)
	if fa != null:
		_forward_axis = Vector3(float(fa[0]), 0.0, float(fa[2])).normalized()
	_bind_roles()
	# A walk that stops at the end of its 25 frames is not a walk. glTF carries no loop
	# flag, so Godot imports every clip as one-shot and the ones that cycle are named here.
	_loop_locomotion()
	_style()
	_add_outline()
	_read_socket()
	_add_pollaxe()
	_set_layer(_rig, CHAR_LAYER)
	_build_gear()
	_build_anim_tree()
	_add_foot_lock()
	play(_roles.get("idle", ""))
	_drive()


func _build_anim_tree() -> void:
	"""The shield-carry arm layer, as an AnimationTree Blend2 filtered to four bones.

	`shield_carry_L` is ONE FRAME and it carries tracks for all 24 bones -- measured,
	tools/probe_gear2.gd -- so it is a whole static body pose, not an arm pose. Blended
	unfiltered it would freeze him mid-stride. The filter is what makes it an arm layer,
	and the four paths are taken from the clip's OWN track list rather than composed from
	bone names, so a path that does not exist in the clip cannot be filtered by accident."""
	var spec: Dictionary = cfg.get("arm_layer_armed", _layer_spec())
	var action := String(spec.get("action", ""))
	if _anim == null or action == "" or not _clip_len.has(action):
		return
	var want: Array = spec.get("bones", [])
	var ca := _anim.get_animation(action)
	var bt := AnimationNodeBlendTree.new()

	# LOCOMOTION IS A NORMALIZED-PHASE SYNC GROUP, not a blend space.
	#
	# A BlendSpace1D got the pose right and the FEET wrong: the walk is 25 frames and the
	# run is 16, so at any mixed weight the two clips are at unrelated phases and the
	# blended foot is part-stance part-swing. That is what the 219 mm frame at the
	# walk-run crossover was. Godot's `sync` keeps both clips RUNNING; it does not make
	# their cycles the same length, which is the thing that matters.
	#
	# So each locomotion clip gets an AnimationNodeTimeScale, and both are driven every
	# frame to len_clip / len_blended with len_blended = lerp(walk_len, run_len, w). Both
	# cycles then take the same wall-clock time AT EVERY WEIGHT, not only during the
	# crossover -- which means their relative phase is CONSTANT, and aligning it once at
	# start is enough to keep it aligned for the run of the program.
	#
	# Built as explicit Blend2s rather than a blend space because AnimationNodeTimeScale is
	# an AnimationNode and a blend point has to be an AnimationRootNode: the two-stage
	# blend below reproduces a three-point 1D space exactly and leaves every parameter at a
	# path this script can address.
	var tr: Dictionary = cfg.get("transitions", {})
	var wsp := walk_px_s()
	var rsp := run_px_s()
	var a_idle := AnimationNodeAnimation.new()
	a_idle.animation = String(_roles.get("idle", "idle"))
	var a_walk := AnimationNodeAnimation.new()
	a_walk.animation = String(_roles.get("walk", "walk"))
	var a_run := AnimationNodeAnimation.new()
	a_run.animation = String(_roles.get("run", "run"))
	var ts_walk := AnimationNodeTimeScale.new()
	var ts_run := AnimationNodeTimeScale.new()
	var seek_run := AnimationNodeTimeSeek.new()
	var bl_iw := AnimationNodeBlend2.new()
	var bl_wr := AnimationNodeBlend2.new()
	bl_iw.sync = true
	bl_wr.sync = true
	_walk_len = float(_clip_len.get(a_walk.animation, 1.0))
	_run_len = float(_clip_len.get(a_run.animation, 1.0))

	# THE STRIKES ARE ONE-SHOTS OVER THE TOP, not blend points. They are not speeds, they
	# interrupt, and each has to fade in and back out to whatever he was doing.
	#
	# THREE SEPARATE ONE-SHOTS, not one node re-pointed before each fire. Re-pointing works
	# -- an AnimationNodeAnimation does re-pose when its `animation` property is mutated on
	# a live tree, measured in tools/probe_armed.gd -- but a node re-pointed WHILE its own
	# one-shot is fading out changes the clip under the fade, and "is a strike running" then
	# has no single answer. Three nodes cost nothing when idle: a one-shot that is not
	# active passes input 0 through untouched.
	var fin := float(tr.get("attack_fade_in_s", 0.10))
	var fout := float(tr.get("attack_fade_out_s", 0.25))
	# BUILT FROM THE UNION OF BOTH CLIP SETS, not from the roles live right now. The graph
	# is constructed once; if the chop and bash nodes were built from the unarmed roles --
	# which is the state at _ready, because the gear stack starts at 0 -- they would never
	# exist and picking up the axe could not create them. Whether a strike may FIRE is a
	# question for try_strike; whether it has a node is not.
	var am: Dictionary = cfg.get("clips_armed", {})
	var strikes := {"slash": String(am.get("attack", _roles.get("attack", "attack"))),
					"chop": String(am.get("chop", "")),
					"bash": String(am.get("bash", ""))}

	var b2 := AnimationNodeBlend2.new()
	b2.filter_enabled = true
	var filtered := 0
	for i in ca.get_track_count():
		var pth: NodePath = ca.track_get_path(i)
		if want.has(String(pth.get_concatenated_subnames())):
			b2.set_filter_path(pth, true)
			filtered += 1
	var carry := AnimationNodeAnimation.new()
	carry.animation = action

	# THE BLOCK IS A HOLD, so it is a Blend2 this script drives and not a one-shot: a
	# one-shot runs for its clip's length and cannot be held for as long as a key is down.
	# Full body, above the guard and below the strikes.
	var blk := AnimationNodeBlend2.new()
	# NOT SYNCED. With sync on, a Blend2 advances its input at zero weight, so Block1 ran to
	# its last frame while nobody was blocking and every block showed that frame: the raise
	# never played (attack_lab, 2026-09-29: a_block parked at 3.500 s of 3.500). The block is
	# now DRIVEN -- seeked, played, pinned and reversed by this script -- so it must not also
	# be advancing on its own.
	blk.sync = false
	var a_block := AnimationNodeAnimation.new()
	a_block.animation = String(am.get("block", ""))
	var ts_block := AnimationNodeTimeScale.new()
	var seek_block := AnimationNodeTimeSeek.new()

	bt.add_node("a_idle", a_idle, Vector2(0, -160))
	bt.add_node("a_walk", a_walk, Vector2(0, -60))
	bt.add_node("a_run", a_run, Vector2(0, 40))
	bt.add_node("ts_walk", ts_walk, Vector2(180, -60))
	bt.add_node("ts_run", ts_run, Vector2(180, 40))
	bt.add_node("seek_run", seek_run, Vector2(300, 40))
	bt.add_node("bl_iw", bl_iw, Vector2(430, -110))
	bt.add_node("bl_wr", bl_wr, Vector2(560, -40))
	bt.add_node("carry", carry, Vector2(560, 220))
	bt.add_node("blend", b2, Vector2(700, 60))
	bt.add_node("a_block", a_block, Vector2(700, 260))
	bt.add_node("ts_block", ts_block, Vector2(760, 260))
	bt.add_node("seek_block", seek_block, Vector2(820, 260))
	bt.add_node("blk", blk, Vector2(860, 100))
	bt.connect_node("ts_walk", 0, "a_walk")
	bt.connect_node("ts_run", 0, "a_run")
	bt.connect_node("seek_run", 0, "ts_run")
	bt.connect_node("bl_iw", 0, "a_idle")
	bt.connect_node("bl_iw", 1, "ts_walk")
	bt.connect_node("bl_wr", 0, "bl_iw")
	bt.connect_node("bl_wr", 1, "seek_run")
	# THE ARMED UPPER BODY: the same idle/walk/run blend, on the armed gait clips, locked to
	# the legs' cycle by its own time scales and seeks. `up` takes the spine and arms from it.
	var a_idle_u := AnimationNodeAnimation.new()
	a_idle_u.animation = a_idle.animation
	var a_walk_u := AnimationNodeAnimation.new()
	a_walk_u.animation = a_walk.animation
	var a_run_u := AnimationNodeAnimation.new()
	a_run_u.animation = a_run.animation
	var ts_walk_u := AnimationNodeTimeScale.new()
	var ts_run_u := AnimationNodeTimeScale.new()
	var seek_walk_u := AnimationNodeTimeSeek.new()
	var seek_run_u := AnimationNodeTimeSeek.new()
	var bl_iw_u := AnimationNodeBlend2.new()
	var bl_wr_u := AnimationNodeBlend2.new()
	bl_iw_u.sync = true
	bl_wr_u.sync = true
	var up := AnimationNodeBlend2.new()
	up.filter_enabled = true
	# SYNCED: the upper chain advances even at zero weight, so its idle keeps the legs' idle's
	# time. idle_armed is NOT a seamless loop (its wrap snaps Spine02 34.6 deg, LeftArm 78) and
	# two copies wrapping at different moments would pop twice per loop instead of once.
	up.sync = true
	bt.add_node("a_idle_u", a_idle_u, Vector2(0, -420))
	bt.add_node("a_walk_u", a_walk_u, Vector2(0, -340))
	bt.add_node("a_run_u", a_run_u, Vector2(0, -260))
	bt.add_node("ts_walk_u", ts_walk_u, Vector2(180, -340))
	bt.add_node("ts_run_u", ts_run_u, Vector2(180, -260))
	bt.add_node("seek_walk_u", seek_walk_u, Vector2(300, -340))
	bt.add_node("seek_run_u", seek_run_u, Vector2(300, -260))
	bt.add_node("bl_iw_u", bl_iw_u, Vector2(430, -380))
	bt.add_node("bl_wr_u", bl_wr_u, Vector2(560, -320))
	bt.add_node("up", up, Vector2(620, -120))
	bt.connect_node("ts_walk_u", 0, "a_walk_u")
	bt.connect_node("seek_walk_u", 0, "ts_walk_u")
	bt.connect_node("ts_run_u", 0, "a_run_u")
	bt.connect_node("seek_run_u", 0, "ts_run_u")
	bt.connect_node("bl_iw_u", 0, "a_idle_u")
	bt.connect_node("bl_iw_u", 1, "seek_walk_u")
	bt.connect_node("bl_wr_u", 0, "bl_iw_u")
	bt.connect_node("bl_wr_u", 1, "seek_run_u")
	bt.connect_node("up", 0, "bl_wr")
	bt.connect_node("up", 1, "bl_wr_u")
	# the guard rides over LOCOMOTION ONLY -- everything below this point overrides it
	# THE STRAFE REPLACES LOCOMOTION, it does not ride over it -- a side-step is a different
	# gait, not a modifier on a walk -- so it sits between the blend space and the guard.
	var strf := AnimationNodeBlend2.new()
	strf.sync = true
	var a_strafe := AnimationNodeAnimation.new()
	a_strafe.animation = String(am.get("strafe_l", ""))
	bt.add_node("a_strafe", a_strafe, Vector2(560, 380))
	bt.add_node("strf", strf, Vector2(660, -40))
	bt.connect_node("strf", 0, "up")
	bt.connect_node("strf", 1, "a_strafe")
	bt.connect_node("blend", 0, "strf")
	bt.connect_node("blend", 1, "carry")
	bt.connect_node("blk", 0, "blend")
	bt.connect_node("ts_block", 0, "a_block")
	bt.connect_node("seek_block", 0, "ts_block")
	bt.connect_node("blk", 1, "seek_block")
	# THE AXE ARM'S GUARD: above the block, below the strikes (see _apply_axe_guard)
	var guard_r := AnimationNodeAnimation.new()
	guard_r.animation = action
	# the BLOCK has its own guard: it turns his torso ~50 deg to present the shield, and a pose
	# held relative to the chest would turn the axe out of guard with it. gsel follows the block.
	var guard_rb := AnimationNodeAnimation.new()
	guard_rb.animation = action
	var gsel := AnimationNodeBlend2.new()
	var blend_r := AnimationNodeBlend2.new()
	blend_r.filter_enabled = true
	bt.add_node("guard_r", guard_r, Vector2(900, 300))
	bt.add_node("guard_rb", guard_rb, Vector2(900, 380))
	bt.add_node("gsel", gsel, Vector2(940, 260))
	bt.add_node("blend_r", blend_r, Vector2(960, 100))
	bt.connect_node("gsel", 0, "guard_r")
	bt.connect_node("gsel", 1, "guard_rb")
	bt.connect_node("blend_r", 0, "blk")
	bt.connect_node("blend_r", 1, "gsel")
	var prev := "blend_r"
	var x := 1020.0
	for key in ["slash", "chop", "bash"]:
		var clip := String(strikes[key])
		if clip == "" or not _clip_len.has(clip):
			continue
		var an := AnimationNodeAnimation.new()
		an.animation = clip
		# THE RECOVERY RELEASE (see _release_tick): rel_<key> hands the axe arm back to the guard
		# after the strike's active swing. It sits INSIDE the one-shot, so the fade-out that
		# follows starts from a strike whose arm is already at guard.
		var g_n := AnimationNodeAnimation.new()
		var rp := String(_release_spec().get("pose", ""))
		g_n.animation = rp if _clip_len.has(rp) else clip
		var rel := AnimationNodeBlend2.new()
		rel.filter_enabled = true
		# SYNCED: the held pose advances with the strike, so its time left is the strike's
		rel.sync = true
		var os_n := AnimationNodeOneShot.new()
		os_n.fadein_time = fin
		os_n.fadeout_time = fout
		bt.add_node("a_" + key, an, Vector2(x, 280))
		bt.add_node("g_" + key, g_n, Vector2(x, 400))
		bt.add_node("rel_" + key, rel, Vector2(x, 190))
		bt.add_node("os_" + key, os_n, Vector2(x, 100))
		bt.connect_node("rel_" + key, 0, "a_" + key)
		bt.connect_node("rel_" + key, 1, "g_" + key)
		bt.connect_node("os_" + key, 0, prev)
		bt.connect_node("os_" + key, 1, "rel_" + key)
		_strikes.append("os_" + key)
		prev = "os_" + key
		x += 170.0
	bt.connect_node("output", 0, prev)
	_tree = AnimationTree.new()
	_tree.name = "AnimTree"
	_tree.tree_root = bt
	_anim.get_parent().add_child(_tree)
	_tree.anim_player = _tree.get_path_to(_anim)
	_tree.root_node = _tree.get_path_to(_anim.get_node(_anim.root_node))
	_tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
	_tree.active = true
	_anim.active = false
	_walk_contact = _contact_phase(String(_roles.get("walk", "walk")))
	_run_contact = _contact_phase(String(_roles.get("run", "run")))
	print("anim tree: left-toe contact at phase %.3f of the walk and %.3f of the run"
		% [_walk_contact, _run_contact])
	print("anim tree: %s | sync group walk %.4f s / run %.4f s at %.1f/%.1f px/s | strikes %s at %.2f/%.2f s | arm layer '%s' filtered to %d of %d tracks | block '%s'"
		% ["ARMED" if armed() else "unarmed", _walk_len, _run_len, wsp, rsp, str(_strikes),
		   fin, fout, action, filtered, ca.get_track_count(),
		   String(_roles.get("block", "-"))])


func _contact_phase(clip: String) -> float:
	"""The phase at which the LEFT toe is lowest -- the clip's own statement of when that
	foot is down. Read off the animation's track rather than assumed to be frame 0."""
	if _anim == null or not _clip_len.has(clip) or _skel == null:
		return 0.0
	var a := _anim.get_animation(clip)
	var bone := _skel.find_bone("LeftToeBase")
	if bone < 0:
		return 0.0
	var n: int = maxi(int(round(a.length * 24.0)), 1)
	var best := 1e9
	var at := 0.0
	var save := _anim.current_animation
	var mode := _anim.callback_mode_process
	_anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var was_active := _anim.active
	_anim.active = true
	_anim.play(clip)
	for i in n:
		var tt: float = a.length * float(i) / float(n)
		_anim.seek(tt, true, true)
		var y: float = _skel.get_bone_global_pose(bone).origin.y
		if y < best:
			best = y
			at = float(i) / float(n)
	_anim.active = was_active
	_anim.callback_mode_process = mode
	if save != "":
		_anim.play(save)
	return at


func _layer_weight(clip: String) -> float:
	"""1 whenever the shield is carried -- but ONLY OVER LOCOMOTION, by construction.

	CORRECTED 2026-09-29: this docstring used to open "over every clip INCLUDING the attack",
	which described the D2 rule reversal and was read, reasonably, as the guard still
	fighting the strikes' own left arm. It does not, and has not since the armed wiring: the
	guard Blend2 sits BELOW the block and all three strike one-shots in the graph, so at
	full strike weight the strike owns every bone (attack_lab measures 0.000 m deviation from
	the raw clip there). The history below is kept because it is why the layer exists.

	THE EXPORT'S MANIFEST SAYS THE OPPOSITE and it is worth reading here rather than
	silently disagreeing with it: `do NOT apply it over attack -- the slash uses the right
	arm and the left must swing free`. Reversed by design call on this scene's own
	measurements. Without the layer the shield is 0.249 m inside his torso through the
	slash -- 1107 of 2439 sampled vertices -- and with it 54 at 0.067 m. A free-swinging
	left arm is only free if it is not holding a shield; a shield-bearer keeps his guard up
	while he strikes with the other hand.

	`never_over` is still honoured, and is now empty: the exclusion is data, not code, so
	the next reversal is one line of JSON and not a hunt through a method."""
	if _tree == null or not _layer_on:
		return 0.0
	# NO `never_over` LIST ANY MORE, because the GRAPH says it. The guard blend sits below
	# the block and below all three strike one-shots, so a block or a swing owns the left
	# arm for as long as it runs and hands it back on its own fade. An exclusion expressed
	# as wiring cannot disagree with itself the way a list of clip names can.
	return 1.0


func _build_gear() -> void:
	if _skel == null or String(cfg.get("gear_manifest", "")) == "":
		return
	var ms: float = maxf(_mesh.global_transform.basis.get_scale().x, 1e-9)
	gear = CharGear.build(_skel, String(cfg["gear_manifest"]), String(cfg.get("gear_dir", "")),
						  _figure_scale, ms)
	set_gear_stack(0)
	print("gear: %s" % JSON.stringify(gear.get("_report", {})))


func gear_stack_count() -> int:
	return (cfg.get("gear_stacks", []) as Array).size()


func set_gear_stack(i: int) -> void:
	"""Five stacks, cumulative: base / +helmet+bracers / +byrnie / +mantle / +axe+shield.

	The helmet_on morph FOLLOWS THE HELMET and nothing else changes with it. It compresses
	the crown hair so the helmet has somewhere to sit; leaving it at 0 under a helmet is a
	head of hair through a steel cap, and setting it without one is a dent in a bare skull."""
	var stacks: Array = cfg.get("gear_stacks", [])
	if stacks.is_empty() or gear.is_empty():
		return
	gear_stack = posmod(i, stacks.size())
	var on: Array = stacks[gear_stack]
	CharGear.show_pieces(gear, on)
	for morph in (cfg.get("morph_rules", {}) as Dictionary):
		_set_morph(String(morph), String(cfg["morph_rules"][morph]) in on)
	# THE CLIP SET FOLLOWS THE GEAR. Picking up an axe and a shield changes how he stands,
	# walks and runs, not only what is in his hands -- that is the whole point of the armed
	# set -- so the stack change re-points the tree before anything else reads it.
	var was := _armed
	_layer_on = armed()
	if armed() != was:
		_apply_clip_set()
	if _tree != null:
		_tree.set("parameters/blend/blend_amount", _layer_weight(_clip))
		_tree.set("parameters/blend_r/blend_amount", _axe_guard_weight())


func cycle_gear() -> void:
	set_gear_stack(gear_stack + 1)


func _set_morph(want: String, on: bool) -> void:
	"""helmet_on compresses the crown under the helmet; grip_R and grip_L close the fists
	round the haft and the grip bar. The rig has 24 bones and NO FINGER BONES, so a morph is
	the only way a hand can close -- which is why an open flat hand was what Matt saw."""
	if want == "" or _mesh == null or _mesh.mesh == null:
		return
	for i in _mesh.mesh.get_blend_shape_count():
		if String(_mesh.mesh.get_blend_shape_name(i)) == want:
			_mesh.set_blend_shape_value(i, 1.0 if on else 0.0)
			return


func _read_cfg() -> Dictionary:
	if not FileAccess.file_exists(CHARACTER):
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(CHARACTER))
	return j if typeof(j) == TYPE_DICTIONARY else {}


func _recentre_all() -> Dictionary:
	"""Put any clip that STANDS AWAY FROM THE ORIGIN back over it, horizontally.

	THIS IS THE GLITCH MATT SAW IN THE CHOP AND THE ATTACK. Three armed clips were exported
	standing away from the rig origin -- the point this scene stands the body on: idle_armed
	1.10 m on average, run_armed 1.83 m, attack_chop 0.48 m at its first frame. Every other
	clip keeps its hips within 0.15 m. A displaced clip is drawn away from its own capsule,
	and every blend into or out of it drags the WHOLE FIGURE across the ground by the
	difference: out of idle_armed into the slash that is 1.32 m inside the 0.10 s fade-in,
	535 mm of lurch per game frame (attack_lab, runs/C-9/attack_lab/) against 6.4 mm for the
	unarmed barbarian. Every strike and the block, from idle and from a run: 485-1296 mm.

	NO RUNTIME PIECE CAUSED IT, and the elimination ladder is how that is known: raw clip,
	+grip morphs, +arm layers, +this de-root, +the one-shot fades -- 2.0 mm/frame of hip
	motion at full strike weight on every rung, and a 1.32 m jump at the first rung that
	contains a transition to idle_armed. The fades only turn a one-frame teleport into a lurch.

	HOW IT GOT INTO THE FILE: nb_d2/scripts/45_deroot_trim.py removes drift with the
	first-to-last line and then adds back the clip's own FIRST-FRAME position, so each clip
	was de-rooted about wherever it started -- Meshy's Axe Stance starts 1.1 m off, run_armed
	was trimmed from the middle of a travelling take. The export's lint checked whether a
	clip MOVES; a de-rooted clip does not move, it stands elsewhere.

	The export is fixed at source (49_recentre.py, staged) and its lint now FAILs any clip
	whose root never comes within 0.25 m of rest. This is the SAME TEST, so a displaced clip
	cannot reach the screen again whatever the file says -- and once the fixed export is in,
	it finds nothing, exactly as _deroot_all now finds only the chop.

	LOOPS ARE CENTRED ON THEIR MEAN, ONE-SHOTS ON THEIR FIRST FRAME: a strike starts where
	the idle stands him, and a lunge then carries him from there. A constant horizontal
	shift of the hips moves the whole body rigidly, so no pose changes -- only where it is."""
	var out := {}
	if _anim == null or _skel == null:
		return out
	var m_per_unit: float = _skel.global_transform.basis.get_scale().x / maxf(_figure_scale, 1e-9)
	var hb := _skel.find_bone("Hips")
	if hb < 0:
		return out
	var rest: Vector3 = _skel.get_bone_rest(hb).origin
	var loops := {}
	for key in ["clips", "clips_armed"]:
		var m: Dictionary = cfg.get(key, {})
		for role in ["idle", "walk", "run", "strafe_l", "strafe_r"]:
			if m.has(role):
				loops[String(m[role])] = true
	for name in _anim.get_animation_list():
		var a := _anim.get_animation(name)
		var tr := -1
		for i in a.get_track_count():
			if a.track_get_type(i) == Animation.TYPE_POSITION_3D \
					and String(a.track_get_path(i).get_concatenated_subnames()) == "Hips":
				tr = i
				break
		if tr < 0 or a.track_get_key_count(tr) < 1:
			continue
		var n := a.track_get_key_count(tr)
		var closest := 1e9
		var mean := Vector3.ZERO
		for i in n:
			var v: Vector3 = a.track_get_key_value(tr, i)
			closest = minf(closest, Vector2(v.x - rest.x, v.z - rest.z).length() * m_per_unit)
			mean += v
		mean /= float(n)
		if closest <= 0.25:
			continue
		var loop: bool = loops.has(String(name))
		var ref: Vector3 = mean if loop else a.track_get_key_value(tr, 0)
		var off := Vector3(ref.x - rest.x, 0.0, ref.z - rest.z)
		for i in n:
			var v2: Vector3 = a.track_get_key_value(tr, i)
			a.track_set_key_value(tr, i, Vector3(v2.x - off.x, v2.y, v2.z - off.z))
		out[name] = snappedf(off.length() * m_per_unit, 0.001)
		push_warning("character: '%s' stood %.3f m from the origin and never nearer than %.3f m -- recentred on its %s. The export should not ship this; its lint now fails it."
			% [name, off.length() * m_per_unit, closest, "mean (loop)" if loop else "first frame (one-shot)"])
	return out


func _deroot_all() -> Dictionary:
	"""Convert every TRAVELLING clip into an in-place clip plus a speed.

	FOUR OF THE ARMED CLIPS CARRY ROOT MOTION and the rest do not -- measured,
	tools/probe_root.gd, as the Hips track's net horizontal travel over the clip:

	    run_armed       8.6617 m   4.337 m/s    the retargeted straight armed run
	    strafe_L_armed  1.8591 m   0.931 m/s
	    idle_armed      0.8994 m   0.184 m/s    an IDLE that walks nearly a metre
	    attack_chop     0.7519 m   0.123 m/s    the chop lunges

	walk, run, walk_armed, run_armed_locked, block and shield_bash are in place (net under
	9 mm). Mixing the two kinds in one blend space cannot work: this scene drives the BODY
	at a speed and expects the clip to cycle underneath, so a travelling clip would move him
	twice and a travelling IDLE would slide him sideways while he stands still.

	Godot's own answer, AnimationTree.root_motion_track, is tree-wide: it would strip the
	Hips track from the in-place clips too and take their bob and sway with it. So the
	conversion is done here instead, per clip, once, at load -- subtract a linear ramp from
	the Hips track's HORIZONTAL components so the net is zero, leave the vertical alone so
	the grounding and the bob survive. What comes out is the clip the blend space needs and
	a number that is the speed it was travelling at, which is the same number the blend
	space wants to drive the body with. Nothing is invented: the speed is the clip's own.

	Detected, not listed, so a re-export that fixes one cannot leave a stale entry behind."""
	var out := {}
	if _anim == null or _skel == null:
		return out
	var m_per_unit: float = _skel.global_transform.basis.get_scale().x / maxf(_figure_scale, 1e-9)
	for name in _anim.get_animation_list():
		var a := _anim.get_animation(name)
		var tr := -1
		for i in a.get_track_count():
			if a.track_get_type(i) == Animation.TYPE_POSITION_3D \
					and String(a.track_get_path(i).get_concatenated_subnames()) == "Hips":
				tr = i
				break
		if tr < 0 or a.track_get_key_count(tr) < 2 or a.length <= 0.0:
			continue
		var n := a.track_get_key_count(tr)
		var first: Vector3 = a.track_get_key_value(tr, 0)
		var last: Vector3 = a.track_get_key_value(tr, n - 1)
		var net := Vector3(last.x - first.x, 0.0, last.z - first.z)
		var net_m: float = net.length() * m_per_unit
		if net_m < 0.25:
			continue
		for i in n:
			var tt: float = a.track_get_key_time(tr, i)
			var v: Vector3 = a.track_get_key_value(tr, i)
			var f: float = tt / a.length
			a.track_set_key_value(tr, i, Vector3(v.x - net.x * f, v.y, v.z - net.z * f))
		out[name] = snappedf(net_m / a.length, 0.001)
		# the direction it was travelling, in MODEL space -- which is how the scene knows
		# that strafe_L_armed goes to his left without being told which way "L" means.
		_root_dirs[name] = net.normalized()
		print("de-rooted %-16s %.4f m over %.4f s = %.3f m/s removed, heading %s (%+.1f deg off +Z)"
			% [name, net_m, a.length, net_m / a.length, str(net.normalized().snappedf(0.01)),
			   rad_to_deg(atan2(net.normalized().x, net.normalized().z))])
	return out


func _point_strafe() -> void:
	if _tree == null:
		return
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null or not bt.has_node("a_strafe"):
		return
	var clip := String(_roles.get("strafe_" + _strafe_side, ""))
	if clip != "" and _clip_len.has(clip):
		(bt.get_node("a_strafe") as AnimationNodeAnimation).animation = clip


func _loop_locomotion() -> void:
	"""A walk that stops at the end of its cycle is not a walk. glTF carries no loop flag,
	so Godot imports every clip as one-shot -- and the ARMED clips are new, so idle_armed,
	walk_armed and run_armed all arrive loop=0 exactly as idle/walk/run did. Looped here
	by ROLE, so whichever set is live is the set that cycles."""
	if _anim == null:
		return
	for n in cfg.get("loop", []):
		var real := String(_roles.get(String(n), String(n)))
		if _clip_len.has(real):
			_anim.get_animation(real).loop_mode = Animation.LOOP_LINEAR


func armed() -> bool:
	"""ARMED IS A PROPERTY OF WHAT HE IS HOLDING, not a stack index. The export manifest's
	rule is that armed is this character's default because he ships with an axe and a
	shield, and that the unarmed clips stay because an unarmed barbarian is a real state.
	So the test is whether every piece in `armed_when_pieces` is actually equipped -- which
	stays true if the stack list is ever re-ordered or a sixth stack is added."""
	var need: Array = cfg.get("armed_when_pieces", [])
	if need.is_empty():
		return false
	var stacks: Array = cfg.get("gear_stacks", [])
	if gear_stack >= stacks.size():
		return false
	var on: Array = stacks[gear_stack]
	for piece in need:
		if not (String(piece) in on):
			return false
	return true


func _layer_spec() -> Dictionary:
	"""shield_guard_L when armed, and NOT shield_carry_L, which the export supersedes: it
	was authored for the old shield placement and now puts 128 of 1829 sampled vertices
	inside his torso against 12 for the guard."""
	# ALWAYS the guard, in both states. shield_carry_L is superseded by the export and must
	# not be in the running scene at all: whether the layer COUNTS is _layer_on's business
	# (it follows the shield), and leaving a retired clip wired in at weight 0 is how it
	# comes back. The unarmed state simply runs it at zero.
	if cfg.has("arm_layer_armed"):
		return cfg.get("arm_layer_armed", {})
	return cfg.get("arm_layer", {})


func _clip_map() -> Dictionary:
	return cfg.get("clips_armed", {}) if armed() else cfg.get("clips", {})


func _bind_roles() -> void:
	"""Bind idle/walk/run/attack to whatever this GLB's clips are called.

	Declared names first, then the role word itself, then any clip that CONTAINS the role
	word, then idle. A rigged model that names its clips for what they do therefore drops
	in with no edit at all, and one that does not is one line of JSON -- neither needs a
	change to this script, which is the point of the slot."""
	var want: Dictionary = _clip_map()
	var have := _clip_len.keys()
	_armed = armed()
	# chop, block and bash are ARMED-ONLY and are left empty when he is not: an unarmed man
	# has no shield to bash with, and a role bound to a fallback would give him one.
	for role in ["chop", "block", "bash", "strafe_l", "strafe_r"]:
		_roles[role] = String(want.get(role, "")) if _clip_len.has(String(want.get(role, ""))) else ""
	for role in ["idle", "walk", "run", "attack"]:
		var pick := ""
		var declared := String(want.get(role, ""))
		if declared != "" and _clip_len.has(declared):
			pick = declared
		elif _clip_len.has(role):
			pick = role
		else:
			for n in have:
				if String(n).to_lower().contains(role):
					pick = String(n)
					break
		_roles[role] = pick
	if String(_roles.get("idle", "")) == "" and have.size() > 0:
		_roles["idle"] = String(have[0])
	for role in ["walk", "run", "attack"]:
		if String(_roles.get(role, "")) == "":
			_roles[role] = _roles["idle"]
	print("character: %s  clips %s -> %s" %
		[String(cfg.get("model", "?")).get_file(), str(have), str(_roles)])


func set_figure_scale(s: float) -> void:
	"""TRUE SCALE, on demand. 1.25178 is the painted world's own metric -- the art draws a
	person larger than the world's metres say -- and T9-0 asks what he looks like at 1.0,
	a 1.85 m man among props modelled at true size. The capsule and the ink width follow,
	or he keeps a collider and a line built for a bigger man."""
	_figure_scale = s
	var shape := get_child(0) as CollisionShape3D
	if shape != null and shape.shape is CapsuleShape3D:
		var cap := shape.shape as CapsuleShape3D
		cap.height = float(cfg.get("model_height_m", 1.8)) * s
		cap.radius = 0.35 * s
		shape.position = Vector3(0, cap.height * 0.5, 0)
	if _outline != null and _mesh != null:
		var ms: float = maxf(_mesh.global_transform.basis.get_scale().x, 1e-9) / maxf(_rig.scale.x, 1e-9)
		(_outline.material_override as ShaderMaterial).set_shader_parameter("width_model",
			(float(cfg.get("outline_px", LINE_PX)) / PPM) / maxf(s * ms, 1e-9))
	_drive()


func _find(n: Node, cls: String) -> Node:
	if n.get_class() == cls:
		return n
	for c in n.get_children():
		var r := _find(c, cls)
		if r != null:
			return r
	return null


func _set_layer(n: Node, layer: int) -> void:
	if n is VisualInstance3D:
		(n as VisualInstance3D).layers = layer
	for c in n.get_children():
		_set_layer(c, layer)


func _style() -> void:
	# LIT here, unlike the T3 skin. In the 2D scene the knight was composited into a
	# painting and had to carry his own light; here he is the one object in a real
	# scene with real lights, and the whole point of item 4 is to see whether that
	# makes him sit IN the painting rather than on top of it.
	var src := _mesh.get_active_material(0) as BaseMaterial3D
	var m := StandardMaterial3D.new()
	m.albedo_texture = src.albedo_texture if src != null and src.albedo_texture != null \
		else (src.emission_texture if src != null else null)
	m.roughness = 0.62
	m.metallic = 0.25
	_mesh.material_override = m
	_mesh.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON


func _add_outline() -> void:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled;
uniform float width_model = 0.01;
uniform vec4 line_color : source_color = vec4(0.055, 0.043, 0.063, 1.0);
void vertex() { VERTEX += normalize(NORMAL) * width_model; }
void fragment() { ALBEDO = line_color.rgb; }
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	# 1.1 output px, in metres, in model units. The world camera is orthographic at a
	# known px/m, so this is one number and not a distance-dependent one.
	var w_world := float(cfg.get("outline_px", LINE_PX)) / PPM
	# The shader offsets VERTEX, which is in the MESH's own units -- and a rig authored in
	# centimetres arrives with a 0.0109 scale on its mesh node, so a width in metres would
	# come out a hundredth of the line it should be. Measure the mesh's own scale instead
	# of assuming the model is in metres.
	var ms: float = maxf(_mesh.global_transform.basis.get_scale().x, 1e-9)
	mat.set_shader_parameter("width_model", w_world / maxf(_figure_scale * ms, 1e-9))
	_outline = MeshInstance3D.new()
	_outline.name = "InkLine"
	_outline.mesh = _mesh.mesh
	_outline.skin = _mesh.skin
	_mesh.get_parent().add_child(_outline)
	_outline.transform = _mesh.transform
	if _skel != null:
		_outline.skeleton = _outline.get_path_to(_skel)
	_outline.material_override = mat
	_outline.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _read_socket() -> void:
	var prop: Dictionary = cfg.get("prop", {})
	var path := String(prop.get("socket", ""))
	if path == "" or not FileAccess.file_exists(path):
		return
	var j = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(j) != TYPE_DICTIONARY:
		return
	# The same change of basis and half-turn the chartest build needed: the socket was
	# fitted in Blender (Z-up) and this runtime is Y-up, so its rotation is conjugated
	# rather than applied, and the two number the haft's ends oppositely.
	var C := Basis.from_euler(Vector3(-PI / 2.0, 0.0, 0.0))
	var e = j.get("rotation_euler_xyz_deg", [0, 0, 0])
	var rb := Basis.from_euler(Vector3(deg_to_rad(float(e[0])), deg_to_rad(float(e[1])),
									   deg_to_rad(float(e[2]))))
	_socket_basis = C * rb * C.inverse() * Basis.from_euler(Vector3(PI, 0.0, 0.0))
	var o = j.get("offset", [0, 0, 0])
	var s = j.get("scale", [1, 1, 1])
	var k: float = maxf(float(s[0]), 1e-6)
	_socket_offset = C * Vector3(float(o[0]) / k, float(o[1]) / k, float(o[2]) / k)


func _add_pollaxe() -> void:
	var prop: Dictionary = cfg.get("prop", {})
	var model := String(prop.get("model", ""))
	var bone := String(prop.get("bone", "RightHand"))
	if _skel == null or model == "" or not ResourceLoader.exists(model):
		return
	if _skel.find_bone(bone) < 0:
		return
	_attach = BoneAttachment3D.new()
	_skel.add_child(_attach)
	_attach.bone_name = bone
	_pollaxe = (load(model) as PackedScene).instantiate()
	_skel.get_parent().add_child(_pollaxe)
	for mi in _pollaxe.find_children("*", "MeshInstance3D", true, false):
		var src := (mi as MeshInstance3D).get_active_material(0) as BaseMaterial3D
		var m := StandardMaterial3D.new()
		if src != null:
			m.albedo_texture = src.albedo_texture if src.albedo_texture != null else src.emission_texture
		m.roughness = 0.7
		(mi as MeshInstance3D).material_override = m
	_set_layer(_pollaxe, CHAR_LAYER)


func _place_pollaxe() -> void:
	if _pollaxe == null or _attach == null:
		return
	var t := _attach.global_transform
	var b: Basis = t.basis.orthonormalized()
	_pollaxe.global_transform = Transform3D(b * _socket_basis * _figure_scale,
											t.origin + b * _socket_offset * _figure_scale)


func _azimuth_for(f: String) -> float:
	var t := {"S": 0.0, "SE": 45.0, "E": 90.0, "NE": 135.0,
			  "N": 180.0, "NW": 225.0, "W": 270.0, "SW": 315.0}
	return float(t.get(f, 0.0))


# --- movement, in CANVAS pixels ------------------------------------------------
func canvas_velocity_to_world(v_px: Vector2) -> Vector3:
	"""A canvas-space velocity as a velocity on the ground.

	The 2D route moves 247 px/s in CANVAS pixels, and the canvas is an elevated
	orthographic view, so a metre of ground travelled up-screen is foreshortened while a
	metre travelled across-screen is not. Moving the body at a fixed metres-per-second
	would therefore travel visibly slower up the screen than across it. Solving for the
	ground vector whose PROJECTION is the wanted canvas velocity keeps the feel the 2D
	route has: level-local +x is exactly the guide camera's right, and level-local +z
	projects onto its up at -sin(pitch)."""
	var a := v_px.x / PPM
	var lz := Vector3(sin(deg_to_rad(47.0)), 0.0, cos(deg_to_rad(47.0)))
	var k := -lz.dot(up)                       # = sin(pitch)
	var b := (v_px.y / PPM) / maxf(k, 1e-6)
	return right * a + lz * b


func attacking() -> bool:
	"""Any of the three strikes. They are separate one-shots, so "is he swinging" is the
	OR of them and not a single flag -- and every caller that roots him during a swing
	(drive_dir) or refuses to start another (try_strike) reads this one function."""
	if _tree != null:
		for n in _strikes:
			if bool(_tree.get("parameters/%s/active" % n)):
				return true
		return false
	return _attack_t > 0.0


func blocking() -> bool:
	return _blocking


func try_strike(which: String) -> bool:
	"""Fire one of the three strikes if none is already running. No re-trigger mid-swing:
	the clip's own length IS the cooldown, and it is also the only honest answer available
	-- a one-shot re-fired while active restarts its fade, not the swing.

	A strike also CANCELS A BLOCK. Holding a shield up and swinging an axe through it is
	the one combination the guard layer cannot express, and the block is full-body."""
	var node := "os_" + which
	if not (node in _strikes):
		return false
	# the node exists in both states; the ROLE only binds when armed, so an unarmed man
	# cannot chop or shield-bash and the keys simply do nothing.
	var role: String = {"slash": "attack", "chop": "chop", "bash": "bash"}.get(which, which)
	if String(_roles.get(role, "")) == "":
		return false
	if attacking():
		return false
	if _tree != null:
		if _block_phase != "off":
			# A STRIKE CANCELS A BLOCK OUTRIGHT. The strike owns every bone while it runs, so there
			# is nothing to lower -- the block is reset to its raise start and switched off, and the
			# one-shot fades back to GUARD. Clearing `_blocking` alone left the phase at "hold", and
			# since the block blend follows the phase, the held shield came back after every strike.
			_block_phase = "off"
			_tree.set("parameters/ts_block/scale", 0.0)
			_tree.set("parameters/seek_block/seek_request", _block_t0)
		_blocking = false
		_tree.set("parameters/%s/request" % node, AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)
		_rel_fire[which] = true
		# the feet stay where they stand while the body blends into the strike
		_strike_anim = "a_" + which
		_strike_len = float(_clip_len.get(String(_roles.get(role, "")), 0.0))
		_strike_out_sent = false
		_foot_transition("strike_in", float((_tree.tree_root as AnimationNodeBlendTree).get_node(node).get("fadein_time")))
		return true
	_attack_t = float(_clip_len.get(String(_roles.get("attack", "attack")), 1.5))
	return true


func try_attack() -> bool:
	return try_strike("slash")


func set_block(on: bool) -> void:
	"""Held, not fired. The weight is smoothed in _drive so the pose arrives over
	`block_fade_s` rather than snapping, and the frame the request landed on is recorded so
	the latency to the pose can be MEASURED rather than asserted."""
	if on == _blocking:
		return
	if on and (String(_roles.get("block", "")) == "" or attacking()):
		return
	_blocking = on
	if on:
		_block_req_frame = Engine.get_physics_frames()
		_foot_transition("block_in", _block_fade_s())
	if _tree == null:
		return
	if on:
		# RAISE. From the raise start -- or, if a lower is under way, from wherever it has got
		# to, so tapping B mid-lower goes back up instead of snapping to the bottom first.
		if _block_phase == "off":
			_tree.set("parameters/seek_block/seek_request", _block_t0)
		_block_phase = "raise"
		_tree.set("parameters/ts_block/scale", _block_rate)
	else:
		# LOWER: the raise, reversed, back to where it started; then the blend fades to guard
		if _block_phase != "off":
			_block_phase = "lower"
			_tree.set("parameters/ts_block/scale", -_block_lower_rate)


func _physics_process(dt: float) -> void:
	if Input.is_action_just_pressed("attack"):
		try_strike("slash")
	if Input.is_action_just_pressed("attack_chop"):
		try_strike("chop")
	if Input.is_action_just_pressed("shield_bash"):
		try_strike("bash")
	set_block(Input.is_action_pressed("block"))
	drive_dir(Vector2(
		Input.get_action_strength("move_right") - Input.get_action_strength("move_left"),
		Input.get_action_strength("move_down") - Input.get_action_strength("move_up")),
		Input.is_action_pressed("run_modifier"), dt)


func drive_dir(dir: Vector2, running: bool, dt: float, hold := "") -> void:
	"""One step of movement from a CANVAS direction, with a human beat on either end.

	ONE SPEED DRIVES BOTH THE BODY AND THE BLEND, and that is the whole of the no-slide
	guarantee. If the animation blended on the key and the body moved at the key, a ramp
	would still be honest; but if either smoothed and the other did not, the feet would
	slide for exactly as long as the ramp lasted. So the smoothed speed is the only speed:
	the body travels at it and the blend space is positioned at it.

	Accel and decel have different time constants because starting and stopping do not feel
	alike -- and because stopping from a run has further to come down than stopping from a
	walk, an exponential gives the run the longer stop for free."""
	var tr: Dictionary = cfg.get("transitions", {})
	var want := 0.0
	if dir.length() > 0.01:
		dir = dir.normalized()
		_move_dir = dir
		want = run_px_s() if running else walk_px_s()
	# BLOCKING: he side-steps the way the strafe clip goes, and TURNS to face anything else.
	# There is one strafe clip and it goes one way, so a right-hand input has no animation
	# to play -- turning to face it is the honest answer, and it keeps "he can still turn"
	# true without inventing a mirrored clip the export does not have.
	_strafing = false
	if _blocking and dir.length() > 0.01:
		var wdir := canvas_velocity_to_world(dir).normalized()
		var local: Vector3 = (Basis(Vector3.UP, _yaw_cur).inverse() * wdir).normalized()
		var best := 0.6
		var pick := ""
		for s in ["l", "r"]:
			var sd := _strafe_dir(s)
			if sd == Vector3.ZERO:
				continue
			var d2: float = local.dot(sd)
			if d2 > best:
				best = d2
				pick = s
		if pick != "":
			# SWITCH SIDES ONLY WHILE THE STRAFE IS WEIGHTLESS. Re-pointing the clip under a
			# live blend is the same defect as seeking a branch that is contributing to the
			# pose: it swaps the legs mid-step. At zero weight it is invisible.
			if pick != _strafe_side and _strafe_w <= 0.0:
				_strafe_side = pick
				_point_strafe()
			if pick == _strafe_side:
				_strafing = true
	if _strafing:
		want = strafe_px_s()
	elif attacking() or _blocking:
		want = 0.0                       # a strike roots him, and so does a brace
	_foot_lock_tick(want)
	var tau: float = float(tr.get("accel_tau_s", 0.10)) if want > _speed \
		else float(tr.get("decel_tau_s", 0.15))
	_speed += (want - _speed) * (1.0 - exp(-dt / maxf(tau, 1e-4)))
	if want <= 0.0 and _speed < float(tr.get("stop_snap_px_s", 5.0)):
		_speed = 0.0                     # an exponential never arrives; a walker does
	if _tree != null:
		_set_loco(_speed, dt)
	# the state name is kept for the capture tools that read it
	if attacking():
		state = "attack"
	elif _speed <= 0.0:
		state = "idle"
	elif _speed > walk_px_s() * 1.2:
		state = "run"
	else:
		state = "walk"
	if _blocking:
		state = "block"
	if hold != "":
		state = hold
	if _move_dir.length() > 0.01 and not _strafing:
		facing = _facing_for(_move_dir)
	var v := canvas_velocity_to_world(_move_dir * _speed)
	velocity = Vector3(v.x, velocity.y - 18.0 * dt, v.z)
	# MOVE_AND_SLIDE PICKS ITS OWN DELTA, and which one it picks depends on WHERE IT IS
	# CALLED FROM: the physics delta inside a physics frame, the PROCESS delta outside one.
	# Compensating for whichever it is about to use makes one call mean one `dt` of travel.
	var implicit: float = get_physics_process_delta_time() if Engine.is_in_physics_frame() \
		else get_process_delta_time()
	var boost: float = dt / maxf(implicit, 1e-6)
	velocity *= boost
	move_and_slide()
	velocity /= boost
	if is_on_floor():
		velocity.y = 0.0
	_drive(dt)
	_place_pollaxe()


func _set_loco(v: float, dt: float) -> void:
	"""Position the two blends and set both time scales, every frame.

	THE WEIGHT IS SOLVED FROM THE ANIMATION, not read off the speed, and that correction is
	the whole of the sync group working rather than making things worse.

	Locking both cycles to len_blended = lerp(walk_len, run_len, w) is what aligns the
	phases -- but it also means the blended FOOT speed is

	    S(w) = lerp(stride_walk, stride_run, w) / lerp(walk_len, run_len, w)

	and that is NOT lerp(walk_speed, run_speed, w), because a ratio of interpolations is not
	the interpolation of ratios. Setting w from the speed linearly, as a blend space does,
	therefore puts the feet at S(w) while the body travels at v -- and the first build of
	this took the walk-run median from 10 mm to 116 mm per frame, six times worse than the
	blend space it replaced. The tell was that it got worse at the crossover and better at
	the ends, which is exactly where lerp and S agree.

	So: solve S(w) = v. S is monotone between the two clips' own speeds, so a short bisection
	is exact enough and costs nothing. At w = 0 and w = 1, S returns the clips' natural
	speeds, so the ends are untouched and the middle now agrees with the ground."""
	var wsp := walk_px_s()
	var rsp := run_px_s()
	var a: float = clampf(v / maxf(wsp, 1e-6), 0.0, 1.0)
	var w := 0.0
	if v > wsp and not sync_group:
		w = clampf((v - wsp) / maxf(rsp - wsp, 1e-6), 0.0, 1.0)
	elif v > wsp:
		var lo := 0.0
		var hi := 1.0
		for _i in 20:
			w = (lo + hi) * 0.5
			if _foot_speed(w, wsp, rsp) < v:
				lo = w
			else:
				hi = w
		w = clampf((lo + hi) * 0.5, 0.0, 1.0)
	# DAMP THE RUN WEIGHT, and only the run weight. The armed set narrowed the gait span to
	# 94 -> 344 px/s, so the same speed ramp moves w far further per frame than the unarmed
	# 202 -> 648 did, and walk_armed and run_armed are much less alike than walk and run --
	# w jumping 0 -> 0.602 in one frame put a 1.68 m step into the crossover. That is a POSE
	# SNAP, not ground slide: the body moved 0.10 m on the same frame.
	#
	# This is the one place the "one speed drives both" rule is deliberately bent, so the
	# cost is named: while w lags, the blended foot speed is S(w_lagged) against a body at
	# S(w_target), and the feet slip for the length of the lag. It is bounded by the slew
	# and it buys a snap of metres for a slip of centimetres over about three frames. The
	# BODY is untouched, so the stop times stay where the brief put them.
	var wtau: float = float((cfg.get("transitions", {}) as Dictionary).get("loco_w_tau_s", 0.0))
	if wtau > 0.0 and dt > 0.0 and _w_init:
		w = lerpf(_w_cur, w, clampf(1.0 - exp(-dt / wtau), 0.0, 1.0))
	_w_cur = w
	_w_init = true
	_tree.set("parameters/bl_iw/blend_amount", a)
	_tree.set("parameters/bl_wr/blend_amount", w)
	_tree.set("parameters/bl_iw_u/blend_amount", a)
	_tree.set("parameters/bl_wr_u/blend_amount", w)
	_tree.set("parameters/up/blend_amount", 1.0 if _upper_on else 0.0)
	# the upper walk is aligned to the legs' walk only while it is weightless (standing), the
	# upper run only while the run is (as the legs' run is): a seek under weight is a teleport
	if _upper_on and sync_group and a <= 0.0 and _prev_a <= 0.0:
		_align_upper("walk")
	_prev_a = a
	# ALIGN ONLY WHILE THE RUN IS WEIGHTLESS. Seeking a branch that is contributing to the
	# pose teleports it: firing the alignment at the moment the run first took weight put a
	# 1.09 m foot step into a single frame, twice per walk-run-walk, which is a seek and not
	# a slide. While w is 0 the seek is invisible, and because the target tracks the walk's
	# own phase the run advances correctly rather than being pinned. The locked cycle length
	# then holds the alignment for as long as the run has weight, which is exactly when it
	# may not be touched.
	# SEEK ONLY AFTER A FULL FRAME AT ZERO WEIGHT, not on the frame weight first reaches it.
	# On that frame the run has only just stopped contributing and a Blend2 with sync on is
	# still advancing it; seeking then put a 1.68 m step into one frame of the armed
	# crossover -- eleven times the next largest pair, which is a teleport and not a slide.
	if w <= 0.0 and _prev_w <= 0.0 and sync_group:
		align_phase()
		if _upper_on:
			_align_upper("run")
	_prev_w = w
	if not sync_group:
		_tree.set("parameters/ts_walk/scale", 1.0)
		_tree.set("parameters/ts_run/scale", 1.0)
		_tree.set("parameters/ts_walk_u/scale", 1.0)
		_tree.set("parameters/ts_run_u/scale", 1.0)
		return
	# SLEW THE LOCKED CYCLE LENGTH, don't jump it. The pose blend w must track speed
	# exactly or the feet slide for as long as the ramp lasts -- but the CLIP TIMING need
	# not, and jumping it does harm: stopping from a run collapses w by 0.4 in one frame,
	# which re-times both clips in the middle of a stance and moves a foot that is already
	# on the ground. Measured over the 2 frames above walk speed in a run stop.
	var target: float = lerpf(_walk_len, _run_len, w)
	if _cycle_len <= 0.0 or dt <= 0.0:
		_cycle_len = target
	else:
		_cycle_len = lerpf(_cycle_len, target, 1.0 - exp(-dt / CYCLE_TAU_S))
	var blended: float = _cycle_len
	_tree.set("parameters/ts_walk/scale", _walk_len / maxf(blended, 1e-6))
	_tree.set("parameters/ts_run/scale", _run_len / maxf(blended, 1e-6))
	# THE UPPER CLIPS ON THE LEGS' CYCLE: each completes one cycle in the same `blended`
	# seconds, so their phase against the legs is constant once aligned
	_tree.set("parameters/ts_walk_u/scale", _walk_len_u / maxf(blended, 1e-6))
	_tree.set("parameters/ts_run_u/scale", _run_len_u / maxf(blended, 1e-6))


func walk_px_s() -> float:
	return _clip_px_s("walk", "walk_px_s", "walk_px_s_armed", WALK_PX_S)


func run_px_s() -> float:
	return _clip_px_s("run", "run_px_s", "run_px_s_armed", RUN_PX_S)


func strafe_px_s(side := "") -> float:
	"""THE TWO STRAFES ARE NOT MIRRORS AND NOT THE SAME SPEED -- the export says so and the
	measurement agrees: 77.2 px/s left against 56.5 right, at the reference scale. Driving
	both at one number slides the feet on whichever one it is not."""
	var s := side if side != "" else _strafe_side
	var clip := String(_roles.get("strafe_" + s, "")) if s != "" else ""
	if clip == "":
		return 0.0
	return clip_px_s(clip, "", "", 0.0)


func _strafe_dir(side: String) -> Vector3:
	var clip := String(_roles.get("strafe_" + side, ""))
	var dirs: Dictionary = cfg.get("strafe_dirs", {})
	if clip == "" or not dirs.has(clip):
		return Vector3.ZERO
	var a: Array = dirs[clip]
	return Vector3(float(a[0]), float(a[1]), float(a[2])).normalized()


func _clip_px_s(role: String, key: String, key_armed: String, fallback: float) -> float:
	"""A DE-ROOTED CLIP ALREADY TOLD US ITS SPEED, so use that in preference to anything in
	JSON: it is the clip's own travel, measured off the very track that was removed, and it
	cannot drift out of date the way a hand-copied number can. _root_speeds is metres per
	second at figure scale 1.0, so the live scale multiplies in directly and there is no
	second convention to keep straight."""
	var clip := String(_roles.get(role, ""))
	if _root_speeds.has(clip):
		return float(_root_speeds[clip]) * PPM * _figure_scale
	return clip_px_s(clip, key, key_armed, fallback)


func _read_manifest_speeds() -> Dictionary:
	"""Locomotion speeds READ FROM THE SHIPPED EXPORT MANIFEST, not copied into this scene's
	own config. Two rounds running, a hand-copied number went stale against a re-export --
	a duration that was 19% wrong, then speeds measured by a different method -- and a copy
	is the thing that goes stale. The manifest travels with the GLB, so it cannot.

	THE FOOT-LOCK SPEED (T12_10, coordinator ruling 2026-09-30): speed_m_s is the ground speed
	that pins a planted foot, measured on the clip's own keys (nb_d2/scripts/57_footlock.py). The
	NET / STEPPING pair it replaced is still read if an older manifest carries it (stepping first)."""
	var out := {}
	var path := String(cfg.get("gear_manifest", ""))
	if path == "" or not ResourceLoader.exists(path):
		return out
	var raw = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not (raw is Dictionary):
		return out
	var lip = (raw as Dictionary).get("locomotion_in_place", null)
	if not (lip is Dictionary):
		return out
	for name in (lip as Dictionary):
		var e = (lip as Dictionary)[name]
		if not (e is Dictionary):
			continue
		var v = (e as Dictionary).get("stepping_speed_m_s", (e as Dictionary).get("speed_m_s", null))
		if v == null:
			continue
		# STATED AT THE REFERENCE SCALE, like every other px/s here (walk_px_s, run_px_s, clip_px_s):
		# clip_px_s() rescales by _figure_scale / speed_measured_at_scale. PPM alone is figure scale 1.0,
		# which drove every manifest-priced clip at 0.799 of its speed (T12_10, tools/strafe_probe.gd).
		var at_ref: float = float(cfg.get("speed_measured_at_scale", 1.0))
		out[String(name)] = float(v) * PPM * (at_ref if at_ref > 0.0 else 1.0)
	if not out.is_empty():
		print("manifest speeds (canvas px/s at the reference scale): %s" % str(out))
	return out


func clip_px_s(clip: String, key: String, key_armed: String, fallback: float) -> float:
	"""A clip's OWN measured stance rate, rescaled to the live figure, in preference to any
	per-role number. The clips no longer travel -- the export de-roots at source now -- so
	there is no track left to read a speed off, and the measurement in `clip_px_s` is what
	replaces it."""
	if _manifest_px_s.has(clip):
		var at2: float = float(cfg.get("speed_measured_at_scale", 0.0))
		var m: float = float(_manifest_px_s[clip])
		return m * (_figure_scale / at2) if at2 > 0.0 else m
	var tbl: Dictionary = cfg.get("clip_px_s", {})
	if tbl.has(clip):
		var at: float = float(cfg.get("speed_measured_at_scale", 0.0))
		var v: float = float(tbl[clip])
		return v * (_figure_scale / at) if at > 0.0 else v
	return _speed_for(key, key_armed, fallback)


func _speed_for(key: String, key_armed: String, fallback: float) -> float:
	"""The live gait speed, in canvas px/s -- ARMED SET and FIGURE SCALE both applied here
	so there is exactly one answer and every caller gets the same one.

	THE FIGURE SCALE MATTERS AND WAS BEING IGNORED. Both speeds were derived from the clips'
	strides at figure scale 1.25178 and then driven unchanged at the 1.10 default, so the
	ground moved 13.8% faster than his legs. Measured on the walk clip alone, nothing
	blended: stance-foot travel 6.8 mm/frame median at 1.25178 against 11.4 mm at 1.10, and
	24 of 39 pairs under 10 mm against 13 of 39. About 40% of what was recorded last session
	as "the walk clip's own floor" was this, not the clip.

	A stride is a length on the model, so it scales with the model. Nothing else does."""
	var base: float = float(cfg.get(key, fallback))
	if _armed and cfg.has(key_armed):
		base = float(cfg.get(key_armed, base))
	var at: float = float(cfg.get("speed_measured_at_scale", 0.0))
	if at > 0.0:
		base *= _figure_scale / at
	return base


func _foot_speed(w: float, wsp: float, rsp: float) -> float:
	"""What the blended feet actually travel at, in canvas px/s, at run weight w."""
	var stride_w: float = wsp * _walk_len
	var stride_r: float = rsp * _run_len
	return lerpf(stride_w, stride_r, w) / maxf(lerpf(_walk_len, _run_len, w), 1e-6)


func align_phase() -> void:
	"""Seek the run so its planted-foot contact lands on the walk's.

	The contact frames are read from the CLIPS THEMSELVES in _contact_phase, not chosen:
	the phase at which the left toe is at its lowest is what a contact is. Seeking the run
	branch to (walk_phase - walk_contact + run_contact) * run_len puts the two contacts on
	the same instant, and the constant cycle length above keeps them there."""
	if _tree == null:
		return
	var wl: float = maxf(_walk_len, 1e-6)
	var wp: float = fmod(maxf(float(_tree.get("parameters/a_walk/current_position")), 0.0), wl) / wl
	var target: float = fposmod(wp - _walk_contact + _run_contact, 1.0) * _run_len
	_tree.set("parameters/seek_run/seek_request", target)
	_phase_aligned = true


func _release_spec() -> Dictionary:
	var s = cfg.get("strike_release", {})
	return s if s is Dictionary else {}


func _apply_strike_release() -> void:
	"""Point each strike's release at the guard pose and filter it to the spec's bones, the paths
	taken from whichever clips key them (weapon_r is keyed by the channel, not by the pose)."""
	if _tree == null or _anim == null:
		return
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null:
		return
	var spec := _release_spec()
	var pose := String(spec.get("pose", ""))
	var want: Array = spec.get("bones", [])
	var paths := {}
	for an_name in _anim.get_animation_list():
		var a := _anim.get_animation(an_name)
		for i in a.get_track_count():
			var pth: NodePath = a.track_get_path(i)
			if want.has(String(pth.get_concatenated_subnames())):
				paths[String(pth)] = pth
	var n_on := 0
	for key in ["slash", "chop", "bash"]:
		if not bt.has_node("rel_" + key):
			continue
		var clip := String((bt.get_node("a_" + key) as AnimationNodeAnimation).animation)
		var held := _release_pose_for(clip, String((spec.get("pose_for", {}) as Dictionary).get(clip, pose)))
		(bt.get_node("g_" + key) as AnimationNodeAnimation).animation = held if held != "" else clip
		var b2 := bt.get_node("rel_" + key) as AnimationNodeBlend2
		for p in paths.values():
			b2.set_filter_path(p, _clip_len.has(pose))
		_tree.set("parameters/rel_%s/blend_amount" % key, 0.0)
		n_on += 1
	print("strike release: pose '%s', %d bone paths, %d strikes, swing ends %s, over %.2f s, guard throughout %s"
		% [pose, paths.size(), n_on, JSON.stringify(spec.get("at_s", {})), float(spec.get("over_s", 0.08)),
		   JSON.stringify(spec.get("guard_throughout", []))])


func _release_pose_for(clip: String, pose: String) -> String:
	"""The guard pose as a clip of the STRIKE's length (keys unchanged, so it holds the pose for
	the whole strike): the release Blend2 then reports the strike's own time left."""
	if not _clip_len.has(pose) or not _clip_len.has(clip):
		return ""
	var nm := "%s__%s" % [pose, clip]
	if not _clip_len.has(nm):
		var a := (_anim.get_animation(pose) as Animation).duplicate(true) as Animation
		a.length = float(_clip_len[clip])
		a.loop_mode = Animation.LOOP_NONE
		_anim.get_animation_library("").add_animation(nm, a)
		_clip_len[nm] = a.length
	return nm


func _release_tick(dt: float) -> void:
	"""THE RECOVERY RELEASE, per frame: each strike hands the axe arm back to the guard from the end
	of its active swing (`strike_release.at_s[clip]`) over `over_s`, eased. The weight is taken at
	the position the clip WILL show after this step (current + dt): a release one frame late is an
	arm one frame late, and the slash's first penetrating frame is the first after its swing."""
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null:
		return
	var spec := _release_spec()
	var at_map: Dictionary = spec.get("at_s", {})
	var over: float = maxf(float(spec.get("over_s", 0.08)), 1e-3)
	for key in ["slash", "chop", "bash"]:
		if not bt.has_node("rel_" + key):
			continue
		var r := 0.0
		var clip := String((bt.get_node("a_" + key) as AnimationNodeAnimation).animation)
		var held: bool = (spec.get("guard_throughout", []) as Array).has(clip)
		if held and (bool(_rel_fire.get(key, false)) or bool(_tree.get("parameters/os_%s/active" % key))):
			_rel_fire[key] = false
			r = 1.0
		elif at_map.has(clip):
			var pos := -1.0
			if bool(_rel_fire.get(key, false)):
				pos = 0.0
				_rel_fire[key] = false
			elif bool(_tree.get("parameters/os_%s/active" % key)):
				pos = float(_tree.get("parameters/a_%s/current_position" % key))
			if pos >= 0.0:
				var a0 := float(at_map[clip])
				r = smoothstep(a0, a0 + over, pos + dt)
		_tree.set("parameters/rel_%s/blend_amount" % key, r)


func _axe_guard_spec() -> Dictionary:
	var s = cfg.get("arm_layer_armed_R", {})
	return s if s is Dictionary else {}


func _axe_guard_weight() -> float:
	"""The layer's weight while the axe is carried, blended toward `weight_block` by the block
	weight -- data, swept in the lab -- else 0."""
	var spec := _axe_guard_spec()
	if not _armed or not _clip_len.has(String(spec.get("action", ""))):
		return 0.0
	var w: float = clampf(float(spec.get("weight", 1.0)), 0.0, 1.0)
	var wb: float = clampf(float(spec.get("weight_block", w)), 0.0, 1.0)
	return lerpf(w, wb, clampf(_block_w, 0.0, 1.0))


func _apply_axe_guard() -> void:
	"""Point the layer at its clip and filter it to the spec's DECLARED bones, the paths taken from
	any clip that keys them (T12_10, the coordinator's ruling: a layer's filter is its declared set).
	The importer drops a track equal to the rest pose -- the guard's neutral wrist -- so a filter taken
	from the pose clip's own tracks left RightHand to the base clip; filtered, a bone the pose does not
	key blends to its rest, which is the pose's intent."""
	if _tree == null or _anim == null:
		return
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null or not bt.has_node("blend_r"):
		return
	var spec := _axe_guard_spec()
	var action := String(spec.get("action", ""))
	var b2 := bt.get_node("blend_r") as AnimationNodeBlend2
	var filtered := 0
	if _clip_len.has(action):
		var ab := String(spec.get("action_block", ""))
		if not _clip_len.has(ab):
			ab = action
		(bt.get_node("guard_r") as AnimationNodeAnimation).animation = action
		(bt.get_node("guard_rb") as AnimationNodeAnimation).animation = ab
		var want: Array = spec.get("bones", [])
		var seen := {}
		for c in _anim.get_animation_list():
			var ca := _anim.get_animation(c)
			for i in ca.get_track_count():
				var pth: NodePath = ca.track_get_path(i)
				if want.has(String(pth.get_concatenated_subnames())) and not seen.has(String(pth)):
					seen[String(pth)] = true
					b2.set_filter_path(pth, true)
					filtered += 1
	_tree.set("parameters/blend_r/blend_amount", _axe_guard_weight())
	print("axe guard layer: '%s' at weight %.2f, %d tracks" % [action, _axe_guard_weight(), filtered])


func _upper_spec() -> Dictionary:
	"""`upper_armed` in character.json: the ARMED gait clips whose spine and arms ride over the
	unarmed legs, and the bones they own. Absent, or unarmed -> the layer runs at zero."""
	if not _armed:
		return {}
	var s = cfg.get("upper_armed", {})
	return s if s is Dictionary else {}


func _apply_upper() -> void:
	"""Point the upper chain at the armed gait clips, filter `up` to the spec's bones (paths
	taken from the clips' OWN tracks), and derive the lengths and contact phases the per-frame
	code locks and aligns against. Unarmed, the chain mirrors the legs' clips at weight zero."""
	if _tree == null or _anim == null:
		return
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null or not bt.has_node("up"):
		return
	var spec := _upper_spec()
	var uw := String(spec.get("walk", ""))
	var ur := String(spec.get("run", ""))
	_upper_on = _clip_len.has(uw) and _clip_len.has(ur)
	var idle_c := String(_roles.get("idle", "idle"))
	var walk_c := uw if _upper_on else String(_roles.get("walk", "walk"))
	var run_c := ur if _upper_on else String(_roles.get("run", "run"))
	(bt.get_node("a_idle_u") as AnimationNodeAnimation).animation = idle_c
	(bt.get_node("a_walk_u") as AnimationNodeAnimation).animation = walk_c
	(bt.get_node("a_run_u") as AnimationNodeAnimation).animation = run_c
	for c in [walk_c, run_c]:
		if _clip_len.has(c):
			_anim.get_animation(c).loop_mode = Animation.LOOP_LINEAR
	var want: Array = spec.get("bones", [])
	var up := bt.get_node("up") as AnimationNodeBlend2
	var filtered := 0
	for c in [idle_c, walk_c, run_c]:
		if not _clip_len.has(c):
			continue
		var an := _anim.get_animation(c)
		for i in an.get_track_count():
			var pth: NodePath = an.track_get_path(i)
			var on: bool = _upper_on and want.has(String(pth.get_concatenated_subnames()))
			up.set_filter_path(pth, on)
			if on and c == walk_c:
				filtered += 1
	_walk_len_u = float(_clip_len.get(walk_c, 1.0))
	_run_len_u = float(_clip_len.get(run_c, 1.0))
	_walk_contact_u = _contact_phase(walk_c)
	_run_contact_u = _contact_phase(run_c)
	_tree.set("parameters/up/blend_amount", 1.0 if _upper_on else 0.0)
	if _upper_on:
		_align_upper("walk")
		_align_upper("run")
	print("upper layer: %s | walk '%s' (%.4f s, contact %.3f) run '%s' (%.4f s, contact %.3f) | %d tracks on %d bones"
		% ["ON" if _upper_on else "off", walk_c, _walk_len_u, _walk_contact_u, run_c, _run_len_u,
		   _run_contact_u, filtered, want.size()])


func _align_upper(which: String) -> void:
	"""Seek an upper clip so its left-toe contact lands on the LEGS' walk contact -- the same
	rule align_phase uses for the legs' run, so all four clips share one contact instant."""
	if _tree == null:
		return
	var wl: float = maxf(_walk_len, 1e-6)
	var wp: float = fmod(maxf(float(_tree.get("parameters/a_walk/current_position")), 0.0), wl) / wl
	if which == "walk":
		_tree.set("parameters/seek_walk_u/seek_request", fposmod(wp - _walk_contact + _walk_contact_u, 1.0) * _walk_len_u)
	else:
		_tree.set("parameters/seek_run_u/seek_request", fposmod(wp - _walk_contact + _run_contact_u, 1.0) * _run_len_u)


func speed_px_s() -> float:
	return _speed


func _facing_for(d: Vector2) -> String:
	var ang := rad_to_deg(atan2(-d.y, d.x))
	var names := ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
	var i := int(round(ang / 45.0)) % 8
	if i < 0:
		i += 8
	return names[i]


func _add_foot_lock() -> void:
	"""Leg IK that holds planted feet through strike and block transitions (foot_lock.gd).
	Off with `"foot_lock": false` in character.json; needs TwoBoneIK3D (Godot 4.6+)."""
	if _skel == null or not bool(cfg.get("foot_lock", true)) or not ClassDB.class_exists("TwoBoneIK3D"):
		return
	_foot_lock = FootLock.new()
	_foot_lock.name = "FootLock"
	_skel.add_child(_foot_lock)
	_foot_lock.setup(self, _skel)


func _foot_transition(kind: String, hold_s: float) -> void:
	if _foot_lock != null:
		_foot_lock.transition(kind, hold_s)


func _block_fade_s() -> float:
	return float((cfg.get("transitions", {}) as Dictionary).get("block_fade_s", float(cfg.get("block_fade_s", 0.12))))


func _foot_lock_tick(want: float) -> void:
	"""Two events drive_dir can see that set_block and try_strike cannot: a strike's FADE-OUT
	starting (the body blends back to guard -- the feet hold again), and locomotion taking
	over (the walk owns the feet -- any lock is handed back as a short step)."""
	if _foot_lock == null or _tree == null:
		return
	if attacking() and _strike_anim != "" and not _strike_out_sent:
		var fout := float((cfg.get("transitions", {}) as Dictionary).get("attack_fade_out_s", 0.25))
		var pos: float = float(_tree.get("parameters/%s/current_position" % _strike_anim))
		if _strike_len > 0.0 and pos >= _strike_len - fout:
			_strike_out_sent = true
			_foot_transition("strike_out", fout)
	var moving: bool = want > 0.0 and not attacking()
	if moving and not _was_moving:
		_foot_lock.release_all()
	_was_moving = moving


func _block_tick() -> void:
	if _block_phase == "off" or _tree == null:
		return
	var pos: float = float(_tree.get("parameters/a_block/current_position"))
	if _block_phase == "raise" and pos >= _block_peak:
		_tree.set("parameters/seek_block/seek_request", _block_peak)
		_tree.set("parameters/ts_block/scale", 0.0)
		_block_phase = "hold"
	elif _block_phase == "lower" and pos <= _block_t0 + 1e-3:
		_tree.set("parameters/ts_block/scale", 0.0)
		_block_phase = "off"
		_foot_transition("block_out", _block_fade_s())


func _block_marks() -> void:
	"""Where Block1's RAISE starts and where it PEAKS, read off the clip -- the shield hand's
	height, as _contact_phase reads a foot. Peak = the hand at its highest; raise start = the
	last low before it, where the rise to the peak begins. Measured, not typed in, so a
	re-exported block cannot leave stale numbers here. Durations come from character.json.

	Block1 as shipped (attack_lab): hand 1.591 m at frame 0, a wind-up wobble, the last low
	1.56 m at 0.750 s, the peak 1.728 m at 1.333 s, then a recovery dip and back to 1.591 m."""
	var clip := String((cfg.get("clips_armed", {}) as Dictionary).get("block", ""))
	if _anim == null or _skel == null or not _clip_len.has(clip):
		return
	var a := _anim.get_animation(clip)
	var hb := _skel.find_bone("LeftHand")
	var n: int = maxi(int(round(a.length * 24.0)), 2)
	var ys := []
	var save := _anim.current_animation
	var mode := _anim.callback_mode_process
	_anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var was_active := _anim.active
	_anim.active = true
	_anim.play(clip)
	for i in n + 1:
		_anim.seek(a.length * float(i) / float(n), true, true)
		ys.append(_skel.get_bone_global_pose(hb).origin.y)
	_anim.active = was_active
	_anim.callback_mode_process = mode
	if save != "":
		_anim.play(save)
	var ip := 0
	for i in ys.size():
		if float(ys[i]) > float(ys[ip]):
			ip = i
	var i0 := ip
	while i0 > 0 and float(ys[i0 - 1]) <= float(ys[i0]):
		i0 -= 1
	_block_t0 = a.length * float(i0) / float(n)
	_block_peak = a.length * float(ip) / float(n)
	var bt: Dictionary = cfg.get("block_timing", {})
	var raise_s := float(bt.get("raise_s", 0.18))
	var lower_s := float(bt.get("lower_s", 0.20))
	_block_rate = (_block_peak - _block_t0) / maxf(raise_s, 1e-3)
	_block_lower_rate = (_block_peak - _block_t0) / maxf(lower_s, 1e-3)
	if _tree != null:
		_tree.set("parameters/ts_block/scale", 0.0)
		_tree.set("parameters/seek_block/seek_request", _block_t0)
	print("block: raise %.3f -> %.3f s of '%s', played in %.2f s (x%.2f), lowered in %.2f s"
		% [_block_t0, _block_peak, clip, raise_s, _block_rate, lower_s])


func _apply_clip_set() -> void:
	"""Re-point the live tree at the other clip set. The nodes are mutated in place rather
	than the tree rebuilt: an AnimationNodeAnimation DOES re-pose when its `animation`
	property is set on a running tree (measured, tools/probe_armed.gd), and a rebuild would
	drop the locomotion phase and pop him mid-stride.

	Everything derived FROM the clips is re-derived here too. Forgetting any one of them is
	a foot slide: the cycle lengths drive the sync group's time scales, and the contact
	phases are what the run is aligned against."""
	if _tree == null or _anim == null:
		return
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null:
		return
	_bind_roles()
	_loop_locomotion()
	for pair in [["a_idle", "idle"], ["a_walk", "walk"], ["a_run", "run"], ["a_block", "block"],

				 ["a_slash", "attack"], ["a_chop", "chop"], ["a_bash", "bash"]]:
		var nm := String(pair[0])
		if not bt.has_node(nm):
			continue
		var clip := String(_roles.get(String(pair[1]), ""))
		if clip != "" and _clip_len.has(clip):
			(bt.get_node(nm) as AnimationNodeAnimation).animation = clip
	var spec := _layer_spec()
	var action := String(spec.get("action", ""))
	if action != "" and _clip_len.has(action) and bt.has_node("carry"):
		(bt.get_node("carry") as AnimationNodeAnimation).animation = action
		var b2 := bt.get_node("blend") as AnimationNodeBlend2
		var want: Array = spec.get("bones", [])
		var ca := _anim.get_animation(action)
		for i in ca.get_track_count():
			var pth: NodePath = ca.track_get_path(i)
			b2.set_filter_path(pth, want.has(String(pth.get_concatenated_subnames())))
	_walk_len = float(_clip_len.get(String(_roles.get("walk", "walk")), 1.0))
	_run_len = float(_clip_len.get(String(_roles.get("run", "run")), 1.0))
	_walk_contact = _contact_phase(String(_roles.get("walk", "walk")))
	_run_contact = _contact_phase(String(_roles.get("run", "run")))
	_cycle_len = 0.0
	_point_strafe()
	_block_marks()
	align_phase()
	_apply_upper()
	_apply_axe_guard()
	_apply_strike_release()
	print("clip set -> %s: idle '%s' walk '%s' (%.4f s, %.1f px/s) run '%s' (%.4f s, %.1f px/s) layer '%s'"
		% ["ARMED" if _armed else "unarmed", String(_roles.get("idle", "")),
		   String(_roles.get("walk", "")), _walk_len, walk_px_s(),
		   String(_roles.get("run", "")), _run_len, run_px_s(), action])


func _drive(dt := 0.0) -> void:
	"""The yaw, turned rather than snapped.

	A facing that jumps 45 degrees in a frame is the same defect as a pose that jumps: the
	eye cannot read it as movement. The target comes from the direction he is actually
	travelling when he is travelling, and from the facing name when he is not, so a tool
	that sets `facing` directly still turns him."""
	var wf: Vector3
	# NOT WHILE SIDE-STEPPING. The yaw target was the direction of travel whenever he was
	# moving -- and a strafe moves him -- so he turned toward the strafe direction, fell out
	# of the strafe cone within three frames and stopped: every strafe cancelled itself
	# (attack_lab, 2026-09-29: dot to his left 0.90 -> 0.71 -> 0.53, then no strafe). Holding
	# `facing` was never enough, because this line never read it while he was moving.
	if _move_dir.length() > 0.01 and _speed > 0.0 and not _strafing:
		wf = canvas_velocity_to_world(_move_dir)
	else:
		wf = canvas_velocity_to_world(_canvas_dir_for(facing))
	wf.y = 0.0
	if wf.length() < 1e-6:
		wf = Vector3.FORWARD
	wf = wf.normalized()
	var mf: Vector3 = _forward_axis
	var target: float = atan2(wf.x, wf.z) - atan2(mf.x, mf.z)
	if not _yaw_init:
		_yaw_cur = target
		_yaw_init = true
	elif dt > 0.0:
		var tau: float = float((cfg.get("transitions", {}) as Dictionary).get("turn_tau_s", 0.12))
		_yaw_cur = lerp_angle(_yaw_cur, target, clampf(1.0 - exp(-dt / maxf(tau, 1e-4)), 0.0, 1.0))
	else:
		_yaw_cur = target
	var yaw := Basis(Vector3.UP, _yaw_cur)
	_rig.global_transform = Transform3D(yaw.scaled(Vector3.ONE * _figure_scale), global_position)
	# THE BLOCK WEIGHT, eased rather than switched. He turns while blocking because the yaw
	# above reads `facing`, which drive_dir keeps updating from the key, and only the SPEED
	# is forced to zero.
	if _tree != null:
		_block_tick()
		var sw: float = 1.0 if _strafing else 0.0
		# the block pose is on for the WHOLE raise-hold-lower, not only while the key is down:
		# releasing B starts the lower, and the lower is part of the block
		var bw: float = 0.0 if _strafing else (1.0 if _block_phase != "off" else 0.0)
		var bt: float = float((cfg.get("transitions", {}) as Dictionary).get("block_fade_s",
			float(cfg.get("block_fade_s", 0.12))))
		var step: float = 1.0 if bt <= 0.0 or dt <= 0.0 else dt / bt
		_block_w = move_toward(_block_w, bw, step)
		_strafe_w = move_toward(_strafe_w, sw, step)
		_tree.set("parameters/blk/blend_amount", _block_w)
		_tree.set("parameters/gsel/blend_amount", clampf(_block_w, 0.0, 1.0))
		_tree.set("parameters/blend_r/blend_amount", _axe_guard_weight())
		_tree.set("parameters/strf/blend_amount", _strafe_w)
		_release_tick(dt)


func _canvas_dir_for(f: String) -> Vector2:
	"""The canvas direction a facing name means -- the exact inverse of _facing_for."""
	var names := ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
	var i := names.find(f)
	if i < 0:
		i = 6
	var a := deg_to_rad(float(i) * 45.0)
	return Vector2(cos(a), -sin(a))


func play(clip: String) -> void:
	# ROLE OR CLIP NAME, either works: the scene and the capture tools drive "c_walk" by
	# habit, and a swapped-in model may not have a clip by that name. A role is resolved
	# through the binding; anything else is taken as a literal clip name.
	if _roles.has(clip):
		clip = String(_roles[clip])
	elif _anim != null and not _clip_len.has(clip):
		for role in _roles:
			if String(_roles[role]) != "" and String(clip).contains(role):
				clip = String(_roles[role])
				break
	if _anim == null or not _clip_len.has(clip):
		return
	var w := _layer_weight(clip)
	if _tree != null:
		_tree.set("parameters/blend/blend_amount", w)
	if clip == _clip:
		return
	_clip = clip
	if _tree != null:
		# The tools drive this by clip name; the tree is driven by speed and a one-shot.
		# Translate rather than make every caller learn the new shape.
		var atk_name := String(_roles.get("attack", "attack"))
		if clip == atk_name:
			try_attack()
		else:
			var sp := 0.0
			if clip == String(_roles.get("walk", "walk")):
				sp = walk_px_s()
			elif clip == String(_roles.get("run", "run")):
				sp = run_px_s()
			_speed = sp
			_set_loco(sp, 0.0)
	elif _tree == null:
		_anim.speed_scale = 1.0
		_anim.play(clip, 0.15)


func status() -> Dictionary:
	return {"facing": facing, "state": state, "clip": _clip,
			"figure_scale": _figure_scale, "pos": [global_position.x, global_position.y, global_position.z]}
