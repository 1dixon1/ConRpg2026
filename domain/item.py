from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    key: str
    name: str
    desc: str
    price: int
    sell_price: int = 0
    item_type: str = "misc"

    slot: Optional[str] = None
    atk: int = 0
    defense: int = 0
    hp: int = 0

    crit_chance: float = 0.0
    crit_mult: float = 0.0
