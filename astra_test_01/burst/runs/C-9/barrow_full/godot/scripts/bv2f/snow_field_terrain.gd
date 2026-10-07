extends SnowField
## BV2F lane PT, DEV-18 (R-C9-193): v1's snow field ON THE TERRAIN, pilot-only. v1's scripts/snow_field.gd is untouched:
## this SUBCLASS (barrow_full.gd types `var snow: SnowField`, so a free-standing copy could not be assigned) overrides
## only what reads the flat floor. With no ground height set, ground_h_at() is 0 and every override is v1's code.
##   * _make_material(): v1's shader + the ruled vertex lift (`VERTEX.y += h + ground_h_on * texture(ground_h_tex, UV).r`)
##     applied as asserted string swaps to whichever code v1 would use (SHADER or shader_code_override, e.g. the painted
##     snow of PaintedWorld.snow_shader_code()); the field's plane UV IS the ground-height grid (the depth grid's layout).
##   * _physics_process() / surface_y(): v1's bodies COPIED (barrow_full/godot/scripts/snow_field.gd), floor_y + the
##     ground height on the marked lines (the stamp's lift test, the puff, the surface) -- else no print on a slope.
## The painted snow's undisturbed-surface projection includes the ground height (third swap).
## The snow keeps v1's flat-field normal (R-C9-193: the base colour is the painting; only the print relief is affected).

var ground_h_buf := PackedFloat32Array()     # nx * nz metres, row = z (bv2f_prep.py snow_ground_h.bin)
var gh_origin := Vector2.ZERO
var gh_cell := 0.1
var gh_nx := 0
var gh_nz := 0
var ground_h_tex: Texture2D = null


func set_ground_height(buf: PackedFloat32Array, origin: Vector2, cell: float, nx: int, nz: int) -> void:
	ground_h_buf = buf
	gh_origin = origin
	gh_cell = cell
	gh_nx = nx
	gh_nz = nz
	var img := Image.create_from_data(nx, nz, false, Image.FORMAT_RF, buf.to_byte_array())
	ground_h_tex = ImageTexture.create_from_image(img)


func ground_h_at(xz: Vector2) -> float:
	if ground_h_buf.is_empty():
		return 0.0
	var fx := clampf((xz.x - gh_origin.x) / gh_cell, 0.0, float(gh_nx - 1))
	var fz := clampf((xz.y - gh_origin.y) / gh_cell, 0.0, float(gh_nz - 1))
	var i0 := mini(int(fx), gh_nx - 2)
	var j0 := mini(int(fz), gh_nz - 2)
	var tx := fx - float(i0)
	var tz := fz - float(j0)
	var a := ground_h_buf[j0 * gh_nx + i0]
	var b := ground_h_buf[j0 * gh_nx + i0 + 1]
	var c := ground_h_buf[(j0 + 1) * gh_nx + i0]
	var d := ground_h_buf[(j0 + 1) * gh_nx + i0 + 1]
	return (a * (1.0 - tx) + b * tx) * (1.0 - tz) + (c * (1.0 - tx) + d * tx) * tz


static func terrain_code(code: String) -> String:
	## the ruled two-line shader change (fid/pt/dev18/c_snow_field_terrain_copy.diff), each swap asserted
	assert(code.count("uniform float floor_y;\n") == 1, "snow terrain: floor_y uniform not found once")
	assert(code.count("\tVERTEX.y += h;\n") == 1, "snow terrain: the vertex lift not found once")
	code = code.replace("uniform float floor_y;\n", "uniform float floor_y;\nuniform sampler2D ground_h_tex : filter_linear, repeat_disable;   // BV2F-PT DEV-18\nuniform float ground_h_on = 0.0;   // BV2F-PT DEV-18\n")
	# R-C9-205 (3): the ground height is taken ONCE, at the vertex, and carried to the fragment (v_gh) -- the projection
	# below used to re-sample the grid per fragment (bilinear), which on a steep bank is not the height the triangle was
	# lifted to (piecewise linear between vertices): the paint was then read off the wrong height (white wavy streaks,
	# tents round the bank's tufts -- M2' slopes sheet)
	code = code.replace("uniform float ground_h_on = 0.0;   // BV2F-PT DEV-18\n", "uniform float ground_h_on = 0.0;   // BV2F-PT DEV-18\nvarying float v_gh;   // BV2F-PT R-C9-205\n")
	code = code.replace("\tVERTEX.y += h;\n", "\tv_gh = ground_h_on * textureLod(ground_h_tex, UV, 0.0).r;   // BV2F-PT R-C9-205\n\tVERTEX.y += h + v_gh;   // BV2F-PT DEV-18\n")
	# THE PAINTED SNOW (PaintedWorld.snow_shader_code) projects the painting at the UNDISTURBED surface,
	# floor_y + D: on the terrain that surface is the ground height higher -- else the paint is sampled
	# h x 60.6 px too low on every slope (seen as streaks on the stream banks and the mound flank)
	var und := "guide_uv(vec3(v_world.x, floor_y + D, v_world.z))"
	if code.count(und) == 1:   # the painted path only (v1's SHADER has no projection)
		code = code.replace(und, "guide_uv(vec3(v_world.x, floor_y + D + v_gh, v_world.z))")   # BV2F-PT DEV-18 / R-C9-205: the vertex's own ground height
	return code


func _make_material() -> ShaderMaterial:
	if ground_h_tex != null:
		shader_code_override = terrain_code(shader_code_override if shader_code_override != "" else SHADER)
	var m := super._make_material()
	if ground_h_tex != null:
		m.set_shader_parameter("ground_h_tex", ground_h_tex)
		m.set_shader_parameter("ground_h_on", 1.0)
	return m


func _physics_process(dt: float) -> void:  # BV2F-PT DEV-18 copy
	# THE RIG'S AnimationPlayer RUNS ON THE PHYSICS CALLBACK (knight.gd sets
	# ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS), so the bone poses are only fresh here. Reading
	# them in _process samples whatever last frame left behind.
	_t += dt
	if _mat != null:
		_mat.set_shader_parameter("now_s", _t)
	if _skel == null or _bones.is_empty():
		return
	var fwd := Vector2(0, 1)
	if _body != null:
		var b := _body.global_transform.basis
		fwd = Vector2(-b.z.x, -b.z.z)
	for side in ["L", "R"]:
		var fp := _foot_pos(side + "_foot")
		var tp := _foot_pos(side + "_toe")
		if fp == Vector3.INF:
			continue
		var contact_y: float = fp.y if tp == Vector3.INF else minf(fp.y, tp.y)
		var here := Vector2(fp.x, fp.z) if tp == Vector3.INF \
			else Vector2((fp.x + tp.x) * 0.5, (fp.z + tp.z) * 0.5)
		var lift := contact_y - (floor_y + ground_h_at(here))   # BV2F-PT DEV-18: the foot over the GROUND under it
		if lift > 0.13:
			continue
		var last: Variant = _last_stamp.get(side, null)
		if last != null and here.distance_to(last) < stamp_stride_m:
			continue
		_last_stamp[side] = here
		var D := depth_at(here)
		var deep: bool = D > plough_depth_m
		_stamp(here, fwd, boot_len_m * 0.5, boot_w_m * 0.5, boot_rim_m,
			plough_berm_mult if deep else 1.0)
		if puffs:
			_puff(Vector3(here.x, floor_y + ground_h_at(here) + minf(D, 0.5) * 0.5, here.y), fwd, D, deep)
		if deep:
			_plough(here, fwd, D)


func surface_y(xz: Vector2) -> float:  # BV2F-PT DEV-18 copy
	"""The snow surface, metres in world y, INCLUDING the trail -- the same expression
	snow_h() evaluates on the GPU."""
	if _field_buf.is_empty():
		return floor_y + ground_h_at(xz)   # BV2F-PT DEV-18
	var uv := _uv_of(xz)
	var f := _bilinear4(_field_buf, field_px, uv)
	var t := _bilinear4(_trail_buf, trail_px, uv)
	var fade := clampf(1.0 - (_t - t[1]) / maxf(trail_refill_s, 1e-3), 0.0, 1.0)
	var p := clampf(t[0] * fade, 0.0, 1.0)
	var b := clampf(t[2] * fade, 0.0, 1.0)
	return floor_y + ground_h_at(xz) + lerpf(f[0], minf(residual_m, float(f[0]) * 0.3), p) + berm_frac * b * f[0]
