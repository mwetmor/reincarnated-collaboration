extends RefCounted
class_name CliffWorld
## C-9 R-C9-66 (T7-A): everything that stands ON the projected cliffside.
##
## The plate is only the GROUND AND ROCK painting. The 2D route composites the trees,
## crates, stumps and bridge furniture as separate prop sprites over it (props.json:
## 49 assets, 49 instances), which is why a first comparison of plate-against-2D showed
## every tree in the disagreement map: they were never in the plate to project.
##
## Here each prop becomes a CARD standing at the place the prop stands, found by
## raycasting the real geometry rather than assumed flat. That buys the thing this whole
## test is for: a character walks BEHIND a tree because the tree is in front of it in
## three dimensions, not because a y-sort said so.

const PPM := 100.617553710938
const V4_UMIN := -23.2673988342285
const V4_VMAX := 18.5067100524902
const CHAR_LAYER := 4
const TERRAIN_BIT := 1 << 1          # the collision layer the projected terrain lives on
const PITCH_COS := 0.602462407085    # cos(PL_PITCH_DEG); a vertical metre's screen share
const PROP_LIFT := 0.0               # see build_props: a lift is a misregistration
const HALF_VIEW := Vector2(960.0, 540.0)   # the 2D route's own half-view, in canvas px


static func canvas_to_plane(px: Vector2, right: Vector3, up: Vector3) -> Vector3:
	return right * (V4_UMIN + px.x / PPM) + up * (V4_VMAX - px.y / PPM)


# --- collision, which the greybox has none of ---------------------------------
static func add_collision(fg: Array, owner: Node) -> int:
	"""Trimesh bodies for the foreground.

	The builder is a RENDER greybox -- it was made to be photographed, not walked on, so
	it ships no collision at all. Trimesh from the same meshes keeps the walking surface
	and the painting in exact agreement: a character cannot stand somewhere the painting
	does not show ground, because it is the same triangles."""
	var n := 0
	for mi in fg:
		var m := mi as MeshInstance3D
		if m.mesh == null:
			continue
		var body := StaticBody3D.new()
		# ITS OWN COLLISION LAYER, so ground_at can ask for the GROUND and get it.
		body.collision_layer = TERRAIN_BIT
		body.collision_mask = 0
		var shape := CollisionShape3D.new()
		shape.shape = m.mesh.create_trimesh_shape()
		body.add_child(shape)
		m.add_child(body)
		body.global_transform = m.global_transform
		n += 1
	return n


static func ground_at(space: PhysicsDirectSpaceState3D, px: Vector2, right: Vector3,
					  up: Vector3, fwd: Vector3) -> Dictionary:
	"""Where on the real geometry a canvas pixel lands.

	Cast along the guide camera's own view direction, because that is the ray the
	painter's pixel travelled: whatever it hits is the surface that pixel is painted on.
	Placing props by assuming a flat ground would put them through the rock wherever the
	ground is not flat, which on a cliffside is most of it."""
	var from := canvas_to_plane(px, right, up) - fwd * 150.0
	var q := PhysicsRayQueryParameters3D.create(from, from + fwd * 400.0)
	q.collide_with_areas = false
	# TERRAIN ONLY, and this is not tidiness. The ray starts 150 m in FRONT of the guide
	# plane and travels away from the camera, so anything standing between the camera and
	# the ground is hit FIRST -- including the character's own capsule. Unmasked, asking
	# "where is the ground under this canvas pixel" while the walker is near that pixel
	# returns a point on the WALKER, and placing him there moves him onto his own shoulder,
	# a metre and a half off the ground, every frame. That is what put the stand-in 500 px
	# from where the record said he was during the bridge-post sweep.
	q.collision_mask = TERRAIN_BIT
	var hit := space.intersect_ray(q)
	return hit


# --- props as cards -----------------------------------------------------------
static func card_mesh(w_m: float, h_m: float) -> QuadMesh:
	var q := QuadMesh.new()
	q.size = Vector2(w_m, h_m)
	return q


static func card_material(tex: Texture2D) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
// Unlit, like the plate: a painted prop carries its own light. Alpha-scissor rather
// than blending so the cards SORT BY DEPTH like solid geometry -- which is the entire
// point of putting them in 3D. Alpha blending would put them back in a painter's-order
// queue and hand back the sorting problem the 2D route already has.
//
// AND IT MUST NOT ASSIGN `ALPHA`. `discard` is the scissor; writing ALPHA = 1.0 next to
// it says "opaque" to a reader and "transparent" to Godot, which puts the card in the
// alpha pass with no depth write and no depth sort. That is what made the cards
// invisible -- see the note on the projector shader in cliffside3d.gd. Leaving ALPHA
// alone keeps the material opaque, which is what a tree is.
render_mode unshaded, cull_disabled, depth_draw_opaque, shadows_disabled;
uniform sampler2D tex : source_color, filter_linear_mipmap;
uniform float cutoff = 0.35;
void fragment() {
	vec4 c = texture(tex, UV);
	if (c.a < cutoff) discard;
	ALBEDO = c.rgb;
}
"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("tex", tex)
	return m


static func layer_material(tex: Texture2D) -> ShaderMaterial:
	"""Soft painted layers: ALPHA-BLENDED, not scissored.
	
	The props are cut out with a scissor so they sort like solid geometry, which is what
	a tree wants. A mist bank does not: it is soft everywhere, and a scissor either eats
	its edge or -- at a threshold low enough to keep it -- lets through pixels whose
	alpha is near zero and whose RGB is therefore whatever the painter left in the
	transparent region. That is what turned the chasm into a flat magenta band: not a
	colour-space bug but undefined colour under an alpha nobody was meant to see.
	
	These cards are behind everything and never intersect, so blending costs no sorting."""
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, cull_disabled, blend_mix, depth_draw_never, shadows_disabled;
uniform sampler2D tex : source_color, filter_linear_mipmap;
void fragment() {
	vec4 c = texture(tex, UV);
	ALBEDO = c.rgb;
	ALPHA = c.a;
}
"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("tex", tex)
	return m


static func build_props(root: Node3D, space: PhysicsDirectSpaceState3D, dir: String,
						right: Vector3, up: Vector3, fwd: Vector3) -> Dictionary:
	"""All 49 of props.json's instances, as cards standing on the real geometry.

	`dir` is a res:// path, NOT a globalized one. The earlier version globalized it, which
	works in the editor -- Godot's importer will resolve an absolute path via the .import
	file sitting next to it -- and cannot work in an exported build, where res:// lives in
	the pck and globalize_path returns a filename that is not on disk. Same trap the zones
	PNG fell into. Every asset here is loaded through res:// so the editor run and the
	.app load the same bytes by the same route."""
	var data = JSON.parse_string(FileAccess.get_file_as_string(dir + "/props.json"))
	if typeof(data) != TYPE_DICTIONARY:
		return {"error": "no props.json"}
	var assets := {}
	for a in data["assets"]:
		assets[String(a["name"])] = a
	var holder := Node3D.new()
	holder.name = "Props"
	root.add_child(holder)
	# horizontal screen axis and true world up. `right` already has y = 0 under this
	# camera, so `flat` is `right`; it is recomputed rather than assumed.
	var flat := right
	flat.y = 0.0
	flat = flat.normalized()
	var n := flat.cross(Vector3.UP)
	var placed := 0
	var missed := 0
	var no_ground := 0
	var clearance := []
	for inst in data["instances"]:
		var a = assets.get(String(inst["asset"]))
		if a == null:
			missed += 1
			continue
		var path := dir + "/" + String(a["file"])
		if not ResourceLoader.exists(path):
			missed += 1
			continue
		var tex: Texture2D = load(path)
		var pos := Vector2(float(inst["position"][0]), float(inst["position"][1]))
		var anc := Vector2(float(a["anchor"][0]), float(a["anchor"][1]))
		var w := float(tex.get_width())
		var h := float(tex.get_height())
		var hit := ground_at(space, pos, right, up, fwd)
		if hit.is_empty():
			no_ground += 1
		var base: Vector3 = hit["position"] if not hit.is_empty() else \
			canvas_to_plane(pos, right, up)
		var mi := MeshInstance3D.new()
		mi.name = String(inst["asset"])
		# A card that STANDS UP IN THE WORLD, not one lying in the guide camera's plane.
		# A card in the guide plane carries ONE depth over its whole height, so a rising
		# slope behind it cuts through it; standing it vertically gives it the depth
		# gradient a real tree has. To cover the same screen pixels the painter painted it
		# is then stretched by 1/cos(pitch): a vertical metre spends only cos(pitch) of a
		# metre on screen at this elevation.
		var h_world := (h / PPM) / PITCH_COS
		mi.mesh = card_mesh(w / PPM, h_world)
		mi.material_override = card_material(tex)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		holder.add_child(mi)
		# WHERE THE CARD'S CENTRE GOES, above the anchor.
		#
		# The anchor is `anc.y` px BELOW the sprite's top, so it is `h - anc.y` px above
		# the sprite's bottom, so the sprite's centre is (anc.y - h/2) px ABOVE it. The
		# previous form was h_world*0.5*(1 - anc.y/h), which is the mirror of that: for a
		# foot-anchored sprite (anc.y = h, the common case here) it returns 0 and buries
		# half the card -- 4.55 m for tree_living_a, which is most of a tree.
		var lift := h_world * (anc.y / maxf(h, 1.0) - 0.5)
		var centre := base + Vector3.UP * (lift + PROP_LIFT) \
			+ flat * ((w * 0.5 - anc.x) / PPM)
		# CLEARANCE, measured rather than biased. A card standing at the ground point can
		# still be cut by terrain that rises in front of it. Sample the real surface over
		# the card's own screen rect and push the card forward by exactly the worst
		# overlap found, plus a 2 cm margin -- no more. A fixed bias large enough for the
		# worst prop would float every other one in front of the character, which is the
		# one thing the occlusion view exists to show.
		var bias := _clearance(space, pos, anc, w, h, h_world, base, right, up, fwd)
		if bias > 0.0:
			clearance.append(snappedf(bias, 0.01))
		mi.global_transform = Transform3D(Basis(flat, Vector3.UP, n), centre - fwd * bias)
		mi.set_meta("anchor_px", pos)
		placed += 1
	clearance.sort()
	return {"placed": placed, "asset_missing": missed, "no_ground_hit": no_ground,
			"instances": (data["instances"] as Array).size(),
			"needed_clearance": clearance.size(),
			"clearance_max_m": clearance[-1] if clearance.size() > 0 else 0.0}


static func _clearance(space: PhysicsDirectSpaceState3D, pos: Vector2, anc: Vector2,
					   w: float, h: float, h_world: float, base: Vector3,
					   right: Vector3, up: Vector3, fwd: Vector3) -> float:
	"""How far forward this card must move so the terrain stops cutting it.

	For a grid of points over the card's canvas rect: the card's own depth there (it is
	vertical, so depth falls by dot(UP, fwd) per metre of height) against the terrain's
	depth on the same ray. The answer is the largest amount by which the card is BEHIND
	the surface it is painted over, and zero when it never is."""
	var dy := Vector3.UP.dot(fwd)            # how much nearer a metre of height is
	var top_px := pos.y - anc.y              # the sprite's top edge, in canvas y
	var bot_px := top_px + h                 # and its bottom edge
	var base_d := base.dot(fwd)
	var foot_y := h_world * (anc.y / maxf(h, 1.0) - 1.0) + PROP_LIFT   # card bottom, rel. base
	var worst := 0.0
	for iy in 6:
		var y_px: float = bot_px - (bot_px - top_px) * (float(iy) / 5.0)
		var m_above: float = (bot_px - y_px) / maxf(h, 1.0) * h_world  # metres up the card
		var card_depth: float = base_d + (foot_y + m_above) * dy
		for ix in 5:
			var x_px: float = pos.x - anc.x + w * (float(ix) / 4.0)
			var g := ground_at(space, Vector2(x_px, y_px), right, up, fwd)
			if g.is_empty():
				continue
			worst = maxf(worst, card_depth - (g["position"] as Vector3).dot(fwd))
	return (worst + 0.02) if worst > 0.0 else 0.0


# --- the painted background, as cards at their parallax depths -----------------
static func build_plate_backdrop(root: Node3D, plate: Texture2D, canvas: Vector2,
								 right: Vector3, up: Vector3, fwd: Vector3,
								 depth: float) -> Dictionary:
	"""The part of the PAINTING that has no geometry to land on.

	The plate is 54% opaque and 40% transparent, and the transparent part is where the 2D
	route lets its parallax layers through. The opaque part is not all terrain: the painter
	also put the chasm's clouds, and the haze along its far lip, INTO the plate -- they are
	Foreground pixels in the 2D, drawn over every parallax layer. Projected onto geometry
	they vanish, because there is no geometry in a chasm. That was the single largest
	remaining disagreement with the 2D: at the bridge, a block of 120x120 px differing by
	78/255, and sampling it settles what it is -- screen (930,810) reads [253 216 180] in
	the live 2D and plate_v4.png reads [253 216 180] at the canvas pixel under it, exactly,
	while the 3D read the forest layer behind it.

	So: one quad, the size of the canvas, lying in the GUIDE PLANE -- canvas-locked, like
	the painting it carries, not screen-locked like the parallax -- wearing the same
	projection the terrain wears, discarding where the plate is transparent. It sits just
	BEHIND the farthest terrain, so every real surface still wins, and in FRONT of the
	parallax cards, which is the 2D's own z order (Foreground 0 over mist -10 over forest
	-20 over ruins -30 over sky -40)."""
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
// The same world -> canvas map the projector uses, deliberately: one derivation of the
// camera, not two that resemble each other. Alpha-blended and depth_draw_never because
// this IS the painting's own alpha -- the 40% of the plate the painter left clear so the
// parallax could show through.
render_mode unshaded, cull_disabled, blend_mix, depth_draw_never, shadows_disabled;
uniform sampler2D plate : source_color, filter_linear_mipmap;
uniform vec3 axis_right;
uniform vec3 axis_up;
uniform float ppm;
uniform float umin;
uniform float vmax;
uniform vec2 canvas;
varying vec3 world_pos;
void vertex() { world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }
void fragment() {
	float x_px = (dot(world_pos, axis_right) - umin) * ppm;
	float y_px = (vmax - dot(world_pos, axis_up)) * ppm;
	vec2 uv = vec2(x_px / canvas.x, y_px / canvas.y);
	if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) discard;
	vec4 c = texture(plate, uv);
	if (c.a < 0.02) discard;
	ALBEDO = c.rgb;
	ALPHA = c.a;
}
"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("plate", plate)
	m.set_shader_parameter("axis_right", right)
	m.set_shader_parameter("axis_up", up)
	m.set_shader_parameter("ppm", PPM)
	m.set_shader_parameter("umin", V4_UMIN)
	m.set_shader_parameter("vmax", V4_VMAX)
	m.set_shader_parameter("canvas", canvas)
	var mi := MeshInstance3D.new()
	mi.name = "PlateBackdrop"
	mi.mesh = card_mesh(canvas.x / PPM, canvas.y / PPM)
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	root.add_child(mi)
	var centre := canvas_to_plane(canvas * 0.5, right, up)
	centre = centre - fwd * (centre.dot(fwd) - depth)
	mi.global_transform = Transform3D(Basis(right, up, -fwd), centre)
	return {"depth_m": snappedf(depth, 0.01),
			"size_m": [snappedf(canvas.x / PPM, 0.01), snappedf(canvas.y / PPM, 0.01)]}


static func build_background(root: Node3D, layers_dir: String, parallax_json: String,
							 right: Vector3, up: Vector3, fwd: Vector3,
							 base_depth: float) -> Array:
	"""The four painted layers, as cards behind the geometry.
	
	AN ORTHOGRAPHIC CAMERA CANNOT PARALLAX, and that is worth stating plainly because
	the first version of this function assumed it could. Under orthographic projection a
	card's distance changes neither its size on screen nor how fast it slides when the
	camera moves -- everything at every depth translates together. Placing the sky at
	1632 m and scaling it 8.3x to compensate, as a perspective reading of `scroll_scale`
	would have you do, produces a sky eight times too big that still does not parallax.

	So depth here buys ORDERING and nothing else, matching the 2D route's z_index: sky
	-40, far_ruins -30, forest_valley -20, mist -10. The scroll rate is a compositing
	device the 2D applies by hand, so it is applied by hand here too, in place().

	THE PLACEMENT LAW IS MEASURED, not read off the file. parallax.json gives each layer a
	`position`, and the previous version treated that as an absolute canvas position --
	which put the forest 1027 px too high, over the band where the 2D shows the violet
	ruins. Godot's Parallax2D does not use it that way. Interrogating the LIVE 2D scene at
	four camera points (tools/probe_2d_layers.gd in the chartest project; each layer's
	get_global_transform_with_canvas()) gives, to the last decimal place:

	    layer top-left, in canvas px  =  P + (1 - s) * (camera_aim - HALF_VIEW)

	so `position` is an offset from a camera-relative origin, not a canvas coordinate. The
	same measurement confirms the drift: over a 1000 px camera move each layer's canvas
	position advanced by exactly (1-s)*1000, and its SCREEN position by -s*1000."""
	var pj = JSON.parse_string(FileAccess.get_file_as_string(parallax_json))
	var out := []
	if typeof(pj) != TYPE_DICTIONARY:
		return out
	var holder := Node3D.new()
	holder.name = "Background"
	root.add_child(holder)
	# BEHIND the plate backdrop, in the 2D's own z order: sky farthest, mist nearest.
	var depth := base_depth + 32.0
	for L in pj["layers"]:
		var file := String(L["file"]).get_file()
		var path := layers_dir + "/" + file
		if not ResourceLoader.exists(path):
			continue
		var tex: Texture2D = load(path)
		var s := maxf(float(L["scroll_scale"]), 0.0)
		var pos_px := Vector2(float(L["position"][0]), float(L["position"][1]))
		var w := float(tex.get_width())
		var h := float(tex.get_height())
		var mi := MeshInstance3D.new()
		mi.name = String(L["name"])
		mi.mesh = card_mesh(w / PPM, h / PPM)      # natural size: ortho, so depth is free
		mi.material_override = layer_material(tex)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		holder.add_child(mi)
		mi.set_meta("scroll_scale", s)
		# the layer's centre offset from its top-left, in canvas px
		mi.set_meta("p_px", pos_px + Vector2(w, h) * 0.5)
		mi.set_meta("order_depth", depth)
		var lm := _add_landmarks(mi, layers_dir, String(L["name"]), Vector2(w, h))
		out.append({"name": String(L["name"]), "scroll_scale": s, "z": int(L.get("z", 0)),
					"p_px": [pos_px.x, pos_px.y], "order_depth_m": depth,
					"landmarks": lm,
					"size_m": [snappedf(w / PPM, 0.01), snappedf(h / PPM, 0.01)]})
		depth -= 8.0
	return out


static func _add_landmarks(layer: MeshInstance3D, layers_dir: String, layer_name: String,
						   layer_px: Vector2) -> Array:
	"""The cathedral and the tower that ride the far-ruins layer.

	They are Sprite2D CHILDREN of Layer_far_ruins in the 2D scene -- not entries in
	parallax.json, which is why the first 3D background had a skyline with nothing on it.
	Making them children of the layer card here reproduces that exactly: they inherit the
	layer's parallax by construction instead of having the same rate applied to them a
	second time, and their z_index becomes a few centimetres toward the camera."""
	var out := []
	if not FileAccess.file_exists("res://data/landmarks.json"):
		return out
	var j = JSON.parse_string(FileAccess.get_file_as_string("res://data/landmarks.json"))
	if typeof(j) != TYPE_DICTIONARY:
		return out
	for lm in j.get("landmarks", []):
		if String(lm.get("layer", "")) != layer_name:
			continue
		var path := layers_dir + "/" + String(lm["file"])
		if not ResourceLoader.exists(path):
			continue
		var tex: Texture2D = load(path)
		var k := float(lm.get("scale", 1.0))
		var sz := Vector2(tex.get_width(), tex.get_height()) * k
		var pos := Vector2(float(lm["position"][0]), float(lm["position"][1]))
		var mi := MeshInstance3D.new()
		mi.name = "Landmark_" + String(lm["name"])
		mi.mesh = card_mesh(sz.x / PPM, sz.y / PPM)
		mi.material_override = layer_material(tex)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		layer.add_child(mi)
		# offset of this sprite's centre from the layer sprite's centre, in canvas px
		var off := (pos + sz * 0.5) - layer_px * 0.5
		mi.position = Vector3(off.x / PPM, -off.y / PPM,
							  0.2 + 0.1 * float(lm.get("z_index", 0)))
		out.append({"name": String(lm["name"]), "size_px": [snappedf(sz.x, 0.1), snappedf(sz.y, 0.1)],
					"offset_px": [snappedf(off.x, 0.1), snappedf(off.y, 0.1)]})
	return out


static func place_background(root: Node3D, aim_px: Vector2, aim: Vector3,
							 r: Vector3, u: Vector3, f: Vector3) -> void:
	"""Put every layer where the live 2D puts it, for THIS camera aim.

	Computed from the aim each time rather than accumulated from a home position: an
	offset that is re-derived cannot drift out of step with the camera, and the law above
	is closed-form anyway.

	The cards are built in the CURRENT camera's basis (r, u, f), not the fixed guide
	basis. A screen-space backdrop is what the 2D has; carrying it in the camera's own
	frame keeps it a backdrop when the camera orbits, instead of turning it edge-on."""
	var holder := root.get_node_or_null(^"Background")
	if holder == null:
		return
	for c in holder.get_children():
		var mi := c as MeshInstance3D
		if mi == null or not mi.has_meta("scroll_scale"):
			continue
		var s: float = mi.get_meta("scroll_scale")
		var p: Vector2 = mi.get_meta("p_px")
		var d: float = mi.get_meta("order_depth")
		# centre, in canvas px, then as an offset from where the camera is looking
		var off: Vector2 = (p + (1.0 - s) * (aim_px - HALF_VIEW)) - aim_px
		mi.global_transform = Transform3D(Basis(r, u, -f),
			aim + r * (off.x / PPM) - u * (off.y / PPM) + f * d)


# --- lights, for the character only -------------------------------------------
static func build_lights(root: Node3D, space: PhysicsDirectSpaceState3D, props_dir: String,
						 right: Vector3, up: Vector3, fwd: Vector3, yaw_deg: float) -> Dictionary:
	"""A sunset key from screen-left plus warm points at the painted fires.

	EVERY light here is masked to the character's own visual layer. The painting is a
	painting: it already has a sun in it, and its shadows were painted where the painter
	wanted them. Lighting it again would lay a second sun over the first. The character
	is the only thing in the scene that is not already lit, so it is the only thing lit.

	The fire positions are not invented -- they are props.json's `glows`, which is where
	the 2D route puts its flickering fire glows, so the point lights stand exactly where
	the painted flames are."""
	var holder := Node3D.new()
	holder.name = "Lights"
	root.add_child(holder)
	var key := DirectionalLight3D.new()
	key.name = "Sunset"
	key.light_energy = 1.15
	key.light_color = Color(1.0, 0.76, 0.52)
	key.light_cull_mask = CHAR_LAYER
	key.shadow_enabled = false     # nothing else is lit, so there is nothing to catch one
	holder.add_child(key)
	# low, from screen-left: in the level's own screen-aligned frame, +x is screen right
	var d_local := Vector3(0.92, -0.34, 0.18).normalized()
	var d_world: Vector3 = Basis(Vector3.UP, deg_to_rad(yaw_deg)) * d_local
	key.look_at_from_position(Vector3.ZERO, d_world, Vector3.UP)

	var fires := []
	var data = JSON.parse_string(FileAccess.get_file_as_string(props_dir + "/props.json"))
	if typeof(data) == TYPE_DICTIONARY:
		for g in data.get("glows", []):
			var px := Vector2(float(g["position"][0]), float(g["position"][1]))
			var hit := ground_at(space, px, right, up, fwd)
			if hit.is_empty():
				continue
			var o := OmniLight3D.new()
			o.light_cull_mask = CHAR_LAYER
			o.light_color = Color(float(g["color"][0]), float(g["color"][1]), float(g["color"][2]))
			o.light_energy = 3.2
			o.omni_range = 6.0
			o.shadow_enabled = false
			holder.add_child(o)
			o.global_position = (hit["position"] as Vector3) + Vector3.UP * 0.6
			fires.append([px.x, px.y])
	return {"key_dir_world": [d_world.x, d_world.y, d_world.z], "fires": fires}
