from quests import Quest

QUESTS = {
    "mq_001": Quest(
        qid="mq_001",
        title="First Steps",
        desc="Reach the crossroads.",
        category="main",
        objectives=["Go to Crossroads"],
        requirements=[("visit", "crossroads", 1)],
        reward_gold=20,
        reward_xp=40,
    ),
}
