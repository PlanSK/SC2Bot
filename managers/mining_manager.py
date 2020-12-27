from loguru import logger as log

from sc2.ids.unit_typeid import UnitTypeId

from wrappers import SCV, Mineral

from .base_manager import BaseManager

from wrappers.state import State


class MiningManager(BaseManager):
    def __init__(self, mining_expansion, location, workers, townhalls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.mining_expansion = mining_expansion
        self.workers = workers
        self.townhalls = townhalls
        self.make_scv_wrappers()
        self.make_mineral_wrappers()
    
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
    
    def add_scv_unit(self, unit):
        if unit.tag not in [wrapper.get_tag() for wrapper in self.scv_wrappers]:
            unit.stop()
            self.scv_wrappers.append(SCV(tag = unit.tag))
            print(f"I'm adding {unit.tag} in wrappers list")

    async def idler_hunter(self):
        free_scv = [
            scv 
            for scv in self.scv_wrappers 
            if scv._state == State.IDLE
        ]

        while free_scv:
            for mineral in self.mineral_wrappers_total:
                free_scv = [
                    scv 
                    for scv in self.scv_wrappers 
                    if scv._state == State.IDLE
                ]
                nearest_scv = sorted(
                    free_scv,
                    key=lambda m: mineral.get_unit().distance_to(m.get_unit())
                )
                for scv in nearest_scv:
                    print(f"Ловим бездельников :)")
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                    break

    async def organize_mining(self):
        for mineral in self.mineral_wrappers_high:
            nearest_scv = sorted(
                [scv for scv in self.scv_wrappers if scv._state == State.IDLE],
                key=lambda m: mineral.get_unit().distance_to(m.get_unit())
            )
            for scv in nearest_scv:
                if mineral.get_workers_amount() <= 1:
                    print(f"{scv} Беру большой и толстый.")
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                else:
                    break

        for mineral in self.mineral_wrappers_low:
            nearest_scv = sorted(
                [scv for scv in self.scv_wrappers if scv._state == State.IDLE],
                key=lambda m: mineral.get_unit().distance_to(m.get_unit())
            )
            for scv in nearest_scv:
                if mineral.get_workers_amount() < 1:
                    print(f"{scv} Беру поменьше.")
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                else:
                    break   
        
        self.mineral_wrappers_total = sorted(
            self.mineral_wrappers_total,
            key=lambda m: m.get_workers_amount()
        )

        await self.idler_hunter()

    async def control_mining(self):
        await self.idler_hunter()

        mineral_workers_need_count = len(self.mineral_wrappers_total) * 2
        all_collecting_workers = 0
        for mineral_wrappers in self.mineral_wrappers_total:
            all_collecting_workers += mineral_wrappers.get_workers_amount()
        vespene_workers_need_count = 2 * 3
        # remake to counter of vespene geizer wrappers

        resource_workers_needed = mineral_workers_need_count + vespene_workers_need_count
        unit_type = UnitTypeId.SCV

        if len(self.scv_wrappers) < mineral_workers_need_count:
            if self.bot.supply_left > 1:
                if (self.bot.can_afford(unit_type) 
                        and not len(self.townhalls[0].get_unit().orders)):
                    self.townhalls[0].train_unit(unit_type)
            # else:
                # supply warning!


    def update(self):
        pass
    
    def remove_unit(self, unit):
        print("Removing this unit.")
