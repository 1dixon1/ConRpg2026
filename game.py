from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from enemy import Enemy
from player import Player
from commands import CommandResult, handle_command


@dataclass
class Game:
    player: Player
    enemy: Optional[Enemy] = None
    game_over: bool = False
    should_quit: bool = False

    @classmethod
    def new(cls) -> "Game":
        random.seed()

        player = Player(name="Hero")
        player.gold = 35
        player.add_item("potion_small", 1)
        player.add_item("rusty_sword", 1)

        return cls(player=player)

    def step(self, line: str) -> CommandResult:
        result = handle_command(self.player, self.enemy, self.game_over, line)

        self.enemy = result.enemy
        self.game_over = result.game_over
        self.should_quit = result.should_quit

        return result
