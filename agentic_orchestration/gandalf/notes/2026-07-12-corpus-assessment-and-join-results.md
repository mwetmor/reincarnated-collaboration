# Corpus assessment + roster-join results — ARPG canonical-kit research (mobile session)

**Date:** 2026-07-12 · **Author:** gandalf (ELICITOR, senior-designer lens) · **Mode:** Pattern B (Matt terminal dialogue), durable capture
**Commission:** Matt 2026-07-12 — "ultra think as you research the details found within `claude-mobile-session-docs/ARPG-canonical-kit-research/` and assess it wholistically with the lens of our knowledge base, engine mechanics, serial content pipeline and modular godot plans" + questions A–D + views follow-on.
**Governing pauses (Matt-ruled, recorded in serial tracker thirteenth delta):** (1) periodic-table work PAUSED pending corpus integration; (2) emission moment PAUSED pending mechanics-add decision. Both return-quickly scoped.

---

## 0. Top-line verdict

**Adopt the corpus as substrate. Integration is a JOIN problem, not a rebuild.** The mobile session independently converged on our atlas philosophy (abstain-not-guess, per-axis confidence, convergence-as-signal) and produced a 15-game / 563-record / 505-address corpus whose schema is compatible with our 14-slot key space. Our 35-kit roster is already encoded in the corpus's own vocabulary (`rdr-roster-kits.jsonl`). The empirical join (run this session, § 3) shows lineage falls out computationally — no broad legolas probe needed.

## 1. Question A — inclusion / pollution

**Keep all 15 games. Tag, never remove.** The corpus already implements Matt's tag-don't-remove instinct: tier weights (`T1:4, T2:3, T2b:2.5, T3:2`), spend-stratum riders on mobile titles, negative-twin annotation, era stamps. Pollution guard belongs at the **view/consumption layer** (filter or down-weight at query time), not the crawl layer — same law as the style-register consumption-time filter.

- **Halls of Torment is an unblessed 15th game** (`vampire-survivors/canon-corpus-hot.jsonl`) — absent from Matt's 14-game tier list. Needs a Matt ruling: bless at T3 alongside VS, or flag `experimental`. Either way it stays in the corpus.
- **Recommend explicit `scope` flags** on games: `core-canon` (T1), `breadth` (T2), `monetization-informant` (T2b), `experimental` (T3 + HoT). VS/HoT earn their keep as OOD validators — zero new GX families emerged from them, which is the convergence-stability proof itself.

## 2. Question B — precision / schema sufficiency

**Precise enough to house everything, because it refuses to over-claim.** The {v, c, abstain} per-axis structure + ABSTAIN LAW + POST-CUTOFF LAW (c≤0.5) + coverage contract mean gaps are *recorded as gaps*, not silently filled. The corpus enumerates its own owed backfills (dossier-owed rows, verify rows, PoE1 3.29 delta due ~July 24).

**Four precision findings from my read (gaps to close at ingest, not blockers):**
1. **Per-slot confidence is LOST in the CSV** — generator collapses to `avg_conf = mean(proxy_c, geo_c, commit_c)`. The JSONL retains per-axis {v,c}; the DB ingest must preserve per-axis, treat CSV as a derived view.
2. **Family assignment is fragile** — `family = gx_list[0] or 'econ:'+bucket`; first-GX-listed is an accident of harvest order, not a ranking. Views should treat family as a *set*, not a scalar.
3. **`norm_geo` is lossy** — 'zone'→LARGE, 'melee-radius'→SMALL collapses distinct geometries our engine distinguishes. Keep source vocab in DB; normalize at view time.
4. **Measured-vs-projected epistemic split needs an explicit ruling** — corpus kits are *projected* into BC space (ghost dots); our roster kits are *gauntlet-measured* (or will be). These must never render as the same class of claim. Proposed law: corpus = hollow/ghost glyphs, roster = solid, in every view.

## 3. Question C — roster ↔ corpus mapping (EMPIRICAL JOIN, run 2026-07-12)

Atlas CSV holds **35 roster rows** (K1–K29 + H1–H6; bench B1–B13 not in-atlas). **17 placed** (key_completeness≥4), **18 UNRESOLVED** (mac-fill: K13/K14/K19/K21/K22, H2–H4 identity-unrecoverable; octet kits kc=2; ex-bench K26/K28/K29 kc=3).

**Zero exact-address collisions** — by construction (roster abstain `_` slots make keys distinct). The meaningful join is **wildcard-compatibility** (roster `_` matches any corpus char):

| Kit | Coordinate verdict | Corpus lineage at coordinate |
|---|---|---|
| K12 Standard Wizard | densest genre attractor | 43 kits / 13 games |
| K7 Archer | ON the archer convergence group | 17 kits / 10 games (Tornado Shot, Lightning Arrow, GoD Hungering Arrow) |
| K2 Light Fighter | ON the WW/Cyclone melee attractor | 16 kits / 10 games (Boneshatter, Spin-to-Win, WW STR baseline) |
| K6 Dagger Assassin | dense | 10 kits / 6 games |
| K9 Twin-Blade Fencer | occupied | 7 kits / 4 games (Umbral Blades, Spectral Helix) |
| K27 Thorns Knight | self-identifying | 2 (Retaliation Warlord, Thorns Barbarian) |
| K10 Falconer | occupied (bow-coord; falcon axis abstained) | 2 (Bowazon, Ice Crystal Arrow) |
| K11 Trap Assassin | **self-identifying** | 1 (Trapsin) |
| K5 Ancestor-Warrior | thin | 1 (Emberquake Engineer — imperfect match) |

**Zero-match kits split two ways (BC-masked re-join, econ/elem slots dropped):**
- **Vocabulary-artifact zeros** — engine-native econ/elem vocab (`PB`/`VR`/`RS`) blocks the join; BC-only re-join recovers lineage: **H1 Guard Orbital → 6** (incl. *Ring of Shields / Interceptor* — its literal named lineage), **H5 True Battlemage → 67** (incl. *Battlemage*), **K20 Orbiter-Spiral → 34**, **K23 channel-class → 10** (incl. *Spin-to-Win / Cyclone / BvC* — exactly the channel-spin attractor). → Fix: element/econ-agnostic join mode in all views.
- **Genuine empty-coordinate claims (zero even BC-masked):** **K1 Heavy Barbarian** (low/spiky channel melee — corpus WW attractor is high/flat; **name-vs-coordinate disagreement**: folk-name claims D2 WW lineage, coordinates claim whitespace — either novel-by-design or coordinate drift, Mac-fill must rule), **K3 Polearm Soldier** (med/var melee), **K4 Thrown-Heavy/Atlatl** (STR-thrown slow-spiky), **K8 Crossbow Sniper** (slow-heavy shot — likely PoE2-post-cutoff territory, exactly the POST-CUTOFF LAW case).

**Legolas verdict: NO broad probe.** Lineage is computable from the join. Narrow Mode-A probe only for: (a) the 4 genuine-zero kits — verify real genre whitespace vs harvest gap (incl. PoE2 crossbow post-cutoff check for K8); (b) the corpus's own 26 verify-status representative rows if Matt wants them cleared before views.

## 4. Question D — housing

Three-layer answer, one law:
1. **Raw corpus → durable git home:** move/copy `ARPG-canonical-kit-research/` out of `claude-mobile-session-docs/` into `agentic_orchestration/research/arpg-canon-corpus/` (immutable harvest artifacts + run notes; provenance preserved).
2. **Queryable layer → elrond DB ingest:** JSONL → catalogue DB preserving per-axis {v,c,abstain}, negative twins, era stamps, per-slot key chars. CSV becomes a *derived view*, never the source of truth.
3. **Law layer → canonical doc:** `canon-harvest-pipeline-spec-v2.md` is engine-spec-grade; canonicalize (likely `canonical/reap-die-rise-engine/`) with a STATUS banner and RDR-integration addendum (join rules, measured-vs-projected law, scope flags).
**Overlay-at-render law:** corpus canon joins our gauntlet-measured archive only at render/view time — never merged into engine substrate tables.

## 5. Beyond A–D

- **The GX ledger IS the pause-2 mechanics roster.** Emission stays paused until Matt rules which GX families the engine adds. Leverage ranking belongs in the views (V3).
- **Mechanics-status distribution across 471 representatives:** have-core 181 · blocked-new 116 · partial 104 · verify 51 · designed-addendum 19. (Earlier run-notes' 71/7/60/59/26 figure was a subset snapshot; these are the measured v3 counts.)
- **Cross-links already live:** F5 cost-TYPE math ↔ GX-06 self-damage (convergent validation); Q15 Walls DEFER ↔ GX-18 barrier-terrain; GX-13 enemy-roster-as-arsenal validates the reap keystone from 10 games of genre evidence.
- **Corpus-embedded Matt ruling queue** (GX-02 hearing PAST DUE, GX-12/15/18–21 ratifications, Warlock attr, 8-element mapping, DL-01..04 design laws, grain table, mods tier) → land as batched `matt_decision_needed/` rows, not a dump.
- **PoE1 3.29 delta obligation:** corpus self-declares a re-harvest due ~2026-07-24.
- **Godot lens:** mechanics decisions need a *presentability* column (can drax's scene layer show this verb?) before any blocked-new mechanic is greenlit for engine build.

## 6. Views sketch (V1–V7) — for the classification follow-on

Target rubric per kit/coordinate: **CORE** (unique enough to build into pipeline) / **HYPOTHESIS-DISCOVERABLE** (combinable, found via gauntlet hypothesis testing) / **FLAVOR** (elemental/non-build-defining) / **REDUNDANT** (e.g., collapsing the 9 whirlwind-barb variants).

- **V1 Plane view** — both candidate planes (spec 15-cell vs mock 24-cell 8-family) with corpus ghost-dots + roster solids; the Q19 decision surface.
- **V2 Convergence ledger** — the 9 convergence groups + all cells ≥3 members (14 cells): where the genre re-derives the same kit = REDUNDANT candidates + validated-attractor CORE anchors.
- **V3 Mechanics-leverage board** — GX families × (games spanned, roster kits unblocked, engine cost, Godot presentability): the pause-2 decision surface.
- **V4 Roster adjacency map** — each of the 48 vs nearest corpus neighbors (wildcard + BC-masked joins): the C-question rendered.
- **V5 Flavor-collapse view** — same coordinate, element-only differences → FLAVOR classification (and 8-element mapping check).
- **V6 Era/longevity depth chart** — which coordinates persist across genre eras vs one-era fads.
- **V7 Negative-space map** — empty coordinates + negative twins: where the genre TRIED and failed vs never tried (K1/K3/K4/K8 live here).

## 7. Sign-off

Assessment delivered inline to Matt this session; this note is the durable record. Join computations reproducible from `final-docs-v3/rdr-kit-atlas-v3.csv` + `rdr-roster-kits.jsonl` (wildcard-compat + BC-masked scripts in session transcript). Tracker thirteenth delta + Q19 pause annotation committed alongside.

— gandalf, 2026-07-12
