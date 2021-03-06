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
        self.my_race = self.workers[0].race

    def make_worker_wrappers(self):
        if self.my_race == Race.Terran:
            self.worker_wrappers = [
                SCV(tag = worker_unit.tag)
                for worker_unit in self.workers
            ]
    
    def add_worker_unit(self, unit):
        if unit.tag not in [wrapper.get_tag() for wrapper in self.worker_wrappers]:
            unit.stop()
            if unit.race == Race.Terran:
                self.worker_wrappers.append(SCV(tag = unit.tag))
            elif unit.race == Race.Protoss:
                pass
            elif unit.race == Race.Zerg:
                pass

    def make_workers(self):
        self.townhalls[0].update()

        if self.my_race == Race.Terran:
            unit_type = UnitTypeId.SCV
        elif self.my_race == Race.Protoss:
            pass
        elif self.my_race == Race.Zerg:
            pass

        if (self.bot.can_afford(unit_type) 
                and not len(self.townhalls[0].get_unit().orders)):
            self.townhalls[0].train_unit(unit_type)

    def worker_request(self):
        free_worker_wrappers = list()
        for get_wrapper in self.worker_wrappers:
            if get_wrapper.get_state() == State.IDLE:
                free_worker_wrappers.append(get_wrapper)
        if free_worker_wrappers:
            return free_worker_wrappers[0]
        else:
            return self.on_call_worker

    def on_call_worker_add(self, worker):
        for scv in self.worker_wrappers:
            if scv.get_tag() == worker:
                self.on_call_worker = scv

    def get_worker_wrappers_list(self):
        return self.worker_wrappers

    def update(self):
        pass

    def remove_unit(self, unit):
        print("NOT IMPLEMENTED LOGIC FOR UNIT REMOVAL")