# True-size table — every JOIN-1 enemy pack (2026-10-02)

Lane SZ, Run C-9 Phase 2 (drax; conductor gandalf). Machine-readable twin: `true_size_table_2026-10-02.json` (same directory).

**Why:** KC2 (ledger KP-222) handles big creatures either by per-kit pixels-per-metre or by scaling each record at runtime by `factor`. Every pack is cut at `camera.ppm_render` **151.337** (the contract value, read from each pack's `matrix_index.json`). Every enemy kit now carries a `true_size` block, so KC2 can take either path without a re-cut.

**Rule (en46's, unchanged):** `true = designed height × scale(record) / scale(reference record)`; `factor = true / shipped`. The roster `scale` is DATAMINED. The roster mesh heights are not used (Lap F). **Shipped** = the pack's measured `h_model` (rest crown-to-sole). The 9 earlier blocks used the build target, which differs from h_model by 0.5 mm or less. **Designed** = the EN-E2 build target (`height.json target_m`), or for EN-E3, shipped ÷ cfg `motion_scale` (the canvas downscale). **Reference** = the roster type `lead_record`, except for voidlord, whose clip manifest names Ekket'Zul (see notes).

**Records:** every roster record on the rig that the pack serves (the waves 151-160 roster packet, including summons). Records that have their own pack are excluded: the witches and the mind-taker from acolyte-f, the warden and the magister from acolyte-m. A record **in bold** is used by the referent line-up (BUILD_PRIORITY.md §6). Rows are grouped by scale.

**Pack → rig:** the rig named in each pack's clip manifest (`what`: "roster rig X"), cross-checked against the EN-E3 cfg `type_id` and the EN-E2 manifest `roster.rig`. **UNRESOLVED: none.**

| pack | rig | shipped h_model m | designed m (ref record @ scale) | scale | records (bold = referent) | true m | factor | e_bodies |
|---|---|---|---|---|---|---|---|---|
| en-acolyte-f | heroine01_unarmed | 1.7992 (h_model 1.7992) | 1.800 (ghost_a01 @ 1) | 1 | ghost_a01, ghost_a01_summon, ghost_b01_summon, ghost_b02_summon, kc_bounty08 | 1.8 | 1.000 | 3.146 |
| | | | | 1.15 | **ku_bounty_06** | 2.07 | 1.151 | 0.082 |
| | | | | 1.2 | bl_bounty18, exile_bounty14, exile_bounty15, nemesis_kymon_02, odv_bounty06 | 2.16 | 1.201 | 0.405 |
| | | | | 1.35 | nemesis_orderdeathsvigil_02 | 2.43 | **1.351** | 0.101 |
| en-acolyte-m | hero01_unarmed | 1.8797 (h_model 1.8797) | 1.880 (ghost_a02 @ 1) | 1 | ghost_a02, ghost_b03_summon, ghost_b04_summon, kc_bounty07 | 1.88 | 1.000 | 2.208 |
| | | | | 1.1 | cultist_cultleader_01 | 2.068 | 1.100 | 0.502 |
| | | | | 1.2 | dc_bounty06, dc_bounty07, dc_bounty10, dc_bounty11, dc_bounty15, kc_bounty10, korvaak_lieutenant_01, nemesis_outlaw_01 | 2.256 | 1.200 | 0.795 |
| | | | | 1.35 | eldritcharmor_a01, eldritcharmor_a01_summon, nemesis_kymon_01 | 2.538 | **1.350** | 1.73 |
| | | | | 1.48 | nemesis_outlaw_02 | 2.782 | **1.480** | 0.099 |
| | | | | 1.5 | eldritcharmor_b01 | 2.82 | **1.500** | 0.807 |
| | | | | 1.65 | eldritcharmor_c01 | 3.102 | **1.650** | 0.508 |
| | | | | 1.9 | eldritcharmor_dreegmindreaper_01, mindreaper_summon | 3.572 | **1.900** | 1.012 |
| en-blightsac | voidfiend | 1.4584 (h_model 1.4584) | 1.458 (chthonianwretch_b01 @ 1.1) | 1.1 | chthonianfiend_a01_summon, chthonianwretch_a01, chthonianwretch_b01 | 1.458 | 1.000 | 3.038 |
| | | | | 1.2 | chthonianfiend_c01_summon, chthonianwretch_c01 | 1.591 | 1.091 | 1.466 |
| | | | | 1.35 | **chthonianfiend_h01**, chthonianfiend_h02, chthonianfiend_h03, chthonianfiend_h04, chthonianfiend_h05, devotion/chthonianfiend_h01, devotion/chthonianfiend_h02, devotion/chthonianfiend_h03, devotion/chthonianfiend_h04, devotion/chthonianfiend_h05, **kc_bounty09** | 1.79 | 1.227 | 0.265 |
| | | | | 1.5 | devotion/chthonianfiend_h06 | 1.989 | **1.364** | 0.036 |
| en-bonegolem *(existing)* | golembone_phase01 | 2.2 (h_model 2.1965) | 2.600 (skeletalgolem_c01 @ 1.4) | 1.2 | skeletalgolem_b01 (trash) | 2.229 | 1.013 | 0.234 |
| | | | | 1.4 | skeletalgolem_c01/skeletalgolem_stepsoftorment_01 (boss/trash) | 2.6 | 1.182 | 0.626 |
| | | | | 1.5 | ro_bounty19/skeletalgolem_h01/skeletalgolem_h02/skeletalgolem_h03/... (champion-hero) | 2.786 | 1.266 | 0.277 |
| en-brute | aetherialcorruption | 2.2996 (h_model 2.2996) | 2.300 (aetherialcorruption_c01 @ 1.6) | 1.25 | aetherialcorruption_a01 | 1.797 | 0.781 | 0.557 |
| | | | | 1.48 | **aetherialcorruption_b01**, aetherialcorruption_b01_summon, aetherialcorruption_b02, aetherialcorruption_b02_summon, aetherialcorruption_b03, aetherialcorruption_b03_summon | 2.127 | 0.925 | 8.372 |
| | | | | 1.6 | **aetherialcorruption_c01**, **aetherialcorruption_c01_summon** | 2.3 | 1.000 | 5.605 |
| | | | | 1.65 | **aetherialcorruption_h01**, **aetherialcorruption_h02**, **aetherialcorruption_h03**, **aetherialcorruption_h04**, **aetherialcorruption_h05**, **devotion/aetherialcorruption_h01**, **devotion/aetherialcorruption_h02**, **devotion/aetherialcorruption_h03**, **devotion/aetherialcorruption_h04** | 2.372 | 1.031 | 4.122 |
| | | | | 2.05 | **aetherialcorruption_intro** | 2.947 | 1.281 | 1.0 |
| en-burrowworm *(table only)* | aetherialworm | 0.732 (h_model 0.7320) | 0.732 (aetherialworm_b01_summon @ 1.2) | 1.2 | **aetherialworm_b01_summon**, **aetherialworm_b02_summon**, **aetherialworm_b03_summon**, **aetherialworm_b04_summon** | 0.732 | 1.000 | 1.34 |
| en-cinderstalker | sandlizard | 1.7695 (h_model 1.7695) | 2.466 (sandlizard_volcanic_a01 @ 1) | 1 | **sandlizard_a01**, sandlizard_eldritch_a01, sandlizard_volcanic_a01 | 2.467 | **1.394** | 2.913 |
| | | | | 1.15 | **sandlizard_b01**, sandlizard_b02, sandlizard_eldritch_b01, sandlizard_eldritch_b02, sandlizard_volcanic_b01, sandlizard_volcanic_b02 | 2.837 | **1.603** | 3.187 |
| | | | | 1.25 | **sandlizard_c01**, sandlizard_eldritch_c01, sandlizard_volcanic_c01 | 3.083 | **1.742** | 1.359 |
| en-crawlerlarva *(table only)* | maggot01a | 0.2347 (h_model 0.2347) | 0.235 (beetle_maggot01_maggotsummon @ 1.1) | 1.1 | **beetle_maggot01_maggotsummon** | 0.235 | 1.000 | 0.25 |
| en-cryptgazer | basilisk | 1.6115 (h_model 1.6115) | 1.833 (basilisk_a01 @ 1) | 1 | **basilisk_a01** | 1.833 | 1.138 | 1.545 |
| | | | | 1.22 | **basilisk_b01** | 2.237 | **1.388** | 1.209 |
| | | | | 1.35 | **basilisk_c01**, **basilisk_witchritual** | 2.475 | **1.536** | 1.266 |
| | | | | 1.42 | basilisk_h01, **basilisk_h02**, basilisk_h03, basilisk_h04, **basilisk_h05**, cu_bounty07, devotion/basilisk_h01, devotion/basilisk_h02, devotion/basilisk_h03, devotion/basilisk_h04 | 2.603 | **1.615** | 1.762 |
| en-cryptglutton | aetherialbloater | 2.1864 (h_model 2.1864) | 2.277 (aetherialbloater_a01 @ 1) | 1 | aetherialbloater_a01 | 2.277 | 1.042 | 1.125 |
| | | | | 1.15 | **aetherialbloater_b01**, **aetherialbloater_b01_summon** | 2.619 | 1.198 | 1.724 |
| | | | | 1.25 | **aetherialbloater_c01** | 2.847 | **1.302** | 0.447 |
| | | | | 1.33 | cu_bounty04, devotion/aetherialbloater_h01, devotion/aetherialbloater_h02, devotion/aetherialbloater_h03, devotion/aetherialbloater_h04, pm_bounty05 | 3.029 | **1.385** | 0.425 |
| | | | | 1.53 | **aetherialbloater_malmouthdocks_01** | 3.485 | **1.594** | 0.335 |
| en-cryptmaw | devourer | 1.341 (h_model 1.3410) | 1.341 (chthoniandevourer_a01 @ 0.9) | 0.9 | **chthoniandevourer_a01**, chthoniandevourer_a01_summon | 1.341 | 1.000 | 5.809 |
| | | | | 1.2 | **chthoniandevourer_b01**, **chthoniandevourer_b02** | 1.788 | **1.333** | 6.869 |
| | | | | 1.25 | bl_bounty08, odv_bounty12 | 1.863 | **1.389** | 0.158 |
| | | | | 1.6 | devotion/chthoniandevourer_h01, devotion/chthoniandevourer_h02, devotion/chthoniandevourer_h03, devotion/chthoniandevourer_h04, devotion/chthoniandevourer_h05, devotion/chthoniandevourer_h06 | 2.384 | **1.778** | 0.218 |
| en-gaunt | wendigo | 2.3986 (h_model 2.3986) | 2.400 (wendigo_a01 @ 1) | 1 | **wendigo_a01** | 2.4 | 1.001 | 1.353 |
| | | | | 1.15 | **wendigo_b01**, **wendigo_b02** | 2.76 | 1.151 | 1.315 |
| | | | | 1.2 | cu_bounty09, devotion/wendigo_h01, devotion/wendigo_h02, devotion/wendigo_h03, devotion/wendigo_h04, wendigo_h01, wendigo_h02, wendigo_h03, wendigo_h04, wendigo_h05 | 2.88 | 1.201 | 1.772 |
| | | | | 1.22 | **wendigo_c01** | 2.928 | 1.221 | 0.655 |
| | | | | 1.25 | wendigo_ancient_namadea | 3.0 | 1.251 | 0.248 |
| | | | | 1.4 | nemesis_wendigo_01 | 3.36 | **1.401** | 0.702 |
| en-golem | golemswamp_phase01 | 2.2985 (h_model 2.2985) | 2.300 (swampgolem_a01 @ 1) | 1 | **swampgolem_a01** | 2.3 | 1.001 | 4.188 |
| | | | | 1.15 | swampgolem_b01 | 2.645 | 1.151 | 0.951 |
| | | | | 1.28 | swampgolem_c01 | 2.944 | 1.281 | 0.482 |
| | | | | 1.32 | cu_bounty06, cw_bounty06, devotion/swampgolem_h01, devotion/swampgolem_h02, devotion/swampgolem_h03, devotion/swampgolem_h04, **swampgolem_h01**, **swampgolem_h02**, **swampgolem_h03**, **swampgolem_h04**, **swampgolem_h05** | 3.036 | **1.321** | 3.407 |
| en-icebrute *(existing)* | yeti | 2.2 (h_model 2.1984) | 2.800 (yetidire_a01 @ 0.8) | 0.8 | yetidire_a01/yetidire_b01 (trash) | 2.8 | 1.273 | 1.125 |
| | | | | 0.92 | yetidire_b02 (trash) | 3.22 | **1.464** | 0.393 |
| | | | | 1.05 | ku_bounty_08/yetidire_c01/yetidire_h01/yetidire_h02/... (champion-hero/trash) | 3.675 | **1.670** | 0.635 |
| | | | | 1.12 | cw_bounty09 (champion-hero) | 3.92 | **1.782** | 0.137 |
| | | | | 1.25 | yeti_rimehorn_01 (boss) | 4.375 | **1.989** | 0.251 |
| | | | | 1.6 | nemesis_beast_01_p1 (nemesis) | 5.6 | **2.545** | 0.505 |
| en-imp | aetherialimp | 1.1499 (h_model 1.1499) | 1.150 (aetherialimp_a01 @ 0.65) | 0.65 | aetherialimp_a01 | 1.15 | 1.000 | 3.27 |
| | | | | 0.72 | aetherialimp_b01 | 1.274 | 1.108 | 1.701 |
| | | | | 0.85 | **aetherialimp_h01**, **aetherialimp_h02**, **aetherialimp_h03**, **aetherialimp_h04**, **aetherialimp_h05** | 1.504 | **1.308** | 1.008 |
| en-magister *(existing)* | hero01_unarmed | 2.54 (h_model 2.5395) | 1.880 (ghost_a02 @ 1) | 1.35 | nemesis_aetherialvanguard_01 (nemesis) | 2.538 | 0.999 | 0.5 |
| en-mindtaker *(existing)* | heroine01_unarmed | 1.8 (h_model 1.7990) | 1.800 (ghost_a01 @ 1) | 1 | humanascendant_mindthief_01 (boss) | 1.8 | 1.000 | 0.494 |
| en-ossuarybloom | carnivorousplant01a_p1 | 1.9844 (h_model 1.9844) | 1.984 (livingplant_a01 @ 0.7) | 0.7 | **livingplant_a01**, **livingplant_a01_summon** | 1.984 | 1.000 | 9.761 |
| en-ossuarycrab | crabmonstrosity | 1.7246 (h_model 1.7246) | 1.725 (swampcrab_a01 @ 1) | 0.5 | **springscrab_a00_summon**, **swampcrab_a00_summon** | 0.862 | **0.500** | 3.922 |
| | | | | 1 | **swampcrab_a01** | 1.725 | 1.000 | 3.35 |
| | | | | 1.2 | **swampcrab_b01**, swampcrab_b01_summon | 2.07 | 1.200 | 3.236 |
| | | | | 1.35 | **swampcrab_c01**, swampcrab_c01_summon | 2.328 | **1.350** | 1.896 |
| | | | | 1.45 | cu_bounty08, **devotion/swampcrab_h01**, **devotion/swampcrab_h02**, **devotion/swampcrab_h03**, **devotion/swampcrab_h04** | 2.501 | **1.450** | 0.276 |
| | | | | 2 | ghostcrab_h01, ghostcrab_h02, ghostcrab_h03, ghostcrab_h04, ghostcrab_h05, springscrab_h01, springscrab_h02, springscrab_h03, springscrab_h04, **swampcrab_h01**, **swampcrab_h02**, **swampcrab_h03**, **swampcrab_h04**, **swampcrab_h05** | 3.449 | **2.000** | 3.0 |
| | | | | 2.8 | swampcrab_ugdenbog_01 | 4.829 | **2.800** | 0.247 |
| en-revenant | skeleton_01a | 1.7993 (h_model 1.7993) | 1.800 (skeleton_c03 @ 1.16) | 1 | skeleton_a01_summon, **skeleton_a02_summon** | 1.552 | 0.862 | 1.111 |
| | | | | 1.08 | skeleton_b01_archer_summon | 1.676 | 0.931 | 0.101 |
| | | | | 1.12 | skeleton_b02_knight, skeleton_b02_knight_summon | 1.738 | 0.966 | 1.239 |
| | | | | 1.16 | **devotion/skeleton_h09**, **skeleton_c01**, skeleton_c01_summon, **skeleton_c02**, skeleton_c02_summon, **skeleton_c03**, **skeleton_d01** | 1.8 | 1.000 | 4.506 |
| | | | | 1.2 | **devotion/skeleton_h01**, **devotion/skeleton_h02**, **devotion/skeleton_h03**, **devotion/skeleton_h04**, **devotion/skeleton_h05**, **devotion/skeleton_h06**, **devotion/skeleton_h08**, **devotion/skeleton_h10** | 1.862 | 1.035 | 0.313 |
| | | | | 1.3 | **devotion/skeleton_h07** | 2.017 | 1.121 | 0.037 |
| en-rimethorn | thornedhorrora01 | 1.7339 (h_model 1.7339) | 1.734 (thornedhorrorfrost_a01 @ 0.65) | 0.65 | thornedhorrorfrost_a01 | 1.734 | 1.000 | 1.849 |
| | | | | 0.85 | thornedhorrorfrost_b01 | 2.267 | **1.308** | 0.921 |
| | | | | 1.12 | thornedhorrorfrost_c01, thornedhorrorfrost_h01, thornedhorrorfrost_h02, thornedhorrorfrost_h03, thornedhorrorfrost_h04 | 2.988 | **1.723** | 2.227 |
| | | | | 1.15 | bl_bounty10 | 3.068 | **1.769** | 0.073 |
| en-statue *(existing)* | possessedstatue | 2.05 (h_model 2.0494) | 2.300 (statue_a02 @ 2) | 2 | statue_a01/statue_a02 (trash) | 2.3 | 1.122 | 0.403 |
| | | | | 2.2 | statue_b01/statue_b02 (trash) | 2.53 | 1.234 | 0.317 |
| | | | | 2.5 | statue_c01/statue_c02/statue_templeguardian_02/statue_templeguardian_03 (boss/trash) | 2.875 | **1.402** | 0.678 |
| | | | | 3 | statue_korvaaktombguardian (boss) | 3.45 | **1.683** | 0.498 |
| en-voiddrone *(existing)* | chthonianservitor | 3.6 (h_model 1.9362) | length 3.60 (roster box depth 8.79 @ scale 1) | 0.5 | chthonianservitor_a01 (drone summon) | 4.39 (length) | 1.221 | — |
| | | | | 0.7 | chthonianservitor_b01/b02 | 6.15 (length) | **1.709** | — |
| | | | | 0.9 | chthonianservitor_c01 | 7.91 (length) | **2.197** | — |
| | | | | 0.95 | hero records h01-h04 | 8.35 (length) | **2.320** | — |
| | | | | 1 | chthonianservitor_lunalvalgoth (boss) | 8.79 (length) | **2.442** | — |
| en-voiddrone_boss *(existing)* | chthonianservitor | 3.6 (h_model 1.9362) | length 3.60 (roster box depth 8.79 @ scale 1) | 0.5 | chthonianservitor_a01 (drone summon) | 4.39 (length) | 1.221 | — |
| | | | | 0.7 | chthonianservitor_b01/b02 | 6.15 (length) | **1.709** | — |
| | | | | 0.9 | chthonianservitor_c01 | 7.91 (length) | **2.197** | — |
| | | | | 0.95 | hero records h01-h04 | 8.35 (length) | **2.320** | — |
| | | | | 1 | chthonianservitor_lunalvalgoth (boss) | 8.79 (length) | **2.442** | — |
| en-voidlord | chthonianrylok | 2.5999 (h_model 2.5999) | 2.600 (chthonianrylok_ekketzul @ 1.6) | 1 | chthonianrylok_a01, gargoyle_a01 | 1.625 | **0.625** | 0.713 |
| | | | | 1.2 | chthonianrylok_b01, gargoyle_b01 | 1.95 | 0.750 | 0.467 |
| | | | | 1.32 | chthonianrylok_c01, gargoyle_c01 | 2.145 | 0.825 | 0.334 |
| | | | | 1.4 | cw_bounty04, devotion/chthonianrylok_h01, devotion/chthonianrylok_h02, devotion/chthonianrylok_h03, devotion/chthonianrylok_h04 | 2.275 | 0.875 | 0.273 |
| | | | | 1.44 | **chthonianrylok_gabalthunn** | 2.34 | 0.900 | 0.496 |
| | | | | 1.6 | **chthonianrylok_ekketzul**, nemesis_chthonianvoidborn_01 | 2.6 | 1.000 | 0.699 |
| | | | | 1.75 | korvaakmessenger_02, korvaakmessenger_02b | 2.844 | 1.094 | 0.498 |
| en-warden *(existing)* | hero01_unarmed | 2.63 (h_model 2.6298) | 1.880 (ghost_a02 @ 1) | 1.4 | witchgod_finalboss (boss) | 2.632 | 1.001 | 1.0 |
| en-witch *(existing)* | heroine01_unarmed | 2.07 (h_model 2.0698) | 1.800 (ghost_a01 @ 1) | 1 | witch_larria (boss) | 1.8 | 0.870 | 0.5 |
| | | | | 1.15 | witch_janaxia (boss) | 2.07 | 1.000 | 1.0 |
| en-wraith | wraith | 1.8487 (h_model 1.8487) | 1.850 (wraith_a01 @ 1) | 1 | **eldritchwraith_a01**, **wraith_a01**, wraith_a01_summon | 1.85 | 1.001 | 5.74 |
| | | | | 1.15 | **eldritchwraith_b01**, **wraith_b01**, **wraith_b01_summon** | 2.127 | 1.151 | 5.92 |
| | | | | 1.25 | cw_bounty07, cw_bounty08, devotion/wraith_h01, devotion/wraith_h02, devotion/wraith_h03, devotion/wraith_h04, **eldritchwraith_c01**, **wraith_c01**, wraith_c01_summon, **wraith_h01**, **wraith_h02**, **wraith_h03**, **wraith_h04**, **wraith_h05** | 2.312 | 1.251 | 5.858 |
| | | | | 1.32 | nemesis_wendigo_02 | 2.442 | **1.321** | 0.2 |
| en-wretch | cannibal | 1.7996 (h_model 1.7996) | 1.800 (wendigocannibal_a01 @ 0.9) | 0.9 | **wendigocannibal_a01** | 1.8 | 1.000 | 2.714 |
| | | | | 1 | **wendigocannibal_b01** | 2.0 | 1.111 | 2.107 |
| | | | | 1.15 | wendigocannibal_c01 | 2.3 | 1.278 | 0.498 |
| | | | | 1.25 | wendigocannibal_h01, wendigocannibal_h02, wendigocannibal_h03, wendigocannibal_h04, wendigocannibal_h05, wendigocannibal_packla | 2.5 | **1.389** | 0.332 |

Bold factors fall outside 0.7–1.3.

## Notes per pack

- **en-acolyte-f** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_f/height.json target_m 1.80; no canvas downscale) / reference = the roster type lead_record ghost_a01 / records with their own pack, NOT served here: humanascendant_mindthief_01 -> en-mindtaker, witch_janaxia -> en-witch, witch_larria -> en-witch
- **en-acolyte-m** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_m/height.json target_m 1.88; no canvas downscale) / reference = the roster type lead_record ghost_a02 / records with their own pack, NOT served here: nemesis_aetherialvanguard_01 -> en-magister, witchgod_finalboss -> en-warden / the referent line-up uses NO record this pack serves (roster-only coverage)
- **en-blightsac** (NEW block written to the kit): designed = shipped / cfg motion_scale 1.0000 (en_e3/work/cfg_blightsac.json; a floater sized to 1.6 m max horizontal extent (body ~1.4 m, hover 0.15 m); the roster box (3.0 x 2.74 x 2.62 mesh units x 1.1) reads as the GD mesh incl. its e) / reference = the roster type lead_record chthonianwretch_b01
- **en-bonegolem** (existing block (read in, unchanged)).
- **en-brute** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_b/height.json target_m 2.30; no canvas downscale) / reference = aetherialcorruption_c01 (scale 1.6) = the roster type lead_record; the manifest roster.lead text says "aetherialcorruption_a01: scale 1.6" but a01 is scale 1.25 in the roster, c01 is the 1.6 record (a label slip in the manifest)
- **en-burrowworm** (lane EN-E3 is repainting it: kit untouched, table row only): designed = shipped / cfg motion_scale 1.0000 (en_e3/work/cfg_worm.json) / reference = the summon rig's only/most-used record
- **en-cinderstalker** (NEW block written to the kit): designed = shipped / cfg motion_scale 0.7174 (en_e3/work/cfg_raptor.json; R-C9-132 conductor ruling (a): scaled x0.7174 (5.47 -> 3.924 m) = the largest scale whose every clip at every heading clears the JOIN-1 canvas with a 5% margin ) / reference = the roster type lead_record sandlizard_volcanic_a01
- **en-crawlerlarva** (lane EN-E3 is repainting it: kit untouched, table row only): designed = shipped / cfg motion_scale 1.0000 (en_e3/work/cfg_larva.json) / reference = the summon rig's only/most-used record
- **en-cryptgazer** (NEW block written to the kit): designed = shipped / cfg motion_scale 0.8790 (en_e3/work/cfg_gazer.json; fit-to-canvas from the start (conductor): built at 3.516 m = 4.0 m x 0.879 from n17 on the 4.0 m first rig (binding cast_breath f7 heading 6); final s_fit 1.050) / reference = the roster type lead_record basilisk_a01
- **en-cryptglutton** (NEW block written to the kit): designed = shipped / cfg motion_scale 0.9600 (en_e3/work/cfg_glutton.json; 2.3 m tall sheet design, built at 2.2 m (x0.957) so every clip clears the JOIN-1 canvas with >=5% margin (n17; binding attack_thrash f4)) / reference = the roster type lead_record aetherialbloater_a01
- **en-cryptmaw** (NEW block written to the kit): designed = shipped / cfg motion_scale 1.0000 (en_e3/work/cfg_maw.json) / reference = the roster type lead_record chthoniandevourer_a01
- **en-gaunt** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_n/height.json target_m 2.40; no canvas downscale) / reference = the roster type lead_record wendigo_a01 (= the manifest roster.lead "Wendigo")
- **en-golem** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_g/height.json target_m 2.30; no canvas downscale) / reference = the roster type lead_record swampgolem_a01 (= the manifest roster.lead "Ugdenbog Golem")
- **en-icebrute** (existing block (read in, unchanged)).
- **en-imp** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_i/height.json target_m 1.15; no canvas downscale) / reference = the roster type lead_record aetherialimp_a01 (= the manifest roster.lead "Aetherial Scamp")
- **en-magister** (existing block (read in, unchanged)).
- **en-mindtaker** (existing block (read in, unchanged)).
- **en-ossuarybloom** (NEW block written to the kit): designed = shipped / cfg motion_scale 1.0000 (en_e3/work/cfg_bloom.json) / reference = the roster type lead_record livingplant_a01
- **en-ossuarycrab** (NEW block written to the kit): designed = shipped / cfg motion_scale 1.0000 (en_e3/work/cfg_crab.json) / reference = the roster type lead_record swampcrab_a01
- **en-revenant** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_r/height.json target_m 1.80; no canvas downscale) / reference = the roster type lead_record skeleton_c03
- **en-rimethorn** (NEW block written to the kit): designed = shipped / cfg motion_scale 1.0000 (en_e3/work/cfg_rimethorn.json; built at the roster lead record size: AABB depth 5.12 x scale 0.65 = 3.33 m; n17 s_fit 1.29 (fits the canvas with 29% margin)) / reference = the roster type lead_record thornedhorrorfrost_a01 / the referent line-up uses NO record this pack serves (roster-only coverage)
- **en-statue** (existing block (read in, unchanged)).
- **en-voiddrone** (existing block (read in, unchanged)).
- **en-voiddrone_boss** (existing block (read in, unchanged)).
- **en-voidlord** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_v/height.json target_m 2.60; no canvas downscale) / reference = chthonianrylok_ekketzul (scale 1.6): the clip manifest roster.lead names it (the BOSS, "Ekket'Zul, Progenitor of Darkness"); the roster type lead_record is chthonianrylok_a01 (scale 1.0)
- **en-warden** (existing block (read in, unchanged)).
- **en-witch** (existing block (read in, unchanged)).
- **en-wraith** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_w/height.json target_m 1.85; no canvas downscale) / reference = the roster type lead_record wraith_a01
- **en-wretch** (NEW block written to the kit): designed = the EN-E2 build target (en_e2/export/final_c/height.json target_m 1.80; no canvas downscale) / reference = the roster type lead_record wendigocannibal_a01 (= the manifest roster.lead "Ugdenbog Wretch")

## Factors above 1.3 or below 0.7

- en-acolyte-f nemesis_orderdeathsvigil_02 (nemesis) factor 1.351 [roster only]
- en-acolyte-m eldritcharmor_a01/eldritcharmor_a01_summon/nemesis_kymon_01 (nemesis/summon/trash) factor 1.350 [roster only]
- en-acolyte-m nemesis_outlaw_02 (nemesis) factor 1.480 [roster only]
- en-acolyte-m eldritcharmor_b01 (trash) factor 1.500 [roster only]
- en-acolyte-m eldritcharmor_c01 (trash) factor 1.650 [roster only]
- en-acolyte-m eldritcharmor_dreegmindreaper_01/mindreaper_summon (boss/summon) factor 1.900 [roster only]
- en-blightsac devotion/chthonianfiend_h06 (champion-hero) factor 1.364 [roster only]
- en-cinderstalker sandlizard_a01/sandlizard_eldritch_a01/sandlizard_volcanic_a01 (trash) factor 1.394 [REFERENT: sandlizard_a01]
- en-cinderstalker sandlizard_b01/sandlizard_b02/sandlizard_eldritch_b01/sandlizard_eldritch_b02/... (trash) factor 1.603 [REFERENT: sandlizard_b01]
- en-cinderstalker sandlizard_c01/sandlizard_eldritch_c01/sandlizard_volcanic_c01 (trash) factor 1.742 [REFERENT: sandlizard_c01]
- en-cryptgazer basilisk_b01 (trash) factor 1.388 [REFERENT: basilisk_b01]
- en-cryptgazer basilisk_c01/basilisk_witchritual (boss/trash) factor 1.536 [REFERENT: basilisk_c01,basilisk_witchritual]
- en-cryptgazer basilisk_h01/basilisk_h02/basilisk_h03/basilisk_h04/... (champion-hero) factor 1.615 [REFERENT: basilisk_h02,basilisk_h05]
- en-cryptglutton aetherialbloater_c01 (trash) factor 1.302 [REFERENT: aetherialbloater_c01]
- en-cryptglutton cu_bounty04/devotion/aetherialbloater_h01/devotion/aetherialbloater_h02/devotion/aetherialbloater_h03/... (champion-hero) factor 1.385 [roster only]
- en-cryptglutton aetherialbloater_malmouthdocks_01 (boss) factor 1.594 [REFERENT: aetherialbloater_malmouthdocks_01]
- en-cryptmaw chthoniandevourer_b01/chthoniandevourer_b02 (trash) factor 1.333 [REFERENT: chthoniandevourer_b01,chthoniandevourer_b02]
- en-cryptmaw bl_bounty08/odv_bounty12 (champion-hero) factor 1.389 [roster only]
- en-cryptmaw devotion/chthoniandevourer_h01/devotion/chthoniandevourer_h02/devotion/chthoniandevourer_h03/devotion/chthoniandevourer_h04/... (champion-hero) factor 1.778 [roster only]
- en-gaunt nemesis_wendigo_01 (nemesis) factor 1.401 [roster only]
- en-golem cu_bounty06/cw_bounty06/devotion/swampgolem_h01/devotion/swampgolem_h02/... (champion-hero) factor 1.321 [REFERENT: swampgolem_h01,swampgolem_h02,swampgolem_h03,swampgolem_h04,swampgolem_h05]
- en-icebrute yetidire_b02 (trash) factor 1.464
- en-icebrute ku_bounty_08/yetidire_c01/yetidire_h01/yetidire_h02/... (champion-hero/trash) factor 1.670
- en-icebrute cw_bounty09 (champion-hero) factor 1.782
- en-icebrute yeti_rimehorn_01 (boss) factor 1.989
- en-icebrute nemesis_beast_01_p1 (nemesis) factor 2.545
- en-imp aetherialimp_h01/aetherialimp_h02/aetherialimp_h03/aetherialimp_h04/... (champion-hero) factor 1.308 [REFERENT: aetherialimp_h01,aetherialimp_h02,aetherialimp_h03,aetherialimp_h04,aetherialimp_h05]
- en-ossuarycrab springscrab_a00_summon/swampcrab_a00_summon (summon) factor 0.500 [REFERENT: springscrab_a00_summon,swampcrab_a00_summon]
- en-ossuarycrab swampcrab_c01/swampcrab_c01_summon (summon/trash) factor 1.350 [REFERENT: swampcrab_c01]
- en-ossuarycrab cu_bounty08/devotion/swampcrab_h01/devotion/swampcrab_h02/devotion/swampcrab_h03/... (champion-hero) factor 1.450 [REFERENT: devotion/swampcrab_h01,devotion/swampcrab_h02,devotion/swampcrab_h03,devotion/swampcrab_h04]
- en-ossuarycrab ghostcrab_h01/ghostcrab_h02/ghostcrab_h03/ghostcrab_h04/... (champion-hero) factor 2.000 [REFERENT: swampcrab_h01,swampcrab_h02,swampcrab_h03,swampcrab_h04,swampcrab_h05]
- en-ossuarycrab swampcrab_ugdenbog_01 (boss) factor 2.800 [roster only]
- en-rimethorn thornedhorrorfrost_b01 (trash) factor 1.308 [roster only]
- en-rimethorn thornedhorrorfrost_c01/thornedhorrorfrost_h01/thornedhorrorfrost_h02/thornedhorrorfrost_h03/... (champion-hero/trash) factor 1.723 [roster only]
- en-rimethorn bl_bounty10 (champion-hero) factor 1.769 [roster only]
- en-statue statue_c01/statue_c02/statue_templeguardian_02/statue_templeguardian_03 (boss/trash) factor 1.402
- en-statue statue_korvaaktombguardian (boss) factor 1.683
- en-voiddrone chthonianservitor_b01/b02 factor 1.709
- en-voiddrone chthonianservitor_c01 factor 2.197
- en-voiddrone hero records h01-h04 factor 2.320
- en-voiddrone chthonianservitor_lunalvalgoth (boss) factor 2.442
- en-voiddrone_boss chthonianservitor_b01/b02 factor 1.709
- en-voiddrone_boss chthonianservitor_c01 factor 2.197
- en-voiddrone_boss hero records h01-h04 factor 2.320
- en-voiddrone_boss chthonianservitor_lunalvalgoth (boss) factor 2.442
- en-voidlord chthonianrylok_a01/gargoyle_a01 (trash) factor 0.625 [roster only]
- en-wraith nemesis_wendigo_02 (nemesis) factor 1.321 [roster only]
- en-wretch wendigocannibal_h01/wendigocannibal_h02/wendigocannibal_h03/wendigocannibal_h04/... (boss/champion-hero) factor 1.389 [roster only]

## Caveats

- The 9 existing blocks (bonegolem, icebrute, magister, mindtaker, statue, voiddrone, voiddrone_boss, warden, witch) are read in unchanged. They use the build target as the base, not the measured h_model; the difference is 0.5 mm or less. The two voiddrone blocks are length-based.
- Class rows in the referent line-up (`*_h0x`, `*_b0x`) mark every record of that stem on the rig. For the crab, `swampcrab_h0x` therefore marks both the scale-1.45 copies (`devotion/`) and the scale-2.0 copies (`hero/`). The footage does not tell them apart.
- Records named `devotion/…` are the roster's devotion-directory copies of a hero record. They are listed separately because their scale can differ from the `hero/` copy.
- crawlerlarva and burrowworm: lane EN-E3 holds their kits (repaint), so they get table rows only. Both are single-scale summon rigs, factor 1.0.
