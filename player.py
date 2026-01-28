from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Item:
    key: str
    name: str
    desc: str
    price: int = 0

    item_type: str = "misc"   # "consumable", "weapon", "armor", "misc"
    heal: int = 0

    atk: int = 0
    defense: int = 0


@dataclass
class Player:
    name: str = "Hero"
    hp: int = 10
    max_hp: int = 10

    location: str = "tavern"

    level: int = 1
    xp: int = 0
    skill_points: int = 0
    gold: int = 0

    inventory: Dict[str, int] = field(default_factory=dict)

    equipped_weapon: Optional[str] = None
    equipped_armor: Optional[str] = None

    log: List[str] = field(default_factory=lambda: ["Welcome! Type: goto forest"])

    def add_log(self, message: str) -> None:
        self.log.append(message)

    def add_item(self, item_key: str, amount: int = 1) -> None:
        if amount <= 0:
            return
        self.inventory[item_key] = self.inventory.get(item_key, 0) + amount

    def remove_item(self, item_key: str, amount: int = 1) -> bool:
        if amount <= 0:
            return True

        have = self.inventory.get(item_key, 0)
        if have < amount:
            return False

        left = have - amount
        if left <= 0:
            self.inventory.pop(item_key, None)
        else:
            self.inventory[item_key] = left
        return True

    def add_xp(self, amount: int) -> None:
        self.xp += max(0, amount)
        self.add_log(f"You gained {amount} XP.")

        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            self.level += 1
            self.skill_points += 1
            self.max_hp += 2
            self.hp = self.max_hp
            self.add_log(f"Level up! You are now level {self.level}. (+1 skill point, max HP increased)")

    def xp_to_next_level(self) -> int:
        return 100 + (self.level - 1) * 50

    def add_gold(self, amount: int) -> None:
        self.gold += amount
        self.add_log(f"You received {amount} gold.")

    def spend_gold(self, amount: int) -> bool:
        if amount <= 0:
            return True

        if self.gold < amount:
            self.add_log("Not enough gold.")
            return False

        self.gold -= amount
        self.add_log(f"You spent {amount} gold.")
        return True

    def get_atk(self, items_by_key: Dict[str, Item]) -> int:
        base = 1
        bonus = 0
        if self.equipped_weapon and self.equipped_weapon in items_by_key:
            bonus += items_by_key[self.equipped_weapon].atk
        if self.equipped_armor and self.equipped_armor in items_by_key:
            bonus += items_by_key[self.equipped_armor].atk
        return max(0, base + bonus)

    def get_def(self, items_by_key: Dict[str, Item]) -> int:
        base = 0
        bonus = 0
        if self.equipped_weapon and self.equipped_weapon in items_by_key:
            bonus += items_by_key[self.equipped_weapon].defense
        if self.equipped_armor and self.equipped_armor in items_by_key:
            bonus += items_by_key[self.equipped_armor].defense
        return max(0, base + bonus)
