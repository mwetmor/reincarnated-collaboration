extends SceneTree
## Real arena + audio mixer: accepted/rejected casts, read-only event adapter,
## loop lifecycle, independent mutes, bounded voices and a non-silent capture.
var capture := AudioEffectCapture.new()
var peak := 0.0
var frames := 0
var scene = null

func _initialize() -> void:
	call_deferred("_run")

func _fail(message: String) -> void:
	push_error("ARENA_AUDIO: FAIL; " + message)
	quit(1)

func _drain() -> void:
	var samples := capture.get_buffer(capture.get_frames_available())
	frames += samples.size()
	for sample in samples:
		peak = maxf(peak, maxf(absf(sample.x), absf(sample.y)))

func _run() -> void:
	if OS.get_name() == "macOS":
		GDExtensionManager.load_extension("/Users/admin/Games/reincarnated-godot/kc2_runtime/native/kc2rt_contact.gdextension")
	scene = load("res://scenes/bv2f_arena.tscn").instantiate()
	root.add_child(scene)
	var deadline := Time.get_ticks_msec() + 120000
	while (scene.arena == null or not scene.arena.running) and Time.get_ticks_msec() < deadline:
		if scene.arena != null and scene.arena.fatal != "":
			_fail(scene.arena.fatal)
			return
		await process_frame
	if scene.arena == null or not scene.arena.running:
		_fail("startup timed out")
		return
	var arena = scene.arena
	if not arena.session.fight.select_contact_solver("gdscript"):
		_fail("PC reference solver selection refused")
		return
	var sound = arena.audio
	var expected_sfx := {}
	if sound != null:
		for ids in sound.manifest["cues"].values():
			for id in ids:
				expected_sfx[id] = true
	if sound == null or not sound.report["missing"].is_empty() or sound.streams.size() != expected_sfx.size():
		_fail("SFX missing/undecodable")
		return
	for track in sound.manifest["music"]:
		var id: String = track["clip"]
		var stream: AudioStream = sound._load_clip(id)
		if stream == null or absf(stream.get_length() - float(sound.manifest["clips"][id]["seconds"])) > 0.1:
			_fail("soundtrack decode/duration: " + id)
			return
	var ambience_present: bool = sound.manifest.has("ambience")
	if ambience_present:
		if sound.ambience_voices[0].stream == null:
			_fail("environment track missing")
			return
		sound._tick_ambience(0.016)
		var loops_before := int(sound.report["ambience_crossfades"])
		var environment_voice = sound.ambience_voices[sound.ambience_primary]
		environment_voice.seek(environment_voice.stream.get_length() - 0.4)
		await create_timer(1.0).timeout
		if int(sound.report["ambience_crossfades"]) <= loops_before:
			_fail("environment loop handoff failed")
			return
	capture.buffer_length = 2.0
	AudioServer.add_bus_effect(AudioServer.get_bus_index(sound.MIX), capture)
	# Public intents: first Potion is accepted; an immediate cooldown retry is not.
	arena.pending_presses = [{"skill_id": "potion", "aim_m": [0.0, 0.0]}]
	arena._one_tick()
	if int(sound.report["played"].get("potion", 0)) != 1:
		_fail("accepted potion has no cue")
		return
	sound.now += 0.2
	arena.pending_presses = [{"skill_id": "potion", "aim_m": [0.0, 0.0]}]
	arena._one_tick()
	if int(sound.report["played"].get("potion", 0)) != 1:
		_fail("cooldown-rejected potion played")
		return
	var state: String = JSON.stringify(arena.session.snapshot())
	for skill in ["blitz", "vires_might", "war_cry", "rune_of_rush"]:
		sound.consume([{"event": "cast_start", "actor_id": 0, "skill_id": skill}])
		if int(sound.report["played"].get(skill, 0)) != 1:
			_fail("hero cue missing: " + skill)
			return
	# Presentation adapter must leave the simulation exactly as it found it.
	if state != JSON.stringify(arena.session.snapshot()):
		_fail("audio altered fight state")
		return
	sound.consume([{"event": "channel_on", "actor_id": 0}])
	if not sound.whirlwind.playing:
		_fail("Whirlwind loop did not start")
		return
	sound.consume([{"event": "channel_off", "actor_id": 0}])
	if sound.whirlwind.playing:
		_fail("Whirlwind release did not stop loop")
		return
	# Same physical-hit clip: only the hero's outgoing Whirlwind contacts quieten.
	var hit_levels := {}
	for label in ["normal", "whirlwind", "incoming", "released"]:
		for voice in sound.player_voices + sound.enemy_voices:
			voice.stop()
		sound.now += 0.3
		if label == "whirlwind":
			sound.consume([{"event": "channel_on", "actor_id": 0}])
		elif label == "released":
			sound.consume([{"event": "channel_off", "actor_id": 0}])
		var incoming: bool = label == "incoming"
		sound.consume([{"event": "hit", "src_id": 1 if incoming else 0,
			"dst_id": 0 if incoming else 1, "damage_type": "Physical"}])
		var pool = sound.enemy_voices if incoming else sound.player_voices
		var level := 100.0
		for voice in pool:
			if voice.playing:
				level = voice.volume_db
		var expected := -8.0 if incoming else (-12.0 if label == "whirlwind" else -2.0)
		if not is_equal_approx(level, expected) or not is_equal_approx(sound.whirlwind.volume_db, -8.0):
			_fail("Whirlwind hit balance failed: %s, level %.2f expected %.2f" % [label, level, expected])
			return
		hit_levels[label] = level
	if state != JSON.stringify(arena.session.snapshot()):
		_fail("hit balance altered fight state")
		return
	sound.now += 0.3
	sound.consume([{"event": "channel_on", "actor_id": 0}])
	sound.toggle_sfx()
	if sound.whirlwind.playing or not AudioServer.is_bus_mute(AudioServer.get_bus_index(sound.SFX)):
		_fail("effects mute left loop alive")
		return
	sound.toggle_sfx()
	sound.toggle_music()
	if not AudioServer.is_bus_mute(AudioServer.get_bus_index(sound.MUSIC)) or not AudioServer.is_bus_mute(AudioServer.get_bus_index(sound.ENVIRONMENT)) or AudioServer.is_bus_mute(AudioServer.get_bus_index(sound.SFX)):
		_fail("music/effects mute not independent")
		return
	sound.toggle_music()
	# Deterministic bounded flood: player pool reserved, excess enemy tails dropped.
	for i in 50:
		sound.now += 0.2
		sound.cue("fire_cast", true, 0.0)
	if sound.active_voices() > 11 or int(sound.report["dropped"]) == 0:
		_fail("unbounded voices")
		return
	sound.reset()
	if sound.active_voices() != 0:
		_fail("restart left voices alive")
		return
	arena.autopilot = "channel"
	arena.fight_started = true
	var start := Time.get_ticks_msec()
	while Time.get_ticks_msec() - start < 10000:
		await process_frame
		_drain()
	if peak <= 0.0001 or peak > 0.9 or frames == 0:
		_fail("mixed audio silent/clipping: peak %.5f frames %d" % [peak, frames])
		return
	if int(sound.report["played"].get("physical_hit", 0)) == 0:
		_fail("real combat impacts missing")
		return
	sound.end_fight()
	if sound.whirlwind.playing:
		_fail("terminal fight left loop alive")
		return
	var result := {"platform": OS.get_name(), "audio_driver": AudioServer.get_driver_name(),
		"solver": arena.session.fight.contact_solver,
		"audio_manifest_sha256": FileAccess.get_sha256(sound.MANIFEST),
		"sfx_decoded": sound.streams.size(), "music_decoded": sound.manifest["music"].size(),
		"environment_loop_handoff": ambience_present, "ambience_crossfades": sound.report["ambience_crossfades"],
		"mixed_frames": frames, "mixed_peak": peak, "report": sound.report,
		"accepted_vs_cooldown_refusal": true, "adapter_snapshot_unchanged": true,
		"loop_lifecycle_and_independent_mutes": true, "voice_cap": 11}
	result["hit_voice_db"] = hit_levels
	result["pendulum_voice_db"] = sound.whirlwind.volume_db
	var args := OS.get_cmdline_user_args()
	var at := args.find("--audio-evidence")
	if at >= 0 and at + 1 < args.size():
		var path := args[at + 1]
		DirAccess.make_dir_recursive_absolute(path.get_base_dir())
		var file := FileAccess.open(path, FileAccess.WRITE)
		file.store_string(JSON.stringify(result, "\t"))
		file.close()
	print("ARENA_AUDIO: PASS; " + JSON.stringify(result))
	arena._close_recording("audio probe")
	quit(0)
