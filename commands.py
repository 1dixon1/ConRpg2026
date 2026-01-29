import time
from dataclasses import dataclass
from typing import Optional, Tuple

from enemy import Enemy
from player import Player
from game_state import ITEMS, LOCATIONS, SHOP_STOCK, normalize_location
from encounter import attack_turn, run_attempt, spawn_enemy_for
from exploration import search_location


BOOK_TO_SKILL = {
    "book_power_strike": "power_strike",
    "book_guard": "guard",
    "book_focus": "focus",
    "book_bleed_strike": "bleed_strike",
    "book_poison_dart": "poison_dart",
    "book_stunning_blow": "stunning_blow",
    "book_quick_step": "quick_step",
    "book_sunder_armor": "sunder_armor",
    "book_battle_cry": "battle_cry",
    "book_first_aid": "first_aid",
    "book_vampiric_hit": "vampiric_hit",
    "book_execute": "execute",
}

@dataclass
class CommandResult:
    enemy: Optional[Enemy]
    game_over: bool
    should_quit: bool
    screen: str


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

def requires_map(location_key: str) -> bool:
        # Free locations (always accessible)
        return location_key not in ("tavern", "shop", "forest", "dark_forest")

def has_map(player: Player, location_key: str) -> bool:
    map_key = f"map_{location_key}"
    return player.inventory.get(map_key, 0) > 0

def get_sell_price(item_key: str) -> int:
    item = ITEMS.get(item_key)
    if not item:
        return 0

    if getattr(item, "sell_price", 0) and item.sell_price > 0:
        return item.sell_price

    # Fallback: if item has shop price, sell for 50%
    if getattr(item, "price", 0) and item.price > 0:
        return max(1, item.price // 2)

    return 0




def handle_command(
    player: Player,
    enemy: Optional[Enemy],
    game_over: bool,
    screen: str,
    line: str,
) -> CommandResult:

    if game_over:
        cmd, _ = parse_command(line)
        if cmd == "quit":
            return CommandResult(enemy=enemy, game_over=True, should_quit=True, screen=screen)
        return CommandResult(enemy=enemy, game_over=True, should_quit=False, screen=screen)

    cmd, rest = parse_command(line)
    if not cmd:
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

    # Pages
    if cmd in ("home", "back"):
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="home")

    if cmd in ("inv", "inventory"):
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="inventory")

    if cmd == "shop":
        if player.location != "shop":
            player.add_log("You are not in the shop. Use: goto shop")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

    if cmd == "help":
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="help")

    # System
    if cmd == "quit":
        player.add_log("You left the game.")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=True, screen=screen)

    if cmd == "where":
        player.add_log(f"Location: {player.location}")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

    # Movement
    if cmd == "goto":
        if not rest:
            player.add_log("Usage: goto <location>")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        target = normalize_location(rest)
        if target not in LOCATIONS:
            player.add_log(f"Unknown location: {rest}")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)
        
        if requires_map(target) and not has_map(player, target):
            player.add_log(f"You need a map to enter: {target}. (Buy: map_{target})")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        prev = player.location
        player.location = target
        player.add_log(f"Traveled: {prev} -> {target}")
        enemy = maybe_start_encounter(player, None)

        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="home")

    if cmd == "move":
        if not rest:
            player.add_log("Usage: move <exit>")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        loc = LOCATIONS.get(player.location)
        if not loc:
            player.add_log("Invalid location.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        exits = loc.get("exits", {})
        if rest not in exits:
            player.add_log(f"No exit '{rest}'.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        prev = player.location
        next_loc = exits[rest]

        if requires_map(next_loc) and not has_map(player, next_loc):
            player.add_log(f"You need a map to enter: {next_loc}. (Buy: map_{next_loc})")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        player.location = next_loc
        player.add_log(f"Moved: {prev} -> {player.location}")
        
        enemy = maybe_start_encounter(player, None)

        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="home")

    # Exploration
    if cmd == "search":
        enemy = search_location(player, enemy)
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="home")

    # Shop
    if cmd == "buy":
        if player.location != "shop":
            player.add_log("You must be in the shop.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        parts = rest.split()
        if not parts:
            player.add_log("Usage: buy <number|key> [amount]")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

        raw = parts[0]
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1

        if raw.isdigit():
            idx = int(raw) - 1
            if idx < 0 or idx >= len(SHOP_STOCK):
                player.add_log("Invalid shop item number.")
                return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")
            item_key = SHOP_STOCK[idx]
        else:
            item_key = raw

        if item_key not in ITEMS:
            player.add_log("Unknown item.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

        item = ITEMS[item_key]
        price = item.price * amount
        if not player.spend_gold(price):
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

        player.add_item(item_key, amount)
        player.add_log(f"Bought: {item.name} x{amount}.")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

    if cmd == "sell":
        if player.location != "shop":
            player.add_log("You must be in the shop to sell items.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        parts = rest.split()
        if not parts:
            player.add_log("Usage: sell <item_key> [amount]")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

        item_key = parts[0].strip().lower()
        amount = 1
        if len(parts) >= 2 and parts[1].isdigit():
            amount = int(parts[1])

        if amount <= 0:
            amount = 1

        if item_key not in ITEMS:
            player.add_log("Unknown item.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

        have = player.inventory.get(item_key, 0)
        if have <= 0:
            player.add_log("You don't have that item.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

        if amount > have:
            amount = have

        unit_price = get_sell_price(item_key)
        if unit_price <= 0:
            player.add_log("This item cannot be sold.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

        player.remove_item(item_key, amount)
        gold = unit_price * amount
        player.gold += gold
        player.add_log(f"Sold {ITEMS[item_key].name} x{amount} for {gold} gold.")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="shop")

    # Items
    if cmd == "use":
        item_key = rest
        if item_key not in ITEMS:
            player.add_log("Unknown item.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        if player.inventory.get(item_key, 0) <= 0:
            player.add_log("You don't have that item.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        item = ITEMS[item_key]
        if item.item_type != "consumable":
            player.add_log("You can only use consumables.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        player.remove_item(item_key, 1)
        healed = min(item.heal, player.max_hp - player.hp)
        player.hp += healed
        player.add_log(f"Used {item.name} (+{healed} HP).")

        new_screen = "combat" if (enemy and enemy.is_alive()) else screen
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=new_screen)

    if cmd == "equip":
            item_key = rest.strip().lower()
            item = ITEMS.get(item_key)

            if not item:
                player.add_log("Unknown item.")
                return CommandResult(enemy, game_over, False, "inventory")

            if player.inventory.get(item_key, 0) <= 0:
                player.add_log("You don't have that item.")
                return CommandResult(enemy, game_over, False, "inventory")

            if item.item_type != "equip":
                player.add_log("This item cannot be equipped.")
                return CommandResult(enemy, game_over, False, "inventory")

            # Accessories (2 slots)
            if item.slot == "accessory":
                if player.equipped["accessory1"] == item_key or player.equipped["accessory2"] == item_key:
                    player.add_log("That accessory is already equipped.")
                    return CommandResult(enemy, game_over, False, "inventory")

                if not player.equipped["accessory1"]:
                    player.equipped["accessory1"] = item_key
                    player.add_log(f"Equipped accessory (slot 1): {item.name}.")
                elif not player.equipped["accessory2"]:
                    player.equipped["accessory2"] = item_key
                    player.add_log(f"Equipped accessory (slot 2): {item.name}.")
                else:
                    player.add_log("Both accessory slots are full.")
                    return CommandResult(enemy, game_over, False, "inventory")

                player.apply_hp_bonus(ITEMS)
                return CommandResult(enemy, game_over, False, "inventory")

            # Normal slots
            if item.slot not in player.equipped:
                player.add_log("Invalid equipment slot.")
                return CommandResult(enemy, game_over, False, "inventory")

            player.equipped[item.slot] = item_key
            player.add_log(f"Equipped {item.slot}: {item.name}.")
            player.apply_hp_bonus(ITEMS)
            return CommandResult(enemy, game_over, False, "inventory")


        # UNEQUIP
        
    if cmd == "unequip":
        slot = rest.strip().lower()

        if slot not in player.equipped:
            player.add_log("Usage: unequip <weapon|helmet|chest|gloves|boots|accessory1|accessory2>")
            return CommandResult(enemy, game_over, False, "inventory")

        if not player.equipped[slot]:
            player.add_log("That slot is already empty.")
            return CommandResult(enemy, game_over, False, "inventory")

        name = ITEMS[player.equipped[slot]].name
        player.equipped[slot] = None
        player.add_log(f"Unequipped {slot}: {name}.")
        player.apply_hp_bonus(ITEMS)
        return CommandResult(enemy, game_over, False, "inventory")
    # Combat
    if cmd == "attack":
        if enemy and enemy.is_alive():
            enemy = attack_turn(player, enemy)
            if player.hp <= 0:
                return CommandResult(enemy=enemy, game_over=True, should_quit=False, screen="combat")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="combat")

        player.add_log("No enemy to attack.")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

    if cmd == "run":
        if enemy and enemy.is_alive():
            enemy = run_attempt(player, enemy)
            if player.hp <= 0:
                return CommandResult(enemy=enemy, game_over=True, should_quit=False, screen="combat")
            # if escaped -> back home
            if not enemy or not enemy.is_alive():
                return CommandResult(enemy=None, game_over=game_over, should_quit=False, screen="home")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="combat")

        player.add_log("No enemy to run from.")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

    if cmd in ("learn", "read"):
        book_key = rest.strip().lower()
        if not book_key:
            player.add_log("Usage: learn <book_key>")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        if book_key not in BOOK_TO_SKILL:
            player.add_log("This is not a skill book.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        if player.inventory.get(book_key, 0) <= 0:
            player.add_log("You don't have that book.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        skill = BOOK_TO_SKILL[book_key]
        if skill in player.skills:
            player.add_log("You already know that skill.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        player.remove_item(book_key, 1)
        player.skills.append(skill)
        player.add_log(f"You learned a new skill: {skill}!")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="stats" if screen != "combat" else "combat")

    if cmd in ("journal", "quests"):
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="journal")

    if cmd == "track":
        qid = rest.strip().lower()
        if not qid:
            player.add_log("Usage: track <quest_id>")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)
        if qid not in player.active_quests:
            player.add_log("That quest is not active.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)
        player.tracked_quest = qid
        player.add_log(f"Tracked quest: {qid}")
        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="journal")

    if cmd == "claim":
        from quests import ALL_QUESTS
        qid = rest.strip().lower()
        if not qid:
            player.add_log("Usage: claim <quest_id>")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        if qid not in player.active_quests:
            player.add_log("That quest is not active.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        q = ALL_QUESTS.get(qid)
        if not q:
            player.add_log("Unknown quest.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)

        # We need access to Game._quest_done; simplest: replicate a small check here
        done = True
        for kind, key, need in q.requirements:
            if kind == "visit" and player.q_visit.get(key, 0) < need:
                done = False
            if kind == "kill" and player.q_kill.get(key, 0) < need:
                done = False
            if kind == "kill_loc" and player.q_kill_loc.get(key, 0) < need:
                done = False
            if kind == "loot" and player.q_loot.get(key, 0) < need:
                done = False

        if not done:
            player.add_log("Quest is not completed yet.")
            return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="journal")

        # Reward
        if q.reward_gold > 0:
            player.gold += q.reward_gold
            player.add_log(f"Quest reward: {q.reward_gold} gold.")
        if q.reward_xp > 0:
            player.add_xp(q.reward_xp)

        for item_key, amount in q.reward_items:
            player.add_item(item_key, amount)
            player.add_log(f"Quest reward: {item_key} x{amount}.")

        player.complete_quest(qid)

        # Auto-add next main quest
        if q.category == "main" and q.next_main_qid:
            player.add_quest(q.next_main_qid)

        return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen="journal")


    player.add_log(f"Unknown command: {line.strip()}")
    time.sleep(0.05)
    return CommandResult(enemy=enemy, game_over=game_over, should_quit=False, screen=screen)
