from __future__ import annotations

from typing import Dict, List, Tuple

from player import Item


LOCATIONS: Dict[str, Dict] = {
    "tavern": {
        "title": "Tavern",
        "desc": "Warm lights, loud laughs, and a bowl of stew on the counter.",
        "exits": {"forest": "forest", "shop": "shop"},
    },
    "forest": {
        "title": "Forest",
        "desc": "Tall trees sway in the wind. You hear distant birds.",
        "exits": {"tavern": "tavern", "dark_forest": "dark_forest"},
    },
    "shop": {
        "title": "Shop",
        "desc": "Shelves full of goods. The merchant watches your every move.",
        "exits": {"tavern": "tavern"},
    },
    "dark_forest": {
        "title": "Dark Forest",
        "desc": "The air is cold. Shadows feel too close for comfort.",
        "exits": {"forest": "forest"},
    },
    "crossroads": {
            "title": "Crossroads",
            "desc": "A dusty fork in the road. Signs point in many directions.",
            "exits": {
                "tavern": "tavern",
                "village": "village",
                "forest": "forest",
            },
        },
        "village": {
            "title": "Village",
            "desc": "Small houses, a well, and quiet streets.",
            "exits": {
                "crossroads": "crossroads",
                "shop": "shop",
            },
        },
        "cave": {
            "title": "Cave",
            "desc": "Cold air and dripping water. Something moves in the dark.",
            "exits": {
                "forest": "forest",
                "ruins": "ruins",
            },
        },
        "ruins": {
            "title": "Ruins",
            "desc": "Broken stone walls. Old magic lingers here.",
            "exits": {
                "cave": "cave",
                "swamp": "swamp",
            },
        },
        "swamp": {
            "title": "Swamp",
            "desc": "Wet ground, fog, and strange sounds.",
            "exits": {
                "ruins": "ruins",
                "mountains": "mountains",
            },
        },
        "mountains": {
            "title": "Mountains",
            "desc": "Steep paths and strong winds. The view is breathtaking.",
            "exits": {
                "swamp": "swamp",
                "castle_gate": "castle_gate",
            },
        },
        "castle_gate": {
            "title": "Castle Gate",
            "desc": "A massive gate stands closed. You feel watched.",
            "exits": {
                "mountains": "mountains",
                "crypt": "crypt",
            },
        },
        "crypt": {
            "title": "Crypt",
            "desc": "A sealed underground tomb. The air is heavy.",
            "exits": {
                "castle_gate": "castle_gate",
            },
        },
}


LOCATION_ALIASES = {
    "dark forest": "dark_forest",
    "dark_forest": "dark_forest",
    "darkforest": "dark_forest",
    "tavern": "tavern",
    "forest": "forest",
    "shop": "shop",
}


def normalize_location(raw: str) -> str:
    key = raw.strip().lower()
    key = key.replace(" ", "_")
    key = LOCATION_ALIASES.get(key.replace("_", " "), key)
    key = LOCATION_ALIASES.get(key, key)
    return key


ITEMS: Dict[str, Item] = {
        # Skill Books (learn skills permanently)
    "book_power_strike": Item(
        key="book_power_strike",
        name="Skill Book: Power Strike",
        desc="Learn Power Strike (heavy attack).",
        price=120,
        sell_price=35,
        item_type="misc",
    ),
    "book_guard": Item(
        key="book_guard",
        name="Skill Book: Guard",
        desc="Learn Guard (damage reduction).",
        price=140,
        sell_price=40,
        item_type="misc",
    ),
    "book_focus": Item(
        key="book_focus",
        name="Skill Book: Focus",
        desc="Learn Focus (crit boost).",
        price=150,
        sell_price=45,
        item_type="misc",
    ),
    "book_bleed_strike": Item(
        key="book_bleed_strike",
        name="Skill Book: Bleed Strike",
        desc="Learn Bleed Strike (damage over time).",
        price=180,
        sell_price=55,
        item_type="misc",
    ),
    "book_poison_dart": Item(
        key="book_poison_dart",
        name="Skill Book: Poison Dart",
        desc="Learn Poison Dart (poison over time).",
        price=190,
        sell_price=60,
        item_type="misc",
    ),
    "book_stunning_blow": Item(
        key="book_stunning_blow",
        name="Skill Book: Stunning Blow",
        desc="Learn Stunning Blow (chance to stun).",
        price=220,
        sell_price=70,
        item_type="misc",
    ),
    "book_quick_step": Item(
        key="book_quick_step",
        name="Skill Book: Quick Step",
        desc="Learn Quick Step (evasion boost).",
        price=200,
        sell_price=65,
        item_type="misc",
    ),
    "book_sunder_armor": Item(
        key="book_sunder_armor",
        name="Skill Book: Sunder Armor",
        desc="Learn Sunder Armor (reduce enemy defense).",
        price=240,
        sell_price=80,
        item_type="misc",
    ),
    "book_battle_cry": Item(
        key="book_battle_cry",
        name="Skill Book: Battle Cry",
        desc="Learn Battle Cry (increase attack).",
        price=210,
        sell_price=70,
        item_type="misc",
    ),
    "book_first_aid": Item(
        key="book_first_aid",
        name="Skill Book: First Aid",
        desc="Learn First Aid (heal in combat).",
        price=260,
        sell_price=85,
        item_type="misc",
    ),
    "book_vampiric_hit": Item(
        key="book_vampiric_hit",
        name="Skill Book: Vampiric Hit",
        desc="Learn Vampiric Hit (deal damage and heal).",
        price=320,
        sell_price=110,
        item_type="misc",
    ),
    "book_execute": Item(
        key="book_execute",
        name="Skill Book: Execute",
        desc="Learn Execute (high damage vs low HP enemy).",
        price=360,
        sell_price=120,
        item_type="misc",
    ),

    # Consumables
    "potion_small": Item(
        key="potion_small",
        name="Small Potion",
        desc="Restores 3 HP.",
        price=30,
        item_type="consumable",
        heal=3,
    ),
    "potion_big": Item(
        key="potion_big",
        name="Big Potion",
        desc="Restores 8 HP.",
        price=80,
        item_type="consumable",
        heal=8,
    ),
    # Maps (required to enter locations)
    "map_village": Item(
        key="map_village",
        name="Map: Village",
        desc="Grants access to the Village.",
        price=200,
        item_type="misc",
    ),
    "map_crossroads": Item(
        key="map_crossroads",
        name="Map: Crossroads",
        desc="Grants access to the Crossroads.",
        price=300,
        item_type="misc",
    ),
    "map_cave": Item(
        key="map_cave",
        name="Map: Cave",
        desc="Grants access to the Cave.",
        price=500,
        item_type="misc",
    ),
    "map_ruins": Item(
        key="map_ruins",
        name="Map: Ruins",
        desc="Grants access to the Ruins.",
        price=650,
        item_type="misc",
    ),
    "map_swamp": Item(
        key="map_swamp",
        name="Map: Swamp",
        desc="Grants access to the Swamp.",
        price=2500,
        item_type="misc",
    ),
    "map_mountains": Item(
        key="map_mountains",
        name="Map: Mountains",
        desc="Grants access to the Mountains.",
        price=2800,
        item_type="misc",
    ),
    "map_castle_gate": Item(
        key="map_castle_gate",
        name="Map: Castle Gate",
        desc="Grants access to the Castle Gate.",
        price=3500,
        item_type="misc",
    ),
    "map_crypt": Item(
        key="map_crypt",
        name="Map: Crypt",
        desc="Grants access to the Crypt.",
        price=4000,
        item_type="misc",
    ),

    "torch": Item(
        key="torch",
        name="Torch",
        desc="A simple torch. Might help in dark places.",
        price=6,
        item_type="misc",
    ),

    # Weapon
    "rusty_sword": Item(
        key="rusty_sword",
        name="Rusty Sword",
        desc="Old but usable. +2 ATK.",
        price=20,
        item_type="equip",
        slot="weapon",
        atk=2,
    ),
    "hunter_bow": Item(
        key="hunter_bow",
        name="Hunter Bow",
        desc="Light bow for beginners. +1 ATK, +3% crit.",
        price=56,
        item_type="equip",
        slot="weapon",
        atk=1,
        crit_chance=0.03,
    ),

    # Armor pieces
    "leather_helmet": Item(
        key="leather_helmet",
        name="Leather Helmet",
        desc="Basic helmet. +1 DEF.",
        price=64,
        item_type="equip",
        slot="helmet",
        defense=1,
    ),
    "leather_chest": Item(
        key="leather_chest",
        name="Leather Armor",
        desc="Basic chest armor. +2 DEF.",
        price=82,
        item_type="equip",
        slot="chest",
        defense=2,
    ),
    "leather_gloves": Item(
        key="leather_gloves",
        name="Leather Gloves",
        desc="Keeps your hands safe. +1 DEF.",
        price=52,
        item_type="equip",
        slot="gloves",
        defense=1,
    ),
    "leather_boots": Item(
        key="leather_boots",
        name="Leather Boots",
        desc="Light boots. +1 DEF.",
        price=52,
        item_type="equip",
        slot="boots",
        defense=1,
    ),

    # Accessories (2 slots)
    "silver_ring": Item(
        key="silver_ring",
        name="Silver Ring",
        desc="+5% crit chance.",
        price=78,
        item_type="equip",
        slot="accessory",
        crit_chance=0.05,
    ),
    "lucky_charm": Item(
        key="lucky_charm",
        name="Lucky Charm",
        desc="+0.25 crit multiplier.",
        price=30,
        item_type="equip",
        slot="accessory",
        crit_mult=0.25,
    ),
    "health_amulet": Item(
        key="health_amulet",
        name="Health Amulet",
        desc="+4 Max HP.",
        price=96,
        item_type="equip",
        slot="accessory",
        hp=4,
    ),
        # Loot / Craft materials (sell or later craft)
    "wolf_pelt": Item(
        key="wolf_pelt",
        name="Wolf Pelt",
        desc="A rough pelt. Used for crafting. Sells well.",
        price=0,
        sell_price=12,
        item_type="misc",
    ),
    "slime_gel": Item(
        key="slime_gel",
        name="Slime Gel",
        desc="Sticky gel. Used for potions and glue.",
        price=0,
        sell_price=6,
        item_type="misc",
    ),
    "goblin_ear": Item(
        key="goblin_ear",
        name="Goblin Ear",
        desc="A trophy. Merchants pay a little for it.",
        price=0,
        sell_price=8,
        item_type="misc",
    ),
    "bone_fragment": Item(
        key="bone_fragment",
        name="Bone Fragment",
        desc="Old bone. Good for crafting needles and tools.",
        price=0,
        sell_price=5,
        item_type="misc",
    ),
    "iron_ore": Item(
        key="iron_ore",
        name="Iron Ore",
        desc="Raw ore. Crafting material.",
        price=0,
        sell_price=10,
        item_type="misc",
    ),
    "herbs": Item(
        key="herbs",
        name="Herbs",
        desc="Useful for potions. Can be sold or crafted later.",
        price=0,
        sell_price=4,
        item_type="misc",
    ),
    "ancient_coin": Item(
        key="ancient_coin",
        name="Ancient Coin",
        desc="Old coin from ruins. Collectors love it.",
        price=0,
        sell_price=20,
        item_type="misc",
    ),
    "broken_dagger": Item(
        key="broken_dagger",
        name="Broken Dagger",
        desc="Junk metal. Not usable, but can be sold.",
        price=0,
        sell_price=7,
        item_type="misc",
    ),

}


SHOP_STOCK: List[str] = [
    "potion_small",
    "potion_big",
    "torch",
    "rusty_sword",
    "hunter_bow",
    "leather_helmet",
    "leather_chest",
    "leather_gloves",
    "leather_boots",
    "silver_ring",
    "lucky_charm",
    "health_amulet",
    "map_village",
    "map_crossroads",
    "map_cave",
    "map_ruins",
    "map_swamp",
    "map_mountains",
    "map_castle_gate",
    "map_crypt",
    "book_power_strike",
    "book_guard",
    "book_focus",
    "book_bleed_strike",
    "book_poison_dart",
    "book_stunning_blow",
    "book_quick_step",
    "book_sunder_armor",
    "book_battle_cry",
    "book_first_aid",
    "book_vampiric_hit",
    "book_execute",

]


# Enemy templates (key, name, hp, atk, def, xp, gold)
ENEMIES: Dict[str, Dict] = {
        # --- Crossroads / Village (easy) ---
        "street_thug":     {"name": "Street Thug",      "hp": 13, "atk": 4,  "def": 1, "xp": 18, "gold": 6},
        "pickpocket":      {"name": "Pickpocket",       "hp": 10, "atk": 5,  "def": 1, "xp": 16, "gold": 8},
        "feral_dog":       {"name": "Feral Dog",        "hp": 15, "atk": 6,  "def": 1, "xp": 17, "gold": 5},
        "drunk_brawler":   {"name": "Drunk Brawler",    "hp": 18, "atk": 6,  "def": 2, "xp": 20, "gold": 7},

        # --- Forest (low-mid) ---
        "wolf":            {"name": "Wolf",             "hp": 18, "atk": 6,  "def": 1, "xp": 18, "gold": 6},
        "boar":            {"name": "Wild Boar",        "hp": 24, "atk": 7,  "def": 2, "xp": 22, "gold": 8},
        "bandit":          {"name": "Bandit",           "hp": 22, "atk": 7,  "def": 2, "xp": 24, "gold": 10},
        "giant_spider":    {"name": "Giant Spider",     "hp": 20, "atk": 8,  "def": 1, "xp": 24, "gold": 9},
        "forest_slime":    {"name": "Forest Slime",     "hp": 26, "atk": 6,  "def": 3, "xp": 26, "gold": 7},

        # --- Dark Forest (mid) ---
        "cultist":         {"name": "Cultist",          "hp": 30, "atk": 9,  "def": 3, "xp": 36, "gold": 14},
        "wraith":          {"name": "Wraith",           "hp": 28, "atk": 10, "def": 2, "xp": 38, "gold": 12},
        "dire_wolf":       {"name": "Dire Wolf",        "hp": 34, "atk": 10, "def": 4, "xp": 44, "gold": 16},
        "dark_spider":     {"name": "Dark Spider",      "hp": 32, "atk": 11, "def": 3, "xp": 46, "gold": 14},
        "shadow_bandit":   {"name": "Shadow Bandit",    "hp": 36, "atk": 11, "def": 4, "xp": 52, "gold": 18},

        # --- Cave (mid) ---
        "bat_swarm":       {"name": "Bat Swarm",        "hp": 24, "atk": 9,  "def": 1, "xp": 34, "gold": 10},
        "cave_slime":      {"name": "Cave Slime",       "hp": 34, "atk": 8,  "def": 5, "xp": 44, "gold": 12},
        "kobold":          {"name": "Kobold",           "hp": 30, "atk": 10, "def": 3, "xp": 42, "gold": 14},
        "cave_spider":     {"name": "Cave Spider",      "hp": 28, "atk": 11, "def": 2, "xp": 42, "gold": 13},
        "stone_beetle":    {"name": "Stone Beetle",     "hp": 38, "atk": 9,  "def": 6, "xp": 52, "gold": 16},

        # --- Ruins (mid-hard) ---
        "skeleton":        {"name": "Skeleton",         "hp": 34, "atk": 11, "def": 4, "xp": 50, "gold": 15},
        "skeletal_archer": {"name": "Skeletal Archer",  "hp": 30, "atk": 12, "def": 3, "xp": 52, "gold": 16},
        "ancient_guard":   {"name": "Ancient Guard",    "hp": 44, "atk": 12, "def": 7, "xp": 70, "gold": 24},
        "ruins_cultist":   {"name": "Ruins Cultist",    "hp": 36, "atk": 13, "def": 4, "xp": 60, "gold": 20},
        "haunted_armor":   {"name": "Haunted Armor",    "hp": 52, "atk": 12, "def": 9, "xp": 86, "gold": 30},

        # --- Swamp (hard) ---
        "swamp_leech":     {"name": "Swamp Leech",      "hp": 30, "atk": 12, "def": 2, "xp": 54, "gold": 16},
        "bog_slime":       {"name": "Bog Slime",        "hp": 46, "atk": 10, "def": 8, "xp": 78, "gold": 22},
        "swamp_hag":       {"name": "Swamp Hag",        "hp": 42, "atk": 14, "def": 5, "xp": 82, "gold": 26},
        "giant_frog":      {"name": "Giant Frog",       "hp": 40, "atk": 13, "def": 4, "xp": 74, "gold": 22},
        "poison_spider":   {"name": "Poison Spider",    "hp": 38, "atk": 15, "def": 4, "xp": 80, "gold": 24},

        # --- Mountains (hard) ---
        "mountain_bandit": {"name": "Mountain Bandit",  "hp": 44, "atk": 14, "def": 6, "xp": 86, "gold": 28},
        "ice_wolf":        {"name": "Ice Wolf",         "hp": 42, "atk": 15, "def": 5, "xp": 90, "gold": 26},
        "harpy":           {"name": "Harpy",            "hp": 38, "atk": 16, "def": 4, "xp": 92, "gold": 25},
        "stone_golem":     {"name": "Stone Golem",      "hp": 70, "atk": 14, "def": 12,"xp": 140,"gold": 45},
        "snow_troll":      {"name": "Snow Troll",       "hp": 66, "atk": 16, "def": 9, "xp": 150,"gold": 50},

        # --- Castle Gate (very hard) ---
        "royal_guard":     {"name": "Royal Guard",      "hp": 62, "atk": 17, "def": 11,"xp": 160,"gold": 55},
        "dark_knight":     {"name": "Dark Knight",      "hp": 78, "atk": 18, "def": 14,"xp": 210,"gold": 75},
        "war_hound":       {"name": "War Hound",        "hp": 56, "atk": 18, "def": 8, "xp": 150,"gold": 45},
        "gate_mage":       {"name": "Gate Mage",        "hp": 54, "atk": 19, "def": 8, "xp": 170,"gold": 60},

        # --- Crypt (endgame-ish) ---
        "ghoul":           {"name": "Ghoul",            "hp": 60, "atk": 18, "def": 9, "xp": 180,"gold": 55},
        "lich_apprentice": {"name": "Lich Apprentice",  "hp": 58, "atk": 20, "def": 8, "xp": 190,"gold": 65},
        "crypt_wraith":    {"name": "Crypt Wraith",      "hp": 64, "atk": 20, "def": 10,"xp": 210,"gold": 70},
        "bone_champion":   {"name": "Bone Champion",    "hp": 86, "atk": 20, "def": 15,"xp": 260,"gold": 90},
        "necromancer":     {"name": "Necromancer",      "hp": 72, "atk": 22, "def": 12,"xp": 280,"gold": 95},

        # --- Rare tough enemies (global / optional) ---
        "ogre":            {"name": "Ogre",             "hp": 80, "atk": 19, "def": 12,"xp": 260,"gold": 90},

}

ENEMIES_BY_LOCATION: Dict[str, List[str]] = {
        "tavern"        : ["drunk_brawler", "pickpocket", "street_thug",],
        "shop"          : ["pickpocket", "street_thug", "feral_dog",],
        "crossroads"    : ["feral_dog", "street_thug", "pickpocket", "bandit",],
        "village"       : ["pickpocket", "street_thug", "drunk_brawler",],
        "forest"        : ["wolf","boar", "bandit", "giant_spider", "forest_slime",],
        "dark_forest"   : ["cultist", "wraith", "dire_wolf", "dark_spider", "shadow_bandit", ],
        "cave"          : ["bat_swarm", "kobold", "cave_spider","cave_slime", "stone_beetle",],
        "ruins"         : ["skeleton", "skeletal_archer", "ruins_cultist", "ancient_guard", "haunted_armor",],
        "swamp"         : ["swamp_leech", "giant_frog", "poison_spider", "bog_slime", "swamp_hag",],
        "mountains"     : ["mountain_bandit", "ice_wolf", "harpy", "snow_troll", "stone_golem",],
        "castle_gate"   : ["war_hound", "royal_guard", "gate_mage", "dark_knight",],
        "crypt"         : ["ghoul", "crypt_wraith", "lich_apprentice", "bone_champion", "necromancer",],
}

# (item_key, chance 0..1)
DROPS: List[Tuple[str, float]] = [
    ("wolf_pelt", 0.18),
    ("slime_gel", 0.22),
    ("goblin_ear", 0.15),
    ("bone_fragment", 0.25),
    ("iron_ore", 0.10),
]

OBJECTS_BY_LOCATION: Dict[str, List[str]] = {
    "tavern": ["crate", "barrel"],
    "shop": ["crate", "box"],
    "forest": ["bush", "mushrooms", "crate"],
    "dark_forest": ["bush", "mushrooms", "chest", "crate"],
}


# Search outcome probabilities per location (sum <= 1.0, remaining is "nothing")
# Each entry: (type, key, amount_min, amount_max, chance)
# type: "gold" | "item"
SEARCH_LOOT_TABLE: Dict[str, List[Tuple[str, str, int, int, float]]] = {
    "tavern": [
        ("gold", "gold", 1, 4, 0.25),
        ("item", "potion_small", 1, 1, 0.08),
    ],
    "shop": [
        ("gold", "gold", 1, 6, 0.20),
        ("item", "torch", 1, 1, 0.06),
    ],
    "forest": [
        ("gold", "gold", 2, 10, 0.25),
        ("item", "potion_small", 1, 1, 0.18),
        ("item", "torch", 1, 1, 0.06),
        ("item", "map_crossroads", 1, 1, 0.06),
        ("item", "map_village", 1, 1, 0.04),
        ("item", "herbs", 1, 3, 0.20),
        ("item", "wolf_pelt", 1, 1, 0.08),
        ("item", "iron_ore", 1, 2, 0.06),
        ("item", "broken_dagger", 1, 1, 0.04),
    ],
    "dark_forest": [
        ("gold", "gold", 4, 16, 0.22),
        ("item", "potion_big", 1, 1, 0.12),
        ("item", "torch", 1, 1, 0.10),
        ("item", "map_cave", 1, 1, 0.05),
        ("item", "map_ruins", 1, 1, 0.03),
        ("item", "bone_fragment", 1, 3, 0.18),
        ("item", "ancient_coin", 1, 1, 0.05),
        ("item", "slime_gel", 1, 2, 0.10),
    ],
}


# Encounter chance when using "search"
SEARCH_ENCOUNTER_CHANCE: Dict[str, float] = {
    "tavern": 0.00,
    "shop": 0.00,
    "forest": 0.30,
    "dark_forest": 0.55,
}


