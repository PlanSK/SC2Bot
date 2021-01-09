from wrappers import CommandCenter

from sc2.units import Units

from sc2.ids.unit_typeid import UnitTypeId

from .base_manager import BaseManager


class BuildingManager(BaseManager):
    def __init__(self, townhalls, buildings, location, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buildings = buildings
        self.townhalls = townhalls
        self.location = location
        self.make_buildings_wrappers()

    def make_buildings_wrappers(self):
        self.command_center_wrappers = [
            CommandCenter(tag = get_build.tag)
            for get_build in self.townhalls
            # if get_build.name == "CommandCenter"
        ]

    async def supply_build(self):
        map_center = self.bot.game_info.map_center
        optimal_placement_position = self.bot.start_location.towards(map_center, distance=5)
        placement_position = await self.bot.find_placement(UnitTypeId.SUPPLYDEPOT, near=optimal_placement_position, placement_step=1)
        # Get unit to building supply depot
        if placement_position:
            build_worker = self.bot.workers.closest_to(placement_position)
            build_worker.build(UnitTypeId.SUPPLYDEPOT, placement_position)


    async def supply_control(self):
        uncomplited_depots = [
            depots.tag
            for depots in self.bot.structures 
            if depots.name == "SupplyDepot" and depots.build_progress < 1.0
        ]
        if (self.bot.supply_left == 1 
                and not uncomplited_depots
                and self.bot.can_afford(UnitTypeId.SUPPLYDEPOT)):
            await self.supply_build()
    
    def get_townhalls_wrappers(self):
        return self.command_center_wrappers

    def update(self):
        pass