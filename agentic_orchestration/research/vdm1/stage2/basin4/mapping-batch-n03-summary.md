# VDM-1 basin-4 mapping batch n03 — summary

**Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR) · **Batch:** 10 kits

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 7 | grace-empress-arcanist, gravity-training-destroyer, hunger-reaper, igniter-sorceress, loyal-companion-sharpshooter, lunar-voice-reaper, mayhem-berserker |
| APPROX | 1 | judgment-paladin |
| GAPPED | 2 | liberator-valkyrie, master-summoner |

**MAPPED / MAPPED_DOCKET split:** 8 MAPPED · 2 MAPPED_DOCKET (liberator-valkyrie, master-summoner). R-M7 biconditional honored: all GAPPED = MAPPED_DOCKET; APPROX = MAPPED. No APPROX+DOCKET hybrid.

---

## Per-kit one-liners

| kit_id | grade | one-liner |
|---|---|---|
| la-grace-empress-arcanist | CLOSE | Apply-consume-pair mark chassis (4 Ruin stacks detonate); Card Deck stochastic variance layer (Judgment/Cull/Royal cards) captured in fidelity_notes — no engine token. |
| la-gravity-training-destroyer | CLOSE | Two-stage economy (3 cores -> gravity gauge -> Hypergravity burst_window); Stagger/Counter = boss-break (NOT stun); left-click basic-attack dominant phase is novel delivery texture. |
| la-hunger-reaper | CLOSE | Chaos Meter -> 100% -> 15s Chaos Mode (burst_window with refresh-on-hit near-permanence); back-attack positional is delivery texture; no ailment/element attested. |
| la-igniter-sorceress | CLOSE | GENUINE fire keep: "+18% elemental skill damage, fire attribute on skills" on Arcane Rupture burst_window row; generator names (Inferno/Seraphic Hail/Frost's Call) are NAME-ONLY — element null on generator rows; pre-cast Doomsday timing nuance noted. |
| la-judgment-paladin | APPROX | Negative kit (CONFIRMED); Punishment DPS shell on support chassis — attested loop is sparse melee-arc/Piety-meter-directed-to-self; 'that build, worse' by design intent; no curse:amplify (Brand belongs to Blessed Aura/Sword of Justice, not Judgment dossier). |
| la-liberator-valkyrie | GAPPED | Fourth support pillar (post-cutoff Valkyrie August 2025); party heal/shield/cleanse cannot map in solo engine; Circle of Truth Brand -> curse:amplify correctly emitted (enemy-directed debuff); GAPPED on dominant identity. |
| la-loyal-companion-sharpshooter | CLOSE | Silverhawk "+12% Damage to the boss, only for yourself" = SELF buff (ally/self deals more) = self_buff NOT curse:amplify (DIRECTION TEST passed; contrast n01 Death Strike "27% Increased Damage to the Boss" which was enemy-directed amplify). Negative kit; companion-uptime loop maps as COMPANION_CONTRACT. |
| la-lunar-voice-reaper | CLOSE | POISON ATTESTED: "Shadow Vortex applies Poison: Corrosion debuff" (capstone_alterations dossier, abstained=0) — one genuine LA ailment in-basin; emitted. Persona (Z) = TIMED burst_window (single-Swoop payoff). persona_meter native economy. |
| la-master-summoner | GAPPED | summoner-deferral GAPPED per hot-fact; Ancient Elemental spirits as primary damage proxies have no solo loop; skills[] empty per empty-projection convention; economy note preserves orb-pool and Ancient Spear loop shape. |
| la-mayhem-berserker | CLOSE | PERMANENT Burst Mode = self_buff steady-state + HP-lock economy cost-note (NOT timed burst_window, NOT resource spend); nested Red Dust 8s = burst_window; DEFENSIVE_TRADEOFF + SACRIFICE_ASCENDANCY T4 doors capture HP-trade identity shape. |

---

## T4-door frequency (n03)

| T4 door | Count | Kits |
|---|---|---|
| TEMPORAL_CHARGE | 8 | grace-empress, gravity-destroyer, hunger-reaper, igniter-sorceress, judgment-paladin, loyal-companion, lunar-voice, master-summoner |
| MOMENTUM_CASCADE | 3 | grace-empress, hunger-reaper, loyal-companion |
| DEFENSIVE_TRADEOFF | 3 | gravity-destroyer, liberator-valkyrie (via NETWORK_AMPLIFIER), mayhem-berserker |
| NETWORK_AMPLIFIER | 1 | liberator-valkyrie |
| RESONANCE_LOOP | 1 | liberator-valkyrie |
| ELEMENT_CONVERSION_MONO | 1 | igniter-sorceress |
| COMPANION_CONTRACT | 1 | loyal-companion |
| PERSISTENCE_ENGINE_saturation | 1 | lunar-voice |
| PROXY_ASCENSION | 1 | master-summoner |
| SACRIFICE_ASCENDANCY | 1 | mayhem-berserker |

TEMPORAL_CHARGE dominates (8/10 kits) — expected for LA's universal meter-accumulation pattern.

---

## Candidates

**Docket candidates:** 2 entries in `docket-candidates-batch-n03.jsonl`
- `support-class-identity`: liberator-valkyrie + judgment-paladin (standing class from n01)
- `summoner-deferral`: master-summoner (standing class from n01)

**Mint candidates:** 0 (no novel mechanism warranting quantitative or qualitative mint; stochastic Card Deck layer noted in fidelity_notes but compresses into apply-consume-pair without requiring a new token; refresh-on-hit Chaos Mode captured in fidelity_notes).

---

## §0 near-misses (elements/statuses wanted but not attested)

These were tempting but correctly struck per D4 NAME-ONLY LAW:

- **grace-empress-arcanist:** "Celestial Rain," "The Devil," "Serendipity" — all skill names; no damage-typing. Wanted arcane/shadow — struck.
- **gravity-training-destroyer:** "Gravity" appears throughout — class mechanic label, not element; "Earth Wave" = skill name; "Vortex Gravity" = skill name. Wanted earth — struck.
- **hunger-reaper:** "Chaos" pervasive — class mechanic label. Wanted shadow — struck.
- **igniter-sorceress generators:** "Inferno," "Seraphic Hail," "Frost's Call" — skill names; no damage-typing on generators. Wanted fire/holy/cold — struck on generator rows. Fire KEPT only on Arcane Rupture row where damage-typed.
- **liberator-valkyrie:** "Wings of Liberation," "Divine Confirmation," "Blessing of Salvation" — skill names; no holy damage-typing. Wanted holy — struck.
- **loyal-companion-sharpshooter:** "Fenrir's Messenger," "Wings of Storm," "Silverhawk" — skill/companion names. Wanted wind/lightning — struck.
- **lunar-voice-reaper:** "Moonscent," "Two Moons," "Glowing Brand," "Shadow Vortex" — Ark Grid set + skill names. Shadow Vortex correctly emitted `poison` via Poison: Corrosion DoT attestation (not shadow element — the status is attested, the element is not).
- **master-summoner:** "Ancient Elemental," "Phoenix," "Water Elemental," "Electric Storm," "Earth Collapse" — skill/spirit names. Wanted fire/water/lightning/earth — all struck.
- **mayhem-berserker:** "Hell Blade," "Dark Rush," "Overdrive" — skill names. Wanted shadow/dark — struck.

**Total element near-misses this batch: 9 kits (igniter-sorceress is the sole element keep). Validates basin-4 element-null default law.**

---

## Key decisions called explicitly

**igniter-sorceress fire KEEP:** "+18% elemental skill damage, fire attribute on skills" during Arcane Rupture — damage-type descriptor on generic noun "skills" = GENUINE KEEP per §0.4. Generator rows (Inferno/Seraphic Hail/Frost's Call) are NAME-ONLY — element null there. element_secondary stays null (no second element damage-typed in store per addendum residual OPEN).

**lunar-voice-reaper poison EMIT:** "Shadow Vortex applies Poison: Corrosion debuff" in capstone_alterations dossier (abstained=0, synergy field). "Poison: Corrosion" names the DoT status; "debuff" confirms enemy-directed. Per addendum residual OPEN: emit `poison` when the fetched line attests the DoT status. This is the ONE genuine LA ailment attestation in-basin. Moonscent/Two Moons are Ark Grid set names — not element attestation.

**loyal-companion Silverhawk DIRECTION TEST:** "+12% Damage Increase to the boss, only for yourself" — "only for yourself" is the decisive phrase: ally/self deals more (outgoing player damage buff), NOT enemy-directed (enemy takes more). Result: self_buff. Contrast n01 Death Strike: "27% Increased Damage to the Boss" without self-qualification was adjudicated curse:amplify because the store described it as a debuff on the enemy. The distinction is source-text DIRECTION — LC dossier attests a player-outgoing buff.

**judgment-paladin APPROX (not GAPPED):** Attested Punishment DPS loop exists (sparse but present); negative_canon confirmed; identity maps as 'that build, worse by design intent' per player test. GAPPED requires 'not that build.' The loop's existence (however sub-par) keeps it at APPROX. No curse:amplify — Sword of Justice Brand belongs to Blessed Aura identity, not Judgment dossier.

**mayhem-berserker PERMANENT vs TIMED split:** Burst Mode = permanent self_buff (HP-locked-at-25% standing state, per hot-fact and LA row 2). Red Dust 8s = NESTED burst_window inside permanent state. HP-lock is economy cost-note, NOT a resource spend. Two-layer structure noted in fidelity_notes.

---

## Anything forced

- **judgment-paladin APPROX:** The only APPROX in-batch. Forced by presence of attested (if weak) DPS loop — cannot GAPPED without violating R-M7 player test. The negative_canon rides the review book.
- **master-summoner empty-projection:** skills[] empty forced by summoner-deferral hot-fact and §E.3. Motion_frame preserves the loop description for review context.
- **lunar-voice poison:** Forced-emit (positive force) — the one attested ailment; the addendum residual OPEN explicitly anticipated this call and authorized emit if DoT status named in store. Status confirmed.
