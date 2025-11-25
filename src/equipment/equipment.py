"""
"""


from abc import ABC, abstractmethod


class Equipment:
    def __init__(self,
                 name: str,
                 plus_all_skills: int = 0,
                 mastery: int = 0,
                 pierce: int = 0,
                 sockets: int = 0):
        self.name = name
        self.plus_all_skills = plus_all_skills
        self.mastery = mastery
        self.pierce = pierce
        self.sockets = sockets

    def get_total_mastery(self) -> int:
        return self.mastery + self.sockets * 5

    def get_total_pierce(self) -> int:
        return self.pierce + self.sockets * 5





class DruidEquipment(Equipment):
    def __init__(self, name, plus_all_skills = 0, mastery = 0, pierce = 0, sockets = 0,
                 plus_elemental_skills = 0,
                 plus_shapeshifting_skills = 0,
                 plus_summoning_skills = 0):
        super().__init__(name, plus_all_skills, mastery, pierce, sockets)
        self.plus_elemental_skills = plus_elemental_skills
        self.plus_shapeshifting_skills = plus_shapeshifting_skills
        self.plus_summoning_skills = plus_summoning_skills

    def get_total_plus_elemental_skills(self):
        return self.plus_all_skills + self.plus_elemental_skills
    
    def get_total_plus_shapeshifting_skills(self):
        return self.plus_all_skills + self.plus_shapeshifting_skills

    def get_total_plus_summoning_skills(self):
        return self.plus_all_skills + self.plus_summoning_skills


class NecromancerEquipment(Equipment):
    def __init__(self, name, plus_all_skills = 0, mastery = 0, pierce = 0, sockets = 0,
                 plus_curse_skills = 0,
                 plus_poison_and_bone_skills = 0,
                 plus_summoning_skills = 0):
        super().__init__(name, plus_all_skills, mastery, pierce, sockets)
        self.plus_curse_skills = plus_curse_skills
        self.plus_poison_and_bone_skills = plus_poison_and_bone_skills
        self.plus_summoning_skills = plus_summoning_skills

    def get_total_plus_curse_skills(self):
        return self.plus_all_skills + self.plus_curse_skills

    def get_total_plus_poison_and_bone_skills(self):
        return self.plus_all_skills + self.plus_poison_and_bone_skills

    def get_total_plus_summoning_skills(self):
        return self.plus_all_skills + self.plus_summoning_skills



class AssassinEquipment(Equipment):
    def __init__(self, name, plus_all_skills = 0, mastery = 0, pierce = 0, sockets = 0,
                 plus_assassin_skills = 0,
                 plus_martial_arts_skills = 0,
                 plus_shadow_disciplines_skills = 0,
                 plus_traps_skills = 0,
                 faster_cast_rate = 0,
                 ):
        super().__init__(name, plus_all_skills, mastery, pierce, sockets)
        self.plus_assassin_skills = plus_assassin_skills
        self.plus_martial_arts_skills = plus_martial_arts_skills
        self.plus_shadow_disciplines_skills = plus_shadow_disciplines_skills
        self.plus_traps_skills = plus_traps_skills
        self.faster_cast_rate = faster_cast_rate

    def get_total_plus_martial_arts_skills(self):
        return self.plus_all_skills + self.plus_assassin_skills + self.plus_martial_arts_skills

    def get_total_plus_shadow_disciplines_skills(self):
        return self.plus_all_skills + self.plus_assassin_skills + self.plus_shadow_disciplines_skills

    def get_total_plus_traps_skills(self):
        return self.plus_all_skills + self.plus_assassin_skills + self.plus_traps_skills

    def get_faster_cast_rate(self):
        return self.faster_cast_rate

    def get_total_pierce(self) -> int:
        # No extra pierce from sockets for Mind Blast
        return self.pierce


# TODO: refactor this to be more generic
class MindBlastEquipmentSet:
    def __init__(self, equipments: tuple[AssassinEquipment]):
        self.equipments = equipments

    def get_final_skill_level(self):
        """
        Base 20 skill points and +1 from Battle Command offhand.
        :return:
        """
        skill_level = 20 + 1
        for equipment in self.equipments:
            skill_level += equipment.get_total_plus_shadow_disciplines_skills()
        return skill_level

    def get_final_faster_cast_rate(self):
        fcr = 0
        for equipment in self.equipments:
            fcr += equipment.get_faster_cast_rate()
        return fcr

    def get_total_pierce(self):
        pierce = 0
        for equipment in self.equipments:
            pierce += equipment.get_total_pierce()
        return pierce



HELM_CONFIG = [
    # {
    #     "name": "Trang-Oul's Guise 3OS",
    #     "plus_skills": 0,
    #     "plus_poison_and_bone_skills": 0,
    #     "sockets": 3
    # },
    # {
    #     "name": "Trang-Oul's Guise +1sk 2OS",
    #     "plus_skills": 1,
    #     "plus_poison_and_bone_skills": 0,
    #     "sockets": 2
    # },
    {
        "name": "Trang-Oul's Guise 2OS +6% max life",
        "plus_skills": 0,
        "plus_poison_and_bone_skills": 0,
        "sockets": 2
    },
    # {
    #     "name": "+2sk/20FCR 3os Circlet",
    #     "plus_skills": 2,
    #     "plus_poison_and_bone_skills": 0,
    #     "sockets": 3,
    # },
    {
        "name": "2os Shako +1sk",
        "plus_skills": 3,
        "plus_poison_and_bone_skills": 0,
        "sockets": 2,
    },
]

SHIELD_CONFIG = [
    # {
    #     "name": "Trang-Oul's Wing +1sk 2OS",
    #     "plus_skills": 3,
    #     "sockets": 2,
    #     "pierce": 25,
    # },
    # {
    #     "name": "Trang-Oul's Wing 3OS",
    #     "plus_skills": 2,
    #     "sockets": 3,
    #     "pierce": 25,   # set bonus
    # },
    {
        "name": "Lucion - Trang-Oul's Wing [Lo Lo Facet]",
        "plus_skills": 2,
        "sockets": 1,
        "pierce": 25,   # set bonus
    },
    # {
    #     "name": "Trang-Oul's Wing 2OS +6% max life",
    #     "plus_skills": 2,
    #     "sockets": 2,
    #     "pierce": 25,
    # },
    # {
    #     "name": "Some insane rare +2sk +3nova/desecrate 3OS",
    #     "plus_skills": 6,   # +2sk, +3sk, 1 from arach free up
    #     "sockets": 3,
    #     "pierce": 0,   # set bonus
    # },
    # {
    #     "name": "Boneflame 3OS",
    #     "plus_skills": 3 + 1,   # 1 from Arach free up
    #     "sockets": 3,
    #     "pierce": 0,   # set bonus
    # },
    {
        "name": "Lucion - Boneflame [Lo Lo Facet]",
        "plus_skills": 3 + 1,   # 1 from Arach free up
        "sockets": 1,
        "pierce": 0,   # set bonus
    },
    {
        "name": "+6 Desecrate 2OS Shrunken Head",
        "plus_skills": 6,   # GG Desecrate
        "sockets": 2,
        "pierce": 0,   # set bonus
    },
]

BODY_ARMOR_CONFIG = [
    # {
    #     "name": "Trang-Oul's Scales +1sk 2OS",
    #     "plus_skills": 0,
    #     "sockets": 2,
    # },
    # {
    #     "name": "Trang-Oul's Scales 3OS",
    #     "plus_skills": 0,
    #     "sockets": 3,
    # },
    {
        "name": "Trang-Oul's Scales 2OS +6% max life",
        "plus_skills": 0,
        "sockets": 2,
    },
    {
        "name": "Bramble",
        "mastery": 50,
        "plus_skills": 0,
        "sockets": 0,
    },
    # {
    #     "name": "Venom Ward 3OS",
    #     "mastery": 0,
    #     "pierce": 12,
    #     "plus_skills": 0,
    #     "sockets": 3,
    # },
    # {
    #     "name": "Arkaine's Valor 3OS",
    #     "mastery": 0,
    #     "pierce": 0,
    #     "plus_skills": 2,
    #     "sockets": 3,
    # },
]

# Each one is 1 column.
# Either 7 or 8, depending on Gheed's.  Do 7 for now?
CHARM_CONFIG = [
    {
        "name": "Grand Charm skiller",
        "plus_skills": 1,
        "sockets": 0,
    },
    {
        "name": "2x Large Charm 3%",
        "plus_skills": 0,
        "mastery": 6,
        "sockets": 0,
    },
]