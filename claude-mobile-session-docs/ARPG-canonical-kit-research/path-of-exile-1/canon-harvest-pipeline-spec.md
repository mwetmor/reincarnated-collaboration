# Canon-Harvest Pipeline — SPEC (build-level genre canon → the lattice)

**STATUS:** MATT-FACING · executable by the mobile track (Claude) or the Mac team.
**Job:** Stage 1 of `substrate-coordinates.md` §7 — "canon-kit → coordinate table" — at its true grain: the **build**, not the class. Feeds: the roster (duplicate/variant/new-cell verdicts), the §3 alarm registers (gap records), and **retrodiction dataset v1** (the FUN instrument's validation data, with negatives).
**TRIPLE LAW integration:** harvest records project onto the LATTICE using its locked vocabularies; unprojectable mechanics fire the Codex/Projection alarms; nothing here reopens closed placement rulings.

---

## §1 — The identity rule
A canon build = a **community-named mechanical loop** (Hammerdin, Meteorb, CoC Discharge) — never a class, never an item list. Naming is the canonicity filter: the community only names what recurs.
- **Key:** `{game}-{folk_name}` · **Lineage:** cross-era links (`coc-discharge` = one lineage, N era-records).
- Variants fold into one record with variant notes UNLESS the mechanical loop differs at lattice grain (Lightning-Sentry vs Death-Sentry Trapsin = one record; Summonmancer vs Bonemancer = two).

## §2 — Game tiers (Matt ruling encoded; amendable)
- **Tier 1:** D2/D2R(+RotW), D3, D4, PoE1, PoE2, Last Epoch, Grim Dawn.
- **Tier 2:** Titan Quest, Torchlight 1/2/Infinite, V Rising?, Chronicon, Hades (adjacent — commitment/boon evidence only).
- **Scope question (Matt):** mods — Median XL, Project Diablo 2, Path of Diablo — rich novel-mechanics mines, murkier canonicity. Recommend: harvest LAST, flagged `mod:true`, excluded from retrodiction v1.

## §3 — The five stages (contracts)
1. **CENSUS** — enumerate names per game from pre-aggregated sources (tier lists, compendium threads, poe.ninja archetypes, "best builds of all time" retrospectives, era tier lists via Wayback). Output: `census.jsonl` (name, class, era hints, source URLs). Completeness bar: two independent sources per name OR planner-data presence.
2. **DOSSIER** — per build, 3–5 best sources → 2–4 sentence mechanical summary + core skills + defining items, in ORIGINAL prose (facts, not guide text; URLs + ≤15-word quotes only).
3. **PROJECTION** — constrained extraction against the LATTICE's locked vocabularies. **THE ABSTAIN LAW: abstain-not-guess.** Per-axis `{v, c}` (value, confidence 0–1); where the harvester cannot see the canonical enum (or the source can't support a bin), emit the value in SOURCE vocabulary + `abstain:true`. Reconciliation maps source-vocab → canon enums; unmappable = gap record.
4. **RECONCILIATION** — dedupe (embedding + judge), lineage assembly, roster verdict per record: `duplicate-of:K#` · `variant-of:K#` · `new-cell-candidate` · `bench-evidence:B#`. Gap records route to `projection-atlas.md` §3.
5. **AUDIT** — ≥10% human/judge sample per game; inter-rater on the projection axes; this dataset gates the FUN instrument, so label quality is a certification surface, not paperwork.

## §4 — Source rankings (planner-code sources OUTRANK prose, always)
| Game | Rank-1 (mechanical truth) | Rank-2 (canonicity/usage) | Rank-3 (prose/era) |
|---|---|---|---|
| PoE1 | Path of Building codes | **poe.ninja league snapshots (~2017→)** — usage = canonicity telemetry | forum build index, r/pathofexile, era guides |
| PoE2 | PoB2/planners | poe.ninja PoE2 | reddit/guides |
| D2/D2R | (no planner era) | maxroll d2 tierlists · icy-veins PvM rankings · diablo-wiki named tiers | Amazon Basin wiki, Arreat Summit archive, r/diablo2, 1.09/1.10 era lists via Wayback |
| D3 | — | maxroll/icy-veins set-archetype tiers | era snapshots per set-meta patch |
| D4 | Maxroll planner links | maxroll/icy-veins/mobalytics tiers | season retrospectives |
| LE | lastepochtools planners | LE tier lists, forum compendia | reddit |
| GD | **Grimtools links** | community build compendium threads (forum-maintained) | reddit/forum |
**Era stratification rider:** every record carries `eras[]` (patch bands). Wayback snapshots for era-authentic tier lists — what the era believed, not what 2026 remembers. **Negative-canon rider:** harvest tier-list bottoms, never-picked skills, buffed-because-unused patch notes in the same pass → `negative:true` records (the contrastive population KPI validation requires).

## §5 — Record schema (JSONL, one build per line)
```json
{"id":"d2-hammerdin","game":"d2","folk_name":"Hammerdin","class":"Paladin",
 "aliases":[],"eras":["lod-1.10+","d2r-2.x","rotw-s13+"],"lineage":"d2/hammerdin",
 "canon_tier":"deep|moderate|shallow|negative",
 "canonicity":{"longevity":"1.10→2026","fame":"very-high","evidence":["mx","iv","dw"]},
 "mech_summary":"…","core_skills":[],"key_items":[],
 "proj":{"attr":{"v":"WIS","c":0.8},"range":{"v":"mid","c":0.7},
   "tempo":{"v":"high","c":0.8},"amp":{"v":"flat","c":0.7},
   "proxy":{"v":"solo","c":0.9},"commit":{"v":"instant","c":0.8},
   "geo":{"v":"multi-spawn","c":0.6},"ctrl":{"v":"damage-pure","c":0.8},
   "def":{"v":"mitigator","c":0.7},
   "econ":{"v":"mana-sustain","c":0.5,"abstain":true,"note":"canonical 7-bin enum not visible to harvester"},
   "mob":{"v":"teleport-high","c":0.5,"abstain":true},
   "elem_p":{"v":"magic","c":0.9,"src_vocab":"d2","abstain_map":true},
   "elem_s":{"v":null},"hyb":{"structures":[],"rate":null}},
 "gap_refs":["GAP-D2-01"],"prov":["mx","iv","dw"],"negative":false}
```
Provenance keys resolve in the per-game report's legend. Confidence semantics: c≥0.8 sourced-solid · 0.5–0.7 informed projection · <0.5 or `abstain` = reconciliation work item.

## §6 — Gap-record protocol (the pipeline's most important output)
Stage 3 **fails loudly**: any build that can't take a full address emits
`{gap_id, build_id, missing:"axis|enum|surface", evidence:"≤15w quote + URL", candidate_class:"BC-SAMPLED|BC-MEASURED|IDENTITY|WITHIN-CELL|CONSTRAINT|CODEX-SURFACE"}` → `projection-atlas.md` §3 registers.
**Pre-registered predictions (confirmatory instrument):** movement-verb builds → B5/B6/F4 · trigger/CoC loops → hook layer (ladder #2) · aura/reservation economies → Axis-5 reserved bins · wall builds → B4 · **form-shift builds (werewolf/shapeshift) → likely GENUINE novelty (kit-within-kit state)** · **damage-conversion chains (PoE phys→element) → Codex surface or mask**. Each firing validates the instrument; each surprise is Stage-N evidence.

## §7 — Canonicity scoring
`canon_tier` from: usage share where telemetry exists (poe.ninja) · guide/tier fame · **longevity across patches (strongest)** · community naming persistence. Deep = survived nerfs/eras; shallow = one-league wonder (recorded, down-weighted); negative = documented-bad (tier bottoms, buffed-because-dead).

## §8 — Sequencing, ops, publication
- **Order:** D2 (calibration corpus — smallest, consolidated, stress-tests schema) → PoE1 (biggest payoff, best data) → D3 → D4 → LE → GD → PoE2 → Tier-2 → mods-if-ruled.
- **Ops:** API-first (poe.ninja has one) · rate-limit courtesy · Reddit via API terms · no player PII (archetype aggregates only) · Wayback for era snapshots.
- **Publication policy (inherits §10):** the census is devlog gold; the projected coordinates are basis vectors — basement. Negative canon publishable as genre history; gap register internal.
- **Deliverables:** `census.jsonl` per game · dossier corpus · **canon-kit → coordinate table** (§7 step-1 deliverable, build grain) · gap register feed · **retrodiction dataset v1 (with negatives, era-stratified, provenance-attached).**

---

# AMENDMENT v1.1 — post-D2-calibration (2026-07-11)

## A1 — Schema additions (D2 lessons formalized)
- **`context` field:** `"pve"` (default, omitted) | `"pvp"` | `"party"` — D2's Ghost/BvC/Charger and PoE's aurabot demand it; retrodiction v1 filters to pve+both.
- **`flags` field (optional):** `["degenerate-famous"]` for community-celebrated exploit builds (Wormblaster, Ward Loop) — blacklist-seed evidence, kept out of positive retrodiction.
- **Source-truth-over-conformance rule:** records capture what the SOURCE game does even where it violates RDR design law (Avenger tri-element vs the one-secondary cap). Harvest records truth; reconciliation adjudicates. `elem_s` may carry compound strings descriptively + gap_ref.
- **Derivation classes codified:** `kb` (settled-history knowledge; live-URL backfill owed at audit) vs live-source keys. **Post-cutoff content: search-derivation MANDATORY, confidence ceiling c≤0.5, dossier pass owed** (the RotW/3.27+ rule).

## A2 — Chunked-emission protocol (now law)
Emit ~16–20 records per write · validate ALL lines parse after EVERY chunk · record-size budget ~1.0KB (mech_summary ≤ 2 sentences, ≤2 aliases, ≤2 key_items, notes only where they change a reconciliation decision).

## A3 — PoE1-specific fold rules (the volume problem)
PoE1's grain explosion (skill × ascendancy × mechanic × league) resolves by these folds:
1. **Record = named archetype-lineage.** Ascendancy variants FOLD into one record (RF Jugg/Inq/Chieftain = one) UNLESS the loop changes at lattice grain (CoC Ice Nova ≠ self-cast Ice Nova; mines ≠ self-cast where the community named them separately).
2. **The trigger IS the record** for trigger archetypes (CoC, Poet's Pen, Mjölner, CWDT loops) — host skills are variant notes.
3. **Item-defined archetypes are records** when the item IS the loop (Facebreaker, Whispering Ice, Poet's Pen, Mjölner, Death's Oath); pure amplifiers (Headhunter) are notes.
4. **Mechanic-modifier archetypes are records** when community-named as builds: Archmage, Low-Life Shavs, Aurastacker, Ward Loop, Autobomber.
5. **Transfigured-gem variants (3.23+) fold** into the parent lineage with era/variant notes unless the loop diverges (e.g. PConc of Bouncing → variant of PConc).
6. **Era bands:** `1.x`(2013-15) · `2.x`(2015-16) · `3.0-3.6` · `3.7-3.13`(peak) · `3.14-3.19`(nerf era) · `3.20+`(modern, incl. post-cutoff 3.27-3.28). Removed skills still harvest as era canon.

## A4 — PoE1 source plan
Rank-1: PoB codes (`pb`, team) · **poe.ninja league API (`pn`) — usage-share backfill is a TEAM job with API access; harvest proceeds on fame/longevity now, usage joins later.** Rank-2 live: mobalytics tier lists (`mb`), odealo build index (`od2`), maxroll-poe. Rank-3: wiki (`pw`), forum archive (`pf`), r/PathOfExileBuilds (`rd`), exitlag/skycoach 2026 overviews (`el`,`sky`). Post-cutoff era (3.27 wand rework, 3.28 Mirage, Minion Pact) = live-source-only records at c≤0.5.

## A5 — Coverage contract for this run
Deep canon COMPLETE + strong-moderate comprehensive (~90-105 records); shallow tail DOCUMENTED by name in the report (not recorded); negatives inline; per-league poe.ninja sweep + PoB-code attachment + usage-share columns = the team's completion pass. A coverage claim without this boundary statement is malformed.
