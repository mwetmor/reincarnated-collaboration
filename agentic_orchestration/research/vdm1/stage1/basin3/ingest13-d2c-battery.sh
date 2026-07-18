#!/bin/bash
# INGEST-13 steward D-2c readonly-SQL battery (staged in the INGEST-13 window; RUN ONLY after elrond's completion notification — never against a mid-write DB)
# Every check prints EXPECT vs GOT; no hard exits — full report always produced; steward eyeballs judgment rows.
DB=/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db
Q() { sqlite3 -readonly "$DB" "$1"; }

echo "== 0. integrity =="; Q "PRAGMA integrity_check;"

echo "== 1. verify_ledger total — EXPECT 1512 (831 pre + 680 basin-3 files + 1 cyclone-base insert) =="
Q "SELECT COUNT(*) FROM verify_ledger;"

echo "== 2. run_tag census (eyeball: pre-basin tags unchanged; basin-3 tags present) =="
Q "SELECT run_tag, COUNT(*) FROM verify_ledger GROUP BY run_tag ORDER BY run_tag;"

echo "== 3. basin-3 effective verdict census (d2/d3/d4/di prefixes) — EXPECT 681 = C 576 / U 85 / X 19 / SNF 1 =="
Q "SELECT verdict, COUNT(*) FROM verify_ledger WHERE kit_id LIKE 'd2-%' OR kit_id LIKE 'd3-%' OR kit_id LIKE 'd4-%' OR kit_id LIKE 'di-%' GROUP BY verdict;"
Q "SELECT COUNT(*) FROM verify_ledger WHERE kit_id LIKE 'd2-%' OR kit_id LIKE 'd3-%' OR kit_id LIKE 'd4-%' OR kit_id LIKE 'di-%';"

echo "== 4. basin-3 per-family census (eyeball vs PRE-LOAD table + 22 supersede deltas) =="
Q "SELECT claim_family, verdict, COUNT(*) FROM verify_ledger WHERE kit_id LIKE 'd2-%' OR kit_id LIKE 'd3-%' OR kit_id LIKE 'd4-%' OR kit_id LIKE 'di-%' GROUP BY claim_family, verdict ORDER BY claim_family, verdict;"

echo "== 5a. supersede spot-join: lightning-spear — EXPECT mechanics X (backfill U→X supersede), errata_applied visible =="
Q "SELECT kit_id, claim_family, verdict, errata_applied, substr(claim_text,1,80) FROM verify_ledger WHERE kit_id LIKE '%lightning-spear%';"
echo "== 5b. supersede spot-join: wing-strike — EXPECT NO backfill verify write; era row carries s7-s12 extension via erratum only =="
Q "SELECT kit_id, claim_family, verdict, errata_applied, substr(claim_text,1,100) FROM verify_ledger WHERE kit_id LIKE '%wing-strike%';"
echo "== 5c. insert spot-join: cyclone-strike-monk-base — EXPECT mechanics row PRESENT (the +1 INSERT) =="
Q "SELECT kit_id, claim_family, verdict, errata_applied, substr(claim_text,1,80) FROM verify_ledger WHERE kit_id LIKE '%cyclone-strike-monk-base%';"
echo "== 5d. supersede sweep: basin-3 errata_applied=1 rows (eyeball vs 22-item supersede map + erratum queue) =="
Q "SELECT COUNT(*) FROM verify_ledger WHERE (kit_id LIKE 'd2-%' OR kit_id LIKE 'd3-%' OR kit_id LIKE 'd4-%' OR kit_id LIKE 'di-%') AND errata_applied=1;"

echo "== 6. citations — totals + basin-3 quarantine EXPECT 4 (1 b01 junk-tail + 3 boost/gold-seller); dedupe = GOT vs 346+27 minus elrond OR-IGNORE report =="
Q "SELECT COUNT(*) FROM kit_citations;"
Q "SELECT COUNT(*), SUM(quarantined) FROM kit_citations WHERE kit_id LIKE 'd2-%' OR kit_id LIKE 'd3-%' OR kit_id LIKE 'd4-%' OR kit_id LIKE 'di-%';"

echo "== 7. dossier — EXPECT total 2394 (1320 pre + 1074); basin-3 abstained EXPECT 190 =="
Q "SELECT COUNT(*) FROM kit_dossier;"
Q "SELECT COUNT(*), SUM(abstained) FROM kit_dossier WHERE kit_id LIKE 'd2-%' OR kit_id LIKE 'd3-%' OR kit_id LIKE 'd4-%' OR kit_id LIKE 'di-%';"

echo "== 8. promotion gate — canon_corpus schema dump + basin-3 kit count EXPECT 179 (census query built by steward from schema + elrond MIGRATION report; must sum to 179) =="
Q ".schema canon_corpus"
Q "SELECT COUNT(*) FROM canon_corpus WHERE kit_id LIKE 'd2-%' OR kit_id LIKE 'd3-%' OR kit_id LIKE 'd4-%' OR kit_id LIKE 'di-%';"

echo "== 9. errata ledger — EXPECT ERRATA-43+ entries appended (10-part queue) =="
grep -c 'ERRATA-4[3-9]\|ERRATA-5[0-9]' /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/errata-ledger.md
grep -o 'ERRATA-4[3-9][0-9]*\|ERRATA-5[0-9]' /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/errata-ledger.md | sort -u

echo "== 10. md5 chain — pre-ingest-13 backup md5 must equal recorded ingest-12 POST md5 (compare vs elrond MIGRATION doc) =="
ls -la /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/*.db.bak* 2>/dev/null | tail -5
for f in /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/*.db.bak*; do [ -f "$f" ] && md5 -q "$f" | sed "s|^|$(basename $f): |"; done 2>/dev/null | tail -5
md5 -q "$DB" | sed 's|^|corpus.db (post-ingest-13): |'

echo "== BATTERY COMPLETE — steward verdict required on §§ 4, 5a-d, 6 (dedupe delta), 8 (census sum), 9 (part coverage), 10 (chain) =="
