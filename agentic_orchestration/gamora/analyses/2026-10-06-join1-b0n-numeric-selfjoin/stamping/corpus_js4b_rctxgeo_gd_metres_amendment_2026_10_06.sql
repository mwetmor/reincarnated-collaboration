-- corpus_js4b_rctxgeo_gd_metres_amendment_2026_10_06.sql
-- R-CTX-GEO SCOPE AMENDMENT + the gd_metres skill radii. Proposed by gamora (rule owner); ACCEPTED
-- PROVISIONALLY by the conductor (KP-304), jack-ryan confirms at the JOIN-1 B0-N Gate-2. APPLIED BY elrond,
-- AFTER corpus_js4b_rule_stamping_2026_10_06.sql. If the Gate-2 rejects the amendment, revert = set these
-- 5 rows' {rdr_value, rule_id, rule_version_applied} back to NULL and drop the description suffix.
-- R-CTX-GEO's prose covers 'skill radii in yards/metres'; its Covers enumeration omits gd_metres.
-- Transform unchanged (IDENTITY: a metre is a metre). rule_version left at 1 (no transform change); if the
-- conductor rules a version bump instead, change rule_version and rule_version_applied together.
BEGIN TRANSACTION;
UPDATE normalization_rule SET description = description || ' ⚑ SCOPE AMENDMENT 2026-10-06 (gamora, rule owner; conductor KP-304 ACCEPTED PROVISIONALLY, pending jack-ryan JOIN-1 B0-N Gate-2): + gd_metres (skill radii only, metres; IDENTITY, transform unchanged).'
 WHERE rule_id = 'R-CTX-GEO' AND instr(description, 'SCOPE AMENDMENT 2026-10-06') = 0;
-- the 5 gd_metres skill-radius rows: eor_radius_m, soulfire_explosion_radius_m, vires_might_target_radius_m, war_cry_radius_m_r16, violent_delights_target_radius_m
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-CTX-GEO', rule_version_applied = 1
 WHERE kit_id = 'gd-eor-warlord-referent' AND source_scale = 'gd_metres' AND rule_id IS NULL AND rdr_value IS NULL;
SELECT 'GUARD post: gd_metres rows stamped (expect 5)=' || COUNT(*) FROM kit_numeric WHERE kit_id='gd-eor-warlord-referent' AND source_scale='gd_metres' AND rule_id='R-CTX-GEO';
COMMIT;
