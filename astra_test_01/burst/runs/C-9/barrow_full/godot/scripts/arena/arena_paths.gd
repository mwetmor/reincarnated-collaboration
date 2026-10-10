extends RefCounted
## C-9 BV2F ARENA (R-C9-391) -- WHERE THE ARENA'S OUTSIDE INPUTS LIVE.
##
## In the source tree (this Mac) every input is read in place from its owner: the JOIN-1 art from reincarnated-godot,
## the model pack of record from reincarnated-engine, the crucible geometry from galadriel's notes, the font, the eor
## variants. In a BUNDLED build (the web/export mirror made by tools/arena_bundle.py) they are copies inside the
## project, verified byte-for-byte at bundle time; the bundle's stamp (res://kc2/bundle/BUNDLE_STAMP.json) is what
## says which mode this is. Nothing else in the arena decides it.

const STAMP := "res://kc2/bundle/BUNDLE_STAMP.json"
const Kc2RtPackOfRecord = preload("res://kc2/kc2_runtime/kc2rt_pack_of_record.gd")

const SRC_JOIN1 := "/Users/admin/Games/reincarnated-godot/kc2_play/art/join1/"
const SRC_GEOM := "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json"
const SRC_FONT := "/Users/admin/Games/reincarnated-godot/Assets/fonts/bangers/Bangers-Regular.ttf"
const SRC_EOR3_MATRIX := "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/join1_pack/gd-eor-warlord-eor3/matrix_index.json"
const SRC_EOR4X_GLB := "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/wl_e1/export/final_k_eor4x/wl_body.glb"
const SRC_V1_SNOW_TILE := "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cliffside3d/godot/textures/barrow/snow.png"

static var _bundled := -1


static func bundled() -> bool:
	if _bundled < 0:
		_bundled = 1 if FileAccess.file_exists(STAMP) else 0
	return _bundled == 1


static func join1_root() -> String:
	return "res://kc2/art/" if bundled() else SRC_JOIN1


static func model_pack_dir() -> String:
	return "res://kc2/model_pack" if bundled() else Kc2RtPackOfRecord.MODEL_DIR


static func geom() -> String:
	return "res://kc2/bundle/crucible-arena-geometry-v1.json" if bundled() else SRC_GEOM


static func font() -> String:
	return "res://kc2/bundle/Bangers-Regular.ttf.bin" if bundled() else SRC_FONT


static func eor3_matrix() -> String:
	return "res://kc2/bundle/gd-eor-warlord-eor3_matrix_index.json" if bundled() else SRC_EOR3_MATRIX


static func eor4x_glb() -> String:
	return "res://kc2/bundle/eor4x_wl_body.glb.bin" if bundled() else SRC_EOR4X_GLB


static func v1_snow_tile() -> String:
	return "res://kc2/bundle/v1_snow.png.bin" if bundled() else SRC_V1_SNOW_TILE


## Bundled inputs ship as their RAW BYTES named *.bin (the importer never touches a .bin, and the include filter ships
## the file itself -- the painted Barrow's rule), so every reader takes bytes, never an imported resource.
static func bytes(path: String) -> PackedByteArray:
	return FileAccess.get_file_as_bytes(path)


## An image from bytes, by its magic (PNG / WebP / JPEG), from res:// or an absolute path.
static func load_image(path: String) -> Image:
	var b := bytes(path)
	if b.size() < 12:
		return null
	var img := Image.new()
	var err := ERR_FILE_UNRECOGNIZED
	if b[0] == 0x89 and b[1] == 0x50:
		err = img.load_png_from_buffer(b)
	elif b.slice(0, 4).get_string_from_ascii() == "RIFF":
		err = img.load_webp_from_buffer(b)
	elif b[0] == 0xFF and b[1] == 0xD8:
		err = img.load_jpg_from_buffer(b)
	return img if err == OK else null


## THE LAUNCH REFUSAL (bundled builds): the vendored runtime's members re-hashed against its own MANIFEST, the tree
## digest re-derived by the manifest's law and compared with the stamp's pin (a0e75469...), and the model pack's
## member list against its pack digest. "" = intact; else the reason (the arena refuses to open the fight).
static func verify_bundle() -> String:
	if not bundled():
		return ""
	var stamp: Variant = JSON.parse_string(FileAccess.get_file_as_string(STAMP))
	if typeof(stamp) != TYPE_DICTIONARY:
		return "bundle stamp unreadable"
	var st: Dictionary = stamp
	var rt := _tree_check("res://kc2/kc2_runtime/", "MANIFEST.json", "tree_digest")
	if rt != String(st.get("runtime_tree_digest", "")):
		return "runtime tree %s != the pin %s" % [rt, String(st.get("runtime_tree_digest", ""))]
	var pk := _tree_check("res://kc2/model_pack/", "manifest.json", "pack_digest")
	if pk != String(st.get("model_pack_digest", "")) or pk != Kc2RtPackOfRecord.MODEL_DIGEST:
		return "model pack %s != the pin %s" % [pk, Kc2RtPackOfRecord.MODEL_DIGEST]
	return ""


## Every member re-hashed from the pck; returns the tree digest by the '<path>  <sha256>' sorted-lines law, or a
## "MISMATCH <path>" string on the first member whose bytes are not the manifest's.
static func _tree_check(root: String, man_name: String, key: String) -> String:
	var man: Variant = JSON.parse_string(FileAccess.get_file_as_string(root + man_name))
	if typeof(man) != TYPE_DICTIONARY:
		return "no manifest at " + root
	var lines := PackedStringArray()
	var mem: Array = (man as Dictionary).get("members", [])
	mem.sort_custom(func(a, b): return String(a["path"]) < String(b["path"]))
	for m_any in mem:
		var m: Dictionary = m_any
		var p := root + String(m["path"])
		var got := FileAccess.get_sha256(p)
		if got == "":
			var bytes := FileAccess.get_file_as_bytes(p)
			var ctx := HashingContext.new()
			ctx.start(HashingContext.HASH_SHA256)
			ctx.update(bytes)
			got = ctx.finish().hex_encode()
		if got != String(m["sha256"]):
			return "MISMATCH " + String(m["path"])
		lines.append("%s  %s" % [String(m["path"]), String(m["sha256"])])
	var c2 := HashingContext.new()
	c2.start(HashingContext.HASH_SHA256)
	c2.update("\n".join(lines).to_utf8_buffer())
	var d := c2.finish().hex_encode()
	return d if d == String((man as Dictionary).get(key, "")) else "TREE %s != manifest %s" % [d, String((man as Dictionary).get(key, ""))]
