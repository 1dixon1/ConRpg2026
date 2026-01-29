from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from domain.player import Player
from domain.enemy import Enemy
from commands import CommandResult, handle_command


@dataclass
class Game:
    player: Player
    enemy: Optional[Enemy] = None
    game_over: bool = False
    should_quit: bool = False
    screen: str = "home"

    # (задел под диалоги, пока не используется)
    dialog_npc: Optional[str] = None
    dialog_node: Optional[str] = None

    @classmethod
    def new(cls) -> "Game":
        random.seed()

        player = Player(name="Hero")
        player.gold = 35
        player.add_item("potion_small", 1)
        player.add_item("rusty_sword", 1)
        player.add_item("map_crossroads", 1)

        game = cls(player=player, screen="home")

        # ✅ стартовая инициализация ОДИН раз
        from domain import get_main_chain_start
        game.player.add_quest(get_main_chain_start())
        game.player.add_log("Type 'journal' to open your quest diary.")

        # Засчитываем стартовую локацию как посещённую
        game.player.q_visit[game.player.location] = game.player.q_visit.get(game.player.location, 0) + 1

        return game

    def step(self, line: str) -> CommandResult:
        prev_location = self.player.location

        result = handle_command(self.player, self.enemy, self.game_over, self.screen, line)

        self.enemy = result.enemy
        self.game_over = result.game_over
        self.should_quit = result.should_quit
        self.screen = result.screen or self.screen

        # ✅ visit progress только при смене локации
        if self.player.location != prev_location:
            self.player.q_visit[self.player.location] = (
                self.player.q_visit.get(self.player.location, 0) + 1
            )
            self._check_quests()

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

    def on_kill_enemy(self, enemy_key: str, location_key: str) -> None:
        self.player.q_kill[enemy_key] = self.player.q_kill.get(enemy_key, 0) + 1
        self.player.q_kill_loc[location_key] = self.player.q_kill_loc.get(location_key, 0) + 1
        self._check_quests()

    def on_loot_item(self, item_key: str, amount: int) -> None:
        self.player.q_loot[item_key] = self.player.q_loot.get(item_key, 0) + max(0, amount)
        self._check_quests()

    def _check_quests(self) -> None:
        # ✅ единый источник квестов
        from domain import  quest_done
        from data import ALL_QUESTS

        # Auto-add side quests based on milestones
        if self.player.level >= 2 and "sq_001" not in self.player.active_quests and "sq_001" not in self.player.completed_quests:
            self.player.add_quest("sq_001")
        if self.player.level >= 3 and "sq_002" not in self.player.active_quests and "sq_002" not in self.player.completed_quests:
            self.player.add_quest("sq_002")
        if self.player.level >= 4 and "sq_003" not in self.player.active_quests and "sq_003" not in self.player.completed_quests:
            self.player.add_quest("sq_003")
        if self.player.level >= 5 and "sq_004" not in self.player.active_quests and "sq_004" not in self.player.completed_quests:
            self.player.add_quest("sq_004")

        # Mark quests as ready to claim (UI will show READY)
        for qid in list(self.player.active_quests):
            q = ALL_QUESTS.get(qid)
            if not q:
                continue
            if quest_done(self.player, q):
                pass

    def start_dialog(self, npc_id: str) -> None:
        from data.npcs import NPCS

        npc = NPCS.get(npc_id)
        if not npc:
            self.player.add_log("No such NPC.")
            return

        if npc.get("location") != self.player.location:
            self.player.add_log("That NPC is not here.")
            return

        self.dialog_npc = npc_id
        self.dialog_node = npc.get("start", "start")
        self.player.add_log("Dialog started. Use: choose <number>")

        self.screen = "dialog"

    def end_dialog(self) -> None:
        self.dialog_npc = None
        self.dialog_node = None
        self.screen = "home"

    def dialog_choose(self, index: int) -> None:
        from data.npcs import get_node, npc_name
        from data import ALL_QUESTS

        if not self.dialog_npc or not self.dialog_node:
            self.player.add_log("No dialog active.")
            self.screen = "home"
            return

        node = get_node(self.dialog_npc, self.dialog_node)
        if not node:
            self.player.add_log("Dialog error.")
            self.end_dialog()
            return

        choices = node.get("choices", [])
        if index < 1 or index > len(choices):
            self.player.add_log("Invalid choice.")
            return

        choice = choices[index - 1]

        action = choice.get("action")
        if action:
            atype = action.get("type")
            if atype == "close":
                self.player.add_log(f"You ended the conversation with {npc_name(self.dialog_npc)}.")
                self.end_dialog()
                return

            if atype == "open_shop":
                self.player.add_log("The merchant shows you the goods.")
                self.screen = "shop"
                return

            if atype == "give_quest":
                qid = action.get("qid", "")
                if not qid or qid not in ALL_QUESTS:
                    self.player.add_log("Quest data missing.")
                else:
                    if qid in self.player.completed_quests:
                        self.player.add_log("You already completed that quest.")
                    else:
                        if qid in self.player.active_quests:
                            self.player.add_log("You already have that quest.")
                        else:
                            self.player.add_quest(qid)
                            self.player.add_log("Quest added to your journal.")

        nxt = choice.get("next")
        if nxt:
            self.dialog_node = nxt
        else:
            # If no next, stay on current node
            pass
