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


def render_status(player: Player) -> list[str]:
    atk = player.get_atk(ITEMS)
    defense = player.get_def(ITEMS)

    lines: list[str] = []
    lines.append("[STATUS]")
    lines.append(hr())
    lines.append(
        f"Name: {player.name:<12}  HP: {player.hp:>2}/{player.max_hp:<2}  "
        f"ATK: {atk:<2}  DEF: {defense:<2}  Gold: {player.gold:<4}"
    )
    lines.append(f"Level: {player.level:<3}  XP: {player.xp:>3}/{player.xp_to_next_level():<3}  Skill Points: {player.skill_points}")
    lines.append("")
    return lines


def render_home(player: Player, enemy: Optional[Enemy]) -> list[str]:
    loc = LOCATIONS.get(player.location, {"title": "Unknown", "desc": "", "exits": {}})

    exits = list(loc.get("exits", {}).keys())
    exits_line = ", ".join(exits) if exits else "none"

    objects = get_objects_for(player.location)
    objects_line = ", ".join(objects) if objects else "none"

    lines: list[str] = []
    lines.append("[EXPLORE]")
    lines.append(hr())
    lines.append(f"{loc['title']}  ({player.location})")
    lines.append(loc.get("desc", ""))
    lines.append(f"Exits  : {exits_line}")
    lines.append(f"Objects: {objects_line}")
    lines.append("")
    lines.append("Tip: use 'search' to explore this area.")
    lines.append("")
    return lines


def render_inventory_page(player: Player) -> list[str]:
    lines: list[str] = []
    lines.append("[INVENTORY]")
    lines.append(hr())
    lines.append("Equipment:")
    for x in format_equipment(player):
        lines.append(f"  {x}")
    lines.append("")
    lines.append("Items:")
    for x in clamp_lines(format_inventory(player), 16):
        lines.append(f"  {x}")
    lines.append("")
    lines.append("Commands: use <key> | equip <key> | unequip <weapon|armor> | back")
    lines.append("")
    return lines


def render_shop_page(player: Player) -> list[str]:
    lines: list[str] = []
    lines.append("[SHOP]")
    lines.append(hr())
    if player.location != "shop":
        lines.append("You are not in the shop.")
        lines.append("Go there first: goto shop")
        lines.append("")
        return lines

    for x in format_shop():
        lines.append(x)
    lines.append("")
    lines.append("Commands: buy <number|key> [amount] | back")
    lines.append("")
    return lines


def render_combat_page(player: Player, enemy: Optional[Enemy]) -> list[str]:
    lines: list[str] = []
    lines.append("[COMBAT]")
    lines.append(hr())

    if not enemy or not enemy.is_alive():
        lines.append("No enemy is present.")
        lines.append("Type: back")
        lines.append("")
        return lines

    lines.append(f"Enemy: {enemy.name}")
    lines.append(f"HP   : {enemy.hp}/{enemy.max_hp}")
    lines.append(f"ATK  : {enemy.atk}   DEF: {enemy.defense}")
    lines.append("")
    lines.append("Commands: attack | run | use <consumable>")
    lines.append("")
    return lines


def render_help_page() -> list[str]:
    lines: list[str] = []
    lines.append("[HELP]")
    lines.append(hr())
    lines.append("Pages:")
    lines.append("  home / back   - explore page")
    lines.append("  inv           - inventory page")
    lines.append("  shop          - shop page (only if you are in shop)")
    lines.append("  help          - this page")
    lines.append("")
    lines.append("Explore:")
    lines.append("  goto <location> | move <exit> | search")
    lines.append("")
    lines.append("Items:")
    lines.append("  buy <n|key> [amt] | use <key> | equip <key> | unequip <weapon|armor>")
    lines.append("")
    lines.append("Combat:")
    lines.append("  attack | run")
    lines.append("")
    lines.append("System:")
    lines.append("  quit")
    lines.append("")
    return lines


def render_frame(player: Player, enemy: Optional[Enemy], game_over: bool, screen: str) -> str:
    out: list[str] = []
    out.append(box_title("CONSOLE RPG"))
    out.append("")

    if game_over:
        out.append(box_title("GAME OVER"))
        out.append("")
        out.extend(render_status(player))
        out.append("[LOG]")
        out.append(hr())
        out.extend(clamp_lines([f"- {x}" for x in player.log], 10))
        out.append("")
        out.append("[COMMANDS]")
        out.append(hr())
        out.append("System: quit")
        out.append(hr())
        return "\n".join(out)

    out.extend(render_status(player))

    screen = (screen or "home").lower()

    if screen == "inventory":
        out.extend(render_inventory_page(player))
    elif screen == "shop":
        out.extend(render_shop_page(player))
    elif screen == "combat":
        out.extend(render_combat_page(player, enemy))
    elif screen == "help":
        out.extend(render_help_page())
    else:
        out.extend(render_home(player, enemy))

    out.append("[LOG]")
    out.append(hr())
    out.extend(clamp_lines([f"- {x}" for x in player.log], 8))
    out.append("")

    out.append("[QUICK COMMANDS]")
    out.append(hr())
    out.append("Pages : home | inv | shop | help | quit")
    out.append("Explore: goto <loc> | move <exit> | search")
    out.append("Combat : attack | run")
    out.append(hr())

    return "\n".join(out)


def draw(player: Player, enemy: Optional[Enemy], game_over: bool, screen: str) -> None:
    clear_screen()
    sys.stdout.write(render_frame(player, enemy, game_over, screen))
    sys.stdout.flush()
