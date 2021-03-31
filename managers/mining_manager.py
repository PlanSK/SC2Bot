from loguru import logger as log

from sc2.ids.unit_typeid import UnitTypeId

from wrappers import SCV, Mineral, VespeneGeyser, VespeneFactory

from .base_manager import BaseManager

from wrappers.state import State

from .unit_manager import UnitManager


class MiningManager(BaseManager):
    def __init__(self, mining_expansion, location, worker_wrappers, unit_manager, build_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.mining_expansion = mining_expansion
        self.scv_wrappers = worker_wrappers
        self.make_mineral_wrappers()
        self.make_vespene_wrappers()
        self.unit_mgr = unit_manager
        self.build_mgr = build_manager
        self.organize_control = False
        self.gas_structures = list()
    
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
    
    def make_vespene_wrappers(self):
        self.vespene_geysers_wrappers = list()
        vespene = sorted(
            self.mining_expansion.vespene_geyser,
            key=lambda m: self.location.distance_to(m)
        )
        for geyser in vespene:
            self.vespene_geysers_wrappers.append(VespeneGeyser(tag = geyser.tag))

    def add_vespene_factory(self, vespene_factory_unit):
        self.gas_structures.append(VespeneFactory(tag = vespene_factory_unit.tag))
        log.info(f"Gas structure {vespene_factory_unit.tag} added in wrappers list")

    async def organize_mining(self):
        for mineral in self.mineral_wrappers_high:
            free_workers = self.unit_mgr.get_idle_workers()
            nearest_scv = sorted(
                free_workers,
                key=lambda m: mineral.get_unit().distance_to(m.get_unit())
            )
            for scv in nearest_scv:
                if mineral.get_workers_amount() <= 1:
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                else:
                    break

        for mineral in self.mineral_wrappers_low:
            free_workers = self.unit_mgr.get_idle_workers()
            nearest_scv = sorted(
                free_workers,
                key=lambda m: mineral.get_unit().distance_to(m.get_unit())
            )
            for scv in nearest_scv:
                if mineral.get_workers_amount() < 1:
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                else:
                    break   
        self.unit_mgr.on_call_worker_add(self.mineral_wrappers_low[-1].get_workers()[-1])
        self.mineral_wrappers_total = sorted(
            self.mineral_wrappers_total,
            key=lambda m: m.get_workers_amount()
        )

    def build_vespene_refine(self):
        # постройка фабрики
        if self.bot.can_afford(UnitTypeId.REFINERY):
            get_worker = self.unit_mgr.worker_request()
            location_gas = self.vespene_geysers_wrappers[0].get_unit()
            self.build_mgr.gas_refine_build(get_worker, location_gas)

    async def control_mining(self):
        mineral_workers_need_count = len(self.mineral_wrappers_total) * 2
        vespene_workers_need_count = len(self.vespene_geysers_wrappers) * 3
        all_collecting_workers = 0

        for mineral_wrappers in self.mineral_wrappers_total:
            all_collecting_workers += mineral_wrappers.get_workers_amount()
        # for vespene_wrapper in self.vespene_structures_wrappers:
        #     all_collecting_workers += vespene_wrapper.get_workers_amount()

        resource_workers_needed = mineral_workers_need_count + vespene_workers_need_count

        if all_collecting_workers < resource_workers_needed:
            self.unit_mgr.make_workers()

        free_scv = self.unit_mgr.get_idle_workers()

        if mineral_workers_need_count > all_collecting_workers:
            # distributing free workers to minerals
            while free_scv:
                for mineral in self.mineral_wrappers_total:
                    free_scv = self.unit_mgr.get_idle_workers()
                    nearest_scv = sorted(
                        free_scv,
                        key=lambda m: mineral.get_unit().distance_to(m.get_unit())
                    )
                    for scv in nearest_scv:
                        # print(f"Ловим бездельников :)")
                        mineral.add_worker(scv)
                        scv.mine(mineral)
                        break
        elif (all_collecting_workers >= mineral_workers_need_count 
                and (all_collecting_workers - mineral_workers_need_count) < vespene_workers_need_count):
            if not self.organize_control: # проверка существования фабрики и ее заполненности
                self.build_vespene_refine()
                self.organize_control = True
            # while free_scv:

            # distributing free workers to vespene
        else:
            # ещё какая нибудь история
            pass

    def update(self):
        pass
    
    def remove_unit(self, unit):
        print("Removing this unit.")
