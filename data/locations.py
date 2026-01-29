from __future__ import annotations

from typing import Dict


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
