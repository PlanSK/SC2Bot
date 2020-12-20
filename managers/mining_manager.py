from loguru import logger as log

from wrappers import SCV, Mineral

from .base_manager import BaseManager


class MiningManager(BaseManager):
    def __init__(self, mining_expansion, location, workers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.mining_expansion = mining_expansion
        self.workers = workers
        self.make_mineral_wrappers()
        self.make_scv_wrappers()
    
    def make_mineral_wrappers(self):
        minerals = sorted(
            self.mining_expansion.mineral_field,
            key=lambda m: self.location.distance_to(m)
        )

        self.mineral_wrappers = [
            Mineral(tag = mineral_unit.tag) 
            for mineral_unit in minerals
        ]  
    
    def make_scv_wrappers(self):
        self.scv_wrappers = [
            SCV(tag = scv_unit.tag)
            for scv_unit in self.workers
        ]
    
    async def organize_mining(self):
        for scv in self.scv_wrappers:
            for mineral in self.mineral_wrappers:
                if len(mineral.get_workers()) <= 1:
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                    break

    def update(self):
        pass
    
    def remove_unit(self, unit):
        print("Removing this unit.")
