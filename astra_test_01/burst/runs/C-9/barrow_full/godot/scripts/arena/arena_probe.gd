extends SceneTree
## C-9 BV2F ARENA (R-C9-348) -- headless probe: opens the UNMODIFIED KC2 play session the stock way and prints
## the arm's arena rules (wall, avoidance pools, floor pools, aprons) and the wave roster, so the variant session
## knows what it overrides. Read-only: writes nothing.

const RT := "res://kc2/kc2_runtime/"
const Kc2PlaySession = preload("res://kc2/kc2_runtime/play/kc2play_session.gd")
const Kc2RtPackOfRecord = preload("res://kc2/kc2_runtime/kc2rt_pack_of_record.gd")
const GEOM := "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json"


func _init() -> void:
	var s = Kc2PlaySession.new()
	var ok: bool = s.open(Kc2RtPackOfRecord.MODEL_DIR, Kc2RtPackOfRecord.MODEL_DIGEST, GEOM, 12345, "ZOOM-GD", true)
	print("open ok=", ok, " err=", s.load_error)
	if not ok:
		quit(1)
		return
	var f = s.fight
	print("arm=", f.arm, " is_oracle=", f.is_oracle, " walls_armed=", f.walls_armed, " r_wall=", f.r_wall,
		" avoidance=", f.arena_avoidance, " pool_r=", f.arena_pool_radius_m, " ambush_pt=", f.arena_ambush_point)
	print("arena_state=", f.arena_state)
	print("arena_pools(w151)=", f.arena_pools)
	print("aprons_on=", f.aprons_on, " v_ref_speed=", f.v_ref_speed)
	print("board.spawn_points=", s.board.spawn_points, " src=", s.board.spawn_points_source)
	print("placement_extents=", s.board.placement_extents_m)
	print("arena.pools=")
	for z in s.arena.pools:
		print("   ", z["id"], " c=", z["centre"], " r=", z["radius_m"])
	print("arena.mouths n=", s.arena.mouths.size())
	print("driver.pool_period_ticks=", s.driver.pool_period_ticks)
	print("r_wall_by_wave=", f.arena_r_wall_by_wave)
	var recs := {}
	for k in s.fight.roster.alternatives.keys():
		var key := String(k)
		var w := int(key.split("|")[0])
		if w < 151 or w > 160:
			continue
		var alts = s.fight.roster.alternatives[k]
		recs[key] = alts.size()
	print("alt keys 151-160: ", recs.size())
	var ks := recs.keys()
	ks.sort()
	print(ks)
	quit(0)
