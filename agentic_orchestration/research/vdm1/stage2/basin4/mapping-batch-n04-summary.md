# VDM-1 basin-4 mapping batch n04 — summary

**Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR) · **Kits:** 10 · **Batch mirrors crawl batch 04**

---

## Grade histogram

| Grade | Count | Kit IDs |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 9 | nights-edge-souleater, order-emperor-arcanist, perfect-suppression-shadowhunter, phantom-beast-awakening-wildsoul, pinnacle-glaivier, predator-slayer, punisher-slayer, rage-hammer-destroyer, rage-hammer-destroyer-bt |
| APPROX | 0 | — |
| GAPPED → MAPPED_DOCKET | 1 | peacemaker-gunslinger |

**R-M7 biconditional check:** GAPPED ⟺ MAPPED_DOCKET — 1 kit, 1 docket entry. APPROX+MAPPED_DOCKET hybrid = 0 (OUTLAWED — clean). terminal_state: MAPPED = 9, MAPPED_DOCKET = 1.

---

## Per-kit one-liners

| Kit | Grade | One-liner |
|---|---|---|
| la-nights-edge-souleater | CLOSE | Edge Meter gauge → Soul Snatch burst_window; Ghast-skill melee cycle; Night's Edge suppression-twin of Full Moon; no element, no ailments |
| la-order-emperor-arcanist | CLOSE | Card Deck meter → constant card-draw loop; Emperor card cash-in; delayed-damage signature; engraving axis DEAD; Destruction tag = boss-break delivery_notes only |
| la-peacemaker-gunslinger | GAPPED | Irreducible 3-stance rotation (Pistol/Shotgun/Rifle) is the identity — no dominant mode; mode-swap-identity docket filed |
| la-perfect-suppression-shadowhunter | CLOSE | Shadowburst Meter cycle; priority-list system; Demonize permanently suppressed; physical-null element; PHASE_MOMENTUM suppression shape |
| la-phantom-beast-awakening-wildsoul | CLOSE | Phantom Beast Awakening gauge → TIMED burst_window; Spirit stacks (CDR/mana per stack); Fox/Bear skill families element-null (Fox Flame = name-only) |
| la-pinnacle-glaivier | CLOSE | Dual Meter → stance-swap self-buffs; Focus/Flurry alternation; buff values STALE (shape only per addendum CONTRADICTED verify row) |
| la-predator-slayer | CLOSE | Fury Meter → TIMED Burst Mode; Fatigue stacks reduce Exhaustion downtime; sustained uptime emphasis; Volcanic/Flame skill names element-null |
| la-punisher-slayer | CLOSE | Fury Meter → shorter cyclical Burst windows; Specialization-heavy; Guillotine-priority rotation; Wild Stomp direction-tested → self_buff not curse |
| la-rage-hammer-destroyer | CLOSE | 3-core builder-spender; Gravity Release empowered hits; Gravity = class mechanic not element; TEMPORAL_CHARGE + RESOURCE_CONVERSION |
| la-rage-hammer-destroyer-bt | CLOSE | CONTRADICTED-negative slot; attested BT Berserker identity mapped per §E.5; Red Dust direction-tested → self_buff; negative story rides review book |

---

## T4 door frequency (n04 batch)

| T4 door | Count | Kits |
|---|---|---|
| TEMPORAL_CHARGE | 9 | all except peacemaker (GAPPED) |
| MOMENTUM_CASCADE | 3 | nights-edge, phantom-beast-awakening, predator-slayer |
| PHASE_MOMENTUM | 4 | perfect-suppression, pinnacle-glaivier, punisher-slayer, rage-hammer-destroyer-bt |
| RESOURCE_CONVERSION | 2 | order-emperor-arcanist, rage-hammer-destroyer |

Note: TEMPORAL_CHARGE appears on 9/10 kits — consistent with the gauge-identity pattern dominant across LA (§LA row 1). PHASE_MOMENTUM clusters on suppression/stance-alternation/cycle-variant kits.

---
## Candidate side-files

**docket-candidates-batch-n04.jsonl:** 1 entry
- `mode-swap-identity` — la-peacemaker-gunslinger: 3-stance rotation (Pistol/Shotgun/Rifle) irreducible; destination: review-book §LA row 3

**mint-candidates-batch-n04.jsonl:** not created (0 entries — no quantitative or qualitative mint candidates surfaced in this batch)

---

## §0 near-misses — elements/statuses you WANTED to emit but could not attest

**Element near-misses (all D4 NAME-ONLY LAW strikes):**
- **Volcanic Eruption** (predator-slayer, punisher-slayer) — wanted `fire`; "Volcanic" is skill proper name, zero fire damage-typing in dossier → null
- **Flame Deathblade** (predator-slayer) — wanted `fire`; "Flame" is part of skill proper name; no fire damage descriptor → null
- **Fox Flame** (phantom-beast-awakening-wildsoul) — wanted `fire`; "Fox Flame" is skill proper name with zero fire damage-typing → null
- **Earth Eater** (rage-hammer-destroyer) — wanted `earth`; "Earth" is skill proper name; Gravity mechanic is class system, not element family → null
- **Windsplitter** (pinnacle-glaivier) — wanted `wind`; "Windsplitter" is skill proper name, no wind damage-typing → null
- **Bloody Rush / Dark Resurrection** (rage-hammer-destroyer-bt, order-emperor-arcanist) — "Shadow/Dark" = skill name register; zero shadow damage-typing → null
- **Shadow Shards / Shadow Injection** (perfect-suppression-shadowhunter) — named buff mechanics; zero shadow damage-typing → null; Shadowburst Meter = resource name, not element

**Ailment near-misses:**
- **Weakness Exposure** (peacemaker-gunslinger, pinnacle-glaivier) — boss-break synergy vocabulary (§LA row 4); wanted to emit `sunder` or `curse:sap`; NOT a 16-ailment — raid-encounter debuff mechanic → delivery_notes only
- **Destruction** (order-emperor-arcanist, pinnacle-glaivier) — boss-break vocab (§LA row 4); NOT `sunder` — wanted to emit; delivery_notes only
- **Wild Stomp damage amplification synergy** (punisher-slayer) — wanted `curse:amplify`; DIRECTION TEST: party synergy buff = self_buff; enemy not the recipient → no curse emitted (correct)
- **Red Dust 8s damage amplification** (rage-hammer-destroyer-bt) — wanted `curse:amplify`; DIRECTION TEST: self-cast on player → self_buff only; not enemy-directed → no curse emitted (correct)

---

## Forced calls / discipline notes

1. **rage-hammer-destroyer-bt CONTRADICTED-negative:** corpus folk_name is "Berserker's Technique vs Mayhem (negative twin note)", negative=1, but verify_ledger has TWO negative_canon=CONTRADICTED rows. Mapped attested BT Berserker identity per addendum §E.5. The kit_id containing "rage-hammer-destroyer" is a misfiled slot (mech_note: "NOT a record"). Negative story and slot-malformation ride review book only.

2. **Pinnacle-glaivier buff values STALE:** verify_ledger CONTRADICTED row on mechanics signals stale buff numbers (mech_note values: +20%/+50% vs fetched +25%/+60%). Mapped SHAPE only per addendum ("pinnacle stale buffs — map shape only"). Numbers excluded from mapping_json entirely.

3. **Order-emperor-arcanist engraving DEAD axis:** "Order of the Emperor" was an engraving removed in 2025. Dossier capstone_alterations confirms: "Class engravings Empress's Grace and Order of the Emperor removed; replaced by Enlightenment tree." Spec identity is the PLAYSTYLE (constant card-draw loop, Emperor cash-in) not the engraving name. No engraving differentiation axis used.

4. **Peacemaker-gunslinger GAPPED rationale:** "Pacifist unifies and empowers these buffs, granting all of them regardless of which stance you are in" was a near-approximation candidate — but the buffs are STILL stance-specific in VALUE (Shotgun +10% Crit +24% Damage; Rifle +28% Damage; Handgun +16% Attack Speed) and the rotation through all three stances is the point. Player who plays Peacemaker and gets a single-dominant-mode mapping is playing "not that build." GAPPED is correct.

5. **§LA DEBUFF-DIRECTION LAW fired twice:** Wild Stomp (punisher-slayer) and Red Dust (rage-hammer-destroyer-bt) both tested — both correctly resolved to self_buff, no curse emitted.

---

## Batch-level observations

- **TEMPORAL_CHARGE dominance (9/10):** LA's gauge-identity economy is pervasive — every non-GAPPED kit accumulates a meter of some kind before activating a damage state. This is the basin's structural signature.
- **Zero genuine ailments this batch:** no ailment emitted across all 10 kits. All status-adjacent language was either boss-break vocab (§LA row 4) or name-only. The §LA residual OPEN (lunar-voice poison) remains the sole in-basin ailment candidate and is in n03 (prior batch).
- **Zero genuine elements this batch:** all 10 kits map element_primary=null. Multiple name-only near-misses (Volcanic, Flame, Fox Flame, Earth, Windsplitter). D4 NAME-ONLY LAW validated again.
- **Direction-law fires confirmed clean:** two direction-test events (Wild Stomp, Red Dust) both resolved correctly without curse emission — n01 canary lessons held.
