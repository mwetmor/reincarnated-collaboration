#!/usr/bin/env python3
"""HALT-4: two-point solve on the sheet windows + ordering discrimination test. DESK-MATH."""
W = (16972.0, 40930.0)     # sheet "Weapon Damage"      (ceremony §D #511)
E = (43691.0, 59761.0)     # sheet "Eye of Reckoning"   (ceremony §D #511)
CRITDMG = 57.0             # sheet "Critical Damage +57%"
WDP_DB = 0.64              # DB-CITED: base 50% @26 + Gutsmasher EoR modifier +14%
WDP_SET = 0.69             # if the Warborn set +5% were live (it is gated OFF, P-E1 §5.3)
SKILL_FLAT = (324.0, 344.0)  # spec §1.3 composed flat, all-physical after conversion

print("== TWO-POINT SOLVE: assume  EoR = w * WeaponDamage + X  (w, X constant across the range) ==")
w = (E[1] - E[0]) / (W[1] - W[0])
X = E[0] - w * W[0]
print(f"   w = {w:.4f}     X = {X:,.0f}")
print(f"   DB-CITED weaponDamagePct @26 = {WDP_DB:.2f}  ->  solved w is {100*(w/WDP_DB-1):+.1f}% off")
print(f"   if the Warborn +5% were live ({WDP_SET:.2f}) -> solved w is {100*(w/WDP_SET-1):+.1f}% off")
print(f"   => the WEAPON-DAMAGE TERM of §1.3 is CONFIRMED to within 5%")
print()
print(f"   the additive term X = {X:,.0f}")
print(f"   §1.3's composed flat is {SKILL_FLAT[0]:.0f}-{SKILL_FLAT[1]:.0f} raw.  For X to be that flat "
      f"times a global %, the global % must be:")
print(f"      +{100*(X/SKILL_FLAT[0]-1):,.0f}%  (using flat_min)   /   +{100*(X/SKILL_FLAT[1]-1):,.0f}%  (using flat_max)")
print(f"   DB-observable %Physical from base items alone = +853% (11 items) ; +Divine Mandate@13 = +996%")
print(f"   at x{1+9.96:.2f} the implied raw skill flat = {X/10.96:,.0f}   -> {X/10.96/SKILL_FLAT[0]:.1f}x "
      f"the enumerated {SKILL_FLAT[0]:.0f}")
print()
print("== SHAPE TESTS ==")
print(f"   weapon-line min/max ratio = {W[1]/W[0]:.3f}     EoR-line min/max ratio = {E[1]/E[0]:.3f}")
print(f"   EoR's range is TIGHTER than the weapon's -> a large near-constant addend dominates.")
print(f"   crit-inclusion test: if the top of the EoR window were a crit, it would be "
      f"{1+CRITDMG/100:.2f}x the bottom = {E[0]*(1+CRITDMG/100):,.0f}; the sheet reads {E[1]:,.0f} "
      f"({100*(E[1]/(E[0]*(1+CRITDMG/100))-1):+.1f}%).  -> the window is NOT a crit band; "
      f"CRIT IS EXCLUDED from the tooltip window.")
print()
print("== ORDERING DISCRIMINATION (conversion before vs after the % modifiers) ==")
FIRE_FLAT = 138.0
PCT_FIRE = 111.0 + 143.0    # base items (2 rings) + Divine Mandate @13, DB-CITED
PCT_PHYS = 853.0 + 143.0    # base items (11) + Divine Mandate @13, DB-CITED
a = FIRE_FLAT * (1 + PCT_PHYS / 100)      # convert first, then take %Physical
b = FIRE_FLAT * (1 + PCT_FIRE / 100)      # take %Fire first, then convert
print(f"   ORDER-1 convert-then-modify : 138 fire -> physical, x(1+{PCT_PHYS:.0f}%) = {a:,.0f}")
print(f"   ORDER-2 modify-then-convert : 138 fire x(1+{PCT_FIRE:.0f}%) = {b:,.0f}, then -> physical")
print(f"   separation = {a-b:,.0f} per tick = {100*(a-b)/X:.1f}% of the solved additive term X")
print(f"   -> DISCRIMINABLE IN PRINCIPLE (a {100*(a-b)/X:.1f}% signal), but NOT with the present stack: "
      f"the un-enumerated remainder of X is {100*(1-(a if a>b else b)/X):.0f}% of it.")
