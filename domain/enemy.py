from dataclasses import dataclass


@dataclass
class Enemy:
    key: str
    name: str
    max_hp: int
    hp: int
    atk: int
    defense: int
    xp_reward: int
    gold_reward: int

    def is_alive(self) -> bool:
        return self.hp > 0
