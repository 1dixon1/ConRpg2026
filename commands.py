import time
from dataclasses import dataclass
from typing import Optional, Tuple

from enemy import Enemy
from player import Player
from game_state import ITEMS, LOCATIONS, SHOP_STOCK, normalize_location
from encounter import attack_turn, run_attempt, spawn_enemy_for
from exploration import search_location


@dataclass
class CommandResult:
    enemy: Optional[Enemy]
    game_over: bool
    should_quit: bool


def parse_command(line: str) -> Tuple[str, str]:
    line = line.strip()
    if not line:
        return "", ""
    parts = line.split()
    cmd = parts[0].lower()
    rest = " ".join(parts[1:]).strip()
    return cmd, rest


def maybe_start_encounter(player: Player, enemy: Optional[Enemy]) -> Optional[Enemy]:
    if enemy and enemy.is_alive():
        return enemy

    spawned = spawn_enemy_for(player.location)
    if spawned:
        player.add_log(f"Encounter! A {spawned.name} appears!")
        return spawned

    return None


def handle_command(
    player: Player,
    enemy: Optional[Enemy],
    game_over: bool,
    line: str,
) -> CommandResult:

    # GAME OVER MODE
    if game_over:
        cmd, _ = parse_command(line)
        if cmd == "quit":
            return CommandResult(enemy, True, True)
        return CommandResult(enemy, True, False)

    cmd, rest = parse_command(line)
    if not cmd:
        return CommandResult(enemy, game_over, False)

    # SYSTEM
    if cmd == "quit":
        player.add_log("You left the game.")
        return CommandResult(enemy, game_over, True)

    if cmd == "where":
        player.add_log(f"Location: {player.location}")
        return CommandResult(enemy, game_over, False)

    # MOVEMENT
    if cmd == "goto":
        if not rest:
            player.add_log("Usage: goto <location>")
            return CommandResult(enemy, game_over, False)

        target = normalize_location(rest)
        if target not in LOCATIONS:
            player.add_log(f"Unknown location: {rest}")
            return CommandResult(enemy, game_over, False)

        prev = player.location
        player.location = target
        player.add_log(f"Traveled: {prev} -> {target}")

        enemy = maybe_start_encounter(player, None)
        return CommandResult(enemy, game_over, False)

    if cmd == "move":
        if not rest:
            player.add_log("Usage: move <exit>")
            return CommandResult(enemy, game_over, False)

        loc = LOCATIONS.get(player.location)
        if not loc:
            player.add_log("Invalid location.")
            return CommandResult(enemy, game_over, False)

        exits = loc.get("exits", {})
        if rest not in exits:
            player.add_log(f"No exit '{rest}'.")
            return CommandResult(enemy, game_over, False)

        prev = player.location
        player.location = exits[rest]
        player.add_log(f"Moved: {prev} -> {player.location}")

        enemy = maybe_start_encounter(player, None)
        return CommandResult(enemy, game_over, False)

    # EXPLORATION
    if cmd == "search":
        enemy = search_location(player, enemy)
        return CommandResult(enemy, game_over, False)

    # SHOP
    if cmd == "buy":
        if player.location != "shop":
            player.add_log("You must be in the shop.")
            return CommandResult(enemy, game_over, False)

        parts = rest.split()
        if not parts:
            player.add_log("Usage: buy <number|key> [amount]")
            return CommandResult(enemy, game_over, False)

        raw = parts[0]
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1

        if raw.isdigit():
            idx = int(raw) - 1
            if idx < 0 or idx >= len(SHOP_STOCK):
                player.add_log("Invalid shop item number.")
                return CommandResult(enemy, game_over, False)
            item_key = SHOP_STOCK[idx]
        else:
            item_key = raw

        if item_key not in ITEMS:
            player.add_log("Unknown item.")
            return CommandResult(enemy, game_over, False)

        item = ITEMS[item_key]
        price = item.price * amount

        if not player.spend_gold(price):
            return CommandResult(enemy, game_over, False)

        player.add_item(item_key, amount)
        player.add_log(f"Bought: {item.name} x{amount}.")
        return CommandResult(enemy, game_over, False)

    # ITEMS
    if cmd == "use":
        item_key = rest
        if item_key not in ITEMS:
            player.add_log("Unknown item.")
            return CommandResult(enemy, game_over, False)

        if player.inventory.get(item_key, 0) <= 0:
            player.add_log("You don't have that item.")
            return CommandResult(enemy, game_over, False)

        item = ITEMS[item_key]
        if item.item_type != "consumable":
            player.add_log("You can only use consumables.")
            return CommandResult(enemy, game_over, False)

        player.remove_item(item_key, 1)
        healed = min(item.heal, player.max_hp - player.hp)
        player.hp += healed
        player.add_log(f"Used {item.name} (+{healed} HP).")
        return CommandResult(enemy, game_over, False)

    # COMBAT
    if cmd == "attack":
        if enemy and enemy.is_alive():
            enemy = attack_turn(player, enemy)
            if player.hp <= 0:
                return CommandResult(enemy, True, False)
        else:
            player.add_log("No enemy to attack.")
        return CommandResult(enemy, game_over, False)

    if cmd == "run":
        if enemy and enemy.is_alive():
            enemy = run_attempt(player, enemy)
            if player.hp <= 0:
                return CommandResult(enemy, True, False)
        else:
            player.add_log("No enemy to run from.")
        return CommandResult(enemy, game_over, False)

    player.add_log(f"Unknown command: {line}")
    time.sleep(0.05)
    return CommandResult(enemy, game_over, False)
