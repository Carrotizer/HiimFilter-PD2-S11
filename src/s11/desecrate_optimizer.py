# Export table to google sheets, download as CSV

import csv
from typing import Dict

from equipment.equipment import BODY_ARMOR_CONFIG, HELM_CONFIG, SHIELD_CONFIG, DruidEquipment, Equipment


def get_desecrate_base_damage_mapping() -> Dict[int, float]:
    """

    :return:
    """
    level_to_avg_dmg = {}
    with open("data/s11_desecrate.csv", buffering=1) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for line in reader:
            skill_level = int(line[0])
            avg_damage = (int(line[1]) + int(line[2])) * (1 + 0.2 * 20 + 0.2 * 20)    # Base + synergy
            level_to_avg_dmg[skill_level] = avg_damage
    return level_to_avg_dmg


PLAGUEBEARER = {
    "name": "Plaguebearer",
    "plus_shapeshifting_skills": 5,
    "sockets": 4
}

BASE_DAMAGE_MAPPING = get_desecrate_base_damage_mapping()
POISON_CREEPER_RES_MAPPING = get_poison_creeper_res_mapping()

def run(enemy_resist: int):
    # Plaguebearer
    plaguebearer = DruidEquipment(**PLAGUEBEARER)
    helms = [DruidEquipment(**helm_config) for helm_config in HELM_CONFIG]
    shields = [DruidEquipment(**shield_config) for shield_config in SHIELD_CONFIG]
    body_armors = [DruidEquipment(**body_armor_config) for body_armor_config in BODY_ARMOR_CONFIG]

    config = {}
    max_damage = -1
    for curr_helm in helms:
        for curr_shield in shields:
            for curr_body_armor in body_armors:
                curr_equip = [plaguebearer, curr_helm, curr_shield, curr_body_armor]
                curr_damage, config = calculate_damage(enemy_resist, curr_equip)
                if curr_damage > max_damage:
                    max_damage = curr_damage
                    print(f"New max: {max_damage} | {curr_helm.name} | {curr_body_armor.name} | {curr_shield.name}")
                    print(f"Rabies Level: {config['rabies_level']}, Poison Creeper Level: {config['poison_creeper_level']}, tooltip: {config['tooltip_damage']}")
                    print(f"Total mastery: {config['mastery']} | Total Pierce: {config['pierce']}")
    return max_damage, config

# Should just take in a list of equipments
def calculate_damage(enemy_resist:int,
                     equipments: list[Equipment]):

    # Annihilus column
    anni_column_plus_skills = 2
    torch_column_plus_skills = 2
    battle_command_plus_skills = 1
    amulet_plus_skills = 2  # Let's set this to 2 for now.  Could consider Third Eye Amulet
    rings_plus_skills = 1

    base_plus_all = anni_column_plus_skills + torch_column_plus_skills + battle_command_plus_skills + amulet_plus_skills + rings_plus_skills
    shapeshift_from_skillers = 8

    glove_mastery = 15
    torch_column_mastery = 3
    base_mastery = glove_mastery + torch_column_mastery

    # base level is everything from non-variable equip
    rabies_base_level = 20 + base_plus_all + shapeshift_from_skillers
    poison_creeper_base_level = 20 + base_plus_all

    equipment_plus_shapeshift = sum([dru_equip.get_total_plus_shapeshifting_skills() for dru_equip in equipments])
    equipment_plus_summon = sum([dru_equip.get_total_plus_summoning_skills() for dru_equip in equipments])
    equip_mastery = sum([equip.get_total_mastery() for equip in equipments])
    equip_pierce = sum([equip.get_total_pierce() for equip in equipments])

    final_rabies_level = rabies_base_level + equipment_plus_shapeshift
    final_poison_creeper_level = poison_creeper_base_level + equipment_plus_summon
    final_mastery = base_mastery + equip_mastery
    final_pierce = equip_pierce + POISON_CREEPER_RES_MAPPING[final_poison_creeper_level]

    tooltip_damage = BASE_DAMAGE_MAPPING[final_rabies_level] * (1 + final_mastery/100.0)

    final_enemy_res = enemy_resist - final_pierce
    if final_enemy_res < 0:
        final_enemy_res = final_enemy_res / 2

    config = {"rabies_level": final_rabies_level,
              "poison_creeper_level": final_poison_creeper_level,
              "mastery": final_mastery,
              "pierce": final_pierce,
              "tooltip_damage": tooltip_damage}
    return tooltip_damage * (100 - final_enemy_res)/100.0, config


if __name__ == "__main__":
    # print(get_rabies_base_damage_mapping())
    run(75)