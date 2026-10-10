extends Control
## C-9 BV2F ARENA (R-C9-348) -- the fight's HUD over the barrow scene: wave, the warlord's health and energy, KC2's
## slot bar with its live cooldowns, buffs, monster health bars (N), the start card and RUN OVER. Read-only: it reads
## the snapshot, the driver and the event stream; it posts nothing.

var mode = null
var floats: Array = []          # {txt, at_m, t0, col}
var t_now := 0.0

const SLOTS := [
	["LMB", "Charge", "blitz"], ["RMB", "Whirlwind", "eye_of_reckoning"], ["1", "Potion", "potion"],
	["2", "Might", "vires_might"], ["3", "Battle Cry", "war_cry"], ["4", "Haste", "rune_of_rush"]]
## R-C9-353 (Matt): generic names on screen, no Grim Dawn skill names. DISPLAY ONLY: the sim's skill ids are unchanged.
const BUFF_NAMES := {"war_cry": "Battle Cry", "warcry": "Battle Cry", "vires_might": "Might", "rune_of_rush": "Haste",
	"blitz": "Charge", "eye_of_reckoning": "Whirlwind", "potion": "Potion", "health_potion": "Potion",
	"potion_hot": "Potion",
	# the automatic procs (KP-298): GD names in the sim; PROVISIONAL generic labels, listed for Matt in the report
	"turtle_shell": "Guard", "arcane_barrier": "Barrier", "ascension": "Rally", "menhirs_will": "Endure"}


func bind(m) -> void:
	mode = m


func consume_events(evs: Array) -> void:
	for e_any in evs:
		var e: Dictionary = e_any
		var ev := String(e.get("event", ""))
		if ev == "hit" and int(e.get("dst_id", -1)) == 0:
			floats.append({"txt": "-%d" % int(round(float(e.get("amount", 0.0)))), "player": true, "t0": t_now,
				"col": Color(1.0, 0.45, 0.4)})
		elif ev == "pool_tick":
			floats.append({"txt": "-%d pool" % int(round(float(e.get("amount", 0.0)))), "player": true, "t0": t_now,
				"col": Color(0.6, 1.0, 0.5)})


func _process(dt: float) -> void:
	t_now += dt


func _font() -> Font:
	return ThemeDB.fallback_font


func _text(s: String, at: Vector2, size: int, col: Color, center := false) -> void:
	var f := _font()
	var w := f.get_string_size(s, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x
	var p := at - Vector2(w * 0.5, 0.0) if center else at
	draw_string(f, p + Vector2(1, 1), s, HORIZONTAL_ALIGNMENT_LEFT, -1, size, Color(0, 0, 0, 0.8 * col.a))
	draw_string(f, p, s, HORIZONTAL_ALIGNMENT_LEFT, -1, size, col)


func _bar(r: Rect2, frac: float, col: Color) -> void:
	draw_rect(r, Color(0, 0, 0, 0.6))
	draw_rect(Rect2(r.position, Vector2(r.size.x * clampf(frac, 0.0, 1.0), r.size.y)), col)


func _draw() -> void:
	if mode == null:
		return
	var vs := get_viewport_rect().size
	if mode.fatal != "":
		draw_rect(Rect2(Vector2.ZERO, vs), Color(0.05, 0.02, 0.02, 0.8))
		var y := vs.y * 0.35
		for line in String(mode.fatal).split("\n"):
			_text(line, Vector2(vs.x * 0.5, y), 20, Color(1, 0.6, 0.5), true)
			y += 26.0
		return
	if mode.session == null or mode.snap.is_empty():
		return
	var cam: Camera3D = mode.scene.cam
	var snap: Dictionary = mode.snap
	# ---- monster bars (N) ----
	if mode.show_bars:
		for k in mode.actors.keys():
			var m = mode.actors[k]
			if m.dying or not m.released:
				continue
			var top: Vector3 = m.global_position + Vector3.UP * (float(m.true_height_m) * 0.62 + 0.35)
			if cam.is_position_behind(top):
				continue
			var sp := cam.unproject_position(top)
			var bw := 34.0 if not m.champion else 60.0
			_bar(Rect2(sp - Vector2(bw * 0.5, 0), Vector2(bw, 4)), float(m.hp) / maxf(1.0, float(m.hp_max)),
				Color(0.86, 0.30, 0.30))
			if m.champion or m.label.begins_with("NO PACK") or m.label.contains("NO PACK"):
				if m.label != "":
					_text(m.label.substr(0, 40), sp + Vector2(0, -6), 12, Color(1, 0.92, 0.82), true)
	# ---- floats on the player ----
	var pp: Vector3 = mode.proxy.global_position + Vector3.UP * 2.2
	var psp := cam.unproject_position(pp)
	var keep: Array = []
	for f_any in floats:
		var f: Dictionary = f_any
		var age := t_now - float(f["t0"])
		if age > 0.9:
			continue
		keep.append(f)
		var c: Color = f["col"]
		c.a = 1.0 - age / 0.9
		_text(String(f["txt"]), psp + Vector2(18, -age * 40.0), 16, c)
	floats = keep
	# ---- the wave ----
	var wave := int(snap.get("wave", 0))
	_text("WAVE %d  (%d of 10)" % [wave, wave - 150], Vector2(24, 40), 26, Color(1, 0.93, 0.8))
	_text("%.1f s   ·   %d on the field" % [float(snap.get("wave_elapsed_s", 0.0)), (snap.get("actors", []) as Array).size()],
		Vector2(24, 66), 15, Color(0.85, 0.85, 0.9))
	_text("BARROW_V2 ARENA - the KC2 fight, spawn points moved (R-C9-348). Not the KC2 test.", Vector2(24, vs.y - 16), 12,
		Color(0.8, 0.8, 0.85, 0.8))
	# ---- the warlord ----
	var p: Dictionary = snap.get("player", {})
	var hp := float(p.get("hp", 0.0))
	var hpm := maxf(1.0, float(p.get("hp_max", 1.0)))
	var en := float(p.get("energy", 0.0))
	var enm := maxf(1.0, float(p.get("energy_max", 1.0)))
	var bx := vs.x * 0.5 - 260.0
	var by := vs.y - 120.0
	_bar(Rect2(bx, by, 520, 16), hp / hpm, Color(0.80, 0.16, 0.16))
	_text("%d / %d" % [int(hp), int(hpm)], Vector2(vs.x * 0.5, by + 13), 13, Color(1, 1, 1), true)
	_bar(Rect2(bx, by + 20, 520, 8), en / enm, Color(0.25, 0.55, 1.0))
	# ---- the slot bar (KC2's keys and kit) ----
	var cds: Dictionary = p.get("cooldowns", {})
	var sx := vs.x * 0.5 - 3.0 * 92.0
	var sy := by + 36.0
	for i in SLOTS.size():
		var s: Array = SLOTS[i]
		var r := Rect2(sx + float(i) * 92.0, sy, 86, 50)
		var cd := float(cds.get(String(s[2]), 0.0))
		var on := String(s[2]) == "eye_of_reckoning" and String(p.get("channel", "")) == "ACTIVE"
		draw_rect(r, Color(0.08, 0.08, 0.1, 0.75))
		draw_rect(r, Color(1, 0.5, 0.3, 0.9) if on else Color(0.5, 0.5, 0.55, 0.8), false, 1.5)
		_text(String(s[0]), r.position + Vector2(5, 15), 13, Color(1, 0.9, 0.6))
		_text(String(s[1]), r.position + Vector2(5, 32), 11, Color(0.9, 0.9, 0.95))
		if cd > 0.0:
			draw_rect(r, Color(0, 0, 0, 0.45))
			_text("%.1f" % cd, r.position + Vector2(43, 46), 13, Color(1, 1, 1), true)
	var bl := []
	for b_any in (p.get("buffs", []) as Array):
		var b = b_any
		var bid: String = String((b as Dictionary).get("id", (b as Dictionary).get("name", "?"))) if typeof(b) == TYPE_DICTIONARY else str(b)
		bl.append(String(BUFF_NAMES.get(bid, bid.replace("_", " "))))
	if not bl.is_empty():
		_text("buffs: " + ", ".join(bl), Vector2(bx, by - 8), 13, Color(0.7, 1.0, 0.7))
	_text("hold LMB move · click LMB Charge · hold RMB Whirlwind · 1 Potion · 2 Might · 3 Battle Cry · 4 Haste · Z zoom · N bars · R restart · C capture · Esc quit",
		Vector2(vs.x * 0.5, vs.y - 36), 12, Color(0.85, 0.85, 0.9, 0.85), true)
	# ---- the start card / RUN OVER ----
	if not mode.fight_started:
		draw_rect(Rect2(vs.x * 0.5 - 330, vs.y * 0.30, 660, 120), Color(0.04, 0.04, 0.06, 0.82))
		_text("THE BARROW ARENA", Vector2(vs.x * 0.5, vs.y * 0.30 + 40), 28, Color(1, 0.9, 0.75), true)
		_text("KC2's ten waves (151-160), every monster, the Warlord. Click or press Space to begin.",
			Vector2(vs.x * 0.5, vs.y * 0.30 + 76), 15, Color(0.9, 0.9, 0.95), true)
		_text("Spawns: p01 wreck · p02 barrow door · p03 sea cave · p04 longhall door · p05 mere ambush · p06 gable",
			Vector2(vs.x * 0.5, vs.y * 0.30 + 100), 12, Color(0.75, 0.85, 0.95), true)
	elif not mode.running:
		draw_rect(Rect2(Vector2.ZERO, vs), Color(0, 0, 0, 0.55))
		var term := String(mode.session.terminal)
		var wv := int(mode.session.fight.terminal_wave)
		var head := "VICTORY - all ten waves cleared" if term == "cleared" else "RUN OVER"
		_text(head, Vector2(vs.x * 0.5, vs.y * 0.42), 36, Color(1, 0.85, 0.7), true)
		_text("%s at wave %d   ·   R to restart   ·   Esc to quit" % [term, wv], Vector2(vs.x * 0.5, vs.y * 0.42 + 36), 18,
			Color(0.95, 0.95, 1.0), true)
