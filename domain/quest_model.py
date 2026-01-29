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
