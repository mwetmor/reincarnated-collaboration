extends RefCounted
class_name BundleLoader
# ============================================================================
# bundle_loader.gd — ONE REALM DEMO BUNDLE LOADER (D4).
#
# Consumes star-lord's one_realm_demo_bundle.json (the D1 bundle-schema contract,
# LOCKED via the drax handshake 2026-07-02) and instantiates kits / monsters /
# gear / factions / floor-manifest from ENGINE-EMITTED RECORDS. There are ZERO
# hand-built kits Godot-side — the engine is the product; this loader is a pure
# CONSUMER (one-realm §6.1, §20d the condition under test).
#
# Built against the LOCKED SCHEMA SHAPE (drax's signed handshake answers), NOT a
# DRAFT. Architecture: RUNTIME JSON PARSE (handshake Q1/Q2 — single inline JSON,
# no .tres refs), mirroring the proven data/arena_scenarios.json consume pattern
# in render_arena_room.gd :_load_spec().
#
# SCHEMA-SHAPE SOURCE OF TRUTH:
#   reincarnated-engine/src/reincarnated/export/math/2026-07-02-one-realm-bundle-schema-note.md
#   + drax handshake: agentic_orchestration/drax/notes/2026-07-02-one-realm-bundle-schema-handshake-drax-SIGNED.md
#
# WHAT THIS LOADER DOES (D4 scope):
#   - parse the bundle (single JSON) into typed record dictionaries
#   - instantiate kit / monster / gear records as engine-truth data objects
#   - resolve each kit's primary_attack skill (the §20d playability predicate)
#   - flag the 4 SCAFFOLD proxy magnitudes as NON-TUNED (handshake Q4; gamora-D3
#     calibration targets — Discipline #9)
#   - consume the per-floor element-rotation manifest
#   - apply faction as a PRESENTATION RESTYLE ONLY (III.7 invariant — the restyle
#     pass has no write access to any fight-model field)
#   - null-safe fallbacks for null name/flavor_text (handshake Q3)
#
# WHAT THIS LOADER DOES NOT DO (out of scope — later dispatches):
#   - realize verbs (D5), author floors (D6), enemy AI (D7), UI (D8)
#   - Synty prefab MESH instancing beyond archetype_tag→mesh-set keying (that is the
#     verb/floor build; here we RESOLVE the record + expose the mesh-set key)
#
# drax, 2026-07-02 (D4). WAIT-for-lock guard: the ROUND-TRIP against a real bundle
# file only runs once MIGRATION.md v1.83 reads LOCKED AND the emitted bundle carries
# >=1 non-empty proxies payload (see bundle_roundtrip_smoke.gd).
# ============================================================================

# --- the 4 SCAFFOLD proxy fields (handshake Q4; schema note :162-165) --------
# These are gamora-D3 calibration targets. The loader carries them behind a
# scaffold marker and NEVER presents them as tuned numbers (Discipline #9).
const SCAFFOLD_PROXY_FIELDS := ["base_hp", "damage_multiplier", "attack_interval_s", "proxy_max_active"]

# --- the 10-slot canonical gear vocabulary (handshake Q3; schema note :259) ---
# This is the vocabulary for GearRecord.gear_slot on gear_pool[] records (the
# populated 150-item pool, MIGRATION §v1.84). DISTINCT from the 11-slot vocab on
# KitRecord.gear_representative below (§v1.84 vocab ruling — path (a)).
const GEAR_SLOTS_10 := ["main_hand", "off_hand", "head", "chest", "hands", "feet", "belt", "ring_1", "ring_2", "amulet"]

# --- the 11-slot gear_representative vocabulary (MIGRATION §v1.84, path (a)) ---
# RULING (star-lord, MIGRATION §v1.84): the KitRecord.gear_representative field is
# the cycle-14 ClassData 11-slot GENERATION vocabulary and is DECLARED CANONICAL —
# it is a DISTINCT field from GearRecord.gear_slot (10-slot). It predates the Path-B
# SEAM-3 renaming, which applies ONLY to the loadout equipped-gear dict, not here.
# main_weapon = the weapon slot; secondary_item = the off-hand; legs = the legs slot.
# The D4-close deduped-WARN is RESOLVED here: we ACCEPT these 11 keys rather than warn.
const GEAR_REP_SLOTS_11 := ["main_weapon", "secondary_item", "legs", "head", "chest", "hands", "feet", "belt", "ring_1", "ring_2", "amulet"]

# --- fight-model fields faction restyle must NEVER touch (III.7 guard) --------
const FIGHT_MODEL_FIELDS := ["stat_distribution", "skills", "elemental_resistances", "damage_multiplier", "damage_scaling_type", "elemental_affinity"]

# parsed bundle state
var bundle_version: String = ""
var engine_version: String = ""
var season_id: String = ""
var schema_status: String = ""
var kits: Array = []
var monsters: Array = []
var gear_pool: Array = []
var factions: Dictionary = {}          # FactionBlock or {} if null
var floor_manifest: Dictionary = {}
var errors: Array[String] = []
var warnings: Array[String] = []
# gear_representative slot keys that fall OUTSIDE the ratified 11-slot vocab, warned
# ONCE per distinct offending key. Post §v1.84 this only fires for a genuinely
# UNKNOWN key (i.e. not in GEAR_REP_SLOTS_11) — the former 10-vs-11 deduped-WARN for
# main_weapon/secondary_item/legs is RESOLVED (those are now canonical, path (a)).
var _warned_noncanon_slots: Dictionary = {}


# ---------------------------------------------------------------------------
# LOAD — parse the single-JSON bundle. Returns true on clean parse.
# ---------------------------------------------------------------------------
func load_bundle(path: String) -> bool:
	errors.clear()
	warnings.clear()
	_warned_noncanon_slots.clear()
	if not FileAccess.file_exists(path):
		errors.append("bundle file not found: %s" % path)
		return false
	var txt := FileAccess.get_file_as_string(path)
	if txt.is_empty():
		errors.append("bundle file empty: %s" % path)
		return false
	var parsed: Variant = JSON.parse_string(txt)
	if parsed == null or typeof(parsed) != TYPE_DICTIONARY:
		errors.append("bundle JSON parse failed or root is not an object")
		return false
	var root: Dictionary = parsed

	bundle_version = str(root.get("bundle_version", ""))
	engine_version = str(root.get("engine_version", ""))
	season_id = str(root.get("season_id", ""))
	schema_status = str(root.get("schema_status", ""))

	# top-level type keys (handshake Q1 — single inline JSON, top-level per type)
	kits = root.get("kits", [])
	monsters = root.get("monsters", [])
	gear_pool = root.get("gear_pool", [])
	var fb: Variant = root.get("factions", null)
	factions = fb if (fb != null and typeof(fb) == TYPE_DICTIONARY) else {}
	floor_manifest = root.get("floor_manifest", {})

	if typeof(kits) != TYPE_ARRAY: errors.append("'kits' is not a list"); return false
	if typeof(monsters) != TYPE_ARRAY: errors.append("'monsters' is not a list"); return false
	if typeof(gear_pool) != TYPE_ARRAY: errors.append("'gear_pool' is not a list"); return false

	return true


# ---------------------------------------------------------------------------
# INSTANTIATE A KIT — resolve a KitRecord into a usable kit object.
# The §20d playability predicate lives here: a kit is PLAYABLE iff its
# primary_attack skill resolves with name + geometry + range_m present and
# non-degenerate. A record that merely parses is NOT playable.
# ---------------------------------------------------------------------------
func instantiate_kit(rec: Dictionary) -> Dictionary:
	var kit := {}
	kit["id"] = str(rec.get("id", ""))
	kit["name"] = _name_or_fallback(rec, "%s" % rec.get("archetype_tag", "kit"))
	kit["flavor_text"] = rec.get("flavor_text", null)   # kit flavor populated (TRACK NEW); null-safe anyway
	kit["archetype_tag"] = str(rec.get("archetype_tag", ""))
	kit["energy_type"] = str(rec.get("energy_type", ""))
	kit["role_orientation"] = str(rec.get("role_orientation", ""))
	kit["range_profile"] = str(rec.get("range_profile", ""))
	kit["dominant_element"] = str(rec.get("dominant_element", ""))
	# THEME/COLOR KEY (load-bearing — answers the D4 color-key question):
	# the loader keys presentation theme/color off the KIT's dominant_element, NOT
	# off skill-level canonical_element. On e.g. the Crypt-Lieutenant these DIVERGE
	# (dominant_element='earth' vs skills' canonical_element='water'); the loader
	# themes on 'earth' (coherent). Because the loader never surfaces the skill-level
	# element as the theme key, rocket's parked skill-element rotation (water->dark)
	# is NOT owed for presentation coherence. If a future dispatch re-keys theme off
	# canonical_element, THAT is when the rotation becomes owed — flag it here.
	kit["theme_element_key"] = str(rec.get("dominant_element", ""))
	kit["stat_distribution"] = rec.get("stat_distribution", {})
	# archetype_tag is the Synty-prefab mesh-set key (open question resolved: mesh
	# keys off archetype_tag; §6.1 asset mapping). Verb/floor build consumes this.
	kit["mesh_set_key"] = str(rec.get("archetype_tag", ""))

	# --- skills ---
	var skills: Array = rec.get("skills", [])
	kit["skills"] = []
	for s in skills:
		if typeof(s) == TYPE_DICTIONARY:
			kit["skills"].append(_instantiate_skill(s))

	# --- the §20d playability resolution ---
	var primary := _resolve_primary_attack(kit["skills"])
	kit["primary_attack"] = primary
	kit["playable"] = _is_playable(primary)

	# --- proxies (summoner mandate §3; SCAFFOLD-flagged per Q4) ---
	var proxies: Array = rec.get("proxies", [])
	kit["proxies"] = []
	for p in proxies:
		if typeof(p) == TYPE_DICTIONARY:
			kit["proxies"].append(_instantiate_proxy(p))
	kit["is_summoner"] = kit["proxies"].size() > 0

	# --- gear representative (11-slot canonical; MIGRATION §v1.84 path (a)) ---
	kit["gear_representative"] = _resolve_gear_representative(rec.get("gear_representative", {}))

	# --- faction (presentation restyle ONLY — III.7) ---
	# parent_faction_id / parent_faction_label are presentation-side; carried, never
	# fed to a fight-model field. The restyle application is a SEPARATE pass
	# (apply_faction_restyle) that cannot reach stat_distribution/skills/resistances.
	kit["parent_faction_id"] = rec.get("parent_faction_id", null)
	kit["parent_faction_label"] = rec.get("parent_faction_label", null)

	return kit


func _instantiate_skill(s: Dictionary) -> Dictionary:
	return {
		"id": str(s.get("id", "")),
		"name": str(s.get("name", "")) if s.get("name") != null else "",
		"flavor_text": s.get("flavor_text", null),   # null-accepted (Q3); UI omits the line
		"role": str(s.get("role", "")),
		"canonical_element": str(s.get("canonical_element", "")),
		"geometry": str(s.get("geometry", "")) if s.get("geometry") != null else "",
		"range_m": float(s.get("range_m", 0.0)) if s.get("range_m") != null else 0.0,
		"damage_multiplier": float(s.get("damage_multiplier", 0.0)) if s.get("damage_multiplier") != null else 0.0,
		"effect_category": str(s.get("effect_category", "")),
		"composition_mode": str(s.get("composition_mode", "")),
		"effects": s.get("effects", []),
	}


# The §20d predicate resolver. primary_attack = the skill whose role is
# "primary_attack". Returns {} if none present.
func _resolve_primary_attack(skills: Array) -> Dictionary:
	for sk in skills:
		if typeof(sk) == TYPE_DICTIONARY and str(sk.get("role", "")) == "primary_attack":
			return sk
	return {}


# PLAYABILITY (Gate-1 fold 4 / §20d honesty): name + geometry + range_m present and
# NON-DEGENERATE (non-empty name, non-empty geometry, range_m > 0). A record that
# parses but has an empty geometry or range_m=0 is NOT playable — the summon/attack
# verb has nothing to realize.
func _is_playable(primary: Dictionary) -> bool:
	if primary.is_empty():
		return false
	var nm := str(primary.get("name", ""))
	var geo := str(primary.get("geometry", ""))
	var rng := float(primary.get("range_m", 0.0))
	return nm.length() > 0 and geo.length() > 0 and rng > 0.0


# PROXY instantiation — flags the 4 SCAFFOLD magnitudes as NON-TUNED (Q4 / #9).
func _instantiate_proxy(p: Dictionary) -> Dictionary:
	var proxy := {
		"proxy_type": str(p.get("proxy_type", "")),
		"behavioral_tier": str(p.get("behavioral_tier", "")),
		"range_m": float(p.get("range_m", 0.0)) if p.get("range_m") != null else 0.0,
		"targeting_behavior": str(p.get("targeting_behavior", "")),
		"count": int(p.get("count", 0)),
		"duration_s": float(p.get("duration_s", 0.0)) if p.get("duration_s") != null else 0.0,
		"acquisition": str(p.get("acquisition", "")),
		# proxy-strike geometry + re-raise cadence — the on-screen HORDE-vs-BRUISER
		# read levers (summoner-kit designation §3: many-light-fast melee_strike/count-2/
		# cadence-6 vs one-heavy-slow ground_slam/count-1/cadence-9). These are emitted
		# non-scaffold fields (NOT among the 4 calibration magnitudes); the D5 summon verb
		# stages the legibility read off them. Added D5 (loader boundary was dropping them).
		"geometry": str(p.get("geometry", "")),
		"spawn_cadence_s": float(p.get("spawn_cadence_s", 6.0)) if p.get("spawn_cadence_s") != null else 6.0,
		# --- SCAFFOLD block: gamora-D3 calibration targets. NON-TUNED. ---
		"scaffold": true,
		"scaffold_fields": SCAFFOLD_PROXY_FIELDS.duplicate(),
		"base_hp_SCAFFOLD": float(p.get("base_hp", 0.0)) if p.get("base_hp") != null else 0.0,
		"damage_multiplier_SCAFFOLD": float(p.get("damage_multiplier", 0.0)) if p.get("damage_multiplier") != null else 0.0,
		"attack_interval_s_SCAFFOLD": float(p.get("attack_interval_s", 0.0)) if p.get("attack_interval_s") != null else 0.0,
		"proxy_max_active_SCAFFOLD": int(p.get("proxy_max_active", 0)),
	}
	return proxy


func _resolve_gear_representative(gr: Variant) -> Dictionary:
	var out := {}
	if typeof(gr) != TYPE_DICTIONARY:
		return out
	var g: Dictionary = gr
	# iterate the 11 canonical gear_representative slots (§v1.84 path (a) — this field
	# is the cycle-14 ClassData 11-slot vocab, DECLARED CANONICAL by star-lord). No WARN
	# for main_weapon/secondary_item/legs — they are accepted keys, not divergences.
	for slot in GEAR_REP_SLOTS_11:
		if g.has(slot):
			out[slot] = g[slot]
	# Only a key OUTSIDE the ratified 11-slot vocab is a genuine schema surprise now.
	for k in g.keys():
		if not GEAR_REP_SLOTS_11.has(k) and not _warned_noncanon_slots.has(k):
			_warned_noncanon_slots[k] = true
			warnings.append("gear_representative carries slot key '%s' outside the ratified 11-slot vocab (§v1.84). Non-fatal; routed to star-lord as an engine-side schema surprise." % k)
	return out


# ---------------------------------------------------------------------------
# INSTANTIATE A MONSTER — MonsterRecord (null name/flavor accepted, Q3).
# ---------------------------------------------------------------------------
func instantiate_monster(rec: Dictionary) -> Dictionary:
	return {
		"id": str(rec.get("id", "")),
		"name": _name_or_fallback(rec, "%s (%s)" % [rec.get("archetype_tag", "monster"), rec.get("threat_tier", "?")]),
		"flavor_text": rec.get("flavor_text", null),
		"threat_tier": str(rec.get("threat_tier", "")),
		"archetype_tag": str(rec.get("archetype_tag", "")),
		"dominant_element": str(rec.get("dominant_element", "")),
		"max_hp": float(rec.get("max_hp", 0.0)) if rec.get("max_hp") != null else 0.0,
		"armor": float(rec.get("armor", 0.0)) if rec.get("armor") != null else 0.0,
		"elemental_resistances": rec.get("elemental_resistances", {}),
		"mesh_set_key": str(rec.get("archetype_tag", "")),
		"skills": rec.get("skills", []),
	}


# ---------------------------------------------------------------------------
# INSTANTIATE GEAR — GearRecord (null name/flavor accepted, Q3).
# ---------------------------------------------------------------------------
func instantiate_gear(rec: Dictionary) -> Dictionary:
	return {
		"id": str(rec.get("id", "")),
		"name": _name_or_fallback(rec, "%s %s" % [rec.get("rarity", "common"), rec.get("gear_slot", "item")]),
		"flavor_text": rec.get("flavor_text", null),
		"gear_slot": str(rec.get("gear_slot", "")),
		"rarity": str(rec.get("rarity", "")),
		"is_unique": bool(rec.get("is_unique", false)),
		"set_bonus": rec.get("set_bonus", null),
	}


# ---------------------------------------------------------------------------
# FLOOR MANIFEST — per-floor element rotation (handshake Q5: 4 floor_ids).
# ---------------------------------------------------------------------------
func get_floor_sequence() -> Array:
	var seq: Variant = floor_manifest.get("floor_sequence", [])
	return seq if typeof(seq) == TYPE_ARRAY else []


func dominant_element_for_floor(floor_id: String) -> String:
	for fe in get_floor_sequence():
		if typeof(fe) == TYPE_DICTIONARY and str(fe.get("floor_id", "")) == floor_id:
			return str(fe.get("dominant_element", ""))
	return ""


# ---------------------------------------------------------------------------
# FACTION RESTYLE — III.7 INVARIANT: presentation restyle ONLY.
# This pass builds a kit_id -> {visual/motif/label} overlay. It has NO write path
# to any fight-model field. If a faction field's NAME collides with a fight-model
# field, that is an III.7 violation and we refuse it (surface, don't apply).
# ---------------------------------------------------------------------------
func build_faction_restyle_map() -> Dictionary:
	var restyle := {}
	if factions.is_empty():
		return restyle
	var provisional := factions.has("provisional")
	var clusters: Variant = factions.get("clusters", [])
	if typeof(clusters) != TYPE_ARRAY:
		return restyle
	for c in clusters:
		if typeof(c) != TYPE_DICTIONARY:
			continue
		# III.7 GUARD: refuse any faction key that collides with a fight-model field.
		for k in c.keys():
			if FIGHT_MODEL_FIELDS.has(k):
				errors.append("III.7 VIOLATION: faction cluster '%s' carries fight-model field '%s' — factions restyle ONLY. Surfaced to star-lord." % [c.get("cluster_id", "?"), k])
		var members: Variant = c.get("member_kit_ids", [])
		if typeof(members) != TYPE_ARRAY:
			continue
		for kit_id in members:
			restyle[str(kit_id)] = {
				"faction_name": str(c.get("name", "")),
				"faction_motif": c.get("faction_motif", null),
				"visual_identity": c.get("visual_identity", null),
				"provisional": provisional or bool(c.get("provisional", false)),  # preview-only restyle if provisional
			}
	return restyle


# Apply a restyle overlay to a kit — recolor/relabel ONLY. Explicitly refuses to
# touch stat_distribution / skills / resistances (III.7 architectural isolation).
func apply_faction_restyle(kit: Dictionary, restyle_map: Dictionary) -> Dictionary:
	var kid := str(kit.get("id", ""))
	if restyle_map.has(kid):
		var overlay: Dictionary = restyle_map[kid]
		kit["_restyle"] = overlay   # presentation overlay only; no mechanical mutation
	return kit


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
func _name_or_fallback(rec: Dictionary, fallback: String) -> String:
	var nm: Variant = rec.get("name", null)
	if nm != null and str(nm).length() > 0:
		return str(nm)
	return fallback
