extends SceneTree
func _initialize() -> void:
	for src in [["res://data/height_a_authored.png","res://data/height_a_authored.json"],
				["res://data/height_a_marigold.png","res://data/height_a_marigold.json"]]:
		var w := BarrowHeightfield.new(src[0], src[1])
		var pts := []
		for p in [Vector2(0,-4), Vector2(0,0), Vector2(-6,4), Vector2(30,30)]:
			pts.append("%s=%.2f" % [p, w.height_at(p.x, p.y)])
		print("   heights: %s   normal at mound %s" % [", ".join(pts), w.normal_at(0,-4)])
	quit(0)
