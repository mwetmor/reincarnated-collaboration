-- =====================================================================
-- VDM-2 DATA RIDERS + REGISTRY SEEDS — REVIEWABLE ARTIFACT — *** NOT RUN ***
-- =====================================================================
-- Author:  elrond (data steward) · Wave W3a · VDM-2 -> Edition-next lap
-- Package: 2026-07-22-vdm2-w3a-migration-package.md
-- Runs:    IN W3b, AFTER DDL v1, BEFORE the v2.0 stamp. Requires
--          PRAGMA foreign_keys=ON already set by the apply script.
-- Target:  corpus.db @ (post-DDL-v1) -- NOT applied this wave.
-- Scope:   the CHEAP census derivations only (corpus_class / court / eras_
--          normalized / original_element / atlas_coords). capstone_source_
--          acquisition + all side-car tables (door args, deviations, bands,
--          numerics, hooks, acceptance) populate at W4 re-emission, NOT here.
-- Law:     source-anchored + reversible + no silent transformation. Every
--          derivation preserves its raw source column (elem_raw / eras /
--          cell_key are never dropped). All riders are idempotent (re-run =
--          overwrite-to-same). Syntax-validated on a THROWAWAY COPY only.
-- =====================================================================


-- #####################################################################
-- ## RIDER 1 -- corpus_class  (V-14 + A-6 census)  [record|annex|system]
-- #####################################################################
-- V-14: 3-enum {record, annex, system}. system = ALL is_system=1 (=19, A-6).
--       NULL means 'unclassified' only (reserved), NEVER 'system'.
-- Expected post-rider census over 585 (the A-6 tally that closes the count):
--   system  = 19   (every is_system=1: 11 unmapped + 8 mapped)
--   record  = 267  (is_system=0 AND corpus_bucket IN the 5 record games)
--   annex   = 299  (is_system=0 AND corpus_bucket IN the other 12 games)
--   267 + 299 + 19 = 585   [cross-check: 267+299+8-mapped-system = 574 kit_master]

-- 1a. system FIRST (so it wins on any overlap; is_system is the authority).
UPDATE canon_corpus
   SET corpus_class = 'system'
 WHERE is_system = 1;

-- 1b. record: real kits in the five record games.
UPDATE canon_corpus
   SET corpus_class = 'record'
 WHERE is_system = 0
   AND corpus_bucket IN ('poe1','d2','gd','poe2','le');

-- 1c. annex: real kits in every other game.
UPDATE canon_corpus
   SET corpus_class = 'annex'
 WHERE is_system = 0
   AND corpus_bucket NOT IN ('poe1','d2','gd','poe2','le');

-- 1d. VERIFY (the apply script asserts these three counts before proceeding):
--   SELECT corpus_class, COUNT(*) FROM canon_corpus GROUP BY corpus_class;
--     -- MUST be: record 267 | annex 299 | system 19 | (NULL 0)


-- #####################################################################
-- ## RIDER 2 -- original_element  (H3 promotion of elem_raw)
-- #####################################################################
-- Total promotion on record-270 (elem_raw 270/270 non-NULL, verified). Runs
-- over the whole 585 for completeness (annex/system elem_raw promote too where
-- present; where elem_raw is NULL, original_element stays NULL -- honest).
-- elem_raw is NEVER dropped (reversible; original_element is the promotion).
UPDATE canon_corpus
   SET original_element = elem_raw
 WHERE elem_raw IS NOT NULL AND TRIM(elem_raw) <> '';


-- #####################################################################
-- ## RIDER 3 -- court  (V-15, Q38 k=5, DERIVED from elem_raw; MUTABLE data)
-- #####################################################################
-- V-15 mapping (WITHIN Q38's ruled k=5 frame -- k is NOT changed):
--   fire                                              -> fire
--   cold                                              -> cold
--   lightning, aether                                 -> lightning   (V-15: aether = GD energy/lightning conversion lane)
--   physical, physical?, pierce, bleed                -> physical     (physical? via ?-suffix base rule; pierce/bleed = physical-family sub-tokens*)
--   chaos, poison, acid, necrotic, vitality, void, void? -> chaos-poison (V-15 decay court + ?-suffix base rule for void?)
--   magic, n/a, mixed(...), physical/chaos, shadow?, shadow/blood? -> HONEST NULL
--
-- *pierce/bleed rider extension (documented, NOT silent): V-15 named the decay
--  set + the ?-suffix rule but did not enumerate 'pierce'/'bleed'. Both are
--  physical-damage sub-tokens in every record-game taxonomy (bleed = physical
--  DoT; pierce = physical weapon damage). Assigning them to the physical court
--  is WITHIN k=5 and consistent with V-15's spirit; it is flagged here as an
--  extension for the reviewer, not an invention. If the reviewer prefers these
--  NULL, delete the two tokens from the physical WHEN-clause below (coverage
--  drops 257->253; the 4 rows join the NULL list).
--
-- V-18 coupling: runs on CURRENT (frozen-at-apply) elem_raw. W5 elem_raw
-- corrections (the ~6-8 flagged PoE1 anomalies) trigger a bounded court
-- re-derivation on affected rows LATER (court is mutable; W5 precedes Leg-B).
-- Do NOT block W3 on the anomalies.
--
-- Runs over the RECORD BUCKET (270) -- court is a record-kit derivation. (Annex
-- court is out of scope for Leg A; the column stays NULL for annex/system.)
--
-- Expected coverage: 257/270 courted (95.2%), 13 honest-NULL.
--   physical 90 · fire 54 · chaos-poison 44 · lightning 42 · cold 27 · NULL 13

UPDATE canon_corpus
   SET court = CASE
     WHEN elem_raw IN ('fire')                                   THEN 'fire'
     WHEN elem_raw IN ('cold')                                   THEN 'cold'
     WHEN elem_raw IN ('lightning','aether')                     THEN 'lightning'
     WHEN elem_raw IN ('physical','physical?','pierce','bleed')  THEN 'physical'
     WHEN elem_raw IN ('chaos','poison','acid','necrotic',
                       'vitality','void','void?')                THEN 'chaos-poison'
     ELSE NULL   -- magic, n/a, mixed(...), physical/chaos, shadow?, shadow/blood? -> honest NULL (V-15)
   END
 WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le');

-- 3b. VERIFY (apply script asserts):
--   SELECT court, COUNT(*) FROM canon_corpus
--     WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') GROUP BY court;
--     -- MUST be: physical 90 | fire 54 | chaos-poison 44 | lightning 42 | cold 27 | NULL 13
--
-- The 13 NULL-court record rows (the honest-NULL list; V-15 magic/n/a/mixed +
-- the 3 genuinely-ambiguous multi/shadow tokens the ruling did not reach):
--   magic(4):           d2-berserker, d2-bonemancer, d2-hammerdin, d2-wl-abyss
--   n/a(5):             d2-teleport-sorc, le-low-life-ward, poe1-aurabot,
--                       poe2-grim-feast, poe2-temporalis-blink
--   mixed(1):           gd-panettis-mage-hunter        (mixed(fire/cold/lightning))
--   physical/chaos(1):  poe1-blood-magic-kit           (genuine dual-court)
--   shadow(2):          d2-wl-tainted-summoner (shadow?), d2-wl-blood-boil (shadow/blood?)
-- All 13 are Leg-B per-kit-resolution candidates (V-15: forcing a court =
-- pre-imposed taxonomy; per-kit resolution is a Leg-B beat candidate).


-- #####################################################################
-- ## RIDER 4 -- atlas_coords  (H5 promotion/denorm of cell_key)
-- #####################################################################
-- Promote canon_engine_key.cell_key -> canon_corpus.atlas_coords so pinnacle
-- synthesis + season mutation read coords without an atlas join. 268/270 on
-- record; 2 honest NULL (poe1-blood-magic-kit, d2-teleport-sorc lack cell_key).
-- cell_key is the source of truth (reversible). Runs over the record bucket.
UPDATE canon_corpus
   SET atlas_coords = (
         SELECT ek.cell_key FROM canon_engine_key ek WHERE ek.kit_id = canon_corpus.kit_id
       )
 WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le')
   AND EXISTS (
         SELECT 1 FROM canon_engine_key ek
          WHERE ek.kit_id = canon_corpus.kit_id
            AND ek.cell_key IS NOT NULL AND TRIM(ek.cell_key) <> ''
       );
-- 4b. VERIFY: 268 non-NULL atlas_coords on the record bucket; the 2 NULL are
--     poe1-blood-magic-kit + d2-teleport-sorc (honest -- they have no cell_key).


-- #####################################################################
-- ## RIDER 5 -- eras_normalized  (V-16 option (c): per-game canonical tokens)
-- #####################################################################
-- V-16: fixed lowercase era-token vocabulary PER GAME, documented in
-- MIGRATION.md. NO cross-game ordinal in the column (shelves derive at Leg-B
-- per Q38 eras=shelves). The 'normalization' here is: re-emit the raw
-- semicolon-shorthand as the SAME token list, VALIDATED against the per-game
-- canonical vocabulary (below). Because the raw tokens ALREADY are the
-- canonical per-game vocabulary (verified -- no cross-game collapse is applied),
-- the normalized value == the raw value for the record games. The column
-- carries the validated per-game token list; the vocabulary is the contract.
--
-- This rider is a straight copy WITH a validation contract (the per-game
-- vocabularies are documented in MIGRATION.md; any raw token outside its game's
-- vocabulary is an INGEST error to catch at W4/W5, not silently normalize).
-- Raw 'eras' is preserved (reversible).
--
-- PER-GAME CANONICAL ERA-TOKEN VOCABULARIES (the V-16 contract; full lists in
-- MIGRATION.md draft):
--   poe1: 1.x · 2.x · 3.0-3.6 · 3.2-3.6 · 3.4-3.6 · 3.5-3.6 · 3.7-3.13 ·
--         3.8-3.13 · 3.11-3.13 · 3.12-3.13 · 3.14-3.19 · 3.15-3.19 ·
--         3.16-3.19 · 3.19 · 3.20+                                   (15 tokens)
--   d2:   classic · lod · lod-1.09 · lod-1.09+ · lod-1.10+ · lod-1.11+ ·
--         lod-infinity+ · lod-pvp · d2r · d2r-2.4+ · d2r-2.6+ · d2r-pvp ·
--         rotw · rotw-s13 · rotw-s13+ · rotw-s14                     (16 tokens)
--   gd:   base-2016 · aom-2017 · fg-2019 · patch-1.1-1.2 · foa-pending (5 tokens)
--   poe2: 0.1 · 0.2-dawn · 0.3-edict · 0.4 · 0.5-ancients            (5 tokens)
--   le:   beta-0.8-0.9 · 1.0-launch · 1.1-harbingers · 1.2-woven · 1.4-omens (5 tokens)
--
UPDATE canon_corpus
   SET eras_normalized = eras
 WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le')
   AND eras IS NOT NULL AND TRIM(eras) <> '';
-- 5b. NOTE: 2 poe1 rows have NULL eras (verified) -> eras_normalized stays
--     NULL for them (honest). The copy is validated-against-vocabulary, not a
--     blind copy: W4/W5 QA lints any token not in its game's vocabulary above.


-- #####################################################################
-- ## RIDER 6 -- GX-02 census-tail 3 kits  (V-6: V13 99.47% -> 100% path)
-- #####################################################################
-- V-6: the 3 GX-02 census-tail kits (gd-berserker-wereforms + 2 LA Wildsouls:
--      la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul) fold into
--      the W3 DATA pass -> the V13 100% expressible-now completion path.
--
-- IMPORTANT SCOPE DISCIPLINE (steward call): the "V13 100%" completion is a
-- census-EXPRESSIBILITY metric (does the GX-02 shapeshift LAYER express these
-- kits), which is fundamentally ENGINE-side (the GX-02 docket-to-spec is a
-- SEPARATE gandalf-sub-agent lane; ESC-1 / the kit_architecture enum is
-- explicitly NOT conductor-ruled and NOT this lap, per V-17-c). Therefore this
-- rider does NOT write any shapeshift 'architecture' value -- the canon_corpus.
-- architecture column stays as-is (empty across all 585; it is rocket/Matt's
-- enum at Gate-1, not the catalogue's to fill in this lap).
--
-- What this rider DOES (and all it should do): these 3 kits are RECORD-adjacent
-- catalogue rows and get the SAME cheap census columns as every other row of
-- their class via Riders 1-5 above. Their census-tail status is that they are
-- PRESENT + CLASSIFIED in the re-emission, which is the "fold into the data
-- pass" the V-6 ruling asks for. No extra write is authored here; this block
-- is the EXPLICIT NO-OP-BEYOND-RIDERS-1-5 note so the reviewer sees the
-- discipline (assemble-not-invent; do not reach into engine enum territory).
--
--   gd-berserker-wereforms  : corpus_bucket=gd -> corpus_class already 'record'
--                             via Rider 1b; court from elem_raw via Rider 3;
--                             atlas/eras/original_element via Riders 2/4/5.
--                             (GX-02-tagged, GAPPED/MAPPED_DOCKET; t4_doors=[]
--                             -> its shapeshift-gap is a W4b engine-spec item,
--                             NOT a court/census gap.)
--   la-ferality-wildsoul    : corpus_bucket=la -> corpus_class 'annex' via
--   la-phantom-beast-...    : Rider 1c (LA is an annex game). Their GX-02
--                             census-expressibility is engine-spec (W4b), not a
--                             catalogue write. (Both carry unresolved=1 +
--                             dossier_owed=1; those flags are W4/W5 re-emission
--                             + dossier work, out of this cheap-census scope.)
-- No SQL beyond Riders 1-5. This block is documentation of the correct null-op.


-- #####################################################################
-- ## SEED A -- door catalogue + trigger-door arg schema  (A-2 realized)
-- #####################################################################
-- These are REGISTRY seeds, NOT per-kit data. They land the door_registry rows
-- + the A-2 trigger-door arg declarations. Ordered so door_registry precedes
-- door_arg_schema (FK dependency under foreign_keys=ON). Idempotent.
--
-- SCOPE: this seed lands ONLY the doors + args the W2 pilot ATTESTED (the seed,
-- not the closure). The full 28-door catalogue + each door's arg surface is W4
-- re-emission work (per-game tranches). Landing the pilot-attested subset now
-- keeps A-2 concrete and gives the reviewer a runnable example; W4 grows it.
--
-- Doors attested in the W2 pilot: DUAL_PROXY, PERSISTENCE_ENGINE_uptime,
-- PROXY_ASCENSION, ELEMENTAL_ECHO, GEOMETRY_COLLAPSE, ELEMENT_CONVERSION_MONO.

INSERT OR IGNORE INTO door_registry(door_name, door_status, description) VALUES
  ('DUAL_PROXY','active','Spawns proxy clones that mirror the caster''s skills from their own spatial origins.'),
  ('PERSISTENCE_ENGINE_uptime','active','Sustains a defensive/utility effect while a resource/summon is active.'),
  ('PROXY_ASCENSION','active','Places autonomous emitter proxies (totem lane) that act on their own.'),
  ('ELEMENTAL_ECHO','active','Trigger-family door: a host action triggers a payload skill (e.g. Cast-on-Crit).'),
  ('GEOMETRY_COLLAPSE','active','Collapses delivery geometry (e.g. shotgun-density / burst-around-self).'),
  ('ELEMENT_CONVERSION_MONO','active','Converts a skill''s damage to a single target element.');

-- A-2: the three trigger-door args (int / enum / real). arg_type 'real' is the
-- A-4 addition; cadence_scale is a raw 0..1 fraction, NOT a percent.
INSERT OR IGNORE INTO door_arg_schema(door_name, arg_name, arg_type, enum_values, default_value, notes) VALUES
  ('ELEMENTAL_ECHO','trigger_condition','enum','["on_crit","on_hit","on_kill","on_cast"]','on_crit',
     'A-2: the event that fires the triggered payload (CoC Ice Nova = on_crit).'),
  ('ELEMENTAL_ECHO','parallel_triggers','int',NULL,'1',
     'A-2: count of parallel trigger sources; Cospri''s Malice second on-crit trigger => 2.'),
  ('ELEMENTAL_ECHO','cadence_scale','real',NULL,'1.0',
     'A-2/A-4: raw 0..1 fraction (CoC 14%-CDR breakpoint => 0.75); a real, not a pct.');

-- (Additional pilot-attested door args -- DUAL_PROXY proxy_count/origin_model/
--  sync_mode etc., PROXY_ASCENSION max_active, GEOMETRY_COLLAPSE collapse_mode,
--  ELEMENT_CONVERSION_MONO target_element -- are documented in the pilot report
--  §3 and land at W4 alongside their kit_door_arg bindings. A-2 specifically
--  names the trigger-door args as the DDL-v1 registry addition; those are the
--  three seeded here. The rest ride the W4 per-game door-arg emission.)


-- #####################################################################
-- ## SEED B -- motion_signature_registry  (A-3 realized: fan_spread)
-- #####################################################################
-- Land the v0 seed paths + the A-3 fan_spread addition. Idempotent.
INSERT OR IGNORE INTO motion_signature_registry(signature_name, description) VALUES
  ('straight_line','Projectile travels a straight vector from origin.'),
  ('spiral_out','Projectile spirals outward from origin.'),
  ('orbit_fixed','Effect orbits a fixed point (player or anchor).'),
  ('sine','Projectile follows a sinusoidal path.'),
  ('mortar_arc','Projectile lobs on a ballistic arc to a target point.'),
  ('wall_sweep','Effect sweeps as a wall/line across an area.'),
  ('fan_spread','A-3: radial fan / sector spray (e.g. GD Stun Jacks 180-degree point-blank spread).');


-- #####################################################################
-- ## A-7 -- DOOR-STRIP RIDER BEHAVIOR  (preserve NULL t4_doors)
-- #####################################################################
-- A-7 is a RIDER-BEHAVIOR guarantee, NOT a write. The migration plan (V-11)
-- said "8 empty-string door slots -> W3 rider strips (raws preserved)." The
-- W2 pilot CORRECTED this: the 8 are kits whose t4_doors ARRAY IS NULL (not
-- empty-string slots), all D2, and 7/8 are MEANINGFUL (NULL <-> GAPPED/
-- MAPPED_DOCKET; the source attested no mappable T4 door, so none was
-- fabricated). Only d2-wl-void-rift is a true phantom.
--
-- THE GUARANTEE (baked here so the reviewer sees it): this rider set performs
-- NO write to kit_mapping.mapping_json.t4_doors. There is NO door-strip UPDATE
-- in this file. The NULL t4_doors stay NULL (the honest "no T4 door attested"
-- state). If any future door-catalogue-build rider iterates t4_doors, it MUST
-- skip NULL arrays (treat NULL as "no doors", never coerce to [] or "").
--
-- COUNT CORRECTION (W3a throwaway-validation finding; report-what-EXISTS law):
-- The pilot §7 listed "8 NULL-t4_doors" kits -- those 8 are the RECORD-GAME
-- subset (all D2), which was the pilot's scope. The FULL live population of
-- t4_doors == JSON-null is 29 (json_type='null'): 8 record-game + 21 annex-game.
-- Separately, 16 rows carry an EMPTY ARRAY []. The pilot's characterization of
-- the 8 record-game D2 kits (7 meaningful + 1 phantom) is UNCHANGED and correct;
-- only the corpus-wide tally was under-counted in the pilot's §7 framing. The
-- A-7 preserve-NULL guarantee applies to ALL 29 JSON-null rows (and does not
-- touch the 16 []-rows either).
--   record-game NULL-t4_doors (8, the pilot §7 set, D2): d2-wl-void-rift(phantom)
--     · d2-summonmancer · d2-grim-ward-barb · d2-horker · d2-summon-druid
--     · d2-teleport-sorc · d2-sacrifice · d2-impale-zon (7 meaningful + 1 phantom).
--   annex-game NULL-t4_doors (21): d3(9: 7 GAPPED + 2 APPROX) · di(9: 4 GAPPED +
--     3 APPROX + 2 CLOSE) · d4(3 GAPPED). (annex is out of Leg-A re-emission
--     scope; NULL preserved regardless.)
--
-- The single record-game phantom (d2-wl-void-rift) is a SEPARATE disposition
-- item (phantom-kit cleanup), NOT a door-hygiene write, NOT touched this wave.
--
-- Verification the apply script asserts (proves A-7 held -- count UNCHANGED
-- pre/post riders; use json_type to distinguish JSON-null from missing-key):
--   SELECT COUNT(*) FROM kit_mapping
--    WHERE json_type(mapping_json,'$.t4_doors')='null';   -- MUST equal 29 (unchanged)
--   SELECT COUNT(*) FROM kit_mapping m JOIN canon_corpus c ON m.kit_id=c.kit_id
--    WHERE json_type(m.mapping_json,'$.t4_doors')='null'
--      AND c.corpus_bucket IN ('poe1','d2','gd','poe2','le'); -- MUST equal 8 (record-game)


-- =====================================================================
-- END RIDERS + SEEDS.  *** NOT RUN ***
-- All riders idempotent + reversible (raw columns elem_raw/eras/cell_key never
-- dropped; corpus_class derivable from is_system+corpus_bucket; court re-
-- derivable from elem_raw). Post-rider census assertions are pinned inline for
-- the W3b apply script to check before the v2.0 stamp.
-- =====================================================================
