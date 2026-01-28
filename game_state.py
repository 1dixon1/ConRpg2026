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
    # Consumables
    "potion_small": Item(
        key="potion_small",
        name="Small Potion",
        desc="Restores 3 HP.",
        price=8,
        item_type="consumable",
        heal=3,
    ),
    "potion_big": Item(
        key="potion_big",
        name="Big Potion",
        desc="Restores 8 HP.",
        price=18,
        item_type="consumable",
        heal=8,
    ),
    # Maps (required to enter locations)
    "map_village": Item(
        key="map_village",
        name="Map: Village",
        desc="Grants access to the Village.",
        price=10,
        item_type="misc",
    ),
    "map_crossroads": Item(
        key="map_crossroads",
        name="Map: Crossroads",
        desc="Grants access to the Crossroads.",
        price=10,
        item_type="misc",
    ),
    "map_cave": Item(
        key="map_cave",
        name="Map: Cave",
        desc="Grants access to the Cave.",
        price=18,
        item_type="misc",
    ),
    "map_ruins": Item(
        key="map_ruins",
        name="Map: Ruins",
        desc="Grants access to the Ruins.",
        price=22,
        item_type="misc",
    ),
    "map_swamp": Item(
        key="map_swamp",
        name="Map: Swamp",
        desc="Grants access to the Swamp.",
        price=25,
        item_type="misc",
    ),
    "map_mountains": Item(
        key="map_mountains",
        name="Map: Mountains",
        desc="Grants access to the Mountains.",
        price=28,
        item_type="misc",
    ),
    "map_castle_gate": Item(
        key="map_castle_gate",
        name="Map: Castle Gate",
        desc="Grants access to the Castle Gate.",
        price=35,
        item_type="misc",
    ),
    "map_crypt": Item(
        key="map_crypt",
        name="Map: Crypt",
        desc="Grants access to the Crypt.",
        price=40,
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
        price=16,
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
        price=14,
        item_type="equip",
        slot="helmet",
        defense=1,
    ),
    "leather_chest": Item(
        key="leather_chest",
        name="Leather Armor",
        desc="Basic chest armor. +2 DEF.",
        price=22,
        item_type="equip",
        slot="chest",
        defense=2,
    ),
    "leather_gloves": Item(
        key="leather_gloves",
        name="Leather Gloves",
        desc="Keeps your hands safe. +1 DEF.",
        price=12,
        item_type="equip",
        slot="gloves",
        defense=1,
    ),
    "leather_boots": Item(
        key="leather_boots",
        name="Leather Boots",
        desc="Light boots. +1 DEF.",
        price=12,
        item_type="equip",
        slot="boots",
        defense=1,
    ),

    # Accessories (2 slots)
    "silver_ring": Item(
        key="silver_ring",
        name="Silver Ring",
        desc="+5% crit chance.",
        price=28,
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
        price=26,
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
]


# Enemy templates (key, name, hp, atk, def, xp, gold)
ENEMIES: Dict[str, Dict] = {
    "wolf": {"name": "Wolf", "hp": 10, "atk": 3, "def": 0, "xp": 25, "gold": 6},
    "goblin": {"name": "Goblin", "hp": 12, "atk": 4, "def": 1, "xp": 35, "gold": 10},
    "bandit": {"name": "Bandit", "hp": 14, "atk": 5, "def": 1, "xp": 45, "gold": 14},
    "shadow": {"name": "Shadow", "hp": 18, "atk": 6, "def": 2, "xp": 70, "gold": 22},
}

ENEMIES_BY_LOCATION: Dict[str, List[str]] = {
    "forest": ["wolf", "goblin"],
    "dark_forest": ["goblin", "bandit", "shadow"],
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


