# Serial Content Emission — Endgame Map (the ending emission JSON + what's left)

**Author:** gandalf (`SPEC-AUTHOR` under `RUN-CONDUCTOR` authority), 2026-07-22 — answering Matt's
EXCHANGE-7 question (run ledger `2026-07-22-tier3-encounter-geometry-run-state.md`): *after this
autonomous run, what is left toward the complete serial content emission pipeline; what is the ending
emission JSON Drax builds everything from; do island families still need development + naming; are
there more engine mechanics; why did glance go stale.*

**Survey discipline:** every key below is marked — **LANDED** (exists on disk) · **RESIDUAL** (exists,
one pass owed) · **OWED** (designed, not built) · **GATED** (waiting on a named ruling/run).
Substrate: `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` (sixteenth
delta — assembler-landed reconciliation), `matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md`,
run ledger L-1…L-27.

---

## §1 The one-truth principle (unchanged, now load-bearing)

The engine is the product; **zero hand-authored shipped content**. Therefore the ending bundle is not
a hand-off document — it is the *serialization of the same canonical data the battle sim ran*. Drax
renders what the sim fought. Every content type below resolves to fields the sim already computes (or
will, at a named gate). VFX and Godot parity fall out of this principle rather than adding to it.

## §2 The ending bundle — skeleton (extends the LANDED assembler, not a new artifact)

`one_realm_bundle_assembler.py` (2,053 lines, 93 tests, landed 2026-07-02) already emits
`one_realm_demo_bundle.json` — 54 kits / 40 monsters / 150 gear / `proxies` / `stage2_run_record`.
The end state EXTENDS this spine:

```
one_realm_bundle.json  (end-state)
├─ meta                     LANDED   bundle_version · engine hash · stage2_run_record (provenance)
│                           OWED     + normalization_registry_version (VDM-2 §5 dual-column rule)
├─ player_kits[]            LANDED   kit spine, 648 skills, T4 discipline data, per-skill geometry
│   ├─ identity (LLM)       RESIDUAL flavor pass 0/648 — star-lord dispatch FIRED (~$1–3)
│   ├─ geometry bands       GATED    VDM-2 §4: delivery_class · width/range/speed bands ·
│   │                                pierce/chain/fork · count_multiplier · cadence_class ·
│   │                                motion_signature enum  → these are Drax's RENDER fields
│   ├─ door_args            GATED    VDM-2 §2 typed schemas (e.g. DUAL_PROXY: proxy_count,
│   │                                permanence, mirrored_skills, sync_mode, origin_model, targeting)
│   └─ numerics             GATED    VDM-2 §5 dual-column (source_value/rdr_value; sim reads rdr)
├─ monsters[]               LANDED   40 old-track; RESIDUAL flavor 0/40
│   └─ build_family key     OWED     organize by the 80-row census families + a families index block
│                           GATED    monster gen onto cycle-14 track (launch gap — demo ships old-track)
├─ bosses[]                 OWED     the L-26 three-layer stack, per boss:
│                                    rotation_spine (kit-compiled, authored competence)
│                                    reader_garnish_config (consideration set — THIS gate prices it)
│                                    legibility params (governor)
│                                    organized by build_family like monsters
├─ pinnacle_bosses[]        OWED     player-grade pipeline kits (full T4 + geometry) + LLM-named
│                                    skills (llm/naming.py layer is LIVE — same identity pass as
│                                    player kits) + the boss three-layer wrapper. Pinnacle = kit
│                                    reuse with boss dressing, NOT a new generator.
├─ gear[]                   LANDED   150-item pool wired (_load_gear_pool); RESIDUAL flavor 0/150
├─ islands[]                GATED    Q38 ruled the architecture (element-courts k=5 · eras=shelves ·
│                                    biome-morph rider); build-out L-6 FIREABLE but HELD on fork (b);
│                                    names = Q32 (Matt's ruling — deliberately not conductor-named)
├─ encounters[]             OWED     the reserved key (absent today): W1 MACRO/MESO/MICRO encounter
│                                    grammar · arena geometry (THIS run's Tier-3 substrate) · wave
│                                    compositions referencing monsters BY FAMILY
├─ proxies                  LANDED   D3 calibration ✓; launch dial: proxy share ~25%
├─ vfx_grammar              OWED     data-THIN by design (see §4) — mapping contract, not asset list
└─ reference_traces         OWED     sidecar, not bundle: golden semantic traces for Godot parity (§6)
```

## §3 Per-content-type detail (Matt's enumeration, in order)

1. **Player kits** — spine LANDED (demo run in flight: batch-1 700 martial kits done; summoner share
   0.000 → OPTION 1; batch-2 summoner leg gated on gen-path-pilot-leg3). What upgrades them to
   Drax-renderable: the VDM-2 field families (bands, door_args, dual-column numerics,
   recognition_hooks) — pinned by the VDM-2 pilot (4-kit cross-ontology) + freeze gates G1–G5.
2. **Enemy kits (bosses, by build family)** — OWED; L-26 architecture is ruled (one Reader
   architecture, three configs: player full / mob `{distance}` / boss spine+garnish+legibility). The
   aware-fighter ablation gate NOW IN FLIGHT is the pricing instrument for the garnish layer:
   PASS ⇒ awareness is a real difficulty dial worth boss-config budget; FAIL ⇒ honorable fallback,
   archive reads become garnish candidates, zero code debt. Boss build fires post-verdict.
3. **Pinnacle act enemy kits** — OWED but CHEAP: the pipeline already emits player-grade kits and the
   LLM naming layer is live. Pinnacle = generation-path selection + boss wrapper + naming pass. No
   new engine seam.
4. **Enemies (monsters, by build family)** — LANDED shape, two debts: `build_family` organization
   (census 80-row families as the key + index block) and cycle-14-track regeneration (launch).
5. **VFX** — see §4. No per-skill hand-authored effects, ever.
6. **Gear** — LANDED pool; flavor residual riding the FIRED star-lord wave; faction/weapon
   content-shape specs sit in D.2 launch scope.
7. **Dungeon rooms / biomes** — `islands[]` + `encounters[]` above; the encounter-geometry run
   currently under conduction IS the empirical substrate for arena/room geometry; grammar spec is W1.
8. **Godot real-combat rendering** — see §6.

## §4 VFX — the grammar position (design call, cheap by construction)

VFX must derive from the SAME canonical fields the sim fights with: **element** (palette + particle
vocabulary) × **geometry primitive + bands** (shape/scale/speed of the effect) × **cadence_class +
motion_signature** (animation timing) × **delivery_class** (projectile/beam/nova/zone framing). Drax
builds ONE mapping table in Godot — (element × primitive → particle/shader recipe) — and every skill,
monster, boss, and pinnacle effect renders from data. The bundle needs NO new keys beyond VDM-2's
band fields; what's owed is a short `vfx_grammar` contract doc (gandalf × drax design call) pinning
the mapping so both sides stop guessing. This is the zero-hand-authored principle doing work: 648
skills get VFX from ~dozens of recipes.

## §5 Engine mechanics still to build (Matt's "do we have more?") — YES, four + two residuals

**W2 verb-class unblocks** (routed L-12; Lane-2 spec §A7 — spec'd, unbuilt):
- **R-1 `ss_phase_transform`** — mid-fight entity mutation (blocks the SHAPESHIFT verb class; also
  boss phase-changes). Widened consult (R-1 + ECHO + boss-spine/kit→rotation) queued post-gate.
- **R-2 killable-spawner** · **R-3 projectile wall-reflection** · **R-4 native paired-emitter**.

**Residuals:** E4 STRIKER×ECHO needs the ECHO channel; F-f GEOMETRY is B4-scoped. (A1 bands ride #7.)

That is the whole engine-mechanics frontier. Everything else on the ladder is emission/organization/
presentation work, not new sim capability.

## §6 Godot parity — "render the real combat as modeled in the battle sim"

The instrument I propose (FORK — Matt rules later, flagged not chartered): a **golden-trace
conformance battery**. Engine emits semantic traces (tick · entity · intent · position · damage) for
a fixed reference-fight set; a Godot playback harness re-runs them and compares at the SEMANTIC level
— not bit-level (Python floats vs Godot physics cadence make bit parity a false god; semantic
equivalence is the honest bar). The prototype already exists in our hands: the BW-1 equivalence
battery (256/256 bit-equal within-engine) is the same instrument shape, one abstraction level up.
Sequence: drax bundle loader (one-realm §6.1) → VFX grammar call → parity battery design → then
"real combat in Godot" is a VERIFIED claim, not a vibe.

## §7 The ordered ladder (dependency order — what's left, top to bottom)

1. **This run:** ablation verdict (prereg PINNED L-27; jack-ryan check in flight → freeze → gamora
   execution charter → C2 seal → 512 fights → verdict).
2. **Boss stack build** (L-26; priced by #1) + widened R-1/ECHO/boss-spine consult.
3. **W2 mechanics R-1..R-4** + E4 ECHO channel + F-f (B4).
4. **Fork (b) ruling (MATT)** → island build-out fires (L-6 FIREABLE, HELD) → **Q32 names (MATT)**.
5. **VDM-2 pilot + G1–G5** → bands/door_args/numerics land in kit schema → mechanics-page axis-VALUES.
6. **D.1 residuals:** flavor wave (FIRED) · #7 batch-2 summoner leg (gen-path-pilot-leg3 gate).
7. **Monster gen → cycle-14 track** + build_family organization + `encounters[]` emission.
8. **Unified serial driver** (route-vs-replace PARKED) → trigger layer + web tracker (the
   CALLABLE ✓ → REGISTERED ✓ → TRIGGERED → SURFACED ladder's back half; post-demo by charter).
9. **Drax chain:** bundle loader → VFX grammar → golden-trace parity battery (fork).
10. **Glance refresh lane** (§8).

## §8 Glance — the staleness is real, and here is the honest accounting

/corpus went LIVE 2026-07-20 (574-kit VDM-1 corpus) — glance is not abandoned. The stale trio is
/coordinates + /mechanics + /atlas (v1.9), which pre-date the last week's runs. Cause: conduction
slots were consumed by the run cadence (Atlas Edition-I → VDM-1 → this chain) — a sequencing choice,
not a discontinuation. Two of the three pages are ALSO gated on Matt-side rulings by design: atlas
refresh sits under the F6 gate inside Q32 (repainting the atlas before island names/families lock
means painting twice), and /mechanics gains VDM-2 axis-VALUES only after the empirical taxonomy pass.
**Proposal:** charter a glance-refresh lane immediately post-run — /coordinates repaint from the
current corpus now; /atlas + /mechanics on their gates.

## §9 Matt's open levers (everything above that waits on YOU, in one place)

| Lever | Gates |
|---|---|
| Fork (b) — presentation-layer routing | island build-out (L-6) + emission venue architecture |
| Q32 — island names + F6 atlas-refresh | islands[] naming · atlas repaint |
| Golden-trace parity fork | the Godot "as modeled in sim" verification instrument |
| Route-vs-replace (unified driver) | D.2 serial driver shape (currently PARKED) |
| Story design session | keystone/narrative folds (your sequencing) |

**Signed:** gandalf, 2026-07-22. Ledger cross-ref: EXCHANGE-7. This note is the durable map; the
in-chat answer is its delivery.
