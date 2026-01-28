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
    screen: str = "home"

    @classmethod
    def new(cls) -> "Game":
        random.seed()

        player = Player(name="Hero")
        player.gold = 35
        player.add_item("potion_small", 1)
        player.add_item("rusty_sword", 1)
        player.add_item("map_crossroads", 1)

        return cls(player=player, screen="home")

    def step(self, line: str) -> CommandResult:
        result = handle_command(self.player, self.enemy, self.game_over, self.screen, line)

        self.enemy = result.enemy
        self.game_over = result.game_over
        self.should_quit = result.should_quit
        self.screen = result.screen or self.screen

        # Force combat screen if enemy is alive
        if (not self.game_over) and self.enemy and self.enemy.is_alive():
            self.screen = "combat"

        # If combat ended and we were on combat screen, return to home
        if (not self.game_over) and (not (self.enemy and self.enemy.is_alive())) and self.screen == "combat":
            self.screen = "home"

        # If player is not in shop, don't stay on shop screen
        if self.screen == "shop" and self.player.location != "shop":
            self.screen = "home"

        return result
