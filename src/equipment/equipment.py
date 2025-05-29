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



HELM_CONFIG = [
    {
        "name": "Jalal's Mane 3OS",
        "plus_skills": 2,
        "plus_shapeshifting_skills": 2,
        "sockets": 3
    },
    {
        "name": "Jalal's Mane +1sk 2OS",
        "plus_skills": 3,
        "plus_shapeshifting_skills": 2,
        "sockets": 2
    },
]

WEAPON_CONFIG = [
    {
        "name": "Plaguebearer 4OS",
        "plus_skills": 5,
        "sockets": 4,
    },
    {
        "name": "Plaguebearer +1sk 2OS",
        "plus_skills": 6,
        "sockets": 2,
    } 
]


SHIELD_CONFIG = [
    {
        "name": "Spirit Ward 3OS",
        "plus_skills": 2,
        "sockets": 3
    },
    {
        "name": "Spirit Ward +1sk 2OS",
        "plus_skills": 3,
        "sockets": 2
    },
    {
        "name": "Stormshield 3OS",
        "plus_skills": 0,
        "sockets": 3
    },
    {
        "name": "Stormshield +1sk 2OS",
        "plus_skills": 1,
        "sockets": 2
    },
]

BODY_ARMOR_CONFIG = [
    {
        "name": "Bramble",
        "mastery": 50,
    },
    {
        "name": "Venom Ward 3OS",
        "plus_skills": 0,
        "pierce": 12,
        "sockets": 3,
    },
    {
        "name": "Venom Ward +1sk 2OS",
        "plus_skills": 1,
        "pierce": 12,
        "sockets": 2,
    },
    # {
    #     "name": "Cage of the Unsullied 6OS",
    #     "plus_skills": 0,
    #     "sockets": 6,
    # },
    # {
    #     "name": "Cage of the Unsullied 6OS +1sk (lol)",
    #     "plus_skills": 1,
    #     "sockets": 6,
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