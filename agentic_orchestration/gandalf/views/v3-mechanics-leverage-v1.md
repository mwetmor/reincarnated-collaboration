# V3 — Mechanics-Leverage Board v1 (the pause-2 decision surface)

> **Authored:** gandalf 2026-07-12 (spec §5 row 7 instrument; convening prep per Matt directive). **Decides at pause-2:** the GX add-list + build sequencing under the RULED §F.5(2) objective — *maximal coverage of the candidate pool* ("all mechanics if I can" is a directive, not a maybe). **This board ranks and sequences; Matt rules.**
>
> **Evidence layers merged:** Board 1 mechanics-gap counts (`engine-key/boards-v1.md`, certified mapping pass — engine-frame demand) · expansion census §2/§4 (`expansion-census-findings.md` — basin weights + games-spanned) · GX ledger (`canon-harvest-pipeline-spec-v2.md` §6/§9.1) · founding-roster/bench gates (serial tracker §F.3; roster CSV gate notes). Corpus `gx`-column vocabulary governs attestation counts; ledger names cross-referenced (nomenclature variance flagged where it matters).

---

## 1. The leverage table

Columns: **demand** = engine-frame kit count (Board 1, certified) · **games** = genre breadth (census §4) · **basin** = top unoccupied bc6 cells the mechanic gates (census §2 weight) · **unblocks** = roster/bench/mint rows freed · **engine cost** = gandalf-lean estimate by seam (KR/seam validation owed before dispatch) · **Godot** = presentability on drax's mannequin ladder.

| # | Mechanic (GX / gap) | Demand | Games | Basin gated | Unblocks | Engine cost (lean) | Godot | Risk notes |
|---|---|---|---|---|---|---|---|---|
| 1 | **Summon / proxy economy** — GX-19 (+GX-11 proxy-executes) · gap `SU` | **48** mechanics-demand (6 economy-core) | 15 | **IRMFHI w=325 (13 kits, 24yr) + IMMFHI w=184** — the genre's #1 unoccupied basin | K10 Falconer + K11 Trapsin (gates proxy-P0/P1/P2+E6 named on roster rows) · B11 inversion summoner · **all 9 mint kits** (2 HIGH: poe1-totem-hierophant, d3-cota) | **LARGE** — sim actor class + AI variants + summon economy (gamora); troop-command core EXISTS per K11 note; D3-archer-proxy nav gap (parks 38.9m) is a known sim defect to clear | **HIGH** — summons are visible actors; mannequin-ladder native | v2 spec made summoning a pillar (deferred-flag flip, §3.7); GX-19 ledger nuance: proxies that ABSORB commitment/cost ≠ proxies that deliver damage — spec both |
| 2 | **Reservation / aura** — GX-05 · gap `RS` | **42** | 18 | **WMHFSI aura-paladin w=144 (24yr)** | aura-keyed corpus kits; pairs with #1 (census: "summoner-and-aura wave closes coordinate AND mechanics coverage together") | **MEDIUM** — GX-05 partial (engine has reservation stubs); toggle-state + reserved-pool math (gamora econ) | MEDIUM — aura ring VFX; readable at B′ | PoE2 Spirit = genre's modern validation of reservation-as-core-resource |
| 3 | **Proc / trigger grammar** — GX-17 edge + GX-03 adjacency · gap `PC` | **45** | 12+ | cross-basin (procs ride any geometry) | poe1-coc/cwdt/autobomber cluster (15+ visible in Board 1 list) | **MEDIUM-LARGE** — event-hook bus partially exists (resolver already emits `on_lifesteal` etc.); trigger-condition grammar + loop-guard design | LOW-MED — event VFX only | **Genre warning:** automation edge is nerf-bait in every host game (CWDT loops, PoE2 0.4 CoC meta); design with engagement-axis guard from day one |
| 4 | **Mark-and-consume / combo** — GX-03 · gap `RC` | **18** | 11+ | combo grammar rides existing cells | gd-cadence, le-runic-invocation, VS arcana-cluster | **MEDIUM** — state-tag on target + consume-trigger (gamora); PoE2 MAINLINED this (bell, primed ailments) — strongest cross-game signal in the ledger | MED — primed-state glow + detonation | Timing-window economies (Tal/CoE) stay PARKED under GX-03 notes |
| 5 | **Ammo / consumable economy** — GX-14 · gap `AM` | **18** | 10 | econ-texture, cross-basin | pconc/wormblaster/grenade cluster | **SMALL-MED** — econ model + reload verb (gamora econ) | MED — quiver/flask props | PoE2 Concoction = named negative twin; don't port the failure |
| 6 | **On-kill resource-spawn (corpse/soul)** — GX-04 | (subset of PC/RC lists) | 14 | necro-economy texture | corpse-econ kits (di-corpse-explosion etc.) | **SMALL** — on-kill spawn hook + consumable ground-object (gamora) | HIGH — corpses ARE presentation | Reap-adjacent: RDR's keystone verb already lives here thematically |
| 7 | **Block-trigger** — gap `BT` (D2 ruling census) | **8** | 5+ | defense-texture | d2 block trio + smiter cluster | **SMALL** — trigger-rider on def layer (gamora resolver) | LOW | Physics split already ruled: 6 negate / 1 flat / 1 percent |
| 8 | **Harvest-radius economy** — watch-list | **6** | 3+ | VS/LE cluster | le-wraithlord, vs-magnet cluster | **SMALL** — pickup-radius as build stat | LOW-MED | **Watch-list promotion criterion FIRED** (parked at 2-3, promote at 4 — engine-frame count = 6) |
| 9 | **Kit-native leech channel** — Q23 residue · `partial:LC` | **12** rider + 3 econ | 8+ | sustain-texture | Blood Knight-class identity kits | **SMALL** — kit-level leech param (exists at gear/substrate; lift to kit grammar) | LOW | Q23 RULED rider; this is the build-side residue |
| 10 | **Orbit geometry** — GX-09 · `gx-candidate:orbit` | **4** | 4 | 25th rich-geometry type | poe1-poison-bv (GX-09 anchor), d3-bonestorm, d4-ball-lightning, d4-bouldercane · thaws B8 nested-orbit + B9 spiral-in + B10 detach-seek bench row context | **MEDIUM** — motion-frame orbital family partially built (B7-lite guard shipped); contact-on-rotation + uptime economy new | **HIGH** — orbiting props read instantly | Judgment-pass verdict: mechanically distinct from whirlwind AND circle; keying them elsewhere would bend kits (prime law) |
| 11 | **Walls / placed-lane** — GX-18 ⚑ · Q15 workstream | **3** | 3 | placed blocking/zone geometry | B4 re-spike rider (occlusion half); B7 full version (interception) sits behind it | **MEDIUM-LARGE** — nav-mesh interaction + occlusion (gamora sim + drax nav) | HIGH — walls are literal | Q15 named-workstream now has corpus demand evidence; GX-18 ratification owed |
| 12 | **Draft / pool-steering** — gap `DR` | **2** | 2 | run-convergence econ | vs-queen-sigma, hot-norseman | **DEFER-lean** — 2 kits; Tier-3 grain | LOW | Below any sensible leverage bar as mechanics-add; the *loot-operator* half already routes to agnostic-loot spec |

**Not on this board:** `UNKNOWN` econ census (44 rows — post-cutoff law; dossier backfill resolves, no build decision) · GX-16 party-external scaling (out-of-scope solo filter) · GX-13 reap/possession (RDR-native — our keystone, not a gap) · GX-01/02/03/06/07/09/10/11/17/20/21 occupied-by-founding portions.

## 2. The ailment-layer parallel track (NOT a GX — registry design work)

Board 3 makes the ailment backlog empirical. This is a **design-session track that runs parallel to any wave**, feeding `config/ailments.yaml` + the ailment-synergy design input (hades1-privileged-status routed there by the mapping pass):

| Ailment class | Corpus demand | Note |
|---|---|---|
| **damage-amp** | **97 kits (~21% of corpus)** *(errata: was 100 — see boards-v1.md ERRATA)* | The genre's single most-used missing mechanic (PoE shock, D4 vulnerable, curses). GX-15 multi-element cap collisions (18 games — widest precedent of ANY unoccupied mechanic) lands here too |
| freeze | 42 *(errata: was 43)* | escalation design already queued at ailment layer |
| stun | 36 | distinct from freeze (hit-reaction vs state-lock) |
| poison-dot | 36 | vs existing burn/bleed/drain — stacking identity needed |
| taunt | 11 | proxy-adjacent (pairs with wave #1 — pets taunt) |
| blind / curse-hex / fear | 8 / 4 / 4 | second-tier |

**Lean:** commission the ailment-layer design session (damage-amp + freeze + stun + poison-dot as the first tranche) as soon as pause-2 rules — it gates no wave and every wave benefits. Discipline #18: methodology consultation fires AFTER Board-3 baseline (this board IS the baseline — satisfied).

## 3. Wave-sequencing lean (gandalf; decision-shaped, Matt rules)

- **Wave A — Summoner/Proxy (#1) + its riders (#6 corpse-econ, taunt ailment).** The single largest unlock in every column: 48-kit demand, the genre's #1 basin, 2 roster gates, all 9 mint kits, §F.5(1)'s explicitly named missing corpus. Engine-largest too — start it first so the long pole starts early.
- **Wave B — Reservation/Aura (#2).** The census's own pairing ("closes coordinate AND mechanics coverage together"). Medium cost after Wave A's actor work.
- **Wave C — Trigger grammar (#3) + mark-consume (#4).** Second-biggest demand pair; carries the engagement-axis risk — design the guard rails INTO the spec, citing the genre's nerf history.
- **Small adds ride whichever wave touches their seam:** orbit (#10) + walls (#11) ride the geometry/motion-frame seam whenever rocket/gamora open it; BT (#7), HV (#8), leech (#9), AM (#5) are small gamora econ/resolver units — batch as a "texture wave" or attach opportunistically.
- **Ailment track (§2) runs parallel from day one.**
- **Defer:** DR (#12) as mechanics-add.

## 4. Convening agenda — what pause-2 needs from Matt

1. **Add-list ratification** (§1 rows 1–11: in/out per row; #12 defer-lean).
2. **Wave order** (§3 lean vs alternative: demand-order PC-first; or all-parallel if seam capacity allows).
3. **Growth-direction confirm** (census open item): the expansion field is caster/summoner/aura-shaped — is that the intended tilt, or do we counterweight toward martial texture the roster already holds?
4. **Ailment-layer commissioning** (§2 first tranche).
5. **GX hearings batch (ledger-owed, some PAST DUE):** GX-02 form-shift hearing (4 sightings, 3 games, no roster surface) · GX-12 stochastic-element ruling (exceeds element schema) · GX-15 ruling (element addendum) · GX-18/19/20/21 ratifications (⚑ provisional).
6. **Emission-gate restatement** (no decision — law check): pause-2 lifting ≠ emission; emission stays Matt-judged coverage per §F.4.

## 5. What pause-2 does NOT decide

Per-kit cell-duplication tiebreaks (§F.5(3), later, finest-resolution law) · demo-roster curation (§F.5(4), post-emission) · Q19 plane-lock (separate pause, renders after corpus integration — now unblocked by the ingest landing) · style/presentation registers (drax seam).

---

**Signed:** gandalf 2026-07-12. The board describes; Matt selects. Every row traces to certified counts — no leverage claim here floats free of the mapping pass.

---

## PAUSE-2 RULINGS LANDED (Matt, convening 2026-07-12) — THE BOARD IS RULED

1. **Add-list: ALL-IN as stated** — §1 rows 1–11 ratified into the engine buildout; #12 draft/pool-steering OUT as mechanics-add (loot half rides agnostic-loot spec).
2. **Wave order RULED = §3 lean verbatim:** Wave A summoner/proxy → Wave B reservation/aura → Wave C trigger+mark-consume; small adds ride open seams; ailments parallel.
3. **Growth-direction: tilt ACCEPTED** — expansion follows the genre's caster/summoner/aura demand; roster holds the martial texture.
4. **Ailment-layer design session: COMMISSIONED, fires in parallel** — first tranche damage-amp + freeze + stun + poison-dot (gandalf lean adopted); taunt rides Wave A; GX-15 folds in (see 5).
5. **GX hearings batch:**
   - **GX-02 form-shift: RATIFIED** — routes to the keystone (reap/possession) workstream, not an expansion wave.
   - **GX-12 stochastic element: PARKED + hypothesis registered as descriptor** — Matt verbatim: *"could this be produced naturally via element pipeline?"* Test when element-layer design next opens: stochastic assignment may fall out of cast-time element selection rather than needing schema surgery.
   - **GX-15 multi-element cap collisions: FOLDED into the ailment-layer damage-amp design** (item 4) — ailment-synergy question, not a standalone mechanic.
   - **GX-18 barrier-terrain: RATIFIED** (3-kit walls demand; Q15 workstream).
   - **GX-19 proxy cost-transfer: RATIFIED** — Wave A's spec nucleus; proxies that ABSORB commitment/cost specced distinctly from proxies that deliver damage.
   - **GX-20 default-attack-as-build: RATIFIED, routed to econ/commitment design** (not a wave).
   - **GX-21 sustained-stream-channel: RATIFIED + DL-03's lesson ADOPTED AS DESIGN LAW** — streams must not tax movement; the rooted-channel stillness killed the genre's stream archetype, never the stream itself (HoT = the controlled experiment). Binds all stream/beam kit authoring; lands in the commitment-grammar design surface.
6. **Emission-gate law restated, no decision:** pause-2 lifting authorizes MECHANICS BUILDOUT only; emission stays Matt-judged genre-canon coverage per §F.4.

**Execution fan-out from these rulings:** Wave-A summoner/proxy engine spec (gandalf SPEC-AUTHOR → KR sequences gamora/rocket dispatches) · ailment-layer design session (parallel, GX-15 folded) · GX-12 hypothesis note → element-layer design queue · DL-03 law → commitment-grammar surface · V1 plane view render on the verified corpus DB → Q19 plane-lock (the next pause).

**Signed:** gandalf, 2026-07-12 (rulings recorded verbatim-anchored; veto open on the record itself).
