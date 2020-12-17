from loguru import logger as log

from wrappers.base_wrapper import BaseWrapper

class Mineral(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        capacity = self.unit.mineral_contents
        self.workers = []
        log.info(f'Tag {self} contains {capacity}')

    def get_workers(self):
        return self.workers

    def add_worker(self, worker):
        log.info(f"Added worker {worker} to list")
        self.workers.append(worker)

    def remove_worker(self, worker):
        log.info(f"Removed worker {worker}")
