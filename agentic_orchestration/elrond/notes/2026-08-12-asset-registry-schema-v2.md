# Asset registry — schema spec v2

**STATUS: CURRENT** · Date 2026-08-12 · Author elrond (data steward) · Authority: REG-1..3 (Matt, 2026-08-12, "REG") · Design-only cell — no ingest run, no catalogue mutation, no code.
**Companion docs:** `agentic_orchestration/gandalf/notes/2026-08-12-q55-elicitation-and-gui-prep.md` § 2 (six GUI laws L1–L6, stage table) · `reincarnated-godot/catalogue/packs.json` (v1) · GOVERNANCE ADR-004.

---

## 0 · What the substrate actually says (read before judging the shape)

I surveyed the real store before designing. Eight findings; each one forces a field. **The schema below is a transcription of these facts, not a preference.**

| # | Finding (measured) | Requirement it forces |
|---|---|---|
| **S1** | `packs.json` v1 holds **48 pack rows** — ingest *config* (fbx_roots, skip rules, atlas). It contains **zero asset rows.** The 11,070 assets exist only as 19 × `<pack>/manifest.txt` (`name \t res://path`, 2 columns) and inside the 4.6 MB generated `index.html`. | v1 is a **pack registry**; v2 must add an **asset registry**. The two are different tables. Don't overwrite v1 — extend beside it. |
| **S2** | **1,764 asset names appear in more than one row, spanning 4,290 rows (39%).** e.g. `Characters`, `Capes`, `SM_Prop_Barrel_01`. Zero duplicate `res://` paths. | The ID **must** be pack-scoped. Bare name is not an identity. This is the empirical justification for `@asset:<pack>/<id>`, not an aesthetic one. |
| **S3** | `polygonmodularfantasyheroes` and `polygonmodularfantasyherocharacters` are the **same 776 assets** registered twice from two disk copies (`…-heroes/` vs `…-hero-characters/`). Name columns are byte-identical. | Need `duplicate_of` + a `superseded` state. Deleting the loser breaks the never-reuse rule and any `.tscn` already pointing at it. |
| **S4** | `fantasydungeon` (Matt's tab name) sources **POLYGON - Dungeon Realms**; `polygondungeonrealms` sits disabled as a separate row. `darkfantasy` and `polygondarkfantasy` point at the **identical** `fbx_root` with different skip/section configs. | **Three names must be separated:** registry `pack_id` (key) · `vendor_pack` (lineage) · `label` (display). v1 conflates all three. |
| **S5** | **29 of 48 packs disabled** (incl. `polygonwerewolf` — which SB-1 needs). `ingest_skips.log`: `INTERFACE- Fantasy Menus` → *"no FBX root with .fbx files found."* All 11,070 rows are `.fbx`; nothing else can be registered today. | `file_refs` must be a **typed list**, not an assumed FBX. A 2D/UI pack is not a failure — it's an asset kind the schema didn't have. Skips become **rows with a state**, not log lines. |
| **S6** | **Container FBX:** `SimplePeople3.fbx` is one row holding N characters. `polygon-fantasy-characters-pack` registers `Characters.fbx` **alongside** the 27 individual `SK_Character_*` rows it contains — with no relation recorded. | Need `is_container` + a `contains` / `part_of` relation. Otherwise the same character is counted twice and the palette shows both. |
| **S7** | **Thumbs: 11,007 on disk vs 11,070 rows — 63 missing**, concentrated (`polygonminifantasycharacters` −60, three packs −1). Two packs have no `failures.txt` at all; the rest are 0 bytes. | Thumbnail nullability is not hypothetical — it is **already the state**. Coverage gaps must be a queryable field, not an absent file. |
| **S8** | Section/class is **derived at HTML-build time** from filename grammar (`section_from: fbx_subdir \| prefix_token`) and stored **only in the generated view**. 9 sections summing to exactly 11,070. 369 `SK_*` rows leaked past the `skip_name_contains: ['SK_Chr_']` rule. | This *is* the staleness pathology REG-1 outlaws: the richest asset-level data lives downstream of the source. Class must be **stored with its derivation provenance**, upstream of the view. |

**The inventory's own class vote** (S8 — measured, not proposed): `Props 3444 · Buildings 2254 · Environment 1842 · Characters 1790 · Weapons 743 · Generic-shared-greybox 606 · Misc 283 · FX 61 · Vehicles 47`. Per REG-2, this is the seed enum — the inventory voted, I am transcribing. `Misc 283` is the honest residue and stays visible.

**Parts already exist:** 1,634 rows carry modular-slot grammar today — Synty `Chr_<Slot>_<Sex>_<NN>_Static` (776), Sidekick `SK_FANT_KNGT_17_10TORS_HU01` (slot codes TORS/AUPL/ALWL/HNDR/HIPS/LEGL/FOTR…), plus `FBX/Characters/Attachments/`. REG-2's `parts` stratum is not speculative; it is under-described existing inventory.

---

## 1 · Storage form (steward ruling)

**Source of truth = two newline-delimited JSON files under `reincarnated-godot/catalogue/registry/`.**

| file | rows | written by | nature |
|---|---|---|---|
| `registry/packs.v2.jsonl` | one per **source pack** (48 today) | hand + ingest | authored |
| `registry/assets.v2.jsonl` | one per **asset** (11,070 today) | ingest + deposit merge | authored |
| `registry/index.sqlite` | mirror | generator | **derived — never hand-edited** |
| `catalogue/index.html` | view | generator | **derived** |

Ruling and rationale: **JSONL, sorted by `id`, one row per line.** A single JSON array of 11,070 rows re-indents on every touch and produces unreviewable diffs; JSONL gives per-row git diffs, append-friendly deposits, and streaming reads. This is L3's discipline (composition stays diffable text) applied to the registry itself. The `godot-sqlite` addon is present and a SQLite mirror is the right *query* surface for the Godot dock at 11k rows — so it is **generated by the same pass that generates the HTML**, from the JSONL, and is `.gitignore`d. That preserves **L2 one-data-path**: one authored source, every other form derived. Any surface caught reading a hand-maintained list is in violation.

**Authored vs generated is a hard split** — this is the REG-1 lesson encoded structurally:

- **Authored** (in JSONL): `id, pack, stratum, class, class_source, lineage, files, state, is_container, contains, part_of, duplicate_of, tags, thumb_override, notes, source_date`.
- **Generated** (in the mirror + HTML only, recomputed every build, never written back): `used_by, thumb, thumb_present, section, subgroup, counts, class_inferred`.

A generated field that gets hand-edited is exactly how the HTML went stale. If it can be recomputed, it is not stored in the source.

---

## 2 · Entry shape — the asset row

```jsonc
{
  "id": "sm_prop_barrel_01",                    // slug, unique WITHIN pack. lowercase, [a-z0-9_]
  "pack": "darkfantasy",                        // registry pack_id — the namespace half of the token
  "token": "@asset:darkfantasy/sm_prop_barrel_01",   // generated convenience; canonical = pack + id
  "display_name": "SM_Prop_Barrel_01",          // vendor's original casing, preserved verbatim

  "stratum": "assemblies",                      // OPEN enum — see § 2.1
  "class": "props",                             // OPEN enum — see § 2.2
  "class_source": "prefix_token",               // how class was decided: prefix_token | fbx_subdir
                                                //   | vendor_declared | codex_pass | human
  "class_confidence": "high",                   // high | low | unclassified   (the Misc-283 honesty field)

  "lineage": [                                  // COMPOSABLE — a list, never a scalar. See § 2.3
    { "kind": "synty-pack",
      "vendor_pack": "POLYGON - Dark Fantasy",
      "vendor_sku": "synty-1624674",
      "acquired": "2026-06-21" }
  ],

  "files": [                                    // TYPED list — never assume .fbx (S5)
    { "role": "mesh",    "type": "fbx",  "path": "res://Assets/Synty/polygon-dark-fantasy/SourceFiles/FBX/Props/SM_Prop_Barrel_01.fbx" },
    { "role": "atlas",   "type": "png",  "path": "res://Assets/Synty/polygon-dark-fantasy/SourceFiles/Textures/Alts/PolygonDarkFantasy_Texture_01_A.png" }
  ],                                            // roles: mesh | scene | atlas | material | animation
                                                //        | texture2d | audio | particle | other

  "is_container": false,                        // S6 — one file holding many nameable assets
  "contains": [],                               // tokens of members, when is_container
  "part_of": null,                              // inverse: token of the container this was cut from
  "slot": null,                                 // parts-stratum only: "torso" | "arm_lower_l" | …

  "state": "present",                           // see § 2.4
  "duplicate_of": null,                         // token of the canonical row, when state=superseded
  "thumb_override": null,                       // null = use convention path (§ 2.5)

  "tags": [],                                   // FIELD DESIGNED NOW, POPULATED LATER (§ 2.6)
  "tags_source": null,
  "notes": null,

  "source": "ingest:drax/render_catalogue.gd@v1",   // required — every row traces to its origin
  "source_date": "2026-06-21",                      // required
  "schema_version": 2
}
```

### 2.1 · `stratum` — OPEN enum (REG-2)

Seed values, in composition order: **`parts` → `assemblies` → `completed`**.

- `parts` — a component that is not usable alone: modular limb/slot meshes, attachments, decomposed Unity-VFX fragments. (1,634 rows qualify today.)
- `assemblies` — a self-contained usable mesh/prop/module: the default for the Synty bulk.
- `completed` — a finished, dressed, run-ready artifact: a dressed room, a fully-kitted character, a rebuilt Godot VFX. SB-1's outputs land here (§ 4).

**Extension rule (this is the REG-2 mechanism, stated so nobody has to ask):** a new stratum value is admitted when **≥ 25 existing rows** would be reclassified into it *and* the proposer names the query the current strata cannot answer. Admission = a row in `registry/STRATA.md` (value · date · admitting evidence · reclassified count) plus a migration entry. Values are **never renamed and never deleted** — a retired value is marked `deprecated` with a `succeeded_by` pointer, because live `.tscn` files and prior receipts reference it. Refinements are voted by inventory; nobody imposes a taxonomy in advance.

Same extension rule governs `class` and `file.role`.

### 2.2 · `class` — OPEN enum, seeded from the inventory's own vote

`characters · props · buildings · environment · weapons · vehicles · fx · generic_greybox · misc`

Verbatim the 9 sections the current build derives, summing to exactly 11,070 — REG-2 says the inventory votes, so I transcribed rather than invented. Two known extension candidates the substrate already surfaces but the enum lacks: **`animation`** (29 rows named `Animations*` are clip files, not meshes, currently dumped in Misc) and **`ui_2d`** (the `INTERFACE- Fantasy Menus` skip, S5). Both are left unadmitted until the 25-row threshold is met by real ingest — which is exactly what drax's post-CP-A extension will do.

`class` is stored with `class_source` because the derivation is *fragile* (S8: the `SK_Chr_` skip rule leaked 369 `SK_Character_*` / `SK_FANT_*` rows). Recording *how* we decided lets a later pass re-decide only the low-confidence rows instead of re-deriving all 11,070.

### 2.3 · `lineage` — composable, always a list

An assembled asset has **multiple parents.** A scalar `source_type` column would be a lie the moment SB-1's werewolf lands (Synty base mesh + blender-decomposed parts + authored dressing). Seed `kind` values:

`synty-pack` · `unity-vendor` · `blender-decomp` · `authored` · `harvested-from-run`

Each entry carries its own provenance sub-fields (`vendor_pack`, `vendor_sku`, `acquired`, `derived_from` [token], `tool`, `run_id`). Reversibility (my standing principle): a `blender-decomp` entry **must** carry `derived_from` pointing at the row it was cut from, so the transformation is reproducible from raw input. No silent transformation — a decomposed part that cannot name its parent is a defect, not a row.

### 2.4 · `state` — completeness, not availability

| value | means |
|---|---|
| `present` | files exist on disk, ingest verified |
| `declared` | row exists, files not yet on disk (a disabled pack; a planned deposit) |
| `skipped` | ingest deliberately excluded it — collision proxies, Unreal skeletal dupes. **A row, with a `skip_reason`.** Not a log line (S5). |
| `superseded` | duplicate registration; `duplicate_of` names the canonical row (S3) |
| `missing` | previously present, files no longer found — a real event worth a row, never a deletion |

Rows are never removed. The registry is an archive; absence is expressed as state.

### 2.5 · `thumb` — convention + override, presence is generated

Default path is deterministic: `catalogue/<pack.out_dir>/thumbs/cat_<pack.thumb_prefix>_thumb_<display_name>.png`. The generator stat-checks it and writes `thumb_present: true|false` into the derived layer. `thumb_override` (authored, normally `null`) exists for galadriel's lane when she produces non-conventional thumbs — hero angles, multi-view. **The 63 known gaps (S7) become queryable the day v2 lands**, which is precisely the work-list handoff galadriel's stage needs.

### 2.6 · `tags` — design the field, not the pass

`tags: []` (flat string list) + `tags_source` (`codex-pass-<n>` | `human` | `vendor`) + optional `tags_date`. Discipline #14 spirit: **tagged, not encoded** — no semantic meaning packed into the id or the filename. Tags are additive and non-authoritative; nothing downstream may treat a tag as a required key. When the Codex classification pass runs, it appends `tags` and stamps `tags_source`; it must not touch `class`, which has its own provenance chain. An empty `tags` array is a valid, complete row.

---

## 3 · ID stability rules

1. **What makes an id:** `pack_id` + `slug`. The slug derives from the vendor's `display_name` (lowercased, non-alphanumerics → `_`), **not from the file path.** Paths move — S3 proved it, the same 776 assets living at two paths. Paths are attributes; identity is not.
2. **IDs are never reused.** A retired id is never reassigned to different content. Ever.
3. **Renames keep the id.** If the vendor renames a mesh, `display_name` changes, `id` does not; the prior name moves to `former_names: []`. If a *slug* would change, it doesn't — the id is frozen at first ingest.
4. **Cross-source collision is impossible by construction.** Two packs may both contain `characters`; `@asset:darkfantasy/characters` and `@asset:fantasydungeon/characters` are distinct tokens. This is what the 4,290 colliding rows (S2) buy us, and why the token is two-part rather than a global slug.
5. **Within-pack collision** (same basename in two subdirs) resolves by appending a disambiguator from the nearest distinguishing path segment: `capes` and `capes__attachments`. The row records `slug_disambiguated_from` with the original. **Never silently drop, never auto-number** — an opaque `_2` suffix teaches nobody anything a year later.
6. **Same content under two pack ids is not a collision — it is a duplicate registration.** One row is canonical (earliest `source_date`, ties broken by the enabled pack); the other keeps its id, takes `state: superseded` and `duplicate_of: <canonical token>`. The modular-hero pair (S3) is the founding case: 776 rows resolve this way. Both tokens continue to resolve, because a `.tscn` may already reference either.
7. **Pack ids follow the same rules** and are likewise never reused. `reincarnated*` is a **reserved prefix**, never assignable to a vendor pack.

---

## 4 · `@asset:` token grammar

```
token       := "@asset:" pack "/" id [ "#" fragment ]
pack        := slug
id          := slug
slug        := [a-z0-9] [a-z0-9_]*          ; lowercase, underscore, no dots, no slashes, no spaces
fragment    := [a-z0-9_]+                    ; addresses a member INSIDE a container (S6)
```

- Max length 128 chars total. Case-sensitive and always lowercase — a token differing only by case is malformed, not equivalent.
- No whitespace, no `/` beyond the single separator, no `..`. A token is not a path and must never be string-joined into one.
- **The token is the drag payload** (L1). Surfaces move this string and nothing else. Resolution — token → `files[]` → `res://` — happens once, at the resolver, in the receiving surface. The factory form, the chat surface, and the Godot dock all pass the same 40-odd bytes.
- **Fragment form** addresses container members: `@asset:polygonsimplepeople3/simplepeople3#business_male_01`. This is what lets a container row and its members coexist without double-counting.
- **Unresolvable tokens are an error, never a silent no-op.** A dropped token that resolves to nothing must surface as a validation failure — that is L5's machinery-disposes half.

### 4.1 · Namespacing for completed assets — ruling

**House pack id is `reincarnated`.** SB-1's outputs are `@asset:reincarnated/arena_ravine_dressed_01`, `@asset:reincarnated/werewolf_01`, `@asset:reincarnated/king_01`.

Rejected: `@asset:authored/<id>`. It looks natural and it is a false friend. `authored` is a **`lineage.kind` value**, and lineage is composable (§ 2.3) — the werewolf will carry `synty-pack` + `blender-decomp` + `authored` parents simultaneously. Using the same word as a pack namespace would assert a single-parent claim the data contradicts on day one, and would make "which authored assets are purely authored?" unanswerable. The pack namespace answers *who published this row*; the lineage list answers *what it is made of*. Different questions, different vocabularies.

`reincarnated` (with the reserved `reincarnated*` prefix, § 3.7) leaves room for `reincarnated_vfx` or per-line house packs later without re-namespacing anything already deposited.

---

## 5 · Deposit mechanism — how SB-1's outputs become the first `completed` rows

**Constraint that shapes this:** L5 (agent proposes, machinery disposes) and L2 (one data path). A cell must not hand-append to `assets.v2.jsonl` — concurrent cells would race the file, and hand-editing the source is precisely how v1's asset data ended up living in a generated artifact.

**Mechanism — fragment deposit + merge:**

1. The run cell that lands the artifact writes **one fragment file per asset**: `catalogue/registry/deposits/<run_id>/<pack>__<id>.json`, containing a single asset row. One file per asset means no write contention between cells, and a reviewable per-asset diff.
2. A **merge validator** (drax's ingest extension, Stage 0/1) runs at run close: validates required fields, checks id-uniqueness and never-reuse against the live registry, resolves every `lineage.derived_from` and `contains` token, then appends to `assets.v2.jsonl` in sorted position and moves the fragment to `deposits/<run_id>/merged/`.
3. The generator rebuilds `index.sqlite` + `index.html` **from v2** (§ 6). No hand-fed step exists anywhere in this chain.
4. A fragment that fails validation stays put and reports. **Merge is all-or-nothing per fragment** — a half-written row never enters the archive.

**Fields at deposit:**

| mandatory | may be null / defaulted |
|---|---|
| `id`, `pack` (= `reincarnated`), `display_name` | `tags` → `[]`, `tags_source` → `null` |
| `stratum` (= `completed`), `class` | `thumb_override` → `null` (galadriel's lane fills later) |
| `class_source` (= `human` or `vendor_declared`) | `notes`, `slot`, `part_of` |
| `lineage` — **≥ 1 entry, and every `blender-decomp`/`harvested-from-run` entry must resolve `derived_from`** | `contains` → `[]` unless `is_container` |
| `files` — ≥ 1 entry with `role: scene`, a real `res://` `.tscn` | `duplicate_of` → `null` |
| `state` (= `present`), `source`, `source_date`, `schema_version` | `class_confidence` → `high` for human-classified deposits |

`used_by` is **never** deposited. It is generated by scanning `.tscn` text for tokens and `res://` refs (L3 makes it derivable — placements are diffable data), so back-references cannot drift from reality. Hand-maintaining a back-ref column would reintroduce the exact failure mode REG-1 outlaws.

**SB-1's three concrete first rows:** the dressed arena → `completed`/`environment` with lineage `[{synty-pack: …}×N, {harvested-from-run: SB-1}]` and `files:[{role: scene, path: res://scenes/arena_room.tscn}]`; the werewolf and the king → `completed`/`characters`, each carrying its Synty parent packs plus the run. The werewolf's lineage will name `polygonwerewolf` — **currently a disabled pack (S5)**, which makes it a `declared`-state pack row that drax's extension must promote. That dependency is now visible in the data instead of living in someone's head.

---

## 6 · Migration — v1 → v2, no loss of 11,070 rows

**Nothing is deleted. v1 files stay in place until every consumer has moved.** (Versioned-and-readable, per my standing principle.)

| step | action | loss check |
|---|---|---|
| **M1** | `packs.json` (48 rows) → `registry/packs.v2.jsonl`. Every v1 key retained. `id`→`pack_id`; `label`→`label`; **new** `vendor_pack` + `vendor_sku` carrying the source-pack identity currently buried in `_note` prose (S4: `fantasydungeon` → *POLYGON - Dungeon Realms*). `enabled:false` → `state: declared`. `skip_name_contains`, `section_from`, `generic_section`, `family`, `wave`, `thumb_prefix`, `out_dir`, `primary_atlas`, `texture_dirs`, `materiallists` all survive verbatim as an `ingest` sub-object. | 48 in → 48 out |
| **M2** | 19 × `manifest.txt` (11,070 rows) → `registry/assets.v2.jsonl`. `col1`→`display_name`, slugified→`id`; `col2`→`files[0]{role:mesh,type:fbx}`; dir→`pack`. `source: "manifest:<pack>@2026-06-21"`, `source_date: 2026-06-21`. | **11,070 in → 11,070 out. Exact. This is the migration's acceptance test.** |
| **M3** | Lift the derived section from `index.html` into `class` + `class_source` (`fbx_subdir` \| `prefix_token`), per the 9-value vote. The 283 `Misc` rows get `class: misc`, `class_confidence: unclassified` — the residue stays visible rather than being quietly bucketed. | 9 sections, sum = 11,070 |
| **M4** | Mark strata: the 1,634 modular/attachment rows → `parts` (with `slot` where the grammar yields it); remainder → `assemblies`. No row is `completed` until SB-1 deposits. | 1,634 + 9,436 = 11,070 |
| **M5** | Reconcile duplicates: the 776 `polygonmodularfantasyherocharacters` rows → `state: superseded`, `duplicate_of` → the `polygonmodularfantasyheroes` twin. Flag `darkfantasy`/`polygondarkfantasy` (identical `fbx_root`, S4) for a pack-level duplicate ruling — see Q3. | rows retained, none dropped |
| **M6** | Stat-check thumbs → `thumb_present`. The 63 gaps become a queryable work-list for galadriel's stage. `ingest_skips.log` → `state: skipped` rows with `skip_reason`. | 11,007 present / 63 absent |
| **M7** | **The HTML generator's input changes from `packs.json` + `manifest.txt` to `assets.v2.jsonl`.** From this point the catalogue HTML is a *generated view* of v2 and of nothing else (REG-1). `manifest.txt` becomes a build artifact of the ingest, no longer an input to anything. | one data path (L2) |

**Acceptance:** a diff of `{name, path}` pairs extracted from v2 against the 19 v1 manifests must be **empty in both directions**, and the regenerated HTML must still report 11,070 with the same 9 section counts. Any other outcome is a failed migration, not a new baseline.

**Not in this migration:** admitting `animation`/`ui_2d` classes, ingesting the 29 disabled packs, Unity-vendor VFX decomposition, thumbnails. Those are drax's post-CP-A and galadriel's stages per REG-3's staggered chain. v2's job is to make them additive rather than restructuring.

---

## 7 · Open questions — Matt / gandalf (5, each decision-shaped)

**Q-R1 · Container rows: keep, fragment, or both?** S6 — `Characters.fbx` is registered alongside the 27 `SK_Character_*` rows it contains; `SimplePeople3.fbx` is one row holding N characters that have no rows at all. (a) Keep containers as rows, add `contains`, let the palette hide them by default. (b) Fragment containers into member rows at ingest, retire the container. (c) Both — container row plus member rows linked by `part_of`/`#fragment`. **Lean (c):** it's the only option that doesn't lose information in either direction, and the `#fragment` token grammar already supports it. Cost: ingest must open FBX and enumerate meshes, which is a real drax cost — hence a question, not a ruling.

**Q-R2 · Does `parts` mean "modular slot piece" or "any non-standalone fragment"?** The 1,634 rows split into modular character slots (clean vocabulary: torso/arm/hips) and attachments (capes, back-props — arguably standalone). (a) Narrow: `parts` = slot-addressable only; attachments are `assemblies`. (b) Broad: anything not usable alone. **Lean (a)** — narrow keeps `slot` meaningful and non-null across the whole stratum, which is what makes an assembly UI possible. Broad makes `slot` mostly null, i.e. a stratum that can't be queried. Flag: this decides whether blender-decomposed Unity VFX fragments are `parts` (narrow says no — they'd need a new stratum, and REG-2's 25-row rule would admit one).

**Q-R3 · `darkfantasy` vs `polygondarkfantasy` — same `fbx_root`, two configs (S4).** (a) Retire the disabled twin as `superseded`. (b) Keep both as distinct *ingest profiles* over one asset set. (c) Merge configs into one pack row. **Lean (a)** — the disabled row exists because sectioning was being tuned, not because there are two packs; two pack ids over identical files will eventually produce two tokens for one mesh, which § 3.4's guarantee cannot save us from. Needs drax's confirmation that nothing references the disabled id.

**Q-R4 · Who owns `registry/`?** It lives in `reincarnated-godot/` (drax's seam) but is a data layer (mine), and three surfaces will read it. (a) drax owns the files, I own the schema — changes route ADR-004. (b) I own `registry/`, drax owns ingest that writes through it. (c) Co-owned with a schema-change veto to me. **Lean (a):** it matches the star-lord telemetry precedent exactly — the seam owner owns the store, the steward owns the shape, and cross-seam changes travel through `MIGRATION.md`. Wants an explicit word because it establishes a second cross-seam data boundary.

**Q-R5 · Is `class` one axis or two?** The 9-value vote mixes *what a thing is* (character, weapon) with *where it came from in the pack layout* (`generic_greybox` — 606 rows, meaning "shared across Synty dungeon packs", not a kind of object). (a) Ship the 9 as-is; the inventory voted. (b) Split into `class` (kind) + `provenance_role` (greybox/shared/showcase), moving the 606. **Lean (a) for v2, revisit after the Codex tag pass** — REG-2 says refinements are voted by inventory, and the tag pass is the vote. Splitting now would impose an axis on 11,070 rows on the strength of one 606-row smell. Noting it so the smell is on record rather than rediscovered.

---

*Design-only cell. No ingest was run, no catalogue file was mutated, no code was written. Substrate figures in § 0 are measured from `reincarnated-godot/catalogue/` at 2026-08-12 and are reproducible by re-reading `packs.json`, the 19 `manifest.txt` files, and `index.html`.*
