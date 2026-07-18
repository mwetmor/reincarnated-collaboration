# VDM-1 basin-4 mapping — STEWARD AUDIT, scale wave n02–n05 (gandalf-as-steward, 2026-07-18)

**Verdict: PASS with ONE in-place correction across 41 kits** (n02 11 · n03 10 · n04 10 · n05 10). Basin-4 mapping COMPLETE 52/52 (n01 canary 11 + scale 41). Recounted from committed files (advisory NEVER trusted, D-2c). Depth: **100% mechanical** (all 41 rows via audit-extract) + **~10 kits deep-read** against readonly-DB dossier truth (support-class + Aeromancer + Synergy + genuine-keep clusters).

---

## 1. Histogram recount — ZERO DRIFT (file-truth == advisory, all 4 waves)

| Wave | Kits | EXACT | CLOSE | APPROX | GAPPED | MAPPED | DOCKET |
|---|---|---|---|---|---|---|---|
| n02 | 11 | 0 | 8 | 0 | 3 | 8 | 3 |
| n03 | 10 | 0 | 7 | 1 | 2 | 8 | 2 |
| n04 | 10 | 0 | 9 | 0 | 1 | 9 | 1 |
| n05 | 10 | 1 | 9 | 0 | 0 | 10 | 0 |
| **Σ** | **41** | **1** | **33** | **1** | **6** | **35** | **6** |

**R-M7 biconditional HOLDS on all 41.** The lone APPROX (n03 judgment-paladin) is MAPPED, not MAPPED_DOCKET — the strict biconditional's hard case, correctly handled (attested Punishment DPS loop = "that build, worse" → APPROX; not GAPPED). All 6 GAPPEDs are MAPPED_DOCKET.

**Basin-4 mapping TOTAL (n01+scale): 52 kits — 2E / 41C / 1A / 8G · 44 MAPPED / 8 MAPPED_DOCKET.**

## 2. Element discipline — NEAR-PERFECT + the genuine-keep proof

- **Total element emissions across 41 kits: TWO** — both `fire` on **igniter-sorceress** (n03), and both **GENUINE KEEPS** (verified contiguous): "+18% elemental skill damage, **fire attribute on skills**" + "skills with a **Fire Attribute**" — a damage-type descriptor on a generic effect noun, NOT a skill name. Correctly **window-scoped**: fire only on in-Arcane-Rupture-window burst skills; the Frost's Call generator (used outside the window) stays null. This is the **marquee "the law admits true positives" proof at mapping stage.**
- **Name-only rejection held basin-wide:** reflux-sorceress (7 fire/cold gem names → null), wind-fury-aeromancer (6 wind names → null), demonic-impulse (Blood/shadow → null), deathblow (Lightning Tiger Strike → null, canary-precedent honored). **THE D4 NAME-ONLY LAW is BIDIRECTIONALLY VALIDATED at mapping stage** (rejects name-only ×many + admits the one genuine attested element) — the run's marquee methodological dividend, now proven on both crawl AND mapping of a non-Diablo engine.

## 3. Ailment discipline — correct, with ONE strike (an UNDER-emission)

**Correct emissions (verified enemy-directed against dossier):**
- **curse:amplify** — desperate-salvation-bard (Harp/Sonatina **Brand**), full-bloom-artist (Moonfall "10% Damage increase to enemies" + Drawing Orchids Brand), full-moon-souleater (Deathlord "Amplified Damage on nearby enemies", direction-tested by mapper), liberator-valkyrie (Circle of Truth Brand), shining-knight-valkyrie ("applies Synergy to nearby **enemies**"), surge-deathblade + taijutsu (Synergy applicators), wind-fury (Tornado Synergy). All enemy-anchored (Brand / Synergy-to-enemies), NOT party-anchored auras.
- **poison** — lunar-voice-reaper "Shadow Vortex applies **Poison: Corrosion debuff**" — the ONE genuine LA ailment (named status + enemy-directed). VERIFIED contiguous.
- **chill** — wind-fury Sun Shower "-20% Movement Speed to enemies" → chill (crosswalk line 41: movement-slow → chill). Correct.

**Brand-vs-Aura discrimination HELD (the n01 inoculation working):** mappers correctly WITHHELD curse on party-anchored attack buffs (Artist Sunsketch/Sun Well, Bard Serenade-of-Courage/Heavenly-Tune, Paladin Holy Aura) — these grant the PARTY a buff (self_buff in solo), not an enemy debuff. Affirmative direction-law applications: n03 loyal-companion "+12% Damage… only for yourself" → self_buff (NOT curse:amplify); n04 Red Dust + Wild Stomp → self_buff; n02 souleater Deathlord direction-tested.

**⚠ STRIKE (1) — n02 la-drizzle-aeromancer, 3-ailment UNDER-emission (corrected in-place):** drizzle carried ZERO ailments while its sibling wind-fury-aeromancer (same class, same skills, n05) correctly emitted chill + curse:amplify. drizzle's store attests THREE enemy-directed named effects the mapper withheld:
- Sun Shower "**-20% Movement Speed to enemies**" → `chill` (line 41). Mapper rationale: "NOT named chill in store" — **error: required the literal engine-token word rather than the source mechanism** (the crosswalk translates "-X% Move Speed" → chill).
- Sun Shower "**-10% Attack Power to enemies**" → `curse:weaken` (enemy-damage-reduction, §D Daze-class). Mapper rationale: "not named in 16-registry" — **error: curse:weaken IS the registry token for enemy attack/damage reduction.**
- Tornado "Synergy/Weakness Exposure, maintained" → `curse:amplify`. Mapper rationale: "raid-break vocab (NOT sunder)" — **error: "Weakness Exposure" is NOT in the §LA row-4 boss-break list (Stagger/Weak-Point/Counter/Destruction), and "maintained" implies a persistent damage-amp debuff, not one-shot destruction.** Corrected consistent with wind-fury's same-skill call.

Correction applied; grades/terminal/biconditional UNCHANGED (CLOSE/MAPPED); drizzle row fidelity_notes self-document the correction. **This strike is the MIRROR of the usual leak** — not over-emission from flavor, but UNDER-emission from a too-literal §0-UNIVERSAL reading (demanding the engine-token word in-store instead of the source mechanism the crosswalk translates).

**Boss-break vocab correctly withheld everywhere:** master-summoner (Destruction/Stagger), deathblow, asuras, shock-training-scrapper (Shock ×10+ in store, all suppressed).

## 4. Review-book rulings owed (two)

1. **LA "Synergy" = curse:amplify attestation.** "Synergy" in Lost Ark is a formally-defined mechanic (an enemy-applied damage-taken amplification — the raid-support function that defines these DPS specs), the sibling of "Brand." ACCEPTED as a named mechanic (not flavor) when applied to enemies. **Must be distinguished from Weak-Point / Stagger / Counter / Destruction boss-break vocab (§LA row 4).** Caveat flagged: "Weakness Exposure" (Aeromancer Tornado) ruled damage-amp, not Weak-Point — confirm at book.
2. **Crosswalk line-41 salience — the source-mechanism-not-token-word principle.** The drizzle strike shows mappers can require the literal engine-token word ("chill") rather than recognizing that the SOURCE mechanism ("-X% Move Speed") is what must be named, with the crosswalk performing the translation. Parallel to the n01 DEBUFF-DIRECTION hardening: the rule exists but isn't salient. **Candidate: a salient §LA callout in the basin-5 addendum** — "movement-slow (any '-X% Move Speed' to enemies) → chill; enemy attack/damage-reduction → curse:weaken; you attest the SOURCE effect, the crosswalk supplies the token." (NOT applied to the main crosswalk mid-run — load-bearing across all basins; book-adjudicated.)

## 5. Soft notes (advisory, no strike)

- **master-summoner** (n03, GAPPED) resource_economy carries a `note` key — non-native (R-M4 prefers native gauge keys; meta belongs in fidelity_notes). On a docketed kit; cosmetic.
- **taijutsu-scrapper** (n05) consequence_type `self_buff` (sustained unlimited-resource uptime) vs sibling shock-training-scrapper `burst_window` — author-judged from dominant-loop; defensible.

## 6. Contiguity battery — CLEAN

Load-bearing quotes verified contiguous in-store: igniter "fire attribute on skills" · lunar-voice "Poison: Corrosion debuff" · wind-fury + drizzle Sun Shower "-20% Movement Speed to enemies" (both specs, identical wording — the consistency anchor) · shining-knight "applies Synergy to nearby enemies" · blessed-aura Holy Aura "grants your whole party… +10% Damage dealt to enemies" (the party-anchored self-check — confirms the n01 Holy Aura → [] correction was NOT an over-correction). No splices detected.

---

**Signed:** gandalf (steward) · basin-4 mapping scale wave n02–n05 PASS · 1 correction (drizzle under-emission) · 2 review-book rulings owed · igniter-fire + lunar-voice-poison genuine-keeps confirmed · **basin-4 mapping COMPLETE 52/52, ready for INGEST-16.**
