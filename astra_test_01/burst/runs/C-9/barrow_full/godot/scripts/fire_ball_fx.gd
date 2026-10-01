extends Node3D
## C-9 (c) -- HER FIRE BALL: cliffside's fire_bolt_e1_B, the kit Matt saw, BAKED from its own runtime and
## PLAYED here as flipbooks. drax.
##
## WHY BAKED (the diagnosis, take/build/fire_bolt_diag.json): on the live cliffside page every cast of the
## kit built ~107 shaders, ~330 ShaderMaterials and ~420 nodes at runtime, compiled them on first draw,
## and drew ~115 more draw calls at the impact -- two 250-300 ms frames per cast in Chrome, every cast.
##
## WHAT IS PLAYED: godot/tools/bake_fire_bolt.gd rendered the kit frame by frame in its own renderer
## (a scratch copy of C-7's cliffside_v45); tools/fire_bake_pack.py packed the frames into ONE atlas
## (two pages of a Texture2DArray: rgb = the kit's premultiplied colour, a = the cover of its MIX
## layers, so a frame lays over any ground as out = rgb + ground * (1 - a), the kit's own blend) with
## a frame table and a per-tick record. Proven against the kit: godot/tools/proof_fire_bolt.gd.
##
## HOW: ONE MultiMesh, ONE ShaderMaterial, ONE draw. Every piece of every cast is an instance of one
## unit quad: the vertex shader reads its frame's atlas rect and offset from a small float texture
## (INSTANCE_CUSTOM.r = frame index), so a quad is exactly its frame's size in px. Each cast owns
## SLOTS consecutive instances in the kit's own back-to-front order (floors, motes, puff, travel,
## burst, halo); an idle instance is collapsed to a point. Nothing is created, loaded, duplicated or
## compiled at cast time: the atlas is read and the shader drawn once, invisibly, while the level
## builds (warm_up()).
##
## PLACEMENT, in the kit's px: the painted Barrow's 1920 x 1080 frame and the kit's canvas are both
## 100.62 px a metre, so a frame is drawn at its baked size. Camera-facing quads carry the travel,
## puff, burst, motes and halo; the two FLOOR LIGHTS lie on the snow (a ground quad whose projection
## is the baked frame). The travel and puff are baked flying EAST and turned to her aim on screen, as
## the kit turns them. Her flight: the kit's own per-tick distances (the capsule's start 74.66 px
## ahead of the socket, 1510 px/s, 520 px), along her facing, at the socket's height; the burst where
## it stops. The halo runs from her cast start to her release, 32 steps of its t.

const DATA := "res://data/vfx/fire_ball/"
const PPM := 100.617553710938
const PXV := 80.3076
const PXH := 60.618
const SLOTS := 14                # per cast: see the S_* offsets
const CASTS := 2                 # casts alive at once (the burst outlives the next windup)
const S_CAST_FLOOR := 0
const S_IMPACT_FLOOR := 1
const S_MOTES := 2               # 8 of them
const S_PUFF := 10
const S_TRAVEL := 11
const S_IMPACT := 12
const S_HALO := 13
const TRAVEL_BEHIND_M := 0.30    # her body before the flight on screen, as cliffside's y-sort puts the keeper
const BURST_TOWARD_M := 1.0      # the burst never clipped by the snow it bursts over
const HALO_TOWARD_M := 0.30
const FLOOR_LIFT_M := 0.06

const SHADER := """
shader_type spatial;
render_mode unshaded, blend_premul_alpha, depth_draw_never, cull_disabled, shadows_disabled, ambient_light_disabled, fog_disabled;
uniform sampler2DArray atlas : filter_linear, repeat_disable;
uniform sampler2D frame_table : filter_nearest, repeat_disable;
uniform vec2 atlas_px;
// ?fb=c75 (R-C9-110, Matt: "a bit too wide/large of a blast zone. It needs to be condensed"): the burst and its
// floor light TIGHTENED, not scaled -- drawn at tighten_k of their size about the burst's point, and read back
// through a radial remap (display radius u -> source radius u^tighten_g of the burst's reach) so the core keeps
// its size and density while the outer flames and the flash's spread come in. Same frames, same brightness.
uniform float tighten_k = 0.75;
uniform float tighten_g = 1.35;
uniform float tighten_r = 250.0;          // the burst's visible reach in kit px (its widest frames' half-width, 485-520 px wide)
varying vec3 v_uv;
varying flat vec4 v_rect;                 // the frame's atlas rect (x, y, w, h), for the remap
varying flat vec3 v_off;                  // its offset from the anchor (x, y) and its page
varying vec2 v_px;
varying vec3 v_tint;
varying vec3 v_mode;             // alpha, mode (0 atlas / 1 mote diamond), the diamond's half size

void vertex() {
	vec4 cst = INSTANCE_CUSTOM;
	vec2 q = VERTEX.xy;          // the unit quad, 0..1, y DOWN (screen-like)
	vec2 px;
	if (cst.b < 0.5 || cst.b > 1.5) {
		int fi = int(cst.r + 0.5);
		vec4 r = texelFetch(frame_table, ivec2(fi, 0), 0);
		vec4 o = texelFetch(frame_table, ivec2(fi, 1), 0);
		px = o.xy + q * r.zw;
		v_uv = vec3((r.xy + q * r.zw) / atlas_px, o.z);
		v_rect = r;
		v_off = o.xyz;
		if (cst.b > 1.5) {
			// MODE 2: the tightened burst. The remap bends the frame's straight edges, so the drawn quad is a
			// square about the burst's point reaching the display radius of the frame's farthest corner; the
			// fragment reads back only what falls inside the frame's own rect
			vec2 c0 = o.xy;
			vec2 c1 = o.xy + r.zw;
			float dmax = max(max(length(c0), length(c1)), max(length(vec2(c0.x, c1.y)), length(vec2(c1.x, c0.y))));
			float reach = tighten_r * tighten_k * pow(dmax / tighten_r, 1.0 / tighten_g);
			px = (q * 2.0 - 1.0) * reach;
		}
	} else {
		float h = cst.a + 1.0;
		px = (q * 2.0 - 1.0) * h;
		v_uv = vec3(0.0);
	}
	v_px = px;
	VERTEX = vec3(px, 0.0);      // the instance basis maps px (x right, y down) into the world
	v_tint = COLOR.rgb;
	v_mode = vec3(cst.g, cst.b, cst.a);
}

vec4 tightened() {
	// the display radius, as a fraction of the drawn reach, read back from the source at its power
	float R = tighten_r * tighten_k;
	float u = length(v_px) / R;
	vec2 dir = v_px / max(length(v_px), 1e-4);
	float s = pow(clamp(u, 0.0, 4.0), tighten_g) * tighten_r;
	vec2 src = dir * s;                                    // source px from the anchor
	vec2 in_rect = src - v_off.xy;                         // px inside the frame's rect
	if (any(lessThan(in_rect, vec2(0.0))) || any(greaterThan(in_rect, v_rect.zw))) { return vec4(0.0); }
	return texture(atlas, vec3((v_rect.xy + in_rect) / atlas_px, v_off.z));
}

float lin(float c) {
	return c <= 0.04045 ? c / 12.92 : pow((c + 0.055) / 1.055, 2.4);
}

void fragment() {
	vec4 t;
	if (v_mode.y < 0.5) {
		t = texture(atlas, v_uv);
	} else if (v_mode.y > 1.5) {
		t = tightened();
	} else {
		// the kit's Polygon2D diamond: hard-edged, a pixel is in when its centre is (|x| + |y| <= half)
		t = vec4(v_tint * step(abs(v_px.x) + abs(v_px.y), v_mode.z), 0.0);
	}
	// premultiplied: a fade scales the colour and the cover together
	vec3 c = t.rgb * v_mode.x;
	// the atlas holds the kit's 8-bit sRGB values: handed over linear, so the output's own sRGB
	// encode puts back exactly those values (Compatibility then blends them in sRGB, as the kit's 2D did)
	ALBEDO = vec3(lin(c.r), lin(c.g), lin(c.b));
	ALPHA = t.a * v_mode.x;
}
"""

var scene                        # barrow_full.gd
# THE DATA AND THE SLOT LAYOUT, overridable (meteor_a_fx.gd, lane A's Meteor, plays its flipbook with this player)
var data_dir := DATA
# ?fb=c75 (desktop -- --fb c75): the burst tightened to 0.75 of its reach (R-C9-110); the shader's MODE 2
var tighten := false
var meta_file := "fire_ball.json"
var slots := SLOTS
var cam: Camera3D
var meta: Dictionary = {}
var ok := false
var report := {"casts": 0, "fired": []}
var mm: MultiMesh
var mmi: MultiMeshInstance3D
var mat: ShaderMaterial
var fidx := {}                   # frame key -> Array[int] of rows in the frame table, by baked tick order
var ftick := {}                  # frame key -> Array[int] of the baked ticks
var travel: Array = []           # the kit's flight: [{tick, dx, dy}]
var impact_tick := 18
var births: Array = []
var casts: Array = []            # live casts, one per slot group
var _warm := 0
var warmed := false              # the load-time draw is done (the page's warming veil waits for it)
var _collapsed := Transform3D(Basis(Vector3.ZERO, Vector3.ZERO, Vector3.ZERO), Vector3.ZERO)


func setup(p_scene, p_cam: Camera3D) -> bool:
	scene = p_scene
	cam = p_cam
	var jp := data_dir + meta_file
	if not FileAccess.file_exists(jp):
		report["error"] = "no " + jp
		return false
	meta = JSON.parse_string(FileAccess.get_file_as_string(jp))
	var imgs: Array[Image] = []
	for f in meta["atlas"]["files"]:
		var bytes := FileAccess.get_file_as_bytes(data_dir + String(f["file"]))
		var ctx := HashingContext.new()
		ctx.start(HashingContext.HASH_SHA256)
		ctx.update(bytes)
		if ctx.finish().hex_encode() != String(f["sha256"]):
			report["error"] = "sha256 mismatch: " + String(f["file"])
			return false
		var img := Image.new()
		if img.load_webp_from_buffer(bytes) != OK:
			report["error"] = "decode: " + String(f["file"])
			return false
		imgs.append(img)
	var atlas := Texture2DArray.new()
	atlas.create_from_images(imgs)
	# the frame table: row 0 = (x, y, w, h) in atlas px, row 1 = (ox, oy, page, 0), one column a frame
	var keys: Array = meta["frames"].keys()
	var n := 0
	for k in keys:
		n += (meta["frames"][k] as Array).size()
	var tbl := PackedFloat32Array()
	tbl.resize(n * 2 * 4)
	var col := 0
	for k in keys:
		fidx[k] = []
		ftick[k] = []
		for fr in meta["frames"][k]:
			var o := col * 4
			tbl[o] = float(fr["x"]); tbl[o + 1] = float(fr["y"]); tbl[o + 2] = float(fr["w"]); tbl[o + 3] = float(fr["h"])
			var o2 := (n + col) * 4
			tbl[o2] = float(fr["ox"]); tbl[o2 + 1] = float(fr["oy"]); tbl[o2 + 2] = float(fr["page"]); tbl[o2 + 3] = 0.0
			fidx[k].append(col)
			ftick[k].append(int(fr["tick"]))
			col += 1
	var table := ImageTexture.create_from_image(Image.create_from_data(n, 2, false, Image.FORMAT_RGBAF, tbl.to_byte_array()))
	var sh := Shader.new()
	sh.code = SHADER
	mat = ShaderMaterial.new()
	mat.shader = sh
	mat.render_priority = PaintStack.AFTER_POST_PRIORITY
	mat.set_shader_parameter("atlas", atlas)
	mat.set_shader_parameter("frame_table", table)
	mat.set_shader_parameter("atlas_px", Vector2(float(meta["atlas"]["w"]), float(meta["atlas"]["h"])))
	var quad := ArrayMesh.new()
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = PackedVector3Array([Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(1, 1, 0), Vector3(0, 1, 0)])
	arr[Mesh.ARRAY_INDEX] = PackedInt32Array([0, 1, 2, 0, 2, 3])
	quad.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	quad.surface_set_material(0, mat)
	mm = MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	mm.use_custom_data = true
	mm.mesh = quad
	mm.instance_count = slots * CASTS
	for i in mm.instance_count:
		mm.set_instance_transform(i, _collapsed)
		mm.set_instance_color(i, Color.WHITE)
		mm.set_instance_custom_data(i, Color(0, 0, 0, 0))
	mmi = MultiMeshInstance3D.new()
	mmi.name = "FireBallFX"
	mmi.multimesh = mm
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mmi.custom_aabb = AABB(Vector3(-500, -100, -500), Vector3(1000, 200, 1000))
	add_child(mmi)
	travel = meta["timing"]["travel"]
	impact_tick = int(meta["timing"]["impact_spawn_tick"])
	births = meta["motes"]["births"]
	for i in CASTS:
		casts.append({})
	ok = true
	report["atlas"] = {"pages": imgs.size(), "px": [int(meta["atlas"]["w"]), int(meta["atlas"]["h"])], "frames": n,
		"impact_sets": (meta["impact_seeds"] as Array).size()}
	return true


func warm_up() -> void:
	"""DRAW IT ONCE, INVISIBLY, while the level builds: the shader compiles and the atlas uploads now, not
	on her first cast. One instance at alpha 0, in front of the camera, for a few frames."""
	if not ok:
		return
	_warm = 4


# ---- the cast's clock (spell_fx.gd drives it: the strike's start and its release) -------------------
func cast_started(socket_fn: Callable, release_ticks: int) -> int:
	"""Her Fire Ball strike has started: the halo runs from now to the release. Returns the cast id."""
	if not ok:
		return -1
	var g := _free_group()
	casts[g] = {"state": "windup", "age": 0, "release_ticks": maxi(release_ticks, 2), "socket_fn": socket_fn,
		"set": randi() % maxi(1, (meta["impact_seeds"] as Array).size())}
	report["casts"] = int(report["casts"]) + 1
	return g


func released(g: int, socket: Vector3, dir: Vector3, feet: Vector3) -> void:
	"""The release: the socket, her facing on the ground, her feet. The flight, puff and cast floor start."""
	if g < 0 or casts[g].is_empty():
		return
	var c: Dictionary = casts[g]
	c["state"] = "flight"
	c["tick"] = 0
	c["clock"] = 0.0
	c["socket"] = socket
	var d := Vector3(dir.x, 0.0, dir.z).normalized()
	c["dir"] = d
	c["feet"] = feet
	c["theta"] = _screen_angle(d)
	report["fired"].append({"socket": [snappedf(socket.x, 0.01), snappedf(socket.y, 0.01), snappedf(socket.z, 0.01)],
		"screen_deg": snappedf(rad_to_deg(float(c["theta"])), 0.1), "impact_set": c["set"]})


func abandon(g: int) -> void:
	if g >= 0 and not casts[g].is_empty() and casts[g]["state"] == "windup":
		casts[g] = {}
		_collapse_group(g)


func _free_group() -> int:
	for i in casts.size():
		if (casts[i] as Dictionary).is_empty():
			return i
	# every group busy: take the one whose burst is furthest on
	var best := 0
	for i in casts.size():
		if int(casts[i].get("tick", 0)) > int(casts[best].get("tick", 0)):
			best = i
	_collapse_group(best)
	return best


var last_us := 0                 # this node's own time in its last physics step (the budget harness reads it)


func _physics_process(dt: float) -> void:
	var t0 := Time.get_ticks_usec()
	_step(dt)
	last_us = Time.get_ticks_usec() - t0


func _step(dt: float) -> void:
	if not ok:
		return
	if _warm > 0:
		_warm -= 1
		var at := cam.global_position + (-cam.global_transform.basis.z) * 5.0
		_put(0, "halo" if fidx.has("halo") else String(fidx.keys()[0]), 0, at, 0.0, 0.0)
		if _warm == 0:
			_collapse(0)
			warmed = true
		return
	for g in casts.size():
		var c: Dictionary = casts[g]
		if c.is_empty():
			continue
		# THE CLOCK IS TIME, the kit's 60 ticks a second: a baked frame per 1/60 s of game time, whatever
		# the physics rate or the time scale (the quarter-speed film runs Engine.time_scale 0.25)
		c["clock"] = float(c.get("clock", 0.0)) + dt
		if c["state"] == "windup":
			_tick_windup(g, c)
		else:
			_tick_flight(g, c)


func _tick_windup(g: int, c: Dictionary) -> void:
	# keeper.gd's halo: t = ticks since the cast start / (the release's ticks - 1), live until the release
	var t := clampf((float(c["clock"]) * 60.0 - 1.0) / float(int(c["release_ticks"]) - 1), 0.0, 1.0)
	var n: int = (fidx["halo"] as Array).size()
	var i := clampi(int(round(t * float(n - 1))), 0, n - 1)
	var at: Vector3 = (c["socket_fn"] as Callable).call()
	_put(g * slots + S_HALO, "halo", i, at + _toward(HALO_TOWARD_M), 0.0, 1.0)


func _tick_flight(g: int, c: Dictionary) -> void:
	var b: int = int(floor(float(c["clock"]) * 60.0 + 1e-4)) - 1   # the baked tick: 0 on the release's own step
	var base := g * slots
	_collapse(base + S_HALO)
	var th: float = c["theta"]
	var sock: Vector3 = c["socket"]
	var d: Vector3 = c["dir"]
	var alive := false
	# the travel (and its drain): the kit's own distance at this tick, along her facing
	var tr := _travel_at(b)
	if not tr.is_empty():
		var p: Vector3 = sock + d * (float(tr["dx"]) / PPM)
		c["node"] = p
		_put(base + S_TRAVEL, "travel", _frame_of("travel", b), p + _toward(-TRAVEL_BEHIND_M), th, 1.0)
		alive = true
	else:
		_collapse(base + S_TRAVEL)
	# the puff at the socket, turned to the aim
	var pf := _frame_of("puff", b)
	if pf >= 0:
		_put(base + S_PUFF, "puff", pf, sock + _toward(HALO_TOWARD_M), th, 1.0)
		alive = true
	else:
		_collapse(base + S_PUFF)
	# the cast floor at her feet: one frame, the kit's alpha
	var als: Array = meta["floor_alpha"].get("cast_floor", [])
	if b < als.size() and float(als[b]) > 0.0:
		_put_floor(base + S_CAST_FLOOR, "cast_floor", 0, feet_on_surface(c["feet"]), float(als[b]) / float(als[0]))
		alive = true
	else:
		_collapse(base + S_CAST_FLOOR)
	# the burst and its floor light, where the flight stopped
	var imp_key := "impact_%d" % int(c["set"])
	var fi := _frame_of(imp_key, b)
	if fi >= 0 and c.has("node"):
		var at: Vector3 = c.get("impact_at", c["node"])
		c["impact_at"] = at
		_put(base + S_IMPACT, imp_key, fi, at + _toward(BURST_TOWARD_M), 0.0, 1.0)
		if tighten:
			_mode2(base + S_IMPACT)
		alive = true
		var fl := _frame_of("impact_floor", b)
		if fl >= 0:
			_put_floor(base + S_IMPACT_FLOOR, "impact_floor", fl, _ground_under(at), 1.0)
			if tighten:
				_mode2(base + S_IMPACT_FLOOR)
		else:
			_collapse(base + S_IMPACT_FLOOR)
	else:
		_collapse(base + S_IMPACT)
		_collapse(base + S_IMPACT_FLOOR)
	# the trail motes, re-played by the kit's rule from its births (not on a birth tick: the kit's pool
	# shows a newborn mote one frame at its canvas origin, off the play frame)
	var lat := float(meta["motes"]["lateral_px"])
	var rise := float(meta["motes"]["rise_px_s"])
	for mi in 8:
		var slot := base + S_MOTES + mi
		if mi >= births.size():
			_collapse(slot)
			continue
		var bb: Dictionary = births[mi]
		var age := float(b - int(bb["birth_tick"])) / 60.0
		var life := float(bb["life_s"])
		if age <= 0.0 or age >= life:
			_collapse(slot)
			continue
		var bt := _travel_at(int(bb["birth_tick"]))
		var node0: Vector3 = sock + d * (float(bt["dx"]) / PPM)
		var off := Vector2(float(bb["origin_dx"]) - float(bt["dx"]), float(bb["origin_dy"]) - float(bt["dy"])).rotated(th)
		var ph := float(bb["phase"])
		off += Vector2(lat * (sin(ph + age * 8.0) - sin(ph)) * 0.5, -rise * age)
		var col: Array = bb["color"]
		_put_mote(slot, node0, off, float(bb["half_px"]), Color(float(col[0]), float(col[1]), float(col[2])), 1.0 - age / life)
		alive = true
	c["tick"] = b
	if not alive and b > impact_tick:
		casts[g] = {}
		_collapse_group(g)


# ---- instances ------------------------------------------------------------------------------------
func _screen_basis(theta: float) -> Basis:
	var b := cam.global_transform.basis
	var r := b.x.normalized()
	var dn := -b.y.normalized()
	var ex := (r * cos(theta) + dn * sin(theta)) / PPM
	var ey := (-r * sin(theta) + dn * cos(theta)) / PPM
	return Basis(ex, ey, b.z.normalized() * 0.01)


func _toward(m: float) -> Vector3:
	"""m metres toward the camera (negative: away) -- depth only: an ortho camera does not move it on screen."""
	return cam.global_transform.basis.z.normalized() * m


func _put(i: int, key: String, frame: int, at: Vector3, theta: float, alpha: float) -> void:
	mm.set_instance_transform(i, Transform3D(_screen_basis(theta), at))
	mm.set_instance_color(i, Color.WHITE)
	mm.set_instance_custom_data(i, Color(float((fidx[key] as Array)[frame]), alpha, 0.0, 0.0))


func _put_mote(i: int, anchor: Vector3, off_px: Vector2, half: float, colour: Color, alpha: float) -> void:
	var b := cam.global_transform.basis
	var at := anchor + (b.x.normalized() * off_px.x - b.y.normalized() * off_px.y) / PPM + _toward(-TRAVEL_BEHIND_M)
	mm.set_instance_transform(i, Transform3D(_screen_basis(0.0), at))
	mm.set_instance_color(i, colour)
	mm.set_instance_custom_data(i, Color(0.0, alpha, 1.0, half))


func _put_floor(i: int, key: String, frame: int, ground: Vector3, alpha: float) -> void:
	"""A floor light ON THE SNOW: a ground quad whose projection is the baked frame -- 1 px across is
	1/PPM m along u, 1 px down is 1/PXV m toward the camera along the ground. Lifted clear of the
	snow's relief, and slid toward the camera by as much as the lift raised it on screen."""
	var u: Vector3 = scene.u_hat
	var v: Vector3 = scene.v_hat
	var lift := FLOOR_LIFT_M
	var at := ground + Vector3(0.0, lift, 0.0) - v * (lift * PXH / PXV)
	mm.set_instance_transform(i, Transform3D(Basis(u / PPM, -v / PXV, Vector3.UP * 0.01), at))
	mm.set_instance_color(i, Color.WHITE)
	mm.set_instance_custom_data(i, Color(float((fidx[key] as Array)[frame]), alpha, 0.0, 0.0))


func _mode2(i: int) -> void:
	var c := mm.get_instance_custom_data(i)
	mm.set_instance_custom_data(i, Color(c.r, c.g, 2.0, c.a))


static func tighten_wanted() -> bool:
	var q := PaintStack.web_query("fb")
	var args := OS.get_cmdline_user_args()
	var i := args.find("--fb")
	if q == "" and i >= 0 and i + 1 < args.size():
		q = String(args[i + 1])
	# R-C9-118 (Matt: "I like the smaller fireball. It's perfect."): c75 is her DEFAULT; ?fb=full is the old burst
	return q.to_lower() != "full"


func _collapse(i: int) -> void:
	mm.set_instance_transform(i, _collapsed)
	mm.set_instance_custom_data(i, Color(0, 0, 0, 0))


func _collapse_group(g: int) -> void:
	for k in slots:
		_collapse(g * slots + k)


# ---- the baked record ----------------------------------------------------------------------------
func _travel_at(b: int) -> Dictionary:
	for t in travel:
		if int(t["tick"]) == b:
			return t
	return {}


func _frame_of(key: String, b: int) -> int:
	var ts: Array = ftick.get(key, [])
	var i := ts.find(b)
	return i


func _screen_angle(d: Vector3) -> float:
	var b := cam.global_transform.basis
	return atan2(d.dot(-b.y.normalized()), d.dot(b.x.normalized()))


func _surface_y(p: Vector3) -> float:
	"""The top of what she stands on at p: the snow (its trail included) where the field covers, else
	the Barrow's floor."""
	if scene.snow != null:
		return scene.snow.surface_y(Vector2(p.x, p.z))
	var uv: Vector2 = scene.world_to_uv(p)
	return scene.floor_y_at(uv.x, uv.y)


func _ground_under(p: Vector3) -> Vector3:
	"""The snow point that projects where p does: down the camera's own ray to the surface (twice, so a
	slope under the burst is followed)."""
	var fwd := -cam.global_transform.basis.z.normalized()
	var g := p
	for i in 2:
		var y0 := _surface_y(g)
		var t := (y0 - p.y) / fwd.y if absf(fwd.y) > 1e-4 else 0.0
		g = p + fwd * t
	return Vector3(g.x, _surface_y(g), g.z)


func feet_on_surface(feet: Vector3) -> Vector3:
	return Vector3(feet.x, _surface_y(feet), feet.z)
