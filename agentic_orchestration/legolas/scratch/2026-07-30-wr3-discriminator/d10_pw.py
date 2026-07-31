#!/usr/bin/env python3
"""D10 - can a Plague Walker produce 273.704 under ANY regime? Impact vs aggregated-poison readings."""
PAK_POISON=-38.0   # pak offensiveSlowPoison/DoT modifier family (same slot as SlowCold, -38)
POIS_RES=0.25      # defensivePoison 25 from the necklace (M)
ARMOR=0.30         # 1 - 0.70 armor absorption
print("PLAGUE WALKER (zombie_g01, Common, charLevel 13, armorbase02) vs lastHitBy = 273.704")
print()
print("  (a) SINGLE IMPACT reading -- damagebase_physical01 r13, physical 68-85")
for lbl,f in (("S0_NONE",1.0),("S1_PAK",0.75),("S2_FULL",0.4875)):
    for proc,pl in ((1.0,"base"),(1.35,"+35% proc")):
        v=85*proc*f*ARMOR
        print(f"      {lbl:8s} {pl:10s} = {v:7.2f}   ({273.704/v:5.1f}x short of 273.704)")
print()
print("  (b) AGGREGATED-POISON reading -- zombie_barf 148 + poisongib 133 + acidpool1 89 = 370 raw poison")
for lbl,f in (("S0_NONE",1.0),("S1_PAK",0.75),("S2_FULL",0.4875)):
    plain=370*f*(1-POIS_RES)
    withpak=370*f*(1+PAK_POISON/100)*(1-POIS_RES)
    print(f"      {lbl:8s} poison-resist only = {plain:7.2f}  ({100*(plain-273.704)/273.704:+5.1f}% vs 273.704)"
          f"   |  with pak DoT mod {PAK_POISON:.0f}% = {withpak:6.2f}")
print()
print("  NOTE: (a) fails by 8-14x under every regime -> lastHitBy CANNOT be a single Plague Walker impact.")
print("        (b) S0_NONE lands within 1.4% -- reported as a coincidence-grade fit, NOT as evidence for S0.")
