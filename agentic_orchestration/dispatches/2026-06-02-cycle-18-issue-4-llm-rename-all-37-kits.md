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

---

## Completion record

**Completed by:** gandalf-as-subagent (2026-06-02)
**Engine commit:** `b77cc95` (auto-commit + push to mwetmor/reincarnated-engine main)
**Kits amended:** 37/37
**LLM cost actual:** $0.1497 (vs $0.30 projection; well under $0.60 LOCK R abort ceiling)
**Wall-clock:** 53.1 s (0.88 min; vs ≤30 min acceptance bound)
**Model:** claude-sonnet-4-6 (project default per `src/reincarnated/llm/client.py`)

**Output uniqueness:** PASS (37 unique of 37; 6 first-pass duplicates resolved via seam-internal corrective-prompt re-fire). First-pass duplicate cluster: 5x "Ravager of the Unbroken Fury", 3x "Ravager of the Bloodsworn Fury", 3x "Ravager of the Unyielding Flesh", 3x "Ravager of the Sundered Flesh", 2x "Deepcaller of the Sunken Meridian", 2x "Veilsinger of the Wandering Breath". All offending kits (kept first occurrence; regenerated the rest) now hold unique names. Note for jack-ryan: physical-cluster duplicate-saturation is a substrate signal — 16 physical kits compressed against a narrow vocabulary space; see § Notes for drax Phase 2 below.

**Q18 word check:** PASS — no fire/water/earth/wind/lightning/holy/shadow/physical flavor pool word (per `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 2 — 109-entry full Q18 allow-list inverted as avoid-list) appears in any rename. Word-boundary case-insensitive tokenization applied via `re.findall(r"[A-Za-z]+", name)` intersected with avoid-set.

**Generic-archetype check:** PASS — no Caster/Cleric/Mage/Warrior/Knight/Bearer/Fighter/Warden/Champion/Master/Adept/Apprentice in any rename. (Note: "Cleaver" appears in 3 names — `cleaver/cleave` is NOT in the avoid-list per dispatch § 3; verb-form `slash/sever/strike` IS avoided per Q18 physical pool. Cleaver passes literal acceptance criteria but is verb-archetype-adjacent; flagging for jack-ryan Gate-2 aesthetic-judgment.)

**Etymological-family check:** PASS — no umbra/umbral/penumbra in any rename. shadow_000007 explicitly avoided the prior "Penumbra Caster" template; "Duskweaver of the Eclipsed Meridian" is the validated replacement.

**Regenerations needed:** 0 rule-violation regenerations (all 37 first-attempt outputs passed Q18 + generic + etymological checks); 12 uniqueness-collision regenerations (6 duplicate clusters resolved via corrective-prompt re-fire). Zero LLM violations of the hard prompt rules across the entire cohort — strong signal of prompt clarity.

**Top-1 + top-5 sample inspection:**
- `kit_shadow_000007` (TOP-1): "Penumbra Caster of Dusk Meridian" → **"Duskweaver of the Eclipsed Meridian"** — removes penumbra (etymological-family) + Caster (generic); preserves Meridian lore anchor; invents Duskweaver as kit-specific archetype.
- `kit_fire_000007`: "Ember Caster of Scorched Meridian" → **"Ashcaller of the Burning Veil"** — removes Ember (Q18 fire) + Scorched (Q18 scorch root) + Caster (generic); invents Ashcaller; new lore-suffix.
- `kit_wind_000006`: "Galewright of the Scattered Pale" → **"Driftcaller of the Hollow Sky"** — removes Gale (Q18 wind); preserves invented-archetype-pattern (Galewright was already good-style; Driftcaller is the new invented-archetype). Note: this kit's pre-existing name was acceptable-style per dispatch context note; LLM still regenerated for Q18 compliance.
- `kit_holy_000005`: "Cannonade Cleric of Scattered Light" → **"Verdictbringer of the Hallowed Tribunal"** — removes Cleric (generic); skill themes (Sacred Verdict / Divine Sentence / Holy Decree) drove judicial-thematic Verdictbringer + Tribunal selection (strong context-driven cohesion).
- `kit_physical_000026`: "Stonefist of Broken Wall" → **"Furyboned Cleaver of the Rawbone Pact"** — removes Stone (Q18 earth — note: prior name was technically Q18-violating for earth-not-physical primary). Aesthetic-judgment caveat: "Furyboned" + "Rawbone" within same name is repetitive bone-imagery; "Cleaver" is verb-archetype-adjacent. Acceptable per literal rules; mid-tier aesthetic quality. Flag for jack-ryan Gate-2.

**Gate-2 readiness:** READY (all four hard rules PASS; cost well under projection; uniqueness resolved; sample inspection complete).

**LOCK L disposition:** 0 BLOCKs — first-pass acceptance-criteria PASS across all four checks; only seam-internal duplicate resolution applied (within authority).

**Notes for drax Phase 2 (consumer-side observations):**

1. **Drax sync requirement:** drax must copy `~/Games/reincarnated-engine/data/kit_space/kits/` → `~/Games/reincarnated-loadout/public/kit-space/kits/` to surface the renames in the loadout web app per dispatch § 5. No API change; new values flow automatically through `useKitSpaceData.ts`.

2. **Name-length variance:** post-rename names range 3-7 words (median ~5); UI layout testing should check rendering of longer names like "Deepcurrent Flowsinger of the Abyssal Fen" (7 words) and "Wrathbound Feral of the Crimson Rampage" (6 words) vs shorter forms like "Driftcaller of the Hollow Sky" (5 words).

3. **Sample-inspection priorities for player-facing diff:** the TOP-1 + TOP-5 transitions above are the strongest before/after comparisons; drax may want to highlight these in the demo1 surface to demonstrate the QDX-7-AMEND-FULL game-quality lift.

**Notes for jack-ryan Gate-2 (specific kits worth sample-inspection):**

1. **`kit_physical_000026` Furyboned Cleaver of the Rawbone Pact** — flagged above as aesthetic-mid-tier. Per dispatch § 8 refutation conditions, this is not template-repeat (each physical kit got unique invented archetype) but is the lowest-aesthetic of the cohort. If jack-ryan judges this as quality-floor breach, gandalf can re-fire this single kit at higher temperature.

2. **Cleaver-word recurrence (3 physical kits):** Wrathborn Cleaver / Bonecleaver / Furyboned Cleaver. Per literal dispatch rules: PASS (cleaver/cleave not in avoid-list). Per substrate observation: the physical pool's 4-entry mechanical-action vocabulary (`pierce`, `slash`, `sever`, `strike` per canonical Q18 lock § 2.8) deliberately excluded the cleave-family at v1.0 lock; LLM gravitated to `cleave/cleaver` as a substitute. This is substrate-honest noise (the LLM found the gap and filled it consistently) but worth surfacing to gandalf for v1.1+ deferral list consideration (`crush/impact/rend` per § 2.8 + potentially `cleave`).

3. **Veil-word recurrence (6 kits):** "Smoldering Veil", "Burning Veil", "Crimson Veil", "Hallowed Veil" (none — that was Tribunal), "Hollow Veil" (none — that was Sky), "Pelagic Veilsinger", "Veilsinger of the Wandering Breath", "Breeveiler", "Wrathborn Cleaver of the Crimson Veil". Pattern: "Veil" is a high-frequency mid-fantasy suffix that the LLM clustered toward across elements. Not a violation (Veil is not in any Q18 pool / not a generic archetype). Acceptable per literal rules but worth jack-ryan aesthetic-judgment review for Q19 (emergent-kit-concept naming consistency) wave parameter-tuning.

4. **"Meridian" anchor preserved well:** 3 kits (shadow_000007, lightning_000006, water_000004 was-Sunken-Meridian-but-resolved) retained the "of the X Meridian" lore-suffix pattern; the dispatch § 3 prompt explicitly endorsed this; the LLM applied it judiciously rather than universally. Indicator of prompt design quality.

5. **kit_wind_000004 + kit_wind_000005 are the pre-existing "Scattered Wind Fighter Bearer" template-collapse cases** — both renamed to wholly distinct "Veilsinger of the Wandering Breath" and "Breeveiler of the Wandering Expanse" respectively, demonstrating that the LLM successfully de-collapsed identical pre-existing names into unique post-rename identities.

6. **Discipline-recognition candidate (surface for jack-ryan):** the 12 first-pass duplicates (mostly physical) suggest a discipline candidate — **within-cohort uniqueness should be a first-class LLM prompt constraint when batch-naming N>10 same-primary kits, not a post-hoc filter.** The current prompt fires per-kit-independently with no awareness of sibling outputs; future batch-rename work might benefit from passing the running list of already-assigned names as part of the user prompt. Not architectural-commitment; flagging for Q19 wave consideration.

---

**Completion record signed:** gandalf (story-and-design steward; subagent role for this rename pass)
**For:** cycle-18 Drax QDX-7-AMEND-FULL Issue 4 — the substrate-honest transition of 37 kit identities from generic-archetype-flattening to invented-unique-archetype form per Matt 2026-06-02 directive + Q18 canonical lock as inverted avoid-list.

