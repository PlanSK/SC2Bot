from sc2.data import Race

from sc2.ids.unit_typeid import UnitTypeId


from .base_manager import BaseManager


from wrappers import SCV, Mineral

from wrappers.state import State


class UnitManager(BaseManager):
    def __init__(self, workers, townhalls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workers = workers
        self.townhalls = townhalls
        self.all_workers_stop()
        self.make_worker_wrappers()

    def all_workers_stop(self):
        for worker_unit in self.workers:
            worker_unit.stop()

    def make_worker_wrappers(self):
        if self.bot.race == Race.Terran:
            self.worker_wrappers = {
                worker_unit.tag: SCV(tag = worker_unit.tag)
                for worker_unit in self.workers
            }
    
    def add_worker_unit(self, unit):
        if unit.tag not in self.worker_wrappers.keys():
            unit.stop()
            if self.bot.race == Race.Terran:
                self.worker_wrappers[unit.tag] = (SCV(tag = unit.tag))
            elif self.bot.race == Race.Protoss:
                pass
            elif self.bot.race == Race.Zerg:
                pass

    def make_workers(self):
        self.townhalls[0].update()

        if self.bot.race == Race.Terran:
            unit_type = UnitTypeId.SCV
        elif self.bot.race == Race.Protoss:
            pass
        elif self.bot.race == Race.Zerg:
            pass

        if (self.bot.can_afford(unit_type) and 
                not len(self.townhalls[0].get_unit().orders)):
            self.townhalls[0].train_unit(unit_type)

    def worker_request(self):
        free_worker_wrappers = self.get_idle_workers()
        if free_worker_wrappers.keys():
            return next(iter(free_worker_wrappers.values()))
        else:
            return self.on_call_worker

    def on_call_worker_add(self, worker):
        self.on_call_worker = self.worker_wrappers[worker]

    def get_worker_wrappers_list(self) -> dict:
        return self.worker_wrappers

    def get_idle_workers(self) -> dict:
        """Method returning free worker wrappers list."""

        free_workers = {
            tag: wrapper
            for tag, wrapper in self.worker_wrappers.items()
            if wrapper.get_state() == State.IDLE
        }
        return free_workers

    def update(self):
        pass

    def remove_unit(self, unit):
        print("NOT IMPLEMENTED LOGIC FOR UNIT REMOVAL")
