import os
import sys
from typing import Optional

from enemy import Enemy
from player import Player
from game_state import ITEMS, LOCATIONS, SHOP_STOCK
from exploration import get_objects_for


WIDTH = 72


def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def hr(char: str = "-") -> str:
    return char * WIDTH


def box_title(title: str) -> str:
    title = f" {title} "
    if len(title) >= WIDTH:
        return title[:WIDTH]
    pad_total = WIDTH - len(title)
    left = pad_total // 2
    right = pad_total - left
    return ("=" * left) + title + ("=" * right)


def clamp_lines(lines: list[str], max_lines: int) -> list[str]:
    if len(lines) <= max_lines:
        return lines
    return lines[-max_lines:]


def format_equipment(player: Player) -> list[str]:
    weapon_key = player.equipped_weapon
    armor_key = player.equipped_armor

    if weapon_key and weapon_key in ITEMS:
        w = ITEMS[weapon_key]
        weapon_line = f"Weapon: {w.name}  (ATK {w.atk:+d}, DEF {w.defense:+d})  [{weapon_key}]"
    else:
        weapon_line = "Weapon: (none)"

    if armor_key and armor_key in ITEMS:
        a = ITEMS[armor_key]
        armor_line = f"Armor : {a.name}  (ATK {a.atk:+d}, DEF {a.defense:+d})  [{armor_key}]"
    else:
        armor_line = "Armor : (none)"

    return [weapon_line, armor_line]


def format_inventory(player: Player) -> list[str]:
    if not player.inventory:
        return ["(empty)"]

    lines: list[str] = []
    for key, qty in sorted(player.inventory.items()):
        item = ITEMS.get(key)
        if not item:
            lines.append(f"{key} x{qty}")
            continue

        tag = item.item_type.upper()
        stats = ""
        if item.item_type in ("weapon", "armor"):
            stats = f" | ATK {item.atk:+d} DEF {item.defense:+d}"
        if item.item_type == "consumable":
            stats = f" | HEAL {item.heal}"
        lines.append(f"{item.name} x{qty} [{key}] ({tag}){stats}")

    return lines


def format_shop() -> list[str]:
    lines: list[str] = []
    for idx, key in enumerate(SHOP_STOCK, start=1):
        item = ITEMS[key]
        tag = item.item_type.upper()
        stats = ""
        if item.item_type in ("weapon", "armor"):
            stats = f" | ATK {item.atk:+d} DEF {item.defense:+d}"
        if item.item_type == "consumable":
            stats = f" | HEAL {item.heal}"
        lines.append(f"{idx:>2}. {item.name:<20} {item.price:>3}g  [{key}] ({tag}){stats}")
    return lines


def render_frame(player: Player, enemy: Optional[Enemy], game_over: bool) -> str:
    loc = LOCATIONS.get(player.location, {"title": "Unknown", "desc": "", "exits": {}})

    atk = player.get_atk(ITEMS)
    defense = player.get_def(ITEMS)

    exits = list(loc.get("exits", {}).keys())
    exits_line = ", ".join(exits) if exits else "none"

    objects = get_objects_for(player.location)
    objects_line = ", ".join(objects) if objects else "none"

    log_lines = clamp_lines([f"- {x}" for x in player.log], 7)

    out: list[str] = []
    out.append(box_title("CONSOLE RPG"))
    out.append("")

    if game_over:
        out.append(box_title("GAME OVER"))
        out.append("")

    out.append("[STATUS]")
    out.append(hr())
    out.append(
        f"Name: {player.name:<12}  HP: {player.hp:>2}/{player.max_hp:<2}  "
        f"ATK: {atk:<2}  DEF: {defense:<2}  Gold: {player.gold:<4}"
    )
    out.append(f"Level: {player.level:<3}  XP: {player.xp:>3}/{player.xp_to_next_level():<3}  Skill Points: {player.skill_points}")
    out.append("")

    out.append("[LOCATION]")
    out.append(hr())
    out.append(f"{loc['title']}  ({player.location})")
    out.append(loc.get("desc", ""))
    out.append(f"Exits  : {exits_line}")
    out.append(f"Objects: {objects_line}")
    out.append("")

    if enemy and enemy.is_alive():
        out.append("[ENCOUNTER]")
        out.append(hr())
        out.append(f"{enemy.name}  HP: {enemy.hp}/{enemy.max_hp}  ATK: {enemy.atk}  DEF: {enemy.defense}")
        out.append("Actions: attack | run | use <consumable>")
        out.append("")

    out.append("[EQUIPMENT]")
    out.append(hr())
    for line in format_equipment(player):
        out.append(line)
    out.append("")

    out.append("[INVENTORY]")
    out.append(hr())
    inv_lines = format_inventory(player)
    for line in clamp_lines(inv_lines, 8):
        out.append(line)
    if len(inv_lines) > 8:
        out.append(f"... (+{len(inv_lines) - 8} more)")
    out.append("")

    if player.location == "shop":
        out.append("[SHOP]")
        out.append(hr())
        for line in format_shop():
            out.append(line)
        out.append("Buy: buy <number|key> [amount]")
        out.append("")

    out.append("[LOG]")
    out.append(hr())
    out.extend(log_lines)
    out.append("")

    out.append("[COMMANDS]")
    out.append(hr())
    if game_over:
        out.append("System:  quit")
    else:
        out.append("Travel : goto <location> | move <exit> | where")
        out.append("Explore: search  (may find loot or trigger an encounter)")
        out.append("Items  : buy <n|key> [amt] (shop) | use <key> | equip <key> | unequip <weapon|armor>")
        out.append("Combat : attack | run  (only when an enemy is present)")
        out.append("Debug  : testxp <amt> | gold <amt>")
        out.append("System : quit")
    out.append(hr())

    return "\n".join(out)


def draw(player: Player, enemy: Optional[Enemy], game_over: bool) -> None:
    clear_screen()
    sys.stdout.write(render_frame(player, enemy, game_over))
    sys.stdout.flush()
