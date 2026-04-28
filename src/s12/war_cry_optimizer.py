import csv
import math

from src.s12.mind_blast_optimizer import get_mind_blast_base_damage_mapping


def get_war_cry_base_damage_mapping() -> dict[int, float]:
    """
    110 skill points @ Level 99
    3 points for Leap
    4 points in Combat Masteries
    1 point in Grim Ward for party play
    2 points for Find Item for fun?
    ----100 points remaining for War Cry tree
    20 points in War Cry
    20 points in Battle Cry -> 340%
    20 points in Battle Command -> 260%
    20 Battle Orders -> 13% * 20 = 260%
    1 point in Shout -> 13%
    1 point in Taunt -> 13%
    18 points in Howl -> 17% * 18 = 306%
    Total synergy: 340% + 260% + 260% + 13% + 13% + 306% = 1192%

    :return:
    """
    total_synergy = 11.92
    level_to_avg_dmg = {}
    with open("../../data/s12_war_cry.csv", buffering=1) as csvfile:
        reader = csv.reader(csvfile)
        ignore_header = next(reader)
        for line in reader:
            skill_level = int(line[0])
            min_dmg = math.floor(int(line[1]) * (1 + total_synergy))
            max_dmg = math.floor(int(line[2]) * (1 + total_synergy))
            avg_damage = 1.0 * (min_dmg + max_dmg) / 2
            level_to_avg_dmg[skill_level] = avg_damage

    for level, avg_damage in level_to_avg_dmg.items():
        # Pretty print with f string
        print(f"Level {level:2d}:   Avg Damage = {avg_damage:8.2f}")

    return level_to_avg_dmg

# Note that it's not trivial to reach 200% FCR - it still needs to scrape 26% more somewhere.
# Even though Barbarian casts more per second, Assassin gets 3 Shadows with double Whispering Mirage.
if __name__ == "__main__":
    # Want to compare War Cry base damage with Mind Blast base damage
    # Factor in best Barbarian casting frames is 7 frames at 200% FCR.  Assassin frames are 9 frames at 174% FCR.
    # Barbarian casts per second = 25 / 7 ~= 3.57
    # Assassin casts per second = 25 / 9 ~= 2.78.  So Barbarian has ~28.5% more casts per second.

    get_mind_blast_base_damage_mapping()
    # get_war_cry_base_damage_mapping()
