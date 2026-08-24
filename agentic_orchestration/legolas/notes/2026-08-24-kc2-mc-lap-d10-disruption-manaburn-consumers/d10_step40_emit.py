"""D-10 step 40 — EMITTER.  Every row is re-derived here from the binary and the pinned substrate
at emission time; nothing is transcribed from the README.  READ-ONLY on all sources; writes only
the three CSVs and the digest sidecar inside this lap directory.

Outputs
  d10_armed_row_consumers.csv   — the decoded consumer chain, one row per HOP, with the address and
                                  the method that established it
  d10_roster_carriers.csv       — MD-B4-1 (c): every roster/pet body carrying a Disruption or
                                  ManaBurnDrain row, at what value, on which slot, plus reachability
  d10_player_side_consumers.csv — R-D7-2 player-side + the whole influence/armed family, one row per
                                  family, with the Player-vtable occupant and the verdict
  d10_digests.json              — sha256 of every source read and of every emitted file
"""
import sys, os, csv, json, struct, hashlib, pathlib, subprocess
sys.path.insert(0, '.')
import d4b_dis as D
import d8_lib as B

HERE = pathlib.Path(__file__).resolve().parent
KC2 = pathlib.Path.home() / 'Games/reincarnated-engine/data/kc2'
DLL = pathlib.Path('/Users/admin/Games/vendor/grim-dawn/Game.dll')
ARZ_GDX1 = pathlib.Path.home() / 'Games/vendor/grim-dawn/gdx1/database/GDX1.arz'
pe = D.pe


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def vslot(vft_symbol, off):
    base = D.EX[vft_symbol]
    v = struct.unpack_from('<I', pe.raw, pe.rva2off(base + off))[0] - D.IB
    return v, D.nearest(v)


def first_bytes(rva, n=6):
    return pe.at(rva, n).hex()


# ---------------------------------------------------------------- 1 · consumer chain
CHAIN = []


def hop(family, n, what, rva, method, note):
    CHAIN.append(dict(family=family, hop=n, what=what,
                      rva=f'{rva:#010x}' if isinstance(rva, int) else rva,
                      symbol=D.nearest(rva) if isinstance(rva, int) else '',
                      first_bytes=first_bytes(rva) if isinstance(rva, int) else '',
                      method=method, note=note))


# --- Disruption
hop('Disruption', 1, 'record field -> attribute value',
    D.EX['?GetLoadValueMinTag@DamageAttributeAbs_Disruption@GAME@@MBEPBDXZ'],
    'DECODED', 'returns the C-string "%s"' % pe.cstr(
        int([l for l in B.bounded(D.EX['?GetLoadValueMinTag@DamageAttributeAbs_Disruption@GAME@@MBEPBDXZ'], 6)
             if 'mov      eax' in l][0].split('eax, ')[1], 16) - D.IB))
hop('Disruption', 2, 'mitigation (applied BEFORE Execute)', 0x000d7620, 'DECODED',
    'ReduceDamage@CombatAttributeAbsDamage: if type==self.type -> v *= (1-r/100); then max(v,0). '
    'Disruption does NOT override slot 21, so it inherits this exact law (D-7 s2 scalar).')
hop('Disruption', 3, 'Execute: seconds -> integer MILLISECONDS', 0x000dc9e0, 'DECODED',
    'if v<=0 return; v*=1000.0; cvttss2si; tailcall target->vtable[+0x3d0](int ms). '
    'The x1000 + int-truncate IS the units proof: the field is SECONDS.')
_r, _n = vslot('??_7Player@GAME@@6BObject@1@@', 0x3d0)
hop('Disruption', 4, 'Player vtable +0x3d0', _r, 'DECODED',
    f'{_n} — a REAL Character impl; Player does NOT override it (contrast Confusion/Fear/Taunt).')
hop('Disruption', 5, 'Character -> SkillManager', 0x004454d0, 'DECODED',
    'CombatAddCooldownDamage: (float)ms -> SkillManager::ApplyCooldownDamage at this+0x600.')
hop('Disruption', 6, 'SkillManager fan-out', 0x004454d0, 'DECODED',
    'walks FOUR skill containers (+0x154/+0x158, +0x8c, +0x174/+0x178, +0x1f8/+0x1fc) and calls '
    'skill->vtable[+0x144](ms) on EVERY skill in each.')
hop('Disruption', 7, 'per-skill gate', 0x003bf110, 'DECODED',
    'ApplyDisruptionCooldownTime: if (this->[+0xca]) ReplaceCooldownTime(ms, 0.0). '
    '+0xca is a CTOR-SET class constant, not a DBR field.')
hop('Disruption', 8, 'the write', 0x003bf0b0, 'DECODED',
    'ReplaceCooldownTime(newMs, 0): if newMs<=0 return; if newMs <= (float)[+0x150] return  '
    '=> LONGEST-WINS, never additive; else [+0x150]=(int)newMs, [+0x154]=(int)newMs, '
    '[+0x80]=1 (reason=ON_COOLDOWN), [+0x86]=1.')
hop('Disruption', 9, 'the effect on usability', 0x003bf880, 'DECODED',
    'SetAvailability: [+0x86] = ([+0x150] > 0); if (!ignoreCooldown && [+0x86]) -> [+0x80]=1, return false.')

# --- ManaBurnDrain
hop('ManaBurnDrain', 1, 'record field -> attribute value',
    D.EX['?GetLoadValueMinTag@DamageAttributeAbs_ManaBurn@GAME@@MBEPBDXZ'], 'DECODED',
    'returns the C-string "offensiveManaBurnDrainMin"; the ratio limb is '
    '"offensiveManaBurnDamageRatio" (GetLoadDamageRatioTag).')
hop('ManaBurnDrain', 2, 'mitigation', 0x000dce40, 'DECODED',
    'ReduceDamage@..._ManaBurn OVERRIDES the base: drain [+0x1c] reduced when type in '
    '{self.type, 0x0c ManaBurn, 0x15 ManaLeach}; ratio [+0x2c] reduced when type==0x3e ManaBurnRatio. '
    'Both clamped >=0.')
hop('ManaBurnDrain', 3, 'Execute: value is a PERCENT of the MANA LIMIT', 0x000dcc90, 'DECODED',
    'inlines Character::GetManaLimit() byte-for-byte ([+0xa9c] base, [+0xb84] %mod, [+0xc6c] scale, '
    'same constants/branch/abs); burn = min(v*0.01*ManaLimit, CurrentMana[+0xa54]). NO x1000 anywhere '
    '=> NOT a duration.')
hop('ManaBurnDrain', 4, 'the energy write', 0x000dcc90, 'DECODED',
    'if (!target->[+0x1847]) { target->[+0x10f8]=1; target->[+0xa5c]+=burn; target->[+0x1320]+=burn; }')
hop('ManaBurnDrain', 5, 'the OPTIONAL health limb', 0x000e0a40, 'DECODED',
    'x = ratio[+0x2c]*0.01*burn; if (x>0) CombatManager::ApplyDamage(&target[+0x3dc], x, ...). '
    'Gated on the ratio being > 0.')
hop('ManaBurnDrain', 6, 'the DAMAGE-TOTAL exclusion', 0x0003e4c0, 'DECODED',
    'both Disruption and ManaBurn override GetTotalDamage (slot 9/17) and GetMinMaxDamage (slot 14) '
    'with CombatAttribute:: no-op stubs (ret 0xc / ret 0x14). The base CombatAttributeAbsDamage '
    'versions ADD [+0x1c] into the running total; these do not.')

# --- the carrier skill (SkillBuff_DispelMagic) — the ManaBurn row's own delivery vehicle
hop('ManaBurnDrain-carrier', 7, 'the carrier skill class', 0x003cc730, 'DECODED',
    'SkillBuff_DispelMagic::Install -> on the HOSTILE branch calls target->vtable[+0x320] '
    'Character::DispelSkillBuffs() and THEN runs the attack. dispelFriendly/dispelDamageOverTime '
    'govern only the same-faction branch.')
hop('ManaBurnDrain-carrier', 8, 'what a dispel actually removes', 0x004356f0,
    'DECODED-WITHIN-THE-SkillBuff-FAMILY',
    'SkillManager::DispelSkillBuffs walks a buff container (SkillManager+0x88) calling '
    'vtable[+0x340](Character*). WITHIN the SkillBuff_* family +0x340 is DispelBuff: '
    'SkillBuff::DispelBuff is the shared ret-4 stub and ONLY SkillBuff_{Passive,PassiveCharged,'
    'PassiveEndless,PassiveShield,BuffImmobilize} override it. ⚑ SCOPE GUARD: +0x340 is NOT the same '
    'virtual outside that family (Skill_Passive+0x340 = Load@SkillActivated, '
    'Skill_AttackRadiusSpin+0x340 = StartAction), so the slot may NOT be read as a dispel verdict for '
    'the DBR-declared player passive classes. Which of the pilot Skill_Passive* records instantiate a '
    'SkillBuff_Passive into that container is UNDERIVABLE here — see README R-D10-1.')

with open(HERE / 'd10_armed_row_consumers.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(CHAIN[0].keys()))
    w.writeheader()
    w.writerows(CHAIN)

# ---------------------------------------------------------------- 2 · roster carriers
dmg = list(csv.DictReader(open(KC2 / 'pm2_tg2_attack_damage.csv')))
pools = list(csv.DictReader(open(KC2 / 'pe6_crucible_wave_pools_v2.csv')))

reach = {}
for p in pools:
    for rec in [x.strip() for x in p.get('roster_records', '').split('|') if x.strip()]:
        reach.setdefault(rec, []).append(p)

rows = []
for x in dmg:
    if x['damage_type'] not in ('Disruption', 'ManaBurnDrain'):
        continue
    rec = x['record']
    hits = reach.get(rec, [])
    t16 = [h for h in hits if int(h['tier']) <= 16]
    first = min((int(h['global_wave']) for h in hits), default=None)
    rows.append(dict(
        damage_type=x['damage_type'], kind_in_csv=x['kind'], actor_kind=x['actor_kind'],
        record=rec, display_name=x['display_name'], stratum=x['stratum'],
        level_used=x['level_used'], surface=x['surface'], slot=x['slot'],
        tree_index=x['tree_index'], skill=x['skill'], skill_class=x['skill_class'],
        rank_used=x['rank_used'], rank_grade=x['rank_grade'],
        min_value=x['min'], max_value=x['max'] or 'ABSENT',
        decoded_unit=('seconds (duration)' if x['damage_type'] == 'Disruption'
                      else 'percent of target ManaLimit (magnitude)'),
        decoded_dbr_field=('offensiveDisruptionMin' if x['damage_type'] == 'Disruption'
                           else 'offensiveManaBurnDrainMin'),
        skill_target_number=x['skill_target_number'], skill_target_angle=x.get('skill_target_angle', ''),
        n_pool_appearances=len(hits),
        first_reachable_global_wave=(first if first is not None else 'NEVER-POOLED'),
        tier16_or_below_entries='; '.join(
            f"gw{h['global_wave']}/sp{h['spawn_point']}/n={h['roster_n']}/{h['pool_record'].split('/')[-1]}"
            for h in t16) or 'NONE',
        uniform_draw_p_at_first_entry=(
            f"1/{t16[0]['roster_n']}" if t16 else 'n/a'),
        provenance='pm2_tg2_attack_damage.csv + pe6_crucible_wave_pools_v2.csv',
        grade='MEASURED'))
with open(HERE / 'd10_roster_carriers.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(sorted(rows, key=lambda r: (r['damage_type'], r['surface'], r['slot'], r['tree_index'])))

# ---------------------------------------------------------------- 3 · player-side consumers
FAM = [
    # (family, enum, attribute class, Execute rva, Character-vtable slot,
    #  SECOND hop as (ControllerPlayer vtable slot) or None, note)
    # ⚑ The second hop is NOT decoration. Fear and Taunt occupy a REAL Character:: function that
    #    forwards to the CONTROLLER; a one-hop reading calls them "REAL on Player" and is WRONG.
    ('Disruption', 13, 'CombatAttributeAbsDamage_Disruption', 0x000dc9e0, 0x3d0, None,
     'value x1000 -> int ms; hop 2 is a DIRECT (non-virtual) call into the Character own SkillManager'),
    ('ManaBurnDrain', 12, 'CombatAttributeAbsDamage_ManaBurn', 0x000dcc90, None, None,
     'no vtable hop at all; Execute writes Character fields directly'),
    ('Convert', 51, 'CombatAttributeInfluenceDamage_Convert', 0x000dd010, 0x30c, None,
     'value x1000 -> int ms, gated on casterConvertLevel+5 >= targetLevel'),
    ('Confusion', 53, 'CombatAttributeInfluenceDamage_Confusion', 0x000dd100, 0x3c8, None,
     'D-7 s3.4 reproduced'),
    ('Fear', 52, 'CombatAttributeInfluenceDamage_Fear', 0x000dd100, 0x3c4, 0x84,
     'D-7 s3.4 reproduced — Character impl is real, the CONTROLLER slot is the stub'),
    ('Taunt', 50, 'CombatAttributeInfluenceDamage_Taunt', 0x000dcf30, 0x3cc, 0x8c,
     'D-7 s3.4 reproduced — Character impl is real, the CONTROLLER slot is the stub'),
    ('LifeLeech', 20, 'CombatAttributeAbsDamage_LifeLeech', 0x000dcbb0, 0x3d4, None,
     'for contrast: a real one-hop write to Character+0x4d4'),
]
STUBS = {0x000084d0: 'shared ret-4 stub', 0x0003e4b0: 'shared ret-0x10 stub',
         0x0000f100: 'shared ret-8 stub', 0x0003e4c0: 'shared ret-0xc stub'}
prow = []
for fam, enum, cls, ex, slot, ctrl_slot, note in FAM:
    hop2 = ''
    if slot is None:
        po = mo = '(no vtable hop)'
        verdict = 'REAL on Player — writes Character fields directly'
    else:
        pr, pn = vslot('??_7Player@GAME@@6BObject@1@@', slot)
        mr, mn = vslot('??_7Monster@GAME@@6BObject@1@@', slot)
        po, mo = f'{pn} @ {pr:#010x}', f'{mn} @ {mr:#010x}'
        if pr in STUBS:
            verdict = f'PLAYER NO-OP ({STUBS[pr]}) at hop 1'
        elif ctrl_slot is not None:
            cr, cn = vslot('??_7ControllerPlayer@GAME@@6B@', ctrl_slot)
            hop2 = f'ControllerPlayer+{ctrl_slot:#05x} -> {cn} @ {cr:#010x}'
            verdict = (f'PLAYER NO-OP ({STUBS[cr]}) at hop 2' if cr in STUBS
                       else 'REAL on Player through the controller')
        else:
            verdict = 'REAL on Player'
    prow.append(dict(
        family=fam, combat_attribute_enum=enum, attribute_class=cls,
        execute_rva=f'{ex:#010x}',
        character_vtable_slot=(f'+{slot:#05x}' if slot else ''),
        player_vtable_occupant=po, monster_vtable_occupant=mo,
        second_hop=hop2 or '(none)',
        player_side_verdict=verdict, note=note,
        method='DECODED', grade='MEASURED'))
with open(HERE / 'd10_player_side_consumers.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(prow[0].keys()))
    w.writeheader()
    w.writerows(prow)

# ---------------------------------------------------------------- 4 · digests
dig = dict(
    sources={
        'Game.dll': sha(DLL),
        'GDX1.arz': sha(ARZ_GDX1),
        'pm2_tg2_attack_damage.csv': sha(KC2 / 'pm2_tg2_attack_damage.csv'),
        'pe6_crucible_wave_pools_v2.csv': sha(KC2 / 'pe6_crucible_wave_pools_v2.csv'),
        'pm2_measured_player_sheet.csv': sha(KC2 / 'pm2_measured_player_sheet.csv'),
        'pm4g_played_kit.csv': sha(KC2 / 'pm4g_played_kit.csv'),
    },
    emitted={},
    counts=dict(consumer_hops=len(CHAIN), carrier_rows=len(rows), family_rows=len(prow)),
)
for n in ('d10_armed_row_consumers.csv', 'd10_roster_carriers.csv', 'd10_player_side_consumers.csv'):
    dig['emitted'][n] = sha(HERE / n)
with open(HERE / 'd10_digests.json', 'w') as f:
    json.dump(dig, f, indent=2, sort_keys=True)
print(json.dumps(dig, indent=2, sort_keys=True))
