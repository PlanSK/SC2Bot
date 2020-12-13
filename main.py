import sc2
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer

class MyBot(BotAI):
    async def on_step(self, iteration: int):
        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])

sc2.run_game(
    sc2.maps.get("CatalystLE_NOAI"),
    [
        Bot(sc2.Race.Terran, MyBot()),
        Computer(sc2.Race.Terran,
        sc2.Difficulty.Hard)
    ],
    realtime=False,
)
