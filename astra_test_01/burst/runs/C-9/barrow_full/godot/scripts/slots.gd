extends RefCounted
class_name Slots
## C-9 R-C9-117 -- WHICH SLOT WALKS THE PAINTED BARROW, from the select page's query (or the desktop's args). drax.
##   ?c=barbarian|sorceress|warlord
##   ?armor=   sorceress: cur | bmc | bmd           barbarian: viking | gladc | gladb
##   ?hold=    barbarian with the viking set: (absent: the page's own T12_10) | t1211 | f25l | f40l   (web only)
## (?fb, ?meteor, ?fall are read where they always were.) A variant's models are their own pack, fetched by the page
## only for that variant (variant_<slot>.pck); on the desktop the files are already under res://.

const SLOTS := {
	"so_bmc": {"who": "sorceress", "path": "res://data/slots/so_bmc.json", "script": "res://scripts/slot_knight.gd",
		"sockets": "res://data/slots/sockets_so_bm.json", "label": "battle mage C (painted)"},
	"so_bmd": {"who": "sorceress", "path": "res://data/slots/so_bmd.json", "script": "res://scripts/slot_knight.gd",
		"sockets": "res://data/slots/sockets_so_bm.json", "label": "battle mage D (painted + steel pass)"},
	"barb_gladc": {"who": "barbarian", "path": "res://data/slots/barb_gladc.json", "script": "res://scripts/slot_knight_him.gd",
		"label": "champion gladiator C (painted + colour)"},
	"barb_gladb": {"who": "barbarian", "path": "res://data/slots/barb_gladb.json", "script": "res://scripts/slot_knight_him.gd",
		"label": "champion gladiator B (painted)"},
	"barb_t1211": {"who": "barbarian", "path": "res://data/slots/barb_t1211.json", "script": "res://scripts/variants/slot_knight_t12.gd",
		"label": "axe hold T12_11 (installed)"},
	"barb_f25l": {"who": "barbarian", "path": "res://data/slots/barb_f25l.json", "script": "res://scripts/variants/slot_knight_t12.gd",
		"label": "axe hold T12_12c F25L"},
	"barb_f40l": {"who": "barbarian", "path": "res://data/slots/barb_f40l.json", "script": "res://scripts/variants/slot_knight_t12.gd",
		"label": "axe hold T12_12c F40L"},
	"warlord": {"who": "warlord", "path": "res://data/slots/warlord.json", "script": "res://scripts/slot_knight.gd",
		"label": "dark knight"},
}


static func arg(key: String) -> String:
	var q := PaintStack.web_query(key)
	if q != "":
		return q.to_lower()
	var a := OS.get_cmdline_user_args()
	var i := a.find("--" + key)
	return String(a[i + 1]).to_lower() if i >= 0 and i + 1 < a.size() else ""


static func choose(who: String) -> String:
	"""The slot id for this page ("" = the page's own character, unchanged)."""
	if who == "warlord":
		return "warlord"
	var armor := arg("armor")
	if who == "sorceress":
		return {"bmc": "so_bmc", "bmd": "so_bmd"}.get(armor, "")
	if armor in ["gladc", "gladb"]:
		return "barb_" + armor
	var hold := arg("hold")
	return {"t1211": "barb_t1211", "f25l": "barb_f25l", "f40l": "barb_f40l"}.get(hold, "")


static func fetch_pack(host: Node, slot: String) -> Dictionary:
	"""On the page: the slot's own pack (variant_<slot>.pck), fetched and loaded unless the main pack holds it."""
	var s: Dictionary = SLOTS.get(slot, {})
	var a := OS.get_cmdline_user_args()
	if not OS.has_feature("web") and a.find("--variant-pack") >= 0 and not FileAccess.file_exists(String(s.get("path", ""))):
		# the build's launch fence: the desktop cannot fetch, so it is handed the variant's pack file
		var vp := String(a[a.find("--variant-pack") + 1])
		return {"pack": vp.get_file(), "loaded": ProjectSettings.load_resource_pack(vp)}
	if s.is_empty() or FileAccess.file_exists(String(s["path"])) or not OS.has_feature("web"):
		return {"pack": "in main" if FileAccess.file_exists(String(s.get("path", ""))) else "none"}
	var base := str(JavaScriptBridge.eval("document.baseURI", true))
	var nm := "variant_%s.pck" % slot
	var url := base.get_base_dir() + "/" + nm if not base.ends_with("/") else base + nm
	var http := HTTPRequest.new()
	host.add_child(http)
	http.download_file = "user://" + nm
	var t0 := Time.get_ticks_msec()
	http.request(url)
	var res: Array = await http.request_completed
	http.queue_free()
	var ok := int(res[0]) == HTTPRequest.RESULT_SUCCESS and int(res[1]) == 200
	return {"pack": nm, "http": int(res[1]), "ms": Time.get_ticks_msec() - t0,
		"loaded": ProjectSettings.load_resource_pack("user://" + nm) if ok else false}
