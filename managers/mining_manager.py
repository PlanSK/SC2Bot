from loguru import logger as log


from sc2.ids.unit_typeid import UnitTypeId

from sc2.units import Units


from .base_manager import BaseManager

from .unit_manager import UnitManager


from wrappers import SCV, Mineral, VespeneGeyser, VespeneFactory

from wrappers.state import State


class MiningManager(BaseManager):
    def __init__(self, mining_expansion, location, unit_manager, build_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.mining_expansion = mining_expansion
        self.make_mineral_wrappers()
        self.make_vespene_wrappers()
        self.unit_mgr = unit_manager
        self.build_mgr = build_manager
    
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
            
            if mineral_unit.mineral_contents > mean_minerals_value:
                self.mineral_wrappers_high.append(mineral)
            else:
                self.mineral_wrappers_low.append(mineral)
        
        self.mineral_wrappers_total = self.mineral_wrappers_high + self.mineral_wrappers_low
    
    def make_vespene_wrappers(self):
        vespene = sorted(
            self.mining_expansion.vespene_geyser,
            key=lambda m: self.location.distance_to(m)
        )
        self.vespene_geysers_wrappers = {
            geyser.tag: VespeneGeyser(tag = geyser.tag)
            for geyser in vespene
        }

    def organize_gas_mining(self):
        log.info(f'[GAS] Entering in gas mining organize method.')
        if self.bot.gas_buildings.ready:
            log.info('[GAS] Ready to collecting')
            # self.collecting_gas_factory(get_structure)
        elif self.bot.gas_buildings:
            log.info('[GAS] Waiting to building gas structure')
        else:
            log.info('[GAS] Start of construction GAS build.')
            for geyser in self.vespene_geysers_wrappers.values():
                self.build_mgr.build_vespene_refine(geyser)
                break

    # def collecting_gas_factory(self, vespene_factory_wrapper):
    #     log.ingo(f'Distributing workers to gas factory successful {vespene_factory_wrapper.get_tag()}')
    #     free_workers = self.unit_mgr.get_idle_workers()
    #     for worker in free_workers:
    #         worker.get_unit().gather(vespene_factory_wrapper.get_unit())
    #         vespene_factory_wrapper.add_worker(worker)

    def distribution_of_workers_to_minerals(self, mineral_wrapper_list: list):
        for mineral in mineral_wrapper_list:
            free_workers = self.unit_mgr.get_idle_workers()
            nearest_scv = sorted(
                free_workers.values(),
                key=lambda m: mineral.get_unit().distance_to(m.get_unit())
            )
            for scv in nearest_scv:
                if mineral.get_workers_amount() <= 1:
                    mineral.add_worker(scv)
                    scv.mine(mineral)
                else:
                    break

    async def organize_mining(self):
        """Назначает рабочих на минералы в зависимости от содержания в них 
        минералов, а также устанавливает рабочего по умолчанию и передает 
        его в Unit Manager. 

        После этого производит сортировку по количеству рабочих на минералах
        """

        self.distribution_of_workers_to_minerals(self.mineral_wrappers_high)
        self.distribution_of_workers_to_minerals(self.mineral_wrappers_low)

        # Moving to unit manager
        for wrapper in self.mineral_wrappers_total[::-1]:
            if wrapper.get_workers_amount():
                self.unit_mgr.on_call_worker_add(wrapper.get_workers()[-1])
                break

        # Moving to method of filling mineral wrapper
        self.mineral_wrappers_total = sorted(
            self.mineral_wrappers_total,
            key=lambda m: m.get_workers_amount()
        )

    async def control_mining(self):
        # Moving this to method of filling mineral wrapper
        mineral_workers_need_count = len(self.mineral_wrappers_total) * 2
        collecting_mineral_workers = 0

        for mineral_wrappers in self.mineral_wrappers_total:
            collecting_mineral_workers += mineral_wrappers.get_workers_amount()

        if collecting_mineral_workers < mineral_workers_need_count:
            self.unit_mgr.make_workers()

        free_scv = self.unit_mgr.get_idle_workers()

        if mineral_workers_need_count > collecting_mineral_workers:
            while free_scv:
                for mineral in self.mineral_wrappers_total:
                    free_scv = self.unit_mgr.get_idle_workers()
                    nearest_scv = sorted(
                        free_scv.values(),
                        key=lambda m: mineral.get_unit().distance_to(m.get_unit())
                    )
                    for scv in nearest_scv:
                        mineral.add_worker(scv)
                        scv.mine(mineral)
                        break
        else:
            self.organize_gas_mining()

    def update(self):
        pass
    
    def remove_unit(self, unit):
        print("Removing this unit.")
