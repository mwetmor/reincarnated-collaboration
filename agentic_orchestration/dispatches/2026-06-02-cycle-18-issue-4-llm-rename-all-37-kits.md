# Dispatch — 2026-06-02 — cycle-18 — Issue 4 — LLM rename pass on all 37 QDX-5 kits

**From:** knight-rider (orchestrator)
**To:** gandalf-as-subagent (story-and-design steward executing the rename pass)
**Authority:** Matt 2026-06-02 verbatim "yes, let's do it all" + verbatim "Caster is WAY too generic; LLM should come up with unique variations on what type of 'caster' they are; same goes for Cleric and others" + verbatim "Remove flavor element names from prefixes" → gandalf transmission with embedded LLM prompt
**Wave:** cycle-18 Drax QDX-7-AMEND-FULL — Phase 1 (parallel with Issue 5A + Gate-1)
**State file:** `agentic_orchestration/cycle-18-drax-amend-full/wave-state.md`
**Tag intent:** none (data amendment; auto-commit per cycle-push pattern)
**Estimated horizon:** ~0.5-1 session
**Estimated cost:** ~$0.30 LLM (37 kits × ~$0.008 per Wave B-style rename)

---

## 1. Authoritative reading

1. **`agentic_orchestration/cycle-18-drax-amend-full/wave-state.md`** § 2 Issue 4 + § 5 LOCK L escape
2. **gandalf transmission 2026-06-02** (Matt's session input; contains the LLM prompt below verbatim)
3. **`canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`** § 2 (Q18 vocabulary — consumed INVERTED by this prompt as avoid-list)
4. **`~/Games/reincarnated-engine/data/kit_space/kits/`** — 37 QDX-5 kit JSONs (filter to event `kse_20260602_008`)
5. **Matt 2026-06-01 authority context** verbatim: "flavor element = applied only means to use it within the naming of the skill. A character/kit does not need to have a flavor element tag at all"

---

## 2. Target seam + scope

**Owner seam:** gandalf-as-subagent (story-and-design steward; per LOCK D canonical authoring authority extending to LLM prompt design + per-kit content amendment for this specific rename pass)

**Target files:**
- `~/Games/reincarnated-engine/data/kit_space/kits/kit_<primary>_<seq6>.json` × 37 (event_008 filter; verify FK linkage `kit_space_expansion_event_id == "kse_20260602_008"`)

**Scope:**

For each of the 37 QDX-5 kits, fire the embedded LLM prompt with kit context substituted. Replace the `emergent_kit_concept` field in each kit JSON with the new LLM-generated name. Preserve all other fields unchanged. Auto-commit + push at end.

**Out of scope (CRITICAL):**
- Any other field amendment (skills, t4_selection, balance_metadata, etc. — preserve unchanged)
- Any kit NOT in event_008 (preserve historical kits unchanged per Path α)
- Any change to chronicle event_008 metadata
- Any change to Q18 vocabulary lock (IMMUTABLE per canonical lock)

---

## 3. LLM rename prompt (gandalf-authored; embed verbatim from Matt's transmission)

For each of the 37 kits, fire this prompt with kit context substituted:

```
You are renaming a fantasy ARPG character kit. Produce a single emergent
identity name (4-7 words) per the rules below.

KIT CONTEXT:
  - primary_element: {primary_element}
  - cultural_tradition: {cultural_tradition} (may be NA)
  - period: {period} (may be NA)
  - bc_target_cell: {bc_target_cell}
  - sample skill themes: {first 3 skill names from kit JSON}

HARD RULES (violation = regenerate):

  1. DO NOT use any Q18 flavor element word as prefix or in name.
     AVOID THESE WORDS (full Q18 allow-list):
     fire: ember, cinder, blaze, scorch, inferno, ignite, fira, lava,
           magma, charcoal, char, brand, flare, fusion, thermal, combustion
     water: tide, torrent, glacial, brine, aqua, frost, chill, mist, ice,
            glacier, wave, marsh, hydro, hydraulic
     earth: stone, granite, marble, clay, sand, iron, gold, silver, lead,
            gem, crystal, obsidian, amber, quake, tremor, thorn, seismic,
            tectonic
     wind: tempest, cyclone, whirlwind, gale, gust, squall, hurricane,
           zephyr, hail, sleet, cloud, sonic, shockwave
     lightning: arc, static, surge, volt, bolt, shock, spark, thunder,
                plasma, flash, ion, voltage, tesla
     holy: radiance, radiant, dawn, aura, divine, sacred, blessed, lux,
           celestial, stellar, solar, photon, laser, prismatic
     shadow: void, shade, wraith, drain, necrotic, abyss, shadow, lich,
             blackhole, singularity, darkmatter, soul
     physical: pierce, piercing, slash, slashing, bludgeoning, sever,
               strike, force, bleed

     ALSO AVOID etymological family of removed entries:
     umbra, umbral, penumbra (removed at PG-3 2026-06-01 Matt verbatim
     'this term has little meaning to me')

  2. DO NOT use generic archetype labels:
     AVOID: Caster, Cleric, Mage, Warrior, Knight, Bearer, Fighter,
            Warden, Champion, Master, Adept, Apprentice

     INSTEAD: invent a UNIQUE role/archetype word specific to this kit's
     identity. Examples of acceptable invented archetypes:
       - Eclipsist (shadow-themed; invented; not generic)
       - Hearthwarden (fire-themed; specific role)
       - Soulreaver (shadow-themed; specific action)
       - Tideturner (water-themed; specific action)
       - Stoneghast (earth-themed; specific concept)
       - Lightreader (holy-themed; specific function)
       - Sparkwright (lightning-themed; specific maker-role)
       - Stormcaller (wind-themed; specific calling action)
       - Voidreader (shadow-themed; specific function)
     Each kit gets its OWN unique archetype variation.

  3. Maintain 'of the X' suffix pattern if it adds setting/lore weight.
     Acceptable: 'Eclipsist of the Dusk Meridian'
     Acceptable: 'Hearthwarden of the Scorched Reach'
     Skip suffix if no lore anchor available.

THEMATIC GUIDANCE:
  - Anchor in primary element identity WITHOUT using flavor pool words
  - Use mythological / classical / fantasy literary register
  - Avoid modernisms (corporate / sci-fi unless modern-caster theming
    explicit per substrate inputs)
  - Cohesion with cultural_tradition + period when populated

OUTPUT: single line. The new emergent_kit_concept value. Nothing else.
```

---

## 4. Acceptance criteria

### 4.1 Functional

1. **All 37 kit JSONs amended** — verify by listing `data/kit_space/kits/` filtered to event_008 (37 files; check `kit_space_expansion_event_id` field)
2. **Each kit's `emergent_kit_concept` field replaced** with the LLM rename output
3. **All other fields preserved unchanged** (skills, t4_selection, balance_metadata, faction-related fields, FK linkage, etc.)
4. **Output uniqueness check** — no two kits share an `emergent_kit_concept` value (within-event uniqueness)
5. **Q18 word check** — verify post-rename `emergent_kit_concept` strings against full Q18 allow-list; ANY match = regenerate that kit
6. **Generic-archetype check** — verify post-rename strings do NOT contain Caster/Cleric/Mage/Warrior/Knight/Bearer/Fighter/Warden/Champion/Master/Adept/Apprentice; ANY match = regenerate
7. **Etymological-family check** — verify post-rename strings do NOT contain umbra/umbral/penumbra; ANY match = regenerate

### 4.2 Tests + bounds

8. **Cost actual ≤ $0.60** (vs $0.30 projection; LOCK R 2× upper-bound)
9. **Wall-clock ≤ 30 min**
10. **Auto-commit + auto-push** per cycle-push pattern at end

### 4.3 Sample-inspection-ready

11. **Top-1 sample inspection** — for `kit_shadow_000007` (gandalf-curated top-1), report new `emergent_kit_concept` value + cross-check against Q18 + generic-archetype lists
12. **Top-5 sample inspection** — for each of `kit_fire_000007`, `kit_wind_000006`, `kit_holy_000005`, `kit_physical_000026`, report new value (Issue 3 drax will consume these)

---

## 5. Cross-seam impact

- **Engine seam (rocket):** kit JSONs are engine output; this is a content amendment to existing files (additive in the sense that the rename PROPERLY assigns identity; replaces the prior in-place value)
- **Drax seam (Phase 2 dependent):** drax CONSUMES the renamed values via `useKitSpaceData.ts` and renders `emergent_kit_concept` field; no API change; drax sees the new value automatically once sync'd to `public/kit-space/`
- **Drax sync requirement:** Phase 2 drax dispatch will copy `data/kit_space/kits/` → `reincarnated-loadout/public/kit-space/kits/` to pick up renames

---

## 6. LOCK L iteration discipline

Per gandalf transmission: "LOCK L applies: 2+ Gate-2 BLOCKs on rename quality → Matt aesthetic judgment escalation."

If jack-ryan Gate-2 BLOCKs on rename output (e.g., template-repeat post-rename; OR systematic Q18 leakage; OR systematic generic archetype recurrence):
- **1st BLOCK:** gandalf re-fires the prompt with refinement within seam authority (no Matt-touch)
- **2+ BLOCKs:** Matt escalation per LOCK L escape clause

---

## 7. Required completion record

On work-completion, append a completion record to this dispatch file with:

```markdown
## Completion record

**Completed by:** gandalf-as-subagent (date)
**Engine commit:** `<sha>` (auto-commit + push)
**Kits amended:** <n>/37
**LLM cost actual:** $<x> (vs $0.30 projection)
**Wall-clock:** <y> min
**Output uniqueness:** PASS / FAIL (cross-kit emergent_kit_concept duplicates)
**Q18 word check:** PASS / FAIL (per-kit; list any matches)
**Generic-archetype check:** PASS / FAIL (per-kit; list any matches)
**Etymological-family check:** PASS / FAIL (per-kit; list any matches)
**Regenerations needed:** <n> (kits requiring re-fire due to rule violation)
**Top-1 + top-5 sample inspection:**
  - kit_shadow_000007: <new value>
  - kit_fire_000007: <new value>
  - kit_wind_000006: <new value>
  - kit_holy_000005: <new value>
  - kit_physical_000026: <new value>
**Gate-2 readiness:** READY / NEEDS-ITERATION
**LOCK L disposition:** 0 BLOCKs / 1 BLOCK seam re-fire / 2+ BLOCKs Matt escalation
**Notes for drax Phase 2:** <any consumer-side observations>
**Notes for jack-ryan Gate-2:** <any specific kits worth sample-inspection>
```

---

## 8. Quality criterion

**Game-quality goal this dispatch serves:** the 37 kit identities transition from "Element + Generic Archetype + 'of the X'" template (e.g., "Penumbra Caster of Dusk Meridian", "Cannonade Cleric of Scattered Light") to "Invented Unique Archetype + 'of the X'" form (e.g., "Eclipsist of the Dusk Meridian", "Lightreader of the Open Field") where:
- No Q18 flavor element word appears in the identity (flavor is for SKILL names, not identity)
- No generic archetype label flattens the kit's individuality
- Each kit's archetype variation is unique to that kit

**Refutation conditions** (gandalf surfaces if any apply):
- LLM produces template-repeat across kits despite varied input context (signals prompt design issue → LOCK L iteration)
- LLM systematically falls back to a different generic word not in the avoid-list (e.g., "Adept" if Apprentice avoided; new generic emerges → refine avoid-list)
- Q18 word leakage detected post-fire on multiple kits (signals prompt failure → LOCK L iteration)
- Cost projection exceeds $0.60 actual (LOCK R 2× escape)

---

**End of Issue 4 dispatch.**
