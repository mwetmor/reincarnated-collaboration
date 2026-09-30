extends SceneTree
# C-9 T10-2: what the 16:9 lock does to the ROOT viewport, frame by frame, with no scene loaded.
# Run: Godot --path . --fullscreen --script tools/probe_view.gd
# It prints the OS window, the root Window's size, its texture's reported size, the size of the
# image that texture actually yields, the visible (frame) rect and the final transform.
var n := 0


func _process(_dt: float) -> bool:
	n += 1
	if n in [1, 2, 3, 5, 10, 20, 40, 60, 90, 120, 180, 240]:
		var rt := root.get_texture()
		var img := rt.get_image()
		print("[probe_view] frame=%d window=%s root.size=%s tex=%s img=%s visible=%s final_xform=%s mode=%d screen=%s scale=%s" % [
			n, DisplayServer.window_get_size(), root.size, rt.get_size(), img.get_size(),
			root.get_visible_rect().size, root.get_final_transform(), DisplayServer.window_get_mode(),
			DisplayServer.screen_get_size(), DisplayServer.screen_get_scale()])
	return n >= 240
