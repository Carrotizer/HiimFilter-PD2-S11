import csv
import itertools
import math

from pydantic.v1.fields import MAPPING_LIKE_SHAPES

from equipment.equipment import AssassinEquipment, MindBlastEquipmentSet


def get_mind_blast_base_damage_mapping() -> dict[int, float]:
    """
    Synergy %: 13% per level for Psychic Hammer, Cloak of Shadows, Shadow Warrior
    Total level: 20 * 3

    :return:
    """
    synergy_rate_per_lvl = 0.13
    synergy_total_lvl = 20 * 3
    total_synergy = synergy_total_lvl * synergy_rate_per_lvl
    level_to_avg_dmg = {}
    with open("../../data/s11_mind_blast.csv", buffering=1) as csvfile:
        reader = csv.reader(csvfile)
        ignore_header = next(reader)
        for line in reader:
            skill_level = int(line[0])
            min_dmg = math.floor(int(line[1]) * (1 + total_synergy))
            max_dmg = math.floor(int(line[2]) * (1 + total_synergy))
            avg_damage = 1.0 * (min_dmg + max_dmg) / 2
            level_to_avg_dmg[skill_level] = avg_damage

    # for level, avg_damage in level_to_avg_dmg.items():
    #     # Pretty print with f string
    #     print(f"Level {level:2d}:   Avg Damage = {avg_damage:8.2f}")

    return level_to_avg_dmg


def get_charms(is_bosser: bool = False) -> AssassinEquipment:
    # For bossing, Annihilus would be +2sk
    # 9 Grand Charm skillers, 2 Assassin skill Torch, and Annhilus
    # For season 12, there'd be FCR Large Charm that can help reach FCR breakpoint.
    return AssassinEquipment(
        name="Charms in Inventory",
        plus_all_skills=2 if is_bosser else 1,
        plus_assassin_skills=2,
        plus_shadow_disciplines_skills=9,
        faster_cast_rate=4,
    )

def get_casts_per_second(fcr: int) -> float:
    # Calculate casts per second based on FCR breakpoints for Assassin
    fps = 25.0
    if fcr >= 174:
        return fps / 9
    elif fcr >= 102:
        return fps / 10
    elif fcr >= 65:
        return fps / 11
    elif fcr >= 42:
        return fps / 12
    elif fcr >= 27:
        return fps / 13
    elif fcr >= 16:
        return fps / 14
    elif fcr >= 8:
        return fps / 15
    else:
        return fps / 16


GLOVES = [
    AssassinEquipment(
        name="30% FCR Occultist",
        faster_cast_rate=30,
    ),
    AssassinEquipment(
        name="10% FCR Soul Drainer",
        faster_cast_rate=10,
        pierce=5,
    )
]

# TODO: move these to equipment file
CLAWS = [
    # AssassinEquipment(
    #     name="Shadow Killer +1sk",
    #     plus_all_skills=1,
    #     plus_assassin_skills=0,
    #     plus_shadow_disciplines_skills=4,
    #     faster_cast_rate=20,
    #     pierce=0,
    #     sockets=2
    # ),    Assume physical pierce + extra Shadow Warrior is better QoL.
    AssassinEquipment(
        name="+1sk Whispering Mirage",
        plus_all_skills=1,
        plus_assassin_skills=2,
        faster_cast_rate=10,
        pierce=8,
        sockets=2
    ),
    AssassinEquipment(
        name="20% FCR Whispering Mirage",
        plus_all_skills=0,
        plus_assassin_skills=2,
        faster_cast_rate=20,
        pierce=8,
        sockets=2
    )
]

HELMS = [
    AssassinEquipment(
        name="20% FCR Circlet +1sk",
        plus_all_skills=1,
        plus_assassin_skills=2,
        faster_cast_rate=20,
    ),
    AssassinEquipment(
        name="+1sk +3 Shadow Disc 20% FCR Circlet",
        plus_all_skills=1,
        plus_assassin_skills=0,
        plus_shadow_disciplines_skills=3,
        faster_cast_rate=20,
    ),
    # AssassinEquipment(
    #     name="+1sk Overlord's Helm LOL",
    #     plus_all_skills=1,
    #     pierce=15,
    # )
]

GLOVES = [
    AssassinEquipment(
        name="30% FCR Occultist",
        faster_cast_rate=30,
    ),
    AssassinEquipment(
        name="10% FCR Soul Drainer",
        faster_cast_rate=10,
        pierce=5,
    )
]

MAPPING_BELT = [
    AssassinEquipment(
        name="30% FCR Arachnid Mesh",
        plus_all_skills=1,
        faster_cast_rate=30,
    )
]

BOSSING_BELT = [
    AssassinEquipment(
        name="+2@ Max Res FCR Arachnid Mesh",
        plus_all_skills=1,
        faster_cast_rate=20,
    )
]

RINGS = [
    AssassinEquipment(
        name="30% FCR Constricting Loop",
        faster_cast_rate=30,
    ),
    AssassinEquipment(
        name="10% FCR Bul-Kathos' Wedding Band",
        plus_all_skills=1,
        faster_cast_rate=10,
    ),
]


BOOTS = [
    AssassinEquipment(
        name="Shadow Dancer",
        plus_all_skills=2,
    ),
]

# Gear slots
# Left weapon
# Right weapon
# Helm


AMULETS = [
    AssassinEquipment(
        name="+2sk +3 Shadow Disciplines +10 FCR Magic Amulet",
        plus_all_skills=1,
        plus_shadow_disciplines_skills=3,
        faster_cast_rate=10,
    ),
    AssassinEquipment(
        name="+1sk +3 Shadow Disciplines +20 FCR Magic Amulet",
        plus_all_skills=1,
        plus_shadow_disciplines_skills=3,
        faster_cast_rate=20,
    ),
    AssassinEquipment(
        name="+3 Shadow Disciplines +30 FCR Magic Amulet",
        plus_shadow_disciplines_skills=3,
        faster_cast_rate=30,
    ),
    AssassinEquipment(
        name="+2Sin 20% FCR Caster Craft Amulet",   # For bossing, corrupt has to be +2%
        plus_all_skills=0,
        plus_assassin_skills=2,
        faster_cast_rate=20,
    ),
    AssassinEquipment(
        name="+2sk +2Sin 20% FCR Caster Craft Amulet",
        plus_all_skills=2,
        plus_assassin_skills=2,
        faster_cast_rate=20,
    ),
    AssassinEquipment(
        name="+1sk +2Sin 30% FCR Caster Craft Amulet",
        plus_all_skills=1,
        plus_assassin_skills=2,
        faster_cast_rate=30,
    ),
    AssassinEquipment(
        name="+2Sin 40% FCR Caster Craft Amulet",
        plus_all_skills=0,
        plus_assassin_skills=2,
        faster_cast_rate=40,
    ),


]


def get_mapping_gear_combinations() -> itertools.product:
    left_claws = CLAWS
    right_claws = CLAWS
    armor = [
        AssassinEquipment(
            name="Enigma",
            plus_all_skills=2,
        )
    ]

    left_ring = RINGS
    right_ring = RINGS

    return itertools.product(HELMS,
                             AMULETS,
                             left_claws, right_claws,
                             armor,
                             GLOVES, left_ring, right_ring,
                             MAPPING_BELT,
                             BOOTS,
                             [get_charms(is_bosser=False)],
                             )


def get_rathma_gear_combinations() -> itertools.product:
    """
    Andariel's Visage is forced.
    Belt corruption has to be +2% max @.
    Amulet corruption also has to be +2% max @.

    PLR %: 75 from Natalya's Shadow.  75 from Amulet.  25 from ring gives 175% total.

    :return:
    """
    left_claws = CLAWS
    right_claws = CLAWS
    armor = [
        AssassinEquipment(
            name="Natalya's Shadow +6% Life",   # Could be +1sk or +6% Life.  Doesn't matter.
            plus_shadow_disciplines_skills=3,
        )
    ]
    belt = [

    ]
    left_ring = RINGS
    right_ring = RINGS


def calculate_dps(enemy_res: int = 0, is_bosser: bool = False) -> float:
    # Get equipment combo
    # Get cast rate
    lvl_to_dmg_mapping = get_mind_blast_base_damage_mapping()
    mapping_gears = get_mapping_gear_combinations()
    best_dps = 0.0
    best_gear_set = None
    best_fcr = 0.0
    for gear_set in mapping_gears:
        curr_gear_set = MindBlastEquipmentSet(gear_set)
        avg_dmg = lvl_to_dmg_mapping[curr_gear_set.get_final_skill_level()]
        fcr = curr_gear_set.get_final_faster_cast_rate()
        casts_per_sec = get_casts_per_second(fcr)
        pierce = curr_gear_set.get_total_pierce()
        dps = avg_dmg * casts_per_sec * (100 - enemy_res + pierce) / 100

        # Need to factor in pierce.
        if dps > best_dps:
            best_dps = dps
            best_gear_set = curr_gear_set
            best_fcr = fcr

    print(f"Best DPS: {best_dps:.2f}")
    equipment_pretty_str = "\n".join([f"  - {eq.name}" for eq in best_gear_set.equipments])
    print(f"Best Gear Set:\n{equipment_pretty_str}")
    print(f"Casts per second: {best_fcr:.2f}")
    return best_dps


if __name__ == "__main__":
    # get_mind_blast_base_damage_mapping()
    calculate_dps(enemy_res=50)