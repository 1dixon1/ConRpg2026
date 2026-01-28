from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Item:
    key: str
    name: str
    desc: str
    price: int = 0

    item_type: str = "misc"     # "consumable", "equip", "misc"
    slot: str = ""              # weapon, helmet, chest, gloves, boots, accessory

    heal: int = 0

    atk: int = 0
    defense: int = 0
    hp: int = 0

    crit_chance: float = 0.0
    crit_mult: float = 0.0

    # Attribute bonuses
    str_bonus: int = 0
    dex_bonus: int = 0
    con_bonus: int = 0
    wis_bonus: int = 0
    int_bonus: int = 0
    cha_bonus: int = 0


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

    # Base attributes
    strength: int = 5
    dexterity: int = 5
    constitution: int = 5
    wisdom: int = 5
    intelligence: int = 5
    charisma: int = 5

    inventory: Dict[str, int] = field(default_factory=dict)

    equipped: Dict[str, Optional[str]] = field(default_factory=lambda: {
        "weapon": None,
        "helmet": None,
        "chest": None,
        "gloves": None,
        "boots": None,
        "accessory1": None,
        "accessory2": None,
    })

    skills: List[str] = field(default_factory=lambda: ["power_strike", "guard", "focus"])
    cooldowns: Dict[str, int] = field(default_factory=dict)
    buffs: Dict[str, int] = field(default_factory=dict)

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

    def xp_to_next_level(self) -> int:
        return 100 + (self.level - 1) * 50

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

    def tick_cooldowns_and_buffs(self) -> None:
        for k in list(self.cooldowns.keys()):
            self.cooldowns[k] = max(0, self.cooldowns[k] - 1)
            if self.cooldowns[k] == 0:
                self.cooldowns.pop(k, None)

        for k in list(self.buffs.keys()):
            self.buffs[k] = max(0, self.buffs[k] - 1)
            if self.buffs[k] == 0:
                self.buffs.pop(k, None)

    def equipped_item_keys(self) -> List[str]:
        keys: List[str] = []
        for v in self.equipped.values():
            if v:
                keys.append(v)
        return keys

    def get_total_attributes(self, items_by_key: Dict[str, Item]) -> Dict[str, int]:
        s = self.strength
        d = self.dexterity
        c = self.constitution
        w = self.wisdom
        i = self.intelligence
        ch = self.charisma

        for key in self.equipped_item_keys():
            it = items_by_key.get(key)
            if not it:
                continue
            s += it.str_bonus
            d += it.dex_bonus
            c += it.con_bonus
            w += it.wis_bonus
            i += it.int_bonus
            ch += it.cha_bonus

        return {
            "str": s,
            "dex": d,
            "con": c,
            "wis": w,
            "int": i,
            "cha": ch,
        }

    def clamp01(self, x: float, lo: float, hi: float) -> float:
        if x < lo:
            return lo
        if x > hi:
            return hi
        return x

    def get_total_stats(self, items_by_key: Dict[str, Item]) -> Dict[str, float]:
        attrs = self.get_total_attributes(items_by_key)
        s = attrs["str"]
        d = attrs["dex"]
        c = attrs["con"]
        w = attrs["wis"]
        i = attrs["int"]
        ch = attrs["cha"]

        flat_atk = 1
        flat_def = 0
        hp_bonus = 0
        gear_crit_chance = 0.0
        gear_crit_mult = 0.0

        for key in self.equipped_item_keys():
            it = items_by_key.get(key)
            if not it:
                continue
            flat_atk += it.atk
            flat_def += it.defense
            hp_bonus += it.hp
            gear_crit_chance += it.crit_chance
            gear_crit_mult += it.crit_mult

        # Derived combat stats from attributes
        atk = flat_atk + (s * 1.0) + (d * 0.25)
        defense = flat_def + (c * 0.8) + (w * 0.2)

        # Chances
        hit_chance = 0.70 + (d * 0.02) + (w * 0.005)
        evade_chance = 0.03 + (d * 0.01) + (w * 0.003)

        crit_chance = 0.05 + (d * 0.004) + (ch * 0.002) + gear_crit_chance
        crit_mult = 1.50 + (s * 0.01) + gear_crit_mult

        # Buffs
        if "focus" in self.buffs:
            crit_chance += 0.25

        # Clamp
        hit_chance = self.clamp01(hit_chance, 0.10, 0.95)
        evade_chance = self.clamp01(evade_chance, 0.00, 0.60)
        crit_chance = self.clamp01(crit_chance, 0.00, 0.85)
        if crit_mult < 1.10:
            crit_mult = 1.10

        # Extra HP from CON + item bonuses
        hp_bonus += int(c * 0.6)

        return {
            "atk": max(0.0, atk),
            "def": max(0.0, defense),
            "hp_bonus": float(hp_bonus),
            "hit_chance": hit_chance,
            "evade_chance": evade_chance,
            "crit_chance": crit_chance,
            "crit_mult": crit_mult,
            "str": float(s),
            "dex": float(d),
            "con": float(c),
            "wis": float(w),
            "int": float(i),
            "cha": float(ch),
        }

    def apply_hp_bonus(self, items_by_key: Dict[str, Item]) -> None:
        stats = self.get_total_stats(items_by_key)
        base = 10 + (self.level - 1) * 2
        new_max = base + int(stats["hp_bonus"])

        if new_max < 1:
            new_max = 1

        if new_max != self.max_hp:
            ratio = 0.0 if self.max_hp == 0 else (self.hp / self.max_hp)
            self.max_hp = new_max
            self.hp = max(1, min(self.max_hp, int(round(self.max_hp * ratio))))
