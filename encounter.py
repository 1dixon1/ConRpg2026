import random
from typing import Optional

from enemy import Enemy
from player import Player
from game_state import DROPS, ENEMIES, ENEMIES_BY_LOCATION, ITEMS


def calc_damage(atk: int, defense: int) -> int:
    return max(1, atk - defense)


def spawn_enemy_for(location: str) -> Optional[Enemy]:
    pool = ENEMIES_BY_LOCATION.get(location)
    if not pool:
        return None

    # Encounter chances per location
    if location == "forest":
        if random.random() > 0.45:
            return None

    if location == "dark_forest":
        if random.random() > 0.70:
            return None

    key = random.choice(pool)
    t = ENEMIES[key]
    return Enemy(
        key=key,
        name=t["name"],
        max_hp=t["hp"],
        hp=t["hp"],
        atk=t["atk"],
        defense=t["def"],
        xp_reward=t["xp"],
        gold_reward=t["gold"],
    )


def try_drop(player: Player) -> None:
    for item_key, chance in DROPS:
        if random.random() < chance:
            player.add_item(item_key, 1)
            player.add_log(f"Drop: {ITEMS[item_key].name}.")


def attack_turn(player: Player, enemy: Enemy) -> Optional[Enemy]:
    if not enemy.is_alive():
        player.add_log("No enemy to attack.")
        return None

    player_atk = player.get_atk(ITEMS)
    player_def = player.get_def(ITEMS)

    # Player hits
    dmg_to_enemy = calc_damage(player_atk, enemy.defense)
    enemy.hp = max(0, enemy.hp - dmg_to_enemy)
    player.add_log(f"You hit {enemy.name} for {dmg_to_enemy} damage.")

    if not enemy.is_alive():
        player.add_log(f"You defeated {enemy.name}!")
        player.add_xp(enemy.xp_reward)
        player.add_gold(enemy.gold_reward)
        try_drop(player)
        return None

    # Enemy hits back
    dmg_to_player = calc_damage(enemy.atk, player_def)
    player.hp = max(0, player.hp - dmg_to_player)
    player.add_log(f"{enemy.name} hits you for {dmg_to_player} damage.")

    if player.hp <= 0:
        player.add_log("You died. GAME OVER.")
        return enemy

    return enemy


def run_attempt(player: Player, enemy: Enemy) -> Optional[Enemy]:
    if not enemy.is_alive():
        player.add_log("No enemy to run from.")
        return None

    # Slight bonus in dark forest if you have a torch
    bonus = 0.10 if (player.location == "dark_forest" and player.inventory.get("torch", 0) > 0) else 0.0
    chance = 0.45 + bonus

    if random.random() < chance:
        player.add_log(f"You escaped from {enemy.name}.")
        return None

    player.add_log("Escape failed!")

    # Free hit
    dmg = calc_damage(enemy.atk, player.get_def(ITEMS))
    player.hp = max(0, player.hp - dmg)
    player.add_log(f"{enemy.name} hits you for {dmg} damage while you run.")

    if player.hp <= 0:
        player.add_log("You died. GAME OVER.")
        return enemy

    return enemy
