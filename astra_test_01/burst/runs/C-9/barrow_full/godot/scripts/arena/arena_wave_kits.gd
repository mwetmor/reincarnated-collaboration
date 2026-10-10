extends SceneTree
## C-9 BV2F ARENA (R-C9-391) -- which JOIN-1 kits each wave (151-160) can draw, from the UNMODIFIED runtime's own roster
## (wave/point alternatives -> pool members -> record) and the JOIN-1 record map (record -> kit). Read-only; writes
## res://data/arena/wave_kits.json, which tools/arena_bundle.py reads to pack the web build's per-wave kit packs.
##   Godot --headless --path <godot> -s res://scripts/arena/arena_wave_kits.gd

const Kc2PlaySession = preload("res://kc2/kc2_runtime/play/kc2play_session.gd")
const Kc2RtPackOfRecord = preload("res://kc2/kc2_runtime/kc2rt_pack_of_record.gd")
const J = preload("res://scripts/arena/arena_art.gd")
const Paths = preload("res://scripts/arena/arena_paths.gd")


func _init() -> void:
	var s = Kc2PlaySession.new()
	if not s.open(Paths.model_pack_dir(), Kc2RtPackOfRecord.MODEL_DIGEST, Paths.geom(), 12345, "ZOOM-GD", true):
		print("open failed: ", s.load_error)
		quit(1)
		return
	var r = s.fight.roster
	var by_wave := {}
	var placeholders := {}
	for k in r.alternatives.keys():
		var w := int(String(k).split("|")[0])
		if w < 151 or w > 160:
			continue
		if not by_wave.has(w):
			by_wave[w] = {}
		for alt in r.alternatives[k]:
			for m in r.pool_members.get(String(alt["pool"]), PackedStringArray()):
				var e := J.record_entry(String(m))
				if String(e.get("kind", "")) == "kit":
					by_wave[w][String(e["kit"])] = true
				else:
					placeholders[String(e.get("family", ""))] = true
	var out := {"_what": "R-C9-391: JOIN-1 kits each wave 151-160 can draw (roster alternatives -> pool members -> join1 record map); written by scripts/arena/arena_wave_kits.gd", "hero": J.hero_kit(), "waves": {}}
	var all := {}
	for w in range(151, 161):
		var ks: Array = (by_wave.get(w, {}) as Dictionary).keys()
		ks.sort()
		out["waves"][str(w)] = ks
		for kk in ks:
			all[kk] = true
	out["n_kits"] = all.size()
	var f := FileAccess.open("res://data/arena/wave_kits.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ", false))
	f.close()
	print("wave kits: %d kits over waves 151-160 -> res://data/arena/wave_kits.json" % all.size())
	quit(0)
