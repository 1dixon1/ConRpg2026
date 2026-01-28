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
    "torch": Item(
        key="torch",
        name="Torch",
        desc="A simple torch. Might help in dark places.",
        price=6,
        item_type="misc",
    ),
    "rusty_sword": Item(
        key="rusty_sword",
        name="Rusty Sword",
        desc="Old but usable. +2 ATK.",
        price=20,
        item_type="weapon",
        atk=2,
    ),
    "hunter_bow": Item(
        key="hunter_bow",
        name="Hunter Bow",
        desc="Light bow for beginners. +1 ATK.",
        price=16,
        item_type="weapon",
        atk=1,
    ),
    "leather_armor": Item(
        key="leather_armor",
        name="Leather Armor",
        desc="Basic protection. +2 DEF.",
        price=22,
        item_type="armor",
        defense=2,
    ),
    "iron_vest": Item(
        key="iron_vest",
        name="Iron Vest",
        desc="Heavy vest. +4 DEF, -1 ATK.",
        price=35,
        item_type="armor",
        defense=4,
        atk=-1,
    ),
}


SHOP_STOCK: List[str] = [
    "potion_small",
    "potion_big",
    "torch",
    "rusty_sword",
    "hunter_bow",
    "leather_armor",
    "iron_vest",
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
    ("potion_small", 0.25),
    ("torch", 0.10),
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
    ],
    "dark_forest": [
        ("gold", "gold", 4, 16, 0.22),
        ("item", "potion_big", 1, 1, 0.12),
        ("item", "torch", 1, 1, 0.10),
    ],
}


# Encounter chance when using "search"
SEARCH_ENCOUNTER_CHANCE: Dict[str, float] = {
    "tavern": 0.00,
    "shop": 0.00,
    "forest": 0.30,
    "dark_forest": 0.55,
}
