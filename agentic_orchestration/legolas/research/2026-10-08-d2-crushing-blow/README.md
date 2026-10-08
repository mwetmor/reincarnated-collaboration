# Research: D2 Crushing Blow order of operations (JOIN-1 J3d, lever L-07/L-08), 2026-10-08

**Mode:** A (analytical; primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf (JOIN-1 conductor), for gamora's L-07/L-08 JUDGED defaults
**Scope:** read-only. All captures are under `captures/`.

**No local D2 or D2R install exists.** I checked `~/Games/vendor` (Grim Dawn only), `~/depots` (all Grim Dawn depots: 219991 and the related ones) and a depth-5 search of `~` for `*.mpq` and `D2Game.dll`. The only Diablo II files on disk are GeForce NOW screenshots. So there was no disassembly of my own.

## Grading used

| Grade | Meaning here |
|---|---|
| **PRIMARY-DERIVED** | **D2MOO** (`ThePhrozenKeep/D2MOO @ 5596f5cb6c52`). It is a community reconstruction of the D2 **1.10f** game code, "originally extracted using a reverse engineering tool" (`captures/d2moo-README.md` L60–67). Each function is annotated with its original `D2Game.0x…` address. This is disassembly-derived, but it is not Blizzard text and not my own disassembly. **Version caveat:** it is 1.10f, while JOIN-1 pins the LoD **1.13** law. |
| **SECONDARY** | Arreat Summit (hosted by Blizzard at classic.battle.net, and long-standing). Amazon Basin wiki. Maxroll (D2R). |
| **INDICATIVE** | Forum consensus. |

No Blizzard or D2R developer statement on any of these mechanics was found. The D2R patch notes touch Crushing Blow only in 2.4, where the tooltip changed to "+X% Chance of Crushing Blow".

---

## Q-1 · Life before or after the same hit's damage? **BEFORE.**

From D2MOO `SUnitDmg.cpp` `SUNITDMG_ExecuteEvents` (L1065–1310), in order:
1. The hit's damage is already computed and mitigated (`CalculateTotalDamage`: L1126 for missiles, and in `SUNITDMG_AllocCombat` L2674 for melee).
2. On a successful hit, the item events fire: `UNITEVENT_DOMELEEDMG` (L1144) or `UNITEVENT_DOMISSILEDMG` (L1137).
3. Crushing Blow runs inside that event as `SKILLITEM_EventFunc16_CrushingBlow` (`SkillItem.cpp` L1371–1456, `D2Game.0x6FD04E50`). It reads `STAT_HITPOINTS`, which is the target's life before this hit lands, and **writes the new life directly**.
4. Only after that is the hit's physical damage capped to the remaining life (L1149–1150), leech applied, and then `HP -= dwDmgTotal` (L1299–1306).

So **CB = floor(current life ÷ divisor), and the hit's own damage then lands on the reduced life.**

The other sources agree:
- Arreat Summit: *"Since 1.10 Crushing Blow is calculated before your normal damage … then normal damage apply to the resulting lower life"*.
- Basin: *"before the damage of that attack is applied"*.
- Maxroll: *"prior to the attack's damage"*.

**Grade: PRIMARY-DERIVED + SECONDARY ×3. Confidence: HIGH.**

## Q-2 · Does CB damage count toward life or mana leech? **NO.**

Crushing Blow never touches the damage record (`D2DamageStrc`); it writes `STAT_HITPOINTS` directly. Leech is computed from `pDamage->dwPhysDamage` (`SUnitDmg.cpp` L1210–1228 and L1263).
- That value is first capped at the life left **after** CB (L1150). So a CB can also lower the leech cap on the same hit, when the remaining life is below the hit's physical damage.
- The hit's ordinary physical damage still leeches normally.

Forum consensus agrees (purediablo "Life leech and crushing blow", d2jsp t=71487470); this is INDICATIVE. No Arreat, Basin or Maxroll statement was found.

**Grade: PRIMARY-DERIVED (one code source) + INDICATIVE. Confidence: MEDIUM-HIGH.**

## Q-3 · Reduced by physical resist / DR%? **Only positive DR%.**

From the code (`SkillItem.cpp` L1425–1434):
- `CB -= CB·DR%/100` if DR% > 0, with DR% capped at 100. **DR ≥ 100 means CB is fully immune.**
- **Negative DR% does not amplify CB**, so Amplify Damage and Decrepify have no effect on it.
- The raw stat is read, so **a player's or mercenary's 50 % DR ceiling does not apply.**
- **Flat "Damage Reduced by" does not apply**, and neither do absorbs, Bone Armor or Energy Shield.

Basin (CB and Damage Resist pages) and Maxroll say the same; Arreat says "only if the resistance is positive".

**Grade: PRIMARY-DERIVED + SECONDARY ×3. Confidence: HIGH.**

## Other facts about Crushing Blow

**The CB fraction** (divisor; code L1385–1421):

| Target | Melee | Ranged (`DOMISSILEDMG`, event 6) |
|---|---|---|
| Normal, minion, champion and unique monsters | 1/4 | 1/8 |
| Boss or superunique (`MONSTERS_IsBoss` or type-flag 0x02) | 1/8 | 1/16 |
| Player or hireling | 1/10 | 1/20 |

- For monsters the divisor is also raised by the player-count life bonus: `divisor += divisor·HpBonus/100`, with bonus 0/50/100/… % per extra player (`Monster.cpp` L417–430). That equals ×(0.5 + 0.5·players).
- **There is no class or weapon-type factor** other than melee versus missile.
- **The chance** is one roll, `rand % 100 < summed CB%` (L1379–1383). One CB at most per hit.
- **Version:** Arreat's 1.10 statement is the same law as D2MOO's 1.10f code. **No 1.13 or D2R change was found** (INFERRED from absence: 1.13 is not code-verified).

**Interactions:**
- **Deadly Strike / critical hits** double `dwPhysDamage` before the events fire (`FillDamageValues`). CB reads life, not damage, so **crits do not double CB**. Basin and Maxroll agree. Grade: HIGH.
- **Open Wounds** is a separate item event in the same trigger and is independent of CB. It is halved against champions and uniques (type flag 0xC; L1340–1356), and against players it is ÷4, then ÷2 more if ranged.

## Conflicts (stated, not resolved)
- **Arreat Summit lists 1/8 for "Champions, Uniques, Bosses".** D2MOO, Basin and Maxroll give champions and uniques 1/4. The champion/unique-to-0xC mapping is inferred from the standard D2 type-flag layout and from Open Wounds' use of 0xC; the flag enum header itself was not captured. I would weight the code, but the conflict stands.
- **Version.** D2MOO is 1.10f. JOIN-1's law is LoD 1.13, and D2R also matters. A 1.13 D2Game disassembly would settle it, but no binary exists locally.

## Captures (`captures/`, sha256)

```
80782b217a857d69db2a59f32f14e02a989e4512f488b5ea86cbc3ff62232277  arreat-items-magic.shtml   (classic.battle.net/diablo2exp/items/magic.shtml)
da9065053a066a3fc6a867b8efec057cfa2cb828b26630cac6b91f8d9a31e080  basin-crushing-blow-raw.txt (Basin wiki, action=raw)
724e5f4cd012ae4280bf25d3a3ff5a62da1161467605fb41c4b53d4408fca591  basin-Damage_Resist-raw.txt
0af7cecd2583400ceab1464e3108469938206b69eed2da60b0cdbca302da661a  basin-Deadly_Strike-raw.txt
047f2b6a6b8e0585a28e81adeaa263af3001bc6ae380d32019ec7386f5316ce3  basin-Open_Wounds-raw.txt
1045184b945928fe9f55a2806510dca02772b6867a6fd09bc7c685dc56df8696  d2moo-SkillItem.cpp      (D2MOO @5596f5cb6c52…)
56ab5e14f7aceb18681f1c1e720e89c63bfe2a25e2e41b8aa9907652a7c9daf7  d2moo-SUnitDmg.cpp
1c02d9437eb0f9dacb9d7ee04d0065e3c67e5a759bb9f77ef732479a8caa2ac9  d2moo-SUnitEvent.cpp
64f385bef1e008d1d94ab59eb537bfc80fc0bb3fa6b41859d66063028bac614f  d2moo-SUnitEvent.h       (event enum: DOMISSILEDMG = 6)
397a3f250d527a233fa8cd588650d61e7378b271d0483cec0750b14338f1c15a  d2moo-Monster.cpp        (MONSTER_GetHpBonus)
15cae3c152121852e748894914492194e5bb7610c5118d50d14bdb82e0921223  d2moo-MonsterUnique.cpp
b7162a6d8a5d820edf9c924159f99670a4d6153dd9cfb7b944f23739060b5fc8  d2moo-README.md          (1.10f basis)
```

**Not captured, read through WebFetch:**
- Maxroll, *Attack Modifiers* (MacroBioBoi, 2026-02-10): <https://maxroll.gg/d2/resources/attack-modifiers>
- Forum threads: purediablo t/179393, d2jsp t=71487470.

**Prior packet:** `legolas/research/2026-10-01-join1-j4a-d2-ww-barb/formulas.json` F08, F09, F10 and F13. They are consistent with this one; this packet adds the event-order and leech-path code evidence.
