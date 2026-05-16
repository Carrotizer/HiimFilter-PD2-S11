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


def get_charms() -> AssassinEquipment:
    # 9 Grand Charm Martial Arts skillers, Torch, and Annhilus
    return AssassinEquipment(
        name="Charms in Inventory",
        mastery=3, # 3% Large Charm
        plus_all_skills=1, # Anni
        plus_assassin_skills=2, # Torch
        plus_martial_arts_skills=9,
    )


CLAWS = [
    AssassinEquipment(
        name="Firelizard's Talons 3os",
        plus_fire_skills=4,
        pierce=15,
        sockets=3
    ),
    AssassinEquipment(
        name="Firelizard's Talons +1sk 2os",
        plus_all_skills=1,
        plus_fire_skills=4,
        pierce=15,
        sockets=2
    ),
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
    AssassinEquipment(
        name="Magefist (+1 Fire)",
        plus_fire_skills=1,
    ),
    AssassinEquipment(
        name="+3 Martial Arts Gloves",
        plus_martial_arts_skills=3,
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
    AssassinEquipment(
        name="Stone of Jordan (+1sk)",
        plus_all_skills=1,
    ),
    AssassinEquipment(
        name="Raven Frost",
        plus_all_skills=0,
    )
]

AMULETS = [
    AssassinEquipment(
        name="Mara's Kaleidoscope (+2sk)",
        plus_all_skills=2,
    ),
    AssassinEquipment(
        name="Highlord's Wrath (+1sk)",
        plus_all_skills=1,
    ),

]

BOOTS = [
    AssassinEquipment(
        name="Shadow Dancer (+2 Shadow)",
        plus_shadow_disciplines_skills=2, # Doesn't help FoF damage directly
    ),
    AssassinEquipment(
        name="Gore Rider",
        plus_all_skills=0,
    )
]


def get_gear_combinations():
    return itertools.product(
        HELMS,
        AMULETS,
        CLAWS, CLAWS, # Dual wield
        ARMORS,
        GLOVES,
        RINGS, RINGS, # Two rings
        BELTS,
        BOOTS,
        [get_charms()]
    )


def calculate_dps(enemy_res: int = 50):
    lvl_to_dmg = get_fists_of_fire_base_damage_mapping()
    combos = get_gear_combinations()
    
    best_dps = 0.0
    best_gear = None
    
    for gear_tuple in combos:
        gear_set = FistsOfFireEquipmentSet(gear_tuple)
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
        res_after_pierce = enemy_res - pierce
        if res_after_pierce < 0:
            res_after_pierce = res_after_pierce / 2.0

        if res_after_pierce < -100: 
            res_after_pierce = -100

        res_multiplier = (100 - res_after_pierce) / 100.0
        
        final_dmg = total_dmg * res_multiplier
        
        # We'll just use raw hit damage for comparison, 
        # as APS is complex for Martial Arts (charge-up + finisher)
        if final_dmg > best_dps:
            best_dps = final_dmg
            best_gear = gear_tuple

    print(f"Best Charge 3 Meteor Damage (vs {enemy_res}% res): {best_dps:.2f}")
    
    best_gear_set = FistsOfFireEquipmentSet(best_gear)
    final_lvl = best_gear_set.get_final_skill_level()
    if final_lvl > 60: final_lvl = 60
    
    print(f"Final Skill Level: {final_lvl}")
    print(f"Total Mastery: {best_gear_set.get_total_mastery()}%")
    print(f"Total Pierce: {best_gear_set.get_total_pierce()}%")
    print(f"Enemy Resistance: {enemy_res}%")
    
    print("Best Gear Set:")
    for eq in best_gear:
        print(f"  - {eq.name}")


if __name__ == "__main__":
    # Lucion: 30%
    # DClone: 30%
    # Mendeln: 65%, Rathma: 75% (wtf, they have 0% poison res and so much fire res)
    calculate_dps(enemy_res=75)
