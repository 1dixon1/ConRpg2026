import random
from typing import Optional

from enemy import Enemy
from player import Player
from game_state import DROPS, ENEMIES, ENEMIES_BY_LOCATION, ITEMS


SKILLS = {
    "power_strike":   {"name": "Power Strike",   "cooldown": 2},
    "guard":          {"name": "Guard",          "cooldown": 3},
    "focus":          {"name": "Focus",          "cooldown": 3},

    "bleed_strike":   {"name": "Bleed Strike",   "cooldown": 3},
    "poison_dart":    {"name": "Poison Dart",    "cooldown": 3},
    "stunning_blow":  {"name": "Stunning Blow",  "cooldown": 4},

    "quick_step":     {"name": "Quick Step",     "cooldown": 3},
    "sunder_armor":   {"name": "Sunder Armor",   "cooldown": 4},
    "battle_cry":     {"name": "Battle Cry",     "cooldown": 4},

    "first_aid":      {"name": "First Aid",      "cooldown": 5},
    "vampiric_hit":   {"name": "Vampiric Hit",   "cooldown": 5},
    "execute":        {"name": "Execute",        "cooldown": 6},
}


def apply_start_of_turn_effects(player: Player, enemy: Enemy) -> None:
    # Bleed on enemy
    if player.buffs.get("enemy_bleed", 0) > 0:
        dmg = max(1, int(enemy.max_hp * 0.05))
        enemy.hp = max(0, enemy.hp - dmg)
        player.add_log(f"Bleed deals {dmg} damage to {enemy.name}.")

    # Poison on enemy
    if player.buffs.get("enemy_poison", 0) > 0:
        dmg = max(1, int(enemy.max_hp * 0.04))
        enemy.hp = max(0, enemy.hp - dmg)
        player.add_log(f"Poison deals {dmg} damage to {enemy.name}.")


def calc_damage(raw: float, defense: int) -> int:
    dmg = int(raw) - max(0, defense)
    return max(1, dmg)


def spawn_enemy_for(location: str) -> Optional[Enemy]:
    pool = ENEMIES_BY_LOCATION.get(location)
    if not pool:
        return None

    if location == "forest":
        if random.random() > 0.45:
            return None

    if location == "dark_forest":
        if random.random() > 0.70:
            return None
        
    if location == "dark_forest":
        if random.random() < 0.05:
            key = random.choice(["ogre", "necromancer"])
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
    # 25% chance: no loot at all
    if random.random() < 0.25:
        player.add_log("No loot dropped.")
        return

    # 75% chance: drop exactly 1 item (weighted)
    total = sum(max(0.0, chance) for _, chance in DROPS)
    if total <= 0.0:
        player.add_log("No loot dropped.")
        return

    roll = random.random() * total
    cursor = 0.0

    for item_key, chance in DROPS:
        w = max(0.0, chance)
        cursor += w
        if roll <= cursor:
            if item_key in ITEMS:
                player.add_item(item_key, 1)
                player.add_log(f"Drop: {ITEMS[item_key].name}.")
            else:
                player.add_log("Drop: (unknown item).")
            return

    player.add_log("No loot dropped.")

def enemy_evade_chance(enemy: Enemy) -> float:
    # Simple scaling from defense (you can extend later)
    ev = 0.03 + (enemy.defense * 0.02)
    if ev < 0.00:
        ev = 0.00
    if ev > 0.40:
        ev = 0.40
    return ev


def player_hit(player: Player, enemy: Enemy, mult: float = 1.0) -> None:
    stats = player.get_total_stats(ITEMS)

    atk = float(stats["atk"])
    hit_chance = float(stats["hit_chance"])
    crit_chance = float(stats["crit_chance"])
    crit_mult = float(stats["crit_mult"])


    if player.buffs.get("battle_cry", 0) > 0:
        atk *= 1.20

    enemy_def = enemy.defense
    if player.buffs.get("enemy_sunder", 0) > 0:
        enemy_def = max(0, enemy_def - 3)
    
    # Hit roll vs enemy evade
    if random.random() < enemy_evade_chance(enemy):
        player.add_log(f"{enemy.name} dodged your attack!")
        return

    if random.random() > hit_chance:
        player.add_log("You missed!")
        return

    is_crit = random.random() < crit_chance
    dmg_raw = atk * mult
    if is_crit:
        dmg_raw *= crit_mult

    dmg = calc_damage(dmg_raw, enemy_def)
    enemy.hp = max(0, enemy.hp - dmg)

    if is_crit:
        player.add_log(f"CRIT! You hit {enemy.name} for {dmg}.")
    else:
        player.add_log(f"You hit {enemy.name} for {dmg}.")


def enemy_hit(player: Player, enemy: Enemy) -> None:
    
    apply_start_of_turn_effects(player, enemy)
    if enemy.hp <= 0:
        return
    if player.buffs.get("enemy_stunned", 0) > 0:
        player.add_log(f"{enemy.name} is stunned and skips the turn!")
        return
    
    stats = player.get_total_stats(ITEMS)

    player_def = int(stats["def"])
    player_evade = float(stats["evade_chance"])

    # Enemy hit chance can scale a bit with enemy atk
    enemy_hit_chance = 0.70 + (enemy.atk * 0.01)
    if enemy_hit_chance > 0.95:
        enemy_hit_chance = 0.95

    if random.random() < player_evade:
        player.add_log("You dodged the attack!")
        return

    if random.random() > enemy_hit_chance:
        player.add_log(f"{enemy.name} missed!")
        return

    dmg = calc_damage(enemy.atk, player_def)

    if "guard" in player.buffs:
        dmg = max(1, int(dmg * 0.5))
    
    if player.buffs.get("enemy_stunned", 0) > 0:
        player.add_log(f"{enemy.name} is stunned and skips the turn!")
        return
    
    player.hp = max(0, player.hp - dmg)
    player.add_log(f"{enemy.name} hits you for {dmg}.")

    if player.hp <= 0:
        player.add_log("You died. GAME OVER.")
        


def end_turn_tick(player: Player) -> None:
    player.tick_cooldowns_and_buffs()


def check_enemy_defeat(player: Player, enemy: Enemy) -> Optional[Enemy]:
    if enemy.is_alive():
        return enemy

    player.add_log(f"You defeated {enemy.name}!")
    player.add_xp(enemy.xp_reward)
    player.add_gold(enemy.gold_reward)
    try_drop(player)
    return None


def attack_turn(player: Player, enemy: Enemy) -> Optional[Enemy]:
    if not enemy.is_alive():
        player.add_log("No enemy to attack.")
        return None

    player_hit(player, enemy, mult=1.0)
    enemy = check_enemy_defeat(player, enemy)
    if not enemy:
        end_turn_tick(player)
        return None

    enemy_hit(player, enemy)
    end_turn_tick(player)
    return enemy


def skill_turn(player: Player, enemy: Enemy, skill_key: str) -> Optional[Enemy]:
    if not enemy.is_alive():
        player.add_log("No enemy is present.")
        return None

    if skill_key not in SKILLS:
        player.add_log("Unknown skill.")
        return enemy

    if skill_key not in player.skills:
        player.add_log("You haven't learned that skill.")
        return enemy

    if player.cooldowns.get(skill_key, 0) > 0:
        player.add_log(f"Skill is on cooldown: {skill_key} ({player.cooldowns[skill_key]} turns).")
        return enemy

    if skill_key == "power_strike":
        player.add_log("You use Power Strike!")
        player_hit(player, enemy, mult=1.55)
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "guard":
        player.add_log("You use Guard! (50% damage reduction for 1 turn)")
        player.buffs["guard"] = 1
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "focus":
        player.add_log("You use Focus! (+25% crit chance for 1 turn)")
        player.buffs["focus"] = 1
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "bleed_strike":
        player.add_log("You use Bleed Strike! (bleed for 3 turns)")
        player_hit(player, enemy, mult=1.10)
        player.buffs["enemy_bleed"] = 3
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "poison_dart":
        player.add_log("You use Poison Dart! (poison for 3 turns)")
        player_hit(player, enemy, mult=0.95)
        player.buffs["enemy_poison"] = 3
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "stunning_blow":
        player.add_log("You use Stunning Blow!")
        player_hit(player, enemy, mult=1.05)
        # 35% chance to stun for 1 turn
        if random.random() < 0.35:
            player.buffs["enemy_stunned"] = 1
            player.add_log(f"{enemy.name} is stunned!")
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "quick_step":
        player.add_log("You use Quick Step! (+evade for 2 turns)")
        player.buffs["quick_step"] = 2
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "sunder_armor":
        player.add_log("You use Sunder Armor! (enemy -3 DEF for 3 turns)")
        player_hit(player, enemy, mult=1.00)
        player.buffs["enemy_sunder"] = 3
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "battle_cry":
        player.add_log("You use Battle Cry! (+20% ATK for 3 turns)")
        player.buffs["battle_cry"] = 3
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "first_aid":
        player.add_log("You use First Aid!")
        heal = max(4, int(player.max_hp * 0.18))
        player.hp = min(player.max_hp, player.hp + heal)
        player.add_log(f"You recover {heal} HP.")
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "vampiric_hit":
        player.add_log("You use Vampiric Hit!")
        before = enemy.hp
        player_hit(player, enemy, mult=1.20)
        dealt = max(0, before - enemy.hp)
        heal = max(1, int(dealt * 0.40))
        player.hp = min(player.max_hp, player.hp + heal)
        player.add_log(f"You drain {heal} HP.")
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    elif skill_key == "execute":
        player.add_log("You use Execute!")
        # Extra strong if enemy below 35% HP
        ratio = 0.0 if enemy.max_hp <= 0 else (enemy.hp / enemy.max_hp)
        mult = 1.25 if ratio > 0.35 else 2.10
        player_hit(player, enemy, mult=mult)
        player.cooldowns[skill_key] = SKILLS[skill_key]["cooldown"]

    else:
        player.add_log("Unknown skill.")
        return enemy

    
    

    return enemy


def run_attempt(player: Player, enemy: Enemy) -> Optional[Enemy]:
    if not enemy.is_alive():
        player.add_log("No enemy to run from.")
        return None

    bonus = 0.10 if (player.location == "dark_forest" and player.inventory.get("torch", 0) > 0) else 0.0
    chance = 0.45 + bonus

    if random.random() < chance:
        player.add_log(f"You escaped from {enemy.name}.")
        end_turn_tick(player)
        return None

    player.add_log("Escape failed!")
    enemy_hit(player, enemy)
    end_turn_tick(player)
    return enemy
