## BV2F LV 0.2 -- GDScript TWIN of fid/lv/frame.py (the ONE sim -> world transform). Keep the two identical.
## world = R_y(+47 deg) . (x, z, y): sim +x east -> v1's u_hat (screen-right), sim +y south -> -v_hat (screen-down).
## Camera, heather card basis, suns, snow and pen stay v1's, untouched. Proof: fid/lv/test_frame.py.
class_name BV2Frame

const PL_YAW_DEG := 47.0                 # barrow_full.gd:45
const PL_PITCH_DEG := 52.95354112560294  # barrow_full.gd:44
const FRAME_YAW_DEG := 47.0


static func basis(yaw_deg: float = FRAME_YAW_DEG) -> Basis:
	return Basis(Vector3.UP, deg_to_rad(yaw_deg))


static func sim_to_world(x: float, y: float, z: float = 0.0, yaw_deg: float = FRAME_YAW_DEG) -> Vector3:
	return basis(yaw_deg) * Vector3(x, z, y)


static func world_to_sim(p: Vector3) -> Vector3:
	var q := basis().inverse() * p
	return Vector3(q.x, q.z, q.y)


static func rot_y_to_world(rot_y_sim_deg: float) -> float:
	return rot_y_sim_deg + FRAME_YAW_DEG
