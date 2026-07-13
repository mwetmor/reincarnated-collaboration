# Mega-Probe 2026-07-12 — Index

**Commission:** gandalf, 2026-07-12 (Matt's G1 ruling: "collect entire surface of re-probe at once")
**Filed:** legolas, 2026-07-12
**Purpose:** Re-characterize all 515 canon corpus rows (19 games) from retired mobile-harvest vocabulary to structured mechanical FACTS. Full schema = 6 fact families per positive kit: delivery · footprint · geo_text · control · defense · economy · element · movement · prefix_claims (6-slot: attr/range/tempo/amp/proxy/commit) · mechanics_notes · era_confirmed · post_cutoff · dossier_owed · rank1_upgrade · sources_used. Negative kits use light schema.

**Output directory:** `agentic_orchestration/legolas/research/megaprobe-2026-07-12/`

---

## Schema notes (corrected 2026-07-12 per gandalf mid-run brief)

**CORRECTED POSITIVES (full schema — 6 fact families per kit):**
```
kit_id · game · folk_name · atlas_key (verbatim provenance)
delivery:      {value: projectile|line|beam|at-target|self-origin|orbit|aura-pulse|other, conf, evidence}
footprint:     {value: point|small-radius|large-zone|ring|cone|lane|chain-hop|multi-point|other, conf, evidence}
geo_text:      1–2 sentence plain-text spatial behavior
control:       {ailments: [...], centrality: core|rider|none, conf}
defense:       {layers: [armor|resist|dodge|block|shield-absorb|sustain-leech|hp-stack|glass|other], primary, conf}
economy:       {resource_verbatim, model: spend|cooldown|meter|reserve|ammo|proc|recipe|draft|harvest|self-cost|other,
                meter_type: rage|combo|focus|charge|n/a, builder_source, plain_text, conf}
element:       {label_verbatim, damage_mode: hit|dot|hybrid, conf}
movement:      {verbs: [...], policy_while_casting: rooted|walk|full-move, skill_is_movement: bool, conf}
prefix_claims: {attr, range, tempo, amp, proxy, commitment} — each {value, conf, evidence}
mechanics_notes · era_confirmed · post_cutoff · rank1_upgrade · sources_used: [prov keys + live URLs]
```

**Negatives (light schema):** kit_id · folk_name · game · status · atlas_key · delivery · footprint · why_negative · era_span · post_cutoff · dossier_owed · prov · mech_note

**delivery vocab:** projectile | line | beam | at-target | self-origin | orbit | aura-pulse | other

**footprint vocab:** point | small-radius | large-zone | ring | cone | lane | chain-hop | multi-point | other

**commit vocab:** instant | wind-up | channel (NEVER "snap" — code hygiene flag only)

**Confidence rules (corrected):**
- Prefix slots: source-verified confidence per slot (NOT formula avg_conf × multiplier — that approach retired)
- delivery/footprint: source-verified confidence (approximate the quality of mechanic knowledge for that skill)
- Post-cutoff kits: all slot conf capped at 0.50; `dossier_owed: true`

**Three directed sweeps (restore per gandalf brief):**
1. Support-existence (ctrl C2): does ANY solo-context pure-support kit exist? Answer in index.
2. Line-vs-projectile (geo G2): inside single-target/projectile kits, flag true line geometry.
3. Shield-split (def D1): flag which kits are actually shield/ES/ward kits vs armour/HP.

**UPGRADE-OWED games (status: COMPLETED 2026-07-12):**
- d2, poe1, d3, d4, gd — in-place full-schema upgrade applied (commits 7b64fbb / 44a63e5 / 130feb0 / 955161e / 71b7be2); delivery/footprint/post-cutoff preserved; all 6 fact families added

---

## Game order + status

| # | Game | File | Corpus rows | Status | Commit |
|---|---|---|---|---|---|
| 1 | d2 | `d2-facts.jsonl` | 58 (51 pos / 7 neg) | **DONE (full schema)** | 7b64fbb |
| 2 | poe1 | `poe1-facts.jsonl` | 91 (85 pos / 6 neg) | **DONE (full schema)** | 44a63e5 |
| 3 | d3 | `d3-facts.jsonl` | 46 (42 pos / 4 neg) | **DONE (full schema)** | 130feb0 |
| 4 | d4 | `d4-facts.jsonl` | 45 (41 pos / 4 neg) | **DONE (full schema)** | 955161e |
| 5 | gd | `gd-facts.jsonl` | 41 (38 pos / 3 neg) | **DONE (full schema)** | 71b7be2 |
| 6 | le | `le-facts.jsonl` | 35 (32 pos / 3 neg / 4 pc) | **DONE (full schema)** | 995a732 |
| 7 | poe2 | `poe2-facts.jsonl` | 38 (34 pos / 4 neg / 7 post-cutoff) | **DONE (full schema)** | 998c6a8 |
| 8 | di | `di-facts.jsonl` | 23 (20 pos / 0 neg / 3 post-cutoff) | **DONE (full schema)** | 1df4d50 |
| 9 | tq + tq2 | `tq-facts.jsonl` | 26 (19 pos / 2 neg / 5 post-cutoff TQ2-EA) | **DONE (full schema)** | 1cf9122 |
| 10 | tl1 + tl2 + tli | `tl-facts.jsonl` | 22 (16 pos / 1 neg / 5 post-cutoff TLI-2026) | **DONE (full schema)** | 3de8aa6 |
| 11 | chronicon | `chronicon-facts.jsonl` | 17 (17 pos / 0 neg / 0 post-cutoff) | **DONE (full schema)** | 234f657 |
| 12 | undecember | `undecember-facts.jsonl` | 17 (17 pos / 0 neg / 4 post-cutoff ud-s7-2025) | **DONE (full schema)** | 8729cd6 |
| 13 | hades1 + hades2 | `hades-facts.jsonl` | 13 (13 pos / 0 neg / 4 post-cutoff hades2-1.0+) | **DONE (full schema)** | 3dc0a96 |
| 14 | vs | `vs-facts.jsonl` | 24 (22 pos / 2 neg / 1 post-cutoff vs-1.13-2025+) | **DONE (full schema)** | 2945325 |
| 15 | hot | `hot-facts.jsonl` | 19 (18 pos / 1 neg / 2 post-cutoff hot-1.1-2026) | **DONE (full schema)** | 7384750 |

**Unit B** (founding-roster lineage enrichment, 45 rows): **DONE** — `roster-lineage-enrichment.jsonl` | commit 58d7e96

**Unit C** (per-game meta verify, 19 rows): **DONE** — `per-game-meta.jsonl` | commit cf26c37

**Unit D** (mint dossiers re-expressed in Unit A schema): **DONE** — `mint-dossiers-reexpressed.jsonl` | commit 5f4dbce

---

## Post-cutoff notes per game

- **d2:** 6 Warlock kits (d2-wl-*) — Reign of the Warlock Season 13, launched Feb 2026. All capped at conf≤0.5, dossier_owed=true.
- **poe2:** All 38 rows from 0.1–0.2 era; post-0.2 patches (0.3–0.5, Dawn of the Hunt) = post-cutoff. Check per-row.
- **d4:** S4–S7 era items may be post-cutoff; flag per-row.
- **le:** Epoch 1.0+ kits; verify per-row.
- Other games: mostly pre-cutoff; flag any confirmed post-cutoff.

---

---

## Sweep answers (compiled 2026-07-12 from all 15 game files)

### C2 — Support-existence verdict

**VERDICT: NO solo-context pure-support kit exists in the 515-row corpus.**

No kit has `control.centrality = core` in a way that denotes "pure support with no damage function." All 478 positive kits deliver damage as their primary vector. Control at centrality=rider exists in ~58 kits (kits where control is a meaningful secondary function, e.g., d2-singer stun, d2-bonemancer Bone Prison, poe1-bane curse application, d2-trapsin Lightning Sentry stun) but none are damage-free support kits. The corpus genre (solo-play ARPG) structurally excludes pure supports — there is no ally to support.

Kits with control centrality=core in the data are those where the control mechanism IS the damage delivery (e.g., le-frost-wall-rm, poe2-acolyte-darkness, vs-infinite-corridor-crimson-shroud) — these are better described as control-via-damage kits, not support kits. The C2 question is answered definitively: the genre does not have this archetype.

### G2 — Line-vs-projectile (beam/lane census)

**True beams (delivery=beam): 14 kits**

| Kit | Footprint | Note |
|---|---|---|
| poe1-incinerate | cone | Channeled flamethrower; ramp stages |
| poe1-crackling-lance | lane | Branching lightning beam along lane |
| poe1-divine-ire | lane | Charged-release focused beam |
| d3-arachyr-firebats | cone | Witch Doctor flame beam |
| gd-flames-of-ignaffar-purifier | cone | Channeled flame blast |
| gd-drain-essence-spellbinder | chain-hop | Beam that chains |
| gd-aar-spellbinder | point | Point-discharge beam (low spread) |
| le-ghostflame-warlock | cone | Ghostflame channel cone |
| di-ray-of-frost-wizard | lane | DI beam + lane freeze |
| ud-flamethrower-channel | cone | Undecember flame channel |
| vs-infinite-corridor-crimson-shroud | lane | Clock Lancet freeze beams |
| vs-phieraggi | ring | Rotating laser fans |
| hot-dragons-breath | cone | Halls of Torment flame cone |
| hot-exterminator-burn | cone | Flamethrower class |

**Key non-beams confirmed (poe1 Spark/Arc explicitly):**
- `poe1-arc`: delivery=**projectile**, footprint=chain-hop — NOT a beam. Arc fires projectiles that chain; the "lightning arc" visuals are from the chain, not a sustained beam.
- `poe1-spark`: delivery=**projectile**, footprint=multi-point — NOT a beam. Spark fires wandering scatter projectiles; no beam geometry.
- `vs-heaven-sword`: delivery=projectile, footprint=lane — boomerang return arc; NOT a beam.
- `vs-hellfire`: delivery=projectile, footprint=lane — screen-length piercing projectile; NOT a beam.

**Lane footprint non-beam kits (projectile or self-origin with lane shape):** d2-firewall-sorc (line/lane), d4-pen-shot (projectile/lane), gd-forcewave-warlord (self-origin/lane), le-chthonic-fissure-warlock (line/lane), le-frost-wall-rm (at-target/lane), di-bone-wall-necro-pvp (at-target/lane), di-draw-quarter-crusader (self-origin/lane), tq-shield-charge-conqueror (self-origin/lane), vs-hellfire (projectile/lane), hot-phantom-needles (projectile/lane).

### D1 — Shield-split

**Primary defense layer breakdown across 478 positive kits:**

| Primary layer | Count | Representative kits |
|---|---|---|
| armor | ~300 | Most T1 ARPG kits (default) |
| resist | ~60 | poe1 resist-primary (many poe1 kits) |
| energy-shield | 8 | poe1-bane, poe1-soulrend, poe2 ES builds (poe2-cof-comet, poe2-spark-stormweaver, poe2-demon-form, poe2-erasure-edc-lich, poe2-bonestorm, poe2-temporalis-blink) |
| shield-absorb | 10 | d2-bonemancer (Bone Armor), poe2-grim-feast, di-corpse-explosion-necro, di-bone-wall-necro-pvp, di-minion-necro, di-warlock-launch, tq-liche-king-conjurer, chr-bloodbinder-warlock, chr-demon-legion-warlock, vs-infinite-corridor-crimson-shroud (damage cap) |
| block | 8 | d2-hammerdin, d2-zealot, d2-charger, d2-smiter, di-crusader-banner, chr-thorns-templar, hades1-beowulf-cast, hot-shieldmaiden-block |
| hp-stack | ~15 | Summoner builds, bear form |
| sustain-leech | ~12 | d2-frenzy-barb, poe1-cyclone, poe1-life-tap-slayer |
| glass | ~20 | Nova sorc, poe1 extreme glass cannons |
| dodge | ~15 | Assassin variants, rogue builds |

**Shield-absorb (true absorb buffer) vs ES (energy shield) vs ward:** shield-absorb = a discrete damage-absorb layer that regenerates (bone armor, damage cap, barrier). ES = mana-shield equivalent (poe1/poe2). No ward-specific archetype in corpus. The two are mechanically distinct: ES depletes and recharges via mechanics; shield-absorb is typically a hit-count absorb layer.

---

## Continuation protocol

Each game-file is self-contained JSONL. Sessions can pick up from the next PENDING game in the table. Update this index status column + commit column as each file lands.

**Mega-probe COMPLETE as of 2026-07-12.** All 15 Unit A game files upgraded to full schema. Units B/C/D filed. Three sweep verdicts recorded.
