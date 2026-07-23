-- corpus_poe1_cyclone_weapon_citations.sql
-- KFL-13(d) elrond micro-lane — poe1-cyclone weapon-anchor citations + Berserker-thread disposition.
-- Author: elrond | 2026-07-23 | Source note (conductor-verified ANCHORED, commit 8abfeed5):
--   agentic_orchestration/legolas/notes/2026-07-23-cyclone-weapon-dps-anchor.md
--
-- Adds the three provenance rows for the newly-anchored 3.15 Slayer weapon, and dispositions the
-- pre-existing wrong-build Berserker citation. Idempotent + existing-provenance-preserving.
--
-- IDEMPOTENCY: INSERT OR IGNORE on the three new rows (UNIQUE(kit_id,url) — a re-run conflict-skips).
--   The Berserker UPDATE is idempotent by construction (sets quarantined=1 to a fixed value; re-run = no-op).
--
-- BERSERKER DISPOSITION (elrond curation call — QUARANTINE, NOT delete):
--   Existing citation id 64 = pathofexile.com/forum/view-thread/3078559 = a 3.15 Cyclone BERSERKER build.
--   This kit is Slayer-documented (KFL-2/KFL-5); legolas decoded that thread's PoB (pastebin iXrZh2pY)
--   and REJECTED it as the wrong ascendancy for this kit. Ruling: set quarantined=1 (recorded, never
--   citable) rather than DELETE — provenance is never silently destroyed (charter discipline; schema's
--   quarantine flag exists exactly for "recorded, never citable"). The row stays queryable as the
--   documented reason the wrong build was ruled out.
--   IMPORTANT — this does NOT invalidate the 59% effectiveness build-point leaves whose source_anchor
--   cites thread 3078559: Cyclone's gem effectiveness (59% at gem 20, 3.15) is a property of the SKILL GEM,
--   ascendancy-independent (Slayer and Berserker share the identical Cyclone gem). The effectiveness quote
--   is true regardless of build; the Slayer thread 3033867 (added below) is now the PRIMARY build citation,
--   and the 59% anchor stands on the gem stat. The quarantine narrows the citation's ROLE (not a build
--   endorsement), it does not weaken any leaf. source_value of every existing row is untouched.

-- ============ Three new provenance rows for the 3.15 Slayer weapon anchor ============
-- accessed_date 2026-07-23 (today's harvest). rank_class 'recovered' (live-fetched this pass, house style).
INSERT OR IGNORE INTO kit_citations
  (kit_id, url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined) VALUES
-- (1) the kit's TRUE documented-build thread — the [3.15] Cyclone Slayer thread (supersedes the Berserker
--     thread as the build citation of record; communal forum guide).
('poe1-cyclone','https://www.pathofexile.com/forum/view-thread/3033867','pathofexile.com/forum',NULL,
 '[3.15] Cyclone Build | Slayer | Expedition | Path of Exile 3.15','communal','recovered','2026-07-23',0),
-- (2) the PoB export embedded in that thread — the PRIMARY weapon anchor (verbatim item block).
--     dataset-class (a machine-readable PoB build export, not authored prose).
('poe1-cyclone','https://pastebin.com/Sf8AYHkK','pastebin.com',NULL,
 'PoB export (Cyclone Slayer 3.15) — Weapon 1: Blood Razor, rare Exquisite Blade iLvl 83','dataset','recovered','2026-07-23',0),
-- (3) poedb base-item stats page — the version-stable base for the Exquisite Blade.
('poe1-cyclone','https://poedb.tw/us/Exquisite_Blade','poedb.tw',NULL,
 'Exquisite Blade (base item) — 67-112 phys, 1.35 APS, 5.7% crit','dataset','recovered','2026-07-23',0);

-- ============ Berserker-thread disposition: QUARANTINE (recorded, never citable; NOT deleted) ============
UPDATE kit_citations
   SET quarantined = 1
 WHERE kit_id = 'poe1-cyclone'
   AND url = 'https://www.pathofexile.com/forum/view-thread/3078559'
   AND quarantined = 0;
