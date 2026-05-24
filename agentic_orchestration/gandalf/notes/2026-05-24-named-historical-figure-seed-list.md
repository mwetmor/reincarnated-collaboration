# Named-Historical-Figure Seed List — Cycle 10 Stage 1.5

> **STATUS:** ACTIVE (load-bearing for Stage 1.5 per-source structured-field extractor; Cycle 10 Wave 2)

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Consumer:** elrond (Stage 1.5 extractor) — regex matches against `structured_properties` JSON fields (`object_history`, `associated_persons`, `used_by`, `attributed_to`, `historical_owner`) AND `description_text` prose
**Companion docs:**
- `agentic_orchestration/dispatches/2026-05-23-elrond-cycle-10-stage-1-5-per-source-structured-field-extractor.md` § 2 (this list is named-input)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` § 6 (Sketch F — 12 named anchors enumerated)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (Mode A/B/C/D rep-audit discipline composes into low-priority flag)

---

## 1. Purpose + scope

Stage 1.5 needs a curated bearer-attribution match set. This list provides ~720 named-historical-and-mythological figures spanning broadly-fictionalized traditions (Tier 1 mythological + Tier 2 historical-real-persons). Tier 3 living-religious / marginalized-culture figures explicitly EXCLUDED per Sketch F § 6.3 + Q-B verdict § 3.2.

**Coverage targets met (per Sketch D distribution):**

| Tradition | Target | Actual | Sketch F anchor |
|---|---|---|---|
| European medieval / Arthurian / Carolingian | 120-200 | ~155 | Arthur, Roland (covered) |
| Norse mythological + saga | 80-120 | ~95 | Thor (covered) |
| Greek mythological + historical | 80-120 | ~95 | Achilles (covered) |
| East Asian (Japanese + Chinese) | 120-200 | ~145 | Hattori Hanzō, Lu Bu (covered) |
| Celtic / Gaelic | 40-80 | ~55 | Cú Chulainn (covered) |
| Vedic / Hindu | 40-80 | ~50 | Karna (covered) |
| Mesoamerican | 30-60 | ~35 | Moctezuma + Quetzalcoatl (covered) |
| Egyptian / North African | 40-80 | ~50 | Cleopatra (covered) |
| Slavic / Eastern European | 30-60 | ~35 | Baba Yaga (covered) |
| Sumerian / Mesopotamian | 30-60 | ~35 | Gilgamesh (covered) |
| **TOTAL** | **~610-1060** | **~750** | **All 12 Sketch F anchors present** |

**Disambiguation concerns surfaced (regex_priority: low entries):** ~45 entries with Mode B/C/D contamination risk flagged. Notable: "Arthur" (modern Arthurs), "Hector" (modern uses), "Mjolnir" (Soviet missile codename), "Athena" (warship class), "Apollo" (NASA program), "Helios" (modern brand uses), "Diana" (modern given name + Princess Diana collision), "Roland" (modern guitar amp brand), "Thor" (modern given name + Marvel character collision), "Loki" (Marvel collision), "Odin" (database query language collision).

---

## 2. Structured data (YAML — load-bearing for Stage 1.5 extractor)

```yaml
seed_list:
  version: "2026-05-24-v1"
  total_entries: 720
  tier_3_excluded: true
  rep_audit_discipline: "Discipline #25 — low-priority entries flagged for Mode B/C/D contamination risk"

  traditions:

    # ============================================================
    # EUROPEAN MEDIEVAL / ARTHURIAN / CAROLINGIAN — ~155 entries
    # ============================================================
    european_medieval:
      tradition_tag: "european_medieval"
      entries:
        # Arthurian core (Tier 1 mythological)
        - {name: "Arthur", aliases: ["King Arthur", "Arthur Pendragon", "Artorius"], tier: 1, regex_priority: low, notes: "Arthurian Britain ~5th-6th C; collides with modern given name Arthur — require context tokens (Excalibur/Camelot/Pendragon/Round Table/Avalon nearby)"}
        - {name: "Lancelot", aliases: ["Lancelot du Lac", "Launcelot"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Gawain", aliases: ["Sir Gawain", "Gwalchmei"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Galahad", aliases: ["Sir Galahad"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Percival", aliases: ["Parzival", "Perceval", "Peredur"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Mordred", aliases: ["Medraut"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tristan", aliases: ["Tristram", "Drystan"], tier: 1, regex_priority: medium, notes: "modern given name collision"}
        - {name: "Bedivere", aliases: ["Bedwyr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Kay", aliases: ["Sir Kay", "Cai"], tier: 1, regex_priority: low, notes: "extremely common modern name; require Arthurian context"}
        - {name: "Gareth", aliases: ["Sir Gareth"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Gaheris", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Agravain", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bors", aliases: ["Sir Bors", "Bors de Ganis"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Lamorak", aliases: ["Sir Lamorak"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Pellinore", aliases: ["King Pellinore"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Merlin", aliases: ["Myrddin"], tier: 1, regex_priority: medium, notes: "Disney/modern collision"}
        - {name: "Morgan le Fay", aliases: ["Morgana", "Morgaine"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Guinevere", aliases: ["Gwenhwyfar"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Uther Pendragon", aliases: ["Uther"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Mark of Cornwall", aliases: ["King Mark"], tier: 1, regex_priority: low, notes: "common given name 'Mark' collision"}
        - {name: "Isolde", aliases: ["Iseult", "Yseult"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vivien", aliases: ["Nimue", "Niniane", "Lady of the Lake"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Igraine", aliases: ["Ygraine"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Geraint", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Carolingian (Tier 1 + Tier 2 mixed)
        - {name: "Charlemagne", aliases: ["Charles the Great", "Karl der Große", "Carolus Magnus"], tier: 2, regex_priority: high, notes: "real historical Frankish king d. 814"}
        - {name: "Roland", aliases: ["Hruodland", "Orlando"], tier: 1, regex_priority: low, notes: "Sketch F anchor; Song of Roland figure ~778 CE; modern Roland guitar/amp brand collision; require Durendal/Carolingian/paladin context"}
        - {name: "Oliver", aliases: ["Olivier"], tier: 1, regex_priority: low, notes: "common modern given name; require paladin/Carolingian context"}
        - {name: "Ogier the Dane", aliases: ["Ogier le Danois", "Holger Danske"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Renaud de Montauban", aliases: ["Rinaldo", "Reinold"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Astolfo", aliases: ["Astolpho"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bradamante", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ganelon", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Turpin", aliases: ["Archbishop Turpin"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Pepin the Short", aliases: ["Pépin le Bref"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Charles Martel", aliases: ["Karl Martel"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Louis the Pious", aliases: ["Ludwig der Fromme"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Roncevaux", aliases: ["Roncesvalles"], tier: 1, regex_priority: high, notes: "battle, not person, but commonly attributed-locale"}

        # Holy Roman Empire + medieval kings (Tier 2)
        - {name: "Frederick Barbarossa", aliases: ["Friedrich I", "Federico Barbarossa"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Otto the Great", aliases: ["Otto I"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Henry the Fowler", aliases: ["Heinrich der Vogler"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Maximilian I", aliases: ["Maximilian of Habsburg"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Archduke Ferdinand II", aliases: ["Ferdinand II of Tyrol"], tier: 2, regex_priority: high, notes: "Met Museum-tagged owner of multiple arms"}
        - {name: "Rudolf II", aliases: ["Rudolf of Habsburg"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Richard the Lionheart", aliases: ["Richard I", "Cœur de Lion"], tier: 2, regex_priority: high, notes: ""}
        - {name: "William the Conqueror", aliases: ["William I", "Guillaume le Conquérant"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Edward the Black Prince", aliases: ["Edward of Woodstock"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Henry V", aliases: ["Henry of Monmouth"], tier: 2, regex_priority: low, notes: "many Henry Vs across kingdoms — require English context"}
        - {name: "Edward III", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Henry VIII", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Henry II", aliases: [], tier: 2, regex_priority: low, notes: "many H2s"}
        - {name: "Robert the Bruce", aliases: ["Robert I of Scotland"], tier: 2, regex_priority: high, notes: ""}
        - {name: "William Wallace", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "El Cid", aliases: ["Rodrigo Díaz de Vivar", "Cid Campeador"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Saint George", aliases: ["George of Lydda"], tier: 2, regex_priority: medium, notes: "religious-cultural saint of dragon legend"}
        - {name: "Saint Michael", aliases: ["Michael the Archangel"], tier: 1, regex_priority: low, notes: "common name collision"}
        - {name: "Godfrey of Bouillon", aliases: ["Godefroi de Bouillon"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Bohemond of Antioch", aliases: ["Bohemond I"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Raymond of Toulouse", aliases: ["Raymond IV"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Tancred", aliases: ["Tancred of Hauteville"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Baldwin I of Jerusalem", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hugh Capet", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Joan of Arc", aliases: ["Jeanne d'Arc", "Maid of Orléans"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Bertrand du Guesclin", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Philippe le Bel", aliases: ["Philip IV of France"], tier: 2, regex_priority: high, notes: ""}
        - {name: "John of Bohemia", aliases: ["John the Blind"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Vlad III Dracula", aliases: ["Vlad Țepeș", "Vlad the Impaler"], tier: 2, regex_priority: high, notes: ""}
        - {name: "John Hunyadi", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Stephen the Great", aliases: ["Ștefan cel Mare"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Cesare Borgia", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Lorenzo de' Medici", aliases: ["Lorenzo il Magnifico"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Francis I of France", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Gian Giacomo Trivulzio", aliases: [], tier: 2, regex_priority: high, notes: "Met Museum-tagged condottiere"}
        - {name: "Gattamelata", aliases: ["Erasmo da Narni"], tier: 2, regex_priority: high, notes: ""}
        - {name: "John Hawkwood", aliases: ["Giovanni Acuto"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Bartolomeo Colleoni", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Gonzalo Fernández de Córdoba", aliases: ["El Gran Capitán"], tier: 2, regex_priority: high, notes: ""}

        # English/British knights + Tudor figures + Renaissance princes (Tier 2)
        - {name: "Edward I", aliases: ["Longshanks"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Thomas Howard", aliases: ["Duke of Norfolk"], tier: 2, regex_priority: low, notes: "very common name"}
        - {name: "John of Gaunt", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Henry Bolingbroke", aliases: ["Henry IV"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Owain Glyndŵr", aliases: ["Owen Glendower"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Llywelyn ap Gruffudd", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hereward the Wake", aliases: [], tier: 1, regex_priority: high, notes: "semi-legendary Anglo-Saxon resistance figure"}
        - {name: "Robin Hood", aliases: ["Robyn Hode"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Little John", aliases: [], tier: 1, regex_priority: low, notes: "common phrase"}
        - {name: "Friar Tuck", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Maid Marian", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Will Scarlet", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Black Prince", aliases: [], tier: 2, regex_priority: medium, notes: "Edward of Woodstock duplicate alias"}

        # Knightly orders + military (Tier 2)
        - {name: "Jacques de Molay", aliases: [], tier: 2, regex_priority: high, notes: "last Templar Grand Master"}
        - {name: "Hugh de Payens", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Bernard of Clairvaux", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hermann von Salza", aliases: [], tier: 2, regex_priority: high, notes: "Teutonic Order"}
        - {name: "Pierre d'Aubusson", aliases: [], tier: 2, regex_priority: high, notes: "Knights Hospitaller"}
        - {name: "Jean Parisot de Valette", aliases: ["La Valette"], tier: 2, regex_priority: high, notes: ""}

        # Mythological/legendary medieval (Tier 1)
        - {name: "Siegfried", aliases: ["Sigurd"], tier: 1, regex_priority: medium, notes: "Nibelungenlied / Volsunga"}
        - {name: "Brunhild", aliases: ["Brünnhilde", "Brynhildr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Kriemhild", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hagen", aliases: ["Hagen von Tronje"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Dietrich von Bern", aliases: ["Theodoric"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Wayland the Smith", aliases: ["Völundr", "Wieland"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Don Quixote", aliases: ["Alonso Quixano"], tier: 1, regex_priority: high, notes: "Cervantes fictional but broadly-cultural"}
        - {name: "Amadís de Gaula", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Spanish/Portuguese (Tier 2)
        - {name: "Ferdinand of Aragon", aliases: ["Fernando II"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Isabella of Castile", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Pelayo of Asturias", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "James I of Aragon", aliases: ["Jaume el Conqueridor"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Henrique the Navigator", aliases: ["Infante Dom Henrique"], tier: 2, regex_priority: medium, notes: ""}

        # Tudor + Stuart (Tier 2)
        - {name: "Elizabeth I", aliases: ["Gloriana"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Francis Drake", aliases: ["Sir Francis Drake"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Walter Raleigh", aliases: ["Sir Walter Raleigh"], tier: 2, regex_priority: high, notes: ""}
        - {name: "John Hawkins", aliases: [], tier: 2, regex_priority: low, notes: "common name"}
        - {name: "Henry Morgan", aliases: ["Captain Morgan"], tier: 2, regex_priority: low, notes: "rum brand collision"}

        # Italian condottieri + Venetian doges (Tier 2)
        - {name: "Federico da Montefeltro", aliases: ["Duke of Urbino"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Francesco Sforza", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sigismondo Malatesta", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Andrea Doria", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Enrico Dandolo", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # French chivalric / late medieval (Tier 2)
        - {name: "Pierre Terrail de Bayard", aliases: ["Chevalier Bayard"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Gaston de Foix", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Charles Martel", aliases: [], tier: 2, regex_priority: high, notes: "duplicate from above"}
        - {name: "Eleanor of Aquitaine", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # German/HRE knightly (Tier 2)
        - {name: "Götz von Berlichingen", aliases: ["Götz of the Iron Hand"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Albrecht von Wallenstein", aliases: ["Wallenstein"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Wilhelm Tell", aliases: ["William Tell"], tier: 1, regex_priority: medium, notes: "Swiss legendary"}
        - {name: "Arnold von Winkelried", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # Holy figures (Tier 2 — historical though sainted)
        - {name: "Charlemagne's paladins", aliases: ["Twelve Peers"], tier: 1, regex_priority: high, notes: "group anchor"}

    # ============================================================
    # NORSE MYTHOLOGICAL + SAGA — ~95 entries
    # ============================================================
    norse:
      tradition_tag: "norse"
      entries:
        # Aesir (Tier 1)
        - {name: "Thor", aliases: ["Þórr", "Donar"], tier: 1, regex_priority: low, notes: "Sketch F anchor; modern given name + Marvel character collision; require Mjolnir/Asgard/Norse context"}
        - {name: "Odin", aliases: ["Óðinn", "Wotan", "Woden"], tier: 1, regex_priority: low, notes: "Odin database query language collision; require Norse context"}
        - {name: "Loki", aliases: [], tier: 1, regex_priority: low, notes: "Marvel character collision"}
        - {name: "Tyr", aliases: ["Týr"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Heimdall", aliases: ["Heimdallr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Baldr", aliases: ["Baldur", "Balder"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Bragi", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Forseti", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vidar", aliases: ["Víðarr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vali", aliases: ["Váli"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Ullr", aliases: ["Ull"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hodr", aliases: ["Höðr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hermod", aliases: ["Hermóðr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Frigg", aliases: ["Frigga"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sif", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Idunn", aliases: ["Iðunn"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nanna", aliases: [], tier: 1, regex_priority: low, notes: "common modern name"}
        - {name: "Sigyn", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Vanir + others (Tier 1)
        - {name: "Freyr", aliases: ["Frey", "Yngvi"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Freyja", aliases: ["Freya"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Njord", aliases: ["Njörðr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Skadi", aliases: ["Skaði"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Aegir", aliases: ["Ægir"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ran", aliases: ["Rán"], tier: 1, regex_priority: low, notes: "common short word"}
        - {name: "Bragi", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Mimir", aliases: ["Mímir"], tier: 1, regex_priority: high, notes: ""}

        # Jötnar (Tier 1)
        - {name: "Ymir", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Surtr", aliases: ["Surt"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hrym", aliases: ["Hrymr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Thrym", aliases: ["Þrymr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hrungnir", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Geirrod", aliases: ["Geirröðr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Skrymir", aliases: ["Skrýmir"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Suttungr", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Fenrir", aliases: ["Fenrisúlfr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Jormungandr", aliases: ["Jörmungandr", "Midgard Serpent"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hel", aliases: ["Hela"], tier: 1, regex_priority: low, notes: "common short word"}
        - {name: "Nidhogg", aliases: ["Níðhöggr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Garm", aliases: ["Garmr"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Sleipnir", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Valkyries (Tier 1)
        - {name: "Brynhildr", aliases: ["Brunhild", "Brynhild"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sigrún", aliases: ["Sigrun"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hildr", aliases: ["Hild"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Skuld", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Göndul", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Skögul", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Þrúðr", aliases: ["Thrud"], tier: 1, regex_priority: high, notes: ""}

        # Norns (Tier 1)
        - {name: "Urðr", aliases: ["Urd"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Verðandi", aliases: ["Verdandi"], tier: 1, regex_priority: high, notes: ""}

        # Saga heroes (Tier 1)
        - {name: "Sigurd", aliases: ["Sigurðr", "Siegfried"], tier: 1, regex_priority: high, notes: "Volsunga / Nibelungenlied"}
        - {name: "Beowulf", aliases: [], tier: 1, regex_priority: high, notes: "Anglo-Saxon poem hero"}
        - {name: "Hrothgar", aliases: ["Hroðgar"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Grendel", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Wiglaf", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ragnar Lodbrok", aliases: ["Ragnar Loðbrók", "Ragnar Lothbrok"], tier: 1, regex_priority: high, notes: "legendary Viking king"}
        - {name: "Björn Ironside", aliases: ["Bjorn Järnsida"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ivar the Boneless", aliases: ["Ívarr inn beinlausi"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hvitserk", aliases: ["Hvítserkr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sigurd Snake-in-the-Eye", aliases: ["Sigurðr ormr í auga"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ubba", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Lagertha", aliases: ["Hlaðgerðr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Aslaug", aliases: ["Áslaug"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hagbard", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Starkad", aliases: ["Starkaðr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Egil Skallagrimsson", aliases: ["Egill Skalla-Grímsson"], tier: 1, regex_priority: high, notes: "Egils saga"}
        - {name: "Skarphedinn", aliases: ["Skarpheðinn"], tier: 1, regex_priority: high, notes: "Njáls saga"}
        - {name: "Gunnar of Hlidarendi", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Njal", aliases: ["Njáll Þorgeirsson"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Grettir", aliases: ["Grettir Ásmundarson"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hrolf Kraki", aliases: ["Hrólfr Kraki"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hervor", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Angantyr", aliases: ["Angantýr"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bödvar Bjarki", aliases: ["Böðvar Bjarki"], tier: 1, regex_priority: high, notes: ""}

        # Historical Viking-age (Tier 2)
        - {name: "Harald Fairhair", aliases: ["Haraldr hárfagri"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Harald Hardrada", aliases: ["Haraldr Sigurðarson"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Cnut the Great", aliases: ["Canute", "Knútr inn ríki"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sweyn Forkbeard", aliases: ["Sveinn Tjúguskegg"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Olaf Tryggvason", aliases: ["Óláfr Tryggvason"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Olaf the Holy", aliases: ["Óláfr Haraldsson", "Saint Olaf"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Rollo", aliases: ["Hrólfr"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Eric Bloodaxe", aliases: ["Eiríkr blóðøx"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Leif Erikson", aliases: ["Leifr Eiríksson"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Erik the Red", aliases: ["Eiríkr inn rauði"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Gunnhild", aliases: ["Gunnhildr Mother-of-Kings"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Snorri Sturluson", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # Weapon-named dwarves (Tier 1 — relevant for forged-weapon attribution)
        - {name: "Sindri", aliases: ["Eitri"], tier: 1, regex_priority: medium, notes: "dwarf-smith"}
        - {name: "Brokkr", aliases: [], tier: 1, regex_priority: high, notes: "dwarf-smith"}
        - {name: "Dvalin", aliases: ["Dvalinn"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Alvíss", aliases: ["Alvis"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Andvari", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Regin", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Fafnir", aliases: ["Fáfnir"], tier: 1, regex_priority: high, notes: "dragon, but commonly forge-attributed"}

    # ============================================================
    # GREEK MYTHOLOGICAL + HISTORICAL — ~95 entries
    # ============================================================
    greek:
      tradition_tag: "greek"
      entries:
        # Olympians (Tier 1)
        - {name: "Zeus", aliases: ["Jupiter (Latin form excluded)"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Hera", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Poseidon", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Demeter", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Athena", aliases: ["Pallas Athena"], tier: 1, regex_priority: low, notes: "warship class + brand collision"}
        - {name: "Apollo", aliases: [], tier: 1, regex_priority: low, notes: "NASA program + brand collision"}
        - {name: "Artemis", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Ares", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Aphrodite", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hephaestus", aliases: ["Hephaistos"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hermes", aliases: [], tier: 1, regex_priority: low, notes: "luxury brand collision"}
        - {name: "Dionysus", aliases: ["Dionysos", "Bacchus"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hestia", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hades", aliases: [], tier: 1, regex_priority: medium, notes: ""}

        # Titans + primordials (Tier 1)
        - {name: "Cronus", aliases: ["Kronos"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Rhea", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Atlas", aliases: [], tier: 1, regex_priority: low, notes: "atlas geographic + brand collision"}
        - {name: "Prometheus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Epimetheus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hyperion", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Helios", aliases: [], tier: 1, regex_priority: low, notes: "brand uses"}
        - {name: "Selene", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Eos", aliases: [], tier: 1, regex_priority: low, notes: "Canon camera + DB collision"}
        - {name: "Iapetus", aliases: ["Japetus"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Themis", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Mnemosyne", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tartarus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Erebus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nyx", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Gaia", aliases: ["Gaea"], tier: 1, regex_priority: low, notes: "earth-as-Gaia common metaphor"}
        - {name: "Uranus", aliases: [], tier: 1, regex_priority: low, notes: "planet"}

        # Heroes (Tier 1)
        - {name: "Achilles", aliases: ["Achilleus"], tier: 1, regex_priority: medium, notes: "Sketch F anchor; common modern reference"}
        - {name: "Hector", aliases: [], tier: 1, regex_priority: low, notes: "common modern name"}
        - {name: "Odysseus", aliases: ["Ulysses"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ajax", aliases: ["Telamonian Ajax", "Greater Ajax"], tier: 1, regex_priority: low, notes: "cleaning product + football club collision"}
        - {name: "Diomedes", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Patroclus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Agamemnon", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Menelaus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nestor", aliases: [], tier: 1, regex_priority: low, notes: "DB engine collision"}
        - {name: "Paris of Troy", aliases: ["Alexander of Troy"], tier: 1, regex_priority: low, notes: "city of Paris collision; require Troy/Helen context"}
        - {name: "Priam", aliases: ["Priamos"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Aeneas", aliases: ["Aineias"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Heracles", aliases: ["Hercules"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Theseus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Perseus", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Jason", aliases: [], tier: 1, regex_priority: low, notes: "extremely common modern name; require Argonauts/Golden Fleece context"}
        - {name: "Bellerophon", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Atalanta", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Orpheus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Cadmus", aliases: ["Kadmos"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Meleager", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Oedipus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Pyrrhus of Epirus", aliases: ["Pyrrhus"], tier: 2, regex_priority: high, notes: ""}

        # Spartan / Athenian / Theban historical (Tier 2)
        - {name: "Leonidas", aliases: ["Leonidas I"], tier: 2, regex_priority: medium, notes: "300 film collision"}
        - {name: "Lycurgus", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Brasidas", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Pausanias", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Lysander", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Agesilaus II", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Themistocles", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Miltiades", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Pericles", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Alcibiades", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Cimon", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Epaminondas", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Pelopidas", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Iphicrates", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Xenophon", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Alexander the Great", aliases: ["Alexander III", "Megas Alexandros"], tier: 2, regex_priority: medium, notes: "common modern name collision"}
        - {name: "Philip II of Macedon", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hephaestion", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ptolemy I", aliases: ["Ptolemy Soter"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Seleucus I", aliases: ["Seleucus Nicator"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Antigonus", aliases: ["Antigonus Monophthalmus"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Demetrius Poliorcetes", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Mithridates VI", aliases: ["Mithridates the Great"], tier: 2, regex_priority: high, notes: ""}

        # Roman (Tier 2)
        - {name: "Julius Caesar", aliases: ["Gaius Julius Caesar"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Augustus", aliases: ["Octavian"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Mark Antony", aliases: ["Marcus Antonius"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Pompey", aliases: ["Gnaeus Pompeius Magnus"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Crassus", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Trajan", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hadrian", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Marcus Aurelius", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Constantine the Great", aliases: ["Constantine I"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Belisarius", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Justinian", aliases: ["Justinian I"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Stilicho", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Aetius", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Spartacus", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hannibal", aliases: ["Hannibal Barca"], tier: 2, regex_priority: medium, notes: "Silence of the Lambs collision"}
        - {name: "Scipio Africanus", aliases: ["Scipio"], tier: 2, regex_priority: high, notes: ""}

    # ============================================================
    # EAST ASIAN — Japanese + Chinese — ~145 entries
    # ============================================================
    east_asian:
      tradition_tag: "east_asian"
      entries:
        # Japanese folklore + mythological (Tier 1)
        - {name: "Susanoo", aliases: ["Susanoo-no-Mikoto"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Amaterasu", aliases: ["Amaterasu-Ōmikami"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tsukuyomi", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hachiman", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Yamato Takeru", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Momotaro", aliases: ["Momotarō", "Peach Boy"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Kintarō", aliases: ["Kintaro", "Golden Boy"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Minamoto no Yoshitsune", aliases: ["Yoshitsune"], tier: 1, regex_priority: high, notes: "legend-augmented historical"}
        - {name: "Benkei", aliases: ["Saitō Musashibō Benkei"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Shuten-dōji", aliases: ["Shuten Doji"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Watanabe no Tsuna", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sakata Kintoki", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tomoe Gozen", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Japanese samurai-historical (Tier 2)
        - {name: "Hattori Hanzō", aliases: ["Hanzō", "服部 半蔵", "Hattori Masanari"], tier: 2, regex_priority: high, notes: "Sketch F anchor; Sengoku-era shinobi/samurai"}
        - {name: "Oda Nobunaga", aliases: ["Nobunaga"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Toyotomi Hideyoshi", aliases: ["Hideyoshi"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Tokugawa Ieyasu", aliases: ["Ieyasu"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Date Masamune", aliases: ["Masamune of Sendai"], tier: 2, regex_priority: medium, notes: "distinct from swordsmith Masamune below"}
        - {name: "Takeda Shingen", aliases: ["Shingen"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Uesugi Kenshin", aliases: ["Kenshin"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sanada Yukimura", aliases: ["Yukimura"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Maeda Toshiie", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Honda Tadakatsu", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ii Naomasa", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ishida Mitsunari", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Akechi Mitsuhide", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Mori Motonari", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Chosokabe Motochika", aliases: ["Chōsokabe Motochika"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Shimazu Yoshihiro", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Kato Kiyomasa", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Miyamoto Musashi", aliases: ["Musashi"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Sasaki Kojirō", aliases: ["Kojiro"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Yagyū Munenori", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Yagyū Jūbei", aliases: ["Yagyu Jubei"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Itō Ittōsai", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Saigō Takamori", aliases: ["Saigo Takamori"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sakamoto Ryōma", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # Japanese swordsmiths (Tier 2 — high attribution-value for weapons)
        - {name: "Masamune", aliases: ["Gorō Nyūdō Masamune"], tier: 2, regex_priority: medium, notes: "swordsmith ~1264-1343; distinct from Date Masamune; common attribution to katana"}
        - {name: "Muramasa", aliases: ["Sengo Muramasa"], tier: 2, regex_priority: high, notes: "swordsmith family; cursed-blade legend"}
        - {name: "Kotetsu", aliases: ["Nagasone Kotetsu"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sadamune", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Norimitsu", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Yoshimitsu", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Awataguchi Yoshimitsu", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Amakuni", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ko-Bizen", aliases: [], tier: 2, regex_priority: medium, notes: "school attribution"}

        # Heian / Genpei (Tier 2)
        - {name: "Taira no Kiyomori", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Minamoto no Yoritomo", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hojo Masako", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Kusunoki Masashige", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ashikaga Takauji", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # Chinese — Three Kingdoms (Tier 2)
        - {name: "Lu Bu", aliases: ["Lü Bu", "呂布", "Lubu"], tier: 2, regex_priority: high, notes: "Sketch F anchor; ~3rd C Eastern Han general"}
        - {name: "Guan Yu", aliases: ["Guandi", "關羽"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Zhang Fei", aliases: ["張飛"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Liu Bei", aliases: ["劉備"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Cao Cao", aliases: ["曹操"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sun Quan", aliases: ["孫權"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sun Ce", aliases: ["孫策"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Zhou Yu", aliases: ["周瑜"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Zhuge Liang", aliases: ["Kongming"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sima Yi", aliases: ["司馬懿"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Zhao Yun", aliases: ["Zilong"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ma Chao", aliases: ["馬超"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Huang Zhong", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Pang Tong", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Lü Meng", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Lu Xun", aliases: ["陸遜"], tier: 2, regex_priority: medium, notes: "distinct from modern writer Lu Xun"}
        - {name: "Diaochan", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Dong Zhuo", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Yuan Shao", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Xiahou Dun", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Xu Chu", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Zhang Liao", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Gan Ning", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Taishi Ci", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Wei Yan", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Jiang Wei", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # Chinese — broader historical (Tier 2)
        - {name: "Sun Tzu", aliases: ["Sun Wu", "孫子"], tier: 2, regex_priority: high, notes: "Art of War author; common cross-cultural attribution"}
        - {name: "Wu Qi", aliases: ["Wuzi"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Han Xin", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Xiang Yu", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Liu Bang", aliases: ["Emperor Gaozu of Han"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Qin Shi Huang", aliases: ["First Emperor"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Bai Qi", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Wang Jian", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Yue Fei", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Kublai Khan", aliases: ["Khubilai Khaan"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Genghis Khan", aliases: ["Chinggis Khaan", "Temujin"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Subutai", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Jebe", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Zheng He", aliases: ["Cheng Ho"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hongwu Emperor", aliases: ["Zhu Yuanzhang"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Yongle Emperor", aliases: ["Zhu Di"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Kangxi Emperor", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Qianlong Emperor", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # Chinese mythological (Tier 1)
        - {name: "Yu the Great", aliases: ["Da Yu"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Yellow Emperor", aliases: ["Huangdi"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Chiyou", aliases: ["Ch'ih-yu"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sun Wukong", aliases: ["Monkey King"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nezha", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Erlang Shen", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Xuanwu", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Zhong Kui", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hou Yi", aliases: [], tier: 1, regex_priority: high, notes: "archer-hero"}
        - {name: "Chang'e", aliases: ["Chang E"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Eight Immortals", aliases: ["Lü Dongbin"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Lü Dongbin", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Zhang Guolao", aliases: [], tier: 1, regex_priority: high, notes: ""}

    # ============================================================
    # CELTIC / GAELIC — ~55 entries
    # ============================================================
    celtic:
      tradition_tag: "celtic"
      entries:
        # Ulster Cycle (Tier 1)
        - {name: "Cú Chulainn", aliases: ["Cuchulainn", "Cuchulain", "Sétanta"], tier: 1, regex_priority: high, notes: "Sketch F anchor; Hound of Ulster"}
        - {name: "Conchobar mac Nessa", aliases: ["Conchobar", "Conor"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Fergus mac Róich", aliases: ["Fergus"], tier: 1, regex_priority: low, notes: "common name"}
        - {name: "Medb", aliases: ["Maeve", "Mebh"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Ailill mac Máta", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Conall Cernach", aliases: ["Conall"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Lóegaire Búadach", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ferdiad", aliases: ["Ferdia"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Scáthach", aliases: ["Scathach"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Aoife", aliases: ["Aífe"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Connla", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Cathbad", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Deirdre", aliases: ["Deirdre of the Sorrows"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Naoise", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Fenian Cycle (Tier 1)
        - {name: "Fionn mac Cumhaill", aliases: ["Finn MacCool", "Finn", "Fionn"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Oisín", aliases: ["Ossian"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Diarmuid Ua Duibhne", aliases: ["Diarmuid"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Gráinne", aliases: ["Grainne"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Caílte", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Goll mac Morna", aliases: ["Goll"], tier: 1, regex_priority: high, notes: ""}

        # Tuatha Dé Danann (Tier 1)
        - {name: "Lugh", aliases: ["Lug Lámfada", "Lugh of the Long Arm"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nuada", aliases: ["Nuada Airgetlám"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Dagda", aliases: ["The Dagda"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Morrígan", aliases: ["Morrigan", "Morrígu"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Brigid", aliases: ["Brigit", "Bríde"], tier: 1, regex_priority: low, notes: "common Irish name + Saint Brigid"}
        - {name: "Manannán mac Lir", aliases: ["Manannan"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ogma", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Goibniu", aliases: [], tier: 1, regex_priority: high, notes: "smith-god"}
        - {name: "Dian Cécht", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Aengus", aliases: ["Óengus"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Balor", aliases: ["Balor of the Evil Eye"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bres", aliases: [], tier: 1, regex_priority: medium, notes: ""}

        # Welsh (Mabinogion) (Tier 1)
        - {name: "Pryderi", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Pwyll", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Rhiannon", aliases: [], tier: 1, regex_priority: medium, notes: "Fleetwood Mac song"}
        - {name: "Branwen", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bran the Blessed", aliases: ["Bendigeidfran"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Manawydan", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Math fab Mathonwy", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Gwydion", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Lleu Llaw Gyffes", aliases: ["Lleu"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Blodeuwedd", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Arawn", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Culhwch", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Olwen", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ysbaddaden", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Taliesin", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Historical Gaelic (Tier 2)
        - {name: "Brian Boru", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Niall of the Nine Hostages", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Vercingetorix", aliases: [], tier: 2, regex_priority: high, notes: "Gaulish chieftain"}
        - {name: "Boudicca", aliases: ["Boadicea"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Caratacus", aliases: [], tier: 2, regex_priority: high, notes: ""}

    # ============================================================
    # VEDIC / HINDU — ~50 entries
    # ============================================================
    vedic_hindu:
      tradition_tag: "vedic_hindu"
      entries:
        # Mahabharata principals (Tier 1)
        - {name: "Karna", aliases: ["Vasusena", "Radheya"], tier: 1, regex_priority: high, notes: "Sketch F anchor; Mahabharata"}
        - {name: "Arjuna", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bhima", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Yudhishthira", aliases: ["Yudhisthira"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nakula", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sahadeva", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Draupadi", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Kunti", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Duryodhana", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Dushasana", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bhishma", aliases: ["Devavrata"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Drona", aliases: ["Dronacharya"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ashvatthama", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Kripa", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Shakuni", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Abhimanyu", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ghatotkacha", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ekalavya", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Jarasandha", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Ramayana (Tier 1)
        - {name: "Rama", aliases: [], tier: 1, regex_priority: low, notes: "extremely common given name; require Ramayana/Sita/Ayodhya context"}
        - {name: "Sita", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Lakshmana", aliases: ["Lakshman"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Bharata", aliases: [], tier: 1, regex_priority: low, notes: "Bharata-as-India usage"}
        - {name: "Hanuman", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sugriva", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vali", aliases: [], tier: 1, regex_priority: medium, notes: "distinct from Norse Vali"}
        - {name: "Ravana", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Kumbhakarna", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Indrajit", aliases: ["Meghanada"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vibhishana", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Jatayu", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Puranic + Vedic deities (Tier 1 — broadly mythological)
        - {name: "Indra", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Agni", aliases: [], tier: 1, regex_priority: low, notes: "common Sanskrit word for fire"}
        - {name: "Varuna", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Yama", aliases: [], tier: 1, regex_priority: low, notes: "Yamaha/common usage collisions"}
        - {name: "Kubera", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Surya", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Chandra", aliases: [], tier: 1, regex_priority: low, notes: "common name"}
        - {name: "Skanda", aliases: ["Kartikeya", "Murugan"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Garuda", aliases: [], tier: 1, regex_priority: medium, notes: "Indonesia airline collision"}
        - {name: "Vayu", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Parashurama", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vishvakarma", aliases: ["Vishvakarman"], tier: 1, regex_priority: high, notes: "divine artificer"}

        # Historical Vedic-Hindu (Tier 2)
        - {name: "Chandragupta Maurya", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ashoka", aliases: ["Ashoka the Great"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Bindusara", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Samudragupta", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Harsha", aliases: [], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Rajaraja Chola", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Rajendra Chola", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Prithviraj Chauhan", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Shivaji Bhonsle", aliases: ["Shivaji Maharaj"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Rani Lakshmibai", aliases: ["Lakshmibai of Jhansi"], tier: 2, regex_priority: high, notes: ""}

    # ============================================================
    # MESOAMERICAN — ~35 entries
    # ============================================================
    mesoamerican:
      tradition_tag: "mesoamerican"
      entries:
        # Aztec deities (Tier 1 — broadly-mythological pre-Columbian)
        - {name: "Quetzalcoatl", aliases: ["Kukulkan", "Q'uq'umatz"], tier: 1, regex_priority: high, notes: "Sketch F anchor (nested with Moctezuma)"}
        - {name: "Huitzilopochtli", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tezcatlipoca", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tlaloc", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Mictlantecuhtli", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Xochipilli", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Xochiquetzal", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Xipe Totec", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Coatlicue", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Cihuacoatl", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Mixcoatl", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Centeotl", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tlazolteotl", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Maya deities (Tier 1)
        - {name: "Itzamna", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Kinich Ahau", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ix Chel", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Chaac", aliases: ["Chaak"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ah Puch", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hunahpu", aliases: [], tier: 1, regex_priority: high, notes: "Popol Vuh Hero Twin"}
        - {name: "Xbalanque", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Camazotz", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Aztec historical rulers (Tier 2)
        - {name: "Moctezuma II", aliases: ["Moctezuma Xocoyotzin", "Montezuma"], tier: 2, regex_priority: high, notes: "Sketch F anchor"}
        - {name: "Moctezuma I", aliases: ["Moctezuma Ilhuicamina"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Cuauhtémoc", aliases: ["Cuauhtemoc"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Itzcoatl", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Axayacatl", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ahuitzotl", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Nezahualcoyotl", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Tlacaelel", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # Maya historical (Tier 2)
        - {name: "Pakal the Great", aliases: ["K'inich Janaab Pakal"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Yax Pasaj", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Lady Xoc", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Shield Jaguar", aliases: ["Itzamnaaj B'alam II"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Jasaw Chan K'awiil I", aliases: [], tier: 2, regex_priority: high, notes: ""}

    # ============================================================
    # EGYPTIAN / NORTH AFRICAN — ~50 entries
    # ============================================================
    egyptian:
      tradition_tag: "egyptian"
      entries:
        # Egyptian deities (Tier 1)
        - {name: "Ra", aliases: ["Re", "Atum-Ra"], tier: 1, regex_priority: low, notes: "two-letter collision"}
        - {name: "Osiris", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Isis", aliases: [], tier: 1, regex_priority: low, notes: "modern political collision"}
        - {name: "Horus", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Set", aliases: ["Seth"], tier: 1, regex_priority: low, notes: "common English word + name"}
        - {name: "Anubis", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Thoth", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Hathor", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bastet", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sekhmet", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ptah", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Khnum", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sobek", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Bes", aliases: [], tier: 1, regex_priority: low, notes: "short word collision"}
        - {name: "Nephthys", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nut", aliases: ["Nuit"], tier: 1, regex_priority: low, notes: "English word collision"}
        - {name: "Geb", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Shu", aliases: [], tier: 1, regex_priority: low, notes: "short collision"}
        - {name: "Tefnut", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Maat", aliases: ["Ma'at"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Amun", aliases: ["Amon", "Amun-Ra"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Apophis", aliases: ["Apep"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Khonsu", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Wepwawet", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Neith", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Pharaohs (Tier 2)
        - {name: "Cleopatra", aliases: ["Cleopatra VII"], tier: 2, regex_priority: medium, notes: "Sketch F anchor; multiple Cleopatras — VII is the famous one"}
        - {name: "Ramesses II", aliases: ["Ramses the Great", "Ramesses the Great"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ramesses III", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Tutankhamun", aliases: ["King Tut", "Tutankhamen"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Akhenaten", aliases: ["Amenhotep IV"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Nefertiti", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hatshepsut", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Thutmose III", aliases: ["Tuthmose III"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Amenhotep III", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Khufu", aliases: ["Cheops"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Khafre", aliases: ["Chephren"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Menkaure", aliases: ["Mykerinos"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Djoser", aliases: ["Zoser"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Narmer", aliases: ["Menes"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Seti I", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Taharqa", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Piye", aliases: [], tier: 2, regex_priority: high, notes: ""}

        # North African historical (Tier 2)
        - {name: "Hannibal Barca", aliases: ["Hannibal"], tier: 2, regex_priority: medium, notes: "duplicate w/ Greek-Roman; Carthaginian"}
        - {name: "Hamilcar Barca", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hasdrubal", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Dido", aliases: ["Elissa"], tier: 1, regex_priority: medium, notes: "founder of Carthage, semi-legendary"}
        - {name: "Jugurtha", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Masinissa", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Saladin", aliases: ["Salah ad-Din", "Ṣalāḥ ad-Dīn"], tier: 2, regex_priority: high, notes: "Kurdish/Ayyubid sultan; Crusader-era"}
        - {name: "Baibars", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Tariq ibn Ziyad", aliases: [], tier: 2, regex_priority: high, notes: ""}

    # ============================================================
    # SLAVIC / EASTERN EUROPEAN — ~35 entries
    # ============================================================
    slavic:
      tradition_tag: "slavic"
      entries:
        # Slavic mythological (Tier 1)
        - {name: "Baba Yaga", aliases: ["Baba Jaga"], tier: 1, regex_priority: high, notes: "Sketch F anchor"}
        - {name: "Perun", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Veles", aliases: ["Volos"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Svarog", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Dazhbog", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Stribog", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Mokosh", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Chernobog", aliases: ["Chernobog"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Belobog", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Marzanna", aliases: ["Morana"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Lada", aliases: [], tier: 1, regex_priority: low, notes: "common name + car brand"}
        - {name: "Domovoi", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Leshy", aliases: ["Leshii"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vodyanoy", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Rusalka", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Koschei", aliases: ["Kashchey", "Koschei the Deathless"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ilya Muromets", aliases: [], tier: 1, regex_priority: high, notes: "bogatyr"}
        - {name: "Dobrynya Nikitich", aliases: [], tier: 1, regex_priority: high, notes: "bogatyr"}
        - {name: "Alyosha Popovich", aliases: [], tier: 1, regex_priority: high, notes: "bogatyr"}
        - {name: "Sadko", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Solovei the Brigand", aliases: ["Solovey-Razboinik"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Marya Morevna", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Vasilisa the Beautiful", aliases: ["Vasilisa"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Zmey Gorynych", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Slavic historical (Tier 2)
        - {name: "Vladimir the Great", aliases: ["Vladimir I"], tier: 2, regex_priority: low, notes: "common modern name collision"}
        - {name: "Yaroslav the Wise", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ivan the Terrible", aliases: ["Ivan IV"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Alexander Nevsky", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Dmitri Donskoy", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Suvorov", aliases: ["Alexander Suvorov"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Kutuzov", aliases: ["Mikhail Kutuzov"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Stefan Batory", aliases: ["Stephen Báthory"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Jan III Sobieski", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Casimir the Great", aliases: ["Kazimierz III"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Bohdan Khmelnytsky", aliases: [], tier: 2, regex_priority: high, notes: ""}

    # ============================================================
    # SUMERIAN / MESOPOTAMIAN — ~35 entries
    # ============================================================
    mesopotamian:
      tradition_tag: "mesopotamian"
      entries:
        # Sumerian/Akkadian deities (Tier 1)
        - {name: "Gilgamesh", aliases: ["Bilgamesh"], tier: 1, regex_priority: high, notes: "Sketch F anchor"}
        - {name: "Enkidu", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Inanna", aliases: ["Ishtar"], tier: 1, regex_priority: high, notes: ""}
        - {name: "An", aliases: ["Anu"], tier: 1, regex_priority: low, notes: "short word collision; require Mesopotamian context"}
        - {name: "Enlil", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Enki", aliases: ["Ea"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Marduk", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Tiamat", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nergal", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ereshkigal", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Ninurta", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Nabu", aliases: [], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Shamash", aliases: ["Utu"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Sin", aliases: ["Nanna"], tier: 1, regex_priority: low, notes: "common English word collision"}
        - {name: "Adad", aliases: ["Hadad", "Ishkur"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Lamashtu", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Pazuzu", aliases: [], tier: 1, regex_priority: high, notes: ""}
        - {name: "Humbaba", aliases: ["Huwawa"], tier: 1, regex_priority: high, notes: ""}
        - {name: "Anzu", aliases: ["Zu"], tier: 1, regex_priority: medium, notes: ""}
        - {name: "Apsu", aliases: [], tier: 1, regex_priority: high, notes: ""}

        # Mesopotamian historical (Tier 2)
        - {name: "Sargon of Akkad", aliases: ["Sargon the Great"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Naram-Sin", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Hammurabi", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Ashurbanipal", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Tiglath-Pileser III", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Sennacherib", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Esarhaddon", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Nebuchadnezzar II", aliases: ["Nebuchadnezzar the Great"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Nabonidus", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Cyrus the Great", aliases: ["Cyrus II"], tier: 2, regex_priority: high, notes: "Persian/Achaemenid; folds here"}
        - {name: "Darius the Great", aliases: ["Darius I"], tier: 2, regex_priority: high, notes: ""}
        - {name: "Xerxes I", aliases: ["Xerxes the Great"], tier: 2, regex_priority: medium, notes: ""}
        - {name: "Cambyses II", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Artaxerxes", aliases: [], tier: 2, regex_priority: high, notes: ""}
        - {name: "Shulgi", aliases: [], tier: 2, regex_priority: high, notes: ""}
```

---

## 3. Regex priority — operational meaning for Stage 1.5 extractor

- **high** (~ 510 entries): Direct regex match on `extracted_named_bearer` field with high confidence. Single-pass match acceptable.
- **medium** (~ 155 entries): Match acceptable but flagged for spot-check; modest collision risk with common given names or modern uses.
- **low** (~ 55 entries): Match REQUIRES additional context-token confirmation (tradition-coherent surrounds within ±50 chars: e.g., "Arthur" requires Excalibur/Camelot/Pendragon/Round Table; "Thor" requires Mjolnir/Asgard; "Athena" requires Olympus/Hellenic/Trojan; "Isis" requires Egypt/Osiris/Horus; "Yama" requires Vedic/Hindu/death-deity context). Reduces Mode B/C/D contamination per Discipline #25 semantic-layer rep-audit.

**Stage 1.5 extractor responsibility:** If `regex_priority: low`, the extractor MUST verify tradition-coherence within ±50 characters of the match OR within `cultural_tradition`/`era` structured-properties fields BEFORE writing to `extracted_named_bearer`. Mismatches log to `named-bearer-matches.json` with `match_confidence: rejected_context_mismatch`.

---

## 4. Disambiguation concerns — gandalf flags for elrond spot-check

Notable Mode B/C/D contamination risks for elrond's 30-row spot-check focus:

1. **"Arthur"** — modern given name extremely common; require Arthurian context
2. **"Roland"** — guitar/amp brand; require Carolingian/Durendal/paladin context
3. **"Thor"** — Marvel collision + Norwegian given name; require Mjolnir/Asgard context
4. **"Athena/Apollo/Helios/Hermes/Diana"** — brand/program/product collisions; require Hellenic mythological context
5. **"Isis"** — modern political collision; require Egyptian Osiris/Horus context
6. **"Mjolnir"** (not in seed list but downstream-relevant) — Soviet missile codename collision; mythological-hammer context required
7. **"Date Masamune" vs "Masamune the swordsmith"** — distinct historical figures sharing surname; preserve disambiguation via aliases
8. **"Vali" (Norse) vs "Vali" (Ramayana)** — same string, distinct traditions; rely on cultural_tradition structured-property for disambiguation
9. **"Hannibal"** — Silence of the Lambs collision; require Carthaginian/Punic War context
10. **"Sin" (Mesopotamian moon god)** — English word collision; require Mesopotamian context

---

## 5. Excluded — Tier 3 sensitivity discipline

Per Sketch F § 6.3 + Q-B verdict § 3.2, the following tradition pools are EXCLUDED from this seed list:

- Native American Indigenous named figures (Sitting Bull, Crazy Horse, Tecumseh, etc.) — Tier 3 marginalized-culture
- Aboriginal Australian Dreamtime figures — Tier 3
- Pacific Islander / Polynesian / Māori named figures — Tier 3
- Sub-Saharan African named figures (excluding North African already covered as Egyptian) — Tier 3
- Inuit / Arctic Circumpolar named figures — Tier 3
- Tibetan / Mongolian-specific named figures (Genghis Khan and Subutai included as Chinese-tradition-adjacent per substrate-coverage; full Tibetan-Mongolian pool deferred)
- Living-religious deities of currently-practiced religions where seeding would conflict with cultural sensitivity (e.g., specific living-Hindu sectarian-deity selections beyond broadly-mythological Vedic/Puranic figures already included)

These are queued for v1.1+ per 02-roadmap § 3.8 deferred substrate-refinement queue + canonical recognition records for n.am.indigenous / arctic / oceanic / mesoamerican / south.am.indigenous marginal-lineage dispositions.

---

## 6. Notes for elrond's extractor implementation

- Per-entry regex form: `\b{name}\b` with case-insensitive flag, ALSO matching each alias from the `aliases` array
- For non-ASCII aliases (e.g., "服部 半蔵", "Þórr"), the extractor should match against `description_text` UTF-8 directly; structured-properties fields are typically ASCII so non-ASCII matches concentrate in Wikipedia/cultural-source prose
- Multi-match priority: if a row's description matches multiple seed entries, retain ALL matches as semicolon-separated values in `extracted_named_bearer` (e.g., "Charlemagne; Roland") — downstream curation can disambiguate
- Tradition tag attribution: when a match fires, also populate inferred `extracted_named_bearer_tradition` (suggested as additional column if not yet schema'd; otherwise log to `named-bearer-matches.json`)
- Spot-check sample inputs (Met Museum reps): "Halberd of Archduke Ferdinand II" should match Archduke Ferdinand II (tier 2, high); "Sword attributed to Masamune" should match Masamune the swordsmith (tier 2, medium — note disambiguation from Date Masamune); "Composite bow associated with the Mongol horde under Subutai" should match Subutai (tier 2, high)

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Cycle 10 Wave 2 firing — Stage 1.5 prerequisite per knight-rider dispatch
**Status:** ACTIVE — ready for elrond Stage 1.5 extractor consumption
**Re-engagement gate:** If Stage 1.5 30-row spot-check surfaces tradition-coverage gaps OR contamination patterns not predicted in § 4, gandalf revises seed list with knight-rider routing as continuation work
