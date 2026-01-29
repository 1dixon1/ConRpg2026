from __future__ import annotations

from typing import Dict, List, Tuple

from player import Item

from data import (
    LOCATIONS,
    LOCATION_ALIASES,
    normalize_location,
    ITEMS,
    SHOP_STOCK,
    ENEMIES,
    ENEMIES_BY_LOCATION,
    DROPS,
    OBJECTS_BY_LOCATION,
    SEARCH_LOOT_TABLE,
    SEARCH_ENCOUNTER_CHANCE,
)

__all__ = [
    "Item",
    "LOCATIONS",
    "LOCATION_ALIASES",
    "normalize_location",
    "ITEMS",
    "SHOP_STOCK",
    "ENEMIES",
    "ENEMIES_BY_LOCATION",
    "DROPS",
    "OBJECTS_BY_LOCATION",
    "SEARCH_LOOT_TABLE",
    "SEARCH_ENCOUNTER_CHANCE",
]
