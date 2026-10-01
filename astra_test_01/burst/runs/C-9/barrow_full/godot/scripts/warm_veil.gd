extends CanvasLayer
## C-9 -- THE WARMING VEIL (the coordinator's ruling (a)): on the phone page the level's first draws compile
## their shaders -- 0.7-1.5 s of 170-990 ms frames straight after the Barrow appears
## (take/build/load_tail.json). The loading look stays up until they are done: lifted on a MEASURED signal
## (every warm-up draw issued -- the level ready, her Fire Ball's and her Meteor's warm draws done -- then
## SETTLE_FRAMES frames in a row under SETTLE_MS), never later than CAP_S after the level is ready.
## COLD FIRST LOAD (the coordinator, 2026-09-30): with a cold shader cache her warm-ups took 4.64 s, the old 3 s
## cap lifted the veil first and the first cast carried the rest (358 + 225 ms). The settle frames now count
## only once every warm draw has been issued AND drawn (each warmed flag is set frames after its draw), the cap
## is 8 s, and after NOTE_S a small "preparing effects…" line says the wait is work, not a hang.
## MEASURED COLD (cache cleared): the first draw after ready is ONE frame of 8-12 s (every level shader compiled
## at once) and nothing in the engine can draw during it. So: (1) the cap counts only RESPONSIVE waiting --
## frames under STALL_MS -- because a compile stall is the work it is waiting for, not a hang; HARD_S is the
## wall-clock backstop for a warm-up flag that never comes true. (2) On the web the veil is ALSO a DOM overlay
## laid over the canvas before that frame: the browser keeps compositing it while the engine is blocked, and its
## "preparing effects…" line fades in after NOTE_S by a CSS animation the compositor runs on its own.
## It is a veil, not a pause: the world draws under it the whole time, which is the point.

const SETTLE_FRAMES := 8
const SETTLE_MS := 25.0
const CAP_S := 8.0
const NOTE_S := 3.0
const STALL_MS := 250.0
const HARD_S := 45.0

var scene
var report := {}
var _rect: ColorRect
var _label: Label
var _note: Label
var _t_ready := 0
var _last := 0
var _run := 0
var _frames := 0
var _worst_under := 0.0
var _t_done := 0
var _wait_s := 0.0
var _dom := false


func setup(p_scene) -> void:
	scene = p_scene
	layer = 128
	_rect = ColorRect.new()
	_rect.color = Color(0, 0, 0, 1)          # the web shell's own loading ground
	_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	_rect.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_rect)
	_label = Label.new()
	_label.text = "Loading…"
	_label.add_theme_font_size_override("font_size", 28)
	_label.add_theme_color_override("font_color", Color(0.85, 0.87, 0.9, 0.9))
	_label.set_anchors_preset(Control.PRESET_CENTER)
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.offset_left = -200
	_label.offset_right = 200
	add_child(_label)
	_note = Label.new()
	_note.text = "preparing effects…"
	_note.add_theme_font_size_override("font_size", 16)
	_note.add_theme_color_override("font_color", Color(0.75, 0.77, 0.8, 0.75))
	_note.set_anchors_preset(Control.PRESET_CENTER)
	_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_note.offset_left = -200
	_note.offset_right = 200
	_note.offset_top = 30
	_note.offset_bottom = 60
	_note.visible = false
	add_child(_note)
	if OS.has_feature("web"):
		_dom = true
		JavaScriptBridge.eval("""(function(){
			if (document.getElementById('warm-veil')) return;
			var st = document.createElement('style');
			st.textContent = '#warm-veil{position:fixed;inset:0;background:#000;z-index:50;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:system-ui,sans-serif;color:rgba(217,222,230,.9);pointer-events:auto}' +
				'#warm-veil .l{font-size:22px}#warm-veil .n{font-size:13px;margin-top:10px;color:rgba(191,196,204,.75);opacity:0;animation:wv-note .4s ease %ss forwards}' +
				'@keyframes wv-note{to{opacity:1}}';
			document.head.appendChild(st);
			var d = document.createElement('div'); d.id = 'warm-veil';
			d.innerHTML = '<div class=\"l\">Loading…</div><div class=\"n\">preparing effects…</div>';
			document.body.appendChild(d);
		})()""" % str(NOTE_S), true)


# --- STAGED FIRST DRAW (the coordinator, 2026-09-30) -------------------------------------------------
# Cold, the level's first draw compiled every shader in one 8-12 s frame. At ready the level's visible
# geometry is hidden and given back a few SHADERS per frame (every node sharing a shader comes back with
# it: the compile is per shader), so the compiles spread over many shorter frames under the veil.
const STAGE_SHADERS_PER_FRAME := 1
var _stage: Array = []                 # [[nodes...], ...] in reveal order
var _stage_started := false
var stage_report := {}


func stage_level(root: Node) -> void:
	var groups := {}
	var order: Array = []
	var stack: Array = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is GeometryInstance3D and (n as GeometryInstance3D).visible and n.is_visible_in_tree() and not n.is_ancestor_of(self):
			var key := _shader_key(n as GeometryInstance3D)
			if not groups.has(key):
				groups[key] = []
				order.append(key)
			(groups[key] as Array).append(n)
	for key in order:
		for g in groups[key]:
			(g as GeometryInstance3D).visible = false
		_stage.append(groups[key])
	stage_report = {"shaders": order.size(), "nodes": groups.values().reduce(func(a, b): return a + (b as Array).size(), 0),
		"per_frame": STAGE_SHADERS_PER_FRAME}


func _shader_key(g: GeometryInstance3D) -> String:
	var m: Material = g.material_override
	if m == null and g is MeshInstance3D and (g as MeshInstance3D).mesh != null and (g as MeshInstance3D).mesh.get_surface_count() > 0:
		m = (g as MeshInstance3D).get_active_material(0)
	if m == null and g is MultiMeshInstance3D and (g as MultiMeshInstance3D).multimesh != null and (g as MultiMeshInstance3D).multimesh.mesh != null:
		var mm := (g as MultiMeshInstance3D).multimesh.mesh
		m = mm.surface_get_material(0) if mm.get_surface_count() > 0 else null
	if m is ShaderMaterial and (m as ShaderMaterial).shader != null:
		return "s%d" % (m as ShaderMaterial).shader.get_instance_id()
	if m != null:
		return "m%d" % m.get_instance_id()
	return "none"


func stage_done() -> bool:
	return _stage.is_empty()


func _step_stage() -> void:
	for k in STAGE_SHADERS_PER_FRAME:
		if _stage.is_empty():
			return
		for g in _stage.pop_front():
			if is_instance_valid(g):
				(g as GeometryInstance3D).visible = true


func _warmups_done() -> bool:
	if not bool(scene.ready_done):
		return false
	if not _stage.is_empty():
		return false
	var sfx = scene.spell_fx
	if sfx != null and sfx.fire_ball != null and not bool(sfx.fire_ball.warmed):
		return false
	if sfx != null and sfx.meteor_a != null and not bool(sfx.meteor_a.warmed):
		return false
	if sfx != null and bool(sfx.meteor_a_pending):
		return false
	var mfx0 = scene.get("meteor_fx")
	if mfx0 != null and bool(mfx0.get("mix1_pending")):
		return false
	if mfx0 != null and mfx0.get("proj_a") != null and not bool(mfx0.proj_a.warmed):
		return false
	if mfx0 != null and mfx0.get("burst_a") != null and not bool(mfx0.burst_a.warmed):
		return false
	if mfx0 != null and mfx0.get("cinders") != null and not bool(mfx0.cinders.warmed):
		return false
	if mfx0 != null and mfx0.get("crater") != null and not bool(mfx0.crater.warmed):
		return false
	if mfx0 != null and mfx0.get("crater4") != null and not bool(mfx0.crater4.warmed):
		return false
	var mfx = scene.get("meteor_fx")
	if mfx != null and not bool(mfx.warmed):
		return false
	return true


func _process(_dt: float) -> void:
	# the staged reveal runs whatever the veil's own visibility (a harness may hide the CanvasLayers): the level
	# must never be left hidden
	if scene != null and bool(scene.ready_done):
		if _stage_started:
			_step_stage()
		_stage_started = true
	if scene == null or not visible:
		return
	var now := Time.get_ticks_usec()
	var dt := float(now - _last) / 1000.0 if _last != 0 else 0.0
	_last = now
	if not bool(scene.ready_done):
		return
	if _t_ready == 0:
		_t_ready = now
		return
	_frames += 1
	_worst_under = maxf(_worst_under, dt)
	if dt < STALL_MS:
		_wait_s += dt / 1000.0
	var since := float(now - _t_ready) / 1e6
	if since >= NOTE_S and not _note.visible:
		_note.visible = true
	var done := _warmups_done()
	if done and _t_done == 0:
		_t_done = now
	if done and dt < SETTLE_MS:
		_run += 1
	else:
		_run = 0
	var reason := ""
	if _run >= SETTLE_FRAMES:
		reason = "settled"
	elif _wait_s >= CAP_S:
		reason = "cap"
	elif since >= HARD_S:
		reason = "hard_cap"
	if reason != "":
		visible = false
		while not _stage.is_empty():     # a capped lift gives back whatever is still staged
			_step_stage()
		if _dom:
			JavaScriptBridge.eval("(function(){var d=document.getElementById('warm-veil'); if(d) d.remove();})()", true)
		report = {"lifted_s_after_ready": snappedf(since, 0.001), "reason": reason, "frames_under_veil": _frames,
			"worst_frame_under_veil_ms": snappedf(_worst_under, 0.1), "warmups_done": _warmups_done(),
			"warmups_done_s_after_ready": snappedf(float(_t_done - _t_ready) / 1e6, 0.001) if _t_done != 0 else -1.0,
			"note_shown": _note.visible or since >= NOTE_S, "cap_s": CAP_S,
			"responsive_wait_s": snappedf(_wait_s, 0.001), "staged": stage_report, "stall_ms": STALL_MS, "hard_s": HARD_S}
		print("[veil] lifted " + JSON.stringify(report))
