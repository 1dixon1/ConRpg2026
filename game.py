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
        prev_location = self.player.location
        result = handle_command(self.player, self.enemy, self.game_over, self.screen, line)

        self.enemy = result.enemy
        self.game_over = result.game_over
        self.should_quit = result.should_quit
        self.screen = result.screen or self.screen

        from quests import get_main_chain_start
        self.player.add_quest(get_main_chain_start())
        self.player.add_log("Type 'journal' to open your quest diary.")
        
        if self.player.location != prev_location:
            self.player.q_visit[self.player.location] = (
                self.player.q_visit.get(self.player.location, 0) + 1
            )

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

    def on_visit_location(self, location_key: str) -> None:
        self.player.q_visit[location_key] = self.player.q_visit.get(location_key, 0) + 1
        self._check_quests()

    def on_kill_enemy(self, enemy_key: str, location_key: str) -> None:
        self.player.q_kill[enemy_key] = self.player.q_kill.get(enemy_key, 0) + 1
        self.player.q_kill_loc[location_key] = self.player.q_kill_loc.get(location_key, 0) + 1
        self._check_quests()

    def on_loot_item(self, item_key: str, amount: int) -> None:
        self.player.q_loot[item_key] = self.player.q_loot.get(item_key, 0) + max(0, amount)
        self._check_quests()

    def _check_quests(self) -> None:
        from quests import ALL_QUESTS

        # Auto-add side quests based on simple milestones
        # (пример: после 2 уровня выдать 1–2 сайда)
        if self.player.level >= 2 and "sq_001" not in self.player.active_quests and "sq_001" not in self.player.completed_quests:
            self.player.add_quest("sq_001")
        if self.player.level >= 3 and "sq_002" not in self.player.active_quests and "sq_002" not in self.player.completed_quests:
            self.player.add_quest("sq_002")
        if self.player.level >= 4 and "sq_003" not in self.player.active_quests and "sq_003" not in self.player.completed_quests:
            self.player.add_quest("sq_003")
        if self.player.level >= 5 and "sq_004" not in self.player.active_quests and "sq_004" not in self.player.completed_quests:
            self.player.add_quest("sq_004")

        # Mark quests as ready to claim (we won't auto-claim)
        for qid in list(self.player.active_quests):
            q = ALL_QUESTS.get(qid)
            if not q:
                continue
            if self._quest_done(q):
                # Keep active, but UI will show READY
                pass

    def _quest_done(self, q) -> bool:
        p = self.player
        for kind, key, need in q.requirements:
            if kind == "visit":
                if p.q_visit.get(key, 0) < need:
                    return False
            elif kind == "kill":
                if p.q_kill.get(key, 0) < need:
                    return False
            elif kind == "kill_loc":
                if p.q_kill_loc.get(key, 0) < need:
                    return False
            elif kind == "loot":
                if p.q_loot.get(key, 0) < need:
                    return False
        return True
