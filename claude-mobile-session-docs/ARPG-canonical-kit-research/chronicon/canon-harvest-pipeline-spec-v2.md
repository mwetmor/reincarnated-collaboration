# Canon-Harvest Pipeline — SPEC v2.0 (CONSOLIDATED)

**STATUS:** MATT-FACING · supersedes v1.0 + Amendment v1.1 (retained for provenance) · executable by the mobile track or the Mac team.
**Runs complete:** D2 (58 records) · PoE1 (91 records). **This document is the single source of truth going forward.**
**Job:** `substrate-coordinates.md` §7 Stage 1 at build grain. Feeds the roster (verdicts), projection-atlas §3 (gap records), and retrodiction dataset v1 (the FUN instrument's validation data, negatives included).
**TRIPLE LAW integration:** records project onto the LATTICE's locked vocabularies; unprojectable mechanics fire alarms; nothing here reopens closed placement rulings.

---

## §1 — Identity rule + THE GRAIN LAWS
A canon build = a **community-named mechanical loop**, never a class, never an item list. Naming is the canonicity filter. Key `{game}-{folk_name}`, lineage links across eras. Five grain laws (generalized from the PoE1 folds — they solved a 400+→91 volume problem and now apply to ALL games):
- **G1 — Archetype-lineage grain.** Class/ascendancy/set variants FOLD into one record unless the loop changes at lattice grain (CoC Ice Nova ≠ self-cast; RF Jugg = RF Inq).
- **G2 — The trigger IS the record.** For trigger archetypes (CoC, Poet's Pen, Mjölner, CWDT, Cast-on-Freeze), hosts are variant notes.
- **G3 — Item-defined archetypes are records** when the item IS the loop (Facebreaker, Whispering Ice, Mosaic); pure amplifiers (Headhunter) are notes.
- **G4 — Mechanic-modifier archetypes are records** when community-named as builds (Archmage, Low-Life, Aurastacker, Ward Loop, Autobomber). *Calibration finding: this class produces the corpus's highest-information rows — hunt it DELIBERATELY in every game.*
- **G5 — Sub-variant folding.** Transfigured gems, seasonal set-tweaks, and numbered-patch variants fold into the parent lineage with era notes unless the loop diverges.

## §2 — Game tiers + sequencing (updated by Matt's calls)
**Tier 1:** D2/D2R+RotW ✅ · PoE1 ✅ · **PoE2 ← current (pulled forward: same fold family while loaded, small young canon, the hardest post-cutoff test, and the closest living design cousin to RDR)** · D3 · D4 · Last Epoch · Grim Dawn. **Tier 2:** TQ, Torchlight 1/2/Infinite, Chronicon, Hades (commitment/boon evidence only). **Tier 2b (mobile-native live-service wing, per Hale's call):** Diablo Immortal (~30-35 records; MONETIZATION-CONFOUND RIDER mandatory — spend-stratified canonicity, discounted fame weights, PvE/PvP dual-meta split; sixth-Warlock + spin-lineage + D3-inheritance value) · Undecember (~18-24, Hades-style scope centered on link-rune grammar = the support-gem convergence test; Korean-trunk flagged per §9.9; western basin thin-and-souring). Harvest AFTER Tier 3 (confidence before breadth). **Tier 3 (adjacent-genre validation):** Vampire Survivors (genre anchor, evolved-weapon canon, ~25-30) · Halls of Torment (ARPG-bridge, ~20-25); tail: Brotato, Death Must Die, Soulstone Survivors — seated only if the VS run mints new GX. Purpose: out-of-distribution test of taxonomy convergence per §9.7's metric; run-convergence grain per §9.9. **Mods** (Median XL, PD2, PoD): harvest LAST, `mod:true`, excluded from retrodiction v1 — Matt ruling still pending.

## §3 — The five stages + emission law
1. **CENSUS** — enumerate names from pre-aggregated sources; two independent sources per name OR planner-data presence.
2. **DOSSIER** — 3–5 best sources → 2–4 sentence mechanical summary, original prose, ≤15-word quotes.
3. **PROJECTION** — constrained extraction against locked vocabularies. **THE ABSTAIN LAW: abstain-not-guess.** Per-axis `{v,c,abstain}`; unseen enums → source vocabulary + `abstain:true`; reconciliation maps, unmappable = gap record.
4. **RECONCILIATION** — dedupe, lineage assembly, roster verdicts (`duplicate-of:K#` / `variant-of:K#` / `new-cell-candidate` / `bench-evidence:B#`), gap routing.
5. **AUDIT** — ≥10% sample, inter-rater on projection axes; label quality gates the FUN instrument.
**EMISSION LAW (proven twice):** ~16–20 records per write · validate ALL lines after EVERY chunk · ~1.0–1.4KB/record (mech_summary ≤2 sentences, ≤2 aliases, ≤2 key_items, notes only where they change a reconciliation decision).
**COVERAGE CONTRACT (mandatory per run):** deep canon COMPLETE + strong-moderate comprehensive; shallow tail DOCUMENTED BY NAME, not recorded; negatives inline; team completion pass specified. A coverage claim without this boundary statement is malformed.

## §4 — Sources + derivation classes + THE POST-CUTOFF LAW
| Game | Rank-1 (mechanical truth) | Rank-2 (canonicity/usage) | Rank-3 |
|---|---|---|---|
| PoE1 | PoB codes (`pb`, team) | poe.ninja API (`pn`, team) · mobalytics (`mb`) · odealo (`od2`) | wiki, forum archive, reddit |
| PoE2 | planner links (team) | **mobalytics-poe2 (`mb2`)** · poe2 ninja equivalent (`pn2`, team-verify) · maxroll-poe2 | aoeah/boostmatch/mtmmo live lists, reddit |
| D2/D2R | — | maxroll (`mx`) · icy-veins (`iv`) · diablo-wiki (`dw`) | Basin wiki, Wayback era lists |
| D3 | — | maxroll/icy-veins set-archetype tiers | era snapshots |
| D4 | Maxroll planner links | maxroll/mobalytics tiers | season retrospectives |
| LE | lastepochtools | LE tier lists, forum compendia | reddit |
| GD | **Grimtools links** | forum build compendium | reddit |
**Derivation classes:** `kb` = settled-history knowledge (live-URL backfill owed at audit) vs live-source keys. **THE POST-CUTOFF LAW (fired on ALL THREE runs — now law): budget ≥1 era search per game before trusting knowledge; EXPECT ≥1 content stratum to postdate training** (RotW · 3.27/3.28 · PoE2 0.4-Druid/0.5). Post-cutoff records: search-derivation mandatory, **c≤0.5 ceiling, `dossier-owed`**, heavy abstains over confabulation. Era stratification riders and negative-canon riders apply to every run.

## §5 — Record schema (consolidated)
```json
{"id":"{game}-{folk_name}","game":"","folk_name":"","class":"","aliases":[],
 "eras":[],"lineage":"","context":"pve(omit)|pvp|party","flags":["degenerate-famous"],
 "canon_tier":"deep|moderate|shallow|negative","neg_twin":"id-of-successful-sibling",
 "canonicity":{"longevity":"","fame":"","evidence":[]},
 "mech_summary":"","core_skills":[],"key_items":[],
 "proj":{"attr":{},"range":{},"tempo":{},"amp":{},"proxy":{},"commit":{},
   "geo":{},"ctrl":{},"def":{},"econ":{},"mob":{},
   "elem_p":{"src_vocab":"<game>","abstain_map":true},"elem_s":{},"hyb":{}},
 "gap_refs":[],"prov":[],"negative":false}
```
Conventions: per-axis `{v,c,abstain?,note?}` · c≥0.8 sourced-solid, 0.5–0.7 informed projection, <0.5/abstain = reconciliation queue · **elements ALWAYS in source vocab with `abstain_map:true`** (the canonical 8-element enum stays unguessed) · **host-dependent convention** for delivery-agnostic mechanic archetypes (low c + note) · **source-truth-over-conformance:** record what the source game does even where it violates RDR law (tri-element swings etc.); reconciliation adjudicates · **negative-twin annotation:** failures pair with a same-family success where one exists (Charged Dash↔Flicker; Wild Strike↔Elemental Hit; PoE2 Concoction↔PoE1 PConc) — the highest-value contrastive rows in the retrodiction set.

## §6 — THE CROSS-GAME GAP LEDGER (GX) — consolidation centerpiece
Per-game GAP-{D2,P1,P2}-nn IDs remain local evidence pointers; recurring findings PROMOTE here. Reconciliation reads THIS table.
| GX | Name | Evidence so far | Routes to |
|---|---|---|---|
| GX-01 | Movement verbs load-bearing | D2-01 (Teleport/Charge/Blaze) · P1-03 (Flicker, Autobomber; Charged Dash = negative twin) | B5/B6 · F4 CONFIRMED |
| GX-02 | Form/state-shift, kit-within-kit | D2-02 (were-forms) · PoE2 Demon Form, **Shaman bear** | NOVEL — no roster surface; hearing owed |
| GX-03 | Mark-and-consume / apply-then-detonate | D2-03 (MA charges) · P1-02 (Earthshatter, Hexblast, Conduit, BF/BB, Discharge) · **PoE2 combo grammar is this MAINLINED** (bell, primed ailments, armor-break) | §5 phase axis — strongest cross-game signal in the ledger |
| GX-04 | Corpse/resource-manufacture economies | D2-04 (CE, Find Item) · P1 (DD, General's Cry) | Axis-5 reserved-bin candidate |
| GX-05 | Reservation economies | P1 named occupants (Aurastacker, LL Shavs, Aurabot) · **PoE2 Spirit system = reservation as core resource** | Axis-5 reserved bins |
| GX-06 | Self-damage economies | P1-01 (RF, Boneshatter, FR, Dark Pact, loops) · PoE2 Blood Mage, Infernal Legion | Axis-5 candidate; K26/K27 adjacency |
| GX-07 | Gear-stat-as-weapon | P1-08 (7 builds) · D2 (none — POST-D2 innovation, era finding) · PoE2 (HoWA, Gemling, Pillar) | stat-is-the-build family |
| GX-08 | Conversion chains | P1-05 (LS, FB, TS, wander) | Codex surface/mask CONFIRMED |
| GX-09 | Body-orbit / autonomous orbiters | P1-06 (**Poison BV anchor**, Winter Orb, Helix, BL) | rotational addendum |
| GX-10 | Boomerang return paths | P1-07 (Spectral Throw, Venom Gyre) | dr/dt sign-flip family |
| GX-11 | Proxy-executes-player-skill | P1-09 (General's Cry) · PoE2 **Hollow Form clones, Mirage Deadeye** | novel proxy mode |
| GX-12 | Stochastic element selection | P1-10 (Ele Hit; Wild Strike = negative twin) | exceeds element schema — ruling owed |
| GX-13 | Enemy-roster-as-arsenal | P1-13 (Spectres) · D2-11 (Bind Demon) · PoE2 **Puppet Master/Command keyword** | **reap-verb cousins — mechanics + fiction memo for Matt** |
| GX-14 | Consumable/loot-as-ammo economies | P1-12 (PConc flasks, Animate Weapon, Wormblaster) · PoE2 charms; **Concoction FAILED in PoE2 = negative twin** | Axis-5 candidate |
| GX-15 | Multi-element cap collisions | D2-10 (Avenger) · P1 (Discharge, Golementalist, Wild Strike) | element addendum ruling owed |
| GX-16 | Party-external scaling | D2-05 (Enchant, BO) · P1 (Aurabot) | out-of-scope solo filter; mob/party layer |
| GX-17 | Zero-button automation edge | P1 (CWDT/Ward loops, Autobomber) · PoE2 (0.4 CoC-automation meta, Walking Calamity) | engagement-axis edge; blacklist calibration |

## §7 — Canonicity + negative canon
`canon_tier` from usage telemetry where it exists, tier/guide fame, **longevity across patches (strongest)**, naming persistence. Deep = nerf-survivor; shallow = one-league wonder; negative = documented-bad. **Degenerate-famous flags:** excluded from positive retrodiction, kept as blacklist-calibration references. **Arc recording:** rebirth (FoH, Hydra) and re-kill (Blood Mage) arcs live in `eras[]` + notes — patch-response history is KPI-validation gold.

## §8 — Audit, ops, publication, ledger
Audit per §3.5. Ops: API-first, rate-limit courtesy, no player PII, Wayback for era-authentic lists. Publication (inherits §10): census = devlog gold; projected coordinates = basement; negative canon publishable as genre history; gap ledger internal. **Deliverables ledger:** shipped — spec v1+A, D2 corpus 58 + report, PoE1 corpus 91 + report, this v2. Owed — team passes (pn/pb backfill, kb URLs, post-cutoff dossiers ×6, audits ×2→3), Warlock dossiers, GX-02 hearing, GX-12/GX-15 rulings.

---

# §9 — v2.1 FOLD (post-PoE2 learnings)

## 9.1 — Ledger extensions (provisional pending Matt ratification ⚑)
| GX | Name | Evidence | Routes to |
|---|---|---|---|
| GX-18 ⚑ | Barrier-terrain builds | D2-09 (Bone Prison/Wall) · PoE2 Wall of Shields (0.5-executed) · PoE1 Frost Wall tech | B4 re-spike |
| GX-19 ⚑ | Commitment/cost transfer to proxies | PoE1 (Pizza Sticks carry the channel; FR totems pay the life cost) · PoE2 (Warbringer totems absorb slam wind-ups; Archmage totems absorb mana costs; Snipe's mirage executes the channel) | commitment axis — proxies that ABSORB an axis value are distinct from proxies that merely deliver damage |

## 9.2 — Delta-pass protocol (new standing obligation class)
Live-service games spawn RE-HARVEST TRIGGERS, tracked here: **PoE1 3.29 "Curse of the Allflame" (July 24, 2026)** — delta pass after the meta settles · **PoE2 1.0 launch** — era frame resets, delta census (0.5's 21-skill tail + launch meta) · **D2R next season** — low-priority delta. A corpus without its delta obligations listed is stale-by-design.

## 9.3 — Coverage sizing heuristic (three-run calibration)
Mature-consolidated canon (D2) ≈ 55-65 records · mature-sprawling (PoE1) ≈ 90-105 · young live game (PoE2, 19mo) ≈ 35-45. Sizing far off these bands signals a grain error, not diligence.

## 9.4 — Nerf-list rider (new source class)
Patch-note kill lists and community "dead on arrival" lists are ERA-STAMPED NEGATIVE CANON — harvest them deliberately each run (PoE2 0.5's list yielded four records in one pass). They are the cheapest high-quality negative evidence in the pipeline.

## 9.5 — Deliverables ledger (updated)
Shipped: spec v1+A · spec v2.0+9 · D2 58 · PoE1 91 · PoE2 38 (**187 records, zero invalid**). Owed: team passes (pn/pb/pn2 wiring, kb URLs, post-cutoff dossiers ×13, audits ×3) · GX-02 hearing (now THREE games) · GX-12/15 rulings · GX-18/19 ratification · delta passes per 9.2. Next run: **D3** (set-archetype grain per v2 §2).

## §9.6 — v2.2 FOLD (post-D3 learnings)
- **Numeric-rating rider (new source class):** wherever a game publishes per-build numeric power ratings (D3 GR ceilings, PoE usage %, D4 Pit tiers), scrape as a `power_rating` column — ratio-scale ground truth outranks ordinal tiers for KPI validation. Hunt one per game.
- **Archetype-authorship classification (per-game metadata):** tag each game `authored` (D3 — sets ARE the builds; tier lists read as designer intent + obedience) / `emergent` (D2, PoE — builds are discovered; usage = discovery telemetry) / `hybrid` (D4 aspects, LE — partial authored capstones over free recombination). Changes how canonicity evidence is interpreted per game. Doctrine-pass flag: authored capstones require an emergent-recombination layer (the LoD lesson).
- **Negative taxonomy (four classes, codified):** `born-bad` (trap skills: Impale, Sweep) · `setless-orphan` (authored games: Wave of Force) · `killed-by-nerf` (Shield Bash — made dead, left dead) · `failed-port` (cross-game neg-twins: PoE2 Concoction). Tag in canonicity notes going forward.
- **Timing-window economies** (Tal rotation, CoE) stay PARKED under GX-03 notes pending the timing-axis addendum revival.
- **GX-02 escalated:** four sightings, three games, no roster surface — hearing flagged PAST DUE in the ledger.
- **Ledger:** 233 records shipped (D2 58 · PoE1 91 · PoE2 38 · D3 46), zero invalid. Next: **D4** (hybrid-authorship, aspect-archetype grain, Pit-tier numeric rider, Lord-of-Hatred/Warlock post-cutoff stratum expected).

## §9.7 — v2.3 FOLD (post-D4 learnings)
- **Cross-game lineage assembly = first-class reconciliation deliverable.** Where a thread spans games, `lineage` takes a genre key (`genre/hammerdin`, `genre/spin`, `genre/rabies`, `genre/frozen-orb`, `genre/hydra`, `genre/bell`, `genre/wandering-hazard`, `genre/incinerate`). The lineage table is longevity-canonicity at maximum strength AND the genre's own vote on load-bearing loops.
- **Design-Law candidate register (new output class):** DL-01 authored capstones require an emergent-recombination layer (D3/LoD) · DL-02 movement-verb damage requires low friction (Flicker↔Charged Dash) · DL-03 channel viability is a function of the game's movement tax, not the channel's numbers (poe1↔d4 Incinerate twin). Laws graduate to doctrine only by Matt ruling; harvests may nominate.
- **Watch list convention:** 2-3-sighting patterns park as sub-notes awaiting promotion (immunity-uptime under GX-17 · generator-as-spender-inversion under econ, 3 sightings — promotion candidate at 4).
- **Convergence health metric:** new-GX-entries-per-run is now tracked (D2 seeded · PoE1 +2 · PoE2 +2⚑ · D3 +0 · D4 +0). A maturing taxonomy should trend to zero; a spike on a NEW-subgenre game (Hades-likes) is signal, not failure.
- **Ledger:** 278 records (D2 58 · PoE1 91 · PoE2 38 · D3 46 · D4 45). Next: **Last Epoch** (hybrid authorship — per-skill trees = authored micro-capstones; corruption/arena = numeric rider; GX-02 motherlode expected via Druid forms + Reaper Form).

## §9.8 — v2.4 FOLD (post-LE learnings)
- **Ratification-package convention:** a GX slot is "hearing-ready" when it holds a ≥3-game exhibit with positive AND negative exemplars. Status changes: **GX-02 hearing-ready** (five-game exhibit: D2 wereforms · D3 Archon · D4 Pulverize/Werenado · PoE2 Demon/Bear · LE Druid-trio+Reaper) · **GX-18 hearing-ready** (D2 Bone Prison · PoE2 Wall of Shields · LE Frost Wall, plus Chronomancer as the negative pole). Promotion remains Matt-only.
- **DL-04 nominated:** control archetypes require an attached kill loop; occlusion/CC alone never sustains a build (Frost Wall-with-loop succeeds; Chronomancer and Kick fail without).
- **Authorship sub-axis — WHERE authorship lives:** build-grain (D3 sets) · item-grain (D4 aspects, LE uniques) · **skill-grain (LE per-skill trees — preserves recombination; the doctrine-preferred pole)**. Hybrid tag now carries the grain qualifier.
- **Thin-stratum flag convention:** when a training-era band is thin (LE 1.3/S3), the report flags it and the dossier sweep routes at it — coverage-contract addendum.
- **Watch list:** support-verb-weaponized (Healing Hands) parked at 1 sighting · generator-as-spender-inversion holds at 3.
- **Ledger:** 313 records (D2 58 · PoE1 91 · PoE2 38 · D3 46 · D4 45 · LE 35). Ruling queue for Matt: GX-02 · GX-18/19 · GX-12 · GX-15 · Warlock attr (3 pts) · 8-element mapping · DL-01..04. Next: **Grim Dawn** (emergent-tilted authorship, dual-class combo grain, Grimtools Rank-1, Crucible/SR = numeric rider, FoA/Berserker = expected post-cutoff stratum).

### §9.8a — Mid-run ledger entry (GD harvest)
- **GX-20⚑ default-attack-as-build (PROPOSED, pending Matt):** the generator-as-spender-inversion watch item crossed the 4-sighting promotion threshold during the GD run — exhibits: D3 GoD Hungering Arrow · D4 Bash · D4 Heartseeker · GD Belgothian WPS · GD Fire Strike. Pattern: the zero-cost default attack carries the entire endgame while "real" spenders become support. Negative pole: D4 Blade Shift, LE Shield Bash (defaults that failed). Watch item retired into the proposal.

## §9.9 — v2.5 FOLD (post-GD learnings + Tier 3 grain)
- **Watch-list lifecycle VALIDATED:** GX-20⚑ registered via §9.8a — first item to complete park(2-3)→promote(4)→ratify(pending). Sustained-beam sits at the boundary (AAR · FoI · Drain Essence · LE Disintegrate-tail); count on the next run, promote at a clean fourth cross-game sighting.
- **DL-01 purpose rider:** authored pockets serve ENTRY, emergence serves DEPTH (Krieg lesson — the beginner king is beginner-king BECAUSE authored, inside an emergent sea).
- **Host-multiplication sizing rider:** dual/combo-class systems multiply HOSTS, not archetypes — record the archetype once, carry combo names as aliases; sizing bands read archetype-count, not host-count.
- **Second-canon-basin convention:** non-English community basins (Chinese GD top-20 crossover) get a provenance flag and a dossier-pass lane.
- **Vendor note:** Dammitt adapter covers grimtools + lastepochtools — one scraper, two Rank-1 sources.
- **Reconciliation item:** consider renaming `genre/rabies` → `genre/contagion` (members: rabies, pox, touch-of-death).
- **Tier 3 run-convergence grain (governs VS/HoT):** records = draft-convergence archetypes (evolved weapons, named synergy stacks); canonicity = tier lists + unlock/evolution canon; `attr` abstains by default; econ vocab extends (draft-economy, banish, curse, reroll); GX-17/GX-09 saturation EXPECTED — the convergence metric is formally armed for this tier, and new-GX spikes there are signal.
- **Ledger:** 354 records (58 · 91 · 38 · 46 · 45 · 35 · 41). Tier 1 ✅ COMPLETE. Next: **TQ** (Tier 2 lead — GD's direct ancestor; expect an INHERITANCE-lineage finding distinct from convergent lineage; TQ2 EA status = era-rider question).

## §9.10 — v2.6 FOLD (post-TQ learnings)
- **Lineage edge types formalized:** reconciliation carries `lineage_edge: inheritance | convergence`. Inheritance (Iron Lore→Crate, TQ→TQ2) predicts mechanical fidelity; convergence (hammerdin, spin) predicts the genre's independent vote. Deliverable: the genealogy map joins the lineage table.
- **Negative-decay rider (KPI weighting):** negative canon has a half-life — in old consolidated communities, weak skills vanish from discourse instead of being documented. Absence of negative canon ≠ balance evidence; retrodiction treats it as missing data.
- **Numeric-rider abstention class:** pre-live-service games legitimately lack ratio ladders (TQ1 = first abstention). Canonicity weight shifts to longevity+fame; the KPI stage must not penalize the era.
- **Provenance credibility flags:** `STALE` (abandoned wikis) and `LOW-CRED quarantine` (slop-adjacent sites, corroboration-only) join the config.
- **Delta cadence metadata:** the §9.2 delta ledger now carries cadence (TQ2 = quarterly, fastest subscription; PoE1 3.29 = July 24 ⚠ 13 days).
- **GX-17 hearing addendum:** aim-automation texture (TQ2 Stormblade self-targeting volleys) filed with the exhibit.
- **Ledger:** 380 records (58 · 91 · 38 · 46 · 45 · 35 · 41 · 26). Next: **Torchlight line** (TL1/TL2/Infinite per Matt's tier call — TL3 excluded; the SECOND Blizzard-diaspora inheritance tree: Runic/Schaefer line vs Crate/Iron Lore line; TLI = live post-cutoff stratum + primary Chinese canon basin per the §9.9 convention).

### §9.10a — Mid-run ledger entry (Torchlight harvest)
- **GX-21⚑ sustained-stream-channel (PROPOSED, pending Matt):** the beam/stream watch item reached ratification shape when TL2's Arc Beam supplied a clean second negative pole. Cross-game exhibit: poe1-incinerate(+) · gd-aar(+) · gd-flames-of-ignaffar(+) · gd-drain-essence(+) · le-ghostflame(+) · d4-incinerate(−) · tl2-arc-beam(−) — five games with positives, two with documented negatives, and the failure causes align (rooted channel vs movement tax = DL-03; pool-drain economics). Family definition: continuous directed stream (line beam or cone) as the build's primary, distinct from the commit axis by being an ARCHETYPE identity rather than a commitment value.

## §9.11 — v2.7 FOLD (post-Torchlight learnings)
- **Grain follows the community's ranking unit:** TLI tiers TRAIT VARIANTS, not heroes (Erika 1 ≠ Erika 3) — the §9.9 host rider with the sign flipped. Rule: record at whatever grain the canon basin itself ranks (combo names in GD, trait variants in TLI, element-tree+set in small-basin indies).
- **Negative ledger has three grains:** skill (Blade Trap) · build (setless orphans) · **GAME (TL3's commercial failure — doctrine-file evidence, not corpus records)**.
- **DL external-corroboration convention:** when a community independently states one of our laws (Vorax notes: "stationary builds struggle" = DL-03 verbatim), log it on the DL register as corroboration — laws strengthen without re-derivation.
- **GX-14 formal watch count:** consumable-as-ammo at 2 live exhibits (Carino ammo, Sage elixir) + PoE1 ancestors — promote at 4 per convention.
- **Primary-basin inversion:** TLI = first game whose non-English basin is the TRUNK; §9.9 convention extended.
- **Ledger:** 402 records (58 · 91 · 38 · 46 · 45 · 35 · 41 · 26 · 22). Next: **Chronicon** (solo-dev indie; SECOND authored-at-build-grain game after D3 — classification test: do its escape valves dodge the LoD trap?; Warlock class = FIFTH data point; Mechanist DLC = GX-19 in a third lineage context; Anomaly depth = numeric candidate; small-basin naming caveat expected).

## §9.12 — v2.8 FOLD (post-Chronicon learnings)
- **Title-telemetry source class:** guide titles carrying per-build ceilings (Chronicon T-numbers) populate `power_rating` AT HARVEST — re-check all Steam-native basins for the pattern.
- **Zero-negative declaration protocol:** corpora may ship 0 negatives with explicit decay-rider citation + a dossier-archaeology lane; missing data declared, never padded.
- **Tag-ontology armor (engine doctrine note → Matt):** Drone Pilot's turrets-reclassified-as-drones shows games exploiting their own tag taxonomies. RDR rule candidate: recategorization multipliers are intentional design surface, never emergent tag leakage — the content engine's tag graph needs type walls.
- **GX-12 hearing reframed:** the genre monetizes stochastic identity AND its deletion (Ele Hit/Prismatic vs Crown of Innate Probability). The ruling question is now "when is each pole the capstone," not "is randomness good."
- **Joint-echo signal class:** communities independently drawing our taxonomy's internal joints (thorns≠retaliation, Erika=flicker, Vorax=DL-03) is now a logged validation signal — three instances on record.
- **Ledger:** 419 records (58 · 91 · 38 · 46 · 45 · 35 · 41 · 26 · 22 · 17). Next: **Hades, NARROW SCOPE** — commitment/boon evidence only per the §2 tier call: duo-boon capstone grammar, verb-slot commitment system, Privileged Status as GX-15 evidence, dash-verb GX-01 exemplar, Hades II Omega/Magick strata. Small evidence corpus, freely-abstaining non-scope axes, findings-first report.

## §9.13 — v2.9 FOLD (post-Hades learnings + Tier 2b amendments)
- **Fourth authorship grain: PAIR-grain** (Hades duos — the combination IS the unlock). Grain table now: build (D3) · item (D4/LE-uniques) · skill (LE trees) · pair (Hades). Pair-grain flagged as RDR's reap-system natural fit: author the collision, let the player discover it. → Matt with the table.
- **`deferred` commit-value nominated** for the commit axis (Doom: damage committed at hit, delivered on delay; Hephaestus blast = second authored member).
- **GX-15 hearing gains the mechanized exhibit:** Privileged Status = the cap authored at exactly 2, shipped in both Hades games.
- **Title-telemetry GENERALIZED:** confirmed outside Steam-native basins (Mobalytics Fear-rated verified builds) on first re-check.
- **Cadence law logged (liftable):** fast verbs pair with additive damage sources, slow verbs with percentage amps — community-stated boon-pairing rule; RDR loot-operator input.
- **Tier 3 bridge vocabulary pre-registered:** keepsake pool-steering = PLAYER-STEERED DRAFT; the §9.9 run-convergence grain's econ vocab (draft-economy, banish, curse, reroll) gains `pool-steering`.
- **Tier 2b seated (Hale's call):** DI + Undecember per §2, with the **monetization-confound rider** as new methods work — first corpus games whose fame/tier telemetry is spend-stratified; canonicity weights discounted accordingly. TLI retroactively tagged as the wing's existing partial specimen.
- **Ledger:** 432 records (58 · 91 · 38 · 46 · 45 · 35 · 41 · 26 · 22 · 17 · 13). Tier 2 ✅ COMPLETE. Next: **TIER 3 OPENS — Vampire Survivors + Halls of Torment** under the §9.9 run-convergence grain. Convergence metric ARMED: GX-09/GX-17 saturation expected; new-GX spikes are signal; attr abstains by default; pair-grain gets its out-of-distribution test via union evolutions.

## §9.14 — v2.10 FOLD (post-Tier-3 learnings: VS + HoT)
- **CONVERGENCE VERDICT FORMALIZED — INSTRUMENT VALIDATED:** zero new top-level GX across two out-of-distribution games; GX-09/GX-17 saturations landed as predicted; metric series closes seeded, +2, +2⚑, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0. Retrodiction stage may proceed on a stable taxonomy.
- **Watch-list: harvest-radius economy** parked at 2-3 sightings (Gorgeous Moon vacuum-verb, Je-Ne-Viv magnet-as-damage, Gatti anti-harvest negative pole). Promote at 4.
- **Candidate FIFTH authorship surface: the modifier deck** (VS arcana authoring archetypes — Out of Bounds rewires freeze into a kill loop). Grain-table question → Matt: build · item · skill · pair · deck?
- **System-grain negative class minted:** golden-egg eternal scaling — guide-documented "99% of builds no longer matter." **RDR DOCTRINE FLAG: reincarnation-as-leveling must cap, rotate, or gate — never inflate unboundedly.**
- **Canon-flip methods note:** Clock Lancet (trap→Death-killing core) — community canon self-corrects; KPI ground truth requires snapshot-dating.
- **DL-03 CAUSALLY ISOLATED + GX-21 hearing addendum:** HoT's Dragon's Breath thrives because the genre deleted channel commitment — the stream family's killer was the stillness, never the stream. Filed as the controlled experiment.
- **Bridge-grammar results:** gear survives the horde frame; loot-retrieval is SPATIAL (the walk carries a third job); reroll/lock potions = pool-steering in item form; artifact stacks = self-authored difficulty; offer-pool hygiene = negative-space drafting.
- **Hybrid structure minted:** `derived_from_other_skill` (Landsknecht grenades — output-as-input).
- **Warlock exhibit at seven games** counting DI-incoming; HoT shows the NAME travels where stat systems don't (abstains-by-grain).
- **JP basin wired** (dood.gg; "Red Death-class" = informal ratio scale).
- **Ledger:** 475 records, thirteen corpora. Next: **TIER 2b OPENS — Diablo Immortal, MONETIZATION-CONFOUND RIDER ARMED:** records carry `spend_stratum` (f2p-viable | whale-gated | mixed | unclear) + `meta` (pve | pvp | dual); fame weights discounted where wallet-gated; PvE-primary harvest with PvP thrones noted in canonicity. Era search banked this session (Patch 5.0 Bloodied Jewel, Warlock class June 17 2026).

## §9.15 — v2.11 FOLD (post-DI learnings)
- **Monetization-confound rider VALIDATED at three levels** (community wallet-split language · system-grain anchor record · numeric stratification clause). Rider template now reusable for any monetized-power title.
- **Sizing-law precedence codified:** seating estimates are non-binding; grain-follows-ranking-unit overrules (DI: 23 honest vs ~30-35 seated — under-shoot is correct behavior, padding is corpus corruption).
- **Two signal classes minted, schema names owed before retrodiction:** `frustration-canon` (fame measured in grievances — Druid spirit form) · `support-canonicity` (value measured in allies' output — Banner Crusader).
- **Warlock exhibit RULING-READY:** seven recorded games, INT consolidated (TQ DEX/INT · d2r abst · d4 abst · LE .6 · Chronicon .7 · HoT abst-by-grain · DI .4 launch). → Matt.
- **Vendor self-KPI note:** Blizzard's CoE exclusion of launch-Warlock "while gathering live data" = a commercial validation gate parallel to the five-stage doctrine.
- **DL-03 discriminates WITHIN one game:** DI ships the taxed rooted channel (Ray of Frost) beside move-shoot fusions (Strafe, mobile Whirlwind) — axis resolution confirmed at title grain.
- **Inheritance edge made mechanical:** D3→DI essence transfer = portable authored modifiers; reconciliation note — item-grain authorship where the MODIFIER, not the item, is the durable object.
- **Ledger:** 498 records, fourteen corpora. Next: **Undecember closes Tier 2b** — link-rune scope (the support-gem convergence test), Korean trunk per §9.9, western basin thin-and-souring (records carry `basin:"kr-trunk"`), ~18-24 Hades-style scoped run. Era search banked (Season 11 The Forge, May 14 2026); build-canon search authorized as the game's meta search.

## §9.16 — v2.12 FOLD (post-Undecember learnings) + ATLAS DIRECTIVE
- **Support-grammar portability verdict:** 6-link ceiling, tag-gating, and trigger meta-grammar (CwC) survive transplant verbatim across four live years; hex-color geometry and shared-link topology are the mutations. **Load-bearing parts survive any container; geometry is free design space** — RDR loot-operator finding of the wing.
- **Attractor-state conclusion:** the classless pole converged on the same archetype set as every class game (spin@10, archer, elementalist, summoner) — GX families are attractor states of genre physics, not class artifacts.
- **Person-grain provenance** (KR author culture: Ya55, Daimonios) + **tri-basin stratification** (KR trunk · EN stale-skewed branch · RU tooling).
- **Ledger:** 515 records, fifteen corpora, Tier 2b ✅. All seated tiers harvested except mods (Matt-gated).

### ATLAS DIRECTIVE (v1 — Hale's synthesis order)
- **Coordinate cell key = the OOD-STABLE axes:** `delivery(proxy) × geometry(geo) × commitment(commit)`. Rationale: these three discriminated in every tier and survived both transplants (T3 collapsed attr and mob; elements never mapped; econ is flavor). The space is built from what proved genre-invariant.
- **System/meta records** route to a `SYS|<econ-family>` annex cell class; they are mechanics evidence, not kit candidates.
- **Representative selection within a contested cell (priority order):** game-tier authority (T1 > T2 > T2b > T3) → canon depth (deep > moderate) → lineage weight (named lineage / GX refs) → mean projection confidence. **Negatives are never representative** — they remain in-cell as the cautionary member. Narrow-scope and post-cutoff placeholders are representative-eligible only if no full-scope member exists.
- **Mechanics gating column:** every kit carries `mechanics_status` ∈ {have-core, designed-addendum, partial, blocked-new, verify} + named `blocking_mechanics`, mapped from GX refs and cell class against RDR's current engine surface (battle-sim auto-aim, soul-control troop command, loot-operator framework, orbital/rotational addendum, element-hybridity addendum, reap/possession native). **Status column is a DRAFT for Mac-team second pass** — build decisions follow their validation.
- **Ingest status:** all fifteen corpora were on disk — v1 atlas covers the FULL 515 records. Generator is re-runnable: drop future corpora (mods tier, deltas) into outputs/ and re-run. First pass at 3-axis cells proved under-grained (110-record heartland cell); family suffix added per the attractor-state conclusion → 231 kit cells + 18 SYS annex cells, 80 contested, 223 representatives.

### §9.17 — ATLAS v2: UNIQUE KEY + ROSTER INGEST
- **Unique kit key (14 slots):** `AAAAAA-MMMM-EE-LL-~~` = six BC-SAMPLED codes (attr·range·tempo·amp·proxy·commit) — four BC-MEASURED codes (mobility·geometry·control·defense) — econ-behavior bin (2-char, cost-TYPE bins RESERVED) — identity element (2-char, L3/L4 factor; `VR` = partition pin) — two RESERVED slots (commit arity-gate `E`/deferred; future surface). `_` = abstain; `key_completeness` counts resolved slots. Codebooks live in the generator header; WITHIN-CELL CONFIG and CONSTRAINT/TRANSFORM classes carry no key slots per the scope rule.
- **Grouping at unique grain:** 554 rows → 491 unique kit addresses · **10 true convergence groups** (same address, different games — e.g., the archer address ToS/Wander/Quill-Volley/Spread-Rapid across three tiers; the fire-stream address holding poe1(+)·ud(+)·d4(−)) · 19 SYS annex · 32 UNPLACED. Family cell_id retained as browse column.
- **Roster ingest protocol:** `rdr-roster-kits.jsonl` = 7 anchors (Fo·Bv·Ww·Mo·Sw·Dg·Gw) with DRAFT projections from atlas mocks + canon ancestry (`mac-validate` flagged) + 24 schema-complete ROSTER slots + 8 BENCH slots for Mac fill — no invented kit names (DI sizing precedent applies to our own roster). Incumbents rank first in-group (Ww collision won by the anchor). Mac fills placeholders from Codex v0.9 → re-runs generator → v3.

### §9.18 — ROSTER OF RECORD MERGED (atlas v3) + mock-anchor correction
- **Correction owned:** the seven "anchor" rows ingested at v2 were SYNTHETIC display-contract data from the chart mock (Gravewaltz included — mock-invented). Dropped. Real roster = **Part F: K1–K29 + H1–H6 (35) + bench B1–B13 (13) = 48**, recovered from today's transcripts.
- **Recovery provenance:** K1–K12 BC cells VERBATIM (in-message paste) · B1–B13 VERBATIM (bench table paste) · K15/K20/K23+H5 path-substrate, K20=orbiter_spiral Hammerdin, proxy octet (K5/K10/K16 light · K11/K17/K18/K24/K25 heavy), K1/K23 channel-class, H5=True Battlemage, H1=-lite guard, K26–K29 F5 mechanisms — from cross-refs · K13/K14/K19/K21/K22 + H2–H4 identities unrecoverable → `mac-fill` rows.
- **Grain law extension:** rows with `key_completeness < 4` route to UNRESOLVED, never to key-groups — an unknown address is not a shared address (applies to sparse canon rows too).
- **Bench mechanics = truth-driven:** blocker text maps directly to mechanics_status (promotions→have-core · B12→partial pending zero-diff re-cert · holds/blocks→blocked-new with the named gap).
- **Mac handoff:** fill UNRESOLVED + K12 remainder from substrate-coordinates.md; gauntlet fills BC-MEASURED axes; re-run generator → v4.
