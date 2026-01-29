from __future__ import annotations

from typing import Dict, List


ENEMIES: Dict[str, Dict] = {
    "street_thug": {"name": "Street Thug", "hp": 13, "atk": 4, "def": 1, "xp": 18, "gold": 6},
    "pickpocket": {"name": "Pickpocket", "hp": 10, "atk": 5, "def": 1, "xp": 16, "gold": 8},
    "feral_dog": {"name": "Feral Dog", "hp": 15, "atk": 6, "def": 1, "xp": 17, "gold": 5},
    "drunk_brawler": {"name": "Drunk Brawler", "hp": 18, "atk": 6, "def": 2, "xp": 20, "gold": 7},

    "wolf": {"name": "Wolf", "hp": 18, "atk": 6, "def": 1, "xp": 18, "gold": 6},
    "boar": {"name": "Wild Boar", "hp": 24, "atk": 7, "def": 2, "xp": 22, "gold": 8},
    "bandit": {"name": "Bandit", "hp": 22, "atk": 7, "def": 2, "xp": 24, "gold": 10},
    "giant_spider": {"name": "Giant Spider", "hp": 20, "atk": 8, "def": 1, "xp": 24, "gold": 9},
    "forest_slime": {"name": "Forest Slime", "hp": 26, "atk": 6, "def": 3, "xp": 26, "gold": 7},

    "cultist": {"name": "Cultist", "hp": 30, "atk": 9, "def": 3, "xp": 36, "gold": 14},
    "wraith": {"name": "Wraith", "hp": 28, "atk": 10, "def": 2, "xp": 38, "gold": 12},
    "dire_wolf": {"name": "Dire Wolf", "hp": 34, "atk": 10, "def": 4, "xp": 44, "gold": 16},
    "dark_spider": {"name": "Dark Spider", "hp": 32, "atk": 11, "def": 3, "xp": 46, "gold": 14},
    "shadow_bandit": {"name": "Shadow Bandit", "hp": 36, "atk": 11, "def": 4, "xp": 52, "gold": 18},

    "bat_swarm": {"name": "Bat Swarm", "hp": 24, "atk": 9, "def": 1, "xp": 34, "gold": 10},
    "cave_slime": {"name": "Cave Slime", "hp": 34, "atk": 8, "def": 5, "xp": 44, "gold": 12},
    "kobold": {"name": "Kobold", "hp": 30, "atk": 10, "def": 3, "xp": 42, "gold": 14},
    "cave_spider": {"name": "Cave Spider", "hp": 28, "atk": 11, "def": 2, "xp": 42, "gold": 13},
    "stone_beetle": {"name": "Stone Beetle", "hp": 38, "atk": 9, "def": 6, "xp": 52, "gold": 16},

    "skeleton": {"name": "Skeleton", "hp": 34, "atk": 11, "def": 4, "xp": 50, "gold": 15},
    "skeletal_archer": {"name": "Skeletal Archer", "hp": 30, "atk": 12, "def": 3, "xp": 52, "gold": 16},
    "ancient_guard": {"name": "Ancient Guard", "hp": 44, "atk": 12, "def": 7, "xp": 70, "gold": 24},
    "ruins_cultist": {"name": "Ruins Cultist", "hp": 36, "atk": 13, "def": 4, "xp": 60, "gold": 20},
    "haunted_armor": {"name": "Haunted Armor", "hp": 52, "atk": 12, "def": 9, "xp": 86, "gold": 30},

    "swamp_leech": {"name": "Swamp Leech", "hp": 30, "atk": 12, "def": 2, "xp": 54, "gold": 16},
    "bog_slime": {"name": "Bog Slime", "hp": 46, "atk": 10, "def": 8, "xp": 78, "gold": 22},
    "swamp_hag": {"name": "Swamp Hag", "hp": 42, "atk": 14, "def": 5, "xp": 82, "gold": 26},
    "giant_frog": {"name": "Giant Frog", "hp": 40, "atk": 13, "def": 4, "xp": 74, "gold": 22},
    "poison_spider": {"name": "Poison Spider", "hp": 38, "atk": 15, "def": 4, "xp": 80, "gold": 24},

    "mountain_bandit": {"name": "Mountain Bandit", "hp": 44, "atk": 14, "def": 6, "xp": 86, "gold": 28},
    "ice_wolf": {"name": "Ice Wolf", "hp": 42, "atk": 15, "def": 5, "xp": 90, "gold": 26},
    "harpy": {"name": "Harpy", "hp": 38, "atk": 16, "def": 4, "xp": 92, "gold": 25},
    "stone_golem": {"name": "Stone Golem", "hp": 70, "atk": 14, "def": 12, "xp": 140, "gold": 45},
    "snow_troll": {"name": "Snow Troll", "hp": 66, "atk": 16, "def": 9, "xp": 150, "gold": 50},

    "royal_guard": {"name": "Royal Guard", "hp": 62, "atk": 17, "def": 11, "xp": 160, "gold": 55},
    "dark_knight": {"name": "Dark Knight", "hp": 78, "atk": 18, "def": 14, "xp": 210, "gold": 75},
    "war_hound": {"name": "War Hound", "hp": 56, "atk": 18, "def": 8, "xp": 150, "gold": 45},
    "gate_mage": {"name": "Gate Mage", "hp": 54, "atk": 19, "def": 8, "xp": 170, "gold": 60},

    "ghoul": {"name": "Ghoul", "hp": 60, "atk": 18, "def": 9, "xp": 180, "gold": 55},
    "lich_apprentice": {"name": "Lich Apprentice", "hp": 58, "atk": 20, "def": 8, "xp": 190, "gold": 65},
    "crypt_wraith": {"name": "Crypt Wraith", "hp": 64, "atk": 20, "def": 10, "xp": 210, "gold": 70},
    "bone_champion": {"name": "Bone Champion", "hp": 86, "atk": 20, "def": 15, "xp": 260, "gold": 90},
    "necromancer": {"name": "Necromancer", "hp": 72, "atk": 22, "def": 12, "xp": 280, "gold": 95},

    "ogre": {"name": "Ogre", "hp": 80, "atk": 19, "def": 12, "xp": 260, "gold": 90},
}


ENEMIES_BY_LOCATION: Dict[str, List[str]] = {
    "tavern": ["drunk_brawler", "pickpocket", "street_thug"],
    "shop": ["pickpocket", "street_thug", "feral_dog"],
    "crossroads": ["feral_dog", "street_thug", "pickpocket", "bandit"],
    "village": ["pickpocket", "street_thug", "drunk_brawler"],
    "forest": ["wolf", "boar", "bandit", "giant_spider", "forest_slime"],
    "dark_forest": ["cultist", "wraith", "dire_wolf", "dark_spider", "shadow_bandit"],
    "cave": ["bat_swarm", "kobold", "cave_spider", "cave_slime", "stone_beetle"],
    "ruins": ["skeleton", "skeletal_archer", "ruins_cultist", "ancient_guard", "haunted_armor"],
    "swamp": ["swamp_leech", "giant_frog", "poison_spider", "bog_slime", "swamp_hag"],
    "mountains": ["mountain_bandit", "ice_wolf", "harpy", "snow_troll", "stone_golem"],
    "castle_gate": ["war_hound", "royal_guard", "gate_mage", "dark_knight"],
    "crypt": ["ghoul", "crypt_wraith", "lich_apprentice", "bone_champion", "necromancer"],
}
