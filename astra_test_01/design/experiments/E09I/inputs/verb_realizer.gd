extends RefCounted
class_name VerbRealizer
# ============================================================================
# verb_realizer.gd — ONE REALM VERB REALIZATION (D5).
#
# The §20d HEART: takes a D4-loaded kit (engine-emitted, ZERO hand-built content)
# and derives a DISTINCT PLAYABLE GODOT VERB from its engine fields. The question
# this file exists to answer empirically: can ~10 kits become ~10 distinguishable
# verbs cheaply? If the bundle's own primitive vocabulary collapses many kits into
# few distinguishable verbs, THAT is the §20d cost datapoint (one-realm §8).
#
# ARCHITECTURAL STANCE (§20d / engine-is-the-product):
#   - The verb SPEC is 100% DERIVED from engine fields (geometry / range_m /
#     effect_category / dominant_element / composition_mode). NOTHING here invents
#     game content. This is a pure PROJECTION of loaded data onto a render/feel
#     vocabulary — a lookup, not a design.
#   - The projection tables (geometry->shape, element->palette) are the ONLY
#     Godot-side authored artifact, and they are PRESENTATION vocabulary, not
#     content. Adding a kit costs ZERO new code IFF its (geometry, range, element)
#     tuple is already in the tables. A kit whose tuple is NEW costs one table row.
#     => the §20d per-verb marginal cost = "one row iff a novel primitive tuple".
#
# DISTINCTNESS is measured on the VERB SIGNATURE, defined below. Two kits that map
# to the same signature are NOT distinguishable verbs — the demo would show them as
# the same verb. The realizer reports the distinct-signature count so §20d is
# answered with a number, not a vibe.
#
# The SUMMON verb (the net-new class the summoner mandate §3 adds) is realized by
# summon_verb.gd, which THIS realizer routes to when a kit carries proxies.
#
# drax, 2026-07-02 (D5). Consumes bundle_loader.gd output; no engine change.
# ============================================================================

# --- PROJECTION TABLE 1: primary-attack GEOMETRY -> Godot verb SHAPE ----------
# The engine emits a small geometry vocabulary at the primary-attack layer
# (single_target / large_aoe on the demo bundle; the fuller palette adds cone /
# beam / chain / nova). Each maps to a distinct on-screen SHAPE + hit resolution.
# This is the load-bearing distinctness lever (a single-target bolt vs an AoE
# nova READ differently at a glance). New geometry = one new row.
const GEOMETRY_SHAPE := {
	"single_target": {"shape": "bolt", "hit": "point", "telegraph": "line"},
	"large_aoe":     {"shape": "nova", "hit": "radius", "telegraph": "ring"},
	"cone":          {"shape": "cone", "hit": "wedge", "telegraph": "wedge"},
	"beam":          {"shape": "beam", "hit": "line", "telegraph": "line"},
	"chain":         {"shape": "chain", "hit": "chain", "telegraph": "arc"},
	"nova":          {"shape": "nova", "hit": "radius", "telegraph": "ring"},
	# proxy geometries (summon strikes) — realized by summon_verb.gd, listed for parity
	"melee_strike":  {"shape": "melee_arc", "hit": "arc", "telegraph": "none"},
	"ground_slam":   {"shape": "slam", "hit": "radius", "telegraph": "ring"},
}

# --- PROJECTION TABLE 2: dominant_element -> PALETTE / VFX register key --------
# Element keys the register-2 juice (GPUParticles3D color ramp + light color).
# This is where the A-lock lives (fold D5-a): the element read is carried by
# PARTICLE + LIGHT, not mesh fidelity. New element = one new row.
const ELEMENT_PALETTE := {
	"fire":     {"core": Color(1.0, 0.55, 0.12), "glow": Color(1.0, 0.30, 0.05), "light": Color(1.0, 0.5, 0.2)},
	"earth":    {"core": Color(0.55, 0.42, 0.25), "glow": Color(0.35, 0.28, 0.15), "light": Color(0.6, 0.5, 0.35)},
	"water":    {"core": Color(0.25, 0.55, 0.95), "glow": Color(0.10, 0.35, 0.75), "light": Color(0.3, 0.6, 1.0)},
	"wind":     {"core": Color(0.70, 0.95, 0.80), "glow": Color(0.45, 0.75, 0.60), "light": Color(0.7, 1.0, 0.85)},
	"physical": {"core": Color(0.85, 0.85, 0.88), "glow": Color(0.55, 0.55, 0.60), "light": Color(0.9, 0.9, 0.95)},
	"dark":     {"core": Color(0.45, 0.20, 0.55), "glow": Color(0.25, 0.08, 0.35), "light": Color(0.5, 0.25, 0.6)},
}

# --- RANGE PROFILE -> cast-feel band (windup + projectile speed feel) ----------
# melee = short windup, instant reach; mid = medium; ranged = travel-time bolt.
# This is a FEEL modifier on the verb, distinct enough that a melee single_target
# and a ranged single_target read as different verbs (lunge vs bolt).
const RANGE_FEEL := {
	"melee":  {"windup_s": 0.12, "reach_m": 2.2, "travel": "instant"},
	"mid":    {"windup_s": 0.22, "reach_m": 9.0, "travel": "fast_bolt"},
	"ranged": {"windup_s": 0.30, "reach_m": 18.0, "travel": "bolt"},
}

# --- EFFECT CATEGORY -> secondary verb intent (does it damage / control / support)
const EFFECT_INTENT := {
	"single_target_damage": "strike",
	"aoe_damage":           "blast",
	"control":              "bind",
	"support":              "bolster",
}


# ---------------------------------------------------------------------------
# REALIZE — derive a verb spec from a D4-loaded kit dict. Pure projection.
# Returns a verb spec dict; if the kit carries proxies, spec.summon points to a
# SummonVerb spec (the net-new verb class).
# ---------------------------------------------------------------------------
func realize(kit: Dictionary) -> Dictionary:
	var primary: Dictionary = kit.get("primary_attack", {})
	var geo := str(primary.get("geometry", ""))
	var elem := str(kit.get("theme_element_key", kit.get("dominant_element", "")))
	var rng := str(kit.get("range_profile", ""))
	var eff := str(primary.get("effect_category", ""))
	var comp := str(primary.get("composition_mode", "single"))

	var shape: Dictionary = GEOMETRY_SHAPE.get(geo, {"shape": "unknown", "hit": "point", "telegraph": "none"})
	var palette: Dictionary = ELEMENT_PALETTE.get(elem, {"core": Color(1,1,1), "glow": Color(0.6,0.6,0.6), "light": Color(1,1,1)})
	var feel: Dictionary = RANGE_FEEL.get(rng, {"windup_s": 0.2, "reach_m": 8.0, "travel": "bolt"})
	var intent := str(EFFECT_INTENT.get(eff, "strike"))

	var verb := {
		"kit_id": str(kit.get("id", "")),
		"kit_name": str(kit.get("name", "")),
		"archetype_tag": str(kit.get("archetype_tag", "")),
		"playable": bool(kit.get("playable", false)),
		# --- the derived VERB (all fields projected from engine data) ---
		"verb_shape": shape["shape"],
		"hit_model": shape["hit"],
		"telegraph": shape["telegraph"],
		"element_key": elem,
		"palette": palette,
		"range_band": rng,
		"windup_s": feel["windup_s"],
		"reach_m": feel["reach_m"],
		"travel": feel["travel"],
		"intent": intent,
		"composition_mode": comp,
		"is_summoner": bool(kit.get("is_summoner", false)),
	}
	# the VERB SIGNATURE — the distinctness key (§20d measurement). Two kits with
	# an equal signature are NOT distinguishable verbs on-screen.
	verb["signature"] = _verb_signature(verb)
	return verb


# The distinctness key. A verb is distinguishable by what a player SEES + FEELS:
# its shape (bolt vs nova vs melee_arc), its element palette, its range band, its
# intent (strike/blast/bind/bolster), and whether it summons. This is deliberately
# the PERCEPTUAL signature, not the kit id — the whole §20d question is whether the
# ENGINE's own variety produces perceptually-distinct verbs.
func _verb_signature(verb: Dictionary) -> String:
	return "%s|%s|%s|%s|%s" % [
		verb["verb_shape"],
		verb["element_key"],
		verb["range_band"],
		verb["intent"],
		"summon" if verb["is_summoner"] else "cast",
	]


# ---------------------------------------------------------------------------
# REALIZE ALL + REPORT DISTINCTNESS — the §20d datapoint generator.
# Takes the full loaded kit list, realizes each, and reports:
#   - how many distinct verb SIGNATURES emerge (the distinguishable-verb count)
#   - the collapse ratio (kits / distinct verbs)
#   - which primitive tuples are novel (drive the per-verb marginal cost)
# ---------------------------------------------------------------------------
func distinctness_report(kits: Array) -> Dictionary:
	var verbs: Array = []
	var sig_counts := {}
	var elements := {}
	var shapes := {}
	var summoner_sigs := {}
	for k in kits:
		if typeof(k) != TYPE_DICTIONARY:
			continue
		var v := realize(k)
		verbs.append(v)
		var sig := str(v["signature"])
		sig_counts[sig] = int(sig_counts.get(sig, 0)) + 1
		elements[str(v["element_key"])] = true
		shapes[str(v["verb_shape"])] = true
		if bool(v["is_summoner"]):
			summoner_sigs[sig] = true
	var n_kits := verbs.size()
	var n_distinct := sig_counts.size()
	return {
		"n_kits": n_kits,
		"n_distinct_verbs": n_distinct,
		"collapse_ratio": (float(n_kits) / float(n_distinct)) if n_distinct > 0 else 0.0,
		"distinct_elements": elements.keys().size(),
		"distinct_shapes": shapes.keys().size(),
		"distinct_summon_verbs": summoner_sigs.size(),
		"signature_histogram": sig_counts,
		"verbs": verbs,
	}
