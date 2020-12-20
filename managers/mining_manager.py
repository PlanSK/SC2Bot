from loguru import logger as log

from wrappers import SCV, Mineral

from .base_manager import BaseManager

from wrappers.state import State


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

        self.mineral_wrappers_low = list()
        self.mineral_wrappers_high = list()
        self.mineral_wrappers_total = list()

        mean_minerals_value = (
            sum(m.mineral_contents for m in minerals)
            // len(minerals)
        )

        for mineral_unit in minerals:
            mineral = Mineral(tag = mineral_unit.tag)
            
            self.mineral_wrappers_total.append(mineral)

            if mineral_unit.mineral_contents > mean_minerals_value:
                self.mineral_wrappers_high.append(mineral)
            else:
                self.mineral_wrappers_low.append(mineral)
        
    def make_scv_wrappers(self):
        self.scv_wrappers = [
            SCV(tag = scv_unit.tag)
            for scv_unit in self.workers
        ]
    
    async def organize_mining(self):
        for scv in self.scv_wrappers:
            for mineral in self.mineral_wrappers_high:
                if len(mineral.get_workers()) <= 1:
                    print(f"{scv} Беру большой.")
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                    break
                
        for scv in self.scv_wrappers:
            if scv._state == State.IDLE:
                for mineral in self.mineral_wrappers_low:
                    if not mineral.get_workers():
                        print(f"{scv} Беру поменьше.")
                        mineral.add_worker(scv)
                        scv.mine(mineral)
                        break

        for scv in self.scv_wrappers:
            self.mineral_wrappers_total = sorted(
                self.mineral_wrappers_total,
                key=lambda m: m.get_workers_amount()
            )

            for mineral in self.mineral_wrappers_total:
                if scv._state == State.IDLE:
                    print("Ловим бездельников :)")
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                    break
                
    def update(self):
        pass
    
    def remove_unit(self, unit):
        print("Removing this unit.")
