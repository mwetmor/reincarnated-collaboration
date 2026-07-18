# VDM-1 basin-2 mapping WAVE PLAN (steward, gandalf — authored 2026-07-18 while ingest-11 runs)

**Gate:** ALL m-batches fire only after ingest-11 completes + steward-verifies (dossiers must be queryable in corpus.db; errata'd values govern). Batches mirror the crawl batches 1:1 — same kit windows, so each batch's dossier evidence is a single ingested unit.

**Denominator: 76 of 78.** Two kits are SKIPPED this wave, each with an annotation line in its batch summary (not a mapping row):
- **le-bomb-lance-falconer (m04 window)** — full SNF; zero dossier evidence; mapping cites `kit_dossier` fetched language, so there is nothing legal to map from. Re-crawl queue (S4 guide-lag, BACKFILL-2 class).
- **le-harvest-lich (m05 window)** — CHIMERA (kb folk name conflates Harvest Flay Lich + Death Seal Lich; all families UNSUPPORTED). Cannot grade fidelity against a build that does not exist as recorded. Split/re-anchor decision rides the review book; mapping deferred to post-split.

## Waves (steward audit capacity: recount every return — fire in 3 waves)

| Wave | Batches | Kits |
|---|---|---|
| W1 | m01 + m02 + m03 | gd 1–36 (all-GD; §A law exercised) |
| W2 | m04 + m05 | gd 37–41 + le 42–48 (seam) · le 49–60 |
| W3 | m06 + m07 | le 61–72 · le 73–78 |

**W3 rosters (extracted from batch-verify.jsonl at W2 fire; no SKIPs — 12+6=18):**
- **m06:** le-reaper-form-lich · le-ring-of-shields · le-runic-invocation · le-shadow-bladedancer · le-shield-bash-le · le-shield-throw-time-rot-vk · le-shift-bladedancer · le-skeleton-necro · le-smite-paladin · le-soul-feast · le-squirrel-bm · le-storm-totem-shaman
- **m07:** le-swarmblade-druid · le-tempest-strike · le-umbral-blades · le-warpath-vk · le-werebear-druid · le-wraithlord-necro

## Per-batch hot facts (paste into spawning prompts at fire time)

**m01 (b01 window, gd 1–12):** berserker dossier is THIN by design (FoA unshipped ×6 abstains — map what exists, note the gap; BACKFILL-2 pending) · blade-trap = negative ATTESTED + era restamped `base-2016;aom-2017` ("later reworked" is annotation, never mapping grounds) · belgothian + cadence = §A replacer/WPS row — cadence's Nth-swing detonation FILES an accrual to the two-tier-accumulator family (no numbers; strengthens the fired WATCH-ITEM) · blight-fiend pet-death-payload = pet GAP + own docket-candidate if shape recurs · aar/callidors era-restamped (verify_ledger governs).

**m02 (b02 window, gd 13–24):** eor-warlord = §A devotion-rider row (Maul proc NAME ≠ payload) · fire-strike = replacer + explosive-line WPS; economy CORRECTED to Energy (erratum — do not echo "mana") · pet-conjurer = pet-core → GAPPED/MAPPED_DOCKET candidate per R-M7 player-test; pet-stat lane ≠ player-stat lane · forcewave/mortar/panettis era-restamped; panettis mechanics CORRECTED (tri-elemental, shock-downstream).

**m03 (b03 window, gd 25–36):** retaliation-warlord = §A retaliation-substrate row — loop-verb IS stand-and-return → likely GAPPED ⟺ MAPPED_DOCKET (R-M7 strictly; do NOT stretch aura-pulse tokens) · skeleton-ritualist pet-core + reserve-maintenance note · stun-jacks = name-collision law poster child (map ONLY fetched behavior; negative is UNATTESTED — annotation, not mapping input) · stormbox identity is WATCH-annotated (map the attested mechanics; folk-name weakness is not a mapping concern) · righteous-fervor = replacer verbatim row · reap-spirit negative ATTESTED.

**m04 (b04 window, gd 37–41 + le 42–48; SKIP bomb-lance):** trozan + word-of-pain = §A devotion-rider (word-of-pain elem_raw=fire is ERRATUM — fetched shows chaos/lightning/pierce variants; map from dossier language) · wendigo-totem = GD placed-emitter — §B totem lane is LE-attested SHAPE precedent; GD's own fetched "Dark One's Gift 4-totem" language carries; count → placed-proxy-count accrual · vitality-conjurer era-restamped base-2016 · chthonic-fissure elements CORRECTED fire+necrotic (void was probe artifact) · erasing-strike Void Well = Mana (no spirit/focus) · detonating-arrow identity-WATCH (map Blast-Rain-proc loop as attested).

**m05 (b05 window, le 49–60; SKIP harvest-lich):** low-life-ward = §B ward-from-missing-health row — item-defined archetype; map WITH-items form as core; inversion economy → docket-candidate (consolidates basin-1 overheal-above-cap); R-M7 player-test decides APPROX vs GAPPED honestly · lightning-blast = Reowyn ward-burst rider (§B) · fire-aura-spellblade core CORRECTED: aura is passive-emergent, NOT Flame Ward (Flame Ward = defensive cooldown) · ghostflame geometry: fetched "channeled jet"/"hellish torrent" → cone-projection reading (geo erratum pending) · manifest-armor resource CORRECTED Mana ("Forge Stacks" = probe fabrication) · healing-hands era restamped (+1.0-launch); Rahyeh's Chariot role-conversion = fidelity_notes, not core geometry · hammer-throw "Sigils→Symbols" rename = era-scoped name note.

**m06 (b06 window, le 61–72):** shift-bladedancer = §B traversal-as-proc-hub (traversal token stays; procs are riders; never promote payloads into traversal geometry) · soul-feast = §B single-button carrier + automated riders (one-button ≠ one-mechanic; negative UNATTESTED) · squirrel-bm = §B companions GAP + count-conversion accrual to placed-proxy-count · storm-totem = §B totem lane + Rage-in-form law (map IN-FORM economy; Stormcarved proc-cast = trigger rider) · skeleton-necro pet-core → R-M7 · runic-invocation class CORRECTED (Mage mastery) + Reowyn ward-burst · smite eras post-ruling (1.2-woven is honest-U — lastepochtools inadmissible) · ring-of-shields = support-skill kit, backfilled eras · shield-bash negative UNATTESTED.

**m07 (b07 window, le 73–78):** swarmblade + werebear = §B Rage-replaces-Mana-in-form LAW (map in-form economy as kit economy; swap = fidelity_notes) · tempest-strike class CORRECTED (drop Acolyte) + negative is ERA-SCOPED (annotation, not mapping input) · umbral-blades "void blade" alias = probe artifact (fetched: physical/cold) · warpath = channel + mana-per-tick drain (verbatim-confirmed) · wraithlord = pet-core (Wraithlord's Harbour ITEM enables; "Wraithlord" as discrete skill is ambiguous — map the attested summon-harvest loop) → R-M7.

## Standing counts at fire time (steward-owned; mappers file WITHOUT numbers)
Families: out-and-return · placed-proxy-count (+2 at m03 audit: army-count, recast-count) · two-tier-accumulator (WATCH-ITEM FIRED at 2; cadence would be #3) · stat-as-damage-substrate cluster (4 mechanisms incl. GD retaliation — m03 filed the anticipated own-row docket).

## Post-W1 audit rulings (PASTE into W2/W3 spawning prompts)
- **Gapped-pet geometry convention (m03-audit ruling, REFINED at m02 audit — two-lane, binding):** placement-ATTESTED summons ("at target positions") → `totem` PLACEMENT projection; follow/companion summons with NO placement language → null geometry is honest. Mirrors §B totem-vs-companion at the geometry layer. Either way the autonomy gap lives in grade + deviation_notes + docket per R-M7. Applies to m05 skeleton-necro/wraithlord-adjacent, m06 squirrel-bm/skeleton-necro/storm-totem, m07 wraithlord.
- **Two §A rows ADDED at m02 audit (binding):** GD Internal Trauma → `bleed` (phys-DoT lineage) · GD fumble/attack-miss curses → `blind` (register widened to accuracy-tax) with the sentence-adjacency micro-ruling for skill-level emission. GD confusion/electrocute/frostburn = NO-HOME withholds (review-book list).
- **Verify-anchor admissibility (m01-audit adjudication, in template §0.2):** `verify_ledger.anchor_quote` = LEGAL attestation grounds (fetched-class); `claim_text` = INADMISSIBLE (kb-class). ⚠ STORE-NOT-STYLE: probe prose reads like guide verbatim — admissibility is the STORE, never the styling (m01 bwc leak, struck + re-grounded at audit).
- **Empty-projection convention (m01-audit ruling):** all-family-abstain kits map as the honest empty shell (skills=[], doors=[] LEGAL, motion UNMAPPABLE) + GAPPED/DOCKET; never invent from folk-name. (W2 note: bomb-lance is SKIPPED outright — annotation line, not an empty-shell row; harvest-lich likewise chimera-deferred.)

**W1 CLOSED (m01 `2c816f89`+audit · m02 `792f15f9`+`3266ccb0` · m03 `351d5a70`+`b51bef9c`): 36/36 GD kits · post-audit 8E/20C/2A/6G · 30 MAPPED / 6 DOCKET · 1 leak struck+re-grounded · 1 steward addition · 1 regrade.**

## Post-W2 audit rulings (PASTE into W3 spawning prompts)
- **ANCHOR-SPLICE leak sub-class (m04 audit — LEAK #2 of the run):** a legal store fragment + a memory continuation presented as ONE verbatim quote (the spliced phrase exists in NO store). Distinct from m01 bwc (real line, wrong store). **Audit + authoring instruction: every quoted attestation must be CONTIGUOUS in its store — never assemble a quote from fragments.**
- **Damage-type-over-time RULING (m04 audit, binding):** "X damage over time" attests delivery TIMING, never a status (§0.1 unchanged — burn still needs NAMED ignite/burn). LE mechanically distinguishes skill-native DoT from ailment DoT; emitting burn would MISDESCRIBE a native-DoT skill as an ailment-stacker. The DoT payload is CARRIED by element + delivery_notes — so a correct withhold does NOT understate the mapping and does NOT drive APPROX by itself (ghostflame regraded CLOSE; chthonic-fissure withhold upheld).
- **`_cascade` pin discipline (3 misuses corrected across W2):** `GEOMETRY_PROPAGATION_cascade` = on-KILL propagation ONLY; on-hit scaling = `_overkill`; trigger-driven/unclear → BASE `GEOMETRY_PROPAGATION` (R-M1). Orbit/walking-damage-field loops → `PERSISTENCE_ENGINE_uptime` (RF-class exemplar; hammer-throw corrected TO this).
- **Variant-scoped attributes never ride the core row (§7.2):** a listed variant's element/ailment (Bleed-Hammerdin bleed; Freezing-Aura freeze+cold) stays OFF the core mapping; variant identity may still inform the T4 hint (fire-aura kept ELEMENT_CONVERSION_MONO).
- **Accrual filing-vehicle (2 misses):** family accruals FILE in `mint-candidates-batch-NN.jsonl` with `mint_class: "accrual: <family>"` (m02 exemplar) — fidelity_notes-only is a filing miss.
- **No-home list grows:** + LE Frostbite (cold-DoT, m05 frost-claw) → joins GD confusion/electrocute/frostburn (review-book).
- **THE PHYSICAL RULE reminder (m05 miss):** physical is NEVER an element token — element_primary/secondary null is the honest physical carrier.

**W2 CLOSED (m04 `f5105287`+`975156dc` · m05 `b53d1b2d`+`c13f2e6a`): 22/22 kits (2 SKIPs annotated: bomb-lance, harvest-lich) · post-audit 1E/18C/1A/2G · 20 MAPPED / 2 DOCKET · 1 anchor-splice leak struck · 9 steward corrections · 1 regrade (ghostflame→CLOSE) · dockets +2 (ward-inversion consolidation w/ 2 in-batch evidence kits; gear-stat-as-minion-scaling) · placed-proxy-count accruals recorded steward-side (Dark One's 4-totem = ONE mechanism/TWO kits · explosive-trap carpet · bladestorm triple).**
- **§2 RR-branch reminder:** curse:sap vs sunder picks need an application-shape anchor word in fetched text (aura/presence/entity-anchor → curse:sap; hit-proc window → sunder); shape-silent = WITHHOLD (m03 exercised 5×, consistent).

**Lifecycle:** steward instantiates spawning prompts from the TEMPLATE + this plan at each wave fire; audits every return (D-2c recount); §A/§B extend at audits if NEW mechanisms attest.

## INGEST-12 SPEC (pre-staged at W2 close; FIRES only after W3 audits close — post-audit file truth is the ingest source)

Commission elrond (single-writer). Three payloads, one ingest:

1. **kit_mapping ingestion — 76 rows** from `stage2/basin2/mapping-batch-01..07.jsonl` (post-audit versions; steward-corrected in-place, audit stamps inline). Exact-count contract: **76** (36 W1 + 22 W2 + 18 W3; SKIPs bomb-lance/harvest-lich are annotation lines in summaries, NOT rows — do not expect 78). Terminal states MAPPED/MAPPED_DOCKET only; grades EXACT/CLOSE/APPROX/GAPPED. W1 8E/20C/2A/6G · W2 1E/18C/1A/2G · W3 at audit close.
2. **b05 author-credit backfill — 10 rows** from `stage1/basin2/batch-05-dossier-authorcredit-backfill.jsonl` (legolas `6c14ed8f`, steward-recounted clean). ⚠ Zaodon caveat rides as annotation: QUESTION-thread OP, NOT build author (conf 0.75, disclosed in-row) — review-book author-lineage must not count it as authored-guide credit; Aayron IS genuine (1.0-era build-guide OP).
3. **canon_engine_key WRONG-RESOURCE third-store sweep — 16 gd rows** (extends ERRATA-38; authorized at ingest-11 steward verification — Ruling 1).
4. **Annotation-precision erratum (LOW) — le-umbral-blades mech_note:** current ALIAS-ARTIFACT annotation claims "fetched text attests… physical/cold" but is CIRCULAR to probe-class ("probe element already reads 'Physical / Cold'"); store-grep at m07 audit confirms zero cold tokens in kit_dossier/verify_ledger. Reword to "probe element reads Physical/Cold; fetched text is element-silent." (m07 audit finding; mapping already ships null/null correctly.)

**NOT ingested:** mint-candidates / docket-candidates side-files (file-based → THE REVIEW BOOK consolidation) · batch summaries (git artifacts).

**Disciplines:** clean-backup before write + md5 chain (MIGRATION §Execution-integrity — the ingest-11 dry-run-wrote-live-db lesson is banked; no dry-run harness against the live path) · exact-count contract per payload · errata ledger entries for payload 3 · steward D-2c verification battery on return (readonly-SQL recount: kit_mapping row count + grade/terminal histograms vs post-audit file truth + spot-join 5 kits + backfill rows present + 16 sweep rows changed). Basin-2 checkpoint row appends to the run-state ledger after verification.
