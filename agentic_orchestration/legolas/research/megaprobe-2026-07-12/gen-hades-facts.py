"""
gen-hades-facts.py
Mega-probe Unit A — Hades 1 + Hades 2 (hades) — 13 records
13 positive / 0 negative / 4 post-cutoff (hades2 1.0-2025+)
Full schema (6 fact families per kit).

Notes:
- Attr slot is '_' for all Hades kits (Zagreus/Melinoe don't map to STR/DEX/INT)
- hades2-omega-magick: ea-2024 anchor → NOT formally post-cutoff; reduced conf ~0.62
- Post-cutoff: medea-skull-cast (post1.0-2026), hephaestus-blast, glorious-disaster,
  hail-storm (all 1.0-2025 + post1.0-2026)
"""
import json
from pathlib import Path

OUT = Path("agentic_orchestration/legolas/research/megaprobe-2026-07-12/hades-facts.jsonl")

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

KITS = []

# ── 1. hades1-beowulf-cast ────────────────────────────────────────────────────
# Shield of Chaos / Beowulf aspect: cast bloodstone INTO shield → ranged ammo launch
# Atlas: _DMSSI = unknown attr, mid, med, spiky, solo, instant
# hades1-2020; prov: kb
KITS.append({
    "kit_id": "hades1-beowulf-cast",
    "folk_name": "Beowulf Cast Build",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "_DMSSI-MNDT-AM-__-~~",
    "delivery": dc("projectile", 0.88, "bloodstone loaded into shield becomes a thrown ranged projectile; lodges in enemy on hit"),
    "footprint": dc("point", 0.85, "single-target projectile that lodges in enemy; AOE on retrieval bash is small-radius secondary"),
    "geo_text": "Beowulf aspect loads the cast bloodstone INTO the Shield of Chaos. The shield+bloodstone is then launched as a heavy ranged projectile that lodges in a struck enemy. To retrieve, Zagreus must bash the enemy. Finite ammo: the one bloodstone must be retrieved before re-casting.",
    "control": ctrl(["stagger"], "rider", 0.80),
    "defense": defs(["block"], "block", 0.82),
    "economy": econ("bloodstone ammo (1 charge, retrieve-to-reload)", "ammo", "n/a", "melee_retrieve",
                    "Single bloodstone is the ammo payload. Loaded into shield on Special, then hurled on Cast. Retrieval required (melee-bash the enemy it lodges in) to reload. Finite-ammo-retrieve loop.", 0.85),
    "element": elem("n/a (physical/chaos)", "hit", 0.80),
    "movement": mov(["reposition", "retrieve-bash"], "full-move", False, 0.82),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr slot blank — roguelite verb-augmentation, not STR/DEX/INT"),
        pc("D", 0.85, "mid-range thrown shield; not melee contact but not long-range bow"),
        pc("M", 0.82, "medium tempo; reload cycle (retrieve-to-reload) imposes cadence"),
        pc("S", 0.82, "spiky amplitude — heavy single payload per throw; not flat DPS"),
        pc("S", 0.85, "solo; no proxy element"),
        pc("I", 0.88, "instant trigger per throw"),
    ),
    "mechanics_notes": "Ammo economy (AM): the bloodstone becomes ammunition. Retrieval loop = melee-bass the lodged enemy to get bloodstone back. Distinctive: ammo-retrieve forces engagement with the target — the build closes to melee to reload. Corpus category: boon/aspect build expressing ammo economy.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Bloodstone throw gains boon scaling (e.g., Zeus/Poseidon boons on cast). Shield bash retrieve can chain into attack combos.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 2. hades1-athena-dash ─────────────────────────────────────────────────────
# Athena boon on dash: deflect makes dash a counterattack + defense verb
# Atlas: _MHFSI = unknown attr, melee, high, flat, solo, instant; skill IS movement
# hades1-2020; prov: kb
KITS.append({
    "kit_id": "hades1-athena-dash",
    "folk_name": "Athena Divine Dash Core",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "_MHFSI-KNMD-SP-__-~~",
    "delivery": dc("self-origin", 0.88, "deflect aura activates on the dash body; reflects projectiles through player motion"),
    "footprint": dc("point", 0.85, "deflect applies at contact point during dash; not a zone — the dash path IS the hitbox"),
    "geo_text": "Athena boon converts the dash verb into a deflect. While dashing, any projectile that would hit Zagreus is reflected back at enemies. The dash IS the delivery: the player moves through the projectile plane and it reverses. Skill is movement.",
    "control": ctrl(["deflect", "stagger"], "rider", 0.85),
    "defense": defs(["dodge"], "dodge", 0.90),
    "economy": econ("universal verb mod (no resource — dash cooldown only)", "cooldown", "n/a", "n/a",
                    "No extra resource cost — the deflect is grafted onto the existing dash cooldown. Dash cooldown is the economy unit. The boon itself is free (granted by boon pick). Economy = cooldown (dash timer).", 0.85),
    "element": elem("n/a (physical deflect)", "hit", 0.80),
    "movement": mov(["dash", "deflect-on-move"], "full-move", True, 0.92),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr slot blank"),
        pc("M", 0.88, "melee-contact deflect; must dash through projectile path"),
        pc("H", 0.88, "high tempo — dash is the highest-frequency verb in Hades"),
        pc("F", 0.85, "flat deflect output; consistent damage return per deflected projectile"),
        pc("S", 0.88, "solo; no proxy element"),
        pc("I", 0.90, "instant dash trigger; deflect is instantaneous on contact"),
    ),
    "mechanics_notes": "Mobility=skill-IS-movement. Deflect converts the movement verb into offense + defense simultaneously — a unique dual-role verb. 'The dash DEFLECTS' is the complete kit thesis: defense and counterattack from one button. Core for Merciful End duo boon.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Athena dash upgrades increase deflect damage multiplier and dash distance.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 3. hades1-merciful-end ───────────────────────────────────────────────────
# Duo boon: deflect INSTANTLY triggers Doom (Ares+Athena capstone)
# Atlas: _MHSSI = unknown attr, melee, high, spiky, solo, instant; skill IS movement
# hades1-2020; prov: kb
KITS.append({
    "kit_id": "hades1-merciful-end",
    "folk_name": "Merciful End (Ares+Athena duo)",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "_MHSSI-KSDD-SP-__-~~",
    "delivery": dc("self-origin", 0.85, "duo boon grafted onto deflect; Doom detonates on deflect contact point"),
    "footprint": dc("point", 0.82, "Doom detonates on the deflected target; single-point detonation on enemy"),
    "geo_text": "Pair-grain capstone: Athena deflect (movement verb) + Ares Doom tag. When Zagreus deflects a projectile, Doom is INSTANTLY triggered on the source enemy — bypassing Doom's normal delay. The deflect becomes a burst detonation trigger.",
    "control": ctrl(["deflect", "doom"], "core", 0.85),
    "defense": defs(["dodge"], "dodge", 0.88),
    "economy": econ("pair-grain capstone (duo boon)", "cooldown", "n/a", "n/a",
                    "Economy inherited from dash cooldown. The duo boon itself requires Ares + Athena boon investment; no extra resource cost per use. Pair-grain = requires two boon lineages.", 0.85),
    "element": elem("n/a (doom burst)", "hit", 0.82),
    "movement": mov(["dash", "deflect-trigger"], "full-move", True, 0.88),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr slot blank"),
        pc("M", 0.85, "melee-contact deflect on dash"),
        pc("H", 0.85, "high tempo — dash frequency drives duo proc rate"),
        pc("S", 0.82, "spiky amplitude — Doom burst is a single large spike per deflect"),
        pc("S", 0.85, "solo; pure self-serve counterattack"),
        pc("I", 0.88, "instant: deflect-to-Doom detonation is same-frame"),
    ),
    "mechanics_notes": "Pair-grain-capstone (duo boon grammar): requires both Ares-line AND Athena-line boons in the same run. Doom's normal delay is REMOVED — detonation is immediate on deflect contact. Corpus captures this as the convergence between two boon lineages into a burst detonation verb.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Upgrade both underlying boon lines (Ares Doom level + Athena deflect level) to amplify the detonation burst and deflect frequency.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 4. hades1-ares-doom ───────────────────────────────────────────────────────
# Ares boon: Doom tag → delayed detonation; hit-now-pay-later
# Atlas: _MMSSW = unknown attr, melee, med, spiky, solo, wind-up
# hades1-2020; prov: kb
KITS.append({
    "kit_id": "hades1-ares-doom",
    "folk_name": "Ares Doom Core",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "_MMSSW-HNDD-SP-__-~~",
    "delivery": dc("at-target", 0.88, "Doom tag applied at target on hit; detonation at tagged enemy position after delay"),
    "footprint": dc("point", 0.85, "Doom detonates at the single tagged enemy; no AOE on base Doom"),
    "geo_text": "Ares boon: hitting an enemy applies a Doom tag. After a brief window (Ares' 'delay budget'), Doom detonates for a single burst of heavy damage. Hit-now, damage-later. Can apply multiple Doom stacks; each detonates independently.",
    "control": ctrl(["doom"], "core", 0.88),
    "defense": defs(["dodge", "glass"], "glass", 0.82),
    "economy": econ("tag-bank-payout (Doom window)", "proc", "n/a", "on_hit",
                    "Each hit triggers a Doom application (free proc on hit). The tag 'banks' the damage; it pays out after the delay window. Economy = proc-on-hit triggering delayed detonation. No extra resource cost per tag.", 0.85),
    "element": elem("n/a (doom/darkness)", "dot", 0.82),
    "movement": mov(["kite-out-after-tag", "reposition"], "full-move", False, 0.82),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr slot blank"),
        pc("M", 0.82, "melee or near-melee to apply tag; Ares boon on attack/special"),
        pc("M", 0.82, "medium tempo — Doom window paces the detonation cadence"),
        pc("S", 0.88, "spiky amplitude — single detonation burst is a large spike"),
        pc("S", 0.85, "solo; no proxy element"),
        pc("W", 0.85, "wind-up — the Doom delay is a wind-up analog; damage pays out after a beat"),
    ),
    "mechanics_notes": "Tag-bank-payout grammar: the 'bank' is the Doom window; the 'payout' is detonation. Wind-up commit because the damage is temporally decoupled from the hit — you commit to the hit, damage resolves later. Doom is the canonical 'hit-now-damage-later' archetype. Pairs with Merciful End to remove the delay.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Higher Ares boon tiers increase Doom burst damage; additional Ares boons add Doom to more verbs.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 5. hades1-zeus-chain ──────────────────────────────────────────────────────
# Zeus boon: chain lightning procs on every hit
# Atlas: _RHFSI = unknown attr, ranged, high, flat, solo, instant
# hades1-2020; prov: kb
KITS.append({
    "kit_id": "hades1-zeus-chain",
    "folk_name": "Zeus Chain-Lightning Core",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "_RHFSI-HCDD-PC-LI-~~",
    "delivery": dc("projectile", 0.85, "base attack is ranged projectile; Zeus boon grafts chain-lightning proc onto each hit"),
    "footprint": dc("chain-hop", 0.88, "chain lightning forks through pack on each hit; G2: chain-hop NOT a line/beam"),
    "geo_text": "Zeus boon converts any attack into a chain-lightning engine. Each hit forks lightning through nearby enemies — chain-hop geometry: one hit, multiple chain-jump destinations. High attack frequency drives high chain proc throughput.",
    "control": ctrl(["shock", "stun"], "rider", 0.82),
    "defense": defs(["dodge", "glass"], "glass", 0.80),
    "economy": econ("flat proc per hit (Zeus lightning free proc)", "proc", "n/a", "on_hit",
                    "Chain lightning procs on every hit at no additional resource cost. Economy = pure proc — the attack's normal resource drives the proc rate. PC = proc-chain in old vocab.", 0.85),
    "element": elem("lightning", "hit", 0.88),
    "movement": mov(["kite", "strafe"], "full-move", False, 0.85),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr slot blank"),
        pc("R", 0.85, "ranged attack (bow/heart-seeking arrow base); Zeus boon applies to ranged attacks"),
        pc("H", 0.88, "high tempo — attack frequency drives chain-proc throughput"),
        pc("F", 0.85, "flat proc output per hit; consistent lightning damage addition"),
        pc("S", 0.85, "solo; chain-hop is self-powered, no proxy"),
        pc("I", 0.88, "instant attack trigger; chain fires immediately on hit"),
    ),
    "mechanics_notes": "G2 flag: chain-hop, NOT a line or beam. The chain-lightning forks are bouncing arcs between targets — not a directional sustained beam. Zeus is the canonical chain-hop archetype in Hades. PC economy (proc-chain) in old vocab.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Zeus boon tiers increase chain damage and fork count; Jolted status (Zeus unique) makes chained enemies prime for bonus damage.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 6. hades1-aspect-guan-yu ──────────────────────────────────────────────────
# Aspect of Guan Yu Spear: self-cost contract — trade max HP for life-drinking spin
# Atlas: _MMFSI = unknown attr, melee, med, flat, solo, instant
# hades1-2020; prov: kb
KITS.append({
    "kit_id": "hades1-aspect-guan-yu",
    "folk_name": "Aspect of Guan Yu Spear",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "_MMFSI-MSDG-SC-__-~~",
    "delivery": dc("self-origin", 0.85, "life-drinking spin-special — spear spins in AOE around Zagreus while draining HP"),
    "footprint": dc("small-radius", 0.85, "spin AOE around caster body; classic whirlwind-adjacent small-radius"),
    "geo_text": "Guan Yu aspect: the spear's special cuts max HP (permanent sacrifice) for a life-drinking spin-attack. The spin deals melee AOE damage while draining HP over time during use. Power purchased through permanent HP reduction — a self-cost contract.",
    "control": ctrl(["slow"], "rider", 0.78),
    "defense": defs(["sustain-leech", "hp-stack"], "hp-stack", 0.80),
    "economy": econ("self-cost-contract (max HP drain + sustain leech)", "self-cost", "n/a", "n/a",
                    "SC = self-cost. Aspect reduces max HP permanently (contract). The spin drains HP during use (active self-cost). Simultaneously leeches HP from enemies hit — net sustain depends on hit rate vs drain rate.", 0.85),
    "element": elem("n/a (physical/spear)", "hit", 0.82),
    "movement": mov(["spin", "advance"], "full-move", False, 0.82),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr slot blank"),
        pc("M", 0.88, "melee spin; spear AOE at contact range"),
        pc("M", 0.82, "medium tempo — spin special is sustained but not as high-freq as attack"),
        pc("F", 0.82, "flat spin DPS while active; consistent per-tick output"),
        pc("S", 0.85, "solo; self-contained power trade"),
        pc("I", 0.85, "instant special trigger; spin activates immediately"),
    ),
    "mechanics_notes": "Self-cost-contract grammar: HP sacrifice is permanent (persistent contract), not a per-use resource drain in the typical sense. Active HP drain during spin is the use-cost. Life-leech offsets. Canonical self-cost archetype in corpus — power bought with permanent HP reduction.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Weapon level upgrades to Guan Yu aspect reduce the max HP penalty and/or increase life-leech per hit.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 7. hades1-aspect-chiron ───────────────────────────────────────────────────
# Aspect of Chiron Bow: attack marks → specials auto-seek the mark
# Atlas: _RHFSI = unknown attr, ranged, high, flat, solo, instant
# hades1-2020; prov: kb
KITS.append({
    "kit_id": "hades1-aspect-chiron",
    "folk_name": "Aspect of Chiron Bow",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "_RHFSI-HNDD-AM-__-~~",
    "delivery": dc("projectile", 0.88, "attack projectile marks enemy; special arrows seek the mark automatically"),
    "footprint": dc("point", 0.85, "mark applied at point on enemy; seeking-specials converge on that single marked target"),
    "geo_text": "Chiron bow aspect: attack marks a target. All subsequent special arrows auto-aim at the mark, regardless of player aim direction. 'Aim once, unload blind' — the bow's specials become homing projectiles. Mark-consume loop: mark reapplied on each attack.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["dodge", "glass"], "glass", 0.82),
    "economy": econ("mark-consume (ammo analog — special arrows consume mark)", "ammo", "n/a", "attack_marks",
                    "Attack applies the mark (free, per-attack trigger). Special arrows consume the mark-state as their targeting resource — they seek the mark and bypass aiming. AM notation: the mark IS the ammo for the specials.", 0.85),
    "element": elem("n/a (physical/bow)", "hit", 0.82),
    "movement": mov(["kite", "strafe"], "full-move", False, 0.85),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr slot blank"),
        pc("R", 0.90, "ranged bow; both mark-application and specials are ranged projectiles"),
        pc("H", 0.88, "high tempo — rapid attack rate applies mark continuously"),
        pc("F", 0.85, "flat per-special seeking-arrow damage; consistent output"),
        pc("S", 0.85, "solo; mark loop is self-contained"),
        pc("I", 0.88, "instant attack trigger; mark applies instantly on hit"),
    ),
    "mechanics_notes": "Mark-consume loop: attack → mark → specials auto-seek → repeat. The bow's aiming becomes irrelevant once mark is established; specials find the target regardless. AM (ammo) code in old vocab: the mark-state is consumed as the 'ammo' for seeking-specials. Distinctive targeting inversion.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Chiron aspect upgrades increase special arrow count and mark-consume special damage multiplier.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 8. hades1-privileged-status ───────────────────────────────────────────────
# Privileged Status: bonus damage to enemies with 2+ status effects (meta mechanic)
# Atlas: ___F__ = blank attr/range/proxy/commit, amp=flat; meta-system record
# hades1-2020 + hades2-2024+; prov: ct;kb
KITS.append({
    "kit_id": "hades1-privileged-status",
    "folk_name": "Privileged Status (mechanized cap)",
    "game": "hades1",
    "status": "positive",
    "atlas_key": "___F__-__M_-SP-__-~~",
    "delivery": dc("other", 0.82, "meta-mechanic: bonus damage to enemies under 2+ status effects; not a castable skill"),
    "footprint": dc("other", 0.82, "meta-mechanic; no spatial footprint; applies per-hit to status-loaded enemies"),
    "geo_text": "Privileged Status: any enemy afflicted with two or more status effects simultaneously receives bonus damage from all sources. The game mechanizes multi-element synergy: stacking ailments becomes the prerequisite for a universal damage multiplier.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["other"], "other", 0.78),
    "economy": econ("two-status-gate (passive bonus)", "proc", "n/a", "status_stack_check",
                    "No active resource — Privileged Status is a passive multiplier that auto-applies when 2+ status effects are present on an enemy. Proc grammar: condition (2+ statuses) → bonus damage payout.", 0.82),
    "element": elem("n/a (damage multiplier)", "hit", 0.80),
    "movement": mov([], "full-move", False, 0.78),
    "prefix_claims": pfx(
        pc("_", 0.50, "meta-mechanic; no attr"),
        pc("_", 0.50, "meta-mechanic; no range"),
        pc("_", 0.50, "meta-mechanic; no tempo"),
        pc("F", 0.80, "flat multiplier — consistent bonus applied to all qualifying hits"),
        pc("_", 0.50, "meta-mechanic; no proxy"),
        pc("_", 0.50, "meta-mechanic; no commit"),
    ),
    "mechanics_notes": "System-structural record spanning both games. Hades I (2020) introduced it; Hades II (2024+) carried it forward. The 2-status-effect gate mechanizes element-combo play: build multi-element boon stacks to qualify targets. Convergence-point for cross-god boon synergies.",
    "era_confirmed": "hades1-2020",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Certain boons increase the Privileged Status bonus damage multiplier.",
    "sources_used": ["ct (content/guide corpus)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 9. hades2-omega-magick ────────────────────────────────────────────────────
# Omega/Magick grammar: charged-hold Omega variants costing Magick resource
# Atlas: __MSSW = double-blank attr/range, med, spiky, solo, wind-up
# ea-2024 anchor → NOT formally post-cutoff; reduced conf ~0.65 (EA-era data)
KITS.append({
    "kit_id": "hades2-omega-magick",
    "folk_name": "Omega/Magick Commitment Grammar",
    "game": "hades2",
    "status": "positive",
    "atlas_key": "__MSSW-____-MT-__-~~",
    "delivery": dc("other", 0.65, "meta-system grammar record: Omega variants exist on every verb; delivery shape varies per skill; ea-2024 reduced conf"),
    "footprint": dc("other", 0.62, "meta-system; footprint depends on which verb goes Omega; ea-2024 reduced conf"),
    "geo_text": "Every weapon verb in Hades II gains an Omega variant: hold to charge a Magick-costed powered version. Magick is a dedicated second resource (separate from HP). Sprint is integrated: Melinoe can sprint while performing Omega charges. The Omega commitment grammar defines Hades II's pacing signature vs Hades I.",
    "control": ctrl([], "none", 0.60),
    "defense": defs(["other"], "other", 0.60),
    "economy": econ("Magick meter (Omega spend)", "meter", "focus", "n/a",
                    "Magick is a dedicated resource bar. Omega-variant uses charge/spend Magick. Normal verbs do not cost Magick. MT = multi-trigger in old vocab but here maps to metered Omega spend. Sprint integrated: charging Omega while sprinting is supported.", 0.62),
    "element": elem("n/a (grammar record)", "hit", 0.58),
    "movement": mov(["sprint-while-charging"], "full-move", False, 0.65),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr blank; roguelite verb grammar, not STR/DEX/INT"),
        pc("_", 0.50, "range varies per Omega verb; meta-system record"),
        pc("M", 0.62, "medium tempo — Omega charge has wind-up cost that paces cadence; ea-2024 conf"),
        pc("S", 0.65, "spiky amplitude — Omega hits are charged burst payloads; ea-2024 conf"),
        pc("S", 0.62, "solo; self-powered Magick loop; ea-2024 conf"),
        pc("W", 0.65, "wind-up commit — holding for Omega charge is a wind-up; ea-2024 conf"),
    ),
    "mechanics_notes": "NOT formally post-cutoff: earliest era = hades2-ea-2024 (EA launched May 2024; within training window). Reduced conf throughout (~0.62) due to EA-era data sparsity. Omega/Magick grammar = the defining new system of Hades II vs Hades I. MT economy code (old vocab) maps to magick-metered-omega spend. Sprint integration is the movement innovation.",
    "era_confirmed": "hades2-ea-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Boons and aspects can reduce Omega costs, add Magick regen, or enhance Omega-specific effects per weapon.",
    "sources_used": ["lr (let's-run/guide corpus)", "gt2 (game-tutorial resource)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 10. hades2-medea-skull-cast ───────────────────────────────────────────────
# Medea aspect skull cast: heavy detonating-projectile at 62 Fear
# Atlas: _DLSSW = unknown attr, mid, low, spiky, solo, wind-up
# POST-CUTOFF: hades2-post1.0-2026 ONLY
KITS.append({
    "kit_id": "hades2-medea-skull-cast",
    "folk_name": "62-Fear Medea Skull Build",
    "game": "hades2",
    "status": "positive",
    "atlas_key": "_DLSSW-_LD_-SP-__-~~",
    "delivery": dc("projectile", 0.45, "heavy detonating cast projectile; skull weapon cast; post-cutoff conf capped"),
    "footprint": dc("large-zone", 0.45, "large AOE detonation on impact; post-cutoff conf capped"),
    "geo_text": "Medea aspect skull weapon cast: a heavy lobbed projectile that detonates in a large AOE on impact. Verified at 62 Fear difficulty. Cast-centric build under Medea's aspect. Low tempo (massive per-shot payload), wind-up commitment.",
    "control": ctrl([], "none", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("finite-payload-lob (cast charges)", "ammo", "n/a", "n/a",
                    "Finite cast charges per cast resource; lob heavy detonating payload; post-cutoff economy specifics unknown. Post-cutoff conf capped.", 0.42),
    "element": elem("n/a (chaos/skull)", "hit", 0.40),
    "movement": mov(["reposition"], "full-move", False, 0.42),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr blank; post-cutoff conf capped"),
        pc("D", 0.45, "mid-range lobbed skull; post-cutoff conf capped"),
        pc("L", 0.45, "low tempo — heavy single detonation payload; post-cutoff conf capped"),
        pc("S", 0.45, "spiky amplitude — single large detonation burst; post-cutoff conf capped"),
        pc("S", 0.45, "solo build; post-cutoff conf capped"),
        pc("W", 0.45, "wind-up — cast has a lob arc/delay before detonation; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: hades2-post1.0-2026 is the ONLY era; all conf capped ≤0.50. 62 Fear = the endgame difficulty bracket cited in provenance (mb-h = matchup-build source). Medea aspect is a Hades II cast-weapon aspect introduced post-1.0. Full mechanics not confirmable from training data.",
    "era_confirmed": "hades2-post1.0-2026",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Medea aspect upgrades enhance detonation radius and damage; cast charge recovery unknown (post-cutoff).",
    "sources_used": ["mb-h (matchup-build source, hades2 post-1.0)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 11. hades2-hephaestus-blast ───────────────────────────────────────────────
# Hephaestus boon: hits arm delayed explosive tags → massive blast detonation
# Atlas: _MLSSW = unknown attr, melee, low, spiky, solo, wind-up
# POST-CUTOFF: hades2-1.0-2025 + hades2-post1.0-2026
KITS.append({
    "kit_id": "hades2-hephaestus-blast",
    "folk_name": "Hephaestus Blast Core",
    "game": "hades2",
    "status": "positive",
    "atlas_key": "_MLSSW-_SD_-SP-FI-~~",
    "delivery": dc("at-target", 0.45, "hits arm delayed explosion tags on enemy; detonation at enemy position; post-cutoff conf capped"),
    "footprint": dc("small-radius", 0.45, "explosion has small-radius AOE around tagged enemy; post-cutoff conf capped"),
    "geo_text": "Hephaestus boon: each hit arms a delayed explosion tag on the enemy. After a beat, the tag detonates for massive fire burst damage. Rewards slow heavy-weapon play: fewer hits that each arm bigger payloads. Tag-bank grammar (same as Ares Doom in Hades I but fire element).",
    "control": ctrl(["burn"], "rider", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("tag-bank-payout (Hephaestus delayed explosion)", "proc", "n/a", "on_hit",
                    "Proc on hit (no resource cost); tags arm automatically; detonation is automatic after delay. Post-cutoff conf capped — exact delay window and tag mechanics from 1.0 release unknown.", 0.42),
    "element": elem("fire", "hybrid", 0.45),
    "movement": mov(["reposition"], "full-move", False, 0.42),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr blank; post-cutoff conf capped"),
        pc("M", 0.45, "melee heavy weapon base; Hephaestus boon on melee attacks; post-cutoff conf capped"),
        pc("L", 0.45, "low tempo — slow heavy hits that arm large payloads; post-cutoff conf capped"),
        pc("S", 0.45, "spiky amplitude — delayed detonation burst is a single large spike; post-cutoff conf capped"),
        pc("S", 0.45, "solo; tag loop is self-contained; post-cutoff conf capped"),
        pc("W", 0.45, "wind-up — detonation delay is a temporal wind-up analog; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: earliest era = hades2-1.0-2025; conf capped ≤0.50. Fire-element tag-bank grammar (Ares Doom analog but fire). 'Rewards slow heavy-weapon play' per mech_note. Hades II 1.0 released 2025 — post-training-cutoff. ct;sb provenance = content/guide + speed-build sources.",
    "era_confirmed": "hades2-1.0-2025",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Hephaestus boon tiers increase explosion damage; Volcanic Strike (Hephaestus upgrade) may expand explosion footprint (post-cutoff, unconfirmed).",
    "sources_used": ["ct (content/guide corpus)", "sb (speed-build source)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 12. hades2-glorious-disaster ──────────────────────────────────────────────
# Zeus+Apollo duo boon: channel Magick INTO placed cast → repeated lightning
# Atlas: _RMFLC = unknown attr, ranged, med, flat, light-proxy, channel
# POST-CUTOFF: hades2-1.0-2025 + hades2-post1.0-2026
KITS.append({
    "kit_id": "hades2-glorious-disaster",
    "folk_name": "Glorious Disaster (Zeus+Apollo duo)",
    "game": "hades2",
    "status": "positive",
    "atlas_key": "_RMFLC-LLD_-SP-LI-~~",
    "delivery": dc("at-target", 0.45, "placed cast at target location; channel Magick into it for repeated lightning; post-cutoff conf capped"),
    "footprint": dc("large-zone", 0.45, "large-zone lightning from placed cast grows with Magick channel; post-cutoff conf capped"),
    "geo_text": "Zeus+Apollo pair-grain capstone: place a cast at a target location, then channel Magick INTO it for repeated sustained lightning strikes. 'A boss-shredder' per provenance. Light-proxy from Apollo echo effects. Channel Magick investment = escalating lightning output.",
    "control": ctrl(["shock", "stun"], "rider", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("pair-grain capstone (Magick channel investment)", "meter", "focus", "n/a",
                    "Magick channel fed into placed cast drives strike count. Pair-grain requires Zeus + Apollo boon lineages. Channel economy: Magick drains during sustained channel. Post-cutoff conf capped.", 0.42),
    "element": elem("lightning", "hit", 0.45),
    "movement": mov(["low-while-channeling"], "walk", False, 0.42),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr blank; post-cutoff conf capped"),
        pc("R", 0.45, "ranged placed cast; post-cutoff conf capped"),
        pc("M", 0.42, "medium tempo with channel investment; post-cutoff conf capped"),
        pc("F", 0.42, "flat-ish per-strike output while channeling; post-cutoff conf capped"),
        pc("L", 0.42, "light-proxy (Apollo echo effects contribute light proxy layer); post-cutoff conf capped"),
        pc("C", 0.45, "channel commit — Magick channel sustains the lightning loop; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: earliest era = hades2-1.0-2025; conf capped ≤0.50. Pair-grain requires Zeus + Apollo boon lines. Channel Magick into placed cast = unique verb: the cast becomes a Magick sink that multiplies output. Light-proxy from Apollo. Low mobility while channeling (mob=low-while-channeling).",
    "era_confirmed": "hades2-1.0-2025",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Both Zeus and Apollo boon tiers increase lightning strike frequency and damage; Magick regen upgrades extend channel window.",
    "sources_used": ["tt (tutorial/tier-list corpus)", "lr (let's-run/guide corpus)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 13. hades2-hail-storm ─────────────────────────────────────────────────────
# Zeus+Demeter duo boon: freeze triggers repeated lightning strikes
# Atlas: _RMFSI = unknown attr, ranged, med, flat, solo, instant
# POST-CUTOFF: hades2-1.0-2025 + hades2-post1.0-2026
KITS.append({
    "kit_id": "hades2-hail-storm",
    "folk_name": "Hail Storm (Zeus+Demeter duo)",
    "game": "hades2",
    "status": "positive",
    "atlas_key": "_RMFSI-_LM_-SP-CO-~~",
    "delivery": dc("at-target", 0.45, "freeze effect on enemy triggers lightning bolt at enemy location; post-cutoff conf capped"),
    "footprint": dc("large-zone", 0.45, "repeated lightning strikes expand to large-zone coverage; post-cutoff conf capped"),
    "geo_text": "Zeus+Demeter pair-grain capstone: freeze effects repeatedly trigger lightning bolts. Control converted into a damage engine — each Freeze status refreshes triggers additional lightning. Cold + lightning cross-element synergy satisfying Privileged Status.",
    "control": ctrl(["freeze", "shock"], "core", 0.45),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("pair-grain capstone (freeze-proc triggers)", "proc", "n/a", "on_freeze",
                    "Freeze applications trigger lightning procs; no additional resource cost per lightning strike beyond the freeze-application. Post-cutoff conf capped.", 0.42),
    "element": elem("cold/lightning hybrid", "hybrid", 0.45),
    "movement": mov(["kite", "reposition"], "full-move", False, 0.42),
    "prefix_claims": pfx(
        pc("_", 0.50, "Hades attr blank; post-cutoff conf capped"),
        pc("R", 0.45, "ranged cast-based build; post-cutoff conf capped"),
        pc("M", 0.42, "medium tempo; freeze applications pace lightning procs; post-cutoff conf capped"),
        pc("F", 0.42, "flat per-lightning-strike output; post-cutoff conf capped"),
        pc("S", 0.45, "solo; self-contained freeze-to-lightning loop; post-cutoff conf capped"),
        pc("I", 0.45, "instant freeze-proc triggers lightning immediately; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: earliest era = hades2-1.0-2025; conf capped ≤0.50. Zeus+Demeter pair-grain: Demeter provides freeze (cold), Zeus provides chain lightning. Cross-element satisfies Privileged Status (2+ statuses = freeze + shock). Control IS the damage engine: freeze-proc drives lightning throughput.",
    "era_confirmed": "hades2-1.0-2025",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Zeus and Demeter boon tiers increase lightning damage per trigger and freeze duration respectively; Magick upgrades from Zeus expand trigger frequency.",
    "sources_used": ["tt (tutorial/tier-list corpus)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── output ────────────────────────────────────────────────────────────────────
pos  = [k for k in KITS if k["status"] == "positive"]
neg  = [k for k in KITS if k["status"] == "negative"]
pct  = [k for k in KITS if k.get("post_cutoff")]

with OUT.open("w") as f:
    for k in KITS:
        f.write(json.dumps(k) + "\n")

print(f"Hades (1+2): {len(KITS)} records | pos={len(pos)} neg={len(neg)} post-cutoff={len(pct)}")
print(f"Written: {OUT}")

print("\n=== DIRECTED SWEEP RESULTS (Hades 1 + Hades 2) ===")
print("C2 (support-existence): NO pure-support kit in Hades corpus.")
print("  Both games are solo roguelites; duo boons are self-serving damage capstones, not player support.")
print("G2 (line-vs-projectile):")
print("  CHAIN-HOP NOT LINE: hades1-zeus-chain (chain lightning forks = chain-hop, NOT beam)")
print("  NO true beams or lanes in Hades corpus.")
print("D1 (shield-split):")
print("  DODGE: hades1-athena-dash, hades1-merciful-end, hades1-zeus-chain, hades1-aspect-chiron")
print("  GLASS: hades1-ares-doom, hades2-medea-skull-cast, hades2-hephaestus-blast, hades2-hail-storm, hades2-glorious-disaster")
print("  HP-STACK + SUSTAIN-LEECH: hades1-aspect-guan-yu (self-cost contract; leech offsets drain)")
print("  BLOCK: hades1-beowulf-cast (shield weapon provides block chassis)")
print("  OTHER (meta): hades1-privileged-status, hades2-omega-magick")
print("REDUCED CONF (not post-cutoff): hades2-omega-magick (ea-2024 anchor; conf ~0.62)")
print("POST-CUTOFF roster:")
for k in pct:
    print(f"  {k['kit_id']} | {k['era_confirmed']}")
