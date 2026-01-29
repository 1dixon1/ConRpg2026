from __future__ import annotations

from typing import Dict, List, Optional


# Each NPC has:
# - name
# - location (where they can be found)
# - start node
# - dialog nodes: text + choices
#
# Choice can have:
# - next: next node id
# - action: {"type": "...", ...}
#
# Supported actions (minimal):
# - give_quest: adds quest to player.active_quests
# - open_shop: switches screen to "shop"
# - close: ends dialog

NPCS: Dict[str, Dict] = {
    "innkeeper": {
        "name": "Innkeeper",
        "location": "tavern",
        "start": "start",
        "nodes": {
            "start": {
                "text": "Welcome! Need a bed, a rumor, or work?",
                "choices": [
                    {"label": "Any work for me?", "next": "work"},
                    {"label": "Any rumors?", "next": "rumors"},
                    {"label": "Goodbye.", "action": {"type": "close"}},
                ],
            },
            "rumors": {
                "text": "They say the woods hide old maps... and darker things beyond the trees.",
                "choices": [
                    {"label": "Back.", "next": "start"},
                    {"label": "Goodbye.", "action": {"type": "close"}},
                ],
            },
            "work": {
                "text": "If you want to prove yourself, head to the Crossroads.",
                "choices": [
                    {
                        "label": "I will do it. (Get quest)",
                        "action": {"type": "give_quest", "qid": "mq_001"},
                        "next": "after_work",
                    },
                    {"label": "Back.", "next": "start"},
                ],
            },
            "after_work": {
                "text": "Good. Come back when you're done.",
                "choices": [
                    {"label": "Goodbye.", "action": {"type": "close"}},
                ],
            },
        },
    },

    "merchant": {
        "name": "Merchant",
        "location": "shop",
        "start": "start",
        "nodes": {
            "start": {
                "text": "Browse my wares or bring me trophies.",
                "choices": [
                    {"label": "Show me your shop.", "action": {"type": "open_shop"}},
                    {"label": "Trophies? (Quest)", "next": "trophy"},
                    {"label": "Goodbye.", "action": {"type": "close"}},
                ],
            },
            "trophy": {
                "text": "Goblins leave ears behind. Bring me 3 and I pay well.",
                "choices": [
                    {
                        "label": "Deal. (Get quest)",
                        "action": {"type": "give_quest", "qid": "sq_001"},
                        "next": "start",
                    },
                    {"label": "Back.", "next": "start"},
                ],
            },
        },
    },

    "healer": {
        "name": "Healer",
        "location": "village",
        "start": "start",
        "nodes": {
            "start": {
                "text": "You look hurt. I can help, but I also need herbs.",
                "choices": [
                    {"label": "Herbs? (Quest)", "next": "herbs"},
                    {"label": "Goodbye.", "action": {"type": "close"}},
                ],
            },
            "herbs": {
                "text": "Bring me 6 Herbs from the forest. I'll reward you.",
                "choices": [
                    {
                        "label": "I will bring them. (Get quest)",
                        "action": {"type": "give_quest", "qid": "sq_003"},
                        "next": "start",
                    },
                    {"label": "Back.", "next": "start"},
                ],
            },
        },
    },
}


def npcs_in_location(location_key: str) -> List[str]:
    out: List[str] = []
    for npc_id, npc in NPCS.items():
        if npc.get("location") == location_key:
            out.append(npc_id)
    return out


def npc_exists(npc_id: str) -> bool:
    return npc_id in NPCS


def npc_name(npc_id: str) -> str:
    npc = NPCS.get(npc_id)
    return npc.get("name", npc_id) if npc else npc_id


def get_node(npc_id: str, node_id: str) -> Optional[Dict]:
    npc = NPCS.get(npc_id)
    if not npc:
        return None
    return npc.get("nodes", {}).get(node_id)
