from sc2.bot_ai import BotAI
from managers.mining_manager import MiningManager

class BaseBot(BotAI):
    async def on_before_start(self):
        """
        Вызывается перед стартом.
        """
        pass

    async def on_start(self):
        """
        Вызывается единственный раз перед запуском on_step.
        """
        mine_expansion = self.expansion_locations_dict[self.start_location]
        self.mining_mgr = MiningManager(mine_expansion, self.start_location, self.workers)
        pass


    async def on_step(self, iteration):
        """
        Вызывается на каждом шаге игры.
        :param iteration:
        """
        # print(self.workers.gathering.amount)
        pass

    async def on_end(self, game_result):
        """
        Вызывается в конце игры.
        Обратить внимание запускается laddermanager
        """
        pass

    async def on_unit_destroyed(self, unit_tag):
        """
        Юнит уничтожен.
        """
        # print(f"UNIT GOT DESTROYED {unit_tag}")

    async def on_unit_created(self, unit):
        """ 
        Юнит создан
        """
        # print(f"UNIT GOT CREATED {unit}")

    async def on_unit_type_changed(self, unit, previous_type):
        """ 
        Юнит изменил свой тип
        """
        pass

    async def on_building_construction_started(self, unit):
        """
        Начата постройка.
        """
        pass

    async def on_building_construction_complete(self, unit):
        """
        Постройка завершена.
        """
        pass

    async def on_upgrade_complete(self, upgrade):
        """
        Улучшение завершено.
        """
        pass

    async def on_unit_took_damage(self, unit, amount_damage_taken):
        """
        Юнит получил урон.
        """
        pass

    async def on_enemy_unit_entered_vision(self, unit):
        """
        Увидел врага.
        """
        pass

    async def on_enemy_unit_left_vision(self, unit_tag):
        """
        Вражеский юнит покинул зону видимости.
        """
        pass
