from __future__ import annotations

from typing import Dict, List, Tuple


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


SEARCH_ENCOUNTER_CHANCE: Dict[str, float] = {
    "tavern": 0.00,
    "shop": 0.00,
    "forest": 0.30,
    "dark_forest": 0.55,
}
