"""
gen-undecember-facts.py
Mega-probe Unit A — Undecember (ud) — 17 records
17 positive / 0 negative / 4 post-cutoff (ud-s7-2025 kits)
Full schema (6 fact families per kit).
"""
import json
from pathlib import Path

OUT = Path("agentic_orchestration/legolas/research/megaprobe-2026-07-12/undecember-facts.jsonl")

# ── helpers ──────────────────────────────────────────────────────────────────

def pc(val, conf, ev): return {"value": val, "conf": conf, "evidence": ev}
def dc(val, conf, ev): return {"value": val, "conf": conf, "evidence": ev}
def ctrl(ailments, centrality, conf): return {"ailments": ailments, "centrality": centrality, "conf": conf}
def defs(layers, primary, conf): return {"layers": layers, "primary": primary, "conf": conf}
def econ(res, model, meter, builder, text, conf):
    return {"resource_verbatim": res, "model": model, "meter_type": meter,
            "builder_source": builder, "plain_text": text, "conf": conf}
def elem(label, mode, conf): return {"label_verbatim": label, "damage_mode": mode, "conf": conf}
def mov(verbs, policy, is_move, conf):
    return {"verbs": verbs, "policy_while_casting": policy, "skill_is_movement": is_move, "conf": conf}
def pfx(attr, rng, tempo, amp, proxy, commit):
    return {"attr": attr, "range": rng, "tempo": tempo, "amp": amp, "proxy": proxy, "commitment": commit}

# ── post-cutoff threshold ─────────────────────────────────────────────────────
# ud-s7-2025 = Season 7 (2025) — post-cutoff; conf capped ≤ 0.50
# ud-launch-2022 base kits = pre-cutoff; good confidence
# ud-s11-forge-2026 = post-cutoff ERA but if kit ALSO has ud-launch-2022 anchor,
#   base mechanics are pre-cutoff; flag s11 changes as unknown in mechanics_notes

KITS = []

# ── 1. ud-spread-rapid-dex ───────────────────────────────────────────────────
# Spread Shot + Rapid Shot via Multishot link — DEX ranged kite-archer archetype
# Atlas: DRHFSI = DEX, ranged, high, flat, solo, instant
# launch-2022; prov: pt;gop
KITS.append({
    "kit_id": "ud-spread-rapid-dex",
    "folk_name": "Spread/Rapid Shot Archer (launch baseline)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "DRHFSI-HMDD-SP-PH-~~",
    "delivery": dc("projectile", 0.88, "spread-shot fires multiple simultaneous projectiles per attack; kite-archer pattern in all launch-era guides"),
    "footprint": dc("multi-point", 0.85, "multishot spread hits several targets at range simultaneously"),
    "geo_text": "Ranged projectile volley: multiple arrows fire outward in a spread cone, each independently targeting. Character stays fully mobile — the defining kite-archer pattern.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["dodge"], "dodge", 0.85),
    "economy": econ("mana (6-link spend)", "spend", "n/a", "n/a",
                    "Standard mana spend per attack cast; 6-link slots scale damage/behavior. Rapid Shot high attack speed drains mana at elevated rate.", 0.82),
    "element": elem("physical", "hit", 0.88),
    "movement": mov(["kite", "strafe"], "full-move", False, 0.85),
    "prefix_claims": pfx(
        pc("D", 0.90, "DEX ranged kite-archer; all launch guides specify dexterity scaling"),
        pc("R", 0.90, "bow attack, ranged"),
        pc("H", 0.85, "Rapid Shot high attack frequency"),
        pc("F", 0.80, "flat DPS output per arrow; spread fans out but amplitude per-projectile is consistent"),
        pc("S", 0.82, "solo build; no minion or support function"),
        pc("I", 0.88, "instant attack trigger per cast"),
    ),
    "mechanics_notes": "The 'launch floor' of Undecember: Multishot as a LINK rune attaches to a base attack, multiplying projectile count. Spread Shot + Rapid Shot under the same link set is the beginner-accessible DEX build. Classless system: any character can run this irrespective of STR/INT allocation.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Multishot link rune adds additional projectile count per tier; Rapid Shot scales with attack speed nodes on Zodiac board.",
    "sources_used": ["pt (playthrough video corpus)", "gop (GlassesOfPower guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 2. ud-flamethrower-channel ───────────────────────────────────────────────
# Channeled flame cone caster — INT mid-range, rooted while channeling
# Atlas: IDHFSC = INT, mid, high, flat, solo, channel
# G2 FLAG: TRUE BEAM (channeled directional cone = beam delivery)
# launch-2022; prov: gop;rulib
KITS.append({
    "kit_id": "ud-flamethrower-channel",
    "folk_name": "Flamethrower Channel Caster",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "IDHFSC-RSDG-SP-FI-~~",
    "delivery": dc("beam", 0.83, "channeled flame cone — sustained directional fire spray locked to cast direction; Channeling Enhancement link extends duration"),
    "footprint": dc("cone", 0.80, "flame spreads as widening cone from caster outward; not a narrow lane but a forward arc"),
    "geo_text": "Sustained channeled flame cone: INT caster aims and holds cast, spraying fire in a widening forward arc. Character is rooted while channeling. Channeling Enhancement link rune extends beam duration and damage.",
    "control": ctrl(["burn"], "rider", 0.78),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("mana (channel drain)", "channel", "n/a", "n/a",
                    "Mana drains continuously while channeling; Channeling Enhancement link scales damage but increases drain rate. Must reposition and recast in bursts.", 0.80),
    "element": elem("fire", "hybrid", 0.85),
    "movement": mov(["stand-and-channel"], "rooted", False, 0.85),
    "prefix_claims": pfx(
        pc("I", 0.83, "INT scaling; caster attribute; fire damage scaling"),
        pc("D", 0.80, "mid-range flame cone; not melee contact, not long-range projectile"),
        pc("H", 0.82, "channeled uptime = high tempo throughput while active"),
        pc("F", 0.78, "flat DPS sustained beam — amplitude consistent while channeling"),
        pc("S", 0.80, "solo caster; no proxy defense"),
        pc("C", 0.88, "channel commit; rooted while casting"),
    ),
    "mechanics_notes": "G2 flag: TRUE BEAM delivery — channeled sustained directional spray qualifies as beam (not projectile). Undecember's rune library tags CHANNEL as a first-class category, making this one of the clearest channel archetypes in the corpus. Fire element with burn DoT rider.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Channeling Enhancement link rune tier increases damage multiplier; additional fire link runes add burn stacking.",
    "sources_used": ["gop (GlassesOfPower guide)", "rulib (rune library reference)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 3. ud-toxic-flame ────────────────────────────────────────────────────────
# Poison + fire DoT hybrid — classless cross-element DoT; kite-and-run
# Atlas: DDLFSI = DEX, mid, low, flat, solo, instant
# launch-2022; prov: gop;kb
KITS.append({
    "kit_id": "ud-toxic-flame",
    "folk_name": "Toxic Flame DoT",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "DDLFSI-HSDD-DW-PO-~~",
    "delivery": dc("at-target", 0.82, "cast-and-apply skill; applies poison+fire DoT to target location/enemy on cast"),
    "footprint": dc("small-radius", 0.78, "small AOE splash on application; DoT ticks on affected enemies within zone"),
    "geo_text": "Instant cast applies poison and fire DoT in a small AOE splash. Player walks away while stacks tick down. The hit-and-walk DoT pattern: low cast tempo, high sustained DPS via ticking ailments.",
    "control": ctrl(["poison", "burn"], "core", 0.80),
    "defense": defs(["dodge"], "dodge", 0.82),
    "economy": econ("mana (spend per application)", "spend", "n/a", "n/a",
                    "Single mana spend per cast; DoT damage is free after application — 'hit-and-walk' loop. Drain-while (DW) notation in old vocab refers to DoT drain on enemies, not resource drain.", 0.78),
    "element": elem("poison/fire hybrid", "dot", 0.82),
    "movement": mov(["walk-away", "kite"], "full-move", False, 0.82),
    "prefix_claims": pfx(
        pc("D", 0.82, "DEX build; kite-and-walk pattern; poison scales with dex in Undecember"),
        pc("D", 0.78, "mid-range application; close-enough to apply, far enough to kite"),
        pc("L", 0.82, "low tempo — cast-and-walk; damage from ticks not from cast frequency"),
        pc("F", 0.78, "flat DoT DPS — ailment ticks are consistent amplitude"),
        pc("S", 0.80, "solo build; DoT is entirely self-sufficient"),
        pc("I", 0.85, "instant cast application; no wind-up or channel"),
    ),
    "mechanics_notes": "Classless system poster child: poison (typically DEX) + fire (typically INT) both applied from one skill, available to any stat allocation. Dual-element DoT hybrid. Old vocab DW code refers to DoT drain on enemies, NOT resource drain — captured here as spend economy with DoT rider.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Toxic Flame rune tier increases DoT multiplier; Poison Duration / Fire Duration link runes extend tick windows.",
    "sources_used": ["gop (GlassesOfPower guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 4. ud-illusion-family ────────────────────────────────────────────────────
# Illusion Arrow/Axe/Hook — echo-copy mechanic, DEX light-proxy
# Atlas: DDMFLI = DEX, mid, med, flat, light-proxy, instant
# launch-2022 + s11-2026 anchor; prov: pt;pgm
KITS.append({
    "kit_id": "ud-illusion-family",
    "folk_name": "Illusion Family (Arrow/Axe/Hook)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "DDMFLI-HMDD-SP-PH-~~",
    "delivery": dc("at-target", 0.80, "summons echo-copy illusions at target position; copies mirror player attacks"),
    "footprint": dc("multi-point", 0.78, "multiple illusion copies fight at distinct positions simultaneously"),
    "geo_text": "Illusion copies spawn at target positions and mirror the player's own attacks (Arrow, Axe, or Hook weapon variant). Light-proxy: copies fight alongside player but are fragile echoes, not independent summoned units.",
    "control": ctrl([], "none", 0.75),
    "defense": defs(["dodge"], "dodge", 0.80),
    "economy": econ("mana (echo uptime spend)", "proc", "n/a", "n/a",
                    "Mana spend triggers echo copies; copies persist briefly and proc additional hits. Echo-uptime model — refresh-on-cast.", 0.75),
    "element": elem("physical", "hit", 0.80),
    "movement": mov(["reposition", "kite"], "full-move", False, 0.78),
    "prefix_claims": pfx(
        pc("D", 0.82, "DEX build; illusion runes tied to dex scaling in most guides"),
        pc("D", 0.78, "mid-range; illusions spawn in proximity to target"),
        pc("M", 0.78, "medium tempo; echo refresh on cast; not spammy like rapid shot"),
        pc("F", 0.75, "flat amplitude per illusion copy; consistent echo output"),
        pc("L", 0.80, "light-proxy; illusion copies are fragile echo assists, not full summons"),
        pc("I", 0.82, "instant trigger to spawn illusions"),
    ),
    "mechanics_notes": "Three weapon-type variants (Arrow/Axe/Hook) under the same echo-copy grammar. Notably present in both launch-2022 and s11-forge-2026 eras. S11 (2026) changes unknown — base echo mechanic captured from launch-era provenance; post-cutoff updates not confirmed.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Illusion rune tier increases copy count or damage multiplier; Illusion Duration link extends echo persistence.",
    "sources_used": ["pt (playthrough video corpus)", "pgm (PGMiner/meta site)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 5. ud-ice-crystal-arrow ──────────────────────────────────────────────────
# Ice Crystal Arrow with Chain link — DEX ranged, cold, post-cutoff (ud-s7-2025)
# Atlas: DRHFLI = DEX, ranged, high, flat, light-proxy, instant
# post-cutoff: ud-s7-2025 ONLY (no launch anchor)
KITS.append({
    "kit_id": "ud-ice-crystal-arrow",
    "folk_name": "Ice Crystal Arrow Bow",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "DRHFLI-HCMD-SP-CO-~~",
    "delivery": dc("projectile", 0.45, "ice arrow projectile with chain-bounce on hit; post-cutoff conf capped"),
    "footprint": dc("chain-hop", 0.45, "chain-bounce between enemies (chain link rune effect); NOT a line; post-cutoff conf capped"),
    "geo_text": "Ice arrow fires as a ranged projectile; Chain link rune causes it to bounce between nearby enemies on hit. Clear-speed tool: one arrow can hit several targets via bounce chain. Illusion Arrow layered for additional echo hits.",
    "control": ctrl(["chill", "freeze"], "rider", 0.45),
    "defense": defs(["dodge"], "dodge", 0.45),
    "economy": econ("mana (6-link spend)", "spend", "n/a", "n/a",
                    "Standard 6-link mana spend; Chain is a link rune modifier, not a separate resource cost.", 0.42),
    "element": elem("cold", "hit", 0.45),
    "movement": mov(["kite", "strafe"], "full-move", False, 0.45),
    "prefix_claims": pfx(
        pc("D", 0.45, "DEX ranged bow build; post-cutoff conf capped"),
        pc("R", 0.45, "ranged bow; post-cutoff conf capped"),
        pc("H", 0.42, "high clear speed via chain bounce; post-cutoff conf capped"),
        pc("F", 0.42, "flat per-arrow amplitude; post-cutoff conf capped"),
        pc("L", 0.42, "light-proxy (echo layer from Illusion Arrow); post-cutoff conf capped"),
        pc("I", 0.45, "instant cast; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: ud-s7-2025 is the earliest and only era; all conf capped at ≤0.50. G2: chain-hop, NOT a line/beam — bouncing projectile ≠ directional lane. Illusion Arrow layered as light-proxy echo. Season 7 (2025) meta build.",
    "era_confirmed": "ud-s7-2025",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Ice Crystal Arrow rune tier increases projectile damage; Chain link rune tier increases bounce count.",
    "sources_used": ["pgm (PGMiner/meta site s7 content)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 6. ud-seal-veil-daimonios ────────────────────────────────────────────────
# Seal/Veil reservation build — INT mid, reserve economy, post-cutoff (ud-s7-2025)
# Atlas: IDMFSI = INT, mid, med, flat, solo, instant
KITS.append({
    "kit_id": "ud-seal-veil-daimonios",
    "folk_name": "Seal/Veil Resource Build (Daimonios)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "IDMFSI-MSMM-RS-__-~~",
    "delivery": dc("at-target", 0.42, "Seal skills cast at target; Veil toggle-buffs wrap around; post-cutoff conf capped"),
    "footprint": dc("small-radius", 0.42, "small AOE on Seal casts; Veil buffs are self-origin auras; post-cutoff conf capped"),
    "geo_text": "Many SEAL damage skills stacked with VEIL toggle-reservation buffs sharing a high-level Improved Technique link. Reservation economy: Veil skills reserve mana permanently; Seal skills spend from remaining pool.",
    "control": ctrl([], "none", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("mana (seal-reservation + shared link)", "reserve", "n/a", "n/a",
                    "Veil skills reserve mana as a permanent toggle cost; Improved Technique link shared across Seal skills reduces their individual spend. Dual-layer economy: reservation floor + spend ceiling.", 0.42),
    "element": elem("unknown", "hit", 0.40),
    "movement": mov(["position"], "full-move", False, 0.40),
    "prefix_claims": pfx(
        pc("I", 0.42, "INT scaling per seal/veil mechanics; post-cutoff conf capped"),
        pc("D", 0.42, "mid-range; not melee; post-cutoff conf capped"),
        pc("M", 0.42, "medium tempo reservation build; post-cutoff conf capped"),
        pc("F", 0.40, "flat reserve output; post-cutoff conf capped"),
        pc("S", 0.42, "solo build; reservation economy is self-contained; post-cutoff conf capped"),
        pc("I", 0.42, "instant skill triggers; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: ud-s7-2025 earliest and only era; conf capped ≤0.50. Daimonios archetype — Korean-server term for seal/veil hybrid builds. Element unknown (Seal skills vary by element; build depends on which Seal runes chosen). Reservation economy is the defining mechanic: stacking Veil costs against shared Improved Technique link.",
    "era_confirmed": "ud-s7-2025",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Improved Technique link tier reduces mana reservation cost; Seal rune tier increases damage output.",
    "sources_used": ["pgm (PGMiner/meta site s7 content)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 7. ud-lightning-vortex ───────────────────────────────────────────────────
# Lightning Vortex large-AOE mapper — INT ranged, post-cutoff (ud-s7-2025)
# Atlas: IRHFSI = INT, ranged, high, flat, solo, instant
KITS.append({
    "kit_id": "ud-lightning-vortex",
    "folk_name": "Lightning Vortex Mapper",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "IRHFSI-HLMG-SP-LI-~~",
    "delivery": dc("at-target", 0.45, "cast lightning vortex at target location; large AOE detonation; post-cutoff conf capped"),
    "footprint": dc("large-zone", 0.45, "large AOE zone; clear-speed mapping footprint; post-cutoff conf capped"),
    "geo_text": "Lightning Vortex fires at target location, erupting in a large lightning AOE zone. Season 7 mapping meta build: high clear speed from large-zone coverage. Survivability link lattice wraps around the core vortex rune.",
    "control": ctrl(["shock", "stun"], "rider", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("mana (6-link spend)", "spend", "n/a", "n/a",
                    "Standard 6-link mana spend per cast of Lightning Vortex. High cast frequency for mapping drives elevated mana consumption.", 0.42),
    "element": elem("lightning", "hit", 0.45),
    "movement": mov(["kite", "strafe"], "full-move", False, 0.42),
    "prefix_claims": pfx(
        pc("I", 0.45, "INT scaling; lightning element INT in Undecember; post-cutoff conf capped"),
        pc("R", 0.45, "ranged cast; no melee contact; post-cutoff conf capped"),
        pc("H", 0.42, "high tempo mapping; frequent cast for clear speed; post-cutoff conf capped"),
        pc("F", 0.42, "flat per-cast AOE output; post-cutoff conf capped"),
        pc("S", 0.42, "solo mapping build; no proxy; post-cutoff conf capped"),
        pc("I", 0.45, "instant cast trigger; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: ud-s7-2025 earliest and only era; conf capped ≤0.50. 'The mapping version of the clear-speed caster lane' per mech_note. Shock/stun as riders from lightning. Season 7 (2025) content.",
    "era_confirmed": "ud-s7-2025",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Lightning Vortex tier increases AOE radius and damage; Increased Area link rune further expands zone.",
    "sources_used": ["pgm (PGMiner/meta site s7 content)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 8. ud-summon-strand ──────────────────────────────────────────────────────
# Summoner: Rune Knight + Abyssling — INT ranged, heavy-proxy
# Atlas: IRMFHI = INT, ranged, med, flat, heavy-proxy, instant
# launch-2022; prov: pt;gop;rulib
KITS.append({
    "kit_id": "ud-summon-strand",
    "folk_name": "Summoner (Rune Knight + Abyssling)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "IRMFHI-MNDM-SU-PH-~~",
    "delivery": dc("self-origin", 0.80, "summon Rune Knight and Abyssling minions from caster position on cast"),
    "footprint": dc("small-radius", 0.75, "minions spawn near caster then pursue enemies across zone; summoning footprint is small-radius"),
    "geo_text": "Summon Bursting Rune Knight and Abyssling minions. Minions pursue enemies independently after spawn. Heavy-proxy defense: minions tank and deal damage while caster repositions. Minion HP/Armor link runes reinforce durability.",
    "control": ctrl([], "none", 0.75),
    "defense": defs(["hp-stack", "glass"], "glass", 0.78),
    "economy": econ("mana (summon uptime spend)", "reserve", "n/a", "n/a",
                    "Summoning costs mana per spawn; minions persist without continuous resource drain. Uptime maintained by re-summoning fallen minions. SU notation = summon reserve economy.", 0.78),
    "element": elem("physical", "hit", 0.80),
    "movement": mov(["reposition"], "full-move", False, 0.80),
    "prefix_claims": pfx(
        pc("I", 0.80, "INT scaling for summon damage; INT-primary minion build"),
        pc("R", 0.78, "caster stays at range while minions engage melee"),
        pc("M", 0.80, "medium tempo; occasional re-summon rather than constant casting"),
        pc("F", 0.75, "flat minion DPS output; consistent per-minion damage"),
        pc("H", 0.82, "heavy-proxy; Rune Knight + Abyssling = two distinct minion types tanking for caster"),
        pc("I", 0.80, "instant summon trigger"),
    ),
    "mechanics_notes": "Notably: Abyssling minion is documented in the rune library (rulib provenance) as a named distinct minion type — not a generic summon. 'The classless minion lane' per mech_note. Caster is glass; minions provide all effective defense. Minion HP/Armor links are critical for viability.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Rune Knight / Abyssling rune tiers increase minion stats; Minion HP/Armor link rune tiers add durability.",
    "sources_used": ["pt (playthrough video corpus)", "gop (GlassesOfPower guide)", "rulib (rune library reference)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 9. ud-snowstorm-frost ────────────────────────────────────────────────────
# Snowstorm large-zone frost — INT ranged, med tempo, all-rounder launch default
# Atlas: IRMFSI = INT, ranged, med, flat, solo, instant
# launch-2022; prov: pt;kb
KITS.append({
    "kit_id": "ud-snowstorm-frost",
    "folk_name": "Snowstorm Frost Caster",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "IRMFSI-MLMG-SP-CO-~~",
    "delivery": dc("at-target", 0.82, "Snowstorm cast at target location; large persistent frost zone"),
    "footprint": dc("large-zone", 0.82, "large cold AOE zone persists after cast; enemies in zone take cold damage"),
    "geo_text": "Snowstorm drops a large frost zone at target location. Persistent zone deals cold damage to enemies within. Launch-era all-rounder INT build: Snowstorm for AOE clear with Fireball weaved for burst on single targets.",
    "control": ctrl(["chill", "freeze"], "rider", 0.80),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("mana (6-link spend)", "spend", "n/a", "n/a",
                    "Mana spend per cast of Snowstorm; Fireball weave is a separate mana spend. Standard 6-link scaling architecture.", 0.80),
    "element": elem("cold", "hit", 0.82),
    "movement": mov(["reposition", "kite"], "full-move", False, 0.80),
    "prefix_claims": pfx(
        pc("I", 0.82, "INT scaling; cold element INT in Undecember"),
        pc("R", 0.80, "ranged zone cast; no melee contact"),
        pc("M", 0.80, "medium tempo; not spammy; zone does work between casts"),
        pc("F", 0.78, "flat cold zone DPS; consistent output per zone"),
        pc("S", 0.82, "solo build; no proxy element"),
        pc("I", 0.85, "instant cast; zone appears immediately"),
    ),
    "mechanics_notes": "'The all-rounder INT path the guides recommend before specialization' per mech_note. Cold zone + Fireball weave = hybrid element strategy. Classless: any attribute allocation can run this if INT is sufficient for cold/fire rune scaling.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Snowstorm tier increases zone damage and duration; Increased Area link expands zone footprint.",
    "sources_used": ["pt (playthrough video corpus)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 10. ud-whirlwind-str ────────────────────────────────────────────────────
# STR Whirlwind melee channel — skill IS movement
# Atlas: SMHFSC = STR, melee, high, flat, solo, channel
# launch-2022; prov: od;gop;pt
KITS.append({
    "kit_id": "ud-whirlwind-str",
    "folk_name": "Whirlwind STR Melee (launch baseline)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "SMHFSC-KSDT-SP-PH-~~",
    "delivery": dc("self-origin", 0.88, "spinning AOE around caster while channeling; damage radiates from player body outward"),
    "footprint": dc("small-radius", 0.88, "tight spin radius around caster; classic whirlwind zone"),
    "geo_text": "STR whirlwind channel: player spins continuously, dealing small-radius AOE melee damage around their body while moving freely. Skill IS movement — the spin is the locomotion. Regeneration toggle skills layer in for sustain while channeling.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["armor", "sustain-leech"], "armor", 0.85),
    "economy": econ("mana (channel drain while spinning)", "channel", "n/a", "n/a",
                    "Continuous mana drain while channeling the spin. Regeneration toggle reserves offset drain rate. Classic channel loop: spin > regen toggle > spin.", 0.85),
    "element": elem("physical", "hit", 0.88),
    "movement": mov(["spin-move"], "full-move", True, 0.90),
    "prefix_claims": pfx(
        pc("S", 0.90, "STR scaling; two-hander strength build; pure melee"),
        pc("M", 0.90, "melee contact spin; pure melee range"),
        pc("H", 0.88, "high tempo — continuous channel hits at high frequency"),
        pc("F", 0.85, "flat per-tick spin damage; consistent amplitude"),
        pc("S", 0.85, "solo build; no proxy defense"),
        pc("C", 0.90, "channel commit; continuous spinning = channel"),
    ),
    "mechanics_notes": "Classic whirlwind archetype: skill IS movement (mob=skill-IS-movement per corpus). STR + two-hander path. Launch-era melee default. Regeneration toggle skills used for channel sustain — this is the canonical Undecember sustain-while-channeling pattern.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Whirlwind rune tier increases spin damage; Weapon Skill links add additional hit effects per revolution.",
    "sources_used": ["od (official documentation)", "gop (GlassesOfPower guide)", "pt (playthrough video corpus)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 11. ud-cwc-spin-caster ──────────────────────────────────────────────────
# Cast-while-Channeling Whirlwind → Blizzard trigger — post-cutoff (ud-s7-2025)
# Atlas: SMHFSC = STR, melee, high, flat, solo, channel
KITS.append({
    "kit_id": "ud-cwc-spin-caster",
    "folk_name": "Whirlwind CwC Blizzard (Ya55)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "SMHFSC-KSMT-PC-PH-~~",
    "delivery": dc("self-origin", 0.45, "whirlwind self-origin spin triggers Blizzard proc at target location; post-cutoff conf capped"),
    "footprint": dc("small-radius", 0.42, "spin footprint small-radius; Blizzard triggers expand to large-zone; post-cutoff conf capped"),
    "geo_text": "Whirlwind channel spin triggers 'Spell Activation while Channeling' link, firing Blizzard procs while spinning. Base whirlwind is self-origin small-radius; triggered Blizzard adds large-zone cold AOE. Dual-layer delivery: spin = self-origin, Blizzard = at-target proc.",
    "control": ctrl(["chill", "freeze"], "rider", 0.42),
    "defense": defs(["armor"], "armor", 0.42),
    "economy": econ("mana (channel drain + spell activation link proc)", "proc", "n/a", "on_channel",
                    "Channel drain from whirlwind; 'Spell Activation while Channeling' link procs Blizzard on channel ticks at no additional mana cost. CwC = Cast-while-Channeling.", 0.42),
    "element": elem("physical/cold hybrid", "hybrid", 0.42),
    "movement": mov(["spin-move"], "full-move", True, 0.42),
    "prefix_claims": pfx(
        pc("S", 0.45, "STR base for whirlwind; post-cutoff conf capped"),
        pc("M", 0.45, "melee spin base; post-cutoff conf capped"),
        pc("H", 0.42, "high channel tempo; post-cutoff conf capped"),
        pc("F", 0.42, "flat spin amplitude; post-cutoff conf capped"),
        pc("S", 0.42, "solo; post-cutoff conf capped"),
        pc("C", 0.45, "channel commit; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: ud-s7-2025 earliest and only era; conf capped ≤0.50. CwC pattern: 'Spell Activation while Channeling' link is Undecember's Cast-while-Channeling rune (PoE analog = Cast while Channelling support). Economy=proc (PC) from old vocab. Notable build tag: Ya55 (season 7 meta creator). Dual delivery: self-origin (spin) + triggered at-target (Blizzard).",
    "era_confirmed": "ud-s7-2025",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Spell Activation while Channeling link tier increases proc frequency; Blizzard tier increases triggered AOE damage.",
    "sources_used": ["pgm (PGMiner/meta site s7 content)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 12. ud-multishot-link ────────────────────────────────────────────────────
# Multishot as Link Rune — support grammar record (classless system meta)
# Atlas: _R_F__ = unknown attr, ranged, unknown, flat, unknown, unknown
# launch-2022 + s11-2026; prov: pt;gop
KITS.append({
    "kit_id": "ud-multishot-link",
    "folk_name": "Multishot (as LINK rune)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "_R_F__-_M__-SP-__-~~",
    "delivery": dc("projectile", 0.72, "link rune that multiplies projectile count on host skill; delivery inherited from host skill"),
    "footprint": dc("multi-point", 0.72, "adds multi-directional projectile spread to any compatible ranged skill"),
    "geo_text": "Multishot is a Link Rune (support) — it attaches to a Skill Rune and multiplies the projectile count. The GMP (Greater Multiple Projectiles) analog in Undecember. Delivery and footprint are inherited from the host skill; Multishot modifies quantity, not type.",
    "control": ctrl([], "none", 0.70),
    "defense": defs(["other"], "other", 0.70),
    "economy": econ("support-grammar-portable", "other", "n/a", "n/a",
                    "Multishot is a link rune — no independent mana cost. Host skill's economy absorbs the link rune cost. Portable across any compatible skill rune.", 0.70),
    "element": elem("n/a (host skill element)", "hit", 0.70),
    "movement": mov([], "full-move", False, 0.70),
    "prefix_claims": pfx(
        pc("_", 0.50, "classless; attribute blank in atlas (any attr can use)"),
        pc("R", 0.72, "ranged skill modifier; applies to ranged skill runes only"),
        pc("_", 0.50, "tempo blank; depends on host skill"),
        pc("F", 0.72, "flat projectile count addition; GMP-analog"),
        pc("_", 0.50, "proxy blank; classless, could be any proxy tier"),
        pc("_", 0.50, "commit blank; inherits from host skill"),
    ),
    "mechanics_notes": "System-structural record: documents that projectile multiplication in Undecember ships as a LINK rune, not a skill rune. This is the GMP analog. Era span: launch-2022 through s11-forge-2026; s11 changes unknown. Capture preserves the classless link-rune grammar distinction.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Multishot link tier increases added projectile count.",
    "sources_used": ["pt (playthrough video corpus)", "gop (GlassesOfPower guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 13. ud-zodiac-board ─────────────────────────────────────────────────────
# Zodiac Constellation Board — passive progression meta-system
# Atlas: ______  (blank = meta-system record)
# launch-2022 + s11-2026; prov: od;pgm
KITS.append({
    "kit_id": "ud-zodiac-board",
    "folk_name": "Zodiac Constellation Board",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "______-____-SP-__-~~",
    "delivery": dc("other", 0.72, "meta-system record; passive board is not a castable skill"),
    "footprint": dc("other", 0.72, "meta-system record; no spatial footprint"),
    "geo_text": "The passive constellation lattice: attribute-core nodes radiate into skill-type constellations with stat modifier nodes throughout. The 'big-board grammar' (PoE passive tree / Grim Dawn constellation system analog) for Undecember.",
    "control": ctrl([], "none", 0.70),
    "defense": defs(["other"], "other", 0.70),
    "economy": econ("big-board-passives", "other", "n/a", "n/a",
                    "Passive point allocation into constellation nodes; no active resource cost. Board is the stat scaffolding for all active builds.", 0.70),
    "element": elem("n/a", "hit", 0.65),
    "movement": mov([], "full-move", False, 0.65),
    "prefix_claims": pfx(
        pc("_", 0.50, "meta-system; no attr"),
        pc("_", 0.50, "meta-system; no range"),
        pc("_", 0.50, "meta-system; no tempo"),
        pc("_", 0.50, "meta-system; no amp"),
        pc("_", 0.50, "meta-system; no proxy"),
        pc("_", 0.50, "meta-system; no commit"),
    ),
    "mechanics_notes": "Structural/meta-system record. Zodiac Board = Undecember's passive tree equivalent. Classless architecture means the board has no class-gated zones — any node accessible with sufficient passive points. Era span: launch through s11-2026; board likely evolved across seasons.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "n/a (passive board, not a rankable rune)",
    "sources_used": ["od (official documentation)", "pgm (PGMiner/meta site)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 14. ud-chaos-dungeon-ladder ─────────────────────────────────────────────
# Chaos Dungeon / Arena endgame ladder — numeric spine record
# Atlas: ______ (blank)
# launch-2022 + s11-2026; prov: udn;kb
KITS.append({
    "kit_id": "ud-chaos-dungeon-ladder",
    "folk_name": "Chaos Dungeon / Arena ladder (numeric spine)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "______-____-SP-__-~~",
    "delivery": dc("other", 0.68, "meta-system record; endgame content structure, not a castable skill"),
    "footprint": dc("other", 0.68, "meta-system record; no spatial footprint"),
    "geo_text": "Chaos Dungeon = depth-stratified endgame PvE content (165+ monster level range cited in patch notes). Eunos Dungeons, Constellation of Time, and Arena are the ladder spine. Korean-stratified ladder grammar: numeric depth as the power ceiling signal.",
    "control": ctrl([], "none", 0.65),
    "defense": defs(["other"], "other", 0.65),
    "economy": econ("kr-stratified-ladder", "other", "n/a", "n/a",
                    "Endgame content economy: enter with keys/entries; push depth for better rewards. Numeric depth as power-ceiling signal.", 0.65),
    "element": elem("n/a", "hit", 0.62),
    "movement": mov([], "full-move", False, 0.62),
    "prefix_claims": pfx(
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
    ),
    "mechanics_notes": "Structural record: numeric-depth ladder as endgame spine. Korean ARPG grammar common to Undecember, Lost Ark, etc. Endgame currency: Chaos Dungeon keys. Era span: launch through s11-2026.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "n/a (endgame structure, not a skill)",
    "sources_used": ["udn (undecember news/patch notes)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 15. ud-gear-enchant-economy ─────────────────────────────────────────────
# Enchant/Disassemble gear economy — DR (disassemble-reroll) meta-system
# Atlas: ______ + DR economy code
# launch-2022 + s11-2026; prov: od
KITS.append({
    "kit_id": "ud-gear-enchant-economy",
    "folk_name": "Enchant/Disassemble Gear Economy",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "______-____-DR-__-~~",
    "delivery": dc("other", 0.70, "meta-system record; gear economy, not a castable skill"),
    "footprint": dc("other", 0.70, "meta-system record; no spatial footprint"),
    "geo_text": "Freely re-roll equipment stats, bonuses, and grades through enchanting, fueled by disassembling other gear. Deterministic-leaning crafting grammar: player controls reroll by choosing which stats to retain or reroll with rune materials.",
    "control": ctrl([], "none", 0.68),
    "defense": defs(["other"], "other", 0.68),
    "economy": econ("material-fueled-reroll (DR)", "recipe", "n/a", "n/a",
                    "DR = disassemble-reroll. Gear is disassembled for enchanting materials; materials fuel stat re-roll on target equipment. Deterministic-leaning: retain desired stats, reroll undesired ones.", 0.70),
    "element": elem("n/a", "hit", 0.65),
    "movement": mov([], "full-move", False, 0.65),
    "prefix_claims": pfx(
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
    ),
    "mechanics_notes": "DR economy code in old atlas = disassemble-reroll. Gear economy distinct from skill economy. Undecember's deterministic-leaning crafting stands in contrast to PoE1's chaotic-currency randomness. Era span: launch through s11-2026.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "n/a (economy system, not a skill)",
    "sources_used": ["od (official documentation)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 16. ud-classless-triad ──────────────────────────────────────────────────
# Classless STR/DEX/INT Triad — pure emergent authorship system record
# Atlas: ______ (blank)
# launch-2022 + s11-2026; prov: od;kb
KITS.append({
    "kit_id": "ud-classless-triad",
    "folk_name": "Classless STR/DEX/INT Triad",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "______-____-SP-__-~~",
    "delivery": dc("other", 0.75, "meta-system record; documents classless build grammar"),
    "footprint": dc("other", 0.75, "meta-system record; no spatial footprint"),
    "geo_text": "No classes in Undecember: STR/DEX/INT are gravity wells, not walls. 'Cast magic with a sword or summon minions with a bow' — pure emergent authorship. All Skill Runes and Link Runes accessible regardless of stat allocation; stat requirements gate power, not access.",
    "control": ctrl([], "none", 0.72),
    "defense": defs(["other"], "other", 0.72),
    "economy": econ("pure-emergent-authorship", "other", "n/a", "n/a",
                    "No class-gated economy; any rune combination is legal. STR/DEX/INT stat investment shapes efficiency but not access.", 0.72),
    "element": elem("n/a", "hit", 0.70),
    "movement": mov([], "full-move", False, 0.70),
    "prefix_claims": pfx(
        pc("_", 0.50, "meta-system; no attr lock"), pc("_", 0.50, "meta-system"),
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
        pc("_", 0.50, "meta-system"), pc("_", 0.50, "meta-system"),
    ),
    "mechanics_notes": "Core distinguishing system of Undecember vs class-based ARPGs. Documents the three-gravity-well design. This is what enables the Toxic Flame cross-element DoT on any character. Era span: launch through s11-2026; fundamental system unchanged across seasons.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "n/a (system record, not a skill)",
    "sources_used": ["od (official documentation)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 17. ud-link-rune-grammar ────────────────────────────────────────────────
# Link-Rune Grammar — convergence-test record; 6-link ceiling; TAG-GATED links
# Atlas: ______ (blank); convergence-test record
# launch-2022 + s11-2026; prov: od;ytud;rulib
KITS.append({
    "kit_id": "ud-link-rune-grammar",
    "folk_name": "Link-Rune Grammar (the convergence-test record)",
    "game": "undecember",
    "status": "positive",
    "atlas_key": "______-____-SP-__-~~",
    "delivery": dc("other", 0.78, "meta-system convergence-test record; documents link-rune grammar not a castable skill"),
    "footprint": dc("other", 0.78, "meta-system; no spatial footprint"),
    "geo_text": "Every Skill Rune accepts up to SIX Link Runes — the 6-link ceiling verbatim. Links are TAG-GATED: links only slot into skills whose tags match (e.g., 'Channel' links only work on channeling skills). Hex-edge color-matching makes the system visual. PoE 6-link socket analog with tag gating instead of color gating.",
    "control": ctrl([], "none", 0.75),
    "defense": defs(["other"], "other", 0.75),
    "economy": econ("support-grammar-portable", "other", "n/a", "n/a",
                    "Link runes have no independent resource cost; they modify their host skill's behavior within that skill's existing economy. Portable: same link rune can slot into any compatible skill rune.", 0.75),
    "element": elem("n/a", "hit", 0.72),
    "movement": mov([], "full-move", False, 0.72),
    "prefix_claims": pfx(
        pc("_", 0.50, "convergence-test; no attr"), pc("_", 0.50, "convergence-test"),
        pc("_", 0.50, "convergence-test"), pc("_", 0.50, "convergence-test"),
        pc("_", 0.50, "convergence-test"), pc("_", 0.50, "convergence-test"),
    ),
    "mechanics_notes": "CONVERGENCE-TEST RECORD: this record documents the link-rune grammar as an explicit join test — 'does the 6-link TAG-GATED socket grammar map onto our engine's modifier scaffold?' PoE 6-link = socket color+count; Undecember = tag matching + 6 slots. Tag-gating is the convergence differentiator. Era: launch through s11-2026.",
    "era_confirmed": "ud-launch-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "n/a (system grammar record, not a skill)",
    "sources_used": ["od (official documentation)", "ytud (YouTube Undecember content)", "rulib (rune library reference)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── output ────────────────────────────────────────────────────────────────────
pos  = [k for k in KITS if k["status"] == "positive"]
neg  = [k for k in KITS if k["status"] == "negative"]
pct  = [k for k in KITS if k.get("post_cutoff")]

with OUT.open("w") as f:
    for k in KITS:
        f.write(json.dumps(k) + "\n")

print(f"Undecember: {len(KITS)} records | pos={len(pos)} neg={len(neg)} post-cutoff={len(pct)}")
print(f"Written: {OUT}")

print("\n=== DIRECTED SWEEP RESULTS (Undecember) ===")
print("C2 (support-existence): NO pure-support kit in Undecember corpus.")
print("  Classless system has no dedicated support role; all builds center on personal damage output.")
print("G2 (line-vs-projectile):")
print("  TRUE BEAM: ud-flamethrower-channel (channeled flame cone → delivery=beam, footprint=cone)")
print("  Chain-hop NOT line: ud-ice-crystal-arrow (Chain link rune = bounce, not directional lane)")
print("  No true lane/line kits otherwise.")
print("D1 (shield-split):")
print("  DODGE: ud-spread-rapid-dex, ud-toxic-flame, ud-illusion-family, ud-ice-crystal-arrow (DEX builds)")
print("  GLASS: ud-flamethrower-channel, ud-snowstorm-frost, ud-lightning-vortex (INT casters)")
print("  ARMOR: ud-whirlwind-str, ud-cwc-spin-caster (STR melee)")
print("  HEAVY-PROXY: ud-summon-strand (minions tank)")
print("  RESERVE (toggle mitigation): ud-seal-veil-daimonios (Veil reserve buffs)")
print("  No block or shield-absorb kits in Undecember corpus.")
print("POST-CUTOFF roster (ud-s7-2025 earliest era — all 4 kits):")
for k in pct:
    print(f"  {k['kit_id']} | {k['folk_name']}")
