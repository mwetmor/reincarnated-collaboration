extends Node3D
## JOIN-1 SPRITE-CELL RENDERER (C-9) -- generic; everything kit-specific comes from a kit config.
## Contract: reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md (godot d95e1df). Its
## numbered rules are quoted where they are implemented.
##
##   Godot --path join1_render --resolution 320x180 res://render_cells.tscn
##   env J1_KIT = the kit config (abs path), J1_OUT = <pack_root>/<kit_id>, J1_RAW = raw per-frame json,
##       J1_CLOSURE = scratch dir for the loop-closure frames (render(T), never part of the pack),
##       J1_ONLY = optional "state/DIR,..." subset (a probe run)
##
## SOURCE: the GLBs are loaded at RUNTIME (GLTFDocument), from their own paths -- no editor import. BUT the
## runtime path RE-SAMPLES TOO (measured 2026-09-30, Godot 4.6.3, nb_join/scripts/j_runtime_resample.py): its
## generate_scene(state) bakes every transform track at GLTFState.bake_fps = 30 (keys at 1/30 steps plus one at the
## clip's end) and drops rest-valued tracks -- the editor importer's defaults. A clip keyed on the 30 fps grid comes
## through key-for-key; a 24 fps clip renders as its 30 fps bake. Each kit's `runtime_resample` record says which. Pieces bind gear.gd's way: each skinned MeshInstance3D
## reparented under the body's Skeleton3D, its skin kept, `skeleton` pointed at it.
## CAMERA (2.3): orthographic, size 768/ppm_render, KEEP_HEIGHT, 768^2 SubViewport, pitch alpha
## down from horizontal, yaw 0 (it looks along -Z). THE PORT'S MODEL FRAME is then x = +X (screen-right),
## y = +Z (toward the camera), z = +Y (up); ground origin = world origin. The target is lifted 64 px
## up the screen so the ground origin lands on the anchor (384, 448); that is MEASURED per cell
## (unproject_position), not assumed.
## DIRECTIONS (2.3, the yaw paragraph): direction d's character heading is its ground bearing b in the
## port frame (S 90 ... SE 45). The model faces +Z, and a turn of theta about +Y sends +Z to
## (sin theta, 0, cos theta), so theta = 90 - b EXACTLY. Frame 0's root forward is measured from the
## transform actually rendered and linted to +-0.5 deg by the indexer.
## LIGHT (2.2): the Barrow's winter sun (paint_stack.gd numbers) PARENTED TO THE CAMERA, so every
## direction is lit from the same screen direction. No ground, no plate: a transparent SubViewport.
## FRAMES (2.1): loop t_i = i T / N; casts sample the RELEASE exactly, r = clamp(round((N-1) release_s/T),
## 1, N-2), two uniform segments; hit/death include both ends. No per-direction roll.
## LAYERS, two formats. (a) the sorceress's: kit.layers = {carry_clip, filters{name: bones}, per_state{state: name}}.
## (b) THE LAYER LIST agreed with the scene drax (2026-09-30), for the barbarian: kit.layer_specs = [json paths, each
## with "layers": [...]] (his join_hold.json, read from HIS path, not copied) plus kit.layer_list = [...] (this kit's
## own, e.g. the moves' guards), all applied bottom to top in that order. Each layer {name, action, bones, weight,
## states, time}: a filtered Blend2 over the state's clip, the action behind ITS OWN TimeSeek -- time "pose" = the
## action at 0, "clip" = the base clip's time, or {c_base, c_layer} = PHASE-MAPPED: p = t/T_base, t_layer =
## fposmod(p - c_base + c_layer, 1) * T_layer (his spec, for a gait-synced upper layer). Filter paths come from the
## action's own tracks, or with filter_from "all_clips" from any clip. A state not in a layer's `states` gets it at 0.
## weight_curve {keys: [[t, w]...]} scales the weight over the base clip's time (smoothstep between keys): the death's
## guards blending OUT across the fall, the shout variant's raise blending IN over the cry.

const CANVAS := 768
const ANCHOR := Vector2(384, 448)
const DIRS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
const BEARING := {"S": 90.0, "SW": 135.0, "W": 180.0, "NW": 225.0, "N": 270.0, "NE": 315.0, "E": 0.0, "SE": 45.0}
const STANDOFF := 60.0

var kit: Dictionary
var manifest: Dictionary
var ppm: float
var alpha_deg: float
var who: Node3D
var skel: Skeleton3D
var ap: AnimationPlayer
var tree: AnimationTree
var body: MeshInstance3D
var sv: SubViewport
var cam: Camera3D
var raw := {"frames": [], "cells": {}}
var llist: Array = []

func _ready() -> void:
	kit = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("J1_KIT")))
	manifest = JSON.parse_string(FileAccess.get_file_as_string(String(kit["source"]["clip_manifest"])))
	var cc: Dictionary = kit.get("camera", {})
	ppm = float(cc.get("ppm_render", 151.33680669505316))
	alpha_deg = float(cc.get("pitch_deg", 52.9535411256029))
	get_tree().create_timer(float(kit.get("watchdog_s", 1800.0))).timeout.connect(func(): push_error("J1 WATCHDOG"); get_tree().quit(3))
	_scene()
	await _render_all()
	var f := FileAccess.open(OS.get_environment("J1_RAW"), FileAccess.WRITE)
	f.store_string(JSON.stringify(raw, " ")); f.close()
	print("[j1] %d frames rendered" % raw["frames"].size())
	get_tree().quit()

func _load_glb(path: String) -> Node3D:
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	var err := doc.append_from_file(path, st)
	assert(err == OK, "glTF load failed: " + path)
	return doc.generate_scene(st)

func _scene() -> void:
	sv = SubViewport.new(); sv.size = Vector2i(CANVAS, CANVAS)
	sv.transparent_bg = true
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(sv)
	var env := Environment.new()
	env.background_mode = Environment.BG_CLEAR_COLOR
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1); env.ambient_light_energy = 0.30
	var we := WorldEnvironment.new(); we.environment = env; add_child(we)
	who = _load_glb(String(kit["source"]["body"])); add_child(who)
	skel = who.find_children("*", "Skeleton3D", true, false)[0]
	ap = who.find_children("*", "AnimationPlayer", true, false)[0]
	for p in kit["source"].get("pieces", []):
		_bind(String(p))
	var bname := String(kit.get("h_model", {}).get("mesh_name_contains", "char1"))
	for mi in who.find_children("*", "MeshInstance3D", true, false):
		if String(mi.name).contains(bname) or (mi as MeshInstance3D).find_blend_shape_by_name("grip_R") >= 0:
			body = mi
	_build_tree()
	# the camera: yaw 0, pitched alpha down, the ground origin 64 px below the centre
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.size = float(CANVAS) / ppm
	cam.near = 0.05; cam.far = STANDOFF + 100.0
	sv.add_child(cam); cam.current = true
	var a := deg_to_rad(alpha_deg)
	var fwd := Vector3(0, -sin(a), -cos(a))
	var up := Vector3(0, cos(a), -sin(a))
	var target := up * ((ANCHOR.y - CANVAS / 2.0) / ppm)
	cam.look_at_from_position(target - fwd * STANDOFF, target, Vector3.UP)
	# the light, parented to the camera: the Barrow's winter sun in the camera's (yaw 0) frame
	var e := deg_to_rad(55.0); var az := deg_to_rad(305.0)
	var d := Vector3(-sin(az) * cos(e), -sin(e), -cos(az) * cos(e)).normalized()
	var sun := DirectionalLight3D.new()
	cam.add_child(sun)
	var g := Transform3D().looking_at(d, Vector3.UP)
	sun.global_transform = Transform3D(g.basis, cam.global_position)
	sun.light_color = Color(1.0, 0.955, 0.885); sun.light_energy = 0.90
	sun.shadow_enabled = true; sun.shadow_blur = 1.7
	sun.directional_shadow_max_distance = STANDOFF + 50.0

func _bind(path: String) -> void:
	var src := _load_glb(path)
	for m in src.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null:
			continue
		var local := mi.transform; var skin := mi.skin
		mi.owner = null; mi.get_parent().remove_child(mi)
		skel.add_child(mi)
		mi.transform = local; mi.skin = skin; mi.skeleton = NodePath("..")
	src.queue_free()

func _build_tree() -> void:
	for n in ap.get_animation_list():
		ap.get_animation(n).loop_mode = Animation.LOOP_NONE      # exact seeks, t = T included
	ap.stop()
	tree = AnimationTree.new(); ap.get_parent().add_child(tree)
	tree.anim_player = tree.get_path_to(ap)
	var lay: Dictionary = kit.get("layers", {})
	var bt := AnimationNodeBlendTree.new()
	var a_clip := AnimationNodeAnimation.new(); a_clip.animation = String(kit["states"].values()[0]["clip"])
	var seek := AnimationNodeTimeSeek.new()
	bt.add_node("clip", a_clip); bt.add_node("seek", seek); bt.connect_node("seek", 0, "clip")
	var prev := "seek"
	var tracks := ap.get_animation(a_clip.animation)
	for fname in lay.get("filters", {}):
		# one Blend2 per filter, each fed by ITS OWN carry node (a node's output feeds one input only)
		var carry := AnimationNodeAnimation.new(); carry.animation = String(lay["carry_clip"])
		var b2 := AnimationNodeBlend2.new(); b2.filter_enabled = true
		for i in tracks.get_track_count():
			var pth: NodePath = tracks.track_get_path(i)
			if String(pth.get_concatenated_subnames()) in lay["filters"][fname]:
				b2.set_filter_path(pth, true)
		bt.add_node("carry_" + fname, carry); bt.add_node("L_" + fname, b2)
		bt.connect_node("L_" + fname, 0, prev); bt.connect_node("L_" + fname, 1, "carry_" + fname)
		prev = "L_" + fname
	# (b) the LAYER LIST: his specs first (read from their paths), then this kit's own
	llist = []
	for sp in kit.get("layer_specs", []):
		var spec = JSON.parse_string(FileAccess.get_file_as_string(String(sp)))
		assert(spec != null, "layer spec unreadable: " + String(sp))
		for ly in spec.get("layers", []):
			llist.append(ly)
	for ly in kit.get("layer_list", []):
		llist.append(ly)
	for ly in llist:
		var nm := String(ly["name"])
		var act := ap.get_animation(String(ly["action"]))
		assert(act != null, "layer action not in the GLB: " + String(ly["action"]))
		var an := AnimationNodeAnimation.new(); an.animation = String(ly["action"])
		var ls := AnimationNodeTimeSeek.new()
		var b2 := AnimationNodeBlend2.new(); b2.filter_enabled = true
		var nf := 0
		# filter_from "action" (the agreed default): the action's own tracks. "all_clips": the listed bones' tracks in ANY
		# clip of the file -- Godot's glTF import DROPS rest-valued tracks, so a pose that holds a bone at rest (the
		# guards' neutral wrist, the carry's upper spine) arrives without it, and an action-only filter would let that
		# bone follow the base clip. Filtered but absent in the action, the bone blends toward its rest: the pose's intent.
		var srcs: Array = [act]
		if String(ly.get("filter_from", "action")) == "all_clips":
			srcs = []
			for n2 in ap.get_animation_list(): srcs.append(ap.get_animation(n2))
		var seen := {}
		for a2 in srcs:
			for i in (a2 as Animation).get_track_count():
				var pth: NodePath = (a2 as Animation).track_get_path(i)
				if String(pth.get_concatenated_subnames()) in ly["bones"] and not seen.has(String(pth)):
					seen[String(pth)] = true
					b2.set_filter_path(pth, true); nf += 1
		bt.add_node("la_" + nm, an); bt.add_node("ls_" + nm, ls); bt.connect_node("ls_" + nm, 0, "la_" + nm)
		bt.add_node("LL_" + nm, b2)
		bt.connect_node("LL_" + nm, 0, prev); bt.connect_node("LL_" + nm, 1, "ls_" + nm)
		prev = "LL_" + nm
		print("[j1] layer %s: %s, %d tracks filtered (from %s), weight %s, states %s, time %s" % [nm, ly["action"], nf, ly.get("filter_from", "action"), ly.get("weight", 1.0), ly.get("states", []), ly.get("time", "pose")])
	bt.connect_node("output", 0, prev)
	tree.tree_root = bt
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	tree.active = true

func _pose(state: String, t: float) -> void:
	var st: Dictionary = kit["states"][state]
	((tree.tree_root as AnimationNodeBlendTree).get_node("clip") as AnimationNodeAnimation).animation = String(st["clip"])
	var lay: Dictionary = kit.get("layers", {})
	var on = lay.get("per_state", {}).get(state, null)
	for fname in lay.get("filters", {}):
		tree.set("parameters/L_%s/blend_amount" % fname, 1.0 if on == fname else 0.0)
	for ly in llist:
		var nm := String(ly["name"])
		var on2: bool = state in ly.get("states", [])
		tree.set("parameters/LL_%s/blend_amount" % nm, float(ly.get("weight", 1.0)) * _curve(ly, t) if on2 else 0.0)
		var tm = ly.get("time", "pose")
		var tl := 0.0
		if typeof(tm) == TYPE_DICTIONARY:
			var Tb := ap.get_animation(String(st["clip"])).length
			var Tl := ap.get_animation(String(ly["action"])).length
			tl = fposmod(t / Tb - float(tm["c_base"]) + float(tm["c_layer"]), 1.0) * Tl
		elif String(tm) == "clip":
			tl = t
		tree.set("parameters/ls_%s/seek_request" % nm, tl)
	tree.set("parameters/seek/seek_request", t)
	tree.advance(0.0)
	if body:
		for k in kit.get("morphs", {}):
			if k.begins_with("_"):
				continue
			var i := body.find_blend_shape_by_name(k)
			if i >= 0:
				body.set_blend_shape_value(i, float(kit["morphs"][k]))

## weight_curve (additive to the agreed layer format): {"keys": [[t, w], ...]} in the BASE clip's time, smoothstep-eased
## between keys, held beyond the ends; the layer's blend amount is weight x curve(t). Absent: 1.
func _curve(ly: Dictionary, t: float) -> float:
	if not ly.has("weight_curve"):
		return 1.0
	var ks: Array = ly["weight_curve"]["keys"]
	if t <= float(ks[0][0]):
		return float(ks[0][1])
	for i in range(1, ks.size()):
		if t <= float(ks[i][0]):
			var t0 := float(ks[i - 1][0]); var t1 := float(ks[i][0])
			var u := smoothstep(0.0, 1.0, (t - t0) / maxf(t1 - t0, 1e-9))
			return lerpf(float(ks[i - 1][1]), float(ks[i][1]), u)
	return float(ks[ks.size() - 1][1])

func _mf(path: String):
	var v = manifest
	for k in path.split("."):
		v = v[k]
	return v

func times(state: String) -> Array:
	var st: Dictionary = kit["states"][state]
	var n := int(st["frames"])
	var T := ap.get_animation(String(st["clip"])).length
	var out := []
	match String(st["sampling"]):
		"loop":
			for i in n: out.append(i * T / n)
		"ends":
			for i in n: out.append(T * i / (n - 1))
		"release":
			var rs := float(_mf(String(st["release_from"])))
			var r := clampi(roundi((n - 1) * rs / T), 1, n - 2)
			for i in n:
				out.append(rs * i / r if i <= r else rs + (T - rs) * (i - r) / (n - 1 - r))
	return out

func _world(bone: String) -> Transform3D:
	return skel.global_transform * skel.get_bone_global_pose(skel.find_bone(bone))

func _port(p: Vector3) -> Array:
	return [snappedf(p.x, 0.00001), snappedf(p.z, 0.00001), snappedf(p.y, 0.00001)]

func _sockets(state: String) -> Dictionary:
	var out := {}
	for k in kit["sockets"]:
		var sd: Dictionary = kit["sockets"][k]
		var bone := String(sd.get("per_state_bone", {}).get(state, sd["bone"]))
		var g := _world(bone)
		var p := g.origin + g.basis.y.normalized() * float(sd.get("along_bone_m", 0.0))
		out[k] = _port(p)
	return out

func _facing() -> Dictionary:
	# the rendered root's forward (+Z of her model) and the Hips' (rest forward carried by its pose)
	var f := who.global_transform.basis * Vector3(0, 0, 1)
	var hi := skel.find_bone("Hips")
	var hr := (skel.global_transform * skel.get_bone_global_rest(hi)).basis
	var hp := (skel.global_transform * skel.get_bone_global_pose(hi)).basis
	var hf := hp * (hr.inverse() * (who.global_transform.basis * Vector3(0, 0, 1)))
	return {"root_deg": fposmod(rad_to_deg(atan2(f.z, f.x)), 360.0), "hips_deg": fposmod(rad_to_deg(atan2(hf.z, hf.x)), 360.0)}

func _render_all() -> void:
	var out := OS.get_environment("J1_OUT")
	var clo := OS.get_environment("J1_CLOSURE")
	var only := OS.get_environment("J1_ONLY").split(",", false) if OS.has_environment("J1_ONLY") else PackedStringArray()
	# GPU WARM-UP (2026-09-30): a fresh renderer's first drawn frames can differ -- a spot render's first cell differed
	# in 1 of its 12 frames from the same cell rendered later in a run. Draw throwaway frames of the first state's first
	# pose before anything is saved; nothing here is written.
	who.rotation = Vector3(0, deg_to_rad(90.0 - float(BEARING[DIRS[0]])), 0)
	_pose(String(kit["states"].keys()[0]), 0.0)
	for w in 8: await RenderingServer.frame_post_draw
	for state in kit["states"]:
		var st: Dictionary = kit["states"][state]
		var ts := times(state)
		for dn in DIRS:
			if not only.is_empty() and not ("%s/%s" % [state, dn]) in only:
				continue
			who.rotation = Vector3(0, deg_to_rad(90.0 - float(BEARING[dn])), 0)
			DirAccess.make_dir_recursive_absolute("%s/cells/%s/%s" % [out, state, dn])
			var cell := {"state": state, "dir": dn, "t_s": ts, "anchor_px": [], "sockets": []}
			for i in ts.size():
				_pose(state, float(ts[i]))
				for w in 2: await RenderingServer.frame_post_draw
				var img := sv.get_texture().get_image()
				img.convert(Image.FORMAT_RGBA8)
				var name := "%s_%s_%02d.png" % [state, dn, i]
				img.save_png("%s/cells/%s/%s/%s" % [out, state, dn, name])
				var ap_px := cam.unproject_position(who.global_position)
				cell["anchor_px"].append([snappedf(ap_px.x, 0.001), snappedf(ap_px.y, 0.001)])
				cell["sockets"].append(_sockets(state))
				if i == 0:
					cell["facing"] = _facing()
			if String(st["kind"]) == "loop":
				_pose(state, ap.get_animation(String(st["clip"])).length)
				for w in 2: await RenderingServer.frame_post_draw
				var ci := sv.get_texture().get_image(); ci.convert(Image.FORMAT_RGBA8)
				ci.save_png("%s/%s_%s_T.png" % [clo, state, dn])
			raw["cells"]["%s/%s" % [state, dn]] = cell
			raw["frames"].append_array(ts)
			print("[j1] %-14s %-2s %2d frames  anchor %s  facing root %.4f hips %.2f" % [state, dn, ts.size(), cell["anchor_px"][0],
				cell["facing"]["root_deg"], cell["facing"]["hips_deg"]])
	raw["durations_s"] = {}
	for state in kit["states"]:
		raw["durations_s"][state] = ap.get_animation(String(kit["states"][state]["clip"])).length
	raw["h_model"] = _h_model()

func _h_model() -> Dictionary:
	# sole to crown at REST: skin the body mesh at the skeleton's rest on the CPU (vertex x bone weights)
	skel.reset_bone_poses()
	var mesh := body.mesh
	var arr := mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var bones = arr[Mesh.ARRAY_BONES]; var wts = arr[Mesh.ARRAY_WEIGHTS]
	var skin := body.skin
	var per: int = int(wts.size()) / verts.size()
	var lo := INF; var hi := -INF
	var bind_to_bone := {}
	for b in skin.get_bind_count():
		bind_to_bone[b] = skel.find_bone(skin.get_bind_name(b)) if skin.get_bind_name(b) != &"" else skin.get_bind_bone(b)
	for vi in range(0, verts.size(), 7):
		var p := Vector3.ZERO
		for k in per:
			var w: float = wts[vi * per + k]
			if w <= 0.0:
				continue
			var bi: int = bones[vi * per + k]
			var gb := skel.global_transform * skel.get_bone_global_rest(int(bind_to_bone[bi])) * skin.get_bind_pose(bi)
			p += (gb * verts[vi]) * w
		lo = minf(lo, p.y); hi = maxf(hi, p.y)
	return {"h_m": snappedf(hi - lo, 0.0001), "sole_m": snappedf(lo, 0.0001), "crown_m": snappedf(hi, 0.0001), "vertex_stride": 7}
