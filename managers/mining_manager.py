from collections import OrderedDict

from wrappers import SCV, Mineral

from .base_manager import BaseManager


class MiningManager(BaseManager):
    def __init__(self, mine_expansion, location, workers):
        self.location = location
        minerals = mine_expansion.mineral_field
        vespene = mine_expansion.vespene_geyser

        unsorted_minerals = {}
        for m in minerals:
            unsorted_minerals[location.position.distance_to(m)] = m

        sorted_minerals = [unsorted_minerals[dist] for dist in sorted(unsorted_minerals)]

        self.mineral_wrappers = []
        for mineral_unit in sorted_minerals:
            self.mineral_wrappers.append(Mineral(unit = mineral_unit))
        
        self.scv_wrappers = []
        for scv_unit in workers:
            self.scv_wrappers.append(SCV(unit = scv_unit))


    async def organize_mining(self):
        for scv in self.scv_wrappers:
            for mineral in self.mineral_wrappers:
                if len(mineral.get_workers()) <= 2:
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                    break


        pass

