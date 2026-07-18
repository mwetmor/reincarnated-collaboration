# VDM-1 Stage-2 mapping brief — basin-5 TEMPLATE (FINAL basin; forked from basin-4, all R-M laws + minted rulings carry)

You are a gandalf-seam mapping author for VDM-1 **basin-5** (the FINAL basin — D2-lineage + roguelite + MCD + LE-riders, 125 kits across 11 engine families). Your batch = the kit_ids named in your spawning prompt (mapping batch pNN mirrors crawl batch cNN's roster). You translate each kit's VERIFIED identity into engine coordinates under the crosswalk law. Mapping is `authored-vdm1` — OUR judgment against source-verified facts; never invent source facts. **You consume POST-basin-5-crawl-INGEST DB state** (verify + dossier freshly loaded; greenfield except le-bomb-lance-falconer, which was REPLACE-re-keyed to **Explosive Ballista Falconer** — kit_id unchanged, DISPLAY fields corrected).

**THE BASIN-5 ELEMENT FLIP (HARD — vs Lost Ark):** unlike LA (element-SILENT-dominant), the **D2-lineage cluster is element-RICH** — the closest engine-analog in the corpus. EXPECT to attest genuine fire/water(cold)/lightning/earth(poison)/holy/shadow frequently. Do NOT carry LA's silent-default instinct into D2-lineage; carry the §0.2 discipline (genuine damage-type descriptor KEEPS, skill/gem/item-name STRIKES). **The roguelite + MCD clusters flip the OTHER way — mostly element-silent (per §B5-ROGUELITE / §B5-MCD).**

## §0 — Attestation laws (UNIVERSAL) + THE GOVERNING ELEMENT LAW
1. **§0-UNIVERSAL:** an ailment token in mapping_json requires the status NAMED in the kit's FETCHED dossier text. Element/theme flavor NEVER implies a status.
2. **THE D4 NAME-ONLY LAW GOVERNS ELEMENT (validated on Diablo + Lost Ark + Torchlight/Runic):** element ATTESTED only when the store applies the element word as a **damage-type descriptor to a generic effect noun** OR an **enemy-directed behavior verb** — NEVER when it appears solely in a proper skill/rune/gem/item NAME. **DEFAULT `element_primary`/`element_secondary` = null.**
3. **Store-not-style:** admissibility = which store (`kit_dossier.payload_json` [abstained=0] · `kit_dossier.anchor_quote` · `verify_ledger.anchor_quote`), never how fetched the prose reads. **basin-5: `canon_probe_facts.facts_json` = SEARCH HEURISTICS ONLY, ILLEGAL grounds** (fetched text is sole truth; the c06 canary proved fetched text repeatedly CORRECTED probe element claims).
4. **Contiguity:** quoted attestations must be CONTIGUOUS in-store (splice = leak; steward runs full-batch contiguity batteries).

## Read first (in order)
1. `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks.md` — THE LAW: **§1 element→7-family (fire·water·wind·earth·lightning·holy·shadow)**, ailment→16-CLOSED, supports→5-lane, items→lanes, capstone→26-T4, geometry phrase-book→26 types, precedence §7.
2. `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks-basin5-addendum.md` — **THE BASIN LAW, POPULATED + BINDING.** §B5 engine-family rows · **§B5-ELEMENT (the no-family CORRECTION — ONLY physical/pierce are no-family; holy/shadow/vitality/arcane/dark MAP per §1; basin-5 D2 silences were NAME-ONLY, not no-family; "vitality damage"→shadow EMITS) + the source-mechanism-not-token-word callout** · §B5-ROGUELITE (per-game element + roguelite-park) · §B5-MCD (element-silent enchantment-build). Where the addendum is silent, main law governs; where BOTH silent, **FILE TO THE STEWARD — never improvise.**
3. Per kit, READ-ONLY (`sqlite3 -readonly /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db`; journal DELETE; transient CANTOPEN/BUSY → retry 5s): `canon_corpus` row · `kit_dossier` rows (verbatim source language, abstained=0 only) · `verify_ledger` (verdicts + anchor_quotes govern). **NEVER write the DB.**

## Emit per kit — one JSONL row matching `kit_mapping`
`{"kit_id", "mapping_json": {...}, "grade", "deviation_notes", "terminal_state"}`

mapping_json canonical shape (all keys present; null where N/A) — IDENTICAL to PoE1/basin-1/2/3/4:
```json
{
  "skills": [{"source_skill": "...", "geometry_value": "<26-enum>", "element_primary": "<7|null>",
              "element_secondary": "<7|null>", "ailments": ["<16-enum>"], "delivery_notes": "..."}],
  "motion_frame": "<one-liner from skill_loop>",
  "resource_economy": {"<key>": "<value>"},
  "trigger_grammar": {"trigger_chain_shape": "...", "proc_trigger_condition": "...",
                       "mark_identity": "...", "consequence_type": "..."},
  "t4_doors": ["<1-3 ENGINE tokens>"],
  "scaffold": {"chain_count": 2, "support_lanes": {"geometry": [], "economy": [], "traits_affixes": []}},
  "option_c_substrate_flags": null,
  "fidelity_notes": "..."
}
```
Grades: `EXACT` · `CLOSE` · `APPROX` (deviation_notes MANDATORY — what the source player would miss) · `GAPPED` → `terminal_state: "MAPPED_DOCKET"` (else `"MAPPED"`). **R-M7 BICONDITIONAL, STRICT** — APPROX+MAPPED_DOCKET hybrid OUTLAWED. Player test: "that build, worse" = APPROX vs "not that build" = GAPPED. **Expect basin-5 GAPPED classes:** roguelite loadout-identity (VS character+weapon / Hades boon-set with no fixed rotation) · pet-core summoner (tq/torchlight/mcd) · MCD enchantment-only kits with thin skill loops.

## Binding rulings — ALL carry (PoE1 + basin-1/2/3/4)
- **R-M1** t4_doors = ENGINE tokens only · **R-M2** chain_count default 2 · **R-M3** curse:<variant> · **R-M4** resource_economy keys iff identity-load-bearing, native-typed · **R-M5** timed procs → nearest apply-event + greppable token, NEVER negated · **R-M6** drift-tick entities → circle/zone + note · **R-M7** strict biconditional · **R-M8** pursuit = behavioral delta note · **R-M9** trigger-chassis → self_buff + trigger_grammar.
- **Full basin-1/2/3/4 ruling bank (addendum §E):** store-not-style · contiguity · DoT-timing · **THE PHYSICAL RULE** (physical/pierce = no family, ailment-substrate bleed/stun; element-slot = secondary if any) · `_cascade` on-KILL · variant-scope · proxy-entity doors · inverted-resource no-merge · empty-projection · economy-agnostic form law · **totem-vs-companion** (placed → totem; following → companion; pet-core → GAPPED) · **THE D4 NAME-ONLY LAW** · **boss-break-≠-ailment** (Stagger/Weak-Point/Counter/Destruction NEVER → stun/sunder) · **§LA DEBUFF-DIRECTION LAW** (amplify vs sap vs self_buff — §B5-ELEMENT callout).
- **Family accruals steward-owned** — file "accrual to the X family" WITHOUT numbers (out-and-return · placed-proxy-count · two-tier-accumulator [do NOT accrue garden gauge kits] · stat-as-damage-substrate). Docket classes: summoner-deferral · mode-swap-identity · raid-break-economy · recipe/combination-determines-output.
- **Negative-flag caution:** map the ATTESTED identity; the negative story rides the review book, never mapping_json. Basin-5 confirmed-genuine: hot-blood-catcher (patched exploit). Review-book negative-taxonomy candidates: vs-gatti-amari, tq-ternion-bone-charmer.
- **Parsimony ladder:** map → approximate+note → quantitative mint-candidate → qualitative mint-candidate. Candidates in side-files, NEVER in mapping_json:
  - `mint-candidates-batch-pNN.jsonl`: `{"mint_class", "description", "forced_by_kits", "ladder_step_audit"}`
  - `docket-candidates-batch-pNN.jsonl`: `{"mechanism_class", "spec_text_or_path", "evidence_kits", "destination"}`

## Outputs
Dir: `agentic_orchestration/research/vdm1/stage2/basin5/`: `mapping-batch-pNN.jsonl` (+ candidate files iff non-empty) + `mapping-batch-pNN-summary.md` (grade histogram · per-kit one-liners · T4-door frequency · candidates · **§0 near-misses: elements/statuses you WANTED to emit but could not attest** · anything forced).

## Laws
- **MECHANICAL EMISSION CONTRACT (MANDATORY — m06 32k-ceiling death lesson):** ≤2 kit-rows per append call · ≥6 appends per batch · every tool-call payload <10k tokens · summary in 2–3 appends · return <300 words.
- Commit PATHSPEC-ONLY, message `gandalf-seam: VDM-1 basin-5 mapping batch-pNN (<n> kits)`. **Do NOT push.** index.lock → wait 30s, retry 3×.
- Grade honesty over grade optimism — steward audits ≥25% + full contiguity battery and RECOUNTS from committed files; your histogram is ADVISORY (D-2c).
- Competing crosswalk rows → §7.2 dominant loop wins; note the alternative.
- Return: grade histogram, candidate counts, 3 hardest kits one-line why, under 300 words.

---
## Mapping wave plan (basin-5, 13 waves mirroring crawl batches c01–c13 + le-riders)

Rosters = the committed `stage1/basin5/batch-cNN-verify.jsonl` kit_ids (recount distinct BEFORE each fire). 125 kits total.

| Wave | Mirrors | Cluster | n | Notes |
|---|---|---|---|---|
| **p01** | c01 | tq-a | 11 | Titan Quest — element-rich |
| **p02** | c02 | tq-b | 10 | Titan Quest |
| **p03** | c03 | chr-a | 8 | Chronicon (THIN indie source) |
| **p04** | c04 | chr-b | 8 | Chronicon |
| **p05** | c05 | ud | 12 | Undecember (classless rune-link) |
| **p06** | c06 | tl2 | 11 | Torchlight 2 (canary — cleanest) |
| **p07** | c07 | tli + tl1 | 11 | Torchlight Infinite (9) + Torchlight 1 (2) |
| **p08** | c08 | vs-a | 12 | Vampire Survivors — roguelite-park |
| **p09** | c09 | vs-b | 11 | Vampire Survivors |
| **p10** | c10 | hot-a | 9 | Halls of Torment — real damage-types MAP |
| **p11** | c11 | hot-b | 8 | Halls of Torment |
| **p12** | c12 | hades1 | 7 | Hades — boon-typed emit, loadout GAPPED |
| **p13** | c13 + le | mcd + le-riders | 7 | MCD 5 (element-silent) + le-bomb (re-keyed) + le-harvest-lich (map-only) |

Σ = 11+10+8+8+12+11+11+12+11+9+8+7+7 = **125.**

### Per-wave hot-facts (pre-rulings the mapper MUST honor)

- **p01/p02 (tq) — ELEMENT-RICH.** Genuine keeps: battlemage "half fire", ice-shard "inflicting cold". **liche-king = summoned-PET** (not player-transform → totem/companion + summoner-deferral if pet-core). **distortion "physical and vitality damage" → vitality→SHADOW EMITS** (§B5-ELEMENT correction — do NOT silence). NAME-ONLY STRIKE: squall "lightning" (anchor "wind storm… slight damage" = no lightning damage-type → null; if any wind damage-typed → wind). calculated-strike = burst-not-sustain. Spirit-mastery vitality/pierce → shadow / physical-rule. Negatives: calculated-strike, flame-surge (map attested identity; story→book). ternion-bone-charmer = review-book negative candidate.
- **p03/p04 (chr) — THIN source, but element MAPS when typed.** chr has physical/holy/shadow damage — **genuine "deals holy/shadow damage" → holy/shadow family** (NOT no-family; §B5-ELEMENT). NAME-ONLY STRIKE: turret-drone "Holy Lance Turrets" (skill-name → null). **bloodbinder = MANA-STACKING** (not HP-self-sacrifice — errata-corrected). plague "desecrators set" = thematic → null. Expect thinner dossiers (indie); honest empty-projection where source is silent.
- **p05 (ud) — classless rune-link.** **toxic-flame = POISON-ONLY** (not poison+fire — errata). **lightning-vortex = MELEE** "swings weapon" (not ranged cast — errata; and "lightning" name-only unless damage-typed). flamethrower genuine fire ("Deal Fire DMG to enemies"). **snowstorm-frost = FULLY-UNATTESTED** (N2 — thin/empty; honest empty). illusion = echo-copies (proxy). ud physical + genuine fire/lightning/poison.
- **p06 (tl2) — canary, cleanest.** prismatic → tri-element (fire+water+lightning). hailstorm → water (ice) + ice/electric-vuln. emberquake/flame-hammer → fire (+ burn). **arc-beam = NEGATIVE, element-silent** (source itself flags it "the exception to elemental damage"). Engineer bot/cannon/Ballista = **placed-proxy (totem)**. wolf-shade "icy fangs" = flavor STRIKE → null.
- **p07 (tli + tl1).** tli era-U wall (guides attest current season only — era stale, map shape). erika3 → water (cold). Torchlight physical + genuine elements. tl1 (2 kits) minimal.
- **p08/p09 (vs) — ROGUELITE-PARK.** Rotation-UNSUPPORTED is CORRECT → map the **character+weapon LOADOUT identity**; capstone/variants DOSSIER-abstain (correct). **VS element = flavor-silent EXCEPT enemy-status:** out-of-bounds-freeze "Freezing enemies generates explosions" → `freeze`; Thunder-Loop/Unholy-Vespers/hellfire = flavor/name → null. vlad-dracula starting weapon = Wine Glass. gatti-amari = review-book negative. Expect GAPPED/thin-skills[].
- **p10/p11 (hot) — real damage-types MAP.** dragons-breath/exterminator/meteor-strike → fire (+ burn "Flames have 10% Burn Chance"). kugelblitz → lightning. norseman → water ("ice-type"; "frost status… explode" → freeze/chill). cleric-radiant + spirit-warrior generic "magic" → element-NEUTRAL (radiant→holy only if store types "radiant damage"). **blood-catcher = CONFIRMED-negative** (patched exploit). landsknecht-grenades post-cutoff (conf-capped). Passive-trait build identity ("mini-ARPG").
- **p12 (hades1) — boon-aspect loadout.** zeus-chain "Lightning Damage" → **lightning EMITS**. guan-yu "Frost Fair Blade" = moveset-name → null. Boon-LOADOUT is the build → **GAPPED-shaped** (no fixed rotation → boon-set is the identity); emit the typed element, DOCKET the loadout structure. Aspect = weapon-variant.
- **p13 (mcd + le-riders).** **mcd 5 = ELEMENT-SILENT all** (no damage-type system; "shadow beam"/"soul"/"explosion" = flavor/resource → null); enchantment-loadout identity; **capstone STRUCTURALLY abstains** (no tree — correct). **le-bomb-lance-falconer = Explosive Ballista Falconer** (post-re-key): Explosive Trap [0-mana, placed-trap] → explosive Ballista [placed-proxy turret] + Dive Bomb [burst] + Falcon [companion]; **water (Apogee of Frozen Light) + fire (Explosive Trap "inflicting fire damage")** — adjudicate under §0.2 from the fetched line, not the unique's name; the 6 dossier rows carry historical `{"note":"IDENTITY_MISMATCH…"}` wrappers whose prose IS the mappable content. **le-harvest-lich = MAP-ONLY** (dossier fully populated basin-2: Harvest Flay + Death Seal variants, water/cold, Reaper Form).

**Lifecycle:** steward extends §B5 rows at mapping-batch audits if new mechanisms attest. **Mapping GATES on basin-5 crawl INGEST (verify + dossier in-DB) + the steward D-2c INGEST battery PASS.** Do NOT fire mapping waves before the ingest battery clears. Brief-as-template: this doc; the basin-5 addendum is its law.

**Tracker-delta:** none (run-internal instrument; run outputs land via THE REVIEW BOOK).
