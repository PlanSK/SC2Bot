from loguru import logger as log

from wrappers import SCV, Mineral

from .base_manager import BaseManager


class MiningManager(BaseManager):
    def __init__(self, mine_expansion, location, workers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.mine_expansion = mine_expansion
        minerals = mine_expansion.mineral_field
        vespene = mine_expansion.vespene_geyser

        unsorted_minerals = {}
        for m in minerals:
            unsorted_minerals[location.position.distance_to(m)] = m

        sorted_minerals = [unsorted_minerals[dist] for dist in sorted(unsorted_minerals)]

        self.mineral_wrappers = []
        for mineral_unit in sorted_minerals:
            self.mineral_wrappers.append(Mineral(tag = mineral_unit.tag))
        
        self.scv_wrappers = []
        for scv_unit in workers:
            self.scv_wrappers.append(SCV(tag = scv_unit.tag))
    
    async def update_mineral_units(self, mine_expansion):
        pass


    async def organize_mining(self):
        for scv in self.scv_wrappers:
            for mineral in self.mineral_wrappers:
                if len(mineral.get_workers()) <= 1:
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                    break

    async def control_mining(self):
        for scv in self.scv_wrappers:
            orders = str(scv.get_unit().orders)
            ability_name = orders.find("Gather")
            ability_tag = int(orders.split()[1][:-1])
            if ability_name >= 0:
                print(f"Worker {scv} = {orders}")
                # if ability_tag != scv.get_my_mineral().get_unit().tag:
                #     print(f"Worker {scv}::::{ability_tag}/{scv.get_my_mineral().get_unit().tag}")
                # else:
                #     print(f"Ok, Worker {scv}::::{ability_tag}/{scv.get_my_mineral().get_unit().tag}")
        print("=" * 30)

    def update(self):
        pass
    
    def remove_unit(self, unit):
        print("Removing this unit.")
