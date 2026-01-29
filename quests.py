from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Quest:
    qid: str
    title: str
    desc: str
    category: str  # "main" or "side"
    objectives: List[str]

    # Progress keys: ("visit", "forest"), ("kill", "wolf"), ("loot", "wolf_pelt"), ("gold", "earn")
    requirements: List[Tuple[str, str, int]]

    reward_gold: int = 0
    reward_xp: int = 0
    reward_items: List[Tuple[str, int]] = None

    next_main_qid: Optional[str] = None  # for main quest chain

    def __post_init__(self) -> None:
        if self.reward_items is None:
            self.reward_items = []


def build_quests() -> Dict[str, Quest]:
    # Main quest chain
    quests: Dict[str, Quest] = {
        "mq_001": Quest(
            qid="mq_001",
            title="Main: First Steps",
            desc="Leave the tavern and reach the Crossroads.",
            category="main",
            objectives=["Go to Crossroads."],
            requirements=[("visit", "crossroads", 1)],
            reward_gold=20,
            reward_xp=40,
            reward_items=[("potion_small", 1)],
            next_main_qid="mq_002",
        ),
        "mq_002": Quest(
            qid="mq_002",
            title="Main: Into the Woods",
            desc="Prove yourself by surviving the forest.",
            category="main",
            objectives=["Defeat 3 enemies in the Forest.", "Find herbs by searching."],
            requirements=[("kill_loc", "forest", 3), ("loot", "herbs", 2)],
            reward_gold=35,
            reward_xp=70,
            reward_items=[("map_cave", 1)],
            next_main_qid="mq_003",
        ),
        "mq_003": Quest(
            qid="mq_003",
            title="Main: The Cave Map",
            desc="Explore deeper places and prepare for danger.",
            category="main",
            objectives=["Enter the Cave.", "Defeat a tough cave creature."],
            requirements=[("visit", "cave", 1), ("kill", "stone_beetle", 1)],
            reward_gold=60,
            reward_xp=120,
            reward_items=[("book_guard", 1)],
            next_main_qid="mq_004",
        ),
        "mq_004": Quest(
            qid="mq_004",
            title="Main: Ruins of the Past",
            desc="Old stones hide old threats.",
            category="main",
            objectives=["Enter the Ruins.", "Defeat 5 enemies in Ruins."],
            requirements=[("visit", "ruins", 1), ("kill_loc", "ruins", 5)],
            reward_gold=90,
            reward_xp=180,
            reward_items=[("book_sunder_armor", 1), ("map_swamp", 1)],
            next_main_qid=None,
        ),

        # Side quests (unlocked gradually)
        "sq_001": Quest(
            qid="sq_001",
            title="Side: Collector's Request",
            desc="A merchant pays for trophies.",
            category="side",
            objectives=["Bring 3 Goblin Ears."],
            requirements=[("loot", "goblin_ear", 3)],
            reward_gold=55,
            reward_xp=60,
            reward_items=[],
        ),
        "sq_002": Quest(
            qid="sq_002",
            title="Side: Fur Trader",
            desc="Pelts are always in demand.",
            category="side",
            objectives=["Bring 2 Wolf Pelts."],
            requirements=[("loot", "wolf_pelt", 2)],
            reward_gold=45,
            reward_xp=55,
            reward_items=[],
        ),
        "sq_003": Quest(
            qid="sq_003",
            title="Side: Herbal Remedy",
            desc="A healer needs fresh herbs.",
            category="side",
            objectives=["Gather 6 Herbs."],
            requirements=[("loot", "herbs", 6)],
            reward_gold=70,
            reward_xp=80,
            reward_items=[("potion_big", 1)],
        ),
        "sq_004": Quest(
            qid="sq_004",
            title="Side: Scrap Metal",
            desc="Junk can still be useful.",
            category="side",
            objectives=["Bring 4 Broken Daggers."],
            requirements=[("loot", "broken_dagger", 4)],
            reward_gold=65,
            reward_xp=75,
            reward_items=[],
        ),
    }

    return quests


ALL_QUESTS = build_quests()


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

