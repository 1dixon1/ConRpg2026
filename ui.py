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
    order = ["weapon", "helmet", "chest", "gloves", "boots", "accessory1", "accessory2"]
    lines: list[str] = []

    for slot in order:
        key = player.equipped.get(slot)
        if key and key in ITEMS:
            it = ITEMS[key]
            stats = []
            if it.atk != 0:
                stats.append(f"ATK {it.atk:+d}")
            if it.defense != 0:
                stats.append(f"DEF {it.defense:+d}")
            if it.hp != 0:
                stats.append(f"HP {it.hp:+d}")
            if it.crit_chance != 0.0:
                stats.append(f"CRIT +{int(it.crit_chance * 100)}%")
            if it.crit_mult != 0.0:
                stats.append(f"CMULT +{it.crit_mult:.2f}")

            stats_text = (" | " + " ".join(stats)) if stats else ""
            lines.append(f"{slot:<10}: {it.name} [{key}]{stats_text}")
        else:
            lines.append(f"{slot:<10}: (none)")

    return lines

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
    stats = player.get_total_stats(ITEMS)

    atk = int(stats["atk"])
    defense = int(stats["def"])
    hit = int(stats["hit_chance"] * 100)
    evade = int(stats["evade_chance"] * 100)
    crit = int(stats["crit_chance"] * 100)
    cmult = float(stats["crit_mult"])

    s = int(stats["str"])
    d = int(stats["dex"])
    c = int(stats["con"])
    w = int(stats["wis"])
    i = int(stats["int"])
    ch = int(stats["cha"])

    lines: list[str] = []
    lines.append("[STATUS]")
    lines.append(hr())
    lines.append(
        f"HP: {player.hp:>2}/{player.max_hp:<2}  Gold: {player.gold:<4}  "
        f"ATK: {atk:<3} DEF: {defense:<3} HIT: {hit:>2}% EVA: {evade:>2}% CRIT: {crit:>2}% x{cmult:.2f}"
    )
    lines.append(
        f"LVL: {player.level:<2} XP: {player.xp:>3}/{player.xp_to_next_level():<3} SP: {player.skill_points:<2}  "
        f"STR {s:<2} DEX {d:<2} CON {c:<2} WIS {w:<2} INT {i:<2} CHA {ch:<2}"
    )
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
    lines.append("Commands: buy <number|key> [amount] | sell <item_key> [amount] | back")
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
    lines.append("Skills: " + ", ".join(player.skills))
    lines.append("Use: skill <name>   |   skills (show cooldowns)")
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

def render_stats_page(player: Player) -> list[str]:
    stats = player.get_total_stats(ITEMS)
    attrs_total = player.get_total_attributes(ITEMS)

    base = {
        "str": player.strength,
        "dex": player.dexterity,
        "con": player.constitution,
        "wis": player.wisdom,
        "int": player.intelligence,
        "cha": player.charisma,
    }

    bonus = {k: int(attrs_total[k]) - int(base[k]) for k in base.keys()}

    def fmt_attr(label: str, key: str) -> str:
        b = base[key]
        t = int(attrs_total[key])
        d = bonus[key]
        sign = "+" if d >= 0 else ""
        return f"{label:<4}: {b:>2} -> {t:>2}   ({sign}{d})"

    atk = int(stats["atk"])
    defense = int(stats["def"])
    hit = int(float(stats["hit_chance"]) * 100)
    evade = int(float(stats["evade_chance"]) * 100)
    crit = int(float(stats["crit_chance"]) * 100)
    cmult = float(stats["crit_mult"])

    lines: list[str] = []
    lines.append("[STATS]")
    lines.append(hr())
    lines.append("Attributes (base -> total, bonus from gear):")
    lines.append(f"  {fmt_attr('STR', 'str')}     {fmt_attr('DEX', 'dex')}")
    lines.append(f"  {fmt_attr('CON', 'con')}     {fmt_attr('WIS', 'wis')}")
    lines.append(f"  {fmt_attr('INT', 'int')}     {fmt_attr('CHA', 'cha')}")
    lines.append("")
    lines.append("Derived combat:")
    lines.append(f"  ATK  : {atk}")
    lines.append(f"  DEF  : {defense}")
    lines.append(f"  HIT  : {hit}%")
    lines.append(f"  EVADE: {evade}%")
    lines.append(f"  CRIT : {crit}%  x{cmult:.2f}")
    lines.append("")
    lines.append("Explanation:")
    lines.append("  STR (Strength)      - increases damage and critical multiplier.")
    lines.append("  DEX (Dexterity)     - increases hit chance, critical chance, and dodge chance.")
    lines.append("  CON (Constitution)  - increases max HP and defense.")
    lines.append("  WIS (Wisdom)        - slightly increases defense, hit chance, and dodge chance.")
    lines.append("  INT (Intelligence)  - reserved for magic/skills scaling later (spells, mana, etc).")
    lines.append("  CHA (Charisma)      - slightly increases crit chance (and later: prices/dialogue).")
    lines.append("")
    lines.append("Commands: back | inv | home")
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
    elif screen == "stats":
        out.extend(render_stats_page(player))

    else:
        out.extend(render_home(player, enemy))

    out.append("[LOG]")
    out.append(hr())
    out.extend(clamp_lines([f"- {x}" for x in player.log], 8))
    out.append("")

    out.append("[QUICK COMMANDS]")
    out.append(hr())
    out.append("Pages : home | inv | shop | stats | help | quit")
    out.append("Explore: goto <loc> | move <exit> | search")
    out.append("Combat : attack | run")
    out.append(hr())

    return "\n".join(out)


def draw(player: Player, enemy: Optional[Enemy], game_over: bool, screen: str) -> None:
    clear_screen()
    sys.stdout.write(render_frame(player, enemy, game_over, screen))
    sys.stdout.flush()
