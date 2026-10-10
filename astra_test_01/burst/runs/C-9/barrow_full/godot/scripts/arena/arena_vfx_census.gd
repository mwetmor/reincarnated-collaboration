extends SceneTree
## C-9 BV2F ARENA (R-C9-358..361) -- headless census of every enemy attack slot in waves 151-160: the fields the
## enemy-VFX classifier reads (slot skill path, skill_class, extent carrier, weapon swing, the fight's deferred
## velocity, the damage rows' families). Read-only: opens the UNMODIFIED KC2 play session, writes one JSON.
##   Godot --headless --path <godot> -s res://scripts/arena/arena_vfx_census.gd -- --out <file.json>

const Kc2PlaySession = preload("res://kc2/kc2_runtime/play/kc2play_session.gd")
const Kc2RtPackOfRecord = preload("res://kc2/kc2_runtime/kc2rt_pack_of_record.gd")
const ArenaPathsG = preload("res://scripts/arena/arena_paths.gd")
static var GEOM: String = ArenaPathsG.geom()


func _init() -> void:
	var a := OS.get_cmdline_user_args()
	var i := a.find("--out")
	var out := String(a[i + 1]) if i >= 0 and i + 1 < a.size() else "user://vfx_census.json"
	var s = Kc2PlaySession.new()
	if not s.open(ArenaPathsG.model_pack_dir(), Kc2RtPackOfRecord.MODEL_DIGEST, GEOM, 12345, "ZOOM-GD", true):
		print("open failed: ", s.load_error)
		quit(1)
		return
	var f = s.fight
	var r = f.roster
	var recs := {}
	for k in r.alternatives.keys():
		var w := int(String(k).split("|")[0])
		if w < 151 or w > 160:
			continue
		for alt in r.alternatives[k]:
			for m in r.pool_members.get(String(alt["pool"]), PackedStringArray()):
				recs[String(m)] = true
	# the damage rows by (record, skill), whatever the slot part of their group key
	var fam_by := {}
	var sample_keys: Array = []
	for dk in r.damage_by_slot.keys():
		var parts := String(dk).split("|")
		if sample_keys.size() < 6:
			sample_keys.append(String(dk))
		var rk := parts[0] + "|" + (parts[2] if parts.size() > 2 else "")
		if not fam_by.has(rk):
			fam_by[rk] = {}
		for dr in r.damage_by_slot[dk]:
			if (dr as Dictionary).has("damage_type"):
				fam_by[rk][str(dr["damage_type"])] = true
	var rows: Array = []
	var row_keys := {}
	var slot_keys := {}
	for rec in recs.keys():
		for sl_any in r.slots_for(rec):
			var sl: Dictionary = sl_any
			for kk in sl.keys():
				slot_keys[kk] = true
			var key := String(sl.get("_slot_key", ""))
			var skill := String(sl.get("skill", ""))
			var fams := {}
			for fk2 in (fam_by.get(rec + "|" + String(sl.get("slot", "")), {}) as Dictionary).keys():
				fams[fk2] = true
			var dmg_rows: Array = r.damage_rows_for(key)
			for dr in dmg_rows:
				for kk in (dr as Dictionary).keys():
					row_keys[kk] = true
				for fk in ["family", "damage_family", "damage_type", "element", "type"]:
					if (dr as Dictionary).has(fk):
						fams[str(dr[fk])] = true
			rows.append({"record": rec, "slot_key": key, "skill": skill,
				"skill_class": str(sl.get("skill_class", "")), "extent_carrier": str(sl.get("extent_carrier", "")),
				"is_weapon_swing": sl.get("is_weapon_swing", null), "is_telegraph": sl.get("is_telegraph", null),
				"defer_v": f.defer_velocity.get(skill, null), "families": fams.keys(), "n_dmg_rows": dmg_rows.size()})
	var fo := FileAccess.open(out, FileAccess.WRITE)
	fo.store_string(JSON.stringify({"records": recs.size(), "slots": rows.size(), "slot_fields": slot_keys.keys(),
		"damage_row_fields": row_keys.keys(), "damage_key_samples": sample_keys, "rows": rows}, "  "))
	fo.close()
	print("census: %d records, %d slots -> %s" % [recs.size(), rows.size(), out])
	quit(0)
