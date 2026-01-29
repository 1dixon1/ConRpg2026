import random
from typing import Optional

from domain.enemy import Enemy
from domain.player import Player
from encounter import spawn_enemy_for
from game_state import ITEMS, OBJECTS_BY_LOCATION, SEARCH_ENCOUNTER_CHANCE, SEARCH_LOOT_TABLE


def get_objects_for(location: str) -> list[str]:
    return OBJECTS_BY_LOCATION.get(location, [])


def search_location(player: Player, enemy: Optional[Enemy]) -> Optional[Enemy]:
    # If combat is active, block searching
    if enemy and enemy.is_alive():
        player.add_log("You cannot search while an enemy is present.")
        return enemy

    objects = get_objects_for(player.location)
    if objects:
        obj = random.choice(objects)
        player.add_log(f"You search the {obj}...")
    else:
        player.add_log("There is nothing interesting to search here.")

    # First: chance to trigger an encounter
    enc_chance = SEARCH_ENCOUNTER_CHANCE.get(player.location, 0.0)
    if enc_chance > 0.0 and random.random() < enc_chance:
        spawned = spawn_enemy_for(player.location)
        if spawned:
            player.add_log(f"You disturbed something... Encounter! A {spawned.name} appears!")
            return spawned

    # Second: loot roll
    # 75% chance to find nothing
    if random.random() < 0.75:
        player.add_log("You found nothing.")
        return None

    table = SEARCH_LOOT_TABLE.get(player.location, [])
    if not table:
        player.add_log("You found nothing.")
        return None

    # Weighted pick (so if we passed the 25% gate, we almost always get something)
    total = sum(max(0.0, row[4]) for row in table)
    if total <= 0.0:
        player.add_log("You found nothing.")
        return None

    roll = random.random() * total
    cursor = 0.0

    for kind, key, min_amt, max_amt, chance in table:
        w = max(0.0, chance)
        cursor += w
        if roll <= cursor:
            amount = random.randint(min_amt, max_amt)

            if kind == "gold":
                player.add_gold(amount)
                player.add_log(f"You found {amount} gold.")
                return None

            if kind == "item":
                if key in ITEMS:
                    player.add_item(key, amount)
                    player.q_loot[key] = player.q_loot.get(key, 0) + amount
                    name = ITEMS[key].name
                    if amount == 1:
                        player.add_log(f"You found: {name}.")
                    else:
                        player.add_log(f"You found: {name} x{amount}.")
                    return None

                player.add_log("You found something strange, but it crumbled to dust.")
                return None

    # Nothing found
    player.add_log("You found nothing.")
    return None
