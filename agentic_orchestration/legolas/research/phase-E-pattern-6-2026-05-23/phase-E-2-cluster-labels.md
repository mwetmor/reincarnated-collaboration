# Phase E-2 — Cluster Canonical Labels (125 clusters; coarse-spine)

**Author:** gandalf
**Date:** 2026-05-23
**Cluster algorithm version:** `phase-E-1-subsample-k3-2026-05-23`
**Labeling pass:** Phase E-2 (coarse-spine canonical; per gandalf Gate-2 condition 3, weapon-form-resolution-final deferred to Phase E-1.5 sensitivity sweep)
**Framing-audit checklist applied:** Yes — first applied use per `gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5
**Representative sampling:** hdbscan_native rows only per dispatch § 1 (Gate-2 condition 2 / MIGRATION.md § 4)
**Non-canonical lineages (no cluster home):** north_american_indigenous — see `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md`

---

## Summary

- **Total clusters labeled:** 125
- **Provisional-description overrides applied:** 47 (predicted 5-15; actual 47 indicates systematic provisional-label-generator drift — see sub-carry 9.11-A)
- **Indexing:** `id` = legolas cluster_id (0-124, matches clusters.md + axis-discovery + dispatch text). `db_cluster_id` = SQLite `clusters.id` (1-125, for Phase E-2-DB UPDATE clause). DB id = legolas id + 1.

**Cluster type distribution:**

| cluster_type | count |
|---|---|
| `weapon_family` | 50 |
| `named_template_family` | 41 |
| `mixed_cross_cultural` | 18 |
| `mixed_form_pool` | 9 |
| `modern_military_hardware_pool` | 4 |
| `rare_lineage_isolate` | 2 |
| `metadata_bucket` | 1 |

**Special-case flag distribution:**

| special_case_flag | count |
|---|---|
| `provisional_description_overridden` | 46 |
| `low_lineage_purity` | 20 |
| `mixed_form_within_cluster` | 13 |
| `modern_military_hardware` | 7 |
| `lineage_uncurated` | 7 |
| `period_tag_likely_metadata_artifact` | 2 |
| `absorbs_rare_lineage_rows` | 2 |
| `lineage_tag_geographic_not_cultural` | 1 |
| `labeling_pipeline_bug_surfaced` | 1 |
| `fantasy_named_template_cross_form` | 1 |
| `phase_e15_split_candidate` | 1 |
| `n_am_indigenous_passenger` | 1 |
| `rare_lineage_substrate_isolate` | 1 |
| `metadata_bucket` | 1 |
| `phase_d_bis_curation_gap` | 1 |
| `rare_lineage_no_home` | 1 |

---

## Per-Cluster Labels

Clusters are listed in legolas cluster_id order (0-124).

### Cluster 0 — Cross-Cultural Contemporary Mixed-Form Pool

- **Pool count:** N=46 (hdbscan_native subsample: 12; lineage purity 0.7391)
- **Dominant lineage / period / register / kind / wield:** cross_cultural / contemporary / military_modern / category / one_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Navy Revolver; mild steel kukri; wakizashi
- **Provisional description:** PROVISIONAL: cross_cultural contemporary staff/axe weapons (military_modern register; category; N=46)
- **Override applied:** Yes — Provisional 'staff/axe' weapon-type tokenization is wrong; top hdbscan_native reps are navy revolver + mild steel kukri + wakizashi — a cross-cultural contemporary mixed-form pool, not a staff/axe cluster.
- **Framing-audit notes:** Load-bearing assumption: provisional 'staff/axe' label denotes weapon-form coherence. Reps refute (revolver/kukri/wakizashi span pistol/knife/sword forms). Refinement: label as cross-cultural mixed-form rather than naming a specific form. Substrate is axis-coherent (cross-cultural + contemporary + military_modern + category + two-hand) but weapon-form-heterogeneous at coarse k=3.
- **Special-case flags:** provisional_description_overridden, mixed_form_within_cluster
- **Phase E-3/E-4 hand-off notes:** Phase E-1.5 sensitivity sweep at higher k may split this cluster along weapon-form lines; defer form-resolution to that pass.
- **DB cluster id:** 1 (for Phase E-2-DB UPDATE clause)

### Cluster 1 — Cross-Cultural Contemporary Pistol Pool

- **Pool count:** N=105 (hdbscan_native subsample: 27; lineage purity 0.9714)
- **Dominant lineage / period / register / kind / wield:** cross_cultural / contemporary / military_modern / category / one_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Knife; Pistol; Heavy Pistol
- **Provisional description:** PROVISIONAL: cross_cultural contemporary pistol/knife weapons (military_modern register; category; N=105)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cross-cultural contemporary pistol cluster (purity 0.9714).
- **Special-case flags:** none
- **DB cluster id:** 2 (for Phase E-2-DB UPDATE clause)

### Cluster 2 — Fantasy-Generic Fictional Battleaxe Named-Item Family

- **Pool count:** N=214 (hdbscan_native subsample: 40; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Battleaxe (rare variant); Battleaxe +1; Battleaxe +2
- **Provisional description:** PROVISIONAL: fantasy_generic fictional axe/greataxe weapons (fantasy register; named_template; N=214)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'battleaxe' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 3 (for Phase E-2-DB UPDATE clause)

### Cluster 3 — European-Tagged Contemporary Knife Pool (Mixed)

- **Pool count:** N=91 (hdbscan_native subsample: 16; lineage purity 0.5165)
- **Dominant lineage / period / register / kind / wield:** european / contemporary / historical / category / one_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Butterfly Knife; Gut Knife; Skeleton Knife
- **Provisional description:** PROVISIONAL: european contemporary pistol/knife weapons (historical register; category; N=91)
- **Override applied:** No
- **Framing-audit notes:** Low lineage purity 0.5165 — cluster has substantial secondary lineage content. Coarse-spine label retains dominant tagging with mixed flag.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 4 (for Phase E-2-DB UPDATE clause)

### Cluster 4 — Fantasy-Generic Fictional Club Family

- **Pool count:** N=31 (hdbscan_native subsample: 15; lineage purity 0.9355)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Katar; Katar of Bloodletting; Slingshot
- **Provisional description:** PROVISIONAL: fantasy_generic fictional club/hammer weapons (fantasy register; category; N=31)
- **Override applied:** Yes — Provisional weapon-form 'club/hammer' refined from rep evidence; dominant rep-form is 'wakizashi' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9355); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'club/hammer' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 5 (for Phase E-2-DB UPDATE clause)

### Cluster 5 — Fantasy-Generic Fictional Dagger Family

- **Pool count:** N=77 (hdbscan_native subsample: 18; lineage purity 0.9351)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Dagger of Terror; Javelin +3; Pistol
- **Provisional description:** PROVISIONAL: fantasy_generic fictional dagger/wand weapons (fantasy register; category; N=77)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9351); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 6 (for Phase E-2-DB UPDATE clause)

### Cluster 6 — Fantasy-Generic Fictional Wand Named-Item Family

- **Pool count:** N=149 (hdbscan_native subsample: 26; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Black Bloom Wand (rare variant); Prospector's Wand; Wand of Relieved Burdens
- **Provisional description:** PROVISIONAL: fantasy_generic fictional wand/axe weapons (fantasy register; named_template; N=149)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'wand' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 7 (for Phase E-2-DB UPDATE clause)

### Cluster 7 — Fantasy-Generic Fictional Shield Named-Item Family

- **Pool count:** N=59 (hdbscan_native subsample: 15; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Dangerous Volatile Spiked Shield; Alder Spiked Shield; Mirrored Spiked Shield
- **Provisional description:** PROVISIONAL: fantasy_generic fictional pike/sword weapons (fantasy register; named_template; N=59)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'shield' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 8 (for Phase E-2-DB UPDATE clause)

### Cluster 8 — Fantasy-Generic Fictional Revolver Named-Item Family

- **Pool count:** N=249 (hdbscan_native subsample: 44; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Bloodbone Kris; Bloodshot Revolver; Caster Blaster Revolver
- **Provisional description:** PROVISIONAL: fantasy_generic fictional axe/spear weapons (fantasy register; named_template; N=249)
- **Override applied:** Yes — Provisional weapon-form 'axe/spear' refined from rep evidence; dominant rep-form is 'revolver' (3/5).
- **Framing-audit notes:** Form-bundled named-template cluster — 3/5 top hdbscan_native reps contain 'revolver' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space. Provisional weapon-form tokens (axe/spear) did not match dominant rep-form (revolver); refined from rep evidence.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 9 (for Phase E-2-DB UPDATE clause)

### Cluster 9 — Fantasy-Generic Fictional Javelin Named-Item Family

- **Pool count:** N=155 (hdbscan_native subsample: 35; lineage purity 0.8839)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Corpse Slayer Javelin; Javelin of Certain Death; Lichslayer Dagger (rare variant)
- **Provisional description:** PROVISIONAL: fantasy_generic classical dagger/wand weapons (fantasy register; named_template; N=155)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 3/5 top hdbscan_native reps contain 'javelin' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 10 (for Phase E-2-DB UPDATE clause)

### Cluster 10 — Fantasy-Generic Fictional Javelin Named-Item Family

- **Pool count:** N=80 (hdbscan_native subsample: 20; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Javelin (rare variant); Defender Javelin; Driftwood Javelin
- **Provisional description:** PROVISIONAL: fantasy_generic fictional javelin weapons (fantasy register; named_template; N=80)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'javelin' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 11 (for Phase E-2-DB UPDATE clause)

### Cluster 11 — Fantasy-Generic Fictional Shortsword Family

- **Pool count:** N=76 (hdbscan_native subsample: 16; lineage purity 0.9211)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Greatsword +3; Shortsword of Defense; Shortsword of Wounding
- **Provisional description:** PROVISIONAL: fantasy_generic fictional sword/greatsword weapons (fantasy register; category; N=76)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9211); 3/5 reps confirm 'shortsword' form.
- **Special-case flags:** none
- **DB cluster id:** 12 (for Phase E-2-DB UPDATE clause)

### Cluster 12 — Fantasy-Generic Fictional Dagger Named-Item Family

- **Pool count:** N=266 (hdbscan_native subsample: 50; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Dagger; Adamantine Dagger; Chardalyn Dagger
- **Provisional description:** PROVISIONAL: fantasy_generic fictional dagger/sword weapons (fantasy register; named_template; N=266)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'dagger' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 13 (for Phase E-2-DB UPDATE clause)

### Cluster 13 — Fantasy-Generic Fictional Wand Named-Item Family

- **Pool count:** N=72 (hdbscan_native subsample: 11; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Mana Channeling Wand; Bloodwood Wand; Magician's Wand
- **Provisional description:** PROVISIONAL: fantasy_generic classical wand weapons (fantasy register; named_template; N=72)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'wand' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 14 (for Phase E-2-DB UPDATE clause)

### Cluster 14 — Fantasy-Generic Fictional Pistol Named-Item Family

- **Pool count:** N=83 (hdbscan_native subsample: 12; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Deepshot Pistol (rare variant); Enspelled Pistol (Level 4); Giant Slayer Pistol
- **Provisional description:** PROVISIONAL: fantasy_generic fictional pistol/lance weapons (fantasy register; named_template; N=83)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'pistol' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 15 (for Phase E-2-DB UPDATE clause)

### Cluster 15 — Fantasy-Generic Fictional Starknife Named-Item Family

- **Pool count:** N=135 (hdbscan_native subsample: 32; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / one_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Cosmic Starknife; Rootbound Multiweapon Starknife (very rare variant); Sacrificial Knife, Ceremonial
- **Provisional description:** PROVISIONAL: fantasy_generic fictional knife weapons (fantasy register; named_template; N=135)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 4/5 top hdbscan_native reps contain 'starknife' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 16 (for Phase E-2-DB UPDATE clause)

### Cluster 16 — Fantasy-Generic Fictional Shortsword Named-Item Family

- **Pool count:** N=224 (hdbscan_native subsample: 53; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Aldrnari Blade Shortsword; Aldrnari Blade Shortsword (very rare variant); Blade of Prey Shortsword
- **Provisional description:** PROVISIONAL: fantasy_generic fictional sword/shortsword weapons (fantasy register; named_template; N=224)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'shortsword' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 17 (for Phase E-2-DB UPDATE clause)

### Cluster 17 — Fantasy-Generic Fictional Greatsword Named-Item Family

- **Pool count:** N=317 (hdbscan_native subsample: 61; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Acheron Greatsword; Aperture Sword Greatsword (rare variant); Blade of the Battle Seer Greatsword
- **Provisional description:** PROVISIONAL: fantasy_generic fictional sword/greatsword weapons (fantasy register; named_template; N=317)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'greatsword' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 18 (for Phase E-2-DB UPDATE clause)

### Cluster 18 — Fantasy-Generic Fictional Longsword Named-Item Family

- **Pool count:** N=239 (hdbscan_native subsample: 46; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Adamantine Longsword; Aperture Sword Longsword (very rare variant); Aperture Sword Rapier (rare variant)
- **Provisional description:** PROVISIONAL: fantasy_generic fictional sword/longsword weapons (fantasy register; named_template; N=239)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 4/5 top hdbscan_native reps contain 'longsword' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 19 (for Phase E-2-DB UPDATE clause)

### Cluster 19 — East Asian Early-Modern Wakizashi Family

- **Pool count:** N=68 (hdbscan_native subsample: 12; lineage purity 0.9559)
- **Dominant lineage / period / register / kind / wield:** east_asian / early_modern / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Blade and Mounting for a Short Sword (Wakizashi); Blade and Mounting for a Sword (Katana); Blade and Mounting for a Sword (Katana)
- **Provisional description:** PROVISIONAL: east_asian early_modern sword/dagger weapons (historical register; category; N=68)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9559); 3/5 reps confirm 'wakizashi' form.
- **Special-case flags:** none
- **DB cluster id:** 20 (for Phase E-2-DB UPDATE clause)

### Cluster 20 — European Industrial Sword Family

- **Pool count:** N=66 (hdbscan_native subsample: 14; lineage purity 0.7121)
- **Dominant lineage / period / register / kind / wield:** european / industrial / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Light Cavalry sword; Sword and knot; Sacrificial sword (ram dao)
- **Provisional description:** PROVISIONAL: european industrial sword/axe weapons (historical register; category; N=66)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.7121); 5/5 reps confirm 'sword' form.
- **Special-case flags:** none
- **DB cluster id:** 21 (for Phase E-2-DB UPDATE clause)

### Cluster 21 — Cross-Cultural Contemporary Hafted/Edged Pool

- **Pool count:** N=123 (hdbscan_native subsample: 23; lineage purity 0.9268)
- **Dominant lineage / period / register / kind / wield:** cross_cultural / contemporary / military_modern / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** war hammer; high steel war hammer; simple makeshift glaive
- **Provisional description:** PROVISIONAL: cross_cultural contemporary sword/bow weapons (military_modern register; category; N=123)
- **Override applied:** Yes — Provisional 'sword/bow' label contradicts reps (war hammer + high steel war hammer + simple makeshift glaive). Cluster groups cross-cultural contemporary hafted+edged melee weapons.
- **Framing-audit notes:** Substrate-honest cross-cultural mixed-form cluster; reps fall in hafted/edged contemporary melee category rather than sword/bow.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 22 (for Phase E-2-DB UPDATE clause)

### Cluster 22 — East Asian Traditional Polearm/Blade Pool

- **Pool count:** N=1256 (hdbscan_native subsample: 274; lineage purity 0.9793)
- **Dominant lineage / period / register / kind / wield:** east_asian / contemporary / military_modern / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** naginata; ji; dao
- **Provisional description:** PROVISIONAL: east_asian contemporary rifle/lance weapons (military_modern register; category; N=1256)
- **Override applied:** Yes — Provisional 'rifle/lance' contradicted by reps (naginata + ji + dao — all classical East Asian polearms/blades). Despite period='contemporary' tag dominating, the represented forms are traditional east-asian polearm/sword forms.
- **Framing-audit notes:** Cluster reflects East Asian traditional weapon forms (polearm/blade). Period='contemporary' tag is likely a substrate-tagging artifact (catalogue entries describing classical forms under contemporary collection metadata). Coarse-spine label honors weapon-form signal.
- **Special-case flags:** provisional_description_overridden, period_tag_likely_metadata_artifact
- **Phase E-3/E-4 hand-off notes:** elrond Phase-D-bis follow-on: east_asian contemporary-tagged historical polearm entries may warrant period re-curation.
- **DB cluster id:** 23 (for Phase E-2-DB UPDATE clause)

### Cluster 23 — Arctic/Northern Contemporary Heavy Weapon Systems

- **Pool count:** N=34 (hdbscan_native subsample: 14; lineage purity 0.8824)
- **Dominant lineage / period / register / kind / wield:** arctic_circumpolar / contemporary / military_modern / category / two_hand
- **Cluster type:** `modern_military_hardware_pool`
- **Top-3 hdbscan_native representatives:** 2S1 Gvozdika Russian 122mm Amphibious Self-Propelled Howitzer (SPH); RBS-70 Swedish Man-Portable Air Defense Missile System (MANPADS); Mistral 3 French Man-Portable Air Defense Missile System (MANPADS)
- **Provisional description:** PROVISIONAL: arctic_circumpolar contemporary lance/rifle weapons (military_modern register; category; N=34)
- **Override applied:** Yes — Provisional 'lance/rifle' weapon-form contradicted by reps (2S1 Gvozdika SPH + RBS-70 MANPADS + Mistral 3 MANPADS). Cluster is contemporary military hardware (self-propelled howitzers, man-portable air-defense systems), not lance.
- **Framing-audit notes:** Provisional label retained 'arctic_circumpolar' lineage but reps reveal cluster is dominated by Russian/Swedish/French missile + artillery systems whose lineage tagging reflects geographic-origin metadata, not arctic-circumpolar cultural lineage. Substrate-honest arctic_circumpolar coherent weapons cluster does NOT exist at this k.
- **Special-case flags:** provisional_description_overridden, modern_military_hardware, lineage_tag_geographic_not_cultural
- **Phase E-3/E-4 hand-off notes:** Sub-carry: arctic_circumpolar substrate may need lineage-tagging re-curation distinguishing geographic-origin from cultural-lineage.
- **DB cluster id:** 24 (for Phase E-2-DB UPDATE clause)

### Cluster 24 — Fantasy-Generic Classical Pike Family

- **Pool count:** N=361 (hdbscan_native subsample: 63; lineage purity 0.9197)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Grovelthrash; Mincer; Headchopper
- **Provisional description:** PROVISIONAL: fantasy_generic classical pike/bow weapons (fantasy register; category; N=361)
- **Override applied:** Yes — Provisional weapon-form 'pike/bow' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9197); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'pike/bow' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 25 (for Phase E-2-DB UPDATE clause)

### Cluster 25 — Fantasy-Generic Fictional Hook-Sword Named-Item Family

- **Pool count:** N=410 (hdbscan_native subsample: 79; lineage purity 0.9829)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Deadly Volatile Hook Sword; Defensive Hook Sword +2; Double Sword
- **Provisional description:** PROVISIONAL: fantasy_generic fictional sword/greatsword weapons (fantasy register; named_template; N=410)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 3/5 top hdbscan_native reps contain 'hook sword' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 26 (for Phase E-2-DB UPDATE clause)

### Cluster 26 — Fantasy-Generic Fictional Staff Named-Item Family

- **Pool count:** N=244 (hdbscan_native subsample: 38; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Warden Staff; War Staff; Advisor's Gnarled Staff
- **Provisional description:** PROVISIONAL: fantasy_generic classical staff weapons (fantasy register; named_template; N=244)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'staff' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 27 (for Phase E-2-DB UPDATE clause)

### Cluster 27 — Fantasy-Generic Fictional Spear Family

- **Pool count:** N=1301 (hdbscan_native subsample: 247; lineage purity 0.9885)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Acid; Ballista; Blade of Petals
- **Provisional description:** PROVISIONAL: fantasy_generic fictional spear/mace weapons (fantasy register; category; N=1301)
- **Override applied:** Yes — Provisional weapon-form 'spear/mace' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9885); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'spear/mace' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 28 (for Phase E-2-DB UPDATE clause)

### Cluster 28 — Fantasy-Generic Fictional Staff Named-Item Family

- **Pool count:** N=437 (hdbscan_native subsample: 89; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Quarterstaff; Abyssal Bane Quarterstaff (very rare variant); Baton of the Mindbender Staff
- **Provisional description:** PROVISIONAL: fantasy_generic fictional staff/spear weapons (fantasy register; named_template; N=437)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 3/5 top hdbscan_native reps contain 'staff' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 29 (for Phase E-2-DB UPDATE clause)

### Cluster 29 — Fantasy-Generic Fictional Crossbow Named-Item Family

- **Pool count:** N=76 (hdbscan_native subsample: 12; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Nine Lives Stealer Light Crossbow; Nine Lives Stealer Scimitar; Ram's Head Crossbow
- **Provisional description:** PROVISIONAL: fantasy_generic classical bow/crossbow weapons (fantasy register; named_template; N=76)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 4/5 top hdbscan_native reps contain 'crossbow' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 30 (for Phase E-2-DB UPDATE clause)

### Cluster 30 — South Asian Contemporary Mixed-Form Pool

- **Pool count:** N=77 (hdbscan_native subsample: 41; lineage purity 0.6234)
- **Dominant lineage / period / register / kind / wield:** south_asian / contemporary / military_modern / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** kirpan; Browning Hi-Power .40 S&W; Advik FPV Indian Unmanned Aerial Vehicle (UAV)
- **Provisional description:** PROVISIONAL: south_asian contemporary pistol/sword weapons (military_modern register; category; N=77)
- **Override applied:** Yes — Provisional 'pistol/sword' contradicted by reps spanning kirpan (Sikh dagger) + Browning Hi-Power pistol + Advik Indian UAV. Cluster mixes religious knives, modern pistols, and Indian drone systems.
- **Framing-audit notes:** Lineage purity 0.6234 — cluster has secondary lineage contribution. Coarse-spine label reflects mixed-form nature; weapon-form distinctions impossible at k=3.
- **Special-case flags:** provisional_description_overridden, modern_military_hardware, low_lineage_purity
- **DB cluster id:** 31 (for Phase E-2-DB UPDATE clause)

### Cluster 31 — Southeast Asian Contemporary Heavy Munitions Pool

- **Pool count:** N=194 (hdbscan_native subsample: 30; lineage purity 0.5155)
- **Dominant lineage / period / register / kind / wield:** southeast_asian / contemporary / military_modern / category / two_hand
- **Cluster type:** `modern_military_hardware_pool`
- **Top-3 hdbscan_native representatives:** DARPA flamethrower; STK 40 AGL Singaporean 40mm Automatic Grenade Launcher; MDH-10 Vietnamese Anti-Personnel Mine
- **Provisional description:** PROVISIONAL: southeast_asian contemporary rifle weapons (military_modern register; category; N=194)
- **Override applied:** Yes — Provisional 'rifle' contradicted by reps (DARPA flamethrower + STK 40 AGL Singaporean grenade launcher + MDH-10 Vietnamese anti-personnel mine). Cluster is contemporary heavy munitions, not rifles.
- **Framing-audit notes:** Lineage purity 0.5155 — secondary contributions present. Cluster substrate-honest at axis level (contemporary + military_modern + southeast asia adjacency) but populated with grenade/mine/flamethrower forms.
- **Special-case flags:** provisional_description_overridden, modern_military_hardware, low_lineage_purity
- **DB cluster id:** 32 (for Phase E-2-DB UPDATE clause)

### Cluster 32 — Cross-Cultural Contemporary Rifle Pool

- **Pool count:** N=121 (hdbscan_native subsample: 31; lineage purity 0.9752)
- **Dominant lineage / period / register / kind / wield:** cross_cultural / contemporary / military_modern / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Bullpup Rifle; Marksman Rifle; Military Rifle
- **Provisional description:** PROVISIONAL: cross_cultural contemporary rifle/shotgun weapons (military_modern register; category; N=121)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cross-cultural contemporary rifle cluster (purity 0.9752).
- **Special-case flags:** none
- **DB cluster id:** 33 (for Phase E-2-DB UPDATE clause)

### Cluster 33 — Fantasy-Generic Fictional Sword Family

- **Pool count:** N=54 (hdbscan_native subsample: 16; lineage purity 0.9444)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Sword of Answering; Sword of Corrosion; Sword of Kas
- **Provisional description:** PROVISIONAL: fantasy_generic fictional sword/greatsword weapons (fantasy register; category; N=54)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9444); 4/5 reps confirm 'sword' form.
- **Special-case flags:** none
- **DB cluster id:** 34 (for Phase E-2-DB UPDATE clause)

### Cluster 34 — Fantasy-Generic Fictional Mixed Named-Item Pool

- **Pool count:** N=468 (hdbscan_native subsample: 94; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Caustic Bow; Chardalyn Shortbow; Compound Bow
- **Provisional description:** PROVISIONAL: fantasy_generic fictional bow/club weapons (fantasy register; named_template; N=468)
- **Override applied:** No
- **Framing-audit notes:** Mixed named-template cluster; neither weapon-form nor name-prefix dominates top-5 reps. Coarse-spine label.
- **Special-case flags:** mixed_form_within_cluster
- **DB cluster id:** 35 (for Phase E-2-DB UPDATE clause)

### Cluster 35 — Fantasy-Generic Fictional Halberd Named-Item Family

- **Pool count:** N=152 (hdbscan_native subsample: 38; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Halberd (very rare variant); Blood Drinker Halberd; Consecrated Weapon Halberd
- **Provisional description:** PROVISIONAL: fantasy_generic fictional halberd weapons (fantasy register; named_template; N=152)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'halberd' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 36 (for Phase E-2-DB UPDATE clause)

### Cluster 36 — Fantasy-Generic Fictional Glaive Named-Item Family

- **Pool count:** N=115 (hdbscan_native subsample: 34; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Blood Drinker Glaive (legendary variant); Chaos Glaive; Defender Glaive
- **Provisional description:** PROVISIONAL: fantasy_generic fictional glaive weapons (fantasy register; named_template; N=115)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'glaive' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 37 (for Phase E-2-DB UPDATE clause)

### Cluster 37 — Fantasy-Generic Fictional Staff Family

- **Pool count:** N=133 (hdbscan_native subsample: 23; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Blackstaff; Staff; Staff of Giantkin
- **Provisional description:** PROVISIONAL: fantasy_generic fictional staff/axe weapons (fantasy register; category; N=133)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 1.0); 4/5 reps confirm 'staff' form.
- **Special-case flags:** none
- **DB cluster id:** 38 (for Phase E-2-DB UPDATE clause)

### Cluster 38 — Fantasy-Generic Fictional Mixed Named-Item Pool

- **Pool count:** N=349 (hdbscan_native subsample: 67; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Bane Hammer; Chardalyn Light Hammer; Chardalyn Warhammer
- **Provisional description:** PROVISIONAL: fantasy_generic fictional hammer/pike weapons (fantasy register; named_template; N=349)
- **Override applied:** No
- **Framing-audit notes:** Mixed named-template cluster; neither weapon-form nor name-prefix dominates top-5 reps. Coarse-spine label.
- **Special-case flags:** mixed_form_within_cluster
- **DB cluster id:** 39 (for Phase E-2-DB UPDATE clause)

### Cluster 39 — Fantasy-Generic Fictional Mixed Named-Item Pool

- **Pool count:** N=143 (hdbscan_native subsample: 34; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Pike; Abyssal Bane Spiked Cestus (rare variant); Abyssal Bane Spiked Knuckle Duster (rare variant)
- **Provisional description:** PROVISIONAL: fantasy_generic fictional pike/lance weapons (fantasy register; named_template; N=143)
- **Override applied:** No
- **Framing-audit notes:** Mixed named-template cluster; neither weapon-form nor name-prefix dominates top-5 reps. Coarse-spine label.
- **Special-case flags:** mixed_form_within_cluster
- **DB cluster id:** 40 (for Phase E-2-DB UPDATE clause)

### Cluster 40 — Fantasy-Generic Fictional Scimitar Named-Item Family

- **Pool count:** N=237 (hdbscan_native subsample: 49; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Scimitar; Adamantine Scimitar; Blade of Prey Scimitar
- **Provisional description:** PROVISIONAL: fantasy_generic fictional scimitar/axe weapons (fantasy register; named_template; N=237)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'scimitar' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 41 (for Phase E-2-DB UPDATE clause)

### Cluster 41 — Fantasy-Generic Fictional Crossbow Named-Item Family

- **Pool count:** N=342 (hdbscan_native subsample: 57; lineage purity 0.9825)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Bloodseeker Crossbow Bolt; Crosstacean Hand Crossbow (very rare variant); Crosstacean Light Crossbow (very rare variant)
- **Provisional description:** PROVISIONAL: fantasy_generic fictional bow/crossbow weapons (fantasy register; named_template; N=342)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'crossbow' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 42 (for Phase E-2-DB UPDATE clause)

### Cluster 42 — Fantasy-Generic Fictional Handaxe Named-Item Family

- **Pool count:** N=434 (hdbscan_native subsample: 89; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Handaxe; Adamantine Handaxe; Awakened Abyss Warden's Axeblade
- **Provisional description:** PROVISIONAL: fantasy_generic fictional axe/flail weapons (fantasy register; named_template; N=434)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 4/5 top hdbscan_native reps contain 'handaxe' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 43 (for Phase E-2-DB UPDATE clause)

### Cluster 43 — Fantasy-Generic Fictional Lance Named-Item Family

- **Pool count:** N=114 (hdbscan_native subsample: 24; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Centaur Lance; Chardalyn Lance; Corpse Slayer Lance
- **Provisional description:** PROVISIONAL: fantasy_generic fictional lance/shotgun weapons (fantasy register; named_template; N=114)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'lance' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 44 (for Phase E-2-DB UPDATE clause)

### Cluster 44 — African Contemporary Military Vehicles + Munitions Pool

- **Pool count:** N=72 (hdbscan_native subsample: 15; lineage purity 0.6806)
- **Dominant lineage / period / register / kind / wield:** african / contemporary / military_modern / category / two_hand
- **Cluster type:** `modern_military_hardware_pool`
- **Top-3 hdbscan_native representatives:** Exodii Sapra grenade launcher; OT 4x4 Serbian Armored Personnel Carrier (APC); 9M113 Konkurs (AT-5 Spandrel) Russian Anti-Tank Guided Missile (ATGM)
- **Provisional description:** PROVISIONAL: african contemporary pike/rifle weapons (military_modern register; category; N=72)
- **Override applied:** Yes — Provisional 'pike/rifle' contradicted by reps (Exodii Sapra grenade launcher + OT 4x4 Serbian APC + 9M113 Konkurs ATGM). Cluster is contemporary armored vehicles + anti-tank missiles, not pike forms.
- **Framing-audit notes:** Lineage purity 0.6806; cluster identity is contemporary military hardware with African geographic-origin tagging.
- **Special-case flags:** provisional_description_overridden, modern_military_hardware, low_lineage_purity
- **DB cluster id:** 45 (for Phase E-2-DB UPDATE clause)

### Cluster 45 — Fantasy-Generic Fictional Flail Named-Item Family

- **Pool count:** N=110 (hdbscan_native subsample: 18; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Driftwood Flail; Enspelled Flail (Level 6); Flail +2
- **Provisional description:** PROVISIONAL: fantasy_generic fictional flail weapons (fantasy register; named_template; N=110)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'flail' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 46 (for Phase E-2-DB UPDATE clause)

### Cluster 46 — Fantasy-Generic Fictional Rapier Named-Item Family

- **Pool count:** N=223 (hdbscan_native subsample: 52; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Aldrnari Blade Rapier; Broken Promise Rapier; Chardalyn Rapier
- **Provisional description:** PROVISIONAL: fantasy_generic fictional rapier/axe weapons (fantasy register; named_template; N=223)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'rapier' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 47 (for Phase E-2-DB UPDATE clause)

### Cluster 47 — European-Tagged Fictional Scimitar Pool (Mixed)

- **Pool count:** N=107 (hdbscan_native subsample: 31; lineage purity 0.514)
- **Dominant lineage / period / register / kind / wield:** european / fictional / fantasy / named_template / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Crossbow bolts +1; Crossbow bolts +2; Gaol Net
- **Provisional description:** PROVISIONAL: european fictional scimitar/bow weapons (fantasy register; named_template; N=107)
- **Override applied:** No
- **Framing-audit notes:** Low lineage purity 0.5140 — secondary lineage absorption. Substrate-honest fictional european scimitar cluster but with significant cross-lineage drift.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 48 (for Phase E-2-DB UPDATE clause)

### Cluster 48 — Fantasy-Generic Fictional Rifle Named-Item Family

- **Pool count:** N=68 (hdbscan_native subsample: 16; lineage purity 0.9265)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Burnside Rifle; Sporting Rifle; Barrel-Blade Longrifle
- **Provisional description:** PROVISIONAL: fantasy_generic classical rifle/shotgun weapons (fantasy register; named_template; N=68)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 4/5 top hdbscan_native reps contain 'rifle' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 49 (for Phase E-2-DB UPDATE clause)

### Cluster 49 — Fantasy-Generic Fictional Rifle Named-Item Family

- **Pool count:** N=68 (hdbscan_native subsample: 14; lineage purity 0.9853)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Bloodhound's Immobiliser Rifle; Bloodshot Rifle (very rare variant); Bloodwork Sniper Rifle
- **Provisional description:** PROVISIONAL: fantasy_generic fictional rifle/axe weapons (fantasy register; named_template; N=68)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 4/5 top hdbscan_native reps contain 'rifle' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 50 (for Phase E-2-DB UPDATE clause)

### Cluster 50 — European Contemporary Two-Hand Mixed Pool (Mil-Modern + Reproduction Blade)

- **Pool count:** N=1907 (hdbscan_native subsample: 413; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** european / contemporary / military_modern / category / two_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** zweihänder; zweihänder; hardened steel kriegsmesser
- **Provisional description:** PROVISIONAL: european contemporary bow weapons (military_modern register; category; N=1907)
- **Override applied:** Yes — Provisional 'bow' contradicted by top hdbscan_native reps: zweihänder ×2 + hardened steel kriegsmesser + Zhakh-15 Ukrainian UAV + Chuyka 3.0 drone detector. Cluster mixes contemporary military_modern hardware (Ukrainian drones/detectors) with category-tagged reproduction two-handed swords (zweihänder/kriegsmesser tagged 'contemporary military_modern'). Provisional-description weapon-type generator likely fired on a sparse weapon_type field.
- **Framing-audit notes:** Substrate-honest axis-coherent (European + contemporary + military_modern + two-hand) but weapon-form-heterogeneous. The zweihänder + kriegsmesser rows are tagged as contemporary military_modern apparently because they were imported from a modern reproduction catalogue; this is a substrate-tagging artifact that the cluster faithfully captures.
- **Special-case flags:** provisional_description_overridden, mixed_form_within_cluster, modern_military_hardware, labeling_pipeline_bug_surfaced
- **Phase E-3/E-4 hand-off notes:** Cluster surfaced by Gate-2 Question A.2 as the canonical example of labeling-pipeline bug. Phase E-1.5 sensitivity sweep should split reproduction-blade rows from drone/UAV rows. elrond review of zweihänder/kriegsmesser period+register tagging warranted.
- **DB cluster id:** 51 (for Phase E-2-DB UPDATE clause)

### Cluster 51 — Fantasy-Generic Fictional Mace Named-Item Family

- **Pool count:** N=75 (hdbscan_native subsample: 16; lineage purity 0.9867)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Mace of the Black Crown; Mace of the Black Crown, Dormant; High Warlord's Battle Mace
- **Provisional description:** PROVISIONAL: fantasy_generic classical mace/club weapons (fantasy register; named_template; N=75)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'mace' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 52 (for Phase E-2-DB UPDATE clause)

### Cluster 52 — Fantasy-Generic "Chicken Chucker / Arrow" Named-Item Family

- **Pool count:** N=1819 (hdbscan_native subsample: 365; lineage purity 0.9956)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Arrow of Teleportation; Assassin's Arrow; Chicken Chucker (Common)
- **Provisional description:** PROVISIONAL: fantasy_generic classical spear/musket weapons (fantasy register; named_template; N=1819)
- **Override applied:** Yes — Provisional 'spear/musket' contradicted by reps (Arrow of Teleportation + Assassin's Arrow + Chicken Chucker — fantasy-named arrows/thrown items with classical-period tagging).
- **Framing-audit notes:** Large named-template cluster (N=1819) bundling classical-period fantasy named projectiles/thrown items. Mixed signature between arrows and chicken-chucker variants.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 53 (for Phase E-2-DB UPDATE clause)

### Cluster 53 — Fantasy-Generic Fictional Bow Family

- **Pool count:** N=161 (hdbscan_native subsample: 32; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Bow of Grounding; Glaive; Halberd
- **Provisional description:** PROVISIONAL: fantasy_generic fictional bow/hammer weapons (fantasy register; category; N=161)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 1.0); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 54 (for Phase E-2-DB UPDATE clause)

### Cluster 54 — Fantasy-Generic Fictional Axe Family

- **Pool count:** N=85 (hdbscan_native subsample: 19; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Flail; Myrnaxe; Rapier of Defense
- **Provisional description:** PROVISIONAL: fantasy_generic fictional axe/rapier weapons (fantasy register; category; N=85)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 1.0); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 55 (for Phase E-2-DB UPDATE clause)

### Cluster 55 — Fantasy-Generic Fictional Mixed Named-Item Pool

- **Pool count:** N=65 (hdbscan_native subsample: 19; lineage purity 0.8462)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Composite Bow; Lichslayer Halberd (rare variant); Lichslayer Longbow
- **Provisional description:** PROVISIONAL: fantasy_generic classical sword/bow weapons (fantasy register; named_template; N=65)
- **Override applied:** No
- **Framing-audit notes:** Mixed named-template cluster; neither weapon-form nor name-prefix dominates top-5 reps. Coarse-spine label.
- **Special-case flags:** mixed_form_within_cluster
- **DB cluster id:** 56 (for Phase E-2-DB UPDATE clause)

### Cluster 56 — Fantasy-Generic Fictional Axe Named-Item Family

- **Pool count:** N=117 (hdbscan_native subsample: 21; lineage purity 0.9829)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Nine Lives Stealer Flail; Angerforge's Battle Axe; Colossal Great Axe
- **Provisional description:** PROVISIONAL: fantasy_generic classical axe/rapier weapons (fantasy register; named_template; N=117)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 4/5 top hdbscan_native reps contain 'axe' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 57 (for Phase E-2-DB UPDATE clause)

### Cluster 57 — Fantasy-Generic Fictional Mace Named-Item Family

- **Pool count:** N=160 (hdbscan_native subsample: 29; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Mace (rare variant); Cobra Mace (Common); Enspelled Mace (Level 1)
- **Provisional description:** PROVISIONAL: fantasy_generic fictional mace/staff weapons (fantasy register; named_template; N=160)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'mace' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 58 (for Phase E-2-DB UPDATE clause)

### Cluster 58 — East Asian-Tagged Industrial Pistol Pool (Mixed)

- **Pool count:** N=76 (hdbscan_native subsample: 14; lineage purity 0.5132)
- **Dominant lineage / period / register / kind / wield:** east_asian / industrial / historical / category / one_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Decorated shield; Centrefire self-loading military pistol; Type 64 pistol
- **Provisional description:** PROVISIONAL: east_asian industrial pistol/knife weapons (historical register; category; N=76)
- **Override applied:** No
- **Framing-audit notes:** Low lineage purity 0.5132 — cluster has substantial secondary lineage content. Coarse-spine label retains dominant tagging with mixed flag.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 59 (for Phase E-2-DB UPDATE clause)

### Cluster 59 — Fantasy-Generic Fictional Mixed Named-Item Pool

- **Pool count:** N=129 (hdbscan_native subsample: 26; lineage purity 0.9147)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Hammer of Thunderbolts (Template); Nine Lives Stealer Light Hammer; Inlaid Thorium Hammer
- **Provisional description:** PROVISIONAL: fantasy_generic classical hammer/pike weapons (fantasy register; named_template; N=129)
- **Override applied:** No
- **Framing-audit notes:** Mixed named-template cluster; neither weapon-form nor name-prefix dominates top-5 reps. Coarse-spine label.
- **Special-case flags:** mixed_form_within_cluster
- **DB cluster id:** 60 (for Phase E-2-DB UPDATE clause)

### Cluster 60 — Fantasy-Generic Fictional Longbow Named-Item Family

- **Pool count:** N=127 (hdbscan_native subsample: 20; lineage purity 0.9921)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / classical / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Infernal Longbow; Nine Lives Stealer Shortbow; Gryphonwing Long Bow
- **Provisional description:** PROVISIONAL: fantasy_generic classical bow/glaive weapons (fantasy register; named_template; N=127)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 3/5 top hdbscan_native reps contain 'longbow' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 61 (for Phase E-2-DB UPDATE clause)

### Cluster 61 — Fantasy-Generic Fictional Spear Named-Item Family

- **Pool count:** N=272 (hdbscan_native subsample: 52; lineage purity 0.9926)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Consecrated Weapon Spear; Dornish Horse Spear; Enspelled Spear (Level 1)
- **Provisional description:** PROVISIONAL: fantasy_generic fictional spear/scimitar weapons (fantasy register; named_template; N=272)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'spear' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 62 (for Phase E-2-DB UPDATE clause)

### Cluster 62 — Fantasy-Generic "Abyssal Bane" Named-Template Mega-Family

- **Pool count:** N=4807 (hdbscan_native subsample: 1017; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Chakram (very rare variant); Abyssal Bane Knuckle Duster (rare variant); Abyssal Bane Knuckle Duster (very rare variant)
- **Provisional description:** PROVISIONAL: fantasy_generic fictional axe/greataxe weapons (fantasy register; named_template; N=4807)
- **Override applied:** Yes — Provisional 'axe/greataxe' contradicted by reps — the entire 'Abyssal Bane' fantasy item-template family bundles across weapon-forms (chakram, knuckle-duster, maul, nunchaku, etc.) into one cluster because axis-1 (kind_named_template + fantasy_generic + register_fantasy + period_fictional) dominates over weapon-shape signal at k=3.
- **Framing-audit notes:** Gate-2 Question B canonical example: largest fantasy_generic cluster (N=4807) bundles the Abyssal Bane named-item family across weapon-forms. Substrate-honest at k=3 axes but weapon-form-resolution-deferred to Phase E-1.5 sensitivity sweep.
- **Special-case flags:** provisional_description_overridden, fantasy_named_template_cross_form, phase_e15_split_candidate
- **Phase E-3/E-4 hand-off notes:** Phase E-1.5 sensitivity sweep at higher k should split this mega-family along weapon-form lines; Phase E-2-DB label is the coarse-spine canonical reference.
- **DB cluster id:** 63 (for Phase E-2-DB UPDATE clause)

### Cluster 63 — European Industrial Decorative/Mixed-Form Pool

- **Pool count:** N=187 (hdbscan_native subsample: 40; lineage purity 0.8396)
- **Dominant lineage / period / register / kind / wield:** european / industrial / historical / category / one_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Parade shield; Shield Depicting Saint George Slaying the Dragon; Smith & Wesson 7-shot revolver of 1874
- **Provisional description:** PROVISIONAL: european industrial sword/mace weapons (historical register; category; N=187)
- **Override applied:** Yes — Provisional 'sword/mace' contradicted by reps (parade shield + Saint George shield + Smith & Wesson revolver). Cluster mixes ceremonial shields + industrial-period revolvers under axis-coherent industrial+european positioning.
- **Framing-audit notes:** Substrate-honest but weapon-form-heterogeneous; the cluster includes decorated shields + pistols that share axis-position despite not sharing form. Coarse-spine label.
- **Special-case flags:** provisional_description_overridden, mixed_form_within_cluster
- **DB cluster id:** 64 (for Phase E-2-DB UPDATE clause)

### Cluster 64 — Fantasy-Generic Fictional Musket Named-Item Family

- **Pool count:** N=59 (hdbscan_native subsample: 11; lineage purity 0.8814)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Bloodhound's Immobiliser Musket (very rare variant); Bloodshot Musket (very rare variant); Deepshot Musket (rare variant)
- **Provisional description:** PROVISIONAL: fantasy_generic fictional musket/bow weapons (fantasy register; named_template; N=59)
- **Override applied:** No
- **Framing-audit notes:** Form-bundled named-template cluster — 5/5 top hdbscan_native reps contain 'musket' as weapon-form signal. Cluster identity is weapon-form within fantasy named-template space.
- **Special-case flags:** none
- **DB cluster id:** 65 (for Phase E-2-DB UPDATE clause)

### Cluster 65 — Fantasy-Generic Fictional Mixed Named-Item Pool

- **Pool count:** N=232 (hdbscan_native subsample: 47; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** fantasy_generic / fictional / fantasy / named_template / two_hand
- **Cluster type:** `named_template_family`
- **Top-3 hdbscan_native representatives:** Abyssal Bane Greatclub; Club of Inverted Probability; Consecrated Weapon Club
- **Provisional description:** PROVISIONAL: fantasy_generic fictional club weapons (fantasy register; named_template; N=232)
- **Override applied:** No
- **Framing-audit notes:** Mixed named-template cluster; neither weapon-form nor name-prefix dominates top-5 reps. Coarse-spine label.
- **Special-case flags:** mixed_form_within_cluster
- **DB cluster id:** 66 (for Phase E-2-DB UPDATE clause)

### Cluster 66 — Untyped-Lineage Ceremonial-Shield Pool

- **Pool count:** N=103 (hdbscan_native subsample: 20; lineage purity 0.4078)
- **Dominant lineage / period / register / kind / wield:** unknown / unknown / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Ceremonial shield with mosaic decoration.; Gweagal shield; Garibaldi shield
- **Provisional description:** PROVISIONAL: unknown unknown pistol/sword weapons (historical register; category; N=103)
- **Override applied:** Yes — Provisional 'pistol/sword' contradicted by reps (ceremonial shield + Gweagal shield (Aboriginal) + Garibaldi shield (Italian) + Hylian shield (fantasy) + hunting-vignette shield). Cluster is a cross-cultural ceremonial-shield pool whose lineage is untyped in substrate metadata.
- **Framing-audit notes:** Substrate-honest cluster identity is 'ceremonial / decorated shield' across uncurated lineage tagging. Coarse-spine label honors form (shield) and acknowledges lineage gap.
- **Special-case flags:** provisional_description_overridden, lineage_uncurated
- **Phase E-3/E-4 hand-off notes:** elrond: lineage_unknown shield entries warrant lineage curation pass.
- **DB cluster id:** 67 (for Phase E-2-DB UPDATE clause)

### Cluster 67 — European Modern Sword-Adjacent Component Pool

- **Pool count:** N=238 (hdbscan_native subsample: 39; lineage purity 0.5966)
- **Dominant lineage / period / register / kind / wield:** european / modern / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Bayonet; Cross-guard; Pricker
- **Provisional description:** PROVISIONAL: european modern sword/dagger weapons (historical register; category; N=238)
- **Override applied:** Yes — Provisional 'sword/dagger' partially-correct but reps reveal cluster is sword-adjacent components/auxiliaries: bayonet, cross-guard (a sword part), pricker (small awl-like tool). The cluster is sword-adjacent rather than swords-proper.
- **Framing-audit notes:** Lineage purity 0.5966 — secondary lineage contribution. Reps surface a substrate-tagging issue where sword components are tagged 'sword' weapon_type.
- **Special-case flags:** provisional_description_overridden, low_lineage_purity
- **DB cluster id:** 68 (for Phase E-2-DB UPDATE clause)

### Cluster 68 — Cross-Cultural Contemporary Mixed-Munitions Pool

- **Pool count:** N=502 (hdbscan_native subsample: 118; lineage purity 0.8785)
- **Dominant lineage / period / register / kind / wield:** cross_cultural / contemporary / military_modern / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Assault SMG; Tear Gas; Missiles
- **Provisional description:** PROVISIONAL: cross_cultural contemporary shotgun/rifle weapons (military_modern register; category; N=502)
- **Override applied:** Yes — Provisional 'shotgun/rifle' contradicted by reps (assault SMG + tear gas + missiles). Cluster is a contemporary mixed-munitions pool with cross-cultural lineage.
- **Framing-audit notes:** Largest cross-cultural cluster (N=502). Includes oceanic absorption per Gate-2 Question C. Coarse-spine label reflects mixed-munitions identity.
- **Special-case flags:** provisional_description_overridden, absorbs_rare_lineage_rows, modern_military_hardware
- **DB cluster id:** 69 (for Phase E-2-DB UPDATE clause)

### Cluster 69 — European Contemporary Assault-Rifle Pool

- **Pool count:** N=77 (hdbscan_native subsample: 22; lineage purity 0.7792)
- **Dominant lineage / period / register / kind / wield:** european / contemporary / military_modern / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** SL8 civilian rifle; AK-203 Russian 7.62mm Assault Rifle; Hopak-61 Ukrainian 7.62mm Assault Rifle
- **Provisional description:** PROVISIONAL: european contemporary rifle/musket weapons (military_modern register; category; N=77)
- **Override applied:** No
- **Framing-audit notes:** Provisional 'rifle/musket' matches reps (SL8 + AK-203 + Hopak-61 + Colt CM901 + Beretta ARX-160). 7 n.am.indigenous rows ride along (Gate-2 Question C); these are non-canonical lineage absorption — see canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md. The 'european contemporary rifle' label is honest about the dominant cluster identity; n.am.indigenous rows are not canonically labeled here.
- **Special-case flags:** absorbs_rare_lineage_rows, n_am_indigenous_passenger
- **Phase E-3/E-4 hand-off notes:** Cross-reference recognition record: 7 n.am.indigenous rows in this cluster do NOT canonically label this as n.am.indigenous.
- **DB cluster id:** 70 (for Phase E-2-DB UPDATE clause)

### Cluster 70 — European-Tagged Contemporary Spear Pool (Mixed)

- **Pool count:** N=77 (hdbscan_native subsample: 16; lineage purity 0.5584)
- **Dominant lineage / period / register / kind / wield:** european / contemporary / military_modern / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** fire-hardened wooden spear; hardened steel spear; tempered steel spear
- **Provisional description:** PROVISIONAL: european contemporary lance/spear weapons (military_modern register; category; N=77)
- **Override applied:** No
- **Framing-audit notes:** Low lineage purity 0.5584 — cluster has substantial secondary lineage content. Coarse-spine label retains dominant tagging with mixed flag.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 71 (for Phase E-2-DB UPDATE clause)

### Cluster 71 — Middle Eastern Contemporary UAV/Drone Pool

- **Pool count:** N=423 (hdbscan_native subsample: 93; lineage purity 0.9787)
- **Dominant lineage / period / register / kind / wield:** middle_eastern / contemporary / military_modern / category / two_hand
- **Cluster type:** `modern_military_hardware_pool`
- **Top-3 hdbscan_native representatives:** Shahed-238 Iranian Unmanned Aerial Vehicle (UAV); Shahed-136 Iranian Unmanned Aerial Vehicle (UAV); Shahed-131 Iranian Unmanned Aerial Vehicle (UAV)
- **Provisional description:** PROVISIONAL: middle_eastern contemporary club/spear weapons (military_modern register; category; N=423)
- **Override applied:** Yes — Provisional 'club/spear' contradicted by reps (Shahed-238 + Shahed-136 + Shahed-131 — all Iranian UAVs). Cluster is contemporary Iranian-origin UAV systems.
- **Framing-audit notes:** Substrate-coherent middle_eastern contemporary cluster; weapon-form is UAV/drone rather than club/spear. Lineage tagging via geographic origin (Iran).
- **Special-case flags:** provisional_description_overridden, modern_military_hardware
- **DB cluster id:** 72 (for Phase E-2-DB UPDATE clause)

### Cluster 72 — European Industrial Pistol Family

- **Pool count:** N=327 (hdbscan_native subsample: 56; lineage purity 0.7645)
- **Dominant lineage / period / register / kind / wield:** european / industrial / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Dagger with Rock Crystal and Garnet  Handle (modern forgery); Percussion pocket pistol; Percussion cavalry pistol
- **Provisional description:** PROVISIONAL: european industrial pistol/dagger weapons (historical register; category; N=327)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.7645); 4/5 reps confirm 'pistol' form.
- **Special-case flags:** none
- **DB cluster id:** 73 (for Phase E-2-DB UPDATE clause)

### Cluster 73 — European Early-Modern Pistol Family

- **Pool count:** N=315 (hdbscan_native subsample: 72; lineage purity 0.8857)
- **Dominant lineage / period / register / kind / wield:** european / early_modern / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Pair of Flintlock Pistols of Empress Catherine the Great (1729–1796); Pistol of the Gendarmes de la Maison du Roi model 1750-Musée de l'Armée on display 4; Pistol of the Gendarmes de la Maison du Roi model 1763-Musée de l'Armée on display 5
- **Provisional description:** PROVISIONAL: european early_modern pistol/knife weapons (historical register; category; N=315)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.8857); 4/5 reps confirm 'pistol' form.
- **Special-case flags:** none
- **DB cluster id:** 74 (for Phase E-2-DB UPDATE clause)

### Cluster 74 — Southeast Asian Early-Modern Dagger Pool (Mixed)

- **Pool count:** N=115 (hdbscan_native subsample: 23; lineage purity 0.3043)
- **Dominant lineage / period / register / kind / wield:** southeast_asian / early_modern / historical / category / one_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Flint Dagger from Denmark; Dagger; Dagger (Jambiya) with Sheath
- **Provisional description:** PROVISIONAL: southeast_asian early_modern dagger/knife weapons (historical register; category; N=115)
- **Override applied:** No
- **Framing-audit notes:** Very low lineage purity 0.3043 — cluster is substrate-mixed across lineages. Coarse-spine label retains dominant tagging but flags low-purity.
- **Special-case flags:** low_lineage_purity
- **Phase E-3/E-4 hand-off notes:** Cluster purity below the 0.70 acceptance gate at per-cluster level; reviewable in Phase E-1.5.
- **DB cluster id:** 75 (for Phase E-2-DB UPDATE clause)

### Cluster 75 — South Asian Early-Modern Dagger Family

- **Pool count:** N=76 (hdbscan_native subsample: 16; lineage purity 0.75)
- **Dominant lineage / period / register / kind / wield:** south_asian / early_modern / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Dagger with Hilt in the Form of a Blue Bull (Nilgai); Dagger (katar); Dagger with Sheath
- **Provisional description:** PROVISIONAL: south_asian early_modern dagger/knife weapons (historical register; category; N=76)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.75); 5/5 reps confirm 'dagger' form.
- **Special-case flags:** none
- **DB cluster id:** 76 (for Phase E-2-DB UPDATE clause)

### Cluster 76 — European Early-Modern Sword Family

- **Pool count:** N=183 (hdbscan_native subsample: 47; lineage purity 0.7705)
- **Dominant lineage / period / register / kind / wield:** european / early_modern / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Sword hilt; Sword (talwar); Sword hanger
- **Provisional description:** PROVISIONAL: european early_modern sword/rapier weapons (historical register; category; N=183)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.7705); 4/5 reps confirm 'sword' form.
- **Special-case flags:** none
- **DB cluster id:** 77 (for Phase E-2-DB UPDATE clause)

### Cluster 77 — Untyped-Lineage Early-Firearm/Shield Mixed Pool

- **Pool count:** N=65 (hdbscan_native subsample: 20; lineage purity 0.6462)
- **Dominant lineage / period / register / kind / wield:** unknown / unknown / historical / category / one_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Ottoman cavalry shield; Pistola de Pederneira; Pistola de Pederneira Transformada em Percussão
- **Provisional description:** PROVISIONAL: unknown unknown pistol/knife weapons (historical register; category; N=65)
- **Override applied:** Yes — Provisional 'pistol/sword' partially-correct but reps reveal cluster mixes Ottoman cavalry shield + Portuguese pistola de pederneira (flintlock) + flintlock-to-percussion conversions.
- **Framing-audit notes:** Untyped-lineage cluster bundling early firearms + shield forms.
- **Special-case flags:** provisional_description_overridden, lineage_uncurated
- **DB cluster id:** 78 (for Phase E-2-DB UPDATE clause)

### Cluster 78 — European Early-Modern Mixed Edged/Hafted Pool

- **Pool count:** N=311 (hdbscan_native subsample: 59; lineage purity 0.9518)
- **Dominant lineage / period / register / kind / wield:** european / early_modern / historical / category / one_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Hanger; Yataghan bayonet for Martini Henry; Palstave
- **Provisional description:** PROVISIONAL: european early_modern pistol/knife weapons (historical register; category; N=311)
- **Override applied:** Yes — Provisional 'pistol/knife' contradicted by reps (hanger + yataghan bayonet for Martini Henry + palstave (a bronze-age axe)). The palstave inclusion is a period-tagging artifact; cluster mixes early-modern edged + hafted forms with a bronze-age intruder.
- **Framing-audit notes:** Cluster substrate-coherent at axis-level but includes palstave (bronze-age) — likely a period-canonicalization gap where pre_classical items received early_modern tagging.
- **Special-case flags:** provisional_description_overridden, period_tag_likely_metadata_artifact
- **Phase E-3/E-4 hand-off notes:** elrond: palstave-style pre-classical items mis-tagged early_modern warrant period-canonicalization review.
- **DB cluster id:** 79 (for Phase E-2-DB UPDATE clause)

### Cluster 79 — European Modern Pistol Family

- **Pool count:** N=116 (hdbscan_native subsample: 23; lineage purity 0.9569)
- **Dominant lineage / period / register / kind / wield:** european / modern / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Centrefire self-loading military pistol; Rimfire breech-loading target pistol; Rimfire breech-loading double-barrelled pistol
- **Provisional description:** PROVISIONAL: european modern pistol/dagger weapons (historical register; category; N=116)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9569); 5/5 reps confirm 'pistol' form.
- **Special-case flags:** none
- **DB cluster id:** 80 (for Phase E-2-DB UPDATE clause)

### Cluster 80 — Southeast Asian Early-Modern Knife Family

- **Pool count:** N=192 (hdbscan_native subsample: 38; lineage purity 0.6302)
- **Dominant lineage / period / register / kind / wield:** southeast_asian / early_modern / historical / category / one_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Hunting Knife; Kris with Sheath; Shield
- **Provisional description:** PROVISIONAL: southeast_asian early_modern knife/dagger weapons (historical register; category; N=192)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 0.6302); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 81 (for Phase E-2-DB UPDATE clause)

### Cluster 81 — East Asian Contemporary Rifle Family

- **Pool count:** N=250 (hdbscan_native subsample: 57; lineage purity 0.972)
- **Dominant lineage / period / register / kind / wield:** east_asian / contemporary / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** shotgun Lee-Enfield (Museu Militar da Madeira); Electroshock torch; Al-Samoud 2
- **Provisional description:** PROVISIONAL: east_asian contemporary rifle/shotgun weapons (historical register; category; N=250)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 0.972); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 82 (for Phase E-2-DB UPDATE clause)

### Cluster 82 — Southeast Asian-Tagged Contemporary Mixed-Form Pool

- **Pool count:** N=104 (hdbscan_native subsample: 13; lineage purity 0.5288)
- **Dominant lineage / period / register / kind / wield:** southeast_asian / contemporary / historical / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Jungle carbine; GKN Simba; F1 submachine gun
- **Provisional description:** PROVISIONAL: southeast_asian contemporary rifle weapons (historical register; category; N=104)
- **Override applied:** Yes — Provisional weapon-form 'rifle' refined from rep evidence; dominant rep-form is 'carbine' (1/5).
- **Framing-audit notes:** Low lineage purity 0.5288 — cluster has substantial secondary lineage content. Coarse-spine label retains dominant tagging with mixed flag. Provisional weapon-form 'rifle' not present in top-3 hdbscan_native reps.
- **Special-case flags:** mixed_form_within_cluster, low_lineage_purity, provisional_description_overridden
- **DB cluster id:** 83 (for Phase E-2-DB UPDATE clause)

### Cluster 83 — South Asian Contemporary Sword Family

- **Pool count:** N=33 (hdbscan_native subsample: 19; lineage purity 0.6667)
- **Dominant lineage / period / register / kind / wield:** south_asian / contemporary / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Mission Shakti; Polaris Inc.; FN MAG
- **Provisional description:** PROVISIONAL: south_asian contemporary sword/rapier weapons (historical register; category; N=33)
- **Override applied:** Yes — Provisional weapon-form 'sword/rapier' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.6667); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'sword/rapier' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 84 (for Phase E-2-DB UPDATE clause)

### Cluster 84 — European Contemporary Spear Family

- **Pool count:** N=734 (hdbscan_native subsample: 151; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** european / contemporary / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Catapult; Percussion six-shot replica revolver; Belt buckle knuckle duster
- **Provisional description:** PROVISIONAL: european contemporary spear/hammer weapons (historical register; category; N=734)
- **Override applied:** Yes — Provisional weapon-form 'spear/hammer' refined from rep evidence; dominant rep-form is 'revolver' (2/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 1.0); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'spear/hammer' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 85 (for Phase E-2-DB UPDATE clause)

### Cluster 85 — African Contemporary Musket Family

- **Pool count:** N=44 (hdbscan_native subsample: 11; lineage purity 0.8864)
- **Dominant lineage / period / register / kind / wield:** african / contemporary / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Mamba APC; Vektor CR-21; Denel NTW-20
- **Provisional description:** PROVISIONAL: african contemporary musket/lance weapons (historical register; category; N=44)
- **Override applied:** Yes — Provisional weapon-form 'musket/lance' refined from rep evidence; dominant rep-form is 'apc' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.8864); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'musket/lance' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 86 (for Phase E-2-DB UPDATE clause)

### Cluster 86 — S. American Indigenous Contemporary Shotgun Cluster

- **Pool count:** N=36 (hdbscan_native subsample: 15; lineage purity 0.9444)
- **Dominant lineage / period / register / kind / wield:** south_american_indigenous / contemporary / historical / category / two_hand
- **Cluster type:** `rare_lineage_isolate`
- **Top-3 hdbscan_native representatives:** FAMAE SAF; LAHAT; Taurus Millennium series
- **Provisional description:** PROVISIONAL: south_american_indigenous contemporary shotgun/rifle weapons (historical register; category; N=36)
- **Override applied:** No
- **Framing-audit notes:** Rare-lineage substrate-led cluster (purity 0.9444, N=36); genuine S. American Indigenous contemporary firearms isolate. Substrate-honest rare-lineage representation per Gate-2 Question C.
- **Special-case flags:** rare_lineage_substrate_isolate
- **DB cluster id:** 87 (for Phase E-2-DB UPDATE clause)

### Cluster 87 — Untyped-Lineage Fantasy/Modern Improvised Pool

- **Pool count:** N=190 (hdbscan_native subsample: 41; lineage purity 0.8105)
- **Dominant lineage / period / register / kind / wield:** unknown / contemporary / historical / category / two_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Flushomatic; Nail Gun; Photon Projector
- **Provisional description:** PROVISIONAL: unknown contemporary shotgun/rifle weapons (historical register; category; N=190)
- **Override applied:** Yes — Provisional 'shotgun' contradicted by reps (flushomatic, nail gun, photon projector, ICER, bad rabbit). Cluster mixes improvised weapons + sci-fi tools + named gadgets under untyped lineage.
- **Framing-audit notes:** Substrate-honest untyped-lineage contemporary cluster; reps show improvised/named gadget pool. Coarse-spine label.
- **Special-case flags:** provisional_description_overridden, lineage_uncurated
- **DB cluster id:** 88 (for Phase E-2-DB UPDATE clause)

### Cluster 88 — European Contemporary Rifle Family

- **Pool count:** N=63 (hdbscan_native subsample: 13; lineage purity 0.9365)
- **Dominant lineage / period / register / kind / wield:** european / contemporary / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Centrefire automatic rifle; Air rifle; SEAL Recon Rifle
- **Provisional description:** PROVISIONAL: european contemporary rifle weapons (historical register; category; N=63)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9365); 5/5 reps confirm 'rifle' form.
- **Special-case flags:** none
- **DB cluster id:** 89 (for Phase E-2-DB UPDATE clause)

### Cluster 89 — Middle Eastern Contemporary Spear Family

- **Pool count:** N=211 (hdbscan_native subsample: 44; lineage purity 0.8957)
- **Dominant lineage / period / register / kind / wield:** middle_eastern / contemporary / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Spearhead; Spearhead; Qassam rocket
- **Provisional description:** PROVISIONAL: middle_eastern contemporary spear/mace weapons (historical register; category; N=211)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 0.8957); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 90 (for Phase E-2-DB UPDATE clause)

### Cluster 90 — East Asian Uncurated-Period Metadata Pool

- **Pool count:** N=10087 (hdbscan_native subsample: 2040; lineage purity 1.0)
- **Dominant lineage / period / register / kind / wield:** east_asian / unknown / historical / category / two_hand
- **Cluster type:** `metadata_bucket`
- **Top-3 hdbscan_native representatives:** H/AKJ-16; Q132210441; Teppô
- **Provisional description:** PROVISIONAL: east_asian unknown rifle/spear weapons (historical register; category; N=10087)
- **Override applied:** Yes — Provisional 'rifle/spear' contradicted by reps (alphanumeric catalog IDs: H/AKJ-16, Q132210441, Q132526367, Q132526368; plus romaji 'Teppô'). 10,087 rows (77% of east_asian pool) collapsed into single uncurated-period bucket. Per Gate-2 Question A.1, this is NOT a coherent weapon family — it is the Phase-D-bis east_asian period_unknown metadata residue.
- **Framing-audit notes:** Canonical metadata-bucket cluster (Gate-2 Question A.1, dispatch § 2). Do NOT retro-fit weapon-design narrative onto this cluster. Cluster reflects uncurated metadata, not weapon coherence.
- **Special-case flags:** metadata_bucket, phase_d_bis_curation_gap
- **Phase E-3/E-4 hand-off notes:** Sub-carry 9.11-C: elrond Phase-D-bis Step 6.6.c-adjacent review of east_asian period_unknown rows (~10K) for additional curation. Non-blocking for Phase E-2.
- **DB cluster id:** 91 (for Phase E-2-DB UPDATE clause)

### Cluster 91 — South Asian-Tagged Early-Modern Mixed-Form Pool

- **Pool count:** N=161 (hdbscan_native subsample: 25; lineage purity 0.528)
- **Dominant lineage / period / register / kind / wield:** south_asian / early_modern / historical / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Malik-E-Maidan; Mysorean rockets; Quiver, Belt, and Twenty Arrows
- **Provisional description:** PROVISIONAL: south_asian early_modern sword/spear weapons (historical register; category; N=161)
- **Override applied:** Yes — Provisional weapon-form 'sword/spear' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Low lineage purity 0.528 — cluster has substantial secondary lineage content. Coarse-spine label retains dominant tagging with mixed flag. Provisional weapon-form 'sword/spear' not present in top-3 hdbscan_native reps.
- **Special-case flags:** mixed_form_within_cluster, low_lineage_purity, provisional_description_overridden
- **DB cluster id:** 92 (for Phase E-2-DB UPDATE clause)

### Cluster 92 — Untyped-Lineage Early-Modern Mixed Pool

- **Pool count:** N=92 (hdbscan_native subsample: 13; lineage purity 0.5435)
- **Dominant lineage / period / register / kind / wield:** unknown / early_modern / historical / category / two_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Ceremonial ax; Early bayonet-Arm B 259; Q106379646
- **Provisional description:** PROVISIONAL: unknown early_modern lance/shotgun weapons (historical register; category; N=92)
- **Override applied:** Yes — Provisional 'lance' contradicted by reps (ceremonial ax + early bayonet-arm + Q-number + firebomb + chatan nakiri — Okinawan knife). Cluster mixes mostly-unidentified early-modern items.
- **Framing-audit notes:** Lineage purity 0.5435; substrate-honest untyped-lineage early-modern cluster with heterogeneous reps including raw Q-numbers (Wikidata IDs that lack canonical-name curation).
- **Special-case flags:** provisional_description_overridden, lineage_uncurated, low_lineage_purity
- **Phase E-3/E-4 hand-off notes:** elrond: raw Wikidata Q-number canonical_names indicate name-curation gap.
- **DB cluster id:** 93 (for Phase E-2-DB UPDATE clause)

### Cluster 93 — East Asian Early-Modern Musket Family

- **Pool count:** N=380 (hdbscan_native subsample: 69; lineage purity 0.8)
- **Dominant lineage / period / register / kind / wield:** east_asian / early_modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Flintlock musketoon; Percussion military musket; Centrefire breech-loading military carbine
- **Provisional description:** PROVISIONAL: east_asian early_modern musket/sword weapons (historical register; category; N=380)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 0.8); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 94 (for Phase E-2-DB UPDATE clause)

### Cluster 94 — European Early-Modern Sabre Family

- **Pool count:** N=164 (hdbscan_native subsample: 33; lineage purity 0.6463)
- **Dominant lineage / period / register / kind / wield:** european / early_modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Boarding sabre, model called "Louvois"; Garde nationale sabre with lion and panoply; Garde nationale sabre with lion, phrygian hat and fasces
- **Provisional description:** PROVISIONAL: european early_modern rifle/sabre weapons (historical register; category; N=164)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.6463); 5/5 reps confirm 'sabre' form.
- **Special-case flags:** none
- **DB cluster id:** 95 (for Phase E-2-DB UPDATE clause)

### Cluster 95 — European Early-Modern Spear Family

- **Pool count:** N=1305 (hdbscan_native subsample: 236; lineage purity 0.9985)
- **Dominant lineage / period / register / kind / wield:** european / early_modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Weapons of Honour; Wheel-lock Petronel; Detached flintlock lock
- **Provisional description:** PROVISIONAL: european early_modern spear/rifle weapons (historical register; category; N=1305)
- **Override applied:** Yes — Provisional weapon-form 'spear/rifle' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9985); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'spear/rifle' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 96 (for Phase E-2-DB UPDATE clause)

### Cluster 96 — European-Tagged Early-Modern Halberd Pool (Mixed)

- **Pool count:** N=187 (hdbscan_native subsample: 37; lineage purity 0.5936)
- **Dominant lineage / period / register / kind / wield:** european / early_modern / historical / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Steel bow; Glaive of the Bodyguard of Guglielmo Gonzaga (1538–1587), Duke of Mantua and Monferrato; Halberd of Wolf Dietrich von Raitenau, Prince-Archbishop of Salzburg (reigned 1587–1612)
- **Provisional description:** PROVISIONAL: european early_modern bow/crossbow weapons (historical register; category; N=187)
- **Override applied:** No
- **Framing-audit notes:** Low lineage purity 0.5936 — cluster has substantial secondary lineage content. Coarse-spine label retains dominant tagging with mixed flag.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 97 (for Phase E-2-DB UPDATE clause)

### Cluster 97 — East Asian Classical Sword Family

- **Pool count:** N=218 (hdbscan_native subsample: 35; lineage purity 0.9862)
- **Dominant lineage / period / register / kind / wield:** east_asian / classical / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Mace Head; S-300 missile system; AGM-122 Sidearm
- **Provisional description:** PROVISIONAL: east_asian classical sword/bow weapons (historical register; category; N=218)
- **Override applied:** Yes — Provisional weapon-form 'sword/bow' refined from rep evidence; dominant rep-form is 'mace' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9862); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'sword/bow' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 98 (for Phase E-2-DB UPDATE clause)

### Cluster 98 — South Asian-Tagged Industrial Mixed-Form Pool

- **Pool count:** N=107 (hdbscan_native subsample: 24; lineage purity 0.5981)
- **Dominant lineage / period / register / kind / wield:** south_asian / industrial / historical / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Iroquois club; Club; Medal
- **Provisional description:** PROVISIONAL: south_asian industrial spear/musket weapons (historical register; category; N=107)
- **Override applied:** Yes — Provisional weapon-form 'spear/musket' refined from rep evidence; dominant rep-form is 'club' (2/5).
- **Framing-audit notes:** Low lineage purity 0.5981 — cluster has substantial secondary lineage content. Coarse-spine label retains dominant tagging with mixed flag. Provisional weapon-form 'spear/musket' not present in top-3 hdbscan_native reps.
- **Special-case flags:** mixed_form_within_cluster, low_lineage_purity, provisional_description_overridden
- **DB cluster id:** 99 (for Phase E-2-DB UPDATE clause)

### Cluster 99 — European Early-Modern Musket Family

- **Pool count:** N=82 (hdbscan_native subsample: 16; lineage purity 0.9146)
- **Dominant lineage / period / register / kind / wield:** european / early_modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Flintlock muzzle-loading musket; Flintlock musket; Matchlock military musket
- **Provisional description:** PROVISIONAL: european early_modern musket/sabre weapons (historical register; category; N=82)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9146); 4/5 reps confirm 'musket' form.
- **Special-case flags:** none
- **DB cluster id:** 100 (for Phase E-2-DB UPDATE clause)

### Cluster 100 — African-Tagged Classical Bow Pool (Mixed)

- **Pool count:** N=144 (hdbscan_native subsample: 29; lineage purity 0.4861)
- **Dominant lineage / period / register / kind / wield:** african / classical / historical / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Panzerjäger I; FN 303; .460 Weatherby Magnum
- **Provisional description:** PROVISIONAL: african classical bow/halberd weapons (historical register; category; N=144)
- **Override applied:** No
- **Framing-audit notes:** Low lineage purity 0.4861. Coarse-spine.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 101 (for Phase E-2-DB UPDATE clause)

### Cluster 101 — Untyped-Lineage Industrial Catalog-Residue Pool

- **Pool count:** N=64 (hdbscan_native subsample: 17; lineage purity 0.5156)
- **Dominant lineage / period / register / kind / wield:** unknown / industrial / historical / category / two_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Boomerang; Q29341376; Q131904965
- **Provisional description:** PROVISIONAL: unknown industrial lance/rifle weapons (historical register; category; N=64)
- **Override applied:** Yes — Provisional 'lance' contradicted by reps (boomerang + Q29341376 + Q131904965 + 'Canon de l'armée russe' + Lantaka 1). Cluster bundles industrial-tagged items with significant raw Wikidata-ID residue.
- **Framing-audit notes:** Lineage purity 0.5156. Reps surface canonical-name gap (raw Q-numbers) and form-heterogeneity (boomerang + cannon + lantaka).
- **Special-case flags:** provisional_description_overridden, lineage_uncurated, low_lineage_purity
- **DB cluster id:** 102 (for Phase E-2-DB UPDATE clause)

### Cluster 102 — European Industrial Shotgun Family

- **Pool count:** N=56 (hdbscan_native subsample: 15; lineage purity 0.9107)
- **Dominant lineage / period / register / kind / wield:** european / industrial / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Percussion double-barrelled shotgun; Percussion shotgun; Centrefire breech-loading shotgun
- **Provisional description:** PROVISIONAL: european industrial shotgun/rifle weapons (historical register; category; N=56)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9107); 5/5 reps confirm 'shotgun' form.
- **Special-case flags:** none
- **DB cluster id:** 103 (for Phase E-2-DB UPDATE clause)

### Cluster 103 — African Uncurated-Period Mace Family

- **Pool count:** N=95 (hdbscan_native subsample: 22; lineage purity 0.9474)
- **Dominant lineage / period / register / kind / wield:** african / unknown / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Weapon; Weapon 2; Greek fire
- **Provisional description:** PROVISIONAL: african unknown mace weapons (historical register; category; N=95)
- **Override applied:** Yes — Provisional weapon-form 'mace' refined from rep evidence; dominant rep-form is 'mine' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9474); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'mace' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 104 (for Phase E-2-DB UPDATE clause)

### Cluster 104 — East Asian Modern Rifle Family

- **Pool count:** N=491 (hdbscan_native subsample: 96; lineage purity 0.9104)
- **Dominant lineage / period / register / kind / wield:** east_asian / modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Tumi; Catapulta salva-vidas; Atsu Tōshirō
- **Provisional description:** PROVISIONAL: east_asian modern rifle/spear weapons (historical register; category; N=491)
- **Override applied:** Yes — Provisional weapon-form 'rifle/spear' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9104); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'rifle/spear' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 105 (for Phase E-2-DB UPDATE clause)

### Cluster 105 — European-Tagged Classical Sword Pool (Mixed)

- **Pool count:** N=218 (hdbscan_native subsample: 47; lineage purity 0.3028)
- **Dominant lineage / period / register / kind / wield:** european / classical / historical / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Iron sword, National Museum in Damascus; Heaven Sword; Sword of Omens
- **Provisional description:** PROVISIONAL: european classical sword/hammer weapons (historical register; category; N=218)
- **Override applied:** No
- **Framing-audit notes:** Very low lineage purity 0.3028 — cluster has substantial secondary lineage content.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 106 (for Phase E-2-DB UPDATE clause)

### Cluster 106 — European Classical Sword Family

- **Pool count:** N=984 (hdbscan_native subsample: 216; lineage purity 0.9817)
- **Dominant lineage / period / register / kind / wield:** european / classical / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Light Sword; Serpent Sword; pike
- **Provisional description:** PROVISIONAL: european classical bow/sword weapons (historical register; category; N=984)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9817); 4/5 reps confirm 'sword' form.
- **Special-case flags:** none
- **DB cluster id:** 107 (for Phase E-2-DB UPDATE clause)

### Cluster 107 — European Industrial Rifle Family

- **Pool count:** N=337 (hdbscan_native subsample: 80; lineage purity 0.8309)
- **Dominant lineage / period / register / kind / wield:** european / industrial / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Percussion military rifle; Percussion rifle; Centrefire bolt-action military rifle
- **Provisional description:** PROVISIONAL: european industrial rifle/musket weapons (historical register; category; N=337)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.8309); 4/5 reps confirm 'rifle' form.
- **Special-case flags:** none
- **DB cluster id:** 108 (for Phase E-2-DB UPDATE clause)

### Cluster 108 — Untyped-Lineage Classical Catalog-Residue Pool

- **Pool count:** N=112 (hdbscan_native subsample: 31; lineage purity 0.3929)
- **Dominant lineage / period / register / kind / wield:** unknown / classical / historical / category / two_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Escut d'una estàtua de gladiador (MNAT-45405); Q18425053; Hummingbird Bloodletter
- **Provisional description:** PROVISIONAL: unknown classical lance/hammer weapons (historical register; category; N=112)
- **Override applied:** Yes — Provisional 'lance' contradicted by reps (gladiator-statue shield + Q18425053 + hummingbird bloodletter + boomerang + XM1111 mid-range missile). Cluster is heterogeneous mostly-uncurated classical items.
- **Framing-audit notes:** Lineage purity 0.3929 (one of the lowest in the pool). Substrate-honest catalogue-residue cluster.
- **Special-case flags:** provisional_description_overridden, lineage_uncurated, low_lineage_purity
- **Phase E-3/E-4 hand-off notes:** elrond: this cluster's <40% purity flags lineage-canonicalization gap on classical-tagged uncurated entries.
- **DB cluster id:** 109 (for Phase E-2-DB UPDATE clause)

### Cluster 109 — Middle Eastern Classical Halberd Family

- **Pool count:** N=159 (hdbscan_native subsample: 40; lineage purity 0.7107)
- **Dominant lineage / period / register / kind / wield:** middle_eastern / classical / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Mount for Spear-Shaft; Iron Spearhead socket, Yale University Art Gallery, inv. 1938.5999.1082; Iron spear head, Yale University Art Gallery, inv. 1938.5999.1308
- **Provisional description:** PROVISIONAL: middle_eastern classical halberd/spear weapons (historical register; category; N=159)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest cluster (purity 0.7107); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint.
- **Special-case flags:** none
- **DB cluster id:** 110 (for Phase E-2-DB UPDATE clause)

### Cluster 110 — East Asian Industrial Spear Family

- **Pool count:** N=191 (hdbscan_native subsample: 43; lineage purity 0.9162)
- **Dominant lineage / period / register / kind / wield:** east_asian / industrial / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Trident (san gu cha or bian cha); Arisaka; Maxim gun
- **Provisional description:** PROVISIONAL: east_asian industrial spear/sword weapons (historical register; category; N=191)
- **Override applied:** Yes — Provisional weapon-form 'spear/sword' refined from rep evidence; dominant rep-form is 'trident' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9162); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'spear/sword' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 111 (for Phase E-2-DB UPDATE clause)

### Cluster 111 — European-Tagged Modern Shotgun Pool (Mixed)

- **Pool count:** N=115 (hdbscan_native subsample: 26; lineage purity 0.3565)
- **Dominant lineage / period / register / kind / wield:** european / modern / historical / category / two_hand
- **Cluster type:** `mixed_cross_cultural`
- **Top-3 hdbscan_native representatives:** Escudo; Canon de BirHakeim; Boomerang
- **Provisional description:** PROVISIONAL: european modern shotgun/rifle weapons (historical register; category; N=115)
- **Override applied:** No
- **Framing-audit notes:** Low lineage purity 0.3565 — cluster has substantial secondary lineage content. Coarse-spine.
- **Special-case flags:** low_lineage_purity
- **DB cluster id:** 112 (for Phase E-2-DB UPDATE clause)

### Cluster 112 — European Modern Rifle Family

- **Pool count:** N=2062 (hdbscan_native subsample: 447; lineage purity 0.9961)
- **Dominant lineage / period / register / kind / wield:** european / modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Maltese Ring; Seax of Beagnoth; M2 machine gun at Musee de l'Armée
- **Provisional description:** PROVISIONAL: european modern rifle/spear weapons (historical register; category; N=2062)
- **Override applied:** Yes — Provisional weapon-form 'rifle/spear' refined from rep evidence; dominant rep-form is 'revolver' (2/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9961); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'rifle/spear' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 113 (for Phase E-2-DB UPDATE clause)

### Cluster 113 — Middle Eastern Uncurated-Period Spear Family

- **Pool count:** N=257 (hdbscan_native subsample: 55; lineage purity 0.6654)
- **Dominant lineage / period / register / kind / wield:** middle_eastern / unknown / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** HYDRA Heavy Assault Rifle; Spear head; Spear head
- **Provisional description:** PROVISIONAL: middle_eastern unknown spear/rifle weapons (historical register; category; N=257)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.6654); 3/5 reps confirm 'spear' form.
- **Special-case flags:** none
- **DB cluster id:** 114 (for Phase E-2-DB UPDATE clause)

### Cluster 114 — S. American Indigenous Modern Pool (Mixed)

- **Pool count:** N=95 (hdbscan_native subsample: 22; lineage purity 0.4947)
- **Dominant lineage / period / register / kind / wield:** south_american_indigenous / modern / historical / category / two_hand
- **Cluster type:** `rare_lineage_isolate`
- **Top-3 hdbscan_native representatives:** Browning M1919; Apache (missile); Tanque Argentino Mediano
- **Provisional description:** PROVISIONAL: south_american_indigenous modern rifle/sabre weapons (historical register; category; N=95)
- **Override applied:** No
- **Framing-audit notes:** Rare-lineage isolate; lineage purity 0.4947 indicates secondary lineage absorption. Coarse-spine label.
- **Special-case flags:** low_lineage_purity, rare_lineage_no_home
- **DB cluster id:** 115 (for Phase E-2-DB UPDATE clause)

### Cluster 115 — European Uncurated-Period Spear Family

- **Pool count:** N=1335 (hdbscan_native subsample: 258; lineage purity 0.9251)
- **Dominant lineage / period / register / kind / wield:** european / unknown / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** GYATA-64 mine; Round sheild; M111 offensive hand grenade
- **Provisional description:** PROVISIONAL: european unknown spear weapons (historical register; category; N=1335)
- **Override applied:** Yes — Provisional weapon-form 'spear' refined from rep evidence; dominant rep-form is 'mine' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9251); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'spear' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 116 (for Phase E-2-DB UPDATE clause)

### Cluster 116 — Southeast Asian Uncurated-Period Sabre Family

- **Pool count:** N=151 (hdbscan_native subsample: 33; lineage purity 0.9868)
- **Dominant lineage / period / register / kind / wield:** southeast_asian / unknown / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Pedang Diraja; Sundang Diraja; Areindama
- **Provisional description:** PROVISIONAL: southeast_asian unknown sabre/musket weapons (historical register; category; N=151)
- **Override applied:** Yes — Provisional weapon-form 'sabre/musket' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9868); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'sabre/musket' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 117 (for Phase E-2-DB UPDATE clause)

### Cluster 117 — South Asian Uncurated-Period Musket Family

- **Pool count:** N=127 (hdbscan_native subsample: 24; lineage purity 0.9291)
- **Dominant lineage / period / register / kind / wield:** south_asian / unknown / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Bachhawali Tope; Pinaka multi-barrel rocket launcher; OTO Melara 76 mm
- **Provisional description:** PROVISIONAL: south_asian unknown musket weapons (historical register; category; N=127)
- **Override applied:** Yes — Provisional weapon-form 'musket' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9291); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'musket' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 118 (for Phase E-2-DB UPDATE clause)

### Cluster 118 — European Industrial Spear Family

- **Pool count:** N=1262 (hdbscan_native subsample: 254; lineage purity 0.9699)
- **Dominant lineage / period / register / kind / wield:** european / industrial / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** 7.7 cm FK 96; 75 mm Whitworth gun, Model 1873 (Cartagena); Centrefire five-shot revolver
- **Provisional description:** PROVISIONAL: european industrial spear/rifle weapons (historical register; category; N=1262)
- **Override applied:** Yes — Provisional weapon-form 'spear/rifle' refined from rep evidence; dominant rep-form is 'revolver' (2/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9699); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'spear/rifle' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 119 (for Phase E-2-DB UPDATE clause)

### Cluster 119 — Untyped-Lineage Mixed Mythical/Fantasy/Modern Pool

- **Pool count:** N=1205 (hdbscan_native subsample: 257; lineage purity 0.9768)
- **Dominant lineage / period / register / kind / wield:** unknown / unknown / historical / category / two_hand
- **Cluster type:** `mixed_form_pool`
- **Top-3 hdbscan_native representatives:** Round sheild; Ame no Makakoyumi; Anjalikastra
- **Provisional description:** PROVISIONAL: unknown unknown rifle/lance weapons (historical register; category; N=1205)
- **Override applied:** Yes — Provisional 'rifle' contradicted by reps (round shield + Ame no Makakoyumi (Shinto mythological bow) + Anjalikastra (Hindu mythic weapon) + Serious Bomb + Ultimate Nullifier). Cluster spans mythological, fantasy, and modern items under untyped lineage+period.
- **Framing-audit notes:** Second-largest 'unknown lineage' cluster (N=1205); coarse-spine label reflects its catch-all mythical/fantasy/modern nature.
- **Special-case flags:** provisional_description_overridden, lineage_uncurated, mixed_form_within_cluster
- **Phase E-3/E-4 hand-off notes:** Phase E-1.5 sensitivity sweep should split mythological from fantasy from modern subgroups.
- **DB cluster id:** 120 (for Phase E-2-DB UPDATE clause)

### Cluster 120 — Southeast Asian Modern Musket Family

- **Pool count:** N=115 (hdbscan_native subsample: 21; lineage purity 0.6957)
- **Dominant lineage / period / register / kind / wield:** southeast_asian / modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** AGM-65 Maverick; Karambit; FV106 Samson
- **Provisional description:** PROVISIONAL: southeast_asian modern musket/rifle weapons (historical register; category; N=115)
- **Override applied:** Yes — Provisional weapon-form 'musket/rifle' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.6957); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'musket/rifle' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 121 (for Phase E-2-DB UPDATE clause)

### Cluster 121 — African Industrial Sword Family

- **Pool count:** N=65 (hdbscan_native subsample: 16; lineage purity 0.6462)
- **Dominant lineage / period / register / kind / wield:** african / industrial / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Handkerchief; Flyssa; 4 bore
- **Provisional description:** PROVISIONAL: african industrial sword/spear weapons (historical register; category; N=65)
- **Override applied:** Yes — Provisional weapon-form 'sword/spear' refined from rep evidence; dominant rep-form is 'carbine' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.6462); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'sword/spear' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 122 (for Phase E-2-DB UPDATE clause)

### Cluster 122 — European Modern Rifle Family

- **Pool count:** N=133 (hdbscan_native subsample: 32; lineage purity 0.9023)
- **Dominant lineage / period / register / kind / wield:** european / modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Rimfire self-loading magazine rifle; Centrefire self-loading magazine rifle; Centrefire bolt-action target rifle
- **Provisional description:** PROVISIONAL: european modern rifle/sabre weapons (historical register; category; N=133)
- **Override applied:** No
- **Framing-audit notes:** Substrate-honest weapon-family cluster (purity 0.9023); 5/5 reps confirm 'rifle' form.
- **Special-case flags:** none
- **DB cluster id:** 123 (for Phase E-2-DB UPDATE clause)

### Cluster 123 — Middle Eastern Modern Spear Family

- **Pool count:** N=130 (hdbscan_native subsample: 26; lineage purity 0.9692)
- **Dominant lineage / period / register / kind / wield:** middle_eastern / modern / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** Iron Quarrel Head, Yale University Art Gallery, inv. 1938.5999.1039; Iron Quarrel Head, Yale University Art Gallery, inv. 1938.5999.1045; Iron Quarrel Head, Yale University Art Gallery, inv. 1938.5999.1047
- **Provisional description:** PROVISIONAL: middle_eastern modern spear/lance weapons (historical register; category; N=130)
- **Override applied:** Yes — Provisional weapon-form 'spear/lance' not supported by top hdbscan_native reps.
- **Framing-audit notes:** Substrate-honest cluster (purity 0.9692); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'spear/lance' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 124 (for Phase E-2-DB UPDATE clause)

### Cluster 124 — Middle Eastern Medieval Rifle Family

- **Pool count:** N=56 (hdbscan_native subsample: 11; lineage purity 0.6786)
- **Dominant lineage / period / register / kind / wield:** middle_eastern / medieval / historical / category / two_hand
- **Cluster type:** `weapon_family`
- **Top-3 hdbscan_native representatives:** FV432; APC Talha; Emad (missile)
- **Provisional description:** PROVISIONAL: middle_eastern medieval rifle/lance weapons (historical register; category; N=56)
- **Override applied:** Yes — Provisional weapon-form 'rifle/lance' refined from rep evidence; dominant rep-form is 'apc' (1/5).
- **Framing-audit notes:** Substrate-honest cluster (purity 0.6786); reps do not surface single dominant form-token at top-5. Provisional weapon-form retained as coarse-spine hint. Provisional weapon-form 'rifle/lance' not present in top-3 hdbscan_native reps.
- **Special-case flags:** provisional_description_overridden
- **DB cluster id:** 125 (for Phase E-2-DB UPDATE clause)

---

## Cross-references

- Dispatch: `agentic_orchestration/dispatches/2026-05-23-gandalf-phase-E-2-cluster-labeling.md`
- Gate-2 findings record: `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-gate-2-findings-record.md`
- Phase E-1 clusters: `phase-E-1-clusters.md`
- Phase E-1 axis discovery: `phase-E-1-axis-discovery.md`
- MIGRATION.md § 4 (native-vs-nearest split): `MIGRATION.md`
- Framing-audit checklist: `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5
- N. am. indigenous recognition record: `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md`
- ADR-001 (tag protocol), ADR-002 (tiered approval), ADR-004 (cross-seam MIGRATION.md), ADR-006 (read-only external state)
- Discipline #18 (substrate-voting-is-binding); Discipline #19 (forensic-conclusion-discipline)

---

**Signed:** gandalf, 2026-05-23T17:01:45Z