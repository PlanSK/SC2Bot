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
        for get_crystal in sorted_minerals:
            self.mineral_wrappers.append(Mineral(unit = get_crystal))
        
        self.scv_wrappers = []
        for get_scv in workers:
            self.scv_wrappers.append(SCV(unit = get_scv))


    async def organize_mining(self):
        pass

