extends Node
## Presentation-only audio. Consume accepted events; never write fight state or draw its RNG.
## Original demo files are staged by tools/arena_stage_audio.py; raw .bin files survive exports.
const MANIFEST := "res://data/audio/arena_audio.json"
const EnemyVFX = preload("res://scripts/arena/arena_enemy_vfx.gd")
const MIX := "BarrowMix"
const SFX := "BarrowSFX"
const MUSIC := "BarrowMusic"
var mode = null
var manifest: Dictionary = {}
var streams: Dictionary = {}
var rotations: Dictionary = {}
var last_cue: Dictionary = {}
var player_voices: Array[AudioStreamPlayer] = []
var enemy_voices: Array[AudioStreamPlayer] = []
var whirlwind: AudioStreamPlayer
var music: AudioStreamPlayer
var now := 0.0
var music_index := 2
var music_muted := false
var sfx_muted := false
var focused := true
var previous_pos := Vector2.ZERO
var stride_m := 0.0
var music_db := -20.0
var last_combat := -10.0
var report := {"loaded": 0, "missing": [], "played": {}, "dropped": 0, "peak_voices": 0}
var fallback_classifier = null


func setup(arena) -> void:
	mode = arena
	fallback_classifier = EnemyVFX.new()
	fallback_classifier.mode = arena
	fallback_classifier._build_families()
	for pair in [[MIX, "Master", 0.0], [SFX, MIX, -10.0], [MUSIC, MIX, music_db]]:
		if AudioServer.get_bus_index(pair[0]) < 0:
			AudioServer.add_bus()
			var i := AudioServer.bus_count - 1
			AudioServer.set_bus_name(i, pair[0])
			AudioServer.set_bus_send(i, pair[1])
			AudioServer.set_bus_volume_db(i, pair[2])
	var limiter := AudioEffectHardLimiter.new()
	limiter.ceiling_db = -1.0
	AudioServer.add_bus_effect(AudioServer.get_bus_index(MIX), limiter)
	for i in 4:
		player_voices.append(_voice("PlayerSound%d" % i, SFX))
	for i in 6:
		enemy_voices.append(_voice("MonsterSound%d" % i, SFX))
	whirlwind = _voice("Whirlwind", SFX)
	music = _voice("Soundtrack", MUSIC)
	if not FileAccess.file_exists(MANIFEST):
		push_warning("Arena audio manifest missing; run arena_stage_audio.py")
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
	if not parsed is Dictionary:
		push_warning("Arena audio manifest invalid")
		return
	manifest = parsed
	music_index = int(manifest.get("default_music", 2))
	# Decode SFX once. Music loads lazily as compressed MP3, one current track at a time.
	for ids in manifest.get("cues", {}).values():
		for id in ids:
			if not streams.has(id):
				var stream := _load_clip(id)
				if stream != null:
					streams[id] = stream
	var loop_stream: AudioStream = _stream_for("whirlwind_loop")
	if loop_stream is AudioStreamWAV:
		loop_stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		loop_stream.loop_begin = 0
		loop_stream.loop_end = roundi(loop_stream.get_length() * loop_stream.mix_rate)
	whirlwind.stream = loop_stream
	whirlwind.volume_db = -8.0
	reset()
	print("[arena audio] %d SFX decoded; %d music tracks; missing %s" %
		[streams.size(), manifest.get("music", []).size(), str(report["missing"])])


func _voice(label: String, bus: String) -> AudioStreamPlayer:
	var voice := AudioStreamPlayer.new()
	voice.name = label
	voice.bus = bus
	add_child(voice)
	return voice


func _load_clip(id: String) -> AudioStream:
	var clip: Dictionary = manifest.get("clips", {}).get(id, {})
	var path := MANIFEST.get_base_dir().path_join(String(clip.get("file", "")))
	if clip.is_empty() or not FileAccess.file_exists(path) or FileAccess.get_sha256(path) != String(clip.get("sha256", "")):
		report["missing"].append(id)
		push_warning("Arena audio missing/changed: " + path)
		return null
	var bytes := FileAccess.get_file_as_bytes(path)
	var stream: AudioStream = null
	match String(clip.get("format", "")):
		"wav":
			stream = AudioStreamWAV.load_from_buffer(bytes)
		"ogg":
			stream = AudioStreamOggVorbis.load_from_buffer(bytes)
		"mp3":
			stream = AudioStreamMP3.load_from_buffer(bytes)
	if stream == null or stream.get_length() <= 0.0:
		report["missing"].append(id)
		return null
	report["loaded"] = int(report["loaded"]) + 1
	return stream


func _stream_for(cue: String) -> AudioStream:
	var ids: Array = manifest.get("cues", {}).get(cue, [])
	if ids.is_empty():
		return null
	var n := int(rotations.get(cue, 0))
	rotations[cue] = n + 1
	return streams.get(String(ids[n % ids.size()]), null)


func cue(key: String, enemy := false, interval := 0.08, gain_db := 0.0) -> bool:
	if not focused or sfx_muted or now - float(last_cue.get(key, -10.0)) < interval:
		return false
	var stream := _stream_for(key)
	if stream == null:
		return false
	var pool: Array[AudioStreamPlayer] = enemy_voices if enemy else player_voices
	var selected: AudioStreamPlayer = null
	for voice in pool:
		if not voice.playing:
			selected = voice
			break
	if selected == null and not enemy:
		# Player feedback has reserved voices; replace its oldest tail if necessary.
		selected = pool[0]
		for voice in pool:
			if float(voice.get_meta("started", 0.0)) < float(selected.get_meta("started", 0.0)):
				selected = voice
	if selected == null:
		report["dropped"] = int(report["dropped"]) + 1
		return false
	selected.stop()
	selected.stream = stream
	selected.volume_db = gain_db - (8.0 if enemy else 2.0)
	selected.set_meta("started", now)
	selected.play()
	last_cue[key] = now
	last_combat = now if key != "snow_step" else last_combat
	report["played"][key] = int(report["played"].get(key, 0)) + 1
	report["peak_voices"] = maxi(int(report["peak_voices"]), active_voices())
	return true


func active_voices() -> int:
	var n := 1 if whirlwind.playing else 0
	for voice in player_voices + enemy_voices:
		if voice.playing:
			n += 1
	return n


func _record(id: int) -> String:
	var actor = mode.actors.get(id, null)
	if actor != null:
		return String(actor.record)
	for actor_row in mode.snap.get("actors", []):
		if int(actor_row.get("id", -1)) == id:
			return String(actor_row.get("record_path", ""))
	return ""


func _voice_family(record: String) -> String:
	var p := record.to_lower()
	if p.contains("wraith") or p.contains("ghost") or p.contains("spectr") or p.contains("banshee"):
		return "ghost"
	if p.contains("golem") or p.contains("construct") or p.contains("elemental_earth"):
		return "golem"
	if p.contains("ghoul") or p.contains("zombie"):
		return "ghoul"
	if p.contains("orc"):
		return "orc"
	return "enemy"


func consume(events: Array) -> void:
	for e in events:
		var event := String(e.get("event", ""))
		var id := int(e.get("actor_id", -1))
		match event:
			"cast_start":
				var skill := String(e.get("skill_id", ""))
				if id == 0:
					cue(skill, false, 0.1)
				elif id > 0:
					var record := _record(id)
					var c: Dictionary = {}
					if mode.enemy_vfx != null:
						c = mode.enemy_vfx.classify(record, skill)
					else:
						# Classifier has no visual setup/process; only reads the sealed roster.
						c = fallback_classifier.classify(record, skill)
					var element := String(c.get("el", "physical"))
					var key := "slash" if element == "physical" else element + "_cast"
					if element == "physical" and String(c.get("cls", "")) == "ranged":
						key = "arrow_cast"
					if _voice_family(record) == "ghost" and String(c.get("cls", "")) == "melee":
						key = "ghost_cast"
					cue(key, true, 0.18)
			"channel_on":
				if id == 0:
					cue("whirlwind_start", false, 0.2)
					if focused and not sfx_muted and whirlwind.stream != null:
						whirlwind.play()
			"channel_off":
				if id == 0:
					whirlwind.stop()
			"hit":
				var source := int(e.get("src_id", -1))
				var target := int(e.get("dst_id", -1))
				if source == 0 or target == 0:
					var families := {String(e.get("damage_type", "Physical")): true}
					var element := EnemyVFX._element(families, "")
					cue(element + "_hit", target == 0, 0.14)
			"death":
				if id > 0:
					cue(_voice_family(_record(id)) + "_death", true, 0.25)
			"player_death":
				whirlwind.stop()
				cue("player_death", false, 0.5)
			"energy_refused":
				cue("energy_refused", false, 0.8, -6.0)


func reset() -> void:
	for voice in player_voices + enemy_voices:
		voice.stop()
	whirlwind.stop()
	music.stop()
	music.stream = null
	last_cue.clear()
	stride_m = 0.0
	previous_pos = mode.player_pos_m


func end_fight() -> void:
	whirlwind.stop()
	for voice in enemy_voices:
		voice.stop()


func toggle_sfx() -> void:
	sfx_muted = not sfx_muted
	AudioServer.set_bus_mute(AudioServer.get_bus_index(SFX), sfx_muted)
	if sfx_muted:
		whirlwind.stop()
	elif mode.running and mode.fight_started and mode.session.driver.channel_on and whirlwind.stream != null:
		whirlwind.play()


func toggle_music() -> void:
	music_muted = not music_muted
	AudioServer.set_bus_mute(AudioServer.get_bus_index(MUSIC), music_muted)


func next_music() -> void:
	var tracks: Array = manifest.get("music", [])
	if tracks.is_empty():
		return
	music_index = (music_index + 1) % tracks.size()
	_play_music()


func _play_music() -> void:
	var tracks: Array = manifest.get("music", [])
	if tracks.is_empty():
		return
	var stream := _load_clip(String(tracks[music_index]["clip"]))
	if stream is AudioStreamMP3:
		stream.loop = true
		music.stop()
		music.stream = stream
		music.play()


func music_title() -> String:
	var tracks: Array = manifest.get("music", [])
	return String(tracks[music_index]["title"]) if not tracks.is_empty() else "unavailable"


func _process(delta: float) -> void:
	now += delta
	if mode == null or mode.session == null:
		return
	if mode.fight_started and not music.playing and music.stream == null:
		_play_music()
	var target_db := -26.0 if now - last_combat < 0.5 or whirlwind.playing else -20.0
	music_db = move_toward(music_db, target_db, delta * 12.0)
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index(MUSIC), music_db)
	var distance: float = mode.player_pos_m.distance_to(previous_pos)
	previous_pos = mode.player_pos_m
	if mode.running and mode.fight_started and mode.session.driver.charge_to == null and distance < 2.5:
		stride_m += distance
		if stride_m >= 1.1:
			stride_m = 0.0
			cue("snow_step", false, 0.22, -9.0)
	else:
		stride_m = 0.0


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_APPLICATION_FOCUS_IN:
		focused = what == NOTIFICATION_APPLICATION_FOCUS_IN
		for child in get_children():
			if child is AudioStreamPlayer:
				child.stream_paused = not focused


func _exit_tree() -> void:
	if fallback_classifier != null:
		fallback_classifier.free()
	# Arena owns these buses; leave the rest of the application's audio untouched.
	for bus in [MUSIC, SFX, MIX]:
		var index := AudioServer.get_bus_index(bus)
		if index >= 0:
			AudioServer.remove_bus(index)
