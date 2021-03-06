import os

from random import choice

import sc2

from sc2.player import Bot, Computer

from planbot import PlanBot

maps = [
    map_name[:-7]
    for map_name in
    os.listdir(os.getenv('SC2PATH') + "/Maps")
]

sc2.run_game(
    sc2.maps.get(choice(maps)),
    [
        Bot(sc2.Race.Terran, PlanBot()),
        Computer(sc2.Race.Terran,
        sc2.Difficulty.Hard)
    ],
    realtime=False,
)
