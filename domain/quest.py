from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class Quest:
    qid: str
    title: str
    desc: str
    category: str  # "main" or "side"
    objectives: List[str]
    requirements: List[Tuple[str, str, int]]

    reward_gold: int = 0
    reward_xp: int = 0
    reward_items: List[Tuple[str, int]] = None

    next_main_qid: Optional[str] = None

    def __post_init__(self) -> None:
        if self.reward_items is None:
            self.reward_items = []

def get_main_chain_start() -> str:
    return "mq_001"

def quest_done(player, quest: Quest) -> bool:
    """Pure check: is quest completed for the given player progress counters."""
    for kind, key, need in quest.requirements:
        if kind == "visit":
            if player.q_visit.get(key, 0) < need:
                return False
        elif kind == "kill":
            if player.q_kill.get(key, 0) < need:
                return False
        elif kind == "kill_loc":
            if player.q_kill_loc.get(key, 0) < need:
                return False
        elif kind == "loot":
            if player.q_loot.get(key, 0) < need:
                return False
        else:
            # Unknown requirement type: treat as not done
            return False
    return True


def requirement_progress(player, requirement: Tuple[str, str, int]) -> Tuple[str, int, int]:
    """Returns (label, got, need) for a requirement."""
    kind, key, need = requirement
    if kind == "visit":
        return (f"visit {key}", player.q_visit.get(key, 0), need)
    if kind == "kill":
        return (f"kill {key}", player.q_kill.get(key, 0), need)
    if kind == "kill_loc":
        return (f"kill in {key}", player.q_kill_loc.get(key, 0), need)
    if kind == "loot":
        return (f"loot {key}", player.q_loot.get(key, 0), need)
    return (f"{kind} {key}", 0, need)

