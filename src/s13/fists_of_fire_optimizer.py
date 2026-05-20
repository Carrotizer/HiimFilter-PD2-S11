import csv
import itertools

from equipment.equipment import AssassinEquipment


class FistsOfFireEquipmentSet:
    def __init__(self, equipments: tuple[AssassinEquipment]):
        self.equipments = equipments

    def get_final_skill_level(self):
        """
        Base 20 skill points and +1 from Battle Command offhand.
        :return:
        """
        skill_level = 20 + 1
        for equipment in self.equipments:
            # FoF is a Martial Arts skill and a Fire skill
            skill_level += equipment.get_total_plus_martial_arts_skills()
            skill_level += equipment.get_plus_fire_skills()
        return skill_level

    def get_total_mastery(self):
        mastery = 0
        for equipment in self.equipments:
            mastery += equipment.get_total_mastery()
        return mastery

    def get_total_pierce(self):
        pierce = 0
        for equipment in self.equipments:
            pierce += equipment.get_total_pierce()
        return pierce


def get_fists_of_fire_base_damage_mapping() -> dict[int, dict[str, float]]:
    """
    Synergy %: 26% per level for Tiger Strike, Dragon Flight
    Total level: 20 * 2

    :return: Mapping from level to a dict of average damages for Burning, Nova, and Meteor
    """
    synergy_rate_per_lvl = 0.26
    synergy_total_lvl = 20 * 2
    total_synergy = synergy_total_lvl * synergy_rate_per_lvl
    
    level_to_dmg = {}

    with open("./data/S13_Fist_of_Fire.csv", buffering=1) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for line in reader:
            skill_level = int(line[0])
            # Columns: Level, Burning Min, Burning Max, Nova Min, Nova Max, Meteor Min, Meteor Max, ...
            burn_avg = (int(line[1]) + int(line[2])) / 2.0
            nova_avg = (int(line[3]) + int(line[4])) / 2.0
            meteor_avg = (int(line[5]) + int(line[6])) / 2.0
            
            level_to_dmg[skill_level] = {
                "burning": burn_avg * (1 + total_synergy),
                "nova": nova_avg * (1 + total_synergy),
                "meteor": meteor_avg * (1 + total_synergy)
            }

    return level_to_dmg


def get_charms(gc: int, lc: int) -> AssassinEquipment:
    # 10 columns total:
    # - 1 column: Anni (1x1) + 1x GC skiller (1x3)
    # - 1 column: Torch (1x2) + 1x LC 3% (1x2)
    # - 8 columns: either 1x GC skiller OR 2x LC 3% (3% per LC, 6% per column)
    # gc is the number of GCs in the 8 variable columns.
    # lc is the number of LC columns in the 8 variable columns. gc + lc = 8.
    return AssassinEquipment(
        name=f"Charms (GC={gc+1}, LC={lc*2+1})",
        plus_all_skills=1, # Anni
        plus_assassin_skills=2, # Torch
        plus_martial_arts_skills=gc + 1, # +1 from Anni column
        mastery=3 + 6 * lc, # 3 from Torch column, 6 per LC column
    )


CLAWS = [
    AssassinEquipment(
        name="Firelizard's Talons 3os",
        plus_fire_skills=4,
        pierce=15,
        sockets=3
    ),
    # 3os seems better - +1sk here doesn't apply to CtA so less efficient.
    # AssassinEquipment(
    #     name="Firelizard's Talons +1sk 2os",
    #     plus_all_skills=1,
    #     plus_fire_skills=4,
    #     pierce=15,
    #     sockets=2
    # ),
]

HELMS = [
    # AssassinEquipment(
    #     name="Kira's Guardian 3os",
    #     pierce=15, 
    #     sockets=3
    # ),
    # AssassinEquipment(
    #     name="Kira's Guardian +1 2os",
    #     plus_all_skills=1,
    #     pierce=15, 
    #     sockets=2
    # ),
    AssassinEquipment(
        name="Steel Shade +1 2os",
        plus_all_skills=1,
        sockets=2
    ),
    AssassinEquipment(
        name="Circlet 3os",
        plus_assassin_skills=2,
        sockets=3
    )
]

GLOVES = [
    # Rare gloves seem BiS - res, HFD, a lot of good options.    
    # AssassinEquipment(
    #     name="+3 Martial Arts Gloves",
    #     plus_martial_arts_skills=3,
    # ),
    AssassinEquipment(
        name="Hellmouth -10% Enemy Fire Res",
        pierce=10,
    ),
    AssassinEquipment(
        name="20 IAS / +2 MA Crafted Gloves",
        plus_martial_arts_skills=2,
    )
]

ARMORS = [
    AssassinEquipment(
        name="Arkaine's Valor 3os",
        plus_all_skills=2,
        sockets=3
    ),
    AssassinEquipment(
        name="Arkaine's Valor +1sk 2os",
        plus_all_skills=3,
        sockets=2
    ),
]

BELTS = [
    AssassinEquipment(
        name="String of Ears",
        plus_all_skills=0,
    )
]

RINGS = [
    AssassinEquipment(
        name="Bul-Kathos' Wedding Band (+1sk)",
        plus_all_skills=1,
    ),
]

AMULETS = [
    AssassinEquipment(
        name="Mara's Kaleidoscope (+2sk)",
        plus_all_skills=2,
    ),
]

BOOTS = [
    AssassinEquipment(
        name="Shadow Dancer (+2 Shadow)",
        plus_shadow_disciplines_skills=2, # Doesn't help FoF damage directly
    ),
]


def print_gear_set(rank_name: str, final_dmg: float, gear: tuple, enemy_res: int, lvl_to_dmg: dict):
    print(f"{rank_name} Charge 3 Meteor Damage (vs {enemy_res}% res): {final_dmg:.2f}")
    
    gear_set = FistsOfFireEquipmentSet(gear)
    final_lvl = gear_set.get_final_skill_level()
    if final_lvl > 60: final_lvl = 60
    
    print(f"Final Skill Level: {final_lvl}")
    print(f"Total Mastery: {gear_set.get_total_mastery()}%")
    print(f"Total Pierce: {gear_set.get_total_pierce()}%")
    
    # Calculate effective resistance for display
    res_after_pierce = enemy_res - gear_set.get_total_pierce()
    if res_after_pierce < 0:
        res_after_pierce = int(res_after_pierce / 2.0)
    if res_after_pierce < -100:
        res_after_pierce = -100
        
    print(f"Enemy Resistance: {enemy_res}% ({res_after_pierce}% after pierce)")
    
    print(f"{rank_name} Gear Set:")
    print(f"  - Helm: {gear[0].name}")
    print(f"  - Amulet: {gear[1].name}")
    print(f"  - Weapons: {gear[2].name} / {gear[3].name}")
    print(f"  - Armor: {gear[4].name}")
    print(f"  - Gloves: {gear[5].name}")
    print(f"  - Rings: {gear[6].name} / {gear[7].name}")
    print(f"  - Belt: {gear[8].name}")
    print(f"  - Boots: {gear[9].name}")
    print(f"  - {gear[10].name}")
    print("-" * 30)


def calculate_dps(enemy_res: int = 50):
    lvl_to_dmg = get_fists_of_fire_base_damage_mapping()
    
    gear_combos = itertools.product(
        HELMS,
        AMULETS,
        CLAWS, CLAWS, # Dual wield
        ARMORS,
        GLOVES,
        RINGS, RINGS, # Two rings
        BELTS,
        BOOTS
    )
    
    charm_configs = [(gc, 8 - gc) for gc in range(9)]
    
    all_results = []
    
    for gear_tuple in gear_combos:
        for gc, lc in charm_configs:
            charms = get_charms(gc, lc)
            full_gear = gear_tuple + (charms,)
            
            gear_set = FistsOfFireEquipmentSet(full_gear)
            lvl = gear_set.get_final_skill_level()
            if lvl > 60: lvl = 60
            
            # Calculate Meteor damage as primary metric
            base_dmg = lvl_to_dmg[lvl]["meteor"]
            
            mastery = gear_set.get_total_mastery()
            pierce = gear_set.get_total_pierce()
            
            # Total damage = Base * (1 + Mastery/100)
            total_dmg = base_dmg * (1 + mastery / 100.0)
            
            # Resistance factor
            # If enemy resistance is < 0, then the pierce after 0% is halved.
            # Rounded 'against the player' (towards zero for negative resistance)
            res_after_pierce = enemy_res - pierce
            if res_after_pierce < 0:
                res_after_pierce = int(res_after_pierce / 2.0)

            if res_after_pierce < -100: 
                res_after_pierce = -100
            res_multiplier = (100 - res_after_pierce) / 100.0
            
            final_dmg = total_dmg * res_multiplier
            all_results.append((final_dmg, full_gear))

    # Sort by damage descending
    all_results.sort(key=lambda x: x[0], reverse=True)

    # Print top 2
    ranks = ["Best", "2nd Best"]
    for i in range(min(2, len(all_results))):
        dmg, gear = all_results[i]
        print_gear_set(ranks[i], dmg, gear, enemy_res, lvl_to_dmg)



if __name__ == "__main__":
    # Lucion: 30%
    # DClone: 30%
    # Mendeln: 65%, Rathma: 75% (wtf, they have 0% poison res and so much fire res)
    calculate_dps(enemy_res=65)
