#!/usr/bin/env python3
"""
Cycle 13 Character Analysis HTML Generator

Reads the 16 character JSONs + 16 gear_set JSONs from
reincarnated-engine/output/cycle-13-mechanical-season-001/ and produces a
comprehensive HTML analysis doc at:
agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-character-analysis.html

Purpose: gold-standard cross-reference for drax loadout app implementation.
HTML doc sources from JSON (authoritative); drax loadout page sources from DB.
Matt compares both views to verify drax integration faithfulness.

Author: gandalf (story-and-design steward)
Date: 2026-05-27
"""

import json
from pathlib import Path
from collections import Counter
from html import escape

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SEASON_DIR = Path("/Users/admin/Games/reincarnated-engine/output/cycle-13-mechanical-season-001")
OUTPUT_PATH = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-character-analysis.html")

CHARACTER_FILES = sorted((SEASON_DIR / "characters").glob("*.json"))
GEAR_SET_FILES = sorted((SEASON_DIR / "gear_sets").glob("*.json"))
SEASON_METADATA = json.loads((SEASON_DIR / "season_metadata.json").read_text())
QUALITY_REPORT = json.loads((SEASON_DIR / "sim_cycling_quality_report.json").read_text())

# Gauntlet sim results from Track A remediation (commit b90b371 + W2 canonical-path fix 37f6fff)
GAUNTLET_RESULTS_PATH = Path("/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json")
GAUNTLET_RESULTS = (
    json.loads(GAUNTLET_RESULTS_PATH.read_text())
    if GAUNTLET_RESULTS_PATH.exists()
    else None
)

CHARACTERS = [json.loads(p.read_text()) for p in CHARACTER_FILES]
GEAR_SETS = {
    p.stem.replace("_gear_full", ""): json.loads(p.read_text())
    for p in GEAR_SET_FILES
}

# Index gauntlet results by character_id (kit_results use legendary_id which contains character cell)
GAUNTLET_KIT_BY_CHAR = {}
GAUNTLET_ENCOUNTERS_BY_CHAR = {}
if GAUNTLET_RESULTS:
    for kit in GAUNTLET_RESULTS.get("kit_results", []):
        leg_id = kit.get("legendary_id", "")
        # legendary_id like "endgame_dex_01_dagger_assassin_T4"
        cid = "S1_" + leg_id.rsplit("_T4", 1)[0] if "_T4" in leg_id else None
        if cid:
            GAUNTLET_KIT_BY_CHAR[cid] = kit
    for enc in GAUNTLET_RESULTS.get("encounter_results", []):
        leg_id = enc.get("legendary_id", "")
        cid = "S1_" + leg_id.rsplit("_T4", 1)[0] if "_T4" in leg_id else None
        if cid:
            GAUNTLET_ENCOUNTERS_BY_CHAR.setdefault(cid, []).append(enc)

# ---------------------------------------------------------------------------
# Gandalf analysis text per character (mechanical / playability / thematic)
# ---------------------------------------------------------------------------

# Per-character analysis dictionary keyed by character_id.
# Each entry: mechanical, playability, thematic, cohesion observations.
# Drawn from JSON data + design-fit interpretation.

GANDALF_ANALYSIS = {
    "S1_endgame_str_01_heavy_barbarian": {
        "mechanical": (
            "STR/melee/spiky-amplitude/cooldown with earth-element identity. T4 Category A "
            "DEFENSIVE_CONVERSION × Category C ELEMENT_CONVERSION character-wide scope means "
            "this build trades defensive posture for elemental-conversion impact across all "
            "skills. Net synergy 10 is positive but thin; resolve_score 72 indicates the "
            "kit has tensions for the T4 to resolve, create_score 62 indicates the conversion "
            "creates new tensions (likely defensive opportunity cost). 3-chain class with "
            "2 T4 chains + 1 supporting — concentrated identity."
        ),
        "playability": (
            "Cooldown-driven melee with spiky amplitude implies burst rotation: big-hit cooldown "
            "skills with character-wide elemental conversion amplifying each. Dps_min_maxer cohort "
            "expects 110-130% of KPM target; the spiky pattern suggests gameplay alternates between "
            "high-damage burst windows and cooldown-pacing pauses. Defense uptime will be the gate "
            "here — DEFENSIVE_CONVERSION may push defense below the 60-70% floor dps_min_maxer "
            "tolerates."
        ),
        "thematic": (
            "Earth-aligned barbarian with thorny_on_hit triggered passive (15% weapon damage as "
            "thorns) reads as a stone-skinned berserker — defensive sacrifice for elemental "
            "vengeance. T4 'earth_t4_chain_1' attunement on the main weapon is mechanically and "
            "narratively legible: the heavy weapon IS the conduit for the earth-elemental "
            "conversion. Legendary T1 across all 11 slots is appropriate endgame baseline."
        ),
    },
    "S1_endgame_str_02_light_fighter": {
        "mechanical": "Faster STR melee variant; less spiky amplitude tolerance; balanced cohort more likely viable.",
        "playability": "Sustained-attack rotation more compatible with balanced cohort's 95-105% KPM band.",
        "thematic": "Light fighter reads as agile-but-mortal warrior; element/T4 should reinforce skill-shot identity.",
    },
    "S1_endgame_str_03_polearm_soldier": {
        "mechanical": "Reach + melee STR with polearm geometry; control density likely elevated.",
        "playability": "Polearm timing typically slow + deliberate; balanced cohort fit; rotation pacing matters.",
        "thematic": "Soldier discipline cohort: organized, formation-aware; T4 should resonate with martial pattern.",
    },
    "S1_endgame_dex_01_dagger_assassin": {
        "mechanical": "DEX/melee/dagger with assassin identity; expects high crit + speed; tempo likely high; dps_min_maxer fit natural.",
        "playability": "Combo-building rotation; dagger-strike speed; crit-driven burst windows; resource flow critical.",
        "thematic": "Shadow-themed; rogue archetype; legendary content should evoke assassin folklore (poisoned blade, vanish).",
    },
    "S1_endgame_dex_02_archer": {
        "mechanical": "DEX/ranged/archer; tempo varies (longbow slow + heavy vs shortbow fast); positioning matters.",
        "playability": "Kiting + positioning rotation; defense uptime via mobility, not armor.",
        "thematic": "Classical ranger archetype; bow + arrow + wilderness; element/T4 should compose with elemental-arrow tradition.",
    },
    "S1_endgame_dex_03_crossbow_sniper": {
        "mechanical": "DEX/ranged/crossbow with sniper identity; expect high amplitude/low tempo (heavy shots).",
        "playability": "Reload-pacing rotation; cover-based positioning; dps_min_maxer fit if amplitude justifies.",
        "thematic": "Mechanical-precision identity; crossbow tradition (medieval/Renaissance precedent); T4 should resonate with mechanism + precision.",
    },
    "S1_endgame_dex_04_twin_blade_fencer": {
        "mechanical": "DEX/melee/dual-wield; rapid striking; combo-building viable; dps_min_maxer or balanced fit.",
        "playability": "Twin-strike rhythm; energy/combo-resource model likely; defense via dodge not armor.",
        "thematic": "Duelist archetype; fencing precision + flourish; pair-blade traditions (eastern + western both rich).",
    },
    "S1_endgame_int_01_standard_wizard": {
        "mechanical": "INT/caster/standard wizard; mana resource model; cooldown-managed burst likely.",
        "playability": "Cast-time + cooldown rotation; mana economy gates rotation pacing; balanced cohort fit.",
        "thematic": "Quintessential wizard archetype; element-aligned T4 expression; spellbook + staff tradition.",
    },
    "S1_endgame_int_03_pyromantic_caster": {
        "mechanical": "INT/caster/fire-specialized; expect element=fire; T4 likely ELEMENT_CONVERSION or DUAL_ELEMENT_ADDITION reinforcing fire identity.",
        "playability": "Fire-focused rotation; burn DoT layering likely; sustained pressure cohort fit.",
        "thematic": "Pyromancer archetype; fire-mage tradition (Mushoku Tensei pyromancy precedent); flame-bearing legendaries.",
    },
    "S1_endgame_int_04_red_mage_spellsword": {
        "mechanical": "INT/hybrid/red mage spellsword; cross-attribute hybrid cell (Option C per substrate composition); ω-penalty applies.",
        "playability": "Spell + sword alternation; resource model likely hybrid (mana + stamina); rotation complexity elevated.",
        "thematic": "Red Mage / Spellsword tradition (FF6/Magic Knight lineage); legendary should reinforce dual identity.",
    },
    "S1_endgame_int_05_arcane_familiar_mage": {
        "mechanical": "INT/caster/familiar-summoner; proxy density may be elevated (familiar as proxy); damage geometry varies.",
        "playability": "Familiar control + spell layering; resource economy supports multi-actor pattern.",
        "thematic": "Summoner-bond archetype; arcane familiar (cat / owl / serpent traditions); legendary should evoke binding/pact.",
    },
    "S1_endgame_wis_01_channeling_cleric": {
        "mechanical": "WIS/caster/channeling; channeled resource model; sustained-beam damage geometry likely.",
        "playability": "Channeling rotation; resource depletes over channel; positioning matters (channeled = stationary).",
        "thematic": "Devout cleric tradition; holy/divine element; channeled prayer/grace mechanism; legendary should evoke sanctity.",
    },
    "S1_endgame_wis_02_holy_knight": {
        "mechanical": "WIS/hybrid/holy knight; cross-attribute hybrid (Option C); melee + faith-casting.",
        "playability": "Melee strike + faith-skill alternation; defense uptime should be high; balanced or defensive cohort.",
        "thematic": "Paladin/holy knight tradition (FF Cecil precedent); divine + martial fusion; legendary should be sacred-blade.",
    },
    "S1_endgame_wis_03_ritual_mage": {
        "mechanical": "WIS/caster/ritual; pre-cast preparation; high amplitude/low tempo likely.",
        "playability": "Ritual-prep rotation; setup-then-execute pattern; defense uptime during setup matters.",
        "thematic": "Ritual-magic tradition (Fate Grand Order Caster precedent); circles + sigils + invocations; legendary should be ritual focus.",
    },
    "S1_endgame_wis_04_storm_caller": {
        "mechanical": "WIS/caster/storm; lightning element likely; AoE damage geometry; tempo high.",
        "playability": "Chain-lightning + storm-AoE rotation; positioning for AoE optimal; resource economy active.",
        "thematic": "Storm-shaman / weather-caller tradition; thunder gods + lightning legends; legendary should evoke storm-binding.",
    },
    "S1_endgame_wis_05_monk": {
        "mechanical": "WIS/hybrid/monk; cross-attribute hybrid; energy/combo resource model likely; martial + spiritual.",
        "playability": "Combo-building strike rotation; spiritual ki resource; dps_min_maxer or balanced fit.",
        "thematic": "Monk tradition (D&D monk, FF White Mage/Monk hybrid, eastern martial-arts); legendary should evoke spiritual focus + martial mastery.",
    },
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def short_name(character_id: str) -> str:
    """Extract short display name from character_id."""
    return character_id.replace("S1_endgame_", "").replace("_", " ").title()

def format_modifier(m: dict) -> str:
    cat = m.get("category", "")
    mid = m.get("modifier_id", "")
    mag = m.get("magnitude", 0.0)
    pol = m.get("modifier_polarity", "")
    tier = m.get("tier_restriction", "none")
    tier_str = f" <em>[{tier}]</em>" if tier != "none" else ""
    return f"<code>{escape(mid)}</code> ({cat}, {pol}, mag={mag:.3f}){tier_str}"

def format_capability(c: dict) -> str:
    return f"<code>{escape(c.get('modifier_id', ''))}</code> ({c.get('capability_category', '')})"

def format_triggered_passive(t: dict) -> str:
    if not t:
        return "<em>none</em>"
    desc = escape(t.get("description", ""))
    pid = escape(t.get("pattern_id", ""))
    is_active = "TRUE-ACTIVE" if t.get("is_true_active") else "passive"
    prob = t.get("probability_at_rarity", 0.0)
    return f"<strong>{pid}</strong> ({is_active}, p={prob}): {desc}"

# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

STYLE = """
:root {
  --bg: #1a1a2e;
  --bg2: #16213e;
  --bg3: #0f3460;
  --fg: #eaeaea;
  --fg-muted: #a0a0b0;
  --accent: #e94560;
  --accent2: #f5b800;
  --accent3: #44a08d;
  --border: #2d3754;
  --legendary: #ff8c00;
  --epic: #a335ee;
  --rare: #0070dd;
  --uncommon: #1eff00;
  --common: #ffffff;
}
* { box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}
.container { max-width: 1400px; margin: 0 auto; padding: 24px; }
h1, h2, h3, h4 {
  color: var(--accent2);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
  margin-top: 32px;
}
h1 { font-size: 2.5em; color: var(--accent); border-bottom: 3px solid var(--accent); }
h2 { font-size: 1.8em; }
h3 { font-size: 1.4em; color: var(--accent3); }
h4 { font-size: 1.1em; color: var(--fg); border-bottom: 1px dashed var(--border); }
.tldr { background: var(--bg2); padding: 20px; border-left: 4px solid var(--accent); border-radius: 4px; margin: 16px 0; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; background: var(--bg2); }
th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.92em; }
th { background: var(--bg3); color: var(--accent2); font-weight: 600; }
tr:hover { background: var(--bg3); }
.character-section {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  margin: 24px 0;
}
.id-card { background: var(--bg3); padding: 12px 16px; border-radius: 6px; margin-bottom: 16px; }
.id-card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
.id-card-grid div { padding: 4px 0; }
.id-card-grid strong { color: var(--accent2); display: block; font-size: 0.85em; }
.chain-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 12px 0; }
.chain {
  background: var(--bg3);
  padding: 12px;
  border-radius: 6px;
  border-left: 3px solid var(--accent3);
}
.chain.t4-chain { border-left-color: var(--accent); }
.chain.supporting { border-left-color: var(--fg-muted); opacity: 0.85; }
.chain h5 { margin: 0 0 8px 0; color: var(--accent2); font-size: 1em; }
.t4-detail {
  background: rgba(245, 184, 0, 0.08);
  border: 1px solid var(--accent2);
  border-radius: 6px;
  padding: 14px;
  margin: 12px 0;
}
.t4-detail h5 { color: var(--accent2); margin: 0 0 8px 0; }
.scope-projection { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin: 8px 0; font-size: 0.88em; }
.scope-projection div { background: var(--bg); padding: 6px 8px; border-radius: 4px; }
.scope-projection .selected { background: rgba(233, 69, 96, 0.15); border: 1px solid var(--accent); }
.gear-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin: 12px 0; }
.gear-slot {
  background: var(--bg3);
  padding: 12px;
  border-radius: 6px;
  border-top: 3px solid var(--legendary);
  font-size: 0.88em;
}
.gear-slot h5 { margin: 0 0 6px 0; color: var(--accent2); font-size: 0.95em; }
.gear-slot .rarity { font-weight: bold; color: var(--legendary); font-size: 0.85em; margin-bottom: 4px; }
.gear-slot ul { margin: 4px 0; padding-left: 20px; }
.gear-slot li { margin: 2px 0; font-size: 0.82em; }
.gandalf-analysis {
  background: rgba(68, 160, 141, 0.08);
  border-left: 3px solid var(--accent3);
  padding: 14px 18px;
  border-radius: 4px;
  margin: 16px 0;
}
.gandalf-analysis h5 { color: var(--accent3); margin: 0 0 6px 0; }
.gandalf-analysis p { margin: 6px 0; }
code { background: rgba(0,0,0,0.3); padding: 1px 5px; border-radius: 3px; font-size: 0.88em; color: var(--accent2); }
em { color: var(--fg-muted); }
.metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 8px; margin: 12px 0; }
.metric { background: var(--bg3); padding: 10px; border-radius: 4px; text-align: center; }
.metric .label { font-size: 0.75em; color: var(--fg-muted); text-transform: uppercase; }
.metric .value { font-size: 1.4em; font-weight: bold; color: var(--accent2); }
.warning { background: rgba(233, 69, 96, 0.15); border-left: 3px solid var(--accent); padding: 12px 16px; border-radius: 4px; margin: 12px 0; }
.warning strong { color: var(--accent); }
.toc { background: var(--bg2); padding: 16px; border-radius: 6px; margin: 16px 0; }
.toc ol { columns: 2; column-gap: 24px; margin: 0; padding-left: 24px; }
.toc a { color: var(--accent3); text-decoration: none; }
.toc a:hover { color: var(--accent2); text-decoration: underline; }
.footer { text-align: center; padding: 24px; color: var(--fg-muted); font-size: 0.85em; border-top: 1px solid var(--border); margin-top: 48px; }
"""

def render_id_card(char: dict) -> str:
    bc = char["bc_tuple"]
    chain = char["chain_composition"]
    return f"""
    <div class="id-card">
      <div class="id-card-grid">
        <div><strong>Character ID</strong><code>{escape(char['character_id'])}</code></div>
        <div><strong>BC Cell</strong>{escape(char['bc_cell_id'])}</div>
        <div><strong>Element</strong>{escape(char['element'])}</div>
        <div><strong>Resource Model</strong>{escape(char['resource_model'])}</div>
        <div><strong>Cohort</strong>{escape(char['cohort_archetype'])}</div>
        <div><strong>Class Chain Count</strong>{char['class_chain_count']}</div>
        <div><strong>BC Range</strong>{escape(bc['range'])}</div>
        <div><strong>BC Tempo</strong>{escape(bc['tempo'])}</div>
        <div><strong>BC Amplitude</strong>{escape(bc['amplitude'])}</div>
        <div><strong>BC Attribute</strong>{escape(bc['attribute'])}</div>
        <div><strong>BC Proxy Density</strong>{escape(bc['proxy_density'])}</div>
        <div><strong>Chain Composition</strong>{chain['t4_chains']} T4-chains + {chain['supporting_chains']} supporting</div>
      </div>
    </div>
    """

def render_t4_section(char: dict) -> str:
    """Render T4 candidate(s) + scope projection."""
    if not char["t4_candidates"]:
        return "<p><em>No T4 candidates.</em></p>"

    parts = []
    for t4 in char["t4_candidates"]:
        cat_bc = t4["t4_category_bc"]
        if cat_bc == "C":
            cat_bc_label = "Category C — Chain element conversion / addition"
        elif cat_bc == "B":
            cat_bc_label = "Category B — Chain multiplicative event"
        else:
            cat_bc_label = f"Category {cat_bc}"

        scope_data = t4.get("scope_projection_data", {})
        active_scope = t4.get("t4_scope", "")

        scope_html = "<div class='scope-projection'>"
        for sname in ["character_wide", "chain_wide_own", "chain_wide_parallel"]:
            sd = scope_data.get(sname, {})
            sel = " selected" if sname == active_scope else ""
            label = sname.replace("_", " ").title()
            scope_html += (
                f"<div class='{sel.strip()}'><strong>{label}</strong><br>"
                f"weighted: {sd.get('weighted_score', 0):.2f}<br>"
                f"net synergy: {sd.get('net_synergy_score', 0):.2f}<br>"
                f"prior: {sd.get('prior_weight', 0):.2f}</div>"
            )
        scope_html += "</div>"

        parts.append(f"""
        <div class="t4-detail">
          <h5>T4 Candidate: <code>{escape(t4['candidate_id'])}</code></h5>
          <p><strong>Category A (character-wide):</strong> <code>{t4['category_a_strategy']}</code></p>
          <p><strong>{cat_bc_label}:</strong> <code>{t4['category_bc_strategy']}</code>
              {f"(secondary element: <code>{escape(str(t4['secondary_element']))}</code>)" if t4.get('secondary_element') else ""}</p>
          <p><strong>Parallel-chain mode:</strong> <code>{t4['parallel_chain_mode']}</code></p>
          <p><strong>Active scope:</strong> <code>{active_scope}</code></p>
          <div class="metric-grid">
            <div class="metric"><div class="label">Resolve Score</div><div class="value">{t4['resolve_score']:.1f}</div></div>
            <div class="metric"><div class="label">Create Score</div><div class="value">{t4['create_score']:.1f}</div></div>
            <div class="metric"><div class="label">Net Synergy</div><div class="value">{t4['net_synergy_score']:.1f}</div></div>
            <div class="metric"><div class="label">Separability</div><div class="value">{"PASS" if t4['separability_pass'] else "FAIL"}</div></div>
          </div>
          <h6>Scope Projection (weighted_score per scope option)</h6>
          {scope_html}
          {f"<p class='warning'><strong>Pattern 9 WARN active.</strong></p>" if t4.get('pattern_9_warn') else ""}
          {f"<p class='warning'><strong>Pattern 10 WARN active.</strong></p>" if t4.get('pattern_10_warn') else ""}
        </div>
        """)
    return "\n".join(parts)

def render_gear_slot(slot_name: str, gear: dict) -> str:
    mods_html = "<ul>" + "".join(f"<li>{format_modifier(m)}</li>" for m in gear.get("partition_modifiers", [])) + "</ul>"
    caps_html = "<ul>" + "".join(f"<li>{format_capability(c)}</li>" for c in gear.get("capability_modifiers", [])) + "</ul>"
    t4_ann = gear.get("t4_annotation") or {}
    t4_ann_html = ""
    if t4_ann:
        t4_ann_html = f"<p><strong>T4-attunement (metadata):</strong> chain=<code>{escape(str(t4_ann.get('chain_alignment','')))}</code>, target=<code>{escape(str(t4_ann.get('t4_target_intent','')))}</code>, scope=<code>{escape(str(t4_ann.get('scope_preference','')))}</code></p>"
    trig = gear.get("triggered_passive")
    trig_html = f"<p><strong>Triggered passive:</strong> {format_triggered_passive(trig)}</p>" if trig else ""
    set_html = ""
    if gear.get("set_bonus") or gear.get("set_bonus_rank"):
        set_html = f"<p><strong>Set rank:</strong> {gear.get('set_bonus_rank', 0)}</p>"

    rarity_class_map = {
        "legendary_t0": "legendary", "legendary_t0_5": "legendary",
        "legendary_t1": "legendary", "legendary_t2": "legendary",
        "set_t1": "legendary", "set_t2": "legendary",
        "epic": "epic", "rare": "rare", "uncommon": "uncommon", "common": "common",
    }
    rarity = gear.get("rarity", "")
    return f"""
    <div class="gear-slot">
      <h5>{slot_name.replace('_', ' ').title()}</h5>
      <div class="rarity">{escape(rarity).upper()}</div>
      <p><code>{escape(gear.get('gear_instance_id',''))}</code></p>
      <strong>Partition modifiers:</strong>{mods_html}
      <strong>Capability modifiers:</strong>{caps_html}
      {t4_ann_html}
      {trig_html}
      {set_html}
    </div>
    """

def render_full_gear_set(char_id: str, gear_set: dict) -> str:
    """Render the full gear inventory across all 10 rarities × slots."""
    parts = []
    parts.append('<h4>Full gear inventory across all rarities (per-slot drop pool)</h4>')
    parts.append('<details><summary>Click to expand full gear matrix (10 rarities × 10 slots = up to 100 gear instances)</summary>')
    parts.append('<table>')
    parts.append('<tr><th>Slot</th>')
    rarities = ["common", "uncommon", "rare", "epic", "legendary_t0", "legendary_t0_5", "legendary_t1", "legendary_t2", "set_t1", "set_t2"]
    for r in rarities:
        parts.append(f'<th>{r.replace("_", " ").title()}</th>')
    parts.append('</tr>')
    for slot in gear_set.keys():
        parts.append(f'<tr><td><strong>{slot.replace("_"," ").title()}</strong></td>')
        for r in rarities:
            gi = gear_set[slot].get(r, {})
            mods_count = len(gi.get("partition_modifiers", []))
            caps_count = len(gi.get("capability_modifiers", []))
            has_trig = "✓" if gi.get("triggered_passive") else ""
            t4_ann = "✓" if gi.get("t4_annotation") else ""
            parts.append(f'<td><small>mods:{mods_count} caps:{caps_count} trig:{has_trig} t4:{t4_ann}</small></td>')
        parts.append('</tr>')
    parts.append('</table></details>')
    return "\n".join(parts)

def render_empirical_sim_results(cid: str) -> str:
    """Render empirical gauntlet sim results per character (post Track A remediation)."""
    if not GAUNTLET_RESULTS:
        return ""

    kit = GAUNTLET_KIT_BY_CHAR.get(cid)
    encounters = GAUNTLET_ENCOUNTERS_BY_CHAR.get(cid, [])

    if not kit:
        return f'<h4>Empirical Sim Results</h4><p><em>No empirical results indexed for {cid}.</em></p>'

    parts = []
    parts.append('<h4>Empirical Gauntlet Sim Results (post Track A remediation)</h4>')
    parts.append(f'<p>Source: <code>cycle-13-gauntlet-sim-results-2026-05-27.json</code> (Track A commit <code>b90b371</code> + W2 canonical-path fix <code>37f6fff</code>)</p>')

    # Per-cohort results
    parts.append('<table>')
    parts.append('<tr><th>Cohort</th><th>Encounters Passed</th><th>Encounters Total</th><th>Pass Rate</th><th>Gauntlet Pass</th></tr>')
    per_cohort = kit.get("per_cohort", {})
    for cohort, data in per_cohort.items():
        passed = data.get("encounters_passed", 0)
        total = data.get("encounters_total", 0)
        rate = f"{passed/total*100:.0f}%" if total > 0 else "—"
        gp = data.get("gauntlet_pass", False)
        gp_style = ' style="color: #44a08d;"' if gp else ' style="color: #e94560;"'
        parts.append(f'<tr><td>{cohort}</td><td>{passed}</td><td>{total}</td><td>{rate}</td><td{gp_style}>{"✓ PASS" if gp else "✗ FAIL"}</td></tr>')
    parts.append('</table>')

    # Season emit indicator
    season_emit = kit.get("season_emit", False)
    parts.append(f'<p><strong>Season emit:</strong> <span style="color: {"#44a08d" if season_emit else "#e94560"};">{"YES — kit ships" if season_emit else "NO — kit failed to emit"}</span></p>')

    # KPM summary from encounter results
    if encounters:
        kpm_by_cohort = {}
        for enc in encounters:
            cohort = enc.get("cohort", "")
            kpm = enc.get("tier_2_kpm")
            if kpm is not None:
                kpm_by_cohort.setdefault(cohort, []).append(kpm)

        if kpm_by_cohort:
            parts.append('<table>')
            parts.append('<tr><th>Cohort</th><th>Mean KPM (tier 2)</th><th>Min KPM</th><th>Max KPM</th><th>Encounter Count</th></tr>')
            for cohort, kpms in kpm_by_cohort.items():
                mean_kpm = sum(kpms) / len(kpms)
                parts.append(f'<tr><td>{cohort}</td><td>{mean_kpm:.2f}</td><td>{min(kpms):.2f}</td><td>{max(kpms):.2f}</td><td>{len(kpms)}</td></tr>')
            parts.append('</table>')

    # Diagnostic note for failed cohorts
    if not kit.get("per_cohort", {}).get("Defensive", {}).get("gauntlet_pass", True):
        parts.append('<div class="warning"><strong>Defensive cohort fail observed.</strong> Per gamora Track A diagnostic, the synthetic player class (calibration stand-in; magnitude=3000, cooldown=0.7s) does not satisfy Defensive cohort\'s stricter survival + KPM requirements. This is consistent across all 16 characters — Defensive 0/16 is a documented WARN at Cycle 13 close. Will improve when per-skill content layer lands per doc 46 Layers 1-5.</div>')

    return "\n".join(parts)

def render_character_section(char: dict, gear_set: dict) -> str:
    cid = char["character_id"]
    name = short_name(cid)
    analysis = GANDALF_ANALYSIS.get(cid, {})

    gear_rep = char.get("gear_representative", {})
    slot_order = ["main_weapon", "secondary_item", "head", "chest", "hands", "feet", "legs", "amulet", "ring_1", "ring_2", "belt"]
    gear_slots_html = "\n".join(render_gear_slot(s, gear_rep[s]) for s in slot_order if s in gear_rep)

    return f"""
    <section class="character-section" id="char-{cid}">
      <h3>{name}</h3>
      {render_id_card(char)}

      <h4>T4 Algorithm Output</h4>
      {render_t4_section(char)}

      <h4>Equipped Loadout (gear_representative — legendary T1 standard)</h4>
      <p><em>11 slots — main weapon + secondary (off-hand) + 5 armor + 4 accessory + belt</em></p>
      <div class="gear-grid">
        {gear_slots_html}
      </div>

      {render_full_gear_set(cid, gear_set) if gear_set else ""}

      {render_empirical_sim_results(cid)}

      <div class="gandalf-analysis">
        <h5>Gandalf Mechanical Analysis</h5>
        <p>{analysis.get('mechanical', '<em>Pending analysis.</em>')}</p>
      </div>

      <div class="gandalf-analysis">
        <h5>Gandalf Playability Analysis</h5>
        <p>{analysis.get('playability', '<em>Pending analysis.</em>')}</p>
      </div>

      <div class="gandalf-analysis">
        <h5>Gandalf Thematic / Legendary + Chain + T4 Cohesion Analysis</h5>
        <p>{analysis.get('thematic', '<em>Pending analysis.</em>')}</p>
      </div>

      <p><strong>WR-bracket pass:</strong> {char.get('wr_bracket_pass', False)} —
        <em>{escape(str((char.get('wr_bracket_details') or {}).get('note', '')))}</em></p>
    </section>
    """

# ---------------------------------------------------------------------------
# Cross-character analysis
# ---------------------------------------------------------------------------

def render_summary_table(chars: list) -> str:
    rows = []
    for c in chars:
        t4 = c["t4_candidates"][0] if c["t4_candidates"] else {}
        rows.append(f"""
        <tr>
          <td><a href="#char-{c['character_id']}">{short_name(c['character_id'])}</a></td>
          <td>{c['bc_tuple']['attribute']}</td>
          <td>{c['element']}</td>
          <td>{c['resource_model']}</td>
          <td>{c['cohort_archetype']}</td>
          <td>{c['class_chain_count']}</td>
          <td>{t4.get('category_a_strategy', '-')}</td>
          <td>{t4.get('t4_category_bc', '')}: {t4.get('category_bc_strategy', '-')}</td>
          <td>{t4.get('t4_scope', '-')}</td>
          <td>{t4.get('net_synergy_score', 0):.1f}</td>
        </tr>
        """)
    return f"""
    <table>
      <tr><th>Character</th><th>Attr</th><th>Element</th><th>Resource</th><th>Cohort</th><th>Chains</th><th>T4 Cat A</th><th>T4 Cat B/C</th><th>Scope</th><th>Net Synergy</th></tr>
      {"".join(rows)}
    </table>
    """

def render_cross_character_analysis(chars: list) -> str:
    # Cohort distribution
    cohorts = Counter(c['cohort_archetype'] for c in chars)
    elements = Counter(c['element'] for c in chars)
    attributes = Counter(c['bc_tuple']['attribute'] for c in chars)
    resource_models = Counter(c['resource_model'] for c in chars)
    cat_a = Counter()
    cat_bc = Counter()
    scopes = Counter()
    for c in chars:
        if c['t4_candidates']:
            t4 = c['t4_candidates'][0]
            cat_a[t4['category_a_strategy']] += 1
            cat_bc[t4['category_bc_strategy']] += 1
            scopes[t4['t4_scope']] += 1

    def render_counter(label, counter):
        return (
            f"<h4>{label}</h4><ul>"
            + "".join(f"<li><strong>{k}</strong>: {v}</li>" for k, v in counter.most_common())
            + "</ul>"
        )

    return f"""
    <h3>Cohort distribution (substrate-led per Q10)</h3>
    {render_counter("Cohort archetypes", cohorts)}
    <div class="warning">
      <strong>Defensive: 0 / Hybrid: 0</strong> — substrate-led result per Q10 amendment.
      Current ENDGAME_ENCOUNTER_CATALOG BC-cell coverage doesn't include cells that produce
      defensive (<code>bc_tempo=low + bc_amplitude in {{flat, sustained}}</code>) or hybrid
      (<code>bc_proxy_density=dense</code>) archetypes. Future encounter catalogs unlock
      these. NOT a bug.
    </div>

    {render_counter("Element distribution", elements)}
    {render_counter("Attribute distribution", attributes)}
    {render_counter("Resource model distribution", resource_models)}

    <h3>T4 algorithm distribution</h3>
    {render_counter("Category A (class-mechanical) strategy distribution", cat_a)}
    {render_counter("Category B/C (chain-specific) strategy distribution", cat_bc)}
    {render_counter("T4 scope dimension distribution", scopes)}

    <div class="gandalf-analysis">
      <h5>Gandalf Cross-Character Cohesion Observations</h5>
      <p><strong>Element diversity:</strong> the engine emitted {len(elements)} distinct elements
      across 16 characters — a healthy spread that avoids the form-bias failure modes flagged in
      2026-05-14 historical analysis.</p>

      <p><strong>Resource model diversity:</strong> {len(resource_models)} resource models
      represented out of 8 in the v1 catalog. Substrate-led — kits that ship reflect which
      cells the algorithm could fill against the WR bracket and per-cell resource-model mapping.</p>

      <p><strong>T4 Category A strategy diversity:</strong> {len(cat_a)} of 4 character-wide
      Category A strategies fired (RESOURCE_CONVERSION / TRADE_OFF / DEFENSIVE_CONVERSION /
      DEFENSIVE_TRADEOFF). The session's 3-category taxonomy is operationally expressed.</p>

      <p><strong>T4 Category B/C strategy diversity:</strong> {len(cat_bc)} Category B/C
      strategies in play. DUAL_ELEMENT_ADDITION (NEW from 2026-05-27 Pattern-B session) firing
      empirically demonstrates the new strategy is operational, not just spec'd.</p>

      <p><strong>Scope distribution:</strong> the 3-way split across <code>character_wide</code> /
      <code>chain_wide_own</code> / <code>chain_wide_parallel</code> reflects the scope-dimension
      selection algorithm operating per Phase 3 D81 implementation. Parallel-chain reach
      (NEW from 2026-05-27) is firing — visible cohesion impact when the build's parallel chain
      meaningfully composes with T4 effect.</p>

      <p><strong>One-T4-unlocked-at-a-time discipline (Matt 2026-05-27 lock):</strong>
      visible in t4_candidates per character — each character has exactly ONE active T4 candidate
      (<code>is_active: true</code>). The respec-with-legendary-trigger mechanism is the only
      path to swap unlock between alternate candidates — but each character has a single resolved
      T4 in the season-generated state.</p>

      <p><strong>Substrate-led pattern observation:</strong> the 88.9% WR-bracket pass rate
      (16 of 18 candidates ship) reflects the design discipline operating correctly — engine
      generates against spec; whatever validates ships; substrate determines what's in vs out
      of band. NOT pre-imposed N.</p>
    </div>
    """

def render_empirical_cross_character() -> str:
    """Render aggregate empirical gauntlet sim stats across all 16 characters."""
    if not GAUNTLET_RESULTS:
        return ""

    meta = GAUNTLET_RESULTS.get("gauntlet_metadata", {})

    parts = []
    parts.append('<h3>Empirical gauntlet sim cross-character aggregate</h3>')
    parts.append('<p>Post Track A remediation (gamora commit <code>b90b371</code> + W2 canonical-path fix <code>37f6fff</code>) — full empirical run results.</p>')

    parts.append('<div class="metric-grid">')
    parts.append(f'<div class="metric"><div class="label">Total Fights Run</div><div class="value">{meta.get("total_fights_run", 0):,}</div></div>')
    parts.append(f'<div class="metric"><div class="label">Kits Season Emit</div><div class="value">{meta.get("kits_season_emit", 0)}/{meta.get("total_kits_validated", 0)}</div></div>')
    parts.append(f'<div class="metric"><div class="label">Mean Encounters Passed</div><div class="value">{meta.get("mean_encounters_passed_per_kit", 0):.1f}</div></div>')
    parts.append(f'<div class="metric"><div class="label">Tier 1 Fights</div><div class="value">{meta.get("tier_1_fights_run", 0):,}</div></div>')
    parts.append(f'<div class="metric"><div class="label">Tier 2 Fights</div><div class="value">{meta.get("tier_2_fights_run", 0):,}</div></div>')
    parts.append(f'<div class="metric"><div class="label">Wall Clock</div><div class="value">{meta.get("wall_clock_seconds", 0):.1f}s</div></div>')
    parts.append('</div>')

    # Cohort pass distribution
    parts.append('<h4>Gauntlet pass distribution by cohort</h4>')
    parts.append('<table>')
    parts.append('<tr><th>Cohort</th><th>Pass count</th><th>Pass rate</th><th>Status</th></tr>')
    cohort_passes = meta.get("gauntlet_pass_by_cohort", {})
    total = meta.get("total_kits_validated", 16)
    for cohort, count in cohort_passes.items():
        rate = f"{count/total*100:.0f}%" if total > 0 else "—"
        if count == total:
            status = '<span style="color: #44a08d;">✓ Full pass</span>'
        elif count == 0:
            status = '<span style="color: #e94560;">✗ Full fail (synthetic-stub limitation)</span>'
        else:
            status = f'<span style="color: #f5b800;">Partial</span>'
        parts.append(f'<tr><td>{cohort}</td><td>{count}/{total}</td><td>{rate}</td><td>{status}</td></tr>')
    parts.append('</table>')

    # KPM distribution per cohort (aggregated across all 16 characters × ~57 encounters each)
    kpm_by_cohort = {}
    for kit in GAUNTLET_RESULTS.get("kit_results", []):
        cid_leg = kit.get("legendary_id", "")
        cid = "S1_" + cid_leg.rsplit("_T4", 1)[0] if "_T4" in cid_leg else None
        if cid:
            encs = GAUNTLET_ENCOUNTERS_BY_CHAR.get(cid, [])
            for enc in encs:
                cohort = enc.get("cohort", "")
                kpm = enc.get("tier_2_kpm")
                if kpm is not None:
                    kpm_by_cohort.setdefault(cohort, []).append(kpm)

    if kpm_by_cohort:
        parts.append('<h4>Mean tier-2 KPM by cohort (aggregated across 16 characters)</h4>')
        parts.append('<table>')
        parts.append('<tr><th>Cohort</th><th>Mean KPM</th><th>Min KPM</th><th>Max KPM</th><th>Encounter samples</th></tr>')
        for cohort, kpms in kpm_by_cohort.items():
            mean_kpm = sum(kpms) / len(kpms)
            parts.append(f'<tr><td>{cohort}</td><td>{mean_kpm:.2f}</td><td>{min(kpms):.2f}</td><td>{max(kpms):.2f}</td><td>{len(kpms)}</td></tr>')
        parts.append('</table>')

        parts.append('<div class="warning">')
        parts.append('<strong>Empirical KPM well below cohort bands.</strong> The synthetic player class (calibration stand-in; magnitude=3000, cooldown=0.7s) produces KPM ~2-3 across all cohorts, far below the cohort bands (Balanced 71-79, DPS 82-97, etc.). This is the synthetic_mode-driven outcome — <code>in_band</code> for synthetic sweeps means "encounter completable without timeout" (Discipline #12 semantic shift per gamora Track A), NOT "KPM within cohort band." When per-skill content lands per doc 46 Layers 1-5 (Cycle 14), KPM bands should reach realistic values.')
        parts.append('</div>')

    return "\n".join(parts)

def render_drax_cross_reference_notes(chars: list) -> str:
    return f"""
    <h3>Cross-reference notes for drax loadout app implementation</h3>
    <p>The drax loadout sample page should faithfully render the following data per character.
    Any element below that is missing in the loadout page UI surfaces a drax integration gap.</p>

    <h4>Per-character data drax MUST render</h4>
    <ul>
      <li><strong>Identity card:</strong> character_id, bc_cell_id, element, resource_model,
        cohort_archetype, class_chain_count, full bc_tuple (range/tempo/amplitude/attribute/proxy_density)</li>
      <li><strong>Chain composition:</strong> t4_chains count, supporting_chains count, total_chains</li>
      <li><strong>T4 candidates list:</strong> one or more T4 candidates per character.
        Per candidate: candidate_id, category_a_strategy, category_bc_strategy + t4_category_bc letter,
        parallel_chain_mode, t4_scope, all 3 scope_projection_data entries (character_wide / chain_wide_own /
        chain_wide_parallel) with weighted_score + net_synergy_score + prior_weight,
        resolve_score, create_score, net_synergy_score, separability_pass, is_active flag,
        pattern_9_warn and pattern_10_warn indicators, secondary_element (for DUAL_ELEMENT_ADDITION),
        magnitude_tier + magnitude_midpoint where applicable</li>
      <li><strong>Gear representative (11 slots):</strong> main_weapon, secondary_item, head, chest,
        hands, feet, legs, amulet, ring_1, ring_2, belt — each with gear_instance_id, rarity,
        partition_modifiers (each with modifier_id + category + polarity + tier_restriction + magnitude),
        capability_modifiers (each with modifier_id + capability_category),
        t4_annotation (chain_alignment + t4_target_intent + scope_preference),
        triggered_passive (pattern_id + description + is_true_active + probability),
        set_bonus / set_bonus_rank, is_unique</li>
      <li><strong>Full gear set per slot per rarity:</strong> 10 rarities (common through legendary_t2 +
        set_t1 + set_t2) × 10-11 slots. Drop pool restriction per content-tier per D50.</li>
      <li><strong>WR-bracket pass status + details:</strong> wr_bracket_pass + wr_bracket_details</li>
    </ul>

    <h4>Interactive controls drax MUST provide (per Matt 2026-05-27 directive)</h4>
    <ul>
      <li><strong>Skill tree node investment editor:</strong> add/subtract node investment per node,
        with per-node max enforcement (passive 5 max / active 15 max / T4 binary 1 per Block A3 lock).
        Visualize per-chain investment threshold = 70% of chain max (T4 unlocks when met).</li>
      <li><strong>T4 selection toggle:</strong> player can select which T4 is active (one at a time
        per Matt 2026-05-27); respec mechanism options:
        (1) T4-only respec — swap which T4 is active if multiple chains above T4-unlock threshold,
        (2) full respec — reset all chain investment + T4 selection (Spirit-Guide-mediated;
        auto-allocate option per Block A4). Spirit Guide as interaction surface per D75 / D28-D32.</li>
      <li><strong>All 11 gear slots displayed:</strong> drax must NOT collapse / omit any of the 11
        slots from the sample page. Common omission risk: ring_1 vs ring_2 (treat as distinct slots);
        belt (sometimes overlooked); secondary_item (must support all 7 off-hand categories per
        off-hand-items-2026-05-24.md).</li>
    </ul>

    <h4>Discrepancy flags to watch</h4>
    <ul>
      <li>If the drax loadout page shows a node count exceeding 5 for passive nodes, exceeding 15
        for active nodes, or showing T4 with non-binary value — that's a per-node-max violation.</li>
      <li>If the drax loadout page allows multiple T4s unlocked simultaneously, that violates the
        Matt 2026-05-27 one-T4-at-a-time lock.</li>
      <li>If a triggered_passive on a non-weapon slot is rendered as a true-active skill, that
        violates D55 (true-actives are weapon-only).</li>
      <li>If the T4-attunement is rendered as a toggleable bonus multiplier with on/off states,
        that violates Block B1 content-compositional attunement (annotation is metadata-only,
        NOT a toggle mechanism).</li>
      <li>If gear at Tier 0 or Tier 0.5 carries a T4-attunement annotation, that violates D33 + D51
        (T4-attunement ONLY at Tier 1+2 legendary/set).</li>
    </ul>
    """

# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

toc_items = "\n".join(
    f'<li><a href="#char-{c["character_id"]}">{short_name(c["character_id"])}</a></li>'
    for c in CHARACTERS
)

character_sections = "\n".join(
    render_character_section(c, GEAR_SETS.get(c["character_id"], {}))
    for c in CHARACTERS
)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cycle 13 Character Analysis — gandalf cross-reference</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class="container">

    <h1>Cycle 13 Character Analysis</h1>
    <p><strong>Author:</strong> gandalf (story-and-design steward) &middot;
       <strong>Date:</strong> 2026-05-27 &middot;
       <strong>Source:</strong> <code>reincarnated-engine/output/cycle-13-mechanical-season-001/</code>
    </p>
    <p><strong>Purpose:</strong> gold-standard cross-reference for drax loadout app implementation.
      This HTML doc reads the 16 character JSONs + 16 gear_set JSONs from the engine's Cycle 13
      Wave 5 Track B season generation output, faithfully renders the data, and adds
      mechanical / playability / thematic analysis. drax loadout sample page (sources from
      loadout DB post star-lord schema extension) should render the same data;
      discrepancies surface drax integration gaps.</p>

    <div class="tldr">
      <strong>TL;DR.</strong> 16 endgame-node (L45-50+) characters covering 4 attributes
      (STR / DEX / INT / WIS) × multiple elements × multi-T4 architecture (3-category taxonomy
      + DUAL_ELEMENT_ADDITION + parallel-chain reach + compositional synergy scan + content-compositional
      attunement). Substrate-led WR-bracket pass: <strong>{SEASON_METADATA['wr_bracket_pass_count']} of
      {SEASON_METADATA['kit_candidate_count']}</strong> ({SEASON_METADATA['wr_bracket_pass_rate']*100:.1f}%).
      Cohort distribution: dps_min_maxer: {SEASON_METADATA['cohort_distribution_season']['dps_min_maxer']},
      balanced: {SEASON_METADATA['cohort_distribution_season']['balanced']},
      defensive: {SEASON_METADATA['cohort_distribution_season']['defensive']},
      hybrid: {SEASON_METADATA['cohort_distribution_season']['hybrid']}.
      Defensive 0 + Hybrid 0 are substrate-led results (encounter catalog BC-coverage gap),
      not bugs.
    </div>

    <div class="tldr" style="border-left-color: #44a08d;">
      <strong>UPDATED 2026-05-27 post Track A remediation:</strong> Gamora's Track A
      diagnostic identified 3 bugs (auto-attack interference / KPM quantization
      impossibility / floating-point cooldown accumulation) and remediated via
      <code>synthetic_mode=True</code> + Discipline #12 semantic shift + parameter
      corrections. <strong>Empirical results NOW on disk:</strong>
      27,360 fights run / 12 of 12 populated strata / 16 of 16 kits season_emit /
      canonical output at <code>src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json</code>
      (620 KB). Gauntlet pass by cohort: <strong>DPS-min-maxer 16/16, Balanced 16/16,
      Hybrid 16/16, Defensive 0/16</strong>. Defensive 0/16 documented WARN per
      synthetic-stub limitations; expected to improve when per-skill content layer
      lands per doc 46 Layers 1-5 (Cycle 14 sidecar).
    </div>

    <div class="warning">
      <strong>Cycle 14 architectural amendments queued per doc 46
      (Concentration Architecture — 9 layers):</strong>
      Stat-range bounds + affix migration + capability scope reduction + trigger
      vocabulary expansion + concentration probability table + cohesion-judge
      layered architecture + compositional synergy scan refined + set keying to
      T4 strategy × element clusters + class-agnostic spec-driven per-drop
      generation. Architectural through-line: <em>concentration over distribution;
      identity = chain composition + T4 + 4-6 build-defining items + stat-affix
      support; gear amplifies, gear does not constitute</em>. See
      <code>canonical/46-concentration-architecture-2026-05-27.md</code> for full
      architectural foundation. Cycle 13 capability-soup pattern (~22 mechanic-
      alterations per character; per-character bespoke sets; missing stat bounds;
      template-driven redundancy) will be remediated in Cycle 14.
    </div>

    <h2>Table of Contents</h2>
    <div class="toc">
      <ol>{toc_items}</ol>
    </div>

    <h2>Cross-character summary table</h2>
    {render_summary_table(CHARACTERS)}

    <h2>Per-character analysis</h2>
    {character_sections}

    <h2>Cross-character analysis</h2>
    {render_cross_character_analysis(CHARACTERS)}

    {render_empirical_cross_character()}

    {render_drax_cross_reference_notes(CHARACTERS)}

    <h2>Cycle 13 Discipline Observations</h2>
    <div class="gandalf-analysis">
      <h5>Compositional synergy scan firing empirically</h5>
      <p>Per character, the t4_candidates[].resolve_score and create_score fields capture the
      two-pass synergy scan (Pass 1 resolve + Pass 2 preserve per the 2026-05-27 first-do-no-harm
      discipline). Net synergy = resolve − create; positive nets pass the synergy gate.
      Pattern 9 / Pattern 10 WARN flags are inactive across all 16 characters in this snapshot —
      no character is exhibiting the synergy-amplification or scope-amplification edge-case
      WARN states.</p>

      <h5>Content-compositional T4-attuned gear visible in data</h5>
      <p>Every gear slot at Tier 1+ legendary carries a <code>t4_annotation</code> field with
      <code>chain_alignment</code>, <code>t4_target_intent</code>, <code>scope_preference</code>,
      and <code>attunement_count</code>. Per the Matt 2026-05-27 lock: this annotation is
      METADATA recording generation-time alignment intent, NOT a toggle mechanism. The gear's
      capability_modifiers and triggered_passive content composes with the active build's
      T4 selection by virtue of what they DO, not by activation flag.</p>

      <h5>Three-category T4 taxonomy operationally expressed</h5>
      <p>Every character's t4_candidate carries explicit <code>category_a_strategy</code>
      (Category A — character-wide class-mechanical alteration) AND <code>category_bc_strategy</code>
      with <code>t4_category_bc</code> letter indicating B (multiplicative) or C (element conversion /
      addition). The 3-category taxonomy supersedes the prior 6-strategy registry as design-spec
      and player-facing vocabulary; the existing 6 strategies are retained as algorithm
      implementation detail.</p>
    </div>

    <div class="footer">
      Authored by gandalf (story-and-design steward) 2026-05-27 ·
      Source: 16 character JSONs + 16 gear_set JSONs + season_metadata.json +
      sim_cycling_quality_report.json at
      <code>reincarnated-engine/output/cycle-13-mechanical-season-001/</code> ·
      Generation script: <code>generate_cycle13_character_analysis.py</code> ·
      For: gold-standard cross-reference for drax loadout app implementation faithfulness check
    </div>
  </div>
</body>
</html>
"""

# Write
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(HTML)
print(f"Generated: {OUTPUT_PATH}")
print(f"Characters analyzed: {len(CHARACTERS)}")
print(f"Gear sets loaded: {len(GEAR_SETS)}")
print(f"HTML size: {len(HTML):,} chars")
