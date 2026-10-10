extends RefCounted
## C-9 BV2F ARENA (R-C9-348) -- the JOIN-1 art the KC2 fight already plays, READ IN PLACE (never copied).
##
## The same catalogue kc2_play draws from (kc2_play/art/join1/: join1_index.json -> per-kit index.json -> cell strips),
## with the same lookup rules as kc2_play/src/kc2p_join1.gd (record -> kit + true-size factor; state metadata; the
## frame-at-time law; the 8-way bearing law). The strips are decoded at run time from their PNGs on a worker thread
## (no Godot import, so nothing is staged or duplicated into this project); a cell not yet decoded draws its last
## decoded frame (or nothing on first sight) and is ready a frame or two later.

const Paths = preload("res://scripts/arena/arena_paths.gd")
## R-C9-391: the catalogue root -- in place on this Mac, the bundle's res://kc2/art/ in a bundled (web) build
static var ROOT: String = Paths.join1_root()
const ROOT_X := "res://kc2/art_x/"
const DIRS: PackedStringArray = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]

static var _index: Dictionary = {}
static var _index_error: String = ""
static var _kits: Dictionary = {}          # kit -> its index.json
static var _tex: Dictionary = {}           # abs path -> Texture2D (ready)
static var _pending: Dictionary = {}       # abs path -> WorkerThreadPool task id
static var _images: Dictionary = {}        # abs path -> Image (decoded, waiting for upload)
static var _mutex := Mutex.new()
static var n_tex: int = 0
static var bytes_rgba: int = 0


static func index() -> Dictionary:
	if not _index.is_empty() or _index_error != "":
		return _index
	var p := ROOT + "join1_index.json"
	if not FileAccess.file_exists(p):
		_index_error = "%s missing (kc2_play/tools/stage_join1.py stages it)" % p
		push_warning("[arena] " + _index_error)
		return _index
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(p))
	if typeof(d) != TYPE_DICTIONARY:
		_index_error = "join1_index.json does not parse"
		return _index
	_index = d
	return _index


static func ok() -> bool:
	return not index().is_empty()


static func hero_kit() -> String:
	return String(index().get("hero", ""))


## record path -> {"kind": "kit"|"none", "kit", "factor", "family"} (kc2p_join1.record_entry's rule)
static func record_entry(rec: String) -> Dictionary:
	var rm: Dictionary = index().get("record_map", {})
	if rm.has(rec):
		var e: Dictionary = rm[rec]
		return {"kind": "kit", "kit": String(e["kit"]), "factor": float(e.get("factor", 1.0)),
			"type_id": String(e.get("type_id", ""))}
	var tid := ""
	for u_any in (index().get("unmapped_wave_records", []) as Array):
		var u: Dictionary = u_any
		if String(u.get("record", "")) == rec:
			tid = str(u.get("type_id", ""))
			break
	return {"kind": "none", "family": tid if tid != "" else rec.get_file().get_basename(), "factor": 1.0}


## R-C9-366: a VARIANT kit staged for the arena (tools/arena_stage_x.py -> res://kc2/art_x/<kit>/) is read from there.
static func root_of(kit: String) -> String:
	var x := ProjectSettings.globalize_path(ROOT_X)
	return x if FileAccess.file_exists(x + kit + "/index.json") else ROOT


static func kit_meta(kit: String) -> Dictionary:
	if _kits.has(kit):
		return _kits[kit]
	var p := root_of(kit) + kit + "/index.json"
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(p)) if FileAccess.file_exists(p) else null
	_kits[kit] = d if typeof(d) == TYPE_DICTIONARY else {}
	if (_kits[kit] as Dictionary).is_empty():
		push_warning("[arena] kit %s has no index at %s" % [kit, p])
	return _kits[kit]


static func cell(kit: String, cid: String) -> Dictionary:
	return (kit_meta(kit).get("cells", {}) as Dictionary).get(cid, {})


static func state(kit: String, st: String) -> Dictionary:
	return (kit_meta(kit).get("states", {}) as Dictionary).get(st, {})


static func has_state(kit: String, st: String) -> bool:
	return (kit_meta(kit).get("states", {}) as Dictionary).has(st)


static func states_with_role(kit: String, role: String) -> Array:
	var out: Array = []
	var sts: Dictionary = kit_meta(kit).get("states", {})
	for k in sts.keys():
		if String((sts[k] as Dictionary).get("role", "")) == role:
			out.append(String(k))
	out.sort()
	return out


static func frame_at(t_s: Array, c: float) -> int:
	var n := t_s.size()
	if n == 0:
		return 0
	if c <= float(t_s[0]):
		return 0
	var hi := n - 1
	if c >= float(t_s[hi]):
		return hi
	var lo := 0
	while lo < hi:
		var mid := (lo + hi + 1) >> 1
		if float(t_s[mid]) <= c:
			lo = mid
		else:
			hi = mid - 1
	return lo


## model-plane bearing (x right, y toward the camera) -> one of the 8 pack directions (kc2p_join1.dir_of)
static func dir_of(v: Vector2) -> String:
	var a := rad_to_deg(atan2(v.y, v.x))
	var i := int(round(wrapf(a - 90.0, 0.0, 360.0) / 45.0)) % 8
	return DIRS[i]


static func _decode(path: String) -> void:
	var img := Image.load_from_file(path)
	_mutex.lock()
	_images[path] = img
	_mutex.unlock()


## The cell's strip texture, or null while it decodes (the request is fired on the first call).
static func cell_tex(kit: String, cid: String) -> Texture2D:
	var c := cell(kit, cid)
	if c.is_empty():
		return null
	return tex_at(root_of(kit) + String(c["file"]))


static func tex_at(path: String) -> Texture2D:
	if _tex.has(path):
		return _tex[path]
	if path.begins_with("res://"):
		return _tex_res(path)
	if not _pending.has(path):
		_pending[path] = WorkerThreadPool.add_task(_decode.bind(path))
		return null
	_mutex.lock()
	var img: Image = _images.get(path, null)
	var done := _images.has(path)
	_images.erase(path)
	_mutex.unlock()
	if not done:
		return null
	WorkerThreadPool.wait_for_task_completion(int(_pending[path]))
	_pending.erase(path)
	var t: Texture2D = null
	if img != null and not img.is_empty():
		t = ImageTexture.create_from_image(img)
		n_tex += 1
		bytes_rgba += img.get_width() * img.get_height() * 4
	else:
		push_warning("[arena] could not decode %s" % path)
	_tex[path] = t
	return t


## R-C9-391 BUNDLED: the strip is an IMPORTED texture (VRAM-compressed by the bundle's import: Basis Universal, so a
## phone holds it at ~1/4 of RGBA), loaded on Godot's own loader thread; null until it lands.
static func _tex_res(path: String) -> Texture2D:
	if not _pending.has(path):
		if not ResourceLoader.exists(path):
			return null                            # its wave pack is not loaded yet
		ResourceLoader.load_threaded_request(path, "Texture2D")
		_pending[path] = 1
		return null
	var st := ResourceLoader.load_threaded_get_status(path)
	if st == ResourceLoader.THREAD_LOAD_IN_PROGRESS:
		return null
	_pending.erase(path)
	var t: Texture2D = ResourceLoader.load_threaded_get(path) if st == ResourceLoader.THREAD_LOAD_LOADED else null
	if t == null:
		push_warning("[arena] could not load %s" % path)
	else:
		n_tex += 1
		bytes_rgba += t.get_width() * t.get_height()
	_tex[path] = t
	return t


## Forget a kit's index so it is re-read (a wave pack holding it has just been loaded).
static func refresh_kit(kit: String) -> void:
	_kits.erase(kit)


## Fire decodes for every cell of a kit whose state is in `states` (all when empty). Cheap to repeat.
static func prefetch(kit: String, states: Array = []) -> void:
	for cid_any in (kit_meta(kit).get("cells", {}) as Dictionary).keys():
		var cid := String(cid_any)
		if not states.is_empty() and not states.has(cid.split("/")[0]):
			continue
		cell_tex(kit, cid)
