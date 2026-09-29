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
const PITCH_COS := 0.602462407085    # cos(PL_PITCH_DEG); a vertical metre's screen share
const PROP_LIFT := 0.05              # a hair off the ground, to break the surface tie


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
render_mode unshaded, cull_disabled, depth_draw_opaque, shadows_disabled;
uniform sampler2D tex : source_color, filter_linear_mipmap;
uniform float cutoff = 0.35;
void fragment() {
	vec4 c = texture(tex, UV);
	if (c.a < cutoff) discard;
	ALBEDO = c.rgb;
	ALPHA = 1.0;
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
	var data = JSON.parse_string(FileAccess.get_file_as_string(dir + "/props.json"))
	if typeof(data) != TYPE_DICTIONARY:
		return {"error": "no props.json"}
	var assets := {}
	for a in data["assets"]:
		assets[String(a["name"])] = a
	var holder := Node3D.new()
	holder.name = "Props"
	root.add_child(holder)
	var placed := 0
	var missed := 0
	var no_ground := 0
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
		# the sprite's own centre, in canvas pixels, with its anchor on `pos`
		var centre_px := pos - anc + Vector2(w, h) * 0.5
		var hit := ground_at(space, pos, right, up, fwd)
		var depth := 0.0
		if hit.is_empty():
			no_ground += 1
		else:
			# how far along the view ray the ground sits, so the card sorts with it
			depth = (hit["position"] as Vector3).dot(fwd)
		var mi := MeshInstance3D.new()
		mi.name = String(inst["asset"])
		# A card that STANDS UP IN THE WORLD, not one lying in the guide camera's plane.
		#
		# The flat version was swallowed by the terrain and it took a while to see why,
		# because physics said there was nothing in the way: the raycast found the ground
		# at depth -6.77 and the card sat at -11.77, five metres nearer, and it still
		# never drew. The error was not in the depth of the card's ORIGIN but in the
		# depth of everything above it. A card in the guide plane has CONSTANT depth over
		# its whole height, while the ground behind it does not: rising a metre in world
		# Y moves a surface sin(pitch) = 0.80 m NEARER the camera, so a slope or a cliff
		# face climbs toward the viewer as it climbs the screen and cuts straight through
		# a tall flat card. Biasing the card forward only postponed that -- it needed
		# 80 m to clear, which should have been the clue that the fix was not a bias.
		#
		# Standing the card vertically gives it the same depth gradient as the world it
		# stands in, which is what a real tree has. To look the same as the painted
		# sprite it is then stretched by 1/cos(pitch): a vertical metre only spends
		# cos(pitch) of a metre on screen at this elevation, so the card must be that
		# much taller to cover the pixels the painter painted.
		var h_world := (h / PPM) / PITCH_COS
		mi.mesh = card_mesh(w / PPM, h_world)
		mi.material_override = card_material(tex)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		holder.add_child(mi)
		var base := canvas_to_plane(Vector2(centre_px.x, pos.y), right, up)
		base = base - fwd * (base.dot(fwd) - depth)
		if not hit.is_empty():
			base = hit["position"]
			base.x = (canvas_to_plane(Vector2(centre_px.x, pos.y), right, up)).x if false else base.x
		# horizontal axis that faces the camera, and true world up
		var flat := right
		flat.y = 0.0
		flat = flat.normalized()
		var n := flat.cross(Vector3.UP)
		mi.global_transform = Transform3D(Basis(flat, Vector3.UP, n),
			base + Vector3.UP * (h_world * 0.5 * (1.0 - float(anc.y) / maxf(h, 1.0)) + PROP_LIFT)
			+ flat * ((centre_px.x - pos.x) / PPM))
		placed += 1
	return {"placed": placed, "asset_missing": missed, "no_ground_hit": no_ground,
			"instances": (data["instances"] as Array).size()}


# --- the painted background, as cards at their parallax depths -----------------
static func build_background(root: Node3D, layers_dir: String, parallax_json: String,
							 right: Vector3, up: Vector3, fwd: Vector3,
							 _unused: float) -> Array:
	"""The four painted layers, as cards behind the geometry.
	
	AN ORTHOGRAPHIC CAMERA CANNOT PARALLAX, and that is worth stating plainly because
	the first version of this function assumed it could. Under orthographic projection a
	card's distance changes neither its size on screen nor how fast it slides when the
	camera moves -- everything at every depth translates together. Placing the sky at
	1632 m and scaling it 8.3x to compensate, as a perspective reading of `scroll_scale`
	would have you do, produces a sky eight times too big that still does not parallax.
	
	So depth here buys ORDERING and nothing else: each card sits just far enough back to
	be behind the geometry and behind the layer in front of it. The scroll rate is not a
	geometric fact at all -- it is a compositing device the 2D route applies by hand --
	so it is applied by hand here too, in drift(), as an offset proportional to how far
	the camera has moved. That is the honest reconstruction: the 2D scene's parallax was
	never geometry, and dressing it up as geometry would be a worse lie than copying it.
	
	The alternative is a perspective game camera, which would parallax for free and
	would stop the projected plate matching the 2D route pixel for pixel. That trade is
	in the report, not decided here."""
	var pj = JSON.parse_string(FileAccess.get_file_as_string(parallax_json))
	var out := []
	if typeof(pj) != TYPE_DICTIONARY:
		return out
	var holder := Node3D.new()
	holder.name = "Background"
	root.add_child(holder)
	var depth := 60.0
	for L in pj["layers"]:
		var file := String(L["file"]).get_file()
		var path := layers_dir + "/" + file
		if not ResourceLoader.exists(path):
			continue
		var tex: Texture2D = load(path)
		var s := maxf(float(L["scroll_scale"]), 0.02)
		var pos_px := Vector2(float(L["position"][0]), float(L["position"][1]))
		var w := float(tex.get_width())
		var h := float(tex.get_height())
		var centre_px := pos_px + Vector2(w, h) * 0.5
		var mi := MeshInstance3D.new()
		mi.name = String(L["name"])
		mi.mesh = card_mesh(w / PPM, h / PPM)      # natural size: ortho, so depth is free
		mi.material_override = layer_material(tex)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		holder.add_child(mi)
		var centre := canvas_to_plane(centre_px, right, up)
		centre = centre - fwd * (centre.dot(fwd) - depth)
		mi.global_transform = Transform3D(Basis(right, up, -fwd), centre)
		mi.set_meta("scroll_scale", s)
		mi.set_meta("home", centre)
		out.append({"name": String(L["name"]), "scroll_scale": s,
					"order_depth_m": depth, "size_m": [snappedf(w / PPM, 0.01), snappedf(h / PPM, 0.01)]})
		depth -= 8.0
	return out


static func drift(root: Node3D, cam_aim: Vector3, home_aim: Vector3,
				  right: Vector3, up: Vector3) -> void:
	"""Apply the 2D route's parallax by hand, since the camera cannot.
	
	A layer at scroll_scale s moves s times as fast as the world, so relative to the
	world it LAGS by (1 - s) of the camera's travel. Same arithmetic the 2D route does,
	written where it belongs: on the thing that is pretending to be far away."""
	var holder := root.get_node_or_null(^"Background")
	if holder == null:
		return
	var d := cam_aim - home_aim
	var du := d.dot(right)
	var dv := d.dot(up)
	for c in holder.get_children():
		var mi := c as MeshInstance3D
		if mi == null or not mi.has_meta("scroll_scale"):
			continue
		var s: float = mi.get_meta("scroll_scale")
		var home: Vector3 = mi.get_meta("home")
		var lag := (1.0 - s)
		mi.global_position = home + right * (du * lag) + up * (dv * lag)


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
