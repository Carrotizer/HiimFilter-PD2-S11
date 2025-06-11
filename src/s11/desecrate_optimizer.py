import csv
from typing import Dict

from equipment.equipment import BODY_ARMOR_CONFIG, HELM_CONFIG, SHIELD_CONFIG, Equipment

from src.equipment.equipment import NecromancerEquipment


def get_desecrate_base_damage_mapping() -> Dict[int, float]:
    """
    :return:
    """
    level_to_avg_dmg = {}
    with open("../../data/s11_desecrate.csv", buffering=1) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for line in reader:
            skill_level = int(line[0])
            avg_damage = (int(line[1]) + int(line[2])) * (1 + 0.2 * 20 + 0.2 * 20) / 2   # Base + synergy
            level_to_avg_dmg[skill_level] = avg_damage
    return level_to_avg_dmg


def get_poison_nova_base_damage_mapping() -> Dict[int, float]:
    """
    :return:
    """
    level_to_avg_dmg = {}
    with open("../../data/s11_poison_nova.csv", buffering=1) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for line in reader:
            skill_level = int(line[0])
            avg_damage = (int(line[1]) + int(line[2])) * (1 + 0.1 * 20 + 0.1 * 20) / 2   # Base + synergy
            level_to_avg_dmg[skill_level] = avg_damage
    return level_to_avg_dmg



D_WEB = {
    "name": "Death's Web 2os",
    "plus_skills": 2,
    "plus_poison_and_bone_skills": 3,
    "pierce": 20,
    "sockets": 2,
}

TRANG_GLOVES = {
    "name": "Trang-Oul's Claws",
    "mastery": 14,
}

BASE_DAMAGE_MAPPING = get_desecrate_base_damage_mapping()
PNOVA_DAMAGE_MAPPING = get_poison_nova_base_damage_mapping()

def run(enemy_resist: int):

    """
    Take Trang set bonus into account.  Set bonus from pieces are already account for in equipment
    Ignore potential Lower Resist curse because of their low effectiveness vs bosses.
    """
    dweb = NecromancerEquipment(**D_WEB)
    trang_gloves = NecromancerEquipment(**TRANG_GLOVES)

    helms = [NecromancerEquipment(**helm_config) for helm_config in HELM_CONFIG]
    shields = [NecromancerEquipment(**shield_config) for shield_config in SHIELD_CONFIG]
    body_armors = [NecromancerEquipment(**body_armor_config) for body_armor_config in BODY_ARMOR_CONFIG]

    config = {}
    max_damage = -1
    charm_config = [(gc , 8 - gc) for gc in range(9)]   # Assume
    for curr_helm in helms:
        for curr_shield in shields:
            for curr_body_armor in body_armors:
                for gc, lc in charm_config:
                    curr_equip = [dweb, trang_gloves, curr_helm, curr_shield, curr_body_armor]
                    curr_damage, config = calculate_damage(enemy_resist, curr_equip, gc, lc, False)
                    if curr_damage > max_damage:
                        max_damage = curr_damage
                        print("----------------------------")
                        print(f"New max: {max_damage} | {curr_helm.name} | {curr_body_armor.name} | {curr_shield.name} | # GC skillers: {gc} | # LC Columns: {lc}")
                        print(f"Desecrate Level: {config['desecrate_level']}, tooltip: {config['tooltip_damage']}")
                        print(f"Total mastery: {config['mastery']} | Total Pierce: {config['pierce']}")
    return max_damage, config

# Should just take in a list of equipments
def calculate_damage(enemy_resist: int,
                     equipments: list[Equipment],
                     gc: int, lc: int, is_vampire_form=False):

    anni_column_plus_skills = 2     # Anni + skiller
    torch_column_plus_skills = 2
    battle_command_plus_skills = 1
    amulet_plus_skills = 2  # Let's set this to 2 for now.  Could consider Third Eye Amulet
    rings_plus_skills = 2

    base_plus_all = anni_column_plus_skills + torch_column_plus_skills + battle_command_plus_skills + amulet_plus_skills + rings_plus_skills
    pnb_from_skillers = gc  # 1 in Anni column accounted above
    mastery_from_charms = 3 * (1 + 2 * lc)    # Just from LC in Torch column

    # base level is everything from non-variable equip
    desecrate_base_level = 20 + base_plus_all + pnb_from_skillers

    equipment_plus_shapeshift = sum([equip.get_total_plus_poison_and_bone_skills() for equip in equipments])
    final_desecrate_level = desecrate_base_level + equipment_plus_shapeshift

    vampire_form_mastery = 20 if is_vampire_form else 0
    total_mastery = vampire_form_mastery + get_total_equipment_mastery(equipments) + mastery_from_charms
    # tooltip_damage = BASE_DAMAGE_MAPPING[final_desecrate_level] * (1 + total_mastery/100.0)
    tooltip_damage = PNOVA_DAMAGE_MAPPING[final_desecrate_level] * (1 + total_mastery/100.0)

    total_pierce = get_total_equipment_pierce(equipments)
    final_enemy_res = enemy_resist - total_pierce
    if final_enemy_res < 0:
        final_enemy_res = final_enemy_res / 2   # 50% effectiveness when < 0

    config = {"desecrate_level": final_desecrate_level,
              "mastery": total_mastery,
              "pierce": total_pierce,
              "tooltip_damage": tooltip_damage}
    return tooltip_damage * (100 - final_enemy_res)/100.0, config


def get_total_equipment_mastery(equipments: list[Equipment]):
    """
    :param equipments:
    :return:
    """
    return sum([equip.get_total_mastery() for equip in equipments])


def get_total_equipment_pierce(equipments: list[Equipment]):
    """
    Equipment pierces
    :param equipments:
    :return:
    """
    return sum([equip.get_total_pierce() for equip in equipments])


if __name__ == "__main__":
    """
    D Clone: 75% Poison Length Reduction.
    Arreat summit poison resist is 95%?
    """

    """
    run(30) # D Clone?  for 6% max life corruption on each one
    New max: 62083.307250000005 | Trang-Oul's Guise 2OS +6% max life | Trang-Oul's Scales 2OS +6% max life | Trang-Oul's Wing 2OS +6% max life | # GC skillers: 8 | # LC Columns: 0
    Desecrate Level: 45, tooltip: 48692.79
    Total mastery: 78 | Total Pierce: 85
    """

    """
    P Nova  Bramble vs Venom Ward with 2/20FCR 3os Circlet
    New max: 17216.962499999998 | +2sk/20FCR 3os Circlet | Bramble | Trang-Oul's Wing 3OS | # GC skillers: 5 | # LC Columns: 3
    Desecrate Level: 44, tooltip: 13503.499999999998
    Total mastery: 126 | Total Pierce: 85
    
    Desecrate Bramble vs Venom Ward
    New max: 77917.08600000001 | +2sk/20FCR 3os Circlet | Bramble | Trang-Oul's Wing 3OS | # GC skillers: 8 | # LC Columns: 0
    Desecrate Level: 47, tooltip: 61111.44
    Total mastery: 108 | Total Pierce: 85
    
    Looks like Venom Ward is better UNTIL 95 enemy resist...
    """



    # import os
    # current_directory = os.getcwd()
    # print(current_directory)
    run(75) # D Clone?