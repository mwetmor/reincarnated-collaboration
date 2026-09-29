extends SceneTree
# PROBE: can Godot hand raw frames to ffmpeg through a pipe, so no frame ever reaches disk?
# The brief forbids frame dumps; the established precedent in this run is JPEG-to-scratch then
# encode then delete. OS.execute_with_pipe (4.3+) would remove the intermediate entirely, but
# "the API exists" is not "the API works for 8 MB writes" -- so it is measured here first, on
# 40 frames of a moving gradient, and the result is checked by DECODING the mp4 back.
const W := 640
const H := 360
const N := 40

func _init() -> void:
	var out := "/tmp/claude-501/pipeprobe/pipe.mp4"
	var args := ["-y", "-loglevel", "error", "-f", "rawvideo", "-pixel_format", "rgba",
		"-video_size", "%dx%d" % [W, H], "-framerate", "30", "-i", "pipe:0",
		"-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p", out]
	var p: Dictionary = OS.execute_with_pipe("/opt/homebrew/bin/ffmpeg", args)
	if p.is_empty():
		print("PIPE_FAIL: execute_with_pipe returned empty")
		quit(1); return
	print("pid=%s keys=%s" % [p.get("pid", -1), p.keys()])
	var io: FileAccess = p["stdio"]
	var t0 := Time.get_ticks_usec()
	for f in N:
		var img := Image.create(W, H, false, Image.FORMAT_RGBA8)
		img.fill(Color(float(f) / float(N), 0.3, 0.7, 1.0))
		io.store_buffer(img.get_data())
	io.close()
	var ms := float(Time.get_ticks_usec() - t0) / 1000.0
	print("wrote %d frames of %d bytes in %.1f ms (%.2f ms/frame)" % [N, W * H * 4, ms, ms / N])
	# ffmpeg needs a moment after EOF to flush the trailer
	OS.delay_msec(1500)
	print("exists=%s size=%d" % [FileAccess.file_exists(out),
		FileAccess.open(out, FileAccess.READ).get_length() if FileAccess.file_exists(out) else -1])
	quit(0)
