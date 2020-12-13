import sc2
from sc2.player import Bot, Computer

from planbot import PlanBot

sc2.run_game(
    sc2.maps.get("CatalystLE_NOAI"),
    [
        Bot(sc2.Race.Terran, PlanBot()),
        Computer(sc2.Race.Terran,
        sc2.Difficulty.Hard)
    ],
    realtime=True,
)
