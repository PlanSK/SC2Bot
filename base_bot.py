import sc2
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
        for worker in self.workers:
            worker.stop()

        mine_expansion = self.expansion_locations_dict[self.start_location]
        self.mining_mgr = MiningManager(mine_expansion, self.start_location, self.workers)
        await self.mining_mgr.organize_mining()

    async def on_step(self, iteration):
        """
        Вызывается на каждом шаге игры.
        :param iteration:
        """
        self.draw_sphere(self.start_location, 10)

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

    def get_xyz(self, point):
        if isinstance(point, sc2.position.Point3):
            x, y, z = point
        elif isinstance(point, sc2.position.Point2):
            x, y, z = (*point, self.get_terrain_z_height(point))
        else:
            raise NotImplementedError("get_xyz not implemented for this type")

        return (x, y, z)

    def draw_sphere(self, position, radius=1, color=None):
        x, y, z = self.get_xyz(position)
        position = sc2.position.Point3((x, y, z))
        color = (255, 255, 255) if not color else color

        self.client.debug_sphere_out(
            p=position,
            r=radius,
            color=color
        )