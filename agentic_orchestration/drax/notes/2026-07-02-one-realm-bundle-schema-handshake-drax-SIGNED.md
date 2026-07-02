# One Realm — Demo Bundle Schema HANDSHAKE (drax → star-lord) — SIGNED

**Date:** 2026-07-02
**Author:** drax (consumer / Godot D4 loader)
**Counterparty:** star-lord (producer / emission assembly driver)
**Governs:** `reincarnated-engine/src/reincarnated/export/math/2026-07-02-one-realm-bundle-schema-note.md` (DRAFT-pending-drax-handshake)
**Authority:** Matt 2026-07-02 one-realm §5.1; D4 dispatch `2026-07-02-drax-godot-bundle-loader.md` scope item 1 (handshake = sign the schema)
**Status:** SIGNED — this document IS the lock signal. Per the schema note's lock condition, star-lord may now re-run assembly `--locked`, emit the sample bundle, and stamp MIGRATION.md v1.83 LOCKED.
**Home rationale:** authored in the collaboration repo (drax's authority) rather than co-located in `reincarnated-engine/` because engine is read-only to drax. Star-lord (engine owner) folds the LOCKED status back into the engine-side schema note when firing the lock-emit.

> **Read me as the answer to BOTH numberings.** The dispatch enumerates the open questions 1–5 (packaging / inline-vs-refs / null-handling / ProxyDecl SCAFFOLD acceptance / FloorManifest granularity). The schema note's lock condition enumerates the same decisions a–e (packaging / null-handling / ProxyDecl SCAFFOLD / FloorManifest granularity / no-III.7-violation). I answer by the schema note's Q1–Q5 numbering and cross-map to the a–e lock signal at the end.

---

## The principle governing every answer

**Loader ergonomics govern the format (dispatch §12), and the loader is a runtime JSON parser (see architecture decision below).** A GDScript runtime parser is *more* tolerant of a fat inline JSON manifest than of a fan-out of files or Godot-Resource refs. So my defaults align with star-lord's defaults — the simplest producer shape is also the simplest consumer shape here. I push back in exactly one place (null-handling, Q3), and I raise one schema ambiguity that must be resolved before lock (the gear-slot count, under Q3).

---

## Q1 — Single JSON vs. per-type files?

**ANSWER: SINGLE JSON. Confirmed. Do not split.**

Rationale (loader ergonomics):
- The Godot loader is a **runtime JSON parse** (`FileAccess.get_file_as_string` → `JSON.parse_string`), the exact pattern already proven in `scripts/render_arena_room.gd :_load_spec()` against `data/arena_scenarios.json`. One `parse_string` call, one `Dictionary` root, done.
- A single manifest means **one atomicity boundary**: the bundle is either wholly present and parsed or it isn't. Per-type files introduce partial-load failure modes (kits.json present, monsters.json missing) that force defensive existence-checks per file — brittle special-casing the dispatch tells me to push back on.
- The demo bundle is one realm's curated slice (~8–10 kits, 44 monsters, 200 gear). That is a small manifest; there is no size argument for splitting.
- **Provenance stays co-located:** `bundle_version` / `generated_at` / `engine_version` / `season_id` / `schema_status` at the top level are read once and apply to the whole payload. Splitting would either duplicate them or orphan them.

No adjustment requested. Single JSON with top-level keys per content type is the locked packaging.

## Q2 — Inline records vs. asset refs (Godot `.tres`)?

**ANSWER: INLINE JSON. Confirmed. Do not emit `.tres` refs.**

Rationale:
- Godot `.tres` Resource refs would make the **engine** responsible for authoring Godot-project-relative resource paths and Resource class layouts — coupling the emission pipeline to Godot's serialization format. That is exactly the cross-seam coupling the consumer-governs-format principle exists to prevent. The engine should emit **engine-truth data**; the loader converts to Godot runtime objects (Dictionaries → my own instancing) on the Godot side.
- Inline records let me instantiate kits/monsters/gear as **plain Dictionaries** and key Synty prefab selection off `archetype_tag` / `threat_tier` (the same tier→prefab map pattern already live in `render_arena_room.gd :PREFAB_BY_TIER`). No `.import` round-trip, no UID cache dependency, no per-record Resource file.
- If a future launch-scope pipeline wants a Godot-native import path, that is a separate optimization — **not** demo-critical, and not worth the coupling now.

No adjustment requested. All records stay inline.

## Q3 — Null handling for name / flavor_text?

**ANSWER: NULL IS ACCEPTED — DO NOT stub-fill at assembly time. The GDScript loader handles null gracefully. One condition + one ambiguity below.**

The loader treats null as first-class and falls back deterministically:
- **Kit:** `name` + `flavor_text` are populated (TRACK NEW) — no fallback needed.
- **Skill:** `name` populated; `flavor_text` null → UI simply omits the flavor line. The **skill NAME is what the §20d verb-realization test keys off** (name + geometry + range_m), so null skill flavor does not touch the playability predicate. Accepted.
- **Monster:** `name` null → display `"%s (%s)" % [archetype_tag, threat_tier]` (e.g. "brute (elite)"). `flavor_text` null → omit line.
- **Gear:** `name` null → display `"%s %s" % [rarity, gear_slot]` (e.g. "rare main_hand"). `flavor_text` null → omit line.

GDScript null-safety is trivial here: `.get(key, default)` + explicit `!= null` guards. **No crash risk. Do NOT pre-fill stub strings** — stub strings ("monster_00001") are *worse* than null because they render as if they were real names and defeat the fallback. Null is the honest signal; my loader owns the fallback. This keeps the demo-scope flavortext gap visible in the data rather than papered over.

**CONDITION (hard):** the null-vs-absent distinction must be **stable**. A field that is "sometimes null, sometimes absent from the record" forces me to write `.has(key) and rec[key] != null` everywhere. **Every field in every record shape must be PRESENT with an explicit `null` when it has no value — never omitted.** I want the guarantee so field-presence assertions in the round-trip smoke are meaningful (a missing field is a schema violation, not a null value). Confirm the assembly driver always writes the full key set per record.

**AMBIGUITY TO RESOLVE BEFORE LOCK (schema self-inconsistency, not a preference):** the schema note says `gear_representative` is an **"11-slot dict"** (KitRecord, note line 87) but the GearRecord note (line 259) locks the canonical vocabulary at **10 slots** (`main_hand / off_hand / head / chest / hands / feet / belt / ring_1 / ring_2 / amulet`). My loader iterates `gear_representative` slot-keyed; an 11th slot with no canonical name would be an unhandled key. **Resolve to 10** (the canonical Path-B SEAM-3 vocabulary) unless there is a real 11th slot, in which case name it in the schema so I can map it. I am building the loader against the **10-slot** vocabulary; flag if that is wrong before emit.

## Q4 — ProxyDecl SCAFFOLD magnitudes — Godot need non-scaffold values, or are placeholders OK for the D4 load test?

**ANSWER: SCAFFOLD PLACEHOLDERS ARE ACCEPTED for the D4 load test — with a mandatory boundary the loader enforces.**

- The D4 load/instantiate test proves the **summon VERB is wired** (a summoner kit's `proxies` payload resolves to N spawnable proxy entities with a targeting behavior and a lifecycle), NOT that the proxies are *balanced*. Balance is gamora-D3's calibration. So SCAFFOLD magnitudes are sufficient to instantiate and render the verb.
- **BOUNDARY (I enforce this loader-side, per D4 fold 3 + Discipline #9):** the four SCAFFOLD fields — `base_hp`, `damage_multiplier`, `attack_interval_s`, `proxy_max_active` — are **flagged SCAFFOLD in the loaded proxy object** and MUST NOT feed anything presented as a *tuned* number. My loader carries them behind a `scaffold: true` marker and gates any HUD/tuning surface on it. They drive placeholder instantiation only. When gamora-D3 lands calibrated magnitudes, the emitted bundle carries real numbers and the marker clears — no loader change needed.
- **CONDITION (this is the §20d trap, D4 fold 1):** the *load test* accepts SCAFFOLD magnitudes, but it does **NOT** accept an EMPTY proxies payload. The round-trip smoke asserts **≥1 kit with a non-empty `proxies` list** (D2's summoner decls injected). A `proxies: []` bundle would let the summon verb pass untested — I BLOCK the round-trip on that, not paper over it. SCAFFOLD-but-present = OK; empty = refutation.

So: SCAFFOLD values OK to *instantiate*; SCAFFOLD values NOT OK to *present as tuned*; EMPTY proxies NOT OK at all.

## Q5 — FloorManifest granularity (four floor_ids) sufficient, or need per-room / per-sub-floor?

**ANSWER: FOUR floor_ids are SUFFICIENT for D4. Confirmed. Do not add granularity now.**

- The four `floor_id`s (`structure_1 / biome_crossing / structure_2 / escape`) map 1:1 to the §23.1 three-beat descent + escape. The FloorManifest's job at D4 is to give the loader a **per-floor dominant_element** so monster/skill spawns rotate element per beat. Four entries deliver that.
- Per-room / per-sub-floor rotation is a **floor-authoring (D6) concern**, not a bundle-loader (D4) concern. D6 will consume the room-level procgen; if per-room element variation is wanted then, that is a D6 schema conversation, not a D4 blocker. Adding sub-floor entries now would be speculative granularity the loader can't yet use.
- The `notes` field (`"lieutenant floor"` / `"champion floor"`) is enough to let the loader tag the two boss beats. Sufficient.

No adjustment requested. Four-entry FloorManifest is locked.

---

## III.7 faction-invariant check (schema note lock condition (e))

**CONFIRMED — NO III.7 violation risk in the proposed FactionBlock shape.**

I reviewed every FactionBlock / FactionClusterRecord / FactionRelationshipRecord field. All are presentation-restyle only: `name`, `thematic_tags`, `visual_identity`, `faction_motif`, `faction_location`, `narrative_hook`, `member_kit_ids`, relationship `type` / narrative hooks. **None** carries a stat, damage-scaling, elemental affinity, or resistance field. My loader consumes FactionBlock as a **restyle map** (kit_id → visual/motif overlay) and applies it at the presentation layer *after* the kit's mechanical record is instantiated — faction can only recolor/relabel, never mutate a fight-model field. This is architecturally enforced on my side: the restyle pass has no write access to `stat_distribution`, `skills`, resistances, or any combat number. If a future faction field ever tries to bleed into combat, my loader surfaces it as an III.7 violation to star-lord (per the schema note's INVARIANT GUARD). Signed clean.

`PROVISIONAL_BLOCK_MARKER` handling: if the block is marked provisional, the loader treats faction as **preview-only restyle** (renders but flags as non-validated taxonomy) — never as validated content. Confirmed acceptable.

---

## The lock signal (a–e), signed

| Lock cond | Decision | Signed |
|---|---|---|
| (a) Packaging format confirmed | Single JSON, inline records (Q1 + Q2) | CONFIRMED |
| (b) Null-handling confirmed | Null accepted, loader-side fallback, NO stub-fill; **presence-of-all-keys guarantee requested** (Q3) | CONFIRMED (1 condition) |
| (c) ProxyDecl SCAFFOLD acceptance | SCAFFOLD placeholders OK to instantiate; loader flags them non-tuned; **non-empty proxies required for round-trip** (Q4) | CONFIRMED (1 condition) |
| (d) FloorManifest granularity | Four floor_ids sufficient (Q5) | CONFIRMED |
| (e) No III.7 violation risk | FactionBlock is restyle-only; loader enforces presentation-layer isolation | CONFIRMED |

**One pre-lock ambiguity to resolve (NOT a blocker to my sign, but resolve before emit):** the `gear_representative` **10-vs-11 slot** self-inconsistency in the schema note (Q3). I am building against 10. Confirm.

---

## What star-lord does next (per the schema note + dispatch)

1. Resolve the gear-slot count ambiguity (10 unless there's a real 11th slot to name).
2. Re-run assembly `--locked` with D2's landed summoner proxy decls injected (so ≥1 kit has non-empty `proxies` — NOT `proxies:[]`).
3. Emit the sample `one_realm_demo_bundle.json` with `schema_status: "LOCKED"`.
4. Stamp MIGRATION.md v1.83 `schema_status: LOCKED`; fold the LOCKED status into the engine-side schema note.

Until (2)+(3)+(4) land, drax builds the loader against the **locked schema SHAPE** (these signed answers) but does **NOT** run the round-trip smoke against a real bundle file (D4 fold 1 WAIT-for-lock guard). The round-trip closes when MIGRATION.md reads LOCKED **and** the emitted bundle carries ≥1 non-empty `proxies` payload.

**Signed:** drax, 2026-07-02. Loader ergonomics govern; the two conditions (all-keys-present guarantee, non-empty proxies) and the one ambiguity (gear-slot count) are the only pushbacks. Everything else: star-lord's defaults are the right defaults. Lock it.
