#!/usr/bin/env python3
"""
gen-unit-c.py — Unit C: per-game meta verify (19 rows)
Output: per-game-meta.jsonl
HoT T3 confirm-or-refute explicitly included per brief.
"""

import csv, json
from pathlib import Path

BASE = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/megaprobe-2026-07-12")
CORPUS_CSV = Path("/Users/admin/Games/reincarnated-collaboration/claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv")

# Canonical tier definitions per corpus schema
TIER_NOTES = {
    "T1": "Primary genre touchstone — the major ARPG titles with full, authoritative design lineage. Highest corpus weight.",
    "T2": "Strong genre contributor — mid-tier ARPGs with verified design contributions and cross-game evidence. Standard corpus weight.",
    "T2b": "T2 with caveats — strong genre contributor but limited corpus depth (fewer rows, access gaps, or subgame status).",
    "T3": "Genre reference — horde-survivor / roguelite adjacent; real mechanical contributions but distinct genre position. Lower corpus weight; use for specific pattern evidence only.",
}

# Per-game known metadata that isn't in the CSV
GAME_META_OVERRIDES = {
    "hot": {
        "full_name": "Halls of Torment",
        "genre_class": "horde-survivor",
        "release_era": "EA-2023; 1.0-2024",
        "dev": "Chasing Carrots",
        "notes": "Horde-survivor with ARPG gear-well extraction bridge. Unique among T3 games: has persistent gear system with affixes, not just run-modifier upgrades. Canonical bridge kit: hot-gear-well-retrieval (real items with affixes inside survivor loop).",
        "t3_verdict": "CONFIRMED T3",
        "t3_rationale": (
            "Confirmed T3, NOT promoted to T2. Rationale: (1) genre-class is horde-survivor, not core ARPG — "
            "the build loop is single-run character-growth, not persistent gear economy as primary driver; "
            "(2) corpus depth = 18 pos + 1 neg; covers the full non-post-cutoff roster adequately but "
            "thin by T1 standards (poe1=85, d2=51); (3) mechanical contributions that ARE corpus-grade: "
            "aura-pulse delivery (Radiant Aura), stat-threshold-payoff economy (Shieldmaiden), "
            "offer-pool-hygiene/DR economy (Norseman), gear-well/draft-lock economy (hot-gear-well-retrieval). "
            "These belong in corpus as pattern evidence — T3 weight is appropriate for that role. "
            "(4) Promotion argument (for T2): HoT is richer than generic VS-tier games — it has a real "
            "gear system. Counter: the gear system is a distinguishing BRIDGE FEATURE, not full parity with "
            "ARPG-native persistence loops (no non-seasonal character progression, no long-term gear economy). "
            "T3 stands; the gear-well kit remains as the canonical bridge record."
        ),
    },
    "vs": {
        "full_name": "Vampire Survivors",
        "genre_class": "horde-survivor",
        "release_era": "EA-2021; 1.0-2022",
        "dev": "poncle",
        "notes": "Genre-originating horde-survivor. No persistent gear economy; build loop is per-run upgrade selection.",
        "t3_verdict": "CONFIRMED T3",
        "t3_rationale": "Genre-defining horde-survivor, no persistent gear economy. T3 is accurate weight.",
    },
    "d2": {
        "full_name": "Diablo II (+ Lord of Destruction, D2R, Reign of the Warlock S13)",
        "genre_class": "arpg-primary",
        "release_era": "2000 (LoD 2001); D2R 2021; RotW S13 Feb 2026",
        "dev": "Blizzard North / Vicarious Visions / Eleventh Hour",
        "notes": "Genre-founding ARPG. 6 warlock kits are post-cutoff (RotW S13 Feb 2026).",
        "t3_verdict": "N/A",
        "t3_rationale": "T1 — genre touchstone, no tier question.",
    },
    "poe1": {
        "full_name": "Path of Exile 1",
        "genre_class": "arpg-primary",
        "release_era": "2013–present",
        "dev": "Grinding Gear Games",
        "notes": "The modern ARPG design canon. Largest corpus set (85 pos). Ongoing content but corpus focuses on pre-3.25 era.",
        "t3_verdict": "N/A",
        "t3_rationale": "T1.",
    },
    "poe2": {
        "full_name": "Path of Exile 2",
        "genre_class": "arpg-primary",
        "release_era": "EA 0.1 Dec 2024; 0.2 Apr 2025",
        "dev": "Grinding Gear Games",
        "notes": "EA-state ARPG. Post-0.2 patches (0.3+, Dawn of the Hunt) are post-cutoff.",
        "t3_verdict": "N/A",
        "t3_rationale": "T1.",
    },
    "d3": {
        "full_name": "Diablo III",
        "genre_class": "arpg-primary",
        "release_era": "2012; Seasons through S30 2024",
        "dev": "Blizzard Entertainment",
        "notes": "Set-driven economy, season-rotation meta. S29+ potentially post-cutoff.",
        "t3_verdict": "N/A",
        "t3_rationale": "T1.",
    },
    "d4": {
        "full_name": "Diablo IV",
        "genre_class": "arpg-primary",
        "release_era": "2023; S1–S7 2023–2025",
        "dev": "Blizzard Entertainment",
        "notes": "Live-service ARPG. S5-S7 potentially post-cutoff for some kits.",
        "t3_verdict": "N/A",
        "t3_rationale": "T1.",
    },
    "gd": {
        "full_name": "Grim Dawn",
        "genre_class": "arpg-primary",
        "release_era": "2016 (Ashes of Malmouth 2017, Forgotten Gods 2019)",
        "dev": "Crate Entertainment",
        "notes": "Dual-mastery system, DA/OA defensive architecture. Pre-cutoff for all corpus rows.",
        "t3_verdict": "N/A",
        "t3_rationale": "T1.",
    },
    "le": {
        "full_name": "Last Epoch",
        "genre_class": "arpg-primary",
        "release_era": "EA 2019; 1.0 Feb 2024; Epoch 1.1+ ongoing",
        "dev": "Eleventh Hour Games",
        "notes": "Mastery tree ARPG. Epoch 1.0+ kits verified as pre-cutoff in corpus.",
        "t3_verdict": "N/A",
        "t3_rationale": "T1.",
    },
    "di": {
        "full_name": "Diablo Immortal",
        "genre_class": "arpg-mobile",
        "release_era": "2022; ongoing",
        "dev": "Blizzard Entertainment / NetEase",
        "notes": "Mobile ARPG with live-service economy. T2b — 23 pos but mobile-format constraints limit some corpus dimensions.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2b confirmed.",
    },
    "tq": {
        "full_name": "Titan Quest (2006) + Anniversary Edition",
        "genre_class": "arpg-secondary",
        "release_era": "2006; AE 2016",
        "dev": "Iron Lore Entertainment / THQ Nordic",
        "notes": "Dual-mastery ARPG predecessor. Combined with tq2 in megaprobe file.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2.",
    },
    "tq2": {
        "full_name": "Titan Quest II (EA 2025)",
        "genre_class": "arpg-secondary",
        "release_era": "EA 2025",
        "dev": "Pieces Interactive / THQ Nordic",
        "notes": "EA-state sequel. Post-cutoff by launch date; all tq2 kits have dossier_owed=true.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2 but all rows post-cutoff.",
    },
    "tl1": {
        "full_name": "Torchlight 1",
        "genre_class": "arpg-secondary",
        "release_era": "2009",
        "dev": "Runic Games",
        "notes": "Single-player ARPG. Thin corpus (2 rows). Combined in tl-facts.jsonl.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2.",
    },
    "tl2": {
        "full_name": "Torchlight 2",
        "genre_class": "arpg-secondary",
        "release_era": "2012",
        "dev": "Runic Games",
        "notes": "4-class ARPG with engineer/outlander/embermage. 11 rows.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2.",
    },
    "tli": {
        "full_name": "Torchlight: Infinite (2026)",
        "genre_class": "arpg-mobile",
        "release_era": "EA 2022; ongoing; 2026 season content = post-cutoff",
        "dev": "XD Inc.",
        "notes": "Mobile ARPG in poe1-influenced design space. TLI-2026 season kits are post-cutoff.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2.",
    },
    "hades1": {
        "full_name": "Hades 1",
        "genre_class": "roguelite-action",
        "release_era": "EA 2018; 1.0 Sep 2020",
        "dev": "Supergiant Games",
        "notes": "Roguelite action game. 8 positive corpus rows; all pre-cutoff.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2.",
    },
    "hades2": {
        "full_name": "Hades 2",
        "genre_class": "roguelite-action",
        "release_era": "EA May 2024; 1.0 Aug 2025",
        "dev": "Supergiant Games",
        "notes": "5 rows; 4 are post-cutoff (1.0-2025+). 1 at EA-2024 anchor (hades2-omega-magick, conf~0.62).",
        "t3_verdict": "N/A",
        "t3_rationale": "T2.",
    },
    "undecember": {
        "full_name": "Undecember",
        "genre_class": "arpg-mobile",
        "release_era": "2022; S7-2025 content = post-cutoff",
        "dev": "Line Games",
        "notes": "Mobile ARPG with poe1-influenced skill link system. 4 rows post-cutoff (ud-s7-2025).",
        "t3_verdict": "N/A",
        "t3_rationale": "T2b.",
    },
    "chronicon": {
        "full_name": "Chronicon",
        "genre_class": "arpg-indie",
        "release_era": "EA 2018; 1.0 2021",
        "dev": "Subworld",
        "notes": "Indie ARPG with 4 classes. 17 positive rows; all pre-cutoff.",
        "t3_verdict": "N/A",
        "t3_rationale": "T2.",
    },
}

def main():
    with open(CORPUS_CSV) as f:
        all_rows = list(csv.DictReader(f))

    # Filter out rdr-roster
    canon_rows = [r for r in all_rows if r.get('game') not in ('rdr-roster',) and r.get('game','')]

    # Aggregate per game
    game_agg = {}
    for r in canon_rows:
        g = r['game']
        if g not in game_agg:
            game_agg[g] = {
                'pos': 0, 'neg': 0, 'total': 0,
                'post_cutoff': 0,
                'tiers': set(), 'canon_tiers': set(),
                'provs': set(), 'eras': set(),
            }
        game_agg[g]['total'] += 1
        if r.get('negative','').lower() == 'true':
            game_agg[g]['neg'] += 1
        else:
            game_agg[g]['pos'] += 1
        if r.get('tier',''):
            game_agg[g]['tiers'].add(r['tier'])
        if r.get('canon_tier',''):
            game_agg[g]['canon_tiers'].add(r['canon_tier'])
        if r.get('prov',''):
            for p in r['prov'].split(';'):
                game_agg[g]['provs'].add(p.strip())
        if r.get('eras',''):
            for e in r['eras'].split(';'):
                game_agg[g]['eras'].add(e.strip())

    # For post-cutoff, load the fact JSONL files to get accurate counts
    # Games in the mega-probe have post_cutoff tracked per row
    JSONL_GAME_MAP = {
        # Maps game code → jsonl file(s)
        'd2': 'd2-facts.jsonl', 'poe1': 'poe1-facts.jsonl',
        'd3': 'd3-facts.jsonl', 'd4': 'd4-facts.jsonl',
        'gd': 'gd-facts.jsonl', 'le': 'le-facts.jsonl',
        'poe2': 'poe2-facts.jsonl', 'di': 'di-facts.jsonl',
        'chronicon': 'chronicon-facts.jsonl',
        'undecember': 'undecember-facts.jsonl',
        'vs': 'vs-facts.jsonl', 'hot': 'hot-facts.jsonl',
    }
    # Combined files
    COMBINED_GAME_FILES = {
        'tq': 'tq-facts.jsonl', 'tq2': 'tq-facts.jsonl',
        'tl1': 'tl-facts.jsonl', 'tl2': 'tl-facts.jsonl', 'tli': 'tl-facts.jsonl',
        'hades1': 'hades-facts.jsonl', 'hades2': 'hades-facts.jsonl',
    }

    pc_counts = {}
    for game, fname in {**JSONL_GAME_MAP, **COMBINED_GAME_FILES}.items():
        fpath = BASE / fname
        if fpath.exists():
            try:
                with open(fpath) as f:
                    recs = [json.loads(l) for l in f if l.strip()]
                # For combined files, filter by game
                if fname in ('tq-facts.jsonl', 'tl-facts.jsonl', 'hades-facts.jsonl'):
                    recs = [r for r in recs if r.get('game','') == game]
                pc_counts[game] = sum(1 for r in recs if r.get('post_cutoff', False))
            except Exception as e:
                pc_counts[game] = None
        else:
            pc_counts[game] = None

    # Build output rows
    out_rows = []
    for game in sorted(game_agg.keys()):
        agg = game_agg[game]
        meta = GAME_META_OVERRIDES.get(game, {})
        canon_tier_list = sorted(agg['tiers'])
        canon_tier = canon_tier_list[0] if canon_tier_list else 'unknown'

        row = {
            'game': game,
            'full_name': meta.get('full_name', game),
            'genre_class': meta.get('genre_class', 'arpg'),
            'canon_tier': canon_tier,
            'tier_definition': TIER_NOTES.get(canon_tier, ''),
            'release_era': meta.get('release_era', ''),
            'dev': meta.get('dev', ''),
            'corpus_pos': agg['pos'],
            'corpus_neg': agg['neg'],
            'corpus_total': agg['total'],
            'post_cutoff_count': pc_counts.get(game),
            'prov_sources': sorted(agg['provs']),
            'era_range': sorted(e for e in agg['eras'] if e),
            'notes': meta.get('notes', ''),
            't3_verdict': meta.get('t3_verdict', 'N/A'),
            't3_rationale': meta.get('t3_rationale', ''),
            'crawl_date': '2026-07-12',
        }
        out_rows.append(row)

    out_path = BASE / 'per-game-meta.jsonl'
    with open(out_path, 'w') as f:
        for row in out_rows:
            f.write(json.dumps(row) + '\n')

    print(f"Written {len(out_rows)} rows to {out_path}")
    print("\nHoT entry:")
    hot = next(r for r in out_rows if r['game'] == 'hot')
    print(f"  game={hot['game']} | tier={hot['canon_tier']} | verdict={hot['t3_verdict']}")
    print(f"  rationale (first 200 chars): {hot['t3_rationale'][:200]}")

    print("\nTier summary:")
    from collections import Counter
    tier_counts = Counter(r['canon_tier'] for r in out_rows)
    for tier, count in sorted(tier_counts.items()):
        games_in_tier = [r['game'] for r in out_rows if r['canon_tier'] == tier]
        print(f"  {tier}: {count} → {games_in_tier}")

if __name__ == '__main__':
    main()
