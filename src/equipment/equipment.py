"""
"""


from abc import ABC, abstractmethod


class Equipment:
    def __init__(self, 
                 name: str, 
                 plus_skills: int = 0, 
                 mastery: int = 0,
                 pierce: int = 0,
                 sockets: int = 0):
        self.name = name
        self.plus_skills = plus_skills
        self.mastery = mastery
        self.pierce = pierce
        self.sockets = sockets

    def get_total_mastery(self) -> int:
        return self.mastery + self.sockets * 5

    def get_total_pierce(self) -> int:
        return self.pierce + self.sockets * 5
    

class DruidEquipment(Equipment):
    def __init__(self, name, plus_skills = 0, mastery = 0, pierce = 0, sockets = 0,
                 plus_elemental_skills = 0,
                 plus_shapeshifting_skills = 0,
                 plus_summoning_skills = 0):
        super().__init__(name, plus_skills, mastery, pierce, sockets)
        self.plus_elemental_skills = plus_elemental_skills
        self.plus_shapeshifting_skills = plus_shapeshifting_skills
        self.plus_summoning_skills = plus_summoning_skills

    def get_total_plus_elemental_skills(self):
        return self.plus_skills + self.plus_elemental_skills
    
    def get_total_plus_shapeshifting_skills(self):
        return self.plus_skills + self.plus_shapeshifting_skills

    def get_total_plus_summoning_skills(self):
        return self.plus_skills + self.plus_summoning_skills


class NecromancerEquipment(Equipment):
    def __init__(self, name, plus_skills = 0, mastery = 0, pierce = 0, sockets = 0,
                 plus_curse_skills = 0,
                 plus_poison_and_bone_skills = 0,
                 plus_summoning_skills = 0):
        super().__init__(name, plus_skills, mastery, pierce, sockets)
        self.plus_curse_skills = plus_curse_skills
        self.plus_poison_and_bone_skills = plus_poison_and_bone_skills
        self.plus_summoning_skills = plus_summoning_skills

    def get_total_plus_curse_skills(self):
        return self.plus_skills + self.plus_curse_skills

    def get_total_plus_poison_and_bone_skills(self):
        return self.plus_skills + self.plus_poison_and_bone_skills

    def get_total_plus_summoning_skills(self):
        return self.plus_skills + self.plus_summoning_skills



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
        "name": "Trang-Oul's Wing 2OS +6% max life",
        "plus_skills": 2,
        "sockets": 2,
        "pierce": 25,
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