from base_bot import BaseBot

from managers.mining_manager import MiningManager

from managers.build_manager import BuildingManager

from managers.unit_manager import UnitManager

from wrappers.base_wrapper import BaseWrapper


class PlanBot(BaseBot):
    async def on_before_start(self):
        """
        Вызывается перед стартом.
        """
        pass

    async def on_start(self):
        """
        Вызывается единственный раз перед запуском on_step.
        """
        # for worker in self.workers: # move to unit manager
        #     worker.stop()

        self.building_mgr = BuildingManager(
            townhalls = self.townhalls,
            buildings = self.structures,
            location = self.start_location
        )

        self.unit_manager = UnitManager(
            workers = self.workers,
            townhalls = self.building_mgr.get_townhalls_wrappers()
        )

        mine_expansion = self.expansion_locations_dict[self.start_location]

        self.mining_mgr = MiningManager(
            mining_expansion = mine_expansion, 
            location = self.start_location, 
            unit_manager = self.unit_manager,
            build_manager = self.building_mgr
        )

        self.building_mgr.transer_managers(self.unit_manager, self.mining_mgr)

        await self.mining_mgr.organize_mining()
        

    async def on_step(self, iteration):
        """
        Вызывается на каждом шаге игры.
        :param iteration:
        # """
        await self.mining_mgr.control_mining()
        await self.building_mgr.supply_control()
        await self.update()
        # self.draw_sphere(self.start_location, 10)

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
        worker_unit_names = ["SCV", "DRONE", "PROBE"]
        if unit.name.upper() in worker_unit_names:
            self.unit_manager.add_worker_unit(unit)

    async def on_unit_type_changed(self, unit, previous_type):
        """ 
        Юнит изменил свой тип
        """
        pass

    async def on_building_construction_started(self, unit):
        """
        Начата постройка.
        """
        self.building_mgr.make_building_wrapper(unit)

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
