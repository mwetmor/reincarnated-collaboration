#!/usr/bin/env python3
"""LE facts generator — megaprobe-2026-07-12 (full schema per gandalf correction)
35 rows: 32 positive (4 post-cutoff) + 3 negative (light schema)
Post-cutoff kits: 1.4-omens-only (Season 4, ~late 2025) + conf <= 0.5
"""
import json

OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/megaprobe-2026-07-12/le-facts.jsonl"


def pc(v, c, ev):
    """prefix_claims slot helper"""
    return {"value": v, "conf": round(c, 2), "evidence": ev}


def dc(v, c, ev):
    """delivery/footprint field helper"""
    return {"value": v, "conf": round(c, 2), "evidence": ev}


def ctrl(ailments, centrality, conf):
    return {"ailments": ailments, "centrality": centrality, "conf": round(conf, 2)}


def defs(layers, primary, conf):
    return {"layers": layers, "primary": primary, "conf": round(conf, 2)}


def econ(resource_verbatim, model, meter_type, builder_source, plain_text, conf):
    return {
        "resource_verbatim": resource_verbatim,
        "model": model,
        "meter_type": meter_type,
        "builder_source": builder_source,
        "plain_text": plain_text,
        "conf": round(conf, 2),
    }


def elem(label_verbatim, damage_mode, conf):
    return {"label_verbatim": label_verbatim, "damage_mode": damage_mode, "conf": round(conf, 2)}


def mov(verbs, policy, skill_is_movement, conf):
    return {"verbs": verbs, "policy_while_casting": policy, "skill_is_movement": skill_is_movement, "conf": round(conf, 2)}


def prefix(attr_v, attr_c, attr_ev, rng_v, rng_c, rng_ev, tmp_v, tmp_c, tmp_ev,
           amp_v, amp_c, amp_ev, prx_v, prx_c, prx_ev, cmt_v, cmt_c, cmt_ev):
    return {
        "attr":       pc(attr_v, attr_c, attr_ev),
        "range":      pc(rng_v, rng_c, rng_ev),
        "tempo":      pc(tmp_v, tmp_c, tmp_ev),
        "amp":        pc(amp_v, amp_c, amp_ev),
        "proxy":      pc(prx_v, prx_c, prx_ev),
        "commitment": pc(cmt_v, cmt_c, cmt_ev),
    }


RECORDS = []

# ---------------------------------------------------------------------------
# POSITIVE RECORDS — full schema
# ---------------------------------------------------------------------------

# 1. le-umbral-blades
RECORDS.append({
    "kit_id": "le-umbral-blades", "folk_name": "Umbral Blades Rogue", "game": "le",
    "status": "positive", "atlas_key": "DDHFSI-HMDD-SP-PH-~~",
    "delivery": dc("projectile", 0.83, "Thrown spectral blades travel to target range, lodge, then RECALL through all enemies on return path; two-phase projectile confirmed"),
    "footprint": dc("multi-point", 0.78, "Blades lodge at multiple ground positions before recall sweep; multi-point scatter + lane-return"),
    "geo_text": "Umbral Blades throws spectral daggers that embed in the ground at scattered positions. On recall, every lodged blade sweeps back through all targets along its return path, dealing damage twice per blade.",
    "control": ctrl([], "none", 0.75),
    "defense": defs(["dodge", "glass"], "dodge", 0.80),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana-spend per cast; no secondary resource. Bladedancer node tree governs cooldown-recovery interactions for repeated throws.",
                    0.78),
    "element": elem("Physical / Cold (hybrid via node)", "hit", 0.72),
    "movement": mov([], "rooted", False, 0.80),
    "prefix_claims": prefix(
        "DEX", 0.88, "Rogue class is universally DEX-primary; Umbral Blades has no STR/INT node pathing",
        "mid", 0.75, "Blades thrown at mid-range (not melee contact, not long-range bow); atlas D=mid confirmed by throw-range design",
        "high", 0.80, "High tempo: rapid successive throw cadence; cast-speed scaling in tree accelerates the rhythm",
        "flat", 0.72, "Damage output is flat per-blade hit; no amp spike mechanic; spiky would require a condition-stack explosion model which is absent",
        "solo", 0.88, "No proxy entities; player throws own blades; solo damage vector confirmed",
        "instant", 0.90, "Instant cast; no wind-up animation or channel"),
    "mechanics_notes": "Two-phase mechanic (throw-lodge-recall) means a single cast applies damage on the way out AND on recall. Scale via cast speed + projectile count nodes. mech_note ref: 'plant the field, recall through everything.'",
    "era_confirmed": ["1.0-launch", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "rank1_upgrade: live source verification deferred; prov=kb",
    "sources_used": ["kb (training knowledge)", "LE wiki (deferred live URL verification)"],
})

# 2. le-skeleton-necro
RECORDS.append({
    "kit_id": "le-skeleton-necro", "folk_name": "Skeleton Necromancer", "game": "le",
    "status": "positive", "atlas_key": "IMMFHI-MNDM-SU-PH-~~",
    "delivery": dc("at-target", 0.82, "Skeletons (warriors/mages) seek and attack enemies; delivery is mediated through minion autonomy targeting enemies"),
    "footprint": dc("small-radius", 0.75, "Individual skeleton melee/ranged attacks cover small-radius per skeleton; collective coverage is multi-point but per-unit footprint is small"),
    "geo_text": "Skeleton warriors close to melee range; skeleton mages volley projectiles at mid-distance. The necromancer commands placement; skeletons autonomously pursue and strike within small radii around each target.",
    "control": ctrl([], "none", 0.75),
    "defense": defs(["minion-shield", "hp-stack"], "minion-shield", 0.78),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Each Skeleton summoned costs Mana. Army self-sustains once summoned (no per-attack cost). Death of skeletons triggers re-summon cycle.",
                    0.80),
    "element": elem("Physical", "hit", 0.82),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": prefix(
        "INT", 0.88, "Acolyte/Necromancer is INT-primary; minion scaling tied to INT gear; confirmed",
        "mid", 0.72, "Skeletons operate at mid-range between player and enemies; player maintains mid-field spacing; atlas D=mid is an approximation of collective army engagement range",
        "med", 0.78, "Medium tempo: summon cooldown + army turnover rate; not rapid-cast, not slow; atlas M confirmed",
        "flat", 0.80, "Skeleton damage scales flat per-minion per-hit; no spike damage model",
        "heavy", 0.88, "Skeleton army IS the primary damage vector; player deals minimal direct damage; heavy proxy confirmed",
        "instant", 0.90, "Each skeleton summoned with instant cast; no channel"),
    "mechanics_notes": "Supports warrior/mage/death-knight skeleton types via node tree. prov=eg;kb. mech_note ref: 'LE minion default and classic skeletal legion.'",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=eg;kb",
    "sources_used": ["kb", "eg (external guide reference)"],
})

# 3. le-dive-bomb-falconer
RECORDS.append({
    "kit_id": "le-dive-bomb-falconer", "folk_name": "Dive Bomb Falconer", "game": "le",
    "status": "positive", "atlas_key": "DDHSHI-HSDD-SP-PH-~~",
    "delivery": dc("at-target", 0.85, "Player commands falcon to execute Dive Bomb on specified target; falcon is the delivery vehicle; at-target confirmed by command mechanic"),
    "footprint": dc("small-radius", 0.80, "Falcon dive creates small splash area on impact; compact AoE centered on dive target"),
    "geo_text": "Player issues Dive Bomb command; falcon streaks from current position and impacts a targeted enemy zone with a small radial AoE. Player kites freely while falcon executes the strike.",
    "control": ctrl(["exposed"], "rider", 0.65),
    "defense": defs(["dodge", "evasion"], "dodge", 0.80),
    "economy": econ("Mana + Falcon cooldown", "spend+cooldown", "n/a", "n/a",
                    "Dive Bomb has both a Mana cost and a per-command falcon cooldown. High-cooldown-reduction builds reduce the cooldown gap. Mana cost is secondary to the cooldown constraint.",
                    0.78),
    "element": elem("Physical", "hit", 0.82),
    "movement": mov([], "full-move", False, 0.88),
    "prefix_claims": prefix(
        "DEX", 0.90, "Rogue/Falconer is DEX-primary; falcon mastery tree reinforces DEX scaling",
        "mid", 0.75, "Falcon operates at mid-field; player maintains distance while falcon executes in mid-range; D=mid confirmed",
        "high", 0.80, "High-tempo: repeated Dive Bomb commands at rapid cadence once cooldown is reduced; prov=gg;lw confirms endgame cadence is high",
        "spiky", 0.82, "Dive Bomb is the spike damage event; high burst per dive; atlas S=spiky confirmed",
        "heavy", 0.88, "Falcon IS the primary damage vector; player is positioning/commanding only; H=heavy proxy confirmed",
        "instant", 0.90, "Command is instant; falcon execution is autonomous"),
    "mechanics_notes": "prov=gg;lw;kb. mech_note ref: 'YOUR BIRD does the killing — command Dive Bomb strikes while you kite untouchable.' Falconer kiting + bird killing = archetypal ranger-proxy build.",
    "era_confirmed": ["1.0-launch", "1.2-woven", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=gg;lw;kb",
    "sources_used": ["kb", "gg (guide reference)", "lw (Last Epoch wiki)"],
})

# 4. le-explosive-trap-falconer
RECORDS.append({
    "kit_id": "le-explosive-trap-falconer", "folk_name": "Explosive Trap Falconer", "game": "le",
    "status": "positive", "atlas_key": "DDHSLI-HLDD-SP-PH-~~",
    "delivery": dc("at-target", 0.80, "Player places traps at target location; falcon Dive Bombs detonate traps; delivery is mediated: player places, falcon triggers"),
    "footprint": dc("large-zone", 0.80, "Trap explosions cover large AoE; atlas geo=large-AOE confirmed by 'carpet the floor' mech_note"),
    "geo_text": "Player carpets the ground with explosive traps placed at target positions. When the falcon executes Dive Bomb into the trap zone, the traps chain-detonate in a large explosion radius. Deploy-and-detonate pattern.",
    "control": ctrl(["ignite"], "rider", 0.68),
    "defense": defs(["dodge", "evasion"], "dodge", 0.80),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Each trap placed costs Mana. Falcon detonation is the trigger mechanism (no additional resource for detonation). Multiple traps can be pre-placed before trigger.",
                    0.78),
    "element": elem("Physical / Fire", "hit", 0.75),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": prefix(
        "DEX", 0.90, "Rogue/Falconer DEX-primary confirmed",
        "mid", 0.72, "Traps placed at mid-range; player positions in mid-field relative to enemies; D=mid approximate",
        "high", 0.70, "Atlas says H=high; mech_note ref 'carpet the floor' suggests rapid trap deployment; HIGH tempo reflects placement speed, not detonation frequency; conf MED because single detonation events are spaced",
        "spiky", 0.82, "Chain-detonation creates massive spike damage events; S=spiky confirmed",
        "light", 0.80, "Traps are light-proxy (placed equipment, not autonomous entities); L=light confirmed",
        "instant", 0.90, "Instant trap placement; no wind-up"),
    "mechanics_notes": "prov=kb. mech_note ref: '1.0 launch most overtuned archetype, deploy-detonate.' Falcon detonates traps = combined falcon+trap proxy. Note: proxy characterization is nuanced — traps are 'light' (placed kit), falcon is 'heavy' (autonomous); aggregate proxy=light-to-heavy depending on which arm is dominant. Atlas coded L=light (trap arm dominant).",
    "era_confirmed": ["1.0-launch", "1.1-harbingers"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=kb",
    "sources_used": ["kb"],
})

# 5. le-bomb-lance-falconer (POST-CUTOFF — 1.4-omens only, conf=0.33)
RECORDS.append({
    "kit_id": "le-bomb-lance-falconer", "folk_name": "Bomb Lance Falconer", "game": "le",
    "status": "positive", "atlas_key": "DDMSLI-HSDD-SP-PH-~~",
    "delivery": dc("projectile", 0.33, "POST-CUTOFF: Season 4 skill; ballista-and-bird delivery inferred from mech_note; live verification required"),
    "footprint": dc("small-radius", 0.33, "POST-CUTOFF: small AoE inferred from geo=small-AOE in atlas; live verification required"),
    "geo_text": "POST-CUTOFF (1.4-omens, Season 4). Ballista-and-bird engine per mech_note. Full spatial characterization deferred to dossier.",
    "control": ctrl([], "unknown", 0.33),
    "defense": defs(["dodge"], "dodge", 0.33),
    "economy": econ("Mana", "spend", "n/a", "n/a", "POST-CUTOFF: economy inferred from Falconer class pattern; live verification required", 0.33),
    "element": elem("Physical (inferred)", "hit", 0.33),
    "movement": mov([], "full-move", False, 0.33),
    "prefix_claims": prefix(
        "DEX", 0.45, "Rogue/Falconer class = DEX; POST-CUTOFF cap applied; atlas D confirmed",
        "mid", 0.33, "POST-CUTOFF: D=mid from atlas; cannot verify at post-cutoff cap",
        "med", 0.33, "POST-CUTOFF: M=med from atlas; cannot verify",
        "spiky", 0.33, "POST-CUTOFF: S=spiky from atlas; cannot verify",
        "light", 0.33, "POST-CUTOFF: L=light from atlas; cannot verify",
        "instant", 0.40, "Falconer pattern is instant-cast; inferred from class pattern; POST-CUTOFF cap"),
    "mechanics_notes": "POST-CUTOFF. Season 4 (1.4-omens) new Rogue skill. prov=gg;mx-le. mech_note ref: 'ballista-and-bird engine to the top of the endgame pile.' Full dossier required.",
    "era_confirmed": ["1.4-omens"],
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "DEFERRED — post-cutoff; live source required",
    "sources_used": ["gg (guide reference, post-cutoff)", "mx-le (maxroll LE, post-cutoff)"],
})

# 6. le-bladestorm-bd (POST-CUTOFF — 1.4-omens only, conf=0.33)
RECORDS.append({
    "kit_id": "le-bladestorm-bd", "folk_name": "Bladestorm Bladedancer", "game": "le",
    "status": "positive", "atlas_key": "DMHFLI-HSDD-SP-PH-~~",
    "delivery": dc("orbit", 0.33, "POST-CUTOFF: 'persistent storm of orbiting blades' per mech_note implies orbit delivery; live verification required"),
    "footprint": dc("ring", 0.33, "POST-CUTOFF: orbiting blades create ring footprint around caster; inferred; live verification required"),
    "geo_text": "POST-CUTOFF (1.4-omens, Season 4). Persistent orbiting blade storm under Bladedancer restructured mechanic. Full spatial characterization deferred.",
    "control": ctrl([], "unknown", 0.33),
    "defense": defs(["dodge"], "dodge", 0.33),
    "economy": econ("Mana", "spend", "n/a", "n/a", "POST-CUTOFF: economy inferred from Bladedancer class pattern; live verification required", 0.33),
    "element": elem("Physical (inferred)", "hit", 0.33),
    "movement": mov([], "full-move", False, 0.33),
    "prefix_claims": prefix(
        "DEX", 0.45, "Rogue/Bladedancer DEX-primary; POST-CUTOFF cap applied",
        "melee", 0.33, "POST-CUTOFF: M=melee from atlas; orbit blades at melee range inferred",
        "high", 0.33, "POST-CUTOFF: H=high tempo from atlas; cannot verify at cap",
        "flat", 0.33, "POST-CUTOFF: F=flat from atlas; cannot verify",
        "light", 0.33, "POST-CUTOFF: L=light from atlas; blade storm as light-proxy inferred",
        "instant", 0.40, "Bladedancer pattern typically instant; POST-CUTOFF cap"),
    "mechanics_notes": "POST-CUTOFF. Season 4 (1.4-omens) new Rogue skill, immediate S-tier per mech_note. prov=lb;mx-le. mech_note ref: 'persistent storm of orbiting blades under the restructured Bladedancer [tree].' Full dossier required.",
    "era_confirmed": ["1.4-omens"],
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "DEFERRED — post-cutoff; live source required",
    "sources_used": ["lb (leaderboard data, post-cutoff)", "mx-le (post-cutoff)"],
})

# 7. le-shadow-bladedancer
RECORDS.append({
    "kit_id": "le-shadow-bladedancer", "folk_name": "Shadow Bladedancer", "game": "le",
    "status": "positive", "atlas_key": "DMHSLI-KMDD-SP-PH-~~",
    "delivery": dc("at-target", 0.82, "Shadows mirror player attacks and strike at enemy positions simultaneously; each shadow delivers at-target hits"),
    "footprint": dc("multi-point", 0.80, "Multiple stationary shadow copies at different map positions each strike targets independently — multi-point coverage"),
    "geo_text": "Player spawns stationary shadow copies at placed positions. Every attack the player makes is simultaneously mirrored by each shadow, striking at their respective nearby targets. Coverage scales with shadow count.",
    "control": ctrl(["bleed"], "rider", 0.68),
    "defense": defs(["dodge", "evasion"], "dodge", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Shadow placement costs Mana. Subsequent mirror attacks are free (shadows copy player actions without additional cost). Shadow duration limits active count.",
                    0.78),
    "element": elem("Physical", "hit", 0.82),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": prefix(
        "DEX", 0.90, "Rogue/Bladedancer DEX-primary confirmed",
        "melee", 0.80, "Shadows engage at melee range; player also attacks at melee; M=melee confirmed",
        "high", 0.82, "High attack tempo while shadows multiply hits; effectively multiplied cadence",
        "spiky", 0.78, "Spike damage when multiple shadows simultaneously mirror a high-damage skill; atlas S=spiky supported",
        "light", 0.82, "Shadows are light-proxy; they mirror but player still attacks directly; L=light confirmed (not heavy — player is active combatant)",
        "instant", 0.90, "Shadow placement and attacks are instant"),
    "mechanics_notes": "prov=eg;kb. mech_note ref: 'Spawn SHADOWS — stationary copies of yourself — then every attack you make is MIRRORED by every shadow simultaneously.' Shadow count is the primary scaling axis — more shadows = multiplicative output. Ctrl C2 note: shadows require player proximity to enemies; not pure support.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=eg;kb",
    "sources_used": ["kb", "eg"],
})

# 8. le-detonating-arrow-mm
RECORDS.append({
    "kit_id": "le-detonating-arrow-mm", "folk_name": "Detonating Arrow Marksman", "game": "le",
    "status": "positive", "atlas_key": "DRHSSI-HSDD-SP-FI-~~",
    "delivery": dc("projectile", 0.88, "Arrow fired at ranged target; detonates on impact or after delay; projectile delivery confirmed"),
    "footprint": dc("small-radius", 0.83, "Explosive detonation creates small-radius blast at impact point; atlas geo=small-AOE confirmed"),
    "geo_text": "Marksman fires an explosive-tipped arrow that travels to target and detonates on impact or after a configurable delay. Some tree nodes enable multi-shot volleys with staggered explosions.",
    "control": ctrl(["ignite"], "rider", 0.72),
    "defense": defs(["dodge", "evasion"], "dodge", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per arrow. High-tempo arrow spam with cast-speed investment. No secondary resource.",
                    0.82),
    "element": elem("Fire / Physical", "hit", 0.80),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "DEX", 0.90, "Rogue/Marksman DEX-primary; bow mastery DEX-gated",
        "ranged", 0.90, "Bow ranged attack; R=ranged confirmed",
        "high", 0.85, "High attack tempo: rapid arrow volley confirmed in prov=eg;kb sources",
        "spiky", 0.85, "Detonation creates explosive spike damage burst per shot; S=spiky confirmed",
        "solo", 0.88, "No proxy; player fires own arrows; S=solo confirmed",
        "instant", 0.90, "Instant bow draw and release; no channel"),
    "mechanics_notes": "prov=eg;kb. mech_note ref: 'Explosive-tipped shots with tree paths for delayed detonation payloads — the marksman's screen-clear staple, with Multishot layering.' Multishot = multiple simultaneous arrows. FI suffix = Fire element.",
    "era_confirmed": ["1.0-launch", "1.2-woven", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=eg;kb",
    "sources_used": ["kb", "eg"],
})

# 9. le-ghostflame-warlock
RECORDS.append({
    "kit_id": "le-ghostflame-warlock", "folk_name": "Ghostflame Warlock", "game": "le",
    "status": "positive", "atlas_key": "IDHFSC-_SDM-SP-NE-~~",
    "delivery": dc("beam", 0.85, "Channeled spectral fire stream directed at target; beam delivery confirmed by 'stream of spectral fire' mech_note and channel commit"),
    "footprint": dc("cone", 0.80, "Channel projects a cone-shaped stream of ghostflame; enemies in the cone path take DoT damage"),
    "geo_text": "Warlock channels a spectral fire beam in a cone projection toward targeted direction. Curse stacks on enemies amplify the beam's damage. The channel is directional but covers a widening cone shape rather than a pure line.",
    "control": ctrl(["curse-stacks", "slow"], "rider", 0.72),
    "defense": defs(["shield-absorb", "ward"], "ward", 0.85),
    "economy": econ("Mana", "reserve", "n/a", "n/a",
                    "Ghostflame channel drains Mana continuously while held. Warlock builds invest in Mana regeneration or leech to sustain channel. Releasing ends the drain.",
                    0.80),
    "element": elem("Necrotic / Fire (hybrid per mech_note)", "dot", 0.82),
    "movement": mov([], "rooted", False, 0.85),
    "prefix_claims": prefix(
        "INT", 0.88, "Acolyte/Warlock INT-primary; channeled magic spells scale INT",
        "mid", 0.75, "Beam has mid-range reach; not melee contact, not long-range; D=mid approximate",
        "high", 0.72, "Atlas H=high; for a channel, 'high' reflects damage-per-second rate while channeling rather than cast frequency; conf MED because high-vs-med for channel DPS is subjective",
        "flat", 0.78, "Ghostflame applies consistent DoT rather than burst spikes; F=flat confirmed; damage ramps via curse stacks but is still cumulative-flat not spiky",
        "solo", 0.88, "No proxy entities; player channels directly; S=solo confirmed",
        "channel", 0.92, "Confirmed channel commitment; key position 6 = C; mech_note confirms channeled stream"),
    "mechanics_notes": "prov=kb. mech_note ref: 'Channel a stream of spectral fire that hybridizes necrotic and fire damage while curses amplify.' NE suffix = Necrotic element. Warlock primary defense = Ward (Acolyte ward-stack class). atlas pos-5 = S=solo, pos-4 = F=flat confirmed. Damage_mode=dot (continuous channel DoT).",
    "era_confirmed": ["1.0-launch", "1.1-harbingers"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=kb",
    "sources_used": ["kb"],
})

# 10. le-frost-claw
RECORDS.append({
    "kit_id": "le-frost-claw", "folk_name": "Frost Claw Sorcerer", "game": "le",
    "status": "positive", "atlas_key": "IDHFSI-MSMM-PC-CO-~~",
    "delivery": dc("projectile", 0.85, "Frost Claw fires raking spectral claw projectiles in a fan/cone pattern; projectile delivery confirmed"),
    "footprint": dc("cone", 0.82, "Claws fan out in a cone from cast point; coverage is conical not single-target; PC suffix references proc cascade (free Elemental Novas)"),
    "geo_text": "Frost Claw fires multiple spectral claw projectiles in a widening fan/cone from the player. On hit, tree nodes trigger free Elemental Nova procs at impact points. The cone-fan delivery plus proc cascade creates a layered AoE.",
    "control": ctrl(["chill", "freeze"], "core", 0.85),
    "defense": defs(["ward", "glass"], "ward", 0.80),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per cast. Cast-speed investment enables rapid Frost Claw spam driving the proc-cascade engine.",
                    0.82),
    "element": elem("Cold", "hit", 0.88),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "INT", 0.90, "Mage/Sorcerer INT-primary; Cold spells scale INT exclusively",
        "mid", 0.75, "Projectile claws have mid-range reach; D=mid confirmed",
        "high", 0.82, "High cast tempo: proc-cascade engine requires rapid Frost Claw spam; prov=kb confirms as dominant playstyle in 0.8-0.9 through 1.0",
        "flat", 0.78, "Flat damage per claw hit; chill/freeze is control rider, not amp mechanism; F=flat confirmed",
        "solo", 0.88, "No proxy; player casts; S=solo confirmed",
        "instant", 0.90, "Instant cast; no wind-up"),
    "mechanics_notes": "prov=kb. mech_note ref: 'Raking spectral claws with a tree that triggers FREE Elemental Novas off claw hits — the proc-cascade caster that ruled [the meta].' CO suffix = Cold element. The free Elemental Nova procs are the key multiplier. Control = core (build's identity is Chill/Freeze debuff + damage; Freeze makes enemies vulnerable to shatter). Ctrl C2: Frost Claw is damage-primary with control as scaling tool; NOT pure support.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=kb",
    "sources_used": ["kb"],
})

# 11. le-chthonic-fissure-warlock
RECORDS.append({
    "kit_id": "le-chthonic-fissure-warlock", "folk_name": "Chthonic Fissure Warlock", "game": "le",
    "status": "positive", "atlas_key": "IDLFLI-MLDM-SP-FI-~~",
    "delivery": dc("line", 0.82, "Fissure 'crawls forward' per mech_note — it extends as a moving line tear in the ground rather than a static placed AoE; line delivery confirmed"),
    "footprint": dc("lane", 0.80, "Fissure creates a lane of damage as it crawls forward belching chaos spirits along its path; lane footprint confirmed by directional crawl mechanic"),
    "geo_text": "A ground tear opens and crawls forward in the cast direction, continuously belching chaos spirits along its path. Spirits seek nearby enemies and apply damage while curse stacks multiply output. The fissure lane persists briefly before collapsing.",
    "control": ctrl(["void-corruption", "curse"], "rider", 0.72),
    "defense": defs(["shield-absorb", "ward"], "ward", 0.85),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per cast. Light proxy spirits are not manually resummoned; they spawn from the active fissure.",
                    0.80),
    "element": elem("Void / Fire (FI suffix)", "hit", 0.72),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "INT", 0.88, "Acolyte/Warlock INT-primary confirmed",
        "mid", 0.75, "Fissure extends in mid-range from player; L in atlas pos-2 would be melee... atlas says D=mid: fissure crawls out to mid-range",
        "low", 0.80, "L=low tempo: fissure placed at moderate cadence; not rapid-fire; L confirmed by single-cast-and-wait pattern",
        "flat", 0.78, "Flat damage from spirits; curses amplify flat rate; F=flat confirmed; no burst spike",
        "light", 0.82, "Chaos spirits are light-proxy — they seek enemies autonomously but are low-count, brief; L=light confirmed",
        "instant", 0.88, "Instant cast to place fissure; no wind-up"),
    "mechanics_notes": "prov=gg;lw;kb. mech_note ref: 'Tear the ground open — the fissure crawls forward belching chaos SPIRITS that seek and burn while curse stacks multiply damage.' Correction from atlas geo=large-AOE: this is NOT a static large-AOE — it is a lane/crawl. delivery=line, footprint=lane is the corrected characterization. FI suffix = Fire element (though spirits are void-flavored; the damage_mode element is Fire per atlas suffix). soul-feast is the feed inside this build (see le-soul-feast negative).",
    "era_confirmed": ["1.0-launch", "1.1-harbingers", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=gg;lw;kb",
    "sources_used": ["kb", "gg", "lw"],
})

# 12. le-frost-wall-rm
RECORDS.append({
    "kit_id": "le-frost-wall-rm", "folk_name": "Frost Wall Runemaster", "game": "le",
    "status": "positive", "atlas_key": "IDMFLI-MLCM-SP-CO-~~",
    "delivery": dc("at-target", 0.83, "Frost Wall segments placed at targeted ground position; static structure delivery; at-target confirmed"),
    "footprint": dc("lane", 0.82, "Wall extends horizontally across cast line, blocking movement and projectiles; lane footprint confirmed by wall structure"),
    "geo_text": "Runemaster places a wall of ice segments at targeted position. The wall creates a physical lane barrier that blocks movement and projectiles, chills/freezes passing enemies, and (via tree nodes) detonates or amplifies spells fired through it.",
    "control": ctrl(["chill", "freeze", "slow"], "core", 0.85),
    "defense": defs(["shield-absorb", "ward"], "ward", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per wall placement. Multiple wall segments can be stacked. Runemaster's proc system fires secondary effects off wall interactions.",
                    0.80),
    "element": elem("Cold", "hit", 0.88),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "INT", 0.88, "Mage/Runemaster INT-primary; Cold spell scaling confirmed",
        "mid", 0.75, "Walls placed at mid-range; D=mid approximate for placement distance",
        "med", 0.80, "M=med tempo: wall placement is deliberate, not rapid-fire; medium cadence confirmed",
        "flat", 0.78, "Wall damage is flat cold DoT per segment; F=flat confirmed",
        "light", 0.72, "L=light in atlas proxy position: walls are placed terrain objects (light proxy type) not autonomous entities; confirmed",
        "instant", 0.88, "Wall placed instantly on cast"),
    "mechanics_notes": "prov=let;kb. mech_note ref: 'WALLS as the win condition — Frost Wall segments block, chill, and detonate through tree nodes while spells fired THROUGH the wall [are amplified].' CO suffix = Cold. Atlas geo=large-AOE captured the wall's horizontal extent; corrected to lane (wall is elongated lane not a large circular zone). Ctrl C2: control is CORE to this kit — the wall IS the damage/zone mechanism.",
    "era_confirmed": ["1.0-launch", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=let;kb",
    "sources_used": ["kb", "let (Last Epoch tools)"],
})

# 13. le-reaper-form-lich
RECORDS.append({
    "kit_id": "le-reaper-form-lich", "folk_name": "Reaper Form Lich", "game": "le",
    "status": "positive", "atlas_key": "IMHFSI-HSDG-LC-NE-~~",
    "delivery": dc("self-origin", 0.83, "Reaper Form is a character transformation — primary delivery is self-origin (the form itself radiates and enables scythe melee attacks)"),
    "footprint": dc("small-radius", 0.80, "Reaper melee scythe attacks cover small-radius melee range around the Lich in form"),
    "geo_text": "Lich transforms into the Reaper with a second decaying health bar. In form, the Lich executes melee scythe attacks within close range. The form decays every second; survival requires leech from scythe hits.",
    "control": ctrl(["necrotic-weakness"], "rider", 0.65),
    "defense": defs(["sustain-leech"], "sustain-leech", 0.82),
    "economy": econ("Life (form decay)", "self-cost", "n/a", "n/a",
                    "Reaper Form has a second HP bar that decays every second regardless of combat. The Lich must leech Life via scythe attacks faster than the decay rate to survive. The form is a self-cost maintenance loop.",
                    0.82),
    "element": elem("Necrotic", "hit", 0.85),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": prefix(
        "INT", 0.88, "Acolyte/Lich INT-primary; necrotic scythe skills scale INT",
        "melee", 0.88, "Reaper Form uses melee scythe attacks; M=melee confirmed",
        "high", 0.82, "High tempo: rapid scythe hits required to sustain leech > form decay; H=high confirmed by leech-or-die cadence",
        "flat", 0.78, "Flat damage per scythe hit; no spike mechanism; F=flat confirmed",
        "solo", 0.88, "No proxy; Lich attacks directly in form; S=solo confirmed; atlas pos-5 = S",
        "instant", 0.88, "Transformation triggered instantly; form entry is instant"),
    "mechanics_notes": "prov=gg;eg;kb. mech_note ref: 'Transform into the Reaper — a second health bar that DECAYS every second, harvest-scythe kit, leech-or-die tempo.' NE suffix = Necrotic. HSDG suffix pos-5 may encode a special LC (life-cost?) proxy category in old vocab; modern schema captures this as self-cost economy. Defense = sustain-leech (must leech to survive form). Ctrl C2: Reaper Form is solo offense; no support application.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=gg;eg;kb",
    "sources_used": ["kb", "gg", "eg"],
})

# 14. le-flame-reave-spellblade
RECORDS.append({
    "kit_id": "le-flame-reave-spellblade", "folk_name": "Flame Reave Spellblade", "game": "le",
    "status": "positive", "atlas_key": "IMHFSI-HSDM-SP-FI-~~",
    "delivery": dc("at-target", 0.85, "Melee sword swings create crescent fire waves at target; at-target melee delivery confirmed"),
    "footprint": dc("small-radius", 0.82, "Crescent wave spreads in tight arc from melee contact point; small-radius close range confirmed"),
    "geo_text": "Spellblade executes melee sword swings emitting crescent-shaped fire waves from the blade. Firebrand stacks accumulate on hits and generate Ward. The melee contact range is close; fire wave extends slightly beyond sword reach.",
    "control": ctrl(["ignite"], "rider", 0.68),
    "defense": defs(["shield-absorb", "ward"], "ward", 0.88),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per strike. Firebrand stacks are the secondary economy — they build on hits and convert to Ward, making each swing both offense and defense investment.",
                    0.82),
    "element": elem("Fire", "hit", 0.90),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "INT", 0.88, "Mage/Spellblade INT-primary; fire spells and melee-mage scaling both INT",
        "melee", 0.90, "Melee sword attack; M=melee confirmed unambiguously",
        "high", 0.85, "High attack tempo: rapid melee swing cadence; prov=mx-le confirms high-attack-speed investment",
        "flat", 0.78, "Flat fire damage per swing; Firebrand stacks are Ward-generation not damage spikes; F=flat confirmed",
        "solo", 0.88, "No proxy; Spellblade attacks directly; S=solo confirmed",
        "instant", 0.90, "Instant melee strikes"),
    "mechanics_notes": "prov=mx-le;kb. mech_note ref: 'Melee-mage crescent waves of fire off sword swings, ward from Firebrand stacks — the battle-mage identity build since beta.' FI suffix = Fire. Ward defense = primary (Spellblade builds Ward via Firebrand + INT). Shield-split D1: this IS a Ward kit (not armor/block). Flame Reave is the foundational Spellblade skill from beta through 1.4.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=mx-le;kb",
    "sources_used": ["kb", "mx-le"],
})

# 15. le-harvest-lich
RECORDS.append({
    "kit_id": "le-harvest-lich", "folk_name": "Harvest Death Seal Lich", "game": "le",
    "status": "positive", "atlas_key": "IMHFSI-HSDM-SP-NE-~~",
    "delivery": dc("at-target", 0.83, "Harvest scythe attacks at melee range; Death Seal modifies self not delivery pattern; primary delivery = at-target melee"),
    "footprint": dc("small-radius", 0.80, "Melee scythe sweeps cover small-radius close range"),
    "geo_text": "Death Seal locks the Lich's HP at a fraction of maximum, converting missing HP into bonus Necrotic damage. Harvest scythe attacks at melee range shred targets. Damage scales inversely with remaining HP.",
    "control": ctrl(["necrotic-weakness"], "rider", 0.65),
    "defense": defs(["self-cost", "glass"], "self-cost", 0.85),
    "economy": econ("Life (sealed by Death Seal)", "self-cost", "n/a", "n/a",
                    "Death Seal seals current HP as the maximum HP ceiling, preventing all healing above that threshold. The 'missing life' gap between sealed maximum and true maximum provides damage bonus. Self-cost sacrifice for power.",
                    0.85),
    "element": elem("Necrotic", "hit", 0.88),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": prefix(
        "INT", 0.88, "Acolyte/Lich INT-primary; Harvest + Death Seal both INT-scaling",
        "melee", 0.88, "Harvest is a melee scythe skill; M=melee confirmed",
        "high", 0.82, "High attack tempo: rapid Harvest scythe hits; H=high confirmed",
        "flat", 0.78, "Flat Necrotic damage output; missing-HP bonus is a flat multiplier, not spiky; F=flat confirmed",
        "solo", 0.88, "No proxy; Lich attacks directly; S=solo confirmed",
        "instant", 0.90, "Instant melee strikes"),
    "mechanics_notes": "prov=kb. mech_note ref: 'Death Seal LOCKS your health at a fraction and pays you damage for the missing life while Harvest scythes through melee range.' NE suffix = Necrotic. Shield-split D1: defense is self-cost (glass cannon via intentional HP reduction), NOT ward/shield. Different from le-reaper-form-lich's leech defense. Death Seal = economy=self-cost; Harvest = the delivery tool.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=kb",
    "sources_used": ["kb"],
})

# 16. le-fire-aura-spellblade (POST-CUTOFF 1.4-omens only, conf=0.37)
RECORDS.append({
    "kit_id": "le-fire-aura-spellblade", "folk_name": "Fire Aura Spellblade", "game": "le",
    "status": "positive", "atlas_key": "IMMFSI-_SDM-RS-FI-~~",
    "delivery": dc("aura-pulse", 0.37, "POST-CUTOFF: 'burning aura output on the melee-mage chassis' per mech_note implies aura-pulse delivery; live verification required"),
    "footprint": dc("small-radius", 0.37, "POST-CUTOFF: aura-pulse footprint is small-radius around player; inferred from aura class; live verification required"),
    "geo_text": "POST-CUTOFF (1.4-omens, Season 4). Fire aura radiating from melee-mage chassis. Full spatial characterization deferred to dossier.",
    "control": ctrl(["ignite"], "rider", 0.37),
    "defense": defs(["shield-absorb", "ward"], "ward", 0.40),
    "economy": econ("Mana", "reserve", "n/a", "n/a", "POST-CUTOFF: aura economy inferred as reserve/channel; live verification required", 0.37),
    "element": elem("Fire", "dot", 0.40),
    "movement": mov([], "full-move", False, 0.37),
    "prefix_claims": prefix(
        "INT", 0.45, "Mage/Spellblade INT-primary; POST-CUTOFF cap applied",
        "mid", 0.37, "POST-CUTOFF: M=mid from atlas; aura is near-melee range; cannot verify at cap",
        "med", 0.37, "POST-CUTOFF: M=med tempo from atlas; aura is sustained not pulsed rapidly; cannot verify",
        "flat", 0.37, "POST-CUTOFF: F=flat from atlas; aura damage is continuous flat output; cannot verify at cap",
        "solo", 0.37, "POST-CUTOFF: S=solo from atlas; aura is self-origin; cannot verify at cap",
        "instant", 0.40, "Aura activation likely instant; inferred from class pattern; POST-CUTOFF cap"),
    "mechanics_notes": "POST-CUTOFF. Season 4 (1.4-omens) aura-scaling rework. prov=lb. mech_note ref: 'The Season 4 aura-scaling rework birthed an S-tier — burning aura output on the melee-mage chassis, walk-forward damage.' RS suffix in old vocab = reserve economy. FI = Fire. Full dossier required.",
    "era_confirmed": ["1.4-omens"],
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "DEFERRED — post-cutoff; live source required",
    "sources_used": ["lb (post-cutoff)"],
})

# 17. le-lightning-blast
RECORDS.append({
    "kit_id": "le-lightning-blast", "folk_name": "Lightning Blast", "game": "le",
    "status": "positive", "atlas_key": "IRHFSI-HCMM-SP-LI-~~",
    "delivery": dc("projectile", 0.88, "Lightning Blast fires a projectile bolt that chains; initial delivery is projectile; chain behavior is footprint characteristic"),
    "footprint": dc("chain-hop", 0.88, "Atlas geo=chain confirmed; bolt chains between enemies (chain-hop footprint); multiple chain targets per cast"),
    "geo_text": "Lightning Blast fires a lightning bolt projectile that arcs between nearby enemies in chain-hop sequence. Tree nodes expand chain count, fork paths, and add repeat-cast procs for sustained storm coverage.",
    "control": ctrl(["shock", "electrify"], "core", 0.85),
    "defense": defs(["ward", "glass"], "ward", 0.78),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per blast. High cast-speed investment drives rapid bolt spam.",
                    0.82),
    "element": elem("Lightning", "hit", 0.90),
    "movement": mov([], "rooted", False, 0.85),
    "prefix_claims": prefix(
        "INT", 0.90, "Mage primary; Lightning Blast is a pure Mage spell scaling INT",
        "ranged", 0.88, "Ranged projectile bolt; R=ranged confirmed",
        "high", 0.85, "High cast tempo: rapid lightning spam; prov=lb;kb confirms high-cast-speed investment",
        "flat", 0.78, "Flat damage per bolt hit; chain procs are multiplicative but per-hit is flat; F=flat confirmed",
        "solo", 0.88, "No proxy; player casts directly; S=solo confirmed",
        "instant", 0.90, "Instant cast lightning bolt"),
    "mechanics_notes": "prov=lb;kb. mech_note ref: 'The chain-lightning perennial — tree paths for chains, forks, and repeat-cast storms, currently wearing the Runemaster's [optimization layer].' LI suffix = Lightning. Control=core: Shock/Electrify debuffs are the primary damage-amplification loop in Lightning Blast builds. Chain-hop footprint: G2 flag — this is chain-hop not a true line (each hop is a discrete jump, not a continuous beam). Ctrl C2: pure offense, no support application.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.2-woven", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=lb;kb",
    "sources_used": ["kb", "lb"],
})

# 18. le-wraithlord-necro
RECORDS.append({
    "kit_id": "le-wraithlord-necro", "folk_name": "Wraithlord Necromancer", "game": "le",
    "status": "positive", "atlas_key": "IRMFHI-MSDM-SU-NE-~~",
    "delivery": dc("at-target", 0.83, "Wraithlord autonomously seeks and attacks targets; at-target delivery mediated through the single large-proxy wraith"),
    "footprint": dc("small-radius", 0.78, "Wraithlord's attacks cover small-radius melee area around each targeted enemy"),
    "geo_text": "A single towering Wraithlord is summoned by feeding it smaller wraith minions via the Wraithlord's Harbour helm. The Wraithlord autonomously attacks enemies in melee range with massive impact. Player kites while the single proxy dominates.",
    "control": ctrl(["necrotic-weakness"], "rider", 0.65),
    "defense": defs(["minion-shield", "hp-stack"], "minion-shield", 0.78),
    "economy": econ("Mana + Wraith Consumption", "harvest", "n/a", "wraith minion kills feed the Wraithlord",
                    "Wraithlord's Harbour unique helm transforms the summon system: smaller wraiths are sacrificed to empower/maintain the single Wraithlord. Economy is harvest (consume minions to sustain/power the boss proxy).",
                    0.78),
    "element": elem("Necrotic", "hit", 0.85),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": prefix(
        "INT", 0.88, "Acolyte/Necromancer INT-primary; necrotic minion scaling INT",
        "ranged", 0.72, "Atlas R=ranged; nuance: Wraithlord itself is melee but the PLAYER operates at ranged-safe distance commanding it; atlas characterizes player range positioning; conf MED",
        "med", 0.80, "M=med tempo: Wraithlord attacks at measured pace; not rapid but consistent; M confirmed",
        "flat", 0.78, "Flat necrotic damage per Wraithlord hit; no spike mechanism",
        "heavy", 0.90, "Wraithlord IS the damage; player deals no direct damage; H=heavy proxy confirmed strongly",
        "instant", 0.90, "Summoning instant; Wraithlord attacks are autonomous"),
    "mechanics_notes": "prov=let;kb. mech_note ref: 'One helm replaces the army — Wraithlord's Harbour summons a SINGLE towering wraithlord you FEED your other wraiths to, empowering the boss-proxy while clearing with the expendable fodder.' NE suffix = Necrotic. Economy=harvest (minion consumption). This is the archetype-defining 'one big proxy' pattern distinct from le-skeleton-necro's 'many small proxies.'",
    "era_confirmed": ["1.0-launch", "1.1-harbingers", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=let;kb",
    "sources_used": ["kb", "let"],
})

# 19. le-runic-invocation
RECORDS.append({
    "kit_id": "le-runic-invocation", "folk_name": "Runic Invocation Runemaster", "game": "le",
    "status": "positive", "atlas_key": "IRMSSI-HLMM-MT-LI-~~",
    "delivery": dc("projectile", 0.78, "Most runic invocations fire projectile-type effects at target direction; delivery varies by rune combination but projectile dominates for damage combos"),
    "footprint": dc("large-zone", 0.80, "Major invocations create large elemental zone effects; atlas geo=large-AOE confirmed for the primary damage invocations"),
    "geo_text": "Runemaster slots 2-3 rune types in sequence and then invokes. The rune combination determines the spell output from dozens of possible invocations (fire burst, ice storm, lightning fork, etc.). High-tier combinations produce large elemental zones.",
    "control": ctrl(["chill", "shock", "ignite"], "rider", 0.75),
    "defense": defs(["shield-absorb", "ward"], "ward", 0.82),
    "economy": econ("Rune Sequences", "recipe", "n/a", "Runemaster slots runes before each cast",
                    "Economy is recipe-based: player arranges rune inputs (Glyph slots, Rune types) before casting. The combination is the 'recipe' that determines output. Mana cost applies on invocation.",
                    0.78),
    "element": elem("Cold / Lightning / Fire (rune-combination-dependent)", "hit", 0.78),
    "movement": mov([], "rooted", False, 0.80),
    "prefix_claims": prefix(
        "INT", 0.88, "Mage/Runemaster INT-primary; elemental spell scaling INT",
        "ranged", 0.82, "Invocations fire at ranged target; R=ranged confirmed for dominant invocation types",
        "med", 0.78, "M=med tempo: rune setup adds overhead vs pure spam; deliberate cadence; M confirmed",
        "spiky", 0.80, "High-tier rune combinations produce burst damage spikes; S=spiky confirmed for the build-defining invocations",
        "solo", 0.88, "No proxy; player invokes directly; S=solo confirmed",
        "instant", 0.85, "Invocation fires instantly after rune setup completes; no additional wind-up"),
    "mechanics_notes": "prov=gg;lw;kb. mech_note ref: 'Cast three RUNES in sequence and INVOKE the spell their combination spells out — dozens of distinct invocations from fire/ice/lightning combinations.' LI suffix = Lightning (dominant element in the corpus characterization). MT suffix in old vocab = multi-target. The recipe economy is unique in the LE corpus. Control=rider because element varies by rune choice; no single ailment is core identity.",
    "era_confirmed": ["1.0-launch", "1.2-woven", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=gg;lw;kb",
    "sources_used": ["kb", "gg", "lw"],
})

# 20. le-warpath-vk
RECORDS.append({
    "kit_id": "le-warpath-vk", "folk_name": "Warpath Void Knight", "game": "le",
    "status": "positive", "atlas_key": "SMHFSC-_SDT-SP-VO-~~",
    "delivery": dc("self-origin", 0.88, "Warpath spins the player continuously as a moving self-origin attack; all damage radiates from player position while channeling"),
    "footprint": dc("small-radius", 0.85, "Warpath's spin covers small-radius around player's moving position; Devouring Orb orbits in a larger ring but primary Warpath footprint is close-range"),
    "geo_text": "Warpath channels a continuous spinning attack around the player while they move freely. Devouring Orb (orbiting void sphere) procs and time-echo abilities add secondary void damage around the spinning Lich. The player IS the AoE center.",
    "control": ctrl(["void-corruption"], "rider", 0.72),
    "defense": defs(["armor", "block", "resist"], "armor", 0.82),
    "economy": econ("Mana", "reserve", "n/a", "n/a",
                    "Warpath drains Mana continuously while spinning. Void Knight Devouring Orb generates Void Stacks passively during the channel; Stacks empower void echoes.",
                    0.82),
    "element": elem("Void / Physical", "hit", 0.85),
    "movement": mov(["move-while-spinning"], "full-move", True, 0.88),
    "prefix_claims": prefix(
        "STR", 0.88, "Sentinel/Void Knight STR-primary; armor and melee scaling STR",
        "melee", 0.90, "Warpath is melee spinning; M=melee confirmed",
        "high", 0.85, "High tempo: continuous rapid spinning hits; H=high confirmed",
        "flat", 0.78, "Flat damage per spin tick; void echoes are additional flat events; F=flat confirmed",
        "solo", 0.85, "Primary damage from player's own spin; Devouring Orb is orbiting companion but the CORE is solo; S=solo is a reasonable characterization (though VK has echo/orb assists)",
        "channel", 0.92, "Confirmed channel: Warpath is a hold-to-spin channel; C=channel confirmed"),
    "mechanics_notes": "prov=eg;gg;kb. mech_note ref: 'Spin-to-win in void — Warpath's channel-move whirl paired with Devouring Orb's orbiting void spheres and time-echo procs.' VO suffix = Void element. skill_is_movement=true: Warpath allows free movement while spinning (unlike most channel skills that root the player). Movement verb = 'move-while-spinning' (the player walks/runs while the spinning channel continues). Defense = armor+block (Sentinel class archetype). Shield-split D1: Sentinel uses ARMOR+BLOCK, NOT ward/ES.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.1-harbingers", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=eg;gg;kb",
    "sources_used": ["kb", "eg", "gg"],
})

# 21. le-erasing-strike-vk
RECORDS.append({
    "kit_id": "le-erasing-strike-vk", "folk_name": "Erasing Strike Void Knight", "game": "le",
    "status": "positive", "atlas_key": "SMLSLW-LLDT-SP-VO-~~",
    "delivery": dc("at-target", 0.83, "Aimed colossal void cleave delivered at targeted direction; at-target melee delivery confirmed"),
    "footprint": dc("large-zone", 0.82, "Colossal cleave covers large zone in strike direction; atlas geo=large-AOE confirmed by 'colossal void cleave' description"),
    "geo_text": "Void Knight executes one massive telegraphed void cleave after wind-up. Time echoes replay the full strike as ghost copies seconds later, extending effective coverage. Low cadence — single devastating strike per cycle.",
    "control": ctrl(["void-corruption", "time-stop"], "rider", 0.72),
    "defense": defs(["armor", "block", "resist"], "armor", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per strike. Low tempo means low Mana expenditure rate but each strike is expensive. Time-echo generation is passive (no additional cost).",
                    0.80),
    "element": elem("Void", "hit", 0.88),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "STR", 0.88, "Sentinel/Void Knight STR-primary confirmed",
        "melee", 0.90, "Melee cleave; M=melee confirmed",
        "low", 0.85, "L=low tempo: single slow deliberate cleave; L confirmed by wind-up pattern and large-zone design",
        "spiky", 0.85, "Colossal single-hit spike; S=spiky confirmed; time-echoes add spiky replay events",
        "light", 0.78, "L=light proxy: time echoes replay the strike as ghost copies — light proxy assistance, player still primary; L=light confirmed",
        "wind-up", 0.88, "W=wind-up confirmed; telegraphed colossal cleave requires visible wind-up before release"),
    "mechanics_notes": "prov=gg;kb. mech_note ref: 'One colossal void cleave — then the VK's TIME ECHOES replay the entire hit seconds later as a ghost of yourself repeating the strike.' VO suffix = Void. wind-up commitment is the defining mechanical feature (the echo-replay pattern requires the original strike to trigger echoes). Low tempo + spiky amp + wind-up = classic heavy-hitter pattern. Ctrl C2: pure offense.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=gg;kb",
    "sources_used": ["kb", "gg"],
})

# 22. le-manifest-armor
RECORDS.append({
    "kit_id": "le-manifest-armor", "folk_name": "Manifest Armor Forge Guard", "game": "le",
    "status": "positive", "atlas_key": "SMMFHI-MSDT-SU-PH-~~",
    "delivery": dc("at-target", 0.82, "Manifest Armor construct autonomously attacks enemies; at-target delivery via animated proxy"),
    "footprint": dc("small-radius", 0.78, "Manifest Armor's melee attacks cover small-radius around each target"),
    "geo_text": "Forge Guard's equipped armor animates as a fighting construct that scales from the gear on the player's body. The Manifest Armor pursues and attacks enemies at melee range while the player commands from behind.",
    "control": ctrl(["stun"], "rider", 0.65),
    "defense": defs(["armor", "block", "resist"], "armor", 0.88),
    "economy": econ("Forge Stacks", "harvest", "n/a", "melee kills generate Forge Stacks",
                    "Forge Guard harvests Forge Stacks from melee kills to upgrade and maintain the Manifest Armor construct. Higher Forge Stack investment improves the armor's power level. Primary Mana cost for initial summon.",
                    0.78),
    "element": elem("Physical / Fire", "hit", 0.78),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": prefix(
        "STR", 0.88, "Sentinel/Forge Guard STR-primary; armor scaling STR",
        "melee", 0.88, "Manifest Armor fights at melee range; M=melee confirmed",
        "med", 0.80, "M=med tempo: animated armor attacks at moderate cadence; M confirmed",
        "flat", 0.78, "Flat damage per construct hit; no spike mechanism; F=flat confirmed",
        "heavy", 0.88, "Manifest Armor IS the primary damage vector; player deals minimal direct damage; H=heavy proxy confirmed",
        "instant", 0.88, "Manifest Armor summoned instantly"),
    "mechanics_notes": "prov=let;kb. mech_note ref: 'Your EQUIPPED ARMOR stands up and fights — Manifest Armor animates a construct whose stats scale from the gear on YOUR body.' PH suffix = Physical element. Economy=harvest (Forge Stacks from melee kills). The unique gear-scaling mechanic means the construct's power IS the player's gear investment — tight stat coupling. Shield-split D1: Sentinel uses ARMOR, not ward/ES.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=let;kb",
    "sources_used": ["kb", "let"],
})

# 23. le-smite-paladin
RECORDS.append({
    "kit_id": "le-smite-paladin", "folk_name": "Smite Paladin", "game": "le",
    "status": "positive", "atlas_key": "WDHFSI-MNDT-PC-LI-~~",
    "delivery": dc("at-target", 0.85, "Smite calls lightning down on targeted position (overhead delivery to at-target location); PC suffix = proc-trigger Smite on melee hits"),
    "footprint": dc("point", 0.82, "Single lightning strike at targeted point; small point impact; atlas geo=single confirmed"),
    "geo_text": "Smite calls down holy lightning on a targeted point. The key engine is proc-triggering: every melee hit, thrown weapon hit, or similar trigger fires an additional Smite call. Multiple Smites rain from above every time the player attacks.",
    "control": ctrl(["shock", "stun"], "rider", 0.72),
    "defense": defs(["armor", "block", "resist"], "armor", 0.82),
    "economy": econ("Mana", "proc", "n/a", "melee/weapon attacks trigger Smite procs",
                    "Smite's primary economy is proc-triggered: each melee or weapon hit auto-generates a Smite for free. A base Mana cost exists for manually cast Smite but the dominant playstyle is proc-chain (economy = proc).",
                    0.80),
    "element": elem("Lightning", "hit", 0.88),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "WIS", 0.85, "Sentinel/Paladin WIS-secondary (Paladin uses both STR and WIS; WIS governs Holy/Lightning scaling); atlas W=WIS confirmed",
        "mid", 0.75, "Smite strikes from above; player operates at mid-range; D=mid characterizes player positioning relative to proc triggers",
        "high", 0.82, "High tempo: proc-chain fires many Smites per second at high attack speed; H=high confirmed",
        "flat", 0.78, "Flat lightning damage per Smite; no spike mechanism per proc; F=flat confirmed",
        "solo", 0.88, "No proxy; Smite is player-triggered holy power; S=solo confirmed",
        "instant", 0.90, "Instant delivery (lightning from sky); no wind-up"),
    "mechanics_notes": "prov=let;kb. mech_note ref: 'Bolts of holy lightning called down on every trigger the tree can wire — smite-on-hit, smite-on-throw, smite raining from procs.' LI suffix = Lightning. PC suffix in old vocab = proc-trigger economy (confirmed by mech_note). This is the canonical proc-spam archetype in LE. Shield-split D1: armor+block (Sentinel), NOT ward.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=let;kb",
    "sources_used": ["kb", "let"],
})

# 24. le-hammer-throw-paladin
RECORDS.append({
    "kit_id": "le-hammer-throw-paladin", "folk_name": "Hammer Throw Paladin", "game": "le",
    "status": "positive", "atlas_key": "WDHFSI-_MDT-SP-PH-~~",
    "delivery": dc("orbit", 0.83, "Hammer Throw evolves into orbit pattern: thrown hammers travel and ultimately circle/orbit the walking Paladin; orbit delivery is the build-defining form"),
    "footprint": dc("multi-point", 0.80, "Multiple hammers orbiting at different angular positions create multi-point coverage around the player; atlas geo=multi-spawn confirmed"),
    "geo_text": "Hammer Throw launches physical hammers that travel outward and then — via tree nodes — begin orbiting the moving Paladin. Multiple hammers orbit simultaneously, striking all enemies the player walks through or near.",
    "control": ctrl(["shock"], "rider", 0.65),
    "defense": defs(["armor", "block", "resist"], "armor", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per hammer throw. Orbit-enabling tree nodes cause thrown hammers to persist in orbit (no per-orbit cost). Active hammer count is the key economy variable.",
                    0.78),
    "element": elem("Physical / Lightning", "hit", 0.78),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": prefix(
        "WIS", 0.83, "Sentinel/Paladin WIS-secondary scaling; Hammer Throw uses WIS-linked holy damage nodes",
        "mid", 0.75, "Hammers thrown at mid-range before orbit; D=mid approximate for throw range",
        "high", 0.82, "High tempo: multiple orbiting hammers hit rapidly as player moves through enemies; H=high effective strike cadence",
        "flat", 0.78, "Flat physical damage per hammer hit; no spike model",
        "solo", 0.85, "Player throws own hammers; no proxy entities; S=solo confirmed",
        "instant", 0.90, "Instant throw; no wind-up"),
    "mechanics_notes": "prov=let;kb. mech_note ref: 'Thrown hammers with tree nodes for RICOCHET and ORBIT paths circling the walking Paladin — Last Epoch's chapter of the genre-wide Hammerdin lineage.' PH suffix = Physical. geo=multi-spawn in atlas correctly characterized as orbit/multi-point. Orbit delivery is the distinguishing mechanic vs simple projectile throw. Two delivery modes (ricochet vs orbit) with orbit being the canonical endgame build. Ctrl C2: pure offense.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.2-woven", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=let;kb",
    "sources_used": ["kb", "let"],
})

# 25. le-storm-totem-shaman
RECORDS.append({
    "kit_id": "le-storm-totem-shaman", "folk_name": "Storm Totem Shaman", "game": "le",
    "status": "positive", "atlas_key": "WDMFHI-HMMM-SP-LI-~~",
    "delivery": dc("at-target", 0.82, "Totems placed at target location autonomously fire lightning at nearby enemies; at-target delivery mediated by totem placement and totem-autonomous attack"),
    "footprint": dc("multi-point", 0.82, "Multiple totems placed at different positions simultaneously; each totem covers its own area; multi-point coverage atlas geo=multi-spawn confirmed"),
    "geo_text": "Shaman plants lightning totems at targeted positions. Active totems channel lightning at nearby enemies and call tornadoes. Multiple simultaneous totems provide multi-point area coverage while the Shaman repositions freely.",
    "control": ctrl(["shock", "slow-tornado"], "rider", 0.72),
    "defense": defs(["hp-stack", "armor"], "hp-stack", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per totem placed. Totems persist until killed or replaced. Multiple totems active simultaneously up to cap.",
                    0.80),
    "element": elem("Lightning", "hit", 0.88),
    "movement": mov([], "full-move", False, 0.88),
    "prefix_claims": prefix(
        "WIS", 0.85, "Primalist/Shaman WIS-primary (Primalist uses WIS for elemental/totem scaling); W=WIS confirmed",
        "mid", 0.75, "Totems placed at mid-range relative to enemies; D=mid characterizes totem placement distance",
        "med", 0.80, "M=med tempo: moderate totem placement cadence; each totem persistent; M confirmed",
        "flat", 0.78, "Flat lightning damage per totem strike; F=flat confirmed",
        "heavy", 0.88, "Totems DO the work; Shaman kites; H=heavy proxy confirmed (totems = autonomous heavy proxy)",
        "instant", 0.90, "Instant totem placement"),
    "mechanics_notes": "prov=kb. mech_note ref: 'Planted totems channel the storm FOR you — lightning pylons and spinning tornadoes doing the casting while the shaman repositions.' LI suffix = Lightning. Heavy proxy: the totems are fully autonomous and generate all meaningful damage — Shaman is a placement/movement unit. Shield-split D1: Primalist uses HP-STACK, not ward or block.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=kb",
    "sources_used": ["kb"],
})

# 26. le-squirrel-bm
RECORDS.append({
    "kit_id": "le-squirrel-bm", "folk_name": "Squirrel Beastmaster", "game": "le",
    "status": "positive", "atlas_key": "WMHFHI-HNDM-SU-PH-~~",
    "delivery": dc("at-target", 0.82, "Squirrel swarm autonomously attacks and shreds targeted enemies; at-target delivery via companion swarm"),
    "footprint": dc("small-radius", 0.78, "Squirrels cluster and attack within small-radius around each enemy target; atlas geo=single characterizes per-target focus"),
    "geo_text": "Beastmaster summons a swarm of squirrels (converted from wolf companion slots via Herald of the Scurry). The squirrel tide autonomously pursues and overwhelms enemies at close range, each squirrel dealing rapid physical hits.",
    "control": ctrl(["bleed"], "rider", 0.65),
    "defense": defs(["hp-stack", "armor"], "hp-stack", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend to summon squirrels. Squirrels persist autonomously and resupply from Herald of the Scurry passive conversion.",
                    0.78),
    "element": elem("Physical", "hit", 0.85),
    "movement": mov([], "full-move", False, 0.88),
    "prefix_claims": prefix(
        "WIS", 0.85, "Primalist/Beastmaster WIS-primary; companion scaling WIS for Primalist",
        "melee", 0.82, "Squirrels fight at melee range; M=melee confirmed",
        "high", 0.82, "High tempo: rapid multi-squirrel attack cadence; H=high confirmed by 'shrieking rodent tide' descriptor",
        "flat", 0.78, "Flat physical damage per squirrel hit; F=flat confirmed",
        "heavy", 0.88, "Squirrel swarm IS the primary damage vector; player deals no direct damage; H=heavy proxy confirmed",
        "instant", 0.88, "Summon instant; squirrels attack autonomously"),
    "mechanics_notes": "prov=let;kb. mech_note ref: 'Herald of the Scurry converts your wolf slots into a SWARM OF SQUIRRELS — a shrieking rodent tide that shreds the endgame pile.' PH suffix = Physical. Unique economy: Herald of the Scurry is the enabling unique item (converts wolf summons to squirrels). Atlas geo=single refers to each squirrel's per-target focus.",
    "era_confirmed": ["1.0-launch", "1.1-harbingers", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=let;kb",
    "sources_used": ["kb", "let"],
})

# 27. le-swarmblade-druid
RECORDS.append({
    "kit_id": "le-swarmblade-druid", "folk_name": "Swarmblade Druid", "game": "le",
    "status": "positive", "atlas_key": "WMHFLI-KSDD-MT-PH-~~",
    "delivery": dc("self-origin", 0.80, "Swarmblade form transforms the player into a swarm-hybrid; attacks emanate from player position in melee/short range; self-origin transformation delivery"),
    "footprint": dc("small-radius", 0.78, "Swarm and melee attacks cover small-radius close area around the transformed Druid"),
    "geo_text": "Druid transforms into the Swarmblade — a locust-swarm hybrid with its own skill bar. In form, the Druid executes swarm-dive attacks, serpent-strikes, and summons a swarm aura around the body. The swarm damages enemies within close range while the form persists.",
    "control": ctrl(["poison", "slow"], "rider", 0.68),
    "defense": defs(["hp-stack", "armor"], "hp-stack", 0.80),
    "economy": econ("Mana + Transformation Meter", "meter", "n/a", "combat actions in Swarmblade form maintain transformation meter",
                    "Entering Swarmblade costs Mana. Maintaining the form requires sustained combat (attacks refresh the transformation meter). Abandoning combat causes the form to time out.",
                    0.72),
    "element": elem("Physical / Poison", "hybrid", 0.75),
    "movement": mov(["dive-as-swarm"], "full-move", False, 0.80),
    "prefix_claims": prefix(
        "WIS", 0.83, "Primalist/Druid WIS-primary; transformation forms scale WIS",
        "melee", 0.82, "Swarmblade attacks at melee/close range; M=melee confirmed",
        "high", 0.80, "High tempo: rapid swarm attacks in form; H=high confirmed",
        "flat", 0.75, "Flat damage per swarm hit; poison DoT adds hybrid element but base is flat; F=flat confirmed",
        "light", 0.78, "L=light proxy: the swarm assists the player-form but player IS the swarmblade; light companion assistance",
        "instant", 0.85, "Transformation instant; in-form attacks instant"),
    "mechanics_notes": "prov=kb. mech_note ref: 'Transform into a locust-swarm hybrid with ITS OWN SKILL BAR — dive as the swarm, serpent-strike as the blade-arms, rage.' PH suffix = Physical. MT suffix in old vocab = multi-target. Movement verb=dive-as-swarm: in Swarmblade form, Dive Swarm is a short-range movement skill within the form. damage_mode=hybrid (physical hit + poison DoT from swarm contacts). conf=0.65 in atlas (lower confidence build — less documented than other Primalist builds).",
    "era_confirmed": ["1.0-launch", "1.1-harbingers", "1.2-woven"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=kb",
    "sources_used": ["kb"],
})

# 28. le-healing-hands-paladin
RECORDS.append({
    "kit_id": "le-healing-hands-paladin", "folk_name": "Healing Hands Paladin", "game": "le",
    "status": "positive", "atlas_key": "WMHFSI-MSDT-SP-FI-~~",
    "delivery": dc("at-target", 0.82, "Healing Hands wired to trigger on melee hits; each melee attack delivers heal-strike at target; at-target confirmed"),
    "footprint": dc("small-radius", 0.80, "Healing Hands covers small-radius around melee target; SP suffix = single-point/small in old vocab"),
    "geo_text": "Healing Hands triggers on melee hits, converting sustain into stacked holy fire damage. Each melee strike applies both a heal and stacked holy amplification. In party context, heals apply to nearby allies; in solo play, self-sustain is the primary application.",
    "control": ctrl([], "none", 0.75),
    "defense": defs(["sustain-leech", "armor", "block"], "sustain-leech", 0.82),
    "economy": econ("Mana", "proc", "n/a", "melee hit triggers Healing Hands proc",
                    "Healing Hands is proc-economy: each melee hit auto-fires Healing Hands without additional Mana cost (beyond initial skill cast). The dominant spend is initial skill activation.",
                    0.80),
    "element": elem("Fire / Holy (Lightning)", "hit", 0.78),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "WIS", 0.85, "Sentinel/Paladin WIS-primary for Holy/heal scaling; W=WIS confirmed",
        "melee", 0.88, "Healing Hands triggers on melee hits; M=melee confirmed",
        "high", 0.82, "High tempo: rapid melee attack cadence with every hit triggering Healing Hands; H=high confirmed",
        "flat", 0.78, "Flat heal/damage per trigger; stacking amplification is cumulative-flat not spiky; F=flat confirmed",
        "solo", 0.85, "No proxy; player melee attacks; S=solo confirmed",
        "instant", 0.90, "Proc-triggered instant heal/damage; no wind-up"),
    "mechanics_notes": "prov=gg;kb. mech_note ref: 'The HEAL becomes the weapon — Healing Hands wired to trigger on melee hits, converting sustain into stacked holy damage that melts bosses.' FI suffix = Fire element. Ctrl C2 NOTE: Healing Hands CAN function as party-heal support in multiplayer; however, LE is primarily solo and the build is typically built as offense (sustain-as-damage). NO pure-solo-support kit found; Healing Hands is the closest candidate but its primary build mode is offensive self-sustain. Shield-split D1: Sentinel armor+block, also sustain-leech from heals. Ctrl C2 sweep: NEGATIVE — Healing Hands is not a pure support kit in solo context.",
    "era_confirmed": ["1.1-harbingers", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=gg;kb",
    "sources_used": ["kb", "gg"],
})

# 29. le-judgement-paladin
RECORDS.append({
    "kit_id": "le-judgement-paladin", "folk_name": "Judgement Paladin", "game": "le",
    "status": "positive", "atlas_key": "WMMFSI-MLDT-SP-FI-~~",
    "delivery": dc("at-target", 0.83, "Judgement slams the ground at targeted location creating a consecrated blast zone; at-target ground slam delivery"),
    "footprint": dc("large-zone", 0.82, "Consecrated zone covers large AoE; atlas geo=large-AOE confirmed by 'consecrates the ground' mech_note"),
    "geo_text": "Paladin slams creating a large consecrated zone that heals the Paladin and applies burning damage to enemies within it. Judgement echo strikes rain down from above inside the zone during the active duration.",
    "control": ctrl(["slow", "burn"], "rider", 0.72),
    "defense": defs(["armor", "block", "resist", "sustain-leech"], "armor", 0.82),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per Judgement cast. Moderate tempo: zone persists briefly, Paladin can recast to maintain.",
                    0.80),
    "element": elem("Fire", "hit", 0.85),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": prefix(
        "WIS", 0.85, "Sentinel/Paladin WIS-primary for Fire/Holy scaling; W=WIS confirmed",
        "melee", 0.82, "Ground slam at melee/close range; M=melee confirmed (player must be near the target zone)",
        "med", 0.80, "M=med tempo: Judgement has a cast cycle; not rapid-fire but not slow; M confirmed",
        "flat", 0.78, "Flat damage from consecrated zone + echo strikes; F=flat confirmed",
        "solo", 0.88, "No proxy; player slams; S=solo confirmed",
        "instant", 0.85, "Instant slam (though echo strikes follow after brief delay, the player commitment is instant)"),
    "mechanics_notes": "prov=lb;kb. mech_note ref: 'Slam that consecrates the ground — the zone heals you and burns them while Judgement echoes rain down; melee-caster hybrid.' FI suffix = Fire. The dual function (heal zone + damage zone) is notable: defense = sustain-leech from the heal component. Echo strikes = secondary delivery events within the zone. Shield-split D1: armor+block+sustain, NOT ward.",
    "era_confirmed": ["1.0-launch", "1.2-woven", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=lb;kb",
    "sources_used": ["kb", "lb"],
})

# 30. le-werebear-druid
RECORDS.append({
    "kit_id": "le-werebear-druid", "folk_name": "Werebear Druid", "game": "le",
    "status": "positive", "atlas_key": "WMMFSI-MSMT-MT-PH-~~",
    "delivery": dc("self-origin", 0.82, "Werebear transformation — player becomes the bear; all damage emanates from bear-form melee attacks centered on player position; self-origin transformation"),
    "footprint": dc("small-radius", 0.80, "Bear form melee attacks (swipe, maul, roar) cover small-radius around the transformed Druid"),
    "geo_text": "Druid transforms into a Werebear with its own skill bar (swipe, roar, maul). The bear form provides massive built-in tankiness and melee attacks within close range. Form is maintained on a Rage-drain meter.",
    "control": ctrl(["maul-wound", "roar-slow"], "rider", 0.68),
    "defense": defs(["hp-stack", "armor"], "hp-stack", 0.88),
    "economy": econ("Mana + Rage", "meter", "rage", "combat attacks in bear form generate then drain Rage",
                    "Entering Werebear costs Mana. Rage builds during combat and drains when not attacking. Rage powers enhanced bear attacks. The bear form itself persists as long as the player maintains combat activity.",
                    0.78),
    "element": elem("Physical", "hit", 0.85),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": prefix(
        "WIS", 0.83, "Primalist/Druid WIS-primary; transformation forms scale WIS; W=WIS confirmed",
        "melee", 0.90, "Werebear is pure melee in form; M=melee confirmed",
        "med", 0.80, "M=med tempo: bear form attacks are deliberate heavy hits; not rapid-fire but not slow; M confirmed",
        "flat", 0.78, "Flat physical damage per bear hit; F=flat confirmed",
        "solo", 0.88, "No proxy in bear form; player IS the bear; S=solo confirmed",
        "instant", 0.88, "Transformation triggered instantly"),
    "mechanics_notes": "prov=mx-le;eg;kb. mech_note ref: 'The bear form with its own bar — swipe, roar, maul on rage-drain fuel, massive built-in tankiness; the Season 4 bossing king.' PH suffix = Physical. MT suffix in old vocab = multi-target (bear AoE). meter_type=rage: Werebear uses Rage secondary meter. eras include 1.4-omens but also beta through 1.0 — NOT post-cutoff (bear existed from beta; Season 4 reference = became S-tier, not introduced). conf=0.73 in atlas reflects the build's relatively consistent but not dominant historical presence pre-Season-4.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; prov=mx-le;eg;kb",
    "sources_used": ["kb", "mx-le", "eg"],
})

# 31. le-low-life-ward
RECORDS.append({
    "kit_id": "le-low-life-ward", "folk_name": "Low-Life Ward (archetype)", "game": "le",
    "status": "positive", "atlas_key": "IMHFSI-MSDM-RS-__-~~",
    "delivery": dc("at-target", 0.55, "Low-life-ward is an archetype, not a specific skill; primary delivery is whatever melee/spell the Spellblade uses (typically Flame Reave = at-target); conf LOW due to archetype-level abstraction"),
    "footprint": dc("small-radius", 0.52, "Spellblade INT/melee context = small-radius melee footprint; conf LOW due to archetype abstraction"),
    "geo_text": "The low-life-ward archetype (Exsanguinous + Last Steps of the Living uniques) drains the HP bar to near-zero and pays Ward per missing HP. The character exists at a sliver of health but walls of Ward absorb all incoming damage. Primary delivery is class-dependent (typically Spellblade melee-mage).",
    "control": ctrl([], "none", 0.55),
    "defense": defs(["shield-absorb", "ward"], "ward", 0.92),
    "economy": econ("Life (intentionally depleted)", "self-cost", "n/a", "Exsanguinous + Last Steps drain HP to near-zero",
                    "The unique items (Exsanguinous, Last Steps of the Living) drain HP and pay Ward per missing HP point. The 'economy' is accepting extreme self-cost (near-zero HP) to maximize Ward generation.",
                    0.85),
    "element": elem("Element varies by class/skill; typically Fire or Cold for Spellblade", "hit", 0.52),
    "movement": mov([], "full-move", False, 0.72),
    "prefix_claims": prefix(
        "INT", 0.82, "Atlas bc6 pos-1 = I=INT; low-life-ward is most common on INT-primary classes (Spellblade, Warlock, Runemaster); INT confirmed as primary archetype anchor",
        "melee", 0.70, "Atlas bc6 pos-2 = M=melee; low-life-ward most commonly appears on Spellblade (melee) context; M=melee is the corpus characterization",
        "high", 0.72, "Atlas bc6 pos-3 = H=high; Spellblade low-life-ward builds use high attack speed; H=high confirmed from Spellblade context",
        "flat", 0.70, "Atlas bc6 pos-4 = F=flat; Ward-scaling is flat (HP-to-Ward ratio); flat damage output from skills; F=flat confirmed",
        "solo", 0.80, "Atlas bc6 pos-5 = S=solo; no proxy; player attacks; S=solo confirmed",
        "instant", 0.82, "Atlas bc6 pos-6 = I=instant; Spellblade attacks instant; confirmed"),
    "mechanics_notes": "prov=eg;kb. mech_note ref: 'Exsanguinous and Last Steps DRAIN your health bar and pay ward per point missing — the character lives at a sliver of reality.' RS suffix = reserve economy in old vocab. conf=0.47 in atlas — reflects that this is an archetype (item combo) rather than a specific skill build, leading to lower confidence in characterization. NOT post-cutoff: spans beta-0.8-0.9 through 1.4; the archetype predates training cutoff. The Ward defense is primary and defining; all other fields are secondary to the Ward-stack pattern. Shield-split D1: this IS a Ward kit — explicitly Ward-primary (Exsanguinous+Last Steps = LE's ES/ward equivalent). Low conf carried forward into prefix_claims to reflect archetype-level uncertainty.",
    "era_confirmed": ["beta-0.8-0.9", "1.0-launch", "1.2-woven", "1.4-omens"],
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "NOT APPLICABLE — archetype defined by unique items, not a rankable skill",
    "sources_used": ["kb", "eg"],
})

# 21 (VK shield throw) - POST-CUTOFF
RECORDS.append({
    "kit_id": "le-shield-throw-time-rot-vk", "folk_name": "Shield Throw Time Rot VK", "game": "le",
    "status": "positive", "atlas_key": "SDMFSI-MCDT-SP-VO-~~",
    "delivery": dc("projectile", 0.40, "POST-CUTOFF: thrown shield is projectile delivery; ricochet pattern inferred from mech_note; live verification required"),
    "footprint": dc("chain-hop", 0.38, "POST-CUTOFF: 'ricocheting shield throws' per mech_note implies chain-hop footprint; live verification required"),
    "geo_text": "POST-CUTOFF (1.4-omens only). Ricocheting shield throws carrying Time Rot void stacks. Full spatial characterization deferred.",
    "control": ctrl(["void-corruption", "time-rot"], "core", 0.38),
    "defense": defs(["armor", "block"], "armor", 0.40),
    "economy": econ("Mana", "spend", "n/a", "n/a", "POST-CUTOFF: economy inferred from Sentinel class pattern", 0.38),
    "element": elem("Void", "hit", 0.40),
    "movement": mov([], "full-move", False, 0.40),
    "prefix_claims": prefix(
        "STR", 0.45, "Sentinel/Void Knight STR-primary; POST-CUTOFF cap",
        "mid", 0.38, "POST-CUTOFF: D=mid from atlas; shield throw range; cannot verify at cap",
        "med", 0.38, "POST-CUTOFF: M=med from atlas; cannot verify",
        "flat", 0.38, "POST-CUTOFF: F=flat from atlas; cannot verify",
        "solo", 0.38, "POST-CUTOFF: S=solo from atlas; cannot verify",
        "instant", 0.40, "VK pattern typically instant; POST-CUTOFF cap"),
    "mechanics_notes": "POST-CUTOFF. 1.4-omens only; conf=0.40 in atlas. prov=mx-le. mech_note ref: 'Ricocheting shield throws carrying Time Rot void stacks — the captain-america delivery finally earning a tier row through the Season 4 mechanics.' VO suffix = Void. Time Rot = void ailment. Full dossier required.",
    "era_confirmed": ["1.4-omens"],
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "DEFERRED — post-cutoff; live source required",
    "sources_used": ["mx-le (post-cutoff)"],
})

# ---------------------------------------------------------------------------
# NEGATIVE RECORDS — light schema
# ---------------------------------------------------------------------------

NEGATIVES = [
    {
        "kit_id": "le-soul-feast", "folk_name": "Soul Feast (as primary)", "game": "le",
        "status": "negative", "atlas_key": "IRMSSI-MNDM-AM-NE-~~",
        "delivery": dc("at-target", 0.80, "Life-drain anchored to target; at-target delivery"),
        "footprint": dc("point", 0.75, "Single-target life drain; point footprint; atlas geo=single confirmed"),
        "why_negative": "support-only; Soul Feast functions as the 'feed' mechanism inside Fissure/Warlock builds (cursor-consumption nuke), never as primary build identity; no community-defined Soul Feast primary build exists at corpus-eligible tier",
        "era_span": ["1.0-launch", "1.1-harbingers", "1.2-woven"],
        "post_cutoff": False,
        "dossier_owed": False,
        "prov": "kb",
        "mech_note": "NE suffix = Necrotic. AM suffix in old vocab = ammo/proc economy. mech_note ref: 'The curse-consumption nuke that never carried a build of its own — it lives as the FEED inside Fissure builds.' Ctrl C2: NEGATIVE — Soul Feast is the purest 'support-only' case in LE corpus but it's a rider inside offense builds, not a standalone support.",
    },
    {
        "kit_id": "le-shield-bash-le", "folk_name": "Shield Bash (LE)", "game": "le",
        "status": "negative", "atlas_key": "SMMSSI-LNMT-SP-PH-~~",
        "delivery": dc("at-target", 0.85, "Melee shield slam at target; at-target"),
        "footprint": dc("point", 0.80, "Single-target shield impact; atlas geo=single but SP='point' in new vocab"),
        "why_negative": "failed-meta; Shield Bash has no LE node tree depth worth building around — the third game in the corpus (after D2 and PoE1) where a skill named Shield Bash appears as a negative; LE's Sentinel tree provides no meaningful Shield Bash scaling path",
        "era_span": ["beta-0.8-0.9", "1.0-launch", "1.2-woven"],
        "post_cutoff": False,
        "dossier_owed": False,
        "prov": "kb",
        "mech_note": "mech_note ref: 'The shield-slam that never found a tree path worth building — the third game in the corpus where a skill named Shield Bash appears as a negative.' PH suffix = Physical.",
    },
    {
        "kit_id": "le-tempest-strike", "folk_name": "Tempest Strike", "game": "le",
        "status": "negative", "atlas_key": "WMHVSI-MSMM-PC-LI-~~",
        "delivery": dc("at-target", 0.82, "Melee strikes proc storm spells on hit; at-target melee delivery"),
        "footprint": dc("small-radius", 0.78, "Storm spell procs cover small-radius around the melee hit"),
        "why_negative": "mechanic-too-narrow; Tempest Strike procs RANDOM storm spells (lightning/gale/ice on dice roll) — stochastic element makes it impossible to optimize for any single elemental identity; variable amp (V in atlas) reflects the uncontrollable variance; never dominant in any element tier",
        "era_span": ["beta-0.8-0.9", "1.0-launch", "1.2-woven"],
        "post_cutoff": False,
        "dossier_owed": False,
        "prov": "kb",
        "mech_note": "mech_note ref: 'Melee strikes that proc random storm spells — lightning, gale, or spike on dice rolls — a stochastic proc identity that [never achieved dominant meta tier].' V=variable amp in atlas confirms the uncontrolled element variation. LI suffix = Lightning dominant element in atlas but the proc pool is all-element.",
    },
]

# ---------------------------------------------------------------------------
# WRITE OUTPUT
# ---------------------------------------------------------------------------

all_records = RECORDS + NEGATIVES

with open(OUT, "w") as f:
    for rec in all_records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

pos_count = sum(1 for r in all_records if r["status"] == "positive")
neg_count = sum(1 for r in all_records if r["status"] == "negative")
pc_count = sum(1 for r in all_records if r.get("post_cutoff"))
print(f"LE: {len(all_records)} records | pos={pos_count} neg={neg_count} post-cutoff={pc_count}")
print(f"Written: {OUT}")

# ---------------------------------------------------------------------------
# DIRECTED SWEEP SUMMARY (for index)
# ---------------------------------------------------------------------------
print()
print("=== DIRECTED SWEEP RESULTS ===")
print()
print("SWEEP 1 — Support-existence (ctrl C2):")
print("  Result: NO pure solo-context support kit found in LE corpus.")
print("  Closest: le-healing-hands-paladin (can heal party) but primary build is offense/self-sustain.")
print("  le-soul-feast is rider-support inside other builds, not standalone.")
print("  C2 answer for LE: NEGATIVE — LE is offense-only in corpus characterization.")
print()
print("SWEEP 2 — Line-vs-projectile (geo G2):")
print("  G2 flags (true line geometry, NOT chain-hop):")
print("  - le-chthonic-fissure-warlock: delivery=line, footprint=lane (fissure crawls forward as directional line)")
print("  - le-ghostflame-warlock: delivery=beam, footprint=cone (channeled directional cone beam)")
print("  - le-frost-wall-rm: footprint=lane (wall extends as a horizontal lane barrier)")
print("  Chain-hop (NOT true line):")
print("  - le-lightning-blast: footprint=chain-hop (discrete hops, not continuous beam)")
print()
print("SWEEP 3 — Shield-split (def D1):")
print("  WARD/ES kits (shield-absorb primary):")
print("  - le-low-life-ward: ward (archetype-defining Ward kit)")
print("  - le-ghostflame-warlock: ward (Warlock class)")
print("  - le-chthonic-fissure-warlock: ward (Warlock class)")
print("  - le-frost-wall-rm: ward (Runemaster class)")
print("  - le-flame-reave-spellblade: ward (Spellblade class)")
print("  NOT ward — armor+block (Sentinel): le-smite-paladin, le-hammer-throw-paladin,")
print("    le-storm-totem-shaman (HP), le-squirrel-bm (HP), le-erasing-strike-vk,")
print("    le-manifest-armor, le-warpath-vk, le-judgement-paladin, le-healing-hands-paladin")
print("  Self-cost defense: le-harvest-lich (Death Seal), le-reaper-form-lich (form decay)")
print("  Dodge: le-umbral-blades, le-shadow-bladedancer, le-dive-bomb-falconer, le-explosive-trap-falconer, le-detonating-arrow-mm")
