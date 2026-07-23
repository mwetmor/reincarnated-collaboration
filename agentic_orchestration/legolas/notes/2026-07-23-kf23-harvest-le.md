# KF-2/3 Harvest — Last Epoch (le-frost-claw)
**Legolas Mode B** | 2026-07-23 | Kit: `le-frost-claw` (Frost Claw Sorcerer)
**Charter ref:** KFL-3 — LE CONDITIONAL: keep le-frost-claw; swap to d2-fire-sorc iff LE database proves insufficient (insufficiency = frost-claw numeric sheet cannot be fetched with verbatim anchors).

---

## SUFFICIENCY VERDICT: INSUFFICIENT — SWAP TO d2-fire-sorc AUTHORIZED

**Evidence:**

The sole community database with per-skill base stat tables is **lastepochtools.com** (canonical LE skills DB, surfaced in both the corpus citations and the KF-2 search passes). It returns **HTTP 403** on all endpoints:
- `https://www.lastepochtools.com/skills/frost_claw` → 403
- `https://www.lastepochtools.com/skills/frost_claw/nodes` → 403
- `https://www.lastepochtools.com/skills/frost_claw/sources` → 403

Official support pages (`support.lastepoch.com/hc/...`) → HTTP 403.
Official game wiki (`lastepoch.fandom.com/wiki/Frost_Claw`) → HTTP 402.
Official Last Epoch forum bug thread (`forum.lastepoch.com/t/mana-cost-reduction-in-frost-claw/61292`) → HTTP 404.

All reachable sources (maxroll.gg, icy-veins.com, forum.lastepoch.com build threads, mmoexp.com, fextralife.com, mmowts.com) are **strategy/build guides**, not database pages. They contain NO verbatim base damage, NO damage effectiveness percentage, NO baseline mana cost (only reduced post-gear targets), NO cast speed base, NO crit chance base, NO per-level scaling table.

**What IS present (strategy-level, non-anchor-grade):**
- "reduce [mana cost] to around 25 or less" — Maxroll Frostbite Runemaster guide (endgame target, not base)
- "Frost Claw mana cost gets down to 3 mana per cast" — Fextralife fire claw guide (fully geared, not base)
- "level 21 Frost Claw" mentioned as a setup example — mmowts forum (no stat numbers)
- "5 projectiles hitting same target" from Volley of Glass node — forum thread (node effect, not base projectile count)
- "400% cast speed and 1000% spell damage on sorc" — forum discussion (fully built character, not base)
- "1000 Health" / "80% Resistances" / "15000-20000+ Ward" — endgame gear targets, not base stats

**Kit-side anchor gaps (full-sheet per KFL-3):**

| Field | Status |
|---|---|
| Base cold damage (min/max per projectile) | GAP — no verbatim source found |
| Damage effectiveness | GAP — no verbatim source found |
| Base mana cost | GAP — no verbatim source found |
| Base cast speed | GAP — no verbatim source found |
| Base crit chance | GAP — no verbatim source found |
| Crit multiplier | GAP — no verbatim source found |
| Base projectile count | PARTIAL — "5 projectiles with Volley of Glass" node; base un-anchored |
| Intelligence (base/at build point) | GAP — only "80 Intelligence" as gear-milestone example |
| Attunement | GAP |
| Strength / Dex | GAP |
| Vitality | GAP |
| Ward (base / at build point) | GAP — only endgame targets (15k-20k) |
| Armor | GAP |
| Dodge | GAP |
| Cold/Fire/Lightning resist | GAP — only target goals (80%) |
| Health | GAP — "3000 HP minimum" (target, not anchored value) |

**Monster-side:** No LE enemy stat database reached. Lastepochtools.com (the only structured monster data source known) blocks all access. No HP/armor/resist/damage tables for any LE mob found with verbatim anchors.

---

## Sources consulted (all read-only, 2026-07-23)

| URL | Result |
|---|---|
| https://www.lastepochtools.com/skills/frost_claw | HTTP 403 |
| https://www.lastepochtools.com/skills/frost_claw/nodes | HTTP 403 |
| https://www.lastepochtools.com/skills/frost_claw/sources | HTTP 403 |
| https://www.lastepochtools.com/news/article/last-epoch-shattered-omens-patch-notes-80571 | HTTP 403 |
| https://support.lastepoch.com/hc/en-us/articles/46363062648987-Mage-Skills | HTTP 403 |
| https://lastepoch.fandom.com/wiki/Frost_Claw | HTTP 402 |
| https://forum.lastepoch.com/t/mana-cost-reduction-in-frost-claw/61292 | HTTP 404 |
| https://maxroll.gg/last-epoch/build-guides/frostbite-frost-claw-sorcerer-guide | Fetched — strategy only, no base stats |
| https://maxroll.gg/last-epoch/build-guides/frostbite-frost-claw-runemaster-guide | Fetched — strategy only, target stats only |
| https://maxroll.gg/last-epoch/build-guides/frost-claw-runemaster-guide | Fetched (redirect) — strategy only |
| https://www.icy-veins.com/last-epoch/runemaster-lightning-frost-claw-endgame-build | Fetched — no base skill stats |
| https://fextralife.com/last-epoch-runemaster-build-guide-fire-claw/ | Fetched — fully-geared values only |
| https://forum.lastepoch.com/t/my-best-frost-claw-nova-mage-rm-sorc/69060 | Fetched — strategy/mechanic discussion, no base stats |
| https://forum.lastepoch.com/t/frostclaw-question/68377 | Fetched — Volley of Glass discussion, no base stats |
| https://www.mmoexp.com/News/last-epoch-frost-claw-and-its-changes-in-1-2.html | Fetched — patch context, no base stats |
| https://forum.lastepoch.com/t/last-epoch-patch-1-0-2-notes/66953 | Fetched — Frost Claw not mentioned |
| https://www.mmowts.com/news/last-epoch-a-complete-guide-to-the-frost-claw-sorcerer-build | Fetched — "base damage of about 10,000 points" is a quoted estimate, not a verbatim tooltip value |

---

## KF-3 Monster harvest (LE): NOT EXECUTED

Per the sufficiency verdict (INSUFFICIENT), LE monster harvest is moot. d2-fire-sorc is the authorized swap. Monster harvest for LE's slot will be executed under d2-fire-sorc (D2 game mobs) instead.

---

## Corpus context (for elrond's reference)

- `kit_citations` for `le-frost-claw`: 2 rows (maxroll.gg frostbite guide + forum.lastepoch.com build thread) — both confirmed strategy-level, no numeric anchors.
- `canon_probe_facts` sources_used family: `["kb"]` — knowledge-base only provenance, no named source with verbatim numeric fetch.
- `kit_mapping.mapping_json` notes: "Cryomantic Fragility affix reduces Frost Claw Mana cost to ZERO" — this is an item effect, confirms base cost is non-zero, but no base cost number is anchored anywhere.

---

**Legolas scout note:** The LE data wall is total — the authoritative tool (lastepochtools.com) blocks all crawl access and no alternative public source carries verbatim base-skill numeric sheets. This is a clean INSUFFICIENT under anchor law, not a partial-data borderline case. The swap is warranted.
