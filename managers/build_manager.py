from loguru import logger as log


from sc2.units import Units

from sc2.ids.unit_typeid import UnitTypeId

from sc2.ids.ability_id import AbilityId


from .base_manager import BaseManager

from wrappers import CommandCenter, VespeneFactory


class BuildingManager(BaseManager):
    def __init__(self, townhalls, buildings, location, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buildings = buildings
        self.townhalls = townhalls
        self.location = location
        self.make_townhall_wrappers()
        self.gas_structures = list()

    def make_townhall_wrappers(self):
        self.command_center_wrappers = [
            CommandCenter(tag = get_build.tag)
            for get_build in self.townhalls
        ]

    def transer_managers(self, unit_manager, mining_mgr):
        self.unit_mgr = unit_manager
        self.mining_mgr = mining_mgr

    async def supply_build(self):
        map_center = self.bot.game_info.map_center
        optimal_placement_position = self.bot.start_location.towards(map_center, distance=5)
        placement_position = await self.bot.find_placement(UnitTypeId.SUPPLYDEPOT, near=optimal_placement_position, placement_step=1)
        # Get unit to building supply depot
        if placement_position:
            build_worker = self.unit_mgr.worker_request().get_unit()
            build_worker.build(UnitTypeId.SUPPLYDEPOT, placement_position)

    def build_vespene_refine(self, vespene_geyser):
        builder = self.unit_mgr.worker_request().get_unit()
        if (self.bot.can_afford(UnitTypeId.REFINERY) and 
                not builder.order_target == vespene_geyser.get_tag()):
            builder.build(
                UnitTypeId.REFINERY, 
                vespene_geyser.get_unit()
            )

    async def supply_control(self):
        uncomplited_depots = [
            depots.tag
            for depots in self.bot.structures.not_ready
            if depots.name == "SupplyDepot"
        ]
        if (self.bot.supply_left == 1 
                and not uncomplited_depots
                and self.bot.can_afford(UnitTypeId.SUPPLYDEPOT)):
            await self.supply_build()
    
    def make_building_wrapper(self, unit):
        gas_factory_names = ["REFINERY", "ASSIMILATOR", "EXTRACTOR"]
        if unit.name.upper() in gas_factory_names:
            self.add_vespene_factory(unit)

    def add_vespene_factory(self, vespene_factory_unit):
        get_structure = VespeneFactory(tag = vespene_factory_unit.tag)
        self.gas_structures.append(get_structure)
        for geyser in self.mining_mgr.vespene_geysers_wrappers:
            print(get_structure.get_unit().distance_to(self.bot.vespene_geyser.find_by_tag(geyser.get_tag())))
            print(get_structure.get_unit().distance_to(geyser.get_unit()))

            if not get_structure.get_unit().distance_to(self.bot.vespene_geyser.find_by_tag(geyser.get_tag())):
                geyser.factory_id = vespene_factory_unit.tag
                get_structure.geyser_id = geyser.get_tag()
                log.info(f"Gas structure {get_structure.get_tag()} added in wrappers list")
                break
            else:
                log.info(f"Not found this factory on this geyser :)")

    def get_townhalls_wrappers(self):
        return self.command_center_wrappers

    def update(self):
        pass

    def remove_unit(self, unit):
        pass
