extends SceneTree
# jack-ryan H-3 (2026-10-03) SCRATCH DRIVER -- not a runtime file. Prereg v1.14 C.9.8: native shadow bit-equality on a
# FRESH w151-w160 run per arm at the attempt digest, the port's OWN generator. Built from kc2rt_tick_timing.gd's
# _fight (verbatim, minus the timing subclass); each wave run fresh run(w, w); contact=shadow; aggregates EVERY
# integer field of contact_solver_report() (incl. petpath_shadow_*) and keeps every first-mismatch string.
# Run: Godot --headless --path <archive> --script kc2_runtime/tools/jr_shadow_fresh.gd -- arm=W1 salt=0 waves=151-160 out=<json>
const Kc2RtPack = preload("res://kc2_runtime/kc2rt_pack.gd")
const Kc2RtConfig = preload("res://kc2_runtime/sim/kc2rt_config.gd")
const Kc2RtBoard = preload("res://kc2_runtime/sim/kc2rt_board.gd")
const Kc2RtRng = preload("res://kc2_runtime/sim/kc2rt_rng.gd")
const Kc2RtPackOfRecord = preload("res://kc2_runtime/kc2rt_pack_of_record.gd")
const FightBase = preload("res://kc2_runtime/sim/kc2rt_fight.gd")
const P := "[jr-shadow] "

func _arg(name: String, dflt: String) -> String:
	for a in OS.get_cmdline_user_args():
		if String(a).begins_with(name + "="):
			return String(a).substr(name.length() + 1)
	return dflt

func _init() -> void:
	var arm := _arg("arm", "W1")
	var salt := int(_arg("salt", "0"))
	var wr := _arg("waves", "151-160").split("-")
	var out_path := _arg("out", "")
	var contact := _arg("contact", "shadow")
	var pack := Kc2RtPack.new()
	if not pack.load_pack(Kc2RtPackOfRecord.MODEL_DIR, Kc2RtPackOfRecord.MODEL_DIGEST, Kc2RtConfig.CONFIG_ORACLE):
		print(P + "LOAD FAIL " + pack.load_error)
		quit(1)
		return
	var agg: Dictionary = {}
	var firsts: Dictionary = {}
	var per_wave: Dictionary = {}
	var meta: Dictionary = {}
	for w in range(int(wr[0]), int(wr[wr.size() - 1]) + 1):
		var f = _fight(pack, arm, salt)
		if f == null:
			quit(1)
			return
		if not f.select_contact_solver(contact):
			print(P + "contact solver REFUSED: " + str(f.last_error))
			quit(1)
			return
		f.run(w, w, 400000)
		var sr: Dictionary = f.contact_solver_report()
		meta = {"contact_solver": sr["contact_solver"], "native_build_id": sr["native_build_id"],
			"native_lib_sha256": sr["native_lib_sha256"], "note": sr["note"], "oracle_level": f.oracle_level}
		var row := {"terminal_reason": String(f.terminal_reason)}
		for k in sr.keys():
			var v = sr[k]
			if typeof(v) == TYPE_INT:
				agg[k] = int(agg.get(k, 0)) + int(v)
				row[k] = int(v)
			elif String(k).ends_with("first_mismatch") and String(v) != "":
				if not firsts.has(k):
					firsts[k] = "w%d: %s" % [w, String(v)]
		per_wave[str(w)] = row
		print(P + "%s s%d w%d %s" % [arm, salt, w, JSON.stringify(row)])
	var res := {"arm": arm, "salt": salt, "waves": wr, "pack": Kc2RtPackOfRecord.MODEL_DIGEST, "meta": meta,
		"totals": agg, "first_mismatches": firsts, "per_wave": per_wave}
	print(P + "TOTAL " + JSON.stringify(res))
	if out_path != "":
		var fo := FileAccess.open(out_path, FileAccess.WRITE)
		if fo != null:
			fo.store_string(JSON.stringify(res, "  "))
			fo.close()
	quit(0)


func _fight(pack, arm: String, salt: int):
	var rng = Kc2RtRng.new()
	rng.load_contract(pack.model["model/rng_contract.json"])
	rng.load_v3p2_registry(pack.v3p2)
	rng.seed_with(salt)
	var board := Kc2RtBoard.new()
	var extents := float((pack.model["model/arena.json"].get("placement_extents_m", {}) as Dictionary).get("value", 0.0))
	board.setup(pack.roster, rng, true, extents, pack.model["model/arena.json"].get("spawn_points", []), pack.clock.hz())
	var fight := FightBase.new()
	fight.roster = pack.roster
	fight.board = board
	fight.rng = rng
	fight.clock = pack.clock
	fight.leech_table = pack.leech_table
	fight.ticks_per_s = pack.clock.hz()
	if not fight.bind_wire(pack.model, pack.v3p2, pack.v0, pack.ledger):
		print(P + "bind_wire FAILED " + str(fight.last_error))
		return null
	if not fight.bind_motion_suppress(pack.model["model/rng_contract.json"]):
		print(P + "motion suppress FAILED " + str(fight.last_error))
		return null
	var typeb := 0.0
	var v19: Variant = pack.v3p2.superseded_value("V19-TYPEB-1")
	if typeof(v19) == TYPE_DICTIONARY:
		typeb = float((v19 as Dictionary).get("value", (v19 as Dictionary).get("p_per_tick", 0.0)))
	if not fight.configure_arm_from_pack(arm, pack.config.is_oracle(), typeb, false):
		print(P + "arm REFUSED " + str(fight.last_error))
		return null
	fight.policy_of_record = pack.v0.player_policy()
	return fight
